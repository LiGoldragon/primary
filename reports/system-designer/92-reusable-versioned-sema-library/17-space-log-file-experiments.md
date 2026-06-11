# Design space: same-file vs separate-file log — the experiment matrix

## Frame

The psyche wants the durable-state version-control library tested as runnable experiments, not chosen on paper. The single axis this report maps is **where the authoritative, payload-bearing, hash-linked commit log physically lives** relative to the redb materialized view. Everything else in the design direction (payload envelope, schema-transition entries, durability levels, checkpoints, digests-beside-cursors) is held *constant* across the experiments; we vary only the storage substrate of the log so that the substrate's properties can be measured in isolation.

This report deliberately does **not** decide. It enumerates three log-location options, gives each one an honest atomicity / recovery / read-after-write / shippability / throughput / replay / complexity account, and specifies what a concept-branch experiment would fork and instrument to compare them. Audit 208's "keep one transaction first, split last" (`reports/system-operator/208-...md:93-108`, `:190-208`) is the grounding sequence, and the kernel inversion remains the sema/sema-engine owners' call — undecided.

### What is constant across all three experiments

So the comparison is clean, every option assumes the same already-directed shape:

- The log is **payload-bearing** (today `CommitLogOperation` is metadata-only — `operation + table_name + key`, no payload, `sema-engine/src/log.rs:63-68` — and cannot rebuild state).
- Each entry carries the **typed replay envelope**: op kind, table identifier, record key, schema-hash decoder selector, payload, tombstone, optional prior value, entry digest, prev digest + sequence (per audit 208 `:110-132`).
- **`CommitSequence` stays the ordered cursor**; digests sit beside it, never replacing the monotonic markers (`sema-engine/src/snapshot.rs:19,35-38`; audit 208 `:45-69`).
- The redb tables are demoted to a **rebuildable materialized view**; the experiment harness must be able to delete and rebuild them from the log.
- One redb file per component; no shared sema daemon; the server/mirror is the only shared infrastructure (the library is linked code, not a process).

### Ground truth for the substrate

- sema's write helper is `Sema::write(|txn| ...)`: one `database.begin_write()` then `txn.commit()` on `Ok`, rollback-on-`Err` (`sema/src/lib.rs:568-573`). redb 4.x (`sema/Cargo.toml:11`) is a single-file mmap copy-on-write B+tree, single-writer ACID.
- **Durability is redb's default (no `set_durability` call anywhere in sema/sema-engine)** — i.e. `Durability::Immediate`, fsync-on-commit. This is the floor every option inherits or must reproduce.
- The engine writes the log entry and the data row **in the same redb transaction**: `assertion.table().sema_table().insert(transaction, ...)` and `COMMIT_LOG.insert(transaction, ...)` are both inside one `with_write` closure (`sema-engine/src/engine.rs:121-126`). That single transaction is the free atomicity Option A keeps and Options B/C must re-earn.
- The only first-party content hash today is criome's blake3 `ObjectDigest` (`signal-criome/src/lib.rs:55-57`) and spirit's hand-rolled `state_digest` blake3 fold over `(identifier, archived bytes)` (`spirit/src/store.rs:902-929`). Sema itself is sequence-addressed (`SnapshotIdentifier(u64)`, `snapshot.rs:19`).

## Option A — payload log as a redb table *inside* the component's single `.sema` file

Status-quo location (`COMMIT_LOG` table, `engine.rs:32`) plus payload plus hash-linking. The log table and the data tables share one redb file and are written in one transaction.

### Atomicity story
Free and total. The log entry and the materialized view mutate in the **same** `begin_write`/`commit` (`engine.rs:121-126`). redb's single-writer ACID guarantees the pair commit or neither does. There is no window where the log records a write the view never applied, or vice versa — the invariant audit 208 calls out at `:99-104` ("the log entry and visible state cannot diverge") is structural, costing zero engineering.

### Crash recovery
Inherited from redb: on reopen, redb's copy-on-write root pointer is either the pre-commit or post-commit tree; a torn write reverts to the last committed root. Because log and view are in that same tree, recovery is consistent for both with no replay step required. The log is a *redundant* on-disk copy of what the view already reflects, so post-crash the two agree by construction.

