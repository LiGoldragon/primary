# Mind Queryable Knowledge Architecture And Implementation Handoff

## Task And Scope

Produce the first architecture and implementation handoff for Mind's queryable architecture/report knowledge slice. This is a synthesis report only. No source repositories were edited, no tests were run, and no new broad source inspection was performed.

Primary inputs:

- `agent-outputs/MindComponentScout/Scout-SituationalMap.md`
- `agent-outputs/MindOrchestrateChangeClosure/Scout-SituationalMap.md`
- `agent-outputs/MindJudgmentLoopPatterns/Scout-SituationalMap.md`

Narrow public Spirit read:

- `PublicTextSearch [Mind Spirit knowledge architecture reports]` observed `qjrf`, `10pz`, `t5qr`, `hv5f`, and `k09z`. Relevant conclusion: Spirit holds psyche intent only; non-intent architecture/report/spec/rationale knowledge belongs outside Spirit, and incomplete design surfaces must not be filled in as psyche-authorized intent.

Approved alignment preserved here: Mind, not Mine, is the non-Spirit knowledge substrate for the engine. Mind should hold non-intent system knowledge: reports, architecture, specs, rationale, and eventually many comments. Spirit remains only psyche intent. The first useful slice optimizes for making existing architecture/report knowledge queryable; full multi-component code/spec synchronization with Orchestrate and the repository-ledger/version-control layer is later.

## Current-State Architecture Picture

Mind already exists as a Rust component with a daemon, Kameo actor runtime, `mind` CLI, `meta-mind` CLI, Sema-backed durable store, ordinary `signal-mind` contract, and meta `meta-signal-mind` policy contract. Its current durable graph includes typed `Thought` and `Relation` records plus a technical graph. The technical graph already has the nouns needed for a first architecture/report knowledge substrate: `Component`, `Repository`, `Crate`, `Contract`, `WorkItem`, `SourceArtifact`, `Report`, `TechnicalClaim`, `Witness`, `StorageResource`, `SchemaFamily`, and `Table`.

The important gap is not substrate existence. The gap is workflow: no scout observed a first-class importer/indexer that ingests existing public `ARCHITECTURE.md` files, public reports, specs, and rationale material into Mind as queryable, source-backed technical knowledge. Existing seed data is hard-coded and includes report paths that were missing during scouting. Existing query contracts can already navigate technical nodes, relation neighborhoods, dependency closure, and provenance chains; the first slice should make those useful for the existing architecture/report corpus before attempting live code/spec synchronization.

## Responsibility Boundary

Mind owns non-Spirit system knowledge: architecture facts, report claims, specs, rationale, source-artifact references, evidence, technical claims, witnesses, dependency/provenance neighborhoods, corrections, and later derived synchronization obligations. Mind records are knowledge and observations, not psyche intent.

Spirit owns only psyche intent: what the psyche directs, decides, wants, or constrains durably. Spirit should not receive architecture/report facts merely because they sound important. If a Mind import finds missing intent or conflicting design direction that only the psyche can decide, the outcome is an open question to the psyche, not an inferred Spirit record.

Orchestrate owns active coordination machinery: claims, releases, handoffs, activities, role/lane registry, worktree inventory, lock-file projection, and later observer delivery. Mind may consume Orchestrate events as observations and may issue Orchestrate meta orders only under configured Mind authority mode.

Repository-ledger/version-control owns closure evidence about what actually changed: post-push repository events, commits, changed files, commit messages, and version/schema handover facts. Repository-ledger should feed Mind with source-artifact and witness evidence after push. It should not be stretched into pre-commit work ownership, because Orchestrate owns active work and worktree state.

## First Slice Design: Architecture/Report Import And Query

Build a component-local Mind slice that imports a small public architecture/report corpus and answers source-backed questions through existing `signal-mind` technical graph nouns wherever possible.

Initial corpus:

- `ARCHITECTURE.md` for `mind`, `signal-mind`, `meta-signal-mind`, `orchestrate`, `signal-orchestrate`, `meta-signal-orchestrate`, `repository-ledger`, and adjacent version/change components when referenced by the scouts.
- Public reports already named by the scout outputs and current public protocols, only when present.
- `protocols/active-repositories.md` and other public workspace architecture/protocol files only as source artifacts, not as psyche intent.
- No private reports or private repositories in the first slice.

Importer workflow:

