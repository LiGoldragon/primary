# Signal / Sema / Executor Refresh

## Current State

This report updates the earlier lower-component refresh after
`reports/designer/254-signal-executor-sema-refresh-audit.md`.

The architecture now has three distinct layers:

```text
Contract Operation
  external operation vocabulary in a signal contract

Component Command
  internal executable command vocabulary owned by a daemon/component

Sema Classification
  universal payloadless observation labels:
  SemaOperation + SemaOutcome = SemaObservation
```

The important shift is that Sema is no longer treated as the executable
database language. A component executes its own commands. Sema records the
cross-component class of what happened.

## What Landed

| Repo | Commit | Change |
|---|---|---|
| `signal-frame` | `68891f60` | Owns `BatchErrorClassification`; tests canonical batch failure projection; observable examples use `EffectEmitted`. |
| `signal-executor` | `66b5ee48` | Imports/re-exports `signal-frame::BatchErrorClassification`; executor no longer owns that trait; docs cleaned. |
| `signal-persona-spirit` | `a1909872` | Canonical observable event pair is now `OperationReceived` / `EffectEmitted`. |
| `persona-spirit` | `6aeea3fd` | Bumped to the new `signal-frame` and `signal-persona-spirit` revisions. |
| `persona-spirit` | `951603c3` | Added constraint witnesses for explicit no-change commands and unimplemented observer requests. |

Earlier same-slice commits still matter:

- `signal-executor` `1757d519`: removed the old executor-owned
  `SemaEffect`, `SemaEffectOutcome`, and `SemaEngine` surface.
- `signal-sema` `a1715949`: reframed Sema docs as
  classification/projection.
- `persona-spirit` `556bafcc`: made the CLI binary `spirit`; CLI accepts
  one raw-NOTA or path argument and only translates NOTA to signal frames
  and signal replies back to NOTA.

## Audit Items Closed

### Batch Error Classification

`BatchErrorClassification` now belongs to `signal-frame` beside the wire
types it classifies:

```rust
pub trait BatchErrorClassification {
    fn batch_failure_reason(&self) -> BatchFailureReason;
    fn retry_classification(&self) -> RetryClassification;
    fn commit_status(&self) -> CommitStatus;
}
```

`signal-executor` now requires `CommandExecutor::Error:
BatchErrorClassification` instead of hardcoding every engine failure as
unknown/not-committed/engine-rejected.

This means higher components implement one small trait for their engine
error type and get honest wire-safe batch abort metadata.

### Observable Naming

The canonical observable pair is:

```text
OperationReceived
EffectEmitted
```

`EffectEmitted` carries a `SemaObservation`, not a typed component effect.
The old name `SemaEffectEmitted` was wrong because the old `SemaEffect`
type is gone.

### Explicit No-Change Commands

`persona-spirit` now witnesses that valid no-change paths are still real
commands:

- `Tap` projects as `SemaOperation::Subscribe` +
  `SemaOutcome::NoChange` while observer subscriptions are not implemented.
- `Untap` projects as `SemaOperation::Retract` +
  `SemaOutcome::NoChange`.
- `persona_spirit_unimplemented_observer_request_uses_reply_shaper_not_store`
  proves that the valid unimplemented request goes through `ReplyShaper`
  and does not touch `RecordStore`, `SemaWriter`, or `SemaReader`.

This keeps the invariant: accepted operations do not disappear. Even an
idempotent or unimplemented accepted path has a typed command/effect witness.

## Verification

All repo checks below passed.

`signal-frame`:

```text
CARGO_BUILD_JOBS=2 cargo fmt
CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

`signal-executor`:

```text
CARGO_BUILD_JOBS=2 cargo update -p signal-frame -p signal-frame-macros
CARGO_BUILD_JOBS=2 cargo fmt
CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

`signal-persona-spirit`:

```text
CARGO_BUILD_JOBS=2 cargo update -p signal-frame -p signal-frame-macros
CARGO_BUILD_JOBS=2 cargo fmt
CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

`persona-spirit`:

```text
CARGO_BUILD_JOBS=2 cargo update -p signal-frame -p signal-frame-macros -p signal-persona-spirit
CARGO_BUILD_JOBS=2 cargo fmt
CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

The Nix checks used `--max-jobs 0` and ran on the remote builder.

## Effect On Higher Components

