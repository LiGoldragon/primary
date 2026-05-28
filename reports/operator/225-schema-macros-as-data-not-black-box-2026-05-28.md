# 225 — Schema macros as data, not black-box parser logic

## Why this report exists

Psyche corrected the schema direction on 2026-05-28: macros are not
special parser tricks. A macro is a data object. It must be assembled,
serialized, deserialized, and then read into the executable macro table.

Spirit record 1108 captures the durable version:

> Schema macros must be assembled before use. A macro is a schema data
> object: it lowers to assembled schema, can be serialized and
> deserialized, and is then read to produce the executable macro table.
> Pre-assembled macros and pre-assembled schemas must be loadable as
> data; no schema mechanism should exist only as ad hoc parser logic or
> black-box code.

## My corrected understanding

The intended stack is not:

```text
schema text -> ad hoc Rust parser structs -> macro behavior
```

That is the black box psyche is rejecting.

The intended stack is:

```text
schema text
  -> nota object tree
  -> macro-schema lowering
  -> assembled schema data
  -> serialized/deserialized assembled schema
  -> read assembled macro data into macro table
  -> use macro table to assemble later schemas
  -> emit Rust from assembled schema data
```

The key distinction: executable Rust code may implement the mechanics
of reading and dispatching, but the macro definitions themselves must
not live only as private Rust structs produced by handwritten parsing.
They must be normal schema data.

## What `builtin-macros.schema` should become

Current file:

```nota
(SchemaMacro SchemaStructDefinition NamespaceDeclaration
  ($Name [$*Fields])
  (Type (Struct $Name [$*Fields])))

(SchemaMacro SchemaEnumDefinition NamespaceDeclaration
  ($Name ($*Variants))
  (Type (Enum $Name ($*Variants))))

(SchemaMacro SchemaStructFields StructFields
  [$*Fields]
  (Fields $*Fields))

(SchemaMacro SchemaEnumVariants EnumVariants
  ($*Variants)
  (Variants $*Variants))
```

What each entry should be after assembly is data like this, not an
opaque parser side effect:

```text
SchemaMacro {
  macro_name: SchemaStructDefinition,
  macro_position: NamespaceDeclaration,
  macro_pattern: Pair(Name, SquareBracket(RestCapture(Fields))),
  macro_template: Type(Struct(Name, Fields))
}
```

Then it serializes as an assembled schema object and can be loaded back
to produce the runtime macro table entry.

The runtime macro table is therefore a cache/view of assembled macro
objects, not the source of truth.

## What the current code does wrong

`repos/schema-next/src/declarative.rs` currently parses
`schemas/builtin-macros.schema` directly into private Rust structs:

- `MacroDefinition`
- `MacroDefinitionRecord`
- `MacroPattern`
- `PatternObject`
- `MacroTemplate`
- `TemplateObject`
- `CaptureName`

Those objects are useful as a bootstrap prototype, but they are not yet
the desired architecture. They are not emitted from schema as Rust
datatypes, and the macro table is not loaded from serialized assembled
schema data.

That is the black-box boundary to remove.

## What the actual data types should be

The bootstrap schema for macro definitions should emit Rust data types
roughly equivalent to:

```rust
pub struct SchemaMacro {
    pub macro_name: MacroName,
    pub macro_position: MacroPosition,
    pub macro_pattern: MacroPattern,
    pub macro_template: MacroTemplate,
}

pub enum MacroPattern {
    Capture(CaptureName),
    RestCapture(CaptureName),
    Atom(Text),
    Parenthesis(PatternObjects),
    SquareBracket(PatternObjects),
    Brace(PatternObjects),
}

pub enum MacroTemplate {
    Capture(CaptureName),
    RestCapture(CaptureName),
    Atom(Text),
    Parenthesis(TemplateObjects),
    SquareBracket(TemplateObjects),
    Brace(TemplateObjects),
}

pub enum MacroOutputKind {
    Imports,
    RootEnum,
    Types,
    Type,
    Fields,
    Variants,
    Reference,
    Asschema,
}
```

Those are not final names, but they show the required shape: the macro
language itself is a typed data language.

## What `.asschema` means

`.asschema` is NOTA-formatted assembled-schema data. It is not a
readable debug trace and not a prose witness. The readable expansion
view belongs beside it as `*.witness.txt`.

