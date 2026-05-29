# Overview — cross-lane context maintenance (dispatcher synthesis)

*Dispatcher (system-designer) synthesis of the 2026-05-28 cross-lane sweep. The subagent produced five per-topic aggregation sub-reports (slots 1-5) across ~237 reports in 11 lanes; this overview records the decisive cross-cutting finding, the system-designer-lane drops I executed, the per-lane handoffs the other lanes apply, and the items surfaced to the psyche. Per `skills/context-maintenance.md`: the dispatcher executes drops ONLY in its own lane; other lanes get handoff recommendations in the sub-reports.*

## The decisive cross-cutting finding

**The schema-derived-stack substance has now migrated into `INTENT.md`** (verified: the §"schema-driven stack" + the schema/Rust-mirror sections, INTENT.md now 660 lines). That single fact is what makes this sweep able to retire the large operator + second-designer + persona piles that the PRIOR sweep (designer/386, 2026-05-27) could not: a report is only stale when its substance is absorbed somewhere permanent, and until the schema-stack design landed in INTENT.md, those piles' substance had no permanent home. Now it does — so ~190 reports across the workspace flag genuinely stale, backed by the specific INTENT.md sections + the canonical era-2 reports.

The workspace is in a **two-era** state on its dominant topics: an era-1 analysis/vision phase (measured against the legacy `intent/*.nota` substrate) superseded by an era-2 schema-at-heart re-grounding (schema-next/nota-next + the pilots). Era-1 reports across every lane are the bulk of the stale flags.

## Topic landscape + stale counts

| Sub-report | Topic | Stale flags | Heaviest lane |
|---|---|---|---|
| 1 | schema-derived stack | ~57 | operator 35, second-designer 19 |
| 2 | lojix / horizon / CriomOS | ~13 | system-designer 7, system-operator 4 |
| 3 | cloud + deployment | ~10 (mostly forward) | system-operator 156-160 → cloud lanes |
| 4 | persona runtime / spirit upgrade | ~48 | operator ~21, second-designer 23 |
| 5 | workspace / Pi / nota / misc | ~38 | Pi-harness 13, nota-designer 7 |

## System-designer-lane drops — EXECUTED (this dispatcher's own lane)

I dropped 8 verified-stale reports (each substance-migrated; reviewed the sub-report reasoning + confirmed the landing before deleting). Collapses system-designer 17 → 9:

| Dropped | Substance landed |
|---|---|
| `26` lean-rewrite shape analysis | repos/lojix + repos/horizon per-repo INTENT; superseded by /40 |
| `27` nota-mixed-enum support | INTENT.md §three-schema-types (enum support landed in schema) |
| `28` lojix vision-gap audit | /40 + /42; audited a retired lane (system-specialist/154) — doubly stale |
| `29` lean-horizon cluster data-shape | INTENT.md §schema-driven-stack + /41 |
| `30/` horizon-lojix low-level migration | /40 (feasibility) + /37 (schema-deep pilot) |
| `31` audit of cluster-operator/7 pi-harness | Pi-harness topic retired; historical |
| `36` criomos-reconciliation audit | /40 (substrate-direction) + INTENT.md §two-deploy-stacks |
| `38` source-staging prototype audit | /40 + /41/3 + /39 (3-track convergence resolved) |

**KEPT (the current arc):** `34/` (active bead queue — production-realities /40 defers TO it), `35/` (schema-deep design), `37/` (schema-deep pilot), `39/` (cross-crate import), `40/` (port feasibility — load-bearing verdict), `41/` (Horizon concept — now finished + verified), `42` (/167 divergence audit), `43` (/168 review), `44/` (this sweep).

## Per-lane handoffs (the lanes apply these on their next maintenance)

I did NOT execute these — each lane owns its own drops. The recommendations live in the sub-reports.

- **operator** — the heaviest: ~56 of 67 reports stale (35 schema-stack era-1 + ~21 the Spirit v0.1→v0.3 deploy-event chain, all absorbed into INTENT.md + the spirit upgrade landing). Collapses to ~11.
- **second-designer** — ~42 of 45 stale (schema audits + persona-runtime). Collapses to ~3.
- **system-operator** — ~9: lojix (162, 163, 165 clean; 164 forward-then-drop) + the cloud-foundation reports (156-160 forward to the cloud lanes) + DJI-mic dedup (drop 161, keep 166).
- **cluster-operator** — ~2 (lojix-daemon-state `4`; `1` update-authority is keep-or-migrate, a §3a design-rationale check).
- **cloud-operator / cloud-designer** — current; `cloud-operator/11` is the newest canonical lojix/horizon cross-cutting read (KEEP).

## Surfaced to the psyche (carry-uncertainty — your call)

1. **Two full lane-retirement candidates.** `nota-designer` (all 9 reports stale — the NOTA-string work shipped into the AGENTS.md hard override + INTENT.md) and `third-designer` (all 8 stale, quiet since 05-24). `second-operator` empties entirely. Per `skills/context-maintenance.md` §"Retiring a lane", retiring an identifier is gated on its memories finding homes — which this sweep does. Whether to retire these lanes is a psyche decision (record 920 lane-shape governance).
2. **`designer/386/` (the PRIOR cross-lane sweep) should retire** — this sweep (`/44`) supersedes it (re-ranks all lanes by topic, re-issues the handoffs). It's designer-owned, so it's a handoff to the designer lane to drop; flagged so two cross-lane-sweep meta-dirs don't linger (the exact staleness you flagged). The designer lane already ran its own drop today (designer/415, 42→15) — so designer is otherwise current; don't re-action it.
3. **Aging psyche-review flags.** `designer/351` + `352` carry psyche-review items now pending across three sweeps (designer/415 already recommended surfacing them). They need a psyche decision to either resolve or park as architecture "Possible features."

## Result

system-designer: 17 → 9 (under the 12 cap). The other over-cap lanes (operator 67, second-designer 45, system-operator 21) have their drop lists ready as handoffs — when applied, operator → ~11, second-designer → ~3, system-operator → ~12. No substance dropped without a verified permanent landing (INTENT.md, per-repo INTENT, the era-2 canonical reports). The "stale reports don't linger" goal is met for this lane and queued for the rest.

## See also

- `0-frame-and-method.md` — frame, inventory, method.
- `1-schema-derived-stack.md` / `2-lojix-horizon-criomos.md` / `3-cloud-and-deployment.md` / `4-persona-runtime-spirit-upgrade.md` / `5-workspace-pi-nota-and-misc.md` — the per-topic aggregations with per-report drop/forward/migrate/keep + owning lane.
- `skills/context-maintenance.md` — the discipline (topic-recency §2, the §3a design-rationale guard, dispatcher-executes-own-lane-only, lane retirement).
- `INTENT.md` §"schema-driven stack" — the permanent landing that makes the schema-stack piles retireable.
