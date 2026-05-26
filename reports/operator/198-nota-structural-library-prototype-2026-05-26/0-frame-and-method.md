# 198 — NOTA structural library prototype: frame and method

Operator meta-report for the 2026-05-26 prompt that reframed NOTA as the
thin structural library underneath schema macros.

## Prompt Reading

The new design move is that NOTA itself is not the place where final type
legality is decided. NOTA gives methods on raw structure:

- delimiter kind;
- source span;
- object count at a block level;
- recursive child shape;
- atom text;
- symbol qualification by structural alphabet and case class.

Schema macros consume those structural methods to build specific positional
domain languages. Final decisions such as whether PascalCase is a type name,
unit variant, or string belong to the schema or macro context that consumes
the raw block, not to the raw NOTA scanner.

## Intent Captured

Captured before implementation:

- `783` — NOTA is the thin structural library for delimiter-level methods over
  blocks and atoms.
- `784` — schema macros are custom parsers over NOTA block structure.
- `785` — `.schema` root `Schema` struct is implied by file context.
- `786` — raw NOTA should not decide final PascalCase legality; raw atoms can
  promote to qualified symbols and later demote to strings by schema context.
- `791` — schema root should be represented through positional structs:
  imports/exports and input/output.
- `792` — clean new repos are an agreed direction to consider, while old-repo
  feature branches remain acceptable for faithful prototypes.
- `793` — core schema layer is the macro interface exposed from the bootstrap
  engine.
- `794` — this task should use subagents and synthesize their findings.

## Subagents

- `1-intent-and-design-synthesis.md` — latest intent and report synthesis.
- `2-code-shape-audit.md` — implementation shape audit across operator and
  designer prototype branches.
- `3-guidance-drift-audit.md` — guidance and repo-intent drift audit.

## Local Implementation Plan

The main thread will work in:

`/home/li/wt/github.com/LiGoldragon/schema/operator-schema-driven-nota-parser-prototype-2026-05-26`

Target implementation:

1. Extend the source-block layer into a true NOTA structural library surface:
   `SymbolClass`, `QualifiedSymbol`, and typed structural methods on atoms and
   blocks.
2. Add a small macro matcher that composes these predicates into reusable
   patterns.
3. Move the schema reader prototype one step away from hard-coded delimiter
   lowering by exercising the matcher in tests.
4. Keep the old Feature cleanup out of this slice except as report/audit
   scope; deleting the retracted Feature surface is a separate integration
   pass.

## Verification Target

- Focused tests for the new structural methods and macro matcher.
- Existing object-block tests.
- Existing schema-driven reader tests.
- Full `cargo test --workspace` on the operator schema branch.

