# Lojix onto its Ethos: step R and step 8

Every change is on branch `ethos28-be2651`, one commit per repository per step, pushed and gated green on prometheus. Nothing is merged, released or deployed.

Each claim is marked **Observed** (seen in a run or in source) or **Inference**. `$S` is `/tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad`.

## Heads

| repository | was | step R | step 8 | gate |
|---|---|---|---|---|
| signal-lojix | 8a77619 | **17c23e2ef85afdb2834b546442d3020c204d14f9** (0.12.0) | — | 10 of 10, `$S/s8/gate-signal-lojix-17c23e2.log` |
| meta-signal-lojix | 4e42269 | **7fe43b82e29631db9d5cf266db594a51c61bc9eb** (0.13.0) | — | 10 of 10, `$S/s8/gate-meta-signal-lojix-7fe43b8.log` |
| lojix | 7f218c1 | **70ff5fe** (0.11.0) | **23f88f27d4643510b164e41ae902eb729b77685f** (0.11.0) | 18 of 18 each: `$S/s8/gate-lojix-70ff5fe.log`, `$S/s8/gate-lojix-23f88f2.log` |
| horizon-rs | — | pinned at 182f530, untouched | — | — |

Versions do not move: each of the three is still unreleased on this branch, so its existing UPGRADES entry carries the change.

## Step R

**signal-lojix 17c23e2 (Observed).**
- `Refused.Refusal` / `Refusal.[ Store.String ]` is now `Refused.StoreFailure` / `StoreFailure.String`. The text is `Refused.«…»`, and a test checks it.
- The build-dependency is ethos-zero 29 (f23eacf). Regenerating with 29 changes only the `Refusal` enum, which becomes the `StoreFailure` newtype.
- horizon-lib is repinned to 182f530. This is forced, because a Lojix graph holds one horizon-lib.
- ARCHITECTURE and UPGRADES are updated (0.11.0 to 0.12.0, now naming 29 and 182f530).

**meta-signal-lojix 7fe43b8 (Observed).**
- It imports `StoreFailure` in place of `Refusal`, so its `Output::Refused` holds `signal_lojix::StoreFailure`. That is the only change in the generated file.
- It repins signal-lojix 17c23e2 and horizon-lib 182f530, with tests and UPGRADES updated.

**lojix 70ff5fe (Observed).**
- **The SSH policy.** `ethos/ingress.ethos` drops `RequireKnownHost.{}`, so `BootstrapSshPolicy.{ BootstrapSshIdentityFile BootstrapSshKnownHostsFile }`.
  - The bootstrapper still writes `StrictHostKeyChecking yes`.
  - The hand model in `bootstrap.rs` keeps its `BootstrapStrictHostKeyMode::RequireKnownHost`, set in the lowering. The reason: the journal fingerprint is the sha256 of the hand request's Debug form, so removing the field would rename every journal. That model belongs to step 11.
- **The reset.** `ResetStore` leaves the ingress. `lojix-reset-store` takes no input: any argument is refused with `Error::UnexpectedResetArguments`. Tests cover no arguments, `{}`, a path, a flag and extra arguments.
- **The repins.** horizon-lib goes to 182f530 on every crate and on the flake's `horizon` input, and flake.lock moves with it. The contracts go to 17c23e2 and 7fe43b8.
- **Ondyfaind.** `grep -rI Ondyfaind` over the lojix worktree (checks/horizon, tests/fixtures, flake fixtures, all sources) finds nothing, so there was nothing to respell.
- README, ARCHITECTURE, skills.md, NON_IDEAL_AGENTS and UPGRADES are updated.

## Tool-text changes

| tool | at 7f218c1 | now | at 0.10.6 |
|---|---|---|---|
| `lojix-reset-store` | `{}` | no argument | `ResetStore` |
| `lojix-bootstrap`, Remote policy | `{ <identity> <known-hosts> {} }` | `{ <identity> <known-hosts> }` | `{ <identity> <known-hosts> RequireKnownHost }` |
| any store failure, either socket | `Refused.Store.«…»` | `Refused.«…»` | no reply |

The rest of the table in `lojix-steps-5.md` stands.

CriomOS at origin/main 7bef66f must move with the pin (Observed by `git grep`):
- `modules/nixos/lojix.nix:267` and `checks/lojix-nexus-service/default.nix:73` run `lojix-reset-store ResetStore`. They must run it with no argument.
- `docs/GUIDELINES.md:277` describes `SshPolicy.{… RequireKnownHost}`.

## Step 8: lojix 23f88f2

**The dispatch (Observed).**
- The new `src/answering.rs` holds `Answerer`, which implements `signal_lojix::Answering` and `meta_signal_lojix::Answering` over `Arc<Store>`.
- Both sockets answer with `input.answer(&answerer)`, and the output is the whole reply.
- Each capability works through a fresh `SchemaRuntime`, using the operation plane (`apply_memory` / `observe_memory`).
- A store failure is answered through `RefusedByStore`, as `Refused(StoreFailure(<the store's words>))`, on either contract. A unit test covers both contracts and the read mapping.

