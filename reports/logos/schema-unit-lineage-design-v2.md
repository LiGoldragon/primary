# Schema-unit and split/merge identity — design v2

> **Supersedes `schema-unit-lineage-design-v1.md`.** The psyche engaged v1's
> chat summary and ruled. His rulings **delete machinery**: v1's identity keystone
> ("identity lives in an allocated handle held apart from a derived fingerprint")
> is kept, but the surrounding lineage apparatus — the `DocumentLineage` origin
> DAG (v1 §6), the receipts / multi-authority residual (v1 L2 revision trigger,
> O2), the rename-intent alias (v1 §5, L4), and "move" as a distinct primitive —
> is **removed, not deferred**. The unit is re-seated from the **document** onto
> the **schema-whole** (v1 §2 reversed). This v2 is deliberately leaner than v1
> and is not padded back. Read this file; v1 remains only as superseded history.

Written 2026-07-17, session `LanguageFamilyDesign`, lane `SchemaUnitLineageDesign`,
generalist, Opus 4.8 (1M). Design-only; read-only on every engine repo. Bead
**primary-56d1.11** stays OPEN — closure follows psyche acceptance, not this write.

## 0. Provenance markers

- **[ruling]** — a settled psyche decision (verbatim quoted where quoted); overrides.
- **[keystone]** — the identity keystone (§1) or a consequence forced by it.
- **[observed — cite]** — a delivered-engine code fact, file:line, from this lane's recon.
- **[lean]** — a revisable design lean, NOT psyche-graded; each carries a revision trigger (§8).
- **[deleted]** — machinery present in v1 and removed by the rulings (ledger in §7).

## 1. The keystone and the two laws — the enforceable heart

**Identity IS the ID.** [ruling, keystone, psyche verbatim] "*if it got re-ID'ed
then its not the same, and if it's the same and got re-ID'ed, the system is
implemented wrong*." The ID is constitutive of sameness, not a label pasted over
some deeper sameness the system must separately remember. There is nothing beneath
the ID to reconcile against.

From the keystone, the authority's whole job is **two invariants** — the
enforceable heart of the design:

1. **Never re-mint an ID for the same thing.** The same thing keeps its one ID
   forever; a second ID for it is a bug.
2. **Never rebind an existing ID to a different thing.** An ID names exactly one
   thing for all time; pointing it at a different thing is a bug.

Their contrapositive is the keystone read back: two things with different IDs are
different (correctly), and one thing that acquired a second ID means the system is
implemented wrong. Everything below is these two laws applied uniformly to the two
identity levels — **type identity** and **schema-whole identity**.

**Single authority.** [ruling, psyche verbatim] "*single authority.
criome-authorized propagation is in the future.*" One logical allocation authority
mints both id levels from one keyspace; the two laws are its only mandate. Any
future federation is criome-authorized propagation and is **out of scope**. This
permanently closes the multi-authority / receipts case (v1's one surviving reason
for lineage bookkeeping); it is not deferred, it is gone. The authority is already
seated in the delivered engine: `StorageRecord::Allocator { scope, next }` leasing
`IdentifierBlock`s [observed — `sema-storage/src/lib.rs:31,213`].

## 2. Q1 — the unit of one schema is the schema-whole

[ruling, psyche verbatim] "*schema isnt a document, the document form is a
legacy-view; schema is loaded **as a whole schema with its dependencies**.*"

**The unit of one schema is the schema-whole** — the closed set of type identities
that load together with their dependency closure, carrying its own constitutive
schema-whole identity. Identity attaches to the whole, not to a document or file.

**Documents and files are legacy packaging — a view.** How a whole is chunked into
stored records, documents, or files is a **storage/view concern that does not touch
identity**. The delivered `DocumentKey { scope, kind, slot }` + `Version` [observed
— `signal-sema-storage/src/lib.rs:36,68-71`] is retained as a storage-view address
over the whole; it is demoted from "identity of a schema" (its role in v1 §2) to
"one packaging address," not identity-bearing [lean L3].

So there are exactly two identity levels, both governed by the §1 two laws, both
minted by the single authority:

- **Type identity** — one constitutive ID per type (delivered: `ScopedCoreTypeId`).
  The stable atom; invariant under editing, renaming, and re-partitioning.
- **Schema-whole identity** — one constitutive ID per whole. A whole *is* a
  declared membership of type identities plus dependency closure [lean L1].

## 3. Version-within-identity (kept)

[ruling] Same ID, versions and content fingerprints advance on edit. Within one
identity the durable ID is fixed while the **content fingerprint moves on every
semantic edit** — the delivered `content_hash` is a domain-separated BLAKE3 over
the Core payload with the NameTable excluded (the match arms drop the `names`
field via `{ .. }`) [observed — `signal-sema-storage/src/lib.rs:280-309`]. The
fingerprint is the per-revision content identity under an unchanged type/whole ID.

