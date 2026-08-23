# Herdr and Orca packaging

Observed 2026-08-23. Upstream versions and package availability are current-state claims, not permanent design facts.

## Herdr

The project meant by Herdr is `herdrdev/herdr`, a Rust terminal workspace and agent multiplexer. Stable `v0.8.2` is commit `9eb521456ac0d19d3ab3d9d7cea3cca10baa8a4c`; its current license is Apache-2.0.

Herdr has two sound installation routes. Its official tagged flake supports `nix run` and `nix profile install`, and upstream nixpkgs has packaged `0.8.2`. The configured nixpkgs seen by the research subflow still exposes `0.8.0`, so a durable deployment must either advance that input or pin the official `v0.8.2` flake explicitly. The official shell installer is suitable for unmanaged exploration but not for an environment already owned by Nix.

Herdr provides `integration install claude` and `integration install codex`. Those commands mutate the harness configuration directories to add hooks and enable Codex hooks. In this workspace, durable integration should instead be expressed by the owning declarative user-environment source, once modification of both harness configurations is explicitly in scope.

The existing `firstmate-bridge/bin/bridge-herdr` pin to `v0.7.4` cannot be replaced as a package-only update. Herdr `v0.7.5` broke the command surface used by the bridge: current agent start requires a kind and pane, and output waiting moved under `pane wait-output`. Migrating that private pin therefore requires a bridge command migration and end-to-end proof.

## Orca

StablyAI Orca is a local-first control plane around terminal coding agents. Stable `v1.4.188` is commit `f32ce859047a85a3ea4f507f633604dfbf596a0e`. Upstream publishes Linux x64 and arm64 AppImages, Debian and RPM packages, and macOS artifacts, but no official Nix package.

The nixpkgs name `orca` belongs to GNOME's screen reader, and `orca-ide` is absent. Any package for the agent orchestrator must therefore be named `orca-ide`.

The strongest current Nix starting point is the unmerged `Samuka007/nix-orca` PR updating its AppImage wrapper to `v1.4.188`. Its declared-system evaluation passes and the release hashes match upstream digests. An actual build, CLI smoke, GUI launch, and `orca serve` smoke have not yet been witnessed, so this remains a candidate rather than a verified package. Building Orca from source is the more expensive path because it combines Node 24, pnpm, Electron 43, native modules, patched rebuilds, speech binaries, and a glibc compatibility target.

## Recommended ownership

Package and integrate Herdr through `CriomOS-home`, the declarative owner of the user environment, using a pinned official flake or a nixpkgs input containing `0.8.2`.

Orca packaging belongs in a standalone public Nix repository. That repository should own the stable release pin and hashes, AppImage wrapper, `orca-ide` and `orca-ide-gui` executables, desktop metadata, update automation, supported-system outputs, and behavioral checks. `CriomOS-home` should consume only a pinned `packages.${system}.orca-ide` output and own its installation.

The least duplicative route is to contribute the missing proof and current release update to the existing `Samuka007/nix-orca` project, provided its absent license and maintainer/ownership expectations can be resolved. A separate LiGoldragon repository is warranted only if independent ownership is desired or the existing maintainer does not accept the terminal package shape.

Agent operating guidance, if wanted, belongs in authored Curriculum skill sources and manifests, followed by regeneration into both Claude and Codex consumers. Package definitions and mutable upstream integration installers do not belong in those instructions.

## Sources

- Flow `01a02a72` and `flows/01a02a72/reports/orca.md`.
- Herdr repository and release: https://github.com/herdrdev/herdr and https://github.com/herdrdev/herdr/releases/tag/v0.8.2
- Herdr installation and integration documentation: https://herdr.dev/docs/install/ and https://herdr.dev/docs/integrations/
- Herdr tagged flake and package: https://github.com/herdrdev/herdr/blob/v0.8.2/flake.nix and https://github.com/herdrdev/herdr/blob/v0.8.2/nix/package.nix
- Herdr CLI and changelog: https://herdr.dev/docs/cli-reference/ and https://github.com/herdrdev/herdr/blob/master/CHANGELOG.md
- Nixpkgs Herdr update: https://github.com/NixOS/nixpkgs/commit/916377a8f81a1cf4834e110f8fbe2666938dbc4b
- Orca stable release and installation overview: https://github.com/stablyai/orca/releases/tag/v1.4.188 and https://github.com/stablyai/orca/blob/v1.4.188/README.md
- Orca headless guide and build inputs: https://github.com/stablyai/orca/blob/v1.4.188/docs/reference/headless-linux-server.md and https://github.com/stablyai/orca/blob/v1.4.188/package.json
- Orca AppImage wrapper candidate: https://github.com/Samuka007/nix-orca/pull/1
