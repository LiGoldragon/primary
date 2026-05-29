# 2 — Topic: Lojix / Horizon / CriomOS deploy stack (cross-lane)

*Cross-lane topic aggregation per `skills/context-maintenance.md` §2.
The lean-rewrite deploy stack — lojix daemon + thin CLI, horizon-rs,
CriomOS, the cluster proposal — and its 2026-05-28 re-grounding onto
the schema-next/nota-next stack. Threads system-designer (the home
lane), system-operator, cloud-operator, cluster-operator. This is the
SECOND-most-active topic and the centre of this dispatcher's own lane.*

## The arc in one line

Two eras: (1) the **lean-rewrite analysis era** (2026-05-20→23) —
shape analysis, vision-gap audits, low-level migration, measured
against legacy `intent/*.nota`; and (2) the **schema-next re-grounding
era** (2026-05-27→28) — "port horizon/lojix to be schema-at-heart",
the schema-deep pilots, the collections gate, the Horizon pure-schema
concept prototype + its divergence audit. The era-2 work supersedes
era-1's framing because the whole stack is now being re-grounded on
schema-next.

## Recency rank (newest canonical at top)

**Current surface (KEEP):**

1. `cloud-operator/11` (05-28) — Lojix/Horizon/CriomOS rewrite intent
   + implementation audit. The **newest cross-cutting read** of the
   whole topic: reads INTENT.md + system-designer/37-42 +
   system-operator/164-167. **KEEP — newest canonical synthesis.**
2. `system-designer/42` (05-28) — Horizon /167 divergence + fixes.
   Artifact-grounded audit of the Horizon pure-schema concept against
   FULL intent. **KEEP — current designer audit; cloud-operator/11
   and designer/412 both build on it.**
3. `system-operator/167` (05-28) — Horizon pure-schema concept
   prototype (the artifact /42 audits). **KEEP — the live prototype.**
4. `system-designer/41/` (05-28) — horizon-schema-pipeline concept
   (collections + Horizon). **KEEP — current concept brief.**
5. `system-designer/40/` (05-28) — horizon/lojix schema-next port
   feasibility (verdict: YES; collections+Option is the first gate).
   **KEEP — the load-bearing feasibility verdict; /41, /42, /167,
   cloud-operator/11 all depend on it.**
6. `system-designer/39/` (05-28) — schema-cargo cross-crate import
   (types-only-module finding). **KEEP — current; feeds the port.**
7. `system-operator/166` (05-28) — DJI mic profile-churn fix.
   **KEEP (recent, but a hardware-repair one-off — see note).**
8. `system-designer/37/` (05-27) — schema-deep iteration 2 (nexus /
   mail / sema engine). **KEEP — the schema-deep pilot the port
   feasibility builds on; cited by cloud-operator/11.** Borderline:
   may collapse into /40 once the port lands.
9. `designer/412` (05-28) — review of system-designer/42 + horizon/167
   audit. **KEEP — designer lane, protected (in the 405-414 band).**

**Stale band (drops, by lane):**

### system-designer (this dispatcher's lane — I execute these)

| Report | Date | Superseded by | Substance landed |
|---|---|---|---|
| `26` lean-rewrite shape analysis | 05-23 | era-2: /40 (port feasibility) re-grounds the whole shape | shape now in `repos/lojix` + `repos/horizon` per-repo INTENT; superseded framing |
| `28` lojix vision-gap audit | 05-23 | audits `system-specialist/154` (a RETIRED lane) against legacy `intent/*.nota`; superseded by /40 + /42 | gaps closed by the schema-next port direction |
| `29` lean-horizon cluster data-shape | 05-23 | /40 + /41 (collections gate reframes cluster data) | INTENT.md §schema-driven-stack + /41 |
| `30/` horizon-lojix low-level migration | 05-23 | /40 (feasibility) + /37 (schema-deep pilot) | superseded by the schema-next re-grounding |
| `31` audit of cluster-operator/7 pi-harness | 05-23 | Pi-harness topic retired (see workspace sub-report) | Pi work shipped; audit historical |
| `36` criomos-reconciliation audit | 05-27 | audits system-operator/162, which /163 then re-critiqued post-schema-next; /40+/42 carry forward | reconciliation direction in /40; INTENT.md two-deploy-stacks |
| `38` source-staging prototype audit | 05-27 | audits system-operator/165; superseded by /40 (full port feasibility supersedes the source-staging step) | staging finding absorbed into /40 |

**7 system-designer reports** DROP. Notes:
- `28` audits `system-specialist/154` — `system-specialist` is a
  **retired lane** (record 920). Its audit target no longer exists in
  the inventory; the report is doubly stale.
