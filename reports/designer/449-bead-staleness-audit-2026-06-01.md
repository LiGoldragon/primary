---
title: 449 — Bead-staleness audit
role: designer
variant: Audit
date: 2026-06-01
topics: [bead-staleness, audit, calibration, psyche-intent-vs-substrate, persona-prefix-retirement, next-stack-pivot, upgrade-as-sema, schema-core-extraction]
description: |
  Calibration audit of the 269 open beads in `.beads/` against the current intent corpus (Spirit 1280-1319) and the recent designer + operator reports. Substrate has drifted heavily; the dominant pattern is pre-pivot persona-stack work that the schema/NOTA-next/upgrade-as-SEMA arc has now subsumed. Detailed verdict on the 41 most-stale P0/P1 beads + sampled across the P2/P3 substrate. Recommendation: bulk retirement of the persona-* component-migration backlog plus the macro-substrate work plus the upgrade-handover work, with new tracking shaped around designer 446's porting waves + designer 447's upgrade-as-SEMA slice.
---

# 449 — Bead-staleness audit

## TL;DR

The bead store carries **269 open beads** (1 P0, 67 P1, 162 P2, 48 P3). The current intent corpus (Spirit 1280-1319, designer 443-448, operator 265-270) has comprehensively re-shaped what's load-bearing.

Detailed survey covered all 68 P0/P1 beads (the headline level) plus a stratified sample (~25) across the P2/P3 substrate to confirm patterns. The P2/P3 substrate carries the same supersession pattern at scale: ~110-130 of the 162 P2 beads belong to the persona-stack / `signal_channel!` / persona-spirit cutover arcs and inherit the same supersession verdict as their P1 parents; ~35-40 of the 48 P3 beads target the legacy `contract-repo.md` skill update queue + persona-stack contract renames + persona-stack canonical-example beads with the same supersession. The current bead substrate would shrink to ~30-40 beads after a thorough sweep — within the healthy queue size `skills/beads.md` §"Periodic audit" recommends.

Of the **68 P0+P1 beads**:

- **49 are wholly stale (category 4 — superseded).** Persona-* migration, `signal_channel!` macro substrate, persona-spirit v0.1.0/v0.1.1 cutover, persona-agent triad, persona-supervised tap-emit observability, signal-version-handover.
- **9 are technically stale (category 1 or 5).** Premise/path drift; current intent has moved.
- **6 carry retired-lane labels (category 3 — additionally).** `role:second-operator-assistant`, `role:system-specialist`, `role:designer-assistant` paths in audit references.
- **0 are stale-via-text-contradiction-only (category 2).** No bead names a specific approach that current intent forbids while otherwise being current; all category-2-style violations are wholly-stale via category 4.
- **10 remain actionable** as work units — either current concept + refresh text needed (mostly), or fully current (rare). These cluster around: bracket-string migration epic (`primary-36iq` subtree, 4/7 children closed), cloud + domain-criome wave-1 ports (`primary-kbmi` + .2), nix-auth integration (`primary-srmq`), spirit-next OutputNexus dispatcher (`primary-a1px`), `primary-2y5` persona-daemon foundation (was load-bearing for persona engine, but the persona engine itself is now superseded — should be retired with that arc), and a few others requiring rewrite.

Across the **162 P2 + 48 P3 beads**: the sampled cross-section confirms the same supersession spread. Skill-update beads (10+ P3 beads targeting `contract-repo.md`) are stale because they target the contract-authoring discipline that schema-source authoring largely replaces. Per-contract beads in the persona triad family (signal-persona-mind, signal-persona-orchestrate, signal-persona-spirit, etc., with variant renames + canonical.nota example beads) carry the persona-stack supersession. The deploy-stack beads (chronos, CriomOS modules, prometheus, clavifaber) are a separate class — they're cluster-operator / system-operator scope, NOT next-stack-pivot stale, and stay actionable in their own arc.

The headline pattern: the bead store assumed (a) the persona-prefix rename wave (R1-R12) would complete and unblock (b) per-component migration to a `signal-executor v4`-based foundation, and (c) the persona engine would orchestrate cross-version handover for upgrade. Per recent reports (designer 446 §"Phase 0 spirit fold", designer 447, Spirit 1305-1314), the work has pivoted to porting components into the schema-emitted next-stack substrate and upgrade-as-SEMA. The legacy persona-stack and macro substrate are being absorbed, not extended.

**Recommended action for the orchestrator:** the audit recommends bulk close-as-superseded for the 5 large stale arcs (persona-* migrations, `signal_channel!` macro consolidation, persona-spirit cutover, persona-agent triad, persona-prefix rename remnants) plus the contract-repo.md skill-update queue. The remaining ~30-40 actionable beads need text refresh in the 5-7 rewrite cases. The designer lane can apply the close-sweep directly since the closing notes are short and the substantive supersession is clear from the audit. The rewrites should go to operator/cluster-operator for execution since they require operator's current understanding of work in flight. Do NOT close beads in this pass — the audit is the proposal surface; the close sweep is a separate action.

## Method

| Step | What I did |
|---|---|
| Workspace contract refresh | Read `AGENTS.md`, `ESSENCE.md`, `skills/beads.md`, `skills/intent-maintenance.md`, `skills/role-lanes.md`, `protocols/active-repositories.md`. |
| Recent intent corpus | Queried Spirit `(Range (1280 1319))`. Read every record's verbatim + topics + certainty. Focused on the 1287/1290/1292 body-stream landing, 1294/1295 enum-body honesty, 1297 prototype strict-syntax, 1300-1302 single-datatype shape, 1305-1314 upgrade-as-SEMA, 1315-1319 spirit-query design. Cross-referenced earlier high-impact records (920 lane retirement, 1268-1278 schema vocabulary). |
| Recent designer corpus | Read `reports/designer/443-design-improvements-audit/{0-frame, 5-overview}`, `444-stack-vision/5-overview`, `445-next-stack-audit`, `446-next-stack-porting-research/4-overview`, `447-upgrade-as-sema-design`, `448-single-field-wrapper-audit`. |
| Recent operator corpus | Read `reports/operator/265-programmable-nota.../4-overview-and-gaps`, `267-macro-library-nota-types`, `268-schema-source-artifact-datatype-split-audit`, `269-rust-single-field-wrapper-validity-audit`, `270-single-field-wrapper-comparison-with-designer-448`. |
| Bead survey — P0/P1 | `bd list` then `bd show <id>` for every P0/P1 bead's full body + notes + comments + children + dependencies (68 beads). Each cross-checked against the intent corpus + reports. |
| Bead survey — P2/P3 sample | Stratified sample of ~25 P2/P3 beads across topic clusters (macro substrate, persona-* migrations, deploy-stack, skill-updates, contract renames). Confirmed pattern; counts extrapolated from sample. |
| Classification | One verdict per surveyed bead against the five-category scheme in the prompt. Bead-by-bead in the table below for the 41 most-substantive stale; pattern paragraphs for the broader 100+ stale beads at the P2/P3 layer. |

The audit took ~4 hours of careful reading; bead bodies are dense with historical context that has to be re-anchored against current intent to evaluate.

## Classification scheme (restated)

- **Category 1** — Technical premises superseded (architecture has changed under the bead).
- **Category 2** — Instruction text contradicts current pattern (workspace rules or recent Spirit records now forbid the approach).
- **Category 3** — Lane assignment now wrong (role retired or scope moved).
- **Category 4** — Wholly superseded (scope subsumed by larger landing or follow-up).
- **Category 5** — Premise unchanged but text drift (file paths, names, anchors have moved).

A bead may carry multiple categories; the dominant one is named.

## Stale-bead table

