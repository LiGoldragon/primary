# Dependency crates the lojix stack builds on — state + public API

Reconnaissance for the lojix production-refresh. Every claim below is
grounded in a file read or a `jj` command run on the colocated checkouts
under `/git/github.com/LiGoldragon/`. Versions are `[package].version`
from each `Cargo.toml`; "main HEAD" is `jj log -r main`.

## What lojix actually depends on

lojix's manifest (`/git/github.com/LiGoldragon/lojix/Cargo.toml:26-42`)
declares these git deps, all `branch = "main"` (no rev pins):

- Runtime: `horizon-lib` (horizon-rs), `nota-next`, `meta-signal-lojix`,
  `signal-lojix`, `triad-runtime`, plus crates.io `rkyv`/`rustix`/`tokio`/`thiserror`.
- Build-dependency: `schema-rust-next`.

Direct vs transitive (from `lojix/Cargo.lock`):
- DIRECT in tree: `horizon-lib`, `nota-next`, `triad-runtime`, `schema-rust-next` (build), `signal-lojix`, `meta-signal-lojix`.
- TRANSITIVE only: `signal-frame` (0.2.1) and `schema-next` (0.2.0), each
  present once via `signal-lojix` / `schema-rust-next`
  (`lojix/Cargo.lock:624,553,656-664`).
- NOT a lojix dependency at all (0 occurrences in lock): `sema-engine`,
  `signal-sema`. lojix carries its own checked-in `src/schema/sema.rs`
  generated nouns and talks SEMA through `triad-runtime`'s `NextStep::SemaRead/SemaWrite`
  abstraction, not the engine library.

## Per-crate state

### nota-next — v0.4.0 (DIRECT dep)
- Role: raw NOTA structural floor + structural-macro-node codec for the
  schema-derived stack (`nota-next/ARCHITECTURE.md:1-3`; `lib.rs:1-8`).
- Public surface (`src/lib.rs`): codec (`NotaBlock`, `NotaBody`,
  `NotaDecode`, `NotaEncode`, `NotaDecodeError`, `NotaString`, `ByteSequence`,
  `FixedByteSequence`, ...), macros (`StructuralMacroNode`, `MacroRegistry`,
  `Pattern`, ...), parser (`Document`, `Block`, `Atom`, `Delimiter`,
  `SourceSpan`, `NotaError`), and re-exported derives `NotaDecode`,
  `NotaEncode`, `StructuralMacroNode`.
- main HEAD `065fa2ad` "nota-next: own byte scalar codec" (additive: +152
  in codec.rs, lib.rs +9/-4; new `ByteSequence`/`FixedByteSequence`).
- BREAKING-PIN: lojix lock pins nota-next at `af6a2080` (`lojix/Cargo.lock:397`),
  which is BEHIND main `065fa2ad`. Floating `branch = main` means a `cargo update`
  pulls the new byte-scalar codec.

### schema-rust-next — v0.5.3 (build-dependency; owns the codegen)
- Role: THE modern-schema-syntax Rust emission layer. Lowers
  `schema-next::Schema` / `SchemaSource` into Rust via `quote!`/proc-macro2
  tokens (`schema-rust-next/ARCHITECTURE.md:1-9`). This crate (with
  `schema-next` as its input) owns "the modern schema syntax" codegen.
  lojix's `build.rs` drives it: `schema_rust_next::build::{GenerationDriver,
  GenerationPlan, DependencySchema}` regenerate and `write_or_check` the
  checked-in `src/schema/nexus.rs` + `src/schema/sema.rs`
  (`lojix/build.rs:3,29-37`).
- Public surface: `RustEmitter`, `RustSchemaLowering`,
  `RustSchemaSourceLowering`, `LowerToRust<Target>`, `RustModule`,
  `RustEmissionOptions`/`RustEmissionTarget`/`NotaSurface`, the `Rust*`
  declaration tree, `build::*`, `daemon_emit::*`, `migration::*`.
- main HEAD `cedb2e06` "schema-rust-next: stop emitting nota bridge methods"
  (lib.rs -140; fixtures -1453 lines net).
- **BREAKING for lojix regeneration.** This commit removes the inherent
  `from_nota_block` / `to_nota` bridge methods from generated nouns (the
  `#[derive(NotaEncode/NotaDecode)]` trait impls remain; only the inherent
  convenience methods + the `NotaInherentBridgeTokens`/`NotaEncodeReceiver`
  emitters were deleted — confirmed via `jj diff -r main --git`). lojix's
  CHECKED-IN generated files still carry these bridges (nexus.rs: 64 defs,
  sema.rs: 60 defs of `pub fn from_nota_block`/`pub fn to_nota`). lojix lock
  pins schema-rust-next at `b252e81e` (`lojix/Cargo.lock:564`), BEHIND main
  `cedb2e06`. Bumping the pin and re-running the build's `write_or_check`
  freshness gate will REWRITE both files (dropping ~124 inherent method
  defs); a stale checked-in file fails the gate (`build.rs:36`).
