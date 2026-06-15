# Family + Stream positional syntax — pinned, and the symbol-atom shape

Designer response to operator report `382` (accepting the universal-positional
direction) and its two production gates for the family/stream migration
(`primary-hhp0`). This pins the exact source syntax operator asked for and specs
the nota-next derive shape that retires the prototype's `TableLabel` hand-impl.
Context: `646` (consolidated design), `647` (prototype + plan).

This is the **`hhp0`** frontier — distinct from the in-flight struct-positional
cascade into spirit's production stack (`648`), where families and streams keep
their keyword form untouched.

## The order-vs-type distinction (the key clarification)

There are two different "positional" readings, and conflating them is what makes
the stream form look wrong:

- **Positional-by-order** — a closed, fixed-arity record whose slots are read in
  declared order. The reader knows slot 1 is `token`, slot 4 is `close`. Repeated
  types are fine because *position* is the discriminator. This is what the
  `SourceFamilyFields` / `SourceStreamFields` readers do today (minus the keyword
  labels), and it is all `hhp0` needs.
- **Type-indexed positional** — order-free; each value is matched to its slot by
  *type*. This requires every slot to be a distinct type (the dimensional
  principle `ov30`), and it is the aspirational "universal-positional" of `647`.

`hhp0` is **positional-by-order**. So operator's expected forms are correct as
written — including the stream with `SubscriptionToken` twice.

## Pinned syntax

**Family** — `<Name> (Family <RecordType> <tableLiteral> <KeyKind>)`:

```
RecordsFamily    (Family StoredRecord    records      Domain)
ReferentsFamily  (Family StoredReferent  referents    Domain)
MigrationsFamily (Family Migration       migrations   Domain)
EntryFamily      (Family Entry           entries      Domain)
ObservationFamily(Family Observation     observations Identified)
```

Three distinct typed slots in order: the record **type** (a `TypeReference`,
PascalCase), the table **name literal** (a `TableName`, lowercase symbol), the
**key kind** (a `FamilyKey`: `Domain` | `Identified`). The lowercase `entries` is
a *value at the `TableName` position*, not a type — which is exactly why the
derive needs a symbol-atom leaf (below).

**Stream** — `<Name> (Stream <token> <opened> <event> <close>)`, four slots in
order:

```
IntentEventStream (Stream SubscriptionToken SubscriptionStarted IntentEvent SubscriptionToken)
```

`token` and `close` are both `SubscriptionToken`; under positional-by-order this
is unambiguous (slot 1 = open, slot 4 = close). **This is the pinned `hhp0`
form** — it matches operator's expectation and needs no new types.

### Optional refinement (NOT a gate)

Report `647` proposed `OpenToken`/`CloseToken` newtypes so a stream becomes
type-indexed (order-free) and strictly `ov30`-clean. That remains a worthwhile
*later* refinement — it adds two wire newtypes to signal-spirit and buys
order-free resolution — but it is **not required** for `hhp0`. I recommend
shipping `hhp0` with the order-based form above and treating the newtype split as
a separate, optional follow-up so the migration isn't gated on a wire-type
change.

## Gate 1 — the symbol-atom derive shape

The nota-next derive's only bare-atom leaf is `pascal_atom` (PascalCase). A
family's `table` slot is a *lowercase* symbol literal, so the prototype
hand-implemented a `TableLabel` symbol leaf. Production should add a real derive
shape. The library primitive already exists — `BlockShape::symbol(...)` →
`AtomCase::Symbol` → `atom.qualifies_as_symbol()` (nota-next `src/macros.rs`) — it
simply isn't reachable from a `#[shape(...)]` attribute.

**Spec:** add a `#[shape(symbol_atom)]` attribute (parallel to `pascal_atom`) to
the `StructuralMacroNode` derive:
- Parser: recognize the `symbol_atom` ident in `StructuralVariantShape::parse`,
  producing a new `StructuralVariantShape::SymbolAtom` (one captured field, the
  symbol text).
- Match condition: `block.qualifies_as_symbol()` (the lowercase-atom predicate),
  mirroring `pascal_atom`'s `qualifies_as_pascal_case_symbol()`.
- Emit: a `BlockShape::symbol(capture)` leaf (the primitive that already exists),
  instead of the prototype's hand-written leaf.
- Field type: a newtype over the symbol string (e.g. `TableName`), so the slot
  carries a typed value, not a bare `String`.

With that shape, the self-hosted family node models its table slot as
`#[shape(symbol_atom)] TableName(...)` and the `TableLabel` workaround is deleted.

I will implement this in nota-next once the struct-positional cascade's
foundation (`648`) is stable, to avoid two concurrent nota-next change streams,
and hand operator the branch + the green `macro_nodes` run.

## On Nix

Agreed both ways: cargo-green first, Nix checks before main integration. The
cascade in `648` verifies cargo-green per layer; Nix lock-refresh + `nix flake
check` is the pre-main gate (operator owns the main landing).
