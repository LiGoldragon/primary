# The ideal nexus-plane generated code

What `schema-rust-next` *should* emit for a component's Nexus plane, designed
from first principles (a four-architect judge-panel, grounded in the live
code), holding to one bar that cannot be wished away — **it must compile** —
and one the psyche set — **no type aliases**. This is the target shape; report
618 is the diagnosis of today's shape, and this is where it should land.

Framing that unlocked the design: schema is *our* specification language, so
"can schema express this?" is never the constraint — we design the authoring
surface to say exactly what we mean, and the emitter lowers it to whatever Rust
best realizes it. The only hard constraint is that the generated Rust compiles.

## The shape in one sentence

One reaction frame — `Work<P>` / `Action<P>` and the budgeted `drive` loop —
declared **once** in `triad-runtime`, instantiated per component by **binding
an eight-slot `Plane` trait**, never by re-declaring the frame and never by a
type alias.

## Shared once (triad-runtime)

The frame, its behavior, and the loop live in exactly one place. This deletes,
from the current stack: `NextStep<5 params>`, `RunnerEngines`, the
per-component `NexusWork`/`NexusAction` enums + their wrapper newtypes + route
enums, the `into_next_step` shim, and the `pub type Work`/`pub type Action`
aliases at `spirit/src/schema/nexus.rs:2464-2466`.

```rust
// triad-runtime/src/reaction.rs — the universal reaction frame, ONCE.

/// Wire bundle: rkyv always, NOTA under the `nota-text` feature.
#[cfg(feature = "nota-text")]
pub trait Wire: rkyv::Archive + Clone + Debug + PartialEq + Eq + Send + 'static
    + nota_next::NotaEncode + nota_next::NotaDecode {}
// (+ a blanket impl<T> Wire for T where T: ...; and a non-nota cfg form)

/// A component's payload alphabet — the ONLY thing a component supplies.
pub trait Plane: Sized + Send + 'static {
    type Reply: Wire;            // ReplyToSignal   (signal Output)
    type Event: Wire;           // SignalArrived   (signal Input)
    type SemaWrite: Wire;       // CommandSemaWrite (Infallible if no sema-write plane)
    type SemaWriteResult: Wire; // SemaWriteCompleted
    type SemaRead: Wire;        // CommandSemaRead
    type SemaReadResult: Wire;  // SemaReadCompleted
    type Effect: Wire;          // CommandEffect   (effect vocabulary)
    type EffectResult: Wire;    // EffectCompleted (effect-result set)
}

#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
// #[rkyv(bound(serialize/deserialize = "P::Event: Archive, P::SemaWriteResult: Archive, ..."))]
pub enum Work<P: Plane> {
    SignalArrived(P::Event),
    SemaWriteCompleted(P::SemaWriteResult),
    SemaReadCompleted(P::SemaReadResult),
    EffectCompleted(P::EffectResult),
}

#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
// #[rkyv(bound(... all eight projections ...))]
pub enum Action<P: Plane> {
    ReplyToSignal(P::Reply),
    CommandSemaWrite(P::SemaWrite),
    CommandSemaRead(P::SemaRead),
    CommandEffect(P::Effect),
    Continue(Work<P>),                 // unboxed — Action holds Work, Work never holds Action
}

// Routes are payload-independent → non-generic, declared once.
pub enum WorkRoute   { SignalArrived, SemaWriteCompleted, SemaReadCompleted, EffectCompleted }
pub enum ActionRoute { ReplyToSignal, CommandSemaWrite, CommandSemaRead, CommandEffect, Continue }

// Constructors + route() live ONCE on the generic (impl<P: Plane> Work<P> / Action<P>),
// so they apply to every component's binding for free.

/// The per-component seam: the engine IS the Plane (Self: Plane), so the
/// payload alphabet and the behavior live on one real data-bearing noun — no
/// separate ZST. Emitted `impl Plane for Nexus` (types) + hand-written
/// `impl Reactor for Nexus` (behavior).
pub trait Reactor: Plane {
    fn decide(&mut self, work: Nexus<Work<Self>>) -> Nexus<Action<Self>>;            // sync
    fn apply_sema_write(&mut self, w: Self::SemaWrite) -> impl Future<Output = Self::SemaWriteResult> + Send + '_;
    fn observe_sema_read(&mut self, r: Self::SemaRead) -> impl Future<Output = Self::SemaReadResult> + Send + '_;
    fn run_effect(&mut self, e: Self::Effect) -> impl Future<Output = Self::EffectResult> + Send + '_;
    fn budget_exhausted_reply(&self, exhausted: ContinuationExhausted) -> Self::Reply;
}

impl Runner {
    /// The budgeted loop matches Action<R> DIRECTLY — no NextStep, no shim.
    pub async fn drive<R: Reactor>(&self, engine: &mut R, first: Nexus<Work<R>>) -> R::Reply {
        let origin = first.origin_route();
        let mut work = first;
        let mut budget = self.continuation_limit().budget();
        loop {
            let next: Work<P> = match engine.decide(work).into_root() {
                Action::ReplyToSignal(reply)   => return reply,
                Action::CommandSemaWrite(w)    => Work::sema_write_completed(engine.apply_sema_write(w).await),
                Action::CommandSemaRead(r)     => Work::sema_read_completed(engine.observe_sema_read(r).await),
                Action::CommandEffect(e)       => Work::effect_completed(engine.run_effect(e).await),
                Action::Continue(continuation) => continuation,
            };
            if let Err(exhausted) = budget.spend_next_step() { return engine.budget_exhausted_reply(exhausted); }
            work = next.with_origin_route(origin);
        }
    }
}
```

