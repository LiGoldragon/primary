# Items 1 and 2 on item 5

Build host: `hostname` returned `prometheus` for every cargo and nix run. Scratch copies are in `/tmp` on Prometheus, with remotes removed. Nothing was pushed, and nothing in Primary was committed.

## Base

- ethos-zero: 07714b0 ("Format item 5 trait terminology source"), version 17.0.0, cloned from main. Its parent is a09bb81 ("Generate item 5 kind-to-trait model and fixture outputs"), and a09bb81's parent is b2fa8b0. The brief named b2fa8b0 as the parent; it is the grandparent. The scratch tree is `/tmp/ez-i5`, branch `set`, at cf1d79f.
- protos: 15b41da plus `item12-final-protos.patch`, uncommitted, in `/tmp/protos-i5`.
- datom-codec: `/tmp/datom-codec-item12b` at 296b256 (4dff16b plus `item12-final-datom-codec.patch`). The diff 4dff16b..296b256 matches that patch byte for byte.

Method: `item12-final-ethos-zero.patch` was applied at b2fa8b0 and committed, then rebased onto main (07714b0).

## Conflicts and resolutions

Four files conflicted. The other 31 files merged without conflict.

1. **error.ethos.** Item 5 changed `Kind` to `Trait` in the `Form` list. The set added `SinglePosition` after `Renamed.String`. The resolution keeps both: `SinglePosition` is added, and `Form.[ … Constraint Trait Capability Constant Association ]` is kept.
2. **src/generation.rs `use crate::{…}`.** Item 5 renamed `KindBody` and `KindDeclaration` to `TraitBody` and `TraitDeclaration`. The set added `Identifiable`. The resolution imports `Identifiable` together with item 5's `TraitBody` and `TraitDeclaration`.
3. **src/lib.rs test.** Item 5 renamed the test to `library_traits_generate_trait_surfaces`. The set changed the source from `Sink.{ String }` to `Sink.String`. The resolution uses item 5's name and the set's source.
4. **tests/ethos.rs test.** Item 5 renamed the test to `full_library_round_trips_and_generates_named_types_and_traits`. The set changed the source to `Sink.String`. The resolution uses item 5's name and the set's source.

There was one further change with no textual conflict. Two doc comments added by the set still read "The kind whose capability …": on `trait Single` in src/checking.rs, and on `trait Plain` in src/generation.rs. Item 5 uses "The trait whose capability …" in that position, so both now use "trait". A grep of the added lines finds no other `Kind`, `KindBody`, `KindDeclaration` or prose "kind".

## Committed Rust

`tests/freshness.rs` generates src/error.rs, src/ethos-zero.rs and all 18 fixtures plus the print fixtures from their sources, then compares the result with the committed text. All 4 freshness tests pass, so the merged committed Rust already equals a fresh generation, and regenerating changes nothing. src/error.rs contains `SinglePosition`. No separate step that writes files was run.

## Checks

- ethos-zero, `cargo test --offline`: all pass. lib 21, main 0, cli 17, ethos 33, flow_contract 1 (inner package 2), freshness 4, generated 20, print 9, signal_without_datom 2.
- ethos-zero, `nix flake check --keep-going --override-input protos path:/tmp/protos-i5 --override-input datom-codec "git+file:///tmp/datom-codec-item12b?rev=296b256118e76cdfa6bb11628c4042ec4b294b4d"`:
  - It exited 0 with "running 12 flake checks…" and "all checks passed!".
  - All 8 check attributes have built outputs in the store: build, test, fmt, clippy, doc, dependency-ethos, no-free-functions and no-inherent-methods.
  - `nix flake metadata` with the same overrides shows datom-codec resolved to the scratch rev 296b256. The dependency-ethos derivation reads `datom-codec.ethos` from that source.
- protos scratch, `cargo test --offline`: all pass (4, 15, 1, 18, 13, 8).
- datom-codec scratch, `cargo test --offline --workspace`: all pass (14, 33, 1).

## Files touched

- protos (1): protos.ethos. The patch is identical to item12-final-protos.patch.
- datom-codec (2): crates/datom-codec-derive/src/lib.rs, tests/composition.rs. The patch is identical to item12-final-datom-codec.patch.
- ethos-zero (35, +359 / -240), against 07714b0:
  - Root: Cargo.lock, Cargo.toml, error.ethos.
  - Fixtures (.ethos): composition-types, empty-signal, generic-shadow, inline-collision, nested-collision, signal-decimal, tree-types.
  - src (.rs): checking, conception, error, generation, lib, location, protosization, sectioning.
  - tests (.rs): cli, ethos, flow_contract, generated.
  - tests/generated/ (.rs): alias-format, composition-types, empty-signal, flow-library, flow-operation, flow-signal, generic-shadow, inline-collision, multi-types, nested-collision, orchestrate, signal-decimal, tree-types.
  - None of the fixtures that item 5 renamed (capability-traits, processable-traits, self-traits, streamable-trait) are touched.
  - `git apply --check` of item12-on-item5-ethos-zero.patch on a clean 07714b0 succeeds.

The Cargo.toml datom-codec pin is still the scratch `file:///tmp/datom-codec-item12b` rev 296b256. It moves to the released datom-codec revision when that lands, as item12-final.md describes.

Provenance receipt: unavailable.
