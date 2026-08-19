# Prior Art: Flows, Names, and Harness Prompts
**Filed:** 2026-08-19

This report covers three threads from a design dictation: (A) naming a component by its core (synecdoche in software vocabulary, and prior uses of "nexus"), (B) "flow" as a unit versus "agent," and (C) what coding harness built-in prompts actually contain and how they can be replaced.

Each claim carries its source. "Witnessed" means the text was read directly from a fetched URL. "Reported" means the claim comes from secondary sources (search result summaries, articles). Claims from the designer's dictation are not checked here; they are the subject of the research.

---

## A. Naming by the Core Part for the Whole

### Synecdoche in systems vocabulary

Naming the whole by a central part — or a central part by the whole — is old in computing.

**Kernel.** Wikipedia (Kernel, operating system): "A kernel is a computer program at the core of a computer's operating system that always has complete control over everything in the system." In practice, "the kernel" is the core component; "Linux" or "the OS" names the whole. The terms bleed in common speech: people say "the Linux kernel" when they want precision and "Linux" when they mean the whole stack. Source: https://en.wikipedia.org/wiki/Kernel_(operating_system)

**Daemon.** The term was coined at MIT Project MAC circa 1963, after Maxwell's Demon (a thought-experiment entity that works tirelessly in the background). Fernando Corbató: "We fancilessly began to use the word daemon to describe background processes that worked tirelessly to perform system chores." The daemon is a part (a background service process) of a running system; over time "daemon" names a category of software entity where the background process is the defining characteristic. Source: https://en.wikipedia.org/wiki/Daemon_(computing); https://gigazine.net/gsc_news/en/20180206-unix-linux-daemon/

**Erlang node.** From Erlang/OTP documentation: "A running instance of the Runtime System is referred to as an Erlang node." The node is a full running BEAM VM; the term encompasses all processes within it. Multiple nodes connect into a distributed Erlang network. "Node" names the individual whole-instance and (loosely) the runtime itself. Source: https://www.erlang.org/doc/system/distributed.html

**Smalltalk image.** A Smalltalk "image" is the complete serialized snapshot of the running environment: objects, classes, methods, and state. "The word 'image' means the set of objects that makes up a Smalltalk in a specific instant." The image is the whole system, not merely its representation. Source: https://playingwithobjects.wordpress.com/2012/06/01/the-image-dilemma/ (reported)

**Plan 9 file server.** In Plan 9, a "file server" is a stand-alone system that provides the main file system; the term names the machine and the process that serves it. The Plan 9 architecture generalizes all resources as file-serving entities. Source: https://plan9.io/sys/doc/9.html; https://9p.io/sys/man/4/INDEX.html

**General pattern.** These examples share the structure the designer describes: a component's name (kernel, daemon, image, node, file server) expands to name the thing it anchors — not by imprecision, but because the component is the defining characteristic of the whole. There is no specific academic literature on this phenomenon in software naming that this search found; the linguistic term is synecdoche (Wikipedia: https://en.wikipedia.org/wiki/Synecdoche), specifically pars pro toto (part standing for whole).

### Prior uses of "Nexus" as a software and system term

**Latin origin.** From nectere, "to bind or tie." The noun nexus in classical Latin means a binding connection or interlaced structure. First attested in English 1663. Source: https://www.etymonline.com/word/nexus

**Sonatype Nexus Repository.** An artifact repository manager acting as a central hub for storing and distributing software components across development pipelines. "A single, auditable place to store, proxy, and distribute all the artifacts your software depends on." In production since approximately 2008. Three-tier architecture: hosted, proxy, and group repositories. The name reflects the Latin binding/connecting sense. Source: https://www.sonatype.com/products/sonatype-nexus-repository; https://medium.com/@Raghvendra_Tyagi/all-about-nexus-and-how-to-setup-nexus-sonatype-repository-e67548bf8356 (reported)

