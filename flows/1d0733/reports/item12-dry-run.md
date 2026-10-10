# Items 1 and 2 dry run on ethos-zero c2653d

Host: `hostname` on the build machine returned `prometheus`. The scratch copy is `/tmp/ethos-zero-item12` on Prometheus. It was cloned at c2653dd, its remote was removed, and nothing was committed, pushed or merged. Builds and tests ran through `nix develop -c cargo …` and `nix flake check` / `nix build .#checks.x86_64-linux.<name>`. The patch against c2653dd is `item12-dry-run.patch`, beside this file: 33 files, 357 insertions, 290 deletions.

## Result

- `cargo test`: every target passes. The lib has 21 tests, cli 16, ethos 31, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2.
- Flake checks: build, clippy, doc, fmt, no-free-functions, no-inherent-methods and test pass. **dependency-ethos fails.** The pinned protos input's `protos.ethos` line 17, `ReaderBudget.{ Integer }`, is now refused with `Conceptual.{ [ 1 1 8 ] SinglePosition }`. protos-kinds.ethos, datom-codec.ethos and datom-codec-kinds.ethos all return `Checked`. Getting this check to pass needs a protos change: `ReaderBudget.Integer`, plus a release of protos and its consumers, because ethos-zero's own tests build `ReaderBudget { remaining: 1024 }`. That change is outside this scratch copy.

## Item 1: new type emission

`TypeDeclaration::Alias` is renamed to `NewType` in src/lib.rs, and every use is updated. When the held reference is a plain value (String, Integer, Decimal or Boolean, with no source and no arguments), the declaration is emitted as `#derive pub struct Name(pub T);`, carrying the derive that every struct and enum carries. This follows the design's default, Fork 4 (c), and the emission sits on one line. Any other reference still emits `pub type`, as the design scopes it. The plain test is a new trait, `Plain for Reference`, in src/generation.rs.

What this changes outside the seven fixtures:
- error.ethos `Line.Integer` and `Column.Integer` become `Line(pub i64)` and `Column(pub i64)`. src/location.rs now builds `Line(..)` and `Column(..)`. Under today's derive, the CLI rejection location prints as `{ { 3 } { 19 } }` where it used to print `{ 3 19 }`, and tests/cli.rs expects the new form. Fork 3 is still open, so this form is not settled.
- Newly emitted new types in the generated files: Short, SpiritGuardianProviderName and SpiritGuardianMaximumOutputTokens (alias-format); FlowId (flow-library); Brief (flow-signal); Home (flow-operation); LockId (multi-types); LockId, LockName, FlowId, LockPath and LockReason (orchestrate); X_Data (inline-collision); A (generic-shadow); Measurement (signal-decimal); Name (empty-signal); Vec (composition-types). `DuplicateName.Lock` and every container alias stay `pub type`.
- New tests:
  - `a_new_type_over_a_plain_value_is_a_struct_of_one_unnamed_position`: `FlowId.String Age.Integer` gives `pub struct FlowId(pub String);` and `pub struct Age(pub i64);`, both parse as Rust, and no `pub type` is emitted.
  - `a_new_type_has_its_value_size_and_reads_as_its_value_in_datom`: size_of FlowId equals size_of String, size_of FlowId(i64) equals size_of i64, and `FlowId("abc123")` prints as `{ abc123 }`.
- Not built: the E0308 compile-fail pair (`FlowId` refused where `LockName` is wanted). The repository has no compile-fail harness.

## Item 2: one-position struct refused

`Problem::SinglePosition` is added to error.ethos, with no payload; the path locates it. src/error.rs is regenerated. A new trait, `Single for [Position]` in src/checking.rs, refuses a position list of length one. It is called in `TypeDeclaration::check` for `Struct`, after the name, case and intrinsic checks, and in `Variant::check` for `Variant::Struct`. The refusal sits at the declaration's or the variant's own path.

New test `a_struct_of_one_position_is_refused`:
- `Age.{ Integer }` is refused at `[1 1 0]`, and `Age.Integer` is accepted.
- `Event.[ Started.{ String } ]` is refused at `[1 1 0 1 0]`.
- The original collision probe `P.[ X.{ String } ] Q.[ X.{ Integer } ] X_Data.String` is refused at `[1 1 0 1 0]`.
- `Signal [] [ Ask.{ String } ] [ Ask.{ Integer } ] []` is refused at `[1 1 0]`.
- `Chain.{ Option<Chain> }` is refused at `[1 1 0]`.

Double wrapping and a new type over a struct or enum are not built; this run's brief named only the one-position refusal.

## The seven fixtures

| Fixture | Rewrite | Result |
|---|---|---|
| inline-collision | `P.[ X.String Y.[ X.String ] ] Q.[ X.String ] X_Data.String R.[ Z.String ]` | Generates. P, Y_Data and Q each get the variant `X(String)`, R gets `Z(String)`, and X_Data becomes `struct X_Data(pub String)`. |
| nested-collision | `Outer.[ A.[ X.String ] B.[ X.String ] ]` | Generates. A_Data and B_Data each get `X(String)`. |
| tree-types | `Loop.Knot`, `B.String` | Generates. `pub type Loop = Knot;`, and `Knot::Loop` is now boxed: `Box<Loop>`. B_Data is gone and the variant is `B(String)`. The archive round trip of Knot passes. |
| generic-shadow | `A.String` | `pub struct A(pub String)`, and Holder holds it. |
| signal-decimal | `Measurement.Decimal` | `pub struct Measurement(pub Decimal)`. The archive round trip passes. |
| empty-signal | `Shared.Name Name.String` | `pub type Shared = Name;` and `pub struct Name(pub String)`. The rkyv and datom round trips pass, and so does the build without the datom feature. |
| composition-types | `Vec.String` | `pub struct Vec(pub String)` does not capture the fully qualified `std::vec::Vec`. Generates and compiles. |

