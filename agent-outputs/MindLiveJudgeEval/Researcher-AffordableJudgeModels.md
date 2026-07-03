# Affordable Judge Models For Mind Accepted Knowledge

Task: research affordable high-reasoning model candidates for Mind's accepted-knowledge judge. Scope included local Mind live-eval evidence, prompt/config surfaces, and current external sources as of July 3, 2026. No code was implemented and no live provider/model calls were run.

## Sources And Local Evidence

Local files consulted:

- `/home/li/primary/agent-outputs/MindLiveJudgeEval/Researcher-JudgeTrainingRecommendations.md`
- `/home/li/primary/agent-outputs/MindLiveJudgeEval/RustAuditor-Review.md`
- `/home/li/primary/agent-outputs/MindLiveJudgeEval/GeneralCodeImplementer-JudgeHardeningEvidence.md`
- `/home/li/primary/agent-outputs/MindLiveJudgeEval/rust-prompt-v3-stateful/summary.json`
- `/home/li/primary/agent-outputs/MindLiveJudgeEval/rust-prompt-v3-isolated/summary.json`
- `/git/github.com/LiGoldragon/mind/src/knowledge-judge-prompts/accepted-knowledge.md`
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs`
- `/git/github.com/LiGoldragon/agent/src/provider.rs`
- `/git/github.com/LiGoldragon/agent/src/registry.rs`

Read-only commands included `spirit`, `ls`, `sed`, `rg`, `find`, `jq`, and `test`. Spirit `PublicTextSearch [Mind accepted knowledge judge model selection reasoning classification output cost]` returned public records emphasizing that deterministic classifications with derivable answers belong in mechanism, while agent work should be reserved for decisions code cannot make; that supports keeping exact duplicate handling deterministic and using the model only for semantic judgment.

External sources:

- DeepSeek official models/pricing: <https://api-docs.deepseek.com/quick_start/pricing>
- DeepSeek reasoning model guide: <https://api-docs.deepseek.com/guides/reasoning_model>
- Together GLM-5.2 model/pricing page: <https://www.together.ai/models/glm-52>
- Alibaba Cloud Model Studio model pricing and model catalog: <https://www.alibabacloud.com/help/en/model-studio/model-pricing>, <https://www.alibabacloud.com/help/en/model-studio/models>
- Kimi API platform docs and pricing landing page: <https://platform.kimi.ai/>, <https://platform.kimi.ai/docs/guide/kimi-k2-6-quickstart>, <https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart>
- MiniMax API docs: <https://platform.minimax.io/docs/api-reference/text-openai-api>, <https://platform.minimax.io/docs/guides/pricing-paygo>
- Mistral Small 4 announcement/pricing: <https://mistral.ai/news/mistral-small-4/>
- Mistral general pricing FAQ/model overview: <https://mistral.ai/pricing/>, <https://docs.mistral.ai/models/overview>
- xAI model docs: <https://docs.x.ai/developers/models>
- Google Gemini pricing and OpenAI compatibility docs: <https://ai.google.dev/gemini-api/docs/pricing>, <https://ai.google.dev/gemini-api/docs/openai>
- OpenAI pricing and structured outputs docs: <https://developers.openai.com/api/docs/pricing>, <https://developers.openai.com/api/docs/guides/structured-outputs>

## Local Baseline

DeepSeek Flash after prompt hardening is not promotable as final accepted-knowledge authority. The strongest local evidence is the v3 stateful and isolated runs:

- Stateful: verdict-class `112/132` (`84.85%`), identity-bearing `27/52` (`51.92%`), accepted-positive `22/27` (`81.48%`), paraphrase duplicate `2/14`, conflict `7/14`, false/unsupported `1/6`.
- Isolated: verdict-class `108/132` (`81.82%`), identity-bearing `27/52` (`51.92%`), accepted-positive `17/27` (`62.96%`), paraphrase duplicate `2/14`, conflict `6/14`, false/unsupported `1/6`.

The failures line up with model capability rather than missing prompt coverage: semantic paraphrase matching, minimal conflict identity selection, source-required versus false/unsupported taxonomy, wrong-subject overuse, and valid stable fact acceptance.

The current agent daemon is friendly to broad provider experiments. `agent/src/provider.rs` builds one OpenAI-compatible `/chat/completions` request, passes `temperature`, `max_tokens`, `reasoning_effort`, and a top-level `thinking` object when configured, asks for NOTA text, validates it, and retries once. Provider changes are mostly endpoint/model/secret-source configuration if the provider accepts this shape.

## Cost And Fit Table

Prices are per 1M tokens unless noted. Output price is the primary ranking axis because judge replies can include hidden/reasoning tokens on thinking models and because the user treats roughly `$0.87/M output` as the expensive edge of acceptable.

| Model / provider route | Output price | Input price | Context | API compatibility | Expected strengths / risks for Mind judge | Recommendation |
| --- | ---: | ---: | ---: | --- | --- | --- |
| DeepSeek `deepseek-v4-flash` direct | `$0.28`; cache-hit input `$0.0028` | `$0.14` cache miss | `1M`, max output `384K` | OpenAI-format base URL; JSON output/tool calls; thinking mode available | Cheap and already integrated, but local evidence shows weak paraphrase duplicate detection, conflict identity precision, false/unsupported taxonomy, and over-rejection. | Keep only as telemetry, draft, or reject-only screen. Do not use as final accepting authority. |
| DeepSeek `deepseek-v4-pro` direct | `$0.87`; cache-hit input `$0.003625` | `$0.435` cache miss | `1M`, max output `384K` | Same DeepSeek OpenAI-format API; thinking/non-thinking modes | Best same-provider upgrade; cheap enough by stated ceiling; likely improves semantic comparisons while preserving daemon compatibility. Risk: still needs live proof and may produce more hidden/thinking output if enabled. | First final-authority candidate to test. Also useful as confirmation model for Flash-screened accepts. |
| Gemini `gemini-2.5-flash-lite` via Gemini OpenAI endpoint | `$0.40` standard, `$0.20` batch/flex | `$0.10` standard, `$0.05` batch/flex | `1M` | Google documents OpenAI-compatible chat completions endpoint; native structured-output support exists outside Mind's NOTA path | Very strong price point, long context, structured-output ecosystem, likely good for classification/extraction. Risk: Lite may underperform on nuanced conflict identity and stable-positive acceptance; OpenAI-compatible endpoint may not expose every Gemini-native control. | Second cheap final-authority candidate after DeepSeek Pro, or first non-DeepSeek candidate. |
| Mistral Small 4 direct or via OpenAI-compatible router | `$0.60` | `$0.15` | `256K` | Native Mistral API; use a compatible router unless direct OpenAI shape is verified for current daemon | Hybrid instruct/reasoning/coding model with configurable reasoning effort; official note emphasizes shorter outputs at comparable reasoning performance. Risk: not as cheap as Flash but still below DeepSeek Pro; direct API compatibility must be verified before running through current daemon. | High-value final-authority candidate if accessible through current daemon path; otherwise defer until adapter/router is available. |
| Qwen `qwen3.7-plus` Alibaba global | `$1.101` <=256K, `$3.301` >256K | `$0.276` <=256K, `$0.826` >256K | Up to `1M` tier | Alibaba Model Studio uses Qwen-compatible API; third-party model catalog says same API format for Qwen and listed third-party models | Good mid-tier agent/coding model, likely stronger than Flash for classification. Risk: output cost is above the DeepSeek Pro ceiling at normal global pricing and jumps for long contexts; thinking output may count as output. | Try after cheaper candidates if identity-bearing categories still fail; not the first affordability pick. |
| Qwen `qwen3.6-flash` / `qwen3.5-flash` Alibaba | `qwen3.6-flash`: `$1.50` <=256K, `$4.00` >256K international; `qwen3.5-flash`: `$0.40` up to 1M international | `$0.25` / `$1.00`; `qwen3.5-flash` `$0.10` | Up to `1M` | Alibaba Model Studio | Qwen flash line is cheap and long-context; `qwen3.5-flash` price is excellent. Risk: likely closer to DeepSeek Flash than final judge quality unless the newer model's classification behavior is much better; `qwen3.6-flash` output is not cheaper than DeepSeek Pro. | Test `qwen3.5-flash` only as cheap screen. Use `qwen3.6-flash` only if the exact available route is cheaper in the local account/region. |
| Qwen `qwen-long-latest` Alibaba | `$0.287` | `$0.072` | Long-context model | Alibaba Model Studio | Extremely cheap long-context route. Risk: optimized for long input handling rather than subtle reasoning; likely not enough for final authority but could help neighbor pre-summarization if Mind later adds deterministic retrieval/context shaping. | Not a final judge candidate. Possible future context-assist experiment only. |
| MiniMax `MiniMax-M3` direct | `$1.20` <=512K, `$2.40` >512K; cache read `$0.06`/`$0.12` | `$0.30` <=512K, `$0.60` >512K | `1M` | MiniMax documents OpenAI-compatible chat completions and `MiniMax-M3` context | Built for agentic reasoning, tool use, coding, and long context; price still near affordable band. Risk: above DeepSeek Pro on output; M3 is broad agent/coding oriented, not proven for compact semantic judgment. | Good second-wave final-authority test if DeepSeek Pro/Gemini/Mistral fail. |
| MiniMax `MiniMax-M2.7` / `M2.5` direct | `$1.20`; highspeed `$2.40` | `$0.30`; highspeed `$0.60` | `204.8K` | MiniMax OpenAI-compatible chat completions | Mature lower-cost MiniMax line, possibly adequate for classification. Risk: similar output price to M3 with less context/capability, so little reason to prefer unless M3 rate limits are poor. | Backup screen/final candidate only if M3 unavailable. |
| Kimi `kimi-k2.7-code` direct/Alibaba/Together | `$4.00` direct/Together; `$3.713` on several Alibaba global routes | `$0.95` direct/Together; `$0.894` on Alibaba global routes | `256K` | Kimi docs use OpenAI SDK/base URL; JSON Mode/tool calls; K2.7 Code requires thinking enabled | Strong instruction compliance, long-context coding, and reasoning claims. Risk: output cost is 4.3x DeepSeek Pro and K2.7 Code fixed thinking/temperature behavior may be awkward for deterministic judge calls. | Do not start here for affordability. Use as premium comparison only if cheaper models cannot clear identity/reason gates. |
| Kimi `kimi-k2.6` direct | `$4.00` direct; Kimi page lists cache-hit `$0.16` and input `$0.95` | `$0.95` | `256K` | OpenAI SDK/base URL; thinking can be disabled for K2.6 | Stronger instruction/self-correction claims than older Kimi; can disable thinking, unlike K2.7 Code. Risk: same high direct output price; Alibaba global direct K2.6 availability was not visible in US/Germany sections inspected. | Premium diagnostic candidate, not an affordability shortlist model. |
| GLM-5.2 via Together | `$4.40`; cached input `$0.26` | `$1.40` | `256K` on Together; max output `131K` | Together page says OpenAI-compatible and Anthropic Messages compatibility for integrations; JSON mode/function calling listed | Strong long-horizon/reasoning positioning, configurable thinking, and likely good at complex code/agent reasoning. Risk: no official launch benchmarks on Together page; output price is far above the accepted DeepSeek Pro edge; long output budgets can be dangerous for cost. | Good capability probe, not an affordable first-line final judge. |
| GLM-5.2 via Alibaba global routes | `$3.851`; input `$1.100` | `$1.100` | Flat-rate route; Alibaba catalog lists GLM-5.2 as third-party | Alibaba Model Studio catalog says third-party models use same API format as Qwen models | Cheaper than Together but still 4.4x DeepSeek Pro output; may be attractive if local Alibaba route is already configured and quality is excellent. | Try only after cheaper candidates or as a GLM-specific answer to the user's question. |
| xAI `grok-4.3` direct | `$2.50` | `$1.25` | `1M` | xAI REST; docs include structured outputs/reasoning sections, but current daemon compatibility should be verified | xAI describes minimal hallucinations, configurable reasoning, and long context. Risk: output price is 2.9x DeepSeek Pro; not clearly better fit than Gemini/Mistral/MiniMax for this narrow classifier. | Lower priority. Test only if cheaper options fail and xAI route is easy. |
| xAI `grok-build-0.1` direct | `$2.00` | `$1.00` | `256K` | xAI REST; verify daemon compatibility | Coding-agent tuned, maybe precise on code/domain facts. Risk: not primarily a semantic taxonomy judge; output price above shortlist. | Not first-line. |
| OpenAI `gpt-5-mini` direct | `$2.00`; cached input `$0.025` | `$0.25` | Model page inspected for price; context not relied on here | Native OpenAI API; strongest structured-output support | Excellent schema adherence path if Mind later adds JSON-schema/provider-native output. Risk: output cost above affordable target and user already flagged GPT/Claude class as too expensive; current Mind emits NOTA, not schema. | Useful benchmark/control, not budget final authority. |
| OpenAI `gpt-5.4-nano` / `gpt-5-nano` class | `gpt-5.4-nano` `$0.625`; external route pages report `gpt-5-nano` `$0.40` | `$0.10` or lower depending model/route | Not relied on | OpenAI API, structured outputs | Very attractive for structured classification if capability is enough. Risk: nano models may repeat the Flash failure pattern on nuanced paraphrase/conflict identity; exact current native model/price should be rechecked before live eval. | Consider as cheap screen or schema baseline, not first final authority without a small pilot. |

## Shortlist

1. DeepSeek `deepseek-v4-pro`: best immediate upgrade. It is the only candidate that is both strongly compatible with current DeepSeek-oriented settings and exactly at the user's remembered output-cost ceiling (`$0.87/M`). It should be tested as final authority first.

2. Gemini `gemini-2.5-flash-lite`: best cheap non-DeepSeek challenger. At `$0.40/M output` with 1M context and an OpenAI-compatible endpoint, it is inexpensive enough to be a production judge if it clears identity/reason categories. The main unknown is whether Flash-Lite has enough semantic precision for paraphrase and conflict identity.

3. Mistral Small 4: best value reasoning hybrid if reachable through the current daemon without an adapter. It is below DeepSeek Pro on output (`$0.60/M`) and explicitly unifies instruct, reasoning, and coding behavior with configurable reasoning effort. Verify OpenAI-compatible route before live eval.

4. MiniMax M3: stronger long-context/agent candidate at a still-plausible but not ideal output price (`$1.20/M`, or `$2.40/M` above 512K input). It is likely worth testing if the first three fail, especially because MiniMax's OpenAI-compatible docs line up with the daemon.

5. Qwen `qwen3.7-plus` or `qwen3.5-flash`: Qwen deserves a lane because its recent models are strong and Model Studio has broad API coverage. For pure affordability, `qwen3.5-flash` at `$0.40/M output` is more interesting than `qwen3.7-plus`; for capability, `qwen3.7-plus` is more plausible but not cheaper than DeepSeek Pro.

6. GLM-5.2: capability-interest candidate, not cost-first. Use it if the user specifically wants to answer the GLM question with live evidence or if all cheaper models fail.

Premium controls only: Kimi K2.7 Code/K2.6, xAI Grok 4.3, and OpenAI GPT-5 mini. These are useful as quality references but not as first affordability candidates.

## Final Authority Versus Screen

Final-authority candidates:

- DeepSeek `deepseek-v4-pro`
- Gemini `gemini-2.5-flash-lite` if it clears identity-bearing and valid-positive gates
- Mistral Small 4 if an OpenAI-compatible route is available
- MiniMax M3 if cheaper candidates fail
- Qwen `qwen3.7-plus` if capability justifies output cost

Draft/reject-only screen candidates:

- DeepSeek `deepseek-v4-flash`
- Qwen `qwen3.5-flash`
- OpenAI nano-class models
- possibly Gemini Flash-Lite if it is strong on safety/rejects but weak on valid positives

Do not use draft screens to accept into the store unless a final-authority model confirms. A cheap model can safely reduce expensive calls only when it emits a rejection class with high measured precision, or when deterministic exact duplicate code already resolves the case.

## GLM-5.2 Answer

GLM-5.2 is likely good at this kind of reasoning in the broad sense: it is positioned as a reasoning/chat/code model with 744B/753B-class MoE scale, 40B active parameters, configurable thinking, large context, JSON/function features, and long-horizon orchestration use cases. That maps well to Mind's hard parts: proposition comparison, neighbor-sensitive conflict reasoning, and resisting prompt-like neighbor text.

But it is not the best affordability candidate. Together lists it at `$4.40/M output`, and Alibaba global routes inspected list GLM-5.2 at `$3.851/M output`. That is roughly 4.4x to 5.1x DeepSeek Pro's direct `$0.87/M output` and 9.6x to 11x Gemini Flash-Lite's `$0.40/M output`. Also, the Together page explicitly says no official benchmarks were published at launch, so the praise should be treated as capability signal, not proof for Mind's semantic taxonomy.

Practical answer: yes, GLM-5.2 is plausible for this reasoning class, but it should be a capability probe or premium comparator, not the first model to try for an affordable accepted-knowledge judge.

## Practical Eval Plan

Prerequisite harness fixes before model comparison:

- Fix conflict identity scoring so `ConflictsAcceptedKnowledge` requires the exact minimal identity set, not "contains expected".
- Rename or replace the current runner-ledger storage absence witness so reports do not overclaim direct storage absence.
- Include temporal/unstable in the safety gate or split safety metrics into private/task/temporal submetrics.
- Prefer deterministic isolated fixture seeding when available; until then, keep setup failures separated from primary rows.

High-level run shape using the existing Rust harness:

```sh
cd /git/github.com/LiGoldragon/mind
cargo build --bin mind-live-knowledge-judge-eval --bin mind --bin mind-daemon --bin mind-write-configuration