**Cisco Nexus.** A data-center networking architecture. "Cisco Nexus is a comprehensive architectural framework designed to converge network connectivity, security policy, and operational management across all major Cisco data center fabric types." Uses "nexus" as a convergence/binding point. Source: https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/cisco-nexus-one-fabric-architecture-white-paper.html

**Azure Operator Nexus.** Microsoft's telco network infrastructure service, named after the same hub metaphor. Source: https://learn.microsoft.com/en-us/azure/operator-nexus/concepts-nexus-networking

**arXiv 2502.19091 — direct collision.** A February 2025 paper titled "Nexus: A Lightweight and Scalable Multi-Agent Framework for Complex Tasks Automation." From the search result summary: "Nexus is a modular multi-agent architecture that integrates a single root Supervisor agent alongside multiple Task Supervisors and Worker agents arranged within a hierarchical execution graph." This paper uses "Nexus" for an AI orchestration system with exactly the hub-and-coordination role the designer describes. **This is a strong naming collision in the designer's target space.** Source: https://arxiv.org/abs/2502.19091

**Agent-Nexus (GitHub).** A repository described as "Central hub for multi-agent AI orchestration with real-time visualization." Source: https://github.com/dtkmn/agent-nexus (reported)

**Nexus Agents (GitHub).** A repository: "A hierarchical multi-agent architecture with web interface, API server, and worker processes." Source: https://github.com/trilogy-group/nexus-agents (reported)

**Summary of collision risk.** "Nexus" is saturated in: (1) artifact/package management (Sonatype), (2) data-center networking (Cisco, Azure), (3) multi-agent AI orchestration (arXiv 2502.19091, two GitHub repos). The designer's daemon-centred component-that-composes-flows overlaps most directly with the multi-agent orchestration use.

---

## B. "Flow" as a Unit Versus "Agent"

### Flow-based programming (FBP)

J. Paul Morrison developed FBP at IBM in the late 1960s. "FBP defines applications as networks of 'black box' processes, which communicate via data chunks (called Information Packets) travelling across predefined connections. Processors are connected by bounded buffers called 'connections'... A process may become suspended while sending (if the connection fills up), as well as while receiving (when the connection becomes empty)." Processes are reusable; they do not know about each other. "IBM used [the term 'flow'] in the 70s to define concepts of more manageable business workflows." Source: https://jpaulm.github.io/fbp/ (witnessed); https://en.wikipedia.org/wiki/Flow-based_programming

