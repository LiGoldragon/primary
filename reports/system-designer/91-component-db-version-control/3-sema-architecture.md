## Scope and method

Read actual source under `/git/github.com/LiGoldragon/{sema,signal-sema,sema-engine}` plus the first real consumer `spirit` (which is where migration and backup actually live — the engine has neither). Verified the live store on disk at `~/.local/state/spirit/`. All file:line citations below are from the read source.

## 1. On-disk format

**Physical store: one redb file per component.** `sema::Sema` wraps a single `redb::Database` opened at one path (`sema/src/lib.rs:471-508`, `Database::create(path)`). redb 4.1.0 (confirmed in both `Cargo.lock`s) is a single-file, mmap'd, copy-on-write B-tree. The live file `~/.local/state/spirit/spirit.sema` begins with the ASCII magic `redb\032\n...` — confirmed it is a bare redb file, not a directory. Every `*.sema` in the spirit dir carries the `redb` magic.

**Values are rkyv archives; keys are redb-native.** `Table<K, V>` (`sema/src/lib.rs:231-462`) stores values as `&[u8]` of `rkyv::to_bytes(value)` (`insert`, line 381-388) and decodes with `rkyv::from_bytes` + bytecheck validation (`decode_value`, line 456-461). rkyv feature pinning is fixed across the workspace: `little_endian`, `pointer_width_32`, `unaligned`, `bytecheck` (all three Cargo.toml + `DatabaseHeader::current()` `sema/src/lib.rs:120-128`).

**Tables / keyspaces.** Tables are created lazily on first write — NOT declared in a schema (`Schema` carries only a version; `sema/src/lib.rs:180-204`, comment at 161-179). A redb table is keyed by `(name, K, V)`. The kernel reserves two internal tables (`sema/src/lib.rs:466-469`): `__sema_meta` (holds `schema_version: u64`) and `__sema_headers` (holds the rkyv `DatabaseHeader`). `sema-engine` adds its own internal tables (`engine.rs:26-36`): `__sema_engine_catalog` (registered table names), `__sema_engine_counters` (`latest_commit_sequence`, `latest_snapshot`, `next_subscription`), `__sema_engine_commit_log` (keyed by `u64` commit sequence), `__sema_engine_subscriptions`, `__sema_engine_identified_counters`. A component's record families are ordinary tables — spirit registers `records` and `referents` (`store.rs:41-42, 265-266`).

**Live store on disk** (`ls -la ~/.local/state/spirit/`):

| File | Size | Note |
|---|---|---|
| `spirit.sema` | 1,241,088 | live store (mod Jun 11 14:02) |
| `spirit.schema-old-backup-3.sema` | 1,224,704 | migration backup |
| `spirit.schema-old-backup-{0,1,2}.sema` | ~1.21M each | older migration backups |
| `spirit.schema-1-backup-0.sema` | 1,253,376 | older-naming backup |
| `spirit.sock`, `meta-spirit.sock` | 0 | daemon sockets |

## 2. Operation model — current-state, destructive

`signal-sema` is a payloadless classification vocabulary only — six labels `Assert/Mutate/Retract/Match/Subscribe/Validate` (`operation.rs:19-32`) classified into `Write/Read/Stream/Validation` (`class()`, line 67-74). It carries no executable payload and no storage logic.

The engine semantics (`sema-engine/src/engine.rs`):
- **Assert** — insert at key, REJECTS if key exists (`assert_keyed` line 294-363, dup-check at 308-319). Destructive in the sense it occupies the key thereafter.
- **Mutate** — `sema_table().insert(...)` overwriting the existing value (`mutate_keyed` line 383-452). The OLD record bytes are gone — redb last-writer-wins, no prior version retained.
- **Retract** — `sema_table().remove(...)` (`retract` line 454-523). Row is deleted; no tombstone row, no prior bytes kept.
- **Match / Validate** — read-only over current rows (`match_records` line 681-758; `validate` line 842-861).

**There is no accretive/Datomic fact log of values.** The store is a mutable current-state snapshot. Spirit confirms this at the consumer level: `change_certainty`, `bump_importance`, `change_record`, `clarify` all do `mutate(...)` overwriting the single `records` row (`store.rs:583-672`). Spirit retains prior states only by manually copying into a SEPARATE archive `*.sema` database before overwriting (`clarify` archives then mutates, `store.rs:649-672`; `ArchiveDatabase`, `store.rs:1013-1039`) — application-level, not a kernel facility.

## 3. Operation log — metadata only, NOT replayable

