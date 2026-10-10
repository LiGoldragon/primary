# Lojix: realize the target closure in the target's own store

Read-only subflow of da88cf, 2026-09-26. Nothing was built, copied, or deployed. **W** = witnessed, **I** = inferred.

## What the code does today (lojix 8.0.0, main `f090da07`, `src/schema_runtime.rs`) (W)

- `eval_drv_path` (~7250, 7355): `nix eval --raw <attr>.drvPath` runs with no store flags. The deadlock comment covers **evaluation over ssh-ng only**. Commit `250c1e3` (2026-07-29) added it when it removed build-on-target. Lojix 0.3.9 had run the eval with `--store ssh-ng://…` and no `--eval-store auto`, so the evaluator wrote every `.drv` through the remote daemon. That is the transport `NON_IDEAL_AGENTS.md` says "can wedge while Nix and SSH wait on one another". The comment says nothing against building in a remote store from a `.drv` evaluated locally.
- `run_nix_build` (5225): `BuildTarget` (`src/runtime_flow.rs:107`) is now only `Local | Remote(builder)`. Both variants import outputs into ouranos. `ClosureCopy` (6146) then runs `nix copy --substitute-on-destination --to <nix_store_uri>`, but only when `activates()` is true. Realize runs no copy, so it fills only ouranos's store.
- History: lojix 0.3.5 (`fc9707b`) shipped build-on-target as `BuildTarget::TargetStore`, which made the copy a no-op. 0.3.8 (`860e99a`) hit "gguf.drv does not exist" and moved eval onto the target store. That eval move is what deadlocked (0.3.9, `664b618`). The design worked; the eval move broke it.
- The same shape was proven by hand on 2026-09-24 (`flows/d8df70/witnesses/prometheus-build-on-target.log`). `nix copy` of 4 `.drv`s to `ssh-ng://root@prometheus` took 4 s, then 3 derivations were built on Prometheus, followed by a test activation.
- Nix versions: ouranos and Prometheus both run **2.35.1** (W). Prometheus has `max-jobs=6`, `builders=` (empty), `substituters=cache.nixos.org`, `trusted-users` includes root, `keep-outputs`/`keep-derivations=true`, and 1015 G free. `--eval-store` and `copyDrvsFromEvalStore` have existed since Nix 2.4, so neither store needs anything new.

## Options

| | (a) `nix build --eval-store auto --store ssh-ng://root@T <attr or drv^*>` | (b) local eval → `nix copy --derivation --to ssh-ng://root@T <drv>` → `nix build --store ssh-ng://root@T <drv>^*` | (c) local eval → drv copy → `ssh root@T` runs `nix-store --realise` (detached unit) |
|---|---|---|---|
| Staged on ouranos | `.drv` closure only (already present after eval) | `.drv` closure only | `.drv` closure only |
| Model fixed-output derivations | already valid on T, so not fetched (W for the six paths); anything missing substitutes on T | same | same |
| Operator link | one ssh-ng session; Nix copies the drvs implicitly (I) | two ssh-ng calls: copy (seconds), then build (minutes, logs stream) | ssh only for starting and polling; the build survives a dropped link |
| GC root on T | none (a remote store gets no `--out-link`, I) | none from the build; one extra `ssh root@T nix-store --add-root /nix/var/nix/gcroots/lojix/<gen> -r <out>` needed | `--add-root` in the same command |
| Pipeline fit | eval and build blur into one step if given the attribute; given `drv^*` it is (b) with an implicit copy | keeps the Evaluate / Build / Copy stages; Copy becomes a no-op | needs a new remote-unit effect and resume polling, like BootOnce |
| Failure modes | same as (b), less visible | drv copy fails loudly if an eval-cache hit points at a GC'd `.drv` (the likely 0.3.8 cause, I). Fix: re-eval with refresh. A dropped ssh-ng link kills the remote build (I); the retry is idempotent | unit-name collisions and orphaned units; more code |

## Recommendation: (b)

(b) keeps local evaluation, so the deadlock never comes into play. It was proven by hand on this exact pair of hosts. It keeps Lojix's staged records honest. Model bytes never cross the link, and the laptop does no build work. Its one real weakness is a build tied to a flaky ssh link. At present that link is ouranos's Wi-Fi to Prometheus's AP. The retry is idempotent, and (c)'s detached unit can harden it later.

### Typed change: behaviour only, no signal-lojix or meta-signal-lojix schema change

