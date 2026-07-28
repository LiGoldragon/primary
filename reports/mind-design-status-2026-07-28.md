# Mind design status recovery — 2026-07-28

## Finding

Mind is **not design-complete**.  It has several real, independently useful
implementation slices, but the inspected record does not contain a psyche
approval of a complete operational design, a declared first production use, or
the policy that would make its advertised authority meaningful.  Therefore the
2026-07-28 deployment proposal is a technically bounded service proposal, not
evidence that deploying a fixture-backed daemon is the next approved product
step.

This is a read-only historical recovery.  It distinguishes (a) witnessed
implementation, (b) an attested ruling or alignment, and (c) agent proposal.
It does not infer missing psyche choices from code, tests, or a prior report.

## What Mind is meant to be

The stable through-line is a durable, local Persona knowledge/state component,
not a router or a second Spirit:

- `mind/AGENTS.md`, `README.md`, and `ARCHITECTURE.md` assign it central
  memory/work state, typed graph facts and relations, durable subscriptions,
  accepted knowledge, and eventually channel-choreography policy.  They assign
  ordinary claims, handoffs, and activity to Orchestrate.
- The current `signal-mind` contract describes accepted knowledge as a
  non-Spirit substrate; `mind-judge-config` describes the accepted-knowledge
  store as public, non-private, non-intent knowledge.  The concrete v1
  admission record is presently a shared `Domain` plus a statement, with an
  identity minted by Mind after a judge accepts it.
- The later queryable-knowledge handoff extends that role to source-backed
  architecture, reports, specs, rationale, technical claims, witnesses and
  dependency/provenance views.  It expressly puts active coordination in
  Orchestrate and says a missing or conflicting design choice is a question for
  the psyche rather than a Mind/Spirit record.

This is a broad intended role, not one completed product.  In particular,
"central state machine", "accepted-knowledge store", and "queryable
architecture knowledge" are all present.  The record does not choose which is
the first deployed human workflow or the acceptance criterion by which the
first deployment is useful.

## Authority and provenance ledger

| Claim | Classification | Evidence and limitation |
| --- | --- | --- |
| Do not fabricate a design resolution when a design surface is incomplete. | Attested psyche rule. | Public Spirit record `qjrf`, recorded in `MindNotaSurfaceScout` and the legacy Spirit recovery reports, says Spirit holds what the psyche directs rather than information/belief and that incomplete design should be asked of the psyche. The original conversation was not re-opened in this recovery. |
| Mind is the non-Spirit substrate for engine/system knowledge; Spirit is for psyche intent. | Repeatedly reported as psyche-approved alignment. | `MindKnowledgeModel`, `MindPracticalKnowledgeModel`, `MindQueryableKnowledgeWeave`, and `MindOrchestrateChangeClosure` all say this. The alignment is consistent with the public contract/prompt boundary. No primary psyche transcript or append-only Mind design ruling was located in the surveyed material, so it is not elevated to a verbatim ruling here. |
| Make existing architecture/report knowledge queryable before the full Orchestrate/repository-ledger code/spec synchronization loop. | Reported later psyche priority, but source not primary here. | `MindOrchestrateChangeClosure` says an additional psyche answer gave this priority; `MindQueryableKnowledgeWeave` builds the first slice around it. The raw answer was not found during this recovery. |
| AI decides semantic admission; deterministic code owns typed shape, routing, storage, and applying a verdict. | Reported constraint plus implemented design. | The practical-model reports call it controlling; `signal-mind`, `mind`, and `mind-judge` implement a typed judge port. It is strong design evidence, but not a located direct ruling in this survey. |
| A profile-min user service with `%t` sockets, XDG state, and the fixture judge is the correct first deployment. | Agent deployment proposal. | `reports/mind-deployment-proposal-2026-07-28.md` explicitly calls itself a proposal. It offers no psyche ruling selecting its scope, owner boundary, fixture default, or activation as the next product step. |
| Rich entity/relation/domain/source ontology; corpus importer; change-set workflow; Guardian-like alignment judge; authority escalation. | Agent proposals/destination designs. | These appear in the knowledge, queryable-weave, judgment-loop, and Orchestrate-closure handoffs. They name useful directions and open decisions, not settled authority. |

Unattributed code is not thereby wrong, but it is not authority.  Current
choices such as the fixture default, the simple domain-plus-statement accepted
knowledge record, `mind.sema` table/schema evolution, manual injected
Orchestrate decisions, and the dual-purpose owner socket are implementation
facts unless and until a ruling or approved design ties them to the selected
product purpose.

## Current behavior: wired, partial, and absent

### Wired implementation

- The long-lived daemon, one-NOTA-request thin CLI, Signal-frame socket
  transport, owner-only working/meta socket modes, and durable `mind.sema`
  store are implemented in `mind` at `042550a03083`.
