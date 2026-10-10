# Multi-Agent Setup Homogeneity: Four Papers

**Flow:** b9f4f6  
**Question:** In the experiments that found multi-agent systems doing no better or worse than a single agent, did every agent share the same base model and the same top-of-context (system prompt, role instructions, tools), or were the agents' top layers specialized per job?

Observations (quotes) and facts are reported as found. Inference is marked separately. Quotes were obtained through the WebFetch HTML reader; exact typographic fidelity cannot be guaranteed for all passages, but content accuracy is assessed as high based on corroboration across fetches.

---

## Paper 1: "Towards a Science of Scaling Agent Systems" (arXiv 2512.08296, Anthropic, Dec 2025)

**Source:** https://arxiv.org/html/2512.08296

### Models Used

Three families, three tiers each:
- OpenAI: "GPT-5-nano, GPT-5-mini, GPT-5"
- Google: "Gemini-2.0 Flash, Gemini-2.5 Flash, Gemini-2.5 Pro"
- Anthropic: "Claude Sonnet 3.7, Claude Sonnet 4, Claude Sonnet 4.5"

### Whether All Agents in One Configuration Share the Same Model

The paper does not explicitly state this. What it does state is: "instantiated across three major LLM families (OpenAI, Google, Anthropic) sampling models at varying capability tiers." This describes cross-family variation, not intra-configuration variation. Whether agents within a single multi-agent run use the same or different model variants is **not stated**.

### System Prompts / Role Instructions

No prompt text is provided. Agents are defined formally: "each agent $a_i$ is defined as a tuple $S_i = (\Phi_i, \mathcal{A}_i, M_i, \pi_i)$" — symbolic, not textual. The paper maintains "identical task prompts, tools, and computational budgets across all configurations, while systematically varying only coordination structure and model capability." This refers to task-level uniformity; it does not resolve whether coordination agents (orchestrators vs. subagents) received different role instructions internally.

### Tools Per Agent

"identical tool APIs and observation structures for all architectures to eliminate confounds from external feedback quality." Tool counts varied by benchmark (2–16 tools) but no differential tool assignment across agent roles is described.

### Specialization Varied?

The paper explicitly names specialization as a distinct dimension it did **not** vary: "Our taxonomy focuses on _communication topology_: one of several orthogonal MAS design dimensions including agent specialization." The five architectures (Single, Independent, Centralized, Decentralized, Hybrid) are topological, not role-specialized. No "analyst" vs. "verifier" differentiation appears.

### Author Statement on Homogeneity as Limitation

The Limitations section (Section 5) is referenced in the table of contents but its full text was not accessible in the HTML fetch. No explicit author statement identifying agent homogeneity as a limitation was found in the retrievable portion.

**What the paper does not state:** Whether agents within one architecture run identical or different model variants; actual prompt text given to any agent; whether role specialization would change the results.

---

## Paper 2: "Do More Agents Help?" (arXiv 2606.05670, June 2026)

**Source:** https://arxiv.org/html/2606.05670

### Models Used

Primary: **GPT-4.1** (gpt-4.1-2025-04-14). Sensitivity checks: **Qwen3-32B** and **GLM-5**.

"All reported main-text BenchAgent results use GPT-4.1."

### Whether All Agents in One Configuration Share the Same Model

Yes, within each system. "All reported main-text BenchAgent results use GPT-4.1" with shared global configuration parameters across all workflows.

### System Prompts / Role Instructions

Prompts differ substantially across systems and roles:

**BenchAgent (single-agent anchor):**  
- "Answer this question correctly. You have all the tools needed."  
- "Always prioritize using available tools over writing custom code."

**ChatEval (fixed MAS, specialized roles):**  
- Math Expert: "analyze mathematically; verify with Python; use web_search"  
- Logic Expert: "analyze logical structure…be extremely concise; no tools"  
- Critical Thinking Expert: "analyze from multiple angles…be extremely concise"

**EvoAgent (evolving MAS, seed prompts via evolutionary search):**  
- EVO-1: "You are a mathematics expert…think step by step"  
- EVO-2: "You are a logical reasoning expert…provide detailed reasoning"  
- EVO-3: "You are a problem-solving expert…clearly show your thinking"

