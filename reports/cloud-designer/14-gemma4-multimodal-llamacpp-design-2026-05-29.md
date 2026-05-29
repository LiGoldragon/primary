# 14 · Gemma 4 multimodal on llama.cpp — research + deployment design (2026-05-29)

Research + design for running **Gemma 4 fully multimodal** on prometheus
(records 1023, 1206), prompted by the operator's finding that deployed
`llama-cpp-8470` fails with `unknown model architecture: 'gemma4'` and
that a bump attempt to `b9404` "did not build" (reverted as CriomOS
`c66599e8`). cloud-designer researches + designs here; the **operator
implements** the llama.cpp package fix.

## TL;DR for the operator

1. **`b9404` is the right version — do not hunt for another build.** It
   is llama.cpp's *latest* tag (published 2026-05-29) and postdates every
   Gemma-4 fix. The failure is a **Nix packaging** problem, not a missing
   feature. `b8470` (2026-03-22) simply predates Gemma 4's launch
   (2026-04-02), so it has no `gemma4` arch at all.
2. **The build break is almost certainly the stale `npmDepsHash`.** The
   reverted attempt bumped `version`/`tag`/`src.hash` but left
   `npmDepsHash = sha256-DxgUDVr+…` untouched. llama.cpp's server WebUI
   npm lockfile changed across 2+ months (Mar→May), so the fixed-output
   npm-deps derivation mismatches → build fails. Recompute it the same
   way we just did for the pi package: set `npmDepsHash =
   pkgs.lib.fakeHash`, build, read the `got: sha256-…` from the mismatch
   error, paste it back. **Better: we run with `--no-webui`** — if the
   nixpkgs `llama-cpp` expression exposes a "don't build the WebUI"
   path, take it and the npm dep (and its hash churn) disappears entirely.
3. **Second risk: base-expression drift.** The package is
   `(pkgs.llama-cpp.override { vulkanSupport = true; }).overrideAttrs
   { src = b9404; … }` — it grafts a brand-new source onto whatever
   `llama-cpp` build expression CriomOS's pinned **nixpkgs** carries. If
   that nixpkgs is old, b9404's CMake/layout may not match. Check
   `pkgs.llama-cpp.version`; if it's far behind, bump CriomOS's nixpkgs
   input (or adopt a llama.cpp flake) so the build recipe matches b9404.
4. **Stay on Vulkan.** Confirmed correct for Strix Halo (below). Do not
   switch to ROCm.

## Hardware reality — prometheus is Strix Halo (gfx1151) on Vulkan

