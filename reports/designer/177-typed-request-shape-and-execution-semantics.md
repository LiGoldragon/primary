# 177 — Typed `Request<Payload, Intent>`, closed intents, and execution semantics

*Designer follow-up, 2026-05-15. Responds to DA's critique of the prior draft.
All six findings are correct on the design level — none are migration
concerns. Settles the open type-shape and semantic-precision questions
that prevented the prior draft from being implementation-ready. Becomes the
spec of record; the prior draft is superseded by the present report's §3–§7.
The verb spine remains six elementary verbs (Assert / Mutate /
Retract / Match / Subscribe / Validate), no `Atomic`; frames are
operation-batches with a consistency boundary.*

**Retires when**: the operator picks up implementation; the spec
absorbs into `signal-core/ARCHITECTURE.md`.

---

## 0 · TL;DR

DA's six findings on the prior draft:

1. `Request<P>` typing doesn't match per-domain `BatchIntent`. Either
   make Request generic over both, or move intent into the payload.
2. `Custom(String)` in the intent enum violates closed-boundary
   discipline.
3. "Frame is the commit boundary" is too absolute — pure Match,
   Validate, or Subscribe frames don't commit.
4. Mixed-Validate semantics contradict operation-ordering — the prior draft
   says both "strict ordered" and "phased."
5. Mixed Match + writes is ambiguous — pre-write / post-write /
   read-your-own-writes are different.
6. `BatchOutcome::Committed` doesn't fit non-write frames; the names
   should describe completion, not only commit.

All six are real. The settlements:

1. **`Request<Payload, Intent>`** generic over two type parameters.
   Each contract's macro invocation supplies its concrete types.
2. **No `Custom(String)`.** Intent enums are closed. Adding a new
   intent is a coordinated contract-version bump, same discipline as
   adding a request variant.
3. **The frame is an *operation batch* and a *consistency
   boundary*.** Writes inside it commit atomically; reads inside it
   observe one snapshot; subscribes inside it open at the snapshot.
   "Commit boundary" applies to the write subset only.
4. **Strict ordered execution.** Each op sees the cumulative effects
   of all prior ops in the same frame. This is more expressive than
   phased (preflight patterns work by putting Validates first;
   checkpoint patterns work by putting Validates after writes).
5. **Read-your-own-writes.** Each Match (and each later Mutate) sees
   the cumulative state including effects of prior ops in the same
   frame. No result binding (no variables); conditional writes use
   the existing `expected_rev` pre-condition pattern.
6. **`BatchOutcome::Completed` / `Aborted`.** Names describe
   completion; outcome works for any frame shape. Per-op replies
   carry the verb-specific result.

The corrected design is the `signal-core` and `Request`/`Reply` spec
of §3–§7 below. the prior draft's recommendation (the collapse) stands; the
shape is now precise enough to implement.

---

## 1 · The findings, taken in order

### 1.1 · `BatchIntent` can't live in `signal-core` ✓

the prior draft wrote:

```rust
pub struct Request<P> {
    pub intent: Option<BatchIntent>,
    pub correlation: Option<CorrelationId>,
    pub ops: Vec<Op<P>>,
}
```

…and then said `BatchIntent` is per-domain. But `signal-core` doesn't
know domain-specific intent enums. The shape doesn't typecheck. Fix:
generic over both:

```rust
// signal-core
pub struct Request<Payload, Intent> {
    pub intent: Option<Intent>,
    pub correlation: Option<CorrelationId>,
    pub ops: Vec<Op<Payload>>,
}
```

Each contract's `signal_channel!` invocation supplies concrete types:

```rust
// signal-persona-mind
signal_channel! {
    request MindRequest with intent MindBatchIntent {
        Assert SubmitThought(SubmitThought),
        Mutate StatusChange(StatusChange),
        // ...
    }
}

// Macro emits:
pub type MindFrame = Frame<MindRequest, MindReply, MindBatchIntent>;
```

The intent type is part of the channel's typed identity, exactly
like the request payload enum.

### 1.2 · `Custom(String)` is a closed-boundary violation ✓

the prior draft ended the example intent enum with:

```rust
pub enum MindBatchIntent {
    RoleHandoff(...),
    SchemaUpgrade(...),
    ChannelMigration(...),
    Custom(String),    // ← violates closed-boundary discipline
}
```

