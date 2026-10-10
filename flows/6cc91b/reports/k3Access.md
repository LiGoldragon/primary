# Kimi K3 access, pricing, and uncensored options — 2026-09-14

Subflow of 6cc91b, answering the living's questions on `vision/thirdModel.md` (2026-09-14). Builds on Codex's prior evidence at `flows/34d94e/reports/thirdStackRecommendation.md`. All prices read 2026-09-14; grade in brackets: (a) primary page, (b) search snippet, (c) inference.

## 1. Hosted Kimi K3 access, ranked

Model: 2.8T-parameter MoE, 1,048,576-token context, native vision, released mid-July 2026.

| Provider | Input $/M | Output $/M | Cached input $/M | Context served | Notable claims | ZDR/retention | Region | OpenAI-compat | OpenCode entry |
|---|---|---|---|---|---|---|---|---|---|
| **Fireworks** | $3.00 | $15.00 | $0.30 | 1040k | Fast + Priority tiers; day-0 launch | **ZDR by default**; US-only endpoint option | US-hosted | yes | not directly named in search, but OpenRouter/models.dev route works |
| **DeepInfra** | $2.85 | $14.25 | $0.285 | 1M | "practical speed, predictable cost" marketing | not confirmed ZDR | not stated | yes | via OpenRouter/models.dev |
| **OpenRouter** (aggregator, 17 providers) | $2.10 | $10.95 | not exposed | varies by upstream | cheapest blended quote found; routes to Fireworks/DeepInfra/others | depends on routed provider | depends on routed provider | yes | **yes — this is OpenCode's documented default path** |
| **Together** | listed among Fireworks/Baseten as US-hosted partner (b); exact price not independently pulled this pass, reported at parity ~$3/$15 (b) | | | 1M (b) | US-hosted partner | not confirmed | US | yes | via OpenRouter/models.dev |
| **Baseten** | $3.00 | $15.00 | not published | 1M | US-hosted partner; no public rate card, quote-based | not confirmed | US | yes | via OpenRouter/models.dev |
| **Novita** | $3.00 | $15.00 | $0.30 | 1M | budget-positioned marketing | not confirmed | not stated | yes | via OpenRouter/models.dev |
| **SiliconFlow** | $3.00 | $15.00 | $0.30 | 1M | "first open 3T-class model at frontier performance" | not confirmed | China-based platform (c) | yes | via OpenRouter/models.dev |
| **Groq** | not offering Kimi K3 as of this pass (b) | | | | | | | | |
| **Moonshot direct** (platform.moonshot.ai / platform.kimi.ai) | $3.00 | $15.00 | $0.30 | 1M | official first-party rate; OpenCode's own onboarding default provider | **no self-serve opt-out**; prompts may train future models unless you request de-identified opt-out via support (b) | China (Moonshot) + Singapore subsidiary; National Intelligence Law exposure flagged by third-party privacy reviews (b/c) | yes | **yes — Moonshot publishes an official OpenCode integration guide** (a): https://platform.kimi.ai/docs/guide/open-code |
| **Featherless** | not pulled | | | 256K on serverless Developer plan; full 1M on dedicated tier only (b) | | not confirmed | | yes | not confirmed |
| **RunPod** | pay-per-second GPU rental, not per-token (b) | | | self-hosted, so full context if you configure it | sub-200ms cold starts advertised | you control it entirely — full privacy | your choice of GPU region | yes (OpenAI-compatible public endpoint) | not confirmed |

