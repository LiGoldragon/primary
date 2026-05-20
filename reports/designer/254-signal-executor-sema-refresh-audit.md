# 254 — signal-executor + signal-sema refresh audit (operator-facing)

*Audit of operator's three-layer landing per /144, now extended with
psyche affirmations on five surfaced gaps (intent records
2026-05-20T15:00:00Z in `intent/persona.nota` and
`intent/component-shape.nota`). All five points are now locked.
This report is the operator-facing direction for the next slice.*

## 0 · TL;DR

**Audit verdict on the landed slice**: spec-correct. The three-layer
model is faithfully implemented at the signal-sema + signal-executor
library boundary. `CommandEffect::sema_observation()` composes both
projection traits at the right point. Counter test fixture exercises
the full pattern. Library tests + Nix checks pass.

**Five gaps surfaced; all now psyche-affirmed**:

| # | Gap | Status | Intent record |
|---|---|---|---|
| 1 | `BatchErrorClassification` trait | **Land now, before pilot** | `component-shape.nota` 15:00:00Z |
| 2 | Observable event-pair name | **`OperationReceived` / `EffectEmitted`** | `component-shape.nota` 15:00:00Z |
| 3 | No-op as explicit command | **Affirmed — every operation lowers to `NonEmpty<Command>`** | `component-shape.nota` 15:00:00Z |
| 4 | Persona-spirit as first pilot | **Confirmed — psyche wants to use spirit now** | `persona.nota` 15:00:00Z |
| 5 | Spirit CLI replaces intent-log filesystem | **Major workspace direction; pilot's load-bearing motivator** | `persona.nota` 15:00:00Z |

Operator's work order: (1) land `BatchErrorClassification` trait
first; (2) update the observable event-pair name to drop the Sema
prefix; (3) start the persona-spirit pilot under the now-locked
three-layer shape; (4) thread the no-op-as-explicit-command rule
through spirit's lowering. The pilot's ultimate target is the
substrate replacement — agents stop writing `intent/*.nota` files
and start using a spirit CLI instead.

## 1 · What was implemented (per /144)

Three commits across two repos:

| Repo | Commit | Effect |
|---|---|---|
| signal-executor | `1757d519` | use component-local effects; removed `SemaEffect`, `SemaEffectOutcome`, `SemaEngine`; introduced `CommandExecutor`, `CommandEffect`, per-operation effect grouping |
| signal-executor | `6c374c47` | bump signal-sema classification docs |
| signal-sema | `a1715949` | describe sema as classification (docs only) |

The implementation matches /246-v4 §3, /248 §1 v4 target, and /253's
two-trait shape. `CommandEffect::sema_observation()` composes
`ToSemaOperation` (on `Command`) and `ToSemaOutcome` (on
`ComponentEffect`) into a payloadless `SemaObservation`. `SemaOutcome`
includes `NoChange` per /253 §5's recommendation.

The Counter test fixture demonstrates the intended pattern end-to-end
— a component declares its own `CounterCommand` and
`CounterEffectOutcome` enums, impls both projection traits, and the
executor handles the plumbing.

## 2 · What aligns with the spec

### Trait shapes

```rust
pub trait Lowering {
    type Operation: RequestPayload;
    type Reply;
    type Command;
    type ComponentEffect;
    fn lower(&self, operation: &Self::Operation)
        -> Result<OperationPlan<Self::Command>, Self::Reply>;
    fn reply_from_effects(
        &self,
        operation: &Self::Operation,
        effects: &OperationEffects<Self::Command, Self::ComponentEffect>,
    ) -> Self::Reply;
}

pub trait CommandExecutor {
    type Command;
    type ComponentEffect;
    type Error;
    fn execute_atomic_batch(&mut self, plan: BatchPlan<Self::Command>)
        -> Result<BatchEffects<Self::Command, Self::ComponentEffect>, Self::Error>;
}
```

All four associated types on `Lowering` per /248. `CommandExecutor`
returns component-typed effects, not `SemaEffect`. ✓

### Structural shape

- `OperationPlan<Command>` carries `NonEmpty<Command>`. ✓
- `BatchPlan<Command>` carries `NonEmpty<OperationPlan<Command>>`. ✓
- `BatchEffects<Command, ComponentEffect>` carries
  `NonEmpty<OperationEffects<Command, ComponentEffect>>`. ✓
- `CommandEffect { command, effect }` is the raw fact unit. ✓

### Projection trait composition

```rust
impl CommandEffect<Command, ComponentEffect> {
    pub fn sema_observation(&self) -> SemaObservation
    where Command: ToSemaOperation, ComponentEffect: ToSemaOutcome,
    { SemaObservation::from_projection(&self.command, &self.effect) }
}
```

