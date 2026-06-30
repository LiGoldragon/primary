# Mind Judgment Loop Patterns — Situational Map

## Task and Scope

Read-only scout task: inspect local source truth in `/home/li/primary` for reusable judgment-loop patterns from Spirit Guardian, Appealer / Court of Appeal concepts, and Menchie / Mentci prompt-analysis or pre-dispatch review concepts. Focus is only on patterns potentially useful for Mind as the non-Spirit knowledge substrate: intake filtering, accumulated rejected or uncertain material, escalation, typed decisions, evidence capture, and AI-in-loop boundaries.

Approved alignment from the brief: Mind, not Mine, is the non-Spirit knowledge substrate for the engine. Mind should use AI judgment loops similar in spirit to Guardian / Appealer to keep specification and implementation synchronized. Mind stores non-intent system knowledge, so Spirit intent behavior must not be copied blindly.

No source files were edited. This report is the only written artifact.

## Locations and Commands Consulted

Commands:

- `spirit "(PublicTextSearch [Mind Spirit Guardian Appealer Menchie prompt analysis judgment loop])"`
- `rg -n "Guardian|guardian|Appealer|appealer|Court of Appeal|court of appeal|appeal" . --glob '!repos/**' --glob '!private-repos/**' --glob '!target/**' --glob '!node_modules/**'`
- `rg -n "Menchie|menchie|prompt analysis|prompt-analysis|pre-dispatch|predispatch|pre dispatch|dispatch review|review gate" . --glob '!repos/**' --glob '!private-repos/**' --glob '!target/**' --glob '!node_modules/**'`
- `ls -la /home/li/primary` and `ls -la /home/li/primary/repos`
- `rg --files /home/li/primary/repos/spirit /home/li/primary/repos/mentci-lib /home/li/primary/repos/mentci-egui`
- Bounded `rg` and `nl -ba ... | sed -n ...` reads over Spirit, Mentci, Mind, and signal-mind paths named below.

Relevant public Spirit query records observed:

- `qjrf`: Spirit holds intent, not information or belief; incomplete design surfaces should be asked about rather than inferred into fake records.
- `w312`: deterministic answers belong in code or schema-derived machinery; agents are reserved for cognition code cannot make.
- `zbuy`: Guardian model performs semantic judgment for every guarded write; deterministic code gathers context, validates structure, and applies typed verdict consequences.
- `zgi8`: Spirit Guardian is the single locus of semantic judgment; model checks semantic concerns, structural admission stays upstream.
- `y9c6`: agent hooks to Mind for skills and accumulated context.