Everyone quoting a per-token rate converges near **$3.00 input / $15.00 output**, the number Moonshot itself set; nobody has yet undercut it structurally. The two real spreads are (1) **OpenRouter's blended $2.10/$10.95**, likely a promotional or specific-upstream-provider rate rather than a universal floor, and (2) **DeepInfra's $2.85/$14.25**, a modest but consistent ~5% discount off list. [OpenRouter](https://openrouter.ai/moonshotai/kimi-k3) (a/b), [DeepInfra blog](https://deepinfra.com/blog/kimi-k3-pricing-providers-cost) (b), [Novita blog](https://blogs.novita.ai/kimi-k3-on-novita-ai/) (b), [SiliconFlow blog](https://www.siliconflow.com/blog/kimi-k3-siliconflow-api) (b), [Fireworks model page](https://fireworks.ai/models/fireworks/kimi-k3) (a), [Fireworks AI on X](https://x.com/FireworksAI_HQ/status/2081764187827847654) (b), [Jamin Ball on X, Baseten/Fireworks parity](https://x.com/jaminball/status/2081829990015127743) (b), [Moonshot OpenCode guide](https://platform.kimi.ai/docs/guide/open-code) (a), [Kimi privacy policy analysis](https://gist.github.com/gadgetb0y/11931119946c2e9dcae0a438fdefe0d5) (b).

### Ranking on fast / reliable / affordable, privacy as tiebreak

1. **Fireworks** — same $3/$15 price as everyone, but the only provider in this pass documented with **US-hosted, zero-data-retention-by-default**, a Fast tier for latency and a Priority tier for reliability under load. This is the strongest fit for "fast, reliable, affordable" once privacy breaks the tie, since it costs nothing extra over the going rate to get ZDR. [Fireworks blog](https://fireworks.ai/blog/kimik3-on-fireworks) (a), [Fireworks AI on X](https://x.com/FireworksAI_HQ/status/2081891063162442106) (b).
2. **OpenRouter** — cheapest blended number found and it's what OpenCode's provider list treats as the aggregator path, giving automatic failover across 17 upstream providers (reliability via redundancy) — but you inherit whichever upstream provider's retention policy, unknown per-request unless pinned. Good default if the living wants "set it up now" simplicity; can be pinned to route only to Fireworks for the privacy property.
3. **Moonshot direct** — official OpenCode integration guide exists and is literally the harness's onboarding default, so it is the lowest-friction "just works" path, but its own privacy policy has no self-serve training opt-out and is jurisdictionally exposed (China + National Intelligence Law per third-party review, not Moonshot's own statement) — worst of the credible options on the privacy tiebreak. [Kimi privacy policy](https://www.kimi.com/user/agreement/userPrivacy?version=v2) (a).
4. **DeepInfra / Novita / SiliconFlow / Baseten / Together** — parity or near-parity pricing, no ZDR claim found in this pass for any of them; treat as backups or price-shop only if Fireworks has an outage.

**Recommendation for setup: Fireworks first (direct or via OpenRouter pinned to Fireworks), Moonshot direct as the documented fallback since it's what the integration guide targets.**

## 2. Uncensored / abliterated K3, and touchy-subject alternatives

**Real today:**
- **Kimi-K3-Abliterated-V1** (Uniboshi, HF) — abliteration technique removing refusal-direction activations across layers, reported **98.44%–98.62% of "safeguards" removed** by the uploader's own numbers. Same 2.8T parameter footprint as base K3 (F32/BF16/U8 + quantized GGUF variants for llama.cpp/Ollama/LM Studio). **Self-hosted only** — no commercial inference API lists it; three community demo Spaces exist but need your own compute. No independent quality-loss benchmark was found in this pass, only the uploader's safeguard-removal percentage — treat that number as a claim, not a verified benchmark (b/c). [Model card](https://huggingface.co/Uniboshi/Kimi-K3-Abliterated-V1) (a).
- Several smaller/competing abliterated repacks exist (Ryanchen911, audnai/penclaw, GrEarl, Blackfrost-AI) — same pattern, self-host only, unverified quality claims, differing quantizations. Not independently vetted here.
- Self-hosting K3 (censored or abliterated) is **cluster-scale**: prior evidence (`thirdStackRecommendation.md`) cites the published vLLM recipe needing ≥8×GB300 or 8×MI355X/MI350X. RunPod publishes a guide to run K3 on rented GPUs by the second rather than owning that hardware — the realistic self-host path is rented cluster time, not local hardware. [RunPod K3 FAQ](https://www.runpod.io/articles/guides/kimi-k3-technical-faq) (a/b).
- **License question**: Moonshot's Kimi K3 license permits download/modify/fine-tune/deploy commercially at no cost for ordinary use; restrictions only bite above $20M/12mo MaaS revenue or 100M MAU/$20M monthly revenue products (must display "Kimi K3" in the interface). Nothing in the reviewed terms forbids modifying the model or its system prompt to reduce refusals for internal/small-scale use — **abliteration and system-prompt jailbreaking both appear licensable for our scale**, though this is a reading of secondary summaries, not the license text itself pulled fresh this pass. [License summary via MoClaw](https://moclaw.ai/blog/kimi-k3-license) (b), prior evidence: [HF license](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE) (a, from `thirdStackRecommendation.md`).

**Real today, and arguably the better answer:**
- **DeepSeek V4.1 Flash** — released 2026-09-10, **MIT weights**, and within hours independent uncensored/abliterated builds appeared on HuggingFace (e.g. `dealginai/DeepSeek-V4.1-Flash-UNCENSORED-FP8`, one build logging 23,375 downloads). MIT means no revenue-threshold license friction at all, unlike K3. DeepSeek itself did not create or endorse these builds — they're third-party. This is the psyche's own prior candidate from the thirdStackRecommendation pass, now with a live uncensored ecosystem already forming. [DeepSeek uncensored coverage](https://pasqualepillitteri.it/en/news/16070/deepseek-41-flash-uncensored-abliterated-builds) (b), [HN thread](https://news.ycombinator.com/item?id=49654387) (b).
- **Hermes 4 / 4.3 (Nous Research)** — purpose-built for low refusal, not a post-hoc abliteration. Built on Llama 3.1 (14B/70B/405B); Hermes 4 leads RefusalBench at 57.1% reasoning-mode compliance (vs. GPT-4o 17.67%, Claude Sonnet 4 17%); Hermes 4.3 reportedly reaches 74.6%. Hosted on OpenRouter (`nousresearch/hermes-4-405b`) — this is a **hosted, API-reachable, purpose-designed low-refusal model today**, not a hobbyist abliteration. Smaller and less conceptually capable than K3/DeepSeek by parameter count and benchmark class, but real, hosted, and cheap. [Hermes 4 on OpenRouter](https://openrouter.ai/nousresearch/hermes-4-405b) (a), [VentureBeat](https://venturebeat.com/ai/nous-research-drops-hermes-4-ai-models-that-outperform-chatgpt-without-content-restrictions) (b).

**Not real today:** a hosted, commercially-served *uncensored K3* (no Featherless/DeepInfra/Together/RunPod-serverless listing found carrying the abliterated weights specifically — RunPod's offering is a template to self-deploy the abliterated GGUF on rented GPUs, not a managed serverless endpoint for it). Anyone claiming "just call an API for uncensored K3" is wrong as of this pass.

**Plain answer:** for a touchy-subject flow, three honest options exist — (1) rent GPU time and self-host the K3 abliteration (real, costly, cluster-scale, unverified quality loss), (2) use DeepSeek V4.1 Flash's emerging uncensored ecosystem (real, MIT, cheap once someone hosts it or you self-host a smaller footprint), or (3) call Hermes 4/4.3 today via OpenRouter (real, hosted now, cheapest to start, smaller model). No option gives K3-class conceptual capability *and* hosted-uncensored *and* cheap simultaneously today.

## 3. Recommended setup path (Fireworks-via-OpenRouter, top choice)

1. **[Living]** Create an OpenRouter account and add payment (or create a Fireworks account directly if pinning to Fireworks only) — either takes a card and an API key generation, minutes of work.
2. **[Living]** Decide retention posture: OpenRouter routed generally (simplest, inherits upstream policy) vs. pinned to Fireworks provider (guaranteed ZDR, still on OpenRouter's routing UI) vs. Moonshot direct (matches the official OpenCode guide exactly, weakest privacy).
3. **[Codex]** In OpenCode, run the documented auth flow for the chosen provider (`opencode auth login`, select OpenRouter or Moonshot AI from the models.dev-backed list) and paste in the API key the living generated.
4. **[Codex]** Configure the third-council-seat subagent in OpenCode's agent config to target `kimi-k3` (or the OpenRouter provider-pinned equivalent), with reasoning effort set explicitly per the prior evidence's recommendation (compare high vs. max on hard cases), and wire the bounded read/search/fetch tool set from `thirdStackRecommendation.md`'s proposed composition.
5. **[Codex]** Run the synthetic-fixture adapter test the prior report calls for — assistant-message replay with provider fields and tool calls intact — before sending any real local record through the new provider, then report back with the first live OpenCode call's result.

## Sources

- [OpenRouter Kimi K3](https://openrouter.ai/moonshotai/kimi-k3) (a/b)
- [Fireworks Kimi K3 model page](https://fireworks.ai/models/fireworks/kimi-k3) (a)
- [Fireworks blog: Kimi K3 on Fireworks](https://fireworks.ai/blog/kimik3-on-fireworks) (a)
- [Fireworks AI on X, ZDR/US-hosted](https://x.com/FireworksAI_HQ/status/2081764187827847654) (b)
- [Jamin Ball on X, Baseten/Fireworks pricing parity](https://x.com/jaminball/status/2081829990015127743) (b)
- [DeepInfra: Kimi K3 pricing, providers & real-world costs](https://deepinfra.com/blog/kimi-k3-pricing-providers-cost) (b)
- [Novita: Kimi K3 pricing](https://blogs.novita.ai/kimi-k3-on-novita-ai/) (b)
- [SiliconFlow: Kimi K3 on SiliconFlow](https://www.siliconflow.com/blog/kimi-k3-siliconflow-api) (b)
- [Moonshot: Use Kimi Models in OpenCode](https://platform.kimi.ai/docs/guide/open-code) (a)
- [Kimi privacy policy](https://www.kimi.com/user/agreement/userPrivacy?version=v2) (a)
- [Kimi privacy policy analysis (third-party)](https://gist.github.com/gadgetb0y/11931119946c2e9dcae0a438fdefe0d5) (b)
- [Uniboshi/Kimi-K3-Abliterated-V1](https://huggingface.co/Uniboshi/Kimi-K3-Abliterated-V1) (a)
- [RunPod: Kimi K3 technical FAQ / self-host breakeven](https://www.runpod.io/articles/guides/kimi-k3-technical-faq) (a/b)
- [Featherless: Kimi K3 is live](https://featherless.ai/blog/kimi-k3-is-live-on-featherless) (b)
- [MoClaw: Kimi K3 license summary](https://moclaw.ai/blog/kimi-k3-license) (b)
- [DeepSeek V4.1 Flash uncensored builds coverage](https://pasqualepillitteri.it/en/news/16070/deepseek-41-flash-uncensored-abliterated-builds) (b)
- [Hacker News thread on DeepSeek V4.1 Flash Uncensored](https://news.ycombinator.com/item?id=49654387) (b)
- [Hermes 4 405B on OpenRouter](https://openrouter.ai/nousresearch/hermes-4-405b) (a)
- [VentureBeat: Nous Research Hermes 4](https://venturebeat.com/ai/nous-research-drops-hermes-4-ai-models-that-outperform-chatgpt-without-content-restrictions) (b)
- Prior evidence: `flows/34d94e/reports/thirdStackRecommendation.md` (K3 license, vLLM hardware recipe, OpenCode agent docs, K3 API guide)
- `flows/6cc91b/vision/thirdModel.md` (the living's questions, verbatim, this pass)

All prices and claims read/checked 2026-09-14.
