---
title: 473 — Spirit algorithm proposals
role: designer
variant: Design
date: 2026-06-02
topics: [spirit-algorithms, intent-maintenance, dedup, supersession, magnitude-calibration, topic-vocabulary, query-before-capture, forwarded-prompt-protocol]
description: |
  Proposals for Spirit/intent-maintenance algorithms responding to psyche directive 2026-06-02 (intent maintenance is a large topic; ask questions; propose spirit algorithms). Five concrete algorithm proposals + four targeted psyche questions whose answers shape which proposals to ratify. Substance grounded in the dedup incidents this session surfaced (7 duplicates removed by 472 sweep + 5 by main-agent self-corrections) — the discipline needs algorithms not just discipline-statements. Each proposal: problem it solves, mechanism, implementation cost, trade-offs.
---

# 473 — Spirit algorithm proposals

## TL;DR

The 2026-06-02 session produced **12 Spirit duplicates** (7 swept by designer 472 + 5 by main-agent self-corrections) over ~3 hours of multi-agent design conversation. The discipline statements in `skills/intent-maintenance.md` worked correctly when applied but were not applied consistently — agents captured without querying first. The pattern suggests **discipline alone isn't enough**; spirit needs algorithms (mechanisms, protocols, defaults) that make the discipline automatic.

This report proposes five concrete algorithms + asks four psyche questions whose answers determine which to ratify.

## Section 1 — What the dedup incidents teach

