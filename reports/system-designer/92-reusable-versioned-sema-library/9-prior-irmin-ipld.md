# Prior art: irmin (functor-parameterized Merkle store), IPLD/IPFS, Merkle-CRDT

## Scope

Three prior-art systems, all attacking pieces of what Spirit j487 asks for — a reusable, generic, content-addressed version-control mechanism — but from different traditions. Irmin is the closest analogue: a *library* of generic types parameterized by functors over content/hash/branch/path, with a real production consumer (Tezos). IPLD/IPFS is the content-addressed typed-DAG substrate and its schema-evolution discipline. Merkle-CRDT is the formal model that makes a Merkle-DAG double as a logical clock for replication. For each, the brief's seven questions: model, durability/replication, schema evolution, library-genericity mechanism, what worked, what hurt, what applies / does not.

This report maps the genericity mechanism in particular, because that is where our central tension lives: generic over arbitrary record families WITHOUT a stringly-typed generic-record store. Irmin solves exactly this problem in OCaml and is worth studying as an existence proof, not a template.

## Irmin: the functor-parameterized Merkle store

### What it is and its core model

Irmin is "a distributed database that follows the same design principles as Git" — a library, not a CLI, exposing Git's object model (content-addressed blocks, trees, commits, branches, merge) as typed OCaml modules ([mirage/irmin](https://github.com/mirage/irmin), [irmin.org tutorial](https://irmin.org/tutorial/getting-started/)). The principal abstraction is the *store* (`Irmin.S`): a branch-consistent key-value map where keys are paths (lists of steps, like Git filenames) and values are user-defined mergeable contents. Underneath, it is a Merkle-DAG: a content-addressable block store of serialized values + prefix-tree nodes + commit metadata, plus an atomic-write tag/branch store mapping mutable branch names to commit hashes.

### How it version-controls / replicates / makes durable

Two lower-level heaps compose every backend:

- a **content-addressable store** (hash-addressed, append-only, immutable) holding blobs, nodes, and commits — this is the durable history;
- an **atomic-write store** holding mutable branch references (the only mutable surface).

