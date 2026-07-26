# Bad Data Shapes Register — family-wide audit, 2026-07-26

Five independent read-only auditors swept the family at origin refs
(local checkouts distrusted). Grades: A = violates an explicit psyche
ruling, B = violates the typed-shape doctrine, C = cosmetic. P suffix =
provisional on the unratified durable-family-identity rule. Governing
rulings: "fully typed struct, not a vector of strings"; "Exactness is
structural — errors are also structural values"; no two same-typed
positions a reader counts apart; field names illegal in encoded forms;
IDs are variant-wrapped u16; manifests/config tables in nota format.

## Cross-cutting patterns (the defect families)

P1. THE REJECTED SHAPE IS IN THE KERNEL. The psyche's complaint object
    is structural-codec's own SequenceForm::Product(Vec<StructuralForm>)
    (form.rs:110) — every consumer indexes positionally; sibling
    PositionalSignature(Vec<ScopedEncodedTypeId>) (ids.rs:104) is the
    codec field list with an unenforced doc-claimed invariant. Fixing
    this moves table-identity hashes (layout bump) — gated on psyche.

P2. TYPED HAPPY PATH, PROSE/RAW ERROR PATH. Everywhere, handwritten and
    generated: typed values in hand are degraded to u8/u32/String at
    the moment of failure. Instances: signal-frame operation_dispatch
    (u8s beside a correct WireRoute variant), generated SignalFrameError
    (raw ints two lines from the newtypes), EncodeError::ShapeMismatch
    (4 failures, one &'static str), schema ReifyShape (39 sites, 34
    English strings), nomos Generation (11 sites), spirit SEMA boundary
    (~15 hand-authored English literals string-matched downstream by
    render.rs:289), criome_gate re-stringifying its own GateRefusal enum.

P3. PARALLEL STRING TABLES. Index-aligned string vectors standing in
    for typed pairings: schema-rust Plane alias/canonical name vectors;
    generated HEADS: &[&str] duplicating enum variant names; CLI routing
    via containment in &[&str] head lists; trigger-role prose beside a
    closure that does the real check (same role spelled two ways).

P4. SAME-TYPED ADJACENT POSITIONS. Systemic: newtype visibility pair
    (known), schema universe 4x Option<ScopedEncodedTypeId>, nomos
    trait_impl(trait, self_type) swappable silently, (root, variant)
    Identifier pairs, RangeExpression two Options encoding 4 states,
    ProtocolVersion(u16,u16,u16), [u8;32] family-hash pairs in spirit
    migration, (certainty_rank, importance_rank) both u64 in the core
    read path, pinned/actual ContentHash pairs, first/second usizes
    indexing an ephemeral flattened Vec no caller can resolve.

P5. IDENTITY VALUES WITH INEXACT REPRESENTATIONS. Character sets as
    unsorted String — same set, different ContentHash (profile.rs:298,
    :120); ContentHash domain tag laundered off via from_bytes/bytes();
    legacy delimiter enum still in the hashed table pre-image beside
    the boundary trigger that supersedes it; zero-filled [0u8;32]
    layout identity placeholder in a hashed position.

P6. THE RULE TABLE PROBLEM. Load-bearing policy data hand-copied across
    languages with no single typed source: the pin/dependency-direction
    rule exists in 4+ places (Rust substring asserts in protos tests,
    shell regex, IFS='|' pin table, sed pattern); repository-shape
    allowlist; generated-file layout spelled in 3 places. Psyche ruling:
    such tables are nota data consumed by all enforcers.

P7. CONFIG THAT LIES. Types whose shape cannot hold what their surface
    claims: guardian AgentGuardianConfiguration::new accepts and
    silently discards provider/model/max-tokens (owner config is
    ignored at runtime); FreshnessCheck bool-mode fabricates the
    sentinel "<update variable unavailable>" which reaches the user as
    an instruction; Result<Option<T>,E> where Err is unconstructible;
    check-dependency-direction documents an operand it discards.

## Live bugs found by shape alone (not aesthetics)

