# Mind Accepted-Knowledge Model Situational Map

## Task And Scope

Research scout task: investigate practical information-modeling foundations for Mind's accepted-knowledge schema. Scope was read-only local inspection plus source-backed research. The goal is not a literature essay; it is a practical model a Rust component can implement now, with AI semantic judgment from the first slice and fixture-driven guardrails before corpus import.

The psyche-approved constraints from the brief are treated as controlling direction:

- Mind, not Mine, is the non-Spirit knowledge substrate for engine/system knowledge.
- First implementation is guarded and fixture-driven before real corpus import.
- Semantic judgment belongs to AI from the beginning.
- Deterministic code handles structure, typed inputs/outputs, routing, storage, and verdict application.
- Rejected Mind knowledge is not stored; the requester receives typed rejection and owns retry/abandonment.
- Accepted admission receipts are not stored.
- Persisted source/provenance is not mandatory; if source matters, it is part of the accepted knowledge itself.
- Avoid blurry nouns like `Thought` unless defended.
- Output must be practical and implementable now in Rust components.

## Commands And Local Surfaces Consulted

- Read requested library skill: `/home/li/primary/.agents/skills/library/SKILL.md`.
- Queried public Spirit intent:
  - `spirit "(PublicTextSearch [Mind knowledge schema accepted knowledge])"`
  - `spirit "(PublicTextSearch [Mind not Mine knowledge substrate])"`
  - `spirit "(PublicTextSearch [semantic judgment AI deterministic structure storage verdict])"`
- Checked source tooling:
  - `command -v papers` found `/run/current-system/sw/bin/papers`.
  - `papers --help` showed it is a document viewer, not a searchable library/catalog manager.
  - No `library`, `lit`, or `zotero` command was discoverable in `PATH`.
- Local workspace and repo context:
  - `/home/li/primary/ARCHITECTURE.md`
  - `/home/li/primary/protocols/active-repositories.md`
  - `/git/github.com/LiGoldragon/signal-mind/ARCHITECTURE.md`
  - `/git/github.com/LiGoldragon/signal-mind/README.md`
  - `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
  - `/git/github.com/LiGoldragon/signal-mind/src/graph.rs`
  - `/git/github.com/LiGoldragon/signal-mind/src/technical.rs`
  - `/git/github.com/LiGoldragon/meta-signal-mind/ARCHITECTURE.md`
  - `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
  - `/git/github.com/LiGoldragon/mind/README.md`
  - `/git/github.com/LiGoldragon/mind/schema/mind.concept.schema`
  - `/git/github.com/LiGoldragon/domain-criome/ARCHITECTURE.md`
  - `/git/github.com/LiGoldragon/signal-domain-criome/ARCHITECTURE.md`

No source was downloaded or added through a library mechanism, so the library skill's bibliography-update rule was not triggered. No `/nix/store` search was performed. Private scopes were not opened.

## Sources Consulted

