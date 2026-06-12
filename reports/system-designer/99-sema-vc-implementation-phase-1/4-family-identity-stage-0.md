# 99/4 — sema-engine typed family identity + stage 0 + mind memory-graph family

*Implementation sub-agent chapter (workflow run `wf_8724d72d-bd4`, 2026-06-12, system-designer lane). The adversarial review — which independently re-ran every test suite — is appended.*

# Typed family identity in the versioned log + Stage 0 (the log becomes complete)

Two branches, both pushed and green: `versioned-family-identity` in sema-engine (0.2.3 → 0.3.0) and `memory-graph-family` in mind (0.2.0 → 0.3.0, based on a fresh `origin/main`, narrow scope). 67 sema-engine tests + 65 mind tests pass; both crates build and lint clean (`cargo clippy --all-targets` zero warnings).

## Part 1 — typed family identity (sema-engine)

New nouns in `src/versioning.rs`:

- `FamilyName(String)` (:42) — the schema declaration name, the stable semantic identity that survives table renames.
- `SchemaHash([u8; 32])` (:78) — re-scoped as the **per-family** blake3 content hash, supplied as a typed value at registration (`for_label` retained as the transitional constructor until schema-rust-next emits content hashes from `.schema`; no schema-crate dependency added).
- `StoreSchemaHash([u8; 32])` (:120) — the **derived** store-level identity: `impl From<&Catalog> for StoreSchemaHash` (:128) computes domain-separated blake3 (`sema-engine-store-schema-hash-v1`, length-prefixed fields) over the **sorted (family, schema_hash) inventory**; table names are excluded, so a rename keeps store identity stable. It is structurally impossible to hand-supply: `StoreSchemaHash` has no public constructor.
- `FamilyIdentity { family, schema_hash, table_name }` (:157) with `shares_family` (:187) — the replay dispatch relation: family name + per-family hash, table coordinate deliberately ignored. The archived form owns the table name as `String` (constructor takes `TableName`), matching the prior `VersionedLogOperation` idiom, because `TableName` wraps `&'static str` and cannot archive.

`VersionedLogOperation` now carries `family: FamilyIdentity` instead of `table_name: String` (versioning.rs:341-417); `table_name()` survives as a convenience accessor documented as the logged coordinate, not the dispatch key. `VersionedCommitLogEntry.schema_hash` is now `StoreSchemaHash` and the entry-digest domain string bumped to `sema-engine-versioned-commit-log-entry-v2` (:243).

Registration carries identity: `TableDescriptor` / `IdentifiedTableDescriptor` gain `family + schema_hash` (table.rs:30-105, constructors at :50/:77; descriptors lost `Copy` since `FamilyName` owns a `String`). The catalog **is** the family inventory: `TableRegistration { identity: FamilyIdentity }` (catalog.rs:63-67), with `Catalog::family_identity` / `registration_for_family` lookups. `Engine::family_registration_state` (engine.rs:1244) rejects re-registration under a conflicting identity (`FamilyIdentityMismatch`) and a second table binding the same family version (`FamilyAlreadyBound`); the persisted inventory rebuilds the catalog at open. `VersioningPolicy` lost `schema_hash` — `VersioningPolicy::new(VersionedStoreName)` (versioning.rs:13-15); every versioned entry stamps `Engine::store_schema_hash()` (engine.rs:1118) derived at entry time.

**Clean break**: no migration. Engine-internal storage layout guard `STORAGE_LAYOUT = 2` persisted in the counters table (engine.rs:34-38, `guard_storage_layout` :1211). A pre-family-identity store (no layout slot but engine counters present, or a catalog row that no longer decodes — both checked at `Engine::open` :55-72) hard-fails with typed `Error::StorageLayoutMismatch { stored: 1, expected: 2 }` (error.rs:8-12). Crate version 0.2.3 → 0.3.0 per skills/versioning.md (breaking pre-1.0 ⇒ minor).

