# Subagent Audit Opinion: Refined Runtime Triad

## Scope

This report treats the forwarded designer prompt as design material, not as direct
work instructions to this subagent. The prompt refines the meaning of a
component's internal architecture around three runtime planes: Signal, Executor,
and SEMA. My opinion is that this is a real architectural clarification, but it
must be named carefully so it does not collide with the existing repository
triad discipline.

## Core Read

The strongest interpretation is:

- **Signal** is the reactive external boundary. It receives messages from
  people, agents, CLIs, daemons, and other persona systems. It owns message
  shape, caller provenance, wire encoding, short-header triage, and the initial
  validity surface.
- **Executor** is the internal decision plane. It decides whether a message is
  valid, accepted, rejected, forwarded, lowered into a state operation, or
  answered without touching state.
- **SEMA** is the durable state plane. It is the interface to storage and
  persistent facts. It should keep a single-writer rule and expose typed
  operations rather than letting callers mutate state directly.

That gives the component a clean reaction shape:

```text
external message -> Signal -> Executor -> SEMA
                              |            |
                              v            v
                         reply/effect <- state response
```

The important shift is that "component triad" now has two meanings in the
workspace unless we separate terms:

- The existing **repository triad** is `<component>`,
  `signal-<component>`, and `owner-signal-<component>`.
- The new **runtime plane triad** is Signal, Executor, and SEMA inside a
  component's behavior.

I recommend keeping both concepts, but naming the second one "runtime planes" or
"reaction triad" in skills and architecture files. Reusing "component triad" for
both will create avoidable agent confusion.

## Schema And Rust Boundary

The forwarded prompt strengthens the current schema direction. Schema should
own the data nouns and protocol contracts. Rust should own behavior on those
nouns.

My preferred boundary:

- Schema emits structs, enums, wire roots, SEMA operation types, replies, events,
  and trait interfaces implied by the declared planes.
- Rust implements methods and trait bodies on those emitted objects.
- Free functions remain the wrong shape because they detach behavior from the
  object tree the schema just created.
- Executor logic should be expressed as methods on generated request, command,
  reply, and runtime-state objects, not as a loose dispatch helper layer.

This means `schema-rust-next` or its successor should not merely emit passive
types. It should emit the expected attachment points:

```text
Signal object: parse, encode, header, route, caller, reply envelope
Executor object: validate, accept, lower, respond, project effect
SEMA object: query, mutate, commit, rollback or reject
```

The method bodies can be handwritten first. The trait definitions and the type
placement should still come from schema so the code has a stable target.

## Federation Implication

The federation part of the prompt is directionally coherent, but it should not
drive the first implementation slice. The near-term implementation should only
need to prove that one component has a clean local boundary between external
messages, executor decisions, and SEMA state.

Federation becomes natural only after local contracts are strict. Once Spirit,
Mind, and Orchestrate each expose schema-derived Signal and SEMA surfaces, a
remote persona can be "just another typed peer" rather than a special
integration. The "thing with context" phrasing is useful: a persona can be
addressed as a contextual actor if its external signal contract and reply
contract are explicit.

The federation design should later add:

- identity for persona namespaces,
- typed task/message identifiers,
- delivery and response correlation,
- authorization through owner/core signal surfaces,
- observability across persona boundaries.

Those should remain later until local schema-derived component behavior is
boring and tested.

## What Should Happen

My recommended operator path is:

1. **Codify the terminology.** Update the relevant architecture/skill material
   to distinguish repository triad from runtime planes. Do not let agents use
   one phrase for both.
2. **Make Spirit the proof.** Spirit should express a public Signal surface, an
   owner/core Signal surface, an Executor lowering surface, and a SEMA operation
   surface in schema. The running 0.3 behavior is the capability target.
3. **Emit attachment traits.** The schema stack should emit traits and impl
   targets for each plane, even if method bodies are handwritten. This proves
   "schema writes types and traits, Rust writes methods."
4. **Constrain with tests.** Add Nix tests that prove CLI NOTA enters at the edge,
   component-to-component transport is binary/rkyv, generated headers are used
   for dispatch, and executor code calls schema-emitted trait methods rather
   than hand-written route tables.
5. **Only then generalize.** After Spirit is schema-derived, repeat the same
   shape for Orchestrate or Mind. Federation should be an integration test after
   at least two local components use the same plane pattern.

## Risks

- **Term collision.** If "triad" means both repositories and runtime planes,
  agents will misfile work and design reports. The repo triad is packaging; the
  runtime planes are behavior.
- **Executor as helper soup.** The executor can easily become a pile of free
  functions. That would violate the method-on-object discipline and weaken the
  whole schema direction.
- **Schema overclaim.** Schema should emit type and trait structure first. It
  should not pretend to infer all behavioral decisions before the patterns are
  demonstrated in Rust.
- **SEMA single-writer drift.** If the executor can mutate storage directly, the
  state plane is not real. SEMA needs explicit command/reply types and a single
  write path.
- **Premature federation.** Remote persona awareness is important, but it should
  not be used to excuse vague local contracts. Federation works only when local
  Signal, Executor, and SEMA surfaces are strict.

## Still-Unclear Questions

1. Should the new runtime concept be named **runtime planes**,
   **reaction triad**, or something else? I recommend "runtime planes" for
   clarity.
2. Does the workspace intend to rename owner-signal to core-signal, or is "core"
   only a conceptual description for now? This affects repo names and generated
   schema names.
3. Which traits are emitted by schema in the MVP, and which remain handwritten?
   My lean is: emit trait definitions and type placement now; handwritten method
   bodies until patterns stabilize.
4. Where should SEMA's single-writer guarantee be enforced first: in the daemon
   runtime, the generated schema traits, or the test harness? My lean is all
   three, but daemon runtime first.
5. Is federation a Spirit-Mind-Orchestrate integration target for the next stack,
   or a later cross-persona target after schema-derived Spirit is deployed?

## Bottom Line

The prompt should be accepted as a structural refinement: components have a
runtime plane triad of Signal, Executor, and SEMA. It should not overwrite the
existing repository triad. The implementation priority is to make Spirit prove
the refined planes using schema-emitted types and traits, with Rust methods
attached to those objects and Nix tests proving the generated surfaces are
actually used.
