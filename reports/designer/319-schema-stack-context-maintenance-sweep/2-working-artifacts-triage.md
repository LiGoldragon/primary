*Kind: Triage · Topic: working-artifacts-triage (Subagent B) · Date: 2026-05-24*

# 319/2 — Working-artifacts triage (designer/297-314)

Per the frame at
`/home/li/primary/reports/designer/319-schema-stack-context-maintenance-sweep/0-frame-and-method.md`,
this is Subagent B's slice covering the 13 by-construction
finite-lifetime working artifacts under `reports/designer/`:
five design reports (297-301), two audits (302, 304), three
sweeps (303, 306, 311), one consolidation sweep (314), one
roadmap (310), and one handover (313).

Each row carries the substance-status assessment (LANDED /
IN-FLIGHT / STALE), recommended action (DROP / FORWARD /
MIGRATE / KEEP), the citation that justifies the action, and
the design-rationale guard per `skills/context-maintenance.md`
§3a.

## §1 Verification corpus

Beads queried via `bd show <id>` (state captured 2026-05-24):

| Bead | State | Relevance |
|---|---|---|
| `primary-915w` | CLOSED 2026-05-23 | /301 elegant signal_cli! foundation (commit `468357ef` in signal-frame) |
| `primary-uxq1` | CLOSED 2026-05-23 | /301 first persona-spirit proof |
| `primary-fka1` | CLOSED 2026-05-23 | /297 rename epic (all sub-beads closed) |
| `primary-fka1.1` | CLOSED 2026-05-23 | /297 crate rename signal-persona-auth → signal-persona-origin |
| `primary-8r1j` | OPEN P1 | /298 Help auto-injection (NOT closed; absorbed into `primary-ezqx` consolidated macro epic) |
| `primary-uq04` + sub-beads | mostly OPEN | /301 per-component CLI migration sweep |
| `primary-0m1u` | OPEN P1 EPIC | /318 persona-prefix rename wave (active execution per operator/169) |
| `primary-ezqx` | OPEN P1 EPIC | Consolidated signal_channel! + signal_cli! macro extension (absorbs 915w/uxq1/8r1j/l02o/v5n2/3cl1) |

Code state checked:

- `/git/github.com/LiGoldragon/signal-persona-origin/` — repo exists
  with `Cargo.toml`, `ARCHITECTURE.md`, `src/` per directory listing
  (rename per /297 has landed).
- `/git/github.com/LiGoldragon/signal-frame/src/caller.rs` — `pub
  struct Caller` and `impl Caller` exist (`grep "Caller"`
  output), confirming `primary-915w` close-reason
  "Implemented signal-frame signal_cli foundation in commit
  468357ef: Caller capture, Request caller field, shared
  SingleArgument/ClientShape, full signal_cli main generation"
  is truthful.
- `signal-persona-origin/ARCHITECTURE.md` — does NOT carry a
  "Trust gradient" section nor compose `Caller` into
  `IngressContext` yet (verified by `grep -nE "(Trust|Caller)"`).
  The /301 ARCH-side composition therefore has NOT fully landed.

Successor reports / artifacts:

- /312 (recursive Help on every enum) supersedes /298's flat
  Help model per /313 §2 explicit "Superseded by /312".
- /318 meta-dir (upgrade merger + persona-prefix rename) is
  the operator-executing wave of /310's booking.
- /317 meta-dir (sema-upgrade and macro convergence audit)
  cites /298 + /301 + /313 + /314.
- /315 (sema-upgrade current state) and /316 (forge family
  current direction) are the consolidations /314 produced.

## §2 Per-report triage

### §2.1 /297 — design-signal-persona-auth-rename

