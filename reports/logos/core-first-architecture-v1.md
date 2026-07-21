# Core-first recrystallization of the language stack — v1

Retired vocabulary (psyche ruling 2026-07-21): "mouth" -> textual interface; "organs" -> the two trees (nametree, structuretree); "spine" -> core invariant / core pathway; "door" -> entry point; "currency" -> value type. Historical text below is unreworded; read it through this table.

A deep architecture audit and recrystallization of the next-generation language
stack (NOTA → schema → Nomos → Logos → generated Rust → rustc), re-centered on
the psyche's **Core-first** principle: the strictly-typed true-binary
(rkyv-portable) in-memory/in-database representation — historically named **sema**
— is the essential substance of the language-system; **text is a bootstrap
bridge** for viewing, LLM interaction, and bootstrap compiling until in-daemon
Core editing/snapshotting/version-control and predictable programmatic
format-upgrading are developed well enough that text becomes viewing-only.

Written 2026-07-14 (session `nextgen-recrystallization`, lane
`core-first-architecture`). Read-only on all code repositories; the one artifact
this lane writes is this file.

"Recrystallization" means: re-derive the cleanest architecture from the psyche's
confirmed rulings, allowing any magnitude of rewrite. Current implementation is
**evidence, not a constraint**; psyche rulings **are** constraints. Where a
finding would conflict with a ruling it is surfaced as an explicitly-marked
proposed reversal with cost/benefit, never silently overridden.

Provenance discipline, as in the sibling `design-v0.md` / `architecture-v0.md`:

- **[psyche ruling — cite]** — a settled decision.
- **[observed — cite]** — a worker-verified fact about the current code, cited to
  a scout's file:line reading this session.
- **[interpretation]** — my reading; not the psyche's words.
- **[AGENT PROPOSAL]** — a recommendation on an open question, collected in §5.

## 0. The one-paragraph thesis

Across the whole stack the **implemented** primary is TEXT and the Core/binary
form is aspirational-or-derived — the exact inverse of the ruling. The single
substrate that already embodies Core-first is **sema-engine**: rkyv values at
rest, blake3-over-rkyv content addressing, a versioned hash-chained log as the
authoritative source of truth with the store as a rebuildable view, and real
layout-version upgrade machinery. The name "sema" for that engine is precisely
the psyche's point made concrete — the *database* already treats true-binary as
the substance, and the *language front-end* (nota, schema) has not caught up. The
recrystallization is therefore not an invention from scratch: it is **lifting the
Core discipline that sema-engine already proves up into nota, schema, Nomos, and
Logos**, and demoting text and named views to edge projections everywhere.

## 1. Core-first audit — where text is treated as primary

Deliverable 1. Each finding separates observation (cited to this session's
scouts) from interpretation.

### 1.1 NOTA — the codec is built around text, rkyv is an unexercised bolt-on

**[observed — nota `origin/next-gen` `08ce05c`, nota 0.8.0 / nota-derive 0.4.0]**
The only structural type is `Block` (`src/parser.rs:57-80`:
`Delimited`/`Application`/`PipeText`/`Atom`) — a **syntax tree over text**, not a
typed value model. The two load-bearing codec traits (`src/codec.rs:119-125`) are
`NotaDecode::from_nota_block(&Block)` and `NotaEncode::to_nota() -> String`. There
is **no** canonical in-memory `Value`/`Record`/`Core` sum type anywhere;
`src/lib.rs` exports none.

**[observed]** rkyv is a dependency (`Cargo.toml:17`, 0.8, `default-features =
false`) and is derived on exactly two byte-sequence helpers plus the macro-data
types in `src/macros.rs`, **but there are zero `rkyv::to_bytes`/`from_bytes`/
`access`/`deserialize` call sites in the entire repo** — the rkyv capability is
derived and never exercised. `nota-derive` generates **only** the text codec
(`NotaDecode`/`NotaEncode`/`NotaDecodeTraced`/`StructuralMacroNode`); it has zero
rkyv codegen (`derive/src/lib.rs`, `grep -c rkyv` = 0). Tests are text
round-trip only (`tests/codec.rs`, `tests/next_gen_grammar.rs`); **no binary
round-trip is tested**. There is **no hashing/content-addressing code of any
kind** in nota (over text or binary).

