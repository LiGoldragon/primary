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


def identity(model="claude-haiku-4-5-20251001", effort="low"):
    return {"attachment": {"identity": {"modelId": model, "effort": effort}}}


with tempfile.TemporaryDirectory() as temp:
    root = pathlib.Path(temp)
    for skill in ("main-flow", "spirit"):
        directory = root / ".claude/skills" / skill
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(skill)
    (root / "Vision").mkdir()
    source = root / "Vision/source.md"
    source.write_text("witnessed source")
    manifest = {"session_id": "01234567-0000-4000-8000-000000000000", "model": "claude-haiku-4-5-20251001", "effort": "low", "role": "fixture", "skills": ["spirit", "main-flow"], "sources": [{"path": "Vision/source.md", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}]}
    good = {"isMeta": True, "turnCompanion": True, "message": {"content": [{"type": "text", "text": f"Base directory for this skill: {MODULE.ROOT}/.claude/skills/main-flow"}]}}
    assert MODULE.has_skill([good], "main-flow")
    assert not MODULE.has_skill([{**good, "turnCompanion": False}], "main-flow")
    assert not MODULE.has_skill([{"message": {"content": [{"type": "tool_use", "name": "Skill"}]}}], "main-flow")

    transcript = root / "fixture.jsonl"
    transcript.write_text(json.dumps(identity()) + "\n")
    path, idle, listed = MODULE.transcript_path, MODULE.wait_for_idle, MODULE.agents
    MODULE.transcript_path = lambda cwd, session, required=False: transcript
    MODULE.wait_for_idle = lambda session, deadline: {"cwd": str(root), "pid": 7}
    MODULE.agents = lambda: [{"id": "01234567", "sessionId": manifest["session_id"], "status": "idle", "cwd": str(root)}]
    def sender(short, text):
        rows = [identity()]
        if text.startswith("/"):
            name = text[1:]
            rows.append({"isMeta": True, "turnCompanion": True, "message": {"content": [{"type": "text", "text": f"Base directory for this skill: {MODULE.ROOT}/.claude/skills/{name}"}]}})
        else:
            ack = "BOOTSTRAP_READY " + MODULE.payload_hash(manifest, MODULE.validate_sources(manifest, root))
            rows.append({"type": "assistant", "message": {"content": [{"type": "text", "text": ack}]}})
        with transcript.open("a") as handle:
            for row in rows: handle.write(json.dumps(row) + "\n")
    receipt = MODULE.refresh(manifest, root, 1, sender)
    assert len(receipt["generation"]["skills"]) == 2

    transcript.write_text(json.dumps(identity()) + "\n" + json.dumps(good) + "\n")
    try: MODULE.refresh(manifest, root, .01, lambda short, text: None)
    except RuntimeError as error: assert "receipt missing" in str(error)
    else: raise AssertionError("stale receipt accepted")
    for key, value, word in (("model", "wrong-model", "model mismatch"), ("effort", "medium", "effort mismatch")):
        bad = dict(manifest); bad[key] = value
        try: MODULE.refresh(bad, root, .01, sender)
        except RuntimeError as error: assert word in str(error)
        else: raise AssertionError("wrong identity accepted")
    source.write_text("changed")
    try: MODULE.plan(manifest, root)
    except ValueError as error: assert "source changed" in str(error)
    else: raise AssertionError("changed fat source accepted")
    MODULE.transcript_path, MODULE.wait_for_idle, MODULE.agents = path, idle, listed

print("claude-native-seat-refresh fixtures passed")
