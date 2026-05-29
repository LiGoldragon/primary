# Prometheus Gemma 4 serving fix

## Frame

The local Pi profile was already configured to use `criomos-local/gemma-4-26b-a4b`, and Prometheus exposed Gemma 4 model IDs, but the deployed server was still `llama-cpp-8470`. That binary could list the files but failed at load time with `unknown model architecture: 'gemma4'`.

## Implemented fix

CriomOS now overrides the Strix Halo llama.cpp package to upstream b9404, including the moved npm package-lock root at `tools/ui` and the matching fixed `npmDepsHash`.

Pushed CriomOS commit:

- `a10a35ad3bf5` — `llm: update llama.cpp package for Gemma 4`

Prometheus was deployed from pushed `github:LiGoldragon/CriomOS/main` using the Prometheus builder path. The BootOnce generation booted as generation 47, then was promoted with transient systemd units:

- `lojix-promote-gemma4-generation-47.service` — `switch-to-configuration switch`
- `lojix-set-default-generation-47.service` — `bootctl set-default nixos-generation-47.conf`

Both units exited successfully. Current and persistent default boot entry are now generation 47.

## Verification

Verified runtime state:

- Prometheus `prometheus-llama-router.service` is active.
- The service is running `llama-cpp-9404`.
- `gemma-4-26b-a4b` loads successfully through the OpenAI-compatible API.
- `gemma-4-31b` loads successfully through the OpenAI-compatible API.
- Pi headless call with `criomos-local/gemma-4-26b-a4b` returned `OK`.
- Primary AP, backup AP, SSH, and the LLM router remained active after booting generation 47.

Observed performance from the smoke tests:

- `gemma-4-26b-a4b`: about 17 prompt tokens/s and 16 generation tokens/s for the tiny probe.
- `gemma-4-31b`: about 10 prompt tokens/s and 4 generation tokens/s for the tiny probe.

## Note

Tiny direct API probes with very low `max_tokens` may return text in `reasoning_content` before normal answer content, because the Gemma 4 chat template exposes reasoning. Pi's headless probe produced normal visible output for the default 26B model.
