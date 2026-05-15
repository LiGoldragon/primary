# 177 — Typed `Request<Payload>` and execution semantics

*Designer spec, 2026-05-15. Compact current-state record after the
async-first correction (DA/60), consolidating the iteration chain
into one self-contained spec. Companion to `/176` (the
`signal_channel!` macro spec). Aligns with
`reports/designer-assistant/61-signal-redesign-current-spec.md` and
`reports/designer-assistant/62-signal-redesign-implementation-brief.md`.*

**Retires when**: signal-core lands wave 1 against this spec; the
substance migrates to `signal-core/ARCHITECTURE.md`.

---

## 0 · TL;DR

> Signal is async request/reply over a negotiated connection. A
> request is one or more verb-tagged domain operations. Each request
> opens one exchange identified by the sender's negotiated lane and
> monotonic sequence. The reply closes that exchange by echoing the
> same exchange identifier. Subscription events flow on the daemon's
> own lane, addressed by `SubscriptionToken`. No transport metadata
> is payload. No audit label is payload unless the audit label is
> itself the domain object being asserted or mutated.

Six verbs (no `Atomic`). Atomicity is structural — the
`NonEmpty<Operation>` sequence in a request commits as a unit.
Request/reply matching is per-frame `ExchangeIdentifier` derived
from shared handshake state, not client-chosen correlation strings.

---

## 1 · Layer split

| Layer | Owns | Does not own |
|---|---|---|
| Signal verb | `Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`, `Validate` | Transport, audit labels |
| Domain payload | The typed noun the verb acts on | Exchange ids, trace ids, correlation ids |
| Request container | `NonEmpty<Operation<Payload>>`; atomic multi-op boundary | Workflow labels, reply routing |
| Frame exchange | Async request/reply matching: lane + sequence, negotiated at handshake | Domain meaning |
| Trace/audit | Future introspection/log metadata | Request/reply correctness |

---

## 2 · `signal-core` primitives

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

// signal-core/src/non_empty.rs
//
// Non-empty by construction; empty Vecs cannot occur. rkyv: derive
// Archive + check_bytes; the `head: T` field guarantees non-emptiness
// structurally. NOTA: hand-written NotaDecode that consumes
// `[item item ...]`, errors on empty with NotaCodecError::EmptyNonEmpty,
// splits into head + tail.
pub struct NonEmpty<T> {
    head: T,
    tail: Vec<T>,
}

