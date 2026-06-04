---
title: 71.4 — Overview — intent architecture redesign + stack rewrite, synthesised
role: system-designer
variant: Psyche
date: 2026-06-04
topics: [spirit, record-shape, intent-maintenance, agglomeration, composite, weight, archive, lojix, horizon, schema, triad-engine]
description: |
  Orchestrator synthesis of the three-angle study. Thread A (stack rewrite):
  the triad-engine separation is compile-enforced and sound; lojix adoption is
  small and mechanical (one schema + three trait impls); horizon-rs is correctly
  a library, not a component-to-be. Thread B (intent architecture): the deployed
  flat 5-field record becomes a per-kind variant enum (privacy only on the
  private variant), gains a weight axis distinct from certainty, adds a Composite
  record referencing source hashes, and a single unified archive type carrying
  composite provenance. The build target is the schema-derived spirit pilot on a
  feature branch (version 5->6, breaking — needs psyche authorization), not the
  deployed v0.5.0 contract. Four forks await the psyche.
---

# 71.4 — Overview: intent architecture redesign + stack rewrite

Kind: psyche (orchestrator synthesis of the meta-investigation)
Date: 2026-06-04

## Intent anchors

[Spirit record fields should vary by record kind rather than every record carrying every field — a private-bearing record carries a privacy field while an ordinary public record omits it; reduces total field count and gives each kind a tighter purpose-fit shape.] (Spirit Decision 3awz)

[Spirit should support composite intent records that reference older intent records as source material, so repeated or closely related intent can be agglomerated into a newer stronger record without losing provenance.] (Spirit Principle audg3)

[Intent should be refreshed by agglomeration: combine many lower-certainty records into a single fresh higher-certainty record; older agglomerated records retire under the explicit-supersession discipline.] (Spirit Principle 1zd6)

[Spirit records should distinguish certainty from weight: certainty is confidence, weight is accumulated importance/reinforcement, especially for composite records derived from multiple sources.] (Spirit Principle 6vsl)

[lojix should be built on the triad engine and schema substrate now that those are stabilizing, the same schema-derived component shape the other components are converging on, rather than remaining a hand-written hack.] (Spirit Decision 4sff)

[Do work properly or not at all — no half-assed slop, no underspecified or wrong-shaped dispatch that produces garbage.] (Spirit Correction 157dwrve)

## Thread A — the stack rewrite (detail in `1-stack-rewrite-study.md`)

The triad-engine architecture is **sound and already enforced by the type
system**: schema-rust-next emits `SignalEngine` / `NexusEngine` / `SemaEngine`
traits whose plane-envelope signatures make a cross-engine call a *compile
error*, and the spirit pilot ships a `compile_fail` doctest proving it. What is
not yet built is the generic **runner** (`TriadComponent::serve()`, ratified
1574/1581) — until it lands, each daemon hand-writes its accept loop + transport.

- **lojix adoption is small and mechanical.** The `horizon-leaner-shape` branch
  already uses sema-engine (correct DB boundary) and signal-core (correct wire);
  it only hand-writes Kameo actor supervision instead of the generated engines.
  Adoption = author one `.schema`, implement three trait impls, delete the
  hand-written choreography. `(Spirit Decision 4sff)` is well-founded and cheap.
- **horizon-rs is correctly a library, not a component.** It reads cluster
  proposals and emits views (NodeDomain, LAN CIDRs). The "hack" in `(Spirit
  Clarification 4v45)` is the in-process library pattern, not a triad violation —
  so it does **not** mean "make horizon a component." Worth confirming.
- The pilot's one real defect is the sema-engine boundary (raw redb in Store,
  bead `primary-w42y`) — the same finding as reports 63 / 501.

## Thread B — the intent architecture redesign (detail in `3-…redesign.md`)

**Current shape (verified):** deployed `Entry` (signal-persona-spirit
lib.rs:511-518) is one flat 5-field positional record — `topics, kind,
description, certainty, privacy` — every record carrying all five; privacy is an
optional decode tail defaulting to `Zero`. `RecordIdentifier` is already a
random-minted 96-bit base36 value — the hash identity the composite move needs
already exists in v0.5.0.