No position was added, no name was changed, and nothing uses an underscore. None of the seven became a refusal fixture: in each, the one-position struct was a means to another point. The refusal is instead asserted inline in tests/ethos.rs. The comment in inline-collision.ethos still says P and Q "each declare a payload X in place". That is no longer what the fixture does, and the comment was not rewritten.

## Collision fixtures: no collision is exercised

With `X.String` in both places, X is a variant that carries a String. It is no longer an inline struct, so the generator derives no payload type: no `P_X_Data`, `Q_X_Data`, `A_Data_X_Data`, `B_Data_X_Data` or `Z_Data`. Nothing collides, and X_Data captures nothing. Inline payload naming (`<Enum>_<Variant>_Data`, ancestry after the first level, the refusal of an authored name that captures a derived one) is now exercised only by multi-position payloads such as `PathOverlap.{ String String }`. It is no longer exercised in any collision case. The test names `nested_inline_payloads_have_distinct_rust_types` and `colliding_inline_payloads_are_named_for_their_enums` in tests/generated.rs now describe something the tests no longer check. Restoring a real collision needs an inline payload of two or more positions, which this brief rules out.

## Inline test sources outside the fixtures

The same rule was applied to inline sources in src/lib.rs, tests/ethos.rs and tests/cli.rs: `N.{ T }` becomes `N.T`. Where a source needed a one-position struct to make its point, it became a SinglePosition assertion instead:
- `S.{ Vector<Self> }`, `S.{ Option<Self> }`, `S.{ Result<Self String> }`. As `S.Vector<Self>` and the like they generated `pub type S = std::vec::Vec<Self>;`, which rustc does not accept, so they now assert the refusal.
- `Chain.{ Option<Chain> }`. As `Chain.Option<Chain>` it is refused as `Cycle.Chain`. Boxing through Option is still covered by tree-types `Chain.{ String Option<Chain> }`.
- `an_authored_name_capturing_a_derived_inline_name_is_refused` and `signal_query_and_response_inline_payloads_are_unique_file_wide` are replaced by `a_variant_carrying_one_type_derives_no_inline_name`. With X.String or Ask.String, all four capture sources generate, and no `Ask_Data` is emitted.
- Unchanged, and still refused at the read stage: `Sema [] [ Record.{ String } ]` (two tests). `A.{ Brief.String } B.{ Brief.Integer }` and `Brief.String A.{ Brief.Integer }` are unchanged and assert only `is_err()`. Which Problem refuses them now was not observed.
- `S.Self` keeps `Cycle.S` at `[1 1 0 0]`, and `B.A` keeps `Cycle.A` at `[1 1 1 0]`.

## Files and lines touched (c2653dd numbering)

Source:
- src/lib.rs: 277-285 (the variant is renamed and documented); behaviour tests at 822, 847, 1001, 1038, 1047-48, 1175, 1178, and 1200 (`.0`).
- src/generation.rs: 29 (Identifiable import); 353, 445 (rename); after 786 (`Plain` trait); 876-885 (emission).
- src/checking.rs: 67, 286, 375, 597, 652, 1155, 1263, 1320, 1416, 1442 (rename, plus rustfmt reflow); 1432 (Struct arm); after 1455 (`Single` trait); after 1465 (Variant arm).
- src/conception.rs: 247, 475.
- src/protosization.rs: 140, 269.
- src/sectioning.rs: 161.
- src/location.rs: 12, 89-90.
- error.ethos: 24.
- src/error.rs: regenerated.

Fixtures:
- composition-types.ethos 8; empty-signal.ethos 1; generic-shadow.ethos 1; inline-collision.ethos 6-7 and 9; nested-collision.ethos 1; signal-decimal.ethos 5; tree-types.ethos 11 and 14.
- tests/generated/: 13 files regenerated (the diff stat is in the patch). src/ethos-zero.rs is unchanged.

Tests:
- tests/cli.rs: 164, 192, 202, 210, 228, 241, 278, 292.
- tests/ethos.rs: 17-26, 44, 92, 97, 113, 148, 164-168, 178-194, 216, 223, 244-288, 311-388; new tests after 522.
- tests/generated.rs: 76-98, 129, 183, 217, 271-273, 338-362, 375-381, 454-467; new test after 483.
- tests/flow_contract.rs: 29, 38, 44.

## Sources

- Design: /home/li/primary/flows/d5df1d/reports/ethos-solution.md, items 1 and 2.
- Previous run: /home/li/primary/flows/1d0733/reports/item2-dry-run.md.
- Patch: /home/li/primary/flows/1d0733/reports/item12-dry-run.patch. It is byte-identical (cmp) to the local mirror's diff.
- Witnesses: the cargo test, per-check `nix build` and ethos-zero `Check` runs on Prometheus in this flow's thread. Provenance receipt: unavailable.
