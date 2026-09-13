# Open-source coding-agent harnesses, doubting models, and harness-vs-model evidence

Research only; web access authorized by the living for this subflow. Every claim tagged (a) primary page, (b) search snippet, (c) inference.

## 1. Harnesses comparable to Claude Code / Codex CLI (Sept 2026)

### OpenAI Codex CLI (openai/codex)
- License: Apache-2.0. (b) github.com/openai/codex/blob/main/LICENSE
- Model backend: OpenAI-only in the documented app-server (model/list references only GPT-family ids like gpt-5.6-terra); no arbitrary-backend support surfaced in docs. (a) https://learn.chatgpt.com/docs/app-server
- Remote-control mechanism: **app-server**, a bidirectional JSON-RPC 2.0 protocol over stdio/WebSocket(experimental)/Unix socket, with `thread/start`, `thread/resume`, `thread/fork`, `turn/start`, `turn/steer`, interrupt, and event streaming - a real program-drivable headless/attach mechanism. (a) https://learn.chatgpt.com/docs/app-server. Community still asking for a *stable* version of this for external orchestration as of 2026 (open issue). (b) https://github.com/openai/codex/issues/36694
- Headless exec: `codex exec` runs the same core engine non-interactively for CI. (b) https://deepwiki.com/openai/codex/4.2-headless-execution-mode-(codex-exec)
- Hooks: `hooks.json` / `config.toml` hooks (e.g. `hooks.pre_tool_use.codex`) are a documented, stable surface. (b) codex.danielvaughan.com / OpenAI migration docs
- Skill/instruction injection: AGENTS.md plus a `.codex` project folder carrying config, skills, plugins, subagents. (b) https://blakecrosley.com/guides/codex
- Note: the standalone `codex mcp-server` binary was removed; MCP and app-server are now distinct surfaces - integrations must use app-server, not MCP tool calls, for full control. (a) https://learn.chatgpt.com/docs/app-server

### OpenCode (sst/opencode)
- License: MIT. (b) github.com/sst/opencode/blob/dev/LICENSE
- Model backend: connects to 75+ providers, "any LLM you point it at" - explicitly arbitrary/BYOK. (b) developersdigest.tech/blog/opencode-developer-guide-2026
- Remote-control mechanism: `opencode serve --port 4096` runs a headless HTTP server with an OpenAPI spec at `/doc`, plus an official `@opencode-ai/sdk` - this is the strongest "program can drive it" story of the field besides Codex's app-server. (b) developersdigest.tech; dev.to/rosgluk
- Hooks: plugin system with `message.part.removed/updated`, `message.removed/updated`, `session.created/updated/compacted`, `tui.prompt.append`, and an `experimental.session.compacting` hook for injecting context before compaction. (a) https://opencode.ai/docs/plugins/ - note: no explicit "on incoming user prompt" hook was found in the fetched doc excerpt; may exist under a name not surfaced.
- Skill/instruction injection: discovers `SKILL.md` from `.claude/skills/`, `.agents/skills/`, `.opencode/skill/`, and config paths/URLs; plugins can register skills as dynamic tools. (b) via search snippet of opencode docs

### Goose (Block, now under Agentic AI Foundation / Linux Foundation)
- License: Apache-2.0; moved from Block to the Agentic AI Foundation (Linux Foundation) April 2026. (b) search snippet citing project move
- Model backend: "any LLM," general-purpose (not code-only). (b) blog.agentailor.com
- Remote-control mechanism: CLI headless automation "for running recipes on remote servers, integrating into CI/CD," plus a documented API "to embed it anywhere." Desktop/CLI/API triad. (b) pulsemcp.com / goose-docs.ai. Exact program-drivable RPC/session-attach protocol was not independently confirmed on a primary API-reference page in this pass - treat as (c) probable but unverified in depth.
- Hooks/skill injection: **Recipes** (YAML) bundle instructions (system prompt), initial prompt, MCP extensions, parameters, sub-recipes - this is the injection mechanism. (a) https://goose-docs.ai/docs/guides/recipes/. Ships built-in prompt-injection detection and an "adversary reviewer" mode as a safety feature, notable given the living's harness-purity concerns. (b) maxamillion.sh blog

