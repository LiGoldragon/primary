# 131 — persona-router triad audit

*Audit of the persona-router triad: `signal-persona-router`
(working contract) + `owner-signal-persona-router` (policy
contract) + `persona-router` (daemon). Of the three legs, only the
owner contract has migrated to the current substrate; the working
contract and the daemon are entirely stale. The triad is the worst-
preserved component triad in the workspace after `signal-persona-
mind`.*

## 0 · TL;DR

The router triad sits roughly **one-third migrated**. The owner
contract — `owner-signal-persona-router` — is the only leg that
landed under the current shape: `signal-frame` dependency,
contract-local verbs (`Grant`, `Extend`, `Revoke`, `Deny`), and
clean payload records. The working contract and daemon both still
live entirely on the old substrate.

Migration state by leg:

- `signal-persona-router` — **stale**. Depends on `signal-core` (not
  `signal-frame`); request enum uses universal-verb prefixes
  (`Match Summary / Match MessageTrace / Match ChannelState`);
  every type carries the `Router*` ancestry prefix; no
  `observable` block; configuration record carries a stale
  `supervision_socket_*` triplet (per /252 should be
  `engine_management_socket_*`).
- `owner-signal-persona-router` — **mostly current**. On
  `signal-frame`; contract-local verbs in verb form; payload
  records clean (`ChannelGrant`, `ChannelExtension`,
  `ChannelRevocation`, `AdjudicationDenial`). Open gaps:
  `OwnerRouter*` ancestry on the macro-emitted types
  (alias-dance not done), no `observable` block, redundant
  `RequestUnimplemented.operation` field, hand-written codec
  impls on `ChannelEndpoint` and `ChannelDuration` while
  mixed-enum support now exists, the `OperationKind::Deny`
  caller-direction smell from /257 §1.5 (`Deny` is on the
  channel-grant family, but the variant payload is
  `AdjudicationDenial` not `ChannelDenial` — see §3.2).
- `persona-router` daemon — **stale**. Depends on
  `signal-core`; depends on `signal-persona-mind` not on the
  owner contract; has **no thin CLI binary** (no
  `src/bin/router.rs`); the one binary
  `persona-router-daemon` parses flags (`--socket`, `--store`,
  `--bootstrap`); daemon does not consume `signal-executor`,
  has no `Lowering`, no `CommandExecutor`, no `ToSemaOperation`
  / `ToSemaOutcome` impls; carries its own bespoke
  `supervision.rs` hand-rolled supervision listener; observation
  reply path matches over `RouterRequest` directly without any
  executor framework.

Beyond the three-channel separation flagged in /150 §6.2
(message-routing vs channel-grants vs observation), the daemon
currently has **only one channel** in its working contract — the
observation surface — and the channel-grant logic enters the
daemon through a side door: by depending on `signal-persona-mind`
and decoding `MindChannelGrant` records (see §2.4). This is the
load-bearing structural problem: the working contract should
carry message routing AND observation as its two public surfaces;
channel grants belong in the owner contract and are CALLED by
Orchestrate per `intent/component-shape.nota` 2026-05-20T13:30:00Z.

**Priority for the triad's next slice**: clean the owner contract
first (small, almost-done) — alias drop, observable block, redundant
fields. Then redesign the working contract from scratch under the
three-surface plan from /150 §6.2 + the contract-local-verb shape.
Then rewrite the daemon onto signal-executor with the binary split
(`router-daemon` + thin `router` CLI per the universal CLI shape).

## 1 · /257 findings status

The /257 audit treated `signal-persona-router` as "still on
signal_core; old universal-verb shape" and recommended a full
rewrite. Detailed status:

### /257 §1.1 — Universal-verb shape on operations

**Status: NOT FIXED on the working contract; FIXED on the owner
contract.**

`signal-persona-router/src/lib.rs:289-305`:

```rust
signal_channel! {
    channel Router {
        request RouterRequest {
            Match Summary(RouterSummaryQuery),
            Match MessageTrace(RouterMessageTraceQuery),
            Match ChannelState(RouterChannelStateQuery),
        }
        reply RouterReply { ... }
    }
}
```

The `Match` prefix is the retired universal-verb shape per
`intent/component-shape.nota` 2026-05-19T19:45:00Z. The
`request RouterRequest` grammar itself is the pre-`operation`
macro syntax — even after the rewrite to `operation Verb(...)`,
this whole channel will be reshaped.

`owner-signal-persona-router/src/lib.rs:292-298` already uses the
current shape:

```rust
signal_channel! {
    channel OwnerRouter {
        operation Grant(ChannelGrant),
        operation Extend(ChannelExtension),
        operation Revoke(ChannelRevocation),
        operation Deny(AdjudicationDenial),
    }
    ...
}
```

### /257 §1.2 — Doubling smell

**Status: NOT FIXED.** `Match Summary(RouterSummaryQuery)` and
`Match MessageTrace(RouterMessageTraceQuery)` and
`Match ChannelState(RouterChannelStateQuery)` — three flat
operation variants each carrying a `Router*Query` payload. Per
/150 §3 the target shape is

```rust
operation Query(Query),

pub enum Query {
    Summary(SummaryQuery),
    MessageTrace(MessageTraceQuery),
    ChannelState(ChannelStateQuery),
}
```

and the reply side collapses symmetrically:

```rust
reply Reply {
    Queried(QueryResult),
    Unimplemented(UnimplementedDetail),
}

pub enum QueryResult {
    Summary(Summary),
    MessageTrace(MessageTrace),
    MessageTraceAbsent(MessageTraceAbsence),
    ChannelState(ChannelState),
}
```

This is /257 §1.4 (lift the repeated category) and the worked
example for router in /257 §"signal-persona-router".

### /257 §1.5 — Ancestry-prefixed type names

**Status: NOT FIXED on working contract; PARTIALLY FIXED on owner
contract.**

