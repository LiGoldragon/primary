# Lojix Generic Real Build Smoke Runner

Role: system-specialist  
Date: 2026-05-16  
Branch: `lojix/horizon-re-engineering`  
Commit: `c39dc90e` (`lojix: add generic real build smoke runner`)

## What Changed

The real-build smoke is now a Nix-provided impure operator app:

```sh
nix run .#real-build-smoke
```

The app deliberately has no baked-in cluster defaults. Callers provide:

- `LOJIX_SMOKE_CLUSTER`
- `LOJIX_SMOKE_NODE`
- `LOJIX_SMOKE_BUILDER`
- `LOJIX_SMOKE_PROPOSAL_SOURCE`
- `LOJIX_SMOKE_FLAKE_REFERENCE`

The script starts a temporary `lojix-daemon`, submits a build-only
`FullOsDeployment`, waits for `DeploymentBuilt`, runs `GenerationQuery`,
and verifies that the built-output GC root and the generation listing
agree on the same store path.

It is an app, not a pure flake check, because it uses SSH and the
caller's live cluster.

## Verification

Build and source checks:

- `cargo fmt --check`
- `cargo test --jobs 1 --test socket -- --test-threads=1`
- `cargo clippy --jobs 1 --all-targets -- -D warnings`
- `nix build --max-jobs 1 --cores 2 .#real-build-smoke .#checks.x86_64-linux.test-socket .#checks.x86_64-linux.clippy`

Packaged real smoke against the current goldragon/CriomOS redesign
branches:

```sh
LOJIX_SMOKE_CLUSTER=goldragon
LOJIX_SMOKE_NODE=zeus
LOJIX_SMOKE_BUILDER=prometheus
LOJIX_SMOKE_PROPOSAL_SOURCE=/home/li/wt/github.com/LiGoldragon/goldragon/horizon-re-engineering/datom.nota
LOJIX_SMOKE_FLAKE_REFERENCE=github:LiGoldragon/CriomOS/horizon-re-engineering
LOJIX_SMOKE_KEEP_ROOT=1
nix run --max-jobs 1 --cores 2 .#real-build-smoke
```

Result:

- accepted `deployment_1`
- observed `DeploymentBuilt`
- `GenerationQuery` returned `generation_12 ... Built`
- GC root pointed to
  `/nix/store/qsz55smwzwl11i9p150ikkw5zisrmf6p-nixos-system-zeus-26.05.20260510.da5ad66`

The preserved smoke root was:

```text
/tmp/lojix-real-build-smoke-UHIM19
```