Higher components should now follow this pattern:

```rust
pub enum ComponentCommand {
    RecordEntry(Entry),
    ReadEntries(ReadPlan),
    OpenObserver(ObserverFilter),
}

impl ToSemaOperation for ComponentCommand {
    fn to_sema_operation(&self) -> SemaOperation {
        match self {
            Self::RecordEntry(_) => SemaOperation::Assert,
            Self::ReadEntries(_) => SemaOperation::Match,
            Self::OpenObserver(_) => SemaOperation::Subscribe,
        }
    }
}

pub enum ComponentEffect {
    EntryRecorded(Receipt),
    EntriesRead(Listing),
    ObserverOpened(Token),
}

impl ToSemaOutcome for ComponentEffect {
    fn to_sema_outcome(&self) -> SemaOutcome {
        match self {
            Self::EntryRecorded(_) => SemaOutcome::Asserted,
            Self::EntriesRead(_) => SemaOutcome::Matched,
            Self::ObserverOpened(_) => SemaOutcome::Subscribed,
        }
    }
}
```

The component-local command/effect records are where execution semantics
live. `SemaObservation` is the generic observer label.

For daemon pilots, that means:

- the signal contract stays external and user-facing;
- the daemon lowers contract operations into internal commands;
- the executor runs those commands;
- observer streams publish `OperationReceived` before execution and
  `EffectEmitted` after command effects commit;
- the CLI remains a thin NOTA-to-frame and frame-to-NOTA adapter.

## Remaining Drift

A workspace scan still finds old names outside the lower slice:

```text
signal-persona-orchestrate/src/lib.rs
  ObservationEvent::SemaEffect(SemaEffectObserved)

signal-persona-orchestrate/ARCHITECTURE.md
  effect_event SemaEffectEmitted

signal-persona-introspect/ARCHITECTURE.md
  OperationReceived / SemaEffectEmitted wording
```

Those are not part of the verified lower-component slice. They should be
migrated when the orchestrate/introspect contracts are next touched.

Some components still have error variants named `SemaEngine(...)` because
the crate is still named `sema-engine`. That is not the old
`signal-executor::SemaEngine` alias, but the repeated phrase will keep
confusing agents. Rename only if the owning component is otherwise being
edited.

## Advice

Use `signal-frame::BatchErrorClassification` at every executor boundary.
Do not define local copies.

Use `OperationReceived` / `EffectEmitted` for Persona observable contracts
unless there is a concrete local reason to deviate.

Never reintroduce executable Sema payloads. If a component needs executable
data, that data belongs in its local command enum.

Treat no-op and idempotent paths as explicit commands. The outcome can be
`NoChange`, but the command should still exist.

Keep the `spirit` CLI thin. It should accept one NOTA record or one path,
send a signal frame to the daemon socket, and print a NOTA reply. No store
fallback, no in-process actor tree, no convenience business logic.

## Intent Clarification Needed

1. `CommitStatus::Partial` exists in `signal-frame`, but the current
   `CommandExecutor::execute_atomic_batch` contract is all-or-nothing. Do
   we keep `Partial` as a future-proof honest classification for uncertain
   lower engines, or should the executor interface forbid it for now?

2. For the intent-log replacement, should agents start using `spirit
   '(Record ...)'` as soon as the daemon is available, or do we need an
   explicit dual-write/import window for the existing `intent/*.nota`
   files?

3. Should `Tap` / `Untap` observer operations be implemented before
   `spirit` becomes the replacement for intent logging, or is the current
   typed `NoChange` placeholder acceptable until introspection integration?

4. Should `signal-persona-orchestrate` be migrated immediately away from
   `SemaEffectObserved`, or should it wait for the orchestrate contract
   redesign?

5. Is `EffectEmitted` mandatory for every Persona observable contract, or
   is it only the default generated name when a contract does not need a
   more specific observable event vocabulary?

## Next Work

The next productive implementation target is `persona-spirit` as the first
pilot:

```text
spirit NOTA
  -> signal-persona-spirit request frame
  -> persona-spirit daemon
  -> Spirit-local command/effect execution
  -> SemaObservation projection
  -> signal-persona-spirit reply frame
  -> spirit NOTA
```

The minimum pilot bar is a real daemon run proving record submission,
record query, typed rejection, observer-event projection, and restart over
durable state.
