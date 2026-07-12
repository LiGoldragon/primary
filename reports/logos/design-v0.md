# Logos — design document v0

Durable design pickup surface for the Logos intermediate representation.
Written 2026-07-11 by the design session (session `schema-codex`, lane
`logos-design-doc`). A prior handover was corrupted by context compression, so
this document favors completeness and precise attribution over polish.

## How to read this document

Every substantive item is tagged with its provenance. A fresh-context reader
must respect these tags and must not promote a lower-authority tag to a higher
one:

- **[psyche ruling]** — the psyche's decision. Unless noted otherwise, taken
  in today's session (2026-07-11). These are settled unless he retracts them.
- **[evidence]** — a worker-verified fact with a cited source. True about the
  world as recorded; not itself a design decision.
- **[proposal]** — an agent suggestion awaiting the psyche's decision. Not
  accepted. Do not implement as if settled.
- **[open]** — undecided. No ruling exists; the question is live.
- **[resolved YYYY-MM-DD]** — a former [open] or [proposal] item the psyche has
  since settled; the entry points to the governing [psyche ruling].

Attribution rule for this document: it deliberately cites **no Spirit intent
tags**. A fresh audit found unresolvable intent tags in existing architecture
prose, so this session is cited by date (2026-07-11) instead. Where the
psyche's words were open, they are recorded open — statements are not
overextended into rulings.

## 1. What Logos is

**[psyche ruling]** The name is **Logos**. It is the intermediate
representation that sits between the schema language and the generated Rust.

**[psyche ruling]** The prior working name **"codex" was retracted** — it
collides with the Codex AI harness. Note: the evidence file in section 6 still
carries the old name in its filename (`codex-rust-construct-survey.md`); the
filename predates the Logos naming and has not been renamed. Treat any
occurrence of "codex" in that survey as referring to what is now Logos.

**[psyche ruling]** Logos models a **deliberately standardized subset of Rust**
as strictly typed, positional, NOTA-style data.

**[psyche ruling]** The pipeline is:

```
schema dialects  →  macro expansion  →  logos  →  Rust text  →  rustc
```

**[psyche ruling]** Rust is the **runtime backend**. The intended analogy: this
is like Shen lowering to its K Lambda kernel hosted on a small primitive set.
Logos is the small standardized core; Rust text is the lowering target;
rustc is the host. (Caveat, see section 1.1: "small" describes the fixed Rust
lowering semantics, not the logos structure-type vocabulary, which is
deliberately WIDE.)

## 1.1 Logos is 1-to-1 with Rust — the wordy vision (correction 2026-07-11)

> **PARTIALLY SUPERSEDED by section 1.2 (2026-07-11 session 2).** The 1-to-1
> "everything represented, transcription-only" core STANDS. But the anti-empty-slot
> mechanism below — "proliferation of specialized structure types" — was REVERSED by
> the psyche: he does not want many struct types; variance (visibility, etc.) is
> expressed by **fields/variants on general structures**. Read 1.2 first. Every
> "Nomos" mention in this document is also retired by 1.2.

**[psyche ruling]** (2026-07-11) An earlier reading of Logos as a *thin* IR whose
derives, `pub`, `struct`, `rustfmt::skip`, etc. materialize from macros at
projection **"totally missed my vision, by a long shot."** This ruling
**supersedes** any thin-logos framing elsewhere in this document and in
`syntax-mockup-v0.md`. His words:

> "I meant 1 to 1 equivalence. Basically, take the rust code, and write it with
> adaptive schema structures. so you can have a SimpleStruct, a
> GenericsBoundedStruct, a PublicSimpleStruct ... go crazy with the number of
> different 'code structures' ... The brief view is schema; logos is *wordy as
> fuck* — but as all the types needed to not need an empty slot (SimpleStruct
> instead of a general Struct with a bunch of empty (because unused for this
> simple struct) fields)."

Load-bearing consequences:

- **Everything in the Rust is represented in logos.** He asked pointedly: "where
  is rustfmt::skip represented? Where is struct represented? and pub? and all the
  derive blocks?" — all of it lives in logos. **Nothing materializes at
  projection**; **logos→Rust is transcription**.
