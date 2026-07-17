# Up-close design v1 — the shared-codec family and the logos→Rust lowering, reconciled with Codex, at code level

The psyche accepted two design slates and asked to see them **up close** before
implementation: "Yes, and I want to see the design of all that up close first"
(shared-library slate) and "that all sounds right. Id like to see the design up
clos" (logos→Rust lowering slate). This report is the code-level rendering: real
Rust type definitions and trait surfaces at sketch-but-plausible level, the
worked example with real data, and the reconciliation of a Codex-authored
recrystallized-pipeline design forwarded by the psyche.

Written 2026-07-15, session `nextgen-recrystallization`, lane `up-close-design`,
generalist, Opus 4.8 (1M). Read-only on all code repositories; this one file is
the lane's only artifact. The psyche does not read reports — the chat return is
his surface; this file is the agent pickup point.

Provenance: **[ruling]** = settled psyche decision (brief or `design-v0.md`);
**[psyche verbatim]** = his exact words this session; **[observed — cite]** =
code fact from a sibling report's citation or this session's reconnaissance;
**[interpretation]** = my reading; **[AGENT PROPOSAL]** = needs his word, all
collected in §9; **[changed from X]** = an explicit deviation from an accepted
report or the Codex design.

## 0. Supersedence map

This report **consolidates and supersedes specific sections** of the two accepted
slate reports where they are now rendered at code level or reshaped by the newest
rulings. It does **not** edit those files; it supersedes by reference.

**Amendment status (latest first):** §4.6 folds the **Codex kernel hardening,
accepted on recommendation trust** (`ConstructorCodec`, `SequenceForm` algebra,
narrowed kernel + authoring vocabulary, table-identity payload with the hash stored
outside it, scoped Core-type ids, transactional interning, PipeText-as-carrier, and
the conformance laws). Forks A/B/C are all **settled** (§9): `StructuralForm` +
`macro`-for-Nomos; `True*`→`Textual*` confirmed; the evaluator **ships in the
runtime**. Earlier §4.1/§8.4 lines that the amendment reverses are marked
`superseded-by-§4.6` in place rather than deleted, so the history stays spot-checkable.

```
[ (shared-codec-library-v1.md
    supersedes §2.2-2.5  (crate type surfaces now concrete here §2-§5)
    supersedes §2.5-decision-8  (entry-location fork RESOLVED to external sidecar §4.3, §8)
    supersedes §5-decision-7  (nota-derive: entries-only → entries+codecs+conformance §4.5)
    keeps       §1  (the repetition survey — evidence, unchanged)
    keeps       §5-decisions-1..6,9  (crate count, split, names, repos, blake3 — unchanged))
  (logos-rust-lowering-v1.md
    supersedes §1-§2  (CoreItem/ProjectRust now inside the Textual family §6)
    supersedes §6  (RustShape now NAMED TextualRust, a form in the many-forms family §6)
    supersedes §7-decision-A,G  (ProjectRust/RustShape reconciled into the shared evaluator §6.3)
    keeps       §3  (transcription discipline / five synthesized things — unchanged)
    keeps       §4  (the worked example — reused verbatim as the golden oracle §7)
    keeps       §5  (evolution / Phase-D kernel — unchanged))
  (core-first-architecture-v1.md
    keeps       §2.6  (Phase A-D — reconciled with Codex into one order §8))
  (nomos-macro-model-v1.md  keeps all  (input `{ Name Type }`, capitalized macros, named/structural))
  (Codex recrystallized-pipeline design  folded throughout; every fold marked [changed from Codex]) ]
```

## 1. The one-paragraph thesis of the reconciliation

Three settled shapes now fit into one picture. **(a)** Four layered crates carry
the shared machinery, dependencies strictly downward, so stringless Core never
depends on text (`content-identity ← name-table ← raw-discovery ← structural-codec`).
**(b)** The psyche's two newest rulings turn the "structural-expectation table"
into the **Textual view layer itself**: the parser-side structural data *is* an
extension of the renamed `Textual*` view (ruling 1), and each Core is viewed
through a **family** of per-form Textual data-trees — `TextualLogos` and
`TextualRust` both over `CoreLogos`, each a bidirectional codec (ruling 2). **(c)**
Codex's recrystallized pipeline — versioned raw profile → structural tree →
expected-type lookup → typed import → Nomos — is the *mechanism* of that Textual
layer, and its strongest new substance (declarative structural programs +
one trusted evaluator + generated optimized codecs + conformance tests proving
them equal) makes parser behavior itself content-addressed Core-like data — the
psyche's library instinct, extended one level up. The single reconciliation move
that dissolves the remaining open questions: the structural form is an **external
sidecar**, keyed by stable `CoreTypeId`, carrying its own content identity
**excluded from the Core hash** — derived, not chosen, from the settled ruling
that text evolution must never move Core identity.

## 2. Crate 1 — `content-identity` (leaf: portable archive + content hash)

Depends only on `rkyv` + `blake3`. No strings, no text. Collapses §1.7 (34+ rkyv
restatements), §1.8 (5 duplicate digest newtypes, 3 blake3 conventions) of the
library report. Absorbs Codex's "envelopes" here [changed from Codex: Codex's
"language-core" owns hashes+envelopes+NameTables together; the four-crate split
keeps hashing below names because **hashing must not depend on names** — §5].

```rust
//! Portable content identity for stringless Core values.

/// The one portable-archive discipline, lifted verbatim from sema-engine's
/// EngineStoredValue/EngineStoredRecord bound (record.rs:153-198). A type that
/// is `PortableArchive` round-trips through rkyv with validation-on-read, in the
/// fixed little-endian / 32-bit-pointer / unaligned layout, with no
/// engine-specific type in the bound. Blanket-impl'd so callers never restate it.
pub trait PortableArchive:
    rkyv::Archive
    + for<'a> rkyv::Serialize<HighSerializer<'a>>
    + Sized
where
    Self::Archived: rkyv::Deserialize<Self, LowDeserializer> + for<'a> CheckBytes<Validator<'a>>,
{
    fn to_archive_bytes(&self) -> Result<AlignedVec, ArchiveError>;
    fn from_archive_bytes(bytes: &[u8]) -> Result<Self, ArchiveError>;
}

/// One generic 32-byte content hash, parameterized by a typed domain. Collapses
/// sema-engine's five identical [u8;32] newtypes (EntryDigest, SegmentDigest,
/// CheckpointDigest, SchemaHash, StoreSchemaHash) and schema's ContentHash into
/// one type. The domain carries the layout-version tag, so "which layout" lives
/// in the type, never in a hand-remembered `&'static [u8]` suffix.
pub struct ContentHash<Domain: HashDomain> {
    bytes: [u8; 32],
    domain: PhantomData<Domain>,
}

impl<Domain: HashDomain> ContentHash<Domain> {
    /// blake3 over the given canonical bytes, domain-separated via
    /// `new_derive_key(Domain::context())` and folded with a length-prefix
    /// (sema-engine's `update_bytes`, versioning.rs:299-302) so concatenations
    /// cannot collide.
    pub fn derive(bytes: &[u8]) -> Self { … }

    /// Ruling 3: hash a stringless Core value over its canonical rkyv bytes.
    /// The NameTable is NOT in the pre-image (it is not in the Core value), so a
    /// rename is hash-stable by construction.
    pub fn of_core<Value: PortableArchive>(value: &Value) -> Result<Self, ArchiveError> { … }
    // NOTE (reconnaissance): this NameTable-excluded pre-image is a NEW derivation.
    // sema-engine's EXISTING digests deliberately INCLUDE names (store name, family
    // name, table name, decimal key string; versioning.rs `EntryDigest::from_entry_fields`,
    // `VersionedLogOperation::update_digest`); only `StoreSchemaHash` excludes table
    // names. So `of_core` is added alongside, and sema-engine's on-disk digest bytes do
    // not move (§8 decision 6) — the existing domain strings become HashDomain variants.

    pub fn bytes(&self) -> &[u8; 32] { &self.bytes }
}
// hex Display, Eq/Ord, rkyv derive elided.

/// A typed, closed, layout-versioned hash domain. A trait (not one enum) so each
/// crate owns its own closed domain set while sharing the primitive: sema-engine
/// keeps its EXACT existing domain strings as variants (byte-stable on-disk
/// digests, §5 decision 6), and each Core crate defines fresh layout-tagged
/// domains without content-identity knowing about them.
pub trait HashDomain {
    fn context(&self) -> &'static str;      // the blake3 derive-key context
    fn layout_version(&self) -> LayoutVersion;
}

pub struct LayoutVersion(pub u16);

/// Codex's "envelope" absorbed here: a content-addressed wrapper of stored bytes,
/// carrying the layout version and the hash of its payload. signal-frame reuses
/// this for the shared bound; sema-engine's stored records are envelopes.
pub struct Envelope<Domain: HashDomain> {
    pub layout: LayoutVersion,
    pub identity: ContentHash<Domain>,
    pub payload: AlignedVec,
}
```

Lead name **`content-identity`**; alternates `archive-identity`, `portable-digest`.
Full-English compliant.

## 3. Crate 2 — `name-table` (stringless-Core Identifier space)

Depends on `content-identity`. Holds names as data; no text codec. Collapses §1.4
(the derived-name walker written twice) and §1.9 (123 `: Name` string sites) of
the library report.

```rust
//! The stringless-Core identifier space and its name interning.

