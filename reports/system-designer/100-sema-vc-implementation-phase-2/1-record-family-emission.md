# 100/1 — schema-next family declarations + schema-rust-next RecordFamily emission

*Continuation-builder chapter (interrupted run `wf_9da92403-3c4` recovered into run `wf_948413c9-560`, 2026-06-12, system-designer lane). Adversarial review appended.*

# Storage family declarations + record-family emission — completion report

## Part 1 — schema-next, branch `storage-family-declarations` (head 89fe33a9)

The recovered wip commit 2755dfe1 was substantially complete and correct; I absorbed it, added the one missing witness, wrote the intent/architecture prose, and shipped it as commit 89fe33a9 "family declarations: schema-declared stored record families on the stream-metadata precedent".

What the recovered work already had (verified against the spec, kept as-is):

- Authored form `EntryFamily (Family { record Entry table entries key Domain })` in the namespace map, mirroring the stream precedent exactly: `SourceFamilyBody` / `SourceFamilyFields` (src/source.rs:938-1063) are structural twins of `SourceStreamBody` / `SourceStreamFields` (src/source.rs:795-935) — `NotaBody::from_delimited` typed delimiter reading, even-map-entry checks, required-field assembly.
- Semantic `FamilyDeclaration { name, record, table, key }` (src/schema.rs:948-975) as a sibling of streams/relations on `Schema` (src/schema.rs:215), excluded from namespace type declarations (`SourceDeclarationValue::is_type_declaration` src/source.rs:789-791; engine-side `MetadataDefinitionProbe` src/engine.rs:891-920), carried through `SchemaEditor`/upgrade rebuild (src/upgrade.rs:317-573), rkyv-derived, and written back out in the canonical source projection (`SourceFamilyBody::to_schema_text` src/source.rs:989-1004).
- `TableName` newtype with bare-atom-aware NOTA encode (src/schema.rs:878-911) — the storage coordinate deliberately separate from schema symbols.
- `FamilyKey` as a closed two-variant keyword structural macro node, `Domain | Identified` (src/schema.rs:917-946, `#[shape(keyword = ...)]` via `nota_next::StructuralMacroNode` derive), decoded with `FamilyKey::from_structural_block` (src/source.rs:1038).
- Typed errors with tests: `SchemaError::FamilyRecordNotFound` (enforced on BOTH lowering paths through `Schema::families_verified`, src/schema.rs:296-317 + src/engine.rs:450-461 + src/source.rs:172-187), `DuplicateFamilyName`, `DuplicateFamilyTable` (src/source.rs:439-461).
- Fixture tests/fixtures/source-codec/family-declarations.schema and 7 witnesses in tests/family_declarations.rs.

What I added:

- The missing rkyv witness `semantic_schema_carrying_families_round_trips_through_rkyv` (tests/family_declarations.rs:84-96) — the brief required the semantic `Schema` (not just the source artifact) to round-trip carrying families.
- INTENT.md: new constraint paragraph "Stored record families are schema-declared metadata" bracket-quoting Spirit wrjl (Decision) with identifier; x0ja already quoted on the branch base.
- ARCHITECTURE.md: family-declarations paragraph beside the stream-declarations paragraph in the Authored Schema Source section.

Verification: full suite green (15 suites, includes the 8 family tests), `cargo fmt --check` clean. Clippy: 3 pre-existing warnings, none introduced by this branch — `large size difference between variants` (src/macros.rs:222), `too many arguments 9/7` on the pub(crate) `Schema::new` (src/schema.rs:220; it already warned at 8/7 on the base commit), `manual_range_patterns` (src/source.rs:36). I left them: all three pre-date the branch and fixing the constructor shape mid-branch would churn three files for a pub(crate) surface.

## Part 2 — schema-rust-next, branch `record-family-emission` (head 9892d59d, from origin/main cedb2e06)

Built from zero (nothing was recovered for Part 2). Cargo.toml points `schema-next` at branch `storage-family-declarations` (Cargo.lock pins it at exactly the Part 1 head 89fe33a92ade) and adds dev-dependency `sema-engine` at branch `versioned-family-identity` (0.3.0, pinned 53426b14).

