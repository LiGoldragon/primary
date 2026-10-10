---
title: 303.2 - Dependency/version inventory
role: operator
variant: Audit
date: 2026-06-04
topics: [repository-stack, dependencies, rust, nix]
parent_meta_report: reports/operator/303-Audit-repository-stack-state-2026-06-04
slot: 2
description: |
  Inventory of important Cargo, lockfile, flake, and package-version pins
  across the active repository stack named by protocols/active-repositories.md.
  Highlights Rust edition/rust-version clusters, important dependency locks,
  Nix input divergence, replacement-stack worktrees, and deploy-stack pin drift.
---

# 303.2 - Dependency/version inventory

## Scope and method

This pass covers the 76 table-listed repositories in
`/home/li/primary/protocols/active-repositories.md`, plus
`CriomOS-lib` because the same protocol names it in the two deploy stacks at
lines 124-125 and 141-144. All table-listed repositories have local checkouts.

Replacement-stack inventory uses the active `horizon-leaner-shape` worktrees
for `signal-lojix` and `lojix` because the protocol says implementation lands
there (`/home/li/primary/protocols/active-repositories.md:111-112`).
`criomos-horizon-config` has a canonical checkout but no matching
`horizon-leaner-shape` worktree.

`signal-frame` is not a table-listed active repo, but it is included as a
dependency evidence repo because the requested dependency family explicitly
includes it and active locks depend on `signal-frame 0.1.0`.

Evidence came from structured reads of `Cargo.toml`, `Cargo.lock`,
`flake.lock`, and the one `package.json`/`package-lock.json` found in the
active set. No `/nix/store` search was used.

## Repository classification

| Class | Count | Repositories |
|---|---:|---|
| Active/current | 57 | `primary`, `lore`, `persona`, `mind`, `router`, `message`, `introspect`, `signal-introspect`, `system`, `harness`, `terminal`, `terminal-cell`, `sema`, `signal-sema`, `sema-engine`, `schema`, `schema-next`, `schema-rust-next`, `triad-runtime`, `spirit-next`, `version-projection`, `signal-version-handover`, `owner-signal-version-handover`, `upgrade`, `signal-upgrade`, `meta-signal-upgrade`, `signal-core`, `signal`, `owner-signal-persona`, `signal-engine-management`, `signal-persona-origin`, `signal-agent`, `owner-signal-agent`, `signal-message`, `signal-router`, `owner-signal-router`, `signal-system`, `signal-harness`, `signal-terminal`, `owner-signal-terminal`, `signal-mind`, `owner-signal-mind`, `orchestrate`, `signal-orchestrate`, `owner-signal-orchestrate`, `signal-criome`, `repository-ledger`, `signal-repository-ledger`, `owner-signal-repository-ledger`, `nexus`, `nexus-cli`, `nota`, `nota-next`, `nota-codec`, `nota-derive`, `nota-config`, `CriomOS-lib`. |
| Adjacent active | 16 | `criome`, `cloud`, `signal-cloud`, `owner-signal-cloud`, `domain-criome`, `signal-domain-criome`, `owner-signal-domain-criome`, `chroma`, `CriomOS`, `CriomOS-home`, `mentci-lib`, `horizon-rs`, `lojix-cli`, `goldragon`, `chronos`, `TheBookOfSol`. |
| Replacement stack | 3 | `signal-lojix`, `lojix`, `criomos-horizon-config` (`/home/li/primary/protocols/active-repositories.md:103-113`). |
| Retired/compatibility/stale | 1 | `signal-persona`, explicitly "Retired compatibility shim" at `/home/li/primary/protocols/active-repositories.md:51`. |
| Missing local checkout | 0 | None among the table-listed repositories. |

Classification correction: `terminal` stays active/current even though its
row says old terminal-brand mux helpers are retired
(`/home/li/primary/protocols/active-repositories.md:31`). `version-projection`
stays active/current even though its domain is compatibility policy
(`/home/li/primary/protocols/active-repositories.md:41`).

