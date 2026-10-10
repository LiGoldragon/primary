# Code Anatomy: Datom, Ethos-Zero, Protos, Orchestrate

Witnessed 2026-09-04 by subflow of flow 6329f1.
Method: code reading, git inspection, cargo check/test where cheap.

---

## 1. Repository Inventory

### protos

- **Path**: `/git/github.com/LiGoldragon/protos`
- **Remote**: `git@github.com:LiGoldragon/protos.git`
- **Branch**: Detached HEAD at `2f605fd` (same as local `main`; `origin/main` at `bfde3b8`, behind)
- **Status**: Clean
- **Last 5 commits**:
  - `2f605fd` State complete Protos declaration contract in Ethos
  - `589c039` Complete Protos E2 trait signatures
  - `caf468c` Specify Protos E2 public-surface ownership
  - `f9eadcd` Normalize map declarations for Portion grammar
  - `99cb6d9` Adopt headed Schema map root
- **In-progress branches**: `SpiritLineageBTrain` (4590b48), `SpiritSourceIntegration` (e67c4cf), `SpiritSourceIntegrationPreEncoded` (d6a2d96), `SpiritV14Implementation` (a591162), `identifier-slicing-contracts` (c7510d3), `no-alias-migration` (e9983d6)
- **Crate**: `protos` v0.14.0, single crate, no workspace, zero runtime dependencies
- **Build/test**: PASS (cargo check, cargo test -- 13 tests all pass)

### datomic (repo name "datom" on GitHub, crate name "datomic")

- **Path**: `/git/github.com/LiGoldragon/datomic` (also symlinked as `/git/github.com/LiGoldragon/datom`)
- **Remote**: `git@github.com:LiGoldragon/datomic.git`
- **Branch**: Detached HEAD at `8b17abc` (same as local `main`; `origin/main` at `b670c72`, behind)
- **Status**: Clean
- **Last 5 commits**:
  - `8b17abc` Release Datomic map layout correction
  - `8e194c6` Complete Datomic map-owned private layouts
  - `4baeaac` Pin Datomic to complete Protos contract
  - `fae7f3e` State complete Datomic declaration contract in Ethos
  - `6f0354d` Normalize map declarations for Portion grammar
- **In-progress branches**: `epic-datom-path-locks-20260822` (4435f76 "Add Datom path lock replies")
- **Crate**: `datomic` v0.7.1, single crate, depends only on `protos` at rev `2f605fd`
- **Build/test**: PASS (cargo check, cargo test -- 13 tests all pass)

### ethos-zero

- **Path**: `/git/github.com/LiGoldragon/ethos-zero`
- **Remote**: `git@github.com:LiGoldragon/ethos-zero.git`
- **Branch**: Detached HEAD at `b0830fb` (ahead of local `main` at `b922afb`; `origin/main` at `b922afb`)
- **Status**: Clean
- **Last 5 commits**:
  - `b0830fb` Prove complete map-owned Rust contracts
  - `e98c3f5` Emit executable Datomic anatomies from Ethos maps
  - `bf2cd73` Strengthen Ethos File embodiment foundation
  - `a1a0061` Realize ethos-zero E0-E2 on the Portion pivot
  - `b73d535` Flatten single-record reply variants as Datom roots
- **In-progress branches**: `e3-bootstrap-wip-01a04a30` (3ff4da9 "WIP: retain Nexus bootstrap after WireContract landing")
- **Crate**: `ethos-zero` v0.1.0, single crate, depends on `protos` (rev `2f605fd`), `datomic` (rev `4baeaac`), `quote`/`proc-macro2`/`syn`/`thiserror`
- **Build/test**: PARTIAL -- cargo check passes; cargo test: 18 pass, 2 fail (require Nix env vars `ETHOS_PROTOS_MAP`/`ETHOS_DATOMIC_MAP`)

### orchestrate

