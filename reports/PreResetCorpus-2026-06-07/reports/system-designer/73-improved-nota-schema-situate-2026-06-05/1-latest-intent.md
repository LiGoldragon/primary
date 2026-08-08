# Latest psyche intent — improved NOTA/schema mechanism

Read-only intent sweep of the deployed Spirit CLI (v0.5.0), 2026-06-05.
Topic clusters swept: schema / schema-next / schema-rust-next; nota /
nota-next / nota-design / codec; structural-macro / macro-node / macro;
asschema / schema-pipeline / emission; resolution / reactive-schema /
schema-language / derive / lowering / rust-emission; spirit / record-shape
(plus the redesign-overlap topics relations / weight / privacy / hash
identity). Only `Observe` was used; nothing mutated.

## 1. Synthesized current direction (dense prose)

The improved mechanism has converged, as of 2026-06-04/05, onto a
**three-stage pipeline with NO intermediate assembled-schema IR**, anchored
by two genuinely-restated psyche records: **vez8** (Decision, Maximum) for
the pipeline shape and **xai7** (Principle, VeryHigh) for the structural
macro node. These two are the current ground truth and they SUPERSEDE the
large body of older asschema/macro-grammar records.

**The pipeline (vez8).** A schema file is *full NOTA* — schema is a
specialized NOTA dialect built on structural macro nodes, NOT a separate
language that lowers into NOTA. The canonical flow is:

1. **Authored schema (NOTA)** DESERIALIZES — via the structural macro node
   codec — directly into
2. **schema-in-rust**: typed Rust that fully defines the schema,
   rkyv-serializable, a faithful CANONICAL-round-trip image (not
   byte-identical source preservation, per fz9n);
3. schema-in-rust then **LOWERS** into Rust interface code (the emitter does
   Rust *projection*, not schema semantics).

The load-bearing change versus all prior design: **ASSEMBLED SCHEMA
(Asschema) is REMOVED.** There is no separate assemble step and no public
SchemaResolution IR (fz9n reinforces "avoid a public SchemaResolution IR").
The resolution work Asschema used to perform — inline-declaration hoisting,
visibility, ordering, symbol paths — now lives as **methods on
schema-in-rust types**, invoked during the lower step. Schema deserializes
directly into the typed form; it is not separately assembled. vez8
consolidates prior records lcwu (conditional) + pv61 (decided) + fkbz (the
pipeline), restated with rising conviction; certainty was raised to Maximum
to mark that genuine repetition.

**The structural macro node (xai7).** This is the codec primitive the whole
schema dialect rests on. A structural macro node is **a NOTA enum decoded by
SHAPE, not by a data tag**. The enum TYPE is the whole specification: decode
is TYPE-DIRECTED — the codec performs a structural match on each variant in
**declaration order, first structural match wins**, then decodes that
variant's data, RECURSIVELY (a variant may itself hold further structural
macro nodes). Encode emits a NOTA block matching the chosen variant shape —
the codec is BIDIRECTIONAL. It is explicitly NOT a runtime registry, NOT a
capture-map, NOT string variant-name dispatch. It is realized as a derive,
`#[derive(StructuralMacroNode)]`, on the enum with per-variant shape
attributes. The psyche frames this as "the part of NOTA original design that
was never implemented." xai7 consolidates prior records ejvc + i0e6 and is
refined/restated by **z544** (Clarification, High): the macro-node
definition is known before reading the value; the node is an enum type;
decoding tries each variant's structural match in declaration order; this is
"not a separate NOTA parser or global registry."

**Net effect on older grammar debate.** A long arc of records wrestled with
the enum-vs-macro disambiguation (mha3, fo38, b0s4, dxmu, hh9p, nryo, 1fgo),
the at-sigil and star-suffix grammar (degt, 6gb0, jony, c3tb, fhaj), the
everything-is-a-struct / macros-as-data foundation (umsv, dwtm, bkzd, hc0t,
4itr), and the assembled-schema-first sequencing (av1q, cupj, 2in8, duse,
l95b, qods). **vez8 and xai7 collapse most of that:** the
enum-vs-macro-and-sigil ambiguity is dissolved because decode is
type-directed (the expected enum type at each position drives the structural
match), and the "define assembled schema first" sequencing is moot now that
assembled schema is removed. These older records remain valuable as the
rationale trail but are no longer the live design surface. Note umsv's
"EVERYTHING is a struct / positional typing dissolves the ambiguity / no
sigil needed" foreshadows xai7's type-directed decode — the two are
consonant; xai7 is the codec-level realization.

