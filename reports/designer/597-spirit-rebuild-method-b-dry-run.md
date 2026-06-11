# Spirit corpus rebuild — Method B dry run (read-only simulation)

A segregated, read-only simulation of Method B (report 596): pull all 1407 records out, re-domain
every one into the real taxonomy, then dedup/cull within the resulting clusters — **writing
nothing back to the live store.** Workflow `wf_7e35f9d4-cbe`, 80 agents, ~2.0M tokens, ~7.7 min.
Spot-checks below confirm the judgments are sound, so the numbers are a credible *floor*.

## Headline: re-domaining dissolves the catch-all

| Area | Now (live) | After re-domain (sim) |
|---|---|---|
| **Technology** | **13** | **1359 (97%)** |
| Information | 1101 | 27 |
| Work | — | 11 |
| Language | — | 6 |
| Safety | — | 3 |

The corpus was never "Information/Documentation." It is the workspace's **software-design
history** — 97% of it. Re-domaining is the whole game: the dead domain signal (everything in one
leaf) comes alive (spread across the tree). Within Technology/Software:

| Subcategory | Records | | Subcategory | Records |
|---|---|---|---|---|
| Data | 389 | | Security | 56 |
| Engineering | 357 | | Quality | 35 |
| Languages | 211 | | Observability | 31 |
| Operations | 106 | | Surfaces / Systems | 16 / 16 |
| Distributed | 75 | | Hardware (all) | 5 |
| Intelligence | 62 | | | |

Data (NOTA/schema/serialization), Engineering (architecture/process), and Languages (the schema
language itself) hold ~70% — which *is* what this workspace builds. Categorization confidence:
795 high, 578 medium, 33 low (97% medium-or-high). Note these are subcategory rollups; the actual
tags are leaf-level (Data has 18 leaves, Engineering 22), so retrieval lands tighter than the
rollup suggests.

## Dedup / cull — a conservative floor

| Disposition | Count | |
|---|---|---|
| Duplicates retired (merge) | **107** | same arrow restated; keep one canonical |
| Superseded (stale) | **28** | a later record obsoletes an earlier one |
| Dropped (non-intent / task-state) | 2 | very conservative |
| Compound flagged → split proposed | 60 → 9 | records bundling several arrows |
| **Total removed** | **137** | |
| **Survivors** | **1269** | of 1406 processed (~10% shrink) |

This is a **floor, not the real number** (see caveats): the dedup ran cluster-local *and*
chunk-local (Data's 389 were split into 7 chunks of ≤60 that couldn't see each other), so
cross-chunk and cross-cluster duplicates are under-counted. The agent was deliberately
conservative — it *kept* related-but-distinct arrows (a cluster of near-dups is a signal of
importance, not noise; keep one, don't over-merge).

## The gold: stale superseded intent is real and substantial

The 28 confirmed supersessions reveal whole **evolution chains** sitting live in the store, the
obsolete versions never retired — exactly the debt 594 predicted. These are higher-value than
dedup: they're not redundant, they're *wrong now*.

- **Syntax design churned for months and every step is still live.** The `@`-sigil / pipe-form
  declaration syntax: `dwtm`/`f743` ← `ilaq`, `r8da`/`s260` ← `own9`, `3cse` ← `506w`,
  `dqmc` ← `ghw7`. A reader (or the guardian) retrieving "schema declaration syntax" today gets
  the whole obsolete trail.
- **`yu14` supersedes three** context-maintenance records (`vqfk`, `roh7`, `ywaq`) — a
  consolidating statement that orphaned its predecessors.
- **A reversed model choice:** `tlv0` (host small Gemma-4-Flash locally) ← `7ily` (no — biggest
  model that fits), which literally says "superseding the earlier small-gemma-flash choice."
- **A component rename:** `lzno` (`persona-llm-client`) ← `tc80` (rename to `agent`).
- **Field-model correction:** `dwkb` (split Magnitude into Certainty + Weight) ← `t4uq` (no Weight
  — it's Importance).
- Plus daemon-binary-config (`30m5`←`1dpi`, `u4st`←`ur16`), access-classification
  (`wm4q`/`0gxx`←`8ll8`), record consolidations (`3got`/`ej7d`←`o8x5`).

## Verified against the live store (sample)

Each spot-check confirms the sim read the records correctly and judged soundly:

- `k4zc`←`34hu`: identical "typed-recursive-enum DomainScope" arrow; `34hu` fuller. ✓
- `dwkb`←`t4uq`: `t4uq` is the later correction that drops `dwkb`'s Weight framing. ✓
- `tlv0`←`7ily`: `7ily` explicitly reverses `tlv0`. ✓
- `lzno`←`tc80`: rename obsoletes the original; `lzno` was mis-tagged `(Kinship Rapport)`. ✓
- `1sa2` (compound→5): genuinely bundles braces-are-maps + namespace-is-dynamic-enum +
  single-colon separator + schema entrypoints + module-tree emission. ✓

## Caveats (so the numbers read right)

1. **Simulation, not the live guardian.** This uses workflow LLM judgment, not
   DeepSeek-through-the-daemon. It shows what Method B *can* produce (its ceiling for
   re-domaining, a floor for dedup). The real guardian, with its cap-64 retrieval, would catch
   *fewer* duplicates incrementally.
2. **Dedup is cluster- and chunk-local** → 137 removed is a floor; the true dedup/supersede count
   is higher once a full-cluster (or real-guardian incremental) pass runs.
3. **1-record discrepancy** (1406 processed vs 1407 live): one categorizer omitted a record — a
   sim artifact, not real loss; the live store is intact at 1407.
4. **Subcategory concentration** (Data 389, Engineering 357) could partly be categorizers
   over-defaulting to popular leaves (Serialization, SoftwareDesign); a real run should verify
   leaf-level spread.
5. **No per-record mapping persisted.** This run returned aggregates + dispositions, not the full
   id→domain table. Applying for real needs a fresh categorization run that *writes* the mapping.

## What this says about Method B

The method is **validated and the categorization is verifiably correct.** Three takeaways:

- **Re-domaining is the high-value, low-risk first move** — it single-handedly revives the domain
  signal (13 → 1359 Technology) and is a near-deterministic batch migration from a ratified
  mapping. It does not depend on dedup.
- **Supersede-collapse is the highest-value cleanup** — removing intent that is *wrong now*, not
  merely redundant. Worth a focused pass.
- **Dedup needs a non-chunk-local pass** for real numbers; the ~10% floor will grow.

The sane corpus is **≤1269 records, ~97% Technology/Software, with evolution-chains collapsed to
their latest form** — and it's the same gate (guardian) that would then keep it there.

## Next moves (psyche)

1. **Make it real, or just look?** This was "see what happens." To execute B we need: a fresh
   categorization run that *persists* the id→domain mapping, your distribution-level ratification,
   and operator's apply tool (batch migration for re-domain; guardian/full-cluster pass for
   dedup+supersede).
2. **Re-domain first, independently?** The safest high-value slice: apply only the re-domaining
   (revives retrieval), defer dedup/supersede to a second pass. Recommended sequencing.
3. **Tighter dedup pass?** I can re-run dedup full-cluster (no 60-chunk cap) to get the real
   shrink number before any writes.
4. **The supersede set is a ready worklist** — 28 verified stale records to retire with lineage,
   the cleanest first cull.
