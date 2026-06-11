# Prior art: serialization schema evolution

## Scope and framing

This maps how the major serialization formats handle schema change, and reads each against our stance and the j487 reusable-VC brief. It does not choose a design.

The central contrast: **every mainstream format below is built around in-place, wire-compatible evolution — old and new code reading the same bytes by ignoring/defaulting unknown fields. We have deliberately taken the opposite stance.** rkyv 0.8 archives are schema-FRAGILE: any field add/remove/reorder changes the byte layout, with no silent backward compatibility (confirmed in our brief and by rkyv's own design — see below). So the formats' headline feature (forward/backward wire compat) is the thing we have rejected, and their *secondary* machinery (schema identity, fingerprints, registries) is the thing that actually applies to us. Read each section for that split.

A second framing: our accepted direction is "version the LOG, not the store" with a typed `SchemaTransition(v_old_hash -> v_new_hash, reducer)` entry carrying a per-entry SCHEMA-HASH decoder selector. The closest production prior art for that selector is **Avro single-object encoding** (a schema fingerprint prepended to every record) and **Confluent's schema registry** (a registry-assigned schema id prepended to every record). The closest prior art for the "log is authoritative, tables are a rebuildable view" shape is **Datomic**. Both are detailed below.

## Our format: rkyv 0.8 — near-zero evolution tolerance

rkyv stores zero-copy archived bytes laid out like a compiler arranges a struct: fixed widths, fixed offsets, alignment. There is no field-tag/vtable indirection at rest, so the byte layout *is* the schema. Consequences confirmed against rkyv's own maintainer and docs:

- **Format is pinned within 0.8 but the *type* schema is not evolvable in place.** Data serialized under 0.8 stays compatible for the life of 0.8 releases; 0.7 data is not 0.8-compatible (major bump). That is *format/version* stability, not *schema* evolution.
- **Schema evolution is an unfinished, opt-in side feature, not a core capability.** The only sanctioned mechanism is the `Versioned<T>` + `#[rkyv(with = AsBox)]` "out-of-line serialization" pattern in `rkyv/examples/backwards_compat.rs`. It gives **backward** compat only: "we can view a v2 as a v1" but explicitly "we can't view a v1 as a v2 because v1 is not forward-compatible with v2." Its own comment states version negotiation needs an external protocol: "sending a version number along with the buffer would allow clients to reject incompatible messages before validating the buffer."
- **Forward compatibility is blocked at the language level.** Maintainer djkoloski (rkyv/rkyv#164, 2022-03-05): true schema evolution needs a DST whose pointer metadata is a version number to compute size/field-availability dynamically — "that's not currently possible because custom DSTs are not supported in Rust." The only workaround is trait objects, which "risks creating a large amount of vtable bloat… The number of vtables would increase linearly with the number of versions."
- **protoss (the dedicated rkyv schema-evolution crate) is abandoned.** Archived/read-only, last push 2022-12-16, 5 stars, ~6 commits. It is not a dependency we can lean on; treat it as a design study, not infrastructure.

The takeaway: rkyv will not give us in-place evolution, and the one library that tried (protoss) is dead. This is not a gap to paper over — it is *why* the brief reaches for migration-per-change and a typed `SchemaTransition` log entry instead of wire-compat tricks. Our "each schema version is a different rkyv type set" framing is the honest reading of the format.

## Tag-numbered, ignore-unknown formats: Protobuf, Thrift, FlatBuffers, Cap'n Proto

These share one model: **fields carry a numeric tag/ordinal on the wire, never a name; readers skip tags they don't recognise and default tags they expect but don't find.** Evolution = append fields, never reuse a retired number.

### Protocol Buffers
- Wire carries field *numbers*, not names; names and order are free to change. Adding fields is the safe operation: old code ignores new fields, new code defaults missing ones.
- Removing a field requires `reserved`-ing its number/name forever so it can never be silently reused with a different type. Changing a field's wire type is unsafe.
- Pure tag-VARINT stream; no zero-copy. Parsing is mandatory.

### Apache Thrift
- Same integer-field-id model: deserialization skips unknown ids; never reuse a numeric id (retired fields stay as comments/renamed stubs).
- Asymmetry worth noting against rkyv: only *optional* fields can be added; *required* is forever ("Required is forever, even in unit tests"). To change a key's type (e.g. i32→i64) you must add a new field and carry both — you cannot mutate a field type compatibly. This is the same wall rkyv hits, but Thrift lets you live behind it via optionality; rkyv gives no optionality at the byte level.

### FlatBuffers
- Zero-copy via a per-table **vtable**: an offset table that says where each field lives or that it's absent (→ default returned). New fields MUST be appended at the schema end; earlier fields can only be `deprecated`, never removed or reordered. Adding a field at the *beginning* silently corrupts reads (CodeV1 reading V2 reads c's bytes as a) — a vivid demonstration of why position matters.
- This is the closest mainstream analogue to "zero-copy that still evolves": it buys evolution by spending one indirection (the vtable) that rkyv does not have at rest.

### Cap'n Proto
- Zero-copy, position-independent (relative word offsets), O(1) "parsing" — load a segment into contiguous memory and dereference. Closest in *spirit* to rkyv's at-rest model.
- Evolution rule: new struct members must have a number larger than all previous; numbers/ordinals are fixed forever; only symbolic names may change. New fields go at the struct end or into reserved padding. Changing an ordinal "would disrupt the entire memory layout and break compatibility."
- Has a defined **canonical form** (preorder, single segment, trailing-zero-word truncation) usable for hashing/signing *without schema knowledge*, and canonical messages are unpacked. This is directly relevant prior art for how a zero-copy format defines a stable, hashable byte image — i.e. how one could content-address a snapshot or log entry deterministically.

**Why none of these "just solve it" for us:** their evolution tolerance comes from a *tagged or vtable'd* wire layout that pays a per-field indirection rkyv deliberately omits for raw mmap speed. Adopting their model means adopting their format (or bolting a vtable onto rkyv ≈ reinventing FlatBuffers/protoss). The brief's no-backward-compat / migration-per-change stance is consistent with keeping rkyv's bare layout and handling change at the *log* layer instead of the *byte* layer.

## Schema-described, registry-backed formats: Avro (+ schema registry)

This is the most load-bearing prior art for the brief, because Avro separates two concerns we are also separating: the **writer schema** (what the bytes are) and the **reader schema** (what the consumer wants), resolved at decode time.

- **Schema resolution:** Avro data is raw, untagged binary that is meaningless without its writer schema; the reader translates writer→reader. Field in writer but not reader → ignored; field in reader but not writer → filled from the reader schema's declared default. Compatibility = "all datum instances of the writer schema can be decoded under the reader schema."
- **The decoder selector exists in production, two ways:**
  1. **Avro single-object encoding** — every record is prefixed with a 2-byte marker `C3 01` (version 1 of the single-object format) + the **8-byte little-endian CRC-64-AVRO (Rabin) fingerprint of the writer schema**. The reader uses the marker to cheaply reject non-Avro, then resolves the fingerprint → writer schema → decode. **This is exactly "schema-hash as decoder selector," shipped.** The fingerprint is a *content hash of the schema*, not of the data.
  2. **Confluent wire format** — a magic byte `0x00` + a 4-byte big-endian *registry-assigned integer schema id* prepended to each record; the id is resolved against a central schema-registry service to fetch the writer schema. This is the "schema registry" model: a centralized authority that mints monotone schema ids and enforces compatibility modes (BACKWARD / FORWARD / FULL / NONE) on registration.
- **What the registry gives that a bare fingerprint doesn't:** a *governance gate* — it can reject an incompatible schema *at registration time* before any bad data is written, and it gives an ordered id space (a registry id is a small sortable int; a fingerprint is not). This maps cleanly onto our split: a content **schema-hash** is the decoder selector (the `v_old_hash`/`v_new_hash` in `SchemaTransition`), while a monotone marker stays the ordered cursor (our `CommitSequence`). The brief's instinct to keep digests *beside* the monotone markers, not replacing them, is precisely the Avro-fingerprint-vs-registry-id tension resolved by keeping both.

**Where Avro diverges from us:** Avro's whole point is *resolving* writer→reader so old bytes are still readable in place. We have rejected in-place resolution (rkyv can't do it). So we take Avro's *identity machinery* (schema fingerprint as selector, registry as compatibility gate) but NOT its *resolution machinery* (we migrate by replaying through a typed reducer into a new type set, not by defaulting fields at decode time). A "schema registry" for us would be an inventory of `schema-hash → typed rkyv type set + the reducer that transitions from the prior hash" — closer to a migration registry than Avro's read-time resolver.

