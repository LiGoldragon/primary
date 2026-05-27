# 8 — cluster-operator lane sweep

*Per-lane handoff for the agent in the `cluster-operator` role.
9 reports as of 2026-05-27.*

## Inventory

| # | Date | Topic | One-line summary |
|---|---|---|---|
| 1 | (no date) | bird/zeus local update | Bird-on-zeus local update authority design |
| 3 | 2026-05-22 | third-designer 17 blocker | Audit of /third-designer/17 blockers |
| 4 | 2026-05-22 | update authority + lojix | Current state of update authority + lojix daemon |
| 6 | 2026-05-22 | Pi harness defaults | Pi harness defaults + extension packaging |
| 7 | 2026-05-23 | Pi harness follow-up | Pi harness follow-up after /third-designer/21 |
| 8 | 2026-05-23 | Pi harness extension testing | Pi harness extension testing |
| 9 | (no date) | Pi-operator safety audit | Audit of pi-operator safety dirty-repository fix |
| 10 | 2026-05-23 | Pi YOLO mode | Pi YOLO mode + flake input extensions |
| 11 | 2026-05-23 | MVP sandbox audit | MVP sandbox repo audit + small fixes |

## Topic clusters

### A. Pi-harness implementation thread (dominant)

6 (defaults + packaging), 7 (follow-up), 8 (extension testing), 9
(safety audit), 10 (YOLO mode), 11 (MVP sandbox audit). All
2026-05-22/23.

### B. Update authority + Zeus

1 (bird/zeus local update authority), 4 (current state of update
authority + lojix daemon).

### C. Cross-lane audit

3 (audit of third-designer/17 blockers).

## Recency rank per topic

**Pi-harness:** 11 (2026-05-23) → 10 (2026-05-23) → 9 → 8
(2026-05-23) → 7 (2026-05-23) → 6 (2026-05-22).

**Update authority:** 4 (2026-05-22) → 1 (no date but related).

## Stale flags

Most reports are 2026-05-22 / 2026-05-23 — 4-5 days old. Whether
they're stale depends on whether the Pi-harness work has shipped
and stabilised.

| # | Stale? | Why |
|---|---|---|
| 1 | Possibly stale | Bird/zeus local update authority — if shipped, retire. |
| 3 | Stale | Cross-lane audit of /third-designer/17 (which is recommended for drop in slot 4). |
| 4 | Stale or migrate | Update authority + lojix current state from 2026-05-22; substance likely in `repos/lojix-cli/` and `repos/CriomOS-home/` now. |
| 6-11 | Mixed | Pi-harness landings; if the harness has stabilised, most can retire. /11 (MVP sandbox audit) is the latest in the thread. |

## Drop / forward / migrate / keep per report

| # | Recommendation |
|---|---|
| 1 | **Migrate then drop.** Bird/zeus local-update-authority design → `repos/CriomOS-home/ARCHITECTURE.md`. |
| 3 | **Drop.** Audit of /third-designer/17 which is recommended for drop. |
| 4 | **Migrate then drop.** Update-authority + lojix current state → `repos/lojix-cli/INTENT.md`. |
| 6, 7, 8 | **Drop.** Pi harness defaults + packaging + testing — implementation landed; substance is in `repos/CriomOS-home/`. |
| 9 | **Drop.** Pi-operator safety audit; the fix landed. |
| 10 | **Drop.** YOLO mode is a flag; substance in code. |
| 11 | **Migrate then drop.** MVP sandbox audit — if any substance is still load-bearing for the lean rewrite, migrate to `repos/lojix-cli/INTENT.md`. |

## Handoff section

**When you (the agent in `cluster-operator`) do your next context
maintenance, the relevant decisions are:**

1. **The lane is mostly Pi-harness landing notes.** With 6-11
   covering the harness work from 2026-05-22/23 — the harness
   has shipped, so most of these are historical.

2. **Migrate update-authority + lojix-daemon substance** (1, 4)
   before dropping. The architectural substance belongs in
   `repos/CriomOS-home/` and `repos/lojix-cli/`.

3. **Soft cap.** 9 reports under cap; after drops + migrations,
   1-2 reports max. The lane will be effectively empty.

4. **Cross-lane:** /3 audits third-designer/17 (recommended for
   drop in slot 4 of this meta-directory); /9 audits
   pi-operator's safety fix. Coordinate the audit-target drops.

5. **Open question:** if the cluster-operator lane is going to be
   effectively empty for a while, consider whether to keep the
   lane registered. Per current AGENTS.md the lane has its own
   scope (live cluster maintenance, production deploy/update
   authority); the empty state is just that there's no active
   work right now.
