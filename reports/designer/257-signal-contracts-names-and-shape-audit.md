# 257 — Signal contracts: bad-name and bad-shape audit

*Workspace-wide audit of every signal contract for name and shape
gaps against the psyche's stated discipline: contract-local verbs in
verb form (`intent/component-shape.nota` 2026-05-19T19:30, 19:45,
20:00, 20:30); lift-the-repeated-suffix
(2026-05-20T00:07:55+02:00); names don't carry full ancestry
(ESSENCE.md §Naming); no-empty-markers / use mixed enums; Tap/Untap
mandatory for persona components (2026-05-20T02:00:00Z); two-field
timestamps in intent records (`intent/workspace.nota` 2026-05-19
18:30). Spirit was audited in /255 / /256 and is referenced here as
the migration template.*

## 0 · TL;DR

**Migration status of 18 in-scope contracts** (ordinary + owner):

| Migrated to `signal-frame` + contract-local verbs | Stale on `signal-core` + universal-verb shape |
|---|---|
| signal-persona-spirit ✓ (per /255 /256) | signal-persona-mind |
| signal-persona-orchestrate (frame ✓ but text stale per /256) | signal-persona-router |
| signal-persona (frame ✓ but `supervision::` namespace not renamed per /252) | signal-persona-message |
| signal-repository-ledger ✓ | signal-persona-introspect |
| owner-signal-persona-spirit ✓ | signal-persona-system |
| owner-signal-persona-mind ✓ | signal-persona-terminal |
| owner-signal-persona-orchestrate ✓ | signal-persona-harness |
| owner-signal-persona-router ✓ | owner-signal-persona-terminal |
|  | signal-criome |
|  | owner-signal-repository-ledger |

Roughly half migrated, half not. The unmigrated half all share the
same shape problems; the migrated half mostly only has the
finer-grained name/shape smells.

**Five workspace-wide patterns dominate** (every contract hits at
least one):

1. **Old universal-verb shape on operations** (`Assert / Match /
   Subscribe / Retract / Mutate` prefixes). Should be **contract-
   local verbs in verb form** per the 2026-05-19T19:45 Decision.
   10 contracts affected.
2. **Repeated-suffix smell on operations and replies**
   (`SubmitThought / SubmitRelation`, `QueryThoughts /
   QueryRelations`, five `*Receipt` siblings, etc.). Should **lift
   the repeated category into a typed sum** per
   2026-05-20T00:07:55+02:00. Especially severe in
   signal-persona-mind.
3. **Ancestry-prefixed type names**
   (`RouterObservationId`, `SystemTarget`, `TerminalName`,
   `MindRequest`, `IntrospectionUnimplemented`). Every contract
   uses its own crate name (`Router`, `Terminal`, `System`,
   `Mind`, `Introspection`) as a type prefix. The crate IS the
   ancestry; the prefix is redundant per ESSENCE §Naming.
4. **`*RequestUnimplemented { operation, reason }` redundancy** —
   the `operation` field restates information the reply already
   carries positionally. Same smell as the spirit `RequestUnimplemented`
   pre-fix. 7 contracts have this.
5. **No `observable` block** on persona-component contracts that
   are triad components — Tap/Untap is **mandatory** per the
   2026-05-20T02:00:00Z Decision. Only spirit has the observable
   block today.

**Three contract-specific high-impact items**:

- `signal-persona-mind`: 15-variant `MindOperationKind` is a sign
  the channel mixes three relations (work graph / mind graph /
  channel choreography) under one root. Psyche's
  2026-05-19T20:30 Decision said the choreography family should
  split into multiple contract-local verbs (Grant / Extend /
  Revoke / List / Deny). Not done. Mind is the worst-shape
  contract in the workspace.
- `signal-persona`: still uses `supervision::` namespace +
  `Supervision*` types instead of the affirmed `engine_management::`
  + `EngineManagement*`. The /252 rename has not been executed.
- `signal-persona-orchestrate`: ARCH text still mentions
  `SemaEffectObserved` / `SemaEffectEmitted` (per /256); migrate
  with the contract redesign.

The substance below is per-contract, with specific renames and
shape changes.

## 1 · Universal patterns (with examples)

### 1.1 — Old universal-verb shape

Stale shape (`signal-persona-mind/src/lib.rs:1382-1400`):

```rust
signal_channel! {
    channel Mind {
        request MindRequest {
            Assert SubmitThought(SubmitThought),
            Assert SubmitRelation(SubmitRelation),
            Match QueryThoughts(QueryThoughts),
            Match QueryRelations(QueryRelations),
            Subscribe SubscribeThoughts(SubscribeThoughts) opens MindEventStream,
            ...
            Mutate StatusChange(StatusChange),     // doubly wrong — see 1.4
            ...
            Match Query(Query),                     // doubly wrong — see 1.3
            ...
        }
    }
}
```

