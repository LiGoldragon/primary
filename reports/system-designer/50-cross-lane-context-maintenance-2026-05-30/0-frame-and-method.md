# Frame — cross-lane context maintenance (2026-05-30)

*Dispatcher: system-designer. Successor to
`reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/`
(which retires once this sweep re-issues its still-live
handoffs). Per psyche directive 2026-05-30 ("do a deep
context-maintenance") and `skills/context-maintenance.md` +
Spirit record 921 (cross-lane topic-recency ranking). Trigger:
the past 48 hours added ~40 new reports in the schema-stack
topic across operator + designer lanes while three lanes ran
their own sweeps in response to 44 — the workspace needs a
re-rank and a fresh handoff round.*

## Trigger + inventory (2026-05-30)

Report counts per lane, with delta from 44 (2026-05-28):

| Lane | Now | Was (44) | Δ | Notes |
|---|---|---|---|---|
| operator | 47 | 67 | -20 | Cleaned up; new schema-stack churn 224-259 (+35 fresh) |
| designer | 22 | 42 | -20 | Cleaned up; new schema-stack churn 421-438 (+18 fresh) |
| system-operator | 7 | 21 | -14 | Major cleanup; 172 just absorbed 168/169/170/171 |
| cloud-operator | 7 | 11 | -4 | |
| system-designer | 5 | 15 | -10 | Just absorbed 35/37/39/40/41/42 into 49 |
| cloud-designer | 4 | 6 | -2 | |
| second-designer | 2 | 45 | -43 | Massive cleanup |
| cluster-operator | 1 | 9 | -8 | Massive cleanup |
| third-designer | 0 | 8 | -8 | Lane empty (retirement candidate) |
| second-operator | 0 | 4 | -4 | Lane empty (retirement candidate) |
| poet | 0 | — | — | Lane empty |
| nota-designer | 0 | 9 | -9 | Lane empty (retirement candidate) |

~95 active reports across 8 active lanes. Headline shift since 44:
**the schema-stack arc moved from "vision audits at the door of
implementation" to "live implementation iteration"** — 35+
operator reports and 18 designer reports landed in 3 days, much
of it pair-shaped (designer report → operator implementation
response → designer review of operator's response). The other
lanes are quieter; the schema-stack is where staleness now lives.

## What's also happened since 44 — three lane-side maintenance ledgers

Three lanes responded to 44's handoff with their own
maintenance ledgers, which now sit on disk:

- `reports/system-operator/169-context-maintenance-2026-05-28/`
  — applied 44's system-operator handoff; produced an inventory
  sub-report and executed drops in-lane.
- `reports/designer/415-context-maintenance-2026-05-28.md` —
  designer lane's own sweep.
- `reports/cloud-operator/12-context-maintenance-skill-update-2026-05-28/`
  — cloud-operator's sweep.
- `reports/cloud-designer/15-lane-agglomeration-audit-and-maintenance-2026-05-29.md`
  — cloud-designer's sweep.
- `reports/operator/223-context-maintenance-skill-audit-2026-05-28/`
  — operator's sweep.

Plus this lane's prior sweep `44-cross-lane-context-maintenance-2026-05-28/`.

All six are working artifacts whose retirement (per
`skills/context-maintenance.md` §"Successor sweeps retire
maintenance ledgers") is gated on this sweep absorbing their
still-live handoffs. Each is OWNED BY ITS LANE; the dispatcher
does not delete other lanes' ledgers — the overview records the
handoff to drop them when their owning lane next does
maintenance.

## Method — topic-recency ranking, cross-lane

Per `skills/context-maintenance.md` §2 + record 921: rank
**by topic, across all lanes**, then by recency within topic.
Stale = newer report supersedes + substance landed in successor
or permanent doc. Drop / Forward / Migrate / Keep per §2a.

**Dispatcher executes drops only in its own lane.** Sub-reports
produce per-lane handoff recommendations; each lane applies its
own on next maintenance.

**Landing-gate discipline:** no drop without a named successor
report or permanent home. Per `skills/intent-maintenance.md`
§"Removing a record — tombstone first", the per-report-table
analog is the landing-evidence column in each sub-report's
drop-bands table.

## Slot plan + sub-agent allocation

The directory IS the meta-report (no `meta-` prefix). Six
files; the dispatcher writes 0 and 5; four sub-agents write 1-4
in parallel.

| Slot | File | Owner | Scope |
|---|---|---|---|
| 0 | `0-frame-and-method.md` | dispatcher | this file |
| 1 | `1-schema-derived-stack.md` | sub-agent A | operator 210-259 + designer 421-438 + system-designer 49 + system-operator 172 (Spirit/schema sections) + second-designer 165/176 |
| 2 | `2-deploy-stack-lojix-horizon-cloud.md` | sub-agent B | system-designer 34 + system-operator 167 + cloud-designer 11/13/14 + cloud-operator 6-13 + cluster-operator 1 + the cloud-related parts of 172 |
| 3 | `3-spirit-and-intent-removal.md` | sub-agent C | system-designer 48 + 49 (intent-removal/search sections) + system-operator 172 (Spirit sections) + 169-context-maintenance + intent-related operator/designer reports |
| 4 | `4-standalone-and-workspace.md` | sub-agent D | system-operator 1/2/139/166 (Arca, Whisrs, DJI) + designer 351/352/412 (intent audits) + workspace-discipline reports + the prior maintenance ledgers (44/415/12/15/223/169) as retirement candidates |
| 5 | `5-overview.md` | dispatcher | synthesis + per-lane handoffs + dispatcher-executed drops + retirement of prior maintenance ledgers |

## Sub-agent discipline (briefed to each)

Each sub-agent:

- Is **read-only**: writes only its assigned slot file. No
  drops; no commits.
- Inherits the system-designer lane per
  `skills/role-lanes.md` §"Subagent dispatch inherits the
  dispatcher's lane".
- Reads inventory + dates first; deep-reads only stale
  candidates and their proposed successors / permanent
  landings. No deep-reading hundreds of reports.
- Follows the §"Per-topic sub-report shape" structure (topic
  arc → canonical surface → drop bands by lane → landing
  evidence → drop ownership handoff).
- Includes the path-as-locator (per psyche 2026-05-30 record
  1242) every time it cites a report.
- Watches the §3a design-rationale guard (a report
  enumerating competing designs stays even when its chosen
  design migrates — recommend "Keep + status-banner" not
  "Drop").
- Stays bounded to its topic; cross-topic edges go in the
  overview, not the sub-report.

## Anti-patterns to watch (this sweep specifically)

- **Bulk-retiring the schema-stack pile.** With ~55 reports
  in flight and many pair-shaped (designer↔operator
  response), staleness is read pair-wise. A response-report
  whose source-report is also stale retires together; a
  response-report whose source is canonical (designer vision
  → operator implementation that landed) needs landing-
  evidence even if the visual mass looks redundant.
- **Treating prior maintenance ledgers as permanent
  archive.** They're working artifacts under the standard
  rules — each retires when its handoffs are applied AND a
  newer sweep covers the same ground. This sweep is the
  successor.
- **Forgetting record 1242 (path-as-locator).** Every report
  reference in every sub-report carries the full path. No
  bare numbers.
