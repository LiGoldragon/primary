---
title: 529 — The operator schema-stack audit — what "smell", "hypothesis", and "missing layer" mean, grounded
role: designer
variant: Psyche
date: 2026-06-05
topics: [audit, code-quality, code-smell, missing-layer, nota-next, schema-next, schema-rust-next, emitter, resolution]
description: |
  Explains the audit in plain engineering terms — what a code SMELL is,
  what the HYPOTHESIS was (your own audit premise: repetition/nesting are
  symptoms of missing layers), and what a MISSING LOGIC LAYER is — each
  grounded in a real example from the operator's code. Then the 30 findings
  organized, and what I think needs checking. The smells concentrate in the
  two places the Asschema-removal migration will rewrite.
---

# 529 — The operator schema-stack audit, explained

This report does two things: (1) explains, in plain engineering terms,
what I meant by "smell", "your hypothesis", and "missing logic layer" —
each tied to a real line of the operator's code; and (2) presents the 30
findings and what to check. You designed the architecture; what follows
explains the *engineering vocabulary*, not the architecture.

## What a "code smell" is

A **code smell** is a surface symptom in *working* code that signals a
deeper structural problem. It is **not a bug** — the code compiles and
runs correctly. It is a sign that the *shape* is wrong: that something is
in the wrong place, or duplicated, or absent. The term is from refactoring
practice (Fowler/Beck): you can't always say "this is a bug," but you can
*smell* that the structure will cause trouble — it will be hard to change,
easy to break, painful to extend.

The value of a smell is that it is a **pointer, not a verdict.** "This code
is repeated 12 times" doesn't say the code is wrong; it says *look here —
there is probably a concept that should have been named once and wasn't.*

The four smells the audit hunted, each with a real example from the
operator's code:

- **Repetition** — the same shape of code written many times.
  *Real example:* the "parse a brace into validated pairs" routine is
  copy-pasted **12+ times** across schema-next's source types
  (`source.rs:232, 309, 345, 422, 496, 671, 712, …`).
- **Deep nesting** — logic buried several levels of `match`/`if` deep, so
  the reader can't see the decision being made.
  *Real example:* `SourceField::to_lowered_field` (`source.rs:600-649`) is
  a four-level nested match that is really a 2×3 decision table written the
  hard way.
- **Missing logic layer** — see the next section; it's the most important.
  *Real example:* the schema resolution work is smeared across three types
  (`SourceTypeResolver` + `SourceLoweredNamespace` + `SourceDeclarationGroup`)
  with no single type that *owns* "resolution."
- **Pattern abuse** — a pattern stretched past where it fits.
  *Real example:* `RustWriter` started as a string accumulator and grew into
  a **52-method god-struct** (`lib.rs:848-2200+`) — the "accumulate strings"
  pattern stretched to orchestrate the whole emitter.

## What your "hypothesis" was

You didn't ask me to "find ugly code." You asked me to look for "repetitive
code and deeply nested logic and stuff like that, **like things that speak
of missing logic layers or abuse of certain patterns**." That last clause
is a **hypothesis** — a claim about cause and effect:

> *The surface problems (repetition, deep nesting) are not the real
> problem. They are SYMPTOMS. The real problem underneath is usually a
> missing layer or a misused pattern.*

That is exactly right, and it is the professional way to read code smells.
The audit tested it and **it held**: of the 30 findings, 11 are repetition
and 8 are missing-layer — and most of the repetition is *caused by* the
missing layer. The duplication isn't sloppiness; it's the shadow cast by a
concept that was never given a name.

## What a "missing logic layer" is — the core insight

When you see the **same shape of code in 12 places**, or logic nested
**4 levels deep**, it almost always means there is a **concept** — a
function, a type, or a trait — that *should exist on its own* but doesn't.
Because the concept has no home, it gets **smeared across many places**
instead of **named once**. That absent home is the "missing layer."

Two concrete examples from the operator's code:

- The "parse a brace into validated pairs" routine appears 12 times. The
  *concept* "validated pair-parse of a block" exists 12 times but is
  **named zero times**. The missing layer is **one method**,
  `Block::parse_pairs_map(delimiter, context, f)`. The moment it exists,
  the 12 copies collapse into 12 one-line calls, and a change to the rule
  is one edit instead of twelve.
