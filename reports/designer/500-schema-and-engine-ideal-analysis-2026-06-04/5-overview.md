---
title: 500 - Schema and engine ideal analysis - overview
role: designer
variant: Synthesis
date: 2026-06-04
topics: [schema, schema-in-action, ideal-vs-current, this-code-creates-this-code, rust-emission, runner]
description: |
  Synthesis of the four-agent ideal-vs-current analysis. Entry 1 is the
  centerpiece the psyche asked for — schema in action, this-code-creates-this-code,
  and the template to repeat. The ideal-vs-current finding across the schema
  stack: nota-next is at its ideal; the other three carry the same gap from
  different angles — ratified intent that has not become main.
---

# 500 - Schema and engine ideal analysis - overview

## Entry 1 is the recurring report you asked for

`1-schema-in-action.md` is the centerpiece: schema in action on the **real**
spirit schema, seven this-code-creates-this-code pairings across five angles.
This is the template to repeat. The headline pairings:

- **One bare-name header line creates a whole interface.** The line
  `[Record Observe Lookup Count Remove LookupStash]` at `lib.schema:2` becomes
  the `Input` enum, its variant constructors, its `FromStr`, and the rkyv frame
  codec — all emitted. Three positional NOTA roots (no keywords) become `Input`
  or `Output` purely by their `MacroPosition` at `engine.rs:441`.
- **An alias binding** (`Rejected SignalRejection`) creates `pub type Rejected
  = SignalRejection;` plus the enum variant carrying it and the pass-through
  constructor — no wrapper nesting.
- **The five angles**, each with real code: **forward** (schema → Asschema →
  Rust), **backward** (the Rust mapped to its schema origin; the
  `spirit:signal:Frame` ↔ `spirit::signal::Frame` mirror), **inside** (the
  macro passes), **outside** (the CLI/daemon using the emitted types), **down**
  (the rkyv wire bytes).

Three gaps the schema-in-action view exposes: backward is reconstructed by
hand (no emitted per-type back-pointer); the SymbolPath flat-vs-structured
shape is reopened (record 1586); the trace vocabulary is hard-coded at
`schema-rust-next:1492` rather than authored in the schema (not a single
source).

## Ideal vs current — the schema stack

The four substrate repos sort along one axis: how far data-before-text and
single-home discipline have reached the landed code versus the ratified intent.

- **nota-next — at its ideal.** A clean structural-NOTA substrate that knows
  nothing about schema ([this crate does not know what a schema type means],
  ARCHITECTURE.md:82-84). The only gap is reuse-proof: one consumer today, so
  the "any structural language reuses it" claim is latent, not witnessed.
- **schema-next — right shape, ships the one bug.** Two divergent lowering
  engines on main (`lower_source` drops bare-header payloads to `None`; the
  source path resolves them) — the stack's one correctness bug, upstream of
  every component. And schema-as-its-own-codec is a destination: the source has
  a one-way emit path, not a witnessed round-trip (record 1591).
- **schema-rust-next — data-before-text only reaches the type declarations.**
  `RustModule` and the four-arm `RustTypeDeclaration` are real data, but the
  impl layer is 504 hand-indented `self.line()` calls (unchanged since the 495
  audit). The `RustItem`/`RustImplBlock`/`RustMatch` token model (1576/1584) is
  ratified intent, not landed.
- **triad-runtime — owns only trace, correctly.** The generic runner
  (`triad_main!`, 1574/1581) — the single most-repeated missing noun — is
  unbuilt.

**Three of the four gaps are the same gap from different repos: ratified intent
that has not become main** (per report 499, ratified is not built).

## The open design questions (entry 4)

Entry 4 gives each open question as an ideal pattern with proposed code: the
SymbolPath flat-vs-structured shapes shown **both ways** so the psyche can
decide; the runner (`SignalDaemonEngine` trait + generic struct); the RustItem
token model; the help/description mirror namespace; the NOTA config registry.
SymbolPath is the decision the psyche most owes (record 1586 reopened
structured against the landed flat).

## Where this points

The schema-in-action template (entry 1) is now established as the recurring
report. The ideal-vs-current gaps converge on the same operator work already
beaded: fix the dual-engine bug, build the RustItem token model, extract the
runner. Those three are the schema stack's ideals made real — and the runner,
per report 501, is also what makes the strict engine separation structural.
