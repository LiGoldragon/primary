# Design — Mentci → Orchestrate → Harness → terminal-cell Claude session flow

Design pickup point for a later implementation lane. No production code changes,
no commits. Built directly on `agent-outputs/MentciOrchestrateSessionFlow/Scout-SituationalMap.md`
and the load-bearing source it cites; every claim carries a `repo/path:line`
witness or is marked interpretation. Schemas use nota-schema-docs pseudo-NOTA
(documentation, not the authoritative wire shape).

## 0 · The one fact that reshapes the migration

The scout mapped the three engines (`preflight.rs`, `harness_sessions.rs`,
`harness_adapters.rs`, plus `harness_liveness.rs`) as a ~3244-line blob "inside
the UI daemon." Two follow-up traces refine that: the blob is **library and
test-only machinery that no shipped daemon reaches.**

- The shipped `mentci-daemon` request path is exhaustively matched at
  `mentci/src/state.rs:106-136` (no wildcard arm) and handles only
  approvals / questions / interface-state / intercept-policy variants.
  `mentci/src/daemon.rs` and `state.rs` contain zero references to
  `preflight`, `harness_sessions`, `harness_adapters`, or `harness_liveness`.
- `PreflightEngine::launch` (`mentci/src/preflight.rs:335`), `open_or_reuse`
  (`harness_sessions.rs:737`), `NamedHarnessSessions::launch` (`:713`), and
  `ClaudeCodeAdapter::launch` (`harness_adapters.rs:51`) are invoked **only**
  from `mentci/tests/*` and the feature-gated `mentci/src/bin/mentci-claude-proof-test.rs`.
- The real process spawn is delegated to the external `terminal-cell` crate
  (`TerminalCell::spawn_session`, reached via `harness_liveness.rs:757`) behind
  the opt-in `terminal-cell-runtime` feature (`mentci/Cargo.toml:11-12`,
  `default = []`). A default `mentci` build compiles no live launcher at all.
- Harness's Claude observer is the mirror image: `ClaudeArtifactObserver` is a
  real, tested capability (`harness/src/claude.rs:16`, `harness/tests/claude_artifact_observer.rs`)
  but `harness/src/daemon.rs` never references `claude` — it is library/test-only
  in its correct home.

Interpretation: this is not a rip-from-live-code decomposition with consumers to
preserve. It is **relocating already-isolated machinery into its correct component
homes before it is ever wired live.** The migration is cheap and low-risk; the
expensive parts are the two genuinely-new wires (Mentci→orchestrate prompt
ingress, harness→terminal-cell launch) and the two genuinely-new stores
(orchestrate session store, harness live-session table). This also means the
mentci `ARCHITECTURE.md` "Possible Future Design" (`mentci/ARCHITECTURE.md:87-318`)
is the design-of-record being *revised* here, not live behavior being changed
(§9 records the divergence).

## 1 · Component ownership split (before → after)

Ground truth: each responsibility, the module it lives in today, and its target
home under the settled intent.

