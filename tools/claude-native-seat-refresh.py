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
import re


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
    if "main-flow" not in data["skills"] or "testing-flow-titles" not in data["skills"]:
        raise ValueError("manifest must include main-flow and testing-flow-titles")
    if len(data["skills"]) != len(set(data["skills"])):
        raise ValueError("manifest repeats a skill")
    if "nativeTitle" in data or canonical_role(data["role"]) is None:
        raise ValueError("manifest requires a canonical role without an arbitrary nativeTitle")
    aspect, power = canonical_role(data["role"])
    if data.get("titlePlan") != {"aspect": aspect, "power": power, "afterOwnVerifiedFlowId": True,
                                  "template": f"{aspect} {power} <FLOW_ID>"}:
        raise ValueError("manifest title plan differs from canonical role")
    audit = data.get("sourceAudit")
    if not isinstance(audit, dict) or not isinstance(audit.get("reviewedAt"), str) or not isinstance(audit.get("newestApplicableVision"), list) or not audit["newestApplicableVision"]:
        raise ValueError("manifest requires an audited newest applicable Vision declaration")
    if any(item not in [source.get("path") for source in data["sources"]] for item in audit["newestApplicableVision"]):
        raise ValueError("audited newest applicable Vision must be in sources")
    if data.get("resumed_skills"):
        raise ValueError("resuming skills requires a recorded generation receipt; start a fresh bootstrap generation")
    return data


def canonical_role(role):
    match = re.fullmatch(r"(Psyche|Mind|Field) (High|Medium|Low|Ultra Low)", role or "")
    if match:
        return match.groups()
    return {"Field Astra": ("Field", "High"), "Field Sol": ("Field", "Medium"),
            "Mind Astra": ("Mind", "High"), "Mind Sol": ("Mind", "Medium")}.get(role)


def provisional_title(manifest):
    aspect, power = canonical_role(manifest["role"])
    return f"{aspect} {power} (claim pending)"


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


def herdr_agent(target):
    value = json.loads(subprocess.check_output(
        ["herdr", "--session", target["session"], "agent", "get", target["agent"]], text=True))
    agent = value.get("result", value).get("agent")
    if not agent or any((agent.get(key) != expected for key, expected in (
            ("name", target["agent"]), ("pane_id", target["pane"]),
            ("terminal_id", target["terminal"]), ("agent", "claude")))):
        raise RuntimeError("Herdr Claude target binding changed")
    if agent.get("interactive_ready") is not True:
        raise RuntimeError("Herdr Claude target is not interactive ready")
    return agent


def wait_for_herdr_idle(target, deadline):
    while time.monotonic() < deadline:
        agent = herdr_agent(target)
        if (agent.get("agent_status") or agent.get("status")) in ("idle", "done"):
            return agent
        time.sleep(0.5)
    raise RuntimeError("Herdr Claude target did not become idle")


def herdr_send(target, message):
    herdr_agent(target)
    subprocess.check_call(["herdr", "--session", target["session"], "agent", "prompt",
                           target["pane"], message], stdout=subprocess.DEVNULL)


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


def require_transcript_uuid(entries, session_id):
    if any(entry.get("sessionId") not in (None, session_id) for entry in entries):
        raise RuntimeError("native Claude transcript contains another session UUID")


def validate_bootstrap_failed_state(state, manifest, cwd, target, transcript):
    """Corroborate the prior failure; live process checks remain authoritative."""
    seats = state.get("seats")
    if state.get("version") != 1 or not isinstance(seats, list) or len(seats) != 1:
        raise RuntimeError("running bootstrap requires one failed seat")
    seat = seats[0]
    expected = (target["pane"], target["terminal"], manifest["session_id"])
    if (seat.get("phase") != "failed" or
            (seat.get("paneId"), seat.get("terminalId"), seat.get("nativeThreadId")) != expected or
            (seat.get("retained") or {}).get("paneId") != target["pane"] or
            (seat.get("retained") or {}).get("terminalId") != target["terminal"] or
            (seat.get("retained") or {}).get("nativeThreadId") != manifest["session_id"] or
            seat.get("receipt") is None):
        raise RuntimeError("running bootstrap failed-state identity differs")
    if f"native Claude transcript unavailable: {transcript}" not in seat.get("error", ""):
        raise RuntimeError("running bootstrap failure phase differs")
    previous = state.get("manifest", {})
    declared = previous.get("seats", [])
    if (previous.get("cwd") != str(cwd) or previous.get("session") != target["session"] or
            len(declared) != 1 or declared[0].get("model") != manifest["model"] or
            declared[0].get("effort") != manifest["effort"] or
            declared[0].get("agent") != target["agent"]):
        raise RuntimeError("running bootstrap failed-state profile differs")


