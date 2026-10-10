# Overview — recent intent, reports, and branch state

## What was dispatched

Psyche asked pi-operator to read recent intent, operator reports, designer reports, nota-designer reports, and their working branch state, using subagents.

I launched four asynchronous read-only scout subagents:

- recent Spirit intent;
- operator reports and branch state;
- designer reports and branch state;
- nota-designer reports and branch state.

The operator subagent returned only a locator, so I filled that slice directly in `2-operator-reports-and-branch.md` from the same evidence set.

## Current durable intent

The latest Spirit intent says the current stack is a schema/NOTA restack, not a continuation of the old authored-Features design.

The load-bearing direction:

- NOTA is a thin structural library over delimiter-bounded blocks and atoms.
- Raw NOTA exposes delimiter kind, source span, object counts, child shape, and `qualifies_as_*` predicates.
- Raw NOTA does not decide final semantic type, PascalCase legality, enum-variant meaning, or string-vs-symbol context.
- Schema/macros consume those raw structural facts and lower toward `Asschema` / `AssembledSchema`.
- Schema files are read under an implied root `Schema` struct supplied by `.schema` context; field ordering is still open, with imports/exports-first only the current lean.
- Schema-derived Rust emission is a fresh top-down composer from assembled schema, not reuse of `signal_channel!`.
- Authored schema `Features`, `EffectTable`, `FanOutTargets`, and `StorageDescriptor` are retracted as user-facing schema surface.
- New Spirit-facing schema-derived work should target the clean repos `spirit`, `signal-spirit`, and `core-signal-spirit`; old persona-prefixed repos are maintenance surfaces unless explicitly named.
- Major architectural breaks may use new `-next` / `-v2` style prototype repos; `nota` specifically uses the existing repo's `nota-next` branch.

## Operator state

Operator report `198` is the current implementation-facing center. It lands the first real NOTA structural-library slice on the schema operator worktree.

Important branch:

- `/home/li/wt/github.com/LiGoldragon/schema/operator-schema-driven-nota-parser-prototype-2026-05-26`
- Clean working copy.
- Branch/bookmark `operator-schema-driven-nota-parser-prototype-2026-05-26` at `skqzqpok` / `9dcc0244` (`schema: match macro shapes through structural nota blocks`).
- Empty `@` descendant at `pqvlstmr` / `be3df64b`.

What operator has made real:

- `SchemaBlockPass` with source spans and recursive shape predicates.
- `QualifiedSymbol` / `SymbolClass` candidate logic.
- `SchemaMacroPattern` over raw block objects.
- A narrow namespace matcher proving schema lowering consumes block facts before assigning meaning.
- Compiled-fixture reader tests from report `195` plus structural/macro tests from report `198`.

The remaining operator gaps are still substantial: unify block and value trees, stabilize `Asschema`, remove old Feature acceptance/tests, settle bracket string/vector behavior, and update repo-local guidance that still teaches the old six-position schema shape.

## Designer state

Designer report `357` is the latest design refinement and supersedes the looser `/353` three-peer-section framing. The current design says schema files are a root struct implied by `.schema`, not explicitly wrapped and not permanently represented as three peer sections.

Important designer reports:

- `350` retracts authored schema `Features` and effect/fan-out schema drift.
- `351` relocates misplaced intent into the repo that owns it and flags uncertain file-intent surfaces for psyche review.
- `352` audits Spirit records and flags duplicates/hallucinations without superseding them.
- `353` establishes the all-the-way-back schema-derived NOTA direction.
- `355` critiques operator `195` and names the missing next slices.
- `357` is the current refined target: NOTA as structural library, schema-schema/core Rust as macro interface, implied root struct, field ordering uncertainty carried.

Primary branch state during this pass:

- `main` at `wmlvvqvy` / `3999552f` when the subagents first inspected it, later advanced by operator work to `zsyznnns` / `972e32bb` (`report operator/199: nota core schema implementation target`).
- This pi-operator meta-report is being separated from concurrent designer-assistant skill/report edits in the same working copy.

Designer-related source state observed:

- `/git/github.com/LiGoldragon/schema` is currently on designer prototype bookmarks `designer-schema-derived-nota-2026-05-26` and `designer-schema-schema-prototype-2026-05-26`, with dirty prototype block-parser files under `prototype/`.
- The pushed schema intent cleanup branch from designer report `351` is `designer-intent-cleanup-2026-05-26` at `1b5c8037`, awaiting operator integration.
- `/349` per-repo sweep branches should not be blindly fast-forwarded now because `/350` and `/351` later retract or flag Features-based content.

## Nota-designer state

Nota-designer's latest report `9` is still the most direct note for pi-operator: the operator captured the schema/NOTA shape-logic intent mostly correctly, and the boundary is clear.

The boundary:

- `nota-codec::NotaValue` / raw structural values are the shape-inspection substrate.
- The schema macro engine is the next layer and must consume those predicates in macro positions.
- Reports must distinguish implemented behavior, tested behavior, design intent, and uncertainty.

Nota-designer report `8` is older and now partially stale because it still describes six fixed schema fields and Feature surfaces. Its durable value is the ownership boundary: schema owns lowering and assembled shape; `signal-frame-macros` should become an adapter over `schema`, not a private schema parser.

Adjacent checkout state noted by the nota-designer scout:

- `/git/github.com/LiGoldragon/nota-codec` has an active `nota-codec-intent-synthesis` working copy with `A INTENT.md`; that file reportedly still claims legacy quote acceptance and conflicts with current quote-rejection code/intent.
- `/git/github.com/LiGoldragon/signal-frame` is clean on main, with schema-derived branches present but not current.

## Practical read for pi-operator

The safe synthesis is:

1. Treat `/357`, `/198`, and Spirit records `799-811` as the current top of stack.
2. Use the operator schema worktree as the implementation base when asked to implement this path.
3. Port concepts from designer prototypes, not whole prototype crate shape.
4. Do not revive authored `Features` or old signal macro reuse.
5. Keep `Asschema` central: the fully resolved, order-preserving, macro-free target object.
6. Treat guidance drift as a blocker for future agents: repo `schema` docs, NOTA quote docs, and owner/core terminology still need cleanup before more agents build from them.

## Open coordination notes

- Operator holds locks on the operator schema worktree, the operator nota-codec worktree, and `reports/operator`; pi-operator should stay read-only there.
- The Primary working copy had concurrent designer-assistant edits while this report was written. This meta-report is intentionally split into a pi-operator-only commit before pushing.
- The subagent run fulfilled the requested fanout, but one child failed to provide substance; the orchestrator-filled operator report is marked accordingly in `2-operator-reports-and-branch.md`.