- `DeploymentTransport { nix_store_uri, ssh_destination }` is already mandatory, and `validate_nix_store_uri` already requires ssh-ng. Rule: **Realize and every activating action build in `nix_store_uri`, unless the target node is the daemon host.** The self-target check already exists for self-Switch (`daemon_host`). For a self-target, keep `Local`.
- Internal changes (lojix-only, lojix 8.1.0):
  - Restore `BuildTarget::TargetStore(NixStoreUri)` in `runtime_flow.rs`.
  - `DeployPipeline::build_target` (~1787) picks it.
  - `run_nix_build` runs `nix copy --derivation --to <uri> <drv>`, then `nix build --no-link --print-out-paths --store <uri> <drv>^* <substituter options>`, then `add-root` over ssh.
  - Folding all three into the one Build effect means **no new `DeployResumeStage`**, so no sema migration.
  - `ClosureCopy` is skipped when the source is `TargetStore`: the router at ~3448 goes straight to activation.
  - Realize now leaves the closure on the target, and a later ScheduleBootOnce rebuilds as a no-op.
- Lojix records: `GcRoot` and `LiveGeneration` keep the same fields, and `closure_path` names a path in T's store. The new on-disk root `/nix/var/nix/gcroots/lojix/<generation>` on T makes the durable `GcRoot` row true. Pruning that row must also remove the link.
- Only if the living wants per-deploy choice would a field be needed: a `RealizationStore [ Operator Target ]` on meta-signal-lojix `HostDeployment` (breaking bump). I do not recommend adding it now.

### Where the builder field goes dead

`HostDeployment.nix_builder_spec_option` (meta-signal-lojix, `Some.@/etc/nix/machines`) is consumed only at `DeployPipeline::build_target` (~1787 → `BuildTarget::Remote`) and in `build_closure_remote` (`--option max-jobs 0 --builders`). Under TargetStore the target daemon builds with its own settings, and ouranos's machines file names Prometheus itself. So for a non-self target the field is irrelevant. It should be **rejected, or ignored with a witness line**, and must not win the way it did in 0.3.5. A client-side `--builders` could be forwarded to a trusted remote daemon (I), so it must not be passed. The field stays meaningful only for a self-target, for example ouranos offloading its own build.

## Tests (argv-level, no real closure)

1. A remote-node Realize or ScheduleBootOnce resolves `BuildTarget::TargetStore(transport.nix_store_uri)`. A daemon-host target stays `Local`.
2. Eval argv never contains `--store` or `--eval-store`. This guards against the deadlock and inverts nothing in the existing tests at ~9368–9405.
3. The TargetStore build emits, in order: `copy --derivation --to <uri> <drv>`, then `build --no-link --print-out-paths --store <uri> <drv>^*` with substituters and without `--builders` or `max-jobs 0`, then `add-root` on `ssh_destination`.
4. The builder spec is present but ignored or rejected for a remote target.
5. The router skips `CopyClosure` after a TargetStore `ClosureBuilt`. Activating actions go straight to activation, and Realize finishes.
6. A missing local `.drv` makes the Build stage fail with its own evidence, not a partial copy.
7. Resuming from `DeployResumeStage::NixBuild` reruns the idempotent triple.
8. Existing `tests/deploy_transport_integration.rs`: extend it with a fake `nix` that records calls for the TargetStore path.
9. A live check, later: Realize for Prometheus while `df /nix` on ouranos is watched. The expected delta is 0 bytes of outputs.

## Sources

- lojix `f090da07`: `src/schema_runtime.rs` (7240–7440, 5225–5260, 6146–6190, 3435–3465, 1740–1800, 2145–2190, 4745–4775); `src/runtime_flow.rs:107`; `src/runtime_model.rs:932`.
- lojix history: `fc9707b`, `860e99a`, `664b618`, `250c1e3` (diff and `NON_IDEAL_AGENTS.md`).
- signal-lojix `cd16489` (`DeploymentTransport`, `DeploymentInputMode`); meta-signal-lojix `c0f883c` (`HostDeployment.nix_builder_spec_option`).
- `nix --version` and `nix config show` on ouranos and on `root@prometheus.goldragon.criome`; `/etc/nix/machines` on ouranos; `df -h /nix` on Prometheus.
- `flows/d8df70/witnesses/prometheus-build-on-target.log`; `flows/da88cf/reports/prometheus-deploy-risk.md`.
- Scratch: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/lojix-target-store/sr.rs`.