## Datomic — the "version the log, not the store" shape

Not a serialization format, but the closest *architecture* to our accepted direction, so it belongs here as prior art for `SchemaTransition` and the materialized-view demotion:

- **The log is the information model and the source of truth.** Transactions append immutable datoms (entity, attribute, value, tx) and never update/delete; "a database value is the set of all datoms ever added… it only accrues new information like a log or ledger." The log is queryable as a first-class API, "not an implementation detail."
- **Indexes are derived and rebuildable.** Four covering indexes (EAVT/AEVT/AVET/VAET) are persistent immutable trees built *from* the log, refreshed by background indexing; recent changes merge from an in-memory layer so reads never lag the log. **This is exactly "demote redb tables to a rebuildable materialized VIEW, with read-after-write on the local view, while the remote mirror may lag."** Datomic is independent confirmation that the inversion is sound and shipped at scale.
- It validates two brief points: (a) the local view must not lag even while the durable substrate is remote (Datomic peers merge in-memory recent datoms over remote index trees), and (b) the log being authoritative is what makes time-travel/backup/replication be "ship the log," not "diff the store."

## The schema-hash-as-decoder-selector idea, assessed

The idea is well-grounded in production prior art and is the right shape for rkyv specifically:

- **It is real and proven** (Avro single-object `C3 01` + CRC-64 fingerprint; Confluent magic-byte + schema id). Prefixing every persisted/transmitted record with a schema identity so the decoder knows *which type set produced these bytes* is exactly how the industry handles "the bytes alone don't tell you their schema" — which is precisely rkyv's situation.
- **For rkyv it is arguably mandatory, not optional.** Because an rkyv archive is layout-fragile and self-describes nothing, a record with no schema tag is undecodable after any schema change. A per-entry schema-hash is the minimum viable disambiguator; without it, replay across a `SchemaTransition` cannot know which reducer/decoder to apply.
- **Hash vs. id is the one real choice to surface (not decide):** a content **hash** (Avro/Rabin style) needs no central allocator, dedupes identical schemas, and is verifiable offline, but is unordered and opaque in chat/logs. A **registry id** (Confluent style) is small, ordered, and human-legible, but needs an allocator/authority and a lookup. The brief already resolves this correctly in principle — hash as selector, monotone sequence as cursor — and the registry's *compatibility-gate-at-registration* role is a separate, valuable function worth considering independent of the id-vs-hash choice.