**[observed]** `ARCHITECTURE.md:432-466` ("Binary boundary") states the
Core-first direction — "rkyv binary is the single encoded form, living both in
the database as the SEMA body at rest and on the wire" via one `AssembledSchema`
reading those bytes in both places — but **`AssembledSchema` does not exist as a
type** (zero `.rs` hits; prose only, Spirit-tagged as intent).

**[interpretation]** NOTA's implemented substance is the text-AST↔Rust-struct
bridge. The Core (rkyv-portable binary as the true representation) is
prose-and-derives, not a tested reality. This is the deepest text-primary
inversion in the stack, because NOTA is the substrate every other language sits
on.

### 1.2 schema — CoreSchema and NameTable do not exist; TrueSchema (named) is the stored primary

**[observed — schema repo, TrueSchema-model branch, `36a79b7`]** `CoreSchema`
**does not exist** (zero `rg` hits in `src/`). `NameTable` **does not exist**
(zero hits; one aspirational prose mention at `schema-rust/ARCHITECTURE.md:525`).
`TrueSchema` (`src/schema.rs:464`) is the real, pervasive type and is **not
stringless**: its identifiers are `Name(String)` (`schema.rs:14`) embedded
verbatim in every declaration — no index/table indirection.

**[observed]** The load pipeline is text-in as the **sole** entry point:
`fs::read_to_string` (`module.rs:157`) → parse NOTA (`source.rs:36`) →
`lower_schema_source` → `TrueSchema` (`module.rs:211-214`). No internal
round-trip through text mid-compile was found (`to_schema_text` is export/test
only). rkyv exists (`schema.rs:453-462,1064-1071`
`to_binary_bytes`/`from_binary_bytes`) but only as a post-hoc serialization of the
already-built **named** value.

**[interpretation]** TrueSchema today is conflated: it is simultaneously the
stored primary and the named view. The Core-first ruling wants those split
(stringless CoreSchema as substance, TrueSchema as projection). Neither the Core
type nor the NameTable exists yet — this is a large gap, not a small one.

### 1.3 Identity/hashing — hashed over rkyv bytes (good) but over the *named* form (wrong pre-image)

**[observed — schema `src/identity.rs:70-75,158-165`]** `TrueSchema::content_hash`
is **blake3 over the canonical rkyv bytes** of the value, domain-separated
(`HashDomain::TrueSchema`), explicitly **not over `.schema` text** — so
whitespace/comment edits do not move the address. This is genuinely Core-ish: the
hash pre-image is binary, not text bytes.

**[observed]** But the pre-image is `TrueSchema`, whose `Name(String)` identifiers
are in those bytes, so **a pure rename moves the content hash** — the opposite of
the stringless-Core, rename-stable identity the ruling describes.
**[observed — `signal-schema/ARCHITECTURE.md:8-12`]** the codebase itself names
this gap: the current scaffold "does not present the current string-bearing
`TrueSchema::content_hash()` as the final core hash" and defers the final
`CoreTrueSchema` model.

**[interpretation]** Identity is half-migrated: the hash correctly folds binary,
not text — but folds the *named* binary. The fix is a pre-image change (Core, not
True), not a hashing-mechanism change. See decision 2.

### 1.4 signal-schema — rkyv frames (good) carrying text payloads (the leak)

**[observed — `signal-schema/src/schema/lib.rs`]** The wire uses **rkyv typed
frames** (`encode_signal_frame`/`decode_signal_frame`, 8-byte header;
`Frame = ExchangeFrame<Input,Output>`), NOTA only as an optional
`#[cfg(feature="nota-text")]` projection. Good so far. But the operation
**payloads are text**: `LoadPackage` carries `SchemaText`; `EmitRust` returns
`RustText`. There is **no** slot-listing, **no** hash-addressed fetch, and **no**
CoreSchema/NameTable exposure of any kind — only `LoadPackage` (push text in) and
`EmitRust` (pull text out).

