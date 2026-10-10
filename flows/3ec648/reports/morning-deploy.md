# Morning deploy: orchestrate 0.36.1 Home switch on ouranos

Nothing was switched or restarted tonight, and the live Nexus was not touched. The CriomOS-home branch `3ec648-orchestrate-0.36` (commit `feebd281a0bdd02fc67ef410677f612ce467990c`, pushed, not merged) does two things. It repins `orchestrate` to `bc5cd36e81df395ed1f84e2e3e98d5a6ee90bf8c` (0.36.1). It also makes the installed `orchestrate` and `orchestrate-meta` wrappers honour a caller-set `ORCHESTRATE_SOCKET` / `ORCHESTRATE_META_SOCKET`, falling back to `XDG_RUNTIME_DIR` otherwise. Its parent is Home `main` `0025894f`, which is the source of the live generation.

## Built store path

`/nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation`

- It was built on Prometheus (`--max-jobs 0`) in the user unit `3ec648-home-build` (MemoryMax=8G, RuntimeMaxSec=7200). The build used `homeConfigurations.li.activationPackage` with Lojix's ouranos user-environment inputs: `--override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system` and `--override-input horizon path:…/user-environment/horizon`.
- Control: the same command at `main` `0025894f` produced `/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation`. That is exactly the live Home generation (`~/.local/state/nix/profiles/home-manager` -> `home-manager-1039-link`). The method therefore reproduces live.
- `nix store diff-closures` from live to the new generation shows only `orchestrate`, `orchestrate-clients` and `orchestrate-nexus` moving from 0.35.0 to 0.36.1. The unit's ExecStart is now `/nix/store/b2585m3pkgy8yxsxdpahsazz11rlvnrm-orchestrate-0.36.1/bin/orchestrate-nexus`, so sd-switch restarts `orchestrate-nexus` during the switch.

## Pre-switch condition

```sh
orchestrate 'Observe.Locks'
```

Switch only when the answer is `Observed.Locks.[]`. The wire break is total: a 0.35 client cannot talk to a 0.36 Nexus, and the reverse fails too. A flow that holds a Lock across the switch could still release it afterwards, because the store carries it. However, any running script that captured a 0.35 client path would fail. Wait until no Lock is held.

## Switch command

```sh
/nix/store/rn8fzfbws25svmzpkfh2c9k7khnlzrx9-home-manager-generation/activate
```

This activates the exact artifact that was built and checked. The Home Manager activation sets the `home-manager` profile to it as generation 1040 and runs sd-switch. Lojix's `Current` for ouranos UserEnvironment is already stale (`y2mh…`, not the live `xp12f872…`), and this switch does not refresh it. To deploy through Lojix instead, CriomOS-home must first merge this branch to `main`, and a CriomOS revision must pin it. The CriomOS `main` `6485b64e` currently pins Home `acf6d376`, which is older than live. Then use `lojix-meta 'Deploy.UserEnvironment.{ goldragon ouranos li … HomeManagerNixProfileV1 ActivateNow RequireImmutable … }'` at that CriomOS revision. That route is not prepared here.

## Post-switch checks

1. `systemctl --user status orchestrate-nexus` shows it running from `…-orchestrate-0.36.1`.
2. `orchestrate 'Observe.Locks'` answers `Observed.Locks.[]` (exit 0) from the 0.36.1 Nexus over the new wire.
3. The meta socket. The live store predates 0.34.0 and binds the legacy `meta-orchestrate.sock`, and the store persists that path across the restart. A plain `orchestrate-meta` call would therefore answer `Unreachable.{ …/orchestrate-meta.sock … }`. The procedure is in `flows/3ec648/witnesses/orchestrate-meta-socket.md`. The new wrapper honours the caller's value, so the installed client reaches the legacy name:

   ```sh
   ORCHESTRATE_META_SOCKET=/run/user/1001/orchestrate-nexus/meta-orchestrate.sock \
     orchestrate-meta 'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
   orchestrate 'Observe.Locks'   # still Observed.Locks.[] before the restart
   systemctl --user restart orchestrate-nexus
   orchestrate-meta 'Configure.{ «/run/user/1001/orchestrate-nexus/orchestrate.sock» «/run/user/1001/orchestrate-nexus/orchestrate-meta.sock» }'
   ```

   The first call answers `Configured`, and the running Nexus keeps serving the old path until the restart. The last call, made after the restart through the plain wrapper, must answer `Configured.{ { …/orchestrate.sock …/orchestrate-meta.sock } True }` (exit 0). That proves the designed meta socket is bound. Finish with `orchestrate 'Observe.Locks'` once more.

