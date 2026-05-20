# 256 — signal/sema/spirit post-fix audit (deep code read)

*Designer audit after operator landed the /255 high-signal fixes plus
several judgment-call changes not in /255. All /255 findings are
closed. One critical new gap surfaces from the side-changes: spirit's
`Timestamp(u64)` violates a Maximum-certainty Decision in
`intent/workspace.nota` 2026-05-19 18:30 that timestamps are two
positional fields. Three smaller follow-ups also surface.*

## 0 · TL;DR

**/255 closure verified** (all three findings):

| /255 finding | Status |
|---|---|
| F1 — signal-executor unused | **Closed**. `SpiritLowering` + `SpiritCommandExecutor` + `ObserverChannel` impls in `persona-spirit/src/actors/dispatch.rs`; daemon path routes through `Executor::execute(request).await`. |
| F2 — contract smells | **Closed**. Subscription triplication collapsed; empty markers replaced with unit-variant enums (NotaEnum mixed form, now workspace-supported per psyche); `Statement { text }`; `RequestUnimplemented` without redundant `operation`. |
| F3 — introspection thinness | Unchanged by design — awaits persona-introspect; the Tap/Watch split is the intentional shape. |

**One critical new gap, three smaller ones**:

1. **`Timestamp(u64)` violates the two-field-timestamp Decision**
   (`intent/workspace.nota` 2026-05-19 18:30). The intent specifies
   timestamps as **two positional NOTA fields** — a date field and a
   time field, both bare-friendly. Operator's String→u64 migration
   went in the wrong direction; the right shape is splitting into
   `Date` and `Time` as two fields on `Entry` (and `RecordProvenance`).
2. `SpiritCommandExecutor::execute_atomic_batch` rejects batches > 1
   AND, even for size 1, calls commands sequentially without any
   transaction boundary. The "atomic" promise of `execute_atomic_batch`
   is structurally unfulfilled. Honest under the current
   single-command-plan assumption; will break the contract the moment
   multi-command plans exist.
