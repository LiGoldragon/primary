# Anatomy audit: concepts held in the wrong component

Audit for 33752b, 2026-10-12; read at the cited lines unless marked "lead".
`CH` is /git/github.com/LiGoldragon/CriomOS-home (HEAD 8fa8630c), `MC` is
/git/github.com/LiGoldragon/messenger-clj (85e71b1), `PR` is /home/li/primary,
`VF` is /git/github.com/LiGoldragon/psyche-skills/skills/vision-flow.md
(psyche-skills 5a18f9c).

Judged against: VF line 20 (flow id, "No flow declares its id: every call to
Flow is identified by the calling process"), line 22 ("Message asks Flow to
send ... Flow owns the lock and the delivery"), lines 26-30 ("A Nexus component
decides the system prompt and everything about a launch"; "the layer decides
the model, declared once in Flow as configuration"), lines 39-40 (skills live
outside the runtime repository "so that a change to a skill causes no Nix
rebuild"), lines 50-58 (reaping belongs to the refresh event; "Every harness
event reaches Flow through the harness's hooks calling the Flow CLI"); and
vision-nexus.md lines 141-144 ("Polling is forbidden") and its Signal /
Operation / Memory section; walk/run/turn/stop: PR/flows/33752b/log.md 38.

## Kind (a): welds into components that are not ours

### A1. Agent-executable selection welded into Herdr (witnessed)
- Concept: which harness binary a flow is launched with (a Flow launch fact).
- Held in: a 540-line source patch to Herdr. Should be: Flow, choosing the
  executable it launches and passing it through Herdr's public interface.
- Evidence: CH/packages/herdr/default.nix 3-7
  `inputs.herdr...herdr.overrideAttrs (previous: {`
  `  ../../patches/herdr/codex-executable-selection.patch`
  CH/patches/herdr/codex-executable-selection.patch 7-10 (new `executable`
  field on Herdr's agent-start API), 131-155 (`resolve_agent_executable`, an
  allowlist check for Codex only). The allowlist is Flow vocabulary written
  into Herdr config: CH/modules/home/profiles/min/herdr.nix 75-80
  `codex_executables = [ "${stableCodexClientPackage}/bin/codex-stable-flow-client",`
  Consumer: PR/tools/primary-committer/restart.mjs 177
  `'agent', 'start', c.name, '--kind', 'codex', ... '--executable', c.resumeExecutable`
  (that file is untracked in Primary).
- Breaks: turn. Each Herdr upgrade must rebase a patch on Herdr's API and
  wire schema; the patched API exists on no upstream Herdr, so a launch that
  depends on it cannot run on a stock Herdr.

### A2. Role and skill-loading policy written into Pi's built-in prompt (witnessed)
- Concept: a role's action space (an orchestrator dispatches rather than
  inspects) and the rule for already-pasted skill blocks.
- Held in: source patches to Pi's system-prompt and skills code, built by Nix.
  Should be: our skills (role text), which VF 39-40 keeps outside any
  Nix-built repository.
- Evidence: CH/packages/pi/default.nix 8-12 (three patches);
  CH/packages/pi/patches/preserve-active-action-space-for-pi-docs.patch 16
  `+- If an active role or skill restricts this session to an action space such as orchestration ... must dispatch a worker/subagent`
  CH/packages/pi/patches/complete-pasted-skill-blocks-are-loaded.patch 9
  `A complete pasted <skill ...> block with the full body is already loaded`
  The same rule also exists as role text in
  /git/github.com/LiGoldragon/Curriculum/roles.datom line 2 (`codex-skill-loading`).
- Breaks: turn. Changing a role rule needs a Nix rebuild of Pi, and the rule
  is held twice.

### A3. Quiet hours and sound mode welded into Herdr; the "9eb" lead resolved (witnessed)
- Lead resolution: `9eb521456ac0` is upstream Herdr's own v0.8.2 commit, not
  ours. `git ls-remote https://github.com/herdrdev/herdr` returned
  `9eb521456ac0d19d3ab3d9d7cea3cca10baa8a4c refs/tags/v0.8.2^{}`; CH/flake.lock
  1435 and /git/github.com/LiGoldragon/CriomOS/flake.lock 1927 lock that rev.
  The quiet-hours changes are a local patch applied on top of it.