- Work graph operations; typed thought/relation and technical graph
  persistence/query; durable filters and an initial/post-commit subscription
  path; and a judge-gated accepted-knowledge v1 path have source and test
  witnesses.  `mind/ARCHITECTURE.md` carefully calls older work tables and the
  subscription buffer transitional in places.
- The Mind-to-Orchestrate transport for manually injected Create, Retire, and
  Refresh decisions exists.  This proves frame transport, not a policy that
  decides when any order should be issued.
- `mind-judge` has a socket-serving adapter and `mind-judge-config` owns public
  prompt text.  Its own architecture still calls socket activation/semi-
  persistence a target shape and says that integration is pending where stated.

### Direct disconfirming evidence of overall completion

- `mind/src/meta.rs` answers every current `meta-mind` Configure/Inspect
  operation with `RequestUnimplemented(NotBuiltYet)`.  The Mind architecture
  likewise states policy storage and evaluation are destination work.
- `mind/src/actors/dispatch.rs` returns `NotInPrototypeScope` for
  `AdjudicationRequest` and `ChannelList`; the architecture calls inbound
  choreography policy partial and says decision derivation is unbuilt.
- The architecture marks the three-actor, demand-driven subscription design as
  destination work; the current in-actor buffer is explicitly transitional.
- `MindOrchestrateChangeClosure` found no real Orchestrate observer delivery,
  no typed proposed-change-set object, no repository-ledger-to-Mind bridge, and
  no event that expresses code/spec review obligations.  These are prerequisites
  for the proposed wider synchronization role.
- The queryable-knowledge handoff says corpus scope, contract gaps, importer,
  query UX, validation, and audit must precede a claim that its first slice is
  complete.  No evidence was found that it was implemented.
- The accepted-knowledge usability audit documented a live wrong-admission
  failure: a statement was reported accepted while the prompt example was
  stored instead.  Later commits repair/restructure the judge vertical slice,
  but this recovery performed no build or live test and therefore cannot claim
  the practical admission product is now proven.

## Historical completion check

No inspected historical document says that **Mind's design as a whole** is
complete.  The positive completion statements are deliberately narrower:

- `MindPracticalKnowledgeModel/GeneralCodeImplementer-Evidence.md` says its
  *v1 contract implementation and verification* were complete.
- `mind/src/technical_seed.rs` describes completion of the first public typed
  technical-memory slice.
- Current history contains vertical-slice and prompt/evaluation commits, most
  recently moving judge calls off the store-kernel path.

Those claims do not close the competing product definitions or the missing
policy/integration design.  They are evidence of progress, and also
disconfirm the opposite error that Mind is merely a blank scaffold.

## Open design questions

1. What first human workflow is Mind being deployed to serve: durable work
   memory, accepted-knowledge admission, or queryable source-backed
   architecture knowledge?
2. If queryable knowledge is first, what public corpus is in scope, what is the
   admission/ingestion rule, and how should contradictory or superseded claims
   appear in default answers?
3. What is the durable relationship between the current simple
   `Domain + statement` accepted-knowledge v1 and the proposed richer
   technical/architecture graph?  Are they separate products, a migration, or
   one common knowledge model?
4. What are the semantic-judge failure semantics: fail closed only, remand and
   retain a pending candidate, or escalation; and what evidence/provenance is
   durable without importing Spirit's intent model?
5. What policy is Mind meant to own before it can observe, propose, or issue
   orders to Orchestrate/router?  This includes storage, configuration,
   authority proof, failure/retry, audit, and the boundary with Orchestrate's
   active claims and lifecycle.
6. Is deployed Mind deliberately a narrow independently useful user service,
   or one member of a later Persona federation?  The two have different
   configuration, dependency, test, readiness, and rollback designs.

## First question for the psyche

**Which single real workflow should the first deployed Mind make useful to a
person or agent—durable work memory, accepted-knowledge admission, or
queryable source-backed architecture knowledge—and what observable outcome
would make that first use successful?**

This question is intentionally not answered here.  It selects the product
boundary before a service module, judge configuration, corpus importer, or
federation integration is treated as the next required work.

## Sources consulted

- `reports/mind-deployment-proposal-2026-07-28.md`
- `/git/github.com/LiGoldragon/mind/{AGENTS.md,README.md,ARCHITECTURE.md,Cargo.toml,src/{daemon.rs,meta.rs,configuration.rs,actors/dispatch.rs}}`
- `/git/github.com/LiGoldragon/{signal-mind,meta-signal-mind,mind-judge,mind-judge-config,signal-mind-judge}` source, architecture, tests, and Jujutsu history
- `agent-outputs/Mind{KnowledgeModel,PracticalKnowledgeModel,QueryableKnowledgeWeave,OrchestrateChangeClosure,NotaSurfaceScout,JudgmentLoopPatterns,UsabilityAudit,LiveJudgeEval}/`
- `reports/{recovery-map-2026-07-28.md,persona-system-audit/,field-readiness/}` and primary beads (read-only)

No source was edited, no test/build/deployment/live-state observation was run,
and no beads were changed.  This report is the required recovery artifact.
