# Morning deploy: Flow 0.23.0 and Message 0.19.0, next slot, Home candidate

Nothing was switched, activated or restarted. No live Nexus, store or Home profile was touched. At the time of writing, the profile is still `home-manager-1039-link` → `xp12f872…`. The live next slot still runs flow 0.17.4 and message 0.17.0, and the stable `flow-nexus` still runs 0.12.2.

This candidate sits on top of the orchestrate 0.37.0 candidate (`morning-deploy-orchestrate-037.md`). One activation of it therefore carries all three. Read that report for the orchestrate half: the pre-check, the meta rebind and the rollback.

## Branch and commit

- CriomOS-home branch `f1c841-flow-message-next` at commit `4b863bb5030fa32ff1f473afa62c3759800d411f`. It is pushed and not merged.
- Its parent is `f1c841-orchestrate-0.37` `61abe3fb`. Below that come `3ec648-orchestrate-0.36` `feebd281` and `main` `0025894f`.
- Worktree: `~/wt/github.com/LiGoldragon/CriomOS-home/orchestrate-037-f1c841`. It is the 0.37.0 candidate's worktree, now advanced onto this commit. The `f1c841-orchestrate-0.37` bookmark has not moved.

### What the commit changes

- **`flake.nix` and `flake.lock`.**
  - `flow-next` moves from `bc464e5e` (0.17.4) to `636214e515f7c09d32ae614033224aa40944423f` (0.23.0).
  - `message-next` moves from `481b579f` (0.17.0) to `ce3eb6c65a0244672b34d8e91df2e840865d64e5` (0.19.0).
  - The comments above the two inputs now name the new versions and contract revisions.
  - The lock changes only those two nodes; their input sets are unchanged.
- **`modules/home/profiles/min/flow-message-next.nix`.**
  - `flowNexusUnit` no longer exports `FLOW_SOURCE_ROOT` or the eight `FLOW_CODEX_*` variables.
  - The unit keeps the anchors, `CLAUDE_CONFIG_DIR`, `CODEX_HOME` and `PATH`. `PATH` still includes harness, which provides `flow-id`.
  - The header comment now says "Flow 0.23.0 and Message 0.19.0".
  - The unreferenced `occupiedNextFlowUnit` and `occupiedNextFlowConfigurationUnit` bindings still contain the old variables. They are dead code that no unit uses, and they were left alone because the brief said to change nothing else.
- **`modules/home/profiles/min/flow.nix`** (the stable unit).
  - The same nine exports are removed.
  - The two `let` bindings that only those exports used, `stableCodexClient` and `nextCodexClient`, are removed with them.
- **Checks that asserted the removed exports or the old pins.** These change only the generation's checks, not its contents.
  - `checks/flow-message-next` now expects the two new revisions.
  - `checks/herdr-agent-executable` loses its eight `FLOW_CODEX_*` assertions and the `flowEnvironment` binding they used.
  - `checks/flow-service-path` loses its `FLOW_SOURCE_ROOT` and `FLOW_CODEX_NEXT_SOCKET` assertions.
- **Not changed.**
  - `criomosHome.flow.enable` stays true. The stable unit is not removed (see "What stays behind").
  - `UPGRADES.md`, `message.nix` and `message-daemon` are untouched.
  - nixfmt reports four of the touched files as unformatted. They were equally unformatted at the parent, so they were not reformatted.

### Flow and Message without orchestrate

Duplicate this one commit onto `main` and build that commit instead: `jj duplicate 4b863bb5 --destination 0025894f`, then bookmark and push it.

The commit touches no orchestrate line. A trial duplicate onto `0025894f` reported `No conflicts found at this revision` and was then abandoned. That branch was neither built nor pushed tonight. Its generation would differ from live only in `flow` and `message`. Its rollback would be the live `xp12f872…`, and the orchestrate report would not apply to it.

## Generation

`/nix/store/2hnqcg3q8lwbhfmxa5nbmg9217v8cndh-home-manager-generation`

It was built on Prometheus (`--max-jobs 0`) in the user unit `f1c841-home-build-fmn` (MemoryMax=8G, RuntimeMaxSec=7200), which exited with Result=success. The command is the one the 0.37.0 candidate used:

```sh
nix build --max-jobs 0 '.#homeConfigurations.li.activationPackage' \
  --override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system \
  --override-input horizon path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon
```

