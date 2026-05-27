# 380 — Bottom-up tour, Layer 2: Schema macros

*Psyche-verification tour, Layer 2 of 7 (record 868). Layer 1
(/376) covered NOTA. Layer 2 is the macro system in `schema-next`
— the substrate where `nota-next` blocks become typed schema
declarations.*

*This is a rewrite. The earlier version was wrong on multiple
specifics; the audit catalogue is at
`reports/designer-assistant/381-schema-design-truth-finding-2026-05-27.md`.
Records 874-877, 886-890, 894 (all 2026-05-27, mostly Maximum)
carry the corrected design.*

## Part A — Layer boundary recap

NOTA has no macros. The macro system is a SCHEMA-LAYER mechanism
that operates on the AST `nota-next` produces. See `/376` Part A
for the boundary discipline.

The macro system claims one new NOTA sigil — `$` (with `$*`
derived) — for capture variables. Per record 890 (Medium): `$`
is a candidate; operator shipped it; locked-Maximum vote open.

## Part B — Foundational rule: braces are key/value maps; the namespace is a dynamic enum

Per records 891 and 893 (2026-05-27): **a brace `{...}` in NOTA
is ALWAYS a key/value map** — that's its structural meaning at
the NOTA layer (already stated in `skills/nota-design.md`
§"Map keys"). Inside `{...}`, odd positions are keys and even
positions are values.

The schema's namespace (position 3 of the schema document) is a
brace. Therefore each entry is a key/value pair `Name
TypeDefinition`. Wrapping each entry in parens — `(Name
TypeDefinition)` — is wrong in a brace namespace. It replaces the
brace map's flat key/value stream with a sequence of parenthesis
objects, which is the shape psyche corrected.

**The conceptual model**: the namespace IS a DYNAMIC ENUM. Each
type name is a variant tag; each type definition is the variant's
payload. The enum is APPEND-ONLY in the Cap'n Proto style — new
declarations concatenate at the end of the namespace so existing
type positions stay stable. The schema could eventually compile
to a single-byte (or larger) enum tag space with an enum-
upgrading facility — but in the meantime it's stored as a
key/value map for composition convenience. The mental model is
*conceptual* (an enum you could compile to one byte) but the
*storage* is the key/value map.

This rule applies wherever a brace appears in NOTA — same
principle, every brace.

## Part C — The 4-position document

Every schema file is exactly four root NOTA objects:

```
{ <imports> }                            ← position 0: RootImports — brace, key/value map
( <InputName> ( <variants…> ) )          ← position 1: RootInput — parenthesis (Name (variants))
( <OutputName> ( <variants…> ) )         ← position 2: RootOutput — same shape
{ <namespace> }                          ← position 3: RootNamespace — brace, key/value map
```

Positions 0 and 3 are BRACES (key/value maps per Part B);
positions 1 and 2 are PARENTHESES (case-1 enum variants in NOTA
grammar terms; the inner variants block is a nested parenthesis).

### Canonical authored form — `schemas/spirit-min.schema` (post-record-894 target)

```nota
{}
(Input ((Record Entry) (Observe Query)))
(Output ((RecordAccepted RecordIdentifier) (RecordsObserved RecordSet)))
{
  Topic [Text]
  Topics [Topic]
  Description [Text]
  RecordIdentifier [Integer]
  Entry [Topics Kind Description Magnitude]
  Query [Topic Kind]
  RecordSet [Entry]
  Kind (Decision Principle Correction Clarification Constraint)
  Magnitude (Minimum VeryLow Low Medium High VeryHigh Maximum)
}
```

**Implementation status:** `schema-next`, `schema-rust-next`, and
`spirit-next` now use this pair-only namespace form. `schema-next`
also rejects the old one-entry parenthesized namespace form in a
Nix-checked regression test.

### Position 0 — imports `{…}`

Brace map of `LocalName SchemaSource` pairs. `{}` for no imports.
Engine path: `RootImportsMacro` (`engine.rs:281-321`). This
position has always been pair-style; no migration needed here.

### Positions 1 and 2 — root enums

```
(Input ((Record Entry) (Observe Query)))
```

Two children inside the outer paren: NAME (PascalCase atom) +
NESTED-VARIANTS-BLOCK (parenthesised list). Variants live in the
NESTED parenthesis as the SECOND child of the root enum.

Each variant inside the nested block:
- Unit variant: bare PascalCase (e.g. `Decision`)
- Payload-carrying: `(VariantName PayloadType)` (e.g. `(Record Entry)`)

