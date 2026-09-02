# Flow Composition Ontologies: How the Bleeding Edge Divides Agentic Systems into Thinking Units (2024–2026)

Report for flow b9f4f6. Sourced claims carry URLs and dates; training-knowledge claims and inferences are labelled.

---

## 1. Anthropic: "Building Effective Agents" Workflow Patterns

**Source:** [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents), Anthropic, December 2024.

### Key distinction

Anthropic separates **workflows** ("systems where LLMs and tools are orchestrated through predefined code paths") from **agents** ("systems where LLMs dynamically direct their own processes and tool usage"). The recommendation: "finding the simplest solution possible, and only increasing complexity when needed."

### Five workflow patterns

| Pattern | Units | Composition | What crosses the boundary | Selection rule |
|---|---|---|---|---|
| **Prompt chaining** | Sequential LLM calls | Linear pipeline with programmatic gates | Output of one call → input of next | Task decomposable into fixed subtasks; trade latency for accuracy |
| **Routing** | Classifier LLM + specialised handlers | Decision tree (one entry, multiple branches) | Classified input dispatched to handler | Distinct categories needing separate handling |
| **Parallelisation** | Multiple independent LLM calls (sectioning) or repeated same call (voting) | Fan-out / fan-in | Divided inputs → aggregated outputs | Speed from independence, or confidence from multiple perspectives |
| **Orchestrator–workers** | Central orchestrator LLM + worker LLMs | Hierarchy (orchestrator determines subtasks dynamically) | Task decomposition down, results up, synthesis at top | Complex tasks with unpredictable subtask structure |
| **Evaluator–optimiser** | Generator LLM + evaluator LLM | Feedback loop | Generated response → evaluation → feedback → refined response | Clear evaluation criteria exist; iterative refinement measurably improves output |

### Autonomous agent pattern

A single LLM in a loop with tools. Composition: iterative loop with environmental feedback. Requires "ground truth from the environment at each step." Selection: open-ended problems, unpredictable step counts. Evidence: SWE-bench, computer use.

### Evidence and caveats

No quantitative benchmarks given in the post. The guidance is experience-based ("worked with dozens of teams"). The strongest claim is negative: most successful implementations used simple, composable patterns, not complex frameworks. *[Inference: the post is deliberately anti-framework, which positions it against MetaGPT-style role systems.]*

---

## 2. Anthropic's Multi-Agent Research System (Claude Research)