**The redesign, in one move:** the flat record becomes a **per-kind variant
enum** (the kind IS the variant tag), so each kind carries only its relevant
fields:

- `Decision / Principle / Correction / Clarification / Constraint` carry a public
  body with **no privacy field** (the `3awz` move).
- A private variant carries the privacy field — privacy lives *only* there.
- A **Composite** record carries `source_records: Vec<RecordIdentifier>` — the
  hashes it fuses (`audg3`).
- Common to all: topics, description, certainty, **weight**.

**weight** (agent 3's recommendation): the same `Magnitude` ladder on a second
axis (not an integer count), so the contract stays all-qualitative and queries
stay uniform; a composite's weight compounds "one rung above its strongest
source, saturating at Maximum"; non-composite default low.

**archive** (the `73t3` streamlining): one unified `ArchivedRecord { identifier,
full-body+timestamp, retired_by }` where `retired_by = RemovalCandidate |
Composite(RecordIdentifier)`. Bidirectional provenance: the composite points
forward to its sources, each archived source points back to its composite. This
replaces today's summary-only ad-hoc archive dump.

**Two relations, not one** (agent 2's load-bearing guardrail): agglomeration
needs `AgglomeratedFrom` (sources genuinely say the same thing → fuse + archive)
kept **distinct** from `Supersedes` (this replaced that → keep lineage visible).
The corpus contains a real trap — the removal-candidate cluster *looks* like 8
duplicates but is a supersession chain that **flipped** mid-design; naive fusion
would re-admit rejected wording. Similarity is not equivalence. This is exactly
the danger the psyche named ("it's a bit dangerous").

## The agglomeration demonstration (detail in `2-…agglomeration-study.md`)

A live read-only pass proposed ~9 composites over ~45 source records across 6
clusters (drafted as NOTA, nothing removed). The bloat is concentrated in the
reporting / recency / certainty / citation bands; the big topics (`schema` 427,
`nota` 150) are deep-but-distinct, not duplicative — so agglomeration targets the
bloat bands, not the big counts. Working-orders mis-logged as intent are
**removal** candidates, not agglomeration candidates.

## Build target + discipline

Per agent 3: **prototype in the schema-derived `spirit/` pilot** (`spirit/schema/
lib.schema`) on a feature branch — that is where Spirit is being rebuilt anyway —
**not** the deployed v0.5.0 contract. The redesign is a breaking contract change:
schema version **5 → 6**, which per the workspace major-version rule **requires
explicit psyche authorization**. Cutover later via the existing version-handover
migration machinery.

Per `(Spirit Correction 157dwrve)`: the design is concrete first; the
feature-branch implementation happens only after the psyche answers the forks and
authorizes the version bump — not as a blind dispatch.

## The four forks for the psyche

1. **Composite shape** — its own `Composite` variant (simplest, but loses the
   fused intent's original kind), or a wrapper that preserves kind (a composite
   *Decision* / composite *Principle*). Lean: preserve kind.
2. **weight type** — `Magnitude` ladder on a second axis (uniform queries) vs an
   integer count of fused sources (literal "composed of many"). Lean: Magnitude.
3. **Agglomeration trigger** — always agent-proposes / psyche-confirms (same
   authority as supersession) vs auto-fuse on a similarity threshold with
   after-the-fact review. Lean: propose-confirm, given the flip trap.
4. **Build + version bump** — prototype in the schema-derived spirit pilot at
   version 6 on a feature branch (needs your authorization for the breaking
   bump), or hold at design-only.

## Follow-on (not done this session)

- `skills/intent-log.md`, `skills/spirit-cli.md`, `skills/intent-maintenance.md`
  document the now-wrong flat v0.4.2 shape — refresh once the new shape lands.
- `skills/intent-maintenance.md` gains the agglomeration section (manifestation
  of `audg3` / `1zd6`) — lands with the design, not as new intent.

## See also

- `1-stack-rewrite-study.md` — triad/schema substrate, lojix/horizon adoption.
- `2-intent-corpus-agglomeration-study.md` — the proposed composites + the flip trap.
- `3-spirit-record-architecture-redesign.md` — the full schema/Rust types, migration table, ordered implementer edit list.
- `0-frame-and-method.md` — the frame.
