# Ground: spirit (poster-child) and repository-ledger — what a VC library would absorb

## Why spirit is the poster-child

Spirit is a production `sema-engine` consumer that, lacking any version-control library, has hand-rolled **four separate version/history mechanisms** on top of the kernel — each a candidate for a reusable VC layer to absorb. It opens its live `*.sema` with `Store::open` at `SchemaVersion::new(8)` (`store.rs:47`, `store.rs:270-285`), registers two tables (`records`, `referents`), and drives all writes through `sema-engine`'s six verbs (`assert`/`mutate`/`retract`/`match_records`). It owns nothing about durability ordering — that is the kernel's monotonic commit sequence (`store.rs:898-900`, `self.database.current_commit_sequence()`). Everything *else* about "what changed, what it used to be, can I recover it" spirit built by hand.

The central finding: **spirit re-implements, in spirit-domain types, exactly the four primitives a generic VC library would own** — schema-versioned historical decode, content digest of state, retained prior values, and an append-only operation journal — while keeping genuinely Spirit-domain logic (intent semantics, supersession lifecycle, base36 keys) that no VC library should touch.

## Mechanism 1 — Historical readers `SpiritStoreV1..V7` (the migration chain)

Lives in `src/production_migration.rs`. Spirit freezes one full record-type set per past schema version: `SpiritStoreV1Record`/`Entry` (`:133-145`) through `SpiritStoreV7Record`/`Entry` (`:214-228`), plus a yet-older `ProductionStoredRecord`/`ProductionStampedEntry` (`:120-130`) at `PRODUCTION_SCHEMA_VERSION = 5`. Each version is a separate `rkyv::Archive` struct with its own `EngineRecord` impl, opened by its own `SpiritStoreVNDatabase` at its own pinned `SchemaVersion` (`:1029-1128`). Because rkyv archives are byte-fragile, **the only way to read an old file is to declare the old type and ask the kernel to open at the old schema number.**

The migration mechanics (`SpiritStoreUpgrade::run`, `:919-995`):
1. Try `Store::open` at the current version; if it returns `SchemaVersionMismatch { expected: 8, found }` for any known prior (1-7), dispatch to `upgrade_previous_store` (`:949-995`).
2. Per-version `From`-style reducers convert old → current `Entry` (`SpiritStoreV1Entry::into_new_entry` ... `V7`, `:1305-1389`); these encode real domain knowledge — V1 has no `importance` so it defaults `Magnitude::Minimum` (`:1312`); V4/V5 drop a `LegacyWeight` field (`:1335`, `:1350`); V7 re-parses a frozen 24-variant `Domain` enum through NOTA text into the current domain tree (`store_version_seven`, `:258-833`, `Craft::Programming` → `(Technology (Software (Languages ProgrammingLanguages)))`).
3. **The migration is a full rewrite plus `fs::rename` aside** (`:978-989`): open a fresh temp `*.sema`, `import_record` every reduced record, `fs::rename` the old file to `schema-old-backup-N.sema`, `fs::rename` the temp over the original. No in-place schema transition; the prior file survives only as a manual filesystem backup.

This is the single richest target for the VC library. The frozen-type-per-version pattern, the `found`-version dispatch, the per-version reducer, and the rewrite-and-rename are precisely the "`SchemaTransition(v_old_hash -> v_new_hash, reducer)` + post-migration checkpoint" shape the design direction proposes. **What the library absorbs:** the open-at-old-version plumbing, the dispatch-on-found-version, the temp+rename atomic swap, the backup retention. **What stays spirit-domain:** the reducer bodies themselves (`into_new_entry`) — they carry irreducible meaning (what a missing `importance` should default to, how a retired `Craft::Schema` maps into the new tree). A generic library can *invoke* a typed reducer; it cannot *write* one.

## Mechanism 2 — the blake3 `state_digest` (content addressing, layered by hand)

