# The Jev ecosystem

Research for the living's order of 2026-10-04: a book on our open-source stack, starting with how Jev is used, the tools, plugins, infrastructure and trends around it. It extends `flows/93ba9f/reports/jev-and-openrouter.md` (identity, OpenRouter setup) and `flows/d66c26/reports/jev-reuse-book-evidence.md` (Rust reuse audit) and does not repeat them. Web findings are this worker's reading of public pages and registry APIs on 2026-10-04; nothing was installed or called. Star counts and dates move daily. "Not verified" marks a claim taken from one secondary page only.

## 1. How Jev is used

### Question kinds

There are still exactly three. No fourth kind is documented in the API reference ([api](https://docs.typesafe.ai/api.md)).

| Kind | Asks | `criteria` | Answer fields | Limit |
|---|---|---|---|---|
| `noul` | Is this true? | optional `{true, false}` descriptions | `noul` (0–1) | — |
| `choice` | Which option? | map option → description or `null` | `choice`, `probabilities`, `confidence` | max 255 options |
| `score` | Which level? | ordered array of level descriptions | `score` (can fall between levels), `legend`, `probabilities`, `confidence` | 2–10 levels |

New since the earlier reports:
- `instructions` and every criterion can be a string, an object or an array. Data a question refers to can sit beside it and be named in backticks, as can paths into state such as `` `ticket.messages[0].text` `` ([api](https://docs.typesafe.ai/api.md), [advanced structure](https://docs.typesafe.ai/primitives/advanced.md), [primitives](https://docs.typesafe.ai/primitives.md)).
- Question keys are not sent to the model. Answers are independent: one answer never becomes context for another in the same request ([api](https://docs.typesafe.ai/api.md), [primitives](https://docs.typesafe.ai/primitives.md)).
- The response carries `model` (the versioned ID that answered, e.g. `jev-1.13.0`) and `usage {input_tokens, output_tokens}` ([api](https://docs.typesafe.ai/api.md)).
- `GET /v1/models` lists the aliases. `jev-latest` and `jev-preview` both point to `jev-1.13.0`. TypeSafe advises pinning the versioned ID once confidence thresholds are tuned ([models](https://docs.typesafe.ai/models.md)).
- Errors are 401, 422, 429 (rate limit) and 529 (overloaded). The SDKs retry with backoff and honour `retry-after` ([api](https://docs.typesafe.ai/api.md), [models](https://docs.typesafe.ai/models.md)).

Example answer, from the docs ([api](https://docs.typesafe.ai/api.md)):

```json
{"model":"jev-1.13.0","answers":{"department":{"type":"choice","choice":"billing",
 "probabilities":{"billing":0.88,"technical":0.12,"sales":0.0},"confidence":0.81}},
 "usage":{"input_tokens":318,"output_tokens":34}}
```

### Prices and limits as published

| Item | TypeSafe direct ([models](https://docs.typesafe.ai/models.md)) | Elsewhere |
|---|---|---|
| Price | $0.042 / Mtok input; output free | Same on OpenRouter ([model page](https://openrouter.ai/typesafe/jev-1.13)) and OpenCode Zen; Zen also lists a free `jev-1.13-free` ([Zen](https://opencode.ai/docs/zen/)) |
| Context | 64k per request; 32k for state plus the longest question | OpenRouter lists 32K ([model page](https://openrouter.ai/typesafe/jev-1.13)). The two figures describe different budgets |
| Rate limits | 100K tokens/s and 80 requests/s, "adjusting dynamically… can change without notice" | 2026-10-01 article quoted 250K tok/s and 1,200 req/min ([flaviocopes](https://flaviocopes.com/jev/)). The docs figure is the current one |
| Input | Text, JSON object, or array of text; no image, audio or video | — |
| Customisation | No fine-tuning or LoRA; one set of weights serves every account | — |
| Data | Not trained on customer traffic; ZDR for enterprise | ([legal](https://docs.typesafe.ai/legal.md)) |

### Known weak spots, from TypeSafe's own list

The [jaggedness page](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md), reviewed 2026-10-02, names nine failure modes:
- literal reading;
- math and counting;
- date comparison;
- indirection;
- large or irrelevant state ("context rot");
- adversarial content in state;
- contradictory instructions and criteria;
- a bias toward the first Choice option;
- generation.

For each it gives the same advice: keep arithmetic and dates in code, filter state first, and reorder options to check consistency.

### Documented uses and patterns

TypeSafe publishes four patterns and about twenty cookbooks ([index](https://docs.typesafe.ai/llms.txt)).

| Use | TypeSafe source | Shape |
|---|---|---|
| Batching (speculative fan-out) | [fan-out](https://docs.typesafe.ai/patterns/fan-out.md), [parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions.md) | 13 questions in one call: 12.2× cheaper, 10× faster, same answers |
| Confidence-gated routing | [confidence routing](https://docs.typesafe.ai/patterns/confidence-routing.md), [confidence](https://docs.typesafe.ai/confidence.md) | answer = what; confidence = whether to act |
| Intent routing | [intent routing](https://docs.typesafe.ai/patterns/intent-routing.md) | to code, a specialist LLM, or a human |
| Composite scoring | [composite](https://docs.typesafe.ai/patterns/composite-scoring.md) | atomic scores, weights kept in code |
| Classification | [hierarchical](https://docs.typesafe.ai/cookbooks/hierarchical_classification.md), [SEC industries](https://docs.typesafe.ai/cookbooks/classification_using_confidence.md) | beam search over Choice probabilities; fall back to the parent class when confidence is low |
| Extraction | [date extraction](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook.md), [pre-parsed values](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook.md), [SDE cascade](https://docs.typesafe.ai/cookbooks/sde_cascade.md) | regex or LLM proposes candidates; Jev picks one; code normalises |
| Reranking and search | [rerank](https://docs.typesafe.ai/cookbooks/rerank_typesafe.md), [line search](https://docs.typesafe.ai/cookbooks/semantic_find.md), [RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages.md) | one question per candidate, or a Choice over line IDs |
| Agent skill selection | [skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion.md) | at most one of 182 Hermes skills, in two requests |
| Guardrails and checks | [LLM guardrails](https://docs.typesafe.ai/cookbooks/llm_guardrails.md), [citation check](https://docs.typesafe.ai/cookbooks/citation_check.md) | pass, review, block or route |
| Function calling | [function calling](https://docs.typesafe.ai/cookbooks/function_calling.md) | function name and closed-set arguments as questions |

TypeSafe says plainly that Jev is not a replacement LLM for a coding agent. "There is no `model: "jev-latest"` setting that turns your coding agent into a Jev-powered agent." Instead, use the agent to write code that calls Jev ([coding agents](https://docs.typesafe.ai/introduction/coding-agents.md)).

Public projects using these patterns:
- email triage ([jevmail](https://github.com/fazlerocks/jevmail));
- input moderation in Mastra, which blocked 9 of 9 hostile and 0 of 49 real messages, as reported by its author ([mastra-jev-moderation](https://github.com/CodeAlive-AI/mastra-jev-moderation));
- a calibrated reranker ([hev/reranker](https://github.com/hev/reranker));
- Postgres predicates ([pg-jev](https://github.com/realZachi/pg-jev)).

## 2. Tools

### Official, from TypeSafe ([github.com/typesafe-ai](https://github.com/typesafe-ai))

| Repo / package | License | Last release | Covers |
|---|---|---|---|
| [typesafe-sdk-python](https://github.com/typesafe-ai/typesafe-sdk-python) / PyPI `typesafe-sdk` | MIT | 0.7.2, 2026-09-26 ([PyPI](https://pypi.org/project/typesafe-sdk/)) | sync and async clients, retries, typed questions and answers |
| [typesafe-sdk-js](https://github.com/typesafe-ai/typesafe-sdk-js) / npm `@typesafe-ai/sdk` | MIT | 0.6.0, 2026-09-15 ([npm](https://www.npmjs.com/package/@typesafe-ai/sdk)) | `TypeSafeClient`, `choice()` / `noul()` / `score()` |
| [skills](https://github.com/typesafe-ai/skills) | MIT | no release; about 2.6k stars | agent skill; Claude Code plugin `typesafe@typesafe-ai`; `npx skills add` for other agents ([agent skill](https://docs.typesafe.ai/agent-skill.md)) |
| [system-one-adapter-python](https://github.com/typesafe-ai/system-one-adapter-python) | MIT | no release | "Drop-in TypeSafeClient replacement backed by LLM APIs", for cost and accuracy comparison |
| [n8n-nodes-typesafe-ai](https://github.com/typesafe-ai/n8n-nodes-typesafe-ai) | MIT | no release | n8n node |
| [WorkflowEvals](https://github.com/typesafe-ai/WorkflowEvals) | Apache-2.0 | no release | code behind [evals.typesafe.ai](https://evals.typesafe.ai) |

TypeSafe publishes no weights, no training code and no `typesafe-ai/jev` repo ([jev-ai.org survey](https://jev-ai.org/blog/jev-github/), consistent with the org listing above). No official CLI, Rust, Go or Clojure SDK was found.

### Gateways that serve Jev

All four hosts take the same System One request shape ([gateway survey](https://jevtypesafeai.com/get-jev), not verified per host).

| Host | Model ID | Endpoint | Source |
|---|---|---|---|
| TypeSafe | `jev-latest` | `api.typesafe.ai/v1/systemone` | [api](https://docs.typesafe.ai/api.md) |
| OpenRouter | `typesafe/jev-1.13` | `/api/alpha/decisions`, `/api/v1/systemone` | earlier reports |
| OpenCode Zen | `jev-1.13`, `jev-1.13-free` | `opencode.ai/zen/v1/systemone` | [Zen](https://opencode.ai/docs/zen/) |
| Vercel AI Gateway | `typesafe-ai/jev` | AI Gateway | [Vercel](https://vercel.com/i/jev-integrations), [flaviocopes](https://flaviocopes.com/jev/) |
| Cloudflare | `typesafe/jev` | AI Gateway / Workers AI | [AICrier](https://aicrier.com/post/c9kqhtucxuduminzo4iz), [CloudflareDev on X](https://x.com/CloudflareDev/status/2100688880798159254) — not verified |

### Community clients by language

Registry metadata was read on 2026-10-04. Every client listed is unofficial.

| Language | Client | License | Maintainer | Last release | Covers |
|---|---|---|---|---|---|
| Rust | [typesafe-sdk](https://crates.io/crates/typesafe-sdk) ([repo](https://github.com/codeitlikemiley/typesafe-sdk-rust)) | MIT | codeitlikemiley | crate 0.2.0, 2026-09-29; most downloaded (about 1.2k) | direct TypeSafe API |
| Rust | [typesafe-system-one](https://crates.io/crates/typesafe-system-one) ([repo](https://github.com/haileyok/typesafe-client)) | MIT | haileyok | **GitHub release `rust/v0.1.1`, 2026-09-26** — the earlier report said there was none; there now is one | System One; OpenRouter base URL documented |
| Rust | [fuzzy-jev](https://crates.io/crates/fuzzy-jev) | MIT | dsaad68 | 0.6.0, 2026-10-01 | OpenRouter `/alpha/decisions` |
| Rust | [jev-driver](https://crates.io/crates/jev-driver) + `jev-driver-macros` | Apache-2.0 | Shearerbeard | 0.1.0, 2026-10-02 | derive macros `JevChoice` / `JevScore` / `JevNoul` |
| Rust | [jev](https://crates.io/crates/jev) ([GitLab](https://gitlab.com/porky11/jev)) | see crate | porky11 | 0.1.2, 2026-09-22 | TypeSafe plus self-hosted compatible backends |
| Rust | [jevkit-cli](https://crates.io/crates/jevkit-cli), [nu_plugin_jev](https://crates.io/crates/nu_plugin_jev) | see crate | ariel-frischer, gleb-chipiga | 0.4.2, 0.1.1 | CLI; Nushell plugin |
| TypeScript | [@patdown/jev](https://www.npmjs.com/package/@patdown/jev), [jev-systemone](https://www.npmjs.com/package/jev-systemone) | see npm | tyler.earth, sc0d3r | 0.9.0, 0.1.1 | Effect HttpClient; TypeSafe plus OpenCode Zen |
| Python | [`jev`](https://pypi.org/project/jev/) | see PyPI | — | 0.3.0, 2026-09-18 | decorator that compiles a Python function into Jev questions |
| Go | [haileyok/typesafe-client](https://github.com/haileyok/typesafe-client) (Go half), [atharvamhaske/typesafe-sdk-go](https://github.com/atharvamhaske/typesafe-sdk-go) | MIT | haileyok, atharvamhaske | —, v0.2.0 2026-09-21 | System One |
| Clojure | **none found** on GitHub search ("jev clojure", "babashka jev") | — | — | — | — |
| Others | Java, Kotlin, Swift, C#, Elixir, Ruby, PHP, C++, Godot, Nushell | mostly MIT | many | — | ([search](https://github.com/search?q=typesafe-sdk&type=repositories), [awesome-typesafe-jev](https://github.com/AbdelStark/awesome-typesafe-jev)) |

Standalone CLIs:
- [`@jev-harness/cli`](https://www.npmjs.com/package/@jev-harness/cli): `jev ask`, `eval`, `jev-gate`;
- [jev-axi](https://www.npmjs.com/package/jev-axi);
- [jev-kit](https://www.npmjs.com/package/jev-kit);
- [jev-repl](https://crates.io/crates/jev-repl).

## 3. Plugins and integrations

### Agent harnesses

| Harness | Project | Kind | Notes |
|---|---|---|---|
| Claude Code | official [skills](https://github.com/typesafe-ai/skills) plugin | skill | teaches the agent to write Jev code |
| Claude Code | [fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) | compaction | about 7.4k stars, MIT; Jev scores each tool call instead of an LLM summary |
| Claude Code | [jev-router](https://github.com/gargpratyush/jev-router), [jev-enforce](https://www.npmjs.com/package/jev-enforce), [claude-x-jev](https://github.com/charlesdove977/claude-x-jev), [jevmem](https://github.com/Avinash-jetwani/jevmem) | routing, CLAUDE.md enforcement, memory | — |
| Claude Code / Codex / pi / OpenCode | [jev-code](https://github.com/FrancoisChastel/jev-code) | tool | MIT, v0.4.1 on 2026-10-03; OpenRouter and Vercel hosts ([PR 7](https://github.com/FrancoisChastel/jev-code/pull/7)) |
| Claude Code / Codex / pi | [jev-use](https://github.com/shitianfang/jev-use) | hands steps with no text output to Jev | MIT, v0.6.0 |
| Codex | [jev-codex-router](https://github.com/0xNatoshi/jev-codex-router), [codex-systemone-router](https://www.npmjs.com/package/codex-systemone-router) | per-turn model and effort routing | — |
| pi | [pi-jev-auto-mode](https://github.com/jomatsu/pi-jev-auto-mode), [pi-typesafe](https://www.npmjs.com/package/pi-typesafe), [pi-jev](https://www.npmjs.com/package/pi-jev), [pi-jev-guard](https://www.npmjs.com/package/pi-jev-guard), [pi-system-one](https://www.npmjs.com/package/pi-system-one), [@cr1ms0n/pi-subagent](https://www.npmjs.com/package/@cr1ms0n/pi-subagent) | auto-approval, tool routing, bash gating, subagent routing | the densest plugin scene of the four harnesses |
| OpenCode | [opencode-jev-router](https://www.npmjs.com/package/opencode-jev-router), [opencode-auto-jev](https://www.npmjs.com/package/opencode-auto-jev), [opencode-smart-reasoning](https://www.npmjs.com/package/opencode-smart-reasoning), [fast-jev-opencode](https://github.com/nrdz-labs/fast-jev-opencode), [openjev](https://github.com/darwintechlab/openjev), [opencode-shell-safety](https://www.npmjs.com/package/opencode-shell-safety) | subagent routing, reasoning effort, pruning, shell permission | smart-reasoning uses Zen's SystemOne |
| Herdr | [jev-herdr](https://github.com/alexzfe/jev-herdr) | spawns Claude Code agents in Herdr with Jev choosing model and effort | MIT, 0 stars, no release |
| Cursor | **none found** | — | TypeSafe lists Cursor only among agents Jev does *not* replace ([coding agents](https://docs.typesafe.ai/introduction/coding-agents.md)) |
| MCP (any) | [jev-mcp (jkudish)](https://github.com/jkudish/jev-mcp), [typesafe-mcp](https://pypi.org/project/typesafe-mcp/), [decisions-judge-mcp](https://github.com/clouatre-labs/decisions-judge-mcp) | judgment tools | jev-mcp: MIT, about 490 stars, v0.13.0 on 2026-10-02 |

### Workflow frameworks

| Framework | Integration | Status |
|---|---|---|
| Vercel AI SDK | [`@ai-sdk/typesafe-ai`](https://ai-sdk.dev/providers/ai-sdk-providers/typesafe-ai) | first-party, Apache-2.0, 3.0.12 on 2026-09-30; `typeSafeAi.evaluationModel('jev-latest')` with `experimental_evaluate`; Noul surfaces as `boolean` |
| LangChain (Python) | [`langchain-typesafe`](https://docs.langchain.com/oss/python/integrations/providers/typesafe) | first-party, MIT, 0.0.1a3; `TypeSafeClassifier` Runnable; experimental `ModelRouterMiddleware` and `AutoModeMiddleware` (risky tool call → error ToolMessage) |
| LangChain (JS) | [`@langchain/typesafe`](https://www.npmjs.com/package/@langchain/typesafe) | first-party, MIT, 0.0.2 on 2026-10-01 |
| Effect | [`@effect/ai-typesafe`](https://www.npmjs.com/package/@effect/ai-typesafe) | 4.0.1, 2026-10-04 |
| Mastra | community [mastra-jev-moderation](https://github.com/CodeAlive-AI/mastra-jev-moderation) (MIT, one file) | upstream processor [PR 24372](https://github.com/mastra-ai/mastra/pull/24372) **closed unmerged** |
| n8n | official [n8n-nodes-typesafe-ai](https://github.com/typesafe-ai/n8n-nodes-typesafe-ai) plus at least six community nodes ([npm search](https://www.npmjs.com/search?q=n8n-nodes-typesafe)) | — |
| Others | OpenClaw [`@openclaw/typesafe`](https://www.npmjs.com/package/@openclaw/typesafe), RubyLLM [provider](https://github.com/javiergradiche/ruby_llm-providers-typesafe), ComfyUI [systemone-nodes](https://github.com/rockerBOO/systemone-nodes), Home Assistant [HA-SystemOne](https://github.com/AtHeartEngineer/HA-SystemOne) | — |

### Observability and testing

- [`@arizeai/openinference-instrumentation-typesafe`](https://www.npmjs.com/package/@arizeai/openinference-instrumentation-typesafe): OpenInference/OTel tracing of the TS SDK. Apache-2.0, 0.1.0, Arize maintainers.
- [jeview](https://github.com/andududu/jeview): local live viewer of every call. MIT.
- [`@gbesse/jev-shadow`](https://www.npmjs.com/package/@gbesse/jev-shadow): runs a decision provider in shadow mode and measures disagreement.
- [jevkit-vitest](https://www.npmjs.com/package/jevkit-vitest): records and replays requests as `.jevl` cassettes.
- [AnthusAI/Jev-Calibration](https://github.com/AnthusAI/Jev-Calibration): Platt recalibration of confidence.
- No Langfuse- or Helicone-specific integration was found.

## 4. Infrastructure

### Local and self-hosted serving

Jev itself cannot be self-hosted: there are no weights ([jev-ai.org](https://jev-ai.org/blog/jev-github/), [flaviocopes](https://flaviocopes.com/jev/)). What exists is open models and servers that speak the same `/v1/systemone` shape.

| Project | What | License | Notes |
|---|---|---|---|
| Cloudflare **Clef** / **Clef-flash** | open-weight decision models, System One-compatible | Apache-2.0 | [blog](https://blog.cloudflare.com/clef-decision-models/), [HF](https://huggingface.co/Cloudflare/clef). Clef is post-trained from `Qwen/Qwen3.8-27B` (about 27.4B params, per the HF API), multimodal, 64k context, on Workers AI and vLLM; released 2026-10-01 |
| [autotrust/JEV-27B-VL](https://huggingface.co/autotrust/JEV-27B-VL), JEV-9B, JEV-27B | community open models | see HF | JEV-27B-VL: about 726k downloads, the most-downloaded "jev" model on HF |
| [Ollaya](https://ollaya.dev/) | "Ollama for Jev-style decision models" | — | [HN, 618 points](https://news.ycombinator.com/item?id=49848269) |
| [llama-system1](https://www.npmjs.com/package/llama-system1) | llama.cpp `/v1/systemone` shim | — | 1.1.0, 2026-10-04 |
| Laya: [`@metalagman/layajev`](https://www.npmjs.com/package/@metalagman/layajev), [maclaya](https://www.npmjs.com/package/maclaya), [laya-system-one](https://www.npmjs.com/package/laya-system-one) | local Jev-compatible server (Linux binary; Apple Silicon) | — | upstream `convaiinnovations/laya` returned 404 — not verified |
| [simple-jev](https://github.com/featherless-ai/simple-jev), [AnyJev](https://github.com/nokia-applied-research/AnyJev), [jev-bridge](https://crates.io/crates/jev-bridge), [SystemOneHarness](https://github.com/HarnessRouter/SystemOneHarness), [lichen](https://github.com/Mushroom-Systems/lichen) | turn any open or OpenAI-compatible model into a Jev endpoint | Apache-2.0 / MIT | AnyJev: about 1k stars, Nokia Applied Research |
| [SemIf-OpenJev](https://github.com/TheoLeeCJ/SemIf-OpenJev), [NanoJev](https://github.com/TianyuCodings/NanoJev), [kev](https://github.com/jaredpalmer/kev), [jeff](https://github.com/firelex/jeff), [feder-cr/jev](https://github.com/feder-cr/jev) | open replicas or training pipelines | MIT | SemIf runs on a single 3090; jeff: 0.8B, about 30 ms ([HN](https://news.ycombinator.com/item?id=49883844)) |

### Nix

- No nixpkgs package or nixpkgs PR was found for any TypeSafe SDK or Jev client.
- One flake exists: [jev-nixos-setup](https://github.com/mustapha-rashiduddin/jev-nixos-setup) — packaging, CLI and sops key storage. No license, 0 stars.
- TypeSafe's org has a [daggerverse](https://github.com/typesafe-ai/daggerverse), which is not Nix.

### Rate limiting, batching, caching

- **Rate limiting.** Use the SDKs' built-in retry (`RetryPolicy`: attempts, retryable statuses, backoff, honouring `retry-after`) ([Python retries](https://docs.typesafe.ai/sdk/python/api/retries.md)). Raw HTTP callers must back off on 429 and 529 themselves ([api](https://docs.typesafe.ai/api.md)).
- **Batching.** The intended form is many questions per state in one request ([parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions.md)). Fan-out across states is client-side; see the batch WebUI [jev-webui](https://github.com/chcknnbn/jev-webui). No server-side batch API is documented.
- **Caching.** No server-side or prompt cache is documented ([flaviocopes](https://flaviocopes.com/jev/)). Community options:
  - record and replay for tests ([jevkit-vitest](https://www.npmjs.com/package/jevkit-vitest));
  - an experimental verified response cache ([jev-cache](https://github.com/chaqchase/jev-cache), Apache-2.0, 1 star).

  Because output is free and only input is billed, caching saves only the input tokens of a repeated state (an inference from the price table, not a published claim).

## 5. Trending

### What people are building (2026-09-15 to 2026-10-04)

Jev launched on 2026-09-15, so "last month" and "this month" together are the three weeks since. The table counts GitHub stars as of 2026-10-04.

| Theme | Leading examples |
|---|---|
| Browser and computer-use agents | [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast) (about 22k), [jev-voice-browser](https://github.com/moritzkremb/jev-voice-browser), [jev-mcp](https://github.com/jkudish/jev-mcp) |
| Coding-agent plumbing (compaction, routing, approval, code search) | [fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) (about 7.4k), [jevgrep](https://github.com/dzhng/jevgrep) (about 2.2k), the pi and OpenCode plugins in §3 |
| Open replicas and local decision models | [SemIf-OpenJev](https://github.com/TheoLeeCJ/SemIf-OpenJev) (about 4.7k), [NanoJev](https://github.com/TianyuCodings/NanoJev) (about 2.5k), Clef, [kev](https://github.com/jaredpalmer/kev), [Jeeves](https://github.com/PostHog/jeeves) (reasoning plus decisions) |
| Trading bots | [jev-trader](https://github.com/jarrodwatts/jev-trader) (about 2.8k), [finance survey](https://gist.github.com/drillan/6916b16e8ea31a8ec36c8f59d6483150) |
| Data-system predicates | [pg-jev](https://github.com/realZachi/pg-jev), [vgi-typesafe (DuckDB)](https://github.com/Query-farm/vgi-typesafe), MySQL `AILIKE` ([awesome list](https://github.com/AbdelStark/awesome-typesafe-jev)) |
| Games and demos | [Jev Plays Pokémon Red](https://news.ycombinator.com/item?id=49845172), [clash-jev](https://github.com/bytelabs-oss/clash-jev) |
| Awesome-lists | more than 20 competing lists, e.g. [yibie/awesome-jev](https://github.com/yibie/awesome-jev) (about 2.1k stars) |

Signals that go beyond the projects themselves:
- **Vercel adoption.** InfoQ reports Jev reached "nearly 13% of paid teams within 24 hours" on Vercel ([InfoQ](https://www.infoq.com/news/2026/10/typesafe-ai-jev-released/), not verified).
- **OpenAI's answer.** OpenAI announced a Decision API built on Luna ([The New Stack](https://thenewstack.io/openai-decision-api-luna/), [HN](https://news.ycombinator.com/item?id=49896979)).
- **Cloudflare's copy.** Cloudflare deliberately copied the API with Clef ([blog](https://blog.cloudflare.com/clef-decision-models/)).
- **A de facto wire format.** "System One API" is turning into a shared protocol several vendors serve ([Zen](https://opencode.ai/docs/zen/), [Clef](https://blog.cloudflare.com/clef-decision-models/)).

### Loudest criticisms

| Criticism | Where |
|---|---|
| "Can't hallucinate" is too strong: Jev can return a confident, valid, wrong value | [HN launch thread, 1,989 points](https://news.ycombinator.com/item?id=49717558); [InfoQ](https://www.infoq.com/news/2026/10/typesafe-ai-jev-released/) |
| "70–500 ms vs 3–329 s" compares unlike work; RLCD has no paper behind it | [HN launch thread](https://news.ycombinator.com/item?id=49717558) |
| Calling it a "frontier model" oversells a strong zero-shot classifier; the naming is confusing | HN launch thread; [eesel review](https://www.eesel.ai/blog/typesafe-jev-review) (not verified) |
| No weights and no paper; prior open work went uncredited | [Towards Deep Learning](https://www.towardsdeeplearning.com/typesafe-spent-two-years-building-jev-in-secret-open-source-cloned-it-in-4-days-6020238ae08f); [arcturus-labs, "OpenAI is well positioned to fast-follow"](https://arcturus-labs.com/blog/2026/09/21/will-openai-eat-jevs-lunch/) |
| A new vendor that receives your data | discussed on [HN](https://news.ycombinator.com/item?id=49846907) |

### Open problems

These come from TypeSafe's own docs and independent studies:
- **Abstention and forced choice.** Jev abstained on 95% of ambiguous KoBBQ items when "unknown" was offered, and made errors once the gold label was removed ([awesome-typesafe-jev](https://github.com/AbdelStark/awesome-typesafe-jev), not verified individually).
- **Unstable limits.** Rate limits are unstable ([models](https://docs.typesafe.ai/models.md)).
- **Weak non-English accuracy** ([models](https://docs.typesafe.ai/models.md)).
- **Prompt injection.** State can be steered by text written into it ([jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md)).
- **First-option bias** ([jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md)).
- **Alpha OpenRouter surface.** OpenRouter's Decisions endpoint is still `alpha` (earlier report).
- **Recorded non-adoptions.** At least one public "evaluated, not adopted" write-up exists ([oboete #303](https://github.com/ojungo69/oboete/issues/303), not read in full).

## 6. Our stack today, from our records

| Part | What the records show | Record |
|---|---|---|
| Claude Code | public-part seat (the Claude/Codex pair); generated `.claude/` tree | `CLAUDE.md` (private-part charter); `.claude/` |
| Codex | public-part seat; generated `.codex/` tree | `CLAUDE.md`; `.codex/` |
| pi | generated `.pi/` agents tree | `.pi/agents/` |
| OpenCode on a local model | OpenCode 1.18.16 deployed to Ouranos on 2026-10-03, "local model service active"; server password held in sops for Prometheus and Ouranos | `flows/28d847/log.md`; `flows/b7da5d/log.md` |
| Herdr | Herdr 0.8.2 server with `default` and `messaging-build` sessions (census 2026-09-24); flows bind to Herdr at startup | `flows/752e0f/receipts/census-2026-09-24.md`; `flows/098f27/log.md` |
| messenger-clj | Clojure messenger, a working proof of concept for send and register (10 tests, 40 assertions, 2026-09-25); flows use its `hm-*` commands | `flows/38de5b/log.md`; skill `compensation-messenger-clj` |
| Nexuses | Orchestrate 0.37, Flow 0.23, Message 0.19, Lojix 8.1 running, with stable sockets — attributed Field evidence, receipt not yet available | skill `knowledge-nexus` |
| Jev itself | not installed. Root has an unpublished custom judge; the OpenRouter key was missing or inaccessible in gopass. A Rust-reuse check was ordered after the living's correction | `flows/d66c26/reports/jev-reuse-book-evidence.md`; `flows/d66c26/log.md` |
| Provider plan | proposed, not witnessed running: OpenRouter as the "public open-weight and Jev door", a Prometheus llama.cpp router as the private door, and a "decision tier: Jev" | `flows/752e0f/reports/model-providers-2026-09-24.md` |

Where a typed-decision model would slot in, only as the living has said it (no design here):

| Place | His words, in short | Record |
|---|---|---|
| Reaping / retired responses | "this is where we're going to start using JEV … statistical decisions with data" (2026-09-19) | `flows/b81560/vision/operational-retiredResponseAndReaping.md` |
| Monitor flow (Field) | "what would be really good for this is Jev" (2026-09-25); Monitor runs "Luna at light effort, later Jev" | `flows/e51411/notion/v2.md`; `flows/38de5b/reports/specialties-distillation.md` |
| Power tier | "Maybe Jev redefines what is actually ultra-low power" (2026-09-24) | `flows/752e0f/vision/models.md` |
| Ethos/datom bridge | translate our language to JSON for Jev; future models trained on datom (2026-09-26) | `flows/93ba9f/vision/jev.md` |
| CLIs taking datom payloads | "JEV validates this approach" | `flows/b81560/vision/operational-flowDatomCLIAndSignalLibrary.md` |
| Typed communication through Nexus | "putting [Jev] in the middle of that" | `flows/bad807/notion/voices.md` |
| Chained decisions | Jev to "make decisions, or to guide decisions, or to give data" for a further Jev call (2026-10-04) | `flows/bad807/vision/jev.md` |

Public projects already sit at three of these seams:
- harness routing for Herdr ([jev-herdr](https://github.com/alexzfe/jev-herdr));
- Codex and OpenCode routing (§3);
- pi auto-approval (§3).

A dated note: [firelex/jeff](https://github.com/firelex/jeff), a Jev-compatible model named "Jeff", was posted on 2026-09-28. That is two days after the living's 2026-09-26 "Jeff [sic]", so it cannot be what he meant on that day.

## Sources

- TypeSafe docs: [index](https://docs.typesafe.ai/llms.txt), [api](https://docs.typesafe.ai/api.md), [models](https://docs.typesafe.ai/models.md), [primitives](https://docs.typesafe.ai/primitives.md), [jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md), [coding agents](https://docs.typesafe.ai/introduction/coding-agents.md), [agent skill](https://docs.typesafe.ai/agent-skill.md); GitHub org [typesafe-ai](https://github.com/typesafe-ai).
- Registries, read through their public APIs on 2026-10-04: [crates.io](https://crates.io/search?q=jev), [npm](https://www.npmjs.com/search?q=jev), [PyPI](https://pypi.org/project/typesafe-sdk/), [Hugging Face](https://huggingface.co/models?search=jev), GitHub search through `gh`, and [HN Algolia](https://hn.algolia.com/?q=jev).
- Gateways and frameworks: [OpenCode Zen](https://opencode.ai/docs/zen/), [Vercel](https://vercel.com/i/jev-integrations), [AI SDK provider](https://ai-sdk.dev/providers/ai-sdk-providers/typesafe-ai), [LangChain provider](https://docs.langchain.com/oss/python/integrations/providers/typesafe), [Cloudflare Clef](https://blog.cloudflare.com/clef-decision-models/).
- Press and analysis: [InfoQ](https://www.infoq.com/news/2026/10/typesafe-ai-jev-released/), [flaviocopes](https://flaviocopes.com/jev/), [jev-ai.org](https://jev-ai.org/blog/jev-github/), [awesome-typesafe-jev](https://github.com/AbdelStark/awesome-typesafe-jev), [awesome-jev-use-cases](https://github.com/walidboulanouar/awesome-jev-use-cases).
- Our records: as named in §6, plus the two prior reports named at the top.
- Provenance receipt: unavailable. No PROVENANCE handoff was received for this report.