- **The anti-empty-slot mechanism is proliferation of specialized structure
  types**, not optional/general types. A `SimpleStruct`, `PublicSimpleStruct`,
  `GenericsBoundedStruct`, … each carries exactly the slots it uses, all filled —
  rather than one general `Struct` with unused empty slots.
- **Brief→wordy is the expansion direction.** Schema is the brief view; Nomos
  expands it into wordy, fully-specified logos; logos transcribes to Rust. The
  expansion adds nothing at the logos→Rust step.

**[psyche ruling]** (2026-07-11) **Structure bodies are pure positional.** Shown a
sketch with dotted-head labels inside a body (`Derives.( … )`,
`CfgAttrDerives.( … )`), he corrected: **"your PublicTupleStruct would have
positional arguments probably, not named."** Dotted heads used as labels inside a
body are named binding — forbidden. **Each slot's type comes from the structure's
definition by expectation**; body values are bare (e.g. slot 2 is a paren list of
gated derives, slot 3 a paren list of plain derives, with no head announcing
either).

**[psyche ruling]** (2026-07-11) **The "small kernel" prior-art instinct is
INVERTED for the logos vocabulary.** The Shen/K-Lambda ~46-primitive instinct
(section 7.2) governs the fixed Rust lowering semantics, not logos. The logos
structure-type vocabulary is **wide, flat, and fully specified**: node types are
cheap, empty slots are forbidden. Optimize for zero empty slots by adding types,
not for a minimal type count.

**Resolved open choices** (carried rulings / interpretation, 2026-07-11):

- **Choice 3 (field names)** — settled by the prior-session composed rule,
  psyche-confirmed then: field names = **snake_case of the type name**, a per-kind
  pattern for generics, with an **explicit disambiguator only on repeats**. The
  names are **computed by Nomos at expansion but stored explicitly in logos**,
  because the Rust contains them (per the 1-to-1 ruling above). [psyche ruling]
- **Choice 5 (Vector vs builtin)** — settled by his original vision words:
  **array = a Rust primitive = a logos builtin; vector = a generic = has a
  definition** (a named Nomos macro). [psyche ruling]
- **Choice 4 (tuple vs named struct)** — **[proposal / agent interpretation
  2026-07-11]**: since tuple and named structs are **distinct specialized logos
  structures** (explicit, per the 1-to-1 ruling), arity is purely the *Nomos-side*
  selection rule for which structure to emit; Choice 4 dissolves as a *logos*
  question.

## 1.2 Reset — Nomos dropped, no type proliferation, psyche-authored base (2026-07-11 session 2)

The psyche rejected the v1 mockup root-and-branch and wrote logos himself; his sample
is now the authoritative base (recorded verbatim below). Six rulings:

**[psyche ruling] (1) Macro language — DROPPED, then REINSTATED (both recorded in
order, no smoothing).** First he said: **"we drop nomos; there isnt enough room for
another component; schema lowers into logos through logos macros."** Then, same
session, he reversed it: **"actually, we should keep nomos, because it is its own
language syntax. logos is a rust-equivalent, but our macros will not be rust macros."**
Net state (the reversal wins): **Nomos exists as the transformation language, with its
own syntax**; **Logos is the Rust-equivalent data language**; **macros are Nomos
macros, NOT Rust macros** (and not "logos macros written in logos"). Do NOT assert
anything about Nomos being or not being a separate component/daemon — he did not settle
that; his "not enough room for another component" remark was about components, and the
standing consumption ruling (Nomos definitions consumed in the logos daemon, section
3.1) is unaffected. The section-3 Nomos naming and consumption rulings therefore STAND.
What DID change from v1: a structure like the v1 `WireStructure`-with-baked-derives is
a **Nomos macro** (schema-side compression that expands to the full logos form), **not a
distinct logos type** (see ruling 2).

**[psyche ruling] (2) NO type proliferation.** His words: **"we dont want to create a
bunch of different struct types; logos is going to be mostly generated from schema. So
we use a field or variants for everything, like visibility."** This **REVERSES** the
"go crazy with the number of code structures" reading and v1's 19-type vocabulary.
Structures are **general**; variance is expressed by **fields and variants** (e.g.
visibility is a field/variant on a general structure, not a `PublicStruct` vs
`PrivateStruct` type split).

**[psyche ruling] (3) His hand-written sample is the base** (recorded verbatim as
**[psyche-written]**, including his inline comments):

