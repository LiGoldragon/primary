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

**Current codec scope** `[implementation-fact: core-ethos/src/whole.rs
lines 608-613]` — of the six slots, the codec currently *parses content* only
at the Types slot. Imports, Generics, and Impls delegate to `empty_braces`;
Input and Output delegate to `empty_square`. This means those five slots must
be literally `{}` / `[]` for the current codec to accept a document — any
populated content in them (trait catalogs, interface variants, etc.) is
**old-generation evidence only**, and whether current Ethos will ever carry
such content is `[open]`. Sections below covering Impls- and Input/Output-slot
syntax describe old-schema shapes, not current codec behavior.

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

**Current item vocabulary is exactly three constructors** `[implementation-fact:
core-ethos/src/whole.rs; WholeEthosItem enum, lines 165-171]` — `WholeEthosItem`
contains only two variants, `Newtype` and `Enumeration`. There is **no struct
constructor** in the current Ethos surface.

| Form | Meaning | Source |
|------|---------|--------|
| `X.Y` | newtype wrapping `Y` | `newtype_rule`, line 731 |
| `X.Y.Z` | newtype wrapping the application `Y.Z` — head `X` consumed as the declaration, remainder parsed as a type reference | `application_reference_rule`, line 798 (applied within `newtype_rule`) |
| `X.{A B}` | enum, brace-delimited variants | `brace_enumeration_rule`, line 741 |
| `X.[A B]` | enum, square-delimited variants | `square_enumeration_rule`, line 754 |
| (both enum forms decode to the same `WholeEthosEnumeration`) | | lines 916-917 region (`reify_item`, enum branch) |

The codebase itself describes this as deliberately narrow: `[implementation-fact:
core-ethos/src/whole.rs line 704]` — "bounded six-slot Ethos fixture breadth."

**Older flat-algebra struct/newtype-lowering material (not current surface):**
the braced-body struct form and the single-field-brace newtype lowering below
belong to an older flat algebra, not the six-slot item vocabulary above.
Whether struct support returns to the six-slot surface is `[open]`.

| Form | Meaning | Source |
|------|---------|--------|
| `X.{many fields}` | positional struct (older flat algebra, not in current `WholeEthosItem`) | `[old-schema evidence]` |
| `X.{one field}` | lowers to a newtype (field name dropped) | `[old-schema evidence]`: `core-ethos/src/declaration.rs`, `EncodedType::from_braced_body`, doc comment cites psyche ruling 2026-07-17, bead `primary-56d1.36`; converges byte-for-byte with the legacy `schema-language` `MacroExpansionStructBody::lower_type` behavior. This is older flat-algebra machinery, not confirmed part of the current six-slot item vocabulary. |

Variant syntax inside enum bodies (`core-ethos/src/whole.rs`) —
`[implementation-fact]` — three constructors:

| Form | Meaning | Source |
|------|---------|--------|
| bare atom | unit variant | `unit_variant_rule`, line 767 |
| `A.{T1 T2 ...}` | tuple variant, 1+ fields | `tuple_variant_rule`, line 771 |
| `A.T` | payload variant, compact single-payload form | `payload_variant_rule`, line 784 |

Both `A.T` and `A.{T}` reify to the same shape:
`[implementation-fact: core-ethos/src/whole.rs lines 950-984]` — both forms
produce `WholeEthosVariantPayload::Tuple`.

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
**old-schema evidence only**. The current six-slot codec does not decode
Impls-slot content at all: `[implementation-fact: core-ethos/src/whole.rs
lines 608-613]` — Impls delegates to `empty_braces`, meaning it must be
literally `{}` to parse. Treat the shape above as inherited intent, not
current behavior — carrying it forward is `[open]`.

## At the Input / Output slots

`[old-schema evidence + six-slot slot roles]`

`X.Y` at Input or Output names an interface variant: `X` is the variant name,
`Y` its payload — structurally the same `Name.Payload` application shape used
for enum payload variants at the Types slot. This reading is **old-schema
evidence only**. The current six-slot codec does not decode Input/Output-slot
content at all: `[implementation-fact: core-ethos/src/whole.rs lines
608-613]` — both slots delegate to `empty_square`, meaning they must be
literally `[]` to parse. The slot *roles* (`InputRole` / `OutputRole`) are
confirmed structural positions in the six-slot codec; the populated `X.Y`
reading has not been, and currently cannot be, exercised against a decoding
six-slot Input/Output fixture. Whether it carries forward is `[open]`.

## Type applications in reference positions

`[implementation-fact: core-ethos/src/whole.rs]` — two type-reference
constructors: `identity_reference_rule` (line 794, a bare name) and
`application_reference_rule` (line 798, `Y.Z`).