- Concept: when the machine may make sound (a quiet-hours schedule plus a
  persisted on/off/auto override).
- Held in: an 817-line patch to Herdr (CH/patches/herdr/quiet-hours.patch)
  that adds two crates (`iana-time-zone`, `jiff`, lines 1-13), a state file
  `state_dir().join("sound-mode")` (lines ~385-411), a `herdr sound
  [auto|on|off]` subcommand (lines 717-786) and a gate in `src/sound.rs`
  (`sound_playback_allowed`). It also replaces Herdr's Cargo.lock
  (CH/packages/herdr/default.nix 8-10). Should be: a notification policy of
  ours, using Herdr's public `[ui.sound] enabled` setting.
- Observation: the managed Herdr config no longer sets quiet hours. They
  appear only in `legacyHerdrConfig` (CH/modules/home/profiles/min/herdr.nix
  35-37: `[ui.sound.quiet_hours] start = "21:00" end = "06:00"`), which is
  used only in activation backup comparisons (lines 296, 343). The current
  `herdrConfig` (lines 75-91) has no `quiet_hours`. A search of CH/modules
  and PR/tools found no caller of `herdr sound`.
- Breaks: turn. The patch is still applied and rebased on every Herdr bump,
  and its feature appears to be unconfigured.

### A4. Claude Desktop's binary resolution rewritten (witnessed)
- Concept: which Claude Code binary the desktop app runs; held in a
  build-time rewrite of the vendor's app.asar.
- Evidence: CH/owned-agents/claude-desktop/default.nix 199
  `node ${./patch-runtime.mjs} "$extracted_app" ${claudeCodePackage}/bin/claude`;
  patch-runtime.mjs 167 `replaceOne(source, "async initLocalBinary(e){", ...)`,
  177 injects a refusal into `prepareForVM`.
- Should be: a vendor setting, if one exists (unknown). Breaks: turn. It is
  keyed to minified method names, but the patch checks itself at build time
  (lines 71-72), so drift fails the build and not the running app.

### A5. Small vendor byte-edits (witnessed, low)
CH/owned-agents/chatgpt/patch-process-report.py 12-13 (`isLinux() &&
process.report` becomes `false`); CH/packages/traycer/default.nix 42-48
(`autoHideMenuBar: true`). Packaging and cosmetics; no flow concept.

### Checked and found not to be welds
Codex (CH/owned-agents/codex/default.nix 39-45, release binaries unmodified);
yt-dlp overlay (source bump); CriomOS `mkForce`/systemd settings (ordinary
NixOS configuration; headscale ExecStartPre only adds a check); the Claude Code
wrapper (public flags; see B9).

## Kind (b): concepts misplaced among our own components

### B1. Flow launch is held in Primary launcher scripts (witnessed; most serious)
- Concept: launching a flow, meaning its system prompt, skill selection,
  session id, flow id claim, continuation record, title, pane, and
  registration.
- Held in: PR/tools/claude-main-flow-launch.mjs, plus parallel copies in
  codex-, opencode- and native-worker-launch.mjs. Should be: the Flow Nexus
  (VF 26-30).
- Evidence: claude-main-flow-launch.mjs 269
  `skillNames = orderSkillsForPrompt(resolveSkillDependencies(BIRTH_SKILLS).filter(... !(name === 'vision-design' && (o.aspect === 'Psyche' || o.layer === 'Primary')) ...`
  277-280 `const sessionId = crypto.randomUUID(); const flowId = claimFlow(...); writeContinuationRecord(...); canonicalTitleFor(...)`
  297 builds the `claude --session-id ... --model ... --system-prompt-file ...`
  command; 365 `execFileSync('hm-register', [flowId, ...])`. Skill policy per
  aspect is hard-coded again in codex-main-flow-launch.mjs 30
  (`ASPECT_SKILLS`).
- Breaks: walk and turn. Launch logic exists four times in a repository that
  is not a Nexus. A change to launch policy means editing several scripts,
  and nothing records or locks the metaflow.

### B2. Layer to model is declared in three places, none of them Flow (witnessed)
- Concept: which model and effort a layer runs. VF 30 says this is "declared
  once in Flow as configuration and changed only over its meta socket".
