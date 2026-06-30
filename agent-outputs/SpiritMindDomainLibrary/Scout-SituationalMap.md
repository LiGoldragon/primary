# Scout Situational Map: Spirit Recursive Domains for Mind Sharing

## Task And Scope

Read-only research scout task: inspect Spirit's recursive domain system and judge whether it should become a shared domain library for Spirit and Mind.

The supplied psyche direction treated as current authority for this scout:

- Mind, not Mine, is the non-Spirit knowledge substrate for engine/system knowledge.
- First Mind implementation should be guarded and fixture-driven before real corpus import.
- Semantic judgment belongs to AI from the beginning; deterministic code handles structure, evidence gathering, typed verdict parsing/application, and storage.
- Rejected Mind knowledge is not stored; accepted admission receipts are not stored.
- Persisted source/provenance is not mandatory unless source matters as part of accepted knowledge.
- Avoid blurry nouns like `Thought` unless defended.
- Produce an implementable model, not a conceptual essay.

This scout did not edit Spirit, Mind, or signal-mind. It wrote only this output file.

## Commands And Files Consulted

Commands used:

- `orchestrate "(Observe Roles)"` from `/home/li/primary`.
- `spirit "(PublicTextSearch [Mind Spirit domain recursive knowledge substrate])"`.
- `spirit "(PublicTextSearch [Mind non-Spirit knowledge substrate semantic judgment fixture rejected receipts])"`.
- `jj status` in `/home/li/primary`, `/home/li/primary/repos/spirit`, `/git/github.com/LiGoldragon/mind`, and `/git/github.com/LiGoldragon/signal-mind`.
- `rg`, `find`, `ls`, and `sed` against Spirit, signal-spirit Cargo checkout, Mind, and signal-mind.