### OpenHands (All Hands AI)
- License: MIT. (b) search snippet; theaiagentindex.com
- Model backend: BYOK via LiteLLM abstraction - effectively arbitrary/OpenAI-compatible. (b) openhands.dev blog
- Remote-control mechanism: `--headless` for CI/CD, `--resume` to reattach a conversation, and (recent releases) a REST API for programmatic task submission - real remote-control surface. Architecture: Python controller + Docker sandbox over a socket. Rebuilt on a new "Software Agent SDK" for the 1.0 line in 2026 (at v1.7.0 as of May 2026). (b) openhands.dev blog; github PRs
- Hooks: documented lifecycle hooks - `PreToolUse`, `PostToolUse`, `UserPromptSubmit` - explicitly including a hook keyed on the incoming user prompt, which answers the "hooks on incoming prompts" criterion directly. (b) dev.to/truongpx396 deep-dive
- Skill/instruction injection: **microagents** (renamed "skills" in the V1/SDK line) - markdown files with frontmatter (`trigger_type: always` or keyword-triggered), plus `.openhands_instructions` / `.openhands/` repo-root customization (setup script, pre-commit script). (a)/(b) github.com/OpenHands/OpenHands/blob/main/skills/README.md and related issues

### Aider
- License: Apache-2.0 (long-standing; not independently re-verified this pass - (c)).
- Model backend: explicitly vendor-agnostic - GPT-5 family, Claude 4.x, Gemini 2.5 Pro, DeepSeek V3.2/R1, Grok 4, Ollama, dozens more. (b) betterstack.com guide
- Remote-control mechanism: weak by this report's key criterion. Aider is designed around stdin/stdout against the local filesystem and SSH/CI scripting, not an attach/app-server protocol with session objects a program can steer mid-turn. (b) tembo.io / betterstack.com. No app-server-style JSON-RPC surface was found.
- Hooks: editor-integration hooks exist (e.g. `aidermacs-before-run-backend-hook` in the Emacs wrapper), but this is a client-side wrapper hook, not a first-class Aider hook system. (b) github.com/MatthewZMD/aidermacs
- Skill/instruction injection: conventions files (`CONVENTIONS.md`) and repo maps; automatic git commit messages. Weaker/less structured than AGENTS.md/microagents/SKILL.md ecosystems. (c)

### Pi (earendil-works/pi, `@mariozechner/pi-coding-agent`)
- License: MIT. (b) search snippet, ~64-98k stars depending on source (numbers disagree across sources - flagged, not resolved). (b)
- Model backend: 20+ providers (Anthropic, OpenAI, Google, xAI, DeepSeek, Mistral, Groq) plus subscription login (Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot) instead of API keys. (b) llmreference.com / silenceper.com
- Remote-control mechanism: four modes - interactive, print/JSON, **RPC for process integration**, and an SDK for embedding - this is a direct, named answer to "remote control a program can drive." Also: sessions can be rewound/branched and shared. (b) silenceper.com/en/article/2026-05-27-pi-coding-agent-harness/
- Hooks/skill injection: TypeScript Extensions, Skills, Prompt Templates, Themes - adapts without forking internals. (b) same source
- Minimal core toolset (Read/Write/Edit/Bash only) - deliberately lean, which the living's "right ontology and guidance" framing may find attractive as a clean substrate. (c)

### Others surfaced but not deeply verified (flagging for follow-up, not fully sourced this pass)
- Crush, Plandex, Amp, mini-swe-agent - named in a 2026 "underrated harnesses" roundup alongside Pi; not individually verified against the four criteria here. (b) https://dev.to/rigor120000/underrated-ai-coding-agent-harnesses-in-2026-pi-mini-swe-agent-crush-plandex-amp-and-more-5c0a

