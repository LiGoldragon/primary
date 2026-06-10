# Operator Audit 348 — How Schema Structural Macro Decoding Works

Target: current `nota-next` + `schema-next` schema decoding model.

Spirit context: record `yntp` says schema input/output inline declarations
should stay shallow: root payload bodies can be inline, while deeper reusable or
nested structure should move into named namespace types.

## Short Answer

Schema decoding is typed after the first NOTA parse. NOTA parses only raw
objects: atoms, parentheses, brackets, braces, and pipe forms. Then schema-next
interprets those raw blocks at known positions. At enum/root-variant positions,
schema-next uses `nota-next::StructuralMacroNode` to choose a typed variant shape
from the raw block.

For input/output roots, the path is:

1. `nota-next::Document::parse` turns text into raw `Block` objects.
2. `SchemaSource::from_document` expects three or four root objects: optional
   imports, input root vector, output root vector, namespace map.
3. `SourceRootEnum::from_block` reads the input/output vector.
4. `SourceEnumBody::from_blocks` iterates each vector member.
5. Each member is decoded as `SourceVariantSignature` through
   `StructuralMacroNode`.
6. Inline payload bodies become real declarations named after the variant and
   are hoisted into the schema namespace before the root enum is assembled.

So `[(Record { Topic * Description * })]` becomes:

- root enum variant: `Record(Record)`
- public namespace declaration: `Record { Topic * Description * }`

## The Two Macro Systems

There are two related but distinct systems:

### `nota-next::StructuralMacroNode`

This is typed structural decoding for one object. A type says, "at this position,
these shapes are valid." `SourceVariantSignature` uses this.

Current source:

```rust
pub enum SourceVariantSignature {
    #[shape(pascal_atom)]
    Unit(SourceVariantName),
    #[shape(pascal_head, arity = 1)]
    SelfTagged(SourceVariantName),
    #[shape(pascal_head, arity = 2)]
    Data(SourceVariantName, SourceVariantPayload),
    #[shape(pascal_head, arity = 4)]
    Streaming(SourceVariantName, SourceVariantPayload, StreamRelationKeyword, SourceVariantName),
}
```

The derive expands this into a list of `StructuralVariant` match patterns. At
runtime, `from_structural_block` wraps the raw `Block` in a `MacroCandidate` and
dispatches against the pattern list. The first matching structural variant wins.

This is how schema recognizes:

- `Record` as a unit variant.
- `(Record)` as a self-tagged variant whose payload is `Record`.
- `(Record Entry)` as a data variant whose payload is reference `Entry`.
- `(Record { Topic * Description * })` as a data variant whose payload is an
  inline declaration.
- `(Subscribe Query opens RecordStream)` as a streaming relation variant.

### `schema-next::MacroRegistry`

This is the broader schema macro registry for positions such as imports,
namespace declarations, struct fields, enum variants, and type references. It
can dispatch `MacroObject::Block` or `MacroObject::Pair` through
`SchemaMacroHandler`. It is the older/larger schema-position macro layer and
also exposes node definitions for introspection.

The current input/output inline variant path primarily rides the typed
`StructuralMacroNode` path, not an arbitrary runtime macro expansion.

## Inline Payload Decoding

`SourceVariantSignature::Data` carries a `SourceVariantPayload`.

`SourceVariantPayload::from_structural_block` tries two interpretations:

1. `SourceReference::from_block(block)` — a payload reference such as `Entry`,
   `(Vec Entry)`, `(Map (Key Value))`, `Bytes`, or `(Bytes 32)`.
2. If that fails, `SourceDeclarationValue::from_block(block)` — an inline
   declaration body such as `{ Topic * Description * }` or `[ByTopic ByKind]`.

That fallback is why inline struct and inline enum payloads work:

```nota
[(Record { Topic * Description * })]
[(Select [(ByTopic { Topic * }) (ByKind { Kind * })])]
```

The inline body is not kept as anonymous payload syntax. Schema gives it a name:
the variant name. So the examples become declarations named `Record` and
`Select`, and the root variants carry those named types.

## Hoisting And Visibility

Inline declarations are hoisted differently depending on where they appear:

- Inline declarations in root input/output vectors become public namespace
  declarations. They are part of the wire surface.
- Inline declarations inside a namespace enum become private declarations used
  by that enum.

This matters for "do not go too deep." The mechanism currently allows nested
inline shapes, because an inline enum body can contain variants whose payloads
are themselves inline declarations. The parser is capable of deeper trees; the
style rule needs to constrain authors.

The shallow style should be:

```nota
[(Record { Topic * Description * })
 (Observe { TopicMatch * })
 Version]
{
  Topic String
  Description String
  TopicMatch [(Any) (Full { topics (Vec Topic) })]
}
```

And for deeper structure:

```nota
[(Record { Entry * })
 (Observe { Query * })]
{
  Entry { Topic * Description * Metadata * }
  Query { TopicMatch * PrivacySelection * }
  Metadata { CreatedBy * CreatedAt * }
}
```

The exact threshold is design policy, not parser policy. Current code does not
enforce "one inline layer only."

## Current Fit Against Psyche Intent

What works properly:

- Input/output roots can define operation-owned payload bodies inline.
- Inline enum payloads work through the same `SourceVariantPayload` path as
  inline struct payloads.
- The schema is typed after parsing: `SchemaSource`, `SourceRootEnum`,
  `SourceEnumBody`, `SourceVariantSignature`, `SourceVariantPayload`,
  `SourceDeclarationValue`, and `SourceReference` are real Rust nouns.
- The source value round-trips: it can write canonical schema text and archive
  through rkyv.

What may not match the intended authoring discipline:

- Current parser accepts deeper nested inline declaration trees. It does not
  enforce "root inline only one level deep."
- Current docs still have alias-era drift. Code says aliases are gone; docs must
  be corrected before broad porting.
- Existing tests and fixtures still demonstrate old direct payload root forms in
  many places. Tests should be ported to the inline root-payload style where the
  operation owns the payload body.

## Porting Implication

Before porting all consumer schemas, port the schema-next/schema-rust-next tests
first to teach the desired style:

- Replace root-level `(Record Entry)` examples with
  `(Record { ... })` when `Record` owns that operation payload body.
- Keep `(Record Entry)` when `Entry` is a reusable domain noun and `Record` is
  only routing it.
- Use inline enum payloads for operation-local closed choices.
- Move nested reusable shapes into namespace declarations instead of burying
  them in root vectors.

Then, if the psyche wants enforcement rather than convention, add a validation
pass: root inline declarations may contain references and scalar fields, but
nested inline declarations beyond one level are rejected with a specific schema
error.

## Sources

- Spirit record `yntp` — shallow inline input/output declaration constraint.
- `/git/github.com/LiGoldragon/nota-next/src/macros.rs`
- `/git/github.com/LiGoldragon/nota-next/tests/macro_nodes.rs`
- `/git/github.com/LiGoldragon/schema-next/src/source.rs`
- `/git/github.com/LiGoldragon/schema-next/src/engine.rs`
- `/git/github.com/LiGoldragon/schema-next/src/macros.rs`
- `/git/github.com/LiGoldragon/schema-next/src/schema.rs`