Exactly /253's two-trait shape. ✓

### Reply correlation

- Domain rejection during lowering → `Reply::Accepted` +
  `AcceptedOutcome::OperationAborted` + typed `SubReply::Failed.detail`. ✓
- Engine failure → `Reply::Accepted` + `AcceptedOutcome::BatchAborted`
  + all sub-replies `SubReply::Invalidated`. ✓
- Successful batch → `Reply::Accepted` +
  `AcceptedOutcome::Committed` + per-operation `SubReply::Ok(...)`. ✓

### Observer publication

- `publish_operation_received` before lowering. ✓
- `publish_effect_emitted` after each command-effect pair commits. ✓
- `FrameObserverBridge` composes
  `ObservationProjection` + `ObservableSet` + `ObserverDelivery`
  per /246-v4 §3. ✓

The architecture and the code agree.

## 3 · The five affirmed directions

### 3.1 — `BatchErrorClassification` trait (land now)

**Affirmation**: `intent/component-shape.nota` 2026-05-20T15:00:00Z.
Psyche: *"yes, land now. I told him to go back to that now."*

**Current shape (incorrect)**: `executor.rs:80-83, 153-168` hardcodes
`retry: Unknown, commit: NotCommitted, reason: EngineRejected` on
every engine failure. The engine error is stashed via
`take_last_engine_error()`.

**Correct shape**: a `BatchErrorClassification` trait bound on
`CommandExecutor::Error`:

```rust
pub trait BatchErrorClassification {
    fn batch_failure_reason(&self) -> BatchFailureReason;
    fn retry_classification(&self) -> RetryClassification;
    fn commit_status(&self) -> CommitStatus;
}
```

Then `CommandExecutor::Error: BatchErrorClassification` is a bound on
the executor's generic. At `batch_aborted_reply` construction the
executor calls `error.batch_failure_reason()`, `error.retry_classification()`,
`error.commit_status()` and threads them into
`AcceptedOutcome::BatchAborted { reason, retry, commit }`.

The wire reply then carries meaningful per-engine-error metadata.
Different engine errors classify themselves:

- A transient lock-contention error: `EngineUnavailable`,
  `Retryable`, `NotCommitted`.
- A constraint-violation panic: `EngineRejected`, `NotRetryable`,
  `NotCommitted`.
- A mid-commit crash recovery sees uncertain commit:
  `EngineRejected`, `NotRetryable`, `Unknown`.

The `take_last_engine_error()` stash pattern stays as a complementary
diagnostic surface for daemon-side logging; the trait does not
replace it but supplements it.

**Operator action**:
1. Add `BatchErrorClassification` trait to `signal-frame` (alongside
   the existing `BatchFailureReason` / `RetryClassification` /
   `CommitStatus` types).
2. Bound `CommandExecutor::Error: BatchErrorClassification` in
   signal-executor.
3. Update `batch_aborted_reply` to call the three classification
   methods at construction time instead of hardcoding constants.
4. Update Counter test fixture: define `CounterEngineError` with a
   `BatchErrorClassification` impl exercising different
   classification combinations.
5. Document the trait's contract in signal-executor/ARCHITECTURE.md.

### 3.2 — Observable event-pair naming

**Affirmation**: `intent/component-shape.nota` 2026-05-20T15:00:00Z.
Psyche: *"go with your lean."*

**Canonical pair**: `OperationReceived` / `EffectEmitted`.

The Sema prefix is dropped from `EffectEmitted` because the event
carries the **typed component effect**, not the universal Sema
classification. (The universal classification is `SemaObservation`,
derived via `CommandEffect::sema_observation()`.)

**State of code**:

- `signal-executor::observer.rs`'s `RecordedEvent` variants are
  already `OperationReceived` / `EffectEmitted`. ✓
- `signal-executor::bridge.rs` uses generic
  `Projection::OperationEvent` / `Projection::EffectEvent` — no
  hardcoded name. ✓
- The **macro-generated observable block** in `signal-frame` needs
  the rename. The current emit produces `SemaEffectEmitted`; new
  emit produces `EffectEmitted`.

**Operator action**:
1. Update `signal-frame`'s macro emit (`signal-frame-macros/src/emit.rs`)
   to generate `EffectEmitted` instead of `SemaEffectEmitted`.
2. Search workspace for `SemaEffectEmitted` references; rename across
   contracts that already declared observable blocks.
3. Tests + Nix checks across signal-frame + downstream contracts.

### 3.3 — No-op as explicit command (rule affirmed)

**Affirmation**: `intent/component-shape.nota` 2026-05-20T15:00:00Z.
Psyche: *"I greelight your recommendation"* (responding to concrete
examples).

