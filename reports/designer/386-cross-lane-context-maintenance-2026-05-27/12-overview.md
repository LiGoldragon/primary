# 12 — Overview: cross-lane synthesis

*Orchestrator synthesis of the sweep in this meta-directory.
Per psyche records 920 + 921 (Maximum, 2026-05-27).*

## What each lane needs to know about itself

The eleven preceding sub-reports each carry a handoff section
for the agent in that role. The headlines:

- **designer (slot 1, 32 reports).** Now includes folded
  designer-assistant content. Soft cap exceeded by 20+; the
  recommended drops + migrations bring the lane down to ~15
  reports of active substance. Active thread: 383 + 384 + 385.
- **operator (slot 2, 59 reports).** Workspace's largest lane.
  Soft cap exceeded by ~47. Schema-language and Spirit-deployment
  clusters both want collapsing. Recommended pass: keep ~12
  most-recent + structural-rationale reports; drop the rest.
- **second-designer (slot 3, 45 reports).** Counter-ego audit
  thread mostly retires when audited reports retire. Persona-
  architecture substance has matured and wants migration to
  permanent docs.
- **third-designer (slot 4, 8 reports).** Quiet since 2026-05-24.
  Most reports are 5+ days old; substance is absorbed.
- **second-operator (slot 5, 4 reports).** All from 2026-05-25.
  Substance wants migration to ARCH; lane will be effectively
  empty after.
- **system-operator (slot 6, 16 reports).** Includes 7 folded
  from second-system-assistant. Cloud-foundation work (156-160)
  wants forward to cloud lanes. CriomOS reconciliation is the
  current active thread.
- **system-designer (slot 7, 9 reports).** Lean-rewrite substance
  wants per-repo migration. CriomOS reconciliation audit (/36)
  is the current thread.
- **cluster-operator (slot 8, 9 reports).** Mostly Pi-harness
  landing notes from 2026-05-22/23; ready to retire.
- **cloud-operator (slot 9, 8 reports).** Most content (1-5) is
  misplaced Pi-related work; should forward to cluster-operator
  or pi-operator.
- **cloud-designer (slot 10, 3 reports).** Brand-new lane;
  nothing to clean up. Pending inbound content from
  system-operator + third-designer + second-designer.
- **nota-designer (slot 11, 9 reports).** Bracket-string work
  shipped; reports are historical. NOTA+schema lowering work
  may have folded into designer/385.

## Cross-cutting observations

### 1. The schema-language thread is the workspace's centre of gravity

Roughly 80+ reports across designer, operator, second-designer,
second-operator, nota-designer, and system-operator carry
schema-language substance. The current canonical is `designer/385`
+ `operator/210-214`. Older substance from 170s/180s/early-300s
has either absorbed into the schema crate, into permanent docs,
or is ready to retire.

The cross-lane work suggests a substantive migration pass into
`repos/schema/ARCHITECTURE.md` is overdue — the lane reports
duplicate substance that wants to live in one place.

### 2. The Pi-harness thread is mostly retired

Cluster-operator (6-11), third-designer (20, 21), cloud-operator
(1-5) all carry Pi-harness work from 2026-05-22/23. The work
shipped; the reports are historical. A coordinated retirement
pass across these lanes would clear ~15 reports in one move.

### 3. Cloud-component foundation should consolidate

System-operator (156-160), second-designer (196), third-designer
(22), and cloud-designer (1-3) + cloud-operator (8) all carry
cloud-component design substance. The newer lanes
(cloud-designer, cloud-operator) are the canonical home. The
older lane reports should forward.

### 4. Spirit deployment is mostly absorbed

Operator (158-163, 186-191, 205, 206) carries the Spirit
deployment chain. The v0.2 cutover landed (operator/189); the
substance should migrate into `repos/persona-spirit/
ARCHITECTURE.md` and the reports retire.

### 5. The counter-ego audit pattern works

Second-designer's audit thread (170s-190s) demonstrates the
parallel-designer audit-of-parallel-operator pattern. It catches
issues operator's self-audit misses. The audits retire when their
targets retire; the *pattern* should live in `skills/<role>.md`
(designer + operator).

### 6. Workspace is mid-fold from heavy specialist-suffix usage

The retired-suffix transition (record 920) lands at a moment
when the workspace has 12+ active lanes and growing. The new
naming (ordinal + qualifier) is cleaner; the migration is mostly
complete after this sweep.

## Open questions surfaced

### 1. `cloud-designer` / `cloud-operator` vs `cluster-operator`

**Evidence:** `cluster-operator` per current AGENTS.md is "live
cluster maintenance, production deploy/update authority". The
existing content under `cluster-operator/` is Pi-harness work
(bird-on-zeus, lojix daemon, Pi extensions). The `cloud-operator`
lane exists separately — its bootstrap content (cloud-component
design recap) is about Cloudflare DNS and cloud daemons.

**Recommendation:** these are distinct lanes — `cluster-operator`
is Pi/Zeus/criome-physical-cluster; `cloud-operator` is
cloudflare-DNS / cloud-daemon. Document this distinction in
`orchestrate/AGENTS.md` and `AGENTS.md`'s role table to prevent
mis-routing.

