# Signal Frame / Executor v4 Reconciliation

This report considers `reports/designer/246-v4-bundled-fix-deep-design-with-examples.md`
against the current `signal-frame` and `signal-executor` worktrees.

The short finding: `/246` is now the better target than
`reports/operator/141-signal-frame-executor-correction-examples.md`,
but the current implementation has only landed part of it. It also
currently does not compile.

## Current Lock State

`operator.lock` currently owns the main implementation files:

- `/git/github.com/LiGoldragon/signal-frame/src/reply.rs`
- `/git/github.com/LiGoldragon/signal-frame/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-frame/tests/frame.rs`
- `/git/github.com/LiGoldragon/signal-executor/src/lowering.rs`
- `/git/github.com/LiGoldragon/signal-executor/src/executor.rs`
- `/git/github.com/LiGoldragon/signal-executor/src/engine.rs`
- `/git/github.com/LiGoldragon/signal-executor/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-executor/tests/*`

`second-designer-assistant.lock` owns `/git/github.com/LiGoldragon/signal-frame/macros`
for the `/246` macro changes.

I did not edit through those locks. This report is the handoff surface.

## Compile State

I ran:

```sh
CARGO_BUILD_JOBS=1 cargo test --all-targets
```

in both repos.

`signal-frame` fails in `signal-frame-macros`. The macro model now has
`ObservableBlockSpec { filter, operation_event, effect_event }`, but emitter
code still tries to read `open_verb` and `close_verb`, and it tries to quote
`FilterDecl` directly:

```text
error[E0609]: no field `open_verb` on type `&ObservableBlockSpec`
error[E0609]: no field `close_verb` on type `&ObservableBlockSpec`
error[E0277]: the trait bound `FilterDecl: quote::ToTokens` is not satisfied
```

`signal-executor` also fails because its Git dependency resolves to the same
broken `signal-frame` revision, so it sees the macro compile errors before it
can compile its own code.

This is the first thing to fix: restore `signal-frame` compile green before
continuing the executor migration.

## What Already Aligns With v4

The current implementation has absorbed some of `/246`:

- `signal-frame::AcceptedOutcome` is split into `Committed`,
  `OperationAborted`, and `BatchAborted`.
- Contract-domain rejection is no longer a kernel `Reply::Rejected`; it is
  carried as typed detail in `SubReply::Failed`.
- `signal-executor::Lowering` now has a `Command` associated type.
- `OperationPlan<Command>` and `BatchPlan<Command>` exist, so ownership is
  structural instead of a sidecar index.
- `SemaEngine` executes component-local commands rather than bare
  `SemaOperation` tags.

That is real progress, but it is not the full v4 design.

## Missing From v4

### 1. Batch abort metadata is incomplete

`/246` requires:

```rust
AcceptedOutcome::BatchAborted {
    reason: BatchFailureReason,
    retry: RetryClassification,
    commit: CommitStatus,
}
```

Current code has:

```rust
AcceptedOutcome::BatchAborted {
    reason: BatchFailureReason,
}
```

This loses two pieces of generic execution metadata:

- whether retrying the same request is meaningful;
- whether the engine can prove no state changed.

That distinction matters because batch failure is not always the same fact.
`EngineRejected + NotCommitted` is ordinary failure. `EngineRejected +
CommitStatus::Unknown` is an operator alarm.

### 2. Component effects are still collapsed into `SemaEffect`

`/246` names three layers:

- Contract Operation: wire language.
- Component Command: daemon-owned executable language.
- Sema Operation: payloadless observation classification only.

The current executor has `Command`, but it still makes the engine return
`Vec<SemaEffect>`. That skips the v4 `ComponentEffect` layer.

Current `Lowering`:

```rust
pub trait Lowering {
    type Operation: RequestPayload;
    type Reply;
    type Command;

    fn lower(&self, operation: &Self::Operation)
        -> Result<OperationPlan<Self::Command>, Self::Reply>;

    fn reply_from_effects(
        &self,
        operation: &Self::Operation,
        effects: &[SemaEffect],
    ) -> Self::Reply;
}
```

v4 target:

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
        effects: &[Self::ComponentEffect],
    ) -> Self::Reply;
}
```

The current shape still treats universal `SemaEffect` as the thing execution
produces. v4 says the daemon executes component commands and produces
component effects; Sema classification is projected for observation.

### 3. The Sema projection boundary is resolved by `/253`

`/246` defines:

```rust
pub trait ToSemaOperation {
    fn to_sema_operation(&self) -> SemaOperation;
}
```

on `Command`.

That classifies the command, but observers also need an effect outcome.
`reports/designer/253-tosemaoutcome-trait-shape.md` settles the answer:
use two traits, both owned by `signal-sema`.

```rust
pub trait ToSemaOperation {
    fn to_sema_operation(&self) -> SemaOperation;
}

