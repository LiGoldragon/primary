# 136 — persona-terminal triad audit

*Audit of the persona-terminal triad: `signal-persona-terminal`
(working contract) + `owner-signal-persona-terminal` (owner
contract) + `persona-terminal` (daemon + bundled thin CLI). Of
the three legs, none has been touched by the signal-frame /
signal-executor / contract-local-verb migration. The triad is
the most operationally surface-heavy persona component — fifteen
operations + nineteen replies on the working channel alone — so
the redesign has correspondingly more work to do. Eleven
findings specific to terminal, on top of the workspace-wide
patterns /257 catalogued.*

## 0 · TL;DR

The terminal triad is **fully stale on the old foundation**. It
sits roughly where spirit sat before /255 / /256.

State summary:

- **`signal-persona-terminal`**: still on `signal-core` with
  universal-verb-prefixed operations (`Assert TerminalConnection`,
  `Mutate TerminalResize`, `Retract TerminalDetachment`, `Match
  TerminalCapture`, etc.). Fifteen operations, nineteen reply
  variants, all `Terminal*`-ancestry-prefixed. Three hand-written
  codec impls (`PromptPattern`, `PromptState`,
  `TerminalWorkerStopReason`, `TerminalWorkerLifecycle`,
  `TerminalExitStatus` — actually five). No `observable` block.
  Empty marker `ListSessions {}`. Stale
  `supervision_socket_path` field in `TerminalDaemonConfiguration`.
- **`owner-signal-persona-terminal`**: still on `signal-core`
  with `Mutate CreateSession` / `Retract RetireSession`. Owner
  contract carries `OwnerTerminal*`-ancestry-prefixed types
  (`OwnerTerminalOperationKind`, `OwnerTerminalUnimplementedReason`,
  `OwnerTerminalRequestUnimplemented`). Variants live at the
  crate root, not in a `pub mod owner_terminal`. No observable
  block. The `OwnerTerminalRequestUnimplemented` struct carries
  `terminal`, `operation`, AND `reason` — triple redundancy.
- **`persona-terminal`** daemon: does not depend on
  `signal-frame`, `signal-sema`, or `signal-executor`. No
  `Lowering`, `CommandExecutor`, `ToSemaOperation`,
  `ToSemaOutcome`, or `BatchErrorClassification` impls. The
  socket handling is direct Kameo actor dispatch with `match
  request { TerminalRequest::… }` statements in
  `src/supervisor.rs` and `src/contract.rs`.
- **CLI**: ten bin targets (`persona-terminal-view`,
  `persona-terminal-send`, `persona-terminal-capture`,
  `persona-terminal-type`, `persona-terminal-sessions`,
  `persona-terminal-resolve`, `persona-terminal-signal`,
  `persona-terminal-validate-capture`, `persona-terminal-daemon`,
  `persona-terminal-supervisor`). The intent
  (`intent/component-shape.nota` 2026-05-20T13:00:00Z) is one
  thin CLI named `terminal` — drop the `persona-` prefix and
  fold the verb-specific bins into single-NOTA-argument calls.
  Per /150 §6.4, the **CLI also needs the generated two-socket
  dispatch macro** (per /129).
- **Owner contract is wired-but-not-implemented**: both owner
  variants currently return
  `OwnerTerminalRequestUnimplemented` — the contract shape exists
  on the wire, the daemon doesn't yet execute the session
  lifecycle through it.

