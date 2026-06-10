# Operator Audit 349 - Schema Decoding Step-by-Step Trace

Target: how current schema-next decodes terse inline input/output syntax, plus
the next source-scope rule implied by the edited example.

This expands report `348` with the concrete "NOTA turns this into this, schema
interprets it as this" trace.

Status note: the example below now expresses the desired next model: root inline
payload fields can declare reusable schema types, and later source positions can
refer to those types. Current `schema-next` partially supports the lowering, but
keeps those field-created declarations private and does not yet treat them as
first-class source-scope names during initial resolver construction.

## Example Source

Use this small schema:

```nota
[(Record { Topic String Description String })
 (Select [(ByTopic { Topic * }) (ByKind { Kind * })])
 Version]
[(Recorded { RecordIdentifier (Bytes 12) DatabaseMarker * })]
{
  Kind [Decision Constraint]
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
  Brace([Atom("Topic"), Atom("String"), Atom("Description"), Atom("String")])
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
children. `{ Topic String Description String }` is just a brace block with four
children. No `Input`, `Record`, field, enum, or payload meaning exists yet.

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
{ Topic String Description String }
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
      SourceField(name = Topic,       value = Reference(String)),
      SourceField(name = Description, value = Reference(String)),
    ])
  )
)
```

The interesting part is that `Topic String` is both a field and an inline type
declaration because the field name is PascalCase. Current code already has this
rule in `SourceField::to_lowered_field`:

```text
PascalCase field name + reference value
  -> private TypeDeclaration::Newtype(Topic(String))
  -> field topic: Topic
```

So the intended read is:

```nota
Topic String
Description String
```

later becomes:

```text
type Topic = newtype String
type Description = newtype String
topic: Topic
description: Description
```

The proposed production change is visibility and scope: those declarations
should be source-scope/exported declarations, not only private declarations
attached to the `Record` declaration group.

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
Kind [Decision Constraint]
CommitSequence Integer
StateDigest (Bytes 8)
DatabaseMarker { CommitSequence * StateDigest * }
```

Each pair becomes `SourceNamespaceEntry { name, value }`.

Examples:

```text
Kind [Decision Constraint]
  -> SourceDeclarationValue::Enum(SourceEnumBody(Unit(Decision), Unit(Constraint)))

DatabaseMarker { CommitSequence * StateDigest * }
  -> SourceDeclarationValue::Struct(SourceStructBody(...))
```

In the edited model, `Topic`, `Description`, and `RecordIdentifier` are absent
from this trailing namespace because they are declared inline at their first
semantic use. They still need to enter the final namespace/export surface.

## Step 7 - SourceTypeResolver Sees Names Before Lowering

Before producing semantic `Schema`, `SchemaSource::to_schema` builds a
`SourceTypeResolver`.

It contains:

- namespace type names: `Kind`, `CommitSequence`, `StateDigest`,
  `DatabaseMarker`
- inline input declaration names: `Record`, `Select`
- inline output declaration names: `Recorded`

This matters because a bare unit-looking variant may resolve to a payload if a
same-named declaration exists. It also lets inline declarations refer to names
known elsewhere in the source.

Current gap: this resolver does not collect field-created inline declaration
names such as `Topic`, `Description`, or `RecordIdentifier`. The lowering path
can still create those declarations, and ordinary field references can still
point at them, but same-name root variant resolution and deliberate library
export semantics do not yet treat them as source-scope declarations.

The intended resolver should collect all declarations first:

```text
explicit namespace names
+ root inline payload names
+ root inline field-declaration names
+ output inline field-declaration names
+ selected nested names that are meant to be exported
```

Then every reference lowers against that fixed source table.

Concrete distinction:

- `Version` stays unit here because no declaration named `Version` exists.
- A bare `Record` root member would become `Record(Record)` once a declaration
  named `Record` exists.
- `(Record)` is the explicit self-tagged form and always means `Record(Record)`.

## Step 8 - Namespace Declarations Lower First

`SourceLoweredNamespace::from_source` lowers the explicit namespace entries:

```text
Kind [Decision Constraint]
  -> Declaration::public(TypeDeclaration::Enum(Kind {
       Decision: None,
       Constraint: None,
     }))

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
  payload = Declaration(Struct({ Topic String Description String }))
)
```

Current lowering produces:

```text
Declaration::private(TypeDeclaration::Newtype(Topic(String)))
Declaration::private(TypeDeclaration::Newtype(Description(String)))
Declaration::public(TypeDeclaration::Struct(Record {
  topic: Topic,
  description: Description,
}))
```

Desired lowering changes the two field-created declarations to exported
source-scope declarations:

```text
Declaration::public(TypeDeclaration::Newtype(Topic(String)))
Declaration::public(TypeDeclaration::Newtype(Description(String)))
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

`ByTopic { Topic * }` should resolve `Topic` to the same source-scope
declaration created by `Record { Topic String ... }`. This should not be an
order-dependent "previous inline wins" rule; it should be a whole-source symbol
table with one unique declaration named `Topic`.

For `Recorded`:

```text
Declaration::public(TypeDeclaration::Newtype(RecordIdentifier(FixedBytes(12))))
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
[(Record { Topic String Description String })
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
- PascalCase fields with explicit references, such as `Topic String`, lowering
  into a named newtype plus a field reference
- semantic schema as typed data

What is not enforced:

- no maximum inline depth
- no lint that says "this root vector is too deep"
- no automatic style preference that ports tests away from older `(Root Payload)`
  examples
- no source-scope collection/export policy for field-created inline
  declarations such as `Topic String`
- no duplicate-name rule for the case where inline and trailing namespace both
  declare `Topic`

Next useful implementation step before fleet porting: make source lowering build
a whole-source declaration table, promote root payload field declarations that
are intended as reusable nouns to the exported namespace, reject duplicate
declarations by name, then port schema-next and schema-rust-next tests/fixtures
to this shallow inline root style.
