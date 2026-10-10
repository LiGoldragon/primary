# Canonical NOTA / Schema Syntax — Source-Backed Map

Read-only grounding for the four schema-language syntax questions. Every claim
is cited to `file:line` in source truth. Observations (what the grammar/parser
actually does) are separated from interpretation.

## Scope and sources consulted

- Grammar / parser / lowering (definitive): `schema-next`
  - `src/declarative.rs` — struct-field and enum-variant lowering
  - `src/schema.rs` — arity + variant-payload validation (the `schema-next` guard)
  - `src/engine.rs` — `SchemaError` definitions and messages
  - `schemas/reference-grammar.nota` — parenthesis-reference dispatch precedence
- Doctrine: `LiGoldragon/skills/modules/nota-design/full.md`,
  `.../nota-schema-docs/full.md`
- Real `.schema` worked examples: `schema-next/schemas/core.schema`,
  `schema-next/tests/fixtures/specified-ir.schema`,
  `signal-spirit/schema/signal.schema`, `signal-mentci/schema/lib.schema`,
  `signal-spirit/schema/domain.schema`

All repo paths are under `/git/github.com/LiGoldragon/`.

## Item 1 — Named brace-record fields: it is a DOT (`name.Type`)

**Canonical form (observation):** inside a brace struct body `{ ... }`, a field
whose name differs from its type binds the field name to the type with a
literal `.` (dot). There is NO space form and the parenthesized-pair form is
retired (see below). Two spellings of the dot form exist:

- `name.Type` — both simple PascalCase symbols, one atom split on the first `.`.
- `name.(Type args...)` — parenthesized/native type; the field-name atom carries
  a trailing `.` immediately before the open paren. This is exactly the
  `retries.(Optional Count)` shape asked about.

A field whose name equals the (snake-case of the) type is written bare, just the
PascalCase type; adding an explicit `name.Type` where they match is a
`RedundantExplicitFieldRole` error.

**Grammar rule that proves the dot binding:**

- Inline dot form: `src/declarative.rs:1834` — `if let Some((field_name,
  type_name)) = text.split_once('.')` then `explicit_dot_field(...)`
  (`src/declarative.rs:1859`). The field-name atom is split on the first `.`.
- Trailing-dot form for parenthesized types: `src/declarative.rs:1766` —
  `let Some(field_name) = text.strip_suffix('.')`, then the NEXT object is taken
  as the type reference (`src/declarative.rs:1774-1785`,
  `explicit_trailing_dot_field`). This is what parses `name.(Optional Count)`:
  the atom `name.` (trailing dot) followed by the list `(Optional Count)`.
- Authoritative error text stating the two legal forms:
  `src/engine.rs:72-75` — `RetiredStructFieldSyntax`: *"struct bodies are
  positional field types, use TypeName or field_name.TypeName"*.

**Real cited examples (dot form):**

- `schema-next/schemas/core.schema:15` —
  `MacroPatternDelimited { delimiter.MacroDelimiter MacroPatternObjects }`
  (`delimiter.MacroDelimiter` is dot-bound; `MacroPatternObjects` is the bare
  name==type form).
- `schema-next/tests/fixtures/specified-ir.schema:9` —
  `Entry { domains.(Vector Domain) Kind Description ... }`
- `schema-next/tests/fixtures/specified-ir.schema:11` —
  `Query { filter.DomainMatch limit.(Optional Integer) }`
  (both spellings: simple `filter.DomainMatch` and parenthesized
  `limit.(Optional Integer)`).
- `signal-spirit/schema/signal.schema:134` —
  `VerbatimQuote { QuoteText OptionalAntecedent.(Optional Antecedent) }`
  (a live production `name.(Optional T)` field — the requested shape).
- `signal-spirit/schema/signal.schema:140` —
  `ReferentRegistration { Referent aliases.Referents Justification }`
- `signal-mentci/schema/lib.schema:159-160` — `label.ContextLabel` /
  `body.ContextBody`.

**In-repo doctrine statement (matches the parser):**
`signal-mentci/schema/lib.schema:60` — *"a field whose name differs from its type
is written field.Type (dot form)"*; `:65` — *"The retired two-atom  field Type
pair no longer lowers."*

**Answer to the explicit question:** the named-field form is **`name.(type)` /
`name.Type` — DOT-bound**, not a space and not a parenthesized `(name Type)` pair.
The dot is the binder.

## Item 2 — Positional record components

**Canonical form (observation):** a record is a parenthesized list
`(Head component1 component2 ...)`. Components are whitespace-separated objects
in declared order; the head is typically the type/variant tag. There are no
field names in the value/positional form — names live in the schema. NOTA is
**strict positional**: every declared component always appears in the text form.

- Doctrine: `nota-design/full.md:7` — *"Records are positional. Field order is
  part of the interface; reordering fields is a compatibility change."*
- Doctrine: `nota-design/full.md:21` — *"every positional component ... always
  appears in the text form."*
- Struct bodies are themselves positional field lists (interpretation of the
  doc comment): `src/declarative.rs:1792` — *"Strict struct bodies are positional
  lists."*

**Real cited examples:**

- `signal-spirit/schema/domain.schema:66` —
  `(Equivalence [(Information Database) (Technology Software Data All)])`
  where `(Information Database)` and `(Technology Software Data All)` are
  positional records (2 and 4 components, no names).
- Pseudo-NOTA doc form: `nota-schema-docs/full.md:11` —
  `(Bug <title> <description> <severity> <incident-at?> <reproduction?>)`
  (head `Bug` + positional components; `?` marks documentation-only optionality,
  not a wire feature).

