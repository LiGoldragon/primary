# Items 1 and 2 dry run, second pass

Host: `hostname` on the build machine returned `prometheus`. All three scratch copies live in `/tmp` on Prometheus with their remotes removed; nothing was pushed, and nothing in Primary was committed.

- ethos-zero: `/tmp/ethos-zero-item12b`. **Base: 9ea7c80** (item 3, "Reject repeated reference sources"), not c2653d. The first pass's patch applied on it with one conflict, in tests/ethos.rs: item 3's two new tests and the first pass's replacement of `an_authored_name_capturing_a_derived_inline_name_is_refused` touched the same place. Both were kept: item 3's tests first, then `a_variant_carrying_one_type_derives_no_inline_name`.
- protos: `/tmp/protos-item12b`, at 15b41da, left uncommitted.
- datom-codec: `/tmp/datom-codec-item12b`, at 4dff16b, plus one local scratch commit, 296b25, so that Cargo can pin it by rev.

## Result

| Repository | cargo test | Flake checks |
|---|---|---|
| ethos-zero (protos input overridden) | all pass: lib 21, cli 17, ethos 33, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2 | 8 of 8 pass: build, clippy, dependency-ethos, doc, fmt, no-free-functions, no-inherent-methods, test |
| datom-codec scratch | all pass with `--features rkyv`: archival 1, composition 14, core 33, hygiene 1, kinds 0 | 12 of 12 pass. nix printed "running 11 flake checks … all checks passed!" for 12 attributes |
| protos scratch | all pass | 12 of 12 pass ("all checks passed!") |

Command for ethos-zero: `nix flake check --keep-going --override-input protos path:/tmp/protos-item12b`.

## Per ruling

1. **protos line 17.** `ReaderBudget.{ Integer } ]` became `ReaderBudget.Integer ]`. ethos-zero's flake `protos` input points at the scratch copy through `--override-input`, so flake.nix and flake.lock are unchanged. dependency-ethos passes: the scratch protos.ethos, protos-kinds.ethos, datom-codec.ethos and datom-codec-kinds.ethos each return `Generated.[ … ]`. The protos Cargo dependency of ethos-zero and datom-codec is still the pinned 15b41da on GitHub. protos's own checks run its pinned ethos-zero, which still accepts the line.
2. **A new type prints and parses as its inner value.** This is done in the codec: datom-codec-derive treats a struct with exactly one unnamed field as transparent. `Datomizable` returns the inner value's datom at the same path. `Composing` composes the inner value and wraps it. The new type gets no `Compositional` impl. ethos-zero's emission is unchanged from the first pass: `#derive pub struct Name(pub T);` still carries the datom derives. ethos-zero's Cargo.toml line 28 points datom-codec at `git+file:///tmp/datom-codec-item12b` rev 296b25, and Cargo.lock lines 49 and 59 change to match. The tests/cli.rs location expectations are reverted to `{ 3 19 }`, `{ 5 26 }`, `{ 4 3 }`, `{ 4 10 }`, `{ 4 28 }` and `{ 1 1 }`, and they pass. Item 3's `{ 3 18 }` passes unchanged. The ethos-zero test `a_new_type_has_its_value_size_and_reads_as_its_value_in_datom` now expects `abc123` instead of `{ abc123 }`. "Golden file" was read as the expected outputs of the tests, in tests/cli.rs and in fixtures/print/, which has no diff. The generated modules in tests/generated/ still change, because item 1's emission changes them.
3. **Collision fixtures.** X now has the payload `{ String Integer }` everywhere it appears. In inline-collision that is `P.[ X.{ String Integer } Y.[ X.{ String Integer } ] ] Q.[ X.{ String Integer } ]`; in nested-collision it is `Outer.[ A.[ X.{ String Integer } ] B.[ X.{ String Integer } ] ]`. The regenerated modules contain `P_X_Data`, `Y_Data_X_Data` and `Q_X_Data` again, and `A_Data_X_Data` and `B_Data_X_Data`, each with the fields `string` and `integer`. The authored `X_Data` is `pub struct X_Data(pub String);` and captures nothing. `nested_inline_payloads_have_distinct_rust_types` and `colliding_inline_payloads_are_named_for_their_enums` build those structs again. Still open: R's `Z.String` was not changed, so `Z_Data` (the unique payload that keeps its short name) is still not generated, and the fixture comment's last clause still does not hold. The inline capture probe in tests/ethos.rs still uses `X.String`.
4. Left as is.
5. `a_new_type_over_a_plain_value_is_a_struct_of_one_unnamed_position` (tests/ethos.rs) asserts the emitted text `pub struct FlowId(pub String);` and `pub struct Age(pub i64);`. **Untested:** E0308, meaning `FlowId` is refused where `LockName` is wanted. The repository has no compile-fail harness.

## Repositories touched

### protos (`item12-dry-run-2-protos.patch`)
- protos.ethos 17.

### datom-codec (`item12-dry-run-2-datom-codec.patch`, 4dff16b to 296b25)
- crates/datom-codec-derive/src/lib.rs:
  - after line 15: `is_new_type(&Fields)`.
  - after line 86, in `composing`: the transparent `Composing` impl.
  - after line 178, in `datomizable`: the transparent `Datomizable` impl.
- tests/composition.rs, after line 402: `Line(i64)`, `Name(String)`, `Location { line, column }`, and the test `a_new_type_prints_and_reads_as_the_value_it_holds`. It checks that `Line(3)` prints `3`, `Name("abc123")` prints `abc123`, and Location prints `{ 3 19 }`; that each round trips; and that `{ 3 }` is refused as a Line.

### ethos-zero (`item12-dry-run-2-ethos-zero.patch`, against 9ea7c80; 35 files, +358 / −239)
Hunk start lines are in 9ea7c80 numbering.
- Cargo.toml 28; Cargo.lock 49, 59.
- error.ethos 24; src/error.rs regenerated.
- src/checking.rs: 67, 286, 375, 597, 652, 1155, 1263, 1320, 1416, 1432, 1442; after 1455; after 1465.
- src/conception.rs 247, 481.
- src/generation.rs: 29; 353; 445; after 786; 876; 884.
- src/lib.rs: 277, 284, 822, 847, 1001, 1038, 1047, 1175, 1178, 1200.
- src/location.rs 12, 89; src/protosization.rs 140, 269; src/sectioning.rs 161.
- Fixtures: composition-types 8; empty-signal 1; generic-shadow 1; inline-collision 6-7, 9; nested-collision 1; signal-decimal 5; tree-types 11, 14.
- tests/cli.rs 220. This is the duplicate source rewrite only; every location expectation is the original.
- tests/ethos.rs: 17, 26, 44, 92, 97, 113, 148, 164, 168, 178, 181, 194, 216, 223, 244, 250, 296, 320, 326, 328, 353, 371, 379, 387, 395, 399, 406, 407, 410, 412, 414, 420, 430; after 564.
- tests/flow_contract.rs 29, 38, 44.
- tests/generated.rs: 78, 82, 91, 94, 96, 129, 183, 217, 271, 338, 344, 358, 362, 375, 381, 454, 464, 467; after 483.
- 13 files regenerated in tests/generated/. Of these, inline-collision.rs and nested-collision.rs were regenerated again in this pass.

## Sources

- First pass: item12-dry-run.md and item12-dry-run.patch, beside this file.
- Witnesses: the cargo test, `nix flake check` and ethos-zero `Generate` runs on Prometheus in this flow's thread. Provenance receipt: unavailable.