- Claude E. Shannon, "A Mathematical Theory of Communication", Bell System Technical Journal 27, 1948. Locator used: Harvard-hosted PDF, page 1, lines 11-15 in web extraction, `https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf`. Relevant point: communication engineering handles selection, transmission, and noise separately from semantic meaning.
- Marvin Minsky, "A Framework for Representing Knowledge", MIT AI Memo 306, 1974. Locator used: MIT course PDF, pages 1-2, lines 59-80 in web extraction, `https://courses.media.mit.edu/2004spring/mas966/Minsky%201974%20Framework%20for%20knowledge.pdf`. Relevant point: frame-like structures bundle slots, defaults, matching, failure, and replacement, but are incomplete as a storage schema.
- Thomas R. Gruber, "A Translation Approach to Portable Ontology Specifications", Knowledge Acquisition 5(2), 1993. Locator used: author PDF, pages 1, 5-6, lines 18-44 and 187-220 in web extraction, `https://tomgruber.org/writing/ontolingua-kaj-1993.pdf`. Relevant point: an ontology is a shared domain vocabulary of classes, relations, functions, and objects; implementations can use restricted concrete representations.
- W3C, "RDF 1.1 Concepts and Abstract Syntax", Recommendation, 2014. Locator used: abstract lines 29-30, `https://www.w3.org/TR/rdf11-concepts/`. Relevant point: RDF's durable core is graph triples over resources and typed literals; datasets organize named graphs.
- W3C, "SKOS Simple Knowledge Organization System Reference", Recommendation, 2009. Locator used: section 8.1 and 8.6 lines 901-906 and 1050-1062, `https://www.w3.org/TR/skos-reference/`. Relevant point: concept schemes distinguish immediate broader/narrower assertions from inferred transitive closure; hierarchical and associative links have integrity constraints.
- Renzo Angles, "The Property Graph Database Model", AMW 2018, CEUR Vol. 2100 paper 26. Locator used: PDF pages 0-4, lines 4-28, 38-67, 87-134 in web extraction, `https://ceur-ws.org/Vol-2100/paper26.pdf`. Relevant point: a property graph is a directed labeled multigraph where nodes and edges can carry properties; a graph schema defines node types, edge types, property datatypes, and allowed edge types between node types.
- David I. Spivak, "Functorial Data Migration", arXiv:1009.1166v4, 2013 revision. Locator used: arXiv abstract lines 12-30, `https://arxiv.org/abs/1009.1166`. Relevant point: schemas can be modeled as small categories, instances as set-valued functors, and schema mappings induce canonical data migrations.
- E. F. Codd, "A Relational Model of Data for Large Shared Data Banks", Communications of the ACM 13(6), 1970. Locator used: UPenn-hosted PDF page 0, lines 5-24 in web extraction, `https://www.engineering.upenn.edu/~zives/03f/cis550/codd.pdf`. Relevant point: users/programs should be insulated from physical storage representation; relations and operations support consistency and representation independence.
- Stefano Ceri, Georg Gottlob, Letizia Tanca, "What You Always Wanted to Know About Datalog", IEEE TKDE 1(1), 1989. Locator used: SFU-hosted PDF pages 0-1, lines 4-13, 92-138 in web extraction, `https://www2.cs.sfu.ca/CourseCentral/721/jim/DatalogPaper.pdf`. Relevant point: Datalog separates stored extensional facts from derived intensional relations/rules; useful later for closure/query, not necessary for v1 admission.
- W3C, "PROV-DM: The PROV Data Model", Recommendation, 2013. Locator used: section 2.1 lines 209-240 and 263-271, `https://www.w3.org/TR/prov-dm/`. Relevant point: provenance can be modeled as entities, activities, agents, and binary relations; derivation requires influence, not merely a processing chain.
- Luciano Floridi, "Is Semantic Information Meaningful Data?", Philosophy and Phenomenological Research 70(2), 2005. Locator used: PhilSci Archive PDF pages 0-1 and 16-18, lines 7-16 and 31-43 in web extraction, `https://philsci-archive.pitt.edu/2536/1/iimd.pdf`. Relevant point: for declarative semantic information, truthfulness is not optional; false "information" is better treated as pseudo-information for admission purposes.
- ISKO Encyclopedia, "Literary warrant", entry by Mario Barite et al. Locator used: lines 38-46, 52-58, 80-82, 190-224, `https://www.isko.org/cyclo/literary_warrant`. Relevant point: classification vocabulary should be warranted by actual literature/practice/user need, not abstract taxonomy alone; warrant is useful for adding classes/domains, not for every fact record.

## Observed Local Facts

- `/home/li/primary/ARCHITECTURE.md` frames Persona as a system where components are mechanism and LLM agents are the cognitive layer. It says schema is the source of truth, fully-qualified symbol paths are universal machine-readable identity, and most workspace logic is enum-domain cross-product matching.
- Public Spirit record `w312` says deterministic answers derivable from input, including routing, dispatch, lookup, classification, projection, and address resolution, are mechanism and belong in code/schema-derived machinery; agents are reserved for decisions code cannot make.
- `/home/li/primary/protocols/active-repositories.md` lists `signal-mind`, `meta-signal-mind`, and `mind` as active local repos. It also lists `domain-criome`, `signal-domain-criome`, and `meta-signal-domain-criome`, but those are Criome domain-name authority/projection components, not a general knowledge-domain ontology service.
- `signal-mind` currently defines:
  - a typed mind graph with `ThoughtKind` values `Observation`, `Memory`, `Belief`, `Goal`, `Claim`, `Decision`, `Reference`;
  - `RelationKind` values including `Implements`, `Requires`, `Supports`, `Refutes`, `Supersedes`, `Authored`, `References`, `Decides`, `Belongs`;
  - a separate technical dependency graph as `TechnicalNode` / `TechnicalRelation`;
  - canonical `TechnicalNodeKey` families such as `component:<name>`, `repo:<name>`, `contract:<crate>:<surface>`, `storage:<component>:<name>`, `schema:<component>:<name>`, and `table:<component>:<name>`;
  - typed rejection reasons for invalid keys, kind/body mismatch, duplicates, missing endpoints, domain/range violations, and persistence rejection.
