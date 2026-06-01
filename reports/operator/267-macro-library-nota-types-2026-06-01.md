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

At the source layer, the file is a sequence of `SchemaMacro` records. Each
record has five positional fields:

```text
SchemaMacro
MacroName
MacroPosition
MacroPattern
MacroTemplate
```

So the macro-library source is conceptually a vector of macro-definition
structs.

## Runtime Data Type

The checked-in `.macro-library` artifact is typed as:

```rust
pub struct MacroLibraryData {
    definitions: Vec<MacroDefinitionData>,
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

The macro-library file is typed as `MacroLibraryData`, which contains
`Vec<MacroDefinitionData>`.

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

## Current Gap

The data discipline is real, but one piece remains pre-final: the Rust nouns
for `MacroLibraryData`, `MacroDefinitionData`, `MacroPatternObjectData`, and
`MacroTemplateObjectData` are still hand-written in `schema-next`. The intended
next step is to emit those nouns from `schemas/core.asschema`, then delete the
hand-written mirror.

