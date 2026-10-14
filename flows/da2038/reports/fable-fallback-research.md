# Fable fallback research (2026-10-14, Sonnet subflow, web sources; vendor scores unverified)

Local machine: no discrete GPU (Intel Meteor Lake iGPU), 30 GiB RAM, llama-server installed; ollama/vllm absent. => hosted for real work; local only a small filter or tests.

Shortlist (open weights):
1. GLM-5.2 (MIT) — highest open-weight AA index (51); best judgment/design stand-in; ~$0.45 in / $3.31 out per M; token-hungry.
2. DeepSeek V4 Flash (284B/13B active, MIT, 1M ctx) — 79.0% SWE-bench Verified; ~$0.05–0.14 in / $0.24–0.28 out per M; best value for lean calls.
3. DeepSeek V4 Pro — 80.6% SWE-bench Verified reported; licence unconfirmed.
4. Kimi K2.6 (1T/32B active, modified MIT, 262K) — ~80.2%; hosted only.
5. Qwen3.8-27B (Apache 2.0, 262K) — only one that fits locally (~17–19 GB Q4), slow here.
Independent standardized boards score open weights far lower (best 38.7% on Scale SWE-bench Pro): test on our own dialect.

Structured output: llama-server GBNF grammars can enforce Variant.{ Field … } exactly; vLLM/SGLang (XGrammar) support custom CFGs; most hosted APIs only JSON schema — per-provider check needed. A grammar fixes syntax, not content: parser + retry.

Router evidence: RouteLLM (ICLR 2025) >2x cost cut at equal quality; ICML 2026 "Is Escalation Worth It?" — a light pre-generation router beats cascades on 4/5 datasets. None measured on agentic/design requests: measure on our labeled requests.

Data: DeepSeek first-party API retains data for training; no-train hosts cost about double.