// signal-core/src/operation.rs
pub struct Operation<Payload> {
    pub verb: SignalVerb,
    pub payload: Payload,
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
    /// An op at position `failed_at` failed; the request was aborted.
    /// Writes that would have committed did not. Subscribes that
    /// would have opened did not.
    Aborted {
        failed_at: usize,
        reason: RequestFailureReason,
    },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum RequestFailureReason {
    /// The op at `failed_at` was rejected by the receiver.
    OpRejected,
    /// The request violated a universal rule (verb/payload mismatch,
    /// non-empty, etc.).
    PolicyViolation,
    /// The channel-declared static policy rejected the request.
    ChannelPolicyViolation { rule: &'static str, limit: usize },
    /// A Subscribe was not at the tail (universal rule; fires at
    /// receive time before any op runs).
    SubscribeOutOfOrder,
    /// A `Validate` op failed.
    ValidationFailed,
    /// Receiver-internal error.
    Internal,
}

/// Per-op reply — typed sum. Illegal states unrepresentable.
pub enum SubReply<ReplyPayload> {
    /// Op ran and committed/completed. Only emitted in
    /// RequestOutcome::Completed requests.
    Ok { verb: SignalVerb, payload: ReplyPayload },

    /// Op ran inside a request that subsequently aborted. For writes:
    /// durable effects rolled back. For reads/validates: result may
    /// have observed speculative state — no longer authoritative.
    /// (Open naming question — see §9 Q1.)
    RolledBack { verb: SignalVerb },

    /// Op was attempted and failed; this is the cause of the abort.
    /// Exactly one per aborted request, at failed_at.
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

// signal-core/src/subscription.rs
//
// Per-channel typed wrapper around this inner u64. Each subscription-
// bearing channel declares its own `<Channel>SubscriptionToken` newtype
// plus a `Retract SubscriptionRetraction(<Channel>SubscriptionToken)`
// variant. Tokens are monotonic per-channel; the channel mints.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent,
         Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SubscriptionTokenInner(u64);
```

---

## 3 · Frame and exchange types

The exchange id lives at the frame body, not in request payloads.
Handshake variants don't carry one — the exchange grammar is what
the handshake establishes.

```rust
// signal-core/src/exchange.rs
pub struct SessionEpoch(u64);
pub struct ExchangeSequence(u64);

pub enum ExchangeLane {
    Connector,   // the side that opened the connection
    Acceptor,    // the side that accepted
}

pub struct ExchangeIdentifier {
    pub session_epoch: SessionEpoch,
    pub lane: ExchangeLane,
    pub sequence: ExchangeSequence,
}

pub enum ExchangeMode {
    LaneSequence { session_epoch: SessionEpoch },
    // Future cryptographic-derivation modes for network components
    // get their own enum variants. Local IPC uses LaneSequence.
}

// signal-core/src/frame.rs
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
    /// Daemon-initiated subscription event. Rides on the acceptor's
    /// outbound lane with its own monotonic sequence. The
    /// `SubscriptionTokenInner` demuxes to the subscriber that
    /// requested the stream; the `sequence` in `ExchangeIdentifier`
    /// gives the client a "resume from N+1" capability on reconnect.
    /// (Open structural question — see §9 Q2.)
    SubscriptionEvent {
        exchange: ExchangeIdentifier,
        token: SubscriptionTokenInner,
        event: ReplyPayload,
    },
}

pub struct Frame<RequestPayload, ReplyPayload> {
    pub body: FrameBody<RequestPayload, ReplyPayload>,
}
```

---

## 4 · Exchange correctness rules

Sender-side:

- Maintain `next_outgoing_sequence` per local lane.
- Assign the next sequence before writing a Request frame.
- Insert the exchange into the pending map.
- Remove the pending exchange when its reply arrives.

Receiver-side:

- Reject a Request whose lane is not the peer's outbound lane.
- Reject a duplicate open `(lane, sequence)` Request while the prior
  exchange is still open.
- Process Requests independently (under actor backpressure).
- Reply with the exact `ExchangeIdentifier` from the Request.

Reply-side:

- Reject a Reply whose exchange is not pending.
- Reject duplicate Replies for a closed exchange.
- Route the Reply by exchange id to the waiting requester.

Failure modes: unknown-exchange Reply, wrong-lane Request, duplicate
open exchange — all protocol errors (drop connection, log). Out-of-
order Replies are normal.

---

## 5 · Validation API

Four explicit methods on `Request<Payload>` — no default type
parameters on generic methods (Rust forbids them). The
no-suffix forms delegate to `DefaultPolicy` internally.

```rust
impl<Payload> Request<Payload>
where
    Payload: RequestPayload,
{
    /// Universal rules + DefaultPolicy. Universal: per-op
    /// verb/payload alignment via RequestPayload::signal_verb(),
    /// Subscribe-must-be-last position, NonEmpty (type-enforced).
    pub fn check(&self) -> Result<(), RequestVerbMismatch> {
        self.check_with_policy::<DefaultPolicy>()
    }

    pub fn check_with_policy<Policy>(&self)
        -> Result<(), RequestVerbMismatch>
    where
        Policy: ChannelPolicy<Payload>,
    { /* universal + policy */ }

    pub fn into_checked(self)
        -> Result<CheckedRequest<Payload>, (RequestVerbMismatch, Self)>
    {
        self.into_checked_with_policy::<DefaultPolicy>()
    }

    pub fn into_checked_with_policy<Policy>(self)
        -> Result<CheckedRequest<Payload>, (RequestVerbMismatch, Self)>
    where
        Policy: ChannelPolicy<Payload>,
    {
        if let Err(reason) = self.check_with_policy::<Policy>() {
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

Method named `check` rather than `validate` to avoid confusion with
`SignalVerb::Validate` (the verb that means "dry-run an op against
rules"). The two are different things; the name change makes that
visible. (Open naming question — see §9 Q5.)

**`ChannelPolicy` trait** (channel-declared static rules, opt-in
per contract):

```rust
pub trait ChannelPolicy<Payload>
where Payload: RequestPayload,
{
    fn max_ops() -> usize { usize::MAX }
    fn allow_mixed_read_write() -> bool { true }
    fn forbid_subscribe() -> bool { false }
    fn forbid_validate() -> bool { false }
}

pub struct DefaultPolicy;
impl<P> ChannelPolicy<P> for DefaultPolicy where P: RequestPayload {}
```

Declarative only — no closures, no runtime expressions (those
violate `skills/contract-repo.md`). Custom runtime checks live in
daemon code, not in the contract.

---

## 6 · Composition rules

Strict-ordered execution + read-your-own-writes within a request:

| Frame contents | Behaviour |
|---|---|
| All Assert/Mutate/Retract | All-or-nothing atomic commit. Each write sees prior writes. First failure aborts at `failed_at`; subsequent ops are `Skipped`. |
| All Match | One snapshot; reads observe the cumulative pre-batch state. |
| All Subscribe | All open atomically in a two-phase staged-open (validate all, then commit-open all). If one validation fails, none open. |
| All Validate | Dry-run against the request-time snapshot. First failure aborts. |
| Validate + writes | Strict-ordered; Validate at position N sees cumulative writes 1..N-1. Preflight (Validates first) and checkpoint (Validates after) both work. |
| Match + writes | Strict-ordered; Match at position N sees cumulative writes 1..N-1. SQL SELECT-FOR-UPDATE pattern works. **No result binding** — Match's payload is for the caller's read; later ops carry their own pre-conditions (e.g., `expected_rev` on Mutate). |
| Subscribe + non-Subscribe | **Subscribes must come last in the request.** Non-Subscribe ops execute in strict order first; if any fails, no streams open. If all succeed, writes commit, then subscribes open at the post-commit snapshot. A Subscribe in the middle is rejected at receive-time as `RequestFailureReason::SubscribeOutOfOrder`. |

Subscribes use the **two-phase staged-open**: validate every
Subscribe first (filter type-checks, resource exists, requester
authorized, receiver has capacity); only if all pass and prior ops
commit do the streams open atomically. Otherwise zero streams
open. This handles the "external side-effect can't be rolled back"
problem — a subscription is the one side-effect with no
rollback.

---

## 7 · Sema-engine direction

Sema-engine moves in the same wave as signal-core. The
`SignalVerb::Atomic` usage retires; commits become structural.

```rust
pub struct CommitLogEntry {
    pub snapshot: SnapshotId,
    pub operation_count: usize,
    pub operations: NonEmpty<CommitLogOperation>,
}

pub struct CommitLogOperation {
    pub verb: SignalVerb, // Assert / Mutate / Retract for write effects
    pub table: TableName,
    pub key: SerializedKey,
}
```

`Match`, `Subscribe`, `Validate` don't create write effects; a
later read-audit/introspection design may record them separately.

Names retire per DA/62 §5: `AtomicBatch` → `WriteBatch` or
`CommitRequest`; `AtomicOperation` → `WriteOperation`;
`AtomicReceipt` → `CommitReceipt`; `Engine::atomic` →
`Engine::commit`; `Error::EmptyAtomicBatch` → impossible by
`NonEmpty`; `Error::DuplicateAtomicKey` → `Error::DuplicateWriteKey`.

---

## 8 · CLI / NOTA surface

Verb + domain payload only. Exchange ids hidden by the transport
layer.

```sh
# Single-op:
mind '(Assert (SubmitThought (...)))'

# Multi-op atomic:
mind '[(Retract (RoleClaim (role Designer)))
       (Assert (RoleClaim (role Poet)))]'

# Validate-then-commit pattern:
mind '[(Validate (Integrity (table thoughts)))
       (Mutate (Catalog (table thoughts) (status Active)))]'

# Subscribe at the tail of a write request:
mind '[(Mutate (Catalog (table thoughts) (status Active)))
       (Subscribe (ThoughtFilter (kind Decision)))]'
```

The `[ ... ]` sequence brackets are the **structural** marker of
a multi-op atomic request. No `(Batch ...)` wrapper. No
`(Anonymous)` / `(Tracked ...)` / `(Named ...)` headers. The
CLI / client library mints the next-sequence on the Connector lane
and wraps the typed request in a frame; users don't type the
exchange identifier.

---

## 9 · Open design questions

### Q1 — `RolledBack` vs `Invalidated` for prior aborted ops?

`SubReply::RolledBack { verb }` currently covers both:
- Writes that ran and were rolled back (durable effects undone)
- Reads/validates that ran and observed speculative state (no
  durability, but the result isn't authoritative)

DA/61 §9 suggests splitting:

```rust
pub enum SubReply<R> {
    Ok { verb, payload: R },
    /// Writes whose durable effects were rolled back.
    RolledBack { verb },
    /// Reads/validates whose results observed speculative state.
    Invalidated { verb },
    Failed { verb, reason, detail: Option<R> },
    Skipped { verb },
}
```

Pro split: distinguishes "system reverted my durable effects"
from "my read described uncommitted state." Different actions:
re-issue vs re-query.

Pro unified: callers usually just need "don't trust this op's
result; the request aborted." The distinction is rare in practice
and the embedded `verb` already lets callers infer it
(`verb: Match` → it's a read; not a durable rollback).

My lean: unified `RolledBack`. The verb already disambiguates.

### Q2 — Where do subscription events live in `FrameBody`?

§3 above adds `SubscriptionEvent { exchange, token, event }` as
the fourth FrameBody variant. DA/61 §3 is silent on this — the
spec only names HandshakeRequest, HandshakeReply, Request, Reply.

Without an event variant, subscription events would have to be
either (a) replies-after-replies on the original Subscribe
exchange (breaks "one reply per exchange") or (b) daemon-initiated
requests on `Acceptor` lane that expect a trivial ack from the
client (overhead per event). Neither is clean.

My lean: include `SubscriptionEvent` as a fourth variant. The
overhead is small (one variant in the enum); the alternative
shoehorns events into protocols they don't fit.

### Q3 — `ExchangeMode::LaneSequence` no longer needs explicit lane fields

DA/61 §3 still has:

```rust
pub enum ExchangeMode {
    LaneSequence {
        session_epoch: SessionEpoch,
        connector_lane: ExchangeLane,
        acceptor_lane: ExchangeLane,
    },
}
```

But `connector_lane` is always `ExchangeLane::Connector` and
`acceptor_lane` is always `ExchangeLane::Acceptor` by convention.
The fields are tautological — known from the connection direction.

§3 above simplifies to:

```rust
pub enum ExchangeMode {
    LaneSequence { session_epoch: SessionEpoch },
}
```

The runtime knows each side's lane from connection state
(who opened the socket vs who accepted). If a future variant
genuinely needs dynamic lane assignment (e.g., a server-initiated
reversal during handshake), it gets its own enum variant.

### Q4 — `session_epoch` on every frame, or implicit?

DA/61 §3 says *"the live wire may omit `session_epoch` from each
frame if connection state already supplies it. Durable logs expand
identity as needed."* That's wishy-washy — either the wire always
includes it or never does.

§3 above keeps it on every frame. Costs 8 bytes per frame. Buys: a
confused reconnect can't accidentally interpret an old-epoch frame
as current-epoch.

My lean: keep it on the wire. The cost is trivial; the safety is
real.

### Q5 — `check` vs `validate` method name

§5 above uses `check()` / `check_with_policy()`. DA/61 §9 suggests
this to avoid confusion with `SignalVerb::Validate` (the verb that
means "dry-run an op against rules").

Pro `check`: visibly different from `SignalVerb::Validate`.
Avoids the "validate-validate" awkwardness.

Pro `validate`: matches Rust convention (`String::from_utf8`-shaped
validators usually use `validate`); CS tradition.

My lean: `check`. The Verb collision is real; `check` reads cleanly.

---

## 10 · See also

- `~/primary/reports/designer/176-signal-channel-macro-redesign.md`
  — the macro spec over these primitives.
- `~/primary/reports/designer-assistant/61-signal-redesign-current-spec.md`
  — the DA-side spec; aligns substantively with this report.
- `~/primary/reports/designer-assistant/62-signal-redesign-implementation-brief.md`
  — operator-facing implementation brief.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs` — what
  this spec replaces.
- `/git/github.com/LiGoldragon/signal-core/src/reply.rs` — what
  this spec replaces.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  macro this spec's companion redesigns.
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the upstream
  discipline.
