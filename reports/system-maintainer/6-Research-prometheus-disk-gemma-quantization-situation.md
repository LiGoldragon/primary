---
variant: Research
primary-topic: prometheus
secondary-topic: gemma-quantization
---

# Prometheus disk and Gemma 4 quantization situation

## Scope

Read-only analysis of Prometheus disk usage and the Gemma 4 model variants currently retained by the Nix-managed large-AI router. No files, Nix roots, profiles, or model declarations were deleted or changed.

## Host disk state

Prometheus is not in immediate disk pressure.

| Surface | Observed state |
|---|---:|
| Root Btrfs filesystem | 1.82 TiB device |
| Used | 1.15 TiB |
| Free by `df` / Btrfs statfs | about 681 GB |
| Use percentage | 64% |
| Btrfs unallocated | about 669 GiB |
| Nix database path count | about 122k paths |
| Nix metadata total `narSize` | about 1.26 TiB |
| Nix GC dry-run dead paths | about 54.5k paths |
| Nix GC dry-run dead `narSize` estimate | about 444 GiB |

The visible non-store data is small compared with the Nix store:

| Path / area | Size | Note |
|---|---:|---|
| `/home/li/Downloads` | 37 GiB | two Qwen GGUF downloads, not Gemma |
| `/var/log/journal` | 2.3 GiB | ordinary journal footprint worth periodic rotation, not the main problem |
| `/var/lib/llama` | 17 MiB | runtime state only; model weights are Nix-store managed |
| `/root` | 251 MiB | not material |

The largest Nix paths are model weights. Gemma BF16 shards, Qwen/GPT-OSS/Nemotron shards, and some older Q8 model paths dominate the top of the store. This is expected for a machine acting as the shared large-AI host.

## Nix roots and generations

The current system profile is generation 48. Generations 43 through 48 retain the current Gemma 4 BF16 roots, and `/run/current-system`, `/run/booted-system`, and `/nix/var/nix/profiles/system` all point at generation 48.

A future cleanup has two layers:

1. Change the model catalog so future generations stop rooting the unwanted Gemma variants.
2. After the replacement generation is deployed and accepted, old system generations can be pruned and GC can reclaim the unreferenced model paths.

Running GC today would also reclaim already-dead E4B Gemma artifacts: one E4B Q8 file, one E4B model directory, and one E4B projector, roughly 13.6 GiB by Nix metadata. Those were not deleted.

## Live large-AI router state

`prometheus-llama-router.service` is active. It runs llama.cpp router mode with:

| Setting | Value |
|---|---|
| `modelsMax` | 1 |
| `sleepIdleSeconds` | 300 |
| service memory high / max | 100G / 110G |
| loaded child at observation time | `gemma-4-26b-a4b-ud-q8-k-xl` |
| observed service memory | about 80.7G, peak about 93.8G |

The current loaded model being `gemma-4-26b-a4b-ud-q8-k-xl` matters: it is in active use, but it is not necessarily the best default. It is a high-quality 8-bit tradeoff; the upstream Gemma 4 guidance recommends Dynamic 4-bit as the starting point for the larger 26B-A4B and 31B models.

## Gemma 4 variants currently declared

The catalog contains legacy BF16 aliases plus explicit BF16 and UD quantized names. The two legacy BF16 aliases share the same underlying weights as the explicit `-bf16` names, so the catalog's nominal `sizeGB` double-counts them; the actual store does not duplicate identical BF16 shards for the alias and explicit name.

| Catalog model | Quantization | Catalog size | Actual role |
|---|---:|---:|---|
| `gemma-4-26b-a4b` | BF16 | 52 GB | legacy alias; currently the Pi default in CriomOS-home |
| `gemma-4-26b-a4b-bf16` | BF16 | 52 GB | explicit BF16 name, same weights as legacy alias |
| `gemma-4-26b-a4b-ud-q4-k-xl` | UD-Q4_K_XL | 17 GB | best daily-driver candidate |
| `gemma-4-26b-a4b-ud-q8-k-xl` | UD-Q8_K_XL | 28 GB | current live loaded model; quality-sensitive candidate |
| `gemma-4-31b` | BF16 | 63 GB | legacy alias |
| `gemma-4-31b-bf16` | BF16 | 63 GB | explicit BF16 name, same weights as legacy alias |
| `gemma-4-31b-ud-q4-k-xl` | UD-Q4_K_XL | 19 GB | best dense Gemma candidate |
| `gemma-4-31b-ud-q8-k-xl` | UD-Q8_K_XL | 35 GB | optional dense near-lossless candidate |

Actual unique Gemma 4 footprint, excluding duplicate alias accounting but including both 26B-A4B and 31B BF16, Q4, Q8 weights, is roughly 196 GiB for weights plus about 2.2 GiB of rooted Gemma projectors. The BF16 weights alone account for about 104 GiB of that.

## Quantization research summary

Sources checked:

- Unsloth Gemma 4 local-running guide: `https://unsloth.ai/docs/models/gemma-4`
- Unsloth Dynamic 2.0 GGUF guide: `https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs`
- llama.cpp quantization guide: `https://mintlify.wiki/ggml-org/llama.cpp/models/quantizing-models`

Key points from those sources:

- Unsloth's Gemma 4 guide says 26B-A4B runs at about 18GB for 4-bit and 28GB for 8-bit; 31B needs about 20GB for 4-bit and 34GB for 8-bit.
- Unsloth explicitly recommends Dynamic 4-bit as the starting point for larger Gemma 4 models.
- Unsloth frames 26B-A4B as the speed/quality tradeoff: MoE, 4B active parameters, faster than dense 31B.
- Unsloth frames 31B as the strongest Gemma 4 model if memory is available and slower inference is acceptable.
- Unsloth Dynamic 2.0 GGUFs are model-specific layer-selection quants intended to preserve quality under compression; they use KL divergence and task benchmarks rather than only nominal bit-depth.
- llama.cpp's generic guidance puts 4-bit K-style quants as the best balance for most production use, Q8 as near-original quality when enough memory is available, and BF16/F16 as full-precision/baseline territory rather than ordinary serving defaults.

The important conclusion: for Prometheus, BF16 is not the rational serving default. Q8 is already the near-lossless operational tier, and Dynamic 4-bit is the intended large-Gemma daily-driver tier.

## Recommended keep / use / let-go policy

### Keep and use first

| Model | Why |
|---|---|
| `gemma-4-26b-a4b-ud-q4-k-xl` | Best default candidate. It matches upstream's Dynamic 4-bit recommendation for large Gemma 4, has the MoE speed advantage, and is small enough to reduce router memory pressure. |
| `gemma-4-31b-ud-q4-k-xl` | Best dense Gemma candidate. Keep for “strongest Gemma 4” comparisons without paying Q8/BF16 storage and memory cost. |

If the goal is a compact but useful Gemma shelf, these two are enough: fast MoE daily driver plus stronger dense Q4.

### Keep only if there is a current quality-sensitive use case

| Model | Why |
|---|---|
| `gemma-4-26b-a4b-ud-q8-k-xl` | Current live loaded model. It is the best 26B-A4B quality tier short of BF16 and still much cheaper than BF16. Keep until Q4 is A/B tested for Pi/local-agent quality. |
| `gemma-4-31b-ud-q8-k-xl` | Optional maximum-quality dense Gemma serving tier. Keep only if “best Gemma answer quality” matters enough to justify 35GB and slower inference. |

The current live router has the 26B-A4B Q8 loaded and stable, so I would not remove it blindly. I would A/B the Q4 and Q8 26B-A4B variants on the actual Pi/local-agent tasks, then keep Q8 only if the difference is visible.

### Let go first

| Model / artifact | Why |
|---|---|
| `gemma-4-26b-a4b` legacy BF16 alias | It points at BF16 while the name hides quantization. It is also currently the Pi default; change the default before removing. |
| `gemma-4-26b-a4b-bf16` | BF16 is too expensive for ordinary serving; Q8 is the near-lossless operational tier. Removing the actual 26B-A4B BF16 weights would save about 47 GiB once no roots reference them. |
| `gemma-4-31b` legacy BF16 alias | Same alias problem: hides quantization and retains huge BF16 weights. |
| `gemma-4-31b-bf16` | Removing the actual 31B BF16 weights would save about 57 GiB once no roots reference them. |
| dead E4B Gemma artifacts | Already unrooted according to Nix GC dry-run; ordinary GC would reclaim about 13.6 GiB. |

Alias-only removal has zero disk effect if the explicit BF16 model remains. The disk win comes from removing the actual BF16 model entries and deploying a generation that no longer references their shards.

## Recommended next action, if cleanup is approved later

Do not delete by hand. Make a catalog change in `CriomOS-lib/data/largeAI/llm.json`, then deploy Prometheus through the normal system path.

Proposed catalog policy:

1. Change Pi/Home default from `gemma-4-26b-a4b` to `gemma-4-26b-a4b-ud-q4-k-xl`, or to Q8 only if the user explicitly wants quality over memory.
2. Remove the two BF16 legacy aliases.
3. Remove the explicit BF16 26B-A4B and 31B entries unless a benchmark-baseline use case is explicitly named.
4. Keep `gemma-4-26b-a4b-ud-q4-k-xl` and `gemma-4-31b-ud-q4-k-xl`.
5. Temporarily keep `gemma-4-26b-a4b-ud-q8-k-xl` because it is currently used; decide after A/B testing.
6. Drop `gemma-4-31b-ud-q8-k-xl` unless dense max-quality Gemma has a named user.
7. After deployment and acceptance, prune old Prometheus system generations, then run Nix GC.

Expected reclaim if this policy is implemented and old roots are pruned:

| Action | Approximate reclaim |
|---|---:|
| Remove Gemma 4 BF16 26B-A4B and 31B weights | about 104 GiB |
| Let existing dead E4B Gemma paths be GC'd | about 13.6 GiB |
| Also remove 31B Q8 | about 32.6 GiB |
| Also remove 26B Q8 after A/B says Q4 is enough | about 25.7 GiB |

Conservative cleanup therefore saves about 118 GiB. Lean cleanup saves about 176 GiB. The larger 444 GiB Nix GC dry-run number includes many non-Gemma dead paths and should be treated as a separate system-generation/cache cleanup discussion.
