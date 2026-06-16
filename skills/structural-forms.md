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

## Streams and families are positional special forms, not structs

Streams and families are **not structs**: they are closed typed records
with fixed heterogeneous slots. The positional struct rule (`FieldName`
derived from type, dot differentiator for named fields) does not apply.

They still use structural positional syntax of their own. The reader
resolves the slots by declared position, not by type identity. Repeated
types are therefore legal when the slots differ by role:

```nota
RecordsFamily (Family StoredRecord records Domain)
IntentEventStream (Stream SubscriptionToken SubscriptionStarted IntentEvent SubscriptionToken)
```

For `Family`, slot 1 is the record type, slot 2 is the lowercase table
literal, and slot 3 is the key kind. For `Stream`, the open and close
tokens are distinct slots even when both have the same concrete type.
Splitting them into `OpenToken` / `CloseToken` newtypes is an optional
later strictness improvement, not a gate for the positional form.
(Reports `645`, `647`, `649`.)

## Pipe delimiters: generics and traits/impls

The pipe delimiter family is assigned as schema-level structural syntax:

```nota
[| text |]             ;; bracket-safe / multiline string
Name (| [T] body |)    ;; generic declaration; params scope the nested body
{| Trait Target |}     ;; trait/impl structural form, simplest marker shape
```

Generic **use** stays ordinary application: `(Head Arg ...)`. A use site
does not take `{| |}` just to say it is generic; the declaration makes
`Head` a known generic, the same way built-in `(Vector T)` is understood.
This keeps `{| |}` assigned to traits/impls.

An impl is one pipe-brace object, never a map key/value split. Anything
scoped by binders must live inside the same structural object. The
matcher may structurally sugar the optional ends:

```nota
{| Trait Target |}                    ;; marker impl, non-generic
{| [T] Trait (Target T) |}             ;; marker impl, generic
{| Trait Target [ (deref ...) ] |}     ;; method-bearing impl, non-generic
{| [T] Trait (Target T) [ (f ...) ] |} ;; method-bearing impl, generic
```

The leading parameter list is optional and recognized by square-bracket
shape before the trait. The trailing body list is optional and recognized
after the target. A marker trait may have no body. A method-bearing impl
must carry its function bodies as data; there is no ad hoc `method`
keyword. Function/signature forms are their own construct and should be
designed explicitly when that layer is implemented.

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
  `639`. Positional syntax: `640`/`643`. Streams/families: `645`/`649`.
  Generic and pipe-delimiter assignment: `655`/`658`.
- Intents: `7c71` `2zed` `my86` `wqdi` (thesis); `ov30` (dimensional principle);
  `adnn` (positional syntax).
- `skills/abstractions.md` (newtype-per-role endpoint), `skills/nota-design.md`
  (NOTA records; defers struct-body grammar here), `skills/component-triad.md`.
- Code: nota-next `derive/src/lib.rs`, schema-next `src/declarative.rs` +
  `src/schema.rs` (epic branch `next/structural-forms`).
