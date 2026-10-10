# Flow Composition Ontologies: How Agentic Systems Divide Thinking (2024--2026)

Report for flow b9f4f6. Sourced claims carry URLs and dates; inferences are marked [inference]; training-knowledge claims are marked [training-knowledge].

---

## 1. Anthropic's Workflow Patterns

**Source:** Anthropic, "Building Effective Agents," December 2024. https://www.anthropic.com/research/building-effective-agents

Five composable workflow patterns, plus a sharp workflow-vs-agent distinction:

### Units and Composition

| Pattern | Units | Composition | Boundary-crossing | When chosen |
|---|---|---|---|---|
| **Prompt Chaining** | Sequential LLM calls with programmatic gates | Pipeline | Output of step N -> input of step N+1; gate can reject | Task decomposes into fixed subtasks; trade latency for accuracy |
| **Routing** | Classifier + specialized handlers | Dispatch (fan-out by type) | Classification label selects handler | Distinct input categories need different treatment; enables cost routing (Haiku for simple, Sonnet for hard) |
| **Parallelization** | Independent subtasks ("sectioning") or identical runs ("voting") | Fan-out + programmatic aggregation | Results merge via code | Speed or confidence through diversity; guardrail screening parallel to main response |
| **Orchestrator--Workers** | Central orchestrator LLM + worker LLMs | Dynamic hierarchy; orchestrator decomposes and synthesizes | Task decomposition downward, results upward | Subtasks cannot be predicted beforehand (e.g., multi-file code changes) |
| **Evaluator--Optimizer** | Generator LLM + evaluator LLM | Iterative loop | Evaluation feedback drives next generation | Clear evaluation criteria exist; iterative refinement measurably helps |

**Agent** (distinguished from workflow): an LLM that dynamically directs its own process and tool use, in an open-ended loop. Recommended only for "open-ended problems where it's difficult or impossible to predict the required number of steps."

**Key principle:** "Find the simplest solution possible, and only increasing complexity when needed." Start with a single prompt; add patterns only when they demonstrably improve outcomes.

### Evidence

The guide reports experience from "dozens of teams building LLM agents across industries" but gives no controlled benchmarks or effect sizes. The examples (marketing copy, customer service, multi-file code edits, search) are illustrative, not experimental. [Sourced: the guide itself makes this distinction.]

---

## 2. Later Multi-Agent Guidance (Anthropic, OpenAI, Google)

### Anthropic Multi-Agent Research (December 2025)

**Source:** "Towards a Science of Scaling Agent Systems," arXiv 2512.08296, December 2025. https://arxiv.org/abs/2512.08296

Evaluated 260 configurations across six benchmarks, five architectures (Single-Agent, Independent, Centralized, Decentralized, Hybrid), three model families.

Key findings:
- Architecture-task alignment determines outcomes: "+80.8% on decomposable financial reasoning to -70.0% on sequential planning." [Sourced]
- Architectures without centralized verification propagate errors more. [Sourced]
- Multi-agent coordination yields diminishing returns once single-agent performance reaches certain thresholds. [Sourced]
- Tool-heavy tasks impose overhead penalties for multi-agent systems. [Sourced]
- Token usage explains ~80% of performance variance. [Sourced from fork summary; verify against paper]

### Anthropic Claude Code (2025--2026)

**Sources:** Claude Code documentation, 2025--2026. https://www.cloudzero.com/blog/claude-code-agents/ ; https://www.vibecodingacademy.ai/blog/claude-code-subagents-complete-guide ; https://code.claude.com/docs/en/model-config

- **Subagents:** Three specialized types -- Explore (read-only search), Plan (architecture/design, read-only), and General-purpose (full tool access). Each runs in its own context window; the orchestrator sees only the final summary message. [Sourced]
- **Agent teams ("Swarms"):** A team-lead session delegates to teammates who share a task list and message each other directly. [Sourced]
- **Plan mode:** A read-only state (Shift+Tab or `/plan`) where Claude can read but not write. Separates planning from execution. "Ultraplan" (April 2026) trades latency for plan quality on complex tasks. [Sourced]
- **Dynamic Workflows (2026):** Parallel fan-out of subagents for independent work streams. [Sourced from fork]
- **Per-subagent effort and model overrides:** A main Opus agent can spawn Haiku subagents at low effort for lookups, Opus subagents at high effort for analysis. [Sourced: https://github.com/anthropics/claude-code/issues/25669]

Units: lead agent, typed subagents (isolated context windows), plan-mode pass.
Composition: hierarchy (lead -> subagents) or peer messaging (teams); plan mode is a pipeline gate.
Boundary-crossing: task descriptions downward, final summary upward; shared task list for teams.

### OpenAI Agents SDK (March 2025)

**Source:** OpenAI, "New tools for building agents," March 2025. https://openai.com/index/new-tools-for-building-agents/ ; https://openai.github.io/openai-agents-python/multi_agent/

Two orchestration patterns:
- **Manager (agents as tools):** Central orchestrator invokes sub-agents as tools, retains control. The sub-agent runs in a bounded scope and returns a result.
- **Handoffs:** Peer agents transfer full conversation control to a specialized agent that takes over.

Units: agents with instructions, tools, guardrails.
Composition: hierarchy (manager) or sequential handoff (peer).
Boundary-crossing: tool-call interface (manager) or control transfer with full conversation context (handoff).
Selection: LLM-driven (the model decides which agent to call or hand off to) or code-orchestrated.

### OpenAI Codex (May 2025)

**Source:** OpenAI, "Introducing Codex," May 2025. https://openai.com/index/introducing-codex/ ; https://www.zenml.io/llmops-database/building-production-ready-ai-agents-openai-codex-cli-architecture-and-agent-loop-design

- Flat iterative loop: inference -> tool call -> execute -> re-query. No explicit plan/act separation. [Sourced]
- Three approval modes control human checkpoints (suggest, auto-edit, full-auto). [Sourced]
- Each task gets an isolated sandbox and its own git worktree. [Sourced]
- Subagent capability (early 2026): main agent spawns specialized subagents in parallel, each with independent context window and sandbox. [Sourced]

Units: reasoning loop, tool executor, sandbox.
Composition: pipeline (reason -> execute -> observe) with parallel fan-out for subagents.

### Google ADK (2025--2026)

**Source:** Google Agent Development Kit documentation and guides. [Sourced from fork]

Eight named patterns: sequential, coordinator/dispatcher, fan-out/gather, hierarchical decomposition, generator-critic, iterative refinement, human-in-the-loop, composite. No published benchmarks. [Sourced]

---

## 3. Andrew Ng's Agentic Design Patterns (March 2024)

**Source:** Andrew Ng, X/Twitter post, March 2024. https://x.com/AndrewYNg/status/1773393357022298617

Four patterns: **Reflection, Tool Use, Planning, Multi-Agent Collaboration.**

- **Reflection:** LLM examines its own output to improve it. A loop.
- **Tool Use:** LLM invokes external tools. An action step in a loop.
- **Planning:** LLM decomposes a task into subtasks. Ng flagged this as "less mature, less predictable."
- **Multi-Agent Collaboration:** Multiple specialized agents with distinct prompts, LLMs, tools, and code.

Units: these are cross-cutting capabilities, not structural units. A single agent can use all four.
Composition: unspecified; Ng described these as mixable ingredients, not a fixed architecture.
Evidence: no benchmarks; positioned as a practitioner's framing for the year ahead. [Sourced: Ng's own characterization.]

