# Mind Practical Knowledge Model Implementation Brief

## Task And Scope

This synthesis turns the two scout reports into an implementable first-slice handoff for Mind's accepted-knowledge substrate. It does not edit source repositories, create beads, commit, audit, or push.

Inputs consulted:

- `agent-outputs/SpiritMindDomainLibrary/Scout-SituationalMap.md`
- `agent-outputs/MindKnowledgeModel/Scout-SituationalMap.md`

Read-only public Spirit queries consulted:

- `PublicTextSearch [Mind knowledge substrate semantic judgment rejected receipts]` returned `w312`, supporting that deterministic routing, lookup, classification, projection, and address resolution belong in code/schema machinery while agents do cognitive judgment.
- `PublicTextSearch [Mind Spirit domain recursive shared library]` returned `qjrf`, supporting that Spirit holds psyche intent, not general information or belief. Mind must not inherit Spirit record semantics.
- `PublicTextSearch [deterministic code agents semantic judgment structure storage verdict]` returned `w312` plus broader agent-quality records; only `w312` and `qjrf` are load-bearing here.

Controlling psyche constraints preserved:

- Mind, not Mine, is the non-Spirit knowledge substrate for engine/system knowledge.
- First implementation is guarded and fixture-driven before real corpus import.
- Semantic judgment belongs to AI from the beginning.
- Deterministic code handles structure, typed inputs/outputs, routing, storage, and verdict application, not semantic judgment via regex, keywords, or handcrafted contradiction logic.
- Rejected Mind knowledge is not stored. The requesting agent receives the typed rejection and owns retry or abandonment.
- Accepted admission receipts are not stored.
- Persisted source/provenance is not mandatory; if source matters, it is part of accepted knowledge itself.
- Avoid blurry nouns like `Thought` unless defended.
- Spirit's recursive domain system is important and may become a shared library, but broad prior-report scouting is intentionally skipped.

## Architecture Proposal

Mind should model accepted knowledge as a typed attributed graph admitted by a transient AI judge. The durable root noun is `AcceptedKnowledge`, not `Thought`.

Accepted knowledge has four durable record families in v1:

- `KnowledgeEntity`: an accepted thing, component, repository, contract, schema, table, source object, domain concept, or other identified object.
- `KnowledgeStatement`: an accepted declarative claim that has not yet been normalized into only entities and relations. This is a narrow escape hatch, not the default permanent shape.
- `KnowledgeRelation`: an accepted typed edge between accepted records.
- `KnowledgeDomain`: an accepted classification concept used for routing and retrieval.

Optional source/provenance is not process metadata. If source matters, it is represented as normal accepted knowledge:

- `KnowledgeSource`: an entity-like accepted record, or a source-specific entity kind, plus explicit relations such as `References`, `SupportedBy`, or `DefinedBy`.

The admission path is:

1. `SubmitKnowledge(KnowledgeSubmission)` arrives with typed candidate data.
2. Deterministic preflight validates structure: enum variants, newtypes, key syntax, payload size, existing endpoints for relation candidates, domain/range table compatibility where endpoints are already known, store readiness, and privacy/scope gates that are mechanically knowable.
3. Code builds a typed `KnowledgeJudgePacket` containing candidate, relevant accepted neighbors, allowed relation/domain rules, and fixture policy.
4. AI returns `KnowledgeJudgeVerdict`.
5. Deterministic code applies the verdict:
   - `Accept(AcceptedKnowledgeDraft)` persists only accepted records and relations named in the draft.
   - `Reject(KnowledgeRejection)` returns the rejection and persists nothing.
   - persistence failure after acceptance returns a typed persistence rejection and must not create an admission receipt.

The query path is deterministic:

- `QueryKnowledge(KnowledgeQuery)` reads only accepted store state.
- Current-view projection hides or demotes superseded accepted records without deleting them.
- Closure such as broader/narrower domain expansion is derived at query time or through an explicit derived-view store later; v1 stores only direct asserted links.
- Query code may filter by record kind, identifier, stable key, domain selector, relation kind, endpoint, and current/historical view. It must not infer semantic contradiction, truth, duplicate, or support from regex/keyword rules.

## AI Judge Boundary

AI owns semantic judgment:

- whether a candidate is knowledge rather than a task, log, receipt, instruction, vague prose, private material, or non-knowledge;
- whether it is meaningful and true enough for Mind;
- semantic classification when not mechanically derivable;
- semantic duplicate, contradiction, supersession, support, and normalization decisions;
- whether a source must be part of the accepted knowledge.

