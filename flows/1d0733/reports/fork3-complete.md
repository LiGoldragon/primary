# Fork 3 complete: the braced set, and Represented on both sets

Build host: `hostname` over ssh returned `prometheus` for every cargo and nix run. The scratch trees are in `/tmp/f3c` on Prometheus, with no remotes. Nothing was pushed, nothing landed, and nothing in Primary was committed.

## Variants and bases

| Variant | ethos-zero tree | datom-codec | protos |
|---|---|---|---|
| bare set | `/tmp/ez-i6` 77fc650 (held, not rebuilt) | 296b256 (set patch) | `/tmp/protos-i5` |
| braced set | `/tmp/f3c/ez-bs` 5ff8e81 | 4dff16b, main, unchanged | `/tmp/protos-i5` |
| bare represented | `/tmp/f3c/ez-rb` 21da35b | `/tmp/dc-f3` d6191ff = 776cf4b + set's datom-codec patch | `/tmp/protos-i5` |
| braced represented | `/tmp/f3c/ez-rbr` 406410c | `/tmp/dc-f3` 776cf4b alone | `/tmp/protos-i5` |

`/tmp/protos-i5` is protos 15b41da plus item12-on-item5-protos.patch; its `git diff` equals that patch byte for byte. `nix flake metadata` with each variant's overrides shows the datom-codec and protos inputs listed above.

## Task 1: the braced set

Method: fresh 07714b0, then item12-on-item5-ethos-zero.patch and item6-on-set-ethos-zero.patch applied. The set's only Cargo.toml and Cargo.lock change is the datom-codec pin to the scratch 296b256, so both files were restored to 07714b0, which pins datom-codec main 4dff16b. That datom-codec has no newtype print hunk, so a newtype prints braced.

Before the edits, `cargo test` failed in 9 places, all where the answer prints: 8 cli tests (the error location, a struct of two newtypes, printed `{ { 3 } { 19 } }` against `{ 3 19 }`) and the generated test (`{ abc123 }` against `abc123`). The edits:

- `tests/cli.rs`: the location in 8 expectations becomes braced, for example `{{ {{ 3 }} {{ 19 }} }}`. `Arity.{ 2 1 }` stays as it is, because it is a struct of two Integers and prints that way under both answers. rustfmt rewrapped two of the lines.
- `tests/generated.rs`: `FlowId("abc123")` prints `{ abc123 }`. The test name claimed the bare answer, so `a_new_type_has_its_value_size_and_reads_as_its_value_in_datom` is renamed `a_new_type_has_its_value_size_and_reads_as_a_struct_of_its_value_in_datom`.
- `README.md`: the CLI example `{ 4 19 }` becomes `{ { 4 } { 19 } }`. `UPGRADES.md` still shows `{ 1 1 }` under 15.0.0. That entry records the 15.0.0 output, so it was left unchanged.

### Golden diffs, braced set against bare set

Every fixture and every file under `tests/generated/` is byte-equal, including src/error.rs and src/ethos-zero.rs. `git diff 77fc650 5ff8e81` touches only these files:

- `Cargo.toml`, `Cargo.lock`: the datom-codec pin (bare 296b256 scratch, braced 4dff16b main).
- `README.md`: one line, the CLI location.
- `tests/cli.rs`: 8 expectations, the location.
- `tests/generated.rs`: one expectation and the name of that test.

## Task 2: Represented, with d5df1d's rulings

Both variants carry the same candidate. They differ only in Cargo.toml and Cargo.lock (the pin) and in one line of tests/represented.rs: `TICKET_TEXT` is `[ 4 2 ]` in bare and `[ { 4 }\n  { 2 } ]` in braced. Against the earlier candidate 31b346d, seven files change: src/checking.rs, src/conception.rs, src/generation.rs, src/lib.rs, src/protosization.rs, tests/generated/represented-types.rs and tests/represented.rs. The src changes outside generation.rs are only the rename in (c).

### (a) Test (3), restated

The test is now `the_assertion_pins_the_representation_and_rustc_enforces_the_bounds_at_the_impl`. Its association binds `Representation.Opaque`, where Opaque is neither Datomizable nor Composing. It asserts the following:

- An impl with `Representation = String` fails with E0271 at `assert_ticket_represented`, and without E0277: the pin.
- An impl with `Representation = Opaque` fails with E0277: "Opaque: Composing" and "Opaque: Datomizable", required by `Represented::Representation`. It does not fail with E0271. This is rustc enforcing the trait's bounds at the impl, even though the impl's Representation is the one the assertion pins.

