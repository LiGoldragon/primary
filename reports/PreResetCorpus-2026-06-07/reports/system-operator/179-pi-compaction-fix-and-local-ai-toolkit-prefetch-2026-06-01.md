# Pi compaction fix and local AI toolkit prefetch — 2026-06-01

## Frame

The immediate failure was that this Pi session lost useful task continuity after auto-compaction. I treated it as a harness/runtime issue first, then resumed the Prometheus model-toolkit work by starting durable target-side downloads.

No new Spirit capture was made for this turn: the prompt was a work order plus a tentative bug observation, not a durable rule or decision beyond the already-captured preference for Prometheus-side durable predownloads.

## Pi harness diagnosis and fix

CriomOS-home was still packaging Pi `0.76.0`. Upstream Pi `0.77.0` carries two relevant lifecycle fixes:

- session disposal now aborts in-flight agent, compaction, branch-summary, retry, and bash work;
- follow-up messages queued by `agent_end` extension handlers are drained before the agent becomes idle.

The second point matches the observed class of failure: after compaction or event settlement, queued continuation/extension work can be left behind and the agent appears to have failed or stopped carrying the task.

I updated CriomOS-home to Pi `0.77.0`:

- `flake.nix`: `pi-src` now points at `github:earendil-works/pi?ref=v0.77.0`.
- `flake.lock`: `pi-src` now pins upstream commit `8322745e28f47225e9f8c8161c1dca5c0bd74dfb`.
- `packages/pi/default.nix`: package version is `0.77.0`; npm dependency hash is updated for that source.

The CriomOS-home commit is `a21e45bbc12d` — `home: update Pi to 0.77` — and it is pushed to `origin/main`.

## Validation

Completed checks:

- Built `packages.x86_64-linux.pi` successfully from the new source.
- Built the Pi harness checks:
  - `checks.x86_64-linux.pi-harness-profile`
  - `checks.x86_64-linux.pi-criomos-extension-load`
- Ran `nix flake check --no-build`; all checks evaluated.
- Activated Home on `ouranos` with `lojix-cli (HomeOnly goldragon ouranos li ... Activate None None)` from pushed `github:LiGoldragon/CriomOS-home/main`.
- Verified the live profile reports `pi --version` as `0.77.0`.
- Verified Pi still sees the local quantized Gemma model `criomos-local/gemma-4-26b-a4b-ud-q4-k-xl`.
- Ran a local Prometheus-backed Pi smoke prompt on `gemma-4-26b-a4b-ud-q4-k-xl`; it returned `OK`.

Important limitation: this already-running Pi process is still the old process image. New Pi sessions started after activation use `0.77.0`.

## Curated model-toolkit direction

The toolkit should avoid near-duplicate entries. The current inventory has many overlapping general/reasoning models. The next target shape is one best/latest model per role:

- Daily local text + vision: keep `gemma-4-26b-a4b-ud-q4-k-xl` as the likely default because it is already deployed, compact, and verified through text and vision.
- Higher confidence same family: keep `gemma-4-26b-a4b-ud-q8-k-xl`; do not add more Gemma 26B variants beyond explicit BF16 reference if needed.
- Coding agent specialist: add `qwen3-coder-next-80b-a3b-q5-k-m` as the current best open coding-agent GGUF candidate; it is non-thinking, 80B total / 3B active, 262K context.
- Small audio/vision scout: add `gemma-4-e4b-it-ud-q8-k-xl` plus `mmproj-F16`; this is the small Gemma-family candidate for image/audio experiments.
- Omni perception: add `nemotron-3-nano-omni-30b-a3b-reasoning-ud-q4-k-xl` plus `mmproj-F16`; this is the single broad image/audio/video/text perception candidate.
- Speech-to-text: add `parakeet-tdt-0.6b-v3` as the single best/latest local ASR candidate; it is not a llama-router model and needs a separate runtime path.
- Text retrieval: add Qwen3 Embedding 8B + Qwen3 Reranker 8B as the single text RAG pair.
- Image generation/editing: add FLUX.2 Klein 4B Q5_K_M as the compact Apache-2.0 local image generation/editing candidate; this needs ComfyUI or another image runtime, not the llama router.

Models to demote or avoid adding as duplicates once replacements prove out:

- `gpt-oss-120b`, unless it wins a specific benchmark over Qwen3-Coder-Next or the current large Qwen.
- older small Qwen reasoning duplicates (`qwen3.5-27b`, `qwen3.6-27b`, `qwen3.6-35b-a3b`) if no distinct workflow chooses them.
- non-omni `nemotron-3-nano-30b-a3b` once the omni candidate is verified.

## Prometheus-side durable prefetch

Started on Prometheus over wired `eno1` as root systemd transient work.

Main unit:

```text
lojix-prefetch-local-ai-toolkit-2026-06-01.service
```

Monitor unit:

```text
lojix-prefetch-local-ai-toolkit-monitor-2026-06-01.service
```

Work directory:

```text
/var/tmp/local-ai-toolkit-prefetch-2026-06-01
```

Files in that directory:

- `prefetch.sh` — sequential `nix store prefetch-file --json` downloader.
- `urls.tsv` — pinned Hugging Face URLs.
- `progress.log` — live start/done/failure log.
- `results.jsonl` — per-artifact hashes and realized store paths when each finishes.
- `monitor.log` — ten-minute status snapshots while the main unit is active.

The queued prefetch set is:

- Qwen3-Coder-Next Q5_K_M: 4 GGUF shards.
- Gemma 4 E4B UD-Q8_K_XL and `mmproj-F16`.
- Nemotron 3 Nano Omni 30B-A3B Reasoning UD-Q4_K_XL and `mmproj-F16`.
- NVIDIA Parakeet TDT 0.6B v3 `.nemo`.
- Qwen3 Embedding 8B: 4 safetensor shards.
- Qwen3 Reranker 8B: 5 safetensor shards.
- FLUX.2 Klein 4B Q5_K_M GGUF.

Initial status after dispatch: main prefetch unit active; first artifact in progress; result file still empty.

## Next actions

1. Monitor the Prometheus prefetch unit until it exits.
2. Read `results.jsonl` and collect the SRI hashes.
3. Add only the llama-router-compatible GGUF winners to `CriomOS-lib/data/largeAI/llm.json` with explicit quantization suffixes.
4. Keep non-llama runtime models — Parakeet, Qwen embedding/reranker, FLUX — out of `llm.json` until their serving/runtime homes are designed.
5. After model inventory edits, repin CriomOS-home and deploy Home so Pi can select the new IDs.
