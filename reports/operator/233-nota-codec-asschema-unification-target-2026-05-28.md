# 233 - NOTA Codec and Asschema Unification Target

Date: 2026-05-28  
Lane: operator  
Question: what would it look like for schema, assembled schema, and direct
Rust-defined objects to use the same NOTA interfaces?

## Answer

The clean target is one typed NOTA interface shared by both routes:

```text
hand-written Rust type
  -> NotaEncode / NotaDecode
  -> NOTA text

.schema file
  -> Asschema data
  -> generated Rust type
  -> NotaEncode / NotaDecode
  -> NOTA text
```

Today this is split:

- `nota-codec` supports hand-written Rust types through `NotaRecord`,
  `NotaEnum`, `NotaEncode`, and `NotaDecode`.
- `nota-next` is parse-only. It gives `Document`, `Block`, `Delimiter`, and
  source spans.
- `schema-rust-next` currently emits a small local NOTA reader/writer into each
  generated output file.

The next shape removes the third item. Schema-emitted Rust should implement the
same NOTA traits that direct Rust code implements.

## Input Syntax

Authored reactive schema stays terse. The file root is known before reading, so
the root fields are positional.

```nota
{}
((Record Entry) (Observe Query))
((RecordAccepted SemaReceipt) (RecordsObserved RecordSet) (Rejected ErrorReport))
{
  Topic [Text]
  Description [Text]
  RecordIdentifier [Integer]
  Entry [Topic Kind Description Magnitude]
  Query [Topic Kind]
  RecordSet [(Vec Entry)]
  SemaReceipt [RecordIdentifier DatabaseMarker]
  ErrorReport [Description DatabaseMarker]
  DatabaseMarker [CommitSequence StateDigest]
  CommitSequence [Integer]
  StateDigest [Integer]
  Kind (Decision Principle Correction Clarification Constraint)
  Magnitude (Minimum VeryLow Low Medium High VeryHigh Maximum)
}
```

Important delimiter meanings:

- `[]` in `Entry [Topic Kind Description Magnitude]` is a struct field list.
- `(Vec Entry)` is the type-reference object for `Vec<Entry>`.
- `{}` is a native NOTA key/value map.
- `((Record Entry) ...)` is an enum body at a known root position. `Record` is
  a data-carrying variant whose payload type is `Entry`.

## Assembled Schema Data

The assembled schema is not "code in disguise." It is normal serializable data.
It has no macros left. It can be decoded from NOTA, archived with rkyv, cached,
diffed, upgraded, and fed to emitters.

Rust shape:

```rust
#[derive(NotaRecord, rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
pub struct Asschema {
    pub identity: SchemaIdentity,
    pub imports: Vec<ImportDeclaration>,
    pub roots: Vec<RootDeclaration>,
    pub declarations: Vec<TypeDeclaration>,
}

#[derive(NotaEnum, rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
pub enum TypeDeclaration {
    Struct(StructDeclaration),
    Enum(EnumDeclaration),
}

#[derive(NotaEnum, rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
pub enum TypeReference {
    Plain(Name),
    Vector(Box<TypeReference>),
    Optional(Box<TypeReference>),
    Map(Box<MapReference>),
}
```

Asschema NOTA, read against known root type `Asschema`:

```nota
([spirit:lib] [0.1.0])
[]
[
  (RootEnum Input ((Record (Plain Entry)) (Observe (Plain Query))))
  (RootEnum Output ((RecordAccepted (Plain SemaReceipt)) (RecordsObserved (Plain RecordSet)) (Rejected (Plain ErrorReport))))
]
[
  (Struct (Topic [(text (Plain Text))]))
  (Struct (Entry [(topic (Plain Topic)) (kind (Plain Kind)) (description (Plain Description)) (magnitude (Plain Magnitude))]))
  (Struct (RecordSet [(entries (Vector (Plain Entry)))]))
  (Enum (Kind [Decision Principle Correction Clarification Constraint]))
]
```

This output is deliberately more explicit than authored schema. Authored schema
optimizes for humans. Asschema optimizes for exact machine processing.

## Generated Rust

