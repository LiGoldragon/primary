# Flow Artifacts Protocol — Prior Art Research

**Filed:** 2026-08-21
**Produced by:** a subflow of design session `5c8be3ca`. The subflow's own short id is unknown (no session UUID was available to this agent at runtime).
**Research conducted by:** research subagent (general-purpose, Luna/xhigh). All external claims are cited with URLs. [WITNESSED] means the source page was fetched and read directly. [REPORTED] means the claim comes from search summaries, secondary descriptions, or community posts.

The system being designed: model sessions called "flows," each with a UUID; first-8-hex is the "short id." A repository where every flow gets one directory named by its short id, holding artifacts the flow produces. Artifacts are classified epistemically: WITNESSED (direct observation — test run, probe, code read), REPORTED (relayed claims — research from another agent, documentation-based, opinion-based), SESSION LOG (the flow's self-witness). There is an index of flows; subflow artifacts file under the parent flow, marked with the subflow's short id. The short id beside every record forms a "chain of origin" enabling re-verification against the full transcript.

The claim taxonomy given here — WITNESSED, REPORTED, SESSION LOG — is the protocol's design. All prior art is judged against it.

---

## Part 1: Practice — Agent Memory and Artifact Storage Systems

### 1A. MemGPT / Letta

**Structuring principle:** OS-inspired hierarchical memory tiers managed by the agent itself through explicit function calls. Three tiers: Core Memory (fixed-size, prompt-pinned, writeable only via tool calls — persona, key facts), Archival Memory (vector-DB-backed, semantic retrieval), Recall Memory (searchable log of full historical interaction). [REPORTED: https://serokell.io/blog/design-patterns-for-long-term-memory-in-llm-powered-architectures] The MemGPT paper confirms "hierarchical memory systems in traditional operating systems" as the inspiration. [WITNESSED: https://arxiv.org/abs/2310.08560] The Letta homepage names "Memory Models," "Context Repositories / Git-based Memory," and "Sleep-time Compute" as research directions, without detailing tier names. [WITNESSED: https://letta.com]

Letta ships MemFS — a git-backed memory directory providing version history. Changes are versioned as commits; they are not traced back to specific source episodes. [REPORTED: https://kenhuangus.substack.com/p/how-ai-agents-actually-remember-inside]

**Mapping:** Recall Memory is the LOG (direct interaction log). Core and Archival are derived outputs — closer to REPORTED. No first-class WITNESSED category; the tier boundary is "in-context vs. retrieved," not "direct observation vs. hearsay."

**Worth adopting:** The three-tier naming is useful for distinguishing access cost and freshness. It does not capture epistemic origin; the protocol should not conflate freshness with epistemic type.

---

### 1B. mem0

**Structuring principle:** Flat fact store with entity linking for a graph layer, scoped by four orthogonal keys at write time: `user_id`, `agent_id`, `run_id` (session), `app_id`. User messages stored under `user_id`; assistant messages under `agent_id`. Retrieval filters by any combination. [REPORTED: https://github.com/Snseam/awesome-agent-memory/blob/main/products/archives/mem0-blog-state-of-2026.md] [WITNESSED: https://kenhuangus.substack.com/p/how-ai-agents-actually-remember-inside]

Each memory write can carry: source type, timestamp, authoring agent, supporting evidence, transformation operation, confidence, update history. An actor-aware Group Chat mode distinguishes user-stated facts from agent-generated inferences. These are emerging norms, not guaranteed defaults. [REPORTED: https://mem0.ai/blog/state-of-ai-agent-memory-2026]

**Mapping:** `run_id` is the session key — the LOG anchor. The actor-aware separation of user-stated vs. agent-generated is the closest to WITNESSED/REPORTED, framed as "who said it" rather than "how do I know it."

**Worth adopting:** The four-axis scoping model. The `run_id` key on every memory write is directly analogous to tagging every artifact with the producing flow's short id. The confidence and source-type fields on individual writes are worth including.

---

### 1C. Zep

**Structuring principle:** Context graph with explicit episode-to-derived-artifact provenance at every level. Three layers: Episodes (raw verbatim sources — chat messages, documents, JSON records, stored byte-for-byte), Entities (nodes extracted by LLMs across episodes), Facts (timestamped relationships / edges between entities, each carrying an `episodes` list of every source that contributed). [WITNESSED: https://blog.getzep.com/how-zep-tracks-provenance-in-agent-memory/] [WITNESSED: https://www.getzep.com]

Every derived artifact (entity, fact) is associated at construction time with the episodes it came from. Entity merging preserves episode associations from both merged nodes. Multi-source facts accumulate the full list of contributing episodes. Facts carry `valid_at` and `invalid_at` timestamps; the superseding episode is part of the record. Homepage states: "Every fact in the graph traces back to the source episode that produced it." [WITNESSED: https://blog.getzep.com/how-zep-tracks-provenance-in-agent-memory/]

**Mapping:** Episodes are the LOG (direct observation, verbatim). Entities and Facts are REPORTED (derived by LLM extraction). The episode-list on every fact is exactly the chain-of-origin concept. Temporal invalidation (a later episode can mark a fact invalid with a timestamp and a link to the superseding episode) is valuable.

**Worth adopting:** The episode → entity → fact hierarchy with episode-list provenance carried on every derived artifact. Temporal invalidation linked to the superseding source. This is the most directly applicable pattern among memory systems.

---

### 1D. LangMem

**Structuring principle:** Namespace-tuple-keyed memory collections managed through LangGraph's store. Four semantic types: Semantic (facts/knowledge), Episodic (past interaction examples), Procedural (self-updated system prompts), Short-term (in-context working memory). Namespaces are tuples, e.g., `("memories", "{user_id}")`. `thread_id` is not part of the default namespace. [WITNESSED: https://langchain-ai.github.io/langmem/] [WITNESSED: https://langchain-ai.github.io/langmem/guides/dynamically_configure_namespaces/]

**Mapping:** No provenance tracking found in reviewed pages. The namespace tuple is a clean scoping mechanism; the absence of source attribution is a gap.

**Worth adopting:** The namespace tuple pattern for scoping. Do not follow LangMem's pattern of omitting provenance.

---

### 1E. MLflow

**Structuring principle:** Experiment-organized runs, each with a UUID `run_id`. Metrics, params, tags, and an artifact log stored per-run. Child runs store their own artifacts independently. [REPORTED: https://thelinuxcode.com/managing-nested-runs-mlflow/]

Sub-runs: created with `mlflow.start_run(nested=True)`. Each child gets its own UUID `run_id`. Parent-child link is a tag: `mlflow.parentRunId` on the child stores the parent's `run_id`. `get_parent_run(run_id)` navigates up. [REPORTED: https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/hyperparameter-tuning/part1-child-runs/]

**Mapping:** The run is the LOG unit. Nested run hierarchy is the chain-of-origin structure. No WITNESSED/REPORTED distinction within a run.

**Worth adopting:** The `mlflow.parentRunId` tag convention for linking a subflow artifact to its parent flow. Simple, queryable, and applicable directly: a subflow's artifact directory carries a `parent_id` field pointing to the parent flow's short id.

---

### 1F. Weights and Biases

**Structuring principle:** Separates the run record (metrics, hyperparams — lightweight) from versioned Artifact objects (datasets, models, checkpoints — linked as inputs/outputs of runs). Convention: `name:alias` (e.g., `training_dataset:latest`). Artifact lineage graph: raw data → preprocessing → training → evaluation → deployed model. Any artifact traces to the exact dataset version that produced it. [WITNESSED: https://docs.wandb.ai/models/artifacts] [REPORTED: https://letsdatascience.com/blog/w-b-complete-guide-ml-experiment-tracking]

**Mapping:** Artifact lineage is chain-of-derivation — "what produced what" — but does not capture observation type (WITNESSED vs. REPORTED).

**Worth adopting:** The clean separation of the run record (lightweight metadata) from heavier versioned artifact objects. The `name:alias` versioning convention allows stable references alongside evolving content.

---

### 1G. LangSmith

**Structuring principle:** Hierarchical traces with three levels of identifier: `id` (unique per span), `trace_id` (= root run's `id`, shared by all spans), `parent_run_id` (immediate parent's `id`), and `dotted_order` (sortable string encoding the full ancestor chain: `<timestamp>Z<uuid>.<timestamp>Z<uuid>...`). Invariants: `id` = last 36 chars of `dotted_order`; `trace_id` = first UUID in `dotted_order`. [WITNESSED: https://docs.langchain.com/langsmith/run-data-format]

**Mapping:** `trace_id` is the LOG root. `dotted_order` is a machine-readable chain of origin. No WITNESSED/REPORTED distinction.

**Worth adopting:** The `dotted_order` encoding — a single sortable string that encodes both the timestamp and the full ancestor chain, allowing provenance reconstruction without a separate graph query. Directly applicable to our short-id chain.

---

### 1H. LangFuse

**Structuring principle:** Trace (32-char hex `trace_id`, root of one interaction) with child Observations (16-char hex `observation_id`). All child observations inherit the parent's `trace_id`. Distributed tracing via `parentSpanContext` (contains: `traceId`, `spanId`, `traceFlags`). [WITNESSED: https://langfuse.com/docs/observability/features/trace-ids-and-distributed-tracing]

**Mapping:** Trace is the LOG root; observations are production steps. No WITNESSED/REPORTED distinction. Different ID lengths for root vs. child make hierarchy level visually legible in a log.

**Worth adopting:** Using different id lengths (or a clear visual marker) to distinguish root flow ids from subflow ids at a glance.

---

### 1I. Agent Journal / Memory Bank Practices

**Cline memory bank:** Six core Markdown files in `memory-bank/`: `projectBrief.md`, `productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`. A temporal variant adds `changelog.md` and a sliding window on `activeContext.md` — the 10 most-recent dated events, oldest dropped when an 11th arrives. [WITNESSED: https://github.com/cline/prompts/blob/main/.clinerules/memory-bank.md] [WITNESSED: https://github.com/cline/prompts/blob/main/.clinerules/temporal-memory-bank.md]

**Mapping:** `activeContext.md` and `progress.md` function as a running LOG of the current flow. Static context files are REPORTED background. No provenance distinction.

**Worth adopting:** The temporal sliding window on the live LOG file — fixed-size, drops stale entries. When a flow ends the full transcript is the permanent record; the sliding window serves the live flow's self-reference only.

**Known gap:** Claude Code subagents do not share what they learn; each has an isolated context. Shared memory banks are an unsolved coordination problem. [REPORTED: https://hindsight.vectorize.io/blog/2026/05/06/claude-code-subagents-shared-memory]

---

### 1J. Claude Code Session Storage

**Root index:** `~/.claude.json` — global config tracking projects, MCP servers, recent prompts. [WITNESSED: https://milvus.io/blog/why-claude-code-feels-so-stable-a-developers-deep-dive-into-its-local-storage-design.md]

**Session files:** `~/.claude/projects/<encoded-project-path>/<session-ulid>.jsonl`. Path encoding: absolute project path with every `/` replaced by `-`. Each session is a ULID (Universally Unique Lexicographically Sortable Identifier) as the filename base. ULIDs sort lexicographically oldest-first. [WITNESSED: https://clauderecall.com/blog/where-claude-code-stores-sessions] [WITNESSED: https://promptconduit.dev/blog/claude-code-transcripts-location]

**File format:** Append-only JSONL. Record types: `user`, `assistant`, `tool_use`, `tool_result`, `summary` (compaction checkpoint), `system` (session metadata), file-history snapshot (pre-edit backup). Every record carries a `uuid` and `parentUuid`, forming a linked cause-and-effect chain. [WITNESSED: https://clauderecall.com/blog/where-claude-code-stores-sessions] [WITNESSED: https://milvus.io/blog/why-claude-code-feels-so-stable-a-developers-deep-dive-into-its-local-storage-design.md]

**Mapping:** The JSONL file is the SESSION LOG. The `uuid`/`parentUuid` chain within a session is a structural antecedent of the chain-of-origin concept. No WITNESSED/REPORTED distinction within the transcript.

---

### 1K. OpenAI Codex CLI

**Storage:** `~/.codex/sessions/YYYY/MM/DD/rollout-{ISO8601-TIMESTAMP}-{UUID}.jsonl`. Date-organized directories. [WITNESSED: https://github.com/openai/codex/issues/24948]

**Session id:** Generated by the OpenAI backend at session start, embedded inside JSONL records. Filename and embedded `session_id` are both auto-generated. Session resumption reads the embedded ID; renaming a file does not break resumption. A resumed session appends to the existing file. [WITNESSED: https://github.com/openai/codex/discussions/3827] [WITNESSED: https://github.com/openai/codex/pull/27264]

**File format:** Append-only JSONL. Record types: `compacted`, `response_item/reasoning`, `response_item/function_call`, `response_item/function_call_output`, `response_item/custom_tool_call`, `event_msg/token_count`, `turn_context`. Each record carries `originator`, `cli_version`, `model_provider`, timestamps. Files can reach 700 MB–2 GB. [WITNESSED: https://github.com/openai/codex/issues/24948]

**Subagent session ids:** Subagents receive their own separate `ThreadId` and rollout files. Parent-child lineage is a directed graph of spawn edges tracked via `upsert_thread_spawn_edge` in `StateRuntime`. Forked rollouts embed source session metadata. Subagents can be resumed independently. Known bug: the main agent may not be aware of subagents spawned before context compaction. [WITNESSED: https://deepwiki.com/openai/codex/4.4-session-resumption] [REPORTED: https://github.com/openai/codex/issues/24281]

**Mapping:** Each rollout file is the SESSION LOG. The `ThreadId` DAG formed by spawn edges is the chain-of-origin for subflows. Embedding the session ID inside the JSONL (not derived from filename) is a design choice that ensures resumption integrity.

**Worth adopting:** The spawn-edge directed graph for tracking subagent parentage. The decision to embed the session ID in the data, not rely on the filename.

---

## Part 2: Theory — Knowledge Classification by Provenance

### 2A. Evidentiality in Linguistics

**Structuring principle:** Evidentiality is a grammatical category marking the source of information for a statement. About one-quarter of the world's languages require speakers to mark evidentiality morphosyntactically — you cannot make a tensed assertion without choosing a category. [WITNESSED: https://en.wikipedia.org/wiki/Evidentiality]

Main categories: (1) Direct / Visual sensory — speaker directly perceived, typically by sight. (2) Non-visual sensory — perceived through hearing, touch, smell. (3) Inferential — deduced from physical evidence without direct perception. (4) Reportative / Hearsay — received from another person; sometimes split into hearsay-reportative (what others say, potentially inaccurate) vs. quotative-reportative (attributed direct quote, higher fidelity). (5) Assumed / General cultural knowledge.

The globally most common evidential system is two-term: witnessed vs. non-witnessed. [WITNESSED: https://en.wikipedia.org/wiki/Evidentiality] [REPORTED: https://glossary.sil.org/term/evidentiality]

**Mapping:** Direct (WITNESSED) vs. Reportative (REPORTED) vs. Inferential (a possible third category — "I deduced this from observations I made, but I did not directly see the event"). The two-term binary the protocol uses is linguistically universal — no cross-linguistic justification for more elaborate primary taxonomy.

**Worth adopting:** The inferential category as a potential third tag, distinct from pure REPORTED. It would cover "I ran a test and concluded X" (inferential, hence still WITNESSED in our scheme) vs. "the documentation says X" (REPORTED). The protocol may not need to split inferential from direct-witnessed, but the distinction is real and non-trivial.

---

### 2B. Law of Evidence

**Structuring principle:** A witness testifies only to what they personally perceived — admissible because they are present, under oath, subject to cross-examination. Hearsay is an out-of-court statement offered for the truth of the matter asserted; the original speaker is unavailable for challenge. Hearsay is presumptively inadmissible (U.S. FRE 801). [WITNESSED: https://en.wikipedia.org/wiki/Hearsay]

Chain of custody: a verifiable log of location and possession history of evidence from collection to courtroom. Any gap raises the possibility of tampering. [REPORTED: https://caseguard.com/articles/documenting-chain-of-custody/]

Software analogy: an artifact not traceable to an identified, verifiable source is the software equivalent of hearsay. Cryptographic hashes play the role of tamper-evidence seals. [REPORTED: https://www.kusari.dev/learning-center/chain-of-custody] [REPORTED: https://danacrane.medium.com/how-to-implement-a-chain-of-custody-for-your-software-supply-chain-96ffb4685a19]

**Mapping:** Direct testimony = WITNESSED. Hearsay = REPORTED. The requirement that even inadmissible hearsay must be traceable to an identified speaker maps onto the requirement that every REPORTED artifact carries a `reported_by` attribution pointing to the source flow or source document.

**Worth adopting:** The "challengeability" criterion: a WITNESSED artifact is one a later flow can re-examine independently (re-run the test, re-read the code). A REPORTED artifact's challenge must trace through the chain of relaying agents. This operationalizes the distinction without requiring philosophical debate.

---

### 2C. Historiography: Primary / Secondary / Tertiary Sources

**Structuring principle:** Primary — original material created at the time (artifacts, diaries, eyewitness accounts, raw data). Secondary — interprets, analyzes, or evaluates primary sources; written after the fact. Tertiary — compilation or digest of primary and secondary sources (encyclopedias, textbooks). [WITNESSED: https://en.wikipedia.org/wiki/Primary_source] [REPORTED: https://en.wikipedia.org/wiki/Tertiary_source]

Context-dependence: the same document can be primary or secondary depending on the research question. Primary does not mean infallible; secondary synthesis can be more reliable than naive primary reading.

**Mapping:** SESSION LOG = primary source (unedited flow transcript). WITNESSED artifacts = primary sources derived from direct observation within the flow. REPORTED artifacts = secondary. A summary artifact compiled from multiple REPORTED sources = tertiary.

**Worth adopting:** The framing that WITNESSED does not mean automatically correct — it means "directly observed." The protocol should not conflate direct observation with truth. WITNESSED artifacts can be wrong.

---

### 2D. W3C PROV Ontology

**Structuring principle:** Core classes: Entity (thing with fixed aspects), Activity (something that occurs over time and acts on entities), Agent (bears responsibility for an activity). Core properties: `wasGeneratedBy`, `used`, `wasDerivedFrom`, `wasAttributedTo`, `wasAssociatedWith`, `wasInformedBy`. Subproperties of `wasDerivedFrom`: `hadPrimarySource` (derived from a first-hand source), `wasQuotedFrom`, `wasRevisionOf`. [WITNESSED: https://www.w3.org/TR/prov-o/]

PROV does not have a "hearsay" subproperty. The epistemological status of the original observation is outside its scope. [WITNESSED: https://www.w3.org/TR/prov-o/]

**Mapping:** `hadPrimarySource` ≈ WITNESSED derivation. `wasDerivedFrom` ≈ REPORTED derivation. The flow artifact protocol extends PROV by making the epistemic type a first-class attribute that PROV leaves implicit.

**Worth adopting:** The Entity / Activity / Agent triple as interoperable vocabulary. A WITNESSED artifact is generated by (`wasGeneratedBy`) an observation Activity, which `used` an Entity (the thing observed). A REPORTED artifact `wasDerivedFrom` another Entity (the source document or source flow's artifact). The `hadPrimarySource` property names the WITNESSED relationship in standard vocabulary.

---

### 2E. Software Supply-Chain Attestation: in-toto and SLSA

**Structuring principle (in-toto):** Layout (signed document defining expected steps, authorized actors, verification rules) + Links (signed documents produced at each step: command executed, materials/inputs with digests, products/outputs with digests, byproducts) + Functionaries (named actors who sign links) + Inspections (verification operations run at consumption). At verification: every step has a signed link from the authorized functionary, digests chain correctly (outputs of step N match inputs of step N+1), no unauthorized actors. [WITNESSED: https://in-toto.io] [WITNESSED: https://slsa.dev/blog/2023/05/in-toto-and-slsa]

**Structuring principle (SLSA):** A SLSA Provenance attestation is an in-toto Statement with a SLSA-specific predicate: builder identity, build instructions, input parameters, environment variables, dependency digests, output artifact digest. Wrapped in a DSSE signed envelope. Four levels of increasing build-platform trustworthiness. [WITNESSED: https://slsa.dev/blog/2023/05/in-toto-and-slsa] [WITNESSED: https://mikael.barbero.tech/blog/post/2023-12-28-slsa-and-in-toto/]

An artifact without a signed attestation is the software equivalent of hearsay. [REPORTED: https://appsecuritystandards.org/glossary/provenance-attestation]

**Mapping:** A signed Link is a WITNESSED artifact — the step produced it directly, with cryptographic commitment to inputs and outputs. An artifact without a link is REPORTED — claimed provenance, unchallengeable. The SESSION LOG for a flow is the chain of Links.

**Worth adopting:** The "materials + products + digests" structure of a Link maps onto flow artifact metadata. The typed predicate inside a signed container (DSSE pattern) is a model for how a flow artifact header could carry verifiable identity without conflating format and content.

---

### 2F. Epistemic-Status Headers (Gwern, LessWrong)

**Structuring principle (Gwern):** Two orthogonal axes: Confidence (subjective probability the core thesis is correct, tagged as: Certain / Highly likely / Likely / Possible / Unlikely / Highly unlikely / Remote / Impossible) and Epistemic status / source type (Log, Emotional, Fiction, completion-status markers). Also: Importance on a 0–10 scale. These are independent. [WITNESSED: https://gwern.net/about]

Lineage: Muflax coined "epistemic state" tags → Gwern adapted → Scott Alexander converted to freeform prose disclaimers → LessWrong community diversified. [REPORTED: https://contentcreation.issarice.com/epistemic-status/]

**Structuring principle (LessWrong):** Freeform prose conveying one or more of: (a) degree of belief, (b) reasons for confidence ("written in a textbook" vs. "personal experiment"), (c) social stance ("what kind of discussion do I want?"). Separate concept: epistemic effort — "how much research went into this," distinct from "how confident am I." [REPORTED: https://forum.effectivealtruism.org/posts/bbtvDJtb6YwwWtJm7/epistemic-status-an-explainer-and-some-thoughts] [WITNESSED via snippet: https://www.greaterwrong.com/posts/oDy27zfRf8uAbJR6M/epistemic-effort]

**Mapping:** Gwern's "Log" category maps onto LOG. The distinction between "this is based on personal experiment" vs. "this is from documentation" is the WITNESSED/REPORTED split stated informally. Epistemic effort maps onto the depth of the observation backing the artifact.

**Worth adopting:** Confidence and source-type are orthogonal. An artifact can be WITNESSED but uncertain (I ran the test and it gave an ambiguous result), or REPORTED but high-confidence (the official spec clearly states). The protocol should carry both axes. This is a non-obvious design decision: the WITNESSED/REPORTED tag alone is not sufficient; confidence must also travel with the artifact.

---

### 2G. Zettelkasten Note Types

**Structuring principle:** Fleeting notes (temporary, unstructured, must be processed within a day or two — converted or discarded, never filed in the slip-box), Literature notes (reference stored in a reference manager with brief remarks, represent engagement with an external source), Permanent notes / Zettels (self-contained, written in the author's own words, understandable without external context, stored permanently, never discarded — the only notes that enter the slip-box), Structure notes (meta-notes organizing relationships between other notes). [WITNESSED: https://zettelkasten.de/posts/concepts-sohnke-ahrens-explained/] [WITNESSED: https://zettelkasten.de/introduction/]

The permanent note forces genuine understanding rather than copying: if you cannot restate it in your own words without context, it is not ready.

**Mapping:** Fleeting notes = ephemeral LOG entries during a live session. Literature notes = REPORTED (relayed from an external source). Permanent notes = processed output: WITNESSED if the synthesis came from direct observation, REPORTED if from literature. The key risk Zettelkasten exposes: when making a permanent note, attribution collapses into the author's voice. The protocol must prevent this collapse by always carrying the source tag on the artifact, not just at creation time.

**Worth adopting:** The lifecycle rule — at end-of-flow, the SESSION LOG is the permanent record; ephemeral intermediate notes can be discarded. The requirement that a permanent (WITNESSED or REPORTED) artifact is "self-contained without external context" maps onto the requirement that a flow artifact carries enough metadata to be re-verifiable without re-running the flow.

---

### 2H. Provenance in RAG and Retrieval Systems

**Standard practice:** Each document chunk carries metadata (filename, source URL, page/paragraph number, byte offsets, document ID) stored alongside the embedding vector. Retrieved chunks are returned with metadata intact. [REPORTED: https://milvus.io/ai-quick-reference/how-does-llamaindex-manage-document-metadata]

**LlamaIndex:** Nodes carry metadata and relationship information including a reference to their parent document via `index_id`. Adjacent chunks have PREV/NEXT relationship pointers. Custom metadata attached at ingest time usable as retrieval filters. [WITNESSED via snippet: https://milvus.io/ai-quick-reference/how-does-llamaindex-manage-document-metadata]

**RAGTrace (2025):** Visual evidence traceability with chunk-relink graphs. Three confidence annotations on generated text: blue for entities, green for well-supported content, orange for uncertain claims. Three implicit categories: well-supported (directly from retrieved context), uncertain (inferred or lightly supported), ungrounded / hallucinated. [WITNESSED: https://arxiv.org/html/2508.06056v1]

**TREC RAG Track (2025):** Required structured JSON where each answer sentence is explicitly linked to supporting citations — sentence-level citation, not document-level. [REPORTED: https://arxiv.org/pdf/2603.09891]

No mainstream RAG framework makes an explicit WITNESSED/REPORTED distinction. RAGTrace's three-way annotation is the closest. [WITNESSED: https://arxiv.org/html/2508.06056v1] [REPORTED: https://medium.com/@duckweave/the-provenance-checks-your-rag-stack-is-missing-c4a6f17bc3e4]

**Mapping:** A directly retrieved chunk is like WITNESSED — it came from a document read in this session. A fact synthesized across multiple chunks without explicit citation is like REPORTED. The protocol's WITNESSED/REPORTED distinction is a cleaner, higher-level formulation of the gap RAGTrace identifies.

**Worth adopting:** Claim-level (or sentence-level) citation rather than document-level. RAGTrace's three-level confidence annotation (well-supported / uncertain / ungrounded) is useful for SESSION LOG entries, which are WITNESSED but may contain uncertain synthesized claims.

---

### 2I. Agent Proof and Verification Schemes

**Evidence Tracing and Execution Provenance Survey (arXiv 2606.04990):** Six evidence source types: reasoning traces, retrieval traces, tool traces, memory traces, environment traces, multi-agent traces. Nine typed provenance relations: Support, Contradict, Invalidate, Derive, Depend-on, Trigger, Update, Use, Generate. Five granularity levels: Run-level, Step-level, Tool-call-level, Parameter-level, Claim-level. "Document-level citation is often too coarse for factual attribution." Direct observations (user inputs, environment states, tool outputs, retrieved documents) are immediate timestamped evidence. Derived or memorized information "reliability is dependent on source lineage rather than direct observation." [WITNESSED: https://arxiv.org/html/2606.04990v1]

**LEDGER (arXiv 2608.18398):** Three-layer architecture from a captured agent session: (1) Trace Records (bottom) — deterministic transcript parsing: raw prompts, tool calls, results, lifecycle events, timing; these are the anchors a reviewer can verify independently against the JSONL. (2) Evidence Nodes (middle) — groups of related trace records forming inspectable work units (action nodes: control, user_message, assistant_message, tool_call; artifact nodes: code, plots, tables, patches). (3) Workflow Nodes (top) — collections of evidence nodes organized by task phase: context, plan, inspect, execute, validate, claim. Six semantic edge types: frames, uses, produces, informs, checked_by, supports. All graph nodes retain "source pointers into the evidence substrate." Starting from a conclusion, following `support` edges leads to concrete Trace Records — the only entities verifiable against the original transcript. Session directory stores "hook payloads, transcript, and trace summary." [WITNESSED: https://arxiv.org/html/2608.18398]

**Scratchpad faithfulness problem:** Chain-of-thought / scratchpad reasoning may be post hoc — "better described as scratchpads that influence output rather than faithful transcripts." A flow's SESSION LOG is not equivalent to the model's actual reasoning; it is a surface transcript. [REPORTED: https://www.mindstudio.ai/blog/what-is-chain-of-thought-faithfulness-ai-reasoning]

**"Verify Before You Commit" (arXiv 2604.08401):** Four-step claim verification: claim identification, supporting evidence analysis, verification planning, faithful-tool verification. Forces the agent to locate concrete evidence in its observation log for each claim before committing to it. [REPORTED: https://arxiv.org/html/2604.08401]

**Signed Provenance (Zylos Research, 2026):** Each agent step appends a Trace Node containing: agent ID, model fingerprint, execution context hash, result hash, cryptographic signature, parent lineage reference. Forming a tamper-evident DAG rooted in a Signed Intent Envelope recording the original human request. [WITNESSED: https://engineeringagents.substack.com/p/provenance-as-the-chain-of-accountability]

**Mapping:** LEDGER's Trace Records are WITNESSED — directly grounded in the transcript. LEDGER's Workflow Nodes are REPORTED — summary and interpretation. The SESSION LOG is the per-session directory holding the raw transcript. LEDGER is the closest existing formal system to the flow artifacts protocol.

**Worth adopting:** LEDGER's source-pointer requirement on all higher-level artifacts — every non-Trace-Record node must carry a pointer back into the Trace Records it is derived from. This is the technical implementation of "chain of origin."

---

## Part 3: Session-ID-Centric Workflows

**Google Agent Development Kit (ADK) Artifact System:** Artifacts scoped by three identifiers: `app_name`, `user_id`, `session_id`. Plain filenames are session-scoped. Filenames prefixed with `"user:"` are user-scoped (cross-session). Automatic versioning assigns incremental version numbers per filename. Provenance via version history; no explicit audit log linking an artifact version to the session that produced it. [WITNESSED: https://adk.dev/artifacts/] [WITNESSED: https://irbox.github.io/adk-docs/artifacts/]

**Long-Running AI Agent Runtime (Slavadubrov, 2026):** Three time spans: thread (long-lived, keyed by `thread_id`), model session (one continuous context stretch), session (durable log of one run). Three-store pattern: Git for workspace state, checkpoint database for graph state, artifact store (S3/GCS) for large outputs. Artifact key schema: `(thread_id, checkpoint_id, artifact_name)` — the producing run (checkpoint) is baked into the artifact key, so provenance is never separated from the artifact reference. Debug bundle pattern: on failure, produce `/workspaces/${THREAD_ID}/_debug/` with full event-log dump, last successful state snapshot, OTLP-exported trace spans, tool-call timeline, workspace git diffs. [WITNESSED: https://slavadubrov.github.io/blog/2026/05/26/ai-agent-runtime/]

**Agent Artifact Store (Orellazri):** UUID-keyed artifact store; each artifact linked to a `conversation_id` via a `ConversationArtifact` join table. Conversation-level, not run-level; provenance at the execution level is not captured. [WITNESSED: https://orellazri.com/posts/building-artifacts-system-for-llm-data-agents/]

**Artifacta:** Artifact store where "agent, model, session, and timestamp travel with the link." Framing: "When someone asks 'where did this come from,' the page already answered." [REPORTED: https://artifacta.io/]

**AWS Well-Architected — Agentic AI Lens (AGENTSEC05-BP01):** Prescribes logging and decision artifact storage with consistent key schema: `(agent ID, session ID, timestamp, decision type)`. Tamper-evident artifact storage attributed to the original trigger. Queryable index for forensic capability. [REPORTED: https://docs.aws.amazon.com/wellarchivected/latest/agentic-ai-lens/agentsec05-bp01.html]

**LEDGER (cross-reference):** The only system reviewed that is explicitly session-centric and transcript-verifiable: per-session directory, transcript stored, all graph nodes retain source pointers back into the session evidence substrate. [WITNESSED: https://arxiv.org/html/2608.18398]

**Mapping:** Slavadubrov's artifact key schema, Google ADK's three-id scoping, and AWS's `(agent ID, session ID, timestamp, decision type)` all converge on the same design: embed the session/run id in the artifact key. None introduces the WITNESSED/REPORTED distinction. LEDGER is the exception — the only one that also distinguishes transcript-grounded from derived artifacts.

---

## Distilled Shortlist: Design-Relevant Patterns

Each pattern is stated as a concrete design decision. Sources are cited.

**Pattern 1 — Embed the flow short id in every artifact key.**
The producing flow's id must be part of the artifact's identity, not recoverable only by traversal. This is the consensus of MLflow, mem0, Slavadubrov, Google ADK, and AWS. Slavadubrov's `(thread_id, checkpoint_id, artifact_name)` is the tightest formulation — the artifact cannot exist without its provenance key. [REPORTED: https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/hyperparameter-tuning/part1-child-runs/] [WITNESSED: https://slavadubrov.github.io/blog/2026/05/26/ai-agent-runtime/] [WITNESSED: https://adk.dev/artifacts/]

**Pattern 2 — Subflows get their own id; parent-child is a spawn-edge graph, not a naming convention.**
OpenAI Codex CLI's `ThreadId` DAG via `upsert_thread_spawn_edge` demonstrates that subagent parentage must be a data structure, not a filename prefix. The session ID is embedded in the JSONL, not derived from the filename. Subflows can be resumed independently. [WITNESSED: https://deepwiki.com/openai/codex/4.4-session-resumption] [WITNESSED: https://github.com/openai/codex/issues/24948]

**Pattern 3 — Every derived artifact carries an explicit list of its source sessions.**
Zep's episode-list on every fact — multi-source facts accumulate the full list of contributing episodes — is the cleanest implementation of chain-of-origin. The chain is not reconstructed at query time; it is written at construction time. [WITNESSED: https://blog.getzep.com/how-zep-tracks-provenance-in-agent-memory/]

**Pattern 4 — The SESSION LOG is a verbatim, append-only primary source; all WITNESSED and REPORTED artifacts are derived from it.**
LEDGER's Trace Record layer formalizes this: deterministic transcript parsing produces ground-truth anchors. Higher-level artifacts must carry source pointers into the Trace Records. Starting from any claim, following provenance edges must reach a Trace Record. [WITNESSED: https://arxiv.org/html/2608.18398]

**Pattern 5 — WITNESSED and REPORTED are the universal minimum epistemic binary.**
Cross-linguistic evidentiality typology validates the two-term system (witnessed vs. non-witnessed) as the baseline. The most common evidential system in human language is exactly this binary. The inferential category ("I deduced this from observations I made") is a natural third term; whether the protocol needs it depends on how often a flow produces inferences from its own observations distinct from relayed claims. [WITNESSED: https://en.wikipedia.org/wiki/Evidentiality]

**Pattern 6 — Confidence and source-type are orthogonal; both must travel with the artifact.**
Gwern's two-axis model: source-type (Log / personal experiment / documentation) and confidence (Certain → Impossible) are independent. An artifact can be WITNESSED but uncertain, or REPORTED but high-confidence. The protocol must carry both axes; the WITNESSED/REPORTED tag alone is insufficient. [WITNESSED: https://gwern.net/about]

**Pattern 7 — WITNESSED means "independently re-verifiable by a later flow"; REPORTED means "chain-dependent."**
The law-of-evidence "challengeability" criterion operationalizes the distinction without philosophical overhead. WITNESSED = a later flow can re-run or re-read the same thing independently. REPORTED = the challenge must trace back through the relaying agent chain. [WITNESSED: https://en.wikipedia.org/wiki/Hearsay]

**Pattern 8 — Source pointers must survive artifact promotion; attribution must not collapse into the author's voice.**
Zettelkasten's provenance risk: when a fleeting note becomes a permanent note, attribution collapses into the author's voice. The protocol must enforce that the WITNESSED/REPORTED tag and source citation are part of the artifact's permanent identity, not just its creation-time metadata. [WITNESSED: https://zettelkasten.de/posts/concepts-sohnke-ahrens-explained/]

**Pattern 9 — Claim-level citation, not document-level.**
The evidence tracing survey and TREC RAG Track both conclude that document-level citation is too coarse. "Document-level citation is often too coarse for factual attribution." [WITNESSED: https://arxiv.org/html/2606.04990v1] [REPORTED: https://arxiv.org/pdf/2603.09891] Each claim in a REPORTED artifact should cite its specific source claim or passage, not just the source document.

**Pattern 10 — The LangSmith `dotted_order` encoding for machine-readable chain-of-origin.**
A single sortable string encodes the full ancestor chain: `<timestamp>Z<uuid>.<timestamp>Z<uuid>...`. Root UUID = first segment; terminal UUID = last segment. Provenance reconstruction requires no separate graph query — the string carries the full chain. Applicable to the flow's short id chain: `<parent_short_id>.<subflow_short_id>`. [WITNESSED: https://docs.langchain.com/langsmith/run-data-format]

**Pattern 11 — The "materials + products + digests" structure of an in-toto Link as the WITNESSED artifact schema.**
A WITNESSED artifact records: (a) what was consumed (materials, with digests), (b) what was produced (products, with digests), (c) who executed the step (flow short id), (d) what the step was (the observation activity). This is more verifiable than a prose description and directly maps to in-toto's formal supply-chain model. [WITNESSED: https://in-toto.io] [WITNESSED: https://slsa.dev/blog/2023/05/in-toto-and-slsa]

**Pattern 12 — W3C PROV vocabulary for interoperability.**
`hadPrimarySource` is the formal name for the WITNESSED relationship; `wasDerivedFrom` for REPORTED. `wasGeneratedBy` (Activity) + `wasAttributedTo` (Agent = the flow) + `used` (Entity observed) form the standard triple for a WITNESSED artifact. Using this vocabulary costs nothing and enables interoperability with existing provenance tools. [WITNESSED: https://www.w3.org/TR/prov-o/]

**Pattern 13 — Temporal invalidation linked to the superseding source.**
Zep's `valid_at` / `invalid_at` model: a later episode can mark a fact invalid, with the superseding episode as part of the record. For the flow artifact index, a WITNESSED claim that is later contradicted should carry both the original observation and the superseding observation, not silently overwrite. [WITNESSED: https://blog.getzep.com/how-zep-tracks-provenance-in-agent-memory/]

**Pattern 14 — The debug bundle pattern: per-flow `_debug/` directory on failure.**
Slavadubrov's practice: on failure, produce a directory keyed by thread ID containing the full event-log dump, last successful state snapshot, trace spans, tool-call timeline, and workspace git diffs. This maps directly to a per-flow directory containing all session artifacts. The "on failure" trigger is one instance of the more general rule: the per-flow directory is always populated; `_debug/` is just the failure-time artifact bundle. [WITNESSED: https://slavadubrov.github.io/blog/2026/05/26/ai-agent-runtime/]

**Pattern 15 — LEDGER as the nearest existing system; adopt its three-layer source-pointer requirement.**
LEDGER (arXiv 2608.18398) is the only reviewed system that is simultaneously: (a) session-centric, (b) transcript-verifiable, and (c) distinguishes transcript-grounded from derived artifacts. Its source-pointer requirement — every non-Trace-Record node must carry a pointer back into the Trace Records it derives from — is the technical implementation of the chain-of-origin rule. [WITNESSED: https://arxiv.org/html/2608.18398]

---

## Unknowns and Open Questions

The following were researched but not resolved:

**Unknown 1:** Whether any existing system explicitly labels artifacts with a three-term vocabulary (WITNESSED / REPORTED / LOG or equivalent) rather than inferring it from structural position. No such system was found. LEDGER comes closest but does not use this vocabulary.

**Unknown 2:** Whether the inferential category (deduced from observations made, but not directly seen) warrants a third tag distinct from WITNESSED and REPORTED in the protocol's use cases. The linguistic evidence says it is a real and non-trivial distinction. Whether it matters in practice depends on how often flows produce inference artifacts vs. direct observation artifacts.

**Unknown 3:** The exact Claude Code session file layout for subagents (whether a subagent's session file carries a `parentSessionId` analogous to Codex CLI's `ThreadId` spawn edge). The reviewed sources describe the JSONL format at the message level (`uuid`/`parentUuid`) but do not describe cross-session parent linking. Treat as unknown; do not assume it matches Codex CLI's model without verification.

**Unknown 4:** Whether the `verified/` ledger envisioned in the psyche (see `psyche/Vision/verifiedInformation.md`) is intended to be a subset of the flow artifacts protocol or a separate system. The psyche's ruling is that the ledger lives at `verified/` and re-verifications append. Whether each `verified/` entry is a WITNESSED artifact in the flow artifacts sense, filed under the verifying flow's short id, is not stated and should be resolved before implementation.
