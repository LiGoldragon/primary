# 99/1 — schema-next typed macro library + nota-next structural-shape-extension

*Implementation sub-agent chapter (workflow run `wf_8724d72d-bd4`, 2026-06-12, system-designer lane). The adversarial review — which independently re-ran every test suite — is appended.*

# schema-next: typed macro library — hand parsing retired

## What landed

Two branches, both pushed, both fully green.

### nota-next `structural-shape-extension` (e92a9295) — general derive extension

The `StructuralMacroNode` derive gains one new general-purpose shape form, `#[shape(head = "...", body)]`, plus a vector node impl. This was genuinely required: the expansion-template heads `Fields` / `Variants` are variable-arity (`(Fields item*)`), and the source-entry head `SchemaMacro` carries a 4-field struct-shaped body — neither fits the existing `head = "...", arity = N` form whose variant field count is pinned to `arity - 1`.

- `derive/src/lib.rs:869` — `StructuralVariantShape::HeadedBody { head }`: matches a literal-headed parenthesis of **any** object count (`derive/src/lib.rs:999`), requires exactly one variant field (`:966`), and decodes the headed tail by handing it to the field type as a multi-block `MacroCandidate` at the field type's own `structural_position()` (`:805-827`). This is precisely nota-next INTENT's body abstraction ("the next semantic parsing step should receive the matched body's inner object stream rather than the outer delimiter wrapper") lifted into the derive. Encode writes `(Head body)`, eliding the space for an empty body (`:1124`).
- `src/macros.rs:1338` — `impl<Item: StructuralMacroNode> StructuralMacroNode for Vec<Item>`: a candidate's block sequence decodes as ordered items; encode space-joins. Mirrors the existing `Box<Inner>` blanket impl directly above it. Together with `body`, `(Head item*)` lists decode as `Vec<Node>` with zero consumer plumbing.
- `tests/macro_nodes.rs` — four new tests: vector body decode + encode round-trip, empty tail `(Variants)`, heterogeneous body through a hand `from_structural_candidate` struct, unknown head rejected as a dispatch error.
- `ARCHITECTURE.md` derive paragraph updated to document the new form. nota-next INTENT.md untouched (no psyche record to reflect there; its existing derive paragraph is non-exhaustive "such as ...").

### schema-next `typed-macro-library` (d7b34a24) — all three violation sites dissolved

Depends on the nota-next branch via `Cargo.toml`: `nota-next = { git = ..., branch = "structural-shape-extension" }` (lock pinned to e92a9295).

**Site 1 + 2 — entry dispatch and positional record wrapper, deleted.** `MacroLibrarySourceEntry::from_block` (the `record.variant_name()?.as_str() == "SchemaMacro"` match) and the entire `MacroLibrarySourceEntryRecord` wrapper (`child(0)..child(4)` with `.expect()`) are gone. The enum now derives `StructuralMacroNode` with `#[shape(head = "SchemaMacro", body)]` (`src/declarative.rs:1041-1043`). The headed tail decodes as the `SchemaMacro` definition body via a slice-pattern `from_structural_candidate` (`src/declarative.rs:257`): name through `schema_name()`, position through `MacroPosition`'s **keyword structural variants** (`src/macros.rs:29` — every position is `#[shape(keyword = "...")]`; the hand-written `MacroPosition::from_name` and `SchemaError::UnknownMacroPosition` are removed), pattern and template through their own typed nodes. No index arithmetic, no string-compared variant names; malformed input yields the structural no-match diagnostics (witnessed by `macro_library_source_rejects_malformed_definitions_with_typed_errors`).

**Site 3 — expansion-template head-string dispatch, deleted.** `MacroExpansionTemplate` (matching `"Type" | "Fields" | "Variants" | "Reference"`) and `MacroExpansionType` (matching `"Struct" | "Enum" | "Newtype"` one level down) are removed wholesale. `MacroTemplate` is now the typed structural macro node enum (`src/declarative.rs:592`):

