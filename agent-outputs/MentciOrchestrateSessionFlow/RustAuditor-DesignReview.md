# Rust Auditor — Design Review of the Mentci→Orchestrate→Harness Session-Flow Spec

## Scope

Adversarial design-spec audit (no code or spec changed, no commits) of
`agent-outputs/MentciOrchestrateSessionFlow/Design-SessionFlowSpec.md`, judged for
coherence and safety-to-enshrine as the mentci-family design-of-record before a
separate worker rewrites `ARCHITECTURE.md`. Judged against the settled fixed
intent (Mentci = UI ingress/egress only; Orchestrate owns choose/create/reuse/
archive; Harness owns Claude launch/observe/close via terminal-cell; never
interrupt a working agent; staleness measured in context size) and against
workspace doctrine: component-architecture, contract-repo, push-not-pull,
typed-records-over-flags, rust-storage-and-wire, design-quality, repo-intent.

## Evidence consulted

Design spec and Scout situational map (both in this lane). Source verified by
direct read/grep at `/git/github.com/LiGoldragon/`:

- Confirmed the spec's central premise: `mentci/src/{daemon,state}.rs` contain
  zero references to `preflight` / `harness_sessions` / `harness_adapters` /
  `harness_liveness` (grep empty). The four modules are library/test-only.
- Confirmed `mentci/Cargo.toml` has no `signal-orchestrate` dep; `terminal-cell`
  is optional feature-gated.
- Confirmed `signal-harness` `AdapterEvent` family (`lib.rs:647-654`),
  `MessageDelivery` (`:144`), `WatchHarnessTranscript … opens HarnessTranscriptStream`
  (`:635`), fixed startup `harnesses: Vec<HarnessInstanceConfiguration>` (`:922`),
  and that the crate documents its peer as **`router` ↔ `harness`** (`lib.rs:1,17`).
- Confirmed mentci's `ClaudeCodeEventMapper` already emits
  `signal_harness::HarnessEvent::Adapter*` (`harness_adapters.rs:5,188-317`) — the
  spec's "output type is already the contract, delete the duplicate shape" holds.
- Confirmed `harness/src`: no live `Command::new("claude")` / `--resume` / `--model`
  (only `pi.rs`); `harness/src/daemon.rs` does not reference the `claude` observer.
- Confirmed the `Worktree` template: `signal-orchestrate` `Worktree` (`:690`),
  `WorktreeStatus {Active,Merged,Archived,Recycled}` (`:652`), `HarnessKind {Codex,Claude}`
  (`:723`), `orchestrate/src/tables.rs` schema version 3 + `StoredWorktree`,
  `worktree.rs` infrastructure-minted `last_activity`, `worktree_projection.rs`
  `gc_candidates → Archived|Recycled`. Meta orders live in `meta-signal-orchestrate`
  (`RegisterWorktree`, `ArchiveWorktreeOrder`), not `signal-orchestrate`.
- Confirmed `terminal-cell` `LaunchCell` is a generic PTY launcher and `SendLine`
  routes to `send_programmatic_input` (`lifecycle_cli.rs`, `client.rs:77`).

No Rust checks were run: no code changed and none were named by an implementer.
The verification above is source inspection, the appropriate evidence for a
design-spec audit.

Bottom line: the spec's factual ground truth is accurate — every load-bearing
witness I spot-checked holds, and the core direction (three clean ownership
regions, push throughout, store mirrors `Worktree`, context-size staleness,
stop-driven archival) is sound and worth preserving. The defects below are
targeted gaps in the *addressing model*, one *contract reply shape*, one
*fixed-intent contradiction* in a fallback, and several state-machine and
concurrency edges — not a wrong overall shape.

## Must-fix before enshrining

### M1 — Harness-instance ↔ session cardinality and addressing is unresolved, and the contract shapes contradict each other

Spec locations: §2c `OpenClaudeSession <harness> <session-handle> <launch-plan>`;
§2d `ClaudeSessionObservation <harness> <session-identifier?> …` (no session-handle);
§2a Mentci watches via `WatchHarnessTranscript` on `harness-name`; §4a "many
concurrent sessions"; §6 step 8.

The design simultaneously assumes two incompatible cardinalities:

- `OpenClaudeSession` is keyed by **(harness, session-handle)** — implying a
  harness instance can host **many** sessions distinguished by handle.
- `ClaudeSessionObservation`, `WatchHarnessTranscript`, and the transcript stream
  are keyed by **harness-name alone** — implying **one** session per harness.

