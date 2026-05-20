# 246 — Bundled fix design for the /244 holes, with examples

*Deep design report combining the alternatives from `/245` with
the operator's corrections in `/140`. Covers each of the five
holes from `/244` with the final shape, mechanical justification,
and a worked example. Plus the bigger-rethinks all settled. This
is the implementation-ready spec for the bundled fix — the next
designer/operator pair can read this and write code from it.*

## 0 · TL;DR

Five holes, five fixes:

| Hole | Final shape |
|---|---|
| 1 (typed rejection on wire) | `lower()` returns `Result<Vec<SemaOperation>, Self::Reply>`; executor encodes the Err as `Reply::Accepted` with `AcceptedOutcome::Aborted`, multi-op per-operation slots become `Invalidated` / `Failed { detail }` / `Skipped`. Kernel `Reply::Rejected` narrows to true frame-level failures only. |
| 2 (`Observe` verb collision) | `observable { open <Verb>(Filter); close <Verb>; … }`. Contract author names the open/close verbs; macro auto-emits the close-op's token payload type. |
| 3 (publish-bridge) | Crate-boundary projection separated as its own concern. `signal-frame` owns observer subscription/fanout; `signal-executor` owns execution facts (`Operation`, `SemaEffect`) AND defines a small `ObservationProjection` trait + `FrameObserverBridge<Projection, ObserverSet, Deliver>` struct that wires the pieces. Daemons that don't observe don't impl `ObservationProjection`. Macro-generated `<Channel>ObservationProjection` trait alias gives compile-time check against the contract's `observable { operation_event … effect_event … }` declarations. (Revised 2026-05-20 after `/141` analysis: projection is its own concern, not a method on `Lowering`.) |
| 4 (filter-match impl trust) | `observable { … filter default; … }` triggers macro-generated closed-enum `ObserverFilter` with sensible variants (`All` / `OnlyOperations { kinds }` / `OnlySemaEffects { classes }`) and the auto-impl of the filter-match trait. Contract authors opt out (`filter <CustomType>;`) only when the defaults don't fit. |
| 5 (worked example) | Complete the `signal-repository-ledger` + `repository-ledger` pilot as the canonical Phase-3 reference — adopt the observable block, write the daemon `Lowering` impl, add one end-to-end observer-subscribe test. |

Work order: 1 → 2 → 4 → (design pass on 3) → 3 → 5.

## 1 · Hole 1 — Lowering returns the contract reply on rejection

### The shape

`Lowering` trait surface:

```rust
pub trait Lowering {
    type Operation: RequestPayload;
    type Reply;
    type EngineError;

    /// Lower one contract operation into the Sema operations it
    /// produces. On Err, the contract reply IS the rejection
    /// detail; the executor stops further lowering and produces
    /// an Aborted outcome.
    fn lower(
        &self,
        operation: &Self::Operation,
    ) -> Result<Vec<SemaOperation>, Self::Reply>;

    /// Build the per-op success reply from the Sema effects that
    /// were committed.
    fn reply_from_effects(
        &self,
        operation: &Self::Operation,
        effects: &[SemaEffect],
    ) -> Self::Reply;
}
```

Three associated types (down from four — `RejectionReason` is
gone). One Err-on-failure return shape.

### The `Reply` / `SubReply` extensions

`signal-frame::Reply<ReplyPayload>` grows an `AcceptedOutcome`:

```rust
pub enum Reply<ReplyPayload> {
    Accepted {
        outcome: AcceptedOutcome,
        per_operation: Vec<SubReply<ReplyPayload>>,
    },
    Rejected {
        reason: RequestRejectionReason,  // narrowed to true kernel failures
    },
}

pub enum AcceptedOutcome {
    Committed,
    Aborted {
        failed_at: usize,                       // op index that failed
        reason: OperationFailureReason,
    },
}

pub enum SubReply<ReplyPayload> {
    Ok(ReplyPayload),
    Invalidated,                                // earlier op; would have committed; rolled back
    Failed {
        reason: OperationFailureReason,
        detail: Option<ReplyPayload>,           // ← typed contract reply lives here
    },
    Skipped,                                    // later op; never executed
}

pub enum OperationFailureReason {
    DomainRejection,                            // Lowering returned Err
    EngineRejection,                            // SemaEngine returned Err
}
```

