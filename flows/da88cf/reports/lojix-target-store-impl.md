# Lojix 8.1.0: realize a remote node's closure in its own store

A subflow of da88cf wrote this on 2026-09-26. It implements option (b) from `reports/lojix-realize-on-target.md`. The revision is lojix **`3fc95f0cf4eaf14ff62898c4783ebbc670fdf96b`**. Both `main` and `target-store-da88cf` point at it on GitHub; `git ls-remote` returns that hash for both. Its parent is `f090da07`. Nothing was deployed. The live Nexus and its store were not touched.

## The change

- **Where the build runs.** `DeployPipeline::build_target(daemon_host)` in `src/schema_runtime.rs` compares the deployed node with the daemon host.
  - Same node: `Local`, or `Remote(builder)` when a builder spec is given. This is the path 8.0.0 used.
  - Different node: `BuildTarget::TargetStore(TargetStoreBuild { deployment_transport, node_name, operator_node, ignored_builder_option })`. This is new, in `src/runtime_flow.rs`.
- **The Build step for `TargetStore`.** This is the `TargetStoreRealization` effect. It is folded into the existing `NixBuild` effect and runs three commands:
  1. `nix copy --derivation --to <nix_store_uri> <drv>`
  2. `nix build --no-link --print-out-paths --store <nix_store_uri> <drv>^*`, plus any extra substituters, with no `--builders` and no `max-jobs`
  3. `ssh -o BatchMode=yes <ssh_destination> 'export PATH=…; mkdir -p <dir> && nix-store --add-root <dir>/generation-<id> --realise <out>'`. For a `root` login `<dir>` is `/nix/var/nix/gcroots/lojix/<daemon-host>`. For any other login it is `"$HOME"/.local/state/lojix/gcroots/<daemon-host>`, an indirect root.
  - The step refuses input that is not a `.drv` path.
  - No new `DeployResumeStage` and no store migration. Resuming from `NixBuild` reruns all three commands, and each one is idempotent.
- **Evaluation stays local.** `eval_drv_path` still adds no `--store` or `--eval-store` for any build target. This is the guard against the 0.3.9 deadlock.
- **The copy stage.** `CopyClosureCommand` gained `closure_origin: ClosureOrigin`. When the origin is `TargetStore`, the stage runs only `nix path-info --store <nix_store_uri> <out>`. That is a presence check, not a transfer. If the output is missing, the copy stage fails and names that command.
- **Logging.** When a builder spec is ignored, the daemon logs one line on stderr per build: `lojix-nexus: BuilderIgnored.{ <node> TargetStore «<spec>» }`. Each target-store build also logs `lojix-nexus: TargetStoreRealized.{ <node> <uri> <out> <gc-root> }`.
- **Recording.** Lojix records the output path as it exists in the target's store. It goes in the job cursor, `LiveGeneration` and the `GcRoot` row. The VM check's `Query.ByDeployment` showed `Some./nix/store/j2cj…-lojix-target-store-fixture`. The terminal `DeploymentRecord` schema is unchanged, so the record of a Realize that activates nothing does not carry the path. For that case the evidence is the `TargetStoreRealized` log line and the root on the target.
- **Version.** 8.1.0 in every workspace `Cargo.toml` and in `Cargo.lock`. The versioning skill says to bump for a deploy-behaviour change; there is no wire, store or resume-stage change. There is a new `UPGRADES.md` entry "8.0.0 to 8.1.0". `ARCHITECTURE.md` and `NON_IDEAL_AGENTS.md` now describe both paths.
- **Library surface.** `DaemonRuntime::with_daemon_host`. `build_target`, `nix_eval_command`, `nix_build_command` and `copy_closure_command` now take the daemon host.

## Deploy.Host semantics after 8.1.0

