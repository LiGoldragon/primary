# Morning deploy: orchestrate 0.37.0 Home switch on ouranos

Nothing was switched, activated or restarted, and the live Nexus and the Home profile were not touched. At the time of writing, the profile is still `home-manager-1039-link` and the running Nexus is still `0grjjmjc…-orchestrate-nexus-0.35.0`, bound to `orchestrate.sock` and the legacy `meta-orchestrate.sock`.

This candidate takes the place of the 0.36.1 candidate (`rn8fzfbw…`) from `flows/3ec648/reports/morning-deploy.md`. Switch to one of the two, not both in turn.

## Branch and commit

- CriomOS-home branch `f1c841-orchestrate-0.37` at commit `61abe3fb7f2922ed432d3120bb03b8174181bd38`. It is pushed and not merged.
- Its parent is `3ec648-orchestrate-0.36` `feebd281`, whose parent is `main` `0025894f`.
- The commit changes only `flake.nix` and `flake.lock`. It moves `orchestrate.url` from `bc5cd36e…` (0.36.1) to `c7c44cb39934b0727d724a6aa03a36a2a94cacf9` (0.37.0). `nix flake update orchestrate` changed no other lock node.
- The caller-set `ORCHESTRATE_SOCKET` / `ORCHESTRATE_META_SOCKET` wrapper change from 3ec648 is carried over unchanged. The built wrappers read `${ORCHESTRATE_META_SOCKET:-${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/orchestrate-nexus/orchestrate-meta.sock}`.
- The branch's `UPGRADES.md` was not touched because the brief said "nothing else". Its 0.35.0 → 0.36.1 entry still names the input `bc5cd36e`. The breaking step it describes (signal 7 exchange layer, a total wire break from 0.35) applies to this switch unchanged, because 0.37.0 has the same wire as 0.36.1.
- Worktree: `~/wt/github.com/LiGoldragon/CriomOS-home/orchestrate-037-f1c841` (jj workspace `orchestrate-037-f1c841`).

## Built store path

`/nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation`

- It was built with the same command 3ec648 used. The build ran on Prometheus (`--max-jobs 0`) in the user unit `f1c841-home-build-037` (MemoryMax=8G, RuntimeMaxSec=7200), which exited with Result=success:

  ```sh
  nix build --max-jobs 0 '.#homeConfigurations.li.activationPackage' \
    --override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system \
    --override-input horizon path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon
  ```

- `nix store diff-closures` against the live `xp12f872…` shows only `orchestrate`, `orchestrate-clients` and `orchestrate-nexus` moving, 0.35.0 → 0.37.0. Against the 0.36.1 candidate `rn8fzfbw…` the same three move, 0.36.1 → 0.37.0.
- The unit's ExecStart is `/nix/store/kjs1zikz9p0v2jnf8f1pcih6z3n4sl30-orchestrate-0.37.0/bin/orchestrate-nexus`. sd-switch therefore restarts `orchestrate-nexus` during the switch.
- The clients in the generation are `home-path/bin/orchestrate` and `home-path/bin/orchestrate-meta`. Both point to `/nix/store/vsj5mw3jfbwmclzpa4gqlgysvxfip3g2-orchestrate-0.37.0-profile/bin/…`, and both wrap `kjs1zikz…-orchestrate-0.37.0/bin/{orchestrate,orchestrate-meta}`.

## GC root

`/home/li/.local/state/f1c841/gcroots/hm-candidate-orchestrate-0.37.0` → `qda5pkid…-home-manager-generation`. It is an indirect root made with `nix-store --add-root … --indirect -r`. `nix-store -q --roots` lists that link plus the scratchpad out-link `…/scratchpad/home-037`; the scratchpad link does not last. The 0.36.1 candidate root `hm-candidate-orchestrate-0.36.1` and `hm-rollback` (→ `xp12f872…`) are still in the same directory. To clean up after the ruling, delete the links.

## Sandbox witness

Method:

- Fresh `XDG_RUNTIME_DIR` and `XDG_STATE_HOME` under `mktemp -d /tmp/claude-1001/o37.XXXX`, so the store is fresh.
- Every process ran under `env -i` with only `PATH`, `HOME` and the two XDG variables, so no `ORCHESTRATE_*` value reached it. The wrappers resolved their sockets from `XDG_RUNTIME_DIR`.
- The binaries are exactly the generation's: the Nexus taken from its unit's ExecStart, and the clients as `$G/home-path/bin/…`.
- Script: `sandbox-037.sh` in the session scratchpad. The sandbox was removed afterwards.