## Rust toolchain surface

All Rust package manifests found in scope use edition `2024`. The main split
is `rust-version`.

| Rust surface | Repositories | Evidence |
|---|---|---|
| `edition = "2024"`, `rust-version = "1.89"` | `mind`, `router`, `harness`, `terminal`, `orchestrate`, `nexus`, `criome` | `mind` has `/git/github.com/LiGoldragon/mind/Cargo.toml:4-5`; `criome` has `/git/github.com/LiGoldragon/criome/Cargo.toml:4-5`. |
| `edition = "2024"`, `rust-version = "1.88"` | `persona`, `message`, `introspect`, `signal-introspect`, `system`, `terminal-cell`, `signal-router`, `chroma`, `lojix` worktree | `persona` has `/git/github.com/LiGoldragon/persona/Cargo.toml:4-5`; `lojix` has `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/Cargo.toml:4-5`. |
| `edition = "2024"`, `rust-version = "1.85"` | 52 repositories, mostly schema, signal, sema, nota, cloud/domain, and smaller contract/runtime crates | Examples: `/git/github.com/LiGoldragon/schema-next/Cargo.toml:4-5`, `/git/github.com/LiGoldragon/spirit-next/Cargo.toml:4-5`, `/git/github.com/LiGoldragon/signal-frame/Cargo.toml:8-9`, `/home/li/wt/github.com/LiGoldragon/signal-lojix/horizon-leaner-shape/Cargo.toml:4-5`. |
| `edition = "2024"`, no `rust-version` | `horizon-rs`, `lojix-cli` | `/git/github.com/LiGoldragon/horizon-rs/cli/Cargo.toml:4`, `/git/github.com/LiGoldragon/lojix-cli/Cargo.toml:4`. |
| No Cargo surface in scope | `lore`, `CriomOS`, `CriomOS-home`, `goldragon`, `TheBookOfSol`, `criomos-horizon-config`, `CriomOS-lib` | These have no in-scope `Cargo.toml`; `CriomOS-home` has a small package-json wrapper, covered below. |

## Cargo dependency locks