```
Public.Newtype.(
  CommitSequence
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.(
      nota-text
      [NotaDecode NotaDecodeTraced NotaEncode])
    Derive.[rkyv.[Archive Serialize Deserialize]
            Clone Debug PartialEq Eq]]
  Integer
)

Public.Struct.(
  DatabaseMarker
  [ Literal.[[rustfmt.skip] [second.literal.thing]]
    ConfigurationAttribute.Feature.(
      nota-text
      [NotaDecode NotaDecodeTraced NotaEncode])
    Derive.[rkyv.[Archive Serialize Deserialize]
            Clone Debug PartialEq Eq]]
  [Public.CommitSequence
   Public.StateDigest
   Private.secretDigest.StateDigest]
)
```

Shapes therein: **name first**; **attributes as a typed vector** (`Literal` escape
hatch / `ConfigurationAttribute` with `Feature` as one predicate-kind variant /
`Derive` with dotted path-grouping `rkyv.[…]`); **fields as dotted chains**
`Visibility.name?.Type` with an explicit name ONLY on a repeated field type (the
established composed rule — `Public.StateDigest` derives `state_digest`;
`Private.secretDigest.StateDigest` disambiguates the repeat).

**[psyche ruling] (4) Visibility — two forms offered for his pick.** Outer variant
(`Public.Newtype.(…)`) or a variant field (a `[Public Private]`-style visibility slot),
**"if it's easier to deal with."** Both drawn on the same example in
`syntax-mockup-v2.md` §; trade-off stated, not picked.

**[psyche ruling] (5) Dotted-prefix pushed INTO nota** — supersedes mockup Open
Choice 1. His words: **"even in nota, when we expect a data variant, I would rather use
`Variant.(Data)` (or `.[]` for vectors)."** Nota's grammar/data model evolves to bind
expectation-driven variant application across all our languages. (This is already the
documented TARGET dotted carrying syntax in the `nota-schema-design` skill:
`Head.Payload`, `Variant.Payload`.)

**[psyche proposal — leaning, NOT final] (6) Delimiter reshuffle.** Record his
reasoning, not as settled: drop `[]` as strings; `{}` moves to **structs** (aligning
with the schema's landed struct-declaration syntax — see the constraint citation
below); `[]` becomes **vectors**; strings become `()` with `(| |)` as the
indentation-escaped form; maps possibly `()` or `[]` or — flagged — **no delimiter of
their own**, a map being a vector of pair-structs by expectation. Cited reasons:
struct-syntax alignment, and the `[this is a vector of strings]` ambiguity dissolving
into space-separated bare atoms. He notes his own sample uses the "wrong" delimiters if
this proceeds.

**[psyche ruling] (7) No double colons — Rust paths are DOTTED in logos.** His words:
**"I dont want the double colon; I dont want to start using exact rust syntax — logos
has to feel like logos."** Rust paths are represented **dotted** (`rustfmt.skip`,
`rkyv.[…]`); the **projection owns the `.`→`::` translation**. Literal foreign text
(tool-attribute names and the like) is carried in this dotted logos form, never
byte-exact Rust with `::`. This makes his sample's `rustfmt.skip` and `rkyv.[…]`
canonical, not deviations; the earlier "store `rustfmt::skip` byte-exact" option is
withdrawn.

**[evidence] The schema tuple-disallow constraint** (he referenced it from memory):
`schema-rust/ARCHITECTURE.md:186-197`. The schema has only `TypeDeclaration::Alias`,
`Newtype`, and `Struct`. A **newtype is a single-element brace carrying just the
wrapped type and no field name**, authored as the dotted `Topic.{ String }` (e.g.
`DecisionReceipt.{ Integer }`); a multi-field declaration is a named-field `Struct`.
There is **no multi-field tuple** form — the newtype-only constraint. Note the schema's
landed authoring surface is **already dotted-brace `.{ }`**, which is exactly what
reshuffle ruling 6 aligns logos to.

## 2. Identity architecture (mirrors the schema)

**[psyche ruling]** Logos mirrors the schema identity architecture. The core /
true mirror below is psyche-stated vision:

- **CoreLogos** — a stringless core. Identifiers are indices into a logos
  **NameTable**.
- **TrueLogos** — the projected named view over CoreLogos.
- **rkyv** — the stored / in-memory form.
- **deserialized text** — the agent-readable projection, with pretty-printing.

