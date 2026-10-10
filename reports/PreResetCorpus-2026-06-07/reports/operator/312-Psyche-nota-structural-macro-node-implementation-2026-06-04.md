# Operator Psyche Report — NOTA Structural Macro Node Implementation

Date: 2026-06-04

## Executive Read

The operator-side implementation landed on the main branches of both relevant
repositories:

- `nota-next` main commit `35786532` — adds the typed structural macro-node
  codec surface.
- `schema-next` main commit `87991f83` — consumes that surface for authored
  schema enum-variant sugar.

The implemented design is deliberately smaller than a derive macro and larger
than a test-only concept. `nota-next` now exposes the runtime trait that a
future derive macro can generate: an enum-shaped consumer lists structural
variants in source order, NOTA dispatches a parsed `Block` through those
ordered structural patterns, and the matched `MacroMatch` is decoded into the
consumer's Rust value. The same Rust value must encode back to structural NOTA.

`schema-next` now proves the mechanism in real schema source. Authored enum
variant entries such as `Reserved`, `(Record Entry)`, and
`(Inline { Topic * })` are parsed as `SourceVariantSignature` structural macro
nodes. That source value round-trips back to the same `.schema` surface and
then lowers to `Asschema`.

## What Was Implemented

### `nota-next`

Files:

- `/git/github.com/LiGoldragon/nota-next/src/macros.rs`
- `/git/github.com/LiGoldragon/nota-next/src/lib.rs`
- `/git/github.com/LiGoldragon/nota-next/tests/macro_nodes.rs`
- `/git/github.com/LiGoldragon/nota-next/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/nota-next/INTENT.md`

The new reusable surface is:

```rust
pub trait StructuralMacroNode: Sized {
    type Error;

    fn structural_position() -> PositionPredicate;
    fn structural_variants() -> Vec<MacroNodeDefinition>;
    fn from_structural_match(matched: MacroMatch<'_>) -> Result<Self, Self::Error>;
    fn to_structural_nota(&self) -> String;
}
```

The trait also provides `from_structural_block`, `from_structural_pair`, and
`from_structural_candidate`. Those helpers build a `MacroRegistry` from the
consumer's ordered variants, dispatch the raw NOTA structure, and map either
the structural dispatch error or the semantic decode error into
`StructuralMacroError`.

`MacroMatch` also gained capture accessors:

- `capture`
- `block_capture`
- `body_capture`

Those avoid every consumer hand-reaching through the capture map.

The NOTA test witness is intentionally plain:

```text
Input NOTA block:
Reserved

Structural cases:
1. literal Reserved
2. generic PascalCase unit variant
3. parenthesized data variant

Decoded Rust:
ExampleStructuralVariant::Reserved

Encoded NOTA:
Reserved
```

That proves source-order matching matters. `Reserved` also qualifies as
PascalCase, but the literal variant is earlier, so it wins.

The data-carrying witness:

```text
Input NOTA block:
(Record Entry)

Decoded Rust:
ExampleStructuralVariant::Data {
    variant_name: "Record",
    payload_name: "Entry",
}

Encoded NOTA:
(Record Entry)
```

That proves the mechanism is not just a validator. It selects a structural
variant, decodes captures into a typed enum value, emits the structural surface
again, and decodes the emitted surface back to the same value.

### `schema-next`

Files:

- `/git/github.com/LiGoldragon/schema-next/src/source.rs`
- `/git/github.com/LiGoldragon/schema-next/src/engine.rs`
- `/git/github.com/LiGoldragon/schema-next/tests/source_codec.rs`
- `/git/github.com/LiGoldragon/schema-next/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/schema-next/INTENT.md`
- `/git/github.com/LiGoldragon/schema-next/Cargo.lock`

`SourceVariantSignature` now implements `nota_next::StructuralMacroNode`.
It reuses the existing schema-side `EnumVariants` structural cases instead of
creating a third definition:

- `unit variant` — a bare PascalCase atom.
- `data variant` — a parenthesized two-object block containing variant name
  plus payload object.

The live source parser now reads enum bodies from `Block` values, not from the
older `RawNotaDatatype` mirror, so variant sugar is parsed at the structural
NOTA layer before semantic conversion. The namespace and struct source readers
were also moved onto `Block` paths so nested inline declaration payloads reach
the same structural enum parser.

The concrete schema witness:

```text
Input schema source:
{}
[Reserved (Record Entry) (Inline { Topic * })]
[]
{
  Entry { Topic * }
  Topic String
}
```

Typed source interpretation:

```text
Input variants:
Reserved -> unit/header variant
Record   -> reference payload Entry
Inline   -> inline declaration payload { Topic * }
```

Canonical encode-back:

```text
{}
[Reserved (Record Entry) (Inline { Topic * })]
[]
{
  Entry { Topic * }
  Topic String
}
```

