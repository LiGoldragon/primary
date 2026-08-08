---
title: 552/10 — Legacy intent salvage — small cluster B mining
role: designer
variant: Audit
date: 2026-06-07
topics: [intent, spirit, legacy-nota, nix, jj, markdown, intent-log, nota-mixed-enum, deletion-readiness]
description: |
  Mining of the five small legacy intent files (nix, jj, markdown, intent-log,
  nota-mixed-enum-support — 14 records total) for at-risk core design intent.
  One genuine salvage candidate surfaced (the Nix-is-bootstrap design posture);
  everything else is already preserved, superseded, or too task-specific.
---

# 552/10 — Legacy intent salvage — small cluster B

## Scope

Five legacy files, 14 records scanned: `nix.nota` (3), `jj.nota` (2),
`markdown.nota` (1), `intent-log.nota` (1), `nota-mixed-enum-support.nota` (7).
One genuine salvage candidate; 13 records dropped as preserved, superseded, or
too task-specific.

## Salvage candidates

### Candidate 1 — Nix is bootstrap infrastructure; design as if it gets replaced

**Kind:** Principle (the legacy record is logged Decision, but the durable core
that survives is a design-posture *principle*).

**Proposed topics:** `nix forge bootstrap-infrastructure design-posture beauty-asymmetry horizon`

**Proposed description:**
Nix code is bootstrap infrastructure, not a long-term home — Forge (the
psyche's future better builder system, a concept only for now) is the intended
destination that replaces Nix's build infrastructure. The design posture that
flows from this: design choices that hinge on Nix permanence are wrong; design
AS IF Nix gets replaced. Corollary — the beauty/cleanliness investment is
asymmetric: keep horizon (and the typed cluster-data model) clean because it
OUTLIVES Nix, and tolerate ugly constants living in the Nix code because the
Nix layer is going away. This is the upstream WHY behind the typed-source-first
and horizon-stays-clean disciplines; it is distinct from forge's own
implementation intent (what forge does), which is already captured in
forge/ARCHITECTURE.md.

**Proposed certainty:** Medium. The legacy record is logged Maximum, but it is
explicitly direction-only and deferred ("just a concept for now... not
something I'm going to address right now"). The durable design *posture* it
licenses is solid, but the Forge concept itself is speculative, so Medium is the
honest certainty for the surviving principle (matching the Medium certainty of
the related forge records z5aw / m937 already in Spirit).

**Supporting verbatim (legacy):**
> The Nixcode is more, I see it more as a thing that we will eventually move on
> from when we implement Forge, which is our answer to Nix. An actual better
> builder system than Nix can ever become, which is just a concept for now...
> So for me, the Nixcode is something we bootstrap on, but eventually move on
> from.

Plus the summary's corollary: *"keep horizon clean because horizon outlives
Nix; keep ugly constants in Nix because Nix is going away."*

**Preservation evidence (why it is at risk):**
- Spirit query `(Observe (Records ((Partial [nix forge bootstrap builder
  horizon]) ...)))` returns many nix/forge records, but the forge-specific ones
  (`z5aw` — generated Rust as content-addressed crates outside Nix, Medium;
  `m937` — Sema upgrade via Nix-backed forge path, Medium; `z5aw` again)
  capture narrow downstream *implications* of forge, not the upstream posture
  "design as if Nix is temporary / Nix is bootstrap-only."
- `rg -i 'forge|nix.*replace|move on from|nix.*bootstrap|outliv|asymmetr'`
  across ESSENCE.md / AGENTS.md / INTENT.md / skills/ found only the unrelated
  `signal-forge` repo references and the word "forget"; `skills/nix-discipline.md`
  actively frames Nix as a permanent tool ("pays back permanently"), the
  OPPOSITE of the salvage idea — so the posture is not just missing but
  contradicted by the current guidance framing.
- `forge/ARCHITECTURE.md` does state "forge is the planned replacement for
  nix's build infrastructure," but only as forge's own *status / scope*, not as
  the workspace-wide design-posture principle ("design as if Nix gets
  replaced," beauty asymmetry). `horizon-rs/INTENT.md` mentions forge migration
  in passing but carries no such posture.

**At-risk rationale:** The forge repo will keep its implementation intent, but
the upstream *design discipline* — write today's design assuming the Nix layer
is disposable, and invest cleanliness asymmetrically into the layers that
outlive it — lives ONLY in this legacy record. Deleting nix.nota erases the
stated WHY that justifies the horizon-stays-clean / Nix-can-stay-ugly tradeoff.

## Already preserved / dropped

Confirmed safe to delete — each scanned and shown to be preserved, superseded,
or non-durable:

### nix.nota
- **Records 1 & 2 (use max-jobs 0 on nix calls)** — DROPPED, too specific +
  transient. Both are session constraints scoped to "this work" / a specific
  signal-frame migration. The general remote-builder discipline is already in
  Spirit (`ot9e` — OS build tests run on remote builders with max-jobs zero;
  `jb73` — build the inference node on the remote builder, never local).
- **Record 3** — the durable half is Candidate 1; the forge-implementation half
  is preserved in `forge/ARCHITECTURE.md` and Spirit `z5aw` / `m937`.

### jj.nota
- **Record 1 (canonical commit is `jj commit -m`; `describe @` forbidden)** —
  DROPPED, preserved. AGENTS.md hard override ("jj invocations are always
  headless/inline," `jj commit -m '...'` as the primary form) and
  `skills/jj.md` already carry this.
- **Record 2 (`jj commit <paths>` for path-selective commits)** — DROPPED,
  SUPERSEDED. AGENTS.md ("Commit the WHOLE working copy — never path-scoped")
  and Spirit `r2x2` / `cjx1` now forbid path-scoped commits; recording this
  legacy clarification would re-introduce a now-banned practice.

### markdown.nota
- **Record 1 (no `---` horizontal-rule lines)** — DROPPED, preserved verbatim
  as an AGENTS.md hard override ("No `---` horizontal-rule lines in markdown").

### intent-log.nota
- **Record 1 (a question is not automatically intent)** — DROPPED, preserved.
  The AGENTS.md Spirit gate lists "**no capture** (question, tangent, task-only
  order, ...)" and `skills/intent-log.md` echoes "No capture — pure question,
  tangent, task-only order." Spirit `7hrd` reinforces (working orders are not
  intent).

### nota-mixed-enum-support.nota
- **All 7 records** — DROPPED, non-durable. Every record is a task-specific
  session order: lane assignment (record 1 "you're the second-system-assistant"),
  reading-order constraints for a specific report (records 2, 5, 7), the
  report-as-deliverable shape (record 3), an out-of-scope course-correction for
  one report (record 4), and a follow-up implementation order (record 6). None
  survives criterion 1 (the work they refer to is done; they don't guide future
  work). The one durable technical seed inside them — "NOTA should support a
  single enum mixing data-carrying and non-data-carrying variants" — is a NOTA
  feature design that belongs to the nota stack's design surface, not a
  durable psyche-intent principle, and is being tracked as implementation work
  (the vision report and its implementation order); it is not at-risk core
  *intent* that deletion would lose.
