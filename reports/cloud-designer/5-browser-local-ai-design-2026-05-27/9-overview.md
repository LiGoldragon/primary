# 9 · Overview — cycle synthesis (the psyche read)

This file is the synthesis the psyche reads. Everything else
in this meta-report directory is supporting material.

## What this cycle did

Executed the **mine → design → prototype → bead → hand off**
flow against the browser-on-local-AI directive (spirit
983–987):

1. **Mined.** Four parallel scouts:
   - [Chrome dev port + picked CLI](1-browser-cli-state.md):
     port 9222 already wired via hexis wrapper on Max's
     profile; `browser-use` is the picked CLI (pre-implementation
     packaging plan at `CriomOS/reports/0031`); it supports
     `OPENAI_API_BASE` natively in v2.0.
   - [Local AI node](2-local-ai-node-state.md): atlas
     (LargeAiRouter, AMD Strix Halo via Vulkan, llama-server
     on port 11434, OpenAI-compatible, 8 GGUF models 17–122 GB,
     models-max=1 with 5-min idle unload). Declarative but
     not deployed; no auth enforced.
   - [HF prefetch precedent](3-hf-prefetch-precedent.md):
     per-shard `pkgs.fetchurl` with hand-transcribed hashes in
     `CriomOS/modules/nixos/llm.nix` + `CriomOS-lib/data/largeAI/llm.json`;
     NO automation utility yet — building from scratch was the
     right move.
   - [Gemma 4 + browser CLI web](4-gemma-and-browser-cli-web.md):
     Gemma 4 released 2026-04-02; the small multimodal variant
     is `google/gemma-4-E4B-it` (4.5B/8B, 128K context,
     text+image+audio, Apache 2.0); llama.cpp supports it via
     Unsloth's GGUF mirror `unsloth/gemma-4-E4B-it-GGUF`;
     browser-use v2.0 (Jan 2026) the top candidate.

2. **Designed.** Three-tier architecture (cloud GPT-5.5
   orchestrator → local browser-use CLI → local atlas Gemma 4
   actor → Chrome on dev port 9222). Four components: HF
   prefetch utility (new), Gemma 4 inventory entry (new),
   browser-use atlas-wrap (new), cloud-side GPT-5.5 wiring
   (deferred). Full picture: [5-design.md](5-design.md).

3. **Prototyped the highest-risk piece.** Built the HF model
   fetch utility end-to-end:
   - `tools/nix-prefetch-huggingface` (bash script,
     nix-prefetch-url shape).
   - `lib/fetchHfModel.nix` (fixed-output derivation).
   - Smoke-tested against
     `hf-internal-testing/tiny-random-gpt2`. Round-trip
     verified: prefetch produces `sha256-8K9B/C62GW5lXC...`;
     fetcher builds that exact hash; resulting `$out/` has
     the full snapshot.
   - Pushed to origin:
     https://github.com/LiGoldragon/CriomOS-lib/pull/new/designer-hf-prefetch-utility-2026-05-27.
   - Details: [6-prototype.md](6-prototype.md).

4. **Filed beads for cloud-operator.** Four beads, dependency
   chain runs 1 → 2 → 3 → 4:
   - `primary-3dqf` — land the HF utility on `CriomOS-lib`
     main.
   - `primary-1ubd` — add Gemma 4 E4B GGUF to atlas inventory.
   - `primary-ooh1` — package browser-use with the atlas wrap.
   - `primary-y3is` — deploy atlas + end-to-end smoke.
   - Details: [7-beads.md](7-beads.md).

5. **Passed forward open questions** (per spirit 987's
   dual-question principle):
   - 5 questions for the psyche (need direction before /
     during implementation — orchestrator shape, wrapper home,
     auth posture, gating, atlas hardware).
   - 7 questions for cloud-operator (resolve as you implement
     — branch landing shape, llm.nix dispatch extension,
     Python packaging specifics, Strix Halo vision flag,
     token rotation, Chrome port collision, smoke targets).
   - Full text: [8-open-questions.md](8-open-questions.md).

## What's working today (provable)

- Atlas declaratively configured; can be deployed to any
  Strix Halo host with `behavesAs.largeAi=true`.
- Chrome dev port 9222 already enabled by hexis wrapper.
- browser-use v2.0 supports `OPENAI_API_BASE` override.
- `nix-prefetch-huggingface` + `fetchHfModel` round-trip
  proven on a 10-file tiny model.
- All four components compose into a clear three-tier
  picture with no architectural surprises.

## What's blocked on you (the psyche)

The 5 psyche questions in
[8-open-questions.md](8-open-questions.md). Highest-priority:

- **P5 (atlas hardware)** — without a target node,
  bead `primary-y3is` can't even start.
- **P1 (orchestrator shape)** — the GPT-5.5 ↔ browser-use
  wiring is the entire cloud-side mechanism the directive is
  pointed at; cloud-operator can land the local-AI piece
  without it, but the directive only completes when this is
  decided.
- **P3 (atlas auth)** — affects whether the browser-use
  wrapper's `dummy` fallback is acceptable or needs
  hardening.

P2 (wrapper home) and P4 (Gemma gating) are lower-stakes;
cloud-operator can ship a default that you redirect later
without rework.

## What's in cloud-operator's queue

Four beads, ready to pick up. The dependency chain (HF
utility → Gemma 4 in inventory → browser-use wrap → e2e
smoke) means they're naturally sequential, but landing
1+2+3 in parallel waves is fine; 4 is the integration gate.

The browser-use packaging plan (`CriomOS/reports/0031`) was
pre-implementation when scout 1 surveyed; if it's still in
that state when cloud-operator starts, completing the
packaging IS the first step of bead `primary-ooh1`.

## What's NOT in scope for this directive

- The cloud-side GPT-5.5 orchestrator wiring (depends on
  psyche question P1).
- domain-criome integration for resolving browser destinations
  through the Criome domain layer.
- Multi-instance browser fleet management.
- Persistent browser sessions vs. fresh-per-task.

These are downstream cycles once the foundation is in.

## Anchors

- Worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS-lib/designer-hf-prefetch-utility-2026-05-27/`
- Branch: `designer-hf-prefetch-utility-2026-05-27` @ `55407c1c5c0b`
- PR URL: https://github.com/LiGoldragon/CriomOS-lib/pull/new/designer-hf-prefetch-utility-2026-05-27
- Beads: `primary-3dqf` (utility), `primary-1ubd` (Gemma),
  `primary-ooh1` (browser-use wrap), `primary-y3is` (e2e smoke).
- Spirit anchors: 983, 984, 985, 986, 987.
- Cycle meta-report: `reports/cloud-designer/5-browser-local-ai-design-2026-05-27/`.
