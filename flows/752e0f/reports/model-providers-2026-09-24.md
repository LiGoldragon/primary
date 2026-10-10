# Model providers, uncensored models, and the best stack — 2026-09-24

Research subflow for Psyche High 752e0f, answering the living's question of 2026-09-24 (`vision/models.md`): *"Or is OpenRouter the best to get what we want? Also would they have the jailbroken or uncensored versions of the open-weight models? Which stack is the best from a user's perspective, from a programmer's perspective, from our perspective?"*

Evidence grades: **(a)** primary page fetched today; **(b)** search-result snippet or third-party write-up, not opened; **(c)** this subflow's inference. Local records are cited by path. No provider account was opened, no model was called, nothing was installed.

## Recommendation (one page)

**"Jev" is Jev, from TypeSafe AI.** It is a closed model released 2026-09-15. It is not a chat model: you give it application state and typed questions (*Choice*, *Score*, *Noul*), and it returns typed decisions with probabilities in about 70–500 ms. It costs $0.042 per million input tokens, and output is free (a, Wikipedia; b, The Register). OpenRouter serves it with no waitlist as `typesafe/jev-1.13` through a separate Decisions API (`POST /api/alpha/decisions`), not through chat completions (a, OpenRouter Jev guide). This matches the living's own earlier words: "JEV, the new model that essentially deals with these statistical decisions with data" (`flows/b81560/vision/operational-retiredResponseAndReaping.md`, 2026-09-19). It also explains "so we should get OpenRouter": OpenRouter is the open door to Jev. (c) So Jev defines a new **decision tier** below "ultra-low". It does not replace a text tier, and because it is closed it cannot serve the private layer.

**Question 1: Is OpenRouter the best way to get what we want?** It is the best **single door to hosted models**. It has 500+ models on 80+ providers (b), including Kimi K3 on 17 providers, GLM 5.3, DeepSeek V4.x, Qwen, Hermes 4, Venice Uncensored, Jev, Claude, and GPT. It uses one key and one bill, and it offers OpenAI-compatible, Anthropic-compatible, and Responses API shapes. It is **not** the best for three jobs:
- **The Claude seat and the Codex seat.** Keep these on their own subscriptions. OpenRouter guarantees Claude Code only with Anthropic's own first-party provider (a), and it bills credits, not the subscription.
- **The private layer.** Anything sent to OpenRouter leaves the cluster, whatever the ZDR setting.
- **The cheapest steady bulk use.** The 5.5% card fee applies. BYOK has no fee up to $25k a month (b).

**Question 2: Does it have jailbroken or uncensored versions?** Only a few, and they are small or older models. On OpenRouter:
- **Venice Uncensored** (Dolphin Mistral 24B; no longer free since 2026-07-21)
- **Hermes 4 70B and 405B** (Llama 3.1 base, "neutrally aligned", low refusal)
- **Venice as a provider** for 36 models. These are Venice's hosting of the stock weights, not abliterated versions (c).

Off OpenRouter, **Featherless** hosts 781 "uncensored" models, including Huihui-Qwen3.5-27B-abliterated and gemma-4-26B-A4B-it-uncensored. It says it does not log prompts, and it charges a flat $25/month or more. **Venice's own API** is another hosted option. I found **no hosted abliterated version of a current frontier open model** (Kimi K3, GLM 5.3, DeepSeek V4). Only self-hosting runs *any* abliterated weights. Every hosted option also sends the prompt off the cluster, which the private-layer charter forbids.