- Held in:
  - PR/tools/native-voice-profiles.mjs 8:
    `'Psyche.Secondary': {... model: 'claude-opus-5-5', effort: 'medium', source: 'living ruling 2026-10-10'}`
  - /git/github.com/LiGoldragon/Curriculum/roles.datom line 2: depth to model
    for subflows (`{ demanding { opus Some.Medium } { gpt-5.6-sol Some.Medium } }`)
  - PR/SKILL_VARIABLES.md: `Psyche medium Claude model: claude-opus-4-6[1m]`
- The three values differ for the Psyche medium seat (opus-5-5 compared with
  opus-4-6). Breaks: turn. A model change must be made in three
  repositories, and the copies can disagree.

### B3. Flow lifecycle and delivery are held in the messenger (witnessed)
- Concept: the flow route registry, retirement or reaping, rebinding and
  moving a flow, and the delivery lock. VF 22 gives the lock and delivery to
  Flow; VF 50-58 makes reaping part of the refresh event.
- Held in: MC/src/messenger_clj/core.clj, at
  512 `(defn register! [flow name session native-thread]`,
  678 `(defn retire!`, with a retirement marker and an evidence file at 711-726
  (`"Retired " flow ": delivery is blocked before Herdr routing"`),
  729 `rebind!`, 784 `move!`, 968 `heartbeat-state!`. The lock is taken from
  orchestrate inside the messenger at 446-470.
- Breaks: stop. Ending a flow happens outside Flow, through `hm-retire` run
  by hand, so Flow cannot reap in the refresh event. Related witness:
  PR/tools/reaper 31 still reads `~/.local/state/hacky-messenger/*.json`, a
  store that messenger-clj no longer uses (core.clj 113-116 uses
  `.local/state/messenger-clj` Datalevin): a dead reaper.