**Relevance to the designer's use.** Morrison's "flow" names the whole application-as-network, not an individual process. The designer uses "flow" for a single LLM session (one bounded process in Morrison's terms). The designer's multiple flows composing a Nexus is closer to Morrison's network than to Morrison's individual process. The naming is inverted from FBP convention.

### Other prior "flow" uses

**Control flow.** A fundamental programming concept: the order in which instructions execute. Entirely different sense; background noise in any naming discussion.

**Data flow.** Programs represented as directed graphs of operations and data dependencies, predating FBP. Source: https://en.wikipedia.org/wiki/Control_flow; https://www.sciencedirect.com/topics/computer-science/data-flow-language (reported)

**Apache Airflow.** Created by Airbnb in 2015, transferred to Apache in 2016. DAG-based batch workflow orchestration. Uses "flow" in the product name and "DAG" (directed acyclic graph) internally. Source: https://www.getorchestra.io/guides/apache-airflow-vs-nifi-which-data-orchestration-tool-is-better-in-2026 (reported)

**Apache NiFi.** Flow-based data routing and transformation platform. Open-sourced by NSA in 2014. Source: same URL (reported)

**CrewAI "Flows."** CrewAI introduced a concept called "Flows" for deterministic, event-driven task orchestration, alongside "Crews" for dynamic role-based agent collaboration. This is a direct prior use of "flow" as a unit in an LLM orchestration framework as of 2024–2025. Source: https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen (reported)

**Csikszentmihalyi's "flow."** Psychologist Mihaly Csikszentmihalyi's 1990 book "Flow: The Psychology of Optimal Experience" defines flow as a state of complete absorption and optimal experience. The term is strongly associated with this psychological concept in general culture. Source: https://www.goodreads.com/book/show/66354.Flow (reported). This is not a computing use, but a naming collision in general vocabulary.

**LangGraph.** Uses "node" (not flow) for individual agent steps; "graph" for the composed system. Source: https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen (reported)

### AI agent definitions and the designer's critique

**Russell & Norvig (1995).** "An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through effectors." Characteristics include autonomy, persistence over time, adaptability, and goal-pursuit. Source: https://mkyush.medium.com/the-anatomy-of-an-ai-agent-from-russell-norvig-to-the-agentic-era-9142a9e6263d (reported)

**Wooldridge & Jennings (1995).** Properties: autonomy (no direct human intervention), social ability (interaction with other agents), reactivity (responding to environment), pro-activeness (goal-directed behavior). Source: same (reported)

**Anthropic "Building Effective Agents" (December 2024).** Distinguishes: workflows = "LLMs and tools orchestrated through predefined code paths"; agents = "LLMs dynamically directing their own processes and tool usage, maintaining control over how they accomplish tasks." Five workflow sub-patterns identified: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer. The guide advises: "most production AI systems do not need another autonomous agent — they need a workflow with clear steps." Source: https://www.anthropic.com/engineering/building-effective-agents (witnessed)

**arXiv 2508.05338 — agent dilution.** A 2025 paper titled "The Term 'Agent' Has Been Diluted Beyond Utility and Requires Redefinition." The search result abstract indicates the term is contested as LLM use has expanded. Source: https://arxiv.org/html/2508.05338v1

**LangGraph / CrewAI / AutoGen terminology summary.** LangGraph: explicit directed graph, nodes and edges; agent steps are nodes. CrewAI: Crews (dynamic, role-based) and Flows (deterministic, event-driven). AutoGen: agents as conversational participants in structured turn-taking. Source: https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen (reported)

### "Synthetic intelligence"

John Haugeland, "Artificial Intelligence: The Very Idea" (MIT Press, 1985): proposed "synthetic intelligence" as an alternative to "artificial intelligence." Haugeland's analogy: a synthetic diamond is a true diamond made by a non-biological process, not a fake diamond; similarly, machine intelligence should be viewed as genuine, not as imitation. Haugeland also used the term in 1986 to characterize earlier symbolic AI research (which he separately named "GOFAI" — good old-fashioned AI). The designer's use of "synthetic intelligence" directly echoes Haugeland's distinction. Source: https://en.wikipedia.org/wiki/Synthetic_intelligence; https://www.researchgate.net/publication/256121747_Artificial_intelligence_The_very_idea_J_Haugeland_MIT_Press_Cambridge_MA_1985_287_pp (reported)

### Composing many bounded sessions into a larger entity

**Society of Mind (Minsky, 1986).** "The Society of Mind" argues that human intelligence is not a single unified process but emerges from coordinated interaction of many simpler, specialized sub-agents, "each competent within a narrow domain and each incapable alone of producing the rich cognitive behavior they collectively enable." Intelligence emerges from "many small agents organized into agencies." Source: https://en.wikipedia.org/wiki/Society_of_Mind (reported); https://medium.com/@Micheal-Lanham/society-of-mind-the-50-year-old-blueprint-for-ai-agents-b0e62eb4ec06 (reported)

**Blackboard architecture.** Three components: (1) independent knowledge sources (specialists), (2) a shared data structure (the blackboard), (3) a control mechanism ordering knowledge source operations. Knowledge sources communicate only via the blackboard; they are unaware of each other. Source: https://en.wikipedia.org/wiki/Blackboard_system; https://mas.cs.umass.edu/Documents/Corkill/ai-expert.pdf (witnessed from search; content reported)

**Multi-agent debate / internal dialogue systems.** The search did not return a specific named paper for "multi-agent debate" or "internal dialogue" systems in LLMs. The concept of multiple LLM sessions debating to reach consensus has been implemented in frameworks (AutoGen, 2023) but no foundational paper was located in this search.

---

## C. Harness Built-In Prompts: Content and Replacement Mechanisms

### Codex CLI (OpenAI)

**Prompt structure.** The built-in prompt is at `codex-rs/core/gpt-5.1-codex-max_prompt.md` in the openai/codex repository. Content witnessed via fetch of the raw file:

- General practices: prefer `rg` for search
- Editing constraints: stick to ASCII; add comments only for non-obvious code; prefer `apply_patch` for single-file edits; handle dirty git worktrees carefully (never revert user changes, never amend commits without explicit request); stop immediately if unexpected changes appear
- Planning tool: skip for simple tasks; avoid single-step plans; update after completing subtasks
- Special user requests: answer simple requests by running terminal commands; treat "review" as code review focusing on bugs, risks, regressions
- Frontend tasks: create intentional designs, avoid generic output, use expressive typography and purposeful color
- Output presentation: concise, friendly tone; summarize substantial work; lead explanations with overview; use plain text with minimal formatting; backticks for commands and paths

Source: https://github.com/openai/codex/blob/main/codex-rs/core/gpt-5.1-codex-max_prompt.md (direct fetch, witnessed)

**Instruction hierarchy (reported).** From search results: "The LLM goes through instruction layers in order: OpenAI's hidden system prompt, model_instructions_file, AGENTS.md, and the user message." The contents of the hidden top-level OpenAI system prompt were not accessible.

**Replacement mechanism.** `model_instructions_file` in `config.toml` replaces Codex's built-in instructions. Also: `--config experimental_instructions_file=<path>`. Source: https://github.com/openai/codex/discussions/7296 (reported); https://github.com/Austin1serb/agents-md/blob/main/change-codex-system-prompt.md (reported)

### Aider

**Prompt structure.** Aider organizes prompts by coder type in `aider/coders/` (editblock, whole-file, architect, etc.). Witnessed from `aider/coders/editblock_prompts.py`:

- Role definition: "Act as an expert software developer. Follow best practices."
- File management protocol: create new files freely; for existing files not in chat, request user add them first
- Response structure: explain changes briefly; present all modifications using SEARCH/REPLACE blocks only; never return code outside these blocks
- SEARCH/REPLACE format: file path + code fence + literal matching content; blocks replace first match only
- Block best practices: match exactly, keep concise, use multiple blocks for large changes

From `aider/prompts.py` (witnessed):
- Commit message generator: Conventional Commits format, imperative mood, under 72 characters
- Undo command reply
- Added files notification
- Command execution output display
- Chat history summarization

**Replacement mechanism.** GitHub issue #1258 indicates users have requested the ability to change the system prompt; the issue was not resolved as a clean "replace" feature as of the search. No documented single flag for full replacement found.

Source: https://github.com/Aider-AI/aider/blob/main/aider/prompts.py (witnessed); https://github.com/Aider-AI/aider/blob/main/aider/coders/editblock_prompts.py (witnessed); https://github.com/Aider-AI/aider/issues/1258 (reported)

### Cline

**Prompt structure.** Witnessed from https://harrywang.github.io/cline — Cline's system prompt is described as "very long and complex." Sections:

1. Tool Use — step-by-step sequential execution requiring user approval
2. Tool Use Formatting — XML-style syntax for invoking tools
3. Tools — 12 tools listed (file operations, command execution, search, browser automation)
4. Tool Use Guidelines — best practices, confirming successful execution
5. MCP Servers — Model Context Protocol, external servers providing additional tools/resources
6. Editing Files — distinguishes file modification approaches for efficiency
7. Act Mode vs. Plan Mode — execution mode versus planning/discussion mode
8. Capabilities — available functionalities summary
9. Rules — constraints and guidelines
10. System Information — OS, shell, directories
11. Objective — structured approach to task completion

Source: https://harrywang.github.io/cline (witnessed); https://github.com/cline/cline (repository, reported)

**Replacement mechanism.** Not documented in search results. The prompt is open-source and can be modified by forking, but no runtime flag for replacement was found.

### Goose (Block / AAIF)

**Prompt structure.** Witnessed from https://deepwiki.com/block/goose/4.1.4-prompt-management:

Managed by `PromptManager` using a builder pattern. Final prompt hierarchy:
1. Base instructions: rendered `system.md` template (core identity, behavioral guidelines)
2. Mode-specific guidance: different instructions per operating mode (Auto, Approve, Chat — in Chat mode, explicit statement of no tool access)
3. Tool descriptions: extension metadata adapted to available tools
4. Additional sections: recipe-specific directions or subagent parameters (named "Additional Instructions")
5. Safeguards: warnings when tool counts exceed limits (>50 tools or >5 extensions)

Dynamic context injection adds: active MCP extensions and capabilities, project-specific hints (from `.goosehints` or `AGENTS.md`), current date/time, operating mode.

**Replacement mechanism.** Goose exposes prompts via Settings > Prompts for direct editing. Source: https://deepwiki.com/block/goose/4.1.4-prompt-management (witnessed)

### Claude Code (Anthropic)

**Prompt content.** The internal system prompt content is not publicly documented. The search returned only references to what happens when it is replaced or appended; the content itself is treated as proprietary. This report marks it: **unknown**.

**Replacement mechanism.** Two flags documented:
- `--append-system-prompt`: appends content to end of base system prompt; keeps built-in tool guidance, safety instructions, environment context
- `--system-prompt`: replaces entire system prompt; warning from docs: "Overriding the system prompt replaces Claude Code's default instructions, which include tool usage guidance, safety instructions, and environment context"

SDK alternative: `:system_prompt` to replace entirely.

Source: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts (reported); https://github.com/anthropics/claude-code/issues/6973 (reported)

### Pi harness

**Prompt content.** Pi keeps its system prompt under 1,000 tokens. It describes four core tools: read, write, edit, and bash. No further content was found. Source: https://medium.com/@codexpedite/opencode-vs-pi-which-terminal-ai-coding-agent-actually-fits-your-workflow-a9c2ab5fcc2b (reported); https://grigio.org/opencode-vs-pi-which-ai-coding-agent-should-you-use/ (reported)

**Replacement mechanism.** Not documented in search results.

### OpenCode

**Prompt content.** System prompt can reach 10K+ tokens. Reported to include extensive rules, examples, and safety instructions. Supports specialized agents and language server integration. Source: same Pi vs OpenCode comparison articles (reported)

**Replacement mechanism.** Not documented in search results.

---

## Summary Classification of Harness Prompt Content Categories

Across the harnesses above, the content categories observed are:

| Category | Codex | Aider | Cline | Goose |
|---|---|---|---|---|
| Role / identity | implied | explicit | explicit | explicit |
| Tool use mechanics | partial | format-specific | explicit | explicit |
| Tool use formatting | (apply_patch) | SEARCH/REPLACE | XML syntax | extension metadata |
| Environment / system info | git worktree rules | file scope | OS/shell/dirs | date/time, mode |
| Safety / behavioral guardrails | stop-on-surprise, no amend | file scope rules | Rules section | SmartApprove, safeguards |
| Planning / task decomposition | planning tool guidance | task framing | Act vs Plan mode | recipe system |
| Output style / presentation | concise, plain text | brief explanation | Objective section | mode-specific guidance |
| MCP / extensions | (not covered) | (not covered) | MCP Servers section | Tool descriptions, extensions |

Claude Code's categories are inferred from what the docs say is lost when the prompt is replaced (tool guidance, safety instructions, environment context) — not from reading the prompt directly.

---

*All URLs were active as of 2026-08-19. Claims marked "reported" were not directly read from the source document; claims marked "witnessed" were read directly from a fetched URL.*
