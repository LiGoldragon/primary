# Ethos Positional Grammar — Reconstructed Reference

Purpose: stop agents re-mining or guessing the Ethos (formerly "schema")
positional grammar. Every claim below is graded by provenance. Grades:

- `[psyche-ruled]` — a recorded ruling by the psyche (li). Binding.
- `[implementation-fact]` — read directly from current source, with `file:line`.
- `[old-schema evidence]` — observed in the old `schema-rust` generation only;
  not yet confirmed present in the current `core-ethos` six-slot codec.
- `[open]` — unresolved; do not treat as settled.

## Stratigraphy warning (read first)

The design was discussed under the name **"schema"** in nearly all older
material. When searching prior sessions, reports, or code history, search
under `schema`, not `ethos` — the rename came later.

- `schema-rust` (`/git/github.com/LiGoldragon/schema-rust`) is the **old**
  generation. Its fixtures and emitter show old syntax and old lowering
  behavior; treat it as archaeological evidence, not current ground truth.
- `core-ethos` (`/git/github.com/LiGoldragon/core-ethos`), specifically its
  `src/whole.rs` six-slot codec and `tests/whole_six_slot.rs`, is **current**.
- `reports/logos/` archives predate the name "logos" itself — the name changed
  underneath the archived content.
- Many original design sessions are deleted. Some rulings survive only as
  recovered quotes inside later reports, or as inference from implementation
  behavior. Where a ruling has no surviving direct quote, that is noted.

Also: `[psyche-ruled, PsycheVisionReacquisition entry 3]` — the shared textual
style of all four languages (Ethos and its siblings) is named **"protos"**.

## The six-slot document model

`[implementation-fact: core-ethos/src/whole.rs, struct SixSlotDocumentRecord
at line 583; field roles ImportsRole..ImplsRole lines 571-579]`
`[implementation-fact: core-ethos/tests/whole_six_slot.rs, BREADTH_SOURCE at
line 21]`

An Ethos document is exactly six positional slots, in this fixed order:

| # | Slot | Delimiter |
|---|------|-----------|
| 1 | Imports | `{}` |
| 2 | Input | `[]` |
| 3 | Output | `[]` |
| 4 | Types | `{}` |
| 5 | Generics | `{}` |
| 6 | Impls | `{}` |

Test source shape (from `BREADTH_SOURCE`, `whole_six_slot.rs:21`):

```
{} [] [] {Identifiers.Vector.Integer Status.{Pending Ready.{Integer} Batch.{Vector.Integer Integer}}} {} {}
```

There are no field names in the six-slot document — slot meaning is entirely
positional (see "No grammar keywords" below).

## The dot is the application operator

`[implementation-fact: core-ethos/src/whole.rs:32]` — `APPLICATION_OPERATOR`
is a distinct trigger from the boundary delimiters.
`[implementation-fact: core-ethos/src/whole.rs:30-31]` — `SQUARE_BOUNDARY`
(`[]`) and `BRACE_BOUNDARY` (`{}`) are the two boundary delimiters.

`.` applies one atom to what follows it. `[]` and `{}` only mark boundaries
(list/group extent and, at the Types slot, enum-variant-style vs.
struct/newtype-style bodies) — they carry no operator meaning of their own.

`[psyche-ruled: "ALL FIELDS ARE POSITIONAL", "field names are now
COMPLETLY ILLEGAL EVERYWHERE"]` — meaning is position-dependent throughout
the language; this is why it is called a positional grammar rather than a
keyed/named one.

## At the Types slot

All rows `[implementation-fact: core-ethos/src/whole.rs]` unless noted.

| Form | Meaning | Source |
|------|---------|--------|
| `X.[A B C]` | enum, square-delimited variants | `square_enumeration_rule`, line 754 |
| `X.{A B C}` | enum, brace-delimited variants | `brace_enumeration_rule`, line 741 |
| (both above decode to the same `WholeEthosEnumeration`) | | lines 916-917 region (`reify_item`, enum branch) |
| `X.Y` | newtype wrapping `Y` | `newtype_rule`, line 731 |
| `X.Y.Z` | newtype wrapping the application `Y.Z` — head `X` consumed as the declaration, remainder parsed as a type reference | `application_reference_rule`, line 798 |
| `X.{many fields}` | positional struct | — |
| `X.{one field}` | lowers to a newtype (field name dropped) | `core-ethos/src/declaration.rs`, `EncodedType::from_braced_body`, doc comment cites psyche ruling 2026-07-17, bead `primary-56d1.36`; converges byte-for-byte with the legacy `schema-language` `MacroExpansionStructBody::lower_type` behavior |

