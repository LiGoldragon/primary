# 358 — NOTA library + schema-schema prototype

*Designer-assistant implementation of records 799-807 (Maximum except 806 carry-uncertainty). Layers on top of sibling subagent aed752c4's block-by-block parser slice (records 774-777). Narrows NOTA's API to a structural-query library, implements the schema-schema as core Rust (the macro interface), demonstrates the root-struct-implied-by-.schema model, and pins each load-bearing intent in 799-807 as a named constraint test per record 777.*

## Summary

| Repo | Branch | HEAD | Tests | Nix check |
|---|---|---|---|---|
| `schema` | `designer-schema-schema-prototype-2026-05-26` | `cc0c340` | 51/51 prototype tests | green |

The branch is based on aed752c4's `designer-schema-derived-nota-2026-05-26` (which carries `/354`'s prototype + aed752c4's block-by-block parser slice). The new branch ADDS the schema-schema layer; it does not modify aed752c4's `blocks.rs` or `block_parser_constraints.rs` semantically.

Worktree: `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-schema-prototype-2026-05-26/`. Branch pushed to `origin/designer-schema-schema-prototype-2026-05-26`.

## Coordination state with aed752c4

What aed752c4 landed (visible at session start):

- Three new repos `spirit`, `signal-spirit`, `core-signal-spirit` with skeleton structure (README, ARCHITECTURE.md, INTENT.md, Cargo.toml, flake.nix). The `spirit/schema/spirit.schema` is populated; `spirit/src/lib.rs` is a placeholder.
- `nota-next` branch on the existing `nota` repo — a fresh starter commit with no implementation yet (zero file changes vs main, just the bookmark anchor).
- On the existing `/354` schema worktree (`designer-schema-derived-nota-2026-05-26`): two new files — `prototype/src/blocks.rs` (block parser with `SourceSpan`, `SourcePosition`, `DelimiterKind`, `Block` carrying delimiter classification + `holds_root_objects` + `root_object_at(n)` + recursive shape predicates like `second_root_object_is_a_square_bracket_object`) and `prototype/tests/block_parser_constraints.rs` (12 named constraint tests pinning records 774-776).

What I built on top:

- `prototype/src/block_query.rs` — the NOTA library's REFINED narrow API surface per records 799-803 + /357 §2. Methods on `Block` (not replacing the `_block`-suffixed ones aed752c4 wrote — supplementing). Distinguishes FACTUAL `is_X_bracket()` from STRUCTURAL `qualifies_as_X()` per the record 800 discipline.
- `prototype/src/schema_schema.rs` — the schema-schema as core Rust per record 807. `Macro` trait, `MacroContext`, `SchemaSchema::default()`, `parse_schema_file` treating .schema text as the implied root struct per record 805.
- `prototype/src/bin/schema_schema_demo.rs` — end-to-end demo exercising the whole stack against `coordinate.schema`.
- `prototype/tests/schema_schema_constraints.rs` — 10 named constraint tests pinning records 799-807.

Boundary: aed752c4's code paths (`blocks.rs`, `block_parser_constraints.rs`) are not semantically modified. The only edit to `block_parser_constraints.rs` is `cargo fmt` output to satisfy the project rustfmt rule (without it `nix flake check` fails on the fmt check). The new layer uses aed752c4's `Block` struct and methods via additive composition (extra impl-block on `Block` in `block_query.rs`).

Where the work belongs eventually: per the brief, when `nota-next` lands the block parser, the refined `block_query.rs` surface migrates there as the canonical NOTA-library home. For now the work lives in the schema prototype crate, ready to lift.

## Deliverable A — NOTA library surface

The `block_query.rs` module adds the refined-API methods to `Block` per /357 §2. Key methods:

```rust
impl Block {
    // FACTUAL — record 799 (delimiter classification is fact)
    pub fn is_square_bracket(&self) -> bool;
    pub fn is_parenthesis(&self) -> bool;
    pub fn is_brace(&self) -> bool;

    // STRUCTURAL — records 800, 801 (qualifies, does not decide)
    pub fn qualifies_as_symbol(&self) -> bool;
    pub fn qualifies_as_pascal_case_symbol(&self) -> bool;
    pub fn qualifies_as_camel_case_symbol(&self) -> bool;
    pub fn qualifies_as_kebab_case_symbol(&self) -> bool;
    pub fn qualifies_as_string(&self) -> bool;
    pub fn qualifies_as_literal(&self) -> bool;

    // The unified classification — defaulting to highest (record 801)
    pub fn classification(&self) -> Option<Classification>;
    pub fn delimiter_block_kind(&self) -> Option<BlockKind>;
    pub fn source_span(&self) -> SourceSpan;
}
```

