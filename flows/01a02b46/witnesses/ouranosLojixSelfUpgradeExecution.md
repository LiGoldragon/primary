# Ouranos Lojix self-upgrade execution witness

Method: owner-socket stage submissions, ordinary-socket re-queries, and
read-only SSH/systemd/profile/boot/socket/archive/journal probes on 2026-08-23.
No TestActivation, reboot, reset, GC, hot fix, user-environment deployment, or
retry of a failed stage was performed.

## Corrected source and terminal stages

Deployment 31 was rejected before evaluation as `FlakeReferenceMalformed` after
using the older slash-revision spelling. The living explicitly authorized one
corrected new request with immutable source
`github:LiGoldragon/CriomOS?rev=a4322cd144821119936283339b1bc5926b97a738`.
All corrected requests otherwise used the stated CompleteHost proposal,
Ouranos root transport, Horizon selector, NixosSystemdBootV1,
RequireImmutable, `Some.@/etc/nix/machines`, and no substituters.

- 32 corrected Evaluate: accepted `(693 693)`, succeeded `(708 708)`.
- 33 Realize: accepted `(713 713)`, succeeded `(729 729)`.
- 34 ActivateNow: accepted `(734 734)`, failed at Activate `(758 758)`.

The post-failure ordinary node query has marker `(762 762)` and retains 34 as
`Failed.(Activate ActivationFailed)`. No retry followed. During Evaluate and
Realize, Lojix-owned `nix` work was observed in its daemon cgroup. Before the
corrected attempt, no active self-switch unit, unit file, or matching process
for historic IDs 5 or 7 was present.

## Durable and live state

The durable deployment is terminally failed. Nevertheless the persistent
profile is `system-164-link` and both it and `/run/current-system` resolve to:

```text
/nix/store/i0j3f8zqi2wfz7vbxjvi0zkjzjnam58j-nixos-system-ouranos-26.11.20260813.0e251e2
```

The running boot entry remains generation 162 without a reboot. `bootctl list`
marks generation 164 default; `bootctl status` separately prints
`Default Entry: nixos-generation-153.conf`. Both projections are reported as
observed and were not changed.

## Successor daemon and timeout removal

The successor service is active, PID 2649656, with `NRestarts=0`, running
Lojix 0.18.0. Both sockets reappeared at their expected owner and modes. The
new archive is present at `/run/lojix/startup.rkyv` (182 bytes), and the
successful writer invocation is:

```text
ConfigurationWriteRequest.{/run/lojix/ordinary.sock 432 /run/lojix/owner.sock 384 /var/lib/lojix /var/lib/lojix/lojix.sema ouranos NoTestDefaults /run/lojix/startup.rkyv}
```

This nine-field configuration has no timeout. The active 0.18 daemon opened
the existing store and answered the ordinary query, behavioral evidence that it
accepted the v4 store; no destructive store inspection or reset was used.
Strict SSH continuity held.

## PID-1 activation failure

`lojix-self-switch-deploy-34.service` set the system profile, ran candidate
`switch-to-configuration switch`, stopped 0.17.5, and started the 0.18.0
successor. It then exited `status=4/NOPERMISSION` because
`complex-init.service` failed during the candidate switch. The reported cause
was:

```text
dotos: expected ClaviFaberRequest to be a unit-variant atom or Variant.payload application block
```

No self-switch unit remains. `complex-init.service` is the only failed unit
after the crossing; `home-manager-li.service` is no longer failed.

## Result

The timeout-free Lojix 0.18.0 system is live, but deployment 34 did not
reconcile to durable Current. This is a partial self-switch; no remediation is
authorized.

## Sources

- `flows/01a02b46/reports/lojixSelfUpgrade.md`
- `flows/01a02b46/reports/ouranosStaleDeployments.md`
- `flows/01a02b46/witnesses/lojixSelfUpgrade.md`
- live requests and probes named in this witness
