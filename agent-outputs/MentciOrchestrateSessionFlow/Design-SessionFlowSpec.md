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
is the design-of-record being *revised* here (psyche ACCEPTED the revision; a
separate worker rewrites that doc — see §9).

## 0.5 · Governing lifecycle principle — do not interrupt a working agent

Psyche ruling, and the frame the whole session lifecycle is built on: **a session
is done when it stops, and nothing in this design may interrupt a running one.**
A large or complex flow may legitimately consume a great deal of context and pass
through several compactions before it finishes — that is normal and must not
trigger eviction, archival, or a forced handover. Every consequence of this
principle recurs below: sessions are only ever moved out of the hot set on a
harness-reported *stop* (§4c), staleness is a *soft nudge toward* context handover
rather than a kill (§4b), there is no wall-clock age sweep, and the "many
concurrent sessions" choice (§4a) is precisely what lets long runs coexist without
contending for a single hot slot. Read this as the constraint that any later
implementation lane must not violate.

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

Orchestrate's store needs the recovered Claude session-id, model, **accumulated
context size** (the staleness signal, §4b), and stop lifecycle to make future
reuse/handover/archive decisions. The producer of those facts is harness's JSONL
observer (`harness/src/claude.rs`). Per push-not-pull, harness pushes and
orchestrate subscribes — **reusing harness's landed multi-watch transcript stream**
(`signal-harness/src/lib.rs:661-666`; multi-watcher is safe by design,
Scout-SituationalMap §cross-check). Add one typed observation event to that stream
carrying store-shaped facts (the raw `TranscriptObservation` line is too weak):

```nota
;; New stream event on HarnessTranscriptStream: store-shaped session facts.
(ClaudeSessionObservation <harness> <session-identifier?> <model?>
                          <accumulated-context?> <last-activity> <lifecycle>)
;;   session-identifier? : ClaudeResumeIdentifier   ;; recovered from JSONL (claude.rs:594,1022)
;;   model?              : DetectedModel             ;; recovered (claude.rs:602)
;;   accumulated-context?: ContextTokens             ;; the staleness signal (§4b); Option — see sourcing note below
;;   last-activity       : TimestampNanos            ;; display/ordering ONLY, never gates resume (§4b)
;;   lifecycle           : Ready | Active | Completed | (Exited <exit-status>)
```

Orchestrate subscribes to the harness it just opened (it knows the `HarnessName`
from §2c), receives current-state-on-connect then deltas, and writes
`accumulated_context` / `resume_locator` / `model` / `status` into the session
record (§3). `last_activity` mirrors `Worktree.last_activity`'s
infrastructure-minted discipline (`orchestrate/src/worktree.rs:52-54`, never
agent-supplied) but — unlike the worktree case — is display/ordering metadata only.

**Sourcing the context figure — the harness's own number, never a self-calculation
(blocks §4b until wired).** `accumulated_context` is the context size the Claude
Code harness **already computes for itself**; the workspace harness reads that
authoritative figure and never re-derives it. Summing `message.usage` token fields
out of the JSONL is explicitly rejected: Claude Code documents the transcript
format as internal and version-unstable and warns against parsing it
(`https://code.claude.com/docs/en/sessions.md`), so a hand-rolled total would
silently drift. The JSONL observer (`harness/src/claude.rs`) is therefore left
as-is on this axis — it carries no token field today (grep over
`harness/src/claude.rs`; fixture `harness/tests/claude_artifact_observer.rs:15-18`
models none) and none is added there.

- **Primary — the statusline JSON payload.** Claude Code pipes a structured JSON
  blob to a configured statusline command on stdin, carrying a `context_window`
  object (`used_percentage`, `remaining_percentage`, `total_input_tokens`,
  `context_window_size`, and a `current_usage` token breakdown) plus a top-level
  `exceeds_200k_tokens` boolean (`https://code.claude.com/docs/en/statusline.md`).
  That is exactly the §4b axis — the harness's own token count, and a native
  past-200K flag that maps directly onto the `HandoverDue` threshold — delivered as
  push. Harness supplies a statusline command that forwards the `context_window`
  block into `ClaudeSessionObservation`, rather than reading the transcript.
