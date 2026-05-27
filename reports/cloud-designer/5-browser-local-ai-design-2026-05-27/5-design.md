# 5 · Design — three-tier browser orchestration on local AI

Synthesised from
[1-browser-cli-state.md](1-browser-cli-state.md),
[2-local-ai-node-state.md](2-local-ai-node-state.md),
[3-hf-prefetch-precedent.md](3-hf-prefetch-precedent.md),
[4-gemma-and-browser-cli-web.md](4-gemma-and-browser-cli-web.md).

## Picture in one block

```
┌────────────────────────────────────────────────────────────┐
│ CLOUD: GPT-5.5 orchestrator                                │
│   high-level instructions, multi-step plan, sanity-checks  │
└─────────────────┬──────────────────────────────────────────┘
                  │ instruction text via cloud component signal
                  ▼
┌────────────────────────────────────────────────────────────┐
│ LOCAL (Max's workstation): browser-use CLI                 │
│   wrapped with OPENAI_API_BASE → atlas:11434/v1            │
│   wrapped with OPENAI_API_KEY ← gopass atlas/llama-api-key │
│   spawned per-task; non-resident                           │
└─────────────────┬──────────────────────────────────────────┘
                  │ OpenAI-compatible chat-completions stream
                  ▼
┌────────────────────────────────────────────────────────────┐
│ LOCAL (atlas, AMD Strix Halo): llama-server                │
│   serves gemma-4-E4B-it (4.5B mm, ~5GB GGUF Q4_K_M)        │
│   text + image + audio modal under 128K context            │
│   models-max=1 with 5-min idle unload                      │
└─────────────────┬──────────────────────────────────────────┘
                  │ Chrome DevTools Protocol (CDP)
                  ▼
┌────────────────────────────────────────────────────────────┐
│ LOCAL: Chrome on remote-debugging-port=9222                │
│   already configured via hexis wrapper                     │
│   browser-use uses cdp-use as direct CDP client            │
└────────────────────────────────────────────────────────────┘
```

Three tiers, three model roles: **orchestrator** (cloud,
high-context plan), **actor** (local, fast multimodal vision),
**substrate** (browser).

## What's already in place (per scout findings)

- **Chrome dev port 9222**: configured by hexis wrapper at
  `CriomOS-home/modules/home/profiles/max/default.nix:54-82`.
  No further wiring needed.
- **browser-use as the picked CLI**: pre-implementation
  packaging plan at
  `CriomOS/reports/0031-browser-use-packaging-plan.md`.
  Agent-agnostic; reads `OPENAI_API_KEY`/`ANTHROPIC_API_KEY`/
  `GOOGLE_API_KEY` from env. v2.0 (Jan 2026) supports
  `OPENAI_API_BASE` natively per scout 4.
- **Atlas largeAI node**: declaratively configured in
  `CriomOS/modules/nixos/llm.nix` + `CriomOS-pkgs`'s
  `llama-cpp-strix-halo` + inventory at
  `CriomOS-lib/data/largeAI/llm.json`. llama-server on port
  11434, OpenAI-compatible, AMD Strix Halo via Vulkan, 8
  existing GGUF models up to 122B, models-max=1,
  5-min idle unload, MemoryMax 110 GB. **Currently
  declarative-but-not-deployed** — no production hardware
  surveyed.
- **HF model fetching precedent**: per-shard `pkgs.fetchurl`
  with hand-transcribed sha256 hashes inside llm.nix
  (lines 32-64) and llm.json (one URL+sha256 entry per shard).
  No automation existed; **this cycle adds it**.

## What's missing (designed below)

1. A Nix utility to prefetch HF model snapshots and produce SRI
   hashes the same way `nix-prefetch-url` produces them for
   single files. (Designed + prototyped.)
2. A Gemma 4 E4B GGUF entry in the model inventory so atlas
   serves it.
3. A `browser-use` wrapper that points `OPENAI_API_BASE` at
   atlas and pulls `OPENAI_API_KEY` from gopass.
4. Actual deployment of atlas + the cloud-side GPT-5.5
   integration via the cloud component signal contract
   (these two land in cloud-operator's hands, with operator
   beads).

## Component 1 — HF model prefetch utility (PROTOTYPED)

Two-file pair, both in `CriomOS-lib`:

- **`tools/nix-prefetch-huggingface`** — bash script that takes
  `<repo> [<revision>]`, downloads the snapshot via the modern
  `hf` CLI (falls back to deprecated `huggingface-cli`),
  strips the `.cache/` bookkeeping noise, and prints the
  recursive SHA-256 in SRI format on stdout. Diagnostic output
  on stderr so the stdout is pipe-clean.

- **`lib/fetchHfModel.nix`** — fixed-output derivation
  parameterised by `{ repo, revision, hash, files?,
  tokenEnvironmentVariable? }`. Uses
  `python3Packages.huggingface-hub`'s CLI inside the FOD; pins
  the snapshot to the SRI hash from the script. `files` is an
  optional glob filter for fetching only specific files from
  multi-quant repos (`["*Q4_K_M*.gguf"]` to grab one quant
  variant). `tokenEnvironmentVariable` opt-in handles gated
  models (Gemma 4 requires Google's acceptance click, then
  `HF_TOKEN`); fetcher honors the env var only under
  `nix build --impure`.

