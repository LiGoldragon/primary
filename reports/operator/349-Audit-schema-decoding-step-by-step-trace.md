# Operator Audit 349 - Schema Decoding Step-by-Step Trace

Target: how current schema-next decodes terse inline input/output syntax.

This expands report `348` with the concrete "NOTA turns this into this, schema
interprets it as this" trace.

## Example Source

Use this small schema:

```nota
[(Record { Topic * Description * })
 (Select [(ByTopic { Topic * }) (ByKind { Kind * })])
 Version]
[(Recorded { RecordIdentifier * DatabaseMarker * })]
{
  Topic String
  Description String
  Kind [Decision Constraint]
  RecordIdentifier (Bytes 12)
  CommitSequence Integer
  StateDigest (Bytes 8)
  DatabaseMarker { CommitSequence * StateDigest * }
}
```

The intended author read is:

- `Record` is an input operation with an operation-owned payload body.
- `Select` is an input operation whose payload is an operation-owned enum.
- `Version` is a unit input.
- `Recorded` is an output with an operation-owned payload body.
- `Topic`, `Description`, `Kind`, identifiers, and `DatabaseMarker` are reusable
  namespace nouns.

## Step 1 - NOTA Parses Raw Blocks Only

`nota-next::Document::parse` does not know schema. It only sees a document with
three root objects:

```text
root[0] = SquareBracket([...])  // input root vector
root[1] = SquareBracket([...])  // output root vector
root[2] = Brace({...})          // namespace map
```

Inside `root[0]`, NOTA sees three vector members:

```text
input[0] = Parenthesis([
  Atom("Record"),
  Brace([Atom("Topic"), Atom("*"), Atom("Description"), Atom("*")])
])

input[1] = Parenthesis([
  Atom("Select"),
  SquareBracket([
    Parenthesis([Atom("ByTopic"), Brace([Atom("Topic"), Atom("*")])]),
    Parenthesis([Atom("ByKind"), Brace([Atom("Kind"), Atom("*")])])
  ])
])

input[2] = Atom("Version")
```

At this stage, `(Record { ... })` is just a parenthesized block with two
children. `{ Topic * Description * }` is just a brace block with four children.
No `Input`, `Record`, field, enum, or payload meaning exists yet.

## Step 2 - SchemaSource Splits The Document

`SchemaSource::from_document` expects exactly three or four root objects:

- three: `input output namespace`
- four: `imports input output namespace`

For the example:

```text
imports   = SourceImports::empty()
input     = SourceRootEnum(name = Input,  block = root[0])
output    = SourceRootEnum(name = Output, block = root[1])
namespace = SourceNamespace(block = root[2])
```

So the schema reader already knows root position:

- first vector means `Input`
- second vector means `Output`
- brace map means namespace declarations

This is position-defined meaning. NOTA supplied shape; schema supplies role.

## Step 3 - The Input Vector Becomes SourceEnumBody

`SourceRootEnum::from_block` calls `SourceEnumBody::from_block`.

`SourceEnumBody::from_block` requires square brackets and iterates each member:

```text
for block in input_vector_members:
    SourceVariantSignature::from_structural_block(block)
```

This is the key structural macro moment.

## Step 4 - SourceVariantSignature Dispatches By Shape

`SourceVariantSignature` is a typed structural macro node:

```rust
Unit        : PascalCase atom
SelfTagged  : parenthesized PascalCase head, arity 1
Data        : parenthesized PascalCase head, arity 2
Streaming   : parenthesized PascalCase head, arity 4
```

Applied to the example:

```text
Atom("Version")
  -> SourceVariantSignature::Unit(SourceVariantName("Version"))

Parenthesis([Atom("Record"), Brace(...)])
  -> SourceVariantSignature::Data(
       SourceVariantName("Record"),
       SourceVariantPayload::from_structural_block(Brace(...))
     )

Parenthesis([Atom("Select"), SquareBracket(...)])
  -> SourceVariantSignature::Data(
       SourceVariantName("Select"),
       SourceVariantPayload::from_structural_block(SquareBracket(...))
     )
```

The structural macro system does not itself understand schema declarations. It
only chooses the enum variant by shape and passes captured children to the Rust
type's decode logic.

## Step 5 - SourceVariantPayload Tries Reference, Then Declaration

For `Record`, the payload block is:

```nota
{ Topic * Description * }
```

`SourceVariantPayload::from_structural_block` tries:

1. `SourceReference::from_block`
2. if that fails, `SourceDeclarationValue::from_block`

