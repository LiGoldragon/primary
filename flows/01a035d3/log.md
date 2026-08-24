# Curriculum/Nix boundary investigation

Investigating whether authored curriculum data unnecessarily rebuilds Rust code, what the actual dependency path is, and the terminal separation that would remove the coupling. No implementation is authorized in this round.

Recorded the living's conditional Rust/data-boundary ruling verbatim. Dispatched read-only subflows for the Nix dependency trace, the code/data architecture, and relevant written-psyche/past-flow evidence.

Remembered: 15b67974, 68512643, 358f143a, e06e4c07 — depth 1

Established that a combined Nix source, not Rust embedding, couples curriculum data to repeated local-crate build/test/lint derivations. Wrote witnesses and the separation design; no implementation or expensive build was performed. The remaining design question is whether the implementation round also realizes the newer no-activation-manifest skill anatomy.

The living ruled implementation as a new public `curriculum-deploy` repository, with the runtime moved out of Curriculum, external Curriculum data, Datom replacing DOTOS, and all CLI configuration carried exclusively by the typed Datom input.

Created the public `LiGoldragon/curriculum-deploy` repository and its clean local Jujutsu checkout. No runtime code had been moved at bootstrap; existing Primary flow work was preserved.

The living supplied an exact prompt-crafting rule to add to the authored Curriculum source after the new deployment works; queued it behind runtime/data validation.