L1. Nomos same-typed field grouping keys on derived SPELLINGS:
    Vector<Topic>, Optional<Topic>, Topic all derive "topic" and get
    ordinal-prefixed as if same-typed. Wrong generated output.
    core-nomos/src/name_boundary.rs:94-122, core-schema reference.rs:192.
L2. Expression::StringLiteral's only two production uses carry resolved
    name spellings -> renames move the logos content hash, falsifying
    core-logos' own rename-stability invariant. generation.rs:944,1687.
L3. schema-rust stale-artifact message tells the user to set an env var
    literally named "<update variable unavailable>". build.rs:823,865.
L4. Spirit guardian silently ignores configured provider/model/tokens.
    guardian.rs:79-130 vs bin/spirit-write-configuration.rs:63-69.
L5. Spirit DatabaseMarker renders read FAILURE as commit_sequence 0 /
    state_digest 0 — error indistinguishable from empty store.
    store/mod.rs (unwrap_or(0) pair).
L6. render.rs:289 string-matches "no matching record" against a prose
    error payload to recover meaning the type system threw away.
L7. triad-runtime to_string_lossy on env socket paths corrupts non-UTF8
    values before validation can name them. process.rs:425,437.
L8. ShortCode rkyv deserialize now routes through FromStr, so archived
    non-canonical spellings (e.g. "00000") fail to deserialize; the
    compatibility lock test only witnesses canonical spellings.
    content-identity/src/short_code.rs:165-174.

## A-grade register by layer

### structural-codec / raw-discovery / name-table / content-identity

EC1  form.rs:110 Product(Vec<StructuralForm>) + ids.rs:104
     PositionalSignature — P1. Replacement: typed position records per
     rule. GATED: moves table identity.
EC2  table.rs:409-413 trigger role as &'static str + parallel accepts
     closure; 9 prose sites, same role spelled two ways. Replacement:
     TriggerRole enum with admits(); model exists at raw-discovery
     TriggerTextRole (profile.rs:688).
EC3  evaluator.rs:363 block_kind -> &'static str; error field mixes
     block kinds and delimiter descriptions. Replacement: BlockKind
     enum in raw-discovery + ExpectedBlock sum.
EC4  disjoint.rs:262-269 first/second indices into an ephemeral
     flattened Vec — unresolvable by callers; AmbiguousTriggerSet
     unordered tie encoded as ordered pair. Replacement:
     DecodeFormAddress { constructor, form }; canonical TriggerTie.
EC5  value.rs:30, evaluator.rs:29, disjoint.rs:24 unnamed Application
     pairs dropping head/payload names; text.rs:1236 (&str,&str)
     dropping opening/closing; authoring.rs:37-38 operator/boundary
     adjacent same-typed. Replacement: named records / position
     newtypes (also dissolves EC2 at type level).
EC6  Span/position raw usizes: error.rs:112, text.rs:116,
     boundary.rs:18-71 (three same-typed SourceBounds), error.rs
     SourcePosition 3x pub usize. Replacement: ByteOffset/ByteLength/
     OpeningSpan/InteriorSpan/ClosingSpan.