Primary file locations inspected:

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/home/li/primary/repos/spirit/ARCHITECTURE.md`
- `/home/li/primary/repos/spirit/manual.md`
- `/home/li/primary/repos/spirit/src/guardian.rs`
- `/home/li/primary/repos/spirit/src/guardian_prompt.rs`
- `/home/li/primary/repos/spirit/src/guardian_journal.rs`
- `/home/li/primary/repos/spirit/src/store/mod.rs`
- `/home/li/primary/repos/spirit/src/store/guardian_bundle.rs`
- `/home/li/primary/repos/spirit/src/nexus.rs`
- `/home/li/primary/repos/spirit/src/criome_gate.rs`
- `/home/li/primary/repos/spirit/src/guardian-prompts/{role,record-shape,justification-shape,checklist,few-shot}.md`
- `/home/li/primary/repos/mentci-lib/ARCHITECTURE.md`
- `/home/li/primary/repos/mentci-lib/src/{approval,decision,observation}.rs`
- `/home/li/primary/reports/preciousMainContext/10-minimal-early-context-design.md`
- `/home/li/primary/reports/legacy-disposition/SITUATION-2026-06-30-parked-spirit-tracks.md`
- `/home/li/primary/repos/mind/ARCHITECTURE.md`
- `/home/li/primary/repos/signal-mind/README.md`
- `/home/li/primary/repos/signal-mind/src/{lib,technical}.rs`

Not checked:

- Private repositories.
- Live daemons, sockets, stores, or production state.
- Full test execution.
- `signal-mentci` source, because no `/home/li/primary/repos/signal-mentci` symlink was present in the inspected repo list.

## Confirmed Observations

### Spirit Guardian

Spirit is explicitly the intent layer, not a general knowledge store. `/home/li/primary/repos/spirit/manual.md:3` says it captures what the psyche directs, decides, and wants; `/home/li/primary/repos/spirit/manual.md:9` says the explanation of Spirit lives in the manual, not in the store. `/home/li/primary/repos/spirit/manual.md:50` through `:64` separates intent from information and warns against inferred design synthesis.

The Guardian is the single semantic judgment point. `/home/li/primary/repos/spirit/manual.md:25` through `:31` says the Guardian checks consistency, duplication, trampling, and genuine intent, while only structural parse/type validation stays upstream. `/home/li/primary/repos/spirit/manual.md:130` through `:146` repeats the split: model semantic judgment; deterministic code gathers context, validates structure, applies typed consequences, and parses closed verdicts.

The court metaphor is implemented as a Guardian pattern, not an appeal system. `/home/li/primary/repos/spirit/manual.md:156` through `:165` describes the submitting agent as advocate, verbatim psyche quotes as testimony, typed justification as argued case, and Guardian as judge. `/home/li/primary/repos/spirit/src/guardian_prompt.rs:1` through `:17` states the same in code comments and says the verdict is strictly binary, admit or remand.

Intake filtering is conservative and ordered. `/home/li/primary/repos/spirit/src/guardian-prompts/checklist.md:1` says gates run in order, stop at first failure, and uncertainty is reject-and-remand rather than accept. The checklist covers retrieval sufficiency, target soundness, operation fit, testimony, destructive-op authorization, warrant, shape, affirmative framing, classification, metadata burden, and cross-record collision at lines `:1` through `:12`.

Rejected material is not discarded silently. `/home/li/primary/repos/spirit/manual.md:193` through `:205` says rejections are remands that name the coherent repair shape, and direct psyche declarations that conflict with active records should become broader maintenance operations. `/home/li/primary/repos/spirit/src/guardian_prompt.rs:123` through `:140` includes a `Matter` remand pattern naming the proper home outside Spirit.

The Guardian output vocabulary is typed and closed. `/home/li/primary/repos/spirit/src/guardian_prompt.rs:56` through `:81` lists model-emittable `GuardianRejectionReason` variants. `/home/li/primary/repos/spirit/src/guardian_prompt.rs:277` through `:294` renders the rejection catalogue from the enum. `/home/li/primary/repos/spirit/src/guardian_prompt.rs:297` through `:322` renders exact NOTA verdict grammar from real `GuardianVerdict` values.

The model call is narrow and bounded. `/home/li/primary/repos/spirit/src/guardian.rs:193` through `:219` performs the Guardian call, parses the verdict, and retries malformed verdicts through `GuardianRetry`. `/home/li/primary/repos/spirit/src/guardian.rs:27` through `:33` caps verdict-format retries at two. `/home/li/primary/repos/spirit/src/guardian_prompt.rs:325` through `:340` fixes model options to NOTA output, temperature 0, high reasoning effort, and thinking enabled.

Some rejection is deterministic rather than AI-driven. `/home/li/primary/repos/spirit/src/guardian.rs:152` through `:164` rejects empty testimony as a structural fact before the model call. `/home/li/primary/repos/spirit/src/store/mod.rs:971` through `:982` detects duplicate entries deterministically by kind, domains, and normalized description. `/home/li/primary/repos/spirit/src/store/mod.rs:985` through `:1013` applies a duplicate Guardian rejection by bumping the existing record's importance and returning a typed duplicate rejection.

Context gathering is deterministic and typed. `/home/li/primary/repos/spirit/src/store/mod.rs:871` through `:936` assembles the `RecordSet` for each guarded operation, including candidate-entry neighborhoods and named target records for maintenance operations. `/home/li/primary/repos/spirit/src/store/mod.rs:939` through `:954` gathers context by domain scopes and referents. `/home/li/primary/repos/spirit/src/store/guardian_bundle.rs:1` through `:7` and `:13` through `:44` show a deduplicating accumulator keyed by record identifier.

Guardian evidence is persisted. `/home/li/primary/repos/spirit/src/guardian_journal.rs:35` through `:60` defines `GuardianOperation` and `GuardianDecision` as typed stored audit data containing operation, record bundle, verdict, and database marker. `/home/li/primary/repos/spirit/src/nexus.rs:877` through `:882` records each Guardian decision after a model decision. `/home/li/primary/repos/spirit/src/nexus.rs:849` through `:875` records a typed `HarnessUnavailable` rejection when Guardian is required but not configured.

Fail-closed behavior is explicit. `/home/li/primary/repos/spirit/manual.md:148` through `:154` says a Spirit with no configured Guardian fails closed. `/home/li/primary/repos/spirit/src/nexus.rs:849` through `:875` implements that for guarded record operations when `guardian_required` is true.

Guardian prompts are compiled in but partly runtime-swappable. `/home/li/primary/repos/spirit/src/guardian.rs:87` through `:101` sets the compiled-in prompt source by default; `/home/li/primary/repos/spirit/src/guardian.rs:124` through `:130` and `:138` through `:144` allow a runtime prompt source swap. `/home/li/primary/repos/spirit/src/guardian_prompt.rs:405` through `:422` include prompt sections from `src/guardian-prompts/`.

### Appealer / Court of Appeal

No local implementation was found for an Appealer or Court of Appeal. The bounded appeal search found `/home/li/primary/reports/legacy-disposition/SITUATION-2026-06-30-parked-spirit-tracks.md:515` through `:546`, which explicitly says appeals are not built, the string appears only in forward design language, and no Spirit source, skill, bead, or config mentions an appeals mechanism. That report interprets appeals as a possible future path to re-submit a Guardian-rejected record with added testimony or contest a rejection, but flags it as future design only.

Therefore, the confirmed source-truth pattern available today is Guardian's reject-and-remand loop, not a second-level appeal system.

### Criome Gate Adjacent Pattern

Spirit's criome gate is an authorization-loop pattern adjacent to Guardian. `/home/li/primary/repos/spirit/src/criome_gate.rs:201` through `:222` defines typed `GateDecision` variants: `Authorized`, `Observed`, `Unconfigured`, `Denied`, and `Unreachable`. `/home/li/primary/repos/spirit/src/criome_gate.rs:224` through `:231` says only `Authorized` or `Observed` ship. `/home/li/primary/repos/spirit/src/criome_gate.rs:268` through `:276` makes `Off` / unarmed the fail-closed default, and `/home/li/primary/repos/spirit/src/criome_gate.rs:334` through `:359` maps authorization observations into fan-out decisions.

This is not an AI judgment loop in the inspected code, but it is a clean typed gate / observe-mode / fail-closed pattern.

### Menchie / Mentci Prompt Analysis and Pre-Dispatch

The canonical spelling is Mentci; "Menchie" appears as old speech-to-text drift. `/home/li/primary/ARCHITECTURE.md:266` states the earlier Menchie spelling was a speech-to-text error.

Mentci prompt-to-session preflight is documented as direction, not current implementation. `/home/li/primary/repos/mentci-lib/ARCHITECTURE.md:81` through `:89` describes a Mentci-daemon-level direction where a prompt enters Mentci, a cheap contained-API preflight model analyzes it, emits fixed-schema NOTA, loads skills, builds a scaffold, and opens a persistent named harness session through `terminal-cell` / orchestrate. `/home/li/primary/reports/preciousMainContext/10-minimal-early-context-design.md:120` through `:153` confirms the classify-select-route machinery does not exist as built machinery, and that the preflight router, prompt-pack generator, harness driver, and Mentci's routing-front-door role are net-new or unratified.

The implemented Mentci pattern today is a client-side MVU approval/observation model over daemon-owned state. `/home/li/primary/repos/mentci-lib/ARCHITECTURE.md:50` through `:59` says the implemented pieces are `ObservationModel`, approval state machine, NOTA fallback renderer, and closed-decision to criome verdict mapping. `/home/li/primary/repos/mentci-lib/ARCHITECTURE.md:126` through `:142` says `on_user_event`, `on_engine_event`, and `view` are the MVU surface; side effects are `Cmd` descriptions and transport is owned by the outer runtime.

Mentci accumulates pending and answered approval material locally while daemon state remains canonical. `/home/li/primary/repos/mentci-lib/src/approval.rs:206` through `:217` defines `ApprovalModel` with pending queue, selected question, answered log, subscriptions, and next subscription ID. `/home/li/primary/repos/mentci-lib/src/approval.rs:260` through `:295` makes `Defer` leave a question pending while binding verdicts remove and log it. `/home/li/primary/repos/mentci-lib/src/approval.rs:314` through `:328` models edited answers as proposals, not as a verdict variant.

Mentci uses typed closed decisions and a single enum contact point. `/home/li/primary/repos/mentci-lib/src/decision.rs:1` through `:12` says Mentci consumes real contract types, not duplicate vocabularies. `/home/li/primary/repos/mentci-lib/src/decision.rs:51` through `:71` maps `ApprovalDecision` to `AuthorizationApprovalDecision` in exactly one `From` match.

Mentci keeps AI / human / daemon boundaries separate. `/home/li/primary/repos/mentci-lib/ARCHITECTURE.md:40` through `:48` says thin clients do not open criome sockets, and clients subscribe to updates and submit responses rather than owning approval logic. `/home/li/primary/repos/mentci-lib/src/observation.rs:170` through `:182` sends `AnswerQuestion` to the Mentci daemon rather than opening criome from the client.

### Existing Mind Substrate

Mind already has a daemon, Kameo actor runtime, typed work graph, typed Thought/Relation graph, typed technical graph, subscriptions, and a Signal-frame daemon/client transport. `/home/li/primary/repos/mind/ARCHITECTURE.md:1` through `:17` summarizes this status.

Mind's current public surface is `signal-mind`. `/home/li/primary/repos/signal-mind/README.md:5` through `:23` lists memory/work graph operations, typed mind graph operations, typed technical dependency graph operations, and channel choreography. `/home/li/primary/repos/signal-mind/src/lib.rs:1249` through `:1301` declares the `Mind` channel operations and replies, including `SubmitTechnicalNode`, `SubmitTechnicalRelation`, query/subscription operations, and typed technical rejection replies.

Mind has an existing technical graph suited to non-intent knowledge. `/home/li/primary/repos/signal-mind/src/technical.rs:196` through `:209` defines technical node key families including component, repository, crate, contract, source artifact, report, technical claim, witness, storage, schema, and table. `/home/li/primary/repos/signal-mind/src/technical.rs:421` through `:543` defines node bodies, including `TechnicalClaimNode` and `WitnessNode`. `/home/li/primary/repos/signal-mind/src/technical.rs:609` through `:626` defines relation kinds including `Implements`, `Documents`, `ClaimsAbout`, `ProvenBy`, and `Supersedes`.

Mind already treats corrections as append plus relation rather than mutation. `/home/li/primary/repos/mind/ARCHITECTURE.md:646` through `:648` says technical corrections append a newer technical fact and a `Supersedes` relation to the old fact. `/home/li/primary/repos/mind/ARCHITECTURE.md:654` through `:656` says old thoughts remain in `mind.sema`; correction is a view rule, not in-place mutation.

Mind currently enforces structural typed checks, not AI judgment. `/home/li/primary/repos/mind/ARCHITECTURE.md:623` through `:642` lists rejections before persistence for kind/body mismatch, missing endpoints, invalid relation endpoints, malformed technical keys, and typed dependency/provenance traversal. No Mind Guardian-like AI admission loop was found in the inspected paths.

## Interpretations for Mind

### Patterns That Transfer Cleanly

Use a single narrow judgment loop for a specific write family, not a general agent reviewer. Spirit's strongest transferable pattern is not "intent capture"; it is the shape in which deterministic code assembles a typed case, one specialized model judges only the semantic part, the model emits a closed typed verdict, and deterministic code applies consequences. For Mind, the likely first family is technical-claim admission or spec-implementation alignment, not all Mind writes.

Keep deterministic structure outside the model. Mind should keep current structural checks for key shape, relation endpoint kinds, existing target lookup, and typed query assembly in code, mirroring Spirit's split at `/home/li/primary/repos/spirit/manual.md:130` through `:146`. AI should judge only semantic adequacy: whether a claim is supported by witnesses, whether it duplicates or contradicts live knowledge, whether a source artifact really implements a specification claim, or whether uncertainty should remain unresolved.

Use typed case records. Spirit's `GuardianOperation` plus `RecordSet` plus `DatabaseMarker` maps cleanly to a Mind judgment case such as `TechnicalClaimJudgmentOperation` plus relevant technical neighborhood plus store marker. The case should include the candidate claim, claimed target nodes, witness nodes/source locators, and relevant existing claims/relations.

Use closed verdicts and closed reasons. Mind should not accept prose-only AI judgments. A first loop can have variants such as `Accept`, `Reject`, `Remand`, or `Escalate`, with reasons such as `MissingWitness`, `UnsupportedClaim`, `DuplicateClaim`, `ContradictsClaim`, `TargetMissing`, `RetrievalInsufficient`, `ImplementationDrift`, and `UnclearScope`. Exact names need design, but the closed-vocabulary pattern is source-backed by Guardian.

Persist the judgment evidence. Spirit's Guardian journal stores operation, bundle, verdict, and marker. Mind should store a judgment receipt as technical graph material: a `TechnicalClaim` or `Witness` plus relations, or a dedicated judgment table if the contract grows one. Since Mind already has `TechnicalClaim`, `Witness`, `ClaimsAbout`, `ProvenBy`, and `Supersedes`, the first slice can use existing graph nouns where possible.

Treat rejections as remands, not dead ends. For Mind, rejected/uncertain material should accumulate as explicit pending or remanded claims with evidence of why they failed, not disappear. Mentci's `Defer` leaves the question pending; Guardian remands name repair shapes. A Mind loop should preserve rejected/uncertain candidates with enough context for a later agent or model to add witnesses, narrow the claim, or supersede a stale claim.

Allow observe-mode before gate-mode. CriomeGate's `Observed` mode is useful for rollout: Mind can run a judgment loop that records what it would reject or remand without blocking technical graph writes at first. Once verdict quality is trusted, gate only the narrow operation family.

Use Mentci-style preflight as a separate intake classifier, not the same as the knowledge admission judge. The prompt-preflight design can classify a user prompt into skills, scaffold, and target session before dispatch. Mind's knowledge judge should instead assess whether a technical claim or spec/implementation relation belongs in Mind. These can share infrastructure, but not prompts or verdict vocabularies.

### Patterns That Do Not Transfer Blindly

Do not copy Spirit's intent-vs-matter bar. For Spirit, "matter" is rejected because it belongs in repos, skills, or trackers. For Mind, non-intent system knowledge is the point. The Spirit `Matter` reason is useful only as a warning against wrong substrate, not as a Mind rejection reason for technical content.

Do not require psyche verbatim testimony for ordinary Mind knowledge. Spirit's evidence law depends on preserving psyche intent. Mind technical knowledge should rely on source locators, reports, code paths, schemas, test output, and agent observations. Verbatim psyche quotes may be one evidence kind when a claim is about psyche-approved architecture, but they should not be the universal admission requirement.

Do not make all Mind writes AI-gated. Mind already stores operational work graph state, technical graph nodes, subscriptions, and choreography scaffolding. Structural deterministic writes should continue without AI when correctness is derivable from the request and existing typed state. This matches public intent record `w312`.

Do not treat appeals as an existing reusable implementation. The appeal layer is only future design in the inspected sources. Mind can define a remand/resubmission path now, but should not claim to be porting a built Appealer.

Do not put side effects in the review model. Mentci confirms a useful boundary: the model or client produces typed decisions or commands; daemon-owned code performs transport, persistence, and external effects.

## Risks and Unknowns

- Appeal architecture is not built. Any Mind "Appealer" design would be new work, based on Guardian remands plus the parked appeal concept, not an implementation transplant.
- The prompt-to-dispatch preflight router is not built. It is only a documented direction; no source implementation was found.
- `signal-mentci` was not present under `/home/li/primary/repos`, so Mentci contract details were inferred from `mentci-lib` imports and docs, not checked in the contract repo.
- Mind has no current AI judgment loop in inspected paths. Adding one will require new contract and storage design or careful reuse of technical graph records.
- The first Mind loop must avoid becoming a second Spirit. If it starts requiring psyche testimony for technical knowledge or rejecting "matter", it will contradict the approved alignment.
- Model drift and stale prompt risk apply. Guardian mitigates prompt/type drift by rendering verdict grammar from enums; Mind should do the same if it adds judgment prompts.
- Evidence retrieval quality is load-bearing. Guardian has `RetrievalInsufficient`; Mind needs an equivalent because spec/implementation drift judgment is only as good as the code/report/schema neighborhood supplied.
- Private material was intentionally not inspected. If Mind eventually stores private-sensitive non-intent knowledge, privacy and access policy need a separate design pass.

## Recommended First Judgment-Loop Slice for Mind

Build a narrow "technical claim admission / alignment review" loop over existing Mind technical graph concepts.

Proposed first slice:

1. Intake operation: a candidate `TechnicalClaim` about a component, repo, contract, schema, source artifact, or implementation relation, with one or more `Witness` locators.
2. Deterministic preparation: validate technical keys and relation endpoints with existing `signal-mind` validators; gather relevant existing `TechnicalClaim`, `Witness`, `Implements`, `Documents`, `ClaimsAbout`, `ProvenBy`, and `Supersedes` neighborhoods.
3. AI judgment: one clean-context model judges only semantic support and synchronization: does the witness support the claim, is it duplicate, contradicted, stale, too broad, or insufficiently retrieved.
4. Typed verdict: `Accept`, `Remand`, or `Escalate`, with a closed reason set rendered from the enum and parsed as one NOTA value.
5. Evidence capture: persist the candidate, relevant bundle identity, verdict, explanation, and store marker. Prefer representing accepted knowledge as existing technical graph nodes/relations; represent remands as pending/remanded technical claims rather than deleting them.
6. Initial rollout: observe-mode first. Record verdicts and compare them against human/agent expectations without blocking `SubmitTechnicalNode` or `SubmitTechnicalRelation`. Gate only after the verdict/reason distribution is trustworthy.

This slice keeps Mind focused on non-intent system knowledge while reusing the mature Guardian loop shape: deterministic retrieval, specialized AI judgment, closed typed decisions, audit evidence, and remandable uncertainty.