| Responsibility | Today (module, status) | Target home | Move |
|---|---|---|---|
| UI ingress/egress, approval state | `mentci` daemon + `signal-mentci` (LIVE) | Mentci | stays |
| Prompt ingress (user → UI) | absent (`signal-mentci` Input, `schema/lib.rs:604`, has no prompt op) | Mentci | **new op** |
| Display of live harness output | `mentci` maps events locally (`harness_adapters.rs:173`), no wire to ingest a stream | Mentci (subscribes to harness) | rewire to contract |
| Prompt → session choice (reuse/new) model call | `mentci/src/preflight.rs` `PreflightEngine` (test-only) | Orchestrate | **move** |
| Session registry + reuse decision | `mentci/src/harness_sessions.rs` `InMemoryHarnessSessionDirectory` / `register_or_reuse` (`:528`, test-only, in-memory) | Orchestrate (durable store) | **move + persist** |
| Session archive / GC policy | none (Mentci registry only marks Open/Closed/Retired, `harness_sessions.rs:202`) | Orchestrate | **new (mirror Worktree)** |
| Claude launch/resume/model/close | `mentci/src/harness_adapters.rs` `ClaudeCodeAdapter` (`:51`, test-only) | Harness | **move** |
| Adapter transcript → neutral events | `mentci` `ClaudeCodeEventMapper` (`harness_adapters.rs:173`) **and** `signal-harness` `AdapterEvent` family (`signal-harness/src/lib.rs:647-654`) | Harness (reuse contract types) | **move + dedupe** |
| terminal-cell driver + liveness (send/read/idle/stall/close) | `mentci/src/harness_liveness.rs` `TerminalCellDriver` (feature-gated) | Harness | **move** |
| Claude JSONL/session observation | `harness/src/claude.rs` (library/test-only, right home) | Harness | wire to daemon |
| PTY/TUI process primitive | `terminal-cell` `CellRequest` (`lifecycle_cli.rs:22`) | terminal-cell | stays |
| Transcript multi-watch stream | `harness/src/daemon.rs:125`, `signal-harness/src/lib.rs:661` | Harness | stays (landed) |

Net after the split:

- **Mentci** = pure UI organ. Adds one inbound prompt op and one outbound
  route call; drops the four `harness_*`/`preflight` modules entirely (they were
  never live). Displays a live session by subscribing to harness's transcript
  stream (already a landed multi-watch producer).
- **Orchestrate** = session-choice/create/reuse/archive owner. Gains the routing
  model call, a durable session store modeled on `Worktree`, and a meta-signal
  archive/GC lifecycle modeled on `ArchiveWorktree`.
- **Harness** = Claude operation owner. Gains the adapter (argv/model/initial-input/
  close), the terminal-cell driver+liveness, a dynamic session-open operation, and
  wires its existing JSONL observer into the live session.
- **terminal-cell** = unchanged generic PTY primitive.

## 2 · Typed messages (contract-repo + push-not-pull)

Four new operations plus reuse of the existing harness event family. Producers
push; every consumer subscribes once and receives current-state-then-deltas
(`orchestrate/ARCHITECTURE.md:376`, push invariant; `push-not-pull`).

### 2a · `signal-mentci` — user prompt into the UI daemon (new)

A Mentci client submits a prompt to the Mentci daemon. New ordinary variant on
`Input` (`signal-mentci/src/schema/lib.rs:604`) and its `Output` mirror (`:625`).

```nota
;; New Input variant: a raw user prompt to be routed to work.
(SubmitPrompt <prompt-text> <work-surface> <hard-constraints>)
;;   prompt-text     : PromptBody          ;; new newtype; not QuestionProposal.PromptText (that is a question shown TO the psyche, signal-mentci lib.rs:77)
;;   work-surface    : WorkSurface
;;   hard-constraints: [LaunchConstraint]   ;; first-proof sandbox requirement lives here

;; New Output variant: acknowledgement carrying where to watch.
(PromptRouted <session-address> <disposition> <harness-name>)
;;   disposition : Reused | Created
;;   harness-name: HarnessName             ;; the harness the client then watches (signal-harness)
```

Rationale: the prompt op is genuinely distinct from `QuestionProposal.prompt`
(an approval question presented to the human, `signal-mentci/src/schema/lib.rs:77`).
The reply carries `harness-name` so the client knows which harness transcript to
`WatchHarnessTranscript`, rather than Mentci re-streaming output through its own
wire (that would re-add provider coupling to the UI).

### 2b · `signal-orchestrate` — Mentci asks orchestrate to route (new, ordinary)

Mentci gains a dependency on `signal-orchestrate` (it has none today,
`mentci/Cargo.toml`). New ordinary operation on the `Orchestrate` channel
(`signal-orchestrate/src/lib.rs:1627-1640`) and a reply on `Reply` (`:1641-1660`),
modeled on the ordinary `RunWorkflow` → `WorkflowRunAccepted` shape.

