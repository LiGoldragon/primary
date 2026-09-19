#!/usr/bin/env python3
"""Refresh an idle native Claude seat through one slash-command turn per skill.

The manifest is the audited contract for one existing seat.  This helper never
chooses a model, effort, role, predecessor, or source set.  It checks those
facts before it types into the native Claude session, and records only an
observed native Skill invocation as a skill-expansion receipt.
"""

import argparse
import hashlib
import json
import os
import pathlib
import socket
import subprocess
import sys
import time


ROOT = pathlib.Path(__file__).resolve().parent.parent
DAEMON_ROOT = pathlib.Path(f"/tmp/cc-daemon-{os.getuid()}")
KEY_PATH = pathlib.Path.home() / ".claude/daemon/control.key"
PROJECT_ROOT = pathlib.Path.home() / ".claude/projects"


def load_manifest(path):
    data = json.loads(pathlib.Path(path).read_text())
    required = ("session_id", "model", "effort", "role", "skills", "sources")
    absent = [key for key in required if not data.get(key)]
    if absent:
        raise ValueError("manifest missing: " + ", ".join(absent))
    if "main-flow" not in data["skills"]:
        raise ValueError("manifest must include main-flow")
    if len(data["skills"]) != len(set(data["skills"])):
        raise ValueError("manifest repeats a skill")
    if data.get("resumed_skills"):
        raise ValueError("resuming skills requires a recorded generation receipt; start a fresh bootstrap generation")
    return data


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_sources(manifest, cwd):
    witnessed = []
    for source in manifest["sources"]:
        relative = source.get("path")
        if not relative or pathlib.PurePath(relative).is_absolute():
            raise ValueError("source path must be workspace-relative")
        file = cwd / relative
        if not file.is_file():
            raise ValueError(f"source missing: {relative}")
        actual = sha256(file)
        expected = source.get("sha256")
        if not expected:
            raise ValueError(f"source hash missing: {relative}")
        if actual != expected:
            raise ValueError(f"source changed since manifest: {relative}")
        witnessed.append({"path": relative, "sha256": actual, "body": file.read_text().rstrip()})
    return witnessed


def validate_skills(manifest, cwd):
    result = []
    for name in manifest["skills"]:
        file = cwd / ".claude" / "skills" / name / "SKILL.md"
        if not file.is_file():
            raise ValueError(f"native Claude skill unavailable: {name}")
        result.append({"name": name, "path": str(file), "sha256": sha256(file)})
    return result


def agents():
    return json.loads(subprocess.check_output(["claude", "agents", "--json"], text=True))


def idle_agent(session_id):
    agent = next((item for item in agents() if item.get("sessionId") == session_id), None)
    if not agent:
        raise RuntimeError("native Claude session is not listed")
    if agent.get("status") != "idle":
        raise RuntimeError(f"native Claude session is not idle: {agent.get('status', agent.get('state'))}")
    return agent


def wait_for_idle(session_id, deadline):
    last = None
    while time.monotonic() < deadline:
        try:
            return idle_agent(session_id)
        except RuntimeError as error:
            last = error
            time.sleep(0.5)
    raise last or RuntimeError("native Claude session did not become idle")


def transcript_path(cwd, session_id, required=True):
    encoded = "-" + str(cwd).strip("/").replace("/", "-")
    path = PROJECT_ROOT / encoded / f"{session_id}.jsonl"
    if required and not path.is_file():
        raise RuntimeError(f"native Claude transcript unavailable: {path}")
    return path


def transcript_entries(path):
    if not path.is_file():
        return []
    entries = []
    for line in path.read_text().splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def observed_identity(entries):
    models, efforts = [], []
    for entry in entries:
        attachment = entry.get("attachment", {})
        identity = attachment.get("identity", {})
        model = identity.get("modelId") or identity.get("model")
        if model:
            models.append(model)
        effort = identity.get("effort") or identity.get("effortLevel")
        if effort:
            efforts.append(effort)
        model = entry.get("message", {}).get("model")
        if model:
            models.append(model)
        effort = entry.get("message", {}).get("effort") or entry.get("message", {}).get("effortLevel")
        if effort:
            efforts.append(effort)
    return {"model": models[-1] if models else None, "effort": efforts[-1] if efforts else None}


