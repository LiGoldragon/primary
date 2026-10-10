# Next-generation syntax → Spirit foundation audit v1

Audited 2026-07-14. This is a source-and-runtime audit, not an implementation plan acceptance or deployment authorization. It incorporates the psyche-settled Core rulings from the dispatch:

- every `Core*` is stringless and uses its corresponding `NameTable`;
- Core identity is domain-separated, layout-version-tagged BLAKE3 over stringless Core rkyv bytes, excluding the `NameTable`, so rename is hash-stable;
- `CoreNomos` is durable state at rest, symmetric with Schema and Logos.

## Executive findings

### The next-generation NOTA branch is real, complete for its own contract, and not integration-ready

`nota` bookmark `next-gen` is pushed at `08ce05ca` (`nota` 0.8.0, `nota-derive` 0.4.0), three commits ahead of `main` `f8de7a51`. Its changed surface is intentionally a public raw-tree break: `Block::Application` is added and parsing is right-associative (`A.B.C = App(A, App(B,C))`), codecs use dotted variants and `Map.(key.Value ...)`, structs use braces, strings use bare/parenthesis/pipe-parenthesis projection, and floats reconstruct from dotted raw structure.

This audit reconstructed exactly that revision in `/tmp` without modifying the checkout. Both `cargo test --all-targets` and the durable Nix `checks.x86_64-linux.test` passed: 14 next-generation grammar tests, 24 macro-node tests, and all other test binaries passed. The tests directly witness the three proposed readings: right association, dotted-float reconstruction, and pipe-parenthesis treatment of period-bearing strings.

It cannot be merged as an isolated release. Rebuilding `schema-language` `59d59aca` against the exact 0.8.0 source fails before tests: three removed `Atom::split_at_first_dot` call sites and ten non-exhaustive matches on the new `Block::Application` (including `src/raw.rs`, `src/source.rs`, `src/declarative.rs`, `src/expansion.rs`, and `src/schema.rs`). This is the correct kind of break—raw syntax is deliberately no longer hidden—but establishes that downstream migration is a blocking release-train dependency, not post-merge cleanup.

`StructuralMacroNode` remains headed in `nota/tests/macro_nodes.rs` and derive generation. That is the one visible pre-next-gen syntax survivor. It must be settled and converted before schema can use it as its normal structural decoder; retaining a compatibility headed path would create a permanent special case.

### The current schema foundation is farther along than the handover says, but not yet compliant with the clarified Core contract

The current `schema-language` `main` is `59d59aca`, not the old source revision cited by `reports/logos/core-first-architecture-v1.md`. It already contains `src/core.rs`, `src/identifier.rs`, `src/view.rs`, `src/identity.rs`, `src/lineage.rs`, and Core/NameTable test suites. `TrueSchema` is currently a view holding `SchemaIdentity`, `CoreSchema`, and `NameTable`; its tests prove table-mediated rename preserves Core bytes and moves the true/name hash. The Nix test derivation passed all schema-language tests, including core projection, identity, identifier-substrate, import-unification, lineage, and upgrade witnesses.

The implementation is a useful bridge, not the final universal Core substrate:

- `CoreSchema::canonical_bytes()` is rkyv and `TrueSchema::core_hash()` uses a domain-separated BLAKE3 context over it, while `NameTable` is excluded. This satisfies the central rename-stability direction.
- It does **not** visibly carry an explicit Core layout-version value in the hash preimage. The date-bearing BLAKE3 context is not a durable, typed layout-version protocol. The settled ruling needs a typed `CoreLayoutVersion` included in every Core identity envelope and test vectors for a version bump.
- It is not fully stringless. `CoreImportDeclaration` stores `source: TypeReference` (`src/core.rs:284-305`), and Core declarations retain name-bearing schema-side facts such as `ImplCatalog`. The existing documentation permits some provenance exceptions, but the new ruling says every `Core*` is stringless. These are design conflicts to remove or explicitly relocate to a non-Core source/provenance sidecar.
- The current nominal identity is a 128-bit digest minted from names and re-associated through a prior table (`src/identifier.rs`), explicitly marked provisional. File-only rename is indistinguishable from deletion plus addition without the previous table. It is appropriate bootstrap machinery but cannot be the authoritative daemon identity allocator.
- `TrueSchema` still serializes through a name-bearing `SchemaTree` sidecar for text and binary codecs (`src/view.rs`). That preserves current compatibility but means binary wire/storage is not yet Core-first.

