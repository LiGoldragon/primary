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
rustc is the host.

## 2. Identity architecture (mirrors the schema)

**[psyche ruling]** Logos mirrors the schema identity architecture. The core /
true mirror below is psyche-stated vision:

- **CoreLogos** — a stringless core. Identifiers are indices into a logos
  **NameTable**.
- **TrueLogos** — the projected named view over CoreLogos.
- **rkyv** — the stored / in-memory form.
- **deserialized text** — the agent-readable projection, with pretty-printing.

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

**[psyche ruling]** (2026-07-11) The macro language is named **Nomos**. The
psyche picked it from the offered candidates (Nomos, Gramma, Techne, Poiesis):
"Nomos is great." References to "the macro language" throughout this document
now mean Nomos.

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

**[resolved 2026-07-11]** Where macro definitions live — **confirmed**: a
dialect IS a Nomos macro package (macro table plus structural section rules),
see section 3.1. Was: proposal pending psyche discussion.

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
