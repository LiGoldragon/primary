#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import pathlib
import tempfile

TOOL = pathlib.Path(__file__).with_name("claude-native-seat-refresh.py")
SPEC = importlib.util.spec_from_file_location("claude_native", TOOL)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

with tempfile.TemporaryDirectory() as temp:
    root = pathlib.Path(temp)
    (root / ".claude/skills/main-flow").mkdir(parents=True)
    (root / ".claude/skills/spirit").mkdir(parents=True)
    (root / ".claude/skills/main-flow/SKILL.md").write_text("main")
    (root / ".claude/skills/spirit/SKILL.md").write_text("spirit")
    (root / "Vision").mkdir()
    source = root / "Vision/source.md"
    source.write_text("witnessed source")
    manifest = {
        "session_id": "01234567-0000-4000-8000-000000000000",
        "model": "claude-haiku-4-5-20251001", "effort": "low", "role": "disposable probe",
        "skills": ["spirit", "main-flow"],
        "sources": [{"path": "Vision/source.md", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}],
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    plan = MODULE.plan(MODULE.load_manifest(manifest_path), root)
    assert plan["skills"][1]["name"] == "main-flow"
    assert plan["sources"][0]["sha256"] == manifest["sources"][0]["sha256"]
    assert MODULE.has_skill([{"message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "main-flow"}}]}}], "main-flow")
    assert not MODULE.has_skill([{"message": {"content": [{"type": "text", "text": "/main-flow"}]}}], "main-flow")
    source.write_text("changed")
    try:
        MODULE.plan(MODULE.load_manifest(manifest_path), root)
    except ValueError as error:
        assert "source changed" in str(error)
    else:
        raise AssertionError("changed source must refuse refresh")

print("claude-native-seat-refresh fixtures passed")