| Dependency family | Inventory | Evidence |
|---|---|---|
| `kameo` | All active locks that include `kameo` resolve to `0.20.0` (14 repos). Manifests mix crates.io `0.20` and a LiGoldragon fork branch: `mind` and `message` use `github.com/LiGoldragon/kameo` branch `persona-lifecycle-terminal-outcome`; the lock still records package version `0.20.0`. | `/git/github.com/LiGoldragon/mind/Cargo.toml:20`, `/git/github.com/LiGoldragon/message/Cargo.toml:27`, `/git/github.com/LiGoldragon/mind/Cargo.lock:193-194`, `/git/github.com/LiGoldragon/persona/Cargo.lock:385-386`. |
| `redb` | Two live baselines exist. `redb 4.1.0` is the current daemon/storage lane in `persona`, `mind`, `router`, `sema`, `sema-engine`, `orchestrate`, `repository-ledger`, `criome`, `chronos`, and `lojix`. `redb 2.6.3` remains in schema-derived and upgrade surfaces including `schema-next`, `schema-rust-next`, `spirit-next`, `signal-upgrade`, `meta-signal-upgrade`, and `chroma`. `upgrade` currently locks both `2.6.3` and `4.1.0`. | `persona` manifest asks for `redb = "4"` at `/git/github.com/LiGoldragon/persona/Cargo.toml:27`; `persona` locks `4.1.0` at `/git/github.com/LiGoldragon/persona/Cargo.lock:712-713`. `schema-next` asks for `2.6.3` at `/git/github.com/LiGoldragon/schema-next/Cargo.toml:17` and locks it at `/git/github.com/LiGoldragon/schema-next/Cargo.lock:209-210`. |
| `rkyv` | The active locks converge on `rkyv 0.8.16` (62 scoped repos plus `signal-frame`). Most manifests use the portable feature set `std`, `bytecheck`, `little_endian`, `pointer_width_32`, `unaligned` with default features off. `router`, `message`, and `introspect` use bare `0.8` in the manifest but still lock `0.8.16`. | Portable feature examples: `/git/github.com/LiGoldragon/signal-frame/Cargo.toml:22`, `/git/github.com/LiGoldragon/mind/Cargo.toml:23`, `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/Cargo.toml:51`. Lock examples: `/git/github.com/LiGoldragon/mind/Cargo.lock:413-414`, `/git/github.com/LiGoldragon/signal-frame/Cargo.lock:243-244`. |
| `tokio` | `tokio 1.52.3` is the main daemon lock in `persona`, `mind`, `router`, `message`, `introspect`, `system`, `harness`, `terminal`, `terminal-cell`, `upgrade`, `chroma`, `lojix-cli`, `chronos`, and `lojix`. `tokio 1.52.1` appears in `nexus`, `criome`, and `mentci-lib`. Contract-only crates usually have no direct `tokio`. | `/git/github.com/LiGoldragon/mind/Cargo.lock:689-690`, `/git/github.com/LiGoldragon/persona/Cargo.lock:1218-1219`, `/git/github.com/LiGoldragon/criome/Cargo.lock:916-917`. |
| Errors | `thiserror 2.0.18` is the active direct error crate across 61 scoped locks. `harness`, `terminal`, `terminal-cell`, and `chronos` also lock `thiserror 1.0.69` transitively. `anyhow 1.0.102` appears in 19 locks. No `eyre` or `color-eyre` package was found in the scoped locks. | Direct examples: `/git/github.com/LiGoldragon/persona/Cargo.toml:42`, `/git/github.com/LiGoldragon/persona/Cargo.lock:1183-1184`, `/git/github.com/LiGoldragon/lojix-cli/Cargo.lock:6-7` for `anyhow`. |
| CLI parsers | Direct CLI parsing is sparse. `clap` is direct in `criome` and `horizon-rs`; locks are `clap 4.6.1` for `criome` and `clap 4.5.60` for `horizon-rs`. No `argh` package was found in the scoped locks. | `/git/github.com/LiGoldragon/criome/Cargo.toml:21`, `/git/github.com/LiGoldragon/criome/Cargo.lock:157-158`, `/git/github.com/LiGoldragon/horizon-rs/Cargo.toml:12`, `/git/github.com/LiGoldragon/horizon-rs/Cargo.lock:62-63`. |
| NOTA | `nota-codec` locks as `0.1.0` in 61 scoped repos and `signal-frame`; most manifests use `git = "https://github.com/LiGoldragon/nota-codec.git", branch = "main"`. `horizon-rs` and `lojix-cli` omit the branch. The `lojix` worktree has both `horizon-nota-codec` as a package alias with no branch and `nota-codec` on `branch = "main"`. | `/git/github.com/LiGoldragon/horizon-rs/Cargo.toml:10`, `/git/github.com/LiGoldragon/lojix-cli/Cargo.toml:15`, `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/Cargo.toml:42`, `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/Cargo.toml:45`, `/git/github.com/LiGoldragon/horizon-rs/Cargo.lock:161-162`. |
| `nota-next` / schema-next stack | `nota-next`, `schema-next`, and `schema-rust-next` all lock as `0.1.0`. `schema-next` consumes `nota-next`; `schema-rust-next` consumes `schema-next` and `nota-next`; `spirit-next` consumes all three through `branch = "main"`. | `/git/github.com/LiGoldragon/schema-next/Cargo.toml:16`, `/git/github.com/LiGoldragon/schema-rust-next/Cargo.toml:16`, `/git/github.com/LiGoldragon/schema-rust-next/Cargo.toml:30`, `/git/github.com/LiGoldragon/spirit-next/Cargo.toml:52-53`; locks: `/git/github.com/LiGoldragon/spirit-next/Cargo.lock:288-289`, `/git/github.com/LiGoldragon/spirit-next/Cargo.lock:449-460`. |
| Signal and Sema local crates | Active locks record `signal-frame`, `signal-core`, `signal-sema`, `sema`, and `sema-engine` at crate version `0.1.0`. These are Git/path style stack crates, so the version alone is not enough: branch/rev pins matter. | `mind` locks these at `/git/github.com/LiGoldragon/mind/Cargo.lock:449-460`, `/git/github.com/LiGoldragon/mind/Cargo.lock:501-534`, `/git/github.com/LiGoldragon/mind/Cargo.lock:601-612`. `lojix` replacement locks `signal-lojix 0.1.0` at `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/Cargo.lock:741-742`. |

