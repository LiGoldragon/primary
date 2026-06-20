# Agentic browser control tools and cost-efficient models

Date: 2026-06-20

## Short recommendation for our Zeus/Bird setup

For local/browser-profile control, keep the **dedicated Chrome CDP profile** and use **browser-use** as the self-hosted agent loop. It fits the current deployment because it connects to a normal Chrome DevTools endpoint, supports many providers, and can run with our packaged `browser-agent-chrome` profile.

Model routing should be tiered:

1. **Default cheap trial model:** `gemini-2.5-flash` or `gemini-3-flash-preview` for low-stakes navigation, simple extraction, and smoke tests.
2. **Default reliable model:** keep **OpenAI `gpt-4.1`** only because it has already passed our live browser-use smoke test here; reassess against current Claude/Gemini models when keys are available.
3. **Best value if switching providers:** **Claude Sonnet** class is consistently a better standalone browser-agent value than Opus/Fable, while much more reliable than the cheapest Flash-class models.
4. **Best pure browser-agent product if cloud is acceptable:** Browser Use Cloud / `ChatBrowserUse` style models, because the benchmark claims fewer steps and lower total task cost even when the model call itself is not the cheapest.
5. **Do not assume local small Gemma works for production browser control yet:** it was not actually benchmarked before this report. The first attempted smoke test was interrupted after revealing a Chrome profile mismatch, not a Gemma capability result.

## What people use

### Browser-control frameworks

| Tool | How it controls the browser | Best use | Cost shape | Notes |
|---|---|---|---|---|
| **browser-use** | Python agent loop over Playwright/CDP; LLM observes page state, picks actions, repeats | General agentic web tasks, local Chrome/CDP, quick integration | Your browser infra + model tokens, or Browser Use Cloud | Docs say it supports 15+ providers and `ChatBrowserUse`; `ChatBrowserUse` is priced at $0.60/M input, $0.06/M cached, $3.50/M output and claims 3-5x faster task completion. |
| **Stagehand / Browserbase** | Playwright plus natural-language `act`, `extract`, and agent primitives; often runs on Browserbase cloud browsers | TypeScript/Playwright teams, repeatable automations with AI only where needed | Browserbase session costs + model gateway or own model | Docs show `Stagehand` using Browserbase Model Gateway and `google/gemini-3-flash-preview`; useful when you want deterministic Playwright around fuzzy steps. |
| **Skyvern** | Visual browser automation platform with planner/agent/validator concepts | Form filling, portals, invoices, layout-shifting sites | Cloud product or self-host + model keys | Docs emphasize real browser, visual page analysis, API/SDK, dashboard, and self-hosting. |
| **Plain Playwright/Puppeteer/Selenium + LLM** | Deterministic automation with LLM only for extraction/planning | Stable sites, cheap at scale | Lowest runtime cost when selectors are stable | Most cost-efficient if pages are stable; highest maintenance on changing UIs. |
| **Playwright MCP / browser MCP servers** | Expose browser actions as tools to an agent host | Agent IDEs and general assistants | Depends on host model | Good for interactive assistants; less specialized than browser-use/Stagehand/Skyvern. |
| **Managed computer-use agents** | Provider-hosted screen/browser environment | Full desktop/browser tasks with less setup | Token + runtime/session pricing | Anthropic documents computer-use token overhead and managed-agent session runtime; useful but less aligned with reusing Bird’s local browser profile. |

Sources: Browser Use supported-model docs; Browser Use model benchmark; Browserbase Stagehand quickstart; Skyvern docs; Anthropic pricing docs.

## Model comparison for browser agents

Browser agents are not normal chat. Total cost is driven by: page-observation tokens, screenshots/vision if enabled, tool schemas, retries, and number of browser steps. A model that is 3x pricier per token can be cheaper per completed task if it needs half the steps and fails less.

