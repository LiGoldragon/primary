# Prior art: WAL/log shipping and replication to a server

## Scope and frame

The brief's design direction — "version the LOG, not the store; demote the redb tables to a rebuildable materialized view; ship the log suffix since the peer's last head to ouranos" — is the canonical shape of WAL-shipping / log-replication systems. This report maps the precedents that already do exactly this and extracts the load-bearing mechanics: how each defines durability and ack/RPO levels, how each makes shipping atomic and idempotent, how each handles schema/format evolution, and — critically for Spirit j487 — whether each is packaged as a reusable generic library or a monolithic service, and by what genericity mechanism.

A single distinction organises everything below. There are two precedent families:

1. **Page/block shippers** (Litestream, LiteFS, Postgres WAL archiving + WAL-G/pgBackRest). They replicate the *physical byte deltas* of the storage engine. They are schema-agnostic precisely because they never look at rows — they ship pages. This makes their durability/atomicity machinery directly reusable, but their "schema evolution story" is *not applicable* to us: a page shipper does not know what a schema is, whereas our log is *typed* and a schema transition is a first-class log entry.
2. **Command/consensus log shippers** (rqlite, dqlite, etcd/Raft, openraft). They replicate a *logical operation log* and replay it into a deterministic state machine. This is structurally our model ("version the log, payload-bearing, replay into a materialized view"). openraft in particular is the closest genericity precedent for the j487 reusable-library mandate.