1. Accept a bounded import manifest of public source paths and optional component/repository hints.
2. Read each source artifact and split it conservatively by stable locator: path plus heading, section anchor, or line span when available.
3. Create or find `Repository`, `Component`, `Contract`, `SourceArtifact`, and `Report` nodes.
4. Extract coarse `TechnicalClaim` nodes only when the source plainly states a system fact. Avoid speculative semantic atomization.
5. Create `Witness` nodes for the exact source locator and summary/evidence text needed to support each claim.
6. Append technical relations: `Documents`, `ClaimsAbout`, `ProvenBy`, `LocatedAt`, and explicit dependency/provenance relations only where the source states them.
7. Represent missing source paths explicitly as missing/unresolved source artifacts or rejected import evidence, not silent success.
8. Represent corrections by appending a newer claim/witness and `Supersedes` relation; do not mutate old graph truth in place.

Implementation boundary:

- Prefer using existing `SubmitTechnicalNode`, `SubmitTechnicalRelation`, `QueryTechnicalNodes`, and `QueryTechnicalRelations` operations.
- Add contract vocabulary only if the existing query/import surface cannot express source-located import results, missing-source status, or correction/supersession behavior.
- Do not implement Orchestrate observer ingestion, repository-ledger ingestion, proposed change sets, AI judgment gating, or authority escalation in this first slice.

## Data Model Mapping

Use existing technical nodes:

- `Repository`: a repo such as `mind` or `signal-mind`.
- `Component`: an engine component described by architecture/report knowledge.
- `Contract`: a contract crate or signal surface such as `signal-mind`.
- `SourceArtifact`: source files and docs such as `ARCHITECTURE.md`, schemas, protocol files, or code files named by architecture.
- `Report`: agent-output or public report files that are themselves durable evidence.
- `TechnicalClaim`: a source-backed system fact, such as "Mind owns non-Spirit system knowledge" or "Orchestrate owns active coordination machinery."
- `Witness`: the source locator proving a claim, including path and section/line locator where available.
- `WorkItem`: only for explicit work obligations, not ordinary imported facts.

Use existing technical relations:

- `Documents`: report/source artifact documents a component, repo, contract, or source artifact.
- `ClaimsAbout`: technical claim is about a component, repo, contract, source artifact, or work item.
- `ProvenBy`: technical claim is supported by a witness.
- `LocatedAt`: node maps to a path or source locator.
- `DefinesContract`, `DefinesCrate`, `OwnsRepository`, dependency relations, and provenance relations only where already explicit.
- `Supersedes`: newer claim/witness corrects an older claim/witness.

Likely contract gaps to verify before implementation:

- Whether existing node bodies can store a stable source locator with path plus heading/line span without overloading free text.
- Whether missing source behavior has a typed representation or needs an import rejection/result reply.
- Whether query replies can return enough provenance in one response for a fresh agent to trust the answer without follow-up graph crawling.
- Whether correction status is a view rule over `Supersedes` or needs a query option to hide superseded claims by default.

## Query UX

An agent should be able to ask Mind questions in component/repo/report/source language and receive compact source-backed answers. The CLI may project these to NOTA, but daemon traffic should remain typed `signal-mind` through Signal-frame/rkyv.

Minimum query intents:

- "What is known about component `<component>`?"
- "What architecture/report sources mention repo `<repo>`?"
- "What claims are made by report `<path>`?"
- "What source artifacts and witnesses prove claim `<claim>`?"
- "What does Mind know about source artifact `<path>`?"
- "What claims were superseded or corrected for `<component>`?"
- "What import sources were missing or unresolved?"

Expected reply shape:

- Answer summary as technical claims, not model prose authority.
- Each claim includes target node, source artifact/report, witness locator, and supersession status.
- Missing or unresolved source artifacts are returned explicitly.
- If the graph has no source-backed answer, reply with "no known source-backed claim" rather than synthesizing.
- If the answer requires psyche choice, return an open question marker rather than inferring intent.

## Worker Implementation Brief

`SignalMindContractWorker`

- Scope: inspect `signal-mind` technical node/relation/query contracts and decide whether existing vocabulary can carry import results, source locators, missing-source status, and superseded-view behavior.
- Source context: `signal-mind/src/technical.rs`, `signal-mind/src/lib.rs`, `signal-mind/schema/signal-mind.concept.schema`, existing round-trip tests.
- Completion claim: contract is either sufficient for first slice or has a minimal named gap with proposed operation/reply/body additions.
- Evidence: contract diff or no-diff rationale, round-trip/schema-drift checks planned or run.

`MindImporterWorker`

- Scope: implement bounded public corpus import into Mind technical graph using the contract result.
- Source context: `mind/src/actors/store/kernel.rs`, `mind/src/tables.rs`, `mind/src/technical_seed.rs`, CLI/client code, existing technical-memory tests.
- Completion claim: fixture and selected public architecture/report files import into append-only technical nodes/relations with provenance.
- Evidence: imported fixture graph, missing-source fixture result, durable restart proof.