**LLM-Debate:**  
- "You are a helpful AI assistant." (same for all agents — homogeneous)

Role instructions range from a single sentence naming a role to multi-sentence domain-specific directives with tool constraints. This is not a sentence naming a role; ChatEval and EvoAgent have purpose-built per-role programs.

### Tools Per Agent

Yes, tools differ. Most benchmarks use "python_interpreter only." HotpotQA uses "expanded full BenchAgent tool registry." Within ChatEval: Math Expert has Python and web_search; Logic and Critical Thinking experts are "LLM-only" (no tools).

### Specialization Varied?

Yes, implicitly. The paper compares systems with different degrees of specialization (homogeneous LLM-Debate vs. role-specialized ChatEval vs. evolutionarily-generated EvoAgent). Results are task-dependent: "ChatEval gains on IFEval under multi-judge instruction checking" but "collapses on AIME." EvoAgent gains on BBH (94.00% vs. 78.25% baseline) through "prompt-scaffold search." Specialization is a design variable that is compared across systems, not held constant.

### Author Statement on Homogeneity as Limitation

The authors do not explicitly identify agent homogeneity as a limitation. They note "MAS gains are task-dependent."

**What the paper does not state:** Whether any configuration was varied along homogeneity as a controlled dimension; whether homogeneous vs. heterogeneous top-layers were directly compared on the same task.

---

## Paper 3: "The Illusion of Multi-Agent Advantage" (arXiv 2606.13003, June 2026)

**Source:** https://arxiv.org/html/2606.13003v2

### Models Used

"GPT-4o, GPT-5, GPT-OSS-120B, and Gemini-2.5-Pro."

### Whether All Agents in One Configuration Share the Same Model

Yes, with one noted exception. For most systems: same backbone model. For ADAS specifically: "The original work used varied LLMs to reduce costs," but the authors "standardize the backbone to maintain architectural parity" in their evaluation. For DyLAN: "the four agents are configured with a general 'Assistant' role alongside three domain-specific expert roles" but "all use the same backbone model selected per experiment."

### System Prompts / Role Instructions

DyLAN (provided in Table 5):

**Assistant:** "You are a super-intelligent AI assistant capable of performing tasks more effectively than humans."

**Theoretical Physicist:** "You are a Theoretical Physicist…capable of solving graduate-level problems by applying fundamental laws."

**Molecular Chemist:** "You are a Molecular Chemist…integrated principles from across chemistry to provide precise solutions."

**Cellular Biologist:** [domain-specific expertise description — exact text not fully retrieved]

These are purpose-built role programs, not one-sentence labels. For other frameworks (MAS-Zero, ADAS, AFlow, MaAS, MAS-Orchestra), complete prompt text is not provided in the paper.

### Tools Per Agent

Not detailed in the retrievable text.

### Specialization Varied?

Yes, and with a notable result. The paper directly tests role specialization vs. homogeneity within DyLAN: "the all-assistant setting achieved the highest accuracy (54.41%), outperforming task-specific experts (53.40%)." Role specialization did not help; the homogeneous-role configuration outperformed the specialized configuration.

### Author Statement on Homogeneity as Limitation

No explicit sentence naming agent homogeneity of backbone models as a study limitation was found. The paper notes that all agents share the same backbone "to maintain architectural parity" — presented as a methodological choice, not a limitation.

**What the paper does not state:** Whether backbone heterogeneity (different models per agent) would alter results; detailed prompt text for frameworks other than DyLAN.

---

## Paper 4: Tran & Kiela, "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets" (arXiv 2604.02460; ResearchGate 403529711)

**Note on access:** The ResearchGate URL (publication/403529711) returned HTTP 403 Forbidden and full text could not be retrieved from that source. The paper is available on arXiv as 2604.02460. The brief names this paper as "The Illusion of Multi-Agent Advantage (April 2025)" but the arXiv ID 2604 corresponds to April 2026. The brief's title and the arXiv title differ; web search confirms Dat Tran and Douwe Kiela as authors of arXiv 2604.02460 with the DPI argument, and no separate April 2025 paper by those authors under that title was located. The paper below is arXiv 2604.02460; if the brief intends a distinct April 2025 document, its full text is unreachable from available sources.

