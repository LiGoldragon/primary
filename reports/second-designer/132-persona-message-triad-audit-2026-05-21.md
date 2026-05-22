# 132 — persona-message triad audit (working + missing policy)

*Audit of the persona-message triad: `signal-persona-message` (the
working contract) + `persona-message` (the daemon + `message` thin
CLI). The `owner-signal-persona-message` repository **does not
exist**; this report proposes its signal-type names and signal-tree
shape under the universal owner-contract Decision
(`intent/component-shape.nota` 2026-05-20T12:11:26Z). Spirit and
the mind owner contract are the migrated templates; persona-message
has not yet been touched by the signal-frame / contract-local-verb
/ signal-executor migration arc that landed for spirit
(/255 / /256) and was carried forward by /258 for engine-manager.*

## 0 · TL;DR

The persona-message triad is the engine's text-boundary ingress:
agents and the bundled CLI hand NOTA `Send` / `Inbox` records to
the daemon; the daemon stamps origin/time and forwards
`StampedMessageSubmission` frames to `persona-router`. The daemon
is stateless. Its working contract is small (three operation
variants, four reply variants) and is the smallest persona contract
still on the old shape.

State summary:

- `signal-persona-message` is **stale on `signal-core`** with the
  universal-verb shape (`Assert MessageSubmission`,
  `Assert StampedMessageSubmission`, `Match InboxQuery`). The
  contract has not been migrated to `signal-frame` + contract-local
  verbs. The `ARCHITECTURE.md` "MUST IMPLEMENT — three-layer
  migration" section names the target but the implementation has
  not landed. (`signal-persona-message/src/lib.rs:16,271-285`;
  `signal-persona-message/ARCHITECTURE.md:7-55`.)