The package comment ("Vulkan — faster and more stable than ROCm on Strix
Halo (gfx1151)") is right and the research backs it hard:

- **Vulkan RADV is the reliable path** on Ryzen AI Max+ / Strix Halo.
  Reported Gemma-4-26B-A4B: ~48-52 tok/s generation, ~1142 tok/s prompt
  on 128 GB unified memory with *standalone* llama.cpp Vulkan.
- **ROCm is the wrong choice here** for two independent reasons: (a) ROCm
  doesn't officially support Strix Halo (Preview, PyTorch-only), and
  (b) llama.cpp issue **#21416** — *"With ROCm the gemma-4-26B-A4B model
  causes endless loop"* (our exact model). Vulkan sidesteps both.
- **Standalone llama.cpp beats Ollama's vendored copy** (~52 vs ~34 tok/s)
  because Ollama lagged on Vulkan Wave32 flash-attention + graphics-queue
  fixes. We build standalone + latest, so we get those — another reason
  `b9404` is the target.
- `llm.nix` sets `HSA_OVERRIDE_GFX_VERSION=11.5.1`. That's a **ROCm/HIP**
  env var; with a Vulkan build it's inert. Harmless, but it's dead config
  — fine to leave, worth a comment so no one thinks ROCm is in play.
- Memory: both models are **BF16** (31B ≈ 63 GB, 26B-A4B ≈ 52 GB) and the
  service caps at `MemoryMax=110G`. They cannot **both** be resident; the
  router (`--models-max`) must keep it to one large model at a time. KV
  cache at the configured 32K ctx is modest; one model + KV + mmproj fits.

## Known Gemma-4 bugs in llama.cpp — all FIXED in b9404

| Issue | Symptom | Fixed | In b9404? |
|---|---|---|---|
| #21321 | generates `<unused24>` tokens (chat-template/tokenizer) | 2026-04-07 | yes |
| #21416 | ROCm → endless loop on 26B-A4B | 2026-04-08 | yes (and we use Vulkan) |
| #21497 | **26B-A4B cannot process images** (our model + our goal) | **2026-05-10** | yes |
| post-launch | chat-template fixes, logit softcapping, tool-call parsing | through April | yes |

So multimodal on 26B-A4B specifically was broken until 2026-05-10 and is
only available on a build newer than that — `b8470` could never have done
vision even if it knew `gemma4`. `b9404` clears all of these.

Still open upstream (not blocking us): `convert_hf_to_gguf.py` doesn't yet
recognize `Gemma4AssistantForCausalLM` (the speculative-decoding *drafter*
models) — irrelevant; we run the base instruct models, and we consume
prebuilt Unsloth GGUFs rather than converting.

## Multimodal setup — what "all features" means here

Capability by model (HF/Google): **our 31B-dense and 26B-A4B-MoE do text
+ image + video; they do NOT do audio** (audio is E2B/E4B only). So "all
features" for *our* models = vision (images) + video-as-frames + the long
context, not speech.

- **Vision** rides the **mmproj** projector GGUF. We already fetch it
  (`mmproj-F16.gguf` per model) and wire it as `mmproj = <path>` in the
  per-model preset (`llm.nix` `mkModelPreset`). The OpenAI surface
  (`/v1/chat/completions` with `image_url` content parts) is what Pi/
  clients use — fully supported once on b9404.
- **VERIFY the router-mode preset path.** Our deploy uses llama-server
  *router* mode (`--models-dir` + `--models-preset` + `--models-max`),
  not a single `--model … --mmproj …` invocation. The single-model docs
  all show the `--mmproj` *flag*; that the `mmproj = <path>` **preset
  key** is honoured per-model in router mode is the one thing the docs
  don't confirm. This is exactly report 9's "vision runtime-unverified."
  Operator must confirm an actual image request returns a real answer
  (not "model is text-only"); if the preset key is ignored, the fallback
  is a per-model `--mmproj` or a non-router single-model service.
- **Vision tuning:** mmproj is GPU-offloaded by default; `--no-mmproj-offload`
  only if VRAM-pressured (not our case — unified memory). Image OCR /
  charts / document / UI / handwriting / pointing all come "for free" with
  the vision tower; no extra flags.
- **Video** = client sends a sequence of frames; no server flag, but the
  client (Pi) must sample frames. Lower priority than images.

## Recommended runtime settings (Google/Unsloth defaults)

- **Sampling: `temp 1.0`, `top-p 0.95`, `top-k 64`.** Gemma 4 is tuned
  for these; lower temp degrades it. **Disable repetition/presence
  penalty** (1.0 / off) — only enable if you observe looping.
- **Context:** model max is **256K** (31B/26B); we set **32K** (`ctxSize`),
  a sane memory/latency default. Raise per need; 256K BF16 KV is large.
- **Thinking mode:** Gemma 4 has internal reasoning. Server-side toggle is
  `--chat-template-kwargs '{"enable_thinking":false}'`. (Pi's
  `defaultThinkingLevel` is a *client* hint; the server flag is the real
  control.) Decide one policy and set it on the router, not per-call.
- **Avoid the CUDA-13.2 runtime** for GGUFs (poor outputs) — N/A for us
  (Vulkan), noted for completeness.

## Design flag — quantization ladder (BF16 is the odd choice)

Record 1033 chose **BF16** for both ("biggest that fits, max quality").
The ladder, per-model approximate GGUF sizes, and quality:

- **BF16** (16-bit, what we run): 31B ≈ 63 GB, 26B ≈ 52 GB. Reference
  quality, but largest + slowest (bandwidth-bound).
- **Q8_0** (8-bit): ≈ 33 GB / 27 GB — half BF16. Quality is
  **effectively indistinguishable** from BF16 (perplexity delta near
  noise). So BF16 buys essentially nothing over Q8 for inference —
  **Q8 strictly dominates BF16**: same quality, half the memory +
  bandwidth, ~2× faster on the dense 31B.
- **UD-Q4_K_XL** (Unsloth dynamic 4-bit): ≈ 18-20 GB / 15 GB — a quarter
  of BF16. Keeps precision-sensitive layers higher and squeezes the rest;
  quality typically within ~1% of BF16 for these sizes. The sweet spot.
- Below Q4 (Q3/Q2): quality degrades steeply — avoid.

Gemma has historically been a touch **quant-sensitive**, which is exactly
why the *dynamic* quants exist — use **UD-Q4_K_XL**, never a plain
`Q4_0`. (Unsloth's own split confirms: Q8_0 for the tiny E2B/E4B,
UD-Q4_K_XL for our 26B/31B.)

**Recommendation: drop BF16** — it's dominated by Q8 (no quality gain,
2× the cost). For daily use, **UD-Q4_K_XL**: ~4× smaller + faster, both
models resident under 110 G, room for bigger context. If a max-fidelity
option is *also* wanted, the router can serve **both** quants as separate
named models (e.g. `gemma-4-31b` at Q4_K_XL + `gemma-4-31b-q8`) — cost is
the extra store path + one-model-at-a-time loading + a busier picker, and
Q8's edge over dynamic-Q4 is small for these sizes, so it's optional.
Psyche call (1033 = BF16 honoured; usability = Q4_K_XL). mmproj stays F16
either way.

