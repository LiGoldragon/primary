# Prior art: git object model, libgit2/gitoxide, Mercurial revlog, Fossil

## Scope and how to read this

Four content-addressed / append-only version stores, each studied as a candidate *donor* of mechanism for the reusable Sema-VC library: git's object model (and the two embeddable libraries that expose it, libgit2 and gitoxide), Mercurial's revlog, and Fossil. For each: (1) core model, (2) durability/replication, (3) schema evolution, (4) library-genericity mechanism, (5) what worked, (6) what hurt, (7) what applies to us, (8) what does not. The throughline question the brief poses — *can a content store be generic over arbitrary payloads without degenerating into a stringly-typed blob bag, and can it be packaged as a reusable library* — is answered four different ways here, and the four answers bracket our design space cleanly.

Two of these systems are the closest analogues to our accepted direction ("version the LOG, not the store; demote redb tables to a rebuildable VIEW"): **Fossil** is almost exactly that shape (authoritative content-addressed artifact blobs + a rebuildable relational cache on top), and **Mercurial's revlog** is the canonical answer to "how do you store an append-only log of a payload efficiently with periodic checkpoints." Git/libgit2/gitoxide answer the *genericity-and-reuse* half of the brief: how a content-addressed store becomes a linkable library with a pluggable storage trait.

## Git object model

### Core model

Git is a content-addressed key-value store of four immutable object types: **blob** (file bytes, no name), **tree** (a directory listing mapping names+modes to blob/tree hashes), **commit** (a snapshot pointer to one tree plus parent commit hashes and metadata), and **tag**. Every object's key is the hash of `<type> <length>\0<content>`; identical content is stored exactly once (natural dedup). The commit DAG plus immutable objects is the entire data model — refs (branches/tags) are mutable pointers *outside* the object store, the only mutable surface ([git-scm Pro Git, Git Internals — Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects); [Git Object Hashing and Content Addressability](https://blogs.kenokivabe.com/article/git-object-hashing-and-content-addressability)).

Crucially git is a **snapshot** model, not a delta model at the logical level — each commit names a complete tree. Deltas are a *physical storage detail* of packfiles only.

### Durability / replication