Deterministic code owns mechanism:

- typed request/reply contracts;
- schema-derived decoding and validation;
- relation domain/range tables;
- existing endpoint lookup;
- route selection and store family selection;
- ID and timestamp minting;
- verdict application;
- current-view projection;
- typed rejection delivery.

The first implementation must consume a judge trait or actor boundary with fixture-backed verdicts. This keeps Rust tests deterministic while preserving the real AI-shaped boundary from the beginning.

## Shared Domain Library Recommendation

Recommendation: defer extraction; use Spirit's existing recursive domain shape as inspiration only for Mind v1.

Reasoning:

- Spirit's reusable core is valuable: closed recursive subject taxonomy, generated scope projection, `All` scopes, containment, and symmetric equivalence expansion.
- Extracting it now would require cross-repo changes in `signal-spirit`, Spirit, and Mind before Mind's basic admission behavior is proven.
- Mind's first risk is not taxonomy richness; it is admission/storage correctness: accepted-only persistence, no receipt storage, typed rejection, fixture AI boundary, and query behavior.
- Mind already has naming collision risk around "domain/range" relation validation. Importing a generic `Domain` type immediately would blur the first slice.

First implementation impact:

- Do not make a shared `subject-domain` crate a dependency of Mind v1.
- Use Mind-local `KnowledgeDomainKey` and `KnowledgeDomain` fixtures.
- Preserve the shape that would map cleanly later: direct domain records, direct broader/narrower links, derived closure, and a future `SubjectDomain` adapter.
- File a follow-on extraction bead only after the fixture slice passes and a worker can validate Spirit compatibility separately.

Conservative follow-on recommendation:

- Extract a small `subject-domain` contract crate later, not a broad knowledge crate.
- Move only Spirit's domain schema, generated domain/scope Rust, containment, expansion, equivalence tests, and NOTA projection.
- Do not move Spirit entries, referents, certainty, importance, privacy, guardian prompts, accepted receipts, or intent operations.

## V1 Contract Nouns

Requests and replies:

```text
MindRequest
  | SubmitKnowledge(KnowledgeSubmission)
  | QueryKnowledge(KnowledgeQuery)

MindReply
  | KnowledgeAccepted(AcceptedKnowledgeView)
  | KnowledgeRejected(KnowledgeRejection)
  | KnowledgeList(KnowledgeList)
```

Admission records:

```text
KnowledgeSubmission {
  candidate: KnowledgeCandidate,
  fixture_policy: FixturePolicy,
  requester_context: RequesterContext
}

KnowledgeCandidate
  | Entity(KnowledgeEntityCandidate)
  | Statement(KnowledgeStatementCandidate)
  | Relation(KnowledgeRelationCandidate)
  | Domain(KnowledgeDomainCandidate)
  | Source(KnowledgeSourceCandidate)

KnowledgeJudgeVerdict
  | Accept(AcceptedKnowledgeDraft)
  | Reject(KnowledgeRejection)
```

Stored accepted records:

```text
AcceptedKnowledge
  | Entity(KnowledgeEntity)
  | Statement(KnowledgeStatement)
  | Relation(KnowledgeRelation)
  | Domain(KnowledgeDomain)
  | Source(KnowledgeSource)
```

Identifier and key nouns:

- `KnowledgeIdentifier`: daemon-minted stable identifier for accepted records.
- `KnowledgeStableKey`: optional caller-visible key for things that already have a stable external identity, such as `component:mind` or `contract:signal-mind:ordinary`.
- `KnowledgeDomainKey`: canonical classification key such as `domain:component` or `domain:contract`.

Rejection nouns:

```text
KnowledgeRejection {
  reason: KnowledgeRejectionReason,
  candidate_summary: CandidateSummary,
  retry_hint: Option<RetryHint>
}

KnowledgeRejectionReason
  | NotKnowledge
  | PrivateOrUnauthorized
  | MeaningUnclear
  | FalseOrUnsupported
  | SemanticDuplicate(KnowledgeIdentifier)
  | ConflictsAcceptedKnowledge(Vec<KnowledgeIdentifier>)
  | WrongDomain(KnowledgeDomainKey)
  | NeedsMoreSpecificShape(Vec<ExpectedKnowledgeShape>)
  | SourceRequiredByCandidate
  | StructuralPreflightFailed(StructuralRejection)
  | PersistenceRejected
```

