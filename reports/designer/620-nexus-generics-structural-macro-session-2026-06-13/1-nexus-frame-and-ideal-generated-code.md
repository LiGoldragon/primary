# Nexus frame: the flaw and the ideal generated code

Consolidates reports 618/619 and the design evolution past them. Verified
against source this session.

## The flaw (verified)

The workspace-canonical Signal/Nexus/SEMA **reaction frame** —
`NexusWork [(SignalArrived) (SemaWriteCompleted) (SemaReadCompleted) (EffectCompleted)]`
and `NexusAction [(CommandSemaWrite) (CommandSemaRead) (ReplyToSignal) (CommandEffect) (Continue)]`
plus the structural wrapping and recursion (`Continue` → `Work`) — is
**hand-re-authored in all 12 components'** `schema/nexus.schema`
(confirmed: `spirit/schema/nexus.schema:66-67`; the 12 are cloud, terminal,
system, agent, spirit, router, orchestrate, mirror, mind, message, lojix,
harness). Only the per-component *payloads* legitimately differ: this
component's signal `Input`/`Output`, its `NexusEffectCommand` vocabulary
(spirit 18, router 2, agent 1), its sema write-command set, its
`NexusEffectResult` set.

The runtime side already proves the frame is genericizable: there are THREE
representations of the same five-way choice — `triad_runtime::NextStep<Reply,
SemaWrite, SemaRead, Effect, Work>` (generic, once, `runner.rs:26`), the
per-component concrete `NexusAction` (14×, emitted), and spirit's hand-written
`execute_to_reply` loop (`spirit/src/nexus.rs:974`). `schema-rust-next` even
emits a bridge `into_next_step` (`lib.rs:2017-2080`) converting the concrete
twin to the generic — *and* emits the correct generic instantiation
`pub type NexusRunnerNextStep = NextStep<…>` right next to it, then ignores it.

The driver fork is spirit-only and transitional: the shared driver
`triad_runtime::runner::drive<Engines>` exists and is used by the emitted path
and by `repository-ledger`; spirit forked `execute_to_reply` because it adopted
a "no-alias schema shape the runner no longer emits" (its own code comment,
`nexus.rs:1041-1043`). The frame TYPES are the systemic duplication; the driver
is one fork to re-absorb.

Governing intent: `n6fz` (this session) + the recorded `differ never by
authored shape` principle. C-CRATE-PREFIX (`Nexus*` prefix) is report 618 flaw 2.

## The ideal — three constraints the psyche set this session

1. **No re-authoring the universal frame per component** (`n6fz`). Declared
   once, bound per component.
2. **No type aliases** (`sarw`). `pub type Action = NextStep<…>` is rejected:
   transparent, carries no methods, orphan-rule-blocked. Not the mechanism.
3. **No ZSTs.** A `struct Binding;` marker as the frame's type carrier is
   rejected. The carrier must be a real data-bearing noun.

## The ideal generated code (engine-bound; superseded-by §2-of-file-2 for the surface)

Per-component generated nexus plane shrinks from ~2577 lines to the payload
enums + one binding. The frame lives once in `triad-runtime`. Report 619 shows
the engine-bound form:

- `triad-runtime`: `Plane` trait (8 associated types, each `: Wire`),
  `Work<P>` / `Action<P>` generic enums, `Reactor: Plane` (behavior: `decide` +
  async IO hooks), `Runner::drive<R: Reactor>`. Frame behavior (constructors,
  `route()`, the budgeted loop) lives here once.
- Per component (emitted): payload enums (`SemaWriteSet`, `EffectCommand`,
  `EffectOutcome`) + `impl Plane for Nexus { type Event = SignalInput; … }`
  bound onto the **engine** (the real data-bearing noun holding the store
  handle) — NOT a ZST.
- Per component (hand-written): `struct Nexus { store: … }` +
  `impl Reactor for Nexus { fn decide … }`.

Why no extra cost from dropping the ZST: `Work<P>`'s fields are associated-type
projections (`P::Event`), which Rust's `#[derive]` cannot bound anyway, so the
frame's Clone/Debug/Eq/rkyv/NOTA impls are hand-written once in triad-runtime
with the bound on the projection via the `Wire` supertrait — and once they are,
`P` can be the non-`Clone`/`Wire` engine with no problem.

## IMPORTANT evolution past 619 (read file 2 §"schema syntax")

The psyche then pushed on HOW the schema expresses this, and the design moved
**off the `Plane`-trait-with-associated-types shape toward direct generics +
type application**, because:

- The schema already expresses generic *application*: `(Vec Domain)` →
  `Vec<Domain>` (`signal.schema:101`). Generalizing that to
  `(reaction:Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)`
  applies the shared frame to the component's payloads **positionally**, in the
  Input/Output **root position** of the plane schema (no alias, no ZST).
- With `Work<Event, Write, Read, Effect>` generic over **direct type
  parameters** (not `P::projection`), the standard derives (Clone, rkyv, NOTA)
  **work natively** — the projection-bound residue that the `Plane`-trait shape
  introduced largely **dissolves**.

So the engine-bound `Plane` trait (619) is one viable shape, but the
schema-native, lower-residue shape is direct generic application. The trait may
still appear for the engine/driver seam, but the DATA types (`Work`/`Action`)
are best as direct-parameter generics. This is unresolved-pending-prototype
(task #408) — reconcile the two before committing 619 as final.

## Fix sequencing (from 618/619, updated)

1. Schema-stack: define the canonical frame once (a shared `reaction` schema —
   see file 2), give the schema language generic definition + application,
   delete the 14 hand-authored frame copies.
2. One-shot: drop the `Nexus*` prefix (folds into step 1 since the shared frame
   is authored unprefixed).
3. Re-absorb spirit's `execute_to_reply` into `triad_runtime::runner::drive`.

None of these belong to bead `primary-tqe3` (guardian retrieval) — verified the
`guardian_journal` "violations" were false positives; the guardian work doesn't
intersect the frame/naming/driver roots.
