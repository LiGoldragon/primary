# 4 — Topic: persona components + runtime + spirit deployment + upgrade (cross-lane)

*Cross-lane topic aggregation per `skills/context-maintenance.md` §2.
The older persona-component arc: the triad (daemon + working signal +
policy signal), persona-engine, persona-mind / persona-orchestrate
replacements, the Spirit deployment chain (v0.1 → v0.2 → v0.3 cutover),
the version-handover + database-upgrade mechanism. Threads operator
(150-191), second-designer (142-163, 172-189), second-operator (184,
186). Almost all of it is **2026-05-22→25 event/foundation work** that
the schema crystallization (2026-05-25→28) then re-grounded.*

## The arc in one line

This is the "before schema-at-heart" runtime work. Two sub-threads:
(1) **persona-architecture + mind/orchestrate replacement** (second-
designer 142-163) — the design pulse for replacing beads with persona-
mind and tools/orchestrate with persona-orchestrate; and (2) the
**Spirit deployment + version-upgrade mechanism** (operator 158-191,
second-designer 172-189, second-operator 184/186) — building version-
handover, upgrade signals, and cutting Spirit from v0.1 → v0.3 live.
Both threads are now mostly historical: the upgrade mechanism is
**schema-derived** (INTENT.md §schema-emitted-Rust: upgrade is a
generated behaviour, "encode/decode, upgrade, mail-event hook"), and
Spirit is live at v0.3 with its architecture in `repos/persona-spirit/
INTENT.md` + `skills/spirit-cli.md`.

## Recency rank (newest canonical at top)

**Current surface (KEEP):**

1. `system-operator/168` (05-28) — Spirit signal-surface bad-pattern
   audit (the live production query surface). **KEEP — newest Spirit
   report; it's an audit of the LIVE v0.3 surface, the current state.**
2. `second-designer/176` (05-25) — upgrade-mechanism soup-to-nuts.
   **KEEP-as-§3a-guard-OR-MIGRATE — this is the comprehensive "show me
   every part" upgrade design (intent 545). If the schema-derived
   upgrade has fully absorbed it into INTENT.md §schema-emitted-Rust +
   skills, it migrates; until then it's the canonical upgrade-mechanism
   reference. Recommend the second-designer agent decide. Note 175
   (upgrade-mechanism full design) is the predecessor of 176 — 176
   supersedes 175.**

**Stale band (drops, by lane):**

### operator — persona / version / spirit-deployment chain

| Report | Date | Note | Recommendation |
|---|---|---|---|
| `150` triad signal/sema migration current-state | 05-22 | Already self-supersedes 137-149; a consolidation handoff, now itself superseded by the schema-stack re-grounding (INTENT.md §three-schema-types) | DROP |
| `157` version-projection refresh + question rollover | 05-22 | Rollover report; questions resolved by the upgrade design (second-designer/176) + schema-derived upgrade | DROP |
| `158` version-handover foundation impl | 05-22 | Foundation impl; version-projection/handover now schema-derived | DROP — INTENT.md §schema-emitted-Rust |
| `159` persona-engine upgrade foundation | 05-22 | Foundation impl, superseded by schema-derived upgrade | DROP |
| `160` spirit smart-handover sandbox test | 05-22 | Point-in-time sandbox test; superseded by the v0.3 live cutover (191) | DROP |
| `161` spirit private-handover socket | 05-22 | Socket impl; superseded by 191 (live) + system-operator/168 (current surface) | DROP |
| `162` persona owner-version handover authority | 05-22 | Owner-authority design; absorbed into component-triad (owner-signal) — INTENT.md + skills/component-triad.md | DROP |
| `163` persona systemd component-management position | 05-22 | systemd-management position; superseded — component management settled | DROP |
| `164` operator refresh-audit + meta-overhaul context | 05-23 | Refresh/orientation report (ephemeral by nature) | DROP |
| `165/` bead-fix + subagent-wave | 05-23 | Bead-fix + orientation; ephemeral | DROP |
| `166` sema-upgrade + schema-macro current-state | 05-24 | Current-state snapshot superseded by the schema-stack surface (operator/219-222) | DROP |
| `167` recent-reports + intent refresh | 05-24 | Refresh/orientation; ephemeral | DROP |
| `168` latest-design-intent + bead orientation | 05-24 | Orientation; ephemeral | DROP |
| `169` post-318 refresh + next-work | 05-24 | Refresh/orientation; ephemeral | DROP |
| `178` primary-wdl6 spirit v0.1.0 protocol build | 05-25 | v0.1.0 build event; superseded by v0.3 (191) | DROP |
| `186` spirit-next description-only impl | 05-25 | v0.x feature event; in live v0.3; system-operator/168 audits the live surface | DROP |
| `187` spirit v0.2.0 side-by-side deployment | 05-25 | Deploy event; superseded by v0.3 cutover (191) | DROP |
| `188` spirit timestamp-preserving migration | 05-25 | Migration event; done; superseded by 191 | DROP |
| `189` spirit v0.2 live cutover | 05-25 | Cutover event; superseded by v0.3 cutover (191) | DROP |
| `190` audit spirit-docs + multi-topic | 05-25 | Doc audit; superseded by the live v0.3 multi-topic deploy (191) + system-operator/168 | DROP |
| `191` spirit-next multi-topic deployment (v0.3 cutover) | 05-25→26 | The v0.3 cutover event itself. Now the **live state** is the baseline; the cutover is done. system-operator/168 audits the live surface. | DROP — cutover complete; live state is the baseline, not this event log |
| `205` spirit-next schema pilot impl | 05-26 | The schema pilot designer/406 + operator/221 built on | FORWARD-or-DROP (also flagged in schema sub-report) |

