# Scout Situational Map — Mentci → Orchestrate → Harness → terminal-cell Claude session flow

## Task And Scope

Read-only ground-truth map for a later design worker. The design must specify:
Mentci prompt → orchestrate session decision (reuse / create / archive) → harness Claude
launch/resume → terminal-cell Claude TUI → harness event stream → Mentci display.

I mapped what exists today across the wire contracts, harness Claude mechanics,
orchestrate session state, the terminal-cell surface, and current boundary reality.
I did not edit code, run non-inspection tests, commit, push, inspect `private-repos/`,
read `~/.claude`, or search `/nix/store`. Observations carry `repo/path:line` witnesses;
interpretations are marked as such.

Repos live under `/git/github.com/LiGoldragon/`. All relevant repos were clean at
inspection (`jj log -r main`), current heads:

- `harness` — `f07c4dfe17` (rehome: integrate archived intent into ARCHITECTURE)
- `signal-harness` — `52cd2ed9fc`
- `orchestrate` — `b25c1894d7` (add ArchiveWorktree lifecycle + GC manifest reader)
- `signal-orchestrate` — `76a663a2e1`
- `mentci` — `d467236348`
- `signal-mentci` — `0859e6a5a9`
- `terminal-cell` — `e87dd66b99`

## Confirmed-Fact Cross-Check (against brief)

- Multi-watcher transcript + cross-harness rejection are LANDED and present at current
  `harness` main. `harness/src/daemon.rs:709` stores `bound_harness: HarnessName`,
  `daemon.rs:937` rejects nested `WatchHarnessTranscript` whose `watch.harness != bound_harness`
  via `cross_harness_watch_event` (`daemon.rs:850`). The cited commit
  `81433075` (`reject cross-harness transcript watches`) is an ancestor of current main
  `f07c4dfe17` (verified `jj log -r '81433075::main'`). signal-harness
  `HarnessTranscriptToken` carries both `harness` and per-open `subscription` identity
  (`signal-harness/src/lib.rs:555`, `:574`). So "multiple watchers allowed and safe" holds.
- Claude JSONL/session-file state tracking is REAL and tested. `harness/src/claude.rs`
  (1445 lines) reads model, cwd, sessionId, permissionMode, tool_use, file edits,
  and stop_reason from JSONL. The test fixture
  `harness/tests/claude_artifact_observer.rs:15-23` uses real Claude JSONL shape
  (`"permissionMode":"bypassPermissions"`, `"model":"claude-3-5-haiku-latest"`,
  `tool_use` Write, `"stop_reason":"end_turn"`) and asserts `turn.model()` and
  file-write recovery. This backs "JSONL sufficient for model/cwd/tool-use state;
  TUI scraping not needed for state." The observer is observation-only.
- The exact live-proof flags `--dangerously-skip-permissions --model claude-haiku-4-5-20251001`
  are NOT in any committed source I found; they were run manually (prior scout
  `MentciClaudeGroundStatus`). Source instead carries `permissionMode:bypassPermissions`
  as an observed JSONL value and `claude-3-5-haiku-latest` as a test-fixture model string.

## Observed Facts By Map Area

### 1. Existing message/wire types between Mentci, orchestrate, harness

Mentci UI contract `signal-mentci` (`signal-mentci/src/schema/lib.rs:604` `enum Input`):
`PresentQuestion`, `PushUpdate`, `ObserveInterfaceState`, `AnswerQuestion`,
`ProposeEditedAnswer`, `CreateInterceptPolicy`/`Replace`/`Cancel`/`ListInterceptPolicies`,
`FetchParkedRequests`, `AnswerParkedRequest`, `RetractInterfaceObservation`.
`Output` (`:625`) mirrors these. This wire is entirely approval/question/pane/intercept.
Fact: there is NO Mentci operation carrying a user prompt to be routed to a session.
`PromptText` (`signal-mentci/src/schema/lib.rs:77`) is the text of an approval question
presented TO the psyche (`QuestionProposal.prompt`), not a prompt going to a model.

Orchestrate contract `signal-orchestrate` (`signal-orchestrate/src/lib.rs:1627` channel):
operations `Claim`, `Release`, `Handoff`, `Observe`, `Submit`, `Query`, `RunWorkflow`,
`ObserveWorkflowRun`, `WorkflowRunObservationRetraction`, `Watch`, `Unwatch`. It owns
`Role`, `Lane`, `LaneRegistration`, `Worktree`, workflow run machinery, and its OWN
`enum HarnessKind { Codex, Claude }` (`:723`) with wire-token round-trip (`:729`).
Fact: no `ChooseSession`/`CreateSession`/`ReuseSession`/`ArchiveSession` operation exists.

