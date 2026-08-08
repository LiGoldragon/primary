# Overview — local AI toolkit prefetch mining — 2026-06-03

## Result

The Prometheus prefetch results were mined successfully. The result set has 19 rows and 0 failures. The subagent reports that all inspection happened through read-only SSH to Prometheus and that no downloads, builds, or evaluations were performed on this machine or any non-Prometheus computer.

## Llama-router candidates

The GGUF candidates worth considering for `llm.json` are:

- `qwen3-coder-next-80b-a3b-q5-k-m` — four split GGUF files.
- `gemma-4-e4b-it-ud-q8-k-xl` — GGUF model file.
- `gemma-4-e4b-it-mmproj-f16` — multimodal projection companion for Gemma E4B, not a standalone chat model.
- `nemotron-3-nano-omni-30b-a3b-reasoning-ud-q4-k-xl` — GGUF model file.
- `nemotron-3-nano-omni-30b-a3b-reasoning-mmproj-f16` — multimodal projection companion for Nemotron, not a standalone chat model.

The full SRI hashes and Prometheus store paths are in `reports/system-operator/185-local-ai-toolkit-prefetch-mining-2026-06-03/1-subagent-prefetch-mining.md`.

## Keep out of `llm.json` for now

These were prefetched successfully but should stay out of `llm.json` until their runtime homes are designed:

- `parakeet-tdt-0.6b-v3` — `.nemo`, speech/runtime home needed.
- `qwen3-embedding-8b` — safetensors embedding model, embedding runtime home needed.
- `qwen3-reranker-8b` — safetensors reranker model, reranker runtime home needed.
- `flux-2-klein-4b-q5-k-m` — GGUF artifact but not a llama-router LLM chat runtime target.

## Recommended next action

Do not blindly add every GGUF row to `llm.json`. The next system-operator pass should inspect the current `CriomOS-lib/data/largeAI/llm.json` schema and add only the actual llama-router entries:

1. Qwen3 Coder Next as a split-GGUF model entry, if the router/schema supports split file sets.
2. Gemma E4B Q8 as a model entry with its mmproj companion wired according to the existing multimodal schema.
3. Nemotron 3 Nano Omni Q4 as a model entry with its mmproj companion wired according to the existing multimodal schema.

Before any build or validation that can touch model artifacts, run it on Prometheus or the designated AI node only.