**The watch (Observed).**
- `watch_deployments` registers the watcher before reading the commit sequence, as before.
- The daemon claims the stream when the answer is `DeploymentsWatched`. The stream itself stays hand-written beside the dispatch (Fable C).

**Admission (Observed).**
- `deploy` and `test` reserve a slot of their executor's cap. They then write the durable record and the job row (or the pending test row) through the existing synchronous `submit_deploy` / `submit_test`, which is now synchronous too.
- The seeded engine and its slot are then handed to `DeployJobs` / `TestJobs` with `tell(LaunchDeploy | LaunchTest).try_send()`. The actor spawns the pipeline, which holds the slot until it ends.
- Over the cap, a deploy is rejected `DeploymentInFlight` with its own record, and a test `SubstrateUnavailable`, as before.
- Effects stay on the actors.

**What retired (Observed).**
- `src/adapters.rs`, with `Lowerable`/`Raisable`.
- `OrdinaryIngress`/`Egress` and `MetaIngress`/`Egress`.
- `SignalInput`/`SignalOutput` and `NexusWork::SignalArrived`.
- The `AdmitDeploy`/`AdmitTest`/`DeployCompleted`/`TestCompleted` messages, and the actors' `cap`/`active_count`.
- The decide paths for arriving inputs: `decide_signal_arrival`, `decide_ordinary_input`, `decide_meta_input`, `open_subscription`, `close_subscription`, `decide_test`, `decide_read_completion`.
- The runtime_model twins:
  - `Selection`, the five-way one; queries use the contract's three-way Selection;
  - `Generation` and `GenerationListing`; the canonical-path filter moved into the read projection, for test runs too;
  - `DeploySubmission`, `HostDeployment` and `UserEnvironmentDeployment`; the engine now carries the contract's `ActualizedDeploySubmission`, which is also what the deploy job stores.

**Renamed (Observed).**
- `NexusAction::ReplyToSignal(SignalOutput)` is `Finish(PipelineOutput)`, where `PipelineOutput = meta_signal_lojix::Output`.
- `SignalDeciding` is `PipelineDeciding`.
- `MetaOperation` keeps `Deploy` and `Test`.

**Size (Observed).** 16 files: +1215 / −1701 against 70ff5fe. runtime_model.rs goes from 364 to 243 lines, and daemon.rs from 1461 to 1265.

**One behaviour change (Observed).** A store failure while a test is refused for capacity now answers `Refused.«…»`. Before, `.expect` panicked inside the TestJobs actor. It is noted in UPGRADES.

**Assumed, not ruled.** The brief puts admission in the answer, and `Answering` is synchronous. The cap check therefore moved with admission, from the actor's single-writer count to a shared `tokio::sync::Semaphore` (`JobSlots`).
- A slot is reserved before anything is written and is freed when the pipeline ends, however it ends.
- Admissions now run concurrently on their connection tasks instead of one at a time through the actor.
- **Inference:** this is equivalent, since the only state the serialization guarded was the count.
- A failed hand-off is logged `DeployNotLaunched` / `TestNotLaunched`. That happens only if the actor is gone, and the actor's mailbox is now unbounded. The durable row stays for the next start's reconcile.

## What is left in runtime_model.rs, and elsewhere, and why

adapters.rs is gone.

runtime_model.rs keeps:
- **The operation plane, for step 9 (`operation.ethos`).**
  - `MemoryReadInput`/`Output` and `MemoryWriteInput`/`Output`, the 11 writes and 3 reads with their outcomes.
  - `ActivationCommit`, `ContainerTransition`, `AppliedActivation`, `ContainerReceipt`, `RejectionReport` and `RejectionReason`.
  - The `triad_runtime` marker impls on them.
- **Re-exports** of the generated contract and Memory types.
- **The `carried!` bridge**, which implements Lojix's `Payload` on generated newtypes. It is not a twin. Dropping it touches about 980 `::new`/`.payload()` call sites, mechanical work I left out of this step.
- **The `From` wrappers** into `StoredDeploymentRecord` and `StoredTestRun`.

Kept elsewhere:
- **runtime_flow.rs, for step 10 (`emission.ethos`):**
  - `EffectCommand`/`EffectResult` and their commands;
  - the effect-side twins `DeploymentTransport`, `DeploymentInputMode`, `ActivationBackend`, `ExtraSubstituter` and `TestExecutionProfile`.
- **runtime_flow.rs, for step 9 (the runner):**
  - `NexusWork`/`NexusAction`, `Routable`/`Routed`/`Nexus<Root>`/`OriginRoute` and `NexusEngine`.
  - The pipeline runner still drives through them, so `CommandMemoryRead`/`MemoryReadCompleted` stay as the runner's read type.
  - A read, or a configuration/pin/unpin/retire write, reaching a pipeline is now refused `NoCorrelatedDeployment`, naming what arrived. No pipeline makes one.
