# Design — Mentci → Orchestrate → Harness → terminal-cell Claude session flow

Design pickup point for a later implementation lane. No production code changes,
no commits. Built directly on `agent-outputs/MentciOrchestrateSessionFlow/Scout-SituationalMap.md`
and the load-bearing source it cites; every claim carries a `repo/path:line`
witness or is marked interpretation. Schemas use nota-schema-docs pseudo-NOTA
(documentation, not the authoritative wire shape).

## Headless reconciliation — supersedes the terminal-cell launch mechanic

**Status:** psyche-locked and demo-proven (mentci commit `7a0c8e44`, see
`HeadlessDemo-Evidence.md` in this directory). This section governs wherever it and
the older body below disagree; the body's terminal-cell mechanics are retained only
as the *optional attach* path.

The psyche validated a headless direction that revises the launch mechanic this spec
was written around. **Claude runs headless as the engine; Mentci is the view; the
harness process and `terminal-cell` beneath it are dumb infrastructure.** A
`terminal-cell` attach is an optional convenience for a human who wants a raw
terminal, no longer the required host. This supersedes the terminal-cell `LaunchCell`
/ `TerminalCellDriver` launch path in §2c and §6 step 6 and the "harness drives
terminal-cell directly" spine step (§7 step 3): those become the *optional attach*
path, while the default engine path is a headless `claude` run whose transcript the
existing `ClaudeArtifactObserver` (`harness/src/claude.rs`) already observes
unchanged (the JSONL/session artifact is identical for headless and attached runs).

**Ephemeral harness, durable resumable session.** The harness need not stay running
once a turn is done; it is free to tear down entirely between turns. The durable
carrier of a session across turns is the **resumable session-id in orchestrate's
session store** (§3 `HarnessSession.resume-locator`), not a live process. This revises
the §4a/§4c `Hot` invariant: `Hot` = a live *turn* is running on a reserved instance;
the moment the turn stops the harness tears down and the record returns to `Idle`,
carrying only its resumable id. A session "between turns" is an `Idle` resumable id,
not a parked process. Continuing a session is **resuming its stored id with the
additional prompt** — a fresh headless run against that id from the session's stable
working directory. For the headless path this replaces the §6 step 9 / §8
"resume (if cold) + `MessageDelivery`" framing: there is no live TUI to deliver a turn
into, so the next turn is itself a resume.

**Self-heal on a lost session.** A guidance/steering prompt may target a session whose
id the engine no longer knows ("no such session"). Handle it by **re-resuming**:
attempt the resume; if the id is truly gone, mint a fresh session, run the prompt into
it, and update the store. This generalizes §4b's resume-fail edge (`→ Recycled`) with
an automatic fresh-mint so the user never sees the loss.

**Session routing is one sub-treatment of a future prompt-treatment meta-phase.** The
§5 rename (`preflight` → session routing) stands, but session routing is now
understood as *one* sub-treatment inside a future **prompt treatment** meta-stage —
alongside intent detection and a summarized feed of each prompt into a long-lived
meta / dialogue session synced across all sessions. That meta-phase and its other
sub-treatments are direction only; do not spec them. Only session routing is designed
here.

**Multiple Mentci windows.** The view must not be designed to foreclose several Mentci
windows (multi-monitor) rendering the same session; multi-window rendering is not
built now.

### Implementation notes (headless invocation)

Confirmed against real `claude` v2.1.198 (headless-demo evidence, same directory):

```
claude -p "<prompt>" [--session-id <uuid> | --resume <id>] --output-format stream-json --verbose
```

`-p/--print` is headless (no TUI); `--output-format stream-json` requires `--print`
and, in practice, `--verbose`, and emits one JSON object per line ending in a
`{"type":"result", ...}` line carrying `session_id` and the assistant text.
`--session-id <uuid>` on a fresh turn lets orchestrate choose and pre-track the id.
Two verified gotchas the implementer must respect:

- **Resume is cwd/project-scoped.** `claude --resume <id>` only finds the session when
  run from the same working directory it was created in; a valid id from another cwd
  yields "No conversation found with session ID: <id>." This is why the session's
  working directory is stored and stable, and why a resume must run there.
- **Session-not-found exits 0.** Resuming an unknown id still exits 0 while emitting a
  `result` line with `"subtype":"error_during_execution"`, `"is_error":true` (and the
  not-found message on stderr). Not-found must be detected from the JSON/stderr, never
  from the exit code — it is the trigger for the self-heal re-resume above.

### Open item — context sourcing under headless (revises §2d / §4b / §9; to be settled by the live-view build)