The `Classification` enum encodes the default-to-higher rule (record 801):

```rust
pub enum Classification {
    Block(BlockKind),                  // highest
    QualifiedSymbol(SymbolKind),
    String,
    Literal(LiteralKind),               // lowest
}
```

When a token COULD be a symbol AND a string, `classification()` returns `QualifiedSymbol(...)` (the higher form). The schema layer demotes to `String` when its type context requires.

The vector-content rule (record 802) is enforceable structurally: every element of a vector either classifies as `QualifiedSymbol(...)` (a bare type name) or as `Block(...)` (a nested vector / record / map). Pinned by `constraint_802_vector_contents_are_qualified_symbols_or_blocks`.

The `BlockReassembler::reemit_concatenated` static method provides the refined-API form of the reassembly primitive per record 776 — preserved here on an `impl` block to satisfy the methods-only discipline.

## Deliverable B — schema-schema as core Rust

The `schema_schema.rs` module implements the macro interface per record 807. Core types:

```rust
pub trait Macro: Send + Sync {
    fn name(&self) -> &str;
    fn matches_shape(&self, block: &Block) -> bool;
    fn lower(&self, block: &Block, ctx: &MacroContext)
        -> Result<AssembledNode, MacroError>;
}

pub struct MacroContext {
    pub namespace: NamespaceTable,
    pub parent: Option<Arc<MacroContext>>,
    pub schema_schema: Arc<SchemaSchema>,
}

pub struct SchemaSchema {
    builtin_macros: Vec<Arc<dyn Macro>>,
}

impl SchemaSchema {
    pub fn default() -> Self {
        let builtin_macros: Vec<Arc<dyn Macro>> = vec![
            Arc::new(ImportsSectionMacro),
            Arc::new(InputOutputStructMacro),
            Arc::new(NamespaceSectionMacro),
        ];
        Self { builtin_macros }
    }
    pub fn parse_schema_file(&self, source: &str)
        -> Result<AssembledSchema, SchemaError>;
    pub fn lower_via_macros(&self, source: &str, ctx: &MacroContext)
        -> Result<Vec<AssembledNode>, MacroError>;
    pub fn dispatch_for(&self, block: &Block) -> Option<&Arc<dyn Macro>>;
    pub fn lookup_macro(&self, name: &str) -> Option<&Arc<dyn Macro>>;
}
```

Three built-in macros are the load-bearing primitives:

- `ImportsSectionMacro` — matches `{...}` brace blocks with paired `(Pascal (ImportTag ...))` entries. Lowers to `AssembledNode::ImportsTable`.
- `InputOutputStructMacro` — matches `[...]` square-bracket blocks containing `(Tag (Payload))` operation records. Lowers to `AssembledNode::InputOutputStruct` with operation declarations.
- `NamespaceSectionMacro` — matches `{...}` brace blocks with paired (PascalCase / camelCase) keys and arbitrary type-body values. Lowers to `AssembledNode::Namespace` with declarations.

The .schema extension implies the root struct (record 805). `parse_schema_file` accepts text containing ONLY the positional fields — no explicit `(Schema ...)` wrapping. `lower_via_macros` dispatches by POSITION (block 0 = imports, block 1 = input header, block 2 = input extras, block 3 = namespace, block 4 = output) per the Option-A field ordering carried in /357 §6 (the record 806 carry-uncertainty).

The macro context (`MacroContext`) carries the namespace table, a parent-context chain (for nested macros), and a back-reference to the schema-schema itself — so user-defined macros can recursively dispatch to the built-ins.

## Deliverable C — end-to-end demo

`prototype/src/bin/schema_schema_demo.rs` runs the full chain against `coordinate.schema`. Sample output (full demo binary exits 0):