---

## 4. Generator--Verifier Separation and the GV Gap

### The Generation-Verification Gap

**Source:** "Variation in Verification: Understanding Verification Dynamics in Large Language Models," arXiv 2509.17995, September 2025 (ICLR 2026). https://arxiv.org/abs/2509.17995

14 models (2B--72B) + GPT-4o across 4,444 problems:
- Easy problems: true positive rate (TPR) >0.7 -- verification works well. [Sourced]
- Strong generators produce harder-to-detect errors: true negative rate (TNR) drops from 0.68 to 0.17 as generator strength increases. [Sourced]
- Medium difficulty: linear correlation r>0.9 between generation and verification ability. [Sourced]
- Hard problems: near-zero TPR improvement even with stronger verifiers. [Sourced]
- "Strong verifiers offer limited advantage over weak ones" -- verifier scaling alone cannot overcome fundamental challenges. [Sourced]
- Weak generators can nearly match stronger ones after verification: "the Gemma2-9B to Gemma2-27B performance gap shrinks by 75.7%." [Sourced]

### Closing the Gap with Ensembles

**Source:** "Shrinking the Generation-Verification Gap with Weak Verifiers" (Weaver), arXiv 2506.18203, June 2025. https://arxiv.org/abs/2506.18203

- 33 open-source verifiers (8B--72B) for Llama 3.3 70B generator. [Sourced]
- Ensemble closes GV-Gap by 14.5%. Weighted ensembles outperform individual verifiers by up to 11.2 pp; outperform majority voting by 15.5%. [Sourced]
- Even weak verifiers close much of the generation gap, but as generators improve, their errors become more subtle and harder to detect. [Sourced]

### Generative Verifiers

**Source:** "Generative Verifiers," ICLR 2025. https://openreview.net/attachment?id=Ccwp4tFEtE&name=pdf

- Generative verifiers (CoT + verdict) scale more favorably than discriminative verifiers; outperform LLM-as-a-Judge with majority voting. [Sourced]

### Generator vs. Discriminator in ToT

**Source:** "Understanding When Tree of Thoughts Succeeds," arXiv 2410.17820, October 2024. https://arxiv.org/abs/2410.17820

- "The generator plays a more critical role than the discriminator in driving the success of ToT." [Sourced]
- Scaling the generator produces substantial gains even with smaller discriminators; enlarging the discriminator alone yields marginal improvements. [Sourced]
- [Inference: this cuts against designs that invest heavily in a separate evaluator while keeping the generator cheap.]

### CoVerRL: Co-Evolution

**Source:** "CoVerRL: Breaking the Consensus Trap in Label-Free Reasoning via Generator-Verifier Co-Evolution," arXiv 2603.17775, March 2026. https://arxiv.org/abs/2603.17775

- Proposes co-evolving generator and verifier to break the "consensus trap" where both converge on the same errors. [Sourced]
- [Inference: this is the strongest current attempt to overcome the shared-blind-spot problem of same-model verification.]

---

## 5. Self-Verification Weakness

### Self-Correction Failure

**Source:** Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet," ICLR 2024. https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4add8b0aa8749d80a34ca5d941c355-Abstract-Conference.html

- GPT-4 drops from 95.5% to 91.5% on GSM8K when asked to self-correct without external feedback. [Sourced]
- Intrinsic self-correction fails and can degrade accuracy. [Sourced]
- Models repair errors when location is given but cannot find error locations independently. [Sourced]
- Gains come from outside the model: tool-interactive critic, execution signal, or a corrector instilled at training time. [Sourced]

### The Self-Correction Illusion

**Source:** "The Self-Correction Illusion: LLMs Correct Others but Not Themselves," arXiv 2606.05976, June 2026. https://arxiv.org/abs/2606.05976

- 10 models (GPT-4o, Claude Sonnet 4, Gemini 2.5 Flash, open-weight 7B--72B). Byte-identical errors tested in 5 role conditions. [Sourced]
- Self-correction in own `<thought>`: 0--53% (median ~17%). [Sourced]
- Relabeled as external `<memory>`: median +53.3 pp lift (10/13 cells significant at p<0.001). [Sourced]
- Role tag alone accounts for ~30 pp of the lift. [Sourced]
- Self-Refine, Reflexion, Chain-of-Verification all produced negative or small lifts. [Sourced]
- Self-correction failure is largely an artifact of role labeling, not a fundamental cognitive deficit. [Sourced]
- [Inference: a separate verifier may help not because it is smarter, but because the same model treats externally-attributed claims differently.]

### Error Localization as Bottleneck

**Source:** "LLMs cannot find reasoning errors, but can correct them given the error location," arXiv 2311.08516, November 2023. https://arxiv.org/pdf/2311.08516

- Error localization is the bottleneck, not error correction ability. [Sourced]

---

## 6. Plan/Act/Review in Coding Agents (2025--2026)

### Aider Architect/Editor

**Source:** Aider documentation and benchmarks, September 2024 onward. https://aider.chat/docs/usage/modes.html ; https://aider.chat/2024/09/26/architect.html

- **Architect model** proposes changes in natural language; **editor model** translates proposals into file edits. [Sourced]
- Published benchmarks (strongest per-pattern evidence found):
  - o1-preview architect + o1-mini editor: **85.0%** vs o1-mini solo: **61.1%** (+23.9 pp). [Sourced]
  - Same-model architect/editor: +3.1 pp. Cross-model: +7.6 pp average. [Sourced from fork]
  - Especially useful when the reasoning model (e.g., o1) is strong at reasoning but weak at edit formatting. [Sourced]

