# 134 — Lean Horizon, Pan-Horizon Config, and Lojix Build

Date: 2026-05-17  
Role: system-specialist

## Outcome

The `horizon-leaner-shape` sibling branch stack is now implemented far
enough for the new Horizon and new Lojix daemon to build a real CriomOS
system target.

The successful real smoke was:

- cluster: `goldragon`
- node: `zeus`
- builder: `prometheus`
- flake: `git+https://github.com/LiGoldragon/CriomOS?ref=horizon-leaner-shape`
- result: `/nix/store/fglyy0sb13kkm4dl32ldpkr4pninlks8-nixos-system-zeus-26.05.20260510.da5ad66`
- Lojix recorded: `Generation generation_12 goldragon zeus FullOs ... Built`
- Lojix pinned: `/tmp/lojix-real-build-smoke-U6PiYw/gcroots/goldragon/zeus/full-os/built/deployment_1`

## Branches Pushed

- `horizon-rs/horizon-leaner-shape` — `45056dc4`
- `lojix/horizon-leaner-shape` — `5cc1eaf6`
- `goldragon/horizon-leaner-shape` — `989572de`
- `CriomOS/horizon-leaner-shape` — `5027d9ac`
- `CriomOS-home/horizon-leaner-shape` — `e1206533`
- `CriomOS-lib/horizon-leaner-shape` — `21de5ebc`
- new repo `criomos-horizon-config/main` — `1218566e`

## Shape Changes

`criomos-horizon-config` now carries the pan-horizon constants:

- internal suffix: `criome`
- public suffix: `criome.net`
- LAN pool: `10.18.0.0/16`
- LAN prefix length: `24`
- reserved labels: `tailnet`, `vault`, `git`, `mail`

`horizon-rs` now projects those constants with cluster facts:

- cluster domain and public domain are derived, not authored in cluster data
- router SSID derives as `<cluster>.<internal>`, currently `goldragon.criome`
- LAN CIDR/gateway/DHCP pool derive by stable hash from cluster and router
- resolver listen addresses derive from loopback plus router gateway
- Tailnet base domain derives as `tailnet.<cluster>.<internal>`
- AI and VPN cluster data are now provider selections, not full catalogs

`CriomOS-lib` now owns runtime catalogs/defaults:

- local llama catalog and runtime defaults
- NordVPN server/client/DNS catalog
- resolver upstream/fallback defaults
- DHCP lease default

`CriomOS` and `CriomOS-home` enrich lean Horizon provider selections
from those CriomOS-owned catalogs.

## Verification

Passed:

- `horizon-rs`: `CARGO_BUILD_JOBS=2 cargo check --workspace`
- `horizon-rs`: `CARGO_BUILD_JOBS=2 cargo test --workspace`
- `lojix`: `CARGO_BUILD_JOBS=2 cargo check --workspace`
- `lojix`: `CARGO_BUILD_JOBS=2 cargo test --workspace`
- `CriomOS-lib`: `nix flake check --max-jobs 1 --cores 2`
- `CriomOS-home`: `nix flake check --no-build --max-jobs 1 --cores 2`
- `CriomOS`: `nix flake check --no-build --max-jobs 1 --cores 2` with generated `zeus` Horizon, system, deployment, and secrets inputs
- `CriomOS`: `nix build --dry-run --max-jobs 1 --cores 2 .#nixosConfigurations.target.config.system.build.toplevel` with generated `zeus` inputs
- `lojix`: impure real-build smoke, `zeus` target built through `prometheus`

## Remaining Caveat

The `prometheus` full-system dry-run reaches the large-AI model
closure. That exposed a separate problem: the llama model catalog makes
the OS system closure reference GGUF fetch derivations, and the dry-run
failed on a missing GGUF `.drv`. Even once that is corrected, building
the full `prometheus` system would pull large model payloads into the
system build.

That should be treated as its own follow-up architecture issue: local
AI model materialization probably wants a runtime/cache-managed path,
not unconditional inclusion in the NixOS system closure.

