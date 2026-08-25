# Ethos-monolith emission audit

Audited claims from flow 01a03603 (ethos-monolith POC realization, 2026-08-25) against direct evidence. The audit is read-only on all product repositories.

## 1. Checkout location and revision

Method: probe `ls /git/github.com/LiGoldragon/ethos-monolith/` and `git rev-parse HEAD; git branch -r --contains cc3ee3221401`

The ethos-monolith checkout lives at `/git/github.com/LiGoldragon/ethos-monolith/`, not under `/home/li/wt/github.com/LiGoldragon/`. HEAD is `cc3ee3221401bf4edec0e6c9b1c1b2ce35e28ff6` and `origin/main` contains it. The revision exists both locally and on the remote.

## 2. Six-path component generation (claim 1)

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/generate.rs`

`ComponentGeneration` declares exactly three source paths (`signal.ethos`, `nexus.ethos`, `sema.ethos`) and three output paths (`signal.rs`, `nexus.rs`, `sema.rs`) derived from a source directory and an output directory. These are the six canonical paths. The `generate()` method at line 149 realizes all three Ethos sources into `Interface` values, projects each to a `GeneratedArtifact`, runs `rustfmt --edition 2024` on each, writes all three to `.pending` files first, and only then renames them to the output paths. If any source fails, pending files are cleaned up and no output is installed.

### Signal output content

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs` lines 1944-2067 and `/git/github.com/LiGoldragon/signal-orchestrate/src/generated/signal.rs`

The signal projection (`signal_rust_source`) emits:
- A source-owned binding: `Channel.{Name ContractId WireRevision}` parsed at line 544 produces `OrchestrateWire` implementing `WireContract` with `ContractBinding::new(ContractId::new(NonZeroU32::new(1)), WireRevision::new(NonZeroU16::new(4)))`.
- Dotos encode/decode traits for each declared type (codecs).
- rkyv Archive/Serialize/Deserialize derives on every structural type (frames).
- An exact concrete Datom projection: each named struct, typedef, and enum gets `DotosEncode`/`DotosDecode` and `EthosValueEncoding`/`EthosValueDecoding` implementations built from the parsed field names.
- `signal_channel!` macro invocation with the channel name, contract type, operations, and a closed reply enum.
- A `Request` type alias.

### Rustfmt as required generation phase (decision 11)

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/generate.rs` lines 26-56, 181-186

`RustFormatting::rustfmt()` runs `rustfmt --edition 2024 --emit stdout` on each artifact's content. Failure produces `GenerationError::FormatRust`. This is invoked at line 181 on every artifact.

### Atomic three-source installation (decision 12)

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/generate.rs` lines 187-216

All three sources are realized into `GeneratedArtifact` values at lines 187-192 before any output is written. Pending files are written at lines 195-204; if any write fails, all pending files are removed. Only after all three succeed are the files renamed from `.pending` to their final paths at lines 205-215. A partial-install is impossible: either all three are installed or none.

**Witnessed: CONFIRMED.**

## 3. Contract repos use Ethos triplets and commit only projections (claim 2)

### signal-orchestrate

Method: probe `git rev-parse HEAD; grep '^version' Cargo.toml` in `/git/github.com/LiGoldragon/signal-orchestrate`

Revision `d23fb6430eda87e16a6f08899f02f013ece0803b`, version `0.16.1`.

Method: probe `find /git/github.com/LiGoldragon/signal-orchestrate -type f \( -name '*.ethos' -o -name '*.rs' \) | grep -E '(ethos|generated)'`

Ethos sources: `ethos/signal.ethos` (contains `Channel.{Orchestrate 1 4}`), `ethos/nexus.ethos` (empty Interface), `ethos/sema.ethos` (empty Interface). Committed generated: `src/generated/mod.rs`, `src/generated/signal.rs`, `src/generated/nexus.rs`, `src/generated/sema.rs`. The `src/` tree contains only `lib.rs` and the `generated/` subtree; no handwritten Rust source beyond the module re-export.

### meta-signal-orchestrate

Method: probe `git rev-parse HEAD; grep '^version' Cargo.toml` in `/git/github.com/LiGoldragon/meta-signal-orchestrate`

