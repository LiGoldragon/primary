# Primary-8vzk Pipe Declarations And Fixture Tests

Bead: `primary-8vzk` — implement consolidated NOTA/Schema spec from designer reports 421/422/423 and records 1137/1152/1155/1176/1178, plus gap-fill record 1179.

## Implemented

The pass landed the current syntax boundary across the three active next-stack repos:

```mermaid
flowchart LR
  A[nota-next] --> B[schema-next]
  B --> C[schema-rust-next]
  A -. parses .schema/.nota .-> A
  B -. lowers pipe declarations .-> B
  C -. emits Rust from Asschema .-> C
```

`nota-next` now parses compact nested recursive pipe delimiters. This matters because schema macro expansion re-emits compact NOTA fragments like `{|Receipt ...|}`; the raw parser must see `|}` as a delimiter close even when there is no separating whitespace.

`schema-next` now treats authored datatype declarations as pipe-family forms:

```schema
{
  Entry {| Entry topic Topic kind Kind description Description |}
  Kind (| Kind Decision Correction Clarification |)
}
```

Plain `[]` and `()` are still legal NOTA data, but `SyntaxSchema` now rejects plain square-bracket datatype declarations at the authored schema layer. The active syntax-layer test uses a real `.schema` fixture and adds an explicit rejection case for `{ Text [String] }`.

Inline pipe declarations at reference positions now lower into ordered `Asschema.namespace` data:

```schema
() ()
{
  Entry {| Entry receipt {| Receipt recordIdentifier RecordIdentifier |} later Receipt |}
}
```

That lowers as `Receipt` first, then `Entry`, with both `receipt` and `later` pointing at `Plain(Receipt)`.

`schema-rust-next` now consumes the same syntax in all real schema fixtures. It also gained file-backed NOTA fixtures and a shared test helper (`tests/support/mod.rs`) so meaningful schema/NOTA inputs live as files instead of hidden Rust string bodies.

## Real Test Surfaces

Representative load-bearing tests now include:

- `schema-next/tests/lowering.rs::inline_pipe_declaration_creates_ordered_namespace_type`
- `schema-next/tests/syntax_layer.rs::plain_square_bracket_datatype_declarations_are_rejected`
- `schema-rust-next/tests/emission.rs::emits_schema_plane_engine_traits_for_declared_nexus_and_sema_languages`
- `schema-rust-next/tests/big_emission.rs::compiled_large_spirit_generated_rust_parses_frames_and_dispatches_mail`

The Rust-emission tests load real files:

```rust
let asschema = FixtureSchema::new("plane-triad.schema").lower("spirit:lib");
let input = FixtureNota::new("nota/record-schema-objects-behavior.nota")
    .read()
    .parse::<generated::Input>()
    .expect("parse generated input");
```

That keeps the actual language examples in:

- `tests/fixtures/plane-triad.schema`
- `tests/fixtures/spirit-min.schema`
- `tests/fixtures/collections.schema`
- `tests/fixtures/big-schemas/*.schema`
- `tests/fixtures/nota/*.nota`

## Commits

- `nota-next`: `bca1af83` — `nota: parse compact nested pipe delimiters`
- `schema-next`: `3230b50b` — `schema: make pipe declarations load-bearing`
- `schema-rust-next`: `5dd44847` — `schema-rust: consume pipe schema fixtures`

All three are on `main` and pushed.

## Verification

Passed:

- `nota-next`: `cargo test`
- `schema-next`: `cargo test`
- `schema-next`: `nix flake check`
- `schema-rust-next`: `cargo test`
- `schema-rust-next`: `nix flake check`

The first `schema-rust-next` Nix run exposed a real fixture-filter gap: `.nota` files were not included in the cleaned Nix source. I fixed the flake source filter to include `.nota`, then reran `nix flake check` successfully.

## Remaining Gaps

Step 1 of bead `primary-8vzk` is not complete yet: `nota-next` still does not own the shared `NotaEncode`/`NotaDecode` derive layer. Current Rust emission still emits per-file codec code over `nota_next::Block`. That is the next major implementation slice.

The `schema-next` raw-core fixtures intentionally still preserve raw NOTA forms such as `Text [String]` because that layer proves raw delimiter preservation before schema semantics. Those are not authored-schema syntax examples.