Kernel `Reply::Rejected { reason: Internal }` is reserved for
true frame-level failures (parse error, version skew). Domain
rejections never appear there.

### Executor::execute under the new shape

```rust
pub fn execute(
    &mut self,
    request: Request<L::Operation>,
) -> Reply<L::Reply> {
    let payloads: &NonEmpty<L::Operation> = request.payloads();
    let mut sema_ops: Vec<SemaOperation> = Vec::new();
    let mut sema_op_owners: Vec<usize> = Vec::new();  // op index for each sema op

    // 1. Lower every op. On the first Err, build the Aborted outcome
    //    with per-op slots: Invalidated for earlier, Failed for the
    //    failing op, Skipped for later.
    for (op_index, op) in payloads.iter().enumerate() {
        self.observers.publish_operation_received(op);
        match self.lowering.lower(op) {
            Ok(ops) => {
                sema_op_owners.extend(std::iter::repeat(op_index).take(ops.len()));
                sema_ops.extend(ops);
            }
            Err(contract_reply) => {
                let per_operation = build_aborted_replies(
                    payloads.len(),
                    op_index,
                    contract_reply,
                    OperationFailureReason::DomainRejection,
                );
                return Reply::Accepted {
                    outcome: AcceptedOutcome::Aborted {
                        failed_at: op_index,
                        reason: OperationFailureReason::DomainRejection,
                    },
                    per_operation,
                };
            }
        }
    }

    // 2. Atomic execute.
    let effects = match self.sema_engine.execute_atomic(sema_ops) {
        Ok(effects) => effects,
        Err(engine_error) => {
            // Engine rejection is an infrastructure failure, not a
            // contract-domain reply. It stays kernel-shaped — the typed
            // engine error remains daemon-side (logs + ExecutorOutcome);
            // the wire reply is just kernel rejection.
            //
            // (Revised 2026-05-20 per /141: engine errors don't belong
            // in Reply::Accepted; they're not a per-op domain outcome.)
            return Reply::Rejected {
                reason: RequestRejectionReason::Internal,
            };
        }
    };

    // 3. Publish Sema effects to observers.
    for effect in &effects {
        self.observers.publish_sema_effect_emitted(effect);
    }

    // 4. Per-op success replies from effects, filtered by ownership.
    let per_operation: Vec<SubReply<L::Reply>> = payloads.iter().enumerate()
        .map(|(op_index, op)| {
            let op_effects: Vec<&SemaEffect> = sema_op_owners.iter()
                .zip(&effects)
                .filter_map(|(&owner, effect)| if owner == op_index { Some(effect) } else { None })
                .collect();
            SubReply::Ok(self.lowering.reply_from_effects(op, &op_effects))
        })
        .collect();

    Reply::Accepted {
        outcome: AcceptedOutcome::Committed,
        per_operation,
    }
}
```

Note the implicit ownership tracking — `sema_op_owners` maps each
Sema operation back to the request op that produced it. This
closes hole 13 from `/242` (implicit positional correlation) by
making correlation explicit and typed.

### Worked example — spirit, 3-op request with middle rejection

Inbound:

```nota
[(State first-statement)
 (State bad-statement-policy-violation)
 (Record entry-3)]
```

Lowering trace:

- `lower(State(first-statement))` → `Ok([SemaOperation::Assert(...)])`. `sema_ops = [Assert-first]`, `sema_op_owners = [0]`.
- `lower(State(bad-statement))` → `Err(SpiritReply::StateRejected(StateRejectionReason::PolicyDenied))`.
- Executor stops; builds Aborted reply.

