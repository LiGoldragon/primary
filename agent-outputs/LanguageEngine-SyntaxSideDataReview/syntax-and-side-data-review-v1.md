# Language-family syntax-versus-vision review + side-data survey (v1)

Read-only review. Session `LanguageEngine`, lane `SyntaxSideDataReview`, Fresh,
generalist, Opus 4.8 (1M), 2026-07-17. No repository, generated artifact, store,
or Spirit record was changed. This one file is the lane's only artifact and the
pickup point for a follow-up rename lane.

The psyche does not read reports; the chat return is his surface. Every claim
below is anchored to `file:line` in a named repo under `repos/`, to a report under
`reports/logos/`, or to an epic item id. Examples are lifted verbatim from
fixtures/tests/source — none invented.

## 0. What is ground truth, and one brief-correction up front

- **Grammar/terminology authority:** `reports/logos/up-close-design-v1.md`
  (1268 lines; the reconciled code-level design). Identity authority:
  `reports/logos/schema-unit-lineage-design-v2.md` (supersedes v1).
- **Epic:** `primary-56d1` (43 items, 19 closed). Pilot-port directive is `.39`.
- **Live closure + witness:** `repos/language-engine-witness` (main), which pins
  the delivered engine crates by git rev (§Revisions).

**Brief-correction (verified, load-bearing for deliverable 2):** the brief states
the psyche "has ruled that the two ways to see the languages are named TextualForm
and EncodedForm." That is **not a ruling.** Bead `primary-56d1.37` (created
2026-07-17, P4, OPEN) records it verbatim as a **hedged lean**: *"TextualForm vs
CoreForm (which I think could be called EncodedForm?)"* and states "hedged-lean /
review-later. NOT blocked-on-psyche — it blocks nothing... No rename executed on a
hedge." The only 2026-07-17 rulings adjacent to it are `.31` (String stays String)
and `.36` (single-field brace = newtype); both cite the form-vocabulary only as the
*cause* of a bug, not to bless a rename. So the follow-up "rename lane" is premised
on a ruling that has not happened — see Decision item 1.

## Revisions read (a concurrent `LanguageEngine/DaemonPort` lane is Active)

Working-copy commit ids at read time (`repos/<name>`):

```
nota 4c98c87ba16e · core-schema e5f1c69699ba · core-nomos fb420bc21332
core-logos c6429182bad2 · textual-rust 893e82d811dc · structural-codec 5ef3d03a602e
structural-codec-derive 33c14d25cbc2 · raw-discovery d3622785d3af
name-table 2f4112cfc748 · content-identity 4a6b20472a8a
schema-language f1cc35f96ac5 · schema eadfb7a6ccb6 · schema-rust 8ecc5b2d6613
language-engine-witness 5709590c1910 · nomos-engine 836793f0be50
logos-engine bc158f1280fd · sema-engine 0904218556ce
```

Witness pins (delivered runtime, `language-engine-witness/Cargo.toml`): logos-engine
`d67d2e88`, nomos-engine `f129677f`, schema-engine `bf05d105`, schema-language
`4270fbda`, schema-rust `79a9e5c9`, sema-storage `a088dc14`, name-table `c3237f77`,
signal-{schema,nomos,logos,sema-storage,frame}. The live `LanguageEngine/DaemonPort`
lane (Generalist, "port daemons onto new language engine") held **no repo path
claims** during this review, so no engine repo was mid-commit under me; re-verify
these ids if acting later.

# Deliverable 1 — Per-language syntax sheet (real examples + divergences)

The design's "five languages" are NOTA (substrate), the human **schema** dialect,
**Nomos** (macro/transformation), **Logos** (Rust-equivalent data), and the
**textual projections**. The single most important finding for this deliverable:
**of the projected `Textual*` family, only `TextualSchema` and `TextualRust` are
built. `TextualNomos` is explicitly deferred and `TextualLogos` does not exist.**
The real pipeline is text only at the two ends: `core-nomos/tests/pipeline.rs:3`
— *"schema TEXT -> CoreSchema -> Nomos macros -> CoreLogos -> TextualRust -> Rust"*.
Nomos and Logos move as **data**, never text, today.

## 1. NOTA — the positional substrate