- `signal-mind/ARCHITECTURE.md` states `RelationKind` and `TechnicalRelationKind` own domain/range validation tables, and runtime-local relation folklore is not accepted.
- `mind/ARCHITECTURE.md` states the daemon persists typed `Thought`/`Relation` and `TechnicalNode`/`TechnicalRelation` records through `sema-engine` registered families. It mints IDs and timestamps inside store/infrastructure actors, not request payloads.
- `mind/ARCHITECTURE.md` says current `Thought` / `Relation` records are immutable, corrections append a newer fact plus `Supersedes`, and current thought queries hide superseded targets while old records remain in `mind.sema`.
- `mind/schema/mind.concept.schema` is older and extremely coarse: `Thought (Text)`, `Relation (Text)`, `Note (Text)`. The architecture and contract schema are more current than this concept file.
- `domain-criome` is a content-addressed `.criome` domain registry/resolution/projection daemon. It provides an analogy for delegated authority chains, but it is not currently a shared knowledge-domain classifier.

## Interpretations

- The existing `Thought` noun is too broad for the brief. It mixes mental state, work memory, goals, beliefs, claims, and references. The literature does not rescue the noun for a durable accepted-knowledge substrate; Minsky's frames are richer cognitive structures, not a license to store every accepted statement as a "thought".
- The existing technical graph is closer to the right shape than the typed mind graph: stable public keys, closed node kinds, closed relation kinds, domain/range validation, and typed rejection are all good. It is still too pre-specialized for general accepted knowledge because it embeds technical dependency vocabulary directly into the record family.
- The best v1 substrate is a typed attributed graph with a small ontology layer: accepted node records, accepted relation records, domain/classification records, and optional accepted source/evidence records only when semantically asserted. This follows RDF/property-graph practice without importing RDF's full global-web machinery.
- Category theory helps mainly as a design discipline: distinguish schema from instance, keep mappings explicit, and expect future migrations between schemas. It does not require a category-theory runtime in v1.
- Datalog helps later for derived views such as transitive domain closure, dependency closure, or "current accepted knowledge" projections. It should not be part of admission v1 because deterministic rule layers could tempt the system into emulating semantic judgment.
- Provenance should not be automatic metadata in v1. W3C PROV is useful if Mind needs to assert "this accepted knowledge was derived from X by activity Y" as domain knowledge. That should be a normal accepted node/relation, not a mandatory receipt or hidden audit store.

## Practical Principles Extracted

- Separate syntax from semantics. Shannon supports the code/AI boundary: code can validate payload shape and message flow; it cannot decide meaning just because the bytes parse.
- Store accepted semantic information, not every submission. Floridi supports a sharp admission rule: if the AI judge does not accept the candidate as well-formed, meaningful, and true enough for the domain, it is pseudo-information for Mind and should be returned as rejection, not archived.
- Use a graph, but type it. RDF shows that subject-predicate-object is enough to link resources; property graph work shows why implementation wants typed nodes, typed edges, properties, and schema-instance constraints.
- Store asserted direct links separately from derived closure. SKOS is the practical model: assert immediate broader/narrower or belongs-to links; derive transitive closure in query/view code.
- Keep domain vocabulary small and warranted. Classification warrants argue against inventing a huge top ontology. Add domains/classes when fixtures or repeated accepted knowledge require them.
- Make schema migrations first-class. Spivak's categorical database work points to explicit schema mappings as the right future affordance; Codd points to representation independence. v1 should use typed Rust records and store families in a way that can migrate without rewriting semantic policy into storage layout.
- Keep frames out of storage v1. Minsky's frames are useful for AI prompt context and later retrieval/matching, but slots/defaults/surprise handlers are too much for the first accepted-knowledge schema.

## Recommended Minimal Mind Nouns