/// The index every Core type carries in place of a string. Owns only its
/// representation; the table is the noun that carries meaning.
pub struct Identifier(u32);

/// Interned, append-only Identifier → Name. The `extend_from` method builds the
/// CONTINUOUS schema→logos space (ruling 2): the logos table is a higher-index
/// append-extension of the schema table, so a carried-over schema identifier
/// keeps its exact index.
pub struct NameTable { … }

impl NameTable {
    pub fn intern(&mut self, name: &str) -> Identifier;
    pub fn resolve(&self, id: Identifier) -> &Name;
    pub fn extend_from(&self, base: &NameTable) -> NameTable;
    pub fn identity(&self) -> ContentHash<NameTableDomain>;   // co-versioned stored sibling
}

/// A name, and the single home of the derived-name rule (the loop hand-written
/// twice today: schema `Name::field_name`, schema-rust `ScreamingName::screaming`).
pub struct Name(String);

impl Name {
    pub fn field_name(&self) -> String;    // PascalCase → snake_case
    pub fn screaming(&self) -> String;     // PascalCase → SCREAMING_SNAKE
    pub fn pascal_case(&self) -> String;
}

/// The two-way name contact point, both impl'd by NameTable. ENCODE resolves an
/// Identifier to text; DECODE interns text to an Identifier (allocating into the
/// continuous space). Threaded down the codec call tree, never held by a node —
/// the exact bidirectional boundary of ruling 6.3 of the lowering report.
pub trait NameResolver { fn resolve(&self, id: Identifier) -> &str; }
pub trait NameInterner { fn intern(&mut self, name: &str) -> Identifier; }
```

[changed from library report §2.3] the report placed a `Named<Core>` **projection
trait** in `name-table`. Under ruling 1 the view now carries text *structure*, so
the projection moves up into `structural-codec` and becomes an **external codec
over Core-as-data** (not a `Self` trait on Core types) — otherwise Core would have
to depend on text to implement it. `name-table` keeps only `NameResolver` /
`NameInterner` (pure name substance, no structure). §6.

Lead name **`name-table`** (the psyche's own word); alternates `identifier-space`,
`stringless-core`.

## 4. Crate 4 — `structural-codec` (the Textual structure vocabulary, evaluator, sidecar registry) — the centerpiece

Depends on `raw-discovery` (§5) + `name-table`. This crate is where the three
settled shapes meet: it is the home of the **Textual structure vocabulary** (ruling
1), the **many-forms family** (ruling 2), and Codex's **declarative-program +
evaluator + generated-codec + conformance** triad.

### 4.1 The structural-program data model IS the Textual structure vocabulary (ruling 1)

**[psyche verbatim]** "all that pertains to the textualization is an extension of
the text-side (true) - maybe true is renamed to Textual, and the Textual* view is
thus extended (by adding the structural aspect in data which maximizes
enums/variants with specialized struct as usual - like DelimitedBlock or Vec's of
ObjectSymbolPrefixedBlock (PascaleCase dot prefixed block), etc."

So the "structural expectation entry" is not a foreign registry format — it is the
**Textual view's own data**, maximized into enums with specialized structs. This
is exactly the structural-program data model Codex describes; the manager's
assessment makes the identity explicit: *the structural-program data model IS the
Textual structure vocabulary; DelimitedBlock, ObjectSymbolPrefixedBlock etc. are
its constructors.* **Terminology settled (his Q2, verbatim):** "Yes, I agree on
the surface" — `StructuralForm` for the parser-side data, `macro` reserved for
Nomos. This section renders the COMPLETE data-tree he asked to see, fully fielded
and grounded line-by-line in the real nota `macros.rs` shapes it lifts.

**The tree is not greenfield; it is the lifted, stringless, Core-keyed
generalization of nota's existing `Pattern`/`PatternElement` (macros.rs:307,525).**
Every type below cites the real shape it lifts and marks what is new. The nota
originals **already derive `nota::NotaEncode`**, so the self-description in §4.1.1
is real, not hypothetical.

```rust
//! The structural-form data model. A form is a SEQUENCE of positional elements
//! (nota Pattern { elements: Vec<PatternElement> }); the recognizer (§5) discovers
//! raw structure, the evaluator (§4.4) interprets a form both directions. A form is
//! DATA — no arbitrary parsing code (Codex: "each entry contains NO parsing code").

// ===== container / keys (AMENDED — Codex kernel hardening, accepted on trust; see §4.6) =====
pub struct CoreUniverseId(u32);      // NEW — the Core universe a type belongs to (fixture universe for the PoC)
pub struct ScopedCoreTypeId { pub universe: CoreUniverseId, pub local: u32 }   // was CoreTypeId(u32)
pub struct CoreConstructorId { pub core_type: ScopedCoreTypeId, pub constructor: u32 }  // per Core CONSTRUCTOR
pub struct StructuralRevision(u32);
pub struct ProfileRevision(u32);

/// The external sidecar (§4.3): keyed by ScopedCoreTypeId, one ConstructorCodec per
/// Core constructor. [changed from my earlier StructuralEntry/StructuralVariant:
/// the unit is the Core CONSTRUCTOR, with an ASYMMETRIC codec — many accepted decode
/// forms, exactly one canonical encode form (§4.6).]
pub struct ExpectationTable {
    pub revision: StructuralRevision,
    pub entries:  BTreeMap<ScopedCoreTypeId, Vec<ConstructorCodec>>,
    // identity is computed over `TableIdentityPayload` and STORED OUTSIDE it (§4.6,
    // fixes the self-reference bug); still EXCLUDED from Core value identity.
    pub identity: ContentHash<StructuralTableDomain>,
}

/// The table-identity pre-image. [changed-from — self-reference bug fix, §4.6.]
pub struct TableIdentityPayload {
    pub universe:        CoreUniverseId,
    pub layout:          CoreLayoutIdentity,          // the Core layout these forms target
    pub raw_profile:     RawProfileIdentity,          // profile identity (glyph set + revision)
    pub lexicon:         Vec<u8>,                     // the committed lexicon — EXACT glyph bytes
    pub leaf_contracts:  Vec<LeafCodecContractId>,    // leaf-codec contract identities
    pub entries:         BTreeMap<ScopedCoreTypeId, Vec<ConstructorCodec>>,
    // NOTE: the resulting ContentHash is stored on ExpectationTable, NOT inside here.
}

/// One Core constructor's codec: several disjoint ACCEPTED decode forms, exactly ONE
/// canonical ENCODE form, and a positional output signature that MUST equal the
/// constructor's Core field signature. (Replaces the symmetric StructuralVariant set;
/// nested alternatives are still reached by Delegate.)
pub struct ConstructorCodec {
    pub constructor:  CoreConstructorId,
    pub decode_forms: Vec<StructuralForm>,           // disjoint accepted inputs; validate_no_silent_conflicts
    pub encode_form:  StructuralForm,                // the single canonical output
    pub signature:    Vec<ScopedCoreTypeId>,         // positional; MUST equal the Core field signature
}

// ===== the form (nota Pattern) =====
pub struct StructuralForm {          // nota `Pattern { elements: Vec<PatternElement> }`
    pub elements: Vec<StructuralElement>,
}

/// AMENDED (§4.6): the KERNEL is narrowed to exactly these seven. `Any` is dropped
/// from the kernel; `ObjectPrefixed`/`Dotted` move to the AUTHORING vocabulary below
/// (they normalize to plain `Application` before hashing and evaluation).
pub enum StructuralElement {
    Product(Vec<StructuralElement>), // NEW — heterogeneous positional tuple (sequence algebra, §4.6)
    Atom(AtomForm),                  // nota Atom(AtomShape)
    Leaf(LeafForm),                  // the leaf/carrier model (§4.6): scalar rejoin OR PipeText carrier
    Literal(Identifier),             // nota Literal(String) → interned keyword
    Application(ApplicationForm),    // right-associative head.payload — the normalized application form
    Delimited(DelimitedBlock),       // a delimiter around a SequenceForm (§4.6)
    Delegate(ScopedCoreTypeId),      // constructs a wrapper; rejects transparent cycles (§4.6)
}

/// AUTHORING vocabulary — his named structs, PRESERVED. These appear in the authoring
/// surface and NORMALIZE to plain `Application` before the form is hashed or evaluated,
/// so the kernel stays small while his vocabulary stays in the surface (his ruling 1).
pub enum AuthoringElement {
    ObjectPrefixed(ObjectSymbolPrefixedBlock),  // `CommitSequence.{ Integer }` → Application(Atom, Delimited)
    Dotted(DottedForm),                         // `rkyv.Archive` → right-assoc Application chain
    Kernel(StructuralElement),                  // anything already in kernel form
}

