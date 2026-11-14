# Lojix: steps A and B

Both steps are on branch `ethos28-be2651` of lojix, pushed and gated green on prometheus. Nothing is merged, released or deployed. Step B is done for its terminal-accounting half only. Its capability half, `bootctl --graceful`, rests on a premise that does not hold, so it waits on a ruling (below).

Each claim is marked **Observed** (seen in a run or in source) or **Inference**. `$S` is `/tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad`.

## Heads

| step | commit | gate |
|---|---|---|
| base | 5c2cff8ced2efc07d3fffe29cbd4a35d6bc6b2cd | (step 10) |
| A | **10241fbc1dd54f362ec24a01f11ede16894ea63a** | 18 of 18, exit 0, `$S/sab/gate-lojix-10241fb.log` |
| B (accounting) | **38a57f1d12af12d31cb377abf86f082f79d6d04b** | 19 of 19, exit 0, `$S/sab/gate-lojix-38a57f1.log` |

The version stays 0.11.0. Each step adds a paragraph to the existing UPGRADES entry.

## Ruling needed: the boot-entry clears (step B, capability half)

**`--graceful` does not cover `set-default` or `set-oneshot` (Observed).**
- I ran `bootctl --graceful set-default ''` on ouranos (systemd 262) as an unprivileged user. It printed `Not booted with a supported boot loader.` and exited 1. The plain command does the same, and so did the live failure (`flows/374411/fy2t/ouranos/self-switch-journal.txt:23`).
- systemd's source on its main branch agrees. `verb_set_efivar` calls `verify_touch_variables_allowed` (`src/bootctl/bootctl-util.c`). Its comment says that for these verbs "we fail loudly", unlike the verbs that skip gracefully. It never reads `arg_graceful`. It refuses when the machine did not boot UEFI, and when the `LoaderInfo` EFI variable is absent ("Not booted with a supported boot loader."). `--graceful` applies only to `is-installed`, `update`, `remove`, `random-seed` and one `set-timeout` case.
- So the approved shape would not have stopped the ouranos failure, and I left the clears unchanged.

**Options (Inference).**
1. Guard the clears with the same test bootctl itself makes: clear only when `/sys/firmware/efi/efivars/LoaderInfo-4a67b082-0a4c-41cf-b6c7-440b29bb8c4f` exists. The guard goes in both the foreground clears and the self-switch script, and `set -eu` stays. A supporting loader still clears; a loader without the interface is a successful no-op. This is my reading of what the approved shape meant.
2. Declare each node's loader in Horizon, and emit the clears only for systemd-boot hosts.
3. `bootctl --variables=yes` skips the check and writes the variable anyway. That is wrong for a loader that ignores it, and it still fails on a host that did not boot UEFI.

Until a ruling, every same-host switch on ouranos ends `Failed(Activate/ActivationFailed)` with its generation Current. That is now the honest record of what the unit did (below).

## Step A: the stages are attempts (10241fb)

**operation.ethos (Observed).**
- The ten pipeline stages are operations beside the 14 Memory operations, each named as the doing: `ResolvingFlake`, `MaterializingHorizon`, `EvaluatingClosure`, `BuildingClosure`, `CopyingClosure`, `ActivatingGeneration`, `CollectingGarbage`, `BuildingHermeticCheck`, `BringingUpTestVm` and `TearingDownTestVm`.
- Their outcomes are `FlakeResolved`, `HorizonMaterialized`, `ClosureEvaluated`, `ClosureBuilt`, `ClosureCopied`, `ActivationCompleted`, `DetachedTestActivationDispatched` (renamed `DetachedActivationDispatched` in B), `PathsCollected`, `HermeticCheckBuilt`, `TestVmStarted` and `TestVmStopped`. `EffectFailed.EffectFailure` is the outcome they share.
- `ActivationCompleted` replaces the effect result's `GenerationActivated`, because the Memory outcome already has that name.
- The stage inputs and results are generated with them: `BuildTarget`, `TargetStoreBuild`, `ActivationProfile`, `MaterializationShape`, `EffectStage`, `EffectFailure` and the rest. Three fields gained types:
  - `TargetStoreBuild` carries `Option<IgnoredBuilder>` and `emission::OperatorNode`;
  - the test-VM commands carry `GuestNode`, a new `TestVmHost` and `GuestAddress`, where they had `node`, `host` and `string`;
  - `GarbageCollected` carries `CollectedPaths`, where it had a `u64`.
- `horizon_lib:[ HorizonDefinition ]` and `:crate:emission:[ … ]` are imported. ethos-zero 29 generates the file without complaint (`src/operation.rs`, 108 to 384 lines).

**The runner (Observed).**
- `EffectCommand`, `EffectResult` and `NexusWork` are gone. `NexusAction` is now `Operate(Operation) | Finish`.
- `NexusEngine::attempt(Operation) -> Outcome` is async and covers every operation: a stage awaits its emissions, and a Memory operation goes to the synchronous `Operating::operate`, which the answerer still calls.
- `decide(Outcome)` is one exhaustive match. It sends a stage outcome to the test router while a test is active, and to the deploy router otherwise.
- runtime_flow.rs goes from 427 to 143 lines.