**Source:** https://arxiv.org/html/2604.02460

### Models Used

"Qwen3-30B-A3B," "DeepSeek-R1-Distill-Llama-70B," "Gemini 2.5 (Flash and Pro versions)."

### Whether All Agents in One Configuration Share the Same Model

Yes. All agents within each system use the same model. No mention of heterogeneous model assignments.

### System Prompts / Role Instructions

Prompts are short but not all identical across roles:

**Single-Agent:** "You are a helpful assistant. Think step by step, then answer. Be as succinct as possible."

**Sequential Planner:** "Break the user task into the fewest necessary sequential steps so each step output feeds the next."

**Parallel-Roles Solver:** "Provide the best possible answer to the question."

**Debate Critic:** "Point out flaws, missing constraints, or alternative reasoning. Then provide a corrected improved answer."

These are functional instructions (one to two sentences per role), not purpose-built domain programs. The roles differ in function description but share a generic format.

### Tools Per Agent

None. The paper "explicitly focuses on text-only multi-hop reasoning with no tool use mentioned for any agent type." Appendix C Limitations states: "(i) We focus on text-only multi-hop reasoning; MAS advantages with tools/vision or safety constraints are out of scope."

### Data Processing Inequality Argument

"By the Data Processing Inequality (DPI), $I(Y;C) \geq I(Y;M)$, and equivalently, $H(Y \mid M) \geq H(Y \mid C)$. Thus, conditioning on M leaves more residual uncertainty about Y than conditioning on C; the multi-agent architecture cannot increase mutual information."

The argument is model-agnostic and applies regardless of whether the agents are homogeneous or heterogeneous, provided agents cannot receive information that was not in the original context.

### Specialization Varied?

Not as a direct experimental variable. The four agent types (single, sequential, parallel, debate) vary in coordination pattern and role instruction, not in domain specialization. Homogeneity of base model is held constant throughout.

### Author Statement on Homogeneity as Limitation

"(i) We focus on text-only multi-hop reasoning; MAS advantages with tools/vision or safety constraints are out of scope."

This acknowledges that the results may not extend to tool-using agents, but does not name agent top-layer homogeneity specifically as a limitation.

**What the paper does not state:** Whether role-specialized or heterogeneously-trained agents would evade the DPI bound (the theoretical argument applies regardless, but empirical results are only for generic-role agents); whether the April 2025 ResearchGate version differs from arXiv 2604.02460.

---

## Cross-Paper Summary

| Paper | Base model same across agents? | Top-layer (role prompts) same? | Tools same per agent? | Specialization tested? |
|---|---|---|---|---|
| 2512.08296 | Not stated | Not stated (task prompt uniform; role prompt not disclosed) | Yes (identical APIs) | No — topology only |
| 2606.05670 | Yes (GPT-4.1) | No — ChatEval/EvoAgent have distinct per-role programs; LLM-Debate homogeneous | No — ChatEval tool access varies by role | Yes — compared across systems |
| 2606.13003 | Yes (standardized) | No — DyLAN has domain-expert roles with distinct prompts | Not stated | Yes — all-assistant outperforms expert roles (54.41% vs 53.40%) |
| 2604.02460 | Yes | Partial — short role-specific instructions, not domain-expert programs | No tools at all | No |

No paper found a statement explicitly identifying base-model homogeneity across agents as a confound or limitation of their conclusions. Paper 3 (2606.13003) directly tested role specialization and found it did not help. Paper 1 (2512.08296) explicitly bracketed specialization as out of scope.

---

## Sources

- https://arxiv.org/abs/2512.08296 (abstract)
- https://arxiv.org/html/2512.08296 (full text, fetched)
- https://arxiv.org/abs/2606.05670 (abstract)
- https://arxiv.org/html/2606.05670 (full text, fetched)
- https://arxiv.org/abs/2606.13003 (abstract)
- https://arxiv.org/html/2606.13003v2 (full text, fetched)
- https://arxiv.org/abs/2604.02460 (Tran & Kiela)
- https://arxiv.org/html/2604.02460 (full text, fetched)
- https://www.researchgate.net/publication/403529711 (403 Forbidden — not retrieved)