- **Path**: `/git/github.com/LiGoldragon/orchestrate`
- **Remote**: `git@github.com:LiGoldragon/orchestrate.git`
- **Branch**: Detached HEAD at `e0f3bc5` (same as local `main`; `origin/main` at `dadd537` "Port Orchestrate to WireContract 0.26", ahead)
- **Status**: DIRTY -- 4 files modified (ARCHITECTURE.md, README.md, src/bin/orchestrate.rs, tests/live_nexus.rs)
- **Last 5 commits**:
  - `e0f3bc5` Realize durable ordinary Lock Nexus
  - `6ced922` Close ordinary operations deployment task
  - `c66ff74` Record ordinary operations skill progress
  - `4cc55c0` Track ordinary Orchestrate operations skill
  - `7857a47` Close Orchestrate Nexus release epic
- **In-progress branches**: `epic-datom-path-locks-20260822`, `LandTypedHumanTime`, `RegistryMaintenanceDeployment`, `WorktreeSubjectIntegration`, `workflow-engine-thin-slice`, and many more
- **Crate**: `orchestrate` v0.25.0, single crate, 4 binaries
- **Build/test**: FAILS -- dirty working copy references `textualize_source()` which does not exist on pinned `signal-orchestrate` rev

### signal-orchestrate

- **Path**: `/git/github.com/LiGoldragon/signal-orchestrate`
- **Remote**: `git@github.com:LiGoldragon/signal-orchestrate.git`
- **Branch**: Detached HEAD at `6fc8c5b` (`origin/main` at `a597f1a`, behind)
- **Status**: DIRTY -- M Cargo.lock, Cargo.toml, src/generated/signal.rs, tests/generated_contract.rs
- **Last 5 commits**:
  - `6fc8c5b` Generate Orchestrate Lock Datom contract
  - `88cc01e` Generate Orchestrate wire from signal Ethos only
  - `d23fb64` Verify Ethos output from Cargo OUT_DIR
  - `3de1c5d` Generate Orchestrate PathLock wire contract from Ethos
  - `3ac5991` docs: integrate Protos estate status
- **Crate**: `signal-orchestrate` v0.17.1, depends on `datom` (rev `4e13442b`), `protos` (rev `3b190f9f`), `signal-frame`, `rkyv`; build-dep: `ethos-monolith` (rev `b73d535`)

### protos-engine

- **Path**: `/git/github.com/LiGoldragon/protos-engine`
- **Remote**: `git@github.com:LiGoldragon/protos-engine.git`
- **Status**: Clean (one untracked file in ideas/), at `7a1bfd1`
- **Not a Rust crate** -- documentation/management repository with shell scripts for checking repository shape and coherence

### Sibling Repositories

| Repo | Path | Status | Key Dependency |
|------|------|--------|----------------|
| structural-codec | `/git/github.com/LiGoldragon/structural-codec` | Clean | content-identity, name-table, raw-discovery, rkyv |
| structural-codec-derive | `/git/github.com/LiGoldragon/structural-codec-derive` | Clean | **DEPRECATED** -- consolidated into protos |
| signal | `/git/github.com/LiGoldragon/signal` | DIRTY (20 files) | dotos, signal-sema, signal-derive, rkyv |
| signal-ethos-zero | `/git/github.com/LiGoldragon/signal-ethos-zero` | Clean | rkyv only |
| signal-ethos | `/git/github.com/LiGoldragon/signal-ethos` | Clean | signal-sema-storage, rkyv |
| signal-derive | `/git/github.com/LiGoldragon/signal-derive` | DIRTY (ARCHITECTURE.md) | proc-macro crate (proc-macro2, quote, syn) |
| signal-lojix | `/git/github.com/LiGoldragon/signal-lojix` | Clean | signal-frame, rkyv; build: core-ethos, structural-codec |
| sema | `/git/github.com/LiGoldragon/sema` | Clean | redb, rkyv |
| lojix | `/git/github.com/LiGoldragon/lojix` | DIRTY (.beads/) | signal-lojix, signal-frame, sema-engine, dotos |
| ethos-engine | `/git/github.com/LiGoldragon/ethos-engine` | Clean | core-ethos, signal-ethos, kameo |
| core-ethos | `/git/github.com/LiGoldragon/core-ethos` | Clean | structural-codec, name-table, content-identity |
| spirit-ethos | `/git/github.com/LiGoldragon/spirit-ethos` | DIRTY | dev-deps only (name-table, nomos-engine, sema-translator) |
| name-table | `/git/github.com/LiGoldragon/name-table` | Clean | content-identity, rkyv |

