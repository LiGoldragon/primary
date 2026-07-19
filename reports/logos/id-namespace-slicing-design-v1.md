# ID Namespace Slicing — up-close design (v1)

Status: DESIGN ONLY. Nothing here is implemented. This is the up-close design the
psyche asked to see before any implementation ("Yes, and I want to see the design of
all that up close first"). Every recommendation below is a lean, not a decision; the
psyche-owned choices are gathered in the decision slate at the end, each answerable
in a word.

This design is written against verified code (revisions in the appendix), not prose.
Where it draws a picture it uses plain ASCII, never a rendered Protos surface, and it
quotes only real atoms that exist in the code today.

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
The reframe keeps one global keyspace but gives every identifier a slice and a local:

```
   TODAY                              PROPOSED
   Identifier(u32)                    Identifier { slice, local }
   = dense index into one Vec         = which block, and where inside it

   one flat table per component       one COMPOSED table per component,
   built by cloning schema's              built by composing slices:
   table and appending

   +------------------------+         +--------- component nametree view ---------+
   | schema names ...       |         | borrow: [ logos standard slice ] (r/o)    |
   | Vec Option String ...  |  --->   | borrow: [ schema slice ]         (r/o)    |
   | (logos tail, re-made   |         | own:    [ logos allocation slice ] (append)|
   |  every run, index      |         +-------------------------------------------+
   |  depends on schema)    |             one view, many slice-nametrees
   +------------------------+
```

The identity of a name never moves when a table composes it: a schema name keeps its
`(schema-slice, local)` because logos **borrows** the schema slice rather than copying
it. That is the literal realization of "the continuous identifier space" — continuous
because it is the *same* slice seen from two components, not because one component
copied the other's indices to matching positions.

Precedent already exists in the workspace: `ScopedCoreTypeId { universe, local }` in
`structural-codec/src/ids.rs` is exactly this shape for the **type-id** space (a
universe number plus a local). The name-id space is the one axis still flat. This
design brings the name-id space into the same shape sema already assigns type-ids in
(`CoreUniverse::from_assignment`, the authority-provided path).

## 2. Question 1 — slice topology

How the one global keyspace is carved.

### 2.1 The two representations

```
  Packed / CIDR form                 Struct-of-two form
  Identifier(u32)                    Identifier { slice: SliceId(u32), local: u32 }
  [ p prefix bits | 32-p local ]     [ full u32 slice ][ full u32 local ]
  self-describing slice by bit-mask  self-describing slice by field
  caps: 2^p slices, 2^(32-p) locals  caps: none of practical concern
  smallest wire                      64-bit, mirrors ScopedCoreTypeId exactly
```

The packed form is the literal letter of the IP analogy — a fixed-width prefix like a
CIDR network number, the slice recoverable by masking. Its cost is the analogy's own
warning: an 8-bit prefix is 256 slices (IPv4-scale scarcity), and stealing bits for
more slices shrinks every slice. Range-registry allocation (variable blocks recorded
in a table) is the third option and is rejected outright: it needs a lookup to answer
"which slice owns this id", which is a per-resolve coordination the whole point is to
avoid, and it violates the self-describing property the analogy insists on.

### 2.2 Is u32 wide enough

For the *local* axis, u32 is ample (4 billion names in one component's own slice). The
real width question is whether the *slice* selector shares the local's u32 (packed) or
gets its own (struct). Slicing does not force a wider *local*; it forces a decision
about where the slice selector's bits come from.

### 2.3 Recommendation

Struct-of-two: `Identifier { slice: SliceId(u32), local: u32 }`. Three reasons:

- It removes exhaustion pressure from both axes, so slice-exhaustion stops being a
  scenario the design must special-case (see Q2).
- It is byte-for-byte the shape the workspace already proved in `ScopedCoreTypeId`.
  One shape for the two id families is the harmony lta7 asks for, and it opens the
  unification in Q6 (one grant, both id families).
- The packed-CIDR form is then a pure **wire projection** of the same structure — if
  archived size ever bites, an `Identifier` packs to a u32 at a codec boundary without
  changing the in-memory model. Nothing is lost by choosing the struct first.

Psyche-owned: struct (analogy's spirit, workspace harmony) or packed (analogy's
letter, smallest id). One word.

## 3. Question 2 — allocation authority

How the central authority delegates slices, and how a holder allocates locally.

### 3.1 The delegation picture

```
        sema  (single seated allocation authority — prior ruling)
          |  grants a slice (a block of the keyspace) to a component
          v
   +--------------+   +--------------+   +--------------------+
   | schema slice |   | logos std    |   | logos alloc slice  |
   | (granted)    |   | slice (grant)|   | (granted)          |
   +--------------+   +--------------+   +--------------------+
   holder appends locals within its own slice, 0 coordination
```

Identity is the id and there is one keyspace (prior ruling). sema mints slice grants;
a grant is a typed delegation record, not a hardcoded constant. Once a component holds
a slice it allocates locals by appending to that slice's own nametree — precisely
today's `intern` (append + dedup), now scoped to the holder's slice. No allocation
touches sema; coordination happens once, at grant time, exactly as an RIR delegates a
subnet once and the holder assigns hosts freely.

"criome-authorized propagation is in the future" fixes a constraint on the record
shape, not on today's behavior: a slice grant must be a **delegation** that can itself
be re-delegated later (Criome authorizing a holder to sub-grant), even though today
only sema mints. The design must not bake a single-minter assumption into the grant
type; it must bake it into current policy alone.

### 3.2 Slice exhaustion

With the struct-of-two representation a slice never runs out of locals in practice. If
a holder ever did exhaust a slice, it requests a second slice — and a component holding
two slices is *already* the composable model from Q4. Exhaustion therefore dissolves
into ordinary multi-slice composition rather than becoming a special path (lta7). This
is the strongest single reason to prefer the struct representation in Q1: it turns the
one genuinely ugly failure mode into the normal case.

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

### 4.2 How it ships — three options

```
  (a) compiled-in constants        (b) runtime data file        (c) content-identified
      pub const STRING: Identifier      load a serialized            NameTableDomain sibling
        = ...in the std slice;          nametree at startup          shipped + versioned by hash
      engine references directly    string lookups at runtime    the co-versioning discipline
                                                                  name-table already has
```

### 4.3 Recommendation

Ship the logos standard slice as a content-identified `NameTableDomain` sibling (c) —
the co-versioning mechanism `NameTable::identity()` already provides — and **generate**
the compiled-in `Identifier` constants (a) from it as the engine's reference surface.
The sibling nametree is the single source of truth (its content hash is its version);
the constants are its deterministic projection (w312: derivable, so mechanism, not
hand-authored). Nomos then references `standard::STRING` directly and never interns the
string "String" again. The pure data-file (b) alone is rejected: the engine wants a
compile-time typed reference, not a runtime string lookup, and (c)+(a) gives both a
versioned artifact and a typed reference.

Psyche-owned within this: does **logos own** its standard vocabulary (sema grants only
the block number, logos fills and versions the block), or does **sema own/freeze** the
vocabulary? Lean: logos owns the contents, sema grants the slice — single allocation
authority over *blocks* without sema needing to know logos's vocabulary.

## 5. Question 4 — composability

How per-slice nametrees compose into a component's one NameTable, and how that
preserves the one-nametable-per-component ruling.

### 5.1 The composed view

```
   component nametree (ONE view, the ruling's "one NameTable per component")
   +---------------------------------------------------------------+
   |  slice map:  SliceId -> slice-nametree                        |
   |                                                               |
   |   [ logos standard slice ]  borrowed, read-only               |
   |   [ schema slice ]          borrowed, read-only               |
   |   [ logos alloc slice ]     owned, append target (home slice) |
   +---------------------------------------------------------------+

   resolve(id)  = slices[id.slice].names[id.local]      (pick slice, index local)
   intern(name) = append into the HOME slice only       (foreign slices are read-only)
```

`resolve` selects a slice by `id.slice` and indexes by `id.local` — each slice keeps
today's dense `Vec<Name>`, so the fast path inside a slice is unchanged. `intern`
targets the component's **home** (owned) slice; borrowed slices such as the standard
slice or the schema slice are never appended to, which is why a standard object is
referenced by its fixed id and never re-interned.

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
    Identifier(u32)            -> Identifier { slice: SliceId(u32), local: u32 }
    NameTable (one Vec)        -> composition: SliceId -> slice-nametree,
                                  a home (owned) slice + borrowed read-only slices
    extend_from(base)          -> compose(borrowed slices) + fresh home slice  [retire]
    intern                     -> append into the home slice
    resolve                    -> dispatch by id.slice, index id.local
    NameTableDomain            -> per-slice content identity (already the mechanism)

  core-schema
    Universe.names             -> the schema's own granted slice
    from_assignment            -> already assigns locals centrally; extend the grant to
                                  carry the slice id alongside the local

  core-nomos
    NameTableBoundary::new      -> compose standard slice + schema slice + fresh alloc
                                   slice (stop cloning via extend_from)
    place_literal_name          -> composition; the package authoring slice is borrowed,
                                   so the round-trip through a string is gone
    leaf_path("Integer") + kin  -> reference standard::INTEGER and its pre-allocated kin
    field_names / transform_name/ derived-name allocation stays at the boundary, now
      route/short-header/etc.      writing into the logos alloc slice

  core-logos
    ships the logos standard slice: the standard nametree (content-identified sibling)
    and the generated Identifier constants the engine references
```

### 7.2 Content identity and vjvm

`Identifier` is rkyv-archived and rides inside every `Core`/`Encoded` value's
pre-image, so changing its layout re-hashes every content identity in the family. This
is a clean break, which vjvm (no backward compatibility) blesses: no stored name-table
or Core value needs migrating — they are regenerated. Two properties are worth stating
as gains, not merely costs:

- Schema name ids become **authority-pinned** `(slice, local)` rather than
  interning-order-derived, so they are more stable, not less.
- Standard-object ids become **schema-independent** (the section 0 latent special case
  is dissolved): `Vec` has one id everywhere, so logos content identity for its own
  vocabulary stops depending on schema size.

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

## 8. Decision slate (psyche-owned, each answerable in a word)

1. Slice representation — `Identifier { slice, local }` struct (workspace harmony with
   `ScopedCoreTypeId`, no exhaustion), or packed-CIDR u32 (the literal IP analogy,
   smallest id)?  Lean: struct.  Answer: struct / packed.
2. Standard-slice ownership — logos owns and versions its standard vocabulary (sema
   grants only the block), or sema owns/freezes it?  Lean: logos.  Answer: logos / sema.
3. Standard-slice shipment — content-identified sibling nametree with generated
   `Identifier` constants, or a plain runtime data file, or hand-written compiled
   constants?  Lean: generated.  Answer: generated / data / compiled.
4. Slice-axis unification — one sema grant covers both a component's type-ids and its
   name-ids under one slice number, or two parallel independent grants?  Lean: unify.
   Answer: unify / parallel.
5. Tandem derived names — eager materialization at the boundary (dedup preserved, the
   blessed string touch), or deferred to render (pure no-strings-in-tandem,
   canonicalization moved to render)?  Lean: eager.  Answer: eager / deferred.
6. Sequencing — land slicing as its own cascade after the `Core*`->`Encoded*` rename,
   or fold both into one cascade?  Lean: after.  Answer: after / fold.

Not psyche decisions (mechanism / prior rulings): single allocation authority seated in
sema; slice grants as re-delegatable records for future Criome propagation; slice
exhaustion resolved by requesting a second slice (which composition already handles);
composition preserving the one-nametable-per-component ruling; the clean rkyv break
under vjvm.

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
  CoreUniverseId(u32), local: u32 }` in `src/ids.rs` is the proven struct-of-two shape
  this design mirrors for the name-id space.
- `sema` (repos/sema): the seated typed storage kernel / authority home (`ARCHITECTURE.md`).