// ===== element payloads (each grounded) =====

/// A single bare atom, case/sigil constrained; ALWAYS resolves to a NameTable
/// identifier. Lifted from nota `AtomShape { case, sigil, capture }` (macros.rs:623).
/// [changed from my §4.1 sketch: (1) no `leaf` field — a case-constrained atom is a
/// name, scalars live in `Leaf`; (2) `capture` DROPPED — capture binds an atom to a
/// result-template variable, which is a Nomos-MACRO concern, not structural parsing.]
pub struct AtomForm {
    pub case:  Option<CaseExpectation>,   // nota `Option<AtomCase>`; None = any case
    pub sigil: Option<SigilSpec>,         // nota `Option<SigilSpec>`; the `$` escape rides HERE
}
pub enum CaseExpectation { Symbol, PascalCase, CamelCase, KebabCase }   // nota `AtomCase` (macros.rs:703)
pub struct SigilSpec { pub character: String, pub position: SigilPosition }  // nota `SigilSpec` (macros.rs:732)
pub enum SigilPosition { Prefix, Suffix }   // nota `SigilPosition` (macros.rs:777) — NOT Leading/Trailing

/// AMENDED (§4.6) — the leaf/CARRIER model. A leaf either flattens-and-parses a
/// scalar (the rejoin mechanism: an atom flattens to itself; a dotted Application
/// rejoins via `Block::dotted_text`) OR names a CARRIER for content that a bare atom
/// or `()` cannot hold. PipeText did NOT disappear — it is the carrier the branch
/// rework's StringForm classification assigns to delimiter/whitespace-bearing strings.
pub struct LeafForm { pub codec: LeafCodec }
pub enum LeafCodec {
    Scalar(ScalarLeaf),        // flatten-then-parse
    Carrier(CarrierLeaf),      // an explicit carrier for content bare/() cannot hold
    Foreign(ForeignLeafId),    // a Rust custom leaf (§6, TextualRust)
}
pub enum ScalarLeaf {
    Integer,   // flatten → parse integer   (a single atom flattens to itself)
    Float,     // flatten → parse float     (App(-122, 3) → "-122.3")
    Text,      // flatten → the string      (App(a, App(b, c)) → "a.b.c")   — ordinary strings by rejoin
    Boolean,   // a keyword atom
}
/// [changed-from — my prior amendment said "PipeText is gone from the vocabulary."
/// WRONG: the string requirement was rejected, but PipeText survives as a CARRIER for
/// strings that bare/() cannot represent (StringForm classification, §4.6).]
pub enum CarrierLeaf { PipeText }   // the (| |) carrier; extends as other carriers earn a form

/// A delimiter around a SequenceForm (the sequence algebra, §4.6). [changed-from — the
/// `cardinality: Cardinality { Any, Even, Exact }` field is replaced by SequenceForm,
/// which composes Product and Repeat(minimum, maximum, element).]
pub struct DelimitedBlock {
    pub delimiter: Delimiter,
    pub sequence:  SequenceForm,
}
pub enum Delimiter { Parenthesis, SquareBracket, Brace }   // nota `MacroDelimiter` (macros.rs:42)

/// The sequence algebra (§4.6), replacing the flat cardinality enum.
pub enum SequenceForm {
    Product(Vec<StructuralElement>),                 // fixed heterogeneous positional slots
    Repeat { minimum: u64, maximum: Option<u64>, element: Box<StructuralElement> },  // homogeneous
}

/// His named example: a PascalCase object symbol dot-prefixing a block —
/// `CommitSequence.{ Integer }`. Specialized sugar over Application(Atom{PascalCase},
/// Delimited); kept distinct because it is the dominant DECLARATION shape (ruling 1:
/// "maximize enums/variants with specialized structs").
pub struct ObjectSymbolPrefixedBlock { pub object: AtomForm, pub block: DelimitedBlock }

/// Right-associative application head.payload.
pub struct ApplicationForm { pub head: Box<StructuralElement>, pub payload: Box<StructuralElement> }

/// AUTHORING-only: a dotted segment run — the qualified-path shape (`rkyv.Archive`).
/// Normalizes to a right-associative `Application` chain before hashing/evaluation.
pub struct DottedForm { pub segment: Box<StructuralElement>, pub repeat: SequenceForm }
```

**Two `[changed from Codex/report]` removals worth stating plainly.** (1) There is
**no `Escape` variant**: the `$` structural escape is `AtomForm.sigil =
Some(SigilSpec { character: "$", position: Prefix })`, grounded exactly in nota's
`AtomShape.sigil` — the escape is a field of an atom, not a new form. (An escape
carrying a whole-block payload, `$( … )`, would need a sigil on a delimited form;
nota's `SigilSpec` is atom-only today — noted as a `$`-reading extension.) (2)
`ScalarLeaf::Float`/`Text` and `SigilSpec`/`SigilPosition::Prefix` (the `$`) are
dependencies on **non-rejected** readings (floats-from-dotted-text; the `$`
profile) — gated behind profile revisions (§4.2) until the psyche accepts them.

### 4.1.1 Three concrete entry instances, and the entry as its own NOTA value

Real data trees, indented constructor-style. A branch worker is implementing the
string-rejoin on nota next-gen in parallel; this is the vocabulary expression only.

**[shown in the PRE-amendment `StructuralEntry`/`StructuralVariant` shape.** They
map to the amended §4.6 `ConstructorCodec` model directly: a per-type entry → one
`ConstructorCodec` per Core constructor; each variant's `form` → an entry in
`decode_forms` with the canonical one lifted to `encode_form`; the Field two-variant
entry (b) → **two** `ConstructorCodec`s; `cardinality: Any/Exact(1)` →
`Repeat{minimum:0,maximum:None}` / `Product`. The §7.3 worked example is already
rendered in the amended form. These three are left as-is so the shapes the psyche
was shown stay spot-checkable.]**

**(a) The schema Struct-declaration entry** (Codex: "Application(ObjectName,
Brace.Sequence(Field))" — with Sequence folded into the brace's cardinality):

```
StructuralEntry {
  core_type: CoreTypeId(17),                       ;; STRUCT_DECLARATION
  variants: [
    StructuralVariant {
      name: Identifier(→ "struct-declaration"),
      produces: CoreTypeId(17),
      form: StructuralForm { elements: [
        Application(ApplicationForm {
          head:    Atom(AtomForm { case: Some(PascalCase), sigil: None }),   ;; the struct name
          payload: Delimited(DelimitedBlock {
                     delimiter:   Brace,
                     cardinality: Any,                          ;; zero-or-more fields
                     children:    StructuralForm { elements: [
                       Delegate(CoreTypeId(23)),                ;; each field → FIELD_DECLARATION
                     ] } }),
        }),
      ] },
    },
  ],
}
```

**(b) The Field-declaration entry — two structurally disjoint variants** (Codex:
"Field accepts Type or Name.Type"):

```
StructuralEntry {
  core_type: CoreTypeId(23),                       ;; FIELD_DECLARATION
  variants: [
    ;; (1) Type only — the field name is elided and DERIVED from the type
    StructuralVariant {
      name: Identifier(→ "type-only"),  produces: CoreTypeId(23),
      form: StructuralForm { elements: [
        Atom(AtomForm { case: Some(PascalCase), sigil: None }),          ;; the Type
      ] },
    },
    ;; (2) name.Type — an explicit lowercase field name dotting the Type
    StructuralVariant {
      name: Identifier(→ "named"),  produces: CoreTypeId(23),
      form: StructuralForm { elements: [
        Application(ApplicationForm {
          head:    Atom(AtomForm { case: Some(CamelCase),  sigil: None }),  ;; field name (lowercase)
          payload: Atom(AtomForm { case: Some(PascalCase), sigil: None }),  ;; the Type
        }),
      ] },
    },
  ],
}
;; nota `validate_no_silent_conflicts` proves (1) a bare PascalCase atom and (2) a
;; camelCase.PascalCase application are structurally distinct — no silent shadowing.
;; On encode, the Core Field variant (has-explicit-name?) selects (1) or (2); on
;; decode, the expected FIELD_DECLARATION type limits lookup to this variant set.
```

**(c) A string-resolving leaf through newtype depth — the SAME mechanism as float.**
The psyche, verbatim: "since floats can be parsed correctly when expected, so can
strings, or any string wrapping newtype (even if has more than one newtype wrapper
that resolves ultimately into a string inner type)." The wrapper depth is a
`Delegate` chain; the terminal `Leaf(Scalar(Text))` does the rejoin, identically to
`Leaf(Scalar(Float))`:

```
;; VALUE forms (object level). Expected type Documentation = newtype over Summary
;; over a string inner. Each wrapper is a transparent Delegate; the raw block passes
;; through unchanged until the terminal scalar leaf flattens it.
entry(CoreTypeId(31)) = StructuralEntry { core_type: 31,  variants: [ single →
    StructuralForm { elements: [ Delegate(CoreTypeId(32)) ] } ] }          ;; Documentation → Summary