**[interpretation]** The frame is binary but the semantics are text — the daemon
is handed text to parse and hands text back. Core-first requires the payloads
themselves to be Core (CoreSchema + NameTable), with Rust text remaining text
only at the final rustc-facing edge where text is legitimate.

### 1.5 schema-rust — the oracle is byte-exact Rust *text*, input is the *named* IR

**[observed — schema-rust `main` `87de872`]** Token-based emitter
(`proc_macro2` + `quote`, one `prettyplease` pass per item, every item
`#[rustfmt::skip]`; `src/lib.rs:5032-5036,36-58`). Top-level input is
`TrueSchema` (`emit_*_from_true_schema`, `src/lib.rs:84-102`). Goldens
(`tests/fixtures/*generated.rs`, 9 files, ~9000 lines from 23 `.schema`
fixtures) are compared **byte-exact text-vs-text** via a homegrown `assert_eq!`
harness with a `SCHEMA_RUST_UPDATE_FIXTURES` self-write hatch
(`tests/emission.rs:21-28`); the same goldens double as **compiled modules
exercised at runtime**. No mid-pipeline text round-trip; text only at the two
edges.

**[interpretation]** Byte-exact Rust-text goldens are **correct and should
stay** — Rust text is the legitimate bridge to rustc, so the oracle lives at the
one edge where text is truth. The issue is only that the emitter's *input* is the
named `TrueSchema`; under Core-first the input becomes CoreLogos (or CoreSchema
projected), while the golden Rust output must not move — which is exactly what
makes the goldens a clean gate for the whole migration.

### 1.6 sema-engine — already Core-first; the model to lift upward

**[observed — sema-engine `main` `fa3a822`]** rkyv is the stored-value form
(`src/record.rs`, `EngineStoredValue: rkyv::Archive + …`, features
`little_endian`, `pointer_width_32`, `unaligned`, `bytecheck` — portable,
validated-on-read). The **versioned hash-chained append log is the authoritative
source of truth; the redb store is a rebuildable materialized view folded from
the log** (`ARCHITECTURE.md:26-30`). blake3-over-rkyv content addresses
**checkpoint segments** (`src/checkpoint.rs`, `SegmentDigest`) and forms the
tamper-evident payload digests (`versioning.rs:340-350`, pre-image = rkyv bytes).
**Layout-version upgrade machinery is real and implemented** (storage layout v5,
staged 2→3→4→5 upgrade-at-open that re-folds the log and verifies the digest
chain; `ARCHITECTURE.md:96-116`). The engine is schema-aware (family
registration with per-family `SchemaHash`).

**[observed]** Record **lookup** identity is `RecordKey` (a domain string or an
engine-minted monotonic `RecordIdentifier(u64)`; `record.rs:59-62`), **not** a
content hash. And the **successor stored-record identity basis is explicitly
open** — HEAD's own commit notes the family-closure hash was retired and "the
successor identity basis for stored records is not yet chosen; pending the
`sema.schema` document-kind design session."

**[interpretation]** sema-engine is the working proof of every mechanism the
psyche wants for daemon-resident Core editing: log-as-truth, content-addressed
snapshots, rebuildable views, mechanical format-upgrade. The recrystallization
should make the language daemons **sit on this engine** rather than reinvent it,
and the open record-identity question is the same question as the schema Core
hash (§1.3) — they should be answered together.

### 1.7 Audit verdict

The stack is text-primary at the front (nota, schema, signal-schema payloads) and
Core-first only at the back (sema-engine). The named view (`TrueSchema`) is
conflated with the stored substance. The content hash folds binary but the
*named* binary. The recrystallization inverts all of this: **Core is the one
stored substance; names and text are always projections.** That inversion is the
central beauty claim — today's special cases ("sometimes text is truth, sometimes
a view; sometimes we hash names, sometimes not") dissolve into one normal case.

## 2. Recrystallized architecture — Core-first

Deliverable 2. The cleanest design derivable from the rulings.

### 2.1 Core type shapes for all three languages

Three stringless cores, one discipline:

- **CoreSchema**, **CoreNomos**, **CoreLogos** — every identifier is an
  `Identifier(u32)` index into a NameTable; the core carries **no strings**. Each
  derives `rkyv::{Archive, Serialize, Deserialize}` under the **exact portable
  feature set sema-engine already uses** (`little_endian`, `pointer_width_32`,
  `unaligned`, `bytecheck`) so a Core value is a portable, validated-on-read
  archive identical in discipline at rest and on the wire.
- **NameTable** — `Identifier -> Name`, interned, append-only. **One continuous
  NameTable spans schema→logos**: the logos NameTable is an *extension* (higher
  indices appended) of the schema NameTable, so a carried-over schema identifier
  keeps its exact index inside CoreLogos. This realizes the psyche's "continuous
  identifier space; logos re-uses the same ID→name allocation and extends it."
  **[psyche ruling — design-v0 §2]**
- **TrueSchema / TrueNomos / TrueLogos** — the **named projection** =
  `CoreX + NameTable` resolved. **Not stored; derived on demand** for viewing and
  text. This is the inversion of today, where TrueSchema is the stored primary
  (§1.2). The named types survive as *views*, not truth.
- **Text** — a codec at the edges only (§2.4). NOTA's `Block` becomes strictly the
  parse/print form of the text bridge, not the internal substance.

**rkyv portability discipline.** The Core is the single encoded form at rest
(daemon store) and on the wire (signal frames) — the `AssembledSchema` intent
(§1.1) made real: one Core type read from rkyv bytes in both places. Layout
changes to any CoreX are **versioned** (decision 3), never silent refactors —
matching the `rust-storage-and-wire` rule that reordering fields or changing
archive feature sets is a coordinated storage-schema change.

The `NotaDecode`/`NotaEncode` traits stay, but are re-seated as the **text bridge
codec**; the **primary codec is rkyv**, and nota must actually exercise a binary
round-trip (today zero call sites, §1.1). This is the concrete nota rewrite: make
the derived-but-dead rkyv path the tested truth and demote text to projection.

### 2.2 Content addressing and identity

- **Hash over the stringless Core rkyv bytes.** `content_hash(CoreX)` = blake3
  over `CoreX`'s canonical rkyv bytes, domain-separated per language and **tagged
  with the Core layout version**, with the **NameTable excluded** from the
  pre-image. Reuse schema `identity.rs`'s existing blake3-over-rkyv derive and
  sema-engine's `ContentHash::derive(HashDomain, bytes)` pattern verbatim; only
  the **pre-image changes from TrueSchema to CoreSchema**.
- **Rename-stability falls out for free.** Because names live in the NameTable and
  not in CoreX, a rename is a NameTable-only edit that **does not move the Core
  hash**. Structural edits (add field, change type, add variant) change CoreX
  bytes and do move it. This is exactly schema-rust's stated "target evolution
  model" (`ARCHITECTURE.md:525`): a `Rename` touches only the NameTable and emits
  no migration; structural edits change core bytes and emit historical→current
  `From` impls.
- **Stability across format upgrades.** The hash is over the *current* Core
  layout's bytes, so a Core-layout change moves the hash by construction; the
  layout-version tag in the hash domain makes this explicit and the format-upgrade
  (decision 3) re-derives the address under the new layout deterministically. So
  identity = "hash of stringless Core at layout version V"; upgrading V is a
  deterministic re-fold, not an ad-hoc re-hash.

This directly retires the disclaimed provisional hash (§1.3) and is the natural
unifying candidate for sema-engine's open stored-record identity basis (§1.6,
decision 6).

### 2.3 Daemon-resident editing as the eventual primary interface

The end-state the psyche describes — in-schema-daemon and in-nomos/logos-daemon
editing, snapshotting, version-control, and predictable programmatic
format-upgrading, with text merely for viewing/LLM interaction — is **built by
seating each language daemon on sema-engine**, whose mechanisms already exist:

- **Editing operates on Core, not text.** An edit is a typed operation over
  `CoreX + NameTable` — `AddField`, `ChangeFieldType`, `AddVariant`, `Rename`, … —
  mirroring sema-engine's `VersionedLogOperation` and schema-rust's target
  structural-edit vocabulary. The daemon never reconstructs owned state by parsing
  its own text projection (`rust-storage-and-wire`: the daemon keeps the typed
  value as truth and regenerates projections).
