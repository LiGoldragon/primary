---
title: 288 — Nexus Recursion Comparison With Designer 477
role: operator
variant: Synthesis
date: 2026-06-02
topics: [nexus, recursive-computation, designer-comparison, schema-composition, runner-loop, implementation-lean]
description: |
  Comparison of designer 477 against operator 287. Designer 477 strengthens the architecture with the generic envelope, subprocess examples, and cross-repo composition analysis. Operator 287 keeps the cleaner root naming and stricter action/work split. Recommended merge: use NexusWork/NexusAction root names, keep designer's fact/command variant clarity, keep recursion as schema-enumerated work/actions, and avoid treating Nexus<Root> as an unrestricted universal wrapper.
---

# 288 — Nexus Recursion Comparison With Designer 477

## Verdict

Designer 477 and operator 287 converge on the important substance:
Nexus receives facts, chooses actions, and the runner translates actions
back into facts until a Signal reply is reached. That is the right
model.

The main difference is emphasis:

- Designer 477 is stronger on breadth: generic `Nexus<Root>` envelope,
  subprocess examples, cross-repo imports, and nested computation.
- Operator 287 is stronger on discipline: `NexusWork` / `NexusAction`
  makes the roots directional and avoids keeping the weak
  `NexusInput` / `NexusOutput` names.

The merge should take both, with one guard: `Nexus<Root>` is an
envelope shape, not permission for any archived type to become valid
Nexus work. The schema must still enumerate every accepted work/action
variant.

## What Designer 477 Adds That 287 Should Adopt

### Generic Envelope As Transport Shape

Designer 477 correctly points out that `Nexus<Root>` is already a useful
envelope pattern:

```rust
pub struct Nexus<Root> {
    origin_route: OriginRoute,
    root: Root,
}
```

That is the right wrapper for origin/correlation metadata. It lets the
same transport idea carry `NexusWork`, `NexusAction`, imported Signal
roots, or effect completions without inventing a different mail wrapper
per plane.

The important constraint: the root type is still schema-chosen. The
runtime does not accept arbitrary `Root`; generated runner methods
accept specific roots.

```rust
impl ComponentRunner {
    pub fn run_signal(&mut self, input: Signal<Input>) -> Signal<Output>;
    pub fn run_nexus(&mut self, work: Nexus<NexusWork>) -> Nexus<NexusAction>;
}
```

### Command To Fact Translation

Designer 477 names the runner's job well: commands go out, facts come
back in. That is the simplest mental model for the loop.

```text
NexusAction::CommandSemaRead -> SEMA observe -> NexusWork::SemaReadCompleted
NexusAction::CommandEffect -> effect runner -> NexusWork::EffectCompleted
NexusAction::Continue -> immediate NexusWork
NexusAction::ReplyToSignal -> final Signal output
```

This should become the generated runner contract.

### Worked Recursive Examples

The examples in designer 477 are useful because they show why recursion
exists. `Observe` can read a large record set, stash it, then return a
slim handle. `introspect` can ingest a trace event, query policy, spawn
another computation, write a summary, and only then reply.

That is exactly the behavior gap current `spirit-next` has: its Nexus
slot exists, but the current domain is too thin to prove computation.
The stash pilot is the right first concrete proof.

## What 287 Should Keep Over 477

### Root Names Should Be Work And Action

Designer keeps `NexusInput` / `NexusOutput` in several places, then
clarifies them by variant names. That is better than the old state, but
not as clean as changing the roots.

Preferred root names:

```nota
NexusWork [
  (SignalArrived Input)
  (SemaWriteCompleted SemaWriteOutput)
  (SemaReadCompleted SemaReadOutput)
  (EffectCompleted NexusEffectResult)
  (InternalContinued NexusInternalWork)
]

NexusAction [
  (ReplyToSignal Output)
  (CommandSemaWrite SemaWriteInput)
  (CommandSemaRead SemaReadInput)
  (CommandEffect NexusEffectCommand)
  (Continue NexusWork)
]
```

`Input` and `Output` are too generic after Spirit 1438. The actual
roles are consumed work and produced action.

### Avoid Unrestricted Universal Nexus

