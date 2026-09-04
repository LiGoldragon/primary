# ethos-zero ProtoformStack rewrite

Subflow of 6329f1. Thread: ethos-zero realization.

## What was read

1. Flow log at flows/6329f1/log.md (the design spec, whole)
2. Vision/ethos.md, Vision/datom.md, Vision/protos.md (referenced, not re-read; the spec covers them)
3. ethos-zero origin/main (b922afb): src/lib.rs (2562 lines), tests/file_contract.rs, Cargo.toml, flake.nix, ethos-zero.ethos, signal.ethos, cli/, nexus/, meta-cli/
4. signal-orchestrate origin/main: src/generated/signal.rs (the current wire contract shape), ethos/signal.ethos
5. protos origin/main (bfde3b8): src/lib.rs (public API: Portion, Delineatable, EnclosedAnatomy, PortionViewing)
6. datomic origin/main (b670c72): src/lib.rs (public API: Datomic, PortionViewing, PortionBuilding, TextEdge)
7. protos origin/ProtoformStack (630fa17): src/lib.rs (new API: Protoform, Structural, Printing, Protosizable, Potential)
8. datomic: no ProtoformStack branch found

## What was written

### ethos-zero branch ProtoformStack, rev 33d85a85

**Removed**: Interface/Schema roots, Channel, Visibility enum, named struct fields, Manifest/DatomicManifest, FileReader/RustEmitter structs, Nexus workspace (nexus/, cli/, meta-cli/), signal.ethos, meta-signal.ethos, AGENTS.md. The old 2562-line lib.rs is replaced entirely.

**Written** (in order):

1. `Cargo.toml` -- single package, version 1.0.0, lib + [[bin]], no workspace; deps on current protos (bfde3b8) and datomic (b670c72)
2. `src/lib.rs` (1460 lines) -- concept types, reader, emitter:
   - Concept types: Version, Import, TypeExpression, Variant, TypeDeclaration, Receiver, Capability, AssociatedType, AssociatedConstant, KindConstraint, KindDeclaration, Association, SectionReference, Library, Signal, Concept
   - Reader (`pub fn read`): Text -> Delineation -> Portion walk -> Concept; handles sweet and full forms
   - Emitter (`pub fn emit`): Concept -> quote tokens -> syn::File -> Rust text; generates Datomic impls for every type; generates traits, association assertions; for Signal adds rkyv derives and wire envelope (Frame, Body, Refusal, Version)
3. `src/main.rs` (185 lines) -- CLI binary: `ethos-zero 'Generate.{ path out }'` speaks datom; no-arg prints self-description
4. `ethos-zero.ethos` -- self-description as Signal root
5. `fixtures/orchestrate.ethos` -- orchestrate Lock signal in new format
6. `fixtures/example-library.ethos` -- Library with types, kinds, associations
7. `tests/file_contract.rs` (30 tests) -- reader tests (sweet/full form, imports, types, kinds, associations), emitter tests (parseable Rust, trait generation, Datomic impls), fixture tests
8. `flake.nix` -- simplified: removed signal-orchestrate/meta-signal-orchestrate inputs and workspace build args
9. `ARCHITECTURE.md`, `README.md`, `UPGRADES.md`, `CLAUDE.md` -- rewritten for the new shape

## Reader grammar

| Ethos | Reader produces |
|---|---|
| `Library.{major minor patch} [imports] [types] [kinds] [associations]` | Concept::Library |
| `Signal.{major minor patch} [imports] [requests] [responses] [types]` | Concept::Signal |
| `Library.{ {ver} [imports] [types] [kinds] [associations] }` | Concept::Library (full form) |
| `source:Name` | Import::Single |
| `source:[ N1 N2 ]` | Import::Multiple |
| `Name.{ T1 T2 }` | TypeDeclaration::Struct (tuple struct) |
| `Name.[ V1 V2 ]` | TypeDeclaration::Enum |
| `Name.Type` | TypeDeclaration::Alias |
| `Name.\u{00AB}K V\u{00BB}` | TypeDeclaration::Map |
| `Bare` inside enum | Variant::Unit |
| `Name.Type` inside enum | Variant::Typed |
| `Name.{ T1 T2 }` inside enum | Variant::InlineStruct |
| `Name.[ V1 V2 ]` inside enum | Variant::InlineEnum |
| `Name.[ caps ]` | KindDeclaration::Simple |
| `Name.{ [superkinds] [assoc-types] \u{00AB}constants\u{00BB} [caps] }` | KindDeclaration::Complex |
| `cap.[ T ]` | Capability (Shared, no inputs) |
| `cap!{ [inputs] [yield] }` | Capability (Mutable, with inputs) |
| `cap:[ T ]` | Capability (None, no inputs) |
| `Type.[ Kinds ]` | Association |

