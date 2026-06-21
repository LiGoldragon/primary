# Browser-agent tooling comparison after local browser-use debugging

Date: 2026-06-20

## Bottom line

The new evidence does **not** support “browser-use is unmaintained or unpopular.” It is popular and active: the GitHub result found roughly 99k stars, 11k forks, 320 contributors, and a same-day push. Its own docs market it as a Python browser-automation library with tens of thousands of stars, local/self-host support, and many LLM integrations.

The evidence **does** support: browser-use is a risky fit as our durable local-browser control layer when the requirements are:

- persistent human Chrome profile,
- local OpenAI-compatible multimodal model,
- authenticated heavy single-page apps like X and DigitalOcean,
- privacy-sensitive visible sessions,
- predictable cleanup/cancellation.

It is a good prototype harness and benchmark harness. It is not yet trustworthy as the core abstraction for CriomOS browser control without patching and strict configuration.

## Our new local findings

### What worked

- `browser-agent-chrome` persistent profile migration worked.
- Local Gemma 4 through Prometheus successfully completed the trivial browser-use smoke test:
  - task: visit `example.com` and return heading,
  - result: `Example Domain`.
- After raising browser-use/Gemma timeouts, Gemma got substantially further on X:
  - recognized logged-in user,
  - selected the Following tab,
  - scrolled,
  - identified visible accounts/posts including `@toppraddd`, `@Steve_Yegge`, `@midjourney`, `@FardeemM`, and `@guinnesschen`.

### What failed

- Default browser-use `llm_timeout` killed local Gemma calls at about 75 seconds, while Prometheus logs showed realistic local multimodal calls taking 116–127 seconds.
- llama-server continued working after the browser-use client canceled, producing `http client error: Connection handling canceled`; with `--parallel 1`, retries queued behind stale work.
- Browser-use’s screenshot/watchdog path timed out on heavy pages:
  - `Clean screenshot timed out after 6 seconds`,
  - `ScreenshotWatchdog.on_ScreenshotEvent timed out after 15.0s`.
- Direct CDP screenshot capture against the same X tab was fast and healthy:
  - JPEG: ~0.20–0.24s,
  - PNG: ~0.29s.
- Therefore the screenshot problem is not Chrome/CDP itself; it is browser-use’s clean-screenshot/watchdog/event pipeline, or how it sequences browser state collection on heavy pages.
- Setting `use_vision=false` did not fully stop screenshot capture; browser-use still triggered `ScreenshotWatchdog`. This matches an upstream issue class: browser-use has open bug reports that screenshots can still be sent/used even when vision is disabled, and separate open reports around screenshot timeouts.

## What the upstream docs say

Browser-use docs expose the relevant knobs:

- `use_vision`: docs say false should never include screenshots and should exclude the screenshot tool.
- `llm_timeout`: docs list a timeout for LLM calls.
- Browser event timeouts are environment variables, including:
  - `TIMEOUT_ScreenshotEvent`, default 15s,
  - `TIMEOUT_BrowserStateRequestEvent`, default 30s,
  - `TIMEOUT_ScrollEvent`, default 8s.

Our runtime contradicted the simple reading of `use_vision=false`: screenshots still ran as part of browser state collection. That may be a bug, a judging/final-response path, or a browser-state path separate from the LLM screenshot tool.

## Tool comparison

| Tool | Popularity / maintenance signal | Architecture | Strengths | Weaknesses for us | Fit for CriomOS local browser |
|---|---|---|---|---|---|
| **browser-use** | Very high stars and active pushes; not unmaintained | Python autonomous agent loop over browser state/actions; supports many LLM providers | Quick to prototype; local/self-host friendly; model-flexible; can attach to CDP; strong community | Hidden agent-loop behavior; screenshot/watchdog fragility; cancellation/timeout mismatch with local models; `use_vision=false` not enough in practice; harder to make deterministic | Good prototype and model-eval harness; questionable durable core unless patched |
| **Playwright/CDP direct** | Mature browser automation ecosystem | Deterministic browser control; explicit CDP calls | Maximum control; screenshots work directly; easiest privacy/cancellation story; no hidden agent loop | We must build our own planner/extraction conventions; more engineering work | Best durable core for persistent local browser sessions |
| **Stagehand** | Popular, active Browserbase-backed project; ~20k+ stars in search result | Playwright/CDP + AI primitives: `act`, `extract`, `observe`, and optional agent | Designed to mix deterministic code with AI; better production philosophy; less all-or-nothing agent autonomy | TypeScript-first; Browserbase docs strongly recommend cloud browser infra; local persistent-profile path needs testing | Strong candidate if it can attach cleanly to our local Chrome/CDP profile |
| **Skyvern** | Active OSS/product; workflow/RPA orientation | Visual automation with planner/agent/validator; cloud or self-host | Better for visually-driven forms and portals; self-host exists; ops/workflow friendly | More platform-heavy; less obviously suited to “use my existing local Chrome profile”; vision dependence may be costly/slow locally | Candidate for portal workflows, not first choice for local personal browser profile |
| **Playwright MCP / browser MCP** | Increasingly common in IDE/agent tooling | Browser exposed as MCP tools | Good for interactive assistant workflows and visible control | Depends heavily on host model; less specialized; may still need screenshots | Useful integration layer, not necessarily the browser-control engine |