entry(CoreTypeId(32)) = StructuralEntry { core_type: 32,  variants: [ single →
    StructuralForm { elements: [ Delegate(CoreTypeId(33)) ] } ] }          ;; Summary → Text
entry(CoreTypeId(33)) = StructuralEntry { core_type: 33,  variants: [ single →
    StructuralForm { elements: [ Leaf(LeafForm { codec: Scalar(Text) }) ] } ] }   ;; Text = string inner

;; the SAME shape for float — only the ScalarLeaf differs:
entry(CoreTypeId(9))  = StructuralEntry { core_type: 9,   variants: [ single →
    StructuralForm { elements: [ Leaf(LeafForm { codec: Scalar(Float) }) ] } ] }  ;; Float inner

;; DECODE of raw `alpha.beta.gamma` (= Application(alpha, Application(beta, gamma)))
;; under expected Documentation(31):
;;   Delegate(31→32) → Delegate(32→33) → Leaf(Scalar(Text))
;;   → Block::dotted_text() flattens the Application  → "alpha.beta.gamma"  → the string.
;; DECODE of raw `-122.3` (= Application(-122, 3)) under expected Float(9):
;;   Leaf(Scalar(Float)) → Block::dotted_text() flattens  → "-122.3"  → parse f64.
;; One control path; the expected type (via its terminal ScalarLeaf) decides the parse.
;; The raw layer NEVER classified — it only discovered a dotted Application.
```

**The entry as its own NOTA value** (deliverable 3 — the self-description the design
promises: forms are serializable, content-identified data; and these very nota types
already derive `nota::NotaEncode`). Instance (a) serialized:

```
;; StructuralEntry(a) as a NOTA value — storable/content-hashable like any Core value.
StructuralEntry.( 17
  [ StructuralVariant.( struct-declaration 17
      StructuralForm.(
        [ Application.(
            Atom.( PascalCase None )
            Delimited.( Brace Any
              StructuralForm.( [ Delegate.( 23 ) ] ) ) ) ] ) ) ] )
```

Grammar details riding on **non-rejected** readings (marked, per deliverable 3):
`Name.( … )` — a capitalized object dot-prefixing a parenthesized positional record
— is the StructuralMacroNode dotting/dissolution reading; `[ … ]` is the vector
delimiter for the `Vec` fields; `Option::None` renders as the bare keyword atom
`None`; the `CoreTypeId` payloads `17`/`23` render as bare integers — themselves
resolved by `Leaf(Scalar(Integer))`, so the table entry that describes a struct is
read by the very leaf vocabulary it contains (the self-hosting closure Codex names);
and the interned `struct-declaration` shows as its resolved kebab text, though in the
stringless substrate it is an `Identifier(u32)` resolved through the NameTable at the
boundary.

### 4.2 The versioned profile (Codex) lives with the raw layer, revisioned

**[changed from Codex — folded]** Codex splits variation into lexical/structural
**profile** (which glyphs the recognizer sees) vs **typed** structural variation
(what shapes mean under an expected type). That split is adopted whole. The
profile is a `raw-discovery` concept (§5) because it governs raw recognition; the
typed variation is the `StructuralForm` above.

```rust
// in raw-discovery, referenced here (ProfileRevision / StructuralRevision are the
// keys defined in §4.1):
pub struct RawProfile { pub revision: ProfileRevision, pub glyphs: GlyphSet }
pub enum GlyphSet { Standard, NomosExtended }   // Standard: . () [] {} ; Nomos: + $
// [changed: the period-string (| |) is no longer REQUIRED — ordinary strings resolve
// by the Text scalar leaf (§4.1). Whether (| |) survives as an OPTIONAL explicit
// escape for strings bearing delimiters/whitespace is a non-rejected detail; if kept
// it is a glyph-set member, if dropped strings needing escaping ride a different form.]
```

### 4.3 The external sidecar registry, keyed by CoreTypeId — the RESOLVED fork

**[changed from library report §2.5 / decision 8]** The library report left the
entry's home as a fork (Core-resident data vs text-side behavior) and proposed
"data" tentatively. Codex left sidecar-vs-embedded open. Both are **resolved by
derivation**, per the manager's binding assessment: embedding a structural-codec
identity in the Core hash would make text evolution move Core identity — a
contradiction of the settled identity ruling. Therefore the form is an **external
sidecar**, associated by stable `CoreTypeId`, carrying its own content identity
**excluded** from the Core value's hash.

`ExpectationTable`, `CoreTypeId`, and `StructuralEntry` are the types defined in
§4.1 (the container section). The sidecar contract, restated (Codex: "association
is EXTERNAL, keyed by stable Core type identity ... the table has its own content
identity, co-versioned with the language package, EXCLUDED from the Core value's
hash — old table decodes old text, new table emits new text, both reach the same
Core"):

```rust
impl ExpectationTable {
    /// Queried BY expected type, never globally searched; the input never selects
    /// its own type. Returns the type's disjoint-variant entry (§4.1).
    pub fn entry(&self, expected: CoreTypeId) -> Option<&StructuralEntry>;
    pub fn identity(&self) -> ContentHash<StructuralTableDomain>;   // co-versioned; NOT in Core hash
}
```

This satisfies both psyche refinements: "associated with the Core type" (keyed by
its identity) and "Core never depends on text" (the association is stored
externally, in the text-side crate). The reconciled tension of library report §2.5
is gone: the form is neither a method on Core nor a closure Core carries; it is
sidecar data the text-side evaluator reads.

### 4.4 The small trusted evaluator

Codex: "a small trusted evaluator executes [the declarative programs]." It works
over a **generic structural mirror** so it is Core-agnostic; the concrete Core
type is recovered by the generated codec (§4.5), and conformance proves the two
agree.

```rust
/// The evaluator's generic currency: a structural mirror of a decoded value,
/// aligned to the element model of §4.1 (no PipeText/Escaped — both removed there).
pub enum StructuralValue {
    Atom(Identifier),                                          // a resolved name
    Scalar(ScalarValue),                                       // a flattened leaf (Integer/Float/Text/Boolean)
    Delimited(Delimiter, Vec<StructuralValue>),
    Application(Box<StructuralValue>, Box<StructuralValue>),
    Delegated(Box<StructuralValue>),                           // passed through a transparent Delegate
    Chosen { variant: usize, payload: Box<StructuralValue> },  // which disjoint entry-variant matched
    Empty,
}
pub enum ScalarValue { Integer(i64), Float(f64), Text(String), Boolean(bool) }

/// The one interpreter of StructuralForm, both directions. SHIPS IN THE RUNTIME
/// (Fork C settled, §9 / §4.6): dialect tables are genuinely data-loadable at
/// runtime and the evaluator executes them directly; generated codecs (§4.5) remain
/// the fast path; the laws (§4.6) keep the two in agreement. Encode and decode read
/// the SAME form, so round-trip coherence holds by construction.
pub struct StructuralEvaluator<'table> {
    table: &'table ExpectationTable,
    raw: &'table RawLayer,
}

impl StructuralEvaluator<'_> {
    /// text tree + expected type → structural value. The expected type limits the
    /// lookup; the input never selects its own type.
    pub fn decode(&self, expected: CoreTypeId, block: &Block, names: &mut NameTable)
        -> Result<StructuralValue, DecodeError>;

    /// structural value → text tree. The Core variant selects the canonical form.
    pub fn encode(&self, expected: CoreTypeId, value: &StructuralValue, names: &NameTable)
        -> Result<Block, EncodeError>;
}
```

### 4.5 The nota-derive entry-generation contract, and the conformance triad

**[changed from library report §2.5 / decision 7 — reconciled with Codex]** The
library report said nota-derive should generate **entries, not codec bodies**.
Codex says generate **both**: "nota-derive generates optimized typed codecs FROM
the same [declarative] programs; conformance tests prove evaluator and generated
codecs agree." Adopt Codex's richer version — it dissolves the apparent conflict:
the **form is always authoritative** (a dialect can add a form the evaluator runs,
with zero codegen — the extensibility the library report wanted), and the
**generated codec is an optimization** for hot types (the performance the derive
gave), with **conformance as the safety net** proving they can never disagree.

```rust
/// Generated per Core type by nota-derive. Emits the authoritative form AND an
/// optimized concrete codec. `structural_form()` is the single source; both the
/// evaluator (over StructuralValue) and this optimized codec (over Self) read the
/// same shape, and the conformance harness proves they agree.
pub trait StructuralCodec: Sized {
    const CORE_TYPE: CoreTypeId;
    fn structural_form() -> StructuralForm;                                  // authoritative
    fn decode(block: &Block, names: &mut NameTable) -> Result<Self, DecodeError>;  // optimized
    fn encode(&self, names: &NameResolverView) -> Block;                     // optimized
}

