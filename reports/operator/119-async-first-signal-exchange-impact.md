# 119 - Async-First Signal Exchange Impact

*Operator impact report, 2026-05-15. Reads
`reports/designer-assistant/60-async-first-signal-exchange-protocol.md`
and operator `/118`. Purpose: update the operator implementation target
after DA/60 superseded the ordered-single-flight v1 lean.*

## Bottom Line

Signal should be async from v1. This does not revive `CorrelationId`,
`RequestHeader<Intent>`, generic `Intent`, or payload-level metadata.
It means the frame layer owns a small deterministic exchange protocol:

```text
handshake negotiates exchange grammar
each endpoint owns one outbound lane
each request uses the next sequence on its lane
reply echoes the request's exchange id
wrong lane / duplicate / unknown exchange is a protocol error
```

That is the correct base for Persona's actor topology. It avoids the
two bad future paths: ad hoc extra connections to simulate concurrency,
or private request ids outside `signal-core`.

## Current Core Shape

The signal-core request/reply data remains clean:

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
```

The exchange id is not payload and not generic metadata. It is the
structural request/reply matching key on request and reply frame bodies:

```rust
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
}
```

## Handshake Contract

The handshake establishes the exchange mode and lane ownership:

```rust
pub struct ExchangeHandshake {
    pub exchange_mode: ExchangeMode,
}

pub enum ExchangeMode {
    LaneSequence {
        session_epoch: SessionEpoch,
        connector_lane: ExchangeLane,
        acceptor_lane: ExchangeLane,
    },
}

pub struct ExchangeIdentifier {
    pub session_epoch: SessionEpoch,
    pub lane: ExchangeLane,
    pub sequence: ExchangeSequence,
}
```

The live connection records which lane belongs to which endpoint.
An endpoint may only issue request frames on its own outbound lane.
Replies echo the exact `ExchangeIdentifier` from the request.

`session_epoch` can be implicit on the live wire if connection state
already provides it, but logs and diagnostics should be able to expand
the full identity:

```text
engine_id + component_id + connection_instance + session_epoch + lane + sequence
```

## Runtime Rules

Sender side:

- maintain `next_outgoing_sequence` for the endpoint's lane;
- assign the next sequence before writing a request frame;
- insert the exchange into the pending map;
- reject local sequence reuse;
- remove the pending exchange when its reply arrives.

Receiver side:

- reject a request whose lane is not the peer's outbound lane;
- reject a duplicate open `(lane, sequence)`;
- process requests independently under actor backpressure;
- reply with the exact exchange id from the request.

Reply side:

- reject a reply whose exchange is not pending;
- reject duplicate replies for a closed exchange;
- route the reply to the waiting actor/requester by exchange id.

Out-of-order replies are normal. Unknown replies, wrong-lane requests,
and duplicate open exchanges are protocol errors.

## Text Surface

Human-facing Nexus/CLI input stays verb-rooted:

```nota
(Assert (SubmitThought ...))
```

or a multi-operation request:

```nota
[(Retract (RoleClaim Designer))
 (Assert (RoleClaim Poet))]
```

The CLI/client library wraps that request in a frame with an exchange
id. Humans only see exchange ids when inspecting or replaying frames as
protocol objects.

## Macro Consequences

`signal_channel!` should not emit:

- `with intent <T>`;
- an `intent <T> { ... }` block;
- `NoIntent`;
- `single_named`;
- `single_tracked`;
- `batch_tracked`;
- request/reply header aliases.

It should emit or support:

- request payload enum;
- reply payload enum;
- per-variant `SignalVerb` witness;
- operation-kind enum if it still earns its place;
- aliases for `Request<Payload>`, `Reply<ReplyPayload>`, and
  `Frame<RequestPayload, ReplyPayload>`;
- constructors/builders for one or more operations;
- declarative batch policy if the policy remains channel-level.

The exchange protocol belongs in `signal-core` frame/handshake code and
the component runtime, not in each contract payload.

## Implementation Witnesses

First `signal-core` / runtime tests should include:

```text
handshake records lane ownership
request frame on own lane is accepted
request frame on peer lane is rejected
two requests in flight on one connection resolve by exchange id
out-of-order replies resolve to the correct pending exchange
duplicate open exchange is rejected
unknown reply exchange is rejected
closed exchange cannot be replied to twice
payload codecs never contain exchange ids
```

The decisive witness is the two-in-flight test: request A and request B
leave on the same connection, reply B arrives before reply A, and both
waiting actors receive the correct replies.

## Sema-Engine Consequences

The sema-engine wave remains unchanged in substance:

- remove Atomic-colored names and log shape;
- commit structural write batches;
- log per-operation write effects;
- do not depend on `RequestHeader<Intent>` or `CorrelationId`.

If commit logs need trace/audit context later, that comes from the
frame/log metadata design, not the core request payload.

## Operator Stance

DA/60 should replace `/118`'s ordered-single-flight question. The
current operator implementation target is:

```text
signal-core:
  SignalVerb
  NonEmpty<T>
  Operation<Payload>
  Request<Payload>
  Reply<ReplyPayload>
  SubReply<ReplyPayload>
  ExchangeHandshake
  ExchangeMode::LaneSequence
  ExchangeLane
  ExchangeSequence
  ExchangeIdentifier
  FrameBody<RequestPayload, ReplyPayload>

runtime:
  connection exchange state
  outbound sequence counter per local lane
  pending exchange map
  protocol-error paths

sema-engine:
  structural write-batch commit and log shape, no Atomic root
```

Trace/audit remains separate. `CorrelationId` should not be used for
request matching.
