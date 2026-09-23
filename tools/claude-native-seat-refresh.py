#!/usr/bin/env python3
"""Refresh an idle native Claude seat through one slash-command turn per skill.

The manifest is the audited contract for one existing seat.  This helper never
chooses a model, effort, role, predecessor, or source set.  It checks those
facts before it types into the native Claude session, and records only an
observed native Skill invocation as a skill-expansion receipt.
"""

import argparse
import datetime
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


def validate_bootstrap_failed_state(state, manifest, cwd, target, transcript,
                                    failed_state_file=None, failed_state_sha256=None,
                                    allow_partial_identity_failure=False):
    """Corroborate the prior failure; live process checks remain authoritative."""
    seats = state.get("seats")
    if state.get("version") != 1 or not isinstance(seats, list) or len(seats) != 1:
        raise RuntimeError("running bootstrap requires one failed seat")
    seat = seats[0]
    expected = (target["pane"], target["terminal"], manifest["session_id"])
    if (seat.get("phase") != "failed" or
            (seat.get("paneId"), seat.get("terminalId"), seat.get("nativeThreadId")) != expected or
            seat.get("receipt") is None):
        raise RuntimeError("running bootstrap failed-state identity differs")
    retained = seat.get("retained")
    if retained:
        if (retained.get("paneId"), retained.get("terminalId"), retained.get("nativeThreadId")) != expected:
            raise RuntimeError("running bootstrap retained identity differs")
    else:
        # The first managed launch writes this manifest and records the planned
        # receipt before invoking the helper. The helper checks the transcript
        # before its first /rename or skill input.
        if failed_state_file is None or failed_state_sha256 is None:
            raise RuntimeError("VerifierUnavailable: initial managed-start state is not pinned")
        failed_state_file = pathlib.Path(failed_state_file)
        if (failed_state_file.is_symlink() or not failed_state_file.is_file() or
                sha256(failed_state_file) != failed_state_sha256 or
                json.loads(failed_state_file.read_text()) != state):
            raise RuntimeError("initial managed-start state changed")
        failed_state_file = failed_state_file.resolve()
        prior_receipt = pathlib.Path(seat["receipt"])
        expected_receipt = failed_state_file.parent / "receipts" / f"{target['agent']}.json"
        prior_manifest = prior_receipt.with_suffix(".manifest.json")
        failure = re.sub(r"\x1b\[[0-9;]*m", "", seat.get("error", ""))
        if (not prior_receipt.is_absolute() or prior_receipt != expected_receipt or
                prior_receipt.exists() or prior_receipt.is_symlink() or
                prior_manifest.is_symlink() or not prior_manifest.is_file() or
                json.loads(prior_manifest.read_text()) != manifest):
            raise RuntimeError("initial managed-start manifest or output differs")
        if ("tools/claude-native-seat-refresh.py" not in failure or
                "in refresh" not in failure or "RuntimeError" not in failure):
            raise RuntimeError("initial managed-start failure did not stop in bootstrap pre-input phase")
    missing_transcript = f"native Claude transcript unavailable: {transcript}"
    partial_identity = (f"native identity mismatch: expected {manifest['model']}/{manifest['effort']}, "
                        f"observed {manifest['model']}/None")
    failure = seat.get("error", "")
    if missing_transcript not in failure and not (allow_partial_identity_failure and partial_identity in failure):
        raise RuntimeError("running bootstrap failure phase differs")
    previous = state.get("manifest", {})
    declared = previous.get("seats", [])
    if (previous.get("cwd") != str(cwd) or previous.get("session") != target["session"] or
            len(declared) != 1 or declared[0].get("model") != manifest["model"] or
            declared[0].get("effort") != manifest["effort"] or
            declared[0].get("agent") != target["agent"]):
        raise RuntimeError("running bootstrap failed-state profile differs")
    if not retained and (declared[0].get("harness") != "claude" or
                         declared[0].get("claudeProfile", {}).get("skills") != manifest["skills"] or
                         declared[0].get("claudeProfile", {}).get("sources") != manifest["sources"] or
                         declared[0].get("claudeProfile", {}).get("sourceAudit") != manifest["sourceAudit"] or
                         declared[0].get("claudeProfile", {}).get("role") != manifest["role"] or
                         declared[0].get("claudeProfile", {}).get("titlePlan") != manifest["titlePlan"] or
                         declared[0].get("predecessor") != manifest["predecessor"]):
        raise RuntimeError("initial managed-start profile differs")


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
             ["claude", "--session-id", session_id, "--model", manifest["model"], "--effort", manifest["effort"], "--remote-control"]]
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


