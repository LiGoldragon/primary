# 568 — Open-weight reasoning models (mid-2026): the leaders and the pick for Spirit

designer, 2026-06-09. Question from the psyche: which open-weight model (with
API access cheaper than Claude/Codex) has the highest reasoning capacity?
Researched live (web, 2026-06-09) because the field turns over monthly and
training memory is two+ generations stale. Every load-bearing number is anchored
to the neutral [Artificial Analysis](https://artificialanalysis.ai/leaderboards/models)
(AA) Intelligence Index or an official model card; vendor self-reported scores
(notably GLM/Qwen near-perfect AIME/GPQA) are discounted as contested.

"Open-weight" here = weights downloadable under an open/source-available license,
not merely a cheap API.

## The bar to beat (frontier API pricing, per 1M tokens)

- Claude Opus 4.8 — $5 in / $25 out · Sonnet 4.6 — $3 / $15
- GPT-5.5 — $5 / $30 · GPT-5.5 Pro — $30 / $180

Every model below is 5–30× cheaper than these.

## The leaders (AA Intelligence Index, accessed 2026-06-09)

Frontier reference: Claude Opus 4.8 = **61**, GPT-5.5 = **60**, Gemini 3.1 Pro = 57.

| Rank | Model | Maker | AA Index | Cheapest API (in/out, $/1M) | License | Context | Params (total/active) |
|---|---|---|---|---|---|---|---|
| 1= | **Kimi K2.6** | Moonshot | 54 | 0.95 / 4.00 (Moonshot, Fireworks) | Modified MIT (commercial OK) | 256K | 1T / 32B MoE |
| 1= | **MiMo-V2.5-Pro** | Xiaomi | 54 | 0.435 / 0.87 (Xiaomi, OpenRouter) | **plain MIT** | 1M | 1.02T / 42B MoE |
| 3 | **DeepSeek V4 Pro (Max)** | DeepSeek | 52 | 0.435 / 0.87 (DeepSeek direct) | MIT | up to 1M | 1.6T / 49B MoE |
| 4 | GLM-5.1 (Reasoning) | Zhipu/Z.ai | 51 | 1.40 / 4.40 | MIT | 200K | 744B / 40B MoE |
| 5= | MiniMax-M2.7 | MiniMax | 50 | ~0.30/M class | open (verify HF tag) | long | ~10B active MoE |

All are dedicated reasoning ("thinking") models.

## Top three, verified detail

- **Kimi K2.6** — the most-verified individual benchmarks (official card): GPQA-Diamond
  90.5, AIME 2026 96.4, SWE-bench Verified 80.2, LiveCodeBench 89.6, HLE 34.7. Priciest
  of the group but still ~5–6× under Opus. Modified-MIT (a UI-attribution clause only
  kicks in above 100M MAU / $20M monthly revenue — one aggregator mislabels it
  non-commercial; the official card is authoritative).
- **DeepSeek V4 Pro (Max)** — co-equal, arguably the strongest *individually-verified*
  coding/math: SWE-bench Verified 80.6, LiveCodeBench 93.5, AIME 2025 93.5, GPQA 90.1,
  MMLU-Pro 87.5. Dirt cheap on DeepSeek-direct ($0.435/$0.87); third-party hosts
  (Together, Fireworks) charge 3–5×. MIT.
- **MiMo-V2.5-Pro** — co-leader on the composite, cleanest license (plain MIT, no
  clauses), 1M context, cheapest of the leaders. Caveat: its individual hard-benchmark
  breakdown is thinner than Kimi's/DeepSeek's, so its #1 rests mainly on the AA
  composite.

## Ranked answer

- **Highest reasoning:** a real tie — **Kimi K2.6 ≈ MiMo-V2.5-Pro (AA 54)**, with
  **DeepSeek V4 Pro (52)** effectively co-equal. Forced to pick one, **Kimi K2.6** is
  most defensible on *verified* numbers; **DeepSeek V4 Pro** wins on verified coding/math.
- **Best value:** **MiMo-V2.5-Pro** or **DeepSeek V4 Pro** (~$0.435/$0.87 at AA 52–54);
  **MiniMax-M2.7** is the cheapness floor (~$0.30/M at AA 50).
- **Gap to frontier:** ~11–12% behind on the composite (54 vs 61), but **within ~2–3%
  on GPQA-Diamond** (≈90.5 vs ~93) and **at parity on SWE-bench Verified** (~80). The
  frontier's remaining edge is in long-horizon/agentic and "omniscience" evals, not in
  classic math/science/coding reasoning — open weights have largely closed *that* gap.

## The judgment for Spirit specifically

Two things the raw ranking doesn't say but matter for our use:

1. **The cheap first-party API is fine — privacy does not gate this (`qoku`).** A
   hosted inference call is not the publication-leak the privacy-closed-by-default rule
   targets (that rule guards world-readable surfaces — public repos, public reports,
   chat), so routing Spirit's intent through DeepSeek / Moonshot / Xiaomi direct is
   acceptable. That *simplifies* the pick: use the best cheap first-party API (Kimi
   K2.6 or DeepSeek V4 Pro) — no self-host overhead, no Western-host premium.
   Self-hosting the open weights stays *optional* — worth it only for latency,
   independence, or if the psyche later decides a genuinely-sensitive slice should stay
   in-cluster (a deliberate call, not a default).
2. **This is a different tier from the local scout.** These are 1T-class MoE models —
   they do not run on the Gemma cluster node. The design splits cleanly: the **small
   local Gemma** stays the per-capture scout (cheap, frequent, on-box); one of these
   **heavy open-weight reasoners** (self-hosted or trusted-host) is the candidate for
   the occasional *tending/synthesis* pass and any hard agent-side reasoning — where
   the extra capability is worth the cost and the data stays in our trust boundary.

## Honesty flags

- Live-search June 2026; version numbers and scores move monthly and are partly
  vendor-influenced. AA Index is the neutral cross-check; treat single-vendor near-perfect
  scores as upper bounds.
- MiMo-V2.5-Pro and MiniMax-M2.7 have thinner individual-benchmark documentation than
  Kimi/DeepSeek — their rank leans on the AA composite.
- MiniMax-M2.7's exact license needs confirming on its HF card before commercial use.
- "Cheapest API" for DeepSeek/MiMo assumes first-party/OpenRouter; trusted Western hosts
  cost more (relevant only if you choose to avoid the first-party endpoint).