EC7  error.rs:138 EncodeError::ShapeMismatch(&'static str) — 7 sites,
     4 distinct failures. SLATED (granular EncodeError). Also encode
     never validates atom case (no EncodeError::CaseMismatch) — text
     that will not decode back.
EC8  error.rs:87 ScalarParse(String) + two disagreeing scalar parsers
     (evaluator.rs:295 vs text.rs:969). One parser, typed failure enum.
EC9  Boolean spellings have three authorities (evaluator.rs:318 English
     match, text.rs:984 bool::parse, text.rs:1216 Display) in a
     profile-driven design. Replacement: BooleanKeywords in lexicon.
EC10 ids.rs:22,55,86 + form.rs:283 + table.rs:75 — type-id family bare
     pub u32; ForeignLeafId vs LeafCodecContractId two types for one
     concept with unenforced correspondence. Reference conformer:
     name-table Identifier variant-wrapped u16. QUEUED QUESTION: does
     the u16-variant ruling reach type-ids.
EC11 table.rs:33,49 [u8;32] pub identity fields laundering ContentHash
     domain tags; content-identity from_bytes/bytes() are the holes.
     GATED: identity plumbing.
EC12 recognizer.rs:117-145 ForeignLanguage { name: String }; new("Rust")
     != rust() silently. Replacement: closed enum.
EC13 recognizer.rs:186,261,276 errors fabricate unobserved characters
     (unwrap_or('?'), unwrap_or('|')); :234 fabricates empty body.
     Replacement: FoundClose sum incl. EndOfInput.
EC14 profile.rs:165-190 trigger spellings as raw String (Boundary/
     Carrier two adjacent same-typed) — untypedness manufactures
     validate-nonempty, TriggerTextRole, EmptyTrigger, and 90 lines of
     can_tie string surgery. Replacement: Spelling newtype + role
     positions. GATED: profile identity.
EC15 profile.rs:298,120 character sets as String — same set hashes
     differently. Replacement: canonical CharacterSet. GATED.
EC16 profile.rs:374 + recognizer.rs:401-411 numbered trigger table
     0..=6, meaning recovered by re-parsing matched text's first char.
     Replacement: NotaTrigger enum, derived root set.
EC17 textual_form.rs:71-76 ChunkName(pub String), canonical name is the
     English literal "unit". Replacement: enum { Unit, Filed(Identifier) }.
EC18 evaluator.rs:201, text.rs:314 missing-lexicon reported as
     LiteralMismatch. Add MissingLexicon.
EC19 name-table table.rs:298 intern silently returns existing id (the
     redefinition-error ruling has no enforcement layer — name-table
     has no define op; enforcement belongs at universe seal). SLATED
     (slice 1 builtins path).

### core-schema / core-logos / core-nomos

LL1  Type-id family bare u32 (ScopedEncodedTypeId, EncodedConstructorId)
     — same as EC10; nomos additionally still compiles against the old
     FLAT Identifier(u32) via its stale pin. SLICE-0 repin + QUEUED
     QUESTION on ruling scope.
LL2  StringLiteral carries resolved names — live bug L2. QUEUED
     QUESTION: NameLiteral(Identifier) vs accept rename-instability.
LL3  Fixture rules as five-position homogeneous vectors with two
     Visibility delegates told apart by counting (core-logos tests
     textual.rs:206, core-schema fixture.rs:274,298) — the ruling's
     own example. Falls out of P1 fix + typed rule vocabulary.
LL4  Same-typed adjacencies: universe.rs:91-94 four Option slots (use
     existing ScalarSlot as key); error.rs 4 instances (incl. a
     FABRICATED codec count at universe.rs:452); trait_impl positional
     (trait, self_type) — proof of harm: one call site passes
     ("Request","Request"); (root, variant) Identifier pairs;
     RangeExpression 2 Options for 4 states (2 legal); IndexExpression;
     textual.rs input/output slots.
LL5  GenerationClass: 6 payload-free variants driving 1841 lines of
     handwritten dispatch — inverse of "macros are data filling those
     variants". ConstructorSource in same file is the correct pattern.
     Largely superseded by slice rebuild of generation.
LL6  Prose errors: ReifyShape 39 sites/34 strings; ReifyUnknownType
     (String); nomos 5x &'static str variants incl. Generation 11
     sites. Typed vocabularies already exist for most.
LL7  Vec<InterfaceRoot> where index 0 = request, 1 = reply, consumed by
     counting. Replacement kills 6 of the 11 Generation prose sites.
LL8  PathNode segment bags: path(&["rkyv","rancor","Error"]) — 85 call
     sites mixing crate/module/type/constructor roles; worst mixes
     literal and variable in one slice.
LL9  Stringly grouping bug L1 (group by type identity, not spelling).
LL10 Short-header layout as bit arithmetic (u64 shifts, usize/u8/u64/
     u128 laundering) instead of a typed layout record.
LL11 Builtins string-keyed HashMap + spelling functions returning
     &'static str ("Vec"/"Option"/"ScopeOf"/"Map", leaf_path("Integer"))
     — SLATED (slice 1 builtins-as-priors).
LL12 Option-as-mode: ImplBlock.implemented_trait (two constructors
     already exist because of it), Function receiver/return_type,
     FieldInitializer.value None-means-shorthand.
LL13 MemberKind::Primitive payload-less, forcing a parallel
     Vec<(ScalarSlot, ScopedEncodedTypeId)> — highest leverage-to-size
     single fix in the language layer.

### protos / protos-engine / schema-rust / textual-rust

CE1  ContractCrateBuild: four adjacent impl Into<String> positions in
     the public build API; the correct newtypes already exist private
     to the bin — promote them. Highest blast radius here.
CE2  Cargo feature as String literal 12 sites; gate belongs in a
     compilation-config record per the Cargo-metadata ruling.
CE3  RustEmissionOptions: target + Option<family> two fields for one
     sum; MissingWireContractFamily error exists only because the
     record admits the invalid state; invariant bypassable via pub
     fields. Fold family into the WireContract variant.
CE4  WireBinding { contract_id: u32, wire_revision: u16 } strips
     protos' typed identity at the seam; rebuild as
     WireBinding(signal_frame::ContractBinding).
CE5  FreshnessCheck bool-mode -> live bug L3. Enum with the update
     variable on the CheckOnly arm.
CE6  RuntimePlaneSet enum->3 bools->Vec<Plane> round trip; delete type.
CE7  Plane parallel string vectors (alias vs canonical names) — P3.
     PlaneRole enum pairing both names. Psyche scope call pending on
     whether the plane vocabulary survives the new engine.
CE8  textual-rust subset boundary in prose: 10 error variants carrying
     construct: &'static str, three prose-map traits + ~80 inline
     literals, catch-all arms defeating closedness; `rendered: String`
     holds source text at 6 sites and English descriptions at 4.
     The classification is surviving knowledge — retype as closed
     UnmodeledX enums before the corpus knowledge is lost.
CE9  Pin/dependency policy in 4+ hand-copies (P6): protos test
     substring-asserts a revision literal; protos-engine pin table in
     shell with 3 internal copies + sed; dependency-direction regex.
     One nota table consumed by flake, checker, test.
CE10 protos wire_identity: registry declared via 9-position ident
     macro DSL (B, const-validated); RegistryValidationError 6
     payload-free variants discarded to prose panic; retirement
     declared first-class then modeled as Option (current_binding);
     pinned/actual same-typed pairs (role newtypes); ShortCode
     domain-erased beside domain-typed ContentHash in the same
     contract; CLI maintains a parallel hand-written family enum with
     no sync guard.
CE11 Structural identity round-tripped through "crate:module" string
     with strip_prefix recovery (build.rs:372-385).
CE12 Option<ZST> as bool (tcp_tier: Option<TcpListenerTier>), collapsed
     into five duplicated bool sets across token structs.
CE13 Result<Option<PathBuf>, BuildError> with unconstructible Err;
     Cargo metadata seam stringly both sides sharing no key;
     generated-file layout spelled in 3 places (silent-stale hazard);
     ModuleFeedback path typed/stringly split; RuntimeRoleTraitImpl
     matcher consults canonical_type_name while the field named
     type_name is never read (P7 specimen).

### signal-frame / triad-runtime / contract repos (keep-material)

WF1  log_variant() -> u64 hand-packed route bits — root cause forcing
     raw-u64 handling into every generated contract; return WireRoute.
WF2  operation_dispatch errors carry bare u8s beside a correct typed
     sibling variant; swap to RootCode/VariantCode.
WF3  command_line: working/meta head routing via &[&str] containment
     (P3); UnexpectedFrame { got: format!("{other:?}") }; three error
     junctions discard the crate's own typed taxonomy via to_string();
     hand-rolled length-prefix parse duplicating frame.rs helpers.
WF4  ProtocolVersion three positional u16s.
WF5  triad-runtime: to_string_lossy L7; EngineRequestError/Listener
     errors as detail: String; PathBuf-vs-RuntimeSocketPath double
     representation; --pretty magic string -> bool where NotaOutputForm
     is named in the doc.
WF6  signal-spirit Domains::from_strings substring-sniffs ~10 &[&str]
     needle lists to re-derive a typed taxonomy, silent fallback.
WF7  judge ContentHash accepts any non-empty string via generic macro.
WF8  Generator-stamped (fix generator, not output): SignalFrameError
     raw ints; EngineRefusal { detail: String } prose on the wire;
     frame-kind dispatch on string literals; magic (u8,u8) route
     matches beside the typed route enums; HEADS parallel string
     array; ~50 hand-packed short-header hex consts; WireRoute
     repacked into u64 (consequence of WF1); Integer/Boolean/Path raw
     aliases latent hazard.

### spirit port (worktree)

SP1  SEMA boundary prose errors, string-matched downstream — L6.
     Closed SemaMissReason enum; may need schema-level change to
     ErrorReport/ErrorMessage.
SP2  Five faults collapsed to ConfigureRejectionReason::InternalError,
     one site let _ = error.
SP3  criome_gate re-stringifies its own typed GateRefusal (the file
     does it right one function above).
SP4  open_with_family_identity(path, [u8;32], [u8;32]) same-typed
     positional pair across ~6 call sites — silent wrong-table on
     transposition. A regardless of the unratified hash rule.
SP5  Magic [u8;32] constants + equality-chain dispatch (3 current + 14
     historical + generated) instead of a closed generation registry.
     A for shape; P on whether identity is a hash at all.
SP6  Observation sort key (certainty_rank, importance_rank) both u64 —
     core read path ordering.
SP7  DatabaseMarker unwrap_or(0) — L5.
SP8  Guardian config discards 3 of 5 constructor params — L4.
SP9  Operation identity crosses the criome socket twice, once typed,
     once as a matchable bare string.
SP10 B-tier: raw-keyed mail ledger (Integer keys because identifiers
     lack Hash); format!-built composite record keys; record
     identifiers as bare String internally with RecordIdentifier only
     at the wire edge; env-var socket defaults bypassing the typed
     Configuration; publish_checkpoint bool conflating published with
     mirroring-off; positional Option-heavy generated constructors at
     every call site.

## Sequencing

Tier 1 — standalone fixes, no identity movement, no ruling needed:
  WF1+WF2 (one train, signal-frame), CE5 (live bug), CE1 (promote
  existing newtypes), EC13, EC18, SP7, SP8, WF5 lossy-path fix.
Tier 2 — folded into vertical slices (already slated): EC7, EC19,
  LL5, LL11, and every shape on the slice path (typed rule vocabulary
  IS the P1 fix for the Rust vocabulary).
Tier 3 — GATED on psyche rulings:
  (a) kernel typed positions + identity/layout bump (EC1, EC11, EC14,
      EC15, B5 delimiter-in-preimage, zero-filled layout id);
  (b) ID-ruling scope (EC10/LL1, ContractId, ShortCode domain);
  (c) StringLiteral remedy (LL2);
  (d) plane-vocabulary survival (CE7).
Tier 4 — generator-stamped shapes (WF8): die with schema-rust; encode
  the lessons as requirements on the new engine's emission instead.

## Confirmed clean

signal-domain entirely; triad-runtime daemon/runner/frame plumbing;
signal-frame newtype family and error taxonomy (apart from named
junctions); judge typed request/reply vocabulary; spirit config.rs;
generated RecordFamilyError and WorkingInputLane (positive exemplars);
meta-signal-spirit typed Selected*Target wrappers; no Vec<u8> untyped
payloads anywhere in handwritten wire code.

## Open questions queued for the psyche (one at a time)

Q1. Does the typed-record ruling reach the protos kernel itself —
    Product becomes typed positions, accepting the content-hash/layout
    bump now while consumers are zero? (Tier 3a hangs on this.)
Q2. Does the variant-wrapped-u16 ID ruling reach type-ids
    (ScopedEncodedTypeId, EncodedConstructorId), ContractId
    (NonZeroU32), and ShortCode (u64, domain-erased)?
Q3. StringLiteral remedy: interned NameLiteral(Identifier) restoring
    rename-stability, or accept rename-instability and correct the
    architecture doc?
Q4. Does the Plane/role vocabulary survive into the new engine as
    typed domain data, or is it re-derived from logos (drops CE7 to
    cosmetic)?
