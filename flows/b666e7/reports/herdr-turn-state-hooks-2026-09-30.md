# Herdr turn state and hook evidence

Prepared 2026-09-30 for named consumer Psyche Opus `7328f4`. This is a
source-based evidence account. No live Herdr UI observation was made, and no
host or session probe was run.

## What the evidence settles

Herdr installed version `0.8.2` matches source tag `v0.8.2`. Its detector
(`src/detect/mod.rs:1-19`) derives state from periodic bottom-of-buffer
terminal text. The UI status mapping in `src/ui/status.rs:196-206,227-244`
is:

- red filled: blocked;
- yellow filled: working;
- teal filled: idle/unseen;
- green hollow: idle/seen;
- gray dot: unknown.

The living's wording should therefore be gently corrected where it says red
means busy: in Herdr `0.8.2`, red means **blocked** and yellow means
**working**.

`PaneState.seen` is defined in `src/pane/state.rs:3-20`. The transition logic
in `src/app/actions.rs:3095-3115` sets `seen=false` when a background pane
moves working→idle, and sets it true for the active tab. Focus-related paths
also mark seen: tab/pane focus in `src/app/actions.rs:1277-1297`, workspace
focus in `src/workspace.rs:504-512`, and agent focus in
`src/app/agents.rs:75-84`. Tests at `src/app/actions.rs:4882-4946` cover the
seen transition behavior. The v0.8.2 automation documentation (lines 76-82)
states that CLI reading does not mark a pane seen.

The installed Herdr integration assets are present and configured as
`SessionStart` identity reporters only: `~/.claude/settings.json`,
`~/.codex/hooks.json`, and `~/.codex-next/hooks.json` invoke their respective
`herdr-agent-state.sh session` scripts. The scripts report the harness session
identity to Herdr's `pane.report_agent_session`; they do not report turn
lifecycle or alter a Herdr dot. `installer/targets.rs:176-190` mentions event
mapping, but no active mapping beyond those identity reports was witnessed.
Official hook surfaces are consequently a separate source of possible turn events: [Claude Code
hooks](https://code.claude.com/docs/en/hooks) documents `SessionStart/End`,
`UserPromptSubmit`, `Stop`, `StopFailure`, and `Notification`; [Codex
hooks](https://learn.chatgpt.com/docs/hooks) documents `SessionStart/End`,
`UserPromptSubmit`, `Stop`, and `Interrupt`. The Codex documentation's
`transcript_path` behavior is unstable in the observed account, and matchers
for prompt/stop were unsupported.

## Binding and design consequence

The Flow adapter (`flow/crates/flow-nexus/src/herdr.rs:136-147,375-421`)
uses an exact Herdr snapshot binding and status for routing. Pane read/marker
operations deliver terminal content; they do not witness that the living read
it. The native transcript verifies launch receipt. These are different facts.

The design should therefore keep hook-derived turn state separate from Herdr
UI focus acknowledgement. A hook can report turn lifecycle; Herdr focus can
acknowledge a pane as seen. A pane read or terminal delivery must not be
promoted to a human-read acknowledgement.

## Sources

- Herdr source tag `v0.8.2` and installed Herdr `0.8.2` comparison, as
  witnessed by Luna.
- Herdr `src/detect/mod.rs:1-19`.
- Herdr `src/ui/status.rs:196-206,227-244`.
- Herdr `src/pane/state.rs:3-20`.
- Herdr `src/app/actions.rs:1277-1297,3095-3115,4882-4946`.
- Herdr `src/workspace.rs:504-512`.
- Herdr `src/app/agents.rs:75-84`.
- Herdr v0.8.2 automation documentation, lines 76-82.
- Herdr `installer/targets.rs:176-190` and integration asset inspection.
- Flow adapter `flow/crates/flow-nexus/src/herdr.rs:136-147,375-421`.
- Native transcript launch receipt, as witnessed by Luna.
- [Claude Code hooks documentation](https://code.claude.com/docs/en/hooks).
- [Codex hooks documentation](https://learn.chatgpt.com/docs/hooks).