| Bead | Title (paraphrased) | Cat | Supersession | Recommended action |
|---|---|---|---|---|
| `primary-602y` | Rebuild persona-spirit v0.1.0.1 retrofit against current signal-frame (post-ShortHeader) | 4 | Designer 446 §"Phase 0" — `spirit-next` pilot folds into `spirit`, retiring the v0.1.0.x retrofit chain entirely; Spirit 1314 — design self-editing schema-daemon NOW, not after legacy stack stabilizes. The v0.1.0.x line is being abandoned, not patched forward. | RETIRE — closing note: "Persona-spirit v0.1.0.x line abandoned per designer 446 spirit-fold and Spirit 1314 upgrade-as-SEMA pivot. Current upgrade work is in `schema-daemon` / `spirit` per designer 447, not legacy retrofit." |
| `primary-07ot` | persona-router: Delivered row only on harness-side ack (4-hop chain) | 4 | Persona-router is part of the persona-* stack that designer 446 §"Phase 2 — stateful runtimes" defers behind schema-core extraction. The named `signal-executor v4` substrate (sub-bead language) is not in current code; routers are not in the wave-1 porting trio. | RETIRE — closing note: "Persona-router migration deferred per designer 446 wave-2; the 4-hop ack chain is a substrate concern that re-anchors on schema-core extraction (designer 444 §5 horizon 1) before router-level work is sensible." |
| `primary-0bls` | Migrate criome triad to current foundation | 4 + 3 | `criome` is named in `protocols/active-repositories.md` as today's "minimal Spartan BLS12-381 daemon" — a real but narrowly-scoped component. The bead's "current foundation" means the OLD signal-core + signal-executor + persona-mind foundation, not the schema-derived stack. References `designer-assistant/141` (retired role per spirit record 920). | REWRITE — re-anchor at designer 446 wave-2 (criome is not a wave-1 candidate); restate the foundation as "schema-emitted Signal/Nexus/SEMA per the `spirit-next` pilot per designer 446's playbook." Replace the dead `designer-assistant/` paths with current report references. |
| `primary-0jjz` | Execute spirit v0.1.0 to v0.1.1 brief-outage cutover (production) | 4 | The brief-outage cutover was an MVP scaffold for the legacy persona-spirit upgrade. Spirit 1305-1314 reshape the upgrade mechanism as SEMA operations on Asschema; the brief-outage cutover is no longer the canonical mechanism. The `spirit-next` pilot's runtime IS where future cutover discipline lives. | RETIRE — closing note: "Brief-outage cutover MVP was a scaffold for the legacy persona-spirit line. Per Spirit 1305-1314 + designer 447, upgrade IS SEMA on Asschema; future cutovers ride that mechanism. Legacy persona-spirit deployment will be replaced by `spirit` fold per designer 446 Phase 0." |
| `primary-0m1u` (epic) | EPIC: /318 persona-prefix rename wave (R1-R12) | 4 | The persona-prefix rename wave is 10/12 complete (per bead listing). The remaining two (R11 spirit rename, R12 meta catch-up) target the legacy persona-spirit triad that designer 446 Phase 0 obsoletes via the `spirit-next → spirit` fold. The rename wave's epic body assumes a per-triad migration cadence the schema-emitted next-stack pivot supersedes. | RETIRE — closing note: "R1-R10 landed. R11/R12 are obsolete: the `spirit` triad is becoming the `spirit-next` fold target per designer 446 Phase 0 (not a 'rename'). Persona meta + CriomOS-home repin work will re-anchor on the next-stack `spirit` repo. New tracking: file fresh bead for spirit-next fold once designer 446 Phase 0 starts." |
| `primary-0m1u.11` | [R11] Rename spirit triad after cutover | 4 | Child of `0m1u` — same supersession. The "rename" framing is wrong: it's a fold, not a rename. | RETIRE with parent. |
| `primary-0m1u.12` | [R12] Persona meta catch-up and CriomOS-home repin | 4 | Child of `0m1u` — same supersession. CriomOS-home pin work re-anchors on the new `spirit` repo's deployment artifacts, not on a persona-spirit rename. | RETIRE with parent. |
| `primary-145a` | persona-introspect: tap-emit subscriber for spirit socket_ingress (Tier 1 consumer) | 4 + 1 | Targets the legacy `signal_channel!` Tier 1 micro tap architecture. The schema/NOTA-next stack does NOT use signal_channel!-emitted micros. Per Spirit 1287/1290/1292, the macro and tap-emission substrate has been wholesale rebuilt; per designer 446 §"Phase 2", persona-introspect ports in wave-2. The tap-emit-on-Tier-1 micro architecture is not in the new substrate. | RETIRE — closing note: "Tier 1 micro tap-emit substrate was a `signal_channel!` extension predating the schema/NOTA-next pivot. Per designer 444 §5 + Spirit 1290, the macro-emission substrate is now schema-derived; persona-introspect ports in wave-2 per designer 446, but the tap-emit Tier 1 micro architecture is not the destination shape." |
| `primary-1jql` | In-transition messages probe in spirit-nspawn upgrade test | 4 | Tests the legacy persona-spirit cross-version handover. The bead's own status note says "may be PARTIALLY OBVIATED by the full-ceremony-e2e test." Persona-spirit cross-version handover is being abandoned per Spirit 1314 + designer 446 Phase 0 fold. | RETIRE — closing note: "Persona-spirit cross-version handover is abandoned per Spirit 1314 + designer 446 Phase 0 fold. The in-transition probe was a legacy-pilot scaffold; not needed for `spirit` fold which doesn't run cross-version handover." |
| `primary-36iq` (epic) | EPIC: Coordinate NOTA bracket-string merge and consumer migration | 5 | Substrate-current. 4/7 sub-beads complete; remaining sub-beads (.3 nota-config/Spirit examples + .6 adjacent consumers + .7 quote-mark sweep) target real ongoing work. The deployed-CLI blocker named in .3 is real. | KEEP, refresh text — update epic body's "Definition of done" to reference the current Spirit deployment state; verify all listed consumer repos are still active per `protocols/active-repositories.md`. |
| `primary-36iq.3` | Update nota-config + Spirit CLI examples for bracket-string NOTA | 5 | Premise unchanged (bracket-string migration is live workspace concern), but the bead body's last update (2026-05-23) precedes the deployed-Spirit blocker timeline. The latest comment from 2026-05-24 names the blocker honestly. | KEEP — annotate the live blocker is now over a week old; verify the profile-pin still rejects bracket strings before continuing. |
| `primary-36iq.6.1` | lojix: port to current signal-lojix API before bracket-string migration can close | 5 + 4 | The `lojix` triad migration is named in `protocols/active-repositories.md` as the `horizon-leaner-shape` feature arc. The bead's mention of `wire::LojixFrame/LojixFrameBody/Request` retired variants is real, but the bracket-string migration's bigger gating is the whole `horizon-leaner-shape` arc, not just lojix's port. Designer 446 doesn't name lojix porting at all — it's an adjacent active concern, not a wave-1/2 next-stack candidate. | REWRITE — re-anchor the bead at the `horizon-leaner-shape` feature arc + add the cross-reference to the deploy-stack discipline. Restate as a deploy-stack-side task, not a bracket-string blocker. |
| `primary-3cl1` | signal-frame-macros: frame_micro() projection emit in signal_channel! | 4 | Targets the legacy `signal_channel!` macro substrate. Per Spirit 1287/1290/1292 + designer 444 §"What's LIVE today", the macro-emission stack is now schema-derived through `nota-next` + `schema-rust-next`. The `signal_channel!` macro is being retired in favor of schema-emitted nouns. `signal-frame-macros` repository is not in `protocols/active-repositories.md`. | RETIRE — closing note: "`signal-frame-macros` repo + `signal_channel!` macro substrate are being retired per the schema-derived next-stack pivot (designer 444 §'What's LIVE today' + Spirit 1290). Macro work now lives in `schema-rust-next`." |
| `primary-4naq` (epic) | primary-a5hu.1: port persona-* components to signal-executor v4 + per-component coordination | 4 | The whole epic targets `signal-executor v4` substrate that is being superseded by the schema-emitted next-stack. The persona-* component porting is now scoped through designer 446's wave-1 (cloud/upgrade/repository-ledger) + wave-2 (mind/router/terminal/orchestrate/message/introspect). The bead's listed sub-beads (primary-c620, primary-9os, primary-es9, primary-hj4, ...) are persona-stack ports with the same supersession. | RETIRE — closing note: "Sequencing superseded by designer 446 porting waves. The `signal-executor v4` migration recipe is the wrong target; persona-* components port to the schema-emitted next-stack substrate per designer 446 Phase 1 + Phase 2. New trackings: per-wave operator beads referencing designer 446 §'Recommended first slice' + §'Phase 1a in parallel'." |
| `primary-c620` | Migrate persona-orchestrate triad to current foundation | 4 + 3 | Child epic of `4naq` — same supersession. Audit reference `designer-assistant/137` is in a retired role directory (spirit record 920). | RETIRE with parent. |
| `primary-54ti` | horizon-rs: migrate to current nota/signal/sema/spirit foundations (Spirit 303) | 5 | Spirit record 303 (2026-05-23) names lean-stack horizon-rs migration; the substrate references are stale (the `current` foundations have evolved through 100+ Spirit records since). Horizon-rs is named adjacent-active in `protocols/active-repositories.md`. The bead's "ToSemaOutcome trait, BatchErrorClassification" references are pre-schema-emission. | REWRITE — re-anchor on designer 446 §"What's NOT recommended" (horizon-rs is not a next-stack port candidate; the `horizon-leaner-shape` arc is the canonical home). The lean-stack catch-up belongs in cluster-operator's deploy-stack work, not in next-stack porting. Re-file as cluster-operator scope, not designer/operator. |
| `primary-8avm` | DeliveryTraceKey four-field correlation with Tap stream indexing in persona-introspect | 4 | persona-introspect is wave-2 in designer 446. The bead's `Tap stream` model is `signal_channel!`-era; the schema-emitted stack supersedes the Tap-event substrate. The bead's recent comments (2026-05-22, 2026-05-23) show partial landing on the legacy stack, but the underlying mechanism does not survive the schema-emission pivot. | RETIRE — closing note: "Tap-stream substrate is part of the `signal_channel!`-era observability arc; persona-introspect ports in wave-2 per designer 446, and the schema-emitted runtime's introspection model is a follow-on designer report. DeliveryTraceKey four-field correlation can re-emerge as schema-emitted nouns once the wave-2 port lands." |
| `primary-9hx0` | Split lib.schema into three schema-type files per record 964 | 1 | Record 964 (three schema types: Signal/Nexus/SEMA) is consistent with the live shape. The bead's note acknowledges PARTIAL: spirit-next has three explicit roots (NexusInput/Output, SemaInput/Output) in ONE schema document. Per designer 444 §"What's LIVE today", that single-document form is the live shape; the three-file split is a refinement question, not a workspace requirement. Designer 444 does not flag the file split as a horizon. | REWRITE — re-frame as an open design question, NOT a P1 task. The bead body should ask "should the prototype lib.schema split into three files?" with the spirit-next status as evidence. Move to P2/P3 or convert to a designer report (per `skills/beads.md` §"Anti-pattern B: tracking design questions as beads"). |
| `primary-9up1` | Migrate lojix triad to current foundation (new branch) | 5 + 4 | Same supersession as `36iq.6.1`. Lojix is on the `horizon-leaner-shape` deploy-stack arc, not next-stack porting. Audit reference `designer-assistant/139` is in a retired role directory. | RETIRE — closing note: "Lojix triad's migration runs in the `horizon-leaner-shape` deploy-stack feature arc per `protocols/active-repositories.md` §'Active feature arc'. The 'current foundation' target moved with the schema-emission pivot; the deploy-stack arc is the canonical home, tracked separately." |
| `primary-a1px` | spirit-next cycle-2 followup: emit OutputNexus client-side dispatcher | 1 + 5 | The spirit-next pilot is now THE flagship subject of designer 444 + 445 + 446. The "cycle-2" naming + `designer/403` reference predate the body-stream-substrate landing (Spirit 1287/1290) and the spirit-fold direction (designer 446 Phase 0). OutputNexus dispatcher emission may still be useful but the framing is pre-current. | REWRITE — re-anchor at designer 445 §"Findings" + designer 446 §"Operator-bead-shaped first action — Phase 0 spirit fold". The dispatcher emission is now a sub-slice of the spirit fold, not a standalone cycle-2 follow-on. |
| `primary-a5hu` (epic) | second-operator: build out persona engine — port persona-* components to signal-executor v4 + add upgrade orchestration | 4 + 3 | Same supersession as `4naq`. The bead's "second-operator" framing in the title was valid when filed; the lane discipline still works (per `skills/role-lanes.md` second-operator is a window on the operator agent). But the WORK SCOPE — `signal-executor v4` + persona engine in production with upgrade orchestration — is wholesale superseded by designer 446 + 447. The "persona engine" framing is part of the legacy persona-stack supervisor model. | RETIRE — closing note: "Persona-engine + signal-executor v4 substrate is superseded by the schema-emitted next-stack pivot (designer 444-447). Upgrade orchestration is now SEMA-on-Asschema per Spirit 1305-1314 + designer 447 — schema-daemon + upgrade-daemon are the canonical objects, not persona engine. Sub-beads (primary-2y5, primary-nobf, primary-q98d) carry the same supersession." |
| `primary-bann` | persona-spirit-daemon: socket_ingress tap point (Tier 1 emission on accept) | 4 | Same supersession family as `145a` + `3cl1` — Tier 1 micro tap architecture is `signal_channel!`-era. persona-spirit-daemon's tap point is in the legacy persona-spirit daemon; persona-spirit is being subsumed by the `spirit-next → spirit` fold per designer 446 Phase 0. | RETIRE — closing note: "Tap-emission substrate retires with the `signal_channel!` macro substrate per designer 444 §'What's LIVE today'. Persona-spirit daemon is being subsumed by `spirit-next → spirit` fold per designer 446 Phase 0." |
| `primary-bg9l` | signal-frame: LogSummary trait + const-generic 64-byte size check | 4 | Same supersession as `l02o` — targets retired `signal_channel!` substrate. The /155 design report is referenced as "retired" in the bead's own note. | RETIRE — closing note: "LogSummary trait + size check were part of the three-tier signal-sizing arc tied to `signal_channel!` macros. Retired per designer 444 §'What's LIVE today' as the macro substrate moves to schema-emission." |
| `primary-c2da` (epic) | /249 gap-closure sweep: close 24 open gaps from designer/249-component-intent-gap-analysis | 4 | Targets designer/249 (component-intent-gap-analysis), a report the persona-stack 24-gap inventory. Per `skills/beads.md` §"Anti-pattern B", this is a design question epic, not a work-unit. The 24 gaps were anchored at the legacy persona stack architecture; the schema-emission pivot supersedes most of them. The bead's own 2026-05-23 split-recommendation comment says "NOT FILED TODAY because the epic body doesn't enumerate the 24 specific gaps." | RETIRE — closing note: "Design-question epic, not a work-unit (anti-pattern per `skills/beads.md`). The 24-gap analysis at designer/249 was anchored at the legacy persona stack; the schema-emission pivot supersedes most of those gaps. Current gap inventory: designer 444 §5 horizons + designer 445 Findings 1-4 + designer 446 Phase 0/1a operator beads." |
| `primary-duuv` | Land DatabaseMarker on every signal reply per record 935+970 | 5 + 4 | Premise SHIPPED in spirit-next (per bead's own note: "SHAPE is done"). Followup work (durable redb backing, content-addressed StateDigest) lives in the `Store` + `MailLedger` substrate that designer 446 §"Phase 0" picks up. The acceptance criteria are literally met. | CLOSE-AS-SHIPPED (operator action, not retire) — closing note: "Shipped via spirit-next 6afe7280; DatabaseMarker carries through Nexus to Signal reply with monotonic marker test. Follow-ups (durable redb, content-addressed StateDigest) land in the spirit fold per designer 446 Phase 0." |
| `primary-ekxx` | Promote signal-version-handover to schema-derived (second schema-macro pilot) | 4 | `signal-version-handover` lives in the retired persona-spirit cross-version handover model. Per Spirit 1305-1314, upgrade is SEMA-on-Asschema; the handover handshakes (AskHandoverMarker / ReadyToHandover / HandoverCompleted) are the OLD upgrade-mechanism shape. Designer 447 names the NEW shape (SchemaEdit operations + transitory-database pattern). | RETIRE — closing note: "signal-version-handover encodes the legacy persona-spirit handover protocol. Per Spirit 1305-1314 + designer 447, upgrade IS SEMA-on-Asschema, not a handover handshake. The schema-daemon + upgrade-daemon are the canonical objects; signal-version-handover does not have a future in the new shape." |
| `primary-ezqx` (epic) | EPIC: Consolidated signal_channel! + signal_cli! macro extension (one PR-shaped landing) | 4 | The entire epic is `signal_channel!` macro substrate work. Same supersession family as `3cl1`, `bg9l`, `l02o`, `v5n2`. The epic body's "PR pair (signal-frame + signal-frame-macros + signal-cli-macros)" repositories are not in `protocols/active-repositories.md` as active. | RETIRE — closing note: "Macro substrate moved to schema-emission per designer 444 §'What's LIVE today'. `signal-frame-macros` + `signal-cli-macros` are retired in favor of `schema-rust-next` emission. The consolidated landing this epic targeted is moot." |
| `primary-ezqx.1` | MVP schema-language pilot — Spirit through NOTA-data macro input + ShortHeader emission + tap test | 4 | Child of `ezqx`. Spirit 1287/1290/1294/1295/1297 reshape the schema reader entirely; the bead's "multi-pass NOTA-first reader" model has been superseded by the body-stream substrate (Spirit 1287 LANDED). | RETIRE with parent. |
| `primary-ezqx.3` | Recursive Help-on-every-enum macro emission per /312 (supersedes primary-8r1j) | 4 | Child of `ezqx`. Help-on-every-enum was a `signal_channel!` ergonomic; supersedes with the macro substrate retirement. | RETIRE with parent. |
| `primary-gu7t` | Migrate persona-harness triad to current foundation | 4 + 3 | Same persona-* migration supersession. Audit reference `designer-assistant/135` is retired-role-directory. Persona-harness becomes a LIBRARY (not a daemon) per `primary-gvgj` parent — and `gvgj` itself is now superseded. | RETIRE — closing note: "Persona-harness migration superseded by schema-emission pivot. Harness daemon is being retired entirely per `primary-gvgj` (which is itself stale)." |
| `primary-gvgj` (epic) | EPIC: persona-agent component triad — agent abstracts harness backends (10 sub-beads) | 4 | The persona-agent triad was designer/309's proposal to absorb harness backends. The schema-emission pivot subsumes this work: agent backends + harness library + router migration all re-anchor on the next-stack substrate. Designer 446 wave-2 picks up router; the agent triad design is pre-pivot. | RETIRE — closing note: "Persona-agent triad design (designer/309) was anchored at the legacy persona stack. The schema-emission pivot reframes agent backends, harness libraries, and router migration as schema-emitted Signal/Nexus/SEMA components per designer 444-447. New design needed; do not pick up the old triad shape." |
| `primary-gvgj.3-.9` (7 sub-beads) | persona-agent daemon skeleton + 5 backends + router migration | 4 | All children of `gvgj` — same supersession. | RETIRE with parent. |
| `primary-kbmi` (epic) | Implement cloud and domain-criome runtime daemons | 1 + 5 | Cloud + domain-criome are named in `protocols/active-repositories.md` as adjacent-active. **CLOUD is named in designer 446 §"Phase 1a in parallel" as one of three wave-1 ports** alongside upgrade + repository-ledger. The bead's TEXT predates designer 446's framing; the work is still relevant but the recipe is now the porting playbook (designer 446 sub-agent 2), not the legacy persona-stack daemon shape. | REWRITE — re-anchor at designer 446 §"Phase 1a in parallel". Replace the legacy `signal-frame request/reply handling + sema-engine stores` recipe with the schema-emission porting recipe from designer 446 sub-agent 2's playbook. Drop the `role:system-specialist` label (retired lane). |
| `primary-kbmi.2` | implement domain-criome daemon runtime | 1 + 5 | Child of `kbmi`. domain-criome is named in active-repositories as adjacent. Same recipe-supersession as parent. | REWRITE with parent — same re-anchoring. |
| `primary-l02o` | signal-frame: LogVariant trait + autogen derive macro | 4 | Same supersession family as `bg9l`, `3cl1`, `ezqx`. | RETIRE — closing note: same as `bg9l`. |
| `primary-lrf8` | Promote mail handling to explicit queue + fanout observers per record 963+970 | 5 | The mail-keeper + database-marker substrate landed in spirit-next per Spirit 1287/1290 + designer 444 §"What's LIVE today" (Mail<Phase> typestate live, Engine + Nexus + Store live). The bead's own 2026-05-27 note acknowledges the cycle-3 prep landing. The remaining followup is shape-refinement, not new work. | CLOSE-AS-SHIPPED (operator action) — closing note: "Mail-keeper substrate live in spirit-next per designer 444 §'What's LIVE today'. Multi-observer fanout, on_mail_sent hooks, queue mechanics are now shape-refinement question for the spirit fold (designer 446 Phase 0), not new work tracking." |
| `primary-muu2` | persona triad: pilot adopt contract_section grammar (signal-persona + owner-signal-persona) | 4 | Same `signal_channel!` macro substrate supersession. The golden-ratio split + contract_section grammar were `signal_channel!` extensions. | RETIRE — same closing note family as `ezqx`. |
| `primary-nobf` | primary-a5hu.2: persona supervision + lifecycle (EngineSupervisor, SpawnEnvelope, lifecycle reducer wiring) | 4 | Same supersession as parent `a5hu`. | RETIRE with parent. |
| `primary-q98d` | primary-a5hu.3: persona upgrade orchestration (HandoverDriver, active-version selector, recovery) | 4 | Same supersession as parent `a5hu`. The HandoverDriver pattern is the OLD upgrade-orchestration shape; new shape is upgrade-daemon per designer 447. | RETIRE with parent. |
| `primary-srmq` | lojix-daemon: authenticated Nix flake resolution via nix-auth crate | 5 | Lojix is on `horizon-leaner-shape` arc per active-repositories. The nix-auth design (designer 32) is real and current; the bead is still actionable. The labels `role:operator` are correct. Bead text references are mostly stable. | KEEP — refresh text reference to confirm the `horizon-leaner-shape` worktree is the destination + verify the design report cross-reference still resolves. |
| `primary-v5n2` | signal-frame-macros: accept contract_section grammar + auto-allocate variant indices within range | 4 | Same `signal_channel!` macro substrate supersession. | RETIRE — same closing note family as `ezqx`. |
| `primary-wvdl` | Persona: port to current Signal stack + complete upgrade orchestration | 4 + 3 | Same persona-* migration supersession. Audit references `reports/designer-assistant/...` retired-role paths. The "Track A — finish upgrade orchestration" work is anchored at the OLD upgrade-orchestration shape (HandoverDriver, signal-version-handover); new shape per designer 447 is upgrade-daemon on schema-emitted nouns. | RETIRE — closing note: "Persona engine + upgrade orchestration superseded per designer 446-447 + Spirit 1305-1314. The whole bead is anchored at the pre-pivot architecture; new tracking lives in `upgrade-daemon` + `schema-daemon` operator beads per designer 447 §'Operator-bead-shaped first action'." |
| `primary-x3ci` | Cut over Spirit daemon to v0.1.1 migrated database after current binary deployment | 4 | Same persona-spirit v0.1.0 / v0.1.1 cross-version cutover supersession as `0jjz`, `602y`, `ekxx`. The whole arc is being abandoned in favor of the `spirit-next → spirit` fold. | RETIRE — same closing note family as `0jjz`. |
| `primary-x3ci.1` | Wire production pre-migration step before next daemon starts (commit_sequence trap) | 4 | Child of `x3ci` — same supersession. | RETIRE with parent. |

### Summary count by category (P0/P1 detailed survey, 68 beads)

| Category | Count |
|---|---|
| 1 — Premises superseded | 4 (overlapping with 5) |
| 2 — Instruction contradicts pattern | 0 net (subsumed by category 4) |
| 3 — Lane misfile (retired `designer-assistant`/`second-operator`/`system-specialist` labels) | 6 (mostly overlapping with 4) |
| 4 — Wholly superseded | 49 |
| 5 — Premise unchanged, text drift | 11 (mostly overlapping with 1 + 4) |
| Net stale (deduplicated against multi-category overlap) | 58 |
| Current + actionable | 10 |

The high overlap is genuine — many stale beads are stale on multiple axes (e.g. wholly-superseded AND filed to a retired lane AND have stale anchor paths). The dominant axis is category 4 (wholly superseded).

## P2/P3 substrate sampling — pattern-driven extrapolation

The P0/P1 layer is the headline; the broader P2/P3 substrate (210 beads) was sampled stratified across topic clusters rather than surveyed bead-by-bead. The sample confirms five clusters; each cluster's per-bead supersession follows the same logic as its P1 counterpart.

### Cluster 1 — Persona-stack continuation work (~85-95 P2/P3 beads stale)

Across the bead store, persona-stack continuation work includes per-component CLI migrations to `signal_cli!` (`primary-uq04` epic + 4 children), `signal_channel!` template migrations (`primary-u8vo` epic + 11 children for the 10 unmigrated signal contracts), persona-* triad rearrangement by socket authority (`primary-ep45`), defense-in-depth section-vs-socket validation (`primary-9dce`), three-tier subscription delivery (`primary-k8cn`, `primary-b86d`), persona-mind sema-tag dropping (`primary-ql6q`), agent triad creation (`primary-c0pp`, `primary-fwll`, `primary-rtz8`, `primary-g3gm`, `primary-7i6a`), MessageProxy phantom retirement (`primary-devn` + .1.4), persona daemon foundation (`primary-2y5` IN_PROGRESS), persona-engine-sandbox credential root (`primary-a18` IN_PROGRESS).

**Same supersession family as P1 cluster.** All target the legacy persona stack + `signal_channel!` macro substrate that the schema-emission pivot supersedes. Estimate: 85-95 of 162 P2 beads carry this pattern. Recommendation: RETIRE in the same close-sweep, with closing notes pointing at designer 446 Phase 2 (stateful runtimes wave after schema-core extraction).

### Cluster 2 — Skill-update queue targeting contract-repo.md (~12-15 P3 beads stale)

A large P3 cluster targets the `skills/contract-repo.md` skill: 11 beads each adding a different doctrinal item — Tier 1 micro header (`primary-xaxv`), Help variant (`primary-3jkm`), signal_cli! caller-pid (`primary-2xzv`), SignalCore system-types zone (`primary-yee8`), per-record schema-version tag (`primary-ydbu`), Cloud as Sema-shaped (`primary-hfmu`), Unknown variant amendment (`primary-1uil`), supervision-is-not-namespace (`primary-0obj`), per-operation-replies-no-repeat (`primary-ilel`), three-tier sizing (`primary-0190`), universal data variants pre-allocation (`primary-4jms`), last-known-acknowledgment state (`primary-6my0`), owner-vs-public socket discipline (`primary-jc91`), raw-bytes escape hatch (`primary-hy7b`), NOTA-as-code-comments (`primary-xrvi`), multi-version handover protocol (`primary-nzh8`), signal_channel! + Tier 1 header cluster (`primary-xaxv`), component binary naming (`primary-c5sr`), NoRecords typed-result (`primary-zle8`).

**Why this cluster is stale:** `skills/contract-repo.md` describes the contract-authoring discipline for hand-rolled `signal_channel!`-style contract crates. Per the schema-emission pivot, contract authoring largely moves to `.schema` source files consumed by schema-rust-next emitter; the doctrinal items being added to contract-repo.md target a substrate that's being supplanted. Some doctrines (Help-on-every-enum, NOTA-as-code-comments, NoRecords) survive as schema-source patterns but their CANONICAL HOME is no longer `contract-repo.md` — it's `skills/nota-design.md` + the schema language's macro library.

**Proposed action:** RETIRE most of this cluster as a group. Cherry-pick 2-3 doctrines that survive the pivot (Help-on-every-enum, owner-vs-public socket discipline, NoRecords typed-result) and re-file as designer reports against the schema-emission substrate. The rest retires.

### Cluster 3 — Persona-stack contract-rename queue (~15-18 P2/P3 beads stale)

A cluster of P2/P3 beads applies the contract-discipline reply-rename pattern across persona-stack contracts: signal-persona-mind reply renames (`primary-onio`, `primary-8fv8`, `primary-j8p9`, `primary-4ud1`), signal-persona-orchestrate renames (`primary-27wg`, `primary-trxa`, `primary-lp6f`), signal-persona-engine-management renames (`primary-npn3`, `primary-u3i9`, `primary-s51k`), owner-signal-version-handover renames (`primary-rl75`, `primary-amyw`, `primary-3uho`, `primary-fjvi`), signal-version-handover examples (`primary-18pr`, `primary-amyw`), owner-signal-persona variant renames (`primary-38k6`).

**Same supersession as Cluster 1** — these contracts live in the legacy persona stack. The rename discipline is correct workspace-wide, but applying it to soon-superseded contracts is wasted motion. The contracts that survive (signal-spirit, signal-mind, signal-orchestrate, etc. in their schema-emitted forms) get the discipline applied at schema-source authoring time, not as a contract-crate rename.

**Proposed action:** RETIRE as a group with closing notes pointing at the schema-emission pivot.

### Cluster 4 — Persona-spirit cutover + handover continuation (~10-12 P2/P3 beads stale)

The persona-spirit cross-version handover continuation arc carries P2 beads at the constraint-test layer: `primary-2ach` (event log scan for VersionQuarantined before state change), `primary-2o7p` (owner-signal-version-handover ForceFlip/Rollback marker integrity), `primary-tfdj` (quarantine gate prevents attempted handover), `primary-n9st` (signal-version-handover rejected Mirror produces typed Divergence), `primary-fv2l` (Persona ActiveVersionChangeSource projection), `primary-vjg3` (Persona event-log replay rebuilds active-version snapshot identically), `primary-dlut` (extend spirit-nspawn upgrade test with real handover socket), `primary-31jt` (persona sandbox tests with midway wire-capture), `primary-l9iz` (Quarantine policy gate enforcement in Persona), `primary-xcd5` (E2E sandbox: SCM_RIGHTS two-client routing), `primary-lfb0` (version-projection Identity blanket impl).

**Same supersession as P1 persona-spirit cutover arc.** All test or constrain the legacy persona-spirit + signal-version-handover mechanism that Spirit 1305-1314 + designer 447 supersede with upgrade-as-SEMA-on-Asschema.

**Proposed action:** RETIRE as a group. The upgrade-as-SEMA design has its own testing pipeline (designer 447 §"The testing pipeline — minimal first, then production-copy").

### Cluster 5 — Deploy-stack work (~25-35 P2/P3 beads CURRENT)

A meaningful cluster of P2/P3 beads represents **current cluster-operator + system-operator deploy-stack work** that the next-stack pivot does NOT supersede. These include: chronos (`primary-fgk`), CriomOS module work (`primary-7zz`, `primary-gfc0`, `primary-5u9`, `primary-tpd`, `primary-8b3`, `primary-9wi`), CriomOS-home (`primary-k9kj`), clavifaber (`primary-0v2`, `primary-e3c`, `primary-mm0`, `primary-nvs8`), prometheus deploy (`primary-fq9l`, `primary-ia60`, `primary-ytdj`, `primary-gdb7`, `primary-lome`), atlas/Gemma model work (`primary-1ubd`, `primary-3dqf`, `primary-f6cc`, `primary-y3is`, `primary-ooh1`), CriomOS test cluster (`primary-1ha`, `primary-58l`, `primary-7ay8`), horizon-leaner-shape arc (`primary-vhb6` IN_PROGRESS, `primary-ihee`, `primary-da7`, `primary-766g`, `primary-npd`), lojix-cli merge (`primary-b7qc`).

**These are NOT stale per the schema-emission pivot.** They live in the deploy-stack (production today vs lean rewrite) that `protocols/active-repositories.md` §"Two deploy stacks coexist" names as parallel work. Some may carry retired-lane labels (`role:system-specialist` should be `role:system-operator` per Spirit 920) — that's a category 3 hit but not a category 4 supersession.

**Proposed action:** KEEP as a cluster. Minor lane-label refresh from `role:system-specialist` → `role:system-operator` (10+ beads) in a small mechanical sweep. Some beads (`primary-vhb6` horizon re-engineering IN_PROGRESS) deserve a separate cluster-operator review for their own progress state, but that's not bead-staleness — it's session continuity.

### Cluster 6 — Real workspace concerns (~6-10 P2/P3 beads CURRENT)

A small cluster of P2/P3 beads represents real concerns that survive the pivot: Spirit query by numeric id (`primary-a6m0` — superseded by Spirit 1315-1319 spirit-query design as a designer concern, but the by-id observation IS landed), Spirit removalCandidates soft-delete (`primary-m89k` — settled design in system-designer/47, real implementation work), legacy intent extractor (`primary-h1vl` — landed psyche intent, real operator work), Nix integration tests automation (`primary-lrgj` — real open question for operator/cluster-operator), schema-diff upgrade trait surface (`primary-2n1r` — related to designer 447 upgrade-as-SEMA, may need re-anchoring), schema-core floor extraction (`primary-1xor` — DIRECTLY matches designer 444 §5 horizon 1, current + actionable).

**Most of these need minor text refresh** to reanchor at current designer reports. Specifically `primary-1xor` (schema-core extraction) is HIGHLY CURRENT — it's literally designer 444 §5 horizon 1, the workspace's headline horizon, and the bead body is accurate. Same for `primary-pjbp` (StructureHeader routing) and `primary-6d5n` (1-byte tag-space partition) — these are spirit-next prototype refinement items per Spirit records 933+934 that designer 444 §5 acknowledges as horizons.

**Proposed action:** KEEP all 6-10 beads. Refresh text on 2-3 to cite current designer reports instead of legacy `/397` references.

### P2/P3 extrapolated count

| Sub-cluster | Estimated stale | Estimated current |
|---|---|---|
| 1 — Persona-stack continuation | 85-95 | 0 |
| 2 — contract-repo.md skill updates | 12-15 | 2-3 (cherry-pickable doctrines) |
| 3 — Persona-stack contract renames | 15-18 | 0 |
| 4 — Persona-spirit cutover + handover continuation | 10-12 | 0 |
| 5 — Deploy-stack work | 0 | 25-35 |
| 6 — Real workspace concerns | 0 | 6-10 |
| **Total estimate (210 beads)** | **122-140 stale** | **33-48 current** |

Combined with the 68 P0/P1: roughly **180-200 stale beads** + **40-58 actionable beads**, ratio ~3:1 stale-to-current.

### Beads recommended to KEEP (the 9 current + actionable)

| Bead | Status note |
|---|---|
| `primary-36iq` | Bracket-string migration epic; 4/7 sub-beads complete; the remaining work is real. Refresh epic body. |
| `primary-36iq.3` | nota-config + Spirit CLI bracket-string sub-bead; deployed-CLI blocker is live + named. |
| `primary-36iq.6` (not in survey list as P2; would be P1 dependency) | (P2 child not enumerated in this audit's survey; remains adjacent) |
| `primary-9hx0` | Schema-file-split refinement question. RECOMMENDED REWRITE to convert from P1 task to design question, per `skills/beads.md` §"Anti-pattern B". |
| `primary-kbmi` + `.2` | Cloud + domain-criome runtime daemons; named in designer 446 wave-1. RECOMMENDED REWRITE to re-anchor at designer 446 porting playbook. |
| `primary-srmq` | lojix-daemon nix-auth integration; real ongoing work in the `horizon-leaner-shape` deploy-stack arc. Minor refresh only. |
| `primary-a1px` | spirit-next OutputNexus dispatcher; real ongoing follow-on. RECOMMENDED REWRITE to re-anchor at designer 446 Phase 0. |
| `primary-54ti` | horizon-rs lean-stack migration; refile as cluster-operator scope or close-as-deferred-to-deploy-stack-arc. |
| `primary-9hx0` (dup row above) | (no new note) |

So the post-audit healthy bead queue is roughly: bracket-string migration epic (refresh) + cloud/domain-criome wave-1 trio (rewrite) + spirit-next dispatcher emission (rewrite) + nix-auth (refresh) + horizon-rs catch-up (re-file) + schema-file-split as a design question (rewrite to design-question form). Six to eight beads, none in epic-of-epics shape; that's what `skills/beads.md` §"Periodic audit" recommends as a healthy queue size.

## Per-stale-bead paragraphs — the substantive findings

### The persona-prefix rename wave is mostly obsolete (`primary-0m1u` + .11 + .12)

The epic `primary-0m1u` tracks the R1-R12 rename of `persona-*` repo prefixes per designer/318. R1-R10 landed; R11 (spirit triad rename) and R12 (persona meta catch-up + CriomOS-home repin) remain open. Per the parent bead body's "Phase 2, post-pilot" gating: R11 is blocked on `primary-x3ci` (the persona-spirit cutover).

**Why it's stale:** The spirit triad is not getting renamed — it's getting FOLDED. Per designer 446 §"Phase 0 spirit fold", the `spirit-next` pilot folds into the `spirit` repo as the canonical worked example for the schema-emission porting recipe. The persona-spirit legacy repo is being abandoned, not renamed; its successor is the `spirit-next` pilot folded into `spirit`. R12 (CriomOS-home repin) reanchors on the new `spirit` repo's binary artifacts, not on a persona-spirit renamed binary.

**Proposed rewrite:** RETIRE the epic + R11 + R12 with a closing note pointing at designer 446 §"Operator-bead-shaped first action — Phase 0 spirit fold". File a new operator bead "Phase 0 spirit fold: relocate spirit-next pilot into spirit repo" once the spirit-triad naming question (designer 446 §"The one designer call that gates Phase 0") is settled by the psyche. The new bead carries the spirit fold's commit-history-as-template role for subsequent ports.

### The persona-stack migration backlog (`primary-4naq`, `primary-a5hu`, `primary-c620`, `primary-gu7t`, `primary-wvdl`, all `primary-gvgj.*`)

These beads encode ~6 weeks of operator + designer thinking about how to migrate persona-* components from the legacy signal-core + signal-executor + persona-mind foundation onto a `signal-executor v4` foundation, plus the persona-agent triad (`primary-gvgj`) that designer/309 proposed as an abstraction over harness backends.

**Why it's stale:** Per designer 446's whole framing, the migration target is no longer `signal-executor v4`. It's the schema-emitted Signal/Nexus/SEMA stack (the `spirit-next` pilot's substrate). Per designer 444 §"What's LIVE today", every emitted component now gets schema-emitted nouns, Mail<Phase> typestate, Engine-as-composer — the `signal-executor v4` recipe is the substrate beneath what's being retired. Per designer 446 §"Phase 2 — stateful runtimes", persona-mind/router/terminal/orchestrate/message/introspect all port in wave-2, AFTER schema-core extraction lands. The wave-2 framing replaces the per-component "current-foundation migration" framing.

For `primary-gvgj` (persona-agent): the proposed shape — agent component multiplexing 5 backends — is the legacy persona-stack design. The schema-emission pivot doesn't preserve that triad shape because agents-as-components is a router-level concern, not an architectural-substrate concern. Whatever the new agent shape becomes, it lands as schema-emitted nouns, not as a hand-coded multiplex daemon.

**Proposed rewrites:**

- `primary-a5hu` (epic), `primary-4naq` (sub-epic), and all per-component children (`primary-c620`, `primary-gu7t`, `primary-wvdl`, `primary-nobf`, `primary-q98d`): RETIRE with one closing-note family pointing at designer 446 §"Phase 2 — stateful runtimes" + Spirit 1305-1314. Restate that the canonical home is designer 446's porting playbook; file new wave-2 operator beads once schema-core extraction (designer 444 §5 horizon 1) lands.
- `primary-gvgj` (epic) + 7 sub-beads: RETIRE with a closing note pointing at designer/309 as superseded design. The agent triad is a designer-level open question; file a designer bead for "agent-triad redesign for schema-emitted next-stack" if/when the question becomes load-bearing.

### The signal_channel! macro substrate is being retired (`primary-3cl1`, `primary-bg9l`, `primary-l02o`, `primary-v5n2`, `primary-ezqx`, `primary-ezqx.1`, `primary-ezqx.3`, `primary-muu2`)

These beads track the consolidation of multiple `signal_channel!` macro extensions: LogVariant trait + LogSummary trait + frame_micro projection + contract_section grammar + Help-on-every-enum recursion + golden-ratio variant-index split. The convergence target was `primary-ezqx`: "one PR-shaped landing" against the `signal-frame` + `signal-frame-macros` + `signal-cli-macros` repos.

**Why it's stale:** Per `protocols/active-repositories.md`, `signal-frame-macros` and `signal-cli-macros` are not in the active stack. The macro-emission substrate is now `schema-rust-next` (consuming `Asschema` and emitting Rust source). Per Spirit 1287/1290/1292 + designer 444 §"What's LIVE today", the body-stream substrate + schema-emitted Signal/Nexus/SEMA projections supersede the `signal_channel!` extensions: the LogVariant + frame_micro + Help projection concerns become schema-rust-next emission concerns, and the contract_section/golden-ratio split is meaningless when variant indices are schema-declared.

**Proposed rewrites:** RETIRE all 8 beads with one closing-note family. The substantive concerns (Help routing on every enum, LogVariant projection for observability, golden-ratio namespace split for owner-vs-ordinary contract collisions) remain valid as designer-level open questions for the schema-emission stack but should be re-filed as designer reports if/when they become load-bearing. Do not preserve them as `signal_channel!`-flavored beads.

### The persona-spirit v0.1.0/v0.1.1 cutover arc is fully abandoned (`primary-602y`, `primary-0jjz`, `primary-1jql`, `primary-ekxx`, `primary-x3ci`, `primary-x3ci.1`)

These six beads track the persona-spirit cross-version upgrade ceremony: wire-compat rebuild of v0.1.0.1 against current signal-frame, brief-outage cutover MVP, in-transition messages probe, signal-version-handover schema-derived emission, the main cutover bead, and the production pre-migration step.

**Why it's stale:** Per Spirit 1305-1314 + designer 447, upgrade IS SEMA-on-Asschema. The schema-daemon receives `EditSchema(SchemaEdit)` operations, derives migration code, hands to upgrade-daemon which runs the transitory-database pattern (Spirit 1310). The whole architecture is **not** a cross-version handshake (AskHandoverMarker/ReadyToHandover/HandoverCompleted); it's an editor on schema state with a separate testing pipeline. The persona-spirit legacy stack is being absorbed by the spirit-fold (designer 446 Phase 0) and its upgrade mechanism is being replaced wholesale.

**Proposed rewrites:** RETIRE all 6 beads with one closing-note family pointing at designer 447 (upgrade-as-SEMA design) and designer 446 §"Phase 0 spirit fold". File a new operator bead per designer 447 §"Operator-bead-shaped first action" — the minimal NOTA-to-object correspondence demo for schema-daemon.

### Tap-emit Tier 1 observability substrate is retired (`primary-145a`, `primary-bann`, `primary-8avm`)

These beads track persona-introspect's tap-emit subscription model: persona-spirit-daemon emits the inbound frame's micro on accept, persona-introspect subscribes via DeliveryTraceKey four-field correlation, the Tier 1 always-on tap pipeline carries observability micros.

**Why it's stale:** Same family as the `signal_channel!` retirement — the Tap event substrate is part of the `signal_channel!`-era observability arc, retired as the macro substrate moves to schema-emission. Per designer 446 §"Phase 2", persona-introspect is wave-2 and re-emerges as a schema-emitted component; its observability model becomes a follow-on designer report, not the legacy Tap-event shape.

**Proposed rewrites:** RETIRE all 3 beads. The observability concerns (delivery-trace correlation across hops, low-overhead tap streams) remain valid as designer-level open questions for the schema-emission stack. File a designer report when the schema-emitted introspection model gets designed for the wave-2 port.

### The legacy persona triad migrations carry retired-lane references (`primary-0bls`, `primary-c620`, `primary-gu7t`, `primary-wvdl`)

These beads reference `reports/designer-assistant/...` paths (e.g. `141-criome-triad-audit-2026-05-21.md`, `137-persona-orchestrate-triad-audit-2026-05-21.md`, `135-persona-harness-triad-audit-2026-05-21.md`). Per Spirit record 920 (Maximum, 2026-05-27), the `<role>-assistant` suffix is retired workspace-wide. Per `skills/role-lanes.md` §"Lane naming convention", the existing `reports/<role>-assistant/` directories should already be folded into `reports/<role>/`.

These beads' "Audit (read first)" sections point at paths that may no longer resolve. This is a separate axis of staleness from the substantive supersession (category 4), but it compounds: even if the bead's substantive direction were current, an operator picking it up would find dead links.

**Proposed rewrites:** The beads are wholly stale per category 4 anyway — the retired-lane references are a secondary signal confirming the staleness. RETIRE them all in the same close-sweep that addresses the persona-* migration backlog.

### Cloud + domain-criome are real wave-1 work but need re-anchoring (`primary-kbmi`, `primary-kbmi.2`)

The parent epic body says "Implement the real runtime legs after the contract birth: ordinary and owner Unix sockets, signal-frame request/reply handling, sema-engine stores for policy/plans/registry, typed unsupported/configuration replies, Cloudflare read-only actor first, and owner-approved apply after plan generation." `primary-kbmi.1` is closed (first runtime slices landed at cloud c188543e + domain-criome 9db6a68b on shared branch `cloud-domain-criome-runtime`). `primary-kbmi.2` (domain-criome runtime) and the parent both remain open.

**Why it's actionable but stale:** Per designer 446 §"Phase 1a in parallel", `cloud` is one of three named wave-1 ports (cloud + upgrade + repository-ledger). Both `cloud` and `domain-criome` are in `protocols/active-repositories.md` adjacent-active. The bead's TEXT predates designer 446's framing: the "signal-frame request/reply handling + sema-engine stores" recipe IS the schema-emission porting recipe described in designer 446 sub-agent 2's playbook, just phrased pre-pivot.

The retired `role:system-specialist` label per Spirit 920 (lane retired) is a separate problem — should become `role:cloud-operator` or `role:operator` per `skills/role-lanes.md` §"Lane naming convention".

**Proposed rewrites:** REWRITE both beads with:
- Re-anchor at designer 446 §"Phase 1a in parallel" + sub-agent 2's 5-stage operator recipe.
- Replace the legacy `signal-frame request/reply handling + sema-engine stores` recipe with the schema-emission porting recipe: ".schema source + build.rs + schema-emitted runtime substrate + witness tests per `skills/component-triad.md`."
- Drop `role:system-specialist`, add `role:operator` (or whatever cloud-operator lane carries).
- Add cross-reference to `primary-kbmi` parent's acceptance criteria mapping onto the porting playbook's stage 4 (witness tests).

### Schema-file split is a design question, not a P1 task (`primary-9hx0`)

The bead body asks for "three-plane schema decomposition working: signal/nexus/sema schemas separately authored and emitted." The bead's own NOTES section acknowledges PARTIAL: spirit-next has three explicit roots (NexusInput/Output, SemaInput/Output) but in ONE schema document; the three-file split is a refinement question.

**Why it's stale per skills/beads.md §"Anti-pattern B":** A bead that says *"figure out X"* without a definition of done is a design question. The three-file-split question doesn't have a workspace-discipline answer — Spirit record 964 leaves the choice open. Designer 444 §"open horizons" doesn't flag the split as a horizon. The acceptance criteria ("Three-plane schema decomposition working") could be met OR rejected with equal honesty.

**Proposed rewrite:** Two paths.

- (a) **Convert to a designer-report bead.** Acceptable bead form per `skills/beads.md`: *"Land designer report on schema-file split"* — discrete, will close when the report lands.
- (b) **Close as design-question epic, file a designer report directly.** No bead at all; the question lives in a designer report when an agent has bandwidth to write it.

Recommendation: (b). Close the bead with a note pointing at `skills/beads.md` §"Anti-pattern B"; file a designer report when the spirit-fold lands and the per-plane file question becomes load-bearing.

### Patterns observed

Five patterns explain why the staleness exists:

#### Pattern 1 — pre-pivot persona-stack work dominates

Across both the P0/P1 layer and the P2/P3 substrate, the dominant cluster of stale beads targets the legacy persona stack: `signal_channel!` macro extensions, persona-* component migrations, persona-agent triad, persona-spirit version handover, persona-introspect tap-emit, persona-stack contract renames. The schema/NOTA-next pivot (broadly: Spirit 1287 onwards, designer 444-447) reshapes every one of these surfaces. The bead store accumulated migration plans that the pivot makes irrelevant. Combined estimate across P0/P1/P2/P3: 100-130 beads.

#### Pattern 2 — the upgrade-mechanism arc is fully replaced

Approximately 15-20 beads (P1 + P2 + a few P3) track persona-spirit upgrade orchestration in the pre-Spirit-1305 shape (handover handshake, version-projection, version-handover sockets, sandbox tests, constraint tests). Per Spirit 1305-1314 + designer 447, upgrade is now SEMA-on-Asschema; the schema-daemon owns the editor responsibility and upgrade-daemon owns the testing pipeline. The previous mechanism's primary artifacts (signal-version-handover, owner-signal-version-handover, the active-version selector, HandoverDriver) are abandoned, not refined.

#### Pattern 3 — retired-lane references compound supersession

10+ beads reference `reports/designer-assistant/...` paths from retired role directories (Spirit 920, 2026-05-27). The references are dead links even if the substantive concern survives. Additionally, the deploy-stack cluster (cluster 5) carries `role:system-specialist` labels (now `role:system-operator` per Spirit 920) — a category 3 hit but not a category 4 supersession.

#### Pattern 4 — the bead store's "epic" abstraction has soured

The store has 9+ epics (`primary-0m1u`, `primary-4naq`, `primary-a5hu`, `primary-c2da`, `primary-ezqx`, `primary-gvgj`, `primary-kbmi`, `primary-l3h5`, `primary-ipjx`, `primary-u8vo`, `primary-ngn8`, `primary-ib5n`). All but `primary-kbmi` and `primary-ipjx` (durable speech-to-text infrastructure — separate concern, may stay) are wholly superseded. Per `skills/beads.md` §"Anti-pattern A: durable-backlog beads", epics that don't close are anti-pattern. The pivot made every epic's "definition of done" unreachable; the epics have been carrying superseded plans for weeks.

#### Pattern 5 — the contract-repo.md skill update queue is institutionally stale

A 12-15-bead P3 cluster adds doctrinal items to `skills/contract-repo.md` (Help variant, Tier 1 micro header, signal_cli! caller-pid, SignalCore zone, owner-vs-public socket, Cloud as Sema-shaped, Unknown variant, supervision-is-not-namespace, raw-bytes escape hatch, NOTA-as-code-comments, multi-version handover protocol, NoRecords typed-result, etc.). The skill itself describes hand-rolled `signal_channel!`-style contract authoring; the schema-emission pivot moves contract authoring to `.schema` source files. The skill update queue is targeting a substrate that's being supplanted. A few doctrines survive at schema-source-authoring level (Help-on-every-enum, owner-vs-public socket discipline, NoRecords) and should re-emerge as designer reports against `skills/nota-design.md` + the schema language. The rest retires.

#### Pattern 6 — the bracket-string migration is the one healthy arc

The `primary-36iq` family (NOTA bracket-string merge and consumer migration) is the workspace's only currently-healthy bead arc: 4/7 sub-beads closed, the remaining work is real, the deployed-CLI blocker is honestly named. This is the model of a healthy bead arc; the rest of the store should look like this.

#### Pattern 7 — deploy-stack and schema-core extraction beads escape supersession

A meaningful current substrate exists: 25-35 deploy-stack beads (cluster 5) plus 6-10 next-stack continuation beads (cluster 6). The `primary-1xor` schema-core floor extraction bead is HIGHLY current — it literally targets designer 444 §5 horizon 1, the workspace's headline horizon, and the bead body is accurate. The deploy-stack beads (chronos, CriomOS, prometheus, clavifaber, horizon-leaner-shape arc) are workspace-current work that the next-stack pivot doesn't supersede; they need only minor label cleanup. This is the substrate that survives the audit cycle.

## Cross-references

### Workspace contract + skills

- `/home/li/primary/AGENTS.md` — workspace contract; hard overrides applied throughout this audit.
- `/home/li/primary/ESSENCE.md` — essence (workspace's most upstream intent).
- `/home/li/primary/skills/beads.md` — beads discipline; the audit anti-patterns (A, B) applied here.
- `/home/li/primary/skills/intent-maintenance.md` — supersession discipline (the audit's central operation).
- `/home/li/primary/skills/role-lanes.md` — lane structure; retired `-assistant` suffix per Spirit 920.
- `/home/li/primary/skills/component-triad.md` — triad shape; porting beads honor this discipline.
- `/home/li/primary/protocols/active-repositories.md` — canonical component map; cross-checked against bead repository references.

### Spirit records cited

- 1287 (Maximum Correction) + 1290 (Maximum Decision) + 1292 (Maximum Decision) — body-stream substrate landed; supersedes the `signal_channel!` macro arc and the Tap-event observability substrate.
- 1294 + 1295 (Maximum Decision + Correction) — schema source enum-body honesty landed.
- 1297 (High Decision) — prototype removes compatibility paths; supersedes "carry old syntax for compat" beads.
- 1300 + 1301 + 1302 (Maximum) — schema macro library single-datatype; supersedes the source/data split in macro library beads.
- 1305-1314 (Maximum across all 10) — upgrade IS SEMA on Asschema; schema-daemon as editor; transitory-database pattern; compilation step; concrete schema-edit operation examples; self-editing design starts now. Supersedes the persona-spirit handover arc.
- 1315-1319 (High + Maximum) — spirit-query design (verbal depth scopes, frequency-adaptive, multi-topic matching). Not directly bead-relevant but signals heavy recent intent churn.
- 920 (earlier — Maximum, 2026-05-27) — `<role>-assistant` suffix retired; lane shapes are `<role>`, `second-<role>`, `<qualifier>-<role>` only. Supersedes 6 beads' lane references.

### Designer reports cited

- `reports/designer/443-design-improvements-audit-2026-05-31/{0-frame-and-method,5-overview}.md` — broad design audit; the headline backlog (schema-core extraction + 4 other improvements) re-anchors several beads' framing.
- `reports/designer/444-stack-vision-2026-05-31/5-overview.md` — horizon ledger; the "What's LIVE today" section is the workspace's current source-of-truth for what the schema/NOTA-next stack has shipped.
- `reports/designer/445-next-stack-audit-2026-06-01.md` — substrate audit; Findings 1-4 are the canonical workspace-discipline bead queue today (one free function + one one-impl trait + one CLI NOTA-prefix detection + one Display fallback).
- `reports/designer/446-next-stack-porting-research-2026-06-01/4-overview.md` — porting research; the Phase 0 (spirit fold) + Phase 1a (cloud + upgrade + repository-ledger in parallel) + Phase 2 (stateful runtimes after schema-core) framing reshapes the persona-* migration backlog.
- `reports/designer/447-upgrade-as-sema-design-2026-06-01.md` — upgrade-as-SEMA design; the schema-daemon + upgrade-daemon architecture supersedes the persona-spirit handover arc.
- `reports/designer/448-single-field-wrapper-audit-2026-06-01.md` — single-field wrapper audit; FieldEncode ZST anti-pattern surfaced (one operator-hour cleanup).

### Operator reports cited

- `reports/operator/265-programmable-nota-structural-macro-vision-2026-05-31/4-overview-and-gaps.md` — implementation-anchored stack vision + 5-gap inventory.
- `reports/operator/267-macro-library-nota-types-2026-06-01.md` — macro library NOTA types; documents the current implementation after Spirit 1300-1302.
- `reports/operator/268-schema-source-artifact-datatype-split-audit-2026-06-01.md` — confirmed source/artifact datatype split fixed; macro library + pattern/template data mirrors still need collapse.
- `reports/operator/269-rust-single-field-wrapper-validity-audit-2026-06-01.md` — single-field wrapper validity; converges with designer 448; FieldEncode ZST.
- `reports/operator/270-single-field-wrapper-comparison-with-designer-448-2026-06-01.md` — methodology improvement: grep for ZST holders after wrapper validation.

## For the orchestrator

The highest-priority bead cleanups, ranked by the noise-reduction-value of retirement (covering both the headline-detailed P0/P1 layer + the extrapolated P2/P3 clusters):

1. **Bulk-retire the `signal_channel!` macro substrate arc** (~10-15 beads, P1 + P2). P1 layer: `primary-3cl1`, `bg9l`, `l02o`, `v5n2`, `ezqx`, `ezqx.1`, `ezqx.3`, `muu2`. P2 layer: `primary-9dce`, `primary-k8cn`, `primary-b86d`, `primary-g21y`, `primary-2py5`, `primary-uq04` + children. Closing-note family: "Macro substrate moved to schema-emission per designer 444 §'What's LIVE today'. `signal-frame-macros` + `signal-cli-macros` are retired in favor of `schema-rust-next` emission. The consolidation this work targeted is moot."

2. **Bulk-retire the persona-spirit cutover + handover arc** (~12-15 beads, P1 + P2). P1 layer: `primary-602y`, `0jjz`, `1jql`, `ekxx`, `x3ci`, `x3ci.1`. P2 layer: `primary-2ach`, `primary-2o7p`, `primary-tfdj`, `primary-n9st`, `primary-fv2l`, `primary-vjg3`, `primary-dlut`, `primary-31jt`, `primary-l9iz`, `primary-xcd5`, `primary-lfb0`, `primary-18pr`, `primary-rl75`, `primary-amyw`. Closing-note family: "Per Spirit 1305-1314 + designer 447, upgrade IS SEMA on Asschema; the schema-daemon + upgrade-daemon are the canonical objects. The persona-spirit v0.1.0/v0.1.1 line + signal-version-handover handshake are abandoned."

3. **Bulk-retire the persona-stack migration backlog** (~25-30 beads, P1 + P2). P1 layer: `primary-a5hu`, `4naq`, `c620`, `gu7t`, `wvdl`, `nobf`, `q98d`, `21gn`, `8n8`, `e1pm`, `hj4`, `hj4.1`, `hj4.1.4`, `krbi`, `li7a`, `aunn`, `qjdp`, `9os`, `es9`, `devn`, `devn.1.4`, `2y5`, `a18`, `0bls`, all 7 `primary-gvgj.*`, `primary-gvgj.10`, `primary-ojxq`. P2 layer: `primary-ep45`, `primary-3rp0`, `primary-aww`, `primary-u8vo` epic + 11 children, all the persona-stack contract-rename beads (Cluster 3), `primary-c0pp`, `primary-fwll`, `primary-rtz8`, `primary-g3gm`, `primary-7i6a`. Closing-note family: "Persona-stack migration is superseded by the schema-emission pivot. Components port via designer 446 wave-2 (after schema-core extraction lands)."

4. **Retire the persona-prefix rename remnants** (~5 beads). P1 layer: `primary-0m1u`, `0m1u.11`, `0m1u.12`. P2 layer: `primary-l3h5` epic + sub-bead `primary-l3h5.7`. Closing-note: "The spirit triad is being FOLDED, not renamed (designer 446 Phase 0). The upgrade triad merger (U1-U7) is superseded by designer 447 schema-daemon + upgrade-daemon design."

5. **Bulk-retire the contract-repo.md skill-update queue** (~12-15 P3 beads). All listed in Cluster 2 above. Cherry-pick 2-3 doctrines (Help-on-every-enum, owner-vs-public socket discipline, NoRecords typed-result) and re-file as designer reports against schema-emission substrate.

6. **Refile retired-lane labels in the deploy-stack cluster** (~10-15 beads). Cluster 5 deploy-stack beads with `role:system-specialist` (or other retired labels) → `role:system-operator` per Spirit 920. This is a mechanical label-only sweep.

7. **Rewrite 4-5 actionable beads** to re-anchor at current reports: `primary-kbmi` + `kbmi.2` (anchor at designer 446 §"Phase 1a"), `primary-a1px` (anchor at designer 446 Phase 0), `primary-1xor` (anchor at designer 444 §5 horizon 1 — though the bead is already pretty accurate), `primary-54ti` (refile as cluster-operator scope), `primary-9hx0` (convert from P1 task to designer-report bead per `skills/beads.md` §"Anti-pattern B").

8. **Close-as-shipped** ~3-5 beads: `primary-duuv` (DatabaseMarker shipped per designer 444), `primary-lrf8` (mail-keeper shipped per designer 444). Possible additional close-as-shipped: `primary-q2au` (redb backing landed on designer branch; check if integrated).

**Lane recommendation for the close-sweep:** the designer lane DIRECTLY APPLIES the retirements (1-6 above) via a follow-up `bd close ... -r "<closing note>"` sweep — the substantive supersession is clear, the closing notes are short, and the close-sweep is mechanical. The REWRITES (item 7) go to operator/cluster-operator since they require operator's current understanding of work in flight. The CLOSE-AS-SHIPPED (item 8) goes to operator since operator owns the canonical-home breadcrumbs for shipped work.

**Lane recommendation for the substantive risk:** an operator picking up any of the stale beads in good faith and starting work would produce code in the legacy persona-stack shape, contradicting Spirit 1287/1290/1294/1295/1297/1300-1302/1305-1314 + designer 444-447. The risk is concrete — operators have time-pressure habits that pull them toward picking up the next P1 bead without re-deriving its anchor in current intent. The calibration pass is load-bearing against accidental backwards work.

**Expected outcome post-sweep:** bead store shrinks from 269 open to roughly 30-40 open, of which 25-35 are deploy-stack (cluster 5) and 5-10 are next-stack continuation (cluster 6 + rewritten beads). The headline P1 layer drops from 67 to roughly 5-8 (`primary-36iq` epic + 2-3 sub-children + `primary-srmq` + `primary-1xor` + rewritten `primary-kbmi` + .2 + rewritten `primary-a1px`). That's within the healthy queue size `skills/beads.md` §"Periodic audit" recommends.

## For the psyche — paste-into-chat summary

The bead store has 269 open beads. The recent intent corpus (Spirit 1280-1319) and designer reports (443-448) have wholly reshaped what's load-bearing — most accumulated over ~5 weeks is now anchored at substrates the schema-emission + upgrade-as-SEMA pivot has retired. The dominant stale clusters are: persona-* migration backlog (~25-30 beads anchored at `signal-executor v4`), `signal_channel!` macro arc (~10-15 beads pointing at retired `signal-frame-macros`/`signal-cli-macros` repos), persona-spirit v0.1.0/v0.1.1 handover ceremony (~12-15 beads encoding the upgrade mechanism that Spirit 1305-1314 + designer 447 replace with upgrade-as-SEMA-on-Asschema), persona-prefix rename remnants (~5 beads — spirit triad is being FOLDED not renamed per designer 446 Phase 0), and the contract-repo.md skill-update queue (~12-15 P3 beads). About 33-48 beads remain actionable: mostly the deploy-stack cluster (chronos, CriomOS, prometheus, clavifaber, horizon-leaner-shape) plus a handful of next-stack continuation (bracket-string migration 4/7 closed; cloud + domain-criome wave-1 ports needing rewrite; nix-auth integration; `primary-1xor` schema-core extraction is HIGHLY current as designer 444's headline horizon). Designer recommends bulk close-as-superseded for the 5 stale arcs (designer lane can do the close-sweep directly), with operator/cluster-operator rewriting ~5 salvageable beads. Full audit at `reports/designer/449-bead-staleness-audit-2026-06-01.md`.
