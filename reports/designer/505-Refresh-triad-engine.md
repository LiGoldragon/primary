---
title: 505 — Refresh — the triad engine (Signal/Nexus/SEMA)
role: designer
variant: Refresh
date: 2026-06-04
topics: [triad-engine, signal, nexus, sema, sema-engine, engine-separation, nexus-recursion, nexus-work-action, inner-runtime-engine, schema-emitted-traits, runner, spirit-pilot, spirit-triad-naming]
description: |
  Agglomerated canonical surface for the triad-engine design — the
  Signal/Nexus/SEMA three-center runtime, the asymmetric NexusWork/NexusAction
  pair, the Continue recursion, the inner runtime engine (future direction),
  the strict-separation constraint (record 2560), and the schema-emission /
  honesty arc. Absorbs designer 458 (spirit-triad naming gate), 463 (operator
  trace audit + intent gaps + actor traits), 466 (triad-engine honesty
  situation), 477 (Nexus re-agglomeration three angles), 478 (inner Nexus
  recursive runtime engine). Reports 499 (persona-engine vision) and 501
  (strict-separation audit) hold the current cutover + audit state and are NOT
  duplicated here; this Refresh is the engine-design substance behind them.
---

# 505 — Refresh — the triad engine (Signal/Nexus/SEMA)

## What this report is

The canonical engine-design surface for the Signal/Nexus/SEMA triad. It carries
the design state, the live decisions, the asymmetry refinement, the recursion
model, the inner-engine future direction, the honesty arc, and the open
questions — densely. It is the agglomeration of five older designer reports
(458, 463, 466, 477, 478) whose un-superseded substance lives on here.

Two current reports stay canonical for what they own and are not repeated:
**499** (the psyche-facing persona-engine vision, cutover ordering, and the
corrections the psyche owes) and **501** (the strict-separation audit verdict:
pilot passes intra-daemon separation, fails the sema-engine boundary, old-stack
daemons need cutover, the runner makes the constraint structural). This Refresh
is the *engine design* those two reports stand on.

## The triad in one frame

Every daemon's runtime is three execution centers, each a schema type with the
same four-position shape, differing by **ownership not authored form**. The
vocabulary closes the loop: schema specifies, signal moves, sema holds.

- **Signal** — boundary / triage / wire. Admission, validation, the operation
  roots. The only string-tolerant edge: NOTA at the CLI, binary rkyv on the
  wire. The wire-frame codec is schema-emitted on the Signal types, so the
  daemon hand-rolls no frames.
- **Nexus** — decisions / heavy logic / mail keeper. The decision loop;
  Signal↔SEMA translation; effects; recursion. Owns the durable Store handle and
  the MailLedger.
- **SEMA** — durable single-writer state. The component `.sema` database (record
  2564: the file extension states it is a sema-redb database, hiding redb behind
  our own file type), reached **through sema-engine** (record 2563), never raw
  redb. The canonical state-of-record.

The strong separation guarantee is **already structural in the type system**:
schema-rust-next emits three engine traits whose plane-envelope signatures
(`signal::Signal` / `nexus::Nexus` / `sema::Sema`) make a cross-engine call a
*type error*. The spirit pilot ships a `compile_fail` doctest proving a Nexus
value cannot reach `Store::apply`. The only durable verbs are
`SemaEngine::apply` / `observe`; the only decision verb is `NexusEngine::decide`
(spelled `execute` in the landed pilot). The engines cannot leak into each
other. The constraint that governs this is record 2560 — see §"The
strict-separation constraint".

## The NexusWork / NexusAction asymmetry — the central refinement

The most load-bearing refinement across this whole arc (operator's correction,
record 1438; landed and verified in the pilot schema): **Nexus input and output
are NOT symmetric lists of the same operation categories.** If both sides list
Signal and SEMA operations the same-looking way, the interface loses meaning and
reads as nonsense.

