# 102/6 — TypeReference becomes a structural macro (the v0n6 close-out)

*The last hand-parsing site for type references, eliminated. Implemented after
reading the touching intent (the psyche: "make sure you're all read on any
intent touching this, and implement"), which reshaped the plan: drop the
aliases (`qz6j`) rather than add alias-set vocabulary, and extend the derive
only for the one shape it genuinely couldn't express.*

## What the intent decided

- **`v0n6` (Clarification, High):** "Everything reading NOTA-shaped structure
  above the raw structural parser must go through typed structural macro nodes;
  surviving hand-parsing sites … are design violations to fix. If structural
  macro nodes cannot express a needed shape, that signals the NOTA design was
  not implemented properly and must be surfaced to the psyche." → the
  hand-rolled `TypeReference` head-dispatch must become a derived node, and the
  derive must be *extended* (not worked around) where it falls short.
- **`qz6j` (Decision):** aliases lose the safe bare form and "are dropped." →
  **do not** add "head alias-set" vocabulary; use one canonical head per
  variant. The alias spellings drop out naturally. Usage data confirmed this is
  near-zero ripple (`Vector` 0 files, `KeyValue` 0, `Option` 1, `ScopeOf` 1, vs
  `Vec` 35 / `Optional` 14). Recorded as a pattern-based decision.

## What landed

| Repo | Branch | Head | Ver | Verdict |
|---|---|---|---|---|
| nota-next | `typeref-shape` | `3e18e370` | 0.5.0 (derive 0.3.0) | approve |
| schema-next | `typeref-structural-macro` (on `schema-next-polish`) | `5baef265` | 0.4.0 | approve |

**nota-next** — the *one* genuine derive gap was a headed variant carrying a
single **numeric/atom leaf** (`(Bytes 32)` → `FixedBytes(u64)`): `Headed { head,
arity }` decodes every child as a `StructuralMacroNode` sub-node, and a `u64`
width is a primitive leaf, not a sub-node. Added the minimal
`#[shape(head = "…", atom)]` → `HeadedAtom { head }` form (one canonical head,
no alias set; decode via the field's `FromStr`, encode via `Display`; dispatch
still generated). Everything else was already expressible: `Vec`/`Optional`/
`Scope` = `Headed` arity 1, **`Map` = `Headed` arity 3** (flat `(Map K V)`, no
named-field form needed), scalars/`Plain` = `pascal_atom`, bare `Bytes` =
keyword. Six new round-trip tests; suite 65/0.

**schema-next** — `TypeReference` now `#[derive(StructuralMacroNode)]` with one
`#[shape]` head per variant; the `NotaDecode`/`NotaEncode` impls delegate to the
derived codec. `ReferenceHead` + `classify` and the three head-dispatch sites
are **deleted** — `from_parenthesis_objects`, the macro-template expansion path,
and `SourceReference::from_block` all route through the derive (and
`SourceReference::to_schema_text` delegates to the derived encode, so source and
derive can't disagree). 12 round-trip witnesses in
`tests/typeref_structural_macro.rs`, including assertions that the dropped
aliases (`Vector`/`Option`/`ScopeOf`/`KeyValue`) and nested `(Map (K V))` now
**fail** to parse. Full suite 147/0; no new clippy/compiler warnings.

## Grammar changes (intended, bounded)

- **`Map` flattened** `(Map (K V))` → `(Map K V)` — 4 schema-next fixtures + docs
  updated in-repo. No live component `.schema` uses `Map` (grep: 0 files), so the
  only break was the schema-next fixtures (fixed).
- **Aliases dropped** — only two downstream files use a dropped spelling and need
  canonicalization when they regenerate against schema-next 0.4.0:
  `signal-spirit/schema/domain.schema` (`ScopeOf` → `Scope`) and a
  `meta-signal-spirit` concept schema (`Option` → `Optional`). Named as
  separate-repo follow-ons, not edited here.
- **Pre-existing staleness** (out of scope, noted): `schema-next
  schemas/root.schema:19` self-describes the `TypeReference` enum with
  variant-signature names that already drifted (missing `Bytes`/`FixedBytes`/
  `ScopeOf`) before this change — a self-description refresh follow-on.

## Integration

The schema-next final tip is `typeref-structural-macro` @ `5baef265` (stacks on
`schema-next-polish`), pinning nota-next `typeref-shape` @ `3e18e370`. Integration
order: nota-next first, then schema-next; canonicalize the two downstream alias
files before/at component regeneration. Folded into `primary-qu28`; `primary-xzzf`
closed.

## Arc status

The designer-side SEMA-VC audit arc is now complete: audit (102/1–2), the
suggestions (102/3), the clear tasks incl. the gated shipper (102/4), the
god-impl split (102/5), and this. What remains is not designer work: operator
integration of the branch tower (`qu28`), and the deploy gate to make remote
durability live — the psyche's ingress-auth-mechanism choice (`x3l7`: tailnet
bind now / BLS as the hardening), then enabling the `mirror-shipper` feature.
