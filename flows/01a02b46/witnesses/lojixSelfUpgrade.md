# Ouranos Lojix self-upgrade witness

Method: read landed Lojix `edbb53aab003a071ffbb0f6643e8d29c0bf9b691`, landed
CriomOS `a4322cd144821119936283339b1bc5926b97a738`, NixOS systemd unit
handling, the live `lojix-daemon.service`, and prior Ouranos self-switch
evidence. No deploy, activation, restart, copy, build, reboot, or source/runtime
mutation was performed.

## Live unit and ownership

Method: read-only `systemctl show/cat`, `ps`, and profile links on Ouranos on
2026-08-23.

- `lojix-daemon.service` is active, `Type=simple`, `User=li`, `Group=users`,
  `WorkingDirectory=/var/lib/lojix`, `Restart=on-failure`, `RestartSec=5s`, and
  `KillMode=control-group`. Main PID 1735 is
  `/nix/store/...-lojix-0.17.5/bin/lojix-daemon /run/lojix/startup.rkyv`.
- The live unit has no `ExecReload`, no drop-ins, and no `X-ReloadIfChanged`,
  `X-RestartIfChanged=false`, or `X-StopIfChanged=false` markers. Its
  `ExecStartPre` is the 0.17.5 configuration writer with the old `2700`
  timeout field. The live system and Nix system profile currently resolve to
  `/nix/store/jngjk328r5nd3xvkjw9wppb02ghm0jir-nixos-system-ouranos-26.11.20260813.0e251e2`.

Method: read landed CriomOS module at
`modules/nixos/lojix.nix:23-37,185-215` and persona projection at
`modules/nixos/lojix-persona-development.nix:41-55`.

- The landed unit writes `ConfigurationWriteRequest` without an effect-timeout
  field, then starts the selected daemon/archive. Production uses
  `NoTestDefaults`, ordinary `/run/lojix/ordinary.sock` mode 432, owner
  `/run/lojix/owner.sock` mode 384, store `/var/lib/lojix/lojix.sema`, archive
  `/run/lojix/startup.rkyv`, and daemon host `config.networking.hostName`.
- The landed unit sets no service-specific restart/reload overrides. NixOS
  defaults are `restartIfChanged=true`, `reloadIfChanged=false`, and
  `stopIfChanged=true` (`nixos/lib/systemd-unit-options.nix:544-575`). Changed
  service contents therefore stop the old service/cgroup and start the new
  unit; this is not a reload path. The unit's foreground SSH/Nix children are
  in that cgroup and are killed by the stop.

## Candidate crossing: ActivateNow

Method: read Lojix 0.17.5 commit `0d968da4` and landed 0.18.0 commit
`edbb53aab003a071ffbb0f6643e8d29c0bf9b691` at `src/schema_runtime.rs` and
`src/daemon.rs`.

- `HostActivation::runs_detached_self_switch` is true only for host
  `ActivateNow` whose target node equals the configured daemon host
  (`schema_runtime.rs:5406-5409`). For Ouranos this is the self-target case.
- The old daemon runs the remote command through explicit SSH as root, but the
  command is placed in `systemd-run --unit=lojix-self-switch-deploy-<id>
  --collect --wait --service-type=oneshot /bin/sh -c ...` owned by target PID 1
  (`schema_runtime.rs:5386-5398,5434-5452`). The script sets the system profile,
  runs the candidate `switch-to-configuration switch`, verifies the new boot
  entry, sets the EFI default, and clears a stale one-shot. The daemon and its
  foreground SSH can die while this transient continues; that is the intended
  deadlock-free self-switch shape.
- The 0.17.5 and 0.18.0 `src/daemon.rs` files are identical for deploy startup,
  reconciliation, and self-switch persistence. Both open the configured store
  and issue `ReconcilePersistedJobs` during startup (`daemon.rs:215-230`).
- On restart, an `Activating` job with no boot-once unit and node equal to
  `daemon_host` is checked against the canonical live system profile
  (`/nix/var/nix/profiles/system`). `self_switch_activation_record` accepts only
  a persisted host `ActivateNow` through `NixosSystemdBootV1` and an exact
  closure match (`daemon.rs:576-621`; `schema_runtime.rs:1899-1920`). The
  daemon then records the `Current` generation and GC root, retracting the job
  only after a successful store write (`daemon.rs:661-695`). A profile mismatch
  leaves the row for the not-yet-implemented generic S5 polling path.

Conclusion: old-daemon `Deploy.Host` `ActivateNow` is the supported no-reboot
self-upgrade crossing, with a PID-1-owned activation that survives the daemon
restart and a v0.18 startup reconciliation intended to record terminal state.
It is source/test-backed but not yet live-proven at exactly 0.17.5→0.18.0.

## Candidate crossing: TestActivation

Method: read `HostActivation::ssh_invocation` at landed
`schema_runtime.rs:5310-5338`, NixOS action semantics, and the daemon unit
above.

- `TestActivation` invokes only
  `<candidate>/bin/switch-to-configuration test`; it does not set the persistent
  system profile or boot default. It is still a live systemd activation, not a
  dry evaluation.