## Part 2 — Stage 0: the log becomes complete

### Sweep — every `storage_kernel` use across /git/github.com/LiGoldragon/*/src

| Component | Site | Kind | Disposition |
|---|---|---|---|
| sema-engine | engine.rs:1080 `pub fn storage_kernel()` | the leak | **removed**; replaced by read-only `storage_reader()` |
| mind | tables.rs:144 (`ensure` 3 local tables at open) | writer | **migrated** — tables registered as engine families |
| mind | tables.rs:175 (`memory_graph` read) | reader | **migrated** to `match_records` |
| mind | tables.rs:180 (`replace_memory_graph`) | writer | **migrated** to engine mutate/assert |
| mind | tables.rs:293, :325 (subscription persists) | writers | **migrated** to engine `assert` |
| mind | tables.rs:615 (test read) | reader | **migrated** to `match_records` |
| orchestrate | tables.rs — writers :72 (open ensure), :114 insert_role, :129 remove_role, :154 insert_lane, :167 replace_lanes, :184 remove_lane, :207 replace_repositories, :224 replace_claims, :255 append_activity, :276 append_divergence; readers :87, :97, :109, :137, :149, :192, :263, :288, :308, :321 | both | **stage-0 residue** — entire component-local table layer (claims/roles/lanes/repositories/activities/divergences); non-trivial, pins sema-engine `main` |
| persona | manager_store.rs:267 write_engine_record, :293 write_engine_event, :388 rebuild_snapshots_from_event_log, :424 truncate_and_rebuild_snapshots | writers | **stage-0 residue**; note persona/tests/manager_store.rs:884-928 is a source-scan truth test that *requires* the literal `storage_kernel().write(` text — persona's migration must rewrite that witness too |
| router | tables.rs:66 (open ensure), :106 insert_channel | writers | **stage-0 residue** |

Residue components pin `sema-engine` `branch = "main"` in Cargo, so they keep building and running untouched; they break only when an operator rebases sema-engine main onto this branch, at which point each needs the mind-style family migration.

### The narrowed kernel handoff

`Engine::storage_reader()` (engine.rs:1112) returns `StorageReader<'engine>` (:1544) whose entire public surface is one `read` method over `sema::ReadTransaction` — **the type has no write affordance; the type system is the witness**. `lib.rs` no longer re-exports `Sema as StorageKernel` or `WriteTransaction as StorageWriteTransaction`; it re-exports `ReadTransaction as StorageReadTransaction` for transitional local-table reads. The architectural truth test `tests/storage_boundary.rs` pins this: no `pub fn storage_kernel`, no public method returning `&sema::Sema`, no `WriteTransaction` re-export, `StorageReader` has read and only read, plus a behavioral witness that the reader observes state written through the logged choke points. Engine-internal catalog/counter bookkeeping still writes directly — that is the log's own dispatch substrate, not component record state.

### Replay on family identity

`Engine::replay_versioned(VersionedReplay)` (engine.rs:1128) folds versioned entries into the registered family named by a `TableReference`, dispatching each operation on `FamilyIdentity::shares_family` and applying through the **public** choke points (assert_keyed / mutate_keyed / retract), so a rebuilt store logs its own complete history — iir4 realized: log authoritative, table store a rebuildable materialized view. `ReplayReceipt { applied, skipped }` reports family dispatch honestly.

### Witnesses (tests/family_identity.rs)

- :110 versioned log operations carry typed family identity; entry hash equals derived store hash.
- :131 **replay rebuilds typed state dispatching on family identity** (4 thought ops applied, 1 foreign-family op skipped, final state exact).
- :181 **the rename witness**: entries logged under `thoughts_v1` replay into `thoughts_v2` (same family, same schema hash).
- :223 store hash invariant under rename, distinct under inventory growth.
- :250/:275 typed rejection of conflicting identity / double family binding.
- :293 pre-family-identity store hard-fails `StorageLayoutMismatch { stored: 1, expected: 2 }`.
- Same-transaction witness stays green (`operation_log.rs` versioned tests; the versioned entry still inserts in the same kernel write transaction as the data row, engine.rs write closures).

