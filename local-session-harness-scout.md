# Local session/harness reconnaissance

## Observed facts

- **Mentci already has a terminal-cell seam.** `/home/li/primary/agent-worktrees/mentci-os-update-2026-07-08/src/harness_liveness.rs:450-515` defines `TerminalSessionLauncher`, `TerminalSessionSurface` (`send`, `read_event`, `transcript`, `close`), and `TerminalCellDriver`; the feature-gated implementation at `:730+` imports `terminal_cell::{TerminalCell, TerminalCellSession, TranscriptSubscription, ...}` and uses a `kameo` actor. `Cargo.toml:12,28` makes `terminal-cell` an optional git dependency (`terminal-cell-runtime`); `Cargo.lock:1286` pins a git revision. This is a PTY/terminal-cell driver, not a durable external session daemon.
- **The driver already supports injection and transcript capture.** `harness_liveness.rs:90-135` has `LaunchRequest::with_initial_input`; `TerminalFeed` is raw bytes; the live session can send feeds and close with terminal input. `harness_adapters.rs:23-129` builds Claude launches, bracketed/interactive input, working directory, liveness and privacy metadata. Claude command defaults to `claude`, and arguments include `--add-dir` and `--name`.
- **Persistent named session model exists in Mentci.** `harness_sessions.rs:1-180` defines `NamedHarnessLaunch`, metadata (`HarnessKind::{ClaudeCode,Codex,Pi,...}`, adapter, terminal-cell driver, session model), `SessionAddressRecord`, named addresses and open/closed/retired state. Later in the file (`:680+`) `NamedHarnessSessions` owns a directory plus terminal-cell driver. Current evidence is in-memory directory/tests; no external daemon or on-disk PTY registry was found in this repo search.
- **Message/event component exists at the contract boundary.** `/home/li/primary/agent-worktrees/mentci-os-update-2026-07-08/tests/harness_adapters.rs:552-606` maps transcript/input/stop outcomes to `signal_harness::HarnessEvent` variants, including `MessageSlot`; `src/harness_adapters.rs` keeps provider-specific Claude parsing in the adapter. The test `claude_specific_behavior_is_not_in_generic_liveness_or_session_layers` (`tests/harness_adapters.rs:629+`) explicitly checks this ownership boundary.
- **Pi already implements live message injection and UI.** `/home/li/primary/agent-worktrees/pi-child-intercom-subagents/src/agent-manager.ts:495-515` has `AgentManager::steer`: deliver immediately via `record.session.steer(message)` or queue `pendingSteers` until session creation. `/src/index.ts:1514-1565` registers `steer_subagent`, documenting delivery after the current tool execution as a user message. `/src/ui/conversation-viewer.ts:46-75,229-240` provides an inline composer; `/src/ui/fleet-list.ts:270-295` wires it to `manager.steer`. `/CHANGELOG.md:14-32,568` corroborates persistent session/resume, fleet UI, and steering.
- **Pi has a broker/intercom session plane, but it is not a terminal multiplexer.** Home configuration `/home/li/primary/agent-worktrees/pi-subagents-acceptance-reliability-home-jj/modules/home/profiles/min/pi-models.nix:102-105,229-230` declares `pi-intercom` and its broker config; the packaged broker is currently running at `/home/li/.pi/agent/intercom/broker.pid` (process snapshot showed `pi-intercom ... broker.ts`). Pi sessions/indexes live under `/home/li/.pi/agent/sessions/` and are Pi-owned session persistence, not arbitrary process/PTY persistence.
- **Launch ownership is split by harness.** Home config `.../modules/home/profiles/min/default.nix:252-292` packages direct Claude, Codex, and Pi commands; `:271-280` defines `pi-testing` with separate `PI_CODING_AGENT_DIR` and `PI_CODING_AGENT_SESSION_DIR`. `pi-models.nix:153-207` projects Pi package/extensions (`pi-criomos`, `pi-subagents`, `pi-intercom`, `pi-session-namer`) into both normal and testing homes. There is no corresponding generic Claude/Codex session registry in this home module.
- **Terminal/compositor surface is Ghostty + Niri.** `.../modules/home/profiles/min/niri.nix:11-27,194-227,325-326` launches Ghostty (`+new-window`) and a rescue Ghostty via systemd scope; it declares `criomos-agent-tests` workspace. Live `/home/li/.config/niri/config.kdl` confirms Ghostty and rescue-terminal keybindings, workspace, and startup services. `/home/li/.config/ghostty/config` contains only presentation settings. Niri owns window/workspace placement and keybindings; it does not provide process/session persistence.
- **Multiplexer packages are present, but no active multiplexer was observed.** `.../modules/home/profiles/min/default.nix:306-311` installs `abduco`; `.../modules/home/profiles/med/cli-tools.nix:52-58` installs `tmux`. `/home/li/.tmux.conf` configures persistent tmux sessions, truecolor/extkeys, session/window linking, and detach-on-destroy behavior. `command -v` found `tmux`, `abduco`, `niri`, `ghostty`, `pi`, `codex`, and `claude`; `zellij`, `kitty`, `foot`, `alacritty`, and `wezterm` were absent. Process inspection found no tmux/abduco process, but did find Niri, Pi, Claude, Codex API daemon, Pi-intercom broker, and Spirit services.