Designer 477 says schemas compose because the `Root` parameter accepts
any archived type. That is technically true as a Rust bound, but it is
not the architectural rule we want.

The architecture rule should be:

```text
Nexus can process any work variant its schema declares.
```

Not:

```text
Nexus can process any type satisfying Archive + Serialize + Deserialize.
```

The first is schema-driven. The second is a generic-programming escape
hatch and would make the schema less authoritative.

### Subprocess Should Not Become A Magic Plane

Designer 477's `InvokeNexus(Box<Nexus<NexusInvocationInput>>)` is useful
as a thought experiment, but it risks creating a special subprocess
surface before the simple continuation model is proven.

Better first cut:

```nota
NexusAction [(Continue NexusWork) ...]
```

That handles in-process recursion. Cross-component recursion should go
through a component's Signal contract or through a typed effect command,
not by importing another daemon's Nexus internals.

```nota
NexusEffectCommand [
  (CallComponent ComponentCall)
  (Stash StashRequest)
]

NexusEffectResult [
  (ComponentCalled ComponentReply)
  (Stashed StashResult)
]
```

Then the runner translates cross-component calls into Signal frames and
returns the reply as `EffectCompleted`. Nexus still sees facts and emits
actions; it does not need a special nested-process concept yet.

## Naming Merge

The strongest merged names are:

```text
Root received by Nexus: NexusWork
Root produced by Nexus: NexusAction
Signal fact variant: SignalArrived
SEMA result variants: SemaWriteCompleted / SemaReadCompleted
Effect result variant: EffectCompleted
Final action: ReplyToSignal
SEMA command variants: CommandSemaWrite / CommandSemaRead
Effect command variant: CommandEffect
Immediate recursion: Continue
```

Designer's `EmitSignal` is reasonable, but `ReplyToSignal` keeps the
client-response meaning clearer. The runner may emit the reply; Nexus
chooses to reply.

## Recommended Implementation Slice

The implementation should not start with generic subprocess recursion.
Start with the smallest complete recursive proof.

1. Rename generated roots in `spirit-next` from `NexusInput` /
   `NexusOutput` to `NexusWork` / `NexusAction`.
2. Rename variants to facts and commands.
3. Add `NexusEffectCommand` / `NexusEffectResult` with only `Stash`.
4. Generate or implement the runner loop:
   `NexusWork -> NexusEngine -> NexusAction -> runner -> NexusWork`.
5. Change `Observe` to return a slim Signal reply with a handle.
6. Add follow-up query by handle.
7. Use trace to prove one request enters Nexus multiple times.
8. Add a continuation budget.

The first trace witness should show:

```text
SignalArrived -> CommandSemaRead -> SemaReadCompleted -> CommandEffect(Stash) -> EffectCompleted -> ReplyToSignal
```

That proves the recursive Nexus model without cross-component
subprocess complexity.

## Questions Still Worth Asking

### Wire Boundary Expression

Designer 477 is right that this still needs design. The open question is
not whether cross-component recursion exists; it does. The question is
how schema expresses that a target is local, another component's Signal
contract, or a daemon-private effect.

My lean: local recursion uses `Continue(NexusWork)`; cross-component work
uses `CommandEffect(ComponentCall)` or a more specific
`CommandComponent` action after the stash pilot proves the base loop.

### Correlation Across Recursion

Origin routes must become tree-shaped enough to distinguish parent and
child computations. Designer 477 identifies this correctly. It should
land with the first nested/cross-component recursion slice, not with the
simple stash pilot.

### Effect Versus SEMA

Designer 477 leans to keeping effects distinct from SEMA. I agree. SEMA
means durable state. Effects mean runtime actions outside the durable
single-writer store. The runner dispatch may look similar, but the nouns
should stay distinct.

## Bottom Line

Designer 477 is directionally right and adds useful depth. The operator
merge should keep the stricter names and smaller first proof from 287:
`NexusWork` and `NexusAction`, schema-enumerated variants, one `Stash`
effect, generated runner loop, trace proof of Nexus re-entry.

The generic envelope belongs in the implementation. The unrestricted
generic reading does not. Nexus is universal because schemas can compose
and enumerate work, not because any archived Rust type can be smuggled
into computation.