Outbound:

```
Reply::Accepted {
    outcome: AcceptedOutcome::Aborted {
        failed_at: 1,
        reason: OperationFailureReason::DomainRejection,
    },
    per_operation: [
        SubReply::Invalidated,                            // op 0 — would have committed; rolled back
        SubReply::Failed {
            reason: OperationFailureReason::DomainRejection,
            detail: Some(SpiritReply::StateRejected(
                StateRejectionReason::PolicyDenied,
            )),
        },
        SubReply::Skipped,                                // op 2 — never executed
    ],
}
```

NOTA wire form:

```nota
(Accepted
    (Aborted 1 DomainRejection)
    [Invalidated
     (Failed DomainRejection (Some (StateRejected PolicyDenied)))
     Skipped])
```

The caller knows exactly which op failed, why (`PolicyDenied`),
and that ops 0 and 2 weren't committed.

### Documentation update on `SubReply::Invalidated`

`signal-frame`'s current `SubReply::Invalidated` doc leans
toward *"operation ran but its result is no longer
authoritative"* (per `/141` reading). Under this design, the
variant also covers *"operation was planned and lowered but
invalidated before commit because a sibling op rejected the
request."* Widen the doc to cover both cases, or introduce a
more precise variant if the wording feels too elastic.

## 2 · Hole 2 — Author-named observable verbs

### The shape

The observable block accepts contract-authored open/close verbs:

```rust
observable {
    open <OpenVerb>(<FilterType>);
    close <CloseVerb>;
    filter <FilterType>;                  // or `filter default;` (hole 4)
    event <EventType>;
    event <EventType>;
    // … more events …
}
```

Three things the macro auto-emits when this block is present:

1. `operation <OpenVerb>(<FilterType>) opens <Channel>ObserverStream`
2. `operation <CloseVerb>(<Channel>ObserverSubscriptionToken)` — close payload type is macro-determined; the contract author writes `close <Verb>;` with no payload
3. The `<Channel>ObserverStream` block with all declared events; the `<Channel>ObserverFilterMatch` trait; the `<Channel>ObserverSet`; the publish closures

### Worked example — spirit with Watch/Unwatch

Spirit's channel declaration:

```rust
signal_channel! {
    channel Spirit {
        operation State(Statement),
        operation Record(Entry),
        operation Observe(Selection),         // contract-author's own read verb — no collision
        operation Watch(Subscription) opens RecordStream,
        operation Unwatch(RecordSubscriptionToken),
        operation Query(Selection),
        // ...
    }
    reply SpiritReply { ... }
    observable {
        open Tap(SpiritObserverFilter);       // ← author picks Tap to avoid collision with Watch
        close Untap;
        filter default;                        // ← hole 4 — uses macro-generated standard filter
        event OperationReceived;
        event SemaEffectEmitted;
    }
}
```

The macro injects:

```rust
operation Tap(SpiritObserverFilter) opens SpiritObserverStream
operation Untap(SpiritObserverSubscriptionToken)

stream SpiritObserverStream {
    token SpiritObserverSubscriptionToken;
    opened SpiritObserverSubscriptionOpened;
    event OperationReceived;
    event SemaEffectEmitted;
    close SpiritObserverSubscriptionToken;
}
```

No collision with the contract's own `Observe(Selection)` or
`Watch(Subscription)` operations. The contract author chose
`Tap` for the debug-stream verb because the natural names were
taken by domain operations.

For a contract without those collisions, the typical choice is
`Watch`/`Unwatch`:

```rust
observable {
    open Watch(LedgerObserverFilter);
    close Unwatch;
    filter default;
    event OperationReceived;
    event SemaEffectEmitted;
}
```

Each contract picks the verbs that fit its domain. Cross-contract
reuse is fine; the receiver determines the effect per the
contract-locality principle (`intent/component-shape.nota`
2026-05-19T19:45Z).

