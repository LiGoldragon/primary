---
title: 317 — Operator psyche report — token lowering and Spirit readiness
role: operator
variant: Psyche
date: 2026-06-05
topics: [schema-rust-next, spirit, quote, proc-macro2, source-visible-generation, schema-pipeline, production-readiness]
description: |
  Operator-side report after implementing the first token-based Rust lowering
  slice and updating Spirit. Explains why proc macros can generate Rust but are
  not the current artifact boundary, what changed in schema-rust-next and
  spirit, what remains difficult, and what questions still matter.
---

# 317 — Token Lowering And Spirit Readiness

## Short Verdict

The psyche's objection was correct: the old `RustWriter` path was too much of
an ad hoc Rust macro system. It used a typed `RustModule` middle layer, but the
bottom half still treated Rust as formatted strings. That is now corrected for
the core declaration surface: aliases, tuple newtypes, structs, fields, enums,
variants, and type references are produced as Rust token streams through
`proc_macro2`/`quote` and then pretty-printed into the same source-visible
generated files.

The important boundary stays intact: a real compiler proc macro can absolutely
generate Rust code, but the current best artifact boundary is not hidden macro
expansion. The current best boundary is build-time token generation into
checked `src/schema/*.rs`, because Spirit and future agents need to inspect,
diff, freshness-check, and compile those generated interfaces directly.

## What Changed

`schema-rust-next` main now has commit `2437413f`:

- Version moved from `0.1.12` to `0.1.13`.
- Added `proc-macro2`, `quote`, `syn`, and `prettyplease`.
- Added `LowerToRust<Target>` as the recursive lowering trait.
- Implemented schema-subobject lowering for imports, declarations, type
  declarations, aliases, newtypes, structs, fields, enums, variants, and
  support metadata.
- Added context-carrying token wrapper nouns:
  `RustDeclarationTokens`, `RustStructTokens`, `RustEnumTokens`,
  `RustFieldTokens`, `RustTypeReferenceTokens`, and siblings.
- Changed emitted type declarations and root enums to render through tokens
  and `prettyplease`, not direct `format!` strings.
- Added a regression proving individual schema subobjects lower themselves
  into Rust model nouns.
- Manifested the token/codegen and context-wrapper discipline in
  `schema-rust-next/INTENT.md` and `ARCHITECTURE.md`.

`spirit` main now has commit `4154f25b`:

- Locked to `schema-next` `5311f9ad` and `schema-rust-next` `2437413f`.
- Made namespace enum payload variants explicit in
  `schema/{signal,nexus,sema}.schema`, e.g. `(Record Record)` and
  `(CommandSemaWrite CommandSemaWrite)`.
- Kept root enum headers as bare exported object lists.
- Updated tests and docs to reflect strict namespace enum signatures,
  typed `SchemaSource` artifacts, semantic `Schema`, and no checked
  `.asschema` artifact.

## Why This Fulfills The Intent

The pipeline is now closer to the intended shape:

`authored .schema` deserializes into typed schema data, that data lowers through
schema nouns into Rust model nouns, and Rust syntax is built from those nouns as
tokens. Strings are now only the final file artifact boundary for the shipped
slice, not the internal language of the core declaration generator.

The `ToTokens` context issue matters. Plain `quote::ToTokens` has no context
argument, while this generator still has real global context: NOTA feature
gates, private-type visibility, selected runtime target. The correct current
pattern is therefore a context-carrying wrapper around each noun. Intrinsic
shape belongs on the noun; generation-wide switches stay contextual.

## Contentions

The next implementation contention is how aggressively to move the remaining
runtime-support emission out of `RustWriter`. The declaration slice is clean;
the runtime slice is where cross-object concepts concentrate: plane routes,
trace names, runner projection, SEMA half detection, and engine trait support.
That part should not become many isolated `ToTokens` impls that secretly share
string predicates. It wants named cross-object nouns first, especially a
`PlaneType` or equivalent model.

The second contention is actual proc macro versus build-time token generation.
A proc macro can generate Rust code. The reason not to make that the default
now is artifact visibility: inline macro expansion hides the generated
interface unless the reader runs expansion tools. Build-time token generation
keeps `quote` while preserving checked generated files. That matches the
workspace's introspection priority.

## Remaining Difficult Parts

`RustWriter` still exists and still owns most runtime/support output. The
highest-value next slices are:

- Route and frame support as token nouns.
- Plane type detection as a real type instead of repeated name predicates.
- Nexus runner projection and adapter emission as token nouns.
- Trace/support/lifecycle trait emission as named token surfaces.
- Eventually, remove the old string writer once every emitted section has an
owning noun.

Spirit itself is in a strong pilot state: SEMA durability is real through
`sema-engine` and `.sema` files, Nexus runner flow is exercised, binary daemon
configuration is enforced, and all-feature process-boundary tests prove the
real CLI/daemon path. The remaining production gap is not "does it run"; it is
finishing the generated runner and generation cleanup so ports do not inherit
remaining hand-written runtime boilerplate.

## Verification

`schema-rust-next`:

- `cargo check`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`

`spirit`:

- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo test --no-run`
- `cargo test`
- `cargo test --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`

Ignored Nix integration tests were not run in this pass. They are the slow
`nix build` surface; the all-feature `process_boundary` suite did run and
passed.