**Source:** [Building Production Multi-Agent Research Systems with Claude](https://www.zenml.io/llmops-database/building-production-multi-agent-research-systems-with-claude), ZenML/Anthropic, April 2025.

### Units

- **Lead researcher** (Claude Opus 4): analyses query, develops strategy, spawns workers, synthesises results.
- **Subagent workers** (Claude Sonnet 4): each chases one independent research thread with its own context window.
- **Citation agent**: processes documents for citation placement.

### Composition

Orchestrator–worker hierarchy with parallel fan-out. The lead agent "synthesises these results and decides whether more research is needed" (iterative loop at the top level).

### What crosses boundaries

Task descriptions (objective, output format, tool guidance, boundaries) flow down. Findings flow up. Only the final message returns — intermediate tool calls stay isolated in the subagent context.

### Evidence (quantitative)

- Multi-agent with Opus 4 + Sonnet 4 **outperformed single-agent Opus 4 by 90.2%** on internal research evaluations.
- Token usage explained **80% of performance variance**; model choice and tool calls secondary.
- System uses **~15× more tokens** than standard chat.
- Upgrading to Sonnet 4 "provided a larger performance gain than doubling the token budget on Sonnet 3.7."

### When multi-agent helps vs. hurts

Helps: "heavy parallelisation, information exceeding single context windows, interfacing with numerous complex tools." Hurts: tasks requiring "all agents to share the same context or involve many dependencies between agents." Coding tasks lack sufficient parallelisable components. *[Sourced claim.]*

---

## 3. OpenAI: Swarm → Agents SDK

### Swarm (October 2024)

**Source:** [OpenAI Swarm](https://github.com/openai/swarm), October 2024; [Arize AI explainer](https://arize.com/blog/comparing-openai-swarm).

Experimental, educational framework. Two primitives: **agents** (LLM + instructions + tools) and **handoffs** (agent-to-agent transfer carrying conversation context). Composition: flat peer-to-peer handoff graph. Explicitly "not yet ready for large-scale deployment."

### Agents SDK (March 2025, major overhaul April 2026)

**Source:** [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/), OpenAI, 2025; [Agents SDK docs](https://openai.github.io/openai-agents-python/).

Three built-in primitives: **handoffs**, **guardrails**, **tracing**.

Two orchestration patterns:

| Pattern | Units | Composition | When to use |
|---|---|---|---|
| **Agents as tools** | Manager agent + specialist agents via `Agent.as_tool()` | Hierarchy — manager retains conversation control | Specialist handles bounded subtask, shouldn't own the conversation |
| **Handoffs** | Triage agent + specialist agents | Peer transfer — specialist owns remainder of current turn | Routing is part of the workflow; specialist should own the conversation |

What crosses: tool outputs (agents-as-tools) or full conversation ownership (handoffs). Task selection: LLM-driven through prompts, or code-based via structured outputs + deterministic routing.

April 2026 overhaul added: native sandbox execution, long-horizon harness, subagent primitive (beta), planned code mode. *[Sourced: search result summary.]*

---

## 4. Google: Agent Development Kit (ADK)

**Source:** [Developer's guide to multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/), Google Developers Blog, 2025.

### Patterns

| Pattern | Units | Composition | Data boundary | Selection |
|---|---|---|---|---|
| **Sequential pipeline** | Parser → Extractor → Summariser | Linear chain via `output_key` / `session.state` | Output of each agent | Deterministic, debuggable data processing |
| **Coordinator / dispatcher** | Central coordinator + domain specialists | Tree with intelligent routing at root | User request routed by intent | Systems needing decision-making for domain routing |
| **Parallel fan-out / gather** | Independent workers + synthesiser | Fan-out / fan-in; unique state keys prevent races | Each agent writes to unique state key; synthesiser reads all | Tasks lacking dependencies; need diverse perspectives |
| **Hierarchical decomposition** | Parent + child agents (nested) | Tree hierarchy; children wrapped as `AgentTool` | Parent treats child as tool; waits for result | Task exceeds single context window |
| **Generator–critic** | Generator + critic | Sequential loop with conditional exit | Draft → binary pass/fail validation | Compliance-critical outputs |
| **Iterative refinement** | Generator + critic + refiner | Loop with multi-iteration improvement | Draft → critique notes → refined draft | Qualitative improvement through polish |
| **Human-in-the-loop** | Agents + human checkpoint | Sequential with pause | Agent escalates to `ApprovalTool` | Irreversible or high-consequence actions |
| **Composite** | Any combination | Nested multi-pattern | Mixed | Real-world enterprise applications |

Also: deterministic vs. dynamic orchestration (code-defined flow vs. LLM-decided delegation).

**Evidence:** None provided — no quantitative benchmarks. Google's own guidance echoes Anthropic's: "start simple, add complexity incrementally." *[Sourced.]*

### Agent2Agent (A2A) protocol

Cross-vendor agent communication standard, now a Linux Foundation project with 150+ backing organisations as of April 2026. *[Sourced: search result.]*

---

## 5. Andrew Ng's Four Agentic Design Patterns

**Source:** [Andrew Ng on X](https://x.com/AndrewYNg/status/1773393357022298617), March 2024; [LinkedIn post](https://www.linkedin.com/posts/andrewyng_one-agent-for-many-worlds-cross-species-activity-7179159130325078016-_oXr).

### The four patterns

1. **Reflection**: LLM examines its own work, critiques, revises. Loop.
2. **Tool use**: LLM makes API calls, interacts with external data. Extension.
3. **Planning**: Complex task → sequence of smaller steps. Decomposition. Ng flagged this as "less mature, less predictable."
4. **Multi-agent collaboration**: Multiple specialised agents, each with own prompt/LLM/tools. Composition.

### Composition

Ng's framing is combinatorial: "the most sophisticated AI systems often combine multiple patterns." No hierarchy among patterns; no formal composition rule. Selection is by need.

### Evidence

No benchmarks. The framing is influential but prescriptive, not empirical. *[Inference: this is a categorisation of capabilities, not a composition ontology. It says what an agent can do, not how agents compose into systems.]*

---

## 6. Aider: Architect / Editor Separation

**Source:** [Separating code reasoning and editing](https://aider.chat/2024/09/26/architect.html), Aider blog, September 2024.

### Units

- **Architect**: reasoning-capable model describes how to solve the coding problem, without formatting constraints.
- **Editor**: second model converts the Architect's solution into specific code editing instructions.

### Composition

Two-step pipeline. Not a loop — the Architect produces once, the Editor applies once.

### What crosses

Natural-language solution description flows from Architect to Editor. The Editor never reasons about the problem; the Architect never formats edits.

### Rationale

"Splitting responsibilities addresses a fundamental constraint" — requiring a single model to simultaneously reason and conform to edit formats dilutes performance on both.

### Evidence (quantitative)

- o1-preview + DeepSeek/o1-mini Editor: **85% pass rate** (SOTA at time of publication).
- o1-preview + Claude 3.5 Sonnet Editor: **82.7%**.
- Claude 3.5 Sonnet with itself: **80.5%** (vs. 77.4% baseline — a 3.1pp gain just from separation).
- R1 + Sonnet as editor: **64.0%** on polyglot benchmark at **14× less cost** than previous o1 SOTA.

*[Inference: this is strong evidence that separating reasoning from formatting into distinct calls helps, even when the same model plays both roles.]*

---

## 7. Claude Code: Plan Mode and Subagents (2025–2026)

**Source:** [Codex vs Claude Code: Subagent Design Philosophy](https://smartscope.blog/en/blog/codex-vs-claude-code-subagent-architecture-2026/), SmartScope, 2026; [Claude Code Plan Mode guide](https://stacknotice.com/blog/claude-code-plan-mode-guide-2026), StackNotice, 2026.

### Plan mode

Separates thinking from doing: "retaining full access to read tools while blocking all write tools." The question shifts from "Did Claude do this correctly?" to first "Is this the right plan?"

### Subagent architecture

- Organised around **thinking phases** (Plan, Explore, General-purpose), not task types.
- Delegation is **implicit** (agent-judged), not user-commanded.
- Only the subagent's **final summary message** returns to the parent — intermediate tool calls stay isolated.
- Subagents can select model by task complexity (Haiku for simple, Opus for complex).

### Codex comparison

Codex (March 2026 multi-agent v2) organises around **task execution units** with explicit user spawn commands, path-based subagent addresses, and structured inter-agent messaging. Delegation is explicit, user-initiated. *[Sourced.]*

### Evidence

No direct comparative benchmarks between the two philosophies. *[Observation.]*

---

## 8. OpenAI Codex Agent Architecture

**Source:** [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/), OpenAI, 2025; [Everything About Codex](https://bhavishyapandit9.substack.com/p/everything-about-codex-the-complete), 2026.

### Units

Disaggregated architecture: LLM reasoning loop separated from tool execution. Each task runs in an isolated cloud container or local sandbox. Early 2026: main agent can spawn specialised subagents in parallel, each with independent context window and sandbox.

### Composition

Asynchronous by default. Produces reviewable artefacts (comments, drafts, proposed changes). The human is the final approval gate.

### Evidence

SWE-bench Verified: ~45.8% (Devin 2.0), vs. OpenHands with Claude Opus 4.6 at 68.4%. *[Sourced: search result, early 2026.]*

---

## 9. Other Coding Agents: OpenHands, Devin

**Source:** [OpenHands Software Agent SDK](https://arxiv.org/html/2511.03690v1), arXiv, November 2025.

### OpenHands

Event-sourced state model with deterministic replay. V1 refactored into modular SDK with clear boundaries, opt-in sandboxing, reusable agent/tool/workspace packages. Composition: single-agent loop with tool access, not multi-agent by default.

### Industry convergence

"The industry seems to have collectively discovered the core ingredients required to make agents useful for real development work" — the plan/act/review loop is now standard across Claude Code, Codex, Cursor, Gemini, Aider, Devin, OpenHands. *[Sourced: search result summary.]*

---

## 10. Generator–Verifier Separation and the Generation–Verification Gap

### Formal definition

**Source:** [Mind the Gap: Examining the Self-Improvement Capabilities of LLMs](https://arxiv.org/pdf/2412.02674), ICLR 2025.

The Generation-Verification Gap (GV-Gap) is a formal metric between a generator f and verifier g. When f = g (same model), it is the **self-improvement GV-Gap**. Key finding: while generation scales, verification becomes the bottleneck — discriminative models, reward functions, or humans are required.

### Scaling properties

- Iterative self-improvement **saturates** — repeated generate-verify loops hit diminishing returns.
- Ensemble verification methods enhance the gap.
- Quality coefficients for proposer quality were **2–4× larger** than diversity coefficients (see §12 on MoA).

### Multi-Agent Verification (MAV)

**Source:** [Multi-Agent Verification: Scaling Test-Time Compute with Multiple Verifiers](https://arxiv.org/abs/2502.20379), Lifshitz et al., February 2025.

Introduces **Aspect Verifiers** (AVs): off-the-shelf LLMs prompted to verify different aspects. Binary outputs combined by voting. BoN-MAV (best-of-N + MAV) shows stronger scaling than self-consistency and reward-model verification. Demonstrates **weak-to-strong generalisation**: combining weak verifiers improves even stronger generators.

### Shrinking the gap with weak verifiers

**Source:** [Shrinking the Generation-Verification Gap with Weak Verifiers](https://arxiv.org/html/2506.18203v1), 2025.

Shows that even weak verifiers (smaller models) can narrow the GV-Gap when used as separate processes — supporting architectural separation of generation and verification. *[Sourced.]*

---

## 11. Self-Verification Weakness: When the Same Model Reviews Itself

### Systematic findings

**Source:** [On the Self-Verification Limitations of Large Language Models](https://arxiv.org/pdf/2402.08115), ICLR 2025.

LLM self-critique decomposed into three components: verification, critique generation, critique consideration. Across hard reasoning domains, **LLMs performed poorly in all three**, with stacked errors often making the self-critiquing loop **worse than the initial guess**.

### The self-critique paradox

**Source:** [The Self-Critique Paradox](https://snorkel.ai/blog/the-self-critique-paradox-why-ai-verification-fails-where-its-needed-most/), Snorkel AI, 2025.

- For tasks where models started strong (≥75% accuracy), critique loops were **devastating** — the critic hallucinated errors.
- For tasks where models started weak (<35% accuracy), critique **caught real errors** effectively.

*[Inference: self-critique helps where the model is bad (catching obvious mistakes) but hurts where the model is good (introducing phantom errors). This is a strong argument for using a different model or a different process for verification.]*

### External verifier advantage

Performance gains observed when "an external sound verifier provided the verification signal and critique instead" of the generating model. *[Sourced: ICLR 2025 paper.]*

---

## 12. Mixture-of-Agents (MoA) and Debate

### Original MoA

**Source:** [Mixture-of-Agents Enhances Large Language Model Capabilities](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5434be94e82c54327bb9dcaf7fca52b6-Abstract-Conference.html), ICLR 2025.

Layered architecture: each layer has multiple LLM agents; each agent sees all outputs from the previous layer as auxiliary information. Composition: layered pipeline (not a loop). Achieved SOTA on AlpacaEval 2.0 (65.1% vs. GPT-4o's 57.5%) using open-source LLMs.

### Rethinking MoA: Self-MoA

**Source:** [Rethinking Mixture-of-Agents: Is Mixing Different Large Language Models Beneficial?](https://arxiv.org/html/2502.00674v1), February 2025.

**Key finding:** Self-MoA (same top-performing model repeated) **outperformed Mixed-MoA** (different models) by 6.6 points on AlpacaEval 2.0 and an average of 3.8% across MMLU, CRUX, and MATH.

Through regression: quality coefficients were **2–4× larger** than diversity coefficients. Mixed-MoA showed marginal advantage (0.17–0.35%) only when combining equally-performing specialists.

*[Inference: this is a direct challenge to the intuition that "diverse models catch each other's errors." Quality of the proposer matters more than variety. This cuts against naive multi-model debate.]*

### Multi-Agent Debate

**Source:** [Multi-LLM-Agents Debate](https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/), ICLR Blogposts, April 2025.

Multiple agents independently generate proposals, then engage in deliberation to reach consensus. Inspired by Society of Mind. But: "a single model with carefully designed prompts can sometimes match the performance of agent discussions, and agent discussions mainly outperform a single LLM when the prompts are insufficient." *[Sourced.]*

---

## 13. MetaGPT: SOP Roles

**Source:** [MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352), ICLR 2024.

### Units

Software company roles: Product Manager, Architect, Project Manager, Engineer. Each is an LLM agent with role-specific prompts and output schemas.

### Composition

Publish-subscribe via global message pool. SOPs define sequential handoffs with structured intermediate artefacts (PRD → design doc → task list → code). "Code = SOP(Team)."

### What crosses

Standardised documents (PRDs, design documents, task lists). Not raw text — structured artefacts with schemas.

### Evidence

ICLR 2024 conference paper. Subsequent AFlow (ICLR 2025, oral, top 1.8%) used LLMs to search the space of possible SOP configurations — essentially automated workflow architecture search. *[Sourced.]*

*[Inference: MetaGPT's approach is the most role-rigid in the field. It assumes the roles themselves are the right decomposition. AFlow's automated search of SOP space implicitly questions whether human-designed role assignments are optimal.]*

---

## 14. Thought-Structure Ontologies: ToT, GoT, FoT

### Tree of Thoughts (ToT)

**Source:** [Tree of Thoughts](https://arxiv.org/abs/2305.10601), Yao et al., 2023 (NeurIPS 2024).

Units: "thoughts" (intermediate reasoning steps) as tree nodes. Composition: tree search (BFS or DFS) with LLM-generated evaluations at each node. What crosses: partial solutions and heuristic evaluations. Selection: problems requiring search, planning, exploration.

### Graph of Thoughts (GoT)

**Source:** [Graph of Thoughts](https://dl.acm.org/doi/10.1609/aaai.v38i16.29720), AAAI 2024.

Units: thoughts as vertices in an arbitrary graph; edges are dependencies. Composition: graph — enables combining thoughts, distilling networks, feedback loops. Generalises ToT by allowing merges and cycles.

### What came after

- **Lateral Tree-of-Thoughts** (2025): incorporates logically-consistent, low-utility candidates to surpass standard ToT. *[Source: arXiv 2510.01500.]*
- **MTMT** (2024): consolidates multiple thinking modes into a single thought tree. *[Source: arXiv 2412.03987.]*
- **Forest of Thoughts**: multiple reasoning trees in parallel — scaling test-time compute.

### Key empirical finding

**Source:** [Understanding When Tree of Thoughts Succeeds](https://arxiv.org/pdf/2410.17820), October 2024.

"Larger models excel in generation, not discrimination" — ToT's value-guided search is limited by the model's ability to evaluate intermediate thoughts, not generate them. *[Sourced.]*

*[Inference: this mirrors the generator-verifier gap. Tree/Graph search requires evaluation at each node; when the evaluator is the same model, the benefit plateaus or reverses for strong models.]*

---

## 15. Difficulty- and Effort-Routing

### RouteLLM

**Source:** [RouteLLM](https://arxiv.org/abs/2406.18665), 2024; search results.

Learns routing policy from human preference data. Routers include matrix factorisation and causal LLM classifiers trained on Chatbot Arena data. Routes easy queries to cheap models, hard queries to expensive ones.

### Cascading

**Source:** [Cluster, Route, Escalate: Cascaded Framework for Cost-Aware LLM Serving](https://arxiv.org/pdf/2606.27457), June 2026; [Is Escalation Worth It?](https://arxiv.org/pdf/2605.06350), 2025.

Sequential: start with cheap model, escalate to expensive one when initial response is insufficient. Unlike routing (one-shot selection), cascading allows retry.

### Adaptive test-time compute

**Source:** [Scaling LLM Test-Time Compute Optimally](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b623663fd9b874366f3ce019fdfdd44-Paper-Conference.pdf), ICLR 2025.

Compute-optimal scaling prescribes adaptive, prompt-dependent strategy. Adaptively allocating compute using predicted difficulty yields clear performance gains. But "compute-optimal" ≠ "latency-optimal" — parallel scaling can be 1.6× faster.

### Overthinking

**Source:** [When More Thinking Hurts](https://arxiv.org/html/2604.10739v1), April 2026.

o1-like models consume excessive tokens on simple problems with minimal accuracy benefit. Adaptive reasoning length based on problem difficulty is the proposed solution.

### Industry practice

GPT-5 reportedly routes between "a smart, efficient model that answers most questions, [and] a deeper reasoning model for harder problems." *[Sourced: search result summary, attributed to industry reporting.]*

*[Inference: difficulty routing is converging from research to product. The units here are not "types of thinking" but "amounts of thinking," and the composition rule is an escalation ladder.]*

---

## 16. Hierarchical Planning in LLM Agents

### HiPlan

**Source:** [HiPlan: Hierarchical Planning for LLM Agents with Adaptive Global-Local Guidance](https://arxiv.org/html/2508.19076), 2025.

Two-level planning: global planner creates high-level subgoals; local planner executes within each subgoal. Adaptive: the global plan can be revised based on local execution feedback.

### HTN integration

**Source:** [Hierarchical Task Network Planning with LLM-Generated Heuristics](https://arxiv.org/html/2605.07707v1), 2025.

ChatHTN interleaves approximate (LLM) planning with symbolic HTN planning. LLMs generate heuristics; HTN provides formal guarantees. Composition: nested loop where LLM proposes and HTN validates/refines.

### Empirical findings on hierarchy

**Source:** [DEPART: Hierarchical Multi-Agent System](https://openreview.net/pdf/af2cc92bb045206ca7733acadb3a94fe72719916.pdf), 2025.

Removing hierarchy (single LLM agent) dropped success rate to 0.25 (−59.3%), "highlighting the critical role of hierarchical decomposition in limiting input length and enabling parallelism." *[Sourced.]*

### GeoJSON planner ablation

**Source:** Search result summary from [GeoJSON Agents](https://arxiv.org/pdf/2509.08863).

Removing the Planner module: accuracy dropped from 85.71% to 12.86%. *[Sourced.]*

---

## 17. Context Contamination and Tool-Presence Bias

### Context contamination in retries

**Source:** [Why Retrying Fails: Context Contamination in LLM Agent Pipelines](https://arxiv.org/html/2605.08563), June 2025.

Failed attempts pollute context, elevating error rate on subsequent attempts. On SWE-bench: contaminated attempts are **7.1× more error-prone**. Standard IID model predicts 98.6% pass@3; actual is 81.2% (17.4pp gap). Recommendation: **clear context before retrying** (~21% improvement).

### Structural Alignment Bias (tool presence → action)

**Source:** [Do LLMs Know Tool Irrelevance?](https://arxiv.org/html/2604.11322), April 2026.

When tools are structurally aligned (parameters match query attributes) but semantically irrelevant, error rates jump from <0.2% to ~42%, escalating to 90% as more parameters align. Models tested: Qwen3 series, ToolACE-2.5-8B, Watt-Tool-8B.

Implication: "the mere presence of tools dramatically affects LLM reasoning" — LLMs rely on structural matching as a shortcut, not semantic verification. Proposed mitigation achieved 80% error reduction.

*[Inference: this is direct evidence that tool-equipped and tool-free thinking are qualitatively different cognitive modes. Putting tools in the context changes the model's reasoning even when the tools are irrelevant. This supports separating "think about what to do" from "do it with tools."]*

---

## 18. Society of Mind / Internal Dialogue Models

### Society of Mind for LLM agents

**Source:** [Language Model Agents in 2025: Society of Mind Revisited](https://isolutions.medium.com/language-model-agents-in-2025-897ec15c9c42), Medium, 2025.

Intelligence emerges when computational modules interact, achieving collective objectives exceeding individual modules. The SoM concept from Minsky (1986) is the explicit inspiration for multi-agent debate and MoA. *[Sourced.]*

### Dual-process models (fast/slow thinking)

**Source:** [DUMA: a Dual-Mind Conversational Agent with Fast and Slow Thinking](https://arxiv.org/pdf/2310.18075), 2023. *[Training knowledge: SwiftSage also proposed fast/slow agent separation.]*

Units: a fast-thinking module (pattern matching, retrieval) and a slow-thinking module (deliberate reasoning). Composition: the fast module handles routine queries; the slow module is invoked when the fast module's confidence is low. This maps directly to difficulty routing.

### Multi-Agent Debate

**Source:** [Multi-LLM-Agents Debate — Performance, Efficiency, and Scaling Challenges](https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/), ICLR Blogposts, April 2025.

Du et al.'s MAD framework: agents independently propose, then deliberate to consensus. But the empirical finding undermines the premise: "agent discussions mainly outperform a single LLM when the prompts are insufficient." *[Sourced.]*

---

## 19. When Separating Thinking Into Separate Calls Helps vs. Hurts: The Empirical Record

### Helps

| Finding | Source | Effect |
|---|---|---|
| Architect/Editor separation on code editing | Aider, Sep 2024 | +3.1pp even same-model; +7.6pp cross-model (SOTA) |
| Multi-agent research vs. single-agent | Anthropic, Apr 2025 | +90.2% on research tasks |
| Planner + worker vs. worker alone | GeoJSON Agents, 2025 | 85.7% → 12.9% without planner |
| Hierarchical decomposition vs. flat | DEPART, 2025 | −59.3% success rate without hierarchy |
| External verifier vs. self-verification | ICLR 2025 | Self-critique loop worse than initial guess on hard reasoning |
| Context clearing between retries | arXiv Jun 2025 | ~21% improvement; 7.1× error reduction |
| Weak multi-verifier ensemble | MAV, Feb 2025 | Stronger scaling than self-consistency |

### Hurts or doesn't help

| Finding | Source | Effect |
|---|---|---|
| Self-critique on tasks where model is already strong | Snorkel/ICLR 2025 | Critique **devastates** performance (≥75% baseline) |
| Mixed-MoA vs. Self-MoA | arXiv Feb 2025 | Same model repeated beats different models by 6.6pp |
| Multi-agent debate vs. well-prompted single agent | ICLR Blogposts 2025 | Debate wins mainly when prompts are insufficient |
| Multi-agent on tightly-coupled sequential tasks | Anthropic 2025 | Not worth 15× token cost |
| More agents without complementary roles | Agents that Matter, 2025 | Redundant agents waste cost; removal + model substitution can improve by 17% |

### Key disagreement

The sharpest tension: **Anthropic's "start simple" guidance** vs. **the planner-ablation evidence** showing massive drops without hierarchy. The resolution appears to be task-dependent: parallelisable research benefits enormously from multi-agent; sequential reasoning does not. The generator–verifier gap literature adds nuance: separation helps when the verifier is genuinely independent (different model, different aspect, external ground truth), but same-model self-critique often backfires.

---

## 20. Unknowns and Open Questions

1. **Optimal granularity of thinking-unit separation.** No principled method exists for deciding how many units or what kind. AFlow's automated search is the closest attempt, but it searches SOP configurations, not cognitive-mode decompositions.

2. **Whether role-based decomposition (MetaGPT) or phase-based decomposition (Claude Code) is superior.** No head-to-head comparison exists.

3. **The relationship between difficulty routing and thinking-type routing.** Are these the same axis (amount of thinking) or orthogonal (kind of thinking)? The field treats them separately; no work unifies them.

4. **Context contamination mitigation beyond clearing.** The 7.1× cascade ratio implies that even sophisticated retry strategies fail without context isolation, but the cost of full isolation (separate context windows, 15× token overhead) may not be justified for all tasks.

5. **Whether the Self-MoA finding (same model > diverse models) holds for non-generative tasks.** The evidence is on benchmarks like AlpacaEval and MATH; whether it extends to agent tool use, planning, or coding is untested.

---

## Sources

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents), Anthropic, December 2024
- [Building Production Multi-Agent Research Systems with Claude](https://www.zenml.io/llmops-database/building-production-multi-agent-research-systems-with-claude), ZenML, April 2025
- [OpenAI Agents SDK — Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/), OpenAI, 2025
- [Developer's guide to multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/), Google Developers Blog, 2025
- [Andrew Ng on X — four agentic design patterns](https://x.com/AndrewYNg/status/1773393357022298617), March 2024
- [Separating code reasoning and editing](https://aider.chat/2024/09/26/architect.html), Aider, September 2024
- [Codex vs Claude Code: Subagent Design Philosophy](https://smartscope.blog/en/blog/codex-vs-claude-code-subagent-architecture-2026/), SmartScope, 2026
- [MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352), ICLR 2024
- [Mind the Gap: Examining the Self-Improvement Capabilities of LLMs](https://arxiv.org/pdf/2412.02674), ICLR 2025
- [Multi-Agent Verification: Scaling Test-Time Compute with Multiple Verifiers](https://arxiv.org/abs/2502.20379), Lifshitz et al., February 2025
- [On the Self-Verification Limitations of Large Language Models](https://arxiv.org/pdf/2402.08115), ICLR 2025
- [The Self-Critique Paradox](https://snorkel.ai/blog/the-self-critique-paradox-why-ai-verification-fails-where-its-needed-most/), Snorkel AI, 2025
- [Rethinking Mixture-of-Agents](https://arxiv.org/html/2502.00674v1), February 2025
- [Mixture-of-Agents Enhances LLM Capabilities](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5434be94e82c54327bb9dcaf7fca52b6-Abstract-Conference.html), ICLR 2025
- [Multi-LLM-Agents Debate](https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/), ICLR Blogposts, April 2025
- [Graph of Thoughts](https://dl.acm.org/doi/10.1609/aaai.v38i16.29720), AAAI 2024
- [Understanding When Tree of Thoughts Succeeds](https://arxiv.org/pdf/2410.17820), October 2024
- [Scaling LLM Test-Time Compute Optimally](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b623663fd9b874366f3ce019fdfdd44-Paper-Conference.pdf), ICLR 2025
- [When More Thinking Hurts](https://arxiv.org/html/2604.10739v1), April 2026
- [Why Retrying Fails: Context Contamination in LLM Agent Pipelines](https://arxiv.org/html/2605.08563), June 2025
- [Do LLMs Know Tool Irrelevance? Structural Alignment Bias](https://arxiv.org/html/2604.11322), April 2026
- [HiPlan: Hierarchical Planning for LLM Agents](https://arxiv.org/html/2508.19076), 2025
- [Hierarchical Task Network Planning with LLM-Generated Heuristics](https://arxiv.org/html/2605.07707v1), 2025
- [DEPART: Hierarchical Multi-Agent System](https://openreview.net/pdf/af2cc92bb045206ca7733acadb3a94fe72719916.pdf), 2025
- [Shrinking the Generation-Verification Gap with Weak Verifiers](https://arxiv.org/html/2506.18203v1), 2025
- [OpenHands Software Agent SDK](https://arxiv.org/html/2511.03690v1), November 2025
- [Agents that Matter: Optimizing via Removal-Based Attribution](https://arxiv.org/html/2605.27621), 2025
- [RouteLLM](https://arxiv.org/abs/2406.18665), 2024
