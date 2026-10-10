# Herdr and Orca packaging

Observed 2026-08-23. Upstream versions and package availability are current-state claims, not permanent design facts.

## Herdr

The project meant by Herdr is `herdrdev/herdr`, a Rust terminal workspace and agent multiplexer. Stable `v0.8.2` is commit `9eb521456ac0d19d3ab3d9d7cea3cca10baa8a4c`; its current license is Apache-2.0.

Herdr has two sound installation routes. Its official tagged flake supports `nix run` and `nix profile install`, and upstream nixpkgs has packaged `0.8.2`. The configured nixpkgs seen by the research subflow still exposes `0.8.0`, so a durable deployment must either advance that input or pin the official `v0.8.2` flake explicitly. The official shell installer is suitable for unmanaged exploration but not for an environment already owned by Nix.

Herdr provides `integration install claude` and `integration install codex`. Those commands mutate the harness configuration directories to add hooks and enable Codex hooks. In this workspace, durable integration should instead be expressed by the owning declarative user-environment source, once modification of both harness configurations is explicitly in scope.

## Orca

StablyAI Orca is a local-first control plane around terminal coding agents. Stable `v1.4.188` is commit `f32ce859047a85a3ea4f507f633604dfbf596a0e`. Upstream publishes Linux x64 and arm64 AppImages, Debian and RPM packages, and macOS artifacts, but no official Nix package.

The nixpkgs name `orca` belongs to GNOME's screen reader, and `orca-ide` is absent. Any package for the agent orchestrator must therefore be named `orca-ide`.

The existing `Samuka007/nix-orca` default branch packages `v1.4.146`. Its open PR updates the wrapper to `v1.4.188`. The exact PR revision's declared-system evaluation, release hashes, x86_64-linux package build, CLI status and agent-context commands, visible GUI launch, headless readiness, HTTP response, and WebSocket handshake were witnessed successfully. Building Orca from source is the more expensive path because it combines Node 24, pnpm, Electron 43, native modules, patched rebuilds, speech binaries, and a glibc compatibility target.

## Recommended ownership

Package and integrate Herdr through `CriomOS-home`, the declarative owner of the user environment, using a pinned official flake or a nixpkgs input containing `0.8.2`.

Orca packaging belongs in a standalone public Nix repository. That repository should own the stable release pin and hashes, AppImage wrapper, `orca-ide` and `orca-ide-gui` executables, desktop metadata, update automation, supported-system outputs, and behavioral checks. `CriomOS-home` should consume only a pinned `packages.${system}.orca-ide` output and own its installation.

The least duplicative route is to contribute the missing proof and current release update to the existing `Samuka007/nix-orca` project, provided its absent license and maintainer/ownership expectations can be resolved. A separate LiGoldragon repository is warranted only if independent ownership is desired or the existing maintainer does not accept the terminal package shape.

Agent operating guidance, if wanted, belongs in authored Curriculum skill sources and manifests, followed by regeneration into both Claude and Codex consumers. Package definitions and mutable upstream integration installers do not belong in those instructions.

## Home realization

CriomOS-home revision `756ce723ea7f1a58d20e2b6f153f15e30aa9b885` pins Herdr `v0.8.2` and the exact `nix-orca` `v1.4.188` packaging revision, then selects `herdr` and `orca-ide` through the existing `AIPackages` Home Manager surface. It also updates the Nix-owned Codex CLI to `0.149.0` and Claude Code plus its VSIX to `2.1.241`. A projected-Horizon evaluation included the intended package versions in the full Home package list.

Herdr and Orca realized successfully on the configured Prometheus remote builder. Herdr's CLI, server lifecycle, and API snapshot passed. Orca's CLI returned valid status and agent-context JSON, its GUI produced a visible window, and its headless server emitted readiness before answering HTTP and WebSocket probes. The headless smoke created unmanaged launchers in `~/.local/bin`; both were proved to be smoke-generated, removed, and verified absent before deployment.

The direct deployment output is `homeConfigurations.li.activationPackage`; `independentHomeConfigurations.li.activationPackage` is comparison-only. The stale `DeploymentHomeSelector` variable was corrected in primary commit `75f36b73`. The authorized direct deployment uses the immutable CriomOS-home revision through Lojix `Deploy.UserEnvironment` with Horizon input, the configured Ouranos transport, `HomeManagerNixProfileV1`, `ActivateNow`, and `RequireImmutable`.

Lojix accepted deployment 42 with marker 915, realized and copied the closure, then recorded terminal `Some.Failed.(Activate ActivationFailed)` at marker 939. The configured `li@ouranos` transport was already unprivileged, but the activation command invoked `runuser --login li`; `runuser` rejected the non-root caller. The live Home Manager profile therefore remained generation 972 and contained neither executable. Admission, realization, copy, terminal failure, and unchanged live state are separate observations; no retry or manual activation followed.

Lojix `0.19.1` corrected activation authority so an explicit SSH login matching the target user runs directly, root retains `runuser` mediation, and a different unprivileged login is rejected before effects. Its first self-deployment made the corrected daemon live, but restart reconciliation exposed a second defect: public deployment 45 remained `Copying` after its Current generation was recorded and its recovery cursor retired.

Lojix `0.19.2` added durable successor reconciliation of the public terminal record. CriomOS revision `65a0e024a1b870c981826f24ca941c59214c08be` pinned it. Ouranos deployments 46 Evaluate, 47 Realize, and 48 ActivateNow each reached public `Completed/Succeeded`; the live system, Current generation, client, and daemon all resolve to the `0.19.2` closure. Deployment 45 remains untouched historical divergence.

Home deployment 49 then activated CriomOS-home `756ce723ea7f1a58d20e2b6f153f15e30aa9b885` and reached public `Completed/Succeeded` plus live `Current`. Ordinary login-shell resolution and resolved Nix paths witness Codex `0.149.0`, Claude Code `2.1.241`, Herdr `0.8.2`, and Orca IDE `1.4.188`. `orca-ide status --json` succeeded and the user manager had no failed units.

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