The `Assert / Match / Subscribe / Retract / Mutate` prefixes are
universal Sema verbs that were retired at the public contract
layer per `intent/component-shape.nota` 2026-05-19T19:45:00Z. The
new shape is **contract-local verb in verb form**, with the macro
keyword `operation`:

```rust
signal_channel! {
    channel Mind {
        operation Submit(Submission),     // typed sum of Thought | Relation | Opening | Note | Link | Alias
        operation Query(Query),           // typed sum of QueryKind
        operation Watch(Subscription) opens MindEventStream,
        operation Unwatch(SubscriptionToken),
        operation ChangeStatus(StatusChange),
        operation Adjudicate(AdjudicationRequest),
        operation ListChannels(ChannelFilter),
    }
    ...
    observable { ... }                    // mandatory for persona — see 1.11
}
```

Applies to: signal-persona-mind, signal-persona-router,
signal-persona-message, signal-persona-introspect,
signal-persona-system, signal-persona-terminal,
signal-persona-harness, owner-signal-persona-terminal,
signal-criome, owner-signal-repository-ledger.

### 1.2 — Doubling smell

`Match Query(Query)` (mind), `Match EngineSnapshot(EngineSnapshotQuery)`
(introspect), `Match Summary(RouterSummaryQuery)` (router),
`Assert MessageSubmission(MessageSubmission)` (message),
`Match FocusSnapshot(FocusSnapshot)` (system).

Psyche's exact framing (2026-05-19T19:30):

> *"match query query, but that is fucking ugly as fuck."*

The verb-form rule resolves it: the variant carries an action
(verb), the payload carries data (typed record). When both are the
same word, the variant collapses into the operation root and the
payload becomes a typed sum.

Worked example for router:

```rust
operation Query(Query),                  // Query is contract-local verb
// Query enum payload:
pub enum Query {
    Summary(SummaryQuery),
    MessageTrace(MessageTraceQuery),
    ChannelState(ChannelStateQuery),
}
```

### 1.3 — `Mutate <Verb>` is grammatically wrong

`Mutate StatusChange(StatusChange)` (mind). Per the 2026-05-19T19:30
Correction:

> *"you mutate nouns, not verbs. So mutate configure doesn't work
> out... mutate register might work, but only if you're considering
> register as a noun and not a verb."*

`StatusChange` is verb-form (the act of changing status). `Mutate
StatusChange` reads as "mutate a status-change," which is incoherent.

Fix: rename the operation to a contract-local verb. Options:

```rust
operation Transition(StatusTransition),     // Transition is verb; payload is noun
operation ChangeStatus(StatusChange),        // ChangeStatus is the verb; StatusChange is the request noun
```

Either works. `ChangeStatus(StatusChange)` keeps the existing
record name; `Transition(StatusTransition)` is structurally cleaner
(verb verbs a noun).

### 1.4 — Repeated-suffix smell

Psyche's 2026-05-20T00:07:55+02:00 correction on the
repository-ledger pilot (canonical reference):

> *"five \*Listing siblings want lifting the same way \*Query was
> lifted on the request side... Same shape both sides — Query
> operation root with Query enum payload; QueryResult reply variant
> with QueryResult enum payload. Symmetric."*

Workspace-wide instances:

- **signal-persona-mind operations** (line 1385-1399):
  `SubmitThought` + `SubmitRelation`; `QueryThoughts` +
  `QueryRelations`; `SubscribeThoughts` + `SubscribeRelations`.
  Plus `Opening` / `NoteSubmission` / `Link` / `StatusChange` /
  `AliasAssignment` (five item-level submissions).
- **signal-persona-mind replies** (line 1402-1416):
  `ThoughtCommitted` + `RelationCommitted` + `OpeningReceipt` +
  `NoteReceipt` + `LinkReceipt` + `StatusReceipt` + `AliasReceipt`
  = seven `*Committed/*Receipt` siblings.
- **signal-persona-terminal** (line 953-974): 19 reply variants,
  several with shared suffixes (`PromptPatternRegistered` +
  `PromptPatternUnregistered` + `PromptPatternList`,
  `GateAcquired` + `GateBusy` + `GateReleased`, etc.).
- **signal-persona-system**: `SubscriptionAccepted` +
  `SubscriptionRetracted` + `ObservationTargetMissing` —
  borderline.

Lift to typed sums. Mind's submission family becomes:

```rust
operation Submit(Submission),

pub enum Submission {
    Thought(Thought),
    Relation(Relation),
    Opening(Opening),
    Note(Note),
    Link(Link),
    Alias(AliasAssignment),
}

reply MindReply {
    Submitted(Receipt),
    Queried(QueryResult),
    Watched(SubscriptionOpened),
    Unwatched(SubscriptionRetracted),
    ...
}

pub enum Receipt {
    Thought(ThoughtReceipt),
    Relation(RelationReceipt),
    Opening(OpeningReceipt),
    Note(NoteReceipt),
    ...
}
```