The correction landed in `schema-next` commit `2d4d680e`
(`schema: make asschema fixtures nota data`):

- `Asschema::to_nota()` serializes assembled schema into one NOTA root.
- `Asschema::from_nota()` parses that NOTA back into `Asschema`.
- Every big `.asschema` fixture now round-trips through those methods.
- Human-readable macro traces moved to `.witness.txt`.

So an assembled macro table for the builtin macro file should be NOTA
data, not this prose shape:

```text
macro_table
  macro SchemaStructDefinition
    position NamespaceDeclaration
    pattern
      pair
        capture Name
        square
          rest_capture Fields
    template
      parenthesis
        atom Type
        parenthesis
          atom Struct
          capture Name
          square
            rest_capture Fields

  macro SchemaEnumDefinition
    position NamespaceDeclaration
    pattern
      pair
        capture Name
        parenthesis
          rest_capture Variants
    template
      parenthesis
        atom Type
        parenthesis
          atom Enum
          capture Name
          parenthesis
            rest_capture Variants
```

That prose can exist only as `builtin-macros.witness.txt`. The
load-bearing artifact is `builtin-macros.asschema`, a NOTA value that
can be parsed and compared as data.

## Existing big examples and their limitation

The current big examples now exist in both schema and Rust-emission
repos:

- `/git/github.com/LiGoldragon/schema-next/tests/fixtures/big-schemas/spirit-reactive-large.schema`
- `/git/github.com/LiGoldragon/schema-next/tests/fixtures/big-schemas/spirit-reactive-large.asschema`
- `/git/github.com/LiGoldragon/schema-next/tests/fixtures/big-schemas/triad-reactive-large.schema`
- `/git/github.com/LiGoldragon/schema-next/tests/fixtures/big-schemas/triad-reactive-large.asschema`
- `/git/github.com/LiGoldragon/schema-next/tests/fixtures/big-schemas/imported-mail-consumer.schema`
- `/git/github.com/LiGoldragon/schema-next/tests/fixtures/big-schemas/imported-mail-consumer.asschema`

The Rust-emission side landed in `schema-rust-next` commit `0dda5fd7`
(`schema-rust: add big schema emission witnesses`):

- `/git/github.com/LiGoldragon/schema-rust-next/tests/fixtures/big-schemas/spirit-reactive-large.generated.rs`
- `/git/github.com/LiGoldragon/schema-rust-next/tests/fixtures/big-schemas/triad-reactive-large.generated.rs`
- `/git/github.com/LiGoldragon/schema-rust-next/tests/fixtures/big-schemas/imported-mail-consumer.generated.rs`

The `schema-rust-next` tests now prove:

- authored `.schema` lowers to NOTA `.asschema`;
- the checked-in `.asschema` parses back into `Asschema`;
- the same `Asschema` emits checked-in Rust;
- the large Spirit generated Rust compiles and drives NOTA parse,
  rkyv frame encode/decode, generated Nexus trait dispatch, and
  origin-route preservation;
- generated no-free-function and no-legacy-helper checks now cover
  every `*.generated.rs` fixture, not only the small Spirit fixture.

These examples are stronger than before, but still not enough for the
macro-table vision. They show ordinary schema documents lowering to
assembled schema and generated Rust. They do not yet prove that the
macro table itself is schema data that can be serialized/deserialized
and loaded.

## Implementation target from here

The next implementation should stop treating
`schemas/builtin-macros.schema` as a special parser file and instead
create the missing data pipeline:

1. Define the macro-definition schema as data.
2. Lower `builtin-macros.schema` into an assembled macro-table
   witness.
3. Emit Rust datatypes for the macro table from that assembled schema.
4. Serialize and deserialize the assembled macro-table data.
5. Build `MacroRegistry` from the deserialized macro-table data.
6. Re-run the existing big schemas through that loaded macro table.

The proof is not complete until a test can say:

```text
builtin-macros.schema
  -> builtin-macros.asschema
  -> builtin-macros.generated.rs
  -> serialized macro table
  -> deserialized macro table
  -> MacroRegistry
  -> spirit-reactive-large.schema
  -> spirit-reactive-large.asschema
  -> spirit-reactive-large.generated.rs
```

That is the end-to-end shape psyche is asking for.