### B4. Flow identity is a claim carried in the environment (witnessed)
- Concept: who is calling. VF 20 and vision-nexus.md ("a Nexus knows its
  caller by the process, never by a claim") require the calling process to
  identify itself.
- Held in: the `FLOW_ID` environment variable, which the launcher sets and
  everything downstream trusts. PR/tools/claude-main-flow-launch.mjs 166-168
  `return ... FLOW_ID=${sh(flowId)}`; MC core.clj 906
  `(let [sender (or *flow-id* (System/getenv "FLOW_ID") (fail "Set FLOW_ID ..."))`;
  also 447 (lock owner) and 713 (`retired_by`). The id itself is minted by
  the `flow-id` tool (claude-main-flow-launch.mjs 179-180, `flow-id claude
  --flows-root ...`), packaged from the harness repository
  (CH/modules/home/core-packages.nix 23-27, "parent-flow identity helper").
  It is not minted by Flow.
- Breaks: run. Any process can send as any flow, and a subprocess with a
  stale or inherited `FLOW_ID` acts under the wrong identity.

### B5. Harness hooks call Primary scripts and the messenger, not the Flow CLI (witnessed)
- Evidence: PR/tools/claude-main-flow-launch.mjs 154-161 installs a
  `UserPromptSubmit` hook (`reminder-hook.py`) and a `Stop` hook
  (`primary-committer/turn-end.mjs`). turn-end.mjs 15 `const flow = env.FLOW_ID;`
  and 41 `run('hm-send', [committer, '--stdin'], ...)`.
- Should be: hooks call the Flow CLI (VF 56). Breaks: run. Flow never learns
  that a turn ended, so it cannot know flow state without polling.

### B6. Supervision and restart of a flow in a Primary tool with its own unit (lead: untracked work in progress)
- Evidence: PR/tools/primary-committer/restart.mjs 62-91 (`register`, then
  watch; on death `deregister` and `register` through the messenger), 177
  (Herdr `agent start ... --executable`); restart-service.nix 40-50 defines a
  systemd user unit from inside Primary's tools. All three files are untracked
  (`git status`).
- Should be: Flow, which owns the replacement of flows. A systemd unit
  belongs in CriomOS-home. Breaks: stop and turn.

### B7. A second Claude launch and refresh route through Claude's private daemon (witnessed)
- Evidence: PR/tools/claude-native-seat-refresh.py 26-27
  `DAEMON_ROOT = pathlib.Path(f"/tmp/cc-daemon-{os.getuid()}")`,
  `KEY_PATH = ... ".claude/daemon/control.key"`, and 647-653 (connects to
  `control.sock`). This is a 1028-line launch and bootstrap path alongside B1.
- Not a weld (nothing modified) but rests on an undocumented vendor
  interface; refresh belongs to Flow (VF 58). Breaks: turn.

### B8. Polling inside our components (witnessed)
- MC core.clj 455-466: the lock is retried with
  `(Thread/sleep (long *reservation-retry-ms*))` (50 ms) until 15 s pass.
- PR/tools/claude-main-flow-launch.mjs 244-247 `async function poll(...)`
  re-reads the transcript every second. claude-native-seat-refresh.py has
  `time.sleep` loops at 206, 228, 587, 605 and 696.
- vision-nexus.md 141-144 forbids polling, and VF 56 requires an unavoidable
  poller to be registered. Breaks: stop. Nothing goes quiet.

### B9. Permission mode is baked into the Claude Code package (witnessed)
- CH/owned-agents/claude-code/default.nix 52-54
  `wrapProgram $out/bin/claude ... --add-flags "--dangerously-skip-permissions"`.
  The launcher also passes the same flag (claude-main-flow-launch.mjs 297).
- Concept: launch permission mode. Held in: the user-environment package.
  Should be: Flow's launch. Breaks: turn. No caller can launch Claude in any
  other mode.

### B10. Curriculum emits launcher code into Primary and defines harness subagents (witnessed, lower)
- /git/github.com/LiGoldragon/Curriculum/src/projection.rs 434-442 writes
  `tools/standing-skill-selection.mjs`, which the Primary launchers import.
  PR/tools/standing-skill-selection.mjs line 1 reads `// Generated by
  curriculum-deploy`. roles.datom defines Codex and Claude subagents
  (`explorer`, `worker`, `tester`, `book`), which VF 60-62 says are replaced
  by Flow subflows.
- Projecting skill trees is sanctioned (PR/CLAUDE.md, "Regenerate them
  through Curriculum Nexus"). The launcher code and the subagent definitions
  are the misplaced part. Breaks: turn. Launch policy is split between
  Curriculum and Primary.

### B11. Deployment state in a knowledge skill (witnessed, lower)
mind-skills/skills/knowledge-flow.md 12-26 holds dated store paths, versions
(client 0.23.0, service 0.14.0, source 0.24.0) and socket paths; these belong
in Flow's own status or skill variables. Breaks: walk (stale facts acted on).

## Unknowns
- Not audited, because they are not listed in PR/SKILL_VARIABLES.md: the flow,
  nexus and orchestrate sources, Lojix, goldragon, and the harness repository
  (the source of `flow-id`). So whether Flow 0.24 already implements Launch,
  hooks, lock or retirement (which would make B1-B5 duplicates rather than
  gaps) is unknown. messenger-clj was audited because the base context names
  it under `Repository root`. CriomOS-pkgs is out of scope.
- No subagent tool was available in this thread, so the Opus fan-out the
  brief ordered did not run. Every finding comes from this flow's own reading.
  The `flow-evidence` skill could not be loaded because no Skill tool is
  available. `FLOW_ID` and `FLOW_DIRECTORY` were empty in this environment.
  No provenance receipt is available.
- Not read whole: core.clj beyond the cited functions,
  codex-/opencode-/native-worker-launch.mjs bodies, claude-native-seat-refresh.py
  beyond the cited lines, CH codex-remote-control.nix and flow-message-next.nix,
  CH/packages/pi/patches/extension-context-theme-persistence.patch
  (it adds `setTheme` to Pi's extension API; this looks like a weld but its
  purpose was not qualified), and the pi-subagents patch
  (CH/packages/pi-subagents/reconciliation, which rewrites the vendor's
  SKILL.md; its consumer is unknown).
- Not checked: whether Herdr or Claude Desktop offer a public setting that
  would replace A1 or A4, or whether a ruling sanctions A1-A3 (that would
  change their standing, not their anatomy).