## Authored per component (spirit/schema/nexus.schema)

The human writes leaf imports, **one `frame` binding block**, and the
component's own payload vocabularies. The frame variant names
(`SignalArrived`, `CommandSemaWrite`, …) and the `NexusWork`/`NexusAction`
re-declarations **vanish** from the component schema.

```
{ ;; leaf imports — spirit-specific, unchanged from today
  SignalInput spirit:signal:Input   SignalOutput spirit:signal:Output
  SemaReadInput spirit:sema:ReadInput   SemaReadOutput spirit:sema:ReadOutput
  SemaWriteOutput spirit:sema:WriteOutput   Entry spirit:signal:Entry  ;; ...rest... }

;; The ONE new construct: bind the shared `reaction` frame's eight slots onto
;; the component's engine noun (`Nexus`). No type alias, no path to a Rust type,
;; no `= NextStep<...>`. A slot the component lacks is simply OMITTED.
frame reaction on Nexus {
  Reply SignalOutput        Event SignalInput
  SemaWrite SemaWriteSet     SemaWriteResult SemaWriteOutput
  SemaRead SemaReadInput     SemaReadResult SemaReadOutput
  Effect EffectCommand       EffectResult EffectOutcome
}

{ ;; the component-specific payload vocabularies — the ONLY substance here
  SemaWriteSet [(Record) (Remove) (ChangeCertainty) (BumpImportance) (ChangeRecord) (RegisterReferent)]
  Record Entry   Remove Removal   ;; ...
  EffectCommand [(Stash StashRequest) (ClassifyState Statement) ;; ...16 more... ]
  EffectOutcome [(Stashed StashResult) ;; ...20 more... ]
  StashRequest { Records * DatabaseMarker * }   ;; ...records... }
```

A component with no sema plane (e.g. `agent`) just **omits the four sema
lines** from the `frame` block; today it hand-prunes those arms out of its
concrete enums.

## Generated per component (spirit/src/schema/nexus.rs)

The whole nexus plane the emitter writes: the payload enum bodies plus a
~12-line binding — versus today's **verified 2577 lines**. No `NexusWork`, no
`NexusAction`, no wrapper newtypes, no route enums, no `into_next_step` shim,
no aliases.

The payload alphabet binds onto the component's **engine** — the real
data-bearing noun (it owns the store/redb handle) — NOT a ZST marker. The
emitted `impl Plane for Nexus` sits beside the hand-written engine `struct
Nexus { … }` and its hand-written `impl Reactor for Nexus { fn decide … }`.

```rust
// @generated by schema-rust-next
pub use crate::schema::signal::{Input as SignalInput, Output as SignalOutput, Entry, ...};
pub use crate::schema::sema::{ReadInput as SemaReadInput, ReadOutput as SemaReadOutput, WriteOutput as SemaWriteOutput};

// ---- component-owned payload trees (the only genuinely per-component data) ----
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
pub enum SemaWriteSet { Record(Entry), Remove(Removal), ChangeCertainty(CertaintyChange),
    BumpImportance(ImportanceBump), ChangeRecord(RecordChange), RegisterReferent(ReferentRegistration) }

pub enum EffectCommand { Stash(StashRequest), ClassifyState(Statement), /* ...16 more... */ }
pub enum EffectOutcome { Stashed(StashResult), /* ...20 more... */ }
// StashRequest / StashResult / GuardianVerdict / Reject / ... — unchanged records.

// ---- the ONE binding: spirit's eight payload types, onto the real engine noun ----
// `Nexus` is the hand-written engine (holds the store/redb handle). No ZST.
impl triad_runtime::reaction::Plane for Nexus {
    type Reply = SignalOutput;            type Event = SignalInput;
    type SemaWrite = SemaWriteSet;        type SemaWriteResult = SemaWriteOutput;
    type SemaRead = SemaReadInput;        type SemaReadResult = SemaReadOutput;
    type Effect = EffectCommand;          type EffectResult = EffectOutcome;
}

// Work / Action / Runner are NOT re-declared and NOT aliased. The hand-written
// engine implements the behavior and names the frame inline:
//   impl triad_runtime::reaction::Reactor for Nexus {
//       fn decide(&mut self, work: Nexus<Work<Self>>) -> Nexus<Action<Self>> { ... }
//   }
```