pub trait ToSemaOutcome {
    fn to_sema_outcome(&self) -> SemaOutcome;
}
```

`SemaOperation` is the payloadless intent classifier implemented on each
daemon's `Command`. `SemaOutcome` is the payloadless result classifier
implemented on each daemon's `ComponentEffect`. `signal-sema` also owns the
payloadless universal observation record:

```rust
pub struct SemaObservation {
    pub operation: SemaOperation,
    pub outcome: SemaOutcome,
}
```

`signal-frame::ObserverFanout` composes the observation from
`(command.to_sema_operation(), effect.to_sema_outcome())`. The rejected
alternative is a unified `ToSemaEffect(command, effect)` projection because it
tangles classification with executor choreography. Projection belongs on the
Layer-2 data types; the executor only composes the two projections at the
fanout point.

### 4. Engine error classification needs a real trait

`/246` sketches:

```rust
let (reason, retry, commit) = engine_error.classify();
```

The current `SemaEngine` trait exposes only:

```rust
pub trait SemaEngine {
    type Command;
    type Error;

    fn execute_atomic(
        &mut self,
        commands: Vec<Self::Command>,
    ) -> Result<Vec<SemaEffect>, Self::Error>;
}
```

There is no trait requiring `Error` to produce `BatchFailureReason`,
`RetryClassification`, and `CommitStatus`. Without that trait, the executor
can only hard-code `BatchFailureReason::EngineRejected`, which is exactly the
metadata loss `/246` is trying to remove.

### 5. Operation plan cardinality needs one final decision

`/246` prose says lowering returns an operation plan of commands. Its struct
sketch uses `NonEmpty<Command>`. Some earlier discussion implied operations
may lower to zero commands.

The current code chooses `NonEmpty<Command>`. That is probably the cleaner v1
choice because every accepted operation should have an executable witness, but
the design should say that explicitly:

- If an operation is a no-op, it should still lower to an explicit command
  such as `ValidateAlreadyCurrent`, `ReadCurrentState`, or `RecordNoChange`.
- If true zero-command operations are allowed, `OperationPlan` cannot be
  `NonEmpty`.

I recommend keeping `NonEmpty` and making the no-op-as-explicit-command rule
part of the executor contract.

## Macro Contradiction In /246

`/246` has one internal contradiction that matters for implementation.

The top-level TLDR says:

- observable contracts must use standardized `Tap` / `Untap`;
- persona components do not choose their observer open/close verbs.

But later text still includes the older grammar:

```rust
observable {
    open Watch(LedgerObserverFilter);
    close Unwatch;
    filter default;
    event OperationReceived;
    event SemaEffectEmitted;
}
```

and says each contract picks verbs that fit its domain.

The current locked macro work appears to be moving toward the newer
`Tap`/`Untap` direction, because `ObservableBlockSpec` no longer has
`open_verb` and `close_verb`. That means the old examples in `/246` are stale.

Implementation should follow the TLDR:

```rust
observable {
    filter default;
    operation_event OperationReceived;
    effect_event SemaEffectEmitted;
}
```

and the macro should inject `Tap` and `Untap`.

## Recommended Landing Order

1. Fix `signal-frame-macros` compile errors under the `/246` macro shape.
   `emit.rs` and validation must stop reading `open_verb` and `close_verb`,
   and must resolve `FilterDecl` to a concrete generated or named type before
   quoting.

2. Finish `signal-frame` reply metadata:
   - add `RetryClassification`;
   - add `CommitStatus`;
   - add `BatchFailureReason::EngineUnavailable`;
   - expand `AcceptedOutcome::BatchAborted` and `Reply::batch_aborted`.

3. Commit and push `signal-frame`, then update `signal-executor`'s
   `signal-frame` dependency lock.

4. Finish `signal-executor` v4:
   - add `type ComponentEffect` to `Lowering`;
   - change `SemaEngine` to return component effects;
   - introduce the projection trait from command/effect into Sema
     observation;
   - add an engine-error classification trait.

5. Only after both crates are green, move to the repository-ledger pilot.
   The pilot should be the worked example that proves contract operation →
   command plan → component effects → Sema observation → typed reply.

## Questions That Need Design Attention

1. Should `OperationPlan` remain `NonEmpty<Command>`?

   My recommendation: yes. If a public operation is accepted, it should produce
   at least one explicit command. This keeps every operation visible to the
   executor and introspection layer. No-op should be a named command, not an
   empty plan.

2. What exactly maps `ComponentEffect` into a universal Sema effect?

   Resolved by `reports/designer/253-tosemaoutcome-trait-shape.md`: use the
   two-trait shape. `Command` implements `ToSemaOperation`; `ComponentEffect`
   implements `ToSemaOutcome`; `signal-sema` owns `SemaOutcome` and
   `SemaObservation`.

3. Is `Tap` / `Untap` now fully settled?

   The implementation appears to be headed there, and I think that is the
   correct persona-wide shape. If so, the stale `open Watch` / `close Unwatch`
   examples in `/246` should be treated as historical residue, not as
   implementation guidance.

4. Should engine errors that happen after acceptance ever become
   `Reply::Rejected`?

   My recommendation: no. Once the frame is accepted and lowering begins, the
   reply should remain `Reply::Accepted` with `BatchAborted`. `Reply::Rejected`
   is only for pre-acceptance frame/kernel failure.