Variant syntax inside enum bodies (`core-ethos/src/whole.rs`):

| Form | Meaning | Source |
|------|---------|--------|
| bare atom | unit variant | `unit_variant_rule`, line 767 |
| `V.Payload` | payload variant | `payload_variant_rule`, line 784 |

Note on line numbers: the task brief cited `whole.rs` 572-591 for
`SixSlotDocumentRecord`; the struct is at line 583 in the checked-out
revision (within that range's neighborhood — file has likely shifted
slightly between sessions). Cited line numbers above were re-verified
2026-07-31 against the current checkout.

## At the Impls slot

`[old-schema evidence: schema-rust/tests/fixtures/standard-newtype-impls.schema]`

```
NameText.[ Display AsRef PartialEq ]
```

`X.[A B C]` at the Impls slot names a trait catalog for type `X`. This is
**old-schema evidence only** — whether the current six-slot `core-ethos`
codec decodes Impls-slot content at all (it currently only asserts the slot
is present/delegated; see `ensure_delegated::<ImplsRole>` in
`whole.rs`) is check-worthy and not yet confirmed. Treat the shape above as
inherited intent, not verified current behavior.

## At the Input / Output slots

`[old-schema evidence + six-slot slot roles]`

`X.Y` at Input or Output names an interface variant: `X` is the variant name,
`Y` its payload — structurally the same `Name.Payload` application shape used
for enum payload variants at the Types slot. Confirmed as a slot *role*
(`InputRole` / `OutputRole` in the six-slot codec); the specific `X.Y` reading
carries over from old-schema material and has not been independently
re-verified against a decoding six-slot Input/Output fixture.

## Type applications in reference positions

| Form | Reading | Status |
|------|---------|--------|
| `Vector.Integer` | `Vector` applied to `Integer` | current, exercised in `whole_six_slot.rs` |
| `Optional.NodeConfig` | `Optional` applied to `NodeConfig` | current, same shape |
| `ScopeOf.Domain` | `ScopeOf` applied to `Domain` | current, same shape (see ScopeOf section below) |
| `Bytes.4` | application with a value argument | old-schema shape; not independently re-verified in six-slot fixtures |
| `Map.(A B)` | parenthesized multi-argument application | `[old-schema evidence only]` — parentheses are not present in the six-slot codec's boundary triggers (`SQUARE_BOUNDARY`, `BRACE_BOUNDARY` are the only two; no paren trigger in `whole.rs`). Not yet in the current six-slot codec. |

## Declaration vs. reference — the deepest positional fact

`[implementation-fact: structural-codec crate, SharedDescriptor::Declaration
vs. SharedDescriptor::Reference variants, as constructed throughout
core-ethos/src/whole.rs (e.g. `newtype_rule` line ~732 uses
`SharedDescriptor::Declaration`; `application_reference_rule` line ~800 uses
SharedDescriptor::Reference)]`

The same atom spelling means different **binding behavior** depending on
which position it occupies:

- A declaration position requires a translator-issued assignment that has
  already been made for that spelling (`declaration_assignment()` /
  `DeclarationAssignment`, requires pre-issued translator assignment).
- A reference position requires the spelling to resolve against a prior that
  is already known (`reference_resolution()` / `ResolvedReference`, requires
  resolved prior).

`decode()` in `whole.rs` documents this directly: "Name bindings are
read-only: declaration positions require an assignment already issued by the
translator, and reference positions require an already-resolved prior. No
spelling-to-ID operation exists here."

This is the sense in which Ethos is positional that goes beyond slot order:
the identical token `X` is not merely displayed differently by position, it
is *processed* by an entirely different binding rule depending on whether it
sits in a declaring or referring position.

## No grammar keywords

`[psyche-ruled 2026-07-22: "make them the same thing" — "exceptions are
symptoms of bad design"]`

Builtins — `Integer`, `String`, `Vector`, `Optional`, `ScopeOf`, and so on —
are **prior definitions in the translator table**, syntactically identical to
any user-authored name. There is no reserved-word class in the grammar.