Lowering (src/lib.rs:825-925): `LowerToRust<RustVersionedStore> for Schema` builds the model — store name from `Schema::identity().component()`, plus one `RustRecordFamily { declaration, schema_hash }` per declared family, with `schema_hash` computed AT GENERATION TIME as `*schema.family_closure(record).expect(..).content_hash().expect(..).as_bytes()` (panics only on an internal invariant violation, since Part 1's `families_verified` guarantees resolution; matches the crate's existing expect-on-invariant idiom). `RustModule` carries `versioned_store` beside streams/relations with a public accessor.

Emission (renderer method `emit_record_family_support`, src/lib.rs:4787-4837, gated by `!versioned_store.is_empty()` in `RustModule::render` at src/lib.rs:325-327 — a schema without families emits nothing new, asserted by test). Three `ToTokens` sections through the single `prettyplease` pass, per the repo's token-wrapper law:

1. `FamilyIdentityModuleTokens` (src/lib.rs:3857-3889) — `pub mod family_identity { pub const ENTRY_FAMILY: [u8; 32] = [...]; ... }`, SCREAMING_SNAKE family names via the existing `ScreamingName` noun, on the `short_header` module precedent. The generated artifact pins the identity; the existing build-driver freshness check needs no new machinery.
2. A fixed-token `RecordFamilyError` enum (UnknownFamily / SchemaHashMismatch {family, stored, generated} / RecordDecode, all carrying `sema_engine::FamilyName` / `sema_engine::SchemaHash`) with Display + Error impls, emitted the same way the generated `SignalFrameError` is.
3. `RecordFamilyEnumTokens` (src/lib.rs:3891-3990) — the closed sum `pub enum RecordFamily { EntryFamily(Entry), ObservationFamily(Observation) }` whose impl owns the whole surface: `STORE_NAME` (schema identity component name), `versioning_policy() -> sema_engine::VersioningPolicy`, per-family snake_case descriptor constructors (`entry_family() -> sema_engine::TableDescriptor<Entry>`, `observation_family() -> sema_engine::IdentifiedTableDescriptor<Observation>`, key kind selecting the descriptor per sema-engine's two registration shapes), and `decode(identity: &sema_engine::FamilyIdentity, bytes: &[u8]) -> Result<Self, RecordFamilyError>` dispatching on (family name, schema hash) with hash drift and unknown identity as typed hard errors and rkyv payload decode per variant. All paths reference the real `sema_engine` crate exactly as wire targets reference `signal_frame::`.

Witnesses (tests/family_emission.rs, 8 tests; fixtures tests/fixtures/record-families.schema with one Domain-keyed and one Identified family, and the checked-in generated module tests/fixtures/families_generated.rs):

- `family_declarations_emit_the_version_control_surface` — fragment assertions + byte-exact `assert_generated_fixture` snapshot.
- Compile witness, the repo's strongest existing form: the checked-in generated module is `#[path]`-included into the test crate and compiles against the REAL sema-engine (versioned-family-identity), signal-frame, and triad-runtime dev-dependencies — the same idiom as `spirit_generated.rs`.
- `generated_decode_round_trips_both_families` (rkyv bytes through real `FamilyIdentity` values from the generated descriptors), `generated_decode_rejects_an_unknown_family` and `generated_decode_rejects_schema_hash_drift` (full typed-error equality, not just variant matching), `generated_descriptors_carry_the_pinned_family_identity`, `generated_versioning_policy_names_the_component_store`.
- `schema_field_change_moves_the_emitted_family_constant` — adding a field to Entry moves the EntryFamily hash at both the model and emitted-const level while ObservationFamily's constant stays fixed (per-family isolation).
- `schema_without_families_emits_no_family_surface` — spirit-min emits no `RecordFamily`, no `family_identity`, no `sema_engine` reference.

INTENT.md: new paragraph "Declared record families emit the component's version-control surface" bracket-quoting wrjl (Decision) and v0n6 (Clarification) with identifiers. ARCHITECTURE.md: full constraint bullet in the Constraints section.

Verification: full suite green (9 suites, 75 tests total incl. the 8 new), `cargo clippy --all-targets` ZERO warnings, `cargo fmt --check` clean, `cargo build` clean.

## Cross-cutting verification note (v0n6)

The brief's "all reading through typed structural macro nodes; no string-matched heads, no positional indexing" is satisfied where the substrate allows: the key kind is a derived keyword structural macro node, and all reading operates on typed `NotaBody`/`Block` structures, never re-parsed text. However the `(Family {...})` / `(Stream {...})` head discrimination and the brace key/value field payload read through the stream-precedent hand-shaped path (`demote_to_string` head check + `chunks_exact(2)` pairs), because nota-next's structural shape vocabulary (pascal_atom / keyword / headed-arity in /git/github.com/LiGoldragon/nota-next/derive/src/lib.rs:846-915) has NO brace-map shape — a `StructuralMacroNode` for the family body is currently inexpressible. Per v0n6's own rule ("If structural macro nodes cannot express a needed shape, that signals the NOTA design was not implemented properly and must be surfaced to the psyche rather than worked around"), this gap is surfaced in blockers rather than silently absorbed.

## branches
- schema-next @ storage-family-declarations head 89fe33a92ade08af0f1e81a69a3c0016b7699a2c (/home/li/wt/github.com/LiGoldragon/schema-next/storage-family-declarations)
- schema-rust-next @ record-family-emission head 9892d59d7cd23dc47bdb375bf9a78a1d813f25e7 (/home/li/wt/github.com/LiGoldragon/schema-rust-next/record-family-emission)

## designDecisions
RECOVERED PART-1 CHOICES KEPT: (1) The stream-precedent reading shape for SourceFamilyBody/SourceFamilyFields — kept verbatim because the brief's first requirement is "follow the stream-declaration precedent" and nota-next's structural shape vocabulary has no brace-map shape, so a derived StructuralMacroNode for the body is currently inexpressible (gap surfaced in blockers per v0n6); the key kind IS a derived keyword structural macro node. (2) FamilyKey as Domain|Identified closed keyword enum, TableName as a separate NOTA-encoding newtype, FamilyDeclaration as a sibling of streams/relations on Schema, families_verified() called on both lowering paths so record resolution is enforced regardless of entry point — all kept. (3) Duplicate-name/duplicate-table checks living in SourceNamespace::family_declarations (shared by both paths) — kept. REVISED/ADDED: only the missing semantic-Schema rkyv witness, INTENT/ARCHITECTURE prose, and the real commit message; nothing in the recovered code needed rework.

FAMILIES-SURFACE ATTACHMENT (Part 2): registry-on-the-closed-sum, not on-record-type. The generated RecordFamily enum owns the entire surface (STORE_NAME, versioning_policy, per-family descriptor constructors, decode). Deciding argument: a family's record type may be a cross-crate import, which emits as a Rust alias re-export — Rust forbids inherent impls on foreign types (E0116), so on-record-type attachment would break exactly the imported-record case Part 1 explicitly allows. Secondary arguments: the sum is a real data-bearing schema-emitted noun (no ZST holder); descriptor constructors are variant-correlated associated constructors, the same category as the repo's emitted enum variant constructors; one noun keeps the version-control surface cohesive and greppable. Constructor names are snake_case family names (Name::field_name), constants are SCREAMING family names via the existing ScreamingName noun on the short_header-module precedent — both collision-free because Part 1 rejects duplicate family names.

GENERATION-TIME HASHING vs FRESHNESS: the hash is computed during LowerToRust<RustVersionedStore> for Schema while the semantic value is in hand (blake3 of the family closure's canonical rkyv bytes, domain-separated from the whole-schema hash), then frozen into the emitted family_identity constants. Freshness needs zero new machinery: the constants are part of the generated artifact the existing GenerationDriver already freshness-checks against the working tree, so any schema edit that moves a family closure fails the build until deliberate regeneration — the artifact diff shows exactly which family's identity moved (witnessed by schema_field_change_moves_the_emitted_family_constant, which also proves per-family isolation: an Entry edit does not move ObservationFamily's constant). Emission is target-independent (any target with declared families gets the surface; none declared, nothing emitted) — declaring families is the explicit opt-in, and it adds sema-engine to the consumer's dependencies, documented in ARCHITECTURE.md.

COMPILE-WITNESS FORM: the repo already had the strongest honest form — checked-in generated fixture #[path]-included as a test module compiling against real runtime dev-dependencies (spirit_generated.rs precedent) — so I used it rather than a cargo-checked scratch crate: families_generated.rs compiles against real sema-engine (branch versioned-family-identity) and the runtime tests drive the generated decode/descriptor/policy paths with real FamilyIdentity values.

## testResults
schema-next (storage-family-declarations): cargo test — all 15 suites pass, 0 failures. New suite tail:

running 8 tests
test duplicate_family_names_are_a_typed_error ... ok
test duplicate_family_tables_are_a_typed_error ... ok
test family_declarations_lower_to_semantic_schema_metadata ... ok
test family_record_must_resolve_to_a_declared_type ... ok
test family_declarations_round_trip_through_canonical_schema_source ... ok
test family_key_kind_is_a_closed_structural_choice ... ok
test family_record_closure_hashes_through_the_content_identity_surface ... ok
test semantic_schema_carrying_families_round_trips_through_rkyv ... ok
test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

cargo clippy --all-targets: 3 warnings, ALL pre-existing on the branch base (large enum variant src/macros.rs:222; Schema::new 9/7 args src/schema.rs:220 — already 8/7 before this branch; manual_range_patterns src/source.rs:36). cargo fmt --check clean. cargo build clean.

schema-rust-next (record-family-emission): cargo test — all 9 suites pass (75 tests), 0 failures. New suite tail:

running 8 tests
test generated_decode_rejects_an_unknown_family ... ok
test generated_descriptors_carry_the_pinned_family_identity ... ok
test generated_decode_rejects_schema_hash_drift ... ok
test generated_versioning_policy_names_the_component_store ... ok
test generated_decode_round_trips_both_families ... ok
test schema_without_families_emits_no_family_surface ... ok
test family_declarations_emit_the_version_control_surface ... ok
test schema_field_change_moves_the_emitted_family_constant ... ok
test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s

cargo clippy --all-targets: zero warnings. cargo fmt --check clean. The compile witness is real: tests/fixtures/families_generated.rs is #[path]-included into the family_emission test binary and compiles + runs against sema-engine 0.3.0 (branch versioned-family-identity, pinned 53426b14), signal-frame, and triad-runtime.

## blockers
- nota-next structural-shape gap, surfaced per v0n6's own rule: the StructuralMacroNode shape vocabulary (pascal_atom / keyword / headed-arity) cannot express a brace key/value payload, so the (Family { record .. table .. key .. }) and pre-existing (Stream { ... }) bodies still read through the hand-shaped NotaBody/SourceAtom path with a demote_to_string head check (src/source.rs SourceFamilyBody::from_block, mirroring SourceStreamBody). v0n6 says an inexpressible shape must be surfaced to the psyche rather than worked around — a brace-map structural shape in nota-next would let both stream and family bodies become derived structural macro nodes. Not fixable inside this brief's repo scope.
- Two families over the same record type are legal in Part 1 (only family names and table names are deduplicated) and Part 2 handles them (constructors and constants are family-named, variants are family-named); flagging because no Spirit record states whether record-type sharing across families is intended.
- The whole-schema content_hash includes SchemaIdentity's hand-authored version string (pre-existing, documented on the branch base); family hashes are pure structure. The generated STORE_NAME uses the full component name (e.g. example:lib) — if the psyche wants the bare crate part as the store name, that is a one-line emission change.


## Adversarial review

VERDICT: approve

## mustFix

## advisory
- Spirit v0n6 gap (agent-disclosed, precedent-bound): the family BODY is not read through a typed structural macro node. SourceFamilyBody::from_block string-matches the Family head (src/source.rs:968) and SourceFamilyFields::insert string-dispatches on record/table/key over hand-walked brace pairs (src/source.rs:1033-1048); only FamilyKey reads via derived StructuralMacroNode (src/source.rs:1038, src/schema.rs FamilyKey #[shape(keyword)]). This mirrors the stream precedent verbatim (SourceStreamFields::insert, src/source.rs:900-917) and is blocked on nota-next lacking a brace-map structural shape. It should become a tracked follow-up (streams + families together) so the gap does not silently become permanent.
- Untested enforcement path: families_verified() is called on both lowering paths (src/engine.rs:461 and src/source.rs:186), but every family test lowers through SchemaEngine::lower_source (engine path). No test drives an unresolvable family record through the typed-source path (lower_schema_source -> SourceFamilyBody/to_schema, src/engine.rs:340-357). Code-verified correct; one test would pin it.
- Imported-record family untested end to end: the deciding argument for registry-on-the-closed-sum (imported records emit as alias re-exports, E0116 forbids inherent impls) is sound, and Part 1 resolves family records against imports (schema-next src/schema.rs:309-316 family_record_resolves), but no fixture declares a family whose record is a cross-crate import. Worth a witness before a real consumer relies on it.
- Weak negative test: family_key_kind_is_a_closed_structural_choice (schema-next tests/family_declarations.rs:160-173) asserts only expect_err without matching the error variant, so any lowering failure passes. Pin the expected SchemaError kind.
- Generator panic surface: LowerToRust<RustVersionedStore> for Schema uses .expect() for closure build and content hashing (schema-rust-next src/lib.rs:869-871). Justified today by the families_verified invariant and matching crate idiom (src/lib.rs:752), but any future Schema entry point that skips verification turns this into a build-time panic rather than a typed error.
- Minor duplication: the FamilyKey match appears twice in emission — RustRecordFamily::descriptor_type (src/lib.rs:926-932) and the separate descriptor_head match inside RecordFamilyEnumTokens::to_tokens — one method returning the descriptor type + constructor head pair would name the contact point once.
- Clippy nuance, honestly disclosed: the three schema-next warnings are at pre-existing sites (verified on base 3e72902d), but this branch deepens Schema::new from 8/7 to 9/7 arguments (src/schema.rs:220). A schema-parts input struct is the eventual one-object-in fix.
- Theoretical name collision: Part 1 rejects exact duplicate family names but two distinct PascalCase names could case-fold to the same SCREAMING constant / snake_case constructor. Same exposure as the existing short_header naming; negligible but real.
- Reviewer note: the constraint items 'import path structurally unavailable to ordinary handlers' and 'outbox row in the same transaction at every choke point' do not pertain to these two branches — no handlers, transactions, or outbox exist in either diff; they appear to be carry-over from a sibling task brief. All constraints that do apply to these branches were verified and hold.

## disciplineFindings
- Methods-on-types: clean. Every new production function is a method or associated function on a data-bearing type — SourceFamilyBody/SourceFamilyFields/MetadataDefinitionProbe/NamespaceMetadataProbe (schema-next src/source.rs, src/engine.rs), TableName/FamilyKey/FamilyDeclaration/Schema::families_verified (src/schema.rs:298-316), RustVersionedStore/RustRecordFamily and the reference-carrying (non-ZST) FamilyIdentityModuleTokens/RecordFamilyEnumTokens matching the crate's RouteEnumTokens/ShortHeaderModuleTokens idiom (schema-rust-next src/lib.rs:1449,1712). Free functions only in #[cfg(test)] files.
- Naming: full English throughout (constant_identifier, constructor_identifier, versioned_store, families_verified); Rust* prefixes match the established Rust-model nouns (RustEnum, RustRelation); no ancestry repetition; generated RecordFamilyError is descriptive disambiguation inside a many-type generated module, not a namespace echo.
- Typed errors: three new structured SchemaError variants FamilyRecordNotFound/DuplicateFamilyName/DuplicateFamilyTable (schema-next src/engine.rs:188-197), all asserted by exact variant in tests; generated RecordFamilyError is a typed enum with Display + std::error::Error; zero anyhow/eyre anywhere.
- Constraint — family declarations as schema metadata on the stream precedent: holds. Lowered to Schema::families() (src/schema.rs:286-288), excluded from namespace typing via MetadataDefinitionProbe (src/engine.rs:891-918) and is_type_declaration (src/source.rs:789-791); proven by family_declarations_lower_to_semantic_schema_metadata asserting type_named("EntryFamily").is_none().
- Constraint — generation-time hash consts genuinely derived from the closure: holds. LowerToRust<RustVersionedStore> computes blake3 of Schema::family_closure(record).content_hash() while the semantic value is in hand (schema-rust-next src/lib.rs:858-880), pins it into the family_identity module (FamilyIdentityModuleTokens), and schema_field_change_moves_the_emitted_family_constant proves the constant moves with an Entry edit while ObservationFamily's stays fixed (per-family isolation).
- Constraint — closed RecordFamily sum, decoder hard-fails on unknown identity AND stale hash: holds. Generated decode matches the stored FamilyName against the closed arm set, checks identity.schema_hash() != generated before any rkyv decode, and falls through to typed UnknownFamily — never a fallback (fixture tests/fixtures/families_generated.rs:337-382); behaviorally witnessed by generated_decode_rejects_an_unknown_family and generated_decode_rejects_schema_hash_drift.
- Constraint — generated VersioningPolicy + sema-engine on the signal-frame precedent: holds. RecordFamily::versioning_policy()/STORE_NAME from the schema identity component (fixture lines 317-322); generated paths are fully-qualified sema_engine:: exactly as signal_frame:: in spirit_generated.rs; sema-engine is a dev-dependency pinned to versioned-family-identity 53426b14 (the live remote head) and schema-next to the sibling branch head 89fe33a9 — cross-repo deps via Cargo git branch names, no path patches.
- Constraint — emission gated only on declared families, target-independent: holds (src/lib.rs:329-331 is_empty gate); schema_without_families_emits_no_family_surface proves a family-free schema emits zero RecordFamily/family_identity/sema_engine references.
- No backward-compatibility shims, no opt-in framing, no compatibility language anywhere in the diffs; INTENT.md updates bracket-quote only Spirit wrjl and v0n6 with identifiers; both branches are single described commits on the correct bases (89fe33a9 on 3e72902d schema-content-identity; 9892d59d on origin/main cedb2e06) and are pushed at exactly the claimed heads (git ls-remote verified).

## testHonesty
Re-ran everything myself; every numeric claim reproduces exactly. schema-next: 15 suites all ok (13 test-bearing + empty lib unit + doc-tests), new family_declarations suite 8/8 matching the claimed tail; clippy 3 warnings at src/macros.rs:222, src/schema.rs:220, src/source.rs:36 — I verified all three sites exist unchanged on base 3e72902d, and the agent itself disclosed the 8/7-to-9/7 deepening of Schema::new; fmt and build clean. schema-rust-next: 9 suites, 75 tests (10+2+9+34+8+6+6), all pass; clippy zero warnings; fmt clean. The witnesses prove the claims rather than flatter them: the three text-shaped assertions (assert_code_contains, on the emission.rs precedent) are confined to the generator test where generated source IS the product, and every text claim is double-covered — the checked-in families_generated.rs is asserted byte-equal to fresh emission (freshness proven in-run), #[path]-included so it must compile against real sema-engine/signal-frame/triad-runtime pins, and five runtime tests drive the compiled surface with real values (decode round-trip both families, typed unknown-family rejection, typed hash-drift rejection with the exact stored/generated pair asserted, descriptor identity equality against the pinned constants, versioning-policy store name). schema_field_change_moves_the_emitted_family_constant is a genuine behavioral freshness witness including per-family isolation, not a string check. The only soft spot is family_key_kind_is_a_closed_structural_choice asserting expect_err without the variant (advisory). Nothing is asserted on source text where behavior was claimable.