## Emitter mapping (ethos to Rust)

| Ethos construct | Generated Rust |
|---|---|
| `Name.{ T1 T2 }` | `pub struct Name(pub T1, pub T2);` |
| `Name.[ V1 V2.T ]` | `pub enum Name { V1, V2(T) }` |
| `Name.Type` | `pub type Name = Type;` |
| `Name.\u{00AB}K V\u{00BB}` | `pub type Name = BTreeMap<K, V>;` |
| `Text` | `protos::Text` (= String) |
| `Integer` | `i64` |
| `Decimal` | `f64` |
| `Boolean` | `bool` |
| `Meaning` | `datomic::Meaning` |
| `Vector<T>` | `Vec<T>` |
| `Option<T>` | `Option<T>` |
| `Result<T E>` | `Result<T, E>` |
| `Self` | `Self` |
| Kind | `pub trait Name: Superkinds { type Assoc: Bounds; const C: T; fn cap(&self) -> T; }` |
| Association | `const _: () = { fn assert<T: Kind>() {} let _ = assert::<Type>; };` |
| Every declared type | `impl datomic::Datomic for Name { fn embody(...) fn portion(...) }` |
| Signal types | rkyv derives on every type |
| Signal wire | `Frame(Version, Body)`, `Body { Request, Reply, Refusal }`, `Refusal { VersionMismatch, Unreadable }` |

## Judgment calls (this subflow's)

1. **Current protos/datomic API**: Built against current protos 0.14.0 (Portion-based) and datomic 0.7.1 (embody/portion) because datomic's ProtoformStack branch does not exist yet. The reader walks Portions directly; the emitter generates current-API Datomic impls. When both ProtoformStack branches are pushed, pin them and adapt (Protoform replaces Portion, incorporate/datomize replace embody/portion).

2. **Comment syntax**: Fixture files use `;;` comments (current protos 0.14.0). The spec and new protos 0.15.0 use single `;`. Will update when protos dep moves to ProtoformStack.

3. **Kind constraints syntax**: The spec shows `Name<constraints>.body` which faults in current protos (separator after closer = MissingHead). Constraints are supported inside the complex kind body as an Angled first element: `Name.{ <constraints> [superkinds] ... }`. Will update syntax if the new protos parser supports the name-level form.

4. **Nexus removal**: The Nexus runtime, edge CLIs, signal-ethos-zero dependency, and signal-frame integration are removed. The spec says the CLI is a direct tool. UPGRADES.md documents how to migrate.

5. **Version 1.0.0**: Complete rewrite of the public API (FileReader/RustEmitter removed, read/emit free functions added, all concept types redesigned). Major version bump signals the break.

6. **No generated module committed yet**: The spec says "the generated module is committed." The self-bootstrap test (ethos-zero reads its own ethos and emits parseable Rust) passes, but the committed generated file is deferred until the API stabilizes with the new protos/datomic.

## Witnessed test results

```
cargo test: 34 tests passed (30 integration + 4 CLI unit)
cargo clippy --all-targets -- -D warnings: clean
cargo fmt --check: clean
```

`nix flake check` not run (requires remote builder; the flake inputs need updating to ProtoformStack revs before it would fully pass).

## Pushed rev

`ProtoformStack` at `33d85a85` on `origin` in `ethos-zero`.

## Left undone

1. **Pin ProtoformStack protos and datomic**: protos origin/ProtoformStack exists (630fa17) but datomic does not. Once both exist, update Cargo.toml and flake.nix input revs, adapt the reader (Protoform API) and emitter (incorporate/datomize), and run `nix flake check`.

2. **End-to-end compilation test**: A fixture-generated Rust module compiled against real protos and datomic crates. Blocked on ProtoformStack datomic.

3. **Datom round-trip proptest**: Round-trip test through datom text for every generated type. Requires the new datomic Datom type.

4. **Self-bootstrap committed module**: The generated Rust for ethos-zero.ethos should be committed. Deferred until API stabilizes.

5. **Single-`;` comments**: Update fixture files and reader when protos dep moves to 0.15.0.

## Sources

- flows/6329f1/log.md (design spec)
- ethos-zero origin/main b922afb (existing codebase)
- signal-orchestrate origin/main a597f1a (wire contract reference)
- protos origin/main bfde3b8 and origin/ProtoformStack 630fa17
- datomic origin/main b670c72