- `#[shape(head = "Type", arity = 2)] Type(TypeTemplate)` — `TypeTemplate` (`src/declarative.rs:685`) carries `Struct` / `Enum` / `Newtype` as `head`-shaped variants of two template-object payloads each;
- `#[shape(head = "Fields", body)] Fields(Vec<MacroTemplateObject>)` and the same for `Variants` — the variable-arity case the derive extension exists for;
- `#[shape(head = "Reference", arity = 2)] Reference(MacroTemplateObject)`.

The template's output kind is part of its decoded structure: an unknown head now fails **when the library is read**, not mid-expansion, and expansion dispatches on the enum (`MacroTemplate::expand_output`, `src/declarative.rs:604`; `TypeTemplate::expand_declaration`, `:704`). The pre-existing rule that the live expansion path never re-parses text through `Document::parse` is preserved — payload expansion still produces owned `ExpandedObject` trees; compact notation survives only as the `MacroContext` diagnostic string.

**One typed read path, bidirectional.** `MacroLibrary::from_source` (`src/declarative.rs:49`) decodes the bootstrap document body as `Vec<MacroLibrarySourceEntry>` through one structural candidate; `MacroLibrary::to_source` (`:61`) writes the same notation back (capture sigils re-emitted by `MacroPatternObject::to_source_notation` `:504` / `MacroTemplateObject::to_source_notation` `:886`). `builtin()` (artifact, `NotaDecode`) and `builtin_source()` (bootstrap, `StructuralMacroNode`) are now both typed codecs over the same value; the freshness test still requires exact equality between them, and `schemas/builtin-macros.macro-library` was regenerated via `examples/emit_artifacts` because the template's typed-data projection changed shape (now `(Type (Struct (...)))`, `(Fields [...])`). Error surface: removed `UnknownMacroExpansionTemplate` + `UnknownMacroPosition`; added `ExpectedTemplateObjectCount` (`src/engine.rs:103`) for captures that expand to the wrong object count at single-object template positions.

**Tests.** Full suite 119 green (was 115), zero warnings. New in `tests/macro_exploration.rs`: `macro_library_bootstrap_source_round_trips_through_typed_nodes` (decode → encode → decode fixpoint over both the bootstrap notation and the artifact projection), `macro_library_source_rejects_malformed_definitions_with_typed_errors` (unknown head, short body, unknown position keyword), `expansion_template_enum_decodes_each_template_kind` (all four kinds + the three Type sub-kinds, with encode-back equality), `expansion_template_enum_rejects_unknown_heads_with_typed_errors` (outer and inner unknown heads → `UnsupportedMacroNodeStructure` / `MalformedSchemaNode`). The executable path is proven end-to-end by the untouched `builtin_macro_library_round_trips_as_typed_data_and_still_executes` and the user-macro design examples (`(SchemaMacro Bag TypeReference (Bag $Type) (Reference (Vector $Type)))` still registers and lowers).

**Docs.** `INTENT.md` gains the Spirit v0n6 reflection (quoted verbatim with identifier). `ARCHITECTURE.md` "Core Macro Schema" now describes the two typed codecs over one library value, the typed template enum, and the leaf-node status of the pattern/template object trees.

## Integration note for the operator lane

`schema-next@typed-macro-library` builds against `nota-next@structural-shape-extension`. Merge order: land the nota-next branch into nota-next `main` first, then flip schema-next's `Cargo.toml` dependency back to `branch = "main"` (one-line change + `cargo update -p nota-next`) when rebasing the schema-next branch onto main. Note the lock also moves nota-next forward from af6a208 to e92a9295, picking up two intervening main commits (bare-string canonicality, byte scalar codec) — the full schema-next suite is green against them.

## Design notes

- `SchemaMacro` survives as the definition noun (the architectural-witness test `operator_271_closed_claims::macro_library_source_entries_are_one_type` asserting `entry.definition() -> &SchemaMacro` passes unchanged); the body shape exists exactly so the noun did not have to be flattened into four loose variant fields.
- `MacroPosition`'s keyword variants make the position atom a recursively-decoded structural node — the same pattern as `StreamRelationKeyword` in `src/source.rs`, now covering an 8-variant enum.
- The `$`-sigil capture classification (`CaptureName::from_token`) is atom-text interpretation at a leaf, retained inside the leaf node impls; see notaGap for the precise boundary.

