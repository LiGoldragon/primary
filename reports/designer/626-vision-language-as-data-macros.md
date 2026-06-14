# Vision — a language is data: structural macros all the way down

The north-star synthesis of the design thread of 2026-06-13/14. It exists so
context can restart on the *why* without re-deriving it. The concrete bricks
(reports 103, 625, the operator slice) ladder up to this; read this first, then
them.

## The thesis

Per Spirit `7c71` (Principle, VeryHigh): [A programming language is, in essence,
a set of structural macros — constructors that take a typed, counted set of
objects, with Rust's struct, enum, fn, impl, and generics included and every
language likewise. Conventional languages freeze that macro set inside the
compiler, making it closed. This approach instead treats the macro set as data,
so the language becomes infinitely extensible — new constructs are added as data
rather than compiler changes — and far easier for an LLM to read, write, and
reason about, because the language's own constructs are uniform typed data in the
schema-NOTA-rkyv substrate.]

## Why it's the differentiator (and not just "we have macros")

Lisp has macros; Rust has macros. The novelty here is not *having* macros — it is
that **the macro set itself is data, not compiler-frozen.** In Lisp the reader
and special forms are frozen in the implementation; you extend syntax but not the
expander. Here even the *shape vocabulary* — how a node decodes — is data (report
103). So the openness goes one level deeper than macro systems usually reach.

Two things keep that from collapsing into "an untyped pile of macros":

- **Typed, so still safe.** Every extension is a *typed* value validated against
  its schema. Infinite extensibility does not cost the type system, because the
  extension mechanism is itself typed — the schema (spec) + structural-macro
  decode + rkyv (binary) *are* the type system. Open and checked at once.
- **Bootstrapped, so honest.** "Infinitely extensible" means *extensible down to
  a tiny frozen trust root* — the NOTA parser and one hand-written derive (report
  103's L1). Everything above the seed is data; the seed is a named, narrow,
  frozen exception, not a hand-wave. The rigor lives in keeping that seed small.

The LLM-legibility claim is load-bearing, not decorative: an agent reads and
writes `(SchemaMacro Bag TypeReference (Bag $Type) (Reference (Vector $Type)))`
far more reliably than a proc-macro's token-stream surgery. When the language's
own constructs are uniform data, the model operates at the *meta* level — it can
read and write the grammar, not only programs in it.

## The principle ladder (recorded intent)

The thesis rests on three supporting records, captured this thread:

- Spirit `2zed` (Principle, High): [everything is data, including a macro, a value
  of a specialized struct — pattern and template are ordinary typed fields, not
  special kinds]. This dissolved a false "open mirror vs closed typed kind"
  template fork: both candidate template representations were always just data.
- Spirit `t85k` (Principle, Low): the structural-macro-node grammar is itself
  schema-expressible. The macro-scoped seed of the thesis.
- Spirit `j9du` (Principle, Low): NOTA's own grammar is schema-describable; its
  delimiter set is a closed enum with reserved extension headroom.

And the committed first step:

- Spirit `wfdt` (Decision, Medium): [self-host the schema substrate's own
  definition types — generate the macro-table types from `core.schema` rather
  than hand-writing them — as the proving first step of absorbing Rust's type
  surface into schema].

## The live frontier — a macro *is* a reaction

The psyche's current move unifies two threads. A macro is a reaction: its
**pattern** is the `Work` that arrives (an input to expand), its **template** is
the `Action` produced (emit this output). Match-then-produce *is*
arrive-then-decide. So the macro substrate and the reaction frame (the `Work` /
`Action` of #407) are the **same generic structure** — a macro is a *constrained*
reaction whose DB-read / DB-write / effect legs are unused, marked `Absent` (the
#408 marker, here earning its purpose). And since "every output kind corresponds
to a macro," kinds are an open, data-defined set, not a closed enum — the
"what does this produce?" check survives as *which macro matched*.

**Governing open question (psyche's call):** is the reaction frame THE universal
structure, with macros, components, and config all applications of it? If yes,
`SchemaMacro` should not be a bespoke struct — it should be the reaction frame
applied. This is downstream of the current operator slice and does not block it.

## The concrete ladder — bricks of the thesis

Each brick moves one construct from compiler-frozen to schema-data:

| Brick | Moves to data | Status |
|---|---|---|
| Macro *definitions* | already data (`builtin-macros.macro-library`, `DeclarativeSchemaMacro`) | done (verified, report 624) |
| Macro-table *nouns* (`MacroPattern` family) | schema-emitted from `core.schema` | operator slice, bead `primary-bojw` (spec 625) — in progress |
| Macro-node *shapes* (`#[shape]` vocabulary) | `StructuralNodeSpec` data + derive-as-freshness-witness | report 103 — next slice |
| The macro *struct* itself | the reaction frame applied (`Work`/`Action`) | live frontier, gated on the question above |

103 and 625 are different layers — 103 makes the decode *shapes* data, 625 makes
the macro-table *types* schema-emitted — and they compose; neither blocks the
other. The template-model divergence in `core.schema` stays unresolved inside the
operator slice (and is dissolved conceptually by `2zed` / kinds-as-macros, but
that is a deeper redesign than this slice).

## What is settled vs. still being designed

- **Settled** (recorded): everything is data; the language-as-data-macros thesis;
  self-host the macro-table types as the first step.
- **Being designed** (open): whether the reaction frame is the universal struct
  (macro-as-reaction); the macro-node-shapes-as-data slice (103); how far to push
  the uniform-substrate generalization (records, wire, macros, *and* daemon config
  are already one schema-NOTA-rkyv substrate — 103 §generalization).
- **The irreducible seed**, named: the NOTA parser + one frozen derive. Kept
  small on purpose; if it accretes, the trust root erodes into the thing it
  replaces.