Two implementations coexist: the **legacy `nota` crate** (still the parser
`schema-language` depends on — `schema-language/Cargo.toml:20`, git main) and the
**lifted `raw-discovery` crate** (the next-gen raw layer). They disagree on grammar.

Next-gen (raw-discovery / nota `next-gen`) rules, each with a real witness in
`nota/tests/next_gen_grammar.rs`:
- Glued dot binds head→payload as one application: `Variant.Data` (`:19`).
- Right-associative chaining: `A.B.C = A.(B.C)`; `Private.secretDigest.StateDigest`
  reads `visibility, (name, type)` (`:52-66`). **Matches vision** (dotted
  right-associative delimiters).
- Each delimiter kind binds as payload: `Variant.(a b)`, `.[a b]`, `.{a b}` (`:29-46`).
- Period binds **only when glued both sides**; `Head .Payload` is an error (`:69`).
- Delimiter roles (`up-close-design-v1.md:751-757`, nota header): `{}` structs,
  `[]` vectors, `()` payloads, `(| |)` multiline strings.

**Divergence — two live grammars.** The legacy nota still uses the older macro-node
grammar with space-separated elements and `*` cardinality markers:
`nota/tests/fixtures/macro-node/strict-namespace.nota` reads `Entry { Topics * Kind * }`
(space before brace, `*` for repeat) — versus next-gen `Entry.{ Topics Kind }`
(glued dot, no `*`). schema-language rides the legacy grammar; core-schema rides
raw-discovery. This is the "settled-wave grammar migration" still open as `.5`/`.6`.

## 2. The human schema dialect — real, round-trips, closest to vision

Real fixtures the witness drives end-to-end
(`language-engine-witness/tests/fixtures/spirit-min.schema`, verbatim):

```
Topic.String
Topics.Vector.Topic
Description.String
Summary.{ Description }
RecordIdentifier.Integer
Entry.{ Topics Kind Description Magnitude }
Query.{ Topic Kind }
RecordSet.Vector.Entry
Kind.[Decision Principle Correction Clarification Constraint]
Magnitude.[Minimum VeryLow Low Medium High VeryHigh Maximum]
```

Decode is by **expected type at the boundary** (never content-guessed):
`core-schema/tests/textual_roundtrip.rs:41-46` calls `textual.decode(COMMIT_SEQUENCE,
source, &mut names)` — the caller passes the type; the parser never selects it.
`TextualSchema` is the only concrete `Textual*` struct (`core-schema/src/textual.rs:41`).

Vision-rule conformance (all **verified present** in code):
- **Dotted right-associative:** `Topics.Vector.Topic` = `Vector` applied to `Topic`,
  bound right-associatively (nota `:52`).
- **Generics by kind, no head-string dispatch:** `core-schema/src/reference.rs:4`
  — *"application dispatches on its kind and projection, never on a head string."*
  `CoreReference` (`:44-63`): `String|Integer|Boolean|Bytes|Plain(Identifier)` plus
  `SingleTypeReferenceProjection {Vector|Optional|ScopeOf}`, `MultiTypeReferenceProjection
  {Map}`, `ValueReferenceProjection {Bytes}`. So `Vector`/`Map`/`Optional` are
  **kinds**, not names — matches vision exactly.
- **Elided field names derived; explicit name is `camelCase.Type`:** the struct
  fixture `DatabaseMarker.{ CommitSequence StateDigest secretDigest.StateDigest }`
  exercises BOTH `Field` alternatives against the real layout
  (`textual_roundtrip.rs:70-90`): two elided-derived, one explicit
  (`secretDigest.StateDigest`). Matches vision.
- **Single-field brace = newtype:** `Summary.{ Description }`. Ruled newtype
  (`.36`, verbatim "2. newtype"); native decode's earlier single-field-**struct**
  reading converged (dispatched Session EnginePerfection / RulingConvergenceSlice).
  `core-schema/src/document.rs:148,155` seats `DeclarationRole::Newtype` first-class.
  **Verified at the role level; a `Summary`-specific round-trip test was not located
  — see Decision item 4.**
- **Elided String scalar is `String`:** `.31` ruled *"Strings are Strings"* — the
  scalar keeps the spelling `String`. `core-schema/src/reference.rs:80-92` records
  the ruling in the docstring and `:150-155` `from_atom` maps `"String" => String`.
  The superseded `Text`/`text` lean is gone. **Textual-vocabulary-bleed is fixed**
  here (this was exactly the bleed the rule forbids — see §naming).

