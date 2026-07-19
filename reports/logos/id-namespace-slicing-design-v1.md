# ID Namespace Slicing — up-close design (v1)

Status: DESIGN ONLY. Nothing here is implemented. This is the up-close design the
psyche asked to see before any implementation ("Yes, and I want to see the design of
all that up close first"). Every recommendation below is a lean, not a decision; the
psyche-owned choices are gathered in the decision slate at the end, each answerable
in a word.

This design is written against verified code (revisions in the appendix), not prose.
Where it draws a picture it uses plain ASCII, never a rendered Protos surface, and it
quotes only real atoms that exist in the code today.

## Revision note — the identifier representation is settled (2026-07-19)

The psyche ruled on slate item 1, and the ruling supersedes both candidates this
document originally proposed (the `{slice, local}` struct and the packed-CIDR u32).
His words, verbatim:

- "actually, I was complicating things; the ID is the variant with its inner u16
  (16 bits should be lots for a language)"
- "Schema.Id16 Logos.Id16 etc"

Settled: the identifier is a **data-carrying enum** whose *variant is the slice* —
`Schema`, `Logos`, and so on — each variant carrying an inner `u16` local
(~65 000 names per language). No `{slice, local}` struct, no CIDR packing, no block
arithmetic. Global uniqueness is by construction through the type system, matching is
exhaustive, and the variant set *is* the namespace registry: minting a slice for a new
component is adding an enum variant, and recompilation is cheap (Spirit 16jw, enums
over strings — this ruling is that intent made concrete).

The sections below are revised around this ruling. Everything the psyche had already
confirmed is kept intact — the nametree is composable, a table borrows slices rather
than copying them, and the tandem design records ID-to-ID links. Section 2 records the
ruling; sections 3, 4, 7 and 8 are re-derived from it. The superseded struct/packed
analysis is retained only as the decision trail that led here.

## 0. What the psyche said, and what it means against the code

Three statements drive this design (2026-07-19, verbatim):

- "logos (and maybe others) need multiple nametrees; that way logos already has its
  own encodedID namespace, so the nomos conversion can use those ID's in the
  conversion (some fields will not be coming from schema, but will be part of the
  logos 'standard objects' which get their own slice of the ID namespace — we should
  do a slicing similar to hop IP addresses are shared while remaining global
  namespace."
- "so the nametree is composable."
- "it it more efficient to do the nametree conversion in tandem with the encodedform
  transform?" (open question)

The code makes the first statement concrete. Today the logos NameTable is built by
`NameTable::extend_from(schema_names)` — a clone of the schema table — after which
`NameTableBoundary` re-materializes logos's own standing vocabulary as fresh strings
on **every** conversion run. The verified re-materialized atoms are, from
`core-nomos/src/name_boundary.rs`:

```
Integer  String  Boolean  Bytes        (the scalar leaf spellings, leaf_path)
Vec  Option  ScopeOf                   (single-arg projection heads)
Map                                    (multi-arg projection head)
```

plus the module-head vocabulary in `prelude.rs` and the standing derive paths
(`Copy` is resolved by string in `remove_copy_derive`). These are logos's "standard
objects": names that are **not coming from schema** — they are logos's own, produced
fresh each run and interned at the tail of the extended table.

This has a latent consequence the psyche's design fixes. Because the standard atoms
are interned at the tail of a table that begins as a clone of schema, the local index
of `Vec` (or `Option`, or `String`) **depends on how many schema names preceded it**.
The same logos construct built against a 50-name schema and a 500-name schema gives
`Vec` two different identifiers. Logos content identity for its own vocabulary is
therefore schema-size-dependent today — a special case waiting to bite. Giving the
standard objects their own fixed slice makes `Vec` a fixed identifier regardless of
schema, which dissolves that special case (design-quality: the schema-independent
vocabulary stops being a moving target).

The IP-address analogy is exact and load-bearing: one global namespace, carved into
delegated blocks; every address globally unique; each block locally allocatable by
whoever holds it, with no per-address coordination; and — the word he chose — blocks
are **shared** structurally the way subnets share the one IPv4 space. "The nametree is
composable" is the same picture from the holder's side: a component's one nametree is
**composed** from the slices it holds plus the read-only slices it borrows.

## 1. The reframe: one keyspace, sliced

Today an `Identifier(u32)` is a dense index into one `Vec<Name>` owned by one table.
The reframe keeps one global keyspace but makes the identifier an enum whose *variant
is the slice*, each variant carrying a `u16` local:

```
   TODAY                              SETTLED
   Identifier(u32)                    Identifier = enum { Schema(u16), Logos(u16), ... }
   = dense index into one Vec         = the variant IS the slice; the u16 is the local

   one flat table per component       one COMPOSED table per component,
   built by cloning schema's              built by composing per-variant nametrees:
   table and appending

   +------------------------+         +--------- component nametree view ---------+
   | schema names ...       |         | borrow: [ Logos-standard nametree ] (r/o) |
   | Vec Option String ...  |  --->   | borrow: [ Schema(..) nametree ]     (r/o) |
   | (logos tail, re-made   |         | own:    [ Logos(..) nametree ]     (append)|
   |  every run, index      |         +-------------------------------------------+
   |  depends on schema)    |             one view, many per-variant nametrees
   +------------------------+
```

Global uniqueness is now a type-system fact, not an arithmetic one: a `Schema(7)` and a
`Logos(7)` are distinct identifier values that cannot be confused, and an exhaustive
match over the variant set is total. The variant set is the namespace registry — the
compiled enum definition names every slice that exists.

The identity of a name never moves when a table composes it: a schema name keeps its
`Schema(local)` because logos **borrows** the schema nametree rather than copying it.
That is the literal realization of "the continuous identifier space" — continuous
because it is the *same* slice seen from two components, not because one component
copied the other's indices to matching positions.

The workspace's type-id space has a parallel today: `ScopedCoreTypeId { universe, local }`
in `structural-codec/src/ids.rs`. Whether that space should adopt the same variant-enum
shape as the name space is a follow-on question, surfaced in the revised slate; the
ruling here is specifically about the name identifier.

## 2. Question 1 — slice topology (SETTLED: the variant is the slice)

How the one global keyspace is carved. The psyche settled this, superseding the two
representations this document first proposed.

### 2.1 The ruling

The identifier is a data-carrying enum, one variant per language/component, each
carrying an inner `u16` local:

```
   Identifier = enum {
     Schema(u16),      # ~65 000 names in schema's slice
     Logos(u16),       # ~65 000 names in logos's slice
     ...               # one variant per component; the variant set is the registry
   }
```

His words: "the ID is the variant with its inner u16 (16 bits should be lots for a
language)" and "Schema.Id16 Logos.Id16 etc". The carving is done by the type system:
the variant *is* the slice, so there is no prefix to mask, no block to arithmetic over,
and no range registry to look a slice up in. Global uniqueness holds by construction —
two variants are distinct values — and an exhaustive match is total, so adding a
component is adding a variant and the compiler finds every site that must handle it.

### 2.2 Why this is better than what this document first proposed

The originally-proposed `{slice, local}` struct and packed-CIDR u32 both carried the
IP analogy's arithmetic baggage — a slice number that could be miscomputed, mismatched,
or exhausted, and (for the packed form) the analogy's own scarcity warning. The enum
keeps the analogy's *spirit* (one global namespace, per-component slices, local
allocation with no coordination) while discarding its arithmetic: a slice is named, not
numbered, so the whole class of block-arithmetic errors cannot be written. This is the
16jw intent (enums over strings/numbers) applied to the id space itself. The struct and
packed forms are retained above only as the trail that led to the ruling.