**Priority for the triad's next slice** (in order): contract
redesign on signal-frame with contract-local verbs and the
observable block first (mechanical, well-understood from
spirit's template); then session-lifecycle implementation on the
owner contract (currently stub); then daemon migration onto
signal-executor; then the CLI consolidation; then per-channel
splitting per the operational planes (transport / prompt-gate /
worker-lifecycle / session-registry).

## 1 · /257 findings status

Every workspace-wide pattern /257 catalogued applies to this
triad. Status of each:

### /257 §1.1 — old universal-verb shape

**Status: NOT FIXED.** `signal-persona-terminal/src/lib.rs:934-984`
declares the channel using the pre-/238 grammar:

```text
Assert TerminalConnection(...),
Assert TerminalInput(...),
Mutate TerminalResize(...),
Retract TerminalDetachment(...),
Match TerminalCapture(...),
Assert RegisterPromptPattern(...),
Retract UnregisterPromptPattern(...),
Match ListPromptPatterns(...),
Assert AcquireInputGate(...),
Retract ReleaseInputGate(...),
Assert WriteInjection(...),
Subscribe SubscribeTerminalWorkerLifecycle(...) opens TerminalWorkerLifecycleStream,
Retract TerminalWorkerLifecycleRetraction(...),
Match ListSessions(...),
Match ResolveSession(...),
```

Owner side same shape
(`owner-signal-persona-terminal/src/lib.rs:146-158`):

```text
Mutate CreateSession(CreateSession),
Retract RetireSession(RetireSession),
```

All Sema-verb prefixes at the public layer per /257 §1.1.

### /257 §1.4 — repeated-suffix smell

**Status: NOT FIXED.** The terminal reply enum
(`signal-persona-terminal/src/lib.rs:953-974`) carries multiple
sibling families:

- `PromptPattern` siblings: `PromptPatternRegistered`,
  `PromptPatternUnregistered`, `PromptPatternList` (three
  variants sharing the same prefix-suffix structure).
- `Gate` siblings: `GateAcquired`, `GateBusy`, `GateReleased`
  (three siblings — borderline; the parent
  could be a `GateOutcome` enum).
- `Injection` siblings: `InjectionAck`, `InjectionRejected` (two
  — under the threshold but symmetric with `Gate*` for `*Rejected`).
- `Session` siblings: `SessionList`, `SessionResolved` (two —
  could be a `SessionRead` parent symmetric with how `Query`
  collapses in other contracts).
- `Terminal*` future-tense siblings on the request: five
  separate variants (`TerminalConnection`, `TerminalInput`,
  `TerminalResize`, `TerminalDetachment`, `TerminalCapture`) and
  on the reply: seven (`TerminalReady`, `TerminalInputAccepted`,
  `TranscriptDelta`, `TerminalResized`, `TerminalCaptured`,
  `TerminalDetached`, `TerminalExited`).

The terminal-transport family is the deepest case for parent
lifting: a `Transport` operation carrying the five sub-actions,
with a symmetric `Transported` reply variant carrying typed
outcomes. See §2.5 for the proposed shape.

### /257 §1.5 — ancestry-prefixed type names

**Status: NOT FIXED — among the worst offenders.** Per /257
§1.5, this contract was listed as having "about 20+ types"
prefixed with `Terminal`. Verified by reading the source:

Working contract `Terminal*` prefixes
(`signal-persona-terminal/src/lib.rs`):

- `TerminalName` (line 25), `TerminalGeneration` (49),
  `TerminalSequence` (73), `TerminalInputBytes` (88),
  `TerminalTranscriptBytes` (107), `TerminalRows` (135),
  `TerminalColumns` (159), `TerminalByteCount` (183),
  `TerminalConnection` (762), `TerminalInput` (767),
  `TerminalResize` (773), `TerminalDetachment` (780),
  `TerminalDetachmentReason` (786), `TerminalCapture` (793),
  `TerminalReady` (798), `TerminalInputAccepted` (804),
  `TerminalResized` (817), `TerminalCaptured` (825),
  `TerminalDetached` (832), `TerminalExited` (839),
  `TerminalExitStatus` (846), `TerminalRejected` (903),
  `TerminalRejectionReason` (909),
  `TerminalWorkerLifecycleToken` (921),
  `TerminalWorkerLifecycleSnapshot` (750),
  `TerminalWorkerLifecycleEvent` (755),
  `TerminalWorkerStopReason` (543),
  `TerminalWorkerLifecycle` (698), `TerminalWorkerKind` (532),
  `TerminalOperationKind` (511), `TerminalDaemonConfiguration`
  (1222).

That's 31 types. Per the rule (the crate name supplies the
"terminal" context), most drop the `Terminal` prefix:
`Name`, `Generation`, `Sequence`, `InputBytes`,
`TranscriptBytes`, `Rows`, `Columns`, `ByteCount`,
`Connection`, `Input`, `Resize`, `Detachment`, `DetachmentReason`,
`Capture`, `Ready`, `InputAccepted`, `Resized`, `Captured`,
`Detached`, `Exited`, `ExitStatus`, `Rejected`,
`RejectionReason`, `WorkerLifecycleToken`,
`WorkerLifecycleSnapshot`, `WorkerLifecycleEvent`,
`WorkerStopReason`, `WorkerLifecycle`, `WorkerKind`,
`OperationKind`, `DaemonConfiguration`.

Note an edge case: `Worker*` is a sub-domain inside the crate.
If the contract is reshaped per §2.5 to put worker-lifecycle in
its own `pub mod worker_lifecycle` (after the macro emits clean
unprefixed names), then `Worker` itself drops too:
`Lifecycle`, `LifecycleEvent`, `LifecycleSnapshot`,
`LifecycleToken`, `Kind`, `StopReason`.

The owner-side prefix is **`OwnerTerminal*`** — drops to
unprefixed forms after the same migration:
`OwnerTerminalOperationKind` → `OperationKind` (or, in a `pub
mod owner_terminal`, just `OperationKind`),
`OwnerTerminalUnimplementedReason` → `UnimplementedReason`,
`OwnerTerminalRequestUnimplemented` → `RequestUnimplemented`.

### /257 §1.6 — `*RequestUnimplemented { operation, reason }`

**Status: NOT FIXED on owner side.**
`OwnerTerminalRequestUnimplemented`
(`owner-signal-persona-terminal/src/lib.rs:131-136`):

```text
pub struct OwnerTerminalRequestUnimplemented {
    pub terminal: TerminalName,
    pub operation: OwnerTerminalOperationKind,
    pub reason: OwnerTerminalUnimplementedReason,
}
```

Three fields — `operation` is redundant per /257 §1.6, AND
`terminal` is also redundant: the request payload (`CreateSession`
or `RetireSession`) already carries the terminal name, and the
reply is positionally aligned with the request. Drop both;
keep `reason` only:

```text
pub struct RequestUnimplemented {
    pub reason: UnimplementedReason,
}
```

**On the working side**: no `TerminalRequestUnimplemented`
present in the contract today. The terminal contract does not
emit `RequestUnimplemented` at all — its reply enum has no
`Unimplemented` variant. Once the contract migrates to the new
shape (where macro-injected `Tap` / `Untap` plus contract-author
verbs need a fallback for unimplemented surfaces), a
`RequestUnimplemented(RequestUnimplemented)` variant should
appear, carrying `reason` only per the post-fix spirit shape.

### /257 §1.7 — empty marker records

**Status: NOT FIXED.** `ListSessions {}`
(`signal-persona-terminal/src/lib.rs:196`) is the canonical
empty marker. After mixed-enum support landed in `nota-codec`,
this should be a unit variant inside the read parent:

```text
pub enum SessionQuery {
    List,
    Resolve(ResolveSession),
}
```

(Better yet, fold into the broader `Query` parent — see §2.5.)

### /257 §1.9 — frame type alias boilerplate

**Status: PRESENT on owner side, absent on working side**
(strangely). Working
`signal-persona-terminal/src/lib.rs` does NOT have the
`pub type Frame = TerminalFrame;` alias dance — consumers
import the channel-prefixed names directly. Owner
`owner-signal-persona-terminal/src/lib.rs:160-164` HAS the
dance:

```text
pub type Frame = OwnerTerminalFrame;
pub type FrameBody = OwnerTerminalFrameBody;
pub type ChannelRequest = OwnerTerminalChannelRequest;
pub type ChannelReply = OwnerTerminalChannelReply;
pub type RequestBuilder = OwnerTerminalRequestBuilder;
```