## Model/runtime implications

Local Gemma is not disqualified by these tests. The exact lesson is narrower:

- Local Gemma needs longer LLM timeouts than cloud defaults.
- Local Gemma should likely be prompted to produce shorter actions and summaries.
- Browser-use should cap output tokens for local models.
- Prometheus llama-server needs better cancellation behavior or the client must avoid cancel/retry storms.
- Browser-use retry behavior is dangerous when the model endpoint has one active slot.

The local model stack should be tested with direct Playwright/CDP extraction before blaming the model.

## Recommended architecture now

### Durable path

Build a small CriomOS browser-control layer around direct CDP/Playwright:

1. `browser-agent-chrome` owns the persistent automation Chrome profile and CDP port.
2. A deterministic collector reads DOM text, accessibility snapshots where available, and screenshots only when explicitly requested.
3. Local Gemma receives compact page summaries or selected screenshots, not browser-use’s full heavy browser state prompt.
4. Actions are explicit CDP/Playwright operations with bounded timeouts and clear logs.
5. The model server is called with:
   - timeout >= 240s for multimodal local Gemma,
   - max output cap,
   - no automatic retry while a previous slot is still active.

### Near-term browser-use use

Keep browser-use for:

- quick smoke tests,
- comparing models,
- low-stakes public sites,
- experiments where hidden behavior is acceptable.

Do not use browser-use as the main path for:

- authenticated heavy SPAs,
- billing/admin portals,
- private sessions where logs must be tightly controlled,
- tasks where stale server-side generations are unacceptable.

### Stagehand experiment

Stagehand deserves a focused test because its philosophy matches our post-debug conclusion: deterministic code plus AI where useful. Test whether Stagehand can:

- connect to an existing local Chrome CDP profile,
- run `extract` from X/DigitalOcean without cloud browser infra,
- use our OpenAI-compatible Prometheus endpoint,
- avoid hidden screenshots when asked to operate DOM-first.

If yes, Stagehand may be a better library-level dependency than browser-use. If no, direct CDP/Playwright remains the safer base.

## Immediate patches already made locally

In `/git/github.com/LiGoldragon/CriomOS-home/packages/browser-use/browser-use-local-driver.py`:

- added `BROWSER_USE_LLM_TIMEOUT_SECONDS`, defaulting to 240 seconds,
- passed that timeout to both `ChatOpenAI(timeout=...)` and `Agent(llm_timeout=...)`,
- set `step_timeout` to at least timeout + 60,
- added `BROWSER_USE_USE_VISION=false` support.

This improves the LLM-timeout failure but does not fix browser-use’s internal screenshot/watchdog behavior.

## Recommendation

Stop treating browser-use as the durable answer. Keep the packaging for experimentation, but shift the durable design to:

**local persistent Chrome + direct CDP/Playwright collector + local model planner/summarizer**.

Then evaluate Stagehand as an optional higher-level wrapper. If it behaves cleanly with our persistent profile and local model endpoint, use it for structured `act`/`extract`; otherwise own the small browser-control layer ourselves.

## Sources consulted

- Browser-use GitHub and docs: high adoption, active repository, Python open-source browser automation, model/provider flexibility.
- Browser-use parameter docs: `use_vision`, `llm_timeout`, `TIMEOUT_ScreenshotEvent`, `TIMEOUT_BrowserStateRequestEvent`, and related environment variables.
- Browser-use GitHub issues/search results: reports of screenshots being used despite `use_vision=false`; reports of screenshot timeouts.
- Stagehand docs: production-oriented browser automation that combines natural language actions with deterministic code via `act`, `extract`, `observe`, and `agent`.
- Browserbase Stagehand search results: active TypeScript project, Playwright/CDP-oriented, Browserbase-backed.
- Skyvern docs/search results: visual browser automation platform with self-host and cloud modes, planner/validator workflow orientation.
