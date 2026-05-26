# Frame and method — refreshed intent/report visual audit

## User request

Psyche asked pi-operator to repeat the recent refresh, now as an updated report with lots of visuals and code examples, including things I like and dislike.

Intent capture: Spirit record `828` records the task constraint: re-read current intent and reports, include many visuals and code examples, and mark likes/dislikes.

## Method

This is a pi-operator meta-report directory because the refresh uses asynchronous scout subagents. The parent orchestrator remains responsible for synthesis and for distinguishing:

- Spirit intent records;
- role reports;
- repository/branch state;
- my own implementation taste notes.

Subagents are read-only. They must not edit source, reports, lock files, or branches. They return evidence-backed summaries with file paths, report references, branch state, code snippets, diagrams worth carrying forward, and like/dislike notes.

## Output map

Planned files:

- `1-recent-intent.md` — current Spirit intent refresh.
- `2-operator-refresh.md` — operator reports and implementation branch state.
- `3-designer-refresh.md` — designer/designer-assistant reports and prototype branch state.
- `4-nota-designer-refresh.md` — nota-designer and adjacent NOTA/schema repo state.
- `5-overview-visual-audit.md` — pi-operator synthesis with visuals, code examples, likes/dislikes, and practical next moves.

## Stop rules

- Do not rewrite other roles' reports.
- Do not touch operator/designer/nota-designer source worktrees.
- Treat stale reports as evidence with date/order, not as current truth.
- If branch state conflicts with report text, mark the conflict rather than reconciling silently.
