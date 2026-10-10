# Ouranos Lojix self-upgrade preflight

Method: read-only `nix store ping`, strict-host-key SSH, remote `systemctl`,
`bootctl`, `df`, `lojix-inspect-store`, and local ordinary-socket Lojix queries
on 2026-08-23. No owner-socket request, build, closure copy, activation,
restart, reboot, reset, garbage collection, or runtime mutation was performed.

## Route and host

The requested historical transport resolved to the requested host:

- `nix store ping --store ssh-ng://root@ouranos.goldragon.criome` reported
  `Trusted: 1`.
- Strict SSH host-key checking accepted the existing `ouranos.goldragon.criome`
  ED25519 known-host record, fingerprint
  `SHA256:x5qI23+57xXlINVab5szQd2UVgwb4F9a9PzwLJj6FCw`.
- The remote hostname is `ouranos`; the observed machine-id digest is
  `4397cc32e0c45d8900421c99db96e83eee53a482ffaecd19339d1a83eb33df23`.

## Baseline

- Persistent system profile and `/run/current-system` both resolved to
  `/nix/store/jngjk328r5nd3xvkjw9wppb02ghm0jir-nixos-system-ouranos-26.11.20260813.0e251e2`.
- The current default boot entry is NixOS generation 163. The current-entry ID
  reported by systemd-boot is
  `nixos-f038b2d30d75e3e63ff30e3b6d9325548e653d272c81b304b6c32c5ca53e0ce1.conf`;
  this pre-existing difference was observed but not changed.
- `/nix/store` had `411941621760` bytes available at the initial preflight.
- `lojix-daemon.service` was `active (running)`, owned by `li`, PID 1735, from
  `lojix-0.17.5`; its active startup writer had the old ten-field request with
  `2700` as the effect timeout. Both Lojix sockets existed with the expected
  owner and mode: ordinary `660 li:users`, owner `600 li:users`.
- `CheckHostKeyMaterial` returned
  `KeyMaterialChecked.(ouranos [] (687 687))`. The ordinary `ByNode` query
  also returned state marker `(687 687)`.
- `lojix-inspect-store` could not acquire the running daemon's store lock, so
  it did not independently read the live schema. It reported `Database already
  open. Cannot acquire lock.` No reset or workaround was attempted.
- Pre-existing failed units were `complex-init.service` and
  `home-manager-li.service`.

## Durable deployment gate

The first ordinary `Query.ByNode.(goldragon ouranos None)` and a re-query both
reported two nonterminal CompleteHost jobs:

- deployment 5: `Host.ActivateNow`, marker `(62 62)`, state `Copying`;
- deployment 7: `Host.ActivateNow`, marker `(98 98)`, state `Copying`.

They have no terminal marker or terminal outcome in the current durable reply.
The re-query preserved both records and returned state marker `(687 687)`.
The running service remained active with `NRestarts=0` afterwards.

`Query.ByDeployment.5` and `.7` were rejected by this client's parser; the
parenthesized alternatives reached the ordinary socket but ended with frame
EOF. The supported `ByNode` query above is the durable witness used for the
gate. No retry, store edit, or manual reconciliation was attempted.

## Result

The historical Ouranos route and host identity passed, but the required empty
unrelated-job gate did not: deployments 5 and 7 are nonterminal. In addition,
the live store schema could not be independently inspected while the daemon
holds its lock. Evaluate was not submitted, so Realize and ActivateNow were
not eligible.

## Sources

- `flows/01a02b46/reports/lojixSelfUpgrade.md`
- `flows/01a02b46/witnesses/lojixSelfUpgrade.md`
- `flows/01a02b46/vision/zeusUpdate.md`
- live read-only commands named in this witness
