# persona-mind gap close — 2026-05-16

*Operator-assistant audit + finish work on the /185 persona-mind gap-scan
priority list, picking up after a prior session left an uncommitted working
copy. Two clean commits land; two priorities are deferred with concrete
escalation reasons.*

---

## TL;DR

| Priority | Status | Notes |
|---|---|---|
| P1 Channel choreography handlers | **Deferred — design escalation** | Minimal accept-all `ChoreographyAdjudicator` reachable, but the choreography policy/grant table/adjudication-log shape needs design beyond /91. Filing now would lock the wrong shape. |
| P2 StoreKernel Template 2 (dedicated OS thread) | **Deferred — kameo gap** | Kameo 0.20's supervised `spawn_in_thread()` signals "child closed" *before* the actor's `Self` value (which owns the redb `Database`) is dropped. Restart tests race the still-locked file and fail with `UnexpectedEof` or hang. Surfaced in ARCH + code comment; needs an upstream kameo hook. |
| P3 `ReplySupervisor` → `ReplyShaper` | **Already landed** before this session (commit `b4be099`). |
| P4 Subscription close, request-side + ack | **Landed (contract)** | `signal-persona-mind` commit `743a406` adds `MindReply::SubscriptionRetracted`, the `SubscriptionRetracted` record on `graph.rs`, ARCH text aligned with /91, plus a new `subscribe_opens_and_subscription_retraction_closes_the_mind_event_stream` witness that pins the `opened_stream()`/`closed_stream()` pairing. **Wire shape correct on the contract side; persona-mind dispatch still routes `SubscriptionRetraction` to `unimplemented()` — see P1.** |
| P5 Subscription push delivery (3-actor split) | **Deferred** | Larger refactor, gated on P1's choreography decision plane landing. The current `SubscriptionSupervisor` still buffers events behind `events: Vec<_>`; ARCH §"Subscription push delivery (destination)" describes the destination. |

Two commits pushed this session:

- `signal-persona-mind` `743a406` — pin streaming close semantics
  (`Retract SubscriptionRetraction` + `SubscriptionRetracted` ack); add the
  witness test that pins the macro's opened/closed-stream pairing; ARCH
  reworded to drop the "Path A reply-side only" overcorrection.
- `persona-mind` `3e3465f` — document `StoreKernel` Template-2 deferral
  (revert `.spawn_in_thread()` to `.spawn()`); correct ARCH text on
  subscription close to match `signal_channel!` grammar; drop the
  not-yet-true invariants the prior session added.

All 84 persona-mind tests pass; 67 signal-persona-mind tests pass (66
prior + 1 new witness).

---

## What the prior session actually landed (audit)

The session ran for ~47 minutes and committed real work to both repos
before hitting a rate-limit. Then it left an uncommitted working copy
that mixed correct work with at least three problems.

### Already-committed before this session

**`persona-mind`** (visible in `git log`):

- `b4be099` rename `ReplySupervisor` → `ReplyShaper`  (closes /185 P3)
- `ba920a4` document and test graph id policy
- `af19a16` consume proc-macro signal frames
- `63dac87` assert typed signal rejections
- `9d5c0ee` migrate transport+supervision to signal-core v3
- `730aacf` reject mismatched signal verbs on receive
- `b026b2f` own supervision relation

**`signal-persona-mind`**:

- `1dcb91b` pin hardened signal-core
- `60f341d` document streaming frame channel
- `51ac78b` update round trips for streaming signal frames
- `ec00cde` migrate to streaming channel grammar

These commits land the streaming-grammar wave and the rename. They are
correct.

### Found in the uncommitted working copy

`signal-persona-mind` had these unsaved edits when this session began:

- `src/lib.rs` — `MindReply::SubscriptionRetracted` variant added to the
  `signal_channel!` reply block.
- `src/graph.rs` — `SubscriptionRetracted` record (carries the
  `SubscriptionId`).
- `tests/round_trip.rs` — `subscription_replies_round_trip` extended to
  assert the new reply round-trips through Frame.
- `ARCHITECTURE.md` — added `SubscriptionRetracted` to the reply block,
  table row, and §"Path A reply-side variant" prose.

These were Path-A-aligned but written under /195's reading, not /91's.
Specifically, the prose said "the consumer cannot pre-emptively retract
through a request" and called `MindRequest::SubscriptionRetraction`
"transitional; it retires on the next major schema bump." That
contradicts /91 directly. The CODE (the `signal_channel!` macro
invocation) was already right — `Retract SubscriptionRetraction` is a
request variant and `close SubscriptionRetraction` names it as the
stream's close trigger. Only the ARCH narrative was overcorrected.

`persona-mind` had these unsaved edits:

- `src/actors/store/mod.rs` — `.spawn()` → `.spawn_in_thread()` on the
  supervised `StoreKernel`.
- `tests/*` — every `#[tokio::test]` annotated as
  `#[tokio::test(flavor = "multi_thread")]`.
- `ARCHITECTURE.md` — added §"ChoreographyAdjudicator (destination)",
  §"Subscription push delivery (destination)", and the Template-2
  status text claiming the kernel runs on a dedicated OS thread.
- New invariants at §9 asserting `spawn_in_thread`, Path A reply-side
  close, and choreography-actor routing — none of which the code holds
  today.

The `.spawn_in_thread()` change introduced a real correctness regression
(see §"Template-2 deferral" below). The multi_thread annotations
amplified it: they revealed a parallel-test hang that single-thread
annotations don't trigger.

---

## P4 — subscription close discipline (`signal-persona-mind` `743a406`)

### What changed

The contract's `signal_channel!` invocation already had the right shape
in `ec00cde` (the streaming-grammar migration):

```rust
Subscribe SubscribeThoughts(SubscribeThoughts) opens MindEventStream,
Subscribe SubscribeRelations(SubscribeRelations) opens MindEventStream,
Retract  SubscriptionRetraction(SubscriptionId),
…
stream MindEventStream {
    token   SubscriptionId;
    opened  SubscriptionAccepted;
    event   SubscriptionDelta;
    close   SubscriptionRetraction;
}
```

The macro emits `MindRequest::opened_stream()` and
`MindRequest::closed_stream()` from this pairing. `SubscribeThoughts`
returns `Some(MindEventStream)` from `opened_stream`; `SubscriptionRetraction`
returns `Some(MindEventStream)` from `closed_stream`. That is the /91
shape: subscribe → events → retract → final ack → stream end.

The reply enum's `SubscriptionRetracted` variant and the record on
`graph.rs` were uncommitted in the prior session's working copy. This
session committed them together with:

- ARCH text rewritten to describe the four-step lifecycle in `signal_channel!`
  terms, dropping the "Path A reply-side only" language.
- A focused witness test
  `subscribe_opens_and_subscription_retraction_closes_the_mind_event_stream`
  in `tests/round_trip.rs` that asserts:
  - `SubscribeThoughts.opened_stream() == Some(MindEventStream)`
  - `SubscribeRelations.opened_stream() == Some(MindEventStream)`
  - `SubscriptionRetraction.closed_stream() == Some(MindEventStream)`
  - `SubscribeThoughts.closed_stream() == None` (opens, doesn't close)
  - `SubscriptionRetraction.opened_stream() == None` (closes, doesn't open)
  - The retract request round-trips through Frame.

This witness is the architectural-truth test for /91: a future refactor
that tries to drop the request-side retract verb (returning to the /195
reading) breaks compilation and review here.

### What the contract change does **not** touch

The persona-mind `DispatchPhase` still routes `MindRequest::SubscriptionRetraction(_)`
to `self.unimplemented(trace)` at `src/actors/dispatch.rs:118`. The wire
shape is correct on both sides of the contract; the runtime handler
isn't wired yet. That sits in the same package as the choreography
handlers (P1).

---

## P2 — StoreKernel Template-2 deferral

### The discovered gap

The prior session changed the supervised `StoreKernel` spawn from
`.spawn()` to `.spawn_in_thread()` (Template 2 from
`~/primary/skills/kameo.md`). The intent matches /185 P2 exactly:
StoreKernel does synchronous redb transactions on every message; running
those on the shared tokio worker pool stalls sibling actors scheduled
there.

The implementation breaks daemon restart. With `.spawn_in_thread()`:

- First daemon writes, then drops.
- `MindRoot::stop()` → `stop_gracefully` propagates through
  `set_children_parent_shutdown` → `send_children_shutdown` →
  `wait_children_closed`.
- For the StoreKernel child, that "closed" signal fires the moment
  Kameo's `notify_links` drops `mailbox_rx` (kameo
  `src/actor/spawn.rs:232`, lifecycle path).
- But the actor's `Self` value (which owns `MindTables` → `Engine` →
  `Sema` → `redb::Database`) lives until the `block_on(...)` returns,
  which is after `on_stop` runs at `spawn.rs:235` and the function
  returns at `spawn.rs:257`.
- The parent's `wait_for_shutdown` returns BEFORE the redb file lock
  is released.
- The second daemon's `bind()` opens redb. It races the old OS thread.
  On the same machine, the `mind_memory_graph_survives_process_restart`
  test fails with `Io(Custom { kind: UnexpectedEof, error: "early eof" })`;
  `mind_store_survives_process_restart` hangs indefinitely.