The previously published core-first report is therefore materially stale in its foundational observation that CoreSchema and NameTable do not exist. Its architecture direction remains useful, but implementation statements must be re-audited against `schema-language` main before being used as authority.

### Nomos and Logos do not exist as source components or contracts

There are no `repos/nomos`, `repos/logos`, `repos/signal-nomos`, or `repos/signal-logos` checkouts, and no implementation references to Nomos/Logos conversion operations in the audited source repositories. The existing `signal-schema` `0.1.0` only offers `LoadPackage` and `EmitRust`, carries source text on its wire, and still has build dependencies on the older `schema`/`schema-rust` `trueschema` branches. It does not expose slot listing, hash fetch, Core plus NameTable, or conversion.

The newest Nomos report (`nomos-macro-model-v1.md`) documents a good target, but no lexer/parser/runtime implements `$` realization/splice/recursive invocation, macro identity lookup, structural macro fallback, CoreNomos persistence, or CoreLogos. Nomos and Logos must begin as new typed components, not as an edit to the Spirit daemon.

### Spirit is a deployment pilot and acceptance oracle, not a safe first host for the raw grammar change

Spirit `main` is at `33f16e7d`; both current CriomOS and CriomOS-home locks pin that same Spirit revision. Spirit's own flake lock pins an older NOTA revision `d25c08a`, schema-language `6aae825d`, and schema-rust `f3b4563`, not this audit's current source revisions and not `nota/next-gen`. The daemon keeps its desired binary-only invariant: NOTA is optional `nota-text`, and `tests/dependency_surface.rs` guards its absence from the normal daemon tree. Runtime code consumes checked-in generated Rust, not schema text.

Spirit and sema-engine are strong acceptance assets:

- Spirit has versioned-store, checkpoint/suffix restore, process-boundary, generated-source freshness, and Nix integration witnesses.
- `sema-engine` 0.7.0 already provides the needed durable pattern: rkyv typed values, a versioned hash chain, checkpoint/refold validation, durable staging, and a rebuildable materialized view (`src/versioning.rs`, `src/checkpoint.rs`, `src/fold.rs`). It is a storage mechanism, not a Core identity or name-allocation policy.
- The current deployment is **not healthy evidence**. The user service `spirit-daemon.service` is inactive/dead (successful explicit stop, no running daemon) while `spirit-judge.service` is active. The state directory still has stale Spirit sockets; the working socket is mode 0755. Historical journal lines show both a July 6 start-limit event and repeated manual stop/start cycles. No activation, recovery, store inspection, or mutation was attempted by this audit.

Do not deploy a syntax branch to Spirit until the current service has first been independently recovered and verified against its present pinned closure and store migration path. The rollout must neither treat stale socket files as liveness nor use the language migration to repair runtime health.

### The published reports and tracker are useful but have status drift

`primary-56d1` is open with all seven children open; `primary-z4s9` correctly records `next-gen` as pending psyche acceptance. The older grammar report labels the delimiter reshuffle as leaning and says raw dot application is unimplemented, while the branch has implemented and tested both. Several sample files still present contradicted v0/v1 syntax alongside v2. Conversely, the source shows the Core/NameTable work that `core-first-architecture-v1.md` says is absent. The next phase needs a single generated or hand-maintained decision/status ledger with source revision stamps; otherwise designers and implementers will keep choosing incompatible premises.

The previously reported substituter outage is not current evidence: both Nix test derivations in this audit built through the configured remote builder successfully.

## Recommended implementation design

### One Core substrate contract, then three language components

Make Core the authoritative typed representation, with text only an import/export projection. Each language has a typed stored pair:

```text
CoreSchema + SchemaNameTable
CoreNomos  + NomosNameTable
CoreLogos  + LogosNameTable
```

