# lojix signal migration vision

## Scope

This is the starting report for migrating the **new** `lojix` stack:

- `/home/li/wt/github.com/LiGoldragon/signal-lojix/horizon-leaner-shape`
- `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape`

It does not concern production `lojix-cli` on `main`.

The migration target is the landed Signal shape from:

- `reports/operator/144-signal-sema-executor-refresh-2026-05-20.md`
- `reports/designer/254-signal-executor-sema-refresh-audit.md`
- `reports/system-specialist/153-signal-refresh-144-system-impact.md`

The model:

```text
signal-lojix contract operation
-> lojix-daemon component command
-> signal-sema payloadless classification observation
```

## Current reading

`signal-lojix` is already partly migrated. Its source declares
contract-local operation roots through `signal_frame::signal_channel!`:

```text
Deploy
Pin
Unpin
Retire
Query
WatchDeployments / UnwatchDeployments
WatchCacheRetention / UnwatchCacheRetention
```

That is the right public vocabulary direction. But its
`ARCHITECTURE.md` and `skills.md` still contain stale
`signal-core`, `SignalVerb`, `Assert`, `Mutate`, `Match`,
`Subscribe`, and `Retract` wording. The first task is to make the
docs and tests agree with the actual contract-local source.

`lojix` is not migrated yet. It still depends on `signal-core`, imports
`SignalVerb`, handles `Operation<wire::Request>`, builds
`CoreReply::completed(...)`, and dispatches directly from wire request
variants to daemon behavior. There is no `signal-executor` lowering
layer and no `LojixCommand` / `LojixEffect` language yet.

`lojix` also still has the earlier deployment-identity smell:

```text
DeploymentLedger::allocate_deployment()
-> DeploymentId::from_text(format!("deployment_{}", key.value()))
```

That should be retired during the migration, not preserved.
Infrastructure mints identity through typed slots/keys; an agent-facing
string format is at most an output projection.

## Desired end shape

### Contract layer: `signal-lojix`

`signal-lojix` owns only Layer 1:

- public deployment operations;
- typed deployment/cache/generation payload records;
- typed replies;
- pushed deployment/cache observation event records;
- startup configuration records;
- canonical deployment request digest helpers.

It should not depend on `signal-sema`, and it should not expose the six
Sema words as public request roots. It should also not retain
`SignalVerb` compatibility shims once `lojix` consumes the
`signal-frame` shape.

### Command layer: `lojix-daemon`

`lojix-daemon` owns Layer 2:

```rust
enum LojixCommand {
    AllocateDeployment,
    RecordDeploymentSubmitted(...),
    AuthorizeDeployment(...),
    ProjectHorizon(...),
    StageGeneratedInputs(...),
    RunBuild(...),
    RecordBuildStarted(...),
    RecordBuildFinished(...),
    RecordDeploymentFailed(...),
    QueryGenerations(...),
    PinGeneration(...),
    UnpinGeneration(...),
    RetireGeneration(...),
    OpenDeploymentWatch(...),
    CloseDeploymentWatch(...),
}
```

The exact names should be refined while editing, but the rule is
settled: every accepted operation lowers to a non-empty typed command
plan. No-op, idempotent, validation, and currently-unimplemented
accepted paths still lower to named commands with explicit `NoChange`
effects.

### Sema classification layer

Each `LojixCommand` implements `ToSemaOperation`:

```text
record new deployment fact -> Assert
transition deployment/generation state -> Mutate
close watch / retire durable fact -> Retract
query generations -> Match
open watch -> Subscribe
dry-run validation -> Validate
```

Each command effect implements `ToSemaOutcome`. The projection exists
for observation and introspection. It is not the executable language of
the daemon.

## Important split: durable commands vs external effects

`lojix` has harder effects than the counter fixture or spirit:

- Criome authorization;
- Horizon projection;
- generated Nix inputs;
- SSH/rsync transfer;
- Nix build/store import;
- GC root mutation;
- activation;
- future Arca and dynamic cache coordination.

Those must not be hidden inside one blocking command executor. The
migration should separate:

1. **Admission and durable state commands** — execute atomically through
   sema-engine where possible, with `BatchErrorClassification` on
   engine errors.
2. **Effect workflow commands** — actor-owned, timeout-bounded, and
   observed as state transitions. They write durable observations before
   and after effects; they do not block the socket acceptor or observer
   fanout.

The first working migration should therefore wrap the existing actors
rather than flattening them into `signal-executor`. `signal-executor`
coordinates the request/reply and observation shape; Kameo actors still
own long external effects.