The meta sequence was witnessed against 0.35.0 in the sandbox. Against 0.36.1 it rests on two points: the store format is unchanged (UPGRADES 0.36.1), and the `Configure` form is the same in the 0.36.1 README.

## Rollback

Go back to the previous generation, the live `xp12f872…` (0.35.0). The 0.36.1 Nexus does not change the store format, so 0.35.0 opens it again:

```sh
/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation/activate
```

(equivalently `home-manager-1039-link/activate`). sd-switch restarts `orchestrate-nexus` back onto 0.35.0. Check it with `orchestrate 'Observe.Locks'`. If the meta Configure was already done, 0.35.0 binds `orchestrate-meta.sock`, which matches its wrapper too.

## Checks run on the branch

- `checks.x86_64-linux.orchestrate-wrapper-fallback` passed (`/nix/store/saghazavysnmbk3qfy4ybfmiq9r69bgm-orchestrate-wrapper-fallback`). It now covers three cases: a caller-set value wins over `XDG_RUNTIME_DIR`; with no caller value, `XDG_RUNTIME_DIR` decides; with neither, `/run/user/<uid>` is used. The extended check was first run against the unchanged wrapper and failed there. `orchestrate-service-path` also passed.
- The built wrapper itself, with `ORCHESTRATE_SOCKET=/tmp/claude-1001/none/o.sock`, answered `Unreachable.{ /tmp/claude-1001/none/o.sock … }`. It honours the caller's value with the real 0.36.1 client.
- `nix flake check --keep-going` (same overrides, Prometheus) exited 1. Six checks failed, and every one also fails at `main` `0025894f` with the identical derivation:
  - `ai-agent-launch-orchestration`: eval assertion `elem codexCliPackage profile.home.packages`.
  - `codex-remote`: `46jy25yi…-codex-remote-contract.drv`.
  - `codex-remote-control-vm`: socket mode `stat … = 600` assertion.
  - `session-variables`: `m5q07sci…-home-session-variables.drv`.
  - `pkgs-mentci`: `meta-signal-mentci` build script, `q61c1w84…-mentci-0.5.0.drv`.
  - `main-contract-pins`: depends only on that same failing mentci derivation.

  None of them involves orchestrate. Every other check passed.

UPGRADES.md on the branch records the breaking switch.

## Flow upgrade (not part of this switch)

Relayed from the coordinator and not verified here. Flow 0.18.0 (`main` `ae050272`) no longer reads `FLOW_SOURCE_ROOT` or `FLOW_CODEX_*`. CriomOS-home still exports them, in `modules/home/profiles/min/flow.nix:81-89` (stable) and `modules/home/profiles/min/flow-message-next.nix:114-122,150-` (next slot). A fresh next-slot store seeds `~/.local/state/flow-next/primary` as its source root and needs a meta `Configure` after start. This branch does not change Flow (`flow` stays `9fcd625a` and `flow-next` stays `bc464e5e`). The living rules on that upgrade separately.

## Sources

- CriomOS-home branch `3ec648-orchestrate-0.36` `feebd281`. Its parent is `main` `0025894f`.
- orchestrate `bc5cd36e81df` UPGRADES.md (0.35.0 to 0.36.0, 0.36.0 to 0.36.1) and README.md.
- `flows/3ec648/witnesses/orchestrate-meta-socket.md`.
- `flows/d5b96b/reports/codex-rotation-complete.md`, which records the live generation `xp12f872` built from Home `0025894f`.
- Lojix `Query.ByNode.{ goldragon ouranos None }` (ordinary socket), for Current `y2mh…`.
- Build logs: user units `3ec648-home-build` and `3ec648-main-control`. The logs are in the session scratchpad.