target/debug/mind-live-knowledge-judge-eval \
  --mode stateful \
  --probe-rejections \
  --provider <provider-name> \
  --endpoint <openai-compatible-base-url> \
  --model <model-id> \
  --secret-source <typed-secret-source-reference> \
  --eval-id <model>-stateful-<date> \
  --output-directory /home/li/primary/agent-outputs/MindLiveJudgeEval/<model>-stateful \
  --work-directory /tmp/mj-<short-model>-stateful

target/debug/mind-live-knowledge-judge-eval \
  --mode isolated-categories \
  --probe-rejections \
  --provider <provider-name> \
  --endpoint <openai-compatible-base-url> \
  --model <model-id> \
  --secret-source <typed-secret-source-reference> \
  --eval-id <model>-isolated-<date> \
  --output-directory /home/li/primary/agent-outputs/MindLiveJudgeEval/<model>-isolated \
  --work-directory /tmp/mj-<short-model>-isolated
```

Do not put resolved API keys in commands, reports, manifests, or chat. Use the existing typed secret-source mechanism only.

Suggested live eval order:

1. `deepseek-v4-pro`, thinking enabled at low or medium if the existing config can set it, with the same `maximum_output_tokens` cap used for Flash unless invalid/truncated output appears.
2. `gemini-2.5-flash-lite` through `https://generativelanguage.googleapis.com/v1beta/openai/`, starting with low thinking if exposed through `extra_body` is later supported; otherwise default chat-completions mode.
3. Mistral Small 4 through a verified OpenAI-compatible route. Start with no/low reasoning effort, then high only if taxonomy errors persist.
4. MiniMax `MiniMax-M3` through its OpenAI-compatible chat endpoint.
5. Qwen `qwen3.5-flash` as cheap screen and `qwen3.7-plus` as stronger Qwen final-authority candidate if budget permits.
6. GLM-5.2 via Alibaba or Together only as a capability comparator.