**Question 3: Which stack is best?**
| Perspective | Best stack | Why | Cost of choosing it |
|---|---|---|---|
| **User** (the living: phone and workstation) | The existing Claude and ChatGPT subscriptions, plus **one OpenRouter account** for everything else, plus Prometheus reached over the tailnet | One extra account covers every hosted model and Jev. The phone reaches OpenRouter's web chat anywhere, and reaches Prometheus over the tailnet | Two bills instead of one. Local models are only as available as Prometheus |
| **Programmer** | **OpenRouter as the one API**, with the Prometheus llama.cpp router behind the same OpenAI-compatible shape | Tool calling, structured output, and streaming come in one shape. Codex CLI works through `model_providers` with `wire_api = "responses"`. Claude Code works through `ANTHROPIC_BASE_URL`. OpenCode works natively | Jev needs its own endpoint. Non-Anthropic models inside Claude Code are unsupported. Provider quirks leak through routing |
| **Ours** (private data never leaves the cluster, cost, every power tier) | **Three parts:** (1) Claude and Codex direct for the public seats; (2) OpenRouter with **ZDR enforced account-wide** for public open-weight models and Jev; (3) **Prometheus llama.cpp router** as the only private-layer backend and the local ultra-low tier | This is the only arrangement that meets the charter. Prometheus already serves 16 GGUF roots, gpt-oss-120b included, at about 31–34 tok/s on this hardware class. Ouranos can run a 1–8B tier | Local quality is capped at about 120B MoE; the frontier open models (K3 at 2.8T) do not fit. Three backends to operate |

**Overall:** a hybrid, with **OpenRouter as the public open-weight and Jev door, Prometheus as the private and local door, and the subscriptions staying as they are**. Put one OpenAI-compatible adapter in front of the OpenRouter and Prometheus parts, so that a flow picks a model by name and the privacy class picks the backend. For uncensored work: **self-host abliterated GGUFs on Prometheus** (for example Huihui-Qwen3.5-27B-abliterated, or an abliterated 120B-class MoE if one exists) rather than buy hosted uncensored models. That keeps the private layer's data on the cluster and matches the charter.

**Third-seat harness:** OpenCode (v1.18.30, 2026-09-09) is the strongest general choice. Pi is already packaged in Home. DeepSeek Harness is powerful but a developer preview. None of them matches Claude Code's hooks and permission model or Codex's sandbox (details in §4).

---

## 1. OpenRouter and its alternatives

