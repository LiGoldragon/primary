# 7 · Beads — cloud-operator implementation queue

Four beads filed against the BEADS shared store. Each names
the work + an acceptance criterion + the design context in
this report directory. cloud-operator picks them up in any
order, but the dependency chain runs roughly 1 → 2 → 3 → 4.

## `primary-3dqf` — Land fetchHfModel + nix-prefetch-huggingface

**Scope:** review the cloud-designer prototype branch
`designer-hf-prefetch-utility-2026-05-27` on `CriomOS-lib`,
decide whether to land as-is or restructure (e.g. `tools/` vs
`scripts/` subdir), merge to main.

**Acceptance:** `fetchHfModel` + `nix-prefetch-huggingface`
on `CriomOS-lib` main; smoke test passes.

**Notes:** the smoke test at
`tools/smoke-fetch-tiny-model.nix` runs under `--impure` and
verifies the round-trip. Keep or remove per the repo's test
conventions.

## `primary-1ubd` — Add Gemma 4 E4B GGUF to atlas inventory

**Scope:** add the Gemma 4 E4B-it variant (Unsloth GGUF) to
atlas's model inventory, using `fetchHfModel` from the
landed utility. Pin the snapshot hash via
`nix-prefetch-huggingface unsloth/gemma-4-E4B-it-GGUF`.

**Acceptance:** atlas serves `gemma-4-E4B-it` via the
OpenAI-compatible endpoint; `curl -X POST
atlas:11434/v1/chat/completions ...` returns a sensible
response.

**Inventory location decision:** `data/largeAI/llm.json`
today, or `horizon.cluster.aiProviders` per the
horizon-re-engineering branch's in-flight migration. Whichever
lands first — both can consume `fetchHfModel`.

**Multimodal verification needed:** scout 4 said llama.cpp
supports Gemma 4 multimodal; scout 2 noted no multimodal
models in current atlas inventory. May require
`llama-cpp-strix-halo` recompile with vision flag enabled.
Confirm before assuming image input works.

## `primary-ooh1` — Package browser-use with OPENAI_API_BASE wrap

**Scope:** complete the browser-use packaging plan at
`CriomOS/reports/0031-browser-use-packaging-plan.md`,
wrapping the binary with `OPENAI_API_BASE=http://atlas:11434/v1`
+ `OPENAI_API_KEY=$(gopass show -o atlas/llama-api-key)`.

Pattern mirrors the cloud component's flarectl-gopass wrap
from spirit 924 (cloud-designer cycle commit `ec2d3493`):
`symlinkJoin` + `wrapProgram` + `--run`.

**Acceptance:** `browser-use` binary on PATH (Max's profile)
with `OPENAI_API_BASE` pointed at atlas; `browser-use
--instruction "navigate to example.com"` works without an
external API key.

## `primary-y3is` — Deploy atlas + end-to-end smoke

**Scope:** stand up the actual atlas node (or assign
`behavesAs.largeAi=true` to a real existing node), populate
`/var/lib/llama/api-key` (gopass-fed), and run the e2e smoke
recipe through browser-use.

**Acceptance:** `browser-use --instruction X` drives Chrome
via atlas-served Gemma 4 with no external API calls;
screenshot lands in the screenshot directory.

**Prereqs:** depends on the other three beads landing first.

## Why beads (not just a written plan)

BEADS is the workspace's shared work-item store; the cloud
component cycle showed beads are the right substrate for
operator-implementation handoffs (intent 977's audit
discipline names beads as the post-audit growth queue).
Filing them now means cloud-operator's `bd ready` query
surfaces them automatically alongside their other workload.

Each bead carries enough description that operator can pick
it up without re-reading the whole design report — but the
design report stays the canonical context for the *why*.