The context-size staleness mechanism (§2d, §4b) sources its figure **primarily** from
the Claude Code statusline `context_window` JSON payload — which assumed a running
TUI/statusline. Under the proven headless `-p` path the statusline may never be
emitted, while stream-json instead carries a per-message `usage` token breakdown. If
headless emits no statusline, the context figure would have to come from that
stream-json `usage`, which reopens §2d's "never self-calculate; read the harness's own
number" decision (a per-message usage total is closer to a self-sum than to a single
authoritative figure). This is flagged, not resolved: the live-view build settles
whether headless emits a usable statusline and, if not, which stream-json `usage`
figure is authoritative. Do not rewrite the §2d mechanism on the strength of this note.

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
**"Interrupt" has a precise meaning here: forcibly stopping a working agent
mid-work.** It is *not* any injected message. Guidance, query, and steering
messages sent into a session are **not** interrupts and are permitted — including
injecting `/context` to read the accumulated size (§2d) and delivering the ~200K
handover nudge (§4b). Neither forcibly stops the agent; they inform or steer a run
that remains free to keep working. What the principle forbids is a *forced stop* —
eviction, archival, or forced handover — of a run that has not itself stopped.
The rest of the lifecycle model is unchanged under this definition: stop-driven
archival (§4c) and the handover nudge (§4b) were never interrupts.
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
;;   work-surface    : WorkSurface          ;; opaque routing hint the UI forwards verbatim (which surface the user is on); the UI does not compute it
;;   hard-constraints: [LaunchConstraint]   ;; opaque routing hints the UI forwards verbatim (first-proof sandbox requirement); NOT launch/sandbox posture the UI decides

;; New Output variant: acknowledgement carrying the watch address.
(PromptRouted <harness-name> <disposition>)
;;   harness-name: HarnessName             ;; the harness instance hosting the session; the address the client then watches (signal-harness)
;;   disposition : Reused | Created
```

Rationale: the prompt op is genuinely distinct from `QuestionProposal.prompt`
(an approval question presented to the human, `signal-mentci/src/schema/lib.rs:77`).
The reply carries `harness-name` so the client knows which harness transcript to
`WatchHarnessTranscript`, rather than Mentci re-streaming output through its own
wire (that would re-add provider coupling to the UI). Both `work-surface` and
`hard-constraints` are opaque routing hints Mentci forwards unread — no
launch/sandbox posture or provider logic re-enters the UI (O4). `PromptRouted`
is a symmetric pass-through of orchestrate's `SessionRouted` (§2b): under the
one-session-per-harness-instance addressing model (§4a, M1), the `HarnessName`
alone identifies the live session to watch, so no separate session key crosses
the UI boundary.

### 2b · `signal-orchestrate` — Mentci asks orchestrate to route (new, ordinary)

Mentci gains a dependency on `signal-orchestrate` (it has none today,
`mentci/Cargo.toml`). New ordinary operation on the `Orchestrate` channel
(`signal-orchestrate/src/lib.rs:1627-1640`) and a reply on `Reply` (`:1641-1660`),
modeled on the ordinary `RunWorkflow` → `WorkflowRunAccepted` shape.

```nota
;; Ordinary operation: route a prompt to an existing-or-new session.
(RouteSession <prompt-text> <work-surface> <hard-constraints>)