Lowered assembled input variants:

```text
Reserved -> no payload
Record   -> payload Entry
Inline   -> payload Inline
```

The inline declaration becomes an exported same-named schema type, so `Inline`
is not a string trick or parser side effect; it is a typed source node that
lowers after structural selection.

Malformed structural input now reports the shared structural diagnostic:

```text
Input schema source:
{}
[(Record Entry Extra)]
[]
{}

Error shape:
UnsupportedMacroNodeStructure {
  position: "EnumVariants",
  expected: ["unit variant: ...", "data variant: ..."],
  found: "parenthesis",
}
```

That is the right failure mode: the object is legal NOTA, but it is not one of
the structural macro cases allowed at the `EnumVariants` position.

## How This Fulfills The Intent

The implementation follows the core intent directly:

- **Structural matching happens first.** `nota-next::MacroRegistry` dispatches
  over a raw parsed `Block` before Schema interprets a variant as unit,
  reference-carrying, or declaration-carrying.
- **Variant order matters.** `StructuralMacroNode::structural_variants` returns
  an ordered vector, and the registry returns the first matching case.
- **Parsing continues after the match.** The matched payload block in
  `schema-next` is recursively parsed by `SourceVariantPayload::from_block`,
  which can read a reference or an inline declaration.
- **The mechanism is bidirectional.** NOTA has `to_structural_nota`, and Schema
  proves the concrete source-level bidirectionality through
  `SchemaSourceArtifact::to_schema_text`.
- **Schema sugar stays inside NOTA.** The schema source file is legal NOTA
  before Schema semantics are applied. The sugar is a position-specific
  structural interpretation of NOTA blocks, not a side language that must first
  lower through text.

This also gives the future derive macro a real target. The derive does not need
to invent matching semantics; it can generate the ordered
`MacroNodeDefinition` list, the `from_structural_match` capture decoder, and
the `to_structural_nota` encoder for a Rust enum.

## Important Boundaries

This slice does not remove `Asschema`. That is intentional. The current stack
still uses `Asschema` as the typed macro-free endpoint for tests, storage,
symbol paths, and Rust emission. The implemented change proves that authored
schema sugar can be decoded and encoded as specialized NOTA before assembly.
Removing or replacing `Asschema` should be a separate design and migration
slice, after the new structural source path has more coverage than enum
variants.

This slice does not emit a derive macro. It creates the trait surface that a
derive macro should target. That keeps the semantics inspectable before hiding
them behind proc-macro output.

This slice does not route every schema macro handler through typed structural
nodes. It routes authored `SchemaSource` enum bodies first because that is the
place where the psyche's structural enum explanation is most direct. Namespace
declarations, struct fields, root sections, and type-reference macro calls
still have their existing registry/handler paths. Those can now migrate toward
the same typed structural-node pattern case by case.

This slice keeps `RawSchemaFile` and `SyntaxSchema` alive. They still serve
lower-level inspection and compatibility tests. The duplicated raw helpers
inside the authored source parser were removed because the live source path now
needs block-level structure.

## Verification

`nota-next`:

- `cargo test`
- `cargo clippy -- -D warnings`

`schema-next`:

- `cargo test --test source_codec`
- `cargo test`
- `cargo clippy -- -D warnings`

All passed.

## Intent Log Audit

The forwarded prompt rule applied here. The originally addressed side had
already captured the durable intent in Spirit:

- `ejvc` — NOTA needs structural macro nodes matched by structure, in
  declaration order, with recursive decode and bidirectional encode.
- `lcwu` — Schema is a specialized NOTA dialect built on structural macro
  nodes, not a separate language lowered into NOTA.

The operator subagent accidentally added a duplicate record, `24ds`, at
maximum certainty. I removed it with `spirit "(Remove [24ds])"` because it was
not a gap-fill and the original capture already covered the content.

## Next Correct Moves

1. Add a `nota-next-derive` structural macro-node derive that targets
   `StructuralMacroNode`. The derive should be boring: generate ordered cases,
   matched-capture decoding, and encode-back.
2. Move additional Schema positions onto typed structural nodes, starting with
   namespace declaration and struct field values. The structural case lists
   already exist; the missing piece is typed consumer objects like
   `SourceVariantSignature`.
3. Decide the staged fate of `Asschema`. The operator recommendation is not to
   delete it immediately. First expand bidirectional `SchemaSource` coverage
   and identify which downstream jobs still need a macro-free typed endpoint.
4. Add an ambiguity/lint policy for overlapping structural cases. The current
   implementation intentionally uses source order and catches exact duplicate
   patterns through the existing registry conflict check, but it does not yet
   explain broader overlaps.
5. Keep reports showing "schema text in, typed source value, encoded text out,
   assembled value out" for every new sugar mechanism. This is the most useful
   way to keep Schema understandable from above, below, inside, and outside.
