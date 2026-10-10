---
title: 549 — Deep context-maintenance pass
role: designer
variant: Review
date: 2026-06-07
topics: [context-maintenance, intent, reports, skills, workspace, supersession, hygiene]
description: |
  Deep context-maintenance pass across the workspace agent-context surfaces.
  APPLIED in-lane: reports/designer GC (39 -> 13, toward the 12 soft cap),
  11+5 doc/skill staleness edits (the spirit-next -> spirit rename, the removed
  Asschema concept, dead lowercase repo paths), and removal of 7 stale
  orchestrate locks. SURFACED for authorization (intent removal is psyche-gated
  per record 1496): 17 Spirit supersession proposals (clear cases) + 3
  transcription fixes. HANDED OFF to operator: code-repo INTENT.md/ARCHITECTURE.md
  drift in 6 files (the persona- component-prefix rename that did not propagate +
  dead report citations). Intent sweep was a clear-cases pass, not exhaustive.
---

# 549 — Deep context-maintenance pass

A workspace-wide context-maintenance pass (4-agent discovery → in-lane apply + gated proposals). Method: read-only discovery against every agent-context surface, then apply what is in-lane and non-destructive, and surface what is psyche-gated (Spirit removals, per record `1496` — context-maintenance may name clear contradictions but deletion stays authorized) or out-of-lane (code-repo main, which the operator owns).

## Applied this pass (in-lane, non-destructive)

- **reports/designer GC: 39 → 13.** Deleted 26 reports whose substance is already homed (in skills/ARCHITECTURE/landed code) or superseded by a newer report — the git history holds every deletion (`jj show <change>:reports/designer/<name>`). The 8 meta-report session directories (495/498/500/501/502/516/532/533) retired as session units. Kept the 13 still-load-bearing: 525, 526, 527, 528, 536, 537, 541, 543, 544, 545, 546, 547, 548 (this pass adds 549 → 14, just over the soft cap of 12; 528 and 536/537 are flagged to retire once the operator lands the migration and spirit/schema-rust-next `ARCHITECTURE.md` absorbs the PlaneType design + corrected ground-truth, which would bring it to ~11).
- **12 doc/skill staleness edits.** The dominant theme was the `spirit-next` → `spirit` repo rename not propagating (the repo is canonically `spirit` now; `spirit-next` was its temporary name) — fixed in `skills/component-triad.md` (×4 incl. a historical commit citation), `skills/reporting.md`, `skills/naming.md`, and `INTENT.md` (×5). Plus the removed-Asschema concept (`vez8`, Maximum): dropped the dead `asschema` topic from `skills/spirit-cli.md`'s example query and rewrote `skills/designer.md`'s two `.asschema` durable-artifact teaching examples to the schema-in-Rust artifact. Plus two dead lowercase `ligoldragon/...` repo paths in `RECENT-REPOSITORIES.md` → `LiGoldragon/...`.
- **Removed 7 stale orchestrate locks** (empty, May mtimes, gitignored local cruft): the six retired `-assistant`-suffix locks (the suffix is retired per Spirit `920`) + the orphan `primary-ngn8.lock`. All current-lane locks kept.

## Intent supersession proposals — for your authorization

Spirit removal is destructive and psyche-gated (record `1496`); I executed nothing. These are the **clear-cases** found (a clear-cases pass over ~1904 records, NOT exhaustive — see Coverage). On your go I'll tombstone-capture each (full text + provenance into this report) then remove, or lower to `Zero` for the recoverable `CollectRemovalCandidates` path.

### The removed-Asschema cluster (superseded by `vez8`, Maximum — "there is NO separate assemble/Asschema step")

These records describe the removed assembled-schema/Asschema IR as a live target. `vez8` (Decision, Maximum, 06-05) + `fc7l` (VeryHigh, remove the compatibility surface) supersede them; `protocols/active-repositories.md` already documents the removal. Propose zero-nomination: `h053`, `fv2a`, `2in8`, `5mbd`, `9ptu`, `yuku` (Asschema/AsschemaArtifact as named typed objects), and the cleanup working-orders `cupj` (pinned to dead numeric report 254), `mnl1`, `0zci` (erase-from-reports orders, already executed).

### The abandoned at-binder cluster (superseded by `own9`, "the ENTIRE at-binder surface is ABANDONED")

`n2z3` (the at-binder authored-declaration surface) — `own9` (Correction, 06-06) supersedes it *wholesale*; `n2z3` is **already at certainty `Zero`** (already nominated). `7m84` (pipe-form declaration guidance) is likewise superseded by `own9`'s positional-form direction (it also straddles the Asschema cluster). Propose remove `n2z3`; zero-nominate `7m84`.

