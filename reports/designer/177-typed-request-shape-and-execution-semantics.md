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
//
// Reply is a typed sum. Pre-execution rejection and in-execution
// abort are different categories: one has no per-op results
// because no op ran; the other has per-op results because some did.
// Splitting the variants makes illegal states unrepresentable.
pub enum Reply<ReplyPayload> {
    /// Request was accepted for execution. Per-op results follow.
    /// `outcome` distinguishes all-committed from aborted-at-N.
    Accepted {
        outcome: AcceptedOutcome,
        per_operation: NonEmpty<SubReply<ReplyPayload>>,
    },

    /// Request was rejected before any op began (pre-flight rule
    /// violation: verb/payload mismatch, Subscribe position,
    /// decode error, malformed shape). No per-op results because
    /// no op ran.
    Rejected {
        reason: RequestRejectionReason,
    },
}

pub enum AcceptedOutcome {
    /// All operations completed/committed. Each `per_operation`
    /// entry is `SubReply::Ok`.
    Completed,
    /// Op at position `failed_at` failed; the request was aborted.
    /// Writes that would have committed did not. Subscribes that
    /// would have opened did not.
    Aborted {
        failed_at: usize,
        reason: OperationFailureReason,
    },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum RequestRejectionReason {
    /// An op's `verb` did not match its payload's
    /// `RequestPayload::signal_verb()`.
    VerbPayloadMismatch { index: usize },
    /// A `Subscribe` op appeared outside the request's tail-contiguous
    /// Subscribe suffix.
    SubscribeOutOfPosition { index: usize },
    /// Receiver-internal error before any op ran.
    Internal,
}

// NOTE: there is no `DecodeError` variant. A typed `Reply::Rejected`
// requires an exchange identifier to address; rkyv-level frame decode
// failure means there is no typed request to answer (no exchange).
// That case is a protocol error: drop the connection, log.

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum OperationFailureReason {
    PreconditionFailed,
    ValidationFailed,
    DomainRejection,
}

/// Per-op reply — typed sum. Illegal states unrepresentable.
/// Only present inside `Reply::Accepted`.
pub enum SubReply<ReplyPayload> {
    /// Op ran and committed/completed. Only emitted when the
    /// containing `AcceptedOutcome` is `Completed`.
    Ok { verb: SignalVerb, payload: ReplyPayload },

    /// Op ran inside a request that subsequently aborted. For writes:
    /// durable effects were reverted. For reads/validates: result
    /// observed speculative state that did not persist. Either way,
    /// the result is no longer authoritative.
    Invalidated { verb: SignalVerb },

    /// Op was attempted and failed; this is the cause of the abort.
    /// Exactly one per aborted request, at `failed_at`.
    Failed {
        verb: SignalVerb,
        reason: OperationFailureReason,
        detail: Option<ReplyPayload>,
    },

