*Kind: Mockup · Topic: extensible-macro-variant-engine · Date: 2026-05-24 · Lane: second-designer-assistant (sub-agent C)*

# 172/3 · Extensible macro-variant lowering engine — mockup

## §1 Worktree + branch + commit

- Worktree: `/tmp/mockup-c-macro-variant-engine`
- Source repo: `/git/github.com/LiGoldragon/schema`
- Branch: `feature/macro-variant-engine`
- Commit short-id: `e4a86450`
- Bead: `primary-oh6i` ([mockup] schema extensible macro-variant lowering engine — second-designer/172 slice C)

## §2 What was implemented

Two new modules sitting alongside the existing `Schema::assemble` path so the architecture can be demonstrated without removing the operator's landed lowering code.

### §2.1 `src/macro_variant.rs`

- `MacroVariant` — data-carrying enum (9 members), each carrying its own input struct that defines the shape it consumes at the node-definition point:
  - `EnumDeclaration(EnumDeclarationInput)`
  - `NewtypeDeclaration(NewtypeDeclarationInput)`
  - `RecordDeclaration(RecordDeclarationInput)`
  - `AliasDeclaration(AliasDeclarationInput)`
  - `ImportedType(ImportedTypeInput)`
  - `ReplyFeature(ReplyFeatureInput)`
  - `EventFeatureMacro(EventFeatureInput)`
  - `ObservableFeatureMacro(ObservableFeatureInput)`
  - `UpgradeFeatureMacro(UpgradeFeatureInput)`
- Per-variant input structs (`EnumDeclarationInput`, `NewtypeDeclarationInput`, `RecordDeclarationInput`, `AliasDeclarationInput`, `ImportedTypeInput`, `ReplyFeatureInput`, `EventFeatureInput`, `ObservableFeatureInput`, `UpgradeFeatureInput`) — each holds exactly the data the lowering branch needs.
- `MacroVariantLowering` trait — `type Output; fn lower(&self, context: &LoweringContext<'_>) -> Result<Self::Output>`. Implemented for every input struct; this is the substrate both for the built-in match dispatch and for a future trait-object plugin surface (see §4).
- `LoweringContext<'a>` — threaded through the lowering walk; carries the component name + resolved imports. Future shape rules (UID-prefixing per `/170` §5; cross-schema qualification) hang off this struct without touching variant code.
- `LoweredNode` — `Type(AssembledType) | FeatureBinding(FeatureBinding)`; the output of one `lower()` call.
- `FeatureBinding` — engine-side mirror of `Feature` so the engine can fan multiple inputs back into the assembled feature list without losing variant identity, plus `into_feature()` for the round-trip.
- `MacroVariant::lower` — the dispatch table. Pure `match self { Self::EnumDeclaration(input) => ... }` — no shape inspection, no name special-casing. New variant types land by adding a new arm.

### §2.2 `src/lowering_engine.rs`

- `LoweringEngine` — owns `component: Name`, `variants: Vec<MacroVariant>`, and `RoutingInputs` (the three header legs + resolved imports the route walk consumes). Constructors:
  - `LoweringEngine::from_schema(schema, component, resolutions) -> Result<Self>` — walks an existing `Schema`'s namespace, imports, and features into the variant catalog. This is the bridge enabling the equivalence test in §3.
  - `LoweringEngine::from_variants(component, variants, ordinary_header, owner_header, sema_header, import_bindings)` — the path future schema-language readers will take after they stop detouring through `Schema`.