## mind — memory-graph-family (narrow, based on fresh origin/main)

All durable mind state now flows through engine record families (src/tables.rs): `MIND_SCHEMA_VERSION` 7 → 8 (:21); `memory_graph`, `thoughts`, `relations`, `thought_subscriptions`, `relation_subscriptions` all registered via `family_descriptor` (:199, label-derived per-family `SchemaHash` stand-ins until schema generation); `EngineRecord` impls for `MemoryGraph` (key `current`, :139) and both subscription records (:145/:151); `memory_graph()` reads via `match_records` (:210); `replace_memory_graph` is assert-or-mutate through the logged choke points (:222); subscription persists are engine asserts. `versioning_policy()` is store-name-only (:191). Zero `storage_kernel` references remain in mind source/tests. Cargo points sema-engine at `branch = "versioned-family-identity"` with the lock pinned to 53426b14, so the branch builds standalone. `StoreKernel`/`MemoryStore`/`GraphStore` actor interfaces unchanged — the migration is entirely inside `MindTables`. INTENT.md, ARCHITECTURE.md, skills.md updated accordingly (INTENT bracket-quotes iir4 and fosp).

**Mind-store reset implication (honest)**: any existing `mind.sema` is unreadable on this branch — doubly guarded by the engine layout error (typed `StorageLayoutMismatch`) and mind's kernel schema bump v7→v8 (`SchemaVersionMismatch`). Every prior memory_graph replacement bypassed the log, so the old store has no complete versioned history to replay from; production mind state must be re-seeded (or re-imported at the domain level) when this lands. Per the brief, pre-production: accepted. Side effect worth knowing: each work/memory mutation now logs a full `MemoryGraph` snapshot payload into the versioned log, so the log grows with snapshot size per work mutation until the memory graph is decomposed into row-level families.

## Notes for the orchestrator

- sema-engine INTENT.md quotes iir4 (Decision), fosp (Correction), x0ja (Constraint), 29pb/j487 with identifiers; ARCHITECTURE.md constraints/surface updated (read-only handoff, family identity, derived store hash, replay, layout guard).
- The canonical mind checkout's working copy shows crate version 0.3.0 (system-operator's in-flight, uncommitted modernization) while origin/main was 0.2.0; this branch bumps 0.2.0 → 0.3.0, which may collide with that lane's intended number — reconcile at integration.
- Identified-table replay is not implemented (no consumer needs it yet); `replay_versioned` covers keyed families, and Match/Subscribe/Validate operations in a log return typed `ReplayUnsupportedOperation`.
- sema-engine's per-file nix test apps (`.#test-engine` etc.) still run; the two new test files are covered by `cargo test` / `.#test`.

## branches
- sema-engine @ versioned-family-identity head 53426b1457eb (/home/li/wt/github.com/LiGoldragon/sema-engine/versioned-family-identity)
- mind @ memory-graph-family head b7b1bd7785f1 (/home/li/wt/github.com/LiGoldragon/mind/memory-graph-family)

## testResults
sema-engine (cargo test, 67 passed / 0 failed across 8 suites):
test result: ok. 8 passed; 0 failed (dependency_boundary)
test result: ok. 22 passed; 0 failed (engine)
test result: ok. 7 passed; 0 failed (family_identity)
test result: ok. 7 passed; 0 failed (operation_log)
test result: ok. 6 passed; 0 failed (seam_gap_falsification)
test result: ok. 5 passed; 0 failed (signal_frame_seam)
test result: ok. 3 passed; 0 failed (storage_boundary)
test result: ok. 9 passed; 0 failed (subscriptions)
tail:
test subscribe_delta_kind_tracks_write_operation ... ok
test subscribe_commit_bundle_delivers_per_operation_deltas_after_single_snapshot_commit ... ok
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.09s
   Doc-tests sema_engine