The 15-variant `MindOperationKind` collapses to 6 or 7 root verbs
(`Submit`, `Query`, `Watch`, `Unwatch`, `ChangeStatus`,
`Adjudicate`, `ListChannels`).

### 1.5 — Ancestry-prefixed type names

Per ESSENCE.md §"Naming":

> *"A type, variant, or field belongs to its surrounding namespace;
> repeating the namespace in the name is redundant ceremony."*

Inside `signal-persona-router`, the crate name supplies "router"
context. The type should be `ObservationId`, not
`RouterObservationId`. Inside `signal-persona-terminal`, the type
should be `Name`, not `TerminalName`.

Worst offenders:

- **signal-persona-router**: drop `Router` prefix from
  `RouterObservationId`, `RouterObservationScope`, `RouterSummary`,
  `RouterMessageTrace`, `RouterMessageTraceMissing`,
  `RouterChannelState`, `RouterChannelStatus`,
  `RouterDeliveryStatus`, `RouterBootstrapOperation`,
  `RouterBootstrapDocument`, `RouterObservationUnimplemented`,
  `RouterObservationUnimplementedReason`,
  `RouterDaemonConfiguration`, `RouterSummaryQuery`,
  `RouterMessageTraceQuery`, `RouterChannelStateQuery`. The macro
  emits `RouterRequest`/`RouterReply` etc. as the channel-prefixed
  names; non-macro types should be unprefixed.
- **signal-persona-system**: drop `System` prefix from
  `SystemTarget`, `SystemBackend`, `SystemHealth`,
  `SystemReadiness`, `SystemStatusQuery`, `SystemStatus`,
  `SystemRequestUnimplemented`, `SystemUnimplementedReason`,
  `SystemOperationKind`, `SystemDaemonConfiguration`.
- **signal-persona-terminal**: drop `Terminal` prefix from
  `TerminalName`, `TerminalGeneration`, `TerminalSequence`,
  `TerminalInputBytes`, `TerminalTranscriptBytes`, `TerminalRows`,
  `TerminalColumns`, `TerminalByteCount`, `TerminalRejected`,
  `TerminalRejectionReason`, `TerminalConnection`, `TerminalInput`,
  `TerminalResize`, `TerminalCapture`, `TerminalDetachment`,
  `TerminalReady`, `TerminalInputAccepted`, `TerminalResized`,
  `TerminalCaptured`, `TerminalDetached`, `TerminalExited`,
  `TerminalWorkerLifecycleToken`,
  `TerminalWorkerLifecycleSnapshot`, `TerminalWorkerLifecycleEvent`.
  About 20+ types.
- **signal-persona-introspect**: drop `Introspection` prefix from
  `IntrospectionTarget`, `IntrospectionScope`,
  `IntrospectionUnimplemented`, `IntrospectionUnimplementedReason`,
  `IntrospectionDenied`, `IntrospectionDeniedReason`. Keep
  `IntrospectDaemonConfiguration` → `DaemonConfiguration`.
- **signal-persona-message**: drop `Message` prefix from
  `MessageRecipient`, `MessageSender`, `MessageBody`,
  `MessageSlot`, `MessageKind`, `MessageSubmission`,
  `MessageOperationKind`, `MessageRequestUnimplemented`,
  `MessageUnimplementedReason`, `MessageDaemonConfiguration`.