**Rule**: every accepted operation lowers to `NonEmpty<Command>`.
No-ops, validations, and idempotent applies lower to **explicit
named commands**, not empty plans.

**Worked examples** (operator can reuse these in lowering impls):

- `ValidateProposal` operation →
  `LedgerCommand::CheckProposalAgainstCurrent { proposal }`.
  Command runs (reads state, computes verdict). Effect:
  `LedgerEffect::ProposalVerdict { matches }`.
  `SemaOperation::Validate` / `SemaOutcome::Validated` (or
  `NoChange` if literally nothing was read).
- `ApplyConfiguration` where the config is already current →
  `LedgerCommand::RecordIdempotentApply { reason: AlreadyCurrent }`.
  Explicit command saying *"we processed this, no state change
  needed."* Effect: `LedgerEffect::IdempotentApplyRecorded`.
  `SemaOperation::Mutate` (intent was a write) /
  `SemaOutcome::NoChange` (no durable change).
- Pure read → `LedgerCommand::ReadLatestEntry`. Always lowers —
  never zero commands.

**Why the rule**:
1. The structural type already says `NonEmpty<Command>` — if
   zero-command operations were allowed, the type would have to
   weaken to `Vec`.
2. Every operation has an executor-visible witness. Empty plans
   would be invisible to introspection and break Sema observation
   coverage.
3. Named-command shape makes semantics explicit:
   `RecordIdempotentApply` is a different fact than
   `RecordSuccessfulApply`, even if both produce
   `SemaOutcome::NoChange`.

**Operator action**:
- Apply this rule in persona-spirit's lowering impl. Spirit's
  validation operations (e.g., classify-without-storing) lower to
  explicit `SpiritCommand` variants with appropriate `SemaOutcome`
  projections.
- Document the rule in signal-executor/ARCHITECTURE.md alongside
  the `Lowering` trait surface.

### 3.4 — Persona-spirit as first pilot (confirmed)

**Affirmation**: `intent/persona.nota` 2026-05-20T15:00:00Z. Psyche:
*"persona-spirit first because I want to use it."*

**Decision**: persona-spirit is the first signal-executor pilot. The
earlier /143 + /159 + /152 recommendation of repository-ledger as the
simpler proving ground is **deferred**, not abandoned. Psyche has
weighed the trade-off — infrastructure issues during the pilot will
be debugged alongside cognitive concerns — and prioritized spirit
because the workspace needs the substrate replacement (see §3.5
below).

This is a conscious workspace direction, not an oversight.

**Operator action**:
- Persona-spirit is the next pilot. The repository-ledger pilot
  remains on the backlog (/248 §3) for after spirit ships.

### 3.5 — Spirit CLI replaces intent-log filesystem (major workspace direction)

**Affirmation**: `intent/persona.nota` 2026-05-20T15:00:00Z. Psyche:
*"I want it migrated to the new architecture and ready to replace
our ugly ad-hoc intent-log file system with an elegant spirit cli."*

**Decision**: persona-spirit's eventual role is the canonical
substrate for psyche intent recording. The current
`intent/*.nota` flat files (lock-free O_APPEND) are **transitional**;
the eventual substrate is spirit's typed record store, accessed via
spirit CLI.

Today (transitional):

```sh
cat >> intent/<topic>.nota <<'EOF'
(Decision "..." "..." "..." Maximum 2026-05-20T...)
EOF
```

Future (post-pilot):

```sh
spirit '(Decision "..." "..." "..." Maximum <timestamp>)'
```

The five-kind taxonomy (Decision / Principle / Correction /
Clarification / Constraint) persists; only the substrate changes.

**Implications**:

1. Spirit's contract and storage schema must support the
   five-kind taxonomy + the canonical positional-NOTA shape
   (summary / verbatim / context / certainty / timestamp).
2. The agent-facing CLI is spirit's primary surface, not its
   sema-engine database directly.
3. Skills change. `skills/intent-log.md` will need a major
   revision to document the spirit-CLI substrate.
   `skills/intent-maintenance.md` similarly.
4. Migration arc (designer follow-up, not blocking the pilot):
   ingestion of existing `.nota` records into spirit; dual-substrate
   window; agent tooling; eventual deletion of the file-based
   substrate.

**Operator action**:
- Persona-spirit pilot must support intent-record submission via
  CLI as a core operation. Spirit's `Submit` (or equivalent
  contract verb) accepts a `PsycheStatement` payload with the
  five-kind shape. Spirit stores it as a typed record.
- Spirit's `Query` returns intent records by topic + filter.
- The pilot is the proving ground for both the signal-executor
  three-layer pattern AND the substrate replacement.

## 4 · Other audit observations

### Reply correlation: the `assert_eq` on shape

