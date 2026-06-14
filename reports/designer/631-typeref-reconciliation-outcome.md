# TypeReference reconciliation — outcome

The `TypeReference` conflict from the cross-lane review (`630` target #2/#3) is
reconciled into one designer branch set, building and testing green. Produced by a
worktree-isolated designer effort under the recipe in `630` plus the three settled
decisions (lineage / spelling / Map shape). Verified: branches and key changes
spot-checked directly; cargo green per the implementer.

## Branches produced (designer `next/` branches; main untouched)

| Repo | Branch | Change | What |
|---|---|---|---|
| nota-next | `next/combined-leaf-shapes` | `zqlqmvvp` / `70a246b6` | `HeadedAtom` + `PascalHeadBody` unioned (the two disjoint leaf derives serialized) |
| schema-next | `next/typeref-structural-generics` | `ypzukvmp` / `17b4ebc7` | reconciled `TypeReference` |

Tests (implementer-reported, branches spot-checked): nota-next `cargo test` **69
passed**; schema-next `cargo test` **159 passed** (generics, structural-macro, and
the reaction-frame fixture all green). `nix flake check` fails only on
**pre-existing, unrelated** source lints (`no-btree-canonical` on
`src/identity.rs`, untouched, fails identically on the base branch) — not
introduced here; cargo is the real signal for this change.

## What was folded

- **Base = `schema-generics`'s lineage** — keeps the generics intent: the
  `Application{head, arguments}` form, parameterized declaration heads,
  root-position application, the reaction-frame fixture + spirit pilot.
- **From `typeref-structural-macro` / `schema-next-polish`:** deleted
  `schema-generics`'s redundant hand-written `NotaDecode`/`NotaEncode` machine
  codec (replaced by thin delegators to the structural path); re-applied
  `SchemaError → thiserror` (51 `#[error]` in `engine.rs`, `thiserror = "2"`);
  the `(Bytes N)` leaf now decodes through the **HeadedAtom** derive.
- **Decisions applied:** full-English heads `Vector`/`Optional`/`ScopeOf`/`Map`;
  **flat `(Map K V)`** across all three lowering paths and both encoders, with all
  downstream `.schema` fixtures rewritten to flat Map (Spirit `wqdi`).
- So the reconciled grammar genuinely consumes **both** nota-next leaf derives —
  `PascalHeadBody` for the `(Foo A B)` application tail, `HeadedAtom` for the
  `(Bytes N)` numeric leaf.

## Three judgment calls — reviewed and blessed (designer)

1. **`ReferenceHead` vs derive-single-source (a real tension in my recipe).** The
   recipe asked for both "derive is the single source of truth" *and* "keep
   `ReferenceHead`," but neither rival branch had both (typeref *deleted*
   `ReferenceHead` when it adopted the derive). Resolution: the derives own the
   actual decode (application tail + bytes leaf); a *new* `ReferenceHead` owns
   **only reserved-head arity classification**, driving a wrong-arity guard so a
   malformed `(Map X)` is rejected rather than silently lowered as a generic
   application. Built-in heads still dispatch through `from_block`'s
   registry-aware recursive lowering — the real macro-expansion grammar, not a
   second codec. **Sound** — it dissolves my recipe's tension correctly.
2. **`TypeReference` is not itself a single `#[shape]`-derived enum — and can't
   be yet.** Its `Application{head, arguments}` is a *named-field* struct variant
   and `ApplicationHead` is a `Local`/`Imported` *sum*; the nota-next derive only
   supports unnamed/tuple variants with plain-name heads. So a hand-written
   `StructuralMacroNode` impl on `TypeReference` delegates the two macro forms to
   the derived `ApplicationNode`/`FixedBytesNode`. **Blessed as the right seam for
   now — and it is the notable finding (below).**
3. **Flat-Map consequence + `root.schema` layering.** With Map no longer
   arity-2-special-cased, `(Map X)` would become `Application(Map,[X])`; the
   reserved-head arity guard preserves the rejection (`map_with_wrong_argument_count_is_rejected`).
   `root.schema` keeps `(Map TypeReferencePair)` as the *enum-variant declaration*
   (the data-model description of the Map variant carrying a key+value pair) —
   distinct from the flat `(Map K V)` *source wire grammar*. Both correct in their
   own layer. **Sound.**

## The notable finding — `TypeReference` self-host is partial

The epic's goal is `TypeReference` becoming a pure structural form (its grammar is
data, decode is derive-driven). This reconciliation gets **most** of the way: the
`(Foo A B)` application tail and the `(Bytes N)` leaf are genuinely derive-driven.
But the **top-level** `TypeReference` decode keeps a hand-written delegating impl,
because the nota-next derive cannot express a node whose variants carry
*named fields* or a *sum-typed head* (`ApplicationHead`). So full self-host of
`TypeReference` requires a **future nota-next derive extension**: support
named-field `pascal_head`/`body` variants (and a sum-typed head). Until then, the
delegating impl is the honest seam — and it is a concrete, well-scoped instance of
the "tiny hand-written seed" the Structural Forms thesis (`627`) names: this is one
of the seed's current edges, with a clear path to shrinking it. Not blocking; a
candidate future nota-next slice.

## Operator handoff (ties to 630 action split)

The schema-next `Cargo.toml` `[patch]` points at the combined nota-next worktree
and is marked a **DESIGNER-PROTOTYPE SEAM**. To integrate: (1) operator lands
**both** nota-next leaf shapes on nota-next main (serializing the `derive/src/lib.rs`
textual conflict — runtime `src/` is byte-identical between the two source
branches); (2) drop the `[patch]` so the `branch = "main"` git dep carries both
derives; (3) integrate the reconciled `next/typeref-structural-generics` onto
schema-next main. This supersedes 630's #2/#3 "designer reconciles first" — the
reconciliation is done; what remains is the operator integration in that order.
