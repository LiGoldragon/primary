# 5 — Topic: workspace discipline + Pi-harness + NOTA-string + misc (cross-lane)

*Cross-lane topic aggregation per `skills/context-maintenance.md` §2.
The catch-all of three retired threads + the maintenance ledgers:
(a) the **Pi-harness** thread (cluster-operator, third-designer, cloud-
operator 1-5) — shipped, historical; (b) the **NOTA bracket-string**
thread (nota-designer 1-7) — shipped, the discipline is now a hard
override; (c) **context-maintenance ledgers + intent audits** (designer
386/, 351, 352, second-operator/191) — the meta-layer. Plus the
**third-designer questions/architecture** meta-dirs that span cloud +
schema.*

## (a) Pi-harness thread — SHIPPED, retire as a block

The prior cross-lane sweep (designer/386/12 §2) already found: "The
Pi-harness thread is mostly retired… a coordinated retirement pass
across these lanes would clear ~15 reports in one move." That finding
**has not been actioned** (the reports still exist). It remains
correct. The Pi-harness work (Pi-as-Codex-replacement, Pi extensions /
defaults / yolo-mode, subagents+chains, safety dirty-prompt fix) all
shipped 2026-05-22→25.

### Recency rank + drops (Pi-harness)

**Newest canonical (KEEP one as the landing state, if any):** none of
these is a current active surface — Pi work is done. The most recent is
cloud-operator/5 (Pi chain function, 05-25) + cluster-operator/11 (MVP
sandbox audit, 05-23, which actually points at system-designer/34's
frame — it's half Lojix-MVP, half Pi-sandbox).

| Lane | Reports | Date | Recommendation |
|---|---|---|---|
| cluster-operator | `3` (third-designer/17 blocker audit), `6` (Pi defaults + extension packaging), `7` (Pi follow-up after third-designer/21), `8` (Pi extension testing), `9` (audit pi-operator safety fix), `10` (Pi yolo-mode + flake inputs) | 05-22→23 | **DROP all** — Pi work shipped; defaults/extensions live in the Pi profile + cluster runbook |
| cluster-operator | `11` MVP sandbox + small fixes | 05-23 | **DROP** — points at system-designer/34's frame; the MVP-sandbox audit is superseded by system-designer/40 (port feasibility); small fixes landed |
| third-designer | `20` Pi-as-Codex-replacement design | 05-22 | **DROP** — Pi adopted; design realized |
| third-designer | `21` audit cluster-operator/6 Pi-harness | 05-22 | **DROP** — audit of cluster-operator/6 (dropping) |
| cloud-operator | `1` Pi-operator safety dirty-prompt handoff | 05-27* | **DROP** — handoff to cluster-operator/9 (dropping); safety fix landed (*git date late; content is 05-23-era Pi work) |
| cloud-operator | `2/` Pi-harness follow-up audit | 05-23 | **DROP** |
| cloud-operator | `3` Pi subagents + chains research | 05-23 | **DROP** |
| cloud-operator | `4` Pi auto-compaction + web-access update | 05-23 | **DROP** |
| cloud-operator | `5` Pi-harness chain function | 05-25 | **DROP** — chain behaviour documented; lives in Pi profile |

**~13 Pi-harness reports** DROP across three lanes. **Misplacement
note (from prior sweep, still true):** cloud-operator/1-5 are
Pi-related work sitting in the `cloud-operator` lane — they belong
conceptually to `cluster-operator`/`pi-operator`. Since they're all
DROP candidates anyway, the cleanest resolution is to drop them rather
than relocate. The prior sweep also clarified the lane boundary
(cluster-operator = physical Pi/Zeus cluster; cloud-operator =
Cloudflare/cloud-deploy) in orchestrate/AGENTS.md — so future Pi work
won't land in cloud-operator.

## (b) NOTA bracket-string thread — SHIPPED, discipline is a hard override

The nota-designer bracket-string arc (changing canonical NOTA strings
from quoted to bracket forms) **shipped**. The discipline is now a
**hard override in AGENTS.md** ("NOTA strings come EXCLUSIVELY from
bracket forms; never emit quotation marks") and lives in
`skills/nota-design.md` §"Strings come EXCLUSIVELY from bracket forms".
The migration is done.

| Report | Date | Recommendation |
|---|---|---|
| `nota-designer/1` protocol adoption + lane gap | 05-22 | **DROP** — lane-gap orientation; the lane is established |
| `nota-designer/2` bracket-string vision + production audit | 05-22 | **DROP** — vision shipped; in nota-design.md + AGENTS.md override |
| `nota-designer/3` bracket-string implementation result | 05-22 | **DROP** — impl landed |
| `nota-designer/4` bracket-string verification + migration beads | 05-23 | **DROP** — verification done; beads closed |
| `nota-designer/5/` bracket-string migration | 05-23 | **DROP** — migration executed |
| `nota-designer/6` quoted-string purge audit | 05-24 | **DROP** — purge done; the override codifies "never emit `\"`" |
| `nota-designer/7` notation-cutover database handover | 05-24 | **DROP** — DB cutover survived (Spirit live at v0.3) |

**7 nota-designer reports** DROP. Combined with nota-designer/8+9 (in
the schema sub-report), **the entire nota-designer lane retires.** This
re-raises the prior sweep's open question (designer/386/12 Q2): *is the
nota-designer lane still load-bearing?* With all 9 reports stale and
the NOTA-string + schema-lowering work absorbed, the lane is a
candidate for retirement (fold any residue into designer/, per record
920 retired-lane discipline). **Flag for the psyche** — carry-
uncertainty: proposed-not-decided.

## (c) Context-maintenance ledgers + intent audits

| Report | Date | Note | Recommendation |
|---|---|---|---|
| `designer/386/` cross-lane maintenance (PRIOR sweep) | 05-27 | The predecessor of THIS sweep. designer/415 KEPT it because "no evidence the per-lane handoffs were applied." **This sweep (system-designer/44) supersedes it** — it re-ranks all lanes by topic and re-issues the handoffs. | **DROP — owned by designer lane.** Once system-designer/44's overview lands, designer/386/ is superseded; per `skills/context-maintenance.md` (a deletion-ledger / sweep meta-dir retires on successor). Handoff to the designer agent. |
| `second-operator/191` intent-context-maintenance | 05-25 | A context-maintenance ledger for the second-operator lane; absorbed by subsequent sweeps | **DROP — owned by second-operator.** Empties the lane (with 184/186/190). |
| `designer/351` intent-file tour | 05-26 | Carries **5 pending psyche-review flags**; designer/415 KEPT it as load-bearing-until-psyche-acts | **KEEP — designer lane (§ pending psyche).** Flag aging (3 sweeps). |
| `designer/352` intent-log audit | 05-26 | Carries **D1-D18 / M1-M5 / H1-H12 flagged-for-psyche** items; per record 719 agents FLAG never supersede | **KEEP — designer lane (§ pending psyche).** Flag aging. |

**Note on this sweep vs designer/386:** the cleanest outcome is that
**system-designer/44 (this directory) becomes the live cross-lane
maintenance meta-report and designer/386 retires.** The dispatcher
should coordinate with the designer lane to drop 386/ once 44's
overview is written — otherwise two cross-lane sweep meta-dirs linger
(exactly the "stale reports lingering" the psyche directive targets).

## (d) third-designer questions/architecture meta-dirs + misc

| Report | Date | Topic spillover | Recommendation |
|---|---|---|---|
| `third-designer/17` situation + questions | 05-22 | Orientation/questions | **DROP** — questions resolved by subsequent design |
| `third-designer/18` audit synthesis | 05-22/23 | Audit synthesis | **DROP** — superseded |
| `third-designer/19` refresh after prime session | 05-22 | Refresh/orientation | **DROP** — ephemeral |
| `third-designer/23/` architecture update | 05-23 | cloud-criome + signal 64-bit header + arca cascade | **DROP-or-FORWARD** — the cloud-criome part → cloud-designer (cloud sub-report); signal-header part superseded by INTENT.md §signal-protocol. Mostly stale; forward the criome-audit slice if not absorbed |
| `third-designer/25/` most-important-questions | 05-24 | signal-channel macro + cloud quorum + deploy-cutover | **DROP-or-KEEP** — if any of its questions remain open they're load-bearing; most are answered by the schema-stack + Lojix work. third-designer agent should check; default DROP |

**~5 third-designer reports** DROP/forward (with /20, /21 Pi above and
/22 cloud forwarded in the cloud sub-report, this clears the entire
8-report third-designer lane). The lane has been quiet since 05-24
(prior sweep noted this) — another retirement candidate.

### system-operator misc (NOTA + AI-points folded reports)

| Report | Date | Note | Recommendation |
|---|---|---|---|
| `system-operator/3` Mario Zechner AI-agent points | 05-17 | Talk notes (folded from retired lane) | **DROP** — talk notes, historical; extract any live insight to a skill first if valuable |
| `system-operator/4` NOTA mixed-enum support vision | 05-17 | NOTA-language design | **DROP** — superseded by system-designer/27 (nota-mixed-enum) + INTENT.md §three-schema-types (enum support landed in schema) |
| `system-operator/5` NOTA syntax exception audit | 05-17 | NOTA syntax | **DROP** — syntax settled; nota-design.md |
| `system-operator/6` NOTA family audit | 05-17 | NOTA family | **DROP** — superseded by nota-design.md + the schema stack |
| `system-operator/7` persona-spirit production user-session | 05-17 | Spirit usage session | **DROP** — Spirit live; superseded by system-operator/168 |
| `system-designer/27` nota-mixed-enum support | 05-23 | Designer-side NOTA-enum design | **DROP — system-designer lane.** Enum support landed in schema (INTENT.md §three-schema-types); mirror of system-operator/4. |

**6 misc reports** DROP (system-operator 5, system-designer 1). The
system-operator NOTA reports (4, 5, 6) and system-designer/27 are the
same NOTA-language-design topic, now absorbed into the schema stack +
nota-design.md.

## Stale-flag count for this topic

**~38 reports** flagged stale: Pi-harness 13 (cluster-operator 7, third-
designer 2, cloud-operator 5*… note cloud-operator/1's late git date),
NOTA-string 7 (nota-designer), ledgers 2 (designer/386, second-operator/
191), third-designer questions/arch ~5, system-operator misc 5, system-
designer 1. KEEP: designer/351, 352 (pending psyche).

## Drop ownership by lane (handoff)

- **system-designer (THIS dispatcher executes):** 27 (nota-mixed-enum,
  → absorbed into schema stack). [Combined with sub-report 2's
  Lojix drops 26/28/29/30/31/36/38, the dispatcher's own lane goes from
  15 → ~6-7.]
- **When `cluster-operator` next does maintenance, the Pi drops it owns
  are:** 3, 6, 7, 8, 9, 10, 11 (Pi-harness block). With sub-report 2's
  `4` (lojix daemon), the lane reduces to ~1 (the update-authority
  design `1`, keep-or-migrate). **Retirement candidate.**
- **When `third-designer` next does maintenance, the drops it owns
  are:** 17, 18, 19, 20, 21, 23/, 25/ (+ 22/ forwarded to cloud in
  sub-report 3). Clears the lane. **Retirement candidate.**
- **When `cloud-operator` next does maintenance, the Pi drops it owns
  are:** 1, 2/, 3, 4, 5 (+ 8 cloud-recap in sub-report 3). Leaves the
  current cloud impl (9, 10, 11) — clean + under cap.
- **When `nota-designer` next does maintenance, the drops it owns are:**
  1, 2, 3, 4, 5/, 6, 7 (+ 8, 9 in schema sub-report). **Entire lane
  retires — flag to psyche (lane-status question, carry-uncertainty).**
- **When `second-operator` next does maintenance, the ledger drop it
  owns is:** 191 (+ 184/186 persona, 190 schema). **Lane empties.**
- **When `system-operator` next does maintenance, the misc drops it
  owns are:** 3, 4, 5, 6, 7 (folded-from-retired-lane NOTA/AI/Spirit).
- **designer lane (handoff to designer agent):** DROP 386/ once this
  sweep's overview lands (it supersedes the prior cross-lane meta-dir).
  KEEP 351, 352 (pending psyche — surface the aging flags to the
  psyche per designer/415's recommendation).