running 0 tests
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

mind (cargo test, 65 passed / 0 failed across 7 suites):
test result: ok. 5 passed; 0 failed (lib unit)
test result: ok. 16 passed; 0 failed (actor_topology)
test result: ok. 6 passed; 0 failed (cli)
test result: ok. 11 passed; 0 failed (daemon_wire, incl. mind_memory_graph_survives_process_restart)
test result: ok. 7 passed; 0 failed (memory)
test result: ok. 3 passed; 0 failed (orchestrate_caller)
test result: ok. 17 passed; 0 failed (weird_actor_truth)
tail:
test parallel_runtimes_cannot_share_registry_names_or_memory ... ok
test kameo_is_the_only_actor_library_boundary ... ok
test result: ok. 17 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s
   Doc-tests mind
running 0 tests
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

## blockers
- None blocking the branches themselves. Integration-time items: (1) rebasing sema-engine main onto versioned-family-identity breaks orchestrate (orchestrate/src/tables.rs component-local table layer, ~10 write sites), persona (persona/src/manager_store.rs:267/:293/:388/:424 plus persona/tests/manager_store.rs:884-928 whose source-scan truth test requires the removed storage_kernel().write text), and router (router/src/tables.rs:66/:106) until each migrates to engine record families — all currently pin sema-engine main and keep working untouched. (2) Existing mind.sema stores hard-fail on the mind branch (engine StorageLayoutMismatch + mind schema v7->v8); no migration by design — production mind state must be re-seeded when this lands. (3) The canonical mind checkout carries an uncommitted version 0.3.0 (system-operator lane) while this branch bumps origin/main 0.2.0 -> 0.3.0; reconcile the number at integration.


## Adversarial review

VERDICT: approve

## mustFix
- The mind branch is based one commit behind origin/main: its parent is 7e29a4f4 (mind: opt store into sema-engine version log), missing main's tip b9cd8c23 (mind: modernize cli and meta policy entrypoint). A naive fast-forward/reset of main to the branch head would silently revert the CLI modernization (no-flags env-var CLI, meta-mind owner client, frame_bytes extraction, removal of the free function supervision_synthetic_exchange) — the raw diff origin/main...branch misleadingly shows all of that as deletions. REQUIRED: rebase memory-graph-family onto b9cd8c23 before integrating. I verified this myself in a scratch clone: git rebase main completes with zero conflicts (Cargo.lock included) and the full integrated suite passes 65/65 across all 7 suites. The branch's own content (6 files: ARCHITECTURE.md, Cargo.toml/lock, INTENT.md, skills.md, src/tables.rs) is untouched by the rebase.
  AT: /home/li/wt/github.com/LiGoldragon/mind/memory-graph-family (branch memory-graph-family, head b7b1bd7785f1; parent 7e29a4f4cfa0, not main@origin b9cd8c23894c)