**No brief-listed divergence survives on the schema dialect** beyond the two-grammar
split (§1) and the un-round-trip-tested newtype convergence (item 4). This is the
language closest to the psyche's vision.

## 3. Nomos — the macro/transformation language: Core exists, **syntax is deferred**

CoreNomos is real **as data**: `core-nomos/src/definition.rs:13` `MacroDefinition
{ name, kind, input, template }` — *"a macro is a value... No behavior, no text."*
Input meta-shape is the `{ Name Type }` model (`up-close-design-v1.md:54`); a real
registration (`core-nomos/tests/pipeline.rs:522-548`) builds `WireNewtype` with
`InputSignature { name.Name, type.Type }`, `MacroKind::Structural(SectionDefault::
Newtype)`, and a `ResultTemplate::Item(Newtype{...})` whose fields are `Escape::
Realize`/`Escape::Invoke` — the macro is authored **in Rust, not in Nomos text**.

**Divergence — Nomos has no concrete syntax yet.** The design says Nomos owns its
own syntax = NOTA's delimiters **plus** the `$` sigil and `<<>>` template escapes
(`up-close-design-v1.md:846-847`; slate `.9(c),(f)`). In code this is **explicitly
deferred**: `core-nomos/src/lib.rs:9-12` — *"What is here (CoreNomos), and what is
deferred (TextualNomos) ... TextualNomos — the `$` / `<<>>` [text spelling]"*;
`core-nomos/src/template.rs:8` — *"The `$name`/`<<name>>` text spelling of an escape
is TextualNomos, which is [deferred]."* So the Nomos macro/transform language runs,
but **you cannot write a Nomos macro as text today** — it must be constructed as
CoreNomos data. The `$`-sigil / `<<>>` slate is also still psyche-non-rejected, not
blessed (`.9`).

## 4. Logos — the Rust-equivalent data language: real algebra, **no text form**

CoreLogos is the closed Rust-as-data algebra: `core-logos/src` has `item.rs`,
`newtype.rs`, `struct`/`structure.rs`, `enumeration.rs`, `alias.rs`, `impl_block.rs`,
`function.rs`, `generics.rs`, `attribute.rs`, `path.rs`, `type_reference.rs`,
`visibility.rs`, etc. — one file per Rust construct. Totality is structural (design
§6.2, `up-close-design-v1.md:908-910`): a non-projecting node is a compile error.

**Divergence — `TextualLogos` does not exist.** The design's many-forms family
(`up-close-design-v1.md:848` `TextualLogos over CoreLogos`) and its worked logos
text `Public.CommitSequence.{ Integer }` (§7.5, `:1067`) are **not implemented**.
`core-logos` renders only through the `TextualRust` sibling (`core-logos/src/lib.rs:9`);
there is no logos-text encode/decode. A grep for `Recognizer`/`textual`/`to_text`
in `core-logos/src` finds only `domain.rs`. Logos is a **data language with exactly
one projection today: Rust.**

## 5. Textual projections that actually exist

- **TextualRust** (`repos/textual-rust`): the two-way Rust bridge, `syn` on decode
  and `prettyplease` on encode (`textual-rust/src/lib.rs:3`; `read.rs`, `project.rs`,
  `codec.rs`). It is **byte-exact against real schema-rust goldens** — provenance in
  `textual-rust/tests/fixtures/PROVENANCE.md` (copied from schema-rust @87de872);
  the capstone proves 153 items (`core-nomos/tests/pipeline.rs:7`). Example golden
  (`pipeline.rs:29-33`): `pub struct CommitSequence(Integer);` with `#[rustfmt::skip]`
  + derive attributes. **Crucially, TextualRust does NOT use the structural side-data
  table** (no `AddressedStructuralTable`/`StructuralEntry` reference in
  `textual-rust/src`) — it is `syn`/`prettyplease`-driven, exactly as designed
  (foreign raw layer, `up-close-design-v1.md:869-877`).
- **TextualSchema** — §2 above; the one structural-table-driven form.
- **NOTA raw** — §1; the substrate both legacy and next-gen readers share.