    /// Op never ran because an earlier op failed.
    Skipped { verb: SignalVerb },
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
pub struct LaneSequence(u64);

pub enum ExchangeLane {
    Connector,   // the side that opened the connection
    Acceptor,    // the side that accepted
}

/// Identifies a request/reply exchange. The request frame mints
/// it; the reply frame echoes it. The pair is the exchange.
pub struct ExchangeIdentifier {
    pub session_epoch: SessionEpoch,
    pub lane: ExchangeLane,
    pub sequence: LaneSequence,
}

/// Identifies one subscription-event frame's position on the
/// acceptor lane. Same wire shape as `ExchangeIdentifier`, but a
/// distinct type — an event is a stream item, not half of a
/// request/reply pair. The field exists for future
/// resume-from-N reconnect support.
pub struct StreamEventIdentifier {
    pub session_epoch: SessionEpoch,
    pub lane: ExchangeLane,
    pub sequence: LaneSequence,
}

pub enum ExchangeMode {
    LaneSequence { session_epoch: SessionEpoch },
    // Future cryptographic-derivation modes for network components
    // get their own enum variants. Local IPC uses LaneSequence.
}

// signal-core/src/frame.rs
//
// Three payload type parameters keep replies and subscription events
// in distinct types — a reply cannot accidentally carry an event
// variant and vice versa. Channels without Subscribe ops set
// EventPayload = core::convert::Infallible, making the
// SubscriptionEvent variant unconstructible by type.
pub enum FrameBody<RequestPayload, ReplyPayload, EventPayload> {
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
    /// requested the stream (see §4.2).
    SubscriptionEvent {
        event_identifier: StreamEventIdentifier,
        token: SubscriptionTokenInner,
        event: EventPayload,
    },
}

pub struct Frame<RequestPayload, ReplyPayload, EventPayload> {
    pub body: FrameBody<RequestPayload, ReplyPayload, EventPayload>,
}
```

---

## 4 · Connection state — exchanges and subscriptions

Two parallel concerns live on the runtime: request/reply exchange
tracking, and subscription-event tracking. The handshake establishes
the lane/sequence grammar for both.

### 4.1 · Request/Reply exchange state

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

### 4.2 · Subscription state

A `Subscribe` op opens a long-lived event stream; that needs explicit
per-connection state on both sides for routing and lifecycle.

```rust
// Connector (subscriber) side: routes incoming SubscriptionEvent
// frames to the actor that opened the stream.
pub struct ConnectorSubscriptionState {
    pub open: BTreeMap<SubscriptionTokenInner, ConnectorSubscriptionHandle>,
}

pub struct ConnectorSubscriptionHandle {
    pub token: SubscriptionTokenInner,
    pub opener_exchange: ExchangeIdentifier,
    pub event_sink: SubscriptionEventSink,
}

// Acceptor (emitter) side: tracks which subscriptions exist on this
// connection so writes know whom to notify.
pub struct AcceptorSubscriptionState {
    pub open: BTreeMap<SubscriptionTokenInner, AcceptorSubscriptionRecord>,
    pub next_token: SubscriptionTokenInner,  // monotonic mint
}

pub struct AcceptorSubscriptionRecord {
    pub token: SubscriptionTokenInner,
    pub opener_exchange: ExchangeIdentifier,
    pub filter: ChannelSubscriptionFilter,   // per-channel typed
}
```

**Token assignment**: the acceptor mints. The `SubscriptionOpened`
reply carries the assigned token. Subsequent `SubscriptionEvent`
frames on that connection's acceptor lane reference it.

**Token uniqueness**: per-connection. Different connections may
mint colliding numeric values without consequence — the
`(connection, token)` pair is the identity.

**Connector-side routing**:
1. Decode `FrameBody::SubscriptionEvent { event_identifier, token, event }`.
   The `event` is the channel's `EventPayload` enum (`MindEvent`,
   `RouterEvent`, etc.), not its `ReplyPayload`.
2. Look up `token` in `open`.
3. Forward `event` to `event_sink`.
4. Unknown token ⇒ protocol error (drop connection, log).

**Acceptor-side fanout**: each write/state-change iterates `open`,
evaluates per-subscription filters, emits matching events on the
acceptor lane using the standard `LaneSequence` counter.

**Ordering guarantees**:
- *Within a subscription*: transport-ordered. Frames on the acceptor
  lane arrive in emission order; the daemon's emit-loop serializes.
  No per-event sequence number on `SubscriptionEvent` beyond the
  acceptor-lane `StreamEventIdentifier`.
- *Across subscriptions*: events interleave on the shared acceptor
  lane. Each substream stays ordered; cross-substream order is the
  daemon's emission order, not a promised invariant.

**Retraction**: a `Retract <Channel>SubscriptionRetraction(token)`
request closes the subscription. On commit, the acceptor removes
the entry; the reply confirms; the connector removes its entry on
reply. Late events for a closed token (racing the retract) are
dropped on the connector side.

**Disconnect**: closing a connection clears both open maps. No
cross-connection subscription continuity in v1; reconnect re-opens
explicitly.

**Resume / replay (deferred)**: the `event_identifier.sequence` on
each `SubscriptionEvent` (acceptor-lane monotonic `LaneSequence`)
is the position required for future resume-from-N. A reconnect
handshake variant could carry the connector's "highest seen
acceptor-lane sequence." Not in v1; the field is in the frame for
the day it becomes useful.

**Subscription "name"**: the wire identity is the token. Any
human-readable label lives on `ConnectorSubscriptionHandle` (or
on the actor that owns the `event_sink`) — client-side concern,
not protocol.

---

## 5 · Validation API

Two methods on `Request<Payload>`; both enforce the same universal
rules. v1 has no channel-specific policy in the kernel — see §9 Q6.

```rust
impl<Payload> Request<Payload>
where
    Payload: RequestPayload,
{
    /// Run universal structural rules: per-op verb/payload alignment
    /// via `RequestPayload::signal_verb()`, Subscribe-must-be-last
    /// position. NonEmpty is type-enforced and needs no runtime check.
    pub fn check(&self) -> Result<(), RequestRejectionReason> { /* ... */ }

    /// Consume self and return a `CheckedRequest` if universal rules
    /// pass. Returns the rejection reason plus the original request
    /// on failure (so the caller can recover the payload).
    pub fn into_checked(self)
        -> Result<CheckedRequest<Payload>, (RequestRejectionReason, Self)>
    {
        if let Err(reason) = self.check() {
            return Err((reason, self));
        }
        Ok(CheckedRequest { operations: self.operations })
    }
}

pub struct CheckedRequest<Payload> {
    pub operations: NonEmpty<Operation<Payload>>,
}
```

Universal-only rule set:

1. **Verb/payload alignment**: each `Operation { verb, payload }` has
   `verb == payload.signal_verb()`. Catchable at construction by
   using `From<Payload> for Request<P>` paths that auto-derive verb;
   `check()` enforces for constructions that don't.
2. **Subscribe suffix**: `Subscribe` ops, if any, form a contiguous
   suffix of the operation sequence. A single Subscribe is a special
   case (suffix of length 1); multiple Subscribes at the tail open
   atomically via two-phase staged-open (see §6). A Subscribe at any
   position other than the suffix is `SubscribeOutOfPosition`.

Method named `check` rather than `validate` to avoid confusion with
`SignalVerb::Validate` (the verb that means "dry-run an op against
rules"). The two are different things; the name change makes that
visible. (Open naming question — see §9 Q5.)

Channel-specific static policy (max ops, read/write mixing rules,
forbidden verbs) is **not in v1**. The kernel ships with universal
rules only. When a concrete channel needs stricter rules, a
typed channel-level policy lands then. See §9 Q6.

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
| Subscribe + non-Subscribe | **Subscribes, if any, form a contiguous suffix.** Non-Subscribe ops execute in strict order first; if any fails, no streams open. If all succeed, writes commit, then the Subscribe suffix opens atomically at the post-commit snapshot via two-phase staged-open. A Subscribe outside the tail-contiguous suffix is rejected at receive-time as `Reply::Rejected { reason: RequestRejectionReason::SubscribeOutOfPosition }`. |

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

### 8.1 · NOTA codec at the kernel layer

`signal-core` owns the NOTA codec for `Operation<Payload>` and
`Request<Payload>`. The macro owns the NOTA codec for the channel's
payload enum. Stacked, they produce the verb-wrapped form above.

**`Operation<Payload>` codec** (where `Payload: NotaEncode + NotaDecode + RequestPayload`):

```text
encode(Operation { verb, payload }) → (<verb-name> <encoded-payload>)
decode((<verb-name> <inner>))      → Operation {
                                       verb: <verb-name>,
                                       payload: Payload::decode(<inner>),
                                     }
                                       — and then check
                                         payload.signal_verb() == verb
                                         (else DecodeMismatch error)
```

`<verb-name>` is the PascalCase `SignalVerb` discriminant
(`Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`, `Validate`).

**`Request<Payload>` codec**:

```text
length-1 request: encode as the single Operation form
                  (Assert (SubmitThought ...))
length-N request: encode as bracketed sequence of Operation forms
                  [(Assert ...) (Match ...) ...]

decode head:
  - record head matching a SignalVerb name → length-1 request,
    decode as single Operation
  - sequence head [ → length-N request, decode each element as Operation,
    construct NonEmpty
```

Round-trip witnesses live in `signal-core/tests/`:

- `single_op_request_round_trips_through_verb_wrapper`
- `multi_op_request_round_trips_through_sequence`
- `verb_payload_mismatch_in_outer_wrapper_is_rejected`
- `bare_payload_without_verb_wrapper_is_rejected` (catches the
  current macro-test regression)

The channel macro's NOTA codec for `MindRequest` only covers the
payload enum (`(SubmitThought ...)` ↔ `MindRequest::SubmitThought(...)`).
Wrapping in `(Assert ...)` and request-sequence handling live at
the kernel layer, where they're shared across every channel.

---

## 9 · Open design questions

### Q1 — `Invalidated` (unified) for prior aborted ops

`SubReply::Invalidated { verb }` is the universal predicate for ops
that ran in an aborted request:

- A **write** that ran and got reverted: the receipt promised a
  durable effect the engine then undid. The receipt is invalid.
- A **read or validate** that ran against speculative state: the
  view is no longer authoritative. The result is invalid.

```rust
pub enum SubReply<R> {
    Ok { verb, payload: R },
    /// Ran but its result is no longer authoritative because the
    /// request as a whole aborted. For writes, the effect was
    /// reverted; for reads, the observed state did not persist.
    Invalidated { verb },
    Failed { verb, reason, detail: Option<R> },
    Skipped { verb },
}
```

`RolledBack` would be a half-lie: it correctly names the write case
but is a category error for reads (nothing was rolled back; the read
was accurate at the moment it ran, the world just didn't keep that
state). `Invalidated` is universally true.

The `verb` field tells callers *how* the result got invalidated
(`verb: Mutate` ⇒ a write was reverted; `verb: Match` ⇒ a read
observed dead state). No separate variant earns its keep.

Settled: unified `Invalidated`.

### Q2 — `SubscriptionEvent` is the 5th `FrameBody` variant

§3 carries `SubscriptionEvent { exchange, token, event }` as the
fifth FrameBody variant. The alternatives (replies-after-replies
on the original Subscribe exchange, or per-event daemon-initiated
request frames) either break "one reply per exchange" or pay
handshake overhead per event.

§4.2 specifies the connector-side and acceptor-side subscription
trackers: the connector maintains `SubscriptionTokenInner →
ConnectorSubscriptionHandle` so events route to the right
subscriber; the acceptor maintains `SubscriptionTokenInner →
AcceptorSubscriptionRecord` so writes know whom to notify.
Ordering within a subscription is transport-guaranteed (single
acceptor lane, serialized emit-loop); cross-subscription order is
not promised.

Settled: 5th variant + stateful per-connection trackers on both
sides.

### Q3 — `ExchangeMode::LaneSequence` drops the tautological lane fields

The `connector_lane`/`acceptor_lane` fields in DA/61's
`ExchangeMode::LaneSequence` were always `Connector`/`Acceptor`
respectively — known from connection direction, not negotiated.

§3 simplifies to `LaneSequence { session_epoch }`. A future
variant that genuinely needs dynamic lane assignment gets its
own enum variant.

Settled.

### Q4 — `session_epoch` on every frame

§3 keeps `session_epoch` on every frame. Costs 8 bytes per frame.
Buys: a confused reconnect can't accidentally interpret an
old-epoch frame as current-epoch.

Settled.

### Q5 — `check` (settled)

§5 uses `check()`. Visibly different from `SignalVerb::Validate`
(the verb that means "dry-run an op against rules"); the two
concepts no longer collide on a single name.

Settled.

### Q6 — `ChannelPolicy` deferred out of v1 (per DA/63 F2)

DA/63 §F2 argues `ChannelPolicy` in `signal-core` and
`channel_policy { ... }` in the macro are premature: no concrete
channel has been identified that needs stricter-than-universal
rules, so the kernel doesn't earn the abstraction yet. v1 should
ship with universal rules only.

§5 now reflects this: only `check()` / `into_checked()` enforce
universal rules (verb/payload alignment + Subscribe position).
The `_with_policy` methods, the `ChannelPolicy` trait, the
`DefaultPolicy` struct, and the macro's `channel_policy { ... }`
block all come back the day a real channel needs them.

Settled-as-deferred.

### Q7 — Architecture drift (per DA/63 §3)

Resolved 2026-05-15. Workspace-wide architecture sweep landed across
the affected docs:

- `skills/contract-repo.md` (primary repo)
- `signal-core/ARCHITECTURE.md`
- `sema-engine/ARCHITECTURE.md` (with rename map for the seven-root
  → six-root transition)
- `signal/ARCHITECTURE.md` + `README.md`
- `signal-persona/ARCHITECTURE.md`
- `nexus/ARCHITECTURE.md` + `spec/grammar.md`
- `signal-persona-mind/ARCHITECTURE.md` (no change needed; already
  consistent)
- `persona/ARCHITECTURE.md` (no change needed; already consistent)

Settled.

### Q8 — `SubscriptionEvent` payload type (per DA/63 v2 #1)

`FrameBody` is now three-axis: `FrameBody<RequestPayload, ReplyPayload,
EventPayload>`. The `SubscriptionEvent` variant carries `event:
EventPayload`, distinct from `reply: Reply<ReplyPayload>`. Channels
with `Subscribe` ops declare an `event <EventName> { ... }` macro
block; channels without `Subscribe` set `EventPayload =
core::convert::Infallible`, making the `SubscriptionEvent` variant
type-uninhabited.

Settled.

### Q9 — Subscribe placement is the tail-contiguous suffix (per DA/63 v2 #2)

§5 and §6 both say: `Subscribe` ops, if any, form a contiguous suffix
of the operation sequence. A single Subscribe is a special case
(suffix of length 1); multiple Subscribes at the tail open atomically
via two-phase staged-open. Subscribes elsewhere are
`RequestRejectionReason::SubscribeOutOfPosition`.

Settled.

### Q10 — `DecodeError` removed from `RequestRejectionReason` (per DA/63 v2 #3)

A typed `Reply::Rejected` requires an `ExchangeIdentifier` to address.
rkyv-level frame decode failure means there is no typed request to
answer (no exchange ⇒ no addressable reply). That case is a protocol
error: drop the connection, log. `RequestRejectionReason` now contains
only `VerbPayloadMismatch`, `SubscribeOutOfPosition`, and `Internal`.

Settled.

### Q11 — `LaneSequence` replaces `ExchangeSequence` (per DA/63 v2 #4)

The monotonic counter is a property of the lane, not of the exchange.
Replies don't consume sequence numbers (they echo the request's).
SubscriptionEvents consume sequence numbers on the acceptor lane.
Naming the counter `LaneSequence` makes it correct for both
`ExchangeIdentifier` and `StreamEventIdentifier`, which both embed it.

Settled.

### Q12 — One parameterized `FrameBody`, not two types (vs DA/64 §5)

DA/64 §5 recommends splitting `FrameBody` into two distinct types
— `ExchangeFrameBody<RequestPayload, ReplyPayload>` for non-streaming
channels and `StreamingFrameBody<RequestPayload, ReplyPayload,
EventPayload>` for streaming — to avoid a "fake zero-sized NoEvent
type."

I disagree. `core::convert::Infallible` is the standard Rust idiom
for "this case cannot exist" (used by `Result<T, Infallible>` in
the stdlib, by `Never` in nightly, by the `?` operator's type
machinery). Setting `EventPayload = Infallible` on non-streaming
channels makes the `SubscriptionEvent` variant **type-uninhabited**
at use-site — a real compile-time guarantee, not a fake type.

One parameterized type wins on:
- single decode/dispatch path in transport code;
- single `Frame<RequestPayload, ReplyPayload, EventPayload>` API
  shared by every channel;
- future frame variants (flow control, cancellation, etc.) land
  once, not twice.

The wire overhead is one unreachable rkyv tag value per
non-streaming connection — irrelevant.

Settled: one `FrameBody`. Non-streaming channels' macro emission
sets `EventPayload = Infallible`.

### Q13 — Verb-wrapped NOTA codec at the kernel layer (per DA/64 §6)

§8.1 above adds `Operation<Payload>` and `Request<Payload>` NOTA
codecs to `signal-core`. The channel macro emits payload-only
codecs; verb-wrapping (`(Assert ...)`) and request-sequence
brackets (`[(Assert ...) (Match ...)]`) are kernel concerns
shared across every channel.

DA/64 §7 notes the current macro tests prove only bare-payload
NOTA. New round-trip witnesses required in `signal-core/tests/`:

- `single_op_request_round_trips_through_verb_wrapper`
- `multi_op_request_round_trips_through_sequence`
- `verb_payload_mismatch_in_outer_wrapper_is_rejected`
- `bare_payload_without_verb_wrapper_is_rejected`

Settled.

### Q14 — No auto-`From<Payload>` impls (per DA/64 §7)

DA/64 §7 flags that auto-`From<Payload> for RequestEnum` impls
conflict if two variants ever share a payload type. The current
convention (unique payload types per enum) is enforced by Rust's
compile-error on conflict, but the diagnostic is poor.

Drop the auto-From entirely. Variant constructors are already
ergonomic — `MindRequest::SubmitThought(payload)`. If a channel
wants `.into()` for an unambiguous payload, hand-write `From` for
that one.

Settled: macro doesn't emit auto-From impls.

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
