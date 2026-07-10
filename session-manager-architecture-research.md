# Persistent TUI harness sessions and message injection

## Decision

**Use terminal-cell, not tmux or abduco, as the PTY/session substrate.** Put a small durable Mentci session-manager above it. Keep Ghostty and Niri as disposable presentation only. Use provider-native asynchronous delivery where it exists (Codex app-server and Pi); allow terminal-cell PTY injection only as explicitly enabled, guarded fallback for live Claude/Codex/Pi TUIs.

This means changing the *shape* of the current Mentci integration, not terminal-cell: Mentci's current feature-gated `TerminalCellSurface::from_launch` embeds a `TerminalCell` actor and Tokio runtime in the Mentci process. It dies with Mentci. Instead launch/use the standalone `terminal-cell-daemon` and reconnect with `TerminalCellSocketClient` (`mentci/src/harness_liveness.rs:730-836`; terminal-cell `src/daemon.rs:90-159`).

## Findings

### 1. terminal-cell lifetime and reconnection

| Question | Answer and evidence |
|---|---|
| Child independent of terminal emulator? | **Yes.** `terminal-cell-daemon` owns the child PTY/process group; `terminal-cell-view` is a socket client. Dropping an attached viewer leaves the daemon and child alive; a later viewer replays transcript and continues (`ARCHITECTURE.md:66-72,195-208`; `tests/production_witnesses.rs:209-227`). Ghostty restart/close is therefore only a viewer detach. |
| Client reconnect after session-manager/daemon restart? | **No live-PTY reconnect contract.** State is actor memory; configuration explicitly says terminal-cell owns “no durable store” (`src/configuration.rs:161-165`). Actor stop kills the child (`src/session.rs:1512-1517`). Runtime metadata permits stale-session detection, not resurrection. A new daemon starts a new PTY/process; recover with the provider conversation ID, not an old socket. |
| Naming/enumeration | `LaunchCell.requested_name` is sanitized and suffixed with epoch milliseconds into `$XDG_RUNTIME_DIR/terminal-cell/session-<name>-<suffix>` (`src/lifecycle_cli.rs:370-399,717-745`). Metadata, PID files and two socket paths support lookup/selector; this is a convenience registry, not durable truth (`ARCHITECTURE.md:79-108`; README “Session listing…”). Runtime directories normally vanish on reboot. A manager must own stable logical IDs and durable names. |
| Resize | Any control client can resize the PTY; the view forwards initial size and `SIGWINCH` (`src/session.rs:1557-1568`; `src/bin/terminal-cell-view.rs:114-187`). Headless resize is tested (`tests/production_witnesses.rs:260-281`). One active viewer means no defined arbitration for competing viewer sizes. |
| Multiple clients | There may be multiple **control** clients and transcript subscribers, but exactly **one active raw viewer**; a second attach is rejected (`src/session.rs:879-1005`; `tests/production_witnesses.rs:230-257`). Treat manager/terminal-cell as the single writer/visible-view authority. |
| Transcript | In-memory append-only byte transcript, replay plus live broadcast (`src/session.rs:1523-1532,1622-1633`). It is **not lossless durable logging**: the viewer-to-scriber notification queue is 1024 and drops oldest under load (`src/session.rs:781-875,1018-1045`). Archive important events/transcript outside the cell if durable audit is required. |
| Input serialization | One `TerminalInputWriter` serializes Viewer and Programmatic bytes. The lease gate buffers viewer bytes while injection writes, then flushes them in order (`src/session.rs:438-625`); concurrent gate acquire is typed rejection (`tests/daemon_witness.rs:387-427`). Signal `WriteInjection` also checks a registered prompt pattern and rejects a dirty prompt by default (`ARCHITECTURE.md:371-384`). This prevents byte interleaving, **not** unsafe application-state injection. |
| Security | Control and data Unix sockets are mode `0600`, with plane separation; data accepts only attach and control rejects attach (`src/configuration.rs:14,145-159`; `src/daemon.rs:375-425,1061-1164`; `tests/daemon_witness.rs:205-285`). This is same-user local access, not per-client authorization. The manager must make its state/runtime directories `0700`, not expose sockets remotely, and treat transcript/input as private. |

The repository architecture itself records the desired ownership split: systemd supervises cells, a control component owns durable instance records and reconnects sockets, while terminal-cell remains the PTY primitive (`terminal-cell/ARCHITECTURE.md:109-118`). That is directly aligned with this design.

### 2. Installed provider surfaces

#### Codex CLI 0.144.1

**Yes: there is an installed, usable but explicitly experimental app-server protocol.** `codex --help` exposes `app-server [experimental]`; `codex app-server --help` supports stdio, Unix, and WebSocket listeners; `codex --remote <URL>` says it connects the TUI to a remote app-server endpoint. The local protocol generator successfully emitted a versioned schema bundle.

