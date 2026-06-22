# 12 — Unified dot-prefix struct-field syntax

schema-designer lane. Design (confirmed against code) for collapsing
schema-next's struct-field specs onto a single explicit-field-name form:
the **dot-prefix `name.TypeReference`**, extended so the type after the
dot may be a composite (`members.(Vector X)`, `limit.(Optional Integer)`,
`m.(Map K V)`). This lets the parenthesized `(name composite)` explicit
form be deprecated and removed.

Investigated at commit `4b7e830` (schema-next, detached HEAD; the three
landed structural-forms commits `af3705c`, `95f1ee7`, `1de72dd` are all
ancestors — verified via `git merge-base --is-ancestor`). NOTA lexer read
from the vendored `nota-next` in the nix build sandbox
(`.../vendor-sources/nota-next/src/parser.rs`).

There are TWO independent struct-field parsers in schema-next, and every
change below must land in both:

- **`source.rs`** — `SourceField::from_positional_block` (the source/codec
  round-trip layer).
- **`declarative.rs`** — `MacroExpansionField::lower` (the macro-expansion
  lowering layer, where fields can be macro-expanded objects).

## (a) The retired forms are rejected today — confirmed

The prompting example
`ClusterRunRecord { ClusterRunIdentifier * ClusterName * members (Vec ...) phase ClusterRunPhase ... }`
uses two retired shapes; both are rejected loudly.

| Retired shape | Where caught | Error |
|---|---|---|
| `*` shorthand (atom) | `source.rs:2098-2102` | `SchemaError::RetiredStructFieldSyntax` |
| `*` shorthand (atom) | `declarative.rs:1796-1805` | `SchemaError::RetiredStructFieldSyntax` |
| `field Type` name-value pair, parenthesized `(field Type)` with lowercase head | `source.rs` via `from_positional_block` falling through to `2114-2116`; `declarative.rs:1773-1781` (`is_explicit_field_pair`) | `SchemaError::RetiredStructFieldSyntax` |
| lowercase-leading bare atom (e.g. `members`, `phase` standing alone) | `declarative.rs:1796-1805`; `source.rs:2114-2116` | `SchemaError::RetiredStructFieldSyntax` |
| redundant explicit role `topic.Topic` | `source.rs:2160-2166`; `declarative.rs:1837-1843` | `SchemaError::RedundantExplicitFieldRole` |

Error definitions: `engine.rs:71-76`.

```
RetiredStructFieldSyntax  -> engine.rs:74
  "retired struct field syntax {found}; struct bodies are positional
   field types, use TypeName or field_name.TypeName"
RedundantExplicitFieldRole -> engine.rs:76
  "redundant explicit field role {found}; just use {type_name}"
```

Note on the prompting example specifically: the bare-word fields after
`*` (`members`, `phase`, `outcome`) and the `(Vec ContainedRunIdentifier)`
composite are not even reached as valid fields — the `*` atoms fail first,
and the lowercase bare atoms would each fail as `RetiredStructFieldSyntax`.
So the example is rejected today, exactly as the prompt states.

## (b) The three accepted forms today — confirmed, with file:line

The doc comment at `declarative.rs:1749-1757` states the model; the code
implements it as follows.

1. **Bare PascalCase type** — `Topics`, `ClusterName`. Role/field-name is
   derived from the type. The default.
   - `source.rs:2106-2113` (atom, `is_type()`, not a reserved scalar →
     `SourceFieldValue::Derived`).
   - `declarative.rs:1806-1815` (atom → `FieldDeclaration` with
     `name.field_name()` from the type).
   - Native composite references also sit bare in a field position —
     `(Vector Topic)`, `(Map NodeName NodeConfig)`, `(Optional Topic)` —
     with the name *derived from the reference shape*
     (`declarative.rs:1785-1791` → `derived_name_for_reference`
     `1909-1929`: `topic_vector`, `node_config_by_node_name`,
     `optional_topic`). These are a bare form, NOT the explicit-name
     parenthesized form; the head is a `ReferenceHead`, not a field name.

