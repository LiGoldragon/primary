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
   The current final provisional source proposal is
   `3f550fc278b8e14c37158036d420e7e3ed1d7c7b`.
2. `meta-signal-lojix`: make the same contract and fixture updates and pin the
   exact published `signal-lojix` revision. Its current final provisional
   source proposal is `a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85`.
3. Lojix: update root `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`,
   `UPGRADES`, and the four member `Cargo.toml` files for `nexus`,
   `clients/ordinary`, `clients/meta`, and `tools`, plus the exact signal/meta
   contract revisions. The root-only pin was insufficient. The current
   consumer proposal is branch `proposal/horizon-contract-repin-8565e8` at
   `34115703fad1df0bcf11814fc82456abc2f42b58`: all five workspace crates are
   `7.0.0`, the exact diff is nine files, and the old dependency graph is
   absent; Luna reported source PASS.

   The producer fixtures must cover `OpenCodeTesting` and `FixedLocation` with
   all four Goldragon Decimal fields, including peer-byte restore/round-trip
   checks. The separate Lojix fallback branch is
   `proposal/remote-builder-fallback-false` at `476bc56`; Luna PASS covers its
   one-file diff and focused test. Neither proposal is integrated or deployed.

No generated runtime kinds or store migration is indicated by this audit.
Remote codec and round-trip tests are required before acceptance. Deployment
is not part of this scope.

## Separate proposals and current locks

| Component | Current provisional proposal | Audit state |
| --- | --- | --- |
| `signal-lojix` | `3f550fc278b8e14c37158036d420e7e3ed1d7c7b` | Source PASS; remote contract test pending |
| `meta-signal-lojix` | `a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85` | Source proposal; remote contract test pending |
| Lojix consumer | `proposal/horizon-contract-repin-8565e8` at `34115703fad1df0bcf11814fc82456abc2f42b58` | Luna source PASS; nine-file diff, old graph absent; five crates `7.0.0` |
| Lojix fallback | `proposal/remote-builder-fallback-false` at `476bc56` | Separate one-file proposal; Luna PASS; unintegrated |

The final provisional source proposals are `signal-lojix`
`3f550fc278b8e14c37158036d420e7e3ed1d7c7b`, `meta-signal-lojix`
`a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85`, and the Lojix consumer
`34115703fad1df0bcf11814fc82456abc2f42b58` above. All five workspace crates
are `7.0.0` in the consumer proposal. Luna's source result is PASS; this is
not contract or deployment acceptance. The fallback branch remains separate
and unintegrated. The former producer locks `3002` and `3003` are not evidence
of acceptance; fallback Lock `2995` was released.

## Remote test status

The expanded signal Datom foreground test was interrupted and reaped with
exit 1, with no codec result. A detached rerun (PID `1240203`, bounded to
7200 seconds) is recorded at
`flows/8565e8/witnesses/signal-lojix-test-datom-contract.log`; it was still
pending after a two-minute sample. Its child PID `1240223` was state `S`,
`/proc` I/O was denied, and `ss` showed no attributable socket. The 100-byte
log sample contained a `cache.nixos.org` copy line; the store path remained a
4096-byte directory. This measures no visible progress. It does not establish
zero network bytes or daemon health. Raw logs are not copied into this report.

## Later living deployment boundary

Morning action is to wait for the bounded runner to exit or time out, then
assess the Ouranos Nix substituter/daemon path with privileged correlated
counters if available. Rerun producer checks sequentially; only after they
pass run the remote Lojix `7.0.0` check and the full pre-socket Home request.
There is no next check, Realize, activation, or deployment claimed here.

## Sources

- `flows/8565e8/reports/morning-2026-09-20.md` — request shape, Goldragon
  child, parser and preflight observations.
- `flows/f38926/log.md` — revision comparison, producer scope, fixture gap,
  proposal revisions, lock status, and deployment boundary.
