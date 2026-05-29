# Frame — cross-lane context maintenance (2026-05-28)

*Dispatcher: system-designer. Per psyche directive 2026-05-28 ("use a subagent to do context-maintenance — aggregate reports per topic so stale reports don't linger") and `skills/context-maintenance.md` + Spirit record 921 (cross-lane topic-recency ranking). Trigger: the report directories are far over the 12-report soft cap on five lanes. This meta-report directory carries the sweep; per the skill the dispatcher executes drops ONLY in its own lane (system-designer), and produces handoff recommendations for the other lanes.*

## Trigger + inventory

Report counts per lane (2026-05-28):

| Lane | count | over 12-cap? |
|---|---|---|
| operator | 67 | yes (5.5x) |
| second-designer | 45 | yes |
| designer | 42 | yes |
| system-operator | 21 | yes |
| system-designer | 15 | yes (this lane) |
| cloud-operator | 11 | no |
| nota-designer | 9 | no |
| cluster-operator | 9 | no |
| third-designer | 8 | no |
| cloud-designer | 6 | no |
| second-operator | 4 | no |

~237 reports across 11 active lanes. Heavy staleness expected — this session alone added system-designer 34-44 + designer 374-409, much of which threads a few fast-moving topics where newer reports supersede older.

## Method (per `skills/context-maintenance.md` §2 + record 921)

**Topic-recency ranking, across all lanes.** For each major topic, find all reports across every lane, recency-rank (newest canonical), flag stale (a newer report supersedes the substance AND it's absorbed), and recommend drop / forward / migrate / keep per the skill's §2a rule. The output is TOPIC-AGGREGATED (the psyche's emphasis: "aggregate reports per topic so stale reports don't linger"), not a flat per-lane dump.

**Dispatcher executes drops only in its own lane.** The sweep produces recommendations; system-designer (me) executes drops/forwards in `reports/system-designer/` on return; every other lane gets a handoff recommendation it applies when it next does its own maintenance (per the skill §"Per-lane sub-report shape").

## Proposed topic clusters (the subagent refines)

The major topics threading the workspace right now:

1. **Schema-derived stack** — nota-next/schema-next/schema-rust-next/spirit-next, the macro/emission/runtime-triad/Plane design. Threads designer/ (376-409), nota-designer/ (5-9), second-designer/ (schema audits 190-196), operator/ (210-219).
2. **Lojix / Horizon / CriomOS deploy stack** — the lean rewrite, schema-deep pilots, horizon-next, the cutover/reconciliation. Threads system-designer/ (29-44), system-operator/ (162-168), cluster-operator/, operator/ (lojix-related).
3. **Cloud + deployment** — gemma/cloudflare/browser, prometheus inference. Threads cloud-designer/ (1-6), cloud-operator/ (1-11).
4. **Persona components + runtime** — spirit/mind/router/terminal/agent/upgrade, the older component arcs. Threads operator/ (most of the 67), second-operator/.
5. **Workspace discipline + misc** — intent/reporting/naming/jj/role-lanes sweeps. Scattered.

## Slot plan

- `0-frame-and-method.md` — this file.
- `1-...` through `N-1` — per-topic aggregation sub-reports (the subagent allocates by the clusters above; each lists the topic's reports across lanes, recency-ranked, with drop/forward/migrate/keep + the lane that owns each drop).
- `N-overview.md` — dispatcher synthesis: the cross-cutting picture + the system-designer-lane drops I execute + the per-lane handoff pointers.

## Dispatch — one context-maintenance subagent (inventory-level, may sub-dispatch)

A single subagent does the cross-lane sweep at inventory level (filenames + dates + topic-cluster + recency-rank), reading the newer+older pair only on stale CANDIDATES to confirm supersession (not deep-reading all ~237). It is authorized to sub-dispatch background helpers per topic-cluster if the volume demands (designer protocol). It writes the per-topic aggregation sub-reports; it does NOT execute drops (the dispatcher does, in-lane only). Brief is in the dispatch prompt.

## Constraints

- Research-only at the report level: the subagent reads reports + permanent docs (does this substance already live in a skill / ARCH / INTENT? superseded?) and RECOMMENDS; it does not delete other lanes' reports.
- Retired lanes (the prior `-assistant`/`-specialist` suffixes per record 920): none remain as directories in the inventory above, so no retired-lane amalgamation needed this pass — but flag any retired-lane references found.
- Honesty: a stale flag must be backed by the specific newer report that supersedes it + where the substance landed; don't recommend dropping un-migrated substance (skill §"Anti-patterns").