Asymmetric. After bead `primary-77hh` (clean macro output) the
dance retires on both sides. Per /258 §2.4's module-isolation
pattern: when the working/owner contracts are co-located in
their respective single-channel crates, `pub mod working` and
`pub mod owner` aren't required at the crate boundary because
the crate names already disambiguate (signal-persona-terminal
vs owner-signal-persona-terminal).

### /257 §1.10 — no observable block

**Status: NOT FIXED.** Neither contract declares an
`observable` block (verified by grep — no occurrences of
`observable`, `Tap`, `Untap`, `OperationReceived`,
`EffectEmitted` across the triad). Persona-terminal is a
persona component — Tap/Untap is mandatory per the
2026-05-20T02:00:00Z Decision. Both contracts need the standard
block:

```text
observable {
    filter default;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

Designer lean (consistent with /258 §1.11 for engine-manager):
**add the observable block to the working contract**, and
**confirm with psyche before adding it to the owner contract**.
Owner contracts are owner-only — subscribers are limited to the
component's owner (orchestrate, per the workspace authority
graph). Persona-introspect introspects the working surface;
adding an observable block to the owner surface lets a future
orchestrate-side observer trace its own administration of
terminal sessions, which may be useful for the engine-manager's
session-lifecycle audit.

### /257 §1.11 — single-field timestamps

**Status: NO TIMESTAMPS in the terminal contract.**
Terminal-domain types are not timestamped (the contract uses
`TerminalSequence` and `TerminalGeneration` instead — sequence
numbers, not wallclock times). The two-field-timestamp question
does not apply here. Per
`intent/component-shape.nota` 2026-05-20T15:00:00Z's
no-op-as-explicit-command rule, terminal sequence/generation
ordering is already structurally correct (every output byte
gets a generation and sequence; the daemon owns minting per
ARCHITECTURE.md §4.1).

### /257 §1.13 — `supervision::` namespace stale

**Status: STALE on this triad too.**
`signal-persona-terminal/src/lib.rs:1228-1230`:

```text
pub supervision_socket_path: signal_persona::WirePath,
pub supervision_socket_mode: signal_persona::SocketMode,
```

These are configuration fields on `TerminalDaemonConfiguration`
naming the supervision socket persona-terminal binds. Per /252,
"supervision" renames to "engine_management" across the
workspace because the persona daemon is the **engine manager**,
not a generic supervisor (kameo's actor-tree-side `Supervisor`
keeps its name). Rename:

- `supervision_socket_path` → `engine_management_socket_path`.
- `supervision_socket_mode` → `engine_management_socket_mode`.

These are downstream of the /252 contract rename in
`signal-persona` (per /258 §2.6 — every supervised daemon's
config carries these fields).

### /257 §3 — bead coverage

The /258 beads apply:

- **`primary-77hh`** (frame alias-dance + clean unprefixed macro
  emission): retires the `pub type Frame = OwnerTerminalFrame;`
  block in the owner contract. Working contract doesn't have
  the dance.
- **`primary-k3bu`** (UnknownKindForVerb rename): this triad's
  hand-written codecs include `UnknownKindForVerb` references in
  `PromptPattern`, `PromptState`, `TerminalWorkerStopReason`,
  `TerminalWorkerLifecycle`, `TerminalExitStatus` — five sites
  in `signal-persona-terminal/src/lib.rs` (lines 293, 433, 689,
  741, 894). All need the rename.
- **`primary-u0lh`** (extend nota-codec derive coverage): the
  same five hand-written codec impls should move to
  `#[derive(NotaSum)]` or `#[derive(NotaEnum)]`. After mixed-enum
  support, all five qualify (`PromptPattern` is a sum with
  payload-carrying and unit variants;
  `PromptState::Dirty { trailing_count }` is mixed too;
  `TerminalExitStatus::Exited { code }` and `Signaled { signal }`
  vs `StatusUnavailable` likewise).

## 2 · New findings specific to this triad

### 2.1 — `Terminal*` ancestry on operation names

In addition to the type-name prefixes (§/257 §1.5 above),
operation **variants** also restate the domain. From the
working channel (lines 937-951):

```text
Assert TerminalConnection(...),
Assert TerminalInput(...),
Mutate TerminalResize(...),
Retract TerminalDetachment(...),
Match TerminalCapture(...),
```

Five operation variants prefixed with `Terminal`. In the
post-migration `operation <Verb>(<Payload>)` form, these become:

```text
operation Connect(Connection),
operation Input(InputBytes),       // or Inject — see §2.7
operation Resize(Resize),
operation Detach(Detachment),
operation Capture(Capture),
```

Drop the `Terminal` prefix from both verb and payload. Same
pattern on the reply side: `TerminalReady` → `Ready`,
`TerminalInputAccepted` → `InputAccepted`, etc.

### 2.2 — Operation tree: fifteen flat operations want planes

The working contract carries fifteen flat operation variants
covering at least four distinct logical planes:

| Plane | Variants | Purpose |
|---|---|---|
| **Transport** | `TerminalConnection`, `TerminalInput`, `TerminalResize`, `TerminalDetachment`, `TerminalCapture` | Move bytes / state between viewer and PTY. |
| **Prompt-pattern lifecycle** | `RegisterPromptPattern`, `UnregisterPromptPattern`, `ListPromptPatterns` | Manage prompt patterns per terminal. |
| **Input gate + injection** | `AcquireInputGate`, `ReleaseInputGate`, `WriteInjection` | Coordinate writer-side arbitration. |
| **Worker lifecycle subscription** | `SubscribeTerminalWorkerLifecycle`, `TerminalWorkerLifecycleRetraction` | Push lifecycle observations. |
| **Session registry read** | `ListSessions`, `ResolveSession` | Read the component registry. |

Per the schema-as-tree principle
(`intent/naming.nota` 2026-05-19T18:50:00Z + 18:55:00Z), four
planes flat at the operation root is one of the diagnostic
patterns. The shape that reads best:

```text
operation Connect(Connection),
operation Send(Sending),        // typed sum: Input | Resize | Capture
operation Detach(Detachment),
operation Register(PromptPatternRegistration),
operation Unregister(PromptPatternUnregistration),
operation Query(Query),         // typed sum: PromptPatterns | Sessions | ResolveSession
operation Gate(GateOperation),  // typed sum: Acquire | Release
operation Inject(Injection),
operation Watch(Subscription) opens WorkerLifecycleStream,
operation Unwatch(SubscriptionToken),
```

Or, by tightening further, the transport-family lifts:

```text
operation Connect(Connection),
operation Transport(Transmission),  // Input | Resize | Capture | Detach
operation Register(PromptPatternRegistration),
operation Unregister(PromptPatternUnregistration),
operation Query(Query),
operation Gate(GateOperation),
operation Inject(Injection),
operation Watch(Subscription) opens WorkerLifecycleStream,
operation Unwatch(SubscriptionToken),
```

Designer call: nine operations is still a lot. Whether to
collapse `Transport` to a sum or keep the five sub-operations
flat depends on whether `Connect` / `Resize` / `Capture` need
distinct semantics — they do (Connect produces `Ready`; Resize
produces `Resized`; Capture produces `Captured`; Input produces
`InputAccepted`). The right shape may be **`operation Send(Sending)`**
carrying just the transport-of-bytes variants
(`Input`, `Resize`, `Capture`) while `Connect` and `Detach`
stay separate as session-state transitions. Confirm with psyche
before committing.

### 2.3 — `PromptPattern` enum is hand-written codec (per /257 hint)

The `PromptPattern` enum
(`signal-persona-terminal/src/lib.rs:255-299`) is hand-written
`NotaEncode` / `NotaDecode`:

```text
pub enum PromptPattern {
    LiteralSuffix(PromptPatternBytes),
    RegexSuffix { pattern: PromptPatternBytes },
}
```

Note the asymmetry between variants: `LiteralSuffix` is a
tuple-style variant (positional `PromptPatternBytes`),
`RegexSuffix` is a struct-style variant with a named field
`pattern: PromptPatternBytes`. Both wrap exactly the same type
in exactly the same way; the field name `pattern` in
`RegexSuffix` adds nothing — the variant tag already says
"this is a regex prompt pattern" and the payload is the
pattern bytes. Two fixes:

1. **Normalize both variants to tuple form**: `LiteralSuffix(PromptPatternBytes)`
   and `RegexSuffix(PromptPatternBytes)`. Then `#[derive(NotaSum)]`
   (or `NotaEnum` if `nota-codec` calls homogeneous tuple-sum
   that). Drops the hand-written codec.
2. **OR fold `pattern` field into NotaSum/NotaEnum support** if
   the codec generator supports mixed payload-shapes — but the
   minimal cleanup is normalising the variant shape so the
   derive applies.

Mixed-enum codec support exists per
`intent/component-shape.nota` 2026-05-21T01:15:44+02:00 (macro
auto-generates structurally derivable boilerplate). The
hand-written codec is technical debt the macro should retire.

Same story applies to `PromptState` (lines 387-439),
`TerminalWorkerStopReason` (542-695),
`TerminalWorkerLifecycle` (697-747), `TerminalExitStatus`
(845-900) — five hand-written codecs.

### 2.4 — Event stream shapes (worker lifecycle, prompt state)

The contract declares **one event stream** today:

```text
stream TerminalWorkerLifecycleStream {
    token TerminalWorkerLifecycleToken;
    opened TerminalWorkerLifecycleSnapshot;
    event TerminalWorkerLifecycleEvent;
    close TerminalWorkerLifecycleRetraction;
}
```

Inputs:

- Worker lifecycle observations on the running terminal session.
- One opened-snapshot + delta-event stream pattern (matches the
  /176 §1 stream-block grammar).

The Subscribe variant
(`SubscribeTerminalWorkerLifecycle(SubscribeTerminalWorkerLifecycle)`)
carries only `terminal: TerminalName`. The empty
`SubscribeTerminalWorkerLifecycle` record is shaped as a
single-field record — could be the bare `TerminalName` after
the ancestry drop (`Subscribe(Name)`), but the surrounding
`SubscribeTerminalWorkerLifecycle` filter-style payload signals
this **could grow filter fields** in future. Keep the wrapper
record for forward-evolution; rename to `WorkerLifecycleFilter`
or similar.

Per /150 §6.4: "event streams for worker lifecycle and
transcript/prompt state" — terminal **should** carry more
streams than just worker lifecycle. Two additional stream
candidates surface from the current contract:

1. **Transcript stream**: `TranscriptDelta` is currently a
   `reply` variant (line 956 in the reply enum), but it
   behaves more like an event (PTY produces transcript bytes
   continuously). Today, `TerminalCapture` is a one-shot
   request that returns `TerminalCaptured` (full transcript
   capture). A subscription that pushes `TranscriptDelta`
   events would let viewers observe deltas without polling.
   The current reply-level `TranscriptDelta` is structurally a
   confusing mid-tier — it sits in the reply enum but is the
   PTY's ongoing output, not a one-shot reply to a request.
   Move it to an event stream: `TranscriptStream`.
2. **Prompt-state stream**: `PromptState` changes as the user
   types or as injected bytes resolve. Today, prompt state is
   surfaced only via `GateAcquired` reply (line 466 — embeds
   `PromptState`). A push stream lets the harness observe
   prompt-state transitions without re-acquiring the gate.
   Open question: is this needed, or does the gate-acquire
   loop suffice? Designer lean: **defer the prompt-state
   stream** until a concrete consumer requests it; the gate
   loop covers today's harness path.

So a redesigned event surface might be:

```text
stream WorkerLifecycleStream {
    token WorkerLifecycleToken;
    opened WorkerLifecycleSnapshot;
    event WorkerLifecycleEvent;
    close Unwatch;
}

stream TranscriptStream {
    token TranscriptToken;
    opened TranscriptSnapshot;   // initial scrollback
    event TranscriptDelta;
    close Unwatch;
}
```