- **No `observable` block** — persona-message is a persona
  component, so Tap/Untap is mandatory per
  `intent/component-shape.nota` 2026-05-20T02:00:00Z and
  `intent/persona.nota` 2026-05-21T10:00:00Z (*"debug the
  debugger"*).
- **`Message*` ancestry prefix on most types** —
  `MessageRecipient`, `MessageSender`, `MessageBody`, `MessageSlot`,
  `MessageKind`, `MessageSubmission`, `MessageOperationKind`,
  `MessageRequestUnimplemented`, `MessageUnimplementedReason`,
  `MessageDaemonConfiguration`, `MessageChannel`, `MessageRequest`,
  `MessageReply`. The crate name supplies "message"; the prefix is
  redundant per ESSENCE §Naming.
- **`MessageRequestUnimplemented { operation, reason }`** —
  carries a redundant `operation` field (the same /257 §1.6 smell
  fixed in spirit at `d87e4055`).
- **`StampedMessageSubmission` carries `TimestampNanos`** —
  nanosecond precision on an ingress stamp is excessive; the
  designer lean across the workspace (/258 §2.1, /257 §1.11) is to
  drop to seconds for runtime-stamped protocol timestamps.
- **Daemon does not use `signal-executor`** — `persona-message`'s
  `Cargo.toml` lists `signal-core`, not `signal-frame` /
  `signal-executor`. The daemon dispatches through an ad-hoc Kameo
  actor mesh (`MessageDaemonRoot`) and a hand-rolled frame codec
  (`persona-message/src/router.rs:1-100`,
  `persona-message/src/daemon.rs:1-167`). Same gap as /258 §2.2 for
  engine-manager — but persona-message is structurally simpler
  (stateless, no atomic batch), so the executor migration is
  smaller.
- **One operation per request (degenerate atomicity)** — explicit
  per the ARCH (line 167-168). With `signal-executor`, multi-
  operation batches reject before commit until the component has a
  real transaction boundary; persona-message never gets a real
  transaction boundary because it has no durable state. The
  executor invariant is degenerate-but-honest, like spirit's.
- **Supervision module is `Supervision*` not `EngineManagement*`**
  (`persona-message/src/supervision.rs:13-19`,
  `persona-message/src/daemon.rs:29-30`). Same /252-stale rename
  scope flagged in /258 §1.13.
- **Two CLI environment variables** — `PERSONA_MESSAGE_SOCKET` /
  `PERSONA_SOCKET_PATH` (`persona-message/src/router.rs:34-38`).
  Two variables instead of the single env-var carve-out per
  `intent/component-shape.nota` 2026-05-20T13:00:00Z. The CLI also
  predates the two-socket (working + policy) dispatch rule, so
  there is no policy-socket override path at all today.
- **No CLI dispatch macro** — `persona-message/src/main.rs` is a
  hand-written three-line dispatch. The `signal_cli!` macro
  affirmed at `intent/component-shape.nota` 2026-05-20T22:27:40Z
  has not been applied here.

**Missing leg — the policy signal.** The triad's third leg
(`owner-signal-persona-message`) does not exist. §3 below proposes
its signal-tree shape: socket-binding policy (rebind the ingress
socket with new mode), router-peer policy (point at a different
router socket), ingress allow-list policy
(`ComponentMessageIngress` mutation), and the open lifecycle
question per `intent/component-shape.nota` 2026-05-20T13:45:00Z.

**Priority for the triad's migration slice**: (1) propose the
owner contract shape (this report); (2) execute the working-
contract three-layer migration (signal-core → signal-frame,
contract-local verbs, observable, drop ancestry, drop
`*RequestUnimplemented.operation`); (3) implement owner contract
once the working migration is settled and §3 has psyche approval;
(4) daemon onto signal-executor + signal_cli; (5) /252 supervision
rename.

## 1 · /257 findings status

### /257 §1.1 — old universal-verb shape

**Status: NOT FIXED.** The working contract still uses
`Assert MessageSubmission`, `Assert StampedMessageSubmission`,
`Match InboxQuery`. (`signal-persona-message/src/lib.rs:271-285`.)

The contract-local verb redesign target is:

```rust
signal_channel! {
    channel Message {
        operation Send(Submission),       // was Assert MessageSubmission
        operation Deliver(StampedSubmission), // was Assert StampedMessageSubmission
        operation Inbox(InboxQuery),      // was Match InboxQuery
    }
    reply Reply {
        Submitted(SubmissionAcceptance),
        SubmitRejected(SubmissionRejection),
        Listed(InboxListing),
        RequestUnimplemented(RequestUnimplemented),
    }
    observable {
        filter default;
        operation_event OperationReceived;
        effect_event EffectEmitted;
    }
}
```

`signal-persona-message/ARCHITECTURE.md` lines 13-23 already name
`Submit`/`Deliver`/`Query` as the three contract-local verbs. This
report's lean refines `Query` to `Inbox` because the contract has
only one read shape — inbox-by-recipient — and `Inbox` reads as
the action the receiver does (look up the inbox); `Query` is the
right name only when the read surface needs a parent enum
(per /257 §1.4 + skills/naming.md §"repeated category words"). One
read surface, name it for what it reads.

Designer lean: prefer `Inbox(InboxQuery)` over `Query(InboxQuery)`
for this contract; lift to `Query(Query)` only when a second read
shape appears.

### /257 §1.2 — doubling smell

**Status: NOT PRESENT in target.** The current shape has
`Assert MessageSubmission(MessageSubmission)` — Sema-verb-prefix +
typename = payload-typename = the doubling smell. The migrated
shape (`operation Send(Submission)`) drops it.

### /257 §1.3 — `Mutate <Verb>` grammatically wrong

**Status: NOT PRESENT.** The current contract has no `Mutate`
variants.

### /257 §1.4 — repeated-suffix smell

**Status: NOT PRESENT.** The reply enum's four variants
(`SubmissionAccepted`, `SubmissionRejected`, `InboxListing`,
`MessageRequestUnimplemented`) do not share a suffix that would
indicate a missing parent enum. The two `Submission*` variants are
the request/rejection pair on the same operation, which is the
contract pattern, not the repeated-category smell.

### /257 §1.5 — ancestry prefixes

**Status: NOT FIXED.** Persona-message is one of the worst
offenders on this rule. Inside the `signal-persona-message` crate,
the crate name already supplies "message" — every `Message*`
prefix is redundant ceremony.

Rename list (drop `Message` prefix where present):

| Current | Target |
|---|---|
| `MessageRecipient` | `Recipient` |
| `MessageSender` | `Sender` |
| `MessageBody` | `Body` |
| `MessageSlot` | `Slot` |
| `MessageKind` | `Kind` |
| `MessageSubmission` | `Submission` |
| `MessageOperationKind` | `OperationKind` (macro-emitted) |
| `MessageRequestUnimplemented` | `RequestUnimplemented` |
| `MessageUnimplementedReason` | `UnimplementedReason` |
| `MessageDaemonConfiguration` | `DaemonConfiguration` |
| `MessageChannel` (macro arg) | `Message` |
| `MessageRequest` (macro emit) | `Operation` (post macro-rename) |
| `MessageReply` (macro emit) | `Reply` |
| `MessageRequestBuilder` (alias) | `RequestBuilder` |

**Caveats**:

- `MessageSlot`, `MessageSender`, `MessageBody` are imported by
  `signal-persona-router` (`signal-persona-router/src/lib.rs:14,
  206, 234, 244` for `MessageSlot`). After the rename, callers
  write `signal_persona_message::Slot`, `Sender`, `Body`.
  Cross-contract name reuse (`signal-persona-harness` also defines
  `MessageSender` / `MessageBody` / `MessageSlot` per /257 §1.12)
  becomes the type-system disambiguator's job:
  `use signal_persona_message::Sender as MessageSender;` at the
  consumer when collision matters. The /257 lean is
  inline-duplication; designer agrees here.
- `MessageOriginStamper`, `MessageIngressContext`,
  `MessageIngressAuthority`, `MessageSocketBinder` are daemon-side
  types (in `persona-message/src/daemon.rs`), not contract types.
  The daemon's domain noun IS "message" (the runtime's job is
  message ingress), so the prefix is meaningful — Origin alone is
  ambiguous; MessageOrigin reads. Keep the daemon-side prefixes
  where they describe what the daemon does, not what its crate is
  called. Apply ESSENCE §Naming case-by-case at the daemon
  boundary; the contract is the clear-cut case.

### /257 §1.6 — `*RequestUnimplemented { operation, reason }`

**Status: NOT FIXED.** `MessageRequestUnimplemented` carries
`operation: MessageOperationKind` and `reason:
MessageUnimplementedReason`
(`signal-persona-message/src/lib.rs:190-194`). Same smell spirit
fixed in `d87e4055`. Per-operation replies are positionally
aligned with the request; the caller already knows which operation
produced this reply. Drop the `operation` field; keep `reason`
only.

Post-rename target:

```rust
pub struct RequestUnimplemented {
    pub reason: UnimplementedReason,
}
```

`MessageOperationKind` becomes macro-emitted `OperationKind` per
the `signal-frame` macro change (`intent/component-shape.nota`
2026-05-21T01:15:44+02:00).

### /257 §1.7 — empty marker records

**Status: NOT PRESENT.** Persona-message has no empty marker
structs. The `MessageKind { Send, Inbox }` is correctly a unit
enum already.