3. `SpiritLowering::reply_from_effects` returns the *last* component
   effect's reply. Fine for current 1:1 operation→command lowerings;
   fragile under future N-command plans (no signal of "which effect
   is canonical").
4. `SpiritObserverRecorder` constructs `OperationReceived` /
   `EffectEmitted` events and **discards** them (`let _event = …`).
   Only a trace witness is kept; no subscriber fanout. Honest
   placeholder while Tap subscribers don't exist, but the publisher
   side is not yet wired through `FrameObserverBridge`.

The Timestamp gap is **stop-the-world**: every `Entry` written to
spirit's store right now has a u64 single-field timestamp, which
means the substrate-replacement target (psyche logging intent via
`spirit '(Record ...)'`) cannot agree-by-shape with the existing
`intent/*.nota` two-field form. Fix this before spirit is used as
the substrate.

## 1 · /255 closure verification

### F1 — signal-executor is now used

`persona-spirit/Cargo.toml` adds `signal-executor`.
`persona-spirit/src/actors/dispatch.rs` constructs an
`Executor<SpiritLowering, SpiritCommandExecutor>` per request and
calls `.execute(request).await` (line 115-116):

```rust
let mut executor = Executor::new(SpiritLowering, command_executor, observers);
let reply = executor.execute(request).await;
```

`SpiritLowering: Lowering` (lines 158-185) maps SpiritRequest →
Command via `Command::from_request`, defaults to
`RequestUnimplemented` reply when `from_request` returns `None`.
`SpiritCommandExecutor: CommandExecutor` (lines 424-441) holds
actor refs to the existing Kameo mesh and runs commands through
them. `SpiritObserverRecorder: ObserverChannel` (lines 449-465)
publishes operation-received and effect-emitted events.

Verification tests in `tests/actor_runtime.rs` actively pin this:

```rust
#[test]
fn persona_spirit_dispatch_path_depends_on_signal_executor() {
    assert!(manifest.contains("signal-executor"));
    assert!(source.contains("signal_executor::"));
    assert!(source.contains("Executor::new"));
    assert!(source.contains(".execute(request).await"));
}
```

The architectural witness is real and won't drift silently.

### F2 — Contract smells fixed

`signal-persona-spirit/src/lib.rs`, verified by diff against
`a1909872` (prior state):

- **Subscription replies collapsed.** Lines 401-402 are now just
  `SubscriptionOpened(SubscriptionOpened)` and
  `SubscriptionRetracted(SubscriptionRetracted)`. The four typed
  `State*` / `Record*` variants are gone. Spirit's local `Effect`
  enum (`persona-spirit/src/observation.rs`) tracks the change.
- **Empty marker payloads gone.** `enum Observation` (lines 305-310)
  is now mixed unit/data:
  ```rust
  pub enum Observation { State, Records(RecordQuery), Questions }
  ```
  Same for `enum Subscription`. The `NotaEnum` derive now handles
  mixed unit/data variants per psyche's confirmation.
- **`Statement.text`.** Was `Statement { statement: StatementText }`;
  now `Statement { text: StatementText }`. Operator chose the
  field-rename option (vs tuple struct); fine.
- **`RequestUnimplemented` no longer carries `operation`.** Now just
  `{ reason: UnimplementedReason }`. Positional addressing supplies
  the operation identity.

### F3 — Introspection thinness

Unchanged by design. `OperationReceived` still carries
`OperationKind`; `EffectEmitted` still carries `SemaObservation`.
Per /255 §4, this is the intentional cross-component-class-only
shape, with rich data flowing through the `Watch` stream instead.
Persona-introspect will consume the class stream when it lands.

## 2 · Side-changes operator made (not requested in /255)

Two operator-judgment changes landed alongside the /255 fixes:

1. **`CommandExecutor::execute_atomic_batch` is now `async`**
   (signal-executor `7b0ca56a`). The trait uses RPIT for the
   future:
   ```rust
   fn execute_atomic_batch(&mut self, plan: BatchPlan<Self::Command>)
       -> impl Future<Output = Result<...>> + Send + '_;
   ```
   Required because spirit's actor-mesh `ask` calls are async.
   Correct call: the executor cannot promise sync execution if
   real engines are async. Designer endorses.
2. **`Timestamp: String → u64` whole-seconds**
   (signal-persona-spirit `060bef9a`, persona-spirit `8c300ae3`).
   See §3.1 — this one is wrong and needs to be undone in favor of
   the two-field shape.

## 3 · New gaps

### 3.1 — `Timestamp(u64)` violates the two-field-timestamp Decision (critical)

`intent/workspace.nota` 2026-05-19 18:30 (Maximum certainty):

> *"Timestamp in intent records is two positional fields, not one: a
> date field and a time field. Both bare-friendly in NOTA (the date is
> digits-and-hyphens; the time is digits-and-colon). The space between
> them is the NOTA positional separator, not a delimiter inside the
> value. Drops the T problem, drops the :00Z noise, and the visual
> reads as two clean fields."*

Psyche verbatim: *"why? that looks better. two fields, date then
time."*

Spirit's current shape (signal-persona-spirit/src/lib.rs:115-125 and
:200, :234):

```rust
pub struct Timestamp(u64);              // whole seconds since epoch

pub struct Entry {
    ...
    pub timestamp: Timestamp,             // single field
    ...
}
```

This is wrong twice:
- **Single field, not two.** The intent is explicit that timestamps
  are *two positional fields* on the parent record. Spirit packs
  date+time into one field.
- **Opaque u64, not bare-friendly NOTA forms.** The intent specifies
  digits-and-hyphens (date) and digits-and-colon (time). The
  agent-facing NOTA form should be readable: `2026-05-20 14:30:30`.
  Operator's u64 means the agent writes `... 1779000000 ...` —
  opaque, non-bare-friendly, and the wrong shape.

This is the *agent-facing* substrate. If spirit replaces
`intent/*.nota` files (per the substrate intent), every record an
agent writes must align with the existing convention. The existing
`intent/*.nota` records already use the two-field form — e.g.,
`intent/workspace.nota:208` ends with `2026-05-19 18:30)`.

Right shape:

```rust
pub struct Date { ... }       // bare-friendly digits-and-hyphens
pub struct Time { ... }       // bare-friendly digits-and-colon

pub struct Entry {
    pub topic: Topic,
    pub kind: Kind,
    pub summary: Summary,
    pub context: Context,
    pub certainty: Certainty,
    pub date: Date,            // <-- two positional fields
    pub time: Time,
    pub quote: Quote,
}
```

(Field order TBD — current order has timestamp before quote, which
matches the two-field expansion.)

`Date` and `Time` should be typed records with NOTA codec support
for the bare digit-and-hyphen / digit-and-colon forms. Whether the
inner representation is `(u16 year, u8 month, u8 day)` etc. is an
implementation detail; the wire and CLI form is the bare-friendly
sequence the psyche specified.

The same fix applies to `RecordProvenance` (line 234 of
signal-persona-spirit/src/lib.rs).

