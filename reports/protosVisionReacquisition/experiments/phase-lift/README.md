# Phase-Lift Research Witnesses

> **TENTATIVE, NON-AUTHORITATIVE AGENT SYNTHESIS.** Psyche review is required. Accepted material must be decomposed and deliberately ported into authoritative design logs, owning `ARCHITECTURE.md` files, READMEs, or standards.

These are research witnesses for the tentative phase-lift discussion in
[`2-Research-psyche-vision-open-questions-and-proposals.md`](../../2-Research-psyche-vision-open-questions-and-proposals.md).
They do not specify the Protos design and do not authorize implementation.

## Provenance

The sources were copied on 2026-07-31 from the ephemeral research directory
`/tmp/protos-phase-lift.RyMA4Q`. Binaries, Cargo targets, caches, and the
generated lock file were deliberately excluded. The only source adjustment is
pinning the `rkyv` dependency to exact version `0.8.17` so this durable witness
does not silently select a later compatible release.

The observed research environment was:

```text
rustc 1.96.0 (ac68faa20 2026-05-25)
cargo 1.96.0 (30a34c682 2026-05-25)
host x86_64-unknown-linux-gnu
LLVM 22.1.2
rkyv 0.8.17
```

These versions record the witnessed environment. Future toolchains may produce
different diagnostics without changing the underlying type-system result.
Because no generated `Cargo.lock` is retained, transitive dependency resolution
can still move even though the direct `rkyv` version is exact. The bundle is a
durable research witness, not a bit-for-bit supply-chain reproduction capsule.

## Witness inventory

- [`phase_family.rs`](phase_family.rs) is a successful phase-family prototype.
  It covers computed root/product/sum values, nested positions, visibility,
  sequence elements, splice, and indexed insertion.
- [`no_hole_failure.rs`](no_hole_failure.rs) is expected not to compile. It
  demonstrates that `Declaration<Nomos>` cannot enter an API accepting only
  `Declaration<Logos>` in this candidate representation.
- [`hkt_failure.rs`](hkt_failure.rs) is expected not to compile. It records the
  stable-Rust limitation on applying an unconstrained type parameter as a type
  constructor.
- [`schema_hybrid.rs`](schema_hybrid.rs) is a successful staged-check witness.
  It demonstrates that structural sealing cannot by itself prove that a
  reference exists in the population.
- [`rkyv-phase`](rkyv-phase) contains two successful archive witnesses for a
  generic-associated-type phase projection and a recursive typed expression.

## Exact commands

Run from this directory. Outputs are placed in a disposable directory so the
report tree remains free of build artifacts and generated lock files.

```sh
experiment_tmp="$(mktemp -d)"
rustc phase_family.rs -o "$experiment_tmp/phase-family"
"$experiment_tmp/phase-family"

rustc schema_hybrid.rs -o "$experiment_tmp/schema-hybrid"
"$experiment_tmp/schema-hybrid"
```

Expected success output:

```text
phase-family: all position classes lowered without surviving holes
schema-hybrid: shape seal, evaluation, semantic check, typed reification separated
counterexample: a shape-valid reference can still be semantically dangling
```

The next two commands are negative compile witnesses and must return nonzero:

```sh
experiment_tmp="$(mktemp -d)"
rustc no_hole_failure.rs -o "$experiment_tmp/no-hole"
rustc hkt_failure.rs -o "$experiment_tmp/hkt"
```

Expected diagnostic cores:

```text
error[E0308]: mismatched types
expected `Declaration<Logos>`, found `Declaration<Nomos>`

error[E0109]: type arguments are not allowed on type parameter `Constructor`
```

Build the archive witnesses from a disposable source copy so Cargo writes its
generated lock file and target output outside this report directory:

```sh
experiment_tmp="$(mktemp -d)"
cp -R rkyv-phase "$experiment_tmp/rkyv-phase"
CARGO_TARGET_DIR="$experiment_tmp/target" \
  cargo run --quiet --manifest-path "$experiment_tmp/rkyv-phase/Cargo.toml" \
  --bin rkyv-phase
CARGO_TARGET_DIR="$experiment_tmp/target" \
  cargo run --quiet --manifest-path "$experiment_tmp/rkyv-phase/Cargo.toml" \
  --bin typed_expr
```

Expected output:

```text
rkyv-phase: archived and bytechecked a phase-family projection
typed-expr: recursive heterogeneous children archived after explicit bounds
```

The original intermediate recursive-derive failure was not retained and is
not reproducible from this bundle. Only the corrected explicit-bounds witness
is preserved.

> **TENTATIVE, NON-AUTHORITATIVE AGENT SYNTHESIS.** Psyche review is required. Accepted material must be decomposed and deliberately ported into authoritative design logs, owning `ARCHITECTURE.md` files, READMEs, or standards.
