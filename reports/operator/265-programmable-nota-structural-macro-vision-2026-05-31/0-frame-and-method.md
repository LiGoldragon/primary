# 0 - Frame and Method

Kind: meta-report frame. Topics: programmable-nota, structural-macros, asschema, schema-rust, spirit-runtime. Date: 2026-05-31. Lane: operator.

## Purpose

This meta-report presents the current architecture as the best vision of the system after the 2026-05-31 NOTA/Schema/Spirit work. It is not an implementation plan and does not edit code. It shows how the current code now supports Spirit record 1281:

NOTA is a programmable syntax library for structural-macro languages such as Schema. NOTA owns parsed structure and macro-node programmability. Consumers supply structural vocabulary and lowering.

## Current State Read

I read the live worktrees, not only the prompt state.

- `nota-next` is clean at parent commit `3f46c2e9` (public delimiter substrate, recursive macro patterns, multi-field enum variant derive support).
- `schema-next` is clean at parent commit `fe770d1d` (repinned to recursive NOTA macro substrate after `877c03f5` made declarative macro expansion structural). This is newer than the prompt's `57bab609` state and rewrites one older audit finding.
- `schema-rust-next` is clean at parent commit `33d7a678` (repinned to the recursive schema substrate).
- `spirit-next` is clean at parent commit `de7af0f7` (repinned to the same recursive schema substrate and Nix inputs).

## Method

The report is broken into three presentation parts plus synthesis:

1. `1-nota-layer-programmable-syntax.md` - parser, known-root body codec, derives, delimiter/block substrate, macro-node registry and pattern matching.
2. `2-schema-asschema-consumer-layer.md` - Schema as NOTA macro consumer, authored `.schema`, typed `Asschema`, checked-in `.asschema`, rkyv artifact and SEMA store path.
3. `3-spirit-runtime-layer.md` - Rust emission into nouns, CLI with NOTA enabled, daemon binary-only, Signal/Nexus/SEMA actor flow and `.sema` state.
4. `4-overview-and-gaps.md` - synthesis, rewritten older ideas, open questions and remaining gaps.

Each part uses short Mermaid graphs and compact snippets from current code. The graph labels are intentionally small; details live in the surrounding prose and source references.

## Source Surface

Primary sources read:

- `repos/nota-next/src/parser.rs`
- `repos/nota-next/src/codec.rs`
- `repos/nota-next/src/macros.rs`
- `repos/nota-next/derive/src/lib.rs`
- `repos/nota-next/tests/derive.rs`
- `repos/nota-next/tests/block_queries.rs`
- `repos/nota-next/tests/macro_nodes.rs`
- `repos/schema-next/src/asschema.rs`
- `repos/schema-next/src/declarative.rs`
- `repos/schema-next/src/macros.rs`
- `repos/schema-next/src/store.rs`
- `repos/schema-next/schemas/core.asschema`
- `repos/schema-next/tests/asschema_definition.rs`
- `repos/schema-rust-next/src/lib.rs`
- `repos/schema-rust-next/tests/emission.rs`
- `repos/spirit-next/build.rs`
- `repos/spirit-next/schema/lib.schema`
- `repos/spirit-next/schema/lib.asschema`
- `repos/spirit-next/src/schema/lib.rs`
- `repos/spirit-next/src/bin/spirit-next.rs`
- `repos/spirit-next/src/bin/spirit-next-daemon.rs`
- `repos/spirit-next/src/config.rs`
- `repos/spirit-next/src/engine.rs`
- `repos/spirit-next/src/nexus.rs`
- `repos/spirit-next/src/store.rs`
- `repos/spirit-next/tests/runtime_triad.rs`

## Rewritten Older Idea

The stale idea: the schema declarative macro engine still round-trips through text in the middle of lowering.

Current truth: `schema-next` commit `877c03f5` changed the core, and `fe770d1d` repinned it to the recursive NOTA macro substrate. `MacroBindings` now stores `Block` and `Vec<Block>` values, and `ExpandedTemplate::lower_to_output` lowers an `ObjectView::Expanded` directly. A compact text `source` string remains for trace/context (`context.remember_expanded_template`), but it is not the lowering substrate.

That means the architecture now presents Schema as a structural consumer of NOTA macro nodes, not as a text macro engine with structural decoration.
