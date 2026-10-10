# Invariants Fork 3 (Mutex): both testable options built

Spec: `flows/d5df1d/reports/fork-options-spec.md`, section "Invariants Fork 3". Option (c) has no content and was not built.

Build host: `hostname` returned `prometheus` for every cargo, nix and rustc run. Base: Prometheus `/tmp/ethos-zero-item12b`, whose HEAD tree equals ethos-zero b2fa8b0's tree (26223cd, compared against a fresh GitHub clone) and whose working diff equals `item12-final-ethos-zero.patch`; protos through `--override-input protos path:/tmp/protos-item12b` (diff equals `item12-final-protos.patch`); datom-codec through the Cargo pin `file:///tmp/datom-codec-item12b` rev 296b25. Each option is a copy of that base with the set committed as a scratch commit, so each patch applies on top of the set. Nothing pushed; nothing in Primary committed.

Regeneration (`/tmp/regen-item12.sh`, pointed at each copy) changed no file in either option: src/error.rs, src/ethos-zero.rs and every tests/generated/*.rs are byte-equal to the set.

## Option (a): multi-segment imports

Option (a) imports the path and generates the field. The generated Rust still does not compile (11 rustc errors) because Mutex carries none of the derived traits, so (a) is import-only. A compiling Mutex field needs the derive-less declaration the invariants book leaves to the living.

Patch: `fork-invariants-f3-a.patch`. Files touched (3, +55 / -13): src/conception.rs, src/protosization.rs, tests/ethos.rs.

Change: `Conceiving<Import>` folds a chain of colon heads into one Source (`std:sync:Mutex` gives Source `std::sync`, name `Mutex`). `Protosizing for Import` prints a Source of several segments as the same colon chain. Test added: `a_multi_segment_import_reaches_its_path` (reads, round-trips through the print, generates, asserts the field, parses with syn).

Checks:
- cargo test: all pass; lib 21, cli 17, ethos 34, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2.
- `nix flake check --keep-going --override-input protos path:/tmp/protos-item12b`: exit 0, "running 9 flake checks", "all checks passed!"; 8 attributes (build, clippy, dependency-ethos, doc, fmt, no-free-functions, no-inherent-methods, test).

Before the change, the spec's source was refused on the base with `Conceptual.{ [ 1 0 0 1 ] Expected.Import }`, as probe c1 recorded.

Matches:
- Generated struct, header and field: exactly the spec's block, `pub flow_vector_mutex: std::sync::Mutex<std::vec::Vec<Flow>>,` and `pub integer: i64,` under the standard header. `Flow` is `pub struct Flow(pub String);`.
- Goldens changed: none. Byte-equal: all.
- rustc on the generated file (scratch crate copied from the mutex-probe crate, `cargo check` in the ethos-zero dev shell): without features, 11 errors: E0277 Archive x4, Clone, Eq, Hash, and E0369 `==`. With `--features datom`, 13 errors: those plus E0277 Composing and E0599 `datomize`. No E0425. That crate pins datom-codec 4dff16b, not the set's 296b25.

Mismatches:
- Layer. The spec names conception alone. Observed: with conception alone, the round trip fails. The print writes `std::sync:Mutex`, and reading it back gives the refusal `Expected.Import`. Test output: "source did not read: Library.{ [ std::sync:Mutex ] ...". The print layer (src/protosization.rs) also had to change.
- Fixture. The spec says "this adds a fixture". In this repository, any file under fixtures/ needs a golden. It is also counted by `every_fixture_module_is_fresh` (18) and the print round-trip test (20), and tests/generated.rs compiles it as a module. A golden with a Mutex field does not compile, so the source sits inline in the test instead. No fixture was added.
- Not built: the "fewer derives" half. The spec gives no form for it, and its `#[derive(Debug)]` header is the spec's own inference.

## Option (b): refused, stays outside ethos

Patch: `fork-invariants-f3-b.patch`. Files touched (1, +13): tests/ethos.rs. Generator unchanged.

Test added: `a_multi_segment_import_is_refused`. It reads `Library [ std::sync:Mutex ] [ Holder.{ Mutex<String> Integer } ] [] []` and asserts `Problem::Expected(Form::Import)` at `[ 1 0 0 ]`.

Checks:
- cargo test: all pass; lib 21, cli 17, ethos 34, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2.
- nix flake check, same command: exit 0, "running 9 flake checks", "all checks passed!"; the same 8 attributes.

Matches: the refusal is `Conceptual.{ [ 1 0 0 ] Expected.Import }`, as predicted. Layer: none. Byte-equal: all.

Mismatches: none.

Provenance receipt: unavailable.
