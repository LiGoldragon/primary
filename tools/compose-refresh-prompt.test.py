#!/usr/bin/env python3
import importlib.machinery
import importlib.util
import pathlib
import tempfile

tool = pathlib.Path(__file__).with_name("compose-refresh-prompt")
loader = importlib.machinery.SourceFileLoader("composer", str(tool))
spec = importlib.util.spec_from_loader("composer", loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)

with tempfile.TemporaryDirectory() as temp:
    root = pathlib.Path(temp)
    (root / ".claude/skills/main-flow").mkdir(parents=True)
    main_flow = root / ".claude/skills/main-flow/SKILL.md"
    main_flow.write_text("main-flow exact body\n")
    (root / ".claude/skills/refresh").mkdir(parents=True)
    refresh = root / ".claude/skills/refresh/SKILL.md"
    refresh.write_text("refresh exact body\n")
    variables = root / "SKILL_VARIABLES.md"
    variables.write_text("")
    module.ROOT, module.MAIN_FLOW, module.VARIABLES = root, main_flow, variables
    module.SEATS = {"fixture": {"role": "fixture", "vision_topics": ()}}
    prompt = module.compose("fixture", None)
    expected = f"Base directory for this skill: {main_flow.parent}\n\nmain-flow exact body\n\n"
    assert prompt.startswith(expected)
    assert "Load these through the Skill tool" in prompt

    main_flow.write_text("x" * (20 * 1024))
    try:
        module.compose("fixture", None)
    except SystemExit as error:
        assert "smaller than 20 KiB" in str(error)
    else:
        raise AssertionError("oversize first prompt was accepted")

print("compose-refresh-prompt fixtures passed")
