---
title: 525 — Intent maintenance — schema-thread consolidation + duplicate removal
role: designer
variant: Audit
date: 2026-06-05
topics: [intent, intent-maintenance, spirit, schema, structural-macro, asschema, tombstone]
description: |
  Psyche-authorized intent-maintenance pass over the structural-macro /
  schema-pipeline / Asschema thread. Two operations: (a) consolidate
  genuine psyche repetition into fewer records at higher weight; (b)
  remove mistaken two-agent duplicates. This report is the TOMBSTONE
  provenance for the 7 removed records (capture-before-remove discipline).
---

# 525 — Intent maintenance — schema-thread consolidation

The psyche authorized an intent-maintenance pass (2026-06-05), drawing a
distinction: **mistaken repetition** (two agents logging the same thing)
is just removed, no weight change; **genuine psyche repetition** (the
psyche restating an intent) is reintroduced as a single (or fewer) record
at **higher weight**. This pass applies both to the structural-macro /
schema-pipeline / Asschema thread.

Per `skills/intent-maintenance.md` §"Removing a record — tombstone
first", removal is destructive and irreversible (redb reuses freed pages
within hours). This report captures the full text + daemon provenance of
every removed record **before** the `(Remove …)` calls; the report IS the
provenance.

## What changed

### Consolidated (genuine psyche repetition → fewer records, higher weight)