Working contract `Router*` prefixes:
`RouterObservationId`, `RouterBootstrapOperation`,
`RouterBootstrapDocument`, `RouterObservationScope`,
`RouterSummaryQuery`, `RouterMessageTraceQuery`,
`RouterChannelStateQuery`, `RouterSummary`,
`RouterMessageTrace`, `RouterMessageTraceMissing`,
`RouterDeliveryStatus`, `RouterChannelState`,
`RouterChannelStatus`, `RouterObservationUnimplemented`,
`RouterObservationUnimplementedReason`,
`RouterDaemonConfiguration` (16 types).

These should all drop the `Router` prefix because the crate
namespace (`signal_persona_router::`) already supplies the context
— per /150 §3.3 the spec is `signal_persona_router::ObservationIdentifier`
not `signal_persona_router::RouterObservationIdentifier`.

The macro-emitted types (`RouterFrame`, `RouterFrameBody`,
`RouterRequest`, `RouterReply`, `RouterOperationKind`,
`RouterReplyKind`) come from the macro's channel-name parameter.
Per `intent/component-shape.nota` 2026-05-21T10:30:00Z and the
new macro emission shape in `signal-frame/macros/src/emit.rs`
(line 534-563, the `Frame` / `FrameBody` / `Request` /
`ReplyEnvelope` / `RequestBuilder` aliases), the macro now emits
clean unprefixed names. After the working contract migrates to
`signal-frame`, the prefixed forms retire.

Owner contract `OwnerRouter*` aliases at
`owner-signal-persona-router/src/lib.rs:309-314`:

```rust
pub type OwnerRouterRequest = OwnerRouterOperation;
pub type Frame = OwnerRouterFrame;
pub type FrameBody = OwnerRouterFrameBody;
pub type ChannelRequest = OwnerRouterChannelRequest;
pub type ChannelReply = OwnerRouterChannelReply;
pub type RequestBuilder = OwnerRouterRequestBuilder;
```

Same alias-dance /257 §1.10 / bead `primary-77hh` (macro prefix
drop) addresses. After the macro emits unprefixed types by
default, these aliases retire.

### /257 §1.6 — `*RequestUnimplemented { operation, reason }`

**Status: SPLIT — the working contract is clean by accident; the
owner contract has the smell.**

Working contract `RouterObservationUnimplemented` at
`signal-persona-router/src/lib.rs:274-278` carries
`scope: RouterObservationScope` plus
`reason: RouterObservationUnimplementedReason`. The `scope` field
is the same redundancy /257 §1.6 calls out — it restates the
operation position the reply already correlates with — except the
`scope` is more interesting than the bare `operation` field
because `RouterObservationScope` is a narrower enum than the full
operation root. With the §1.2 lift (`operation Query(Query)` with
a `Query` sum), `scope` would become genuinely redundant with the
request payload and should drop.

Owner contract `RequestUnimplemented` at
`owner-signal-persona-router/src/lib.rs:286-290`:

```rust
pub struct RequestUnimplemented {
    pub operation: OperationKind,
    pub reason: UnimplementedReason,
}
```

The `operation: OperationKind` field is exactly the redundancy
/257 §1.6 flags. Per the spirit fix in commit `d87e4055`, drop
the `operation` field; keep `reason` only. The
`OperationKind` enum at
`owner-signal-persona-router/src/lib.rs:267-275` then has only
one consumer (the `operation_kind()` method at line 316-324) and
that method itself is unused if the macro auto-generates
`OperationKind` per /257 §3.1 / bead `primary-77hh`.

### /257 §1.7 — Empty marker records

**Status: NOT PRESENT in either contract.** No empty struct
markers. ✓

### /257 §1.8 — Single-variant enums

**Status: NOT PRESENT.** All enums in both contracts have ≥2
variants today. (`EndpointKind` has 3, `RouterObservationScope` 3,
`RouterDeliveryStatus` 5, `RouterChannelStatus` 3, etc.)

### /257 §1.9 — `TimestampNanoseconds` excess precision

**Status: NOT FIXED.** `owner-signal-persona-router/src/lib.rs:42-65`
defines `TimestampNanoseconds(u64)` — nanosecond precision for
`ChannelDuration::TimeBound`. Per /257 §1.11 (and the
2026-05-20T18:44:49+02:00 spirit correction *"fuck nanoseconds —
fucking ridiculous"*), seconds suffice for any duration measured
in real-world authorization lifetimes. Rename to `Timestamp` with
second granularity.

### /257 §1.10 — Frame type alias boilerplate

**Status: NOT FIXED.** Owner contract has the 6-line alias dance
at `owner-signal-persona-router/src/lib.rs:309-314`. Per bead
`primary-77hh` (macro prefix drop) this retires once the macro
emits unprefixed names by default.

### /257 §1.11 — No observable block

**Status: NOT FIXED on either contract.** Neither
`signal_channel!` declaration carries an `observable` block.
Working contract observation channel needs it per the universal
mandate at `intent/component-shape.nota` 2026-05-20T02:00:00Z
*"Tap/Untap is mandatory for persona components, no author
override"* and `intent/persona.nota` 2026-05-21T10:00:00Z *"debug
the debugger!"* (every persona component is observable, including
the ones whose primary role is to observe others). Add to working
contract:

```rust
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

**Open question for the owner contract**: the owner channel
carries channel-policy orders (Grant / Extend / Revoke / Deny)
that arrive only from Orchestrate. Persona-introspect's purpose is
to observe cross-component activity; if introspect can already
observe the working-channel side of every grant/revoke (delivery
state changes, channel-state queries), does it also need to
observe the policy-channel surface? Designer lean: **yes, add the
observable block to the owner channel as well** — it matches the
universal mandate, and introspecting an authority-decision stream
separately from observation traffic is the kind of meta-debugging
the *debug-the-debugger* principle calls for. Confirm with psyche
before adding.

### /257 §1.13 — `supervision::` namespace stale

**Status: NOT FIXED.** Worse, the staleness has propagated into
the router daemon's configuration and supervision listener:

- `signal-persona-router/src/lib.rs:328-331`:
  `RouterDaemonConfiguration.supervision_socket_path` and
  `.supervision_socket_mode` — should be
  `engine_management_socket_path` /
  `engine_management_socket_mode` per /252.
- `persona-router/src/supervision.rs:11-16`: still imports
  `SupervisionFrame`, `SupervisionReply`, `SupervisionRequest`,
  `SupervisionProtocolVersion`, `GracefulStopAcknowledgement` from
  `signal-persona`. After /252 these become
  `EngineManagementFrame`, `EngineManagementReply`, etc.
- `persona-router/src/supervision.rs:36-46`:
  `SupervisionSocketMode`, `SupervisionListener`,
  `SupervisionProfile`, `SupervisionPhase` — local types named
  after the stale `supervision` vocabulary.
- `persona-router/src/router.rs:58-95`: `SupervisionListener`
  usage throughout daemon startup.

The rename touches both contracts plus six daemon files. /258
flagged this for the engine-manager triad; the router triad
inherits the staleness through the wire and the local types.

### /257 §3 — Bead coverage

The three building-block beads cover the router triad's
mechanical work:

- `primary-77hh` (frame alias-dance / macro prefix drop) — applies
  to `owner-signal-persona-router/src/lib.rs:309-314` and to
  whatever the working contract emits after migration.
- `primary-k3bu` (UnknownKindForVerb rename in consumers) —
  applies to `owner-signal-persona-router/src/lib.rs:106` and
  `:196` (hand-written codec impls; see §3.3).
- `primary-u0lh` (extend nota-codec derive coverage) — covers the
  same two hand-written impls and the `ChannelDuration` /
  `ChannelEndpoint` enums where mixed-enum derive now applies.

## 2 · New findings specific to this triad

### 2.1 — Working contract has only one channel (observation); the routing surface is missing

The current `signal-persona-router` declares a single channel:
the observation surface (`Summary`, `MessageTrace`,
`ChannelState`). It does NOT declare:

- a message-routing/delivery channel;
- a channel-grant/installation channel.

Per /150 §6.2 (the recommendation this audit was tasked to
verify) the router's public tree should separate three concerns:

> *Router should route messages and grants through contract-
> local operations, not old Sema verbs. Its public tree should
> separate: message routing / delivery; channel grants and
> revocations; observation / trace queries. Owner-only policy
> orders belong in `owner-signal-persona-router`. Ordinary
> callers should not even have owner-only variants in their
> contract.*

The current state collapses the three concerns:

- **Message routing** is currently inbound to the daemon via
  `signal-persona-message` frames (`StampedMessageSubmission`,
  `InboxQuery`). The router daemon directly accepts the
  message contract on its `router.sock` — see
  `persona-router/src/router.rs:1611-1640` where
  `RouterSignalInput` decodes `StampedMessageSubmission` or
  `SignalInboxQuery`. **Router has no native operation root for
  message handoff; it borrows message's contract types**.
- **Channel grants** are currently inbound from
  `signal-persona-mind` (the now-superseded direction). The
  daemon decodes `MindChannelGrant` and `MindAdjudicationDeny`
  through `signal-persona-mind`'s contract types (see
  `persona-router/src/router.rs:27-30` and `:1032-1058`).
- **Observation** is the only surface with its own contract
  operations.

Three problems with this shape:

1. **The working contract doesn't describe what the router does.**
   The daemon's actual public surface (accept stamped messages,
   answer inbox queries, apply channel grants, observe state) is
   spread across three external contracts; only one of those
   four operation families lives in `signal-persona-router`. A
   future agent reading the contract crate cannot tell from the
   contract what the router accepts.
2. **Channel grants enter the working channel.** Per
   `intent/component-shape.nota` 2026-05-20T13:30:00Z (the
   correction to the earlier Mind→Router direction): channel-
   policy orders (Grant / Extend / Revoke / Deny) move to
   `owner-signal-persona-router` and the CALLER is Orchestrate.
   The router daemon's current
   `ApplyMindChannelGrant`/`ApplyMindAdjudicationDeny` inputs
   should retire when Orchestrate stands up; the channel-grant
   intake should arrive over the owner socket. **The daemon
   already imports `owner-signal-persona-router` not** — see §2.5.
3. **The message-handoff surface should be router-local
   contract types**, not borrowed from `signal-persona-message`.
   Today the message ingress daemon (`persona-message`) frames
   `StampedMessageSubmission` onto router's
   `router.sock` directly — router's library re-exports
   `SignalMessageSubmission` as a router input. This is the
   triad invariant 2 question (*the daemon's external surface is
   exclusively signal-frame frames*): even though it IS signal-
   frame, the contract types-on-the-wire are from a different
   contract crate. The redesign question is whether router's
   "accept a stamped message" is its own operation
   (`operation Route(StampedMessage)`) or whether `persona-
   message` is the contract owner and router is just a peer
   destination — designer call, but the current shape (router
   library re-exporting message types as part of its public
   surface) is the worst of both: neither contract clearly owns
   the records.

The target shape per /150 §6 + 2026-05-20T13:30:00Z:

```rust
// signal-persona-router (the working contract):
signal_channel! {
    channel Routing {                    // peer-callable
        operation Route(StampedMessage),      // accept a stamped message
        operation Query(Query),               // observation queries
        operation Watch(Subscription) opens RoutingStream,
        operation Unwatch(SubscriptionToken),
    }
    reply Reply { Routed(RouteOutcome), Queried(QueryResult), ... }
    observable { ... }
}
```

```rust
// owner-signal-persona-router (the policy contract):
signal_channel! {
    channel ChannelPolicy {              // owner-only (called by Orchestrate)
        operation Grant(ChannelGrant),
        operation Extend(ChannelExtension),
        operation Revoke(ChannelRevocation),
        operation Deny(AdjudicationDenial),
    }
    reply Reply { ... }
    observable { ... }
}
```

The router daemon receives all three of (message routing, channel
policy, observation) — the working surface is the peer-callable
intersection (message handoff + observation), the policy surface
is owner-only authority.

### 2.2 — Daemon does not use signal-executor

`persona-router/Cargo.toml` depends on `signal-core`, not
`signal-frame` or `signal-executor`. Grep across
`persona-router/src/*.rs` finds zero `signal_executor::` imports,
zero `Lowering` impls, zero `CommandExecutor` impls, zero
`ToSemaOperation` impls, zero `ToSemaOutcome` impls.

This is the same gap /255 surfaced for spirit pre-migration and
/258 surfaced for the engine-manager triad. Spirit was migrated;
the others were not.

The migration pattern per /150 §7:

```rust
struct RouterLowering { ... }
impl Lowering for RouterLowering {
    type Operation = RoutingOperation;        // contract type after redesign
    type Reply = RoutingReply;
    type Command = RouterCommand;             // local enum
    type ComponentEffect = RouterEffect;      // local enum
    fn lower(...) -> Result<OperationPlan<RouterCommand>, RoutingReply> { ... }
    fn reply_from_effects(...) -> RoutingReply { ... }
}

struct RouterCommandExecutor { ... }
impl CommandExecutor for RouterCommandExecutor { ... }

impl BatchErrorClassification for RouterError { ... }
```

`RouterCommand` variants would be the typed daemon-internal
records the existing actor mesh already operates on
(`RegisterActor`, `RouteMessage`, `GrantRouteChannel`,
`InstallRouteStructuralChannels`, `RetractRouteChannel`, etc. —
already declared in `persona-router/src/router.rs:2189-2270` as
the `RouterInput` enum). The existing `RouterRoot` Kameo actor
becomes the engine inside a `CommandExecutor::execute_atomic_batch`
implementation.

`RouterEffect` variants would be the existing
`RouterOutput::ChannelGranted`, `MindChannelGrantApplied`,
`MindAdjudicationDenyApplied`, `Registered`, `DeliveryChanged`,
`ChannelRetracted`, `StructuralChannelsInstalled` records (per
`persona-router/src/router.rs:2363-2410`).

The work is non-trivial — router.rs is 2457 lines, the actor
mesh has 6 root actors and several specialised planes — but the
shape is mechanically the same as spirit's migration. The
**load-bearing structural next-slice item for the router triad**
along with §2.1's contract redesign.

### 2.3 — Daemon has no thin CLI binary; daemon binary parses flags

`persona-router/Cargo.toml:18-20`:

```toml
[[bin]]
name = "persona-router-daemon"
path = "src/main.rs"
```

One binary. No `src/bin/router.rs`. Per
`intent/component-shape.nota` 2026-05-20T13:00:00Z
(*"the naming of the CLI is just the name of the daemon minus
the daemon"*), the router triad should have **two** binaries:

- `persona-router-daemon` — the long-lived daemon.
- `router` — the thin CLI that translates one NOTA argument to a
  signal frame, sends it to one of the daemon's two sockets,
  prints the typed reply as NOTA.

Currently neither role is cleanly separated. The single
`persona-router-daemon` binary at `persona-router/src/main.rs`
dispatches between two paths:

- Typed configuration source (NOTA `(`-string or `.nota`/`.rkyv`
  file) → boots the daemon.
- Any other argv shape → calls `RouterCommandLine::from_env()`
  which then dispatches between `daemon` subcommand and `client`
  subcommand.

This is **multi-mode binary parsing** layered on the supposed
single-argument rule. Worse, the inner `RouterCommandLine` parser
accepts flags:

`persona-router/src/router.rs:1478-1505` — `RouterDaemonArguments`
parses `--socket <path>`, `--store <path>`, `--bootstrap <path>`.

`persona-router/src/router.rs:1560-1571` — `RouterClientArguments`
parses `--socket <path>` plus an inline-NOTA record argument.

Per `intent/component-shape.nota` 2026-05-19T01:23:00Z and the
`AGENTS.md` hard override *"No flags. No --verbose, no
--format=json, no --config=path"*: **no flags, ever**. The single
binary parsing flags is the canonical violation.

The migration: split the bin into two crates' worth of binary,
delete the entire `RouterCommandLine`, `RouterDaemonArguments`,
`RouterClientArguments`, `CommandLineArgument` machinery (~200
lines), and use the `signal_cli!` macro per
`reports/second-designer/129` for the generated route table.

The CLI's two-socket dispatch (working socket via working
contract operation heads; owner socket via owner contract
operation heads) is exactly the universal pattern from
2026-05-20T13:00:00Z and 2026-05-20T22:27:40+02:00.

### 2.4 — Daemon depends on signal-persona-mind, not on owner-signal-persona-router

`persona-router/Cargo.toml` depends on `signal-persona-mind` and
`signal-persona-message`. It does NOT depend on
`owner-signal-persona-router`. The daemon imports
`MindChannelGrant`, `MindAdjudicationDeny`, `MindChannelDuration`,
`MindChannelEndpoint` at `persona-router/src/router.rs:27-30`
and consumes them as the channel-grant intake (the
`RouterInput::ApplyMindChannelGrant`, `ApplyMindAdjudicationDeny`
variants at `:2267-2268`).

This is the now-superseded direction. Per
`intent/component-shape.nota` 2026-05-20T13:30:00Z:

> *I disagree that this means that the mine owns the router, the
> orchestrator owns the router. There's no need for the mind to
> take care of all of this low-level operation. This is
> orchestrator work. … Grant, Extend, Revoke, Deny correctly live
> in owner-signal-persona-router (destination is right); the
> caller is Orchestrate, not Mind.*

The current router daemon imports a Mind contract for the
authority intake — which means the daemon ITSELF carries the
flawed direction. After migration:

- The daemon depends on `owner-signal-persona-router` for the
  policy intake (Grant/Extend/Revoke/Deny payloads).
- The daemon's `MindChannelGrant` import retires.
- The `RouterInput::ApplyMindChannelGrant` enum variant becomes
  `RouterCommand::InstallChannelGrant(ChannelGrant)` (lowered
  from the contract `Grant(ChannelGrant)` operation).
- The mind→router direct grant path retires; Orchestrate becomes
  the only caller of the router's owner socket.

The current `MindAdjudicationOutbox` (the in-memory outbox where
parked messages collect typed `MindAdjudicationRequest` records
for eventual delivery to mind — `persona-router/src/adjudication.rs`)
also retires: when a message has no channel, the router
escalates to Orchestrate via Orchestrate's working channel; Mind
adjudicates cognitively; Orchestrate then orders Router back
through the owner socket with either `Grant` or `Deny`. The
router's local outbox is the placeholder for an actor mesh that
doesn't exist yet (per `persona-router/ARCHITECTURE.md:74-78`).

### 2.5 — `OperationKind` is hand-maintained on the owner contract

`owner-signal-persona-router/src/lib.rs:267-275`:

```rust
pub enum OperationKind {
    Grant,
    Extend,
    Revoke,
    Deny,
}
```

Plus the `operation_kind()` method on
`OwnerRouterOperation` at `:316-324`. Per bead `primary-77hh`
(macro auto-generates `OperationKind`), this entire enum + method
becomes macro-emitted. Until then it's the same drift risk /257
§3.1 flagged for every contract.

Per `intent/component-shape.nota` 2026-05-21T01:15:44+02:00:

> *"Macro auto-generates *OperationKind and From<Payload> for
> Reply impls."*

The owner contract has both — the `OperationKind` enum AND eight
hand-written `From` impls at lines 327-385. All structurally
derivable.

### 2.6 — `RequestUnimplemented.operation: OperationKind` redundancy

`owner-signal-persona-router/src/lib.rs:286-290`:

```rust
pub struct RequestUnimplemented {
    pub operation: OperationKind,
    pub reason: UnimplementedReason,
}
```

Per /257 §1.6 and the spirit fix in commit `d87e4055`: the
`operation` field restates information the reply already carries
positionally (the per-operation `SubReply` correlates with the
source operation by position). Drop the `operation` field.

### 2.7 — Hand-written codec impls when mixed-enum derive applies

`owner-signal-persona-router/src/lib.rs:67-202` hand-rolls
`NotaEncode` + `NotaDecode` impls for two enums:

- `ChannelEndpoint { Internal(ComponentName), External(ConnectionClass) }`
  at lines 67-112 (45 lines of hand-written codec).
- `ChannelDuration { OneShot, Permanent, TimeBound(TimestampNanoseconds) }`
  at lines 149-202 (53 lines).

Both are mixed enums (unit variants + tuple-payload variants).
With the recent `nota-codec` mixed-enum support (per `intent/nota-
mixed-enum-support.nota` and bead `primary-u0lh`, surfaced by the
engine-manager triad audit since dropped), these should be
`#[derive(NotaSum)]` or `#[derive(NotaEnum)]` depending on the
variant set. The two hand-rolled impls retire.

Both impls also use `nota_codec::Error::UnknownKindForVerb`
at lines 106 and 196 — bead `primary-k3bu` rename target.

### 2.8 — `ChannelMessageKind` is a closed 12-variant enum

`owner-signal-persona-router/src/lib.rs:117-147`:

```rust
pub enum ChannelMessageKind {
    MessageIngressSubmission,
    MessageSubmission,
    InboxQuery,
    FocusObservation,
    PromptBufferObservation,
    MessageDelivery,
    TerminalInput,
    TerminalCapture,
    TerminalResize,
    TranscriptEvent,
    AdjudicationRequest,
    DeliveryNotification,
}

impl ChannelMessageKind {
    pub const ALL: [Self; 12] = [ ... ];
}
```

Per /257 §1.13 open question #4 (*Closed `ChannelMessageKind`
enum agent-cultivated per /249 gap #22*): designer/psyche call.
Twelve hard-coded message kinds spanning every typed channel
message in the workspace — adding a new contract message kind
requires editing this enum. This is the "schema as agent-managed
table" shape /237 critiqued; the alternative is treating channel-
message-kind as data (a string token resolved at runtime against
the per-contract enums each contract exposes).

Designer lean: keep the closed enum for the prototype while the
contract set is small (12 kinds is still maintainable). When the
workspace grows past ~20 kinds, revisit. Flagging for psyche
attention because changing this shape later requires migrating
every grant record's `kinds: Vec<ChannelMessageKind>` field.

### 2.9 — `Deny` operation variant carries `AdjudicationDenial`, not a channel-typed denial

`owner-signal-persona-router/src/lib.rs:294-298`:

```rust
operation Grant(ChannelGrant),
operation Extend(ChannelExtension),
operation Revoke(ChannelRevocation),
operation Deny(AdjudicationDenial),
```

Three of the four operations carry channel-typed payloads
(`ChannelGrant`, `ChannelExtension`, `ChannelRevocation`). The
fourth — `Deny` — carries `AdjudicationDenial`, which has fields
`request: AdjudicationRequestIdentifier` and `reason: TextBody`.

Read directly: `Deny(AdjudicationDenial)` is "deny an
adjudication request" — the upstream Mind∶adjudication has
escalated a parked message and Orchestrate orders Router to
record a deny verdict. This is a different conceptual operation
from Grant/Extend/Revoke (which mutate channel records).

Two ways to read this:

- **It's structurally correct.** Adjudication is the prerequisite
  flow for Grant — when Mind decides a channel can't exist,
  Orchestrate tells Router to record the denial so the message
  retries don't keep escalating. Deny IS a separate verb because
  the operation targets a request-id, not a channel record.
- **It's a missing schema layer.** Adjudication is a
  sub-concern within the channel-policy family; the schema would
  read more clearly with:

  ```rust
  operation Adjudicate(Adjudication),

  pub enum Adjudication {
      Approve(ChannelGrant),       // alias for Grant
      Deny(AdjudicationDenial),
  }

  // ... or kept separate ...

  operation Grant(ChannelGrant),
  operation Extend(ChannelExtension),
  operation Revoke(ChannelRevocation),
  operation DenyAdjudication(AdjudicationDenial),  // verb names what it acts on
  ```

  The second form makes the verb-payload pair self-naming —
  `DenyAdjudication(AdjudicationDenial)` reads "the receiver
  denies the adjudication" instead of "the receiver denies
  [something]" where the [something] is only clear from the
  payload type.

Designer lean: rename the variant to `DenyAdjudication` and keep
the payload — the compound is a single atomic verb per
2026-05-19T21:15:00Z (*compound contract verbs are fine when the
action they name doesn't decompose into separate verbs cleanly*).
Confirm with psyche.

### 2.10 — `AdjudicationRequestIdentifier` keeps full ancestry

`owner-signal-persona-router/src/lib.rs:16-25`:

```rust
pub struct AdjudicationRequestIdentifier(String);
```

Per /257 §"owner-signal-persona-router": rename to
`AdjudicationId` or simply `RequestId` (channel-grant
adjudication is the contract's domain — the type name doesn't
need to spell out the full ancestry). `Identifier` already
clarifies the type's role.

Designer lean: `AdjudicationId` reads cleanly within the contract.
`Id` is a borderline acronym per `skills/naming.md`
§"Permitted exceptions" #4 — the psyche has been explicit that
*"identifier is actually better"* than `id`. Use
`AdjudicationIdentifier` to satisfy both rules.

### 2.11 — `RouterBootstrapDocument` records on the working contract

`signal-persona-router/src/lib.rs:153-187` declares
`RouterBootstrapDocument` and `RouterBootstrapOperation` (with
variants `RegisterActor`, `GrantDirectMessage`,
`InstallStructuralChannels`). These are bootstrap-policy records.

Per `intent/component-shape.nota` 2026-05-19T01:30:00Z and the
component-triad invariant 5 (*policy state bootstraps once from
`bootstrap-policy.nota` in the component repo*), bootstrap records
belong in the **policy state** and the bootstrap file format
should mirror the OWNER signal contract's records, not the
working contract.

Today's router bootstrap declares actor registrations and
structural channel installations — both of which are policy /
configuration state (which actors exist, which structural channels
exist). With the §2.1 redesign, these records move into
`owner-signal-persona-router` and the working contract carries
only message-routing + observation + Tap.

The bootstrap reading machinery (`from_nota_lines` /
`to_nota_lines` at lines 171-186) also predates the standard
bootstrap-policy reading discipline (per `component-triad.md`
§"5. Policy state and working state"). Bootstrap is the one-shot
file read at daemon first start; the contract doesn't need its
own reader machinery — the daemon's bootstrap reader uses the
contract's record types directly.

### 2.12 — `RouterDaemonConfiguration` carries supervision-stale fields

`signal-persona-router/src/lib.rs:322-340`:

```rust
pub struct RouterDaemonConfiguration {
    pub router_socket_path: WirePath,
    pub router_socket_mode: SocketMode,
    pub supervision_socket_path: WirePath,
    pub supervision_socket_mode: SocketMode,
    pub store_path: WirePath,
    pub bootstrap_path: Option<WirePath>,
    pub owner_identity: OwnerIdentity,
}
```

Three issues:

- `supervision_socket_*` should be `engine_management_socket_*`
  per /252 (the engine-manager rename).
- The configuration record currently exposes ONE socket
  (`router_socket_path`). The post-migration shape needs TWO
  sockets: working (`working_socket_path`) and policy
  (`owner_socket_path`). Per `intent/component-shape.nota`
  2026-05-20T13:00:00Z (*"Every CLI is going to use two
  sockets"*) and the universal `signal_cli!` macro shape, the
  daemon binds both.
- After the §2.1 redesign, the configuration carries the
  bootstrap path for the OWNER signal contract's records (channel
  policy), not the working contract.

### 2.13 — `RouterObservationId` and `ActorId` overlap with daemon identity types

Working contract `RouterObservationId(String)` at
`signal-persona-router/src/lib.rs:19` and `ActorId(String)` at
`:34` — both are wire-record-bearing newtypes.

The daemon also defines `ActorId` in
`persona-router/src/message.rs` (re-exported via `lib.rs:35`). The
contract's `ActorId` is the same shape but lives separately in
the contract crate. Per /257 §1.12 (name collisions across
contracts), the workspace-wide question is whether to inline-
duplicate or extract to `signal-persona` / `signal-persona-auth`.

The clean answer for router: actor identity is router-domain
data. Per the routing redesign, the actor-id type lives in the
working contract (`signal-persona-router::ActorIdentifier`) and
the daemon imports it. The daemon's `ActorId` retires.

### 2.14 — Bespoke supervision listener will become dead code

`persona-router/src/supervision.rs` (334 lines) is a hand-rolled
sync Unix-socket listener for the supervision/engine-management
protocol, separate from the main Kameo actor tree. After /252
(engine-management rename) and after the engine-manager triad
adopts signal-executor (per /258), every component daemon's
supervision listener becomes either:

- The standard engine-management listener emitted by a future
  shared library (`signal-persona`'s engine_management module),
  or
- Eliminated in favor of the daemon binding its own working
  socket and letting the engine-manager component query it via
  the daemon's normal signal channel.

For now this file is partial duplication; flagging it so the
router migration absorbs the engine-manager-rename pass too.

## 3 · Owner signal audit

The owner contract is the most-current leg of the triad. The
positive points first, then the gaps:

### What's right

- **`signal-frame` dependency.** Current substrate.
- **Contract-local verbs in verb form.** `Grant`, `Extend`,
  `Revoke`, `Deny` — all verbs the receiver does on its inputs.
  Per /150 §6 and `intent/component-shape.nota` 2026-05-19T19:30Z,
  this is the right shape.
- **Caller-direction is correct (per the most recent intent).**
  The crate's doc-comment at `:1-6` explicitly states: *"Ordinary
  router observation traffic lives in `signal-persona-router`.
  This crate carries Orchestrate-to-Router owner-only channel
  authority orders. Mind-level decisions reach Router through
  Orchestrate, not by calling this contract directly."* — aligns
  with 2026-05-20T13:30:00Z exactly.
- **Payload records cleanly named.** `ChannelGrant`,
  `ChannelExtension`, `ChannelRevocation`, `AdjudicationDenial` —
  no ancestry prefixes within the crate's domain (Channel is the
  domain noun, not the namespace).
- **Reply variants in past-tense outcome form.** `ChannelGranted`,
  `ChannelExtended`, `ChannelRevoked`, `AdjudicationDenied` — the
  past-tense paired with the request verb. Clean.
- **`ChannelOrderRejected` for typed rejection.** Carries
  `ChannelOrderRejectionReason` (5 variants: owner-authority,
  channel-already-exists, channel-missing,
  adjudication-request-missing, policy-refused). Honest typed
  rejection per /150 §3 / /258 § "Engine atomic failures stay in
  Reply::Accepted".

### What's wrong

- **No observable block** (§1 /257 §1.11). Per
  `intent/component-shape.nota` 2026-05-20T02:00:00Z + 2026-05-21
  Clarification on debug-the-debugger, owner channels of persona
  components also support Tap/Untap. Open psyche call (lean: yes).
- **Alias-dance at the bottom of the crate** (§1 /257 §1.10). The
  six `OwnerRouter*` aliases at lines 309-314 — retires when bead
  `primary-77hh` lands.
- **Hand-written `OperationKind` enum + `operation_kind()`
  method** (§2.5). Auto-generated per bead `primary-77hh`.
- **Eight hand-written `From<Payload> for Reply` impls** (lines
  327-385). Auto-generated per the same bead.
- **`RequestUnimplemented.operation: OperationKind` redundancy**
  (§2.6). Drop the field.
- **Two hand-written codec impls on `ChannelEndpoint` and
  `ChannelDuration`** (§2.7). Replace with mixed-enum derive.
- **`TimestampNanoseconds` excess precision** (§1 /257 §1.9).
  Lower to seconds.
- **`AdjudicationRequestIdentifier` over-prefixed** (§2.10).
  Rename to `AdjudicationIdentifier`.
- **`Deny(AdjudicationDenial)` verb-payload pair reads
  ambiguously** (§2.9). Designer lean: `DenyAdjudication(AdjudicationDenial)`.
- **No reply variant for adjudication-grant**. The current
  reply tree has `ChannelGranted`, `ChannelExtended`,
  `ChannelRevoked`, `AdjudicationDenied`, `ChannelOrderRejected`,
  `RequestUnimplemented`. There's no `AdjudicationApproved` /
  `AdjudicationGranted` — presumably because an approval IS a
  channel grant (the approval IS the `Grant` operation, and the
  reply IS `ChannelGranted`). This needs documentation in the
  contract because the asymmetry (Deny replies with
  `AdjudicationDenied`; Approve has no `AdjudicationApproved`
  twin) is non-obvious.

### Open scope question

The owner contract's `OperationKind::Deny` participates in the
typed rejection path (`ChannelOrderRejected.operation:
OperationKind` at line 252). If the macro auto-generates
`OperationKind`, the rejection-classification consumer becomes
the macro-emitted enum. This is structurally fine.

## 4 · Recommended next slice for the router triad

In priority order:

1. **Owner-contract cleanup** (small, mostly already-current).
   - Drop the alias-dance (when `primary-77hh` lands).
   - Drop the redundant `RequestUnimplemented.operation` field.
   - Replace hand-written codec impls with mixed-enum derive.
   - Rename `AdjudicationRequestIdentifier` →
     `AdjudicationIdentifier`.
   - Lower `TimestampNanoseconds` → `Timestamp` (seconds).
   - Resolve §2.9 verb-name ambiguity (`Deny` →
     `DenyAdjudication`).
   - Add `observable` block (pending psyche call).
2. **Working contract full redesign** per §2.1 + /150 §6.2.
   - Replace the single observation channel with the three-
     surface split: message routing + observation in the working
     contract; channel policy in the owner contract.
   - Lift the `Match Summary/Trace/ChannelState` triad to
     `operation Query(Query)` per /257 §1.4 + /150 §3.
   - Drop the `Router*` ancestry from all 16 types.
   - Migrate the bootstrap records to the owner contract.
   - Migrate the `RouterDaemonConfiguration` to two sockets and
     post-/252 field names.
   - Add `observable` block to both channels.
3. **Daemon migration onto signal-executor** (§2.2). The
   structural piece. Same shape as spirit's `786ab311` migration.
   - Define `RouterCommand` / `RouterEffect` enums.
   - Implement `Lowering` for the routing+observation+policy
     surfaces.
   - Wrap the existing `RouterRuntime` actor mesh in a
     `CommandExecutor`.
   - Implement `BatchErrorClassification` for `RouterError`.
   - Wire `signal_executor::Executor::execute(request).await` for
     both sockets.
4. **Binary split + thin CLI** (§2.3). Add
   `src/bin/router.rs` using the `signal_cli!` macro per
   `reports/second-designer/129`. Rename `persona-router-
   daemon` to keep the `-daemon` suffix discipline. Delete the
   entire `RouterCommandLine` + `RouterDaemonArguments` +
   `RouterClientArguments` flag-parsing machinery (~200 lines).
5. **Authority intake rewiring** (§2.4). The daemon depends on
   `owner-signal-persona-router` not `signal-persona-mind`.
   `MindChannelGrant` / `MindAdjudicationDeny` imports retire;
   `RouterInput::ApplyMindChannelGrant` /
   `ApplyMindAdjudicationDeny` enum variants retire. The
   in-memory `MindAdjudicationOutbox` retires (the escalation
   path goes through Orchestrate's working channel, not router-
   local state).
6. **Supervision rename** (§1 /257 §1.13 + 2.14). The
   `supervision.rs` file + every `Supervision*` type renames
   per /252.

Beads worth filing (subject to psyche approval):

- A new bead "Migrate persona-router triad onto current
  substrate" modeled on spirit's migration template. The work is
  larger than spirit's (the daemon is 2457 lines of router.rs
  alone) but the shape is identical.

## 5 · References

### Workspace authority

- `intent/component-shape.nota` 2026-05-19T01:23:00Z — NOTA is
  the only argument language; no flags.
- `intent/component-shape.nota` 2026-05-19T19:30:00Z — contract-
  local verbs replace universal-verb prefixes.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z — Tap/Untap
  mandatory for persona components.
- `intent/component-shape.nota` 2026-05-20T12:11:26Z — triad =
  daemon + working signal + owner signal; CLI is bundled
  machinery, not a leg.
- `intent/component-shape.nota` 2026-05-20T13:00:00Z — CLI
  naming + two argument shapes + pure NOTA↔Signal bridge +
  env-var carve-out + two-socket dispatch.
- `intent/component-shape.nota` 2026-05-20T13:30:00Z — Orchestrate
  owns Router; Mind does not. The earlier Mind-to-Router framing
  is superseded.
- `intent/component-shape.nota` 2026-05-21T01:15:44+02:00 —
  signal_channel! macro generates `OperationKind` + From<Payload>
  for Reply.
- `intent/component-shape.nota` 2026-05-21T10:30:00Z — macros
  emit clean unprefixed names; modules disambiguate.
- `intent/persona.nota` 2026-05-20 17:30 — router as channel
  gate; reachability-query semantics; default mind-channel
  open.
- `intent/persona.nota` 2026-05-21T10:00:00Z — debug-the-debugger
  (every persona component, including observation-purpose ones,
  is itself observable).
- `intent/signal.nota` 2026-05-20T17:10:00Z — persona-spirit
  pilot complete; signal/sema convergence available.
- `intent/naming.nota` 2026-05-19T18:50:00Z — repeated category
  words indicate missing parent enum.
- `ESSENCE.md` §Naming — full-English-words + no-ancestry pair.
- `skills/component-triad.md` — five invariants + single-
  argument rule.
- `skills/naming.md` — full-English + no-ancestry pair-of-rules.
- `skills/reporting.md` — report discipline.

### Prior reports

- `reports/designer/257-signal-contracts-names-and-shape-audit.md`
  — workspace-wide audit; classifies router as "still on
  signal_core; old universal-verb shape" with worked example.
- `reports/operator/150-triad-signal-sema-migration-current-state.md`
  — current substrate handoff; §6.2 (router public tree
  three-surface separation) is the audit task's anchor.
- `reports/second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md`
  — eight-principle guideline; principles 2 (tree-not-table),
  4 (no ancestry), 5 (verbs name what the receiver does), 6
  (working ≠ policy), 7 (mind/body owner-verb level) all apply
  to the router redesign.
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  — the `signal_cli!` macro sketch for two-socket dispatch; the
  router CLI uses this.

### Code under audit

- `/git/github.com/LiGoldragon/signal-persona-router/src/lib.rs`
  (340 lines).
- `/git/github.com/LiGoldragon/signal-persona-router/Cargo.toml`
  (depends on `signal-core`, stale).
- `/git/github.com/LiGoldragon/owner-signal-persona-router/src/lib.rs`
  (385 lines).
- `/git/github.com/LiGoldragon/owner-signal-persona-router/Cargo.toml`
  (depends on `signal-frame`, current).
- `/git/github.com/LiGoldragon/persona-router/src/main.rs` (33
  lines).
- `/git/github.com/LiGoldragon/persona-router/src/lib.rs` (65
  lines re-export hub).
- `/git/github.com/LiGoldragon/persona-router/src/router.rs`
  (2457 lines).
- `/git/github.com/LiGoldragon/persona-router/src/channel.rs`
  (655 lines).
- `/git/github.com/LiGoldragon/persona-router/src/observation.rs`
  (224 lines).
- `/git/github.com/LiGoldragon/persona-router/src/supervision.rs`
  (334 lines).
- `/git/github.com/LiGoldragon/persona-router/Cargo.toml`
  (depends on `signal-core` + `signal-persona-mind`, both
  superseded for this surface).

### Beads referenced (no new beads filed per task constraint)

- `primary-77hh` — macro prefix drop + `OperationKind` /
  `From<Payload>` auto-generation.
- `primary-k3bu` — `UnknownKindForVerb` rename in consumers.
- `primary-u0lh` — extend nota-codec derive coverage.

This report retires when (a) the working contract is redesigned
per §2.1, AND (b) the daemon migrates onto signal-executor with
the binary split and authority rewiring (§2.2 / §2.3 / §2.4),
OR (c) a successor audit supersedes.
