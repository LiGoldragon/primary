# 135 - Lean Horizon Follow-Up After User Decisions

Date: 2026-05-17  
Role: system-specialist

## Input

This implements the immediate engineering guidance from:

- `reports/designer-assistant/109-lean-horizon-forward-guidance-after-user-decisions-2026-05-17.md`
- `reports/designer-assistant/110-ideal-cluster-schema-visualization-2026-05-17.md`

The implemented scope is the near-term part: typed pan-Horizon
configuration for Lojix, explicit transitional IPv4 LAN data, and moving
projected-only network/router records out of `proposal::*`.

The ideal future split from report 110 remains design guidance. The
closed `NodeRole` / `NodeSpecies` redesign is not implemented in this
slice.

## Changes Shipped

### `horizon-rs`

Branch: `horizon-leaner-shape`  
Commit: `28dbca890b8d horizon-rs: make transitional LAN explicit`

Changes:

- Replaced `LanPool` and hash allocation with exact
  `TransitionalIpv4Lan { cidr, gateway, dhcp_pool, warning }`.
- Removed reserved-service-label configuration from `HorizonProposal`.
- Moved `LanNetwork`, `LanCidr`, `DhcpPool`, and `ResolverPolicy` under
  `view::network`.
- Moved `Ssid` under `view::router`; proposal router interfaces now
  carry only authored interface/regulatory/password facts.
- Updated architecture docs and repo skills to describe temporary exact
  IPv4 LAN data instead of LAN allocation policy.

### `signal-lojix`

Branch: `horizon-leaner-shape`  
Commit: `958a6bb787a6 signal-lojix: configure pan-horizon source`

Changes:

- Added `horizon_configuration_source: WirePath` to
  `LojixDaemonConfiguration`.
- Updated NOTA and rkyv configuration round-trip tests.
- Updated the contract architecture to name the pan-Horizon source as
  daemon control-plane configuration.

### `lojix`

Branch: `horizon-leaner-shape`  
Commit: `464c35766fff lojix: load horizon config from daemon configuration`

Changes:

- Removed the hardcoded production pan-Horizon config path from
  `RuntimeConfiguration`.
- `RuntimeConfiguration::from_daemon_configuration` now reads
  `configuration.horizon_configuration_source`.
- Added a source-level configuration-boundary witness for that rule.
- Updated daemon integration and real-build-smoke configuration records.
- Updated `signal-lojix` and `horizon-lib` locks to the new branch
  commits.

### `criomos-horizon-config`

Branch: `main`  
Commit: `08adcf11bd5e criomos-horizon-config: use transitional IPv4 LAN`

Changes:

- Rewrote `horizon.nota` to the new `TransitionalIpv4Lan` record:
  `10.18.0.0/24`, gateway `10.18.0.1`, DHCP range
  `10.18.0.100` through `10.18.0.240`.
- Updated repo docs to describe the explicit transitional IPv4 value.

## Verification

Rust suites:

- `horizon-rs`: `CARGO_BUILD_JOBS=2 cargo test --workspace` passed.
- `signal-lojix`: `CARGO_BUILD_JOBS=2 cargo test --workspace` passed.
- `lojix`: `CARGO_BUILD_JOBS=2 cargo test --workspace` passed.

Nix-backed checks:

- `signal-lojix`: `nix flake check --max-jobs 1 --cores 2` passed.
- `horizon-rs`: `nix flake check --max-jobs 1 --cores 2` passed.
- `lojix`: `nix flake check --max-jobs 1 --cores 2` passed.

Real build smoke:

- `lojix` real smoke built `goldragon/zeus` FullOS through builder
  `prometheus`.
- First attempt using `github:LiGoldragon/CriomOS/horizon-leaner-shape`
  failed before build because GitHub rate-limited Prometheus resolving
  the branch through the GitHub API.
- Re-run with direct git rev flake reference passed:
  `git+https://github.com/LiGoldragon/CriomOS?rev=5027d9acb43b54f84fc13fd270e61ca9bfc4980a`
- Built generation:
  `/nix/store/l1vngwlwck9skkd9695jsvdccm9jkx6z-nixos-system-zeus-26.05.20260510.da5ad66`

## Remaining Work

- The branch still needs the future `NodeSpecies` / additive
  `NodeRole` redesign from report 110.
- The real smoke runner should prefer direct git revision flake
  references or another non-GitHub-API path when running on Prometheus.
- Large AI model materialization remains tracked separately in
  `primary-f6cc`.