Promotion gates should be stricter than aggregate pass rate:

- Paraphrase duplicate: near-perfect, because duplicates are the highest-risk silent store pollution.
- Conflict identity: exact minimal identity set must pass.
- Valid positives: high enough that the judge does not block ordinary stable knowledge; target at least `90%` before final authority.
- Safety/private/task/temporal: `100%` or documented reason for any miss.
- Structured output: invalid NOTA retries should be counted. Any model that often emits prose around NOTA is a poor fit even if verdicts are semantically good.

Cost controls:

- Keep `maximum_output_tokens` tight. The production verdict is one NOTA value; long rationales are waste.
- Disable thinking for screen models when allowed; enable low/medium thinking only for final-authority candidates whose first run shows semantic rather than output-format failures.
- Do not use Kimi K2.7 Code as an early judge because it requires thinking and fixed sampling behavior, which can inflate output cost and reduce deterministic control.
- Reuse provider prompt caching where available for the long static judge prompt and repeated eval setup, but do not let input-cache discounts distract from output-token price.

## Unknowns And Blockers

- I did not run live provider calls, so all suitability rankings are source-backed expectations, not Mind-specific outcomes.
- Some routes have provider-specific request extensions. The current daemon can send `reasoning_effort` and DeepSeek-style `thinking`, but not arbitrary provider `extra_body`; Gemini thinking controls and some vendor-specific switches may require adapter work or accepting default behavior.
- Mistral direct OpenAI-compatible support was not verified from primary Mistral docs in this pass. Use a gateway/router or verify before scheduling a live run through the current daemon.
- Provider account region can change effective Qwen/GLM/Kimi pricing. The report uses official/global route prices visible in the inspected pages; check the actual configured account region before committing budget.
- Structured JSON/schema support is valuable evidence for output reliability, but Mind currently asks for NOTA text. Provider-native schema features do not automatically help until Mind adds a schema-backed provider mode or translates JSON into typed verdicts.