**One choice I made (Inference; say if you want it otherwise).** `Operating::operate` must match every variant of the one generated `Operation`. A stage reaching it answers `StoreRefused` ("a pipeline stage is attempted by its pipeline, not applied to the store"). The answerer never sends one.

**emission.ethos (Observed).**
- `ActiveState` is `[ Active Reloading Inactive Failed Activating Deactivating Maintenance Refreshing Unrecognized.String ]`, from systemd's `unit_active_state_table`.
- `ServiceResult` is `[ Success Resources Protocol Timeout ExitCode Signal CoreDump Watchdog StartLimitHit OomKill ExecCondition Unrecognized.String ]`, from systemd's `service_result_table`.
- They are read through `ActiveStateReading` and `ServiceResultReading`, each `Read | Unreadable.BusFault`. `PropertyReading` goes.
- The words live in the translator (`SystemdWord`). Evidence and log text are unchanged.
- `InputDirectory`, `HomeDirectory`, `UnitName`, `GuestAddress` and `SriHash` were already newtypes, so nothing changed there.
- The materialization's file writes are untouched, as the brief said (pending at Fable).

## Step B: a same-host switch is settled from PID 1's receipt (38a57f1)

**The dispatch (Observed).**
- The self-switch unit is dispatched exactly as the self-test is: `systemd-run --no-block --service-type=oneshot --remain-after-exit`. It was `--collect --wait`. The script is unchanged.
- A waited-on unit cannot also retain its receipt: systemd's `run.c` refuses the pair ("--wait may not be combined with --remain-after-exit").
- `RetainedUnitDispatch` now carries a `TransientScript`, which gains `SelfTest`.

**Who settles (Observed).**
- The same observer that watched the self-test now watches both. It is held by the dispatcher, and by the successor if the switch replaces the daemon.
- It reads the exact unit's `ActiveState`, `Result` and `ExecMainCode`/`ExecMainStatus` and classifies them (`DetachedActivationUnit::classify`).
- `settle` then does four things:
  1. completes a failure with the unit's journal;
  2. for a Switch, records the generation Current when `/nix/var/nix/profiles/system` resolves to the closure (`self_switch_activation_record`);
  3. writes the terminal the unit came to (`terminal_outcome`);
  4. stops the unit once that terminal is durable.
- If the Current write fails, the deployment stays Activating for the next start, as before.

**What goes (Observed).**
- The startup branch that recorded `Succeeded` from profile equality alone is gone.
- So are `persist_reconciled_self_switch` and `daemon_host_system_closure`, which move into `settle` and `SystemProfile`.
- `detached_test_activation_unit` becomes `detached_activation_unit`, for `ActivateNow` and `TestActivation` alike.

**Two classification and record changes (Observed).**
- An `inactive` unit with `Result=success` whose main process exited 0 is now a success. That is how a unit dispatched by an older daemon (`--collect`, no retained receipt) ends. Without this, the first switch across the upgrade would be read as failed while PID 1 still held it. Before, every state but `active`+`success` was a failure.
- The recorded artifact is the submission's own `host_composition`, where it was always `CompleteHost`. The observer now records every same-host switch, including ones whose dispatcher survives, so it must record what the pipeline would have recorded.

**Tests (Observed).** These follow the audit's test plan.
- **Unit tests:**
  - `a_retained_receipt_is_classified_from_systemd_values`: active and inactive success, signalled, running, failed with exit code 1, and an unrecognized word kept as text;
  - `a_self_switch_unit_that_failed_carries_its_result_and_journal`;
  - `self_host_switch_selects_the_detached_shape`, which now asserts `--no-block`, `--remain-after-exit` and neither `--wait` nor `--collect`.
- **Daemon tests on a real store:**
  - `a_succeeded_self_switch_unit_settles_current_and_succeeded`;
  - `a_self_switch_unit_that_failed_after_the_switch_settles_current_and_failed`: ouranos's failed / exit-code / status 1 ends Current and `Failed(Activate/ActivationFailed)`, its evidence naming the unit and exit 1;
  - `the_system_profile_records_current_and_never_the_terminal`.
- **Failure-evidence paths:**
  - The fake-program self-switch journal test went, because the unit's failure is now read over D-Bus, not from systemd-run's exit. The two tests above and the VM check carry that coverage.
  - `an_unreadable_unit_journal_says_why` now drives the boot-once, the remaining waited unit.
  - The boot-once journal test gained the check that the journal is read on the unit's own node.

**The new VM check, `same-host-switch-activation` (Observed; 23.4 s, `$S/sab/gate-B.clean` from line 19,500).** It runs the real daemon, real systemd and the real `nix-env`; Nix, ssh and the loader interface are faked.
1. **No boot-loader interface.** The VM's real bootctl prints "Not booted with UEFI." and exits 1, after the switch that replaced the daemon.
   - The successor (pid 1313) read `failed`/`exit-code` from the retained unit, which the dispatcher (pid 1249) had attached.
   - It recorded `{ 1 1 … BaseHost LiveActivation Current … }` and `Failed.{ Activate ActivationFailed … systemd reported Result=exit-code; main process exited with status 1`, followed by `--- journal of lojix-self-switch-deploy-1.service ---` and `Not booted with UEFI.`.