The emitted Rust should be ordinary Rust types plus shared NOTA/rkyv traits:

```rust
#[derive(
    Clone,
    Debug,
    PartialEq,
    Eq,
    NotaRecord,
    rkyv::Archive,
    rkyv::Serialize,
    rkyv::Deserialize,
)]
pub struct Entry {
    pub topic: Topic,
    pub kind: Kind,
    pub description: Description,
    pub magnitude: Magnitude,
}

#[derive(
    Clone,
    Debug,
    PartialEq,
    Eq,
    NotaEnum,
    rkyv::Archive,
    rkyv::Serialize,
    rkyv::Deserialize,
)]
pub enum Input {
    Record(Entry),
    Observe(Query),
}
```

That should compile to the same behavior as the direct Rust path:

```rust
impl NotaDecode for Input {
    fn decode(reader: &mut NotaReader<'_>) -> Result<Self, NotaError> {
        reader.decode_enum()
    }
}

impl NotaEncode for Input {
    fn encode(&self, writer: &mut NotaWriter) -> Result<(), NotaError> {
        writer.encode_enum(self)
    }
}
```

The exact implementation can be derive-generated, schema-emitted, or a mix
during bootstrap. The invariant is that the public interface is shared:
`NotaEncode` and `NotaDecode`, not a private generated mini-codec.

## Direct Rust Route

A hand-written type should use the same interface:

```rust
#[derive(
    Clone,
    Debug,
    PartialEq,
    Eq,
    NotaRecord,
    rkyv::Archive,
    rkyv::Serialize,
    rkyv::Deserialize,
)]
pub struct Query {
    pub topic: Topic,
    pub kind: Kind,
}
```

Input:

```nota
([schema] Decision)
```

Output object:

```rust
Query {
    topic: Topic("schema".to_owned()),
    kind: Kind::Decision,
}
```

The hand-written and schema-generated types do not need two reader stacks.

## Communication Traits

Communication is an additional trait surface on schema root objects, not a
different object model.

```rust
pub trait SignalRoot: NotaEncode + NotaDecode + rkyv::Archive {
    fn short_header(&self) -> ShortHeader;
}

pub trait RoutedMessage<Root> {
    fn origin_route(&self) -> OriginRoute;
    fn root(&self) -> &Root;
}
```

Generated root objects can derive or receive impls for:

- NOTA text at CLI and file boundaries.
- rkyv binary on the socket.
- short-header route triage.
- origin-route mail tracking.
- upgrade/accept-previous traits when schema diff detects a changed type.

The data object remains one object. The traits state which system surfaces it
can participate in.

## Code Transformation

The compiler pipeline should read as a sequence of typed object transforms:

```text
Document
  -> RawSchemaFile
  -> SyntaxSchema
  -> Asschema
  -> RustModule
  -> compiled component
```

Each arrow is a method on a data-bearing object:

```rust
impl RawSchemaFile {
    pub fn read_syntax(&self) -> Result<SyntaxSchema, SchemaError> { ... }
}

impl SyntaxSchema {
    pub fn assemble(&self, registry: &MacroRegistry) -> Result<Asschema, SchemaError> { ... }
}

impl Asschema {
    pub fn emit_rust(&self, emitter: &RustEmitter) -> RustCode { ... }
}
```

No free helper layer is needed. The noun owns the verb at each step.

## Implementation Delta

To reach this target:

1. Move a typed codec surface into `nota-next`: reader, writer, error, traits,
   and derive support or derive-compatible codegen.
2. Make `Asschema` and schema-macro definitions implement the same NOTA traits
   and rkyv traits.
3. Change `schema-rust-next` to emit type definitions and trait impls against
   the shared `nota-next` codec instead of emitting `NotaSource`, `NotaBlock`,
   and local parse helpers into each generated module.
4. Keep schema-generated communication traits on generated root objects:
   Signal, Nexus, SEMA, origin route, short header, mail events, and upgrade.

The value is that every layer becomes ordinary typed data:

```text
NOTA text <-> Rust data <-> rkyv bytes
```

Schema then becomes the mechanism for generating those Rust data objects, not a
parallel runtime language.