(Earlier drafts of this report used a `struct Binding;` ZST as the `Plane`
implementor; that is rejected — no ZSTs. `P` is the engine, a real
data-bearing type. Removing the ZST costs nothing extra: `Work<P>`'s fields are
associated-type projections (`P::Event`), which Rust's `#[derive]` cannot bound
anyway, so the frame's Clone/Debug/Eq/rkyv/NOTA impls are hand-written once in
triad-runtime with the bound on the projection via the `Wire` supertrait — and
once they are, `P` can be the non-`Clone`/`Wire` engine with no problem.)

## What schema's functionality must change

The one conceptual change: today the schema treats the universal frame as
*ordinary per-component type declarations* — `spirit/schema/nexus.schema:66-67`
literally writes `NexusWork [...]` / `NexusAction [...]`, and the emitter has no
idea they are universal, so it monomorphizes them per component. The change is
that **schema gains a shared, parameterized frame that a component *binds*
rather than *re-declares*.** Everything else follows.

Per-component generated artifacts, now vs want:

| Generated artifact | Now (`spirit/src/schema/nexus.rs`) | Want |
|---|---|---|
| Work event enum | `enum NexusWork {4}` + 4 wrapper newtypes (rkyv+NOTA derives) | gone — `Work<Nexus>` shared |
| Action enum | `enum NexusAction {5}` + 5 wrapper newtypes | gone — `Action<Nexus>` shared |
| Route enums | `NexusWorkRoute`, `NexusActionRoute` | gone — shared |
| Trace names | `NexusObjectName` | gone — shared |
| Frame aliases | `pub mod nexus { pub type Work=…; pub type Action=…; }` (`:2464`) | gone |
| Runtime bridge | `pub type NexusRunnerNextStep = NextStep<…>` + `impl NexusAction for NexusAction { into_next_step }` | gone |
| Payload vocab | `NexusEffectCommand {18}`, `NexusEffectResult {21}`, sema-write set | keep, unprefixed: `EffectCommand`, `EffectOutcome`, `SemaWriteSet` |
| Frame binding | (none) | new — `impl reaction::Plane for Nexus { …8… }` |

Schema language (schema-next) — two new constructs:

1. **Declare a shared frame once.** A `reaction` frame declaration names the
   Work-event set, the Action-choice set, and the open slot list; a component
   may not re-declare it.