Switching to `.spawn()` (Tokio task) fixes both tests because the
tokio runtime continues processing the task to completion before the
test's `tokio::main` exits, dropping the actor's Self value while
the runtime is still alive.

### Where the kameo hook needs to grow

Kameo 0.20's `Actor::on_stop` runs *after* `notify_links` (which is
what makes "child closed" fire), so on_stop can't release resources
early enough either. The right shape is one of:

- **Kameo grows a `pre_notify_links` hook** that runs before
  `notify_links` so resource-holding actors can drop their handles
  while the parent is still waiting on `wait_children_closed`.
- **The actor wraps its critical resource in `Option<T>` and exposes a
  close-then-confirm message** the supervisor sends before
  `stop_gracefully`, with the supervisor `await`ing the confirm before
  it propagates shutdown further.

Both options are escalation territory: option 1 needs an upstream PR
(or fork) of kameo; option 2 is a non-trivial actor protocol design
that interacts with restart semantics.

### What this session actually landed

- `src/actors/store/mod.rs` reverts `.spawn_in_thread()` to `.spawn()`.
  The destination-shape comment block in `on_start` documents the gap,
  the failure mode, and the hook that needs to land.
- `ARCHITECTURE.md` §4 reworded — current implementation says `.spawn()`
  with destination of Template 2 + explicit gap explanation. The §9
  invariant claiming the dedicated OS thread is removed; the file
  states what IS, not what we wish were true.
- Tests reverted from `#[tokio::test(flavor = "multi_thread")]` back to
  `#[tokio::test]`. The reason: with the kernel on a Tokio task
  (`.spawn()`), multi_thread isn't required, and the multi_thread
  annotations introduce a second hang — see §"Found by accident" below.

### Found by accident — multi_thread parallel-restart hang

With `flavor = "multi_thread"` AND `.spawn_in_thread()`, the restart
tests fail individually. With `flavor = "multi_thread"` AND `.spawn()`,
the restart tests pass individually but **hang when run in parallel**
(default cargo test order):

```
test mind_memory_graph_survives_process_restart ... ok
test mind_store_survives_process_restart has been running for over 60 seconds
test mind_typed_thought_graph_survives_process_restart has been running for over 60 seconds
```

With `#[tokio::test]` (single-thread default) AND `.spawn()`, all 12
daemon_wire tests pass in parallel. The multi-thread + parallel
combination triggers a separate kameo/tokio interaction that needs
isolating — possibly registry contention between multiple tokio
runtimes each containing the same actor names, possibly something
about how kameo's link bookkeeping shares state across runtimes via
the `parallel_runtimes_cannot_share_registry_names_or_memory` witness
test. Out of scope for this gap-close; flagging here so the next
session that revisits Template 2 lands the `multi_thread` flip
together with whatever isolation fix this needs.

---

## P1 — channel choreography handlers (deferred)

Per /200 Move F1 and the ARCH §"ChoreographyAdjudicator (destination)"
the destination is a stateful child of MindRoot owning:

- a live `ChoreographyPolicy` that decides grant/deny;
- a grant table keyed by `ChannelId` carrying active grants;
- an adjudication log for audit and replay.

A minimal "accept all by default" implementation is reachable:
generate a `ChannelId`, emit `ChannelGrant` / `AdjudicationReceipt`,
keep grants in a `HashMap<ChannelId, ChannelGrant>` for `ChannelExtend`
/ `ChannelRetract` / `ChannelList`, and `AdjudicationDeny` rejects a
pending request.

**Reason for deferral: design beyond /91.** The choreography policy
must answer at least:

- *Where does the policy live?* In code (a const decision tree)? In a
  config file? In `mind.redb`? Per /91 it needs to be reachable by
  designers without a recompile, but no existing report names the
  policy storage shape.
- *Who is authorised to call which choreography verb?* The contract
  carries `MessageOrigin` but the persona-side mapping from caller
  identity to "allowed to grant a channel between X and Y" is
  undefined.
- *What's the relationship between `ChannelGrant`/`AdjudicationRequest`
  and the channel allow-list that the router enforces today?* Per
  /200 the choreography actor is supposed to *gate* router traffic.
  No report names the data flow from grant → router.
- *Does `ChannelRetract` propagate to existing in-flight messages, or
  only to new traffic?*

Landing a minimal "accept all" handler closes the dispatch
`unimplemented()` arm but bakes in answers to all four questions by
silent default. Per the discipline rule "If a gap requires DESIGN
beyond /185 + /90 + /91, STOP and surface in report" — escalating.

`SubscriptionRetraction` shares the dispatch arm but is conceptually a
**different** verb: it closes a subscription stream, it isn't a
choreography request. The destination is for the subscription
supervisor (P5) to handle, not the choreography adjudicator. The ARCH
text was corrected to reflect that.