Plus the standard observer stream (macro-injected via
`observable` block).

Confirm with psyche before adding the transcript stream — it's
a real shape change in the contract.

### 2.5 — Repeated-suffix smell: lift reply families

Worked example for the terminal reply side. Today's flat
nineteen-variant reply (line 953-974):

```text
reply TerminalReply {
    TerminalReady, TerminalInputAccepted, TranscriptDelta,
    TerminalResized, TerminalCaptured, TerminalDetached,
    TerminalExited, TerminalRejected,
    PromptPatternRegistered, PromptPatternUnregistered, PromptPatternList,
    GateAcquired, GateBusy, GateReleased,
    InjectionAck, InjectionRejected,
    TerminalWorkerLifecycleSnapshot,
    SubscriptionRetracted,
    SessionList, SessionResolved,
}
```

After ancestry drop and parent lifting (lift the suffix into a
parent enum), the shape that reads cleanly:

```text
reply Reply {
    Connected(Ready),                   // was TerminalReady
    Transported(TransportOutcome),       // was InputAccepted | Resized | Captured | Detached | Exited | TranscriptDelta
    TransportRejected(RejectionDetail),  // was TerminalRejected (with reason enum)
    Registered(PromptPatternRegistered),
    Unregistered(PromptPatternUnregistered),
    Queried(QueryResult),                // was ListSessions reply | ResolveSession reply | ListPromptPatterns reply
    Gated(GateOutcome),                  // was GateAcquired | GateBusy | GateReleased
    Injected(InjectionOutcome),          // was InjectionAck | InjectionRejected
    Watched(SubscriptionOpened),
    Unwatched(SubscriptionRetracted),
    Unimplemented(RequestUnimplemented),
}
```

Parent enums absorb the sibling families:

```text
pub enum TransportOutcome {
    InputAccepted(InputAccepted),
    Resized(Resized),
    Captured(Captured),
    Detached(Detached),
    Exited(Exited),
}

pub enum QueryResult {
    PromptPatterns(PromptPatternList),
    Sessions(SessionList),
    SessionResolved(SessionResolved),
}

pub enum GateOutcome {
    Acquired(GateAcquired),   // with the prompt_state field
    Busy(GateBusy),
    Released(GateReleased),
}

pub enum InjectionOutcome {
    Acknowledged(InjectionAck),
    Rejected(InjectionRejected),  // with the reason enum
}
```

Significantly fewer top-level variants (eleven vs nineteen).
Each parent enum names a complete read or write outcome.

### 2.6 — Owner contract: split between ordinary & owner is correct, but ancestry-prefixed

Per /150 §6.4 and the active-repositories.md guidance, the
correct authority split is in place: **`CreateSession` and
`RetireSession` are owner-only**, on
`owner-signal-persona-terminal`; ordinary terminal queries and
operations stay on `signal-persona-terminal`. That structural
boundary is correct.

What's wrong on the owner side: every owner-side type carries
the `OwnerTerminal` prefix — `OwnerTerminalOperationKind`,
`OwnerTerminalReply`, `OwnerTerminalRequest`,
`OwnerTerminalRequestUnimplemented`,
`OwnerTerminalUnimplementedReason`. The crate is
`owner-signal-persona-terminal`; the prefix is restating the
entire crate name.

After ancestry drop:

```text
// owner-signal-persona-terminal/src/lib.rs
pub enum OperationKind { CreateSession, RetireSession }
pub struct RequestUnimplemented { pub reason: UnimplementedReason }
pub enum UnimplementedReason { NotBuiltYet, DependencyTrackNotLanded }
signal_channel! {
    channel OwnerTerminal {
        operation CreateSession(CreateSession),
        operation RetireSession(RetireSession),
    }
    reply Reply {
        SessionCreated(SessionCreated),
        SessionRetired(SessionRetired),
        Unimplemented(RequestUnimplemented),
    }
    observable { … }  // confirm with psyche per §1.10 above
}
```

Note: variants in the channel macro are no longer
ancestry-prefixed; the channel name `OwnerTerminal` is still the
channel's wire name (no harm — it's load-bearing for the macro
to disambiguate).

### 2.7 — `TerminalInput` vs `WriteInjection` plane separation

The contract carries two distinct write paths for bytes-to-PTY:

- `TerminalInput { terminal, bytes: TerminalInputBytes }`
  (transport plane) — raw keyboard bytes from a viewer adapter.
- `WriteInjection { terminal, lease: InputGateLease, bytes: TerminalInputBytes }`
  (gate-and-inject plane) — programmatic injection under a held
  lease.

These are different operations with different authorization
(injection requires a lease; raw input does not). The shape is
correct. After ancestry drop:

```text
operation Send(InputBytes),         // raw input transport
operation Inject(Injection),        // gate-and-inject
```

