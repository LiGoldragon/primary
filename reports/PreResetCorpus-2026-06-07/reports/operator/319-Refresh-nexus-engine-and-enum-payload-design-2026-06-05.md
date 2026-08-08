---
title: 319 — Refresh — Nexus recursive-engine design, the enum-payload rule, and the generated triad runner
role: operator
variant: Refresh
date: 2026-06-05
topics: [nexus, recursive-computation, nexus-work-action, enum-payload, schema, triad-runner, signal-nexus-sema, spirit-next]
description: |
  Agglomerated operator-side engine-design surface. Absorbs the un-superseded
  substance from operator 285, 286 (record-1419 generated-runner intent
  manifestation), 287, 288, 289 (Nexus as a recursive computation engine —
  NexusWork/NexusAction asymmetry, internal control interface), and 290 (the
  enum-payload-variant design rule). The Nexus recursive-engine design is
  canonical in designer 505-Refresh and Spirit record z6qu (the nexus interface
  is the engine's internal feature interface, VeryHigh); this Refresh holds the
  operator-side reading plus the still-live enum-payload authoring rule, with
  the stale Asschema lowering examples dropped.
---

# 319 — Refresh — Nexus recursive-engine design, enum-payload rule, generated runner

## What this report is

The operator-side engine-design surface, agglomerated from the 2026-06-02
nexus/runner reports (285-290). The *design* substance for the Nexus recursive
engine is canonical in **designer 505-Refresh** (the triad-engine Signal/Nexus/
SEMA surface, which already absorbed designer 477) and in Spirit record z6qu
(the Nexus interface is the engine's INTERNAL FEATURE INTERFACE — every engine
feature is a Nexus verb+object so the full feature surface is visible in the
nexus schema, VeryHigh, today). This Refresh keeps the operator-side reading
that is not duplicated there, plus the still-live enum-payload authoring rule
(operator 290), and drops the stale `.asschema` lowering examples those reports
carried.

## Nexus as a recursive computation engine (absorbs 287, 288, 289)

Nexus input and output are **not symmetric**. Nexus consumes *work* and emits
*actions*; the two are different schema types, not a single envelope reused on
both sides:

- **NexusWork** — what Nexus is asked to decide on. It arrives from Signal
  (external facts), from SEMA completions, or recursively from a prior Nexus
  action.
- **NexusAction** — what Nexus decides. An action either finishes as a Signal
  reply, commands SEMA / effects, or **recurs** as more Nexus work.

Recursion is schema-enumerated, not an unrestricted universal wrapper:
`Nexus<Root>` is not a generic envelope you can put anything in. The work and
action roots are real multi-variant enums whose variants name the actual
decision branches.

The first model is a **daemon-internal Nexus control interface**, not a public
subprocess protocol (Spirit 1464). Nexus receives external facts through Signal
and SEMA completions, and it can also produce internal control actions that
schedule more Nexus work, defer SEMA work, shed load, preserve tracing, or
notify clients the system is busy. The public subprocess/cross-repo composition
shape is a later direction, not the starting point.

This aligns with z6qu: because every internal feature — any computation, any
filter or condition on results, any conditional write, any internal logic — must
be a declared Nexus verb+object, the recursive control surface IS the readable
catalog of what the engine can do internally. Internal features do not live as
inline hand-written logic hidden from the schema.

## The enum-payload-variant rule (absorbs 290)

The authoring rule for reply/decision shapes, grounded in still-live intent
(Spirit records 73, 437, 1269, 1294/1295, 1466-1468):

- **Direct enum payload** when the carried data is one axis of choice:
  `Output [(Busy BusyReason)]` with `BusyReason [DatabaseOverloaded
  ResourceDisconnected OtherBusyReason]`. The generated value is `(Busy
  DatabaseOverloaded)`.
- **Struct payload** when the value is a product of independent facts:
  `Output [(RecordAccepted SemaReceipt)]`.
- **Nested data-carrying enum** when only some choices need extra data:
  `BusyReason [(DatabaseOverloaded RetryGuidance) ResourceDisconnected
  OtherBusyReason]`.

The discipline: **do not invent a wrapper struct that exists only to hold one
enum that could be the payload directly.** A `BusyReport { BusyReason *
RetryGuidance * DatabaseMarker * }` is wrong when the runtime decision is only
"busy because this reason" — it forces every busy reply to pretend to be a
multi-field product and hides the useful choice one layer deeper. Add structure
only when there are at least two independent facts all variants of that branch
must carry. This is the "notation truthfully represents the data shape; no empty
wrappers" rule (record 1269) applied to runtime replies.

Two compact header forms ride on the same rule:

- **Inline payload enum at the header position** (records 1467/1468):
  `(Busy [DatabaseOverloaded ResourceDisconnected OtherBusyReason])` declares
  the payload enum inline; the header stays a vector of variant-signature
  objects.
- **Type-table variant resolution** (record 1468):
  `Output [RecordAccepted RecordsObserved Busy Rejected]` — a listed name
  resolves to a data-carrying variant when a type of that name is in scope, and
  to a unit variant otherwise. The header "does not need to know" because the
  type table already does. The explicit `(Variant PayloadType)` form stays
  available when the variant name and payload type differ.

The emitter needs no new kind for any of this: enum variants carrying named
payload types are already supported. The discipline is the schema authoring
choice, not an emitter feature.

## The generated triad runner (absorbs 285, 286)

Spirit record 1419's direction: triad wiring moves toward a programmatic,
schema-generated substrate. Daemon `main` shrinks to a tiny generated runner or
macro call; domain logic lives in non-default implementations of the generated
Signal / Nexus / SEMA engine traits — **Nexus owns the heavier decision
algorithms, SEMA owns durable state/indexes, Signal owns communication.** This
manifested into `schema-rust-next` and `spirit-next` INTENT.md / ARCHITECTURE.md
as the generated-component-runner target (kept honest: runner emission was named
as the next target, not over-claimed as already-landed code at the time). The
runner is the mechanism that makes the strict engine-separation constraint
structural rather than aspirational.

## What carried forward / what dropped

Carried forward: the NexusWork/NexusAction asymmetry, the recursion-as-
schema-enumerated-work model, the internal-control-interface-first stance, the
enum-payload authoring rule with its two compact header forms, and the
generated-runner direction.

Dropped from the source reports:

- The Nexus *design* prose duplicated in **designer 505-Refresh** and **Spirit
  z6qu** — not re-derived here.
- The `.asschema` / assembled-schema lowering examples in 290's "Assembled
  Schema" section — superseded by the Asschema removal (Spirit vez8, Maximum;
  `schema-next/INTENT.md` "Asschema is removed"). The schema authoring rule
  survives; the lowering-target illustration does not.
- The designer-477 comparison framing (288) — designer 477 retired into 505.

## Recommended permanent landings (operator → designer / repo owners)

- **The enum-payload-variant rule** is leaned-on design that recurs across every
  reply schema. It belongs as a constraint in `schema-rust-next/ARCHITECTURE.md`
  or the relevant nota/schema design skill (per the manifest-leaned-on-design
  discipline, record 2578) — expressed as a constraint so it can carry a test
  (e.g. an emission test asserting `(Busy DatabaseOverloaded)` rather than a
  wrapped record). PROPOSED to the schema-repo / designer owners; this operator
  Refresh does not edit those surfaces.

Sources retired by this Refresh: operator 285, 286, 287, 288, 289, 290. Git
history preserves them; this Refresh is the landing witness.
