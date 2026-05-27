# 382 — pair-style namespace sweep (intent 894)

Sweep dispatched by prime designer to align workspace surface with
intent record 894 (Maximum, 2026-05-27): brace `{...}` in NOTA is
ALWAYS a key/value map; schema namespace at position 3 uses
pair-style not named-object form; namespace is conceptually a
dynamic enum, append-only Cap'n Proto style.

## What changed where

### `schema-next` — already swept on main by operator

Operator already landed commit `8c821cba` "make schema namespaces
key-value only" on `main` BEFORE this sweep arrived. That commit
already:

- Stripped parens from namespace entries in `schemas/spirit-min.schema`,
  `schemas/root.schema`, `schemas/core.schema`.
- Deleted `schemas/simple.schema` (was an old-form fixture).
- Removed `NamedTypeDefinition` from `MacroShape` enum and named-object
  branch from engine (`src/engine.rs` `NamespaceBlock`).
- Added `tests/lowering.rs::brace_namespace_rejects_parenthesized_named_objects`
  test that expects `ExpectedEvenMapEntries`.
- Added `flake.nix` checks `namespace-braces-are-key-value` to grep-fence
  the old form out of source.

This task became "fix what `8c821cba` didn't cover". The remainder
listed below was outside that commit's scope.

### `schema-next` worktree — `designer-pair-style-namespace-2026-05-27`

- `ARCHITECTURE.md`: lines 29-32 contradicted record 894 ("A named
  enum definition is `(Name (Variant ...))`"). Rewrote those lines
  to state pair-style + dynamic-enum + append-only framing,
  citing intent records 892 and 894.

Worktree: `/home/li/wt/github.com/LiGoldragon/schema-next/designer-pair-style-namespace-2026-05-27`.
Commit: `7b264003` "ARCHITECTURE: brace key/value rule, append-only
dynamic-enum framing (intent 894)" on branch
`designer-pair-style-namespace-2026-05-27` (pushed to origin).

### Primary workspace — `designer-assistant-pair-style-skills-intent-2026-05-27`

- `skills/nota-design.md` §"Map keys": extended the existing
  schema-namespace example with the dynamic-enum framing + APPEND-ONLY
  framing, citing intent records 891, 893, 894.
- `INTENT.md` §"schema-driven stack": added one paragraph before the
  "Schema-language design ..." reference, restating the brace
  key/value rule and dynamic-enum framing + APPEND-ONLY in Cap'n
  Proto style.

Commit: `19f48717` "skills + INTENT: brace key/value rule +
dynamic-enum namespace framing (intent 894)" on branch
`designer-assistant-pair-style-skills-intent-2026-05-27` (pushed to
origin). Bookmark `main` NOT moved; integration left to operator/
designer to consolidate with the other in-flight commits between
`votsqvkq` (origin/main) and my commit.

### `signal-frame`, `spirit-next` — already pair-style

Investigated and found NO drift in either:

- `signal-frame/schema/signal-frame.concept.schema` — already pair-style.
- `signal-frame/schema-rust/tests/fixtures/simple.schema` — already pair-style.
- `spirit-next/schema/spirit.schema` — already pair-style.

Signal-frame uses the OLD `schema` repo (NOT `schema-next`) — its
parser at `parser.rs:92-102` already reads pair-style namespace via
`read_map_name` + `parse_declaration_body`. The OLD engine has been
pair-style since well before record 894.

`cargo test` passes in `signal-frame` and `spirit-next` without
changes.

## Hard-remove vs soft-remove for engine

`8c821cba` chose **hard-remove**. The named-object branch is fully
deleted from `engine.rs` `NamespaceBlock`. `flake.nix` adds grep-
fence checks rejecting the old form. Test
`brace_namespace_rejects_parenthesized_named_objects` codifies the
rejection. No deprecation period; the engine errors with
`ExpectedEvenMapEntries`. This was the prompt's preferred outcome.

## Test pass status

- `schema-next` worktree (post-ARCHITECTURE.md edit): 10/10 tests pass.
- `signal-frame` main: 1/1 tests pass.
- `spirit-next` main: 5/5 tests pass.

## Skills + INTENT updated

- `/home/li/primary/skills/nota-design.md` — added schema-namespace
  example block + dynamic-enum framing tightening.
- `/home/li/primary/INTENT.md` — added one paragraph in the
  schema-driven stack section.
- `/home/li/wt/github.com/LiGoldragon/schema-next/designer-pair-style-namespace-2026-05-27/ARCHITECTURE.md`
  — rewrote misleading lines about `(Name (...))` form.

## Surprises

- **Sweep was 90% already done.** Operator commit `8c821cba`
  pre-empted most of the schema-next work — schemas, engine,
  tests, flake check. The sweep was reduced to one operator-territory
  doc that the operator's commit missed (`ARCHITECTURE.md`) plus
  the workspace skill / INTENT tightening.
- **Signal-frame uses the OLD `schema` repo, not `schema-next`.**
  Its dependency in `schema-rust/Cargo.toml` is
  `schema = { git = "...schema.git", branch = "main" }`. The old
  schema parser ALREADY uses pair-style namespace, so no migration
  was needed. The prompt's instruction to "update all `.schema` files
  in `schema/` and `schema-rust/tests/fixtures/`" was vacuously
  satisfied — they were already pair-style.
- **My commit sits behind unpushed work by other agents.** Between
  `origin/main` (`votsqvkq`) and my commit (`rolxtmyp`) there are two
  intermediate commits (`mpnwltn` rust-skills tighten, `xmpnuvl`
  operator/report-211) — the second is already pushed via
  `operator/report-211` bookmark, the first is not. I left `main`
  alone to avoid pushing the unpushed intermediate.

## Flagged for designer review

- **`INTENT.md` paragraph placement.** I inserted the new schema
  brace/key-value paragraph between the NEXT/MAIN/PREVIOUS authoring
  paragraph and the "Schema-language design ... lives in
  `repos/schema/INTENT.md`" pointer. Designer may want to move it
  earlier in the section or consolidate with that pointer.
- **`schema-next/ARCHITECTURE.md` is operator-owned.** I edited it
  in a designer feature branch per the prompt's authorisation. The
  branch is pushed; operator decides when/whether to integrate.
- **The integration sequence on primary main.** My commit, two
  rust-skill + operator-report commits, and several agent-private
  uncommitted changes all live ahead of `origin/main`. Someone needs
  to pick the order for landing them.