### /257 §1.8 — single-variant enums

**Status: PARTIALLY PRESENT.**
`DependencyKind { Router, Mind, Harness, Terminal }` has four
variants — not a problem. `ResourceKind { MessageSocket,
RouterSocket, PeerCredentials, Store }` has four — fine. The
`MessageKind { Send, Inbox }` has two — fine. **Watch
`SubmissionRejectionReason { StoreRejected, RecipientNotFound }`**:
two variants, both load-bearing, fine. No collapse candidates.

### /257 §1.9 — frame type alias boilerplate

**Status: NOT FIXED.** Lines 287-291 of `lib.rs`:

```rust
pub type Frame = MessageChannelFrame;
pub type FrameBody = MessageChannelFrameBody;
pub type ChannelRequest = MessageChannelChannelRequest;
pub type ChannelReply = MessageChannelChannelReply;
pub type MessageRequestBuilder = MessageChannelRequestBuilder;
```

Five lines of alias-dance to drop the channel-name prefix. Fixed
by the `signal-frame-macros` prefix-drop change per
`intent/component-shape.nota` 2026-05-21T10:30:00Z (the macro
emits unprefixed names by default; the alias block disappears).

### /257 §1.10 — no observable block

**Status: NOT FIXED.** The persona-message contract has no
`observable` block. The macro does not inject `Tap`/`Untap`. The
daemon has no Tap surface — agents cannot subscribe to observe
message ingress flow.

This is **mandatory** per `intent/component-shape.nota`
2026-05-20T02:00:00Z and reaffirmed by `intent/persona.nota`
2026-05-21T10:00:00Z (the universal Tap/Untap mandate applies to
introspect itself; the principle is universal).

Add (in the post-rename shape):

