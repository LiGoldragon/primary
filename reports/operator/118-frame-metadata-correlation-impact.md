# 118 - Frame Metadata And Correlation Impact

**Status update, 2026-05-15:** this report is now **pre-DA60** for
the transport exchange shape. Keep its layer split and rejection of
`RequestHeader<Intent>` / `CorrelationId` / generic `Intent`, but read
`reports/operator/119-async-first-signal-exchange-impact.md` for the
current exchange decision: Signal is async from v1, with lane/sequence
exchange ids negotiated in the handshake.

*Operator impact report, 2026-05-15. Reads
`reports/designer-assistant/59-frame-metadata-and-correlation-correction.md`,
current `reports/designer/177-typed-request-shape-and-execution-semantics.md`,
current `reports/designer/176-signal-channel-macro-redesign.md`, and
operator `/117`. Purpose: prevent implementation from baking
transport/audit metadata into the signal request core while the
designer/user decision is still active.*

## Bottom Line

DA/59 is correct to challenge the current `Request<Payload, Intent>` /
`RequestHeader<Intent>` path. It separates five planes that `/177` and
`/176` currently blur:

```text
Signal verb       -> Assert / Mutate / Retract / Match / Subscribe / Validate
Domain payload    -> typed noun the verb acts on
Request container -> one or more verb-rooted operations
Frame/session     -> wire carrier, ordering, request/reply matching
Trace/audit       -> optional metadata outside payload semantics
```

Implementation should not proceed on the `Intent` / `RequestHeader`
shape until the user/designer settles DA/59's questions.

## What Survives From `/117`

The following remain sound and should stay in the first signal-core +
sema-engine wave:

- Six signal roots; no `Atomic`.
- `NonEmpty<Operation<Payload>>` for non-empty request containers.
- `SubReply` is a typed sum, not status plus optional payload.
- Handshakes live at the frame body layer, not inside `Reply`.
- sema-engine moves with signal-core because its old Atomic-colored
  log and receipt shape breaks as soon as `Atomic` disappears.
- sema-engine commit logs should record structural write batches and
  per-operation effects, not a top-level `SignalVerb::Atomic`.

## What DA/59 Invalidates Or Pauses

These `/117` and `/177` implementation details should be paused:

```text
Request<Payload, Intent>
RequestHeader<Intent>
ReplyHeader<Intent>
NoIntent as the replacement for absent intent
Named / Tracked request constructors
(Batch (Named RoleHandoff "cor-id") [...]) as core-visible syntax
correlation id as request semantic data
generic Intent as a signal-core type parameter
```

The cleaner signal-core shape is closer to:

```rust
pub enum SignalVerb {
    Assert,
    Mutate,
    Retract,
    Match,
    Subscribe,
    Validate,
}

pub struct Operation<Payload> {
    pub verb: SignalVerb,
    pub payload: Payload,
}

pub struct Request<Payload> {
    pub operations: NonEmpty<Operation<Payload>>,
}

pub struct Reply<ReplyPayload> {
    pub outcome: RequestOutcome,
    pub per_operation: NonEmpty<SubReply<ReplyPayload>>,
}

pub struct Frame<RequestPayload, ReplyPayload> {
    pub metadata: FrameMetadata,
    pub body: FrameBody<RequestPayload, ReplyPayload>,
}
```

`FrameMetadata` should start minimal. For a local v1 daemon, ordered
single-flight means no request-matching id is needed for correctness.
If multiplexing arrives later, the matching key should be scoped by
connection/session plus a negotiated sender lane and monotonic request
sequence, not a client-supplied global correlation string.

DA/59's sharper async rule is worth carrying into implementation:

```rust
pub enum ExchangeMode {
    OrderedSingleFlight,
    Multiplexed {
        session_epoch: SessionEpoch,
        client_lane: RequestLane,
        server_lane: RequestLane,
    },
}

pub struct RequestIdentifier {
    pub session_epoch: SessionEpoch,
    pub lane: RequestLane,
    pub sequence: RequestSequence,
}
```

The handshake negotiates `ExchangeMode`. `OrderedSingleFlight` carries
no request identifier. `Multiplexed` gives each side its own lane; a
party mints outgoing request ids only by incrementing its own lane's
sequence. The peer rejects ids outside the negotiated session/lane or
duplicates within that lane.

## Domain Intent

`RoleHandoff` is either a domain operation or an audit label. It should
not be a generic request header.

If it is domain semantics:

```text
(Mutate (RoleHandoff Designer Poet))
```

If it is audit classification, it belongs in trace/log metadata owned
by the frame/session or introspection layer, with a precise type such
as `AuditLabel`. It should not change the domain request type.

## Macro Consequences

If DA/59's split is accepted, `signal_channel!` should not emit an
`intent` enum or `NoIntent` machinery. It should emit:

- request payload enum;
- reply payload enum;
- per-variant `SignalVerb` witness;
- operation-kind enum if still useful;
- type aliases for `Request<Payload>`, `Reply<ReplyPayload>`, and
  `Frame<RequestPayload, ReplyPayload>`;
- constructors/builders for one or more operations;
- declarative batch policy if the policy is truly channel-level.

It should not emit `single_tracked`, `single_named`, or
`RequestHeader`-colored constructors unless frame metadata later earns
those concepts under a separate transport/audit API.

## Sema-Engine Consequences

The sema-engine replacement shape from `/117` still needs to happen,
but its commit log should not depend on `RequestHeader<Intent>`.

The log can keep structural write information:

```rust
pub struct CommitLogEntry {
    pub snapshot: SnapshotId,
    pub op_count: usize,
    pub operations: NonEmpty<CommitLogOperation>,
}

pub struct CommitLogOperation {
    pub verb: SignalVerb, // Assert / Mutate / Retract only.
    pub table: TableName,
    pub key: SerializedKey,
}
```

Trace/audit fields can be added through frame/log metadata once that
design exists. Do not smuggle them into the storage request core.

## Decisions To Bring Forward

1. Should local Signal IPC v1 be ordered single-flight? Operator lean:
   yes. It keeps request/reply matching out of the core request type.
2. Should future multiplexed channels negotiate
   `(session_epoch, sender_lane, sequence)` in the handshake rather
   than accept global correlation strings? Operator lean: yes.
3. Should trace/audit metadata be absent from v1 frames unless the
   introspection/logging layer requires it? Operator lean: yes.
4. Should generic `Intent` be removed from signal-core request/reply
   primitives? Operator lean: yes.
5. Should human-facing CLI/Nexus input stay verb-rooted, with frame
   wrappers visible only when inspecting transport frames? Operator
   lean: yes.

## Implementation Stance

Do not implement `/177`'s `RequestHeader<Intent>` design. The safe
first implementation slice is now:

```text
signal-core:
  SignalVerb
  NonEmpty<T>
  Operation<Payload>
  Request<Payload>
  Reply<ReplyPayload>
  SubReply<ReplyPayload>
  FrameBody<RequestPayload, ReplyPayload>
  minimal FrameMetadata, or no metadata if ordered single-flight wins

sema-engine:
  remove Atomic-colored names and log shape
  commit structural write batches
  log per-operation write effects
```

Everything involving request intent, named batches, tracked batches,
and correlation ids waits for the frame/session metadata decision.
