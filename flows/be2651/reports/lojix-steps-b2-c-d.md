# Lojix: steps B2, C and D

All three steps are on branch `ethos28-be2651` of lojix. Each is one commit, pushed and gated green on prometheus. Nothing is merged, released or deployed. The version stays 0.11.0, and each step adds a paragraph to the existing UPGRADES entry.

Each claim is marked **Observed** (seen in a run or in source) or **Inference**. `$S` is `/tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad`.

## Heads

| step | commit | gate |
|---|---|---|
| base | 38a57f1d12af12d31cb377abf86f082f79d6d04b | (step B) |
| B2 | **73dfcf3f20102c97fd57b65cc32962ecbeb311bc** | 19 of 19, exit 0; 255 passed, 3 ignored; `$S/sbcd/gate-73dfcf3.log` |
| C | **2d4330e5226c7d8def22539f0cd00dcfbbd47787** | 19 of 19, exit 0; 257 passed, 3 ignored; `$S/sbcd/gate-2d4330e.log` |
| D | **a83218cac892c65fc3ef560043186d6fd4b86780** | 20 of 20, exit 0; 258 passed, 3 ignored; `$S/sbcd/gate-a83218c.log` |

## Step B2: boot-entry clears only under a loader with the interface (73dfcf3)

**The read (Observed).**
- There is a new emission, `ReadLoaderInterface.LoaderInterfaceQuery { SshDestination }`. Its outcome is `LoaderInterfaceOutcome.[ Read.LoaderInterface Unrecognized.Stdout Failed.ProcessFailure ]`, where `LoaderInterface.[ Implemented NotImplemented ]`.
- It runs over the activation's own ssh route: `if [ -e /sys/firmware/efi/efivars/LoaderInfo-4a67b082-0a4c-41cf-b6c7-440b29bb8c4f ]; then echo implemented; else echo not-implemented; fi`.
- The node prints one of two words, so a failed ssh is never read as "absent".

**Where the read runs (Inference: my reading of the brief).**
- **Remote Boot or Switch:** the read runs before the switch. `LoaderInfo` is set by the loader at boot, so no switch changes it. A read that fails therefore fails the activation before anything on the node changes.
- **Same-host switch:** the daemon makes the same read before the dispatch, over the dispatch's own ssh route. It then chooses the script: `TransientScript.SelfSwitch` now carries `SelfSwitchScript.{ ClosurePath LoaderInterface }`, and the script includes the two `bootctl` lines only when the loader is `Implemented`. That script is byte-equal to today's.
- The brief said the read is made "in the self-switch script". I moved it out because a check inside the script could not report a skip as a typed fact: the observer sees only the unit's result. Say if you want the check inside the script instead.

**Saying the skip (Observed).**
- `operation.ethos` gains `BootEntryReconciliation.[ Cleared SkippedWithoutLoaderInterface NotRequired ]`.
- `ActivatedGeneration` carries it, and `DetachedActivationDispatched` now carries it too. Every action other than Boot and Switch gives `NotRequired`.
- When the clears are skipped, the daemon logs: `lojix: <node> boots a loader that does not implement the boot loader interface (no LoaderInfo); its boot-entry clears are skipped`.
- No Memory change.

**When the loader has the interface (Observed).** The clears run as today. A clear that fails is still `Failed(Activate/ActivationFailed)`. For a same-host switch the generation is also recorded Current, which the VM proves below.

**A gap I left (Observed in source; not changed).** On the remote foreground path, a clear that fails after a successful switch ends Failed without recording Current. That was already true at 38a57f1. Fixing it needs a stage outcome meaning "switched, then the trailing step failed", and the router would record Current before the Failed terminal. That is the bead's "says both, typed", and it is a design step, not a cleanup.

**Tests (Observed).**
- Unit tests, with a fake `ssh`:
  - `a_switch_under_a_loader_without_the_interface_skips_the_clears_and_says_so`;
  - `..._with_the_interface_clears_both_entries`;
  - `a_clear_that_fails_..._fails_the_activation`;
  - `a_loader_read_that_prints_neither_answer_fails_before_the_switch`;
  - `the_loader_interface_read_and_a_self_switch_without_clears_are_the_named_additions`.
