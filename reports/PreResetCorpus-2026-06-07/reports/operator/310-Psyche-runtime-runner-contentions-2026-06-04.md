---
title: 310 - Psyche - shared triad runner contentions
role: operator
variant: Psyche
date: 2026-06-04
topics: [runtime, runner, triad-runtime, spirit, nexus, sema, signal, schema-rust-next, meta-signal]
description: |
  Operator psyche report on designer report 513: what is correct, what is
  contested, which questions remain, and the implementation shape that best
  fits the current code.
---

# 310 - Psyche - shared triad runner contentions

## Current verdict

Designer report 513 is right in its central direction: build the shared triad
runner as real library code in `triad-runtime`, with `schema-rust-next`
emitting only thin, component-specific glue. The live code supports this:
`triad-runtime` already owns argument classification, length-prefixed frames,
and typed trace transport, while `spirit` still hand-writes the recursive
Nexus loop, daemon startup, single socket accept loop, and signal transport.

My contention is about the exact load-bearing shape, not the direction. The
runner must not become a fourth engine, must not flatten Signal/Nexus/SEMA
plane identity, and must not pretend it can run several listener threads
against one owned `&mut` engine without either a central engine owner or a
mutex. The best implementation is a library-owned runtime loop plus a
generated adapter over the existing three engine traits.

## Reality anchors

- `triad-runtime` is real but still substrate-only. Its architecture says it
  owns generic frame, argument, and trace runtime, and that daemon command
  scaffolding / signal transport are future extraction waves. Its live crate
  surface is `argument`, `frame`, and `trace`, with no `Runner`, `NextStep`,
  `TriadEngines`, or generated main support yet.
- `spirit` proves the runner target. `src/nexus.rs` owns
  `ContinuationBudget` and a `loop` inside `NexusEngine::decide`; the actual
  one-step decision is the private `step_decide`. `src/daemon.rs` owns
  `DaemonCommand`, socket binding, stale socket removal, an accept loop, and
  `SignalTransport` handoff. `src/engine.rs` composes Signal and Nexus, but
  wraps Nexus in `Mutex<Nexus>` because `Engine::handle` takes `&self`.
- The generated trait shape already wants the loop outside `decide`.
  `src/schema/lib.rs` emits `NexusEngine::execute` as trace-enter, call
  `decide` once, trace-decided. The current handwritten `decide` violates
  that shape by doing the whole recursive drive.
- The generated plane envelopes are currently duplicated as `Signal<Root>`,
  `Nexus<Root>`, and `Sema<Root>` with the same two fields:
  `origin_route` and `root`. They are an extraction target, but their plane
  type identity is real and should not be erased.
- `persona-spirit` proves the multi-listener pressure. Its daemon binds
  ordinary, meta/legacy-owner, upgrade, and optional engine-management
  listeners, applies socket permissions, and has tests proving ordinary and
  policy sockets reject each other's frames. It is the right source for socket
  mechanics, but not for current naming: new runner code should say `meta`,
  not `owner`.
- `schema-rust-next` already has `RustEmissionTarget::{WireContract,
  ComponentRuntime, NexusRuntime, SemaRuntime}` and a `GenerationDriver`.
  It does not yet emit runner glue.

## Contentions

### 1. The runner extraction is correct, but the runner is not a fourth engine

The strict separation law is Signal for communication, Nexus for decisions,
SEMA for durable state. The shared runner is an execution harness over those
three engines. It may own generic transport mechanics, lifecycle order, and
the recursive loop, but it must never own communication semantics, decision
semantics, or database semantics.

The implementation boundary should therefore be:

- Signal engine / generated listener adapter owns what a frame means and how
  it becomes Nexus work.
- Nexus engine owns one decision step from work to action.
- SEMA engine owns apply/observe.
- `triad-runtime` owns the generic loop and IO scaffolding that cannot inspect
  component payloads.

This matters because a too-powerful `Runner` becomes the exact host code where
the psyche's "no daemon boilerplate outside engines" rule can be violated
again.

### 2. `TriadEngines` should be a generated adapter, not a handwritten author surface

Report 513's bundled `TriadEngines` trait is useful as the library's adapter
shape. It should not become the thing component authors implement by hand.

The author surface should remain the three existing generated engine traits
plus a component effect handler and a typed budget-exhausted reply method. The
generator should then implement the bundled runner adapter for a data-bearing
component runtime object that owns those engines. That keeps the author's work
plane-separated and lets the runner receive one object without making the
bundle a new architectural plane.

In short: `TriadEngines` is library glue, not a new engine contract.

### 3. The "one thread per listener" plus "drop the mutex" plan has a real tension

Report 513 says two things that cannot both be true without another mechanism:
spawn one accept thread per listener, and let the runner own the engine by
value so the mutex disappears.

If several listener threads call `drive` directly, they need shared access to
the engine, which requires a mutex or actor/mailbox. If the runner owns the
engine by value and relies on `&mut` as the single-flight guard, there must be
exactly one execution owner. Multiple listeners can still exist, but accepted
work has to be handed to that owner.

There are two clean shapes:

- Phase-one shape: one listener, one runner thread, owned engine, no mutex.
  This matches current `spirit` and proves the core extraction.
- Multi-listener shape: listener threads decode frames and hand typed accepted
  work to one engine-owner loop; that owner holds `&mut EngineSet` and drives
  requests sequentially. This is a minimal internal handoff, not the deferred
  backpressure/scheduler system.

The wrong shape is listener threads all sharing the engine directly while
claiming the mutex was removed.

### 4. `Plane<Root>` must preserve plane identity

