# 279 - NOTA schema language and content-addressable version hash

*Deeper design of the NOTA-based schema specification language and
the content-addressable schema-version-hash mechanism naming the
sema database's schema identity. Picks up from /263's initial
sketch and grounds the schema-address-vs-semver fork (sema-upgrade
prototype uses semver `Version (major minor patch)`; this report
moves toward Blake3 hash as canonical identity) plus just-logged
intent record 107. Five questions answered: the grammar; the
canonical encoding under Blake3; what the hash binds to; how the
sema database stores it; how sema-upgrade-daemon dispatches on it.*

## 1. Frame

Intent records 29 and 107 are the same idea two ways. Record 29:
each persona contract carries an explicit schema-layout schema in
a NOTA-based language; fully content-addressable; hash is identity.
Record 107: the sema database holds a schema-version hash as
canonical version identity, derived from a deterministic
content-addressable schema. "Deterministic" and "content-
addressable" name one property — the schema's content fully
determines its hash; the hash IS the address. The sema-upgrade
prototype uses semver `Version (major minor patch)` rather than
the hash from /263/270; record 107 settles toward the hash.
Semver is at best a human label layered above; the hash is
load-bearing identity.

## 2. The NOTA schema language grammar

The schema language is itself NOTA. A schema file is a NOTA stream
under one root record; every declaration is positional (record 42,
skills/nota-design.md): no labeled fields; no tuples; every
PascalCase token is a variant tag per the three-case rule.

### 2a. Top-level shape

```nota
(Schema component [(Leaf …) (Branch …) (Newtype …) (Channel …)])
```

`Declaration` is a five-variant enum: `Leaf` (unit-only enum —
final leaf per record 73; `Kind`, `Magnitude`); `Branch` (struct
or data-carrying enum — record 73; `Entry`, `Observation`);
`Newtype` (transparent newtype); `Channel` (wire vocabulary — one
per signal-component); `Primitive` (workspace-shared scalars
that are neither built-ins `u8`–`u64`/`String`/`bool` nor named
records — rare; `Date`, `Time` if promoted).

The Leaf/Branch split is load-bearing: record 73's branches/leaves
vocabulary maps directly. Leaves carry no layout-annotation block
(no growth axis); branches carry one when growth-relevant.

### 2b. Leaf declarations

```nota
(Leaf Kind
    [Decision Principle Correction Clarification Constraint]
    [(discriminantWidth 1)])
(Leaf Magnitude
    [Minimum VeryLow Low Medium High VeryHigh Maximum]
    [(discriminantWidth 1)])
```

Three positional fields: name, variant sequence (bare PascalCase
unit variants per NOTA case 3), layout annotations.
`discriminantWidth 1` says one byte holds up to 256 variants;
widening to 2 bytes is itself structural. Variant *order* is
load-bearing — rkyv assigns discriminators by declaration
position; reordering is a structural break.

### 2c. Branch — struct shape

```nota
(Branch Entry Struct
    [(topic Topic) (kind Kind) (summary Summary)
     (context Context) (certainty signal-sema:Magnitude)
     (quote Quote)]
    [])
```

Four positional fields: name, shape discriminator (`Struct` or
`Enum`), field sequence, annotations. The discriminator unifies
two sub-shapes into one declaration kind. Each field is
`(camelCaseName Type)`. Type appears bare when it is a primitive
built-in, same-schema reference, or cross-schema reference
written colon-separated (`signal-sema:Magnitude`). Composites use
sequence form: `[Vec Topic]`, `[Option Topic]`. `Vec` and `Option`
are reserved type constructors — not enum variant tags.

### 2d. Branch — data-carrying enum shape; Newtype declarations

```nota
(Branch Observation Enum
    [State (Records RecordQuery) Topics Questions]
    [(discriminantWidth 1) (appendOnly)])

(Newtype Topic String)
(Newtype RecordIdentifier u64)
```

In enum bodies: bare PascalCase is a unit variant (NOTA case 3);
`(VariantName PayloadType)` is data-carrying (NOTA case 1) with
a *named* payload — no anonymous payloads. `appendOnly` commits
to additions-at-the-end-only; the diff classifier flags
mid-insertions as structural. Newtypes have two positional
fields — name, inner type — and no annotations; they inherit
the inner type's layout entirely.

