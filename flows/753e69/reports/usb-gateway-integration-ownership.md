# USB gateway integration ownership

Field Sol `753e69` coordinates this integration and will own its eventual
main-merge sequence. That does not transfer any repository source ownership
or authorize a code edit.

## Disjoint implementation lanes

| Order | Workspace and paths | Accepted owner | Current state / next decision |
|---|---|---|---|
| 1 | `/home/li/wt/github.com/LiGoldragon/horizon-rs/post-terminus-horizon-data/lib/src/{proposal.rs,node.rs,horizon.rs}` and `lib/tests/{datomic_proposal.rs,node.rs,horizon.rs}` | Horizon component owner; no currently accepted individual worker | Unlocked and clean. Claim this lane to add the USB IPv4 gateway `NodeService`, Datomic codec, and viewpoint projection proof. |
| 2 | `/home/li/wt/github.com/LiGoldragon/goldragon/post-terminus-horizon-data/proposal.datomic` | Goldragon data owner; no currently accepted individual worker | Unlocked and clean. Claim only after Horizon accepts the variant; add the Ouranos record only. |
| 3 | `/home/li/wt/github.com/LiGoldragon/lojix/horizon-contract-repin-8565e8/src/{schema_runtime.rs,bootstrap.rs}` and relevant materialization test | Lojix component owner; historical Field Sol `8565e8` proposal ownership is carried through `395aed → 7091ea → 753e69`, without a source transfer | Unlocked and clean. Existing generic output already writes `horizon.json` and imports it with `builtins.fromJSON`; decide after the Horizon revision whether a pin or contract-test update is needed. |
| 4 | `/home/li/wt/github.com/LiGoldragon/CriomOS/usb-share-6db4fe/modules/nixos/node-services.nix`, `modules/nixos/network/default.nix`, a new NetworkManager capability module, and focused evaluation fixture/check | Terra is assigned permanent Ouranos NetworkManager, firewall/NAT, and Horizon-capability mutation | Unlocked and clean. Terra must choose exactly one NAT owner and implement payload-only enablement. Do not extend `network/networkd.nix`. |
| 5 | Main/pin integration in the four repositories | Field Sol `753e69` coordinates; no merge workspace or exact source lock exists | The `primary-99n-*-integration` mirrors have no working copy. The integrator must claim exact pin/merge paths when source revisions are accepted. |

## Protected concurrent work

`f72ab7` owns three disjoint protected locks: `2836`
`/home/li/wt/github.com/LiGoldragon/flow/night-messaging-0ab019`, `2862`
`/home/li/wt/github.com/LiGoldragon/signal-flow/night-messaging-0ab019`, and
`2864` `/home/li/wt/github.com/LiGoldragon/message/night-messaging-0ab019`.
They are not part of this integration. The Signal Flow workspace currently has
uncommitted `flake.nix` and `flake.lock`; do not enter any of these workspaces.

Older `542442` locks cover separate `*-542442` migration workspaces. Astra's
historical `3939` source lock is absent; `3926` covered a report only.

## Dependency and proof gates

1. Horizon type, codec, and projection proof.
2. Goldragon `proposal.datomic`, validated by that exact Horizon revision.
3. Lojix consumes/pins that revision and proves typed materialization.
4. CriomOS consumes the payload through NetworkManager and its focused check.
5. Field Sol coordinates the exact-path claims, accepted revisions, and main
   merge; activation remains separately authorized.

Goldragon validation must project every declared node with the Horizon revision
pinned by the intended Lojix revision, then show Lojix accepts typed
materialization. On Ouranos, every relevant Nix invocation is remote-only on
Prometheus: `max-jobs = 0`, builders `@/etc/nix/machines`, and fallback
disabled. CriomOS whole-system checks require Lojix-materialized `system`,
`horizon`, `deployment`, and `secrets` inputs; a bare flake evaluation is not a
valid gate. Verify that `/etc/nix/machines` selects Prometheus before the run,
and propagate the same no-fallback settings to child Nix processes.

## Sources

- `flows/753e69/reports/horizon-usb-gateway-contract.md`
- `flows/753e69/reports/network-path-plan-2026-09-21.md`
- Current `orchestrate 'Observe.Locks'` snapshot, 2026-09-21
- `AGENTS.md` and `NON_IDEAL_AGENTS.md` in the four listed workspaces