Use these as v1 contract/storage nouns. Names are intentionally plain and narrower than `Thought`.

- `KnowledgeSubmission`: transient request object. Carries the candidate body, caller-visible domain/classification hint if any, and optional source/evidence candidate if the requester wants source to become accepted knowledge. This is not stored as a receipt.
- `KnowledgeIdentifier`: compact daemon-minted stable identifier for accepted records. Type carries whether it identifies an entity, relation, statement, or domain concept; the string should not encode kind prefixes.
- `KnowledgeEntity`: an accepted object/concept/artifact/system thing. Fields: identifier, `entity_kind`, optional stable key, label/title, typed payload.
- `KnowledgeStatement`: an accepted declarative claim that is not yet normalized into an entity or relation. Fields: identifier, `statement_kind`, text/body, domain, optional about-list of entity selectors. This is the escape hatch for fixture-driven implementation; it should be actively normalized later, not treated as the permanent default.
- `KnowledgeRelation`: an accepted typed edge between two accepted records. Fields: identifier, relation kind, source identifier, target identifier, optional typed payload. This is the normal home for dependency, classification, support, contradiction, supersession, source-use, and ownership links.
- `KnowledgeDomain`: a controlled classification concept/scheme node. Fields: identifier, stable key, label, optional parent domain through relation rather than inline tree.
- `KnowledgeSource`: an accepted source/evidence object only when the source is itself part of the accepted knowledge. A source is not an admission receipt. It may be a document, repository path, symbol, URL, report, test fixture, or human-stated instruction if admissible.
- `KnowledgeVerdict`: transient AI judge output. It is returned to the requesting agent and applied by deterministic code, but is not stored after admission/rejection except insofar as accepted source/evidence is separately modeled as knowledge.

Recommended v1 enum sketch:

```text
KnowledgeBody
  | Entity(KnowledgeEntityCandidate)
  | Statement(KnowledgeStatementCandidate)
  | Relation(KnowledgeRelationCandidate)
  | Domain(KnowledgeDomainCandidate)
  | Source(KnowledgeSourceCandidate)

AcceptedKnowledge
  | Entity(KnowledgeEntity)
  | Statement(KnowledgeStatement)
  | Relation(KnowledgeRelation)
  | Domain(KnowledgeDomain)
  | Source(KnowledgeSource)

KnowledgeJudgeVerdict
  | Accept(AcceptedKnowledgeDraft)
  | Reject(KnowledgeRejection)
```

## Recommended Minimal Relation Types

Start with a small closed enum. Add relation kinds only when fixtures require them and the domain/range table is clear.

- `ClassifiedAs`: accepted record belongs to a `KnowledgeDomain` or class concept. This is direct classification only.
- `BroaderThan` / `NarrowerThan`: direct domain/concept hierarchy links. Do not assert transitive closure.
- `RelatedTo`: associative non-hierarchical concept relation. Keep it disjoint from hierarchical links where possible.
- `References`: a knowledge record mentions or refers to a source/entity without claiming proof.
- `SupportedBy`: a statement/relation/entity is supported by a `KnowledgeSource` or `KnowledgeStatement`. Use only when the support relation is itself accepted knowledge.
- `Contradicts`: accepted knowledge conflicts with another accepted record. This is AI-judged, not regex-derived.
- `Supersedes`: newer accepted record replaces older accepted record in current views. The old record may remain if it was previously accepted; for newly rejected candidates nothing is stored.
- `DependsOn`: only if dependency type is unknown in v1 fixtures. Prefer split relation kinds such as `BuildDependsOn`, `RuntimeDependsOn`, `WireDependsOn`, `StorageDependsOn` when the domain is technical and the split is known.
- `Defines`: repository/crate/schema/source artifact defines a contract, type, table, or domain object.
- `Implements`: component/code artifact implements contract/schema/behavior.
- `Uses`: broad operational use when a more precise dependency relation is not warranted.

Domain/range constraints should live on the relation enum, as `signal-mind` already does. Example: `ClassifiedAs` target must be `KnowledgeDomain`; `SupportedBy` target must be `KnowledgeSource` or a statement accepted as evidence; `Supersedes` should require same top-level accepted-kind unless the AI judge returns an explicit cross-kind replacement draft and the relation enum allows it.

## Recommended Domain Classification Shape