The landed shape:

```text
NexusWork   [SignalArrived SemaWriteCompleted SemaReadCompleted EffectCompleted]
NexusAction [CommandSemaWrite CommandSemaRead ReplyToSignal CommandEffect Continue]
```

- `NexusWork` is the **fact stream** Nexus decides *from* — a Signal arrived, a
  SEMA write completed, a SEMA read completed, an effect completed. Facts and
  completions.
- `NexusAction` is the **command stream** Nexus emits *next* —
  `CommandSemaWrite` / `CommandSemaRead` delegate to SEMA, `CommandEffect` runs a
  runtime side-effect, `ReplyToSignal` is the **only wire exit**, and `Continue`
  is in-process recursion.

Both sides reference `signal::*` and `sema::*` types, but a `SignalArrived` fact
and a `ReplyToSignal` command are different concepts even though both touch
`signal::Output`. The asymmetry is encoded in the *variant names and roles*, not
just the type parameter. This was the failure mode the earlier symmetric framing
fell into; the correction makes the runner honest: commands go out, facts come
back in, Nexus decides, repeat until `ReplyToSignal` exits.

The runner loop (the generated scaffold, conceptually):

```rust
loop {
    let action = nexus.decide(current_work);   // NexusWork -> NexusAction
    match action {
        NexusAction::ReplyToSignal(output) => return output,            // EXIT to wire
        NexusAction::CommandSemaWrite(input) => {
            let done = sema.apply(input);
            current_work = NexusWork::SemaWriteCompleted(done);          // fact re-enters
        }
        NexusAction::CommandSemaRead(input) => {
            let done = sema.observe(input);
            current_work = NexusWork::SemaReadCompleted(done);
        }
        NexusAction::CommandEffect(effect) => {
            let done = effects.execute(effect);
            current_work = NexusWork::EffectCompleted(done);
        }
        NexusAction::Continue(work) => current_work = work,              // in-process recursion
    }
}
```

A `ContinuationBudget` bounds the loop so a misbehaving decider cannot recurse
forever. The runner is generic; the per-variant decision logic is the
component-specific algorithm. The `&mut Nexus` borrow on `execute` is the
single-flight guard — Rust prevents two mutable executions on the same Nexus at
once.

## Nexus recursion as universal computation destination

Record 1439 (Decision): when more work needs to happen, the next object is a
`Nexus` object rather than a final reply. `Continue(NexusWork)` is the landed,
typed form — Nexus feeds itself a freshly-built fact with no round trip, and
because the payload is *literally the fact stream*, the recursion is type-checked
by construction. This is the concrete realization of "recursive Nexus as
universal computation destination."

The architecture has **one recursion pattern at multiple scales**:

- **Per-request recursion** — `Continue` re-enters the same Nexus with a new fact
  (landed today).
- **Effect re-entry** — `CommandEffect` runs a typed side-effect (record 1437's
  effect language: Stash, Fanout, Summarize, Drop, Enqueue, Preempt, Cascade);
  the completion re-enters as `EffectCompleted`. The effect language EXISTS at
  Maximum magnitude (record 1437); the exact variant list is a lower-magnitude
  designer proposal pending evidence. Pilot Stash first.
- **Cross-component recursion** (designed, not built) — a Nexus from one
  component invokes another component's computation. Cross-component invocation
  goes through the target's **Signal contract** (the wire boundary), never its
  daemon-internal Nexus types. Daemons depend on each other's Signal contracts,
  not each other's Nexus internals — clean separation per the contract-repo
  split (record 1422). In-process recursion is a function call; cross-process is
  rkyv-over-socket with origin-route propagation.