**Operator must fix this before spirit is used as a substrate.**
Existing tests in `tests/daemon.rs` use `Timestamp::new(1_779_000_000)`
— those need to update to the new shape.

### 3.2 — `execute_atomic_batch` is not actually atomic

`persona-spirit/src/actors/dispatch.rs:429-441`:

```rust
async fn execute_atomic_batch(
    &mut self,
    plan: BatchPlan<Self::Command>,
) -> Result<BatchEffects<Self::Command, Self::ComponentEffect>> {
    let operation_count = plan.operations().len();
    if operation_count != 1 {
        return Err(Error::UnsupportedAtomicBatch { operation_count });
    }
    let operation = plan.into_operations().into_head();
    let effects = self.execute_operation_plan(operation).await?;
    Ok(BatchEffects::single(effects))
}
```

Two problems:

- **Multi-operation rejection**. The implementation rejects batches
  > 1 with `Error::UnsupportedAtomicBatch`. The framework was
  designed to handle multi-operation atomic commits; spirit
  declares it cannot do that yet.
- **No transaction boundary even for size 1.** `execute_operation_plan`
  loops through commands and calls `execute_command(command).await`
  for each (lines 206-218). Each command is an actor `ask` — its
  own request to a Kameo actor that writes to redb. If command 2
  fails after command 1 commits, command 1 is NOT rolled back. The
  trait's name promises atomicity; the implementation provides
  best-effort sequential execution.