## Migration order

### 1. Stabilize `signal-lojix`

- Finish or verify the current contract-local verb migration.
- Remove stale `signal-core` / `SignalVerb` / Sema-verb docs.
- Ensure tests assert the absence of `SignalVerb` and the presence of
  contract-local operation roots.
- Push the branch before touching `lojix`, so the implementation crate
  can update its lock to a real commit.

### 2. Move `lojix` wire dependency to `signal-frame`

- Replace direct `signal-core` imports with `signal-frame` equivalents.
- Update frame/reply/socket code to the current generated
  `signal-lojix` channel types.
- Preserve the CLI invariant: exactly one peer, `lojix-daemon`.
- Preserve pushed deployment observation streams while changing frame
  plumbing.

### 3. Introduce `LojixCommand` and `LojixEffect`

- Add internal command/effect types in `lojix`, not `signal-lojix`.
- Move `RuntimeRoot` away from matching directly on public request
  variants.
- Add a lowering type that converts each `LojixOperation` into
  `OperationPlan<LojixCommand>`.
- Add explicit no-change commands for unimplemented accepted paths if
  any remain.

### 4. Integrate `signal-executor`

- Use `Lowering` / `CommandExecutor` where the command batch is durable
  and atomic.
- Implement `BatchErrorClassification` for `lojix` engine errors.
- Keep external effects actor-owned; command execution records and
  observes the workflow rather than blocking inside a mailbox.

### 5. Repair identity and ledger shape

- Replace `deployment_{n}` and `generation_{n}` projection as the
  internal identity model.
- Use sema-engine slot/key identity as the source of truth.
- Keep human-readable IDs only as output projection if needed.

### 6. Split `deploy.rs`

The current `src/deploy.rs` is the complexity center. Split by noun
while migrating:

- `deploy/ledger.rs`
- `deploy/identity.rs`
- `deploy/watch.rs`
- `deploy/build_job.rs`
- `deploy/generated_inputs.rs`
- `deploy/garbage_collection_roots.rs`
- `deploy/remote_inputs.rs`
- `deploy/secrets.rs`

This is not cosmetic. The command/effect migration will otherwise land
inside a 2k-line file and make the next migration harder.

### 7. Nix witnesses

Each stage needs a Nix-backed witness:

- `signal-lojix-has-no-signal-verb-surface`
- `lojix-cli-has-exactly-one-signal-peer`
- `lojix-cli-cannot-open-horizon-or-sema`
- `lojix-every-operation-lowers-to-non-empty-command-plan`
- `lojix-domain-rejection-is-operation-aborted-not-frame-rejected`
- `lojix-engine-failure-is-batch-aborted-with-classification`
- `lojix-watch-stream-pushes-current-state-then-events`
- `lojix-deployment-identity-is-minted-by-sema`
- `lojix-effect-actor-cannot-block-socket-acceptor`

Pure source checks are acceptable for boundary absence. Runtime paths
need binary-level Nix checks using the packaged daemon and CLI.

## Current risks

1. `signal-lojix` has a described working-copy change on the
   `horizon-leaner-shape` worktree. Before editing it, confirm whether
   that change is peer-owned or finish/push it as the first migration
   commit.

2. `lojix` and `signal-lojix` currently disagree at the dependency
   boundary: `signal-lojix` source is on `signal-frame`; `lojix` still
   imports `signal-core`. That is the first compile break to expect.

3. A naive migration could move Nix builds and activation into a
   generic executor and block daemon responsiveness. Keep those effects
   in actor planes.

4. The old stream code uses `SignalVerb::Subscribe` to build stream
   replies. The new contract-local stream close/open grammar must drive
   that reply shape without reintroducing universal Sema verbs.

## Open questions

1. For the first `lojix` migration pass, should deployment-domain
   streams remain the only streams, or should `lojix` also declare a
   universal observer block immediately?

2. Should `Deploy` remain one broad public operation carrying a
   `DeploymentPlan`, or should the public contract split into `Build`,
   `Activate`, `Deploy`, and `Rollback` before the command-layer work?
   My preference is to keep `Deploy` until activation/rollback semantics
   are real enough to deserve public verbs.

3. Should identity projection expose short human-readable handles at
   all, or should the CLI render sema-backed slots directly? My
   preference is sema identity as truth, optional readable projection
   only in replies.

## Next action

Claim both worktree paths under `system-specialist`, settle the
`signal-lojix` dirty working-copy ownership, and start with the
contract/docs/test cleanup before editing `lojix`.

