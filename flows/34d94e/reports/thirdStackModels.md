# Third open-weight council candidate — bounded research note

**Checked 2026-09-14.** This compares published weights and documented
interfaces only. It does not install, call, benchmark, or spend on any provider.
Vendor benchmark tables are vendor claims; they are not evidence that a model is
careful, doubtful, suitable for council membership, or able to run subflows.

## Short recommendation

**Propose a controlled evaluation of DeepSeek-V4.1-Flash as the first third
candidate, pinned to its Hugging Face weight revision rather than an API alias.**
It is an MIT-licensed, downloadable 552B-MoE model with 8B/16B activated
parameters, 1M context, multimodal input, documented tool-call/prompt tooling,
and a published reproduction path for one agent benchmark. These make it the
best *currently documented* candidate for a harness trial, not a proven most
careful or conceptually capable council member. [DeepSeek model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)

The evaluation should use the same bounded research/database task, fixed
harness/tool permissions, source pin, prompt, budget, and an independent
reviewer. Score source fidelity, uncertainty calibration, refusal to invent
evidence, tool-use recovery, and disagreement quality separately from coding.

**Do not use the official API alias as an identity pin.** On 2026-09-14,
`deepseek-flash` selects V4.1-Flash; legacy `deepseek-v4-flash` and
`deepseek-v4-flash-vision-exp` are temporarily routed there, and
`deepseek-v4-pro` requests route there until V4.1-Pro launches.
[DeepSeek announcement](https://www.deepseek.com/en/news/deepseek-v4-1-flash/)
[API model table](https://api-docs.deepseek.com/quick_start/pricing/)

## Candidate comparison

| Candidate | Weights and license | Research/tool evidence | Main limitation |
| --- | --- | --- | --- |
| **DeepSeek-V4.1-Flash** | Official Hugging Face card identifies downloadable V4.1 weights as MIT; its card reports 552B backbone parameters, 8B active prefill/16B decode, 1M context. [card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) | Official card documents a maintained prompt/protocol toolkit, tool-call encoding, and reproducible DeepSWE instructions. Its agent benchmark table is vendor-run and scaffold-sensitive: it reports results under several harnesses and settings. [card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) | Model/inference transport/tool execution are left to the integrator. API aliases demonstrably change routing, so hosted behavior is not a stable model identity. |
| **Qwen3.5-397B-A17B** | Official Qwen release says 397B total/17B active. The official HF weight repository is 807GB and Apache-2.0. [Qwen release](https://qwen.ai/blog?email_hash=23463b99b62a72f26ed677cc556c44e8&id=qwen3.5) [weights](https://huggingface.co/Qwen/Qwen3.5-397B-A17B/tree/main) [license](https://huggingface.co/Qwen/Qwen3.5-397B-A17B/blame/main/LICENSE) | The weight card gives vLLM/SGLang serving paths and supports multimodal input. A smaller Qwen3.5 card documents tool-call parser integration, but that is compatibility information, not a reliability study. [397B card](https://huggingface.co/Qwen/Qwen3.5-397B-A17B/tree/main) [9B card](https://huggingface.co/Qwen/Qwen3.5-9B) | The official hosted `Qwen3.5-Plus` adds 1M context, built-in tools and adaptive tool use; those hosted features must not be attributed automatically to the open weights. No independent evidence here establishes research judgment or subflows. |
| **GLM-5.2** | Official HF weights are MIT and listed at 1.51TB. The card says GLM-5.2 is aimed at long-horizon tasks and 1M context. [weights/card](https://huggingface.co/zai-org/GLM-5.2) [license](https://huggingface.co/zai-org/GLM-5.2/blob/main/LICENSE) | The Z.ai repository frames GLM-5 as agentic engineering and publishes local serving directions; these are vendor claims/docs. [GLM-5 repo](https://github.com/zai-org/GLM-5) | The 1.51TB artifact makes local operation a substantial infrastructure decision. The 5.2 card itself points to a newer 5.3 weight; this note does not treat 5.2 as the current GLM answer without separately verifying 5.3’s exact license, weights and tool support. |

## DeepSeek V4/V4.1 distinction

- V4-Pro and V4-Flash are open-weight V4 releases; the official April API
  notice describes Pro as 1.6T total/49B active and Flash as 284B/13B active.
  [official V4 notice](https://api-docs.deepseek.com/news/news260424/)
- V4.1-Flash is a distinct official HF model card, not merely an API spelling:
  it names a different 552B backbone and its own architecture. It remains
  MIT-licensed. [V4.1 card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)
- The current API route change means an API result labelled with a legacy V4
  name should not be described as a fixed V4 checkpoint result. [official announcement](https://www.deepseek.com/en/news/deepseek-v4-1-flash/)

## What research/database access and subflows actually require

Weights do not grant web, database, credentials, sandbox, or subflow access.
Those are harness capabilities and permissions. A candidate can only be said to
have them after the selected harness gives them explicitly and records the
boundary. The DeepSeek card’s evaluation harness examples show compatibility
with agent scaffolds, but do not prove this workspace’s integration.

A third member should therefore be selected in two stages:

1. choose an open-weight checkpoint and immutable revision;
2. evaluate it in a minimal, separately permissioned harness with an approved
   research/database connector and a bounded child-task protocol.

No “most doubtful” conclusion follows from coding, terminal, or agent benchmark
scores. The council can decide whether its desired third role values dissent,
literature synthesis, fault finding, or throughput, then evaluate that role.

## Sources

All URLs above were checked 2026-09-14. Primary sources are DeepSeek’s API
docs/news and official DeepSeek, Qwen, and Z.ai Hugging Face/GitHub pages.
Vendor performance claims are labelled as such. No provider, model endpoint, or
local inference runtime was invoked.