## Interpretation / ownership boundaries

- `terminal-cell` is the strongest reusable substrate for **structured terminal I/O, PTY transcript deltas, initial input, later feeds, exit, and liveness**. Mentci already wraps it behind provider-neutral traits and metadata, so adding a message/session-manager API there would avoid coupling generic liveness to Claude.
- A durable psyche-facing manager needs a separate ownership layer above `TerminalCellDriver`: identity/address persistence, reconnect/recovery, authorization, lifecycle across process restarts, and routing to Pi/Codex/Claude. Existing `NamedHarnessSessions` is the natural conceptual home, but currently appears in-memory and driver-bound.
- Pi’s `AgentManager`/`AgentSession.steer` is reusable for Pi-native injection only; it cannot inject into arbitrary Claude or Codex processes. `pi-intercom` is inter-agent messaging/broker infrastructure, not a PTY/session keeper.
- Niri/Ghostty should remain presentation/window placement surfaces. Neither is an appropriate persistence substrate. The tmux configuration demonstrates a ready external persistence option, but tmux is currently an optional user tool rather than an owned harness abstraction.

## Unknowns and blockers

- The local checkout does not contain the `terminal-cell` source (only the git dependency and wrapper); its exact restart/reconnect, resize, persistence, and security APIs require inspecting the upstream dependency repository.
- Codex and Pi adapter implementations were not found in the inspected Mentci worktree; `ClaudeCodeAdapter` is the concrete adapter evidence. Search did not establish whether other worktrees contain newer adapter code.
- No systemd user unit, socket protocol, or on-disk registry dedicated to a cross-harness session manager was found under the scoped worktrees/home configuration. Existing Pi session SQLite/index files and intercom broker state are product-specific.
- No active tmux/abduco sessions were enumerated; this was process/config inspection only, not a live multiplexer query.
- Niri live config is generated state; source ownership is the Home Manager module above, while `/home/li/.config/niri/config.kdl` is runtime evidence.

## Recommendation

Use **terminal-cell as the I/O substrate**, retaining Mentci’s provider-neutral `TerminalSessionSurface` and `HarnessEvent`/`MessageSlot` boundaries. Build a small **external/session-manager layer above it** (likely a user systemd service with a local authenticated socket and durable session metadata) rather than making terminal-cell itself the durable manager. Keep Pi steering as an adapter optimization, and add Claude/Codex feed adapters through the same manager. Do not make Niri/Ghostty part of persistence; use tmux only as an optional compatibility backend if terminal-cell cannot yet guarantee restart/reconnect. This recommendation is conditional on upstream terminal-cell confirming resize, reconnect, and child-process ownership semantics.

## Acceptance report

```acceptance-report
{
  "criteriaSatisfied": [
    {"id": "criterion-1", "status": "satisfied", "evidence": "Read-only reconnaissance only; no repository or runtime files were edited."},
    {"id": "criterion-2", "status": "satisfied", "evidence": "Report cites terminal-cell, Mentci harness/session/adapter layers, Pi steering/intercom, Niri/Ghostty, multiplexer configuration, launch paths, observed processes, unknowns, and a substrate recommendation."}
  ],
  "changedFiles": ["/home/li/primary/local-session-harness-scout.md"],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {"command": "find/rg/sed scoped local reconnaissance", "result": "passed", "summary": "Inspected relevant worktrees, source/configuration, and process/tool availability."},
    {"command": "command -v tmux zellij abduco kitty niri foot alacritty wezterm ghostty pi codex claude", "result": "passed", "summary": "Recorded installed command surfaces."},
    {"command": "ps -eo pid,ppid,comm,args", "result": "passed", "summary": "Observed current Niri, Pi, Claude, Codex daemon, intercom broker, and no active multiplexer."}
  ],
  "validationOutput": ["Report written at the authoritative requested path; no destructive commands or tests run."],
  "residualRisks": ["Upstream terminal-cell reconnect/resize/persistence semantics remain unchecked.", "Codex/Pi Mentci adapters may exist outside the inspected worktree."],
  "noStagedFiles": true,
  "diffSummary": "Added one read-only reconnaissance report; no repository changes.",
  "reviewFindings": ["no blockers"],
  "manualNotes": "The report itself is the only written artifact; runtime/configuration surfaces were not changed."
}
```