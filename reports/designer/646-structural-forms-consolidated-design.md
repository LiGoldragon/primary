# Structural Forms — the consolidated design

One document for the whole structural-forms design arc, agglomerating reports
`627` and `631`–`645` (those remain as the detailed record). It ends with the
synthesis the dialogue reached: **universal positional syntax**, and what it
takes to get there.

## 1. The thesis — a language is data

A programming language is a set of *shapes*. Conventional languages freeze that
set inside the compiler; here it is kept as inspectable, typed **data**. A file
is a typed tree of nodes matched by shape, recursively — the grammar is a type,
the type is the parser. Only a tiny **seed** stays hand-written (the NOTA block
parser + one derive); everything above is data or derived. This makes the
language open (a new construct is new data) and LLM-legible. The same value has
three faces — NOTA (text), schema (type), rkyv (bytes). *Spirit `7c71` (the
thesis), `2zed` (everything is data; a macro is a struct value), `my86` (the file
is a typed tree). Detail: report `627`.*

## 2. The shape vocabulary — the `StructuralMacroNode` derive

`#[derive(StructuralMacroNode)]` turns a `#[shape(...)]`-tagged type into a
matcher + decoder + encoder, for **enums** (each variant a shape) and **structs**
(a positional typed body). Seven shapes:

| `#[shape(...)]` | matches | fields |
|---|---|---|
| `pascal_atom` | `Topic` | 1 |
| `keyword = "X"` | literal `X` | 0 |
| `head = "H", arity = N` | `(H a …)` fixed | N-1 |
| `head = "H", atom` | `(H 32)` head + atom | 1 |
| `head = "H", body` | `(H a b …)` any | 1 body |
| `pascal_head, arity = N` | `(Foo a …)` fixed | N |
| `pascal_head, body` | `(Foo a b …)` any | 2 (head + body) |

Enum variants carry positional **or named** fields (`Apply { head, arguments }`),
mapped to shape captures by declaration order. A struct derives one positional
body — the derived replacement for hand-written body readers. *Detail: `635`,
`636`. Code: nota-next `derive/src/lib.rs`.*

## 3. `TypeReference` and the self-host boundary

`TypeReference` (a type at a field/payload position) has one codec — the
structural-macro grammar: a built-in-head fast path (`Vector`/`Optional`/
`ScopeOf` arity-2, flat `(Map K V)`, `(Bytes N)` via the `HeadedAtom` seam) plus
the `pascal_head, body` `ApplicationNode` seam for the generic `(Foo A B)` form;
`NotaDecode`/`NotaEncode` are thin delegators; thiserror errors. But its
*top-level* decode is **registry- and context-aware** (declared user macros,
inline `|(…)|` declarations that mutate context) — which a pure derive cannot
model. So the hand-written delegating impl is the **permanent boundary between
shape and meaning**, not a seed to shrink. *Detail: `631` (reconciliation), `635`
(the registry finding that corrected `631`), `637` (TypeReference from the ground
up).*

## 4. Positional struct syntax (Spirit `adnn`)

A schema struct body is a **positional list of types**, mirroring how the data
reads in NOTA — not name-value pairs:

```
Entry { Topics Kind Description }          ;; bare types — names derived
ImportDeclaration { Name source.TypeReference }   ;; dot differentiator
Namespace { declaration (Vector Declaration) }    ;; lowercase names a composite
Detail { Field { String } }                ;; PascalCase + block = inline decl
```

The field name derives from the type by default; a field whose name differs uses
the `key.TypeReference` dot-differentiator. The `*` shorthand and the name-value
form are **retired and rejected loudly** (`SchemaError::RetiredStructFieldSyntax`)
in both lowering paths. *Detail: `638`, `640` (separator decision), `642`
(migration spec), `643` (landed, 159 tests), `644` (the reject, operator audit
`380`). Settled separator: `key.TypeReference`, dot, name-first.*

## 5. The dimensional principle (Spirit `ov30`)

> A struct field's role is its type, so no struct has two fields of the same
> type. Distinct roles are distinct types — **dimensional correctness**: `Height`
> and `Width` are both metres yet cannot be interchanged or multiplied as alike.
> Repetition is a keyed collection (a `Vector` is a `Map` over an ordinal index),
> never repeated fields. Field-name equals type-name by default; an explicit name
> signals a missing type or a collection.

