# Locally served AI models: status, 2026-09-25 night

Read-only account for the morning book. Nothing was changed, pulled, restarted or generated. Probes ran at 2026-09-25 21:26–21:30 local (-06:00) on ouranos, Prometheus and zeus. Each claim is marked **observed** (seen this session), **inferred**, or **unknown**.

## In one paragraph

What the living last asked for (2026-09-16) was to keep only Gemma and the latest Qwen on Prometheus, remove everything else, and keep at least one model at all times. That wish has not reached the running machine. The shared model data file (CriomOS-lib `data/largeAI/llm.json`) was cut on main to **one** model, Qwen3.5-122B-A10B, which also dropped Gemma. But CriomOS main still pins CriomOS-lib at the old August revision, which lists 17 models. Prometheus (NixOS 26.11, system-55, activated 2026-09-24, rebooted 21:15 tonight) therefore still serves all **17** models from its llama.cpp router on port 11434, and 707 GB of GGUF weight files remain in its Nix store. A Qwen-only Prometheus system was built on 2026-09-17 (realize-18) but never activated. Its leftover GC root on ouranos pins 72 GB of Qwen weights on a disk that is 92% full. Nothing from the 2026-09-15 "latest models" wish (Motif, Laguna, newest Qwen) is on main. It exists only as an unmerged CriomOS proposal branch.

## 1. What the living said, newest first

**2026-09-25 ~22:10, STT, to 88475f** (`flows/da88cf/vision/prometheus.md`):

> We had changed the models we wanted to have serve locally on the AI side but I'don't know what the status of that is. You can present that to me in the book in the morning.

**2026-09-18, to 1ac573** (`flows/1ac573/vision/operational-privateLayerCoreLayer.md`):

> Let's develop the private aspect of all this so that we have a private repo for the soul, the core layer. Let's set up the private layer, the core layer.

**2026-09-17, typed, to 9993b5** (`flows/9993b5/vision/powerLevels.md`):

> And what are the open-source models that were contenders for the high, medium, and low power levels? It's a power level, right? High because it's literally how much energy we're spending. High, medium, or low power for the open-source models: all the contenders, why, what their strengths are, their sizes, and what could actually run on my node here of the small ones

**2026-09-16, typed, to f55ec8.** This is the change the living refers to. The verbatim text comes from the f55ec8 Claude transcript, 17:46:33Z. The log keeps only a paraphrase (`flows/f55ec8/log.md`: "keep Gemma and the latest Qwen…").

> Yeah, we almost don't want most of these models. Let's just keep Gemma and the latest Quan that we have, maybe, and remove everything else. Let's get the best model that we've determined on our own research to be the only dependency, and then we can garbage collect. Just keep one model at all times, right? Let's pick one that you keep, at least, so that the machine remains operative. After your garbage collection, it still has a model to operate from. Tell me which models you picked, and we don't need Nematron. I think that's a pretty garbage model, or Lama or any of that.

It came eleven minutes after this message (transcript, 17:37:57Z):

> Let's get rid of all the AI models and the AI model downloads that we aren't going to use anymore. Let's change the criome's definition. Redeploy a new version on Prometheus. Disable the models if you can't build, just so you can detach and unlink all of these old models.

**2026-09-16, typed, to f55ec8** (`flows/f55ec8/vision/modelRoles.md`):

> …there's going to be another one: open source, right? Is it K3? Is it Motif? Is it Laguna Medium? Is Laguna Medium out, or something really large, actually really wise?

**2026-09-15, typed, to 05c604** (`flows/05c604/vision/cluster.md`):

> …getting the latest models that we talked about hosting, like: Motif; Laguna; the types and sizes that fit; the latest Quinn [Qwen]; all of the best performers in different areas

**2026-09-14, STT** (`flows/e1953c/vision/privateLayer.md`):

> The private part is because the whole idea is that it can be self-hosted, so it has to stay on self-hosted or self-hostable open-weight models.

**2026-09-14, typed artifact comment** (`flows/6cc91b/vision/thirdModel.md`): "Kimi K3 on OpenCode sounds great. Let's set that up." This is a **hosted** third seat through a provider, not local serving.

**2026-09-13, STT** (`flows/024bc7/vision/effort.md`, `flows/bcd02a/notion/prometheus.md`):

> …a thread rolling on Prometheus with the most doubtful model… either Laguna from Laguna Small or this Korean message motif 3, the version that runs on Prometheus, the AMD Strix with 128 GB of unified memory.