It supports thread/turn asynchronous delivery:

- `thread/start`, `thread/resume`, `thread/list`, `thread/read`, `turn/start`, `turn/interrupt`, and v2 `turn/steer` are present in the generated schema bundle.
- `TurnSteerParams` requires `threadId`, `expectedTurnId`, and user input. The expected active-turn ID is an explicit compare-and-fail precondition; response returns the turn ID.
- `ThreadResumeParams` explicitly says that when `threadId` identifies a running thread, app-server **rejoins** it; it recommends thread ID. Turn started/completed notifications are supplied.
- An active turn can reject steer/start as non-steerable (examples in schema: `/review` and manual `/compact`). This is desirable fail-closed behavior, not a reason to fall back to PTY bytes.

**Can it share an interactive TUI thread? Conditionally yes.** Start/own an app-server and launch the Codex TUI with `codex --remote unix://…`; then the manager is another app-server client which `thread/resume`s the same thread and sends `turn/steer` with the current turn ID. This is not evidence that a manager can attach to an arbitrary standalone `codex` TUI that was launched without the same app-server. The app-server/remote-control surfaces are explicitly experimental, so pin the exact CLI version and feature-detect schema/methods at startup.

Locators: installed `codex --version` = `codex-cli 0.144.1`; `codex --help`; `codex app-server --help`; `codex app-server generate-json-schema --out <temporary-dir>`; generated `v2/ThreadResumeParams.json` (running-thread rejoin), `v2/TurnSteerParams.json` (turn-ID precondition), `v2/TurnStartResponse.json` (non-steerable error), `v2/Turn{Started,Completed}Notification.json`.

#### Claude Code 2.1.206

There is **no documented local app-server-style API in the installed CLI** for an arbitrary controller to join a live interactive TUI and submit a user message. Confirmed surfaces are:

- Interactive `--resume <session-id>` / `--continue`, and `--session-id`.
- Headless/SDK-oriented `--print --input-format stream-json --output-format stream-json`; the help explicitly scopes streaming input to print mode.
- `--bg` plus `claude agents --json` enumerates active background/interactive sessions (pid, cwd, session ID, name, state); it is observation, not a send-message endpoint.
- **Remote Control is an additional supported-looking surface**, not merely headless/resume: `claude remote-control --help` describes a persistent local server controlled from claude.ai/code or Claude mobile, capable of multiple concurrent sessions and a pre-created session. It is a vendor-mediated product UI, however: no local machine-readable control socket, API, protocol, or CLI send operation was exposed by help. It must not be used as the manager's programmatic delivery contract without vendor documentation/approval.

Thus: use Claude Agent SDK/headless streaming when the manager owns the session; use terminal-cell only for an already-human-owned interactive Claude TUI, with injection default-off and guarded. Resume IDs recover conversation after process loss but do not restore an in-flight TUI.

Locators: installed `claude --version` = `2.1.206 (Claude Code)`; `claude --help:94-163`; `claude agents --help`; `claude remote-control --help` (persistent multi-session description).

#### Pi native steer

Pi steering is semantic in-process session control, not terminal automation. `AgentManager.steer` sends `record.session.steer(message)` to a running `AgentSession`, or queues `pendingSteers` until the session exists (`pi-subagents/src/agent-manager.ts:286-295,495-512`). The registered tool specifies delivery after the current tool execution “as a user message” (`src/index.ts:1514-1565`). It therefore has message ordering/agent interruption semantics that terminal-cell lacks. Pi intercom is a broker/message plane, not a keeper for arbitrary PTYs. The live `AgentSession` object must be manager-owned; persisted Pi sessions support resume, not reattachment to a lost in-memory steer object.

## Concrete component architecture

### Boundaries

```text
Ghostty/Niri ── disposable view ──> terminal-cell-view/data.sock
                                     │ raw PTY bytes
systemd --user ── supervises ──> terminal-cell-daemon (one per live TUI)
                                     │ control.sock 0600
Mentci Session Manager ──────────────┼── cell state, guarded PTY injection
                                     ├── Codex app-server client (native turn/steer)
                                     ├── Pi intercom/AgentSession adapter (native steer)
                                     └── Claude headless/SDK adapter (manager-owned only)
```

Create a stateful `mentci-session-manager` component with a public `signal-harness-session` contract.

- **Signal:** authenticated local Unix-socket admission for list/open/inspect/attach/inject/subscribe. Thin CLI is its first client. Do not expose terminal-cell byte sockets directly to other components.
- **Nexus:** starts/observes terminal-cell systemd units, app-server clients, Ghostty views, Niri IPC placement, transcript fanout and timeouts. It performs no durable state transition directly.
- **SEMA:** the sole persistent writer for logical sessions, native provider references, message sequence/idempotency, delivery results, view intent, and recovery state. It never stores credentials or raw secret messages in public/audit surfaces.