Guardrail: code may produce `StructuralPreflightFailed` and `PersistenceRejected`. AI produces semantic rejection variants. Code applies semantic verdicts but does not synthesize them through keyword logic.

## V1 Relation Kinds

Start with a closed enum and a deterministic domain/range table:

- `ClassifiedAs`: source is any accepted knowledge record; target is `KnowledgeDomain`.
- `BroaderThan`: source and target are `KnowledgeDomain`; direct hierarchy assertion only.
- `NarrowerThan`: source and target are `KnowledgeDomain`; direct hierarchy assertion only.
- `RelatedTo`: source and target are `KnowledgeDomain` or compatible concept records; non-hierarchical association.
- `References`: source is any accepted record; target is `KnowledgeSource` or `KnowledgeEntity`.
- `SupportedBy`: source is `KnowledgeStatement`, `KnowledgeRelation`, or another accepted record whose support is being asserted; target is `KnowledgeSource` or `KnowledgeStatement`.
- `Contradicts`: source and target are accepted records; semantic conflict asserted by AI, never detected by code heuristics.
- `Supersedes`: source and target are accepted records; current query prefers the source.
- `Defines`: source is a repository, crate, file, schema, or source record; target is a contract, type, table, domain, or other definitional object.
- `Implements`: source is a component or code artifact; target is a contract, behavior, schema, or interface.
- `DependsOn`: source and target are accepted records; use only until fixtures justify more precise technical relations.

Use more precise technical relations when fixture evidence requires them, for example `BuildDependsOn`, `RuntimeDependsOn`, `WireDependsOn`, or `StorageDependsOn`. Do not add relation kinds without a domain/range table and a passing fixture.

## Exact First Fixture-Driven Vertical Slice

Implement one guarded route family: `SubmitKnowledge` and `QueryKnowledge`. Do not route this through `SubmitThought`.

Fixture judge behavior:

- Use a `KnowledgeJudge` trait or actor port.
- The test implementation returns typed verdicts from fixtures.
- A later AI-backed implementation may use the same packet/verdict contract.

Store effects:

- Accepted entity/domain/statement/source drafts create accepted records.
- Accepted relation drafts create a relation only after endpoint validation.
- Semantic rejections create no rows in any accepted family.
- Structural preflight rejections create no rows and do not call the AI judge.
- Accepted replies and admission receipts are not stored.
- Source/provenance rows are absent unless the accepted draft explicitly includes `KnowledgeSource` or source relations.

Initial fixture sequence:

1. Submit domain `domain:component`; verdict accepts `KnowledgeDomain`; store has one domain.
2. Submit domain `domain:contract`; verdict accepts `KnowledgeDomain`; store has two domains.
3. Submit entity `component:mind` classified as `domain:component`; verdict accepts entity plus `ClassifiedAs`; store has entity and relation.
4. Submit entity `contract:signal-mind:ordinary` classified as `domain:contract`; verdict accepts entity plus `ClassifiedAs`; store has second entity and relation.
5. Submit entity `repo:signal-mind`; verdict accepts entity. Then submit `Defines(repo:signal-mind, contract:signal-mind:ordinary)`; store has the relation.
6. Submit syntactically valid non-knowledge text; fixture verdict rejects `NotKnowledge`; all store family counts remain unchanged.
7. Submit relation with a missing endpoint; preflight rejects `StructuralPreflightFailed`; judge is not called and store counts remain unchanged.
8. Submit a source-backed architecture statement where source is part of the knowledge; verdict accepts `KnowledgeStatement`, `KnowledgeSource`, and `SupportedBy`; store contains source only because it was in the accepted draft.
9. Submit a newer statement that supersedes the older statement; verdict accepts statement plus `Supersedes`; current query returns the newer statement as current and the older statement only when historical view is requested.
10. Submit a candidate that contradicts accepted knowledge; fixture verdict rejects `ConflictsAcceptedKnowledge` and stores nothing. A separate positive fixture may accept an explicit `Contradicts` relation when the contradiction itself is the knowledge being recorded.

Queries to implement:

```text
KnowledgeQuery
  | GetByIdentifier(KnowledgeIdentifier)
  | GetByStableKey(KnowledgeStableKey)
  | ListByKind(KnowledgeRecordKind, CurrentView)
  | ListByDomain(KnowledgeDomainSelector, CurrentView)
  | ListRelations(RelationSelector, CurrentView)
```