This is what makes it possible for `ScopeOf` to become an authored Nomos
transformer without any grammar change: it is just another name with a prior,
not a special form the parser recognizes.

## ScopeOf specifically

`DomainScope.ScopeOf.Domain` declares `DomainScope` as a newtype wrapping the
application `ScopeOf.Domain` `[implementation-fact, per the Types-slot rules
above: X.Y.Z = newtype wrapping (Y applied to Z)]`.

`[old-schema evidence: schema-rust/src/lib.rs, `scope_root_name()` at line
1176, `is_scope_of()` at line 1188]` — the old schema-rust emitter **flattens**
this to a bare concrete enum via `scope_root_name()` rather than preserving
the newtype-over-application shape. This is an **old-generation inconsistency**
between the encoded shape and the emitted Rust, identified by the psyche
2026-07-31. It is evidence of prior (possibly informal) behavior, not a
ruling on what current/future ScopeOf handling should do.

Helper-type identity for ScopeOf remains `[open]` — see
`ProtosEngineDesign-2026-07-29`, open question 15; the overnight addendum
leaned toward "Option B," at a point the psyche had not yet reviewed/endorsed
that lean.

`[psyche-ruled 2026-07-31]` — **All ruling**: `All` is a whole-tree wildcard
("All should, as the name implies, match all"). This ruling **supersedes**
the overnight lean's earlier "All matches only itself" reading — that earlier
reading is superseded, not current.

## Ratified item schema

`[psyche-ruled: "otherwise I like the syntax", ProtosEngineDesign-2026-07-26,
lines 251-293]`

```
NewtypePayload.{ ItemName Visibility Attributes WrappedField }
StructPayload.{ ItemName Visibility Attributes Generics Fields }
EnumerationPayload.{ ItemName Visibility Attributes Generics Variants }
```

The first field is always the identifying subject (the item's own name).

## Summary table — grading of the whole document

| Claim | Grade |
|-------|-------|
| Six-slot document model, order, delimiters | implementation-fact |
| `.` = application operator; `[]`/`{}` = boundaries only | implementation-fact |
| "ALL FIELDS ARE POSITIONAL" / no field names | psyche-ruled |
| Types-slot enum/newtype/struct forms | implementation-fact |
| One-field brace body lowers to newtype | implementation-fact (+ psyche ruling 2026-07-17 cited in code comment) |
| Variant forms (unit / payload) | implementation-fact |
| Impls-slot `X.[A B C]` trait catalog | old-schema evidence; six-slot decode of Impls content is check-worthy/unconfirmed |
| Input/Output-slot `X.Y` named interface variant | old-schema evidence + confirmed slot roles |
| Type applications (`Vector.Integer` etc.) | implementation-fact for unary/binary shapes; `Bytes.4` and `Map.(A B)` are old-schema-only, `Map.(A B)` unsupported by current boundary triggers |
| Declaration vs. reference binding by position | implementation-fact |
| No grammar keywords | psyche-ruled |
| ScopeOf newtype-over-application shape | implementation-fact (derived from Types-slot rule) |
| Old schema-rust ScopeOf flattening inconsistency | old-schema evidence, flagged by psyche 2026-07-31 |
| ScopeOf helper-type identity | open |
| All = whole-tree wildcard | psyche-ruled 2026-07-31, supersedes prior overnight lean |
| Ratified item schema (Newtype/Struct/Enumeration payload) | psyche-ruled |
| "protos" as the shared textual style name | psyche-ruled (PsycheVisionReacquisition entry 3) |

## Sources consulted (2026-07-31)

- `/git/github.com/LiGoldragon/core-ethos/src/whole.rs`
- `/git/github.com/LiGoldragon/core-ethos/src/declaration.rs`
- `/git/github.com/LiGoldragon/core-ethos/tests/whole_six_slot.rs`
- `/git/github.com/LiGoldragon/schema-rust/src/lib.rs`
- `/git/github.com/LiGoldragon/schema-rust/tests/fixtures/standard-newtype-impls.schema`
- `reports/` design-log entries cited inline above (ProtosEngineDesign-2026-07-26,
  ProtosEngineDesign-2026-07-29, PsycheVisionReacquisition) — not re-read in
  full for this pass; citations as supplied and spot-checked where source
  code corroborates them.