- **Snapshotting + version control = sema-engine's versioned hash-chained log,
  reused wholesale.** Each daemon owns a sema-engine store; the log of edit
  operations *is* the version control; each commit is content-addressed
  (decision 2); the redb/materialized view is the rebuildable projection. This is
  already implemented; the language daemons register CoreSchema/CoreNomos/
  CoreLogos families and inherit snapshotting, checkpointing, and log-replay for
  free.
- **Predictable programmatic format-upgrade** models the Core-layout upgrade on
  sema-engine's implemented storage-layout upgrade (v2→5): an upgrade-at-open that
  deterministically re-folds old Core into the new Core layout, verified against
  the digest chain, emitting historical→current `From` impls for structural
  changes and no migration for NameTable-only renames (decision 3).

### 2.4 Text codecs as pure projection at the edges

Text has **no semantic authority**. The nota-text↔CoreX codec is used at exactly
three edges: **authoring** (human/LLM writes text → parse → CoreX), **viewing**
(CoreX → pretty-printed text, the projection with the `.`→`::` translation and
re-sugaring owned here), and **bootstrap compiling** (until in-daemon Core editing
matures). Consequences:

- The entire **delimiter reshuffle** (`{}` structs / `[]` vectors / `()`
  payloads), dotted variants, `Map.( key.Value … )`, and the optional-paren string
  rule are **text-bridge concerns with zero Core-identity impact** — they change
  how CoreX is parsed and printed, never CoreX bytes or hashes. This de-risks the
  reshuffle: it cannot destabilize content addresses.
- signal payloads stop being text (§1.4): `LoadPackage` carries CoreSchema +
  NameTable, not SchemaText. The **one legitimate text output is generated Rust**,
  because rustc consumes text — so the schema-rust byte-exact Rust goldens remain
  the right oracle at the right edge (§1.5).

### 2.5 The three-component spine, Core-first

Each of schema, Nomos, Logos is a daemon owning its CoreX store (sema-engine
versioned log + materialized view) and its slice of the continuous NameTable, and
exposes on its `signal-<component>` surface: **slot-listing** and
**hash-addressed fetch** over stringless Core bytes, plus its conversion
entry-points. **[psyche ruling — design-v0 §22,23]**

- **schema daemon** (existing stack, Core-ified): serves `CoreSchema + schema
  NameTable` by hash; gains slot-listing, hash-fetch, and the `convertToLogos`
  push entry-point (none exist today, §1.4).
- **Nomos** (new): consumes `CoreSchema + NameTable`, produces `CoreLogos + logos
  NameTable` by extending the allocation; the conversion **is** the macro system
  (named + structural macros; `nomos-macro-model-v1.md`). Carries slot-listing +
  hash-fetch. Conversions move Core serialized on rkyv frames, **outside text**.
- **Logos** (new): receives serialized CoreLogos, holds/serves it, owns the text
  projection and (eventually) the Rust lowering.

Both **pull** (logos-side lists schema slots, drives conversion) and **push**
(schema `convertToLogos` chains through Nomos) topologies are first-class.

**The Nomos at-rest question — designed, flagged for ruling (decision 1).**
Slot-listing implies Nomos holds loaded state, so Nomos is designed **stateful**:
a CoreNomos macro-package store, sema-engine-backed like the others; macro
packages are authored in nomos text → parsed to CoreNomos → stored; slot-listing
enumerates loaded packages. This is the symmetric, beautiful shape (all three
daemons identical in kind), but the psyche has not explicitly ruled
definitions-at-rest — it stays a proposal (design-v0 §8 open).

### 2.6 The staged bootstrap path, goldens as oracle at every stage

The Rust output edge never moves; the schema-rust byte-exact goldens gate every
phase. **[psyche ruling — design-v0 §4]**

- **Phase 0 (today):** schema text → TrueSchema → schema-rust → Rust text; goldens
  = byte-exact Rust. Keep.