`Custom(String)` is the same shape as the `Unknown` escape-hatch the closed-boundary discipline
rules out — an open escape hatch that makes the enum no-longer-closed
and the audit-trail no-longer-typed. Either an intent matters (so
it's a closed variant) or it doesn't matter (so the frame goes
without an intent, `intent: None`).

Fix:

```rust
pub enum MindBatchIntent {
    RoleHandoff,
    SchemaUpgrade,
    ChannelMigration,
    // No Custom. Adding a new intent is a coordinated contract bump.
}
```

This matches the discipline used for the request payload variants
themselves. The intent enum participates in the same versioning
contract as the variant enum.

### 1.3 · "Commit boundary" overstates ✓

the prior draft claimed "the frame IS the commit boundary" universally. But:

- A frame of only `Match` ops does not commit; it reads at a snapshot.
- A frame of only `Subscribe` ops does not commit; it opens streams.
- A frame of only `Validate` ops does not commit; it dry-runs.

These frames are still bounded — they share a snapshot, they reply
together — but they don't commit. The honest framing:

> The frame is an **operation batch** and a **consistency
> boundary**. All ops within the frame share one snapshot. Write
> effects inside the batch commit atomically when the batch contains
> writes. Read effects observe the shared snapshot. Subscribe
> effects open at the post-commit snapshot (or, if no writes, the
> shared snapshot). Validate effects dry-run against the shared
> snapshot (including any prior writes in the same batch).

This is precise. "Commit boundary" applies to the write subset, not
to the frame as a whole.

### 1.4 · Ordered vs phased execution — pick one ✓

the prior draft said both:

- "Within an atomic boundary, operations execute in order, with each
  seeing the effects of previous operations in the same boundary"
  (strict ordered, §1.3)
- "Mixed validate + writes: validates run first; if any fails, no
  writes commit. If all validates pass, writes commit atomically."
  (phased, §4.1 table)

These are different models. The strict-ordered model is more
expressive (you can validate intermediate states); the phased model
is simpler.

Settlement: **strict ordered execution**.

```text
- Ops execute in declared order.
- Each op observes the cumulative effects of all prior ops in the
  same batch.
- A Validate at position N checks invariants against state including
  prior writes at positions 1..N-1.
- A Mutate at position N+1 reads the state including writes at
  positions 1..N (read-your-own-writes).
- Failure of any op at position K rolls back writes at positions
  1..K-1; ops at positions K+1..N are skipped (SubStatus::Skipped).
```

Both useful patterns work in this model:

- **Preflight pattern**: put Validates first.
  `[Validate Constraint, Assert RecordA, Assert RecordB]` — if
  validation fails (position 0), no writes execute.
- **Checkpoint pattern**: put Validates after writes.
  `[Mutate Catalog→Migrating, Mutate Row1, Validate Integrity,
  Mutate Catalog→Active]` — the Validate at position 2 sees the
  effects of prior Mutates.

Strict-ordered covers both. Phased only covers the first.

This matches Datomic's `d/with` and SQL's transaction semantics: each
statement sees the cumulative effect of prior statements in the same
transaction.

### 1.5 · Mixed Match + writes — pick semantics ✓

DA's three possibilities:

- **Pre-write snapshot**: reads see state *before* writes in the
  batch.
- **Post-write snapshot**: reads see state *after* all writes commit.
- **Read-your-own-writes**: each read sees the cumulative state
  including prior ops in the batch.

Settlement: **read-your-own-writes** (RYOW), as a direct consequence
of §1.4's strict-ordered execution. Each Match at position N sees:

- The pre-batch snapshot, PLUS
- The cumulative effects of any writes at positions 1..N-1 within the
  same batch.

This is the natural reading of strict-ordered + atomic-write-commit:
the batch is one transaction; within it, each op sees the
transaction's accumulated state.

**Result binding** — using the value from a Match in a later Mutate
— is **not** supported. Frames are not procedural in the
variable-binding sense. Each op's payload is self-contained. If a
later op needs to react conditionally to a prior op's result, the
agent uses:

- **The expected-state pre-condition pattern** (per
  `sema-engine::MutateOperation`'s existing `expected_rev` field):
  the Mutate carries a pre-condition; if state changed, the Mutate
  fails and the batch aborts.
- **A separate Validate op** that fails when a condition isn't met:
  `[Match X, Validate (assert X.value > 5), Mutate ...]` — the
  Validate checks the condition; failure aborts the batch.

This is cleaner than result binding for two reasons. (a) No need to
extend the wire grammar with variables. (b) The
constraint-check-and-mutate logic stays expressible via existing
typed records, not via a new procedural sub-language.

### 1.6 · Reply outcome names — completion, not commit ✓ (with the refinement from DA's second round below)

the prior draft had `BatchOutcome::Committed` which doesn't fit pure
Match/Validate/Subscribe frames. Fix:

```rust
pub enum BatchOutcome {
    /// All ops completed successfully. For writes: committed.
    /// For reads: observed the snapshot. For validates: passed.
    /// For subscribes: opened. For mixed: each op completed in
    /// its mode.
    Completed,

    /// An op at the given position failed; the batch was aborted.
    /// Writes that would have committed did not. Subscribes that
    /// would have opened did not. Per-op replies say which is which.
    Aborted {
        failed_at: usize,
        reason: BatchFailureReason,
    },
}
```

Per-op detail lives in the `SubReply` — a **typed sum**, not a
status-flag-plus-Option-payload (per
`skills/typed-records-over-flags.md` and DA's review of `/177`'s
draft shape, which would have permitted invalid states like `Ok`
with `None` payload):

```rust
pub enum SubReply<ReplyPayload> {
    /// Op ran and committed/completed. Payload carries the result.
    /// Only emitted in BatchOutcome::Completed batches.
    Ok {
        verb: SignalVerb,         // echoed from request
        payload: ReplyPayload,    // mandatory — no Option, no invalid Ok-without-payload state
    },

    /// Op ran but the batch aborted. For writes: durable effects
    /// rolled back. For reads/validates: result observed speculative
    /// state and is no longer authoritative. No payload — the caller
    /// should re-issue if it still wants the value.
    RolledBack {
        verb: SignalVerb,
    },

    /// Op was attempted and failed; this is the cause of the batch
    /// abort. Exactly one op per aborted batch has this status, at
    /// BatchOutcome::Aborted::failed_at. May carry a typed detail
    /// payload describing the failure (e.g. ValidationFailureDetail).
    Failed {
        verb: SignalVerb,
        reason: SubFailureReason,
        detail: Option<ReplyPayload>,
    },

    /// Op was never attempted because an earlier op in the batch
    /// failed.
    Skipped {
        verb: SignalVerb,
    },
}
```

`Completed` + `Ok` per op = clean reads / clean writes / clean
subscribes / clean validates.

`Aborted` + per-op `Skipped`/`Failed`/`RolledBack` = the failure
case, with the exact position and reason recorded.

The typed-sum shape makes illegal combinations unrepresentable:
`Ok` requires a payload; `RolledBack`/`Skipped` have no payload
field at all; `Failed` carries optional detail.

---

### 1.7 · DA's second round (after a draft of this report)

After §1.1–§1.6 were drafted, DA reviewed the draft and flagged five
further design issues. All five are folded into the spec below; the
findings are restated here for completeness:

- **Subscription batching coherence** — subscribes are external
  ongoing side effects; rolling back a stream-open is awkward. The
  spec now requires Subscribes to come last in a batch (per §4
  composition rules and §8.1 worked example). A Subscribe in the
  middle of a batch is rejected at receive-time as
  `BatchFailureReason::SubscribeOutOfOrder`.
- **Aborted-batch speculative-read leak** — read-your-own-writes
  with strict ordering means a Match can observe writes that later
  get rolled back. The spec now requires `Status::RolledBack` to
  cover both rolled-back writes *and* invalidated reads, with
  `payload: None` in both cases (per §1.6's refined SubStatus and
  its invariants block).
- **Non-empty batch invariant** — `Vec<Op>` allows empty batches
  with no semantics. The spec now uses `NonEmpty<Op>` to encode
  non-emptiness at the type level (per §2's signal-core block).
- **No-result-binding example contradiction** — the prior draft's example
  used a Match's result in a later Mutate's pre-condition, silently
  violating the no-result-binding rule. Fixed in §6 — the Match is
  for the caller's read; the Mutate's pre-condition is self-contained;
  the conditional logic lives in a Validate that runs its own typed
  predicate.
- **Handshake duplication** — the prior draft put handshake variants on both
  FrameBody and Reply. The spec now keeps them on FrameBody only;
  `Reply` has no Handshake variant (per §2's signal-core block).

All five settlements are structural; none should change the
implementation work an operator picks up from this spec.

### 1.8 · DA's third round (precision edits)

After the §1.7 settlements landed, DA reviewed the revised draft and
flagged five further precision issues. All are folded into the spec
below; the findings are restated for completeness:

- **`BatchFailureReason::SubscribeOutOfOrder` was referenced but not
  defined.** The enum in §2 now lists it as a fifth variant alongside
  `OpRejected` / `PolicyViolation` / `ValidationFailed` / `Internal`.
- **Subscription opens need an explicit two-phase rule.** §4.1 now
  states the validate-phase + commit-phase protocol: every Subscribe
  is validated before *any* stream opens; only if all preceding ops
  succeed AND all Subscribe-validations pass do all streams open
  atomically. Rolling back a stream-open isn't coherent (the client
  has already consumed events), so the receiver must never half-open.
- **Receiver-side verb-validation API for the multi-op shape.** §2
  now specifies a two-method API (per `/176 §2.2`'s correction):
  `Request::validate(&self) -> Result<(), BatchVerbMismatch>` plus
  `Request::into_checked(self) -> Result<CheckedRequest, (BatchVerbMismatch,
  Self)>`. The borrow-based validator lets receivers build rejection
  replies with the original request's context; the consuming
  `into_checked` returns the unconverted request on failure for the
  same reason. Replaces today's single-op `into_payload_checked`.
- **Stale "Subscribe + writes forbidden" sentence**. The note
  contradicting the table immediately above it has been removed; the
  composition rule is now consistently "Subscribes must come last."
- **`signal_channel!` needs a no-intent path.** §3.0 introduces
  `NoIntent` as an uninhabited enum; §3.1 shows the two macro forms
  (with `intent` block / without). Contracts that have no named
  batches drop the `with intent X` clause and the `intent X { ... }`
  block; the macro substitutes `NoIntent` automatically, and the
  type system guarantees no `Named` header can be constructed for
  that channel.

---

### 1.9 · Historical review round, now absorbed by DA/61 and DA/62

After the §1.8 settlements landed and a corrections-companion
report was drafted, three further reviews surfaced more issues —
all design-level, none migration-shaped (the user explicitly rules
out migration concerns from design judgment).

- **Default type parameters on methods are not legal Rust.** An
  earlier draft of the validate API used
  `validate<Policy: BatchPolicy<P, I> = DefaultPolicy>(...)`, which
  Rust forbids: defaults apply to `struct` / `enum` / `type` /
  `trait` generics, not function or method generics. The spec
  below now uses four explicit methods (`validate`,
  `validate_with_policy::<Policy>`, `into_checked`,
  `into_checked_with_policy::<Policy>`), with the no-suffix forms
  delegating to `DefaultPolicy` internally.
- **`SubReply` typed sum instead of struct + Option payload.** An
  earlier draft used `SubReply { verb, status: SubStatus, payload:
  Option<R> }` with the status-payload invariants documented as
  prose comments. The typed sum below (`Ok { verb, payload: R }` /
  `RolledBack { verb }` / `Failed { verb, reason, detail:
  Option<R> }` / `Skipped { verb }`) makes the invariants
  unrepresentable; per `skills/typed-records-over-flags.md`,
  status-plus-Option is the anti-pattern; the variant form is the
  fix.
- **`NonEmpty<T>` codec impls now specified.** The historical review
  round flagged that rkyv + NOTA codec impls for `NonEmpty<T>` weren't
  named. The `NonEmpty<T>` definition in §2 now carries the rkyv derive
  note and the hand-written NOTA decoder specification.
- **`SubscriptionToken` shape is still pending the user.** Per
  operator-assistant/113 §13 Q3 and reaffirmed by /114 §4.3.
  Surfaced in §7 Q5 below; needs decision before subscription-
  bearing channels can compile.
- **Handshake/Reply cascade.** Today's `signal-core::Reply<Payload>`
  has `Handshake + Operation` variants; the corrected shape moves
  handshakes exclusively to `FrameBody` and makes `Reply` batch-only
  (`Reply::Batch { header, outcome, per_op }`). Every existing
  reply construction site changes — not just request construction.
  Operator pickup affects:

  - `Reply::handshake(reply)` constructor removed from `Reply`;
    handshake replies build `FrameBody::HandshakeReply(reply)`
    directly.
  - Every contract reply path (today
    `Reply::operation(payload)`) becomes
    `Reply::Batch { header, outcome, per_op }`.
  - Every handshake round-trip test currently asserting
    `Reply::Handshake` shape is replaced with
    `FrameBody::HandshakeReply` shape.
  - Same applies to `Request<Payload>::Handshake` → moves to
    `FrameBody::HandshakeRequest`.

  Workspace-wide cascade, but mechanical. Plan for it in wave 1.

### 1.10 · Async-first correction (DA/61 round)

After §1.9 landed, the user pushed back on the `correlation: Option<CorrelationId>`
field that the spec had been carrying. Working through the question —
*why does the protocol need a correlation ID at all?* — revealed the
spec had been muddling three different concerns under one wrapper:

- **Transport request/reply matching** (which reply belongs to which
  request).
- **Audit / workflow naming** (this batch is part of "RoleHandoff").
- **Cross-component trace ID** (observability across daemons).

The earlier `RequestHeader<Intent>` shape conflated all three. DA/61
keeps the clean separation and sharpens the request/reply-matching
answer: **the protocol is async, the matching scheme is a deterministic
id grammar negotiated at handshake**, not a free-form client-chosen
string.

The shape that lands:

- `signal-core` drops `Intent` as a type parameter on `Request` /
  `Reply` / `Frame`. Domain "intent" (`RoleHandoff`, etc.) belongs
  in domain payloads, not in transport wrappers. Audit labels wait
  for tracing.
- `signal-core` drops `CorrelationId`. The request/reply matching
  key is `ExchangeIdentifier = (session_epoch, lane, sequence)`,
  established at handshake, monotonic within a lane, sender-minted
  but not sender-chosen (lane + sequence are deterministic from
  shared connection state).
- Each side owns one outbound lane; sequences are monotonic within
  a lane; `session_epoch` lets reconnect cleanly reset.
- `ExchangeIdentifier` lives on `FrameBody::Request` /
  `FrameBody::Reply` variants — handshake frames don't carry one.
- Subscription events ride on their own `FrameBody::SubscriptionEvent`
  variant (the daemon's outbound lane), addressed by
  `SubscriptionToken` plus a monotonic sequence for resume-on-reconnect.

§2 below carries the corrected primitives. The protocol becomes:

> Signal is async request/reply over a negotiated connection. A
> request is one or more verb-tagged operations. Each request opens
> one exchange identified by the sender's lane and monotonic
> sequence. The reply closes that exchange by echoing the same
> identifier. Subscription events flow on the daemon's lane,
> addressed by subscription token. Trace/audit metadata, when added,
> lives in a separate frame-level field — not in payloads, not in
> the exchange id.

---

## 2 · The corrected design — `signal-core` primitives

Async-first per DA/61. `Intent` is gone. `CorrelationId` is gone.
`RequestHeader<Intent>` / `ReplyHeader<Intent>` are gone. The shape
that lands:

```rust
// signal-core/src/verb.rs
pub enum SignalVerb {
    Assert,
    Mutate,
    Retract,
    Match,
    Subscribe,
    Validate,
}

// signal-core/src/exchange.rs
//
// The negotiated exchange grammar. The handshake establishes
// session_epoch + which lane each side owns; per-message ids are
// then derived monotonically by each sender from its own lane.
// No party invents a global id; no party negotiates per message.
pub struct SessionEpoch(u64);

pub enum ExchangeLane {
    Connector,   // the side that opened the connection
    Acceptor,    // the side that accepted
}

pub struct ExchangeSequence(u64);

pub struct ExchangeIdentifier {
    pub session_epoch: SessionEpoch,
    pub lane: ExchangeLane,
    pub sequence: ExchangeSequence,
}

pub enum ExchangeMode {
    LaneSequence {
        session_epoch: SessionEpoch,
        connector_lane: ExchangeLane,   // by convention, Connector
        acceptor_lane: ExchangeLane,    // by convention, Acceptor
    },
    // Future modes (e.g. cryptographic-derivation chain for network
    // components) get their own enum variants. Local IPC uses
    // LaneSequence.
}

// signal-core/src/operation.rs
pub struct Operation<Payload> {
    pub verb: SignalVerb,
    pub payload: Payload,
}

/// A non-empty sequence — guaranteed at the type level. Empty
/// batches have no semantics; the type rules them out at
/// construction.
///
/// rkyv codec: derive `Archive + check_bytes`; the `head: T`
/// field guarantees non-emptiness structurally.
///
/// NOTA codec: hand-written `NotaDecode` in signal-core that
/// consumes `[item item ...]`, errors on empty with
/// `NotaCodecError::EmptyNonEmpty`, and splits head/tail.
pub struct NonEmpty<T> {
    head: T,
    tail: Vec<T>,
}

// signal-core/src/request.rs
pub struct Request<Payload> {
    pub operations: NonEmpty<Operation<Payload>>,
}

// signal-core/src/reply.rs
pub struct Reply<ReplyPayload> {
    pub outcome: RequestOutcome,
    pub per_operation: NonEmpty<SubReply<ReplyPayload>>,
}

pub enum RequestOutcome {
    /// All operations completed/committed. Per-op `SubReply` carries
    /// the per-verb result.
    Completed,
    /// An op at position `failed_at` failed; the batch was aborted.
    /// Writes that would have committed did not. Subscribes that
    /// would have opened did not. Per-op replies say which.
    Aborted {
        failed_at: usize,
        reason: RequestFailureReason,
    },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum RequestFailureReason {
    /// The op at `failed_at` was rejected by the receiver.
    OpRejected,
    /// The request violated a receive-time check (verb/payload
    /// mismatch, Subscribe-out-of-order, etc.).
    PolicyViolation,
    /// The channel-declared `BatchPolicy` rejected the request.
    BatchPolicyViolation { rule: &'static str, limit: usize },
    /// A Subscribe was not at the tail (universal rule, fires at
    /// receive time before any op runs).
    SubscribeOutOfOrder,
    /// A `Validate` op at `failed_at` failed.
    ValidationFailed,
    /// A receiver-internal error.
    Internal,
}

/// Per-op reply — a typed sum (makes illegal states unrepresentable).
pub enum SubReply<ReplyPayload> {
    /// Op ran and committed/completed.
    Ok { verb: SignalVerb, payload: ReplyPayload },
    /// Op ran inside a request that subsequently aborted. Writes
    /// rolled back; read/validate results no longer authoritative.
    RolledBack { verb: SignalVerb },
    /// Op was attempted and failed; this is the cause of the abort.
    Failed {
        verb: SignalVerb,
        reason: SubFailureReason,
        detail: Option<ReplyPayload>,
    },
    /// Op never ran because an earlier op failed.
    Skipped { verb: SignalVerb },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum SubFailureReason {
    SignalVerbMismatch,
    PreconditionFailed,
    ValidationFailed,
    DomainRejection,
}

// signal-core/src/frame.rs
//
// Handshake variants don't carry an `ExchangeIdentifier` — the
// exchange grammar is what the handshake establishes. Request /
// Reply / SubscriptionEvent variants carry it.
pub enum FrameBody<RequestPayload, ReplyPayload> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request {
        exchange: ExchangeIdentifier,
        request: Request<RequestPayload>,
    },
    Reply {
        exchange: ExchangeIdentifier,
        reply: Reply<ReplyPayload>,
    },
    /// Daemon-initiated subscription event. Rides on the daemon's
    /// outbound lane (Acceptor) with its own monotonic sequence. The
    /// `SubscriptionTokenInner` demuxes to the subscriber that
    /// requested the stream; the `sequence` in `ExchangeIdentifier`
    /// gives the client a "resume from N+1" capability on reconnect.
    SubscriptionEvent {
        exchange: ExchangeIdentifier,
        token: SubscriptionTokenInner,
        event: ReplyPayload,
    },
}

pub struct Frame<RequestPayload, ReplyPayload> {
    pub body: FrameBody<RequestPayload, ReplyPayload>,
}

// signal-core/src/subscription.rs
//
// Per /177 §7 Q5: opaque u64 inner; each subscription-bearing
// channel declares its own typed wrapper plus a per-channel
// `Retract SubscriptionRetraction(<Channel>SubscriptionToken)`
// variant.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent,
         Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SubscriptionTokenInner(u64);
```

### 2.1 · Validation API — `validate` / `into_checked`

Four explicit methods. The default-policy convenience methods
delegate to the policy-typed methods internally; Rust forbids
default type parameters on methods, so the explicit pair is the
only legal shape:

```rust
impl<Payload> Request<Payload>
where
    Payload: RequestPayload,
{
    /// Validate without consuming. Universal rules + `DefaultPolicy`.
    /// Universal rules: per-op verb/payload alignment via
    /// `RequestPayload::signal_verb()`, Subscribe-must-be-last
    /// position check, NonEmpty (type-enforced).
    pub fn validate(&self) -> Result<(), RequestVerbMismatch> {
        self.validate_with_policy::<DefaultPolicy>()
    }

    /// Same with an explicit channel policy.
    pub fn validate_with_policy<Policy>(&self)
        -> Result<(), RequestVerbMismatch>
    where
        Policy: BatchPolicy<Payload>,
    { /* universal + policy */ }

    /// Consume on success; return `(Err, Self)` on failure so the
    /// receiver can build the rejection reply.
    pub fn into_checked(self)
        -> Result<CheckedRequest<Payload>, (RequestVerbMismatch, Self)>
    {
        self.into_checked_with_policy::<DefaultPolicy>()
    }

    /// Same with an explicit channel policy.
    pub fn into_checked_with_policy<Policy>(self)
        -> Result<CheckedRequest<Payload>, (RequestVerbMismatch, Self)>
    where
        Policy: BatchPolicy<Payload>,
    {
        if let Err(reason) = self.validate_with_policy::<Policy>() {
            return Err((reason, self));
        }
        Ok(CheckedRequest { operations: self.operations })
    }
}

pub enum RequestVerbMismatch {
    OpMismatch { index: usize, expected: SignalVerb, got: SignalVerb },
    SubscribeOutOfOrder { index: usize },
    PolicyViolation { rule: &'static str, limit: usize },
}

pub struct CheckedRequest<Payload> {
    pub operations: NonEmpty<Operation<Payload>>,
}
```

### 2.2 · `BatchPolicy` — channel-declared rules

Declarative-only. No closures, no runtime expressions (those would
violate `skills/contract-repo.md`'s "contracts own typed records,
not validation pipelines" discipline).

```rust
pub trait BatchPolicy<Payload>
where
    Payload: RequestPayload,
{
    fn max_ops() -> usize { usize::MAX }
    fn allow_mixed_read_write() -> bool { true }
    fn forbid_subscribe() -> bool { false }
    fn forbid_validate() -> bool { false }
}

pub struct DefaultPolicy;
impl<P> BatchPolicy<P> for DefaultPolicy where P: RequestPayload {}
```

The channel's macro emits a per-channel unit struct that
implements `BatchPolicy` from an optional `batch_policy { ... }`
block. Channels without the block use `DefaultPolicy`.

### 2.3 · Exchange correctness rules

Sender-side (per DA/61):

- Maintain `next_outgoing_sequence` for own lane.
- Assign the next sequence before writing a request frame.
- Insert the exchange into the pending map.
- Remove the pending exchange when its reply arrives.

Receiver-side:

- Reject a request whose lane is not the peer's outbound lane.
- Reject a repeated `(lane, sequence)` request while the prior
  exchange is still open.
- Process requests independently (under actor backpressure).
- Reply with the exact exchange identifier from the request.

Reply-side:

- Reject a reply whose exchange is not pending.
- Reject duplicate replies for a closed exchange.
- Route the reply by exchange id to the waiting requester.

Failure semantics: unknown-exchange reply, wrong-lane request,
duplicate open exchange = protocol error (drop connection or
escalate). Out-of-order replies are normal.

---

## 3 · The corrected design — `signal_channel!` macro

After the async-first correction in §1.10 / §2, the macro
contract simplifies. No `with intent <T>` clause. No `intent <T>
{ ... }` block. No `NoIntent` substitution. No `<IntentName>`
type emissions.

```rust
signal_channel! {
    request MindRequest {
        Assert SubmitThought(SubmitThought),
        Mutate StatusChange(StatusChange),
        Retract RoleRelease(RoleRelease),
        Match QueryThoughts(QueryThoughts),
        Subscribe SubscribeThoughts(SubscribeThoughtsRequest),
        Retract SubscriptionRetraction(MindSubscriptionToken),
        Validate ValidateProposal(Proposal),
    }
    reply MindReply {
        Thought(ThoughtSummary),
        Status(ActivityAck),
        Released(RoleReleaseAck),
        ThoughtList(Vec<Thought>),
        SubscriptionOpened(SubscriptionOpenedAck),
        ValidationPassed(ValidationReceipt),
    }
    // Optional, channels with policy pressure:
    // batch_policy { max_ops: 32, forbid_subscribe: false, ... }
}
```

Macro emissions:

- `pub enum MindRequest { ... }` and `pub enum MindReply { ... }`
  with rkyv + NOTA derives.
- `pub enum MindRequestKind` (unit-only projection of MindRequest
  variants) auto-generated, plus `impl MindRequest { fn kind(&self)
  -> MindRequestKind }`.
- `impl RequestPayload for MindRequest` with the verb-mapping
  match.
- `pub type Frame = signal_core::Frame<MindRequest, MindReply>;`
  — no `Intent` type parameter; the frame is two-axis.
- `pub type FrameBody = signal_core::FrameBody<MindRequest, MindReply>;`
- `pub type ChannelRequest = signal_core::Request<MindRequest>;`
- `pub type ChannelReply = signal_core::Reply<MindReply>;`
- `pub type ChannelBuilder = signal_core::BatchBuilder<MindRequest>;`
- Per-variant `From<Payload>` impls (request + reply).
- Per-channel `BatchPolicy` unit struct impl (or `DefaultPolicy`
  if no `batch_policy` block).
- NOTA codec impls on the payload enums.

The full spec for the macro lives in the companion macro-redesign
report.

## 4 · Composition rules (now precise)

Strict-ordered execution + read-your-own-writes gives clean
semantics for every verb mix:

| Frame contents | Behaviour |
|---|---|
| All Assert/Mutate/Retract (pure writes) | All-or-nothing atomic commit. Each write sees prior writes' effects. First failure aborts at `failed_at`; subsequent ops are `Skipped`. |
| All Match (pure reads) | All reads observe one shared snapshot. Failure of one op aborts; others are `Skipped`. |
| All Subscribe | All Subscribes open at the shared snapshot. First failure aborts the batch and no streams open. |
| All Validate | All validates dry-run against the shared snapshot. First failure aborts. |
| Validate + writes | Strict-ordered: a Validate at position N sees the cumulative state including writes at 1..N-1. The preflight pattern (Validates first) works; the checkpoint pattern (Validates after writes) also works. |
| Match + writes | Strict-ordered: a Match at position N reads cumulative state including writes at 1..N-1. The SQL `SELECT FOR UPDATE` pattern works; result binding (using a Match's result in a later op) does not — see §5 and §10.4 below. |
| Subscribe + any non-Subscribe op | **Subscribes must come last in the batch.** All non-Subscribe ops execute first in strict order; if any fails, the batch aborts and no streams open. If all succeed, writes commit and subscribes open at the post-commit snapshot. A Subscribe in the middle of a batch is rejected at receive-time as `BatchFailureReason::SubscribeOutOfOrder`. |

### 4.1 · Staged subscription open (the two-phase rule)

A Subscribe is an external ongoing side-effect: once a stream is
open, the client is consuming it. Rolling back a stream-open is
incoherent (the client may have already received events). The
receiver therefore opens subscriptions in **two explicit phases**:

1. **Validate phase.** For every Subscribe in the batch, the receiver
   verifies the subscription is acceptable: the filter type-checks,
   the requested resource exists, the requester has the right to
   subscribe, the receiver has capacity. **No streams open yet.**

2. **Commit phase.** If (a) the validate phase passed for every
   Subscribe, AND (b) every preceding non-Subscribe op completed
   successfully (writes committed atomically, reads observed the
   snapshot, validates passed), THEN the receiver opens all Subscribe
   streams in one atomic step. Each gets its `SubscriptionToken` in
   the `SubReply` payload.

If either phase fails, the batch aborts and **zero streams open**.
Per-op statuses for the Subscribes are `RolledBack` (if validation
passed but a later non-Subscribe op failed in commit phase) or
`Failed`/`Skipped` (if a Subscribe's own validation failed).

The two-phase rule applies to *all-Subscribe* batches as well:
validate all subscriptions, then open all atomically. A failing
validation at position K aborts the batch with positions 0..K-1
having status `RolledBack` (validation passed but commit was
abandoned) and position K having status `Failed`.

This is the analog of two-phase commit for stream-opens. It's
necessary because stream-open is the one side-effect that can't be
rolled back once it lands.

---

## 5 · Sema-engine commit-log shape (corrected)

Today: one `OperationLogEntry { snapshot, verb: SignalVerb::Atomic,
table, .. }` per atomic batch. After collapse:

```rust
pub struct CommitLogEntry {
    pub snapshot: SnapshotId,
    pub intent: Option<SerializedIntent>,    // serialized typed intent for cross-domain audit
    pub correlation: Option<CorrelationId>,
    pub op_count: usize,
    pub ops: Vec<OpLogDetail>,
}

pub struct OpLogDetail {
    pub verb: SignalVerb,                    // per-op
    pub table: TableName,
    pub effect: DeltaKind,                   // Assert / Mutate / Retract (Match/Subscribe/Validate don't write)
    pub key: SerializedKey,
}
```

The log is now richer than today — every batch shows its intent and
per-op detail. Audit queries reconstruct the logical transaction.

Two flavors of log entry exist:

- **Write-bearing entries** (`CommitLogEntry` above) — for batches
  that committed at least one write.
- **Read/subscribe/validate-only entries** — for batches that didn't
  commit. These can be omitted from the durable log entirely
  (they're not durable state changes), or kept in a separate
  read-audit log if read-trace is needed.

Default: only commit-bearing batches are durably logged.

---

## 6 · CLI surface (the NOTA grammar)

After the async-first correction, the wire grammar simplifies.
No `(Batch ...)` wrapper. No `(Anonymous)` / `(Tracked ...)` /
`(Named ...)` header. The exchange identifier is transport
plumbing (`ExchangeIdentifier` on the frame), invisible to the
human typing into the CLI:

```sh
# Single-op (the common case):
mind '(Assert (SubmitThought (...)))'

# Multi-op (when several ops must commit atomically):
mind '[(Retract (RoleClaim (role Designer)))
       (Assert (RoleClaim (role Poet)))]'

# Mixed validate + writes (Validate first; if it fails, no writes commit):
mind '[(Validate (Integrity (table thoughts)))
       (Mutate (Catalog (table thoughts) (status Active)))]'

# Mixed Match + writes (Match reads at the request snapshot; the
# Mutate carries its own pre-condition via expected_rev — no
# result binding from Match):
mind '[(Match (ClaimSnapshot (role Designer)))
       (Validate (ExpectedRevision (key Designer) (revision 5)))
       (Mutate (RoleClaim (role Designer) (expected_rev 5)))]'

# Subscribe (one-op; opens a stream on the daemon's lane):
mind '(Subscribe (ThoughtFilter (kind Decision)))'

# Subscribe + writes (writes commit; then subscribe opens at the
# post-commit snapshot; Subscribes must come last):
mind '[(Mutate (Catalog (table thoughts) (status Active)))
       (Subscribe (ThoughtFilter (kind Decision)))]'
```

The `[ ... ]` sequence brackets are the **structural** marker of a
multi-op atomic request. No keyword, no `Batch` wrapper. The
single-op `(Verb ...)` form is sugar for a one-op request; the
CLI parser desugars to a length-1 `NonEmpty<Operation>`
internally.

The `ExchangeIdentifier` lives on the frame at the transport layer
— the CLI client mints the next sequence on the
`Connector`-lane when it sends; replies arrive with the same
exchange echoed. Users don't type the identifier.

## 7 · What's still open

The present spec settles most of the prior draft's open questions. What
remains:

### Q1 — Per-receiver batch policy overrides

The default policy of §4 covers the common cases. A contract that
needs stricter rules (e.g., refusing mixed read+write because its
storage backend can't serve consistent reads) declares so in its
`signal_channel!` invocation. Macro syntax for batch-policy
overrides is not yet specified.

### Q2 — Frame-size limits

How many ops per batch? How many bytes per frame? Defaults likely
~256 ops per batch and ~1 MiB per frame, with per-receiver overrides
via batch policy.

### Q3 — Cross-component sequences

A frame targets one component. Cross-component logical transactions
(e.g., a `persona-router` channel-grant linked to a `persona-mind`
adjudication record) happen as separate frames coordinated through
mind adjudication. Same answer as today; restated.

### Q4 — Correlation ID lifecycle

A correlation id is generated at the originating frame; echoed in
all replies; carried in follow-up frames that logically continue the
same conversation. TTL-based garbage collection. Spec doesn't pin
down details beyond the generation/echo rule.

### Q5 — `SubscriptionToken` shape — *settled 2026-05-15*

Per operator-assistant/113 §13 Q3 and reaffirmed by operator-
assistant/114 §4.3. User settled the three sub-decisions:

- **(a) Field type**: opaque `u64` counter.
- **(b) Scope**: per-channel typed — each contract declares its own
  `<Channel>SubscriptionToken` newtype around `u64`.
- **(c) Retraction shape**: per-channel `Retract
  SubscriptionRetraction(<Channel>SubscriptionToken)` variant on
  every channel that supports subscription cancellation.

The signal-core primitive provides the `u64` newtype wrapper for
contracts to alias:

```rust
// signal-core/src/subscription.rs
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent,
         Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SubscriptionTokenInner(u64);

impl SubscriptionTokenInner {
    pub const fn new(value: u64) -> Self { Self(value) }
    pub const fn into_u64(self) -> u64 { self.0 }
}
```

Each contract that supports subscriptions declares a typed wrapper:

```rust
// signal-persona-mind:
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent,
         Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct MindSubscriptionToken(SubscriptionTokenInner);
```

And one `Retract` variant per subscribe-supporting channel:

```rust
signal_channel! {
    request MindRequest with intent MindBatchIntent {
        // ...
        Subscribe SubscribeThoughts(SubscribeThoughtsRequest),
        Subscribe SubscribeRelations(SubscribeRelationsRequest),
        Retract  SubscriptionRetraction(MindSubscriptionToken),
        // ...
    }
}
```

Subscription replies carry the token:

```rust
reply MindReply {
    // ...
    SubscriptionOpened(MindSubscriptionOpened),
    // ...
}

#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord,
         Debug, Clone, PartialEq, Eq)]
pub struct MindSubscriptionOpened {
    pub token: MindSubscriptionToken,
    pub kind: MindSubscriptionKind,    // Thoughts | Relations | ...
}
```

The per-channel typed wrapping prevents accidental cross-channel
retraction (you can't pass a `TerminalSubscriptionToken` to
`MindRequest::SubscriptionRetraction`); the `u64` inside keeps the
storage compact; each channel mints its own monotonic counter.

---

## 8 · Worked examples

Two scenarios that exercise the spec end-to-end.

### 8.1 · Subscribe-in-batch policy: Subscribes must come last

```sh
# Allowed: Subscribe-only request
mind '[(Subscribe (ThoughtFilter (kind Decision)))
       (Subscribe (RoleFilter (role designer)))]'
# Both subscribes open in the two-phase staged-open (per §4.1).

# Allowed: non-Subscribe ops followed by Subscribes
mind '[(Mutate (Catalog (table thoughts) (status Active)))
       (Subscribe (ThoughtFilter (kind Decision)))]'
# Mutate executes first; if it commits, Subscribe opens at
# post-commit snapshot. If Mutate fails, Subscribe never opens.

# Rejected at receive: Subscribe in the middle
mind '[(Subscribe (ThoughtFilter (...)))
       (Assert (SubmitThought (...)))]'
# → Reply { outcome: Aborted { failed_at: 0, reason: SubscribeOutOfOrder }, ... }
```

Rationale: a subscription is an external ongoing side-effect; once
a stream opens, the client has events. Rolling back a stream-open
is incoherent. Forcing Subscribes to the end collapses both edge
cases (partial open, post-fail stream) into "subscribes only open
after everything else succeeds."

### 8.2 · Failure-reply shape in a mixed validate-write request

**Request (schema-upgrade pattern, checkpoint Validate fails)**:

```sh
mind '[(Mutate (Catalog (table thoughts) (status Migrating)))    ; op 0
       (Mutate (Row 1 (new-shape ...)))                           ; op 1
       (Mutate (Row 2 (new-shape ...)))                           ; op 2
       (Validate (Integrity (table thoughts)))                    ; op 3 — fails
       (Mutate (Catalog (table thoughts) (status Active)))]'      ; op 4
```

**Reply**:

```rust
Reply {
    outcome: RequestOutcome::Aborted {
        failed_at: 3,                            // the Validate that failed
        reason: RequestFailureReason::ValidationFailed,
    },
    per_operation: NonEmpty::from(vec![
        // op 0..2: ran, committed, then rolled back when the batch aborted
        SubReply::RolledBack { verb: SignalVerb::Mutate },
        SubReply::RolledBack { verb: SignalVerb::Mutate },
        SubReply::RolledBack { verb: SignalVerb::Mutate },
        // op 3: the failure. Payload carries the validate's detail
        SubReply::Failed {
            verb: SignalVerb::Validate,
            reason: SubFailureReason::ValidationFailed,
            detail: Some(MindReply::ValidationDetail(integrity_check_failure)),
        },
        // op 4: never ran
        SubReply::Skipped { verb: SignalVerb::Mutate },
    ]),
}
```

The reply carries everything the caller needs: the batch-level
reason (`ValidationFailed` at position 3), the validate's specific
detail in op 3's payload, and the status of every other op
(`RolledBack` for ops that ran-then-undone, `Skipped` for op that
never ran). The typed-sum `SubReply` makes "Ok with no payload"
or "Skipped with payload" structurally impossible.

The `ExchangeIdentifier` on the frame echoes the request's
identifier; the caller routes the reply back to whoever was
waiting on that exchange.

## 9 · See also

- the macro-redesign companion in this directory — the macro shape
  over these primitives.
- `~/primary/reports/designer-assistant/61-signal-redesign-current-spec.md`
  — compact current Signal protocol spec.
- `~/primary/reports/designer-assistant/62-signal-redesign-implementation-brief.md`
  — implementation ordering and witnesses.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs` — what
  this spec replaces.
- `/git/github.com/LiGoldragon/signal-core/src/reply.rs` — what
  this spec replaces.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  macro implementation this spec replaces.
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the upstream
  discipline this spec encodes.
- `/git/github.com/LiGoldragon/sema-engine/src/engine.rs` — the
  commit-log shape that changes per §5.
- `~/primary/reports/designer/163-seven-verbs-no-structure-eighth.md`
  — the closed-boundary discipline that rules out
  `Custom(String)` in §1.2.