Applications are **right-associative**: `Y.Z.W` parses as `Y` applied to
`(Z applied to W)`, not `(Y applied to Z)` applied to `W`.

Application **heads must be registered priors**: `[implementation-fact:
core-ethos/src/whole.rs, accepts_application_head, line 1003]` — a name can
only head an application if it has been registered as an application-head
prior. The default builtin priors are `[implementation-fact:
core-ethos/src/whole.rs, WholeEthosBuiltinPriors, lines 1023-1032]` **only
`Integer` and `Vector`** — no other builtin (not `Optional`, not `ScopeOf`)
is a registered application head by default. The prior set is extensible via
`with_identity` / `with_application_head` (`[implementation-fact: whole.rs
lines 1045-1065]`), so a document or its embedding context can register more,
but nothing beyond `Integer`/`Vector` ships registered by default.

| Form | Reading | Status |
|------|---------|--------|
| `Vector.Integer` | `Vector` applied to `Integer` | current, exercised in `whole_six_slot.rs`; `Vector` is a default-registered application-head prior |
| `Optional.NodeConfig` | `Optional` applied to `NodeConfig` | shape is current-syntax-legal, but `Optional` is **not** a default-registered application-head prior — would require explicit registration |
| `ScopeOf.Domain` | `ScopeOf` applied to `Domain` | shape is current-syntax-legal, but `ScopeOf` is **not** a default-registered application-head prior (see ScopeOf section below) |
| `Bytes.4` | application with a value argument | old-schema shape; not independently re-verified in six-slot fixtures |
| `Map.(A B)` | parenthesized multi-argument application | `[old-schema evidence only]` — parentheses are not present in the six-slot codec's boundary triggers. `[implementation-fact: core-ethos/src/whole.rs lines 1150-1167]` define only square, brace, and whitespace boundary triggers — no parenthesis trigger exists. Not expressible in the current six-slot codec. |

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

This is test-proven, not just structurally inferred: `[implementation-fact:
core-ethos/tests/whole_six_slot.rs lines 386-402]` — the test verifies that
`CommitSequence` (a declaration-position atom) produces `Query::Declaration`
and `Integer` (a reference-position atom) produces `Query::Reference`, each
at its own source position.

Supporting rulings:

`[psyche-ruled, DesignReviewRulings entry 3]` — "nothing declares the coreID,
the coreID is allocated by the translator on receiving an unallocated word."

`[psyche-confirmed]` — "declarations allocate while references only
resolve."

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

**Status correction (important):** `ScopeOf` has **no handling in the
current codec and is not a registered prior**. `[implementation-fact:
core-ethos/src/whole.rs, WholeEthosBuiltinPriors, lines 1023-1032]` — the
default builtin priors are only `Integer` and `Vector`; `ScopeOf` is absent.

Structurally, *if* `ScopeOf` were registered as an application-head prior
(via `with_application_head`, lines 1045-1065), `DomainScope.ScopeOf.Domain`
would parse as newtype `DomainScope` wrapping the application
`ScopeOf.Domain` — `[implementation-fact, per the Types-slot rules above:
X.Y.Z = newtype wrapping (Y applied to Z)]`. But this is conditional on a
registration that does not currently exist; the syntax is legal, the prior
is not present.

`[old-schema evidence: schema-rust/src/lib.rs, `SingleTypeReferenceProjection::ScopeOf`
expansion semantics, lines 1176-1189 (`scope_root_name()` at line 1176,
`is_scope_of()` at line 1188)]` — the old schema-rust emitter **flattens**
`ScopeOf` applications to a bare concrete enum. This old-generation expansion
semantics is **not carried forward as ruled design** — it is evidence of
prior (possibly informal) behavior in the old generation only, not a ruling
on current/future `ScopeOf` handling, and not something the current codec
implements.

Current-Ethos `ScopeOf` is **new design in progress**, per the psyche's
2026-07-31 work order: an authored Nomos transformer plus prior registration
— trait-based Rust target, minimal Ethos syntax, with the Nomos worked out
between the two. Helper-type identity for `ScopeOf` remains `[open]` — see
`ProtosEngineDesign-2026-07-29`, open question 15; the overnight addendum
leaned toward "Option B," at a point the psyche had not yet reviewed/endorsed
that lean.

`[psyche-ruled 2026-07-31]` — **All ruling**: `All` is a whole-tree wildcard
("All should, as the name implies, match all"). This ruling **supersedes**
the overnight lean's earlier "All matches only itself" reading — that earlier
reading is superseded, not current.

## Ratified LOGOS item vocabulary (not Ethos surface syntax)