---

## P5 — subscription push delivery (deferred)

The current `SubscriptionSupervisor` (`src/actors/subscription.rs`)
collects post-commit deltas in an in-actor `events: Vec<_>` buffer.
Per /195 / ARCH §"Subscription push delivery (destination)" the
destination split is three actors:

- `SubscriptionManager` — owns subscription metadata + persists to
  `thought_subscriptions` / `relation_subscriptions` tables.
- `StreamingReplyHandler` — one per live subscription; owns the reply
  channel; emits `SubscriptionRetracted` on close.
- `SubscriptionDeltaPublisher` — fires after each store commit; reads
  the committed delta, looks up matching subscriptions, hands deltas
  to the matching `StreamingReplyHandler`s.

This destination is correctly described in ARCH §3. Implementation
gated on P1's adjudicator landing because the streaming reply channel
shares the choreography policy decision surface (who is allowed to
stream what to whom). Larger than this gap-close session.

---

## Files touched

`/git/github.com/LiGoldragon/signal-persona-mind/` — commit `743a406`:

- `src/graph.rs` — `SubscriptionRetracted` record + doc comment
  (carried over from prior session's working copy).
- `src/lib.rs` — `MindReply::SubscriptionRetracted` variant in the
  `signal_channel!` reply block (carried over from prior session).
- `tests/round_trip.rs` — extended `subscription_replies_round_trip`
  (prior session) + new `subscribe_opens_and_subscription_retraction_closes_the_mind_event_stream`
  witness (this session).
- `ARCHITECTURE.md` — `SubscriptionRetracted` added to reply block + §3.1.5
  table; subscription-close prose rewritten to describe both halves of
  the streaming grammar (this session); transitional-retire comment on
  the `Retract` variant removed (this session); §8 invariant about
  reply-side-only close removed (this session).

`/git/github.com/LiGoldragon/persona-mind/` — commit `3e3465f`:

- `src/actors/store/mod.rs` — `.spawn_in_thread()` reverted to
  `.spawn()`; deferral comment block describing the kameo shutdown
  gap and pointing at this report.
- `ARCHITECTURE.md` — current-vs-destination text on `StoreKernel`
  spawn; subscription-close discipline rewritten per /91; the new §3
  ChoreographyAdjudicator + Subscription push delivery destination
  sections (added in prior session) preserved; §9 invariants that
  don't hold today removed; the `multi_thread` requirement removed.
- `tests/actor_topology.rs`, `tests/cli.rs`, `tests/daemon_wire.rs`,
  `tests/weird_actor_truth.rs` — `#[tokio::test(flavor = "multi_thread")]`
  reverted to `#[tokio::test]`. Reason: with `.spawn()` the
  multi-thread runtime isn't required, and it surfaces a separate
  parallel-test hang in restart tests (see §"Found by accident").

---

## Test results

`persona-mind`: 84 tests pass.

```
running 5 tests  — smoke                            (5 passed)
running 24 tests — actor_topology                  (24 passed)
running 13 tests — cli                              (13 passed)
running 12 tests — daemon_wire                      (12 passed)
running  7 tests — memory                            (7 passed)
running  5 tests — smoke (duplicate from binaries)  (5 passed)
running 18 tests — weird_actor_truth                (18 passed)
```

`signal-persona-mind`: 67 tests pass (66 prior + 1 new
`subscribe_opens_and_subscription_retraction_closes_the_mind_event_stream`
witness).

---

## Open items for the next session

1. **Channel choreography design.** Where does the policy live; who's
   authorised; how do grants gate the router; what does retract mean
   for in-flight messages? Designer call. Then a minimal
   `ChoreographyAdjudicator` actor can land, route the six choreography
   request variants through it, and clear the dispatch `unimplemented()`
   arm. `SubscriptionRetraction` routes to the subscription supervisor,
   not here.
2. **Kameo shutdown hook for Template 2.** Either upstream a
   `pre_notify_links` hook to kameo or design an actor-owned
   close-then-confirm protocol. Then the `.spawn()` → `.spawn_in_thread()`
   switch is one line.
3. **Multi-thread parallel-restart hang.** Independent of (2),
   investigate why `flavor = "multi_thread"` makes the three
   `*_survives_process_restart` tests hang when run in parallel. The
   `parallel_runtimes_cannot_share_registry_names_or_memory` witness
   suggests this is a known shape — needs isolating before the
   multi-thread flip lands with (2).
4. **Subscription push delivery (P5).** Three-actor split per /195.
   Gated on (1) because the streaming reply channel shares the
   choreography decision surface.

The two clean commits are pushed to `origin/main` on both repos. No
in-progress branches; no uncommitted working copy left behind.