| Field | Value |
|---|---|
| Path | `reports/designer/297-design-signal-persona-auth-rename.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home for substance | `signal-persona-origin/` repo (rename complete per `primary-fka1.1` CLOSED; ARCH at `/git/github.com/LiGoldragon/signal-persona-origin/ARCHITECTURE.md`); Spirit record 264 carries the ratified rename target |
| Design-rationale guard? | NO — enumerates three candidates but psyche chose one and the rename has fully landed; the rationale is captured in Spirit record 264's body |
| Reason | The crate rename signal-persona-auth → signal-persona-origin was psyche-ratified (spirit 264), bead-filed and CLOSED (`primary-fka1.1`), and the directory now exists at the new path. /297's three rename candidates and analysis served as the proposal; the chosen candidate is now ground truth in the repo. No residual design substance. Citations from /299, /301, /318 are historical; update or drop those See-also entries when their host reports retire. |

### §2.2 /298 — design-help-operations-in-components

| Field | Value |
|---|---|
| Path | `reports/designer/298-design-help-operations-in-components.md` |
| Substance status | STALE (superseded) + IN-FLIGHT (bead) |
| Recommended action | DROP |
| Target home for substance | Successor report `/312` (recursive Help on every enum, per spirit 363+364+365); skill `skills/component-triad.md` §"Help operations — discovery through NOTA, not through flags" (landed by /303 manifestation); bead `primary-8r1j` (OPEN, absorbed into `primary-ezqx` consolidated macro epic per operator/167 item 1) |
| Design-rationale guard? | NO — /298 proposes a single flat Help model; /312 supersedes it with the recursive-Help-as-noun model (different design, not "competing alternatives in same report") |
| Reason | /313 §2 explicitly states "/298 Help operations in components (flat model) — Superseded by /312". Three substance destinations are accounted for: the discipline lives in `skills/component-triad.md`; the bead `primary-8r1j` carries the implementation scope (and its DEEPER SCOPE note explicitly cites the convergence with `primary-l02o` and signal_cli — so the macro-convergence epic carries forward); the recursive-Help correction is in /312. Nothing in /298 is load-bearing beyond what /312 + the skill + the bead carry. |

### §2.3 /299 — design-origin-process-and-agent-identity

| Field | Value |
|---|---|
| Path | `reports/designer/299-design-origin-process-and-agent-identity.md` |
| Substance status | IN-FLIGHT (partial) |
| Recommended action | KEEP (with design-rationale guard) |
| Target home for substance | Two halves: (a) SO_PEERCRED mechanism analysis — substance is in `signal-persona-origin/ARCHITECTURE.md` §4 (verified line 48 "Boundary trust lives outside this crate" and §"IngressContext"); (b) agent-identity Option 1/2/3 analysis — NOT yet decided by psyche; serves as the rationale archive for the eventual choice |
| Design-rationale guard? | YES — explicitly enumerates Options 1/2/3 for closing the per-process / per-agent gap (Option 1 pid-in-ConnectionClass, Option 2 agent self-id in NOTA, Option 3 long-lived agent socket) with tradeoffs |
| Reason | /299 is the canonical design-rationale carrier for the agent-identity question. Spirit records 308 (parallel subagent dispatch) and 329 (agent component abstracts harness backends) name persona-agent as the harness-multiplexing surface, but /299's three options remain the comparative analysis. Per `skills/context-maintenance.md` §3a, do NOT delete; ADD STATUS-BANNER naming where the chosen option will eventually land (`signal-persona-agent` ARCH once `primary-gvgj.1` lands). Until that decision is made, /299 is load-bearing as the option enumeration. |

### §2.4 /300 — design-cli-macro-caller-context-injection

| Field | Value |
|---|---|
| Path | `reports/designer/300-design-cli-macro-caller-context-injection.md` |
| Substance status | LANDED (superseded by /301) |
| Recommended action | DROP |
| Target home for substance | Successor report `/301` (elegant signal_cli! with Caller — the refined version of /300's proposal); CODE in `/git/github.com/LiGoldragon/signal-frame/src/caller.rs` (verified by `grep`); CODE in `signal-frame/src/request.rs` `caller` field (per `primary-915w` close-reason); bead `primary-915w` (CLOSED 2026-05-23, commit `468357ef`) |
| Design-rationale guard? | NO — /300 is the first proposal; /301 supersedes with a more elegant shape; substance is identical (CallerContext-bundle via getppid + /proc reads), not competing alternatives |
| Reason | /300 introduces the CallerContext bundle, getppid+/proc capture, advisory-vs-authoritative trust gradient. All three are in /301's expanded design and in the actual signal-frame code (`Caller`, `Caller::from_kernel`, `Request.caller` field). /301's See-also explicitly lists /300 as predecessor. Removing /300 loses nothing /301 doesn't carry. |

### §2.5 /301 — design-elegant-cli-macro-with-caller-injection

| Field | Value |
|---|---|
| Path | `reports/designer/301-design-elegant-cli-macro-with-caller-injection.md` |
| Substance status | LANDED (mostly) + IN-FLIGHT (per-component sweep) |
| Recommended action | KEEP — until the per-component CLI migration sweep closes |
| Target home for substance | CODE in `signal-frame/src/caller.rs`, `signal-frame/src/request.rs`, `signal-frame/src/command_line.rs` (the existing `signal_cli!` macro per `primary-915w` close-reason); CODE per-component first-proof in `persona-spirit/src/bin/spirit.rs` (per `primary-uxq1` CLOSED close-reason "spirit binary is a one-line signal_frame::signal_cli! invocation"); ARCH composition into `signal-persona-origin/ARCHITECTURE.md` §"Trust gradient" — NOT yet landed (verified by grep — section absent) |
| Design-rationale guard? | NO — /301 proposes a single shape (one-line `signal_cli!(name, contract_crate)`); no competing alternatives to preserve |
| Reason | The foundation has landed (`primary-915w` CLOSED, `primary-uxq1` CLOSED). Three pieces still depend on /301 as the design source: (i) the per-component CLI migration sweep `primary-uq04` (P2 OPEN with .1 CLOSED, .2/.3/.4 OPEN); (ii) the macro-convergence epic `primary-ezqx` absorbs /301 + /298 + LogVariant per operator/167 item 1; (iii) the `signal-persona-origin/ARCHITECTURE.md` §"Trust gradient" addition (named in /301 §"Daemon side — typed composition" but not yet in ARCH). When `primary-uq04` closes and the Trust-gradient ARCH section lands, /301 can DROP — substance will be fully migrated. Until then, KEEP as the design source. |

### §2.6 /302 — audit-recent-operator-work-2026-05-23

| Field | Value |
|---|---|
| Path | `reports/designer/302-audit-recent-operator-work-2026-05-23.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home for substance | Outputs of the audit: (1) `primary-fka1` (rename epic) CLOSED — addressed the "rename intent not propagating to new code" finding (/302 §"Weaknesses and drift" item 1); (2) operator/167-169 absorbed the systemd / Spirit retrofit / decompose-epics recommendations; (3) `skills/designer.md` §"Audits feed into bead filing" (landed by /303 manifestation per spirit 256); (4) git commits referenced by file:line (e.g., `persona@srrkotlpouuk` "supervise spirit per engine") — historical record persists in jj log |
| Design-rationale guard? | NO — audits are by-construction finite-lifetime working artifacts per `skills/reporting.md`; no design alternatives enumerated |
| Reason | /302 is an audit dated 2026-05-23 of operator reports 157-163 + that-day's commits. Per `skills/context-maintenance.md` §"Anti-patterns", audits retire when their findings address. Every finding has a successor: rename slippage closed by `primary-fka1`; "no operator reports for today's commits" addressed in subsequent operator workflow; sema-upgrade-handover-temporary observation absorbed into /315 (sema-upgrade and handover current state — landed by /314); Spirit v0.1.0 retrofit blocker tracked as `primary-wdl6` OPEN; rename pass landed. The recommendations to designer (file rename bead, land systemd UnitController) both completed. Audit substance survives in its outputs. Per spirit 370 the report itself is retrievable from commit tree if needed. |

