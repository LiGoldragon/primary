# Rust Auditor — Live-View Contract + Subscriber Review

Bead: **primary-og38.6**. Independent audit of the two load-bearing pieces of
the live-view build, before the live proof (og38.7) is built on them.

## Verdict

**SAFE to build the live proof (og38.7) on the pieces as-is.**

- **Must-fix findings: 0.** No correctness, contract-soundness, push-discipline,
  or special-case-dissolution defect blocks og38.7.
- The audited code is sound: the contract is runtime-free with correct additive
  versioning and thorough round-trips; the projection is a clean method on a
  data-bearing type with a properly-marked deferred field; the fan-out is genuine
  push with a race-free snapshot-then-register ordering; the merged delta path
  preserves the sequence guarantee for the subset that needs it without inventing
  one for the subset that does not.
- Findings below are all **optional / provisional** plus one **non-blocking**
  integration front (Flag 1) that is orthogonal to og38.7.

## Scope and sources consulted

Under audit (both working copies sit as empty commits directly on the audited
revisions with no local changes, so on-disk files match exactly):

- Contract: `signal-harness` `main` @ `9f989d24` (v0.3.0), `/git/github.com/LiGoldragon/signal-harness/src/lib.rs`.
- Producer/subscriber: `harness` `main` @ `fbb7d8cd`, `/git/github.com/LiGoldragon/harness/src/{subscription.rs,daemon.rs,claude_session.rs}` and the two witness tests `tests/claude_session_stream.rs`, `tests/claude_session_observation.rs`.
- Grounding: `agent-outputs/MentciOrchestrateSessionFlow/Design-SessionFlowSpec.md` §2d, the og38.3 close reason, and the og38.4 bead NOTES (the implementer's three self-flagged items).
- Doctrine: contract-repo, push-not-pull, typed-records-over-flags, design-quality (all read this session).

## Checks run (exact results)

- `signal-harness` `cargo test` (default features = `nota-text`): the `round_trip`
  suite reports **40 passed, 0 failed**; `claude_session_observation_round_trips_through_rkyv`
  and `..._through_nota_text` both green; whole crate green.
- `signal-harness` `cargo build --no-default-features`: **FAILS** — 10 × E0277 at
  `src/lib.rs:1223` (`HarnessDaemonConfiguration` / `HarnessInstanceConfiguration`
  deriving `NotaEncode`/`NotaDecode` over `signal-persona` socket/owner types whose
  Nota impls are themselves gated behind `signal-persona/nota-text`). **Pre-existing
  and unrelated to this change** — these config types were untouched by the
  ClaudeSessionObservation commit; the crate has never built without `nota-text`.
- `harness` `cargo test --test claude_session_stream --test claude_session_observation`:
  **5 passed, 0 failed** (2 stream + 3 projection).
- `harness` `cargo clippy --lib`: 1 error + 2 warnings. The **error** is
  `never_loop` at `src/claude.rs:369` (`#[deny]`, PRE-EXISTING — also flagged by
  the og38.2 implementer at parent `f07c4dfe`, in untouched `claude.rs`). The two
  **warnings** are `result_large_err` at `src/subscription.rs:219` (Flag 3, see
  below) and a `collapsible_if` at `claude.rs:1417` (pre-existing, untouched file).
- **Not run** (stated as missing prerequisites): the two Nix flake checks
  (`harness-observed-turn-...`, `harness-claude-session-observation-is-pushed-...`),
  the full 48-test harness suite, and the real-headless-claude witness bin
  `harness_claude_session_stream_test` (needs a `claude` binary + sandbox). The
  cargo-level equivalents of the two flake checks were run directly and are green.

## Findings by audit dimension

### 1. Push-not-pull correctness — PASS

- **Genuine push, no hidden poll.** The publisher (`TranscriptDeltaPublisher`,
  `subscription.rs:719-751`) handles `PublishStreamEvent` by reading the handler
  set and `handler.ask(DeliverTranscriptDelta{..}).await` per handler. The daemon
  `serve` loop (`daemon.rs:900-912`) is a `tokio::select!` parked on
  `self.receiver.recv()`. No `sleep`, interval, or ticker anywhere on the
  subscriber path. The witness test `claude_session_observation_is_pushed_to_subscriber_without_polling`
  proves quiescence (`try_recv()` returns `Empty` before publish, and again after
  delivery) and wake-on-push (`recv().await` yields only after the producer
  pushes) — a correct no-poll witness against the real producer-plane actors.
- **Backpressure is sound for the shipped path.** `TranscriptSubscriptionSink::try_push`
  (`subscription.rs:219-238`) returns `Err(event)` when `pending_acceptance == 0`
  (the bounded in-memory sink) or when the mpsc receiver is gone (the channel
  sink). The **production daemon uses the unbounded `channel` sink**
  (`daemon.rs:824`), so the drop-on-overrun branch is exercised only by the
  bounded test sink; the live view cannot lose an event to backpressure. See
  Flag 3 for the discard nuance.
- **No snapshot-then-stream race on a per-open subscription.** In the manager's
  `OpenTranscriptSubscription` handler (`subscription.rs:544-583`) the snapshot is
  pushed into the sink (`handler.ask(DeliverSnapshot).await`, line 568) **before**
  the handler is added to the routing set (`self.open.push(..)`, line 573). The
  manager is a single sequential kameo actor and the publisher discovers handlers
  from that same actor (`ReadSubscriptionHandlers`), so a publisher can never fan a
  delta to a handler before that handler's snapshot is already queued in its FIFO
  channel — snapshot always precedes the first delta. No missed wakeup, no
  inversion, no lost-event on open.

### 2. Special-case dissolution — PASS (correct, not a conflation)

`TranscriptObservation` and `ClaudeSessionObservation` share one fan-out path via
`HarnessStreamEvent`. This is a real dissolution, not a conflation:

- The strictly-increasing sequence lives **inside** `TranscriptObservation`
  (`sequence: HarnessTranscriptSequence`, contract line 623), stamped by the
  producer. The fan-out plane (`DeliverTranscriptDelta`, the handler, the sink) is
  entirely **sequence-agnostic** — it never reads, advances, or requires a
  sequence. So merging the two event types onto one path costs the sequenced
  subset nothing.
- `ClaudeSessionObservation` carries **no** sequence field and the producer path
  for it (`daemon.rs` `publish_claude_session_observation` → `publish_stream_event`)
  touches **no** sequence counter. Publishing a `ClaudeSessionObservation` therefore
  cannot perturb `TranscriptObservation`'s numbering — the transcript subset stays
  strictly increasing regardless of interleaving. No sequence was invented for the
  subset that does not need one.
- The one real subtlety — that a subscriber counting *all* deltas must key
  gap-detection off `TranscriptObservation.sequence` specifically, not off delta
  arrival count — is exactly the invariant the implementer flagged for the
  ARCHITECTURE.md note (Flag 2). The code is correct; only the doc lags.

### 3. Contract soundness — PASS

- **Runtime-free (contract-repo).** `signal-harness` `Cargo.toml` deps are `nota`,
  `signal-frame`, `signal-persona`, `rkyv`, `thiserror` — no tokio/kameo/daemon
  runtime. `unsafe_code = "forbid"`. Clean.
- **Versioning 0.2 → 0.3.** Adding a variant to the `HarnessStreamEvent` enum and
  a stream event is a wire-breaking change (an old exhaustive decoder cannot
  handle the new discriminant). A `0.2 → 0.3` minor bump is the correct
  breaking-signal under 0.x semver. Deliberate and correct.
- **Round-trips (rkyv + NOTA).** `claude_session_observations()` in `round_trip.rs`
  covers a fully-populated completed turn, an all-`Option`-unset pre-first-turn
  observation, and one sample per remaining `launch`/`lifecycle` variant
  (including the data-carrying `Exited(Failure)` arm). The rkyv test is **ungated**
  (proves the binary wire without NOTA); the NOTA-text test is gated behind
  `nota-text`. A `canonical.nota` example for `ClaudeSessionObservation` is added
  and asserted. Both green.
- **typed-records-over-flags.** `TurnLaunch {Fresh, Resumed, SelfHealed}` and
  `ClaudeSessionLifecycle {Ready, Active, Completed, Exited(AdapterExitStatus)}`
  are closed enums (the latter carries data on `Exited`), correctly not booleans.
  The lone `reached_end_of_turn: bool` is a **correct** boolean: its "yes" carries
  no payload (it mirrors the observer's own `has_stop_reason_end_turn()` signal),
  and it is genuinely orthogonal to `lifecycle` (a transcript-level clean-stop
  fact vs the process/session lifecycle — a turn can be `Completed` yet not
  `reached_end_of_turn`, e.g. a turn cap). Defensible.
- **The wide 13-field flat record — defensible, not a misuse hazard.** The three
  activity counts (`streamed_event_count`, `tool_call_count`,
  `status_transition_count`) are each a **distinct newtype**, and the record is
  built by named-field struct literal, so positional/argument confusion is already
  impossible — the newtypes are the misuse guard, not a grouping. Grouping them
  into a `TurnActivityCounts` sub-record would be a mild symmetry/readability win
  (13 → 11 fields) but buys no correctness. Optional (below), not a defect. Note
  the record deliberately fuses design §2d's store-shaped facts with the demo's
  render facts onto one event, which is what widens it beyond §2d's 6-field
  sketch — legitimate under the shared-stream design.

### 4. `accumulated_context` deferral — PASS (clean)

`ObservedClaudeTurn::into_session_observation` (`claude_session.rs:94-130`) sets
`accumulated_context: None` with an explicit inline marker citing bead
`primary-og38.1` and the pending A/B ruling; the doc comment states no figure is
synthesized. The projection is a consuming method on a data-bearing type
(`abstractions`/`rust-methods` clean). Nothing downstream assumes it is
populated: the witness test asserts it crosses the wire as `None`
(`claude_session_stream.rs`), the contract doc marks it `Option` with sourcing
deferred, and orchestrate is not yet a consumer. No pull-shaped placeholder or
self-calculated figure leaked in.

## Optional / provisional findings (not blockers)

- **O1 — `result_large_err` justification is inaccurate (Flag 3).** The Err payload
  of `try_push` (`subscription.rs:219`) is **discarded by every caller**: the three
  handler arms (`DeliverSnapshot`/`DeliverTranscriptDelta`/`EmitFinalRetractionAck`)
  all match `Err(_)` and only bump `buffered_overruns`; the channel path's returned
  event is likewise dropped by the daemon writer. So "Err returns the rejected event
  for backpressure" is not realized — nothing requeues it. The large Err variant is
  therefore pure overhead, not a backpressure mechanism. Harmless (warning-level,
  non-gating, and negligible on the unbounded prod path), but the cleaner shapes are
  to `Box` the variant, return a small overrun marker (`Result<(), ()>` / a typed
  unit), or `#[allow(clippy::result_large_err)]` with an accurate comment. Optional.
- **O2 — Nota-gating asymmetry is cosmetic and slightly misleading.**
  `ClaudeSessionObservation` gates its `NotaEncode`/`NotaDecode` behind `nota-text`
  (forced by its `TimestampNanos` field, whose Nota impl is itself gated — so the
  gate is *necessary* for that type), while sibling `TranscriptObservation` and the
  newtypes derive unconditionally. But the crate **cannot build `--no-default-features`
  at all** (pre-existing failure at the config types, `lib.rs:1223`), so the gate is
  defensive-but-moot. The og38.3 close-reason phrase "NOTA gated behind nota-text"
  could mislead a reader into thinking a no-nota-text build is supported; it is not.
  No regression; note only.
- **O3 — `TurnActivityCounts` sub-record (design-quality).** Optional grouping of
  the three counts for symmetry, per finding in dimension 3. Low value, low risk.

## Flag dispositions

- **Flag 1 (integration skew) — REAL but correctly-deferred; ORTHOGONAL to og38.7;
  needs a tracked bead. Non-blocking for this audit.** Consuming `signal-harness`
  0.3.0 relocked every `branch=main` git dep forward in harness's `Cargo.lock`:
  `signal-frame` `b78c8077 → 0027ea3c` (plus `triad-runtime`, `nota`, `schema`,
  `schema-rust`, `signal-persona`). `message_router_harness_e2e.rs` is a real
  cross-daemon e2e (`message` + `signal-router` + `signal-terminal` binaries) that
  **skips gracefully** without sibling binaries/env (`MESSAGE_CLI_BINARY` etc.), so
  the sandboxed flake check stays green, but **fails locally** because harness's
  daemon now speaks `signal-frame 0027ea3c` while the still-unrelocked message/router
  daemons speak `b78c8077`. Assessment: this is not a defect in either audited piece
  — it is the inherent consequence of the `branch=main` relock model, on the
  explicitly-deferred message-router path (design §8; psyche-deferred). It is
  **orthogonal to og38.7**, which renders a headless session's turns through the
  harness transcript stream + `ClaudeSessionObservation` and does not involve the
  message/router daemons at all. **Recommendation:** it is a genuine latent
  integration front, not benign-nothing-to-do. A `bd list` search
  (`message router` / `signal-frame` / `integration`) found **no existing tracking
  bead**, so one should be filed for the coordinated `signal-frame` relock across
  the `message` and `router` repos, so the skew is not silently rediscovered when the
  `message_router_harness_e2e` path is built. Provisional — auditor recommendation,
  not authority to create it.
- **Flag 2 (docs) — VALID deferral; do before/with og38.7 for the sequence note.**
  The **contract** repo's `ARCHITECTURE.md` *was* updated (adds the
  `ClaudeSessionObservation` paragraph + the reply/event-side table row — verified in
  the diff). The lag is the **harness daemon** repo's `ARCHITECTURE.md`, untouched by
  `fbb7d8cd` (confirmed absent from the diff). It needs a §1.6 update naming
  `ClaudeSessionObservation` as the second stream event and scoping the
  "strictly-increasing sequence" invariant to the `TranscriptObservation` subset
  (`ClaudeSessionObservation` carries none) — which independently matches the real
  subtlety confirmed in dimension 2. Not a code blocker; owned by the docs lane.
- **Flag 3 (lint) — ACCEPT as-is for og38.7; optional cleanup.** `result_large_err`
  confirmed warning-level and non-gating (see O1 for the justification correction).
  The `cargo clippy --lib` **failure** is the separate pre-existing `#[deny]`
  `never_loop` in untouched `claude.rs:369`; it predates this bead (also seen at
  parent `f07c4dfe`) and is worth its own bead if clippy-clean is a repo goal, but it
  does not gate the flake checks and is out of scope here.

## Residual risks for og38.7

- **No current-state replay of `ClaudeSessionObservation` on connect.** The
  subscription snapshot carries only a `TranscriptObservation` sequence pointer (and
  that pointer is a prototype stub always minted as `0`, `subscription.rs:561`); it
  does **not** backfill the last `ClaudeSessionObservation`. A subscriber that
  attaches *after* a turn's observation was pushed will not see it — it receives
  only observations pushed after it subscribed. For og38.7 this is fine **iff the
  egui view opens its `WatchHarnessTranscript` subscription before the headless turn
  runs**; if the view can attach to an already-running/already-finished session it
  will miss that session's latest observation. Pre-existing prototype behavior,
  identical for both event types, not introduced by this change — flag it to the
  og38.7 implementer as an ordering requirement, not a code fix.
- **`accumulated_context` stays `None`.** og38.7 must not render or gate on a
  context figure; it is deferred to og38.1's ruling. The witness confirms it crosses
  as absent.

## Blockers / unknowns

- No blockers to og38.7.
- Not independently verified (stated as missing prerequisites): the two Nix flake
  checks and the real-headless-claude witness bin (need `nix` build of the checks
  and a `claude` binary + sandbox). The cargo-level equivalents of the two flake
  checks and both witness test files were run directly and are green, which
  substantiates the implementer's push-without-polling and projection claims.