Minimal selectors:

- `CurrentView`: `CurrentOnly` or `IncludeSuperseded`.
- `KnowledgeDomainSelector`: `Any`, `Direct(KnowledgeDomainKey)`, `WithDescendants(KnowledgeDomainKey)`.
- `RelationSelector`: by relation kind, source identifier, target identifier, or any combination that is structurally typed.

Tests must prove:

- accepted records are queryable by identifier and stable key;
- domain classification query returns `component:mind` for `domain:component`;
- relation query returns `Defines(repo:signal-mind, contract:signal-mind:ordinary)`;
- rejected semantic candidates store nothing;
- accepted admission replies are not persisted as records;
- source/provenance is absent unless accepted as knowledge;
- missing endpoint rejection is preflight-only and does not call the judge;
- current query hides or demotes superseded records while historical query can see them;
- no test relies on keyword/regex contradiction detection.

## Domain Dependency Graph

Implementation order:

1. Contract nouns and schema block every worker that needs typed request/reply records.
2. Store families and repository methods depend on contract nouns.
3. Deterministic preflight depends on contract nouns and relation domain/range tables.
4. Fixture judge port depends on contract nouns and judge packet/verdict records.
5. Admission application depends on store families, preflight, and fixture judge port.
6. Query API depends on accepted store records and current-view projection.
7. Fixture tests depend on admission application and query API.
8. AI-backed prompt/context integration depends on fixture tests proving the typed boundary.
9. Real corpus import depends on fixture tests and AI-backed integration; it is explicitly blocked until then.
10. Shared domain-library extraction depends on v1 fixture evidence or a separate Spirit compatibility effort; it must not block the first Mind slice.

No obvious dependency cycle: validation and fixture tests precede audit; AI-backed integration and corpus import are downstream of the fixture slice.

## Worker Handoff Plan

Bead-style implementation units to file when implementation begins:

1. `Define Mind Knowledge Contract V1`
   - Owner: signal contract worker.
   - Blocks: all other v1 work.
   - Source context: `/git/github.com/LiGoldragon/signal-mind/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`, `/git/github.com/LiGoldragon/signal-mind/src/graph.rs`, `/git/github.com/LiGoldragon/signal-mind/src/technical.rs`, and this report.
   - Completion claim: `SubmitKnowledge`, `QueryKnowledge`, accepted record nouns, verdict nouns, rejection nouns, relation kinds, selectors, and domain/range validation are represented in the contract surface.
   - Evidence: schema/contract diff, generated Rust or equivalent contract build output, round-trip tests, and domain/range validation tests.
   - Boundary: do not add AI prompt text, store persistence, corpus import, or shared domain extraction.

2. `Add Mind Accepted Knowledge Store`
   - Owner: Mind daemon/store worker.
   - Depends on: `Define Mind Knowledge Contract V1`.
   - Source context: `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`, `/git/github.com/LiGoldragon/mind/schema/mind.concept.schema`, current store/table modules in Mind, and this report.
   - Completion claim: Mind can persist accepted entities, statements, relations, domains, and sources; relation writes enforce endpoint existence and domain/range rules.
   - Evidence: store unit tests or integration tests showing writes, duplicate/key behavior, relation endpoint rejection, and no receipt family.
   - Boundary: do not implement semantic judgment or corpus import.

3. `Implement Fixture Knowledge Judge Port`
   - Owner: Mind admission worker.
   - Depends on: `Define Mind Knowledge Contract V1`.
   - Source context: Mind actor/request handling files, signal-mind contract files, this report.
   - Completion claim: admission flow calls a typed judge boundary; test fixtures can return deterministic accept/reject verdicts; preflight failures bypass the judge.
   - Evidence: tests with a counting fixture judge proving semantic fixtures call the judge and structural failures do not.
   - Boundary: do not implement production AI prompts beyond the typed port shape.

4. `Apply Knowledge Verdicts`
   - Owner: Mind admission/store integration worker.
   - Depends on: `Add Mind Accepted Knowledge Store`, `Implement Fixture Knowledge Judge Port`.
   - Source context: Mind request router, store actor, contract types, this report.
   - Completion claim: accept verdicts persist only accepted drafts; reject verdicts persist nothing; persistence failures are typed rejections with no partial receipt.
   - Evidence: fixture tests for the ten-step vertical slice store effects.
   - Boundary: do not add corpus import or hidden provenance.