`Store::state_digest` (`store.rs:908-933`) folds a blake3 hash over `commit_sequence.to_le_bytes()` then, per record, `record_identifier.as_bytes()` + the record's rkyv archive bytes, then per referent likewise; it truncates the 32-byte digest to the leading 8 bytes as a `u64` (`:930-932`). Empty store digests to zero (`:911`). This `u64` rides in spirit's own schema-level `DatabaseMarker { commit_sequence, state_digest }` (`signal.rs:455-458`) on every receipt.

Critical ground-truth correction: **the digest is a spirit-level invention, not a kernel feature.** `sema-engine`'s own `DatabaseMarker` (`snapshot.rs:35-38`) carries `commit_sequence + SnapshotIdentifier(u64)` — both monotonic counters, *no content hash*; `SnapshotIdentifier` is sequence-addressed (`snapshot.rs:19`, `.next()` at `:53`). So the only first-party content hash in the whole spirit/sema stack is this one (matching the ground-truth claim that criome's `ObjectDigest` is the only other one). Spirit recomputes it on demand by scanning all records — O(n) per marker, no incremental maintenance.

**What the library absorbs:** content-addressing as a first-class kernel/engine concern. A VC layer that hash-links log entries (the "entry digest + prev digest" envelope) makes spirit's hand-folded full-scan digest redundant — the head digest *is* the state identity, maintained incrementally per commit instead of recomputed per query. **What stays spirit-domain:** nothing here is domain-specific; this mechanism is fully absorbable and is arguably the clearest "stop hand-rolling" win.

## Mechanism 3 — the separate `*.archive.sema` (retained prior values, by hand)

Spirit keeps a SECOND `sema-engine` database, opened on demand, for superseded/retired/clarified records. `ArchiveDatabase` (`store.rs:1270-1296`) is a distinct handle over a distinct file (`<stem>.archive.sema` by default, or an owner-configured `ArchiveDatabaseTarget::Path`, `store.rs:336-350`). Before any lossy mutation, spirit copies the current `Entry` into the archive under a versioned key `"<identifier>-<commit_sequence>"` (`archive_identifier`, `store.rs:457-462`) so repeated clarifications of one identifier preserve every prior state:
- `clarify` archives then mutates the description (`store.rs:824-847`).
- `retire` archives then retracts (`store.rs:739-756`).
- `supersede` archives every retired identifier, retracts them, asserts the replacement (`store.rs:849-873`).
- `collect_removal_candidates` archives then retracts matched records (`store.rs:405-448`).

This is hand-rolled **prior-value retention** — the "optional prior value" field of the proposed typed replay envelope, and the "retired/superseded suffix" a payload-bearing log would carry natively. Today it is a second file with no atomic tie to the live file: the archive `assert` and the live `retract` are in **separate transactions on separate databases**, so a crash between them can archive-without-removing or (worse ordering) lose the live record without an archive copy — a durability seam the in-same-transaction commit log explicitly closes.

**What the library absorbs:** prior-value capture and retired-record retention become log history, not a sidecar file — the log *is* the archive, and atomicity is free because history and view commit together. **What stays spirit-domain:** *which* operations are lossy and *what* the archive key means (the supersession/clarification/retirement vocabulary) — the library stores prior values; spirit decides when a write supersedes.

## Mechanism 4 — the `*.guardian.sema` append-only journal (a second hand-rolled log)

`guardian_journal.rs` keeps a THIRD `sema-engine` database (`<stem>.guardian.sema`, `store.rs:352-359`) as an append-only decision log: `GuardianJournal::append` (`:205`) asserts a `GuardianJournalEntry` keyed by `current_commit_sequence + 1` (`:222-225`) — a hand-rolled monotonic append. This is a second event log spirit built because the kernel's commit log (Mechanism 0 below) is metadata-only and not consumable as a domain event stream.

**What the library absorbs:** the "I need a durable append-only domain-event journal alongside my materialized view" pattern — exactly what a payload-bearing authoritative log provides once. **What stays spirit-domain:** the guardian decision vocabulary (`GuardianDecision`, `GuardianOperation`).

## Mechanism 0 — the kernel commit log spirit does NOT consume

