# Ethos emitter

Method: code read /git/github.com/LiGoldragon/ethos-monolith/src/generate.rs, /git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs, and /git/github.com/LiGoldragon/ethos-monolith/tests/generate.rs

The prior component surface derived six canonical paths but did not realize source or write emitted Rust. The committed implementation realizes all three Interface documents before it writes pending artifacts, then installs the three projections. `signal.ethos` is channel-bearing and emits a source-owned Signal binding, structural derivations, macro channel, request alias, and closed reply. `nexus.ethos` and `sema.ethos` retain ordinary Interface output.

Method: probe cargo test --test generate

Before implementation, the added generation tests failed to compile because `GenerationError` and `ComponentGenerationOperations::generate` did not exist. After implementation the generation tests passed, including source failure before installation, the three output artifacts, a `Vector<T>` alias, exact empty nexus/sema documents, and snake_case field emission. The snake_case assertion also failed before its projection correction: `StorePath` had emitted `storePath` rather than `store_path`.

Method: probe cargo test; cargo clippy --all-targets -- -D warnings; nix flake check --no-build -L

The full Rust suite passed (17 tests plus doctests), Clippy passed with warnings denied, and the Nix flake evaluation accepted every declared check.
