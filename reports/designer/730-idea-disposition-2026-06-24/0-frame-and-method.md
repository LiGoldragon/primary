# 0 · Frame and method — designer-lane idea disposition

Date: 2026-06-24. Lane: designer (prime). Trigger: psyche direction —
"do a context-maintenance for the designer lane," reframed by the psyche
into the disposition model below.

## The model — an idea drains to one of three fates

Generic context-maintenance offers four actions (forward / migrate /
keep / drop). The psyche sharpened it for the designer lane: a designer
report is a pile of **ideas**, and an idea is never *kept* as a standing
archive. Each idea drains to exactly one of three fates:

- **intent** — durable direction the psyche wants the project to *be*
  (principle / decision / constraint / clarification). Not already in
  `INTENT.md` or the Spirit log. An idea can only *become* intent with
  the psyche's blessing — agents recommend, never infer. → captured via
  the Spirit CLI, reflected into the relevant `INTENT.md`.
- **work** — a concrete, buildable/actionable thing. Not already a
  tracked bead. → becomes a new `bd` issue (work assignment) for a lane.
- **abandon** — stale / superseded / wrong / a dead exploration, OR
  already-landed (already in code, a skill, `ARCHITECTURE.md`, already
  intent, or already a bead). → the report retires (git preserves it).

The three fates *are* the landing gate: every idea routed to intent, a
bead, or abandonment means its origin report has drained and can retire.
The end state is `reports/designer/` back under the soft cap, with no
load-bearing idea lost — each one became intent, became work, or was
deliberately let go.

## Scope

The literal `reports/designer/` lane: 129 report entries (≈101 flat
reports + 28 meta-report directories), numbered 528→729, dated through
2026-06-24. The scoped designer-family lanes (`cloud-designer`,
`system-designer`, `schema-designer`, `nota-designer`, `second-designer`)
are owned by their own sessions and are out of scope; clean cross-lane
agglomerations are noted for them, not executed against their files.

## Method

1. **Snapshot** current intent (`INTENT.md` + `ESSENCE.md` + Spirit
   records) and current beads (`bd list` open + recently closed), so any
   idea already routed is pre-marked abandon rather than re-litigated.
2. **Extract** every distinct idea across all 129 entries (8 parallel
   range agents) — 312 raw ideas surfaced, each with a recommended fate
   and status evidence.
3. **Cluster + dedupe** — the same idea recurs across dozens of reports;
   raw ideas were partitioned into 11 topic clusters and deduped in
   parallel into distinct ideas, each citing all its origin reports.
4. **Walk** the ledger (`1-idea-ledger.md`) with the psyche, deciding
   each live idea's fate. Intent candidates especially need the psyche's
   explicit blessing.
5. **Execute** the confirmed decisions: capture intent via Spirit, open
   beads for work, retire drained reports.

## Artifacts in this directory

- `0-frame-and-method.md` — this file.
- `1-idea-ledger.md` — the deduped, clustered idea ledger with a
  recommended fate per distinct idea. The centerpiece we walk together.

## Status

Extraction and cluster-dedupe complete; ledger assembled for the
walk-through. Decisions and execution (Spirit captures, beads, report
retirements) follow the psyche's per-idea calls and are recorded as they
land.