Exposed via `criomos-lib`'s `lib/default.nix`:

```nix
fetchHfModel = pkgs: import ./fetchHfModel.nix { inherit pkgs; };
```

so consumers in CriomOS / CriomOS-home call
`criomos-lib.fetchHfModel pkgs { repo = ...; ... }`.

**Smoke test**: built against
`hf-internal-testing/tiny-random-gpt2`. Prefetch script
produced `sha256-8K9B/C62GW5lXC0c8QQpQ9QAE1UMoG+kYqvGhnWIp64=`;
the fetcher derivation built that exact hash from the same
content. Snapshot in store contains the full model:
`config.json`, `model.safetensors`, `pytorch_model.bin`,
tokenizer files, etc.

**License posture**: deliberately no `license` field in
`meta` — `fetchHfModel` is a content fetch primitive parallel
to `fetchurl`. The caller wraps the snapshot in a package
derivation that knows the model license. (Initial prototype
set `license = unfree` and blocked the smoke build; removed.)

## Component 2 — Gemma 4 E4B inventory entry (BEAD)

Per scout 4: Google released Gemma 4 on 2026-04-02. The
small multimodal variant the user named is
`google/gemma-4-E4B-it` (4.5B effective params, 8B with
embeddings, 128K context, text+image+audio, Apache 2.0).
For llama.cpp inference the GGUF quantized version comes
from Unsloth's repo: `unsloth/gemma-4-E4B-it-GGUF`
(confirmed by Hugging Face's own `hf` CLI examples).

Q4_K_M quant lands at ~5 GB on disk — fits comfortably in
atlas's 110 GB MemoryMax alongside the existing 17–122 GB
inventory.

Entry shape (matches existing llm.json schema):

```json
{
  "modelId": "gemma-4-e4b-it",
  "source": {
    "kind": "hfModel",
    "repo": "unsloth/gemma-4-E4B-it-GGUF",
    "revision": "<pin to commit>",
    "hash": "<from nix-prefetch-huggingface>"
  },
  "ctxSize": 131072,
  "loadOnStartup": false
}
```

This requires extending llm.nix's `mkModelStorePath` to
recognise `source.kind == "hfModel"` and call `fetchHfModel`
instead of `fetchurl`. Operator implementation — bead
`primary-1ubd`.

## Component 3 — browser-use wrapper (BEAD)

The simplest possible packaging that converts browser-use's
default outbound-API behaviour to local-AI:

```nix
browser-use-atlas = pkgs.symlinkJoin {
  name = "browser-use-atlas-wrapped";
  paths = [ browser-use ];
  nativeBuildInputs = [ pkgs.makeWrapper ];
  postBuild = ''
    wrapProgram $out/bin/browser-use \
      --set OPENAI_API_BASE "http://atlas.fieldlab.criome:11434/v1" \
      --set OPENAI_MODEL "gemma-4-E4B-it" \
      --run 'export OPENAI_API_KEY=$(${pkgs.gopass}/bin/gopass show -o atlas/llama-api-key 2>/dev/null || echo dummy)'
  '';
};
```

Same shape as the cloud component's flarectl-gopass wrap from
the previous cycle — `--run` fetches the token at every
spawn so atlas's auth surface stays opaque to the daemon
process layer. `dummy` fallback covers the
empty-API-key-file state of atlas today (no auth enforced).

Per scout 1, browser-use's nix derivation is in
pre-implementation stage at
`CriomOS/reports/0031-browser-use-packaging-plan.md`; the
operator's bead `primary-ooh1` ties the wrapper to that
landing.

## Component 4 — Cloud-side orchestration (BEAD)

The cloud-side GPT-5.5 orchestrator is **outside this
prototype**. The shape it would take:

- The cloud component's signal contract gains an operation
  that accepts a high-level browse instruction and routes it
  through a cloud LLM (GPT-5.5 from the model provider).
- The cloud daemon spawns `browser-use` locally with the
  refined per-step instruction.
- Multi-step plans loop: cloud LLM observes result, refines
  next step, re-spawns.

Bead `primary-y3is` covers the end-to-end smoke test once
the first three beads land. The orchestrator design (where in
the cloud component triad it lives, what reply variants it
emits, how multi-step state is held) is its own future cycle.

## Why this design

- **Component reuse over invention.** browser-use already has
  OpenAI-base-URL support; atlas already exposes an
  OpenAI-compatible endpoint; the only new substrate is the
  HF model fetcher.
- **Mirrors the cloud cycle's gopass wrap pattern.** Operators
  are already familiar with the flarectl-gopass shape; the
  browser-use wrap reads identically.
- **No new component-triad.** Browser control is wiring,
  not a new daemon. The cloud component is the orchestrator
  surface (existing); atlas is the model server (existing);
  browser-use + Chrome are the action substrate (existing).
- **Gemma 4 E4B specifically.** Small enough to live alongside
  atlas's existing 17-122 GB models; multimodal so it can read
  browser screenshots without a separate vision encoder;
  Apache 2.0 so deployment is unencumbered. The only blocker:
  Google's gating click for `google/gemma-4-E4B-it` itself;
  using Unsloth's GGUF repo sidesteps the gate.