## branches
- nota-next @ structural-shape-extension head e92a9295d5dec15488c36a7bae202bd24200e7b0 (/home/li/wt/github.com/LiGoldragon/nota-next/structural-shape-extension)
- schema-next @ typed-macro-library head d7b34a241d7574741dc8280f7e910327676f3a24 (/home/li/wt/github.com/LiGoldragon/schema-next/typed-macro-library)

## testResults
== nota-next (branch structural-shape-extension) ==
     Running unittests src/lib.rs (target/debug/deps/nota_next-2009314bb359d204)
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/block_queries.rs — test result: ok. 10 passed; 0 failed
     Running tests/codec.rs — test result: ok. 14 passed; 0 failed
     Running tests/derive.rs — test result: ok. 9 passed; 0 failed
     Running tests/design_examples.rs — test result: ok. 6 passed; 0 failed
     Running tests/macro_nodes.rs — test result: ok. 14 passed; 0 failed
     Running tests/operator_271_closed_claims.rs — test result: ok. 6 passed; 0 failed
   Doc-tests nota_next — test result: ok. 0 passed; 0 failed
TOTAL: 59 passed, 0 failed

== schema-next (branch typed-macro-library) ==
     Running unittests src/lib.rs (target/debug/deps/schema_next-87faa6c295f7222b)
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/big_examples.rs — test result: ok. 3 passed; 0 failed
     Running tests/collections.rs — test result: ok. 13 passed; 0 failed
     Running tests/design_examples.rs — test result: ok. 13 passed; 0 failed
     Running tests/lowering.rs — test result: ok. 25 passed; 0 failed
     Running tests/macro_exploration.rs — test result: ok. 18 passed; 0 failed
     Running tests/operator_271_closed_claims.rs — test result: ok. 7 passed; 0 failed
     Running tests/raw_core_schema.rs — test result: ok. 6 passed; 0 failed
     Running tests/resolution.rs — test result: ok. 7 passed; 0 failed
     Running tests/source_codec.rs — test result: ok. 17 passed; 0 failed
     Running tests/symbol_path.rs — test result: ok. 5 passed; 0 failed
     Running tests/upgrade_pilot.rs — test result: ok. 5 passed; 0 failed
   Doc-tests schema_next — test result: ok. 0 passed; 0 failed
TOTAL: 119 passed, 0 failed (includes 4 new typed-codec tests); cargo build clean, zero warnings

## blockers


## notaGap
No fundamental gap blocked any of the three violation sites; all dispatch now runs through typed structural macro nodes. One precise boundary remains worth the psyche's eye: the pattern/template payload trees (MacroPatternObject / MacroTemplateObject) are universal mirrors of one NOTA object — any delimiter, arbitrary nesting, with $name / $*name capture atoms. They decode through hand-written leaf impls of the StructuralMacroNode trait (the sanctioned SourceVariantName pattern), not through the derive, because (a) the derive has no #[shape(...)] forms for sigil-prefixed atoms, any-atom fallback, or any-delimiter variants, and (b) more fundamentally, the Pattern capture engine captures blocks and bodies but cannot capture WHICH delimiter matched, which a tree-mirror type must store to re-encode. The matcher substrate itself can express sigiled atoms (AtomShape::with_sigil) and any-delimiter shapes (DelimitedShape::any), so this is a derive-vocabulary plus delimiter-capture limitation, not a hole in the macro-node mechanism; if tree-mirror types should also be derive-expressed, the pattern engine needs a delimiter capture kind.


## Adversarial review

VERDICT: approve

## mustFix