---

## 2. Public API: Protos (v0.14.0, current HEAD)

File: `/git/github.com/LiGoldragon/protos/src/lib.rs` (1623 lines)

### Core Data Types

```rust
// The universal structural element
pub enum Portion {
    Headed(Extent, Headed),
    Enclosed(Extent, Enclosed),
    Bare(Extent, Bare),
}

pub struct Headed {
    pub head: Symbol,
    pub separator: Separator,
    pub body: Box<Portion>,
}

pub enum Enclosed {
    Structural(StructuralEnclosed),
    Opaque(OpaqueEnclosed),
}

pub enum StructuralEnclosure { Braced, Bracketed, Guillemets, Angled }
pub enum OpaqueBoundary { CurlyQuote, Dialect(DialectBoundary) }
pub enum Separator { Period, Exclamation, Colon }
pub enum Layout { Flat }

pub struct Text<T = ()> {
    normalized: String,
    content_hash: ContentHash,
    delineation: Option<Delineation>,
    target: std::marker::PhantomData<fn() -> T>,
}
pub type Prospective<T> = Text<T>;

pub struct Delineation { pub portions: Vec<Portion> }
```

### Core Traits

```rust
// Pass 1: text -> Portion tree
pub trait Delineatable {
    type Delineation;
    fn delineate(&self) -> Result<Self::Delineation, Fault>;
}

// Pass 2 inbound: Portion -> Rust type
pub trait Embodied: Sized {
    fn from_portion(portion: &Portion) -> Result<Self, Fault>;
}

// Pass 2 outbound: Rust type -> Portion -> Text
pub trait Textualizable: Embodied {
    fn to_portion(&self) -> Portion;
    fn textualize(&self) -> Text { self.to_portion().print(Layout::Flat) }
}

// Full chain: Text<T> -> T
pub trait Embodiable {
    type Embodied: Embodied;
    fn embody(&self) -> Result<Self::Embodied, Fault>;
}

pub trait ShapeDefined: Embodied { fn matches(portion: &Portion) -> bool; }
pub trait BareSafe { fn is_bare_safe_for(&self, expectation: BareExpectation) -> bool; }
pub trait Printing { fn print(&self, layout: Layout) -> Text; }
pub trait ScalarAnatomy { fn signed_i64(&self) -> Result<i64, Fault>; fn decimal_f64(&self) -> Result<f64, Fault>; }
pub trait DelineatedText { fn delineation(&self) -> Option<&Delineation>; fn retag<U>(self) -> Text<U>; }
```

---

## 3. Public API: Datomic (v0.7.1, current HEAD)

File: `/git/github.com/LiGoldragon/datomic/src/lib.rs`

### Core Trait

```rust
pub trait Datomic: Sized {
    fn embody(portion: &Portion) -> Result<Self, Fault>;
    fn portion(&self) -> Portion;
    fn textualize(&self) -> Text<Self> {
        self.portion().print(Layout::Flat).retag()
    }
}
```

### Supporting Traits

```rust
pub trait TextEdge<T> {
    fn embody(&self) -> Result<T, Fault>;
}

pub trait PortionViewing {
    fn bare_symbol(&self) -> Option<&str>;
    fn headed(&self) -> Option<&Headed>;
    fn structural(&self, enclosure: StructuralEnclosure) -> Option<&[Portion]>;
    fn opaque(&self, boundary: OpaqueBoundary) -> Option<&str>;
    fn fault(&self, problem: FaultProblem) -> Fault;
}

pub trait PortionBuilding {
    fn bare(&self) -> Portion;
    fn headed(&self, separator: Separator, body: Portion) -> Portion;
    fn structural(&self, enclosure: StructuralEnclosure, portions: Vec<Portion>) -> Portion;
}

pub trait DecimalViewing { fn value(&self) -> f64; }
```

### Built-in Datomic Implementations