### §2.7 /303 — intent-manifestation-sweep-2026-05-23

| Field | Value |
|---|---|
| Path | `reports/designer/303-intent-manifestation-sweep-2026-05-23.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home for substance | Direct outputs: `skills/designer.md` §"Designer authority — Pattern-based decisions" + §"Designer authority — High-ratification-probability recommendations" + §"Designer authority — Gap-closure framing" + §"Audits feed into bead filing"; `skills/beads.md` §"Duplicate — preserve information from both"; `skills/component-triad.md` §"Help operations — discovery through NOTA, not through flags"; `signal-persona-origin/ARCHITECTURE.md` §1 ComponentName bullet (extended with rename note). All seven listed in /303 §2 table. /304's classification table item 256 confirms `skills/intent-manifestation.md` §"Pattern-based decision" + §"High-ratification-probability" carry the rule. |
| Design-rationale guard? | NO — manifestation sweeps are by-construction finite-lifetime working artifacts; no design alternatives enumerated; the §3 skip-list is historical context only |
| Reason | /303 is a designer-subagent manifestation pass dispatched in parallel with /304. Its outputs (5 skill/AGENTS edits + 1 per-repo ARCH edit + 1 subsection in existing skill) all landed and are independently verifiable. The skipped-records list (§3) and cross-cutting observations (§4) are working-artifact prose without permanent value. Per /313 §2 entry "Subagent A | 7 records homed in skills/designer.md + skills/beads.md + skills/component-triad.md + signal-persona-origin ARCH" — the manifestation is complete. |

### §2.8 /304 — unimplemented-intent-audit-2026-05-23

| Field | Value |
|---|---|
| Path | `reports/designer/304-unimplemented-intent-audit-2026-05-23.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home for substance | Direct outputs: bead `primary-8r1j` (Help auto-injection, filed per §3.1) OPEN now absorbed into `primary-ezqx`; bead `primary-ft29` (winnow audit, filed per §3.2 per /313 §"Standalone beads filed this session") — listed in /313; bead-state hygiene primary-uzpv reconciliation (§3.3) — `primary-fka1` CLOSED accomplishes this implicitly. The classification table (§2) catalogs Spirit records 217-277 with state-at-audit; states have moved (e.g., 263 Help is now in `primary-ezqx`; 264 rename CLOSED; 326 absorbed into /305-v2). Auditor mechanism design (§5.1) absorbed into AGENTS.md §"Possible additional role". |
| Design-rationale guard? | NO — audits are by-construction finite-lifetime working artifacts; classification analysis served its decision-support purpose |
| Reason | /304 audit was the substance-source for the three operator-bead recommendations in §3 (Help, winnow, primary-uzpv close). All three actions taken per /313 §2 bead list. The (b)-class catalogue is a snapshot whose authoritative state now lives in `bd ready` / `bd show`. The (d)-class items 234/235 are absorbed into AGENTS.md §"Possible additional role". /317 §0 mentions /313's macro convergence framing supersedes /304's macro pivot observation (§6.2). The audit's job is done. |

