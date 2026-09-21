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
        (directory / "SKILL.md").write_text(skill)
    (root / "Vision").mkdir()
    source = root / "Vision/source.md"
    source.write_text("witnessed source")
    manifest = {"session_id": "01234567-0000-4000-8000-000000000000", "model": "claude-haiku-4-5-20251001", "effort": "low", "role": "Psyche Low", "titlePlan": {"aspect":"Psyche","power":"Low","afterOwnVerifiedFlowId":True,"template":"Psyche Low <FLOW_ID>"}, "skills": ["spirit", "main-flow", "testing-flow-titles"], "sources": [{"path": "Vision/source.md", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}], "sourceAudit": {"reviewedAt": "2026-09-21T00:00:00Z", "newestApplicableVision": ["Vision/source.md"]}}
    prompt = MODULE.role_prompt(manifest, MODULE.validate_sources(manifest, root))
    assert "witnessed source" in prompt and "BOOTSTRAP_READY" in prompt
    assert manifest["sources"][0]["sha256"] not in prompt and "SHA-256:" not in prompt
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
    fixture_agents = MODULE.agents
    def sender(short, text):
        rows = [identity()]
        if text.startswith("/rename "):
            rows.append({"type": "custom-title", "customTitle": text.removeprefix("/rename "), "sessionId": manifest["session_id"]})
        elif text.startswith("/"):
            name = text[1:]
            rows.append({"isMeta": True, "turnCompanion": True, "message": {"content": [{"type": "text", "text": f"Base directory for this skill: {MODULE.ROOT}/.claude/skills/{name}"}]}})
        else:
            ack = "BOOTSTRAP_READY"
            rows.append({"type": "assistant", "message": {"content": [{"type": "text", "text": ack}]}})
        with transcript.open("a") as handle:
            for row in rows: handle.write(json.dumps(row) + "\n")
    receipt = MODULE.refresh(manifest, root, 1, sender)
    assert len(receipt["generation"]["skills"]) == 3
    assert receipt["generation"]["source_payload_hash"] == MODULE.payload_hash(manifest, MODULE.validate_sources(manifest, root))
    transcript.write_text(json.dumps(identity()) + "\n")
    herdr_idle, herdr_send = MODULE.wait_for_herdr_idle, MODULE.herdr_send
    MODULE.wait_for_herdr_idle = lambda target, deadline: {"cwd": str(root)}
    MODULE.herdr_send = lambda target, text: sender(None, text)
    MODULE.agents = lambda: (_ for _ in ()).throw(AssertionError("claude agents must not supply Herdr occupancy"))
    target = {"session": "fixture", "agent": "claude", "pane": "p1", "terminal": "t1"}
    herdr_receipt = MODULE.refresh(manifest, root, 1, herdr_target=target)
    assert len(herdr_receipt["generation"]["skills"]) == 3
    # A genuinely new running session may have no JSONL until its first input.
    # The explicit bootstrap path must check the process before that input.
    job_dir = root / ".claude/jobs" / f"native-{manifest['session_id']}"
    job_dir.mkdir(parents=True)
    absent = root / "absent.jsonl"
    receipt_file = root / "new-receipt.json"
    native = [{"sessionId": manifest["session_id"], "cwd": str(root), "status": "idle", "pid": 7, "startedAt": 1000962}]
    process = {"pane_id": "p1", "foreground_processes": [{"pid": 7, "argv": ["claude", "--session-id", manifest["session_id"],
              "--model", manifest["model"], "--effort", manifest["effort"]]}]}
    environment = {"CLAUDE_JOB_DIR": str(job_dir)}
    failed_state = {"version": 1, "manifest": {"cwd": str(root), "session": "fixture", "seats": [
        {"model": manifest["model"], "effort": manifest["effort"], "agent": "claude"}]}, "seats": [{
        "phase": "failed", "paneId": "p1", "terminalId": "t1", "nativeThreadId": manifest["session_id"],
        "retained": {"paneId": "p1", "terminalId": "t1", "nativeThreadId": manifest["session_id"]},
        "receipt": str(root / "prior.json"), "error": f"native Claude transcript unavailable: {absent}"}]}
    MODULE.validate_bootstrap_failed_state(failed_state, manifest, root, target, absent)
    bad_state=json.loads(json.dumps(failed_state))
    bad_state["seats"][0]["phase"]="prompt-started"
    try: MODULE.validate_bootstrap_failed_state(bad_state, manifest, root, target, absent)
    except RuntimeError: pass
    else: raise AssertionError("later failure phase accepted")
    MODULE.validate_running_empty_bootstrap(manifest, root, target, absent, receipt_file,
                                            {"agent_status":"idle", "interactive_ready":True}, native, process, environment, job_dir, 1000000)
    def rejected(**changes):
        values={"manifest":manifest,"cwd":root,"target":target,"transcript":absent,"receipt_path":receipt_file,
                "agent":{"agent_status":"idle","interactive_ready":True},"native_agents":native,
                "process_info":process,"environment":environment,"job_dir":job_dir,"process_started_ms":1000000}
        values.update(changes)
        try: MODULE.validate_running_empty_bootstrap(**values)
        except RuntimeError: return
        raise AssertionError("unsafe running bootstrap accepted")
    absent.write_text(json.dumps(identity()) + "\n")
    rejected()
    absent.unlink()
    receipt_file.write_text("already recorded")
    rejected()
    receipt_file.unlink()
    receipt_file.symlink_to(root / "missing")
    rejected()
    receipt_file.unlink()
    rejected(process_info={"pane_id":"p1","foreground_processes":[{"pid":7,"argv":["claude","--session-id",manifest["session_id"],"--model","other","--effort",manifest["effort"]]}]})
    rejected(environment={"CLAUDE_JOB_DIR":str(job_dir),"CLAUDE_CODE_SESSION_ID":"foreign"})
    rejected(process_started_ms=900000)
    transcript.unlink()
    original_preflight=MODULE.running_empty_bootstrap_preflight
    witnessed=[]
    MODULE.running_empty_bootstrap_preflight=lambda *args: witnessed.append(args)
    empty_receipt=MODULE.refresh(manifest, root, 1, herdr_target=target,
                                 bootstrap_running_empty=True, bootstrap_receipt=receipt_file,
                                 bootstrap_failed_state=failed_state)
    assert witnessed and len(empty_receipt["generation"]["skills"]) == 3
    try: MODULE.refresh(manifest, root, 1, herdr_target=target,
                        bootstrap_running_empty=True, bootstrap_receipt=receipt_file,
                        bootstrap_failed_state=failed_state)
    except RuntimeError as error: assert "empty native history" in str(error)
    else: raise AssertionError("already bootstrapped session accepted")
    MODULE.running_empty_bootstrap_preflight=original_preflight
    MODULE.persist_bootstrap_receipt(receipt_file, empty_receipt)
    assert json.loads(receipt_file.read_text()) == empty_receipt
    assert receipt_file.stat().st_mode & 0o777 == 0o600
    try: MODULE.persist_bootstrap_receipt(receipt_file, empty_receipt)
    except FileExistsError: pass
    else: raise AssertionError("existing receipt overwritten")
    MODULE.wait_for_herdr_idle, MODULE.herdr_send, MODULE.agents = herdr_idle, herdr_send, fixture_agents

    # An interrupted first turn must resume after the witnessed /spirit expansion.
    partial = root / "partial.jsonl"
    command = "<command-message>spirit</command-message>\n<command-name>/spirit</command-name>"
    initial = [
        {"type":"custom-title", "customTitle":MODULE.provisional_title(manifest), "sessionId":manifest["session_id"]},
        {"type":"user", "message":{"content":command}, "sessionId":manifest["session_id"]},
        {"type":"user", "isMeta":True, "turnCompanion":True,
         "message":{"content":[{"type":"text", "text":f"Base directory for this skill: {root}/.claude/skills/spirit\nbody"}]},
         "sessionId":manifest["session_id"]},
        {"type":"attachment", "attachment":{"identity":{"modelId":manifest["model"]}}, "sessionId":manifest["session_id"]}]
    partial.write_text("".join(json.dumps(row)+"\n" for row in initial))
    partial_observation = {"nativeThreadId":manifest["session_id"], "transcriptPath":str(partial),
        "transcriptSnapshotSha256":MODULE.sha256(partial), "nativeSkillCommands":[command],
        "observedIdentity":{"model":manifest["model"],"effort":None}}
    partial_failed=json.loads(json.dumps(failed_state))
    partial_failed["seats"][0]["error"]=f"native Claude transcript unavailable: {partial}"
    MODULE.validate_partial_bootstrap(manifest, root, target, partial, root / "partial-receipt.json",
        partial_failed, partial_observation, initial, {"agent_status":"done","interactive_ready":True}, native,
        process, environment, 1000000, job_dir)
    partial.write_text(partial.read_text()+json.dumps({"type":"user","message":{"content":"extra"}})+"\n")
    try: MODULE.validate_partial_bootstrap(manifest, root, target, partial, root / "partial-receipt.json",
        partial_failed, partial_observation, MODULE.transcript_entries(partial),
        {"agent_status":"done","interactive_ready":True}, native, process, environment, 1000000, job_dir)
    except RuntimeError: pass
    else: raise AssertionError("stale partial cursor accepted")
    partial.write_text("".join(json.dumps(row)+"\n" for row in initial))
    calls=[]
    MODULE.transcript_path=lambda cwd, session, required=False: partial
    MODULE.wait_for_herdr_idle=lambda target, deadline: {"cwd":str(root),"agent_status":"done","interactive_ready":True}
    MODULE.partial_bootstrap_preflight=lambda *args: calls.append("checked")
    def partial_sender(target, message):
        calls.append(message)
        if message.startswith("/"):
            row={"type":"user","isMeta":True,"turnCompanion":True,
                "message":{"content":[{"type":"text", "text":f"Base directory for this skill: {MODULE.ROOT}/.claude/skills/{message[1:]}"}]},
                "sessionId":manifest["session_id"]}
            response={"type":"assistant","message":{"model":manifest["model"],"content":[{"type":"text","text":"skill loaded"}]},
                      "attributionSkill":message[1:],"sessionId":manifest["session_id"]}
        else:
            row={"type":"assistant","message":{"model":manifest["model"],"content":[{"type":"text","text":"BOOTSTRAP_READY"}]},
                 "sessionId":manifest["session_id"]}
            response=None
        with partial.open("a") as handle:
            handle.write(json.dumps(row)+"\n")
            if response: handle.write(json.dumps(response)+"\n")
    MODULE.herdr_send=partial_sender
    continued=MODULE.refresh(manifest,root,1,herdr_target=target,continue_partial=True,
        bootstrap_receipt=root / "partial-receipt.json",bootstrap_failed_state=partial_failed,
        partial_observation=partial_observation)
    assert calls[0]=="checked" and "/spirit" not in calls and not any(x.startswith("/rename") for x in calls)
    assert continued["generation"]["skills"][0]["skill"]=="spirit"
    assert continued["observed_identity"]=={"model":manifest["model"],"effort":None}
    assert continued["requested_identity"]["effort"]==manifest["effort"]
    assert continued["readiness"]=="native-context-model-verified-effort-unobserved-title-pending"
    assert "native effort metadata is unavailable" in calls[-1]
    MODULE.transcript_path= lambda cwd, session, required=False: transcript
    MODULE.herdr_send=herdr_send
    MODULE.wait_for_herdr_idle=herdr_idle

    # A subagent-kind skill may use Sonnet for its own turn inside the same
    # session; that effort must not be mixed with the later Haiku base turn.
    cursor_manifest={**manifest,"skills":["spirit","testing-flow-titles","visual-report-from-md","main-flow","refresh"]}
    for name in ("visual-report-from-md","refresh"):
        folder=root/".claude/skills"/name;folder.mkdir(parents=True)
        (folder/"SKILL.md").write_text("---\nmodel: sonnet\nkind: subagent\n---\n" if name=="visual-report-from-md" else name)
    cursor_path=root/"cursor.jsonl";cursor_rows=[initial[0]]
    for name in cursor_manifest["skills"][:-1]:
        cursor_rows.extend([
          {"type":"user","message":{"content":f"<command-message>{name}</command-message>\n<command-name>/{name}</command-name>"},"sessionId":manifest["session_id"]},
          {"type":"user","isMeta":True,"turnCompanion":True,"message":{"content":[{"type":"text","text":f"Base directory for this skill: {root}/.claude/skills/{name}"}]},"sessionId":manifest["session_id"]},
          {"type":"assistant","attributionSkill":name,"sessionId":manifest["session_id"],"message":{"model":"claude-sonnet-5" if name=="visual-report-from-md" else manifest["model"],"content":[{"type":"text","text":"loaded"}]},**({"effort":"low"} if name=="visual-report-from-md" else {})}])
    cursor_path.write_text("".join(json.dumps(row)+"\n" for row in cursor_rows))
    cursor_obs={"transcriptPath":str(cursor_path),"transcriptSnapshotSha256":MODULE.sha256(cursor_path),
                "commands":["/"+x for x in cursor_manifest["skills"][:-1]]}
    cursor_failed=json.loads(json.dumps(failed_state))
    cursor_failed["seats"][0]["error"]=f"native Claude transcript unavailable: {cursor_path}"
    MODULE.validate_partial_bootstrap(cursor_manifest,root,target,cursor_path,root/"cursor-receipt.json",cursor_failed,
        cursor_obs,cursor_rows,{"agent_status":"done","interactive_ready":True},native,process,environment,1000000,job_dir)
    wrong_turn=json.loads(json.dumps(cursor_rows))
    next(row for row in wrong_turn if row.get("attributionSkill")=="visual-report-from-md")["message"]["model"]=manifest["model"]
    try: MODULE.validate_partial_bootstrap(cursor_manifest,root,target,cursor_path,root/"cursor-receipt.json",cursor_failed,
        cursor_obs,wrong_turn,{"agent_status":"done","interactive_ready":True},native,process,environment,1000000,job_dir)
    except RuntimeError: pass
    else: raise AssertionError("incorrect skill model override accepted")
    assert MODULE.scoped_assistant_identity(cursor_rows)=={"model":manifest["model"],"effort":None}
    cursor_calls=[]
    MODULE.transcript_path=lambda cwd,session,required=False: cursor_path
    MODULE.wait_for_herdr_idle=lambda target,deadline: {"cwd":str(root),"agent_status":"done","interactive_ready":True}
    MODULE.partial_bootstrap_preflight=lambda *args: cursor_calls.append("checked")
    def cursor_sender(target,message):
        cursor_calls.append(message)
        if message.startswith("/"):
            rows=[{"type":"user","isMeta":True,"turnCompanion":True,"message":{"content":[{"type":"text","text":f"Base directory for this skill: {MODULE.ROOT}/.claude/skills/{message[1:]}"}]},"sessionId":manifest["session_id"]},
                  {"type":"assistant","attributionSkill":message[1:],"sessionId":manifest["session_id"],"message":{"model":manifest["model"],"content":[{"type":"text","text":"loaded"}]}}]
        else:rows=[{"type":"assistant","sessionId":manifest["session_id"],"message":{"model":manifest["model"],"content":[{"type":"text","text":"BOOTSTRAP_READY"}]}}]
        with cursor_path.open("a") as handle:
            for row in rows:handle.write(json.dumps(row)+"\n")
    MODULE.herdr_send=cursor_sender
    cursor_result=MODULE.refresh(cursor_manifest,root,1,herdr_target=target,continue_partial=True,
        bootstrap_receipt=root/"cursor-receipt.json",bootstrap_failed_state=cursor_failed,partial_observation=cursor_obs)
    assert cursor_calls[0]=="checked" and [x for x in cursor_calls if x.startswith("/")]==["/refresh"]
    assert cursor_result["observed_identity"]=={"model":manifest["model"],"effort":None}
    assert cursor_result["readiness"]=="native-context-model-verified-effort-unobserved-title-pending"
    MODULE.transcript_path=lambda cwd,session,required=False: transcript
    MODULE.herdr_send=herdr_send
    MODULE.wait_for_herdr_idle=herdr_idle

    assert receipt["native_title"]["value"] == "Psyche Low (claim pending)"
    assert receipt["readiness"] == "native-context-verified-title-pending"
    transcript.write_text(json.dumps(identity()) + "\n" + json.dumps({"type":"custom-title","customTitle":"Psyche Low (claim pending)","sessionId":manifest["session_id"]}) + "\n")
    marker = root / "flows" / ".000000.flow-id"
    marker.parent.mkdir()
    try: MODULE.finalize_title(manifest, root, "000000", receipt, 1, sender)
    except ValueError as error: assert "claim marker" in str(error)
    else: raise AssertionError("missing claim marker accepted")
    marker.write_text("version=1\nharness=claude\nidentity=wrong\nalias=000000\n")
    try: MODULE.finalize_title(manifest, root, "000000", receipt, 1, sender)
    except ValueError as error: assert "differs" in str(error)
    else: raise AssertionError("wrong native session claim accepted")
    marker.write_text(f"version=1\nharness=claude\nidentity={manifest['session_id'].replace('-', '')}\nalias=000000\n")
    final = MODULE.finalize_title(manifest, root, "000000", receipt, 1, sender)
    assert final["canonical_title"]["value"] == "Psyche Low 000000"
    assert final["readiness"] == "native-title-event-witnessed-ui-readback-pending"
    transcript.write_text(json.dumps(identity()) + "\n" + json.dumps({"type":"custom-title","customTitle":"Psyche Low (claim pending)","sessionId":manifest["session_id"]}) + "\n")
    def failed_title_sender(short, text):
        if text == "/rename Psyche Low 000000":
            return
        sender(short, text)
    try: MODULE.finalize_title(manifest, root, "000000", receipt, .01, failed_title_sender)
    except RuntimeError as error: assert "provisional title restored" in str(error)
    else: raise AssertionError("missing native title event accepted")
    assert MODULE.observed_title(MODULE.transcript_entries(transcript), manifest["session_id"]) == "Psyche Low (claim pending)"
    bad = dict(manifest); bad["titlePlan"] = {**manifest["titlePlan"], "power": "Sol"}
    try: MODULE.plan(bad, root)
    except ValueError as error: assert "canonical title plan" in str(error)
    else: raise AssertionError("role-contradicting title plan accepted")
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