- Because the candidate unit definition changes `ExecStartPre`/`ExecStart`, the
  NixOS switch handling stops the old `lojix-daemon.service` and its
  `KillMode=control-group` children, then starts the candidate unit. The old
  foreground SSH cannot commit the terminal activation record.
- A test activation has no detached self-switch unit. On the new daemon,
  `Activating` with `unit=None` is not accepted by the self-switch recovery
  predicate unless the durable submission is specifically host `ActivateNow`.
  The row remains nonterminal rather than being safely adopted.

Conclusion: TestActivation may load the candidate 0.18.0 service into the live
runtime temporarily, but it is not a safe way to cross the daemon version and
does not establish a terminal deployment record. Do not use it as the upgrade
step.

## Store/startup compatibility

Method: read `LOJIX_SCHEMA_VERSION` and store-open code at landed Lojix
`src/lib.rs:49-53,495-545,645-730`, compare 0.17.5 and 0.18.0, and read the
landed startup writer/module.

- Both releases use durable Lojix store schema v4 and the same table/layout
  registration. No store reset or migration is indicated for this timeout-only
  release.
- The startup archive shape did change by removing `effect_timeout_seconds`.
  This is safe only because the landed NixOS `ExecStartPre` runs the 0.18.0
  writer before the 0.18.0 daemon starts. Reusing the old archive without the
  writer is not a supported crossing.
- Lojix v4 deliberately refuses older store schema versions and has no generic
  legacy migration. That is not the current case: the live store is v4 and both
  endpoints are v4.

## Transport and request fields

Method: read the current positional contract in `Curriculum/skills/lojix.md`,
the landed Lojix architecture and transport decoder, and historical Ouranos
self-switch evidence (`agent-outputs/LojixDeployAuthMap/Deploy-H945-LandingEvidence.md`;
`Scout-SituationalMap.md`; `flows/01a01bac/witnesses/lojixDeployment.md`).

The request must be owner-socket `Deploy.Host` with these fields, in order:

```text
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix \
  'Deploy.Host.(goldragon ouranos CompleteHost \
    /git/github.com/LiGoldragon/goldragon/datom.dotos \
    github:LiGoldragon/CriomOS/a4322cd144821119936283339b1bc5926b97a738 \
    (ssh-ng://root@ouranos.goldragon.criome root@ouranos.goldragon.criome) \
    Horizon (nixosConfigurations.target.config.system.build.toplevel) \
    NixosSystemdBootV1 ActivateNow RequireImmutable None [])'
```

The shape is authoritative: cluster, node, `CompleteHost`, proposal source,
immutable flake, request-owned `(nix_store_uri ssh_destination)`, `Horizon`,
output selector, `NixosSystemdBootV1`, `ActivateNow`, `RequireImmutable`,
optional builder, and extra substituters. `None` builder is the historical
Ouranos self-switch posture (local daemon build); it must not be silently
replaced with the Zeus `/etc/nix/machines` builder.

The root route shown above is the exact historical Ouranos route: prior
self-switches executed `ssh ... root@ouranos.goldragon.criome`, and the current
Lojix architecture requires the corresponding explicit `ssh-ng://root@...`
store URI. However, the current setup variable file only names a Zeus root
transport (`ssh-ng://root@192.168.18.95`, `root@zeus.goldragon.criome`) and has
no current Ouranos `DeploymentRoot*` pair. Therefore a fresh read-only
transport/host-key preflight must confirm the Ouranos pair immediately before
submission; if it cannot, stop rather than derive or substitute a route.

## Prior self-upgrade witness

Method: read `agent-outputs/LojixDeployAuthMap/Deploy-H945-LandingEvidence.md`.

On 2026-07-04, a live old-daemon Ouranos system switch upgraded Lojix
0.3.10→0.4.1. The transient `lojix-self-switch-deploy-41.service` completed,
the system profile/boot entry changed, and the successor daemon was active.
The old daemon stopped before committing the activation row, so the successor
answered `GenerationUnknown` on its fresh/diverged ledger. This proves the OS
and daemon process crossing can work, but also proves that “daemon active” is
not enough: the current 0.17.5→0.18.0 run must wait for the ordinary query's
terminal `Current` record and inspect the live profile if the query does not
converge.

## Sources

- `flows/01a02b46/witnesses/lojixSelfUpgrade.md` (this method-bearing witness)
- `/git/github.com/LiGoldragon/lojix@0d968da4` and `@edbb53aab003a071ffbb0f6643e8d29c0bf9b691`, `src/daemon.rs`, `src/schema_runtime.rs`, `src/lib.rs`
- `/git/github.com/LiGoldragon/CriomOS@a4322cd144821119936283339b1bc5926b97a738`, `modules/nixos/lojix.nix`, `modules/nixos/lojix-persona-development.nix`, `flake.nix`
- `/git/github.com/NixOS/nixpkgs`, `nixos/lib/systemd-unit-options.nix`, `nixos/lib/systemd-lib.nix`, `nixos/doc/manual/development/unit-handling.section.md`
- `flows/01a01bac/witnesses/lojixDeployment.md`
- `flows/3cb84d07/witnesses/lojixController.md`
- `agent-outputs/LojixDeployAuthMap/Deploy-H945-LandingEvidence.md`
- `agent-outputs/LojixDeployAuthMap/Scout-SituationalMap.md`