```rust
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

The macro injects `Tap(ObserverFilter)` and
`Untap(ObserverSubscriptionToken)`. The daemon implements the
runtime side per spirit's pattern (today's spirit accepts Tap/Untap
on the wire and returns `RequestUnimplemented` /
`SemaOutcome::NoChange` per the no-op-as-explicit-command rule,
per `intent/persona.nota` 2026-05-20T20:00:00Z; live fanout waits
for persona-introspect). The placeholder shape is the right shape
to land for persona-message too.

### /257 §1.11 — single-field timestamps (and excess precision)

**Status: NOT FIXED.** `StampedMessageSubmission.stamped_at:
TimestampNanos` (line 118). The contract imports `TimestampNanos`
from `signal-persona` — a u64 of nanoseconds since UNIX epoch.

Per psyche correction at `intent/persona.nota`
2026-05-20T18:44:49+02:00 (*"fuck nanoseconds — fucking
ridiculous"*) and the designer lean from /258 §1.12 + /257 §1.11,
runtime/protocol timestamps should drop to seconds. For ingress
stamping, the consumer (router) cares about ordering and
provenance, not sub-second precision; seconds suffice.

Designer lean: change to `TimestampSeconds(u64)` (named in
`signal-persona` per /257 §1.11 to keep the universal timestamp
type there). Confirm via the open psyche call in /258 §1.12.

### /257 §1.12 — name collisions across contracts

**Status: NOT FIXED.** `MessageSender`, `MessageBody`,
`MessageSlot` are defined here AND duplicated in
`signal-persona-harness` per /257 §1.12. Designer lean
(inline-duplication-is-fine — each contract owns its types; the
consumer disambiguates by `as` rename). Keep duplication after the
ancestry-prefix drop.

### /257 §1.13 — `supervision::` namespace stale

**Status: NOT FIXED.** Persona-message imports the
`Supervision*` family from `signal-persona`:
`SupervisionFrame`, `SupervisionFrameBody`,
`SupervisionProtocolVersion`, `SupervisionReply`,
`SupervisionRequest`, `GracefulStopAcknowledgement`. After /252's
engine-management rename lands, every import here renames too. The
local `SupervisionListener`, `SupervisionPhase`,
`SupervisionSocketMode`, `SupervisionStopSignal`,
`SupervisionProfile`, `SupervisionHandle`,
`SupervisionPhaseReply`, `HandleSupervisionRequest` daemon types
all participate in the rename
(`persona-message/src/supervision.rs:13-200+`).

This rename is downstream of the engine-manager triad's /252
execution (/258 §1.13); persona-message inherits the change.

## 2 · New findings specific to this triad

### 2.1 — `MessageChannel` channel name redundant

The `signal_channel!` invocation names the channel `MessageChannel`
(line 272). The channel emission's `MessageChannel*` prefix
combines with the crate's `signal_persona_message` prefix at use
site to produce `signal_persona_message::MessageChannelFrame` —
the word "message" appears three times in one path.

Post macro-rename target: channel name is `Message` (single word,
no `Channel` ceremony), and the macro emits `Frame`, `FrameBody`,
`Operation`, `Reply`, etc. without prefix. The crate path becomes
`signal_persona_message::{Frame, Operation, Reply}` — one
"message" word in the path, supplied by the crate.

### 2.2 — `StampedMessageSubmission` carries the submission as a field

`signal-persona-message/src/lib.rs:114-119`:

```rust
pub struct StampedMessageSubmission {
    pub submission: MessageSubmission,
    pub origin: MessageOrigin,
    pub stamped_at: TimestampNanos,
}
```

Composition shape — the stamped record holds the original
submission plus the daemon-minted fields. **This is the right
shape** (spirit's `StampedEntry` follows the same composition per
/150 §5.1 — "composed as `{ entry, date, time }`, not a duplicate
of `Entry`'s fields"). The current design gets this one right;
no change needed for the composition.

Post-rename: `StampedSubmission { submission: Submission, origin:
Origin, stamped_at: TimestampSeconds }`. The
`MessageOrigin` (from `signal-persona-auth`) keeps its current
name because Origin alone in that crate would be ambiguous (auth
owns multiple origin shapes — `MessageOrigin`,
`InternalComponentInstanceOrigin`); the `Message` prefix on the
auth-crate type names the *domain* of the origin, not the
crate-ancestry — keep.

### 2.3 — Two operations on one wire, two relations on one channel

The current contract serves **two relations on one root family**
(per `signal-persona-message/ARCHITECTURE.md:57-71`):

- **Relation A** — CLI/component-client → `persona-message` (the
  daemon). Legal payloads: `MessageSubmission`, `InboxQuery`.
- **Relation B** — `persona-message` → `persona-router`. Legal
  payloads: `StampedMessageSubmission`.

Per-relation legality is documented in the ARCH but not encoded
in the type system — both relations share `MessageRequest`, and
the daemon must reject `StampedMessageSubmission` on Relation A
("the CLI may not construct a stamped submission") and
`MessageSubmission` on Relation B ("the daemon may not relay a
plain submission to router without stamping it"). Today this
constraint is enforced by witness tests
(`message-cli-sends-router-signal-without-local-ledger`,
`message-frame-codec-rejects-mismatched-signal-verb`).

**Designer call:** this is the right place to ask whether the
contract should split into two channels. Two options:

- **(a) Two channels in one crate** — `pub mod ingress` and
  `pub mod delivery`, each declaring its own `signal_channel!`
  with its own operation set. Per
  `intent/component-shape.nota` 2026-05-21T10:30:00Z (modules-
  not-options for macro disambiguation), this is the natural
  shape. The ingress channel carries `Send` / `Inbox`; the
  delivery channel carries `Deliver`. The type-system enforces
  per-relation legality at compile time. The macro emits clean
  unprefixed names in each module.
- **(b) Keep one channel with three operations**, document the
  per-relation legality in ARCH, enforce via daemon-side
  witnesses (today's shape). This loses the type-level guarantee
  but is simpler — one Operation enum, one Reply enum.

Designer lean: **(a) — two channels**. The current shape is the
case study the /257 §3.4 modules-not-prefixes rule was made for:
two sub-domains in one crate, distinct legality, naturally
separated. Two modules align with the directionality (`ingress::`
is what the daemon listens on; `delivery::` is what the daemon
speaks to router) and let `signal-executor` migration cleanly
separate the two sides of the daemon. /258 §2.4's engine-manager
analogy applies — the choice there is to put `Engine` and
`EngineManagement` channels into separate modules; the same
shape applies here.

**Psyche-touch question (Q1 in §3.5 below)**: should
persona-message use two-channels-per-crate shape, or keep
single-channel with documented per-relation legality?

### 2.4 — CLI carries two env-vars; no policy socket; no `signal_cli!` dispatch

Three findings, one common root.

`persona-message/src/router.rs:34-38`:

```rust
pub fn from_environment() -> Option<Self> {
    std::env::var_os("PERSONA_MESSAGE_SOCKET")
        .or_else(|| std::env::var_os("PERSONA_SOCKET_PATH"))
        .map(Self::from_path)
}
```

Two environment variable names with fallback. The single env-var
carve-out per `intent/component-shape.nota` 2026-05-20T13:00:00Z
allows exactly one env var for socket-path override, *only* for
testing/non-canonical deployment. The current CLI predates that
discipline.

Furthermore, the CLI today knows only one socket — the working
socket (message.sock). After §3 lands the policy contract, the CLI
needs the two-socket dispatch (working + policy) per the same
intent record at 2026-05-20T13:00:00Z. The dispatch becomes
`signal_cli!` macro-generated per `intent/component-shape.nota`
2026-05-20T22:27:40+02:00 + /129's Option A sketch.

Post-migration target (in `persona-message/src/main.rs`):

```rust
signal_frame::signal_cli! {
    cli message;
    working signal_persona_message::Operation;
    policy  owner_signal_persona_message::Operation;
    socket  "persona-message";  // .ord and .own suffixes
}
```

The hand-written three-line `CommandLine::run` chain disappears
in favor of the macro.

### 2.5 — Daemon does not use `signal-executor`

`persona-message`'s `Cargo.toml` depends on `signal-core` and
`signal-persona-message`, not `signal-frame` / `signal-executor` /
`signal-sema`. The frame codec is hand-rolled at
`persona-message/src/router.rs:1-100`; the dispatch loop is a
Kameo `ask` over `MessageDaemonRoot`
(`persona-message/src/daemon.rs:152-164`).

Persona-message is structurally simpler than spirit or engine-
manager because it is stateless (no redb, no atomic batch — the
ARCH explicitly says "the component does not write local message
or pending logs", line 174). Mapping to signal-executor's
template:

- `MessageCommand` enum — daemon-local executable commands.
  Likely just two: `Forward(StampedSubmission)` (the action on
  `Send`); `FetchInbox(InboxQuery)` (the action on `Inbox`). The
  ARCH naming sketch (line 30-34 of ARCH) proposes `RecordSubmission`,
  `StampOrigin`, `ReadInbox` — but since persona-message records
  nothing locally (it forwards), `Forward` reads more honestly
  than `RecordSubmission` (record what? — nothing is recorded).
  `StampOrigin` is composition done in the lowering, not a
  separate command (the stamp is part of building the forwarded
  payload; no observable state-action class on its own).
- `MessageEffect` enum — daemon-local effects. `SubmissionForwarded`
  carrying the router's reply; `InboxFetched` carrying the
  listing.
- `ToSemaOperation` projection. `Forward` → `Assert` (records a
  new fact in router's store, from this component's vantage);
  `FetchInbox` → `Match` (reads).
- `ToSemaOutcome` on effects. `SubmissionForwarded` →
  `Asserted` (router committed) or `NoChange` (router rejected);
  `InboxFetched` → `Matched`.
- `Lowering for MessageLowering`. `lower(Submission)` →
  `OperationPlan` containing one `Forward(StampedSubmission)`
  command (the lowering composes the stamp from
  `MessageDaemonConfiguration.owner_identity` + SO_PEERCRED +
  daemon-minted ingress time). `lower(InboxQuery)` →
  `OperationPlan` containing one `FetchInbox(InboxQuery)`.
- `CommandExecutor for MessageCommandExecutor`. Wraps the
  `SignalRouterClient` (today's `persona-message/src/router.rs:91-99`).
  `execute_atomic_batch` for persona-message is degenerate (single
  command, no transaction boundary — the router is the
  transactional party); reject multi-command batches before
  commit per /150 §7 constraint test.
- `BatchErrorClassification for MessageError` — classify router
  unavailability (`RouterSocketUnavailable`) as `Retryable`,
  router-side rejection (`StoreRejected`) as `NotRetryable`,
  unknown peer credentials (`PeerCredentials`) as `NotRetryable`,
  etc. Generic retry/commit metadata per
  `intent/component-shape.nota` 2026-05-20T02:00:00Z (the
  `BatchAborted { retry, commit }` shape).

**Tap fanout note.** Per `intent/persona.nota`
2026-05-20T20:00:00Z, Tap/Untap is mandatory on the contract but
live fanout is deferred until persona-introspect lands.
Persona-message's Tap surface follows the same shape as spirit's
current placeholder: contract declares the observable block, daemon
accepts Tap/Untap on the working socket, returns
`SemaOutcome::NoChange` until persona-introspect arrives. Do not
treat the no-op as a missing executor step.

The migration is smaller than engine-manager's (single-operation
flow, no actor mesh redesign) and follows /150 §7's playbook.

### 2.6 — `ComponentMessageIngress` is policy, sitting in the working contract

`signal-persona-message/src/lib.rs:121-132`:

```rust
pub struct ComponentMessageIngress {
    pub origin: InternalComponentInstanceOrigin,
    pub socket_path: WirePath,
    pub socket_mode: SocketMode,
}
```

This record describes a manager-created ingress endpoint — one
extra socket the daemon binds, stamped with a typed component-
instance origin. It is **policy state**: the engine manager (or
later, the engine-manager's owner authority — per the
2026-05-20T12:11:26Z three-layer-of-state framing) configures
which internal component instances get their own ingress socket,
under which origin, at which mode. Today it sits in
`MessageDaemonConfiguration` (the daemon's startup
configuration record) per the typed-config-via-argv pattern.

After the owner contract lands, `ComponentMessageIngress` is the
shape the policy contract mutates. It belongs in (or imported by)
`owner-signal-persona-message`, not the working contract. Today
the field stays in the working `signal-persona-message` because
the daemon needs it at bootstrap from
`MessageDaemonConfiguration`; the bootstrap-policy-on-first-start
pattern (per `skills/component-triad.md` §5) covers exactly this
seed-then-mutate-via-owner shape.

Bootstrap: `bootstrap-policy.nota` declares the initial component
ingresses. Post-bootstrap: owner contract `MutateIngresses` or
similar (§3 names it) mutates the table. The contract field stays
defined in `signal-persona-message` (the cross-contract type) and
imported by `owner-signal-persona-message`.

### 2.7 — `MessageDaemonConfiguration` carries the supervision socket — that field is policy

`MessageDaemonConfiguration.supervision_socket_path` and
`.supervision_socket_mode` (lines 326-328 of contract; carried
through to daemon at `persona-message/src/daemon.rs:38-39`).

The supervision (post-/252: engine-management) socket is the
upstream owner's surface — the engine-manager talks to its
supervised daemons over it. The daemon doesn't *control* the
supervision socket; it *exposes* one for the engine-manager to
reach. The path / mode are pre-bootstrap policy: the engine-
manager picks them at spawn time.

This is the same shape as `ComponentMessageIngress` in §2.6 —
policy state seeded at bootstrap. After the owner contract lands,
the engine-manager (owner of persona-message) issues
`MutateEngineManagementBinding` (or similar) through
`owner-signal-persona-message` to change the supervision socket
mid-flight, if that mutation is even allowed (it likely isn't —
the supervision socket is fixed at spawn). Most likely
`supervision_socket_*` stays bootstrap-only and is not exposed in
the owner contract's mutation surface.

### 2.8 — `output_validator.rs` is a daemon-side concern that grew into the binary

`persona-message/src/output_validator.rs` and
`persona-message/src/bin/message_validate_output.rs` exist as a
test/debug surface for validating NOTA reply text from the message
CLI. Per the universal triad invariant, the CLI is "a pure
NOTA↔Signal translation bridge — it does nothing else, no logic,
no state, no fan-out" (`intent/component-shape.nota` 2026-05-20T13:00:00Z).

`message-validate-output` is a separate binary — that's the
right shape (the CLI itself stays pure). But the binary lives in
this repo. After the migration, it could move to a test crate or
stay as a named carve-out for sandbox message-artifact validation
(noted in ARCH line 199 as "test/debug validator for message CLI
NOTA replies"). No action required, flagging for awareness.

## 3 · Proposed owner signal — `owner-signal-persona-message`

The owner contract does not exist. This section proposes its
signal-type names and signal-tree shape per
`intent/persona.nota` 2026-05-20T12:11:26Z (the universal
owner-contract Decision) and the spirit/mind owner contracts as
the migrated templates.

The owner of `persona-message` is the **engine-manager** (per
`skills/component-triad.md` §"Authority chain" — persona daemons
are spawned and supervised by `persona`/engine-manager; the
engine-manager is the owner of every other persona daemon at the
spawn level). The engine-manager is the only caller authorized
on the policy socket.

### 3.1 — What policy operations the owner contract should carry

Persona-message has unusually little durable policy state — it is
stateless. The policy surface is therefore mostly about
configuration override and ingress topology, not about ongoing
rule mutation.

Three policy concerns are clearly motivated by current intent:

1. **Configuration override.** The daemon was started with a
   `MessageDaemonConfiguration` record per the typed-config-via-
   argv pattern. The owner contract carries a `Configure` operation
   so the engine-manager can replace fields without daemon restart
   (e.g., point at a new router socket if the router was respawned
   on a different path; rebind the message socket with a new mode).
   Mirrors the mind owner contract's `Configure(Configuration)`
   pattern.

2. **Ingress allow-list mutation.** Per §2.6,
   `ComponentMessageIngress` is policy. The engine-manager creates
   internal component-instance ingresses as components come up;
   the owner contract carries the verb that adds/removes them
   live (without restarting the daemon). Conservative naming —
   one operation that takes a full new list, not separate
   `AddIngress` / `RemoveIngress` verbs, because the engine-
   manager already maintains the canonical list and can rewrite it
   on each change (avoiding a CRUD-shaped contract surface).

3. **Inspect / read-back.** Owner-side read of the current effective
   policy so the engine-manager can verify a `Configure` landed
   and confirm the current ingress list. Mirrors mind owner's
   `Inspect(Inspection)` pattern.

The open lifecycle question per `intent/component-shape.nota`
2026-05-20T13:45:00Z is named in §3.5 below; **the conservative
landing is no lifecycle verbs in the owner contract for now**.
Persona-message's lifecycle is already governed by the
engine-management socket (the supervision socket inherited from
`signal-persona`), which carries `GracefulStopRequest`,
`ComponentReadinessQuery`, etc. — duplicating lifecycle in the
owner contract would create two surfaces for the same concern.
Persona-spirit's `owner-signal-persona-spirit` *does* carry
`Start` / `Drain` / `Reload` / `Register` / `Retire`, but that is
because persona-spirit is the apex cognitive component spawned
last (per `intent/persona.nota` 2026-05-19T14:00:00Z) and the
supervisor distinction matters there. For persona-message, the
engine-manager already speaks engine-management for lifecycle;
no second lifecycle surface needed.

If lifecycle is later wanted on the owner contract, it lands as
follow-on per the open question.

### 3.2 — Signal-type names

Following the spirit/mind owner contract templates (no ancestry
prefix; the crate name supplies "message"):

```rust
// Operations
pub struct Configure(Configuration);          // record below
pub struct Inspect(Inspection);
pub struct MutateIngresses(IngressList);