Variants stay in PARENS (not braces) because the variant
sequence is mixed-shape — some unit, some payload-carrying — and
unit variants have no value to pair with. A brace would force
every variant to declare a payload; a paren list lets unit and
payload variants coexist.

The engine path for the nested-variant lowering is
`RootEnumBlock::variants_from_nested_enum` (`engine.rs:545-551`);
it delegates the inner block to the `SchemaEnumVariants`
declarative macro at the `EnumVariants` position.

### Position 3 — namespace (pair-style only per records 891 and 893)

```nota
{
  Topic [Text]                                                  ← Newtype (single-field struct)
  Entry [Topics Kind Description Magnitude]                     ← multi-field Struct
  Kind (Decision Principle Correction Clarification Constraint) ← Enum (unit variants)
  TypeDeclaration ((Struct StructDeclaration) (Enum EnumDeclaration))  ← Enum (payload variants)
}
```

Each entry is `Name TypeDefinition` — two tokens at the map level.
The `TypeDefinition`:

- `[...]` square bracket → struct (1 field = Newtype; multi-field
  = Struct)
- `(...)` parenthesis → enum (children are unit variants or
  `(VariantName Payload)` payload-carrying)

The parenthesized `(Name body)` namespace entry form is rejected
per records 891 and 893.

## Part D — Truth source: `schemas/root.schema`

The schema is self-describing. Per record 877 (Maximum),
`schemas/root.schema` is the canonical reference. In pair-style
target form:

```nota
{}
(Input ())
(Output ())
{
  Schema [Imports Input Output Namespace]
  Imports [ImportDeclaration]
  Namespace [TypeDeclaration]
  ImportDeclaration [Name TypeReference]
  TypeDeclaration ((Struct StructDeclaration) (Enum EnumDeclaration) (Newtype StructDeclaration))
  StructDeclaration [Name Fields]
  Fields [FieldDeclaration]
  FieldDeclaration [Name TypeReference]
  EnumDeclaration [Name Variants]
  Variants [VariantDeclaration]
  VariantDeclaration [Name Payload]
  Payload (Unit (Carries TypeReference))
  TypeReference [Name]
  Name [Text]
}
```

Reading this top to bottom: `Schema` is a struct with four named
fields; `Imports` is a list of `ImportDeclaration`s; each
`TypeDeclaration` is an enum with three variants (Struct, Enum,
Newtype) each carrying a declaration; and so on down to `Name`
being a newtype around `Text`.

## Part E — The seven `MacroPosition` slots

`schema-next/src/macros.rs:9-17`:

```rust
pub enum MacroPosition {
    RootImports,
    RootInput,
    RootOutput,
    RootNamespace,
    NamespaceDeclaration,
    StructFields,
    EnumVariants,
}
```

Seven structural slots. Every position in a schema document is
one of these seven.

## Part F — Two macro layers, 8 macros total

The engine registers TWO layers of macros at startup
(`engine.rs:233-244`):

### Layer F.1 — Rust hand-coded macros (4)

1. **`RootImportsMacro`** at `RootImports` — matches `{...}`
   brace; iterates as pairs; produces `Imports`.
2. **`RootEnumMacro("RootInput", …)`** at `RootInput` — matches
   `(Name (variants…))`; produces `RootEnum`.
3. **`RootEnumMacro("RootOutput", …)`** at `RootOutput` — same
   shape, at RootOutput.
4. **`RootNamespaceMacro`** at `RootNamespace` — matches `{...}`
   brace; iterates as pairs only; produces `Types`. Each pair lowers
   through `NamespaceDeclaration` to a `Type`.

These four are Rust because they handle the fixed root positions
the engine must process even before any user-declared macros
load.

### Layer F.2 — Declarative macros loaded from a schema file (4)

The engine loads `schemas/builtin-macros.schema` via
`include_str!` (`declarative.rs:15-17`), parses it as NOTA, and
registers each `(SchemaMacro …)` declaration as a
`DeclarativeSchemaMacro`:

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

5. **`SchemaStructDefinition`** at `NamespaceDeclaration` —
   matches a key/value entry whose key is some `$Name` and whose
   value is `[$*Fields]` (square bracket of fields). Expands to
   `(Type (Struct $Name [$*Fields]))`.
6. **`SchemaEnumDefinition`** at `NamespaceDeclaration` — same
   key shape but value is `($*Variants)` (paren = enum). Expands
   to `(Type (Enum $Name ($*Variants)))`.
7. **`SchemaStructFields`** at `StructFields` — matches
   `[$*Fields]`; expands to `(Fields $*Fields)`.
