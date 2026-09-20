# Lojix schema compatibility addendum

Status: provisional. No deployment, Home activation, or Realize acceptance is
claimed. No source edits, screenshots, or secrets are included here.

## Reproducing request and failure

The affected request is the complete 14-field `Deploy.UserEnvironment`:

```text
Deploy.UserEnvironment.{
  goldragon ouranos li
  $HORIZON_DEFINITION
  SecretsDirectory.$GOLDRAGON_SECRETS
  github:LiGoldragon/CriomOS/aa5c151f87c0283bf63a622bf78224cb1410a188
  { ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome }
  Horizon
  { homeConfigurations.li.activationPackage }
  HomeManagerNixProfileV1
  Realize
  RequireImmutable
  Some.@/etc/nix/machines
  []
}
```

With the Goldragon `8c4d03de76907f590072c0998b00037330ebcd82` Horizon child,
the installed `lojix-meta` rejects the request before socket exchange with
`proposal source is not a Horizon definition`. The first surfaced decode field
is therefore the proposal source/Horizon definition value; that diagnostic
masks the later field comparison. The mismatch inference is grounded by the
consumer pin: Lojix horizon-lib is `40d04d25`, while Goldragon's Horizon is
`ee8d6f8d27eb6e200504807971ffdd26aaca7ed1`. The newer schema adds
`OpenCodeTesting` and changes the `Decimal` location. Horizon CLI parsing of
the child passed, so this is a producer/consumer schema skew inference, not a
finding that the child is invalid.

## Audited smallest coherent source scope

The smallest coherent repair crosses every socket-contract producer and the
Lojix consumer:

1. `signal-lojix`: update `Cargo.toml`, `Cargo.lock`, and `version`/`UPGRADES`
   metadata; regenerate and update the `generated_contract` fixture first.
   Publish the contract as `4.1.1` -> `5.0.0`, pinned to Horizon `ee8d6f8`.
2. `meta-signal-lojix`: make the same contract and fixture updates, pin the
   exact published `signal-lojix` revision, and publish `5.1.1` -> `6.0.0`.
3. Lojix: update `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`, and
   the exact signal/meta contract revisions. The producer fixtures must cover
   `OpenCodeTesting` and `FixedLocation` with all four Goldragon Decimal fields,
   including peer-byte restore/round-trip checks.

No generated runtime kinds or store migration is indicated by this audit.
Remote codec and round-trip tests are required before acceptance. Deployment
is not part of this scope.

## Separate proposals and current locks

The Lojix fallback proposal is separate: branch
`proposal/remote-builder-fallback-false` at `476bc56ebc17` has a one-file
`schema_runtime.rs` diff and a focused test, verified by Luna; it is not
integrated. The provisional `signal-lojix` remote proposal is
`ca32405cc27f`; its expanded `OpenCodeTesting` plus Decimal fixture checks are
still running on Prometheus. The corresponding meta proposal is unpublished.
Locks `3002` and `3003` are producer locks only. Fallback Lock `2995` was
released. These facts do not establish full contract acceptance.

## Later living deployment boundary

After review, promote the producer versions and the Lojix proposal, then run
the required remote tests. Only after those tests pass may the updated Lojix
daemon/CLI be deployed. Re-run the full pre socket Home request, then perform
remote-only Realize. Home activation requires a separate authorization after
the message unit preflight. Current status remains provisional: no activation
and no Realize are claimed.

## Sources

- `flows/8565e8/reports/morning-2026-09-20.md` — request shape, Goldragon
  child, parser and preflight observations.
- `flows/f38926/log.md` — revision comparison, producer scope, fixture gap,
  proposal revisions, lock status, and deployment boundary.