## advisory
- declarative.rs:615-644 (schema-next): MacroTemplate::expand_output Fields and Variants arms are near-duplicates — same expand loop, remember_expanded_template, from_objects(...).lower(...).map(...) differing only in head literal, lowering noun, and output constructor. A small contact-point type owning expand-and-trace would dissolve the duplication.
- declarative.rs:717,728,740-744 vs 622,637,649 (schema-next): trace-string construction is asymmetric — TypeTemplate::expand_declaration builds MacroContext traces with inline format!("(Type (Struct {} {}))", ...) while sibling MacroTemplate arms use the new ExpandedNotation::headed. Extending ExpandedNotation to nest a second head would unify all five trace sites.
- declarative.rs:772-774 (schema-next): ExpandedNotation::text() clones the String it just built for a construct-then-drain value; into_text(self) (or returning &str) fits the single-use shape better.
- derive/src/lib.rs:805-826 + 1075-1077 (nota-next): HeadedBody is special-cased by an early matches! return inside direct_decode_constructor, leaving an unreachable!() guard in direct_field_block. The shape enum should own its whole constructor generation per variant so the panic guard dissolves; today the dispatch for one shape is split across two methods.
- src/macros.rs:30-44 (schema-next): the eight #[shape(keyword = "RootImports")] attributes each repeat the variant name as a string. A derive shape that defaults the keyword to the variant identifier (e.g. pascal_keyword) would remove the eightfold duplication; worth a nota-next follow-up.
- derive/src/lib.rs:817-822 (nota-next, mirrors pre-existing Headed idiom): nested decode failures are flattened to error.to_string() inside StructuralMacroNodeError::Field, so the bootstrap path's typed inner SchemaError (e.g. ExpectedMacroDefinition) surfaces only as the string payload of SchemaError::MalformedSchemaNode (engine.rs:264-269). Typed at the crate surface, stringly underneath — a generic error parameter on Field would carry the cause; pre-existing design, not introduced here.
- declarative.rs:1536-1565 (ExpandedReference::type_reference matching "Vec"/"Vector"/"Optional"/"Map"/"Bytes"), :2117-2131 (MacroExpansionReference::lower_object matching "Vector"/"Optional"/"ScopeOf"/"Map"), :2078-2082 (StreamRelationObject::relation matching "opens"/"belongs"), :1857-1864 and 2011-2051 (root_object_at positional reads in MacroExpansionField/MacroExpansionVariant): head-string dispatch and positional indexing survive in the post-expansion lowering layer. All pre-existing on main and untouched-or-only-trimmed by this branch, but per Spirit v0n6 (everything reading NOTA-shaped structure above the raw parser goes through typed structural macro nodes) this layer is the next hand-parsing site to retire; deserves a bead so the constraint claim does not silently stop at the library codec boundary.
- Pre-existing clippy warnings remain (schema-next: large-enum-variant at src/macros.rs:218, too-many-arguments at src/schema.rs:219, manual-range-patterns at src/source.rs:35; nota-next: one MSRV lint). None are in files this branch touched; the implementer's zero-warnings claim is true for cargo build only.
- declarative.rs:261 / :360 / :911 (schema-next): the leaf impls use prose PositionPredicate::named values with spaces ("macro definition body", "macro pattern", "macro template object") where every other position name is a PascalCase atom; harmless because these never enter the MacroRegistry, but inconsistent if positions ever serialize.
- I could not independently verify Spirit record v0n6 against the intent store (reviewer lane has no Spirit access); the INTENT.md addition quotes it with identifier and kind in the prescribed bracket form and matches the branch's design direction.

