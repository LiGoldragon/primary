# 0 · Frame and method — browser + local AI + HF prefetch cycle

Session-spawning prompt (psyche, 2026-05-27): set up the proper
way to use the browser whose Chrome DevTools port is already
open; redirect the picked browser-control CLI from its outbound
model API to the local AI node on CriomOS; load that node with
Gemma 4 Flash (small multimodal); build a Nix prefetch utility
for Hugging Face models in the nix-prefetch-url shape; design
the three-tier orchestrator → CLI → local model → browser flow;
prototype it; file beads for cloud-operator to implement; carry
open questions forward both to the psyche and to cloud-operator.

Intents captured 983–987 (Decisions + Principles, High):
- 983: local AI node hosts the browser-driving model.
- 984: Gemma 4 Flash (small multimodal variant).
- 985: HF model prefetch nix utility.
- 986: orchestrator/actor/substrate split — GPT-5.5 cloud
  → local CLI → Gemma 4 local → Chrome via DevTools port.
- 987: cloud-designer scope = design + prototype + beads;
  reports carry both psyche-question and operator-question
  sections.

## Method — four parallel research scouts

Subagents in background (designer protocol authorises parallel
dispatch by default). Each writes one report into this
meta-report directory.

- **Scout 1 — Browser CLI + dev-port state.** Surveys CriomOS
  + CriomOS-home (and adjacent repos) for the existing
  `--remote-debugging-port` Chrome config, the picked
  browser-control CLI (likely browser-use, Playwright, Stagehand,
  Skyvern, claude-code-browser, or similar), and how the CLI
  currently calls its external model API. Lands at
  `1-browser-cli-state.md`.

- **Scout 2 — Local AI node setup.** Surveys CriomOS-home,
  CriomOS-test-cluster, CriomOS-pkgs, criomos-horizon-config
  for the local AI node — is there one already? What model
  server (ollama / vLLM / text-generation-inference / llama.cpp
  server)? What network exposure? What's the API surface? What
  hardware (the "large AI node"). Lands at
  `2-local-ai-node-state.md`.

- **Scout 3 — HF prefetch precedent.** Sweeps reports/ + skills/
  + repos for any prior huggingface-model + nix-prefetch work.
  Psyche thinks "somebody had documented maybe a research on
  there's a script out there". Find what we already have so the
  prototype doesn't duplicate. Lands at
  `3-hf-prefetch-precedent.md`.

- **Scout 4 — Web research: Gemma 4 + browser-control CLI
  ecosystem.** Reaches the live web for: (a) Gemma 4's release
  status, variants, sizes, multimodal capabilities, HF model
  IDs; (b) the current browser-control CLI landscape that
  matches "CLI that calls another model API" — likely
  browser-use, Stagehand, Skyvern, claude-code-browser,
  computer-use-demo, etc. Lands at `4-gemma-and-browser-cli-web.md`.

After the four return: synthesis + design + prototype + bead
creation + dual-open-question report.

## Out of scope this cycle

- Implementation of the design — that goes to cloud-operator
  via beads.
- Actually running GPT-5.5 in cloud — the cloud component is
  emerging through cloud-operator's separate work; here we just
  define the interface the CLI presents to the cloud-side
  orchestrator.
- Wiring the local AI node into production cluster topology —
  that's system-operator / cluster-operator territory; we
  describe the requirement, they wire it.
- Multimodal browser-driving prompt engineering — that's the
  next layer up; here we just confirm the model and CLI shape
  support it.
