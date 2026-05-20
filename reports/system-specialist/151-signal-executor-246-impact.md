# signal executor /246 impact on the system-specialist design

## Scope

This report updates the system-specialist migration view after reading:

- `reports/designer/246-v4-bundled-fix-deep-design-with-examples.md`
- `reports/designer/248-three-layer-changes-for-operators.md`
- `reports/operator/142-signal-frame-executor-bundled-fix-logic-probe.md`
- `reports/operator/143-signal-infrastructure-convergence-and-pilot-pivot.md`

It supersedes the active guidance in:

- `reports/system-specialist/150-signal-frame-executor-141-migration-start.md`

where that report still reflects `/141` rather than the v4 bundled
fix.

## Short conclusion

`/246` is the better design. It is not merely a refinement of `/141`;
it changes the load-bearing model to three layers:

| Layer | What it means | Owner |
|---|---|---|
| Contract Operation | public wire action | `signal-<component>` |
| Component Command | typed executable daemon command | component daemon |
| Sema Operation | payloadless state-action classification | `signal-sema` |

This is the right shape for `lojix` too. Deployment commands are not
Sema operations. A `lojix` daemon command can carry the deployment
record, build plan, generation query, cache retention update, or
activation transition. That command then projects to a payloadless Sema
class such as `Assert`, `Match`, or `Mutate` for observation.

## What changes from my previous report

### 1. Lowering returns `OperationPlan<Command>`

My `/150` note used the `/141` shape:

```rust
fn lower(&self, operation: &Self::Operation)
    -> Result<Vec<Self::Command>, Self::Reply>;
```

The current shape is:

```rust
fn lower(&self, operation: &Self::Operation)
    -> Result<OperationPlan<Self::Command>, Self::Reply>;
```

One `OperationPlan` belongs to one source operation. The executor
assembles those into a `BatchPlan`. That structural ownership replaces
the owner-index sidecar idea.

### 2. Engine failure is `BatchAborted`

`/141` left engine failure close to kernel rejection. `/246` and the
operator logic probe correct that.

Current rule:

- malformed frame, decode failure, version failure:
  `Reply::Rejected`;
- domain lowering rejection:
  `Reply::Accepted` with `AcceptedOutcome::OperationAborted`;
- engine or command-executor batch failure:
  `Reply::Accepted` with `AcceptedOutcome::BatchAborted`.

`BatchAborted` carries generic execution metadata:

```rust
BatchAborted {
    reason: BatchFailureReason,
    retry: RetryClassification,
    commit: CommitStatus,
}
```

That is useful for `lojix`: a build/deploy caller can learn whether
the failure is retryable and whether commit status is known without
receiving daemon-private engine errors.

### 3. Observation uses `ObservedLowering` and `ObserverFanout`

My `/150` note proposed a standalone `ObservationProjection` bridge.
The current shape is better:

```rust
pub trait ObservedLowering: Lowering {
    type OperationEvent;
    type EffectEvent;

    fn project_operation(&self, operation: &Self::Operation)
        -> Self::OperationEvent;

    fn project_effect(&self, effect: &Self::ComponentEffect)
        -> Self::EffectEvent;
}
```

`signal-frame` owns the generic fanout:

```rust
pub trait ObserverFanout<OperationEvent, EffectEvent> {
    fn publish_operation(&mut self, event: OperationEvent);
    fn publish_effect(&mut self, event: EffectEvent);
}
```

This keeps dependencies clean:

- `signal-frame` never mentions `signal-executor::SemaEffect`;
- `signal-executor` owns execution ordering and projection calls;
- contract crates own event record types;
- daemons own how component effects become event records.

### 4. Persona observability standardizes on `Tap` / `Untap`

`/141` and my `/150` note preferred contract-authored observer verbs
such as `Watch` / `Unwatch`. `/246` supersedes that for persona
components: observable contracts use standardized `Tap` / `Untap`.

This means domain streams should keep domain verbs such as
`WatchDeployment` only if the domain really needs them. The universal
introspection surface is `Tap` / `Untap`.

For `lojix`, I would apply the same separation even though it is not a
Persona component:

- deployment-domain streams: domain vocabulary, for user-visible deploy
  progress;
- introspection streams: `Tap` / `Untap`, if `lojix` exposes the
  universal observer hook.

### 5. `signal-lojix` should wait longer

My previous "do not migrate `signal-lojix` until foundation settles"
still stands, but the checklist changes.

Do not migrate `signal-lojix` until these are landed:

1. `signal-sema::SemaOperation` is payloadless classification.
2. `ToSemaOperation` exists for component commands.
3. `signal-executor::Lowering` has `Command` and `ComponentEffect`.
4. `OperationPlan` / `BatchPlan` exist.
5. `CommandExecutor` exists.
6. `AcceptedOutcome` has `Committed`, `OperationAborted`, and
   `BatchAborted` with retry/commit metadata.
7. `ObservedLowering` and `ObserverFanout` exist.
8. `signal-frame` observable grammar emits `Tap` / `Untap`.
9. The repository-ledger pilot proves the whole path.

## Inconsistency in `/246`

`/246` has a few stale examples that still show older
`open Watch(...)` / `close Unwatch;` observable grammar. I read those
as stale examples because `/246` §0, §2, and `reports/designer/248`
all say v4 uses standardized `Tap` / `Untap` and drops author-chosen
open/close verbs.

If another agent implements from `/246`, the safer companion is
`reports/designer/248-three-layer-changes-for-operators.md`, which
states the crate-by-crate v4 diff more cleanly.

## System-specialist consequence for `lojix`

`lojix` should define deployment-specific Layer 2 commands in the
daemon, not in `signal-lojix`:

```rust
enum DeploymentCommand {
    RecordSubmission(SubmissionRecord),
    QueryGeneration(GenerationSelection),
    RecordBuildEvent(BuildEvent),
    MarkGenerationCurrent(GenerationIdentity),
}
```

Those commands execute through a `CommandExecutor` against the
daemon's durable store and effect actors. They project to
`SemaOperation` only for classification:

```rust
impl ToSemaOperation for DeploymentCommand {
    fn to_sema_operation(&self) -> SemaOperation {
        match self {
            Self::RecordSubmission(_) => SemaOperation::Assert,
            Self::QueryGeneration(_) => SemaOperation::Match,
            Self::RecordBuildEvent(_) => SemaOperation::Assert,
            Self::MarkGenerationCurrent(_) => SemaOperation::Mutate,
        }
    }
}
```

This keeps `signal-lojix` clean: public operations like `Submit` and
`Query` remain contract-domain verbs; executable deployment details
stay inside `lojix-daemon`; Sema remains an observation vocabulary.

## Current code posture

I did not edit `signal-frame`, `signal-executor`, or `signal-lojix`.
The Signal foundation repos are active under operator-side locks, and
the code migration is implementation-owned. This report updates the
system-specialist guidance so `lojix` does not migrate onto the
superseded `/141` shape.