- Mitigating fact: NO hand-written lojix code calls these as inherent
  methods. `grep from_nota_block|to_nota( ` outside `src/schema/` returns
  nothing; lojix only uses the `NotaDecode`/`NotaEncode` *traits* and
  `derive`s (`src/schema/nexus.rs:53,56`, `src/lib.rs:95`). So the break is
  regeneration-of-artifacts only, not a source-call compile break.

### schema-next — v0.2.0 (TRANSITIVE, via schema-rust-next)
- Role: turns NOTA structure into typed schema source data — the schema
  semantic engine; `.schema` is a NOTA dialect (`schema-next/ARCHITECTURE.md:1-3`).
  Input layer for schema-rust-next; together they ARE the modern schema codegen.
- Public surface: `Schema`, `SchemaSource`, `SchemaEngine`, `SchemaError`,
  the declaration tree (`Declaration`, `EnumDeclaration`, `StructDeclaration`,
  `Name`, `TypeReference`, `Visibility`, ...), `MacroRegistry`/macro types,
  `upgrade::*` migration types, and re-exports from nota-next.
- main HEAD `2397d5b2` "schema-next: add scoped enum type reference" (additive).
- Pin note: lojix lock pins `ccdf5487` (`lojix/Cargo.lock:555`), behind main.
  Additive; no observed break, but moves with schema-rust-next bumps.

### signal-frame — v0.2.1 (TRANSITIVE, via signal-lojix)
- Role: the wire kernel — frame envelope, length-prefixed rkyv archives,
  handshake, exchange ids, async correlation, reply/event shape; base contract
  crate, renamed successor to `signal-core`; the six Sema verbs moved out to
  `signal-sema` (`signal-frame/ARCHITECTURE.md`).
- Public surface: `Request`/`RequestBuilder`/`RequestPayload`, `Caller`,
  `FrameError`, `exchange`, `frame`, `Revision`/`Slot`, `SignalOperationHeads`,
  `signal_channel!`/`legacy_signal_channel!` macros, `version::*`.
- main HEAD `166bda84` "update signal cli example to signal-spirit".
- lojix lock pins `166bda84` = CURRENT main. No break.

### triad-runtime — v0.6.1 (DIRECT dep)
- Role: shared runtime for schema-derived Signal/Nexus/SEMA daemons —
  trace logging, rkyv frame transport, Unix listener shells, `Runner::drive`,
  `NextStep`, argument parsing (`triad-runtime/ARCHITECTURE.md:1-14`).
- Public surface: `kameo` re-export, `argument::*`, `async_runtime::*`,
  `daemon::*`, `FrameBody`/`LengthPrefixedCodec`, `ConnectionContext`,
  **`BindingSurface`** (formerly `DaemonConfiguration`), `ExitReport`,
  `role::*`, `runner::{Runner, NextStep, ...}`, `streaming::*`, `trace::*`,
  `BoundedWorkers`.
- main HEAD `6ea83162` "rename DaemonConfiguration trait to BindingSurface".
- lojix lock pins `6ea83162` = CURRENT main, so already consistent.
- Rename impact on lojix: NONE. lojix uses `Runner`, `NextStep`,
  `NexusAction`, `ComponentCommand`, `FrameBody`, `LengthPrefixedCodec`,
  `ContinuationLimit`, the `Sema{Read,Write}{Input,Output}` traits — NOT the
  renamed trait. lojix's own `DaemonConfiguration` (`lojix/src/lib.rs:119`) is
  a local type, unrelated to the triad-runtime trait.

