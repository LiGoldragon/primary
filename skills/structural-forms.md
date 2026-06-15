# Skill — Structural Forms

*A language is a set of structural macros kept as data. A file is a typed tree
matched by shape; the grammar is a type; the type is the parser. This is how the
nota/schema stack is designed, and the discipline for authoring it.*

## The idea

`if`, a function call, a struct, generics — every construct of a language is a
*shape* the compiler recognizes. Conventional languages keep that set of shapes
frozen and poorly-saved inside the compiler. Here the set is kept as **data**:
typed `#[shape(...)]` node definitions, recognized by form, recursively. That
makes the language open (a new construct is new data, not a compiler change) and
far easier for an LLM to read, write, and reason about. Per Spirit `7c71`
(Principle, VeryHigh): [a language is a set of structural macros; keep the set as
data so it is open and LLM-legible]; `2zed`: [everything is data conforming to a
schema-defined type; a macro is a value of a struct]; `my86`: [the file is a
typed tree of nodes; the grammar is the type, with no hand-written parser].

Only a **tiny seed** stays hand-written: the NOTA block parser plus one derive.
Everything above the seed is data or derived. (Concept: report `627`.)

## The shape vocabulary (the nota-next derive)

`#[derive(StructuralMacroNode)]` turns a `#[shape(...)]`-tagged type into a
matcher + decoder + encoder. It covers **enums** (each variant a shape) and
**structs** (a positional typed body). The seven shapes:

| `#[shape(...)]` | matches | fields |
|---|---|---|
| `pascal_atom` | a PascalCase atom `Topic` | 1 |
| `keyword = "X"` | the literal atom `X` | 0 |
| `head = "H", arity = N` | `(H a …)` fixed count | N-1 |
| `head = "H", atom` | `(H 32)` head + one atom (via `FromStr`) | 1 |
| `head = "H", body` | `(H a b …)` any count | 1 (a body) |
| `pascal_head, arity = N` | `(Foo a …)` captured head, fixed | N |
| `pascal_head, body` | `(Foo a b …)` captured head, any count | 2 (head + body) |

`head` takes exactly one of `arity`/`body`/`atom`; `pascal_head` exactly one of
`arity`/`body`. Enum variants may carry **named** fields (`Apply { head,
arguments }`) or positional tuple fields, mapped to shape captures by declaration
order. A **struct** derives one positional body — `structural_variants()` is
empty, the candidate's blocks decode straight into the fields in order — the
derived replacement for hand-written body readers like schema-next `SchemaMacro`.

## Positional struct syntax (Spirit `adnn`)

Per Spirit `adnn` (Decision): [schema struct declarations are positional lists of
types, mirroring how the data reads in NOTA, not name-value pairs; the field name
is derived from the type by default; a field needing an explicit name uses the
dot-prefix differentiator `key.TypeReference`; the name-value form and the `*`
shorthand are retired].

```
Entry { Topics Kind Description }          ;; bare types — names derived
ImportDeclaration { Name source.TypeReference }   ;; dot differentiator
Namespace { declaration (Vector Declaration) }    ;; lowercase names a composite
Detail { Field { String } }                ;; PascalCase + block = inline decl
```

The retired `field Type` name-value form and `*` shorthand are **rejected loudly**
in both lowering paths (`SchemaError::RetiredStructFieldSyntax`): a bare
struct-field atom must name a type (PascalCase or scoped), else use `field.Type`.

## The dimensional principle (Spirit `ov30`)

Per Spirit `ov30` (Principle, High): [a struct field's role is its type, so no
struct has two fields of the same type; distinct roles are distinct types
(dimensional correctness — Height and Width are both metres yet cannot be
interchanged or multiplied as alike); repetition is a keyed collection (a
`Vector` is a `Map` over an ordinal index), never repeated fields; field-name
equals type-name is the default, and an explicit field name signals a missing
type or a collection]. This is the [newtype per domain value] rule
(`skills/abstractions.md`) pushed to its endpoint: **a newtype per role**. Full
type-level enforcement is aspirational; the principle guides design now. (Report
`639`.)

## Streams and families are NOT structs

A `(Stream { token T opened S … })` or `(Family { record E table t key K })` is
**not** a positional struct — it is a *closed typed record* with a fixed, closed
set of keyword-selected slots holding **heterogeneous** values (a family's
`record` is a type, `table` is a name literal, `key` is a `FamilyKey` enum). The
keyword form is correct here, not a migration gap; the positional struct rule
does not apply and these must not be "positionalized". (Report `645`.)

## The self-host boundary

The derive automates the *shape* layer. Meaning stays hand-written: a
`TypeReference`'s top-level decode is registry- and context-aware (declared
macros, inline declarations) — a permanent border, not a seed to shrink.
`TypeReference` has exactly one codec (the structural-macro grammar: built-in
head fast path + the `pascal_head, body` `ApplicationNode` seam + the
`head="Bytes", atom` `HeadedAtom` seam); `NotaDecode`/`NotaEncode` are thin
delegators. The honest rule: keep the seed small; each remaining hand-written
seam is shape↔meaning boundary, not debt. (Reports `631`, `635`.)

## See also

- Concept + naming: `reports/designer/627`. Dimensional principle:
  `639`. Positional syntax: `640`/`643`. Streams/families: `645`.
- Intents: `7c71` `2zed` `my86` `wqdi` (thesis); `ov30` (dimensional principle);
  `adnn` (positional syntax).
- `skills/abstractions.md` (newtype-per-role endpoint), `skills/nota-design.md`
  (NOTA records; defers struct-body grammar here), `skills/component-triad.md`.
- Code: nota-next `derive/src/lib.rs`, schema-next `src/declarative.rs` +
  `src/schema.rs` (epic branch `next/structural-forms`).