- `LoweringEngine::lower(&self) -> Result<AssembledSchema>` — the dispatch walk:
  1. Iterate `self.variants`, call `variant.lower(&context)` on each, bin the `LoweredNode` into either `types` or `features`.
  2. Lower the three header legs by walking variants matched against the assembled types (`lower_header` mirrors `Schema::lower_header`'s variant-coverage validation).
  3. Assemble the four bins into `AssembledSchema`.

Headers stay outside `MacroVariant` for now because routes consume the already-lowered namespace — they're not node-definition points. A follow-up beyond intent 506 could model them as macro-variants too; the comment in the lower() method calls this out.

### §2.3 `src/lib.rs`

Module declarations for `macro_variant` and `lowering_engine`. Public re-exports for `MacroVariant`, `MacroVariantLowering`, `LoweringContext`, `LoweredNode`, `FeatureBinding`, every input struct, and `LoweringEngine`.

## §3 Tests

`tests/macro_variant.rs` — 8 tests, all passing:

1. `enum_declaration_input_lowers_to_local_enum_assembled_type` — `EnumDeclarationInput { name: Kind, variants: [Decision, Principle] }.lower(context)` → `AssembledType::Local { name: Kind, body: DeclarationBody::Enum { variants: [Decision, Principle] } }`.
2. `newtype_declaration_input_lowers_to_local_newtype_assembled_type` — `NewtypeDeclarationInput { name: Topic, inner: String }.lower(context)` → `AssembledType::Local { name: Topic, body: DeclarationBody::Newtype(String) }`.
3. `record_declaration_input_lowers_to_local_record_assembled_type` — three-field record lowers to `DeclarationBody::Record(fields)` with three entries.
4. `macro_variant_dispatches_each_input_to_the_correct_lowering_branch` — three different variants in one Vec each take the right `MacroVariant::lower` branch.
5. **`engine_lowers_to_same_assembled_schema_as_assemble`** — the equivalence test. Builds the same Spirit MVP schema both `Schema::assemble` and `LoweringEngine::from_schema(...).lower()` consume, then asserts routes / types / imports / features all match. **This proves the architecture is behavior-preserving** — operator can replace `assemble()` with the engine surface without changing the lowered output.
6. `engine_walks_explicit_variant_catalog_without_schema_construction` — demonstrates `LoweringEngine::from_variants` so future macro-language readers can populate the catalog directly from parsed NOTA.
7. `imported_type_macro_variant_lowers_to_imported_assembled_type` — covers the import path.
8. `feature_macro_variant_lowers_to_feature_binding` — covers the feature-macro arm.

Validation pipeline:

- `cargo test` — 16 existing tests + 8 new = 24 tests, all pass.
- `cargo fmt -- --check` — clean.
- `cargo clippy --all-targets -- -D warnings` — clean.
- `nix flake check --option max-jobs 0 path:.` — all checks passed (build / clippy / doc / fmt / test). The `path:.` form is needed because the jj workspace at `/tmp/mockup-c-macro-variant-engine` doesn't carry `.git`, so flake's default git-discovery walks up to `/tmp` and fails. Documenting this for operator — a colocated `jj git init --colocate` would solve it, or the operator can run nix from the main repo path.

## §4 Design choices and trade-offs

### §4.1 Why input-struct-per-variant (intent 506 essence)

The psyche framing: "a struct defining its input type for that macro-variant." Two implications drive the shape:

1. **Each macro-variant fixes the shape of data it consumes at the node-definition point.** The current `DeclarationBody::Enum { variants }` mixes shape (enum) and payload (variants vector) in one anonymous data-bearing enum variant; the macro-variant approach gives every shape its own named input struct (`EnumDeclarationInput`, `RecordDeclarationInput`, etc.) so the input language and the dispatch language match.
2. **Dispatch is a direct match on the macro-variant — no shape inspection.** The /170 dispatch table examines bracket shape (`[…]` vs `(T)` vs `(F1 F2 …)`). In the macro-variant world, the bracket-shape inspection happens once during parsing (NOTA tree → MacroVariant), and the lowering walk just matches on the enum tag. Two phases, each clean.

### §4.2 Extensibility — trait-based plugin vs recompile

The two approaches:

- **Trait-based plugin** — `MacroVariantLowering` is a trait. Users implement it for their own input types and register them with the engine via something like `LoweringEngine::register::<MyVariantInput>()`. The engine stores `Vec<Box<dyn MacroVariantLowering<Output = LoweredNode>>>`. New variants add at runtime; the schema crate doesn't need recompilation.
- **Add-enum-member-and-recompile** — `MacroVariant` is a closed enum. New variants land by adding a new enum member + input struct + `MacroVariantLowering` impl + new arm in `MacroVariant::lower`. The schema crate recompiles every time.

**This mockup picked add-enum-member-and-recompile.** The reasoning:

- The MVP needs ~5–10 macro variants total (enum / newtype / record / alias / imported-type, plus the 4 feature kinds — already enumerated in §2.1). Trait-object indirection adds complexity that pays off only when external crates want to add variants.
- Closed enums let the compiler enforce exhaustive `match` in `MacroVariant::lower`, so adding a new variant gets you a "you forgot to handle this variant" compile error at every consumer site. Trait-object dispatch loses that.
- The `MacroVariantLowering` trait is still in the public surface; if a future use case wants an open-world plugin pattern, the engine can grow a parallel `register::<T>()` path without breaking the closed-enum default. The trait existing today keeps that door open.
- Per intent 506's "builtin variants at nodeDefinition points," the variants ARE built-in to the engine. The extensibility the psyche named is the schema language's expressive power — adding a new built-in shape (e.g., a `Tagged` variant for sum-type-with-discriminant) is a recompile, not a plugin.

Operator: if you have a use case that demands runtime-registered variants (e.g., language plugins per /170 §6.1), the trait surface is already there — wire it up alongside the closed enum.

### §4.3 Relationship to /170 (shape-based dispatch)

`/170` describes the parse-time dispatch — examining `[…]` vs `(T)` vs `(F1 F2 …)` shapes in the NOTA tree to pick the right lowering branch.

The macro-variant engine in this mockup is the **lowering-time dispatch** — the shape inspection from /170 has already happened (during parsing) and produced typed `MacroVariant` values; the engine then dispatches on the variant tag.

The two are **complementary, not duplicative**:

- /170's shape dispatch happens in the NOTA parser → `MacroVariant` conversion (which this mockup doesn't implement; it skips straight to typed variants).
- This mockup's match dispatch happens in `MacroVariant::lower` → `LoweredNode`.