```nota
;; Ordinary operation: route a prompt to an existing-or-new session.
(RouteSession <prompt-text> <work-surface> <hard-constraints>)

;; Reply: the chosen session and how it was chosen.
(SessionRouted <session-address> <disposition> <launch-directive>)
;;   session-address : (SessionAddress <lane> <session-handle>)
;;   disposition     : Reused | Created
;;   launch-directive: FreshLaunch | ResumeExisting   ;; what orchestrate then tells harness
```

`RouteSession` is ordinary because Mentci is an ordinary peer; ordinary peers
cannot compile meta orders (`orchestrate/ARCHITECTURE.md:374-375`). Orchestrate
lowers it internally: run the routing model call (§5), consult the session store
(§3), decide reuse-vs-create, write the store, then push the launch directive to
harness (§2c). The reply returns fast with the address + disposition; live output
does not flow back through this reply — the client subscribes to harness.

### 2c · `signal-harness` — orchestrate opens a Claude session (new)

Orchestrate gains a dependency on `signal-harness` and drives harness to open the
session. The scout confirmed harness has **no** dynamic launch/resume/model/close
operation today — instances are fixed at daemon startup
(`signal-harness/src/lib.rs:889-922`). New operation on the `Harness` channel
(`signal-harness/src/lib.rs:629-637`).

```nota
;; New operation: open (fresh or resumed) a Claude session under a named harness.
(OpenClaudeSession <harness> <session-handle> <launch-plan>)
;;   harness    : HarnessName
;;   launch-plan: (ClaudeLaunchPlan <resume> <model> <working-directory>
;;                                  <scaffold-path> <initial-input> <stop-conditions>)
;;     resume          : FreshSession | (ResumeSession <claude-resume-identifier>)
;;     model           : HarnessSessionModel        ;; semantic knob, not a raw model literal
;;     stop-conditions : [StopCondition]            ;; IdleTimeout | TurnCap | CompletionSignal
```

Replies/events **reuse the existing provider-neutral family** rather than
re-inventing it: `AdapterReady` / `AdapterInputAccepted` / `AdapterOutput` /
`AdapterProgress` / `AdapterCompletion` / `AdapterConfirmationNeeded` /
`AdapterStalled` / `AdapterExited` (`signal-harness/src/lib.rs:647-654`). This is
exactly the vocabulary Mentci's `ClaudeCodeEventMapper` currently re-derives
(`harness_adapters.rs:240-317`); the mapper's *body* moves to harness, but its
*output type* is already the contract — delete the duplicate shape.

Per-turn delivery into an already-open session uses the **existing**
`MessageDelivery` op (`signal-harness/src/lib.rs:144`); a reused session with a
new prompt is "resume (if cold) + `MessageDelivery`." Note: rich per-turn message
routing into a live harness is the deferred `message_router_harness_e2e` path and
is out of scope here (see §8).

### 2d · Harness → orchestrate — keep the session store fresh (push, subscription)

Orchestrate's store needs the recovered Claude session-id, model, and last-activity
to make future reuse/age decisions. The producer of those facts is harness's
JSONL observer (`harness/src/claude.rs`). Per push-not-pull, harness pushes and
orchestrate subscribes — **reusing harness's landed multi-watch transcript stream**
(`signal-harness/src/lib.rs:661-666`; multi-watcher is safe by design,
Scout-SituationalMap §cross-check). Add one typed observation event to that stream
carrying store-shaped facts (the raw `TranscriptObservation` line is too weak):

```nota
;; New stream event on HarnessTranscriptStream: store-shaped session facts.
(ClaudeSessionObservation <harness> <session-identifier?> <model?> <last-activity> <lifecycle>)
;;   session-identifier?: ClaudeResumeIdentifier   ;; recovered from JSONL (claude.rs:594,1022)
;;   model?             : DetectedModel             ;; recovered (claude.rs:602)
;;   last-activity      : TimestampNanos            ;; from JSONL timestamps (claude.rs:590,1121)
;;   lifecycle          : Ready | Active | Completed | (Exited <exit-status>)
```