- The emitter checks "which plane-type is this — `WriteInput`? `ReadInput`?
  `NexusWork`?" with scattered predicates in **5+ different functions**,
  each re-listing the plane types. The *concept* "the set of plane types
  and their properties" exists, smeared. The missing layer is **one type**,
  a `PlaneType` enum that owns the list, so a new plane type is added in one
  place, not five.

This is why repetition and nesting "speak of missing layers": the
duplication and the deep `match` are the *visible footprint* of a concept
that wanted to be a method or a type and was instead inlined everywhere.

## The 30 findings, organized

6 high, 14 medium, 10 low. Honest verdict first: **the stack is genuinely
well-built — clean type models, the shadow-detection, no discipline
regressions. This is good code.** The smells **concentrate in two places:**
schema-next's resolution layer and schema-rust-next's emitter.

| Theme | The smell | Where | Sev | The missing layer |
|---|---|---|---|---|
| Recurring shape, no shared layer | "parse brace into pairs" copy-pasted 12+× | schema-next `source.rs` (many) | high | `Block::parse_pairs_map` |
| Recurring shape, no shared layer | variant-iteration codegen written 3+× | schema-rust-next `lib.rs:1567-1691` | high | `emit_variant_arms(enum, renderer)` |
| Concept not a type | plane-type predicates scattered across 5+ fns | schema-rust-next `lib.rs:1982-2304` | high | a `PlaneType` enum |
| Concept not a type | resolution smeared across 3 types | schema-next `source.rs:126-140, 1139-1273` | high | a `SourceResolutionContext` |
| Concept not a type | type strings built by concatenation | schema-rust-next `lib.rs:~1120` | low | a `TypeExpression` AST |
| Concept not a type | 2×3 field matrix as nested match | schema-next `source.rs:600-649` | med | a `SourceFieldKind` enum |
| Copy-paste | 4 identical SEMA resolvers ×2 | schema-rust-next `lib.rs:2924-3022` | high/med | `resolve_sema_root` / `resolve_sema_type_name` |
| Copy-paste | two near-identical dispatch methods | nota-next `macros.rs:469-490` vs `1010-1033` | high | one named dispatch over (position, variants, candidate) |
| God-struct | `RustWriter` has 52+ `emit_*` methods | schema-rust-next `lib.rs:848-2200+` | med | sub-codegens (Trace/Variant/Type) |
| Over-engineering | derive wraps constructor in a useless closure | nota-next `derive/src/lib.rs:784-795` | med | drop the closure; fix the type at source |

## What I think needs checking — my read

The pattern that matters: **the smells sit exactly where the
Asschema-removal migration is about to rewrite.** So this is "fix as you
migrate," not "schedule a cleanup later."

1. **The resolution scatter gates the migration.** Records 520/524 say the
   Asschema removal works by moving resolution onto methods on the typed
   source nouns. The audit found resolution has *no owning type* and an
   *implicit* visibility interplay. So the migration's first move should be
   to give resolution a home (`SourceResolutionContext`) — the audit's fix
   and the migration's first slice are the **same work**. Worth checking the
   operator's in-flight slice-2 (the schema-source binary archive) untangles
   this rather than piling on it.
2. **Watch the emitter most.** `RustModule::from_source` (the migration's
   emission entry) will land *inside* the 52-method `RustWriter` god-struct,
   which already has copy-paste SEMA resolvers, scattered `PlaneType`
   predicates, and string-concat type building. Adding to a god-struct makes
   it worse; the `from_source` rewrite is the natural moment to introduce
   the missing types (`PlaneType`, `TypeExpression`, a variant-codegen
   helper).
3. **Two one-method extractions are pure wins now:** `Block::parse_pairs_map`
   (kills ~12 duplications) and `emit_variant_arms` (kills the 3× codegen
   copies). Low risk, high leverage.
4. **The nota-next derive smells are low-stakes** — small, tested, works.
   A tidy-up, not a blocker.

Scope: the operator's recent schema-stack work (nota-next, schema-next,
schema-rust-next). Read-only; file:line grounded; nothing changed.
