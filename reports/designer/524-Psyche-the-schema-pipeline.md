---
title: 524 — The schema pipeline (psyche) — deserialize, then lower
role: designer
variant: Psyche
date: 2026-06-05
topics: [schema, nota, asschema, structural-macro, schema-next, schema-rust-next, architecture, pipeline]
description: |
  The psyche's canonical schema pipeline: authored schema (NOTA)
  DESERIALIZES into rust types that define the schema fully (schema-in-rust,
  rkyv-serializable), which then LOWERS into rust interface code. Two
  arrows, not a separate assemble phase. Maps it to the code, and settles
  the SchemaResolution question: schema-in-rust IS the typed representation
  (the faithful deserialize image); resolution is methods on it used during
  lowering. Captured as record fkbz.
---

# 524 — The schema pipeline — deserialize, then lower

The psyche pinned the architecture:

```
schema  ──deserialize into rust types that define schema fully──▶  schema-in-rust  ──lower into rust──▶  rust-interfaces-code
(NOTA)        (structural macro node codec, bidirectional)         (rkyv-serializable)   (the emitter)        (Rust)
```

Two arrows, and the first one is the load-bearing change.

## What each arrow is

**Arrow 1 — deserialize (NOTA → schema-in-rust).** The authored `.schema`
NOTA deserializes, through the structural macro node codec, into Rust
types that *define the schema fully*. Because the codec is bidirectional,
**schema-in-rust is a faithful typed image of the schema — it
round-trips *canonically*.** Re-encode it and you get the *canonical*
`.schema` projection back: formatting, whitespace, and any syntactic
aliases normalize; the invariant is semantic/canonical equality, **not**
original-byte identity (operator 316, conceded). This is *not* a
lower/assemble step; nothing semantic is transformed away. schema-in-rust
is rkyv-serializable: a real typed representation, cacheable when needed.

(Distinct from the migration safety net, which *is* byte-identical: the
generated `.rs` from the old Asschema path vs the new schema-in-rust path
must diff to zero. The schema round-trip is canonical; the emission diff
is byte-exact — two different round-trips.)

**Arrow 2 — lower into rust (schema-in-rust → rust code).** The emitter
(schema-rust-next) takes schema-in-rust and lowers it into the Rust
interface code components use. *This* is where the Rust-specific work
happens — projecting the typed schema into Rust's shape.

## Why this is "no Asschema"

The old pipeline had a *different* first arrow:

```
OLD:  schema ──lower/assemble──▶ Asschema ──emit──▶ rust-code
NEW:  schema ──deserialize──▶ schema-in-rust ──lower──▶ rust-code
```

`Asschema` was produced by a separate *assemble* transformation — a
one-way, resolved IR that did not round-trip with the schema. schema-in-rust
is produced by *deserialization* — a faithful image that *does*
round-trip. Same destination role (the typed representation the emitter
consumes), reached by a faithful codec instead of a lossy assemble phase.
That is what "schema is just NOTA" means concretely: the typed form is the
deserialized NOTA, not a second assembled language.

## Mapping to the code

- **schema-in-rust ≈ `SchemaSource`** (schema-next `src/source.rs`) — the
  typed source the `.schema` decodes into. It should *become* schema-in-rust:
  rkyv-serializable, the faithful image, the single typed representation.
- **Arrow 1 = the structural macro node codec** — most `Source*` types
  already decode by shape; the remaining ones move onto
  `#[derive(StructuralMacroNode)]` (the type-directed decode).
- **Arrow 2 = `RustEmitter`** (schema-rust-next) — changes from
  `emit_file(&Asschema)` to lowering schema-in-rust.
- **`Asschema`, `to_asschema()`, `AsschemaArtifact`, `.asschema` files**
  — the separate assemble step and its IR — are removed.

## This settles the SchemaResolution question (520/522/523)