Today this is hidden because every spirit operation lowers to
exactly one command (lowering's `OperationPlan::single(...)`). The
atomicity question doesn't surface until an operation needs
multi-command plans. But the trait contract is structurally
violated; an honest implementation either:

- Wraps the whole `execute_operation_plan` in a redb write
  transaction so failure-mid-plan rolls back, or
- Renames `execute_atomic_batch` to `execute_sequential_batch` and
  weakens the framework's promise.

The first is correct; the framework should keep its name. Operator
needs to either implement transactional execution at the
`CommandExecutor` boundary, OR explicitly document that spirit's
implementation is degenerate-atomic (one command per plan, one
plan per batch) and any future multi-command lowering is an
architectural change requiring new transactional plumbing.

This is a **design gap** that doesn't currently bite but will the
moment spirit grows a multi-command operation (e.g., a single
"classify and record" operation that lowers to
`[ClassifyStatement, AssertEntry]` instead of routing through a
classifier actor).

### 3.3 — `reply_from_effects` "last" heuristic

`SpiritLowering::reply_from_effects` (dispatch.rs:173-184):

```rust
fn reply_from_effects(
    &self,
    _operation: &Self::Operation,
    effects: &OperationEffects<Command, Effect>,
) -> SpiritReply {
    effects
        .component_effects()
        .last()
        .expect("persona-spirit operation effects are non-empty")
        .clone()
        .into_reply()
}
```

The "last" picks the *last* component effect's reply. Fine for the
current 1:1 case (one command, one effect, the "last" IS the
"only"). Fragile for the multi-command case (same as §3.2): if a
future operation lowers to `[Classify, Assert]` and both produce
effects, "last" returns the Assert reply. That might be right, but
the choice is implicit. No principled signal of *which* effect is
canonical when multiple exist.

Recommendation: as soon as spirit has any multi-command operation,
make this explicit. Options:

- Add a designator to the `Command` enum: `Command::Final(Inner)` /
  `Command::Auxiliary(Inner)`, lowering returns one final + N
  auxiliary. `reply_from_effects` picks the Final's effect.
- Have lowering carry an "effect index" alongside the plan:
  `OperationPlan { commands: NonEmpty<Command>, canonical_index:
  usize }`. The executor exposes the effect at that index.
- Continue with "last" as a documented convention, on the
  assumption that pipeline order matters (the deepest write is
  canonical).

The third is the simplest and matches operator's intuition. If
that's the workspace rule, document it on the `Lowering` trait so
future implementers don't guess.

### 3.4 — Observer publisher is a trace-only placeholder

`SpiritObserverRecorder` (dispatch.rs:443-465):

```rust
impl ObserverChannel<SpiritRequest, CommandEffect<Command, Effect>> for SpiritObserverRecorder {
    fn publish_operation_received(&self, operation: &SpiritRequest) {
        let _event = OperationReceived { operation: operation.operation_kind() };
        self.trace.record(TraceNode::SIGNAL_EXECUTOR, TraceAction::OperationReceived);
    }

    fn publish_effect_emitted(&self, effect: &CommandEffect<Command, Effect>) {
        let _event = EffectEmitted { observation: effect.sema_observation() };
        self.trace.record(TraceNode::SEMA_OBSERVER, TraceAction::ObservationProjected);
    }
}
```

The `let _event = ...` construction is a placeholder — the event
record is built and immediately dropped. The trace records the
*moment* of publication; the event payload goes nowhere. There is
no `FrameObserverBridge` constructed, no `ObservableSet` fanout, no
subscriber socket delivery.

Honest under the current state (Tap returns RequestUnimplemented,
so no subscribers exist). When Tap subscriptions become live, this
placeholder must be replaced with a real bridge:

```rust
let observer = FrameObserverBridge::new(spirit_projection, observer_set, delivery);
let observers = ObserverSet::new(observer);
```

The bridge composes `signal_frame::ObservationProjection` (spirit-
side projection from raw to event records),
`signal_frame::ObservableSet` (macro-generated `SpiritObserverSet`,
filter+token bookkeeping), and an `ObserverDelivery` impl that
writes to subscriber sockets.

Operator note in `tests/actor_runtime.rs` (witness tests) does not
yet test fanout; that's the next slice.

## 4 · /255 follow-ups still open

Tracking against /255 §7:

| /255 item | Status |
|---|---|
| 1. Spirit on signal-executor | Closed |
| 2. Subscription collapse | Closed |
| 3. Empty markers / Statement / RequestUnimplemented | Closed |
| 4. OperationKind macro generation | Not done (designer) |
| 5. Frame type alias cleanup | Not done (designer) |
| 6. Two-stream introspection skill note | Not done (designer) |
| §6.1 — intent-file import phasing | Settled by `intent/persona.nota` 2026-05-20T15:30:00Z (no import logic in spirit) |
| §6.2 — Tap blocking substrate replacement | Still open for psyche |
| §6.3 — orchestrate migration timing | Designer answer in /255 |
| §6.4 — EffectEmitted mandatory/default | Designer answer in /255 |

## 5 · Recommended next slice for operator

In priority order:

1. **Fix the Timestamp shape** per §3.1. This is stop-the-world for
   the substrate-replacement target. Two positional fields (`date`,
   `time`); bare-friendly NOTA values; typed `Date` and `Time`
   records. Both `Entry` and `RecordProvenance` get the split.
   Tests update from `Timestamp::new(1_779_000_000)` to
   `Date::new(...)`, `Time::new(...)`.
2. **Document the `execute_atomic_batch` atomicity discipline**
   (§3.2). Either implement transactional execution at the
   `CommandExecutor` boundary, or document that spirit's current
   implementation is degenerate-atomic (1 op = 1 command = atomic
   by single-effect identity). The framework's name promises
   atomicity; the docs must match.
3. **Document or fix the `reply_from_effects` "last" heuristic**
   (§3.3). Designer lean: document as a convention on the `Lowering`
   trait — pipeline-order canonical, last command's effect is the
   reply.
4. **Defer observer-fanout wiring until Tap subscribers exist**
   (§3.4). Honest placeholder is acceptable until then. When Tap
   goes live: replace `SpiritObserverRecorder` with
   `FrameObserverBridge` composition.

## 6 · Psyche call still pending

From /255 §6.2 — does Tap/Untap need to be live before spirit
becomes the substrate?

Designer recommendation: **no** (Record/Query are one-shot, not
subscription; substrate replacement doesn't depend on live
fanout). The current typed-NoChange placeholder for Tap is honest
until persona-introspect comes online.

If you want a different answer, surface it; otherwise we'll
proceed on the recommendation when the substrate cutover question
is next on the table.

## 7 · References

- `/144`, `/145` — operator implementation + handoff reports.
- `/255` — prior designer audit.
- `intent/workspace.nota` 2026-05-19 18:30 — **two-field timestamp
  Decision** (the critical reference for §3.1).
- `intent/persona.nota` 2026-05-20T15:00:00Z — three-layer
  affirmation, BatchErrorClassification, no-op-as-command,
  EffectEmitted naming.
- `intent/persona.nota` 2026-05-20T15:30:00Z — no import logic in
  spirit.
- Code under audit:
  - `signal-executor/src/{engine,executor,lowering,observer,bridge}.rs`
  - `signal-frame/src/reply.rs` (BatchErrorClassification,
    CommitStatus).
  - `signal-persona-spirit/src/lib.rs` (current contract).
  - `persona-spirit/src/{observation.rs, actors/dispatch.rs,
    error.rs, lib.rs}`.

This report retires when (a) the Timestamp shape is fixed AND the
three smaller gaps are addressed (or documented), OR (b) a
successor audit supersedes.
