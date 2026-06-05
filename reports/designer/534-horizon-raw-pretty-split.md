---
title: 534 — Horizon raw/pretty split — intent resolution and handoff
role: designer
variant: Decision
date: 2026-06-05
topics: [horizon, raw-horizon, pretty-horizon, cluster-data, derive-layer, nix, lojix, handoff]
description: |
  Psyche decision (High): horizon splits into RAW horizon (core typed
  cluster-data model) and PRETTY horizon (pre-computed pre-derived helper
  variables Nix consumes). Resolves the derive-collapse fork; supersedes
  the m85j "move into Nix composition" mechanism. Records the new intent
  (9p8v), tombstones m85j, and hands off the remaining live horizon forks
  to the agent already in the project.
---

# 534 — Horizon raw/pretty split — intent resolution and handoff

## The decision (psyche, High certainty — record `9p8v`)

Horizon was feeling **too big** for what it should do. The fix is not to
push logic out to Nix (the old `m85j` mechanism); it is to **split horizon
into two clearly separated parts** so the model and its presentation helpers
stop tangling:

- **RAW horizon** — the core typed cluster-data model: the `NodeService`
  enum and the typed facts, arch resolution, the rendered typed name and
  key-line newtypes, the cross-node fan-in lists, typed validation, and the
  secret-binding resolution map.
- **PRETTY horizon** — a *separate* layer that adds the **pre-computed,
  pre-derived helper variables that Nix then consumes**: the behaves-as and
  gating booleans (`is-dispatcher`, `is-large-edge`, `enable-network-manager`),
  the resolved magnitude values, the lid-switch policy, and the trust-gated
  extra-groups list.

The load-bearing property: **the pretty helpers are computed in typed Rust
inside the pretty-horizon part, NOT pushed into Nix composition.** Nix only
ever *uses* already-derived variables — it never holds the logic. Typed
source stays typed end to end (`qkvx`, typed-source-first).

## Why this resolves the readability-thesis tension

The earlier `m85j` framing ("move the gating booleans into Nix composition,
emit the raw `Magnitude` ordinal and let Nix do the `>=`") sat in tension
with the readability thesis / refusal-of-opacity just blessed into
`ESSENCE.md` — it pushed real comparison logic out of the typed, compiler-
checked world into untyped Nix. The raw/pretty split **dissolves the
tension instead of trading it off**: every derivation, including the
`at-least` magnitude comparison, is *resolved in pretty-horizon (typed)*,
and Nix receives a finished value. The boundary becomes clean and namable:
**raw horizon is the typed model and all computation; pretty horizon is the
typed pre-derivation layer; Nix is a pure consumer of pre-derived
variables.** Nothing of the program lives in Nix — Nix composes finished
values, which is what it is for.

## What `m85j` said, and how its ten items re-bucket

`m85j` (Decision, High, 2026-06-04 15:32:54) is **removed** (record
`9p8v` supersedes its mechanism and preserves its still-valid timing).
Tombstone — full original text:

> Horizon simplification is a partial collapse landing AFTER cutover, not
> before. Move into Nix composition the behaves-as booleans, the gating
> booleans like is-dispatcher and is-large-edge and enable-network-manager,
> the at-least magnitude ladders by emitting the raw Magnitude ordinal, the
> lid-switch policy, and the trust-gated extra-groups list — re-exported
> once from a single CriomOS derive module so consumer modules stay
> untouched. Keep in Rust: arch resolution, the rendered typed name and
> key-line newtypes, the cross-node fan-in lists, typed validation, and the
> secret-binding resolution map. Parity is the bar for retiring the dual
> stack; the collapse is a clean follow-on that does not gate cutover.
> Prepare the derive seam during cutover so the collapse is a drop-in.

The re-bucketing is exact — the same ten items, re-homed:

| `m85j` item | Was going to | Now lives in |
|---|---|---|
| behaves-as booleans | Nix derive module | **pretty horizon** (typed) |
| gating booleans (is-dispatcher, is-large-edge, enable-network-manager) | Nix derive module | **pretty horizon** (typed) |
| at-least magnitude ladders | Nix (`>=` on raw ordinal) | **pretty horizon** — resolved value, not raw ordinal |
| lid-switch policy | Nix derive module | **pretty horizon** (typed) |
| trust-gated extra-groups list | Nix derive module | **pretty horizon** (typed) |
| arch resolution | Rust | **raw horizon** |
| typed name / key-line newtypes | Rust | **raw horizon** |
| cross-node fan-in lists | Rust | **raw horizon** |
| typed validation | Rust | **raw horizon** |
| secret-binding resolution map | Rust | **raw horizon** |

**What carries over unchanged from `m85j`:** the timing — the pretty layer
lands **after cutover**, **parity is the bar** for retiring the dual stack,
and the collapse **does not gate cutover**. Prepare the (now pretty-horizon)
derive seam during cutover so it is a drop-in.

## Remaining live horizon forks (for the handoff agent)

These surfaced in the 533 situation scan and are still open — not resolved
by `9p8v`. Flagging so the agent in the project has them:

- **horizon-rs vs horizon-next** (`x8iv`, Low) — `horizon-rs` is the
  predates-the-convention hack; `horizon-next` is the schema-derived
  successor. Open: which becomes *the* ported horizon, and does horizon
  become a full component-triad? The raw/pretty split should be built in
  the schema-derived successor, not retrofitted into the hack.
- **Parity scope for cutover** (`fe2j` + `m85j`/now `9p8v`) — full-fidelity
  parity vs a lean minimal-viable deploy path as the cutover bar. Sizes the
  port effort. Open.
- **`meta-signal-lojix` standalone-repo timing** (`vudl`, settled) — carried
  as a local path-dependency package until cutover, standalone repo created
  *at* cutover. The `signal-lojix/INTENT.md` (lines ~36-37) is **stale**
  against the `vudl` authority split and should be refreshed.
- **signal-frame streaming substrate** (`brgo` carries the open question
  verbatim) — deliberate scaffolding ahead of this work, or leftover? Most
  changes the cutover effort estimate. Open.

## Status

- Intent recorded: **`9p8v`** (Decision, High, Zero).
- Superseded entry removed: **`m85j`** (tombstoned above).
- **Not implemented** — this is the intent resolution + handoff only, per
  the psyche's instruction to do the intent implementation and pass the
  report to the agent already in the project. Implementation (building the
  raw/pretty seam in the schema-derived horizon successor) is that agent's.

Per psyche 2026-06-05.
