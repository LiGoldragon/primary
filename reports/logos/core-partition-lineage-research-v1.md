# Core partition/merge lineage — prior-art-grounded suggestions (research v1)

Psyche-ordered research, verbatim: "This is a hard question. Do some research and
make suggestions using similar systems or systems that do similar things as
inspiration." Written 2026-07-16, session `LanguageFamilyPrototype`, lane
`LineageResearch`, generalist, Opus 4.8 (1M). Read-only on all repos; this file
and the chat return are the lane's only artifacts. The chat return carries the
full suggestions self-contained — this file is the durable agent pickup point.

The deliverable is prior-art-grounded suggestions for **Codex slate item 3**
(document-core-adapter-design-v2 §"Decision slate": "what authoritative
lineage/allocation rule carries NameTables through document split and merge?")
and the sibling **bead primary-56d1.11** ("the unit of 'one schema' in the
daemon, including split and merge identity semantics"). The psyche rules; nothing
here is accepted.

## 1. The question, precisely, and what already survives

When the durable Core is partitioned into multiple stores/universes, or several
Cores merge, what preserves identifier continuity?

**Already partition-proof by construction (verified in code):** Core *content*
identity is BLAKE3 over stringless rkyv bytes, domain-separated and
layout-version-tagged, with the NameTable physically excluded from the pre-image
(`content-identity/src/hash.rs:56-76`; `core-logos/tests/content_hash.rs`
proves rename-stability, structural/visibility edits move it). Identical Core
values in any two stores coincide on hash and never conflict on merge. This is
already the Unison / IPFS-CID / git-object property — the stack's spine is
content addressing, and that layer needs no lineage service.

**Does NOT automatically survive partition — the actual question:**

1. `CoreUniverseId` — today a `u32`, with `FIXTURE_UNIVERSE = CoreUniverseId::new(0)`
   as an explicit placeholder pending this ruling (`structural-codec/src/ids.rs:34-35`).
   Load-bearing: it is folded into the structural table-identity pre-image
   (`TableIdentityPayload { core_universe, … }`, `table.rs:65-74`). Two universes
   both numbered `0` cannot coexist; merge is ambiguous.
2. `ScopedCoreTypeId { universe, local: u32 }` — the `local` counter is allocated
   within a universe (`ids.rs:22,53-66`). Unique only relative to a
   non-colliding universe id.
3. NameTable `Identifier(u32)` — a flat, append-only string→u32 interning index
   (`name-table/src/identifier.rs:24`, `name.rs:27`). No graph, no cross-store
   meaning today.
4. Sema-engine stored-record identity basis — blocked on 56d1.11 (56d1.13).

**Codex's framing:** durable "lineage receipts," choice = preserve / reallocate /
defer, recommending **preserve**. The doctrine v2 allocation discipline already
records the hard sub-case (§"Shared Core and NameTable law", point 4): a bare
source spelling change without prior allocation context "is not assumed to be a
rename. It can be delete-plus-add" — an intent that content alone cannot recover.

## 2. Five candidate approaches

Each: the inspiring system(s); the concrete mapping onto this machinery; the
machinery cost; failure modes; fit with rkyv portability, stringless Core, and
the two non-rejected storage proposals on primary-56d1.10 (proposal 1 =
format-upgrade modeled on sema-engine's layout-upgrade machinery; proposal 2 =
NameTables stored as first-class co-versioned Core siblings).

### Candidate A — Content/crypto-derived universe identity (dissolves the type-id collision)

**Inspiration.** Unison: "the hash is the true name," a 512-bit SHA3 over
structure excluding names, so identity needs no registry
(unison-lang.org/docs/the-big-idea). IPFS CIDs: a self-describing content hash,
"the same content … will produce the same CID" in any node
(docs.ipfs.tech/concepts/content-addressing). Git objects: `SHA1(header+content)`,
identical content re-hashes identically (git-scm.com Git-Internals-Git-Objects).
did:key: a globally-unique identifier expanded from key material with "no
centralized registration authority," generated offline (w3.org/TR/did-core,
w3c-ccg.github.io/did-key-spec). Cap'n Proto: a minted 64-bit type id carried in
the schema source, unique "by construction … without coordination"
(capnproto.org/language.html).

**Mapping.** Replace `CoreUniverseId(u32)` + `FIXTURE_UNIVERSE(0)` with a
collision-proof universe id, in one of two flavors:
- **A1 minted (did:key / Cap'n Proto):** mint a random ≥128-bit id once at
  universe genesis, offline, no coordinator; treat it as immutable thereafter.
- **A2 content-derived (Unison / CID / git):** the universe id is a BLAKE3 hash
  of the universe's immutable genesis seed. Identical universes coincide (dedup);
  distinct ones cannot collide.

Then `ScopedCoreTypeId` is globally unique, `local: u32` stays a cheap
within-universe counter, and **merge of two stores is a set-union of universes —
collision-free by construction, no receipts, no coordinator.** This is the direct
fix for the parked `FIXTURE_UNIVERSE(0)`.

**Cost.** Widen the id (u32 → 128-bit or a `ContentHash` newtype); a Core-layout /
table-layout version bump — which is exactly what non-rejected proposal 1's
format-upgrade mechanism exists to carry. Low ongoing cost; no runtime service.

**Failure modes.** A1's classic misuse (Cap'n Proto's named failure): cloning a
universe while copying its minted id forges a false identity — guard the clone
path. A2 avoids clone-forgery (a copy is correctly the same universe) but requires
a genuinely immutable genesis seed; if the seed can evolve, the id moves
(git-rewrite problem). Use ≥128-bit width, never Cap'n Proto's 64-bit (its
"~billion types" birthday concern is real at 64-bit; negligible at 128/256).

**Fit.** Perfectly with the grain — the stack is already content-addressed and
coordination-free for Core; this extends the same discipline to the universe id.
rkyv-portable (a fixed-width byte array). Composes with proposal 1 (the widening
is a format upgrade) and proposal 2 (universe id travels in the co-versioned
sibling's provenance).

### Candidate B — Names/refs are never durable identity; the u32 is store-local cache (dissolves the NameTable question)

**Inspiration.** Unison: names are "separately stored metadata that don't affect
the hash"; short/numeric hashes are display-only, substituted for the full hash
at compile time; merging codebases is a union over hash-keyed definitions and the
only conflicts are name-level, never definition-level
(unison-lang.org/docs/language-reference/hashes). Git refs: "a ref is just a
mutable name pointing at a commit hash, carrying no content identity"; branches do
not survive a rewrite as identity. IPFS separates immutable CIDs from the mutable
IPNS pointer layer (docs.ipfs.tech/concepts/ipns).

**Mapping.** Declare, as law, that NameTable `Identifier(u32)` is a **store-local
interning index, never a cross-store durable identity** — the exact status of a
git ref, a Unison short-hash, or an IPNS pointer. It therefore **does not need to
survive partition.** On merge, re-intern each name into the target store's space;
the u32s renumber freely, and nothing load-bearing moves, because (i) Core
identity excludes the table by construction and (ii) name-level continuity is
resolved by `(kind, owner, spelling)`, not by the integer. On this reading the
"what carries the u32 allocation space across split/merge?" question **dissolves:
nothing does, and nothing must.**

**Cost.** Nearly zero mechanism — it is a constraint, not a service. It formalizes
what doctrine v2 already does (re-associate by `(identifier kind, owner scope,
current spelling)`). Re-interning on merge is an O(names) pass.

**Failure modes.** Only where a u32 *was* mistakenly persisted as durable identity
outside its store (e.g. a sema-engine stored record that keyed by raw
`Identifier`) — that record must be rehydrated through its co-versioned NameTable
sibling, not read as a global key. This candidate's whole job is to forbid that
mistake.

**Fit.** With the grain — it is the Unison architecture the stack already half-
implements (stringless Core + excluded NameTable). rkyv-portable trivially.
Composes with proposal 2 (the NameTable sibling *is* the store-local name layer)
and is the reason a general lineage-receipt service for the u32 space is
over-engineering.

### Candidate C — Durable lineage receipts / explicit id-map artifact (Codex's proposal, grounded)

**Inspiration.** Git filter-repo writes an explicit `commit-map` (old→new columns
for every commit, all-zeros = removed) and `ref-map`, precisely because commit ids
*change* on rewrite; `git replace` / grafts let old ids still resolve
(git-filter-repo docs; git-scm.com/docs/git-replace). Confluent Schema Registry
preserves schema ids across a registry boundary via the **Schema Exporter** +
**IMPORT mode** ("acts like a mini-connector … change data capture for schemas,"
destination read-only, ids preserved not reallocated) and isolates independently-
allocated sources into separate **contexts** to avoid id collisions
(docs.confluent.io schema-linking, migrate). Protobuf **`reserved`** tombstones
retired field numbers/names so they can never be reused
(protobuf.dev/programming-guides/proto3).

**Mapping.** At each split/merge event, emit a durable, content-identified receipt
mapping old allocation → new allocation (universe ids, type ids, and/or name
ids), plus a `reserved`/tombstone set for retired ids so a later reallocation
cannot silently reuse them. This is Codex's "preserve via receipts" verbatim.

**Cost.** Highest of the five: a receipt record type, its own content identity and
layout version, storage, and a merge/split procedure that reads and applies it.
Every partition event becomes a transaction with a durable artifact. This is
git's cost, paid because git *chose* mutable commit ids.

**Failure modes.** Receipt drift (a receipt not written, or written and not
applied) silently corrupts continuity — the failure git mitigates with
"list every commit, even unchanged ones." Confluent's own warning applies: merge
two independently-allocated spaces into one namespace and you get id conflicts
unless each keeps its context. If Candidates A+B are adopted, most of this
machinery is redundant, because there is no id that changes on merge to map.

**Fit.** rkyv-portable (a receipt is just another Core-shaped record) and composes
with proposal 2 (receipts co-versioned as siblings). But it is against the grain
as a *general* mechanism: it re-introduces a mutable-id + id-map model into a
stack that deliberately chose content addressing to avoid exactly that. It earns
its keep only in the narrow intent-loss case (see the recommendation).

### Candidate D — One global keyspace, universes as partitions/ranges (central coordination)

**Inspiration.** Datomic entity ids encode the **partition in high bits**; ids are
minted from partition + transaction counter and are meaningful only within the
database that assigned them (docs.datomic.com/schema/identity,
/transactions/partitions). Spanner: one keyspace sorted by user primary key; a
"split" is a **boundary between contiguous key ranges**, added/removed for
size/load, never a key reassignment (cloud.google.com/spanner schema-and-data-
model, pre-splitting). Vitess: a **keyspace id** range per shard; resharding
"splits or merges" by re-cutting range boundaries via VReplication "without having
to move records in other shards" (vitess.io keyspace-id, resharding).

**Mapping.** Treat all universes as reserved sub-ranges of **one** global
allocation keyspace (Datomic-style partition bits, or Vitess-style ranges). Split
= hand out disjoint ranges; merge = range union. Keys never reallocate because
allocation was never independent — it is repartitioning of a single space.

**Cost.** Requires a single allocation authority (or a pre-agreed static range
carve-up). Dense, small, ordered ids as the payoff.

**Failure modes.** The authority is a coordination point and a single point of
failure; it directly contradicts offline/partition-tolerant universe creation.
Two universes created independently offline cannot both draw from one keyspace
without a prior agreement they never had — the exact situation content addressing
exists to handle without coordination.

**Fit.** Against the grain for this stack. Spanner/Vitess/Datomic are single-
authority databases; this stack is a partition-tolerant, coordination-free content
store. Adopting a coordinator for universe ids would trade away the property the
BLAKE3 spine already gives for free. Graded low **for this stack specifically**,
despite being the mainstream database answer.

### Candidate E — Resolve-by-name with aliases; opaque id + resolver indirection (reallocate, but bridge)

**Inspiration.** Avro resolves by **name, not number**, and bridges renames with
`aliases`: a reader field `y` with alias `x` reads writer field `x` "as though 'x'
were named 'y'" (avro.apache.org/docs specification, Schema Resolution/Aliases) —
the deliberate contrast with protobuf's immovable numeric tag. DOI/ARK: an opaque
identifier plus a **resolver indirection table**; persistence "is a function of
organizations, not of technology" / "purely a matter of service," maintained by
updating the map when the object moves (doi.org handle factsheet; arks.org;
Kunze ARK spec). Datomic `:db/unique` upsert: an external stable key resolves onto
whatever local entity id already exists (docs.datomic.com/schema/identity).

**Mapping.** Do not preserve the numeric id across a boundary at all. Resolve
references by `(kind, owner, spelling)` — exactly doctrine v2's re-association rule
— and carry an **alias chain** that bridges renames, so a renamed declaration's
old spelling still resolves to the new one. Reallocation is free; the alias is the
only durable continuity artifact, and only where a name changed.

**Cost.** Moderate: an alias record per rename, stored in the co-versioned
NameTable sibling. No universe coordinator, no per-partition receipt.

**Failure modes.** Aliases must be authored at edit time (Avro's aliases are
declared, not inferred) — which is precisely doctrine v2's unsolved case: a bare
spelling change with no prior context "can be delete-plus-add," and no resolver
can recover which. So E does not eliminate the intent-loss problem; it gives it a
home (the alias) *if* the intent is captured when the edit happens.

**Fit.** rkyv-portable; composes with proposal 2 (aliases live in the sibling).
With the grain for the *name* layer specifically — it is how you get human-name
continuity without making the u32 durable. Complements B rather than competing.

## 3. Graded recommendation — a hybrid, in Codex's preserve/reallocate/defer framing

The five are not mutually exclusive; the load-bearing insight is that the stack
already solved the hard part (content identity survives partition), so each
remaining id belongs to a different layer and takes a different answer.

**Recommended hybrid = A + B + a narrow slice of E/C.**

| Identifier | Ruling (Codex's axis) | Mechanism | Prior art |
|---|---|---|---|
| `CoreUniverseId` / `ScopedCoreTypeId` | **PRESERVE — by construction** | Content/crypto-derived or minted-once universe id (Candidate A). Merge = set union, no receipts. | Unison, CID, did:key, Cap'n Proto |
| NameTable `Identifier(u32)` | **DEFER / reallocate freely — question dissolves** | Store-local interning cache (Candidate B). Re-intern on merge; never a cross-store key. | Unison names, git refs, IPNS |
| Rename-vs-replace *intent* | **PRESERVE — narrowly** | Alias/receipt keyed by durable content identity, authored at edit time only where content is ambiguous (Candidate E, with C's tombstone for retired ids). | Avro aliases, git replace, protobuf `reserved`, DOI/ARK indirection |

**How this rules Codex's slate item 3.** Codex recommended **preserve** across the
board via durable lineage receipts. This research **endorses the instinct and
relocates the mechanism**:

- **Preserve is right for the identities that are load-bearing inside content
  identity** (the universe/type ids folded into the structural table hash) — but
  achieve preservation **by construction** (a collision-proof universe id), which
  is cheaper, coordination-free, and receipt-free. A general lineage-receipt
  *service* is heavier than the problem.
- **The NameTable u32 space does not need preserving at all** — Unison-style, a
  numeric surface id is never durable outside one store, so partition needs no
  lineage service for it. This is the part of the question that genuinely
  **dissolves**.
- **A durable receipt/alias survives in exactly one place:** the rename-vs-
  delete+add intent that content addressing cannot recover (doctrine v2's own
  unsolved case). There, the receipt is not a partition-time service but an
  **edit-time intent record**, keyed by the durable content identity and stored in
  the co-versioned NameTable sibling.

**Explicit dissolution note (as ordered).** Yes — a candidate dissolves the
question, and it is the stack's own architecture. Because Core content identity
already survives partition (BLAKE3, NameTable excluded) and numeric surface ids
are, Unison-style, never durable outside one store, **partition per se needs no
lineage service.** Only two residues remain: (1) the universe id must be made
collision-proof so independently-created universes can coexist and merge — a
minting/derivation discipline, not a service; and (2) the human-name rename
intent needs an edit-time alias, because it is information content cannot carry.
Everything else the psyche might have feared he must build (a partition-time
id-remapping service over the u32 space) is unnecessary under content addressing.

## 4. Fit with the non-rejected storage proposals (primary-56d1.10)

- **Proposal 1 (format-upgrade mechanism):** widening `CoreUniverseId` u32 →
  128-bit/hash (Candidate A) is a Core-layout / table-layout version bump; the
  format-upgrade machinery is exactly the carrier for old stores. A composes with 1.
- **Proposal 2 (NameTables as co-versioned Core siblings):** the store-local name
  layer (B), the rename aliases (E), and any tombstone/receipt (C) all live in the
  co-versioned sibling. B/E/C compose with 2.

Both proposals remain non-rejected; nothing here accepts them. If A is chosen, the
universe-id widening is the first concrete consumer of proposal 1, which is worth
flagging when the psyche rules on 56d1.10.

## 5. Sources

Local ground truth: `reports/logos/up-close-design-v1.md` (§4.1 identity keystone,
`ScopedCoreTypeId`/`CoreUniverseId`); `reports/logos/stack-re-audit-v1.md`
(Scope 5 identity keystone, Scope 6 table-identity payload + `FIXTURE_UNIVERSE`);
`reports/schema/document-core-adapter-design-v2.md` (allocation discipline,
decision slate item 3); beads primary-56d1.10, primary-56d1.11, primary-56d1.13.
Code cited transitively through the re-audit (content-identity `hash.rs`,
name-table `identifier.rs`/`name.rs`, structural-codec `ids.rs`/`table.rs`,
core-logos `content_hash.rs`).

External prior art (URLs gathered this session):
- Cap'n Proto unique ids — capnproto.org/language.html
- Unison — unison-lang.org/docs/the-big-idea, /language-reference/hashes,
  /language-reference/name-resolution-and-the-environment
- Git objects / filter-repo / replace — git-scm.com/book/en/v2/Git-Internals-Git-Objects,
  git-filter-repo Documentation, git-scm.com/docs/git-replace
- W3C DID / did:key — w3.org/TR/did-core, w3c-ccg.github.io/did-key-spec
- Confluent Schema Registry — docs.confluent.io schema-registry fundamentals,
  schema-linking-cp, installation/migrate
- Protocol Buffers — protobuf.dev/programming-guides/proto3 (field numbers,
  reserved, updating a message type)
- Apache Avro — avro.apache.org/docs/1.11.1/specification (Schema Resolution,
  Aliases)
- Datomic — docs.datomic.com/schema/identity, /transactions/partitions
- Google Spanner — cloud.google.com/spanner/docs schema-and-data-model,
  pre-splitting-overview
- Vitess — vitess.io/docs concepts/keyspace-id, sharding, vreplication reshard
- IPFS / IPLD CIDs — docs.ipfs.tech/concepts/content-addressing, /ipns;
  github.com/multiformats/cid
- DOI / Handle — doi.org DOI-system-and-the-Handle-System; ARK — arks.org,
  Kunze "Towards Electronic Persistence Using ARK Identifiers"