Hoisting the duplicate `Signal<Root>`, `Nexus<Root>`, and `Sema<Root>`
envelope mechanics into `triad-runtime` is right. Collapsing them into one
opaque `Plane<Root>` type is wrong.

The shared shell can be an inner `PlaneEnvelope<Root>` or a generic
`Envelope<PlaneKind, Root>`, but the public generated types still need
separate Signal, Nexus, and SEMA identities. Distinct aliases are not enough
if the Rust type system cannot prevent a Signal envelope from being passed
where Nexus is expected.

This is the runtime version of the schema-contract leak we just fixed:
sharing structure is good; erasing plane semantics is not.

### 5. `NextStep` must be total and typed, with no panic projection

The current generated projection helpers in `schema-rust-next` include
panic-on-wrong-variant methods such as `into_sema_write_input`. That is
acceptable only for narrow helper methods whose caller already selected the
variant.

The runner's `NextStep` projection is different. It is the safety core of the
daemon loop. The generated conversion from component `NexusAction` to
`NextStep` should be exhaustive over the component action enum and should not
use `_ => panic`. If the action enum has a variant the runner does not know
how to dispatch, emission should fail or force an explicit escape hatch.

### 6. Future concurrency mode belongs in runtime configuration, not the public contract

I disagree with report 513's recommendation that a future mailbox mode be
selected by a field in the triad contract. "How parallel this daemon runs" is
deployment/runtime policy unless the choice changes externally visible
semantics.

Schema may eventually declare semantic constraints: single-writer required,
operation ordering, effect idempotence, cancellability, or whether reads may
fan out. The actual scheduler mode or concurrency degree should be selected
by runtime configuration. This keeps the wire vocabulary clean and avoids
hardening a scheduler choice before the deferred runtime work has evidence.

### 7. Bootstrap has a real NOTA-vs-binary tension

The workspace component-triad skill says policy state is seeded once from
`bootstrap-policy.nota`. `spirit`'s current architecture says the daemon
build is binary-only and must not link `nota-next`. Both are legitimate
constraints, but they need one explicit artifact boundary.

The clean shape is:

- The source-of-truth repo artifact remains `bootstrap-policy.nota`, because
  humans and agents author policy as typed text.
- Build/deploy tooling pre-encodes it into a typed binary signal/config
  artifact.
- The production daemon consumes only the binary artifact at first start.
- Later policy changes enter through `meta-signal` Mutate operations, not by
  rereading the NOTA file.

That preserves the human-authored bootstrap source without putting NOTA
parsing in the live daemon.

## Questions

1. Should I treat `TriadEngines` as generator-implemented adapter-only, with
   authors continuing to implement the three plane traits plus effect/budget
   hooks?
2. For future concurrency, do you want to ratify runtime/deploy configuration
   as the selector, with schema declaring only semantic ordering/idempotence
   constraints if they become real?
3. For bootstrap, should the durable rule be "repo source is NOTA; production
   daemon consumes pre-encoded binary"?

I can proceed with those leans unless you object. None of them blocks the
first single-listener runner slice.

## Suggestions

### Implementation order

1. Add `ContinuationBudget`, `ContinuationLimit`, `ContinuationExhausted`, and
   `NextStep` to `triad-runtime`, with tests using a local fake engine set.
2. Add the library `drive` loop only. Do not touch sockets yet.
3. Add generator emission for the exhaustive `NexusAction` to `NextStep`
   projection and the generated adapter over the existing engine traits.
4. Cut `spirit` over so `NexusEngine::decide` becomes the current
   `step_decide`, while `NexusEngine::execute` or the runner adapter owns the
   loop. Keep the current daemon socket path temporarily.
5. Move `SignalTransport` and `DaemonCommand` mechanics into
   `triad-runtime` after the core drive loop is proven.
6. Add the meta listener and management listener as a second slice using a
   single engine-owner loop. Do not let listener threads drive the engine
   directly.
7. Use `persona-spirit` to delete duplication after the schema-derived
   `spirit` runner is proved, but translate stale owner naming to current
   meta naming at the boundary.

### Type names I would aim for

- `ContinuationLimit`, `ContinuationBudget`, `ContinuationExhausted`
- `NextStep<Reply, SemaWrite, SemaRead, Effect, Work>`
- `ComponentRuntime` or `EngineSet` as the data-bearing adapter object
- `SignalEnvelope<Root>`, `NexusEnvelope<Root>`, `SemaEnvelope<Root>` over
  shared envelope mechanics
- `ListenerSet`, `WorkingSignalListener`, `MetaSignalListener`,
  `ManagementListener`
- `AcceptedSignal` or `AcceptedWork` as the object handed from listener code
  to the single engine owner

### Witness tests

- A fake engine test proves `drive` dispatches all five `NextStep` variants.
- Budget exhaustion returns a typed component reply and never panics.
- `spirit` trace equivalence proves Signal/Nexus/SEMA hooks still fire across
  the same live path after the loop moves out of `decide`.
- `spirit` no longer has `SemaEngine::apply` or `SemaEngine::observe` inside
  `NexusEngine::decide`; those calls live in runner-owned dispatch.
- Ordinary and meta listeners reject each other's frames with per-listener
  decoders, not payload inspection.
- The binary-only daemon dependency test stays green: no `nota-next` in the
  normal daemon surface.
- Lifecycle ordering remains SEMA/Nexus/Signal start, Signal/Nexus/SEMA stop,
  with bootstrap before listener accept.

## Operator lean

Build it, but build the smallest correct core first: typed budget, total
`NextStep`, library `drive`, generated adapter, and `spirit` cutover. Treat
multi-listener runtime as the next slice only after the single engine-owner
shape is explicit. Keep all new public names `meta`, not `owner`.