`MindQueryUxWorker`

- Scope: add CLI/query projections for component/repo/report/source-artifact questions over existing technical query operations.
- Source context: `mind` CLI/client text projection code and `signal-mind` query/reply types.
- Completion claim: a fresh agent can query by component, repo, report path, source artifact path, claim, and missing-source status without hand-writing low-level relation traversals.
- Evidence: CLI transcript or integration test showing source-backed answer and no-answer behavior.

`ValidationWorker`

- Scope: write the smallest checks proving the first slice end to end.
- Source context: `mind/tests/*technical*`, `mind/tests/daemon_wire.rs`, `mind/tests/actor_topology.rs`, `signal-mind` round-trip tests, flake checks.
- Completion claim: tests cover corpus import, daemon/Signal query, provenance, missing source behavior, append/supersede correction behavior, and durable restart.
- Evidence: exact commands and results, preferably through existing Nix checks.

`MindKnowledgeAuditor`

- Scope: defect review after implementation, not implementation. Verify that the slice stays within Mind's non-Spirit knowledge boundary and does not silently synthesize unsupported claims.
- Evidence to receive: implementation diff, test output, sample imported graph, sample query replies, and list of imported source paths.
- Review focus: provenance truthfulness, missing-source behavior, contract compatibility, append-only correction behavior, privacy boundary, and whether the query UX overclaims authority.

## Tests And Evidence Plan

Smallest proof set:

1. Corpus import fixture: import two tiny public architecture/report fixture files, producing `SourceArtifact`/`Report`, `TechnicalClaim`, `Witness`, and relations.
2. Daemon/Signal query: start Mind with a temp `mind.sema` store, submit/import through the same typed path expected in production, query over the daemon socket, and verify typed replies.
3. Provenance: query a component and assert every returned claim has `ProvenBy` witness and source locator.
4. Missing source behavior: import a manifest entry for a nonexistent report path and assert the result records or returns missing-source status explicitly.
5. Append/supersede correction: import a corrected claim, assert old and new claims remain durable, `Supersedes` links them, and default query behavior is documented.
6. Durable restart: restart daemon/store and confirm imported graph and supersession state remain queryable.
7. No-answer behavior: query an unknown component and assert no source-backed claim is returned rather than synthesized prose.

## Domain Dependency Graph

First slice:

1. Contract sufficiency check blocks importer and query UX.
2. Import manifest and source-locator design blocks corpus importer.
3. Corpus importer blocks provenance, missing-source, and append/supersede tests.
4. Query UX blocks agent-facing acceptance proof.
5. Validation blocks audit.
6. Audit blocks claiming the first slice complete.

Later staged follow-ons:

1. Orchestrate observer delivery: implement real `Watch` event delivery for claim/release/handoff/activity/worktree/divergence changes, then let Mind consume observations. Blocked by first slice only conceptually; it can proceed after queryable knowledge proves the graph shape.
2. Repository-ledger ingestion: map post-push events, commit messages, and changed files into Mind `SourceArtifact`, `Witness`, and `TechnicalClaim` evidence. Blocks reliable code/spec drift detection.
3. Proposed change sets: introduce a typed object tying claimed scopes, intended source/spec changes, validation evidence, commit identifiers, and closure state. Blocked by Orchestrate event delivery plus repository-ledger ingestion.
4. AI judgment loop: add observe-mode technical-claim admission or spec/implementation alignment review using Guardian-like deterministic retrieval, closed typed verdicts, persisted evidence, and remand behavior. Blocked by source-backed query corpus and enough ingestion to build trustworthy judgment cases.
5. Authority escalation: move from `AuthorityMode::ObserveOnly` to `ProposeOrders`, and only later `IssueOrders`, after observation/proposal behavior is audited. Blocked by AI judgment evidence, Orchestrate policy storage/evaluation, and real caller authority proof.

## Remaining Psyche Decision Points

- How broad should the first public corpus be: Mind-family only, Mind plus Orchestrate/repository-ledger, or all active repository `ARCHITECTURE.md` files?
- Should default query views hide superseded claims, show them marked, or require an explicit history query?
- What wording should Mind use when imported architecture/report knowledge conflicts but there is no psyche decision yet: "conflict", "open question", "needs psyche choice", or another preferred term?

Conservative recommendation: start with Mind plus directly adjacent Orchestrate/repository-ledger architecture/report sources, show superseded claims marked in default answers, and label unresolved conflicts as "open question requiring psyche choice" only when the conflict depends on values or scope rather than implementation evidence.
