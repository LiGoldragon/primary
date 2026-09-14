# Third council stack recommendation — 2026-09-14

Codex recommendation for Fable's doubt and representation. The living has authorized advancing the five audit suggestions and asks for a careful, doubtful, conceptually capable and considerate open-weight stack with its own research subflows. This document chooses the first evaluation target; it does not report a model trial, provider selection, or production deployment.

## Recommendation

**Start with Kimi K3 as the principal model in an OpenCode-based research/review harness. Compare DeepSeek-V4.1-Flash in the same harness as the strongest alternative from this pass.** Select the eventual third council member from observed evidence quality, not from a vendor's coding rank or a name that sounds like a reasoning model.

K3's official card describes an open-weight, native-multimodal model with a one-million-token context and reports research/reasoning/tool benchmarks. This makes it a credible candidate for the role; the published results are vendor evaluations with differing harnesses, not a controlled test of considerate doubt. [K3 model card](https://huggingface.co/moonshotai/Kimi-K3)

The model's custom Kimi K3 license is not MIT/Apache. We should call this **open-weight** rather than claim a completely open training stack. The published license permits use and modification subject to its conditions, including conditions for certain commercial model-service businesses. [License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE)

DeepSeek-V4.1-Flash supplies a materially different model family and MIT weights for the comparison. Its official API routes changed on September14: a legacy `deepseek-v4-pro` label does not currently prove V4-Pro weights were used. Pin and record the actual checkpoint or disclose that the hosted identity is an evolving service alias. [DeepSeek release](https://www.deepseek.com/en/news/deepseek-v4-1-flash/) [weights](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)

The parallel model reader preferred DeepSeek as first evaluation target; I prefer K3 for this particular broad conceptual/research principal role, with cost not the overriding criterion. Neither conclusion is a benchmark result. The same-fixture comparison is how we resolve that disagreement. Root follow-up also checked current GLM5.3 and Qwen3.8-27B weights. GLM5.3 publishes strong agent/reasoning vendor results and uses its own license rather than inheriting GLM5.2's MIT label; include it as an additional serious comparison arm. Qwen3.8-27B is Apache-2.0 and a credible smaller local-helper candidate, subject to hardware and fidelity testing. Neither has been trialed here. [GLM5.3](https://huggingface.co/zai-org/GLM-5.3) [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)

## Proposed composition

| Part | First configuration to evaluate | Purpose |
| --- | --- | --- |
| Principal | Kimi K3, explicitly recorded reasoning effort; compare high and max on hard cases | Frame the question, identify assumptions, reconcile evidence, produce one considerate judgment. |
| Source researcher | Separate K3 subflow with bounded read/search/fetch tools | Gather primary sources and original local records without seeing the principal's preferred conclusion first. |
| Counterexample researcher | Independent subflow; compare same-model K3 and DeepSeekV4.1 variants | Seek disconfirming examples, alternate explanations and missing conditions. Independent assignment matters more than a title like “critic.” |
| Evidence verifier | Separate subflow with cited-record access and reproducible checks | Reopen citations, verify dates/versions/callsites and distinguish source coverage from a successful run. |
| Knowledge access | Existing local records/code plus a provenance-returning search/read interface | Return record ID/path/revision/date and relevant source text; keep raw, approved direction, peer claims and observations distinct. |
| Final council identity | One principal third-member flow | Child flows contribute evidence, not extra council votes. Principal remains responsible for explaining and revising its conclusion. |

Critical inference and criticism should initially use capable models. A small local model may later help with mechanical indexing/extraction only after it passes fidelity checks. The hardware described in earlier records is not evidence that K3 fits locally.

OpenCode offers configurable main/subagents, per-agent model/tools/permissions, and headless server/events; Moonshot publishes a K3 integration guide. These are documented surfaces, not a witnessed package or model-adapter integration here. [OpenCode agents](https://opencode.ai/docs/agents/) [server](https://opencode.ai/docs/server/) [Moonshot integration](https://platform.kimi.ai/docs/guide/open-code)

The harness is orchestration around the model. Message remains the selected inter-component messaging owner; this recommendation does not create another global orchestrator or redefine Nexus. Use source-event and member identities to link the third flow to the pair while keeping origins labelled.

## What makes the stack careful

The task protocol should ask for the strongest supported conclusion and the evidence that could change it. It should reward catching a real mistake, acknowledging a sound proposal, and correcting itself after counterevidence. Reflexive disagreement, performative hesitation, invented citations and endless searching all fail the role.

For material claims: state source and date, what was actually observed, unresolved alternatives and a confidence level. For recommendations: explain consequences in the living's terms and propose a concrete next check. Considerateness is assessed alongside correctness: preserve the user's intent, state disagreement plainly and respectfully, and avoid outsourcing routine technical decisions back to the user.

Longer deliberation, rewards in a prompt and more agents are not guarantees of better judgment. Give the stack useful tools, independent evidence assignments, explicit correction opportunities and a stop rule when additional searching no longer changes the decision. A model's native architecture/training still matters; a strong harness cannot be assumed to make every model equivalent.

## Admission tests already prepared

[The evaluation rubric](thirdStackEvaluation.md) turns our own audit failures into testable cases: wrong service name, conditional polling, scoped absence, stale records, raw versus approved context, counterevidence revision, considerate dissent, conceptual layer separation, retrieval fidelity and authorized task scope. Use synthetic source bundles, blinded labels, paired cases where the initial claim is either true or false, and repeat runs before ranking.

Score factual support, calibration, quality of counterevidence, revision after correction and considerate usefulness separately. Compare the same harness/task/tools first, then model-appropriate harness tuning. A same-model subflow is not an independent ground-truth judge. Human review checks alleged critical failures and a sample of ordinary scores. Report latency and tool/compute use, but do not select the fastest stack when evidence quality is worse. Scores and thresholds are a proposed screening rubric, not validated scientific metrics.

Before any real task trial, test the adapter with synthetic assistant/tool messages. K3 requires complete assistant-message replay across turns, including its provider fields and tool calls; an adapter that drops required fields is not equivalent to the documented model interface. Its official guidance also warns against relying on the currently changing built-in web search, so research tools should be supplied by our harness. [K3 API guide](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)

## Hosting and implementation boundary

I recommend evaluating through a suitable hosted endpoint first, while retaining the option to control the weights later. This is a proposal, not authorization to open an account, spend or send private records to a new provider. Confirm provider identity, retention and tool-field fidelity before using actual local records. Synthetic fixtures can be prepared without those credentials.

K3 self-hosting is cluster-scale: the published vLLM recipe lists at least8×GB300 or8×MI355X/MI350X for its supported setup. That is a published recipe, not a proven minimum for every quantization or an inventory of our hardware. Do not promise a laptop deployment. [vLLM K3 recipe](https://recipes.vllm.ai/moonshotai/Kimi-K3)

Keep durable harness packaging/configuration in the existing declarative environment owner, pin source/model identity and preserve transcripts. No Python messenger/orchestration script is proposed. Provider inference implementations are a separate component choice; this document does not claim the whole inference dependency tree contains no Python.

## Work advanced and what remains

Prepared current primary-source comparisons and a concrete evaluation rubric. No model call, model download, provider signup or running third member exists from this task. The existing two-member POC agreement stands; production still requires the third member and the recorded council agreement.

In parallel, Codex has accepted Fable's exact implementation split: sandbox retest/merge of the existing messenger fixture; integrated Message POC; generated component-evidence tooling; disk-derived repository inventory; rename plan only. Fable owns its five read-only investigations. Those tasks have separate evidence and deployment gates; none is silently treated as completed by choosing this candidate.

## Sources

- Primary model, license, serving and harness URLs cited above, checked2026-09-14. Vendor claims remain labelled.
- [Independent alternative-model research](thirdStackModels.md), [harness comparison](thirdStackHarness.md), [evaluation design](thirdStackEvaluation.md). Root's recommendation resolves their differing provisional rankings; it is not a claim they independently agreed on a winner.
- `flows/6cc91b/vision/thirdModel.md`; latest living request linked in evaluation report to transcript UUID3392116e-3b02-420a-9aa3-056894cb9395, timestamp2026-09-14T15:17:00.135Z.
- `flows/6cc91b/log.md`, latest artifact-comment working instructions: retest/merge and proposed deployment explanation; two-member POC, no production.
