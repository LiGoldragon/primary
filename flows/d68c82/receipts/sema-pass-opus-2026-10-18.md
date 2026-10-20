# Sema used for the database: pass of 2026-10-18

Ruling searched against: Sema is the meaning language, a subdialect; the database is Memory.

Scope: psyche-context, mind-context, field-context (psyche-skills, mind-skills and field-skills are symlinks to these three and were counted once); the Ethos repositories core-ethos, ethos-engine, ethos-test, ethos-zero, meta-signal-ethos-zero, signal-ethos, signal-ethos-zero, spirit-ethos, tree-sitter-ethos (tracked files; generated harness trees excluded); /home/li/primary/flows/d68c82/books/*.md. Search: case-insensitive `sema` not followed by `ntic` or `phore`. No hit in field-context, meta-signal-ethos-zero or signal-ethos-zero. No hit uses Sema for the meaning language.

Psyche-context lines change only through a book; their replacements below are proposal text for one.

Read, not re-verified: ethos-zero/UPGRADES.md 118-124 says core-ethos and spirit-ethos are frozen, spirit's schema is deprecated, and nothing is generated from their `Sema`-headed files.

## Prose: database meaning, replacement proposed (29)

- `/git/github.com/LiGoldragon/psyche-context/vision/ethos.md:58`
  - Now: Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided. Signal gives a Nexus its main types and Sema its database types.
  - Proposed: Signal's sections are queries and responses, since there is communication; Memory's are record types, the rest to be decided. Signal gives a Nexus its main types and Memory its database types.
  - Note: Already proposed in book 38, Proposal 3.

- `/git/github.com/LiGoldragon/psyche-context/vision/ethos.md:60`
  - Now: (same sentence as line 58)
  - Proposed: (see line 58)
  - Note: Already proposed in book 38, Proposal 3.

- `/git/github.com/LiGoldragon/psyche-context/vision/ethos.md:452`
  - Now: In the Signal and Sema roots the associations of the query, response and record types are implied and never written.
  - Proposed: In the Signal and Memory roots the associations of the query, response and record types are implied and never written.
  - Note: Already proposed in book 38, Proposal 22.

- `/git/github.com/LiGoldragon/psyche-context/vision/nexus.md:22`
  - Now: The basic ontology of an actor and dataflow system is designed before implementation; signal and sema are designed against it as if new, the old code at most inspiration.
  - Proposed: The basic ontology of an actor and dataflow system is designed before implementation; signal and memory are designed against it as if new, the old code at most inspiration.
  - Note: Not in book 38.

- `/git/github.com/LiGoldragon/psyche-context/vision/nexus.md:35`
  - Now: The nexus and sema documents are undesigned; when they are designed they live in the Nexus's main repository.
  - Proposed: The nexus and memory documents are undesigned; when they are designed they live in the Nexus's main repository.
  - Note: Not in book 38.

- `/git/github.com/LiGoldragon/psyche-context/vision/nexus.md:91`
  - Now: On start it looks for its Sema database at the default location: a database that exists holds the configuration; a database created new is seeded with the defaults.
  - Proposed: On start it looks for its Memory database at the default location: a database that exists holds the configuration; a database created new is seeded with the defaults.
  - Note: Already proposed in book 38, Proposal 23; that proposal names the file `skills/vision-nexus.md`, the authored path is `vision/nexus.md`.

- `/git/github.com/LiGoldragon/psyche-context/vision/sema.md:2`
  - Now: description: Sema, the database engine of a Nexus, or its record types are being designed or judged.
  - Proposed: description: Memory, the database engine of a Nexus, or its record types are being designed or judged.
  - Note: Not in book 38. The module itself would move from `vision/sema.md` to `vision/memory.md`.

- `/git/github.com/LiGoldragon/psyche-context/vision/sema.md:6`
  - Now: ## What sema is
  - Proposed: ## What Memory is
  - Note: Not in book 38.

- `/git/github.com/LiGoldragon/psyche-context/vision/sema.md:8`
  - Now: Sema is the database engine of a Nexus, authored in Ethos so the stored types are visible; its root, Sema, declares record types.
  - Proposed: Memory is the database engine of a Nexus, authored in Ethos so the stored types are visible; its root, Memory, declares record types.
  - Note: Not in book 38.

- `/git/github.com/LiGoldragon/psyche-context/vision/sema.md:9`
  - Now: (same sentence as line 8)
  - Proposed: (see line 8)
  - Note: Not in book 38.

- `/git/github.com/LiGoldragon/psyche-context/vision/sema.md:14`
  - Now: Sema   (head of the example root in the code block)
  - Proposed: Memory
  - Note: Not in book 38.

- `/git/github.com/LiGoldragon/core-ethos/ARCHITECTURE.md:89`
  - Now: - Sema: PersistentDeclarations, Tables
  - Proposed: - Memory: PersistentDeclarations, Tables

- `/git/github.com/LiGoldragon/core-ethos/ARCHITECTURE.md:103`
  - Now: - Interface/Nexus/Sema admission boundaries;
  - Proposed: - Interface/Nexus/Memory admission boundaries;

- `/git/github.com/LiGoldragon/core-ethos/Cargo.toml:8`
  - Now: Authority-sealed bootstrap reader and model for Interface, Nexus, and Sema Ethos documents.
  - Proposed: Authority-sealed bootstrap reader and model for Interface, Nexus, and Memory Ethos documents.

- `/git/github.com/LiGoldragon/core-ethos/README.md:4`
  - Now: `core-ethos` owns the strict bootstrap Ethos reader and its purpose-built Interface, Nexus, and Sema semantic forms.
  - Proposed: `core-ethos` owns the strict bootstrap Ethos reader and its purpose-built Interface, Nexus, and Memory semantic forms.

- `/git/github.com/LiGoldragon/core-ethos/README.md:53`
  - Now: - Sema `{RecordTypes Tables}` with persistent nominal record/key leaves;
  - Proposed: - Memory `{RecordTypes Tables}` with persistent nominal record/key leaves;

- `/git/github.com/LiGoldragon/ethos-engine/AGENTS.md:5`
  - Now: The Signal → Nexus → SEMA flow and central typed storage socket are wired legacy behavior, not the target architecture.
  - Proposed: The Signal → Nexus → Memory flow and central typed storage socket are wired legacy behavior, not the target architecture.

- `/git/github.com/LiGoldragon/ethos-engine/AGENTS.md:7`
  - Now: The approved target makes this daemon stateful, with its own embedded sema database.
  - Proposed: The approved target makes this daemon stateful, with its own embedded Memory database.

- `/git/github.com/LiGoldragon/ethos-engine/ARCHITECTURE.md:4`
  - Now: In the currently wired legacy topology, typed requests traverse state-bearing Signal → Nexus → SEMA Kameo actors.
  - Proposed: In the currently wired legacy topology, typed requests traverse state-bearing Signal → Nexus → Memory Kameo actors.

- `/git/github.com/LiGoldragon/ethos-engine/ARCHITECTURE.md:8`
  - Now: The approved target is a stateful Ethos daemon whose own embedded sema database stores its documents.
  - Proposed: The approved target is a stateful Ethos daemon whose own embedded Memory database stores its documents.

- `/git/github.com/LiGoldragon/ethos-test/STATEMENTS.md:52`
  - Now: | 57-60 | Roots: Signal's sections are queries and responses; Sema's are record types; Signal gives a Nexus its main types and Sema its database types | pass (Signal), no observable (Nexus and Sema roles) | ethos-zero-roots | Query and Response from the first two sections; what a Nexus or Sema does with the types is outside ethos-zero |
  - Proposed: | 57-60 | Roots: Signal's sections are queries and responses; Memory's are record types; Signal gives a Nexus its main types and Memory its database types | pass (Signal), no observable (Nexus and Memory roles) | ethos-zero-roots | Query and Response from the first two sections; what a Nexus or Memory does with the types is outside ethos-zero |
  - Note: Mirrors vision/ethos.md 58-60; follows that landing.

- `/git/github.com/LiGoldragon/ethos-test/STATEMENTS.md:95`
  - Now: | 441-443 | Associations: implied in Signal and Sema, never written | ...
  - Proposed: | 441-443 | Associations: implied in Signal and Memory, never written | ...
  - Note: Mirrors vision/ethos.md 452; follows that landing.

- `/git/github.com/LiGoldragon/ethos-test/checks/ethos-zero-cargo-signal-associations.nix:1`
  - Now: # "In the Signal and Sema roots the associations of the query, response and record types are implied and never written": ...
  - Proposed: # "In the Signal and Memory roots the associations of the query, response and record types are implied and never written": ...
  - Note: Quotes vision/ethos.md 452; follows that landing.

- `/git/github.com/LiGoldragon/signal-ethos/ARCHITECTURE.md:5`
  - Now: ...then exposes the currently wired `SignalContract`, `NexusRuntime`, and `SemaStorage` roots.
  - Proposed: ...then exposes the currently wired `SignalContract`, `NexusRuntime`, and `MemoryStorage` roots.
  - Note: `SemaStorage` is a variant owned by signal-sema-storage; the doc follows the code.

- `/git/github.com/LiGoldragon/signal-ethos/ARCHITECTURE.md:6`
  - Now: `ethos-engine` will own its embedded sema database, while the separate `sema-translator` owns only shared names and encodedID allocation.
  - Proposed: `ethos-engine` will own its embedded Memory database, while the separate `sema-translator` owns only shared names and encodedID allocation.
  - Note: The `sema-translator` part of this sentence is in the ambiguous list (line 7).

- `/git/github.com/LiGoldragon/signal-ethos/README.md:11`
  - Now: The lockfile still contains the retired `core-schema` package transitively through the exact pinned `signal-sema-storage` revision.
  - Proposed: The lockfile still contains the retired `core-schema` package transitively through the exact pinned `signal-memory-storage` revision.
  - Note: Depends on renaming the signal-sema-storage repository.

- `/git/github.com/LiGoldragon/spirit-ethos/README.md:3`
  - Now: Canonical authored Ethos source for Spirit's Interface, Nexus, and Sema roots.
  - Proposed: Canonical authored Ethos source for Spirit's Interface, Nexus, and Memory roots.

- `/git/github.com/LiGoldragon/spirit-ethos/README.md:19`
  - Now: Sema persists records plus the one v13-to-v14 migration receipt; its active families are records and migrations.
  - Proposed: Memory persists records plus the one v13-to-v14 migration receipt; its active families are records and migrations.

- `/git/github.com/LiGoldragon/spirit-ethos/README.md:66`
  - Now: The new Sema declaration gives records their stable `RecordIdentifier` key and migrations their source-schema-version key.
  - Proposed: The new Memory declaration gives records their stable `RecordIdentifier` key and migrations their source-schema-version key.

## Code and configuration: database meaning, mechanical replacement (129)

Each replacement maps Sema to Memory, sema to memory, SEMA to MEMORY. Lines naming sema-storage or signal-sema-storage depend on those repositories being renamed (to memory-storage, signal-memory-storage). Files named for the root move too: core-ethos/tests/fixtures/bootstrap/sema.ethos and spirit-ethos/sema.ethos to memory.ethos; psyche-context/vision/sema.md to vision/memory.md.

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap.rs:1`
  - Now: `//! Strict shared bootstrap reader for Interface, Nexus, and Sema Ethos files.`
  - Proposed: `//! Strict shared bootstrap reader for Interface, Nexus, and Memory Ethos files.`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap.rs:31`
  - Now: `SemaTransactionAssembler,`
  - Proposed: `MemoryTransactionAssembler,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:13`
  - Now: `/// This is construction metadata, not an identity. The Sema authority mints`
  - Proposed: `/// This is construction metadata, not an identity. The Memory authority mints`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:20`
  - Now: `SemaKind,`
  - Proposed: `MemoryKind,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:67`
  - Now: `const SEMA_KIND_ROLES: &[BootstrapPriorRole] = &[BootstrapPriorRole::FileKind(EthosKind::Sema)];`
  - Proposed: `const MEMORY_KIND_ROLES: &[BootstrapPriorRole] = &[BootstrapPriorRole::FileKind(EthosKind::Memory)];`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:93`
  - Now: `slot: BootstrapPriorSlot::SemaKind,`
  - Proposed: `slot: BootstrapPriorSlot::MemoryKind,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:94`
  - Now: `textual_name: "Sema",`
  - Proposed: `textual_name: "Memory",`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:95`
  - Now: `roles: SEMA_KIND_ROLES,`
  - Proposed: `roles: MEMORY_KIND_ROLES,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:472`
  - Now: `pub sema_kind: EncodedName,`
  - Proposed: `pub memory_kind: EncodedName,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:511`
  - Now: `"sema_kind",`
  - Proposed: `"memory_kind",`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:512`
  - Now: `&identities.sema_kind,`
  - Proposed: `&identities.memory_kind,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:513`
  - Now: `SchemaRole::FileKind(EthosKind::Sema),`
  - Proposed: `SchemaRole::FileKind(EthosKind::Memory),`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:601`
  - Now: `("sema_kind", &identities.sema_kind),`
  - Proposed: `("memory_kind", &identities.memory_kind),`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:628`
  - Now: `metadata.spelling(&identities.sema_kind),`
  - Proposed: `metadata.spelling(&identities.memory_kind),`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/catalog.rs:681`
  - Now: `&ids.sema_kind,`
  - Proposed: `&ids.memory_kind,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/error.rs:170`
  - Now: `#[error("Sema persistent declarations admit only plain nominal types")]`
  - Proposed: `#[error("Memory persistent declarations admit only plain nominal types")]`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/model.rs:53`
  - Now: `Sema,`
  - Proposed: `Memory,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/model.rs:117`
  - Now: `Sema(SemaBody),`
  - Proposed: `Memory(MemoryBody),`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/model.rs:125`
  - Now: `Self::Sema(_) => EthosKind::Sema,`
  - Proposed: `Self::Memory(_) => EthosKind::Memory,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/model.rs:196`
  - Now: `pub struct SemaBody {`
  - Proposed: `pub struct MemoryBody {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:271`
  - Now: `/// The sole Core-provided admission capability for Sema's transaction`
  - Proposed: `/// The sole Core-provided admission capability for Memory's transaction`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:275`
  - Now: `pub struct SemaTransactionAssembler {`
  - Proposed: `pub struct MemoryTransactionAssembler {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:293`
  - Now: `impl SemaTransactionAssembler {`
  - Proposed: `impl MemoryTransactionAssembler {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:294`
  - Now: `/// Obtain the one Core admission used by Sema's transaction assembler.`
  - Proposed: `/// Obtain the one Core admission used by Memory's transaction assembler.`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:300`
  - Now: `impl raw_construction_seal::Sealed for SemaTransactionAssembler {}`
  - Proposed: `impl raw_construction_seal::Sealed for MemoryTransactionAssembler {}`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:302`
  - Now: `impl AdmittedToCoreEthosRawConstruction for SemaTransactionAssembler {`
  - Proposed: `impl AdmittedToCoreEthosRawConstruction for MemoryTransactionAssembler {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:878`
  - Now: `BootstrapBody::Sema(body) => {`
  - Proposed: `BootstrapBody::Memory(body) => {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:2610`
  - Now: `EthosKind::Sema => {`
  - Proposed: `EthosKind::Memory => {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:2621`
  - Now: `"duplicate Sema declaration section in root registry",`
  - Proposed: `"duplicate Memory declaration section in root registry",`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:2628`
  - Now: `"duplicate Sema table section in root registry",`
  - Proposed: `"duplicate Memory table section in root registry",`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:2634`
  - Now: `"Sema root registry section kind",`
  - Proposed: `"Memory root registry section kind",`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:2639`
  - Now: `Ok(BootstrapBody::Sema(SemaBody {`
  - Proposed: `Ok(BootstrapBody::Memory(MemoryBody {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:2641`
  - Now: `"root registry omits Sema declarations",`
  - Proposed: `"root registry omits Memory declarations",`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:2644`
  - Now: `"root registry omits Sema tables",`
  - Proposed: `"root registry omits Memory tables",`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:3050`
  - Now: `BootstrapBody::Sema(body) => {`
  - Proposed: `BootstrapBody::Memory(body) => {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/reader.rs:3162`
  - Now: `BootstrapBody::Sema(body) => {`
  - Proposed: `BootstrapBody::Memory(body) => {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/root.rs:75`
  - Now: `(BootstrapSectionSchema::PersistentDeclarations, BootstrapBody::Sema(body)) => Ok(`
  - Proposed: `(BootstrapSectionSchema::PersistentDeclarations, BootstrapBody::Memory(body)) => Ok(`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/root.rs:78`
  - Now: `(BootstrapSectionSchema::Tables, BootstrapBody::Sema(body)) => {`
  - Proposed: `(BootstrapSectionSchema::Tables, BootstrapBody::Memory(body)) => {`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/root.rs:119`
  - Now: `kind: EthosKind::Sema,`
  - Proposed: `kind: EthosKind::Memory,`

- `/git/github.com/LiGoldragon/core-ethos/src/bootstrap/root.rs:120`
  - Now: `kind_identity: ids.sema_kind.clone(),`
  - Proposed: `kind_identity: ids.memory_kind.clone(),`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:140`
  - Now: `sema_kind: id(3),`
  - Proposed: `memory_kind: id(3),`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:187`
  - Now: `(3, "Sema", vec![SchemaRole::FileKind(EthosKind::Sema)]),`
  - Proposed: `(3, "Memory", vec![SchemaRole::FileKind(EthosKind::Memory)]),`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:244`
  - Now: `let assembler = SemaTransactionAssembler::new();`
  - Proposed: `let assembler = MemoryTransactionAssembler::new();`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:303`
  - Now: `let assembler = SemaTransactionAssembler::new();`
  - Proposed: `let assembler = MemoryTransactionAssembler::new();`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:345`
  - Now: `let assembler = SemaTransactionAssembler::new();`
  - Proposed: `let assembler = MemoryTransactionAssembler::new();`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:682`
  - Now: `let assembler = SemaTransactionAssembler::new();`
  - Proposed: `let assembler = MemoryTransactionAssembler::new();`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:785`
  - Now: `fixture.reader.plan("Sema.{1 0 0}\n[]\n{[] [bad.{String}]}"),`
  - Proposed: `fixture.reader.plan("Memory.{1 0 0}\n[]\n{[] [bad.{String}]}"),`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:841`
  - Now: `.plan("Sema.{1 0 0}\n[dep.[ShapeOnly]]\n{[Record.String] [bad.{Record ShapeOnly}]}")`
  - Proposed: `.plan("Memory.{1 0 0}\n[dep.[ShapeOnly]]\n{[Record.String] [bad.{Record ShapeOnly}]}")`

- `/git/github.com/LiGoldragon/core-ethos/tests/bootstrap_reader.rs:1005`
  - Now: `fixture.reader.section_order(EthosKind::Sema),`
  - Proposed: `fixture.reader.section_order(EthosKind::Memory),`

- `/git/github.com/LiGoldragon/core-ethos/tests/fixtures/bootstrap/sema.ethos:1`
  - Now: `Sema.{1 0 0}`
  - Proposed: `Memory.{1 0 0}`

- `/git/github.com/LiGoldragon/ethos-engine/Cargo.toml:22`
  - Now: `signal-sema-storage={git="https://github.com/LiGoldragon/signal-sema-storage.git",rev="31ab48608a3c2eab0733dcb16a3351251a70789d"}`
  - Proposed: `signal-memory-storage={git="https://github.com/LiGoldragon/signal-memory-storage.git",rev="31ab48608a3c2eab0733dcb16a3351251a70789d"}`

- `/git/github.com/LiGoldragon/ethos-engine/Cargo.toml:26`
  - Now: `sema-storage={git="https://github.com/LiGoldragon/sema-storage.git",rev="269953164460cd842c1f3f8c9c93e4afe1e3628e"}`
  - Proposed: `memory-storage={git="https://github.com/LiGoldragon/memory-storage.git",rev="269953164460cd842c1f3f8c9c93e4afe1e3628e"}`

- `/git/github.com/LiGoldragon/ethos-engine/src/authority_ingest.rs:9`
  - Now: `//! currently wired central authority (`sema-storage`), and build the universe from its`
  - Proposed: `//! currently wired central authority (`memory-storage`), and build the universe from its`

- `/git/github.com/LiGoldragon/ethos-engine/src/authority_ingest.rs:40`
  - Now: `use signal_sema_storage::{`
  - Proposed: `use signal_memory_storage::{`

- `/git/github.com/LiGoldragon/ethos-engine/src/bin/ethos-engine.rs:5`
  - Now: `use signal_sema_storage::{DocumentKind, FixtureScope, FrameMessage, SlotIdentifier, Wire};`
  - Proposed: `use signal_memory_storage::{DocumentKind, FixtureScope, FrameMessage, SlotIdentifier, Wire};`

- `/git/github.com/LiGoldragon/ethos-engine/src/bin/ethos-engine.rs:24`
  - Now: `let sema = PathBuf::from(`
  - Proposed: `let memory = PathBuf::from(`

- `/git/github.com/LiGoldragon/ethos-engine/src/bin/ethos-engine.rs:27`
  - Now: `.unwrap_or_else(|| "/tmp/new-language-engine/sema.sock".into()),`
  - Proposed: `.unwrap_or_else(|| "/tmp/new-language-engine/memory.sock".into()),`

- `/git/github.com/LiGoldragon/ethos-engine/src/bin/ethos-engine.rs:34`
  - Now: `let runtime = Runtime::new(sema);`
  - Proposed: `let runtime = Runtime::new(memory);`

- `/git/github.com/LiGoldragon/ethos-engine/src/bin/ethos-engine.rs:64`
  - Now: `_ => Err("usage: ethos-engine daemon [socket] [sema-socket] | ingest <socket> <file> | subscribe <socket>".into()),`
  - Proposed: `_ => Err("usage: ethos-engine daemon [socket] [memory-socket] | ingest <socket> <file> | subscribe <socket>".into()),`

- `/git/github.com/LiGoldragon/ethos-engine/src/legacy_storage_ingest.rs:3`
  - Now: `//! `signal-sema-storage` is a frozen donor whose `DocumentPayload::TypeSchema``
  - Proposed: `//! `signal-memory-storage` is a frozen donor whose `DocumentPayload::TypeSchema``

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:16`
  - Now: `use signal_sema_storage::{`
  - Proposed: `use signal_memory_storage::{`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:18`
  - Now: `Reply as SemaReply, Request as SemaRequest, Snapshot, SubscriptionIdentifier, Wire,`
  - Proposed: `Reply as MemoryReply, Request as MemoryRequest, Snapshot, SubscriptionIdentifier, Wire,`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:37`
  - Now: `pub struct SemaPlane {`
  - Proposed: `pub struct MemoryPlane {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:41`
  - Now: `impl SemaPlane {`
  - Proposed: `impl MemoryPlane {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:51`
  - Now: `async fn exchange(&self, request: &SemaRequest) -> Result<SemaReply> {`
  - Proposed: `async fn exchange(&self, request: &MemoryRequest) -> Result<MemoryReply> {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:62`
  - Now: `return Err(Error::Codec("Sema rejected frame protocol".into()));`
  - Proposed: `return Err(Error::Codec("Memory rejected frame protocol".into()));`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:76`
  - Now: `return Err(Error::Codec("Sema returned a non-reply frame".into()));`
  - Proposed: `return Err(Error::Codec("Memory returned a non-reply frame".into()));`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:78`
  - Now: `rkyv::from_bytes::<SemaReply, rkyv::rancor::Error>(&payload)`
  - Proposed: `rkyv::from_bytes::<MemoryReply, rkyv::rancor::Error>(&payload)`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:82`
  - Now: `impl Actor for SemaPlane {`
  - Proposed: `impl Actor for MemoryPlane {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:92`
  - Now: `pub struct Commit(pub SemaRequest);`
  - Proposed: `pub struct Commit(pub MemoryRequest);`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:93`
  - Now: `impl Message<Commit> for SemaPlane {`
  - Proposed: `impl Message<Commit> for MemoryPlane {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:94`
  - Now: `type Reply = Result<SemaReply>;`
  - Proposed: `type Reply = Result<MemoryReply>;`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:102`
  - Now: `sema: ActorRef<SemaPlane>,`
  - Proposed: `memory: ActorRef<MemoryPlane>,`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:148`
  - Now: `SemaRequest::Store {`
  - Proposed: `MemoryRequest::Store {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:160`
  - Now: `EthosRequest::StoreSignalContract { scope, slot, root } => SemaRequest::Store {`
  - Proposed: `EthosRequest::StoreSignalContract { scope, slot, root } => MemoryRequest::Store {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:168`
  - Now: `EthosRequest::StoreNexusRuntime { scope, slot, root } => SemaRequest::Store {`
  - Proposed: `EthosRequest::StoreNexusRuntime { scope, slot, root } => MemoryRequest::Store {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:176`
  - Now: `EthosRequest::StoreSemaStorage { scope, slot, root } => SemaRequest::Store {`
  - Proposed: `EthosRequest::StoreMemoryStorage { scope, slot, root } => MemoryRequest::Store {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:179`
  - Now: `kind: DocumentKind::SemaStorage,`
  - Proposed: `kind: DocumentKind::MemoryStorage,`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:182`
  - Now: `payload: DocumentPayload::SemaStorage(root),`
  - Proposed: `payload: DocumentPayload::MemoryStorage(root),`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:184`
  - Now: `EthosRequest::List { scope, kind } => SemaRequest::List { scope, kind },`
  - Proposed: `EthosRequest::List { scope, kind } => MemoryRequest::List { scope, kind },`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:185`
  - Now: `EthosRequest::Fetch { hash } => SemaRequest::HashFetch { hash },`
  - Proposed: `EthosRequest::Fetch { hash } => MemoryRequest::HashFetch { hash },`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:186`
  - Now: `EthosRequest::Subscribe { scope, kind } => SemaRequest::Subscribe { scope, kind },`
  - Proposed: `EthosRequest::Subscribe { scope, kind } => MemoryRequest::Subscribe { scope, kind },`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:189`
  - Now: `.sema`
  - Proposed: `.memory`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:195`
  - Now: `SemaReply::Stored(summary) => {`
  - Proposed: `MemoryReply::Stored(summary) => {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:203`
  - Now: `SemaReply::Listed(values) => EthosReply::Listed(values),`
  - Proposed: `MemoryReply::Listed(values) => EthosReply::Listed(values),`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:204`
  - Now: `SemaReply::Document(value) => {`
  - Proposed: `MemoryReply::Document(value) => {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:205`
  - Now: `EthosReply::Fetched(value.map(|document| signal_sema_storage::SlotSummary {`
  - Proposed: `EthosReply::Fetched(value.map(|document| signal_memory_storage::SlotSummary {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:211`
  - Now: `SemaReply::Subscribed {`
  - Proposed: `MemoryReply::Subscribed {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:218`
  - Now: `SemaReply::Rejected(signal_sema_storage::Rejection::InvalidDocument(_)) => {`
  - Proposed: `MemoryReply::Rejected(signal_memory_storage::Rejection::InvalidDocument(_)) => {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:262`
  - Now: `pub fn new(sema_socket: PathBuf) -> Self {`
  - Proposed: `pub fn new(memory_socket: PathBuf) -> Self {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:263`
  - Now: `let sema = SemaPlane::spawn(SemaPlane {`
  - Proposed: `let memory = MemoryPlane::spawn(MemoryPlane {`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:264`
  - Now: `socket: sema_socket,`
  - Proposed: `socket: memory_socket,`

- `/git/github.com/LiGoldragon/ethos-engine/src/lib.rs:269`
  - Now: `sema,`
  - Proposed: `memory,`

- `/git/github.com/LiGoldragon/ethos-engine/tests/equivalence.rs:4`
  - Now: `//! legacy central identity authority (a live `sema-storage` runtime), yields IDENTICAL`
  - Proposed: `//! legacy central identity authority (a live `memory-storage` runtime), yields IDENTICAL`

- `/git/github.com/LiGoldragon/ethos-engine/tests/equivalence.rs:14`
  - Now: `//! This is the in-process engine-level floor: the authority is a real `sema-storage``
  - Proposed: `//! This is the in-process engine-level floor: the authority is a real `memory-storage``

- `/git/github.com/LiGoldragon/ethos-engine/tests/equivalence.rs:32`
  - Now: `use sema_storage::Runtime;`
  - Proposed: `use memory_storage::Runtime;`

- `/git/github.com/LiGoldragon/ethos-engine/tests/equivalence.rs:33`
  - Now: `use signal_sema_storage::{BoundIdentities, Reply, Request, SchemaWholeHandle};`
  - Proposed: `use signal_memory_storage::{BoundIdentities, Reply, Request, SchemaWholeHandle};`

- `/git/github.com/LiGoldragon/ethos-engine/tests/equivalence.rs:80`
  - Now: `let runtime = Runtime::open(&temporary.path().join("authority.sema"))`
  - Proposed: `let runtime = Runtime::open(&temporary.path().join("authority.memory"))`

- `/git/github.com/LiGoldragon/signal-ethos/Cargo.toml:11`
  - Now: `signal-sema-storage={git="https://github.com/LiGoldragon/signal-sema-storage.git",rev="31ab48608a3c2eab0733dcb16a3351251a70789d"}`
  - Proposed: `signal-memory-storage={git="https://github.com/LiGoldragon/signal-memory-storage.git",rev="31ab48608a3c2eab0733dcb16a3351251a70789d"}`

- `/git/github.com/LiGoldragon/signal-ethos/src/lib.rs:6`
  - Now: `use signal_sema_storage::{`
  - Proposed: `use signal_memory_storage::{`

- `/git/github.com/LiGoldragon/signal-ethos/src/lib.rs:7`
  - Now: `ChangeEvent, ContentHash, DocumentKind, FixtureScope, NexusRuntimeRoot, SemaStorageRoot,`
  - Proposed: `ChangeEvent, ContentHash, DocumentKind, FixtureScope, NexusRuntimeRoot, MemoryStorageRoot,`

- `/git/github.com/LiGoldragon/signal-ethos/src/lib.rs:28`
  - Now: `StoreSemaStorage {`
  - Proposed: `StoreMemoryStorage {`

- `/git/github.com/LiGoldragon/signal-ethos/src/lib.rs:31`
  - Now: `root: SemaStorageRoot,`
  - Proposed: `root: MemoryStorageRoot,`

- `/git/github.com/LiGoldragon/signal-ethos/tests/round_trip.rs:2`
  - Now: `use signal_sema_storage::{FixtureScope, SlotIdentifier};`
  - Proposed: `use signal_memory_storage::{FixtureScope, SlotIdentifier};`

- `/git/github.com/LiGoldragon/spirit-ethos/allocation-manifest.nota:52`
  - Now: `universal EthosSemaBody 41`
  - Proposed: `universal EthosMemoryBody 41`

- `/git/github.com/LiGoldragon/spirit-ethos/allocation-manifest.nota:53`
  - Now: `universal EthosSemaDocument 42`
  - Proposed: `universal EthosMemoryDocument 42`

- `/git/github.com/LiGoldragon/spirit-ethos/allocation-manifest.nota:165`
  - Now: `SpiritV14SemaProvenance.1`
  - Proposed: `SpiritV14MemoryProvenance.1`

- `/git/github.com/LiGoldragon/spirit-ethos/allocation-receipt.nota:36`
  - Now: `SpiritV14SemaProvenance.1`
  - Proposed: `SpiritV14MemoryProvenance.1`

- `/git/github.com/LiGoldragon/spirit-ethos/batch-config.json:5`
  - Now: `"sema_document": [42],`
  - Proposed: `"memory_document": [42],`

- `/git/github.com/LiGoldragon/spirit-ethos/batch-config.json:11`
  - Now: `"sema_body": [41],`
  - Proposed: `"memory_body": [41],`

- `/git/github.com/LiGoldragon/spirit-ethos/batch-config.json:164`
  - Now: `"preserved_sema_families": [`
  - Proposed: `"preserved_memory_families": [`

- `/git/github.com/LiGoldragon/spirit-ethos/batch-config.json:242`
  - Now: `{ "spelling": "EthosSemaBody", "root": "universal", "chain": [41] },`
  - Proposed: `{ "spelling": "EthosMemoryBody", "root": "universal", "chain": [41] },`

- `/git/github.com/LiGoldragon/spirit-ethos/batch-config.json:243`
  - Now: `{ "spelling": "EthosSemaDocument", "root": "universal", "chain": [42] },`
  - Proposed: `{ "spelling": "EthosMemoryDocument", "root": "universal", "chain": [42] },`

- `/git/github.com/LiGoldragon/spirit-ethos/flake.nix:22`
  - Now: `${pkgs.gnugrep}/bin/grep -Fx 'Sema.1' ${./sema.ethos}`
  - Proposed: `${pkgs.gnugrep}/bin/grep -Fx 'Memory.1' ${./memory.ethos}`

- `/git/github.com/LiGoldragon/spirit-ethos/flake.nix:41`
  - Now: `${pkgs.gnugrep}/bin/grep -Fx '    StoredRecord.{RecordIdentifier Entry}' ${./sema.ethos}`
  - Proposed: `${pkgs.gnugrep}/bin/grep -Fx '    StoredRecord.{RecordIdentifier Entry}' ${./memory.ethos}`

- `/git/github.com/LiGoldragon/spirit-ethos/flake.nix:42`
  - Now: `${pkgs.gnugrep}/bin/grep -Fx '    Migration.{SourceSchemaVersion MigratedRecordCount}' ${./sema.ethos}`
  - Proposed: `${pkgs.gnugrep}/bin/grep -Fx '    Migration.{SourceSchemaVersion MigratedRecordCount}' ${./memory.ethos}`

- `/git/github.com/LiGoldragon/spirit-ethos/flake.nix:48`
  - Now: `! ${pkgs.gnugrep}/bin/grep -E 'Certainty|Privacy|Referent|Candidate|Name\.\(|\||Text' ${./interface.ethos} ${./nexus.ethos} ${./sema.ethos}`
  - Proposed: `! ${pkgs.gnugrep}/bin/grep -E 'Certainty|Privacy|Referent|Candidate|Name\.\(|\||Text' ${./interface.ethos} ${./nexus.ethos} ${./memory.ethos}`

- `/git/github.com/LiGoldragon/spirit-ethos/flake.nix:49`
  - Now: `! ${pkgs.gnugrep}/bin/grep -E '^(Interface|Nexus|Sema)\.14$' ${./interface.ethos} ${./nexus.ethos} ${./sema.ethos}`
  - Proposed: `! ${pkgs.gnugrep}/bin/grep -E '^(Interface|Nexus|Memory)\.14$' ${./interface.ethos} ${./nexus.ethos} ${./memory.ethos}`

- `/git/github.com/LiGoldragon/spirit-ethos/flake.nix:62`
  - Now: `and (.grammar.sema_document == [42])`
  - Proposed: `and (.grammar.memory_document == [42])`

- `/git/github.com/LiGoldragon/spirit-ethos/flake.nix:113`
  - Now: `test "$(${pkgs.jq}/bin/jq '.preserved_sema_families | length' ${./batch-config.json})" = 2`
  - Proposed: `test "$(${pkgs.jq}/bin/jq '.preserved_memory_families | length' ${./batch-config.json})" = 2`

- `/git/github.com/LiGoldragon/spirit-ethos/flake.nix:115`
  - Now: `.preserved_sema_families == [`
  - Proposed: `.preserved_memory_families == [`

- `/git/github.com/LiGoldragon/spirit-ethos/meta-allocation-manifest.nota:54`
  - Now: `universal EthosSemaBody 41`
  - Proposed: `universal EthosMemoryBody 41`

- `/git/github.com/LiGoldragon/spirit-ethos/meta-allocation-manifest.nota:55`
  - Now: `universal EthosSemaDocument 42`
  - Proposed: `universal EthosMemoryDocument 42`

- `/git/github.com/LiGoldragon/spirit-ethos/meta-batch-config.json:9`
  - Now: `"sema_document": [`
  - Proposed: `"memory_document": [`

- `/git/github.com/LiGoldragon/spirit-ethos/meta-batch-config.json:27`
  - Now: `"sema_body": [`
  - Proposed: `"memory_body": [`

- `/git/github.com/LiGoldragon/spirit-ethos/meta-batch-config.json:496`
  - Now: `"spelling": "EthosSemaBody",`
  - Proposed: `"spelling": "EthosMemoryBody",`

- `/git/github.com/LiGoldragon/spirit-ethos/meta-batch-config.json:503`
  - Now: `"spelling": "EthosSemaDocument",`
  - Proposed: `"spelling": "EthosMemoryDocument",`

- `/git/github.com/LiGoldragon/spirit-ethos/sema.ethos:1`
  - Now: `Sema.1`
  - Proposed: `Memory.1`

- `/git/github.com/LiGoldragon/spirit-ethos/src/lib.rs:10`
  - Now: `pub const SEMA: &str = include_str!("../sema.ethos");`
  - Proposed: `pub const MEMORY: &str = include_str!("../memory.ethos");`

## Ambiguous (36)

- `/git/github.com/LiGoldragon/mind-context/skills/knowledge-ethos.md:6`
  - Now: `A file headed `Sema`, Memory's head before 15.0.0, is refused as `Conceptual.{ [ 0 ] Renamed.Memory }`.`
  - Why ambiguous: Sema here is the database root's former head, stated to document ethos-zero's refusal. It stays while ethos-zero refuses that head; if `Sema` becomes the meaning language's head in Ethos, the refusal changes in ethos-zero and this line follows the code.

- `/git/github.com/LiGoldragon/mind-context/skills/operation-lojix.md:303`
  - Now: `lojix-inspect-store 'InspectStore.{ /tmp/lojix.sema }'`
  - Why ambiguous: A store file extension naming the database. The line shows an invocation; `/tmp/lojix.memory` is right only if lojix's store files are renamed. The lojix code was not read in this pass.

- `/git/github.com/LiGoldragon/ethos-zero/README.md:59`
  - Now: `Memory record may be named `Record`. A file headed `Sema`, Memory's head`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:84`
  - Now: `- The `Sema` root is renamed `Memory`: same sections (imports, record`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:85`
  - Now: `types), same generation. A file headed `Sema` is refused as`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:101`
  - Now: `- Library API: `File::Sema(Sema)` is `File::Memory(Memory)`; `File` and`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:110`
  - Now: `1. Rename the head of every file headed `Sema` to `Memory`; nothing else in`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:111`
  - Now: `the file changes. Rename the file where its name says `sema`, if the`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:118`
  - Now: `No live consumer uses the Sema root (corrected after 15.0.0; flow 3ec648`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:119`
  - Now: `report `sema-to-memory.md`). The seven `.ethos` files under `/git` headed`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:120`
  - Now: ``Sema` are not ethos-zero consumers: spirit-ethos and core-ethos (core-schema)`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/UPGRADES.md:202`
  - Now: `Sema record prints `{ root\n  [ { first 1 } ] }`).`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/ethos-zero.ethos:10`
  - Now: `; A file headed Sema is refused as Renamed.Memory.`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:683`
  - Now: `/// `Sema` was the memory root's head until 15.0.0.`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:685`
  - Now: `if name == "Sema" {`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:982`
  - Now: `fn a_file_headed_sema_is_refused_naming_memory() {`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:983`
  - Now: `match Potential::<File>::from("Sema [] [ Record.{ String } ]").actualize() {`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:988`
  - Now: `_ => panic!("a Sema file is refused at its head"),`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/tests/cli.rs:302`
  - Now: `fn a_file_headed_sema_is_rejected_naming_memory() {`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/tests/cli.rs:303`
  - Now: `let directory = "sema".scratch();`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/tests/cli.rs:304`
  - Now: `let source = directory.write_source("sema", "Sema\n[]\n[ Record.{ String } ]\n");`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/tests/ethos.rs:59`
  - Now: `fn a_file_headed_sema_is_refused() {`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/ethos-zero/tests/ethos.rs:61`
  - Now: `Potential::<File>::from("Sema [] [ Record.{ String } ]")`
  - Why ambiguous: ethos-zero documents and implements the Sema to Memory rename of the database root (refusal `Renamed.Memory`, changelog, tests). Sema here is the database head as it was; whether the refusal, its tests and its changelog lines change depends on whether `Sema` becomes the meaning language's head.

- `/git/github.com/LiGoldragon/signal-ethos/ARCHITECTURE.md:7`
  - Now: `separate `sema-translator` owns only shared names and encodedID allocation.`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.toml:19`
  - Now: `sema-translator = { git = "https://github.com/LiGoldragon/sema-translator.git", rev = "6df830ab1ec9f315a5b50e40ffc393b48ea3d412" }`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.toml:23`
  - Now: `signal-sema-translator = { git = "https://github.com/LiGoldragon/signal-sema-translator.git", rev = "51c02c4a7b6f67d9dad095f11986085d7d65785b" }`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/README.md:38`
  - Now: ``sema-translator` store.  `allocation-receipt.nota` retains its typed request`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/allocation-manifest.nota:3`
  - Now: `allocator sema-translator`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/allocation-receipt.nota:8`
  - Now: `translator sema-translator`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/meta-allocation-manifest.nota:3`
  - Now: `allocator sema-translator`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/tests/meta_allocation.rs:7`
  - Now: `use sema_translator::{Runtime, StaticAuthorizationPolicy};`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/tests/meta_allocation.rs:9`
  - Now: `use signal_sema_translator::{`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/tests/meta_allocation.rs:204`
  - Now: `&directory.path().join("meta-allocation.sema"),`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/spirit-ethos/tests/meta_allocation.rs:208`
  - Now: `.expect("real isolated sema-translator runtime opens");`
  - Why ambiguous: sema-translator owns shared names and encodedID allocation in its own store. It is a store, but its subject is names; the ruling does not settle whether it becomes Memory or belongs to the meaning side.

- `/git/github.com/LiGoldragon/tree-sitter-ethos/package.json:23`
  - Now: `"sema",   (npm keyword)`
  - Why ambiguous: A package keyword; it does not say whether it names the database root.

- `/home/li/primary/flows/d68c82/books/65-switching-to-flow.md:10`
  - Now: `Observed ... against the running Flow Nexus 0.35.11 (Flow `67b80b3`, store `/home/li/.local/state/flow-production/flow.sema`) ...`
  - Why ambiguous: A real on-disk store path observed at a dated time; the meaning is the database, but `flow.memory` would misreport the observed path unless Flow renames its store file.

## Database meaning, no change proposed (9)

- `/git/github.com/LiGoldragon/psyche-context/vision/archive-ethos-monolith.md:43`
  - Now: The Signal, Nexus, SEMA vocabulary and principles are kept; nothing
  - Why: Archived psyche record; the archive keeps every original word.

- `/git/github.com/LiGoldragon/psyche-context/vision/archive-ethos-monolith.md:45`
  - Now: authored in ethos so its main operations are visible. Sema is the
  - Why: Archived psyche record; the archive keeps every original word.

- `/home/li/primary/flows/d68c82/books/38-ethos-nexus-chronos.md:45`
  - Now: Your words from 2026-10-02 to 2026-10-12 all name the stored part Memory, where this paragraph says Sema. This proposal takes Memory.
  - Why: Book prose naming the word Sema that Proposal 3 replaces.

- `/home/li/primary/flows/d68c82/books/38-ethos-nexus-chronos.md:48`
  - Now: - queries and responses, since there is communication; Sema's are record
  - Why: Removed line of Proposal 3; its added lines already say Memory.

- `/home/li/primary/flows/d68c82/books/38-ethos-nexus-chronos.md:50`
  - Now: - Sema its database types.
  - Why: Removed line of Proposal 3; its added lines already say Memory.

- `/home/li/primary/flows/d68c82/books/38-ethos-nexus-chronos.md:285`
  - Now: Amends Proposal 3; the rename to Memory also reaches the Associations paragraph, which still says Sema.
  - Why: Book prose naming the word Sema that Proposal 22 replaces.

- `/home/li/primary/flows/d68c82/books/38-ethos-nexus-chronos.md:287`
  - Now: - dot, a bracket of its traits. In the Signal and Sema roots the
  - Why: Removed line of Proposal 22; its added line already says Memory.

- `/home/li/primary/flows/d68c82/books/38-ethos-nexus-chronos.md:294`
  - Now: Amends Proposal 16; your word of 2026-10-09 calls loading configuration files in succession a hack to get the Nexus started until datom path expansion is solved, and the Configuration paragraph still says Sema.
  - Why: Book prose naming the word Sema that Proposal 23 replaces.

- `/home/li/primary/flows/d68c82/books/38-ethos-nexus-chronos.md:296`
  - Now: - it looks for its Sema database at the default location: a database
  - Why: Removed line of Proposal 23; its added line already says Memory.

## Lockfiles: generated dependency entries (55)

These follow Cargo.toml and flake.nix once the repositories sema, sema-engine, sema-storage, sema-translator, signal-sema, signal-sema-storage and signal-sema-translator are renamed or dropped; those repositories lie outside this pass.

- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:200`: `"sema-storage",`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:202`: `"signal-sema-storage",`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:633`: `name = "sema"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:635`: `source = "git+https://github.com/LiGoldragon/sema.git?rev=51d7927c872f0df12791bad8d39a4db6433b01a1#51d7927c872f0df12791bad8d39a4db6433b01a1"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:643`: `name = "sema-engine"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:645`: `source = "git+https://github.com/LiGoldragon/sema-engine.git?rev=93a6b5f063292e000a7bf395fdd5b46e3e943068#93a6b5f063292e000a7bf395fdd5b46e3e943068"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:649`: `"sema",`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:651`: `"signal-sema",`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:656`: `name = "sema-storage"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:658`: `source = "git+https://github.com/LiGoldragon/sema-storage.git?rev=269953164460cd842c1f3f8c9c93e4afe1e3628e#269953164460cd842c1f3f8c9c93e4afe1e3628e"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:663`: `"sema-engine",`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:665`: `"signal-sema-storage",`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:712`: `"signal-sema-storage",`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:738`: `name = "signal-sema"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:740`: `source = "git+https://github.com/LiGoldragon/signal-sema.git?rev=4f3a24e6677ab9d200672851016c4c760c1e36e8#4f3a24e6677ab9d200672851016c4c760c1e36e8"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:747`: `name = "signal-sema-storage"`
- `/git/github.com/LiGoldragon/ethos-engine/Cargo.lock:749`: `source = "git+https://github.com/LiGoldragon/signal-sema-storage.git?rev=31ab48608a3c2eab0733dcb16a3351251a70789d#31ab48608a3c2eab0733dcb16a3351251a70789d"`
- `/git/github.com/LiGoldragon/signal-ethos/Cargo.lock:360`: `"signal-sema-storage",`
- `/git/github.com/LiGoldragon/signal-ethos/Cargo.lock:386`: `name = "signal-sema-storage"`
- `/git/github.com/LiGoldragon/signal-ethos/Cargo.lock:388`: `source = "git+https://github.com/LiGoldragon/signal-sema-storage.git?rev=31ab48608a3c2eab0733dcb16a3351251a70789d#31ab48608a3c2eab0733dcb16a3351251a70789d"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:164`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:181`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:198`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:215`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:235`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:255`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:519`: `"sema-engine 0.12.0",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:523`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:742`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:762`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:782`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:834`: `name = "sema"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:836`: `source = "git+https://github.com/LiGoldragon/sema.git?rev=51d7927c872f0df12791bad8d39a4db6433b01a1#51d7927c872f0df12791bad8d39a4db6433b01a1"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:844`: `name = "sema-engine"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:846`: `source = "git+https://github.com/LiGoldragon/sema-engine.git?rev=94d2f7ee7b81d0bf3b6f1a111f6bbbc398c0e7a3#94d2f7ee7b81d0bf3b6f1a111f6bbbc398c0e7a3"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:850`: `"sema",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:852`: `"signal-sema",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:857`: `name = "sema-engine"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:859`: `source = "git+https://github.com/LiGoldragon/sema-engine.git?rev=98a6a252730bfba9d63afd9c5f73a2bc87000a8e#98a6a252730bfba9d63afd9c5f73a2bc87000a8e"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:863`: `"sema",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:865`: `"signal-sema",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:870`: `name = "sema-translator"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:872`: `source = "git+https://github.com/LiGoldragon/sema-translator.git?rev=6df830ab1ec9f315a5b50e40ffc393b48ea3d412#6df830ab1ec9f315a5b50e40ffc393b48ea3d412"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:877`: `"sema-engine 0.11.2",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:879`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:1007`: `name = "signal-sema"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:1009`: `source = "git+https://github.com/LiGoldragon/signal-sema.git?rev=4f3a24e6677ab9d200672851016c4c760c1e36e8#4f3a24e6677ab9d200672851016c4c760c1e36e8"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:1016`: `name = "signal-sema-translator"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:1018`: `source = "git+https://github.com/LiGoldragon/signal-sema-translator.git?rev=51c02c4a7b6f67d9dad095f11986085d7d65785b#51c02c4a7b6f67d9dad095f11986085d7d65785b"`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:1057`: `"sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/Cargo.lock:1061`: `"signal-sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/flake.lock:479`: `"sema-translator": "sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/flake.lock:861`: `"sema-translator": {`
- `/git/github.com/LiGoldragon/spirit-ethos/flake.lock:877`: `"repo": "sema-translator",`
- `/git/github.com/LiGoldragon/spirit-ethos/flake.lock:883`: `"repo": "sema-translator",`

## Not hits: `DatabaseMarker` matches the pattern across `seMa` (17)

`spirit-ethos/allocation-manifest.nota:31`, `spirit-ethos/batch-config.json:221`, `spirit-ethos/interface.ethos:19`, `spirit-ethos/interface.ethos:60`, `spirit-ethos/meta-allocation-manifest.nota:33`, `spirit-ethos/meta-batch-config.json:175`, `spirit-ethos/meta-batch-config.json:349`, `spirit-ethos/meta.ethos:2`, `spirit-ethos/meta.ethos:35`, `spirit-ethos/meta.ethos:36`, `spirit-ethos/meta.ethos:41`, `spirit-ethos/meta.ethos:44`, `spirit-ethos/meta.ethos:47`, `spirit-ethos/tests/meta_allocation.rs:11`, `spirit-ethos/tests/meta_allocation.rs:83`, `tree-sitter-ethos/test/fixtures/ethos/derived-members.ethos:9`, `tree-sitter-ethos/test/fixtures/ethos/derived-members.ethos:18`