**Relabel:** the schema below is the **LOGOS item vocabulary** — the typed
representation of Rust items — and is **not Ethos surface grammar**. It does
not describe what you write in an Ethos document's Types slot; it describes
a downstream typed representation. It is placed here only because earlier
report drafts presented it beside Ethos syntax and that adjacency was
misleading.

`[psyche-ruled, carries an unrecovered exception: "otherwise I like the
syntax", ProtosEngineDesign-2026-07-26, lines 251-293]` — the ratification
itself is conditional. Per `ProtosEngineDesign-2026-07-29` section 13, "what
'otherwise' excepted was never recovered" — the ruling text has a caveat
whose content is lost. Treat this schema as **ratified-with-an-unrecovered-
exception**, not unconditionally settled, wherever relied on.

```
NewtypePayload.{ ItemName Visibility Attributes WrappedField }
StructPayload.{ ItemName Visibility Attributes Generics Fields }
EnumerationPayload.{ ItemName Visibility Attributes Generics Variants }
```

The first field is always the identifying subject (the item's own name).

Note the LOGOS vocabulary includes `StructPayload`, unlike the current
`WholeEthosItem` Ethos-surface enum (Newtype/Enumeration only, see the Types
slot section above) — another reason not to read this as Ethos grammar.

## Summary table — grading of the whole document

| Claim | Grade |
|-------|-------|
| Six-slot document model, order, delimiters | implementation-fact |
| Current codec parses content only at Types slot; other five delegate to empty_braces/empty_square | implementation-fact (whole.rs 608-613) |
| `.` = application operator; `[]`/`{}` = boundaries only | implementation-fact |
| "ALL FIELDS ARE POSITIONAL" / no field names | psyche-ruled |
| Item vocabulary: newtype, brace-enum, square-enum only (no struct) | implementation-fact (WholeEthosItem, whole.rs 165-171) |
| Struct form / one-field brace-body newtype lowering | old-schema / older flat algebra evidence; current six-slot struct support is open |
| Variant forms (unit / tuple / payload); A.T and A.{T} both reify Tuple | implementation-fact |
| Impls-slot `X.[A B C]` trait catalog | old-schema evidence only; current codec requires literal `{}` at Impls |
| Input/Output-slot `X.Y` named interface variant | old-schema evidence only; current codec requires literal `[]` at Input/Output |
| Type applications (`Vector.Integer` etc.), right-associative, heads require registered priors, default priors only Integer/Vector | implementation-fact; `Bytes.4` and `Map.(A B)` are old-schema-only, `Map.(A B)` unsupported by current boundary triggers |
| Declaration vs. reference binding by position | implementation-fact, test-proven (whole_six_slot.rs 386-402) |
| No grammar keywords | psyche-ruled |
| ScopeOf not a registered prior in current codec | implementation-fact (WholeEthosBuiltinPriors, whole.rs 1023-1032) |
| ScopeOf newtype-over-application shape | implementation-fact, conditional on future registration (derived from Types-slot rule) |
| Old schema-rust ScopeOf flattening expansion semantics | old-schema evidence only, not carried forward as ruled design |
| ScopeOf as new design (Nomos transformer + prior registration) | psyche work order 2026-07-31 |
| ScopeOf helper-type identity | open |
| All = whole-tree wildcard | psyche-ruled 2026-07-31, supersedes prior overnight lean |
| LOGOS item vocabulary (Newtype/Struct/Enumeration payload) — not Ethos syntax | psyche-ruled with unrecovered exception ("otherwise...") |
| "protos" as the shared textual style name | psyche-ruled (PsycheVisionReacquisition entry 3) |

## Current grammar — compact summary

Everything confirmed current-implementation-fact, in one place:

```
Document: {imports} [input] [output] {types} {generics} {impls} — only types populated.
Items:    X.Y newtype; X.Y.Z newtype wrapping application; X.[A B C] / X.{A B C} enum.
Variants: A unit; A.T payload; A.{T1 T2} tuple.
References: Y identity; Y.Z application (right-recursive).
Everything else is old-generation evidence or open.
```

## Sources consulted (2026-07-31, includes deeper verification pass)

- `/git/github.com/LiGoldragon/core-ethos/src/whole.rs`
- `/git/github.com/LiGoldragon/core-ethos/src/declaration.rs`
- `/git/github.com/LiGoldragon/core-ethos/tests/whole_six_slot.rs`
- `/git/github.com/LiGoldragon/schema-rust/src/lib.rs`
- `/git/github.com/LiGoldragon/schema-rust/tests/fixtures/standard-newtype-impls.schema`
- `reports/` design-log entries cited inline above (ProtosEngineDesign-2026-07-26,
  ProtosEngineDesign-2026-07-29, PsycheVisionReacquisition) — not re-read in
  full for this pass; citations as supplied and spot-checked where source
  code corroborates them.
