# 381 — Schema design truth-finding (audit of `/380`)

Read-only triangulation of the current canonical NOTA schema design as of
`schema-next` commit `d340433` (2026-05-27 10:50). The prime designer's
`/380` describes an intermediate state from commit `cc05ecc` (2026-05-27
10:37) — 13 minutes stale, several specific claims wrong.

## 1. Current canonical schema design

### Document shape — 4 root positions

`schema-next/src/engine.rs:146-150` asserts `holds_root_objects() == 4`.
The four positions:

```
{ <imports> }                                ← position 0: RootImports brace map
( <InputName> ( <variants…> ) )              ← position 1: RootInput parenthesis (Name (...))
( <OutputName> ( <variants…> ) )             ← position 2: RootOutput parenthesis (Name (...))
{ <namespace> }                              ← position 3: RootNamespace brace map
```

The variants live in a NESTED parenthesis as the second child, not as
direct trailing children of the root enum.

### Concrete authored source — `schemas/spirit-min.schema` (current)

```nota
{}
(Input ((Record Entry) (Observe Query)))
(Output ((RecordAccepted RecordIdentifier) (RecordsObserved RecordSet)))
{
  (Topic [Text])
  (Topics [Topic])
  (Description [Text])
  (RecordIdentifier [Integer])
  (Entry [Topics Kind Description Magnitude])
  (Query [Topic Kind])
  (RecordSet [Entry])
  (Kind (Decision Principle Correction Clarification Constraint))
  (Magnitude (Minimum VeryLow Low Medium High VeryHigh Maximum))
}
```

### Namespace declarations — named-object form only (in current artefacts)

All shipped `.schema` files use parenthesised `(Name body)` named-object
form. Pair-style is still legal in `engine.rs:400-407` (`uses_named_objects`
check) but no canonical file authors it. `core.schema` and `root.schema`
both use only named-object form.

### Declarative macro file — `schemas/builtin-macros.schema`

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

Declaration shape: `(SchemaMacro <Name> <Position> <Pattern> <Template>)` —
5 positional children (`declarative.rs:82`). Captures: `$Name` single,
`$*Fields` rest. This is in `main`, not just on a feature branch.

### Macros actually registered (`engine.rs:231-244`)

Hand-coded Rust macros: `RootImportsMacro`, `RootEnumMacro("RootInput")`,
`RootEnumMacro("RootOutput")`, `RootNamespaceMacro`. Then 4 declarative
macros loaded from `builtin-macros.schema`:
`SchemaStructDefinition`, `SchemaEnumDefinition`, `SchemaStructFields`,
`SchemaEnumVariants`. Total 8 — not 7.

## 2. Diff against `/380`

