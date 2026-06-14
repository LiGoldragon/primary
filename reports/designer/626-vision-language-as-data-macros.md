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
**where the macro set is kept.** Every language already *is* a set of structural
macros; conventional ones just **save that data poorly** — smeared across the
compiler/interpreter implementation, not expressed as clean, inspectable, typed
data. The data was always there; it was badly stored. This approach saves it well:
the macro set, down to the *shape vocabulary* — how a node decodes (report 103's
next brick) — is first-class typed data. So the openness goes one level deeper
than macro systems usually reach, because the thing normally smeared into the
compiler floor is now data you can read, write, and extend.

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

## Correction — a macro is NOT a reaction (category error, retracted)

An earlier version of this report floated "a macro *is* a reaction," mapping a
macro's pattern/template onto the runtime engine's `Work`/`Action` loop. The
psyche caught it as a category error, and it is: the **reaction frame is a runtime
engine abstraction** (I/O arrivals, effects, async orchestration across the live
daemons), while a **macro is compile/load-time** — a pure structural transform
from matched input to produced output, with no I/O, effects, or async. The
"arrive → produce" resemblance is too generic to be load-bearing — it is just "a
function," and stretching the reaction frame over it only hollows out everything
that makes the reaction frame *that* abstraction. The two share the **thesis**
(both are expressible as data); they are **not the same structure**. Language
design (this document) and the runtime engine are different layers; do not fuse
them.

What genuinely survives from that thread — and it lives entirely in the
language-design layer, no engine concept needed — is **kinds-as-macros**: every
output kind corresponds to a macro, so kinds are an open, data-defined set rather
than a closed enum, and the "what does this produce?" check survives as *which
macro matched*. That is what dissolves the template fork.

## The concrete ladder — bricks of the thesis

Each brick moves one construct from compiler-frozen to schema-data:

| Brick | Moves to data | Status |
|---|---|---|
| Macro *definitions* | already data (`builtin-macros.macro-library`, `DeclarativeSchemaMacro`) | done (verified, report 624) |
| Macro-table *nouns* (`MacroPattern` family) | schema-emitted from `core.schema` | operator slice, bead `primary-bojw` (spec 625) — in progress |
| Macro-node *shapes* (`#[shape]` vocabulary) | `StructuralNodeSpec` data + derive-as-freshness-witness | report 103 — next slice |
| The macro *struct* itself | just another schema-defined typed struct (kinds = macros) | language-design layer; no engine concept needed |

103 and 625 are different layers — 103 makes the decode *shapes* data, 625 makes
the macro-table *types* schema-emitted — and they compose; neither blocks the
other. The template-model divergence in `core.schema` stays unresolved inside the
operator slice (and is dissolved conceptually by `2zed` / kinds-as-macros, but
that is a deeper redesign than this slice).

## What is settled vs. still being designed

- **Settled** (recorded): everything is data; the language-as-data-macros thesis;
  self-host the macro-table types as the first step.
- **Being designed** (open): how the macro/template model is shaped now that
  kinds are macros; the macro-node-shapes-as-data slice (103); how far to push
  the uniform-substrate generalization (records, wire, macros, *and* daemon config
  are already one schema-NOTA-rkyv substrate — 103 §generalization). All in the
  language-design / data layer; the runtime engine is a separate concern.
- **The irreducible seed**, named: the NOTA parser + one frozen derive. Kept
  small on purpose; if it accretes, the trust root erodes into the thing it
  replaces.