`executor.rs:94-98` asserts that the `CommandExecutor` returns one
`OperationEffects` per input `OperationPlan`. Structural invariant;
runtime panic on violation. Library-boundary contract violation
warrants a panic; the invariant is correct.

### `OperationFailureReason::DomainRejection` is the only operation-aborted reason

`executor.rs:122-151` always assigns `DomainRejection`. Fine for now;
the enum may grow if lowering can fail in other ways (e.g.,
resource shortage during lowering). Not a blocker.

### The `last_engine_error` stash pattern

`take_last_engine_error(&mut self) -> Option<S::Error>` is the
diagnostic surface complementing the new `BatchErrorClassification`
trait. The stash works under the sequential-execution assumption (one
request at a time per Executor instance). Document this assumption in
the executor's ARCHITECTURE.md.

### Counter fixture is the library-level proving ground

The Counter test fixture exercises:
- Domain-rejection-during-lowering (typed reply).
- Engine-failure (BatchAborted).
- Successful batch (CommandEffect emission, observer publication).
- Sema projection composition.

Strong library-level witness. Not a daemon witness — that requires
the persona-spirit pilot.

## 5 · Operator's work order

Sequence for the next slice:

### 5.1 — `BatchErrorClassification` trait (signal-frame + signal-executor)

1. Add the trait + reuse `BatchFailureReason` / `RetryClassification`
   / `CommitStatus` (already in signal-frame).
2. Bound `CommandExecutor::Error: BatchErrorClassification`.
3. Update `batch_aborted_reply` to thread through `error.classify_*()`.
4. Counter test: define `CounterEngineError` with a multi-variant
   classification impl.
5. Docs + tests + Nix check.

### 5.2 — `EffectEmitted` rename (signal-frame macro)

1. Update `signal-frame-macros/src/emit.rs` to emit `EffectEmitted`
   instead of `SemaEffectEmitted`.
2. Rename in any contract that has already declared an observable
   block.
3. Tests + Nix check.

### 5.3 — Persona-spirit pilot migration

1. Inspect persona-spirit's current contract / daemon / CLI.
2. Identify which pieces block the three-layer migration (e.g.,
   signal-core dependency that needs to become signal-frame +
   signal-sema; SignalVerb usage; old executor shape).
3. Migrate one slice at a time. Prove each slice end-to-end:
   - CLI NOTA → frame → daemon → typed reply → CLI NOTA.
   - Domain rejection produces typed `SubReply::Failed.detail`.
   - Engine failure produces `BatchAborted` with proper
     classification.
   - Successful commits emit observer events.
   - No-op lowering uses explicit named commands (§3.3 rule).
4. The pilot's intent-record-submission operation is the proving
   ground for §3.5 — spirit accepts a `PsycheStatement` payload,
   stores it, returns a typed receipt. Agent-facing CLI surface is
   the substrate replacement target.

### 5.4 — Skipped (out of this slice)

- Downstream component repo sweep for stale `SemaEffect` /
  `SemaEngine` usage. Operator's lane per /144 §"Downstream Drift,"
  but not part of the immediate critical path; can run in parallel
  or after the spirit pilot lands.
- Repository-ledger pilot. Deferred per §3.4.
- Intent-log migration arc (existing `.nota` → spirit storage).
  Designer follow-up after pilot lands.

## 6 · References

### Intent records that landed with this report

- `intent/persona.nota` 2026-05-20T15:00:00Z — spirit CLI replaces
  intent-log filesystem (§3.5).
- `intent/persona.nota` 2026-05-20T15:00:00Z — persona-spirit as
  first pilot, motivator: psyche wants to use it (§3.4).
- `intent/component-shape.nota` 2026-05-20T15:00:00Z —
  `BatchErrorClassification` trait shape (§3.1).
- `intent/component-shape.nota` 2026-05-20T15:00:00Z — no-op as
  explicit command rule (§3.3).
- `intent/component-shape.nota` 2026-05-20T15:00:00Z —
  `OperationReceived` / `EffectEmitted` canonical event-pair (§3.2).

### Design substrate

- `/144` (operator) — refresh implementation report.
- `/246-v4` §1, §3 — Lowering / CommandExecutor / projection spec.
- `/248` §1, §3 — operator-facing change list; pilot landing.
- `/253` — ToSemaOutcome two-trait shape spec.
- `/158`, `/159` (operator-assistant) — independent audits +
  `BatchErrorClassification` recommendation.
- `intent/persona.nota` 2026-05-19T14:00:00Z — persona-spirit as
  cognitive apex.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z — three-layer
  affirmation.

This report retires when the operator's work order in §5 lands
end-to-end and a successor pilot witness report follows.