A complete implementation would have both phases:

```
NOTA tree (parsed) → [/170 §2 dispatch] → MacroVariant catalog → [this mockup's engine] → AssembledSchema
```

The combined pipeline subsumes the today's hardcoded path (parse straight into `Schema` via `parser.rs`, then `Schema::assemble`).

### §4.4 Should `MacroVariant` be the canonical lowering interface?

**Operator decision; the mockup is shaped to make either choice viable.**

The equivalence test (`engine_lowers_to_same_assembled_schema_as_assemble`) proves the engine produces identical output to `Schema::assemble` for the Spirit MVP schema. If operator wants:

- **Engine as the new canonical surface** — keep `Schema::assemble` as a thin wrapper that calls `LoweringEngine::from_schema(self, component, resolutions).lower()`. The hardcoded shape rules in `Schema::lower_header` / `Schema::endpoint_body` move into the engine; `Schema` shrinks to a parsed-but-not-yet-lowered representation. This is the direction /170 §11.2 points to.
- **Engine as an alternative interface** — keep both. `Schema::assemble` stays the validated authoritative path; the engine serves callers that build the variant catalog from parsed NOTA without first materialising a `Schema`. Less aggressive refactor.
- **Engine as the macro-emit substrate** — keep `Schema` validation, but use the engine as the substrate downstream consumers (Rust codegen, schema-doc, schema-diff) read. The engine's variant catalog is the canonical-form integration point per /170 §10.

My lean: **direction one**. The engine cleanly factors the "what shape does each declaration become" rule into one place (`MacroVariantLowering` impls) instead of two (`DeclarationBody` enum + `Schema::assemble`/`Schema::lower_header` walks). The closed-enum match keeps the compiler error budget the same as today. The header lowering eventually moves into variants too (the comment in `LoweringEngine::lower` notes the follow-up). But this is operator's call.

## §5 Reference to operator's existing implementation

The current hard-coded lowering lives at:

- `src/document.rs` — `Schema::assemble` (lines 91-114), `Schema::lower_header` (lines 248-268), `Schema::endpoint_body` (lines 286-324). These are the methods the engine would replace if operator chooses direction one in §4.4.
- `src/declaration.rs` — `DeclarationBody` enum (lines 51-57) is the current shape representation. The engine's input structs (`EnumDeclarationInput` etc.) are 1:1 with `DeclarationBody` variants but each shape gets its own struct so the engine's match dispatch is cleaner.
- `src/feature.rs` — `Feature` enum (lines 3-9) becomes the inputs for the four feature macro-variants.
- `src/assembled.rs` — `AssembledSchema` and `AssembledType` are reused as the engine's output bins; no changes needed.

The engine builds on (does not replace) the existing types — it lifts the dispatch into a typed enum + trait shape without touching the validated authoritative model.

## §6 Psyche questions surfaced

1. **Extensibility approach** — decided in this mockup per §4.2 (closed enum + recompile, with `MacroVariantLowering` trait kept public for future runtime-registered surface). Operator confirms or asks for the trait-object path. **(Recommendation: keep the closed enum default; revisit when a use case demands runtime plugins.)**
2. **Should header lowering also become macro-variants?** The mockup keeps headers outside the variant catalog because routes consume the already-lowered namespace, not raw node definitions. Intent 506 names "builtin variants at nodeDefinition points" — header roots are arguably nodeDefinition points too. **(Recommendation: track separately; the current shape is enough to validate the architecture but the cleaner long-term shape probably models routes-from-headers as variants too.)**
3. **`LoweringContext` shape** — the mockup carries `component: &Name` and `imports: &[ImportBinding]`. The /170 §5 UID-prefixing rule needs the context to also carry a `namespace_path` segment so each lowered type knows its full UID. Adding it is straightforward (one field on `LoweringContext`, no variant changes) but worth confirming the operator wants the engine to be UID-aware versus having a separate UID-stamping pass over the engine's output.
4. **Trait `Output` associated type** — the mockup uses `type Output;` per implementor (each returns either `AssembledType` or `FeatureBinding`), then `MacroVariant::lower` boxes both into `LoweredNode`. An alternative: every implementor returns `LoweredNode` directly, dropping the associated type. The current shape preserves type-precision for downstream code that knows which variant it has; the alternative simplifies the trait. Operator's call.
5. **Engine equivalent of the existing `Schema::validate_*` family** — the mockup punts validation to `Schema::assemble` (the `from_schema` path calls `schema.assemble(resolutions)?` for resolution-and-validation), then lifts the resulting data into variants. A pure-engine pipeline would need validation lifted into the engine too. Operator: do you want the validation rules to live with the macro variants (each input struct validates its own data) or stay as schema-level rules?

## §7 Recommendation for operator

**Pick the best bits — engine as the macro-emit substrate (§4.4 direction three), with the trait still public for future plugin variants.**

The equivalence test is the contract: as long as the engine output matches `assemble()` output, downstream consumers (Rust codegen for `cargo schema-codegen`, schema-doc, schema-diff) can read the engine's typed variant catalog as the canonical form. The existing `Schema::assemble` validation pipeline stays as the authoritative entry point that builds the engine.

Once that lands, the follow-up to fold `Schema::lower_header` / `Schema::endpoint_body` into a HeaderMacroVariant is cleanly separable — it's its own intent-record-and-mockup loop, no urgent integration cost.

## §8 References

- Intent record 506 — schema-lowering-engine clarification (the directly-motivating psyche statement).
- `reports/second-designer/170-schema-lowering-executor-model-2026-05-24.md` — the lowering-executor model this engine implements.
- `reports/second-designer/172-design-mockup-dispatch/0-frame-and-method.md` §3.3 — dispatch frame for slice C.
- `reports/second-operator/180-schema-v13-model-and-upgrade-implementation-2026-05-24.md` — current schema implementation operator landed.
- Source files (mockup) — `/tmp/mockup-c-macro-variant-engine/src/macro_variant.rs`, `/tmp/mockup-c-macro-variant-engine/src/lowering_engine.rs`, `/tmp/mockup-c-macro-variant-engine/tests/macro_variant.rs`.
- Source files (current implementation) — `/git/github.com/LiGoldragon/schema/src/document.rs` (lines 91-324), `/git/github.com/LiGoldragon/schema/src/declaration.rs`, `/git/github.com/LiGoldragon/schema/src/assembled.rs`.