`bool`, `i64`, `FiniteDecimal`, `DatomicString`, `Vec<T>`, `BTreeMap<K, V>`, `Option<T>`.

No derive macros. All compound types are hand-implemented by consumers, or generated by ethos-zero.

---

## 4. Public API: Ethos-Zero (v0.1.0, current HEAD)

File: `/git/github.com/LiGoldragon/ethos-zero/src/lib.rs` (2072 lines)

### Core Public Types

```rust
pub enum File {
    Interface(InterfaceFile),
    Schema(SchemaFile),
}

pub struct InterfaceFile {
    pub header: Header, pub channel: Channel,
    pub imports: Vec<ResolvedImport>,
    pub input: Vec<TypeDeclaration>, pub output: Vec<TypeDeclaration>,
    pub refusal: Vec<TypeDeclaration>, pub stream: Vec<TypeDeclaration>,
    pub types: Vec<TypeDeclaration>,
}

pub struct SchemaFile {
    pub header: Header, pub imports: Vec<ResolvedImport>,
    pub types: Vec<TypeDeclaration>, pub kinds: Vec<KindDeclaration>,
    pub associations: Vec<Association>,
}

pub enum TypeDeclaration {
    Alias { .. }, Struct { .. }, TupleStruct { .. }, Enum { .. },
}
```

### The Two Public Entry Points

```rust
pub struct FileReader<'manifest> { manifest: &'manifest dyn Manifest }
// FileReader::read(&self, source: &str) -> Result<File, FileFault>

pub struct RustEmitter;
// RustEmitter::emit(&self, file: &File) -> Result<String, FileFault>
// RustEmitter::generate(&self, file: &File) -> Result<RustGeneration, FileFault>
// RustEmitter::syntax(&self, file: &File) -> Result<syn::File, FileFault>
```

### The Only Trait

```rust
pub trait Manifest {
    fn resolve(&self, source: &str) -> Option<FileLocation>;
}
```

---

## 5. The Serialization Pipeline

### Current Architecture (protos v0.14.0 + datomic v0.7.1)

The pipeline is two passes with a clean boundary at `Portion`:

```
Text (string)
  |  Pass 1: Protos delineation (character-level parsing)
  v
Portion tree (Headed | Enclosed | Bare, with Extents)
  |  Pass 2: Datomic embodiment (structural pattern-matching)
  v
Typed Rust value
```

**Pass 1** (Protos-owned): `Text::from(source)` normalizes whitespace and strips comments. `text.delineate()` runs the Parser, producing a `Delineation { portions: Vec<Portion> }`. The Parser handles structural delimiters (`{}`, `[]`, `<<>>`, `<>`), opaque delimiters (curly quotes, parentheses), separators (`.`, `!`, `:`), and bare values.

**Pass 2** (Datomic-owned): `T::embody(portion)` pattern-matches via `PortionViewing` trait methods (`bare_symbol()`, `headed()`, `structural()`, `opaque()`). Each type decides its own shape:
- `bool`: bare "True"/"False"
- `i64`: bare digits via `ScalarAnatomy::signed_i64()`
- `FiniteDecimal`: headed with Period separator via `ScalarAnatomy::decimal_f64()`
- `DatomicString`: opaque (curly quotes or dialect parentheses), or bare if safe
- `Vec<T>`: `StructuralEnclosure::Bracketed` (`[...]`)
- `BTreeMap<K,V>`: `StructuralEnclosure::Guillemets` (`<<...>>`)
- `Option<T>`: bare "None" or headed "Some.body"
- Structs: `StructuralEnclosure::Braced` (`{...}`), positional fields
- Enums: headed portions, discriminant in the head symbol

**Outbound**: `T::portion()` builds a Portion tree; `T::textualize()` prints it via `Portion::print(Layout::Flat)`.

### How Ethos-Zero Generates Datomic Implementations

Ethos-zero reads `.ethos` files (parsed by Protos into Portions, then pattern-matched into `File` AST), and emits Rust source via `quote`/`syn`. When a Schema file declares a `Datomic` kind, or for all Interface files, the emitter generates `impl datomic::Datomic for T` blocks with concrete `embody()` and `portion()` method bodies.

