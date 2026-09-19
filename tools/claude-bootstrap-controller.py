#!/usr/bin/env python3
"""Fail-closed controller for a restricted native Claude bootstrap generation."""
import hashlib, json, os, pathlib, re, subprocess, tempfile

EMPTY_MCP = '{"mcpServers": {}}\n'
BOOTSTRAP_GUARD = "BOOTSTRAP ONLY. Do not claim identity, invoke tools, run commands, delegate, edit, commit, register, or retire. Acknowledge only."
INITIAL_GUARD_PROMPT = "BOOTSTRAP_GUARD_ACK only. Do no operational work."

def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def manifest(path):
    data = json.loads(pathlib.Path(path).read_text())
    for key in ("model", "effort", "role", "name", "skills", "sources", "receipt_path", "refresh_manifest_path"):
        if not data.get(key): raise ValueError("manifest missing: " + key)
    for source in data["sources"]:
        if not source.get("sha256"): raise ValueError("every source requires sha256")
    return data

def launch_environment():
    """Environment contract for every Claude process created by this controller."""
    return {"CLAUDE_CODE_FORCE_SESSION_PERSISTENCE": "1",
            "CLAUDE_CODE_CHILD_SESSION": None}

def custom_system_prompt(data):
    """Build appended system material only from hash-verified authored files."""
    cwd = pathlib.Path(data.get("cwd", "/home/li/primary")).resolve()
    parts = []
    for source in data.get("system_sources", data["sources"]):
        relative = pathlib.PurePath(source.get("path", ""))
        if not relative.parts or relative.is_absolute() or ".." in relative.parts:
            raise ValueError("system source path must be workspace-relative")
        file = cwd / relative
        if not file.is_file():
            raise ValueError("system source missing: " + relative.as_posix())
        if sha256(file) != source.get("sha256"):
            raise ValueError("system source changed: " + relative.as_posix())
        parts.append(f"SOURCE {relative.as_posix()}\n\n{file.read_text().rstrip()}")
    return "\n\n".join(parts)

def restricted_args(data, mcp_file):
    pathlib.Path(mcp_file).write_text(EMPTY_MCP)
    args = ["--bg", "--model", data["model"], "--effort", data["effort"], "--tools", "", "--strict-mcp-config", "--mcp-config", str(mcp_file)]
    system = custom_system_prompt(data)
    if system:
        args.extend(["--append-system-prompt", system])
    return [*args, "--append-system-prompt", BOOTSTRAP_GUARD, "--name", data["name"], INITIAL_GUARD_PROMPT]

def bootstrap_plan(data, mcp_file):
    """Executable creation contract; caller must run it from the target project cwd."""
    return {"cwd": data.get("cwd", "/home/li/primary"), "env": launch_environment(), "argv": ["claude", *restricted_args(data, mcp_file)], "requires_initial_ack": "BOOTSTRAP_GUARD_ACK"}

def run_bootstrap(data, mcp_file):
    """Start one guarded native session and persist only its UUID handoff.

    The source payload remains frozen in the manifest for
    claude-native-seat-refresh.py; this function never activates the seat.
    """
    plan = bootstrap_plan(data, mcp_file)
    env = os.environ.copy()
    env.update({key: value for key, value in plan["env"].items() if value is not None})
    for key, value in plan["env"].items():
        if value is None:
            env.pop(key, None)
    started = subprocess.run(plan["argv"], cwd=plan["cwd"], env=env,
                             capture_output=True, text=True,
                             timeout=data.get("launch_timeout_seconds", 45))
    if started.returncode:
        raise RuntimeError("Claude bootstrap failed: " + started.stderr.strip())
    ids = re.findall(r"[0-9a-f]{8}-[0-9a-f-]{27,}", started.stdout + started.stderr, re.I)
    if len(set(ids)) != 1:
        raise RuntimeError("Claude bootstrap did not return one native UUID")
    session_id = ids[0]
    receipt = {"status": "bootstrap-created", "session_id": session_id,
               "model": data["model"], "effort": data["effort"],
               "name": data["name"], "requires_initial_ack": plan["requires_initial_ack"],
               "activation_performed": False}
    refresh_manifest = {key: data[key] for key in ("model", "effort", "role", "skills", "sources")}
    refresh_manifest["session_id"] = session_id
    refresh_manifest["predecessor"] = data.get("predecessor", "not supplied")
    refresh_path = pathlib.Path(data["refresh_manifest_path"])
    refresh_path.parent.mkdir(parents=True, exist_ok=True)
    refresh_path.write_text(json.dumps(refresh_manifest, indent=2) + "\n")
    receipt["refresh_manifest_path"] = str(refresh_path)
    persist(data, receipt)
    return receipt

