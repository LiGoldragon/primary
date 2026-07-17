# Schema-unit and split/merge lineage — design v1

> **SUPERSEDED 2026-07-17 by `schema-unit-lineage-design-v2.md`.** The psyche
> engaged this v1's chat summary and ruled, and his rulings **delete machinery**.
> The identity keystone survives (identity is an allocated ID, not a derived
> fingerprint), but v1's surrounding apparatus is REMOVED, not deferred: the
> `DocumentLineage` origin DAG (§6), the receipts / multi-authority residual (L2
> revision trigger, O2), the rename-intent alias (§5, L4), and "move" as a distinct
> primitive. The unit is re-seated from the **document** (§2) onto the
> **schema-whole** — the document is a legacy view. v1's open questions O1-O4 are
> all resolved or dissolved by the keystone (see v2 §9). Read v2 as authoritative;
> this file is kept only as superseded history.

The design specification bead **primary-56d1.11** needs: the unit of "one schema"
and its split/merge identity semantics, drafted to the point the psyche can grade
it. Written 2026-07-17, session `LanguageFamilyDesign`, lane
`SchemaUnitLineageDesign`, generalist, Opus 4.8 (1M). Read-only on every engine
repo; this file plus the chat return are the lane's only artifacts. The psyche
does not read reports — the chat return carries the graded decision summary
self-contained; this file is the durable agent pickup point.

## 0. Provenance markers

- **[ruling]** — a settled psyche decision this design must conform to.
- **[observed — cite]** — a code fact from this lane's reconnaissance of the
  delivered engine (`repos/sema-storage`, `repos/signal-sema-storage`, and their
  dependency checkouts), with file:line.
- **[lean]** — an explicit revisable design lean, NOT psyche-graded; each carries
  a revision trigger, collected in §8.
- **[open]** — needs the psyche's word; collected in §9.
- **[interface]** — a surface handed to a sibling bead without preempting it.

## 1. The settled basis, and the one reframe that dissolves the question

