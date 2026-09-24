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
    for skill in ("main-flow", "spirit", "testing-flow-titles"):
        directory = root / ".claude/skills" / skill
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(f"{skill} exact body\n")
    (root / ".claude/skills/testing-flow-titles/SKILL.md").write_text(
        "---\ndisable-model-invocation: true\n---\ntesting-flow-titles exact body\n")
    (root / "Vision").mkdir()
    source = root / "Vision/source.md"
    source.write_text("witnessed source")
    session = "01234567-0000-4000-8000-000000000000"
    manifest = {
        "session_id": session, "model": "claude-haiku-4-5-20251001", "effort": "low",
        "role": "Psyche Low",
        "titlePlan": {"aspect": "Psyche", "power": "Low", "model": "Haiku 4.5",
                      "afterOwnVerifiedFlowId": True, "template": "Psyche Haiku 4.5 <FLOW_ID>"},
        "skills": ["spirit", "main-flow", "testing-flow-titles"],
        "sources": [{"path": "Vision/source.md", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}],
        "sourceAudit": {"reviewedAt": "2026-09-21T00:00:00Z", "newestApplicableVision": ["Vision/source.md"]},
    }
    sources = MODULE.validate_sources(manifest, root)
    prompt = MODULE.first_prompt(manifest, root, sources)
    main_flow = MODULE.expanded_skill("main-flow", root)
    assert prompt.startswith(main_flow + "\n\n")
    assert MODULE.expanded_skill("testing-flow-titles", root) in prompt
    assert "witnessed source" in prompt and "BOOTSTRAP_READY" in prompt
    assert len(prompt.encode()) < 20 * 1024
    assert manifest["sources"][0]["sha256"] not in prompt and "SHA-256:" not in prompt

    plain = {"type": "user", "message": {"content": prompt}}
    pasted = {"type": "user", "message": {"content": f'\n<pasted_content id="p1">\n{prompt}\n</pasted_content id="p1">\n'}}
    assert MODULE.first_prompt_receipt([plain], prompt, main_flow, 0)["accepted_user_prompts"] == 1
    assert MODULE.first_prompt_receipt([pasted], prompt, main_flow, 0)["leading_skill"] == "main-flow"
    try:
        MODULE.first_prompt_receipt([plain, plain], prompt, main_flow, 0)
    except RuntimeError as error:
        assert "exactly one" in str(error)
    else:
        raise AssertionError("two accepted first prompts were accepted")
    try:
        MODULE.first_prompt_receipt([{"type": "user", "message": {"content": "wrong"}}], prompt, main_flow, 0)
    except RuntimeError as error:
        assert "differs" in str(error)
    else:
        raise AssertionError("a changed first prompt was accepted")

    transcript = root / "fixture.jsonl"
    initial = [identity(), {"type": "custom-title", "customTitle": MODULE.provisional_title(manifest), "sessionId": session}]
    transcript.write_text("".join(json.dumps(row) + "\n" for row in initial))
    old_path, old_idle, old_agents = MODULE.transcript_path, MODULE.wait_for_idle, MODULE.agents
    MODULE.transcript_path = lambda cwd, native, required=False: transcript
    MODULE.wait_for_idle = lambda native, deadline: {"cwd": str(root), "pid": 7}
    MODULE.agents = lambda: [{"id": "01234567", "sessionId": session, "status": "idle", "cwd": str(root)}]
    calls = []

    def sender(short, text):
        calls.append(text)
        rows = [
            {"type": "user", "sessionId": session, "message": {"content": text}},
            {"type": "assistant", "sessionId": session,
             "message": {"model": manifest["model"], "effort": manifest["effort"],
                         "content": [{"type": "text", "text": "BOOTSTRAP_READY"}]}}
        ]
        with transcript.open("a") as handle:
            for row in rows:
                handle.write(json.dumps(row) + "\n")

    receipt = MODULE.refresh(manifest, root, 1, sender)
    assert calls == [prompt]
    assert receipt["generation"]["first_user_prompt"]["accepted_user_prompts"] == 1
    assert receipt["generation"]["first_user_prompt"]["leading_skill"] == "main-flow"
    assert receipt["native_main_flow"]["observed"] is True
    assert receipt["readiness"] == "native-context-verified-title-pending"
    assert [item["skill"] for item in receipt["generation"]["skills"]] == manifest["skills"]

    transcript.write_text("".join(json.dumps(row) + "\n" for row in initial))
    refused_calls = []
    def refused(_short, text):
        refused_calls.append(text)
        raise RuntimeError("classifier refused prompt injection")
    try:
        MODULE.refresh(manifest, root, .01, refused)
    except RuntimeError as error:
        assert "classifier refused" in str(error)
    else:
        raise AssertionError("refused launcher injection reached readiness")
    assert refused_calls == [prompt]

    transcript.write_text("".join(json.dumps(row) + "\n" for row in initial))
    dropped_calls = []
    try:
        MODULE.refresh(manifest, root, .01, lambda _short, text: dropped_calls.append(text))
    except RuntimeError as error:
        assert "acknowledgement missing" in str(error)
    else:
        raise AssertionError("unwitnessed launcher injection reached readiness")
    assert dropped_calls == [prompt]

    omitted_prompt = main_flow + "\n\n" + MODULE.role_brief(manifest, sources)
    transcript.write_text("".join(json.dumps(row) + "\n" for row in [
        *initial,
        {"type": "user", "sessionId": session, "message": {"content": omitted_prompt}},
        {"type": "assistant", "sessionId": session,
         "message": {"model": manifest["model"], "effort": manifest["effort"],
                     "content": [{"type": "text", "text": "BOOTSTRAP_READY"}]}}
    ]))
    repair_calls = []
    def repair_sender(_short, text):
        repair_calls.append(text)
        name = text.removeprefix("/")
        with transcript.open("a") as handle:
            handle.write(json.dumps({"type": "user", "isMeta": True, "turnCompanion": True,
                "sessionId": session, "message": {"content": [{"type": "text", "text":
                f"Base directory for this skill: {root}/.claude/skills/{name}"}]}}) + "\n")
    repaired = MODULE.repair_startup_skill(manifest, root, "testing-flow-titles", 1, repair_sender)
    assert repair_calls == ["/testing-flow-titles"]
    assert repaired["evidence"] == "verified native omission repair"

    transcript.write_text("".join(json.dumps(row) + "\n" for row in [*initial, {"type": "user", "message": {"content": "prior"}}]))
    no_send = []
    try:
        MODULE.refresh(manifest, root, .01, lambda _short, text: no_send.append(text))
    except RuntimeError as error:
        assert "no accepted user prompt" in str(error)
    else:
        raise AssertionError("nonfresh native session accepted as a launcher")
    assert no_send == []

    try:
        MODULE.refresh(manifest, root, .01, sender, continue_partial=True)
    except RuntimeError as error:
        assert "cannot resume or resend" in str(error)
    else:
        raise AssertionError("ambiguous partial first prompt was resumed")

    transcript.write_text("".join(json.dumps(row) + "\n" for row in initial))
    marker = root / "flows/.000000.flow-id"
    marker.parent.mkdir()
    marker.write_text(f"version=1\nharness=claude\nidentity={session.replace('-', '')}\nalias=000000\n")
    def title_sender(_short, text):
        assert text == "/rename Psyche Haiku 4.5 000000"
        with transcript.open("a") as handle:
            handle.write(json.dumps({"type": "custom-title", "customTitle": "Psyche Haiku 4.5 000000", "sessionId": session}) + "\n")
    final = MODULE.finalize_title(manifest, root, "000000", receipt, 1, title_sender)
    assert final["readiness"] == "native-title-event-witnessed-ui-readback-pending"

    MODULE.transcript_path, MODULE.wait_for_idle, MODULE.agents = old_path, old_idle, old_agents

print("claude-native-seat-refresh fixtures passed")