/// Also generated: the bridge to the evaluator's generic currency, so interpreter
/// output and codegen output are comparable.
pub trait StructuralMirror: Sized {
    fn to_structural(&self) -> StructuralValue;
    fn from_structural(value: &StructuralValue, names: &mut NameTable) -> Result<Self, DecodeError>;
}
```

### 4.6 Amendment — Codex kernel hardening (ACCEPTED ON RECOMMENDATION TRUST)

The psyche accepted the Codex kernel hardening, verbatim: **"1. trusting the
recommendation without a clear view, but the surface sounds correct."** This is a
**trust-based acceptance**, not a spot-checked one — so every piece it changed is
marked here and in the type comments above, so he can spot-check later. The types in
§4.1/§4.4 already carry the amended shapes inline (`ScopedCoreTypeId`,
`ConstructorCodec`, `SequenceForm`, the narrowed kernel, the leaf/carrier model);
this section states the framing, the laws, and the changed-from ledger in one place.

**What the hardening changed (each a `[changed-from]`):**

```
[ (ConstructorCodec  the codec unit is the Core CONSTRUCTOR, ASYMMETRIC: many disjoint
     accepted decode_forms, exactly ONE canonical encode_form, positional `signature`
     that MUST equal the constructor's Core field signature
     — replaces the symmetric StructuralEntry/StructuralVariant set)
  (sequence-algebra  Product / Repeat(minimum, maximum, element) replaces the flat
     `cardinality: Cardinality { Any, Even, Exact }` field
     — REVERSES my prior amendment's "standalone SequenceForm removed" ledger line, §8.4)
  (kernel-narrowed   StructuralElement kernel = { Product, Atom, Leaf, Literal, Application,
     Delimited(SequenceForm), Delegate }; `Any` dropped from the kernel)
  (authoring-vocab   ObjectSymbolPrefixedBlock and Dotted are PRESERVED as AUTHORING
     vocabulary (his named structs stay in the surface) that NORMALIZES to plain
     Application before hashing and evaluation)
  (table-identity    computed over TableIdentityPayload { CoreUniverseId, CoreLayoutIdentity,
     RawProfileIdentity, committed lexicon = EXACT glyph bytes, leaf-codec contract identities,
     entries keyed by ScopedCoreTypeId } — with the hash STORED OUTSIDE the hashed payload
     — [changed-from: OWN THE SELF-REFERENCE BUG in my §4.1.1 NOTA rendering, where the entry's
     own identity would have sat inside its own pre-image]; still EXCLUDED from Core value identity)
  (scoped-ids        CoreTypeId → ScopedCoreTypeId, scoped to a CoreUniverseId; an explicit
     FIXTURE universe for the PoC while the schema-unit question stays PARKED)
  (transactional-interning  a failed decode alternative leaves NO NameTable allocation effects)
  (delegation-discipline    delegation CONSTRUCTS every wrapper, REJECTS transparent cycles,
     allows recursive references only AFTER consuming structure)
  (pipetext-restored  PipeText did NOT disappear — [changed-from my prior amendment's "PipeText
     is gone"]: it is the CARRIER (LeafCodec::Carrier(PipeText)) for content bare atoms or ()
     cannot hold, per the branch rework's StringForm classification) ]
```

**The laws — the conformance contract** (interpreter and generated codec, §4.5,
must satisfy all; they are the runtime-shipped evaluator's correctness spec):

```
[ (round-trip-core     decode ∘ encode = core)
  (round-trip-canonical encode ∘ decode = canonical(raw))
  (interning-atomicity  a failed decoding leaves the NameTable unchanged)
  (identity-preserving  old-table decode → current-table encode preserves Core identity)
  (interpreter≡codegen  interpreter and generated codec AGREE on: the Core value, the
     NameTable delta, the canonical output, and the typed error) ]
```

**What settling Fork C adds here (§9):** the evaluator SHIPS IN THE RUNTIME — his
verbatim "2. yes, that is great design, and a reason I was going this way." Dialect
tables are data-loadable at runtime; generated codecs stay the fast path; the laws
above keep them in agreement. This is why the ConstructorCodec is data, not codegen-
only: a runtime-loaded table is executed directly by the shipped evaluator.

The conformance test shape (one generic function over every derived type's
fixtures) — this is the "conformance tests prove evaluator and generated codecs
agree; encoding and decoding use the same structural contract":

```rust
fn conformance<T>(fixtures: &[Block])
where T: StructuralCodec + StructuralMirror + PartialEq
{
    let form  = T::structural_form();
    let table = ExpectationTable::single(T::CORE_TYPE, form);
    let eval  = StructuralEvaluator::new(&table, &RawLayer::standard());

    for block in fixtures {
        // codegen path
        let mut names_fast = NameTable::new();
        let typed = T::decode(block, &mut names_fast).expect("codegen decode");

        // interpreter path over the SAME form
        let mut names_ref = NameTable::new();
        let mirror = eval.decode(T::CORE_TYPE, block, &mut names_ref).expect("evaluator decode");

        assert_eq!(typed.to_structural(), mirror);              // interpreter == codegen
        assert_eq!(&typed.encode(&names_fast.as_resolver()), block);  // round-trip byte-exact
    }
}
```

**[interpretation]** This triad is the deep prize of the reconciliation: parser
behavior becomes serializable, inspectable, versionable data (`StructuralForm`),
with a proven-equivalent fast path and a proven round-trip — "parser behavior
itself Core-like, content-addressed data," exactly the psyche's library instinct
raised one level. Whether the interpreter also ships in the *runtime* (not only in
conformance tests), enabling dialects to add forms with no codegen at all, is §9
fork C.

Lead name **`structural-codec`**; alternates `expected-shape`, `text-bridge`.
The many-forms ruling (§6) strengthens a `textual-forms` candidate — noted, folded
into the terminology fork (§9 A) rather than decided here.

## 5. Crate 3 — `raw-discovery` (language-agnostic structure + the versioned profile)

Depends only on `rkyv` (its `Block` is archivable; no Core dependency). Lifted from
nota's parser (library report §1.2). This is the crate a structure-only consumer (a
formatter, a tree-sitter bridge, a linter) links without dragging in Core. It is
also the home of the versioned **raw profile** (Codex).

```rust
//! Raw structural discovery: the recognizer sees glyphs, never meaning. It
//! discovers atoms, delimiter boundaries, right-associative application,
//! sequences, pipe text, and supported escapes — never "declaration", "field",
//! "name", or "type" (Codex: "the recognizer does not know 'declaration' …").

/// [observed] The REAL current nota Block (parser.rs:70) has exactly three
/// variants — application is NOT a variant, it is expressed structurally by a
/// capitalized dotted head glued to its argument group. The lift makes that
/// structural application EXPLICIT as a designed variant, so the raw layer names
/// what nota leaves implicit; the `span` is dropped from the archived form.
pub enum Block {
    Delimited { delimiter: Delimiter, root_objects: Vec<Block> },
    PipeText(PipeText),        // (| |) retained ONLY as an optional explicit string escape;
                               // no longer REQUIRED for ordinary strings (newest ruling) — non-rejected
    Atom(Atom),
    Application { head: Box<Block>, payload: Box<Block> },  // DESIGNED-explicit right-assoc dot binding
}

pub enum Delimiter { Parenthesis, SquareBracket, Brace }    // real nota names (parser.rs:235)
pub struct Atom { text: String /* span dropped in archive */ }
pub struct PipeText { /* text + span */ }

impl Atom {
    // the real nota primitives (parser.rs:517,533,555-585)
    pub fn split_at_first_dot(&self) -> Option<(Atom, Option<Atom>)>;
    pub fn qualifies_as_pascal_case_symbol(&self) -> bool;
    pub fn qualifies_as_camel_case_symbol(&self) -> bool;
    pub fn qualifies_as_kebab_case_symbol(&self) -> bool;
}

/// The capitalization classifier — the real nota `AtomCase` (macros.rs:703),
/// one canonical home routing the derive.rs raw-inline bypass through it.
pub enum AtomCase { Symbol, PascalCase, CamelCase, KebabCase }
impl AtomCase { pub fn of(atom: &Atom) -> Self; }

/// The generic recognizer: receives a versioned profile, produces a Block tree.
/// A new glyph is a new ProfileRevision, never runtime guessing (Codex).
pub struct Recognizer { profile: RawProfile }
impl Recognizer {
    pub fn recognize(&self, source: &str) -> Result<Block, RecognizeError>;
}

pub struct RawProfile { pub revision: ProfileRevision, pub glyphs: GlyphSet }
pub enum GlyphSet { Standard, NomosExtended }
pub struct ProfileRevision(u32);

/// The raw-layer abstraction the Textual forms sit on (§6): NOTA-family forms
/// share the Recognizer; foreign-language forms (Rust) supply their own.
pub enum RawLayer {
    Recognizer(Recognizer),   // NOTA family: schema, nomos, logos text
    Foreign(ForeignRawLayer), // Rust: syn parse + prettyplease unparse (§6)
}
```

Lead name **`raw-discovery`**; alternates `positional-structure`, `delimiter-discovery`.

## 6. The Textual many-forms family (ruling 2) — TextualLogos, TextualRust, and beyond

> **Reseated (2026-07-17):** the settled pair is **TextualForm / EncodedForm**
> (`EncodedForm` names the Core-side *view*, not the `Core*` types; `.25`, `.37`).
> `textual-form-vision-design-v1.md` is now the authority for this abstraction and
> the two organs (nametree, structuretree); it supersedes §6.1 (the trait) and §6.2
> (the TextualRust foreign-raw bypass, now reconciled as trees-over-a-raw-layer).

**[psyche verbatim]** "actually, we extend the textual to have many forms, so
corelogos has both the logos and rust textual form data-trees. rust would have more
custom implementations but we would find the logicalization which can also apply to
a language like rust. this even opens us emitting other languages than rust from
logos."

So `Textual` is a **family** of per-form data-trees over one **EncodedForm**
(`CoreLogos` here). `CoreLogos` is
viewed through **both** a `TextualLogos` form tree **and** a `TextualRust` form
tree, each with its own bidirectional codec, sharing the logicalization vocabulary
(the `StructuralForm` constructors of §4.1). Rust supplies more custom leaves. A
third emission language is a third `TextualForm`.

### 6.1 The form as a codec over one EncodedForm, with a principled raw-layer boundary

```rust
/// One textual rendering of a Core family: a raw layer + the expectation table
/// (Core type → structural form) + leaf codecs. NOTA-family forms share the
/// Recognizer; the Rust form supplies `syn` + prettyplease as its raw layer and
/// custom leaves — the principled boundary the reconciliation draws.
pub trait TextualForm {
    type Core;
    fn raw_layer(&self) -> &RawLayer;
    fn expectation_table(&self) -> &ExpectationTable;

    fn decode(&self, text: &str, names: &mut NameTable) -> Result<Self::Core, DecodeError>;
    fn encode(&self, core: &Self::Core, names: &NameResolverView) -> String;
}

pub struct TextualSchema { raw: RawLayer, table: ExpectationTable }   // Recognizer(Standard) over CoreSchema
pub struct TextualNomos  { raw: RawLayer, table: ExpectationTable }   // Recognizer(NomosExtended, has $) over CoreNomos
pub struct TextualLogos  { raw: RawLayer, table: ExpectationTable }   // Recognizer(Standard) over CoreLogos
pub struct TextualRust   { reader: SynReader, writer: PrettyPlaceWriter, table: ExpectationTable } // syn over CoreLogos
```

`TextualSchema`/`TextualNomos`/`TextualLogos` share the Recognizer and the shared
`StructuralForm` vocabulary; they differ only in **which forms their tables hold**
(schema's generative-delimiter declarations, Nomos's structural macros, logos's
reader-serving delimiters — Codex's "dialects differ richly sharing one parser
engine"). `TextualNomos` uses the `NomosExtended` profile (the `$` escape).

### 6.2 TextualRust — the lowering report's `RustShape`, now named

**[changed from lowering report §6]** The lowering report's unnamed `RustShape`
(the two-way per-node structural descriptor) **is** the TextualRust form. Its
entries are `StructuralForm`s whose leaves are largely `LeafCodec::Foreign` (Rust
custom): its raw layer is not the Recognizer but `syn` on decode and prettyplease
on encode — the profile mechanism's principled boundary (manager's binding:
"NOTA-family forms share the recognizer; foreign-language forms get custom leaf
codecs under the same form-tree discipline").

```rust
/// TextualRust's raw layer: never re-implements Rust's grammar. Decode leans on
/// `syn`; encode routes one prettyplease pass per item with `#[rustfmt::skip]`
/// prepended — prettyplease is the SOLE formatting authority (lowering report §3.1).
pub struct SynReader;      // &str → syn AST → CoreLogos (interning names)
pub struct PrettyPlaceWriter;  // CoreLogos → proc_macro2::TokenStream → prettyplease::unparse

/// The five — and only five — things TextualRust synthesizes (lowering report §3):
/// dotted→::, delimiter re-sugaring, stored-identifier realization, one prettyplease
/// pass, the `// @generated` header. Everything semantic is transcribed, not computed.
```

The lowering report's one-way `ProjectRust` trait and its two-way `RustShape` codec
**collapse into TextualRust's encode/decode** run by the shared evaluator plus Rust
custom leaves. `ProjectRust::project` becomes `TextualRust::encode`'s per-node work;
the `NameResolver` contact point is `name-table`'s `NameResolver`/`NameInterner`,
bidirectional at exactly the two leaves (`Identifier`, `PathNode`) — encode
resolves, decode interns (lowering report §6.3). The CoreLogos types are unchanged:

```rust
//! CoreLogos — the closed data algebra 1-to-1 with Rust, stringless (lowering §1).
pub enum CoreItem {
    Newtype(Newtype), Struct(Struct), Enumeration(Enumeration),
    Alias(Alias), TraitDefinition(TraitDefinition), ImplBlock(ImplBlock), FreeMethod(FreeMethod),
}
pub struct Newtype { pub visibility: Visibility, pub attributes: Vec<Attribute>, pub name: Identifier, pub wrapped: TypeReference }
pub struct Struct  { pub visibility: Visibility, pub attributes: Vec<Attribute>, pub name: Identifier, pub generics: Generics, pub fields: Vec<Field> }
pub struct Field   { pub visibility: Visibility, pub name: Identifier, pub type_reference: TypeReference }
pub enum Visibility { Public, Crate, Module(PathNode), Private }   // Private projects to empty
pub enum Attribute { Derive(DeriveGroup), Configuration(ConfigurationAttribute), ToolPath(PathNode), HelperDerive(HelperDerive), Opaque(OpaqueAttribute) }
pub struct DeriveGroup { pub paths: Vec<PathNode> }
pub struct ConfigurationAttribute { pub predicate: ConfigurationPredicate, pub inner: Box<Attribute> }
pub enum  ConfigurationPredicate { Feature(Identifier) }
pub struct HelperDerive { pub path: PathNode, pub derived: DeriveGroup }
pub struct PathNode { pub segments: Vec<Identifier> }             // dotted in logos, `::` in Rust — one home
pub enum  TypeReference { Path(PathNode), Application(TypeApplication) }
pub struct TypeApplication { pub head: PathNode, pub arguments: Vec<TypeReference> }
pub struct Generics { pub parameters: Vec<GenericParameter> }
```

Totality stays structural (lowering §2.2): `impl` over `CoreItem` matches all
variants, no wildcard; every child slot is a bound type, so a non-projecting node
is a compile error, not a runtime skip.

**[observed — this session's reconnaissance] The CoreSchema half already exists.**
`repos/schema-language/src/core.rs` already carries a stringful-but-Core-shaped
family: `CoreType { Struct(CoreStruct) | Enum(CoreEnum) | Newtype(CoreNewtype) }`,
`CoreSchema`, `CoreDeclaration { visibility, parameters, value, impls }`,
`CoreField { identifier, reference }`, and — load-bearing — `CoreReference` with
**projection-by-kind, never by head string**: `SingleTypeApplication { projection:
SingleTypeReferenceProjection { Vector | Optional | ScopeOf }, argument }`,
`MultiTypeApplication { projection: MultiTypeReferenceProjection { Map }, arguments }`,
`ValueApplication { projection: ValueReferenceProjection { Bytes }, value: u64 }`.
Its own comment (schema.rs:2364-2377) states the invariant: applications "dispatch
on **kind and projection** and never on a head string" — the "generics by kind"
ruling already real in code. So `CoreSchema ≈` this existing `CoreType` family
(three declaration kinds), and `CoreLogos` (the `CoreItem` above) is its
**Rust-1-to-1 extension** (seven item kinds, visibility/attributes/generics as
data). The two share `NominalIdentifier` → becomes `Identifier` (§3) once
stringless. This is why Phase B (§8) is "migrate Schema onto the contract," not
"invent CoreSchema": the Core is half-built; the work is stringless-ification plus
the sidecar forms.

### 6.3 The logicalization is shared; Rust has more custom leaves — and adding a third language

**[interpretation]** The shared **logicalization vocabulary** is the
`StructuralElement` set of §4.1 (atom, leaf, delimited-with-cardinality, object-
prefixed, application, dotted, delegate, literal) plus the evaluator, with disjoint
alternatives at the entry level. TextualLogos leaves are `Delegate`/`Atom`/
`Leaf(Scalar)`; TextualRust leaves are mostly `Leaf(Foreign)` (syn/prettyplease-
backed). What a **third** emission language (say a C or a Zig backend) touches:

```
[ (add   [a TextualForm impl] [a RawLayer for it: its own parser+printer or a Recognizer profile]
         [Foreign leaf codecs for its non-structural constructs]
         [expectation-table entries mapping each CoreLogos type to that language's form])
  (reuse [the StructuralForm vocabulary] [the evaluator] [the conformance harness]
         [CoreLogos unchanged] [the NameTable] [content-identity]) ]
```

The kernel (`CoreLogos` + the shared evaluator + the vocabulary) never grows
per-language; a language is **data + custom leaves**, exactly the Shen/K-Lambda
shape the lowering report §5.2 names as the Phase-D prize.

## 7. Worked example end to end — CommitSequence and DatabaseMarker, real data

Schema source (one line each): `CommitSequence.{ Integer }` and
`DatabaseMarker.{ CommitSequence StateDigest }`.

### 7.1 The NameTable rows (continuous schema→logos space)

```
;; positional (index name) — the stringless substrate both Cores share.
[ (0  Integer)          (1  CommitSequence)  (2  StateDigest)     (3  DatabaseMarker)
  (4  commit_sequence)  (5  state_digest)                          ;; derived field names
  (6  rkyv) (7 Archive) (8 Serialize) (9 Deserialize)             ;; derive path segments (logos-added)
  (10 Clone)(11 Debug)  (12 PartialEq)(13 Eq)
  (14 nota) (15 NotaDecode)(16 NotaDecodeTraced)(17 NotaEncode)
  (18 rustfmt)(19 skip)  (20 nota-text) ]
;; indices 0-5 are the SCHEMA table; 6-20 are the logos append-extension
;; (extend_from), so CommitSequence stays index 1 across both Cores.
```

### 7.2 CoreSchema value (minimal), then the Nomos macro, then CoreLogos value (full)

`CoreSchema` carries only the declaration — no derives, no attributes (those are
added by the `WireNewtype`/`WireStruct` Nomos macros over Core, outside text; nomos
model report §2):

```
CoreSchema:  Newtype  { name: Id(1), wrapped: Path[Id(0)] }
             Struct   { name: Id(3), fields: [ Field{ ty: Path[Id(1)] }, Field{ ty: Path[Id(2)] } ] }
;; note: schema fields elide their names (derived), so CoreSchema Field has no explicit name here;
;; the name is materialized as Id(4)/Id(5) when the field-name rule runs at the CoreLogos boundary.
```

After the `WireNewtype`/`WireStruct` macros (CoreSchema + NameTable → CoreLogos,
over Core), the CoreLogos values carry every Rust token as data (lowering §4.1/§4.2):

```
CoreLogos CommitSequence = CoreItem::Newtype(Newtype {
  visibility: Public,
  attributes: [
    ToolPath(Path[Id(18),Id(19)]),                                   ;; rustfmt.skip
    Configuration(ConfigurationAttribute {
      predicate: Feature(Id(20)),                                    ;; feature = "nota-text"
      inner: Derive(DeriveGroup[ Path[14,15], Path[14,16], Path[14,17] ]) }),  ;; nota.*
    Derive(DeriveGroup[ Path[6,7], Path[6,8], Path[6,9], Path[10], Path[11], Path[12], Path[13] ]),
  ],
  name: Id(1),
  wrapped: TypeReference::Path(Path[Id(0)]),                         ;; Integer
})

CoreLogos DatabaseMarker = CoreItem::Struct(Struct {
  visibility: Public, attributes: [ …identical three nodes… ],
  name: Id(3), generics: Generics{ parameters: [] },
  fields: [ Field{ visibility: Public, name: Id(4), type_reference: Path[Id(1)] },
            Field{ visibility: Public, name: Id(5), type_reference: Path[Id(2)] } ],
})
```

### 7.3 The structural-program entries (sidecar forms)

The TextualSchema codecs for the two constructors (queried by `ScopedCoreTypeId`,
§4.3). Shown in AMENDED ConstructorCodec form (§4.6): authoring vocabulary on decode,
one canonical encode form, sequence algebra in place of cardinality.

```
;; newtype constructor: ObjectPrefixed is authoring sugar; it normalizes to Application.
ConstructorCodec { constructor: Newtype, signature: [ Name Type ],
  decode_forms: [ ObjectPrefixed(ObjectSymbolPrefixedBlock {          ;; authoring surface
      object: AtomForm{ case: Some(PascalCase), sigil: None },
      block:  DelimitedBlock{ delimiter: Brace,
                sequence: Product([ Atom(AtomForm{ case: Some(PascalCase), sigil: None }) ]) } }) ],
  encode_form: Application(ApplicationForm{ .. }) }                    ;; canonical (normalized) form

ConstructorCodec { constructor: Struct, signature: [ Name Fields ],
  decode_forms: [ Application(ApplicationForm {
      head:    Atom(AtomForm{ case: Some(PascalCase), sigil: None }),  ;; the struct name
      payload: Delimited(DelimitedBlock{ delimiter: Brace,
                 sequence: Repeat{ minimum: 0, maximum: None,          ;; zero-or-more fields
                                   element: Delegate(Field) } }) }) ],
  encode_form: <same Application> }

;; Field is a Core type with TWO constructors, each its own ConstructorCodec:
ConstructorCodec { constructor: Field::TypeOnly, signature: [ Type ],
  decode_forms: [ Atom(AtomForm{ case: Some(PascalCase), sigil: None }) ],   ;; name elided-derived
  encode_form:   Atom(AtomForm{ case: Some(PascalCase), sigil: None }) }
ConstructorCodec { constructor: Field::Named, signature: [ Name Type ],
  decode_forms: [ Application(ApplicationForm{
      head:    Atom(AtomForm{ case: Some(CamelCase),  sigil: None }),        ;; field name (lowercase)
      payload: Atom(AtomForm{ case: Some(PascalCase), sigil: None }) }) ],
  encode_form: <same Application> }
;; validate_no_silent_conflicts proves the two Field decode_forms disjoint; on encode the
;; Core Field variant selects its own ConstructorCodec's single encode_form.
```

### 7.4 Decode of the schema text

`decode("CommitSequence.{ Integer }", &mut names)` through `TextualSchema`:

1. `Recognizer(Standard).recognize` → `Application{ head: Atom("CommitSequence"),
   payload: Delimited{ Brace, [ Atom("Integer") ] } }` — raw structure only.
2. Expected type at the boundary = `CoreTypeId(Newtype)`; look up its entry
   (the single `ObjectPrefixed` variant). The input never selected its own type.
3. Evaluator walks form+block in lockstep: object head `PascalCase` atom
   "CommitSequence" → `intern` → `Id(1)`; the brace block's `children` atom
   "Integer" (the wrapped type name) → `intern` → `Id(0)`.
4. Yields `StructuralValue`; the generated `StructuralCodec::decode` yields the
   concrete `Newtype{ name: Id(1), wrapped: Path[Id(0)] }`; conformance asserts
   they mirror. → CoreSchema value of §7.2.

### 7.5 Encode to TextualLogos text and to the verbatim golden Rust

**TextualLogos encode** of the CoreLogos `Newtype` (names resolved, derives present
as data; the logos text form re-sugars the attribute vector and elides derived
field names):

```
Public.CommitSequence.{ Integer }
```

(visibility as right-associative application; the derive/attribute vector renders
in the logos surface per its own forms; field names elided where they equal
`snakeCase(Type)` — text-side rule only, lowering §2.3.)

**TextualRust encode** (`SynReader`/`PrettyPlaceWriter`, one prettyplease pass) →
the **verbatim golden** (lowering §4.1, `spirit-reactive-large.generated.rs:83-89`):

```rust
#[rustfmt::skip]
#[cfg_attr(
    feature = "nota-text",
    derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode)
)]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct CommitSequence(Integer);
```

and for `DatabaseMarker` (lowering §4.2, `signal.rs:724-733`):

```rust
#[rustfmt::skip]
#[cfg_attr(
    feature = "nota-text",
    derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode)
)]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct DatabaseMarker {
    pub commit_sequence: CommitSequence,
    pub state_digest: StateDigest,
}
```

Both from the **same** CoreLogos values, through two forms of one family. The
two-way harness (lowering §6.5) runs `decode(golden) → CoreLogos → encode →
byte-exact golden` over the wire-contract goldens, needing zero hand-authored logos
fixtures. The `.`→`::`, the four-line cfg_attr wrap (prettyplease width, not data),
and the field-name resolution are the only synthesized surfaces.

## 8. Dependency graph, consumer map, and the reconciled phase order

### 8.1 Dependency graph (post-reconciliation)

```
                 content-identity        (rkyv + blake3; ContentHash<Domain>, PortableArchive, Envelope)
                /               \
        name-table            raw-discovery      (raw-discovery → rkyv only; no Core dep)
                \               /
                 structural-codec           (Textual vocabulary + evaluator + sidecar registry + Textual forms)
                        |
     TextualSchema  TextualNomos  TextualLogos  TextualRust   (forms; TextualRust adds syn/prettyplease leaves)
