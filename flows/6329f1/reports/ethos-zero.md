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

1. **Nexus removal**: The Nexus runtime, edge CLIs, signal-ethos-zero dependency, and signal-frame integration are removed. The CLI is a direct tool. UPGRADES.md documents migration.

2. **Version 1.0.0**: Complete rewrite. Major version bump signals the break.

3. **Conceptual<Concept> for Datom via protosize**: The `Datom::conceive()` impl protosizes the datom back to a protoform and reads from that. This preserves the structural reading logic while honoring the layer design.

4. **E2e test skipped in Nix sandbox**: The isolated Cargo project needs network access for the rkyv crate from crates.io. Skipped when `NIX_BUILD_TOP` is set. The flake's build and clippy checks compile the generated code at the crate level.

## History

### Initial rewrite (33d85a85)
Rewrote ethos-zero 1.0.0: Library/Signal roots, datom CLI, wire envelope.

### Corrections (907d015e)
No free functions: `Actualizing` and `Emitting` kinds. Fully qualified intrinsic names.

### ProtoformStack integration (52c975e4)
Pinned protos 317a771 and datomic e448736. Protoform/Head/Qualified API, incorporate/datomize.

### Final pins and layers (c85e9f76)
Pinned protos 56c683e, datomic 768426e. Corporal/Datomic split, Protosizable, Conceptual, RustLibrary, bootstrap module.

### Honest completion (b869598d)
Full Protosizable, Corporal/Datomic split, e2e compile test, nix flake check pass.

### Emitter gap fixes (f2211ac6)
1. Signal aliases always emit `pub type Name = Target;` (no single-field structs). No Corporal/Datomic impls for aliases; the underlying type carries them. `Release.42` is now a bare integer.
2. Wire types (Version, Refusal, Body, Frame) get Corporal and Datomic impls. A refusal prints as `VersionMismatch.{ { 1 0 0 } { 0 9 0 } }` or `Unreadable`.
3. E2e test asserts `Release.42`, Lock text unchanged, and both Refusal forms through datom text.
4. All checks re-run: cargo test 41 passed, clippy clean, fmt clean, nix flake check all passed.

## Witnessed test results

```
cargo test: 41 tests passed (37 integration + 4 CLI unit)
cargo clippy --all-targets -- -D warnings: clean
cargo fmt --check: clean
nix flake check -L --builders 'ssh://prometheus': all checks passed
```

## Pushed rev

`ProtoformStack` at `f2211ac6` on `origin` in `ethos-zero`.

## Left undone

1. **Datom round-trip proptest**: Deferred (not cheap enough for this commit).

## Sources

- flows/6329f1/log.md (design spec)
- ethos-zero origin/main b922afb (existing codebase)
- protos origin/ProtoformStack 56c683e (0.15.0)
- datomic origin/ProtoformStack 768426e (0.8.0)
- flows/6329f1/reports/api-deviations.md (Corporal, Head/Qualified, separator fix, incorporate split)

## Re-pin: datomic a27f9b8e (185f13a9)

Datomic ProtoformStack moved to a27f9b8e: structural faults datomize without Debug format. 
Cargo.toml and flake's `datomic-map` input updated. No generated code changes needed; 37 tests pass, 
clippy clean, nix flake check pass through prometheus. Pushed as 185f13a90354.