def observed_model(entries):
    return observed_identity(entries)["model"]


def model_matches(configured, observed):
    """Claude records the canonical ID while a launch may request its [1m] context form."""
    return observed == configured or (configured.endswith("[1m]") and observed == configured.removesuffix("[1m]"))


def skill_receipt(entries, name):
    for entry in entries:
        message = entry.get("message", {})
        companion = entry.get("isMeta") and entry.get("turnCompanion")
        companion_content = message.get("content", [])
        if companion and isinstance(companion_content, list):
            for block in companion_content:
                if isinstance(block, dict) and block.get("type") == "text":
                    marker = f"Base directory for this skill: {ROOT}/.claude/skills/{name}"
                    if marker in block.get("text", ""):
                        return True
    return False


def has_skill(entries, name):
    return skill_receipt(entries, name)


def transcript_digest(entries):
    return hashlib.sha256("\n".join(json.dumps(item, sort_keys=True) for item in entries).encode()).hexdigest()


def assistant_text(entries):
    text = []
    for entry in entries:
        if entry.get("type") not in ("assistant", None):
            continue
        for block in entry.get("message", {}).get("content", []):
            if isinstance(block, dict) and block.get("type") == "text":
                text.append(block.get("text", ""))
    return "\n".join(text)


def daemon_socket():
    sockets = sorted(DAEMON_ROOT.glob("*/control.sock"))
    if len(sockets) != 1:
        raise RuntimeError(f"expected one Claude control socket, found {len(sockets)}")
    if not KEY_PATH.is_file():
        raise RuntimeError("Claude daemon control key unavailable")
    return sockets[0], KEY_PATH.read_text().strip()


def inject(short_id, text):
    control, key = daemon_socket()
    conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    conn.settimeout(2)
    conn.connect(str(control))
    request = {
        "proto": 1, "op": "attach", "short": short_id, "auth": key,
        "cols": 120, "rows": 40, "attachId": os.urandom(8).hex(),
        "caps": {"imark": False, "terminal": "xterm", "mux": None, "ssh": False},
    }
    conn.sendall((json.dumps(request) + "\n").encode())
    header = conn.recv(4096).split(b"\n", 1)[0]
    if b'"ok":true' not in header:
        raise RuntimeError(f"Claude attach refused: {header[:200]!r}")
    time.sleep(0.3)
    conn.sendall(b"\x15")
    body = text.encode()
    if b"\n" in body:
        body = b"\x1b[200~" + body + b"\x1b[201~"
    conn.sendall(body)
    time.sleep(0.2)
    conn.sendall(b"\r")
    conn.close()


def resolve_native_id(session_id):
    matches = [item for item in agents() if item.get("sessionId") == session_id]
    if len(matches) != 1 or not matches[0].get("id"):
        raise RuntimeError("native UUID does not resolve uniquely")
    short = matches[0]["id"]
    if sum(item.get("sessionId", "").startswith(short) for item in agents()) != 1:
        raise RuntimeError("native daemon short identifier is ambiguous")
    return short


def wait_for_skill(path, name, start_at, deadline):
    while time.monotonic() < deadline:
        entries = transcript_entries(path)
        if skill_receipt(entries[start_at:], name):
            return {"entry_start": start_at, "entry_end": len(entries), "generation": transcript_digest(entries[:start_at])}
        time.sleep(0.5)
    raise RuntimeError(f"native expansion receipt missing for /{name}")


def role_prompt(manifest, sources):
    provenance = "\n\n".join(
        f"## Source: `{item['path']}`\n\nSHA-256: `{item['sha256']}`\n\n{item['body']}"
        for item in sources
    )
    return (
        f"# Native Claude main-flow refresh\n\n"
        f"You are {manifest['role']}. Preserve the witnessed native model `{manifest['model']}` "
        f"and effort `{manifest['effort']}`. Your immediate predecessor is "
        f"`{manifest.get('predecessor', 'not supplied')}`; this does not retire, replace, "
        f"or deregister it. Do not claim a new Flow identity until the native Mainflow receipt "
        f"has been witnessed.\n\n"
        f"The applicable native skills were each invoked in separate user turns: "
        f"{', '.join(manifest['skills'])}. The following source bundle is provenance-bearing "
        f"handoff material, not a deployment or retirement instruction.\n\n{provenance}\n\n"
        "BOOTSTRAP ONLY: do not claim identity, invoke tools, delegate, edit, commit, register, "
        "or retire anything. Acknowledge this exact payload by replying only `BOOTSTRAP_READY "
        + payload_hash(manifest, sources) + "`."
    )


