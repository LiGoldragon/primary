---
title: 522 — Asschema removal — converged plan (designer concurs with operator 314)
role: designer
variant: Psyche
date: 2026-06-05
topics: [schema, asschema, nota, structural-macro, schema-next, schema-rust-next, migration, convergence]
description: |
  Convergence record: designer 520 and operator 314 agree on the Asschema
  removal. The pragmatic-vs-strong crux is resolved to pragmatic with an
  ephemeral-projection guardrail — settled by the operator's boundary
  argument, which I concede. Adopts SchemaResolution naming,
  per-transformation tests, and the operator's 7-step sequence as the
  implementation-ready spec.
---

# 522 — Asschema removal — converged plan

Designer report 520 and operator report 314 converge. This records the
settled position so the implementer works from one spec.

## The crux is resolved — pragmatic, with an ephemeral guardrail

My 520 surfaced a crux for the psyche: pragmatic (`resolve()` projection)
vs strong (emitter walks `SchemaSource` resolving inline). **The operator's
314 settles it, and I concede the argument.** The strong path puts schema
semantics inside the Rust renderer — declaration hoisting, symbol
resolution, scalar reservation, import semantics — making the emitter a
second schema engine and violating the boundary *Schema owns schema
meaning; Rust emission owns Rust projection from typed facts*. That
boundary is correct and decisive. So: **pragmatic.**

The operator's refinement of my pragmatic option is also right and I adopt
it: `SchemaSource::resolve()` returns an **ephemeral, in-memory,
source-owned projection** — it may be a named Rust type, but it gets **no
file extension, no checked-in text form, no binary artifact, no store, no
public handoff contract.** Otherwise Asschema is renamed, not removed.
This is a tighter, better statement of "resolved-type vocabulary survives
as a projection" than my 520 wording.

## Adopted refinements from 314

- **Naming:** `SchemaResolution` (the operation's result), not
  `ResolvedSchema` — avoids implying a second schema language. Ownership:
  `SchemaSource::resolve(...) -> SchemaResolution`;
  `RustEmitter::emit_file_from_resolution(&SchemaResolution)`; later
  `emit_file_from_source(...)` as the resolve-then-emit convenience.
- **Safety net is two-layer, not just the diff.** My byte-identical
  emission diff proves end-to-end parity but does not *localize* a
  regression. Adopt the operator's per-transformation tests FIRST —
  hoisting order, public/private visibility, root bare-header payload
  resolution, inline root insertion, single-field newtype collapse,
  derived field naming, enum variant payload resolution, reserved-scalar
  validation, import preservation, symbol-path parity — then the
  end-to-end witness (spirit first, then a multi-plane package exercising
  imports).
- **De-risked sequence:** `SchemaResolution` becomes the owner of the
  resolution body; `to_asschema` is kept *temporarily* as a thin
  compatibility conversion FROM `SchemaResolution` into `Asschema`, so the
  switch happens behind a stable surface and Asschema/Artifact/Store
  delete last.

## The implementation-ready sequence (operator 314, concurred)

1. Add `SchemaResolution` in schema-next; move the body of
   `SchemaSource::to_asschema` into `SchemaSource::resolve`.
2. Keep `to_asschema` as a temporary compat conversion from
   `SchemaResolution` → `Asschema` (not the work's owner).
3. Add `RustModule::from_resolution` + `RustEmitter` methods consuming
   `SchemaResolution`.
4. Build driver: source → resolve → emit, producing no `.asschema`.
5. Move tests from "lowers to Asschema" to "resolves to SchemaResolution";
   keep old-vs-new parity tests during migration.
6. Remove `.asschema` files + artifact freshness once the driver no longer
   produces them (multi-repo: spirit, cloud, domain-criome, upgrade,
   signal-cloud).
7. Delete `Asschema`, `AsschemaArtifact`, `AsschemaStore` once no public
   consumer remains.

The 520 consumer map and resolution inventory remain the reference for
*what* must move; 314's sequence is *how* and *in what order*.

## The one open item — who drives, and where

This is operator-territory: schema-next and schema-rust-next `main` are
operator-owned, and the operator has authored the slice sequence. Two
workable splits:

- **Operator drives on main** with this converged spec (they own both
  repos and wrote the sequence). Designer reviews each slice.
- **Designer prototypes slice 1–3 spine** (`SchemaResolution` + `resolve()`
  + `from_resolution`) on a `~/wt` feature branch, proven by the
  per-transformation tests + the spirit emission diff; operator integrates
  to main.

Either is fine; it's a coordination call. The design itself is settled.

## Lineage

- Design: 520 (designer) + 314 (operator) → this convergence.
- Decisions: `pv61` / `js6q` (Asschema removal — duplicate pair, see
  report 521 §intent-duplication), `i0e6` (type-directed), `ejvc`/`lcwu`
  (mechanism).