`CoreLogos` begins from the schema allocation and appends new identifiers; it must not duplicate a string keyed lookup table. A Core object contains only closed structural variants, stable typed identifiers, scalar values, and references by identifier. Human names, source locations, source import provenance, original formatting, and error rendering live in typed sidecars/projections, never in the Core content-address preimage.

Define a `CoreEnvelope` for every stored/fetched Core value:

```text
CoreEnvelope { language_domain, layout_version, core_rkyv_bytes, core_hash }
```

`core_hash` is recomputed from a domain-specific BLAKE3 context plus an encoded typed layout version and canonical Core rkyv bytes. `NameTable` bytes, display names, text, source spans, and daemon slot names are excluded. A fetched object always carries or is paired with the exact NameTable revision needed to project it, but that revision is a separate identity/address. A rename writes a NameTable delta and a Core-preserving receipt; it must never silently regenerate identifiers.

Do not make `sema-engine` own this semantic identity. Use it as the durable journal/table/checkpoint engine under each daemon. Schema/Nomos/Logos own their domain records and translate typed operations to its registered families.

### NameTable library opportunity and ownership

There is a real shared library seam, but only for generic substrate mechanics: typed stable identifier, name table, typed layout/domain/version envelope, Core hash construction, Core/NameTable pairing validation, and Core-preserving rename receipt. Domain ASTs, schema import semantics, macro syntax, and Logos vocabulary remain in their owning language components.

Do not extract the current `schema-language/src/identifier.rs` mechanically. It is schema-coupled, retains provisional name-derived minting, and would fossilize that bridge. First write conformance fixtures for the generic contract in `schema-language`; then extract the small library immediately before CoreNomos consumes it. Recommended ownership is a dedicated `language-core` library repository/package maintained by the language-stack owner, with schema-language as the first consumer and Nomos/Logos as the second/third. This is a library because identical serialized identity semantics are required across components, not merely similar helper functions. Its first release must state the bootstrap-import rule and forbid file text from becoming the allocator after daemon adoption.

### Macro and projection design

Nomos accepts `CoreSchema + SchemaNameTable` and a durable macro package selected by stable macro identity. Its conversion result is typed `CoreLogos + extended LogosNameTable`; no text crosses the schema→Nomos→Logos boundary. Named macro misses on `X.()` are closed typed errors. Structural defaults are an ordered, per-section table keyed by closed structural shapes, so `X.{...}` remains a normal macro lookup rather than ad hoc parser logic.

Keep Logos maximally explicit in Core: visibility, declaration kind, fields, variants, attributes, derive groups, paths, and field names are all data. Text may elide only a field name that is mechanically derived, because Core still contains that name identity. Rust transcription has exactly one responsibility: map Logos paths' dots to Rust `::`, render delimiters/tokens, and preserve the fully represented meaning. Existing schema-rust fixtures are the initial byte-for-byte Rust oracle; no Rust-token parser should be introduced.

## Smallest coherent branch and integration topology

A single `nota` merge followed by downstream fixes is unsafe. Use one release train with pinned, immutable commit inputs and one temporary integration root:

1. Keep `nota/next-gen` at `08ce05ca` unmerged as the immutable grammar producer. Do not retarget production to it.
2. Create a schema-language next-gen integration branch that pins that exact commit, changes its raw-tree consumers to `Block::Application`, converts all source fixtures/canonical emitters, resolves StructuralMacroNode, and completes the Core compliance work. Its tests must prove old syntax rejection, new syntax round-trip, Core stringlessness, layout-versioned hash identity, and rename stability through persisted allocations.
3. Create a schema-rust integration branch pinned to that schema-language revision. Preserve every current generated Rust golden exactly while replacing its `TrueSchema`-centric lowering boundary with Core plus NameTable projection where required.
4. In parallel only after the common Core contract stabilizes, create `language-core`, `signal-nomos` plus Nomos, and `signal-logos` plus Logos. Add the slot-list/fetch family to the existing schema signal contract on its own wire-compatible versioned branch. New contracts must be binary/rkyv-only by default; NOTA belongs only to CLI/debug projections.
5. Create an integration Spirit branch with a flake lock pinning the exact release-train commits, regenerated `signal-spirit`/`meta-signal-spirit` schema artifacts, unchanged runtime binary boundary, and a data-store migration only if a new runtime record/wire schema actually changes. It must have no dependency on a local worktree or an unmerged producer.
6. Only after a green integration closure, create deployment-pin branches in CriomOS-home and CriomOS. Deploy first to an isolated copy/sandbox store and a separate versioned socket. Promotion is a Lojix deployment with a recorded pre-deploy database/archive backup and an explicit restore procedure, never profile rollback alone.

