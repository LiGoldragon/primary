# Spirit Guardian DeepSeek Pro / Flash Review

The psyche is considering, not deciding, whether the Guardian should move from
DeepSeek V4 Flash to DeepSeek V4 Pro. This report is design evidence only, not
intent capture.

## Current Spirit / Agent State

- Live services: `agent-daemon.service` and `spirit-daemon.service` are active.
- Live Spirit: `spirit Version` reports `0.9.5`.
- CriOMOS-home currently configures the agent provider in
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`:
  provider `deepseek`, endpoint `https://api.deepseek.com/v1`, default model
  `deepseek-v4-flash`, key source `(Gopass platform.deepseek.com/api-key)`.
- Spirit's Guardian configuration uses the agent socket, provider `deepseek`,
  model `deepseek-v4-flash`, a 120 second timeout, and no maximum-output cap.

The production switch from Flash to Pro is mechanically small at the deployed
configuration layer: change `defaultModel` and the Guardian model from
`deepseek-v4-flash` to `deepseek-v4-pro`, rebuild, activate.

The bigger question is whether the call path can express the model behavior we
actually want. Today `signal-agent` exposes `model`, `provider`,
`temperature_milli`, `maximum_output_tokens`, and `output_mode`. It does not
expose DeepSeek's thinking toggle or reasoning effort. The `agent` provider
request therefore sends `temperature` and optional `max_tokens`, but no typed
`thinking` / `reasoning_effort` fields.

## Official DeepSeek Facts

Official API docs list two current model identifiers:

- `deepseek-v4-flash`
- `deepseek-v4-pro`

Both support OpenAI-compatible chat completions, JSON output, tool calls, 1M
context, 384K maximum output, and thinking/non-thinking modes. DeepSeek says
`deepseek-chat` and `deepseek-reasoner` are compatibility names for V4 Flash and
will be retired on 2026-07-24 15:59 UTC.

DeepSeek's own model positioning:

- V4 Pro: 1.6T total parameters, 49B active; the "world-class reasoning" model.
- V4 Flash: 284B total, 13B active; faster and cheaper, with reasoning that
  DeepSeek says closely approaches Pro and simple agent tasks on par with Pro.

Current published prices per 1M tokens:

- Flash: input cache miss `$0.14`, output `$0.28`.
- Pro: input cache miss `$0.435`, output `$0.87`.

The Pro price is roughly 3.1x Flash on uncached input and output. For Guardian
traffic, cost is not the first-order concern, but latency and verdict quality
are.

Sources:

- DeepSeek model/pricing docs:
  `https://api-docs.deepseek.com/quick_start/pricing`
- DeepSeek V4 release:
  `https://api-docs.deepseek.com/news/news260424`
- DeepSeek thinking mode:
  `https://api-docs.deepseek.com/guides/thinking_mode`
- DeepSeek model list:
  `https://api-docs.deepseek.com/api/list-models`

## Designer Context Refreshed

The latest designer reports change the Guardian bar:

- `reports/designer/600-spirit-rebuild-executed.md` says the rebuilt corpus is
  live and Spirit `0.9.5` has the meta import path, but the ordinary Guardian
  remains the incremental admission gate.
- `reports/designer/601-guardian-effect-simulation.md` shows what a stronger
  Guardian would do: merge duplicate arrows, raise importance by repeated
  conviction, and split compound records.
- `reports/designer/602-guardian-modality-catch.md` identifies the central
  over-capture failure: agent turns `could` / `I feel like` / `not intent yet`
  into a confident record.
- `reports/designer/603-intent-capture-protocol.md` corrects 602: the Guardian
  remains binary. It does not rewrite certainty; it accepts or rejects. The
  submitting agent must argue the case with verbatim psyche evidence, and the
  Guardian judges the whole case across faithfulness, domain, certainty,
  importance, and cross-record operation soundness.

So the real model question is not only "Flash or Pro?" It is: can the model
reliably judge a verbatim-grounded argued case, return exactly one typed NOTA
verdict, and avoid over-capturing tentative language.

## Live Probe

I ran direct API comparisons using the existing gopass secret source, without
printing the key. Both models were called through the official
`/chat/completions` endpoint with:

- `thinking: enabled`
- `reasoning_effort: high`
- Guardian-like prompts
- no output-token cap

The first probe used a loose prompt and showed the expected semantic behavior
but poor exact NOTA shape. The second probe used a stricter Guardian-style
grammar and six cases: hedged non-intent, durable rule, compound record,
contradiction, duplicate, and privacy.

### Result Pattern

Semantics:

- Both models caught the explicit "not intent yet" case.
- Both models caught the daemon inline-NOTA contradiction.
- Both models caught the duplicate.
- Both models rejected the private Zero-privacy case, but Flash chose the
  better reason (`UnclearPrivacy`); Pro chose `Contradiction`.
- Both models failed the "durable rule" case because my probe prompt
  over-emphasized "specific action"; this is a prompt-test defect, not a model
  conclusion.
- The compound case was mixed: Flash rejected but used a weak reason; Pro
  accepted, which is a bad Guardian outcome for that scenario.

Output shape:

- Pro followed the exact parenthesized NOTA wrapper more often in this small
  probe.
- Flash often omitted the outer record parentheses, producing a response like
  `Reject (Contradiction [...])` instead of `(Reject (Contradiction [...]))`.
- Pro still produced malformed variants too, especially `(Reject Duplicate
  [...])` instead of `(Reject (Duplicate [...]))`.

Latency:

- Flash was generally faster, but not always. In the first four-case probe Pro
  was faster on the hedged case; in the stricter six-case probe Pro was usually
  slower.
- Pro often spent more reasoning tokens, but not always in a way that improved
  the verdict.

The current Spirit Guardian has a retry path for malformed verdicts, so the
outer-parentheses failure is not automatically fatal, but repeated malformed
output still costs another model call and increases fail-closed risk.

## Operator Read

I do not yet see enough evidence to say "switch Guardian to Pro now" as a
quality decision. Pro is officially the stronger reasoning model, and it did
better on exact output shape in the small probe. But it did not dominate Flash
on Guardian semantics: it accepted one compound case Flash rejected, and it
picked a weaker privacy rejection reason.

The current deployed Flash path is not flimsy. It already passed the real
Guardian live scenario suite in `reports/operator/363-spirit-guardian-live-scenario-suite-2026-06-11.md`:
sandbox Spirit store, real agent engine, gopass DeepSeek key, real
DeepSeek V4 Flash, typed signal frames, parsed NOTA verdicts. Report
`reports/operator/364-guardian-output-budget-optional-2026-06-11.md` then
confirmed the same path with no explicit output cap.

The more important gap is not Pro-vs-Flash. It is that the contract cannot
explicitly request DeepSeek reasoning behavior. Official docs say thinking mode
defaults to enabled, but relying on a provider default is the wrong shape for a
Guardian. The Agent contract should expose the reasoning mode/effort we want,
as typed data, and the provider should pass it through deliberately.

## Recommended Next Slice

1. Add typed reasoning controls to `signal-agent` and `agent`:
   `ThinkingMode` and `ReasoningEffort`, probably in `PromptOptions`.
   Keep them provider-generic enough to map onto OpenAI-compatible providers
   without naming DeepSeek in the ordinary contract.

2. Parameterize the live Guardian scenario suite over at least two models:
   `deepseek-v4-flash` and `deepseek-v4-pro`, both with explicit thinking
   enabled and high effort.

3. Extend the suite with designer 603 cases:
   overstatement from verbatim `could` / `I feel like` / `not intent yet`,
   argued justifications, duplicate merge pressure, compound split pressure,
   privacy, referent ambiguity, and exact NOTA verdict compliance including
   retry behavior.

4. Only then decide whether to switch production Guardian to Pro. If Pro wins
   on the actual suite, the deployment change is a CriOMOS-home model string
   update, not a Spirit rewrite.

## Bottom Line

DeepSeek V4 Pro is the official stronger thinking model, so it is the right
candidate if Spirit's Guardian needs more judgment. But the first live probes do
not prove it is a strictly better Guardian than Flash. The production-worthy
move is to make reasoning effort explicit in the agent contract, run the exact
Guardian suite against both models, and switch only if Pro wins on the real
admission cases.
