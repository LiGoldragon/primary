#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import pathlib
import tempfile

path = pathlib.Path(__file__).with_name("claude-bootstrap-controller.py")
spec = importlib.util.spec_from_file_location("controller", path)
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)

with tempfile.TemporaryDirectory() as temp:
    root = pathlib.Path(temp)
    source = root / "source"
    source.write_text("exact source")
    data = {
        "model": "claude-fable-5-1", "effort": "medium", "role": "Psyche High",
        "name": "Psyche Fable 5.1 (claim pending)", "skills": ["main-flow"],
        "sources": [{"path": "source", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}],
        "receipt_path": str(root / "receipt.json"), "refresh_manifest_path": str(root / "refresh.json"),
        "cwd": str(root),
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(data))
    assert controller.manifest(manifest_path)["name"] == data["name"]
    assert controller.custom_system_prompt(data) == "SOURCE source\n\nexact source"
    environment = controller.launch_environment("01234567-0000-4000-8000-000000000000")
    assert environment["CLAUDE_CODE_CHILD_SESSION"] is None
    assert environment["CLAUDE_JOB_DIR"] is None
    assert controller.resolve([{"id": "abc", "sessionId": "uuid"}], "abc")["sessionId"] == "uuid"

    calls = [
        lambda: controller.restricted_args(data, root / "mcp"),
        lambda: controller.bootstrap_plan(data, root / "mcp"),
        lambda: controller.run_bootstrap(data, root / "mcp"),
        lambda: controller.record_bootstrap(data, "01234567-0000-4000-8000-000000000000"),
        lambda: controller.record_native_refresh(data, root / "native.json"),
        lambda: controller.activation_args(data, {}),
        lambda: controller.continuation_args(data, "uuid"),
    ]
    for call in calls:
        try:
            call()
        except RuntimeError as error:
            assert "single first prompt contract" in str(error)
        else:
            raise AssertionError("obsolete multi-prompt controller entry point remained enabled")
    assert not (root / "receipt.json").exists()
    assert not (root / "refresh.json").exists()

print("claude-bootstrap-controller fixtures passed")
