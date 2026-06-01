# Macro Library NOTA Types

Kind: explanation report  
Topics: schema-next, macro-library, nota-types, asschema, structural-macros  
Date: 2026-06-01  
Lane: operator

## Why This Report Exists

This report backfills a chat answer that should have been report-backed first.
The psyche asked what NOTA type the strict macro definitions have, especially
how the macro body is typed. The correct answer is below, tied to the current
`schema-next` implementation.

## Source Shape

The current strict source macro definitions look like this:

```schema
(SchemaMacro SchemaStructDefinition NamespaceDeclaration
  ($Name {$*Fields})
  (Type (Struct $Name [$*Fields])))

(SchemaMacro SchemaEnumDefinition NamespaceDeclaration
  ($Name [$*Variants])
  (Type (Enum $Name ($*Variants))))

(SchemaMacro SchemaNewtypeDefinition NamespaceDeclaration
  ($Name $Reference)
  (Type (Newtype $Name $Reference)))
```

At the source layer, the file is a sequence of `MacroLibrarySourceEntry`
enum values. Today that enum has one variant: `SchemaMacro`.

`SchemaMacro` is therefore not a loose keyword and not just a string checked
by the parser. The source syntax:

```schema
(SchemaMacro SchemaStructDefinition NamespaceDeclaration
  ($Name {$*Fields})
  (Type (Struct $Name [$*Fields])))
```

means:

```rust
MacroLibrarySourceEntry::SchemaMacro(MacroDefinition {
    name: SchemaStructDefinition,
    position: NamespaceDeclaration,
    pattern: ...,
    template: ...,
})
```

The payload carried by the `SchemaMacro` variant has four fields:

```text
MacroName
MacroPosition
MacroPattern
MacroTemplate
```

So the macro-library source is conceptually a vector of enum variants, where
each current variant is `SchemaMacro` carrying a macro-definition payload.

## The Datatype The Declarations Fit Into

There are two outer containers because the system currently has an authored
source form and a serialized artifact form.

The authored source file `schemas/builtin-macros.schema` fits into:

```rust
pub struct DeclarativeMacroLibrary {
    source_entries: Vec<MacroLibrarySourceEntry>,
}

pub enum MacroLibrarySourceEntry {
    SchemaMacro(MacroDefinition),
}
```

The reader is:

```rust
impl DeclarativeMacroLibrary {
    pub fn from_source(source: &str) -> Result<Self, SchemaError> {
        let document = Document::parse(source)?;
        let mut source_entries = Vec::new();
        for object in document.root_objects() {
            source_entries.push(MacroLibrarySourceEntry::from_block(object)?);
        }
        Ok(Self { source_entries })
    }
}
```

So every top-level object in `builtin-macros.schema` must be a
`MacroLibrarySourceEntry`. A top-level object whose first symbol is
`SchemaMacro` becomes the `SchemaMacro` variant. The variant payload is the
definition struct:

```rust
pub struct MacroDefinition {
    name: Name,
    position: MacroPosition,
    pattern: MacroPattern,
    template: MacroTemplate,
}
```

This is the exact fit:

```text
DeclarativeMacroLibrary
└── source_entries: Vec<MacroLibrarySourceEntry>
    └── MacroLibrarySourceEntry::SchemaMacro(MacroDefinition)
        └── source notation: (SchemaMacro Name Position Pattern Template)
```

The serialized `.macro-library` artifact then fits into:

```rust
pub struct MacroLibraryData {
    source_entries: Vec<MacroLibrarySourceEntryData>,
}

pub enum MacroLibrarySourceEntryData {
    SchemaMacro(MacroDefinitionData),
}
```

The conversion is:

```text
DeclarativeMacroLibrary
  -> to_data()
  -> MacroLibraryData
  -> NOTA / rkyv artifact
```

So the most precise answer is:

- source declarations fit into `DeclarativeMacroLibrary`;
- the `SchemaMacro` source node fits into
  `MacroLibrarySourceEntry::SchemaMacro`;
- the data carried by that variant fits into `MacroDefinition`;
- the serialized NOTA/rkyv data form fits into `MacroLibraryData`;
- each serialized source entry fits into
  `MacroLibrarySourceEntryData::SchemaMacro`;
- each serialized variant payload fits into `MacroDefinitionData`.

## Implementation State

This is implemented in `schema-next` commit `7664138c`
(`schema: model schema macro as source entry variant`):

- `DeclarativeMacroLibrary` now owns
  `Vec<MacroLibrarySourceEntry>`.
- `MacroLibrarySourceEntry::SchemaMacro(MacroDefinition)` is the typed source
  variant for `(SchemaMacro ...)`.
- `MacroLibraryData` now owns
  `Vec<MacroLibrarySourceEntryData>`.
- `MacroLibrarySourceEntryData::SchemaMacro(MacroDefinitionData)` preserves
  the same variant in the checked-in `.macro-library` NOTA/rkyv artifact.
- `schemas/core.schema` and `schemas/core.asschema` now declare
  `MacroLibrarySourceEntry` as an enum with the `SchemaMacro` data-carrying
  variant.
- Tests pin both layers:
  `schema_macro_source_records_are_enum_variants_inside_the_library` and
  `schema_macro_artifact_records_preserve_the_source_entry_variant`.

## Runtime Data Type

The checked-in `.macro-library` artifact is typed as:

```rust
pub struct MacroLibraryData {
    source_entries: Vec<MacroLibrarySourceEntryData>,
}

pub enum MacroLibrarySourceEntryData {
    SchemaMacro(MacroDefinitionData),
}

pub struct MacroDefinitionData {
    name: Name,
    position: MacroPosition,
    pattern: MacroPatternData,
    template: MacroTemplateData,
}
```