**[psyche ruling]** (2026-07-11) The schema→logos conversion consumes
**CoreSchema plus the schema NameTable** — not TrueSchema. Logos uses CoreSchema
so that CoreLogos has a better correspondence: CoreLogos **re-uses the same
identifier→name allocation** and **extends it** for CoreLogos with the logos
NameTable. His words: "logos should use coreschema so that its corelogos has a
better correspondance — so the conversion would be from coreschema +
schemaNameTable — then logos can re-use the same ID to names allocation, and
extend it for its corelogos + logosNameTable." Consequence: the identifier space
is **continuous across schema and logos** (schema identifiers keep their meaning
in logos; logos mints new ones by extension).

**[open]** / floated as "could": Logos **possibly served by its own daemon**
that the schema daemon calls for transforms and views. The psyche floated the
daemon shape with "could" — record it as a possibility, not a decision.

## 3. Macros — the entire lowering logic

**[psyche ruling]** Macros define the **ENTIRE logic** of how schema changes
into logos. There are two dispatch modes, both psyche-stated:

**(a) Named macros.** Objects present in the macro table (example: `Map`). An
application written `Map.()` expands via that macro's table entry.

**(b) Structural macros.** Per-section positional defaults. In a type-namespace
section, a declaration `X.{}` where `X` is **NOT** in the macro table is
processed by that section's **"particular-struct definition" macro** — which
applies the standard derive sets (the rkyv archive/serde trio, optional
NOTA-text derives, etc.).

**[psyche ruling]** This principle applies **everywhere**: every per-kind
section has its own structural macro rules, and those rules are themselves
defined in Nomos.

