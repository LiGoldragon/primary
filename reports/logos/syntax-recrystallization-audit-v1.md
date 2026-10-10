# Syntax recrystallization audit v1 — NOTA / Schema / Nomos / Logos / Rust

Deep audit and recrystallization of the TEXT SYNTAX of the next-generation
language stack. "Recrystallization" here re-derives the cleanest syntax from the
psyche's confirmed rulings, treating current code as evidence and rulings as
constraints. Written 2026-07-14 (session `NextgenRecrystallization`, lane
`SyntaxRecrystallizationAudit`, generalist, Opus 4.8, 1M).

Discipline: **[observed]** is worker-verified with a source citation;
**[interpretation]** is mine; **[AGENT PROPOSAL]** needs a psyche ruling; a
conflict with a ruling is marked **[PROPOSED REVERSAL]** and never silently
adopted. This report invents no rulings.

## 0. Method and the one load-bearing update since the design record

Grounded in `reports/logos/design-v0.md`, `nota-grammar-revision-v0.md`,
`syntax-mockup-v2.md`, `nomos-macro-model-v1.md`, `architecture-v0.md`,
`delimiter-semantics.md`, `reports/codex-rust-construct-survey.md`, the
`reports/logos/samples/`, and a read-only sweep of the `nota` repository at
`remotes/origin/next-gen` (v0.8.0, load-bearing commit `56a6372` "raw
dot-application binding + delimiter reshuffle", `86bd87d` "dotted data variants
in nota-derive + struct brace bodies").

**[observed] The single most important fact for this audit: the delimiter
reshuffle and right-associative dotted application have LANDED in code, and are
tested, even though the dated design reports (2026-07-11) still label the
reshuffle `[LEANING]`.** On `origin/next-gen`:

- Dot-application binds as **one** raw `Application { head, payload }` node;
  `parse_atom` stops at `.` so the period is a structural operator, never atom
  text (`src/parser.rs:724-746, 848-863`; test `tests/next_gen_grammar.rs:18-45`).
- The dot is **right-associative**: `A.B.C = App(A, App(B, C))`
  (`src/parser.rs:67-68, 716-717, 735`; test `dotted_chain_binds_right_associatively`
  on exactly `Private.secretDigest.StateDigest`, `tests/next_gen_grammar.rs:52-61`).
- Delimiters are reassigned: struct/record → `{}` (`derive/src/lib.rs:228,298,602`),
  vector → `[]` (`src/codec.rs:566,926`), map → `Map.( key.Value … )` parenthesis
  application (`src/codec.rs:590-604,971`), option → `None` / `Some.payload`
  (`src/codec.rs:616-641`), single-field variant → `Tag.payload`
  (`derive/src/lib.rs:580-587`).
- Floats reconstruct from dotted text: `-122.3 = App(-122, 3)`, rejoined by the
  Float codec (`src/codec.rs:440-460`; round-trip test `:106-111`).
- Period-bearing strings must use `(| |)` (`src/codec.rs:489-521`).
- **Exception:** `StructuralMacroNode` did NOT migrate; it is still the headed
  `(Head body)` parenthesis form (`derive/src/lib.rs:927-935, 1163-1266`).

**[interpretation]** So scheme-b (the reshuffle) is no longer "leaning" as an
engineering fact — it is the implemented, green ground truth. The recrystallized
design below adopts it as settled-in-code, and the doc/code status mismatch is
itself the first ledger item.

## 1. Discrepancy ledger

Each row: the layers involved, a concrete example, why it costs cognition, and
severity. Rated by cognitive-simplicity cost, the audit's brief.

### D1 — Reshuffle is `[LEANING]` in the reports but `[LANDED]` in code — HIGH

- **Layers:** NOTA, Schema, Logos.
- **Example:** `nota-grammar-revision-v0.md:43-52` and `syntax-mockup-v2.md:137-184`
  present the psyche-authored base with struct payloads as `.( … )` and mark
  `{}`=struct only `[LEANING]`; the code writes structs as `.{ … }` and has for
  two commits.
- **Cost:** a fresh reader who grounds in the reports believes a struct body is
  `Kind.( … )`; a reader who grounds in the code sees `Kind.{ … }`. The canonical
  struct delimiter is genuinely ambiguous across the two sources of truth.
- **Resolution:** the reports are stale on this point; code is ground truth.
  Adopt scheme-b everywhere (this report does). Ruling 24 ("wave one includes the
  delimiter reshuffle") already authorizes it; the docs simply predate the land.

### D2 — Field-name elision contradicts the 1-to-1 "nothing materializes" ruling — HIGH

- **Layers:** Schema, Logos, Rust.
- **Example:** text logos `Public.CommitSequence` (a field) carries **no** field
  name, yet the Rust is `pub commit_sequence: CommitSequence`. The name
  `commit_sequence` appears at projection, derived from the type by the
  snake_case rule. The repeat `Private.secretDigest.StateDigest` DOES carry a
  name. So a normal field is a 2-node application `App(Public, CommitSequence)`
  and a repeat field is a 3-node `App(Private, App(secretDigest, StateDigest))`.
- **Cost:** two frictions. (i) The name materializes at projection from the type,
  which directly contradicts ruling 1.1 ("everything in the Rust is represented
  in logos; nothing materializes at projection; field names computed by Nomos but
  **stored explicitly in logos**"). (ii) The reader must run the snake_case rule
  in their head to know a field's name — the sharpest "invisible context" in the
  whole stack, and a special case (repeat) stacked on the normal case (derive).
- **Resolution (recrystallized, §2.3):** in **CoreLogos** every field carries its
  name uniformly (`App(Vis, App(name, Type))`); the **text projection** elides the
  name exactly when it equals `snakeCase(Type)`. This satisfies 1-to-1 (the name
  is present in core, nothing is invented at Rust projection — it is transcribed
  from core) and dissolves the arity special case (all fields are 3-node in core;
  text shows 2-node iff the name is the canonical derivation). Elision is a
  legitimate text compression because CoreLogos and text are explicitly different
  layers (`design-v0.md §2`).

### D3 — The `.` glyph carries six roles — MEDIUM (principled, total, but real load)

- **Layers:** all.
- **Roles:** (1) application/variant binding `Public.Newtype`, `Some.42`;
  (2) right-associative nesting `A.B.C`; (3) path segment `rustfmt.skip`,
  `rkyv.[…]`; (4) key.value pair `host.prometheus`; (5) visibility.name.type chain
  `Private.secretDigest.StateDigest`; (6) float decimal `-122.3`.
- **Cost:** to grasp any `A.B` a human must read both operands' capitalization /
  numeric-ness. At the **machine** level "the parser never classifies" holds (the
  raw layer always makes an `Application`; the codec interprets by expected type).
  At the **human** level, capitalization is the classifier and the reader must
  apply it.
- **Mitigant / why only MEDIUM:** the disambiguation is **total** on operand kind
  alone — CapitalizedLeading.Capitalized = application/variant;
  lowercase.lowercase-value = pair or path; digits.digits = float. No hidden
  context is consulted. The design is coherent; the cost is that one glyph does a
  lot, learned once. The evolution risk (a seventh non-total role) is in §4.

### D4 — `Head.[vector]` means WRAP or DISTRIBUTE depending on the head — MEDIUM

- **Layers:** Logos, Rust.
- **Example:** `rkyv.[Archive Serialize Deserialize]` **distributes** the prefix
  → `rkyv::Archive, rkyv::Serialize, rkyv::Deserialize`; `Derive.[ … ]` **wraps**
  a single derive attribute over a list. Same surface `Head.[…]`, two projections.
- **Cost:** the reader must apply the capitalization invariant — lowercase `rkyv`
  is a path-prefix (distributes over the vector), capital `Derive` is an object
  (wraps the vector as its payload) — to know which projection applies.
- **Severity:** MEDIUM. This is the capitalization invariant doing real semantic
  work; acceptable, but it is a genuine place where identical surface diverges and
  should be named as such in the grammar page.

### D5 — `Literal` payload: opaque string vs dotted path — MEDIUM

- **Layers:** Logos, Rust.
- **Example:** `Literal.[rustfmt.skip]`. Is `rustfmt.skip` opaque literal text
  (projects `rustfmt.skip`) or a dotted path (projects `rustfmt::skip`)? The Rust
  oracle is `#[rustfmt::skip]` with `::`, so it MUST be a dotted path — which
  means `Literal` is **not** an opaque escape hatch here, despite its name.
- **Cost:** the name "Literal" implies opacity; the content is a structured path
  that projects `::`. The reader is misled about both the payload's type and its
  projection. Compounded by an unsettled delimiter (`[…]` vector-of-one vs `(…)`
  vs `(| |)`).
- **Resolution:** proposal (h) — dotted path, `Literal.( rustfmt.skip )`; reserve
  `(| |)` for genuinely opaque text.

### D6 — Map `Map.( … )` uses `()` while a struct instance uses `{}` — LOW

- **Layers:** NOTA, Schema, Logos.
- **Example:** a map is `Map.( key.Value … )` (parenthesis payload); a struct
  instance is `Name.{ … }` (brace). Both are collections of dotted pairs, but with
  different delimiters and different pair shapes (map `key.Value` vs field
  `Vis.name.Type`).
- **Cost:** minor; the capitalized `Map` head disambiguates, and `()` is the
  ruled payload bracket ("a map is one kind of payload", ruling 11). Named for
  completeness.

### D7 — Nomos escapes do not bind in generic nota — LOW (implementation gap)

- **Layers:** Nomos.
- **Example:** `$name` reads as a plain bare atom and `$(WireAttributes)` splits
  into `$` + `(WireAttributes)`; `<<name>>` mis-lexes as a bare atom
  (`nomos-macro-model-v1.md:240-263`, confirmed against 0.7.0 and unchanged by the
  0.8.0 lexer, which still treats `$`, `<`, `>` as bare-safe).
- **Cost:** the Nomos samples "parse" without carrying escape meaning, so
  parseability does not validate them. Expected — Nomos owns its grammar — but a
  reader can be misled that a sample works. Resolved by proposal (d): Nomos owns
  one escape token.

### D8 — `StructuralMacroNode` still headed while everything else is dotted — MEDIUM

- **Layers:** NOTA (derive/codec).
- **Example:** ordinary variants encode `Variant.payload`
  (`derive/src/lib.rs:580-587`), but `StructuralMacroNode` still encodes the
  headed `(Head body)` parenthesis form
  (`derive/src/lib.rs:927-935, 1258-1266`).
- **Cost:** a reader who internalized "data variants are dotted" meets a headed
  exception precisely at the macro-node layer — the layer meant to be most
  legible. One construct violates the universal encoding.
- **Resolution:** proposal (a) — convert to dotted.

### D9 — Stale v0 Nomos samples contradict the v1 rulings — LOW/MEDIUM

- **Layers:** Nomos.
- **Example:** `samples/types-section.nomos` and `samples/v2-nomos-macros.nomos`
  still use `Macro.` heads, `Input.`/`Result.`/`Match.`/`Arity.` label heads, and
  lowercase `wireNewtype` — all superseded by rulings 25a/25b/26 (headless,
  positional sections, capitalized macro names) and the inline-struct input
  (statement 27). Three contradictory Nomos syntaxes now sit side by side in
  `samples/`.
- **Cost:** a reader browsing samples cannot tell which Nomos syntax is current.
  (This report does not edit existing files; flagged for a later samples-hygiene
  pass — see feedback at end.)

### D10 — nota `ARCHITECTURE.md` describes maps as a brace block; code uses `Map.( … )` — LOW

- **Layers:** NOTA.
- **Example:** `ARCHITECTURE.md:184,363` (origin/next-gen) calls a map a "brace
  block" of `key.value` entries; the implemented `parse_map`
  (`src/codec.rs:590-604`) requires the `Map.( … )` **parenthesis** application.
- **Cost:** the normative-looking doc misdescribes the implemented map form.

### D11 — Nomos meta-types capitalized, accessors lowercase-derived — LOW (virtuous consistency)

- **Layers:** Nomos.
- **Example:** input shape `{ Name Type }` (capitalized meta-types) yields body
  accessors `name`, `type` (lowercase, derived by the same snake_case rule as
  field names, `nomos-macro-model-v1.md:73-95`).
- **Cost:** the same invisible derivation as D2 recurs for macro accessors. This
  is actually a **virtue** — one derived-name rule spans struct fields, macro
  accessors, and (proposal c) synthesized names — but it inherits D2's invisible
  cost, so its resolution rides on D2's (core carries the name; text/derivation is
  the compression).

## 2. Recrystallized syntax design — the same worked example through all five layers

The pipeline is `CommitSequence` and `StateDigest` (newtypes over `Integer`) and
`DatabaseMarker` (a struct whose third field repeats `StateDigest`). Rendered
through every layer under the rulings, adopting the landed reshuffle and the
right-associative dot.

### 2.0 The one unifying insight

**[interpretation]** Right-associative dotted application (LANDED, tested) is the
keystone that dissolves most of the ledger. Because `A.B.C = A.(B.C)`:

- `Public.Newtype.{ body } = App(Public, Newtype.{ body })` — visibility is a
  **general modifier applied to a declaration**, not a minted `PublicNewtype`
  type. Ruling 2 (no type proliferation) is satisfied by composition.
- `Private.secretDigest.StateDigest = App(Private, App(secretDigest, StateDigest))`
  — the **same** visibility modifier applied to a **named field**.
- `Public.CommitSequence = App(Public, CommitSequence)` — the same modifier
  applied to a field whose name is the canonical derivation (elided in text).

So visibility uses one mechanism at declaration level and field level, and the
`Public.Newtype` "cross-product" objection evaporates — those are applications,
not types. This is already how the parser binds; the design only needs to name it.

### 2.1 NOTA (positional data substrate — instances)

```
None
Some.42
State.Running
Position.{ 47 -122.3 }
[ alpha beta gamma ]
Map.( host.prometheus port.5432 retries.3 )
DatabaseMarker.{ 42 7 7 }
```

`DatabaseMarker.{ 42 7 7 }` is a struct instance: three positional fields
(`commit_sequence`, `state_digest`, `secret_digest`), types known by expectation,
names never restated at the value layer. `-122.3` is `App(-122, 3)` rejoined by
the Float codec — no lexer special case.

### 2.2 Schema (brief human surface)

```
CommitSequence.{ Integer }
StateDigest.{ Integer }
DatabaseMarker.{ CommitSequence StateDigest secretDigest.StateDigest }
```

A newtype is a single-type brace; a struct is a multi-type brace; a repeated type
takes an explicit `name.Type` disambiguator (the same dotted pair used
everywhere). Struct delimiter `{}` matches logos `{}` and NOTA `{}` — one glyph,
one meaning, across all three.

### 2.3 Logos (Rust-equivalent data, exploded, non-sugared)

Text projection (canonical, names elided where derivable):

```
Public.Newtype.{
  CommitSequence
  [ Literal.( rustfmt.skip )
    ConfigurationAttribute.Feature.( nota-text [ NotaDecode NotaDecodeTraced NotaEncode ] )
    Derive.[ rkyv.[ Archive Serialize Deserialize ] Clone Debug PartialEq Eq ] ]
  Integer
}

Public.Struct.{
  DatabaseMarker
  [ Literal.( rustfmt.skip )
    ConfigurationAttribute.Feature.( nota-text [ NotaDecode NotaDecodeTraced NotaEncode ] )
    Derive.[ rkyv.[ Archive Serialize Deserialize ] Clone Debug PartialEq Eq ] ]
  [ Public.CommitSequence
    Public.StateDigest
    Private.secretDigest.StateDigest ]
}
```

CoreLogos (what the text elides — every field carries its name uniformly):

```
;; the DatabaseMarker field vector, in core:
[ Public.commit_sequence.CommitSequence
  Public.state_digest.StateDigest
  Private.secretDigest.StateDigest ]
;; text elides the name on rows 1-2 because it equals snakeCase(Type);
;; row 3 shows it because secretDigest != snakeCase(StateDigest).
```

Changes from the psyche-authored base, each licensed: struct payloads use `.{ }`
(reshuffle, landed); `Literal.( rustfmt.skip )` is a dotted **path** not a vector
or opaque string (proposal h); the derived field name is present in core and
elided in text (D2 resolution). Every Rust token is still homed:
`pub`→`Public`; `struct`(newtype)→`Newtype`, `struct`(record)→`Struct`;
`#[rustfmt::skip]`→`Literal.( rustfmt.skip )`; the `cfg_attr` gate→
`ConfigurationAttribute.Feature.( … )`; the derive block→`Derive.[ … ]`; wrapped
type→`Integer`; fields→the field vector.

### 2.4 Nomos (the schema→logos macro package)

```
;; Section 1 — named macros.
[
  WireNewtype.( { Name Type }
    Public.Newtype.{ $name $(WireAttributes) $type } )

  WireStruct.( { Name Fields }
    Public.Struct.{ $name $(WireAttributes) $fields } )

  WireAttributes.( { }
    [ Literal.( rustfmt.skip )
      ConfigurationAttribute.Feature.( nota-text [ NotaDecode NotaDecodeTraced NotaEncode ] )
      Derive.[ rkyv.[ Archive Serialize Deserialize ] Clone Debug PartialEq Eq ] ] )
]
;; Section 2 — structural macros (per-section positional defaults) omitted for brevity;
;; e.g. the "particular-struct" default that fires on an unknown Head.{ … } in a types section.
```

A macro definition is `Name.( <input-struct> <result-template> )`: a capitalized
macro name applied to a two-slot positional payload. The input `{ Name Type }` is
a struct shape over shared meta-types (proposal e), yielding accessors `name`,
`type` by the derived-name rule. `$name`/`$type` realize; `$(WireAttributes)`
recursively invokes and realizes (proposal d, c). The template body IS logos.
`WireStruct` delegates its field vector via `$fields`. Nomos adds exactly one
glyph to NOTA — the `$` escape (proposal g).

### 2.5 Rust (acceptance oracle, verbatim generated form)

```rust
#[rustfmt::skip]
#[cfg_attr(feature = "nota-text", derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct CommitSequence(Integer);

#[rustfmt::skip]
#[cfg_attr(feature = "nota-text", derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct DatabaseMarker {
    pub commit_sequence: CommitSequence,
    pub state_digest: StateDigest,
    secret_digest: StateDigest,
}
```

Logos→Rust is transcription: `.`→`::` on paths, brace/paren re-sugaring, derived
names realized from core. The migration is correct when this equals the Rust the
current `schema-rust` emitter already produces (the golden oracle, `design-v0.md §4`).

## 3. Recommended resolutions — the open syntax questions

Every item is an **[AGENT PROPOSAL]** needing a psyche ruling.

### (a) StructuralMacroNode: convert to dotted — PROPOSAL: YES

`StructuralMacroNode` is the one construct still on the headed `(Head body)`
parenthesis form (`derive/src/lib.rs:927-935,1258-1266`) while every ordinary
variant migrated to `Variant.payload`. **Convert it to the dotted form.**
Rationale: the universal dotted encoding should be truly universal; a lone headed
exception at the macro-node layer — the layer meant to be most legible — is the
worst place to keep a special case. Cognitive: a reader learns "data variants are
dotted" once and never meets a `(Head body)` counterexample. Cost: derive + codec
change + golden regeneration, the same staged, byte-verified migration the
reshuffle itself already followed.

### (b) Bless the three implemented readings — PROPOSAL: BLESS ALL THREE

They are landed, tested, and mutually reinforcing.

- **Right-associative dot** (`A.B.C = A.(B.C)`): bless. It is the keystone (§2.0):
  it makes visibility a general modifier at both declaration and field level,
  resolving proposal (f) for free, and it is tested on exactly the
  `Private.secretDigest.StateDigest` case.
- **Floats reconstructed from dotted text**: bless. `-122.3 = App(-122, 3)`
  rejoined by the Float codec when a Float is expected — the "parser never
  classifies" invariant working perfectly, with **no** lexer special case. The
  only caveat (§4) is that no slot may admit both a number and an application.
- **Period-bearing strings take `(| |)`**: bless, with a flagged **ergonomic
  cost**. Every string containing a `.` (filenames, URLs, versions, domains) must
  use `(|…|)`. This is the price of making `.` fully structural; the alternative
  (a string-vs-application ambiguity on every lowercase dotted pair) is worse.
  Flag: monitor dot-string frequency in authored NOTA; revisit only if it becomes
  dominant.

### (c) Name synthesis: fourth escape vs realize-with-transform — PROPOSAL: NO fourth escape

Model name synthesis as the **same canonical derived-name rule** that already
governs field names (D2) and macro accessors (D11): `$name` in a name position
yields the derived identifier; the snake_case function lives once in the seed
vocabulary as an identity transform, invoked as realize-of-a-transform. Keep the
escape set at two primitives (realize, splice) plus the recursive-call surface.
Rationale/beauty: adding `synthesizeName` would fork a rule already unified
across three sites; one derivation rule, learned once, serves fields, accessors,
and synthesized names. This is also the anti-complexity guard at the macro layer
(§4). Caveat honestly kept: the **gensym** case (minting a genuinely fresh binder
with hygiene) is narrower than snake_case derivation; if a macro ever needs a
fresh, collision-free identifier not derivable from an input, that is the one
place a fourth escape might still earn its keep — flag it, do not pre-build it.

### (d) Escape surface: `$` sigil vs bracket — PROPOSAL: `$` sigil

`$name` (realize), `$@items` (splice), `$(Macro args)` (recursive call): a
coherent single-char family matching the universal `$`/`#` macro convention. The
template body IS logos, so the escape should be the minimal visual intrusion
marking a hole. `<< >>` spends a whole delimiter pair and reads heavier; both are
equally nota-owned additions (neither binds in generic nota —
`nomos-macro-model-v1.md §6`), so the implementation cost is identical (one
nomos-owned lexical token) and the lighter surface wins.

### (e) Meta-types: nomos builtins vs shared schema seed — PROPOSAL: SHARED seed vocabulary

`Name`, `Type`, `Fields`, `Variants`, `Attributes` ARE schema's self-description
vocabulary. Schema is already self-describing and its `TypeReference`/`Name`
already unify into the seed crate `nota-next`
(`reports/schema-designer/25-schema-self-describing-design.md`). If they live once
in the seed crate, nomos's meta-types **are** those objects — shared, not
duplicated. Cognitive/evolution: one vocabulary across schema + nomos + logos, a
new meta-type added once and visible to all three, no drift between a schema
`Name` and a nomos `Name`. This is the psyche's stated lean; the seed-crate
precedent makes it the low-cost path.

### (f) Visibility in logos: outer variant vs variant field — PROPOSAL: OUTER, as right-associative application

With right-assoc dot (proposal b, LANDED), `Public.Newtype.{ … }` parses as
`App(Public, Newtype.{ … })` — the general `Public` visibility variant applied to
a general `Newtype` declaration. There is **no** cross-product and **no** type
proliferation (ruling 2 satisfied): `Public.Newtype` is composition of two
general objects, exactly as `Public.CommitSequence` composes visibility onto a
field. This unifies visibility at declaration and field level, matches the
psyche-authored base, and is already how the parser binds. The old objection —
outer form multiplies `Public.Newtype`/`Private.Newtype`/`Public.Struct`… — is
dissolved: those are applications, not node types. One rule: "visibility is a
modifier you apply by dotting it onto whatever it governs."

### (g) Nomos's own delimiters (unruled) — PROPOSAL: NOTA's delimiters unchanged, plus one `$` escape token

Nomos reuses the entire NOTA delimiter set with no reassignment, adding exactly
one nomos-owned lexical token (the `$` escape from proposal d). The macro
definition is `Name.( <input> <template> )` (application payload); the input is
`{ Name Type }` (struct brace); the two document sections (named macros,
structural macros) are `[…]` vectors; the template body is logos. Every glyph
already means what it means in NOTA; the only addition is the hole-marker.
Cognitive/evolution: a NOTA reader can read Nomos immediately — the transformation
language adds one glyph, not a grammar. The choice is the psyche's; maximal reuse
is the lowest-cognition option.

### (h) `Literal.[rustfmt.skip]` content: dotted path vs `(| |)` string — PROPOSAL: dotted PATH

`Literal.( rustfmt.skip )`, payload a two-segment dotted path
(`rustfmt.(skip)` by right-assoc) that projects `#[rustfmt::skip]` under ruling 7
(projection owns `.`→`::`). A `(| |)` string would be opaque and project the
literal text `rustfmt.skip` (no `::`, wrong). So the payload TYPE is "path," and
`Literal` should be read as "tool-attribute path," not "opaque literal." Reserve
`(| |)` strictly for genuinely opaque foreign text; multiple paths take a vector
`Literal.[ rustfmt.skip other.path ]`. This also fixes D5: the reader reads
`rustfmt.skip` as a path and knows it projects `::`, with no opacity guess.

## 4. Evolution analysis — staying simple as the system grows

### 4.1 Why Rust hit "exponential parsing complexity" (the failure to avoid)

**[interpretation, general knowledge]** Rust's grammar is context-sensitive with
unbounded-lookahead seams: `<` as generic-open vs less-than (the turbofish
`::<>` exists only to rescue this); `|` as closure-param vs bit-or; `{` as block
vs struct-literal (forcing struct-literal restrictions in `if`/`while`
conditions); `macro_rules!` accepting arbitrary token trees whose meaning cannot
be known without running the macro; and full expression-precedence climbing. The
parser is a fixed artifact every new feature must negotiate with the existing
ambiguities — so complexity compounds.

### 4.2 What the next-gen stack structurally excludes

- **Strictly-typed positional + expected type at every boundary.** The raw parser
  discovers structure (balanced delimiters, dotted application) and never
  classifies by lookahead; the codec interprets by the known expected type. Floats
  (`App` rejoined when a Float is expected), variants (unit atom vs `Tag.payload`
  when an enum is expected), and generics (`Vector.( Domain )` dotted application
  by kind, never `<>`) are all resolved by type, not by backtracking. The
  `<`-ambiguity cannot arise.
- **No operator precedence.** Everything is application/nesting via balanced
  pairs; no precedence-climbing, so grammar size does not grow with operators.
- **No sugar in logos** (ruling: exploded, non-sugared). There is nothing for a
  new construct to conflict WITH. Adding a Rust construct = adding a general
  structure + a lowering rule (data + a Nomos macro), never a parser change. This
  is the substance of "infinitely programmable, unlike Rust": programmability
  lives in Nomos, which transforms **typed objects** (with minted identities), not
  text token-trees — so a macro cannot introduce a parsing ambiguity the way
  `macro_rules!` can.
- **Capitalization as a total lexical classifier.** Object vs name is decided
  lexically, removing whole classes of Rust's context-sensitivity.
- **Dialect growth is additive.** A new dialect = a new Nomos macro package (table
  + structural rules): zero grammar change, zero parser change. The logos node
  vocabulary stays small (general structures + variant fields, ruling 2), so the
  ~150–250-node `syn` explosion is avoided by construction.

### 4.3 Where threats still lurk (guard each with an explicit invariant)

- **Totality of the dotted-operand disambiguation (D3).** The six roles are
  resolvable from operand kind alone today. A seventh dotted role that is NOT
  resolvable from operand capitalization/numeric-context would reintroduce human
  classification. Guard: every new dotted meaning must be total under the existing
  operand rules, or it does not ship.
- **The float/decimal seam.** `-122.3 = App(-122, 3)` is saved only by the
  expected type. Guard: no slot may admit both a number and an application; in a
  strictly-typed positional world this holds, but it is the one genuinely
  ambiguous raw form and the invariant that protects it must stay explicit.
- **Period-bearing string tax (proposal b).** A bounded ergonomic cost that grows
  with dot-string frequency, not a complexity explosion. Monitor, do not
  pre-optimize.
- **Nomos escape-set growth.** Keep it at two primitives + recursive call
  (proposal c). A growing escape vocabulary is exactly where a macro language
  re-accumulates Rust-macro complexity. This is the single most important macro-
  layer guard.
- **Self-hosting and macro recursion.** When schema defines its own Nomos packages
  (the stated end state), macro-expansion invoking macro-expansion needs hygiene +
  termination discipline (ruling 25e recursive calls must bound recursion; the
  gensym case in proposal c needs collision-free minting). Contained because
  expansion is over typed, minted-identity objects (no string capture), but
  termination must be enforced, not assumed.

Net: the stack excludes Rust's parsing-complexity failure modes structurally, and
concentrates all remaining risk at two well-marked seams — the totality of dotted
disambiguation and the boundedness of the Nomos escape set — both guardable by
explicit invariants the design can state now.

## 5. Agent feedback (doctrine/tooling friction)

- **Doc/code status drift (D1, D10):** the dated design reports still mark the
  reshuffle `[LEANING]` and describe maps as brace blocks, while `origin/next-gen`
  v0.8.0 has landed the reshuffle and uses `Map.( … )`. The reports have no
  "superseded by code as of commit X" banner, so a fresh reader can ground in a
  stale normative page. Owning surface: a short status stamp on
  `nota-grammar-revision-v0.md §1.3` and on nota `ARCHITECTURE.md` maps section.
- **Sample hygiene (D9):** three contradictory Nomos syntaxes coexist in
  `reports/logos/samples/`. A later samples-hygiene pass should retire the v0
  strawmans (`types-section.nomos`, `v2-nomos-macros.nomos`) or mark them
  `superseded`, leaving the v1 headless/capitalized/inline-struct form as the sole
  current example.
```