## 3 · Hole 3 — Projection bridge across crate boundary

### The crate boundary problem

`signal-frame` cannot reference `signal_executor::SemaEffect` —
that would reverse the dependency (signal-executor → signal-frame
is the right direction; reversing creates a cycle).

But the macro in `signal-frame` generates publish closures that
take **channel-specific event records** (`OperationReceived`,
`SemaEffectEmitted`). The executor publishes **raw execution
facts** (`Operation`, `SemaEffect`).

Something has to project raw facts → channel event records. The
projection is contract-specific (each contract knows how its
`OperationReceived` is constructed from its `Operation`).

### The shape — separate projection trait + bridge struct

**(Revised 2026-05-20 after `/141` analysis: projection is its
own concern, not a method on `Lowering`. Daemons that don't
observe don't impl it. Lowering stays focused on execution.)**

Three pieces in three crates:

1. **`signal-executor`** defines a small `ObservationProjection`
   trait — execution facts in, channel event records out:

   ```rust
   pub trait ObservationProjection {
       type Operation;
       type OperationEvent;
       type EffectEvent;

       fn operation_event(&self, operation: &Self::Operation) -> Self::OperationEvent;
       fn effect_event(&self, effect: &SemaEffect) -> Self::EffectEvent;
   }
   ```

2. **`signal-executor`** also defines a generic bridge struct
   that wires the executor's `ObserverChannel<Operation>`
   contract to the macro-generated `<Channel>ObserverSet`'s
   publish closures + the daemon's delivery callback:

   ```rust
   pub struct FrameObserverBridge<Projection, ObserverSet, Deliver> {
       projection: Projection,
       observer_set: ObserverSet,
       deliver: Deliver,
   }

   impl<Projection, ObserverSet, Deliver, Operation> ObserverChannel<Operation>
       for FrameObserverBridge<Projection, ObserverSet, Deliver>
   where
       Projection: ObservationProjection<Operation = Operation>,
       ObserverSet: ObservableSet<
           OperationEvent = Projection::OperationEvent,
           EffectEvent = Projection::EffectEvent,
       >,
       Deliver: ObserverDelivery<
           OperationEvent = Projection::OperationEvent,
           EffectEvent = Projection::EffectEvent,
       >,
   {
       fn publish_operation_received(&self, operation: &Operation) {
           let event = self.projection.operation_event(operation);
           self.observer_set.publish_operation_received(&event, |token, e| {
               self.deliver.deliver_operation(token, e);
           });
       }

       fn publish_sema_effect_emitted(&self, effect: &SemaEffect) {
           let event = self.projection.effect_event(effect);
           self.observer_set.publish_sema_effect_emitted(&event, |token, e| {
               self.deliver.deliver_effect(token, e);
           });
       }
   }
   ```

   `ObservableSet` is a small trait `signal-executor` defines
   that the macro-emitted `<Channel>ObserverSet` types impl —
   abstract enough that signal-executor doesn't need to know
   the channel.

3. **The contract crate** owns the channel event record types
   (`OperationReceived`, `SemaEffectEmitted`, filter type),
   declared via the macro's `observable` block grammar (which
   `/141` refines to distinguish event roles):

   ```rust
   observable {
       open Watch(ObserverFilter);
       close Unwatch;
       filter ObserverFilter;
       operation_event OperationReceived;
       effect_event SemaEffectEmitted;
   }
   ```

   The `operation_event` and `effect_event` grammar (replacing
   the generic `event`) tells the macro which event record
   maps to which publication moment.

### Why this is more elegant than folding projection into Lowering

`Lowering` is about **execution** (contract op → Sema ops →
contract reply). `ObservationProjection` is about
**observation** (contract op + Sema effect → channel event
records). Same daemon implements both when it observes;
daemons that don't observe don't impl `ObservationProjection`
at all and don't pay the associated-type cost on `Lowering`.