## Item 3 — Variant payloads: `(VariantName Payload)`

**Canonical form (observation):** inside an enum body `[ ... ]`, a variant is
either a bare PascalCase symbol (no payload) or a parenthesized
`(VariantName PayloadType)` where the head atom is the variant name and the
following component is the payload type reference.

**Grammar rule that proves it** (`src/declarative.rs`, `MacroExpansionVariant`):

- `src/declarative.rs:2050-2051` — bare PascalCase symbol → `EnumVariant::new(name,
  None)` (no payload).
- `src/declarative.rs:2074-2085` — parenthesis holding 2 objects → variant named
  by object 0, payload = `type_reference` of object 1. This is the
  `(Data DataLeaf)` shape.
- `src/declarative.rs:2062-2073` — parenthesis holding 1 object `(Name)` → variant
  `Name` with payload derived from the name itself (`TypeReference::from_name`).
- `src/declarative.rs:2086-2101` — 4-object form adds a stream relation
  (`opens`/`belongs`); an advanced variant, still `(Name Payload keyword Stream)`.

**Real cited examples:**

- `schema-next/schemas/core.schema:14` — `MacroPatternObject [(Capture
  MacroCaptureName) (RestCapture MacroCaptureName) (Atom MacroAtom) (Delimited
  MacroPatternDelimited)]` — four `(VariantName PayloadType)` variants.
- `signal-spirit/schema/domain.schema:41` — `(Data DataLeaf)` (the exact form
  in the brief).
- `signal-spirit/schema/domain.schema:32` — `(Hardware HardwareLeaf)`;
  `:33` — `(Software)` (single-object payload-from-name form);
  `:29` — `(Technology)`.

## Item 4 — Where `(Optional T)` is legal vs not

**Observation — legal:** `(Optional T)` is legal as a **named brace-record
field** type (and nests inside other references). The arity checker accepts
`Optional` as an ordinary parameterized reference: `src/schema.rs:862-863`
(`TypeReference::Optional(inner) => self.verify_reference_arities(inner)`). The
field-lowering doc comment lists it explicitly:
`src/declarative.rs:1796-1798` — *"`(Optional Topic)` lower to ... optional
references."*

- Live example: `signal-spirit/schema/signal.schema:134` —
  `OptionalAntecedent.(Optional Antecedent)`; and
  `specified-ir.schema:11` — `limit.(Optional Integer)`.

**Observation — illegal (the `schema-next` guard):** `(Optional T)` is NOT legal
as an **enum-variant payload**, nor (per doctrine) as a bare positional/variant
slot. The guard:

- `src/schema.rs:837-849` (`verify_enum_arities`): for each variant payload,
  `if matches!(payload, TypeReference::Optional(_))` → returns
  `SchemaError::OptionalVariantPayload { enum_name, variant_name }`
  (`src/schema.rs:840-845`).
- Error definition + message: `src/engine.rs:78-84` —
  *"a variant payload must always appear in the text form, so (Optional T) is
  forbidden here — model the optional case as an explicit member carrying a
  required payload (for example a leaf enum with an explicit All member)."*
- Test witness: `schema-next/tests/lowering.rs:229` asserts
  `SchemaError::OptionalVariantPayload`.

**Doctrine agreement:** `nota-design/full.md:21` — *"Never place `(Optional T)`
... in a positional or variant-payload slot. ... `(Optional T)` is legal only as
a named brace-record field, and only when absence means something distinct from
empty."* This exactly matches the code: Optional passes arity everywhere except
the variant-payload position, which the guard rejects.

## Nuance / discrepancy to flag (observation + interpretation)

The composite-field spelling has two live sub-forms and one **retired** form:

- LIVE — explicit name via dot: `field.(Vector X)` / `field.(Optional X)`
  (`explicit_trailing_dot_field`, `src/declarative.rs:1756-1787`).
- LIVE — bare native reference with a *derived* name: `(Vector X)` /
  `(Optional X)` used directly as a field; name derived by
  `derived_name_for_reference` (`src/declarative.rs:1826-1831`, `:1968`).
- RETIRED — the parenthesized pair `(FieldRole (Vector X))` /
  `(retries (Optional Count))`: `explicit_structural_field`
  (`src/declarative.rs:1914-1945`) and `is_explicit_field_pair`
  (`src/declarative.rs:1947-1959`) both raise `RetiredStructFieldSyntax`.

Interpretation: the in-repo comment `signal-mentci/schema/lib.schema:62-65`
describes the composite form as `(FieldRole (Vector X)) / (FieldRole (Optional
X))`. Under current `schema-next` main that pair form is **retired** (it lowers
to `RetiredStructFieldSyntax`); the current canonical spelling is the dot form
`FieldRole.(Vector X)`, as the live schemas actually use
(`signal-spirit/schema/signal.schema:134`). Treat the signal-mentci comment
(dated "past abae95f") as stale relative to the parser. This is the one place
where a doctrine comment and the enforced grammar disagree.

## What was NOT checked

- The `nota-next` grammar/codec crate was not opened; the surface syntax was
  resolved from `schema-next` (the definitive lowering) plus doctrine and live
  `.schema` files, which was sufficient and consistent.
- `tree-sitter-schema` / `tree-sitter-nota` were not consulted; they are editor
  grammars, not the authoritative lowering.
- The instance/value-side dot handling (`src/source.rs:1926`, `:2067`, `:2266`)
  was observed to exist (mirrors the same `name.value` dot convention for
  values) but was not exhaustively read, since the brief targets schema/type
  syntax.