This is build-time code generation, not a proc-macro. The generated code is written to files and compiled as normal Rust source.

---

## 6. The Version Divergence (THE Critical Finding)

**There are two completely different APIs in play.** The protos and datom crates were deeply rewritten, and the consumers have not caught up.

### Old API (protos v0.8.0, datom v0.5.0)

Used by: `signal-orchestrate` (pinned at protos `3b190f9f`, datom `4e13442b`)

```
protos v0.8.0:  Block, BlockScanner, Head, Shape, SourceText
                RealizeScope, RealizeScoping, TextualizeScope, TextualizeScoping
                Shape::Braced, Shape::DottedBraced, Shape::DottedBare, Shape::Bare

datom v0.5.0:   DatomRoot (marker trait)
                DatomRealizing::realize_block(scope, block) -> Result
                DatomTextualizing::textualize_in(scope) -> Result
                DatomFault, DatomProblem, RecordPosition, PositionAdvancing
```

The old pipeline is scope-driven: a mutable `RealizeScope` walks a `Block` tree, calling `realize_body()` with a closure that receives each child. Structs track field positions via `RecordPosition`. Enums match on `Shape` + head name.

### New API (protos v0.14.0, datomic v0.7.1)

Used by: `ethos-zero` (pinned at protos `2f605fd`, datomic `4baeaac`)

```
protos v0.14.0: Portion, Headed, Enclosed, Bare, Extent
                Delineatable, Embodied, Textualizable
                No Block, no RealizeScope, no TextualizeScope

datomic v0.7.1: Datomic::embody(portion) -> Result
                Datomic::portion() -> Portion
                PortionViewing, PortionBuilding
                Fault, FaultProblem
```

The new pipeline is direct: `Datomic::embody` receives a `&Portion` and interrogates it through `PortionViewing` methods. No mutable scope, no walking. The crate name changed from `datom` to `datomic`.

### The Generator Gap