```

Core language types (CoreSchema, CoreNomos, CoreLogos) depend on `content-identity`
+ `name-table` and **never** on `raw-discovery` or `structural-codec` — the whole
identity ruling enforced at crate-dependency level. [changed from Codex: Codex's
single "language-core" is kept split into content-identity + name-table so hashing
sits below names; Codex's "envelopes" absorbed into content-identity (§2).]

### 8.2 Consumer map

```
[ (nota          gets [raw-discovery structural-codec content-identity-bound]  deletes [local-parser-as-sole-codec dead-rkyv-path])
  (schema/CoreSchema  gets [name-table content-identity TextualSchema]         deletes [Name(String)×123 field_name-copy local-ContentHash])
  (nomos/CoreNomos    gets [name-table content-identity TextualNomos(+$ profile)]  builds-new)
  (logos/CoreLogos    gets [name-table content-identity TextualLogos TextualRust]  builds-new)
  (schema-rust        becomes TextualRust leaves; goldens = cross-phase oracle;  harvested Phase D)
  (sema-engine        gets [content-identity-bound ContentHash<Domain>]         deletes [5-duplicate-digests; keeps domain strings as variants])
  (signal-frame       gets [content-identity-bound; absorbs Codex envelopes]    redirect [17 generated frame copies → calls])
  (signal-*×33        gets [content-identity-bound signal-frame-call]           deletes [rkyv-restatement generated-frame-copy]) ]
