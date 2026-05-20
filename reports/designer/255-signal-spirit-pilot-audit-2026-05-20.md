# 255 — signal/sema/spirit pilot audit (deep code read)

*Designer audit of the work in /144 and /145, with an actual code
read across signal-frame, signal-sema, signal-executor,
signal-persona-spirit, and persona-spirit. The infrastructure side
is clean and matches the spec; the pilot side has a load-bearing
gap and several contract smells that should be fixed before spirit
becomes the canonical intent substrate.*

## 0 · TL;DR — three findings ranked

**Finding 1 (critical): `signal-executor` is unused.** No daemon in
the workspace imports `signal-executor`. Spirit, the declared pilot,
processes requests through its own Kameo actor mesh
(`actors/dispatch.rs`, `actors/root.rs`, etc.) and never invokes
`Executor::execute()`, `Lowering::lower()`, or
`CommandExecutor::execute_atomic_batch()`. The
`persona-spirit::observation::Command`/`Effect` types impl
`ToSemaOperation`/`ToSemaOutcome`, but they're exercised only in
`tests/sema_projection.rs` — the production request path doesn't go
through them. The pilot doesn't actually pilot the framework.

**Finding 2 (major): contract-level smells in
`signal-persona-spirit`.** Triple-redundant subscription reply
variants (`StateSubscriptionOpened` / `RecordSubscriptionOpened` /
`SubscriptionOpened` co-exist); empty-marker payloads
(`StateObservation {}`, `QuestionPending {}`, `StateSubscription {}`)
that should be plain enum variants; `Statement { statement:
StatementText }` self-redundant field; `RequestUnimplemented`
carries a redundant `operation` field already known positionally.
These violate the "no repeated suffix" rule from
`intent/component-shape.nota` 2026-05-20T00:07:55+02:00 and the
"names don't carry full ancestry" essence rule.

**Finding 3 (design judgment): introspection thinness via
`Tap`/`Untap`.** Spirit's `OperationReceived` carries only
`OperationKind` (a 7-variant enum tag) and `EffectEmitted` carries
only `SemaObservation` (6×7 payloadless classes). Observers see "a
Record operation arrived, Asserted outcome" — but not what was
recorded. For psyche-introspect cross-component class-monitoring,
this is the right thinness. For the substrate-replacement use case
(persona-introspect surfacing intent records back to the psyche),
this is too thin and introspect will have to read records out of
spirit's storage through the domain `Watch` path. Worth confirming
the two-channel split is intentional.

## 1 · The current daemon flow

What spirit actually does today (verified by reading
`persona-spirit/src/actors/dispatch.rs` lines 38-90 and
`persona-spirit/src/actors/root.rs`):

```text
SocketFrame
  -> codec decodes SpiritRequest (signal-persona-spirit)
  -> SpiritRoot actor receives SubmitRequest
  -> IngressPhase records the request
  -> DispatchPhase routes by SpiritRequest variant:
       State(stmt) -> ClassifierPlane -> RecordStore::CaptureEntry
       Record(entry) -> RecordStore::CaptureEntry
       Observe(...) -> StatePlane / RecordStore / QuestionsPending
       Watch(...) -> SubscriptionPlane open
       Unwatch(...) -> SubscriptionPlane retract
       (Tap/Untap and other unimplemented) -> ReplyShaper::ShapeUnimplemented
  -> ReplyShaper produces SpiritReply
  -> SocketFrame back to caller
```

Notably absent: any call to `signal_executor::Executor`, any
construction of an `OperationPlan<Command>`, any
`BatchPlan<Command>` going through `execute_atomic_batch`.

The `Command` enum in `persona-spirit::observation` (12 variants)
mirrors what *would* be the daemon's command set, and its impls of
`ToSemaOperation` / `ToSemaOutcome` are exactly what the framework
expects. But the daemon doesn't lower SpiritRequest into Command —
it dispatches SpiritRequest directly to actors, and the actors
write to redb directly.

`tests/sema_projection.rs` is the only consumer:

```rust
fn observation_for(request: SpiritRequest, reply: SpiritReply) -> SemaObservation {
    let command = Command::from_request(request).expect(...);
    let effect = Effect::from_reply(reply);
    effect.sema_observation_for(&command)
}
```

