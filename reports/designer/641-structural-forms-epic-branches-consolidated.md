# Structural-forms epic branches consolidated — green and pushed

Per the directive to implement the decided designs in the worktrees, move to
latest main, reuse the decided changes, and name the branches after the epic.
Mains had **not** moved (nota-next `3d6c2cd`, schema-next `f460e7b`,
schema-rust-next `00763d6` all unchanged), so "move to latest main" was a no-op
and the branch bases were already current. Both repos now carry one epic branch,
`next/structural-forms`, consolidating the decided work — built, tested, pushed.

## What landed

| Repo | Epic branch | Tip | Stack | Tests |
|---|---|---|---|---|
| nota-next | `next/structural-forms` | `9d09e944` | leaf shapes (HeadedAtom + PascalHeadBody) → named-field variants → **struct support** | 74 pass, clippy clean |
| schema-next | `next/structural-forms` | `44ac4c65` | TypeReference reconciliation (`17b4ebc` fold-ins) → prototype-seam patch repointed | 121 pass |

Both pushed to origin. The reuse worktrees are reused (not new), now epic-named
where they were renamed last session (`named-field-structural-derive`,
`typeref-structural-generics`).

## New capability this pass: struct-level derive

The `StructuralMacroNode` derive was enum-only. It now supports **structs**: a
struct decodes as a **positional typed body** — the candidate's blocks map
one-to-one onto the fields in declaration order, each decoded by its type;
`from_structural_block` unwraps a block to its root objects; `to_structural_nota`
emits the fields space-joined with no wrapper (the enclosing position supplies
the delimiter). Named and tuple structs both work.

This is the real-consumer next step `635`/`637` identified (not the
consumer-less named-field gap). It is proven two ways in the tests: a struct
decodes a positional body and round-trips, and a **derived** struct slots into a
headed-body enum payload — exactly the slot where a *hand-written* struct impl
(the test's `DerivedSignature`, or schema-next's `SchemaMacro`) was previously
required.

**Honest scope note:** this lands the derive *capability*, proven as a consumer
pattern. Actually retiring schema-next's `SchemaMacro` hand impl is the immediate
follow-on — it needs `Name` and `MacroPosition` to become structural nodes (the
`schema_name`/`Name` wiring quirk flagged in `637`), a small schema-next task.

## The prototype-seam fix

Renaming the nota-next worktree last session broke schema-next's `[patch]` (it
pointed at the old `typeref-shape` path). Repointed it at the nota-next epic
worktree `named-field-structural-derive` (which carries the full epic), and
refreshed the seam comment. Still a designer prototype seam — operator drops it
once the nota-next epic lands on main.

## The divergence is resolved on the designer side

The `634`/`635` flag — operator's `structural-forms-integration` did not contain
the reconciliation `17b4ebc` — is now moot from the designer side: the epic
branch carries the reconciliation cleanly and is the single branch operator
integrates from. (Operator still needs to integrate the epic, not the older
`structural-forms-integration` line.)

## What remains — pending decisions

1. **Positional type-prominent struct syntax (`640`)** — needs the **separator
   locked** before implementation. Designer-prototype blast radius: the
   struct-body reader (`MacroExpansionFields::lower`), the encoder, `root.schema`,
   and schema-next's own fixtures. The cross-repo `.schema` migration (every
   repo with schemas) is a separate operator-scale rollout where the separator
   would be final.
2. **Recording the principles (`639` dimensional principle + `640` syntax)** —
   pending green-light; they sharpen, not duplicate, the newtype rule.

Both are the psyche's calls; everything that was decided is implemented, green,
and pushed.