Worked example (spirit's slim observe, the canonical case): `Observe(query)`
arrives → `CommandSemaRead` → SEMA returns a large result → Nexus decides it is
too large to inline → `CommandEffect(Stash)` stashes to the mail ledger keyed by
a handle → `ReplyToSignal(SlimAck{handle, count, marker})` exits. The client
later issues a `QueryByHandle` follow-up for the full payload. This is the slim-
Nexus-output principle (record 1389) and it is *also* the first place Nexus makes
a real decision — inline-vs-stash — rather than a generated projection.

## The inner runtime engine — future direction

Records 1464 (Clarification) and 1465 (Decision): Nexus has an **internal
interface with a second engine inside it that is recursive**. The OUTER
`NexusEngine` handles per-request domain decisions; the INNER runtime engine
handles **meta-decisions about the runtime itself** — and stays available to
take organizing decisions even under load. It is layered, separable, composable;
it does not replace the outer engine, it wraps the domain concern with a runtime
concern.

What the inner engine handles:

- **Backpressure** — when SEMA is overloaded, emit a typed too-busy reply rather
  than a TCP timeout, so the component stays available and clients retry with
  backoff. The typed reply uses the compact enum-payload shape (record 1466):
  `Busy(BusyReason)` carrying `DatabaseOverloaded` / `ResourceDisconnected` /
  `OtherBusyReason` directly, not a larger eagerly-wrapped report struct.
- **Actor prioritization under contention** — "Nexus actors should run more than
  SEMA actors because the database is busy"; trace/observability and
  health-check requests keep priority so the system can keep logging and report
  its own state while shedding lower-priority load.
- **Recursive meta-reasoning** — the runtime situation itself becomes input to a
  deeper decision (sustained backpressure → escalate to a different shedding
  policy). The inner engine's recursion IS record 1439's recursion at the meta
  level.

Placement per the contract-repo split (record 1422): the inner engine + its
`RuntimeSituation` / `RuntimeDecision` types are **daemon-internal** (not
client-facing) and live in the daemon repo; only the typed overload reply
(`Busy(BusyReason)`) crosses the wire and so belongs in `signal-<component>`.
Each component declares its own `ComponentRuntimeSituation` extension (spirit:
`SemaQueueDeep`; introspect: `TraceBufferNearFull`; orchestrate:
`LockConflictStorm`).

This is **direction, not mandate.** It frames where backpressure + scheduling +
overload-handling will LIVE so future slices have a typed home. Implementation
is gated: prove the outer NexusEngine + runner first (pilot Stash); a first
runtime situation lands when an overload actually surfaces; the inner engine
emerges as a typed trait once two components have analogous situations to handle.
`triad-runtime` ARCHITECTURE explicitly keeps backpressure and deeper
runtime-control machinery out of current scope — consistent with this.

Open inner-engine questions (worktree-resolvable when it lands): separate
`NexusRuntimeEngine` trait vs a `runtime_check` method on `NexusEngine` (lean:
separate trait for composability); when it fires — every decision vs
command-emission checkpoints vs overload-only (lean: command-emission
checkpoints); separate recursion budget from the outer continuation budget
(lean: separate, more conservative); whether it is the scheduler for actor
traits or orthogonal (lean: it schedules; actor traits are the structure,
runtime engine is the policy).

## The honesty arc — interface honest, behavior maturing

The triad-engine "honesty situation" (the psyche's question: are the traits
genuinely schema-driven, or is the schema surface thin while real behavior sits
in hand-written Rust?). The verdict arc:

- **Interface layer: structurally honest.** The three engine traits, plane
  envelopes, and routing match are schema-emitted, real, called by real runtime
  code with a Layer-2 runtime witness in `tests/runtime_triad.rs`. The pilot
  generates a large interface surface from a small schema. Hand-written
  `store.rs` persistence algorithm is *legitimate* per the terseness principle
  (record 1387: schema names the interface, generated Rust names the objects,
  hand-written code is mostly the real algorithm — match, decide, call the next
  typed interface, return).
- **Behavior layer: the slots exist, the substance is filling in.** Three things
  the 466 audit flagged that 499/501 now track as the live work: (1) the
  `Engine` composer was a hidden non-actor owner holding `Mutex<Nexus> +
  SignalActor` (the actor-systems anti-pattern) — the runner extraction
  dissolves this; (2) the observe path carried a full `Vec<Entry>` to the wire,
  violating the slim-Nexus principle — the slim-ack + `QueryByHandle` split
  fixes it and gives Nexus its first real decision; (3) Nexus had a structural
  decision slot but the "decision" was a generated projection — the recursion
  model + effect language fill it.

Three schema-emission targets close the remaining interface leakage (these are
the un-superseded design recommendations from the 466 honesty audit):

- **Trace plane emitted from schema.** Record 1365 (Correction Maximum):
  traceability is expressed as traits on schema-derived interfaces and, where
  possible, on the Signal/Nexus/SEMA actor traits themselves — instrumentation
  belongs to the interface/actor contract, not a local side vocabulary. The
  hand-written trace module retires; concrete actors consume the generated trait
  surface. The generic trace transport (length-prefixed rkyv socket, in-memory
  sink for tests, disabled sink for production) already lives in `triad-runtime`;
  the per-component `TraceEvent` is what schema emits.
- **Validate trait emitted from schema.** Field-constraint annotations on data
  types; schema-rust-next emits `validate()` methods instead of hand-written
  validation in component code — same emission shape as `From` and
  `with_origin_route`.
- **Signal-admission scaffolding emitted from schema.** The hand-invented
  origin-route base constant + identifier minting (the only hand-invented noun in
  the runtime triad) becomes a schema-emitted `OriginRouteAllocator` /
  `MessageIdentifierAllocator` + an admission associated function on
  `Signal<Input>`. (Open question, also raised in 501: whether admission policy
  becomes a `SignalEngine` trait method — record 2560 reads toward "all comms in
  the Signal engine" — or stays generic bookkeeping the runner owns.)

## The strict-separation constraint (record 2560)

Record 2560 (Constraint, VeryHigh) is the governing law of the engine:
[The triad engine separation is strict and absolute: the SEMA engine owns ALL
database and durable-state code, the Nexus engine owns ALL decision-making, and
the Signal engine owns ALL communication. A component daemon must contain NO
database boilerplate, NO decision-making, and NO communication code outside its
respective engine — every such concern lives in its engine and nowhere else]
(record 2560). Record 2559 (Principle, High) is the readability twin: daemon
code should not carry database, decision, or communication boilerplate beyond
process startup and shared runner wiring.

The lever that makes 2560 **structural rather than auditor-policed** is the
runner (ratified records 1574/1581, not yet built — the single most-repeated
missing noun). A non-overridable `TriadComponent::serve()` in triad-runtime owns
the accept loop + transport + composition once, generic over the engines;
schema-rust-next emits the per-component wiring and a one-line `main`. The
component author writes ONLY the three trait impls plus the data-bearing nouns.
With no hand-written host outside the engines, there is nowhere for a database /
decision / comms leak to live — the audit becomes vacuous by construction. The
weak half today is exactly the hand-written accept loop, composer, admission,
and `bin/main`: thin and non-leaking now, but the grey zone an auditor must
police until the runner deletes it.

The sema-engine boundary (record 2563, Correction High): "DB in the SEMA engine"
means **via sema-engine**, not raw redb contained in Store. The pilot's intra-
daemon separation is clean (redb appears only in `store.rs` + generated schema),
but Store still uses raw redb 2.x directly — that is a fake of the intended
architecture even as a pilot, and the live fix (tracked as bead `primary-w42y`,
the spirit-pilot sema-engine adoption) is to reach the database only through
sema-engine, which owns the redb interaction and the commit-sequence marker.

## Schema-emitted actor traits — the trait-on-interface shape

Record 1365 (Correction Maximum) ratified that trace lives as traits on
schema-derived interfaces and, where possible, on Signal/Nexus/SEMA **actor
traits**. The actor-trait shape (the "if possible" hedge means it pilots before
it is mandated):

```rust
pub trait SignalEngine {                    // typed compute (input -> output)
    fn triage(&self, input: signal::Signal<Input>) -> nexus::Nexus<NexusWork>;
    fn reply(&self, action: nexus::Nexus<NexusAction>) -> signal::Signal<Output>;
}

pub trait SignalActor: SignalEngine {       // runtime identity + (testing) trace
    fn identity(&self) -> ActorIdentity;
    #[cfg(feature = "testing-trace")]
    type Trace: SignalTrace;
    #[cfg(feature = "testing-trace")]
    fn trace(&self) -> &Self::Trace;
}
```

The same shape for `NexusActor: NexusEngine` + `NexusTrace` and `SemaActor:
SemaEngine` + `SemaTrace`. The split: the engine trait is the typed-compute
contract; the actor trait is the runtime-actor contract (compute + identity +
tracing). Pilot decisions (worktree-resolvable): super-trait vs peer traits;
associated `type Trace` vs generic vs `&dyn` dispatch; whether `ActorIdentity` /
`started_at` belong on the actor trait now or after a clear use surfaces (lean:
keep the first version minimal). The compile-time / runtime stratification holds
throughout: cargo features control which code *exists* in the binary; the single
NOTA argument controls what the existing binary *does* at runtime — a production
binary without `testing-trace` cannot be reconfigured into emitting traces by
any NOTA argument.

## Open questions

- **Spirit-triad policy-contract naming (from 458).** `core-signal-spirit`
  retires (legacy `core-` prefix; no other `core-signal-*` survives). The
  replacement is `meta-signal-spirit` — the workspace has since adopted
  meta-signal as the policy-contract naming (commit c1b7f17d "primary: adopt
  meta-signal policy contract naming"), superseding the older 458 recommendation
  to defer to `owner-signal-spirit`. The fleet-wide `owner-signal-*` →
  `meta-signal-*` rename is the broader pass; the 458 trade-off analysis is now
  moot and not carried forward.
- **Cross-component Nexus boundary** — when does `Continue`/invoke become a wire
  call vs in-process recursion? Likely via the target type binding: local type →
  in-process, cross-component type → wire through the Signal contract. Needs
  design once the in-process case is proven.
- **Subprocess return semantics** — a nested Nexus computation's `ReplyToSignal`
  is intercepted by the parent runner (not exiting to wire) and converted to a
  completion fact; uniform recursion shape. Lean confirmed, not yet built.
- **Effects vs SEMA delegations** — both re-enter Nexus; keep distinct (SEMA is
  durable state, effects are runtime side-effects) even though runner dispatch is
  structurally similar.
- **Runner concurrency** — stay sequential single-flight (the strongest
  guarantee, what the `&mut Nexus` borrow gives) or grow a generated actor
  mailbox? Genuine decision, not a mechanical extract.
- **Admission policy placement** — `SignalEngine` trait method vs generic runner
  bookkeeping (cross-references the Signal-admission emission target above).

## What lives where now

| Substance | Home |
|---|---|
| Triad three-center design, NexusWork/NexusAction, recursion, SEMA-via-sema-engine | spirit `ARCHITECTURE.md` (+ proposed strict-separation + recursion constraints below) |
| Generic runner, frame codec, argument classification, trace transport | triad-runtime `ARCHITECTURE.md` (+ proposed runner constraint) |
| Strict-separation law | record 2560 (Constraint) — propose ARCHITECTURE constraint mirror |
| Cutover ordering, persona-engine vision, decisions the psyche owes | report 499 (current) |
| Strict-separation audit verdict, old-stack daemon cutover, runner-makes-it-structural | report 501 (current) |
| Inner runtime engine future direction | this Refresh §"The inner runtime engine" + records 1464/1465/1466 |