5. `Implement Knowledge Query Views`
   - Owner: Mind query worker.
   - Depends on: `Add Mind Accepted Knowledge Store`.
   - Source context: existing Mind query paths, relation query helpers, this report.
   - Completion claim: queries by identifier, stable key, kind, domain, relation, and current/historical view work against accepted records.
   - Evidence: query tests covering classification, `Defines`, `Supersedes`, and absence of rejected records.
   - Boundary: no Datalog/rule engine; closure is minimal and deterministic.

6. `Validate First Slice End To End`
   - Owner: validation worker.
   - Depends on: `Apply Knowledge Verdicts`, `Implement Knowledge Query Views`.
   - Source context: all changed contract and Mind files plus this report.
   - Completion claim: fixture-driven vertical slice passes from request through verdict application to query.
   - Evidence: exact test command output, list of passing fixture cases, and any disabled real-corpus gate.
   - Boundary: validation only; no broad refactor.

7. `Review Mind Knowledge Slice`
   - Owner: distinct Mind auditor.
   - Depends on: `Validate First Slice End To End`.
   - Source context: implementation diffs, tests, validation output, and this report.
   - Completion claim: audit reports defects, missing tests, and design risks against the psyche constraints.
   - Evidence: review file or chat review with file/line findings; distinguish defects from provisional guideline observations.
   - Boundary: auditor does not implement fixes.

Optional follow-on:

8. `Scout Subject Domain Extraction After V1`
   - Owner: Spirit/Mind domain scout or contract worker.
   - Depends on: `Validate First Slice End To End`.
   - Source context: `/home/li/primary/repos/spirit`, resolved `signal-spirit` checkout, Mind v1 domain fixtures, and the domain scout report.
   - Completion claim: concrete extraction plan for a `subject-domain` crate with compatibility impact on Spirit and Mind.
   - Evidence: dependency graph, migration risk list, test witnesses to preserve.
   - Boundary: no extraction until approved.

## Non-Goals And Guardrails

Non-goals for v1:

- No source repository edits as part of this synthesis.
- No `Thought` as the v1 accepted-knowledge root noun.
- No real corpus import.
- No rejected-record archive.
- No accepted admission receipt store.
- No mandatory provenance/source metadata.
- No Spirit intent semantics, referents, certainty, importance, privacy, guardian prompts, or record-operation model in Mind.
- No Datalog/rule engine, OWL/RDF import/export, vector identity, frame/default machinery, or upper ontology.
- No deterministic semantic duplicate, contradiction, or truth detector via regex, keywords, or handcrafted logic.
- No shared domain crate extraction in the first Mind implementation slice.

Guardrails:

- New relation kinds require a fixture and domain/range table.
- New domain keys require fixture warrant or accepted source knowledge.
- `KnowledgeStatement` must remain constrained by kind, domain, and about-list where possible; repeated statement shapes should drive normalization into entities and relations.
- AI-backed e2e tests must be separate from deterministic fixture tests.
- Current accepted view may hide superseded records, but old accepted records are not the same as newly rejected candidates. Newly rejected candidates are never stored.
- Private material remains closed unless explicitly authorized through the visible chat surface.

## Remaining Psyche Decisions

No decision is required to begin the first fixture-driven Mind slice if the conservative recommendations above are accepted.

Decisions needed before expanding beyond the slice:

- Whether Mind should later keep superseded accepted records indefinitely or add a retirement/archival policy distinct from rejection.
- Whether `KnowledgeSource` should be a separate accepted record variant or an `EntityKind::Source`; the first slice can choose the simpler implementation that best fits the existing contract style.
- Whether to approve a later `subject-domain` extraction effort after Mind v1 fixtures prove the admission/storage boundary.

## Audit Recommendation

Use a distinct Mind auditor after validation, not the implementation worker. Give the auditor:

- this report;
- the implementation diff;
- generated contract/schema artifacts;
- fixture judge tests;
- store/query tests;
- exact validation command output.

The auditor should review defects against the hard constraints first: rejected knowledge not stored, receipts not stored, AI semantic boundary preserved, deterministic relation validation only, no real corpus import, and no Spirit intent semantics imported. Any broader naming or ontology suggestions should be labeled provisional guidance, not defects, unless they violate the accepted constraints.