Our system sits at an unusual intersection: a logical, typed, payload-bearing op log (family 2 in shape), shipped asynchronously to a single backup ingest target with no online-failover quorum (family 1 in deployment), over rkyv zero-copy archives that are byte-fragile across schema change (a constraint neither family has, because pages don't care and JSON/SQL commands self-describe).

## Litestream — physical WAL frames to object storage

### What it is and core model
A standalone sidecar process that continuously copies SQLite WAL pages to one or more replicas (S3/GCS/Azure/B2/NATS). It is a pure backup/restore + (newly) read-replica tool, not a clustering layer — there is no failover, no second writer. ([litestream.io/how-it-works](https://litestream.io/how-it-works/))

### How it makes state durable on a server
It holds a long-running read transaction to prevent SQLite from checkpointing the WAL out from under it, copies new WAL pages into a "shadow WAL" staging directory (`00000000.wal`, `00000001.wal`, …), and streams those increments to object storage. Restore = fetch the snapshot plus all subsequent WAL frames and replay. ([litestream.io/how-it-works](https://litestream.io/how-it-works/))

### Durability / ack / RPO
**Asynchronous.** The old default sync interval was 1 second, giving a worst-case data-loss window of roughly the last second of writes if the host dies before the next push. There is no synchronous-commit / RPO=0 mode — Litestream explicitly trades a small RPO for operational simplicity. v0.5 (Oct 2025) reframes recovery as point-in-time over the LTX hierarchy rather than a fixed sync tick. ([fly.io/blog/litestream-v050-is-here](https://fly.io/blog/litestream-v050-is-here/), [simonwillison.net/2025/Oct/3/litestream](https://simonwillison.net/2025/Oct/3/litestream/))

### Atomicity / idempotency of shipping
WAL frames are written under monotonically incrementing names; a "generation" (pre-v0.5: a 16-char random hex id) bounds a contiguous restorable run. Any break in WAL continuity forces a *new generation* with a fresh snapshot, so a partial/torn suffix never corrupts a restore — the restorer only ever follows one contiguous chain. v0.5 **removed generations** in favour of a single monotonically incrementing TXID plus the LTX format. ([litestream.io/how-it-works](https://litestream.io/how-it-works/), [fly.io/blog/litestream-v050-is-here](https://fly.io/blog/litestream-v050-is-here/))

### Schema evolution story
**None — and that is the point.** Litestream ships pages, so a SQLite `ALTER TABLE` is just more WAL pages; it has zero schema awareness. *This is exactly the property we cannot have:* our archives are byte-fragile rkyv and a schema change is a different type set, not "more pages."

### Compaction (the LTX hierarchy — directly relevant to our checkpoint protocol)
v0.5 introduced LTX (Litestream Transaction) files: ordered, sorted-page, checksummed transaction files that compact into a level hierarchy — **L1 = a 30-second window, L2 = a 5-minute window, L3 = a 1-hour window** — so a restore touches "a dozen or so files on average" instead of replaying every frame. ([fly.io/blog/litestream-v050-is-here](https://fly.io/blog/litestream-v050-is-here/), [deepwiki.com/benbjohnson/litestream](https://deepwiki.com/benbjohnson/litestream/2.3-data-structures))

### Packaging
**Monolithic sidecar process**, not a library. Genericity = none; it works for any SQLite DB because it operates below the schema at the page layer.

## LiteFS — physical transactions via a FUSE passthrough, with leader election

### What it is and core model
A FUSE passthrough filesystem that intercepts SQLite's file writes, detects transaction boundaries, and records each transaction as an LTX file for shipping to replicas across a cluster. Unlike Litestream it is a *replication/clustering* layer with a single elected primary. ([github.com/superfly/litefs/docs/ARCHITECTURE.md](https://github.com/superfly/litefs/blob/main/docs/ARCHITECTURE.md), [fly.io/docs/litefs/how-it-works](https://fly.io/docs/litefs/how-it-works/))

### How it ships state and detects divergence (the part we should study)
Each LTX file carries an **autoincrementing TXID** plus a **rolling checksum of the entire database**. The checksum is built by XOR-ing per-page CRC64(page-number ‖ page-data) into a running value — XOR being associative/commutative lets it be maintained incrementally and verified against a whole file. A replica connects and announces its position as `(TXID, rolling-checksum)`; the primary streams transactions forward from there, or — if that position is no longer available — resends a full snapshot then resumes streaming. Split-brain is caught when two nodes reach the **same TXID with different rolling checksums**; the stale node re-snapshots from the new primary. ([github.com/superfly/litefs/docs/ARCHITECTURE.md](https://github.com/superfly/litefs/blob/main/docs/ARCHITECTURE.md))

### Leader election / durability / RPO
Leadership is a **Consul session lease** with a TTL the primary renews; clean shutdown destroys the lease (instant handover), unclean death waits out the TTL. Replication is **asynchronous** — "transactions are only durable on the primary node and have not been replicated to a replica" — so a catastrophic primary loss drops in-flight unreplicated transactions. RPO is bounded by replication latency (typically subsecond, unbounded during partitions). Synchronous replication was on the roadmap, not shipped. ([github.com/superfly/litefs/docs/ARCHITECTURE.md](https://github.com/superfly/litefs/blob/main/docs/ARCHITECTURE.md), [fly.io/docs/litefs/faq](https://fly.io/docs/litefs/faq/))

### Schema evolution / packaging
Page-level, schema-blind, same as Litestream. Packaging is a **monolithic FUSE daemon**, not a library; genericity = page layer.

## PostgreSQL WAL archiving + WAL-G / pgBackRest — the atomic-idempotent shipping contract

### Core model
Postgres writes every change to a 16 MB WAL segment before touching data files; a base backup plus the continuous WAL segment stream replays to any point in time (PITR). ([postgresql.org/docs/current/continuous-archiving](https://www.postgresql.org/docs/current/continuous-archiving.html))

### The archive-command contract (the single most reusable idea here)
`archive_command` MUST:
- **refuse to overwrite** any pre-existing archive file (write-once), and
- return **zero only when the segment is durably persisted**; nonzero makes Postgres retry the same segment indefinitely.
Crucially, Postgres **may re-invoke archiving for an already-archived segment** (e.g. after a crash), so the command must be idempotent: if a file already exists with *identical* bytes, succeed; if it exists with *different* bytes, fail loudly. The documented safe form is `test ! -f dest/%f && cp %p dest/%f`. ([postgresql.org/docs/current/continuous-archiving](https://www.postgresql.org/docs/current/continuous-archiving.html))

This is precisely the discipline our "ship the log suffix to ouranos" needs: an entry at sequence N either lands byte-identical or is rejected; re-sending an already-acked suffix is a safe no-op.

### Timelines (the divergence-after-recovery mechanism — maps to our digest chain)
When recovery completes, Postgres forks a **new timeline**; the timeline ID is embedded in WAL filenames and a "timeline history" file records the branch point, so a recovered branch never overwrites the WAL of the abandoned history and PITR can target *any* prior state including abandoned branches. ([postgresql.org/docs/current/continuous-archiving](https://www.postgresql.org/docs/current/continuous-archiving.html))

### Durability / RPO levels
Async archiving's RPO is bounded by `archive_timeout` (segments only ship when full, so the timer forces a switch — "a minute or so is usually reasonable") **plus** the unarchived WAL still in `pg_wal/`. Synchronous streaming replication is the RPO=0 alternative at higher I/O cost. This is the explicit named-RPO ladder the brief wants per-store. ([postgresql.org/docs/current/continuous-archiving](https://www.postgresql.org/docs/current/continuous-archiving.html))

### WAL-G / pgBackRest
Both are the production tooling layer: base backups (full/incremental/delta), parallel compression, encryption, retention, S3/GCS/Azure/SSH targets, restore orchestration. WAL-G uses delta backups and parallel upload; pgBackRest adds backup verification and repository management. They are **monolithic tools/services**, not libraries you link. ([wal-g.readthedocs.io/PostgreSQL](https://wal-g.readthedocs.io/PostgreSQL/), [pgbackrest.org/user-guide](https://pgbackrest.org/user-guide.html))

### Schema evolution
Physical WAL is schema-blind (DDL is just more WAL). PITR replay across a `pg_dump`/restore (logical) boundary is a different story Postgres does *not* solve at the WAL layer — again the gap our typed `SchemaTransition` log entry must fill that none of these page shippers address.

## rqlite & dqlite — command/WAL logs over Raft

### rqlite
A **standalone service**: a full (simple) RDBMS exposing an HTTP API, replicating the **SQL command** to a Raft quorum. Consensus is intrinsic — a write needs quorum agreement (two parallel round-trips leader→quorum) before it is accepted; **Queued Writes** explicitly trade durability for throughput by acking before quorum. Read consistency is a tunable ladder (`strong` / `weak` / `none`/auto, plus linearizable). Raft **snapshotting** periodically compacts the log (a few ms, needs exclusive DB access) and truncates replayed entries. ([rqlite.io/docs/faq](https://rqlite.io/docs/faq/), [onidel.com/blog/sqlite-replication-vps-2025](https://onidel.com/blog/sqlite-replication-vps-2025))

### dqlite
Canonical's **C library** (the closest "reusable" framing in the SQLite family): an embeddable distributed SQLite engine with its own C-Raft, shipping **WAL frames** (not commands) to the quorum, embeddable in any language that can call C. Used by LXD/Incus/MicroK8s. The library-vs-service split is the headline: *dqlite is a library you integrate; rqlite is an application you run.* ([dqlite.io](http://dqlite.io/), [packtpub … dqlite-1-0](https://www.packtpub.com/en-us/learning/tech-news/lxd-releases-dqlite-1-0-a-c-library-to-implement-an-embeddable-persistent-sql-database-engine-with-raft-consensus))

### Applicability
The consistency/durability **ladder** (strong→weak→queued) is the precedent for the brief's per-store ack policy (local-committed / queued-for-mirror / server-committed). But both buy that with a synchronous quorum we explicitly do not have — ouranos is a single async ingest target, not a voting member. The Raft *log truncation after snapshot* is the precedent for our checkpoint + retained-suffix policy.

## Raft as a generic library — etcd & openraft (the j487 genericity precedent)

### etcd / hashicorp-raft
etcd's raft is a widely-reused Go library, but its genericity is *byte-level*: the application hands Raft opaque `[]byte` proposals and implements `apply`. That is exactly the "opaque blob" the psyche rejected in Spirit 29pb — Raft orders and replicates bytes, the application alone knows their type. Useful as a *negative* example: log-shipping generality is trivially achieved by going stringly/bytes-typed, which our perfect-specificity discipline forbids.

### openraft — the one to study closely
openraft makes the whole engine generic over a **single `RaftTypeConfig` trait** carrying associated types: `D` (application request/command data), `R` (response), `NodeId`, `Node`, `Entry` (the log-entry type, implementing `RaftEntry`), `SnapshotData`, `AsyncRuntime`, `Responder`. The `declare_raft_types!` macro fills it in. Storage is three traits the application implements — **`RaftLogStorage`** (append/read/truncate log), **`RaftStateMachine`** (apply committed entries; install snapshots), **`RaftSnapshotBuilder`** (build a snapshot from current state). Snapshots: as of v0.9 the `generic-snapshot-data` feature lets `SnapshotData` be an arbitrary application type instead of forcing `AsyncRead + AsyncWrite`. ([docs.rs/openraft/raft/struct.Raft](https://docs.rs/openraft/latest/openraft/raft/struct.Raft.html), [docs.rs/openraft/storage](https://docs.rs/openraft/latest/openraft/storage/index.html), [docs.rs/openraft/getting_started](https://docs.rs/openraft/latest/openraft/docs/getting_started/index.html), [docs.rs/openraft/upgrade_08_09](https://docs.rs/openraft/latest/openraft/docs/upgrade_guide/upgrade_08_09/index.html))

This is the direct answer to the central tension in the brief — *generic over arbitrary record families WITHOUT a stringly-typed generic-record store.* openraft is generic over the application's command type `D` and entry type `Entry` **by associated type**, so the application's `D` is its own real, specific enum-of-operations (the documented default is `String`, but `D` is meant to be the app's typed command/enum, and `Entry` is a concrete app type implementing `RaftEntry`). The library never inspects `D` — it orders and persists it via traits the app implements. The owning-noun discipline maps cleanly: `RaftLogStorage`/`RaftStateMachine`/`RaftSnapshotBuilder` are traits the data-bearing storage type implements, not free functions; `RaftTypeConfig` is the parameterisation seam. **A Sema VC library could mirror this exactly: a `SemaStorageConfig`-style type-config trait + storage/state-machine/snapshot-builder traits, generic over a component's own typed op enum and entry type, never over a stringly `record_name`.**

The contrast worth holding: **CommitLogOperation today is the anti-pattern openraft avoids** — it carries `table_name: String` and is metadata-only (no payload, log.rs:63-68), i.e. stringly-typed and non-replayable. openraft's `Entry`/`D` are typed and replayable. Moving toward the openraft shape is exactly the brief's "payload-bearing, typed replay envelope, decoder-selected by schema-hash."

## The schema-evolution gap none of the precedents close

Every page shipper (Litestream/LiteFS/Postgres-WAL) is **schema-blind by construction** — they ship bytes/pages and a schema change is invisible. Every logical shipper (rqlite SQL commands, openraft `D`) replays into a **forward-compatible, self-describing or app-deterministic** target (SQL text; an app enum the current binary still understands). **Our situation is the hard one neither solves:** rkyv archives are byte-fragile, each schema version is a *different type set*, and a replayed historical entry must be decoded by *the type that was current when it was written* (hence the brief's per-entry schema-hash decoder selector and the `SchemaTransition(v_old_hash → v_new_hash, reducer)` + post-migration CHECKPOINT). Spirit already hand-rolls this gap manually: frozen historical readers `SpiritStoreV1..V7` (production_migration.rs:89-116) and a full-rewrite + `fs::rename`-aside migration, plus a blake3 `state_digest` over committed state (store.rs:894-915) and a `*.archive.sema` for retired records (store.rs:333-344). That hand-rolled machinery is the per-component reimplementation j487 says to absorb into the library — and the precedents confirm *the durability/atomicity layer is reusable, but the typed schema-transition layer is novel and ours to design.*

## Experiment matrix the psyche asked to test (same-file vs separate-file log)

The precedents bracket this cleanly and are worth stating as the framing (not a decision):

| | Same-file (log inside the component's one `.sema`) | Separate-file (log as its own artifact) |
|---|---|---|
| Atomicity of log↔view | **Free** — log and data commit in one redb txn; today's design (cannot diverge) | Requires a 2-file commit protocol or treating the view as a pure rebuild from the log |
| Precedent | redb single-file ACID; closest to "log is the source, view is a redb table beside it" | Postgres (data dir + separate WAL archive dir); Litestream shadow-WAL; LiteFS LTX dir |
| Shipping the suffix | Must extract the log table's suffix out of the live mmap'd file (no online-snapshot path in redb today — the noted gap) | Suffix is already a discrete, append-only, individually-shippable artifact (Postgres 16 MB segments; LTX files) — write-once + refuse-overwrite idempotency is trivial |
| Compaction/checkpoint | Compaction rewrites the one file; breaks naive suffix sync (the brief's checkpoint problem) | LTX-style level compaction (L1/L2/L3 windows) operates on separate files; restore touches few files |
| Read-after-write | Trivially satisfied (local view is the committed redb state) | Same, if local view stays authoritative and only the mirror lags |

The page shippers (separate-file, write-once segments) and the redb-native (same-file, free atomicity) sides are both first-party-validated precedents; the brief's instruction to test both is well-founded because the atomicity-vs-shippability tradeoff genuinely flips between them.

## Things this maps onto in our stack (orientation, not decisions)
- **Postgres archive-command contract** → our suffix-ship idempotency rule (entry N lands byte-identical or is rejected; re-ship is a no-op).
- **Postgres timelines** ↔ our prev-digest hash chain: both disambiguate divergent histories after a fork/recovery; a digest mismatch at equal sequence is our split-brain signal (mirrors LiteFS's equal-TXID-different-checksum test).
- **LiteFS rolling whole-DB checksum** ↔ our blake3 `state_digest` + post-checkpoint inventory; LiteFS proves an incrementally-maintainable whole-state checksum is practical for catching divergence.
- **rqlite/dqlite consistency ladder + Raft snapshot truncation** → our per-store ack policy (local-committed / queued-for-mirror / server-committed) and retained-suffix-after-checkpoint policy.
- **openraft `RaftTypeConfig` + storage/state-machine/snapshot-builder traits** → the concrete genericity blueprint for j487: typed `D`/`Entry` via associated types, never a stringly `table_name`.
- **Litestream LTX level compaction (30s/5m/1h windows)** → a model for checkpoint cadence and "restore touches a dozen files."