**Engine consolidation (mxo5, 58bv).** Schema-next must have exactly ONE
lowering engine. The dual-path divergence (typed-source path vs registry
lower-source path) is eliminated by keeping the single MOST-CORRECT lowering,
not the smallest. The retained engine should make **schema its own codec** —
the shorthand source form round-trips through the schema codec (xsp1, ji0f).
Note mxo5 carries certainty Zero (probing/uncertain), but 58bv restates the
one-engine direction at High.

**Emission shape (zhjg, kuw2, fhaj, dtwe, 6th4).** Rust emission moves from
hundreds of hand-indented `format!` lines to a typed token model: RustItem /
RustImplBlock / RustMatch, with the writer owning indentation depth (zhjg
Decision; kuw2 the smaller restatement). Data-before-text extends from type
declarations to impl/trait/match output. Generated Rust emits into a
dedicated schema module tree inside the crate (dtwe). Bare namespace bindings
lower to a `TypeDeclaration::Alias` (`pub type Rejected = SignalRejection;`)
rather than tuple newtypes (fhaj). Every root enum auto-gets a `Help` action
variant generated from the schema description, recursively (6th4) — self-
description becomes part of the typed interface contract. The direction is
to push MORE runtime behavior into the macro-generated interface (epn9): the
macro generates default trait wrappers, hooks, tracing (q13r — tracing built
into schema-generated engine traits with default impls, not side traits),
and eventually behavior targets, so hand-written Rust fills only domain
decisions over schema-emitted nouns (u1nr).

**Codec opt-in (bkcd, hu8i).** rkyv is the universal wire base for the whole
schema-derived stack; the NOTA codec (NotaDecode/NotaEncode + derive) is
OPT-IN per consumer. Double clients (text+binary, e.g. the CLI) need the NOTA
derive; binary-only consumers (the daemon) must NOT compile NOTA impls in —
for leanness and structural contract clarity. Schema and schema-emitted Rust
sit on the SAME NOTA typed interfaces direct Rust code uses (hu8i, Maximum) —
no parallel mini-codec per generated schema.

**The driving conviction (u8od, js59, p6jx, 15n7, rnrg).** Schema is the
*growing focus* of the workspace; the psyche wants to understand it from
every angle, and both operator and designer must keep producing concrete
"this-code-creates-this-code" reports showing schema input, emitted output,
and the runtime/trade each shape creates (u8od High; js59, p6jx, 15n7).
rnrg (Maximum) gives the deepest rationale: NOTA is "a hack on the text user
interface" — a typed language where everything reads as a known type;
structural macro nodes extend the type-declaration vocabulary but the
extension is itself typed, so every node resolves to a known type, and a
well-formed NOTA expression decodes reliably. This is the why behind
NOTA-everywhere.

## 2. Load-bearing records (short code + bracket-quoted summary)

**Top anchors (current ground truth):**

- **vez8** (Decision, Maximum, 2026-06-04/05) — [Schema is a specialized
  NOTA dialect built on structural macro nodes ... authored schema (NOTA)
  DESERIALIZES, via the structural macro node codec, into schema-in-rust ...
  schema-in-rust then LOWERS into rust interface code. There is NO separate
  assemble/Asschema step ... ASSEMBLED SCHEMA (Asschema) is REMOVED. The
  resolution Asschema performed ... lives as methods on schema-in-rust
  types, used during the lower step; the emitter does Rust projection, not
  schema semantics. Consolidates lcwu + pv61 + fkbz ... certainty raised to
  Maximum.]

