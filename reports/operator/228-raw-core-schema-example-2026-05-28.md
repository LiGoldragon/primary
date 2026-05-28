# 228 — Raw Core Schema Example

Date: 2026-05-28  
Lane: operator  
Repos touched: `schema-next`

## Request

Create a large example using raw NOTA to read a core schema file. The file is a
struct named after its filename, like Rust modules, and contains a key/value map
of datatype names to raw NOTA datatype objects.

## Result

Implemented `schema_next::RawSchemaFile` as the raw read layer before schema
lowering.

Source path:

```text
/git/github.com/LiGoldragon/schema-next/src/raw.rs
```

The reader does this:

```text
schemas/core.schema
        |
        | file stem
        v
root struct name = Core
        |
        | nota-next parse
        v
one root brace object
        |
        | pair read
        v
RawDatatypeMap { Name -> RawNotaDatatype }
```

No root struct label is written in the file. The caller already knows it is
reading `Core` from `core.schema`.

## Large Fixture

The concrete fixture is:

```text
/git/github.com/LiGoldragon/schema-next/tests/fixtures/raw-core/core.schema
```

It is a real `.schema` file and is legal NOTA before schema-specific reading.
The root object is one brace key/value map:

```nota
{
  Text [String]
  Integer AtomInteger
  Boolean (False True)
  Version [String]
  Name [String]
  TypeName [Name]
  FieldName [Name]
  ModuleName [Name]
  ModulePath [ModuleName]
  CrateName [Name]
  Description [String]
  Documentation [|Core schema raw NOTA fixture with apostrophe's text, a closing bracket ], and no double quotes.|]
  Topic [Text]
  Topics [Topic]
  Magnitude (Trace Low Medium High Maximum)
  Certainty (Possible Likely Certain)
  RecordKind (Decision Principle Correction Clarification Constraint Observation Question)
  RawAtom {| RawAtom text Text |}
  RawText {| RawText text Text |}
  RawRecord {| RawRecord items RawDatatypeList |}
  RawVector {| RawVector items RawDatatypeList |}
  RawKeyValue {| RawKeyValue entries RawDatatypeMap |}
  RawPipeParenthesis {| RawPipeParenthesis items RawDatatypeList |}
  RawPipeBrace {| RawPipeBrace items RawDatatypeList |}
  RawDatatype (| RawDatatype RawAtom RawText RawRecord RawVector RawKeyValue RawPipeParenthesis RawPipeBrace |)
  RawDatatypeList [RawDatatype]
  RawDatatypeMap { key Name value RawDatatype }
  OptionalTopic (Optional Topic)
  DescriptionIndex { key Topic value Description }
  Field {| Field name FieldName datatype RawDatatype |}
  Fields [Field]
  StructDeclaration {| StructDeclaration name TypeName fields Fields |}
  UnitVariant {| UnitVariant name TypeName |}
  DataVariant {| DataVariant name TypeName payload RawDatatype |}
  EnumVariant (| EnumVariant UnitVariant DataVariant |)
  EnumVariants [EnumVariant]
  EnumDeclaration {| EnumDeclaration name TypeName variants EnumVariants |}
  NewtypeDeclaration {| NewtypeDeclaration name TypeName inner RawDatatype |}
  DatatypeDeclaration (| DatatypeDeclaration StructDeclaration EnumDeclaration NewtypeDeclaration |)
  DatatypeDeclarations [DatatypeDeclaration]
  ImportPath [ModuleName]
  ImportAll {| ImportAll path ImportPath |}
  ImportSome {| ImportSome path ImportPath names TypeNames |}
  TypeNames [TypeName]
  ImportDeclaration (| ImportDeclaration ImportAll ImportSome |)
  ImportDeclarations [ImportDeclaration]
  SchemaNode {| SchemaNode tag Name data RawDatatype |}
  MacroParameter {| MacroParameter name Name datatype RawDatatype |}
  MacroParameters [MacroParameter]
  MacroExpansion {| MacroExpansion output RawDatatype |}
  MacroDefinition {| MacroDefinition name Name parameters MacroParameters expansion MacroExpansion |}
  MacroDefinitions [MacroDefinition]
  CoreSchemaFile {| CoreSchemaFile datatypes RawDatatypeMap |}
}
```

## What Entries Become

The raw reader preserves the NOTA data object. It does not lower to schema yet.

| Entry | Raw datatype object |
|---|---|
| `Integer AtomInteger` | `RawNotaDatatype::Atom("AtomInteger")` |
| `Text [String]` | `RawNotaDatatype::Vector([Atom("String")])` |
| `Documentation [|...|]` | `RawNotaDatatype::Text(...)` |
| `Magnitude (Trace Low Medium High Maximum)` | `RawNotaDatatype::Record([Atom("Trace"), ...])` |
| `RawDatatypeMap { key Name value RawDatatype }` | `RawNotaDatatype::KeyValue(RawDatatypeMap { key -> Atom("Name"), value -> Atom("RawDatatype") })` |
| `StructDeclaration {| StructDeclaration name TypeName fields Fields |}` | `RawNotaDatatype::PipeBrace([Atom("StructDeclaration"), Atom("name"), ...])` |
| `DatatypeDeclaration (| DatatypeDeclaration StructDeclaration EnumDeclaration NewtypeDeclaration |)` | `RawNotaDatatype::PipeParenthesis([Atom("DatatypeDeclaration"), ...])` |

This is intentionally not `Asschema` yet. It is the raw NOTA datatype map that a
core schema reader can use before applying macro/lowering semantics.

## Test Witness

The main test file is:

```text
/git/github.com/LiGoldragon/schema-next/tests/raw_core_schema.rs
```

The tests prove:

1. `core.schema` parses as NOTA through `nota_next::Document`.
2. The root name is derived from the path: `schemas/core.schema` -> `Core`.
3. The root object is one native brace key/value map.
4. The large fixture exposes at least 40 datatype entries.
5. Bracket, parenthesis, brace, pipe-parenthesis, pipe-brace, atom, and pipe
   text forms are preserved as distinct raw datatype variants.
6. Negative fixtures are also real `.schema` files and parse as NOTA before
   schema-specific rejection:
   - `tests/fixtures/raw-core/non-map-root.schema`
   - `tests/fixtures/raw-core/odd-map.schema`

## Design Correction Baked In

The raw layer keeps delimiter structure separate from semantic expectation:

- `[]` remains raw bracket/vector structure at this layer. A later schema
  position typed as `String` or a string newtype may read bracket text as text.
- `()` remains raw record/struct structure at this layer. It becomes a
  tagged/data-carrying schema node only when the expected type is `SchemaNode`
  or another struct with tag/payload fields.
- `{}` is native NOTA key/value map structure. The schema layer can consume it,
  but key/value-ness is not macro magic.

## Verification

Commands run in `/git/github.com/LiGoldragon/schema-next`:

```sh
cargo fmt && cargo test
nix flake check --print-build-logs
```

Both passed.