The two concerns share no information beyond the contract
operation type. Coupling them in one trait widens `Lowering`
for daemons that don't need it. The `/141` analysis is right:
**these are separate concerns and they should have separate
traits.**

The compile-time check `/246`'s earlier draft proposed
(macro-generated `<Channel>Lowering` trait alias) translates
cleanly to a `<Channel>ObservationProjection` trait alias —
same mechanism, separate trait:

```rust
// Macro-generated from `channel Spirit { … observable { operation_event OperationReceived; effect_event SemaEffectEmitted; } }`:
pub trait SpiritObservationProjection: ObservationProjection<
    Operation = SpiritOperation,
    OperationEvent = OperationReceived,
    EffectEvent = SemaEffectEmitted,
> {}

impl<T> SpiritObservationProjection for T where T: ObservationProjection<
    Operation = SpiritOperation,
    OperationEvent = OperationReceived,
    EffectEvent = SemaEffectEmitted,
> {}
```

### Worked example — spirit's daemon

```rust
struct SpiritDaemonLowering {
    psyche_policy: PsychePolicy,
    statement_classifier: StatementClassifier,
    // …
}

impl Lowering for SpiritDaemonLowering {
    type Operation = SpiritOperation;
    type Reply = SpiritReply;

    fn lower(&self, op: &SpiritOperation) -> Result<Vec<SemaOperation>, SpiritReply> {
        match op {
            SpiritOperation::State(statement) => {
                if !self.psyche_policy.accepts(statement) {
                    return Err(SpiritReply::StateRejected(
                        StateRejectionReason::PolicyDenied,
                    ));
                }
                let entry = self.statement_classifier.classify(statement)?;
                Ok(vec![SemaOperation::Assert(entry.into_typed_record())])
            }
            // ...
        }
    }

    fn reply_from_effects(&self, op: &SpiritOperation, effects: &[SemaEffect]) -> SpiritReply {
        match op {
            SpiritOperation::State(_) => SpiritReply::Stated(
                StatementCaptured::from_effects(effects),
            ),
            // ...
        }
    }
}

// Separate impl for observability — daemon opts in only when it wants observers.
struct SpiritProjection {
    timestamp_source: TimestampSource,
}

impl ObservationProjection for SpiritProjection {
    type Operation = SpiritOperation;
    type OperationEvent = OperationReceived;
    type EffectEvent = SemaEffectEmitted;

    fn operation_event(&self, op: &SpiritOperation) -> OperationReceived {
        OperationReceived::new(op.kind(), self.timestamp_source.now())
    }

    fn effect_event(&self, effect: &SemaEffect) -> SemaEffectEmitted {
        SemaEffectEmitted::new(effect.operation_class(), effect.outcome().clone())
    }
}
```

The daemon wires it together at construction:

```rust
let observer_bridge = FrameObserverBridge::new(
    SpiritProjection { timestamp_source },
    SpiritObserverSet::new(),  // macro-generated
    spirit_observer_delivery,
);
let executor = Executor::new(SpiritDaemonLowering::new(...), sema_engine, observer_bridge);
```

The compile-time check fires if the `SpiritProjection`'s
associated types don't match the contract's `observable`
declarations.

### Why this isn't /245's "move ObserverChannel to signal-frame"

`/245`'s proposal: move the `ObserverChannel` trait to
signal-frame; the macro emits the impl. `/141` caught the
mechanical problem: the trait would reference
`signal_executor::SemaEffect`, which lives downstream of
signal-frame — backwards dependency.

This revision: `signal-executor` keeps both the
`ObserverChannel` trait AND the new `ObservationProjection`
trait AND the `FrameObserverBridge` struct. The macro-emitted
`<Channel>ObserverSet` impl an `ObservableSet` interface
that signal-executor's bridge composes over. No reverse
dependency.

## 4 · Hole 4 — Default observer filter

### The grammar