### Read-after-write semantics
Strongest possible, and matches today's `Engine` contract (audit 208 `:156-170`): after `commit()` returns, the written record is in the very `Database` view that `read()` and subscriptions use. No lag, no watermark, no catch-up. This is the property audit 208 says is "probably not acceptable" to weaken for the core component-local engine.

### Shippability / backup unit
Weakest. The authoritative bytes are interleaved with view bytes in the B+tree's page structure; the log is *logically* shippable (replay `commit_log_range` / an entry-stream API and upload typed entries — audit 208 `:101-104`) but is **not byte-shippable** as a contiguous artifact. Backup means "iterate entries since the peer's last head, encode, send" — a logical export, not a file-suffix copy. Redb has no online-snapshot path in use, so a whole-file backup needs a quiesced writer or a copied file.

### Write throughput / amplification
Highest amplification of the three. Every commit writes the payload **twice** into the same B+tree (once as the view row, once as the log entry value) and pays copy-on-write page churn plus a fresh fsync for both. The log table's keyspace is monotonic (`commit_sequence.value()` as `u64` key), so its inserts are append-at-the-right-edge of a B-tree — cheap relative to random keys, but still B-tree page splits and root rewrites, not raw append. One fsync per commit covers both writes (the single-transaction win), so latency is one fsync, but bytes-on-disk per commit roughly doubles for the payload.