Use a recursive concept scheme, not a top ontology:

```text
KnowledgeDomainKey(String)  // canonical, caller-visible, validated
KnowledgeDomain {
  identifier: KnowledgeIdentifier,
  stable_key: KnowledgeDomainKey,
  label: TextBody,
  scope_note: Option<TextBody>
}
```

Hierarchy is represented by `BroaderThan` / `NarrowerThan` relations. Query code may compute closure, but the store only accepts direct links. This fits SKOS and avoids accidental recursion bugs.

Domain keys should be warranted by fixtures and local practice. Initial examples likely useful for Mind:

- `domain:system`
- `domain:component`
- `domain:contract`
- `domain:schema`
- `domain:storage`
- `domain:runtime`
- `domain:test-fixture`
- `domain:source`
- `domain:architecture`
- `domain:intent-manifestation`

Do not bind this to `domain-criome`. That component owns Criome domain names, delegations, and projection. Mind's `KnowledgeDomain` is a semantic classification scheme. The fit is architectural: both can use delegated authority and direct-vs-derived views, but they are different domains.

## AI Judgment Boundary

The admission path should be a typed two-stage pipeline:

1. Deterministic preflight:
   - Decode one typed request.
   - Validate newtypes, enum variants, relation endpoint existence, domain key shape, maximum sizes, and store availability.
   - Route to the judge with a typed context packet containing candidate, relevant accepted neighbors, relation domain/range rules, and fixture policy.
2. AI semantic judgment:
   - Decide whether the candidate is knowledge rather than a task, instruction, receipt, log line, private material, or unsupported prose.
   - Decide whether the candidate is meaningful and true enough for the domain.
   - Classify the domain when classification is semantic rather than mechanically derivable.
   - Detect semantic duplicate, supersession, contradiction, or required normalization.
   - Return a typed `KnowledgeJudgeVerdict`.
3. Deterministic verdict application:
   - On `Accept`, persist only the accepted records/relations named in the accepted draft. Mint IDs/timestamps in store actors.
   - On `Reject`, return a typed rejection to requester and persist nothing.
   - On store failure after acceptance, return a typed persistence rejection; do not store a partial receipt.

Suggested transient rejection enum:

```text
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

The important split: `StructuralPreflightFailed` can be produced by code; semantic variants come from the AI judge. Deterministic code may apply the verdict but should not synthesize semantic rejection reasons from keyword/regex rules.

## What Not To Model In V1

- No `Thought` as the accepted-knowledge root noun.
- No `Belief` or confidence ledger unless a fixture requires uncertain accepted knowledge. The brief asks for accepted knowledge; uncertainty can be a statement payload later.
- No mandatory provenance, source, author, admission receipt, or rejected archive.
- No DOLCE/BFO upper ontology.
- No full RDF/OWL import/export, blank nodes, named graphs, RDF reification, or SPARQL.
- No Datalog/rule engine in admission.
- No frame slots/defaults/inheritance machinery.
- No vector embeddings as canonical identity or durable truth.
- No automated contradiction detector implemented as regex/keyword logic.
- No corpus import path until fixture admission, rejection, supersession, and query behavior are proven.
- No cross-component shared "domain" dependency on `domain-criome`; use Mind-local semantic domains first.

## Fit With Recursive Or Shared Domain Systems

No general recursive/shared semantic-domain system was found locally. The closest local system is `domain-criome`, but it is a `.criome` naming/delegation/projection registry. Its useful pattern is delegated authority: if a domain is not owned locally, return a typed not-authoritative/delegation answer rather than pretending the domain is unknown.

For Mind v1:

- Keep `KnowledgeDomain` Mind-local and recursive through explicit broader/narrower relations.
- Store only direct domain links; derive closure in read/query views.
- Make future shared-domain integration a schema mapping, not a hard dependency. If another component later owns domain schemes, Mind can map `KnowledgeDomainKey` to that authority through an accepted relation such as `DelegatedTo` or `DefinedBy`.
- Use fixture-backed domain warrants. New domains/classes land when accepted test fixtures need them, not from abstract top-down taxonomy design.

## First Fixture-Driven Implementation Slice

Implement a guarded `SubmitKnowledge` / `QueryKnowledge` family alongside, or as successor to, the current typed graph. Do not route through `SubmitThought`.

Minimal contract records:

```text
SubmitKnowledge(KnowledgeSubmission)
QueryKnowledge(KnowledgeQuery)

