---
variant: Closeout
primary-topic: prometheus
secondary-topic: nix-store
---

# Prometheus Nix store cleanup with model roots

## Result

Prometheus Nix GC completed after explicit GC roots were created for the Gemma 4 keep/use set. No catalog edit was performed and no manual store-path deletion was used.

## Model roots created first

Root directory:

- `/nix/var/nix/gcroots/criomos-largeai-models/`

Rooted model directories:

| Model | Closure size |
|---|---:|
| `gemma-4-26b-a4b-ud-q4-k-xl` | 15.8 GiB |
| `gemma-4-31b-ud-q4-k-xl` | 17.5 GiB |
| `gemma-4-26b-a4b-ud-q8-k-xl` | 25.7 GiB |

Each root was verified with Nix root discovery before GC and again after GC.

## Cleanup performed

Three ordinary `nix store gc` passes were needed to converge after newly-dead paths appeared between passes.

| Pass | Deleted paths | Freed space |
|---|---:|---:|
| First | 53,738 | 411.8 GiB |
| Second | 879 | 2.0 GiB |
| Final | 18 | 4.4 MiB |
| Total | 54,635 | about 413.8 GiB |

Final `nix-store --gc --print-dead` returned zero paths.

## Disk state

| Mount family | Before | After |
|---|---:|---:|
| Btrfs root / nix / home / var | 1.2T used, 676G free, 64% | 842G used, 1012G free, 46% |

The reported free-space gain is larger than the Nix log's exact freed total because Btrfs accounting also changed as unused links and metadata settled.

## Runtime verification

- `prometheus-llama-router.service` remained active after cleanup.
- The three rooted Gemma keep/use model directories remained present and queryable by `nix path-info`.
- The final GC dead-path count was zero.

## Scope boundary

This cleanup did not implement the earlier catalog recommendation to remove BF16 Gemma entries or legacy aliases. Those entries remain live because the current system generation still references the current catalog. Reclaiming that model-specific BF16 footprint requires a source catalog change in `CriomOS-lib/data/largeAI/llm.json`, a Prometheus redeploy, acceptance of the new generation, and then a later generation prune / GC.
