#!/usr/bin/env python3
"""Fail-closed controller for a restricted native Claude bootstrap generation."""
import ctypes, hashlib, json, os, pathlib, select, subprocess, time, tempfile, uuid

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

def native_transcript_path(cwd, session_id):
    encoded = "-" + str(pathlib.Path(cwd).resolve()).strip("/").replace("/", "-")
    return pathlib.Path.home() / ".claude" / "projects" / encoded / f"{session_id}.jsonl"

def guard_acknowledged(path):
    if not path.is_file():
        return False
    for line in path.read_text().splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") != "assistant":
            continue
        for block in entry.get("message", {}).get("content", []):
            if isinstance(block, dict) and block.get("type") == "text" and "BOOTSTRAP_GUARD_ACK" in block.get("text", ""):
                return True
    return False

def wait_for_guard_ack(cwd, session_id, timeout):
    """Wait for a fresh native transcript event; never poll the agents registry."""
    path = native_transcript_path(cwd, session_id)
    if guard_acknowledged(path):
        return path
    deadline = time.monotonic() + timeout
    directory = path.parent
    directory.mkdir(parents=True, exist_ok=True)
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    fd = libc.inotify_init1(0)
    if fd < 0:
        raise RuntimeError("cannot open an inotify completion watcher")
    try:
        mask = 0x00000008 | 0x00000080 | 0x00000100  # close-write, moved-to, create
        if libc.inotify_add_watch(fd, os.fsencode(directory), mask) < 0:
            raise RuntimeError("cannot watch native Claude transcript directory")
        if guard_acknowledged(path):
            return path
        while time.monotonic() < deadline:
            ready, _, _ = select.select([fd], [], [], deadline - time.monotonic())
            if not ready:
                break
            os.read(fd, 4096)
            if guard_acknowledged(path):
                return path
    finally:
        os.close(fd)
    raise RuntimeError("native Claude bootstrap guard acknowledgement was not observed")

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

def restricted_args(data, mcp_file, session_id=None):
    pathlib.Path(mcp_file).write_text(EMPTY_MCP)
    args = ["--bg", "--session-id", session_id or data.get("session_id", str(uuid.uuid4())), "--model", data["model"], "--effort", data["effort"], "--tools", "", "--strict-mcp-config", "--mcp-config", str(mcp_file)]
    system = custom_system_prompt(data)
    if system:
        args.extend(["--append-system-prompt", system])
    return [*args, "--append-system-prompt", BOOTSTRAP_GUARD, "--name", data["name"], INITIAL_GUARD_PROMPT]

def bootstrap_plan(data, mcp_file, session_id=None):
    """Executable creation contract; caller must run it from the target project cwd."""
    return {"cwd": data.get("cwd", "/home/li/primary"), "env": launch_environment(), "argv": ["claude", *restricted_args(data, mcp_file, session_id)], "requires_initial_ack": "BOOTSTRAP_GUARD_ACK"}

def run_bootstrap(data, mcp_file):
    """Start one guarded native session and persist only its UUID handoff.

    The source payload remains frozen in the manifest for
    claude-native-seat-refresh.py; this function never activates the seat.
    """
    session_id = str(uuid.uuid4())
    plan = bootstrap_plan(data, mcp_file, session_id)
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
    return record_bootstrap(data, session_id)

def record_bootstrap(data, session_id):
    """Persist one already-created UUID only after its native bootstrap proof."""
    transcript = wait_for_guard_ack(data.get("cwd", "/home/li/primary"), session_id, data.get("launch_timeout_seconds", 45))
    env = os.environ.copy()
    for key, value in launch_environment().items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = value
    listed = json.loads(subprocess.check_output(["claude", "agents", "--json"], cwd=data.get("cwd", "/home/li/primary"), env=env, text=True, timeout=15))
    agent = next((item for item in listed if item.get("sessionId") == session_id), None)
    if not agent or agent.get("name") != data["name"] or agent.get("status") != "idle":
        raise RuntimeError("Claude bootstrap UUID/exact name/idle state is absent from native agents registry")
    receipt = {"status": "bootstrap-created", "session_id": session_id,
               "model": data["model"], "effort": data["effort"],
               "name": data["name"], "requires_initial_ack": "BOOTSTRAP_GUARD_ACK",
               "guard_acknowledged": True, "transcript": str(transcript),
               "native_registry": {"id": agent.get("id"), "name": agent["name"], "status": agent["status"]},
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
    # The guarded bootstrap deliberately had no tools.  Activation is a new
    # ordinary continuation, so make the restored built-in tool policy
    # explicit rather than inheriting the bootstrap invocation.
    return ["--resume", receipt["session_id"], "--model", data["model"], "--effort", data["effort"], "--tools", "default"]

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

def continuation_args(data, session_id):
    """Same-UUID foreground continuation with the ordinary built-in tool set."""
    return ["--resume", session_id, "--model", data["model"], "--effort", data["effort"], "--tools", "default"]

def main():
    import argparse
    parser = argparse.ArgumentParser(); parser.add_argument("--manifest", required=True); parser.add_argument("--print-bootstrap", action="store_true"); parser.add_argument("--print-activation", action="store_true"); parser.add_argument("--launch-bootstrap", action="store_true"); parser.add_argument("--recover-bootstrap", metavar="UUID"); parser.add_argument("--acknowledge-live-launch", action="store_true"); parser.add_argument("--record-native-refresh", metavar="RECEIPT")
    args = parser.parse_args(); data = manifest(args.manifest)
    if args.print_bootstrap:
        with tempfile.NamedTemporaryFile(prefix="claude-empty-mcp-", suffix=".json", delete=False) as f: print(json.dumps(bootstrap_plan(data, f.name)))
    if args.launch_bootstrap:
        if not args.acknowledge_live_launch:
            raise SystemExit("--launch-bootstrap requires --acknowledge-live-launch")
        with tempfile.NamedTemporaryFile(prefix="claude-empty-mcp-", suffix=".json", delete=False) as f:
            print(json.dumps(run_bootstrap(data, f.name)))
    if args.recover_bootstrap:
        if not args.acknowledge_live_launch:
            raise SystemExit("--recover-bootstrap requires --acknowledge-live-launch")
        print(json.dumps(record_bootstrap(data, args.recover_bootstrap)))
    if args.record_native_refresh:
        print(json.dumps(record_native_refresh(data, args.record_native_refresh)))
    if args.print_activation: print(json.dumps(activation_args(data, json.loads(pathlib.Path(data["receipt_path"]).read_text()))))
if __name__ == "__main__": main()
