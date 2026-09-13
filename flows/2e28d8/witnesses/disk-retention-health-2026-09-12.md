# Disk retention and activation health — 2026-09-12

## Scope and method

This witness rechecked the host after the earlier Lojix deployment numbered 245
partially activated CriomOS revision `11d41d7e7fa2`. It used live profile
links, `systemctl`, `journalctl`, `bootctl`, the typed ordinary Lojix query
client, and scoped profile-link enumeration. It did not reboot, invoke
`sudo`, open a polkit prompt, or submit a new deployment.

## Activation health

`/run/current-system` and `/nix/var/nix/profiles/system` both resolve to
`/nix/store/41cvi7l9rjy3n05jixzqdk937rg8gz27-nixos-system-ouranos-26.11.20260813.0e251e2`,
the live system profile generation 183. `bootctl status` identifies generation
183 as the default boot entry, built on 2026-09-12. This is a completed
non-reboot switch, not a pending boot-only deployment.

The current Lojix daemon is active. It owns `/run/lojix/ordinary.sock` and
`/run/lojix/meta.sock`, both created at 10:20 CST. Its initial three restarts
were caused by the old store being momentarily locked; it became ready at
10:20:41 and has remained active. The journal then records terminal deployment
states at 10:22:33 and 10:42:46.

The live typed query `lojix 'Query.ByNode.{ goldragon ouranos
Some.CompleteHost }'` reports deployment 4 as `Completed` with `Succeeded`,
generation 4 as `Current`, and the same `41cvi…` closure as the active system.
Deployment 3 is also `Succeeded` and retains the preceding `bbmk…` closure as
`Recent`. Thus the declared activation is already reconciled and complete; no
Lojix or meta-Lojix repair request was needed or sent.

The query for the historical numeric identifier, `lojix
'Query.ByDeployment.{ 245 }'`, returns an empty listing with database marker
`{ 112 112 }`. That identifier belongs to the pre-reset Lojix store and cannot
be used to drive an activation in the new daemon. The persisted current ledger
instead records the successful reconciliation as deployments 3 and 4.

The activation journal explains the earlier partial state. Deployment 2 set
the `bbmk…` system profile and ran its switch, but `switch-to-configuration`
reported `lojix.service` failed during the store-lock restart and therefore
returned status 4. Deployment 3 subsequently records that same closure as a
successful live generation, and deployment 4 records the current closure.

## Retention health

`nix-gc.timer` is enabled and active with `OnCalendar=daily` and
`Persistent=true`; it is next scheduled for 2026-09-13 00:00 CST. Its most
recent service run exited successfully at 00:04:24 CST on 2026-09-12 and
reported 16,450 paths deleted and 30.4 GiB freed.

Three privileged system profile generations remain: 181 (`8cvw…`), 182
(`bbmk…`), and the active 183 (`41cvi…`). Enumerating or pruning the system
profile through `nix-env` is blocked for this user by
`/nix/var/nix/profiles/system.lock` permission. Bird's home/profile tree is
also inaccessible (`/home/bird: Permission denied`), so its retention state
could not be enumerated or changed without an authorized privileged owner
operation.

At observation time the root filesystem had 12,021,325,824 bytes free
(99% used). This is materially worse than the previous flow's 330,433,753,088
bytes free after its collection. A broad `du`/dry-run-GC measurement did not
finish within the 30-second nonblocking command budget, so this witness does
not attribute the new consumption. The successful scheduled collection proves
the declared timer is working, but retention health is currently degraded by
the low remaining space.

## Remaining blockers

- A privileged owner must inspect and, if appropriate, prune old system and
  Bird profile generations; this flow has no noninteractive privilege path.
- The rapid post-GC disk growth needs a bounded root-cause measurement before
  another cleanup run can be claimed effective.
- The retired deployment 245 has no record in the new Lojix database. Current
  deployments 3 and 4 provide the activation evidence instead.

## Coordination

Lock `1389` (`DiskRetentionHealth20260912`) covered this file and is released
after its commit and push.