**No JSON / YAML / TOML / serde projection exists anywhere** in the family: a grep
for `serde_json`/`serde_yaml`/`toml::`/`to_json` across core-schema, core-nomos,
core-logos, structural-codec, textual-rust, nota `src` returns nothing. The only
"other language" surface the design contemplates is additional `TextualForm`
back-ends (C/Zig), none built. So the complete projection inventory today is:
**NOTA-raw, schema text (TextualSchema), Rust text (TextualRust).** Two of the five
languages (Nomos, Logos) have **no human-writable syntax in code.**

# Deliverable 2 — Naming state: the TextualForm / EncodedForm pairing

## What the pairing names, and its true status

The pair distinguishes the **two ways to see one language**: the human **text**
view and the **stringless rkyv-encoded Core** value. Design vocabulary today:
`TextualForm` (the text-side codec trait, `up-close-design-v1.md:837`) versus the
**Core-side** representation (unnamed as a "form"; the psyche floated `CoreForm →
EncodedForm`). Status is a **hedged lean, not a ruling** (`.37`; see §0). It is
tangled with two things the psyche *did* rule:
- `.25`: **Core\* type prefixes stay** ("Core remains the canonical stringless data
  layer name"). So any `EncodedForm` rename applies to the **form-view vocabulary**,
  not to the `Core*` type names — these must not be conflated.
- `.31`: the form vocabulary **bled into a type name** (`Text`/`text` scalar) and was
  reverted to `String`. This is the concrete harm the "no Textual-layer bleed" rule
  guards, and the psyche's own causal diagnosis for why he raised the rename.

## Complete touch-map for a follow-up rename lane

**Finding: there is no code identifier named `TextualForm`, `CoreForm`, or
`EncodedForm` anywhere** (grep across core-schema, core-nomos, core-logos,
textual-rust, structural-codec `src`). The abstraction is **report-and-epic only**;
the code has concrete `TextualSchema`/`TextualRust` (+ deferred `TextualNomos`) and
the `Core*` type family. A rename is therefore **small and doc-scoped**, not a code
refactor. Every occurrence to touch:

Reports (`reports/logos/`):
- `up-close-design-v1.md:828, 837, 941` (the `TextualForm` trait + family prose).
- `vision-evidence-ledger-v1.md:125, 231, 485` (L13 the `Textual*` name; the
  two-concept split `TextualForm` vs `StructuralForm`).
- `language-family-poc-epic-design-v1.md:161, 393` ("the concrete `TextualForm`
  trait"; "A `TextualForm` is proposed as a codec family object").

Epic:
- `.37` — the tracking item itself (retitle/close on ruling).
- `.31` close-reason and `.36` reference the pairing as causal context (update only
  if the vocabulary name changes).

Code (only **if** the psyche wants the abstraction *introduced* as a named trait —
this is new design, not a rename): the design's `TextualForm` trait (`up-close-
design-v1.md:837`) is unimplemented; `TextualSchema`/`TextualRust` are standalone
structs. There is nothing named `CoreForm`/`EncodedForm` to rename in code.

**Tracked rename work item:** none exists beyond `.37` (the hedged-lean tracker,
P4). There is no execution/rename bead. A rename lane cannot proceed until `.37` is
ruled (Decision item 1).

# Deliverable 3 — Side-data (structural-table) survey

## Where it lives and its shape

The side-data is the **external structural table**, `structural-codec/src/table.rs:90`
`AddressedStructuralTable` — the sidecar keyed by `ScopedCoreTypeId`, with its own
content identity **excluded from the Core hash** (`table.rs:1-5`). Shape:
- `AddressedStructuralTable` methods (`table.rs:96-129`): `seal(revision, payload)`,
  `revision()`, `identity()`, `entry(expected: ScopedCoreTypeId)`, `validate_disjoint()`.
- `TableIdentityPayload` (`table.rs:66-75`): `core_universe`, `core_layout_identity`,
  `raw_profile_identity`, `committed_lexicon` (exact glyph bytes), `leaf_codec_contracts`,
  `entries: BTreeMap<ScopedCoreTypeId, StructuralEntry>`. Hash stored **outside** the
  payload (self-reference-bug fix).
- Per entry: `StructuralEntry` (`codec.rs:51`) = `Vec<ConstructorCodec>`; each
  `ConstructorCodec` (`codec.rs:16`) = `decode_forms: Vec<StructuralForm>` (disjoint
  accepted inputs), one canonical `encode_form`, positional `signature`. Forms are
  built from `structural-codec/src/form.rs`: `StructuralForm`, `AtomForm`, `LeafForm`,
  `SequenceForm` (Product/Repeat), `DottedForm`, `AuthoringForm`.
- It is **built once, at the schema layer**: `core-schema/src/document.rs:184-208`
  assembles `entries` and calls `AddressedStructuralTable::seal(...)`.

## Every use it serves today, and its status

| Use | Status | Evidence |
|---|---|---|
| **Decode** schema text → CoreSchema by expected type | **Implemented** | `core-schema/src/textual.rs`; `structural-codec/src/evaluator.rs`; driven by `table.entry(expected)` (`table.rs:122`) |
| **Encode** CoreSchema → canonical schema text | **Implemented** | `textual_roundtrip.rs:60-66` round-trips byte-exact |
| **Disjointness safety** (no silent form conflict) | **Implemented, conservative** | `structural-codec/src/disjoint.rs:114` `validate_disjoint` returns `NotProvablyDisjoint` (safe-reject direction), called per entry (`table.rs:127-129`) |
| **Content identity** of the table, co-versioned, excluded from Core hash | **Implemented** | `table.rs:1-5,116` `identity()` over `TableIdentityPayload` |
| **Interpreter≡codegen conformance** | **Implemented (harness)** | `structural-codec/src/conformance.rs`, `tests/conformance_harness.rs` |
| **Help / usage printing** from the table | **Missing in the new engine** | Help exists ONLY as **legacy** `schema-language/src/source.rs:3865-4028` (`HelpRendering`, `fn help`) over the OLD source model; nothing in `structural-codec`/`core-schema` renders help from `AddressedStructuralTable`. `nota/src/expectation.rs:30` has a `DottedExpectation::description` for diagnostics only. |
| **Rename support** via side-data | **Not a side-data feature (handled elsewhere)** | Rename is hash-stable **by NameTable exclusion**, not by the structural table: `core-schema/src/reference.rs:72`, `declaration.rs:16,101`, `content_hash` drops `names` (`schema-unit-lineage-design-v2.md:143-146`). The v1 rename-intent alias was **deleted** (v2 §6). So "renaming support" is a NameTable property; the structural table plays no part. |
| **Passing data to the next language layer** | **Not carried by side-data** | The schema→nomos→logos hand-off passes **Core values + the continuous NameTable only**, never the structural table: `core-nomos/src/engine.rs` `Lowering { items: Vec<CoreItem>, names: NameTable }`. The NameTable is `extend_from`-continuous (schema indices preserved). The structural table stops at the schema layer. |
| **Nomos / Logos structural tables** (`TextualNomos`/`TextualLogos`) | **Missing** | Only `TextualSchema` builds a table (§Deliverable 1.3–1.4). `TextualRust` deliberately uses none. So the "many-forms" side-data is realized for **one** language. |

## Gap statements (exists vs missing) + recommendation, source-anchored

1. **Help/usage projection off the structural table.** *Exists:* a legacy
   `HelpRendering` over the old source AST (`schema-language/source.rs:3865-4028`),
   and rich per-element form data (`ConstructorCodec.decode_forms`) that already
   describes every accepted shape. *Missing:* any renderer turning
   `AddressedStructuralTable`/`StructuralForm` into help/usage text in the new
   engine. *Recommendation:* the side-data is the natural help source (it already
   holds the disjoint accepted forms per constructor); add a `StructuralForm →
   usage-text` projection in `structural-codec` rather than porting the legacy
   renderer. Small, and it makes the table earn a second use. **Not started; needs a
   design pass — see Decision item 3.**

2. **Next-layer data flow.** *Exists:* NameTable continuity (`extend_from`) carries
   identifiers schema→logos. *Missing:* any structural side-data crossing the
   boundary. This is arguably **correct** (the structural table is a *text-view*
   concern; the next layer consumes Core + names), but the design's "many-forms
   family sharing the vocabulary" implies each layer has its own table, and only
   schema does. *Recommendation:* confirm the boundary is intentional — the table is
   text-side-only and does **not** propagate — and record it, so a future reader does
   not treat the absence as a bug. **Decision item 2.**

3. **Nomos/Logos textual tables.** *Exists:* schema's table. *Missing:* `TextualNomos`
   (deferred, `core-nomos/lib.rs:9-12`) and `TextualLogos` (never built). *Recommendation:*
   these are the real "under-developed because never discussed in depth" gaps the
   psyche suspects. Nomos-as-text and Logos-as-text are genuine language surfaces the
   design promises but code omits. Sequence them explicitly (they are latent in
   `.2`/`.7` but not scoped as "build the text form"). **Decision item 3.**

# Deliverable 4 — Decision items needing psyche ruling

1. **Rename the Core-side form view to `EncodedForm`? (`.37`)** — *What:* the
   text-view/Core-view pairing is `TextualForm` vs an unnamed Core-side form; the
   psyche floated `CoreForm → EncodedForm` as a hedge, never ruled. *Options:*
   (a) adopt `TextualForm`/`EncodedForm` as the settled pair and run the doc-scoped
   rename lane (touch-map above; ~8 report lines + `.37`); (b) keep the current
   vocabulary and close `.37`; (c) defer to the deferred design-authority review.
   *Recommendation:* **(a)** — the names are clear and orthogonal to the `.25` ruling
   that `Core*` **type** prefixes stay (EncodedForm names the *view*, not the types),
   and naming the pair removes the ambiguity that already caused the `.31` `Text`/`String`
   bleed. But note it needs no code change today — there is no `CoreForm`/`TextualForm`
   identifier in code — so this is low-cost and reversible. *Reason:* a named pair
   prevents recurrence of vocabulary-bleed; cost is ~8 report lines.

2. **Is the structural table intentionally text-side-only (does not cross language
   layers)?** — *What:* the schema→logos hand-off carries Core + NameTable, never the
   structural table (`core-nomos/engine.rs` `Lowering`). *Options:* (a) confirm
   intentional and record it as the boundary; (b) design table propagation if a
   downstream layer must see accepted forms. *Recommendation:* **(a)** — the table is
   a text-view concern; the next layer consumes typed Core, so propagation would
   re-introduce text dependence the identity ruling forbids. *Reason:* matches the
   "Core never depends on text" law; only needs recording so absence ≠ bug.

3. **Build the missing text forms (`TextualNomos`, `TextualLogos`) and a table-driven
   help projection — now or deferred?** — *What:* Nomos has no writable syntax
   (`core-nomos/lib.rs:9-12` deferred), Logos has no text form at all, and help exists
   only in legacy schema-language. These are the "under-developed" surfaces.
   *Options:* (a) scope all three now as first-class slices; (b) scope only Nomos text
   (its `$`/`<<>>` slate `.9` is the most-designed); (c) keep deferred until the PoC
   port (`.39`) proves the data path. *Recommendation:* **(c) then (b)** — the witness
   pipeline is byte-exact through data today (`core-nomos/tests/pipeline.rs`), so the
   PoC does not need the text forms; but Nomos-as-text is the next honest gap once the
   port lands, because a human cannot author a macro without it. *Reason:* sequence by
   what blocks a human author, not by design completeness.

4. **`Summary.{ Description }` newtype convergence — confirm with a round-trip test.**
   — *What:* `.36` ruled single-field brace = newtype and convergence was dispatched;
   `DeclarationRole::Newtype` is seated (`core-schema/document.rs:148`), but this lane
   did **not** locate a `Summary`-shaped round-trip test proving the native decode now
   yields a newtype (the located tests cover `CommitSequence` newtype and
   `DatabaseMarker` struct). *Options:* (a) treat as done on the ruling + role seat;
   (b) require a spirit-min `Summary` round-trip witness before closing `.36`.
   *Recommendation:* **(b)** — the divergence was originally proven by ingesting
   spirit-min through both front ends (`.36` evidence, schema-engine
   `tests/equivalence.rs`); the convergence deserves the symmetric witness. *Reason:*
   cheap, and closes the parity claim on the real fixture rather than a purpose-built one.

## Validation scope

Read-only. No engine source, generated artifact, store, deployment, or Spirit record
changed. All code claims are this lane's direct `file:line` reads at the revisions
above; ruling claims cite epic item ids and their recorded verbatim psyche text.
Lane `LanguageEngine/SyntaxSideDataReview` registered Fresh; this file is its only
artifact.