### §2.9 /306 — manifestation-sweep-round-2-2026-05-23

| Field | Value |
|---|---|
| Path | `reports/designer/306-manifestation-sweep-round-2-2026-05-23.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home for substance | Direct ARCH edits: `signal-cloud/ARCHITECTURE.md` §"Public Operations" + §"Ordinary vs owner split"; `owner-signal-cloud/ARCHITECTURE.md` §"Public Operations" + §"Ordinary vs owner split"; `domain-criome/ARCHITECTURE.md` §§"Content-addressed per-domain authority" + "Runtime hard constraints"; `arca/ARCHITECTURE.md` §"Cascade migration discipline"; `persona/ARCHITECTURE.md` §1.6.7 (extended); `INTENT.md` §"Optional third 'stable' branch is deferred". Beads filed: `primary-kbmi.4` P1 (cloud Plan-to-owner), `primary-kbmi.2.1` P1 (domain-criome NotAuthoritative), `primary-srmq` P1 (lojix nix-auth), `primary-0xn7` P2 (arca schema_header) — all listed in /313 §"Cloud track sub-beads". |
| Design-rationale guard? | NO — manifestation sweep, no competing alternatives enumerated |
| Reason | Round-2 manifestation pass companion to /303 and /304. All five ARCH files + INTENT.md edits landed and are checkable; all four beads filed and visible via `bd`. Per /313 §2 entry "Subagent C | 8 intents homed across cloud/persona/arca ARCH; 4 beads filed" — work complete. Cross-cutting observations (§5.1 cloud-feedback-loop, §5.2 continuous-runtime, §5.3 external-state mirror pattern, §5.4 not-touched) are session retrospective without further migration value. |

### §2.10 /310 — meta-overhaul-booking-roadmap

| Field | Value |
|---|---|
| Path | `reports/designer/310-meta-overhaul-booking-roadmap.md` |
| Substance status | LANDED (substance migrated to /317 + /318 + beads) |
| Recommended action | DROP |
| Target home for substance | The roadmap's five waves migrated to: Wave 1+2 → bead `primary-ezqx` consolidated macro epic (per operator/167 item 1 "macro work is now a single strategic landing"); Wave 1 individual beads (`primary-li0p`, `primary-2cjv`, `primary-3cl1`, `primary-v5n2`, `primary-avog`, `primary-9dce`) filed and visible via `bd show`; Wave 3 → `primary-gvgj` epic + 10 sub-beads (visible in bd list); Wave 4 → `primary-07ot` (router-ack), `primary-bann` (spirit socket_ingress tap); Wave 5 → `primary-fka1` epic (CLOSED), `primary-0m1u` epic OPEN (executing under /318 R1-R12). Two refinement waves followed: /317 audit (sema-upgrade + macro convergence) and /318 wave (upgrade merger + persona-prefix rename — currently executing per operator/169). |
| Design-rationale guard? | NO — roadmaps are by-construction finite-lifetime working artifacts; no design alternatives enumerated |
| Reason | The frame notes /310 "was the staging-ground for the wave that became /317 + /318 + the operator beads. Most substance should have migrated. Verify." Verified: all five waves are tracked elsewhere. The bead inventory in /310 §8 is now stale (e.g., D1-B1 became `primary-li0p`; D2-a became `primary-2cjv`; D3-EP became `primary-gvgj`). The 17 open questions in §10 were absorbed into /313 §3 (also slated for DROP) and into /317 + /318 design refinements. Per spirit 369, the upgrade-merger direction (from Wave 1's "consolidated macro PR pair") evolved into the upgrade triad merger that /318 is now executing. The roadmap served as the staging ground; the execution is happening. |

### §2.11 /311 — context-maintenance-sweep-2026-05-23

| Field | Value |
|---|---|
| Path | `reports/designer/311-context-maintenance-sweep-2026-05-23.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home for substance | Outputs are the deletions executed (per spirit 370 retrievable from jj log): ~100+ reports retired across designer, second-designer, third-designer, operator, second-operator-assistant, system-specialist, system-designer, cluster-operator, poet-assistant. Permanent-doc edits in §3 landed: `skills/component-triad.md` citation removal, `INTENT.md` citation removal, surviving-report citation redirects to `criome/ARCHITECTURE.md`. Two "lane empty after sweep" findings (second-operator-assistant, poet-assistant) flagged for lane-retirement consideration. The "Notes for prime designer" §5 observations forwarded into /313 §5 (and from there into the next-sweep retire list /314 acted on). |
| Design-rationale guard? | NO — sweep reports are by-construction finite-lifetime; the substance IS the deletions (per spirit 370) |
| Reason | The frame's analysis is exactly correct: "/311 (context-maintenance sweep) is itself a sweep report — its outputs were the deletions it executed. Likely DROP (its work is the deletions in git history)." Per spirit 370 (ratified 2026-05-24) "Deleted reports live in version-control history and can be read from the commit tree" — the sweep's lineage is preserved without keeping the sweep report itself. The "Notes for prime designer" small thoughts (Arca /139 migration, whisrs /1 + /2 migration target, meta-dir hygiene) are forwardable into a small permanent note if any still matter, or absorbed naturally. /314 already executed the next-wave retirements /311 named. |

