# Q8 candidates 8a and 8c: dry run

Build host: `hostname` returned `prometheus` before every cargo and nix run. Each candidate is its own scratch clone of ethos-zero at 07714b0, with the origin remote removed: `/tmp/q8-8a` and `/tmp/q8-8c`. The held set is not applied. Nothing was pushed or landed, and nothing was committed in Primary. The spec is `flows/d5df1d/reports/inline-import-questions-spec.md`, section Q8.

Regeneration: the built binary regenerated all 24 committed modules into a temporary directory and compared each with `cmp`. The 24 are src/error.rs, src/ethos-zero.rs, 18 tests/generated fixtures and the 4 flow print fixtures.

## 8a: emit `ethos_core::Name`. Patch: `q8-8a.patch`

Files touched: src/generation.rs (+5), tests/ethos.rs (+19, test `the_core_source_emits_as_ethos_core`).

The mapping is in `impl Tokening for Source` (generation.rs:49). Both arms the spec names, the inline source and `Resolution::Imported`, call that function. The spec placed it beside the `std` mapping at :152, but the emitted bytes are the same either way.

Checks:
- `cargo test`: all pass. lib 21, cli 17, ethos 33 (32 at base, plus 1), flow_contract 1 (inner runs 2 and 0), freshness 4, generated 19, print 9, signal_without_datom 2.
- `nix flake check --keep-going`: "running 9 flake checks..." and then "all checks passed!" (a rerun found all 9 already built). The 8 check attributes are build, clippy, dependency-ethos, doc, fmt, no-free-functions, no-inherent-methods and test. The ninth derivation is the package.

Against the spec:
- Match: the example generates exactly the predicted text: `pub type Topic = ethos_core::Name;`, `pub type Label = ethos_core::Name;`, and `Holder { pub label: Label, pub name: ethos_core::Name, }`. The field order and names the spec marked as inference also match.
- Match: every fixture and golden is byte-equal (0 of 24 differ).
- Match: "the Rust does not compile". I compiled the generated example with its derive lines stripped using `rustc --crate-type lib`. It gave 3 errors of `E0433 cannot find module or crate ethos_core`.
- Mismatches: none.

## 8c: refuse source `core`. Patch: `q8-8c.patch`

Files touched: error.ethos (`Source.String` added to `Problem`), src/error.rs (regenerated, +1 `Source(String)`), src/conception.rs (+8, a check at the head of both the import and the colon reference), tests/ethos.rs (+38: `a_core_source_is_refused`, and `other_sources_keep_their_emission_beside_the_core_refusal` for item 7's unchanged forms).

src/error.rs had to be bootstrapped, because the new conception code names `Problem::Source`. The first regeneration used the 8a binary, whose output for error.ethos is the same as base. The 8c binary then regenerated it byte-identically.

Checks:
- `cargo test`: all pass. lib 21, cli 17, ethos 34 (32 plus 2), flow_contract 1 (inner 2 and 0), freshness 4 (`the_error_module_is_fresh` included), generated 19, print 9, signal_without_datom 2.
- `nix flake check --keep-going`: "running 9 flake checks..." and "all checks passed!", exit 0.

Against the spec (CLI `Check` output):
- Match: the example gives `Conceptual.{ [ 1 0 0 0 ] Source.core }` at `{ 2 3 }`. The import is reached first, which the spec had inferred.
- Match: `Library [] [ Topic.core:Name ] [] []` gives `[ 1 1 0 1 0 ] Source.core` at `{ 3 9 }`.
- Match: `Library [] [ Holder.{ Label.core:Name } ] [] []` gives `[ 1 1 0 1 0 1 0 ] Source.core` at `{ 3 18 }`.
- Match: the Problem is `Source`, with no Form.
- Match: `Topic.protos:Name`, `Other.custom:Name` and `Holder.{ std:Mutex<String> }` check and generate `protos::Name`, `custom::Name` and `pub string_mutex: std::Mutex<String>`.
- Match: every other fixture and golden is byte-equal. Only src/error.rs changed, by the one variant.
- Mismatches: none.

### The living's registry key form, `Topic.core:Name`

The spec's Q5 example has `[ hash:Blake3 ]` imported and its key's `Topic.core:Name`. Under 8c it is refused:

`Rejected.{ q5.ethos { 5 23 } Conceptual.{ [ 1 1 0 1 0 1 1 1 0 ] Source.core } }`

Line 5, column 23 is the `core` in the key's `Topic.core:Name`. This is the first use of `core`, and the derived path the spec predicted matches. As the spec predicted, refusing source `core` refuses the living's own registry key form. The `hash` import is not refused.