- **Fallback — inject `/context` and parse it.** If the statusline payload is
  unavailable, harness writes the `/context` slash command into the running Claude
  TUI and parses its output. `/context` is a confirmed command
  (`https://code.claude.com/docs/en/commands.md`) but renders only a visual colored
  grid with no documented structured schema, so this path parses rendered TUI text
  and is strictly the second choice. The injection primitive already exists and
  relocates into harness with the driver (§1, §7 step 3): `TerminalCellSurface::send`
  feeds arbitrary bytes into the live terminal as `InputSource::Programmatic`
  (`mentci/src/harness_liveness.rs:808-817`), so harness writes `/context` + return
  and reads the grid back off the transcript stream it already watches.

The field stays `Option` in the schema above: present once the harness figure is
first observed, absent before the first turn and immediately after `/compact` until
the next call (the statusline `current_usage` is `null` in those windows).
*Implementer-verification items:* confirm the exact nested statusline field
spellings and their stability against the installed Claude Code version (the
payload has grown field-by-field across releases, so treat the names above as
doc-reported, not asserted), and build the wiring by which harness captures the
statusline command's stdout and routes the figure into the observation event
(Claude Code invokes the statusline command; harness provides it).

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
                <resume-locator?> <working-directory> <status>
                <accumulated-context?> <last-activity> <origin-prompt-digest>)
;;   lane                : LaneName            ;; stable lookup key, derived from session intent not provider (mentci/ARCHITECTURE.md:150)
;;   session-handle      : SessionHandle       ;; the token returned to later callers
;;   topic-summary       : PurposeText         ;; reuse Worktree.purpose type; the routing model's one-line topic
;;   provider            : HarnessKind         ;; reuse signal-orchestrate HarnessKind {Codex, Claude} (lib.rs:723)
;;   model               : ModelName           ;; new newtype (absent today outside the fixture workflow)
;;   resume-locator?     : (ClaudeResumeLocator <claude-resume-identifier> <transcript-path>)   ;; Option: present once observed
;;   working-directory   : WirePath            ;; the sandbox jj working copy
;;   status              : HarnessSessionStatus
;;   accumulated-context?: ContextTokens       ;; the staleness signal (§4b); infrastructure-minted from ClaudeSessionObservation; Option until first observed (see §2d sourcing note)
;;   last-activity       : TimestampNanos      ;; DISPLAY/ORDERING ONLY — does not gate resume (§4b); infrastructure-minted, never agent-supplied
;;   origin-prompt-digest: PromptDigest        ;; content hash of the prompt that created it, for audit/dedupe