### Durable model and API sketch

```text
HarnessSession {
  id: SessionId, displayName: SessionName, harness: Pi|Codex|ClaudeCode,
  launch: { cwd, commandProfile, permissionProfile },
  provider: { codexThreadId? | claudeSessionId? | piSessionRef? },
  cell: { unitName?, runtimePath?, controlSocket?, dataSocket?, generation },
  state: Opening|Running|Detached|Exited|Recoverable|Orphaned|Retired,
  presentation: { niriWorkspace?, ghosttyAppId?, desiredView: None|Attached },
  transcript: { archiveCursor, retentionClass }, revision
}

SessionMessage {
  id: MessageId, sessionId, sequence, source, body, createdAt,
  delivery: PiSteer | CodexTurnSteer{expectedTurnId} |
            ClaudeHeadless | GuardedPty{promptPattern, cellGeneration},
  status: Accepted|Delivered|Rejected{reason}|UnknownAfterRestart
}
```

Public operations: `Open`, `List`, `Inspect`, `AttachView`, `DetachView`, `SubscribeEvents`, `SendMessage`, `Recover`, and explicit `Close`. `SendMessage` is idempotent by `(sessionId, MessageId)`, serialized by SEMA, and reports a provider receipt/typed rejection. It never silently retries an `UnknownAfterRestart` injection, because duplication is unsafe.

Native delivery order:

1. Pi `AgentSession.steer` for manager-owned Pi sessions.
2. Codex v2 `turn/steer` when an active `turnId` is known; `turn/start` only when no turn is active. Subscribe to app-server notifications and persist the current thread/turn IDs.
3. Claude SDK/headless stream only when launched and owned by the manager.
4. `GuardedPty` is opt-in only: acquire cell input gate, verify its generation and registered clean prompt pattern, write literal bytes, commit “accepted by PTY” (not “delivered as user message”), release gate. No automatic approval/permission response and no secrets.

### Lifecycle and presentation

- The user systemd manager, not Ghostty/Niri and not the session-manager parent process, supervises each `terminal-cell-daemon` in a distinct per-session user scope/service. The session-manager unit has `Restart=on-failure` and must not be `PartOf=` a cell unit. Restarting the manager then rediscovers live cells by its SEMA record plus cell sockets; restarting a cell means `Recoverable`, not continuation.
- On manager start, probe recorded sockets and process/worker state. A live cell reconnects without touching the child. A dead/missing cell transitions atomically to `Recoverable`; the provider adapter may launch a fresh cell with a native resume/thread ID, incrementing `cell.generation`.
- `AttachView` launches Ghostty with `terminal-cell-view` for that session; terminal-cell admits one interactive view. On exit, the view detaches and the cell remains `Detached`.
- Niri is only a reconciler: launch Ghostty with a distinct app-id/title, watch `niri msg event-stream`, then use JSON window ID plus `move-window-to-workspace`/focus actions. Installed Niri 25.11 supports JSON window/workspace lists and those actions. Never infer a live session from a Niri window.

## Why not tmux or abduco

- **tmux:** installed and excellent generic multiplexing, but its `send-keys` is UI automation, transcript capture is terminal rendering, and its multi-client semantics do not give provider-aware injection or terminal-cell's prompt/gate contract. It would duplicate the session/view ownership already implemented locally.
- **abduco:** installed and is terminal-cell's explicit conceptual reference, but has less control/transcript/prompt-arbitration surface and no advantage over the already-pinned terminal-cell daemon.
- **terminal-cell:** already provides daemon-owned PTY, named runtime cells, detach/reattach, raw view, resize, control/data separation, single writer/gate, transcript capture, and Mentci integration. Its missing durable registry is exactly the manager's responsibility, not a reason to replace it.

## Phased plan

1. **Foundation:** introduce the contract and SEMA record; add an external-daemon terminal-cell adapter without enabling automatic PTY injection. Persist provider session/thread references at creation. Add per-cell systemd unit/scope design and `0700` manager state directory.
2. **Recovery/view:** manager startup reconciliation; Ghostty attach command; Niri event-based placement. Validate terminal-emulator close/reopen and manager restart against a live child.
3. **Native delivery:** implement Pi steer and Codex app-server adapters behind capability negotiation. Codex must use one manager-owned app-server and a TUI explicitly launched with `--remote`; reject unsupported schema/version rather than downgrade.
4. **Claude:** manager-owned headless/SDK sessions and resume support. Treat Claude remote control as a human-facing optional view unless Anthropic publishes a controller contract.
5. **Guarded fallback:** only after the tests below, enable an explicit per-session PTY injection policy for human-owned TUIs. Keep auto-approval and secret injection prohibited.