Objects start as loose zlib-compressed files under `.git/objects/`; `git gc` repacks them into **packfiles** with delta compression (one object stored as a delta against a similar object, chained) plus a sorted `.idx` for O(log n) lookup ([gitperf Chapter 6: Loose Objects, Packfiles, Delta Compression](https://gitperf.com/chapter-06.html)). Replication = the smart transport "want/have" negotiation: peers exchange ref tips, compute the set of reachable objects the other lacks, and ship a packfile of exactly that closure. Because object names are content hashes, the diff is a pure set difference of reachable hashes — no per-object timestamps or vector clocks needed ([DEV: How git clone Really Works](https://dev.to/zopdev/how-git-clone-really-works-a-deep-dive-into-gits-object-database-24j7)).

### Schema evolution

Git's "schema" is fixed (four object types, a stable serialization). It does not evolve per-application — that is precisely why it works as a substrate but says nothing about *typed* schema migration. The only format migration git itself has faced is the SHA-1 → SHA-256 transition, which is a multi-year, interop-painful, dual-hash-mapping effort — direct evidence that changing the *hash basis* of a content-addressed store is expensive.

### Library genericity

The reference C implementation is not a library; the embeddable surface is **libgit2** and the pure-Rust **gitoxide** (below). The object model's reuse property is its *uniformity*: one (type, hash, bytes) triple covers everything. That uniformity is exactly the stringly-typed-blob shape our discipline forbids — git's "type" is a 4-value enum tag on opaque bytes.

## libgit2 and gitoxide (the embeddable libraries)

### libgit2 — pluggable backends via C callback structs

libgit2 is a cross-platform linkable C library exposing git's object model, with **custom backends** for ODB, refdb, and config. A backend is a struct of C function pointers (`git_odb_backend` with `read`/`write`/`exists`/`refresh` callbacks in `git2/sys/odb_backend.h`; `git_refdb_backend` in `git2/sys/refdb_backend.h`). You initialize a `git_odb`, attach a custom backend, and set it on the repository — letting objects live in SQLite, Redis, S3, memory, etc. instead of the filesystem ([libgit2/libgit2-backends](https://github.com/libgit2/libgit2-backends); [Perforce: Your Git Repository in a Database — Pluggable Backends in libgit2](https://www.perforce.com/blog/your-git-repository-database-pluggable-backends-libgit2); [git-scm Appendix B: Libgit2](https://git-scm.com/book/en/v2/Appendix-B:-Embedding-Git-in-your-Applications-Libgit2)). This is the **storage-trait-over-content-store** pattern in its most literal form: the *format* (objects, hashes, deltas) is fixed by the library; the *durable substrate* is swappable.

### gitoxide — a 50+ crate Rust workspace with trait-based ODB

gitoxide is a pure-Rust git implementation organized as a Cargo workspace of 40-50+ crates in four layers: foundation (`gix-hash` for object IDs / hash algos via `sha1`/`sha256` features, `gix-features` for parallelism/compression), domain (`gix-object` zero-copy parse+encode, `gix-odb` loose+pack object DB, `gix-pack` pack gen/consume), networking, and the `gix` facade that aggregates the plumbing behind a `Repository` hub while keeping every sub-crate independently usable ([gitoxide DeepWiki: Crate Organization](https://deepwiki.com/GitoxideLabs/gitoxide/1.3-crates-and-components); [GitoxideLabs/gitoxide](https://github.com/GitoxideLabs/gitoxide); [lib.rs/crates/gix-odb](https://lib.rs/crates/gix-odb)).

Its genericity mechanism is a deliberate three-part choice ([gitoxide DeepWiki](https://deepwiki.com/GitoxideLabs/gitoxide/1.3-crates-and-components)):

- **Traits for object access**: `gix-object` defines `Find`/`FindExt`/`Write`; `gix-odb` provides `Handle`/`OdbHandle` (thread-local and thread-safe variants) implementing them. Object access is generic over the backend behind these traits, and there is explicit design intent to put "everything behind traits" so databases can be *layered* (e.g. in-memory over a normal backend) and to reach WASM ([gix-odb docs](https://docs.rs/gix-odb/latest/gix_odb/); [GitoxideLabs/gitoxide discussion #1281 "custom storage/backends"](https://github.com/GitoxideLabs/gitoxide/discussions/1281); [discussion #302 "a new object database"](https://github.com/GitoxideLabs/gitoxide/discussions/302)).
- **Feature flags for cross-cutting config** (hash algorithm, async-vs-blocking transport) propagated by the facade across the whole stack — *not* trait abstraction for those axes.
- **Small composable crates** as the unit of reuse — a consumer depends on `gix-object` alone if that is all it needs.

This is the most directly relevant reuse precedent for j487: a content store packaged as a *layered set of small typed crates* with a facade, where the storage substrate is a trait and the cross-cutting knobs (hash choice) are features. It validates "build the mechanism once as generic types/traits."

### What worked / what hurt (libraries)

Worked: libgit2's callback-backend pattern made "git over arbitrary storage" real and widely deployed; gitoxide's crate layering lets consumers take exactly the layer they need and has measurably better performance/correctness than shelling out to git. Hurt: libgit2's C-callback genericity is unityped (void* + byte buffers) — no compile-time payload typing; gitoxide's trait surface is still evolving and the "everything behind a trait" goal is partly aspirational, and the 50-crate count is real coordination overhead.

## Mercurial revlog

### Core model

The **revlog** is Mercurial's one storage primitive, reused for all three versioned data kinds — **changelog**, **manifestlog**, **filelog** — *identical format, different payload meaning*, linked hierarchically (changelog entry → manifestlog entry → filelog entries) ([Nathan Goldbaum: Storing versioned data with revlogs](https://ngoldbaum.github.io/posts/revlog/); [Mercurial internals.revlogs help](https://wim.vree.org/wsgi/hgweb.wsgi/mscweb/help/internals.revlogs)). A revlog is an **append-only** structure of two parts: a fixed 64-byte-per-entry **index** (offset, compressed/uncompressed length, base rev, link rev, parent revs, and a per-revision content hash) and the **revision data** (each revision is either a full snapshot or a delta against an earlier revision) ([Gregory Szorc: The Mercurial Revlog](https://gregoryszorc.com/blog/2014/02/05/the-mercurial-revlog/)).

### Durability / checkpoints

Revision data is stored as **delta chains with periodic full snapshots**: once the cumulative delta size since the last snapshot exceeds a threshold (and per heuristics on chain length / change size), a new full snapshot is written instead of another delta ("inspired by video keyframes") ([Nathan Goldbaum](https://ngoldbaum.github.io/posts/revlog/); [book.mercurial-scm.org concepts](https://book.mercurial-scm.org/read/concepts.html)). **Reconstruction** = locate the base snapshot for a rev, then apply the chain of deltas forward. Storage layout is configurable: **interleaved** (data inline after each index entry, `.i` files) for small revlogs vs **separate data files** (`.d`) for large ones — *the same logical structure, two physical layouts.* The 2025 `delta-info-revlog` format adds explicit snapshot/quality metadata per delta to improve delta-tree heuristics ([Mercurial 7.2 relnotes](https://www.mercurial-scm.org/relnotes/7.2)).

### Schema evolution

Revlog format versions are gated by repository **requirements** flags; format migration (e.g. revlogv1 → revlogv2/changelogv2, `delta-info-revlog`) is done by an explicit `hg debugupgraderepo` rewrite pass. Like git, the *payload* schema (what a filelog entry means) is opaque to the revlog; revlog evolves its *container* format, not the application's record types.

### Library genericity

Revlog is reused *within* Mercurial by parameterizing one structure over payload meaning — the textbook "one generic mechanism, three instantiations." But it is **not** packaged as a standalone reusable library for third parties; it is internal Python (with C/Rust accelerators). The genericity is "same code, three call sites," not "published generic crate."

### What worked / what hurt

Worked: extremely compact storage, O(1)-ish append, integrity via per-rev hashing that includes parent hashes, and the keyframe-snapshot trick bounds reconstruction cost. The interleaved-vs-separate-file split is a *direct precedent for our same-file-vs-separate-file experiment* and Mercurial chose **both, switching by size**. Hurt: long delta chains caused real read-amplification pathologies (Mozilla-scale pain drove repeated format work); the 64-byte fixed index couples format tightly; deltas are *byte deltas over serialized content*, which is exactly what our brief rejects for schema transitions (a schema change invalidates the byte-delta basis).

## Fossil

### Core model — the closest analogue to our direction

Fossil is a DVCS built **on SQLite**, and its design explicitly separates authoritative content from derived relations. Every version of every file, wiki page, ticket change, and check-in is an immutable **artifact** identified by its SHA hash; "a Fossil project is a bag of artifacts" ([Fossil: Technical Overview](https://fossil-scm.org/home/doc/tip/www/tech_overview.wiki)). The authoritative storage is **two tables**: `blob` (`uuid` = content hash, `rid` = local integer key, `size`, `content` = zlib+optionally-delta-compressed bytes) and `delta` (maps a blob to the predecessor it is a delta against). *Everything else is derived* ([Fossil: Fossil is not Relational](https://www3.fossil-scm.org/home/doc/tip/www/fossil-is-not-relational.md)).

### The view-is-rebuildable property — this is our accepted direction, already shipped

Fossil's relational tables (`plink`, `mlink`, `filename`, `event`, …) are explicitly **transient cross-link caches**: "All of them, except for `blob` and `delta`, can be destroyed with no loss of SCM-relevant data… destroyed and then recreated by crosslinking all artifacts from the `blob` table (which is exactly what the `rebuild` command does)" ([Fossil: not Relational](https://www3.fossil-scm.org/home/doc/tip/www/fossil-is-not-relational.md)). This is *exactly* our "demote redb tables to a rebuildable materialized VIEW; the log is authoritative" direction, proven in production — including the operational consequence that the queryable schema can evolve **independently** of the immutable artifact format, because `rebuild` regenerates it.

### Durability / replication

Artifacts are content-addressed, so sync is set-reconciliation. The **sync protocol** is a round-based, eventually-consistent HTTP card exchange: peers advertise inventory with `igot` cards, request missing artifacts by hash with `gimme` cards, and transfer with `file` cards in two forms — full (`file id size content`) or **delta** (`file id delta-source-id size content`), where the delta source may be sent after the delta so peers buffer-and-apply ([Fossil: The Fossil Sync Protocol](https://fossil-scm.org/home/doc/tip/www/sync.wiki)). To avoid exhaustively diffing all hashes, **cluster artifacts** list other artifact IDs so a peer follows a chain of clusters to enumerate the repo; requests are capped (~1MB) to bound round size; sync iterates "until the client holds all artifacts that exist on the server." This is precisely our **"ship the log suffix since the peer's last head to the server"** backup model, generalized to content-addressed set difference, and it directly informs the local-committed / queued-for-mirror / server-committed durability ladder.

### Schema evolution

Two layers. (a) The **artifact format** itself is a stable, documented, never-rewritten control-card grammar — the durable contract. (b) The **SQLite query schema** evolves freely because `rebuild` regenerates it from artifacts; Fossil bumps an internal schema cookie and rebuilds on version upgrade. So Fossil cleanly *splits the fragile-evolving part (the queryable view) from the stable-authoritative part (the artifacts)* — the same split our brief draws between schema-fragile rkyv tables and an authoritative log.

### Library genericity

Fossil is a **monolithic single executable**, not a reusable library — the *anti-example* for j487's "library not service." Its content-store + rebuildable-view *architecture* is highly reusable as a pattern, but the code is not packaged for embedding. It leans on SQLite (which *is* the reusable embedded substrate) and treats artifacts as opaque typed-by-control-card payloads, not Rust-typed records.

### What worked / what hurt

Worked: the artifact-bag + rebuildable-cache split is robust, self-checking ([Fossil: Repository Integrity Self-Checks](https://fossil-scm.org/home/doc/trunk/www/selfcheck.wiki)), and lets the query schema churn freely; building on SQLite gave free ACID/durability. Hurt: artifact content is opaque blobs (needs a Fossil-specific function to even read a delta-compressed blob — "extraction… cannot be performed via vanilla SQL"); monolithic packaging blocks reuse; sync is eventually-consistent (acceptable for a DVCS, but means *no read-after-write across peers* — our brief explicitly requires the local view to NOT lag).

## The four-way comparison on the genericity axis (the central tension)

| System | Payload typing | View rebuildable from log? | Packaged as reusable lib? | Genericity mechanism |
|---|---|---|---|---|
| git | unityped (4-enum tag + bytes) | refs are mutable; objects immutable | no (ref impl) | uniform (type,hash,bytes) triple |
| libgit2 | unityped (void*/bytes) | n/a | yes, C callback backends | struct-of-fn-pointers backend |
| gitoxide | unityped (parsed object enums) | n/a | yes, layered crates + facade | `Find`/`Write` traits + feature flags + small crates |
| Mercurial revlog | opaque payload, 3 instantiations | data reconstructs from snapshot+deltas | no (internal) | one struct parameterized by payload meaning |
| Fossil | opaque artifact (typed by control card) | **yes — `rebuild`** | no (monolith) | SQLite blob+delta + rebuildable cache |

Every prior-art system resolves the "generic over payloads" tension by going **unityped/opaque** — none of them carries a compile-time-typed payload through a generic content store. That is the gap our discipline forces us to close that none of these donors solved: we must keep gitoxide-style trait/crate reuse and Fossil-style log-authoritative-view-rebuildable architecture, *without* adopting their stringly/opaque payload. The likely synthesis the experiment must probe: the generic layer owns *ordering, hashing, log structure, checkpoint, sync* (the parts that are genuinely payload-agnostic), while a per-component typed boundary owns *decode-by-schema-hash into the real Rust type* (the part that must stay perfectly specific). That boundary is the schema-hash decoder selector already named in our typed replay envelope.
