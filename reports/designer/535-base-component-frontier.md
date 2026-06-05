---
title: 535 — Base-component frontier — what operator landed, what's next
role: designer
variant: Psyche
date: 2026-06-05
topics: [schema-rust-next, triad-runtime, spirit, signal, engine, runner, streaming, contract-daemon-split, token-lowering, frontier]
description: |
  Designer read of the schema/signal/engine frontier after the operator's
  high-movement push. What landed, what is already decided (execution, not
  open), and the three open candidates for the next slice — with the two
  that need the psyche's input: the runtime-emitter token migration and the
  contract/daemon split exemplar gap.
---

# 535 — Base-component frontier

## What landed (operator — the engine substrate moved)

This was a high-movement day on the base components. On main, verified
(`cargo test` + `clippy -D warnings`):

- **`schema-rust-next` 0.1.13** — token-based lowering for the **declaration
  surface** (aliases, newtypes, structs, fields, enums, variants, type refs)
  via `proc-macro2`/`quote`/`prettyplease`; recursive `LowerToRust<Target>`
  trait. Generated into checked `src/schema/*.rs` (source-visible, diffable).
- **`triad-runtime`** — the shared **Nexus runner core** (`Runner`,
  `NextStep`, `RunnerEngines`, `ContinuationLimit`, `ContinuationExhausted`);
  shared **role traits** (`NexusWork`, `NexusAction`, `SemaWriteInput`,
  `SemaReadInput`, effect roles); and a **multi-listener daemon shell**
  (`MultiListenerDaemon` — many listeners to one runtime owner, not racing
  threads).
- **`spirit`** — now the canonical schema-derived repo: split into
  `schema/{signal,nexus,sema}.schema` → generated `src/schema/{signal,nexus,
  sema}.rs`, running through `sema-engine`. Plane boundary made visible —
  the crate root no longer flattens generated plane nouns into `spirit::*`.
- **`cloud` + `domain-criome`** — `build.rs` now drives the shared
  daemon-runtime generation against ordinary + meta signal contract metadata.

Per operator 311: the old critical path (driver → spirit split → core
runner) is mostly closed. The new critical path is **daemon runner shell →
production parity/migration → separate signal/meta-signal repos → cutover
proof.**

## Already decided (High) — execution remaining, not psyche questions

- **`rpr5`** — the triad runner adapter is **generated glue only**; authors
  implement the three plane engines + effect handler + budget-exhausted
  reply. No hand-written fourth engine. (Settles operator 310 contentions
  #1/#2.)
- **`opvx`** — concurrency mode is a **runtime/deployment config** choice,
  never the public contract; the schema declares semantic constraints
  (ordering, idempotence, single-writer…) only when they are real.
- **`brgo`** — streaming is **full schema-derived**: teach `schema-next` an
  event/stream root with opens+belongs relations; teach `schema-rust-next`
  to emit the event frame reaching `signal-frame`'s existing-but-unused
  `StreamingFrameBody` + `ObservableSet` pub-sub; add a push action +
  subscriber registry to the runtime.
- **`rcn3`** — the multi-listener daemon already shipped (don't re-derive).

## The open frontier — three candidates for the next slice

### 1. The runtime emitter is still string-based (the live 532 debt)

`schema-rust-next/src/lib.rs` carries **~638 `format!`/`self.line(`** string
emissions against **~43 `quote!`/`TokenStream`** uses. The `317` token
migration corrected the **declaration** surface; the **runtime / per-plane
emission** surface is still hand-formatted strings — exactly the "ad hoc Rust
macro system" the psyche objected to (`4np2`, tokens-not-strings). The
declaration half is the gold standard; the runtime half is unconverted.

**Needs the psyche:** finish the token migration into the runtime surface to
honour `4np2` end-to-end, or is the runtime emission legitimately allowed to
stay string-based (it is build-time-checked into source files, and is more
in-flux than declarations)? The intent `4np2` may have been scoped to
declarations or to the whole emitter — this is the ambiguity.

### 2. The streaming / signal-frame slice (`brgo`, direction decided)

Named as the next emission slice (operator 320). Direction is set; this is a
**big build** spanning `schema-next` (the event/stream root), `schema-rust-
next` (emit the event frame), and the runtime (push action + subscriber
registry). It also **sizes the cutover effort** — `brgo` carries the open
sub-question of whether `signal-frame`'s streaming substrate
(`StreamingFrameBody`, `ObservableSet`) is deliberate scaffolding or
leftover. Mostly execution + one investigation; not a psyche fork.

### 3. The contract/daemon split exemplar gap (`wv63`) — foundational

**No correct schema-derived contract/daemon-split exemplar exists yet.**
`spirit` is the all-in-one pilot (Input+Output+Nexus+SEMA in one schema) and
its own ARCHITECTURE.md says the repo-triad split is deliberately *not*
represented — `wv63` says **do not copy it**. A correct contract is
**wire-only** (Input/Output + records + codec); Nexus and SEMA live only in
the daemon. `wv63`: a wire-only contract already emits no engine traits under
`schema-rust-next` today, so contract schemas can be corrected immediately —
but **"the missing macro piece for a client"** remains, and no exemplar
proves the split end to end. This is the shape **lojix** must follow
(`vudl`: `signal-lojix` peer contract + `meta-signal-lojix` owner policy).

**Needs the psyche:** which component proves the correct split **first**? Is
**lojix** the first real split exemplar (proving the split *while* porting
lojix — two unknowns at once), or should the split be proven on a smaller /
existing component first so lojix ports onto a proven shape?

## Designer recommendation

- **Streaming slice (#2) proceeds** as operator execution — decided, named.
- **Two need your input:** (1) the runtime-emitter token question — finish or
  accept strings; (3) the split-exemplar choice — lojix-first vs prove-small-
  first. My lean: prove the contract/daemon split on a **small existing
  wire-only contract first** (the contract schemas can be corrected *now* per
  `wv63`), so lojix ports onto a proven split instead of discovering it. And
  finish the runtime token migration as a **dedicated follow-on slice** —
  it is real debt and `4np2` reads as whole-emitter, but it should not
  pre-empt the streaming slice or the split exemplar.

Per psyche 2026-06-05.