- **Phase A — Core-ify NOTA:** introduce the canonical binary Core discipline and
  a tested rkyv round-trip; re-seat text as projection. *Proves* the Core/text
  inversion at the substrate. *Oracle:* existing nota text round-trips stay green
  **plus** new binary round-trip tests.
- **Phase B — Core-ify schema:** CoreSchema + NameTable become the stored primary;
  TrueSchema becomes a derived projection; the content hash pre-image moves to
  CoreSchema. *Proves* rename-stable identity and text-as-projection at the schema
  layer. *Oracle (sharp):* schema-rust goldens stay byte-exact — the emitter now
  takes CoreSchema (projected to the named view it needs) and the Rust output must
  not move.
- **Phase C — build Nomos + Logos:** CoreNomos/CoreLogos, both topologies, all
  three slot-listing + hash-fetch surfaces; Nomos produces CoreLogos from
  CoreSchema + NameTable over Core, outside text. *Proves* conversion-over-Core.
  *Oracle:* macro-produced CoreLogos lowers to the same Rust the goldens hold.
- **Phase D — Logos becomes THE Rust generator:** harvest schema-rust's
  token lowering as the fixed hosted kernel; retire schema-rust emission; dialects
  become CoreNomos macro packages (self-hosting). *Oracle:* goldens byte-exact
  through the new producer.

sema-engine underpins each daemon's Core store and versioned editing throughout.

## 3. Rewrite-magnitude map

Deliverable 3. Honest accounting; the psyche authorized any magnitude.

**Survives as-is / near-as-is:**

- **sema-engine** — survives and becomes *more* central: the Core substrate for
  all three language daemons. Its versioned log, content-addressed checkpoints,
  and layout-upgrade machinery are exactly the daemon-resident editing/versioning/
  format-upgrade the psyche wants. Change: register the three Core families; adopt
  the Core hash as the successor record-identity basis (decision 6). Low code
  cost, high leverage.
- **schema-rust emitter** (token-based quote/prettyplease machinery) — survives as
  the Phase-0 oracle and the harvest source for the Phase-D fixed Rust kernel. Its
  *input* eventually shifts from TrueSchema to CoreLogos, but the emission
  machinery and every golden are reused. Its goldens survive unchanged as the
  cross-phase gate.
- **signal-frame / rkyv wire discipline** — survives unchanged.
- **nota raw parser** (`Block`/`Application`/`Atom`, dotted binding) — survives as
  the text-bridge parser; its *role* demotes from "the codec" to "one edge codec."

**Gets rewritten:**

- **nota codec's center of gravity** (medium-large) — introduce the canonical
  binary Core value, make rkyv the tested primary round-trip (today derived but
  never called), build the real `AssembledSchema`-equivalent, re-seat
  `NotaDecode`/`NotaEncode` as the projection. nota-derive gains rkyv-primary
  codegen awareness.
- **schema core type** (large) — CoreSchema (stringless) + NameTable as the stored
  primary; `Name(String)` embedded pervasively (`schema.rs:464` and throughout)
  becomes `Identifier(u32)` + NameTable; TrueSchema demotes to a derived
  projection; `identity.rs` content-hash pre-image moves to CoreSchema; the
  `module.rs` load path gains a NameTable allocator. This touches the most code of
  any single component.
- **signal-schema** (medium, regenerated) — replace text-payload ops
  (`LoadPackage{SchemaText}`, `EmitRust{RustText}`) with Core-bearing ops plus
  slot-listing and hash-fetch of CoreSchema + NameTable.

**Gets built new:**

- **CoreNomos + Nomos component** (daemon + `signal-nomos` + macro-package store).
- **CoreLogos + Logos component** (daemon + `signal-logos` + text projection +
  eventual Rust lowering).
- The **continuous NameTable extension** mechanism (schema→logos).
- The **Core-layout format-upgrade** mechanism for the language cores, modeled on
  sema-engine's storage-layout upgrade.

**Gets deleted / demoted:**

- **nexus / nexus-cli** — already deleted on the psyche's order (nexus was only
  ever his concept-name for a daemon's internal-operation IO types; the repos were
  agent fabrications). Carried as fact, not re-planned.