**Shape-change within one identity is where format-upgrade genuinely lives**
[ruling]. When a type keeps its ID but its shape changes across revisions,
converting stored values across those shape-versions is the format-upgrade track —
not an identity event. It rides bead .10's un-ruled pile compatibly (§9, §10).

## 4. Declared identity: bind-existing vs mint-new ("move" disappears)

[keystone] Because the ID *is* the identity, "**move**" is not a primitive. A type
declared in a new home that **binds its existing ID simply IS the same type**; a
freshly minted lookalike **IS a different type**, correctly unrelated. Nothing is
carried or remapped — the ID already says which.

Therefore the authoring surface must let each declaration state **bind-existing-
identity** versus **mint-new** — **declared, never inferred from content, enforced
by the authority** [ruling]. Content similarity may never decide sameness (that
would be the system remembering something beneath the ID, which by the keystone
does not exist). The concrete marker shape is a lean [L4]; that it is declared and
authority-enforced is forced by the ruling.

This is the whole of "same schema, changed vs. a different schema": same when the
declaration binds the existing whole/type IDs (version + fingerprint advance);
different when it mints new ones.

## 5. Split and merge — declared re-partitioning over stable type identities

[keystone] Split and merge are **not new mechanisms**. They are **declared
re-partitioning of schema-wholes over stable type identities**:

- The author re-declares partitions: each stable type identity is assigned to a
  resulting whole, and for each resulting whole the author declares whether it
  **binds an existing whole-identity** (that schema continues) or **mints a new
  one** (§4).
- **Type identities never change.** Because there is one authority and one keyspace
  (§1), the type-id set operations of a split (subset) or merge (union) are
  **collision-free by construction** — no remap, no receipts, no carried record.
  The IDs already carry sameness.