**~21 operator reports** DROP in this topic (150, 157-169, 178,
186-191; +205 forward-or-drop). These are nearly all **deploy-event
logs and orientation/refresh reports** — by nature historical once the
event lands. The Spirit deployment chain (158-191) is the textbook
example: each report is a step in cutting Spirit v0.1→v0.3 live; with
v0.3 live and audited (system-operator/168), the step-logs retire and
the architecture lives in `repos/persona-spirit/INTENT.md`.

### second-designer — persona-architecture + mind/orchestrate

| Report | Date | Note | Recommendation |
|---|---|---|---|
| `142` persona engine-manager triad re-audit | 05-21 | Pre-schema triad re-audit; triad shape now in skills/component-triad.md + INTENT.md | DROP |
| `144` persona introspect design review | 05-21 | Introspect design; superseded by schema-derived runtime | DROP |
| `145` real-time intent-recording system design | 05-21 | Intent-recording = Spirit, now live; design superseded by deployed Spirit | DROP — skills/intent-log.md + spirit-cli.md |
| `146` persona-orchestrate lane management | 05-21 | Lane-mgmt design; orchestrate protocol now in orchestrate/AGENTS.md + skills/role-lanes.md | DROP |
| `147` lane-registry test proposal | 05-21 | Proposal; superseded by the role-lanes mechanism | DROP |
| `148` real-time speech-recognition research | 05-21 | STT research; same topic as system-operator/1-2 (whisrs) — historical research | DROP (or keep one STT research report; see note) |
| `150` agent identity + runtime functions | 05-22 | Pre-schema runtime-functions design; superseded by schema-derived runtime (INTENT.md Pattern B/C) | DROP |
| `151` mind + orchestrate replacement readiness | 05-22 | Readiness pulse; persona-mind destination now stated in INTENT.md §BEADS-transitional; readiness moment passed | DROP — INTENT.md §"BEADS is transitional" |
| `159/` intent-manifestation | 05-23 | Intent-manifestation pass; substance landed (the manifestation reports are droppable by construction, cf. designer/415's same finding) | DROP |
| `160` persona-prefix removal coordinated rename | 05-23 | Rename executed; the rename is done | DROP — naming settled |
| `161/` design-cascade + context-sweep | 05-24 | Context-sweep design; superseded by skills/context-maintenance.md (record 921) | DROP — skills/context-maintenance.md |
| `162/` contract-repo lens + consolidation | 05-24 | Contract-repo design; now in skills/contract-repo.md | DROP — skills/contract-repo.md |
| `163` signal+sema interaction + spirit architecture | 05-24 | Signal/sema interaction; superseded by INTENT.md §three-schema-types + §Nexus-mail-keeper | DROP |
| `166` self-audit | 05-24 | Self-audit (ephemeral reflection) | DROP |
| `167/` mvp-advance-and-fix | 05-24 | MVP-advance work; superseded by the schema-stack MVP surface | DROP |

**15 second-designer reports** DROP. Note `145` (intent-recording) and
`146`/`147` (lane mgmt) describe systems that **shipped** (Spirit, the
role-lanes mechanism) — their substance is in skills/permanent docs.

### second-designer — upgrade + orchestrate-port design

| Report | Date | Note | Recommendation |
|---|---|---|---|
| `172/` design-mockup-dispatch | 05-24 | Mockup-dispatch method; now in skills (mockup-on-worktree, records 502-504) | DROP — skills |
| `173` orchestrate port to schema-engine + no-downtime upgrade | 05-24 | Orchestrate-port design; superseded by the schema-derived upgrade + second-operator/186 (impl) | DROP |
| `174` worktree-audit + rework | 05-25 | Worktree-audit; worktree discipline now in AGENTS.md (record 515) + skills | DROP |
| `175` upgrade-mechanism full design | 05-25 | Predecessor of 176 (soup-to-nuts) which supersedes it | DROP — superseded by 176 |
| `177` orchestrate-upgrade end-to-end test | 05-25 | E2E test event; the upgrade is schema-derived now | DROP |
| `178` audit second-operator/186 orchestrate-upgrade socket | 05-25 | Audit of second-operator/186 (dropping) | DROP — target retires |
| `181` counter-ego MVP leans | 05-25 | Counter-ego audit-lean; pattern noted for skill migration (see schema sub-report) | DROP |
| `186` audit designer/336 leans on 27 questions | 05-25 | Audit of designer/336 (already retired in designer/394 sweep) | DROP — target gone |

**8 more second-designer reports** DROP. (Combined with the 15 above
and the 19 in the schema sub-report, this clears nearly the entire
second-designer backlog — leaving 176 as the one keep-or-migrate.)

### second-operator — orchestrate-upgrade

| Report | Date | Note | Recommendation |
|---|---|---|---|
| `184` orchestrate short-header ingress impl | 05-25 | Ingress impl; superseded by schema-derived signal headers (INTENT.md §signal-protocol) | DROP |
| `186` orchestrate upgrade-socket + Mirror wire | 05-25 | Upgrade-socket impl; superseded by schema-derived upgrade | DROP — INTENT.md §schema-emitted-Rust |

**2 second-operator reports** DROP. (With second-operator/190 in the
schema sub-report and /191 in the workspace sub-report, this empties
the second-operator lane entirely — consistent with the prior sweep's
finding that the lane goes empty after migration.)

## Note on STT research duplication

`second-designer/148` (real-time speech recognition) and
`system-operator/1`+`/2` (whisrs durable-first STT + persona speech
brainstorm) are the same STT-research topic, all 2026-05-17→21,
historical. If any STT work is live it should consolidate into one
report or a per-repo INTENT; otherwise all three retire. Flagged
across both lanes.

## Stale-flag count for this topic

**~48 reports** flagged stale: operator ~21, second-designer 23
(15 persona-arch + 8 upgrade/orchestrate), second-operator 2, plus the
STT trio. The Spirit-deployment event chain (operator 158-191) and the
persona-architecture design pulse (second-designer 142-163) are the two
big historical piles. Backed by `repos/persona-spirit/INTENT.md` +
`skills/spirit-cli.md` + `skills/component-triad.md` +
`skills/contract-repo.md` + `skills/role-lanes.md` + INTENT.md
§schema-emitted-Rust / §BEADS-transitional / §three-schema-types.

## Drop ownership by lane (handoff)

- **When `operator` next does maintenance, the persona/spirit/upgrade
  drops it owns are:** 150, 157, 158, 159, 160, 161, 162, 163, 164,
  165/, 166, 167, 168, 169, 178, 186, 187, 188, 189, 190, 191 (~21).
  Borderline: 205 (forward-or-drop, shared with schema topic). The
  Spirit deploy-event chain (158-191) retires as a block — v0.3 is live
  and audited.
- **When `second-designer` next does maintenance, the persona/upgrade
  drops it owns are:** 142, 144, 145, 146, 147, 148, 150, 151, 159/,
  160, 161/, 162/, 163, 166, 167/ (persona-arch, 15) + 172/, 173, 174,
  175, 177, 178, 181, 186 (upgrade/orchestrate, 8) = 23. KEEP-or-
  MIGRATE: 176 (upgrade soup-to-nuts — the comprehensive reference;
  migrate to INTENT.md/skills or keep until schema-derived upgrade
  fully absorbs it). Combined with the schema sub-report's 19, this
  clears the second-designer backlog to ~1-3 survivors.
- **When `second-operator` next does maintenance, the persona/upgrade
  drops it owns are:** 184, 186. With 190 (schema) + 191 (workspace),
  the lane empties.
- **system-operator/168** (Spirit signal audit, current) — KEEP.