These types currently live in `schema-next/src/declarative.rs` and derive both
NOTA and rkyv:

```rust
#[derive(
    rkyv::Archive,
    rkyv::Serialize,
    rkyv::Deserialize,
    nota_next::NotaDecode,
    nota_next::NotaEncode,
    Clone,
    Debug,
    Eq,
    PartialEq,
)]
```

So the artifact is not a string table and not parser-side magic. It is typed
data that can round-trip through NOTA text and rkyv bytes.

## Macro Body Type

The body is a recursive structural tree. Pattern and template are separate
types because one matches source input and the other builds output, but they
share the same shape family.

Pattern:

```rust
pub struct MacroPatternData {
    object: MacroPatternObjectData,
}

pub enum MacroPatternObjectData {
    Capture(String),
    RestCapture(String),
    Atom(String),
    Delimited(Box<MacroPatternDelimitedData>),
}

pub struct MacroPatternDelimitedData {
    delimiter: MacroDelimiter,
    children: Vec<MacroPatternObjectData>,
}
```

Template:

```rust
pub struct MacroTemplateData {
    object: MacroTemplateObjectData,
}

pub enum MacroTemplateObjectData {
    Capture(String),
    RestCapture(String),
    Atom(String),
    Delimited(Box<MacroTemplateDelimitedData>),
}

pub struct MacroTemplateDelimitedData {
    delimiter: MacroDelimiter,
    children: Vec<MacroTemplateObjectData>,
}
```

The delimiter enum is:

```rust
pub enum MacroDelimiter {
    Parenthesis,
    SquareBracket,
    Brace,
    PipeParenthesis,
    PipeBrace,
}
```

## Example Lowering

The pattern:

```schema
($Name {$*Fields})
```

is data shaped like:

```rust
Delimited(Parenthesis, [
    Capture("Name"),
    Delimited(Brace, [
        RestCapture("Fields"),
    ]),
])
```

The template:

```schema
(Type (Struct $Name [$*Fields]))
```

is data shaped like:

```rust
Delimited(Parenthesis, [
    Atom("Type"),
    Delimited(Parenthesis, [
        Atom("Struct"),
        Capture("Name"),
        Delimited(SquareBracket, [
            RestCapture("Fields"),
        ]),
    ]),
])
```

## Precise Answer

There are two files and therefore two container datatypes:

- `schemas/builtin-macros.schema` is authored source and is read as
  `DeclarativeMacroLibrary { source_entries:
  Vec<MacroLibrarySourceEntry> }`;
- `schemas/builtin-macros.macro-library` is the checked-in serialized
  artifact and is read as `MacroLibraryData { source_entries:
  Vec<MacroLibrarySourceEntryData> }`.

Inside the authored source container, `SchemaMacro` is a variant:

```rust
pub enum MacroLibrarySourceEntry {
    SchemaMacro(MacroDefinition),
}
```

Inside the serialized artifact container, the same variant is preserved as:

```rust
pub enum MacroLibrarySourceEntryData {
    SchemaMacro(MacroDefinitionData),
}
```

So the checked-in `.macro-library` file also carries `SchemaMacro` as a real
variant. It does not project the variant away.

Each `MacroDefinitionData` is a struct with:

- `name`
- `position`
- `pattern`
- `template`

The macro body is not raw text. It is a recursive enum/tree of:

- capture
- rest capture
- atom
- delimited node with a delimiter and vector of child nodes

That recursive structure is the NOTA type of the macro body.

## Which Variants Exist

There are three different "variant" layers in this area.

### Source Record Head

At the top level of `schemas/builtin-macros.schema`, there is currently only
one source-entry variant:

```schema
SchemaMacro
```

The reader now models that as:

```rust
MacroLibrarySourceEntry::SchemaMacro(MacroDefinition)
MacroLibrarySourceEntryData::SchemaMacro(MacroDefinitionData)
```

So at this layer, `SchemaMacro` is a real enum variant. It is not one variant
among many today, but it is still a variant: the macro-library source datatype
and the serialized artifact datatype each have one current case and can grow
more cases later.

### Pattern And Template Object Variants

Inside the pattern and template bodies, the recursive body enum has these
variants:

```rust
Capture(String)
RestCapture(String)
Atom(String)
Delimited(Box<...>)
```

`Delimited` then carries:

```rust
MacroDelimiter
Vec<child object>
```

where `MacroDelimiter` is:

```rust
Parenthesis
SquareBracket
Brace
PipeParenthesis
PipeBrace
```

So `$Name` is `Capture("Name")`, `$*Fields` is
`RestCapture("Fields")`, `Type` is `Atom("Type")`, and
`($Name {$*Fields})` is a `Delimited(Parenthesis, ...)` object.

### Template Output Heads

After a template expands, the assembled-template interpreter currently accepts
these top-level output heads:

```schema
Type
Fields
Variants
Reference
```

`Type` then branches to:

```schema
Struct
Enum
Newtype
```

`Reference` can lower assembled references for:

```schema
Vector
Optional
Map
```

or fall back to ordinary type references such as `String`, `Integer`,
`Boolean`, `Path`, and declared names.

## Current Gap

The data discipline is real, but one piece remains pre-final: the Rust nouns
for `MacroLibraryData`, `MacroLibrarySourceEntryData`,
`MacroDefinitionData`, `MacroPatternObjectData`, and
`MacroTemplateObjectData` are still hand-written in `schema-next`. The
intended next step is to emit those nouns from `schemas/core.asschema`, then
delete the hand-written mirror.
