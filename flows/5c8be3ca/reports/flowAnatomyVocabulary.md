# Flow Anatomy and LLM-Based Engineering Vocabulary
## Research Report — 2026-08-21

Commissioned by design session `5c8be3ca`. Immediate spark: the psyche asked "what is pronouncement? Is that an established vocabulary?" while answering open forks in a flow-artifact draft. The broader charge: establish the anatomy of the flow and LLM-based engineering — a vocabulary for the parts of a model session and the acts around it.

Claims below are labeled by origin. Every statement about external sources is a claim based on the cited URL. Observations from the psyche records are observations. Hypotheses are marked. Unknowns are admitted.

---

## Part 1: Decision-Act Vocabularies in Established Engineering and Governance Processes

### Architecture Decision Records (ADR)

Source: Michael Nygard's 2011 essay at [cognitect.com](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) and subsequent community practice documented at [glama.ai](https://glama.ai/mcp/servers/@dylanmarriner/MCP-server/blob/d9961c1620825d604a398471304b8a5d32793ae0/adr/STATUS_TAXONOMY.md).

ADR lifecycle states: **Proposed** → **Accepted** → **Deprecated** or **Superseded**.

The act of a decision becoming binding is called **acceptance** (Proposed → Accepted). No single word names the moment of acceptance in the original essay; community templates show a status field that changes. The record is then treated as immutable: corrections to typos are permitted, but conclusions are not edited — a reversal requires a new ADR that supersedes the old.

Named acts: propose, accept, deprecate, supersede. The act of making a decision binding is "accepting" the ADR. No "pronouncement" terminology appears in this tradition.

### IETF RFC Lifecycle