- The **framing of TrueSchema/TrueLogos as stored primaries** — demoted to derived
  projections (types survive as views).
- Any assumption that **text is the transport or identity basis** — removed at
  every layer except the generated-Rust output edge.

**Where the oracle gates:** every phase must reproduce
`schema-rust/tests/fixtures/*generated.rs` byte-for-byte. Phases B and C are the
sharp gates (the Rust output must not move while the input substance changes).

**Infrastructure fact to carry, not solve (deliverable 5):** the Nix substituter
`nix.prometheus.goldragon.criome` is **down**, blocking formal `nix flake check`.
Per the `testing` doctrine, durable test evidence in this workspace is
Nix-owned (flake checks / named check derivations); with the substituter down,
each phase's byte-exact golden `cargo test` is **inner-loop evidence only** and
the durable flake-check evidence is gated until the substituter returns. This
gates *evidence*, not design. Do not attempt to fix it.

## 4. Design-quality note (the beauty gate)

The recrystallization's central claim is that Core-first is not merely the
psyche's preference but the *beautiful* shape: today's forced special cases —
TrueSchema being both truth and view, the hash folding named binary, text being
sometimes-truth-sometimes-projection, sema-engine Core-first while the front-end
is text-first — all **dissolve into one normal case**: Core is always the
substance; the NameTable and text are always projections; identity is always the
hash of stringless Core; format-upgrade is always a deterministic re-fold. The
one substrate that is already beautiful (sema-engine) becomes the template the
rest is recrystallized to match. If a constraint forced a language daemon to keep
text as truth, that would be the ugliness to surface — none does.

## 5. Decision points requiring psyche ruling

Deliverable 4. Each carries an [AGENT PROPOSAL] with rationale. Decisions 1–4 are
recommended for resolution now; decisions 5–7 are parked on the psyche's desk —
the option space is analyzed but deliberately **not resolved**.

**Decision 1 — Nomos at-rest state.** *(design-v0 §8, still open; slot-listing
leans stateful.)*
**[AGENT PROPOSAL]** Nomos is **stateful**: a CoreNomos macro-package store,
sema-engine-backed exactly like schema and logos, authored in nomos text → parsed
to CoreNomos → stored; slot-listing enumerates loaded packages; convert requests
name a loaded package. Rationale: ruling 23 gives all three daemons slot-listing,
and a daemon that lists its slots holds loaded state; the stateful shape makes all
three components identical in kind (the symmetric, beautiful shape) and lets Nomos
reuse sema-engine's versioned store for free. The alternative (dialect package
travels in each convert request, Nomos stateless) cannot serve a slot-listing
operation coherently. Needs the psyche's explicit word because he ruled
slot-listing but not definitions-at-rest.

**Decision 2 — Hash basis for content addressing.**
**[AGENT PROPOSAL]** blake3 over the **stringless Core (CoreX) rkyv bytes**,
domain-separated per language and tagged with the Core layout version, with the
**NameTable excluded** from the pre-image. Rationale: realizes the psyche's
Core-first, rename-stable identity (a rename is a NameTable-only edit that does
not move the Core hash); reuses schema `identity.rs` and sema-engine
`ContentHash::derive` unchanged except for the pre-image; and directly retires the
provisional `TrueSchema::content_hash` that `signal-schema/ARCHITECTURE.md`
already disclaims as non-final. This is the keystone decision — decisions 3, 4,
and 6 all lean on it.

**Decision 3 — Format-upgrade mechanism shape.**
**[AGENT PROPOSAL]** Model the language Core-layout upgrade on **sema-engine's
already-implemented storage-layout upgrade** (v2→3→4→5): an upgrade-at-open that
deterministically re-folds old Core bytes into the new Core layout, verified
against the versioned-log digest chain, emitting historical→current `From` impls
for structural changes and **no** migration for NameTable-only renames. Rationale:
sema-engine ships working layout-upgrade code (`ARCHITECTURE.md:96-116`) and
schema-rust `ARCHITECTURE.md:525` already names this exact `From`-emission target;
adopting it makes format-upgrade "predictable and programmatic" as the psyche
requires, with a proven precedent rather than a new mechanism.