2. **Dot-prefix on a PLAIN reference** — `source.TypeReference`.
   - Recognized as a single atom containing `.` →
     `from_explicit_field_reference` (`source.rs:2103-2104`, impl
     `2142-2172`) / `explicit_dot_field` (`declarative.rs:1793-1794`,
     impl `1818-1848`).
   - Both currently reject if `type_name.contains('.')`, if the type is
     not a plain symbol, or if it is not PascalCase
     (`source.rs:2148-2159`, `declarative.rs:1825-1836`). **The type after
     the dot is required to be a plain name — a composite is rejected.**

3. **Parenthesized explicit name on a COMPOSITE** —
   `(Topics (Vector Topic))`, `(Limit (Optional Integer))`.
   - `from_explicit_structural_field` (`source.rs:2119-2140`) /
     `explicit_structural_field` (`declarative.rs:1850-1886`).
   - Guard: parenthesis block, exactly 2 root objects, first object is a
     PascalCase symbol that is NOT a `ReferenceHead`
     (`source.rs:2123-2129`, `declarative.rs:1855-1872`), second object is
     NOT a bare string (i.e. it is itself a composite/delimited reference).
   - The "it's wrapped because a composite cannot take the bare or dot
     form" rationale (Spirit `adnn`): the dot form historically only
     accepted a plain name after the dot, so composites had to be wrapped.

## (c) Proposed unified grammar

One explicit-field-name form, the dot-prefix, for BOTH plain and
composite types. The bare form stays for the common (role = type) case.

```
struct-field   := bare-field | dot-field
bare-field     := PascalCaseType                  ;; role derived from type
                | composite-reference             ;; role derived from shape, e.g. (Vector Topic)
dot-field      := field-name "." type-reference
field-name     := lower-or-Pascal symbol (no '.')
type-reference := plain-name                      ;; name.TypeName  (today)
                | composite-reference             ;; name.(Vector X), name.(Optional X), name.(Map K V)  (NEW)
```

`RedundantExplicitFieldRole` stays: `topic.Topic` (and, once composites
are dot-formed, any `xs.(Vector X)` whose derived name would already equal
`xs`) is still rejected — keep the existing equality check.

### The decisive tokenization fact (drives the parse change)

The NOTA lexer (`parser.rs:781-802`, `parse_atom`) breaks an atom at any
opening or closing delimiter character and at whitespace; `.` is a plain
bare-string character (`parser.rs:898-901`, `.` is not in the
delimiter/quote set). Therefore:

- `source.TypeReference` lexes as **one atom** `source.TypeReference`
  (today's plain dot form — handled by `split_once('.')`).
- `members.(Vector ContainedRunIdentifier)` lexes as **TWO sibling root
  objects**: the atom `members.` (the trailing `.` is consumed, the atom
  stops at `(`) followed by the parenthesis block
  `(Vector ContainedRunIdentifier)`.

Both struct-body parsers iterate root objects **one block → one field**:
`SourceStructBody::from_block` (`source.rs:1950-1957`,
`.map(SourceField::from_positional_block)`) and
`MacroExpansionFields::lower` (`declarative.rs:1737-1746`,
`.map(|object| MacroExpansionField::new(*object).lower(...))`). A
`name.(composite)` field spans two objects, so the current one-to-one
iteration **cannot** see it as one field. This is the core change.

### The minimal parse change

A small lookahead in the struct-body iteration: when a positional object
is an atom that **ends in `.`** (a trailing dot with empty tail after
`split_once('.')`), treat the field name as that atom minus the trailing
dot and consume the **next** sibling object as the type reference, parsing
it with the existing `TypeReference::from_block_with_registry`
(`schema.rs:2481`), which already handles `(Vector X)`, `(Optional X)`,
`(Map K V)` via `resolve_parenthesis_reference` (`schema.rs:2504-2508`).

Concretely:

1. **`source.rs` — `SourceStructBody::from_block` (1950) /
   `from_positional_block` (2085).** Change the iteration from
   `map`-per-block to a hand-written pass over `root_objects()` that peeks
   ahead: if the current atom matches `^<field-name>.$` (non-empty name,
   empty type tail), pull the next object and build a
   `SourceField { name, value: Reference(SourceReference::from_block(next)?), positional: true }`.
   `SourceReference::from_block` (`source.rs:1284`) already accepts a
   parenthesis composite. Apply the same redundancy + symbol-name +
   PascalCase-type guards as `from_explicit_field_reference`
   (`2148-2166`), but on the composite's derived name.

2. **`declarative.rs` — `MacroExpansionFields::lower` (1737) /
   `MacroExpansionField::lower` (1768).** Same lookahead: when the current
   `ObjectView` demotes to a string of form `<name>.` (trailing dot),
   consume the next object and call `next.type_reference(registry,
   context)` (`declarative.rs:1381`, already routes composites to
   `from_block_with_registry`) for the reference. Build the
   `FieldDeclaration` with `name.field_name()`. Keep the redundancy check.

3. **Re-emit (round-trip) — `source.rs:2073-2075.** Flip the
   `(SourceFieldValue::Reference(reference), true)` arm from
   `Delimiter::Parenthesis.wrap([name, reference])` (today emits
   `(Topics (Vector Topic))`) to `format!("{}.{}", name, reference)` so it
   emits `Topics.(Vector Topic)`. The plain-reference arm at `2070-2072`
   already emits `name.Type`; the composite arm just joins with `.`
   instead of wrapping.

4. **Retire the parenthesized recognizers.** Delete / repurpose
   `from_explicit_structural_field` (`source.rs:2119`) and
   `explicit_structural_field` (`declarative.rs:1850`). See (e) for whether
   to delete outright or hard-reject — recommendation: hard-reject.

No NOTA-grammar change is required — the lexer already produces the right
two-object shape; only schema-next's struct-body interpretation changes.
No new error variant is needed; reuse `RetiredStructFieldSyntax` for the
deprecated parenthesized form and `RedundantExplicitFieldRole` unchanged.

## (d) Worked before / after

The ClusterRunRecord example (root-form spelling):

```
;; BEFORE (retired '*' + name-value — rejected today)
ClusterRunRecord {
  ClusterRunIdentifier * ClusterName *
  members (Vec ContainedRunIdentifier)
  phase ClusterRunPhase
  outcome ClusterOutcome
}

;; AFTER (unified)
ClusterRunRecord {
  ClusterRunIdentifier
  ClusterName
  members.(Vector ContainedRunIdentifier)
  phase.ClusterRunPhase
  outcome.ClusterOutcome
}
```

- `ClusterRunIdentifier`, `ClusterName` — bare; role = type.
- `members.(Vector ContainedRunIdentifier)` — NEW dot+composite (note
  canonical head `Vector`, not `Vec`).
- `phase.ClusterRunPhase`, `outcome.ClusterOutcome` — existing dot+plain;
  explicit name differs from the type so not redundant.

Converting the existing parenthesized test examples (`collections.rs:106`,
`source_codec.rs:86,104`):

```
;; BEFORE
Query { (Topics (Vector Topic)) (Limit (Optional Integer)) }
;; AFTER
Query { Topics.(Vector Topic) Limit.(Optional Integer) }
```

Map example:

```
;; BEFORE
{ (Projected (Map NodeName NodeConfig)) }
;; AFTER
{ Projected.(Map NodeName NodeConfig) }
```

Bare composite references DO NOT change — they have no explicit name, the
head is a `ReferenceHead`, name is derived:

```
;; UNCHANGED (collections.rs:220, :238 second field)
Nest (Map Key (Vector (Optional Leaf)))   ;; bare; derived name
(Map NodeName NodeConfig)                  ;; bare; derived name node_config_by_node_name
```

## (e) Deprecation / migration plan

The workspace hard-override forbids backward compatibility pre-production
and forbids presenting non-disruption as a virtue. schema-next has no
production wire-contract on this surface. Recommendation: **clean break —
hard-reject the parenthesized `(name composite)` form**, exactly as `*`
and the name-value pair were hard-rejected. Reasons:

- Symmetry with the already-landed retirements (`af3705c`, `95f1ee7`):
  one rejection mechanism, one mental model.
- Accept-with-warning needs a warning channel these parsers don't have
  (they return `Result`, no diagnostic sink), and would keep two
  recognizers alive — more surface, not less.
- The migration is mechanical and the corpus is tiny (below).

Migration steps:

1. **Sweep every `(Name (composite))` explicit-name field →
   `Name.(composite)`** in all `.schema` sources and Rust test fixtures.
   Known occurrences (all in tests, none in the shipped `schemas/*.schema`
   — grep found zero in `schemas/`):
   - `tests/collections.rs:106` — `(Topics (Vector Topic)) (Limit (Optional Integer))`
   - `tests/collections.rs:238` — `(Projected (Map NodeName NodeConfig))`
   - `tests/source_codec.rs:86` and `:104` — the `Query { ... }` round-trip strings
   - Audit `tests/collections.rs:263` `(HashSet (Vector Leaf))` — `HashSet`
     is not a `ReferenceHead`, so this is currently parsed as the
     explicit-name form `HashSet.(Vector Leaf)`; confirm intent (likely a
     negative/error test) and convert or keep as the migration's
     rejection case.
   - Distinguish carefully from bare composite references like
     `(Map Key (Vector (Optional Leaf)))` (`collections.rs:220`) and
     `(Map NodeName NodeConfig)` — those have a `ReferenceHead` first and
     MUST NOT be rewritten.
2. **Convert the parenthesized recognizers to loud rejections.** In
   `source.rs:2086-2090` and `declarative.rs:1782-1784`, when a 2-object
   parenthesis has a non-`ReferenceHead` PascalCase first object and a
   composite second object, return `RetiredStructFieldSyntax` (extend its
   message to name the dot replacement) instead of building the field.
3. **Land the dot+composite parse change** from (c) in both parsers plus
   the re-emit flip.
4. **Update the doc comment** at `declarative.rs:1749-1757` and Spirit
   `adnn` / `skills/structural-forms.md` to describe the single dot form
   (plain or composite after the dot) and the bare form.
5. Operators rebase code-repo `main`; this report only proposes — no code
   touched.

## (f) Ambiguity risks in `name.(...)` and how the grammar resolves them

1. **Trailing-dot atom vs. plain dot atom.** `source.TypeReference` is one
   atom with the `.` interior; `members.` is one atom with the `.`
   trailing (because `(` ends the atom). `split_once('.')` distinguishes
   them: an empty tail (`("members","")`) means "consume the next object as
   the composite reference"; a non-empty tail (`("source","TypeReference")`)
   is the existing plain dot form. No collision — the empty-tail case is
   currently a `RetiredStructFieldSyntax` reject, so repurposing it is
   safe and additive.

2. **`name.(...)` vs. a bare composite `(Head ...)`.** A bare composite is
   a single parenthesis object whose first element is a `ReferenceHead`
   (`Vector`/`Optional`/`Map`/`ScopeOf`/`Bytes`,
   `schema.rs:2148-2166`). A dot+composite is TWO objects: a trailing-dot
   atom THEN a parenthesis. The lookahead only fires when the *preceding*
   object is a trailing-dot atom, so a lone `(Vector X)` is never
   misread as a field name.

3. **Dot inside a float / qualified path.** NOTA classifies `1.5` as a
   number (`parser.rs:583`), but field names must be PascalCase/lowercase
   symbols, not numbers — the existing `qualifies_as_symbol_name` /
   PascalCase guards reject a numeric field name. A multi-dot atom
   (`a.b.c`) still fails the `field_name.contains('.')` /
   `type_name.contains('.')` guards (`source.rs:2150-2151`,
   `declarative.rs:1827-1828`); the new trailing-dot case is specifically
   the single-trailing-dot atom, so qualified paths are not affected.

4. **Whitespace between name and composite.** `members . (Vector X)` or
   `members. (Vector X)` would tokenize as a bare `members.` atom and a
   detached paren — the lookahead would still pair them since it consumes
   the next sibling regardless of intervening whitespace (NOTA discards
   whitespace between root objects). That is acceptable and matches how
   `members.(Vector X)` and `members. (Vector X)` should mean the same
   thing. If stricter adjacency is wanted later, it would require a
   lexer-level change in nota-next (out of scope; not recommended — the
   loose pairing is fine and simpler).

## Contradiction check

Nothing in the code contradicts the plan. The two enabling facts are both
present today: (i) the NOTA lexer already emits `name.` + `(composite)` as
two sibling objects (`parser.rs:781-802`), and (ii) the composite
reference parser `TypeReference::from_block_with_registry`
(`schema.rs:2481`, `resolve_parenthesis_reference` `2504`) already exists
and is reused by both struct-field parsers. The only true work is teaching
the two struct-body iterations to do a one-object lookahead, flipping one
re-emit arm, and converting the parenthesized recognizer to a rejection.
The change is additive over a currently-rejected token shape (trailing-dot
atom), so it cannot break any currently-valid source.
