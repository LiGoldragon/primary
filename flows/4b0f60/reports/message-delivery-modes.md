# Message delivery modes: Raw and FlowLocked

**Date:** 2026-09-21  
**Owner:** Mind4b0f60 architecture.  
**Status:** proposed compiled-domain capability contract. It is distinct from the existing callable codec and makes no claim of a coherent tested pair, deployment, or production enablement.

## Two independent dimensions

Delivery assurance and sender identity are separate dimensions. A transport-confirmed submission proves only that the transport accepted the submission. It does not prove recipient read, application acceptance, completion, or the originating logical sender. Read and completion remain separately witnessed outcomes.

```text
DeliveryMode = Raw | FlowLocked
SenderAttribution = Unattributed | BoundFlow{flow, binding_generation} | Unavailable{reason}
TransportState = Submitted | TransportConfirmed | Unconfirmed | DefinitiveNonDelivery
ApplicationState = NotObserved | Read | Accepted | Refused | Completed
```

These are proposed semantic shapes, not existing wire syntax or an invitation to build a JSON/string tunnel. Existing compiled binary domain contracts and root versioning remain the implementation medium. Identifiers use the shortest unique form accepted by the actual codec; correlation keys are never truncated, and full hashes remain internal evidence.

## Raw

`Raw` is explicit, UID-authorized, `Unattributed`, and `Unlocked`. Kernel peer evidence remains separately recorded, but Raw is never `AuthBoundFlow` or `VerifiedFlow`. A Raw envelope cannot mint authority, turn a claimed Flow/PID into a sender identity, or carry a delivery permit as authority. `NoRawEnvelope` tests must reject forged sender and permit claims while allowing an explicitly authorized Raw request.

Raw may use a useful disposable-recipient demonstration. Its scope is one authorized recipient, no broadcast, and no acknowledgement probe. The actual CLI syntax and result must be copied from a real candidate and real execution; this report invents neither. The demonstration records the delivery mode, UID policy, peer evidence, transport state, exact recipient selection, correlation key, and any unobserved application state. A successful transport confirmation still does not become read or completion.

## FlowLocked

`FlowLocked` is an optional compiled capability. It requires FlowNexus resolution and an exact durable permit, binding, and binding generation. It is unavailable until those dependencies and the Message bridge are actually implemented and compatible. Disabled or unavailable `FlowLocked` refuses with a typed result; it never silently downgrades to Raw. A permit releases neither refresh admission nor a durable hold by itself, and it does not authenticate the originating logical sender.

```text
FlowLockedRequest{recipient_flow, expected_binding, expected_generation,
                  durable_permit, payload, correlation}
  -> Refused{FlowLockedUnavailable | BindingMismatch | PermitInvalid | SenderUnbound}
   | Submitted{transport_state, receipt_ref}
```

Logical sender attribution remains governed by the peer-auth contract: kernel credentials identify the connector, while a bound Flow requires explicit registered caller binding/delegation with exact generation and the required kernel-identity evidence. Message payload peer records, bearer permit nonces, request IDs, and deduplication are not substitutes. If that proof is unavailable, identity-required mutation refuses; an independently authorized passive inventory may still report an unattributed requester without inventing a Flow.

## VM gate and rollout boundary

Field03 owns existing semi-sandbox VM native-auth Haiku/Luna launches. The authorized test scope prohibits credential copying/logging and requires the exact interface before execution. It permits no action outside the VM under this test authorization. Production has a separate concrete rollback plan and does not follow from a disposable Raw demonstration.

Independent audit evidence remains incomplete: Flow store `1b57de01` and runtime `cc9e7f9d` have publication status unknown; signal-flow is `c601a92d`, signal-message `5f85868a`, and Message `580021b9`. Missing pieces include Flow handlers, consumer pins, and the Message permit bridge. No coherent tested pair is available. Keep deployment, production capability enablement, and release status as unknown until those exact integrations and tests return receipts.

## Required tests and evidence

- Raw: explicit UID authorization, unattributed envelope labeling, kernel-peer evidence kept separate, forged sender/PID/permit rejection, `NoRawEnvelope`, one disposable recipient, no broadcast, and no read/ack probe.
- FlowLocked: disabled/unavailable refusal, exact Flow/binding/generation mismatch, durable permit validation, no Raw fallback, sender-bound proof, transport-confirmed distinct from read/completion, restart/receipt correlation, and hold/admission separation.
- VM: exact pre-execution interface, no credential copy/logging, no outside-VM effects, disposable recipient cleanup, and a concrete production rollback rehearsal before production enablement.

## Sources

- **Current living decision:** Raw/FlowLocked semantics, sender-attribution separation, disposable demonstration scope, VM ownership/gate, and production rollback separation. This is architecture authority, not an implementation receipt.
- **Existing architecture:** [Flow passive observation and peer-auth contract](flow-passive-observation-and-peer-auth.md) for the bound-sender/kernel-proof boundary, and [Nexus and Message current handoff](nexus-messaging-current-handoff.md) for durable permit/admission/hold and reservation boundaries.
- **Independent audit reported in the current conversation:** candidate revisions `1b57de01`, `cc9e7f9d`, `c601a92d`, `5f85868a`, and `580021b9`; no coherent tested pair, Flow handlers, consumer pins, or Message permit bridge. These are source/audit qualifiers, not deployment claims.