## Discipline-fit notes (for the library, not the design)

- A "schema registry" in our world must obey perfect-specificity: it cannot be a `HashMap<Hash, ()>` of opaque schemas. The owning noun is something like a typed `SchemaInventory`/`SchemaTransition` table where each entry carries the *typed* reducer and the from/to hashes — meaning in the type, not stringly-typed metadata. Today's `CommitLogOperation.table_name: String` (sema-engine/src/log.rs:66) is exactly the stringly-typed smell a payload-bearing, schema-hash-tagged log would have to replace with a typed table id.
- Avro/Confluent are *services with shared registries*; our one-redb-file-per-component rule means the per-component log is local and the *only* shared infra is the server/mirror. A schema-hash selector is per-record-local (travels in the bytes), so it is compatible with no-shared-daemon; a registry *id allocator*, if ever adopted, would be the part that wants to be shared/server-side. That boundary is worth drawing explicitly.

## Summary table

| Format | Evolution model | Decoder selector | Zero-copy | Fit for us |
|---|---|---|---|---|
| rkyv 0.8 | none in place (layout = schema); backward-only via `Versioned`/`AsBox`; protoss dead | none built-in (must be added) | yes (raw layout) | our format; forces log-layer migration |
| Protobuf | append tagged fields; reserve removed | field numbers | no | model only; we won't tag the wire |
| Thrift | append optional fields; ids forever | field ids | no | optionality lesson; "required is forever" |
| FlatBuffers | append at end; deprecate, never remove | vtable | yes | nearest evolvable-zero-copy; = adding a vtable rkyv lacks |
| Cap'n Proto | append, ordinals fixed forever | ordinals | yes | canonical-form hashing prior art |
| Avro (+registry) | writer/reader resolution | **schema fingerprint / registry id (per record)** | no | **schema-hash selector + compat-gate prior art** |
| Datomic | append-only log; indexes derived | tx/log | n/a | **"version the log" architecture prior art** |