def validate_running_empty_bootstrap(manifest, cwd, target, transcript, receipt_path, agent,
                                     native_agents, process_info, environment, job_dir, process_started_ms):
    """Validate an already running, never-prompted session before its first input."""
    session_id = manifest["session_id"]
    if (not target or receipt_path is None or transcript.exists() or transcript.is_symlink() or
            receipt_path.exists() or receipt_path.is_symlink() or not receipt_path.parent.is_dir()):
        raise RuntimeError("running bootstrap requires absent transcript and output receipt")
    if (agent.get("agent_status") or agent.get("status")) != "idle" or agent.get("interactive_ready") is not True:
        raise RuntimeError("running bootstrap target is not idle and interactive")
    matches = [item for item in native_agents if item.get("sessionId") == session_id]
    if len(matches) != 1 or matches[0].get("cwd") != str(cwd) or matches[0].get("status") != "idle":
        raise RuntimeError("running bootstrap native session is not unique and idle")
    processes = process_info.get("foreground_processes", [])
    exact = [item for item in processes if item.get("argv") ==
             ["claude", "--session-id", session_id, "--model", manifest["model"], "--effort", manifest["effort"]]]
    if process_info.get("pane_id") != target["pane"] or len(exact) != 1 or matches[0].get("pid") != exact[0].get("pid"):
        raise RuntimeError("VerifierUnavailable: running bootstrap native process identity differs")
    if (not isinstance(process_started_ms, int) or not isinstance(matches[0].get("startedAt"), int) or
            abs(matches[0]["startedAt"] - process_started_ms) > 10_000):
        raise RuntimeError("VerifierUnavailable: running bootstrap process start time differs")
    if (environment.get("CLAUDE_JOB_DIR") != str(job_dir) or
            any(environment.get(key) for key in ("CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_KIND", "CLISESSIONID")) or
            environment.get("CLAUDE_CODE_SESSION_ID") not in (None, "", session_id)):
        raise RuntimeError("running bootstrap native environment differs")
    if job_dir.is_symlink() or not job_dir.is_dir() or any(job_dir.iterdir()):
        raise RuntimeError("running bootstrap job directory is not empty")


def running_empty_bootstrap_preflight(manifest, cwd, target, transcript, receipt_path, agent, failed_state):
    validate_bootstrap_failed_state(failed_state, manifest, cwd, target, transcript)
    native_agents = agents()
    response = json.loads(subprocess.check_output(
        ["herdr", "--session", target["session"], "pane", "process-info", "--pane", target["pane"]], text=True))
    info = response.get("result", response).get("process_info", {})
    exact = [item for item in info.get("foreground_processes", []) if item.get("argv") ==
             ["claude", "--session-id", manifest["session_id"], "--model", manifest["model"], "--effort", manifest["effort"]]]
    if len(exact) != 1 or not isinstance(exact[0].get("pid"), int):
        raise RuntimeError("running bootstrap native process identity differs")
    environment = {}
    pid=exact[0]["pid"]
    stat=pathlib.Path(f"/proc/{pid}/stat").read_text()
    ticks=int(stat.rsplit(")", 1)[1].split()[19])
    boot=int(next(line.split()[1] for line in pathlib.Path("/proc/stat").read_text().splitlines() if line.startswith("btime ")))
    process_started_ms=int((boot + ticks / os.sysconf("SC_CLK_TCK")) * 1000)
    for entry in pathlib.Path(f"/proc/{exact[0]['pid']}/environ").read_bytes().split(b"\0"):
        if b"=" in entry:
            key, value = entry.split(b"=", 1)
            environment[key.decode(errors="replace")] = value.decode(errors="replace")
    job_dir = pathlib.Path.home() / ".claude" / "jobs" / f"native-{manifest['session_id']}"
    validate_running_empty_bootstrap(manifest, cwd, target, transcript, receipt_path, agent,
                                     native_agents, info, environment, job_dir, process_started_ms)