Source: RFC 2026 at [datatracker.ietf.org](https://datatracker.ietf.org/doc/html/rfc2026) and lifecycle materials at [rfc-editor.org](https://www.rfc-editor.org/materials/lifecycle82.pdf).

States (Standards Track): Internet-Draft → **Proposed Standard** → **Internet Standard**. Non-Standards-Track: Informational, Experimental, Historic.

Every RFC begins as an Internet-Draft. Many never advance. The act of moving a draft to Proposed Standard is "publication as an RFC" — no single verb names the approval moment in common usage. The community says a document is "published" or "adopted" as a standard. "Ratification" is not used. "Pronouncement" does not appear.

### W3C Process

Source: [w3.org standards types](https://www.w3.org/standards/types/) and [W3C Recommendation Track overview](https://www.w3.org/2004/02/Process-20040205/tr.html).

States: Working Draft → Candidate Recommendation → Proposed Recommendation → **W3C Recommendation**.

The Director determines that W3C member review supports the specification, and it is "published" as a Recommendation. The act of approval is called "endorsement" at the Advisory Committee level; the final document status is "Recommendation." No "pronouncement" terminology. No "ratification" as the formal act-name (though informal usage of "ratify" appears in discussions).

### ISO Standards Ratification

Source: [asq.org Standards 101](https://asq.org/quality-resources/standards-101) and [ISO/IEC Guide summaries](https://share.ansi.org/Shared%20Documents/News%20and%20Publications/Links%20Within%20Stories/ISO+IEC+Guide+59-2019.pdf).

ISO uses **approval** as the formal act name. A draft International Standard must be approved by two-thirds of participating member bodies and 75% of all members that vote. Within ISO's internal governance, "ratification" is used for subcommittee decisions submitted to the technical management board. The final phase is "approval" then "publication."

Observation: across ADR, IETF, W3C, and ISO, the formal act of a drafted statement becoming binding is named differently by each tradition — acceptance, publication, endorsement, approval — but none uses "pronouncement."

### Legal Usage: Ruling, Judgment, Holding, Pronouncement

Source: [USLegal definitions](https://definitions.uslegal.com/p/pronouncement-of-judgment/), [LawProse](https://lawprose.org/lawprose-lesson-165-ruling-vs-opinion-vs-judgment-etc/), [Wikipedia — Holding](https://en.wikipedia.org/wiki/Holding_(law)).

**Pronouncement** (legal): "Pronouncement of judgment is the rendition of judgment by the court. It is the rendition of judgment and direction for the entry thereof." (USLegal, from California case law.) A court of appeal "pronounces" its judgment when it directs entry — ordinarily when its opinion is filed. Pronouncement describes the formal act of announcing a decision and directing it into the official record. It is the act, not the resulting state.

**Judgment**: The court's decision regarding rights and liabilities; the outcome (affirmed, reversed, remanded).

**Ruling**: The overall decision — on a point of law or on the whole case. A ruling is the judge's final decision. In LawProse usage, a ruling is what a trial judge makes; the appellate court issues an opinion; the judgment is the official court document.

**Holding**: The core legal principle established — the applied rule of law for future precedent. Different from the ruling; the ruling is what was decided, the holding is the reason it was decided and its precedential scope.

Assessment: **"pronouncement" is an established legal term**. Its established meaning — the formal act of an authority declaring a decision and directing its entry into the official record — matches what the psyche uses it for in design records. The act closes an open question; the pronounced statement becomes the official record.

### Parliamentary and Ecclesiastical Usage

Parliamentary: Terms in use include "enacted," "ratified," "resolved," "adopted." [Congress.gov glossary](https://www.congress.gov/help/legislative-glossary) and state legislature glossaries do not list "pronouncement" as a formal parliamentary act. "Ratification" is used specifically for constitutional amendments; "enactment" for bills signed into law.

Ecclesiastical: Source: [encyclopedia.com — Pronouncements, Papal and Curial](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/pronouncements-papal-and-curial) and [UST Paul LibGuide on Papal Documents](https://ustpaul.libguides.com/c.php?g=522115&p=3569976).

"Papal pronouncements" is established vocabulary. Papal documents include apostolic constitutions (the most solemn, defining dogmas or altering canon law), declarations, exhortations, and decrees. The umbrella term "pronouncements" covers documents in which the Pope formally declares the Church's position. The act of issuing a solemn papal statement is "promulgating" it — making it official and binding. "Pronouncement" in ecclesiastical usage names the class of such formal declarations.

"Promulgation" (ecclesiastical and legal) is the act of making a rule officially known and operative. Distinct from "pronouncement": promulgation is the publication step; pronouncement can precede promulgation.

Synthesis: Across law and ecclesiastical tradition, "pronouncement" is established vocabulary for the formal, authoritative declaration of a decision by a legitimate authority. The term is not used in software engineering or LLM-engineering literature.

---

## Part 2: Anatomy of LLM-Based Engineering

### Flow Engineering (AlphaCodium / Qodo)

Source: [arxiv 2401.08500](https://arxiv.org/abs/2401.08500) and [Qodo blog](https://www.qodo.ai/blog/qodoflow-state-of-the-art-code-generation-for-code-contests/).

AlphaCodium (January 2024, Qodo research team) coined "flow engineering" as the subtitle of the paper "Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering." The paper describes AlphaCodium as "a test-based, multi-stage, code-oriented iterative flow."

Their definition: flow engineering is the structured approach of breaking code generation into multiple distinct stages — self-reflection, reasoning, iterative code generation with test feedback, and error correction — rather than issuing a single well-crafted prompt. The flow is deterministic in structure, non-deterministic in model execution.

Community extension (source: [leewayhertz.com](https://www.leewayhertz.com/flow-engineering/), [Medium — Filip K](https://medium.com/@itsfilipk/flow-engineering-the-missing-piece-in-llm-app-development-a27f2838328f)):

> Flow engineering is the process of splitting, separating, and simplifying LLM prompts and tasks by forcing the application to flow under a clearly defined set of possible states and transitions, similar to a finite state machine.

Named components in the AlphaCodium flow: pre-processing stage (problem reflection, public test reasoning, possible solutions generation, solution ranking), code iteration phase (generate → run tests → fix → repeat). No standard vocabulary for the parts of a "flow" has emerged from this tradition.

Assessment: Qodo's "flow engineering" names the practice of multi-stage structured pipelines contrasted with single-prompt engineering. Their "flow" names the pipeline or process, not a single bounded model session. This is a different sense than the psyche's use of "flow."

### Context Engineering

Source: [philschmid.de](https://www.philschmid.de/context-engineering), [LangChain blog](https://www.langchain.com/blog/the-rise-of-context-engineering), [promptingguide.ai](https://www.promptingguide.ai/guides/context-engineering-guide), [kubiya.ai](https://www.kubiya.ai/blog/context-engineering-ai-agents).

Tobi Lütke (Shopify CEO) tweet, June 18 2025 (cited widely): "context engineering is the art of providing all the context for the task to be plausibly solvable by the LLM."

Broader practitioner definition: context engineering is the practice of designing systems that curate and maintain the optimal set of tokens an LLM sees during inference — including the initial prompt, tool definitions, retrieved documents, memory, message history, and structured inputs. It positions prompt engineering as a subset.

Key claim (source: kubiya.ai): "The single biggest predictor of AI agent success in 2025 is not model selection. It's context engineering."

Note: context engineering is now a widely used term with no single standards body definition, but with clear community convergence on the meaning above.

### Anatomy of One LLM Session

Source: [Letta blog — Anatomy of a Context Window](https://www.letta.com/blog/guide-to-context-engineering/), [Anthropic engineering blog on effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [atlan.com context structuring guide](https://atlan.com/know/how-to-structure-context-for-llm-applications/).

Named parts of a context window / session in practitioner literature:

**Kernel context** (system-managed):
- **System prompt** — defines agent behavior, architectural constraints; at harness injection
- **Tool schemas** — specifications of available tool interfaces
- **Memory blocks** — persistent units of context (long-term or working memory)
- **Files and artifacts** — accessible data files; artifacts are editable files allowing iterative modification

**User context** (message buffer):
- **User messages** — the typed prompts
- **Assistant messages** — model responses
- **Tool calls** — structured invocations of tools
- **Tool returns** — results returned from tools

**Turn**: one exchange — one user message plus the model's response. The term "turn" is in common use.

**Context window**: everything the model can see at a single inference call. Not synonymous with session; the context window loads fresh at each inference.

**Conversation / Session**: the full sequence of turns. "Session" is common but contested — it implies a bounded timespan, and multi-turn agent sessions can span many inference calls.

Note from [Letta](https://www.letta.com/blog/guide-to-context-engineering/): "The context window and memory are not the same thing — the context window is the working space an LLM uses during a single session, while memory is information stored outside the model, maintained by the system, and available across sessions and steps."

### Observability Terminology

#### LangSmith

Source: [LangChain observability concepts](https://docs.langchain.com/langsmith/observability-concepts), [statsig perspectives](https://www.statsig.com/perspectives/langsmith-tracing-debug-llm-chains).

- **Run**: every unit of work an agent performs — a model call, tool invocation, or retrieval. The atomic unit.
- **Trace**: a collection of runs for one top-level operation, structured as a tree (root run + child runs). Records the full sequence from input to final output.
- **Thread**: links multiple traces from a multi-turn session together.

Structure: a trace is a tree of runs; a thread is a sequence of traces.

#### OpenTelemetry GenAI Semantic Conventions

Source: [opentelemetry.io GenAI blog 2026](https://opentelemetry.io/blog/2026/genai-observability/), [greptime.com analysis](https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions), [openobserve.ai guide](https://openobserve.ai/blog/opentelemetry-for-llms/).

Named span types:
- **`invoke_agent`** — top-level span for one agent interaction (the multi-turn session boundary)
- **`chat`** — span for one LLM call (one model inference)
- **`execute_tool`** — span for one tool invocation

Session vs. single call: individual `chat` spans nest under the parent `invoke_agent` span. The `invoke_agent` span encompasses the complete multi-turn session or agent interaction sequence.

Key attributes: `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.finish_reasons`, `gen_ai.system_instructions`, `gen_ai.input.messages`, `gen_ai.output.messages`.

Note: OpenTelemetry does not define "session" as a formal span type. Multi-turn conversation grouping requires application-level instrumentation (e.g., a session identifier on spans) rather than a native session span concept.

#### Anthropic Agent SDK (2025-2026)

Source: [augmentcode.com SDK analysis](https://www.augmentcode.com/guides/anthropic-agent-sdk-what-ships-vs-what-you-build), [luhuidev.medium.com architecture overview](https://luhuidev.medium.com/anthropics-2026-agent-harness-architecture-from-agent-loop-to-agent-runtime-6da6db4f3f47).

Named terms in the SDK and associated architecture: **Session**, **Harness**, **Sandbox**, **Credentials**, **Tool Protocol**, **Context Builder**, **Trace**, **Eval**. Sessions persist and export to external storage. OpenTelemetry traces, metrics, and logs export through documented configuration.

### Human-Agent Act Vocabulary: Approval, Sign-Off, Ratify

Source: [augmentcode spec-driven development guide](https://www.augmentcode.com/guides/what-is-spec-driven-development), [thoughtworks.com spec-driven development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices).

In spec-driven development, human oversight occurs at phase boundaries. The verbs used: **review**, **approve**, **sign off**. No single canonical term has emerged for the act of a human authority finalizing a design decision in LLM-engineering literature. "Approve" is most common; "accept" is also used (mirroring ADR vocabulary); "ratify" appears occasionally in governance-heavy contexts.

Claim: the search found no established single-word term in LLM-engineering literature for the act of an authority reviewing a proposed statement and making it official.

### Verification Witnesses in Formal Software Engineering

Source: [ACM TOSEM — Verification Witnesses](https://dl.acm.org/doi/full/10.1145/3477579), [Springer — Safeguarding with Witnesses](https://link.springer.com/chapter/10.1007/978-3-031-73741-1_22).

In formal software verification (the SV-COMP community), "witness" is an established term. A verification witness is a machine-readable artifact that supports a verification claim, allowing independent reproduction of the result. The contrast is between a bare claim (true/false without evidence) and a witnessed result (with supporting artifact).

This is a narrow formal verification usage, not general software engineering vocabulary. It is, however, the closest established parallel to the psyche's witness/claim distinction.

---

## Part 3: Published Attempts at a Full Anatomy or Ontology

No fully canonical published anatomy or ontology of LLM/agent-based software engineering was found in this research. Several partial efforts exist:

1. **SDLC-wide LLM taxonomy (2025)** — an academic survey mapping LLM capabilities and tasks across SDLC phases (requirements, architecture, design, implementation, etc.), published in the International Journal of Advanced Computer Science. Covers tasks and risks but not the internal anatomy of one session or the vocabulary of acts between human and agent.

2. **Letta's "Anatomy of a Context Window"** (cited above) — the most complete single practitioner document on the named parts of a session's context. Introduces the kernel/user-context split, memory blocks, message buffer. Not a formal standard.

3. **OpenTelemetry GenAI Semantic Conventions** — the closest thing to a standard vocabulary for what happens inside one LLM call and across a multi-agent interaction. Covers spans, attributes, and metrics but not the human acts (approve, ratify, pronounce) or the artifact types (report, distillation).

4. **AlphaCodium / Qodo flow engineering** — a vocabulary for the stages of a structured LLM pipeline, not for the human-model interaction acts.

5. **Anthropic context engineering guidance** (published November 2025) — practitioner guidance on context management, state, and handoff artifacts. Uses terms such as "session," "trace," "eval," "handoff artifact."

Finding: there is no published ontology that covers both the internal anatomy of an LLM session and the decision-act vocabulary (the acts by which a human authority closes a design question). This gap is exactly what our internal vocabulary is attempting to fill.

---

## Part 4: Comparative Table — Internal Terms vs Established Terms

| Our term | Established nearest term(s) | Establishment status | Notes |
|---|---|---|---|
| **flow** | session (AI industry); invoke_agent span (OTel); conversation | Partially established. "Session" is the common AI term; "flow" in our sense (one bounded LLM context) is our coinage. AlphaCodium's "flow" names a structured multi-stage pipeline, not one bounded context. | Psyche-defined: "a flow is one bounded LLM context." Distinct from industry "flow engineering." |
| **subflow** | subagent; child run; nested span | Not established in LLM literature with this meaning. Common in workflow/BPM contexts (subprocess, sub-workflow). | Our coinage. Parallel concepts: child run (LangSmith), nested invoke_agent span (OTel). |
| **transcript** | trace (LangSmith, OTel); session log; conversation log; JSONL session file | Partially established. "Trace" is the observability standard; "transcript" evokes the conversation-level, human-readable quality more than raw telemetry. | Psyche-defined term. Anchored in vocabulary skill. Closer to a human-readable conversation log than a telemetry trace. |
| **witness** (observation of the thing itself) | verification witness (formal methods); first-hand observation | Established in formal software verification (SV-COMP), legal/everyday meaning. Not established in LLM engineering vocabulary with our specific meaning. | Our epistemological usage (observation vs. claim) has analogs in formal verification. Legitimate coinage for our context. |
| **claim** (what someone says about it) | claim (formal verification); assertion; statement | Established in formal verification (claim = bare true/false without supporting evidence). Everyday use. | Consistent with established usage. |
| **session log** | session file; trace; run log | "Session" and "log" are each established; the compound is ours but natural. | Psyche-defined as self-witness — the flow's own record of itself. |
| **report** | report (general); test report; audit report | Established generically. No specific meaning in LLM engineering. | Our usage: an artifact produced by a flow for another flow or the psyche. Generic term, unambiguous. |
| **distillation** | re-articulation; synthesis; consolidation | Not established in this sense. "Distillation" in ML means knowledge distillation (training a smaller model from a larger one) — entirely different. | Our coinage. The act of re-articulating psyche records into a unified pronounced statement. No clash with ML usage in our context. |
| **dispatch** | task assignment; delegation; schedule; dispatch (event dispatch in software) | "Dispatch" is established in software as event routing. As a management act (directing a subflow to work), it is natural but not standardized in LLM engineering. | Consistent with standard software vocabulary. Unambiguous in context. |
| **ruling** | decision; holding (law); accepted ADR; governance decision | "Ruling" is established in law (a judge's decision). In ADR: "accepted decision." In LLM-engineering governance literature: no single established term. | Our use of "ruling" mirrors legal usage accurately. The psyche issues rulings; flows act on them. Well-motivated. |
| **pronouncement / pronounced statement** | pronouncement of judgment (law); papal pronouncement (ecclesiastical); acceptance (ADR) | **Established in law and ecclesiastical contexts.** Not established in LLM engineering. | See analysis below. |

---

## Part 5: Candidate Anatomy — Named Parts and Named Acts

### Named Parts of a Flow

The following anatomy is proposed. Established vocabulary is noted; our coinages are marked.

**The flow itself**
- **Flow** [our coinage, psyche-defined] — one bounded LLM context: its system prompt (top stratum), typed prompts (middle stratum), tool calls and returns (bottom stratum), and all model responses within one continuous session. Contrast with AlphaCodium's "flow" (a structured pipeline). Our usage is not in conflict but is narrower.
- **Subflow** [our coinage] — a flow spawned within a parent flow to perform a delegated task. The parent flow is liable for its subflows.
- **Transcript** [our coinage, anchored in vocabulary skill] — the harness's whole-session file: the raw record of a flow, containing every turn, tool call, and model response. Nearest established term: trace (OTel/LangSmith), session log.

**Inside the flow (anatomy of one session)**
- **System prompt / top stratum** [established: system prompt; our coinage for the strata vocabulary] — the harness-composed content at the highest context authority. Contains universal invariants, spirit, skills.
- **Turn** [established] — one user message plus the model's response.
- **Tool call** [established] — a structured invocation of an external tool within a turn.
- **Tool return** [established] — the result delivered back from a tool, entering at the bottom stratum.
- **Context window** [established] — everything the model sees at one inference call.
- **Artifact** [established generically; LLM-engineering usage: files the agent creates or edits] — a produced file, report, or structured output. Our "report" is one type.

**Flow outputs and records**
- **Session log** [our term] — the flow's running self-record, created at first prompt. A self-witness.
- **Report** [established generically] — a structured artifact produced by a subflow for its parent or for the psyche.
- **Distillation** [our coinage] — a re-articulated, unified statement produced from multiple psyche records, proposed to the psyche for pronouncement. Not knowledge distillation (ML).

**Psyche-related record types**
- **Witness** [our epistemological usage; parallel to formal verification usage] — a direct observation of the thing itself, not a claim about it. A flow verifying behavior in code produces a witness; relaying what the docs say produces a claim.
- **Claim** [consistent with formal verification and general usage] — a statement about something, without direct observation. Claims require citation; witnesses are the observation.

### Named Acts Between Psyche and Flow

The following named acts appear in our records and in external literature. Established status is assessed.

**Psyche-to-flow acts**
- **Dispatch** [our usage; established in software event dispatch] — the psyche or a parent flow assigns work to a subflow. Maps to "task assignment" or "delegation" in other traditions.
- **Ruling** [our usage; established in law] — the psyche decides a design question. A ruling closes an open question with authority. Maps to "accepted decision" (ADR) or "judgment" (law).
- **Pronouncement** [our usage; established in law and ecclesiastical tradition] — the psyche formally approves a drafted statement, directing it into the official record. The pronounced statement becomes binding. See analysis below.

**Flow-to-psyche acts**
- **Proposal** [established] — a flow presents a drafted statement to the psyche for review. Maps to "Proposed" in ADR lifecycle; "Internet-Draft" in IETF.
- **Report** (as act) [established generically] — a flow delivers findings or results to the psyche or parent flow.
- **Distillation proposal** [our coinage] — a flow proposes a re-articulated unified statement to replace a set of psyche records.

**Human-in-the-loop acts (from spec-driven development literature)**
- **Review** [established] — human examination of a proposed artifact or decision.
- **Approve** [established] — human authorization of a proposed artifact or decision. The most common term in spec-driven development literature.
- **Sign off** [established, informal] — colloquial equivalent of approve.
- **Accept** [established in ADR tradition] — a proposed decision becomes binding; the ADR moves to Accepted status.
- **Ratify** [established in constitutional and parliamentary law] — formal confirmation of a previously agreed decision, especially for constitutional changes. Less common in engineering.

---

## Part 6: Is "Pronouncement" Established? Should We Keep It?

**The finding**: "Pronouncement" is established vocabulary in law and ecclesiastical tradition, not in LLM-engineering or software-engineering literature.

In law: "pronouncement of judgment" is the formal act of a court declaring its decision and directing it into the official record. The act is transitive — the court pronounces a judgment; the judgment is pronounced.

In ecclesiastical tradition: "papal pronouncements" are solemn formal declarations by an authority with governing weight.

In neither ADR, IETF, W3C, ISO, parliamentary, nor LLM-engineering literature does "pronouncement" appear as the term for the act of a human authority approving a drafted statement and making it official.

**Assessment for our usage**: The psyche uses "pronounced statement" to name a statement that has been reviewed by the psyche and approved, closing a design question. This maps closely to the legal meaning: the authority reviews a proposed judgment, declares it, and directs its entry into the record. The analogy is tight.

Alternatives examined:
- **acceptance** (ADR vocabulary) — describes the resulting state (the statement is now "accepted"), not the act of declaring it. Less expressive of the moment.
- **ratification** — parliamentary connotation; implies a previously agreed-upon thing being formally confirmed, often after the fact. Not quite right for the psyche's act of reviewing and approving a new proposal.
- **adoption** — legislative flavor; a body "adopts" a resolution. Less personal authority, more collective.
- **promulgation** — the act of making a rule official and public (ecclesiastical and legal). Accurate but more formal, less common. Promulgation follows pronouncement in church law.
- **holding** — the legal principle established by a ruling. A holding is what was decided as precedent, not the act of deciding. Not quite right.

**Conclusion**: "Pronouncement" earns its place. It is the only term examined that precisely captures the act of an authority formally declaring a drafted statement into the official record as binding. It has legal precedent behind it. The word "pronounced" in our records correctly describes a statement the psyche has spoken into official existence. No better-established word for this specific act exists in the traditions surveyed; the alternatives miss the moment of declaration.

The one refinement the evidence supports: our use of "pronounce" and "pronounced" as verbs and adjectives is well-motivated, but we should be clear in skills that we are borrowing legal vocabulary deliberately, not LLM-engineering vocabulary, because no LLM-engineering vocabulary exists for this act.

---

## Summary of Key Findings

1. "Pronouncement" is established in law (pronouncement of judgment) and ecclesiastical tradition. It is not used in software engineering or LLM engineering. Our use is legitimate, well-motivated by the legal analogy, and the best available word for the specific act.

2. Across ADR, IETF, W3C, and ISO, the act of making a drafted decision binding is called acceptance, publication, endorsement, or approval — but the terms differ by tradition and none has the personal-authority flavor of "pronouncement."

3. "Flow engineering" as coined by AlphaCodium/Qodo (2024) means structured multi-stage LLM pipelines, not one bounded model session. Our psyche-defined "flow" (one bounded LLM context) is our own coinage; it does not conflict but is narrower.

4. The observability community has the most developed session vocabulary: LangSmith's run/trace/thread and OpenTelemetry's chat/invoke_agent/execute_tool spans. None of these name the human acts (approve, ratify, pronounce).

5. No published anatomy or ontology covers both the internal parts of an LLM session and the human-agent decision-act vocabulary. This gap is what our vocabulary is filling.

6. "Witness" (observation vs. claim) has a parallel in formal software verification but is our epistemological framing applied to LLM engineering. "Distillation" is our coinage with no conflict. "Dispatch" and "ruling" are well-grounded in existing vocabulary.

7. The term "transcript" for the harness session file is our coinage; "trace" is the established observability term. "Transcript" preserves the human-conversation quality that "trace" does not.

---

## Sources

- [Cognitect — Documenting Architecture Decisions (Nygard 2011)](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR Status Taxonomy](https://glama.ai/mcp/servers/@dylanmarriner/MCP-server/blob/d9961c1620825d604a398471304b8a5d32793ae0/adr/STATUS_TAXONOMY.md)
- [RFC 2026 — IETF Standards Process](https://datatracker.ietf.org/doc/html/rfc2026)
- [IETF RFCs overview](https://www.ietf.org/standards/rfcs/)
- [W3C Standards Types](https://www.w3.org/standards/types/)
- [W3C Recommendation Track Process (2004)](https://www.w3.org/2004/02/Process-20040205/tr.html)
- [ASQ Standards 101](https://asq.org/quality-resources/standards-101)
- [USLegal — Pronouncement of Judgment](https://definitions.uslegal.com/p/pronouncement-of-judgment/)
- [LawProse Lesson 165 — Ruling vs. Opinion vs. Judgment](https://lawprose.org/lawprose-lesson-165-ruling-vs-opinion-vs-judgment-etc/)
- [Wikipedia — Holding (law)](https://en.wikipedia.org/wiki/Holding_(law))
- [Encyclopedia.com — Pronouncements, Papal and Curial](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/pronouncements-papal-and-curial)
- [UST Paul LibGuide on Papal Documents](https://ustpaul.libguides.com/c.php?g=522115&p=3569976)
- [AlphaCodium paper — arxiv 2401.08500](https://arxiv.org/abs/2401.08500)
- [Qodo blog — Flow Engineering](https://www.qodo.ai/blog/qodoflow-state-of-the-art-code-generation-for-code-contests/)
- [LeewayHertz — What is flow engineering?](https://www.leewayhertz.com/flow-engineering/)
- [Tobi Lütke context engineering definition — philschmid.de](https://www.philschmid.de/context-engineering)
- [LangChain — The rise of context engineering](https://www.langchain.com/blog/the-rise-of-context-engineering)
- [Letta — Anatomy of a Context Window](https://www.letta.com/blog/guide-to-context-engineering/)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [LangChain LangSmith — Observability concepts](https://docs.langchain.com/langsmith/observability-concepts)
- [OpenTelemetry GenAI blog 2026](https://opentelemetry.io/blog/2026/genai-observability/)
- [Greptime — OpenTelemetry GenAI conventions](https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions)
- [Augmentcode — Spec-driven development](https://www.augmentcode.com/guides/what-is-spec-driven-development)
- [Thoughtworks — Spec-driven development 2025](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [ACM TOSEM — Verification Witnesses](https://dl.acm.org/doi/full/10.1145/3477579)
- [Augmentcode — Anthropic Agent SDK](https://www.augmentcode.com/guides/anthropic-agent-sdk-what-ships-vs-what-you-build)
