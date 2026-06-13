---
title: 614 — Refresh — intent-maintenance + Spirit corpus governance history
role: designer
variant: Refresh
date: 2026-06-13
topics: [intent, intent-maintenance, spirit, corpus, context-maintenance, tombstone, supersession, hygiene, salvage]
description: |
  Agglomerated landing witness for the intent-maintenance and report-GC arc that
  ran BEFORE the 2026-06-12 full corpus rebuild. Merges designer 525, 549, 552/*,
  560 (the audit), 560 (the removed-records archive), 561, 576. Each was a
  point-in-time sweep of the OLD pre-rebuild Spirit store or the report tree;
  their substance is either executed (the GC happened, the removals happened) or
  rendered moot by the full corpus rebuild (designer 600/611), which re-domained
  and culled the entire store from scratch with its own fresh on-disk backups.
  The durable DISCIPLINE lives permanently in skills/intent-maintenance.md +
  skills/context-maintenance.md. This Refresh records the history and points at
  the live recovery surface; the sources retire.
---

# 614 — Refresh — intent-maintenance + corpus governance history

Landing witness for the pre-rebuild intent-maintenance arc. The 7 source reports it
merges are deleted in the same commit; git history holds them. Their substance is
executed or superseded by the full corpus rebuild — this Refresh records what
happened and where recovery lives now.

## Why these retire

Every report here operated on a store or report-tree state that no longer exists:

- **The OLD pre-rebuild Spirit corpus** (designer 525, 560-audit, 560-archive, 561,
  552) was the 1410-record store as it stood before the guardian existed. The
  **2026-06-12 full corpus rebuild** (designer 600, summarized in 611 §6)
  re-domained, dedup'd, and re-derived certainty across the *entire* store from
  scratch — 83 removed, 1325 survivors re-tagged. The old tombstone archives and
  rewrite-shortlists describe a store that was wholly replaced. The current,
  authoritative recovery surface is **`~/spirit-backups/pre-rebuild/`** (the binary
  store, the guardian journal, every original record as NOTA, the 83-removal
  manifest) — not these reports.
- **The report-tree GC passes** (designer 549, 576) executed their drops/
  agglomerations. They were landing-witness ledgers for sweeps now baseline; per
  `skills/context-maintenance.md` §"Keeping successor-superseded ledgers", once a
  newer sweep reissues the live handoffs they are stale. This very Refresh is the
  newer sweep.

## What the arc established (the durable discipline — already permanent)

The intent-maintenance and corpus-governance discipline these sweeps exercised now
lives in the skills layer, not in reports:

- **Capture-before-remove** — every removed record gets a tombstone with provenance
  before deletion, so nothing is lost and any genuine kernel can be re-recorded
  cleanly. (designer 525, 560-archive practiced it; the rule is
  `skills/intent-maintenance.md`.)
- **The gate test for pollution** — *does the statement survive the erasure of its
  task, or is it a working-instruction / status / agent-conclusion wearing the intent
  costume?* The 560 audit classified all ~1706 records this way (79% durable, 11%
  scratchpad, 10% borderline). The test is now in `AGENTS.md` §"Run the Spirit gate"
  and `skills/intent-log.md`.
- **Intent removal is psyche-gated** (record `1496`/`q33z`) — context-maintenance may
  name clear contradictions and propose removals, but deletion stays psyche-authorized.
- **Legacy-NOTA salvage** (designer 552, the ten-finder `intent/*.nota` audit) —
  cross-deduped the legacy intent files against the live store for deletion-readiness;
  that salvage informed the rebuild's source corpus.
- **Report GC discipline** — drop/forward/migrate/keep with a landing gate; meta-report
  directories retire as session units (designer 549 retired 8 session dirs; 576 ran
  cross-lane). The discipline is `skills/context-maintenance.md`, which this very pass
  applies.

## Residual

Nothing actionable carries forward. The corpus is rebuilt and live; the recovery
surface is on disk; the discipline is in skills. The ongoing intent-maintenance work
is now the **guardian** doing it continuously at admission time, plus the planned
**auditor** lane (designer 611 §8) — not manual sweep reports.
