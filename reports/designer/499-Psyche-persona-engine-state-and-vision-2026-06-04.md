---
title: 499 - Psyche - the persona engine, the vision, and what is missing
role: designer
variant: Psyche
date: 2026-06-04
topics: [persona-engine, vision, triad-engine, schema-stack, cutover, spirit, mind, missing-pieces, misunderstandings]
description: |
  The state of the whole persona engine, written for the psyche. What the
  engine is meant to be (persona as meta-AI; the Signal/Nexus/SEMA triad;
  spirit animates), where it actually is (only the spirit pilot proves the
  schema-emitted triad; everything else is old-stack or scaffold), how the
  new schema stack emits the triad and cuts over, what is missing for the
  vision to be whole, and — most importantly — the handful of things you may
  have misunderstood and the decisions you still owe. The do-it-now work is
  filed as ten operator beads.
---

# 499 - The persona engine: where it is, where it's going, what's missing

This is the update you asked for on the whole persona engine. The full
component-by-component map is in the meta-report
`reports/designer/498-persona-engine-state-2026-06-04/` (entry 4 is the
backbone); this is the psyche-facing synthesis with the vision, the gaps,
and the corrections.

## In one breath

The engine is **one proven component and a vision of a fleet**. The spirit
pilot proves the whole schema-derived triad end to end — schema document
→ emitted Rust → real NOTA CLI + rkyv daemon with Signal/Nexus/SEMA engine
traits, typed trace, durable redb state, and the 5-variant Nexus runner.
Everything else — persona, mind, router, message, terminal, introspect — is
either hand-written on the *old* stack or a scaffold. The vision is whole
when the schema stack emits *every* component the way it emits spirit today,
persona supervises them, mind carries the work graph natively, and
production has cut over off the hand-written stack. We are at: pattern
proven once, fleet not yet emitted.

## The vision — persona is a body, the agents are minds, spirit animates

[Persona is a meta-AI system — the next evolutionary step in AI engineering;
models organised in a structure that emulates real human intelligence; what
animates humans at the highest level is spirit] (ESSENCE). Concretely that
resolves to a clean division of labour:

- The **mechanism** is typed, introspectable, single-writer, push-not-poll
  software — daemons that are dumb, durable, and observable. No component
  thinks; [there's no component that works without LLMs].
- The **intelligence** is the agent LLMs on the other end of the wire.
- The **animation** is spirit — the intent layer every agent falls back on,
  the thing that makes the fleet a living system rather than a pile of
  daemons.

The finished engine is one privileged `persona` daemon supervising, per
engine, a federation of component-triad daemons (mind, spirit, router,
message, harness, terminal, introspect, …), each a Signal/Nexus/SEMA triad,
each owning its own redb database, all upgradable in place with no downtime,
and all of that component code **emitted from schema** rather than
hand-written.

## The triad engine — Signal / Nexus / SEMA

Every daemon's runtime is three execution centers, each a schema type with
the same four-position shape, differing by ownership not authored form. The
vocabulary closes the loop: **schema specifies, signal moves, sema holds.**

- **Signal** — boundary / triage / wire. Admission, validation, the
  operation roots. The only string-tolerant edge (NOTA at the CLI, binary on
  the wire).
- **Nexus** — decisions / heavy logic / mail keeper. The decision loop;
  Signal↔SEMA translation; effects; recursion.
- **SEMA** — durable single-writer state. The component `.sema` redb
  database; the canonical state-of-record.

The real refinement, landed and verified in the pilot schema, is that input
and output are **not symmetric** — `NexusWork` is the fact stream Nexus
decides *from*, `NexusAction` is the command stream it emits *next*:

```text
NexusWork   [SignalArrived SemaWriteCompleted SemaReadCompleted EffectCompleted]
NexusAction [CommandSemaWrite CommandSemaRead ReplyToSignal CommandEffect Continue]
```

`ReplyToSignal` is the only wire exit; `Continue(NexusWork)` is in-process
recursion — Nexus feeds itself a freshly-built fact with no round trip, and
because its payload is literally the fact stream, the recursion is typed.
This is the concrete, landed form of the "recursive Nexus as universal
computation destination" you've been circling. The engine traits carry
minimal lifecycle hooks (`on_start`/`on_stop` with typed failure), wired
SEMA→Nexus→Signal, so a future supervisor can decide retry/escalate on typed
reasons.

## Where the engine actually is — the component map

This is the honest state. The cross-cutting truth: **almost the entire fleet
is hand-written on the old stack or scaffold-only; the one thing proving the
schema-emitted triad is the spirit pilot.**

| Component | State | Reality |
|---|---|---|
| **spirit** (the pilot) | BUILT as a pilot | The schema-derived proof: CLI + daemon, three engine traits, typed trace, redb store, the 5-variant Nexus. Lacks the production feature set. |
| **persona-spirit** (production) | DEPLOYED | The hand-written actor stack; the live `spirit` CLI. Has removal-candidate / recency / privacy. The cutover *source*, not the destination. |
| **persona** (engine-management) | PARTIAL, old stack | The supervisor: engine catalog, spawn, FD-handoff. Rich, but on the old signal-frame surface and not yet the privileged system daemon. |
| **mind** (central state) | PARTIAL, old stack | The destination that replaces lock-files + BEADS with a typed work graph. Real, but on the old signal-mind stack, not the schema triad. |
| **sema / sema-engine** | BUILT (library) | Typed storage kernel + database engine. Each component owns its own redb. |
| **nota / nota-codec** | BUILT | The NOTA language + codec. The embedding-safe typed-text substrate. |
| **schema** (legacy) | PARTIAL | The old schema library the next stack replaces. |
| **router / message / harness / terminal / introspect / upgrade** | SCAFFOLD or old stack | Contracts + ARCHITECTURE exist; none on the schema-emitted triad. |

## The schema stack — what emits the triad

The replacement substrate is a five-repo pipeline. Instead of hand-coding
each component's wire types and actor stack, you author one `.schema` per
component and the pipeline emits the Rust:

```text
nota-next  →  schema-next  →  schema-rust-next  →  triad-runtime  →  spirit
(parse)       (lower to       (emit Rust text)     (shared runtime,   (the proof)
              Asschema)                             trace + runner)
```

`spirit` is the consumer that proves the whole pipeline: its `lib.schema`
is lowered, emitted, checked in at `src/schema/lib.rs`, and driven by a real
daemon, with `build.rs` failing if the generated source goes stale. The
recently-ratified shape: one schema-next lowering engine, schema-as-its-own-
codec, the extracted triad runner, the `RustItem` emission token model, and
flat `SymbolPath`.

**The one correctness bug in the whole substrate**: schema-next has two
lowering engines that disagree — the registry path drops bare-header
payloads to `None` while the source path resolves them, and the test that
should catch it is green only because its fixture has no bare header. Because
the emitter sits upstream of *every* component, this is the P1 fix (filed
as a bead; the ratified fix unifies on `SchemaSource`).

## The cutover — three of them, in order

The migration off the hand-written stack is the load-bearing missing
mechanism. Three cutovers that must not be conflated:

- **A — persona as upgrade orchestrator, FIRST.** Your own intent sequences
  this: [land persona engine before spirit cutover; engine orchestrates from
  day one]. Once persona owns upgrade management, the selector-flip stops
  being a CriomOS-home symlink edit and becomes a persona concern, with
  FD-handoff (SCM_RIGHTS) giving the atomic, no-downtime cutover you
  specified. This is the gating precondition.
- **B — spirit, hand-written → schema-derived.** The first concrete cutover.
  The infrastructure is ready (CriomOS-home has the version slots and a
  `currentDefault` selector; two edits flip it). The gap is parity: the
  pilot must absorb the production feature set first.
- **C — every other component**, the same staged way: author the schema,
  emit onto triad-runtime, run both, switch consumers, retire the old. mind
  is the heaviest; introspect comes up natively on the new stack as the
  first cross-component consumer.

**The cutover ordering as a vision: persona (orchestrator) → spirit (prove
the triad) → mind + infrastructure → introspect → the engine is whole.**

## What's missing for the vision to be whole

- **The runner** (`triad_main!`) — every daemon would hand-write the same
  socket-bind + accept-loop; ratified to extract into triad-runtime, not yet
  there. The single most-repeated missing noun.
- **mind on the triad** — until mind runs as a schema-emitted triad and
  carries the work graph natively, we coordinate through lock files and
  `.beads/`, the transitional substrate the vision retires.
- **The help / description namespace** — schema data in a mirror namespace
  keyed by SymbolPath. Designed, not built; no component answers `(Help …)`
  on the new stack.
- **NOTA config-by-convention** — authored files resolving to a typed root
  by path. Designed, not built.
- **The rest of the fleet on the new stack**, and **the cutover mechanism
  itself** — there is no designed contract-equivalence gate, no redb
  data-migration path, and no rollback story for replacing production
  persona-spirit. The docs have the two Spirits coexisting; nothing yet
  *designs the switch*.

## What you may have misunderstood (you asked to be corrected)

This is the part you specifically asked for. Five honest corrections:

1. **Renaming the pilot to `spirit` does not make it production — and the
   rename is only half-done.** The repo directory is renamed and the map
   reflects it, but the Cargo package, library, and binary are still named
   `spirit-next`, and the deployed `spirit` CLI is still the hand-written
   `persona-spirit`. More importantly: before the pilot can *be* production
   Spirit it must absorb a feature set (CollectRemovalCandidates,
   RecordDefault, output-target, small-record, the variant ladder) whose
   **top layer is undecided design** — system-designer 59 found all five
   blocked on decisions you still owe (e.g. Reading-A pure-extract vs
   Reading-B fused archive-then-retract; the deployed code shipped B).

2. **Ratified is not built.** The triad runner (1574/1581), the RustItem
   token model (1576/1584), and the one-engine lowering unification
   (1572/1578) are ratified *intent*, not landed code — per your own
   landed-means-main rule. The dual-engine bug they fix is still on main.

3. **SymbolPath — I may have over-corrected, and I owe you this honestly.**
   During the certainty pass I retired your record 1586 (try the *structured*
   component/plane/variant/payload/field form) in favour of flat, reading
   your final words as "confirm flat, close structured." But 1586 was
   timestamped two minutes *after* the flat ratification, and you'd said you
   wanted to *see* the structured form in code first. So this is **not
   settled** — flat is the landed code, structured is a real thing you asked
   to try. **Decision you own: do you want me to prototype the structured
   form as a designer concept so you can compare, or is flat confirmed?**

4. **The biggest missing piece is the cutover mechanism**, not any one
   component. We have a rich vision of two stacks coexisting and zero design
   for the switch — no equivalence gate, no data migration, no rollback. If
   the engine is going to replace production, that mechanism is the thing
   most worth designing next.

5. **Two pairs you might worry conflict actually don't** (no correction
   needed): lean/break-freely (1579) vs protect-production (1589) — you
   already scoped breakage to development; and most-correct-wins (1580) +
   schema-as-its-own-codec (1573) compose. But note your own caution in 1591
   was right: schema-as-its-own-codec is a *destination* — the source has a
   one-way emit path today, not a witnessed round-trip.

## What I did, and the decisions you owe

**Done this turn:** pruned all 63 stale push-bookmarks (local + remote); the
auto-named ones confirm agents were using `jj git push -c @`, which the jj
skill forbids — I'm reinforcing that. Filed **10 operator beads** for the
do-it-now work: the P1 dual-engine fix; integrate the two pending concept
branches (my triad-runtime witnesses + system-designer's persona-spirit
dedup); extract the runner; build the RustItem token model; finish the
spirit crate rename; add a production marker to persona-spirit; thiserror;
the concept-branch prune; the spirit doc/discipline fixes.

**Decisions you owe:**
- **SymbolPath**: prototype structured (1586) or confirm flat (1577)?
- **The Spirit feature thread** (Reading-A vs Reading-B and the four
  parameters under it) — system-designer 59 has these; they gate the spirit
  cutover.
- **Whether to bless** the broader intent-maintenance cleanup (the ~12
  working-orders mis-captured as intent, per report 497).
- The cutover mechanism is the highest-leverage *design* gap — worth a
  dedicated session when you're ready.
