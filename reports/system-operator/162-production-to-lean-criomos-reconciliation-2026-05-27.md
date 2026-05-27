# Production To Lean CriomOS Reconciliation — 2026-05-27

## Purpose

The current production CriomOS stack has kept moving while the lean Horizon/Lojix stack was developed on `horizon-leaner-shape`. This report records what production gained, what is still missing from the lean stack, what I ported immediately, and what the remote full-OS build sweep proved.

## Context Read

I refreshed the system-operator required skills and the workspace/repo contracts, then read the relevant system-designer reports for the lean stack:

- `reports/system-designer/34-mvp-and-sandbox-audit/5-overview.md`
- `reports/system-designer/34-mvp-and-sandbox-audit/1-mvp-code-state-fresh-audit.md`
- `reports/system-designer/34-mvp-and-sandbox-audit/4-cutover-to-main-deployment-requirements.md`
- `reports/system-designer/35-schema-deep-new-logics/1-vision-schema-deep-new-logics.md`
- `reports/system-designer/30-horizon-lojix-low-level-migration/5-overview.md`
- `reports/system-designer/29-lean-horizon-cluster-data-shape.md`

Working model used for this pass:

- Production stack is mainline `/git/github.com/LiGoldragon/CriomOS` plus production `goldragon/datom.nota`.
- Lean stack is the `horizon-leaner-shape` family under `~/wt`.
- Schema-deep work is a sibling future track; I did not edit it.
- Wholesale rebase is not the right move right now. Both CriomOS and Horizon have semantic branch divergence; the safe path is semantic porting plus targeted tests.

## Production Changes Not Yet Fully In Lean

### Ported In This Pass

I ported the high-confidence production fixes into `CriomOS/horizon-leaner-shape`:

- Nix local builder caps: non-dedicated hosts now get `max-jobs = 1`, `cores = 2`; dedicated center builders keep configurable capacity.
- Remote builder system normalization: Horizon enum names such as `X86_64Linux` and `Aarch64Linux` reduce to Nix names such as `x86_64-linux` and `aarch64-linux`.
- Deployment shape: `includeHome` and `includeAllFirmware` are now consumed by the lean module stack and fixture.
- Metal thermal fix: ThinkPad thermald config keeps `ignoreCpuidCheck = true`.
- Legacy Chroma NixOS module removed from the lean system aggregate.
- Router Wi-Fi secret policy and checks ported.
- Router Wi-Fi projection compatibility added: router module tolerates `country`/`ssid` as the intended names and `wirelessCountryCode`/`wirelessNetworkName` as transitional names.
- Desktop audio policy ported: Bluetooth HSP/HFP roles enabled, native HFP/HSP backend selected, ALSA loopback demoted but not disabled.
- Devshell ghq layout fix ported.
- NordVPN server lock/update files ported.
- WireGuard projection tolerance check adapted to lean typed records.
- New/ported checks wired into the lean flake.

Lean commit pushed:

- `95dda319` — `criomos: port production fixes to lean stack`

Production commits pushed during the build sweep:

- `b6dccb49` — `criomos: align router wifi projection names`
- `a91c9ce2` — `criomos: tolerate derived router wifi names`

### Still Missing Or Not Safely Portable Yet

Repository-ledger/gitolite receive support exists in production but is not fully ported into lean. It also exposed a remote-builder source distribution blocker in production: the `repository-ledger` flake input is `git+ssh://gitolite@localhost/repository-ledger?ref=main`, which cannot be fetched by `root`/Nix on Prometheus when building an edge node remotely.

PersonaDevelopment/Gitolite role shape has been improved in production cluster data, but the lean cluster data in `goldragon/horizon-leaner-shape` is stale and still uses old quoted-string/old proposal forms. That branch needs a Horizon data migration before it can be a trustworthy input to lean CriomOS builds.

CriomOS-home production has continued to move separately. I did not port Home changes in this pass because the immediate lean full-OS path is blocked earlier by Horizon projection and source-distribution issues. Home should be compared next after Horizon projection is green again.

CriomOS-lib production has constants/helper drift that should be compared next, especially where production has moved values out of cluster data. I did not edit it in this pass.

## Remote Production Full-OS Build Sweep

All production full-OS builds were invoked through `lojix-cli` with `nix --option max-jobs 0`, targeting Prometheus as remote builder. No local full-OS build was intentionally run.

Results:

- `zeus`: passed.
  Store path: `/nix/store/30i41zbn7bmlzxprwb45ga7hk8zcb24p-nixos-system-zeus-26.05.20260422.0726a0e`
- `prometheus`: failed first on router Wi-Fi projection names, then passed after `a91c9ce2`.
  Store path: `/nix/store/xxi65lqbrc732crljxn9fgnz2ynjff6z-nixos-system-prometheus-26.05.20260422.0726a0e`
- `tiger`: passed.
  Store path: `/nix/store/5ia8x7vs9pbw2j81fq9ksd44vffzjl8w-nixos-system-tiger-26.05.20260422.0726a0e`
- `ouranos`: failed because edge build evaluates `repository-ledger`, whose flake input points at `gitolite@localhost`. From Prometheus, `localhost` is Prometheus, and `gitolite@ouranos.goldragon.criome:repository-ledger` also rejected root/Prometheus access.
- `balboa`: failed because it is `aarch64-linux` and Prometheus currently presents as an `x86_64-linux` builder only. The immediate error is platform mismatch on aarch64 derivations.

The x86 production stack is mostly healthy under remote builds after the router fix. The two remaining failures are not ordinary module regressions; they are build-topology/source-distribution gaps.

## Lean Stack Test Results

I could not run a real lean full-OS build yet. The first blocker is upstream of CriomOS:

- Lean `horizon-rs` cannot parse the current production `criomos-horizon-config/horizon.nota` bracket-string form: it errors with `expected string literal or bare identifier, got LBracket`.
- Lean `goldragon/datom.nota` is stale relative to the production cluster data shape and the current NOTA bracket-string discipline.

I did run the ported lean CriomOS policy checks directly, bypassing the full lean flake output so the stale Horizon projection did not block them. These were built with `nix --option max-jobs 0`; the output shows execution on `ssh-ng://nix-ssh@prometheus.goldragon.criome`.

Passed checks:

- `nix-role-policy`
- `desktop-audio-policy`
- `devshell-repository-layout`
- `legacy-chroma-runtime`
- `metal-firmware-policy`
- `router-wifi-horizon-policy`
- `router-wifi-secret`
- `wireguard-untrusted-proxy`

## Main Architectural Consequences

### Repository Ledger Must Stop Being Localhost-Only

Production remote builds now prove that a flake input pointing at `gitolite@localhost` is not compatible with distributed builds. This affects both current Lojix and the next daemon architecture.

Viable remedies:

- Publish/mirror `repository-ledger` to a fetchable authenticated remote.
- Teach Lojix/Arca to stage source inputs to the builder as content-addressed artifacts.
- Grant the builder a deploy key and use a cluster-resolved Gitolite host instead of `localhost`.

The third option is the fastest tactical fix, but the second is the cleaner long-term match for the Arca/Lojix direction.

### Aarch64 Needs A Real Build Strategy

Balboa cannot be built by an x86-only Prometheus builder unless we add aarch64 emulation/binfmt support and intentionally advertise it as a supported system, or add a real aarch64 builder. The current failure is correct: Nix refuses to build aarch64 derivations on an x86_64 builder.

### Horizon Projection Is The Next Critical Path

The lean CriomOS code can now carry several current production fixes, but the next stack cannot build a real OS until `horizon-rs` and `goldragon/horizon-leaner-shape` accept and emit the same current NOTA shape as production. This is the most important next port.

### Router Wi-Fi Fallback Is Transitional Debt

The router module currently tolerates both intended names and old names, with a default `PL` country fallback. That is acceptable for keeping production builds green, but it should not become architecture. The proper state is:

- Horizon/pan-Horizon derives SSID from cluster identity.
- Router country comes from explicit Horizon configuration or a standard reduction rule.
- CriomOS consumes the projected value without encoding cluster-specific data.

## Recommended Next Sequence

1. Fix source distribution for `repository-ledger` so edge production remote builds work.
2. Decide whether Prometheus should advertise aarch64 via binfmt/emulation or whether Balboa requires an aarch64 builder.
3. Port production NOTA/bracket-string parser support into `horizon-rs/horizon-leaner-shape`, preserving existing dirty work there.
4. Migrate `goldragon/horizon-leaner-shape/datom.nota` to the current production-style variant/vector cluster shape.
5. Re-run lean Horizon projection for all five nodes.
6. Re-run lean CriomOS full-OS builds through the new Lojix path, still with `max-jobs 0`.
7. Compare and port CriomOS-home and CriomOS-lib production drift after the OS projection path is green.