### §2.12 /313 — great-summary-and-handover-2026-05-24

| Field | Value |
|---|---|
| Path | `reports/designer/313-great-summary-and-handover-2026-05-24.md` |
| Substance status | LANDED (handover absorbed) |
| Recommended action | DROP |
| Target home for substance | The session-handover substance migrated to: (a) all the design reports it summarises (each separately tracked: /297-/301, /305-v2, /306-/312, /314, /315, /316); (b) Spirit records 308, 323-330, 359-365 captured during the session and now part of permanent intent log; (c) the bead pool snapshot in §4 is now the live `bd` state; (d) /317 §0 explicitly cites "/313's macro convergence framing" — the macro-convergence summary is in /317; (e) /318 is the operator-executing wave of /313's "next operator session" pickups in §6; (f) the 17 open questions in §3 have been resolving through subsequent intents (e.g., 367 macro convergence, 369 upgrade merger, 371 persona-prefix). |
| Design-rationale guard? | NO — handovers are by-construction finite-lifetime; per `skills/context-maintenance.md` "The handover report retires once the substance migrates to its right permanent home or the next-session work absorbs it" |
| Reason | The frame's analysis matches: "/313 (great summary + handover 2026-05-24) was a handover for a session; its forward-targets should be in active work now. Likely DROP." Verified by /317 + /318 active execution + operator/167-169 absorbing the handover targets. The 17 open questions are either now-decided (records 367, 369, 371 ratified subsets) or remain open in subsequent design reports (/317, /318). The session's substance lives in (a)-(f) above; the handover paraphrase has served its purpose. Note: the "macro-pivot pattern" observation (§5 first note) is worth folding into `skills/component-triad.md` if not already there — small thought; lossless to drop /313 if absorbed elsewhere or surfaced once into the skill. |