Harness contract `signal-harness` (`signal-harness/src/lib.rs:629` channel):
operations `MessageDelivery`, `InteractionPrompt`, `DeliveryCancellation`,
`HarnessStatusQuery`, `WatchHarnessTranscript` (opens `HarnessTranscriptStream`),
`UnwatchHarnessTranscript`. Reply/event set includes the full provider-neutral adapter
event family `AdapterReady`/`InputAccepted`/`Output`/`Progress`/`Completion`/
`ConfirmationNeeded`/`Stalled`/`Exited` (`:647-654`) plus transcript snapshot/observation/
retraction. Fact: no `LaunchHarness`/`ResumeHarness`/`SelectModel`/`CloseHarness`
operation. Harness instances are fixed at daemon startup by
`HarnessDaemonConfiguration.harnesses: Vec<HarnessInstanceConfiguration>`
(`signal-harness/src/lib.rs:910`, `:889`); there is no dynamic create-over-the-wire.

Who-talks-to-whom (Cargo deps):
- `mentci/Cargo.toml`: depends on `signal-harness`, `signal-mentci`, `signal-criome`,
  `signal-introspect`, `signal-persona`, and optional `terminal-cell` (feature
  `terminal-cell-runtime`, `:12`, `:28`). Fact: `mentci` does NOT depend on
  `signal-orchestrate`. Mentci does not talk to orchestrate today.
- `harness/Cargo.toml:39`: depends on `signal-terminal` (delivery via terminal socket).
  Fact: `harness` does NOT depend on `terminal-cell`, `signal-orchestrate`, or `signal-mentci`.

### 2. Harness Claude mechanics (implemented / stubbed / absent)

- Observation: IMPLEMENTED. `harness/src/claude.rs` — `ClaudeArtifactObserver`
  (`:16`), `ClaudeArtifactEventWatcher` with `notify` file-event + polling fallback
  (`:327`, `:367`), `ClaudeArtifactSnapshot` (`:964`), `ClaudeRecoveredTurn`
  (`:1050`, exposes `model`, `cwd`, `permission_modes`, `stop_reasons`, `tool_calls`,
  `file_edits`, `has_stop_reason_end_turn`, `has_completed_marked_turn`). Reads
  `sessionId`/`session_id` (`:594`), model (`:602`), stop_reason (`:606`),
  permission_mode (`:610`). Locates JSONL under a Claude home/project dir
  (`ClaudeProjectDirectoryName`, `:500`; `ClaudeDirectory`, `:517`).
- Transcript watch/stream: IMPLEMENTED and wired. `harness/src/daemon.rs:125`
  handles `WatchHarnessTranscript` and keeps the accepted stream open; per-open
  subscription tokens, same-harness multi-watch, cross-harness rejection (see cross-check).
- Delivery: IMPLEMENTED for two paths only — Pi RPC (`harness/src/pi.rs`, spawns
  `pi --mode rpc`, `:108`, `:157`) and terminal-socket frames (`harness/src/terminal.rs`
  via `signal-terminal`). MessageDelivery counts only after acceptance.
- Claude LAUNCH: ABSENT. There is no `Command::new("claude")`, no `--resume`,
  no `--model`, no `--dangerously-skip-permissions` emission anywhere in `harness/src`
  (grep over `src/` found only `pi.rs` spawn and terminal delivery). Harness can label
  an instance `HarnessKind::Claude` but has no code to launch, resume, select model,
  or close a Claude process.
- Resume: ABSENT as a mechanic. `claude.rs` reads a Claude `session_identifier` for
  observation/matching (`:71`, `:1022`) but nothing consumes it to build a
  `claude --resume <id>` launch. No resume-id validity check exists.
- Meta `Configure` (privileged reconfigure): stubbed/unimplemented per prior audit
  (`HarnessComponentDirection` scout); `meta-signal-harness` carries `Configure` only.

Interpretation: harness today is an OBSERVER + DELIVERY-FORWARDER + TRANSCRIPT-STREAM
component for Claude. The launch/resume/model/close half the settled intent assigns to
harness is not yet built there.

