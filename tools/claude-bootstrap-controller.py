#!/usr/bin/env python3
"""Fail-closed controller for a restricted native Claude bootstrap generation."""
import hashlib, json, pathlib, subprocess, tempfile

EMPTY_MCP = '{"mcpServers": {}}\n'

def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def manifest(path):
    data = json.loads(pathlib.Path(path).read_text())
    for key in ("model", "effort", "role", "skills", "sources", "receipt_path"):
        if not data.get(key): raise ValueError("manifest missing: " + key)
    for source in data["sources"]:
        if not source.get("sha256"): raise ValueError("every source requires sha256")
    return data

def restricted_args(data, mcp_file):
    pathlib.Path(mcp_file).write_text(EMPTY_MCP)
    return ["--bg", "--model", data["model"], "--effort", data["effort"], "--tools", "", "--strict-mcp-config", "--mcp-config", str(mcp_file)]

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
    if receipt.get("session_id") != data.get("session_id"): raise RuntimeError("receipt UUID differs from manifest")
    if receipt.get("model") != data["model"] or receipt.get("effort") != data["effort"]: raise RuntimeError("receipt identity differs from manifest")
    return ["--bg", "--resume", receipt["session_id"], "--model", data["model"], "--effort", data["effort"]]

def main():
    import argparse
    parser = argparse.ArgumentParser(); parser.add_argument("--manifest", required=True); parser.add_argument("--print-bootstrap", action="store_true"); parser.add_argument("--print-activation", action="store_true")
    args = parser.parse_args(); data = manifest(args.manifest)
    if args.print_bootstrap:
        with tempfile.NamedTemporaryFile(prefix="claude-empty-mcp-", suffix=".json", delete=False) as f: print(json.dumps(restricted_args(data, f.name)))
    if args.print_activation: print(json.dumps(activation_args(data, json.loads(pathlib.Path(data["receipt_path"]).read_text()))))
if __name__ == "__main__": main()
