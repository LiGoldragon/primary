# Ouranos ClaviFaber recovery witness

Method: immutable owner-socket deployment stages, durable ordinary-socket
queries, strict SSH, and read-only systemd/profile/boot/socket/archive/journal
and publication-metadata probes on 2026-08-23. No TestActivation, reboot,
manual service or EFI edit, hot fix, reset, garbage collection,
user-environment deployment, or retry of a failed stage was performed.

## Stages

All requests used immutable CriomOS
`github:LiGoldragon/CriomOS?rev=3bcd9189f72cfef8b17d335d459936b857a38214`,
the existing Ouranos CompleteHost proposal, root transport, Horizon selector,
NixosSystemdBootV1, RequireImmutable, builder `Some.@/etc/nix/machines`, and
no substituters.

- deployment 35 Evaluate succeeded at marker `(778 778)`;
- deployment 36 Realize succeeded at marker `(799 799)`;
- deployment 37 ActivateNow failed at Activate at marker `(828 828)`.

The post-failure node query's marker is `(832 832)` and keeps deployment 37 as
`Failed.(Activate ActivationFailed)`. No retry followed.

## Live state after the terminal failure

Despite the durable failure, candidate `switch-to-configuration switch`
finished successfully. Persistent `system-165-link` and `/run/current-system`
both resolve to:

```text
/nix/store/fvfkqpjy3zglilhgfaykqlragr73ck4x-nixos-system-ouranos-26.11.20260813.0e251e2
```

`bootctl list` marks generation 165 as the effective default EFI entry. The
currently running boot entry is generation 162 without a reboot. `bootctl
status` still separately prints `Default Entry: nixos-generation-153.conf`;
the two boot projections are preserved as observations.

`complex-init.service` is `active (exited)` with `Result=success` and exit
status 0. The public publication output exists at
`/etc/criomOS/complex/publication.dotos`, owned `root:root`, mode `0644`, size
115 bytes. Its content was not read. No unit is currently failed.

## Controller and activation journal

Lojix 0.18.0 remains active, PID 2649656, with `NRestarts=0`; its ordinary and
owner sockets are present with expected modes and ownership. The startup writer
remains the nine-field request with no timeout, and the active daemon answers
ordinary queries, which demonstrates acceptance of its existing v4 store.

The PID-1 transient `lojix-self-switch-deploy-37.service` set the generation
165 system profile and journaled `finished switching to system configuration`.
It then exited status 1 after the switch, and Lojix wrote its durable activation
failure. The available journal does not identify which post-switch command
returned status 1; no cause beyond that observation is claimed.

## Result

The ClaviFaber fix is live and the originally failed service now succeeds, but
deployment 37 did not reconcile to durable Current. This is an ambiguous
partial state. No recovery is authorized.

## Sources

- `flows/01a02b46/reports/ouranosLojixSelfUpgradeFinal.md`
- `flows/01a02b46/witnesses/ouranosLojixSelfUpgradeExecution.md`
- live requests and probes named in this witness
