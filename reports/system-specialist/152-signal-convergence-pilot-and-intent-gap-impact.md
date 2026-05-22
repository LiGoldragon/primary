# signal convergence, pilot, and intent-gap impact

> Superseded on pilot sequencing by
> `reports/system-specialist/153-signal-refresh-144-system-impact.md`.
> The repo-split and three-layer conclusions still stand; the
> repository-ledger-first pilot recommendation is no longer current after
> `reports/operator/144-signal-sema-executor-refresh-2026-05-20.md` and
> `reports/designer/254-signal-executor-sema-refresh-audit.md`.

## Scope

This report incorporates:

- `reports/operator/143-signal-infrastructure-convergence-and-pilot-pivot.md`
- `reports/designer/249-component-intent-gap-analysis.md`
- the three-layer-changes-for-operators design (since dropped;
  substance now in `skills/contract-repo.md` and
  `skills/component-triad.md`)

It updates the system-specialist view from:

- `reports/system-specialist/151-signal-executor-246-impact.md`

## Current conclusion

The Signal foundation direction is converging, not reopening.

Keep the repo split:

| Repo / layer | Stays because |
|---|---|
| `signal-frame` | wire envelope, reply shape, stream token/fanout primitives, macro |
| `signal-executor` | lowering orchestration, batch planning, operation/batch abort semantics, observed-lowering projection calls |
| `signal-sema` | payloadless Sema classification vocabulary and shared primitives |
| `signal-*` contracts | public operation/reply/event/filter vocabulary |
| daemons | policy, component commands, command execution, projection, socket delivery |

Do not replace this with a single runtime crate. Do not move contract
execution into `sema-engine`. Do not migrate to a third-party IPC stack.
The next proof is a real daemon pilot, not another broad architecture
rewrite.

## What `/248` changes for `lojix`

`lojix` should follow the three-layer model only after the foundation
bundle lands:

1. `signal-sema::SemaOperation` becomes payloadless classification.
2. `signal-executor::Lowering` gets `Command` and `ComponentEffect`.
3. `OperationPlan` / `BatchPlan` carry structural ownership.
4. `CommandExecutor` executes component-local commands atomically.
5. `AcceptedOutcome` distinguishes `Committed`, `OperationAborted`,
   and `BatchAborted`.
6. `ObservedLowering` projects typed component values into observer
   event records.
7. `signal-frame` emits standardized `Tap` / `Untap` for observable
   contracts.

For `lojix`, the Layer 2 command enum belongs in `lojix-daemon`, not
`signal-lojix`:

```rust
enum DeploymentCommand {
    RecordSubmission(SubmissionRecord),
    QueryGeneration(GenerationSelection),
    RecordBuildEvent(BuildEvent),
    MarkGenerationCurrent(GenerationIdentity),
}
```

`signal-lojix` stays Layer 1: public contract operations such as
`Submit`, `Query`, and maybe deployment-domain stream verbs. The
payloadless `SemaOperation` projection exists only for observation and
introspection.

## What `/143` changes in sequencing

The immediate target is no longer "migrate `signal-lojix` as soon as
the foundation compiles." The target is:

```text
finish small foundation convergence bundle
→ repository-ledger pilot
→ observer subscribe/effect proof
→ only then move the pattern into persona-spirit/persona-mind
→ only then resume `signal-lojix` migration with confidence
```

The pilot must prove:

- a real daemon receives a contract operation;
- lowering produces typed component command plans;
- typed per-operation replies cross the wire;
- domain rejection and engine/batch failure are distinguishable;
- observer subscription sees operation and effect events;
- no dependency boundary is inverted to make the flow work.

This matters to system work because `lojix` is deploy infrastructure.
It should not be the proving ground for unstable Signal mechanics. It
should consume the proven shape after `repository-ledger` has forced
the real daemon path.

## What `/249` changes in confidence

`/249` does not contradict the three-layer model. It changes how
strongly we should treat adjacent Persona assumptions.

The heavily backed intent:

- contract-local verbs;
- the three-layer model;
- `Tap` / `Untap` mandatory for Persona observability;
- spirit/mind cognitive direction;
- LLM mediation in Persona.

The weakly backed or still-open areas:

- whether `Tap` / `Untap` exactly *is* the universal observer hook the
  psyche intended, or an implementation of that intent;
- what `persona-introspect` is beyond being the observer consumer;
- the top-level `persona` engine-manager status as a triad component;
- supervisor identity in the authority graph;
- owner-signal emergence criteria for missing owner contracts;
- spawn order beyond "spirit last."

The system-specialist consequence: do not let those Persona-specific
uncertainties leak into `lojix` or CriomOS as if they were settled
platform rules. For `lojix`, use the Signal mechanics once proven, but
avoid inheriting Persona engine-manager assumptions.

## Practical guidance

For Signal foundation work:

- follow `skills/contract-repo.md` §"Public contracts use contract-
  local operation verbs" and `skills/component-triad.md` (the
  three-layer-changes substance now codified there) for crate-by-
  crate implementation;
- treat `reports/operator/143-signal-infrastructure-convergence-and-pilot-pivot.md`
  as the sequencing rule;
- treat `reports/designer/249-component-intent-gap-analysis.md` as a
  confidence map: it tells us where to avoid overclaiming intent.

For `signal-lojix` / `lojix`:

- do not migrate before the foundation bundle and repository-ledger
  pilot are proven;
- keep `signal-lojix` as Layer 1 public vocabulary;
- define deployment `Command` and `ComponentEffect` types inside
  `lojix-daemon`;
- project deployment commands to `SemaOperation` only for observation;
- keep user-facing deployment progress streams separate from the
  introspection `Tap` / `Untap` surface if `lojix` exposes one.

## Current posture

No code changes from this report. Active operator locks cover the
Signal foundation code. This report updates system-specialist
sequencing so the `lojix` rewrite waits for the repository-ledger
pilot rather than becoming the first full proof of the new Signal
executor model.