```
# sandbox /tmp/claude-1001/o37.23Sv  (2026-10-03T01:28:16-06:00); env -i with only PATH, HOME, XDG_RUNTIME_DIR, XDG_STATE_HOME
# nexus: /nix/store/kjs1zikz9p0v2jnf8f1pcih6z3n4sl30-orchestrate-0.37.0/bin/orchestrate-nexus  (ExecStart of the generation's orchestrate-nexus.service)
# orchestrate: /nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation/home-path/bin/orchestrate -> /nix/store/vsj5mw3jfbwmclzpa4gqlgysvxfip3g2-orchestrate-0.37.0-profile/bin/orchestrate
# orchestrate-meta: /nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation/home-path/bin/orchestrate-meta -> /nix/store/vsj5mw3jfbwmclzpa4gqlgysvxfip3g2-orchestrate-0.37.0-profile/bin/orchestrate-meta
$ orchestrate-nexus   # first stdout line
orchestrate-nexus ready
$ ls $XDG_RUNTIME_DIR/orchestrate-nexus
orchestrate-meta.sock
orchestrate-meta.sock.claim
orchestrate.sock
orchestrate.sock.claim
$ orchestrate 'Observe.Locks'
Observed.Locks.[]
exit 0
$ orchestrate-meta 'Configure.{ «/tmp/claude-1001/o37.23Sv/run/orchestrate-nexus/orchestrate.sock» «/tmp/claude-1001/o37.23Sv/run/orchestrate-nexus/orchestrate-meta.sock» }'
Configured.{ { /tmp/claude-1001/o37.23Sv/run/orchestrate-nexus/orchestrate.sock /tmp/claude-1001/o37.23Sv/run/orchestrate-nexus/orchestrate-meta.sock } True }
exit 0
$ orchestrate 'Observe.Locks'   # after Configure
Observed.Locks.[]
exit 0
# nexus exit 0 after SIGTERM
# nexus stderr:
```

Results:

- The Nexus starts and prints `orchestrate-nexus ready`. It binds `orchestrate.sock` and `orchestrate-meta.sock`.
- `Observe.Locks` answers `Observed.Locks.[]`, exit 0.
- `Configure` with the two socket paths answers `Configured.{ { … } True }`, exit 0.
- SIGTERM ends the Nexus with exit 0 and nothing on stderr.

## Pre-switch condition

```sh
ls -d /nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation
orchestrate 'Observe.Locks'
```

Switch only when the store path exists and the answer is `Observed.Locks.[]`.

The wire break from the running 0.35.0 is total, in both directions. That is the same as for 0.36.1, because 0.37.0 keeps the 0.36.x wire (orchestrate UPGRADES 0.36.1 → 0.37.0).

A Lock held across the switch survives in the store. Even so, a running script that captured a 0.35 client path would fail, so wait until no Lock is held.

## Switch command

```sh
/nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation/activate
```

This activates the exact artifact that was built and witnessed. Home Manager sets the `home-manager` profile to it as the next generation (1040 if nothing else switches first) and runs sd-switch.

Lojix's `Current` for ouranos UserEnvironment stays stale, as noted in 3ec648's report. Deploying through Lojix would need this branch merged to Home `main` and pinned by a CriomOS revision. That route is not prepared.

## Post-switch checks

1. `systemctl --user status orchestrate-nexus` shows it running from `kjs1zikz…-orchestrate-0.37.0`. To confirm, run `readlink -f /proc/$(systemctl --user show -p MainPID --value orchestrate-nexus)/exe`.
2. `orchestrate 'Observe.Locks'` answers `Observed.Locks.[]`, exit 0.
3. Rebind the meta socket. The live store predates 0.34.0 and resumes the legacy `meta-orchestrate.sock`, so a plain `orchestrate-meta` reaches nothing until the store is reconfigured and the Nexus restarted. Run Configure through the old socket name, using the caller-set variable the new wrapper honours:

   ```sh
   ORCHESTRATE_META_SOCKET=/run/user/1001/orchestrate-nexus/meta-orchestrate.sock \
     orchestrate-meta 'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
   orchestrate 'Observe.Locks'   # still Observed.Locks.[] before the restart
   systemctl --user restart orchestrate-nexus
   orchestrate-meta 'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
   orchestrate 'Observe.Locks'
   ```

   - The first call answers `Configured`. The running Nexus keeps serving the old path until the restart.
   - The call after the restart goes through the plain wrapper. It must answer `Configured.{ { /run/user/1001/orchestrate-nexus/orchestrate.sock /run/user/1001/orchestrate-nexus/orchestrate-meta.sock } True }` with exit 0, which proves the designed meta socket is bound.
   - The final `Observe.Locks` answers `Observed.Locks.[]`.