## disciplineFindings
- Free functions: none introduced. All new nota-next code lives on StructuralVariantDerive / StructuralVariantShape impls (derive/src/lib.rs:743-1160) and the Vec<Item> trait impl (src/macros.rs:1335-1368); all new schema-next code lives on impl blocks for SchemaMacro, MacroPattern, MacroTemplate, TypeTemplate, ExpandedNotation, MacroTemplateObject, MacroLibrarySourceEntry. Test-file free functions are #[cfg(test)]-exempt.
- Zero-sized namespace types: none. ExpandedNotation (declarative.rs:758-775) carries a String; DelimitedNotation/NotationBlock are pre-existing data-bearing values. The existing guard test derive_crate_carries_no_zst_method_holders still passes.
- Naming: every new identifier is a full English word (HeadedBody, TypeTemplate, ExpandedNotation, expand_declaration, expand_single, expand_schema_name, to_source_notation, body_blocks). No crate-name prefixes, no ancestry repetition (TypeTemplate inside the macro-template context, not MacroTypeTemplate).
- Errors: no anyhow anywhere; SchemaError remains the hand-written per-crate enum (engine.rs:49+), extended with typed ExpectedTemplateObjectCount {position, expected, found} replacing the removed UnknownMacroPosition / UnknownMacroExpansionTemplate string-bag variants — a net typing improvement.
- Hand-rolled parsing: the branch removes hand parsing — MacroLibrarySourceEntryRecord (positional 5-object record with child(index) at old declarative.rs:1077-1126), MacroPosition::from_name string match (macros.rs), MacroExpansionTemplate head-string dispatch on Type/Fields/Variants/Reference, and MacroExpansionType dispatch on Struct/Enum/Newtype are all deleted. No new text parsing introduced; encode side emits bare atoms only, never quotation marks.
- Constraint 'fully on typed structural macro nodes': holds for the macro-library codec. from_source decodes through Vec<MacroLibrarySourceEntry>::from_structural_candidate (declarative.rs:49-58); the entry is #[shape(head = "SchemaMacro", body)] (declarative.rs:1041-1044); the body decodes via slice pattern [name, position, pattern, template] (declarative.rs:271-282); MacroPosition is keyword structural variants (src/macros.rs:30-44); MacroTemplate/TypeTemplate are derived structural enums (declarative.rs:592-601, 685-701); patterns/template-objects are documented any-shape leaf nodes (declarative.rs:352-385, 903-936).
- Constraint 'no stringly dispatch / no positional child indexing': holds in the codec — zero root_object_at and zero head.as_str() matches remain on the library read path; both survive only in the pre-existing post-expansion lowering layer (see advisory).
- Constraint 'single typed read path': bootstrap notation and artifact projection now decode into the same MacroLibrary value through derived codecs; the parallel hand-parse path is gone, and decode->encode->decode is asserted as a fixpoint over both projections (tests/macro_exploration.rs:909-921).
- Constraint 'canonical round-trip preserved': the regenerated schemas/builtin-macros.macro-library artifact (new (Type (Struct ...)) template form) is freshness-checked against the hand-authored .schema source by the existing test at tests/macro_exploration.rs:358-370, which passes. The artifact format break is clean pre-production breakage with the in-repo consumer updated — no compatibility shim, none presented as a virtue.
- Cross-repo dependency done right: schema-next Cargo.toml points nota-next at branch structural-shape-extension (no local path patch), Cargo.lock pins commit e92a9295, and git ls-remote confirms both branches pushed at exactly the claimed head commits (nota-next e92a9295d5de, schema-next d7b34a241d75), so the branch builds anywhere.
- Test quality: nota-next's new heterogeneous-body test hand-implements StructuralMacroNode for DerivedSignature (tests/macro_nodes.rs:644-689), exercising the exact downstream extension point schema-next's SchemaMacro impl uses — a genuine witness, not a mock. Both repos assert decode AND encode plus typed error paths (empty tail, short body, unknown head, unknown position).

## testHonesty
Re-ran cargo test myself in both worktrees at the claimed head commits. nota-next: 59 passed, 0 failed (block_queries 10, codec 14, derive 9, design_examples 6, macro_nodes 14, operator_271 6), exactly matching the claim including the 4 new body-shape tests. schema-next: 119 passed, 0 failed across 11 suites, exactly matching the claim including the 4 new typed-codec tests in macro_exploration.rs. cargo build is clean in both (the zero-warnings claim holds for build; cargo clippy shows 3 pre-existing warnings in schema-next files and 1 MSRV lint in nota-next, all in files this branch never touched). The new tests prove the claimed witnesses rather than flattering: they drive real NOTA text through the real parser and derive-generated code, assert both decode and encode (round-trip fixpoint over both library projections at macro_exploration.rs:909-921), assert typed error variants for malformed input, and the freshness test (macro_exploration.rs:358-370) independently confirms the regenerated artifact matches the hand-authored source through the new typed enum. No hidden failures found.