- `26`/`28`/`29`/`30/` all measure against **legacy `intent/*.nota`
  files** (component-shape.nota, signal.nota, deploy.nota, horizon.nota)
  — that substrate is superseded by Spirit + INTENT.md per the workspace
  intent-layer migration. Era-1 framing throughout.
- `34/` (mvp-and-sandbox-audit, 05-23) and `35/` (schema-deep new
  logics, 05-27): **KEEP for now.** `34/` carries an active bead queue
  (production-realities: criome auth, real nspawn, owner-signal) that
  /40 explicitly defers TO `34/`'s queue — load-bearing until that
  queue drains. `35/` is the schema-deep-logics design that /37 and /40
  build on. Both are recent enough and still referenced.

### system-operator

| Report | Date | Superseded by | Recommendation |
|---|---|---|---|
| `162` production-to-lean criomos reconciliation | 05-27 | /163 (own re-critique) + system-designer/40+42 | DROP — superseded by the schema-next re-grounding; reconciliation direction in /40 |
| `163` critique of /162 after schema-next refresh | 05-27 | system-designer/40 (feasibility) + /42 | DROP — the critique's conclusion (re-ground on schema-next) is now the executed direction in /40 |
| `164` criomos-lojix rewrite audit + production vision | 05-27 | cloud-operator/11 (newest cross-cutting) + /40 | FORWARD-then-DROP — the production-vision substance feeds /40 + cloud-operator/11; confirm landed then drop |
| `165` lojix source-staging prototype + component critique | 05-27 | system-designer/38 (audit) + /40 (full feasibility) | DROP — source-staging step superseded by the port feasibility |

**4 system-operator reports** DROP (162, 163, 165 clean; 164 forward-
then-drop). The cloud-component / cloud-foundation system-operator
reports (139, 156-160) belong to the **cloud topic** (sub-report 3).
The NOTA / speech / spirit folded reports (1-7) belong to other topics
(workspace + persona). `161` (DJI mic keepalive, 05-27) and `166`
(DJI mic profile churn, 05-28) are **hardware-repair one-offs** — see
note below.

**Note on the DJI-mic reports (system-operator/161, 166):** these are
device-keepalive repair logs, not topic-arc reports. `166` (05-28)
supersedes `161` (05-27) on the same DJI-mic issue. Recommend
**DROP 161** (superseded by 166) and **KEEP 166** as the current
device state, OR migrate the keepalive fix to a system-operator
runbook if one exists. Cross-topic; flagged here because both surfaced
in the system-operator inventory.

### cluster-operator

The cluster-operator Lojix-adjacent reports:

| Report | Date | Superseded by | Recommendation |
|---|---|---|---|
| `4` update-authority + lojix-daemon current-state | 05-22 | era-2 re-grounding (/40) + INTENT.md §two-deploy-stacks | DROP — lojix daemon state superseded; update-authority design in `1` |
| `1` bird-zeus local update-authority design | 05-22 | (design-rationale — see guard note) | KEEP-or-MIGRATE — see note |

`cluster-operator/1` is a **design report** (update-authority on
bird/zeus). If it enumerates alternatives it's a §3a guard; if single-
shape, it migrates to `repos/lojix/INTENT.md` or the cluster runbook.
Recommend the cluster-operator agent check on its next pass. The rest
of cluster-operator (Pi-harness: 3, 6, 7, 8, 9, 10, 11) is the
**Pi-harness topic** — see the workspace-discipline sub-report.

## Stale-flag count for this topic

**~13 reports** flagged stale: system-designer 7, system-operator 4
(+1 DJI dedup), cluster-operator 1-2. Backed by the named era-2
canonical reports (/40, /42, cloud-operator/11) + INTENT.md
§two-deploy-stacks + §schema-driven-stack.

## Drop ownership by lane (handoff)

- **system-designer (THIS dispatcher executes):** 26, 28, 29, 30/, 31,
  36, 38 (7). KEEP: 34/ (active bead queue), 35/, 37/, 39/, 40/, 41/,
  42 (current arc). This is the dispatcher's own lane — these are the
  drops the dispatcher actions directly. Collapses system-designer
  from 15 → ~8.
- **When `system-operator` next does maintenance, the Lojix drops it
  owns are:** 162, 163, 165 (clean) + 164 (forward-then-drop) + 161
  (DJI dedup vs 166). The cloud-foundation reports (139, 156-160) it
  owns are in the cloud sub-report.
- **When `cluster-operator` next does maintenance, the Lojix drop it
  owns is:** 4 (lojix-daemon state). Borderline: 1 (update-authority
  design — keep-or-migrate). Its Pi-harness reports are in the
  workspace sub-report.
- **cloud-operator/11 is the newest canonical — KEEP.** No cloud-
  operator drops in this topic.