def persist_bootstrap_receipt(path, receipt):
    if path.is_symlink() or not path.parent.is_dir():
        raise RuntimeError("running bootstrap receipt parent is unavailable")
    with path.open("x") as handle:
        json.dump(receipt, handle, indent=2)
        handle.write("\n")
    path.chmod(0o600)


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
        effort = entry.get("effort") or entry.get("effortLevel")
        if effort:
            efforts.append(effort)
    return {"model": models[-1] if models else None, "effort": efforts[-1] if efforts else None}


def observed_model(entries):
    return observed_identity(entries)["model"]


def observed_title(entries, session_id):
    titles = [entry.get("customTitle") for entry in entries
              if entry.get("type") == "custom-title" and entry.get("sessionId") == session_id]
    return titles[-1] if titles else None


def wait_for_title(path, session_id, title, start_at, deadline):
    while time.monotonic() < deadline:
        if observed_title(transcript_entries(path)[start_at:], session_id) == title:
            return {"session_id": session_id, "value": title}
        time.sleep(0.5)
    raise RuntimeError("native Claude custom-title receipt missing")


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
        f"## Source: `{item['path']}`\n\n{item['body']}"
        for item in sources
    )
    return (
        f"# Native Claude main-flow refresh\n\n"
        f"You are {manifest['role']}. Preserve the witnessed native model `{manifest['model']}` "
        f"and effort `{manifest['effort']}`. "
        + (f"Your immediate predecessor is `{manifest['predecessor']}`; this does not retire, replace, or deregister it. "
           if manifest.get('predecessor') else "This is a fresh seat with no predecessor. ")
        + f"Do not claim a new Flow identity until the native Mainflow receipt "
        f"has been witnessed.\n\n"
        f"The applicable native skills were each invoked in separate user turns: "
        f"{', '.join(manifest['skills'])}. The following source bundle is provenance-bearing "
        f"handoff material, not a deployment or retirement instruction.\n\n{provenance}\n\n"
        "BOOTSTRAP ONLY: do not claim identity, invoke tools, delegate, edit, commit, register, "
        "or retire anything. Acknowledge this source bundle by replying only `BOOTSTRAP_READY`."
    )