2. **Loader interface present.** The successor read `active`/`success` and recorded Current and `Succeeded`. The unit was stopped (`LoadState=not-found`), and bootctl saw `set-default ` and `set-oneshot `.
3. **The switch leaves the daemon running.** The dispatcher settled its own deployment as Current and `Succeeded`, and its InvocationID was unchanged.

`same-host-test-activation` passes unchanged (19.7 s).

## Proof

**Gates (Observed).** Both ran `nix-fast-build --remote li@prometheus.goldragon.criome --no-nom --no-download --eval-workers 1` on `git+file://$S/wt/lojix?rev=<head>`, and both exited 0.
- 10241fb: 18 checks, 248 tests passed and 3 ignored.
- 38a57f1: 19 checks, 250 tests passed and 3 ignored.
- On the builder, `cargo test --workspace --all-features --no-fail-fast` passed 235 tests at A and 238 at B. Both fail only the two `tools/tests/nexus_configuration.rs` tests (`LegacyFileLacksSchema`) that fail at every base. clippy `-D warnings` and fmt are clean. Logs: `$S/sab/t1.log` and `$S/sab/t3.log`.

**Argv (Observed).** `every_emission_runs_the_argv_23f88f2_ran_for_the_same_inputs` passes in both gates, against `tests/fixtures/emission-argv.txt` (37 lines, unchanged). Every emission's argv is byte-equal to 23f88f2's except one, which is listed in the test itself:
- `host self-switch`: `--collect --wait --service-type=oneshot /bin/sh` becomes `--no-block --service-type=oneshot --remain-after-exit /bin/sh`. The script is byte-equal.

There is no `--graceful` difference, because the clears are unchanged.

**A/B over a fresh copy of the live store (Observed).**
- **First copy, discarded.** I copied `/var/lib/lojix/lojix.memory` as root over `ssh root@localhost` at 15:01:56. A probe on an isolated copy showed one in-flight row: deployment 591, an ouranos user-environment `ActivateNow` in `Building`. A daemon would restart that pipeline. The live journal showed it fail on its own at 15:01:59. I discarded that copy (`$S/sab/ab/copy-proof-0-inflight.txt`).
- **Second copy, used.** I took it at 15:03:09. The source before, the copy, and the source after all hash `a61dc5a0…`.
- **The live service was not touched.** `lojix.service` was 0.10.6 (`/nix/store/hdkdqgb1…`), pid 1938170, started 12:35:56. Proof: `$S/sab/ab/copy-proof.txt`.
- **Repair.** I repaired the copy once with the redb probe on the builder, giving R = `ce7c7d31…`. R holds 591 deployment records, 203 live generations, 2067 events, an empty deploy-job family and 4 quarantined rows (`$S/sab/ab/inspect-R.txt`).
- **Runs.**
  - The harness is step 5's, with the daemon additionally isolated by `--unshare-net`, an empty `/run/dbus` and an empty nix daemon socket, so no effect could leave the namespace (`$S/sab/ab/session.sh`).
  - The 32 inputs are step 8's.
  - The three daemons were A, 5c2cff8 (`/nix/store/w15j15cq…`); BA, 10241fb (`/nix/store/f9psn807…`); and BB, 38a57f1 (`/nix/store/9dwa18s7…`), each serving its own copy of R.
- **Result.** All three are byte-identical:
  - replies `6f2046d5…` (570,664 bytes);
  - daemon stdout `d799838…` and stderr `e47755c…`, the same as step 10's;
  - final store `bd7231b2…`.
  - The deploy is rejected as deployment 592, the two tests are refused `NoTestDefaults`, and the configuration is reversed.
  - Hashes: `$S/sab/ab/hashes.txt`. Every store copy is deleted, here and on the builder.

## Small changes a reader could notice (Observed)

- **Observer log.** The line reads "lojix detached activation observer …", where it said "detached test activation observer".
- **Same-host switch, phases.** It reaches its terminal with no `Activated` phase event, as a same-host test already did. Before, a dispatcher that survived its own switch recorded `Activated` through the pipeline.
- **Same-host switch, dispatch failure.** It no longer reads the unit's journal. A failed `--no-block` dispatch means no unit ran.
- **Stopped failed units stay loaded (Inference from systemd semantics).** A retained unit that failed stays loaded as `failed` after the stop, until `reset-failed` or a reboot; the self-test already left them so. `--collect` used to remove them. A `ResetFailedUnit` emission would clear them; I did not add one.

## Notes

- `$S/sab/` holds the logs, the cleaned gate logs (`gate-A.clean`, `gate-B.clean`), the A/B harness and replies, and the systemd sources I read (`$S/run.c`, `$S/sd/`).
- Builder copies are at `/tmp/offload/{lojix,egen,redb-repair}`.
- This report is not committed to primary, like the reports beside it.
