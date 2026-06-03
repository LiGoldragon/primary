---
variant: Psyche
topics: [schema, nota, codec, representation, asschema]
date: 2026-06-03
lane: operator
---

# Schema Representation With Its Own Codec

## The Point

[Schema source representation should become its own typed value with a
dedicated in/out codec. The codec reads strict NOTA/schema source into
source-node data and writes it back canonically, separate from raw NOTA parsing
and separate from assembled Asschema serialization. This gives schema syntax a
real data representation before lowering.]

The system needs three distinct values:

```text
NOTA document -> SchemaSource -> Asschema -> RustModule
```

Each value has its own job:

```text
NOTA document  raw delimiters and atoms
SchemaSource   authored schema meaning, still with source sugar
Asschema       macro-free assembled type program
RustModule     Rust emission data before rendered source text
```

The important correction is that `SchemaSource` is not just "halfway parsed
Asschema." It is its own language object. Its codec is the thing that makes
`.schema` readable, writable, canonical, and testable before the assembled
form exists.

## Why This Layer Exists

The current stack already proves the need:

```text
src/raw.rs          RawSchemaFile / RawNotaDatatype
src/syntax.rs       SyntaxSchema / SyntaxDeclaration / SyntaxReference
src/declarative.rs  macro expansion and assembled template lowering
src/asschema.rs     Asschema / Declaration / TypeDeclaration
```

That is a reasonable bootstrap, but it splits one idea across several files:

- raw NOTA keeps delimiter truth;
- syntax reading knows some schema-source meaning;
- declarative lowering knows macro position and shorthand behavior;
- asschema owns the final macro-free program.

The design gap is that no single typed object owns "what a `.schema` file
means before it is assembled."

## The Source Value

The source representation should look conceptually like this:

```rust
pub struct SchemaSource {
    imports: SourceImports,
    input: SourceRootEnum,
    output: SourceRootEnum,
    namespace: SourceNamespace,
}

pub enum SourceDeclarationValue {
    Struct(SourceStructBody),
    Enum(SourceEnumBody),
    Reference(SourceReference),
    Macro(SourceMacroInvocation),
}
```

The source model keeps the sugar because the sugar is real information at this
layer:

```rust
pub enum SourceField {
    Explicit { field_name: Name, reference: SourceReference },
    Derived { type_name: Name },
    InlineType { type_name: Name, value: SourceDeclarationValue },
    AnonymousReference { reference: SourceReference },
}
```

That last distinction matters. Once the system lowers everything to
`FieldDeclaration { name, reference }`, it can be hard to tell whether the user
wrote:

```nota
Topic *
topic Topic
(Vec Topic)
```

Those are semantically close after lowering, but not the same source node.
The source codec should preserve that difference until the source-to-asschema
lowering step decides what it means.

## The In Codec

The input codec reads `.schema` source into `SchemaSource`:

```text
Document::parse(source)
  -> raw body objects
  -> SchemaSourceCodec::decode_document_body
  -> SchemaSource
```

It is not the same as `Asschema::from_nota_source`.

`Asschema` reads known-root assembled schema:

```nota
(schema-next:core [0.1.0])
[]
[]
[]
[]
[(Public CoreSchema ...)]
```

`SchemaSource` reads authored source:

```nota
[]
[]
{
  Topic String
  Topics (Vec Topic)
  Entry { Topics * Description * }
  Output [(RecordAccepted SemaReceipt) Rejected]
}
```

The `.schema` codec has positional knowledge:

- root object 0 is imports;
- root object 1 is input enum body;
- root object 2 is output enum body;
- root object 3 is namespace;
- namespace brace entries are `Name Value` pairs;
- struct brace entries are field nodes;
- enum brackets are variant signature nodes;
- references are atom or parenthesized type-reference nodes.

That is schema-source decoding, not raw NOTA decoding and not asschema
decoding.

## The Out Codec

The output codec writes `SchemaSource` back to canonical `.schema`.

This is the missing half.

The canonical writer decides formatting and sugar in one place:

```nota
Topic String
Topics (Vec Topic)
Entry { Topics * Description * }
Output [(RecordAccepted SemaReceipt) Rejected]
```

Not:

```nota
Topic String
Topics { values (Vec Topic) }
Entry { topics Topics description Description }
Output [RecordAccepted@ SemaReceipt Rejected]
```

The output codec is what prevents every emitter, formatter, report, and test
from inventing its own schema notation. It is also where a future formatter
comes from: formatter = `SchemaSource` output codec with layout policy.

## Source To Asschema