The doc comment states the same thing.

### (b) The source as written

Both the derive and the assertion now come from the same emission of the borne trait's bound (`Reference::emit`). `datom:[ Represented ]` gives `derive(datom::Represented)` and `T: datom::Represented<…>`. `datom_codec:[ Represented ]` gives `datom_codec::` in both places. In src/generation.rs, `Representing::represented -> bool` became `representation -> Option<&AssociatedTrait>`. The golden `tests/generated/represented-types.rs` changes 2 lines, Ticket's and Digest's derive, from `datom_codec::Represented` to `datom::Represented`. A new test, `the_derive_and_the_assertion_name_the_source_as_written`, checks both sources, and checks that neither source's output contains the other's path.

### (c) Names

- `Binding` is what Rust calls an associated type binding (`Representation = Vec<Digit>`). The crate's existing `AssociatedType { name, bounds }` is the declaration side.
- `AssociatedTrait` is one entry of a type's associations section, whatever the trait. `Association.traits` is `Vec<AssociatedTrait>`. Its print helper is `AssociatedTraitProtosizing::associated_trait_nodes`.
- The derive choice is `Representing::representation`, a question asked of a type's AssociatedTraits that returns `Option<&AssociatedTrait>`. It has no type of its own.

### (d) Known gaps, not built

- **A trait imported into a type position is not refused.** An import carries no role, so `datom:[ Represented ]` makes `Represented` resolve the same way in every position.
- **A trait in a field position is emitted as a type.** Witnessed on the bare represented tree: `Library [ datom:[ Represented ] ] [ Holder.{ Represented Integer } ] [] []` generates, and the output contains `pub represented: datom::Represented,`.

## Checks

The 8 check attributes are build, test, fmt, clippy, doc, dependency-ethos, no-free-functions and no-inherent-methods. For each variant, each attribute was built with `nix build` under that variant's overrides and succeeded. `nix flake check --keep-going` then printed "running 0 flake checks…" and "all checks passed!" and exited 0. The count is 0 because every derivation had already been built.

| | braced set | bare represented | braced represented |
|---|---|---|---|
| lib | 21 | 21 | 21 |
| cli | 17 | 17 | 17 |
| ethos | 33 | 33 | 33 |
| flow_contract (inner 2) | 1 | 1 | 1 |
| freshness | 4 | 4 | 4 |
| generated | 20 | 20 | 20 |
| print | 9 | 9 | 9 |
| represented | none | 9 | 9 |
| signal_without_datom | 2 | 2 | 2 |
| flake check attributes | 8/8 | 8/8 | 8/8 |

All three variants pass `cargo fmt --check`.

## Golden diffs from bare

- **Braced set against the bare set:** see the list above. No fixture and no generated golden differs.
- **Bare represented against the bare set:** a new fixture `fixtures/represented-types.ethos` and a new golden `tests/generated/represented-types.rs`. Every existing golden is byte-equal. tests/freshness.rs and tests/print.rs change only their counts (18 → 19 fixtures, 20 → 21 sources).
- **Braced represented against bare represented:** `git diff 21da35b 406410c` touches Cargo.toml, Cargo.lock, README.md, tests/cli.rs, tests/generated.rs (the braced set's five files) and the one `TICKET_TEXT` line in tests/represented.rs. No fixture and no generated golden differs, including represented-types.rs.

## Patches

All are in `/home/li/primary/flows/1d0733/reports/`. Applying each chain to a clean 07714b0 reproduces its tree exactly (`git diff --cached` against the tree is empty).

- `braced-set-ethos-zero.patch`: `git diff 07714b0 5ff8e81`.
- `braced-set-protos.patch`: identical to item12-on-item5-protos.patch. The braced set has no datom-codec patch.
- `fork3-bare-represented-ethos-zero.patch`: `git diff 77fc650 21da35b`, applied on the bare set.
- `fork3-bare-represented-datom-codec.patch`: `git diff 776cf4b d6191ff`. Its +/- lines equal item12-on-item5-datom-codec.patch.
- `fork3-braced-represented-ethos-zero.patch`: `git diff 5ff8e81 406410c`, applied on the braced set. The braced variant uses datom-codec 776cf4b with no patch.

The ethos-zero pins still point at the scratch `file:///tmp/dc-f3`, except the braced set, which pins datom-codec main 4dff16b.

Provenance receipt: unavailable.
