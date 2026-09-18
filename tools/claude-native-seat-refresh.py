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
        if expected and actual != expected:
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


def transcript_path(cwd, session_id):
    encoded = "-" + str(cwd).strip("/").replace("/", "-")
    path = PROJECT_ROOT / encoded / f"{session_id}.jsonl"
    if not path.is_file():
        raise RuntimeError(f"native Claude transcript unavailable: {path}")
    return path


def transcript_entries(path):
    entries = []
    for line in path.read_text().splitlines():
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def observed_model(entries):
    models = []
    for entry in entries:
        attachment = entry.get("attachment", {})
        identity = attachment.get("identity", {})
        model = identity.get("modelId")
        if model:
            models.append(model)
        model = entry.get("message", {}).get("model")
        if model:
            models.append(model)
    return models[-1] if models else None


def has_skill(entries, name):
    for entry in entries:
        for block in entry.get("message", {}).get("content", []):
            if block.get("type") != "tool_use" or block.get("name") != "Skill":
                continue
            value = block.get("input", {})
            if value.get("skill") == name or value.get("name") == name:
                return True
    return False


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


def wait_for_skill(path, name, start_at, deadline):
    while time.monotonic() < deadline:
        if has_skill(transcript_entries(path)[start_at:], name):
            return
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
        "State the model and effort you were actually given, preserve open work and ancestry, "
        "and wait for the main flow's bounded delegation."
    )


def plan(manifest, cwd):
    skills = validate_skills(manifest, cwd)
    sources = validate_sources(manifest, cwd)
    return {"session_id": manifest["session_id"], "model": manifest["model"],
            "effort": manifest["effort"], "role": manifest["role"],
            "skills": skills, "sources": [{k: v for k, v in item.items() if k != "body"} for item in sources],
            "ready_requires": "idle native session, observed model match, and Skill(main-flow) transcript receipt"}


def refresh(manifest, cwd, timeout):
    receipt = plan(manifest, cwd)
    agent = idle_agent(manifest["session_id"])
    if pathlib.Path(agent.get("cwd", "")).resolve() != cwd:
        raise RuntimeError("native Claude session cwd differs from manifest cwd")
    path = transcript_path(cwd, manifest["session_id"])
    model = observed_model(transcript_entries(path))
    if model != manifest["model"]:
        raise RuntimeError(f"native Claude model mismatch: expected {manifest['model']}, observed {model}")
    short = manifest["session_id"].split("-", 1)[0]
    for skill in manifest["skills"]:
        idle_agent(manifest["session_id"])
        start_at = len(transcript_entries(path))
        inject(short, f"/{skill}")
        wait_for_skill(path, skill, start_at, time.monotonic() + timeout)
    idle_agent(manifest["session_id"])
    sources = validate_sources(manifest, cwd)
    inject(short, role_prompt(manifest, sources))
    receipt["native_main_flow"] = {"skill": "main-flow", "transcript": str(path), "observed": True}
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