This topology permits parallel work but gives one dependency direction: `language-core → nota/schema-language → schema-rust + contracts → Nomos/Logos → Spirit → deployment pins`. Nomos/Logos scaffolding may begin once `language-core` has a committed contract, but no source tree should depend on unpublished branch names.

## Bootstrapping and self-hosting sequence

1. Freeze the small bootstrap seed: raw NOTA parser, rkyv Core envelope codec, and the first schema importer. It is allowed to read text but cannot own semantic identity.
2. Make schema daemon state Core-first. A bootstrap import mints/persists allocations once; subsequent edits are typed daemon operations and write Core/NameTable/lineage receipts atomically through sema-engine.
3. Implement Nomos as a stateful CoreNomos package registry and conversion daemon. Prove deterministic conversion of a bounded schema corpus to CoreLogos.
4. Implement Logos storage, fetch/list, text projection, and Logos→Rust transcription. Compare output exactly to current schema-rust goldens.
5. Switch schema-rust's build driver to consume Logos output for a bounded pilot, retaining schema-rust as the oracle/fallback only during the measured equivalence period.
6. Once the full corpus and deployment stacks are equivalent, make Logos the Rust generator and migrate the compiler definition toward schema/Nomos self-hosting. The original seed remains a deliberately small bootstrap reader, not a second compiler.

## Deployment-readiness gates

No gate is satisfied merely by a green NOTA unit suite.

1. **Grammar contract:** grammar rulings are explicitly marked accepted; StructuralMacroNode is dotted; all active schema/Nomos/Logos samples are canonical; old grammar has rejection tests rather than a permissive compatibility parser.
2. **Core contract:** property tests and persisted-store tests prove every Core type has no `String`/name-bearing field; a rename changes only NameTable receipt state; Core hashes are domain-separated and layout-version-tagged; a deliberately changed layout refuses/uses an explicit upgrader; schema-to-logos allocation extension preserves existing IDs.
3. **Compatibility and migration:** schema-language, schema-rust, all contract producers, and their generated artifacts compile against exact pinned next-gen NOTA. Rust oracle goldens are byte-identical. Any real wire/storage schema change has version bumps, typed migration, legacy fixture, forward migration, and rollback/restore evidence.
4. **Component contracts:** schema, Nomos, Logos each have rkyv frame round trips, slot-listing and hash-fetch tests, typed rejection tests, process-boundary tests, and no runtime NOTA dependency in binary-only dependency trees.
5. **Durability:** each daemon proves restart/resume, checkpoint plus suffix restore, tampered hash-chain rejection, Core/NameTable atomic co-versioning, and deterministic rebuild from the authoritative sema-engine log.
6. **Spirit integration:** a Nix-built isolated Spirit daemon using the exact integration lock starts with a fresh copied store, serves representative record/query flows, and proves the normal daemon binary does not link NOTA. Existing Spirit production migration tests must pass against both an old production fixture and a copied non-production state store.
7. **Deploy and rollback:** first restore current Spirit health independently; pre-deploy backup and hash are recorded; Lojix reaches active/current state; `spirit-daemon.service` is active, a real daemon owns freshly created sockets, `Version` and representative queries succeed, and recent journal output is clean. A rollback rehearsal restores the pre-deploy store into an isolated environment, because a profile rollback does not reverse a migrated `.sema` database.
8. **Portability:** every producer commit is pushed, every flake/Cargo pin resolves without a local path, flake checks pass from the integration closure, and deployment uses no runtime source replacement or PATH shim.

## Contradictions, risks, and material unknowns