Orchestrate subscribes to the harness it just opened (it knows the `HarnessName`
from §2c), receives current-state-on-connect then deltas, and writes
`last_activity` / `resume_locator` / `model` into the session record (§3) — the
same infrastructure-minted discipline as `Worktree.last_activity`
(`orchestrate/src/worktree.rs:52-54`, never agent-supplied).

## 3 · Orchestrate session-store schema

A new durable record + redb table + NOTA GC projection, modeled beat-for-beat on
`Worktree` (`signal-orchestrate/src/lib.rs:690`), its store twin `StoredWorktree`
(`orchestrate/src/tables.rs:97-106`), and its lifecycle (`orchestrate/src/worktree.rs`).
Typed records over flags throughout (`typed-records-over-flags`).

```nota
;; The reusable Claude-session record. Lives in signal-orchestrate; the durable
;; twin StoredHarnessSession lives in orchestrate/src/tables.rs. (lane, handle) is
;; the identity, mirroring Worktree's (repository, branch).
(HarnessSession <lane> <session-handle> <topic-summary> <provider> <model>
                <resume-locator?> <working-directory> <status> <last-activity>
                <origin-prompt-digest>)
;;   lane                : LaneName            ;; stable lookup key, derived from session intent not provider (mentci/ARCHITECTURE.md:150)
;;   session-handle      : SessionHandle       ;; the token returned to later callers
;;   topic-summary       : PurposeText         ;; reuse Worktree.purpose type; the routing model's one-line topic
;;   provider            : HarnessKind         ;; reuse signal-orchestrate HarnessKind {Codex, Claude} (lib.rs:723)
;;   model               : ModelName           ;; new newtype (absent today outside the fixture workflow)
;;   resume-locator?     : (ClaudeResumeLocator <claude-resume-identifier> <transcript-path>)   ;; Option: present once observed
;;   working-directory   : WirePath            ;; the sandbox jj working copy
;;   status              : HarnessSessionStatus
;;   last-activity       : TimestampNanos      ;; infrastructure-minted from ClaudeSessionObservation, never agent-supplied
;;   origin-prompt-digest: PromptDigest        ;; content hash of the prompt that created it, for audit/dedupe

;; Lifecycle status. Enum, not a bool bundle — mirrors WorktreeStatus (lib.rs:652).
;;   Hot      : a live terminal-cell process exists in harness right now
;;   Idle     : no live process, but resume-locator makes it resumable
;;   Archived : left the hot set by policy; still resumable-by-id until GC
;;   Recycled : GC-eligible, resume no longer promised
(HarnessSessionStatus Hot | Idle | Archived | Recycled)
```

`resume-locator` is `Option<record>` not a bool: the "yes, resumable" answer
carries the id + transcript path a resume needs (`typed-records-over-flags` form 1).
The reuse decision that `harness_sessions.rs:535-568` performs in-memory (match
lane, reject on identity/metadata/launch-metadata mismatch) becomes a store query
against this record; the `SessionAddressMetadata` comparison
(`harness_sessions.rs:547`) collapses into matching `HarnessSession` fields.

Storage discipline (`rust-storage-and-wire`): the record is a schema-owned type in
the `worktrees`-sibling `harness_sessions` table; adding it is a coordinated store
schema-version bump (mirror `orchestrate/src/tables.rs:41-42`, the 2→3 worktree
bump). The `worktrees.nota` GC manifest gets a `harness-sessions.nota` sibling with
a `gc_candidates`-shaped reader returning `Archived | Recycled`
(`orchestrate/src/worktree_projection.rs:32-56`).

## 4 · Policy decisions [PSYCHE DECISION]

