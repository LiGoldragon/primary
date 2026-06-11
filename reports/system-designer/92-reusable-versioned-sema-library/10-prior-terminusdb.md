# Prior art: TerminusDB

## What it is and its core model

TerminusDB is an open-source, in-process document/graph database with built-in, Git-style version control over the data itself: branch, diff, merge, rebase, clone, push, pull, and time-travel queries, with ACID transactions and on-write schema validation against a typed schema ([terminusdb.org/docs/terminusdb-explanation](https://terminusdb.org/docs/terminusdb-explanation/)). The query/logic engine is written in Prolog (descended from the earlier DACURA/`regulum` work); since v1.1 ("The Big Babushka", Jan 2020) the storage backend was rewritten in Rust as a standalone crate, `terminusdb-store` / `terminus-store` ([terminusdb.com/blog/terminusdb-1-1-the-big-babushka](https://terminusdb.com/blog/terminusdb-1-1-the-big-babushka/)).

The data model underneath is RDF triples: every document is shredded into `(subject, predicate, object)` triples where the object is either a node id or a literal value ([github.com/terminusdb/terminusdb-store](https://github.com/terminusdb/terminusdb-store)). The document/graph layer and the JSON-LD schema sit *above* the triple store. This is the most important structural fact for our purposes: TerminusDB's version control operates on a single, universal, maximally-generic record shape (the triple), not on heterogeneous typed record families. Everything else flows from that decision.

This is the single closest piece of prior art to "a strict-typed, version-controlled database," and uniquely it solves *exactly* the central tension our brief names: how to be a version-control engine generic over arbitrary typed data without becoming a stringly-typed generic-record store. TerminusDB's answer — generic triple substrate below, typed schema as data above, schema migration as first-class versioned operations — is precisely one of the two poles our design space is bounded by, so it deserves close reading both for what to borrow and what to reject.

## How it version-controls and makes state durable

### Immutable content-addressed layers (the substrate)

Storage is a stack of immutable **layers**. A base layer holds a set of triples; each subsequent **delta layer** records only *additions* and *deletions* relative to its parent — two delta graphs, "one which adds edges, and another which deletes them" ([terminusdb.com/blog/succinct-data-structures-for-modern-databases](https://terminusdb.com/blog/succinct-data-structures-for-modern-databases/)). The current state at any point is resolved by walking the layer stack from the queried layer down to the base, applying additions and masking deletions. Because nothing is ever mutated in place, uncoordinated multi-reader MVCC falls out for free, and any historical state is just "stop walking at layer N."

Layers are **content-addressed**: each layer's name is a hash (the design doc discusses a 20-byte name, SHA2/BLAKE-class, choice deemed not load-bearing as long as no collision/preimage break) computed over its serialized content **including its parent id**, so "each layer hash transitively also hashes all parent layers" — a Merkle hash chain ([github.com/terminusdb/terminusdb-store CONTENT.md](https://github.com/terminusdb/terminusdb-store/blob/main/docs/CONTENT.md)). Serialization is in lexical order so identical content always yields an identical name. This gives tamper-evidence and automatic dedup of identical layers.

### The commit graph (the version control proper)

Branches, commits, and remotes are themselves stored as graphs, addressed by appending suffixes to the database id: `org/db/local/_commits` is the commit graph for a branch's local repository, and `org/db/_meta` is the repository graph holding the local repo plus all known remotes ([github.com/terminusdb/terminusdb README](https://github.com/terminusdb/terminusdb/blob/main/README.md), [terminusdb.org/docs/terminusdb-cli-commands](https://terminusdb.org/docs/terminusdb-cli-commands/)). A commit object points at the layer(s) representing the branch state. So TerminusDB is "data all the way down": the VC metadata is modeled in the same triple/layer machinery as user data, which is why the same diff/merge logic works on schema, on data, and on the commit graph itself.

### Compaction

Long layer stacks slow reads (every query walks the whole chain), so TerminusDB periodically runs **delta rollup**: it squashes a run of delta layers into a new consolidated layer to bound read cost ([terminusdb.com/blog/succinct-data-structures-for-modern-databases](https://terminusdb.com/blog/succinct-data-structures-for-modern-databases/), [terminusdb.com/blog/big-graph](https://terminusdb.com/blog/big-graph/)). This is the same problem our brief flags under "checkpoint protocol / compaction breaks naive suffix sync."

### Durability and replication on a server

Durability-on-a-server is handled by the **clone/push/pull/fetch** model, communicating *diffs* (layer deltas) between nodes, exactly like Git ([terminusdb.com/blog/distributed-database-with-collaboration-model](https://terminusdb.com/blog/distributed-database-with-collaboration-model/)). Because layers are content-addressed and parent-linked, a push need only ship the layers the remote does not already have — the suffix of the chain past the remote's known head. Backup is therefore literally "push the new layers to the server," which is the same shape as our brief's "ship the log suffix since the peer's last head."

### Succinct structures (compression, not versioning)

The in-memory representation of each layer uses succinct data structures (wavelet trees / bit-vectors with rank-select) reaching ~13 bytes/triple on billion-triple sets, persisted to disk but queried in-memory ([terminusdb.com/blog/succinct-data-structures-for-modern-databases](https://terminusdb.com/blog/succinct-data-structures-for-modern-databases/), [assets.terminusdb.com research PDF](https://assets.terminusdb.com/research/succinct-data-structures-and-delta-encoding.pdf)). This is an encoding/compression concern orthogonal to versioning and orthogonal to our rkyv/redb substrate — noted so it is not mistaken for part of the VC mechanism.

## Schema-evolution story (the part most relevant to us)

This is TerminusDB's standout contribution and the most directly transferable idea. Schema is data (JSON-LD documents in the schema graph), so it is versioned by the same machinery. On top of that, since the 2023 work, **schema migrations are first-class, named, replayable operations tracked per commit** ([terminusdb.org/blog/2023-04-24-schema-migration](https://terminusdb.org/blog/2023-04-24-schema-migration/)).

A migration is a list of typed operations recorded alongside the commit. Two classes:

- **Weakening** operations cannot invalidate existing instance data, so they are *inferred automatically* when you just edit the schema — no explicit migration needed ([terminusdb.org/docs/what-is-schema-weakening](https://terminusdb.org/docs/what-is-schema-weakening/)).
- **Strengthening** operations can change/invalidate instance data, so they must be explicit and carry the data-rewrite instructions (default value or cast); these remain partly experimental.

The named operation vocabulary ([terminusdb.com/docs/schema-migration-reference-guide](https://terminusdb.com/docs/schema-migration-reference-guide/)):

| Operation | Class | Carries |
|---|---|---|
| `CreateClass` | weakening | — |
| `DeleteClass` | strengthening | — |
| `MoveClass` | strengthening | — |
| `ReplaceClassMetadata` | weakening | — |
| `ReplaceClassDocumentation` | weakening | — |
| `ReplaceContext` | weakening (conditional) | — |
| `ExpandEnum` | weakening | — |
| `CreateClassProperty` | weakening, or strengthening if required | optional default value |
| `DeleteClassProperty` | strengthening | — |
| `MoveClassProperty` | strengthening | — |
| `UpcastClassProperty` | weakening | — |
| `CastClassProperty` | strengthening | `DefaultOrError` (a default value, or fail-on-impossible) |
| `ChangeKey` | strengthening | — |

The transformation is **bidirectional and replayable**: applying a migration returns a count of `{schema_operations, instance_operations}`, confirming it rewrites instance data in the same step. Crucially, a migration can be *targeted across branches* (`terminusdb migration <branch> -t <other>`), which "makes branches comparable so that change requests can be made between them" — i.e. divergent schema histories are reconciled by replaying typed migration operations (with their defaults) rather than by byte-diffing incompatible representations ([dev.to/terminusdb/schema-migration-for-graph-databases-15p6](https://dev.to/terminusdb/schema-migration-for-graph-databases-15p6)).

This is almost exactly the brief's `SchemaTransition(v_old -> v_new, reducer)` typed-log-entry concept, validated in production by an independent project: a schema migration is a *named operation with a data-rewrite rule*, recorded in version history, replayable to bring any peer/branch forward — not a cell-level or byte-level diff.

## Packaging: reusable library vs monolithic service

Mixed, and the split is instructive. `terminus-store` *is* a genuinely reusable Rust library, published on crates.io/docs.rs, "intended as a common base for anyone who wishes to build a database containing triple data" ([docs.rs/terminus-store](https://docs.rs/terminus-store/latest/terminus_store/)). Its public surface is trait/type-based: a `Layer` trait, `IdTriple` and `ValueTriple` structs, an `ObjectType` enum, `SimpleLayerBuilder`, and store factories (`open_directory_store`, `open_memory_store`, `open_archive_store`, plus a `store::sync` wrapper embedding its own tokio runtime). A consumer opens a store, gets the head layer, builds a child layer via the builder, and commits.

But the genericity mechanism is the catch: **`terminus-store` is generic over nothing data-shaped — it is hard-wired to the triple.** It achieves "works for any database" by fixing the universal shape `(subject, predicate, object)` and pushing all type meaning up into the schema layer, which is itself stored as triples. There is no generic parameter `Layer<RecordType>`; there is one `Layer` trait over one triple model. The version control, diff, and merge are reusable precisely *because* they only ever see triples. The typed database (TerminusDB proper, the Prolog engine, schema validation, migrations) is the monolithic service built *on top* and is **not** itself a reusable library.

So TerminusDB resolves the generic-vs-typed tension by *layering*, not by parameterizing: generic substrate (triples + layers), typed semantics as data above it. That is one coherent answer to our central tension — and it is the answer we have a hard discipline constraint against (perfect specificity; the type carries meaning, not stringly-typed metadata; no generic-record store). It is the pole we must understand in order to deliberately sit elsewhere.

## What worked

- **Layering generic substrate under typed semantics** made a Git-complete VC engine (branch/merge/diff/rebase/clone) reusable across arbitrary schemas with one implementation. The VC code never grows with the type catalog.
- **Content-addressed Merkle layer chain** gives tamper-evidence, free dedup, cheap suffix-sync for backup/replication, and trivial historical reads (stop walking). Push = ship unknown layers.
- **Delta layers** keep history compact; **rollup** bounds read latency without losing history semantics.
- **Schema migration as named, classified, replayable operations carrying data-rewrite rules** is the key win: weakening auto-inferred, strengthening explicit-with-defaults, both recorded per commit and replayable to reconcile divergent branches. This is the production-proven instance of the brief's `SchemaTransition` log entry.
- **Modeling VC metadata (commits/branches/remotes) in the same store as data** meant the diff/merge engine got reused for free on the version graph itself.

## What did not / known pain

- **Strengthening migrations are still flagged experimental** — automatic data rewriting under tightening constraints is the genuinely hard part, and even the closest prior art has not fully nailed it. Expect our `reducer` story to be the hard problem too.
- **Long layer stacks degrade reads**, forcing rollup/compaction; compaction then complicates naive "everyone has the same chain" sync (a remote pinned to a pre-rollup head must be handled). This is the brief's checkpoint/compaction warning, confirmed.
- **The Prolog engine is heavy and idiosyncratic**; the reusable, fast, well-factored part is the Rust store, not the database.
- **The triple-shred imposes a real cost**: every typed document is exploded into many triples and re-assembled; type/constraint checking is a query-time/validation concern, not a compile-time one. There is no Rust-type-level guarantee that an instance matches its schema — validation is dynamic.
- **Defaults represented as strings** even for non-string fields ("represented as a string, unfortunately") — a smell of the stringly-typed generic substrate leaking through the typed facade.

## How it maps to our system

The transferable architecture: *content-addressed, parent-linked, append-only delta entries form the authoritative history; current state is a materialized view; schema change is a typed, named, replayable operation carrying a data-rewrite rule; backup/replication is shipping the unknown suffix to a server.* That is, point-for-point, the brief's "version the log, not the store" direction — and TerminusDB is the existence proof that it works at scale. Where TerminusDB stores its history *as content-addressed layer files in its own store*, our equivalent is the payload-bearing hash-linked commit log; both keep the live read view from lagging while letting the remote mirror lag. The hard divergence is the generic-vs-typed axis (below).

## Library-shape lesson for j487

`terminus-store` is the precedent for "build the VC mechanism once as a reusable library." But its genericity is achieved by erasing type into a single triple shape — exactly what `skills/abstractions.md` (perfect specificity, the type carries meaning) forbids us. The design question TerminusDB poses to us, sharply: *can the hash-linked replayable-log + materialized-view machinery be made generic over a component's typed record families (mind, spirit, repository-ledger, criome) without collapsing into a triple/stringly-typed substrate?* TerminusDB says "only by erasing the types"; our discipline says "find the owning noun and keep the types." Resolving that is the heart of j487 — and is exactly what the brief leaves undecided.
