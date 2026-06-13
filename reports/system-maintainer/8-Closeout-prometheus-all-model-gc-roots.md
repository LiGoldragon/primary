---
variant: Closeout
primary-topic: prometheus
secondary-topic: model-gc-roots
---

# Prometheus all-model GC roots addendum

## Correction

After the initial Prometheus Nix store cleanup, explicit manual GC roots existed only for the three Gemma 4 keep/use variants:

- `gemma-4-26b-a4b-ud-q4-k-xl`
- `gemma-4-31b-ud-q4-k-xl`
- `gemma-4-26b-a4b-ud-q8-k-xl`

The rest of the model catalog was still safe during that GC because the current system generation rooted the llama-router model directory and presets. However, the user's intended safety bar was stronger: model files should have explicit GC roots before cleanup. This addendum records the corrected state.

## Roots added

Root directory:

- `/nix/var/nix/gcroots/criomos-largeai-models/`

Aggregate roots now include:

- `all-current-models-dir` — the current llama-router `--models-dir` store path.
- `all-current-presets` — the current llama-router presets file, which carries multimodal projector references.
- the three earlier individual Gemma keep/use roots.

Individual model/projector roots now exist under:

- `/nix/var/nix/gcroots/criomos-largeai-models/all-current-models/`

Rooted names:

- `gemma-4-26b-a4b`
- `gemma-4-26b-a4b-bf16`
- `gemma-4-26b-a4b-ud-q4-k-xl`
- `gemma-4-26b-a4b-ud-q8-k-xl`
- `gemma-4-31b`
- `gemma-4-31b-bf16`
- `gemma-4-31b-ud-q4-k-xl`
- `gemma-4-31b-ud-q8-k-xl`
- `glm-4.7-flash`
- `gpt-oss-120b`
- `mmproj-F16.gguf`
- `nemotron-3-nano-30b-a3b`
- `nemotron-3-super-120b-a12b`
- `qwen3.5-122b-a10b`
- `qwen3.5-27b`
- `qwen3.6-27b`
- `qwen3.6-35b-a3b`
- `qwen3-8b`

The aggregate presets root is load-bearing because multiple projector files can share the same basename. The presets file keeps every current projector reference even where a human-readable individual root name would collide.

## Follow-up GC

After adding all-model roots, two more ordinary `nix store gc` passes were run:

| Pass | Deleted paths | Freed space |
|---|---:|---:|
| After full model roots | 2,159 | 30.9 GiB |
| Final convergence | 110 | 415.9 KiB |

Final `nix-store --gc --print-dead` returned zero paths.

## Final verification

- `prometheus-llama-router.service` is active.
- Aggregate model roots: 5.
- Individual model/projector roots: 18.
- Dead Nix paths after final GC: 0.
- Final observed filesystem state: about 855G used, 1000G free, 47% used.
