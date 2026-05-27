# 7 — system-designer lane sweep

*Per-lane handoff for the agent in the `system-designer` role.
9 reports as of 2026-05-27.*

## Inventory

| # | Date | Topic | One-line summary |
|---|---|---|---|
| 26 | (no date) | lean rewrite | Lean-rewrite shape analysis (Logix/Horizon/CriomOS) |
| 27 | (no date) | NOTA mixed-enum | Proposal: collapse NotaSum + NotaEnum into NotaMixed |
| 28 | (no date) | lojix vision gap | Lojix vision gap audit |
| 29 | (no date) | lean horizon | Lean horizon cluster-data shape |
| 30 | (no date) | horizon-lojix migration | Low-level migration (meta-directory) |
| 31 | 2026-05-23 | cluster-operator audit | Audit of cluster-operator/7 Pi-harness follow-up |
| 34 | (no date) | MVP + sandbox audit | MVP and sandbox audit (meta-directory) |
| 35 | (no date) | schema deep new logics | Schema deep new logics |
| 36 | (no date) | CriomOS reconciliation audit | Designer audit of system-operator/162 |

## Topic clusters

### A. Lean-rewrite stack (Logix / Horizon / CriomOS)

26 (shape analysis), 28 (lojix vision gap), 29 (lean horizon), 30
(horizon-lojix migration, meta-directory).

### B. NOTA + schema design

27 (NOTA mixed-enum), 35 (schema deep new logics).

### C. Cross-lane audits

31 (cluster-operator/7 audit), 34 (MVP + sandbox audit), 36
(system-operator/162 audit).

## Recency rank per topic

**Lean rewrite** (dates mostly missing):

1. 30 (horizon-lojix migration, meta-dir)
2. 29 (lean horizon cluster-data, no date)
3. 28 (lojix vision gap, no date)
4. 26 (shape analysis, no date)

**NOTA + schema:**

1. 35 (schema deep new logics, no date)
2. 27 (NOTA mixed-enum, no date)

**Cross-lane audits:**

1. 36 (CriomOS reconciliation, no date — recent)
2. 34 (MVP + sandbox audit, meta-dir)
3. 31 (cluster-operator/7 Pi audit, 2026-05-23)

## Stale flags

| # | Stale? | Why |
|---|---|---|
| 26, 28, 29 | Possibly stale | Lean-rewrite shape analyses; check current `repos/lojix-cli/` and `repos/horizon-rs/` state. Substance may have shipped or been refactored. |
| 27 | Possibly absorbed | NOTA mixed-enum proposal — check whether absorbed into current schema crate. |
| 30 | Check | Migration meta-directory; might be live or might be done. |
| 31 | Possibly stale | Pi harness audit from 2026-05-23; the Pi work has moved on. |
| 34 | Check | MVP + sandbox audit meta-directory. |
| 35 | Possibly active | Schema deep new logics — depending on how recent. |
| 36 | Recent | CriomOS reconciliation audit; current thread. |

## Drop / forward / migrate / keep per report

| # | Recommendation |
|---|---|
| 26 | **Migrate then drop.** Lean-rewrite shape analysis substance → `repos/lojix-cli/INTENT.md` or `repos/horizon-rs/ARCHITECTURE.md`. |
| 27 | **Drop.** NOTA mixed-enum collapse likely already implemented in the schema crate; check and drop. |
| 28 | **Migrate then drop.** Lojix vision gap → `repos/lojix-cli/INTENT.md`. |
| 29 | **Migrate then drop.** Horizon cluster-data shape → `repos/horizon-rs/ARCHITECTURE.md`. |
| 30 | **Drop if done.** Migration meta-directory; if the migration shipped, the meta-directory retires per `skills/reporting.md` §"Meta-report directories — sub-agent sessions". |
| 31 | **Drop.** Pi-harness audit absorbed into cluster-operator and CriomOS-home current state. |
| 34 | **Drop if done.** MVP + sandbox audit meta-directory. |
| 35 | **Keep or forward.** Schema-deep-logics could fold into designer's schema-language thread (385). Check whether it's still load-bearing. |
| 36 | **Keep.** Recent CriomOS reconciliation audit. |

## Handoff section

**When you (the agent in `system-designer`) do your next context
maintenance, the relevant decisions are:**

1. **Lean-rewrite stack substance wants permanent docs.** Reports
   26, 28, 29 carry per-repo architectural substance that belongs
   in `repos/lojix-cli/`, `repos/horizon-rs/`, and `repos/
   CriomOS-home/`. Migrate before dropping.

2. **NOTA mixed-enum (/27) is likely shipped.** Check the schema
   crate; if the proposal is implemented, the report retires.

3. **Pi-harness audit (/31) is old.** 2026-05-23 audit; the Pi
   work has moved through cluster-operator and beyond. Likely
   drop.

4. **CriomOS reconciliation audit (/36) is the current thread.**
   Active alongside system-operator/162 + /163.

5. **Soft cap.** 9 reports is under cap; after the recommended
   drops + migrations, lane lands at 3-4 reports.

6. **Cross-lane:** /31 audits cluster-operator/7; /36 audits
   system-operator/162. Coordinate the audit-target drops with
   cluster-operator (slot 8) and system-operator (slot 6).
