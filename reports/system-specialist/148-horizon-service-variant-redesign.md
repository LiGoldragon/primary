# Horizon Service Variant Redesign

## Superseded Reports Removed

This report absorbs the useful parts of these stale production reports:

- `reports/system-specialist/144-repository-receive-production-slice-2026-05-18.md`
- `reports/system-specialist/145-persona-gitolite-server-production-shape-2026-05-19.md`
- `reports/system-specialist/146-production-horizon-service-variant-rework-2026-05-19.md`
- `reports/system-specialist/147-production-horizon-circle-back.md`

The Gitolite implementation topic is now owned elsewhere. The durable
lesson from those reports is not Gitolite-specific: cluster data should
select named feature variants and should not author CriomOS ports,
domains, paths, booleans-by-position, or implementation records.

## Production Lesson

The production stack got cleaner when node services became a vector of
self-describing variants:

```nota
[
  (TailnetClient)
  (TailnetController)
  (NixBuilder None)
  (PersonaDevelopment [(GitoliteServer)])
]
```

That shape reads as role selection. The cluster owner can see which
capabilities are present without remembering what `true none true`
means. Data-carrying variants still exist where the cluster is actually
selecting policy, for example `NixBuilder` carrying an optional maximum
job count.

The boundary is:

- Horizon derives cluster domains and router SSIDs.
- CriomOS owns standardized service ports and implementation paths.
- Cluster data selects providers and feature variants.

## Lean Stack Change

The `horizon-leaner-shape` stack now follows the production lesson.

`horizon-rs` changed `NodeProposal.services` from a positional
`NodeServices` record into:

```rust
Vec<NodeService>
```

Current variants:

- `TailnetClient`
- `TailnetController`
- `NixBuilder { maximum_jobs }`
- `NixCache`
- `PersonaDevelopment { capabilities }`

Nested Persona development capabilities currently include
`GitoliteServer`, but the lean branch does not enable that service in
cluster data in this slice.

`number_of_build_cores` was removed from the proposal. Builder capacity
now lives on `NixBuilder`. Remote-builder and Nix-cache projection are
explicit service-role derivations, not size/species inference.

`goldragon/datom.nota` now reads this way:

- `ouranos`: `TailnetClient`, `TailnetController`, `NixBuilder None`
- `prometheus`: `TailnetClient`, `NixBuilder 6`, `NixCache`
- nodes with no selected services: `[]`

`CriomOS` now reads `horizon.node.services` through
`modules/nixos/node-services.nix`, which understands externally tagged
service variants. `tailscale.nix` gates on `TailnetClient`.
`headscale.nix` gates on `TailnetController`.

`CriomOS-lib` owns:

```nix
constants.network.headscale.port = 8443;
```

The Headscale port is no longer cluster-authored in the lean stack.

## Commits

- `horizon-rs/horizon-leaner-shape`: `189bfd04` - `horizon-rs: use service variants in lean proposal`
- `goldragon/horizon-leaner-shape`: `5b55de84` - `goldragon: use lean service variants`
- `CriomOS-lib/horizon-leaner-shape`: `157ec2e0` - `lib: own headscale service port`
- `CriomOS/horizon-leaner-shape`: `325de8a7` - `criomos: consume service variant vector`
- `lojix/horizon-leaner-shape`: `be12741e` - `lojix: align build smoke with service variants`

All were pushed to `origin`.

## Verification

Passed:

- `CARGO_BUILD_JOBS=2 cargo test -p horizon-lib`
- `cargo fmt --check` in `lojix`
- `CARGO_BUILD_JOBS=2 cargo test --test build_pipeline`
- `nixfmt --check` on touched CriomOS Nix files
- `nix flake check --max-jobs 1 --cores 2` in `CriomOS-lib`
- direct CriomOS check derivation for `headscale-selfsigned-cert`
- direct CriomOS check derivation for `resolver-role-policy`
- `horizon-cli` projected `goldragon` for `ouranos`, `prometheus`, and `zeus`

The direct `.#checks.x86_64-linux.*` flake entry still tries to
evaluate the broader target shape and needs real `system` and `horizon`
inputs. With a projected `ouranos` Horizon input it then hit the
pre-existing missing `nordvpn-credentials` secret binding. The check
derivations themselves passed when called directly with the same inputs
they declare.

## Remaining Shape Work

The lean proposal still has several booleans:

- `nordvpn`
- `wifi_cert`
- `wants_printing`
- `wants_hw_video_accel`
- `online`

They are not all the same kind of problem. `online` is an
administrative availability override, not a feature. The others should
be reviewed as candidates for variant vectors:

- VPN client choice likely belongs under a provider/capability variant.
- Wi-Fi certificate participation likely belongs in the Wi-Fi PKI
  shape once ClaviFaber/Horizon integration is ready.
- Printing and hardware video acceleration may be node capabilities or
  profile features, but they should not remain anonymous booleans if
  the cluster data is expected to stay readable.

`horizon-rs/docs/DESIGN.md` still contains historical `NodeServices`
examples. `ARCHITECTURE.md` is the current spec and was updated in this
slice. The next cleanup should either remove `docs/DESIGN.md` or mark it
historical loudly enough that agents do not treat it as current truth.