`nix store diff-closures`:

- **Against the 0.37.0 candidate `qda5pkid…`:** only `flow` 0.17.4 → 0.23.0 and `message` 0.17.0 → 0.19.0.
- **Against the live `xp12f872…`:** those two, plus `orchestrate`, `orchestrate-clients` and `orchestrate-nexus` 0.35.0 → 0.37.0.

The stable `flow` 0.14.0 package (`j689l77b…`) and `message` 0.14.0 do not move.

Artifacts:

| What | Store path |
|---|---|
| `flow-nexus-next` ExecStart | `/nix/store/v945vrlsi6a79v8bighgglsvlp2qaxsz-flow-0.23.0/bin/flow-nexus` (beside it: `flow`, `flow-hook`, `flow-meta`) |
| `message-nexus-next` ExecStart | `/nix/store/np57gg4bqhln3qf1j68q2njxh0p3ckqj-message-0.19.0/bin/message-nexus` |
| `flow-configuration-next` | `/nix/store/n12rhz49canp803nhz9gcy377142y4hn-flow-configure-next`. Its datom is unchanged except that it now admits `np57gg4b…-message-0.19.0/bin/message-nexus` |
| clients | `home-path/bin/flow-next{,-meta}` → `i9dlwf27…-flow-next-clients`; `message-next{,-meta}` → `30vp3dsr…-message-next-clients` |

These unit files differ from the live generation, so sd-switch restarts them:

- `flow-nexus-next`: new ExecStart, no `FLOW_*` variables.
- `flow-configuration-next`: new script and new datom.
- `message-nexus-next`: new ExecStart.
- `orchestrate-nexus`: the orchestrate half.
- **`flow-nexus`, the stable unit.** Its nine `FLOW_*` lines are gone. Its drop-in still sets ExecStart to `c044v5pa…-flow-0.12.2`, so sd-switch restarts the stable Nexus as 0.12.2 without those variables. 0.12.2 reads each variable as an optional override; when one is absent, "an absent or malformed value leaves the stored value in force" (flow `34aaf78`, `crates/flow-nexus/src/store.rs`). So it runs on the configuration its store holds until it is retired a few steps later.

`message-daemon.service` is unchanged, so its broken `ExecStartPre` is not triggered.

## GC root

`/home/li/.local/state/f1c841/gcroots/hm-candidate-flow-message-next` → `2hnqcg3q…-home-manager-generation`. It is an indirect root made with `nix-store --add-root … --indirect -r`. `nix-store -q --roots` lists it, plus the scratchpad out-link, which does not last. `hm-candidate-orchestrate-0.37.0`, `hm-candidate-orchestrate-0.36.1` and `hm-rollback` (→ `xp12f872…`) are still in the same directory.

## Sandbox witness

Method:

- One fresh root from `mktemp -d /tmp/claude-1001/fmn.XXXX`.
- Every Nexus ran under `env -i` with exactly its unit file's `Environment=` lines, taken from the generation's own `home-files/.config/systemd/user/*.service`. In those lines `%t` was mapped to `$R/run` and `/home/li` to `$R/home`. The `XDG_RUNTIME_DIR`, `HOME` and `XDG_STATE_HOME` anchors were therefore all fresh, and no live socket or store was reachable.
- ExecStart, ExecStartPre (Message's peer links) and the `flow-configuration-next` ExecStart are the units' own. The runtime directory is made before ExecStartPre and removed after stop, as systemd does.
- Clients ran under `env -i` with only `PATH`, `HOME` and `XDG_RUNTIME_DIR`, as `<generation>/home-path/bin/…`.
- **The candidate has no 0.17.4 binary.** The 0.17.4/0.17.0-shaped stores were made by the live generation's own units and binaries (`xp12f872…`: `7z15aqi4…-flow-0.17.4`, `3v8qs8h4…-message-0.17.0`), in the same sandbox and with the same mapping. Those stores were copied aside as `.predeploy`. The candidate then opened copies of those copies, put in place.
- Script: `sandbox-fmn.sh` in the session scratchpad; full output in `sandbox-fmn.txt`. The sandbox root was removed. Two earlier runs failed on script faults: `timeout` was resolved through the unit's own PATH, and stale socket files were left after a stop. Both were fixed before this run.

The datom of each `Configured` reply is shortened to `…` below; the full lines are in `sandbox-fmn.txt`.

```
# sandbox /tmp/claude-1001/fmn.mi6Y; candidate 2hnqcg3q…; live xp12f872…
## A. fresh 0.17.4/0.17.0-shaped stores, made by the live generation's own units
# start flow-nexus-next (flow-0174): /nix/store/7z15aqi46rk73v0ahaaazg6nq1hb0vjc-flow-0.17.4/bin/flow-nexus
$ flow-configuration-next ExecStart (live)
Configured.{ { …/run/flow-next/flow/flow.sock …/run/flow-next/flow/flow-meta.sock …/home/primary { … } { … } [ … ] [ Psyche ] /nix/store/3v8qs8h4…-message-0.17.0/bin/message-nexus } NexusRestartRequired }
exit 0
$ flow-next 'List.{}'
Listed.[]
$ ExecStartPre: …-message-nexus-next-peer-links …/run
# start message-nexus-next (message-0170): /nix/store/3v8qs8h4…-message-0.17.0/bin/message-nexus
$ message-next 'QueryReceipts.m-0000'
MessageRejected.UnknownMessage
# copied aside: flow.sema.flow-0.17.4.predeploy message.sema.message-0.17.0.predeploy
## B. candidate units on copies of those stores: Flow first, then Message
# in place: copies of the .predeploy files
# start flow-nexus-next (flow-0230): /nix/store/v945vrlsi6a79v8bighgglsvlp2qaxsz-flow-0.23.0/bin/flow-nexus
# FLOW_ lines in candidate flow-nexus-next.service: 0
# beside flow-nexus: flow flow-hook flow-meta flow-nexus
$ flow-next 'List.{}'
Listed.[]
exit 0
$ flow-configuration-next ExecStart (candidate)
Configured.{ { …/run/flow-next/flow/flow.sock …/run/flow-next/flow/flow-meta.sock …/home/primary { … } { … } [ … ] [ Psyche ] /nix/store/np57gg4b…-message-0.19.0/bin/message-nexus } NexusRestartRequired }
exit 0
$ flow-next 'List.{}'
Listed.[]
exit 0
# start message-nexus-next (message-0190): /nix/store/np57gg4bqhln3qf1j68q2njxh0p3ckqj-message-0.19.0/bin/message-nexus
# message-next flow link -> …/run/flow-next/flow
$ message-next 'QueryReceipts.m-0000'
MessageRejected.UnknownMessage
exit 0
$ message-next-meta 'Send.{ [ 7d41e0 ] Soft Text.«probe» }'
SendRejected.UnknownRecipient.7d41e0
exit 0
## C. rollback: live units on the stores the candidate served
# start flow-nexus-next (flow-0174-back): …-flow-0.17.4/bin/flow-nexus
$ flow-next 'List.{}'
Listed.[]
exit 0
# start message-nexus-next (message-0170-back): …-message-0.17.0/bin/message-nexus
$ message-next 'QueryReceipts.m-0000'
MessageRejected.UnknownMessage
exit 0
```

Results:

- **Start and List.** The 0.23.0 `flow-nexus` from the generation starts on a copied 0.17.4 store and answers `Listed.[]`, before and after its meta `Configure`.
- **Configure.** The generation's own `flow-configuration-next` answers `Configured.{ … NexusRestartRequired }` with exit 0. 0.17.4 gives the same answer on a fresh store.
- **Message after Flow.** The 0.19.0 `message-nexus` starts after Flow, through its unit's peer-link ExecStartPre. Both Message CLIs answer typed replies:
  - `MessageRejected.UnknownMessage`.
  - `SendRejected.UnknownRecipient.7d41e0`. This means next Message resolved the recipient through the 0.23.0 Flow. In a broken first run with no Flow up, the same request answered `MetaRefused.PeerUnknown`.
- **Rollback.** 0.17.4 and 0.17.0 reopen the stores that 0.23.0 and 0.19.0 served, and answer.
- **Shutdown.** Every Nexus was still running at SIGTERM and exited 143, with empty stderr.

The branch's `checks.x86_64-linux.flow-message-next` was also built with the same overrides, and passed. It is a pure check that starts the stable Flow, the next Flow, the configuration and the next Message from the units on a fresh store, and asserts the next CLIs' replies. The other two touched checks also passed; see "Checks" below.

## Pre-switch conditions

Run these with nothing launching, and with no `flow-next 'Start…'` and no message-next delivery in flight that the living cares about.

```sh
ls -d /nix/store/2hnqcg3q8lwbhfmxa5nbmg9217v8cndh-home-manager-generation
readlink -f ~/.local/state/nix/profiles/home-manager        # xp12f872… (live) or qda5pkid… (if the 0.37.0 candidate was switched first)
orchestrate 'Observe.Locks'                                   # Observed.Locks.[]  (the orchestrate half; see its report)
readlink /proc/$(systemctl --user show flow-nexus-next -p MainPID --value)/exe     # …7z15aqi4…-flow-0.17.4/bin/flow-nexus
readlink /proc/$(systemctl --user show message-nexus-next -p MainPID --value)/exe  # …3v8qs8h4…-message-0.17.0/bin/message-nexus
readlink /proc/$(systemctl --user show flow-nexus -p MainPID --value)/exe          # …c044v5pa…-flow-0.12.2/bin/flow-nexus
ss -xp | grep '/run/user/1001/flow/flow'                      # no output: nothing connected to the stable Flow
cat ~/.config/systemd/user/flow-nexus.service.d/override.conf  # ExecStart= / ExecStart=…c044v5pa…-flow-0.12.2/bin/flow-nexus
nix profile list                                              # Name: flow → …c044v5pa…-flow-0.12.2
cat ~/.local/bin/message-next ~/.local/bin/message-next-meta  # exec …nwrvnmk7…-message-0.17.0/bin/message{,-meta}
flow-next 'List.{}'                                           # Listed.[ … ]  (note the rows)
command -v flow-id; ls -d /home/li/primary/flows
nix-store --add-root ~/.local/state/flow/flow-0.12.2.root -r /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2
```

Then copy the next-slot stores aside with their Nexuses stopped, so each copy is a closed store. Stop Message first, then Flow:

```sh
systemctl --user stop message-nexus-next flow-nexus-next      # flow-configuration-next stops with it (PartOf)
cp --reflink=auto ~/.local/state/flow-next/.local/state/flow/flow.sema \
  ~/.local/state/flow-next/.local/state/flow/flow.sema.flow-0.17.4.predeploy
cp --reflink=auto ~/.local/state/message-next/.local/state/message/message.sema \
  ~/.local/state/message-next/.local/state/message/message.sema.message-0.17.0.predeploy
```

## Switch command

```sh
/nix/store/2hnqcg3q8lwbhfmxa5nbmg9217v8cndh-home-manager-generation/activate
systemctl --user start flow-nexus-next
systemctl --user start flow-configuration-next
systemctl --user start message-nexus-next
```

- The three explicit starts come after activation and are idempotent. They make the order Flow, then its Configure, then Message, as Message's UPGRADES require ("start Flow first, then Message"), whatever sd-switch did with the two stopped units.
- sd-switch also restarts `orchestrate-nexus` (the orchestrate half) and the stable `flow-nexus`, which stays on 0.12.2 through its drop-in and has no `FLOW_*` overrides (see above).
- Then retire the stable Flow and the hand-written wrappers:

```sh
systemctl --user stop flow-nexus
cp --reflink=auto ~/.local/state/flow/flow.sema ~/.local/state/flow/flow.sema.flow-0.12.2.retired
mv ~/.config/systemd/user/flow-nexus.service.d/override.conf ~/.local/state/flow/override.conf.retired
rmdir ~/.config/systemd/user/flow-nexus.service.d
systemctl --user daemon-reload
nix profile remove flow
mkdir -p ~/.local/state/f1c841/retired-wrappers
mv ~/.local/bin/message-next ~/.local/bin/message-next-meta ~/.local/state/f1c841/retired-wrappers/
```

- Do not remove the drop-in before stopping the unit, or the unit falls back to Home's `flow` 0.14.0.
- The wrappers must go. `~/.local/bin` is before the Home profile on PATH, so they would shadow Home's `message-next` and speak 0.17.0's wire to a 0.19.0 Nexus.
- **Seats launched before the restart keep their environment.** A Claude seat launched by the 0.17.4 Nexus has no `flow-hook`, no Flow-given `FLOW_ID` and no `FLOW_SOCKET`, so it reports nothing until it is relaunched. Flow's 0.23.0 UPGRADES says: "Flows launched before the restart keep the environment they started with: their hooks report as under 0.22.0 until they are relaunched". Only seats launched by 0.23.0 get `FLOW_SOCKET` pointing at `/run/user/1001/flow-next/flow/flow.sock`.
- Seats resolve `flow-next` and `message-next` through the profile, so they reach the new clients on their next call, once the wrappers are gone.

## Post-switch checks

```sh
readlink /proc/$(systemctl --user show flow-nexus-next -p MainPID --value)/exe     # /nix/store/v945vrlsi6a79v8bighgglsvlp2qaxsz-flow-0.23.0/bin/flow-nexus
systemctl --user show flow-nexus-next -p Environment | grep -c FLOW_               # 0
systemctl --user show flow-configuration-next -p ActiveState,Result               # ActiveState=active Result=success
journalctl --user -u flow-configuration-next -n 3 --no-pager                      # Configured.{ … np57gg4b…-message-0.19.0/bin/message-nexus } …
readlink /proc/$(systemctl --user show message-nexus-next -p MainPID --value)/exe  # /nix/store/np57gg4bqhln3qf1j68q2njxh0p3ckqj-message-0.19.0/bin/message-nexus
readlink -f "$(command -v flow-next)"                                             # …i9dlwf27…-flow-next-clients/bin/flow-next
readlink -f "$(command -v message-next)"                                          # …30vp3dsr…-message-next-clients/bin/message-next
flow-next 'List.{}'                                                               # Listed.[ … ], the same rows as before, exit 0
message-next 'QueryReceipts.m-0000'                                               # MessageRejected.UnknownMessage
message-next-meta 'Send.{ [ <a six-hex id absent from flow-next List> ] Soft Text.«deploy check» }'   # SendRejected.UnknownRecipient.<id>
systemctl --user status flow-nexus                                                # inactive (dead); unit still defined by Home (below)
ls /run/user/1001/flow                                                            # No such file or directory
nix profile list | grep -c c044v5pa                                               # 0
readlink -f "$(command -v flow)"                                                  # …j689l77b…-flow-0.14.0/bin/flow (Home's stable package)
```

- The `Send` check names a recipient that must be unknown. Do not reuse `7d41e0` unless `flow-next 'List.{}'` lacks it. On the live host a real id would actually send.
- Launch check: it opens a real seat, so it is the living's call. Start one small Claude flow through `flow-next 'Start…'`. Then, in its pane, `printenv FLOW_SOCKET` should give `/run/user/1001/flow-next/flow/flow.sock`, and `flow-next-meta 'ReadEvents.<its FlowId>'` should give `EventsRead.{ <id> [ Started … ] }`.

## Rollback

1. Stop the next pair: `systemctl --user stop message-nexus-next flow-nexus-next`.
2. Restore the stable Flow first, so that the activation restarts it with its overrides:
   ```sh
   mkdir -p ~/.config/systemd/user/flow-nexus.service.d
   install -m 600 ~/.local/state/flow/override.conf.retired ~/.config/systemd/user/flow-nexus.service.d/override.conf
   nix profile install /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2
   mv ~/.local/state/f1c841/retired-wrappers/message-next ~/.local/state/f1c841/retired-wrappers/message-next-meta ~/.local/bin/
   ```
3. Activate the previous generation:
   - `/nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation/activate` if the 0.37.0 candidate was live before this one. This keeps orchestrate 0.37.0.
   - Otherwise `/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation/activate`. This also returns orchestrate to 0.35.0; see the orchestrate report's rollback. It is held by `hm-rollback`.
4. Restart the stable Flow and start the next pair in order:
   ```sh
   systemctl --user daemon-reload
   systemctl --user restart flow-nexus
   systemctl --user start flow-nexus-next flow-configuration-next message-nexus-next
   ```
5. Check:
   ```sh
   readlink /proc/$(systemctl --user show flow-nexus-next -p MainPID --value)/exe   # …7z15aqi4…-flow-0.17.4
   flow-next 'List.{}'
   message-next 'QueryReceipts.m-0000'
   readlink /proc/$(systemctl --user show flow-nexus -p MainPID --value)/exe        # …c044v5pa…-flow-0.12.2
   ```
6. If `flow-nexus-next` or `message-nexus-next` fails to start, or does not answer, restore the closed copies:
   ```sh
   systemctl --user stop message-nexus-next flow-nexus-next
   cp ~/.local/state/flow-next/.local/state/flow/flow.sema.flow-0.17.4.predeploy ~/.local/state/flow-next/.local/state/flow/flow.sema
   cp ~/.local/state/message-next/.local/state/message/message.sema.message-0.17.0.predeploy ~/.local/state/message-next/.local/state/message/message.sema
   systemctl --user start flow-nexus-next flow-configuration-next message-nexus-next
   ```
   Flows launched under 0.23.0 are then missing from the restored store.

The stable 0.12.2 store was copied aside and never written by another version.

## What stays behind

- **Home still defines the stable `flow-nexus` unit.** It is Flow 0.14.0 (`j689l77b…`), `WantedBy=default.target`, with no drop-in after retirement. This branch does not set `criomosHome.flow.enable = false`, because the brief said to change nothing else. After the retirement steps the unit is stopped. It could start again as 0.14.0 on `/run/user/1001/flow/` at the next login session or at an activation that changes it. Whether 0.14.0 opens the 0.12.2 store is unknown. Removing it fully takes a later Home commit with `enable = false`.
- **Home's `flow` 0.14.0 client** stays on PATH as `flow`. A hand-started harness without `FLOW_SOCKET` still reaches `/run/user/1001/flow/flow.sock`, which no longer exists after retirement. Its `flow-hook`, if it has one, fails silently.

## Checks

All three checks this branch touches were built with the same `--override-input system`/`horizon` and `--max-jobs 0`, and all three passed (exit 0):

- `checks.x86_64-linux.flow-message-next`
- `checks.x86_64-linux.flow-service-path`
- `checks.x86_64-linux.herdr-agent-executable`

The full `nix flake check` was not run. Six checks already fail at `main` (`morning-deploy-final.md`).

## Unverified

- **A store with rows.** The live 0.17.4 store has rows and a `launch-bundles` directory. The witness used a fresh, empty 0.17.4-made store, so reopening a store with rows, in both directions, is unverified. The rollback was also witnessed only on a store whose events table is empty.
- **sd-switch with the next pair stopped.** What sd-switch does when the two changed units are stopped before activation was not run. The explicit starts are written so that either outcome ends the same way.
- **The stable 0.12.2 without its overrides,** for the minutes between activation and its stop. It is derived from the 0.12.2 source and was not run.
- **The `NexusRestartRequired` answer** from the live store's Configure. In the sandbox the socket paths in the datom were the ones already served, and Message was admitted without a restart. On the live store the same holds by construction, but it was not run there.
- **`FLOW_SOCKET` reaching a real seat's hook on this host.** It is witnessed only in flow-test's `flow-claude-hook` (`reports/flow-hook-socket.md`), not with this generation.
- **The Flow+Message-only branch on `main`.** Its conflict-free apply was tried; it was not built.
- **Lojix** stays stale, as in the orchestrate report. This branch is not merged and not pinned by CriomOS.

## Sources

- CriomOS-home `f1c841-flow-message-next` `4b863bb5` (parent `61abe3fb`): flake.nix, flake.lock, `modules/home/profiles/min/{flow,flow-message-next}.nix`, `lib/stable-next-service.nix`, and `checks/{flow-message-next,flow-service-path,herdr-agent-executable}`.
- flow `636214e5` UPGRADES.md (0.23.0, 0.22.0, 0.21.0) and `34aaf78` (0.12.2) `crates/flow-nexus/src/store.rs`. message `ce3eb6c6` UPGRADES.md (0.18.0 → 0.19.0).
- `flows/f1c841/reports/morning-deploy-final.md` (B1, B2, C1), `morning-deploy-orchestrate-037.md`, and `flow-hook-socket.md`.
- Unit files of `2hnqcg3q…`, `qda5pkid…` and `xp12f872…` (`home-files/.config/systemd/user`), and `nix store diff-closures` among them.
- Session scratchpad: build log `home-build-fmn.log`, `sandbox-fmn.sh`, `sandbox-fmn.txt` and `check-*.log`.
- Live reads (read-only): `~/.config/systemd/user/flow-nexus.service.d/override.conf`, `~/.local/bin/message-next{,-meta}`, `nix profile list`, PATH order, `readlink ~/.local/state/nix/profiles/home-manager`, and `flow-next 'List.{}'`.