- **VM check `same-host-switch-activation`**, now four cases (26.2 s):
  1. **No `LoaderInfo`.** `bootctl` never runs: the argv log is absent. The successor records Current and `Succeeded`, the journal has the skip line, and the unit is stopped.
  2. **`LoaderInfo` present** (a tmpfs over `/sys/firmware`), and the fake `bootctl` refuses. The successor records Current and `ActivationFailed`, with the refusal in the evidence, and the unit's Result is `exit-code`.
  3. **`LoaderInfo` present and both clears succeed.** The result is Current and `Succeeded`, and the unit is stopped.
  4. **The daemon survives the switch.** The dispatcher settles the deployment `Succeeded`.

## Step C: file writes, copies and reads as emissions (2d4330e)

**The new emissions (Observed).** `emission.ethos` gains six emissions. Each runs on the daemon's host, and each fault is the OS error text:

| emission | does |
|---|---|
| `PrepareDirectory` | `create_dir_all` |
| `EmptyDirectory` | remove the directory (an absent one included), then create it |
| `WriteFile` | `{ FilePath FileText }` |
| `CopyFile` | `{ SourceFile DestinationFile }` |
| `ListDirectory` | lists the directory: `Listed.Vector<DirectoryEntry>`, each entry carrying its `EntryKind` |
| `ReadSystemProfile` | `Resolved.ClosurePath` or `Unresolved.FileFault` |

- `EntryKind.[ RegularFile SymbolicLink Directory Other Unreadable.FileFault UndecodableName ]`.
- The listing reads each entry without following a link.
- `FileOutcome.[ Completed Failed.FileFault ]`.

**What moved onto them (Observed).**
- The Horizon materialization's directories, its `horizon.json` and `flake.nix` writes, the emptying of the `secrets` input, the secrets listing and the `.sops` copies.
- The `canonicalize` of `/nix/var/nix/profiles/system` in the self-switch settle.
- `schema_runtime.rs` no longer imports `std::fs` outside its tests.
- The error text is unchanged: `io error: <OS text>`, as asserted in a new test.

**Behaviour changes (Observed).**
- A `.sops` file whose name is not UTF-8 is still refused `SecretFileNameNotUtf8`. It is now refused when the directory is listed, before any copy, where before it was refused mid-copy.
- Before, only `.sops` entries had their metadata read. The listing now reads it for every entry. An unreadable non-`.sops` entry carries its fault and fails nothing.

**HOME and USER: left as environment reads (the change is not small).** The exact change, for a bead right after the release:
1. **signal-lojix.** `LojixNexusConfiguration` gains `ServiceAccount.{ UserName HomeDirectory }`: the Nexus's own login, whose name the local fast path compares and whose home holds the Home Manager profile. This is a contract release, and meta-signal-lojix is re-released over it, because it imports the configuration. It is a wire break of `Configure`, `Configured` and `ConfigurationReceipt`.
2. **lojix Memory.** `NexusConfigurationRecord` changes shape, so the `nexus-configuration` family needs a new schema hash and a one-write upgrade in `src/upgrade.rs`. **A ruling is needed:** what the upgrade fills in for the existing row. Either take the account once from the environment at upgrade time, or hold the store unconfigured until a meta Configure supplies it.
3. **Configuring.** The built-in default cannot know the account without reading the environment. So the CriomOS `lojix` module must supply it, through `lojix-write-configuration` (`ConfigurationWriteRequest` and the reset request string gain the field), or through the meta Configure, from `services.lojix.user` and `config.users.users.<user>.home`.
4. **Engine.** `UserEnvironmentActivation` takes the account from `RuntimeConfiguration`. `current_user` (USER/LOGNAME) and `run_profile`'s HOME read go. The same record could carry the uid, which would retire D's `id -u` read.

**World reads still outside emissions (Observed).** The materialization's admission of the secrets directory (`OfferedPath::existing_directory`: per-component `symlink_metadata`). It is shared with admission, so I left it, together with HOME and USER. The offline tools' migration copy and archive write are not pipeline work and were not touched.

## Step D: local user activation in the user's own manager (a83218c)

**The brief's route does not work for this daemon (Observed on ouranos, systemd 262).**
- `lojix.service` runs as `User=li` with `NoNewPrivileges`, not as root.
- From a transient system service run as li (with or without NoNewPrivileges), `systemd-run --machine=li@.host --user …` fails: `Failed to connect to system scope bus via machine transport: Permission denied`.
- From a root service, the same command works.
- With only `XDG_RUNTIME_DIR=/run/user/1001` set, `systemd-run --user` from the li service works, and the plain form reproduces 591's error.
- So I took the bead's other route: name the runtime directory from the user's identifier.