### 3. Orchestrate session state today

Persistent store `orchestrate/src/tables.rs`: tables are `claims`, `roles`,
`lane_registry`, `repositories`, `worktrees`, `activities`, `activity_next_slot`,
`divergences`, `divergence_next_slot` (`tables.rs:46-68`). Backed by a `sema_engine`
versioned store (schema version bumped `2 -> 3` for worktrees, `tables.rs:41`).
Fact: there is NO session / harness-session / provider-session table.

Closest reusable-record precedent = `Worktree` (`signal-orchestrate/src/lib.rs:690`):
fields `repository`, `branch`, `path`, `owning_lane`, `status: WorktreeStatus`,
`purpose: PurposeText`, `last_activity: TimestampNanos`, `pushed_state`. Orchestrate
already has a lifecycle/archive pattern for these — current main head literally adds
`ArchiveWorktree` transition + GC manifest reader (`orchestrate` head `b25c1894d7`).
`WorktreeStatus` (`:652`) and `TimestampNanos` (`:956`) exist.

Interpretation: to hold reusable Claude-session records, orchestrate would need a NEW
typed record + table roughly paralleling `Worktree`: topic/purpose summary, last-activity
timestamp, provider (`HarnessKind` already exists at `:723`), model, resume id/path, and
an archive status. The lane/worktree/`last_activity`/`ArchiveWorktree`/GC machinery is a
close template but no session noun exists yet.

### 4. terminal-cell surface

`terminal-cell/src/lifecycle_cli.rs:22` `enum CellRequest`: `LaunchCell`, `SendLine`,
`AttachViewer`, `CloseCell`, `ObserveCell`. `LaunchCell` (`:31`) is a fully generic PTY
launcher: `requested_name: Option<String>`, `working_directory: Option<String>`,
`command: String`, `arguments: Vec<String>`, `environment: Vec<CellEnvironmentVariable>`.
`SendLine` (`:58`) injects a line + CR into the child (`:66-68`). `AttachViewer` (`:77`)
attaches a disposable viewer. Fact: terminal-cell has ZERO Claude/resume/provider knowledge
— exactly the "PTY/TUI primitive only" the intent wants. A caller drives a Claude TUI by
setting `command = "claude"` and `arguments = ["--resume", id, "--model", m, ...]`.
Root CLI parses strict NOTA only, rejecting unknown args (prior scout `MentciClaudeGroundStatus`).

### 5. Boundary reality vs. settled intent

The provider-operation and session-choice logic the intent assigns to harness and
orchestrate CURRENTLY LIVES IN THE `mentci` DAEMON. This is the central boundary leak.

`mentci/src/` modules (`lib.rs:7-19`): `harness_adapters.rs` (862 lines),
`harness_sessions.rs` (838), `harness_liveness.rs` (894), `preflight.rs` (650) — ~3244
lines of provider/session logic inside the UI daemon.

- `mentci/src/harness_adapters.rs:29` `ClaudeCodeAdapter` with `launch()` (`:51`),
  argument construction (`arguments()` `:115`, adds `--add-dir`), `initial_input()`
  (`:129`), `stop_conditions()` (`:147`), `close_request()` (`:80`), and a full
  `ClaudeCodeEventMapper` (`:173`) mapping Claude transcript deltas to
  `harness_contract::HarnessEvent` (Ready/Output/Progress/Completion/ConfirmationNeeded/
  Stalled/Exited). Default command `DEFAULT_CLAUDE_COMMAND = "claude"` (`:26`).
- `mentci/src/harness_sessions.rs` holds the SESSION REGISTRY + reuse decision:
  `SessionAddressRecord` (`:93`), `NamedSessionAddress` (`:225`), `SessionRecordState`
  (`:202` Open/…), `register_or_reuse` (`:528`) which looks up `by_lane_name`, checks
  `state == Open`, and rejects on identity/metadata/persistence/launch-metadata mismatch
  (`:535-565`), and public `open_or_reuse` (`:737`). This IS the reuse-vs-new engine.
- `mentci/src/preflight.rs` is the "closed model call" today: `PreflightEngine<Api>`
  (`:55`) + `PreflightApi` trait (`:43`) call a model with `PreflightPrompt`
  (`api_prompt()` `:234`: "Emit exactly one NOTA MentciPreflightLaunch record")
  and parse `MentciPreflightLaunch` (`:65`). Fields: `scaffold: ScaffoldPointer`
  (which carries `reuse_policy: ReusePolicy`, `:81`), `session_identity`,
  `persistent_session`, `sandbox_privacy`, `stop_conditions`, `constraints`.