- **ethos-monolith** (at rev `b73d535`, used by signal-orchestrate's build.rs): generates OLD-API code (`DatomRealizing`, `DatomTextualizing`, `Block`, `Shape`)
- **ethos-zero** (at HEAD `b0830fb`): generates NEW-API code (`Datomic::embody`, `Datomic::portion`, `Portion`, `PortionViewing`)
- `ethos-monolith` at rev `b73d535` IS an old commit of `ethos-zero` (that rev appears in ethos-zero's git log)

---

## 7. Orchestrate CLIs

### Binary Targets (4)

| Binary | Path | Arguments | Purpose |
|--------|------|-----------|---------|
| `orchestrate-nexus` | `src/main.rs` | Zero | Daemon: Sema store + two Unix sockets |
| `orchestrate` | `src/bin/orchestrate.rs` | One Datom text arg | Thin ordinary CLI client |
| `meta-orchestrate` | `src/bin/meta_orchestrate.rs` | One Dotos text arg | Thin meta/privileged CLI client |
| `orchestrate-upgrade-preflight` | `src/bin/orchestrate_upgrade_preflight.rs` | Zero | Read-only legacy row count |

### Request/Reply Lifecycle (ordinary CLI)

1. Single CLI arg parsed as `DatomText<OrchestrateRequest>` via `SourceText(text).realize()`
2. `exchange()` wraps it: `request.into_request()` -> route -> `Frame` with `ExchangeFrameBody::Request`
3. Connects to `$ORCHESTRATE_SOCKET` Unix stream
4. Length-prefixed binary frame written, write-half shut down, reply read back
5. `Frame::decode_length_prefixed` -> extract `ExchangeFrameBody::Reply` -> unwrap `SubReply::Ok(value)` or `SubReply::Failed`

### Concrete Reply Examples (from tests)

Datom text forms:
```
Lock.{cli-lock 01a03eda [/absolute/path] cli-reason}
Observe.Locks
Release.{1}
```

Reply text forms:
```
Observed.Locks.[]
Locked.{1 cli-lock 01a03eda [/absolute/path] cli-reason}
ReleaseRejected.UnknownLockId
```

The committed code prints replies with `println!("{reply:?}")` (Rust Debug format). The dirty working copy attempts `reply.textualize_source()` (Datom text) but does not compile.

### Ethos Location

Orchestrate itself contains NO ethos files. Its wire contracts come from:
- `signal-orchestrate` (ordinary, contract id 1, wire rev 5) -- has `ethos/signal.ethos` and `src/generated/signal.rs`
- `meta-signal-orchestrate` (meta, contract id 2, wire rev 4)

The generator is `ethos-monolith` (an old commit of `ethos-zero`) invoked by `signal-orchestrate/build.rs`:

```rust
use ethos_monolith::generate::{SignalGeneration, SignalGenerationOperations};
SignalGeneration::new(root.join("ethos"), &generated_directory)
    .generate()
    .expect("generate the Orchestrate signal contract from Ethos in OUT_DIR");
```

The build.rs then asserts the generated output matches the committed `src/generated/signal.rs`.

### Reply Formatting Code

- Ordinary CLI: `src/bin/orchestrate.rs` -- committed: `println!("{reply:?}")` (Debug); dirty: `reply.textualize_source()` (broken)
- Meta CLI: `src/bin/meta_orchestrate.rs` -- `value.to_dotos()` (Dotos text format)

---

## 8. Dependency Graph

### Direct Dependencies (Cargo.toml git pins)

```
protos v0.14.0 (no deps)
  ^
  |
datomic v0.7.1 (depends on protos @ 2f605fd)
  ^
  |
ethos-zero v0.1.0 (depends on protos @ 2f605fd, datomic @ 4baeaac)

--- version boundary ---

protos v0.8.0 @ 3b190f9f (old API)
  ^
  |
datom v0.5.0 @ 4e13442b (old API, old crate name)
  ^                    ^
  |                    |
  |     ethos-monolith @ b73d535 (old ethos-zero, build-dep)
  |                    |
signal-orchestrate v0.17.1 (depends on datom @ 4e13442b, protos @ 3b190f9f, signal-frame)
  ^
  |
orchestrate v0.25.0 (depends on signal-orchestrate @ 6fc8c5b, datom @ 4e13442b, protos @ 3b190f9f, sema-engine, signal-frame x2, dotos, meta-signal-orchestrate, rkyv, tokio)
```

### Branch-Train Order

To make orchestrate speak the new datomic, the train must land in this order:

1. **protos** -- already at v0.14.0 (done)
2. **datomic** -- already at v0.7.1 on new API (done, though HEAD not pushed to origin)
3. **ethos-zero** -- already generates new-API code (done, though HEAD not on main)
4. **signal-orchestrate** -- must be updated: replace `ethos-monolith` build-dep with `ethos-zero`, re-pin `datom`->`datomic` and `protos` to current revs, regenerate `src/generated/signal.rs`
5. **orchestrate** -- must be updated: re-pin `signal-orchestrate`, `datom`->`datomic`, `protos`; fix CLI reply formatting

### Wider Dependency Web

The `signal-frame` crate is used by signal-orchestrate and orchestrate (at two different revs for ordinary vs meta contracts). `sema-engine` provides the Sema store. `dotos` and `meta-signal-orchestrate` are used by orchestrate for meta-CLI formatting. `rkyv` v0.8 is universal for wire serialization.

The old `core-ethos` / `structural-codec` / `name-table` chain (used by signal-lojix, ethos-engine) is a separate serialization lineage that does NOT touch the datom/datomic path. Those crates use rkyv-encoded structural records, not Protos Portions.

---

## 9. Test Coverage

### protos (13 tests, all pass)
- Portion round-tripping (proptest)
- Normalization, all delimiters/separators
- Opaque construction, fault extents
- Bare safety, scalar anatomy
- Retag, hash, typed text embodiment

### datomic (13 tests, all pass)
- Scalar round-trips (bool, i64, FiniteDecimal, DatomicString)
- Container embodiment (Vec, BTreeMap, Option)
- Struct/enum round-trips (hand-written impls)
- Full Orchestrate anatomy round-trip (Lock, LockRequest, Reply types)
- Public edge (TextEdge) with trivia

### ethos-zero (20 tests, 18 pass outside Nix)
- Schema/Interface file reading and Rust emission
- Import resolution and manifest
- Type expression projection (Vector, Result, inline payloads)
- Datomic anatomy generation (concrete `impl Datomic` blocks)
- Kind/Association -> trait/assertion emission
- End-to-end: generate Rust, compile in isolated Cargo project, run round-trip tests through Datomic
- 2 tests require Nix env vars (ETHOS_PROTOS_MAP, ETHOS_DATOMIC_MAP)

### orchestrate (cannot run -- build fails)
- `tests/live_nexus.rs`: integration test spawning a real Nexus process
- `tests/ordinary_lock_contract.rs`: store-level Lock behavior
- Both untestable due to dirty working copy compilation error

### signal-orchestrate (not tested -- dirty working copy)
- `tests/generated_contract.rs`: verifies generated wire contract

---

## 10. Ethos File Format (witnessed from signal-orchestrate)

The `.ethos` source for orchestrate's signal contract at `signal-orchestrate/ethos/signal.ethos`:

```
Interface.{0 2 0}
Channel.{Orchestrate 1 5}
[]
{
  [Lock.LockRequest Release.LockId Observe.ObserveSelection]
  [Locked.Lock LockRejected.LockRejection Released.Lock ReleaseRejected.ReleaseRejection Observed.Observation]
  []
  []
  [
    LockName.String
    FlowId.String
    LockPath.String
    LockPaths.Vector<LockPath>
    LockReason.String
    LockRequest.{LockName FlowId LockPaths LockReason}
    LockId.Integer
    Lock.{LockId LockName FlowId LockPaths LockReason}
    DuplicateName.Lock
    LockOverlap.{LockPath Lock}
    LockRejection.[DuplicateName.Lock PathOverlap.LockOverlap]
    ReleaseRejection.[UnknownLockId]
    ObserveSelection.[Locks]
    Locks.Vector<Lock>
    LockSnapshot.{Locks}
    Observation.[Locks.LockSnapshot]
  ]
}
```

The datomic crate's own Ethos declaration at `datomic/datomic.ethos`:

```
Schema.{0 1 0}
[]
Types.[
  Fault.Struct.{Visibility.Public Public.Extent.Extent Public.Problem.FaultProblem}
  FaultProblem.Enum.[Visibility.Public Shape Head Value Arity MapPair DuplicateMapKey UnrepresentableString Protos]
  ...
]
Kinds.[
  Datomic.{Visibility.Public Supertraits.[Sized] Methods.[embody... portion... textualize...]}
  TextEdge.{...}
  PortionViewing.{...}
  ...
]
Associations.[
  FiniteDecimal.[Datomic DecimalViewing]
  DatomicString.[Datomic]
]
```

---

## Sources

All findings witnessed from code at the stated paths and git revisions on 2026-09-04.

- `/git/github.com/LiGoldragon/protos` -- HEAD 2f605fd, `src/lib.rs`, `Cargo.toml`, `tests/delineation.rs`
- `/git/github.com/LiGoldragon/datomic` -- HEAD 8b17abc, `src/lib.rs`, `Cargo.toml`, `datomic.ethos`, `tests/`
- `/git/github.com/LiGoldragon/ethos-zero` -- HEAD b0830fb, `src/lib.rs`, `Cargo.toml`, `tests/file_contract.rs`
- `/git/github.com/LiGoldragon/orchestrate` -- HEAD e0f3bc5, `src/`, `Cargo.toml`, `tests/`
- `/git/github.com/LiGoldragon/signal-orchestrate` -- HEAD 6fc8c5b, `src/`, `Cargo.toml`, `build.rs`, `ethos/signal.ethos`, `src/generated/signal.rs`
- `/home/li/primary/orchestrate/AGENTS.md`, `ARCHITECTURE.md`
- Sibling repos: structural-codec, signal, signal-ethos-zero, signal-ethos, signal-orchestrate, signal-lojix, sema, lojix, ethos-engine, core-ethos, spirit-ethos, signal-derive, name-table, protos-engine
