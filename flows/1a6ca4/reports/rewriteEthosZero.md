# Rewrite: ethos-zero

## What was yanked

| Item | Why |
|---|---|
| `Version` type and version parsing | Vision/ethos.md: "An ethos file carries no version; datom has no versions" |
| `Library` and `Signal` root variants (old shape) | Replaced by four variant-headed File variants: Types, Kinds, Signal, Sema |
| `TypeDeclaration::Map` and guillemet support | Vision/protos.md: "The key-value map, and the guillemets that delimited it, are dropped entirely from protos" |
| `SectionReference` type | Signal requests/responses are now `Variant` values directly, not separate reference types |
| `Corporal<C>` trait references in generated code | Replaced by `Datomic::incorporate_from` per datomic 0.11.0 rewrite |
| `Datomic::datomize` in generated code | Replaced by `Conceivable<Datom>::conceive` per datomic 0.11.0 |
| `Structural`/`Printing` trait references | Replaced by `Protosizable`/`Textualizable` per protos 0.17.0 |
| `Conceptual` trait references | Replaced by `Conceivable` per protos 0.17.0 |
| rkyv derives, Frame, Body, Version, Refusal envelope | Vision: no envelope, no Frame; a wire crate that needs a frame declares it as a type |
| `thiserror` dependency | Manual Display/Error impls instead |
| `proptest` dependency | Specific test cases from Vision/ethos.md replace property testing |
| Custom `Potential` wrapper | protos::Potential used directly where needed |
| Custom `Actualizing`/`Emitting` traits | Replaced by protos' `Conceivable<File>` and new `Generating` trait |
| `Enclosure::Guillemets` references | Guillemets dropped from protos |
| `Reply` enum name | Replaced by `Response` |
| `generated.rs` empty module | Removed; self-generation not yet bootstrapped |
| Old test files (`tests/file_contract.rs`) | Replaced by `tests/ethos.rs` with 43 tests |
| Old fixtures (`example-library.ethos`) | Replaced by per-example fixtures from Vision/ethos.md |

## New anatomy

| Module / section | Layer or kind | What it holds |
|---|---|---|
| Declaration model | Concept | `File` enum (Types, Kinds, Signal, Sema), `Import`, `TypeDeclaration`, `Variant`, `TypeExpression`, `KindDeclaration`, `Capability`, `Association`, `AssociatedType`, `AssociatedConstant`, `KindConstraint`, `Receiver` |
| Faults | Fault | `Fault { path, problem }`, `Problem` enum (Protos, Root, Section, Import, Declaration, TypeExpression, Capability, Kind, Association, Generation) |
| `Canonicalizing` | Text → Text | Sweet-to-canonical text conversion: variant head becomes `Head.{ sections }` |
| `Conceivable<File>` | Protoform → File | Reader: `impl Conceivable<File> for Delineation` and `for Protoform` |
| `Protosizable` | File → Protoform | Ascent: `impl Protosizable for File` (Infallible) |
| `Generating` | File → Rust | Generator: `impl Generating for File`, emits Rust via quote/syn |
| Datomic generation | Generated code | For each declared type: `Conceivable<Datom>` + `Datomic::incorporate_from` + `Incorporable<T> for Datom` |

## Ethos File grammar

### Types variant
```
Types
[ imports ]
[ types ]
[ associations ]
```
generates:
```rust
pub struct Record(pub protos::Text, pub protos::Integer);
// + Conceivable<Datom>, Datomic, Incorporable impls
const _: () = { fn assert_record_summarizable<T: Summarizable>() {} let _ = assert_record_summarizable::<Record>; };
```

### Kinds variant
```
Kinds
[ imports ]
[ kinds ]
```
generates:
```rust
pub trait Summarizable { fn summarize(&self) -> protos::Text; }
pub trait Streamable: Fillable { type Item: Serializable; const CAPACITY: protos::Integer; fn next(&mut self) -> Option<Self::Item>; }
```

### Signal variant
```
Signal
[ imports ]
[ request-variants ]
[ response-variants ]
[ types ]
```
generates:
```rust
// types with Datomic impls
pub enum Request { Lock(LockRequest), Release(LockId), ... }
pub enum Response { Locked(Lock), LockRejected(LockRejection), ... }
// + Datomic impls for Request and Response
```

### Sema variant
```
Sema
[ imports ]
[ types ]
```
generates: types with Datomic impls (implied Datomic associations).

## Decisions on flow authority

