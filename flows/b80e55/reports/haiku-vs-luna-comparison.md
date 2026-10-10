# Haiku 4.5 vs Luna (GPT-5.6) — behavioral comparison for ultra-low seats

Flow b80e55, subflow report, 2026-09-20.

## The specs we value

| Quality | Haiku 4.5 | Luna (GPT-5.6) |
|---------|-----------|-----------------|
| **Refusal calibration** | Refuses more than peers, hallucinates less when it does answer. "Knows-its-limits" archetype. | No documented selective refusal. Attempts answers more freely. |
| **Doubt / uncertainty** | Expresses uncertainty readily. Calibration-by-refusal: declines rather than guesses. | Low calibration evidence. The 92.6% hallucination rate on AA-Omniscience suggests confident wrong answers. |
| **"I don't know"** | Says it when warranted. Anthropic models are trained to abstain. | Rarely abstains. The hallucination rate implies it answers when it shouldn't. |
| **Abstract concepts** | Handles design/architecture reasoning at a basic level. Limited depth at this tier. | Similar basic capability. AA Intelligence Index 37 (above average for its tier). |
| **Complex instructions** | Strong instruction following for nuanced tasks. Tested in multi-model pipelines. | Supports tools, function calling, structured outputs. Instruction following untested at our skill complexity. |

## Hallucination rates (AA-Omniscience benchmark)

- **Haiku 4.5:** Not individually benchmarked, but Anthropic small models consistently under 10% hallucination.
- **Luna:** 92.6% hallucination rate, 42.7% accuracy — the highest hallucination of any flagship-family model measured.
- **For context:** GPT-5.4 Mini at 5.5%, GPT-5.5 at 9.3%, Opus 4.7 at 12.0%.

Luna's hallucination rate is an order of magnitude worse than comparable small models.

## Pricing

| | Input (per M tokens) | Output (per M tokens) | Ratio |
|---|---|---|---|
| **Haiku 4.5** | $1.00 | $5.00 | — |
| **Luna** | $0.20 | $1.20 | **5× cheaper input, 4× cheaper output** |

Luna wins on raw cost by a wide margin.

## Context window

| | Context | Max output |
|---|---|---|
| **Haiku 4.5** | 200K | 64K |
| **Luna** | 1,050K | 128K |

Luna has 5× the context and 2× the output. But Codex CLI caps effective input at ~272K.

## Harness overhead

| | Bootstrap tokens | With typical project |
|---|---|---|
| **Claude Code** | ~33K (tools + system reminders + skills) | 75–85K |
| **Codex CLI** | ~2–5K (system prompt, cached after first turn) | ~5–10K without MCP |

Codex is 7–15× leaner on bootstrap. On a 200K Haiku window, 33K is 16% gone
before the first prompt. On Luna's effective 272K, 5K is under 2%.

## The living's question: which is better for ultra-low?

**Luna wins on:** cost (4–5×), context (5×), harness efficiency (15×), output length (2×).

**Haiku wins on:** refusal calibration, honesty, doubt expression, "I don't know"
behavior, instruction following on complex structured protocols.

**The tension:** Luna is dramatically cheaper and roomier, but it hallucinates at
92.6% on knowledge benchmarks and does not abstain when uncertain. Haiku costs
more but knows its limits. For a psyche seat — where the valued behaviors are
doubt, refusal, and not answering when it doesn't know — Haiku's disposition
is closer to what we want. For a field or mind ultra-low seat doing mechanical
census work, Luna's cost and context advantage dominate.

**The living ruled Luna everywhere.** The harness cost argument is strong: at
33K bootstrap, Haiku's 200K window leaves only 167K of useful work versus
Luna's 267K effective. Luna gets 60% more working space for 80% less money.
The hallucination rate is a real cost — but for ultra-low seats doing bounded,
scripted work (census, GC, status checks), the tasks are narrow enough that
hallucination on open-ended knowledge questions rarely applies.