Ground truth (`signal-harness/src/lib.rs:889-922`, `daemon.rs` `bound_harness`):
today a `HarnessInstanceConfiguration` is one named instance with one
`harness_kind` and one terminal endpoint, and the transcript stream binds to a
single `HarnessName`. So the substrate is **one live session per instance, keyed
by harness-name**, and "multi-watcher" means many observers of one stream — **not**
many sessions on one stream. §4a's claim that "every substrate already supports"
many concurrent sessions conflates "many fixed startup instances"
(`Vec<HarnessInstanceConfiguration>`) and "many watchers" with "many dynamically
addressable sessions," which is a different capability that no cited substrate
provides.

Concrete failures this causes once more than one session is live:

1. **Orchestrate cannot correlate an observation to the right record.** Orchestrate
   opens with (harness, session-handle) but the Claude session-id is only recovered
   later from JSONL (§2d). `ClaudeSessionObservation` returns (harness,
   session-identifier) and never echoes the orchestrate-supplied `session-handle`.
   With more than one session per harness there is no key shared between what
   orchestrate knows at open-time and what the observation carries — so the
   store-update loop that all of §4b/§4c/§6-step-8 depend on cannot find the record
   to write `accumulated_context` / `status` into.
2. **Mentci cannot watch a specific session.** If a harness hosts several sessions,
   watching by `harness-name` yields an interleaved stream; Mentci has no
   per-session filter to render "its" session.
3. **"Many concurrent" has no allocation model.** Instances are fixed at startup and
   `OpenClaudeSession` cannot create one; if each instance hosts one session, the
   spec never says how orchestrate obtains a free instance for the Nth session, nor
   which instance a resumed/reused session binds to.

Correction: pick one model and make every wire consistent with it.
Either (A) one session per instance — then key everything by `HarnessName`, drop
`session-handle` from `OpenClaudeSession`, and design how orchestrate allocates/
addresses instances for concurrency and resume; or (B) many sessions per instance
— then `ClaudeSessionObservation`, `WatchHarnessTranscript`, and the transcript
subscription must all carry the `session-handle` (harness-minted or the
orchestrate handle echoed back) as the per-session key. This is the spine the doc
rewriter must nail; the current mixed model would enshrine a broken addressing
scheme.

### M2 — `SessionRouted` reply omits the address Mentci must watch and instead exposes an internal lowering detail

Spec locations: §2b `SessionRouted <session-address> <disposition> <launch-directive>`
vs §2a `PromptRouted <session-address> <disposition> <harness-name>`.

Mentci's reply to its client (`PromptRouted`) must carry `harness-name` — "the
harness the client then watches." Mentci's only source for that is orchestrate's
`SessionRouted` reply. But `SessionRouted` returns `launch-directive`
(`FreshLaunch | ResumeExisting`) and **not** the harness/session address. Two
problems compound:

- **Missing field:** Mentci cannot populate `PromptRouted.harness-name`. The
  `session-address` `(lane, session-handle)` is orchestrate vocabulary and does not
  resolve to a `HarnessName` on the Mentci side (orchestrate alone knows which
  harness it opened on, from §2c). The end-to-end watch flow is broken as written.
- **Leaked lowering:** `launch-directive` is "what orchestrate then tells harness"
  — a pure daemon-lowering detail. contract-repo: "Public operations name what the
  peer asks for, not how the daemon lowers the request internally … Lowering is
  daemon logic." Mentci never acts on FreshLaunch-vs-Resume, so it does not belong
  in the Mentci-facing reply.

Correction: `SessionRouted` should carry what Mentci acts on — the watch address
(harness-name, and session-handle if M1 resolves to model B) plus `disposition` —
and drop `launch-directive`. This also makes `SessionRouted` and `PromptRouted`
symmetric pass-throughs (the design-quality shape the spec is otherwise reaching
for). This finding is partly a corollary of M1: once addressing is fixed, the
reply must carry that address.

### M3 — The `/context` fallback for context sourcing contradicts the fixed "never interrupt a working agent" principle

Spec locations: §2d "Fallback — inject `/context` and parse it"; §4b/§9 restate it;
governing principle §0.5.

The fallback writes `/context` + return into the running Claude TUI via
`TerminalCellSurface::send` (`InputSource::Programmatic`) and parses the rendered
grid. But:

- If the session is **Hot** (a live TUI exists to inject into), writing input into
  it **is** interrupting a working agent — exactly what §0.5 forbids as fixed
  intent, and it risks the `/context` output being consumed as a turn or disrupting
  the agent mid-flow.