A brace block is not a valid type reference, so step 1 fails. Then
`SourceDeclarationValue::from_block` sees a brace and returns:

```text
SourceVariantPayload::Declaration(
  SourceDeclarationValue::Struct(
    SourceStructBody(fields = [
      SourceField(name = Topic,       value = Derived),
      SourceField(name = Description, value = Derived),
    ])
  )
)
```

The `*` values are `SourceFieldValue::Derived`. A derived field means:

```text
field name = lower_snake_case(type name)
field type = the PascalCase type itself
```

So:

```nota
Topic *
Description *
```

later becomes:

```text
topic: Topic
description: Description
```

For `Select`, the payload block is:

```nota
[(ByTopic { Topic * }) (ByKind { Kind * })]
```

`SourceReference::from_block` fails because square brackets are not type
references. `SourceDeclarationValue::from_block` sees a square bracket and
returns:

```text
SourceVariantPayload::Declaration(
  SourceDeclarationValue::Enum(
    SourceEnumBody(variants = [
      Data(ByTopic, Declaration(Struct({ Topic * }))),
      Data(ByKind,  Declaration(Struct({ Kind * }))),
    ])
  )
)
```

So inline enum payloads use the same path as inline struct payloads. The nested
`ByTopic` and `ByKind` inline bodies are also structural variant signatures.

## Step 6 - Namespace Parses Separately

The namespace brace is parsed as key/value pairs:

```nota
Topic String
Description String
Kind [Decision Constraint]
RecordIdentifier (Bytes 12)
CommitSequence Integer
StateDigest (Bytes 8)
DatabaseMarker { CommitSequence * StateDigest * }
```

Each pair becomes `SourceNamespaceEntry { name, value }`.

Examples:

```text
Topic String
  -> SourceDeclarationValue::Reference(SourceReference::Plain("String"))

Kind [Decision Constraint]
  -> SourceDeclarationValue::Enum(SourceEnumBody(Unit(Decision), Unit(Constraint)))

RecordIdentifier (Bytes 12)
  -> SourceDeclarationValue::Reference(SourceReference::FixedBytes(12))

DatabaseMarker { CommitSequence * StateDigest * }
  -> SourceDeclarationValue::Struct(SourceStructBody(...))
```

## Step 7 - SourceTypeResolver Sees Names Before Lowering

Before producing semantic `Schema`, `SchemaSource::to_schema` builds a
`SourceTypeResolver`.

It contains:

- namespace type names: `Topic`, `Description`, `Kind`, `RecordIdentifier`,
  `CommitSequence`, `StateDigest`, `DatabaseMarker`
- inline input declaration names: `Record`, `Select`
- inline output declaration names: `Recorded`

This matters because a bare unit-looking variant may resolve to a payload if a
same-named declaration exists. It also lets inline declarations refer to names
known elsewhere in the source.

Concrete distinction:

- `Version` stays unit here because no declaration named `Version` exists.
- A bare `Record` root member would become `Record(Record)` once a declaration
  named `Record` exists.
- `(Record)` is the explicit self-tagged form and always means `Record(Record)`.

## Step 8 - Namespace Declarations Lower First

`SourceLoweredNamespace::from_source` lowers the explicit namespace entries:

```text
Topic String
  -> Declaration::public(TypeDeclaration::Newtype(Topic(String)))

Description String
  -> Declaration::public(TypeDeclaration::Newtype(Description(String)))

Kind [Decision Constraint]
  -> Declaration::public(TypeDeclaration::Enum(Kind {
       Decision: None,
       Constraint: None,
     }))

RecordIdentifier (Bytes 12)
  -> Declaration::public(TypeDeclaration::Newtype(RecordIdentifier(FixedBytes(12))))

DatabaseMarker { CommitSequence * StateDigest * }
  -> Declaration::public(TypeDeclaration::Struct(DatabaseMarker {
       commit_sequence: CommitSequence,
       state_digest: StateDigest,
     }))
```

Bare `Name Type` lowers to a newtype, not an alias. That follows Spirit record
`qz6j` (the schema bare-name reference lowers as newtype decision).

One-field brace bodies also lower to newtypes. Two or more fields lower to
structs.

## Step 9 - Root Inline Declarations Are Hoisted

After explicit namespace lowering, `SchemaSource::to_schema` pushes public
inline declarations from input and output roots.

For `Record`:

```text
SourceVariantSignature::Data(
  name = Record,
  payload = Declaration(Struct({ Topic * Description * }))
)
```

public inline declaration lowering produces:

```text
Declaration::public(TypeDeclaration::Struct(Record {
  topic: Topic,
  description: Description,
}))
```

For `Select`:

```text
Declaration::public(TypeDeclaration::Enum(Select {
  ByTopic: ByTopic,
  ByKind: ByKind,
}))
```

Its nested inline variant payloads become private declarations inside the enum's
declaration group:

```text
TypeDeclaration::Newtype(ByTopic(Topic))  // private
TypeDeclaration::Newtype(ByKind(Kind))    // private
```

For `Recorded`:

```text
Declaration::public(TypeDeclaration::Struct(Recorded {
  record_identifier: RecordIdentifier,
  database_marker: DatabaseMarker,
}))
```

This is where inline root payload bodies become real named schema declarations.

## Step 10 - Root Enums Are Assembled

Now schema builds the root enum declarations.

For input:

```text
Input {
  Record:  Some(TypeReference::Plain("Record")),
  Select:  Some(TypeReference::Plain("Select")),
  Version: None,
}
```

For output:

```text
Output {
  Recorded: Some(TypeReference::Plain("Recorded")),
}
```

Notice what happened: the inline body is gone from the root enum. The semantic
schema root only says `Record` carries type `Record`. The body lives in the
namespace declaration named `Record`.

## Step 11 - Semantic Schema Is Typed Data

The final `Schema` contains:

```text
Schema {
  input: EnumDeclaration(Input, variants = ...),
  output: EnumDeclaration(Output, variants = ...),
  namespace: [
    Topic,
    Description,
    Kind,
    RecordIdentifier,
    CommitSequence,
    StateDigest,
    DatabaseMarker,
    Record,
    Select,
    Recorded,
    ...
  ],
  streams: []
}
```

At this point there is no raw text dependency. Rust emission, schema upgrade
logic, symbol paths, source archives, and rkyv round-trips consume typed schema
nouns.

## Step 12 - Rust Emission Sees Only Semantic Types

`schema-rust-next` does not reparse the inline syntax. It receives the typed
semantic `Schema`.

The emitter sees:

```text
TypeDeclaration::Struct(Record { topic: Topic, description: Description })
TypeDeclaration::Enum(Select { ByTopic(ByTopic), ByKind(ByKind) })
TypeDeclaration::Struct(Recorded { record_identifier: RecordIdentifier, ... })
EnumDeclaration(Input { Record(Record), Select(Select), Version })
EnumDeclaration(Output { Recorded(Recorded) })
```

So generated Rust naturally becomes:

```rust
pub struct Record {
    pub topic: Topic,
    pub description: Description,
}

pub enum Input {
    Record(Record),
    Select(Select),
    Version,
}
```

The inline authoring shape is therefore authoring sugar over named schema nouns,
not anonymous Rust payloads.

## Where The Shallow Rule Fits

Current code allows this:

```nota
[(Select [(ByTopic { Topic * }) (ByKind { Kind * })])]
```

and can go deeper if the nested bodies continue using PascalCase inline
declarations. That works mechanically because `SourceVariantPayload` keeps
falling back from reference to declaration.

The psyche's shallow rule should be understood as:

- Inline at the root when the body is the operation-level payload.
- Inline one enum payload if the operation is a small operation-local choice.
- Put nested/reusable structure in the namespace once the root vector starts
  hiding a tree.

Good shallow root:

```nota
[(Record { Topic * Description * })
 (Select { TopicMatch * PrivacySelection * })]
{
  TopicMatch [Any (Full { topics (Vec Topic) })]
  PrivacySelection [Public Private]
}
```

Too deep for root readability:

```nota
[(Select [(ByTopic { Topic * })
          (ByMetadata { Metadata { CreatedBy * CreatedAt * } })])]
```

Better:

```nota
[(Select { Selection * })]
{
  Selection [(ByTopic { Topic * }) (ByMetadata { Metadata * })]
  Metadata { CreatedBy * CreatedAt * }
}
```

## Status

What exists:

- typed source decoding after NOTA parse
- structural macro decoding for enum/root members
- inline struct payloads
- inline enum payloads
- hoisting of root inline declarations to public namespace declarations
- hoisting of nested enum inline declarations to private declarations
- semantic schema as typed data

What is not enforced:

- no maximum inline depth
- no lint that says "this root vector is too deep"
- no automatic style preference that ports tests away from older `(Root Payload)`
  examples

Next useful implementation step before fleet porting: port schema-next and
schema-rust-next tests/fixtures to the shallow inline root style, then decide
whether to add validation/linting for maximum inline depth.
