# Curriculum deploy cutover

Method: probe `cargo test --locked`; `nix flake check -L --max-jobs 0 --builders @/etc/nix/machines`; public forge revision queries; runtime `Generate` and `Check` against Primary

Datom 0.2.0 passed its Cargo suite and all nine remote-builder Nix checks before publication at `d47419ef872ab76bfbd6bb4b3e84b62a883a8d31`.

The public `curriculum-deploy` runtime passed Cargo formatting, strict Clippy, tests, Nix evaluation, its public external-Curriculum integration check, and the full remote-builder Nix gate. Its final public revision is `ef35a6dc00c6df13df4f2067ab34e5f1cfc6bc08`.

The public Curriculum data root at `f06e26b8456731920c2e4770a15b332c901e6d9c` contains 35 authored skills and `roles.datom`; it contains no DOTOS, Rust, Cargo, runtime Nix packaging, activation manifests, fixtures, or generated consumer output.

Primary invoked the final runtime with exactly one typed inline Datom request using its pinned Curriculum store root and explicit workspace root. Generation reported `Generated.{35 27}` and checking reported `Checked.{35 27}`. The resulting surfaces contain 35 `.agents` skills, 35 Claude skill companions, 27 role packets, and 27 typed cleanup-inventory entries. Primary's remote Nix check passed before publication at `339b22a814192f45b17d1ca3bc9adbdc56d2377e`.

The engine package derivation remained `/nix/store/mnndz3258f0f1554iirdxqmbj0qsd28j-curriculum-deploy-0.1.0.drv` when the Curriculum input was overridden from the published data revision to its parent. This witnesses that the data revision is absent from the Rust engine package derivation identity.

The coordination daemon socket was unavailable throughout. Coordination claims therefore remained advisory and could not be recorded; disjoint worktrees and repository ownership were used, and final working copies were clean.