def validate_initial_controller_attestation(source, pinned_sha256, state_sha256, manifest, target, pid,
                                            process_started_ms):
    if source is None or pinned_sha256 is None:
        raise RuntimeError("VerifierUnavailable: initial managed-start exclusive-controller witness missing")
    source = pathlib.Path(source)
    if source.is_symlink() or not source.is_file() or sha256(source) != pinned_sha256:
        raise RuntimeError("initial managed-start controller witness changed")
    attestation = json.loads(source.read_text())
    expected = {
        "version": 1, "failedStateSha256": state_sha256,
        "sessionId": manifest["session_id"], "paneId": target["pane"],
        "terminalId": target["terminal"], "pid": pid,
        "processStartedMs": process_started_ms,
        "exclusiveControl": "same-process-no-restart-no-input-since-managed-start",
    }
    if attestation != expected:
        raise RuntimeError("initial managed-start exclusive-controller witness differs")


def running_empty_bootstrap_preflight(manifest, cwd, target, transcript, receipt_path, agent, failed_state,
                                      failed_state_file=None, failed_state_sha256=None,
                                      controller_attestation_file=None, controller_attestation_sha256=None):
    validate_bootstrap_failed_state(failed_state, manifest, cwd, target, transcript,
                                    failed_state_file, failed_state_sha256)
    if (failed_state_file is not None and not failed_state.get("seats", [{}])[0].get("retained") and
            receipt_path.parent == pathlib.Path(failed_state_file).parent / "receipts"):
        raise RuntimeError("initial managed-start requires a separate continuation receipt directory")
    native_agents = agents()
    response = json.loads(subprocess.check_output(
        ["herdr", "--session", target["session"], "pane", "process-info", "--pane", target["pane"]], text=True))
    info = response.get("result", response).get("process_info", {})
    exact = [item for item in info.get("foreground_processes", []) if item.get("argv") ==
             ["claude", "--session-id", manifest["session_id"], "--model", manifest["model"], "--effort", manifest["effort"], "--remote-control"]]
    if len(exact) != 1 or not isinstance(exact[0].get("pid"), int):
        raise RuntimeError("running bootstrap native process identity differs")
    environment = {}
    pid=exact[0]["pid"]
    stat=pathlib.Path(f"/proc/{pid}/stat").read_text()
    ticks=int(stat.rsplit(")", 1)[1].split()[19])
    boot=int(next(line.split()[1] for line in pathlib.Path("/proc/stat").read_text().splitlines() if line.startswith("btime ")))
    process_started_ms=int((boot + ticks / os.sysconf("SC_CLK_TCK")) * 1000)
    if not failed_state.get("seats", [{}])[0].get("retained"):
        try:
            opened = datetime.datetime.fromisoformat(failed_state["createdAt"].replace("Z", "+00:00"))
            failed = datetime.datetime.fromisoformat(failed_state["seats"][0]["updatedAt"].replace("Z", "+00:00"))
            opened_ms, failed_ms = int(opened.timestamp() * 1000), int(failed.timestamp() * 1000)
        except (KeyError, TypeError, ValueError) as error:
            raise RuntimeError("VerifierUnavailable: initial managed-start time window missing") from error
        if opened_ms > failed_ms or not opened_ms - 1000 <= process_started_ms <= failed_ms + 1000:
            raise RuntimeError("VerifierUnavailable: running process was not born in managed-start window")
        validate_initial_controller_attestation(controller_attestation_file,
                                                controller_attestation_sha256,
                                                failed_state_sha256, manifest, target, pid,
                                                process_started_ms)
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