— builds a Command from a request, an Effect from the reply, and
checks the projection. The projection works; the production path
just doesn't go through it.

## 2 · Finding 1: the framework is unused

### Why this matters

The signal-executor refactor (commits up to /144) landed the
following surface as workspace infrastructure:

- `Lowering` trait with `Operation / Reply / Command /
  ComponentEffect` associated types.
- `CommandExecutor` trait, `Error: BatchErrorClassification` bound.
- `OperationPlan<Command>` / `BatchPlan<Command>` /
  `BatchEffects<Command, ComponentEffect>` /
  `OperationEffects<Command, ComponentEffect>` /
  `CommandEffect<Command, ComponentEffect>`.
- `Executor<L, S>` orchestrator with publisher hooks,
  domain-rejection / batch-abort / committed reply construction.
- `ObserverChannel` / `ObserverSet` / `FrameObserverBridge`
  composition.

**No persona daemon uses any of this.** A grep across all repo
sources shows zero `use signal_executor::` imports outside of
signal-executor's own tests. The persona-spirit Cargo.toml does
not depend on signal-executor.

`/143` (operator) warned of this exact failure mode:
*"the danger is not the current crate split; the danger is endless
infrastructure refinement without a real daemon proving cognitive
value."* The infrastructure has landed in clean shape with strong
library tests. The pilot was supposed to prove it works at the
daemon level. The pilot does not currently use it.

### What this implies

The /144 "lower-component slice" passed. The /145 handoff is
honest about what's implemented and what isn't. But the framing
*"persona-spirit is the first signal-executor pilot"* (from
/254, /145, /248) does not match the code. Spirit is operational,
but it's operating on its old hand-rolled actor pipeline, not on
the executor framework.

Either:

- **(a) Migrate spirit's request path onto signal-executor**:
  Spirit's daemon constructs a `signal_executor::Executor<L, S>`
  where `L: Lowering` lowers `SpiritOperation → Command` and
  `S: CommandExecutor` runs commands atomically against the redb
  store. Spirit's actor mesh becomes the *engine implementation
  detail* under `CommandExecutor::execute_atomic_batch`, not the
  request-routing top-level structure. The whole point of the
  framework is realized.

- **(b) Demote the framework**: Accept that spirit's actor mesh
  is the actual production pattern for persona components, and
  re-scope `signal-executor` to a thinner role (e.g., just the
  `Lowering`+`CommandExecutor` traits as type-system guidance with
  no concrete `Executor` struct). The `Executor` orchestrator is
  retired as unproven speculation.

Designer recommendation: **(a) migrate spirit onto the framework**.
The framework's design is sound (the library tests prove it). The
hand-rolled actor pipeline in spirit duplicates the framework's
orchestration logic (lowering → execute → reply). The migration
clarifies which logic belongs where: contract operations come in
through the framework; component-specific actor mesh is the
engine implementation under `CommandExecutor`. Without the
migration, every future component will be tempted to repeat
spirit's pattern (skip the framework, write request routing by
hand), and the framework becomes dead code.

### What the migration would look like

```rust
// In persona-spirit:
struct SpiritLowering { /* ... */ }
impl Lowering for SpiritLowering {
    type Operation = SpiritOperation;
    type Reply = SpiritReply;
    type Command = Command;             // already exists
    type ComponentEffect = Effect;      // already exists

    fn lower(&self, op: &SpiritOperation)
        -> Result<OperationPlan<Command>, SpiritReply>
    { Ok(OperationPlan::single(Command::from_request(op.clone()).unwrap())) }

    fn reply_from_effects(&self, op: &SpiritOperation, effects: &OperationEffects<Command, Effect>)
        -> SpiritReply
    { /* convert Effect back into SpiritReply variants */ }
}

struct SpiritCommandExecutor { /* wraps the Kameo actor runtime */ }
impl CommandExecutor for SpiritCommandExecutor {
    type Command = Command;
    type ComponentEffect = Effect;
    type Error = SpiritEngineError;

    fn execute_atomic_batch(&mut self, plan: BatchPlan<Command>)
        -> Result<BatchEffects<Command, Effect>, SpiritEngineError>
    { /* dispatch through the existing actor mesh; collect typed effects */ }
}

impl BatchErrorClassification for SpiritEngineError { /* ... */ }
```