- **The triad-runtime dependency stays.** The two-socket daemon (`AsyncMultiListenerDaemon`, peer credentials) and the pipeline `Runner` use it.
- **bootstrap.rs (step 11):** the hand bootstrap model, `BootstrapStrictHostKeyMode` included, and the `*Validated` types.

## A/B over a fresh copy of the live store

**The copy (Observed).**
- I copied `/var/lib/lojix/lojix.memory` as root. The source before, the copy and the source after all hash `8ffc18f9…`.
- `lojix.service` was 0.10.6, pid 1938170, binary `/nix/store/hdkdqgb1…-lojix-0.10.6`. It had been restarted by someone else at 12:35:56, before the copy. I did not touch it. Proof: `$S/s8/ab/copy-proof.txt`.
- I repaired the copy once with the redb probe on the builder, giving R (`e1292168…`). R holds 202 live generations, 2049 events, 586 deployment records, an empty deploy-job family and 4 quarantined rows (`$S/s8/ab/inspect-R.txt`).

**The runs.**
- Both runs used the step-5 bubblewrap harness, `$S/s8/ab/session.sh`. Each daemon served its own copy of R:
  - A was 7f218c1, `/nix/store/2fgqi02b…-lojix-0.11.0`;
  - B was 23f88f2, `/nix/store/yw9vmxb6…-lojix-0.11.0`.
- There were 32 inputs (`$S/s8/ab/inputs.txt`): the 26 from steps 6 and 7, plus answers that write:
  - a Deploy rejected `FlakeReferenceMalformed`, which allocated deployment 587;
  - `Test.Check.[]` and a Live `Test.Run`, both `TestRejected NoTestDefaults`;
  - `ReverseConfiguration`;
  - then event-log, test-run and node queries.

**Result (Observed).**
- The replies are byte-identical: `$S/s8/ab/A/replies.txt` and `$S/s8/ab/B/replies.txt` both hash `3bccbb7a…`, 565,830 bytes.
- The daemon logs are byte-identical: `FamilyUpgraded.{ deploy-job 0 }`, four `QuarantinedRowDropped`, and two `DeploymentWatchEnded`.
- The final stores are byte-identical, both `8f0446a3…` (`$S/s8/ab/hashes.txt`).
- No store failure occurred, so no `Refused` appears.
- I deleted every store copy afterwards, here and on the builder.

## Gates and tests

Every gate ran in the foreground: `nix-fast-build --remote li@prometheus.goldragon.criome --no-nom --no-download --eval-workers 1`, exit 0.

- **lojix 23f88f2:** 18 of 18 checks passed (`$S/s8/gate-lojix-23f88f2.log`). Within them:
  - deploy-honesty, deployment-watch and failure-evidence (`failure_evidence` and `failure_evidence_paths`);
  - the `test` check, which runs `durable_resume`, `engine_routing`, `build_smoke`, `deploy_transport_integration` and 16 other test binaries;
  - the four NixOS VM checks. same-host-test-activation and target-store-realization were rebuilt against the new package. retained-transient-semantics and collected-transient-journal test systemd alone, and were cached.
- **The gate's test totals:** 246 passed, 3 ignored, 0 failed.
- **`cargo test --workspace` on the builder** (`$S/s8/t1.log`): 233 passed and 3 ignored. It fails the same two `tools/tests/nexus_configuration.rs` tests (`LegacyFileLacksSchema`) that fail at every base since 316422f; the gate does not run them.
- **Clippy and fmt:** `clippy --workspace --all-targets -D warnings` and `fmt --check` are clean.
- **Pre-existing, not mine.** `clippy -p lojix-nexus` alone (the lib without `tools`) fails on two dead-code findings in `inspected_text.rs`. It fails identically on 70ff5fe (`$S/s8/clippy-base-n.log`); the gate's clippy check does not build that combination.

## Rulings needed

None blocks. Three readings I took and would have reviewed:
1. **The executor cap** is a semaphore slot reserved at admission, in place of the actor's count (above).
2. **The hand bootstrap model keeps its one-variant strict mode** until step 11, so journal fingerprints stay stable. Dropping it then renames any journal in progress.
3. **A store outcome no capability asks for** is answered `Refused` with the text "the store answered <operation> with <outcome>". This path is unreachable today.

## Notes

- **The contracts' horizon-lib repin** was not named in the brief. Without it, lojix would hold two horizon-lib crates and two `HorizonDefinition` types.
- **Builder copies** are at `/tmp/offload/{lojix,signal-lojix,meta-signal-lojix,egen}`. `egen` is the ethos-zero 29 generator (`$S/s8/gen.sh`).
- **This report is not committed** to primary, like the reports beside it.
