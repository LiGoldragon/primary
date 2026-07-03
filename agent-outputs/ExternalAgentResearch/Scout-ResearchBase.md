# External Agent Skills, Roles, Subagents, and Orchestration Research Base

## Task And Scope

This report maps public external approaches to agent skills, agent roles, subagents, orchestration-first workflows, context management, tool delegation, multi-agent supervision, and evaluation. It is intended as source-backed research for a later critique of an orchestration-first skills and roles system.

Scope constraints followed:

- External-only research. No local repository files, local skills, local roles, or local generated outputs were inspected.
- No source files were edited. This report artifact was written as the requested durable output.
- Sources favor official docs, vendor engineering posts, papers, framework docs, public repositories, talks or transcripts where available, and credible practitioner critiques.
- Observations are separated from interpretations where the report moves from source facts to possible critique dimensions.
- Hidden reasoning traces are treated as unstable evidence unless a source is explicitly critiquing them.

Research date: 2026-07-03.

## Source Inventory

Confidence legend:

- High: official documentation, official repository, peer-reviewed or preprint paper, primary engineering post, or direct transcript from the originating organization.
- Medium: named practitioner or engineering blog post with concrete claims, framework/vendor blog, or third-party transcript of a public talk.
- Low: secondary summary, video description without verified transcript, or source useful mainly for pointers.

### Agent Architecture And Workflow Patterns