### OpenRouter
- **Catalog:** "500+ active models on 80+ providers" as of 2026-09-23 (b, costgoat / deployhq aggregators; OpenRouter's homepage only says "hundreds of models", a). Kimi K3 is served by 17 providers at about $1.40 in / $10.75 out per million tokens, varying by provider (b). The models in §2 are also listed.
- **Pricing:** it passes through the provider's list price. The platform fee is 5.5% on card top-ups (5% crypto), with a $0.80 minimum. BYOK is free up to $25k of list-price inference a month, then 5% (changed August 2026). A September 2026 Business tier charges an 8% fee and locks routing to EU or US providers (b, aireiter, truefoundry).
- **API shapes:** OpenAI-compatible `/api/v1`. There is an "Anthropic Skin" at `/api` for Claude Code (a). Codex CLI works through a `model_providers` entry with `base_url = "https://openrouter.ai/api/v1"` and `wire_api = "responses"`, because Codex removed chat/completions in February 2026 (b, morphllm / OpenRouter blog). Jev uses a separate Decisions API and a System One API (a).
- **Claude Code caveat:** Claude Code with OpenRouter is "only guaranteed to work with the Anthropic first-party provider". Fast mode is served only by Anthropic first-party, and usage is billed as OpenRouter credits (a).
- **Rate limits:** `:free` models allow 20 requests/minute, and 50 requests/day, or 1,000 requests/day once $10 of credit has ever been bought. Paid models have no platform-level cap beyond the provider's own limits (b).
- **Privacy:** OpenRouter keeps no prompts by default unless you opt in to logging, but it keeps metadata such as timestamps, model, and token counts. You can enforce ZDR (routing only to providers that keep nothing) for the whole account, per model group, per key through guardrails, or per request with `provider.zdr: true`. Caveats: in-memory caching does not count as retention, some endpoints keep data for abuse monitoring, and plugins such as web search are exempt (a, ZDR guide). The Terms prohibit unlawful content and require you to comply with each upstream provider's terms. Uploaded files are screened for CSAM and malware (b, openrouter.ai/terms snippet).

### Alternatives for the same job
| Route | Strength | Weakness | Grade |
|---|---|---|---|
| Direct provider APIs (Moonshot, Z.ai, DeepSeek, TypeSafe) | No markup. Native features such as K3 `reasoning_content` and caching work first-hand | One account per vendor. TypeSafe's own API was in limited early access | b |
| Together AI | 200+ open models, fine-tune and serve under one API, OpenAI-compatible | Price close to Fireworks | b |
| Fireworks | Fast engine, strong structured output | Smaller catalog than an aggregator | b |
| Groq | Lowest latency: sub-100 ms TTFT, hundreds of tok/s | Curated catalog, no custom weights | b |
| DeepInfra | Usually cheapest per token; also a Hugging Face provider | Plain feature set | b |
| Hugging Face Inference Providers | OpenAI-compatible router at `router.huggingface.co/v1`, which picks the fastest provider (Together, Groq, Cerebras, SambaNova, Fireworks, DeepInfra and others) | Chat completion only, catalog tied to its providers | b |
| Featherless | Serverless access to more than 32,000 Hugging Face models, abliterated fine-tunes included, flat monthly fee, no prompt logging | Small and mid-size models only, 32k context on the Chat plan | a/b |
| **Self-host on Prometheus** | Private and free per token. Runs *any* open weights, abliterated ones included | Hardware-capped (see below) | c + local record |

**Prometheus as it stands:** the host is a GMKtec EVO-X2 with 128 GB of unified memory (`goldragon/cluster-definition.datom`, tagged `LargeAi`). That is AMD Strix Halo (`flows/024bc7/reports/thirdModel.md`). The 2026-09-16 disk witness shows `prometheus-llama-router.service` ("llama.cpp router — multi-model on-demand serving") active. It also shows 707 GB of GGUF roots: gpt-oss-120b, Nemotron-3-Super-120B-A12B, Qwen3.5-122B-A10B, DeepSeek-R1-Distill-Llama-70B, Qwen3.5-35B-A3B, Nemotron-3-Nano-30B-A3B, GLM-4.7-Flash, Qwen3.5-27B, Qwen3-8B, and Llama-3.2-1B (`flows/f55ec8/reports/prometheusDisk.md`). This is a 2026-09-16 record, not re-observed today. Published figures for this chip: gpt-oss-120b runs at about 31–34 tok/s, 30B-A3B MoE at 70–100 tok/s, and dense 70B at about 5 tok/s, against memory bandwidth of about 215 GB/s real (b, datahardware / localaimaster). (c) So MoE models up to about 120B are practical and dense 70B is not. Ouranos (ThinkPad T14 Gen5, 32 GB) can hold the 1–8B tier. vLLM on Strix Halo was not established in this pass; llama.cpp is what runs there.

## 2. Uncensored open-weight models — what is and is not hosted

**Hosted, found:**
- **OpenRouter → Venice Uncensored** (`cognitivecomputations/dolphin-mistral-24b-venice-edition`). This is Mistral-Small-24B tuned by dphn.ai with Venice; 128k context; Venice says a 2.2% refusal rate. It stopped being free on 2026-07-21 (b; the `:free` page returns 404 today, a).
- **OpenRouter → Hermes 4 70B / 405B** (Nous Research, Llama-3.1 base). "Neutrally aligned", it leads RefusalBench by Nous's own account (b).
- **OpenRouter → Venice as a provider** of 36 models, including DeepSeek V4.1 Flash, GLM 5.3, and GLM 5.3 Flash (b). (c) These are stock weights without Venice-added filters. The models' own trained refusals remain.
- **Venice API directly:** 363 models, with "uncensored" ones including Venice Uncensored, Llama 3.3 70B, and Qwen3 235B. It claims zero retention and TEE decryption (b).
- **Featherless:** 781 models under its "uncensored" filter, including Huihui-Qwen3.5-27B-abliterated (Feb 2026, Apache-2.0), gemma-4-26B-A4B-it-uncensored (Apr 2026), Huihui-Mistral-Small-3.2-24B-abliterated, Huihui-Qwen3.5-9B-abliterated, and Huihui-Qwen3-4B-abliterated. It states "Featherless does not log chats, prompts, or completions" (a, Featherless blog 2026-07-24). The Terms excerpts found restrict under-13 use and rate-limit abuse; no content clause surfaced in the snippet (b). The full Terms were not read.

**Not found hosted:** abliterated or uncensored versions of Kimi K3, GLM 5.3, DeepSeek V4.x, Qwen3.8 flagship, or any other model above about 70B, apart from Hermes 4 405B, a 2025 model.

**Self-hosting:** llama.cpp on Prometheus can serve any abliterated GGUF published on Hugging Face, within the memory limit above. This is the only way to be both uncensored and private.

**Terms:** OpenRouter passes through each provider's terms and bars unlawful content (b). "Uncensored" on a hosted service still means the provider sees the prompt, so (c) hosted uncensored models do **not** satisfy the private-layer charter ("served only through the open-source model", `CLAUDE.md`).

## 3. Stack by perspective — details behind the table

- **User:** Latency: Claude and Codex direct are unchanged. OpenRouter adds a small routing hop, and Groq via OpenRouter or Hugging Face gives the fastest open-model answers (b). On reliability, OpenRouter's fallbacks across providers help open models, and Jev's latency is 70–500 ms (a). The living keeps one extra account. Remote access to Prometheus's router is by tailnet, since Prometheus is tagged `TailnetClient` (local record); `reports/remote-access-options.md` in this Flow covers the phone route.
- **Programmer:** One OpenAI-compatible shape covers OpenRouter, the Hugging Face router, Featherless, and llama.cpp's server, so tool calling, JSON-schema output, and streaming are uniform (c; OpenRouter a). Harness hooks:
  - Codex through `model_providers` in user-level `~/.codex/config.toml` only. It must be Responses-shaped (b), so llama.cpp needs a Responses-capable front or an OpenRouter-style shim. This is inference (c), not verified.
  - Claude Code through `ANTHROPIC_BASE_URL`, guaranteed only for Anthropic models (a).
  - OpenCode natively speaks OpenRouter and local providers (b).
  - Jev needs its own client (TypeSafe SDK with base URL `https://openrouter.ai/api`) (b).
- **Ours:**
  - *Private layer:* only Prometheus, and the router must never fall back to a hosted provider. That rule belongs in the adapter, not in a convention (c).
  - *Cost:* local tokens cost only power. OpenRouter adds a 5.5% fee, or BYOK is free to $25k a month. Jev costs almost nothing.
  - *Power tiers:*
    - high and medium: Claude, GPT-6 Sol, and hosted K3 or GLM 5.3.
    - low: GPT-6 Luna (OpenAI released Sol and Luna on 2026-09-22 with no GPT-6 Terra, which matches "Terra out until Terra 6", b, TechCrunch / The New Stack).
    - ultra-low local: Qwen3-8B or Llama-3.2-1B on Prometheus or Ouranos.
    - decision tier: Jev.

## 4. Open harnesses for a third seat

| Harness | Version / state | Runs local / OpenRouter | Lacks against Claude Code and Codex CLI | Grade |
|---|---|---|---|---|
| **OpenCode** (sst) | v1.18.30, 2026-09-09. About 202k stars, MIT | 75+ providers; Ollama, LM Studio, llama.cpp; build and plan agents, subagents with per-agent model and permissions, `opencode serve` (OpenAPI + SSE) | Weaker permission model. K3 `reasoning_content`/`tool_calls` round-trip unproven (`flows/34d94e/reports/thirdStackHarness.md`). Home excludes it from the launch check | b; local record |
| **DeepSeek Harness (dsh)** | Released 2026-08-13, about 203k stars, developer preview | Plugin everything; Claude, OpenAI, Bedrock, DeepSeek | Breaking changes promised. Web-UI-first. This repo already has a `deepseek-harness` skill | b; `flows/6cc91b/reports/harnessLandscape.md` |
| **Pi** (+ pi-subagents) | Already packaged in CriomOS-home | llama.cpp router, Ollama; lean 4-tool design suits small models | No built-in permission system, so it needs an external sandbox | b; local record |
| **Goose** | Agentic AI Foundation | Widest local runtimes (Ollama, LM Studio, vLLM, KServe…); 70+ MCP extensions | General-purpose rather than coding-focused | b |
| **Hermes Agent** (Nous) | Weekly tags (v2026.9.x), MIT | OpenRouter, Nous Portal, any compatible endpoint; memory and skills across sessions | No mid-turn steering protocol; Python | b; local record |
| **Aider** | 0.86.2 (Feb 2026) after a 6-month gap | Ollama; text edit formats cope with weak tool calling | Maintenance concern; no agent loop comparable to CC/Codex | b |
| **Codex CLI `--oss`** | Current Codex | Ollama or LM Studio; gpt-oss default; built-in sandbox | Responses API only; thin docs for non-OpenAI models | b |
| **Qwen Code, Kilo Code, Cline, OpenHands, mini-swe-agent** | — | Various | Narrower local docs (Qwen Code, Kilo); editor-bound (Cline); container quirks (OpenHands); minimal (mini-swe-agent) | b |

What all of them lack, measured against Claude Code and Codex (c, from the sources above):
- **Guardrails:** hooks and permission policy as mature as Claude Code's, and an OS sandbox like Codex's (only Codex `--oss` and mini-swe-agent document sandboxing).
- **Tool calling:** reliable tool calling with *local* models below about 30B. Every harness guide asks for a context of at least 64k and a model that handles tools.
- **Proven fit:** no witnessed round-trip for K3's reasoning-plus-tool-call turn shape.

The recommendation stands: OpenCode first, Pi as the packaged fallback. Nothing here was installed or tested.

## Sources

- Jev — https://en.wikipedia.org/wiki/Jev_(AI_model) (a, 2026-09-24); https://www.theregister.com/devops/2026/09/23/shut-up-and-calculate-jevs-new-ai-primitives-for-coders/5298431 (a, 2026-09-23); https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711 (b); https://openrouter.ai/docs/guides/community/jev (a); https://openrouter.ai/typesafe/jev-1.13 (b); https://you.com/resources/what-is-jev (b)
- OpenRouter — https://openrouter.ai/ (a); https://openrouter.ai/docs/guides/features/zdr (a); https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration (a); https://openrouter.ai/docs/api_reference/limits (b); https://openrouter.ai/terms (b); https://openrouter.ai/moonshotai/kimi-k3 (b); https://costgoat.com/pricing/openrouter (b, Sep 2026); https://aireiter.com/blog/openrouter-byok-fees-fallback-guide (b); https://www.truefoundry.com/blog/openrouter-pricing (b); https://openrouter.ai/docs/cookbook/coding-agents/codex-cli (b); https://www.morphllm.com/codex-provider-configuration (b)
- Uncensored — https://openrouter.ai/cognitivecomputations/dolphin-mistral-24b-venice-edition:free (404 today, a; content b); https://openrouter.ai/provider/venice (b); https://openrouter.ai/nousresearch/hermes-4-405b (b); https://hermes4.nousresearch.com/ (b); https://docs.venice.ai/models/overview (b); https://featherless.ai/blog/best-uncensored-ai-models-2026 (a, 2026-07-24); https://featherless.ai/models?training=abliterated (b); https://featherless.ai/terms (b)
- Alternatives — https://huggingface.co/docs/inference-providers/index (b); https://deepinfra.com/blog/huggingface-inference-provider (b); https://infrabase.ai/blog/ai-inference-api-providers-compared (b); https://machinelearningplus.com/gen-ai/inference-providers-benchmark/ (b); https://markaicode.com/alternatives/fireworks-ai-alternatives/ (b)
- Hardware — https://datahardware.ai/blog/strix-halo-tokens-per-second-2026 (b); https://localaimaster.com/blog/strix-halo-ai-max-395-guide (b); https://github.com/hogeheer499-commits/strix-halo-guide (a, tables not reached)
- OpenAI tiers — https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/ (b); https://thenewstack.io/openai-gpt-6-sol-luna-release/ (b)
- Harnesses — https://www.marktechpost.com/2026/09/18/best-open-source-agent-harnesses-for-local-llms-in-2026/ (a, 2026-09-18); https://opencode.ai/changelog and https://www.gradually.ai/en/changelogs/opencode/ (b); https://pinggy.io/blog/best_open_source_cli_coding_agents/ (b)
- Local records — `flows/752e0f/vision/models.md`; `flows/b81560/vision/operational-retiredResponseAndReaping.md`; `flows/b81560/vision/operational-flowDatomCLIAndSignalLibrary.md`; `flows/6cc91b/vision/thirdModel.md`; `flows/f55ec8/reports/prometheusDisk.md` (2026-09-16); `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom`; `flows/024bc7/reports/thirdModel.md`; `flows/34d94e/reports/thirdStackRecommendation.md`; `flows/34d94e/reports/thirdStackHarness.md`; `flows/6cc91b/reports/harnessLandscape.md`; `CLAUDE.md` (Private part)