| Decision | Rationale |
|---|---|
| Signal sections: `[ imports ] [ requests ] [ responses ] [ types ]` generating `Request` and `Response` | Main flow suggested this layout; `Response` chosen over `Reply` per brief ("Reply is gone"); `Request` matches the vision's Types example |
| Sema sections: `[ imports ] [ types ]` | Minimal and real per brief; no consumer exists; Datomic is implied for all types; no explicit associations section needed |
| Implied kind associations generate Datomic only | Brief: "What 'implied kind associations' generate today: Datomic for every type; any signal-specific kind does not exist yet and is not invented" |
| Generated module file name: `<stem>.rs` for every variant | Brief directive; no more `signal.rs` special case |
| Recursion boxed via datomic's blanket `Incorporable<Box<T>>` + `impl_datomic_box!` macro | Reuses what datomic 0.11.0 provides; the blanket handles Incorporable, the macro handles Conceivable+Datomic for Box<T> (orphan rule) |
| Import resolution: explicit import = intrinsic name = fully qualified in generated Rust | Vision: "An explicit import and an intrinsic name mean the same thing. The generated code carries no `use` statements; each imported name is written fully qualified" |
| Ethos NOT read through datomic | Brief sets the question aside: "read Protoform directly through your own Conceivable"; Conceivable<File> for Delineation reads the structural form directly |
| Associated constants in brackets: `[ CAPACITY.Integer ]` | Guillemets dropped from protos; headed entries in a bracket replace guillemet key-value pairs |
| Capability parameter naming: `input` for single, `input_0`/`input_1` for multiple | Vision example shows `fn push(&mut self, input: protos::Text)` with singular `input` |
| Fault type uses `path: Vec<Integer>` not `extent: Extent` | Paths into the protoform tree are more informative than text extents; the reader does not track extents |

## Commits and versions

| Crate | Old version | New version | Commit (main) |
|---|---|---|---|
| ethos-zero | 1.3.1 | 2.0.0 | `a2e8eafcd45c` |
| protos (ethos files only) | 0.17.0 | 0.17.1 | `2cb88849f3b1` |
| datomic (ethos files only) | 0.11.0 | 0.11.1 | `cf59b01bbbc8` |

Protos and datomic Rust code unchanged. Their .ethos declarations split from one file into Types + Kinds files to match the new variant-headed grammar.

ethos-zero Cargo.toml pins protos `c5594f9d6f73` and datomic `2c2e2073fd34` (Rust code).
ethos-zero flake.nix pins protos `2cb88849f3b1` and datomic `cf59b01bbbc8` (with fixed .ethos files).

## Test and build output

### cargo test
```
test result: ok. 43 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

### cargo clippy
```
Finished `dev` profile [unoptimized + debuginfo]
```
Clean, no warnings.

### nix build
Success (ethos-zero-2.0.0), built on remote builder prometheus.

## Left hanging

| Item | Why |
|---|---|
| Self-generation (eat own food) | The crate does not yet generate its own contract module from ethos-zero.ethos with a freshness test; the self-description reads and prints the .ethos file but does not generate a committed .rs from it. This requires the Signal generation to produce compilable Rust against the crate's own types, which is a bootstrap problem (the generated types depend on the crate that generates them). Deferred to a follow-up. |
| Datom round-trip tests on generated types | The compilation tests verify syntax via syn::parse; full round-trip (generate, compile, instantiate, datomize, incorporate) requires spawning a cargo project with network access, which fails in nix sandbox. A proper e2e test needs a nix-provided test harness. |

## Sources

- Vision/ethos.md — distilled vision for ethos (authority)
- Vision/protos.md — distilled vision for protos (authority)
- Vision/datom.md — distilled vision for datom (authority)
- Vision/ethosMonolith.md — ethos-monolith vision (authority)
- Intent/mandatoryTraits.md — mandatory traits intent (authority)
- Intent/data.md — everything is data intent (authority)
- flows/995a164e/vision/rust.md — freestanding implementations forbidden
- flows/995a164e/vision/layerMatching.md — data in capabilities, no constants
- flows/995a164e/vision/kinds.md — naming, associated types/constants
- flows/995a164e/vision/concept.md — Concept layer, singular
- flows/995a164e/vision/contexts.md — parsing contexts
- flows/995a164e/vision/explodedForm.md — sweet/canonical form naming
- flows/5abf3be8/vision/sectionsExistToConferTraits.md — sections confer traits
- flows/ba906ae2/vision/signalIsOurMessagingLayer.md — signal naming
- flows/1a6ca4/vision/datom.md — "rewrite anatomically and directly"
- flows/1a6ca4/reports/rewriteProtosDatomic.md — protos/datomic rewrite report