- **The target is the daemon host** (`node == daemon_host`): unchanged. Local eval, then a local build (`--builders <spec>` when `Some.<spec>`), then `nix copy --substitute-on-destination --to <uri> <out>`, then activation.
- **Any other node**: local eval, then the three-command TargetStore build, then the presence check, then the same activation. This applies to Realize and to every activating action, and to user environments as well as hosts.
  - `Some.@/etc/nix/machines`, or any builder spec, is ignored and the daemon logs `BuilderIgnored`.
  - Realize leaves the rooted closure on the target. A following ScheduleBootOnce copies the derivations and rebuilds, and both are no-ops.
- **What the target needs.** The ssh-ng login must be a trusted user of the target daemon. The SSH login must be able to run `nix-store`. Prometheus with `root@` meets both.
- **Not done.** Retiring a generation does not remove its target-side root. For now it must be removed by hand; `UPGRADES.md` says so.

## What a Prometheus deploy now stages on ouranos

**I** (inferred from the code and the VM check; there has been no live run).

- Ouranos receives only the **`.drv` closure** from evaluation, plus the flake source that evaluation fetches.
- **No output paths** land on ouranos. That includes the model `.gguf` fixed-output derivations.
- Prometheus builds, or substitutes from its own caches, into its own store. The output stays rooted at `/nix/var/nix/gcroots/lojix/ouranos/generation-<id>`, assuming the daemon host is named `ouranos`.
- The transfer from ouranos to Prometheus is the `.drv` files and their sources. By hand on 2026-09-24 that was 4 files in 4 seconds.
- Design test 9 is still open: a live Realize while watching `df /nix` on ouranos, where the expected change is 0 bytes of outputs.

## Tests

Every build below ran on `ssh-ng://nix-ssh@prometheus.goldragon.criome`, driven from ouranos with `--max-jobs 0`. In each log, every `building '…'` line is paired with a `building '…' on 'ssh-ng://nix-ssh@prometheus…'` line; there were no local builds. Logs are in the scratchpad `lojix-target-impl/`.

| Check | Result | Offload line |
|---|---|---|
| `clippy` (`--all-targets -D warnings`) | pass | `building '…-lojix-clippy-8.1.0.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'` |
| `test` (cargo test) | pass: 106 unit tests, 13 in `deploy_transport_integration`, all other binaries ok | `…-lojix-test-8.1.0.drv' on 'ssh-ng://nix-ssh@prometheus…'` |
| `target-store-realization` (new, two-VM NixOS test) | pass | `…-vm-test-run-lojix-target-store-realization.drv' on 'ssh-ng://nix-ssh@prometheus…'` |
| `fmt`, `no-free-functions`, `no-inherent-methods`, `bootstrap-rejects-flags`, `nexus-startup-rejects-arguments`, `fresh-daemon-startup`, `failure-evidence`, `deploy-honesty` | pass | each `… on 'ssh-ng://nix-ssh@prometheus…'` |
| `retained-transient-semantics`, `same-host-test-activation` (VM) | pass | `vm-test-run-… on 'ssh-ng://nix-ssh@prometheus…'` |
| `build`, `nexus-binary` | pass | no build line: the output was already valid from the earlier builds on Prometheus |

The first `test` run failed with one error. `deploy_honesty::a_failed_closure_copy_names_the_copy_stage_and_not_a_builder` deploys node `beacon` against the default daemon host, so it now went down the TargetStore path. That test is about the daemon-host copy, so its runtime now runs on `beacon`. The first VM run failed while loading the SSH key: `Load key … error in libcrypto: unsupported`, because the fixture wrapped an already-written key file. It now uses `snakeOilEd25519PrivateKey`. Both reruns passed.

How the design's nine tests are covered:

1. **TargetStore is chosen for a remote node; Local for the daemon host.** Unit tests `build_on_a_different_target_realizes_in_the_transport_store`, `realize_on_a_different_target_also_realizes_in_the_transport_store` and `build_on_the_daemon_host_stays_local`.
2. **Eval never uses `--store` or `--eval-store`.** Unit test `eval_never_redirects_even_for_a_target_store_build`. In the VM, every `eval` call carried no `--store` and no `ssh-ng`.
3. **Command construction.** Unit tests for the drv copy, for the build (substituters present; no `--eval-store`, `--builders` or `max-jobs`), and for the GC root (root login direct, user login indirect). The pipeline test `remote_node_builds_in_its_own_store_roots_the_output_and_skips_the_transfer` checks the order: eval, drv copy, build, root, presence check, profile, activate.
4. **Builder ignored.** Unit test `explicit_builder_is_carried_as_ignored_for_a_remote_target`, pipeline test `remote_node_ignores_the_request_builder`, and the VM journal line `BuilderIgnored.{ target TargetStore «@/etc/nix/machines» }`. The regression test `daemon_host_builder_still_offloads_through_the_local_client` shows the builder still applies on the daemon host.
5. **Copy after a TargetStore build.** The design said to skip it; the brief asked for a no-op, and that is what was built. Unit test `copy_after_a_target_store_build_is_a_presence_check`. Pipeline test `output_missing_on_the_target_fails_the_copy_stage_before_activation`. `remote_realize_leaves_the_rooted_closure_on_the_target_and_nothing_more` shows exactly four effects and no copy or activation.
6. **A missing `.drv`.** `missing_local_derivation_fails_the_build_stage_before_any_remote_build`: the Build stage fails, the failed command recorded is `nix copy --derivation`, and no build or ssh runs.
7. **Resume.** `rerunning_a_target_store_build_repeats_the_same_idempotent_triple` runs the build effect twice and gets two identical triples. The actual `NixBuild` resume rebuilds the command from the cursor through the same method.
8. **Fake-program integration.** `tests/deploy_transport_integration.rs` has six new tests. Its existing tests now run with the daemon on the deployed node, and assert no `--derivation`, `--store`, `path-info` or gcroots appears. They are the daemon-host regression.
9. **Live check on Prometheus.** Not run; out of scope here.

**The integration test with a fixture store for the target.** A `local?root=` chroot store cannot build inside the cargo sandbox, and lojix accepts only `ssh-ng://` URIs. So the fixture is a second NixOS machine (`checks/target-store-realization.nix`) with real Nix, real `nix-daemon` and real `sshd`. The only fake is a `nix` wrapper that logs each call and rewrites the fixture `github:` ref to a local git repo. It proved:

- a real `copy --derivation --to ssh-ng://root@target …drv`
- a real `build --store ssh-ng://root@target …drv^*` on the target, while the operator has `max-jobs = 0`
- a root at `/nix/var/nix/gcroots/lojix/operator/generation-1` that kept `…-lojix-target-store-fixture` through `nix-collect-garbage` on the target
- the output absent from the operator's store (`nix-store --check-validity` fails there)
- the copy stage as `path-info --store ssh-ng://root@target <out>`, with no `--substitute-on-destination`
- the TestActivation running the target-side output
- the deployment ending `Succeeded`

## Sources

- lojix `3fc95f0c` (parent `f090da07`): `src/runtime_flow.rs`, `src/schema_runtime.rs`, `tests/deploy_transport_integration.rs`, `tests/deploy_honesty.rs`, `checks/target-store-realization.nix`, `flake.nix`, `UPGRADES.md`, `ARCHITECTURE.md`, `NON_IDEAL_AGENTS.md`.
- Design: `flows/da88cf/reports/lojix-realize-on-target.md`, `flows/da88cf/reports/prometheus-deploy-risk.md`, `flows/d8df70/witnesses/prometheus-build-on-target.log`.
- Check logs: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/lojix-target-impl/` (`clippy.log`, `test.log`, `vm.log`, `check-*.log`, `checks-summary.txt`).
- `git ls-remote https://github.com/LiGoldragon/lojix main target-store-da88cf`: both `3fc95f0cf4eaf14ff62898c4783ebbc670fdf96b`.
