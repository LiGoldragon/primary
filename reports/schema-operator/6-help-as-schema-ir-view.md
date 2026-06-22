# Help as a schema IR view

Role: schema-operator
Date: 2026-06-22

## Research question

Can Help use the same representation as the intermediate representation
on the way to Rust lowering?

Short answer: **yes, Help should be a view over the same schema IR.**

The current separate Help data model is mostly a mirror of
`schema-next`'s source/lowered schema values. It exists because the first
pilot needed a typed rkyv value quickly, but the shape now points to a
cleaner model: Help is not a new language. Help is a query against the
contract's schema IR.

## Existing IRs

There are three related representations in the current branches.

### Source schema IR

`schema-next` owns the source-level typed declaration values:

```text
SourceDeclaration
SourceDeclarationValue
SourceReference
SourceField
SourceVariantSignature
```

This is what `SchemaSource::from_schema_text` decodes from `.schema`
source. It preserves source-level constructs such as root declarations,
inline declarations, stream/family forms, imports, and declaration text
shape.

This is the right direct substrate for Help because Help asks:

```text
What does this contract say may exist at this named type/root?
```

### Lowered schema IR

`schema-next` also lowers to Rust-independent semantic schema values:

```text
TypeDeclaration::{Struct, Enum, Newtype}
StructDeclaration { name, fields }
EnumDeclaration { name, variants }
NewtypeDeclaration { name, reference }
TypeReference::{Plain, Vector, Optional, Map, ScopeOf, Application, ...}
```

`schema-rust-next` lowers this into Rust-specific IR:

```text
RustTypeDeclaration::{Struct, Enum, Newtype}
RustStruct
RustEnum
RustNewtype
RustField
RustEnumVariant
```

The Rust IR mostly clones `TypeReference` and attaches emission-specific
facts. For example, `TypeReference::Vector(T)` becomes Rust `Vec<T>` in
`RustTypeReferenceTokens`.

This confirms the core claim: the generator already has a typed, semantic
"what this thing is" representation. Help should not reproduce that
representation in `signal-spirit`.

### Per-instance trace IR

`nota-next`'s `NotaDecodeTraced` branch adds:

```text
InstanceSchema { expected, provenance, body }
InstanceSchemaBody::{
  Scalar,
  Newtype,
  Struct,
  EnumPayload,
  Vector,
  Optional,
  Map,
}
```

This is not the same as contract schema IR. It is a realized value trace:
actual vector elements, actual optional presence, actual enum payload,
actual map entries. It must be separate because it answers a different
question:

```text
What type did the decoder expect at each actual position in this value?
```

But its references should project into the same schema reference
vocabulary before text emission. That is exactly what the designer branch
does with:

```text
nota_next::TypeReference -> schema_next::SourceReference -> schema encoder
```

## What this says about Help

The current `signal-spirit` Help model contains:

```text
HelpBody::{Unit, Reference, Struct, Enumeration, Text}
HelpTypeExpression::{Name, Vector, Optional, ScopeOf, Map, Application, ...}
```

That is basically a local duplicate of:

```text
SourceDeclarationValue::{Reference, Struct, Enum, Text, Stream, Family}
SourceReference::{Plain, Vector, Optional, ScopeOf, Map, Application, ...}
```

The duplication is where the `Vec`/`Vector` smell escaped. Help has its
own `HelpTypeExpression` layer and can carry a source `Application(Vec,
Domain)` as if it were a valid help reference. The durable shape is to
remove that parallel representation.

## Vision

The schema stack should have one contract/type IR and two consumers:

```text
schema text
  -> schema-next source decoder
  -> SourceDeclaration / SourceReference
  -> schema-next lowering
  -> TypeDeclaration / TypeReference
      -> schema-rust-next Rust IR
      -> Help view
```

For Help specifically:

```text
HelpModel
  holds a SchemaSource or HelpIndex over SourceDeclaration values

HelpQuery
  selects one root/type name

HelpResponse
  is SourceDeclarations or a thin newtype over SourceDeclarations

text
  is SourceDeclarations::to_schema_text()

decode
  is SourceDeclarations::from_schema_text()
```

The Help-specific value can still exist for rkyv and API clarity, but it
should be a wrapper around schema IR, not a parallel AST:

```text
HelpResponse {
  declarations: SourceDeclarations
}
```

or, if single-entry ergonomics matter:

```text
HelpEntry {
  declaration: SourceDeclaration
}
```

Then `(Help Domains)` is literally a re-headed schema declaration:

```schema
(Domains (Vector Domain))
```

and its internal value is literally:

```text
SourceDeclaration {
  name: Domains,
  value: SourceDeclarationValue::Reference(
    SourceReference::Vector(SourceReference::Plain(Domain))
  )
}
```

No `HelpTypeExpression`. No `HelpBody::Reference`. No local container
spelling. No separate schema codec.

## Why not use Rust IR for Help?

Use schema IR, not `schema-rust-next` Rust IR.

The Rust IR is downstream and emission-specific. It knows facts like
"render vector as `Vec<T>`", route helpers, constructors, derives, actor
planes, and generated Rust module choices. Help is not asking for Rust.
It is asking for schema.

So the common representation should be:

```text
schema-next SourceDeclaration / TypeDeclaration
```

not:

```text
schema-rust-next RustDeclaration
```

`schema-rust-next` and Help should be sibling consumers of schema IR, not
one layered through the other.

## Where source IR versus lowered IR matters

For Help, source IR is usually enough and sometimes better:

- it has roots (`Input`, `Output`) in source terms
- it has stream/family source forms
- it can represent a one-level declaration exactly
- it can encode/decode with the schema text codec

Lowered `TypeDeclaration` is useful when Help needs resolved semantic
truth:

- imported names resolved
- aliases normalized
- built-in container heads canonicalized
- generic applications arity-checked

The clean model is therefore:

```text
HelpIndex = source declaration table + lowered semantic table
```

The response should still be a `SourceDeclaration`, but its references
should be normalized from the semantic table when the source spelling is
ambiguous or legacy.

This is exactly where `Vec` failed. A good Help index should not preserve
`SourceReference::Application(Vec, [Domain])` if lowering says that
position is the vector container. The query response should come from the
semantic declaration:

```text
TypeReference::Vector(Domain) -> SourceReference::Vector(Domain)
```

then encode through the schema codec.

## Consequences

1. Help data should move from `signal-spirit` custom AST to
   `schema-next` schema IR wrappers.
2. `HelpResponse::to_schema_text` and `from_schema_text` should become
   direct schema IR codec calls.
3. `schema-next` needs a public normalization path:

```text
TypeDeclaration / TypeReference -> SourceDeclaration / SourceReference
```

4. The canonical container spelling becomes impossible to fork: one
   `SourceReference` encoder emits it for Help, instance-schema, source
   round-trips, and tests.
5. Per-instance schema remains a trace IR, but every reference token in
   it must resolve through the same schema reference encoder.

## Operator recommendation

Collapse Help onto schema IR before broadening beyond Spirit.

The durable implementation target is:

```text
schema-next:
  HelpIndex or declaration projection APIs over SchemaSource/Schema
  SourceReference <-> TypeReference normalization

signal-spirit:
  no custom HelpBody/HelpTypeExpression AST
  thin accessor: HelpModel::from_signal_schema_source()
  response wraps SourceDeclarations / SourceDeclaration

schema-rust-next:
  emits traced decoding for per-instance schema
  does not own Help's representation
```

This makes the phrase "pure information on what a thing is" literal:
the contract schema IR is the one typed information object. Rust
generation, Help, and instance-schema rendering are projections from it,
not separate languages with separate spelling rules.