**[psyche ruling — dropped then REINSTATED 2026-07-11 session 2, see section 1.2]**
The transformation language is named **Nomos**. History, no smoothing: session 1 named
it Nomos; session 2 first dropped it ("we drop nomos… schema lowers into logos through
logos macros") then reinstated it ("actually, we should keep nomos, because it is its
own language syntax… our macros will not be rust macros"). Net: **Nomos stands, as the
own-syntax transformation language distinct from logos** (the Rust-equivalent data
language). The candidate-name list (Gramma / Techne / Poiesis) is historical; he chose
Nomos. The dispatch/structural-macro ideas in section 3 / 3.1 survive as **Nomos**
(own-syntax macros), not Rust macros.

**[psyche ruling]** (2026-07-11) Dispatch semantics, confirmed ("sounds
correct"):

- The macro table **keys on minted identity**, with names projected through the
  NameTable — lookup never dispatches on a string, preserving the
  no-string-dispatch invariant (section 6).
- An application `X.()` where `X` has **no macro-table entry is an error**. It
  is not silently treated as a structural default; the structural-default path
  is specifically the `X.{}` form of mode (b) above, for `X` not in the table.

### 3.1 Dialects as Nomos macro packages

**[psyche ruling]** (2026-07-11) The dialect-as-macro-package design is
**confirmed as the target**: a dialect (signal schema, sema schema, …) simply IS
a Nomos macro package — a macro table plus structural section rules. His words:
"in theory, although we'll be changing the compiler for a while until we get to
that stable point; eventually schema will be able to self-host." Record all
three parts:

- The **principle stands**: dialect = Nomos macro package.
- The **compiler changes during a staged path** — this is not immediate; the
  current compiler is rebuilt over time until it reaches a stable point.
- The **stated end state is self-hosting**: schema will eventually define its
  own Nomos macros.

**[proposal]** (agent interpretation, 2026-07-11) At the self-hosting end state,
the **Logos→Rust projection is the hosted kernel**: schema defines its own Nomos
macros above a fixed lowering to Rust. This is the same shape as the Shen
parallel in section 1 — a language self-hosting its macro layer atop a small,
fixed kernel (there K Lambda; here the Logos→Rust projection). Marked as agent
interpretation, not the psyche's words.

**[psyche ruling]** (2026-07-11) Where Nomos definitions are **consumed**: the
psyche reframed the earlier "where do they live" question from authorship to
consumption — "or rather, where are they consumed, right? since logos is
converting the schema to logos, it would be in the logos daemon." So Nomos
definitions are consumed **in the logos daemon, at the schema→logos conversion
site**. His words settle consumption only; the **authored surface** (what
document kind holds Nomos definitions at rest) remains [open] — see section 8.

## 4. Acceptance oracle

**[psyche ruling]** The Rust **currently generated by schema-rust** from the
existing definitions becomes the **target**. The logos produced by the macros
must lower to that same Rust.

**[psyche ruling]** Therefore the **existing emission goldens are the
verification basis** for the macro-system migration: the migration is correct
when the macro-produced logos lowers to the Rust the current emitter already
produces.

## 5. Deferrals and retractions (this session, psyche-stated)

**[psyche ruling]** **Pipe delimiters retracted.** Rationale he gave: strict
typing means each kind carries its own syntax, so dotted prefixes suffice and
pipe delimiters are unnecessary.

**[psyche ruling]** **Logos-level lineage machinery deferred.** This is the
minted-identities + rename-stable core-hash machinery for logos nodes. His
words: "possibly, not important right now." Deferred, not rejected.

## 6. Standing invariants

These are carried from the **prior session's handover**, where they were
psyche-stated. They are invariants Logos must hold, all **[psyche ruling]**
(prior session):

- **Strictly typed positional data.** The expected type is known at every NOTA
  boundary; the parser never classifies.
- **Positionality; no named binding.**
- **No aliases anywhere.**
- **Capitalization is semantic.** A capitalized-leading atom is an object; a
  lowercase-leading atom is a name.
- **Per-kind blocks.** A new class of meta-objects earns a new block.
- **One namespace per loaded whole.** A duplicate name is an error.
- **Generics are defined by kind.** Lowering dispatches on kind, never on a
  string name.

## 7. Evidence

### 7.1 The standardized-Rust-subset survey

**[evidence]** Source: `/home/li/primary/reports/codex-rust-construct-survey.md`
(filename predates the Logos naming). The survey directly read `schema-rust`
source and its committed emission goldens, plus an `rg`-counted survey of
hand-written code in `sema-engine`, `spirit`, and `signal-spirit`. The survey
self-tags each claim OBSERVED (direct file evidence) or INTERPRETATION; the
tags below reflect that: OBSERVED items are [evidence], INTERPRETATION items
are [proposal].

**[evidence]** The emitter produces **two dominant output shapes**, both driven
by the same `GenerationDriver` / `ModuleEmission` API:

1. **Wire-contract modules** — pure data shapes: tuple newtypes, named-field
   structs, tuple-variant enums, `From` impls, per-variant constructor factory
   methods. No doc comments, no logic bodies beyond trivial
   constructors/accessors.
2. **Daemon-runtime modules** — richer: traits with associated types, generic
   bounds, lifetimes, `async fn` bodies, kameo `Actor`/`Message` impls with
   real handler bodies, and a match-bearing `Display`/`Error` impl. This means
   the emitted-vs-hand-written boundary is **not** "data vs logic" — the
   emitter already emits a nontrivial slice of actor/runtime scaffolding.

**[evidence]** **Exactly two derive sets dominate**, counted by
`grep -oh 'derive([^)]*)'` over all 9 goldens:
`derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug,
PartialEq, Eq)` (236 occurrences) always paired immediately above with a
feature-gated `#[cfg_attr(feature = "nota-text", derive(nota::NotaDecode,
nota::NotaDecodeTraced, nota::NotaEncode))]` (199 occurrences). The derive set
is **constant** for ordinary schema types, not varying per field type. Two
smaller variants exist (`derive(Clone, Debug, PartialEq, Eq)` 9×, no rkyv;
`derive(PartialEq, Eq, PartialOrd, Ord)` 3×).

**[proposal]** (survey INTERPRETATION) Model derive sets as **single
standardized nodes**, not open attribute lists.

**[evidence]** **Counted zero-hits across four repos** (`schema-rust`,
`sema-engine`, `signal-spirit`, `spirit`), by targeted `grep -c`: `unsafe`
(0; `spirit` also `#![forbid(unsafe_code)]`), `macro_rules!` (0 — the only
macro mechanism anywhere is proc-macro `derive` and `cfg_attr`), and `union`
(0). Also absent: `async_trait`-style macro usage (0; the workspace uses
native `async fn` in traits instead).

**[proposal]** (survey INTERPRETATION) These zero-hit constructs are
**exclusion candidates** for the Logos node set. The `async_trait` *macro
pattern* specifically can be excluded, but async trait methods as a raw
language feature should stay in-scope.

**[evidence]** The emitter is already **token-based**: `proc_macro2::TokenStream`
+ `quote`, with one `prettyplease` pass at `emit_item_tokens`; no emitter code
builds Rust source with `format!`/`self.line` (except the literal
`// @generated` header). This is relevant to the logos→Rust projection: it can
inherit the existing parenthesization / hygiene handling from the token-based
path rather than reinventing it.

**[evidence]** (survey caveat) The survey names its own unknowns: `dyn Trait`,
raw pointers, `impl Trait` return position, const generics, and GATs were not
exhaustively checked (a shallow grep found 0–3 `dyn` hits per repo, not read
for load-bearingness). Treat those as **not-confirmed** rather than excluded.

### 7.2 Prior-art brief (delivered in-session)

**[evidence]** Delivered in this session as a prior-art brief; summarized here
inline as its evidentiary content:

- Shen / K Lambda ports need **~46 primitives**, kept small by
  interdefinability — every non-primitive form is a lowering, not a node.
- Full Rust-as-data (the `syn` crate model) costs **~150–250 node types**, with
  the expression grammar the dominant size driver.
- One-to-one text-projection pitfalls to design in early: **defensive
  parenthesization**; a **source-map** from generated Rust back to the
  schema/logos origin so rustc diagnostics point at the right place; and
  **name hygiene**.
- rustc's HIR/THIR desugaring **inverted**: Logos defines the small core and
  **forbids sugar at the dialect boundary**, re-sugaring only on Rust output.

## 8. Open questions

**[resolved 2026-07-11]** Macro-language name — **Nomos** (section 3). Was:
psyche to pick from Nomos / Gramma / Techne / Poiesis.

**[resolved 2026-07-11]** Where Nomos definitions are **consumed** — the logos
daemon, at the schema→logos conversion site (section 3.1). Also confirmed: a
dialect IS a Nomos macro package (macro table plus structural section rules).

**[open]** Where Nomos definitions are **authored / held at rest** — what
document kind carries a Nomos macro package. The psyche's 2026-07-11 statement
answered consumption, not authorship, so this remains undecided (per the
per-kind-blocks invariant it would earn its own block or document kind).

**[open]** Whether Nomos itself obeys the full NOTA invariants. Presumed
**yes**, but unconfirmed. (The no-string-dispatch invariant specifically is now
confirmed via minted-identity keying — section 3 — but the full set is not.)

**[resolved 2026-07-11]** Semantics of `X.()` where `X` is **not** in the macro
table — **confirmed an error** (section 3), and the macro table keys on minted
identity, not on a string name. Was: presumed error, unconfirmed. The
name-in-table vs structural-default split is the `X.()`-error / `X.{}`-structural
distinction now recorded in section 3.

**[open] / [proposal]** Logos v1 node-inventory scope. Proposal: seed the node
inventory from the emitter's two output shapes (section 7.1) and carve out the
counted exclusions. Awaiting psyche confirmation.

### 8.1 Carried from the prior session (schema-identity)

**[open]** Bootstrap question 1: the unit of "one schema" in the daemon's
database, and identity semantics on split / merge. **Untouched** this session.

**[open]** Bootstrap question 2 was **LOST to handover corruption**. What
survives is only its opening — "how do text edits become daemon edits…". It
**must be restated by the psyche from memory**; no worker should reconstruct
it.

**[open]** The `sema.schema` document-kind design and sema-engine's
stored-record identity basis both remain **pending that session** (blocked on
the two bootstrap questions above).

### 8.2 Operational direction (2026-07-11, pending merge-state verification)

**[psyche direction, pending verification]** The psyche directed the following
component-porting work onto the syntax-redesign base. A merge-state scout is
currently verifying the actual branch state, so this is recorded as **direction
pending that verification, not verified fact**:

- Components are to be **ported onto the syntax-redesign base**; `drop-next` is
  stated merged into `main`.
- A **spirit port is to be attempted** despite the families retirement. The
  families successor is still pending the sema document-kind design (section
  8.1).
- Any remaining **unmerged redesign slice should be merged into `main`** so the
  **dotted-prefix syntax becomes the universal base**.