```rust
observable {
    open <OpenVerb>(<FilterType>);
    close <CloseVerb>;
    filter default;                       // ← macro generates the filter type + impl
    event <EventType>;
    event <EventType>;
}
```

When `filter default;` appears, the macro generates:

```rust
pub enum ObserverFilter {
    All,
    OnlyOperations { kinds: Vec<<Channel>OperationKind> },
    OnlyEvents { event_kinds: Vec<ObserverEventKind> },
}

pub enum ObserverEventKind {
    OperationReceived,
    SemaEffectEmitted,
    // ... one per declared event ...
}

impl <Channel>ObserverFilterMatch for ObserverFilter {
    fn matches_operation_received(&self, event: &OperationReceived) -> bool {
        match self {
            Self::All => true,
            Self::OnlyOperations { kinds } => kinds.contains(&event.operation_kind()),
            Self::OnlyEvents { event_kinds } => event_kinds.contains(&ObserverEventKind::OperationReceived),
        }
    }
    fn matches_sema_effect_emitted(&self, event: &SemaEffectEmitted) -> bool { /* parallel */ }
}
```

A contract author who needs a custom predicate writes
`filter <CustomType>;` instead and provides the impl. Most
contracts use `default`.

### Worked example — spirit subscribing only to State operations

```rust
// Subscriber side
let filter = ObserverFilter::OnlyOperations {
    kinds: vec![SpiritOperationKind::State],
};
let subscription = spirit_client.tap(filter).await?;
while let Some(event) = subscription.next().await {
    // Only OperationReceived events for State ops; nothing else
    println!("psyche stated: {:?}", event);
}
```

The macro's filter-match generated impl filters server-side; the
subscriber only receives matching events. No subscriber-side
filtering needed for the common case.

## 5 · Hole 5 — Pilot as worked example

### The path

`signal-repository-ledger` already has the request/reply lifted
shape from `/124` (`operation Query(Query)`,
`reply Reply { QueryResult(QueryResult), … }`). Three remaining
steps to make it the canonical example:

1. **Add the observable block to signal-repository-ledger**:
   ```rust
   observable {
       open Watch(ObserverFilter);
       close Unwatch;
       filter default;
       event OperationReceived;
       event SemaEffectEmitted;
   }
   ```
2. **Implement `Lowering` for the repository-ledger daemon**:
   - `lower(Receive(...))` → `Assert(EventRecord)` (single Sema op).
   - `lower(Observe(...))` → `Assert(EventRecord)` (single Sema op).
   - `lower(Query(Query::RecentRepositories(...)))` → `Match(RecentRepositoryReadPlan)`.
   - etc.
3. **Add the end-to-end observer test**:
   ```rust
   #[test]
   fn observer_sees_receive_and_resulting_effect() -> Result<()> {
       let mut daemon = LedgerDaemon::start(test_engine())?;
       let mut observer = daemon.client().tap(ObserverFilter::All).await?;
       
       let receipt = daemon.client().receive(hook_notification_payload).await?;
       
       // Observer sees the OperationReceived first, then SemaEffectEmitted.
       let event_1 = observer.next().await?;
       assert_matches!(event_1, ObserverEvent::OperationReceived(_));
       let event_2 = observer.next().await?;
       assert_matches!(event_2, ObserverEvent::SemaEffectEmitted(_));
       
       // The receipt carries the typed contract reply.
       assert_matches!(receipt, SubReply::Ok(LedgerReply::Received(_)));
       Ok(())
   }
   ```

That test exercises every layer of the stack. Phase-3
components (signal-persona-spirit first) follow this pattern.

### What the example demonstrates

- Contract with `observable` block.
- Daemon implementing `Lowering` with all five new associated
  types.
- Executor wired into the daemon's socket loop.
- Observer subscription via the contract-named `Watch` (or
  `Tap`) verb.
- Event flow through the macro-generated publish closures.
- Typed contract reply on success.
- (If a Reject test is added) typed contract reply on
  domain rejection.