Examples from this session:
- **Spirit 1366 + 1367 (mine)** duplicated operator's 1365. I captured on a forwarded prompt without querying operator's captures first.
- **Spirit 1376-1380 (mine)** duplicated operator's 1370-1375. Same failure mode, same session, 30 minutes later.
- **Spirit 1402, 1404, 1406 (operator's)** duplicated my 1400. Same substance, reverse direction.
- **Spirit 1403, 1407 (operator's)** duplicated my 1401.
- **Spirit 1397 (operator's)** duplicated my 1396.

Pattern: **multi-agent sessions on the same forwarded prompt produce duplicates by default**. Both agents see the prompt; both capture independently. The forwarded-prompts rule from `AGENTS.md` says the receiving agent should query the original-addressee's captures first and gap-fill only what's missing — but this requires a pre-flight query that isn't part of any standard protocol.

The discipline says "wait a beat, then query". The reality: agents act on the prompt's substance immediately because the captures feel urgent. The beat doesn't happen.

**Algorithms are what survive this gap** — pre-flight query as a step in the capture procedure, automatic dedup detection during maintenance, calibrated supersession vs removal.

## Section 2 — Five proposed algorithms

### Algorithm 1 — Query-before-capture protocol

**Problem**: agents capture on forwarded prompts without checking what other agents already captured. The dedup incidents above all share this failure mode.

**Mechanism**: every Spirit capture is preceded by a topic-pattern query on the substance keywords. If recent records (last 5-10) match on substance + Kind, the agent does NOT immediately capture — instead presents the existing record(s) and recommends one of three actions:
- **CONFIRM**: existing capture is canonical; don't add.
- **GAP-FILL**: existing capture missed a substantive angle; capture the angle as a sharpening reference.
- **NEW**: substance is genuinely new; capture.

**Implementation cost**: a 2-line addition to `skills/intent-log.md` capture procedure. The query is one `spirit "(Observe (Records ((Partial [topic1 topic2]) None Any Recent SummaryOnly)))"` invocation per capture.

**Trade-off**: adds latency to capture (one query before write). For high-volume sessions (12+ captures/hour), the latency compounds. Mitigation: cache the recent-record summary within a session turn; multiple captures in one turn share one query.

**My lean**: ratify. Latency is small; dedup savings are larger.

### Algorithm 2 — Dedup detection heuristic for maintenance sweeps

**Problem**: even with Algorithm 1 in place, some duplicates leak through (substance overlap with different topic words; cross-session captures). The sweep needs automatic detection.

**Mechanism**: during the `skills/intent-maintenance.md` sweep, scan recent records (last 50-100) for duplicate-substance candidates. The heuristic flags pairs where:
- Records within N (e.g., 10) IDs of each other.
- Topics overlap by ≥ 50%.
- Kind matches.
- Magnitude within ± 1 step.

Flagged pairs are SURFACED for confirmation; the sweep doesn't auto-remove. The maintenance agent decides: keep earlier (default) / keep later / merge substance.

**Implementation cost**: a sweep script using the spirit CLI's existing query mechanisms. Possibly worth a `spirit "(Observe (Duplicates (Range (N M))))"` first-class operation in a future Spirit version.

**Trade-off**: false positives — substance can overlap without being duplicates (corrections of earlier framings; clarifications adding nuance). Confirmation gate handles this.

**My lean**: ratify. Maintenance pass becomes more thorough.

### Algorithm 3 — Supersession vs Removal distinction

**Problem**: current `spirit "(Remove N)"` discards entirely. For genuine reframings (newer intent supersedes older), we lose the lineage; for accidental duplicates, that's fine. The current discipline conflates two cases.

**Mechanism**: introduce a Supersede operation alongside Remove:
- `spirit "(Remove N)"` — accidental duplicate; discard entirely (current behavior).
- `spirit "(Supersede (OldId NewId) [reason]))"` — newer intent supersedes older; preserve the older record marked-superseded with reference to NewId.

Superseded records remain queryable for history; default queries filter them out. A `(Observe (Supersessions Recent))` query surfaces the supersession history.

**Implementation cost**: a Spirit binary feature. Schema needs a "superseded_by" field on records + a Supersede operation in the wire contract. Not trivial.

**Trade-off**: complexity in Spirit's contract. Workspace gain: history preservation for genuine reframings; clean removal for accidental duplicates. The cost may not justify the gain — alternative is "use Remove for both; rely on git history if you need lineage".

**My lean**: NOT YET — the cost may exceed the gain. Question 1 below asks the psyche to weigh in.

### Algorithm 4 — Magnitude calibration rubric

**Problem**: agents use magnitudes inconsistently. Today's session had Decision High captures that probably warranted Medium (1400 candidate B) + Decision Medium captures that warranted High (workflow disciplines). Without a rubric, agent judgment varies.

**Mechanism**: an explicit calibration table in `skills/intent-log.md`:

| Magnitude | When to use | Examples |
|---|---|---|
| Maximum | Workspace-wide hard rule; non-negotiable across all components; permanent | "No NOTA between components" (1373); "trace as trait on schema-derived interfaces" (1365) |
| VeryHigh | Major architectural mandate; binding workspace-wide; few exceptions | (currently unused; should be slot between Maximum and High) |
| High | Component-level significant; binding within scope; reshapes design | "Engine method-count matches wire events" (1361); "Schema drives most behavior; Rust impl terse" (1387) |
| Medium | Strong direction; expected default; component-design guidance | "Cross-pollination methodology" (1364); designer 471 Candidate C |
| Low | Preference; favored option; weak constraint | (rare; usually elevate to Medium or skip) |
| VeryLow | Hedge; uncertainty; might prove wrong | "Browser automation design considers two paths" (1399) |
| Minimum | Considering; not-yet-decided | Future-design candidates |
| Zero | Removal candidate; soft-deletion pending review | Records flagged but not yet removed |

**Implementation cost**: doc edit only. Agents reference the table when capturing.

**Trade-off**: subjective judgment remains; the table is guidance not law. Reduces the variance but doesn't eliminate it.

**My lean**: ratify. Cheap addition; aligns agent judgment.

### Algorithm 5 — Capture cadence pattern (Maximum eagerly; Medium-and-below after recurrence)

**Problem**: workspace accumulates Medium/Low captures that turn out to be one-off mentions rather than durable intent. Examples from prior sessions: tentative directions, design speculation, "might be useful" framings. These become noise in the active record set.

**Mechanism**: cadence rules per magnitude:
- **Maximum / VeryHigh / High**: capture eagerly when the psyche states something workspace-binding. Don't wait.
- **Medium**: capture when the substance has appeared in TWO contexts (conversations, prompts) — once is speculation, twice is direction.
- **Low / VeryLow / Minimum**: capture only when the substance is explicitly named as durable intent or when the agent identifies a clear future-recall trigger.

**Implementation cost**: discipline addition to `skills/intent-log.md`. Agents apply the threshold when deciding to capture.

**Trade-off**: some Medium captures get missed first-time. Mitigation: agents flag would-be Medium captures in chat ("noting this as direction but not yet capturing — will capture if it recurs").

**My lean**: ratify. Reduces noise; preserves the eager-Maximum discipline.

## Section 3 — Open psyche questions

### Question 1 — Supersession vs Removal (Algorithm 3 above)

When older Spirit intent is reframed by newer intent, should the workspace adopt a Supersede operation that preserves lineage, or stick with Remove (which discards entirely; lineage lives in git history of the spirit-records substrate)?

- **Supersede + preserve**: history queryable through Spirit itself; clean Spirit-native superseded-by lineage; cost is contract complexity.
- **Remove + git lineage**: simpler Spirit; lineage requires checking spirit-records git history (heavier query path); cost is reduced first-class discoverability of reframings.

### Question 2 — Magnitude rubric ratification (Algorithm 4 above)

Should the workspace adopt the explicit magnitude calibration rubric in §"Algorithm 4" (or a refined version of it)? It's a one-shot rubric addition to `skills/intent-log.md`; cheap to land. The risk: rubric becomes a procrastination surface for agents debating magnitude instead of capturing.

### Question 3 — Query-before-capture protocol scope (Algorithm 1 above)

Should query-before-capture be:
- **(a) Every capture**, no exceptions — even single-agent sessions with no forwarding pay the latency.
- **(b) Forwarded-prompt captures only** — when the prompt was addressed to another agent (the case where duplicates arise most), query first; direct prompts don't.
- **(c) Topic-volume-driven** — query first only when capturing on topics with high recent-capture volume (the topics most likely to have already-captured substance).

### Question 4 — Topic vocabulary discipline

`skills/spirit-cli.md` says "reuse existing words when they cover the substance". Should the workspace maintain a canonical topics list (auto-extractable from active records) that agents reference when capturing, or stay agent-discovers-from-existing-records (current shape)?

- **Canonical list**: discoverable; reduces topic word fragmentation (e.g., `testing-trace` vs `trace-testing` vs `runtime-trace`).
- **Agent discovers**: lower overhead; topic vocabulary evolves with the workspace organically; risk of fragmentation.

## Section 4 — Recommended order

Independent of psyche answers on Q1-Q4, the cheap wins to land now:
- ~~Algorithm 4 (magnitude calibration rubric) — doc edit; low risk.~~ **NOT adopted per psyche answer Q2**: agent judgment stays, no rubric.
- Algorithm 5 (capture cadence pattern) — discipline addition; low risk.

Dependent on Q3:
- Algorithm 1 (query-before-capture) — **forwarded-prompt scope per psyche answer Q3**. Lands as discipline addition to `skills/intent-log.md`: when capturing on a forwarded prompt (psyche addresses operator + me; operator addresses psyche then me; etc.), query recent records on the substance topics BEFORE recording. Direct-prompt captures don't pay the latency.

Dependent on Q1 + sized as separate Spirit feature work:
- ~~Algorithm 3 (supersession)~~ — **NOT adopted per psyche answer Q1**: Remove + git lineage stays canonical.

Dependent on Q4 / standalone:
- Algorithm 2 (dedup detection heuristic) — sweep tooling; can land independently.

## Section 5 — Psyche answers + redirect on Q4

Recorded 2026-06-02:
- **Q1 — Supersession**: Remove + git lineage (current) wins. No new Supersede operation.
- **Q2 — Magnitude rubric**: NOT adopted. Agent judgment stays; no calibration table in `skills/intent-log.md`.
- **Q3 — Query-before-capture scope**: Forwarded-prompt only. Algorithm 1 lands as discipline addition for forwarded-prompt captures only.
- **Q4 — Topic vocabulary**: substantive redirect — psyche wants *"a feature to spirit to make those discoverable with a cached-value algorithm — something smart and clever to use nowadays, there must be libraries for this kind of thing"*. NOT one of the three options offered. The redirect means designing a new Spirit feature: cached, modern, library-backed topic discovery. Designer 474 dispatched in parallel to research the algorithm + libraries + Spirit-side API shape.

## Cross-references

- `skills/intent-maintenance.md` — the discipline these algorithms operationalize.
- `skills/intent-log.md` — where Algorithm 4 + Algorithm 5 land as doc edits.
- `skills/spirit-cli.md` — current Spirit binary contract (relevant for Algorithm 3).
- `skills/context-maintenance.md` §"Method" step 6 — Spirit capture sweep step references the dedup discipline these algorithms strengthen.
- `reports/designer/472-context-maintenance-2026-06-02.md` — the recent sweep that demonstrated the dedup pattern at scale.
- Spirit records 1366, 1367, 1376-1380, 1397, 1402-1407, 1410 — the dedup incidents this session.

## For the orchestrator (chat paraphrase)

Five algorithm proposals for spirit/intent-maintenance: (1) query-before-capture protocol; (2) dedup detection heuristic during maintenance sweeps; (3) Supersede operation preserving lineage vs current Remove discarding; (4) magnitude calibration rubric; (5) capture cadence per magnitude. Four open psyche questions whose answers determine ratification path. Cheap wins to land regardless: Algorithm 4 (rubric) + Algorithm 5 (cadence). Heavier: Algorithm 3 (supersession contract change). Asking the questions inline.