// Payloads
pub struct Configuration {
    pub router_socket_path: WirePath,
    pub message_socket_mode: SocketMode,
    // Caveat: not every field of the working
    // MessageDaemonConfiguration is owner-mutable post-bootstrap.
    // owner_identity stays bootstrap-only; supervision_socket_*
    // stays bootstrap-only; message_socket_path stays bootstrap-
    // only (the socket is bound once). Only fields the engine-
    // manager can validly change at runtime appear here.
}

pub struct Inspection {
    pub section: PolicySection,
}

pub enum PolicySection {
    Configuration,
    Ingresses,
    All,
}

pub struct IngressList {
    pub ingresses: Vec<ComponentMessageIngress>,
    // ComponentMessageIngress is imported from signal-persona-
    // message; the cross-contract reuse is honest because the
    // type describes one component-instance ingress endpoint —
    // its shape is the same regardless of which contract carries
    // it.
}

// Replies
pub struct Configured {
    pub revision: PolicyRevision,
}

pub struct PolicySnapshot {
    pub revision: PolicyRevision,
    pub configuration: Configuration,
    pub ingresses: Vec<ComponentMessageIngress>,
}

pub struct IngressesMutated {
    pub revision: PolicyRevision,
}

pub struct ConfigurationRejected {
    pub reason: ConfigurationRejectionReason,
}