### Replay cost
Cheap to *exercise* (the experiment's whole point): open the `.sema`, scan `COMMIT_LOG` by ascending sequence, decode each entry by its schema-hash selector, apply into a fresh set of view tables. Replay reads sequentially from one file. Cost scales with total retained entries until checkpoints land.

### Complexity
Lowest. No new file lifecycle, no second fsync ordering, no follower watermark, no cross-file recovery state machine. The only new code is the envelope type + hash-linking + the rebuild-from-log path. This is why audit 208 says start here (`:93-104`, `:190-195`).

### What the experiment measures (Option A baseline)
- Commit latency (p50/p99) and bytes-written-per-commit, with payload duplication on.
- `.sema` file growth rate vs. data-only growth (the amplification tax).
- Rebuild-from-log wall time and correctness: delete view tables, replay, assert the rebuilt view's digest equals the pre-delete digest (reuse the spirit `state_digest` fold shape, `store.rs:902-929`).
- Crash-injection (kill -9 mid-commit, then reopen): confirm log/view never diverge across N trials.

## Option B — payload log as a *second* redb file

The authoritative log is its own redb database (its own file); the view `.sema` becomes a disposable, independently-rebuildable redb file. Two files, two transactions.

### Atomicity story
Lost across files, and this is the defining cost. redb gives single-file ACID; it does **not** give a two-file commit. A crash between "commit log file" and "commit view file" leaves them at different heads. The design must pick an ordering — **log first, view second** — so the log is authoritative and the view is the follower (audit 208 `:157-170`). That demands a **WAL-follower watermark**: a durable "view has applied through sequence N" marker (stored in the view file's own meta) so recovery knows which log suffix to re-apply.

### Crash recovery
A real state machine now. On reopen: read the view's applied-watermark, read the log's head sequence; if `log_head > view_watermark`, replay the log suffix into the view and advance the watermark. Each file is internally ACID (redb), so neither is torn, but the *pair* needs reconciliation every open. The window where view lags log is bounded by one commit's worth of replay.

### Read-after-write semantics
Now a *policy choice*, which is exactly what makes B interesting to test. Two sub-variants:
- **B-sync**: the commit call appends to the log, fsyncs, *then* applies to the view and advances the watermark before returning. Preserves read-after-write (matches A's contract) at the cost of two fsyncs per commit and a wider critical section.
- **B-async**: the commit returns after the log fsync; the view applies on a follower path. Read-after-write is **broken** — a caller can see success then fail to read its own write until catch-up (audit 208 `:163-165` flags this as probably unacceptable for the core engine, acceptable for a mirror).

### Shippability / backup unit
Strong for the *log* file specifically. The log file is the authoritative artifact and can be shipped as a unit (still redb pages, so not a raw byte-suffix — but a clean, isolated file whose only content is the history). The view file is genuinely disposable: deletable and rebuildable from the log, so it never needs backup. This cleanly separates "the thing we protect" from "the cache."

### Write throughput / amplification
Two fsyncs per commit in B-sync (log file, then view file), which is the dominant latency cost — fsync is the expensive syscall and we now pay it twice on the critical path. Payload is still written twice (log value + view row) but into two B-trees, so neither tree's churn pollutes the other (the log file stays append-heavy/monotonic; the view file stays keyed by record key). B-async amortizes the view fsync off the critical path, trading the read-after-write guarantee for ~A-like commit latency.

### Replay cost
Same logical cost as A (scan log by sequence, decode, apply), but now replay is a *first-class operational path* run on every crash recovery, not just an experiment. The rebuild-the-view operation is also the disaster-recovery operation, which is a maturity win — the recovery path is exercised constantly.

### Complexity
Substantial step up from A: two file lifecycles, fsync ordering discipline, the follower watermark, the recovery reconciliation, and a decision about whether the engine handle owns one or two redb `Database` objects. This is audit 208's Stage 4 territory (`:206-208`), explicitly *after* the envelope/digest/checkpoint/replay tests are stable.

### What the experiment measures (B vs A)
- Commit latency delta from the second fsync (B-sync) — isolate fsync count as the variable.
- Recovery time after crash: replay-suffix length vs. wall time, across forced crashes at varying log/view skew.
- Correctness under crash *between the two file commits* (the atomicity hole): N trials of kill-between-fsyncs, assert the watermark+replay always converges the view to the log head.
- Backup-unit cleanliness: ship only the log file to a stub server, rebuild the full component state on the server side, compare digests.
- B-sync vs B-async A/B on the read-after-write probe: write then immediately read in a tight loop, count stale reads.

## Option C — bespoke *append-frame* log file (no redb for the log)

The authoritative log is a custom append-only file of length-prefixed, digest-linked frames (one frame = one envelope). The view stays a redb file, rebuilt from the frame log. This is the possible end state audit 208 names at `:206-208`.

### Atomicity story
Per-frame atomicity is hand-built, not borrowed from redb. A frame is durable when its bytes + a trailing frame-checksum are fully written and fsynced; a partially-written tail frame is detected by length/checksum mismatch and truncated on recovery (standard WAL framing). Cross-artifact atomicity with the view is the same WAL-follower problem as B: log-frame first, view second, with a watermark. The difference from B is that the *log side* is a trivially-recoverable byte file rather than a B-tree.

### Crash recovery
Two-part. (1) Log self-recovery: scan from the last checkpoint offset, validate each frame's checksum and prev-digest link, truncate at the first bad/short frame — the canonical append-log recovery, very fast and very well understood. (2) View catch-up: replay frames past the view watermark, same as B. No B-tree fsck because the log isn't a B-tree.

### Read-after-write semantics
Same policy fork as B (sync applies-to-view-before-return vs. async follower). The frame log doesn't change the read-after-write question; it changes the *cost* of the durable-append half of it — an append + fsync to a flat file is cheaper than a B-tree insert + fsync.

### Shippability / backup unit
Best of the three, and the reason C exists. The frame file is **byte-shippable as a suffix**: backup = copy bytes from the peer's last-acked offset to current head, append on the server. No logical iteration, no B-tree page extraction, no decode/re-encode — a `sendfile`-shaped tail copy (audit 208's "ship the log suffix" taken literally). The server appends frames it has validated by prev-digest continuity. This is the cheapest possible mirror.

### Write throughput / amplification
Lowest amplification on the log side: a frame append is a sequential write at EOF with no page splits, no copy-on-write tree rewrite, no root-pointer churn — just bytes + fsync. Payload is still written twice overall (frame + view row), but the frame write is near-optimal. In sync mode it's frame-fsync + view-fsync (two fsyncs); the frame fsync is cheaper than B's log-file-redb fsync. The write-amplification win is real and measurable.

### Replay cost
Sequential frame scan is the *fastest* replay substrate (linear read, no tree traversal), and it's the same operation as crash recovery and as server-side ingest validation — one code path serves three needs. Checkpoints (audit 208 `:172-188`) bound the scan length; the checkpoint offset is a literal byte offset into the frame file, which is simpler than a redb-keyed checkpoint.

### Complexity
Highest *upfront* — we are writing a durable file format by hand, which collides with two hard constraints: **no hand-rolled parsers** (the frame framing must be a typed encode/decode, not ad-hoc byte slicing) and **every fn is a method on a data-bearing type** (the frame writer/reader must own a real noun — e.g. `FrameLog` owning the file handle + head offset + head digest — not a free `write_frame()`). Format versioning, corruption handling, fsync-barrier discipline, and pruning/compaction of the flat file are all bespoke. This is why it is explicitly the *last* stage: do it only after A/B prove the envelope and protocol (audit 208 `:206-208`).

### What the experiment measures (C vs A and B)
- Append + fsync latency of a flat frame vs. redb log-table insert + fsync (isolate the substrate cost at equal payloads).
- Byte-suffix backup: instrument bytes-shipped-per-commit and server-append latency; compare to B's file-ship and A's logical-iterate export.
- Recovery: torn-tail-frame injection (truncate mid-frame, write garbage tail) and confirm checksum-truncate recovers cleanly; measure scan-from-checkpoint time.
- Compaction behavior: prune a prefix, confirm a peer asking from a pruned head is correctly redirected to a checkpoint boundary (audit 208 `:179-188`).
- The "no hand-rolled parser" cost: how much of the frame format can be a typed envelope encode/decode vs. how much genuinely needs framing bytes — a constraint-fit signal, not just a perf number.

## Cross-option comparison

| Dimension | A: log table in `.sema` | B: second redb file | C: append-frame file |
|---|---|---|---|
| Atomicity log↔view | Free, total (one txn) | Lost; needs watermark | Lost; needs watermark |
| Crash recovery | Inherited from redb, no replay | Replay suffix to watermark | Frame-truncate + replay |
| Read-after-write | Strongest (no lag) | Policy: sync keeps / async breaks | Policy: sync keeps / async breaks |
| Backup unit | Logical entry export | Isolated log *file* | Byte *suffix* (best) |
| fsyncs / commit (sync) | 1 | 2 | 2 (cheaper frame fsync) |
| Write amplification | Highest (2× into one B-tree) | 2× into two B-trees | Lowest log side (append) |
| Replay substrate | B-tree scan | B-tree scan | Linear frame scan (fastest) |
| New complexity | Lowest | Two-file state machine | Bespoke format (highest) |
| Audit 208 stage | Stage 1 — start here | Stage 4 | Stage 4 end state |

The controlled variables that the matrix isolates: **fsync count per commit** (1 vs 2), **log substrate** (B-tree vs flat append), and **view coupling** (same-txn vs follower-watermark). The shared, held-constant payload envelope means any throughput/recovery/backup delta is attributable to the substrate, not the encoding.

## How to run these as concept-branch experiments

Fork one concept branch per option off a common base that already has the payload envelope + digest-linking + rebuild-from-log path landed in `sema-engine` (the held-constant baseline = Option A minus the experiment instrumentation). Then:

- **Branch A** (`exp/log-same-file`): instrument the existing `engine.rs` commit path; add the rebuild-from-log test and crash-injection harness.
- **Branch B** (`exp/log-second-redb`): add a second `sema::Sema` handle for the log, move `COMMIT_LOG` into it, add the view watermark + recovery reconciliation, and a feature gate for sync vs async view-apply.
- **Branch C** (`exp/log-append-frame`): add a `FrameLog` data-bearing type owning the append file + head offset + head digest (typed encode/decode, no hand-rolled parser; methods on the noun, no free fns), wire the view as a follower, reuse B's watermark.

Instrument all three behind one common benchmark + crash harness so the numbers are directly comparable: a fixed workload (N asserts/mutates/retracts at a fixed payload-size distribution, plus one synthetic schema transition), measuring commit latency, bytes-on-disk, recovery time, replay time, and bytes-shipped-per-backup. The crash harness (`kill -9` at instrumented fsync barriers) feeds the correctness assertions: log↔view never diverge (A by construction; B/C via watermark convergence), and rebuilt-view digest equals pre-crash digest.

Decision inputs the experiments produce (the report stops here; the sema/sema-engine owners decide): whether the second-fsync latency of B/C is tolerable for the component-local write path; whether C's byte-suffix backup win justifies its bespoke-format and constraint-fit cost; and whether any component actually needs the async-view (lagging) mode at all, or whether read-after-write must hold everywhere.
