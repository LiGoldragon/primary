# Night hygiene evidence

Collected evidence only; no rescan was performed for this report. No files,
pins, profiles, deployments, or system state were changed.

## Hosts reached

- `ouranos` (local)
- `prometheus.goldragon.criome` (SSH)
- `zeus.goldragon.criome` (SSH)

No other explicit SSH host candidates were configured.

## Disk evidence

| Host | Usage | Finding |
|---|---:|---|
| `ouranos` | Root ext4: 684/916 GiB (79%); inodes 13% | `/home/li` measured 275.8 GB. Deeper usage scan was time-bounded and encountered unreadable Waydroid data. |
| `prometheus` | Shared Btrfs: 1.40/1.82 TiB used; 429.7 GiB free (77%) | Data chunks 99.32% allocated-used and metadata chunks 89.78%, despite 420 GiB unallocated. Journal uses 3.1 GB; shallow scan found `/var/log` 3.1 GB and `/var/lib` 0.7 GB. |

## Pins and bindings observed

- CriomOS checkout: `400f39e121cc92f3979600b8113fd015dd851a9b`
- CriomOS `criomos-home` lock pin: `LiGoldragon/CriomOS-home@ea3a0f9c9266739646003aa265533c5a67693000`
- CriomOS-home checkout: `022c0daf4540d967cc29b5bdbdca8b354ac135a3`
- Both checkout locks pin `nixpkgs@f83fc3c…` and `home-manager@c554d344…`.
- On Prometheus, the Home Manager state profile was observed as
  `~/.local/state/nix/profiles/home-manager -> home-manager-1-link`.
- No standalone `/nix/var/nix/profiles/per-user/li/home-manager` profile was
  observed.

## Zeus and Prometheus runtime observations

| Host | Observed system path | Running kernel observed | Intended generation |
|---|---|---|---|
| Zeus | `system-72`; `/nix/store/kgg7…-nixos-system-zeus-26.11.20260813.0e251e2` | `7.1.8` | **Unverified** |
| Prometheus | `system-53`; `/nix/store/j1362…-nixos-system-prometheus-26.05.20260422.0726a0e` | `7.0.1` | **Unverified** |

The intended Zeus and Prometheus generations are unverified because Lojix was
unavailable: the local query could not decode and `lojix-daemon.service` was
inactive. The observed generation paths and running kernel strings are not a
claim of currency, and this report does not claim a kernel pass. The exact
deployed source/flake revision cannot be derived from the inspected generation
path alone.

The inspection observed `/run/booted-system` equal to `/run/current-system`
on both hosts and each system's kernel link matching `uname -r`; these are
observations only, not a pass claim.

## Evidence sources

The already collected evidence came from bounded read-only use of `df -hT`,
`df -ih`, bounded `du`, `btrfs filesystem usage -h /`,
`journalctl --disk-usage`, `readlink`, `nixos-version`, Git
`rev-parse`/`status`/`log`, `jq` over both `flake.lock` files, HM-bound SSH,
`/nix/var/nix/profiles/system`, `/run/{booted,current}-system`, and `uname -r`.
