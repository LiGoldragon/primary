# 412 — Schema strict positional structs

## Why this exists

The psyche corrected the schema language direction: the old struct-body
pair surface is deprecated and must not be accepted.

Retired:

```nota
Record { Topic String }
Entry { Topic * Kind * }
Entry { topic Topic }
```

Accepted:

```nota
Record { Topic Description }
Entry { Topic Kind }
Entry { marker.DatabaseMarker }
Text String
Entry { Text }
Entry { text.String }
```

The Spirit capture for this correction is `lpk9`: struct bodies are
positional lists of field types; explicit field names use the dot
differentiator; the schema reader rejects the old pair form.

Follow-up Spirit capture `i3p0`: dotted explicit field names are only for
roles that differ from the type-derived field name:

```nota
Entry { topic.Topic }  ;; invalid
Entry { Topic }        ;; correct
```

## Visual Summary

### Syntax Shift

```mermaid
flowchart LR
    old["Old struct body<br/>Record { Topic String }<br/>Entry { topic Topic }<br/>Entry { Topic * }"]
    ambiguity["Ambiguous parser<br/>pairs adjacent objects<br/>or derives fields from *"]
    retired["Rejected<br/>RetiredStructFieldSyntax"]

    new["New struct body<br/>Record { Topic Description }<br/>Entry { marker.DatabaseMarker }<br/>Entry { Text }"]
    strict["Strict parser<br/>one object = one field"]
    lowered["Lowered schema<br/>stable field names<br/>typed references"]

    old --> ambiguity --> retired
    new --> strict --> lowered
```

### What One Field Means Now

```mermaid
flowchart TD
    field["Struct body object"]

    field --> bare["TypeName"]
    bare --> derived["field name derives from type<br/>RecordIdentifier -> record_identifier"]
    derived --> plain["reference = TypeName"]

    field --> dotted["field_name.TypeName"]
    dotted --> explicit["field name is explicit<br/>reference is TypeName"]
    dotted --> redundant["topic.Topic"]
    redundant --> rejectRedundant["reject: just use Topic"]

    field --> structural["(Optional Type)<br/>(Vector Type)<br/>(Map Key Value)"]
    structural --> structuralDerived["field name derives from reference shape<br/>optional_type, type_vector, value_by_key"]

    field --> retiredStar["Type *"]
    retiredStar --> reject["reject"]

    field --> retiredPair["field Type"]
    retiredPair --> reject

    field --> retiredScalar["String / Integer / Boolean / Path / Bytes"]
    retiredScalar --> reject
```

### Concrete Translation Examples

| Intent | Retired | Strict |
|---|---|---|
| Use existing field types | `Entry { Topic * Kind * }` | `Entry { Topic Kind }` |
| Explicit field role | `Entry { marker DatabaseMarker }` | `Entry { marker.DatabaseMarker }` |
| Redundant explicit role | `Entry { topic Topic }` | `Entry { Topic }`; `Entry { topic.Topic }` is rejected |
| Scalar wrapper type | `Topic { string String }` | `Topic String` |
| Struct-local scalar role | `Entry { text String }` | `Entry { text.String }` |
| Named scalar role | `Entry { value String }` | `Value String` then `Entry { Value }` |
| Collection field | `Query { topics (Vector Topic) }` | `Query { (Vector Topic) }` or `Topics (Vector Topic)` then `Query { Topics }` |

## Implementation

Branch:

`/home/li/wt/github.com/LiGoldragon/schema-next/schema-namespaces-poc`

Changed parser surfaces:

- `src/source.rs`: removed the `FieldPairs` mode from source struct
  bodies. A struct field is now one object: `TypeName`,
  `field_name.TypeName`, or a structural reference object such as
  `(Optional Integer)`.
- `src/declarative.rs`: removed the macro-expansion compatibility path
  that paired adjacent struct-field objects. The macro path now follows
  the same one-object-per-field rule.
- `src/engine.rs`: added `RetiredStructFieldSyntax` for direct retired
  syntax diagnostics.
- Bare scalar fields inside struct bodies are rejected to close the
  `Record { Topic String }` ambiguity. Use `Text String` + `{ Text }`,
  or `text.String` when the scalar role must be local to that struct.

### Parser Closure

```mermaid
flowchart TB
    source["Schema source text"]

    source --> sourceCodec["Source codec path<br/>src/source.rs"]
    source --> macroEngine["Macro expansion path<br/>src/declarative.rs"]

    sourceCodec --> oldSource["removed: SourceStructSyntax::FieldPairs"]
    macroEngine --> oldMacro["removed: adjacent object pairing"]

    oldSource --> strictSource["SourceStructBody::from_block<br/>maps every object through<br/>SourceField::from_positional_block"]
    oldMacro --> strictMacro["MacroExpansionFields::lower<br/>maps every object through<br/>MacroExpansionField::lower"]

    strictSource --> common["same accepted shapes<br/>TypeName<br/>field.TypeName<br/>structural reference object"]
    strictMacro --> common

    common --> error["retired forms return<br/>RetiredStructFieldSyntax"]
    common --> schema["valid forms lower to Schema"]
```

## Fixture Migration

The schema-next tests and fixtures were migrated away from:

- star shorthand: `Type *`
- lower-case field pairs: `field Type`
- Pascal-scalar ambiguity: `Topic String` inside a struct body
- inline private field declarations inside struct bodies

The last item is a real semantic change: private helper types are no
longer invented from inside a struct field. If a type is needed, declare
it in the namespace.

### Migration Shape

```mermaid
flowchart LR
    fixtures["schema-next fixtures<br/>and test literals"]
    star["Type *"]
    lower["field Type"]
    scalar["Type String inside struct"]
    inline["inline private declaration"]

    fixtures --> star --> starNew["Type"]
    fixtures --> lower --> lowerNew["field.Type"]
    fixtures --> scalar --> scalarNew["named type declaration<br/>or field.String"]
    fixtures --> inline --> inlineNew["explicit namespace declaration"]

    starNew --> tests["green tests"]
    lowerNew --> tests
    scalarNew --> tests
    inlineNew --> tests
```

## Verification

Passed locally:

```sh
cargo test -- --nocapture
cargo fmt -- --check
cargo clippy --all-targets -- -D warnings
nix flake check
```

`nix flake check` ran all 18 flake checks successfully.

## Migration Surface

Token-level scan across `/git/github.com/LiGoldragon` found 52 `.schema`
files with likely old struct-body tokens. This is a heuristic; it still
includes metadata forms such as `Stream { token ... }` and raw-core
fixtures that are not the strict source language. The live component
repos with likely work include `spirit`, `mind`, `lojix`, `terminal`,
`mirror`, `criome`, `cloud`, `orchestrate`, and the signal/meta-signal
contract repos.

### Broader Porting Surface

```mermaid
flowchart TD
    strict["schema-next strict parser"]
    consumers["consumer schema repos"]
    fail["old syntax fails parse/lower"]
    port["port schema files"]
    regenerate["regenerate emitted Rust"]
    componentTests["run component Nix checks"]

    strict --> consumers --> fail --> port --> regenerate --> componentTests
```

High-count areas:

- `schema-rust-next`: 10 test fixtures still use old examples.
- `schema-next`: remaining hits are intentional macro/raw fixtures or
  negative retired-syntax tests after this branch.
- component contracts: mostly `Type *`, `field Type`, and direct scalar
  wrappers such as `value String`.

The next practical step is to land this parser change, then migrate each
consumer schema repo as it repins to the strict schema-next.
