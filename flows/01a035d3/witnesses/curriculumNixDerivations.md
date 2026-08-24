# Curriculum Nix derivations

Method: probe `nix flake show`; `nix flake check --no-build --no-write-lock-file`; `nix eval`; `nix derivation show` in `/git/github.com/LiGoldragon/Curriculum`

No build was launched and no source file was changed.

The flake's filtered source includes `.rs`, `.md`, and `.dotos`. The evaluated `skills-0.5.0` package derivation takes that full source directly and runs `cargo build --locked`.

The dependency artifact derivation instead takes Crane's generated Cargo-only source: `Cargo.toml`, `Cargo.lock`, and a dummy Rust entry point. Authored curriculum data is absent. Therefore a Markdown- or DOTOS-only change changes the final package derivation but not the cached third-party dependency artifact derivation.

The evaluated native check fan-out is:

- `skills`: the package derivation, running Cargo build;
- `build`: a distinct Cargo build derivation;
- `test` and `default`: one shared Cargo test derivation;
- `clippy`: a distinct Cargo clippy derivation;
- `fmt`: Cargo format checking, without an expected compile;
- four generator/interface checks which depend on the built package and execute it against source/workspace data.

Consequently a real full check after a curriculum-data edit can compile the Curriculum crate in several independent derivations while reusing its dependency artifacts. The evaluation-only probe established the graph and commands; it did not measure wall-clock time or observe a before/after content edit.

No repository watcher or hook that automatically invokes `nix flake check` was found. The command that makes the check run after an edit remains outside this witness.
