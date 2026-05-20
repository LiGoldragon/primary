# 253 — ComponentEffect → Sema projection: two-trait shape

*Answers the open design question flagged in /246-v4 §3, /248 §1, /158
§3, /159 §"effect projection gap": should ComponentEffect map to
universal Sema observation through a separate `ToSemaOutcome` trait?
Designer answer: **yes** — two-trait shape, symmetric with the
three-layer model. This is the stable reference an implementation agent
can pin to.*

## 0 · Answer

**Yes, two traits.** `ToSemaOperation` on `Command` (classifies the
intended operation). `ToSemaOutcome` on `ComponentEffect` (classifies
the outcome). Composition at observer fanout.

```rust
pub trait ToSemaOperation {
    fn to_sema_operation(&self) -> SemaOperation;
}

pub trait ToSemaOutcome {
    fn to_sema_outcome(&self) -> SemaOutcome;
}
```

`SemaOperation` is the six-class payloadless enum already in
`signal-sema` (`Assert` / `Mutate` / `Retract` / `Match` / `Subscribe`
/ `Validate`).

`SemaOutcome` is a new payloadless enum naming what happened to state
visible to a generic observer (the exact variants land with the
implementation; first cut: `Asserted` / `Mutated` / `Retracted` /
`Matched` / `Subscribed` / `Validated` mirroring the operation classes,
plus `NoChange` for a Validate-style read that didn't write).

A `SemaObservation` record carries both halves, payloadless:

```rust
pub struct SemaObservation {
    pub operation: SemaOperation,
    pub outcome: SemaOutcome,
}
```

The observer fanout (`signal-frame::ObserverFanout`) composes
`SemaObservation` from `(command.to_sema_operation(),
effect.to_sema_outcome())` when fanning out to subscribed observers.

## 1 · Why two traits, not one

### Symmetry with the three-layer model

The three-layer model affirmed 2026-05-20T02:00:00Z
(`intent/component-shape.nota`):

- Layer 1 — Contract Operation (external request).
- Layer 2 — Component Command (component-local executable).
- Layer 3 — Sema Operation (universal payloadless classification).

Each Layer-2 type has a symmetric classification surface to Layer 3:

| Layer 2 type | Classifies to | Trait |
|---|---|---|
| `Command` | `SemaOperation` (what was *intended*) | `ToSemaOperation` |
| `ComponentEffect` | `SemaOutcome` (what *happened*) | `ToSemaOutcome` |

Two halves of the projection, one trait each. The structure mirrors
the data.

### Each impl is local to its own type

Adding a new `Command` variant requires impl `ToSemaOperation` on the
new variant — no `ComponentEffect` knowledge.

Adding a new `ComponentEffect` variant requires impl `ToSemaOutcome` on
the new variant — no `Command` knowledge.

A single `ToSemaEffect(command, effect)` trait would force every impl
to know the *other* type's shape, which couples otherwise-independent
extension points.

### The unified alternative tangles execution and classification

The one-trait alternative (`ToSemaEffect` taking both Command + Effect
together) puts the projection point at the executor's choreography:
the executor has both pieces in hand, so it could call one method that
takes both.

But this entangles two concerns:

- Classification is a property of *what the data is*. The Command's
  Sema class is determined by what the Command names; same for the
  Effect's outcome.
- Execution choreography is *when projection happens*. That belongs
  in the executor.

Two-trait shape keeps the projection logic on the data types where it
belongs; the executor stays choreographer-only.

### Convergent recommendation

Three independent design analyses reached the same conclusion:

- This report (designer).
- `/158` §3 + Q2 (operator-assistant).
- `/159` §4 + Q2 (operator-assistant follow-up).

When three independent analyses converge on a shape, that's evidence
the structure is the right one.

## 2 · Where it lives

| Trait | Crate | Implemented on |
|---|---|---|
| `ToSemaOperation` | `signal-sema` | each daemon's `Command` enum |
| `ToSemaOutcome` | `signal-sema` | each daemon's `ComponentEffect` enum |
| `SemaObservation` | `signal-sema` | composed by `signal-frame::ObserverFanout` |

`signal-sema` already owns the `SemaOperation` enum + `ToSemaOperation`
trait. Add `SemaOutcome` enum + `ToSemaOutcome` trait alongside, plus
the `SemaObservation` record.

`signal-frame::ObserverFanout` consumes both projections when emitting
observer events on the ordinary socket per the universal observer-hook
intent (`intent/component-shape.nota` 2026-05-19T20:00Z, refined into
mandatory `Tap` / `Untap` 2026-05-20T02:00Z).

## 3 · Worked example (repository-ledger pilot)

For the canonical pilot per /248 §3:

```rust
// In repository-ledger (daemon).
impl ToSemaOperation for LedgerCommand {
    fn to_sema_operation(&self) -> SemaOperation {
        match self {
            LedgerCommand::RecordEntry(_)       => SemaOperation::Assert,
            LedgerCommand::AmendEntry(_)        => SemaOperation::Mutate,
            LedgerCommand::RetractEntry(_)      => SemaOperation::Retract,
            LedgerCommand::QueryEntries(_)      => SemaOperation::Match,
            LedgerCommand::SubscribeEntries(_)  => SemaOperation::Subscribe,
            LedgerCommand::ValidateEntry(_)     => SemaOperation::Validate,
        }
    }
}

impl ToSemaOutcome for LedgerEffect {
    fn to_sema_outcome(&self) -> SemaOutcome {
        match self {
            LedgerEffect::EntryRecorded(_)      => SemaOutcome::Asserted,
            LedgerEffect::EntryAmended(_)       => SemaOutcome::Mutated,
            LedgerEffect::EntryRetracted(_)     => SemaOutcome::Retracted,
            LedgerEffect::QueryResult(_)        => SemaOutcome::Matched,
            LedgerEffect::SubscriptionOpened(_) => SemaOutcome::Subscribed,
            LedgerEffect::ValidationResult(_)   => SemaOutcome::Validated,
        }
    }
}

// At observer fanout (signal-frame).
let observation = SemaObservation {
    operation: command.to_sema_operation(),
    outcome:   effect.to_sema_outcome(),
};
observer_channel.publish_observation(observation);
```

The observer downstream (e.g., `persona-introspect`) sees
`SemaObservation` records — payloadless universal classification only.
Component-specific detail (the actual entry contents) is carried
separately through the component's own typed events via
`ObservedLowering::project_effect`, which is the component's choice of
what observable detail to surface.

## 4 · How this lands

This report supplements /246-v4 §3 and /248 §1. The implementation
agent finishing signal-executor's ComponentEffect alignment uses this
shape directly:

- Add `SemaOutcome` enum + `ToSemaOutcome` trait to `signal-sema`.
- Add `SemaObservation` record to `signal-sema`.
- Update `signal-frame::ObserverFanout` to compose `SemaObservation`
  from `(command, effect)` pairs.
- Update `signal-executor::Lowering` to keep its `ComponentEffect`
  associated type (per /248 §1 v4 target) and ensure the executor
  drives `ToSemaOperation` + `ToSemaOutcome` at the fanout point.

Once landed, /246-v4 should be updated to bake this shape into the
canonical spec (or /246-v5 issued if the spec moves enough to warrant
it).

## 5 · Open follow-up (post-implementation)

The exact variant set of `SemaOutcome` is a small open question. First
cut mirrors `SemaOperation`'s six classes plus `NoChange`. Whether
additional outcome variants are needed (e.g., `PartialMatch`,
`StaleSubscription`) emerges during pilot implementation.

A second small follow-up: `SemaObservation` could optionally carry
timing/order metadata (e.g., a monotonic sequence id from the
executor) so observers can correlate observations into causal chains
across components. That is a design question for after the pilot, not
a blocker for this trait shape.

## 6 · References

- `/246-v4` §3 — bundled-fix canonical spec; mentions `ToSemaOperation`
  but leaves the effect projection open.
- `/248` §1 — operator-facing change list; flags `ComponentEffect`
  shape as needed but does not lock the projection trait.
- `/158` §3 + Q2 — operator-assistant analysis recommending two-trait
  shape.
- `/159` §4 + Q2 — operator-assistant follow-up confirming two-trait
  recommendation.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z — three-layer
  model affirmation; the structural basis for the two-trait
  symmetry.
- `intent/component-shape.nota` 2026-05-19T20:00Z — universal
  observer-hook intent on the ordinary socket.

This report retires when the trait pair lands in `signal-sema` and
the repository-ledger pilot exercises it end-to-end. At that point,
/246-v4 absorbs the shape and this report converts to a historical
record.