## Rollback

Go back to the live generation `xp12f872…` (0.35.0):

```sh
/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation/activate
```

This is equivalent to `home-manager-1039-link/activate`. It is held by `~/.local/state/f1c841/gcroots/hm-rollback`. sd-switch restarts `orchestrate-nexus` onto 0.35.0. Check it with `orchestrate 'Observe.Locks'`.

0.37.0 makes no store change from 0.36.x, and 0.36.1 made none it reports over 0.35.0, so 0.35.0 reopens the store. This is relayed from both UPGRADES entries; no 0.35.0 reopen of a 0.37.0-served store was witnessed here. If the meta Configure was already done, 0.35.0 binds `orchestrate-meta.sock`, which is also what its wrapper expects.

A rollback to the 0.36.1 candidate `rn8fzfbw…` is also wire-compatible and needs no restart sequence beyond what sd-switch does.

## What differs from the 0.36.1 switch

- **Artifacts.** The store path is `qda5pkid…` instead of `rn8fzfbw…`, and the Nexus is `kjs1zikz…-orchestrate-0.37.0` instead of `b2585m3p…-orchestrate-0.36.1`.
- **Dependency pins.** The orchestrate dependency pins are signal 8.0.0, signal-orchestrate and meta-signal-orchestrate 5.0.0, ethos-zero 16.0.0, and protos/datom-codec 0.32.2. 0.36.1 had signal 7.0.0, 4.0.0, 13.0.0 and 0.31.0.
- **Wire and store.** Not changed: a 0.37.0 client and a 0.36.1 Nexus greet in both directions. orchestrate-test's `orchestrate-previous-orchestrate` scenario witnesses 0.37.0 resuming a 0.36.1 store (relayed from the brief).
- **Client output.** The clients print every reply on one line (protos 0.32 `compact`). The sandbox output above shows this. A script that parsed multi-line replies from 0.36.1 would see a different shape. The forms shown in this report are already the one-line forms.
- **GC rooting.** This candidate is held by a durable GC root from the start. The 0.36.1 candidate was rooted only after the fact.
- **Witnessing.** The sandbox witness was run against the actual 0.37.0 binaries from the generation: start, `Observe.Locks` and meta `Configure`. 3ec648 witnessed its meta sequence against 0.35.0 only. The legacy-name step (Configure through `meta-orchestrate.sock` on a pre-0.34.0 store) is still not witnessed against 0.37.0. It rests on the unchanged store format and the unchanged `Configure` form.
- **Everything else is the same as for 0.36.1:** the pre-check, the switch form, the meta sequence, the rollback, and Lojix staleness.

## Sources

- CriomOS-home `f1c841-orchestrate-0.37` `61abe3fb` (parent `feebd281`), flake.nix and flake.lock.
- orchestrate `c7c44cb3` UPGRADES.md (0.36.1 → 0.37.0, 0.36.0 → 0.36.1) and README.md.
- `flows/3ec648/reports/morning-deploy.md`, and `flows/f1c841/reports/morning-deploy-f1c841.md` section (a).
- `flows/f1c841/witnesses/gc-roots.md`, for the 0.36.1 candidate and rollback roots.
- Build log of user unit `f1c841-home-build-037`, in the session scratchpad (`home-build-037.log`).
- Sandbox script and output: `sandbox-037.sh` and `sandbox-037.txt` in the session scratchpad.
- Live read (read-only): `readlink ~/.local/state/nix/profiles/home-manager`, `/proc/<MainPID>/exe` of `orchestrate-nexus`, and `ls /run/user/1001/orchestrate-nexus/`.