def validate_partial_bootstrap(manifest, cwd, target, transcript, receipt_path, failed_state,
                               observation, entries, agent, native_agents, process_info,
                               environment, process_started_ms, job_dir,
                               failed_state_file=None, failed_state_sha256=None):
    """Accept only the exact title + first-skill cursor, never a completed turn."""
    validate_bootstrap_failed_state(failed_state, manifest, cwd, target, transcript,
                                    failed_state_file, failed_state_sha256,
                                    allow_partial_identity_failure=True)
    session_id = manifest["session_id"]
    if (not receipt_path or receipt_path.exists() or receipt_path.is_symlink() or
            not receipt_path.parent.is_dir() or transcript.is_symlink() or not transcript.is_file() or
            observation.get("nativeThreadId", session_id) != session_id or
            observation.get("transcriptPath") != str(transcript) or
            observation.get("transcriptSnapshotSha256") != sha256(transcript)):
        raise RuntimeError("partial bootstrap transcript or receipt differs from witnessed cursor")
    current_title = observed_title(entries, session_id)
    if current_title != provisional_title(manifest):
        flow_id = observation.get("canonicalFlowId")
        aspect, power = canonical_role(manifest["role"])
        expected_title = f"{aspect} {power} {flow_id}"
        try:
            verify_claim_marker(cwd, flow_id, session_id)
        except ValueError as error:
            raise RuntimeError("partial bootstrap canonical claim differs") from error
        if current_title != expected_title or agent.get("terminal_title_stripped") != expected_title:
            raise RuntimeError("partial bootstrap canonical title differs")
    commands = [entry.get("message", {}).get("content") for entry in entries
                if entry.get("type") == "user" and isinstance(entry.get("message", {}).get("content"), str)
                and "<command-name>" in entry["message"]["content"]]
    if "commands" in observation:
        expected = observation.get("witnessedSkills")
        if (not isinstance(expected, list) or not expected or len(expected) >= len(manifest["skills"]) or
                expected != manifest["skills"][:len(expected)] or
                observation["commands"] != [f"/{name}" for name in expected] or
                commands != [f"<command-message>{name}</command-message>\n<command-name>/{name}</command-name>" for name in expected]):
            raise RuntimeError("partial bootstrap skill cursor differs")
        command_indices = [i for i, entry in enumerate(entries) if entry.get("type") == "user" and
                           entry.get("message", {}).get("content") in commands]
        for index, name in enumerate(expected):
            turn = entries[command_indices[index]:(command_indices[index+1] if index+1 < len(expected) else len(entries))]
            assistants = [entry for entry in turn if entry.get("type") == "assistant"]
            if not skill_receipt(turn, name, cwd) or not assistants or any(
                    entry.get("sessionId") != session_id or entry.get("isSidechain") is True or
                    entry.get("attributionSkill") not in (None, name) for entry in assistants):
                raise RuntimeError("partial bootstrap native skill turn differs")
            if name == "visual-report-from-md":
                skill_source = cwd / ".claude/skills/visual-report-from-md/SKILL.md"
                if (not skill_source.is_file() or not skill_source.read_text().startswith("---\n") or
                        "model: sonnet\n" not in skill_source.read_text().split("---", 2)[1] or
                        "kind: subagent\n" not in skill_source.read_text().split("---", 2)[1] or
                        any(entry.get("message", {}).get("model") != "claude-sonnet-5" for entry in assistants)):
                    raise RuntimeError("partial bootstrap skill model override differs")
            elif any(not model_matches(manifest["model"], entry.get("message", {}).get("model")) for entry in assistants):
                raise RuntimeError("partial bootstrap base model differs")
        identity = scoped_assistant_identity(entries[command_indices[-1]:])
        if not model_matches(manifest["model"], identity["model"]):
            raise RuntimeError("partial bootstrap latest base model differs")
    else:
        # Spirit can invoke another skill internally.  The cursor is bound to
        # exact top-level command records; nested expansions are not evidence
        # that the corresponding top-level manifest command already ran.
        if (not manifest["skills"] or manifest["skills"][0] != "spirit" or
                observation.get("nativeSkillCommands") != ["<command-message>spirit</command-message>\n<command-name>/spirit</command-name>"] or
                not skill_receipt(entries, "spirit", cwd) or
                commands != observation["nativeSkillCommands"]):
            raise RuntimeError("partial bootstrap skill cursor differs")
        identity = observed_identity(entries)
        if identity["effort"] not in (None, manifest["effort"]) or observation.get("observedIdentity") != identity:
            raise RuntimeError("partial bootstrap native identity differs")
    if not model_matches(manifest["model"], identity["model"]):
        raise RuntimeError("partial bootstrap native identity differs")
    matches = [item for item in native_agents if item.get("sessionId") == session_id]
    processes = process_info.get("foreground_processes", [])
    exact = [item for item in processes if item.get("argv") ==
             ["claude", "--session-id", session_id, "--model", manifest["model"], "--effort", manifest["effort"], "--remote-control"]]
    if ((agent.get("agent_status") or agent.get("status")) not in ("idle", "done") or agent.get("interactive_ready") is not True or
            len(matches) != 1 or matches[0].get("cwd") != str(cwd) or matches[0].get("status") != "idle" or
            process_info.get("pane_id") != target["pane"] or len(exact) != 1 or
            exact[0].get("pid") != matches[0].get("pid") or
            not isinstance(process_started_ms, int) or not isinstance(matches[0].get("startedAt"), int) or
            abs(matches[0]["startedAt"] - process_started_ms) > 10_000):
        raise RuntimeError("VerifierUnavailable: partial bootstrap running process differs")
    if (environment.get("CLAUDE_JOB_DIR") != str(job_dir) or job_dir.is_symlink() or not job_dir.is_dir() or
            any(environment.get(key) for key in ("CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_KIND", "CLISESSIONID")) or
            environment.get("CLAUDE_CODE_SESSION_ID") not in (None, "", session_id)):
        raise RuntimeError("partial bootstrap native environment differs")


