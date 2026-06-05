---
title: 529 — Audit of the operator's schema-stack work — code quality
role: designer
variant: Psyche
date: 2026-06-05
topics: [audit, code-quality, nota-next, schema-next, schema-rust-next, missing-layers, repetition, emitter, resolution]
description: |
  Psyche-requested audit of the operator's schema-stack implementation,
  hunting bad patterns, repetition, deep nesting, missing logic layers,
  pattern abuse. 30 findings (6 high / 14 medium / 10 low), file:line
  grounded. The hypothesis holds: the repetition and nesting DO speak of
  missing layers. The smells concentrate in two places — schema-next's
  resolution layer and schema-rust-next's emitter — which are exactly
  what the Asschema-removal migration will rewrite.
---

# 529 — Audit of the operator's schema-stack work

Four subagents swept the operator's recent work (nota-next structural-macro
machinery, schema-next `SchemaSource`/lowering/rkyv, schema-rust-next
emitter, plus a cross-cutting pass) for exactly what you named: bad
patterns, repetition, deep nesting, missing logic layers, pattern abuse.
Every finding cites file:line. **30 findings: 6 high, 14 medium, 10 low.**

## Verdict

**The stack is genuinely well-disciplined — this is good code with smells
concentrated in two hotspots, not bad code.** The auditors independently
noted strong foundations: the typed pattern language (`Pattern`/`AtomShape`
+ shadow-detection), the `RustModule`/`RustDeclaration` type model, clean
trait boundaries, data-bearing types well-placed. No `anyhow`/flag-soup/ZST
regressions. The problems are structural, not sloppy — and they cluster.

## Your hypothesis holds

You said repetition and nesting "speak of missing logic layers or abuse of
certain patterns." That is exactly what the audit found — the smells are
not aesthetic, they are **two recurring code shapes with no shared layer,
and four first-class concepts that should be types but aren't.** Of 30
findings, **11 are repetition and 8 are missing-layer** — and most of the
repetition is *because* of the missing layer.

## The findings, by theme

### 1. Two recurring shapes with no shared layer — highest leverage

- **The `from_block` map-pair parser, repeated 12+ times** (HIGH,
  cross-cutting). The same algorithm — *delimit with context → validate
  even count → chunk into pairs → map each pair* — is copy-pasted across
  schema-next's `SourceImports`, `SourceNamespace`, `SourceStructBody`,
  `SourceEnumBody`, … (`source.rs:232, 309, 345, 422, 496, 671, 712, 811,
  985, 1040, 1312`, and more, plus `declarative.rs`). One change to the
  pair rule means 12 edits. **Fix: one `Block::parse_pairs_map(delimiter,
  context, f)` method** — a single extraction kills the most duplication
  in the stack.
- **The variant-iteration codegen, repeated 3+ times** (HIGH,
  schema-rust-next `lib.rs:1567-1631, 1591-1691`). The emitter writes
  *for variant → match payload → format → write line* three near-identical
  ways (route emission, short-header, frame impl), 4+ levels deep. **Fix:
  one `emit_variant_arms(enum, renderer_closure)`** called three times.

### 2. Concepts that should be types but aren't (the missing layers)

- **`PlaneType`** (HIGH, schema-rust-next `lib.rs:1982-2014, 2262-2304`).
  The plane-type topology (`WriteInput`/`ReadInput`/`WriteOutput`/
  `ReadOutput`/`NexusWork`/…) is scattered as predicates across 5+
  functions, each re-listing the plane types. A new plane type means
  touching 5 places. **It wants a `PlaneType` enum that owns the topology**
  (`is_nexus()`, `is_sema_write()`, …) — the matrix lives in one type.
- **`SourceResolutionContext`** (HIGH, schema-next `source.rs:126-140,
  1139-1273`). The resolution work — *collect declared names, classify
  public vs private, hoist inlines, detect duplicates, order* — is split
  across `SourceTypeResolver` + `SourceLoweredNamespace` +
  `SourceDeclarationGroup` with the visibility interplay **implicit**. The
  core domain concept has no owning type. **(This is the one that gates the
  migration — see below.)**
- **`TypeExpression` AST** (LOW but architectural, schema-rust-next
  `lib.rs:~1120-1200`). `rust_type` builds type strings by concatenation;
  there is no typed representation, so the emitter can't ask "does this
  need a derive? is it a Newtype?" The 516 audit flagged the same
  string-concat codegen (panic arms). **It wants a `TypeExpression` enum
  with `Display`.**