def payload_hash(manifest, sources):
    payload = {"session_id": manifest["session_id"], "model": manifest["model"],
               "effort": manifest["effort"], "role": manifest["role"], "provisionalTitle": provisional_title(manifest),
               "skills": manifest["skills"],
               "sources": [{key: item[key] for key in ("path", "sha256")} for item in sources]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def plan(manifest, cwd):
    if canonical_role(manifest.get("role")) is None or "nativeTitle" in manifest or "testing-flow-titles" not in manifest["skills"]:
        raise ValueError("canonical role and testing-flow-titles required without arbitrary nativeTitle")
    aspect, power = canonical_role(manifest["role"])
    if manifest.get("titlePlan") != {"aspect": aspect, "power": power, "afterOwnVerifiedFlowId": True,
                                      "template": f"{aspect} {power} <FLOW_ID>"}:
        raise ValueError("canonical title plan required")
    skills = validate_skills(manifest, cwd)
    sources = validate_sources(manifest, cwd)
    return {"session_id": manifest["session_id"], "model": manifest["model"],
            "effort": manifest["effort"], "role": manifest["role"],
            "skills": skills, "sources": [{k: v for k, v in item.items() if k != "body"} for item in sources],
            "provisional_title": provisional_title(manifest),
            "ready_requires": "idle native session, observed model and skills, own Flow claim, and final native title readback"}


def refresh(manifest, cwd, timeout, sender=inject, herdr_target=None,
            bootstrap_running_empty=False, bootstrap_receipt=None, bootstrap_failed_state=None):
    receipt = plan(manifest, cwd)
    if herdr_target:
        agent = wait_for_herdr_idle(herdr_target, time.monotonic() + timeout)
        if pathlib.Path(agent.get("cwd", "")).resolve() != cwd:
            raise RuntimeError("Herdr Claude cwd differs from manifest cwd")
        sender = lambda _short, message: herdr_send(herdr_target, message)
    else:
        agent = wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
        if pathlib.Path(agent.get("cwd", "")).resolve() != cwd:
            raise RuntimeError("native Claude session cwd differs from manifest cwd")
    path = transcript_path(cwd, manifest["session_id"], required=False)
    entries = transcript_entries(path)
    require_transcript_uuid(entries, manifest["session_id"])
    if bootstrap_running_empty:
        if not herdr_target or entries:
            raise RuntimeError("running bootstrap requires empty native history and exact Herdr target")
        if bootstrap_failed_state is None:
            raise RuntimeError("running bootstrap requires exact failed-state corroboration")
        running_empty_bootstrap_preflight(manifest, cwd, herdr_target, path, bootstrap_receipt, agent,
                                          bootstrap_failed_state)
    elif not entries and not manifest.get("disposable"):
        raise RuntimeError(f"native Claude transcript unavailable: {path}")
    identity = observed_identity(entries)
    if identity["model"] and not model_matches(manifest["model"], identity["model"]):
        raise RuntimeError(f"native Claude model mismatch: expected {manifest['model']}, observed {identity['model']}")
    if identity["effort"] and identity["effort"] != manifest["effort"]:
        raise RuntimeError(f"native Claude effort mismatch: expected {manifest['effort']}, observed {identity['effort']}")
    short = None if herdr_target else resolve_native_id(manifest["session_id"])
    title_start = len(transcript_entries(path))
    sender(short, f"/rename {provisional_title(manifest)}")
    receipt["native_title"] = wait_for_title(path, manifest["session_id"], provisional_title(manifest), title_start, time.monotonic() + timeout)
    skill_receipts = []
    for skill in manifest["skills"]:
        if herdr_target:
            wait_for_herdr_idle(herdr_target, time.monotonic() + timeout)
        else:
            wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
        start_at = len(transcript_entries(path))
        sender(short, f"/{skill}")
        skill_receipts.append({"skill": skill, **wait_for_skill(path, skill, start_at, time.monotonic() + timeout)})
        current = transcript_entries(path)
        require_transcript_uuid(current, manifest["session_id"])
        identity = observed_identity(current)
        if not model_matches(manifest["model"], identity["model"]) or identity["effort"] != manifest["effort"]:
            raise RuntimeError(f"native identity mismatch: expected {manifest['model']}/{manifest['effort']}, observed {identity['model']}/{identity['effort']}")
    if herdr_target:
        wait_for_herdr_idle(herdr_target, time.monotonic() + timeout)
    else:
        wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
    sources = validate_sources(manifest, cwd)
    prompt = role_prompt(manifest, sources)
    prompt_start = len(transcript_entries(path))
    sender(short, prompt)
    deadline = time.monotonic() + timeout
    expected_ack = "BOOTSTRAP_READY"
    while time.monotonic() < deadline:
        current = transcript_entries(path)
        require_transcript_uuid(current, manifest["session_id"])
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
    receipt["readiness"] = "native-context-verified-title-pending"
    return receipt


def verify_claim_marker(cwd, flow_id, session_id):
    if not re.fullmatch(r"[0-9a-f]{6}", flow_id or ""):
        raise ValueError("title finalization requires own exact short Flow ID")
    marker = cwd / "flows" / f".{flow_id}.flow-id"
    if marker.is_symlink() or not marker.is_file():
        raise ValueError("title finalization requires a regular Flow claim marker")
    expected = ["version=1", "harness=claude", f"identity={session_id.replace('-', '')}", f"alias={flow_id}"]
    if marker.read_text().splitlines() != expected:
        raise ValueError("Flow claim marker differs from exact native session")
    return marker


def finalize_title(manifest, cwd, flow_id, receipt, timeout, sender=inject, herdr_target=None):
    if receipt.get("session_id") != manifest["session_id"] or receipt.get("role") != manifest["role"] or \
            receipt.get("readiness") != "native-context-verified-title-pending" or \
            receipt.get("native_title", {}).get("value") != provisional_title(manifest) or \
            not any(skill.get("skill") == "testing-flow-titles" for skill in receipt.get("generation", {}).get("skills", [])):
        raise ValueError("title finalization requires matching native bootstrap receipt and title skill")
    verify_claim_marker(cwd, flow_id, manifest["session_id"])
    if herdr_target:
        agent = wait_for_herdr_idle(herdr_target, time.monotonic() + timeout)
        if pathlib.Path(agent.get("cwd", "")).resolve() != cwd:
            raise RuntimeError("Herdr Claude cwd differs from manifest cwd")
        sender = lambda _short, message: herdr_send(herdr_target, message)
        short = None
    else:
        agent = wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
        if pathlib.Path(agent.get("cwd", "")).resolve() != cwd:
            raise RuntimeError("native Claude session cwd differs from manifest cwd")
        short = resolve_native_id(manifest["session_id"])
    path = transcript_path(cwd, manifest["session_id"])
    entries = transcript_entries(path)
    require_transcript_uuid(entries, manifest["session_id"])
    if observed_title(entries, manifest["session_id"]) != provisional_title(manifest):
        raise RuntimeError("native Claude before-title changed")
    aspect, power = canonical_role(manifest["role"])
    title = f"{aspect} {power} {flow_id}"
    start = len(entries)
    try:
        sender(short, f"/rename {title}")
        title_receipt = wait_for_title(path, manifest["session_id"], title, start, time.monotonic() + timeout)
    except Exception as error:
        try:
            rollback_start = len(transcript_entries(path))
            sender(short, f"/rename {provisional_title(manifest)}")
            wait_for_title(path, manifest["session_id"], provisional_title(manifest), rollback_start, time.monotonic() + timeout)
        except Exception as rollback_error:
            raise RuntimeError(f"canonical Claude title failed and rollback failed: {error}; {rollback_error}") from error
        raise RuntimeError(f"canonical Claude title failed; provisional title restored: {error}") from error
    return {**receipt, "canonical_flow_id": flow_id, "canonical_title": title_receipt,
            "readiness": "native-title-event-witnessed-ui-readback-pending"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--cwd", default=str(ROOT))
    parser.add_argument("--timeout", type=float, default=45)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--bootstrap-running-empty", action="store_true")
    parser.add_argument("--failed-state")
    parser.add_argument("--finalize-title", action="store_true")
    parser.add_argument("--flow-id")
    parser.add_argument("--receipt")
    parser.add_argument("--acknowledge-live-refresh", action="store_true")
    parser.add_argument("--herdr-session")
    parser.add_argument("--herdr-agent")
    parser.add_argument("--herdr-pane")
    parser.add_argument("--herdr-terminal")
    args = parser.parse_args()
    manifest = load_manifest(args.manifest)
    cwd = pathlib.Path(args.cwd).resolve()
    if args.refresh and not args.acknowledge_live_refresh:
        raise SystemExit("--refresh requires --acknowledge-live-refresh")
    if args.bootstrap_running_empty and (not args.refresh or not args.acknowledge_live_refresh or not args.receipt or not args.failed_state):
        raise SystemExit("--bootstrap-running-empty requires --refresh, --acknowledge-live-refresh, --receipt, and --failed-state")
    if args.finalize_title and (not args.acknowledge_live_refresh or not args.flow_id or not args.receipt):
        raise SystemExit("--finalize-title requires --acknowledge-live-refresh, --flow-id, and --receipt")
    target_fields = (args.herdr_session, args.herdr_agent, args.herdr_pane, args.herdr_terminal)
    if any(target_fields) and not all(target_fields):
        raise SystemExit("all Herdr target fields are required")
    target = dict(zip(("session", "agent", "pane", "terminal"), target_fields)) if all(target_fields) else None
    if args.finalize_title:
        receipt_path = pathlib.Path(args.receipt)
        receipt = json.loads(receipt_path.read_text())
        result = finalize_title(manifest, cwd, args.flow_id, receipt, args.timeout, herdr_target=target)
        receipt_path.write_text(json.dumps(result, indent=2) + "\n")
    else:
        result = refresh(manifest, cwd, args.timeout, herdr_target=target,
                         bootstrap_running_empty=args.bootstrap_running_empty,
                         bootstrap_receipt=pathlib.Path(args.receipt) if args.receipt else None,
                         bootstrap_failed_state=json.loads(pathlib.Path(args.failed_state).read_text()) if args.failed_state else None) if args.refresh else plan(manifest, cwd)
        if args.bootstrap_running_empty:
            persist_bootstrap_receipt(pathlib.Path(args.receipt), result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