`sema-engine`'s `CommitLogEntry { commit_sequence, snapshot, NonEmpty<CommitLogOperation> }` (`log.rs:15-19`) with `CommitLogOperation { operation, table_name, key }` (`log.rs:63-68`) is **metadata-only — no payload, not replayable.** Spirit therefore *cannot* use it as its history substrate, which is precisely why it built Mechanisms 1-4. This is the seed the design direction proposes to generalise (make it payload-bearing/hash-linked/authoritative). The four hand-rolled mechanisms are direct evidence of the gap: every one of them exists because the log carries no payload and no content identity.

## repository-ledger — the already-event-shaped precedent

`repository-ledger` stores `StoredEvent { sequence: EventSequence, ... }` keyed by a zero-padded sequence string (`format!("{:020}", ...)`, `lib.rs:154`) and appends via `record_hook_notification` → `next_event_sequence` + `assert` (`lib.rs:512-524`, `:790-795`). Its records ARE events; queries filter `event.sequence > since_sequence` (`lib.rs:630-639`) — a native log-suffix read. Durability into the store is atomic per assert, but ingest from Gitolite hooks uses a separate filesystem atomic spool: temp-write, then `fs::rename` into `processed/` after the store commit (`spool.rs:40-75`).

**What it would need:** very little — it is already log-shaped and sequence-addressed, so a payload-bearing authoritative log is its natural home; it would gain hash-linking, checkpoint identity, and server mirror of the suffix essentially for free. **What it would NOT need:** the historical-reader migration chain (it has had no schema churn of stored events yet) or a separate archive file (its events are immutable by nature — no clarification/supersession lifecycle). It is the clean case; spirit is the hard case.

## The boundary table — absorbable vs spirit-domain

| spirit-local mechanism | location | VC library absorbs? | what stays spirit-domain |
|---|---|---|---|
| `SpiritStoreV1..V7` frozen types | `production_migration.rs:133-228` | Plumbing yes (open-at-old, dispatch, swap) | The `into_new_entry` reducer bodies |
| Full-rewrite + `fs::rename` migration | `production_migration.rs:949-1010` | Yes — typed `SchemaTransition` + checkpoint | When a migration is triggered |
| blake3 `state_digest` (truncated u64) | `store.rs:908-933` | Yes — entirely; becomes hash-linked log head | Nothing (fully absorbable) |
| spirit `DatabaseMarker{seq,digest}` | `signal.rs:455-458` | Partly — `commit_sequence` stays the ordered cursor; digest moves into the log | The receipt shape on the wire |
| `*.archive.sema` prior-value store | `store.rs:1270-1296`, `405-873` | Yes — prior values become log history (atomic, one file) | Which ops are lossy; archive-key meaning |
| `*.guardian.sema` append journal | `guardian_journal.rs:192-225` | Yes — generic durable event journal | Guardian decision vocabulary |
| base36 `RecordIdentifierMint` | `store.rs:1023-1025`, `1172-1260` | No — production-stable key minting is domain | Entire mechanism |
| supersession/clarification/retire lifecycle | `store.rs:739-873` | No — intent semantics | Entire mechanism |
| query predicate matching | `store.rs:1320-1525` | No — Spirit SEMA semantics | Entire mechanism |

## The central tension, seen through spirit

Spirit's `StoredRecord { record_identifier: String, entry: Entry }` (`store.rs:76-80`) is a *concrete typed* record, and its migration reducers are *concrete typed* conversions — there is no stringly-typed generic-record store anywhere. Yet the migration machinery IS generic over "a sequence of frozen schema versions, each with a reducer to the next." The library must capture that genericity (over `(version_hash, ArchivedType, Reducer)` triples) **without** forcing spirit to surrender the concrete `Entry` type or to route reducers through stringly-typed metadata. The frozen-type-per-version pattern at `production_migration.rs:133-228` is the live demonstration that the generic axis is *the schema-version dimension*, not the record-payload dimension — a VC library generic over schema transitions can stay perfectly specific about each version's type. That is the seam to design against.