The daemon's request entry point then becomes:

```rust
let mut executor = Executor::new(lowering, command_executor, observers);
let reply = executor.execute(request);
```

Spirit's existing actor mesh moves *inside* `CommandExecutor`. The
framework's domain-rejection / batch-abort / observer-publication
mechanics start working for real.

## 3 · Finding 2: contract-level smells in `signal-persona-spirit`

These are visible in the current `src/lib.rs` (verified read
against commits `a1909872` / `2e7a69a0`).

### 3.1 — Subscription reply triplication

Lines 433-438 of the macro declaration:

```rust
reply SpiritReply {
    ...
    StateSubscriptionOpened(StateSubscriptionOpened),
    RecordSubscriptionOpened(RecordSubscriptionOpened),
    SubscriptionOpened(SubscriptionOpened),
    StateSubscriptionRetracted(StateSubscriptionRetracted),
    RecordSubscriptionRetracted(RecordSubscriptionRetracted),
    SubscriptionRetracted(SubscriptionRetracted),
    ...
}
```

Six variants for two events ("subscription opened," "subscription
retracted"). The polymorphic `SubscriptionOpened { token:
SubscriptionToken, snapshot: SubscriptionSnapshot }` (lines 361-365)
already exists and covers both state and record subscriptions via
the typed sum.

This violates the *"lift repeated suffix"* discipline from
`intent/component-shape.nota` 2026-05-20T00:07:55+02:00 — the
psyche's correction on the repository-ledger pilot:

> *"the reply side still has the repeated-suffix smell. The request
> side lifted cleanly … replies stayed flat with five \*Listing
> siblings … By the repeated-category-words rule, the five \*Listing
> siblings want lifting the same way \*Query was lifted on the
> request side."*

Spirit has the same smell: keep `SubscriptionOpened` and
`SubscriptionRetracted` polymorphic; delete the four `State*` and
`Record*` siblings. The `Effect` enum in
`persona-spirit::observation` (12 variants → reduces to 8 after
the lift) gets the same simplification.

### 3.2 — Empty-marker payloads

Lines 205, 219, 222:

```rust
pub struct StateObservation {}
pub struct QuestionPending {}
pub struct StateSubscription {}
```

These are zero-field records used as wrapped payloads in
`Observation::State(StateObservation)`,
`Observation::Questions(QuestionPending)`,
`Subscription::State(StateSubscription)`. Two of the three
`Observation` variants and one of the two `Subscription` variants
carry empty payloads. The `Observation` enum could simply be:

```rust
pub enum Observation {
    State,                          // was Observation::State(StateObservation {})
    Records(RecordQuery),
    Questions,                       // was Observation::Questions(QuestionPending {})
}
```

The empty structs exist to fit the `NotaSum` derive's
positional-record assumption that every variant has a single record
payload. If `NotaSum` can handle unit variants, drop the empty
structs. If it can't, file a `nota-codec` follow-up — the variants
shouldn't have to invent empty records to satisfy a derive macro.

### 3.3 — `Statement { statement: StatementText }`

Line 188-191:

```rust
pub struct Statement {
    pub statement: StatementText,
}
```

The struct name and the field name repeat. ESSENCE.md §"Naming":
*"names don't carry their full ancestry"* — inside a struct called
`Statement`, the field shouldn't restate `statement`. Options:

```rust
pub struct Statement { pub text: StatementText }  // rename field
pub struct Statement(pub StatementText);          // tuple struct
```

The tuple struct is the simplest fit for a single-field newtype-
shaped record. Apply the same rule to other single-field records:
audit for `Foo { foo: X }` shapes across spirit's lib.

### 3.4 — `RequestUnimplemented` carries redundant operation

Lines 393-397:

```rust
pub struct RequestUnimplemented {
    pub operation: OperationKind,
    pub reason: UnimplementedReason,
}
```

The reply is positionally addressed — the caller knows which
operation index produced this reply. The `operation` field
restates information already in the request. Drop the field:

```rust
pub struct RequestUnimplemented {
    pub reason: UnimplementedReason,
}
```

### 3.5 — `OperationKind` enum lists Tap/Untap that aren't in the channel declaration

Lines 374-383 declare `OperationKind::Tap` and `Untap`, and the
`SpiritRequest::operation_kind()` match (lines 466-478) handles
them. But the `signal_channel!` macro declaration (lines 419-426)
only lists `State`, `Record`, `Observe`, `Watch`, `Unwatch` — no
explicit `Tap` or `Untap`.

The `observable` block (lines 452-456) tells the macro to inject
`Tap` and `Untap` operations + filter + observer events. So
`SpiritOperation::Tap(...)` and `SpiritOperation::Untap(...)` exist
post-expansion, and the OperationKind enum agrees with the
expanded surface.

This works but it's invisible. A reader of `signal-persona-spirit`
sees the contract declaration and a separate `OperationKind` enum
with variants the declaration doesn't show. The reader has to know
the macro injects observable verbs.

Fix candidates:

- The macro could generate `OperationKind` automatically from the
  expanded variant set (including injected Tap/Untap). Today
  `OperationKind` is hand-maintained and could drift if the
  injection changes.
- OR: document the injection rule loudly at the top of the
  contract file: *"The observable block injects Tap(ObserverFilter)
  and Untap(ObserverSubscriptionToken) operations; this contract's
  request surface is the declaration below plus those two."*

### 3.6 — Frame type aliases stripping the channel prefix

Lines 459-464:

```rust
pub type Frame = SpiritFrame;
pub type FrameBody = SpiritFrameBody;
pub type ChannelRequest = SpiritChannelRequest;
pub type ChannelReply = SpiritChannelReply;
pub type RequestBuilder = SpiritRequestBuilder;
pub type SpiritRequest = SpiritOperation;
```

These are stripping the `Spirit` prefix that the macro adds. The
macro adds the channel name as prefix because it can't see from
inside what crate it's in. The contract author then re-aliases to
the unprefixed name (which is the right shape per the
"no full ancestry" rule — inside `signal-persona-spirit`, the type
is `Frame`, not `SpiritFrame`).

This is a macro-level issue. The macro should let the contract
author specify the channel-name prefix, or default to no prefix
and let the author opt in. Today every contract has to repeat the
6-line alias block. Worth fixing in `signal-frame-macros`.

## 4 · Finding 3: introspection thinness

### What observers see

When a Tap subscriber receives an `OperationReceived` event, the
payload is:

```rust
pub struct OperationReceived {
    pub operation: OperationKind,    // 7-variant tag
}
```

When they receive an `EffectEmitted` event:

```rust
pub struct EffectEmitted {
    pub observation: SemaObservation,   // 6×7 payloadless classes
}
```

No record contents. No statement text. No entry summary.

### Why this is by design

The intent record on universal observation hooks
(`intent/component-shape.nota` 2026-05-19T20:00Z) framed Tap/Untap
as the **cross-component class-level monitoring** surface. Generic
introspection sees *that* an Assert happened, not *what* was
asserted. Component-specific richer data is in the domain Watch
stream (here: `StateChanged`, `RecordCaptured` events, with
typed payloads).

Two consumers, two streams:

- `persona-introspect` (cross-component): subscribes via Tap;
  sees universal Sema-class events; aggregates across components.
- Component-specific consumer (here: psyche introspection of
  intent records): subscribes via `Watch(Records)`; sees
  `RecordCaptured(RecordCaptured { record: RecordSummary })`
  with summary content.

### Where this gets thin for spirit

The substrate-replacement use case
(`intent/persona.nota` 2026-05-20T15:00:00Z — spirit CLI replaces
intent-log filesystem) implies psyche wants to *use* spirit as the
intent record. Reading-back records — *"what decisions have been
made this week?"* — goes through `Observe(Records)` (a one-shot
query, summary or provenance mode), not through the Tap stream.

That works. But if psyche-introspect ever wants to *push* intent
updates into a panel, the data flow goes through `Watch(Records)`
(domain stream, rich data) AND `Tap` (universal stream, classes
only) at the same time. The two streams are different shapes.
Persona-introspect either has to consume both, or settle for the
class-level view and treat record-contents as a lookup step.

This is a designer-call: confirm the two-stream split is
intentional and how cross-component introspect dashboards consume
the pair. Probably right; worth surfacing explicitly so future
agents don't try to fold the streams.

## 5 · Executor-level observations (when it IS used)

These are notes from the executor code that hold regardless of
the unused-framework finding.

### 5.1 — `Executor::execute` correctness

`signal-executor/src/executor.rs:56-122` correctly threads:

- `publish_operation_received` before lowering (line 61).
- Domain rejection → `operation_aborted_reply` with typed
  `SubReply::Failed.detail` (line 64-71).
- `BatchPlan` construction from non-empty operation plans
  (line 74-76).
- Engine failure → reads three classifications from
  `BatchErrorClassification`, stashes raw error, builds
  `batch_aborted_reply` (line 78-87).
- Per-effect observer publication (line 89-93).
- Reply construction with `SubReply::Ok` per operation
  (line 95-116).

All matches the spec. The assertion at line 97-101 enforces the
`CommandExecutor` contract that one `OperationEffects` returns per
input `OperationPlan`.

### 5.2 — `OperationFailureReason::DomainRejection` is the only variant

`signal-frame/src/reply.rs:185-192`:

```rust
pub enum OperationFailureReason {
    DomainRejection,
}
```

The enum is single-variant. Fine for now (every operation-level
abort under the current contract is domain-rejection), but the
enum-shape leaves room for future variants without restructuring
the wire reply. Designer note: keep the variant set tight; if a
new variant appears, it should be a real new shape, not a
sub-classifier of domain-rejection.

### 5.3 — `last_engine_error` stash pattern

The pattern (line 84) stashes the raw engine error on the
Executor for daemon-side retrieval via `take_last_engine_error()`.
Works for sequential request handling (one request at a time per
Executor instance). The daemon must take the error before the next
request, or the stash gets overwritten. Document this assumption
in signal-executor/ARCHITECTURE.md if not already.

### 5.4 — `BatchErrorClassification` ownership in signal-frame

Operator landed this in signal-frame
(`signal-frame::reply.rs:178-182`) rather than signal-executor —
the right call. The classification is wire-vocabulary
(`BatchFailureReason / RetryClassification / CommitStatus` all live
in signal-frame), so the trait that produces them belongs in the
same crate. Reusable beyond signal-executor if any other surface
needs to classify engine errors.

## 6 · Operator's four open questions

From /145 §"Current Open Questions":

### 6.1 — Existing intent files

**Settled by psyche** `intent/persona.nota` 2026-05-20T15:30:00Z:
*"importing existing nota files STAYS THE FUCK OUT OF SPIRIT - we
can make a dumb tool for a one-time import if we feel like it, but
we might just get an agent to re-log everything by hand. DO NOT
INTRODUCE IMPORT LOGIC IN SPIRIT!"*

Hard Constraint: persona-spirit's contract, daemon, and storage
must not contain any import-aware code path, special ingestion
mode, legacy-substrate vocabulary, or import-shaped contract verb.
Spirit handles typed records going forward; the legacy file
substrate is outside spirit's design surface entirely.

Acceptable paths for the existing `intent/*.nota` content (only if
psyche asks for migration at all):

- **Default**: agents re-log content by hand as it becomes
  relevant. No tooling, no batch migration.
- **Only if psyche explicitly asks**: a dumb one-time external
  tool that walks `intent/*.nota`, parses each record, and submits
  via the spirit CLI's normal `Record` operation — exactly like
  any agent doing manual re-log. The tool is spirit-external; it
  has no privileged surface, no special verb, no awareness inside
  spirit.

The earlier 4-phase-migration framing in this section was a
designer over-extension and is retired. The substrate question is
not "how do we phase a dual-substrate window" — it is "spirit does
not touch this; agents re-log by hand."

### 6.2 — Tap/Untap live before substrate replacement?

**Designer recommendation, awaiting psyche:** no. The
substrate-replacement use case is "agents record/query intent."
Both are one-shot operations (`Record(Entry)` /
`Observe(Records)`), not subscription operations. Tap/Untap is
the cross-component class-level monitoring surface — useful for
persona-introspect but not load-bearing for the substrate role.

Phase 2/3 of §6.1 can proceed before Tap/Untap delivers live
events. The current typed `NoChange` placeholder for Tap is
honest: the operation is accepted, no observer state is created,
no work is done.

Tap/Untap subscription event delivery becomes load-bearing when
persona-introspect starts running — separate arc.

### 6.3 — `signal-persona-orchestrate` migration timing

**Designer recommendation, takeable at designer level:** wait for
the orchestrate contract redesign. The persona-orchestrate
contract is mid-redesign per /233 + intent records on the
work-graph / role-claim split. Migrating its `SemaEffectEmitted`
naming now is churn for a surface that will rewrite shortly
anyway. Add a note to its ARCH that the rename is pending the
contract redesign; rename at the same time as the broader edit.

### 6.4 — `EffectEmitted` mandatory or default name?

**Designer recommendation, takeable at designer level:** mandatory
for the macro-injected observable block emitting class-level Sema
events; **default name** that contract authors can override only
when the event needs to carry richer-than-class payload. Spirit's
case (line 415) uses the default and embeds `SemaObservation` —
this is the canonical shape.

If a future contract needs richer per-component observer events,
it overrides the name (e.g., `LedgerEffectEvent` carrying typed
ledger detail). The default `EffectEmitted` + `SemaObservation`
payload is the workspace-uniform shape; overrides are
component-specific exceptions.

This is a designer-territory call unless psyche wants to weigh in.
Recommend documenting the default-vs-override pattern in
`skills/contract-repo.md` once spirit ships and the shape is
proven.

## 7 · Recommended actions

### Operator (next slice)

1. **Migrate persona-spirit onto signal-executor.** Implement
   `SpiritLowering` and `SpiritCommandExecutor`; wire the daemon
   entry point through `Executor::execute(request)`. The existing
   actor mesh becomes the engine implementation inside
   `CommandExecutor::execute_atomic_batch`. This is the load-
   bearing pilot the framework is waiting for.
2. **Clean the subscription-reply triplication in
   `signal-persona-spirit`.** Drop the four `State*` and
   `Record*` subscription-event variants; keep the polymorphic
   `SubscriptionOpened` and `SubscriptionRetracted`.
3. **Fix the empty-marker payloads, `Statement` field redundancy,
   and `RequestUnimplemented` operation field.** Small surgical
   edits.

### Designer follow-up

4. **`OperationKind` macro-generation.** Investigate having
   `signal-frame-macros` emit `OperationKind` automatically from
   the expanded operation set (including injected Tap/Untap).
   Avoids drift between hand-maintained enum and macro output.
5. **Frame type alias cleanup.** Decide whether
   `signal-frame-macros` should default to no channel-name prefix
   on emitted types, so contracts don't all need the 6-line alias
   block. Pre-pilot finalization.
6. **Two-stream introspection note.** Document the Tap/Watch
   split in `skills/contract-repo.md` or similar — cross-component
   class-level monitoring (Tap) versus component-specific richer
   data (Watch).

### Psyche calls needed

7. **Confirm §6.2 (Tap not blocking substrate replacement).**
   §6.1 is now settled by the no-import-logic-in-spirit Constraint
   (`intent/persona.nota` 2026-05-20T15:30:00Z).

## 8 · References

- `/144` (operator) — refresh implementation report.
- `/145` (operator) — current-state handoff.
- `/254` (designer) — earlier audit, before this code read.
- `/246-v4`, `/248`, `/253` — three-layer spec.
- `intent/component-shape.nota` — three-layer affirmation,
  no-op-as-command rule, EffectEmitted naming, repeated-suffix
  smell.
- `intent/persona.nota` 2026-05-20T15:00:00Z — spirit CLI replaces
  intent-log substrate.
- Code:
  `/git/github.com/LiGoldragon/signal-executor/src/`,
  `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs`,
  `/git/github.com/LiGoldragon/persona-spirit/src/{lib.rs, observation.rs, actors/dispatch.rs, actors/root.rs}`.

This report retires when (a) the spirit migration onto
signal-executor lands AND the contract smells in §3 are cleaned,
OR (b) a successor audit supersedes.