;; Reply: where to watch, and how the session was chosen.
(SessionRouted <harness-name> <disposition>)
;;   harness-name: HarnessName   ;; the harness instance now hosting the session; the address Mentci watches
;;   disposition : Reused | Created
```

`RouteSession` is ordinary because Mentci is an ordinary peer; ordinary peers
cannot compile meta orders (`orchestrate/ARCHITECTURE.md:374-375`). Orchestrate
lowers it internally: run the routing model call (§5), consult the session store
(§3), decide reuse-vs-create, **reserve** a harness instance (§4a) with an atomic
store write that claims the chosen instance conditional on no other `Hot` record
already holding it — **before** the async open — open the session on it (§2c),
confirm-or-release that reservation, write the store, and reply. The reply carries only what Mentci acts
on — the `harness-name` it then watches, and the `disposition` (M2). The internal
fresh-vs-resume launch choice (`FreshLaunch | ResumeExisting`) is daemon lowering
and stays off the wire (contract-repo: replies name the outcome the caller acts
on, not how the daemon lowered the request). The durable session identity
`(lane, session-handle)` is likewise orchestrate-internal store vocabulary (§3),
not a reply field. `SessionRouted` and `PromptRouted` (§2a) are therefore
symmetric `(harness-name, disposition)` pass-throughs. The reply returns fast;
live output does not flow back through it — the client subscribes to harness.

Serialization (S1): the route decision is read-store-snapshot → **slow async
routing model call (§5)** → decide → write, so two concurrent `RouteSession` for
the *same lane* could both observe "no live session for lane L," both decide
`Created`, and split-brain the lane. Orchestrate therefore serializes the route
decision per lane — a per-lane route guard held across the async model call — so
that within one lane the decision is single-threaded and a second concurrent
prompt observes the first's committed record. (This restores the serialization the
in-memory `register_or_reuse`, `harness_sessions.rs:528`, gave for free before the
decision straddled an async boundary.) Distinct lanes route concurrently; the
instance each concurrent route allocates is kept exclusive not by this per-lane
guard but by the atomic instance reservation that precedes the async open (§4a,
V1), so two distinct-lane routes cannot both select and double-book the same free
instance.

### 2c · `signal-harness` — orchestrate opens a Claude session (new)

**Superseded launch mechanic — see the Headless reconciliation section (top).**
`OpenClaudeSession` now means "run Claude headless" as the default engine path; the
terminal-cell `LaunchCell` launch below is retained only as the optional attach path.
The typed `OpenClaudeSession` / `ClaudeLaunchPlan` shape and the reused
`AdapterEvent` reply family are unchanged.

Orchestrate gains a dependency on `signal-harness` and drives harness to open the
session. The scout confirmed harness has **no** dynamic launch/resume/model/close
operation today — instances are fixed at daemon startup
(`signal-harness/src/lib.rs:889-922`). New operation on the `Harness` channel
(`signal-harness/src/lib.rs:629-637`). Under the addressing model (§4a, M1) a
harness instance hosts **exactly one** live session, so the `HarnessName` is the
whole key at this boundary — there is no per-session handle to carry.

```nota
;; New operation: open (fresh or resumed) a Claude session under a named harness.
;; The named instance hosts exactly one live session (§4a); HarnessName is the key.
(OpenClaudeSession <harness> <launch-plan>)
;;   harness    : HarnessName
;;   launch-plan: (ClaudeLaunchPlan <resume> <model> <working-directory>
;;                                  <scaffold-path> <initial-input> <stop-conditions>)
;;     resume          : FreshSession | (ResumeSession <claude-resume-identifier>)
;;     model           : HarnessSessionModel        ;; semantic knob, not a raw model literal
;;     stop-conditions : [StopCondition]            ;; IdleTimeout | TurnCap | CompletionSignal
```

Note (O6): `TurnCap` is inherited verbatim from the existing adapter
(`harness_adapters.rs:147`) and is enshrined as-is, but it sits in tension with
§0.5 — a turn cap can cut off a legitimate long, compaction-heavy flow that §0.5
protects. Flagged for the implementer; not resolved here.

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
;; Keyed by <harness>: one instance hosts one session (§4a), so HarnessName is
;; the per-session key — orchestrate correlates it to the (lane, session-handle)
;; record via the hosting-harness binding it wrote at open time (§3).
(ClaudeSessionObservation <harness> <session-identifier?> <model?>
                          <accumulated-context?> <last-activity> <lifecycle>)
;;   session-identifier? : ClaudeResumeIdentifier   ;; recovered from JSONL (claude.rs:594,1022)
;;   model?              : DetectedModel             ;; recovered (claude.rs:602); see §9 model-vocab note
;;   accumulated-context?: ContextTokens             ;; the staleness signal (§4b); Option — see sourcing note below
;;   last-activity       : TimestampNanos            ;; display/ordering ONLY, never gates resume (§4b)
;;   lifecycle           : Ready | Active | Completed | (Exited <exit-status>)
```

Orchestrate subscribes to the harness it just opened (it knows the `HarnessName`
from §2c), receives current-state-on-connect then deltas, and writes
`accumulated_context` / `resume_locator` / `model` / `status` into the session
record (§3). Correlation is unambiguous under M1: each observation is keyed by
`HarnessName`, and orchestrate recorded that `HarnessName` as the record's
`hosting-harness` (§3) in the reservation transaction that preceded the open (§4a,
V1) — so the binding exists before the first observation and the reverse lookup
(hosting instance → the one Hot record bound to it) resolves to exactly one
record. `last_activity` mirrors `Worktree.last_activity`'s infrastructure-minted
discipline (`orchestrate/src/worktree.rs:52-54`, never agent-supplied) but —
unlike the worktree case — is display/ordering metadata only.

Note (O3): riding `ClaudeSessionObservation` on the existing display
`HarnessTranscriptStream` couples orchestrate's store-feed to the display stream's
evolution and makes orchestrate filter the `AdapterOutput` firehose for its
store-shaped facts. Reusing the landed multi-watch primitive is the push-not-pull
default and is what this design takes; a dedicated observation subscription is the
alternative to weigh if that coupling bites (it also interacts with M1's
per-instance keying). Stated as a tradeoff, not a defect.