def partial_bootstrap_preflight(manifest, cwd, target, transcript, receipt_path, failed_state, observation, entries, agent,
                                failed_state_file=None, failed_state_sha256=None):
    native_agents = agents()
    response = json.loads(subprocess.check_output(
        ["herdr", "--session", target["session"], "pane", "process-info", "--pane", target["pane"]], text=True))
    info = response.get("result", response).get("process_info", {})
    exact = [item for item in info.get("foreground_processes", []) if item.get("argv") ==
             ["claude", "--session-id", manifest["session_id"], "--model", manifest["model"], "--effort", manifest["effort"], "--remote-control"]]
    if len(exact) != 1 or not isinstance(exact[0].get("pid"), int):
        raise RuntimeError("VerifierUnavailable: partial bootstrap native process identity differs")
    pid = exact[0]["pid"]
    stat = pathlib.Path(f"/proc/{pid}/stat").read_text()
    ticks = int(stat.rsplit(")", 1)[1].split()[19])
    boot = int(next(line.split()[1] for line in pathlib.Path("/proc/stat").read_text().splitlines() if line.startswith("btime ")))
    process_started_ms = int((boot + ticks / os.sysconf("SC_CLK_TCK")) * 1000)
    environment = {}
    for entry in pathlib.Path(f"/proc/{pid}/environ").read_bytes().split(b"\0"):
        if b"=" in entry:
            key, value = entry.split(b"=", 1)
            environment[key.decode(errors="replace")] = value.decode(errors="replace")
    validate_partial_bootstrap(manifest, cwd, target, transcript, receipt_path, failed_state,
                               observation, entries, agent, native_agents, info, environment, process_started_ms,
                               pathlib.Path.home() / ".claude" / "jobs" / f"native-{manifest['session_id']}",
                               failed_state_file, failed_state_sha256)


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