## 6 · Bigger rethinks — all settled

Per `/245` §6 and `/140` "Bigger Rethinks", four moves are
considered and declined for now:

| Rethink | Verdict | Reason |
|---|---|---|
| Universal observability (always-on) | Decline — keep opt-in | Small/leaf daemons shouldn't carry observer bookkeeping; bar for opting in should be low |
| Executor in the macro | Decline — keep `signal-executor` separate | Macro is already large; executor is runtime orchestration, not vocabulary emission |
| Drop kernel `Reply` | Decline — keep it, narrow it | Kernel needs a cross-contract shape for frame-level failures; narrow `Reply::Rejected` to true kernel-level failures only |
| Contract-extensible Sema verbs | Decline — wait for forced case | No current contract has proven the 6-verb spine is too tight |

## 7 · Implementation work order

```mermaid
flowchart TD
    h1[Hole 1: Lowering Result + Reply/SubReply extensions]
    h2[Hole 2: observable open/close grammar]
    h4[Hole 4: default observer filter]
    h3design[Hole 3: design pass — projection bridge]
    h3impl[Hole 3: implement projection types + methods]
    h5[Hole 5: pilot as worked example]

    h1 --> h2
    h2 --> h4
    h4 --> h3design
    h3design --> h3impl
    h3impl --> h5
```

Rationale for the order:

- **Hole 1 first** — touches signal-executor + signal-frame
  (`Reply` / `SubReply` extensions). Foundation for everything
  else. Smaller change than it looks (no projection types yet).
- **Hole 2 next** — pure macro grammar change in signal-frame.
  Independent of hole 1.
- **Hole 4 with hole 2** — same macro file, complementary
  grammar additions.
- **Hole 3 design pass** — the projection bridge needs one
  more design report (this report sketches the shape; the
  full mechanical spec for the trait associated types + macro
  generation of the `<Channel>Lowering` trait alias deserves
  its own detail report before implementation).
- **Hole 3 implement** — adds the two associated types + two
  methods to `Lowering`; updates `Executor::execute`.
- **Hole 5 last** — needs all four prior holes to settle so
  the pilot isn't built on transitional API.

## 8 · Estimated touch-points per crate

| Crate | Holes touching it | Touch-points |
|---|---|---|
| `signal-frame` | 1, 2, 3, 4 | `Reply`/`SubReply` enum extensions; macro grammar; macro emit; macro-generated `<Channel>Lowering` trait alias |
| `signal-executor` | 1, 3 | `Lowering` trait extension; `Executor::execute` rewrite |
| `signal-sema` | (none directly) | — |
| `signal-repository-ledger` | 2, 4, 5 | observable block; default filter; integration tests |
| `repository-ledger` | 5 | `Lowering` impl; observer adapter; end-to-end test |

Plus the macro-coordination check across `signal-frame` and
`signal-executor` to make sure the projection types align.

## 9 · References

- `reports/designer/244-hole-finding-after-243-implementations.md`
  — the original hole inventory.
- `reports/designer/245-design-alternatives-for-244-holes.md`
  — alternatives sketch; this report supersedes it for the
  practical spec.
- `reports/operator/140-signal-frame-executor-hole-analysis.md`
  — operator's analysis with crate-boundary correction on
  hole 3; the trigger for this bundled fix.
- `reports/designer/243-reply-naming-observer-hook-executor-trait.md`
  — the original three-design report; hole 1 and 3
  alternatives correct mechanical gaps in §1 and §3.
- `reports/designer/241-signal-architecture-migration-guide.md`
  — broader migration spec.
- `signal-frame` `1610be7c` + `b86442ac` — the observable
  block landing.
- `signal-executor` `57040d59` — the executor crate.
- `intent/component-shape.nota` 2026-05-19T20:00Z — observer
  hook is not security-sensitive (informs hole 4 default
  filter shape).
- `intent/naming.nota` — verb-form rule (informs hole 2
  grammar).