```text
=== schema-schema + NOTA library demo ===

[1] NOTA library — parse_blocks on coordinate.schema
    5 top-level blocks parsed
      block[0]: span=371..463  kind=Block(Brace)  root_objects=0
      block[1]: span=543..619  kind=Block(SquareBracket)  root_objects=3
      block[2]: span=699..701  kind=Block(SquareBracket)  root_objects=0
      block[3]: span=781..1083  kind=Block(Brace)  root_objects=20
      block[4]: span=1163..1186  kind=Block(SquareBracket)  root_objects=1

[2] Default schema-schema — SchemaSchema::default()
    3 built-in macros registered
      - imports_section
      - input_output_struct
      - namespace_section

[3] Lower via macro dispatch (positional)
    5 AssembledNode(s) emitted
      [0] ImportsTable — 0 entries
      [1] InputOutputStruct — 3 operations
            (Move) payload-types: [(MoveRequest)]
            (Rotate) payload-types: [(RotateRequest)]
            (Read) payload-types: [(ReadRequest)]
      [2] InputOutputStruct — 0 operations
      [3] Namespace — 10 declarations
            Coordinate = (square-bracket 2 elements)
            Position = (square-bracket 1 elements)
            Angle = (square-bracket 1 elements)
            ...
            Reply = (parenthesis 2 elements)
      [4] InputOutputStruct — 1 operations
            (Replied) payload-types: [(Reply)]

[4] parse_schema_file → AssembledSchema (positional root struct)
    input_operations: 3 | output_operations: 1 | namespace entries: 10
    input ops: Move Rotate Read
    output ops: Replied

[5] Root struct IMPLIED by .schema extension (record 805)
    coordinate.schema's source contains NO (Schema ...) wrapping —
      (Schema ...) present? false   (Root ...) present? false
    The five top-level blocks ARE the positional fields of the
    implied root struct.

=== demo complete ===
```

The end-to-end path is:

1. `coordinate.schema` text →
2. `BlockParser::parse_blocks` (NOTA library surface) →
3. `SchemaSchema::default()` (schema-schema loaded implicitly) →
4. positional macro dispatch (`lower_via_macros`) →
5. `AssembledSchema` (typed declarations).

No explicit root declaration appears in the source. The five top-level blocks ARE the positional fields of the implied root struct.

## Deliverable D — constraint tests

10 named tests in `prototype/tests/schema_schema_constraints.rs`. Verbatim output:

```text
running 10 tests
test constraint_799_block_exposes_structural_query_methods ... ok
test constraint_800_pascal_token_qualifies_but_does_not_decide_type ... ok
test constraint_801_parser_defaults_to_higher_classification ... ok
test constraint_802_vector_contents_are_qualified_symbols_or_blocks ... ok
test constraint_803_nota_does_not_perform_schema_resolution ... ok
test constraint_804_default_schema_schema_loads_implicitly ... ok
test constraint_805_root_struct_implied_by_dot_schema_extension ... ok
test constraint_805_root_struct_field_positions_are_load_bearing ... ok
test constraint_806_field_ordering_option_a_pending_psyche_decision ... ok
test constraint_807_macro_interface_publicly_exposed ... ok

test result: ok. 10 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

Note: record 805 gets TWO tests — one pinning the implied-root-struct claim (no explicit wrapping in source), one pinning the positional-field-ordering claim (block 0 lowers as imports, block 3 lowers as namespace).

Full test count across the prototype crate:

| File | Tests | Source |
|---|---|---|
| `kernel.rs` | 15 | /354 |
| `schema.rs` | 14 | /354 |
| `block_parser_constraints.rs` | 12 | aed752c4 |
| `schema_schema_constraints.rs` | 10 | this work |
| **Total** | **51** | |

All 51 pass. `nix flake check` is green (all attrs: build, doc, fmt, test).

## What couldn't be done / open shape questions

Per the carry-uncertainty discipline (don't infer to close design gaps — record 735):

1. **Macro dispatch by position vs by content discriminator (record 805 follow-up).** The schema-schema's `lower_via_macros` discriminates the two brace blocks (imports vs namespace) by POSITION in the .schema file. The alternative is content discrimination — but both brace blocks legitimately can contain paren-valued entries (imports values are paren records; namespace values include enum variants which are also paren records). Position works only IF the root-struct field-ordering is fixed (the open carry-uncertainty 806 — Option A vs Option B). The prototype defaults to Option A per /357 §6. If psyche picks Option B, the dispatcher positional table flips.

2. **Empty input/output blocks lower as `InputOutputStruct { input_operations: [], output_operations: [] }`.** The `AssembledNode::InputOutputStruct` carries both input + output operations in one variant, but the macro that produces it doesn't know which side it's on. Currently every block 1/2/4 lowers as if it's input. The caller (`parse_schema_file`) sees the right shape because it uses the existing `ThreePartSchema::read` path which tracks position. The macro layer's `lower_via_macros` produces less-precise output for output-block 4 (it labels operations as `input_operations` regardless). Cleanup: split `InputOutputStructMacro` into two macros (`InputStructMacro` / `OutputStructMacro`) OR thread position into the macro's `lower` signature. Open shape question.

3. **The `Macro::lower` signature returns `AssembledNode`, not a typed-payload-per-macro.** Currently every macro returns the same enum; downstream code matches on variants. The alternative is `Macro<Output>` where `Output` is the macro's domain type. That's the path toward record 807's claim "a macro's input type IS its name in the macro" — but it requires either trait objects with type erasure (loses the typed payload) or generics with monomorphisation (loses dyn dispatch). The current shape sacrifices the typed-output for the polymorphism; the inverse trade-off is also valid. Open question for psyche on which side to favour.

4. **The `BracketString` / `BlockString` discrimination in `LiteralKind`.** I added these as variants but they're under-tested — the kernel's `lex_inline_bracket_string` path is the one source. NOTA strings come EXCLUSIVELY from bracket forms; the `Classification::String` variant covers both. The `LiteralKind::BracketString` / `BlockString` variants exist for callers that want to discriminate the two — but no test exercises this distinction. Whether it's worth keeping separate variants is a question for the next iteration.

5. **The `qualifies_as_string()` method returns true ONLY for explicit bracket-string syntax in the kernel.** Per record 801 the discipline is: parser defaults UP to symbol; string demotion is the schema layer's job. So `qualifies_as_string()` is a query about what the SOURCE looks like, not what a type-context-aware interpreter might decide. This matches the design but may surprise callers expecting "string-able" to include identifier-shaped leaves. Worth a doc-comment clarification; not a code change yet.

6. **Schema-schema is not itself schema-described.** The schema-schema is core Rust per record 807 — but the all-the-way-back claim (record 746) says NOTA itself is schema-derived. The schema-schema's BUILT-IN macros are hand-authored Rust; the question of whether the schema-schema can ALSO be schema-described (in some bootstrap-cut sense) is left open. Likely the same answer as /354's open question 1 — there's a clean cut at the bootstrap kernel, and the schema-schema's macros are on the Rust side of that cut for now.

## Worktrees + branches touched

| Worktree | Branch | Remote | Purpose |
|---|---|---|---|
| `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-schema-prototype-2026-05-26/` | `designer-schema-schema-prototype-2026-05-26` | `origin/designer-schema-schema-prototype-2026-05-26` | The work |

Branch is based on aed752c4's `designer-schema-derived-nota-2026-05-26` (HEAD `0e04c22`). New HEAD on this branch: `cc0c340`. Six files added/modified:

- `prototype/src/block_query.rs` (new, 297 LOC) — refined NOTA library surface
- `prototype/src/schema_schema.rs` (new, 510 LOC) — schema-schema as core Rust + 3 built-in macros
- `prototype/src/bin/schema_schema_demo.rs` (new, 126 LOC) — end-to-end demo
- `prototype/tests/schema_schema_constraints.rs` (new, 360 LOC) — 10 constraint tests
- `prototype/src/lib.rs` (modified) — pub mod + pub use additions for new modules
- `prototype/tests/block_parser_constraints.rs` (modified) — cargo fmt output only, no semantic change

## References

- Spirit records 799-807 (Maximum except 806 Medium) — the directive intent
- `/357` — the design synthesis this implements
- `/354` — the prior prototype foundation (kernel + ThreePartSchema)
- `/355` — the critique with compiled-fixture test methodology (honored in spirit; full three-way verification deferred since this layer doesn't emit Rust code yet)
- aed752c4's `prototype/src/blocks.rs` — the block-by-block parser this work layers on top of
- AGENTS.md hard overrides (NOTA bracket-only, methods-only Rust discipline, qualifies-vs-is distinction)