**Open under headless — see the Headless reconciliation section (top).** The
statusline-primary sourcing below assumed a running TUI/statusline; headless `-p` may
not emit it, in which case the figure would come from stream-json `usage`. That
question is flagged there and is unresolved; the mechanism below is not rewritten.

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

**The statusline JSON payload is the PRIMARY, authoritative source — and stays
primary always, because it is the only source that reports while the agent is
actively working mid-turn.** Claude Code pipes a structured JSON blob to a
configured statusline command on stdin, carrying a `context_window` object
(`used_percentage`, `remaining_percentage`, `total_input_tokens`,
`context_window_size`, and a `current_usage` token breakdown) plus a top-level
`exceeds_200k_tokens` boolean (`https://code.claude.com/docs/en/statusline.md`).
That is exactly the §4b axis — the harness's own token count, and a native past-200K
flag that maps directly onto the handover threshold (§4b) — delivered as **push** to
a **passive**, structured command. Harness supplies a statusline command that
forwards the `context_window` block into `ClaudeSessionObservation`; it never reads
the transcript and never writes anything back into the session. Claude Code invokes
the statusline command on its own cadence, so obtaining the figure requires no input
into the live TUI — which is exactly why it, and only it, yields a reading *while the
agent is mid-turn*. That mid-turn coverage is why the statusline figure is primary
and remains primary.

**`/context` injection is a legitimate fallback, usable only at rest.** Injecting
`/context` into a session is a *query* message, not an interrupt (§0.5) — it does not
forcibly stop the agent — so it is permitted. But a mid-turn injection does not
produce a clean reading: `/context` renders a usable figure only against a session
that is **at rest (idle)**, between turns, not while the agent is actively working.
The fallback is therefore scoped to at-rest sessions: when the primary statusline
figure is missing for an *idle* session, harness (or orchestrate on its behalf) may
inject `/context` into that at-rest session and parse the command's rendered output
to recover the accumulated size. To state both plainly: the statusline
`context_window` figure is **primary always**; the `/context` injection fallback
yields a usable reading **only at rest**; and an at-rest reading is obtained by
**injecting `/context` and parsing its rendered output**.

Absence / missing-payload handling: `accumulated_context` stays `Option` in the
schema above. It is absent before the first turn and immediately after `/compact`
until the next statusline emission (`current_usage` is `null` in those windows),
and it is absent for a session that has never emitted a statusline figure.
Orchestrate's posture on absence is **last-known-figure, else unknown**: it keeps
the most recent observed figure for that session as `accumulated_context`, and
where none has ever been observed the field is unset and the session is treated as
of *unknown* accumulated size — the handover predicate (§4b) reads unknown as "not
past threshold," i.e. fully reusable, never force-handed-over. No figure is ever
synthesized to fill the gap.

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
                <resume-locator?> <working-directory> <status> <hosting-harness?>
                <accumulated-context?> <last-activity> <origin-prompt-digest>)
;;   lane                : LaneName            ;; stable lookup key, derived from session intent not provider (mentci/ARCHITECTURE.md:150)
;;   session-handle      : SessionHandle       ;; durable session identity within the lane; survives across hosting instances (Idle → resume)
;;   topic-summary       : PurposeText         ;; reuse Worktree.purpose type; the routing model's one-line topic
;;   provider            : HarnessKind         ;; reuse signal-orchestrate HarnessKind {Codex, Claude} (lib.rs:723); see §9 provider-vocab note
;;   model               : ModelName           ;; new newtype (absent today outside the fixture workflow); see §9 model-vocab note
;;   resume-locator?     : (ClaudeResumeLocator <claude-resume-identifier> <transcript-path>)   ;; Option: present once observed
;;   working-directory   : WirePath            ;; the sandbox jj working copy
;;   status              : HarnessSessionStatus
;;   hosting-harness?    : HarnessName         ;; the harness instance hosting this session while Hot (§4a, M1); the key ClaudeSessionObservation correlates on (§2d); None whenever not Hot
;;   accumulated-context?: ContextTokens       ;; the staleness signal (§4b); infrastructure-minted from ClaudeSessionObservation; Option until first observed (see §2d sourcing note)
;;   last-activity       : TimestampNanos      ;; DISPLAY/ORDERING ONLY — does not gate resume (§4b); infrastructure-minted, never agent-supplied
;;   origin-prompt-digest: PromptDigest        ;; content hash of the prompt that created it, for audit/dedupe