MindReply
  | KnowledgeAccepted(AcceptedKnowledgeView)
  | KnowledgeRejected(KnowledgeRejection)
  | KnowledgeList(KnowledgeList)
```

Minimal store families:

- `knowledge_entities`
- `knowledge_statements`
- `knowledge_relations`
- `knowledge_domains`
- `knowledge_sources`

The store may physically implement these as one family with a closed `AcceptedKnowledge` enum or as separate families. Prefer one family only if queries and domain/range validation remain clean; otherwise separate families match the property graph node/edge split better.

Initial fixtures:

1. Accept a `KnowledgeEntity` for `component:mind` classified as `domain:component`.
2. Accept a `KnowledgeEntity` for `contract:signal-mind:ordinary` classified as `domain:contract`.
3. Accept a `KnowledgeRelation::Defines` from `repo:signal-mind` or `crate:signal-mind` to `contract:signal-mind:ordinary`.
4. Reject a syntactically valid but semantically non-knowledge submission, returning `NotKnowledge` and storing nothing.
5. Reject a relation with missing endpoint before AI judgment through `StructuralPreflightFailed`.
6. Accept a `KnowledgeStatement` about a source-backed architecture fact, with a `KnowledgeSource` only because the source is part of the accepted knowledge.
7. Accept `Supersedes` from a newer statement to an older statement; current query hides or demotes the old target without deleting it.
8. Reject a candidate that contradicts accepted knowledge unless the AI judge returns an explicit accepted `Contradicts` relation as the knowledge being asserted.

Tests should prove:

- rejected semantic candidates do not add rows to any knowledge family;
- accepted replies are not persisted as receipt records;
- accepted source/provenance is absent unless submitted/accepted as `KnowledgeSource` or source relation;
- relation domain/range validation is deterministic and table-driven;
- semantic verdicts in fixtures are injectable/mocked so Rust tests are deterministic while preserving the AI-shaped boundary;
- corpus import path is disabled or guarded until fixtures pass.

## Risks

- `KnowledgeStatement` can become a junk drawer. Mitigation: require a `statement_kind`, domain, and about-list where possible; add normalization fixtures that turn repeated statement shapes into entity/relation records.
- AI judge nondeterminism can make tests flaky. Mitigation: the Rust slice consumes a typed judge trait with fixture implementations; e2e AI tests can run separately and reshape prompt/context later.
- Domain hierarchy can silently become ontology sprawl. Mitigation: require warrant in fixtures or accepted source knowledge for new domain keys.
- Persisting old superseded accepted records may conflict with the brief's "rejected knowledge is not stored." Clarification: old records were accepted at the time; newly rejected candidates are never stored. Current views should distinguish active accepted knowledge from superseded accepted history.
- Existing `Thought` APIs may pull new work back into the old vocabulary. Mitigation: new contract names should be `Knowledge*`; compatibility should be explicit conversion or migration, not aliasing.
- Source/provenance pressure may reintroduce hidden receipts. Mitigation: source is just another accepted knowledge entity/relation; admission process artifacts stay transient.

## Unknowns And Not Checked

- I did not inspect private repositories or private data.
- I did not search `/nix/store`.
- I did not run tests; this was a scouting/research task.
- I did not fully read DOLCE, BFO, OWL profiles, or institution theory because the practical sources already supported a small typed graph and the brief warned not to over-read.
- I did not verify whether an unpublished branch already contains a `Knowledge*` Mind schema. Local checked-out `mind` and `signal-mind` show `Thought`/`Relation` and technical graph surfaces as of inspection.

## Bottom Line

Mind should start with an accepted typed attributed graph: `KnowledgeEntity`, `KnowledgeStatement`, `KnowledgeRelation`, `KnowledgeDomain`, and optional `KnowledgeSource`, admitted through a transient AI `KnowledgeJudgeVerdict`. Deterministic Rust owns typed decoding, structural validation, relation domain/range tables, ID/time minting, store writes, current-view projection, and typed rejection delivery. AI owns semantic admission, domain judgment when not mechanically derivable, duplicate/supersession/contradiction judgment, and normalization recommendations. Rejections and admission receipts do not persist.