- If the session is **Idle** (stopped), there is **no** live TUI to inject into, so
  the fallback is inapplicable.

So the named fallback is either forbidden or a no-op; it cannot run without
violating the governing principle. The **primary** path (the statusline JSON
`context_window` payload, which Claude Code pushes to a passive statusline command)
is sound and does not have this problem — it never injects. Enshrining a fallback
that contradicts fixed settled intent is the issue.

Correction: remove the `/context` injection fallback, or restrict it to an
explicitly non-interrupting mechanism, and state that context sourcing is the
passive statusline payload only. If a fallback is genuinely needed, it must come
from a non-injecting source (e.g. a JSONL-adjacent figure the harness can read
passively), not from typing into a live agent. At minimum the spec must reconcile
this with §0.5 rather than list it as a routine second choice.

## Should-fix (strong, not blocking enshrinement)

### S1 — The reuse decision has a per-lane time-of-check/time-of-use race across the async routing model call

Spec locations: §2b lowering ("run the routing model call, consult the store,
decide, write"); §6 steps 3-4; §4a many concurrent.

Routing is read-store-snapshot → **slow async model call (§5)** → decide → write.
Two concurrent `RouteSession` for the same lane can both observe "no live session
for lane L," both decide `Created`, and both write — yielding duplicate sessions
for one logical lane, or a clobbering upsert (identity is `(lane, session-handle)`;
lane is the "stable lookup key"). The in-memory `register_or_reuse`
(`harness_sessions.rs:528`) presumably serialized this; relocating it across an
async model call widens the window and the spec never specifies a serialization
point. Failure: double-submit or two watchers produce split-brain sessions for one
topic. Correction: serialize the route decision per lane (or make creation an
identity-keyed upsert that dedupes), and state it.

### S2 — The status machine defines only de-escalation; the re-activation transitions are undefined

Spec locations: §4c (enumerates Hot→Idle, Idle→HandoverDue, Idle/HandoverDue→
Archived, resume-fail Idle→Recycled); §3 ("Archived … still resumable-by-id until
GC"); §4b resume path; §6 step 5.

Resume is a core flow, yet no transition writes a resumed session **back to Hot**.
An implementer following §4c literally leaves a resumed session marked
Idle/HandoverDue/Archived while a live process exists — contradicting the Hot
definition ("a live terminal-cell process exists right now"). Also undefined:
Archived→Hot on resume-from-archive and its **race with GC** (the `gc_candidates`
reaper returns `Archived|Recycled`; a session being resumed out of Archived could
be reaped concurrently), and resume-fail from a non-Idle state (§4b only names
Idle→Recycled). Correction: specify the reactivation edges (→Hot on successful
open/resume for Idle/HandoverDue/Archived), the un-archive-vs-GC ordering, and
resume-fail from every resumable state.

### S3 — `HandoverDue` is a derived predicate stored as an authoritative status

Spec locations: §3 status enum; §4b ("consulted at the next routing decision");
§4c step 2 ("an Idle session whose accumulated_context is past the threshold is
marked HandoverDue").

`HandoverDue` is fully computable from `accumulated_context` (already a record
field) plus `Idle`. Unlike the `Worktree` template's `Archived`/`Recycled` — which
are authoritative states set by explicit orders and are **not** derivable from
another field — `HandoverDue` carries no new data, so it is the inverse of the
typed-records-over-flags trigger ("replace a flag only when the yes-branch carries
data"). Storing it creates a sync obligation: §4c step 2 must rewrite the status on
every threshold-crossing observation, and post-`/compact` context can drop back
below the threshold (§2d), so the stored flag can silently disagree with the field.
And §4b itself says the threshold is "consulted at the next routing decision" —
which argues for **deriving** it at routing time, not storing it. Correction: keep
`HarnessSessionStatus = Hot | Idle | Archived | Recycled` and compute
"handover due" from `accumulated_context` at the routing decision; or, if it must
be stored, name the single writer and the invariant that keeps it consistent with
the field.

## Optional / lower (design-quality and clarity)

- **O1 — One concept, three types for the model value; provider vocab leaking into
  the neutral record.** §3 stores `model: ModelName`, §2c's launch plan carries
  `HarnessSessionModel` (semantic knob), §2d's observation carries
  `DetectedModel`. That is one value wearing three type names across its lifecycle
  (design-quality: symmetry). Separately, §3 puts a Claude-named
  `ClaudeResumeLocator` inside a provider-neutral session record whose `provider`
  is `HarnessKind`. The spec already flags the three-`HarnessKind` reconciliation
  as open (§9); fold the model-type and resume-locator vocabulary into the same
  decision — one owner for provider vocab, one for model vocab, and a
  provider-neutral (or per-provider-variant) resume locator.

- **O2 — `RegisterHarnessSession` as a meta order conflates internal creation with
  external seeding.** §7 step 2 lists `RegisterHarnessSession` alongside
  `ArchiveHarnessSession` as meta-signal orders paralleling the worktree pair. But
  `RegisterWorktree` is meta because an external owner seeds worktrees; a harness
  session is created by orchestrate's **own** ordinary `RouteSession` lowering, so
  its creation is an internal SEMA transition, not an external order (contract-repo:
  "do not mirror internal helper steps as public operations"). `ArchiveHarnessSession`
  as a meta order is well-founded (owner authority, parallels `ArchiveWorktreeOrder`).
  Reconsider whether the register order should exist as a wire op at all.

- **O3 — Orchestrate consumes the display transcript firehose to get store facts.**
  §2d rides `ClaudeSessionObservation` on the existing `HarnessTranscriptStream`, so
  orchestrate receives all `AdapterOutput` deltas it must filter, and its store-feed
  is coupled to the display stream's evolution. Reuse of the landed primitive is
  defensible (push-not-pull "use the existing subscription"); but consider a
  dedicated observation subscription, which also interacts with M1's per-session
  keying. Note this well: it is a tradeoff to state, not an error.

- **O4 — `SubmitPrompt` carrying `work-surface` + `hard-constraints` at the UI
  boundary.** §2a. `work-surface` is a legitimate UI fact (which surface the user is
  on); `hard-constraints` ("first-proof sandbox requirement") is more debatable at
  the UI. Confirm both are opaque pass-through routing hints the UI forwards, not
  values the UI computes — otherwise launch/sandbox posture re-enters Mentci, against
  the "no provider/operation logic" boundary.

- **O5 — `router ↔ harness` peer naming.** The spec (§9) flags that
  `signal-harness` documents its peer as "router." After this design, harness has
  (at least) two ordinary peers: orchestrate (opens sessions via `OpenClaudeSession`)
  and the deferred message-router (delivers turns via `MessageDelivery`). The doc
  rewriter must state harness's peers explicitly and decide whether the contract's
  own "router" prose needs updating; leaving it implicit invites the reader to think
  a single "router" owns both.

- **O6 — `TurnCap` stop-condition vs §0.5.** §2c stop-conditions include `TurnCap`;
  §0.5 says a long flow "may pass through several compactions before it finishes" and
  must not be force-handed-over. A turn cap can cut off a legitimate long flow. This
  is inherited from the existing adapter (`harness_adapters.rs:147`), so it is
  pre-existing, but the spec should note the tension when it enshrines stop-conditions.

## Residual risks and unknowns (carried, not defects)

- The spec's own open items remain valid and should ride into the doc: terminal-cell
  vs archived terminal-daemon for the live proof (§9), no resume-id validity probe
  (§4b/§9), semantic-vs-literal model mapping (§9), and statusline field-spelling
  stability against the installed Claude Code version (§2d implementer items). None
  of these block enshrinement of the *shape*; they block the *implementation* of §4b.
- I did not run component tests (no code changed) and did not read `private-repos/`,
  `~/.claude`, or `/nix/store`.

## Verdict

**MUST-FIX-FIRST — not safe to enshrine as-is.** The direction is sound and should
be preserved, but three items must be resolved before this becomes the
design-of-record, because ARCHITECTURE.md would otherwise bake in an inconsistent
addressing model, a broken reply, and a fallback that contradicts fixed intent:

- **M1** — harness-instance ↔ session cardinality/addressing is internally
  contradictory (open keyed by (harness, handle); watch/observe keyed by harness
  alone); breaks observation-to-record correlation and per-session display once >1
  session is live.
- **M2** — `SessionRouted` omits the harness/session address Mentci must watch and
  leaks an internal `launch-directive`; the end-to-end watch flow cannot be wired.
- **M3** — the `/context` injection fallback interrupts a working agent (or is
  inapplicable when stopped), contradicting the fixed "never interrupt" principle.

Four should-fix items (S1 per-lane route race, S2 missing reactivation transitions,
S3 derived-status `HandoverDue`) and six optional design-quality items round out the
review; they can land with the implementation rather than blocking the doc if M1–M3
are resolved first.

**The single thing the doc rewriter must get right:** the harness-instance ↔
session addressing model (M1). Decide whether a harness hosts one session (key =
`HarnessName`) or many (key = `HarnessName` + `session-handle`, carried on watch and
observation alike), and make `OpenClaudeSession`, `ClaudeSessionObservation`,
`WatchHarnessTranscript`, and the `SessionRouted`/`PromptRouted` replies all consistent
with that one choice. Every downstream wire — orchestrate's store-update loop,
Mentci's display, resume/reuse, and "many concurrent sessions" — hangs off it.

## Verification pass — revised spec (round 2)

Re-read the revised `Design-SessionFlowSpec.md` to confirm the round-1 findings
are genuinely closed and no new inconsistency was introduced. Focused verify
pass, not a fresh audit.

Confirmed resolved:

- **M1 — addressing model.** Revised to one-session-per-harness-instance:
  `HarnessName` is the sole live-session key on `OpenClaudeSession` (§2c, handle
  dropped), `ClaudeSessionObservation` (§2d), `WatchHarnessTranscript`, and both
  replies (§2a/§2b); `(lane, session-handle)` is durable store identity only (§3);
  new `hosting-harness?: HarnessName` binds them (§3), set while Hot / cleared on
  Idle. Correlation is unique (§4c step 1 correlates the exit observation before
  clearing `hosting-harness`; per-open subscription sequencing isolates a
  reallocated instance's stream). §4a corrects the earlier substrate conflation.
  The model is threaded consistently; no surface remains keyed the old
  (harness, session-handle) way. **One new gap introduced by the fix — see below.**
- **M2.** `SessionRouted <harness-name> <disposition>` (§2b); `launch-directive`
  explicitly kept off the wire as daemon lowering; symmetric with `PromptRouted`.
- **M3.** Statusline `context_window` is the sole passive non-injecting source;
  "no `/context` (or any command) injection fallback" stated in §2d/§4b/§7/§9;
  absence handling defined (last-known-figure else unknown → not-past-threshold).
- **S1.** Per-lane route guard across the async model call (§2b, §6 step 4).
- **S2.** Reactivation edges explicit in §4c (→Hot on open/resume; un-archive-vs-GC
  ordering; resume-fail →Recycled from Idle or Archived).
- **S3.** Status enum is `Hot | Idle | Archived | Recycled`; handover-due derived at
  routing time, no stored variant, no dangling reference.
- No regression to the three ownership regions, push flow, `Worktree`-mirrored
  store, or §0.5 (M3 reconciliation reinforces §0.5).

New must-fix introduced by the M1 fix:

- **V1 — instance-allocation reservation race (breaks the invariant M1 rests on).**
  §2b lowering, §4a, and §6 step 5 all order allocation as *select non-Hot instance
  → async `OpenClaudeSession` → then write `hosting-harness`*. S1's guard is
  explicitly **per-lane**. Two concurrent routes for **distinct lanes** contending
  for the last free instance both observe "X is non-Hot," both select X, and both
  open on X before either records `hosting-harness=X` — binding two sessions to one
  instance and violating the one-Hot-record-per-instance invariant that M1's
  observation-to-record correlation depends on. Enshrining §4a's allocation prose
  as-is would carry this M1-shaped defect back in through the allocation path.
  Fix is narrow and already present in the spec for the sibling case: §4c step 3
  reserves the instance "in the same store transaction" for Archived-resume-vs-GC;
  **generalize that transactional/conditional reservation to all fresh and
  Idle-resume allocation** — reserve the chosen instance atomically (single-writer
  conditional on no other Hot record holding that `HarnessName`) *before* the async
  `OpenClaudeSession`, so a second concurrent distinct-lane route sees X taken.

### Round-2 verdict

**NO-GO — one narrow must-fix (V1) first.** M1, M2, M3, S1, S2, S3 are all
genuinely resolved and internally coherent, and nothing sound regressed. The M1
rewrite introduced a single new concurrency gap: instance allocation across
concurrent distinct-lane routes is unserialized (select-then-open-then-record),
which can double-book an instance and break the one-session-per-instance invariant
M1's correlation rests on. The fix is small — generalize the transactional
instance reservation the spec already specifies for the Archived-resume/GC case
(§4c step 3) to all allocation, reserving before the async open. With V1 closed,
the design is safe to enshrine.
