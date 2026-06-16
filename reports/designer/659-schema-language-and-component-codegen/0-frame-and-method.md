# 659 — Schema language & component code generation: meta-report frame

The psyche directed: *"bring it all together in a report — do a context maintenance on the
side to agglomerate into a new meta report with all the constraints and e2e goals."* This
meta-report agglomerates the full arc: how the nota/schema language represents generics and
traits/impls so the compiler **generates** the component code instead of hand-wiring it.

## What this agglomerates

The arc ran across reports `654`–`658` plus a Spirit intent-cleanup, all on primary main:

- `654` — generics/traits-as-data review: what generates today, the hand-wiring inventory,
  and the operator-`384`-shaped overclaim caught (generic-impl emission is real new codegen).
- `655` — explicit generic syntax, the pipe-delimiter family, and the Spirit cleanup tombstone.
- `656` — reaction-frame codegen design + the **verified expansion prototype**.
- `657` — concrete owned interface vs persisted generic (why expansion, not alias).
- `658` — the reactive component end-to-end operator spec (minimal schema → beautiful output).

## Method

A context-maintenance gather workflow ran three parallel passes (transcript in this session's
subagent dir): a comprehensive **constraint sweep** of the live Spirit store (verifying the
cleanup landed), a **design extraction** from `654`–`658`, and an **e2e-goal extraction**.
Their outputs are the three gathered sub-reports here; the synthesis weaves them into the
canonical whole. The Spirit cleanup itself (this arc) was executed and verified live: the
daemon v9/v10 store skew is fixed, `3742` reworded, `td1d`/`010y`/`nbvg` retired,
`1rci`/`f743` clarified, `7m84` superseded → `n1px`, `bpyu` recorded, `hh3z` reconciled.

## Directory map

- `0-frame-and-method.md` — this file.
- `1-constraints.md` — the full constraint catalog (the intent layer governing the design),
  grouped by theme, with the verified current delimiter-assignment state.
- `2-design.md` — the settled design: delimiter family, generics forms, the `{| |}` impl
  shape rule, code-is-data, the expansion codegen, the worked example, operator work, open
  frontiers.
- `3-e2e-goals.md` — the through-line: the original problem, the `zjmc` reaction-frame use
  case, the verified prototype, the hand-wiring inventory it eliminates, the e2e goals.
- `4-synthesis.md` — **the agglomeration**: constraints + design + goals woven into one
  reference, the settled-vs-open ledger, and what operators build.

## The one-paragraph version

A programming language is a set of structural macros kept as data (`7c71`); everything,
the macro most of all, is a serializable data object read by one tiny generic interpreter
(`4itr`). The schema is a NOTA dialect (`6grf`) whose six-delimiter set (`j9du`) now carries
every construct: `{}` struct, `[]` enum, `Name Type` newtype, **`(| … |)` generic
declaration** (`hh3z`), **`{| … |}` trait/impl** (`bpyu`), `[| … |]` strings — with a type's
kind explicit on the form, never guessed (`3742`). Components declare the universal Work/Action
reaction frame **once** and **bind** it per component (`zjmc`); the compiler **expands** the
binding into a concrete owned interface with constructors/`From`/wire-codecs for zero new
machinery (`656`, proven), build-time only (`9rjq`), so a two-line binding replaces ~4,200
lines of hand-spelled Rust. What stays hand-written is genuine behavior on generated nouns
(`5hjv`) — the deliberate boundary, not debt.