## Manifest pin outliers

| Outlier | Repositories | Evidence |
|---|---|---|
| `kameo` uses LiGoldragon fork branch instead of crates.io in two first-stack repos | `mind`, `message` | `/git/github.com/LiGoldragon/mind/Cargo.toml:20`, `/git/github.com/LiGoldragon/message/Cargo.toml:27`. |
| `signal-frame` still points at `operator-full-schema-spirit-2026-05-26` in several contract repos | `signal-sema`, `signal-version-handover`, `owner-signal-version-handover`, `signal-engine-management` | `/git/github.com/LiGoldragon/signal-sema/Cargo.toml:18`, `/git/github.com/LiGoldragon/signal-version-handover/Cargo.toml:16`, `/git/github.com/LiGoldragon/owner-signal-version-handover/Cargo.toml:18`, `/git/github.com/LiGoldragon/signal-engine-management/Cargo.toml:18`. |
| `signal-sema` also uses `operator-full-schema-spirit-2026-05-26` in one owner contract | `owner-signal-version-handover` | `/git/github.com/LiGoldragon/owner-signal-version-handover/Cargo.toml:19`. |
| `nota-codec` has branchless Git specs in older/deploy-surface crates | `horizon-rs`, `lojix-cli`, plus `lojix`'s `horizon-nota-codec` alias in the replacement worktree | `/git/github.com/LiGoldragon/horizon-rs/Cargo.toml:10`, `/git/github.com/LiGoldragon/lojix-cli/Cargo.toml:15`, `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/Cargo.toml:42`. |

## Nix input inventory

The Nix side is much less converged than Cargo. Most active Rust repos have
flakes, but the active set contains many distinct `nixpkgs` and `fenix` pins.

| Input | Distinct pins in scoped `flake.lock` files | Largest clusters |
|---|---:|---|
| `nixpkgs` | 18 | `github:NixOS/nixpkgs@d233902339c0` in 11 repos; `github:LiGoldragon/nixpkgs@0726a0ecb6d4` in 9; `github:NixOS/nixpkgs@68a8af93ff42` in 7; `github:NixOS/nixpkgs@01fbdeef22b7` in 6; `github:NixOS/nixpkgs@b3da656039dc` in 6. |
| `crane` | 7 | `github:ipetkov/crane@6d015ea29630` in 28 repos; `github:ipetkov/crane@edb38893982a` in 27; `github:ipetkov/crane@ad8b31ad0ba8` in 8. |
| `fenix` | 22 | No dominant single pin. Largest clusters are `github:nix-community/fenix@6f6f1110eaea` in 7 repos, `github:nix-community/fenix@f54d64521804` in 8 repos, and several 5-repo clusters. |

Representative flake evidence:

- `persona` uses `nixpkgs = github:LiGoldragon/nixpkgs@0726a0ecb6d4`,
  `crane = github:ipetkov/crane@d459c1350e96`, and
  `fenix = github:nix-community/fenix@3abc2d5559f4`
  in `/git/github.com/LiGoldragon/persona/flake.lock`.
- `mind` uses `nixpkgs = github:NixOS/nixpkgs@b3da656039dc`,
  `crane = github:ipetkov/crane@6d015ea29630`, and
  `fenix = github:nix-community/fenix@f54d64521804`
  in `/git/github.com/LiGoldragon/mind/flake.lock`.
