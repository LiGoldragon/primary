---
title: 523 — "Isn't that what the datatypes are for?" — resolution decomposed
role: designer
variant: Psyche
date: 2026-06-05
topics: [schema, asschema, nota, structural-macro, schema-next, resolution, datatypes]
description: |
  The psyche's pushback on "removing Asschema means relocating resolution":
  isn't that just what the datatypes schema deserializes into are for?
  Decomposing Asschema's 9 resolution jobs against that framing shows the
  psyche is largely right — ~5 are inherent in well-designed datatypes, 1
  is trivial, 2 are cross-reference read-methods, 2 are Rust projection
  (the emitter), 1 disappears. None need a separate resolution engine or a
  SchemaResolution IR. Refines the 522 convergence.
---

# 523 — Resolution is (mostly) the datatypes

The psyche, replying to the operator's "removing Asschema means
relocating resolution, not deleting it": *"isn't that what the datatypes
that schema will be deserialized into [are] for?"*

The psyche is largely right, and it deflates the framing. Here is the
actual resolution inventory (from report 520's recon) re-read against
that question — what each Asschema "resolution" job *actually is* once
schema deserializes into typed datatypes:

| Asschema job | What it actually is |
|---|---|
| Newtype / alias collapse | **Inherent** — a single-field struct datatype *is* a newtype |
| Reserved scalar (`String`/`Integer`/`Boolean`/`Path`) | **Inherent** — distinct variants of the type-reference datatype |
| Nested inline declarations | **Inherent** — a nested datatype, held as authored |
| Visibility (public/private) | **Inherent/trivial** — top-level = public, inline = private; a property or derivation |
| Source order | **Inherent** — the datatype preserves authored order |
| Derived field naming (Pascal→snake) | **Trivial method** — computed from the field's type reference |
| Symbol-path resolution | **Cross-reference read-method** — navigates the tree |
| Variant payload resolution (bare name → type) | **Cross-reference read-method** — a namespace lookup |
| Nested-inline → sibling Rust structs | **Rust projection** — the emitter's job (Rust can't nest type declarations) |
| Emission ordering | **Rust projection** — the emitter orders as it emits |
| Context aggregation (collect inlines mid-traversal) | **Disappears** — a lowering-phase artifact |

## The conclusion

Of Asschema's resolution work: **~5 jobs are inherent** in well-designed
datatypes (free the moment schema deserializes into them), **1 is a
trivial method**, **2 are cross-reference read-methods** (symbol path,
variant payload — they need the namespace datatype in scope), **2 are
Rust projection** (the emitter turning typed schema into Rust's shape),
and **1 disappears**. **None of it is a separate resolution engine, and
none of it needs a `SchemaResolution` IR.**

So the psyche's framing is right: the datatypes schema deserializes into
*are* the resolved schema — that is what they are for. "Relocating
resolution" overstates a thing that mostly evaporates into the datatypes'
own structure, plus two lookup methods, plus the emitter's existing
Rust-shaping job.

## What this refines about 522

Report 522 (concurring with operator 314) landed on a pragmatic
`SchemaSource::resolve() -> SchemaResolution` projection. The psyche's
point suggests **that projection may be unnecessary scaffolding.** If the
datatypes hold the resolved structure (they do, for ~5 of the jobs) and
expose the two cross-references as read-methods, then there is no
resolved-view object to build — the emitter reads the typed source
datatypes directly, doing only Rust projection. That is closer to the
psyche's instinct and to "schema is just NOTA," and it does not reopen the
operator's valid boundary concern, because the two cross-reference
lookups are *simple methods on the datatypes*, not a re-implemented schema
engine.

The operator's guardrail still holds in spirit: no durable IR, no
artifact, no store. The psyche tightens it further: maybe not even an
in-memory projection *type* — just the datatypes and their methods.

## The one genuinely-open seam (small)

The only real remaining decision, and it is local: do the two
cross-reference lookups (variant payload, symbol path) resolve **at
deserialize-time** (baked into the datatype while the namespace is in
scope) or **at read-time** (the datatype holds the bare reference; the
emitter looks it up against the namespace it already has)? Both are fine;
read-time keeps the datatype a faithful image of the authored source
(more "just NOTA"), deserialize-time front-loads the lookup. This is a
small seam, not the "where does the resolution engine live" question that
314/520 framed.

## Process note

This was the psyche's reply *to the operator*; per the forwarded-prompt
discipline the operator owns capturing it as intent. I am engaging with
the substance here and will gap-check the operator's capture after a beat
rather than pre-emptively duplicating the record.

## Lineage

Refines: 520 (removal design), 522 (convergence). Decisions: `pv61`/`js6q`
(removal), `i0e6` (type-directed decode), `ejvc`/`lcwu` (mechanism).