### 2.3 The u16 width

`u16` gives ~65 000 locals per language — the psyche's own sizing ("16 bits should be
lots for a language"). Width is now a *per-variant* property, not a shared budget: a
variant that ever needed more is widened on its own without touching any other slice
(see Q2 exhaustion). The name identifier does not need `u32` locals; a language is not
that large.

## 3. Question 2 — allocation authority (re-derived: authority over the variant set)

Under the enum ruling the central authority governs a different thing than numeric
grants. It governs the **variant set itself**.

### 3.1 What sema now governs

```
        sema  (single seated authority — prior ruling)
          |  owns the identifier variant set (the namespace registry)
          |  minting a slice = adding a variant to the Identifier enum
          v
   Identifier = enum { Schema(u16), Logos(u16), <new component>(u16), ... }
          |  propagation = the recompilation cascade over the family
          v
   holder appends u16 locals within its OWN variant, 0 runtime coordination
```

There is no runtime numeric grant to hand out and no block to reserve. The registry is
the compiled enum definition; "minting a slice for a component" is adding its variant,
a source edit made under sema's authority, and "propagation" is the recompilation
cascade the ruling already accepts as cheap (16jw). Local allocation is unchanged and
fully local: a component appends `u16` locals into its own variant's nametree —
precisely today's `intern` (append + dedup), now scoped to the holder's variant. No
allocation ever touches sema.