2. **Bind it per component.** `frame reaction on <Engine> { <Slot> <localType> … }`
   — a positional slot-binding block naming the real engine noun it lands on,
   resolved by the **existing import resolver** (extended from "resolve a leaf
   type path" to "resolve a frame and bind its slots").

Emitter (schema-rust-next) — three changes:

1. **Delete** the frame-emission paths: the `NexusWork`/`NexusAction` enums, the
   per-variant wrapper newtypes, the route enums, `NexusObjectName`, the
   `pub mod nexus` alias block, and the `NexusRunnerNextStepProjectionTokens` +
   `NexusRunnerAdapterTokens` shim (`schema-rust-next/src/lib.rs:2017-2090`).
2. **Add** one lowering: `frame … on <Engine>` →
   `impl triad_runtime::reaction::Plane for <Engine> { type … = …; }`.
3. **Keep** payload-enum emission, with unprefixed names.

## Why this is right (discipline map)

- **no-alias** — zero `pub type` in the per-component output; today's file
  carries `pub type Work`/`Action` (`:2464-2466`), this removes them. Component
  code spells `Work<Binding>` inline; methods come from `impl<P: Plane>` for
  free, so the alias buys nothing.
- **no-prefix** — slot names (`Reply`, `Event`, `Effect`) and generated enums
  (`SemaWriteSet`, `EffectCommand`, `EffectOutcome`) carry no `Nexus`/`Spirit`
  ancestry.
- **no ZSTs** — the `Plane`/`Reactor` implementor is the engine (`struct Nexus`
  with its store handle), a real data-bearing noun, not a marker.
- **methods-on-nouns** — every verb is a method on a real noun: constructors +
  `route()` on `Work<P>`/`Action<P>`, `drive` on `Runner`, the IO seam is
  `impl Reactor for Nexus` on the engine.
- **frame-once** — `Work`/`Action`/routes/`drive`/`Engine` exist in exactly one
  place; the per-component frame copies and the shim are deleted.
- **actor-native** — the kameo engine actor is generic over the daemon (as
  today); `Plane: Send + 'static` + `Wire: Send + 'static` mean every mailbox
  message is `Send + 'static` with no glue. `decide` stays sync; IO hooks are
  async, preserving no-blocking-in-handler.

## The schema capability required

**One feature: a shared-frame import with named-slot binding.** Two halves:

1. **A frame declared once** in a workspace-shared schema (`reaction`): it names
   the Work-event set, the Action-choice set, and the open slot list; a
   component may not re-declare it. (The schema-level analogue of the generic
   parameter list on `Work<P>`/`Action<P>`.)
2. **A binding directive** in the component schema:
   `frame reaction on <Engine> { <Slot> <localType> … }`, a positional
   slot-binding block (not `(key value)` pairs) naming the engine noun it lands
   on. `reaction` resolves by bareword through the
   **existing import resolver** — the same `ImportSource`/`ResolvedImport`
   machinery that already resolves `spirit:signal:Input`, extended from
   importing a leaf type to importing a parameterized frame and binding its
   slots.

The emitter lowers the block to `impl Plane for <Engine>` on the component's
real, hand-written engine type (no new type at all). That shape (a) carries
methods (all behavior is on the generic and applies to the engine binding),
(b) is orphan-clean (the component owns its engine, so `impl Plane for Nexus`
is foreign-trait-on-local-type, always legal), and (c) needs no `pub type` —
the frame is reached as `Work<Nexus>`, a real generic application that supplies
its methods transitively.

## Honest residue (the "it must compile" bar)

1. **NOTA codec on the generic — the one gating prerequisite. Prove with a
   compile prototype before building.** The `nota_next` derive uses
   `split_for_impl()` on the type's own generics. Whether `#[derive(NotaEncode)]`
   on `Work<P>` compiles hinges on the bound reaching `P::Event`: the `Wire`
   supertrait on each `Plane` slot (`type Event: Wire`, `Wire: NotaEncode`)
   *should* satisfy it transitively, but if the derive instead pushes a bare
   `P: NotaEncode` onto the impl head it will both bound the wrong thing (the
   ZST marker) and miss the projection bound. **Settle it with a 10-line
   prototype.** Bounded fallback either way: add a `#[nota(bound = "…")]`
   container attribute to the derive (a one-time change), or hand-write the two
   `NotaEncode`/`NotaDecode` impls for `Work<P>`/`Action<P>` in triad-runtime.
2. **rkyv generic derive** — supported via `#[rkyv(bound(serialize/deserialize
   = …))]`; the associated-type-projection case (`P::Event`) needs the explicit
   bound (the `Nexus<Root>` precedent uses a field type directly and doesn't
   cover it). Prototype alongside #1.
3. **triad-runtime dependencies** — rkyv currently comes via `signal-frame`;
   `nota-next` is absent. Add `nota-next` under a new `nota-text` feature (and
   surface rkyv directly if the wire derives need it). Trivial Cargo edit, part
   of the same landing.
4. **Absent-slot semantics** — binding an unused slot to `Infallible` leaves the
   arm *present-but-uninhabited* in the generic (a different wire tag than
   today's `agent`, which physically omits the arm). Recommended call: **accept
   the uninhabited-arm shape** — uniform, one generic, and breaking is normal
   pre-production. Pruning would reintroduce a per-component concrete enum, the
   very thing this deletes.
5. **Orphan rule / kameo** — clean by construction; no residue.

## Sequencing into 618's fix

This report is the *target*; report 618 lists the flaws. The landing order:
prove residue #1/#2 with a prototype → add the `reaction` frame + `Plane` to
triad-runtime with working wire derives → teach schema-next the `frame`
binding directive → switch one component (spirit) and delete its 2577-line
nexus.rs down to the payloads-plus-binding → roll the other 13. The `Nexus*`
rename (618 flaw 2) folds in for free, since the new frame is authored with
unprefixed names from the start.