`sema-engine` keeps a commit log table `__sema_engine_commit_log` keyed by `u64` commit sequence. A `CommitLogEntry` (`log.rs:14-61`) holds `commit_sequence`, `snapshot`, and a `NonEmpty<CommitLogOperation>`. **A `CommitLogOperation` is `{ operation: SemaOperation, table_name: String, key: Option<RecordKey> }` (`log.rs:63-90`) — the record VALUE/bytes are NOT stored.** Every write path builds the entry from key + operation only (e.g. `assert_keyed` `engine.rs:324-332`; `commit` `engine.rs:568-622`).

Consequences:
- `commit_log()`, `replay_from_sequence()`, `commit_log_range()` (`engine.rs:892-918`) return only this metadata. "Replay" cannot reconstruct state — there are no values to replay. The `operation_log.rs` test confirms entries carry only operation+table+key (`tests/operation_log.rs:75-78, 154-160`).
- The log is durable (written in the same redb write txn as the data, e.g. `engine.rs:333-347`) and survives reopen (`tests/operation_log.rs:82-129`).
- **"Snapshot identity" is NOT a content hash.** `SnapshotIdentifier(u64)` (`snapshot.rs:5-56`) is a monotonic counter: `next_snapshot()` = `latest_snapshot().next()` (`engine.rs:970-972`); `CommitSequence(u64)` likewise (`sequence.rs`). The engine `DatabaseMarker` is just `(commit_sequence, snapshot)` counters (`snapshot.rs:21-77`).
- **The only real content hash lives in spirit, not the engine.** Spirit defines its OWN `DatabaseMarker { commit_sequence, state_digest }` and computes `state_digest` as blake3 over `(commit_sequence, each record's identifier + rkyv bytes, each referent)` truncated to a `u64` (`spirit/src/store.rs:714-758`). This is recomputed on demand from current rows, not persisted, and is spirit-specific.

## 4. Atomicity today

- **Single-writer ACID via redb.** `Sema::write` opens one `begin_write()`, runs the closure, `commit()`s on Ok, drops (rolls back) on Err (`sema/src/lib.rs:568-573`). The rollback-on-error path is tested (`tests/kernel.rs:379-399`). redb is single-writer / MVCC-readers; commit is durable with fsync by default (redb default `Durability::Immediate`).
- **Multi-op atomicity is structural.** `Engine::commit(CommitRequest)` writes all operations + the log entry + counters inside ONE redb write txn (`engine.rs:635-661`), so a batch is all-or-nothing; a rejected op advances nothing (`tests/operation_log.rs:163-181`).
- **No savepoints / persistent snapshots / custom durability are used.** Grep for `savepoint|set_durability|Durability|compact|fsync|two_phase` across sema + sema-engine + spirit src returns NOTHING. So today there is NO mechanism for a backup tool to take a consistent point-in-time snapshot while the daemon holds the file open — redb 4.x does support `Savepoint`/persistent savepoints and the on-disk format is crash-consistent, but the stack does not expose or use them. A live online backup would need either (a) redb savepoint support added at the kernel, or (b) coordinating with the single-writer daemon to quiesce + copy.

## 5. Resume on restart

There is no separate "load state" step — resume is implicit in reopening the redb file. `Engine::open` (`engine.rs:45-58`) calls `Sema::open_with_schema` then reads `__sema_engine_catalog` to rebuild the in-memory `Catalog`. The counters (`latest_commit_sequence`, `latest_snapshot`, `next_subscription`, per-table `next_record_identifier`) are read live from redb on each call (`current_commit_sequence`/`latest_snapshot` `engine.rs:863-881`), so they "resume" simply because they were committed. The daemon path: `Store::open` → `Engine::open` (`spirit/src/store.rs:261-276`), invoked at daemon boot (`spirit/src/daemon.rs:119,124`). Spirit's `RecordIdentifierMint` re-derives used identifiers by scanning current rows (`store.rs:848-850, 915-948`) rather than trusting a counter. In-memory subscriptions are persisted as registrations (`SUBSCRIPTIONS` table, `engine.rs:1087-1103`) but the live `Arc<dyn SubscriptionSink>` callbacks are NOT restored on reopen (the registry starts empty, `engine.rs:56`).

## 6. Migration — full rewrite into new rkyv types, old file renamed aside

The two-submodule `historical`/`current_shape`/From-chain pattern is implemented in spirit (`spirit/src/production_migration.rs`), NOT in the engine/kernel. The kernel only HARD-FAILS on version skew: `ensure_schema_version` returns `SchemaVersionMismatch` when the stored `u64` differs from expected (`sema/src/lib.rs:527-552`; tested `kernel.rs:159-175`), and refuses to retro-stamp an unversioned legacy file (`LegacyFileLacksSchema`, tested `kernel.rs:177-199`).