```

### 8.3 The one reconciled phase order

Two accepted orderings must become one: the library slate's **Phase L** (extract
`content-identity` from sema-engine first) versus Codex's **structural-front-end
first** ("the first next-gen stage should be the structural front end, not merely
repairing the 13 schema compilation errors"). **[AGENT PROPOSAL — one order, with
its derivation]**:

```
Phase L1  content-identity extracted from sema-engine (keystone).
          Why first: sema-engine is the one already-Core-first component with
          LOCKED-BYTE regression tests, so the lift is proven behavior-preserving;
          and the hash-exclusion property Codex REQUIRES for the sidecar table
          ("its own content identity, excluded from the Core hash") cannot exist
          until content-identity exists. Codex's own design depends on this.
Phase L2  name-table (greenfield, small). The Textual forms use the NameTable at
          every text boundary, so it must precede the structural front end.
Phase L3  raw-discovery — FREEZE the raw profile (Codex step 1), lift nota's Block
          + Recognizer, define RawProfile + revisions.
Phase L4  structural-codec — the structural-program data model + trusted evaluator
          + external sidecar registry + nota-derive entry generation + conformance
          harness (Codex steps 2-5). Express current NOTA behaviors as forms;
          DISSOLVE DottedExpectation and StructuralMacroNode into the general
          surface (Codex; and non-rejected StructuralMacroNode dissolution).
