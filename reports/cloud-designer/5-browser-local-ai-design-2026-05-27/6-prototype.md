# 6 · Prototype — what landed on the worktree

Worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS-lib/designer-hf-prefetch-utility-2026-05-27/`
Branch: `designer-hf-prefetch-utility-2026-05-27`
Pushed to origin: `55407c1c5c0b`
PR URL: https://github.com/LiGoldragon/CriomOS-lib/pull/new/designer-hf-prefetch-utility-2026-05-27

Three new files, plus a one-block edit to `lib/default.nix`.

## `tools/nix-prefetch-huggingface`

71-line bash script. Takes `<repo> [<revision>]`, downloads
the HF snapshot via `hf` (falls back to deprecated
`huggingface-cli` for older releases), strips `.cache/`
bookkeeping noise, prints the SRI hash on stdout. Diagnostic
output on stderr so stdout is pipe-clean.

Key behaviours:

- Refuses to run without `hf` or `huggingface-cli` on PATH;
  prints the install one-liner.
- Refuses to run without `nix` on PATH.
- Uses `nix hash path --type sha256 --format sri` for the SRI
  output the FOD expects.
- `HF_HOME`/`HF_HUB_CACHE` redirected to `$tmpdir` so the
  user's `~/.cache/huggingface` stays untouched.
- For gated models: `HF_TOKEN` env var is honored implicitly by
  the HF CLI; no script-level token plumbing.

## `lib/fetchHfModel.nix`

~110 line nix expression. `{ pkgs }: { repo, revision ? "main",
hash, files ? [], tokenEnvironmentVariable ? null }`.

Fixed-output derivation:

- `outputHashMode = "recursive"` — hashes the whole snapshot
  tree.
- `outputHashAlgo = "sha256"`.
- `nativeBuildInputs = [ python3Packages.huggingface-hub
  pkgs.cacert ]` — `cacert` so HTTPS to HF works inside the
  sandbox.
- `impureEnvVars = [tokenEnvironmentVariable]` (only when set)
  — supports gated models under `nix build --impure`.
- `buildPhase` prefers modern `hf` over deprecated
  `huggingface-cli`; strips `$out/.cache` post-download so
  hash matches script output.
- `meta` — description + homepage; no `license` (caller's
  responsibility per the fetchurl pattern).

## `lib/default.nix` change

Adds two lines (plus comment block) under the existing
`importJSON` helper:

```nix
fetchHfModel = pkgs: import ./fetchHfModel.nix { inherit pkgs; };
```

Consumers call `criomos-lib.fetchHfModel pkgs { repo; ...; }`.

## `tools/smoke-fetch-tiny-model.nix`

A self-contained test expression that builds the smoke
derivation against `hf-internal-testing/tiny-random-gpt2`.

Hash inside the file was produced by running the prefetch
script first, then transcribed. The smoke test proves the
prefetch script ↔ fetcher round-trip exactly matches.

Whether to keep this file or remove before merge is a repo
convention question (some repos keep smoke fixtures, some
prefer them out of tree). Flagged in the operator open
questions.

## Smoke test — full transcript

```text
$ nix shell nixpkgs#python3Packages.huggingface-hub -c \
    ./tools/nix-prefetch-huggingface hf-internal-testing/tiny-random-gpt2
nix-prefetch-huggingface: downloading hf-internal-testing/tiny-random-gpt2 @ main
A new version of huggingface_hub (1.16.4) is available! You are using version 1.10.2.
Fetching 10 files: 100%|██████████| 10/10 [00:02<00:00,  4.36it/s]
nix-prefetch-huggingface: hashing snapshot tree
sha256-8K9B/C62GW5lXC0c8QQpQ9QAE1UMoG+kYqvGhnWIp64=

$ nix build --impure --no-link --print-out-paths \
    --expr 'import ./tools/smoke-fetch-tiny-model.nix'
building '/nix/store/ys6f1rkb5a3djqxs0a2s4s1zlhxfxkq0-hf-internal-testing__tiny-random-gpt2-main.drv'...
copying path '/nix/store/h8x03n2rz05liaslf4zar6wg1zpa22vv-hf-internal-testing__tiny-random-gpt2-main' from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
/nix/store/h8x03n2rz05liaslf4zar6wg1zpa22vv-hf-internal-testing__tiny-random-gpt2-main

$ ls /nix/store/h8x03n2rz05liaslf4zar6wg1zpa22vv-hf-internal-testing__tiny-random-gpt2-main/
config.json
merges.txt
model.safetensors
pytorch_model.bin
special_tokens_map.json
tf_model.h5
tokenizer_config.json
tokenizer.json
vocab.json
```

Round-trip verified: prefetch hash → FOD build → identical
snapshot tree.

## What the prototype does NOT do

Per cloud-designer scope (intent 987 — design + prototype +
beads only), the prototype intentionally stops at the HF
fetch utility. The four production pieces are
cloud-operator's bead queue:

- Land the utility on `CriomOS-lib` main
  (`primary-3dqf`).
- Add the Gemma 4 E4B GGUF entry to atlas's inventory
  (`primary-1ubd`).
- Package + wrap browser-use with the atlas endpoint
  (`primary-ooh1`).
- Deploy atlas + smoke the end-to-end browser flow
  (`primary-y3is`).

Each bead points back at this report directory for design
context.