**Decision 4 — Where NameTables live at rest.**
**[AGENT PROPOSAL]** The NameTable is a **first-class stored sibling of CoreX in
the same daemon store** (its own sema-engine family), versioned in the same log,
so a rename is a NameTable-only commit. The **logos NameTable is stored as an
append-extension keyed to the schema NameTable's identity**, keeping the
identifier space continuous across schema→logos. Rationale: names must survive
daemon restart without re-parsing text (text has no authority); co-versioning Core
and names in one log keeps snapshots atomic while keeping them separable (rename =
NameTable-only edit, decision 2); and the extension-keying is what makes a
carried-over schema identifier resolve identically inside CoreLogos.

**Decision 5 — PARKED: the unit of "one schema" in the daemon, and split/merge
identity semantics.** *(design-v0 §8.1 bootstrap Q1, untouched; do not resolve.)*
Option space only: (a) one schema = one loaded package (LoadPackage granularity);
(b) one schema = one namespace / document-kind whole; (c) one schema = one
continuous-NameTable allocation. Split/merge then either mints fresh Core
identities for the products or preserves per-declaration nominal identities and
unions NameTables on merge. Decision 2's Core hash bears on this (it fixes *a
declaration's* identity but not *a schema's* boundary), but the boundary question
is the psyche's. **Not resolved here.**

**Decision 6 — PARKED: sema.schema document-kind and sema-engine's successor
stored-record identity basis.** *(Explicitly open in sema-engine HEAD; blocked on
the sema.schema design session; do not resolve.)* Option space: (a) per-family
`SchemaHash` (current stopgap); (b) per-declaration nominal-identifier + core-hash
machinery (schema-language's retired family-closure successor); (c) the stringless
CoreSchema content hash from decision 2 as the unifying basis. Decision 2's Core
hash is the natural candidate to unify record-identity with schema-identity, but
whether the engine adopts it is the psyche's call and is coupled to the sema.schema
document-kind design. **Not resolved here.**

**Decision 7 — PARKED and LOST: bootstrap question 2 must be restated by the
psyche.** *(design-v0 §8.1: the question was lost to handover corruption; only its
opening survives — "how do text edits become daemon edits…".)* The
recrystallization gives the *shape* of where the answer lands — the typed
Core-edit-operation vocabulary of §2.3 (`AddField`/`Rename`/…) is the mechanism by
which a text edit is parsed into a Core edit and committed to the daemon log — but
**the psyche's original question is unrecoverable and must come from his memory**;
no worker should reconstruct it.

**Carried lower-order proposals (from architecture-v0, still agent proposals, not
re-opened here):** Nomos/Logos as kameo daemons with signal/nexus/sema planes
(P2 — yes, copy the spirit triad); Logos→Rust as a Logos-daemon plane vs a fourth
component (P3); the exact signal verb sets (P6); the rustc-diagnostic source-map
from generated Rust → logos node → schema identity (P8); and the possible fourth
Nomos escape "name synthesis / realize-into-name-position"
(`nomos-macro-model-v1.md` §3). The Core-first design **resolves former P5** (logos
storage engine) toward **sema-engine-backed for all three daemons**, since Core
editing/versioning/format-upgrade all require the durable log rather than an
in-memory slot store.

## 6. Sources

Design corpus (this workspace): `reports/logos/architecture-v0.md`,
`design-v0.md`, `nomos-macro-model-v1.md`, `delimiter-semantics.md`,
`nota-grammar-revision-v0.md`, `reports/codex-rust-construct-survey.md`,
`reports/schema-redesign-port-readiness-scout.md`.

Code ground truth (read-only this session, cited inline in §1): nota
`origin/next-gen` `08ce05c` (0.8.0 / nota-derive 0.4.0); schema TrueSchema-model
branch `36a79b7`; signal-schema `e8f06cf`; schema-rust `main` `87de872`;
sema-engine `main` `fa3a822`. Repositories under `repos/` are untracked; no code
was edited and no branches were switched.