### Summary judgment (c, inference from the above)
For the living's specific ask - "remote control, essentially open-source Claude and Codex with remote control" - the two strongest matches on the key criterion (a program can drive an attached/headless session, not just fire-and-forget CLI calls) are:
1. **Codex CLI's app-server** (JSON-RPC, thread/turn primitives, steerable mid-turn) - closest structural analog to what this flow pair already uses against Claude via the injector tooling.
2. **OpenCode's `serve` HTTP API + SDK**, and **Pi's RPC mode**, both MIT-licensed and arbitrary-model, are close seconds and notably more open on model backend than Codex.
OpenHands's REST headless API and hook set (including `UserPromptSubmit`) is a credible third, MIT-licensed, with the most explicit "hooks on incoming prompts" story of the group.

## 2. Open-weight models for a doubting/critical-reviewer role

- Token cost noted as explicitly not a concern per the living's framing - so ranking here is by critique quality only, not price/latency.
- **Kimi K2.7 Code** (open-weight) led a 13-model code-review comparison at 0.179 critical findings per review, edging out Grok 4.5 (0.176, closed) and beating Laguna M.1 (0.171, open) - "open-weight models matched the strongest closed model on critical findings per review," occupying 2 of top 3 spots. (a) https://kilo.ai/articles/open-weight-models-code-review
- Same source: GLM-5.2 models scored much lower (0.020-0.041 critical findings/review) and skewed toward soft "suggestions" (58%) rather than critical calls - i.e., less doubtful, more agreeable, in code review specifically. (a) same URL
- On a separate, general (non-code) sycophancy leaderboard (lechmazur/sycophancy, "sides with narrator on both opposing framings of the same case"): Qwen 3.7 Flash had the lowest sycophancy among the open models checked (2.5%) but only moderate decisive coverage (32.8%); Kimi K3 combined middling sycophancy (4.5%) with the highest decisiveness in the whole leaderboard (90.4%) - i.e. it commits to a stance most often, which is a different (and arguably more useful for a "doubter" role) property than raw non-agreement; GLM-5.2 was worse than DeepSeek/Qwen/Kimi on this axis (12.6% sycophancy). (a) https://github.com/lechmazur/sycophancy/
- Tool-use/function-calling context (may matter for a doubting-reviewer-as-agent role): GLM-4.5 reported at 77.8% function calling and 90.6% tool-use success vs Claude Sonnet 89.5%, Kimi K2 86.2%, Qwen3-Coder 77.1%, DeepSeek-R1 63.8%. (b) search snippet aggregating turingpost.com and akitaonrails.com comparisons - not independently verified on a primary benchmark page.
- General caution across the literature: LLMs "struggle with uncertain evidence and cannot exhibit skepticism when studies present design flaws," show "limitations in detecting deeper theoretical flaws, identifying missing metrics, and recognizing overstated conclusions," and are "optimised for plausibility, not correctness" - this applies to models generally, not to any one open-weight model specifically, and tempers all of the above rankings. (b) search-snippet synthesis citing arxiv.org/pdf/2501.10326 (LLM scholarly-review survey) and arxiv.org/pdf/2503.22989 (FindTheFlaws)

### Answer to "what's the most doubtful model" (c, inference synthesizing 2 and 3 above)
No single benchmark directly measures "doubtfulness" as the living means it (a critical peer that pushes back rather than converges). The closest available evidence points to **Kimi's K-series** (K2.7 Code for code-critique volume/quality; K3 for general decisiveness under pushback) as the strongest open-weight candidate for a skeptical-reviewer role, with **Qwen's fast variants** as the lowest-raw-sycophancy alternative and **GLM** consistently the *least* doubtful/most agreeable of the four families checked (DeepSeek, Qwen, Kimi, GLM) across both the code-review and general sycophancy evidence. DeepSeek sits in the middle on both axes reviewed. This is a synthesis across two different benchmarks measuring adjacent but not identical properties - treat as directional, not definitive.

## 3. Evidence that harness design lets a weaker model match a stronger one

The living's claim - "if you do the harness right and give the right ontology and guidance, you can make any model in the right harness ... look it up" - has real, recent, directly-on-point published evidence, though none of it says "any model, unconditionally":