"criome-authorized propagation is in the future" now reads cleanly: today the variant
set is a single compiled registry sema owns; the future is Criome-authorized dynamic
variant registration (a component registering its slice without a central source edit).
The design must not assume the variant set is *forever* static-and-central; it must
assume that only for today's compiled form.

### 3.2 Exhaustion — a raise-then case, not machinery now

A `u16` variant holds ~65 000 locals. Should a single language ever outgrow that, the
raise-then response is local to that one variant: widen its inner (`Schema(u16)` becomes
a wider inner), or add a continuation variant for that language. Either is a bounded
edit to one variant with no effect on any other slice, and neither is built now. The
psyche sized `u16` as "lots for a language", so this stays a documented raise-then, not
present machinery.

## 4. Question 3 — the logos builtin slice

What the "standard objects" are, and how their pre-allocated ids plus pre-named
nametree ship with logos.

### 4.1 What is standard, and what only looks standard

The standard objects are the **fixed atoms** logos always speaks, independent of any
schema. Verified from the code, they are:

- the scalar leaf spellings `Integer`, `String`, `Boolean`, `Bytes`;
- the projection heads `Vec`, `Option`, `ScopeOf`, `Map`;
- the module-head vocabulary (the scalar aliases and the cfg-gated NOTA import name in
  `prelude.rs`);
- the standing derive paths (e.g. the `Copy` that `remove_copy_derive` matches today
  by string).

A sharp line must be drawn against names that only *look* standard. `route_enum_name`
produces `{root}Route`, `signal_object_name_literal` produces `Signal{root}{variant}`,
and `short_header_const_name` joins two screaming forms — these are **derived from
schema names**, not fixed atoms. They are not standard objects; they belong to the
logos allocation slice (Q5), not the standard slice. Only the schema-independent atoms
are pre-allocated. The fixed *affixes* (`Signal`, `Route`) could themselves be standard
atoms, but the composed names they build are always derived.

### 4.2 Where the standard objects sit under the enum (open, propose-not-settle)

The coordinator asked for a lean here without settling. Two placements:

```
  Distinct variant                        Reserved low range inside Logos
  Identifier = { ..., LogosStandard(u16) } Identifier = { ..., Logos(u16) }
  standard objects live in their own       locals 0..N of Logos reserved for
    variant, peer to Logos                   standard objects; derived logos names
  fixed ids by construction; a standard      append from N upward
    id can never collide with a derived    "logos's own namespace, standard a slice
    logos name (different variant, exhaustive  of it" reading; one variant, ordered
    match tells them apart)                 low region
```

His statement carries both readings: "logos already has its own encodedID namespace"
(one Logos variant) and "standard objects ... get their own slice of the ID namespace"
(their own slice). Under the ruling that a slice *is* a variant, "their own slice"
reads most literally as **their own variant**.