**The split-parent question v1 left open (v1 O4) resolves by the keystone applied
uniformly to schema-whole identity itself:** the remainder of a split **IS still
schema A exactly if it keeps A's whole-identity**, and the author declares which —
continue A (remainder binds A's ID, extracted part mints/binds another) or dissolve
A (both results mint new whole-ids, A retired). Symmetric merge is the same rule:
the combined whole binds one parent's identity or mints a fresh one, declared.
[lean L2 — this uniform application of the psyche's law to whole-identity is an
agent derivation, revisable; it is not his verbatim ruling.]

**Name-collision is the only real collision, and it is a name-layer conflict, never
an identity one.** Two distinct type identities may share a spelling in one scope
after a merge; that violates NameTable spelling-uniqueness, so the authority
surfaces it as an authoring conflict for the human to resolve by rename — never a
silent merge or shadow [lean L6]. Identity is untouched (the IDs stay distinct);
only the name view needs disambiguating.

## 6. Rename (Core already stable; nothing added)

A renamed type keeps its ID and its content fingerprint **by construction**, because
names are excluded from the Core value [observed — `content_hash` drops `names`,
`signal-sema-storage/src/lib.rs:280-309`]. At the identity level a rename is a
no-op. This design **adds nothing** here.

In particular, v1's rename-intent alias (`old_spelling → new_spelling`, v1 §5/L4)
is **[deleted]**. It existed to let a downstream reader *recover provenance* across
a spelling change. With declared identity (§4) that recovery is unnecessary and, by
the keystone, meaningless: following the unchanged ID already gives continuity.

## 7. Deletion ledger — what v1 carried and the rulings remove

Stated explicitly so a reader sees the reframe, not a silent gap. Each is deleted,
not deferred.

- **`DocumentLineage` origin DAG, `DocumentOrigin::{Genesis,Split,Merge}`, carried-
  id receipts, ancestry notes** (v1 §6, §3-§4, L5). **[deleted, keystone]** There is
  no ancestry machinery for identity: the ID carries sameness, so there is nothing
  to remember. (The psyche also signalled hedged indifference to provenance —
  verbatim, "*I dont know if I care about the whole 'X came from file Y'*" —
  preserved here as his hedge; the deletion is forced by the keystone regardless of
  how that hedge later settles.)
- **The multi-authority / receipts residual** (v1 L2 revision trigger, O2).
  **[deleted, ruling 2]** Single authority now; federation is future
  criome-authorized propagation, out of scope. The one place receipts survived is
  closed.
- **The rename-intent alias** (v1 §5, L4). **[deleted]** See §6.
- **"Move" as a distinct primitive** (v1's carry/remap framing, §3-§4, §7).
  **[deleted, keystone]** Move is just declaring an existing ID in a new home (§4).
- **Unit = `DocumentKey`** (v1 §2). **[replaced, ruling 1]** Unit = schema-whole;
  the document is a legacy view (§2).
- **Open questions O1-O4** (v1 §9). **[resolved/dissolved]** See §9.

## 8. Leans register (each revisable; not psyche-graded)

- **L1 — Schema-whole identity is a distinct constitutive ID**, governed by the two
  laws, separate from the type identities it contains; a whole is a declared
  membership of type identities plus dependency closure. Revision trigger: the
  psyche deciding the whole carries no identity of its own (identity purely
  per-type), or that whole-identity derives from a designated root type rather than
  being independently minted.
- **L2 — Uniform application of the keystone to whole-identity** (§5): on
  re-partition a resulting whole keeps an existing whole-identity iff the author
  declares it binds that identity, else mints a new one. Revision trigger: the
  psyche ruling asymmetric semantics (e.g. split always mints fresh whole-ids, or
  merge always mints a fresh whole).
- **L3 — `DocumentKey`/document/file demoted to a storage-view address** over the
  whole, retained as packaging (not deleted). Revision trigger: the psyche wanting
  document packaging removed, or a different view-addressing scheme.
- **L4 — bind-existing vs mint-new is an explicit per-declaration authoring
  marker**, authority-enforced, never content-inferred (the *declared + enforced*
  part is forced by ruling; only the marker's surface shape is the lean). Revision
  trigger: a concrete authoring-surface design shaping the declaration differently.
- **L5 — The single authority mints globally-unique type identities from one
  keyspace** (delivered `{universe, local}` structure; compact ids, never reused,
  retired ids tombstoned), replacing the `FIXTURE_UNIVERSE(0)` placeholder. Single
  authority makes split/merge id-set operations collision-free by construction — no
  receipts. Revision trigger: a flat-id or differently-structured keyspace decision.
- **L6 — Name-collision within a merged whole surfaces as an authoring conflict
  resolved by rename**, never a silent shadow. Revision trigger: the psyche wanting
  scoped-coexistence rules instead of a surfaced conflict.

## 9. Open questions — none require the psyche's word

Applying the keystone, **no open question genuinely needs his ruling to let this
design stand.** Each v1 open question is closed:

- **O1 (document = universe?)** — **dissolved.** The document is a view (§2);
  identity is per-type and per-whole, centrally minted. The granularity question
  was an artifact of treating the document as the identity unit.
- **O2 (single-authority topology?)** — **closed by ruling 2.**
- **O3 (origin DAG mandatory vs opt-in?)** — **moot.** There is no DAG (§7).
- **O4 (split-parent semantics?)** — **resolved** by the keystone: the author
  declares which result keeps A's identity (§5). The default is a revisable lean
  (L2), decidable without him.

The one area deliberately left un-ruled is the **format-upgrade pile (bead .10)** —
shape-change within one identity and value conversion across different types. This
design is compatible with it and does **not** need it ruled to stand (§10). That is
a standing decision the psyche will reach on his own timeline, not an open question
this design forces open.

## 10. Boundaries, dependencies, version surfaces

- **Bead .10 (storage pair — un-ruled, untouched).** Format-upgrade for
  shape-change within one identity (§3) and value conversion across different types
  (§4 copy-reshapes create genuinely different types) ride .10's pile. This design
  is compatible with .10's proposals **without ruling any of them**: identity (§1-§6)
  is independent of the storage/upgrade seat. If .10 rules, only the mechanics of
  the format-upgrade track move; identity semantics are unaffected.
- **Bead .12 / .13 / .31 — untouched.** .13 (stored-record identity basis) still
  consumes this design's identity basis: the two identity levels (type identity,
  schema-whole identity), the two laws, the per-revision content fingerprint, and
  the storage-view demotion of `DocumentKey`. It is handed, not preempted.
- **Version surfaces.** No Core-layout bump is forced: identity value shape and
  `content_hash` are unchanged. New surfaces are additive — the per-declaration
  bind/mint marker (authoring surface), the central whole/type-id mint replacing
  `FIXTURE_UNIVERSE(0)` (a one-time data re-stamp within an unchanged type when the
  central mint lands, not a format upgrade). The format-upgrade track itself is
  bead .10's to version.

## 11. Validation scope

Design-only. No engine source, generated artifact, store, deployment, or Spirit
record was changed. Delivered-engine claims are this lane's direct file:line recon
(re-verified this pass); ruling text cites the psyche's 2026-07-17 chat and the .11
bead thread. Nothing here is accepted until the psyche grades it — bead .11 stays
OPEN.