How spirit migrates (`production_migration.rs`):
1. Spirit's current schema is `SchemaVersion::new(7)` (`store.rs:40`). Each historical version has its OWN rkyv struct frozen in the file: `SpiritStoreV1Record`/`V1Entry` … `V6Record`/`V6Entry`, plus `ProductionStoredRecord`/`ProductionStampedEntry` (`production_migration.rs:110-230`). These are the "mod historical reproducing old rkyv types."
2. `SpiritStoreUpgrade::run` opens the live store at the current version; on `SchemaVersionMismatch{found ∈ v1..v6}` it dispatches to `upgrade_previous_store` (`production_migration.rs:316-343`).
3. It opens the file AT THE OLD VERSION with the old rkyv type (e.g. `SpiritStoreV5Database::open` passes `SchemaVersion::new(5)`, `production_migration.rs:472-487`), reads ALL rows, and maps each old `Entry` to the current `Entry` via per-version `into_new_entry()` (the From-chain; `production_migration.rs:658-728`).
4. It writes every record into a FRESH temp store at the current version (`production_migration.rs:371-379`), then `fs::rename(live → backup_path)` and `fs::rename(temp → live)` (`production_migration.rs:380-388`). `backup_path` is `*.schema-old-backup-{N}.sema` with the first free N (`production_migration.rs:394-403`).

**The whole store is rewritten into the new types; the old bytes survive only in the renamed-aside backup file.** This is the version-control crux: each schema version is a genuinely DIFFERENT set of rkyv types (V1Entry has `categories`+`magnitude`; V2 splits into `certainty`+`importance`; V4 adds `weight`; V5 changes `LegacyTextCategories`→`LegacyCategories`; V6 drops `weight`; current `Entry` adds `referents` and uses `Domains`). A generic byte-level VCS over the redb file cannot understand records across a schema bump — diffs would be total. Verified on disk: the live dir holds `spirit.schema-old-backup-{0..3}.sema` exactly matching this naming, all redb files.

## 7. Existing backup

There is NO general backup mechanism — only migration's rename-aside (§6) and two consumer-level features in spirit, none of which is a point-in-time backup of the live store:

- **`~/.local/state/persona-spirit-backups/`** is hand-made historical persona-spirit (the LEGACY pre-Sema `.redb` store) snapshots from May, organized by version (`v0.1.0`…`v0.3.0`) plus dated copies like `persona-spirit.redb.v0.2.0.production-cutover-20260525235707`. These were created by the operator/migration tooling for the legacy `persona-spirit.redb` format, not the current `spirit.sema` store. They are stale (newest content Jun 6) and pre-date the Sema cutover.
- **Spirit's "archive" is not a backup** — `collect_removal_candidates`/`retire`/`clarify`/`supersede` copy individual records into a SEPARATE `*.archive.sema` database before removing/overwriting them in the live log (`store.rs:343-408, 564-698`, `ArchiveDatabase` 1013-1039). It is a retention bin for retired records, application-driven, not a snapshot of the whole store.
- **Migration backups** (`spirit.schema-old-backup-N.sema`) are the closest thing to a whole-store backup, but they only appear as a side effect of a schema upgrade, never on a schedule or per-commit.

Net: no atomic server backup and no per-commit/scheduled whole-store snapshot exists today.

## Implications for version control + atomic backup (design inputs)

- The engine is a current-state store with a metadata-only log. Version control is NOT "already half-built": to reconstruct prior states you must add an ACCRETIVE log that carries record payloads (e.g. log the old+new rkyv bytes or a value-bearing fact stream), since today only `(operation, table, key)` is logged.
- A real content-addressed snapshot identity does not exist at the engine layer; `SnapshotIdentifier` is a counter. Spirit's blake3 `state_digest` is the only content hash and is recomputed, not stored. A VCS-grade state hash would be a new engine facility.
- redb is single-writer with fsync-on-commit; the file is crash-consistent, but no savepoint/online-snapshot path is wired up. Atomic backup needs either redb savepoint support exposed at the kernel, or a quiesce-and-copy protocol with the daemon (which holds the single write lock).
- Schema migration rewrites the entire store into new rkyv types and renames the old file aside. Any VCS must be schema-version-aware: a commit's bytes are only meaningful under their schema version's type set, and a bump produces a wholly new byte image (expected under the no-backward-compat doctrine).