def payload_hash(manifest, sources):
    payload = {"session_id": manifest["session_id"], "model": manifest["model"],
               "effort": manifest["effort"], "role": manifest["role"],
               "skills": manifest["skills"],
               "sources": [{key: item[key] for key in ("path", "sha256")} for item in sources]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def plan(manifest, cwd):
    skills = validate_skills(manifest, cwd)
    sources = validate_sources(manifest, cwd)
    return {"session_id": manifest["session_id"], "model": manifest["model"],
            "effort": manifest["effort"], "role": manifest["role"],
            "skills": skills, "sources": [{k: v for k, v in item.items() if k != "body"} for item in sources],
            "ready_requires": "idle native session, observed model match, and Skill(main-flow) transcript receipt"}


def refresh(manifest, cwd, timeout, sender=inject):
    receipt = plan(manifest, cwd)
    agent = wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
    if pathlib.Path(agent.get("cwd", "")).resolve() != cwd:
        raise RuntimeError("native Claude session cwd differs from manifest cwd")
    path = transcript_path(cwd, manifest["session_id"], required=False)
    entries = transcript_entries(path)
    if not entries and not manifest.get("disposable"):
        raise RuntimeError(f"native Claude transcript unavailable: {path}")
    identity = observed_identity(entries)
    if identity["model"] and not model_matches(manifest["model"], identity["model"]):
        raise RuntimeError(f"native Claude model mismatch: expected {manifest['model']}, observed {identity['model']}")
    if identity["effort"] and identity["effort"] != manifest["effort"]:
        raise RuntimeError(f"native Claude effort mismatch: expected {manifest['effort']}, observed {identity['effort']}")
    short = resolve_native_id(manifest["session_id"])
    skill_receipts = []
    for skill in manifest["skills"]:
        wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
        start_at = len(transcript_entries(path))
        sender(short, f"/{skill}")
        skill_receipts.append({"skill": skill, **wait_for_skill(path, skill, start_at, time.monotonic() + timeout)})
        identity = observed_identity(transcript_entries(path))
        if not model_matches(manifest["model"], identity["model"]) or identity["effort"] != manifest["effort"]:
            raise RuntimeError(f"native identity mismatch: expected {manifest['model']}/{manifest['effort']}, observed {identity['model']}/{identity['effort']}")
    wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
    sources = validate_sources(manifest, cwd)
    prompt = role_prompt(manifest, sources)
    prompt_start = len(transcript_entries(path))
    sender(short, prompt)
    deadline = time.monotonic() + timeout
    expected_ack = "BOOTSTRAP_READY " + payload_hash(manifest, sources)
    while time.monotonic() < deadline:
        current = transcript_entries(path)
        if expected_ack in assistant_text(current[prompt_start:]):
            break
        time.sleep(0.5)
    else:
        raise RuntimeError("native source-payload acknowledgement missing")
    identity = observed_identity(transcript_entries(path))
    if not model_matches(manifest["model"], identity["model"]) or identity["effort"] != manifest["effort"]:
        raise RuntimeError("native identity changed during bootstrap")
    receipt["native_main_flow"] = {"skill": "main-flow", "transcript": str(path), "observed": True}
    receipt["generation"] = {"session_id": manifest["session_id"], "skills": skill_receipts,
                             "source_payload_hash": payload_hash(manifest, sources), "acknowledged": expected_ack}
    receipt["observed_identity"] = identity
    receipt["predecessor_retired"] = False
    receipt["registration_performed"] = False
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--cwd", default=str(ROOT))
    parser.add_argument("--timeout", type=float, default=45)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--acknowledge-live-refresh", action="store_true")
    args = parser.parse_args()
    manifest = load_manifest(args.manifest)
    cwd = pathlib.Path(args.cwd).resolve()
    if args.refresh and not args.acknowledge_live_refresh:
        raise SystemExit("--refresh requires --acknowledge-live-refresh")
    result = refresh(manifest, cwd, args.timeout) if args.refresh else plan(manifest, cwd)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