**Settled rulings this design conforms to** (not reopened): a single logical
allocation authority per sema deployment, seated centrally in sema, daemons as
clients leasing identifier blocks [ruling, psyche verbatim 2026-07-17 "yes, seat
it centrally in sema"]; coordination-freedom rejected [ruling]; stringless Core,
names interned in NameTables, renames never touch a value [ruling]; Core identity
excludes NameTables, domain-separated, layout-versioned hashing, stable across
renames [ruling]; visibility is Schema-authoritative, `Core*` naming keeps, "sema"
names the durable storage/runtime component [ruling].

**The reframe.** "What is the unit of one schema, and how does it survive edits,
split, and merge" reads as one hard question only while two different identities
are conflated. They are already distinct — and, crucially, **already both present
in the delivered engine**:

1. A **content fingerprint** — `ContentHash` — a BLAKE3 derivation over the
   stringless Core structural bytes, NameTable excluded [observed —
   `signal-sema-storage/src/lib.rs:280-309`, every variant drops `names`;
   `name-table/src/identifier.rs:6-9` states the intent: "a rename can never move
   its content identity"]. This is a *derivation*, not an allocation. It **moves
   on every semantic edit**. It is therefore the identity of one *revision* of a
   schema, never the identity of "the schema" across its edit history. This is the
   git-blob / Unison-definition / IPFS-CID property — the partition-proof spine.

2. A **durable handle** — `DocumentKey { scope: FixtureScope, kind: DocumentKind,
   slot: SlotIdentifier }` plus a monotone `Version(u64)` [observed —
   `signal-sema-storage/src/lib.rs:68-72, 328-334`]. This is *allocated*, not
   derived. It is **stable across edits** — an edit advances `Version` and moves
   `ContentHash` under an unchanged `DocumentKey`. This is the git-ref / IPNS
   mutable-pointer property.

Once these are named apart, the whole bead dissolves into: **identity-of-a-schema
lives in the allocated `DocumentKey`, not in the derived `ContentHash`.** The rest
of this design is that sentence worked through split, merge, rename, and lineage,
using the delivered shapes.

The central authority is likewise already seated: `SemaPlane` co-stores a
`StorageRecord::Allocator { scope: FixtureScope, next: u32 }` counter per scope and
leases half-open `IdentifierBlock { first, length }` ranges by bumping `next`
[observed — `sema-storage/src/lib.rs:28-40, 185-219`]. Document slots and (under
the §8 lean) universe ids are minted from this authority. Lineage, split, and merge
operations **do not exist yet** [observed — grep of all seven repos found no
`lineage`/`ancestry`/`provenance` type and no split/merge operation]; everything in
§3-§6 is purely additive.

## 2. Q1 — the unit of "one schema"

**The unit of one schema is a `DocumentKey`.** One schema = one document = one
`DocumentKey { scope, kind, slot }`, whose `slot` (`SlotIdentifier`) is
minted-once by the central authority from a leased `IdentifierBlock`, never reused,
tombstoned on retirement. This aligns with Codex's document-family design (one
typed root, one Core record, one NameTable per document —
`document-core-adapter-design-v2.md`); "one schema" is exactly "one document" in
that family.

**Same schema, changed vs. a different schema.** An edit is *the same schema,
changed* when the authority binds the new revision to an **existing** `DocumentKey`:
`Version` advances, `ContentHash` moves, the NameTable may re-intern, the key is
unchanged. An edit is *a different schema* when it carries a **different**
`DocumentKey` — either freshly minted (genesis) or a split/merge child (§3-§4).

**Continuity is declared, not inferred** [lean L1, but forced in spirit by the
rejection of coordination-free content-inference]. Whether an edit is "the same
schema" is a *declared, authority-witnessed* fact — the edit targets a known
`DocumentKey` — not something recovered from content similarity. This is required,
not stylistic: content alone cannot distinguish a rename+reshape of document X from
a delete-of-X-plus-genesis-of-Y (the doctrine-v2 delete-plus-add ambiguity,
`document-core-adapter-design-v2.md` "Shared Core and NameTable law" point 4). The
authority records the continuity; it never guesses it. This is why the durable
handle is *allocated* and the fingerprint is *derived*.

**Type identities inside a document, across an ordinary edit.** A Core type keeps
its `ScopedCoreTypeId` when the edit is recognized as a modification of that type
(re-association by `(identifier kind, owner scope, current spelling)` against the
prior NameTable — doctrine v2 points 1-2). A renamed type keeps its
`ScopedCoreTypeId` and its `ContentHash` (§5). A genuinely new type mints a new
`local` id in the document's universe. A deleted type's id is tombstoned, never
reused.

## 3. Q2 — Split (one document becomes two)

Let the parent be document `K` (scope `S`, kind `D`, slot `s0`), universe `U`.

**Document identities.** The central authority mints a new slot `s1` from `S`'s
lease, producing a new child `DocumentKey K1`. The parent `K` **continues** — a
split, in the common "extract some declarations into a new document" case, is an
*in-place edit of K* (the extracted declarations leave K) plus a *genesis of K1*
that inherits them. K keeps its key and advances its `Version`; K1 is new. (Full
dissolution — K becomes K1 and K2, neither is K — is the degenerate case: mint two
new keys, retire K. §7 shows both are one primitive.)

**Type identities inside.** Carried-over Core types **keep their exact
`ScopedCoreTypeId`** — preserved by construction, not remapped — **provided
universe ids are globally unique** (the §8 lean L2: universes centrally minted,
never reused). Under that lean, a type `{ universe: U, local: n }` moved into K1
cannot collide with anything K1 mints (K1 mints in its own universe), so no receipt
and no remap is needed. K1's newly-originated types mint `local` ids in K1's own
universe. This is the research's Candidate A ("preserve by construction"),
`core-partition-lineage-research-v1.md` §3.

**NameTables.** Each document owns its own `NameTableBytes` sibling [observed —
`signal-sema-storage/src/lib.rs:243-257`, `names` field per variant]. K1 gets a
fresh NameTable re-interned from K's for the carried names; the `Identifier(u32)`
values renumber freely (they are store-local, never a cross-document key —
Candidate B). Nothing load-bearing moves, because Core identity excludes the table.

**What the authority allocates:** the new slot (`K1`), and any newly-minted `local`
type ids and universe id for K1. **What carries over:** the member Core type
identities (`ScopedCoreTypeId`s), by construction. **What lineage is recorded, and
where:** a sidecar lineage record on K1 (§6) with `origin: Split { parent: K }`,
optionally listing the carried type ids. Stored in sema, outside Core.

## 4. Q3 — Merge (two documents become one)

Let parents be `KA` (universe `UA`) and `KB` (universe `UB`), same `kind`.

**Document identities.** The authority mints a new slot → child `KC` (or, in the
"absorb" case, `KA` continues and absorbs `KB`; §7). Retired parents' slots are
tombstoned.

**Type identities and collision handling.** Carried types keep their
`ScopedCoreTypeId`s. Because `UA ≠ UB` (distinct centrally-minted universes, lean
L2), **no `ScopedCoreTypeId` can collide at the id level** — merge of the type-id
spaces is a collision-free set union. This is the whole payoff of preserve-by-
construction: the central authority owning one keyspace makes union safe
(`core-partition-lineage-research-v1.md` §3 addendum point 1, Confluent-primary-
node model).

**Name-level collision is the only real collision, and it is surfaced, never
silently merged.** If `KA` and `KB` each declare a type spelled `Foo` in the same
`(kind, owner)` scope, the two are distinct Core types with distinct ids, so Core
is fine — but KC's NameTable cannot hold two `Foo`s in one scope (the uniqueness
law, doctrine v2 point 3). The authority **halts the merge with a named-conflict
report**; the human resolves by renaming one (§5) or the `(kind, owner)` scopes
genuinely differ and both coexist. No inference, no silent shadowing — this mirrors
`validate_no_silent_conflicts` in the structural layer.

