# 209 — operator synthesis: refined triad and schema stack direction

## Opinion

The forwarded prompt is a real architecture refinement, not just a
renaming. It clarifies that there are two different triads that agents have
been partially conflating:

- **Repository triad**: `<component>` + `signal-<component>` +
  `core-signal-<component>` (or current `owner-signal-*` while the rename is
  still in transition). This is packaging and authority separation.
- **Runtime triad**: **Signal + Executor + SEMA** inside the component daemon.
  This is behavior and dataflow.

Those two triads should both stay. The repository triad tells us which code
lives where. The runtime triad tells us which generated objects and
hand-written methods exist inside the daemon.

Trying to collapse the names would create drift. "Signal" as a repository
name and "Signal" as a runtime plane are related but not identical. The clean
wording is:

> The component repository contains the daemon. The daemon implements the
> runtime planes: Signal, Executor, and SEMA. The signal repositories contain
> schema-derived public/core wire surfaces consumed by the Signal plane.

## What the prompt adds

### Signal becomes the reactive boundary

The Signal plane is the external, reactive surface. It receives typed messages
from people, agents, peer daemons, and eventually federated persona systems.
CLI NOTA is only the human/agent text projection; daemon-to-daemon traffic is
binary rkyv in a signal frame.

The schema implication: public and core signal schemas emit root input/output
objects, short-header route tables, frame encode/decode methods, caller/process
origin hooks, and NOTA text projections for CLI/debug edges.

### Executor becomes the decision plane

The Executor plane is where the daemon decides what a message means in the
current runtime context:

- reject before processing;
- accept and forward without durable state;
- accept and lower into SEMA work;
- split into fan-out work;
- shape the final reply after SEMA responds.

This is the place where "the engine matches one tree against another" becomes
code: generated signal input meets runtime state and generated SEMA command
language. The implementation should be methods on schema-emitted request,
command, response, and engine state objects. It should not be a bag of free
functions.

The schema implication: schema should not try to generate opaque business
logic. It should emit closed vocabularies and trait/method surfaces that make
the decision points obvious. Rust writes the behavior on those nouns.

### SEMA becomes the single-writer state plane

The SEMA plane is the durable-state interface. It owns storage and applies
state changes through one writer. Nothing changes durable state "on its own";
Signal and Executor ask SEMA to act.

The schema implication: SEMA schemas should emit command/response objects,
storage records, schema hashes, migration surfaces, and typed state
projections. Redb is an implementation backend, not the architecture name.

## Implementation meaning

The current running schema-stack proof is close in direction but incomplete
against this refined triad.

`reports/operator/208-schema-stack-missing-implementation-audit-2026-05-26.md`
already names the biggest concrete gaps: transport route/header logic is still
hand-written, `schema-next` is not yet a fixed-point macro engine, imports are
not resolved, schema diff/upgrade is absent, and `spirit-next` is not
production-feature equivalent.

The refined triad changes the priority order slightly:

1. **Emit Signal plane behavior first.** Move frame encode/decode,
   short-header route matching, and route objects into schema-rust-next
   output. `spirit-next` transport should call generated methods on root
   signal objects.
2. **Then express the Executor plane.** Add a small schema-derived executor
   contract in `spirit-next`: generated `Input` lowers to generated
   `SemaCommand`, generated `SemaResponse` becomes generated `Output`.
   Hand-written Rust methods implement the lowering and reply shaping.
3. **Then make SEMA durable.** Replace the in-memory store with redb-backed
   SEMA records, persisted schema header/hash, daemon-stamped timestamps, and
   multi-topic Spirit v0.3 parity.
4. **Then add schema diff/upgrade.** Once Signal/Executor/SEMA are explicit,
   upgrade derivation has the objects it needs: wire input/output changes,
   executor projection changes, and storage record changes.

This is narrower and stronger than "generate everything." The generator emits
objects, codecs, route tables, traits, and skeleton surfaces. The authored
Rust implements behavior as methods on those objects.

## What should be documented

The operator opinion is that this belongs in three guidance surfaces:

- `skills/component-triad.md`: add a subsection distinguishing repository
  triad from runtime triad. The current file only describes the repository
  triad and verb layers; it needs the Signal / Executor / SEMA runtime-plane
  terminology.
- `skills/rust/methods.md`: already has "Schema-generated objects are the
  method surface." It should gain one sentence tying that directly to
  Signal/Executor/SEMA: executor behavior is authored as methods on generated
  signal/SEMA objects and state-bearing runtime actors.
- Schema-stack repo `INTENT.md` or `ARCHITECTURE.md`: define the generated
  surfaces by plane so implementation tasks can be tested against them.

I would not create a new standalone skill yet. The two existing skills already
own the concepts; adding one more skill would make discovery worse.

## Test implications

This architecture should become tests, not just prose:

- A Nix check fails if `spirit-next` manually maps short-header values to
  `Input`/`Output` variants outside generated code.
- A Nix check proves CLI boundary is NOTA text while daemon boundary is binary
  rkyv frames.
- A Nix check proves Executor lowering is a method/trait impl on generated
  objects or state-bearing engine objects, not a free function.
- A Nix check proves SEMA is the only writer to the durable store.
- A Nix check proves schema changes regenerate types before implementation
  code compiles.

The tests should use `spirit-next` as the first proof, but the constraints
should live in a central integration test surface once the multi-repo stack is
stable enough.

## Federation implication

The federation part of the forwarded prompt should not drive the immediate
implementation slice. It is a design pressure, not the next code target.

The practical implication is that every persona can be treated as a
context-bearing actor system whose external Signal plane is enough for another
persona to ask for work or opinion. That means the message identity, reply
channel, async mail, and caller-origin story matter. But those should follow
after the local triad is explicit and tested.

Immediate rule:

> Build one local component that is beautifully Signal / Executor / SEMA before
> attempting cross-persona federation.

## Risks

The biggest risk is that "Executor" becomes another free-function helper layer.
That would preserve the old ugliness under a better name. Executor should be a
plane of actors and methods on objects, not a namespace of functions.

The second risk is generating trait surfaces too aggressively. A previous
InteractTrait design was retracted because methods are interactions. Schema
should emit only traits that are genuinely protocol surfaces: codec, frame,
route, upgrade, projection, storage. It should not emit abstract interaction
traits just because two objects meet.

The third risk is letting the federation vision pull implementation away from
Spirit parity. Spirit-next still needs v0.3 feature parity: durable database,
multi-topic records, topic counts, query modes, daemon-stamped timestamps, and
production migration. Federation comes after the substrate behaves.

## Operator recommendation

Do not restart the whole stack again. The right move is to update the target
interfaces in place:

1. Keep `nota-next`, `schema-next`, `schema-rust-next`, `spirit-next`, and the
   new `spirit` triad repos as the implementation substrate.
2. Add the runtime-triad vocabulary to guidance and architecture.
3. Make the next code slice generate the Signal plane transport/route behavior
   from schema.
4. Add Executor and SEMA schemas for Spirit as soon as the generated Signal
   plane is real.
5. Treat schema diff/upgrade as the first production-readiness layer after
   Signal/Executor/SEMA are all represented.

The durable slogan is:

> Schema names the nouns and protocol surfaces. Rust writes the methods.
> Runtime behavior flows Signal → Executor → SEMA → Executor → Signal.
