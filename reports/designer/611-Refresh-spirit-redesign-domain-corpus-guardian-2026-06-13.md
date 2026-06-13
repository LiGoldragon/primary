---
title: 611 — Refresh — Spirit redesign: domain vocabulary, corpus rebuild, guardian design (landed + deployed)
role: designer
variant: Refresh
date: 2026-06-13
topics: [spirit, intent, guardian, domain, vocabulary, referent, corpus-rebuild, category, taxonomy, two-layer, deployment]
description: |
  Agglomerated current-state surface for the Spirit intent-tool redesign arc —
  the work that took deployed Spirit from v0.4.0 (a flat, capped, ever-growing
  topics store) to the live nested-domain, guardian-gated store rebuilt and
  re-domained on disk. Merges designer 546, 547, 567, 577, 578, 579, 580/*,
  581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 593, 594, 595, 596,
  597, 598, 599, 600. Carries the SETTLED design (two-layer state/stream model,
  the universal domain vocabulary, the referent facet, the guardian admission
  gate) and the LANDED+DEPLOYED state (live 0.9.x: nested taxonomy migrated,
  corpus rebuilt 1410->1327, guardian gating real DeepSeek). The court-of-law
  justification redesign that BUILDS ON this guardian is the live successor arc
  (designer 601-609) and is NOT folded here — it is still in flight.
---

# 611 — Refresh — Spirit redesign: domain, corpus, guardian (landed + deployed)

This Refresh is the landing witness for the Spirit-redesign arc. The 26 source
reports it merges are deleted in the same commit; git history holds them. It reads
as current state. The **court-of-law justification upgrade** (designer 601, 603,
604, 605, 606, 607, 608, 609) is the live successor that builds on the guardian
described here — it stays as separate active reports, not folded in. The
**current incident** (the live daemon down on a versioned-store deploy skew) is
designer 610, also kept.

## Intent Anchors

[Intent is the psyche at rest — forward, settled, declarative — not motion; Spirit's
flaw was being a pure accumulator with no resting state.]

[Spirit is for the whole world, not just me — the domain taxonomy must be universal
(apply to any human's intent), not workspace-grounded; workspace specifics belong in
the keyword/referent layer, not the top tier.]

[Domain names are self-explanatory — meaning lives in the variant name; no
gloss/annotation layer. Domain granularity tracks intent density; the tree is
variable-depth with a third tier where dense.]

[Recompile is cheap and zero-downtime is the goal — a daemon's vocabulary grows by
recompile-and-redeploy, not runtime config.]

[The guardian gates unvetted incremental writes; a bulk restore of an
already-curated corpus must not re-litigate each record (the meta-signal Import
bypass).]

## 1. The frame — what Spirit is, and the disease it had

Spirit is the typed intent store: it captures the psyche's durable intent as records
and serves them back to agents. The deployed v0.4.0 was diagnosed (designer 577,
empirical, against the running daemon) with four real problems, and crucially **no
retrieval cap** — the bloat complaint was real but mis-attributed: queries returned
everything unranked (385 records / 148 KB for a `schema` query), matching was
exact-topic-string + kind + privacy, never magnitude, never full text.

The four problems (designer 567):

1. **Unbounded growth** — the store only appends; retrieval gets noisier.
2. **Repetition should reinforce, not pile up** — restating should strengthen the
   existing record, not add a row. Certainty != weight.
3. **Deprecation** — stale/superseded intent must stop surfacing without losing
   history, and on a long horizon be physically collected.
4. **Compound records go half-stale** — the unit must be one atomic proposition.

## 2. The two-layer model (state vs stream) — the settled design

The converged design (designer 578, a live design conversation, every open call
resolved to [decided]/[deferred]):

- **Intent is a forward arrow** — generative, expanding; it states *this*, never
  *not that*. The boundary is **referential negation**: a forward law
  (`NOTA emits no quotation marks`) is still intent; a record defined *against
  another record* (a rejected alternative, a debate) is discussion.
- **State = rest, stream = motion.** The store holds pure forward arrows, always
  mutually consistent — no lineage, no contradiction, no correction records.
  Change (supersession, clarification) is a transient event on a subscription
  stream that announces itself and evaporates. "This replaced that" lives exactly
  as long as the notification.
- **Authority hierarchy**: live psyche > intent > everything else (reports, code,
  architecture). Intent is a *derived model* of the psyche and is correctable by
  the live psyche.

The guardian is what makes "query at any instant and get a coherent,
contradiction-free body" true by construction — it won't admit anything that breaks
consistency.

## 3. The domain vocabulary — universal, single-noun, two-tier

The settled vocabulary (designer 583 researched it from knowledge-organization
literature; 584 made the names single nouns and added the referent facet; 587
expanded the Software branch; the psyche correction "Spirit is for the whole world"
in 582 inverted the original workspace-grounded premise).

The shape (designer 584, the canonical vocabulary file):

- **`area`** = ~24 broad groupings (`health`, `craft`, `knowledge`, `nature`,
  `technology`, …). **Never tagged on a record** — they organize the vocabulary and
  give the enlargement gate a ~12-sibling neighborhood to dedup within. Near-frozen.
- **`domain`** = the unit a record tags. ~293 of them, each a single grounded noun
  (`architecture`, `schema`, `agriculture`, `prayer`, `notation`). Multi-word atoms
  are **camelCase** per the NOTA idiom (`firstAid`, `jobSearch`, `recordKeeping`),
  mirroring PascalCase for type variants. No `copyright`/IP domain (psyche: IP isn't
  legitimate property).
- A third tier exists **where density warrants** (designer 587): `Software` became a
  dedicated top-level area (`Software(Cluster(Leaf))`, ~202 universal subjects from
  SWEBOK v4 + ACM CCS), and the Software work later **nested under `Technology`** as
  the settled structural is-a (designer 590): `Technology = Hardware + Software`.

Cross-domain links are **symmetric equivalence only** (designer 590) — subsumption
was dropped. Two equivalences shipped: `Networking`, `DatabaseSystems`. The
vocabulary moved to a first-class **taxonomy schema** (`schema/domain.schema`), a
reusable schema kind.

## 4. The `referent` facet — which-one, not about-what

`domain` answers *about-what* (universal, shared); **`referent`** answers *which-one*
(particular, from one person's own inventory) — a repo, a field, a child, a
marriage. The cross-product is the point: "spirit's architecture should be
schema-first" is `domain=architecture, referent=spirit`.

Key design call (designer 584): **`Referent` is a runtime registry reference, NOT a
schema enum.** Three reasons it diverges from `Domain`: (1) privacy — referents are
private particulars and the schema is a shared public compiled contract; (2) it's
data, not type — you don't bake instances into the type system; (3) frequency — new
repos/projects are registered constantly, so recompile-per-referent is absurd
(the "recompile is trivial" principle was about *rare, deliberate vocabulary*
changes). Referents are registered via a synonym-gated `RegisterReferent` write so
"20 spellings of spirit" can't accumulate. `Entry` gained an optional
`Referents(Vec<Referent>)`. A `ReferentSelection` on `Query` makes "show every intent
governing `spirit`" first-class.

## 5. The guardian — the admission gate

The guardian is the daemon's admission gate: *can this proposed forward-intent arrow
enter a store that stays mutually consistent at rest?* (designer 567 design, 585
end-to-end overview, 581/582 quality audits).

- **Binary verdict** — `Accept`, or `Reject` with a typed reason and the record
  references that justify it. No discretion, no rewriting, no confidence score.
- **The model checks everything** (psyche decision) — a single locus of judgment.
  Consistency, duplicate, trample, non-intent, compound are all the model's; only
  pure structural admission (parseable, non-empty NOTA) stays upstream as input
  validation. The deterministic duplicate check folds *into* the verdict: model
  returns `Reject Duplicate`, daemon bumps importance as a mechanical consequence.
- Because judgment rests entirely on the model, three things are non-negotiable:
  **complete relevance-scoped retrieval** (the model can only catch what it's shown —
  category-only retrieval is a *correctness* bug), **temperature 0**, and a
  fully-specified prompt.

The load-bearing quality opinion (designer 585): the guardian's weakness is **not the
model** — it's three fixable things upstream. The gate covered only one of four write
paths; the retrieval bundle was wrong; the prompt was under-specified. The
retrieval-bundle fix is **relevance-scoping**, not a fixed count cap (designer 593
corrected 585 here): drop the same-`Kind` +1 floor that admitted a fifth of the store
on no real relevance; a count cap can silently drop a genuine duplicate ranked 65th
(a wrong accept). The gate must cover **every write that changes the live arrow set**
(at minimum `Propose`, `Clarify`, `Supersede`) — `Supersede` writing its replacement
blind was the sharpest hole.

## 6. What is LIVE — the deployment + the corpus rebuild

The redesign shipped. Two milestones:

**The nested-taxonomy deploy (live 0.9.0, designer 593 audit against the running
daemon):** the full redesign is live and faithful. The whole 1407-record store was
re-encoded through the new nested vocabulary — former-`Craft(Architecture)` records
correctly re-tagged to `Technology(Software(Engineering SoftwareArchitecture))`, zero
loss. Guardian gating runs real DeepSeek end-to-end (accept + reject both verified
live). Scope prefix-matching works at any depth.

**The corpus rebuild (live 0.9.3, designer 600 — executed autonomously, psyche
authorized "go all the way"):** the store grew to 1410 records *before the guardian
existed*, so the corpus carried what the guardian now rejects on sight — duplicates,
stale arrows, non-intent, ~1100 records mis-filed in the `(Information
Documentation)` catch-all. The rebuild re-domained every record and dedup/culled:

| Metric | Before | After rebuild |
|---|---|---|
| Total records | 1410 | 1327 |
| `Technology` | 13 | 1183 |
| `(Information Documentation)` catch-all | 1100 | 18 |
| Certainty = Maximum (reflexive) | many | 7 |
| Certainty = Medium | ~0 | 781 |

83 records removed (46 duplicates merged, 26 superseded, 11 non-intent dropped),
1325 survivors re-domained + certainty re-derived, **nothing lost silently** — full
manifest + binary backup at `~/spirit-backups/pre-rebuild/`, cutover reversible. The
**meta-signal `Import`** feature (live 0.9.5, the privileged owner-only bypass that
writes pre-vetted records straight to the SEMA store, the general restore/migrate
path) and the **`meta-spirit` CLI** (owner-only privileged sibling of `spirit`)
landed to support it — the two-CLI split is the first instance of the component
two-client pattern (designer 599: every component exposes `<component>` + working
signal and `meta-<component>` + meta policy signal; library holds 100% of the logic,
generation supplies the per-component binding).

## 7. Residual open items (carried forward)

- **Certainty re-derivation** — 781 records now Medium, 7 Maximum. The shape wants a
  psyche sanity-check (designer 600 §"For your review").
- **The 83 removals + 3 reassigned area-only records** — ratifiable ledger in the
  manifest; psyche may pull any back.
- **0.9.5 deploy** — the rebuilt corpus is served by the deployed 0.9.3 daemon; the
  0.9.5 binary (with Import) was built but not yet redeployed at the time of 600 (a
  broad-blast-radius home-manager activation held for attention). The court-guardian
  work (designer 609) deployed past this to 0.11.x — see the active arc.
- **The forgetting-well / lifecycle ladder** (nominate/tombstone/archive/collect/
  compact/purge) and the **subscription stream** for live correction events remain
  designed-not-fully-built (designer 567 §3, 578 §3).

## 8. Where this connects

The guardian described here is the substrate for the **court-of-law justification
upgrade** — designer 603 (intent-capture protocol), 604 (court-of-law design), 605
(implementation spec), 606 (doubts), 607 (lean Phase-1 spec), 608 (prompt spec +
example library), 609 (built + deployed 0.11.x). Those reports are the active
successor and stay. Designer 601 (guardian-effect simulation: merge-with-importance +
split, proposing 1328->1202) and 602 (the could->should modality catch) are the
bridge between this arc and that one — kept as live design input.
