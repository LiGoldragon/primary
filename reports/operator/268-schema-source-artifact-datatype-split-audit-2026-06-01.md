# Schema Source/Artifact Datatype Split Audit

*Kind: audit · Topics: schema-next, source-artifact-types, macro-library, asschema · 2026-06-01 · operator lane*

## Question

The audited pattern is the split the psyche flagged in
`reports/operator/267-macro-library-nota-types-2026-06-01.md`: one
semantic object represented twice, once as a source enum/type and once as
a serialized artifact enum/type.

Governing intent:

- Spirit 1301: macro library source and serialized artifact use one
  datatype for source entries, not separate source/data enum splits.
- Spirit 1302: source text and checked-in artifact data share the same
  typed noun when they represent the same object; only real semantic
  projections get a separate type.

Subagent `Averroes` ran a read-only sweep across `schema-next`,
`schema-rust-next`, `nota-next`, `spirit-next`, and primary reports. I
ran a local grep/read pass in parallel and merged the findings below.

## Verdict

The exact `MacroLibrarySourceEntry` /
`MacroLibrarySourceEntryData` split is fixed. There is still one direct
library-level instance of the same pattern and one deeper data/executable
mirror inside the macro pattern/template model.

No confirmed instance of this source/artifact datatype split was found in
`schema-rust-next`, `nota-next`, or `spirit-next`.

## Confirmed Violation: Macro Library Value Split

Current code:

```rust
pub struct DeclarativeMacroLibrary {
    source_entries: Vec<MacroLibrarySourceEntry>,
}

pub struct MacroLibraryData {
    source_entries: Vec<MacroLibrarySourceEntry>,
}
```

Both types represent the same macro library object: a vector of
`MacroLibrarySourceEntry`. The methods
`DeclarativeMacroLibrary::from_data` and
`DeclarativeMacroLibrary::to_data` are the smell: a conversion exists
between two types whose payload and semantic identity are the same.

File:

- `/git/github.com/LiGoldragon/schema-next/src/declarative.rs`

Cleaner shape:

```rust
pub struct MacroLibrary {
    source_entries: Vec<MacroLibrarySourceEntry>,
}

pub struct MacroLibraryArtifact {
    macro_library: MacroLibrary,
}
```

`MacroLibrary` is the single NOTA/rkyv datatype. It reads source, writes
checked-in `.macro-library`, archives to rkyv, and exposes the entries.
`MacroLibraryArtifact` is only the IO wrapper: paths, file reads, file
writes, binary bytes. If runtime dispatch needs a separate object, name
that projection by what it is:

```rust
struct ExecutableMacroLibrary {
    handlers: Vec<Box<dyn SchemaMacroHandler>>,
}
```

That keeps the semantic split honest: source/artifact data is one noun;
runtime executable handlers are another noun.

## Confirmed Violation: Pattern/Template Data Mirrors

Current code has serializable trees:

```rust
pub struct MacroPatternData { ... }
pub enum MacroPatternObjectData { ... }
pub struct MacroTemplateData { ... }
pub enum MacroTemplateObjectData { ... }
```

and private executable mirrors:

```rust
struct MacroPattern { ... }
enum PatternObject { ... }
struct MacroTemplate { ... }
enum TemplateObject { ... }
```

These are bridged with `from_data` / `to_data` methods. That is the same
family of smell, but one layer deeper. The semantics of pattern and
template are different from each other, so `MacroPattern` and
`MacroTemplate` should remain different nouns. The issue is the duplicate
`Data` tree inside each noun.

Cleaner shape:

```rust
pub struct MacroPattern {
    object: MacroPatternObject,
}

pub enum MacroPatternObject {
    Capture(String),
    RestCapture(String),
    Atom(String),
    Delimited(Box<MacroPatternDelimited>),
}
```

`MacroPattern` derives `NotaDecode`, `NotaEncode`, and rkyv traits
directly. Matching behavior lives as methods on `MacroPattern` and
`MacroPatternObject`. If a cached runtime form becomes necessary, it gets
a name like `CompiledMacroPattern`; it does not become a second
source/artifact noun.

Same rule for `MacroTemplate`.

## Adjacent Mirror: Core Macro Nouns

`schema-next/schemas/core.asschema` already contains the macro-table
nouns as assembled schema data, while `schema-next/src/declarative.rs`
still hand-writes the same vocabulary in Rust.

This is not the same narrow source/artifact enum split, because the Rust
types currently bootstrap the system. It is still adjacent to the same
architectural pressure: the checked-in assembled schema and handwritten
Rust should not both be long-term sources of truth for the same macro
library vocabulary.

Next target after the datatype cleanup: emit the macro-library nouns from
`core.asschema`, then keep handwritten Rust only for the bootstrap reader
and the actual behavior methods.

## Benign Projections

`Asschema` and `AsschemaArtifact` are not a violation. `Asschema` is the
value; `AsschemaArtifact` owns file and binary IO around that value.

`RawSchemaFile`, `SyntaxSchema`, and `Asschema` are not a violation. They
are real semantic stages: raw NOTA delimiter preservation, strict
authored-schema syntax, and macro-free assembled schema.

`RustModule` and `RustDeclaration` in `schema-rust-next` are not a
violation. They are target-language emission models projected from
`Asschema`, not serialized copies of the same schema object.

The schema-level `MacroNodeDefinition` wrapper around
`nota_next::MacroNodeDefinition` is probably legitimate. Schema adds
schema-specific position and dispatch; NOTA owns the structural match
node. Keep an eye on the name, but this does not currently look like a
source/artifact split.

## Implementation Order

1. Collapse `DeclarativeMacroLibrary` and `MacroLibraryData` into one
   public serializable noun, preferably `MacroLibrary`.
2. Keep `MacroLibraryArtifact` as the IO owner only.
3. Collapse `MacroPatternData` into serializable `MacroPattern`, and
   collapse `MacroTemplateData` into serializable `MacroTemplate`.
4. Rename any runtime-only projections with explicit runtime words:
   `ExecutableMacroLibrary`, `CompiledMacroPattern`, or similar.
5. Add a guard test in `schema-next` that rejects revival of the known
   bad names: `MacroLibrarySourceEntryData`, `MacroDefinitionData`,
   `MacroPatternData`, and `MacroTemplateData`.
6. After the data nouns are clean, move toward emitted macro-library
   nouns from `core.asschema` so the handwritten bootstrap surface
   shrinks instead of becoming another mirror.

## Audit Commands

Local audit searches:

```sh
rg -n "MacroLibrarySourceEntryData|DefinitionData|SourceEntryData|from_source|from_data|into_data|to_data|Artifact|SourceEntry|source_entries|struct .*Data|enum .*Data" \
  /git/github.com/LiGoldragon/schema-next/src \
  /git/github.com/LiGoldragon/schema-next/tests \
  /git/github.com/LiGoldragon/schema-next/schemas \
  /git/github.com/LiGoldragon/schema-rust-next/src \
  /git/github.com/LiGoldragon/schema-rust-next/tests \
  /git/github.com/LiGoldragon/nota-next/src \
  /git/github.com/LiGoldragon/nota-next/tests \
  /git/github.com/LiGoldragon/spirit-next/src \
  /git/github.com/LiGoldragon/spirit-next/tests \
  /git/github.com/LiGoldragon/spirit-next/schema
```

The subagent confirmed the same major result independently: no confirmed
source/artifact split outside `schema-next`; remaining issues are the
macro-library value split and macro pattern/template data mirrors.
