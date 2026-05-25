# Implementation

## nota-codec Branch

Branch pushed:

- `feature/notavalue-shape-logic-and-sequence-parser`

Commits:

- `a7aa75b6` — `nota-codec: expand structural shape helpers for schema macros`
- `bb5a55ab` — `nota-codec: make flake source remote-builder safe`
- `d00fbf53` — `nota-codec: exclude target artifacts from flake source`

The branch was rebased onto `nota-codec` main commit `6a851eb6` so it
preserves `ByteRange`, `Lexer::next_token_with_span`, `parse_str`,
and the span tests that landed on main before this pass.

Implemented:

- `NotaValueKind`
- `NotaRecordShape`
- `NotaSequenceShape`
- `NotaMapShape`
- `parse_sequence(input) -> Vec<NotaValue>` for multi-top-level NOTA documents such as `.schema`
- predicate aliases matching the schema macro vocabulary:
  - `is_identifier`
  - `is_pascal_case_identifier`
  - `record_arity`
  - `record_head_value`
  - `record_head_identifier`
  - `is_single_ident_record`
  - `is_tagged_record`

The flake fix matters: the previous Nix source filter accidentally let generated `target/tests/trybuild/.../Cargo.toml` artifacts into the source. Those files carried absolute `/home/li/...` paths, which broke remote builder checks. The flake now excludes `target/` explicitly.

## schema Branch

Branch pushed:

- `feature/fully-schema-and-nota-mvp`

Commit:

- `7100fd4a` — `schema: drive reader and multi-pass pipeline from NotaValue shapes`

The final commit updates `Cargo.lock` to the rebased `nota-codec`
commit `d00fbf53`.

Implemented:

- `Schema::parse_str` now uses `nota_codec::parse_sequence` and `NotaValue` traversal as the canonical parser path.
- The old streaming decoder parser remains as `Schema::parse_str_with_streaming_decoder` for comparison witnesses.
- New `src/shape_parser.rs` maps generic NOTA shapes into `Schema`:
  - six top-level schema positions
  - imports
  - ordinary / owner / sema headers
  - namespace enum / record / newtype / alias declarations
  - field-name overrides
  - container expressions
  - Reply / Event / Observable / Upgrade features
- New `src/multi_pass.rs` implements an MVP macro pipeline:
  - Pass 1: `parse_sequence`
  - Pass 2: six-position structural document
  - Pass 3/4: builtin shape dispatch for Import, Header, Type, Feature, Upgrade
  - Pass 5: `LoweringContext::finish()`

## What This Proves

The implementation now proves two different claims:

1. The production schema parser can be driven from the reusable NOTA shape tree, not a schema-private streaming walker.
2. Builtin schema macros can be represented as `NotaValue` recognizers using shape predicates and lowered through the existing `BuiltinMacroVariant` / `LoweringContext` engine.

This is not yet full fixed-point user macro expansion, and it does not yet emit `VersionProjection` Rust. It is the working substrate those pieces can use.

## Code Shape

The new NOTA layer exposes generic tree facts, not schema semantics:

```rust
pub enum NotaValueKind {
    Record,
    Sequence,
    Map,
    Identifier,
    InlineString,
    BlockString,
    Bytes,
    Integer,
    UnsignedInteger,
    Float,
    Date,
    Time,
}

impl NotaValue {
    pub fn kind(&self) -> NotaValueKind { ... }
    pub fn as_record_shape(&self) -> Option<NotaRecordShape<'_>> { ... }
    pub fn is_single_ident_record(&self) -> bool { ... }
    pub fn is_tagged_record(&self, expected_head: &str) -> bool { ... }
}
```

The schema layer then matches those generic facts against schema-owned
positions:

```rust
pub fn read_schema_six_position(text: &str) -> Result<AssembledSchema> {
    let raw_values = parse_sequence(text).map_err(|error| Error::InvalidSchemaText {
        context: "multi_pass parse_sequence",
        message: error.to_string(),
    })?;
    let document = Document::from_six_values(raw_values)?;
    let mut pipeline = MacroPipeline::new(&document);
    pipeline.run()
}
```

The core relationship is therefore not "stringly parse schema." It is
`NotaValueKind` / shape facts matched against schema node-definition
points, then lowered into `BuiltinMacroVariant`.