### sema-engine — v0.2.3 (NOT a lojix dependency)
- Role: full typed database engine library over `sema` + `signal-sema`;
  registered record families, operation execution, log/snapshot/subscription
  (`sema-engine/ARCHITECTURE.md:1-13`). First consumer is `mind`; lojix is not
  a consumer.
- Public surface: `Engine`/`EngineOpen`, `Catalog`/`TableRegistration`,
  `mutation`/`query`/`record`/`subscribe`/`table` modules, `CommitLogEntry`,
  `SnapshotIdentifier`, and the new `versioning::*` (`VersioningPolicy`,
  `VersionedLogOperation`, `VersionedPayload`, `SchemaHash`, ...).
- main HEAD `c970d3f2` "add opt-in versioned state log" (additive: engine.rs
  +255, new versioning surface). Plus a `reusable-versioned-log-spike` branch
  (concept, off-main). No lojix relevance.

### signal-sema — v0.2.0 (NOT a lojix dependency)
- Role: Sema operation vocabulary (`Assert`/`Mutate`/`Retract`/`Match`/
  `Subscribe`/`Validate`, magnitudes, patterns, outcomes). Public surface:
  `SemaOperation`/`OperationClass`/`ToSemaOperation`, `Magnitude`, `Slot`/
  `Revision`, pattern/outcome types.
- main HEAD `33f62840` "gate NOTA text projection behind feature". Not in lojix tree.

### horizon-lib (horizon-rs) — v0.1.0 (DIRECT dep)
- Role: the horizon projection library lojix orchestrates from. Workspace at
  `horizon-rs` (members `lib` + `cli`); `horizon-rs/Cargo.toml` floats
  `nota-next` to `branch = main`. Public surface (`lib/src/lib.rs`): modules
  `address`, `cluster`, `horizon`, `machine`, `node`, `proposal`, `species`,
  `user`, ...; re-exports `Error`/`Result`, `Horizon`/`Viewpoint`,
  `ClusterProposal`.
- main HEAD `9fae4a36` "align nota-next source with contracts".
- lojix lock pins `9fae4a36` = CURRENT main. No break. (horizon-rs's
  `horizon-leaner-shape` / `horizon-re-engineering` branches exist but main is
  what lojix consumes; one of those branches currently shows a conflict commit
  per `jj log`, irrelevant to the main pin.)

## Breaking changes lojix must track on a refresh

1. **schema-rust-next `b252e81e` → `cedb2e06` ("stop emitting nota bridge
   methods")** — the one real item. Bumping the build-dep pin forces
   regeneration of `lojix/src/schema/nexus.rs` + `sema.rs`, removing ~124
   inherent `from_nota_block`/`to_nota` defs; the build's `write_or_check`
   gate fails until artifacts are regenerated. No source-call break (lojix
   uses the traits/derives, not inherent methods), so the fix is: bump pin,
   set `LOJIX_UPDATE_SCHEMA_ARTIFACTS`, regenerate, commit the slimmed files.

2. **nota-next `af6a2080` → `065fa2ad` ("own byte scalar codec")** — additive
   new codec surface; pulled when the float advances. Verify generated/runtime
   code still compiles against the new `ByteSequence`/`FixedByteSequence`
   codec; no known removal.

3. **schema-next `ccdf5487` → `2397d5b2`** — additive (scoped enum type
   reference); moves transitively with the schema-rust-next bump.

4. Non-events: signal-frame (pin already current), triad-runtime (pin already
   current; the DaemonConfiguration→BindingSurface rename does not touch any
   symbol lojix imports), horizon-lib (pin current). sema-engine and signal-sema
   are not in lojix's tree at all.

## Which crate owns "the modern schema syntax" codegen

`schema-rust-next` (v0.5.3) owns the Rust *emission* of the modern schema
syntax — it is lojix's build-dependency and the crate whose recent
bridge-method removal forces lojix's regeneration. Its semantic input layer is
`schema-next` (v0.2.0), which turns NOTA `.schema` structure into typed schema
data. Together: schema-next = parse/typed-schema engine, schema-rust-next =
Rust codegen. The crate lojix invokes by name in `build.rs` is
**schema-rust-next v0.5.3**.