### Privacy named-tier (superseded by `k5y3`, the Magnitude-axis decision)

`8ll8` (the four named tiers Open/Personal/Sensitive/Sealed, Low) and the deferred-candidate-set part of `0gxx` — `k5y3` (Decision, High, recorded 6 minutes after `8ll8`) explicitly rejects the audience-register enum in favor of reusing the existing `Magnitude` ladder on a privacy axis. Propose zero-nomination of both.

### Mis-logged working orders (not durable intent)

`sybk` and `uyon` — first-person task-kickoff announcements ("I am the designer-assistant subagent…", "Creating a design-nota-from-schema repo") for a repo that is **verified deleted**; both use the retired `designer-assistant` suffix and dead numeric IDs. These are working orders that died when the task ended (not intent). Propose remove.

## Transcription fixes — proposed (also intent-layer, gated)

Non-superseding corrections (an agent may fix transcription, but since the deployed Spirit has no in-place edit op these need a `Correction` record or Remove+re-record, so I'm surfacing rather than executing):

- **`qtbd`** (VeryHigh) bundles a still-valid decision (96-bit CSPRNG, base36 shortest-unique-prefix identity) with a **wrong number** — it says "minimum THREE characters" but `tw81`/`rh29`/`3w61` (same day) corrected it to FOUR (`tw81` explicitly "Refines the prior minimum-three scheme"). Fix: record a `Correction` keeping the CSPRNG/base36 decision and stating the four-char minimum; do NOT remove (the core decision is valid). `y5m9` carries the same three-char drift and is otherwise nearly duplicated by the corrected records → zero-nominate.
- **`h3u7`** — a dense run-on bundling many sub-decisions with an embedded open file-extension question; a cleanup `Correction` could split it. Low priority.

## Code-repo INTENT.md / ARCHITECTURE.md drift — operator handoff

Code-repo main is operator-owned, so these are proposals for the operator (the dominant theme is the `persona-` component-prefix rename — `persona-mind`/`persona-router`/`persona-harness`/`persona-system`/`persona-orchestrate` and `signal-persona-*` — that did not propagate to the older docs; those prefixed repos no longer exist on disk, the bare forms do):

- **`persona/ARCHITECTURE.md`** + **`mind/ARCHITECTURE.md`** (both May 25, the worst) — pervasive `persona-`-prefixed names; both also treat the **retired** `signal-persona` shim as live. Rename to the bare forms; repoint to `owner-signal-persona` + `signal-engine-management`.
- **`orchestrate/INTENT.md`** + **`orchestrate/ARCHITECTURE.md`** — stale `persona-mind` (incl. a mermaid node + authority-table row) + a broken see-also path.
- **`persona/INTENT.md`** — see-also points at the retired `signal-persona`.
- **`message/ARCHITECTURE.md`** — the operator's message fix is half-done (INTENT.md cleaned, ARCHITECTURE.md still says `persona-router` in 6 places incl. the mermaid diagram).
- Cross-cutting: `persona/` + `orchestrate/` docs cite **dead retired reports** (`designer/322`, `designer/324`, `designer/326`, `operator/174`).

Reconciled/clean (no action — verified accurate to landed reality): triad-runtime (both files), `message/INTENT.md`, schema-next, schema-rust-next, spirit, router, sema-engine, nota-next.

## Coverage + follow-ups

- The intent sweep was a **clear-cases pass**, not exhaustive: it covered schema, spirit, nota, signal, triad, engine, identity, workspace, privacy, asschema, at-binder, owner-signal. **Not swept** (a follow-up pass should cover): persona, mind, router, criome, cloud, lojix, sema-engine, reporting, orchestrate, roles, beads, and many design-detail topics.
- Most live records carry inline dead numeric-era citations (record 371, 933/940, 902, etc.) that do **not** by themselves make a record stale — these were deliberately NOT mass-rewritten (high-churn, low-value, risky); date-stamped numeric attributions are accepted as valid.
- `RECENT-REPOSITORIES.md` has systemic drift (still lists the old `persona-*`-prefixed repos, all missing on disk; `gascity`/`gascity-nix` gone) — it is an explicitly churning checkout index overdue for a full re-prune rather than itemized row edits; flagged for its owner to re-prune.
- After the operator lands the component migration and ARCH absorbs the PlaneType design, reports 528/536/537 retire (subdir → ~11).
