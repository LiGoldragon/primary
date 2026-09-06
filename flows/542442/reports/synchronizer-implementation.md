# Synchronizer Datom migration

## Final producer

- **Main:** `b42c9df295adccdd65381f8bd444147099036183`
- **Version:** `0.4.0`
- **Portable source tree:** `5fa1bd4fc68ca2765a1790d43c7c41ff5cc05660`
- **Prior main:** `7d4494442446b18afe96b8fd96f10e1d80233591`

`main` advanced normally from the prior main to `b42c9df…`; the pushed feature contains
`47c2ef…` (the Datom/Horizon migration), `2e3ac7…` (Nix source-filter correction), and
an empty-tree merge `b42c9df…`.  The merge has parents `2e3ac7…` and
`22f28b357abe29578a3e48c08d34b6d9f96078ea` (`docs: mark Protos estate status`).
That documentation commit was already ancestral through `7d449…`; the merge preserves
that history without changing the tested source tree.

## Contract and preserved behavior

Synchronizer now uses current `datom-codec`, Protos, Ethos, and Horizon `0.6.0`.  Its
Ethos-authoritative configuration defines:

```text
ClusterSource.[ HorizonDefinition.AbsolutePath ]
BuilderResolution.[ DirectHost.BuilderHost ClusterRole.BuilderResolutionClusterRole ]
BuilderResolutionClusterRole.{ BuilderRole ClusterSource }
```

Goldragon now owns the rendered configuration and supplies the single immutable composed
public Horizon artifact, for example
`ClusterRole.{ NixBuilder HorizonDefinition./absolute/horizon-definition.datom }`.
There is no hard-coded store path, legacy `ClusterProposal` decoder, or fallback to an old
proposal. `DirectHost` remains an explicit configuration option.

`ClusterRole` resolves only nodes selected into the cluster. It preserves the old dynamic
Nix builder behavior: eligible online builder-capability nodes are considered, configured
capacity decides the winner, equal capacity breaks by node name, and missing or malformed
inputs fail loudly. Tests cover selected catalogue exclusion, capacity, deterministic tie
breaking, offline eligibility, missing capability, and malformed composed input.

`ethos/synchronizer.ethos` is the source of truth; the committed generated contract is
checked byte-for-byte by the generation test. Release-train intent is now a Datom fixture
(`release-trains/language-family-poc.datom`), and the Nix source filter explicitly includes
`release-trains/` because `tests/release_train.rs` compiles that authored fixture with
`include_str!`.

## Validation

Local checks passed before the remote gate:

```text
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --tests
```

The normal SSH/stateful `tests/nix_resolution.rs` case remains explicitly ignored; it is
not represented as a completed portable check.

The definitive portable receipt is the attached remote-only command, run from the source
that has tree `5fa1bd…`:

```text
nix build -L --no-link --no-write-lock-file --max-jobs 0 --option fallback false \
  .#checks.x86_64-linux.build \
  .#checks.x86_64-linux.test \
  .#checks.x86_64-linux.fmt \
  .#checks.x86_64-linux.clippy \
  .#packages.x86_64-linux.default
```

It terminated with CLI exit code `0`. All five derivations were built on
`ssh-ng://nix-ssh@prometheus.goldragon.criome`. The flake exposes exactly the four named
checks and `packages.default`; this receipt therefore builds the package as well as
format, test, build, and clippy checks.

An earlier attached remote command terminated with CLI exit code `1`: its `clippy` target
could not find `release-trains/language-family-poc.datom` because `cleanSourceWith` omitted
the tracked fixture. `2e3ac7…` fixes that narrow source-filter omission. Earlier daemon
lifecycle observations without a captured Nix client exit status are deliberately
**unverified**, not passing evidence.

## Integration boundary

Goldragon `1f49f8dea50932cacc781d531c48b6d20805b439` owns the composed public artifact
and rendered Synchronizer configuration. External configuration, Home/OS consumers, and
test-cluster retain their own pins and combined acceptance checks; they consume this
producer without reconstructing an old proposal shape.