Reports 520/522 proposed a `SchemaResolution` projection; 523 questioned
whether even that is needed. The pipeline answers it: **there is no
separate resolved-view object.** schema-in-rust *is* the typed
representation (the faithful deserialize image). The resolution work
(report 523's decomposition: ~5 jobs inherent in the types, 2
cross-reference lookups, 2 Rust-projection, 1 gone) lives as **methods on
schema-in-rust's types**, computed during arrow 2. The emitter calls those
methods and does Rust projection; it does not re-implement schema
semantics — which is exactly the operator's boundary (314), preserved:
*schema-in-rust owns schema meaning (as methods); the emitter owns Rust
projection.*

So the three positions reconcile:
- **Psyche:** the datatypes (schema-in-rust) *are* the resolved schema.
- **Operator (314):** the emitter must not be a second schema engine.
- **Both hold** when resolution is methods on schema-in-rust, used by the
  lowering step — no separate IR, no emitter-side schema engine.

## What this changes in the migration (vs 522)

The 522 sequence still applies, with one simplification: there is **no
`SchemaResolution` type to introduce.** Instead:

1. Make `SchemaSource` the faithful rkyv-serializable schema-in-rust
   (finish moving `Source*` onto the structural-macro decode; derive rkyv).
2. Put the resolution work as **methods on `SchemaSource`'s types** (the
   body of `to_asschema` becomes methods that the lowering reads).
3. `RustModule::from_source` lowers schema-in-rust into Rust — calling
   those methods + doing Rust projection.
4. Build driver: deserialize `.schema` → schema-in-rust → lower; no
   `.asschema`.
5. Delete `Asschema`/artifacts/store once no consumer remains.

The byte-identical-emission witness + per-transformation tests (314)
remain the safety net.

## Adopted refinements (operator 316)

Operator feedback (report 316) endorses this framing and adds four
precisions, all correct and adopted:

1. **Canonical round-trip, not byte-identical** — fixed inline above.
2. **rkyv on the *clean* schema value, not parse helpers.** The durable
   schema-in-rust value is the clean typed schema object; source spans and
   diagnostics stay parse-time and are not serialized into it.
   *Sharpening:* the cleanest way to satisfy this is to keep the
   structural-macro decode producing **span-free typed values by
   construction** (the typed value holds content, not spans — spans are a
   decode-time error-reporting concern on the `Block`, not carried into
   the value). Then schema-in-rust *is* the decode target *is* the clean
   rkyv value — no separate clean-value projection, which keeps faith with
   "no `SchemaResolution` object."
3. **The emitter calls *high-level* methods, not primitive getters.** The
   resolution methods on schema-in-rust must expose *semantic facts* —
   resolved variant payload meaning, declaration visibility, symbol paths,
   scalar/type-reference classification, import ownership — not low-level
   getters the emitter reassembles into schema logic. This is the real
   guard that keeps the emitter a Rust projector, not a second schema
   engine.
4. **No public `SchemaResolution`; a private traversal context/cache is
   fine** if implementation needs one, kept internal to schema-next. The
   public handoff is `SchemaSource` (the eventual schema-in-rust root
   noun).

The operator's next-slice sequence leads with **fixing the nota-next
derive to direct typed decode** (report 521's recommendation, now adopted)
so schema source nodes do not inherit the string-dispatch seam — then
rkyv-ready the schema datatypes, add the source-owned semantic methods,
and add `RustModule::from_source` with Asschema-parity tests.

## Lineage

Captured: record `fkbz` (the pipeline). Refines: 520, 522, 523. Operator
feedback: 316 (adopted above). Decisions: `pv61`/`js6q` (remove Asschema),
`i0e6` (type-directed decode), `ejvc`/`lcwu` (mechanism). **Intent
duplication:** the pipeline is double-captured — `fkbz` (designer) and
`ydvg` (operator) — the third such pair after `24ds` and `js6q`/`pv61`;
flagged for a consolidation pass (see chat).
