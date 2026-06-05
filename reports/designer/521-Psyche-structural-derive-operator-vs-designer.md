---
title: 521 — Structural macro node derive — operator's landed version vs designer's
role: designer
variant: Psyche
date: 2026-06-05
topics: [nota, structural-macro, macro-node, derive, nota-next, comparison, conflict-detection, intent]
description: |
  Review of the operator's landed #[derive(StructuralMacroNode)] (nota-next
  main f0668055) against the designer's (branch structural-macro-nodes
  add64661). The operator adopted my #[shape] front-end verbatim and kept
  their captures/string-dispatch back-end, plus added exact-duplicate
  conflict detection. The decode fork from 518/519 persists; i0e6 favors
  the direct path. Recommended synthesis + an intent-duplication flag.
---

# 521 — Structural derive — operator's landed version vs designer's

The operator landed `#[derive(StructuralMacroNode)]` on nota-next main
(`f0668055`, version 0.2.1). This compares it to mine (branch
`structural-macro-nodes`, `add64661`). All findings are from the actual
landed code at `f0668055`, not summaries.

## Bottom line

Main now carries **my `#[shape]` front-end + the operator's
captures/string back-end + their conflict detection.** The decode fork
from reports 518/519 persists, and the psyche's clarification `i0e6`
(the type drives the decode) favors the path the operator did *not* take.
The operator's conflict detection is a real value-add but narrower than it
looks. Recommended end-state: keep the shared front-end and the conflict
detection, swap the decode to the direct typed path.

## What's the same — my front-end landed

The operator adopted my user-facing surface verbatim. In their
`derive/src/lib.rs` the `#[shape(...)]` attribute parsing
(`StructuralVariantShape`), `check_field_count`, `encode_body`, and even
the error strings are **word-for-word mine** — e.g. `"head shape needs
arity = N"`, `"shape must be pascal_atom, head = \"...\" with arity, or
pascal_head with arity"`. Independent convergence does not produce
identical error wording; the operator built on my pushed branch. That is
a good collaboration outcome: my contribution is in main. The
`#[shape(pascal_atom | head="X" arity=N | pascal_head arity=N)]` vocabulary
is now shared.

## The persistent fork — decode back-end

This is the same fork reports 518/519 named, now visible in the generated
code:

| | Operator (`f0668055`) | Designer (`add64661`) |
|---|---|---|
| Variant data | `StructuralVariant{ name: String, pattern: Pattern, expected }` — reuses the registry `Pattern` (Any/Atom/Delimited/Literal/Rest + captures) | `BlockShape` (3 cases) on the raw `Block` predicates |
| Dispatch | `StructuralVariantSet::dispatch` → `MacroMatch` (captures + name) | inline in the derived `from_structural_block` |
| Decode | generated `from_structural_match` = **`match matched.macro_name()`** (string), then reads captures per arm | generated `from_structural_block` **fuses** the shape match with typed construction; no `MacroMatch`, no captures, no string |
| Hops | variant → Pattern → MacroMatch → string match → captures → typed | shape match → typed, one hop |

The operator's generated `from_structural_match` (line 697) literally is
`match matched.macro_name() { … }` — the string-matching-as-dispatch
anti-pattern (`skills/enum-contact-points.md`,
`skills/rust/methods.md` §"Don't hide typification in strings"), now
emitted by the derive. The psyche's `i0e6` says the type drives the
decode — "a structural match on each variant" — which is the fused,
direct path (mine), not a structural match thrown away and recovered from
a variant-name string.

## The operator's real value-add — but narrower than it looks

The operator added `StructuralVariantSet::validate_no_silent_conflicts`,
which mine lacks entirely. But read what it catches (`macros.rs:472`):

```rust
if first.pattern() == second.pattern() {   // EXACT pattern equality
    return Err(Conflict(...));
}
```

It catches **exactly-identical patterns** — two variants with the same
shape, where the second is dead code. That is a genuine footgun mine
ignores (mine would silently make the second variant unreachable). Credit
where due.

But it does **not** catch the *subset/shadowing* overlap — a general head
(`pascal_head`) declared before a specific head (`head="Optional"`) it
subsumes. Those patterns are not equal, so the check passes them, and the
general variant silently shadows the specific one by declaration order.
That is exactly what my `MisorderedReference` demo shows happening — and
it is the more dangerous case, because it looks correct. The operator
knows this limit (report 312, next-move-4: "catches exact duplicate
patterns… does not yet explain broader overlaps"). So: **operator catches
exact duplicates; neither catches shadowing.**

## The Pattern-vocabulary difference

The operator's `StructuralVariant` carries a full `Pattern` (rkyv +
NOTA-serializable, with captures, `Rest`, `Literal`), so it can express
richer shapes than my three `BlockShape` cases — at the cost of the
captures-extraction layer. Mine is minimal and would need extension
(per-slot sub-shapes, sigils) for the richer schema positions. Neither is
complete for all of schema's sugar yet; the operator's is closer to
expressive, mine is closer to direct.

## Intent duplication — `js6q` vs `pv61`

The operator captured Spirit record `js6q` for the Asschema decision
("Asschema is no longer the intended intermediate language; schema should
stay specialized NOTA through typed structural macro node codecs"). I
captured `pv61` for the same psyche decision, with more detail (the
resolution work must be preserved; it supersedes the operator's
keep-Asschema recommendation). **These two records cover the same
decision** — a duplication like the earlier `24ds`. I am not removing
`js6q` (it's the operator's capture; supersession needs coordination per
`skills/intent-maintenance.md`). Flagging for consolidation: `pv61` is the
fuller record; one should subsume the other in a coordinated step.

## Recommended end-state

Main is the right base (my surface + their back-end + conflict detection
all landed). The one improvement, consistent with `i0e6` and 518/519:

1. **Swap the generated decode** from `from_structural_match` on
   `macro_name()` to the direct typed `from_structural_block` (fuse match
   + construction) — removes the captures layer and the string dispatch.
2. **Keep and strengthen the conflict detection** — extend
   `validate_no_silent_conflicts` from exact-pattern-equality to
   *subset/shadowing* detection (a general shape declared before a
   specific one it subsumes is the real footgun). This is the genuinely
   valuable part to preserve and grow.
3. **Keep the shared `#[shape]` front-end** and the richer `Pattern`
   vocabulary for positions that need captures/`Rest`.

The synthesis is: my direct typed decode + the operator's (strengthened)
conflict detection + the shared front-end.

## My branch status

`structural-macro-nodes` (`add64661`) is now largely **superseded** — the
operator landed my front-end on main with their back-end. Its remaining
distinct value is the direct `from_structural_block` decode and the
explicit shadowing demo; those should be **folded into main's derive**
(recommendation 1 above), not maintained as a separate branch. I'll
abandon the branch once the direct-decode recommendation is accepted or
declined.

## Where things live

- Operator: nota-next `f0668055`, report `reports/operator/312-...`.
- Designer: branch `structural-macro-nodes` (`add64661`), reports
  517/518/519. Asschema removal design: 520. Decisions: `pv61` (Asschema),
  `i0e6` (type-directed), `ejvc`/`lcwu` (mechanism).