- **signal-persona-mind**: drop `Mind` prefix from `MindRequest`,
  `MindReply`, `MindEvent`, `MindOperationKind`,
  `MindRequestUnimplemented`. (The macro emits these; the rename
  goes through the macro's channel-name parameter — see §1.10.)
- **signal-persona-harness**: drop `Harness` prefix from
  `HarnessName`, `HarnessStatusQuery`, `HarnessOperationKind`,
  `HarnessTranscriptRetraction` (verify).

Note: where the prefix names a **domain concept** (not just the
crate name), keep it. Examples:

- `EngineId` in signal-persona-auth — Engine is the domain
  concept, keep.
- `ChannelEndpoint`, `ChannelDuration`, `ChannelMessageKind` in
  owner-signal-persona-router — Channel is the domain noun, keep.
- `MessageDelivery` in signal-persona-harness — Message is the
  payload type the contract delivers, keep.

### 1.6 — `*RequestUnimplemented { operation, reason }`

Pattern: every contract has a `*RequestUnimplemented` reply variant
that carries `operation: *OperationKind` plus `reason: *UnimplementedReason`.

The `operation` field is **redundant** — the reply is positionally
addressed to its operation; the caller already knows which
operation produced this reply. (Spirit's prior version had this
smell; fixed in `d87e4055`.)

Contracts to fix:

- signal-persona: `SupervisionUnimplemented` (already only has
  `reason` — clean ✓).
- signal-persona-mind: `MindRequestUnimplemented` (verify;
  probably has `operation`).
- signal-persona-router: `RouterObservationUnimplemented { scope,
  reason }` — `scope` is the same redundancy.
- signal-persona-message: `MessageRequestUnimplemented { operation,
  reason }` (line 191-194).
- signal-persona-introspect: `IntrospectionUnimplemented { scope,
  reason }` (line 149-153).
- signal-persona-system: `SystemRequestUnimplemented { operation,
  reason }` (line 290-294).
- signal-persona-terminal: `TerminalRequestUnimplemented` (verify).
- signal-persona-harness: `HarnessRequestUnimplemented` (verify).
- owner-signal-persona-mind: `RequestUnimplemented { operation,
  reason }` (line 131-134).

Fix: drop the `operation` / `scope` field; keep `reason` only.

### 1.7 — Empty marker records

Spirit fixed these in `Observation::State` / `Subscription::State`
etc. by using unit variants on `NotaEnum`. Other contracts still
have empty markers:

- signal-persona-terminal: `ListSessions {}` (line 196).
- Verify others (likely present in any contract with no-payload
  operations).

Fix: replace with unit variants on the enclosing enum, per the
mixed-enum support psyche affirmed.

### 1.8 — Single-variant enums

ESSENCE.md: *"don't design for hypothetical future requirements."*
Single-variant enums signal speculative extensibility.

- **signal-persona-system**: `SystemTarget::NiriWindow(NiriWindowId)`,
  `SubscriptionKind::Focus`, `SystemBackend::Niri`. The
  speculative-future framing is explicit in the docstring
  (*"Currently only Niri windows; future backends..."*). Per
  ESSENCE, collapse:

  ```rust
  // Today:
  pub enum SystemTarget { NiriWindow(NiriWindowId) }
  // Future-aware shape:
  pub type SystemTarget = NiriWindowId;  // or just inline NiriWindowId
  ```

  If/when a real `MacWindow` variant appears, that's the moment to
  introduce the enum — with the actual semantics that variant
  brings, not a speculative empty shell.

- **owner-signal-persona-router**: `ChannelDuration::TimeBound(TimestampNanoseconds)`
  has nanosecond-precision payload but the other two variants
  (`OneShot`, `Permanent`) carry no time. The nanos resolution is
  probably overkill — seconds would do for time-bound channels.

### 1.9 — Frame type alias boilerplate

Every contract has this 5–7 line block:

```rust
pub type Frame = SpiritFrame;
pub type FrameBody = SpiritFrameBody;
pub type ChannelRequest = SpiritChannelRequest;
pub type ChannelReply = SpiritChannelReply;
pub type RequestBuilder = SpiritRequestBuilder;
```

The macro emits `<Channel>Frame`, `<Channel>FrameBody`, etc.
because it can't see from inside which crate it's in. Each contract
re-aliases to drop the channel-name prefix (the right shape per
"no full ancestry"). Every contract repeats this dance.

**Macro fix**: `signal-frame-macros` should emit unprefixed names
by default (`Frame`, `FrameBody`, etc.) and let the contract author
opt into a prefix when needed (e.g., two channels in one crate).
This eliminates the boilerplate.

### 1.10 — No observable block

Per `intent/component-shape.nota` 2026-05-20T02:00:00Z:

> *"Tap/Untap is mandatory for persona components, no author
> override."*

Spirit's contract has the observable block (signal-persona-spirit
line 416-420). Every other persona-component contract is missing it.
Required: persona-mind, persona-router, persona-message,
persona-harness, persona-system, persona-terminal,
persona-introspect, persona-orchestrate. (Spirit done; Persona's
engine-management surface may not need Tap, but verify.)

Each should add:

```rust
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

Macro injects `Tap(ObserverFilter)` / `Untap(ObserverSubscriptionToken)`
operations and the per-channel observer-set / token types.

### 1.11 — Single-field timestamps (and excess precision)

Spirit's `Timestamp(u64)` violates the two-field-timestamp Decision
per /256 §3.1. Cross-contract instances of the same shape:

- signal-persona: `TimestampNanos(u64)` — used for runtime stamping
  (component-ready time, etc.). The two-field intent is *for intent
  records*; protocol/runtime timestamps may be OK as single fields,
  BUT nanosecond precision is excessive for "when did the
  component become ready." Seconds (or milliseconds) would do.
- owner-signal-persona-router: `TimestampNanoseconds(u64)` —
  same. Used for `ChannelDuration::TimeBound`.
- signal-persona-message: imports `TimestampNanos` from
  signal-persona.

Designer recommendation: keep single-field for runtime-stamped
protocol timestamps but lower precision to seconds (matching the
intent-log human convention). The strict two-field rule
applies *only to intent records* (spirit's Entry — per /256).
Confirm or override.

### 1.12 — Name collisions across contracts

- `MessageSender`, `MessageBody`, `MessageSlot` — defined in BOTH
  signal-persona-message AND signal-persona-harness. Same names,
  separate `pub struct ...`. A consumer importing both crates has
  to disambiguate.
- `ComponentName` — defined in signal-persona AND in
  signal-persona-auth.
- `SubscriptionAccepted` / `SubscriptionRetracted` — multiple
  contracts have these names.
- `Configuration`, `RequestUnimplemented`, `OperationKind`,
  `UnimplementedReason` — generic names across owner contracts.

Two resolution approaches:

- **Inline-duplication-is-fine**: each contract owns its types.
  A consumer importing both writes
  `use signal_persona_message::Sender as MessageSender;` if a
  collision matters. Trust the type system; names stay local and
  unprefixed.
- **Shared-types crate**: extract truly-universal types
  (`MessageSlot`, `ComponentName`) into `signal-persona-types` or
  similar, and let every contract import.

Designer lean: **inline-duplication for everything except the
universal infrastructure types** (`ComponentName`, `EngineId`, etc.
which are already in signal-persona-auth). Message-domain types
(`Sender`, `Body`, `Slot`) staying local to their contracts is
cleaner — message and harness use the same words but mean slightly
different things in their domains, and the type-system disambiguates
at the boundary.

### 1.13 — `supervision::` namespace stale

Per /252, the `Supervision*` types in signal-persona should rename
to `EngineManagement*`. Not done yet:

- `signal_persona::supervision` module → `engine_management`.
- `SupervisionProtocolVersion` → `EngineManagementProtocolVersion`.
- `SupervisionUnimplemented` → `EngineManagementUnimplemented`.
- `SupervisionFrame`, `SupervisionFrameBody`,
  `SupervisionOperation`, `SupervisionOperationKind`,
  `SupervisionReply`, `SupervisionReplyKind` → all prefixed.

Across the workspace, every reference to `supervision_*` fields in
daemon configurations (`supervision_socket_path`,
`supervision_socket_mode`) renames too.

## 2 · Per-contract findings

### signal-persona (engine-manager management)

- **Status**: migrated to signal-frame; uses contract-local verbs
  (`Launch`, `Query`, `Retire`, `Start`, `Stop`).
- **Major gap**: `supervision::` module + `Supervision*` types
  not renamed to `engine_management::` + `EngineManagement*` per
  the /252 rename. Action: execute /252.
- **`TimestampNanos`** — single field, nanosecond precision.
  Lower to seconds (`Timestamp`) per 1.12.
- **Type collisions**: `ComponentName` here AND in
  `signal-persona-auth`. Decide one owner.
- **Reply variants** in `EngineReply`: `Launched / LaunchRejected
  / Retired / RetireRejected / ActionAccepted / ActionRejected` —
  the `*Rejected` siblings are clean per the verb-past + rejected
  convention. ✓
- **`Query` enum payload** is a hand-written impl. Should derive
  `NotaEnum` once codec supports it (verify whether enum w/
  data-bearing variants is now supported via mixed enums).

### signal-persona-mind (THE WORST OFFENDER)

- **Status**: still on signal_core; old universal-verb shape.
- **15-variant operation root** mixes three relations under one
  channel. Psyche directed splitting the choreography family per
  2026-05-19T20:30 Decision (Grant / Extend / Revoke / List / Deny);
  not done.
- **Doubling**: `Match Query(Query)` and `Match ChannelList(ChannelList)`.
- **`Mutate StatusChange(StatusChange)`** — wrong grammatically;
  rename to `ChangeStatus(StatusTransition)` or `Transition`.
- **Repeated suffix everywhere**: `*Thought / *Relation` pair on
  three operations; five `*Receipt` siblings on replies; etc.
- **`MindRequest`/`MindReply`/`MindEvent`/`MindEventStream`** —
  prefix dance. Macro renames once frame is migrated.
- **Stale `RoleName` enum** (lines 67-127) — should align with
  signal-persona-orchestrate's dynamic `RoleIdentifier` (String)
  per the roles-are-data intent. Decide one owner.
- **Missing observable block**.
- **15-variant `MindOperationKind`** → collapses to ~7 after the
  lift.

**Proposed shape**:

```rust
signal_channel! {
    channel Mind {
        operation Submit(Submission),
        operation Query(Query),
        operation Watch(Subscription) opens MindEventStream,
        operation Unwatch(SubscriptionToken),
        operation ChangeStatus(StatusTransition),
        operation Adjudicate(AdjudicationRequest),
        operation ListChannels(ChannelFilter),
    }
    reply Reply {
        Submitted(SubmissionReceipt),
        Queried(QueryResult),
        StatusChanged(StatusReceipt),
        Adjudicated(AdjudicationReceipt),
        ChannelsListed(ChannelListView),
        WatchOpened(SubscriptionOpened),
        WatchClosed(SubscriptionRetracted),
        Rejected(RejectionDetail),
        Unimplemented(UnimplementedDetail),
    }
    event Event {
        Delta(SubscriptionEvent) belongs MindEventStream,
    }
    stream MindEventStream {
        token SubscriptionId;
        opened SubscriptionOpened;
        event Delta;
        close Unwatch;
    }
    observable {
        filter default;
        operation_event OperationReceived;
        effect_event EffectEmitted;
    }
}
```

### signal-persona-router

- **Status**: still on signal_core; old universal-verb shape
  (`Match Summary`, `Match MessageTrace`, `Match ChannelState`).
- **`Router` prefix** on 16+ types — drop.
- **Reply variant naming**: `Summary / MessageTrace /
  MessageTraceMissing / ChannelState / Unimplemented`. Drop the
  `Missing` smell — split into Reply::Trace(Trace) + Reply::TraceAbsent.
  Or: keep the explicit-absence variant; document the rationale.
- **Missing observable block**.
- **Proposed**:

```rust
signal_channel! {
    channel Router {
        operation Query(Query),
        // operation Subscribe(Subscription) opens DeliveryStream,  // when added
    }
    reply Reply {
        Queried(QueryResult),
        Unimplemented(UnimplementedDetail),
    }
    observable { filter default; operation_event OperationReceived; effect_event EffectEmitted; }
}