(Or `operation Input(Input)` if `Input` is unambiguous in the
contract — but `Send` clarifies the action's intent.)

The reply asymmetry needs naming attention: `TerminalInputAccepted`
on the transport side, `InjectionAck` / `InjectionRejected` on
the injection side. After cleanup:
`Input → InputAccepted`, `Inject → InjectionOutcome::{Acknowledged,Rejected}`.

### 2.8 — Persona-terminal daemon does not use signal-executor

Verified: `persona-terminal/Cargo.toml` depends on `signal-core`
not `signal-frame`, has no `signal-executor` or `signal-sema`
dep, and no `Lowering` / `CommandExecutor` / `ToSemaOperation` /
`ToSemaOutcome` / `BatchErrorClassification` impls anywhere.
This is the same gap /258 §2.2 flagged for the engine-manager,
applied to terminal.

The current dispatch path:

- `persona-terminal-supervisor` binary binds the terminal
  communication socket.
- `TerminalSupervisor` Kameo actor (in `src/supervisor.rs`)
  receives raw signal frames, decodes via `signal-core`,
  matches on `TerminalRequest::…` variants directly, dispatches
  to per-terminal `TerminalSession` actors.
- Each `TerminalSession` actor wraps a `terminal-cell` library
  instance and forwards control-plane frames to the cell's
  `control.sock`.

The migration shape:

```text
struct TerminalLowering { /* … */ }
impl Lowering for TerminalLowering {
    type Operation = TerminalOperation;
    type Reply = TerminalReply;
    type Command = TerminalCommand;       // local enum
    type ComponentEffect = TerminalEffect; // local enum
    fn lower(...) -> Result<OperationPlan<TerminalCommand>, TerminalReply> { ... }
    fn reply_from_effects(...) -> TerminalReply { ... }
}

struct TerminalCommandExecutor { /* … */ }
impl CommandExecutor for TerminalCommandExecutor { ... }

impl BatchErrorClassification for TerminalError { ... }
```

`TerminalCommand` enum carries the daemon-internal executable
language (per /150 §3.5):

```text
pub enum TerminalCommand {
    AttachSession(SessionAttach),
    WriteBytes(WriteBytes),
    ResizeWindow(ResizeWindow),
    CaptureTranscript(CaptureRequest),
    DetachSession(DetachRequest),
    RegisterPattern(PatternRegistration),
    UnregisterPattern(PatternRetraction),
    AcquireGate(GateAcquisition),
    ReleaseGate(GateRelease),
    InjectUnderLease(LeasedInjection),
    SubscribeWorkerLifecycle(WorkerLifecycleSubscription),
    UnsubscribeWorkerLifecycle(WorkerLifecycleRetraction),
    ListSessions,
    ResolveSession(SessionResolution),
}
```

Plus `ToSemaOperation` impl: most variants project to
`Assert` (record an event), `Mutate` (resize, attach, detach),
`Match` (queries), `Subscribe` (worker lifecycle). The
projection's purpose is workspace-wide observation — knowing
"in the last minute, how many `Mutate`s did terminal serve" is
a class-level introspect query.

Operationally this is the **load-bearing structural change**
for the triad — same shape as spirit's migration (per /150 §5).

### 2.9 — Owner contract is wired-but-not-implemented

Both owner operations currently fall through to
`OwnerTerminalRequestUnimplemented` per
`persona-terminal/src/supervisor.rs:620-630`:

```text
fn event_for_owner_request(&mut self, request: OwnerTerminalRequest) -> OwnerTerminalReply {
    let terminal = match request {
        OwnerTerminalRequest::CreateSession(payload) => payload.name.clone(),
        OwnerTerminalRequest::RetireSession(payload) => payload.name.clone(),
    };
    OwnerTerminalRequestUnimplemented { … }
}
```

The contract shape exists; the daemon implementation does not.
This means today's terminal-session lifecycle (the
`persona-terminal-daemon` binary's session creation) still uses
the transitional `--name` argv and shell-script orchestration —
not the typed `CreateSession` / `RetireSession` operations.

Per the persona.nota 2026-05-19T15:04:19Z Decision (raw MVP
with both contracts shipping), the owner-contract surface must
do real work. The implementation path:

1. Add `CreateSession` and `RetireSession` to the daemon's
   `OwnerTerminalCommand` enum.
2. The `CommandExecutor` calls into the existing
   `terminal-cell` spawn logic (already in
   `src/pty.rs::PtyDaemon`) instead of accepting `--name` argv.
3. `SessionCreated` reply carries the session's data socket
   path (already typed in the contract as
   `SessionCreated { name, data_socket_path }`).
4. `SessionRetired` reply carries the exit status (already
   typed).

This is the second-priority work after the contract redesign:
the owner-contract is the spawn path; without it, the
transitional `--name` argv path can't retire.

### 2.10 — CLI: ten bin targets → one thin `terminal` CLI

`persona-terminal/Cargo.toml:14-52` declares ten `[[bin]]`
entries. Per the universal CLI rule
(`intent/component-shape.nota` 2026-05-20T13:00:00Z):

- The CLI binary name is the daemon binary minus `-daemon`:
  `persona-terminal-daemon` → `terminal`.
- One CLI per triad. Verb-specific bins
  (`persona-terminal-view`, `-send`, `-capture`, `-type`,
  `-sessions`, `-resolve`, `-signal`, `-validate-capture`)
  collapse into one binary taking one NOTA argument.

The ten today:

| Bin | Shape | Migration |
|---|---|---|
| `persona-terminal-daemon` | The daemon | Keep; rename to `terminal-daemon`. |
| `persona-terminal-supervisor` | Transitional | Folds into the daemon. |
| `persona-terminal-view` | Viewer client (raw data plane) | Stays separate per the data-plane carve-out (`skills/component-triad.md` §"Named carve-outs" #2). Rename to `terminal-view`. |
| `persona-terminal-send` | Sends `TerminalInput` | Folds into the `terminal` CLI as a NOTA invocation. |
| `persona-terminal-capture` | Sends `TerminalCapture` | Folds. |
| `persona-terminal-type` | Sends typed input | Folds. |
| `persona-terminal-sessions` | Reads session registry | Folds. |
| `persona-terminal-resolve` | Resolves session name | Folds. |
| `persona-terminal-signal` | Signal client for the contract | Folds — this **IS** the thin CLI's behavior. |
| `persona-terminal-validate-capture` | Test/debug utility | Stays separate; pure offline validator, not a Signal client. Could move out to a sibling test crate. |

After consolidation, the triad's binaries:

- `terminal-daemon` (the daemon)
- `terminal` (the thin CLI; one NOTA arg, two-socket dispatch)
- `terminal-view` (raw data-plane viewer, separate carve-out)
- `terminal-validate-capture` (offline test utility — should
  move to a `dev-bin/` or test crate)

Four bins, not ten. Per /150 §6.4, the **CLI also needs the
generated two-socket dispatch macro** (per /129).

### 2.11 — `signal-persona-terminal-test` fixture crate is empty

`/git/github.com/LiGoldragon/signal-persona-terminal-test/`
contains only a `.git` directory and a README — no Cargo.toml,
no src/. The repository was created (likely intent
`intent/component-shape.nota` 2026-05-19T15:04:19Z which scoped
"temporary repositories to see") but never populated.

The post-migration contract round-trip tests live in
`signal-persona-terminal/tests/` (per the standard contract
crate shape). If the `-test` crate is meant to be the test
fixtures crate for cross-consumer round-trips (e.g., what
persona-introspect or persona-harness needs to assert against
the terminal contract), it should land per the standard shape.
If not, retire the empty repo.

Designer call: **retire `signal-persona-terminal-test`** unless
the psyche has a specific cross-consumer fixture use case for
it. The standard
`signal-persona-terminal/tests/round_trip.rs` covers NOTA + rkyv
round-trips inside the contract crate.

## 3 · Owner signal audit

Specific to the owner contract
(`/git/github.com/LiGoldragon/owner-signal-persona-terminal/src/lib.rs`):

### 3.1 — Variants and their authority direction

Two owner-side variants:

```text
operation CreateSession(CreateSession),   // owner orders terminal to create a session
operation RetireSession(RetireSession),   // owner orders terminal to retire a session
```

The authority direction is correct: persona-terminal is owned by
persona-orchestrate per the workspace authority graph
(`skills/component-triad.md`). Orchestrate issues
`CreateSession` / `RetireSession`; terminal obeys. The mind/body
analogy (`intent/component-shape.nota` 2026-05-20T13:45:00Z)
applies — orchestrate handles routine session lifecycle without
mind's involvement; mind reaches in only for cognitive override.

Future cognitive verbs (e.g., "mind decides this session should
persist longer because the user is mid-conversation") would
land on `owner-signal-persona-orchestrate`, not here. The owner
contract is the right surface for spawn/retire orders.

### 3.2 — Missing: lifecycle / configuration operations

Per /150 §3.4 "owner contracts carry policy and privileged
lifecycle operations," the terminal owner contract is **thin**:
only two session-lifecycle variants, no policy/configuration
mutations. What's missing:

- **`Configure(Configuration)`**: where do session creation
  policies live? E.g., default working directory, environment
  variable scrub list, command allowlist. Per /150's working/policy-state
  taxonomy and `intent/component-shape.nota` 2026-05-19T01:30:00Z
  (every triad daemon has policy state), terminal's policy
  state must be settable via owner Mutate. Today there is no
  `Configure` verb.
- **`Inspect(Inspection)`**: read-side query of policy state.
  Symmetric with Configure.

Designer lean: add `Configure` and `Inspect` to the owner
contract, even if the initial Configuration record is empty
(e.g., `Configuration {}` — no policy knobs yet). The shape
prevents the contract from being expanded incoherently later.

Confirm with psyche before adding — terminal may genuinely have
no policy state today, in which case wait until a real
configuration field is needed before introducing the verb.

### 3.3 — `re-export from signal-persona-terminal` pattern

`owner-signal-persona-terminal/src/lib.rs:9`:

```text
pub use signal_persona_terminal::{TerminalExitStatus, TerminalName};
```

Re-exports two types from the working contract. Standard
shape — the owner contract refers to identity types
(`TerminalName`) that need to match across both contracts.
After ancestry drop, the owner contract imports `Name` and
`ExitStatus` from the working contract crate. The re-export
stays.

Note: `signal_persona_auth::OwnerIdentity` is referenced in the
working contract's `TerminalDaemonConfiguration` (line 1234) but
NOT in the owner contract. The owner identity is a property of
the daemon configuration (set at spawn by the engine-manager),
not a per-operation field. Fine as-is.

### 3.4 — Hand-written `From` and `operation_kind` impls

`owner-signal-persona-terminal/src/lib.rs:166-203` hand-rolls
`operation_kind` and five `From` impls. Per
`intent/component-shape.nota` 2026-05-21T01:15:44+02:00, these
are structurally derivable — the `signal_channel!` macro should
emit them. After bead `primary-77hh` lands the auto-generation,
this whole block drops out.

## 4 · Recommended next slice for the terminal triad

In priority order, modeled on /258's recommendations:

1. **`primary-k3bu`** (rename UnknownKindForVerb in consumers).
   Touches five hand-written codec sites in
   `signal-persona-terminal/src/lib.rs`. Unblocks compile against
   current nota-codec.
2. **`primary-u0lh`** (migrate the five hand-written codecs to
   `NotaSum` / `NotaEnum` derives). Normalises `PromptPattern`
   variants to tuple form per §2.3 first.
3. **Migrate the working contract to signal-frame** with
   contract-local verbs and the observable block. This is the
   biggest mechanical pass on this triad — fifteen operations
   reduce to ~nine via parent-lifting per §2.2 and §2.5; the
   ~31 `Terminal*`-prefixed types drop to unprefixed forms; the
   five hand-written codecs become derives; `ListSessions {}`
   becomes a unit variant; the observable block lands.
4. **Migrate the owner contract to signal-frame**. Same shape
   (drop `OwnerTerminal` prefix, fix triple-redundant
   `RequestUnimplemented`, decide observable-block question per
   psyche). Add `Configure` / `Inspect` if psyche confirms.
5. **Implement `CreateSession` / `RetireSession` for real on
   the daemon** (the §2.9 work). The owner contract is
   wired-but-stub today; this is where the transitional
   `--name` argv path retires.
6. **Migrate persona-terminal daemon onto signal-executor** (the
   §2.8 work). Define `TerminalCommand` / `TerminalEffect` enums;
   impl `Lowering` / `CommandExecutor` /
   `BatchErrorClassification`. Wrap the existing Kameo actor
   mesh inside the `CommandExecutor` impl per spirit's
   template.
7. **Add transcript stream** (`TranscriptStream`) per §2.4.
   Confirm with psyche before — it's a real shape change.
8. **CLI consolidation** (the §2.10 work). Ten bins collapse to
   four. Generated two-socket dispatch macro (per /129)
   replaces the per-bin manual frame construction.
9. **Rename `supervision_socket_*` fields to
   `engine_management_socket_*`** per /252 (downstream of the
   contract rename in `signal-persona`).
10. **Per-plane sub-channel split** (designer follow-up).
    Whether the working contract should split into
    `transport`, `prompt_gate`, `worker_lifecycle`,
    `session_registry` sub-channels (each as a `pub mod` per
    /257 §1.10) is a bigger design call. Per /150 §6.4:
    "runtime actors for each logical plane" — the daemon
    already has plane-shaped Kameo actors (`TerminalSignalControl`
    for prompt-pattern + gate; `TerminalSupervisor` for the
    socket and registry). Multi-channel contract is the natural
    parallel, but warrants confirmation.

## 5 · Cross-cutting note

The terminal triad's migration is **structurally identical** to
spirit's that landed in /255 / /256 and engine-manager's
(unexecuted; tracked in /258). Same template:

| Step | Spirit | Engine-manager | Terminal |
|---|---|---|---|
| signal-core → signal-frame | done | done | NOT DONE |
| Old verbs → contract-local | done | done | NOT DONE |
| Subscription collapse | done | n/a | NOT DONE (worker-lifecycle subscribe → Watch/Unwatch) |
| Field/empty-marker cleanup | done | partial (GracefulStop) | NOT DONE (ListSessions, PromptPattern variant asymmetry) |
| Daemon onto signal-executor | done | NOT DONE | NOT DONE |
| Observable block | done | NOT DONE | NOT DONE |
| `*Unimplemented.operation` drop | done | already clean | NOT DONE (owner side: triple-redundant) |
| Ancestry prefix drop | done | mostly clean | NOT DONE (31 `Terminal*`-prefixed types) |
| Owner contract real work | done | n/a | NOT DONE (currently stub Unimplemented) |
| Hand-written codec → derive | done | partial | NOT DONE (5 codecs) |

Spirit's gap was the smallest; engine-manager's was medium;
terminal's is the largest single-component gap in the
workspace. None of the spirit-template fixes have landed here.

## 6 · References

- `/255`, `/256` — spirit audits (template).
- `/257` — workspace-wide name/shape audit.
- `/258` — engine-manager triad audit (parallel structure).
- `/150` (operator) — current triad migration handoff;
  §6.4 carries terminal-specific guidance.
- `/129` (designer-assistant) — Mind/Orchestrate payload + CLI
  dispatch Option A sketch (the macro that emits the
  two-socket dispatch table the terminal CLI needs).
- `/11` (second-operator-assistant) — signal-type naming and
  shape design guideline (the canonical workspace guidance).
- `intent/persona.nota` 2026-05-20T13:00:00Z — six CLI-design
  records (universal CLI shape).
- `intent/component-shape.nota` 2026-05-19T19:30:00Z + 19:45 +
  20:00 — contract-local verbs supersede Sema-verb prefixes.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z —
  Tap/Untap mandatory for persona components.
- `intent/component-shape.nota` 2026-05-21T01:15:44+02:00 —
  macro auto-generates OperationKind / From impls.
- `intent/component-shape.nota` 2026-05-21T10:30:00Z —
  modules-not-options for macro disambiguation.
- `intent/persona.nota` 2026-05-21T10:00:00Z — debug-the-debugger.
- Beads: `primary-77hh`, `primary-k3bu`, `primary-u0lh`.
- Code under audit:
  `signal-persona-terminal/src/lib.rs`,
  `owner-signal-persona-terminal/src/lib.rs`,
  `persona-terminal/src/*.rs`,
  `persona-terminal/Cargo.toml`,
  `persona-terminal/ARCHITECTURE.md`.

## 7 · Open questions for psyche

These need confirmation before further design moves:

1. **Operation-tree shape**: should the five transport-family
   variants (`Connect`, `Input`, `Resize`, `Capture`, `Detach`)
   collapse into a single `Transport(Transmission)` parent enum,
   or stay as separate root operations? Designer lean: keep
   `Connect` and `Detach` separate (lifecycle); lift
   `Input` / `Resize` / `Capture` into `Send(Sending)` (the
   bytes-and-state transport family). See §2.2 / §2.5.
2. **Per-plane sub-channel split**: should the working contract
   split into `transport`, `prompt_gate`, `worker_lifecycle`,
   `session_registry` sub-channels (each in a `pub mod`)? The
   daemon already has plane-shaped Kameo actors. See §4 #10.
3. **Transcript stream**: add `TranscriptStream` per §2.4 (move
   `TranscriptDelta` from a reply variant to an event stream),
   or keep the current shape where viewers observe transcript
   bytes via the raw data socket and `TerminalCapture` returns
   one-shot snapshots?
4. **Owner observable block**: per /258 §1.11, the
   working-channel observable block is uncontroversial; the
   owner-channel observable block is the question. For
   terminal, would orchestrate-side observers want to observe
   their own `CreateSession` / `RetireSession` orders via
   persona-introspect? Designer lean: **add the observable
   block to owner too** — terminal's owner surface is
   session-creation traffic, which is exactly the
   meta-introspection use case (debug the debugger).
5. **Owner `Configure` / `Inspect` variants**: add now (per
   §3.2 — the universal owner-contract shape) even though no
   concrete policy fields exist yet, or defer until a real
   policy field surfaces?
6. **`signal-persona-terminal-test` crate**: empty repository;
   retire it, or populate it with cross-consumer fixtures?
   Designer lean: retire — standard `tests/round_trip.rs`
   inside `signal-persona-terminal` covers contract-local
   round-trips.

This report retires when (a) the contract redesign lands AND
the daemon migrates onto signal-executor AND the observable
block is added AND the owner contract becomes real work, OR (b)
a successor audit supersedes.