- **Harness-Bench** (arXiv 2605.27922, a primary abstract read): 106 realistic agent tasks show large performance variation purely from harness (context/tool/state/permission/tracing/recovery layer) held against the same base models; the paper's headline claim is that "agent capability should be reported at the model-harness configuration level rather than attributed to the base model alone." It also names "execution-alignment failures" (reasoning disconnected from tool output/evidence) as the dominant failure mode - i.e. harness quality, not raw model strength, is often the bottleneck. (a) https://arxiv.org/abs/2605.27922
- **AI4AI: Strong-to-Weak Capability Transfer via Harnesses** (arXiv 2608.12307, primary abstract read): a stronger model *designs* an inference-time harness (deterministic code offloading for unstable reasoning steps, task-specific routing, strict output-format enforcement) for a weaker model, with no weight changes to the weaker model. Result: weaker-model Theory-of-Mind score rose from 0.49 to 0.91 average - nearly doubling - and the paper states explicitly that "weaker target models receive the largest gains," with gains coming from structural harness changes rather than more elaborate prompting of the weak model itself. This is close to a direct confirmation of the living's specific claim, on the tasks tested (Theory-of-Mind, not general coding). (a) https://arxiv.org/abs/2608.12307
- **Co-Evolving Harnesses and Models** (arXiv 2609.09134, primary abstract read): harness evolution alone lets a weaker model gain substantially on 7 enterprise agentic benchmarks; but naive imitation of an expert's harness-derived trajectories by the weaker model backfires (regressions of 4-30 points across Qwen3-Coder and Gemma 4), because the model "adopts the expert's planning strategy without the competence to execute it." Their fix (on-policy expert correction of only the weak model's own failing turns) recovers the gains. This is the important caveat to the living's claim: **the "right guidance" must fit the model's own competence, not just be copied wholesale from a stronger model's style** - a mismatched harness/ontology can make a weak model worse, not better. (a) https://arxiv.org/abs/2609.09134
- **"From Model Scaling to System Scaling"** (arXiv 2605.26112) was surfaced as directly on-topic ("scaling the harness in agentic AI") but not fetched/read this pass - noted as a further primary source to pull if the living wants more. (b) title/URL only from search results

### Verdict on the claim
Evidence is not thin - three separate 2026 papers converge on: harness/ontology design produces large, measured gains for weaker models on agentic and reasoning tasks, sometimes matching or nearly matching stronger-model performance on the specific benchmarks tested. But all three also show boundary conditions: gains are task-specific (ToM, enterprise agent benchmarks, 106-task agent suite), and copying a stronger model's harness/trajectories verbatim can hurt a weaker model unless the correction stays anchored to what that model can actually execute. So "any model in the right harness" is not fully supported - "the right harness increases the ceiling a lot, but the harness must match the model's own competence" is what the current literature actually shows.

## Sources referenced
- https://learn.chatgpt.com/docs/app-server
- https://github.com/openai/codex (LICENSE, issues #36694, #4219, #2798)
- https://opencode.ai/docs/plugins/
- https://github.com/sst/opencode
- https://developersdigest.tech/blog/opencode-developer-guide-2026
- https://goose-docs.ai/docs/guides/recipes/
- https://maxamillion.sh/blog/stop-building-agents-start-harnessing-goose/
- https://www.openhands.dev/blog/open-source-ai-coding-agents
- https://github.com/OpenHands/OpenHands/blob/main/skills/README.md
- https://dev.to/truongpx396/openhands-deep-dive-build-your-own-guide-1al0
- https://betterstack.com/community/guides/ai/aider-ai-pair-programming/
- https://github.com/MatthewZMD/aidermacs
- https://silenceper.com/en/article/2026-05-27-pi-coding-agent-harness/
- https://github.com/earendil-works/pi
- https://dev.to/rigor120000/underrated-ai-coding-agent-harnesses-in-2026-pi-mini-swe-agent-crush-plandex-amp-and-more-5c0a
- https://kilo.ai/articles/open-weight-models-code-review
- https://github.com/lechmazur/sycophancy/
- https://arxiv.org/abs/2605.27922 (Harness-Bench)
- https://arxiv.org/abs/2608.12307 (AI4AI strong-to-weak)
- https://arxiv.org/abs/2609.09134 (Co-Evolving Harnesses and Models)