8. **`SchemaEnumVariants`** at `EnumVariants` — matches
   `($*Variants)`; expands to `(Variants $*Variants)`.

### Pattern handling — namespace pairs

`declarative.rs:192-209` `matches_pair`: a pair pattern is a 2-
child parenthesis. The first child matches against the pair's
KEY (e.g. `$Name` binds to `Entry`); the second against the
pair's VALUE (e.g. `[$*Fields]` matches `[Topics Kind
Description Magnitude]`). The pattern `($Name [$*Fields])`
written in the macro definition IS this 2-child paren. That
pattern is the macro's internal pair pattern; it does not make
`(Entry [Fields])` a valid authored namespace entry.

Post-record-894 the engine iterates only key/value pairs from the
namespace; the macro patterns continue to work unchanged.

## Part G — Declarative macro declaration shape

```
(SchemaMacro <Name> <Position> <Pattern> <Template>)
```

Five positional fields (`declarative.rs:82`):

- **Name** (PascalCase) — the macro's name.
- **Position** (PascalCase) — one of the 7 `MacroPosition`
  variants.
- **Pattern** — NOTA expression with capture variables;
  determines whether the macro matches.
- **Template** — NOTA expression with capture variables; expanded
  after match, re-parsed as NOTA, lowered through the registry.

## Part H — Capture variables

Two forms (`declarative.rs:430-454`):

- **`$Name`** — single capture. Binds to one NOTA block.
- **`$*Name`** — rest (repeated) capture. Binds to a list of
  zero-or-more NOTA blocks.

Per record 890 (Medium): `$` is the candidate sigil; operator
shipped it; locked-Maximum vote open.

## Part I — How a declarative macro fires

For one namespace pair `Entry [Topics Kind Description
Magnitude]` (pair-style):

1. `RootNamespaceMacro` walks the namespace brace; iterates as
   pairs. Builds `MacroPair { name: &Entry, definition:
   &[Topics Kind Description Magnitude] }`.
2. `registry.lower(MacroObject::Pair(pair),
   NamespaceDeclaration, …)` — first-match-wins scan.
3. `SchemaStructDefinition.matches`: position matches; pair
   pattern `($Name [$*Fields])` tested. `$Name` binds to
   `Entry`; `[$*Fields]` matches the square bracket;
   `$*Fields` binds to `[Topics, Kind, Description, Magnitude]`.
4. `SchemaStructDefinition.lower`: text-level substitute
   bindings into template `(Type (Struct $Name [$*Fields]))` →
   `(Type (Struct Entry [Topics Kind Description Magnitude]))`.
5. Re-parse the expanded text as a `Document`
   (`declarative.rs:592`). Single root object.
6. `AssembledTemplate.lower`: head is `Type`, dispatch to
   `AssembledType.lower_struct`.
7. `AssembledType.lower_struct`: name is `Entry`; body is
   `[Topics Kind Description Magnitude]`. Recursively call
   `registry.lower(body, StructFields, …)`.
8. `SchemaStructFields.matches`: position matches; pattern
   `[$*Fields]` matches the square bracket; `$*Fields` binds to
   the 4-element list.
9. `SchemaStructFields.lower`: expand template `(Fields
   $*Fields)` → `(Fields Topics Kind Description Magnitude)`.
   Dispatch as AssembledTemplate; head `Fields`; produces
   `Vec<FieldDeclaration>` via `AssembledFields`.
10. Back in `lower_struct`: 4 fields → `TypeDeclaration::Struct`
    (1 field would be `TypeDeclaration::Newtype`).

Three macros fired (`RootNamespaceMacro` plus the two
declaratives `SchemaStructDefinition`, `SchemaStructFields`);
two registry recursions; one typed `Type` output.

## Part J — The closed `MacroOutput` set

`schema-next/src/macros.rs:142-151`:

```rust
pub enum MacroOutput {
    Asschema(Asschema),
    Imports(Vec<ImportDeclaration>),
    RootEnum(EnumDeclaration),
    Types(Vec<TypeDeclaration>),
    Type(TypeDeclaration),
    Fields(Vec<FieldDeclaration>),
    Variants(Vec<EnumVariant>),
    References(Vec<TypeReference>),
}
```

Mismatched output (e.g. `EnumVariants` macro returning `Fields`)
→ `UnexpectedMacroOutput { macro_name, expected }`.

## Part K — Assembled-template heads

When a declarative macro's template re-parses, the head atom
determines lowering (`declarative.rs:629-643`):

- **`Type`** → `AssembledType` → Struct / Enum / Newtype.
- **`Fields`** → `AssembledFields` → `Vec<FieldDeclaration>`.
- **`Variants`** → `AssembledVariants` → `Vec<EnumVariant>`.

Three templates the engine knows how to consume.

## Part L — Bootstrap order

1. Construct `MacroRegistry::new()`.
2. Register 4 Rust macros (RootImports, RootInput, RootOutput,
   RootNamespace).
3. `include_str!` `builtin-macros.schema`, parse, register each
   as `DeclarativeSchemaMacro`.

User schemas can be lowered after step 3. Chicken/egg resolved:
the 4 Rust macros handle the root positions; the 4 declarative
macros handle the inner three positions where extensibility
lives.

## Part M — Dispatch trace (post-correction)

For `schemas/spirit-min.schema` in pair-style form,
`tests/lowering.rs:275-301` asserts the macro sequence:

- `RootImports`
- `RootInput` → `SchemaEnumVariants`
- `RootOutput` → `SchemaEnumVariants`
- `RootNamespace`
  - `SchemaStructDefinition` → `SchemaStructFields` (7×: Topic,
    Topics, Description, RecordIdentifier, Entry, Query,
    RecordSet)
  - `SchemaEnumDefinition` → `SchemaEnumVariants` (2×: Kind,
    Magnitude)

## Part N — Open / drifted / in-flight

- **Pair-style sweep** (records 891, 893, 892): implemented in
  `schema-next` commit `8c821cba`, `schema-rust-next` commit
  `b5a851a1`, and `spirit-next` commit `8ef16bc5`. The engine no
  longer has the parenthesized namespace compatibility branch.
- **Schema module slice** (records 895-898): implemented in
  `nota-next` commit `1c11876b`, `schema-next` commit `807c5250`,
  `schema-rust-next` commit `5ca1c964`, and `spirit-next` commit
  `e004fc62`. Colon-qualified schema names parse as symbols, packages
  load `schema/lib.schema`, generated Rust paths mirror schema module
  identity under `schema/...rs`, and the Spirit pilot loads its schema
  through the package entry point.
- **`$` capture sigil Maximum-vote** (record 890, Medium):
  operator shipped; psyche has not locked Maximum.
- **MacroPosition from schema vs hardcoded Rust enum**:
  `core.schema` lists positions in NOTA but Rust enum at
  `macros.rs:9-17` is hand-written. Record 886: core schema is
  "required as a tested artifact: does not have to be load-
  bearing for the reader yet." Bootstrap tension still open.
- **Append-only namespace evolution** (record 892): new
  declarations concatenate at the end; existing positions stable;
  eventual compile to enum tag space requires an enum-upgrading
  facility. Forward-looking; no current code.
- **`signal-frame/schema/signal-frame.concept.schema`** is a
  draft (concept suffix). Not the truth source.
- **Feature branch `designer-finish-macro-engine-2026-05-26`**
  (commit `bc7dc05c`) — older shape; records 888/889 supersede
  that direction.
- **Same-principle extension to enum variants?** — Variants are
  currently in PARENS not braces. The brace-is-key/value rule
  doesn't cleanly apply because unit variants have no payload
  to pair with. Worth a psyche call if extending the rule there
  is desired.

## Part O — Verification anchors

| Claim | File / Line |
|-------|-------------|
| Brace is always key/value map | `skills/nota-design.md:236-247` + records 891 and 893 |
| 4-position document shape | `schema-next/src/engine.rs:146-150` |
| Variants nested in 2nd-position paren | `engine.rs:545-551` |
| Pair-style is canonical namespace | records 891 and 893 |
| 7 MacroPosition variants | `schema-next/src/macros.rs:9-17` |
| 4 Rust macros registered first | `engine.rs:233-236` |
| 4 declarative macros loaded from schema | `engine.rs:239-242` + `declarative.rs:15-17` |
| `(SchemaMacro Name Position Pattern Template)` shape | `declarative.rs:82` |
| `$` / `$*` capture forms | `declarative.rs:430-454` |
| Template expansion: text-level then re-parse | `declarative.rs:587-605` |
| AssembledTemplate heads | `declarative.rs:629-643` |
| Truth source for syntax | `schema-next/schemas/root.schema` per record 877 |
| Dynamic-enum / cap-n-proto framing | record 892 |
| Critical psyche records | 874, 875, 876, 877, 886, 887, 888, 889, 890, 894 (all 2026-05-27) |

## What's next in the tour

Report 3 — schema-rust-next — Rust emission from the lowered
Asschema. Methods-on-non-ZST applied to emitted types. build.rs
build-time emission. Nix checks enforcing the rule.

When ready: "next."
