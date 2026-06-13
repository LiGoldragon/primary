---
title: 612 — Refresh — schema/NOTA/triad-runtime stack: grammar, daemon-emit, EngineActor (landed)
role: designer
variant: Refresh
date: 2026-06-13
topics: [schema, schema-next, schema-rust-next, nota, triad-runtime, daemon, emission, engine-actor, kameo, grammar, plane-type, component-triad, meta-signal, two-client]
description: |
  Agglomerated current-state surface for the schema-derived component-triad
  runtime stack — the work that emits each daemon's runtime, signal/meta-signal
  contracts, and actor shell from its .schema. Merges designer 526, 527, 536,
  537, 541, 543, 550-v2, 553/*, 570, 571, 573, 575, 599. Most of this thread's
  design substance has MATURED into skills/component-triad.md (the
  WireContract/SignalRuntime boundary, the three-plane split, the triad_main!
  runner, kameo EngineActor); this Refresh names those permanent landings and
  carries the residual working-artifact state (the schema grammar that landed on
  main, the daemon-config bootstrap model, the two-client pattern).
---

# 612 — Refresh — schema/triad-runtime stack: grammar, daemon-emit, EngineActor

Landing witness for the schema-derived triad runtime stack. The 13 source reports
it merges are deleted in the same commit; git history holds them. Most of this
thread's design **already lives permanently in `skills/component-triad.md`** — this
Refresh names those landings and keeps only the residual working-artifact state.

## 1. The permanent home — what landed in `skills/component-triad.md`

The component triad is `<component>` (daemon/runtime + bundled thin CLI),
`signal-<component>` (working signal), `meta-signal-<component>` (meta policy
signal). The following design matured out of these reports and into the skill — read
it there, not here:

- **The three-plane emission split** (designer 526, 527): `WireContract` (the public
  `signal-<component>` schema — wire vocabulary + codecs ONLY, zero engines, the
  single source of wire types for every linker including the daemon itself);
  `SignalRuntime` (the daemon-local `signal.schema` — the `SignalEngine` trait over
  the contract's imported types, emits engine/runtime only); `NexusRuntime`,
  `SemaRuntime` for the other planes. `RustEmissionTarget.runtime_planes()` selects
  what each schema emits. This is `skills/component-triad.md` §"the wire boundary".
- **`triad_main!` — the emitted daemon module** (designer 543, design 542): the
  generated daemon `fn main()` + runner loop, proven GREEN end-to-end with option-B
  streaming against the emitted daemon. Permanent in `skills/component-triad.md`.
- **Runtime triad engines are kameo actors — the `EngineActor`** (designer 575,
  records `zk6y`/`96mi`/`ilxh`): the emitter generates a per-daemon `EngineActor`
  that *owns* the engine; the runtime drives every request through the actor's
  mailbox (`engine.ask(WorkingInput{..})`), which serializes access as a lock did but
  without holding a guard across `.await`, and the handler gets `&mut self` for free.
  This replaced the `Mutex<Nexus>` / `Mutex<HandoverState>` interior-mutability
  workaround across the fleet (`orchestrate`, `message`, `spirit`, terminal, …). The
  rule is `skills/component-triad.md` §"Runtime triad engines are kameo actors"; the
  actor-native design frame was designer 553. The actor discipline itself is
  `skills/actor-systems.md`.

## 2. The schema grammar — landed on main

Four schema-grammar improvements landed on `schema-next` main + `schema-rust-next`
(designer 570 review, 571 handover, 573 progress; records `52ro`/`yp29`/`qz6j`/`lm84`):

- **`52ro`** — compact enum-variant forms (`(X)` self-tag).
- **`yp29`** — `Bytes` reserved scalar primitive.
- **`qz6j`** — **aliases dropped entirely** (psyche: "we don't use alias — they're
  useless and offer no correctness"). `TypeDeclaration::Alias` + `AliasDeclaration`
  removed; *every* bare `Name Type` (scalar, declared-type, collection) lowers to a
  distinct `NewtypeDeclaration`. `Recipient String` -> newtype; `State Statement` ->
  distinct `State(Statement)`, no longer interchangeable. Resolved harder than the
  handover scoped.
- **`lm84`** — hash-identifier type.

schema-next grammar side is complete and on main (107 tests). The schema-rust-next
emitter integration (the `From`-impl emission subtlety) is the residual pass.

## 3. PlaneType — promoting the implicit plane axis to a noun

The design that unblocked the runtime-half token migration (designer 537): promote
the implicit plane axis (three bools in `RuntimePlaneSet` + the `*Runtime` target
variants + smeared inline conditionals) into two first-class nouns — **`Plane`** (the
node: per-plane naming) and **`PlaneProjection`** (the edge: cross-plane transforms)
— that the runtime construct nouns consult while owning their own tokens. Grounded in
a survey of all ~26 runtime emit methods. The engine codegen is a decided
token-native migration (declaration half done, runtime half on this design); the
ground-truth correction is designer 536 (the runtime emitter was wrongly framed as
open debt; spirit's schema-plane split exemplar HAD landed, wv63 retired by y88n).

## 4. The daemon-configuration bootstrap — the ratified model

The ratified model (designer 550-v2, psyche ratified all three sub-decisions; records
`e6ri`/`ur16`):

- **Daemons cannot understand NOTA.** A daemon's single startup argument is a
  pre-generated signal-encoded (rkyv) `Configure` message.
- **Bootstrap depends on NO manager** — persona-FD-handoff was rejected (a manager
  dependency is circular and fragile).
- **A virgin daemon** (empty store) applies the `Configure` as its first config; a
  daemon with a populated store self-resumes from persisted SEMA state. The same
  `Configure` type is accepted live over the owner-only meta socket.

The `meta-signal-spirit` owner-only Configuration contract (designer 541, psyche
`oszy`) was the first instance: a wire-only `(Configure ArchiveTarget)` routed over
an owner-only meta socket, daemon migrated to `MultiListenerDaemon`.

## 5. The two-client pattern

Ratified (`8bwo`, designer 599): every component exposes its two contracts as two
thin CLI clients — `<component>` (working signal) and `meta-<component>` (meta policy
signal) — as one extracted pattern. **The library is the engine and holds 100% of the
logic** (connect, encode NOTA->rkyv, send frame, receive, decode rkyv->NOTA, render,
errors, subscription streams), generic over `<Signal, Reply>`, written once. **The
generation is the per-component binding** — each component's two `fn main()`s emitted
by schema-rust-next, supplying only the Signal type and three other things. Spirit's
`spirit`/`meta-spirit` is the first instance (see designer 611 §6).

## 6. Residual open items

- The schema-rust-next emitter integration against the landed schema-next grammar
  (the `From`-impl emission subtlety) — the one remaining grammar-side pass.
- The runtime-half token-native migration driven by the PlaneType design (§3) —
  declaration half done, runtime half remaining.
- The two-CLI emission for the rest of the fleet (spirit is done; the pattern is the
  template).
