# Flow 674a4dab

Design audit of the CriomOS / Lojix / Horizon stack: acquire what the psyche
wanted from recent Codex transcripts (read in depth, not from logs alone), then
audit the current state of CriomOS, CriomOS-home, Goldragon, Lojix, Horizon and
the package/source repositories for broken separation of concerns, duplicated
sources of truth, and slop; propose the end-shape; close with the three most
important questions.

STT note: the living said "Logix" — the repository is `lojix`. "Horizon" is
`horizon-rs` plus `criomos-horizon-config`.

## Plan

- Wave 1: psyche acquisition per plane (OS/Home/Goldragon, Lojix, Horizon,
  packages/sources, origins in older sessions) + structural maps (Nix side,
  Rust side).
- Wave 2: archaeology of how each flagged shape came to be; audit against the
  acquired vision, seeking disconfirming evidence.
- Wave 3: verification of findings, end-shape proposal, report.

## State

Wave 1 dispatched.

Remembered: 01a048a6, 01a04881 — depth 1
Most relevant: the AgentIntercomGraphical gate bundled generic graphical
prerequisites with agent-specific GUIs; the living's working hypothesis was that
the gate was really an Edge-node concern under an unrelated name; deployment
preflight is blocked because no manifest supplies transport/builder/selector.
