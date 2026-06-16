# 657 — Showing it: a concrete component interface vs a persisted generic

The claim to make concrete: *the frame's genericity is a schema-authoring convenience — declare
the shape once, bind it per component — but it should NOT persist as a generic type in the
component's generated output; the component gets a concrete, owned interface.* Three layers,
with the real spirit types (from the verified prototype, report `656`).

## Layer 1 — Schema: the genericity lives HERE, and only here

Declare the frame **once** (the universal `Work`, in the `reaction` namespace):

```
Work (| [Event WriteDone ReadDone EffectDone]
  [(SignalArrived Event) (SemaWriteCompleted WriteDone) (SemaReadCompleted ReadDone) (EffectCompleted EffectDone)] |)
```

Each component **binds** it in one line — never re-spelling the four legs:

```
;; spirit
{ Work reaction:reaction:Work }
(Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)        ;; this IS spirit's Input
;; signal-spirit would write its own one-line binding; meta-signal-spirit its own; etc.
```

This is the whole point of the generic: **one author writes the shape once, every component
supplies only its payloads.** That is the "don't re-author the shape per component"
convenience `zjmc` demands. The genericity has done its entire job at this layer.

## Layer 2 — Generated Rust: does the genericity leak into the output?

**What we built — EXPANSION. The genericity is gone; spirit owns a concrete interface:**

```rust
// spirit/src/schema/nexus.rs
pub enum Input {                          // spirit's own named, concrete type
    SignalArrived(SignalInput),
    SemaWriteCompleted(SemaWriteOutput),
    SemaReadCompleted(SemaReadOutput),
    EffectCompleted(EffectOutcome),
}
impl Input { /* signal_arrived(...) etc. */ }
impl From<SignalInput> for Input { /* ... */ }     // normal impls, emitted for free
```

The word `Work` does not appear anywhere in spirit's output. Spirit's interface is `Input` —
concrete, owns its constructors and `From`s.

**What generic-alias would emit — the genericity PERSISTS in the output:**

```rust
// emitted once, shared:
pub enum Work<Event, Write, Read, Effect> {
    SignalArrived(Event), SemaWriteCompleted(Write), SemaReadCompleted(Read), EffectCompleted(Effect),
}
// in spirit:
pub type Input = Work<SignalInput, SemaWriteOutput, SemaReadOutput, EffectOutcome>;
//  ^ and Input has NO inherent constructors / From — the emitter cannot write
//    impl<Event, Write, Read, Effect> Work<Event, Write, Read, Effect> { ... }
```

Now spirit's interface is an *alias to an abstract generic*. A schema-authoring device has
leaked into spirit's generated surface — and dragged in the generic-impl-emission problem
(`654`) as the price.

## The two outputs are the SAME type at the wire

`Work<SignalInput, SemaWriteOutput, SemaReadOutput, EffectOutcome>` monomorphizes to a layout
**byte-identical** to `enum Input { … }`: same rkyv archive, same NOTA encoding. The prototype
proves the concrete `Input` round-trips through both (`656`). So the concrete interface loses
**nothing** versus the alias — the only difference is whether `Work<…>` shows up in spirit's
output. Concrete says no.

## Where a generic type genuinely belongs: polymorphic runtime code

The generic `Work`/`Action` *should* exist as real types in exactly one place — code that is
genuinely polymorphic over all components, hand-written in the runtime crate:

```rust
// triad-runtime/src/reaction.rs — ONE impl serves every component
impl<Reply, Write, Read, Effect, Continuation>
    From<Action<Reply, Write, Read, Effect, Continuation>>
    for NextStep<Reply, Write, Read, Effect, Continuation> { /* ... */ }
```

That is a true abstraction: one generic impl, every component's `Action` flows through it. It
lives in `triad-runtime`, hand-written, and is the *only* place the generic `Work`/`Action`
belong as types. A component's **generated** interface is not that place — there, the bound
shape is fully known, so it should be concrete.

## The principle, in one line

**Schema:** declare the frame once, bind per component (DRY authoring). **Output:** each
component gets a concrete, owned interface (`enum Input`), not a persisted generic alias.
Genericity is a tool for the *author* and for *genuinely-polymorphic runtime code* — not a
thing to stamp into every component's generated surface, where it buys nothing (wire-identical)
and costs real machinery.
