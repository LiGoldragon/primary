# Curriculum/Nix boundary investigation

Investigating whether authored curriculum data unnecessarily rebuilds Rust code, what the actual dependency path is, and the terminal separation that would remove the coupling. No implementation is authorized in this round.

2026-08-25: Recorded the living's conditional Rust/data-boundary ruling verbatim. Dispatched read-only subflows for the Nix dependency trace, the code/data architecture, and relevant written-psyche/past-flow evidence.

Remembered: 15b67974, 68512643, 358f143a, e06e4c07 — depth 1

2026-08-25: Established that a combined Nix source, not Rust embedding, couples curriculum data to repeated local-crate build/test/lint derivations. Wrote witnesses and the separation design; no implementation or expensive build was performed. The remaining design question is whether the implementation round also realizes the newer no-activation-manifest skill anatomy.