Revision `ebefb65c707629a416e1ff3ba785bcaf4b47d0ea`, version `0.10.1`.

Method: probe `find /git/github.com/LiGoldragon/meta-signal-orchestrate -type f \( -name '*.ethos' -o -name '*.rs' \) | grep -E '(ethos|generated)'`

Ethos sources: `ethos/signal.ethos` (contains `Channel.{MetaOrchestrate 2 3}`), `ethos/nexus.ethos` (empty Interface), `ethos/sema.ethos` (empty Interface). Committed generated: identical module structure. `src/` contains only `lib.rs` and the `generated/` subtree.

**Witnessed: CONFIRMED.**

## 4. Build-time byte comparison (claim 3)

Method: code read `/git/github.com/LiGoldragon/signal-orchestrate/build.rs` and `/git/github.com/LiGoldragon/meta-signal-orchestrate/build.rs`

Both `build.rs` files are structurally identical:
1. Copy Ethos inputs to `$OUT_DIR/ethos-generated` via `ComponentGeneration::new(root.join("ethos"), &generated_directory).generate()`.
2. For each of `signal.rs`, `nexus.rs`, `sema.rs`: read the generated file from `$OUT_DIR` and the committed file from `src/generated`, then `assert_eq!(generated, committed, "committed {module} is stale against Ethos source")`.

### Direct byte-compare probe

Method: probe `diff` between most recent `target/debug/build/*/out/ethos-generated/*.rs` and `src/generated/*.rs` in both repos

All six file pairs (3 per repo) are byte-identical.

### Perturbation probe

Method: probe copy of signal-orchestrate to scratch, `sed -i 's/PathLockName/PathLockLabel/g' ethos/signal.ethos`, `cargo clean && cargo build`

The build failed with: `thread 'main' panicked at build.rs:31:9: assertion 'left == right' failed: committed signal.rs is stale against Ethos source`. The generated output in `$OUT_DIR` contained `PathLockLabel` (16 occurrences) and zero occurrences of `PathLockName`, confirming the output changed in response to the input change and the byte-compare rejected the stale committed file.

### Generated contract integration test

Method: code read `/git/github.com/LiGoldragon/signal-orchestrate/tests/generated_contract.rs`

The test `build_generates_only_in_cargo_out_dir_and_checks_committed_projection` independently asserts the build script generates in `OUT_DIR` and compares against committed projections. The test `generated_contract_textualizes_register_and_release` verifies `OrchestrateWire::BINDING.contract().value() == 1` and `revision().value() == 4`, constructs and round-trips every declared type through Datom encode/decode, and frames a register request through the Signal wire protocol.

**Witnessed: CONFIRMED.**

## 5. Generation is input-driven, not template/hardcoded (asked to establish)

Method: code read of the entire generation pipeline: `src/fixture/mod.rs` (parser/projector), `src/generate.rs` (orchestrator)

The generation path is: read Ethos text from disk -> parse through a `Protos` `RealizeWalk` into an `Interface` struct with typed `Channel`, `Inputs`, `Outputs`, `Refusals`, `Streams`, `Types` sections -> validate all type references resolve within the document -> project to Rust source code by iterating the parsed structure and emitting Rust fragments parameterized by the parsed names, types, and field lists -> run `rustfmt` -> install.

There is no template file, no hardcoded type name, no fixture-specific branch in the projection code. Type names, field names, enum variants, channel names, contract IDs, and wire revisions all come from the parsed `Interface` struct.

Method: probe perturbation (described above)

Renaming `PathLockName` to `PathLockLabel` in the Ethos source produced output containing only `PathLockLabel` and no `PathLockName`. This rules out template or hardcoded output.

Method: probe `cargo test` in ethos-monolith (18 tests, all pass)

The generation tests at `tests/generate.rs` write fresh Ethos source text to temporary directories and generate from it. The test `generation_emits_the_three_checked_interface_modules` writes three Ethos sources with `SignalMessage`, `NexusMessage`, `SemaMessage` type names, generates, and verifies the output contains `pub struct SignalMessage(pub String)`. This independently confirms generation is driven by the source text, not by any fixture.

