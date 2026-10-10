# Curriculum/Nix boundary investigation

Investigating whether authored curriculum data unnecessarily rebuilds Rust code, what the actual dependency path is, and the terminal separation that would remove the coupling. No implementation is authorized in this round.

Recorded the living's conditional Rust/data-boundary ruling verbatim. Dispatched read-only subflows for the Nix dependency trace, the code/data architecture, and relevant written-psyche/past-flow evidence.

Remembered: 15b67974, 68512643, 358f143a, e06e4c07 — depth 1

Established that a combined Nix source, not Rust embedding, couples curriculum data to repeated local-crate build/test/lint derivations. Wrote witnesses and the separation design; no implementation or expensive build was performed. The remaining design question is whether the implementation round also realizes the newer no-activation-manifest skill anatomy.

The living ruled implementation as a new public `curriculum-deploy` repository, with the runtime moved out of Curriculum, external Curriculum data, Datom replacing DOTOS, and all CLI configuration carried exclusively by the typed Datom input.

Created the public `LiGoldragon/curriculum-deploy` repository and its clean local Jujutsu checkout. No runtime code had been moved at bootstrap; existing Primary flow work was preserved.

The living supplied an exact prompt-crafting rule to add to the authored Curriculum source after the new deployment works; queued it behind runtime/data validation.

Published Datom 0.2.0 with the public typed realization/textualization extension required by external schemas. Published the first green public `curriculum-deploy` runtime with a strict one-Datom-input CLI and no authored data or DOTOS dependency.

Converted Curriculum to a public pure-data root containing 35 discovered skills and `roles.datom`, moved the remaining instructional preamble out of runtime code, and added the living's prompt-crafting line after cross-repository generation became green. Published the data-only cutover; Primary migration and final public-ref proof remain.

Hardened the public runtime with a pinned external-data integration check and witnessed an identical engine derivation across Curriculum revisions. Migrated Primary to independently pinned public runtime and data inputs, regenerated and checked all managed surfaces, passed remote Nix gates, committed and pushed every repository, and closed with clean working copies.