Units: architect (planner), editor (executor).
Composition: two-stage pipeline.
Boundary-crossing: natural-language change proposal.

### Claude Code

Plan mode (read-only) -> Act (write/execute) -> Review (subagent or human). Subagents: Explore, Plan, General-purpose, each isolated. Dynamic Workflows for parallel fan-out. See section 2 for detail. [Sourced]

No published ablation comparing separated vs single-pass. [Observation]

### OpenAI Codex

Flat iterative loop without explicit plan/act separation. Three approval modes. See section 2 for detail. [Sourced]

### Cursor (2025--2026)

**Source:** Cursor documentation and reports, 2025--2026. [Sourced from fork]

- Agent-first architecture (Cursor 3, April 2026): up to 8 parallel agents in isolated Ubuntu VMs. [Sourced]
- Background Agent runs asynchronously in cloud: takes GitHub issues, produces draft PRs. [Sourced]
- In-house Composer model (Kimi K2.5 + Cursor RL fine-tuning). [Sourced]

### OpenHands (formerly OpenDevin)

**Source:** https://frontman.sh/blog/best-open-source-ai-coding-tools-2026/

- Event-driven loop with Action/Observation protocol. [Sourced]
- Supports hierarchical agent delegation (macro/micro agents). [Sourced]
- ~77% SWE-Bench Verified with Sonnet 4.5. [Sourced]

### Devin

**Source:** Cognition Labs reports, 2025--2026. [Sourced from fork]

- Compound AI system with specialized models: Planner, Coder, Critic, Browser. [Sourced]
- "Devin Fusion" pairs frontier + helper models for cost efficiency. [Sourced]
- Dynamic re-planning when plans fail. [Sourced]
- PR merge rate improved from 34% to 67% year-over-year. [Sourced]
- Spawns parallel child agents for complex tasks. [Sourced]

### SWE-Search / Moatless

**Source:** SWE-Search, ICLR 2025. [Sourced from fork]

- Monte Carlo Tree Search (MCTS) over action types (Search, Plan, Edit). [Sourced]
- Tree-structured state with per-node file snapshots. [Sourced]
- Flexible Plan transitions risk infinite loops. [Sourced]

### Cross-Cutting Empirical Findings for Coding Agents

**Scaffold taxonomy** (Rombaut, April 2025): 5 composable loop primitives (ReAct, generate-test-repair, plan-execute, multi-attempt retry, tree search). 11 of 13 surveyed agents compose multiple primitives -- no agent uses just one. [Sourced from fork]

**Plan compliance** (April 2025): Plans improve performance, but misaligned plans hurt more than no plans. Even usually-ignored plan phases matter when removed. [Sourced from fork]

**Action bias** (May 2026): Agents modify already-correct code 35--65% of the time. Fixing over-action creates under-action. [Sourced from fork]

**Maker-checker** (July 2026): Self-approval causes grade drift without quality gain. Separate critic needed. 70% of production loops use deterministic verification rather than LLM-based review. [Sourced from fork]

---

## 7. Difficulty and Effort Routing

### RouteLLM

**Source:** RouteLLM, LMSYS/Anyscale, June 2024 (accepted ICLR 2025). https://arxiv.org/abs/2406.18665 ; https://www.lmsys.org/blog/2024-07-01-routellm/

Units: a router (small classifier) plus a pool of candidate LLMs (typically binary: one strong, one weak).
Composition: single-stage routing -- the router classifies each query before any LLM processes it.
Boundary-crossing: only the query. The router outputs a binary or categorical routing decision.
Selection: routers trained on human preference data (Chatbot Arena).

Evidence:
- >2x cost reduction maintaining quality. [Sourced]
- BERT classifier variant runs <10ms. [Sourced]
- Only 14% of queries sent to strong model while maintaining 95% of GPT-4 performance on MT Bench. [Sourced]
- Router architectures tested: matrix factorization, BERT classifier, causal LLM, SW ranking. [Sourced]