Durability and replication ride Git semantics: snapshot, branch, revert, and a *3-way merge* with a user-supplied merge function. Server-backed durability is whatever backend you instantiate — `irmin-git` writes a real `.git` directory (push/pull/clone work), `irmin-pack` is the optimized on-disk format used by Tezos, `irmin-mem` is volatile. The CHANGES log documents typed Merkle Proofs and proof↔tree conversion for verified remote sync ([irmin docs](https://mirage.github.io/irmin/irmin/Irmin/index.html)).

### Schema-evolution story

Two distinct layers, and the distinction matters for us:

1. **Application content schema** (the user's value type) — Irmin does NOT auto-migrate this. Because the value type is fixed at functor-instantiation time and its serializer is a typed `Type.t` descriptor, a content-type change is a new program; data carries no embedded type tag. Lazy/manual re-interpretation is the user's problem (same posture as IPLD below).
2. **On-disk *format* version** — `irmin-pack` tracks an explicit disk-format version and does provide migration. The CHANGES log shows V1→V5 evolution ([CHANGES.md](https://github.com/mirage/irmin/blob/main/CHANGES.md)): V2 (2.3.0) added a generation number to file headers; V3 (3.3.0) added a read-write/read-only sync mechanism and is explicitly "*not* backwards-compatible — a migration done by the readwrite instance is necessary to open older stores"; V4 (3.5.0) changed the suffix from a single file to a **chunked multi-file design**; V5 (3.7.0) added archiving during GC. A `migrate` function (since 2.3.0) upgrades old stores; V5 added control-file corruption detection via checksum.

This two-axis model — content schema fixed at compile time, storage *format* explicitly versioned with a migration step — is directly relevant to our SchemaTransition-as-log-entry direction.

### Library-genericity mechanism (the central study)

This is why Irmin is the poster prior art. Genericity is **OCaml functors over module-type signatures**, not stringly-typed metadata. The schema is a bundle:

- `module Contents : Contents.S` — the user value type. Requires `val t : t Type.t` (a typed serialization descriptor built from `repr`/Type combinators — *fully compile-time typed, not string-based*) and `val merge : old:t option -> t -> t -> (t, Merge.conflict) result` (3-way merge). ([latest docs](https://ocaml.org/p/irmin/latest/doc/index.html))
- `module Hash : Hash.S` — SHA1/SHA256/BLAKE2B, pluggable.
- `module Path` / `module Branch` / `module Metadata` / `module Info` — key path, branch-name type, per-entry metadata, commit-info type.
- `module Node` / `module Commit` — structural modules, themselves `Node.Make(Hash)(Path)(Metadata)` and `Commit.Make(Hash)`.

The store is built by applying a backend Maker:

- `Irmin.Maker (CA : Content_addressable.Maker) (AW : Atomic_write.Maker)` yields a `Maker`; the user then applies it to their `Schema`.
- `Irmin.KV_maker` is the ergonomic shortcut: it bakes in "string-list paths, string branches, no metadata," so the user supplies only `Contents`. Hence the one-liner `module Store = Irmin_mem.KV.Make (Irmin.Contents.String)`.

The lower-level store signatures stack: `Read_only` ⊂ `Append_only` / `Atomic_write`, `Indexable` ⊂ `Content_addressable`. A backend is "an implementation exposing S, or a functor providing S once applied." The key property: **the content type is concrete and type-checked at every layer**; the genericity is parametric polymorphism via functors, so a `Store` over `int` and a `Store` over your record are different types that cannot be confused. There is no `Value = Bytes` escape hatch in the typed API.

### What worked

- Production-proven at scale: Irmin is the storage layer for the Tezos blockchain (Octez), where `irmin-pack` + GC reduced disk usage and hit 1000+ TPS ([Tarides](https://tarides.com/blog/2022-04-26-lightning-fast-with-irmin-tezos-storage-is-6x-faster-with-1000-tps-surpassed/), [Tarides GC/archive](https://tarides.com/blog/2023-05-05-optimising-archive-node-storage-for-tezos/)).
- The functor design genuinely delivered swappable backends (mem / fs / git / pack) behind one store interface, and a *typed* merge that the library invokes automatically on branch reconciliation.
- The prefix/suffix split for GC (read-only "frozen" prefix + appendable suffix, GC-commit offset as the boundary) is a clean compaction model for an append-heavy store.

### What did not / known pain

- "The library tends to be rather functor heavy, and even simple uses require multiple functor instantiations" ([2.10.2 docs](https://ocaml.org/p/irmin/2.10.2/doc/irmin/Irmin/index.html)) — the genericity has real ergonomic cost.
- On-disk format churn was disruptive: V3 explicitly broke compatibility and required a read-write migration pass; the layered store was *removed* in 3.0.0 and only later restored via lower-layer support — a multi-release architecture wobble around exactly the compaction/archival concern our checkpoint protocol must nail.
- Content-schema evolution is unsolved by the library; it is pushed to the application.
- Heavy reliance on the `repr`/Type runtime descriptor for generic serialization is an OCaml-specific lever we cannot copy directly.

## IPLD / IPFS: content-addressed typed DAGs

### Model

IPLD ("InterPlanetary Linked Data") is the data model under IPFS: a unified information space where every hash-linked structure is a Merkle-DAG node addressed by a CID (content identifier = multihash + codec + version) ([ipld.io](https://ipld.io/), [ipld/specs](https://github.com/ipld/specs)). The Data Model has primitive kinds (bool, int, float, string, null, bytes), two recursive kinds (list, map), and a distinguished **Link** kind (a CID embedded in data — this is what makes the DAG). Codecs (DAG-CBOR, DAG-JSON, DAG-PB) sit between raw bytes and the Data Model.

### Durability / replication

Content addressing IS the durability/dedup mechanism: identical content has one CID, so sync is a set-difference over CIDs (fetch only the nodes you lack), and any node's CID self-verifies its bytes. IPFS layers Bitswap (block exchange over a DHT) and libp2p PubSub for announce/discover. There is no single authoritative server; durability is "enough peers pin it."

### Schema-evolution story

IPLD Schemas are a structural-typing IDL: structs, unions, enums, plus a **representation strategy** per type that maps the logical type onto the Data Model (so the same struct can serialize compactly or human-readably) ([ipld.io/docs/schemas](https://ipld.io/docs/schemas/)). Migration is explicitly **manual and lazy** ([migrations doc](https://ipld.io/docs/schemas/using/migrations/)): the slogan is "Data Never Changes; only our interpretation varies." Changing a schema does NOT change a CID; old data keeps its CID and is re-interpreted on read. Version detection is by pattern-match (envelope unions with a version field, or attempt-newest-then-fall-back), and a migration is "a function from Node to Node." Code-gen targets only the current version; legacy versions are handled through untyped `Node`.

### Library-genericity mechanism

The genericity is the **Data Model as a universal intermediate representation** plus pluggable codecs and multihash/multicodec self-description. This is the opposite pole from Irmin: IPLD achieves genericity by being *dynamically* typed at the substrate (everything is a Data Model Node) and layering optional structural schemas on top, rather than parametric compile-time types. That is precisely the "stringly-typed generic-record store" shape our discipline forbids at the typed layer.

### Worked / pain

- Worked: CID self-verification + set-difference sync is the gold-standard model for "ship only the suffix the peer lacks," and the *immutable-data, re-interpret-don't-rewrite* stance is a clean answer to schema fragility.
- Pain: manual version detection is fiddly; the universal-Node model loses static typing; CID churn means any byte-layout change forks the address space (the same fragility our pinned rkyv archives have).

## Merkle-CRDT: the Merkle-DAG as a logical clock

### Model

Sanjuán, Pöyhtäri, Teixeira, Psaras (Protocol Labs / UCL, 2020) formalize using a Merkle-DAG as both transport and logical clock ([arXiv 2004.00107](https://arxiv.org/abs/2004.00107)). A **Merkle-Clock** node is a triple `(α, e_α, C_α)`: CID α, event e_α, and the CID-set of its direct children (Def. 3). The DAG's ancestry IS the partial order: `n_α < n_β` iff α is a descendant of β (Def. 4), so a node is always "later" than its children. The Implementation Rule: every new event becomes a new root whose child-set is the CIDs of the previous roots. Merging two clocks = union of DAGs (a Grow-Only-Set CRDT), with an optional new root to record the merge.

A **Merkle-CRDT** (Def. 6) is a Merkle-Clock whose nodes carry an arbitrary CRDT *payload* `(α, P, C)`. Because the DAG embeds causality, operation-based CRDTs work even over an unreliable broadcast layer — gap detection and per-object causal consistency come for free from DAG ancestry; no version vectors needed. Two abstractions carry it: **DAG-Syncer** (`Get(CID)->Node`, `Put(Node)`) and **Broadcaster** (`Broadcast(Data)` — typically just the current root CID).

### How it makes state durable / converges

Broadcast only the root CID; peers walk down via DAG-Syncer, fetching only missing nodes (anti-entropy algorithm, Def. 7). Dropped/reordered/duplicated/corrupt messages all self-heal: a missing DAG is re-fetched and applied in causal order; a duplicate is already in the DAG; a corrupt download fails its CID check and is discarded. A brand-new or crashed-without-storage replica can reconstruct full state from any one up-to-date peer.

### Worked / pain (explicit in the paper, §VI)

- Worked: decouples causality from replica count (unlike version vectors); self-verifying, de-duplicated, transport-agnostic.
- **Ever-growing DAG**: the central limitation. Non-batched insertion creates a new node per key-write, "larger than the original object itself"; the authors flag GC/compaction as open future work and warn it requires knowing the full replica set (a constraint they "did not have before").
- **Thin-waist / cold-sync latency**: a DAG with few concurrent events is deep-and-thin; a fresh replica must walk it sequentially (can't parallel-fetch branches), so cold sync can be slower than shipping a snapshot.
- **Merkle-Clock sorting cost** when DAGs have diverged far; DAG-Syncer fetch latency.
- Optimizations offered: delayed/batched DAG nodes, quick inclusion-check via a CID→local key-value index, broadcasting payloads inline, CIDs-as-payload-pointers for dedup, extra "deep" pointers to widen the thin waist.

The appendix names real consumers: `ipfs-log` (the first Merkle-CRDT, an append-only op-based log CRDT — directly analogous to our commit log), OrbitDB (P2P database built on `ipfs-log`), `go-ds-crdt` (δ-state Merkle-CRDT datastore used by IPFS Cluster).

## How the three relate to our seed (today's commit log)

Our `CommitLogEntry { commit_sequence, snapshot, NonEmpty<CommitLogOperation> }` (repos/sema-engine/src/log.rs:15-19, confirmed) with metadata-only `CommitLogOperation { operation, table_name, key }` (log.rs:63-68) is structurally an *un-hash-linked, sequence-addressed* version of `ipfs-log`'s Merkle-CRDT. The design direction ("version the log, hash-link it, make it payload-bearing and authoritative, demote tables to a view") is precisely the move from our current log to a Merkle-Clock with payloads — but where our `CommitSequence` stays the ordered cursor (a blake3 digest sits *beside* it, as the brief states, because the DAG ordering is only partial and unsortable). Irmin contributes the *typed, functor-parameterized* discipline so this stays a typed library, not a Node soup; IPLD contributes the immutable-reinterpret stance and CID-set sync; Merkle-CRDT contributes the formal clock model and the explicit warning list (ever-growing DAG, thin-waist cold sync, GC needs replica-set knowledge).

