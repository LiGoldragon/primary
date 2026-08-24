# Ethos emitter

The emitter now has a real, explicit component generation operation. It reads `signal.ethos`, `nexus.ethos`, and `sema.ethos`, validates every source before output installation, writes pending projections, and installs `signal.rs`, `nexus.rs`, and `sema.rs` only after all projections are ready.

The supported signal contract grammar adds one source-owned binding directly after the Interface header: `Channel.{Name ContractId WireRevision}`. It emits `NameWire`, `NameRequest`, `NameReply`, a `signal_channel!` declaration, Signal frame aliases, and local named carrier textual implementations. Input entries form operations and Output entries form the closed reply. Existing nominal `String`/`Integer`, structs, closed enums, nested data variants, and `Vector<T>` are supported; `Vector<T>` emits `Vec<T>` when `T` is local. Generated Rust field names are snake_case projections of their source type names, so `OrdinarySocketPath` becomes `ordinary_socket_path`.

The marker derives `Debug`, `Clone`, `Copy`, `PartialEq`, and `Eq`, satisfying bound-frame structural tests. A named struct deliberately renders/parses as `Name.{...}`, and a named scalar/newtype as `Name.value`; `DotosSource::new(text).parse::<Payload>()` is the parse API. This is generator-owned behavior because the standard Dotos derive only gives structs a bare brace body. It leaves the generated request/reply envelope internal: the concrete payload carries command-line text rather than an operation enum wrapper. All local/refusal/stream closed enum derivations use absolute Dotos paths, allowing enums carried by those named structs to compile without consumer imports.

The direct carrier retains only its outer nominal head. Its named fields recursively use their underlying values, so the concrete lock text is `PathLock.{name [/absolute/path] (description)}`, not nested `PathLockName.`, `PathLockPaths.`, or `PathLockPath.` applications. Direct use of any nominal carrier remains headed. This source-owned embedded projection also applies to vectors and closed enum data variants. The final pinned emitter revision is `d4eae9275686ac84efeb1551fe93d5115a3ba731`, pushed to `main`; its generated output has no unused-binding warnings under consumer `clippy -D warnings`.

A named one-field wrapper around another named struct is flattened at its boundary: `PathLockRegistered.{name [/path] (description)}` and `Configured.{store ordinary meta}`, not double-braced payloads. This is deliberately limited to that one-field nested-struct shape; it does not flatten multi-field carriers or collapse enum variants. Final pinned emitter revision: `41cc747ecf236e543b36cc0106b518eb946717d0`, pushed to `main`.

Generated projections are canonical Rust 2024 formatting, not merely parseable Rust: the generator runs `rustfmt` before installation and rejects a projection if that required formatter is unavailable or rejects it. A data-only closed enum returns its `UnknownVariant` directly instead of emitting a single-binding match, so the committed generated files pass consumer `clippy -D warnings`. Current final pin: `cc3ee3221401bf4edec0e6c9b1c1b2ce35e28ff6` on `main`.

The unfinished boundary is intentional and explicit: imports, interaction syntax, unconstrained generic parameters, and streaming runtime declarations are not emitted by this POC. Channel identity and both wire-binding integers are required in source rather than inferred from a consuming Rust crate.

## Sources

- Vision/ethos.md
- Vision/ethosMonolith.md
- flows/aa4c7747/vision/ethosTraitSyntax.md
- flows/aa4c7747/vision/tuples.md
- flows/2b34fafa/vision/ethosSourceFiles.md
- flows/01a03603/witnesses/ethosEmitter.md