1. [Anthropic, "Building effective agents"](https://www.anthropic.com/research/building-effective-agents), Dec. 19, 2024. Type: official research and engineering guidance. Confidence: High.
2. [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/), current docs. Type: official framework docs. Confidence: High.
3. [OpenAI Agents SDK, "Agents"](https://openai.github.io/openai-agents-python/agents/), current docs. Type: official docs. Confidence: High.
4. [OpenAI Agents SDK, "Handoffs"](https://openai.github.io/openai-agents-python/handoffs/), current docs. Type: official docs. Confidence: High.
5. [OpenAI Agents SDK, "Guardrails"](https://openai.github.io/openai-agents-python/guardrails/), current docs. Type: official docs. Confidence: High.
6. [OpenAI Swarm GitHub repository](https://github.com/openai/swarm), archived educational framework. Type: official example repository. Confidence: High for historical design intent, not for current production recommendation.
7. [LangGraph multi-agent concepts](https://langchain-ai.github.io/langgraph/concepts/multi_agent/), current docs. Type: framework docs. Confidence: High.
8. [LangGraph supervisor library](https://github.com/langchain-ai/langgraph-supervisor-py), repository and docs. Type: framework implementation. Confidence: High.
9. [LangGraph swarm library](https://github.com/langchain-ai/langgraph-swarm-py), repository and docs. Type: framework implementation. Confidence: High.
10. [Microsoft AutoGen documentation](https://microsoft.github.io/autogen/stable/), current docs. Type: official framework docs. Confidence: High.
11. [Microsoft AutoGen, multi-agent design patterns](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/index.html), current docs. Type: official docs. Confidence: High.
12. [AutoGen paper, "Enabling Next-Gen LLM Applications via Multi-Agent Conversation"](https://arxiv.org/abs/2308.08155), 2023. Type: paper. Confidence: High.
13. [CrewAI documentation](https://docs.crewai.com/), current docs. Type: framework docs. Confidence: High.
14. [CrewAI, "Hierarchical Process"](https://docs.crewai.com/en/learn/hierarchical-process), current docs. Type: framework docs. Confidence: High.
15. [Google Agent Development Kit documentation](https://google.github.io/adk-docs/), current docs. Type: official framework docs. Confidence: High.
16. [Google ADK, multi-agent systems](https://google.github.io/adk-docs/agents/multi-agents/), current docs. Type: official docs. Confidence: High.

### Skills, Roles, Subagents, And Context Management

17. [Anthropic, "Equipping agents for the real world with Agent Skills"](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), Oct. 16, 2025. Type: official engineering post. Confidence: High.
18. [Anthropic Agent Skills docs](https://docs.claude.com/en/docs/agents-and-tools/skills/overview), current docs. Type: official docs. Confidence: High.
19. [Anthropic Agent Skills, "Best practices for authoring effective skills"](https://docs.claude.com/en/docs/agents-and-tools/skills/best-practices), current docs. Type: official docs. Confidence: High.
20. [Anthropic Agent Skills, example GitHub repository](https://github.com/anthropics/skills), official examples. Type: repository. Confidence: High.
21. [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents), current docs. Type: official docs. Confidence: High.
22. [Claude Code hooks documentation](https://docs.anthropic.com/en/docs/claude-code/hooks), current docs. Type: official docs. Confidence: High.
23. [Model Context Protocol documentation](https://modelcontextprotocol.io/docs), current docs. Type: official protocol docs. Confidence: High.
24. [Model Context Protocol specification](https://modelcontextprotocol.io/specification), current spec. Type: official protocol specification. Confidence: High.
25. [12-Factor Agents](https://github.com/humanlayer/12-factor-agents), Dexter Horthy and HumanLayer, repository and site. Type: practitioner framework. Confidence: Medium.
26. [Manus, "Context Engineering for AI Agents: Lessons from Building Manus"](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus), 2025. Type: engineering blog. Confidence: Medium.
27. [Drew Breunig, "How Long Contexts Fail"](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html), 2025. Type: practitioner analysis. Confidence: Medium.
28. [LangChain blog, "Context engineering for agents"](https://blog.langchain.com/context-engineering-for-agents/), 2025. Type: framework vendor blog. Confidence: Medium.
29. [Windsurf, "Context Engineering for AI Agents"](https://windsurf.com/blog/context-engineering), 2025. Type: vendor engineering blog. Confidence: Medium.

### Multi-Agent Orchestration, Supervision, And Delegation

30. [Anthropic, "How we built our multi-agent research system"](https://www.anthropic.com/engineering/multi-agent-research-system), 2025. Type: official engineering post. Confidence: High.
31. [LangChain, "How and when to build multi-agent systems"](https://blog.langchain.com/how-and-when-to-build-multi-agent-systems/), 2025. Type: framework vendor engineering blog with benchmark discussion. Confidence: Medium-High.
32. [LangChain multi-agent implementation comparison, blog post and repository pointers](https://blog.langchain.com/langgraph-multi-agent-workflows/), 2024. Type: framework blog. Confidence: Medium.
33. [AWS, "Multi-agent orchestration with Amazon Bedrock Agents"](https://aws.amazon.com/blogs/machine-learning/multi-agent-orchestration-with-amazon-bedrock/), 2024. Type: official vendor blog. Confidence: High for AWS design surface.
34. [Amazon Bedrock Agents documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html), current docs. Type: official docs. Confidence: High.
35. [Microsoft Semantic Kernel agent framework docs](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/), current docs. Type: official docs. Confidence: High.
36. [Semantic Kernel Agent Orchestration docs](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/), current docs. Type: official docs. Confidence: High.
37. [Diagrid, "5 challenges in orchestrating AI agents"](https://www.diagrid.io/blog/5-challenges-in-orchestrating-ai-agents), 2025. Type: vendor/practitioner blog. Confidence: Medium.
38. [Temporal, "Durable Execution for AI Agents"](https://temporal.io/blog/durable-execution-for-ai-agents), 2025. Type: infrastructure vendor engineering blog. Confidence: Medium.

### Evaluation, Observability, And Reliability

39. [OpenAI Evals repository](https://github.com/openai/evals), official repository. Type: evaluation tooling. Confidence: High.
40. [OpenAI Agents SDK tracing documentation](https://openai.github.io/openai-agents-python/tracing/), current docs. Type: official docs. Confidence: High.
41. [LangSmith documentation, evaluate an agent](https://docs.smith.langchain.com/evaluation/how_to_guides/agents), current docs. Type: official docs. Confidence: High.
42. [LangSmith documentation, trace concepts](https://docs.smith.langchain.com/observability/concepts), current docs. Type: official docs. Confidence: High.
43. [AgentBench paper](https://arxiv.org/abs/2308.03688), 2023. Type: benchmark paper. Confidence: High.
44. [ToolBench paper](https://arxiv.org/abs/2307.16789), 2023. Type: benchmark paper. Confidence: High.
45. [WebArena paper](https://arxiv.org/abs/2307.13854), 2023. Type: benchmark paper. Confidence: High.
46. [Tau-bench paper](https://arxiv.org/abs/2406.12045), 2024. Type: benchmark paper. Confidence: High.
47. [SWE-bench paper and project](https://www.swebench.com/), 2024 onward. Type: benchmark/project. Confidence: High.
48. [METR, "Measuring AI Ability to Complete Long Tasks"](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/), 2025. Type: research nonprofit report. Confidence: Medium-High.
49. [Anthropic, "Measuring faithfulness in chain-of-thought reasoning"](https://www.anthropic.com/research/measuring-faithfulness-in-chain-of-thought-reasoning), 2025. Type: official research. Confidence: High.

### Talks, Videos, And Transcripts

50. [AI Engineer / YouTube, "How We Build Effective Agents: Barry Zhang, Anthropic"](https://www.youtube.com/watch?v=D7_ipDqhtwk), 2025. Type: public talk/video description. Confidence: Low unless transcript is obtained directly.
51. [No Priors podcast transcript with Anthropic leaders on agents and MCP](https://podscripts.co/podcasts/no-priors-artificial-intelligence-machine-learning-technology-startups/anthropics-mike-krieger-on-ai-agents-mcp-and-building-better-dev-tools), 2025. Type: third-party transcript. Confidence: Medium.
52. [Sequoia AI Ascent / Agent engineering talks and transcripts](https://www.sequoiacap.com/article/ai-ascent-2025/), 2025. Type: conference materials. Confidence: Medium where transcript is published, lower where video-only.
53. [Andrej Karpathy, "Software Is Changing (Again)"](https://www.youtube.com/watch?v=LCEmiRjPEtQ), 2025. Type: public talk/video. Confidence: Medium for high-level context if using the video itself; low for secondary summaries.
54. [AI Engineer / YouTube, "Don't Build Agents, Build Skills Instead - Barry Zhang & Mahesh Murag"](https://www.youtube.com/watch?v=CEvIs9y1uog), 2026. Type: public talk/video description. Confidence: Low unless transcript is obtained directly.

### Critiques, Failure Modes, And Dissent

55. [Anthropic, "Building effective agents"](https://www.anthropic.com/research/building-effective-agents), same source as item 1. Type: official guidance that argues against unnecessary complexity. Confidence: High.
56. [Anthropic multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), same source as item 30. Type: official engineering post with explicit cost and coordination tradeoffs. Confidence: High.
57. [Augment Code, "The rise and fall of the AI agent: why context, not autonomy, is the breakthrough"](https://www.augmentcode.com/blog/the-rise-and-fall-of-the-ai-agent-why-context-not-autonomy-is-the-breakthrough), 2025. Type: vendor critique. Confidence: Medium.
58. [Matthew Rocklin, "An AI Agent While Coding"](https://matthewrocklin.com/blog/work/2025/02/28/ai-agent), 2025. Type: practitioner reflection. Confidence: Medium.
59. [Tobias Zwingmann, "AI Agents: The Good, The Bad, and The Ugly"](https://tobiaszwingmann.medium.com/ai-agents-the-good-the-bad-and-the-ugly), 2024/2025. Type: practitioner critique. Confidence: Medium-Low because platform date/content can be unstable.
60. [Gary Marcus, critique of LLM agent hype](https://garymarcus.substack.com/), ongoing. Type: public critic commentary. Confidence: Low-Medium unless a specific post is selected for later targeted work.

## Observed External Approaches

### 1. "Workflow first, agent second" is a recurring official recommendation

Observation: Anthropic's "Building effective agents" distinguishes workflows from agents. Workflows are systems where LLMs and tools follow predefined code paths. Agents are systems where LLMs dynamically direct process and tool use. Anthropic recommends starting with direct model calls, then simple workflows, and only adding agentic autonomy when necessary. The same post names common workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer.

Observation: This is not anti-orchestration. The recommended escalation path still includes orchestration, but it asks designers to make the orchestration explicit and justified. The orchestrator-workers pattern is framed as useful when a central LLM decomposes a task into subtasks, delegates to worker LLMs, and synthesizes outputs. Parallelization is framed as useful where subtasks are independent or where multiple model calls can vote or validate.

Observation: OpenAI's Agents SDK encodes agentic systems as agents with instructions, tools, handoffs, guardrails, tracing, sessions, and runners. The architecture makes orchestration concrete in framework terms: the runtime loop executes an agent, invokes tools, follows handoffs, and records traces.

Observation: OpenAI Swarm, now archived and explicitly educational, modeled agent coordination through "routines" and "handoffs." The important design idea is not the old package itself, but the decomposition of an agent system into callable routines and explicit transfers of control.

Interpretation: A later critique should not ask whether the user has "agents" in the abstract. It should ask whether each autonomous surface earned its autonomy, whether deterministic workflow would be simpler, and whether orchestration patterns are explicit enough to inspect.

### 2. Supervisor, swarm, group chat, and hierarchical models are distinct coordination choices

Observation: LangGraph presents multiple multi-agent patterns, including network, supervisor, supervisor-as-tool-calling, hierarchical, and custom architectures. Its supervisor library centralizes routing through a supervisor agent that delegates to specialist agents. Its swarm library instead lets agents hand off to one another dynamically, preserving the active agent as part of graph state.

Observation: Microsoft AutoGen frames multi-agent applications around message-passing agents. Its docs and original paper emphasize conversable agents, group chats, user proxies, tool use, and configurable orchestration. AutoGen's selector group chat and design-pattern docs expose a key choice: a policy or selector chooses the next speaker, rather than every agent deciding independently.

Observation: CrewAI distinguishes "crews" and "flows." Crews emphasize autonomous collaboration among role-based agents. Flows emphasize deterministic, event-driven orchestration with control over state and execution. CrewAI's hierarchical process introduces a manager agent that coordinates tasks, delegation, and validation.

Observation: Google ADK supports multi-agent systems with parent agents, subagents, workflow agents, LLM agents, and custom agents. Its docs present hierarchical composition as a native design surface, not just an implementation detail.

Observation: Microsoft Semantic Kernel's agent orchestration docs expose several named orchestration patterns, including sequential, concurrent, group chat, handoff, and magentic orchestration. This mirrors the broader ecosystem: no single coordination pattern dominates.

Interpretation: "Orchestration-first" needs a more precise shape than "use subagents." A useful critique should identify which coordination topology is intended at each layer: central supervisor, handoff network, deterministic flow, group chat, or nested hierarchy.

### 3. Skills are emerging as portable, progressive context modules rather than just prompts

Observation: Anthropic's Agent Skills docs define skills as folders containing a `SKILL.md` plus optional scripts, references, and assets. The `SKILL.md` frontmatter describes when the skill should be used. The body provides instructions. Optional files are loaded progressively rather than stuffing everything into the model context.

Observation: Anthropic's engineering post on Agent Skills frames skills as a mechanism for equipping agents with task-specific procedures, domain knowledge, scripts, and resources. The core pattern is progressive disclosure: a small description lets the model decide relevance, the main skill file gives operating instructions, and extra files are read only when needed.

Observation: Anthropic best-practice docs emphasize concise skill descriptions, clear trigger conditions, step-by-step workflows, use of executable scripts for repeated deterministic logic, and separating detailed references from the core skill file.

Observation: Claude Code subagents are configured with names, descriptions, prompts, and tool access. They run in separate contexts and can be invoked explicitly or selected automatically. Anthropic frames their advantages as context preservation, specialized expertise, reusability, and flexible permissions.

Interpretation: Skills and roles should be critiqued as different artifacts. A skill is a capability package with trigger rules and bounded instructions. A role or subagent is an execution persona or delegation target with its own context and tool permissions. Combining them can be powerful, but conflating them can cause bloated prompts, ambiguous triggering, and unclear ownership of results.

### 4. Context management is treated as a first-class engineering problem

Observation: Claude Code subagents explicitly preserve main-thread context by moving specialized work into separate contexts. Anthropic Agent Skills reduce context load through progressive disclosure. LangGraph and LangSmith emphasize state, traces, and message history as inspectable runtime surfaces.

Observation: Manus argues for context engineering practices such as designing context around the agent loop, keeping context compact, externalizing memory to files or state where appropriate, preserving stable facts, and avoiding large irrelevant prompt payloads.

Observation: Drew Breunig's "How Long Contexts Fail" identifies context failure modes such as context poisoning, context distraction, context confusion, and context clash. Suggested mitigations include retrieval, summarization, isolation, and context pruning.

Observation: LangChain's "Context engineering for agents" frames context not as one prompt but as the information passed into every model call: instructions, available tools, message history, retrieved data, intermediate state, and structured outputs. It discusses write, select, compress, and isolate as context operations.

Observation: Windsurf's context-engineering writeup emphasizes that coding agents need relevant repository context, recent user intent, and tool outputs, but too much irrelevant context degrades performance.

Interpretation: For an orchestration-first system, context hygiene is not a side benefit; it is the central justification. The later critique should examine whether subagents actually reduce context burden, or whether they create hidden context debt in reports, transcripts, tool outputs, and stale handoffs.

### 5. Tool delegation is moving toward typed, observable, permissioned interfaces

Observation: OpenAI Agents SDK models tools as functions, hosted tools, agents-as-tools, and MCP tools. Handoffs transfer control between agents. Guardrails run checks on inputs and outputs. Tracing records agent execution.

Observation: Model Context Protocol standardizes how applications expose tools, resources, and prompts to models. The protocol separates the host application, client, and server roles and defines tool schemas, resource reads, prompts, sampling, and elicitation features.

Observation: Claude Code subagents can have distinct tool access. Anthropic hooks can run deterministic commands around lifecycle events, which introduces a separation between model agency and fixed automation.

Observation: AutoGen, Semantic Kernel, LangGraph, CrewAI, and Google ADK all expose tool-calling or function-calling as core surfaces. Their common direction is typed or schema-described capabilities rather than arbitrary unstructured textual delegation.

Interpretation: A later critique should treat tool delegation quality as more important than number of tools. Useful dimensions include: explicit schemas, permission scoping, idempotency, auditable side effects, structured outputs, tool-result summarization, and whether human approval is required for irreversible operations.

### 6. Multi-agent systems are recommended mainly when work is decomposable, parallel, or too broad for one context

Observation: Anthropic's multi-agent research system describes a lead agent that plans, delegates to subagents, and synthesizes results. Anthropic reports that multi-agent systems can outperform single-agent systems on broad research tasks, especially when parallel exploration matters. It also warns that they use many more tokens and require careful prompt engineering, evaluation, and observability.

Observation: LangChain's "How and when to build multi-agent systems" argues that multi-agent systems help when tasks exceed one agent's context or require parallel search across independent domains. It also reports that multi-agent benefits can disappear or reverse for narrow tasks where communication overhead dominates.

Observation: CrewAI, AutoGen, LangGraph, Semantic Kernel, and Google ADK provide role-based and hierarchical composition patterns, but none of their serious docs imply that more agents are always better.

Interpretation: The key adoption test is task shape. Multi-agent supervision is likely justified for broad research, cross-domain review, codebase mapping, adversarial critique, or independent verification. It is less justified for narrow deterministic edits, simple lookups, or tasks where one agent can keep all relevant state in context.

## Tradeoffs And Disagreements

### Complexity versus capability

Sources that support orchestration-first:

- Anthropic's orchestrator-workers pattern and multi-agent research system show strong results for broad research tasks.
- OpenAI Agents SDK, LangGraph, AutoGen, CrewAI, Google ADK, and Semantic Kernel all provide first-class constructs for multi-agent orchestration.
- Claude Code subagents and Anthropic Skills directly support context isolation and capability packaging.

Sources that argue for restraint:

- Anthropic's own "Building effective agents" recommends the simplest viable solution and warns against unnecessary framework complexity.
- LangChain's multi-agent benchmark discussion says multi-agent systems help when tasks are broad and parallelizable, but add overhead and may underperform on focused tasks.
- Anthropic's multi-agent research writeup says multi-agent systems can burn substantially more tokens and require strong evaluation and observability.
- Augment Code's critique argues that context quality often matters more than nominal autonomy.

Interpretation: A strong orchestration-first system should not maximize agent count. It should maximize clarity of decomposition, context cleanliness, and inspectable delegation.

### Central supervisor versus peer handoff

Supervisor advantages observed in LangGraph supervisor, CrewAI hierarchical process, Google ADK hierarchy, Semantic Kernel orchestration, and Anthropic's lead-agent research pattern:

- Easier global view.
- Clear synthesis point.
- Cleaner user interaction surface.
- Easier permission and output gating.
- Better fit for the user's desired main session role.

Peer handoff or swarm advantages observed in LangGraph swarm and OpenAI Swarm:

- Agents can transfer control when local expertise determines the next best actor.
- The system can be more flexible for exploratory tasks.
- It may avoid overloading one central planner.

Risks of peer handoff:

- Harder to preserve a coherent user-facing view.
- More risk of circular delegation.
- Harder to know who owns final synthesis.
- More complex evaluation because trajectories vary more.

Interpretation: The user's stated lens favors a central orchestration session with delegated ground-truth workers. Peer handoff may still be useful inside bounded subgraphs, but it should not erase the main session's responsibility for questions, next actions, synthesis, and user interaction.

### Role prompts versus skills

Role/subagent benefits:

- Separate context.
- Separate permissions.
- Specialized operating posture.
- Clear delegation target.

Skill benefits:

- Portable procedure and resources.
- Progressive loading.
- Reusable across agents.
- Easier to evaluate as a capability package.

Conflict:

- A role can become a dumping ground for every possible instruction.
- A skill can become too broad and start behaving like a role.
- Both can encode hidden policy decisions that are hard to test if they lack clear triggers and outputs.

Interpretation: Later critique should check whether "role" files contain stable execution identity and boundaries, while "skill" files contain task-specific methods, trigger rules, and references. If both carry the same doctrine, the system likely has duplication and context bloat.

### Autonomy versus determinism

Autonomy is favored when:

- Subtasks are not known in advance.
- The agent must decide which sources, files, tools, or specialists to use.
- The work benefits from broad exploration.

Determinism is favored when:

- The workflow is known.
- Safety or reproducibility matters.
- A simple script or state machine can do the job.
- Evaluation depends on stable steps.

Anthropic, CrewAI, Temporal, and Diagrid all converge on this split in different language: agentic decisions should be bounded by durable workflows, deterministic hooks, typed tools, or observable orchestration.

Interpretation: The later critique should ask where model judgment is genuinely needed and where instructions should become scripts, schemas, hooks, checks, or fixed workflow edges.

### Evaluation by trace versus evaluation by hidden reasoning

Observation: OpenAI Agents SDK tracing and LangSmith observability expose spans, tool calls, model calls, inputs, outputs, and agent transitions. These are stable enough to audit because they are external behavior.

Observation: AgentBench, ToolBench, WebArena, tau-bench, and SWE-bench evaluate agents through task outcomes, environments, tool use, or user-simulation style interactions, not by trusting private chain-of-thought.

Observation: Anthropic's chain-of-thought faithfulness research cautions that reasoning traces can be incomplete or unfaithful. This is especially relevant where models produce or hide rationales.

Interpretation: Later evaluation should inspect observable trajectories, tool results, final outputs, cost, latency, reproducibility, and human review quality. Hidden chain-of-thought should not be treated as a reliable grading target. Publicly visible rationale can be evaluated as an artifact, but not assumed to reveal the actual internal causal process.

## Critique Dimensions For A Later Orchestration-First Skills/Roles Review

These dimensions are interpretations derived from the external sources above.

### 1. Task-shape fit

Questions:

- Does each delegated subagent map to a task that is broad, independent, specialized, risky, or context-heavy enough to justify isolation?
- Are simple deterministic tasks kept as scripts, checks, or direct tool calls rather than full agents?
- Does the system distinguish broad research, implementation, review, summarization, and user-interaction work?

Evidence to inspect later:

- Role triggers.
- Delegation rules.
- Examples of tasks that should stay in the main session versus go to workers.
- Any benchmarks or transcripts showing improved context cleanliness or outcome quality.

### 2. Orchestration topology

Questions:

- Is the intended topology central supervisor, hierarchical supervisor, peer handoff, group chat, deterministic workflow, or a hybrid?
- Does every topology have an owner for final synthesis?
- Can the main session maintain the global view without becoming a bottleneck or context dump?

Evidence to inspect later:

- Role packets.
- Handoff rules.
- Worker output protocol.
- Rules for when the main session asks the user versus dispatches workers.

### 3. Context hygiene

Questions:

- Do skills and roles use progressive disclosure, or do they load large doctrine by default?
- Are subagent outputs concise enough for synthesis?
- Are stale reports, repeated instructions, and duplicated role text pruned or routed to durable surfaces?
- Is context isolation real, or does the main session still absorb all details?

Evidence to inspect later:

- Skill trigger descriptions.
- Role packet size.
- Output artifacts.
- Summaries and handoffs.
- Any policy for context compaction and report hygiene.

### 4. Skill versus role separation

Questions:

- Are skills capability modules with clear trigger conditions, instructions, references, and assets?
- Are roles execution identities with clear responsibilities, boundaries, and tool permissions?
- Is durable doctrine duplicated across many roles?
- Can one skill be used by multiple roles without carrying irrelevant persona text?

Evidence to inspect later:

- Skill file structure.
- Role prompts.
- References and auxiliary files.
- Naming and trigger conventions.

### 5. Delegation contracts

Questions:

- Does each worker receive a bounded task, authority, source scope, output shape, and evidence requirement?
- Do workers separate observed facts from interpretation?
- Are blocker and unknown reporting requirements explicit?
- Is the main session responsible for synthesis rather than merely concatenating worker reports?

Evidence to inspect later:

- Dispatch envelopes.
- Worker output templates.
- Completed reports.
- Rules for source confidence and evidence.

### 6. Tool permission and side-effect control

Questions:

- Are tools scoped by role or task?
- Are irreversible operations gated by human approval or deterministic checks?
- Are tool schemas explicit and auditable?
- Are side effects tracked in trace, report, or version-control surfaces?

Evidence to inspect later:

- Tool allowlists.
- Hook or approval rules.
- Version-control rules.
- Secret and privacy handling.

### 7. Observability and evaluation

Questions:

- Can a reviewer reconstruct what happened from observable artifacts?
- Are task outcomes evaluated independently of hidden reasoning?
- Are agent trajectories captured where needed?
- Are failed delegations analyzed for prompt, context, tool, or topology causes?

Evidence to inspect later:

- Traces or logs.
- Test runs.
- Review reports.
- Metrics such as pass rate, cost, latency, retries, human interventions, and defect escape rate.

### 8. Cost, latency, and parallelism

Questions:

- Does the system account for token and wall-clock cost of spawning agents?
- Are workers parallelized only when tasks are independent enough?
- Is there a stop condition for excessive delegation?
- Are redundant investigations detected?

Evidence to inspect later:

- Orchestration budgets.
- Worker dispatch counts.
- Rules for when to ask instead of spawning.
- Duplicate report handling.

### 9. Human-in-the-loop behavior

Questions:

- Does the main session ask clarifying questions before costly or ambiguous dispatch?
- Does it suggest next actions rather than just executing a fixed pipeline?
- Does it preserve user intent and constraints across subagent outputs?
- Are human decisions represented as explicit inputs, not inferred from agent artifacts?

Evidence to inspect later:

- Main-session instructions.
- Clarification protocol.
- Intent handling.
- Examples of user-facing synthesis.

### 10. Failure containment

Questions:

- Can a bad worker output be rejected without poisoning the main context?
- Are worker claims labeled by confidence and evidence?
- Is there a path for adversarial critique, independent verification, or rerun?
- Are partial results routed without becoming permanent doctrine?

Evidence to inspect later:

- Report structure.
- Review or auditor roles.
- Confidence labeling.
- Rules for provisional versus accepted findings.

## Practices Likely Worth Adopting

These are interpretations, not claims that every source states in the same terms.

1. Start with a simple workflow and add agents only where task shape justifies autonomy.

Rationale: Anthropic and LangChain both emphasize that agentic complexity has overhead. This practice prevents "multi-agent" from becoming a default rather than a design choice.

2. Use a central orchestrator for user interaction, planning, dispatch, and synthesis.

Rationale: This matches Anthropic's lead-agent research pattern, LangGraph supervisor, CrewAI hierarchical process, and the user's stated desire for a cleaner main session with better global view.

3. Treat subagents as bounded workers with source scope, authority, output contract, and confidence requirements.

Rationale: The framework docs show handoffs and tool calls, but high-quality orchestration requires explicit delegation contracts so the orchestrator can compare, reject, or synthesize worker results.

4. Separate roles from skills.

Rationale: Anthropic Skills are portable capability packages; Claude Code subagents are isolated execution contexts. Keeping those concepts separate should reduce bloat and improve reuse.

5. Use progressive disclosure for skills and doctrine.

Rationale: Anthropic Skills, Manus, LangChain context engineering, and long-context failure analyses all support minimizing irrelevant prompt load.

6. Make tool use typed, permissioned, and observable.

Rationale: OpenAI Agents SDK, MCP, AutoGen, LangGraph, Semantic Kernel, and Claude Code all converge on structured tool surfaces and tracing or logs.

7. Prefer observable evaluation: outcome, trace, tool use, cost, latency, and human review.

Rationale: Agent benchmarks and observability tools rely on externally inspectable behavior. Chain-of-thought faithfulness concerns make hidden reasoning a poor evaluation foundation.

8. Use adversarial or independent review workers for high-stakes conclusions.

Rationale: Anthropic's multi-agent research pattern and evaluator-optimizer workflows suggest value in separate generation and critique paths, especially where one worker may miss facts.

9. Preserve worker outputs as durable artifacts only when they are true pickup surfaces.

Rationale: Context-engineering sources warn against context bloat. Durable reports help when they support synthesis or future agents, but can become clutter if every minor action becomes an artifact.

10. Encode deterministic repeated work as scripts, hooks, tests, or fixed workflows.

Rationale: Anthropic, CrewAI flows, Temporal, Diagrid, and hooks-based approaches all support using deterministic machinery where model judgment is unnecessary.

## Practices Likely Worth Rejecting

1. Treating more agents as automatically better.

Reason: Sources repeatedly identify coordination, cost, and evaluation overhead.

2. Using hidden chain-of-thought as the primary evaluation signal.

Reason: Faithfulness is uncertain, and many production systems hide reasoning. Evaluate observable behavior instead.

3. Giving all subagents all tools by default.

Reason: Tool permissioning is a recurring framework feature because scope matters for safety and clarity.

4. Combining every instruction into one giant role prompt.

Reason: Progressive disclosure and context-engineering sources argue against loading irrelevant instructions.

5. Letting peer handoff networks own final user-facing synthesis.

Reason: Peer handoff can be useful, but the user's desired main-session shape requires a stable global owner.

6. Treating third-party talk summaries as equivalent to official docs or transcripts.

Reason: Video and conference material can be useful, but source confidence should track whether direct transcript, slides, or only descriptions were used.

7. Delegating without a return schema.

Reason: Orchestrators need comparable outputs: facts, evidence, interpretations, unknowns, blockers, and recommendations.

## Practices Worth Investigating Further

1. Skill evaluation harnesses.

Open question: Public docs explain how to author skills, but there is less mature public guidance on testing whether a skill triggers correctly, loads the right references, avoids overreach, and improves task outcomes.

Possible sources for targeted follow-up: Anthropic Skills docs and examples, OpenAI Evals, LangSmith agent evaluation, internal benchmark patterns from SWE-bench style tasks.

2. Role and subagent lifecycle management.

Open question: Frameworks show how to create subagents, but public guidance is weaker on retiring roles, detecting overlapping roles, versioning role prompts, and preventing role sprawl.

Possible sources: AutoGen, LangGraph, CrewAI enterprise docs, practitioner writeups on agent platform operations.

3. Cost-aware orchestration policies.

Open question: Anthropic and LangChain discuss token cost, but a later system critique may need concrete budgets and thresholds for when spawning workers is justified.

Possible sources: vendor tracing docs, LangSmith cost tracking, OpenAI tracing, Anthropic multi-agent research economics.

4. Multi-agent security and prompt injection.

Open question: Tool delegation and subagent browsing create more attack surfaces. This report did not deeply survey prompt-injection and agent security literature.

Possible sources: OWASP Top 10 for LLM Applications, Microsoft prompt injection guidance, Anthropic and OpenAI safety docs, MCP security guidance.

5. Human-in-the-loop protocols.

Open question: Many frameworks include handoffs and approvals, but fewer specify when the orchestrator should stop and ask the user rather than spend more tokens.

Possible sources: OpenAI Agents SDK human-in-the-loop examples, LangGraph interrupt patterns, Semantic Kernel orchestration docs.

6. Transcript-backed talks.

Open question: Public talks contain useful practitioner heuristics, but many available references are video-only or secondary. More targeted transcript collection would improve confidence.

Possible sources: AI Engineer, Sequoia AI Ascent, Anthropic YouTube, No Priors, Latent Space, Practical AI.

## Gaps And Limitations

- No local system, role, skill, or generated-output files were inspected, by instruction.
- This report did not deeply evaluate private enterprise platforms or paid documentation.
- Talk and video coverage is weaker than official documentation coverage. Some talk entries are included as pointers with low or medium confidence because direct transcripts were not consistently available.
- Security research was only lightly covered. A later critique of tool delegation should add prompt injection, data exfiltration, supply-chain, and MCP server trust analysis.
- Quantitative benchmark comparison is shallow. A later evaluation pass should decide which benchmarks match the user's actual tasks, because AgentBench, WebArena, ToolBench, tau-bench, SWE-bench, and METR long-task work measure different capabilities.
- Vendor docs change quickly. The report should be refreshed before using it for a high-stakes design decision.

## Concise Takeaways For Later Critique

- The strongest external support for the user's direction is the convergence of Anthropic subagents and skills, OpenAI handoffs/tracing/guardrails, LangGraph supervisors, AutoGen group orchestration, CrewAI hierarchy, Google ADK multi-agent composition, and Anthropic's own lead-agent research system.
- The strongest external caution is equally clear: do not spawn agents by default. Use them when isolation, parallelism, specialization, or context limits justify the overhead.
- The main session should remain the accountable orchestrator: it asks the user, selects topology, dispatches bounded work, receives evidence-bearing outputs, rejects weak claims, and synthesizes next actions.
- Skills should be portable capability packages with progressive disclosure. Roles should be bounded execution identities with permissions and output contracts.
- Evaluation should use observable behavior: task outcome, trace, tool calls, sources, tests, cost, latency, and human review. Hidden reasoning traces are not a stable evaluation foundation.