def scoped_assistant_identity(entries):
    """Read model and effort from one assistant record, never mix skill turns."""
    for entry in reversed(entries):
        if entry.get("type") == "assistant" and entry.get("message", {}).get("model"):
            message = entry["message"]
            return {"model": message["model"], "effort": message.get("effort") or message.get("effortLevel") or
                    entry.get("effort") or entry.get("effortLevel")}
    return {"model": None, "effort": None}


def wait_for_scoped_skill_identity(path, skill, session_id, start_at, deadline):
    while time.monotonic() < deadline:
        segment = transcript_entries(path)[start_at:]
        assistants = [entry for entry in segment if entry.get("type") == "assistant"]
        if assistants:
            if any(entry.get("sessionId") != session_id or entry.get("attributionSkill") != skill or
                   entry.get("isSidechain") is True for entry in assistants):
                raise RuntimeError("native skill response attribution differs")
            identity = scoped_assistant_identity(assistants)
            if identity["model"]:
                return identity
        time.sleep(0.5)
    raise RuntimeError(f"native model receipt missing for /{skill}")


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


def skill_receipt(entries, name, root=ROOT):
    for entry in entries:
        message = entry.get("message", {})
        companion = entry.get("isMeta") and entry.get("turnCompanion")
        companion_content = message.get("content", [])
        if companion and isinstance(companion_content, list):
            for block in companion_content:
                if isinstance(block, dict) and block.get("type") == "text":
                    marker = f"Base directory for this skill: {root}/.claude/skills/{name}"
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