;; Lifecycle status. Enum, not a bool bundle — mirrors WorktreeStatus (lib.rs:652).
;; Transitions are STOP-driven, never wall-clock (§0.5, §4c). "Handover-due" is a
;; DERIVED predicate over accumulated-context (§4b, S3), not a stored variant here.
;;   Hot        : a live terminal-cell process exists in harness right now; hosting-harness is set
;;   Idle       : the agent stopped; no live process, resume-locator makes it resumable; hosting-harness cleared
;;   Archived   : Idle and no longer needed; still resumable-by-id until GC
;;   Recycled   : GC-eligible, resume no longer promised (e.g. a resume attempt failed, §4b)
(HarnessSessionStatus Hot | Idle | Archived | Recycled)
```

`resume-locator` is `Option<record>` not a bool: the "yes, resumable" answer
carries the id + transcript path a resume needs (`typed-records-over-flags` form 1).
`accumulated-context` (context tokens) — not `last-activity` — is the staleness
axis (§4b): a session that has been quiet for a day but holds only 30K tokens is
fully resumable, while one that just stopped at 210K tokens is *handover-due*.
"Handover-due" is **derived, not stored** (S3): it is fully computable as
`accumulated-context past the threshold AND status == Idle` and carries no data the
record does not already hold, so it is the inverse of the typed-records trigger —
replace a flag with a record only when the yes-branch carries new data, and this
one carries none. Storing it as a fifth status variant would create a sync
obligation and could silently disagree with the field after a `/compact` drops
context back below the threshold. The routing model therefore computes handover-due
from `accumulated-context` at the routing decision (§4b), reading the accumulated
size and the resume-locator straight off the record. The reuse decision that
`harness_sessions.rs:535-568` performs in-memory (match lane, reject on
identity/metadata/launch-metadata mismatch) becomes a store query against this
record; the `SessionAddressMetadata` comparison (`harness_sessions.rs:547`)
collapses into matching `HarnessSession` fields.

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

### 4a · Concurrency — many concurrent sessions, one per harness instance

`decided:` **Many concurrent Claude sessions, realized as many harness instances,
each hosting exactly one live session. No one-hot slot, no eviction/queue policy,
and no session-multiplexing inside a single instance (M1).** The addressing model
is one session per harness instance: an instance is fixed at daemon startup
(`harnesses: Vec<HarnessInstanceConfiguration>`, `signal-harness/src/lib.rs:922`),
carries one `harness_kind` and one terminal endpoint, and its transcript stream
binds to a single `HarnessName` (`daemon.rs` `bound_harness`). So `HarnessName` is
the whole live-session key, and `OpenClaudeSession`, `ClaudeSessionObservation`,
`WatchHarnessTranscript`, and the `SessionRouted`/`PromptRouted` replies all key on
it (§2). Multi-watcher (`:567-577`) means many observers of **one** instance's
stream — Mentci's display and orchestrate's observation feed watching the same
session — not many sessions on one stream. (The earlier "every substrate already
supports many concurrent sessions" grounding conflated "many fixed startup
instances" and "many watchers" with "many dynamically addressable sessions on one
instance"; the last is net-new substrate and is explicitly not built here.)

The durable session identity is `(lane, session-handle)` in the store (§3), which
outlives any one hosting instance (a session goes `Idle`, then resumes on whatever
instance is free); the live `HarnessName` is the transient hosting address, and
orchestrate maps between them via the record's `hosting-harness` binding (§3).

Concurrency is bounded by the pool of configured instances, which is exactly what
§0.5 requires: long, compaction-heavy runs coexist by occupying distinct instances
rather than contending for one hot slot. **Allocation (transactional reservation
before the async open, V1).** orchestrate tracks which instances are currently
`Hot` (each `Hot` record carries its `hosting-harness`, §3); to open a new or
resumed session it selects a non-`Hot` instance and **reserves it atomically in a
single store transaction — conditional on no other `Hot` record already holding
that `HarnessName` — before** issuing the async `OpenClaudeSession` (§2c). The
reservation binds the record's `hosting-harness` to the chosen instance and flips
it `→ Hot` in that one transaction; the conditional write fails if a concurrent
route already claimed the instance, and the router then retries against another
free instance. This closes the cross-lane double-book: two concurrent routes for
distinct lanes cannot both select the same last-free instance, because the first
commit makes the instance appear taken to the second (the per-lane route guard of
§2b/S1 does not cover this, since the contending routes are on distinct lanes).
Only after the reservation commits does orchestrate issue the async open; a
successful open confirms the reservation, and a failed open releases it (§4c step
4, resume-fail `→ Recycled`; a fresh-launch failure frees the reserved instance).
This is exactly the transactional reservation §4c step 3 specifies for the
Archived-resume-vs-GC case, generalized to every fresh and `Idle`-resume
allocation. A resumed session need not return to the instance it last ran on — it
binds to whichever free instance is reserved, via `ResumeSession <id>`. If every
instance is `Hot`, that
is a capacity limit of the configured pool; a soft cap on concurrent `Hot` sessions
is a natural later knob but is not a V1 gate. There is no eviction mechanism to
build for V1.

### 4b · Staleness is measured in context size, not wall-clock time

`decided:` **A session's "age" for resume/handover is the context (token) size it
has accumulated, not elapsed time.** The resume/handover decision reads
`HarnessSession.accumulated_context` (§3), never `last_activity`. `last_activity`
is kept purely for display and ordering.

Soft, guidance thresholds (not hard kills, per §0.5):

- **≈100K tokens — long but fully resumable/workable.** The routing model (§5)
  reuses the session normally.
- **≈200K tokens — old; guide toward context handover.** At the routing decision
  the routing model derives *handover-due* from the record's `accumulated-context`
  (S3 — no stored status; §3) and treats reuse as an *invitation* to wrap up and
  spawn a fresh session rather than resume into an ever-growing context. This is a
  nudge into the workspace's existing **context-handover** discipline
  (`context-handover` skill: a focus-scoped freshness aid carrying only settled
  intent, confirmed facts, recent completed changes, live uncertainties, open
  questions, and agent-output pointers) — it is never a forced action, and a
  handover-due session stays fully resumable if the psyche or the flow chooses to
  continue it. Because the predicate is recomputed each routing decision, a
  post-`/compact` session whose context dropped back below the threshold is simply
  no longer handover-due — nothing to unset.

Because a working agent is never interrupted (§0.5), the thresholds only ever apply
to a session that has **already stopped** — they change how the *next* prompt for
that topic is routed, not what a live run is allowed to do. A run may pass through
several compactions and cross 200K mid-flight; that is fine, and the handover-due
predicate is evaluated only at the next routing decision.

Resume mechanics, unchanged from the reuse path: resumable iff `resume_locator`
present AND transcript file exists (`claude.rs:163,359`), with the resume attempt
itself authoritative. **No resume-id *validity* probe exists anywhere** (Scout §6;
only id *presence*) — so a failed `claude --resume <id>` is a typed outcome that
falls through to `FreshLaunch`, and orchestrate flips the record to `Recycled` from
whatever resumable state it was resumed out of (`Idle` or `Archived`; §4c, S2) on
that failure.

Dependency: this rule fires on live data only once the harness's context figure is
actually wired in — see §2d. That figure's **primary** source is the authoritative
number the Claude Code harness reports via its statusline JSON payload
(`context_window` / `exceeds_200k_tokens`), delivered passively to a statusline
command — the only source that reports mid-turn — with `/context` injection as an
**at-rest-only** fallback (§2d, M3); the workspace harness never self-calculates it
from raw usage tokens. Wiring that surface into `ClaudeSessionObservation` is the
one implementation prerequisite for 4b.

### 4c · Archive is stop-driven, never a wall-clock sweep

`decided:` **A session leaves the hot set only on a harness-reported stop; there is
no forced age sweep that could interrupt live work.** The full transition set,
reconciled with §0.5:

*De-escalation (the only automatic hot-set exit):*

1. **On harness `AdapterExited` / `ClaudeSessionObservation … Exited` (the agent
   stopped):** orchestrate moves `Hot → Idle` and clears `hosting-harness` (process
   gone, still resumable). Push-driven and authoritative.

*Reactivation — back into `Hot` (S2):*

2. **Reservation before the async open, confirmed on success (V1):** the record is
   set `→ Hot` with its `hosting-harness` bound to the chosen instance **in the
   atomic reservation transaction that precedes** the async `OpenClaudeSession`
   (§4a), not after it — the reservation is conditional on no other `Hot` record
   already holding that `HarnessName`, which is what stops two distinct-lane routes
   double-booking one instance. A successful `OpenClaudeSession` (fresh or resume)
   confirms that reservation; a failed one releases it (step 4). This holds for a
   newly `Created` session **and** for any resumed `Idle` or `Archived` session —
   the reservation restores the `Hot` invariant that a live process exists (or is
   being opened under an exclusive claim) now. Without this reservation an
   implementer following only step 1 would leave a resumed session marked
   `Idle`/`Archived` while a live process exists, and concurrent distinct-lane
   routes could double-book the last free instance.
3. **Un-archive vs GC ordering:** resuming out of `Archived` flips `Archived → Hot`
   in the **same store transaction** that reserves the instance, so the
   `gc_candidates` reaper (which returns `Archived | Recycled`) cannot reap a
   session mid-resume; equivalently, the reaper claims a candidate record and skips
   any that is no longer `Archived`/`Recycled` when it goes to reap. One of the two
   orderings must hold; either removes the resume/GC race.
4. **Resume-fail from any resumable state:** a failed `claude --resume <id>` out of
   `Idle` or `Archived` flips the record `→ Recycled` (generalizing §4b's
   `Idle → Recycled`; resume is attempted from either resumable state).

*Archive / GC:*

5. **`Idle` → `Archived` when done and no longer needed:** via an explicit
   `ArchiveHarnessSession` meta order (a `meta-signal-orchestrate` order paralleling
   `ArchiveWorktree`, `orchestrate/ARCHITECTURE.md:361-364`), which reprojects the
   NOTA manifest. A GC reader returns `Archived | Recycled` for a daemon/external
   agent to reap — the unwired `gc_candidates` shape made concrete
   (`orchestrate/src/worktree_projection.rs:32-56`).

Handover-due is deliberately **not** a transition here: it is a predicate derived
from `accumulated-context` at the routing decision (§4b, S3), so an already-stopped
`Idle` session past the threshold needs no status write — nothing marks or unmarks
it, and a later `/compact` that drops it back below threshold needs no correction.

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
   (the relocated `register_or_reuse` logic, `harness_sessions.rs:528`) and derive
   the handover-due predicate from `accumulated_context` (§4b, S3) → decide `Reused`
   (with `resume_locator`) or `Created`. The decision is serialized per lane across
   the async model call (§2b, S1) so concurrent prompts for one lane cannot
   split-brain it. It writes/updates the `HarnessSession` record.
5. Orchestrate **reserves** a free harness instance (§4a) — an atomic store write
   that flips the record `→ Hot` and binds that instance as `hosting-harness`,
   conditional on no other `Hot` record already holding it — **then** pushes
   `OpenClaudeSession` (§2c) to it over `signal-harness` with a `FreshSession` or
   `ResumeSession <id>` launch plan. A successful open confirms the reservation; a
   failed open releases it (§3, §4c steps 2 and 4). Reserving before the async open
   is what keeps two concurrent distinct-lane routes from double-booking the same
   last-free instance (V1).
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
   - **Orchestrate** consumes `ClaudeSessionObservation`, correlates it to the
     record via `hosting-harness` (§2d, M1), and updates `accumulated_context` /
     `resume_locator` / `model` / `status`. It moves `Hot → Idle` (and clears
     `hosting-harness`) only when the agent *stops* (§4c) — never on a live session.
     There is no `HandoverDue` write: handover-due is derived from
     `accumulated_context` at the next routing decision (§4b, S3).
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
   `ArchiveHarnessSession` order (owner authority, parallels `ArchiveWorktreeOrder`).
   Session *creation* is **not** a wire op: it is an internal SEMA transition driven
   by `RouteSession` lowering (§2b), so there is no `RegisterHarnessSession` public
   or meta order (contract-repo: do not mirror internal helper steps as public
   operations — O2).
3. **Harness → terminal-cell launch (the hard new capability).** Add the
   terminal-cell dependency to harness; move `ClaudeCodeAdapter` +
   `TerminalCellDriver`/liveness from `mentci/src/harness_{adapters,liveness}.rs`
   into harness; wire the JSONL observer into the daemon **and wire the
   harness-reported context figure from the passive statusline JSON payload into
   `ClaudeSessionObservation`** (statusline primary; `/context` injection is an
   at-rest-only fallback — M3, §2d; never self-calculated from raw usage tokens —
   the §4b prerequisite); implement `OpenClaudeSession` end-to-end against the
   sandboxed-jj first proof (`mentci/ARCHITECTURE.md:305-309`). Delete Mentci's
   duplicate `ClaudeCodeEventMapper` in favour of the contract `AdapterEvent` family.
4. **Orchestrate routing.** Move the `preflight` engine in (renamed per §5), wire
   `RouteSession` → routing model call → store query (§4b reuse rule) →
   `OpenClaudeSession` push → subscribe to `ClaudeSessionObservation`.
5. **Mentci rewire.** Add `SubmitPrompt` ingress + the `signal-orchestrate`
   dependency + the forward-to-`RouteSession` path; make the client watch the
   returned harness transcript for display. Delete the four now-relocated modules.
6. **Stop-driven archive + GC.** Wire the `Hot → Idle`-on-stop transition, the
   reactivation edges (`→ Hot` on open/resume, un-archive-before-GC ordering,
   resume-fail `→ Recycled`; §4c, S2), the `ArchiveHarnessSession` meta order, and
   the `gc_candidates` reaper (§4c) once the store and observation feedback loop are
   live. Handover-due stays a derived predicate at routing time — nothing to wire as
   a stored flag (§4b, S3). No wall-clock sweep (§0.5).

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
- **Mentci `ARCHITECTURE.md` design-of-record — RESOLVED (rewritten).** The old
  "Mentci-local terminal-cell driver, no harness daemon" framing was already replaced
  on mentci `main` (47bf0af2) by the three-region split (Mentci / orchestrate /
  harness) this spec assumes. That doc has now been **further reconciled to the
  headless direction** (Claude headless engine, Mentci as view, harness + terminal-cell
  as dumb infra, ephemeral harness + durable resumable session-id, self-heal) on
  branch `arch-headless-reconcile` (commit `5d9be739`, pushed; disposition tracked by
  bead `primary-ycda`, full-merge to main pending a rebase over the active live-view
  code branch). No longer an open unknown.
- **Context size comes from the harness, not a self-calculation (blocks §4b until
  wired) — AND now open on headless.** The staleness axis reads `accumulated_context`,
  sourced **primarily** from the Claude Code statusline JSON payload's `context_window`
  block (`used_percentage` / `total_input_tokens` / native `exceeds_200k_tokens`),
  delivered passively — the only source that reports mid-turn — with `/context`
  injection as an at-rest-only fallback (§2d, M3). The workspace harness must **not**
  sum `message.usage` tokens out of the transcript — Claude Code documents that
  format as internal and version-unstable. **New open item under headless** (see the
  Headless reconciliation section, top): headless `claude -p` may emit no statusline
  at all, in which case the figure would have to come from stream-json `usage` —
  reopening the never-self-calculate decision. To be settled by the live-view build.
  Named implementer items: confirm the exact statusline field spellings and their
  version-stability against the installed Claude Code (doc-reported, not asserted
  here), and — once the headless statusline question is settled — build the wiring
  that routes the chosen figure into `ClaudeSessionObservation`, before the §4b
  100K/200K thresholds can fire on live data.
- **Provider and model vocabulary — three `HarnessKind` enums, one model value with
  three type names, and a provider-named resume locator (O1, one decision).**
  `HarnessKind`: `mentci` `{ClaudeCode, Codex, Pi, OpenEndedHarness}`
  (`harness_sessions.rs:176`), `signal-orchestrate` `{Codex, Claude}`
  (`lib.rs:723`), harness `{Codex, Claude, Pi, Fixture}` (`harness/ARCHITECTURE.md:11`).
  The mentci one dies with the module move; the design must pick which crate owns
  the provider vocabulary the *session record* uses (recommended: reuse
  `signal-orchestrate` `HarnessKind` for the store's `provider` field, since
  orchestrate owns the session record) and reconcile it against harness's config
  `HarnessKind` at the `OpenClaudeSession` boundary. **Fold two more vocab choices
  into this same decision:** (a) the model value wears three type names across its
  lifecycle — `HarnessSessionModel` (launch knob, §2c), `DetectedModel` (observed,
  §2d), `ModelName` (stored, §3) — which is one value; collapse it to a single
  model type with one owner, keeping only the genuine semantic-knob-vs-literal
  distinction (the model-knob item below); and (b) `ClaudeResumeLocator` is a
  Claude-named record living inside a provider-neutral session record whose
  `provider` is `HarnessKind` — make it provider-neutral or a per-provider variant.
  Not yet resolved.
- **No resume-id validity probe** anywhere (Scout §6). §4b routes around it with
  attempt-and-fall-through. This is now **demo-proven** (mentci commit `7a0c8e44`):
  resuming a poisoned/unknown id is detected from the JSON `result` line and stderr
  (the process still exits 0), and self-heal mints a fresh session and re-runs the
  prompt. Remaining verification is only that the same graceful fall-through holds for
  a genuinely *expired* (not merely wrong-cwd) id in the wired implementation.
- **Model-knob mapping is semantic, not literal.** The launch plan carries a
  `HarnessSessionModel` semantic knob (`mentci/ARCHITECTURE.md:224-228`); harness
  maps it to `--model <literal>` or `/model <name>` (`harness_adapters.rs:520-527`
  today emits `/model haiku`). Which concrete Claude model literals harness is
  allowed to emit is a harness-side decision not settled here.
- **Harness peer naming — make it explicit (O5).** `signal-harness` documents its
  peer as `router ↔ harness` (`signal-harness/src/lib.rs:1`). After this design
  harness has (at least) two ordinary peers: **orchestrate** (opens sessions via
  `OpenClaudeSession`, §2c) and the deferred **message-router** (delivers turns via
  `MessageDelivery`, §8). The doc rewriter must state harness's peers explicitly and
  decide whether the contract's own "router" prose needs updating — leaving it
  implicit invites the reader to think a single "router" owns both roles.
- **Did not read**: `private-repos/`, `~/.claude` contents, `/nix/store`; ran no
  tests.