- **xai7** (Principle, VeryHigh, 2026-06-04/05) — [The structural macro
  node — a NOTA enum decoded by SHAPE, not by a data tag ... decode is
  TYPE-DIRECTED — the codec performs a structural match on each variant in
  DECLARATION ORDER, first structural match wins ... RECURSIVELY ... encode
  emits a NOTA block matching the chosen variant shape (BIDIRECTIONAL) ...
  realized as a derive (#[derive(StructuralMacroNode)]) ... the part of NOTA
  original design that was never implemented. Consolidates ejvc + i0e6.]

**Direct refinements / supports of the anchors:**

- **z544** (Clarification, High) — [NOTA structural macro nodes are typed
  codec behavior: the macro-node definition is known before reading the
  value, the macro node is an enum type, and decoding that enum tries each
  variant's structural match in declaration order; this is not a separate
  NOTA parser or global registry.]
- **fz9n** (Decision, High) — [schema pipeline report 524 + operator
  feedback 316 accepted ... implement schema-in-Rust as the rkyv-
  serializable typed schema value, use canonical round-trip rather than
  byte-identical source preservation, avoid a public SchemaResolution IR,
  and have Rust emission lower from high-level schema datatype methods.]
- **mxo5** (Decision, Zero) — [Schema-next must have exactly one lowering
  engine ... keep the single most-correct lowering, not the smallest ... The
  retained engine should make schema its own codec.]
- **58bv** (Decision, High) — [Schema-next should have one lowering engine;
  keep the most correct lowering path rather than ... the smallest patch.]
- **xsp1** (Decision, High) — [Schema should be able to act as its own codec
  for its shorthand authored form, so shorthand schema syntax round-trips as
  typed schema data rather than being only a one-way parser convenience.]
- **hu8i** (Principle, Maximum) — [Schema and schema-emitted Rust should sit
  on top of the same NOTA typed interfaces that direct Rust code uses.
  Reusing NOTA decode encode traits is better engineering than emitting a
  parallel mini-codec for each generated schema.]
- **bkcd** (Decision, High) — [rkyv is the universal wire base ... NOTA codec
  is OPT-IN per consumer ... DOUBLE clients (text + binary, e.g. the CLI)
  need the NOTA derive; binary-only clients (the daemon ...) must NOT have
  NotaDecode/NotaEncode impls compiled in ... Same data types across
  consumers — what differs is the derive set, not the wire shape.]

**Emission / interface generation:**

- **zhjg** (Decision, Zero) — [Ratified: a RustItem, RustImplBlock, and
  RustMatch token model for schema-rust-next emission. The writer renders the
  typed item model once and owns indentation depth ... data-before-text ...
  extends from type declarations to the impl, trait, and match output.]
- **kuw2** (Decision, Medium) — [Ratify a small Rust item, Rust impl block,
  and Rust match token model for schema-rust-next emission, with the writer
  owning indentation depth.]
- **dtwe** (Decision, High) — [Schema-generated Rust should emit into a
  dedicated schema module tree inside the crate source.]
- **fhaj** (Decision, High) — [bare namespace bindings such as Rejected
  SignalRejection should lower to schema_next::TypeDeclaration::Alias ...
  emitting pub type Rejected = SignalRejection; rather than tuple newtypes.]
- **6th4** (Decision, High) — [Every root enum emitted by schema-rust-next
  gets a Help action variant generated automatically ... the pattern is
  recursive ... Self-description becomes part of every component's typed
  interface contract.]
- **epn9** (Clarification, High) — [moving more runtime behavior logic into
  the schema/macro-generated interface itself: macros define the interface
  and can also generate default trait wrappers, hooks, and eventually
  behavior targets.]
- **q13r** (Correction, High) — [Tracing should be built into the
  schema-generated engine traits themselves, with default ... trait
  implementations, rather than carried as separate ... side traits.]
- **u1nr** (Constraint, High) — [Each plane defined in schema ... emitted as
  Rust datatypes and basic trait implementations ... Hand-written Rust then
  becomes the decision-making actor system over schema-emitted nouns.]

**Schema-source / grammar trail (now mostly subsumed by vez8/xai7, kept for
rationale):**

- **umsv** (Decision, High) — [EVERYTHING is a struct ... A SCHEMA NODE is a
  tagged variant ... read against the KNOWN type expected at its position ...
  the enum-versus-macro ambiguity dissolves through positional typing, not a
  sigil.]
- **4itr** (Constraint, Maximum) — [EVERYTHING is a serializable data object,
  the MACRO most of all ... A macro is NOT parsing code ... it is a DATA
  OBJECT with a name, position, pattern, and template ... The current engine
  VIOLATES this: its macro expansion builds a string from the template and
  re-parses it.]
- **hc0t** (Constraint, High) — [the assembled schema — the .asschema — is
  canonical NOTA ONLY ... The hand-rolled human-readable line format ... is
  FORBIDDEN.] (Note: scoped to assembled-schema, which vez8 has since
  removed; the underlying everything-is-data force survives.)
- **dwtm**, **bkzd**, **n2z3**, **degt**, **6gb0**, **jony**, **c3tb** —
  the pipe-delimiter / at-sigil / star-suffix grammar arc; superseded as the
  live surface by type-directed decode but documents how the team arrived
  there.
- **mxo5/xsp1/ji0f** already listed above for codec self-hosting.

**Driving-conviction / reporting discipline:**

- **u8od** (Principle, High) — [Schema is the growing focus of the
  workspace; the psyche wants to deeply understand schema from every angle
  ... in the this-code-creates-this-code form, with the implementation —
  repeatedly.]
- **rnrg** (Clarification, Maximum) — [NOTA is at heart a hack on the text
  user interface ... a typed language; everything is read as a known type ...
  Structure macro nodes can have structurally different shapes ... because
  they extend the type-declaration vocabulary, but the macro extension is
  itself typed.]
- **js59 / p6jx / 15n7** (High/Maximum) — reports must foreground schema
  input → generated output → runtime trade.

## 3. Records touching Spirit-record-redesign topics (for cross-link)

These are the live intent on the OTHER design topic (our Spirit-record
redesign) that the situate step should cross-link. The single sharpest tie
is m27p, which sits at the intersection of NOTA optionality and record
privacy.

**Record shape / fields-vary-by-kind:**

- **20jk** (Decision, High) — [Spirit record fields should vary by record
  kind rather than every record carrying every field — eliminate the fields a
  given kind does not use ... a private-bearing record carries a privacy
  field while an ordinary public record omits it ... A better architecture
  than the current one-shape-fits-all positional record.]
- **f0wm** (Principle, High) — [Spirit intent records should be shaped as
  specific variants whose fields match their semantic needs; private record
  variants carry privacy data, while public record variants should not carry
  unused privacy fields.]

**Privacy as NOTA Optional (the NOTA crossover record):**

- **m27p** (Decision, High) — [Spirit record privacy is an Optional field:
  in NOTA a public records privacy is None and an elevated-privacy records is
  (Some Magnitude). Privacy is available to any kind, not tied to specific
  kinds ... optionality is the None token, never an absent or omitted
  positional field, because every NOTA positional record carries every
  field.] NOTE the apparent tension with 20jk/f0wm below.

**Relations / agglomeration / provenance:**

- **a3l4** (Decision, High) — [Spirit records gain a relations field — a
  vector of short record-identifier hashes sized just long enough for
  non-collision, pointing to other records ... a Correction relates to the
  record it corrects ... The relations field is the only code change needed
  to support intent relation and agglomeration.]
- **y0vr** (Correction, High) — [There is no composite intent type in code —
  composite and agglomeration are a language and behavior concept ... not a
  record type or variant ... provenance and agglomeration are expressed
  through a relations field on records, not a dedicated Composite type.]
- **cw5t** (Principle, High) — [Spirit should support composite intent
  records that reference older intent records as source material ... without
  losing provenance.]

**Weight vs certainty (second magnitude axis):**

- **g8ln** (Clarification, Medium) — [Spirit weight uses the same Magnitude
  ladder (Zero through Maximum) on a second axis distinct from certainty, not
  an integer count, keeping the contract all-qualitative.]
- **vbx6** (Principle, High) — [Spirit records should distinguish certainty
  from weight: certainty is confidence in the statement, while weight is
  accumulated importance or reinforcement.]
- **9bxr** (Clarification, High) — [weight measures how much a topic keeps
  recurring ... high weight can pair with low certainty during probing, and
  low weight can pair with high certainty.]

**Privacy operations / query gate (already deployed in v0.5.0):**

- **h7sz** (Decision, Medium) — [Spirit should gain a ChangePrivacy
  operation mirroring ChangeCertainty.]
- **a32n** (Decision, High) — [The normal Spirit query returns only
  Zero-privacy most-public records by default ... an explicit privacy-query
  subtype that carries a privacy level.]
- **7vre** (Decision, High) — [expose all privacy selectors as operations —
  at most inclusive, exact equal, and at least.]
- **twlp** (Decision, High) — [When a record moves into the archive its
  privacy variable moves with it.]
- **h0bj** (Principle, Medium) — privacy classification ladder
  (infrastructure stays Zero; personal gets elevated).

**Hash identity:** no record matched a `[hash-identity]` partial tag. The
identity material lives implicitly inside a3l4 ("short record-identifier
hashes sized just long enough for non-collision") and tyk3 below.

- **tyk3** (Decision, Zero) — [Psyche wants to try the structured SymbolPath
  form — a record of component, plane, variant, payload, field — as the fully
  qualified symbol identity, rather than the landed flat vector of names.]
  (Schema symbol identity, adjacent to record-identity hashing in spirit.)

## 4. Contradictions, tensions, and rising-conviction restatements

**Rising conviction (genuine repetition, certainty raised):**

- vez8 raised to **Maximum** explicitly because the psyche genuinely
  re-stated the no-Asschema pipeline (consolidating lcwu+pv61+fkbz). xai7 at
  **VeryHigh** consolidating ejvc+i0e6. Both carry the explicit "genuinely
  restated by the psyche" marker — these are the strongest current signals.
- The "one lowering engine" direction restated: mxo5 (Zero, probing) →
  58bv (High). The codec self-hosting restated across xsp1, ji0f, mxo5.

**Live tension to flag for the situate step (Spirit record-shape):**

- **m27p vs 20jk/f0wm.** m27p (High) says privacy is an Optional field that
  EVERY record carries (None for public, Some Magnitude for elevated),
  because "every NOTA positional record carries every field." 20jk (High)
  and f0wm (High) say fields should VARY by kind — public records should NOT
  carry an unused privacy field at all. These pull in opposite directions:
  uniform-optional-field vs per-kind-variant-shape. Both are High certainty
  and both name "better architecture." This is the central unresolved design
  question for the Spirit-record redesign and should be surfaced to the
  psyche, not silently resolved. (m27p's framing implicitly assumes a single
  positional record shape; 20jk/f0wm assume per-kind variants — they may be
  reconcilable if "kind" itself becomes the discriminant of which fields
  exist, with privacy-as-Optional only on the kinds that can be private.)

**Superseded, not contradicted (the schema arc):**

- The entire assembled-schema / Asschema body (av1q, cupj, 2in8, duse, l95b,
  qods, mnl1, 0zci, 9ptu, 85o4, hc0t, h053, fv2a, yuku, bpg9, k1p7, 8ryy,
  75ea, 7wst, x020, hhaf, hnog) is **superseded by vez8's removal of
  assembled schema.** Not a contradiction — a clean supersession with rising
  conviction. These records describe a stage that no longer exists; they
  should be read as historical rationale only. mnl1/0zci already pre-marked
  the OLD vector-record asschema syntax obsolete; vez8 removes the whole
  layer.
- The sigil-grammar / enum-vs-macro disambiguation arc (mha3, fo38, b0s4,
  dxmu, hh9p, nryo, degt, 6gb0, jony, c3tb, 1fgo) is **dissolved by
  type-directed decode (xai7) + positional typing (umsv).** The "explicit
  discriminator required" conclusion (b0s4) is no longer load-bearing once
  the expected type at each position drives the structural match. Kept for
  rationale.

**Capture-hygiene note:** oqn6 (Correction, High) flags that an earlier
schema-language record (1088) was over-captured by the operator (a working
order mistaken for durable intent) — relevant if the situate step walks the
numeric-id trail; durable schema-language intent lives in the grammar/pipeline
records, not the task directive.

**No record supersedes vez8 or xai7.** The 2026-06-04-onward sweep (Since
2026-06-04 00:00:00) returns vez8 and xai7 as the newest substantive anchors
with nothing above them; they are the intent ground truth for the improved
NOTA/schema mechanism.