Each is marked for the human. Recommendation + the tradeoff; none silently
defaulted.

### 4a · One hot Claude session vs. many (V1) — [PSYCHE DECISION]

**Recommendation: many.** Every substrate already supports many: harness config
holds `harnesses: Vec<HarnessInstanceConfiguration>` (`signal-harness/src/lib.rs:922`);
the transcript stream is explicitly multi-watcher (`:567-577`); the reuse registry
keys by lane and already stores many named sessions
(`harness_sessions.rs:465`, `by_lane_name`). "One hot at a time" is not a current
constraint anywhere — it would be a *new* orchestrate eviction/queue policy built
on top.

Tradeoff: **many** = simplest to honor, matches the data model, but unbounded
concurrent `claude` processes + model-quota contention with no backpressure.
**One-hot** = a hard resource bound and a single mental model, but forces an
eviction-or-queue mechanism (which session gets suspended when a second prompt
arrives) that has no scaffolding today. Recommendation stands at *many for V1*,
with a soft cap (`Hot`-status count) as a later policy knob rather than a V1 gate.

### 4b · The "too old to resume" rule — [PSYCHE DECISION]

**Recommendation: resumable iff `resume_locator` present AND transcript file exists
AND `now - last_activity < resume_horizon`; the resume attempt is authoritative,
with graceful fall-through to a fresh launch on failure.** Defined only in signals
that actually exist:

- `last_activity: TimestampNanos` on the session record (§3), fed by
  `ClaudeSessionObservation` from JSONL timestamps (`harness/src/claude.rs:590,1121`)
  — the exact infrastructure-minted-staleness pattern `Worktree.last_activity`
  already uses (`orchestrate/src/worktree.rs:261-278`).
- transcript/JSONL file presence via the observer's roots (`claude.rs:163,359`).
- `resume_locator` presence = the recovered `session_identifier` (`claude.rs:1022`).

Critical gap the rule must absorb: **no resume-id *validity* probe exists anywhere**
(Scout §6; only id *presence*). So the rule cannot promise a stale id resumes — it
must treat "harness attempted `claude --resume <id>` and it failed" as a typed
outcome that falls through to `FreshLaunch`, and orchestrate flips the record
`Idle → Recycled` on that failure.

Tradeoff: a **short** `resume_horizon` (e.g. hours) yields fewer stale-resume
surprises but more cold starts that lose warm context; a **long** horizon (e.g.
days) maximizes reuse but leans harder on the (unproven) resume path. Because the
resume attempt is the real source of truth and there is no validity probe, the
recommendation leans **lenient horizon + attempt-and-fall-through**; the exact
`resume_horizon` duration is the psyche's to set.

### 4c · Archive policy — when/how a session leaves the hot set — [PSYCHE DECISION]

**Recommendation: event-driven exit plus an age sweep, mirroring the Worktree
lifecycle.** Three exits, in order of confidence:

1. **On harness `AdapterExited` / `ClaudeSessionObservation Exited`**: orchestrate
   moves `Hot → Idle` (process gone, still resumable). Push-driven, authoritative.
2. **Explicit `ArchiveHarnessSession`** meta order (a `meta-signal-orchestrate`
   order paralleling `ArchiveWorktree`, `orchestrate/ARCHITECTURE.md:361-364`):
   `Idle → Archived`, reproject the NOTA manifest.
3. **Age sweep**: sessions past `resume_horizon` (§4b) move `Idle → Archived`, and
   a GC reader returns `Archived | Recycled` for a daemon/external agent to reap —
   the unwired `gc_candidates` shape made concrete
   (`orchestrate/src/worktree_projection.rs:32-56`).