;; Lifecycle status. Enum, not a bool bundle — mirrors WorktreeStatus (lib.rs:652).
;; Transitions are STOP-driven, never wall-clock (§0.5, §4c).
;;   Hot        : a live terminal-cell process exists in harness right now
;;   Idle       : the agent stopped; no live process, resume-locator makes it resumable
;;   HandoverDue : Idle AND accumulated-context past the handover threshold (§4b) — a soft flag inviting a fresh session, not an eviction
;;   Archived   : Idle/HandoverDue and no longer needed; still resumable-by-id until GC
;;   Recycled   : GC-eligible, resume no longer promised (e.g. a resume attempt failed, §4b)
(HarnessSessionStatus Hot | Idle | HandoverDue | Archived | Recycled)
```

`resume-locator` is `Option<record>` not a bool: the "yes, resumable" answer
carries the id + transcript path a resume needs (`typed-records-over-flags` form 1).
`accumulated-context` (context tokens) — not `last-activity` — is the staleness
axis (§4b): a session that has been quiet for a day but holds only 30K tokens is
fully resumable, while one that just stopped at 210K tokens is `HandoverDue`.
`HandoverDue` is a typed record state, not a boolean flag, so the "yes, past the
threshold" answer keeps the accumulated size and the resume-locator together for
the routing model to act on. The reuse decision that `harness_sessions.rs:535-568`
performs in-memory (match lane, reject on identity/metadata/launch-metadata
mismatch) becomes a store query against this record; the `SessionAddressMetadata`
comparison (`harness_sessions.rs:547`) collapses into matching `HarnessSession`
fields.

Storage discipline (`rust-storage-and-wire`): the record is a schema-owned type in
the `worktrees`-sibling `harness_sessions` table; adding it is a coordinated store
schema-version bump (mirror `orchestrate/src/tables.rs:41-42`, the 2→3 worktree
bump). The `worktrees.nota` GC manifest gets a `harness-sessions.nota` sibling with
a `gc_candidates`-shaped reader returning `Archived | Recycled`
(`orchestrate/src/worktree_projection.rs:32-56`).

## 4 · Policy decisions (psyche-ruled)

All four points are now decided. Each is stated as settled design with a one-line
`decided:` note; the tradeoffs that were weighed are kept only where they still
shape the implementation.

### 4a · Concurrency — many concurrent sessions

`decided:` **Many concurrent Claude sessions. No one-hot slot, no eviction/queue
policy.** Every substrate already supports it: harness config holds
`harnesses: Vec<HarnessInstanceConfiguration>` (`signal-harness/src/lib.rs:922`);
the transcript stream is explicitly multi-watcher (`:567-577`); the reuse registry
keys by lane and already stores many named sessions
(`harness_sessions.rs:465`, `by_lane_name`). This is also what §0.5 requires —
long, compaction-heavy runs must be able to coexist rather than contend for one hot
slot. There is no eviction mechanism to build for V1; a soft cap on `Hot`-status
count remains available as a *later* knob but is explicitly not a V1 gate.

### 4b · Staleness is measured in context size, not wall-clock time

`decided:` **A session's "age" for resume/handover is the context (token) size it
has accumulated, not elapsed time.** The resume/handover decision reads
`HarnessSession.accumulated_context` (§3), never `last_activity`. `last_activity`
is kept purely for display and ordering.

Soft, guidance thresholds (not hard kills, per §0.5):

- **≈100K tokens — long but fully resumable/workable.** The routing model (§5)
  reuses the session normally.
- **≈200K tokens — old; guide toward context handover.** Orchestrate marks the
  record `HandoverDue` and the routing model treats reuse as an *invitation* to
  wrap up and spawn a fresh session rather than resume into an ever-growing
  context. This is a nudge into the workspace's existing **context-handover**
  discipline (`context-handover` skill: a focus-scoped freshness aid carrying only
  settled intent, confirmed facts, recent completed changes, live uncertainties,
  open questions, and agent-output pointers) — it is never a forced action, and a
  `HandoverDue` session stays fully resumable if the psyche or the flow chooses to
  continue it.

Because a working agent is never interrupted (§0.5), the thresholds only ever apply
to a session that has **already stopped** — they change how the *next* prompt for
that topic is routed, not what a live run is allowed to do. A run may pass through
several compactions and cross 200K mid-flight; that is fine, and the `HandoverDue`
flag is only consulted at the next routing decision.

Resume mechanics, unchanged from the reuse path: resumable iff `resume_locator`
present AND transcript file exists (`claude.rs:163,359`), with the resume attempt
itself authoritative. **No resume-id *validity* probe exists anywhere** (Scout §6;
only id *presence*) — so a failed `claude --resume <id>` is a typed outcome that
falls through to `FreshLaunch`, and orchestrate flips the record `Idle → Recycled`
on that failure.

Dependency: this rule fires on live data only once the harness's context figure is
actually wired in — see §2d. That figure is the authoritative number the Claude
Code harness reports via its statusline JSON payload (`context_window` /
`exceeds_200k_tokens`), with `/context` injection+parse as the named fallback; the
workspace harness never self-calculates it from raw usage tokens. Wiring that
surface into `ClaudeSessionObservation` is the one implementation prerequisite for 4b.

### 4c · Archive is stop-driven, never a wall-clock sweep

`decided:` **A session leaves the hot set only on a harness-reported stop; there is
no forced age sweep that could interrupt live work.** Reconciled with §0.5:

1. **On harness `AdapterExited` / `ClaudeSessionObservation … Exited` (the agent
   stopped):** orchestrate moves `Hot → Idle` (process gone, still resumable).
   Push-driven, authoritative — this is the *only* automatic hot-set exit.
2. **Context-size flag (no process change):** an `Idle` session whose
   `accumulated_context` is past the handover threshold (§4b) is marked
   `HandoverDue`. This is a label on an already-stopped session, not an eviction.
3. **`Idle`/`HandoverDue` → `Archived` when done and no longer needed:** via an
   explicit `ArchiveHarnessSession` meta order (a `meta-signal-orchestrate` order
   paralleling `ArchiveWorktree`, `orchestrate/ARCHITECTURE.md:361-364`), which
   reprojects the NOTA manifest. A GC reader returns `Archived | Recycled` for a
   daemon/external agent to reap — the unwired `gc_candidates` shape made concrete
   (`orchestrate/src/worktree_projection.rs:32-56`).

There is deliberately **no `resume_horizon` wall-clock sweep** (an earlier draft
proposed one; it is removed because it could archive or pressure a session that is
simply between turns of a long human-paced task). Following the worktree precedent,
archive is a **meta-signal** order (owner authority), not an ordinary caller op.

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

`decided:` **Rename accepted — `preflight` → session routing (`SessionRouter` /
`RouteSession` / `SessionRoutingPlan`).** The concept name becomes session routing;
"preflight" survives, if anywhere, only as a model-profile label. The actual code
rename (the `PreflightEngine` / `PreflightApi` / `MentciPreflightLaunch` /
`cheap-contained-preflight` identifiers and the `schema/preflight-launch.nota.md`
surface) lands **with the decomposition implementation** — when the engine moves
into orchestrate — not in this design session.

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
     **accumulated context tokens** (the staleness signal, §4b) / stop lifecycle.
     The observer never interrupts the run (§0.5) — it only observes.
8. **Two independent subscribers** consume harness's stream (multi-watch, safe by
   design):
   - **Mentci** opens `WatchHarnessTranscript` on the `harness-name` it got back in
     `PromptRouted` (§2a) and renders live output — Mentci's *display*, no mapping
     logic left in it.
   - **Orchestrate** consumes `ClaudeSessionObservation` and updates the session
     record's `accumulated_context` / `resume_locator` / `model` / `status`. It
     moves `Hot → Idle` only when the agent *stops* (§4c), and marks `HandoverDue`
     when accumulated context crosses the handover threshold (§4b) — both acting on
     an already-stopped session, never on a live one.
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
   into harness; wire the JSONL observer into the daemon **and wire the
   harness-reported context figure from the statusline JSON payload into
   `ClaudeSessionObservation`** (`/context` injection+parse as the fallback; never
   self-calculated from raw usage tokens — the §4b prerequisite, §2d); implement
   `OpenClaudeSession` end-to-end against the
   sandboxed-jj first proof (`mentci/ARCHITECTURE.md:305-309`). Delete Mentci's
   duplicate `ClaudeCodeEventMapper` in favour of the contract `AdapterEvent` family.
4. **Orchestrate routing.** Move the `preflight` engine in (renamed per §5), wire
   `RouteSession` → routing model call → store query (§4b reuse rule) →
   `OpenClaudeSession` push → subscribe to `ClaudeSessionObservation`.
5. **Mentci rewire.** Add `SubmitPrompt` ingress + the `signal-orchestrate`
   dependency + the forward-to-`RouteSession` path; make the client watch the
   returned harness transcript for display. Delete the four now-relocated modules.
6. **Stop-driven archive + GC.** Wire the `Hot → Idle`-on-stop transition, the
   `HandoverDue` context-threshold flag, the `ArchiveHarnessSession` meta order, and
   the `gc_candidates` reaper (§4c) once the store and observation feedback loop are
   live. No wall-clock sweep (§0.5).

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
- **Mentci `ARCHITECTURE.md` design-of-record — RESOLVED (superseded, rewrite
  pending).** That doc's "Possible Future Design" (`mentci/ARCHITECTURE.md:110-176`)
  routes Mentci → orchestrate (address only) → a **Mentci-local** terminal-cell
  driver that owns liveness, with **no harness daemon in the loop** and "harness
  adapters" living in Mentci. The psyche ACCEPTED this spec's direction (harness
  daemon owns launch/liveness/observe/close; orchestrate owns full
  choose/create/reuse/archive), so that section is confirmed stale and authorized
  for rewrite. A separate worker performs the doc rewrite — this lane does **not**
  edit `ARCHITECTURE.md`; it only records that the section is superseded and the
  rewrite is pending.
- **Context size comes from the harness, not a self-calculation (blocks §4b until
  wired).** The staleness axis reads `accumulated_context`, sourced from the Claude
  Code statusline JSON payload's `context_window` block (`used_percentage` /
  `total_input_tokens` / native `exceeds_200k_tokens`), with `/context`
  injection+parse as the fallback (§2d). The workspace harness must **not** sum
  `message.usage` tokens out of the transcript — Claude Code documents that format
  as internal and version-unstable. Named implementer items: confirm the exact
  statusline field spellings and their version-stability against the installed
  Claude Code (doc-reported, not asserted here), and build the wiring that captures
  the statusline command's stdout into `ClaudeSessionObservation`, before the §4b
  100K/200K thresholds can fire on live data.
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