Important files inspected:

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/home/li/primary/repos/spirit/AGENTS.md`
- `/home/li/primary/repos/spirit/ARCHITECTURE.md`
- `/home/li/primary/repos/spirit/README.md`
- `/home/li/primary/repos/spirit/manual.md`
- `/home/li/primary/repos/spirit/Cargo.toml`
- `/home/li/primary/repos/spirit/Cargo.lock`
- `/home/li/primary/repos/spirit/build.rs`
- `/home/li/primary/repos/spirit/flake.nix`
- `/home/li/primary/repos/spirit/src/lib.rs`
- `/home/li/primary/repos/spirit/src/store/mod.rs`
- `/home/li/primary/repos/spirit/src/schema/sema.rs`
- `/home/li/primary/repos/spirit/tests/generated_signal_plane.rs`
- `/home/li/primary/repos/spirit/tests/runtime_triad.rs`
- `/home/li/primary/repos/spirit/tests/operator_271_closed_claims.rs`
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/schema/domain.schema`
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/schema/signal.schema`
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/src/lib.rs`
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/src/schema/domain.rs`
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/src/schema/signal.rs`
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/tests/generated_contract.rs`
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/tests/validation.rs`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/schema/*.schema`
- `/git/github.com/LiGoldragon/mind/src/graph.rs`
- `/git/github.com/LiGoldragon/mind/src/tables.rs`
- `/git/github.com/LiGoldragon/signal-mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
- `/git/github.com/LiGoldragon/signal-mind/src/graph.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/technical.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs`

Not checked: full test execution, live daemon behavior, remote GitHub state, and `/nix/store`. The Mind repo asked to read `/home/li/primary/lore/AGENTS.md`; that path was missing locally.

## Observed Source Facts

Spirit itself no longer owns an authored `schema/domain.schema` or `src/schema/domain.rs`. Its `flake.nix` has a check asserting those files must not exist in Spirit, and its `build.rs` imports the dependency schema from `signal-spirit`. The resolved `Cargo.lock` points `signal-spirit` to `git+https://github.com/LiGoldragon/signal-spirit.git?branch=main#5d0905a7aa8c43951253b86193d76be67a89a945`.

The executable source of truth for the recursive domain model is the resolved signal-spirit checkout:

- `schema/domain.schema` declares `Domain`, `Technology`, `Software`, leaf enums, `DomainScope (ScopeOf Domain)`, `DomainScopes (Vector DomainScope)`, `ScopeSet (Vector DomainScope)`, and one symmetric equivalence relation: `(Equivalence [(Information Database) (Technology Software Data)])`.
- `schema/signal.schema` imports `Domain`, `DomainScope`, and `DomainScopes` from the domain schema; declares `Domains (Vector Domain)`; declares `DomainMatch [Any (Partial) (Full)]`; declares `Entry { Domains Kind Description Certainty Importance Privacy Referents }`; declares `RecordSelection { DomainMatch SelectedKind }`; and declares `Query { DomainMatch KeywordMatch TextMatch ReferentSelection SelectedKind PrivacySelection CertaintySelection ImportanceSelection }`.
- `src/schema/domain.rs` is generated from that schema and contains the recursive Rust types. `Domain` is a closed enum with broad areas such as `Health`, `Information`, and `Technology`. `Technology` contains `Hardware(Option<HardwareLeaf>)` and `Software(Software)`. `Software` contains terminal-capable variants such as `Data(Option<DataLeaf>)`, `Quality(Option<QualityLeaf>)`, and `Engineering(Option<EngineeringLeaf>)`.
- `src/schema/domain.rs` generates a parallel `DomainScope` tree with `All` scope values at nested levels, for example `TechnologyScope::All` and `SoftwareScope::All`.
- `src/schema/domain.rs` implements `DomainScope::contains_scope`, `DomainScope::contains_domain`, `DomainScope::expand`, and `DomainScope::equivalence_relations`. `expand` adds symmetric equivalent scopes from the authored equivalence set.
- `src/lib.rs` adds hand-written contract helpers: `Query::matches`, `DomainMatch::validate`, `DomainMatch::matches`, `Domains::from_strings`, `DomainScopes::from_strings`, `DomainScopes::from_domains`, `ScopeSet::matches_domain`, `ScopeSet::matches_any_domain`, and rank/match helpers for privacy, certainty, and importance.

Spirit stores domains as part of full Spirit entries:

- `src/schema/sema.rs` defines `StoredRecord { record_identifier: RecordIdentifier, entry: Entry }`.
- `src/store/mod.rs` stores records in a `sema-engine` table named `records`, with a `StoredRecord` payload containing the full `Entry`.
- `Store::record_entry` persists an `Entry`; `Store::observe` scans records, canonicalizes query referents, filters with `record.entry.matches(&query)`, then sorts by certainty and importance.
- `Store::count` delegates to `observe(query)?.len()`.
- `Store::retire` archives then retracts by record identifier.
- The store imports and uses `DomainMatch`, `DomainScope`, and `DomainScopes` mostly for guardian-context queries and record filtering. Query matching itself is duplicated locally in extension traits near the bottom of `src/store/mod.rs`, even though signal-spirit also provides `Query::matches`.

Spirit record usage:

- `README.md` says entries carry a vector of domains and queries use `DomainMatch` values. `Partial` matches any requested domain; `Full` requires every requested domain.
- `ARCHITECTURE.md` says the unit of intent is the domain, the domain tree is variable-depth, domain nesting is structural subsumption, and cross-tree relations are symmetric equivalence only.
- `ARCHITECTURE.md` also says domain names must be self-explanatory and that unclear names should be renamed rather than annotated.
- Guardian prompt docs enforce a Spirit-specific classification rule: named particulars such as `spirit`, `rkyv`, or `DeepSeek` are referents, not domains; domains are universal subjects.
- `src/nexus.rs` uses `Domain::Information(Information::Documentation)` as a fallback domain when converting free `State` input into a concrete `Entry`.

Spirit test coverage:

- `tests/generated_signal_plane.rs` proves `DomainScope` parses as recursive enum text, rejects malformed `(Technology Software)`, converts a leaf `Domain` into a matching `DomainScope`, and verifies containing scopes match nested leaves.
- `tests/runtime_triad.rs` defines typed domain-scope helpers and proves equivalent-domain query behavior: a `Technology/Software/Data` scope observes an `Information/Database` record through the equivalence expansion, and expansion does not chain into unrelated hardware.
- `tests/operator_271_closed_claims.rs` checks the signal-spirit domain schema contains the Technology/Software tree, selected leaves, and the `Information Database` / `Technology Software Data` equivalence.
- signal-spirit `tests/generated_contract.rs` proves terminal domain tags such as `(Technology (Software Data))`, curated leaf tags such as `(Technology (Software (Data SchemaEvolution)))`, pure terminal tags such as `(Technology (Software Theory))`, deleted leaves failing to parse, and terminal-value domains converting to scope `All`.
- signal-spirit `tests/validation.rs` proves active entries require non-empty referents, while zero-certainty legacy removal candidates may lack referents.

Mind and signal-mind state:

- `/git/github.com/LiGoldragon/mind` and `/git/github.com/LiGoldragon/signal-mind` are active repos and both working copies were clean.
- Mind currently has typed `Thought`/`Relation` graph records and typed technical graph records. The term `domain` in Mind docs and signal-mind code often means graph domain/range validation for relation endpoints, not Spirit's subject taxonomy.
- signal-mind has closed `ThoughtKind` values (`Observation`, `Memory`, `Belief`, `Goal`, `Claim`, `Decision`, `Reference`) and `RelationKind` endpoint validators. It also has technical node/relation kinds such as `Component`, `Repository`, `Contract`, `StorageResource`, `SchemaFamily`, `Table`, and `TechnicalRelationKind::StorageDependency`.
- Mind architecture says typed graph records are immutable; correction is a new record plus a relation such as `Supersedes`.
- Mind architecture says technical facts, provenance chains, dependency closures, and typed relation endpoint validation are already first-class. It does not currently have Spirit-like subject taxonomy fields in the inspected schema.

Spirit intent query evidence:

- `spirit PublicTextSearch [Mind Spirit domain recursive knowledge substrate]` returned `qjrf`, whose useful conclusion here is that Spirit records are intent, not information or belief. This reinforces that Mind should not inherit Spirit's intent-record semantics.
- `spirit PublicTextSearch [Mind non-Spirit knowledge substrate semantic judgment fixture rejected receipts]` returned `w312`, whose useful conclusion is that deterministic correct work belongs in code/schema machinery, while agents do semantic judgment. This supports keeping domain parsing/matching deterministic and keeping knowledge admission judgment outside the shared domain crate.

## Current Spirit Domain Model Shape

Spirit's domain model has four separable layers:

1. Subject taxonomy: `Domain` and nested payload enums form a closed, variable-depth, typed tree. It is not free text.
2. Scope projection: `DomainScope` is generated from `ScopeOf Domain`; every interior level has an `All` scope that subsumes descendants.
3. Equivalence expansion: `DomainScope::expand` adds symmetric cross-tree equivalents from the authored `Equivalence` list. The current only observed equivalence is `Information/Database` with `Technology/Software/Data`.
4. Spirit query wrapper: `Domains`, `DomainScopes`, `DomainMatch`, `RecordSelection`, `Query`, `Entry`, and validation combine domain matching with Spirit-specific fields: kind, description, referents, privacy, certainty, importance, removal-candidate behavior, guardian rejection reasons, and intent operations.

The reusable core is layers 1 through 3. Layer 4 is mostly Spirit-specific.

## Generic Enough To Share

Recommended to share:

- `Domain`: the closed recursive subject taxonomy.
- Nested enum payloads such as `Information`, `Technology`, `Software`, `DataLeaf`, `EngineeringLeaf`, and sibling areas.
- `DomainScope`: typed prefix scopes generated from `Domain`.
- `DomainScopes` / `ScopeSet`, or equivalent small wrappers.
- `DomainScope::contains_scope`, `DomainScope::contains_domain`, `Domain::matches_scope`.
- `DomainScope::expand` and authored symmetric equivalence relations.
- NOTA text projection behind a `nota-text` feature and rkyv archive support by default, matching the existing contract pattern.
- Schema source constants for audit/help/test surfaces.
- Focused fixture helpers that build known domains and scopes, but not the fuzzy `from_strings` compatibility mapper unless explicitly kept under a test or legacy feature.

This is generic because Mind technical knowledge also needs a stable, typed subject axis for broad routing and retrieval. The taxonomy is not inherently about intent. `Technology/Software/Data`, `Information/Database`, `Technology/Software/Engineering`, `Safety/Cybersecurity`, and similar branches are useful for non-Spirit technical knowledge.

## Spirit-Specific And Should Not Leak Into Mind

Do not move these into a shared domain crate:

- `Entry`, `RecordRequest`, `Proposal`, `Clarification`, `Supersession`, `Retirement`, `RecordChange`, and related Spirit intent-operation records.
- `Kind [Decision Principle Correction Clarification Constraint]`.
- `Certainty`, `Importance`, and `Privacy` as Spirit admission/query axes. Mind may need confidence or visibility later, but the current psyche direction says semantic verdicts are AI-owned and rejected knowledge is not stored; importing Spirit's certainty/removal-candidate semantics would be wrong.
- `DomainMatch` if it remains coupled to Spirit's `Domains`, validation errors, and `Query` defaults. A generic `DomainSelector` can exist, but Spirit's `DomainMatch` currently lives inside the Spirit query model.
- `RecordSelection`, `Query`, `PublicRecords`, `PrivateRecords`, `PublicTextSearch`, `ReferentSelection`, `KeywordMatch`, and text/keyword matching.
- `Referent` and referent-registration/alias machinery. Mind's technical nodes already use stable typed keys and relation endpoints; importing Spirit's referent model would blur identity systems.
- Guardian prompts and rejection reasons such as `UnclearDomain`, `NonIntent`, `Matter`, or testimony/warrant rules. Those are Spirit admission policy for psyche intent.
- Record identifiers, archive/removal-candidate collection, accepted admission receipts, and daemon-stamped marker behavior.
- The `State` fallback to `Information/Documentation`.

The phrase "domain/range" in Mind/signal-mind relation validators must not be conflated with Spirit subject domains. If a shared crate is introduced, call the shared concept `KnowledgeDomain` or `SubjectDomain` at Mind call sites if needed to avoid collision with graph relation domain/range language.

## Minimal Shared Crate/API Proposal

Recommendation: extract a small `knowledge-domain` or `subject-domain` contract crate, not a broad Spirit/Mind knowledge crate.

Crate ownership:

- New crate owns `schema/domain.schema` copied from signal-spirit, renamed only if necessary.
- `signal-spirit` depends on the new crate and imports `Domain`, `DomainScope`, `DomainScopes`, and `ScopeSet` from it.
- Mind or signal-mind depends on the new crate only for subject classification fields in new guarded fixture-driven admission records.

Default features:

- Default: rkyv binary archive types only.
- `nota-text`: NOTA parse/display/help projection.
- No daemon runtime, no sema-engine, no Spirit guardian, no Mind actor dependency.

Minimal Rust surface:

```rust
pub enum Domain { ... }
pub enum DomainScope { ... }
pub struct DomainScopes(Vec<DomainScope>);
pub struct ScopeSet(Vec<DomainScope>);

impl From<Domain> for DomainScope;

impl DomainScope {
    pub fn contains_scope(&self, scope: &DomainScope) -> bool;
    pub fn contains_domain(&self, domain: &Domain) -> bool;
    pub fn expand(&self) -> ScopeSet;
    pub fn equivalence_relations() -> Vec<Vec<DomainScope>>;
}

impl Domain {
    pub fn matches_scope(&self, scope: &DomainScope) -> bool;
}

impl DomainScopes {
    pub fn new(scopes: Vec<DomainScope>) -> Self;
    pub fn iter(&self) -> impl Iterator<Item = &DomainScope>;
    pub fn matches_any_domain(&self, domains: &[Domain]) -> bool;
}

pub enum DomainSelector {
    Any,
    AnyOf(DomainScopes),
    AllOf(DomainScopes),
}
```

`DomainSelector` is optional for the first slice. If added, keep it independent of Spirit `Query`; no privacy/certainty/kind/referent defaults.

Minimal Mind admission shape for the first guarded fixture slice:

```text
KnowledgeAdmissionRequest {
  candidate_subjects: DomainScopes,
  candidate_text: Text,
  evidence_bundle: EvidenceBundle,
  adjudication_prompt_context: PromptContext
}

KnowledgeAdmissionVerdict [
  (Accept AcceptedKnowledge)
  (Reject KnowledgeRejection)
]

AcceptedKnowledge {
  subjects: DomainScopes
  body: TypedKnowledgeBody
}
```

No accepted admission receipt storage. No rejected record storage. Source/provenance only belongs inside `AcceptedKnowledge` when the AI-adjudicated knowledge itself needs it.

## Risks

- Stale docs: signal-spirit `ARCHITECTURE.md` and `INTENT.md` in the Cargo checkout still contain older topic/user-creatable-topic language, while current schema and Spirit docs use recursive domains. Extraction should trust `schema/domain.schema`, `schema/signal.schema`, generated Rust, and Spirit's current `ARCHITECTURE.md`/`README.md` over stale signal-spirit prose.
- Fuzzy compatibility helper: `Domains::from_strings` maps labels like `schema`, `nota`, and `programming` into domains through string heuristics. That is useful for legacy tests and maybe old text inputs, but it is not a clean shared API. Mind should not get a fuzzy subject classifier in deterministic code; AI should choose typed domains and deterministic code should parse/validate them.
- Naming collision: Mind already uses "domain/range" for graph relation endpoint validation. Importing a type literally named `Domain` everywhere may confuse future workers. Use module qualification or a renamed public alias in Mind.
- Coupled query semantics: Spirit currently has `Query::matches` in signal-spirit and duplicate local matching extensions in `src/store/mod.rs`. Before sharing, decide whether selector matching belongs in the shared domain crate or remains per-consumer.
- Versioning/storage compatibility: Spirit schema version 10 coarsened Technology/Software domains and production migration rewrites older domains into current domains plus keywords. Extracting the domain crate changes dependency and schema-import shape; Spirit needs migration/freshness checks before landing.
- Mind noun risk: current Mind uses `Thought`, which the user specifically flagged as a blurry noun unless defended. A domain library does not fix that. Do not design the shared domain API around Mind's current `Thought` model.

## First Implementation Slice

Recommended first slice:

1. Create `subject-domain` as a pure contract/declaration crate from signal-spirit's current `schema/domain.schema`.
2. Move only domain schema, generated domain Rust, schema source constant, and tests for parse/display/scope/equivalence. Do not move Spirit signal schema, entry/query types, guardian rules, referents, or magnitude axes.
3. Update `signal-spirit/schema/signal.schema` imports from `signal-spirit:domain:*` to `subject-domain:domain:*`.
4. Keep `signal-spirit` type exports stable by re-exporting the imported domain types so Spirit call sites can remain mostly unchanged.
5. Run/port existing witnesses: signal-spirit generated-contract domain tests, Spirit `generated_signal_plane` recursive scope test, Spirit `runtime_triad` equivalence query test, and Spirit `operator_271_closed_claims` schema witness adapted to the new crate.
6. Add a small Mind fixture-only admission prototype that accepts typed `DomainScope`/`DomainScopes` from the shared crate, invokes an AI verdict fixture, persists only accepted typed knowledge, and returns typed rejection without storage.
7. Do not import a real corpus until the fixture path proves accepted/rejected behavior and storage boundaries.

Recommended first Mind usage:

- Add domain subjects to new knowledge/technical admission fixtures, not to every existing `Thought`.
- Treat the shared domain as broad retrieval/routing metadata, not as proof, provenance, certainty, source, or admission receipt.
- Keep semantic classification in the AI verdict fixture: deterministic code validates that the returned domain values parse and that accepted knowledge has the required typed shape.

## Blockers And Unknowns

- `/home/li/primary/lore/AGENTS.md` was referenced by Mind's `AGENTS.md` but missing locally.
- No tests were run; all conclusions are from source inspection.
- I did not inspect remote repositories or newer unpublished revisions. The Spirit source currently resolves `signal-spirit` at `5d0905a7aa8c43951253b86193d76be67a89a945`.
- It is not yet known whether the domain crate should be named `knowledge-domain`, `subject-domain`, or another local convention. `subject-domain` is the clearest scout recommendation because it avoids promising a full knowledge model.