**The change (Observed).**
- There is a new emission, `ReadUserIdentifier.UserIdentifierQuery { UserName }`, which runs `id -u <user>` and gives `Identified.UserIdentifier`, `Unrecognized` or `Failed`.
- `LocalHomeActivation` gains `UserIdentifier` and runs `env -u DBUS_SESSION_BUS_ADDRESS XDG_RUNTIME_DIR=/run/user/<uid> /run/current-system/sw/bin/systemd-run --user …`.
- The systemd-run words are unchanged, and the remote activation is byte-equal.
- **Inference:** the uid comes from an `id` read rather than from configuration, because the configuration change is the step C bead above.

**New VM check, `local-user-environment-activation` (Observed; 19.4 s alone, 22.2 s in the gate).**
- Setup:
  - alice is logged in through getty autologin, so `user@1000.service` runs and `/run/user/1000/bus` exists.
  - The real daemon runs as a system service with `User=alice` and `NoNewPrivileges`, on host `atlas`.
  - Nix and the Home Manager generation are faked. `nix-env` is real.
- The check first reproduces 591: the bare `systemd-run --user` from such a service fails, naming `DBUS_SESSION_BUS_ADDRESS`.
- It then deploys `UserEnvironment … ActivateNow` with the local fast path, and asserts:
  - the deployment is `Succeeded` and Current;
  - the activation ran as uid 1000 with `--driver-version 1`, inside `/user.slice/user-1000.slice/user@1000.service/`;
  - the `home-manager` profile is the generation.

## Proof

**Argv equality against 38a57f1 (Observed).** `every_emission_runs_the_argv_23f88f2_ran_for_the_same_inputs` passes in all three gates, against the unchanged 37-line fixture. Every emission is byte-equal to 38a57f1 except these named changes, each written in the tests:
- **B2:** none of the 37 lines moves. The same-host self-switch under `Implemented` is byte-equal. Two additions are asserted whole:
  - the `LoaderInfo` read;
  - the self-switch script without the two `bootctl` lines, for `NotImplemented`.
- **C:** none moves. The file emissions are not processes, so they have no argv.
- **D:** `user local-activate` changes from program `/run/current-system/sw/bin/systemd-run` to program `env`, with `-u DBUS_SESSION_BUS_ADDRESS XDG_RUNTIME_DIR=/run/user/1000` in front of the same argv. The `id -u <user>` read is an addition.

**A/B over a fresh copy of the live store (Observed).**
- **Copy.** I took it at 15:51:12 as root. The source before, the copy, and the source after all hash `4a1efe2b…`. `lojix.service` was 0.10.6 (`hdkdqgb1…`), pid 1938170, started 12:35:56, and was not touched (`$S/sbcd/ab/copy-proof.txt`).
- **Repair.** I repaired the copy once on the builder, giving R = `1ef441fa…`. R holds 597 deployment records, 204 live generations, 2089 events, an empty deploy-job family (nothing in flight) and 4 quarantined rows (`inspect-R.txt`).
- **Runs.** I used step 5's bubblewrap harness, which has no network, D-Bus or nix-daemon socket, with the same 32 inputs. The four daemons each served their own copy of R:
  - A, 38a57f1 (`9dwa18s7…`);
  - B2 (`l5938d16…`);
  - C (`sfpi9g27…`);
  - D (`kvynv2s0…`).
- **Result.** All four are byte-identical:
  - replies `324aa87f…` (601,092 bytes);
  - stdout `d799838…` and stderr `e47755c…`, the same as at steps 10 and B;
  - final store `56f13662…`.
  - The deploy is rejected as 598, both tests are refused `NoTestDefaults`, and the configuration is reversed.
  - Hashes: `$S/sbcd/ab/hashes.txt`.
- **Cleanup.** Every store copy is deleted, here and on the builder.

**Builder cargo (Observed).**
- `cargo` on prometheus's profile is now a wrapper that refuses ("local compilation is disabled"). I ran the flake devShell's toolchain instead: `nix develop path:/tmp/offload/lojix -c env CARGO_INCREMENTAL=0 cargo …`. Incremental compilation hit a rustc ICE.
- Totals: 239 tests at B2 before its four foreground tests, 245 at C and 246 at D. Each run fails only the two `tools/tests/nexus_configuration.rs` tests that fail at every base.
- clippy `-D warnings` and fmt are clean.
- Logs are in `$S/sbcd/`.

## Notes

- `$S/sbcd/` holds the gate logs, builder test and clippy logs, the standalone VM run (`d-vm1.log`) and the A/B (`ab/`).
- This report is not committed to primary, like the reports beside it.
