# Prior art: Dolt, noms, and prolly trees

## Scope and verdict up front

Dolt is the canonical "Git for data" system and the obvious first reference for j487. The brief already flags the danger: reasoning by analogy from Dolt ("we want versioned state, Dolt versions state, therefore copy Dolt") is the named cargo-cult failure mode. This report goes under the analogy. It establishes exactly how Dolt's chunk store and commit DAG work, why that shape exists, and then separates the two things Dolt actually offers us — a *concrete storage mechanism* (prolly trees + content-addressed block store) and a *conceptual model* (Merkle-DAG of immutable commits, versioned-log-as-truth) — because only the second applies to us and the first is a trap.

The short version of the verdict, defended below: **Dolt's prolly tree solves a problem we do not have** (efficient diff/merge/structural-sharing over a large, randomly-mutable, sorted keyspace), and Dolt-the-engine is **not reusable as a generic versioning library** — it is welded to the SQL relational model through go-mysql-server. But Dolt's *commit DAG and content-addressed immutability* are a clean, battle-tested instance of the exact model our DESIGN DIRECTION already chose ("version the log, not the store"), and Dolt's hard lesson that **schema change forces a full table rewrite** is direct, load-bearing evidence for our `SchemaTransition`-as-typed-log-entry direction.

## The lineage: noms is the actual ancestor

Dolt is a re-implementation; the ideas are noms'. Attic Labs' noms (2015-2016, $8.1M raise, now archived) described itself as "the versioned, forkable, syncable database" and was explicitly "philosophically descendant from the Git version control system." Its core model is the one we should study, because it is the *general-purpose* version Dolt later specialized for SQL.

A noms database is "a single large Merkle DAG" with two responsibilities: "it provides storage of content-addressed chunks of data, and it keeps track of zero or more datasets." Everything else falls out of content-addressing:

- **Deduplication is free**: "If you commit the same data twice, it will be deduplicated because of content-addressing. If you commit almost the same data, only the part that is different will be written."
- **History is retained by default**: every prior version is reachable; any two versions are cheaply comparable; you can rewind or branch from any point.
- **Disconnected reconciliation**: "Instances of a single Noms database can be disconnected from each other for any amount of time, then later reconcile their changes efficiently and correctly."
- **Storage-substrate-agnostic**: "A Noms database can be implemented on top of any underlying storage system that provides key/value storage with at least optional optimistic concurrency" — noms shipped an S3 blockstore for exactly this.

This is the cleanest available statement of the *abstract* target: a content-addressed, append-only, server-syncable history where the store is a derived view of immutable chunks. That abstract target maps onto Spirit 29pb and j487. The *concrete* noms/Dolt realization — prolly trees over a chunk store — is where it stops mapping, and the reason is keyspace shape.

## Prolly trees: what they actually are and the problem they solve

A prolly tree ("probabilistic B-tree") is a search tree whose node boundaries are chosen by a *rolling hash over the content*, not by fixed fanout. Dolt's docs describe a six-step recursive build: sort the key-value map by key; walk the sorted keys computing a rolling hash; declare a chunk boundary wherever the hash hits a target pattern; content-address each chunk (strong hash of its bytes) into a block store; build the next level up by mapping each chunk's highest key to its content address; recurse to a single root.

Three properties matter, and all three are *consequences of content-defined chunking*:

### History independence

"No matter which order you insert, update, or delete values, the Prolly tree is the same." A given logical key-value set has exactly one tree shape regardless of operation order. This is what makes diff cheap: "if the hash of the root chunk is the same the entire subtree is the same," so a diff of two versions is `O(d)` in the size of the difference rather than `O(n)` in the dataset, and a structural-equality check is a single root-hash compare.

### Structural sharing across versions

Because identical chunks share one content address and are stored once, "storing multiple versions of the data only requires additional storage proportional to their diff." An edit touches roughly `chunk_size × tree_depth` bytes (Dolt targets ~4 KB average chunks), plus a small probability that a chunk boundary shifts.

### The Dolt-specific refinement over noms

Dolt's rolling hash "only considers keys," not values, so "any updates to values is guaranteed not to shift the chunk boundary" (it can lean on SQL's fixed-width column types). Dolt also folds a target-size CDF into the boundary test — `(CDF(end) - CDF(start)) / (1 - CDF(start))` — to get *normally*-distributed ~4 KB chunks, fixing noms' geometric distribution (many tiny chunks, few huge ones) and its read-amplification.