**Lineage:** KC records `origin: Merge { parents: [KA, KB] }`.

## 5. Q4 — Rename

**The Core already guarantees rename-stability, and this design changes nothing
about it** [observed — `name-table/src/identifier.rs:6-9`;
`signal-sema-storage/src/lib.rs:280-309`]. Renaming a declaration moves only its
NameTable entry (`current_spelling`); its `ScopedCoreTypeId` and its `ContentHash`
are both unchanged, because names are excluded from the Core value. At the Core
level a rename is an identity no-op. Confirmed, not redesigned.

**What the rename-intent path adds, narrowly.** The one thing content addressing
cannot recover is *intent* across a boundary where re-association by spelling fails
— precisely because the spelling changed (doctrine v2's delete-plus-add case). The
rename-intent path is an **edit-time alias**, keyed by the durable
`ScopedCoreTypeId` / `NominalId`, recording `old_spelling → new_spelling`, authored
**only where content is ambiguous** and **only where a name changed**. It lives in
the co-versioned NameTable sidecar (`DocumentNameTableV1`, extended with an alias
entry), never in Core. This is the research's Candidate E, narrowed
(`core-partition-lineage-research-v1.md` §3, addendum layer 3). It is a *name-layer*
concern, disjoint from Core identity; it exists so a downstream reader can bridge a
renamed declaration when it has no allocation context, not to stabilize Core
(already stable).

## 6. Q5 — Lineage records and the sidecar principle

**Lineage must never leak into Core value identity.** `ContentHash` is BLAKE3 over
the stringless structural bytes only [observed — as §1]. If document origin, rename
aliases, or tombstones entered that pre-image, then split, merge, and rename would
move Core hashes — destroying the partition-proof spine (identical Core values in
two stores would stop coinciding). So lineage is **sidecar by necessity**, for
exactly the reason the NameTable is: it is metadata *about a document's history*,
not *about a value's content*.

**Shape** (all [lean], greenfield-additive):

```text
DocumentLineage {
  document: DocumentKey,
  origin:   DocumentOrigin,
  identity: ContentHash<DocumentLineageDomain>   // own domain/layout; NOT in Core identity
}

DocumentOrigin ::=
  | Genesis                                  // created fresh
  | Split { parent: DocumentKey, carried: [ScopedCoreTypeId] }
  | Merge { parents: [DocumentKey] }
```

This is an ancestry DAG over `DocumentKey`s, content-identified under its own
domain and layout version, keyed by the document it describes.

**Where it lives in sema storage.** The delivered `StorageRecord` enum already
holds `Document(StoredDocument)` and `Allocator { scope, next }` in one table
[observed — `sema-storage/src/lib.rs:28-32`]. Lineage takes a **third sidecar
variant** (`StorageRecord::Lineage(DocumentLineage)`) or, equivalently under bead
.10's proposal 2, a co-versioned sibling record alongside the document and its
NameTable. Rename aliases and id tombstones live in the co-versioned NameTable
sibling. All three (origin DAG, aliases, tombstones) are content-identified,
co-versioned, and excluded from Core identity. [dependency on bead .10 — §10.]

## 7. The primitive that dissolves split and merge (design-quality note)

Split and merge are not two new mechanisms. Both are one primitive:

> **create-or-continue a document whose member type-id set inherits a chosen
> subset of ancestor member type-ids (kept by construction), while the authority
> mints the new slot / universe / local ids and records the origin.**

- **Split** = continue K (remove extracted members) + create K1 inheriting the
  extracted subset. Origin `Split{parent}`.
- **Merge** = create/continue KC inheriting the union of parents' members. Origin
  `Merge{parents}`.
- **Genesis** = create with an empty inheritance set. Origin `Genesis`.
- **Ordinary edit** = continue with the full inheritance set unchanged.

The special cases (full-dissolution split, absorb-merge) are just different
inheritance sets and different retirement choices over the same primitive — no side
path. This is the design-quality gate met: the "split" and "merge" special cases
dissolve into "a document inherits member type-ids from ancestors, and the authority
mints what is new." The only operation the engine gains is *inheritance of member
type-ids with origin recording*; everything else is the edit path it already has.

## 8. Leans register (each revisable; not psyche-graded)

- **L1 — Continuity is declared, authority-witnessed, never content-inferred.**
  Revision trigger: if the psyche wants content-similarity heuristics to auto-detect
  "same schema" (rejected here as reintroducing the delete-plus-add ambiguity).
- **L2 — Universes are centrally minted and globally unique (compact `u32`), never
  reused, retired ids tombstoned; a document originates one universe.** This is the
  load-bearing lean: it makes carried `ScopedCoreTypeId`s collision-free across
  split/merge with no receipts. It requires *linking* the currently-independent id
  systems — `CoreUniverseId` (structural-codec, type-identity, today
  `FIXTURE_UNIVERSE(0)`) and `FixtureScope`/`IdentifierBlock` (sema-storage,
  document-slot leasing) [observed — the two are unconnected today,
  `structural-codec/src/ids.rs:22`, `sema-storage/src/lib.rs:185-219`]. Under this
  lean the central authority mints universe ids too, replacing the fixture
  placeholder. Follows research Candidate A + addendum (compact `u32` because a
  central mint owns the keyspace — no 128-bit width needed). Revision trigger: a
  multi-authority topology (two independently-rooted registries merging), where the
  union guarantee no longer holds and Candidate C receipts return at the universe
  layer (research §5 honest residual); or a decision to keep the two id systems
  separate and re-scope type ids on move (Candidate C, receipts — rejected here as
  against the grain).
- **L3 — NameTable `Identifier(u32)` is store-local; re-intern on split/merge, never
  a cross-document key** (research Candidate B). Revision trigger: any stored record
  found keying by raw `Identifier` across a document boundary — that record must
  rehydrate through its NameTable sibling instead.
- **L4 — Rename intent is an edit-time alias in the NameTable sibling, authored only
  where content is ambiguous** (research Candidate E, narrowed). Revision trigger:
  the psyche wanting aliases always-on, or wanting them Core-visible (rejected: would
  leak into identity).
- **L5 — Lineage is a `DocumentLineage` sidecar (origin DAG) in sema storage,
  excluded from Core identity.** Revision trigger: the psyche deciding lineage is not
  worth storing (drop the DAG; keep only tombstones + aliases), or bead .10 resolving
  the sibling-storage mechanism differently.
- **L6 — Split keeps the parent (extract semantics); merge may absorb or mint-new.**
  Revision trigger: the psyche wanting symmetric semantics (split always retires the
  parent and mints two).

## 9. Open questions for the psyche

- **O1 — Document = universe?** Is a schema document the right granularity for "one
  universe" (L2), or should a universe be coarser (a `FixtureScope` grouping many
  documents) or finer? This sets how type ids are scoped across split/merge.