- `schema-next` / `schema-rust-next` / `spirit-next` share
  `nixpkgs = github:NixOS/nixpkgs@f9d8b6595035`,
  `crane = github:ipetkov/crane@edb38893982a`, and
  `fenix = github:nix-community/fenix@6012e5463531`
  in their respective `flake.lock` files.
- `signal-lojix` replacement worktree uses
  `nixpkgs = github:NixOS/nixpkgs@eef00dfd8a71`,
  `crane = github:ipetkov/crane@6d015ea29630`, and
  `fenix = github:nix-community/fenix@67a701a5cb65`
  in `/home/li/wt/github.com/LiGoldragon/signal-lojix/horizon-leaner-shape/flake.lock`.
- `lojix` replacement worktree uses
  `nixpkgs = github:NixOS/nixpkgs@8a1b0127302e`,
  `crane = github:ipetkov/crane@6d015ea29630`, and
  `fenix = github:nix-community/fenix@8650744e43cf`
  in `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/flake.lock`.

Repos with no `flake.nix` in scope: `primary`, `lore`, `goldragon`,
`TheBookOfSol`, `criomos-horizon-config`.

## Deploy-stack lock drift

The protocol currently says production `CriomOS` pins `lojix-cli` at
`42529ebd2114` (`/home/li/primary/protocols/active-repositories.md:147-148`).
The actual lockfiles now differ:

| Surface | Current `lojix-cli` rev | Evidence |
|---|---|---|
| Production `CriomOS` canonical checkout | `4c66b8a6fa556014e48f8c137e1a8176ec713540` | `/git/github.com/LiGoldragon/CriomOS/flake.lock:1331-1350`, especially `:1345`. |
| Production `CriomOS-home` canonical checkout | `4c66b8a6fa556014e48f8c137e1a8176ec713540` | `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:996-1014`, especially `:1009`. |
| Lean `CriomOS` worktree | `ad6ce8ad5d4cdae9b59381c6ba198cbfd3f75494` | `/home/li/wt/github.com/LiGoldragon/CriomOS/horizon-leaner-shape/flake.lock:972-991`, especially `:986`. |
| Lean `CriomOS-home` worktree | `ad6ce8ad5d4cdae9b59381c6ba198cbfd3f75494` | `/home/li/wt/github.com/LiGoldragon/CriomOS-home/horizon-leaner-shape/flake.lock:725-743`, especially `:738`. |

This is reportable protocol drift, not a checkout-missing problem.
The two-stack rule itself still matches the filesystem: production edits
belong to canonical `/git/...` `main` checkouts; rewrite edits belong to
`/home/li/wt/github.com/LiGoldragon/<repo>/horizon-leaner-shape/`.

## Non-Cargo package surface

Only one package-json surface appeared in the active set:

| Repository | Package surface | Versions |
|---|---|---|
| `CriomOS-home` | `/git/github.com/LiGoldragon/CriomOS-home/packages/playwright-cli/package.json` and `package-lock.json` | `@playwright/cli = 0.1.13`; lockfile version 3; transitive `playwright = 1.61.0-alpha-1778188671000`. |

## Audit takeaways

- Cargo is mostly converged on Rust 2024, `rkyv 0.8.16`,
  `thiserror 2.0.18`, local stack crate versions `0.1.0`, and `kameo 0.20.0`
  where actors are used.
- The main Rust-version boundary is architectural age: first-stack daemons
  lean `1.88`/`1.89`, while schema/signal/nota support crates mostly remain
  `1.85`; `horizon-rs` and `lojix-cli` still omit `rust-version`.
- `redb` is the clearest dependency split: current sema/daemon state uses
  `4.1.0`, while schema-derived and upgrade surfaces still include `2.6.3`.
- Nix inputs are not converged. `nixpkgs` has 18 distinct pins and `fenix`
  has 22 across the scoped active repos.
- The active protocol should be corrected for the `lojix-cli` production pin:
  current lockfiles say `4c66b8a6fa55`, not `42529ebd2114`.