Intent-vs-reality table:

| Responsibility | Settled intent owner | Where it lives today | Gap |
|---|---|---|---|
| UI ingress/egress | mentci | `mentci` + `signal-mentci` | Aligned |
| Prompt → session choice (reuse/create/archive) | orchestrate | `mentci` (`preflight.rs`, `harness_sessions.rs`) | LEAK: in Mentci, not orchestrate |
| Session registry (reusable records) | orchestrate | `mentci/harness_sessions.rs` (in-memory) + none in orchestrate | Missing in orchestrate |
| Claude launch/resume/model/close | harness | `mentci/harness_adapters.rs` (`ClaudeCodeAdapter`) | LEAK: in Mentci, not harness |
| Claude session observation (JSONL) | harness | `harness/src/claude.rs` | Aligned (only half built in harness) |
| Adapter→neutral events | harness | BOTH: `mentci` event mapper AND `signal-harness` event types | Split / duplicated shape |
| PTY/TUI primitive | terminal-cell | `terminal-cell` | Aligned |
| Transcript multi-watch | harness | `harness/src/{daemon,subscription}.rs` | Aligned, landed |

Interpretation: the design's core migration is moving `preflight.rs` +
`harness_sessions.rs` session-choice/registry into orchestrate, and moving
`harness_adapters.rs` Claude launch/event-mapping into harness, leaving Mentci as pure UI.
Note the event-shape already exists provider-neutral in `signal-harness` — Mentci's
`ClaudeCodeEventMapper` largely re-derives what harness's contract already defines.

### 6. Open questions — evidentiary footing

- One hot Claude session vs many for V1: harness config allows MANY instances
  (`HarnessDaemonConfiguration.harnesses: Vec<…>`, `signal-harness/src/lib.rs:922`) and
  transcript watching is explicitly multi-watcher. Mentci's registry keys sessions by
  lane (`harness_sessions.rs` `by_lane_name`), so multiple named sessions are already the
  data model. No code enforces a single hot session. Interpretation: "many" is the
  cheaper-to-honor default; "one hot at a time" would be a NEW orchestrate policy, not a
  current constraint.
- "Too old to resume" signals available today: (a) Claude JSONL timestamps — observer
  reads per-record `timestamp` (`claude.rs:590`) and `ClaudeRecoveredTurn.timestamps()`
  (`:1121`); (b) JSONL/session-file mtime is implicitly available via the file watcher
  roots (`claude.rs:163`, `:359`) though no age policy consumes it; (c) Claude
  `session_identifier` presence (`:1022`) as resume-id existence, but NO resume-id
  VALIDITY check exists anywhere; (d) orchestrate `Worktree.last_activity: TimestampNanos`
  is the existing staleness-signal pattern to mirror. There is no implemented "too old"
  threshold today.
- Name for the closed prompt→existing-vs-new model call: the EXISTING convention in
  Mentci is "preflight" (`PreflightEngine`, `PreflightApi`, `PreflightModelProfile`,
  `MentciPreflightLaunch`, semantic profile `cheap-contained-preflight`,
  `preflight.rs:283`). A second existing convention for non-in-harness model calls is
  orchestrate's workflow `ModelAttestation` + `StepLog` (`signal-orchestrate/src/lib.rs:1062`,
  `:1053`) inside `RunWorkflow`. The design should pick a name consistent with one of
  these; "preflight" is the incumbent term for exactly this prompt-routing call.
- Exact typed messages Mentci ↔ orchestrate ↔ harness: enumerated in area 1. The binding
  reality: Mentci↔orchestrate has NO wire today (no dep, no op); Mentci↔harness shares
  only `signal-harness` types via the `mentci` crate depending on `signal-harness`;
  harness↔terminal-cell has NO wire (harness uses `signal-terminal`, not terminal-cell).

## Existing-vs-Missing Ledger (target flow)