**Witnessed: CONFIRMED.**

## 6. Unsupported construct boundaries (claim 4)

### Imports

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs` line 1947

In Signal projection (`signal_rust_source`), non-empty imports return `Err(InterfaceFault::Shape)` at line 1947-1949. This is an explicit generation error.

In non-signal projection (`rust_source` used for nexus/sema), there is no imports check. The `validate()` method does not reject non-empty imports. The `rust_source()` method simply does not emit import-related code. If a nexus.ethos or sema.ethos contained imports, they would be parsed successfully and silently ignored in the output.

**Observation**: imports in Signal are an explicit error. Imports in nexus/sema are silently dropped, not explicitly errored. The ARCHITECTURE.md acknowledges this nuance with "rejected or not selected by the relevant projection" (line 46-48).

### Interactions

Method: probe `grep -rn -i 'interaction' . --include='*.rs'` in ethos-monolith

The word "interaction" appears only in `ARCHITECTURE.md` as "trait interactions". No parser, validator, or projector code references interactions. The Interface grammar has exactly five positional sections (inputs, outputs, refusals, streams, types). The parser at line 1142-1151 rejects any section count other than exactly 5 with `InterfaceFault::ExtraPosition` or `InterfaceFault::MissingPosition`. An interaction section cannot be expressed in the grammar and would be rejected structurally.

**Observation**: interactions cannot be expressed in the current Interface dialect. They are rejected by the positional parser's structure, but there is no named "unsupported interactions" error message.

### Unconstrained generic parameters

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs` lines 517-528

The `type_reference()` function supports only `Vector<T>` where T recursively resolves. The `symbol()` function at line 481-494 requires all characters to be ASCII alphanumeric or underscore, starting with uppercase. Characters like `<` and `>` fail `symbol()`. Therefore:
- `Map<K,V>` would fail `symbol()` validation with `InterfaceFault::Symbol`.
- `Vector<UnknownType>` would pass `type_reference()` but fail `knows_type()` during `validate()` with `InterfaceFault::UnknownType`.

**Observation**: unconstrained generic parameters are explicit validation errors. CONFIRMED.

### Streaming runtime declarations

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs` lines 2023-2033

The Signal projection checks `if !self.streams.0.is_empty()` and EMITS a `Stream` enum with full rkyv and Dotos derives if streams are populated. The non-signal `rust_source()` at line 1920-1925 always emits a `pub enum Stream { ... }` block. Neither projection rejects non-empty streams as an error.

**Observation**: populated stream sections would be emitted as Rust enums, not rejected as errors. The ARCHITECTURE.md says they "remain outside this POC and are rejected or not selected by the relevant projection" (line 46-48). In practice, both actual contracts have empty stream sections, so the question does not arise for the committed sources. However, the code does not enforce an error for populated streams. The distinction may be between the structural Stream enum (which is emitted) and actual streaming runtime infrastructure (which is not generated), but the code does not distinguish these.

### Summary of unsupported boundaries

| Construct | Signal projection | Non-signal projection |
|---|---|---|
| Non-empty imports | Explicit error | Silently ignored |
| Interactions | Cannot be expressed in grammar | Cannot be expressed in grammar |
| Unconstrained generics | Explicit validation error | Explicit validation error |
| Populated streams | Emitted as enum, no error | Emitted as enum, no error |

**Witnessed: PARTIALLY CONFIRMED.** Imports in Signal and unconstrained generics are explicit errors. Interactions are structurally rejected by the parser. Populated streams are emitted, not rejected. The claim that all four are "explicit generation errors" holds for imports-in-signal and unconstrained generics, holds structurally (but without a named error) for interactions, and does not hold for streams.

## 7. Full test suite

Method: probe `cargo test` in `/git/github.com/LiGoldragon/ethos-monolith`

18 tests plus doctests, all passed. Test names and counts match the witness from flow 01a03603.

Method: probe `cargo build` in `/git/github.com/LiGoldragon/signal-orchestrate` and `/git/github.com/LiGoldragon/meta-signal-orchestrate`

Both builds succeeded (the build scripts are the byte-compare gate).
