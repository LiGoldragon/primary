# 386 — Cross-lane context maintenance, 2026-05-27

*Kind: Review · Topic: cross-lane-context-maintenance · 2026-05-27*

## Frame — per psyche records 920 + 921 (Maximum, 2026-05-27)

This is the first cross-lane context-maintenance sweep under the
discipline introduced by records 920 + 921. The sweep covers
every active lane in the workspace, recency-ranks reports by
topic, and produces one handoff sub-report per lane.

### What records 920 + 921 establish

- **920 (Maximum) — subagent dispatch + lane retirement.** When
  an agent in role R dispatches a subagent, the subagent inherits
  the dispatcher's lane, lock, and report-numbering slot. The
  prior `<role>-assistant` and `<role>-specialist` suffixes are
  RETIRED workspace-wide. Valid lane shapes: `<role>`,
  `second-<role>`, `third-<role>`, and `<qualifier>-<role>`.
- **921 (Maximum) — topic-recency ranking + meta-report
  directory.** Context maintenance now ranks reports by topic
  across all lanes, favors newer design, identifies stale.
  Cross-lane maintenance produces ONE meta-directory in the
  dispatcher's lane with per-lane sub-reports inside. Each
  per-lane sub-report is a HANDOFF for that role's next own
  maintenance.

### Method applied in this sweep

1. **Skill edits first.** `skills/role-lanes.md` and
   `skills/context-maintenance.md` updated to encode the new
   discipline before applying it.
   `AGENTS.md`, `orchestrate/AGENTS.md`, `orchestrate/roles.list`
   updated for the retired-suffix rule.
2. **Lane retirement.** `reports/designer-assistant/` folded
   into `reports/designer/` (19 reports → 32 in designer); the
   `poet-assistant/`, `second-operator-assistant/`,
   `second-system-assistant/` subdirectories retired (the
   former two were empty bar `.gitkeep`; second-system-assistant
   had 7 reports, folded into `system-operator/`).
3. **Per-lane inventory + topic clustering.** Each active lane's
   reports got: (a) inventory with date + one-line summary, (b)
   topic clusters, (c) recency-rank per topic with stale flags,
   (d) drop/forward/migrate/keep recommendations, (e) a handoff
   section addressing the role's next own maintenance.
4. **No drops executed in non-designer lanes.** The recommendations
   in each sub-report stay as handoff guidance for that lane's
   agent to apply during their own next maintenance. The
   designer-lane reports are this dispatcher's direct surface and
   are eligible for clearly-superseded drops; conservative
   handoff is preferred for anything ambiguous.

### Lanes covered

| Slot | Lane | Reports | Notes |
|---|---|---|---|
| 1 | `designer` | 32 | Now includes the folded designer-assistant reports |
| 2 | `operator` | 59 | Largest active lane; heavy schema/Spirit topic mass |
| 3 | `second-designer` | 45 | Parallel designer window; counter-ego audit thread |
| 4 | `third-designer` | 8 | Pi-as-Codex thread |
| 5 | `second-operator` | 4 | Sparse parallel operator window |
| 6 | `system-operator` | 16 | Includes folded second-system-assistant content |
| 7 | `system-designer` | 9 | Lean rewrite + NOTA system topics |
| 8 | `cluster-operator` | 9 | Pi harness + lojix lane |
| 9 | `pi-operator` | 0 | No reports (lane registered but unused) |
| 10 | `cloud-operator` | 8 | Cloud daemon + cloudflare API |
| 11 | `cloud-designer` | 3 | Recently bootstrapped lane |
| 12 | `nota-designer` | 9 | NOTA-specific design lane |
| 13 | `poet` | 0 | Empty |
| 14 | overview | — | synthesis across lanes |

### Open questions surfaced (also in N-overview.md)

- **`cloud-designer`/`cloud-operator` vs `cluster-operator`.**
  Are these aliases or distinct? Current evidence: `cloud-*`
  lanes are the cloud-daemon / cloudflare-DNS surface;
  `cluster-operator` is the Pi/Zeus cluster surface. They
  appear distinct.
- **`nota-designer` lane status.** Has its own active body of
  work (9 reports through 2026-05-24); not folded into
  `designer/` even though it could be. Treated as a kept
  specialized designer lane per current AGENTS evidence.
- **Empty lanes (`pi-operator`, `poet`).** Both registered but
  carry no reports. Recommend keeping the lock-file slot and
  `reports/<lane>/` listing but flag for future review if
  they remain empty for another sweep cycle.

### What this sweep does NOT do

- It does not delete reports outside `reports/designer/`. Each
  per-lane sub-report is a handoff for that role.
- It does not migrate substance into ARCH or skills as part of
  this pass — that is the destination home for absorbed
  substance, but migration is its own design pass per
  `skills/context-maintenance.md` §"Distribute".
- It does not amalgamate any retired-lane content into 2-3
  topic-grouped summary reports yet — the four retired lanes
  this sweep retired (`designer-assistant`, `poet-assistant`,
  `second-operator-assistant`, `second-system-assistant`) had
  their content folded into the closest main lane intact
  (number-preserved); amalgamation per
  `skills/context-maintenance.md` §"Retired lanes — amalgamate,
  don't list" can be a follow-up if file count justifies it.