| Model family | Published price signal | Browser-agent quality signal | Practical judgment |
|---|---:|---|---|
| **Browser Use Cloud / `bu-ultra`** | Product/model pricing, not directly comparable to raw LLM tokens | Browser Use reports 78% on BU Bench and fastest throughput | Best if cloud/browser infra is acceptable; not ideal if we require Bird’s local profile. |
| **ChatBrowserUse / `bu-2-0`** | $0.60/M input, $0.06/M cached, $3.50/M output | Browser Use says optimized for browser automation and 3-5x faster; benchmark lists ChatBrowserUse-2 at 63.3% | Strong candidate for self-hosted browser-use if we can use Browser Use’s cloud LLM while keeping our local browser. |
| **Claude Fable / Opus** | Fable $10/M input, $50/M output; Opus $5/M input, $25/M output | Browser Use benchmark: Fable 80%, Opus 62% | Highest reliability, poor cost efficiency except high-value tasks. |
| **Claude Sonnet** | $3/M input, $15/M output; cache hits $0.30/M | Browser Use benchmark: Sonnet 59%; strong tool/code behavior | Best expensive-but-sane standalone model for production browser tasks. |
| **Claude Haiku** | $1/M input, $5/M output; cache hits $0.10/M | No strong browser-use benchmark in the fetched Browser Use table | Good cheap fallback for extraction/classification; should be tested before navigation tasks. |
| **Gemini 3 Flash Preview** | $0.50/M input, $3/M output; batch/flex $0.25/M input, $1.50/M output | Stagehand quickstart uses it by default in example | Likely best cheap modern default to test now, especially where vision/context matter. |
| **Gemini 2.5 Flash** | $0.30/M input, $2.50/M output; batch/flex $0.15/M input, $1.25/M output | Browser Use benchmark lists 35.2%, much lower than pro/Sonnet | Very cheap; use for low-stakes tasks and retry/escalate on failure. |
| **Gemini Flash-Lite** | 2.5 Flash-Lite $0.10/M input, $0.40/M output; 3.1 Flash-Lite $0.25/M input, $1.50/M output | Marketed by Google as cost-efficient/high-volume; no strong browser benchmark here | Cheapest plausible model; likely too weak for complex navigation, useful for page summarization/extraction. |
| **OpenAI GPT-4.1** | Current official pricing was not directly recovered; third-party listings put nano at $0.10/$0.40 and older 4o-mini at $0.15/$0.60 | In our environment, `gpt-4.1` passed browser-use smoke test; Browser Use current benchmark says newer GPT-5 family trails Claude/Gemini on browser tasks | Keep as known-good for now; do not assume OpenAI is best without a fresh benchmark. |
| **DeepSeek V4 Flash** | $0.14/M cache-miss input, $0.0028/M cache-hit input, $0.28/M output | Supports tool calls and 1M context; little browser-agent evidence | Extremely cheap; worth testing only if action-schema reliability is good. |
| **Local small models, e.g. Gemma** | Hardware cost only | Not yet measured; first smoke attempt exposed a profile mismatch before completion | Not recommended until a local benchmark proves success. |

## Cost-efficiency ranking

For **real browser tasks**, I would rank by expected completed-task cost, not token price:

1. **Deterministic Playwright/Selenium with tiny LLM extraction** when target sites are stable.
2. **Browser-use + ChatBrowserUse** if we can use its browser-specialized model with our local browser.
3. **Stagehand + Gemini 3 Flash Preview** when we want Playwright structure plus cheap fuzzy actions.
4. **browser-use + Gemini 2.5/3 Flash** for low-stakes browser tasks with retry/escalation.
5. **browser-use + Claude Sonnet** for important workflows that need reliable reasoning and custom extraction.
6. **Skyvern** for brittle visual portal workflows where maintaining selectors is more expensive than model/runtime cost.
7. **Claude Opus/Fable** only for expensive, hard, high-value tasks.
8. **DeepSeek/local small models** only after proving they emit valid actions and recover from web UI surprises.

## Suggested benchmark for Zeus/Bird

Use the existing dedicated CDP endpoint and run the same fixed suite against candidate models:

- Smoke: open `example.com`, return the heading.
- Search: find a public page and report a visible fact.
- Form: fill a non-submitting local test form.
- Multi-step: navigate docs and extract a version/string.
- Recovery: handle a page with delayed loading or a modal.

Measure:

- success/failure,
- number of steps,
- wall time,
- input/output tokens,
- total API cost,
- whether it opened extra tabs/windows,
- whether it reused the existing automation profile.

For our immediate setup, test in this order: local `gemma-4-26b-a4b` against the correct persistent profile, `gpt-4.1` known-good baseline, `gemini-3-flash-preview`, `gemini-2.5-flash`, `claude-haiku`, `claude-sonnet`, `ChatBrowserUse`, then `deepseek-v4-flash`.

## Source notes

- Browser Use docs: supports 15+ providers including Browser Use Cloud, OpenAI, Anthropic, Google Gemini, Groq, Ollama, Qwen, DeepSeek, Mistral, LiteLLM, OpenRouter; `ChatBrowserUse` pricing is $0.60/M input, $0.06/M cached, $3.50/M output.
- Browser Use benchmark post: BU Bench reports `claude-fable-5` 80%, Browser Use Cloud `bu-ultra` 78%, ChatBrowserUse-2 63.3%, Claude Opus 62%, Gemini 3.1 Pro 59.3%, Claude Sonnet 59%, GPT-5 52.4%, GPT-5-mini 37%, Gemini 2.5 Flash 35.2%.
- Browserbase Stagehand docs: Stagehand combines prompting with Playwright primitives and examples use `google/gemini-3-flash-preview` through Browserbase Model Gateway.
- Skyvern docs: describes English-task browser automation with visual page reading, API/SDK, dashboard, and self-host deployment.
- Anthropic pricing docs: Fable $10/$50, Opus 4.6+ $5/$25, Sonnet 4.5/4.6 $3/$15, Haiku 4.5 $1/$5 per MTok; prompt cache reads are 0.1x base input.
- Google Gemini pricing docs: Gemini 2.5 Flash $0.30/$2.50, 2.5 Flash-Lite $0.10/$0.40, 3 Flash Preview $0.50/$3.00, 3.1 Pro Preview $2/$12 per 1M tokens for standard paid tier.
- DeepSeek pricing docs: DeepSeek V4 Flash cache miss $0.14/M input, cache hit $0.0028/M input, $0.28/M output; V4 Pro $0.435/M input cache miss, $0.87/M output.
- OpenAI pricing page fetched here clearly listed current GPT-5.4 and GPT-5.5 prices but did not expose a clean official table for GPT-4.1 in fetched text. Treat GPT-4.1 as our empirical known-good rather than a cost benchmark until checked against the platform docs/API billing page.