| `/380` line | Wrong claim | Actual truth | Source |
|---|---|---|---|
| 22 | `holds_root_objects() == 4` at `engine.rs:127` | At `engine.rs:146-150` | line moved |
| 28-30 | spirit-min Input has `variants[0].name == "Record"` from trailing children | Input has nested-parenthesis variants block; lowering test at `tests/lowering.rs:14-23` proves nesting | `schemas/spirit-min.schema:2` |
| 94-99 | Root enum form `(Input (Record Entry) (Observe Query) …)` with variants as trailing children | Form is `(Input ((Record Entry) (Observe Query)))` — variants nested in a second parenthesis | `engine.rs:545-551` (`variants_from_nested_enum` is now the path) |
| 107-109 | `(Input ())` test at `tests/lowering.rs:47` shows degenerate trailing-variant form | At `lowering.rs:47` the form is `(Input ())` — the empty parens IS the nested variant block, demonstrating nesting, not a degenerate empty trailing list | `tests/lowering.rs:47` |
| 138-147 | "Pair style" namespace shape is a real authoring option | Pair style is still LEGAL but no canonical file uses it; engine path 428-451 exists but is unused by shipped artefacts | `schemas/{core,root,spirit-min}.schema` |
| 171-181 | 7 MacroPosition variants only | The 7 variants ARE correct (`macros.rs:9-17`) — `/380` got this right |  |
| 212-222 | "with_schema_defaults registers 7" | Registers 4 Rust macros + 4 declarative macros = 8 | `engine.rs:231-244` |
| 244-254 | `MacroOutput` has 8 variants | Correct (`macros.rs:142-151`) |  |
| 274-307 | "The seven built-in macros" — lists `TypeDeclarationMacro`, `StructFieldsMacro`, `EnumVariantsMacro` as Rust types | These three Rust types **no longer exist**. Replaced by 4 declarative macros loaded from `builtin-macros.schema`. The diff at commit `d340433` removed them | `git show d340433 -- src/engine.rs` |
| 314-327 | Dispatch trace shows `RootInput → EnumVariants` then `NamespaceDeclaration → StructFields` etc with hand-coded macro names | Actual trace (`tests/lowering.rs:275-301`) shows `RootInput`, `SchemaEnumVariants`, `RootOutput`, `SchemaEnumVariants`, `RootNamespace`, `SchemaStructDefinition`, `SchemaStructFields`, … — declarative macro names dominate | `tests/lowering.rs:275-301` |
| 392-422 | "Feature branch additions" (record 867, filesystem imports, fixed-point, `.asschema` hash) framed as not-on-main | Records 888/889/890 (2026-05-27, High/Medium) supersede 867's broader scope: the macro language must be real and visibly distinct from Rust shape lowering, and capture-sigil binding (`$`/`$*`) is the locked direction. The declarative library on `main` IS this; the feature branch at `bc7dc05c18b4` describes a different (broader) shape | spirit records 888, 889, 890 |
| 392-403 | `(Macro …)` form has unresolved `+` meta-notation | Settled: capture syntax is `$Name` for single, `$*Name` for rest. Declaration head is `SchemaMacro` (not `Macro`). `declarative.rs:69-71`, `tests/lowering.rs:163-178` | `schemas/builtin-macros.schema` |
| 522-526 | `signal-frame.concept.schema` is "drifted, 6-position older shape" | The .concept file is a draft; it's not the truth source. The truth source IS `schemas/root.schema` per record 877 and ARCHITECTURE.md | `schema-next/ARCHITECTURE.md:30-34`, record 877 |

## 3. Open / in-flight design points

- **Pair-style namespace authoring** — engine still accepts it
  (`engine.rs:428-451`) but no shipped schema uses it. Likely candidate
  for removal; no record yet authorises that.
- **`MacroPosition` from schema vs hard-coded enum** — `core.schema:15` lists
  the 7 positions in NOTA, but Rust's `MacroPosition` enum at
  `macros.rs:9-17` is still hand-written. Record 886 says the core schema is
  "required as a tested artifact: it does not have to be load-bearing for the
  reader yet". Bootstrap tension still open.
- **Built-in core schema vs full self-description** — record 887 marks this
  Medium certainty: "schema likely needs a default built-in core schema
  before the full schema self-description". Exploratory.
- **Capture sigil** — record 890 (Medium): `$` is "a candidate" but
  "important constraint is that macro references must be visible". `$Name` /
  `$*Name` shipped in `main` — operator chose the candidate; not yet locked
  Maximum.
- **Macros parameter** — record 883 (Maximum): the upcoming `lojix-horizon`
  rewrite is "schema-deep rewrite on nota-next plus schema-next" — psyche
  authorises modifying schema-next itself.

## 4. Truth source going forward

**Primary truth source for syntax**: `/git/github.com/LiGoldragon/schema-next/schemas/root.schema` — the schema-authored self-description of the root `Schema` type (record 877, Maximum).

**Secondary truth sources**:

- `/git/github.com/LiGoldragon/schema-next/ARCHITECTURE.md` — operator-maintained prose constraints.
- `/git/github.com/LiGoldragon/schema-next/schemas/spirit-min.schema` — minimal worked example.
- `/git/github.com/LiGoldragon/schema-next/schemas/builtin-macros.schema` — declarative macro form.
- `/git/github.com/LiGoldragon/schema-next/schemas/core.schema` — built-in macro positions/shapes/outputs.
- `/git/github.com/LiGoldragon/schema-next/tests/lowering.rs` — executable contract.

**Stale / non-truth sources**:

- `/git/github.com/LiGoldragon/signal-frame/schema/signal-frame.concept.schema` (draft).
- `/home/li/primary/reports/designer/380-bottom-up-tour-02-schema-macros-2026-05-27.md` (this audit).
- Any reference to feature branch `designer-finish-macro-engine-2026-05-26` (commit `bc7dc05c18b4`) — superseded by main per records 888/889.

**Spirit records that lock the design**: 874, 875, 876, 877, 886, 887, 888, 889, 890 (all 2026-05-27).
