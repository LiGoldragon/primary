# Signal / Sema / Executor Refresh

## Context

I refreshed from the current workspace guidance and the recent signal
redesign reports before touching code:

- `ESSENCE.md`
- `INTENT.md`
- `AGENTS.md`
- `repos/lore/AGENTS.md`
- `orchestrate/AGENTS.md`
- `skills/operator.md`
- `skills/contract-repo.md`
- `skills/component-triad.md`
- `skills/rust-discipline.md`
- `skills/naming.md`
- `reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`
- `reports/designer/239-signal-architecture-migration-plan.md`
- `reports/designer/240-signal-frame-operation-collapse-check-removal.md`
- `reports/designer/246-v4-bundled-fix-deep-design-with-examples.md`
- `reports/designer/247-radical-rethink-or-converge.md`
- `reports/designer/248-three-layer-changes-for-operators.md`
- `reports/designer/253-tosemaoutcome-trait-shape.md`

The design I implemented against is:

```text
Layer 1: Contract Operation
  external, component-local signal contract vocabulary

Layer 2: Component Command
  internal, executable, component-local command record

Layer 3: Sema Classification
  universal, payloadless operation/outcome observation vocabulary
```

`SemaOperation` is not executable. It is the shared observation class.
Execution belongs to each component through its own typed command
records.

## Code Landed

### `signal-executor`

Pushed commits:

- `1757d519` `signal-executor: use component-local effects`
- `6c374c47` `signal-executor: bump signal-sema classification docs`

What changed:

- Deleted `src/effect.rs`.
- Deleted the exported `SemaEffect` and `SemaEffectOutcome` types.
- Deleted the deprecated `SemaEngine` alias.
- Renamed the executable trait surface to `CommandExecutor`.
- Added `CommandEffect<Command, ComponentEffect>`.
- Changed `OperationEffects` and `BatchEffects` to preserve
  source-operation grouping over component-local command effects.
- Made `CommandEffect::sema_observation()` project through
  `ToSemaOperation` and `ToSemaOutcome`.
- Updated observer plumbing so committed facts are command/effect
  pairs, not executor-owned Sema effects.
- Rewrote `ARCHITECTURE.md` and `README.md` around the three-layer
  design.
- Updated the lockfile to the current `signal-sema` commit.

The current executor flow is:

```text
Request<Operation>
  -> Lowering::lower(Operation)
  -> OperationPlan<Command>
  -> CommandExecutor::execute_atomic_batch(BatchPlan<Command>)
  -> BatchEffects<Command, ComponentEffect>
  -> Lowering::reply_from_effects(...)
  -> Reply<ContractReply>
```

Observation flow:

```text
OperationReceived(Operation)                 before lowering
EffectEmitted(CommandEffect<Command, Effect>) after commit
CommandEffect::sema_observation()             generic Sema label
```

### `signal-sema`

Pushed commit:

- `a1715949` `signal-sema: describe sema as classification`

What changed:

- Updated crate docs, README, Cargo description, and operation docs
  so `signal-sema` is described as classification/projection, not as
  the executable database language.
- No runtime code change; this aligned the documentation with the
  already-landed `ToSemaOperation`, `ToSemaOutcome`, and
  `SemaObservation` code.

## Verification

`signal-executor`:

```text
CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

Result: pass.

`signal-sema`:

```text
CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

Result: pass.

The Nix checks used `--max-jobs 0`; the builds ran on the remote
builder.

## What This Accomplishes

The old executor-owned Sema effect path is gone.

Before:

```text
Operation -> Sema command/effect-ish executor surface
```

After:

```text
Operation -> component Command -> component Effect -> SemaObservation
```

This matters because the code now matches the architecture:

- `signal-executor` does not pretend to know database payloads.
- `signal-sema` does not pretend to be the executable command
  language.
- Components keep their own executable command records.
- Generic observers get a uniform, payloadless classification:
  `SemaObservation { operation, outcome }`.

The Counter test fixture now witnesses the intended pattern:

```rust
pub enum CounterCommand {
    Increment { magnitude: u32 },
    Decrement { magnitude: u32 },
    Query,
    ResetTracking,
}

impl ToSemaOperation for CounterCommand {
    fn to_sema_operation(&self) -> SemaOperation {
        match self {
            Self::Increment { .. } => SemaOperation::Assert,
            Self::Decrement { .. } => SemaOperation::Retract,
            Self::Query => SemaOperation::Match,
            Self::ResetTracking => SemaOperation::Validate,
        }
    }
}

pub enum CounterEffectOutcome {
    IncrementApplied { rows_written: u64 },
    DecrementApplied { rows_matched: u64 },
    ReadCompleted { rows_read: u64 },
    TrackingValidated { predicate_held: bool },
}

impl ToSemaOutcome for CounterEffectOutcome {
    fn to_sema_outcome(&self) -> SemaOutcome {
        match self {
            Self::IncrementApplied { .. } => SemaOutcome::Asserted,
            Self::DecrementApplied { .. } => SemaOutcome::Retracted,
            Self::ReadCompleted { .. } => SemaOutcome::Matched,
            Self::TrackingValidated { .. } => SemaOutcome::Validated,
        }
    }
}
```

## Still Not Done

The infrastructure is cleaner, but the full workspace is not migrated.

High-signal remaining work:

- Sweep all contract and component repos for stale `SemaEffect`,
  `SemaEngine`, and old executor API usage.
- Migrate the current Persona pilot component to the
  `CommandExecutor` / `CommandEffect` surface.
- Decide whether the standard observable event record should keep the
  name `SemaEffectEmitted` now that there is no `SemaEffect` type, or
  be renamed to something like `ObservationEmitted`.
- Run the next pilot through the full path:

```text
CLI NOTA
  -> signal-frame Request<Operation>
  -> component Lowering
  -> component CommandExecutor
  -> command/effect observation
  -> Reply<ContractReply>
  -> CLI NOTA
```

## Current Gaps

### Downstream Drift

`signal-executor` and `signal-sema` now agree. Downstream repos may
not. The next task should be a real grep-and-compile sweep over the
active component repos, then small migrations one repo at a time.

### No Live Daemon Witness Yet

The executor tests are strong library witnesses, but we still need a
live daemon witness. The minimum useful witness is one component CLI
talking to one component daemon over signal frames and proving:

- domain rejection returns typed `SubReply::Failed.detail`;
- engine failure returns batch-aborted accepted reply;
- committed commands emit command/effect observations;
- the CLI only translates NOTA to frames and frames to NOTA.

### Non-Empty Operation Plans

`OperationPlan<Command>` is non-empty. That means validation/no-op
work should lower to a typed command that can produce
`SemaOutcome::NoChange` or `SemaOutcome::Validated`, rather than
lowering to an empty command list. This is coherent, but it should be
treated as an explicit architectural rule.

## Intent Clarification Needed

1. Should Persona standardize the observable event record name away
   from `SemaEffectEmitted`, now that `SemaEffect` is not a type?
   My lean: yes, eventually. `ObservationEmitted` is more accurate.
   For the immediate code, I removed the executor-owned type and kept
   projection neutral.

2. Should every source operation always lower to at least one
   component command?
   My lean: yes. No-op and validation are still real commands; their
   effects project to `NoChange` or `Validated`.

3. Is the immediate pilot still `persona-spirit`, or should the
   simpler ledger pilot run first as a pattern witness?
   My current read from recent user direction is `persona-spirit`,
   but the design reports still contain a ledger-first argument.
