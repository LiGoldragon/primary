# 5 · Execution — main-path push (supersedes the "coordinate" lean in file 4)

File 4 recommended coordinating with system-operator. The psyche chose
**push through on main now** (spirit 1022) and **install both big
multimodal models** (1033), correcting the earlier small-Gemma choice
(1032: "biggest that fits, not the small-ass model"). This file records
what was actually built and deployed.

## Model choice

`gemma-4-E4B` (4B) was rejected as too small. prometheus has ~110 GB
and serves one model at a time, so quant/size was never a fit
constraint. Installed BOTH, at full **BF16**, both multimodal:

- **`gemma-4-31b`** — 31B dense, max quality (~62.6 GB). Slow on
  Strix Halo (memory-bandwidth-bound, ~4 tok/s rough).
- **`gemma-4-26b-a4b`** — 26B MoE, only ~4B active/token, so big-model
  capability at near-4B latency (~5–7× the dense). The better fit for a
  live browser actor.

Vision via `mmproj-F16.gguf` (~1.2 GB) for each.

## The zero-download hash technique

The big win: no prefetch download was needed. HuggingFace exposes each
LFS file's **content sha256** in its git-LFS metadata, which is exactly
what nix `fetchurl` verifies. Pulled all shard + mmproj hashes from the
tree API, **verified the technique** against an existing inventory entry
(qwen3-8b's llm.json sha256 matched its HF LFS oid exactly), and used
the existing `multi-shard` schema. The deploy downloads each file once,
on prometheus. (An earlier fetchHfModel snapshot-hash attempt was
abandoned — it tried to substitute the weights into the LOCAL store;
killed, confirmed nothing landed locally.)

## What changed, per repo (all pushed)

- **CriomOS-lib** `main` → `de676a8e`:
  - `185bed88` landed `fetchHfModel` + `nix-prefetch-huggingface` +
    openssl-free `criome-mint-llm-api-token` (from the prefetch branch).
  - `de676a8e` added `gemma-4-31b` + `gemma-4-26b-a4b` to
    `data/largeAI/llm.json` (multi-shard BF16 weights + an `mmproj`
    field, URLs pinned to commit, sha256 from LFS metadata).
- **CriomOS** `main` → `699c7a66`: `modules/nixos/llm.nix`
  - `apiKeyFile` now points at `config.sops.secrets.localLlmApiToken.path`.
  - Added the `sops.secrets.localLlmApiToken` declaration (binary,
    owner llama, restartUnits the router).
  - Added `mkMmprojFile` + a `mmproj = <path>` line in the per-model
    preset for models carrying an `mmproj` field.
  - Dropped the empty-api-key tmpfiles rule; bumped the criomos-lib lock.
- **lojix-cli** (rebuilt, compiles): `src/artifact.rs` now exposes
  `localLlmApiToken = ./local-llm-api-token.sops` in the generated
  secrets flake (mirrors the `routerWifiSaePasswords` pattern). The
  deploy used this rebuilt binary; its generated `secrets` input carried
  the token (confirmed in the deploy log).
- **goldragon** `main` → `c8b5840d`: `secrets/local-llm-api-token.sops`
  — the token, age-encrypted to prometheus (recipient verified two
  ways), produced by a blind `gopass show | sops --encrypt` pipe.

## The deploy

`lojix-cli '(FullOs goldragon prometheus [<datom>] [github:LiGoldragon/CriomOS/main] Switch (Some prometheus) None)'`
with the rebuilt binary. `builder == target == prometheus`, so the build
runs on prometheus over ssh and the closure-copy phase is skipped —
**nothing is realized in the local store** (intent 1016). Cleared eval;
building the Gemma weights + mmproj on prometheus (existing 9 models
already cached there). In flight at time of writing.

## Post-deploy verification (pending)

The build/eval is proven; these are RUNTIME checks once activation lands:

1. **Service health** — `${node}-llama-router` active on prometheus.
2. **Auth enforced** — the start script passes `--api-key-file` from the
   sops secret at `/run/secrets/localLlmApiToken`; confirm a request
   without the bearer token is rejected and one with the gopass token
   succeeds.
3. **Models load** — `gemma-4-31b` and `gemma-4-26b-a4b` served on
   `:11434/v1`.
4. **Vision works — THE open runtime question.** The mmproj is wired via
   a `mmproj = <path>` line in the router preset. Whether this llama.cpp
   build's `--models-preset`/`--models-dir` router actually applies a
   per-model `mmproj` (and supports multimodal in router mode at all) is
   unverified. If it doesn't, the model weights are already cached on
   prometheus, so iterating on the mmproj wiring is a cheap config-only
   redeploy — no re-download. This is the one piece most likely to need
   a follow-up.

## Open for the psyche

- Architecture intent: the original design had cloud GPT-5.5 as the
  orchestrator with a small fast local actor. Installing big local
  models (esp. the 31B dense) shifts that balance — is the local model
  now meant to do more of the reasoning itself, or is the 26B-A4B MoE
  the intended fast actor and the 31B a max-quality option?
