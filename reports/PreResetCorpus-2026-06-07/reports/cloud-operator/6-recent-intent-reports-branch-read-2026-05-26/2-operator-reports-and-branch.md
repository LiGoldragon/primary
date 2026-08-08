# Operator reports and branch state

## Scope

This fills the operator slice of the pi-operator meta-report. The delegated scout returned only a file locator, so the orchestrator read the operator reports and branch state directly.

Read:

- `reports/operator/198-nota-structural-library-prototype-2026-05-26/0-frame-and-method.md`
- `reports/operator/198-nota-structural-library-prototype-2026-05-26/1-intent-and-design-synthesis.md`
- `reports/operator/198-nota-structural-library-prototype-2026-05-26/2-code-shape-audit.md`
- `reports/operator/198-nota-structural-library-prototype-2026-05-26/3-guidance-drift-audit.md`
- `reports/operator/198-nota-structural-library-prototype-2026-05-26/4-overview.md`
- `reports/operator/197-nota-core-design-refresh-and-gap-audit-2026-05-26.md`
- `reports/operator/196-schema-object-block-pass-prototype-2026-05-26.md`
- `reports/operator/195-schema-driven-nota-reader-prototype-2026-05-26.md`

Inspected branch/workspace state with headless `jj` commands only.

## Latest operator direction

Operator report `198` is the current implementation-facing center. It builds on reports `195` through `197` and lands the first concrete NOTA structural-library slice on the schema operator worktree.

The important implementation line is:

```text
source NOTA
  -> delimiter/source-span block pass
  -> reusable macro-pattern matcher over block objects
  -> schema-specific namespace matcher
  -> existing object-value lowering
  -> ordered assembled declarations
  -> generated Rust reader
```

What landed on the operator schema worktree:

- `src/macro_pattern.rs` adds `SchemaMacroPattern`, a reusable matcher over raw block objects.
- `src/object_block.rs` now carries `QualifiedSymbol`, `SymbolClass`, and `qualifies_as_*` methods instead of pretending raw NOTA decides final semantic type.
- `src/nota_reader.rs` wires a narrow `NamespaceBlockMatcher` before existing object-value lowering, proving the schema reader consumes structural block facts before assigning schema meaning.

The operator tests reported green include focused macro-pattern/object-block/schema-reader tests, full `cargo test`, full `cargo test --workspace`, `cargo clippy --workspace --all-targets -- -D warnings`, and explicit named Nix check builds.

## Earlier operator findings that still matter

Report `195` proved a useful but narrow pipeline: schema namespace text can lower to ordered assembled declarations, emit explicit Rust `NotaDecode` implementations, compare generated code against a compiled fixture, and decode real positional NOTA. Designer later corrected that this does not yet make NOTA itself schema-derived.

Report `196` added the missing source-block pass with byte/line/column spans, delimiter kinds, root-object counts, recursive shape predicates, and `[|...|]` block-string opacity. That pass was the bridge from value-tree-only parsing toward macro shape recognition.

Report `197` is the broad gap audit. Its highest-risk findings remain:

- repo-local `schema/INTENT.md` and `schema/ARCHITECTURE.md` still teach six-position schema and authored `Features` in places;
- retracted Feature variants/tests still exist and can keep old behavior green;
- three schema shapes coexist without a clean migration boundary;
- production `nota-codec` is not yet schema-derived;
- square-bracket string/vector interpretation still needs canonical tests;
- `Asschema` / `AssembledSchema` is not yet a stable canonical artifact.

## Current branch state

Primary workspace:

- `main` currently points at `wmlvvqvy` / `3999552f`, description `skills/jj.md: at-a-glance cheat sheet at top + note structural fix landed in source`.
- The current working-copy parent is `tzlwqsyk` / `c39d9a98`, description `report operator/198: verify nota structural prototype`, one commit ahead of `main`.
- The current pi-operator meta-report files are in the working-copy commit above that parent.

Operator schema worktree:

- Path: `/home/li/wt/github.com/LiGoldragon/schema/operator-schema-driven-nota-parser-prototype-2026-05-26`
- Working copy is clean.
- The branch/bookmark `operator-schema-driven-nota-parser-prototype-2026-05-26` points at `skqzqpok` / `9dcc0244`, description `schema: match macro shapes through structural nota blocks`.
- The current `@` is an empty descendant `pqvlstmr` / `be3df64b`.
- The operator branch contains the reader proof, source block pass, macro pattern layer, object pass, fixture, and tests. Diff from its `operator-full-schema-spirit-2026-05-26` base is about twelve files and roughly 2.5K insertions.

Operator nota-codec worktree:

- Path: `/home/li/wt/github.com/LiGoldragon/nota-codec/operator-nota-structural-shape-2026-05-26`
- Working copy is clean.
- Current `@` is an empty change `rlwsvlru` / `3da0b23d` over `nota-codec` main `rsltovoy` / `f761421c` (`nota-codec: reject quoted string delimiters`).
- The operator lock claims this worktree, but the inspected branch has no substantive current diff.

Canonical `/git/github.com/LiGoldragon/schema` state observed during the pass belongs to the designer prototype branch, not the operator branch: it is dirty with prototype block-parser files under `prototype/` and is on bookmarks `designer-schema-derived-nota-2026-05-26` plus `designer-schema-schema-prototype-2026-05-26`.

## Coordination implications for pi-operator

- Operator is actively claiming `/home/li/wt/github.com/LiGoldragon/schema/operator-schema-driven-nota-parser-prototype-2026-05-26`, `/home/li/wt/github.com/LiGoldragon/nota-codec/operator-nota-structural-shape-2026-05-26`, and `/home/li/primary/reports/operator`. Pi-operator should not edit those surfaces.
- The production-adjacent implementation base is the operator schema worktree, not the broader designer prototype crate.
- The next implementation direction is not more emitter output first; it is to converge raw block/value representation, stabilize `Asschema`, and delete/fence old Feature acceptance.
- Any report or branch that uses authored `EffectTable`, `FanOutTargets`, `StorageDescriptor`, or a `Features` section as user schema surface is stale relative to current intent.