Lean (not settled): a distinct `LogosStandard(u16)` variant. It is the literal reading
of "their own slice", it makes the standard ids fixed and schema-independent by
construction, and it uses the exhaustive-match property to keep standard objects and
derived logos names provably separate — the same type-system guarantee the whole
ruling is built on. The reserved-low-range alternative is the "a slice of logos's own
namespace" reading and stays on the table; it is simpler but couples the two
allocations inside one variant. Either way the *contents* of the standard slice are
owned and versioned by logos; sema owns only whether the variant exists in the
registry. (This absorbs the original ownership question: logos owns the standard
vocabulary's contents regardless of which placement wins.)

### 4.3 How it ships — three options

```
  (a) compiled-in constants        (b) runtime data file        (c) content-identified
      pub const STRING: Identifier      load a serialized            NameTableDomain sibling
        = LogosStandard(1); engine      nametree at startup          shipped + versioned by hash
        references directly           string lookups at runtime    the co-versioning discipline
                                                                  name-table already has
```

Recommendation: ship the logos standard slice as a content-identified `NameTableDomain`
sibling (c) — the co-versioning mechanism `NameTable::identity()` already provides — and
**generate** the compiled-in `Identifier` constants (a) from it as the engine's
reference surface. The sibling nametree is the single source of truth (its content hash
is its version); the constants are its deterministic projection (w312: derivable, so
mechanism, not hand-authored). Nomos then references `standard::STRING` directly and
never interns the string "String" again. The pure data-file (b) alone is rejected: the
engine wants a compile-time typed reference, not a runtime string lookup, and (c)+(a)
gives both a versioned artifact and a typed reference.

## 5. Question 4 — composability

How per-slice nametrees compose into a component's one NameTable, and how that
preserves the one-nametable-per-component ruling.

### 5.1 The composed view

```
   component nametree (ONE view, the ruling's "one NameTable per component")
   +---------------------------------------------------------------+
   |  per-variant nametrees, keyed by the identifier variant       |
   |                                                               |
   |   [ Logos-standard nametree ]  borrowed, read-only            |
   |   [ Schema(..) nametree ]       borrowed, read-only           |
   |   [ Logos(..) nametree ]        owned, append target (home)   |
   +---------------------------------------------------------------+

   resolve(id)  = match id { Schema(l) => schema[l], Logos(l) => home[l], ... }
   intern(name) = append into the HOME variant only  (borrowed variants are read-only)
```

`resolve` is an exhaustive match on the identifier variant, then a dense index by the
`u16` local — each variant keeps today's `Vec<Name>`, so the fast path inside a slice is
unchanged, and the match is total so a new variant is a compile error until handled.
`intern` targets the component's **home** (owned) variant; borrowed variants such as the
standard slice or the schema slice are never appended to, which is why a standard object
is referenced by its fixed id and never re-interned.

### 5.2 Why the one-nametable ruling holds

The ruling "one NameTable per component" is preserved because the composition **is**
the component's one NameTable. The slices are the internal structure of that one table,
not competing tables — the public `resolve`/`intern` surface is unchanged. "The
nametree is composable" refines "one nametable per component"; it does not contradict
it. Nomos still owns exactly one logos NameTable; that table now happens to be composed
of a borrowed standard slice, a borrowed schema slice, and its own allocation slice.

### 5.3 What this replaces

Composition replaces `NameTable::extend_from`. Today `extend_from` clones the schema
table so schema ids land at matching indices; composition borrows the schema slice so
schema ids *are* valid unchanged, with no copy. The continuous-identifier-space
property becomes structural rather than a runtime coincidence that interning-dedup has
to reproduce.

## 6. Question 5 — the tandem link design

The psyche's open question: is it more efficient to do the nametree conversion in
tandem with the encodedform transform? The manager's lean (input, not law): tandem for
ID-to-ID links only, strings materialized at the boundary from the links.

### 6.1 Concretized against the real engine

Two kinds of name work happen in lowering today, and they behave differently under
tandem:

```
  LITERAL NAMES (from schema / from the package's authoring table)
     today:  package_names.resolve(id) -> Name(string) -> logos.intern(Name) -> id'
             i.e. a round-trip THROUGH A STRING to move a name between tables
     tandem: compose the source slice; the id is ALREADY valid -> ZERO strings

  DERIVED NAMES (field_name / screaming / pascal_case / {root}Route / Signal{..})
     today:  resolve source id -> compute new string -> intern -> new id (with dedup)
     tandem: record a link (source id, transform) now; materialize the string later
```

For literal names the win is total and clean: once the package's authoring slice and
the schema slice are **composed** into the logos table (Q4), a template literal that
names id N in a borrowed slice needs no `resolve`/`intern` round-trip at all. This is
where `place_literal_name`'s string touch disappears — not by cleverness but because
the slice it came from is present in the composition. The standard-object references
(`leaf_path("Integer")` and its kin) collapse the same way: they become references to
the pre-allocated ids in the standard slice.

Derived names genuinely produce new strings (`field_name` lowercases, `pascal_case`
recases, the affix builders concatenate). Two honest options:

- Eager (conservative tandem): keep materializing derived-name strings at the boundary
  as today, allocating into the logos alloc slice in walk order. Dedup and determinism
  are preserved exactly; the win is only that literal/standard names stop touching
  strings — which is the large majority of the name traffic. The psyche's own ruling
  already blessed this boundary string work as "necessary".
- Deferred (pure tandem): record each derived name as a `(source id, transform)` link
  during the transform and compute the string only at render (TextualRust projection /
  `ModuleHead::render`). Zero strings cross the transform. The cost: `intern`'s eager
  dedup is lost mid-transform, so equal derived names would need a render-time
  canonicalization to stay deterministic, and the derived id must be assigned by a pure
  function of `(source id, transform, slice)` to keep logos content identity stable
  (w312).

### 6.2 Recommendation

Adopt tandem for the ID-to-ID links, with **eager** derived-name materialization
(the conservative form). Composition removes the literal round-trip (the big efficiency
and no-strings win the psyche is reaching for); derived names keep their eager,
deterministic, dedup-preserving materialization at the boundary his ruling already
sanctioned. This answers his efficiency question as: yes, do it in tandem — the tandem
part is that the transform records/reuses ids as it walks and never re-copies a name
between tables, because the tables are composed rather than cloned. Whether to push
all the way to deferred (pure) tandem is a real tradeoff, surfaced for him.

Psyche-owned: eager (dedup preserved, a bounded blessed string touch) or deferred
(pure no-strings-in-tandem, dedup/canonicalization moved to render). One word.

## 7. Question 6 — migration

What changes, in which repository, and how it sequences against the in-flight cascade
re-pin and the authorized `Core*`->`Encoded*` rename.

### 7.1 Per-repository changes

```
  protos / name-table
    Identifier(u32)            -> Identifier = enum { Schema(u16), Logos(u16), ... }
    NameTable (one Vec)        -> composition keyed by variant: a home (owned) variant
                                  nametree + borrowed read-only variant nametrees
    extend_from(base)          -> compose(borrowed variants) + fresh home variant [retire]
    intern                     -> append u16 into the home variant
    resolve                    -> exhaustive match on the variant, index the u16 local
    NameTableDomain            -> per-variant content identity (already the mechanism)
    variant set                -> the namespace registry, owned by sema's authority

  core-schema
    Universe.names             -> the schema's own variant (Schema)
    from_assignment            -> already assigns locals centrally; the assigned local is
                                  now the u16 carried by the Schema variant

  core-nomos
    NameTableBoundary::new      -> compose standard variant + schema variant + fresh
                                   home variant (stop cloning via extend_from)
    place_literal_name          -> composition; the package authoring variant is borrowed,
                                   so the round-trip through a string is gone
    leaf_path("Integer") + kin  -> reference standard::INTEGER and its pre-allocated kin
    field_names / transform_name/ derived-name allocation stays at the boundary, now
      route/short-header/etc.      writing into the logos home variant

  core-logos
    ships the logos standard slice: the standard nametree (content-identified sibling)
    and the generated Identifier constants the engine references (the LogosStandard
    variant, per the Q3 lean)
```

### 7.2 Content identity and vjvm

`Identifier` is rkyv-archived and rides inside every `Core`/`Encoded` value's
pre-image, so changing it from a `u32` newtype to a data-carrying enum (a discriminant
plus a `u16`) re-hashes every content identity in the family. This is a clean break,
which vjvm (no backward compatibility) blesses: no stored name-table or Core value needs
migrating — they are regenerated. Two properties are worth stating as gains, not merely
costs:

- Schema name ids become **variant-pinned** (`Schema(local)`, the authority-assigned
  `u16`) rather than interning-order-derived, so they are more stable, not less.
- Standard-object ids become **schema-independent** (the section 0 latent special case
  is dissolved): `Vec` has one fixed id everywhere, so logos content identity for its
  own vocabulary stops depending on schema size.

### 7.3 Sequencing

```
  in-flight cascade re-pin  ->  Core*->Encoded* rename (authorized, hash-stable)
                                        |
                                        v
                                slicing cascade (this design), its OWN re-pin
                                name-table -> core-schema -> core-logos -> core-nomos
                                        |
                                        v
                                language-engine-witness re-pinned as acceptance evidence
```

Land the `Core*`->`Encoded*` rename first: it is a pure, hash-stable rename that
touches the same files, and racing two breaking changes through one file set is the
avoidable risk. Slicing then rides its own cascade re-pin, because it is a
storage/wire break to `Identifier` (a versioning surface — the name-table wire and
every downstream content identity change, so the versioning skill's truthful-version
rule applies even though vjvm waives compatibility). The core-logos standard-slice
freeze (Q3) sequences with the core-logos step, since that is where the slice ships.
Portability: every producer pin (name-table -> schema -> logos -> nomos) advances in
order, and the witness re-pins to the new revision before its result is acceptance
evidence — the same discipline the current core-nomos ARCHITECTURE already records.

## 8. Decision slate — revised under the enum ruling (each answerable in a word)

Item 1 is **settled** (the identifier is a data-carrying enum, the variant is the
slice, inner `u16` local). It leaves the open slate. The remaining items are re-derived:
one is reshaped, one collapses into another, and three survive intact.

1. SETTLED — identifier is `enum { Schema(u16), Logos(u16), ... }`. Not open.
2. Standard-object placement (reshaped, absorbs the old ownership item) — a distinct
   `LogosStandard(u16)` variant (the literal "their own slice"; fixed, provably
   separate ids), or a reserved low range inside `Logos(u16)` (the "a slice of logos's
   own namespace" reading)?  Lean: variant.  Answer: variant / range.
3. Standard-slice shipment (survives) — content-identified sibling nametree with
   generated `Identifier` constants, or a plain runtime data file, or hand-written
   compiled constants?  Lean: generated.  Answer: generated / data / compiled.
4. Type-id mirror (reshaped from the old slice-axis-unification item, whose "grant"
   premise the enum removes) — should the type-id space (`ScopedCoreTypeId { universe,
   local }`) later adopt the same variant-enum shape as the name identifier, or stay
   numeric and separate?  Lean: separate (out of this slicing's scope; the ruling was
   about the name identifier).  Answer: mirror / separate.
5. Tandem derived names (survives) — eager materialization at the boundary (dedup
   preserved, the blessed string touch), or deferred to render (pure
   no-strings-in-tandem, canonicalization moved to render)?  Lean: eager.
   Answer: eager / deferred.
6. Sequencing (survives) — land slicing as its own cascade after the
   `Core*`->`Encoded*` rename, or fold both into one cascade?  Lean: after.
   Answer: after / fold.

Not psyche decisions (mechanism / prior rulings): single authority seated in sema, now
governing the **variant set** (the registry) rather than numeric grants; the variant set
as a compiled registry today, with Criome-authorized dynamic variant registration the
future propagation path; variant exhaustion (a language past ~65 000) as a per-variant
raise-then (widen the inner or add a continuation variant), not present machinery;
composition preserving the one-nametable-per-component ruling; borrowing variants rather
than copying them; the tandem ID-to-ID link design; the clean rkyv break under vjvm.

## Appendix — verified code facts

- `name-table` (repos/name-table, jj @ `110a3e471913`): `Identifier(u32)` is a newtype
  index (`src/identifier.rs`); `NameTable` is one `Vec<Name>` plus a derived index,
  append-only and index-stable, with `intern`/`resolve`/`extend_from` and
  `NameTableDomain` content-hash identity (`src/table.rs`); `NameResolver`/`NameInterner`
  are the two codec-boundary capabilities (`src/boundary.rs`); `NameTransaction` is the
  speculative overlay.
- `core-nomos` (repos/core-nomos): the engine builds the logos table via
  `NameTableBoundary::new -> NameTable::extend_from(schema_names)`; `name_boundary.rs`
  is the sole string home and re-materializes the standard atoms each run
  (`leaf_path("Integer"|"String"|"Boolean"|"Bytes")`, heads `Vec`/`Option`/`ScopeOf`,
  `Map`), plus the schema-derived affix builders (`route_enum_name`,
  `signal_object_name_literal`, `short_header_const_name`); the no-strings invariant is
  seated in `ARCHITECTURE.md`.
- `core-schema` (repos/core-schema): `CoreUniverse.names` is the schema NameTable;
  `from_assignment` already builds a universe from central-authority-assigned locals
  ("authority-provided universe"), the precedent for central assignment (`src/universe.rs`).
- `structural-codec` (repos/structural-codec): `ScopedCoreTypeId { universe:
  CoreUniverseId(u32), local: u32 }` in `src/ids.rs` is the type-id space; the settled
  name identifier is instead a variant-enum (slate item 4 asks whether the type-id space
  later mirrors it).
- `sema` (repos/sema): the seated typed storage kernel / authority home (`ARCHITECTURE.md`).