Tradeoff: **eager** archive (short horizon, aggressive sweep) frees processes and
quota fast but discards warm sessions a user might return to; **lazy** archive
keeps sessions warm but accumulates `Idle` records and stale resume ids. The
event-driven leg (1) is safe and recommended unconditionally; the psyche sets how
aggressive the age sweep (3) is (it shares `resume_horizon` with 4b, so 4b and 4c
should be ruled on together). Following the worktree precedent, archive is a
**meta-signal** order (owner authority), not an ordinary caller op.

## 5 · Naming the closed routing model call

The task asks for the name of the closed model call that reads a prompt and routes
it to existing-vs-new session — explicitly *distinct from an AI running inside a
harness*. Incumbent: "preflight" (`PreflightEngine`, `PreflightApi`,
`MentciPreflightLaunch`, profile `cheap-contained-preflight`, `preflight.rs:283`).

**Recommendation: rename to session routing — `SessionRouter` / operation
`RouteSession` / output `SessionRoutingPlan` — and retire "preflight" as the
concept name (keep it, if anywhere, only as a model-profile label).**

Reasoning per `naming` and `design-quality`:

- "Preflight" names a **timing** (checks *before* flight), not the **act**. The act
  is: route a prompt to a session decision + launch plan. The naming skill's rule
  is to name what the code does, not when it runs; a timing-word reads as imported
  ceremony to decode.
- Its home explains its old name: it lived at Mentci's *front door*, so it was
  named for the door. Once the act moves to orchestrate — whose domain verb is
  literally choosing/creating sessions — the honest name is the act. The
  code already keeps the right distinction (`ModelSlot::Preflight` vs
  `ModelSlot::HarnessSession`, `preflight.rs:32-35`); "session routing" preserves
  that distinction in a positive, English name.
- It composes cleanly against the neighbouring noun: **session router** (picks/creates
  the session) vs **message router** (delivers turns into a live harness, the
  deferred `message_router_harness_e2e` path). That is a clean, non-colliding pair
  — the session router runs once per prompt-to-session; the message router runs per
  turn. Name them on the *object* they route (session vs message), never abbreviated.

This is a judgment, not a [PSYCHE DECISION]: "preflight" is acceptable and is the
established cross-file term, so the rename is optional polish the implementer may
defer. But the spec's recommendation is to name the act.

## 6 · Restated end-to-end flow (new ownership)

1. A Mentci client (TUI/CLI) sends `SubmitPrompt` (§2a) to the `mentci-daemon`
   over `signal-mentci`. Mentci validates and forwards — it holds no provider or
   session logic.
2. Mentci daemon sends `RouteSession` (§2b) to orchestrate over `signal-orchestrate`
   (a **new** Mentci→orchestrate wire; none exists today, `mentci/Cargo.toml`).
3. Orchestrate runs the **session-routing model call** (§5, the relocated
   `preflight` engine) — a cheap contained model that reads the prompt and emits a
   fixed-schema plan (scaffold pointers, session identity, stop conditions,
   sandbox posture; the `MentciPreflightLaunch` shape, `preflight.rs:64`).
4. Orchestrate consults its **session store** (§3): match by lane + metadata
   (the relocated `register_or_reuse` logic, `harness_sessions.rs:528`) and apply
   the too-old rule (§4b) → decide `Reused` (with `resume_locator`) or `Created`.
   It writes/updates the `HarnessSession` record.
5. Orchestrate pushes `OpenClaudeSession` (§2c) to the chosen harness over
   `signal-harness` with a `FreshSession` or `ResumeSession <id>` launch plan.