- **O2 — Single-authority topology confirmed?** The union-is-collision-free
  guarantee holds within one authority's keyspace. Is a single logical registry the
  assumed deployment (so multi-authority merge stays out of scope)? The ruling
  "seat it centrally in sema" strongly implies yes; confirming closes the one place
  receipts would otherwise survive.
- **O3 — Is the origin DAG mandatory or opt-in?** Every document carrying a
  `DocumentLineage` costs storage; the alternative is recording origin only on
  split/merge events and leaving genesis implicit.
- **O4 — Split parent semantics** (L6): extract-and-continue, or symmetric
  dissolve? Real edits look like extract; confirm the default.

## 10. Boundaries, dependencies, and version surfaces

- **Bead .10 (storage pair — non-rejected, psyche-pending).** Lineage and the
  NameTable-sibling aliases ride proposal 2 (NameTables as co-versioned Core
  siblings) and, where a new record layout appears, proposal 1 (format-upgrade
  machinery). This design is **compatible with both without ruling either**: it adds
  a sidecar `StorageRecord::Lineage` variant that is content-identified and
  co-versioned exactly as proposal 2 prescribes. If .10 rules differently, only the
  storage *seat* of L5 moves; the identity semantics (§2-§5) are unaffected. Marked
  dependency, not a blocker.