## advisory
- Per-family schema hashes are still hand labels: mind/src/tables.rs:199-208 family_descriptor uses SchemaHash::for_label("mind-{family}-v8"), and every sema-engine test does the same. Handoff report 97 §4 named schema-generated content hashes (blake3 of the canonical .schema definition via schema-rust-next LowerToRecordFamily) as 'the recommended core of Stage 1'. The branch honestly documents the label as a typed stand-in (tables.rs:195-198, ARCHITECTURE.md), and label drift now hard-fails (FamilyIdentityMismatch, tests/family_identity.rs:1601) instead of silently corrupting — but the schema-rust-next follow-up must be tracked or the §4 deliverable quietly evaporates.
- replace_memory_graph does a read-then-decide assert/mutate dance (mind/src/tables.rs:222-231) because the engine has no upsert/replace verb. Safe today (MindTables is single-actor-serialized) but the existence check belongs inside the engine; the special case should dissolve into an engine verb before more consumers copy the pattern.
- Engine::guard_storage_layout stamps STORAGE_LAYOUT=2 into the store before the catalog decode is validated (sema-engine/src/engine.rs:55-77, 1211-1242): a layout-1 store with catalog registrations but no commits (counters absent) gets mutated by an open that then fails with StorageLayoutMismatch from the RkyvDecode arm. Outcome is still a correct hard-fail on every open, but a failed open should not write to the store it rejects — probe the catalog (or include CATALOG in has_engine_history) before stamping.
- replay_versioned covers only domain-keyed families: VersionedReplay takes TableReference, so identified families (IdentifiedTableDescriptor, RecordIdentifier counters) have no replay path, and IDENTIFIED_COUNTERS would not be rebuilt by a fold (sema-engine/src/versioning.rs:446, engine.rs:1128-1183). Fine for Stage 1 (mind is all domain-keyed) and Stage 2's engine-owned import explicitly supersedes assert-based replay, but Spirit — the first backup target — must be checked for identified tables before Stage 2.
- A tombstone payload under Assert/Mutate during replay is reported as Error::VersionedPayloadDecode with the string message 'operation payload is a tombstone' (engine.rs:1185-1199, error.rs VersionedPayloadDecode). That is a distinct condition wearing a decode error's clothes; a dedicated variant would keep the error enum honest.
- Two of the three new storage_boundary tests are source-text greps (tests/storage_boundary.rs:1925-1967: asserting src/engine.rs does not contain 'pub fn storage_kernel' etc.). Consistent with the repo's weird-truth idiom and backed by one real behavioral test plus the type-level witness (StorageReader has no write method, lib.rs no longer re-exports WriteTransaction), but the greps are dodgeable (e.g. '-> &mut sema::Sema' would not match '-> &sema::Sema') — treat them as pins, not proof.
- Cargo.lock drift: the mind branch advances the nota-next/nota-next-derive git pin (af6a2080 -> 065fa2ad) as a side effect of the build — an unrelated dependency bump riding a feature branch. Harmless if intentional; worth a one-line acknowledgment or revert at integration.
- FamilyIdentity stores table_name as String while the registration API speaks TableName (&'static str Copy) — the dual representation forces Engine::family_registration_state (engine.rs:1244-1270) to re-implement Catalog's private find-by-table-name instead of going through Catalog::family_identity. A small structural tension worth dissolving when TableName grows an owned form.

## disciplineFindings
- Free functions: none introduced by either branch. sema-engine src/ scan is clean (every new fn is on Engine, Catalog, FamilyIdentity, StoreSchemaHash, StorageReader, VersionedReplay, ReplayReceipt, or a From impl). The free fn supervision_synthetic_exchange at mind/src/supervision.rs:28 in the branch worktree PREDATES the branch (exists at parent 7e29a4f4) and main's tip b9cd8c23 already fixed it — it disappears on the required rebase (verified in the scratch integration). Pre-existing debt not from this branch: free fn exchange() at mind/src/actors/choreography.rs:336, present on main too.
- No ZST namespace types: StorageReader carries &sema::Sema (engine.rs:1544); FamilyRegistration is a private two-variant outcome enum that dissolves the registered-or-new branch cleanly; FamilyIdentity/FamilyName/StoreSchemaHash are data-bearing.
- Naming: every new identifier is a full English word (FamilyName, SchemaHash, StoreSchemaHash, FamilyIdentity, VersionedReplay, ReplayReceipt, shares_family, family_descriptor); no ancestry repetition (FamilyIdentity.family, not familyName-inside-Family); StoreSchemaHash's prefix is descriptive (store-level vs per-family), not a namespace echo. The handoff's suggested 'stable_family_id' was correctly renamed to FamilyName, avoiding the forbidden 'id'. Pre-existing contract field signal_mind::Thought.id is not this branch's doing.
- Errors: typed thiserror variants only (StorageLayoutMismatch, FamilyIdentityMismatch, FamilyAlreadyBound, VersionedPayloadDecode, ReplayMissingKey, ReplayUnsupportedOperation at sema-engine/src/error.rs); zero anyhow in either crate; conversions via From (impl From<&Catalog> for StoreSchemaHash at versioning.rs:128, impl From<TableName> for String at table.rs).
- Design constraints verified in code: (1) typed FamilyIdentity replaces the stringly selector — VersionedLogOperation.family: FamilyIdentity replaces table_name: String (versioning.rs:157, 307-330), replay dispatches on shares_family (family+schema_hash, table excluded; versioning.rs:187, engine.rs:1128); (2) derived store hash replaces the hand label — VersioningPolicy lost schema_hash entirely, StoreSchemaHash is domain-separated blake3 over the sorted (family, hash) inventory excluding table names (versioning.rs:120-145), digest domain bumped to ...-entry-v2; (3) storage_kernel narrowed — pub fn storage_kernel deleted, read-only StorageReader with no write affordance (engine.rs:1112, 1544-1560), lib.rs no longer re-exports Sema-as-StorageKernel or WriteTransaction; (4) mind memory graph (plus thought/relation subscriptions) are registered engine families written through engine verbs, no storage-kernel writes remain in mind (tables.rs:157-231, 339, 369); (5) clean break — sema-engine 0.2.3->0.3.0, mind 0.2.0->0.3.0, MIND_SCHEMA_VERSION 7->8, engine STORAGE_LAYOUT=2 hard-fails pre-family stores with a typed error, no compatibility shims and none presented as virtue.
- INTENT.md updates quote only real Spirit records: I looked up fosp, iir4, x0ja, 29pb, j487 via the spirit CLI — all five exist and the bracket-quoted text is verbatim (fosp Correction on sema-engine exclusivity; iir4 Decision on log-as-truth; x0ja blake3 constraint; 29pb/j487 reusable-library and no-state-loss constraints). No invented intent.
- Beauty: shares_family naming the replay dispatch relation, the FamilyRegistration outcome enum, and the StorageReader-as-type-witness are genuinely good shapes. The honest doc comments distinguishing 'family identity' from 'current table coordinate' carry the design's one essential idea consistently across catalog, log, and replay.

## testHonesty
Yes — I re-ran everything myself. sema-engine worktree: cargo test reproduces the claim exactly, 67 passed / 0 failed across the 8 named suites (dependency_boundary 8, engine 22, family_identity 7, operation_log 7, seam_gap_falsification 6, signal_frame_seam 5, storage_boundary 3, subscriptions 9; lib unit and doc-tests 0). mind worktree: 65 passed / 0 failed exactly as claimed (lib 5, actor_topology 16, cli 6, daemon_wire 11 including mind_memory_graph_survives_process_restart, memory 7, orchestrate_caller 3, weird_actor_truth 17). Beyond the claim, I scratch-rebased the mind branch onto main's tip b9cd8c23 in /tmp/review/mind-integration (conflict-free) and re-ran: 65/65 green on the integrated result, proving the stale base is safely recoverable. The new tests mostly prove real witnesses: family_identity.rs exercises replay dispatch across families (applied=4/skipped=1), table-rename replay into the current coordinate, derived-store-hash invariance under rename, conflicting-identity rejection, double-binding rejection, and a hand-crafted legacy layout-1 store hard-failing with StorageLayoutMismatch{stored:1,expected:2}. The mind restart tests now exercise the engine-family path end-to-end because the implementation moved beneath them. The flattering exceptions: two of three storage_boundary tests assert on source text rather than behavior (repo idiom, but pins not proof), and the catalog-decode legacy path (layout-1 store with registrations but no counters) is reasoned-about in code yet untested.