6. **Harness owns Claude operation.** The relocated `ClaudeCodeAdapter`
   (`harness_adapters.rs:51`) builds argv/model/initial-input; the relocated
   `TerminalCellDriver` (`harness_liveness.rs`) drives **terminal-cell directly**.
   → **NEW WORK, §7 spine step 4.** Harness currently drives `signal-terminal`,
   not terminal-cell (`harness/Cargo.toml:39`, no terminal-cell dep;
   `harness/ARCHITECTURE.md:16-21`). The launch is a terminal-cell `LaunchCell`
   (`terminal-cell/src/lifecycle_cli.rs:31`) with
   `command = "claude", arguments = ["--resume", id, "--model", m, "--add-dir", …]`;
   feed/read/close use terminal-cell's control client
   (`terminal-cell/src/client.rs:77` `send_programmatic_input`, etc.). terminal-cell
   already speaks `signal-terminal` on its control plane (`terminal-cell/src/client.rs:5`),
   which partially resolves the scout's "coexist vs replace" unknown: harness's
   existing `signal-terminal` feed path can point at a terminal-cell control socket,
   while process *spawn* uses the terminal-cell lifecycle `LaunchCell` surface.
7. Harness's JSONL observer (`harness/src/claude.rs`, wire it into the daemon)
   watches the live session and pushes:
   - `AdapterOutput`/`AdapterReady`/`AdapterCompletion`/`AdapterExited` etc. on the
     transcript stream (reused contract types, §2c).
   - `ClaudeSessionObservation` (§2d) carrying recovered session-id / model /
     last-activity.
8. **Two independent subscribers** consume harness's stream (multi-watch, safe by
   design):
   - **Mentci** opens `WatchHarnessTranscript` on the `harness-name` it got back in
     `PromptRouted` (§2a) and renders live output — Mentci's *display*, no mapping
     logic left in it.
   - **Orchestrate** consumes `ClaudeSessionObservation` and updates the session
     record's `last_activity` / `resume_locator` / `status`, driving future reuse
     and archive (§4).
9. A later prompt for the same topic re-enters at step 1; step 4 resolves `Reused`;
   step 5 sends `ResumeSession`; per-turn delivery of the new prompt into the live
   session uses the existing `MessageDelivery` op (the message-router path, §8).

## 7 · Migration / sequencing spine (dependency order, not a task graph)

Build producers before consumers, contracts before movers, stores before routing.

1. **Contracts first.** Add the four typed surfaces (§2) to their contract crates
   with round-trip tests, no daemon wiring yet: `signal-mentci` `SubmitPrompt`;
   `signal-orchestrate` `RouteSession`/`SessionRouted`; `signal-harness`
   `OpenClaudeSession` + `ClaudeSessionObservation`; new newtypes (`ModelName`,
   `PromptBody`, `ClaudeResumeLocator`). Contract-repo discipline: no runtime leaks
   in, round-trips asserted (`contract-repo`).
2. **Orchestrate session store.** Add `HarnessSession` record + `harness_sessions`
   table + schema-version bump + `harness-sessions.nota` projection/GC reader,
   modeled on `Worktree`. No routing yet — just the store and its meta-signal
   `RegisterHarnessSession` / `ArchiveHarnessSession` orders.
3. **Harness → terminal-cell launch (the hard new capability).** Add the
   terminal-cell dependency to harness; move `ClaudeCodeAdapter` +
   `TerminalCellDriver`/liveness from `mentci/src/harness_{adapters,liveness}.rs`
   into harness; wire the JSONL observer into the daemon; implement
   `OpenClaudeSession` end-to-end against the sandboxed-jj first proof
   (`mentci/ARCHITECTURE.md:305-309`). Delete Mentci's duplicate
   `ClaudeCodeEventMapper` in favour of the contract `AdapterEvent` family.
4. **Orchestrate routing.** Move the `preflight` engine in (renamed per §5), wire
   `RouteSession` → routing model call → store query (§4b reuse rule) →
   `OpenClaudeSession` push → subscribe to `ClaudeSessionObservation`.
5. **Mentci rewire.** Add `SubmitPrompt` ingress + the `signal-orchestrate`
   dependency + the forward-to-`RouteSession` path; make the client watch the
   returned harness transcript for display. Delete the four now-relocated modules.
6. **Archive/GC sweep.** Wire the age sweep + `gc_candidates` reaper (§4c) once the
   store and observation feedback loop are live.