## Verification checklist (operator, after the build lands)

- [ ] `llama-server` starts on b9404 (Vulkan) and loads `gemma-4-31b` /
      `gemma-4-26b-a4b` without `unknown model architecture`.
- [ ] A **text** completion succeeds with the api-key (the auth path is
      already fixed client-side — report 13).
- [ ] An **image** request (`image_url`) returns a real description —
      confirms the router-mode `mmproj` preset key works (#21497 + the
      router-path unknown).
- [ ] No `<unused24>` leakage in output (regression check on #21321).
- [ ] No runaway/looping generation (sampling defaults applied).
- [ ] Memory stays under `MemoryMax` with one large model + 32K KV.

## Sources

- HF: *Welcome Gemma 4* (huggingface.co/blog/gemma4); Google model card
  (ai.google.dev/gemma/docs/core/model_card_4).
- llama.cpp: `docs/multimodal.md`; issues #21497 (26B-A4B images, fixed
  2026-05-10), #21321 (`<unused24>`, 04-07), #21416 (ROCm loop, 04-08);
  build tags b8470 (03-22) / b9404 (05-29, latest).
- Unsloth *Gemma 4 — How to Run Locally* (sampling, quant, thinking).
- Strix Halo: ggml-org #13565 (HIP poor on gfx1151), ollama #15601
  (Vulkan FA gap), Framework/strix-halo perf threads.
- AMD *Day-0 Support for Gemma 4 on AMD* (page currently unreachable;
  URL retained for the operator).

## Anchors

- Package: `CriomOS/packages/llama-cpp-strix-halo.nix`; service +
  router + mmproj wiring: `CriomOS/modules/nixos/llm.nix`; model specs:
  `CriomOS-lib/data/largeAI/llm.json` (de676a8e).
- Intent: 1023 (full-multimodal deploy), 1032/1033 (biggest-that-fits,
  BF16 both), 1206 (all features). Prior: report 9 (vision unverified),
  report 13 (client auth fixed).