| New record | Replaces | Weight change |
|---|---|---|
| **`xai7`** — the structural macro node mechanism (Principle) | `ejvc` + `i0e6` | both VeryHigh → VeryHigh (mechanism + its type-directed clarification, unified) |
| **`vez8`** — schema is specialized NOTA; the deserialize→schema-in-rust→lower pipeline; Asschema removed (Decision) | `lcwu` + `pv61` + `fkbz` | `lcwu` High, `pv61`/`fkbz` VeryHigh → **Maximum** (restated 3× with rising conviction — the psyche's genuine-repetition weight-raise) |

### Removed as mistaken two-agent duplicates (no weight change)

| Removed | Was a duplicate of | Captured by |
|---|---|---|
| `js6q` (operator) | `pv61` / now `vez8` (Asschema removal) | duplicate logging |
| `ydvg` (operator) | `fkbz` / now `vez8` (the pipeline) | duplicate logging |

(`24ds`, an earlier operator duplicate, was already removed by the
operator per their report 312.)

### Untouched

- `nqsb` — "every repository needs an INTENT.md" (Principle, VeryHigh) —
  a distinct topic, not part of this thread's repetition. Kept as-is.

## Tombstones (full text + provenance of removed records)

Captured via `spirit "(Observe (RecordIdentifiers ((Exact [<id>]) WithProvenance)))"`.

**`ejvc`** — `[nota schema structural-macro macro-node]` Principle, VeryHigh, 2026-06-04 19:37:22:
> NOTA needs a STRUCTURAL MACRO NODE — a special enum whose variants are matched by STRUCTURE, not by a data tag. Each variant carries a per-variant structural description (a pattern of the NOTA object shape it accepts). When an object sits at a structural-macro-node position, the decoder inspects it structurally FIRST — using structural methods on NOTA blocks (delimiter kind, sub-object count, sub-object shapes/parameters, is-it-a-qualified-symbol, does-it-have-a-sigil, etc.) — and selects the FIRST variant whose structural pattern matches, trying variants in DECLARATION ORDER (so variant order is part of the design and must be considered when the enum is written). Only after the structural match does NOTA parse the object using that matched variant's data type — RECURSIVELY, since the matched variant may itself contain structural macro nodes. The mechanism is BIDIRECTIONAL: encoding the Rust enum value emits a NOTA block matching the chosen variant's structure, and decoding recovers the variant from the block shape. This structural-macro capability is the part of the original NOTA design that was never actually implemented. Per psyche 2026-06-04.

**`i0e6`** — `[nota schema structural-macro macro-node codec derive]` Clarification, VeryHigh, 2026-06-05 07:46:04:
> Clarification of the structural macro node, refining the mechanism: NOTA does not parse anything untyped — decode is ALWAYS type-directed. A NOTA macro node IS a TYPE, specifically an ENUM. The macro-node definition is specified beforehand (the enum type and its variants in order), and that is precisely what lets NOTA read that position — the codec does not discover structure at runtime. The codec has DIFFERENT decode logic for a macro-node type than for ordinary positional NOTA: it performs a structural match on each variant of the enum (declaration order, first structural match wins), then decodes that matched variant data, recursively. The enum type that defines the macro node IS the whole specification. Runtime registries, capture-maps, and string variant-names are NOT the shape — the type drives the decode (so the natural realization is a derive on the enum, not a runtime MacroRegistry). Per psyche 2026-06-05.

**`lcwu`** — `[nota schema asschema schema-next structural-macro]` Decision, High, 2026-06-04 19:37:26:
> Schema is NOT a separate language lowered into NOTA — schema is a more specialized/refined NOTA DIALECT built on structural macro nodes. A schema file is still FULL NOTA: it decodes and encodes with NOTA, just with defined structural macros. Schema's sugar syntax — different SHAPES of object allowed at specific positions, and only where a structural macro is specified — IS structural macros. Consequence: once structural macro nodes exist in NOTA, ASSEMBLED SCHEMA (Asschema) as a distinct lowering target is no longer needed. The original design — invent a language called schema and lower it into NOTA/Asschema — is superseded by: expand NOTA with structural macros so schema is automatically just specialized NOTA. Asschema currently appears to work, but that is a side effect; the assembled-schema concept was a misunderstanding of this structural-macro design. This direction is firm (the psyche would rather expand NOTA than maintain a separate lowered language); the Asschema-removal is being validated by a worktree prototype. Per psyche 2026-06-04.

**`pv61`** — `[schema asschema nota structural-macro schema-next schema-rust-next]` Decision, VeryHigh, 2026-06-05 08:03:08:
> Asschema (assembled schema) is to be REMOVED — we no longer need it. The structural-macro-node mechanism (schema is specialized NOTA, decoded and encoded by shape via the derive) replaces it: the typed schema SOURCE is the representation, decoded directly from NOTA, and Rust emission consumes that typed source rather than a separate assembled-schema lowering target. This is now DECIDED — it supersedes the conditional pending-validation framing of record lcwu, and it overrides the operator staged recommendation to keep Asschema for now (operator report 312). The resolution work Asschema currently performs (inline-declaration hoisting, visibility, ordering, symbol paths) must be preserved as methods/projections on the typed source node types, not as a separate assembled type. Per psyche 2026-06-05.

**`fkbz`** — `[schema nota asschema structural-macro schema-next schema-rust-next architecture]` Decision, VeryHigh, 2026-06-05 09:11:48:
> The canonical schema pipeline, replacing the Asschema assemble step. Two arrows: (1) authored schema (NOTA) DESERIALIZES — via the structural macro node codec — into rust types that DEFINE THE SCHEMA FULLY (schema-in-rust), which is rkyv-serializable; (2) schema-in-rust LOWERS into rust interface code. The first arrow is DESERIALIZE, not lower/assemble: schema-in-rust is a faithful, round-trippable typed image of the authored schema (the bidirectional codec target), NOT a separately-assembled IR. There is no separate assemble/lower-to-Asschema phase — schema deserializes directly into the typed rust form. schema-in-rust is the single typed representation the emitter lowers; the resolution work lives as methods on schema-in-rust types, used during the lower step (schema-in-rust to rust), keeping the emitter from reimplementing schema semantics. Per psyche 2026-06-05.

**`js6q`** (operator) — `[schema nota asschema structural-macro]` Decision, VeryHigh, 2026-06-05 08:02:13:
> Asschema is no longer needed as the schema stack's intermediate language; authored schema should stay NOTA and decode/encode through typed structural macro node codecs, with schema source node types carrying the structural macro behavior.

**`ydvg`** (operator) — `[schema rust rkyv asschema emission]` Clarification, VeryHigh, 2026-06-05 09:08:09:
> The schema stack pipeline is: authored schema deserializes into Rust datatypes that fully define schema; that schema-in-Rust value is rkyv-serializable; Rust interface code is lowered or emitted from that typed schema-in-Rust value.

## Removal executed

After this report is committed (provenance durable), the 7 records above
are removed via `spirit "(Remove [<id>])"`: `ejvc`, `i0e6`, `lcwu`,
`pv61`, `fkbz`, `js6q`, `ydvg`. Active truth is now carried by `xai7`
(mechanism) and `vez8` (direction/pipeline). Report lineage references to
the old ids (reports 517–524) remain valid as history; this report maps
old → new.

## Going forward — one capturer per thread

The duplication root cause: both designer and operator captured the same
psyche statements across this thread (`js6q`/`pv61`, `ydvg`/`fkbz`,
earlier `24ds`). Proposed discipline, pending psyche/operator agreement:
for a live design thread the psyche is conducting with a specific lane,
**that lane owns intent capture**; the other lane gap-checks (per the
forwarded-prompt discipline) rather than re-capturing. This pass is the
cleanup; the discipline is the prevention.