def resolve(items, short):
    matches = [item for item in items if item.get("id") == short or item.get("sessionId", "").startswith(short)]
    if len(matches) != 1 or not matches[0].get("sessionId"): raise RuntimeError("native UUID resolution is not unique")
    return matches[0]

def persist(data, receipt):
    target = pathlib.Path(data["receipt_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2) + "\n")

def activation_args(data, receipt):
    if receipt.get("status") != "bootstrap-ready": raise RuntimeError("bootstrap receipt is not ready")
    expected_session = data.get("session_id", receipt.get("session_id"))
    if receipt.get("session_id") != expected_session: raise RuntimeError("receipt UUID differs from manifest")
    if receipt.get("model") != data["model"] or receipt.get("effort") != data["effort"]: raise RuntimeError("receipt identity differs from manifest")
    return ["--resume", receipt["session_id"], "--model", data["model"], "--effort", data["effort"]]

def record_native_refresh(data, path):
    """Promote only the exact UUID after native skills and frozen payload ack."""
    bootstrap = json.loads(pathlib.Path(data["receipt_path"]).read_text())
    native = json.loads(pathlib.Path(path).read_text())
    if bootstrap.get("status") != "bootstrap-created":
        raise RuntimeError("bootstrap receipt is not awaiting native refresh")
    if any(native.get(key) != bootstrap.get(key) for key in ("session_id", "model", "effort")):
        raise RuntimeError("native refresh identity differs from bootstrap")
    sources = [{key: source[key] for key in ("path", "sha256")} for source in data["sources"]]
    payload = {"session_id": bootstrap["session_id"], "model": data["model"],
               "effort": data["effort"], "role": data["role"],
               "skills": data["skills"], "sources": sources}
    expected = "BOOTSTRAP_READY " + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if native.get("generation", {}).get("acknowledged") != expected:
        raise RuntimeError("native refresh lacks frozen-payload acknowledgement")
    if native.get("native_main_flow", {}).get("observed") is not True:
        raise RuntimeError("native refresh lacks native main-flow receipt")
    observed = [item.get("skill") for item in native.get("generation", {}).get("skills", [])]
    if observed != data["skills"]:
        raise RuntimeError("native refresh skill receipts differ from manifest")
    ready = {**bootstrap, "status": "bootstrap-ready", "native_refresh_receipt": str(path)}
    persist(data, ready)
    return ready

def continuation_args(data, session_id, mcp_file):
    """Same-UUID foreground continuation; never use --bg (which can fork a copy)."""
    return ["--resume", session_id, "--model", data["model"], "--effort", data["effort"], "--tools", "", "--strict-mcp-config", "--mcp-config", str(mcp_file), "--append-system-prompt", BOOTSTRAP_GUARD]

def main():
    import argparse
    parser = argparse.ArgumentParser(); parser.add_argument("--manifest", required=True); parser.add_argument("--print-bootstrap", action="store_true"); parser.add_argument("--print-activation", action="store_true"); parser.add_argument("--launch-bootstrap", action="store_true"); parser.add_argument("--acknowledge-live-launch", action="store_true"); parser.add_argument("--record-native-refresh", metavar="RECEIPT")
    args = parser.parse_args(); data = manifest(args.manifest)
    if args.print_bootstrap:
        with tempfile.NamedTemporaryFile(prefix="claude-empty-mcp-", suffix=".json", delete=False) as f: print(json.dumps(bootstrap_plan(data, f.name)))
    if args.launch_bootstrap:
        if not args.acknowledge_live_launch:
            raise SystemExit("--launch-bootstrap requires --acknowledge-live-launch")
        with tempfile.NamedTemporaryFile(prefix="claude-empty-mcp-", suffix=".json", delete=False) as f:
            print(json.dumps(run_bootstrap(data, f.name)))
    if args.record_native_refresh:
        print(json.dumps(record_native_refresh(data, args.record_native_refresh)))
    if args.print_activation: print(json.dumps(activation_args(data, json.loads(pathlib.Path(data["receipt_path"]).read_text()))))
if __name__ == "__main__": main()
