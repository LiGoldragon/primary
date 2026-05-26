# 209 — overview: refined runtime triad audit opinion

## Result

The forwarded designer prompt is already captured in Spirit. The key records
are:

- **856** — component runtime triad is Signal + Executor + SEMA, distinct from
  the repository triad.
- **857** — persona is federated at its core; persona systems communicate
  through subtasks and context-bearing opinions.
- **858** — schema derives data objects and traits; Rust writes methods on
  schema-generated objects.
- **859** — migration to schema-driven Spirit is the work direction.

No operator gap-fill intent record was needed.

## Shared conclusion

The subagent opinion and my operator synthesis converge on the same structural
point: keep two triads distinct.

- **Repository triad** is packaging and authority:
  `<component>` + `signal-<component>` + `core-signal-<component>` (or current
  owner naming until the rename lands).
- **Runtime triad** is behavior inside the daemon:
  **Signal → Executor → SEMA → Executor → Signal**.

This distinction should become guidance text. Otherwise agents will confuse
repository layout with runtime dataflow.

## My operator recommendation

Use the refined runtime triad to steer the next implementation slice:

1. **Signal plane first** — schema-rust-next should emit root signal object
   framing, short-header route matching, and codec methods. Spirit-next should
   stop hand-writing transport route tables.
2. **Executor plane second** — Spirit-next should express the lowering from
   signal input to SEMA command, and from SEMA response to signal output, as
   methods on schema-generated objects or state-bearing runtime objects.
3. **SEMA plane third** — replace the in-memory Spirit store with a real
   single-writer durable SEMA layer, including schema hash/header and v0.3
   feature parity.
4. **Schema diff/upgrade after the planes are real** — once Signal, Executor,
   and SEMA are explicit, derive main/next migrations from the assembled-schema
   diff.

## What I would change in docs

Two existing skills are the right homes:

- `skills/component-triad.md` should distinguish repository triad from runtime
  triad.
- `skills/rust/methods.md` should tie methods-on-schema-generated-objects
  directly to the runtime triad: executor behavior is authored as methods on
  generated signal/SEMA objects and state-bearing runtime actors.

I would avoid a new standalone skill for now. The existing skills already own
the concepts; adding another file would likely make discovery worse.

## Main risk

The danger is an "Executor" namespace full of free helper functions. That would
rename the old drift rather than solving it. Executor must mean methods on real
objects and data-bearing actors. Schema names the nouns and protocol surfaces;
Rust writes the methods.

## Open questions

I see two still-relevant questions for psyche/designer review:

1. Should the new runtime concept be named **runtime triad** or **runtime
   planes**? My lean is "runtime triad" when contrasting it with repo triad,
   and "planes" when describing the implementation modules.
2. Which schema-emitted traits are in the immediate MVP? My lean is to emit
   codec/frame/route/projection/storage/upgrade surfaces, but not revive the
   retracted `InteractTrait` idea. Methods are interactions.