**Action:** updated `orchestrate/AGENTS.md` in this sweep to
distinguish the two. The boundary is now:
- `cluster-operator` — physical cluster (Pi, Zeus, lojix daemon)
- `cloud-operator` — cloud-deploy surfaces (Cloudflare DNS,
  provider APIs, cloud daemons)
- `cloud-designer` — design for the cloud-operator's surface

### 2. `nota-designer` lane status

**Evidence:** the lane has 9 reports, all bracket-string or
notation work, all 2026-05-23 or older. The active NOTA-language
design has moved into `designer/` (385) and the schema crate.

**Recommendation:** keep the lane registered for now (specialist
lane reservation); reassess if it stays inactive through another
sweep cycle. If it remains inactive, fold its 9 reports into
`designer/` per the lane-retirement discipline.

**Carry-uncertainty per `skills/architecture-editor.md`** — the
lane's future is proposed-not-decided. Default action: keep.

### 3. `pi-operator` and `poet` empty lanes

**Evidence:** Both have `reports/<lane>/` directories that are
empty (no reports). Both are registered in
`orchestrate/roles.list`.

**Recommendation:** keep the lock-file slots and `reports/<lane>/`
listings; the lanes are reservations for future use. If they
remain empty for another sweep cycle, consider whether the
reservations are still load-bearing.

### 4. Soft-cap discipline at lane scale

Several lanes are well over the 12-report soft cap (designer 32,
operator 59, second-designer 45). The soft cap discipline assumes
per-lane review; cross-lane work makes the cap a workspace-wide
concern, not just per-lane.

**Recommendation:** the topic-recency ranking from record 921
gives us a cross-lane handle on the cap. When the workspace's
total report count is X, and one topic threads through several
lanes, the cap should be applied per-topic-cluster as well as
per-lane. The current sweep is the first pass under that
discipline.

### 5. The `<role>-assistant` suffix retirement (record 920) is complete

After this sweep:
- `reports/designer-assistant/` folded into `reports/designer/`.
- `reports/poet-assistant/` retired (was empty).
- `reports/second-operator-assistant/` retired (was empty).
- `reports/second-system-assistant/` folded into
  `reports/system-operator/`.

The `orchestrate/<lane>-assistant.lock` files remain in the
filesystem (gitignored, transient). The `orchestrate/AGENTS.md`
table no longer enumerates the retired lanes. The
`orchestrate/roles.list` no longer registers them.

No agent should ever introduce a new `<role>-assistant` or
`<role>-specialist` lane after record 920.

## What this sweep changed in skills + workspace surface

| File | Change |
|---|---|
| `skills/role-lanes.md` | Added §"Lane naming convention" (retired suffixes, valid shapes). Added §"Subagent dispatch inherits the dispatcher's lane". Updated other sections to remove `-assistant` references. |
| `skills/context-maintenance.md` | Added §"Topic-recency ranking (cross-lane reading)". Added §"Cross-lane meta-report directory". |
| `AGENTS.md` | Updated Roles section, subagent dispatch override, and worktree-discipline override to use the new lane vocabulary. Added reference to record 920. |
| `orchestrate/AGENTS.md` | Replaced role table with the post-retirement set. Updated reports subdirectory list. Updated claim-flow `<role>` enumeration. |
| `orchestrate/roles.list` | Removed retired-assistant entries. Updated header comment to reference record 920. |
| `reports/` | Folded `designer-assistant` into `designer`; retired `poet-assistant`, `second-operator-assistant`, `second-system-assistant` (the last folded into `system-operator`). |

## Where this sweep stops short

- **Did not execute drops in non-designer lanes.** Per the
  directive: per-lane sub-reports are handoffs; the receiving
  agent applies the recommendations during their own next
  maintenance.
- **Did not migrate substance into permanent docs.** Migration
  is a separate design pass; this sweep names the candidates.
- **Did not create the 2-3 topic-grouped summary reports for the
  retired lanes.** Per `skills/context-maintenance.md` §"Retired
  lanes — amalgamate, don't list", the retired-lane content
  could amalgamate into topic-grouped summaries; this sweep
  folded number-preserved instead. If the receiving lanes
  decide the folded content is too noisy, they can do the
  amalgamation as part of their own maintenance.
- **Did not address the `cloud-operator/1-5` misplacement.** The
  recommendation is to forward Pi-related content into
  `cluster-operator/` or `pi-operator/`; this would be a
  cross-lane edit, which is the cloud-operator agent's territory
  to apply.

## Handoff to the dispatching designer

The next-numbered designer report (387) takes over from this
sweep. Whoever continues the designer-lane work after this can:

1. Apply the §"Drop / forward / migrate / keep" recommendations
   for the designer lane (slot 1) — that's the designer's
   direct surface and the only one with execute authority.
2. Pass the per-lane sub-reports (2-11) to the agents in those
   roles when they next open a session. The handoff sections
   address them directly.
3. Track which lanes apply recommendations; the next cross-lane
   sweep can verify.
4. Open the question about the `nota-designer` lane status at
   the next opportune moment with the psyche.
