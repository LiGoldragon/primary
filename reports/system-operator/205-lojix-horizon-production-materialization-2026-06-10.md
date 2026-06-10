# lojix Horizon Production Materialization

## Frame

Psyche intent: the new `lojix` + Horizon stack should follow the overhauled production Spirit/core-crate pattern, become the next production deploy stack, and stop treating real CriomOS deploys as future unsupported shapes.

This session worked on production `lojix` main, not the old `horizon-leaner-shape` worktree. The older lean branch had useful materialization ideas, but its runtime shape predates the actor-native `triad-port` crate and should not be revived.

## Implemented

### Horizon materialization as Nexus effect

`lojix/triad-port/schema/nexus.schema` now names the production materialization step explicitly:

```text
HorizonMaterializationCommand
FlakeInputReference
FlakeInputOverride
MaterializedInputs
EffectCommand::MaterializeHorizon
EffectResult::HorizonMaterialized
EffectStage::MaterializeHorizon
```

`NixEvalCommand` now carries `overrides (Vec FlakeInputOverride)`, so generated flake inputs are data in the engine catalog, not hidden process-global state.

### Runtime path

For a deploy request with absent `build_attribute`, `lojix` now:

1. Resolves flake metadata.
2. Runs `MaterializeHorizon`.
3. Reads the request's `ProposalSource` as a `horizon-rs::ClusterProposal`.
4. Projects that proposal from `(cluster, node)` using `horizon-rs`.
5. Writes generated flake inputs under:

```text
<state-directory>/generated-inputs/<cluster>/<node>/<shape>/
```

6. Writes tiny flakes for:

```text
horizon
system
deployment
```

7. Hashes each directory with:

```text
nix hash path --type sha256 --sri
```

8. Passes `--override-input <name> path:<path>?narHash=<hash>` into `nix eval`.

### Guard change

The old guard rejected all production deploys without `build_attribute` as `UnsupportedDeployAction`. That is gone.

Current guard:

- System `Eval` and `Build`: allowed.
- Home `Build`: allowed.
- Activating actions (`Switch`, `Boot`, `Test`, `BootOnce`, Home `Profile`, Home `Activate`): still rejected.

Reason: copy/activate is still not target-safe. The existing activation code does not yet carry the closure path into the remote activation command, so accepting activation would risk false live-set state.

### Daemon config

`DaemonConfiguration` now includes:

```text
state_directory_path
```

The daemon turns that into the generated input root. Ignored daemon smoke tests were updated to pass the new field.

### Horizon dependency alignment

`horizon-rs` now declares `nota-next` with `branch = "main"`, matching the schema-derived signal crates. This fixed duplicate `nota-next` trait crates and made `lojix --all-features` compile again.

Committed in `horizon-rs`:

```text
9fae4a36 horizon-rs: align nota-next source with contracts
```

## Tests

`horizon-rs`:

```text
cargo test -p horizon-lib
```

Passed.

`lojix`:

```text
cargo fmt --all --check
cargo test --all-targets --all-features
cargo test --test engine_routing production_eval_materializes_horizon_inputs_and_returns_deployed -- --ignored --nocapture
cargo test --test build_smoke permissive_owner_socket_mode_is_refused -- --ignored
```

Passed.

The ignored materialization smoke is the important proof: it creates a tiny local flake and a generated cluster proposal, sends a production-style `System Eval` request with no `build_attribute`, runs real `nix flake metadata` + `nix eval`, and gets `Deployed` without building a closure.

## Remaining Blockers

### Activation is not production-safe yet

`CopyClosure` and `ActivateGeneration` still need a target-safe design. The current activation command shape does not pass the closure path into the remote command. Until this is fixed, activation must remain rejected.

### Secrets are not materialized yet

The implementation materializes `horizon`, `system`, and `deployment`. It does not yet materialize a `secrets` input from the cluster repository. Router or SOPS-dependent production nodes still need this before real full-system builds are production-ready.

### Build smoke is still eval-only

The new ignored live smoke proves materialization through eval. It does not build a CriomOS system closure. The next safe test should run remotely or with `--max-jobs 0` / builder dispatch, not on the laptop.

### SEMA durability remains in-memory

The docs previously claimed the daemon opens `sema-engine`; that was stale. I corrected the docs. The implementation still uses the in-memory shared store and needs the redb/sema-engine cutover before production daemon state is durable.

### Home build semantics need a real target

Home `Build` is now allowed into the effect pipeline, but it assumes the flake exposes:

```text
homeConfigurations.<user>.activationPackage
```

That is correct for `CriomOS-home`, not for the aggregate `CriomOS` flake. The CLI/operator surface needs to make the intended flake explicit per deploy kind.

## Production Readiness

The new `lojix` is materially closer to production:

- actor-native daemon runtime is intact;
- schema-derived Nexus/SEMA artifacts are refreshed;
- real production deploy shapes no longer stop at an unsupported guard;
- Horizon projection and generated flake input overrides work through a live Nix eval.

It is not ready to replace the current production stack for activating deployments. The next production-hardening sequence is:

1. Materialize `secrets`.
2. Make copy/activate target-safe and closure-path-carrying.
3. Add a remote full-system build smoke using the real CriomOS flake and test cluster.
4. Replace in-memory SEMA state with durable `sema-engine` storage.
5. Wire the daemon into CriomOS/Home only after the above pass.