**2026-09-13, STT** (`flows/024bc7/vision/soul.md`): "We're also going to run these speech-to-text models on Prometheus…"

How the wish changed (inferred):

- **2026-09-13 to 09-15:** add new models (Motif, Laguna, latest Qwen) to Prometheus.
- **2026-09-16:** trim hard, keep Gemma plus the latest Qwen, one model at minimum, and drop Nemotron and Llama.

Two gaps between those words and what was done:

1. **Gemma was dropped.** The implementing subflow kept Qwen only. f55ec8's log records "Gemma's return on their word" as a question put to the living. No later answer was found in Claude or Codex transcripts (unknown whether one was given elsewhere).
2. **The Qwen kept is not the newest one.** "The latest Qwen that we have" would read as a Qwen3.6 entry (`qwen3.6-35b-a3b` or `qwen3.6-27b`, both in the old list). The subflow kept `qwen3.5-122b-a10b`, the biggest model and the one already loaded at startup (inferred reading of the living's words).

The private layer, which would serve its model through the open-source seat, is still NOT ACTIVE per CLAUDE.md.

## 2. What is declared

**Cluster data.** Observed in goldragon `origin/main` 8c4d03d, `cluster-definition.datom`. The Horizon enum lives in horizon-rs `lib/ethos/horizon.ethos` (`LargeAi.NoSettings`).

- **prometheus:** `[ Center LargeAi Router TailnetClient NixBuilder.Some.6 NixCache VmHost… ]`. Metal: GMKtec EVO-X2, 128 GB. This is the only `LargeAi` node.
- **ouranos:** Edge, LowPower, NextGeneration, …, OpenCodeTesting. No LargeAi.
- **zeus:** Edge, LowPower, HardwareVideo. No LargeAi.
- **tiger, balboa:** no LargeAi.

**The serving module.** Observed in CriomOS `origin/main` d193baf, `modules/nixos/llm.nix`:

- The only switch is `mkIf behavesAs.largeAi`. There is no enable option of its own.
- It runs `<node>-llama-router.service`, which is `llama-server` in router mode: `--host ::`, `--port` from the manifest's `serverPort` (11434), firewall opened, `--models-max 1`, `--sleep-idle-seconds 300`, and an API key from sops (`localLlmApiToken`).
- Resource settings: `MemoryMax=110G`, `HSA_OVERRIDE_GFX_VERSION=11.5.1`.
- The package is `packages/llama-cpp-strix-halo.nix`, which is llama.cpp with **Vulkan** (not ROCm).
- GGUF files are fetched into the Nix store by `pkgs.fetchurl` at build time, from `inputs.criomos-lib + "/data/largeAI/llm.json"`.
- GPU tuning: `modules/nixos/metal/default.nix:531` sets TTM `pages_limit` on `center` nodes so the GPU can use about 5/6 of unified memory.

**The model list.** Observed in CriomOS-lib `data/largeAI/llm.json`:

| Revision | Where it counts | Models |
|---|---|---|
| `6e3bcb0` (2026-08-12) | **pinned by CriomOS main `flake.lock`** | 17: qwen3.5-122b-a10b (loaded at startup), gpt-oss-120b, nemotron-3-super-120b-a12b, glm-4.7-flash, nemotron-3-nano-30b-a3b, qwen3.5-27b, qwen3.6-35b-a3b, qwen3.6-27b, qwen3-8b, 8 gemma-4 variants (31b and 26b-a4b; bf16, ud-q4-k-xl, ud-q8-k-xl; with a vision projector file) |
| `c74b222` (2026-09-16), CriomOS-lib main | not consumed by any CriomOS main build | 1: qwen3.5-122b-a10b |

**Branches not merged** (observed):

- CriomOS `proposal/348e7b-prometheus-single-model` 9d93d62 pins the Qwen-only catalog, but the branch also carries Prosody and other work (38 files).
- CriomOS `proposal/5f4fea-model-presets` 0cb5152 adds Laguna S 2.1 UD-Q4_K_M (68 GiB) and Qwen3.8-27B Q8_0 (26.6 GiB) with verified hashes, behind `enableProposalModels = false`. In it, Laguna XS and Motif 2 are disabled, Motif 3 is a comment only, the Laguna license awaits the living's confirmation, and zeus serves nothing.

**Clients in the user environment.** Observed in CriomOS-home `origin/main` 478b4ea0:

- `profiles/max/browser-use.nix` hard-codes `localVisionModel = "gemma-4-26b-a4b"` at `http://<largeAi node>:11434/v1`.
- `profiles/min/pi-models.nix` (deprecated) reads the same manifest.
- `profiles/min` installs the `llama-cpp` command-line tool. It fetches no model weights.

**Inferred:** with the Qwen-only list, browser-use would point at a model the router no longer has. The Gemma drop breaks a declared client.

## 3. What is deployed and running

**Prometheus.** Observed.

- NixOS 26.11.20260813; `system -> system-55` (2026-09-24 21:03), which is also the booted system; up since 21:15 tonight.
- GPU: AMD Strix Halo Radeon 8060S, `/dev/kfd` present. The router's log shows `Vulkan0 : AMD Radeon 8060S (RADV STRIX_HALO) (109568 MiB)`. No `nvidia-smi` or `rocm-smi`.
- `prometheus-llama-router.service` is active and running; `*:11434` is listening. The router started at 21:15:50 and "Loaded 17 local model presets".
- Listing only, no generation: `curl localhost:11434/v1/models` returned HTTP 200 with 17 models. `qwen3.5-122b-a10b` is `sleeping` (it loaded at start and went idle). The other 16 are `unloaded`. `/health` returned 200.
- The listing answered **without the API key** and exposes each model's launch arguments. Inferred: llama.cpp does not require the key for listing.
- There is no ollama, vllm or sglang.
- Model storage: 32 GGUF files in the store root, **707 GB**. They are held by the current system's `llm-models-dir` and by 24 older flat roots `/nix/var/nix/gcroots/llm-*` from March 2026. Those older roots cover DeepSeek-R1-Distill-Llama-70B, llama-3.2-1b, Qwen3.5-35B Q8, Nemotron and others, some of which are not in any list.
- `/var/lib/llama` is 8.7 MB. `/nix` has 1016 GB free of 1.9 TB, meaning cleanup has happened since the 2026-09-16 witness.
- **Inferred:** Nix garbage collection alone cannot free the model files while system-55 and the `llm-*` roots hold them.

**ouranos.** Observed.

- No model unit, nothing listening on the probed ports, Intel Meteor Lake GPU only.
- Holds 72 GB of Qwen3.5-122B shards, rooted only by `/home/li/.local/state/secondary-348e7b/realize-18/candidate-root`. That root points to the never-activated Qwen-only Prometheus system of 2026-09-17.
- `/` is at 92% (76 GB free).

**zeus.** Observed. No model unit, no GGUF, Intel UHD GPU, 15 GB RAM. This matches the catalog's "zeus serves nothing".

## 4. Gap table

| Model wanted | Wanted when | Declared where | Deployed where | Running | Serving tested (listing only) |
|---|---|---|---|---|---|
| Gemma (4) | 2026-09-16 keep | Old list only (8 variants). **Removed** on CriomOS-lib main | Prometheus, via the old pin | Listed, unloaded | Listed; generation not tested |
| Latest Qwen | 2026-09-15 add; 09-16 keep | qwen3.5-122b on both lists. qwen3.6-* in the old list only. Qwen3.8-27B on proposal 5f4fea only | Prometheus: 3.5-122b, 3.6-27b, 3.6-35b. 3.8: none | 3.5-122b sleeping (loaded at start) | Listed |
| One model kept at all times | 2026-09-16 | Qwen3.5-122B, loaded at startup, in both lists | Prometheus | Yes | Listed |
| Nemotron, Llama: remove | 2026-09-16 | Still in the pinned list. Llama/DeepSeek only in old roots | Prometheus | Listed (Nemotron); weights rooted | Listed |
| gpt-oss, GLM, qwen3-8b and the rest: remove | 2026-09-16 ("everything else") | Pinned list | Prometheus | Listed | Listed |
| Laguna S / XS | 2026-09-13 / 09-15 | Proposal 5f4fea only (S enabled by flag; XS disabled) | None | No | No |
| Motif 3 | 2026-09-13 / 09-15 | Comment only; does not fit (Q4 about 193 GB); llama.cpp support unmerged (per the catalog) | None | No | No |
| Kimi K3 (third seat) | 2026-09-14 | Hosted provider, not local | Not applicable | Unknown | Not tested |

## 5. What remains

These are declared changes. None were made.

1. **Decide the list.** It needs the living's word, since the living's wording and the current main list disagree:
   - (a) Gemma: add back one Gemma 4 variant? `gemma-4-26b-a4b` is the one browser-use expects.
   - (b) Which Qwen: 3.5-122b (the current one), 3.6-35b-a3b, or Qwen3.8-27B from 5f4fea?
   - (c) Add Laguna S now or not?
   - Edit: CriomOS-lib `data/largeAI/llm.json` on main (entries copied back from `6e3bcb0` or from 5f4fea's sources).
2. **Bump the CriomOS pin.** CriomOS `flake.lock` input `criomos-lib` moves from `6e3bcb0` to the CriomOS-lib main head (`c74b222` or later), landed on CriomOS main. Without this, every Prometheus deploy (including the pending one this flow's gap subflow is tracing) carries all 17 models again. This is what failed deployment 31 on 2026-09-24 when ouranos tried to pull Nemotron, Qwen, Gemma and GLM.
3. **If Laguna or Qwen3.8 are wanted,** either merge 5f4fea's `llm.nix` switch and set `enableProposalModels`, or better, move those entries into the one manifest in CriomOS-lib so the data stays in one place.
4. **Deploy to Prometheus**, built on Prometheus, through Lojix from CriomOS main.
5. **Drop the old roots on Prometheus.** After the new system is active: remove the 24 flat `/nix/var/nix/gcroots/llm-*` roots (they are hand-made, not declared), retire the old system generations, then collect garbage. This is expected to free most of the 707 GB (inferred).
6. **Clean up ouranos.** Drop the stale `secondary-348e7b/realize-18/candidate-root` (72 GB of Qwen, disk at 92%). This belongs to the disk-hygiene owner, the secondary.
7. **CriomOS-home:** make browser-use's model name follow the manifest, or keep a Gemma entry.
8. **Optional:** put an auth proxy in front of the router, or confirm that an unauthenticated model listing on `[::]:11434` is acceptable.

**Unknowns:**

- Whether the living answered the Gemma question anywhere not searched.
- Which Qwen "latest" means.
- Whether Laguna's OpenMDW license is accepted.
- Why realize-18 (Qwen-only) was never activated. The secondary's log ends at "Realize17 running", and system-55 came from the old pin.
- Whether the speech-to-text models on Prometheus (09-13) are still wanted. None are declared.

## Sources

- Vision: `flows/da88cf/vision/prometheus.md`; `flows/f55ec8/vision/modelRoles.md`; `flows/05c604/vision/cluster.md`; `flows/9993b5/vision/powerLevels.md`; `flows/1ac573/vision/operational-privateLayerCoreLayer.md`; `flows/e1953c/vision/privateLayer.md`; `flows/6cc91b/vision/thirdModel.md`; `flows/024bc7/vision/{effort,soul,thirdModel}.md`; `flows/bcd02a/notion/{prometheus,models}.md`.
- Transcript: `/home/li/.claude/projects/-home-li-wt-github-com-LiGoldragon-primary-claude-successor-efa157-jj--claude-worktrees-claude-successor-f55ec8/f55ec8ce-4aa1-45d6-9a3e-dc5bc4ed0764.jsonl`, user turns 2026-09-16T17:37:57Z and 17:46:33Z. The e5141130 transcript, 2026-09-24T20:42Z, has the relay of deployment 31's failure.
- Logs and reports: `flows/f55ec8/log.md`; `flows/f55ec8/reports/prometheusDefinition.md`; `/home/li/secondary/flows/57a7aa/reports/modelCatalog.md`; `/home/li/secondary/flows/348e7b/{log,branches}.md`.
- Repos (fetched tonight): CriomOS `origin/main` d193baf (`modules/nixos/llm.nix`, `modules/nixos/metal/default.nix:531`, `flake.lock`), `origin/proposal/348e7b-prometheus-single-model` 9d93d62, `origin/proposal/5f4fea-model-presets` 0cb5152 (`reports/0042-model-preset-proposal.md`); CriomOS-lib `data/largeAI/llm.json` at `6e3bcb0` and `origin/main` c74b222; CriomOS-home `origin/main` 478b4ea0 (`modules/home/profiles/max/browser-use.nix`, `profiles/min/{default,pi-models}.nix`); goldragon `origin/main` 8c4d03d (`cluster-definition.datom`).
- Host probes (read-only, script at `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/local-models/probe.sh`, output `prometheus.txt` beside it): systemctl, ss, pgrep, lspci, free, `/nix/store` GGUF listing, `du`, gcroots, `systemctl show`, presets file, `curl /health` and `/v1/models`, the router's journal for this boot, `last -x reboot`; `nix-store -q --roots/--requisites` on ouranos.