- The phrase “every Core is stringless” conflicts with current `CoreSchema` fields that retain `TypeReference` and implementation/source facts. This must be resolved before claiming the current Core code is the shared model.
- The completed Core hash lacks an explicit layout-version type in its observed preimage. Existing domain separation is insufficient for safe format evolution.
- Existing `schema-language` passes its own tests but cannot compile against the exact next-generation NOTA API. This is the immediate technical blocker.
- Reports disagree with source on both grammar status and Core existence; samples contain multiple contradictory Nomos syntaxes. A status ledger and sample retirement/reclassification are required before implementation begins.
- The macro escape surface (`$` versus brackets), explicit name synthesis, Nomos meta-type location, and delimiter wording remain design questions. They should not be guessed in a contract crate.
- Current actual Spirit runtime is inactive with stale sockets. This blocks a deployment-readiness claim independent of syntax work.
- Current deployment locks pin old producer revisions. The future integration must update the entire pinned closure, not only `nota`.
- The unit of one schema and split/merge identity semantics remain unresolved. They affect persisted schema-daemon records and therefore must be decided before daemon storage schema is finalized.

## Psyche-only question slate

### Already settled; no new ruling requested

1. Core values are stringless and use their corresponding NameTables.
2. Core identity is domain-separated, layout-version-tagged BLAKE3 over stringless Core rkyv bytes, excluding NameTable; rename is hash-stable.
3. CoreNomos is stateful/durable at rest, symmetric with Schema and Logos.

### Decisions needed before implementation, in priority order

1. **StructuralMacroNode:** should its sole canonical text form become dotted application, with no headed compatibility decoder? **Recommendation: yes.** This removes the last semantic exception and lets all structural forms use one raw application node.
2. **Next-generation grammar acceptance:** bless right-associative dot, numeric reconstruction of dotted floats, and pipe-parenthesis for period-bearing strings. **Recommendation: yes.** All three are implemented and independently tested on `08ce05ca`; their rules are coherent provided literal text escaping remains explicit.
3. **Core-sidecar boundary:** may import source paths, source spans, implementation catalog strings, and other human/provenance data remain outside Core in typed sidecars, while all semantic references inside Core use identifiers? **Recommendation: yes.** This is the only clean reading that honors absolute Core stringlessness without losing provenance.
4. **Name substrate library:** authorize `language-core` as the owner of generic identifier/NameTable/CoreEnvelope/hash semantics, extracted only after schema-language conformance fixtures define the API. **Recommendation: yes.** Do not extract the present provisional name-minting implementation unchanged.
5. **Nomos surface:** choose `$` for realization/splice/recursive invocation and no fourth name-synthesis escape until a concrete non-derived naming operation requires it. **Recommendation: `$`; no fourth escape now.** Derived names are ordinary Core data; fresh name minting is a daemon identity operation, not a template trick.
6. **Meta-types:** should Nomos `Name`, `Type`, `Fields`, and `Variants` use one shared schema seed vocabulary? **Recommendation: yes.** One typed meta-model avoids parallel self-description vocabularies.
7. **Logos visibility:** confirm it is ordinary outer right-associative application (`Public.Newtype`, `Private.name.Type`) rather than a family of specialized declaration types. **Recommendation: yes.** It preserves one composition mechanism across declarations and fields.
8. **Persistence topology:** accept Core plus NameTable as first-class co-versioned sibling records in each language daemon, using sema-engine log/checkpoint mechanics; Logos is rebuildable but may be persisted as a cache. **Recommendation: yes.** This makes rename a normal Core-preserving journal operation and gives restart/rebuild evidence.
9. **Schema unit/split/merge identity:** define the durable unit that owns one NameTable and the rule for splitting/merging it. **Recommendation: one daemon-held loaded whole owns one allocation; splitting creates new allocation domains and merge requires an explicit identifier-remap receipt.** Guessing this would make stored identity and conversion behavior inconsistent.
10. **Spirit rollout authority:** may the release train use an isolated copied store and versioned socket before any production Lojix deployment? **Recommendation: yes, required.** Current Spirit inactivity and stale sockets make direct deployment unsafe.