## Required tests for state-safe injection

1. Cell process survives Ghostty/view disconnect; late view receives replay; manager restart reconnects to the same child/socket.
2. Manager/cell restart is distinguished: killing the cell produces `Recoverable`, does not claim continuity, and resumes a new provider process with incremented generation.
3. Concurrent `SendMessage`s have stable message sequence/idempotent result; duplicate/unknown-after-restart messages are not replayed.
4. Two writers: human bytes are held while a guarded programmatic message writes; they flush after release in order. Assert second lease fails and stale lease cannot release/inject.
5. Dirty/missing prompt pattern, stale generation, active approval/modal, and timeout all reject before PTY bytes are written. Test multiline/control bytes separately.
6. One active viewer; a second attach is rejected. Competing resize policy is deterministic (active view only, or manager-owned fixed size).
7. Transcript flood shows the manager marks terminal-cell capture as best-effort and preserves its own event/audit cursor without claiming lossless PTY history.
8. Codex integration: manager and `codex --remote` rejoin same thread; notification-derived expected turn ID permits `turn/steer`; stale ID and non-steerable turn reject without fallback; app-server restart/thread resume is explicit.
9. Pi integration: steer while tool runs becomes a user message after tool completion; queued-before-session steer is delivered once; manager restart never falsely acknowledges a lost live steer.
10. Claude: prove only manager-owned headless stream accepts real-time input; prove interactive TUI is not targeted by an undocumented channel. Remote-control behavior needs vendor-approved manual acceptance, not an automated assumption.
11. Security: sockets/state/transcript are inaccessible to another UID; unauthorized manager client cannot list/inject; logs redact message bodies/secrets; no view-placement action changes a session's authority.

## Residual vendor-contract uncertainty

- Codex app-server is labelled experimental in installed 0.144.1. Schema proves operations and thread rejoin semantics for this binary, but not a forward compatibility promise. Pin and generate/validate schema at deployment.
- The `--remote` help proves a TUI can connect to an app-server endpoint; an end-to-end shared-thread test is still required before declaring the multi-client TUI topology supported in production.
- Claude 2.1.206 Remote Control is real and persistent but is documented by CLI help only as claude.ai/mobile control. No local external message API was confirmed. Vendor documentation is needed before treating it as automation.
- terminal-cell's transcript is intentionally lossy under overload and its runtime registry is non-durable. The manager must not represent either as durable truth.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Completed only the requested read-only architecture research. No repository or runtime configuration was changed."
    },
    {
      "id": "criterion-2",
      "status": "satisfied",
      "evidence": "Report records pinned local source/version locators, installed CLI evidence, explicit architecture choice, phased plan, API/data model, tests, and vendor-contract gaps."
    }
  ],
  "changedFiles": [
    "/home/li/primary/session-manager-architecture-research.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "inspected terminal-cell pinned source and Mentci/Pi source with sed/rg/find",
      "result": "passed",
      "summary": "Located terminal-cell revision ad133289c2fe3f37e33a515ecf4a5facdb826fd7 and verified daemon, socket, lifecycle, transcript, viewer, and gate behavior."
    },
    {
      "command": "codex --version/--help; codex app-server generate-json-schema --out <temporary-dir>",
      "result": "passed",
      "summary": "Verified Codex CLI 0.144.1 experimental app-server, remote TUI option, and generated thread/turn/steer schemas."
    },
    {
      "command": "claude --version/--help; claude agents --help/--json; claude remote-control --help",
      "result": "passed",
      "summary": "Verified Claude Code 2.1.206 resume, headless stream, session enumeration, and vendor Remote Control surfaces; no local controller API was exposed."
    },
    {
      "command": "tmux list-commands; abduco usage; niri msg --help/action --help; systemctl --user --version",
      "result": "passed",
      "summary": "Confirmed available local session, compositor, and user-manager integration surfaces."
    }
  ],
  "validationOutput": [
    "terminal-cell source and its witness tests explicitly prove viewer detach/reattach, single-viewer rejection, resize, socket mode 0600, and input-gate serialization.",
    "Codex schema generation completed in a temporary directory and was removed within the command; no runtime configuration was modified."
  ],
  "residualRisks": [
    "Codex app-server/remote behavior is experimental and needs pinned end-to-end validation.",
    "Claude exposes Remote Control but no confirmed local programmatic injection protocol.",
    "terminal-cell transcript is lossy under overload and cell restarts cannot preserve a live PTY."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added the requested read-only research report only.",
  "reviewFindings": [
    "no implementation blockers in the report; independent reviewer should specifically challenge the Codex shared-thread integration before approval."
  ],
  "manualNotes": "Recommended implementation boundary is external terminal-cell daemons supervised independently of a restartable Mentci session-manager; native provider delivery precedes guarded PTY injection."
}
```