### 2f. Channel declarations

```nota
(Channel Spirit
    operations [(State Statement NoStream)
                (Record Entry NoStream)
                (Observe Observation NoStream)
                (Watch Subscription DomainStream)
                (Unwatch SubscriptionToken NoStream)]
    replies [RecordAccepted StateObserved RecordsObserved
             RecordProvenancesObserved TopicsObserved
             QuestionsObserved SubscriptionOpened
             SubscriptionRetracted RequestUnimplemented]
    events [(StateChanged DomainStream)
            (RecordCaptured DomainStream)]
    streams [(DomainStream SubscriptionToken SubscriptionOpened
                           [StateChanged RecordCaptured] Unwatch)]
    observability default OperationReceived EffectEmitted)
```

Channel is a struct with five named-field legs; each leg is a
`Vec` of leg-specific positional records. Channel legs are
implicitly `appendOnly` (every leg is itself an enum at the rkyv
layer).

### 2g. Cross-schema references and visibility annotations

`signal-sema:Magnitude` names a type from another schema file
(colon matches NOTA's nested-name separator). Cross-schema
references resolve at canonicalisation to the depended-on schema's
hash, not its textual name (§3d).

```nota
(Branch StoredRecord Struct
    [(identifier RecordIdentifier) (entry StampedEntry)]
    [(visibility private)])
```

Default `public` (wire-facing). `private` marks runtime-internal
storage wrappers (`StoredRecord`, `StampedEntry`, table keys per
/273 §2's type-family split). The schema-address hashes over the
union; private wrapper changes flow into the version-hash. The
generator routes private types into the runtime crate and public
types into the `signal-<component>` crate.

## 3. The canonical encoding for hashing

Blake3 over a precisely-specified byte stream. Rules extend
nota/README.md §"Canonical form".

### 3a. Inherit NOTA's canonical form

Field order is source-declaration order. Single space between
tokens within one expression; one newline between top-level
items; no indentation. Integers decimal, no separators. Floats
shortest round-trip; `.` always present. Strings bare when ASCII
ident-shaped, else `"..."`, else `""" """`. Bytes lowercase hex,
`#` prefix. Options bare `None` / `(Some inner)`. Map entries
sorted by key bytes.

### 3b. Comments stripped before hashing

Per nota/README.md: "Comments carry no load-bearing data." The
canonical encoder discards `;;` lines before assembling the byte
stream. A reader can annotate without affecting the hash.

### 3c. Declaration order is authored, not sorted

Top-level declarations in `Schema`'s sequence are **not sorted**.
Reordering is a structural break — the language is positional;
content-address reflects the order the author chose. Two sequences
with the same set but different order identify different versions.

### 3d. Cross-schema references hash by value

The encoder does not embed `signal-sema:Magnitude` as text. It
replaces the reference with `(SchemaRef <hash>)` where `<hash>`
is the Blake3 of `signal-sema`'s canonical encoding. Hash-by-value
means any change to `signal-sema` propagates to dependents — the
schema dep graph is fully content-addressable, top to bottom.
Hashes compute bottom-up from leaf schemas (no cross-deps) to
the daemon's component schema.

### 3e. Layout annotations sorted inside a block; hash function

Annotations canonicalise under NOTA rules, but the order *inside
a block* is NOT canonical — annotations sort alphabetically by
record-head identifier before encoding. So
`[(appendOnly) (discriminantWidth 1)]` and
`[(discriminantWidth 1) (appendOnly)]` hash identically.
Annotations are declarative facts, not an ordered sequence.
Hash function: Blake3, 32-byte / 256-bit output. Workspace
standard per /262/263; matches nota/README.md's
`#<64 hex chars>` canonical Blake3 form.

## 4. What the hash binds to — granularity

**Decision: the load-bearing hash is the per-component schema
hash.** This is the hash sema-upgrade compares, the hash the sema
database stores, the hash a daemon's binary commits to.
Per-record-type hashes are derived Merkle leaves; per-database
hashes don't exist (a database holds exactly one component's
records).

### 4a. Why per-component

Approach C (record 21, /270 §5) operates at the per-component
boundary. A daemon either can or cannot serve traffic; readiness
depends on the union of all record types. Storing per-record
hashes and asking "can the daemon serve?" requires AND-ing across
every record-type match — heavier and less honest than asking "is
the component's hash known?". /273 §2's type-family split
reinforces: per-component schema is the *union* of public-signal
records and private-storage wrappers. Per-record hashing loses
the union; per-component preserves it.

### 4b. Per-record-type hashes as derived Merkle leaves

Well-defined: Blake3 of the canonical encoding of one `Branch` or
`Leaf` with cross-schema refs resolved. The /263 diff classifier
produces these as it walks the tree to identify which subtree
changed. They do NOT need to be stored at row level; the plan
operates on schema text and recomputes per-record hashes on
demand.

### 4c. Merkle structure; no workspace root

```
Component hash
  ├── Declaration 1 hash
  ├── Declaration 2 hash (depending on D1 via cross-ref)
  └── … (one leaf per declaration)
```

If any leaf changes, the root changes — what record 29 wants.
The workspace has a graph of schemas (`signal-sema` ←
`signal-…` ← runtime); the design does NOT roll these into a
workspace-root. Sema-upgrade tracks per-component hashes; the
dep graph is implicit in §3d. A workspace-root would change on
every component change with no operational benefit.

## 5. Storage shape inside the sema database

**Decision: a single header table holding one row — the
schema-version hash for the component schema this database is
under.** Not embedded per-record; not a sparse metadata index.

### 5a. Why header table, not per-record prefix

Embedding the hash in every record multiplies storage cost; every
row carries the same 32 bytes; updates on schema change become a
full-table rewrite. A header table with one row keeps records
compact; the hash is read once at boot; sema-upgrade reads it
without touching working records.

### 5b. The schema_header table shape and lifecycle

```rust
// in <component>'s runtime crate
const SCHEMA_HEADER_TABLE: TableDefinition<&str, SchemaHeader> =
    TableDefinition::new("schema_header");

#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord)]
pub struct SchemaHeader {
    pub component: ComponentName,
    pub schemaVersionHash: SchemaVersionHash,
    pub recordedAt: Date,
    pub recordedAtTime: Time,
}

#[derive(NotaTransparent, ...)]
pub struct SchemaVersionHash([u8; 32]);
```

One row keyed `"current"` (or component name; operator detail).
Read on every boot before any working table opens. Written at
exactly two moments: database creation (first start ever) and
successful migration (sema-upgrade's MigrationCompleted updates
this row as the final step). Per-migration history lives in
sema-upgrade's own sema database, not in each component's
(record 71); the component's database only needs the current
hash. `schema_header` is NOT exposed through the working signal
contract; sema-upgrade reads via the protocol in §6, not by
opening the redb file.

## 6. Sema-upgrade-daemon's dispatch protocol

How does sema-upgrade-daemon at boot read another daemon's stored
hash and compare against that daemon's declared hash?

### 6a. Two hashes, two access paths

For each daemon D: **stored hash** is the `schema_header` row in
D's sema database (§5) — shape of data on disk. **Declared hash**
is the hash D's *current* binary commits to — shape D's running
code expects. Stored == declared → Proceed; stored != declared
with both registered → PlanRequired; stored unknown →
UnknownStoredAddress.

### 6b. How D's code declares its current hash

**The build emits a constant.** The schema-language toolchain
(generator from /263) runs at build time: reads the schema;
computes canonical encoding (§3); computes Blake3 (§3e); emits
the Rust types plus a constant:

```rust
pub const SCHEMA_VERSION_HASH: SchemaVersionHash =
    SchemaVersionHash::from_bytes([0xAB, 0xCD, /* … */]);
```

D's binary carries its declared hash at compile time; no runtime
schema parsing. Aligns with record 41: the Nix-pinned deployed
binary IS the declaration.

### 6c. How sema-upgrade reads D's stored hash — the inspect socket

**Decision: sema-upgrade does NOT open D's sema database
directly.** Triad invariant 2 forbids cross-daemon database opens
(/270 §9 Q1). The clean shape: D exposes its stored hash through
a Signal operation before binding its main working socket.

Three moves: (1) D's binary starts and binds a smaller **inspect
socket** (per-daemon, e.g. `<daemon-name>-inspect.sock`) — NOT yet
its working socket. (2) D sends `Inspect` to sema-upgrade with
component identity and its compile-time declared hash; D blocks.
(3) Sema-upgrade opens a one-shot client to the inspect socket,
sends `AskStoredSchemaHash`, gets
`(StoredSchemaHashReported (Component …) (Hash …))`, closes.

The inspect socket is a general primitive for "queries answered
before the daemon serves traffic." Other inspect-time queries
(binary version, build hash, configuration snapshot) compose
under it later.

### 6d. The full boot sequence

engine-manager brings up `sema-upgrade-daemon` first (per the
sema-upgrade boot-order intent — sema-upgrade is the first persona
daemon to start, owned by the engine manager), then each persona
daemon D. D binds its inspect
socket, reads its compile-time const, and sends `Inspect` to
sema-upgrade with component identity and declared hash.
Sema-upgrade opens a client to D's inspect socket, calls
`AskStoredSchemaHash`, gets stored hash, and replies:
- stored == declared → `Inspected(Proceed)`.
- stored != declared + migration registered →
  `Inspected(PlanRequired (StoredHash …) (DeclaredHash …))`.
  D waits; sema-upgrade negotiates owner approval; D continues
  after MigrationCompleted.
- stored unknown → `Inspected(UnknownStoredAddress)`. D halts;
  owner intervention.

On Proceed, D unbinds its inspect socket (or keeps it open for
ongoing introspection) and binds its main working socket.

### 6e. Why not just a startup library link?

/270 §9 Q1's alternative — sema-upgrade calls D's read-path
through linkage. /273 §4 designer lean was (2) in-process library.
Refining now: in-process library is right for **migration
execution** (heavy; only-during-migration; linkage-required).
Inspect socket is right for **hash discovery** (fast, cheap,
triad-invariant-preserving; no working data touched). Two paths
layered; different operational scopes.

## 7. Worked example — Entry end-to-end

### 7a. Schema declaration (`signal-persona-spirit/schema.nota`)

```nota
(Schema signal-persona-spirit
    [(Leaf Kind
        [Decision Principle Correction Clarification Constraint]
        [(discriminantWidth 1)])
     (Newtype Topic String)
     (Newtype Summary String)
     (Newtype Context String)
     (Newtype Quote String)
     (Branch Entry Struct
        [(topic Topic) (kind Kind) (summary Summary)
         (context Context) (certainty signal-sema:Magnitude)
         (quote Quote)]
        [])])
```

### 7b. Canonical encoding

The encoder strips comments, normalises whitespace, resolves
cross-schema refs to embedded hashes, sorts annotations. The
result (`#ab12…c4` is the Blake3 of `signal-sema`'s schema, 64
hex chars in real form):

```
(Schema signal-persona-spirit [(Leaf Kind [Decision Principle Correction Clarification Constraint] [(discriminantWidth 1)]) (Newtype Topic String) (Newtype Summary String) (Newtype Context String) (Newtype Quote String) (Branch Entry Struct [(topic Topic) (kind Kind) (summary Summary) (context Context) (certainty (SchemaRef #ab12…c4)) (quote Quote)] [])])
```

### 7c. Blake3 hash and storage

Blake3 over the canonical byte stream produces 32 bytes — call
the result `#ef34…a8`. The generator emits
`pub const SCHEMA_VERSION_HASH: SchemaVersionHash =
SchemaVersionHash::from_bytes([0xef, 0x34, /* … */ 0xa8]);`.
On first start, the daemon writes one row into `schema_header`:
`(SchemaHeader signal-persona-spirit (SchemaVersionHash #ef34…a8)
2026-05-22 13:45:00)`.

### 7d. Sema-upgrade comparison and migration trigger

Schema later changes (Certainty widens to Magnitude through the
sema-upgrade persona-spirit 0.1.0 → 0.1.1 migration); generator on
the new branch emits a different const — `#aa11…b3`.
New binary Nix-installed; on-disk `schema_header` still has
`#ef34…a8`. At boot: sema-upgrade-daemon comes up; spirit binary
binds inspect socket, sends
`Inspect((Component spirit) (DeclaredHash #aa11…b3))`;
sema-upgrade calls back and gets
`(StoredSchemaHashReported spirit #ef34…a8)`. The pair
`#ef34…a8 → #aa11…b3` is in the migration catalogue (registered
via `Register`); sema-upgrade replies `(Inspected (PlanRequired
…))`. Owner approves via `Allow`; sema-upgrade runs the plan
(in-process library call to spirit's per-record transform);
reports `MigrationCompleted`; spirit's `schema_header` updates
to `#aa11…b3`; spirit proceeds. After: sema-upgrade's
`migration_history` links the transition via the spirit transform
module; working tables match the new layout.

## 8. Open psyche questions

**8a. Semver as a human label alongside the hash?** §4 elevates
the hash to canonical identity; the layered option — semver as
wire-friendly label, hash as load-bearing back-stop — remains
viable. Designer lean: keep semver as a human label stored
alongside the hash in `schema_header`; hash is what sema-upgrade
dispatches on and migration registry keys by. Semver is
communication; hash is identity.

**8b. Where does the schema file live?** With §2h's visibility
annotation absorbing private types into the same file, designer
lean is **one schema file per component, in the runtime crate**
(natural home for both public and private types; generator's
output spans both crates).

**8c. Authored vs alphabetical declaration order.** §3c makes
authored order canonical. Alternative: alphabetical by name.
Authored preserves grouping conventions (leaves, newtypes,
branches, channel). Designer lean: authored; convention groups
by kind.

**8d. How sema-upgrade reaches D's inspect socket.** §6c assumes
sema-upgrade knows D's path. Two options: (a) convention —
`<daemon-name>-inspect.sock` at a known directory;
(b) engine-manager owns discovery. Designer lean: (a) first cut,
(b) when engine-manager's discovery surface stabilises.

**8e. Sema-upgrade's own schema-version hash bootstrap.**
Recursive. /270 §9 Q3 lean — hand-written path until contracts
stabilise, then dogfood once — applies. Psyche call on whether
the dogfood crossing is a shipping milestone.

**8f. Malformed header row.** A corrupted `schema_header` row
should produce a typed reply. Designer lean:
`Inspected(MalformedHeader (Reason …))`; D halts; owner
intervention.

## 9. References

**Intent records (spirit sema database).** 12 schema-in-NOTA
proposal; 21 Approach C; 29 schema-layout content-address
direction (founding for §3-§4); 30 rkyv-headroom; 41 Nix-flake
upgrade protocol; 42 no-tuples; 70 universal Magnitude (§7's
example); 71 sema-upgrade universal mechanism; 72 sema database
vocabulary; 73 branches/leaves; 101-103 prototype sequencing;
107 schema-version hash as canonical identity (this report
grounds).

**Designer reports.** /263 schema-spec language (direct
predecessor — §2 deepens); /269 universal Magnitude; /270
sema-upgrade design (§3-§5 wire surface; §6 refines via inspect
socket); /273 schema-migration synthesis (§2h's visibility
annotation absorbs). Approach C (originally /260), the
version-surface research (/261), the /262 predecessor, and the
spirit upgrade test (/265) are all dropped; their substance is
absorbed into intent record 21 + the content-address direction
(§4 of this report) + /273 + /278.

**Workspace artefacts.** `ESSENCE.md`; `skills/nota-design.md`
three rules + grammar facts; `skills/language-design.md`
(esp. 9 content-addressing, 18 delimiters earn their place);
`skills/naming.md`; `skills/component-triad.md` (§6e in-process
library vs cross-database open).

**External.** `nota/README.md` — grammar + canonical-form rules
(§3a inherits); `signal-persona-spirit/src/lib.rs` (master) —
concrete shape used in §7; `signal-sema/src/magnitude.rs` —
Magnitude declaration referenced from spirit's schema.