Because everything moved in steps 3–5 is currently test-only (§0), each move is a
relocation with its tests, not a live-consumer migration.

## 8 · Scope boundary — per-turn message routing (deferred)

`OpenClaudeSession` (§2c) carries the *initial* prompt as session initial-input,
exactly as `ClaudeCodeAdapter::initial_input` does today (`harness_adapters.rs:129`).
Delivering *subsequent* prompts/turns into a live-or-resumed session is the
existing `MessageDelivery` op (`signal-harness/src/lib.rs:144`) and belongs to the
deferred `message_router_harness_e2e` follow-up (Scout §6; task constraint). This
spec covers choose/create/open/observe/archive; it does not design the per-turn
router. A reused session with a new prompt (§6 step 9) therefore depends on that
deferred path for the turn delivery, though the resume itself is in scope.

## 9 · Open unknowns carried forward

- **Scout's flagged unknown — terminal-cell vs archived terminal-daemon for the
  live proof.** Partial resolution: the mentci *code* path (proof-test under the
  `terminal-cell-runtime` feature) spawns via the external `terminal-cell` crate
  (`TerminalCell::spawn_session`, `harness_liveness.rs:757`); but the prior scout
  observed the *manually run* live proof used the archived `terminal-daemon`. Code
  and hand-proof diverge. Settled intent picks terminal-cell; the implementer must
  confirm terminal-cell's `LaunchCell` reaches a working Claude TUI before trusting
  the proof precedent. Still open.
- **Divergence from the mentci `ARCHITECTURE.md` design-of-record.** That doc's
  "Possible Future Design" (`mentci/ARCHITECTURE.md:110-176`) routes Mentci →
  orchestrate (address only) → a **Mentci-local** terminal-cell driver that owns
  liveness, with **no harness daemon in the loop** and "harness adapters" living in
  Mentci. This task's settled intent relocates launch/liveness/observe/close into
  the **harness daemon** and expands orchestrate from address-only to
  choose/create/reuse/archive. This spec follows the settled intent and therefore
  supersedes that section — but `repo-intent` says only the psyche overrides repo
  direction. The settled-intent constraint set is the authority here; the mentci
  `ARCHITECTURE.md` "Possible Future Design" must be rewritten to match once this
  design is accepted. Flag for the psyche.
- **Three `HarnessKind` enums.** `mentci` `{ClaudeCode, Codex, Pi, OpenEndedHarness}`
  (`harness_sessions.rs:176`), `signal-orchestrate` `{Codex, Claude}`
  (`lib.rs:723`), harness `{Codex, Claude, Pi, Fixture}` (`harness/ARCHITECTURE.md:11`).
  The mentci one dies with the module move. The design must pick which crate owns
  the provider vocabulary the *session record* uses (recommended: reuse
  `signal-orchestrate` `HarnessKind` for the store's `provider` field, since
  orchestrate owns the session record) and reconcile it against harness's config
  `HarnessKind` at the `OpenClaudeSession` boundary. Not yet resolved.
- **No resume-id validity probe** anywhere (Scout §6). §4b routes around it with
  attempt-and-fall-through, but a stale/invalid Claude session id failing resume
  *gracefully* is unproven and must be verified during step 3.
- **Model-knob mapping is semantic, not literal.** The launch plan carries a
  `HarnessSessionModel` semantic knob (`mentci/ARCHITECTURE.md:224-228`); harness
  maps it to `--model <literal>` or `/model <name>` (`harness_adapters.rs:520-527`
  today emits `/model haiku`). Which concrete Claude model literals harness is
  allowed to emit is a harness-side decision not settled here.
- **Did not read**: `private-repos/`, `~/.claude` contents, `/nix/store`; ran no
  tests. `signal-harness` is described as a `router ↔ harness` contract
  (`signal-harness/src/lib.rs:1`); whether "router" there is intended to be
  orchestrate or a separate component is not asserted in source and is worth
  confirming before step 4.
