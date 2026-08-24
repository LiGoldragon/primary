# Ethos emitter

The emitter now has a real, explicit component generation operation. It reads `signal.ethos`, `nexus.ethos`, and `sema.ethos`, validates every source before output installation, writes pending projections, and installs `signal.rs`, `nexus.rs`, and `sema.rs` only after all projections are ready.

The supported signal contract grammar adds one source-owned binding directly after the Interface header: `Channel.{Name ContractId WireRevision}`. It emits `NameWire`, `NameRequest`, `NameReply`, a `signal_channel!` declaration, Signal frame aliases, and local named carrier textual implementations. Input entries form operations and Output entries form the closed reply. Existing nominal `String`/`Integer`, structs, closed enums, nested data variants, and `Vector<T>` are supported; `Vector<T>` emits `Vec<T>` when `T` is local. Generated Rust field names are snake_case projections of their source type names, so `OrdinarySocketPath` becomes `ordinary_socket_path`.

The marker derives `Debug`, `Clone`, `Copy`, `PartialEq`, and `Eq`, satisfying bound-frame structural tests. A named struct deliberately renders/parses as `Name.{...}`, and a named scalar/newtype as `Name.value`; `DotosSource::new(text).parse::<Payload>()` is the parse API. This is generator-owned behavior because the standard Dotos derive only gives structs a bare brace body. It leaves the generated request/reply envelope internal: the concrete payload carries command-line text rather than an operation enum wrapper. All local/refusal/stream closed enum derivations use absolute Dotos paths, allowing enums carried by those named structs to compile without consumer imports. The pinned emitter revision is `8a3bec1ea0745aac0a5c0837837e5a795814575b`, pushed to `main`.

The unfinished boundary is intentional and explicit: imports, interaction syntax, unconstrained generic parameters, and streaming runtime declarations are not emitted by this POC. Channel identity and both wire-binding integers are required in source rather than inferred from a consuming Rust crate.

## Sources

- Vision/ethos.md
- Vision/ethosMonolith.md
- flows/aa4c7747/vision/ethosTraitSyntax.md
- flows/aa4c7747/vision/tuples.md
- flows/2b34fafa/vision/ethosSourceFiles.md
- flows/01a03603/witnesses/ethosEmitter.md