Lowering becomes a separate method on the source value:

```rust
impl SchemaSource {
    pub fn assemble(
        &self,
        identity: SchemaIdentity,
        registry: &MacroRegistry,
    ) -> Result<Asschema, SchemaError> {
        // source nodes -> macro-free declarations
    }
}
```

That is where the recent newtype rule belongs:

```text
SourceStructBody with one resolved field -> TypeDeclaration::Newtype
SourceStructBody with many fields        -> TypeDeclaration::Struct
SourceEnumBody                           -> TypeDeclaration::Enum
SourceReference                          -> TypeDeclaration::Newtype
```

The key is that this decision is not made by staring at rendered strings. It
is made by matching typed source nodes.

## How This Fits The Current Code

Current code already has most of the pieces:

```text
RawSchemaFile     preserves raw NOTA delimiter data
SyntaxSchema      reads datatype declarations into typed syntax
Asschema          has known-root NOTA + rkyv codec
AsschemaArtifact  owns .asschema and .asschema.rkyv IO
MacroLibrary      already proves a typed source artifact can feed runtime macro behavior
```

The missing production shape is:

```text
SchemaSource
SchemaSourceArtifact
SchemaSourceCodec
```

Suggested names:

```rust
pub struct SchemaSource { ... }
pub struct SchemaSourceArtifact { source: SchemaSource }
pub trait SchemaSourceDecode { ... }
pub trait SchemaSourceEncode { ... }
```

`SchemaSourceArtifact` should mirror `AsschemaArtifact`:

```rust
impl SchemaSourceArtifact {
    pub fn read_schema_file(path: impl AsRef<Path>) -> Result<Self, SchemaError>;
    pub fn write_schema_file(&self, path: impl AsRef<Path>) -> Result<(), SchemaError>;
    pub fn to_schema_source(&self) -> String;
    pub fn into_source(self) -> SchemaSource;
}
```

Binary archive support can be added once the typed source object is stable:

```rust
pub fn to_binary_bytes(&self) -> Result<Vec<u8>, SchemaError>;
pub fn from_binary_bytes(bytes: &[u8]) -> Result<Self, SchemaError>;
```

## Why Not Just Use NotaEncode

`NotaEncode` is the value codec for typed data objects.

`SchemaSourceEncode` is a language codec for the authored schema surface.

That distinction is important. The schema source output wants shorthand:

```nota
Entry { Topics * Description * }
```

The raw typed data encoding of the same source tree might be more explicit:

```nota
(Struct Entry [(Derived Topics) (Derived Description)])
```

Both can exist, but only the first is the authored `.schema` language. The
source codec owns the authored language.

Asschema is different again:

```nota
(Public Entry (Struct (Entry {topics (Plain Topics) description (Plain Description)})))
```

That is the assembled program, not the source.

## What This Unlocks

The source-codec layer closes several recurring problems:

- no more guessing whether a one-field declaration is a struct or newtype;
- no more duplicated report examples drifting from real source syntax;
- schema formatter becomes a projection of typed source nodes;
- macro definitions can target typed source-node positions;
- schema upgrade/editor messages can modify source nodes first, then assemble;
- `.schema` artifacts can be checked in and freshness-tested with the same
  discipline as `.asschema`;
- eventually schema can describe its own source-language nodes.

## First Implementation Slice

The smallest useful slice:

```text
1. Rename or wrap SyntaxSchema as SchemaSource.
2. Add SchemaSourceArtifact with read/write `.schema` file methods.
3. Add to_schema_source() canonical writer.
4. Make SchemaEngine lower from SchemaSource, not directly from Document.
5. Add round-trip tests:
   .schema text -> SchemaSource -> canonical .schema text -> SchemaSource
   SchemaSource -> Asschema -> existing checked .asschema
```

Do not start with every macro feature. Start with the strict syntax already
live:

```nota
imports
input enum body
output enum body
namespace declarations
struct fields
enum variants
type references
inline Pascal declarations
derived-field `*`
```

Then macro-library data can move onto the same source-node substrate.

## The Clean Mental Model

The system becomes readable because every layer names what it is:

```text
NOTA      parses structure
Schema    represents authored interface language
Asschema  represents assembled type program
Rust      represents executable generated nouns and traits
Spirit    runs those generated interfaces through Signal/Nexus/SEMA
```

That is the same principle as the triad-engine essence:

```text
The schema names the interface.
The generated Rust names the objects and traits.
The handwritten code should mostly be the real algorithm.
```

Here the added sentence is:

```text
The schema source representation names the authored language before assembly.
```