pub enum Query {
    Summary(SummaryQuery),
    MessageTrace(MessageTraceQuery),
    ChannelState(ChannelStateQuery),
}

pub enum QueryResult {
    Summary(Summary),
    MessageTrace(MessageTrace),
    MessageTraceAbsent(MessageTraceAbsence),
    ChannelState(ChannelState),
}
```

### signal-persona-message

- **Status**: still on signal_core; old shape.
- **`Assert MessageSubmission(MessageSubmission)`** — triple
  smell (Assert verb + Message prefix + doubling).
- **`Message` prefix** on ~10 types — drop.
- **`MessageRequestUnimplemented { operation, reason }`** — drop
  operation field.
- **Missing observable block**.
- **Two payloads**: `MessageSubmission` (caller-side) and
  `StampedMessageSubmission` (router-internal post-stamping). Two
  separate operation variants today. Could lift via typed sum but
  the discriminator is meaningful (one is pre-stamp, one is
  post-stamp); two separate operations may be the right shape.
- **Proposed**:

```rust
signal_channel! {
    channel Message {
        operation Send(Submission),
        operation Forward(StampedSubmission),
        operation Query(InboxQuery),
    }
    reply Reply {
        Sent(SubmissionAcceptance),
        SendRejected(SubmissionRejection),
        Queried(InboxListing),
        Unimplemented(UnimplementedDetail),
    }
    observable { ... }
}
```

### signal-persona-introspect

- **Status**: still on signal_core; old shape.
- **`Introspection` prefix** on many types — drop.
- **`IntrospectionUnimplemented { scope, reason }`** — drop scope.
- **`IntrospectionTarget` enum** has `EngineManager / Mind /
  Message / Router / System / Harness / Terminal / Introspect` —
  mirrors `signal_persona::ComponentKind` (which has the same 8
  variants minus EngineManager/Introspect). One should own this
  enumeration; the other reuses.
- **No observable block** — introspect is the *consumer* of every
  other component's Tap stream; introspect itself probably
  shouldn't be observable. Verify with psyche if introspect ITSELF
  needs a Tap surface.
- **Proposed**:

```rust
signal_channel! {
    channel Introspection {
        operation Query(Query),
    }
    reply Reply {
        Queried(QueryResult),
        Denied(DeniedDetail),
        Unimplemented(UnimplementedDetail),
    }
}