This is "newtype per domain value" pushed to its endpoint: **a newtype per
role**. It is the units-of-measure idea generalized to every semantic role. Full
type-level enforcement is aspirational; the principle guides design now. *Detail:
`639`.*

## 6. Closed typed records — and the family-identity newtype

A `Stream { token T … }` or `Family { record E table t key K }` is a **closed
typed record**: a fixed set of keyword-selected slots holding role-specific
values. A family's slots are heterogeneous *kinds* — `record` is a type,
`table` is a `TableName` literal, `key` is a `FamilyKey` enum. (`645` framed
these as a construct distinct from structs — §7 refines that.)

A family's **identity** is its name plus its schema-closure hash. That hash is
now emitted as a **typed `SchemaHash` named newtype** end-to-end — schema-next
computes it, schema-rust-next emits `pub const … : SchemaHash = SchemaHash::new(…)`
(not a raw `[u8; 32]` re-wrapped downstream), sema-engine stores it — single-
sourced on the one sema type, no anonymous bytes. *The type carries the meaning
(`ov30`). Branch `next/family-identity-newtype`, schema-rust-next, 86 tests
green.*

## 7. The synthesis — universal positional syntax

The dialogue's conclusion, and a **correction to `645`**: with the named-newtype
discipline applied, there is **one rule**, and it unifies everything —

> A record is written as a positional list of typed values, with no keyword
> labels, **whenever every slot is a distinct named type.** The types carry the
> meaning; position (or type-indexing) resolves each value to its slot.

This is the dimensional principle (`ov30`) read as a *syntax*. It dissolves the
struct-vs-closed-record split:

- **Families already qualify.** `record` (a `TypeReference`), `table` (a
  `TableName`), `key` (a `FamilyKey`) are three **distinct named types**, so
  `(Family StoredRecord records Domain)` is unambiguous without keywords — the
  named newtypes `TableName`/`FamilyKey` (which already exist) make the positions
  self-describing. `645`'s "families can't be positionalized" was too strong: they
  can't use the *field-name=type-name* form (a table value isn't a type), but they
  **can** be a type-indexed positional record. The keyword form was convenience
  (labels + order-independence), not necessity.
- **Streams need one newtype.** `token` and `close` are **both** `SourceReference`
  — the same type in two roles, the one place that *violates* the rule. Make them
  distinct types (`OpenToken` / `CloseToken`, the dimensional principle's own
  prescription) and streams become universal-positional too.
- **The hash is an instance.** Emitting the family identity as a `SchemaHash`
  newtype (§6) is exactly "make every value a named type" — the prerequisite for
  a self-describing positional record that carries a hash.

So universal positional syntax is reachable, governed by a single principle, and
the remaining work is purely **newtyping the few raw or shared-type slots**: the
hash → `SchemaHash` (done); stream `token`/`close` → distinct types (open). The
honest trade: positional drops the keyword labels' readability and order-
independence — which is acceptable precisely because, under the rule, the *types*
restore both (each value names its own role).

## 8. State and next slices

- **nota-next `next/structural-forms`** — leaf shapes + named-field + struct
  derive (74 tests); docs refreshed (`7547247e`).
- **schema-next `next/structural-forms`** — TypeReference reconciliation +
  positional syntax + retired-syntax reject (161 tests); docs refreshed
  (`51289bc5`).
- **schema-rust-next `next/family-identity-newtype`** — `SchemaHash` named-newtype
  emission (86 tests, `86a346fe`).
- **Workspace** — `skills/structural-forms.md` (indexed), INTENT.md thesis +
  dimensional subsections, `nota-design.md`/`abstractions.md` aligned; Spirit
  `ov30` + `adnn` recorded.
- **Open, ordered:** stream `token`/`close` as distinct types (unlocks
  universal-positional for streams); positionalize the family/stream declaration
  syntax (drop keyword forms once every slot is a distinct named type); finish
  single-sourcing the closure hash (`ContentHash` ↔ `SchemaHash`); operator
  integration of the three epic branches; the `SchemaMacro` struct-derive
  retirement.