**Key limitation (sourced):** "Several routing methods are evaluated on a fixed set of LLMs and struggle to generalize" to unseen models. [Sourced: survey at https://arxiv.org/html/2603.04445v2]

### RouteLLM Successors (2025--2026)

- **BEST-Route** (Microsoft, June 2025): multi-head DeBERTa-v3-small router, selects both model and number of responses. Up to 60% cost reduction with <1% performance drop. [Sourced: https://github.com/microsoft/best-route-llm]
- **R2-Reasoner:** 84.46% API cost savings for reasoning tasks. [Sourced: survey]
- **RouteNLP** (April 2026): combines conformal cascading with distillation co-optimization. [Sourced: https://arxiv.org/pdf/2604.23577]
- **ReLope** (March 2026): KL-regularized LoRA probes for multimodal LLM routing. [Sourced: https://arxiv.org/pdf/2603.24787]
- **LLMRouterBench** (January 2026): comprehensive benchmark for evaluating routing methods. [Sourced: https://arxiv.org/pdf/2601.07206]
- **GraphRouter:** Graph neural networks model task-query-LLM relationships. [Sourced: survey]
- **IRT-Router:** Item Response Theory, combining model ability with query difficulty/discrimination. [Sourced: survey]

### Model Cascades

**Source:** Survey: "Dynamic Model Routing and Cascading for Efficient LLM Inference," arXiv 2603.04445, March 2026. https://arxiv.org/abs/2603.04445

Units: ordered sequence of models from cheapest/weakest to most expensive/strongest.
Composition: pipeline with conditional escalation -- a query starts at the weakest model; if confidence is below a threshold, the query escalates.
Boundary-crossing: the original query plus optionally the weaker model's response and confidence score.
Selection: confidence estimation on the weaker model's output (token probabilities, self-consistency, learned probes).

Evidence:
- MixLLM achieved 97.25% of GPT-4 quality at 24.18% of cost. [Sourced]
- Agreement-based cascading (Chuang et al., July 2024): reduces cost by checking if two cheaper models agree before escalating. [Sourced: https://arxiv.org/pdf/2407.02348]
- "Is Escalation Worth It?" (May 2026): decision-theoretic characterization of when cascading is justified. [Sourced: https://arxiv.org/pdf/2605.06350]

**Key limitation (sourced):** Self-reported model confidence has "low alignment between reported uncertainty and prediction correctness." Trained hidden-state probes are more reliable. [Sourced: same survey]

### Adaptive Reasoning Effort

**Production implementations:**
- **Anthropic effort parameter** (2025--2026): five levels (low, medium, high, xhigh, max). Controls all output tokens including thinking, text, and tool calls. Default is "high." At lower effort, the model can skip thinking entirely for simple problems. Per-message effort changes available on Fable 5.1 and Opus 5. `budget_tokens` deprecated on Opus 4.7+, replaced by the effort parameter. [Sourced: https://platform.claude.com/docs/en/build-with-claude/effort]
- **Claude Code subagent effort:** Per-subagent effort and model overrides. [Sourced: https://code.claude.com/docs/en/model-config]

**Research approaches:**
- **TALE** (ACL 2025 Findings): dynamically adjusts reasoning token count based on problem complexity. Reduces output tokens by 67%, costs by 59%, competitive accuracy vs vanilla CoT. [Sourced: https://aclanthology.org/2025.findings-acl.1274/]
- **SelfBudgeter** (ICLR 2026): self-adaptive controllable reasoning. 61% average response length compression on math reasoning while maintaining accuracy. [Sourced: https://arxiv.org/abs/2505.11274]
- **BudgetThinker** (August 2025): control tokens enforce token budgets by truncating and signaling for final answers. [Sourced: https://arxiv.org/html/2508.17196v1]
- **ARES** (March 2026): Adaptive Reasoning Effort Selection for efficient LLM agents. [Sourced: https://arxiv.org/pdf/2603.07915]

**Adaptive reasoning taxonomy** (November 2025): two categories -- training-based (RL, SFT, learned controllers internalize adaptivity) and training-free (prompt conditioning, feedback-driven halting, modular composition). Central problem: current LLMs "apply uniform reasoning strategies regardless of task complexity." [Sourced: https://arxiv.org/abs/2511.10788]

### Compute-Optimal Test-Time Scaling

**Source:** Snell et al., "Scaling LLM Test-Time Compute Optimally," arXiv 2408.03314, August 2024 (ICLR 2025). https://arxiv.org/abs/2408.03314

Three regimes: (i) parallel scaling (multiple independent samples + consensus/verification), (ii) sequential scaling (iterative refinement, hierarchical pruning), (iii) internal scaling (model adjusts generation depth per task).

Key findings:
- A 14x smaller model can match a larger model's performance through strategic test-time compute allocation. [Sourced]
- Optimal allocation varies per problem difficulty and verifier quality. [Sourced]
- "The effectiveness of different approaches to scaling test-time compute critically varies depending on the difficulty of the prompt." [Sourced]

**"Can 1B LLM Surpass 405B LLM?"** (February 2025, arXiv 2502.06703): Under compute-optimal TTS, a 0.5B model outperforms GPT-4o, a 3B model surpasses 405B, a 7B model beats o1 and DeepSeek-R1 on MATH-500. Strategy is context-dependent, not universally prescribed. [Sourced: https://arxiv.org/abs/2502.06703]

### The Overthinking Problem

**Source:** "When More Thinking Hurts," April 2026. https://arxiv.org/abs/2604.10739

- Marginal returns diminish substantially at higher token budgets. [Sourced]
- Easier problems reach negative marginal utility earlier than hard problems. [Sourced]
- A "negative flip" occurs: the model reaches the right answer early, then talks itself out of it with more tokens. [Sourced]
- Extended thinking becomes harmful on average around 7K tokens. [Sourced]
- Anthropic's own documentation acknowledges: `max` effort "on some structured-output or less intelligence-sensitive tasks can lead to overthinking." [Sourced: https://platform.claude.com/docs/en/build-with-claude/effort]

[Inference: this provides the empirical basis for difficulty-routing: uniform compute allocation is demonstrably suboptimal. The optimal thinking budget depends on problem difficulty, which must be estimated before or early in solving.]

### Difficulty Estimation Methods

**Source:** Survey at https://arxiv.org/html/2603.04445v2 and individual papers.

Methods catalogued:
1. Heuristic signals (text length, word rarity, syntactic complexity). [Sourced: survey]
2. Learned classifiers (DeBERTa-based routers). [Sourced: survey]
3. LLM-as-judge (stronger model evaluates difficulty). [Sourced: survey]
4. Matrix factorization (EmbedLLM learns model embeddings). [Sourced: survey]
5. In-context capabilities (ICL-Router uses query-performance pairs). [Sourced: survey]
6. Graph neural networks (GraphRouter). [Sourced: survey]
7. Item Response Theory (IRT-Router). [Sourced: survey]
8. Hidden-state probes: "LLMs Encode How Difficult Problems Are" -- difficulty information is present in hidden states before generation begins. [Sourced: https://arxiv.org/pdf/2510.18147, October 2025]
9. Pre-generation confidence: "Can Confidence Estimates Decide When Chain-of-Thought Is Necessary?" [Sourced: https://arxiv.org/pdf/2510.21007, October 2025]

---

## 8. Thought-Structure Ontologies

### Tree of Thoughts (ToT)

**Source:** Yao et al., NeurIPS 2023. Successors: ToTRL (arXiv 2505.12717, May 2025), Multi-Agent ToT with Validator, Semantic-pruned ToT. https://arxiv.org/abs/2505.12717

Units: thought nodes (partial reasoning steps).
Composition: tree search (BFS/DFS) with LLM-generated evaluations at each node.
Boundary-crossing: parent thought -> child thoughts; evaluator scores per node.
Selection: the LLM generates candidate next thoughts and evaluates them.

Evidence:
- ToTRL (May 2025): trains ToT via RL on puzzle-solving; ToTQwen3-8B matches GLM-4-Z1-9B on AIME 2024. [Sourced]
- Multi-Agent ToT with Validator: multiple Reasoner agents run ToT searches; a Thought Validator discards faulty explanations; +5.6% over standard ToT on GSM8K. [Sourced]
- Semantic-pruned ToT: 2.3x speedup via dense embedding clustering, matching accuracy on GSM8K and MATH500. [Sourced]

### Graph of Thoughts (GoT)

**Source:** Besta et al., AAAI 2024. Enhanced GoT at ICLR 2025. https://dl.acm.org/doi/10.1609/aaai.v38i16.29720 ; https://openreview.net/pdf?id=l32IrJtpOP

Units: thoughts as vertices, dependencies as edges in an arbitrary graph.
Composition: graph with merging, splitting, and recurrence (not limited to tree structure).
Boundary-crossing: thought dependencies; novel "transformations" combine thoughts into synergistic outcomes.
Key advantage: decompose complex tasks into subtasks, solve independently, merge results.

### Forest of Thoughts (FoT)

**Source:** Bi et al., "Forest-of-Thought: Scaling Test-Time Compute for Enhancing LLM Reasoning," arXiv 2412.09078, December 2024 (ICML 2025). https://arxiv.org/abs/2412.09078

Units: multiple reasoning trees, each an independent search.
Composition: forest (ensemble of trees) with sparse activation, dynamic self-correction, and consensus-guided decision-making.
Boundary-crossing: consensus mechanism selects across trees.
Advantage over ToT: multiple passes with error correction, not single-pass.

### What Came After (2025--2026)

- **MTMT** (arXiv 2412.03987, December 2024): consolidates multiple thinking modes into a thought tree. [Sourced: https://arxiv.org/abs/2412.03987]
- **Layer-of-Thoughts (LoT)** (arXiv 2410.12153, October 2024): constraint hierarchies with retrieval. [Sourced: https://arxiv.org/abs/2410.12153]
- [Inference: the trajectory from CoT -> ToT -> GoT -> FoT represents increasing structural freedom in the reasoning graph: chain -> tree -> arbitrary graph -> ensemble of trees/graphs. Each step adds flexibility at the cost of search complexity.]

---

## 9. Mixture of Agents (MoA) and Debate

### Mixture of Agents

**Source:** Wang et al., "Mixture-of-Agents Enhances Large Language Model Capabilities," arXiv 2406.04692, June 2024. https://arxiv.org/abs/2406.04692 ; https://github.com/togethercomputer/moa

Units: LLM agents arranged in layers; each layer has multiple agents.
Composition: layered pipeline; each agent in layer N takes all outputs from layer N-1 as auxiliary context.
Boundary-crossing: natural-language outputs from all agents in the previous layer.
Selection: models chosen for complementary strengths (proposers and aggregators).

Evidence:
- AlpacaEval 2.0: 65.1% (open-source models only) vs GPT-4 Omni's 57.5% -- a 7.6pp improvement. [Sourced]
- Self-MoA (homogeneous) beats Mixed-MoA (heterogeneous) by 6.6pp -- quality matters more than diversity. [Sourced from fork]

### Multi-Agent Debate

**Source:** "Can LLM Agents Really Debate?" arXiv 2511.07784, November 2025. https://arxiv.org/abs/2511.07784

Controlled study using Knight-Knave-Spy logic puzzles:
- "Intrinsic reasoning strength and group diversity are the dominant drivers of debate success." [Sourced]
- "Majority pressure suppresses independent correction" -- agents abandon correct reasoning when outnumbered. [Sourced]
- Structural parameters (argument order, confidence transparency) provide "limited gains." [Sourced]

### Persuasion Overrides Truth

**Source:** Agarwal & Khanna, "When Persuasion Overrides Truth in Multi-Agent LLM Debates," arXiv 2504.00374, April 2025. https://arxiv.org/abs/2504.00374

- Five open-source LLMs (3B--14B), TruthfulQA dataset. [Sourced]
- "Even smaller models can craft persuasive arguments that override truthful answers -- often with high confidence." [Sourced]

### The Deliberative Illusion

**Source:** "The Deliberative Illusion," arXiv 2606.03032, June 2026. https://arxiv.org/abs/2606.03032

- Multi-agent discussion erases up to 72% of issue-critical facts. [Sourced]
- Agents agree more while retaining less. [Sourced]
- Final stances anchored in base-model priors rather than discussion content. [Sourced]

### The Confident Liar

**Source:** "The Confident Liar: Diagnosing Multi-Agent Debate with Log-Probabilities and LLM-as-Judge," arXiv 2606.10296, June 2026. https://arxiv.org/abs/2606.10296

- Agents express high internal confidence while producing flawed reasoning. [Sourced]
- Constructor (proposer) confidence correlates with reasoning quality ~2x more strongly than Auditor. [Sourced]
- Critical failure detection: Constructor AUROC 0.804 vs Auditor 0.634 using confidence signals. [Sourced]

### Group Conformity

**Source:** ACL 2025 Findings. https://aclanthology.org/2025.findings-acl.265.pdf

- LLMs exhibit conformity to majority regardless of correctness. [Sourced]
- Conformity strengthens with rounds and peer pressure. [Sourced]

[Inference: debate produces illusory consensus -- conformity without genuine deliberation. Functions closer to ensembling than reasoning. Strong evidence against same-model debate as a diversity mechanism.]

---

## 10. MetaGPT-Style SOP Roles

**Source:** Hong et al., "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," arXiv 2308.00352 (ICLR 2024 Oral, #1 in LLM-based Agent category). https://arxiv.org/abs/2308.00352

Units: software-process roles -- Product Manager, Architect, Engineer, QA, etc.
Composition: pipeline following a Standard Operating Procedure; each role produces artifacts consumed by the next.
Boundary-crossing: structured intermediate artifacts (PRDs, design docs, code, test reports) via a publish-subscribe global message pool.
Selection: roles are fixed by the SOP; the SOP itself is the program.

Central thesis: `Code = SOP(Team)`.

### AFlow (ICLR 2025)

**Source:** MetaGPT team, AFlow framework, ICLR 2025.

- Automatically optimizes agent workflows by searching the space of possible SOP configurations. [Sourced]
- [Inference: this moves from hand-designed SOPs to learned ones, but retains the role-based decomposition.]

---

## 11. Society of Mind / Internal Dialogue

**Source:** "Beyond Self-Talk: A Communication-Centric Survey of LLM-Based Multi-Agent Systems," arXiv 2502.14321, February 2025. https://arxiv.org/abs/2502.14321 ; "Language Model Agents in 2025: Society Mind Revisited," iSolutions/Medium. https://isolutions.medium.com/language-model-agents-in-2025-897ec15c9c42

- Multiple LLM agents interact in turns (argue, critique, propose), producing emergent reasoning. [Sourced]
- Multi-agent discussion outperformed single-agent chain-of-thought on benchmarks with no additional human data. [Sourced: iSolutions article citing 2024 studies]
- Related to Minsky's "Society of Mind": collective intelligence from mediocre individuals. [Sourced]

Units: agents with distinct personas/roles in dialogue.
Composition: conversational loop (sequential turns) or structured debate.
Boundary-crossing: natural-language messages.
Selection: personas are assigned by prompt; number of agents is a hyperparameter.

- **MIND** (arXiv 2502.19860, February 2025): multi-agent inner dialogue for psychological healing, with specialized agents (devil agent, compassion agent). [Sourced: https://arxiv.org/abs/2502.19860]

---

## 12. Hierarchical Planning in LLM Agents

### HiPlan (August 2025)

**Source:** Li et al., "HiPlan: Hierarchical Planning for LLM-Based Agents with Adaptive Global-Local Guidance," arXiv 2508.19076. https://arxiv.org/abs/2508.19076

- Global: milestone action guides (roadmap of critical task stages). [Sourced]
- Local: step-wise hints (real-time fine-grained feedback). [Sourced]
- Milestone library built from expert demonstrations; retrieval-augmented. [Sourced]
- Outperforms classic subgoal decomposition and uniform strategy assignment on long-horizon tasks. [Sourced]

Units: milestone planner (global) + step-wise executor (local).
Composition: two-level hierarchy with dynamic adaptation.

### HTN + LLM Integration

**Source:** "Hierarchical Task Network Planning with LLM-Generated Heuristics," arXiv 2605.07707, June 2026. https://arxiv.org/abs/2605.07707 ; "Online Learning of HTN Methods for Integrated LLM-HTN Planning," arXiv 2511.12901, November 2025. https://arxiv.org/abs/2511.12901

- ChatHTN: interleaves approximate (LLM) and symbolic HTN planning. [Sourced]
- LLMs generate heuristics for HTN decomposition. [Sourced]
- [Inference: this is the most direct integration of classical AI planning (HTN) with LLM reasoning.]

### HALO (May 2025)

**Source:** "HALO: Hierarchical Autonomous Logic-Oriented Orchestration for Multi-Agent LLM Systems," arXiv 2505.13516. https://arxiv.org/abs/2505.13516

- Hierarchical orchestration with logic-oriented task decomposition. [Sourced]

### Agent-Oriented Planning (AOP)

**Source:** Li et al., 2024. Referenced in emergentmind.com survey.

- Meta-agent decomposes user queries into sub-tasks allocated to agents based on solvability, completeness, and non-redundancy. [Sourced]

---

## 13. Context Contamination and Tool-Presence Bias

### Structural Alignment Bias

**Source:** "Do LLMs Know Tool Irrelevance? Demystifying Structural Alignment Bias in Tool Invocations," arXiv 2604.11322, April 2025 (ACL 2026). https://arxiv.org/abs/2604.11322

- SABEval benchmark: 5,050+ instances, Qwen3 (4B/8B/14B), ToolACE, Watt-Tool. [Sourced]
- Random tool pairing: <0.2% invocation. Structurally aligned but irrelevant: **41.9%**. High alignment: **90.4%**. [Sourced]
- Counterfactual parameter substitution: 58--83% reduction (causal link established). [Sourced]
- Two competing internal pathways: semantic verification vs structural matching. Structural matching often dominates. [Sourced]

[Inference: this is a direct argument for separating "should I act?" from "which tool?" -- having tools in context contaminates the decision about whether to use one.]

### BiasBusters

**Source:** BiasBusters, ICLR 2026. https://proceedings.iclr.cc/paper_files/paper/2026/file/a79875cc0d046ce7ce65f03f3affaa9e-Paper-Conference.pdf

- Semantic similarity is strongest predictor of spurious invocation. [Sourced]
- Positional bias: middle-of-list tools chosen 22--52% vs 31--32% at extremes. [Sourced]

### The Tool-Use Tax

**Source:** "Are Tools All We Need? Unveiling the Tool-Use Tax in LLM Agents," arXiv 2605.00136, May 2025. https://arxiv.org/abs/2605.00136

- The tool-calling protocol itself introduces a performance penalty. [Sourced]
- Factorized Intervention Framework isolates: prompt formatting costs, protocol overhead, actual tool benefit. [Sourced]
- When semantic distractors are present, protocol-induced errors often negate tool benefits. [Sourced]

### Governance Decay

**Source:** "Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents," arXiv 2606.22528, June 2026. https://arxiv.org/abs/2606.22528

- Violation rates rise from 0% (policy visible) to 30% after context compaction, reaching 59% for some models. [Sourced]
- Violations 8.3x larger for soft organizational policies than hard safety norms. [Sourced]
- Constraint pinning (re-injecting rules after compaction) restores 0% violation. [Sourced]

---

## 14. Multi-Agent vs. Single-Agent: When Separation Helps

### The Illusion of Multi-Agent Advantage

**Source:** Tran & Kiela, April 2025. https://www.researchgate.net/publication/403529711

- Information-theoretic argument (Data Processing Inequality): each additional agent is a lossy transformation. [Sourced]
- Qwen3, DeepSeek-R1-Distill-Llama, Gemini 2.5; 5 multi-agent variants. Single agent matches or exceeds multi-agent at equal token budgets. [Sourced]
- Most published comparisons let multi-agent spend 2--4x more tokens. [Sourced]

**Source:** "The Illusion of Multi-Agent Advantage," arXiv 2606.13003, June 2026. https://arxiv.org/pdf/2606.13003

- GPQA, SWE-bench, BrowseComp+, financial analysis on Claude models. No consistent multi-agent advantage. [Sourced]

### When Multi-Agent Does Help

**Source:** "Beyond the Strongest LLM," arXiv 2509.23537, September 2025. https://arxiv.org/pdf/2509.23537

- Multi-agent CAN rival strongest single LLM when subtasks execute simultaneously and independently. [Sourced]
- When they cannot, coordination hurts. [Sourced]

### Controlled Evaluation

**Source:** "Do More Agents Help?" arXiv 2606.05670, June 2026. https://arxiv.org/abs/2606.05670

- Under controlled conditions (BenchAgent framework, GPT-4.1), at most 1 of 6 tested MAS exceeds the matched single-agent anchor on benchmark-balanced average accuracy. [Sourced]
- Five MAS approaches underperformed by 2.56--11.29 percentage points while consuming more resources. [Sourced]
- A Claude-Code-style runtime workflow reached 66.72% on GAIA, substantially outperforming fixed multi-agent baselines. [Sourced]

### Role Ablation Studies

**Source:** "Agents that Matter," arXiv 2605.27621, May 2025. https://arxiv.org/abs/2605.27621

- Systematic removal of roles: planning/coordination roles show 15--40% accuracy drops. Auxiliary roles: <5% drops. [Sourced]
- Leave-One-Out identifies bottleneck agents as effectively as combinatorial methods. [Sourced]
- Replacing low-contribution agents boosts pass@1 from 62% to 79% while cutting closed-source token usage by 38%. [Sourced]

**Source:** "Planner Matters!" arXiv 2605.02168, May 2025. https://arxiv.org/html/2605.02168v1

- Planner removal: accuracy drops from 85.71% to 12.86%. [Sourced]
- Planner scaling yields largest marginal gains of any role. [Sourced]

**Source:** MARS, arXiv 2503.16874, March 2025. https://arxiv.org/pdf/2503.16874

- Critic removal had least impact in some systems, second-largest in others. Inconsistent across architectures. [Sourced]

### ReAct Interleaving and Its Limits

- Interleaving reasoning with action improves multi-step task success and suppresses hallucinations. [Sourced: emergentmind.com surveys]
- Costs: extra inference per step; little parallelism; increasing tool-selection brittleness as tool surface grows. [Sourced]
- "Inefficient on tasks whose workflow is largely predictable in advance." [Sourced]
- ReWOO (non-interleaved) reduces token usage 30--50% vs. ReAct but is brittle to unexpected observations. [Sourced: https://theaiengineer.substack.com/p/the-4-single-agent-patterns]
- [Inference: neither interleaved nor separated dominates. Interleaving helps adaptability but hurts efficiency and scaling.]

---

## 15. Disagreements and Unknowns

### Sharp Disagreements

1. **Does multi-agent help?** The scaling study (2512.08296) shows +80.8% for decomposable tasks but -70.0% for sequential planning. The controlled evaluation (2606.05670) finds at most 1 of 6 MAS beats a single agent. Tran & Kiela (2025) argue from information theory that it should not help (DPI). "Beyond the Strongest LLM" (2509.23537) says it helps with genuinely independent subtasks. Enterprise adoption grew 327% in four months despite this evidence. [Sourced: all four.]

2. **Generator vs. verifier investment:** The ToT study (2410.17820) says the generator is the bottleneck, not the discriminator. The GV-gap literature (2509.17995) says strong verifiers offer limited advantage over weak ones. But CoVerRL (2603.17775) argues co-evolution is needed to avoid consensus traps. These pull in different directions on where to allocate model capacity.

3. **Debate reliability:** The controlled debate study (2511.07784) says diversity and capability matter, not procedure. The persuasion study (2504.00374) says debate amplifies bluster. The Deliberative Illusion (2606.03032) says it erases up to 72% of facts. Neither finds a regime where debate reliably outperforms single-agent reasoning on hard tasks.

4. **Self-correction feasibility:** The self-correction illusion paper (2606.05976) says role relabeling restores correction (+53 pp median). The ICLR 2024 paper says self-correction degrades accuracy. These may be reconciled by the role-labeling mechanism: the same model can correct if it believes the content is external, but cannot correct what it recognizes as its own. Whether training-time verification instillation survives this is unknown.

5. **Planner as separate role:** Planner ablation shows 85.71%->12.86% accuracy collapse (2605.02168). But Anthropic's "start simple" principle says add complexity only when demonstrated. Resolution appears task-dependent: complex multi-step tasks collapse without planning; simple tasks gain nothing from it. No predictive theory for the boundary.

6. **Critic importance:** MARS (2503.16874) finds critic removal has least impact in some systems, second-largest in others. The maker-checker finding (July 2026) says self-approval causes grade drift. Deterministic verification (test execution) outperforms LLM-based review in 70% of production loops. The critic's value depends on whether it has access to an external signal.

### What Is Unknown

- **Optimal granularity of decomposition:** No study provides a principled method for deciding how many units a task should be split into. The answer appears task-dependent but no predictive theory exists.
- **Difficulty estimation on novel tasks:** Compute-optimal scaling assumes difficulty can be estimated before solving. How well this works on truly novel tasks (vs. well-benchmarked domains) is unknown.
- **Context-crossing cost:** What is lost in the boundary between units? Governance decay shows constraints are lost in compaction. Tool-presence bias shows tools distort reasoning. No unified theory of what should and should not cross boundaries.
- **Composition beyond two levels:** Most systems have at most two levels (orchestrator + workers, architect + editor). Whether deeper hierarchies help is tested only in HiPlan's global-local decomposition, not in three-or-more-level designs.
- **Whether role-label self-correction weakness persists after training-time verification instillation.**
- **Exact compute threshold where multi-agent outperforms single-agent.**
- **Whether structural alignment bias is a training artifact or architectural inevitability.**

---

## Sources

- Anthropic. "Building Effective Agents." December 2024. https://www.anthropic.com/research/building-effective-agents
- Andrew Ng. Agentic design patterns. March 2024. https://x.com/AndrewYNg/status/1773393357022298617
- OpenAI. "New tools for building agents." March 2025. https://openai.com/index/new-tools-for-building-agents/
- OpenAI. "Introducing Codex." May 2025. https://openai.com/index/introducing-codex/
- Wang et al. "Mixture-of-Agents Enhances Large Language Model Capabilities." arXiv 2406.04692, June 2024. https://arxiv.org/abs/2406.04692
- RouteLLM. arXiv 2406.18665, June 2024 (ICLR 2025). https://arxiv.org/abs/2406.18665
- Snell et al. "Scaling LLM Test-Time Compute Optimally." arXiv 2408.03314, August 2024 (ICLR 2025). https://arxiv.org/abs/2408.03314
- "Understanding When Tree of Thoughts Succeeds." arXiv 2410.17820, October 2024. https://arxiv.org/abs/2410.17820
- Bi et al. "Forest-of-Thought." arXiv 2412.09078, December 2024 (ICML 2025). https://arxiv.org/abs/2412.09078
- Besta et al. "Graph of Thoughts." AAAI 2024. https://dl.acm.org/doi/10.1609/aaai.v38i16.29720
- Hong et al. "MetaGPT." arXiv 2308.00352 (ICLR 2024). https://arxiv.org/abs/2308.00352
- Aider architect/editor. September 2024. https://aider.chat/2024/09/26/architect.html
- Huang et al. "Large Language Models Cannot Self-Correct Reasoning Yet." ICLR 2024.
- "LLMs cannot find reasoning errors, but can correct them given the error location." arXiv 2311.08516, November 2023. https://arxiv.org/pdf/2311.08516
- Agarwal & Khanna. "When Persuasion Overrides Truth." arXiv 2504.00374, April 2025. https://arxiv.org/abs/2504.00374
- Tran & Kiela. "The Illusion of Multi-Agent Advantage." April 2025. https://www.researchgate.net/publication/403529711
- "Structural Alignment Bias in Tool Invocations." arXiv 2604.11322, April 2025 (ACL 2026). https://arxiv.org/abs/2604.11322
- "Are Tools All We Need?" arXiv 2605.00136, May 2025. https://arxiv.org/abs/2605.00136
- "Agents that Matter." arXiv 2605.27621, May 2025. https://arxiv.org/abs/2605.27621
- "Planner Matters!" arXiv 2605.02168, May 2025. https://arxiv.org/abs/2605.02168
- MARS. arXiv 2503.16874, March 2025. https://arxiv.org/pdf/2503.16874
- "Variation in Verification." arXiv 2509.17995, September 2025 (ICLR 2026). https://arxiv.org/abs/2509.17995
- "Shrinking the Generation-Verification Gap." arXiv 2506.18203, June 2025. https://arxiv.org/abs/2506.18203
- Generative Verifiers. ICLR 2025. https://openreview.net/attachment?id=Ccwp4tFEtE&name=pdf
- SelfBudgeter. arXiv 2505.11274, May 2025 (ICLR 2026). https://arxiv.org/abs/2505.11274
- TALE. ACL 2025 Findings. https://aclanthology.org/2025.findings-acl.1274/
- BudgetThinker. arXiv 2508.17196, August 2025. https://arxiv.org/html/2508.17196v1
- ARES. arXiv 2603.07915, March 2026. https://arxiv.org/pdf/2603.07915
- Adaptive reasoning taxonomy. arXiv 2511.10788, November 2025. https://arxiv.org/abs/2511.10788
- "Can 1B LLM Surpass 405B LLM?" arXiv 2502.06703, February 2025. https://arxiv.org/abs/2502.06703
- "When More Thinking Hurts." arXiv 2604.10739, April 2026. https://arxiv.org/abs/2604.10739
- Anthropic effort parameter docs. https://platform.claude.com/docs/en/build-with-claude/effort
- "Can LLM Agents Really Debate?" arXiv 2511.07784, November 2025. https://arxiv.org/abs/2511.07784
- "The Deliberative Illusion." arXiv 2606.03032, June 2026. https://arxiv.org/abs/2606.03032
- "The Confident Liar." arXiv 2606.10296, June 2026. https://arxiv.org/abs/2606.10296
- Group Conformity. ACL 2025 Findings. https://aclanthology.org/2025.findings-acl.265.pdf
- "Towards a Science of Scaling Agent Systems." arXiv 2512.08296, December 2025. https://arxiv.org/abs/2512.08296
- "Beyond the Strongest LLM." arXiv 2509.23537, September 2025. https://arxiv.org/pdf/2509.23537
- "The Illusion of Multi-Agent Advantage." arXiv 2606.13003, June 2026. https://arxiv.org/pdf/2606.13003
- "Do More Agents Help?" arXiv 2606.05670, June 2026. https://arxiv.org/abs/2606.05670
- "The Self-Correction Illusion." arXiv 2606.05976, June 2026. https://arxiv.org/abs/2606.05976
- "Dynamic Model Routing and Cascading." arXiv 2603.04445, March 2026. https://arxiv.org/abs/2603.04445
- "CoVerRL." arXiv 2603.17775, March 2026. https://arxiv.org/abs/2603.17775
- BEST-Route. Microsoft, June 2025. https://github.com/microsoft/best-route-llm
- LLMRouterBench. arXiv 2601.07206, January 2026. https://arxiv.org/pdf/2601.07206
- RouteNLP. arXiv 2604.23577, April 2026. https://arxiv.org/pdf/2604.23577
- ReLope. arXiv 2603.24787, March 2026. https://arxiv.org/pdf/2603.24787
- Hidden-state difficulty probes. arXiv 2510.18147, October 2025. https://arxiv.org/pdf/2510.18147
- Confidence estimates for CoT. arXiv 2510.21007, October 2025. https://arxiv.org/pdf/2510.21007
- "Governance Decay." arXiv 2606.22528, June 2026. https://arxiv.org/abs/2606.22528
- BiasBusters. ICLR 2026. https://proceedings.iclr.cc/paper_files/paper/2026/file/a79875cc0d046ce7ce65f03f3affaa9e-Paper-Conference.pdf
- "HiPlan." arXiv 2508.19076, August 2025. https://arxiv.org/abs/2508.19076
- "HTN Planning with LLM-Generated Heuristics." arXiv 2605.07707, June 2026. https://arxiv.org/abs/2605.07707
- "Online Learning of HTN Methods." arXiv 2511.12901, November 2025. https://arxiv.org/abs/2511.12901
- HALO. arXiv 2505.13516, May 2025. https://arxiv.org/abs/2505.13516
- "Beyond Self-Talk." arXiv 2502.14321, February 2025. https://arxiv.org/abs/2502.14321
- MIND. arXiv 2502.19860, February 2025. https://arxiv.org/abs/2502.19860
- ToTRL. arXiv 2505.12717, May 2025. https://arxiv.org/abs/2505.12717
- Enhanced GoT. ICLR 2025. https://openreview.net/pdf?id=l32IrJtpOP
- MTMT. arXiv 2412.03987, December 2024. https://arxiv.org/abs/2412.03987
- Layer-of-Thoughts. arXiv 2410.12153, October 2024. https://arxiv.org/abs/2410.12153
- GeoJSON Agents. arXiv 2509.08863. https://arxiv.org/abs/2509.08863
- "Is Escalation Worth It?" arXiv 2605.06350, May 2026. https://arxiv.org/pdf/2605.06350
- Agreement-based cascading. arXiv 2407.02348, July 2024. https://arxiv.org/pdf/2407.02348
- Scaffold taxonomy (Rombaut). April 2025. [Sourced from fork]
- Aider documentation. https://aider.chat/docs/usage/modes.html
- "When to Think Deeply: Inhibitory Deliberation." arXiv 2606.06745, June 2026. https://arxiv.org/abs/2606.06745
- Multi-Agent Verification. arXiv 2502.20379, February 2025. https://arxiv.org/pdf/2502.20379