Phase B   migrate Schema onto the contract (Codex step 6) = Core-ify schema, i.e.
          stringless-ify the existing schema-language CoreType family (§6.2) + add
          its sidecar forms. (No "13 errors" exist on the current checkout, §10; if
          a branch carries them they resolve as a consequence of this migration,
          not a standalone patch — agreeing with Codex's emphasis.)
Phase C   add the Nomos profile + registry (Codex step 7); build CoreNomos/CoreLogos.
Phase D   TextualRust harvest; Logos becomes THE Rust generator; dialects = CoreNomos
          macro packages. Goldens byte-exact throughout via the two-way harness.
```

**The rationale that makes it one order, not a compromise:** Codex's "structural
front end first" is *correct in emphasis* and is honored — the front end (L3/L4)
lands before any Schema migration, exactly as Codex urges, and the "13 errors" are
fixed by migration rather than patched. But the front end cannot literally precede
the two foundations it structurally needs: `name-table` at every boundary, and
`content-identity` for the sidecar table's excluded co-versioned hash. So the
library's "identity first" wins by *derivation* (Codex's own hash-exclusion
requirement forces it), and Codex's "front end first" wins on *emphasis* (L3/L4
before Schema). One order satisfies both.

### 8.4 Changed-from ledger (every deviation, in one place)

```
[ (from library-report-§2.3  moved Named<Core> projection trait OUT of name-table
     INTO structural-codec as an external codec over Core-as-data — ruling 1 makes the view structural)
  (from library-report-§2.5/decision-8  RESOLVED entry-location fork → external sidecar keyed by CoreTypeId
     — derived from identity ruling, not chosen)
  (from library-report-§2.5/decision-7  nota-derive: "entries not codec bodies" → entries AND optimized
     codecs AND conformance — Codex triad; form authoritative, codec optimization, conformance the net)
  (from lowering-report-§1-§2  True* → Textual*; CoreItem/ProjectRust folded into the Textual family)
  (from lowering-report-§6  RustShape NAMED as TextualRust; ProjectRust one-way + RustShape two-way
     collapse into TextualRust encode/decode via the shared evaluator + Rust custom leaves)
  (from Codex  "language-core" KEPT SPLIT into content-identity + name-table (hashing below names);
     "envelopes" absorbed into content-identity)
  (from Codex  sidecar-vs-embedded OPEN → ANSWERED sidecar by derivation)
  (from Codex  table predates many-forms ruling → FOLDED into Textual family; TextualRust "profile"
     = the syn boundary, not a glyph profile)
  ;; corrections exposed by drawing the FULL data-tree (§4.1/§4.1.1), grounded in nota macros.rs:
  (from my-§4.1  period-string PipeTextForm/PrimitiveLeaf::PeriodString DROPPED → newest ruling:
     strings resolve by ScalarLeaf::Text using the SAME dotted rejoin as Float; wrapper depth = Delegate chain)
  (from my-§4.1  disjoint alternatives are the ENTRY shape (Vec<StructuralVariant>, nota StructuralVariantSet),
     NOT a StructuralForm variant → nested alternatives reached by Delegate)
  (from my-§4.1  cardinality folded into DelimitedBlock (nota object_count); standalone SequenceForm removed)
  (from my-§4.1  the $ escape rides on AtomForm.sigil (nota AtomShape.sigil); no separate Escape variant)
  (from my-§4.1  leaf moved out of AtomForm; AtomForm = case+sigil only, always a name; capture dropped (Nomos concern))
  (from my-§4.1  Cardinality = Any/Even/Exact(u64) (nota MacroObjectCount); SigilPosition = Prefix/Suffix (nota))
  ;; SUPERSEDED by the §4.6 Codex-kernel-hardening amendment (accepted on trust):
  (superseded-by-§4.6  "PipeText DROPPED" → RESTORED as LeafCodec::Carrier(PipeText); StringForm carrier)
  (superseded-by-§4.6  "standalone SequenceForm removed" → REINTRODUCED as the Product/Repeat algebra)
  (superseded-by-§4.6  "disjoint alternatives are the ENTRY shape (StructuralVariant)" → ConstructorCodec
     per Core constructor: many decode_forms, one encode_form, positional signature) ]
```

## 9. Forks — all three SETTLED

The three design forks this report raised are now all ruled; none remains open.

**Fork A — terminology: SETTLED.** `StructuralForm` for the parser-side data,
`macro` reserved for Nomos. His words: "instead of saying structural macro, we say
structural form" + Q2 "Yes, I agree on the surface." Crate name recommendation
stands at `structural-codec`.

**Fork B — `True*` → `Textual*`: SETTLED** (no longer hedged). His words: "when you
say true made no sense, true made no sense for any of them. It's just textual. It's
not more true or less true. So, yeah, textual. The textual schema and the textual
logos, actually." So `TextualSchema`/`TextualNomos`/`TextualLogos`/`TextualRust`
are the confirmed names; there is no `True*` anywhere.

**Fork C — trusted evaluator ships in the runtime: SETTLED.** His words: "yes, that
is great design, and a reason I was going this way." Dialect tables are data-loadable
at runtime and executed by the shipped evaluator; generated codecs remain the fast
path; the laws (§4.6) keep them in agreement.

**Not design forks I own — manager-tracked open items** (listed only so they are not
mistaken for settled design): the Core-side concept name; the epic scope / Spirit
pilot; the merge posture; and the schema-unit / parked "lost question." These are
tracked by the manager, not resolved here.

## 10. The "13 schema compilation errors" claim — cheaply verified, FALSIFIED

Codex asserts "the 13 schema compilation errors" on the multi-repo stack branch.
**[observed — this session's read-only `cargo check`]** No such errors exist on the
checked-out state: `repos/schema` (v0.2.0), `repos/schema-language` (v0.2.0), and
`repos/schema-rust` (v0.8.0) **all compile clean, zero errors**; a grep for the
claim across the three crates found nothing. So the branch-consequence framing
("don't merely repair the 13 errors, build the front end") stands on a premise not
present here — which strengthens, not weakens, the reconciled order: there is no
firefight to trade against, so the front end (Phase L3/L4) is built on its proper
foundations without pressure to patch first. If Codex's "13 errors" refer to a
different, unmerged branch, that is a dependency-portability flag (an unmerged
producer branch) — the design is unaffected either way.

## 11. Sources

Design corpus (this workspace): `reports/logos/shared-codec-library-v1.md`,
`logos-rust-lowering-v1.md`, `core-first-architecture-v1.md`,
`syntax-recrystallization-audit-v1.md`, `nomos-macro-model-v1.md`, `design-v0.md`,
`reports/codex-rust-construct-survey.md`; the Codex recrystallized-pipeline design
forwarded by the psyche this session; the manager's psyche-alignment assessment
(binding on the reconciliation). Code ground truth cited transitively through the
sibling reports (nota `next-gen`, schema, schema-rust goldens, sema-engine
`record.rs`/`versioning.rs`, signal-frame) plus this session's read-only
reconnaissance. No code was edited; repositories under `repos/` are untracked.
```