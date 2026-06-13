# lojix S4 recon — deploy pipeline, activation stub, closure-threading seam

Read-only reconnaissance for the S4 work: make the daemon actually
copy + activate a real closure, and make a deploy survive SSH
disconnect (Spirit `up9q`). Repo: `/git/github.com/LiGoldragon/lojix`
at `main` (`196ab501` — "lojix: durable sema-engine state plane +
self-resume"). All citations are `path:line`. Nothing was mutated.

## The deploy effect chain (continuation hops)

A single owner `Deploy` signal becomes a chain of effect + sema-write
continuations threaded by the `DeployPipeline` cursor
(`src/schema_runtime.rs:101-124`). The runner alternates between
`decide_effect_completion` (which fires the next `EffectCommand`) and
`record_phase` → `advance_after_phase` (which records a durable phase
then fires the following effect). `decide` is the routing brain
(`schema_runtime.rs:2001-2013`).

The actual hop order, traced through the code (not the doc-comment,
which is slightly stale):

1. `decide_meta_input` (`512`) runs the reject-guard
   (`unsupported_deploy_reason`, `559`), then routes
   `RecordDeploySubmitted` to the sema engine.
2. `decide_write_completion` → `begin_deploy_pipeline` (`636`) fires
   the first effect: `ResolveFlakeAuth` (`643`).
3. `decide_effect_completion` `FlakeResolved` (`818`): if the deploy
   needs the horizon override (no `build_attribute`,
   `needs_horizon_materialization` `287`) it fires
   `MaterializeHorizon`; otherwise records phase `Building`.
4. `HorizonMaterialized` (`829`): stores input overrides, records
   phase `Building`.
5. The `Building` phase write hops back through `advance_after_phase`
   (`648`), stage `Submitted → BuildingRecorded`, firing `NixEval`
   (`663`).
6. `ClosureEvaluated` (`833`): stores the drv path, and if the action
   `produces_closure()` (`159`) fires `NixBuild` (`836`); a System
   `Eval` finishes here.
7. `ClosureBuilt` (`845`): stores the built closure path, and if the
   action `activates()` (`169`) fires `CopyClosure` (`848`); a `Build`
   action finishes here (the realised closure is the result).
8. `ClosureCopied` (`858`): records phase `Copying`.
9. The `Copying` write hops through `advance_after_phase`, stage
   `BuildingRecorded → CopyingRecorded`, firing `ActivateGeneration`
   (`669`).
10. `GenerationActivated` (`863`): records phase `Activated`.
11. The `Activated` write hops, stage `CopyingRecorded →
    ActivatedRecorded`, firing the sema write
    `RecordGenerationActivated` (`675`) — the live-set + gc-roots commit
    (`activation_commit`, `366`).
12. `GenerationActivated` sema completion → `finish_deploy_pipeline`
    (`689`) replies `Deployed`.

`run_effect` (`1974`) dispatches each `EffectCommand` to its async IO
body; all of them shell out through `NixCommand` + `tokio::process`
(below).

## The `run_effect` bodies (NixBuild / CopyClosure / ActivateGeneration)

`run_nix_build` (`schema_runtime.rs:1359-1384`):

```rust
let invocation = match &command.target {
    nexus::BuildTarget::Local => {
        NixCommand::build_closure(command.closure_path.payload(), &command.substituters)
    }
    nexus::BuildTarget::Remote(builder) => NixCommand::build_closure_remote(
        builder.payload().payload(),
        command.closure_path.payload(),
        &command.substituters,
    ),
};
match invocation.run().await {
    Ok(output) => nexus::EffectResult::ClosureBuilt(nexus::BuiltClosure {
        generation_identifier: command.generation_identifier,
        closure_path: ordinary::ClosurePath::new(NixCommand::first_line_or(
            &output,
            command.closure_path.payload(),
        )),
    }),
    Err(detail) => Self::effect_failed(nexus::EffectStage::Build, detail),
}
```

`run_copy_closure` (`1386-1398`):

```rust
match NixCommand::copy_closure(command.node_name.payload(), command.closure_path.payload())
    .run()
    .await
{
    Ok(_) => nexus::EffectResult::ClosureCopied(nexus::CopiedClosure {
        generation_identifier: command.generation_identifier,
        node_name: command.node_name,
        closure_path: command.closure_path,
    }),
    Err(detail) => Self::effect_failed(nexus::EffectStage::CopyClosure, detail),
}
```

`run_activate_generation` (`1400-1416`):

```rust
let slot = Self::activation_slot(&command.activation_kind);
match NixCommand::activate_system(command.node_name.payload())
    .run()
    .await
{
    Ok(_) => nexus::EffectResult::GenerationActivated(nexus::ActivatedGeneration {
        generation_identifier: command.generation_identifier,
        node_name: command.node_name,
        generation_slot: slot,
    }),
    Err(detail) => Self::effect_failed(nexus::EffectStage::Activate, detail),
}
```

## The closure-path bug — root cause and exact fix

`nix build --print-out-paths` is built by `NixCommand::build_closure`
(`1817`) / `build_closure_remote` (`1828`). Its stdout (the realised
`/nix/store/...` out-path) lands in `BuiltClosure.closure_path` via
`first_line_or` (`1377`). The pipeline correctly captures it: the
`ClosureBuilt` arm calls `set_closure_path` (`846`, `874`), storing it
on `pipeline.closure_path`.

`CopyClosure` is fine — `copy_closure_command` (`345`) threads the
built `closure_path` into `CopyClosureCommand` (which has a
`ClosurePath` field, `nexus.rs:178-183` / `schema/nexus.schema:66`),
and `run_copy_closure` copies that exact path.

`ActivateGeneration` is the broken seam. `ActivateGenerationCommand`
(`nexus.rs:188-193`, `schema/nexus.schema:67`) carries
`GenerationIdentifier * ClusterName * NodeName * ActivationKind` and
**no `ClosurePath`** — so `activate_generation_command` (`357`) has no
closure to pass. The activation shell command
`NixCommand::activate_system` (`1898-1908`) therefore references an
**unset** shell variable:

```rust
fn activate_system(node_name: &str) -> Self {
    Self::new("ssh", vec![
        node_name.to_string(),
        "nix-env -p /nix/var/nix/profiles/system --set \"$CLOSURE\"".to_string(),
    ])
}
```

`$CLOSURE` is never exported anywhere — the remote shell expands it to
empty, so `nix-env --set ""` fails (or, worse, mis-sets the profile).
It also stops at `nix-env --set` and never runs
`switch-to-configuration <kind>`, so even with a real path the
generation is set but not activated by `ActivationKind`.

**Exact fix (schema-first, no back-compat needed pre-production):**

1. Add `ClosurePath` to `ActivateGenerationCommand` in
   `schema/nexus.schema:67` (becomes
   `{ GenerationIdentifier * ClusterName * NodeName * ClosurePath * ActivationKind * }`),
   regenerate `src/schema/nexus.rs`.
2. `activate_generation_command` (`357`) takes the built closure (the
   already-stored `pipeline.closure_path`, or thread `built.closure_path`
   from the `ClosureBuilt` arm the same way `copy_closure_command`
   already does at `848-849`).
3. `activate_system` becomes `activate_system(node_name, closure_path,
   activation_kind)` and substitutes the real store path inline instead
   of `$CLOSURE`, then runs the kind-appropriate
   `switch-to-configuration` (`switch`/`boot`/`test`) — e.g.
   `nix-env -p /nix/var/nix/profiles/system --set <path> &&
   <path>/bin/switch-to-configuration <kind>`. `activation_slot`
   (`1418`) already maps `ActivationKind → GenerationSlot`; mirror that
   mapping into the switch sub-command.

This makes copy + activate target-safe: copy already sends the real
built path; activate then sets and switches that same path on the
target.

## The reject-guard matrix (what is accepted vs rejected today)

`unsupported_deploy_reason` (`schema_runtime.rs:559-575`):

| Request | Action / mode | Today |
|---|---|---|
| System | `Eval` | accepted (drv path only, no closure) |
| System | `Build` | accepted (realised closure, stops before copy) |
| System | `Switch`/`Boot`/`Test`/`BootOnce` | **rejected** `UnsupportedDeployAction` |
| Home | `Build` | accepted (closure, stops before copy/activate) |
| Home | `Profile`/`Activate` | **rejected** `UnsupportedDeployAction` |

Rejected = exactly the `activates()` set (`169`). The guard rejects
copy/activate because activation is not target-safe (the `$CLOSURE`
bug) and accepting it would write false live-set state.

The lock test is `tests/engine_routing.rs:167-180`
`activating_deploy_is_rejected_until_activate_lands`: a System `Switch`
with a `build_attribute` must reply
`DeployRejectionReason::UnsupportedDeployAction`. Sibling tests confirm
the now-open paths reach the pipeline:
`production_deploy_without_build_attribute_enters_effect_pipeline`
(`182`, System `Build`) and `home_build_enters_effect_pipeline`
(`194`) both expect `ProposalSourceUnreachable` — i.e. they pass the
guard and fail only at the real `nix`/source IO with bogus fixtures.

**What opens once activate is real:** flip `unsupported_deploy_reason`
so `Switch`/`Boot`/`Test`/`BootOnce` and Home `Profile`/`Activate` are
`supported`. The pipeline machinery (stages, phase records, the
`activates()` branch firing `CopyClosure` → `ActivateGeneration`) is
already wired and waiting; only the guard and the activate command
shape block it. Update the lock test from "rejected" to "enters
pipeline" alongside the guard change.

## How nix commands are built / run, and target plumbing

`NixCommand` (`schema_runtime.rs:1766-1955`) is a typed
`{ program, arguments }` value; `run()` (`1917`) spawns via
`tokio::process::Command`, captures stdout on success or a formatted
stderr detail on failure. Each effect awaits its child directly inside
the actor-native request task — no blocking-pool bridge
(`actor_native_runtime.rs` asserts `async fn run_effect`, no
`spawn_blocking`). Constructors:
`flake_metadata` (`1780`), `eval_drv_path` (`1792`, `--refresh --raw
<attr>.drvPath`), `build_closure` (`1817`), `build_closure_remote`
(`1828`), `copy_closure` (`1886`), `activate_system` (`1898`),
`collect_garbage` (`1910`).

Target / builder / substituter plumbing:
- **Remote builder** — `BuildTarget::Remote(BuilderNode)`
  (`nexus.rs:79-82`) from `pipeline.build_target()` (`273`);
  `build_closure_remote` passes `--builders ssh-ng://<builder>`
  (`1838`).
- **Substituters** — `ExtraSubstituter { url, public_key }`
  (`nexus.rs:87`) → `--option extra-substituters / extra-trusted-public-keys`
  (`substituter_options`, `1849`).
- **Copy / activate target** — `copy_closure` (`1886`) sends
  `nix copy --to ssh-ng://<node_name>`; `activate_system` (`1898`) and
  `collect_garbage` (`1910`) `ssh <node_name> ...`. NB: the target is
  the bare `NodeName`, not a resolved reachable address — a second
  target-safety gap beyond `$CLOSURE` (the `se72` routed-microVM
  validation will need a real address, e.g. the node's Criome domain /
  ygg address, per INTENT.md:94-97).

## SSH-disconnect survival (Spirit `up9q`) — current reality vs intent

INTENT.md:82-86 states the design intent: "A durable deploy is owned
by a job actor that owns the external process and persists job state;
process lifetime is decoupled from the request stream, so a dropped
client does not abort the deploy." **None of that exists yet.**

Today the entire pipeline runs synchronously inside the owner
connection handler. `RequestWorker::serve_owner` (`daemon.rs:275-290`)
reads one request frame, then `execute_request` →
`execute_with_store` (`321-338`) awaits the *full* `NexusEngine::execute`
continuation loop (eval → build → copy → activate → record) and only
then writes the single reply frame back on the same stream. The
client (the CLI, run inside an SSH session) blocks on `read_body` for
that one reply (`build_smoke.rs:352-359`). If the owner client
disconnects, the per-connection Tokio task
(`handle_connection`, `223-235`, one task per accepted connection) is
dropped and the in-flight deploy dies with its `tokio::process`
children. There is no detach, no `systemd-run --collect` transient
unit, no persisted job state, no resume-mid-pipeline. Only the *final*
committed state self-resumes (`durable_resume.rs`); a deploy
interrupted mid-pipeline leaves only whatever phase rows were already
written and cannot continue.

**The seam to make the deploy survive disconnect:** decouple pipeline
execution from `serve_owner`. The owner request should record the
submission, spawn/own a durable job actor (the closure of the current
`execute_with_store` continuation loop) that outlives the connection,
reply immediately with an accepted-job handle, and persist job/phase
state so a daemon restart (or client reconnect via the existing
`WatchDeployments` subscription, INTENT.md:59-63) resumes/observes it.
The `DeployStage` cursor + durable phase records
(`schema_runtime.rs:131-142`) are the persistence substrate to build
on; the missing piece is an owning job actor whose lifetime is the
daemon's, not the connection's.