pub enum Query {
    EngineSnapshot(EngineSnapshotQuery),
    ComponentSnapshot(ComponentSnapshotQuery),
    DeliveryTrace(DeliveryTraceQuery),
    PrototypeWitness(PrototypeWitnessQuery),
}
```

### signal-persona-system

- **Status**: still on signal_core; old shape.
- **`System` prefix** on many types — drop.
- **Single-variant enums** (`SystemTarget::NiriWindow`,
  `SystemBackend::Niri`, `SubscriptionKind::Focus`) — collapse.
- **`SystemRequestUnimplemented { operation, reason }`** — drop
  operation.
- **`FocusSnapshotReply(FocusObservation)`** — variant has noisy
  `Reply` suffix; should be `FocusSnapshot(FocusObservation)`.
- **Missing observable block**.
- **Bidirectional shape**: system is the router's downstream. The
  channel is bidirectional (router opens subscriptions, system
  pushes observations). The Tap discipline for cross-component
  introspect applies regardless.

### signal-persona-terminal

- **Status**: still on signal_core; old shape; **largest contract**
  (1237 lines).
- **`Terminal` prefix** on 20+ types — drop most.
- **15 operations + 19 replies** under one channel — possibly
  needs splitting into sub-channels (data plane vs control plane)
  but that's a bigger design call.
- **Empty marker `ListSessions {}`** — replace with unit variant.
- **Hand-written `From<Payload> for Reply` impls for 19 variants**
  — macro should generate these (per the /176 note saying the
  macro deliberately doesn't, this is a discipline choice; revisit).
- **Missing observable block**.
- **Manual operation_kind() match for 14 variants** — should be
  generated.

### signal-persona-harness

- **Status**: still on signal_core; old shape.
- **`Harness` prefix** on key types — drop.
- **`MessageSender`, `MessageBody`, `MessageSlot`** duplicated
  from signal-persona-message. Decide ownership.
- **Bidirectional shape**: harness pushes lifecycle events, router
  sends delivery requests. Two-sided like terminal.
- **Missing observable block**.
- **Reply variant naming**: `DeliveryCompleted` / `DeliveryFailed`
  — past-tense success / explicit failure. Clean ✓.

### signal-persona-orchestrate

- **Status**: migrated to signal-frame; per /256, ARCH text still
  mentions `SemaEffectObserved` / `SemaEffectEmitted` (need rename
  to `EffectEmitted` + `SemaObservation` per /254).
- **`RoleIdentifier` (String)** is the right "roles are data"
  shape. signal-persona-mind's enum form is stale; mind should
  consume orchestrate's type or both should share.
- **`WirePath`, `TaskToken`, `ScopeReference`** — duplicated with
  signal-persona-mind. Extract to signal-persona or signal-persona-
  types.
- **Missing observable block**.

### signal-persona-auth (14 lines)

- **Status**: pure types; no channel.
- **Owns**: `ChannelId`, `ComponentName`, `EngineId`,
  `OwnerIdentity`, `MessageOrigin`, `InternalComponentInstanceOrigin`,
  `ConnectionClass`.
- **`InternalComponentInstanceOrigin`** — five-word compound name;
  unwieldy. Possible rename: `InternalOrigin` or
  `LocalComponentOrigin`. The "Instance" word adds nothing the
  type's role already conveys.
- **Otherwise clean for its scope**.

### signal-persona-spirit

Done in /255 / /256. Remaining: §3.1 Timestamp two-field fix.

### owner-signal-persona-mind

- **Status**: migrated to signal-frame; contract-local verbs
  (`Configure`, `Inspect`).
- **`OwnerMind*` aliases** — alias dance per 1.10.
- **`RequestUnimplemented { operation, reason }`** — drop
  operation (OperationKind enum exists only to populate this
  field; drop both).
- **Missing observable block**.
- **Otherwise clean**.

### owner-signal-persona-spirit

Done in /252.

### owner-signal-persona-orchestrate

- **Status**: migrated to signal-frame.
- Need full read pass; likely has similar smells (alias dance,
  RequestUnimplemented redundancy, missing observable).

### owner-signal-persona-router

- **Status**: migrated to signal-frame.
- **`AdjudicationRequestIdentifier`** — full name carries
  `AdjudicationRequest`. The type is just an identifier; should
  be `AdjudicationId` or `RequestId` per the domain (channel-grant
  adjudication is the contract's domain).
- **`TimestampNanoseconds(u64)`** — same shape issue as
  signal-persona's `TimestampNanos`. Seconds suffice.
- **`ChannelMessageKind` (12-variant)** — closed enum mirroring
  every typed channel message in the workspace. This is
  agent-design-cultivated (per /249 gap #22); confirm with psyche
  whether the closed enum is the right shape vs data-table.

### owner-signal-persona-terminal

- **Status**: still on signal_core; old shape.
- Likely similar smells to other unmigrated contracts.

### signal-repository-ledger

- **Status**: migrated to signal-frame. Should be the canonical
  pilot template — verify it matches /255 / /256 shapes.

### owner-signal-repository-ledger

- **Status**: still on signal_core; old shape. Migrate.

### signal-criome

- **Status**: still on signal_core; old shape. Non-persona;
  separate audit scope. Listed for completeness.

## 3 · Cross-contract recommendations

### 3.1 — Macro fixes (signal-frame-macros)

1. **Default to no channel-name prefix on emitted types.** The
   macro's prefix scheme creates the 5-line alias-dance every
   contract repeats. Default: emit `Operation`, `Reply`, `Event`,
   `Frame`, `FrameBody`, etc.; opt-in to a prefix when needed.
2. **Auto-generate `OperationKind`** from the expanded operation
   set (including macro-injected Tap/Untap). Avoids drift between
   hand-maintained enum and macro output.
3. **Optionally auto-generate `From<Payload> for Reply` impls**
   for unique-payload reply variants. Today hand-written across
   contracts (terminal has 19 of them).

### 3.2 — Workspace-wide rename pass

When operator does the big rename slice:

1. `signal-core` → `signal-frame` dependency migration (10
   contracts).
2. Universal-verb shape (`Assert / Match / ...`) → contract-local
   verbs in verb form (10 contracts).
3. Drop ancestry prefixes per §1.5 (multiple contracts).
4. Lift repeated-suffix smells per §1.4 (mind especially).
5. Drop `*RequestUnimplemented.operation/.scope` fields per §1.6.
6. Add observable blocks per §1.10.
7. Execute /252 (signal-persona `supervision::` →
   `engine_management::`).

### 3.3 — Shared type ownership

- `ComponentName`, `EngineId` already in signal-persona-auth — keep.
- `WirePath`, `TaskToken`, `ScopeReference` — extract to
  signal-persona (one level up) since multiple contracts use them.
- `RoleIdentifier` (orchestrate's String form) — own in orchestrate;
  mind drops its `RoleName` enum and imports.
- `IntrospectionTarget` (introspect) vs `ComponentKind`
  (signal-persona) — one is a subset of the other; consolidate.

### 3.4 — Migration order

Suggested operator slice ordering:

1. **signal-persona** `supervision::` → `engine_management::` per
   /252. Unblocks all downstream supervision-socket renames.
2. **owner-signal-persona-mind**, **owner-signal-persona-orchestrate**
   — small surface, demonstrates the cleanup pattern on the
   already-migrated owner side.
3. **signal-persona-mind** — biggest contract, biggest shape
   redesign (channel choreography split + repeated-suffix lift +
   contract-local verbs). High-impact pilot.
4. **signal-persona-router** — observation-side cleanup; introspect
   depends on it.
5. **signal-persona-introspect** — depends on router; consumer of
   every other component's Tap.
6. **signal-persona-message** / **signal-persona-harness** —
   delivery domain, shared types.
7. **signal-persona-system** / **signal-persona-terminal** —
   bidirectional contracts; larger surface.
8. **owner-signal-persona-router** / **owner-signal-persona-terminal**
   — owner-side cleanup.

Each migration follows spirit's template:
- frame dep
- contract-local verbs in macro
- `operation` keyword, drop universal-verb prefixes
- lift repeated-suffix replies
- drop ancestry prefixes
- add observable block
- drop `*RequestUnimplemented.operation`
- replace empty markers with unit variants

## 4 · Open psyche calls

1. **Single-field timestamps in runtime/protocol contexts** (vs the
   two-field rule for intent records). Confirm the boundary —
   intent records are spirit's domain; protocol stamping (message
   submission time, component-ready time, channel duration) is
   different. Designer lean: single-field is OK for protocol;
   nanosecond precision is excessive and should drop to seconds.

2. **Introspect's own observability**. Persona-introspect is the
   *consumer* of every component's Tap stream. Should introspect
   itself be observable (i.e., have its own Tap surface so meta-
   introspection works)? Designer lean: yes, mandatory by the
   2026-05-20T02:00:00Z rule (every persona component supports
   Tap); introspect's Tap subscribers would be a very narrow
   workspace audience but the rule is universal.

3. **Single-variant enums for future variants**. ESSENCE says no
   speculation. signal-persona-system has `SystemTarget::NiriWindow`
   as a single variant. Collapse, or keep as forward-looking
   scaffold? Designer lean: collapse per ESSENCE.

4. **Closed `ChannelMessageKind` enum** (12 variants). Agent-
   cultivated per /249 gap #22. Confirm whether the closed-enum
   shape is intended or whether channel-message-kind should be data
   (string token) like roles.

5. **`signal-persona-mind` channel choreography split** — psyche
   directed Grant/Extend/Revoke/List/Deny at 2026-05-19T20:30 but
   the implementation hasn't landed. Affirm the verb set; operator
   implements.

## 5 · References

- `intent/component-shape.nota` 2026-05-19T19:30, 19:45, 20:00,
  20:30, 2026-05-20T00:07:55+02:00, 02:00:00Z — verb-form,
  contract-local-verbs, repeated-suffix, Tap/Untap.
- `intent/persona.nota` 2026-05-19T20:30 (channel choreography
  split).
- `intent/workspace.nota` 2026-05-19 18:30 — two-field timestamp
  Decision (intent records).
- `ESSENCE.md` §Naming.
- Code under audit: 18 signal-* contracts in
  `/git/github.com/LiGoldragon/`.

This report retires when the operator's migration order in §3.4 is
underway and a successor surfaces remaining contract-specific
issues post-migration.