def role_prompt(manifest, sources, effort_observed=True):
    provenance = "\n\n".join(
        f"## Source: `{item['path']}`\n\n{item['body']}"
        for item in sources
    )
    return (
        f"# Native Claude main-flow refresh\n\n"
        f"You are {manifest['role']}. Preserve the witnessed native model `{manifest['model']}`. "
        + (f"Preserve the witnessed effort `{manifest['effort']}`. " if effort_observed else
           f"The process requested effort `{manifest['effort']}`; native effort metadata is unavailable. ")
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
            bootstrap_running_empty=False, bootstrap_receipt=None, bootstrap_failed_state=None,
            continue_partial=False, partial_observation=None,
            bootstrap_failed_state_file=None, bootstrap_failed_state_sha256=None,
            controller_attestation_file=None, controller_attestation_sha256=None):
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
                                          bootstrap_failed_state, bootstrap_failed_state_file,
                                          bootstrap_failed_state_sha256, controller_attestation_file,
                                          controller_attestation_sha256)
    elif continue_partial:
        if not herdr_target or bootstrap_failed_state is None or partial_observation is None:
            raise RuntimeError("partial bootstrap requires exact Herdr target and prior evidence")
        partial_bootstrap_preflight(manifest, cwd, herdr_target, path, bootstrap_receipt,
                                    bootstrap_failed_state, partial_observation, entries, agent,
                                    bootstrap_failed_state_file, bootstrap_failed_state_sha256)
    elif not entries and not manifest.get("disposable"):
        raise RuntimeError(f"native Claude transcript unavailable: {path}")
    skill_cursor = continue_partial and "commands" in partial_observation
    identity = scoped_assistant_identity(entries) if skill_cursor else observed_identity(entries)
    if identity["model"] and not model_matches(manifest["model"], identity["model"]):
        raise RuntimeError(f"native Claude model mismatch: expected {manifest['model']}, observed {identity['model']}")
    if identity["effort"] and identity["effort"] != manifest["effort"]:
        raise RuntimeError(f"native Claude effort mismatch: expected {manifest['effort']}, observed {identity['effort']}")
    short = None if herdr_target else resolve_native_id(manifest["session_id"])
    if continue_partial:
        witnessed_skills = partial_observation["witnessedSkills"] if skill_cursor else manifest["skills"][:1]
        prior_title = observed_title(entries, manifest["session_id"])
        receipt["native_title"] = {"session_id": manifest["session_id"], "value": prior_title,
                                   "evidence": ("prior canonical transcript event plus live Herdr title readback"
                                                if partial_observation.get("canonicalFlowId") else
                                                "prior native transcript custom-title event")}
        skill_receipts = []
        for name in witnessed_skills:
            command = f"<command-message>{name}</command-message>\n<command-name>/{name}</command-name>"
            start = next(i for i, entry in enumerate(entries) if entry.get("type") == "user" and
                         entry.get("message", {}).get("content") == command)
            end = next(i + 1 for i in range(start, len(entries)) if skill_receipt([entries[i]], name, cwd))
            skill_receipts.append({"skill": name, "entry_start": start, "entry_end": end,
                                   "generation": transcript_digest(entries[:start]), "evidence": "prior native expansion"})
        remaining_skills = manifest["skills"][len(witnessed_skills):]
    else:
        title_start = len(transcript_entries(path))
        if bootstrap_running_empty:
            # Recheck the same incarnation and immutable input immediately
            # before the first native input, after all planning work.
            running_empty_bootstrap_preflight(manifest, cwd, herdr_target, path, bootstrap_receipt,
                                              wait_for_herdr_idle(herdr_target, time.monotonic() + timeout), bootstrap_failed_state,
                                              bootstrap_failed_state_file, bootstrap_failed_state_sha256,
                                              controller_attestation_file, controller_attestation_sha256)
        sender(short, f"/rename {provisional_title(manifest)}")
        receipt["native_title"] = wait_for_title(path, manifest["session_id"], provisional_title(manifest), title_start, time.monotonic() + timeout)
        skill_receipts = []
        remaining_skills = manifest["skills"]
    for skill in remaining_skills:
        if herdr_target:
            wait_for_herdr_idle(herdr_target, time.monotonic() + timeout)
        else:
            wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
        start_at = len(transcript_entries(path))
        sender(short, f"/{skill}")
        skill_receipts.append({"skill": skill, **wait_for_skill(path, skill, start_at, time.monotonic() + timeout)})
        current = transcript_entries(path)
        require_transcript_uuid(current, manifest["session_id"])
        identity = (wait_for_scoped_skill_identity(path, skill, manifest["session_id"], start_at, time.monotonic() + timeout)
                    if continue_partial else observed_identity(current))
        expected_model = "claude-sonnet-5" if skill == "visual-report-from-md" and continue_partial else manifest["model"]
        if (not model_matches(expected_model, identity["model"]) or
                (identity["effort"] not in (None, manifest["effort"]) if continue_partial else identity["effort"] != manifest["effort"])):
            raise RuntimeError(f"native identity mismatch: expected {manifest['model']}/{manifest['effort']}, observed {identity['model']}/{identity['effort']}")
    if herdr_target:
        wait_for_herdr_idle(herdr_target, time.monotonic() + timeout)
    else:
        wait_for_idle(manifest["session_id"], time.monotonic() + timeout)
    sources = validate_sources(manifest, cwd)
    before_prompt = transcript_entries(path)
    pre_prompt_identity = scoped_assistant_identity(before_prompt) if skill_cursor else observed_identity(before_prompt)
    prompt = role_prompt(manifest, sources, effort_observed=pre_prompt_identity["effort"] is not None)
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
    identity = scoped_assistant_identity(transcript_entries(path)[prompt_start:]) if skill_cursor else observed_identity(transcript_entries(path))
    if (not model_matches(manifest["model"], identity["model"]) or
            (identity["effort"] not in (None, manifest["effort"]) if continue_partial else identity["effort"] != manifest["effort"])):
        raise RuntimeError("native identity changed during bootstrap")
    receipt["native_main_flow"] = {"skill": "main-flow", "transcript": str(path), "observed": True}
    receipt["generation"] = {"session_id": manifest["session_id"], "skills": skill_receipts,
                             "source_payload_hash": payload_hash(manifest, sources), "acknowledged": expected_ack}
    receipt["observed_identity"] = identity
    receipt["requested_identity"] = {"model": manifest["model"], "effort": manifest["effort"]}
    receipt["effort_evidence"] = "native-transcript" if identity["effort"] is not None else "process-argv-requested-only"
    receipt["predecessor_retired"] = False
    receipt["registration_performed"] = False
    if continue_partial and partial_observation.get("canonicalFlowId"):
        receipt["canonical_flow_id"] = partial_observation["canonicalFlowId"]
        receipt["canonical_title"] = receipt["native_title"]
        receipt["readiness"] = "native-ready"
    else:
        receipt["readiness"] = ("native-context-verified-title-pending" if identity["effort"] is not None else
                                "native-context-model-verified-effort-unobserved-title-pending")
    return receipt