### The write cost, and why it is paid

Prolly trees are not free. Read performance equals a B-tree (`log_k(n)`), but writes pay `(1 + k/w)·log_k(n)` because probabilistic splitting can ripple. You pay that write tax *specifically to buy* cheap diff and structural sharing over a **large, sorted, randomly-mutable keyspace** — the SQL table. This is the crux of the brief's rejection: **we are not that shape.** Our state is Datomic-shaped — an append-only fact log where the authoritative artifact is the sequence of operations, not a mutable B-tree of current cells. Cheap diff over an arbitrary mutable keyspace is a problem we don't have, so the write tax buys us nothing. (DoltHub's own "People Keep Inventing Prolly Trees" notes the structure keeps getting independently rediscovered — bup, noms, Inria, DePaul — which says it is the *right* tool *for that specific job*; it does not say it is the right tool for an append-only fact log.)

## The on-disk chunk / block store: journal → table files → oldgen

This is the part most worth understanding concretely, because it is where Dolt's *durability and compaction* story lives — and compaction is precisely the thing our checkpoint protocol must handle.

**Chunk addressing.** "Every piece of information in a Dolt database is stored as Chunks." A chunk is a content-addressed compressed byte buffer; its address is "the SHA512 checksum of the byte buffer truncated to 20 bytes." Identical content → identical address → stored once. (Note this is *truncated SHA512*, a 160-bit address — comparable in width to git's SHA-1 but a different function. Our only first-party content hash today is criome's blake3 `ObjectDigest`; sema itself is sequence-addressed.)

**The chunk journal (the write path).** "All database writes are initially made to the chunk journal" — a single append-only file in the `noms/` directory, literally named `vvvv…` (the all-ones hash). A sidecar `journal.idx` accelerates lookups into it. The journal grows unbounded until GC. This is a write-ahead log of chunks; it is the durability floor and the crash-recovery anchor.

**Generational GC and oldgen.** Storage splits into newgen (`noms/`) and oldgen (`oldgen/`). "All chunks start in newgen." `dolt gc` walks chunks reachable from branch refs in the commit graph, discards unreferenced chunks from the journal, and packs the survivors into immutable **table files** (the NBS format) written into oldgen. The generational trick: chunks already in oldgen, and their children, are skipped on subsequent collections — so "running `dolt gc` again will be very fast" since it only processes the newgen delta. Dolt later added *online* GC and `dolt archive` for further compaction.

**Table files and the manifest.** A **table file** (NBS format) has three regions: a fixed-size **footer** (primarily the chunk count); an **index** (a prefix map of the first 8 bytes of each address, a lengths array, and the address suffixes); and the compressed **chunk records** (Snappy). Existence checks are a binary search over the prefix map (`O(log N)`); retrieval computes a byte offset from the lengths array. A **manifest** file is the "control center": it lists which table files are live and their chunk counts (e.g. `b1co…:132` = that file holds 132 chunks). The manifest is the atomic swap point — GC writes new table files, then flips the manifest.

**The git comparison, made precise.** This is *not* "like git" by hand-wave; it is structurally git's object model with different knobs:
- chunks ≈ git objects (content-addressed, immutable, dedup-by-hash);
- table files ≈ packfiles (many objects, compressed, indexed for `O(log N)` lookup);
- the journal ≈ a write-ahead loose-object staging area;
- `dolt gc` packing journal→oldgen ≈ `git gc` packing loose objects into packs;
- the manifest ≈ refs + pack index, the mutable pointer set over an immutable store.
The *difference* from git: the leaves under a Dolt commit are not file blobs but **prolly-tree nodes over sorted row tuples**, and the commit DAG points at root chunks of those trees. Git content-addresses *files*; Dolt content-addresses *B-tree-shaped row storage*.

## The commit DAG, branches, and remotes

A Dolt commit is a node in a Merkle DAG; `repo_state.json` holds git-like state (current HEAD branch, remotes, tracking). Branches differ in both schema *and* data — "different branches can have different schemas." Merge runs over the prolly trees and can raise *data* conflicts or *schema* conflicts (the latter surfaced in `dolt_schema_conflicts`, blocking the merge).

**Remotes / replication.** Dolt clone/fetch/push/pull mirror git semantics over "a chunk-based storage layer that separates metadata operations from bulk data transfer." Push performs a merge against the remote branch and ships the changed chunks + schema. Remotes can be DoltHub, a filesystem, S3/GCS, or SSH ("Dolt runs its transfer command on the remote host over the SSH connection"). Recently Dolt can even push *into a git remote*: it "stores its remote data under a custom ref path, `refs/dolt/data`," pointing at a git commit whose tree carries the Dolt table files and manifest as git blobs — i.e. git purely as a transport floor, exactly the Stage-1 role the brief permits and nothing more.

## Schema evolution: the most directly applicable lesson

Dolt's schema story is the single most load-bearing piece of prior art for our `SchemaTransition` direction, because Dolt confronted the same physics we have and the answer was unavoidable: **a schema change that alters the row encoding forces a full table rewrite.**

Why: Dolt encodes a row as a serialized tuple — field bytes plus offset metadata — and history-independence *requires* that "schema changes always make the storage for the table look exactly like it would have if the target schema was in place and all the rows of the table were then inserted." So when the encoding changes, every tuple is incompatible and must be re-encoded; no structural sharing survives.

The boundary between "free" and "full rewrite" is instructive:
- **Sharing-preserving** (encoding-neutral): column *rename*; adding a *nullable* column *at the end* (trailing nulls aren't stored); same-width fixed-type changes (SMALLINT → SMALLINT UNSIGNED); CHAR/VARCHAR equivalence; charset changes (stored UTF-8 internally); ENUM *expansion* (ordinals appended); DECIMAL precision *increase* (variable-width).
- **Full rewrite**: primary-key change; column drop; non-nullable column add; column add *with default*; most type conversions; nullable column inserted *mid-tuple*; column reorder.

Read that list against our rkyv reality. Our archives are *more* fragile than Dolt's tuples — the brief states "any field add/remove/reorder changes byte layout; no silent backward compatibility," and the fixed feature pinning (`pointer_width_32`/`unaligned`/`bytecheck`) means even the "free" Dolt cases (append nullable at end, widen a fixed field) are *not* free for us. **For rkyv, essentially every schema change is a full-rewrite event.** This is hard, independent confirmation that our direction is correct: a schema migration cannot be modeled as a cell/byte diff against the prior store; it must be a *first-class typed log entry* (`SchemaTransition(v_old_hash → v_new_hash, reducer)` + checkpoint), because each schema version is a *different rkyv type set* and the old bytes are simply not decodable under the new types. Dolt reached the "rewrite the whole table" conclusion with a *more forgiving* encoding than ours; we should expect to live there permanently.

## Is Dolt-the-engine a reusable library? (the j487 question)

This is where Dolt most clearly *does not* serve as a model. Dolt is packaged two ways, and neither exposes a generic versioning library:

1. **`go-mysql-server`** — the query engine — *is* described as "storage engine agnostic," so other projects can "write their own storage engine plugins." But agnostic here means *agnostic over storage backends behind a SQL/relational interface*; it is generic in the wrong axis for us. The genericity is a storage-plugin trait beneath a fixed relational query model, not a generic-over-record-types versioning kernel.
2. **The embedded `dolthub/driver`** — "a `database/sql` compatible driver for embedding Dolt inside a Go application … akin to SQLite, without running a Dolt server process." Its entire API surface is SQL: you `sql.Open("dolt", DSN)`, run queries, and reach version control through *SQL system tables* (`dolt_log`, `dolt_branches`) and SQL functions (`dolt_commit()`, `dolt_merge()`). There is **no exposed API for the prolly tree, the chunk store, or the commit DAG as reusable generic types.** The docs explicitly warn: "If you use Dolt internals as an API, it can, and likely will, break."

Two further reuse facts sharpen this. First, Doltgres (Postgres-compatible) had to be built as a *separate product*, not a config of Dolt — strong evidence the versioning core is not cleanly separable from the SQL dialect layer. Second, the noms dependency itself was *un-modularized*: the Dolt team forked noms, then "their code became so intertwined that managing Noms as a dependency became messy so they included Noms code directly in the Dolt repository." The most general-purpose version-controlled-DB library in this lineage (noms) was *vendored into a monolith* precisely because the clean library boundary didn't hold up. That is the cautionary tale for j487: the reusable-library boundary is the hard part, and the one team that tried hardest abandoned it.

For our discipline this maps cleanly: a Dolt-style "generic over arbitrary record families via a stringly-typed relational schema and a SQL surface" is *exactly* the stringly-typed generic-record store our `skills/abstractions.md` forbids. Dolt gets away with it because SQL *is* its product; for us the type must carry meaning, which is the central design-space tension the brief names. Dolt does not show us how to resolve that tension — it shows us the resolution we're not allowed to take.

## Mapping onto our DESIGN DIRECTION and experiment matrix

- **"Version the log, not the store."** Dolt's commit DAG over an immutable chunk store *is* this principle, proven at scale: the manifest/refs are the only mutable pointers; everything reachable is immutable and content-addressed; the materialized state is derivable. Dolt validates the *model*. It does not validate the *mechanism* (prolly trees), which we reject for keyspace-shape reasons.
- **Digests beside the monotonic cursor.** Dolt addresses *chunks* by content hash but threads *commits* via a DAG whose traversal order is the parent edges, not a sortable key — the same separation our direction draws between content digests (identity/dedup) and `CommitSequence` (the ordered, range-queryable cursor). Dolt's `dolt gc` reachability walk is over DAG edges, not hash order, reinforcing that the digest answers identity and the sequence answers ordering.
- **Compaction breaks naive suffix sync — Dolt proves it.** Dolt's whole journal→oldgen GC machinery exists *because* you cannot indefinitely append. Their generational scheme (oldgen chunks + children skipped on re-GC) is the concrete answer to "how do you compact a content-addressed log cheaply." Our checkpoint protocol (covered range, schema-hash inventory, retained-suffix policy, pruned-head behaviour) is solving the same problem; Dolt's two-generation split + manifest-flip is a reference design for the *retained-suffix vs. checkpointed-head* boundary, even though our log payloads are typed entries, not chunks.
- **Backup = ship the log suffix.** Dolt push ships changed chunks since the remote's head over SSH/HTTP, separating metadata negotiation from bulk transfer. Our "ship the log suffix since the peer's last head to the server" is the same protocol family; the metadata/bulk split is worth copying at the protocol level (ouranos as the ingest target negotiates heads; the bulk suffix follows).
- **Same-file vs separate-file log (the experiment the psyche wants both ways).** Dolt is *unambiguously the separate-store witness*: the chunk store/journal is a distinct artifact from any single-file embedded DB, and that separation is what enables independent GC, table-file packing, and chunk-level remote transfer. Today's sema, by contrast, writes the commit log *inside the same redb transaction as the data* — buying free atomicity (log and view cannot diverge) at the cost of coupling compaction of the two. Dolt's architecture is concrete evidence for the *separate-file* arm: it shows what you gain (independent compaction, clean suffix shipping, content-addressed dedup) and what you must then build yourself (a manifest/atomic-swap discipline to keep the separate artifacts consistent — which redb-same-file gives us for free). The matrix should weigh: same-file = free atomicity, coupled compaction; separate-file = independent compaction + clean remote suffix transfer, but you re-earn atomicity via a manifest swap.

## Things our design must not copy from Dolt

- Do **not** adopt prolly trees / content-defined chunking. They optimize diff/merge over a randomly-mutable sorted keyspace; our log is append-only and our "diff" is just the new suffix. The write tax buys nothing.
- Do **not** treat git-as-substrate as more than a Stage-1 transport floor. Dolt's `refs/dolt/data` git-remote support is exactly that — table files as opaque blobs under a side ref — and double content-addressing (our digests inside git's) is the cargo-cult the brief rejects.
- Do **not** model genericity as "generic over relational schemas via SQL." That is the stringly-typed generic-record store we forbid; it is reusable *because* SQL is the product, which we are not.
- Do **not** assume the reusable-library boundary is easy. noms — the most general member of this family — was vendored into Dolt because the boundary didn't survive contact. j487's "build once, generic types/traits" is the hard part, and the prior art's lesson is that it failed in the one place it was attempted at this scale.