- **`SourceFieldKind`** (MEDIUM, schema-next `source.rs:600-649`).
  `to_lowered_field` is a four-level nested match encoding a 2×3 matrix
  (Derived/Reference/Declaration × type-cased/value-cased name). **It wants
  an enum naming the six cases** so the matrix is exhaustive and visible
  (`skills/enum-contact-points.md`).

### 3. Copy-paste resolvers + duplicated dispatch

- **Four identical SEMA root resolvers + four identical SEMA type-name
  resolvers** (HIGH+MEDIUM, schema-rust-next `lib.rs:2924-3022`). Textbook
  copy-paste; collapse to `resolve_sema_root(...)` / `resolve_sema_type_name(...)`.
- **Duplicated dispatch: `StructuralVariantSet::dispatch` ≈
  `MacroRegistry::dispatch`** (HIGH, nota-next `macros.rs:469-490` vs
  `1010-1033`). The same contact point (position × variant set) written
  twice — the enum-contact-point isn't named once. Extract a shared
  `Dispatch` over `(position, variants, candidate)`.

### 4. The `RustWriter` god-struct (the biggest missing-layer smell)

`RustWriter` has **52+ `emit_*` methods in one struct** (MEDIUM,
schema-rust-next `lib.rs:848-2200+`), each a separate codegen phase, no
intermediate layer. It grew from a string accumulator into an orchestrator.
It wants decomposition into sub-codegens (`TraceCodegen`, a
`VariantCodegenHelper`, the `TypeExpression` AST above). This is where the
emitter's complexity has outrun its structure.

### 5. Deep-nesting hotspots (the worst)

- **Plane projection** `emit_split_nexus_work_projection` (schema-rust-next
  `lib.rs:2500-2584`) — projecting NexusWork→NexusAction across enum
  boundaries, nesting that obscures the intent; extract per-projection
  helpers returning match-arm strings.
- **The derive's closure-wrap** (nota-next `derive/src/lib.rs:784-795`) —
  the generated `if cond { return (|| -> Result {...})().map_err(...) }`
  wraps the constructor in an anonymous closure *only* to coerce a Result.
  Over-engineered; emit `cond { return #constructor.map_err(...) }` and fix
  the constructor's type at the source.
- **`to_lowered_field`** (covered in §2 as `SourceFieldKind`).

## What I think needs checking — my read

The single most important pattern: **the smells concentrate in exactly the
two places the Asschema-removal migration is about to rewrite.** That
changes the recommendation from "schedule a cleanup" to "fix these *as*
the migration, not after."

1. **The resolution scatter is load-bearing for the migration — check it
   first.** Records 520/524 say the Asschema-removal works by moving the
   resolution onto methods on the typed source nouns. The audit found that
   resolution is tangled across three types with implicit visibility
   interplay (HIGH, `SourceResolutionContext` missing). So the migration's
   first slice should be *untangling resolution into one named owner* —
   which is the audit's exact suggestion. Worth checking the operator's
   in-flight slice-2 work (the schema-source binary archive) isn't piling
   onto the tangle instead of resolving it.

2. **The emitter is where `RustModule::from_source` will land — and it's
   the densest smell.** `RustWriter` is a 52-method string-building struct
   with 4× copy-paste SEMA resolvers, scattered `PlaneType` predicates, and
   no `TypeExpression` AST. The migration adds a *new emission entry* to
   this struct. Bolting `from_source` onto a god-struct makes it worse; the
   from_source rewrite is the natural moment to introduce the missing
   layers (`PlaneType`, `TypeExpression`, `VariantCodegenHelper`). **This
   is the area I'd watch most.**

3. **Two one-method extractions are pure wins** regardless of the
   migration: `Block::parse_pairs_map` (kills ~12 duplications) and
   `emit_variant_arms` (kills the 3× codegen copies). Low risk, high
   leverage — worth doing soon.

4. **The nota-next derive smells are real but low-stakes** — the derive is
   small, tested, and works (the closure-wrap, scattered field-binding,
   format-literal repetition). A tidy-up pass, not a blocker.

The meta-recommendation: **fold the structural fixes into the
Asschema-removal migration**, because the migration touches precisely these
hotspots (resolution-onto-source-nouns and `from_source` emission). Doing
them together means the migration *introduces* the missing layers rather
than the migration making a god-struct bigger and a tangle deeper.

## Scope + provenance

Scope: the operator's recent schema-stack work in nota-next, schema-next,
schema-rust-next (the structural-macro mechanism + the schema pipeline).
Read-only; file:line grounded; nothing changed. Full per-finding evidence
+ suggested fixes are in the audit workflow output. The verdict is
honest-both-ways: strong foundations, smells concentrated in the emitter
and the resolution layer.