def verify_claim_marker(cwd, flow_id, session_id):
    if not re.fullmatch(r"[0-9a-f]{6}", flow_id or ""):
        raise ValueError("title finalization requires own exact short Flow ID")
    marker = cwd / "flows" / f".{flow_id}.flow-id"
    if marker.is_symlink() or not marker.is_file():
        raise ValueError("title finalization requires a regular Flow claim marker")
    expected = ["version=1", "harness=claude", f"identity={session_id.replace('-', '')}", f"alias={flow_id}"]
    lines = marker.read_text().splitlines()
    if lines not in (expected, [*expected, "uuid-version=uuid-v4"]):
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
    parser.add_argument("--continue-partial", action="store_true")
    parser.add_argument("--partial-observation")
    parser.add_argument("--failed-state")
    parser.add_argument("--controller-attestation")
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
    if args.continue_partial and (args.bootstrap_running_empty or not args.refresh or not args.acknowledge_live_refresh or
                                  not args.receipt or not args.failed_state or not args.partial_observation):
        raise SystemExit("--continue-partial requires --refresh, --acknowledge-live-refresh, --receipt, --failed-state, and --partial-observation")
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
        failed_state_bytes = pathlib.Path(args.failed_state).read_bytes() if args.failed_state else None
        attestation_bytes = pathlib.Path(args.controller_attestation).read_bytes() if args.controller_attestation else None
        result = refresh(manifest, cwd, args.timeout, herdr_target=target,
                         bootstrap_running_empty=args.bootstrap_running_empty,
                         bootstrap_receipt=pathlib.Path(args.receipt) if args.receipt else None,
                         bootstrap_failed_state=json.loads(failed_state_bytes) if failed_state_bytes else None,
                         bootstrap_failed_state_file=args.failed_state,
                         bootstrap_failed_state_sha256=hashlib.sha256(failed_state_bytes).hexdigest() if failed_state_bytes else None,
                         controller_attestation_file=args.controller_attestation,
                         controller_attestation_sha256=hashlib.sha256(attestation_bytes).hexdigest() if attestation_bytes else None,
                         continue_partial=args.continue_partial,
                         partial_observation=json.loads(pathlib.Path(args.partial_observation).read_text()) if args.partial_observation else None) if args.refresh else plan(manifest, cwd)
        if args.bootstrap_running_empty or args.continue_partial:
            persist_bootstrap_receipt(pathlib.Path(args.receipt), result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
