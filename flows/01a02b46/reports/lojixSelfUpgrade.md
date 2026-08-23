# Safe Ouranos Lojix self-upgrade path

## Decision

The safe supported no-reboot crossing is one owner-only `Deploy.Host` with
`CompleteHost`, `Horizon`, immutable CriomOS
`a4322cd144821119936283339b1bc5926b97a738`, `NixosSystemdBootV1`, and
`ActivateNow`. The old 0.17.5 daemon deliberately runs this self-target action
inside a PID-1-owned `lojix-self-switch-deploy-<id>` transient unit. That unit
survives the daemon service stop/restart caused by the candidate NixOS unit
change. The new 0.18.0 daemon rewrites its startup archive, opens the same v4
store, and reconciles the exact candidate profile match into a durable `Current`
generation.

Do not use `TestActivation` as the crossing. It invokes the candidate
`switch-to-configuration test` in the foreground, and NixOS's default changed
service handling stops the old daemon cgroup (including the SSH child) before
starting the new unit. There is no detached unit and no terminal-record recovery
for a test row. It can load 0.18.0 into live systemd temporarily, but does not
persist the system profile or prove a terminal record.

## Staged operator plan

1. Read-only preflight: confirm the target is Ouranos, owner socket is
   `/run/lojix/owner.sock`, daemon is 0.17.5/User=li, store is v4, the landed
   candidate and proposal revision are immutable, and no unrelated deployment
   job is active. Confirm the exact root transport pair and host key. The
   historical pair is
   `(ssh-ng://root@ouranos.goldragon.criome root@ouranos.goldragon.criome)`;
   current `SKILL_VARIABLES.md` does not authorize borrowing the Zeus pair.
2. Submit the exact `Deploy.Host` shape recorded in the witness, with
   `ActivateNow`, not TestActivation. `None` builder is the historical
   self-target posture; do not add `/etc/nix/machines`.
3. Treat the immediate owner reply as admission only. Re-query ordinary
   `Query.ByDeployment` or `Query.ByEventLog` until a terminal result is
   observed. During the crossing, expect the old daemon/socket connection to
   disappear briefly; the remote transient is the durable activation owner.
4. Verify all three independent outcomes: candidate system profile and
   `/run/current-system` match the realized closure; the new daemon is active
   from the 0.18.0 store with the new startup archive; and ordinary Lojix query
   reports `CompleteHost` `Current` for the deployment. If the query does not
   converge, inspect the durable job row/profile/journal and report Lojix state
   separately from the live system; do not infer success from process liveness.

## Stop conditions and unresolved questions

- Stop if the Ouranos root transport pair or host key is not freshly confirmed;
  the daemon's current request-owned transport is not derived from node names.
- Stop if the candidate is not exactly CriomOS `a4322cd...` with Lojix
  `edbb53a...`, or if the candidate unit would not run the new
  `ConfigurationWriteRequest` writer before daemon start.
- Stop if the live store is not v4 or startup compatibility reports a table
  mismatch. The supported path has no automatic reset/migration for that case.
- Stop on activation failure, profile mismatch, missing transient unit, or a
  nonterminal `Activating` row after the successor starts. The 0.18 recovery
  only adopts exact host `ActivateNow` + `NixosSystemdBootV1` + live-profile
  closure matches; generic S5 activation-unit polling is not implemented.
- No reboot is part of this plan. `lojix-bootstrap` is not a no-reboot
  replacement: `BuildOnly` cannot activate, and its supported remote mode is
  `BootOnce` (sets a one-shot boot entry and records bootstrap evidence), not an
  immediate Lojix daemon switch or Lojix ledger reconciliation. If the old
  daemon cannot admit the typed request, stop and return that incompatibility
  rather than inventing a manual hotfix or reboot path.

## Sources

- [method-bearing self-upgrade witness](../witnesses/lojixSelfUpgrade.md)
- [Ouranos controller witness](../../3cb84d07/witnesses/lojixController.md)
- [prior Ouranos self-upgrade landing](../../../agent-outputs/LojixDeployAuthMap/Deploy-H945-LandingEvidence.md)
- [current landed timeout-removal report](./lojixTimeoutRemovalImplementation.md)
