# Ethos emitter

Method: code read /git/github.com/LiGoldragon/ethos-monolith/src/generate.rs, /git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs, and /git/github.com/LiGoldragon/ethos-monolith/tests/generate.rs

The prior component surface derived six canonical paths but did not realize source or write emitted Rust. The committed implementation realizes all three Interface documents before it writes pending artifacts, then installs the three projections. `signal.ethos` is channel-bearing and emits a source-owned Signal binding, macro channel, request alias, and closed reply. `nexus.ethos` and `sema.ethos` retain ordinary Interface output.

Method: probe cargo test --test generate

Before implementation, the added generation tests failed to compile because `GenerationError` and `ComponentGenerationOperations::generate` did not exist. After implementation the generation tests passed, including source failure before installation, the three output artifacts, a `Vector<T>` alias, exact empty nexus/sema documents, and snake_case field emission. The snake_case assertion also failed before its projection correction: `StorePath` had emitted `storePath` rather than `store_path`.

Method: probe cargo test; cargo clippy --all-targets -- -D warnings; nix flake check --no-build -L

The full Rust suite passed (17 tests plus doctests), Clippy passed with warnings denied, and the Nix flake evaluation accepted every declared check.

Method: code read /git/github.com/LiGoldragon/dotos/src/codec.rs and /git/github.com/LiGoldragon/dotos/derive/src/lib.rs

The standard `DotosEncode` derive for a named struct writes only its brace body and its decoder accepts that body; it does not retain a `Name.` head. The supported concrete payload API is `DotosSource::new(text).parse::<Payload>()`, not `FromStr`. Therefore the generator must own named-head behavior rather than consumers adding a parallel textual layer.

Method: probe cargo test --test generate generation_emits_comparable_wire_marker_and_named_struct_textual_heads

The regression initially failed because the generated Wire marker lacked `Debug`, `PartialEq`, and `Eq`. After the correction it passed. The generated signal module gives each Wire marker `Debug`, `Clone`, `Copy`, `PartialEq`, and `Eq`; named structs render and require `Name.{...}`; named scalar/newtype carriers render and require `Name.value`. The test covers both `PathLock.{...}` and `PathLockName.value` output paths and rejects a bare payload form by emitting only the dotted-application decoder.

Method: probe cargo test; cargo clippy --all-targets -- -D warnings; nix flake check --no-build -L

The follow-up suite passed (18 tests plus doctests), with Clippy warnings denied and all declared Nix checks accepted. Revision `3c76cddc3374fa93a07f9b45c651f3bf91d1cdc7` is superseded by the pinned correction below.

Method: downstream consumer compile report, then probe cargo test; cargo clippy --all-targets -- -D warnings; nix flake check --no-build -L

The consumer compile discovered that the generator's local/refusal/stream enum derivations still named Dotos traits without a path after unused imports were removed. The correction emits absolute `::dotos::DotosEncode` and `::dotos::DotosDecode` derive paths for every enum family. The named-head regression now includes `PathLockRegistrationRefusal` inside `PathLock`, then passed with the full 18-test suite, denied-warning Clippy, and all Nix checks. Revision `8a3bec1ea0745aac0a5c0837837e5a795814575b` is pushed on ethos-monolith `main`.