- **Bead .13 (sema-engine stored-record identity basis — sibling, blocked).**
  [interface] This design hands .13 its identity basis without designing .13's
  record internals: the durable stored-record key is `DocumentKey { scope, kind,
  slot } + Version`; the content address is `ContentHash` (NameTable excluded); the
  type-level identity is `ScopedCoreTypeId`; retirement tombstones slots and ids.
  .13 consumes these; it is not preempted.
- **Bead .12 (restated bootstrap question 2 — blocked-on-psyche).** Untouched.
- **Bead .31 (text-versus-string).** Untouched.
- **Version surfaces** (all truthful under this design): no **Core-layout** bump is
  forced — lineage is sidecar and excludes Core, and L2 keeps universe ids `u32`
  (no width change), so stored-record Core layout is stable [research addendum point
  2]. New surfaces are additive and take their own layout versions: a
  `DocumentLineageDomain` layout for the lineage record; a **NameTable-layout** bump
  for the alias entry; a **storage-schema** bump for the `StorageRecord::Lineage`
  variant. Existing stores stamped `FIXTURE_UNIVERSE(0)` need a one-time data
  re-stamp to an authority-minted universe id (a data migration within an unchanged
  type, not a format upgrade) — flag for when .10 and L2 are ruled.

## 11. Validation scope

Design-only. No engine source, generated artifact, store, deployment, or Spirit
record was changed. Claims about the delivered engine are this lane's direct
source reconnaissance, cited by file:line; claims about prior rulings cite the .11
bead thread and the named reports. Nothing here is accepted until the psyche grades
it — bead .11 stays open.