| Target-flow element | Status | Witness |
|---|---|---|
| Mentci op carrying a user prompt for routing | MISSING | `signal-mentci/src/schema/lib.rs:604` (Input has no prompt-route) |
| Mentci → orchestrate wire | MISSING | `mentci/Cargo.toml` (no `signal-orchestrate` dep) |
| Orchestrate session choose/create/reuse/archive op | MISSING | `signal-orchestrate/src/lib.rs:1627` (ops list) |
| Orchestrate reusable-session record + table | MISSING | `orchestrate/src/tables.rs:46-68` (no session table) |
| Orchestrate archive-lifecycle template | PRESENT (worktree) | `orchestrate` head `b25c1894d7` `ArchiveWorktree`; `signal-orchestrate/src/lib.rs:690` |
| Orchestrate typed `HarnessKind` | PRESENT | `signal-orchestrate/src/lib.rs:723` |
| Session reuse decision engine | PRESENT but MISPLACED (in Mentci) | `mentci/src/harness_sessions.rs:528`, `:737` |
| Closed prompt→launch model call ("preflight") | PRESENT but MISPLACED (in Mentci) | `mentci/src/preflight.rs:55`, `:234` |
| Harness Claude launch | MISSING | no `Command::new("claude")` in `harness/src` |
| Harness Claude resume (id/path handling) | MISSING | `harness/src/claude.rs` reads id, nothing launches with it |
| Harness Claude model selection | MISSING | no `--model` emission in `harness/src` |
| Harness Claude close mechanics | MISSING (Pi/terminal only) | `harness/src/pi.rs`, `src/terminal.rs` |
| Harness Claude observation (JSONL) | PRESENT | `harness/src/claude.rs`; test `tests/claude_artifact_observer.rs` |
| Harness → terminal-cell drive path | MISSING | `harness/Cargo.toml:39` (`signal-terminal`, not terminal-cell) |
| terminal-cell generic launch/send/attach/close | PRESENT | `terminal-cell/src/lifecycle_cli.rs:22-37` |
| Claude launch/adapter in Mentci (to be moved) | PRESENT but MISPLACED | `mentci/src/harness_adapters.rs:29` |
| Harness transcript event stream (multi-watch) | PRESENT | `harness/src/daemon.rs:125`, `:937`; `signal-harness/src/lib.rs:574` |
| Provider-neutral adapter events on wire | PRESENT | `signal-harness/src/lib.rs:647-654` |
| Mentci display of harness events | PARTIAL | Mentci maps events (`harness_adapters.rs:173`) but has no wire op to ingest a harness stream; UI wire is approvals-only |

## Named Unknowns / Not Confirmed From Source

- Whether the live Claude proof drove terminal-cell (`terminal-cell` LaunchCell) or the
  archived `terminal`/`terminal-daemon` binary. Prior scout observed the live proof used
  `terminal-daemon` (archived `terminal` repo). The `mentci` crate has terminal-cell as an
  OPTIONAL feature (`terminal-cell-runtime`); I did not confirm which path the running
  proof used. This matters for "V1 uses terminal-cell directly."
- Whether harness's `signal-terminal` delivery path is intended to be replaced by direct
  terminal-cell driving, or coexists. `harness` depends on `signal-terminal`, not
  terminal-cell; the intent says V1 uses terminal-cell directly. Unresolved in source.
- `ReusePolicy` currently has a single variant `ReuseDeferred` (`mentci/src/preflight.rs:145`).
  Interpretation: reuse is scaffolded but deferred/unimplemented as policy — the "reuse vs
  new" decision content the design needs is a placeholder, not a live rule.
- No resume-id VALIDITY probe exists anywhere (only id presence). Whether a stale/invalid
  Claude session id fails resume gracefully is unproven.
- `message_router_harness_e2e` (`harness/tests/`) — noted per brief as a separate router
  follow-up; prior audits report it fails with an rkyv/router error. Not mapped deeply.
- I did not read the `mentci` daemon's full request-dispatch to confirm exactly how a
  prompt today reaches `preflight` → `harness_sessions.open_or_reuse` → adapter launch
  (only the module surfaces and `daemon.rs` connection handling were inspected).
- Not checked: `private-repos/`, `~/.claude` contents, `/nix/store`, and I ran no tests
  (only source inspection + `jj log` reads).

## Verification Notes

Every "PRESENT/MISSING/LEAK" claim above is backed by a cited `repo/path:line` or an
explicit grep-absence over the named `src/` tree. Ancestry claim (cross-harness fix in
current main) verified with `jj log -r '81433075::main'` in `harness`. No component tests
were run; no files edited.