pub enum ConfigurationRejectionReason {
    RouterSocketNotReachable,
    SocketModeNotPermitted,
    IngressPathConflict,
}

// Skeleton honesty
pub struct RequestUnimplemented {
    pub reason: UnimplementedReason,
}

pub enum UnimplementedReason {
    NotBuiltYet,
    DependencyNotReady,
}

pub struct PolicyRevision(u64);  // NotaTransparent
```

`PolicyRevision` mirrors `owner-signal-persona-mind/src/lib.rs:25-35`
— same purpose (monotonic revision counter so the owner can
correlate a Configure with the resulting Inspect).

### 3.3 — Signal-tree shape

```rust
signal_channel! {
    channel OwnerMessage {
        operation Configure(Configuration),
        operation Inspect(Inspection),
        operation MutateIngresses(IngressList),
    }
    reply Reply {
        Configured(Configured),
        IngressesMutated(IngressesMutated),
        ConfigurationRejected(ConfigurationRejected),
        PolicySnapshot(PolicySnapshot),
        RequestUnimplemented(RequestUnimplemented),
    }
}
```

No `observable` block on the owner contract — per
`intent/component-shape.nota` 2026-05-19T20:00:00Z + 2026-05-20T02:00:00Z,
Tap/Untap rides the working socket only, never the owner socket
(observation isn't security-sensitive, and putting Tap on the
owner socket would create ambiguity about which owner observation
belongs to). The owner contract's traffic still gets observed —
it shows up in the working channel's Tap fanout via the daemon's
internal projection — but the contract itself declares no
observable block.

No `event` / `stream` blocks — the owner contract is
request/reply only. The engine-manager polls (or one-shot calls)
`Inspect` when it wants policy state, not subscribes.

The /258 §2.4 modules-not-prefixes shape applies here too: when
the macro prefix-drop change lands per
`intent/component-shape.nota` 2026-05-21T10:30:00Z, the crate is a
single-channel crate so the natural shape is just one channel at
the crate root (no `pub mod owner` needed — the crate path
`owner_signal_persona_message::*` supplies all the disambiguation
the names need).

### 3.4 — Sema projections

Each operation lowers to a daemon-local `MessageOwnerCommand` that
projects to a Sema class:

| Operation | Command | Sema class |
|---|---|---|
| `Configure(Configuration)` | `RecordPolicyRevision(Configuration)` | `Mutate` (replaces existing policy at stable identity) |
| `Inspect(Inspection)` | `ReadPolicy(Inspection)` | `Match` (one-shot pattern read) |
| `MutateIngresses(IngressList)` | `RecordIngressList(IngressList)` | `Mutate` |

The Inspect read is `Match` per the spirit pattern (a one-shot
read against current policy is a Match; Subscribe is reserved for
push-with-deltas observation, which the owner contract doesn't do).

The Mutate-vs-Assert distinction: Configure replaces the current
configuration at a stable identity (one Configuration record per
daemon, mutated), so `Mutate` is right. Per
`skills/component-triad.md` §3 the Mutate verb is the authority
verb — owner orders a change, persona-message obeys and confirms.

### 3.5 — Open psyche-touch questions

**Q1 — Two channels in one crate, or single channel with documented
per-relation legality?** (See §2.3.) Designer lean: two channels —
`pub mod ingress` (CLI/component-client → daemon, carries
`Send`/`Inbox`/observable) and `pub mod delivery` (daemon →
router, carries `Deliver` only). Type-system-enforced per-relation
legality. Aligns with /258 §2.4 engine-manager precedent and the
modules-not-prefixes principle. Confirm.

**Q2 — Lifecycle verbs on `owner-signal-persona-message`?** Per
`intent/component-shape.nota` 2026-05-20T13:45:00Z the question
is open for mind; persona-message inherits the same uncertainty.
Conservative landing: **no lifecycle verbs** on the owner
contract (lifecycle stays on the engine-management socket inherited
via `signal-persona`). If lifecycle migrates from engine-management
to per-component owner contracts later, persona-message gets the
verbs then. Confirm.

**Q3 — `MutateIngresses(IngressList)` shape — single full-list
mutation, or per-ingress `AddIngress`/`RemoveIngress` verbs?**
Designer lean: single full-list mutation — the engine-manager
already maintains the canonical list and rewrites it on each
component-instance lifecycle event; the daemon doesn't need to
reconcile add/remove deltas. Aligns with the
`skills/contract-repo.md` rule about not building CRUD-shaped
contracts when the caller already has the canonical state.
Confirm.

**Q4 — `Configuration` field set — which `MessageDaemonConfiguration`
fields are owner-mutable post-bootstrap?** Designer-derived
candidates: `router_socket_path` (router was respawned on a
different socket → re-point), `message_socket_mode` (chmod the
ingress socket without restart). Bootstrap-only fields:
`message_socket_path` (bound once at startup),
`supervision_socket_path/mode` (engine-manager spawn-time
decision), `owner_identity` (engine ownership is fixed for the
daemon's lifetime). Confirm the split — psyche may want a
narrower or broader owner-mutable set.

**Q5 — Should the owner contract carry the `Tap`/`Untap` mandate?**
Per the universal Tap-on-working-only rule, the answer is no — the
owner contract has no observable block. But the working
contract's Tap fanout *does* include the owner-channel traffic
(per `intent/component-shape.nota` 2026-05-19T20:00:00Z — the
universal observer hook on every daemon sees every message
arriving, regardless of socket). Verify the operator implementing
the Tap fanout knows to project owner-channel traffic into the
working-channel Tap stream. This is mechanism, not contract
shape; flagging for awareness rather than as a psyche question.

## 4 · Recommended next slice for the persona-message triad

In priority order:

1. **Working contract three-layer migration**. Smaller than spirit
   (no event/stream, three operations); follow spirit's template.
   Concretely:
   - `signal-core` → `signal-frame` in `Cargo.toml`.
   - `signal_channel!` block to contract-local verbs (`Send`,
     `Deliver`, `Inbox`) with `operation`/`reply` keywords.
   - Drop `Message*` ancestry prefixes from every contract type
     per §1 (/257 §1.5).
   - Drop the `operation` field from `RequestUnimplemented` per
     §1 (/257 §1.6).
   - Add the `observable` block per §1 (/257 §1.10).
   - Drop `MessageOperationKind` (macro-emitted as `OperationKind`).
   - Drop the frame alias dance (lines 287-291) when the macro
     prefix-drop change lands.
   - `TimestampNanos` → `TimestampSeconds` for `stamped_at`
     (subject to psyche call /258 §1.12).
2. **Resolve §2.3 / Q1**: two-channels-per-crate vs single-channel.
   This affects the macro invocation count; do not start coding the
   migration before the psyche answers.
3. **Owner contract creation**. After §3's psyche calls
   (Q2, Q3, Q4) settle:
   - Create `owner-signal-persona-message` repository (or wait
     for psyche per `intent/component-shape.nota` 2026-05-19T20:30:00Z
     — "Don't backfill them by assumption; let them emerge as
     each component's owner discipline crystallizes" — this report
     is the crystallization).
   - Implement the shape per §3.3.
   - Witness tests for owner-socket-rejects-ordinary,
     ordinary-socket-rejects-owner, bootstrap-policy population.
4. **Daemon onto `signal-executor`** per §2.5. Mechanical:
   - Define `MessageCommand` / `MessageEffect` in
     `persona-message/src/`.
   - Implement `Lowering for MessageLowering` (wraps the current
     `MessageDaemonRoot.handle_request` flow).
   - Implement `CommandExecutor for MessageCommandExecutor`
     (wraps the existing `SignalRouterClient`).
   - Implement `BatchErrorClassification for Error` (classify
     `RouterSocketUnreachable` as Retryable; `StoreRejected` as
     NotRetryable; etc.).
   - Wire `signal_executor::Executor::execute(request).await` into
     `persona-message/src/daemon.rs`'s socket-handling path,
     replacing the hand-rolled router codec.
   - Reject multi-operation batches and multi-command operation
     plans before commit (degenerate atomicity — persona-message
     never gets a real transaction boundary).
5. **CLI migration to `signal_cli!`** per §2.4 + /129's sketch:
   - Replace `persona-message/src/main.rs` and
     `command.rs`'s CommandLine dispatch with the macro invocation.
   - Drop `PERSONA_SOCKET_PATH` fallback (single env-var carve-out:
     keep `PERSONA_MESSAGE_SOCKET` for socket override).
   - Two-socket dispatch (working + policy) wired via the macro.
6. **/252 supervision rename** inherited from engine-manager work
   (file moves, type renames, field renames).
7. **Drop `output_validator` binary or move to a test crate** —
   low priority, flagging for cleanup awareness (§2.8).

Beads worth filing (subject to psyche approval):

- "Migrate persona-message working contract to three-layer"
  (modeled on /258's engine-manager template).
- "Create owner-signal-persona-message contract" (gated on
  §3's psyche calls).
- "Migrate persona-message daemon onto signal-executor"
  (downstream of the contract migration).

## 5 · References

- `intent/persona.nota` 2026-05-20T12:11:26Z — universal
  owner-contract Decision (every stateful component has one).
- `intent/component-shape.nota` 2026-05-20T12:11:26Z —
  working/policy vocabulary; signal-type naming is architecture.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z — three-layer
  model; Tap/Untap mandatory for persona components.
- `intent/component-shape.nota` 2026-05-19T19:30Z / 19:45Z /
  20:00Z — contract-local verbs; signal-frame separation; universal
  observer hook on the working socket.
- `intent/component-shape.nota` 2026-05-19T20:30Z — five missing
  owner-signal-persona-* repos are intentionally missing; let
  each component's owner discipline crystallize.
- `intent/component-shape.nota` 2026-05-20T13:00:00Z — CLI design
  (six records: binary naming, two argument shapes, pure
  translation bridge, env-var carve-out, two-socket dispatch,
  universality).
- `intent/component-shape.nota` 2026-05-20T13:45:00Z — Mind/body
  analogy; lifecycle-on-owner-signal open question.
- `intent/component-shape.nota` 2026-05-20T22:27:40+02:00 —
  signal-cli macro Decision.
- `intent/component-shape.nota` 2026-05-21T10:30:00Z — modules-
  not-options for macro disambiguation.
- `intent/persona.nota` 2026-05-20T18:44:49Z — no nanoseconds for
  ingress stamping.
- `intent/persona.nota` 2026-05-20T20:00:00Z — Tap/Untap deferred
  fanout (placeholder shape until persona-introspect lands).
- `intent/persona.nota` 2026-05-21T10:00:00Z — debug-the-debugger
  (universal observability).
- `/255`, `/256` — spirit migration template.
- `/257` — workspace-wide signal-contract audit.
- `/258` — engine-manager triad audit (sibling to this report;
  same migration shape).
- `/150` — operator's consolidated current-state handoff.
- `/129` — `signal_cli!` Option A sketch.
- `~/primary/reports/second-operator-assistant/11` — signal-type
  naming and shape design guideline (the consolidated principles
  this audit applies).
- Code under audit:
  - `signal-persona-message/src/lib.rs:1-339` — contract.
  - `signal-persona-message/ARCHITECTURE.md:1-220` — contract
    architecture (carries the MUST IMPLEMENT three-layer note).
  - `persona-message/src/lib.rs`, `command.rs`, `daemon.rs`,
    `router.rs`, `supervision.rs`, `error.rs`, `surface.rs`,
    `bin/persona_message_daemon.rs`, `bin/message_validate_output.rs`.
  - `persona-message/ARCHITECTURE.md:1-224`.
- Templates:
  - `owner-signal-persona-spirit/src/lib.rs:1-121`.
  - `owner-signal-persona-mind/src/lib.rs:1-200`.
  - `signal-persona-spirit/src/lib.rs:405-453` (observable block
    and contract-local verbs).

This report retires when (a) the working contract is migrated AND
the owner contract is implemented per §3 AND the daemon is on
signal-executor AND the CLI is on signal_cli, OR (b) a successor
audit supersedes.