### §2.13 /314 — aggressive-consolidation-sweep-2026-05-24

| Field | Value |
|---|---|
| Path | `reports/designer/314-aggressive-consolidation-sweep-2026-05-24.md` |
| Substance status | LANDED |
| Recommended action | DROP |
| Target home for substance | Direct outputs: (a) two new reports /315 (sema-upgrade and handover current state) and /316 (forge family current direction) — both exist and listed in `ls reports/designer/`; (b) ten file deletions (270, 271, 273, 274, 286, 288, 289, 290, 295, 296) — retrievable from jj log per spirit 370; (c) surviving-report citation cleanups in /263, /291, /292, /302, /304, /22/2, /22/4, /23/3, /161/2, /162/4b (§5 table) — all landed; (d) bead description updates for `primary-ib5n` and `primary-yp6k` referencing /315 and /316. The two "Notes for prime designer" observations (Mirror-payload settled-state collapse; deploy carve-out bead) forwardable as small notes if still actionable. |
| Design-rationale guard? | NO — consolidation sweeps are by-construction finite-lifetime; the substance IS the consolidated successors (/315, /316) + the deletions |
| Reason | The frame's analysis matches: "/314 (aggressive consolidation sweep) created /315 + /316 and deleted 10 reports. Its outputs migrated; likely DROP." Verified: /315 and /316 exist at expected paths; the ten retired reports are absent from the current `ls` listing; the citation-cleanup edits are mechanical and complete; the bead descriptions reference the new successors. The aggressive-consolidation methodology is captured in spirit record 362 and now part of context-maintenance discipline. The sweep itself has fully served its purpose. |

## §3 Summary table

| Path | Status | Action | Guard? |
|---|---|---|---|
| /297 design-signal-persona-auth-rename | LANDED | DROP | NO |
| /298 design-help-operations-in-components | STALE+IN-FLIGHT | DROP | NO |
| /299 design-origin-process-and-agent-identity | IN-FLIGHT | KEEP | YES |
| /300 design-cli-macro-caller-context-injection | LANDED | DROP | NO |
| /301 design-elegant-cli-macro-with-caller-injection | LANDED+IN-FLIGHT | KEEP | NO |
| /302 audit-recent-operator-work | LANDED | DROP | NO |
| /303 intent-manifestation-sweep | LANDED | DROP | NO |
| /304 unimplemented-intent-audit | LANDED | DROP | NO |
| /306 manifestation-sweep-round-2 | LANDED | DROP | NO |
| /310 meta-overhaul-booking-roadmap | LANDED | DROP | NO |
| /311 context-maintenance-sweep | LANDED | DROP | NO |
| /313 great-summary-and-handover | LANDED | DROP | NO |
| /314 aggressive-consolidation-sweep | LANDED | DROP | NO |

**Tally:** 11 DROP · 2 KEEP (/299 with design-rationale STATUS-BANNER; /301 until per-component sweep + ARCH composition close) · 0 FORWARD · 0 MIGRATE (substance from MIGRATE-shaped candidates already landed via subsequent work).

## §4 Notes for the orchestrator synthesis

### §4.1 Two STATUS-BANNER candidates if /299 retires later

/299 is the only design-rationale guard in this slice. If a later
sweep wants to retire it after the agent-identity question is
psyche-resolved, the STATUS-BANNER should name:

- The chosen option (1/2/3) per the eventual psyche decision.
- The ARCH home for the chosen mechanism — likely
  `signal-persona-agent/ARCHITECTURE.md` if Option 3 (long-lived
  agent socket) wins, since `primary-gvgj` is creating the
  persona-agent triad; or `signal-persona-origin/ARCHITECTURE.md`
  if Option 1 or 2 wins.
- Spirit record number for the agent-identity decision.

Until the decision is made, /299's KEEP is load-bearing rationale.

