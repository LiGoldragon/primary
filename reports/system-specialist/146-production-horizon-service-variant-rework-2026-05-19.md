# Production Horizon Service Variant Rework - 2026-05-19

## Scope

This work stayed on the production stack:

- `horizon-rs` main
- `goldragon` main
- `lojix-cli` main
- `CriomOS` main
- `CriomOS-home` main

The lean `horizon-leaner-shape` / `horizon-re-engineering` worktrees were not touched.

## Boundary Fixed

Cluster data now selects roles with self-describing service variants instead of configuring implementation details.

The production cluster data no longer stores:

- tailnet port numbers
- tailnet domain names
- boolean service slots such as `true none true`
- structural service records that hide intent behind field position

Those values belong in Horizon projection and CriomOS reduction. The cluster data now says what a node is selected to do, not how CriomOS implements that role.

## Shape

`horizon-rs` now models node services as a vector:

```rust
Vec<NodeService>
```

The current production variants are:

- `TailnetClient`
- `TailnetController`
- `NixBuilder { maximum_jobs }`
- `NixCache`
- `PersonaDevelopment { capabilities }`

The current nested Persona development capability is:

- `GitoliteServer`

This gives cluster data names that carry their own meaning:

```nota
[
  (TailnetClient)
  (TailnetController)
  (NixBuilder None)
  (PersonaDevelopment [(GitoliteServer)])
]
```

and:

```nota
[
  (TailnetClient)
  (NixBuilder 6)
  (NixCache)
]
```

## Projection Rules

Horizon now derives the tailnet base domain from the cluster name:

```text
tailnet.<cluster>.criome
```

CriomOS owns the Headscale service port. The production value is the CriomOS constant `8443`, not cluster data.

Remote builder and cache status are no longer inferred from broad node species or size. They require explicit variants:

- remote builder requires `NixBuilder`
- cache requires `NixCache`

The `NixBuilder` variant carries the optional maximum job count. This removed the old top-level `number_of_build_cores` field from node proposals.

## CriomOS Reduction

CriomOS now consumes the projected variant vector through a small Nix helper:

```text
modules/nixos/node-services.nix
```

That helper handles externally tagged JSON variants and keeps the module logic readable:

- `TailnetClient` enables Tailscale.
- `TailnetController` enables Headscale.
- `PersonaDevelopment` with `GitoliteServer` enables repository receive.

## Commits

- `horizon-rs`: `ab0fbb8a` - `horizon: project node service variants`
- `goldragon`: `bfb2716e` - cluster data switched to service variants
- `lojix-cli`: `ec8f7211` - repinned Horizon and updated tests
- `CriomOS`: `27154804` - consumed node service variants
- `CriomOS-home`: `9b0dca4c` - repinned `lojix-cli`
- `CriomOS`: `a11c74f6` - repinned `CriomOS-home`

All six commits were pushed to `origin/main`.

## Verification

Passed:

- `CARGO_BUILD_JOBS=2 cargo test -p horizon-lib`
- `CARGO_BUILD_JOBS=2 cargo test` in `lojix-cli`
- Horizon projection smoke for `ouranos`, `prometheus`, and `zeus`
- `CriomOS` check `headscale-selfsigned-cert`
- `CriomOS` check `repository-receive-role-policy`
- `CriomOS` check `resolver-role-policy`

The CriomOS checks were run with local-only Nix settings:

```text
--builders '' --max-jobs 1 --cores 2
```

## Remaining Caveat

`horizon-rs` still has pre-existing dirty edits in:

- `ARCHITECTURE.md`
- `skills.md`

Those files were dirty before this implementation pass and were not committed as part of this work.

`cargo fmt --check` is not currently a useful repo-wide verifier in `horizon-rs`: many unrelated files in the clean tree fail current rustfmt formatting. The implementation files were handled carefully, and the behavioral tests above are the relevant verifier for this slice.
