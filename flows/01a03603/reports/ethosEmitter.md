# Ethos emitter

The emitter now has a real, explicit component generation operation. It reads `signal.ethos`, `nexus.ethos`, and `sema.ethos`, validates every source before output installation, writes pending projections, and installs `signal.rs`, `nexus.rs`, and `sema.rs` only after all projections are ready.

The supported signal contract grammar adds one source-owned binding directly after the Interface header: `Channel.{Name ContractId WireRevision}`. It emits `NameWire`, `NameRequest`, `NameReply`, a `signal_channel!` declaration, Signal frame aliases, and structural textual derivations for every local type. Input entries form operations and Output entries form the closed reply. Existing nominal `String`/`Integer`, structs, closed enums, nested data variants, and `Vector<T>` are supported; `Vector<T>` emits `Vec<T>` when `T` is local.

The unfinished boundary is intentional and explicit: imports, interaction syntax, unconstrained generic parameters, and streaming runtime declarations are not emitted by this POC. Channel identity and both wire-binding integers are required in source rather than inferred from a consuming Rust crate.

## Sources

- Vision/ethos.md
- Vision/ethosMonolith.md
- flows/aa4c7747/vision/ethosTraitSyntax.md
- flows/aa4c7747/vision/tuples.md
- flows/2b34fafa/vision/ethosSourceFiles.md
- flows/01a03603/witnesses/ethosEmitter.md