### §4.2 /301 retires when two things land

(1) `primary-uq04` sub-beads .2/.3/.4 close (all CLI binaries
migrated to one-line `signal_cli!` invocation). (2) The Trust
gradient section is added to `signal-persona-origin/ARCHITECTURE.md`
composing `Caller` into `IngressContext` (named in /301 §"Daemon
side — typed composition" but not yet in ARCH per grep). Once
both land, /301 can DROP and the substance is fully in code +
ARCH + the macro convergence epic.

### §4.3 Small thoughts worth surfacing

Per `skills/context-maintenance.md` §4 "Small thoughts are OK":

- **note:** The "macro-pivot pattern" observation from /313 §5
  (signal_channel! emits frame.micro + LogVariant + Help recursively
  + signal_cli! emits CLI binary — macro layer is workspace's
  universal cross-component capability surface) is worth a
  sentence in `skills/component-triad.md` §"Help operations" or
  a new §"Macro-layer convergence" if it recurs. Currently
  carried in /313 + /317 §0. If neither lands it as a skill rule,
  it gets lost when both retire. Designer-orchestrator decision:
  surface it now or wait for one more pivot to confirm the
  pattern.

- **note:** /304's §6.3 "Three-tier signal sizing has a full
  bead chain — it just needs operator pickup" — chain is
  `primary-l02o` → `primary-bg9l` → `primary-2py5` → `primary-b86d`
  → `primary-k8cn`. All P1 OPEN per `bd list`. Worth re-stating
  in the orchestrator's overview as a still-relevant pickup
  recommendation (it survived the macro-convergence absorption
  because it's per-triad LogVariant work, not the macro extension
  itself).

- **note:** The lane-retirement candidates flagged in /311 §5
  (second-operator-assistant, poet-assistant — both empty after
  /311's sweep) are still in `orchestrate/roles.list` per the
  context-maintenance §"Retiring a lane" guard. Not in this
  slice's scope, but worth a sentence in the orchestrator's
  overview if the psyche is invited to retire them.

### §4.4 Cross-citations the orchestrator should clean

If /297-/301 all DROP per this triage, dead citations land in:

- /318 meta-dir (cites /301 in `2-rename-tooling-and-mechanics.md`
  per grep — verified citation to "/301 (elegant CLI macro with
  Caller)" in /317 actually, not /318; verify in orchestrator
  pass).
- /317 meta-dir cites /298 (flat Help extended by /312) and /301
  (elegant CLI macro with Caller) in `2-macro-current-state-audit.md`,
  and /313 + /314 in `0-frame-and-method.md`.
- /293 meta-dir likely cites /297-/301 (sibling-session reports).
- /302's See-also cites /293 + /285.

The orchestrator's overview should batch the dead-citation
cleanup as part of executing the DROPs, per the discipline in
/311 §3 and /314 §5.

### §4.5 Aggressive defaults per spirit 362

Per spirit record 362 (Maximum, ratified 2026-05-23), "Aggressive
consolidation supersedes conservative context maintenance when
psyche directs it." The frame at §2 echoes this with "aggressive
per spirit 362". This slice's 11 DROPs are aggressive — every
DROP is justified with a cited successor (bead state, repository
state, ARCH presence, successor report, or git-tree retrievability).
No DROP is "absorbed somewhere general"; each cites a specific
home.

## See also

- Frame: `/home/li/primary/reports/designer/319-schema-stack-context-maintenance-sweep/0-frame-and-method.md`
- Companion slices (when they land):
  - `/home/li/primary/reports/designer/319-schema-stack-context-maintenance-sweep/1-schema-stack-substance-triage.md` (Subagent A)
  - `/home/li/primary/reports/designer/319-schema-stack-context-maintenance-sweep/3-separate-concerns-triage.md` (Subagent C)
  - `/home/li/primary/reports/designer/319-schema-stack-context-maintenance-sweep/4-overview-and-retirement-list.md` (orchestrator synthesis)
- `skills/context-maintenance.md` §"Per item, decide" + §3a "Design-rationale guard against premature DELETE"
- Spirit records 362 (aggressive consolidation discipline), 367 (macro convergence), 369 (upgrade merger), 370 (deleted reports retrievable from commit tree), 371 (persona-prefix drop) — the late-wave intent layer informing this triage
