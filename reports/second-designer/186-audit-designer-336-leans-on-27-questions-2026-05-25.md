*Kind: Audit · Topic: designer/336 leans on 27 psyche questions + MVP plan · Date: 2026-05-25 · Lane: second-designer (counter-ego)*

# 186 — Audit: designer /336 leans on 27 questions + MVP plan

## §1 Scope

Per psyche directive 2026-05-25 ("audit"), apply intent 511 (audit cycle) to `reports/designer/336-designer-leans-on-27-psyche-questions-and-mvp-plan.md`. Compare against my parallel /181 (counter-ego MVP leans) — both reports respond to the same psyche directive (lean on intent + propose MVP). Surface convergences, divergences, and one specific finding where designer's read CORRECTS mine.

## §2 Convergence with /181

Strong agreement on:

- **primary-602y as P0** — /336 §5.3 first item ("signal-frame wire compat: assumed-eventually-rebuilt"); my /181 §2 ("primary-602y bundle FIRST")
- **UpgradeMacro / schema-derived projection as high priority** — /336 Q12 + §5.2.4 ("schema-declared `(Upgrade ...)` variant"); my /181 §3 (UpgradeMacro MVP)
- **Multi-endpoint macro extension needed for orchestrate** — /336 Q21 ("SHIP NOW; blocks Orchestrate cutover"); my /181 §7 deferral (with same blocker note)
- **persona-daemon as the supervisor / fleet conductor** — /336 Q15+Q19+Q20; my /181 §7 deferral + /184 §10
- **In-test unblock-the-blocker pattern** — both reports invoke intent 547 explicitly
- **Schema-as-source-of-truth as the load-bearing pattern** — both cite intent 549 + 551-573

## §3 Complementary scope (not divergent)

/336 covers BROADER ground; /181 covers NARROWER ground:

- /336 addresses 27 specific questions across 6 clusters (handover semantics, schema engine, migration, supervisor+selector, contract promotion, intent retire/supersede)
- /181 proposes 5 concrete MVP implementation slices (primary-602y bundle, UpgradeMacro, Engine-on-Route rebase, Component+UID rebase, Storage feature)

These are different ANGLES on the same MVP target — /336 is question-by-question with confidence ratings; /181 is slice-by-slice with intent-reference tables. Together they cover both the design-question surface AND the implementation-slice surface.

/336 covers areas /181 didn't address: typed Effects capability for imports (Q7), multi-step migration composition (Q13), force-close-lingering verb authority (Q5+Q17), atomic selector flip mechanism (Q16+Q20), intent retire/supersede wire shape (Q23+Q24), audit cadence + archive policy (Q25+Q26). These weren't in my source audits' scope; designer's report fills them.

## §4 The load-bearing correction — Mirror gating per-component, not aligned

/336 §3.1 Q1 + Q4 + Q6: **Mirror gating is per-component, schema-declared, NOT to be aligned across components.** The "Spirit post-completion vs Orchestrate pre-completion" divergence I flagged in /179 §4 as a "divergence to be resolved" is reframed by /336: **both gatings are CORRECT for their respective components' semantics; the schema declares which one**.

This is a STRONG REFRAME. The pattern /336 §2 first observation: "Schema is the source of truth. Per-component variation is expressed through schema declarations, not through code branches." Applied to Mirror gating:
- Spirit's Mirror payload is empty (per /175 §9 + intent 541 simplified per "acked == durable")
- → Spirit can use post-completion gating safely; Mirror is vestigial
- Orchestrate's Mirror payload carries critical in-memory state (claims + lanes per /186)
- → Orchestrate REQUIRES pre-completion gating; the Mirror must transfer state before HandoverCompleted retires sockets

The gating IS the per-component difference. Aligning them would FORCE Spirit to a more complex protocol than it needs OR force orchestrate to a simpler protocol than its state requires. /336's read is the better one.

**My /179 §4 was WRONG to recommend alignment.** The right recommendation: each component's schema declares its `(Mirror (Gating PostCompletion))` or `(Mirror (Gating PreCompletion))` policy, and the daemon's handover logic dispatches per the policy. /336 §5.2.1 demonstrates this in the MVP test path: "schema declares the gating; test enforces it."

**My /181 §2 primary-602y bundle was WRONG to bundle Spirit Mirror phase-alignment with the wire-format backport.** The two are SEPARATE concerns: primary-602y backports ShortHeader-on-wire (correct fix); Mirror gating is per-component schema choice (no alignment needed).

**Corrections to land**:
- /179 §4: annotate with "per /336 Q1+Q4+Q6: this is intended per-component variation, not divergence to fix"
- /181 §2: revise the bundle to be ShortHeader-backport-only; remove the Spirit Mirror alignment from the bundle
- /178 §3: also revise the "should be backported to Spirit for symmetry" recommendation — Mirror phase-ordering is NOT a symmetry concern; it's a per-component schema choice

## §5 Other designer leans worth comparing to my positions

| Q | Designer /336 lean | My /181 position | Disposition |
|---|---|---|---|
| Q2 Divergence policy | typed DivergenceAction (matches typed-records discipline) | /181 §7 deferred to post-supervisor | /336 sharper; agree |
| Q3 Recovery scope | supervisor-driven retry from last marker | /181 §7 deferred to post-supervisor | /336 sharper; agree |
| Q7 Typed Effects for imports | YES (Medium confidence) | not addressed | /336 fills gap; agree direction |
| Q8 Macro registry vs hard-code | hard-code until 3rd-party arrives | implicit agreement | convergent |
| Q9 Layout-after-assemble | YES | /181 §5 includes via mockup A rebase | convergent |
| Q10 Lexer with-span replace vs coexist | replace (beauty: one canonical surface) | /184 §13 Q2 leaned same | convergent |
| Q12 Schema-diff projection ownership | contract crate owns; upgrade consumes | /181 §3 Upgrade-Macro lives in schema engine; emission goes into upgrade crate | convergent (different framing) |
| Q19 upgrade-daemon binary need | NOT needed; persona-daemon sufficient | not addressed | /336 fills gap; agree |
| Q21 Multi-endpoint macro extension | SHIP NOW; blocks Orchestrate | /181 §7 deferred (post-Spirit-MVP) | DIVERGENT — /336 prioritizes higher than mine |
| Q22 Post-promotion manual proc_macro | delete once everything schema-derived | /181 §7 implicit | convergent |
| Q23 Wire-shape extension for retire/supersede | YES — typed records | not addressed | /336 fills gap; agree |

**One real divergence**: Q21 priority. /336 says ship multi-endpoint NOW (blocks Orchestrate); my /181 §7 deferred. Designer's read: orchestrate cutover NEEDS multi-endpoint, so deferral blocks the entire orchestrate-maturity track. **Adopt /336's higher priority** — schedule multi-endpoint right after primary-602y, before UpgradeMacro.

## §6 MVP test path comparison

/336 §5 proposes a SINGLE BIG nspawn test exercising 5 leans on Spirit:
- Per-component Mirror gating (Q1+Q4)
- Typed Divergence action (Q2)
- Recovery from new-daemon-crash (Q3)
- Schema-declared `(Upgrade ...)` variant (Q12+Q13)
- Selector flip via supervisor (Q15+Q16+Q20)
- Run on Prometheus via criomos-nspawn (record 535)

Acceptance witnesses: 6 named output lines per /336 §5.4.

My /181 §9 proposed SEQUENCED INDIVIDUAL SLICES landing as separate operator beads:
- §2 primary-602y bundle first
- §4 + §5 mockup rebases parallel
- §3 UpgradeMacro after §5
- §6 Storage anytime

**Comparison**: /336's shape is NSPAWN-INTEGRATION-FIRST; /181's shape is INCREMENTAL-LANDING-FIRST. Both have merit:
- /336's nspawn test gives a single PASS/FAIL signal for "did the leans actually work end-to-end?"
- /181's incremental landings give per-slice signals + operator can ship each independently

**Recommendation**: BOTH paths run in parallel. /336's nspawn test EXERCISES leans on stubbed substrate (per record 547 in-test unblock); /181's incremental slices LAND the validated leans on production. /336's nspawn test validates that the leans work; /181's slices make them real on main.

## §7 The 5 leans /336 names as uncertain

Per /336 §4:
1. **Q5+Q17 long-lived connection authority** (owner socket vs upgrade socket vs supervisor) — Medium
2. **Q11 self-hosting meta-schema timing** — Medium (designer leans defer; I lean same per /184 §13 Q2)
3. **Q16+Q20 selector flip mechanism** (file vs symlink vs signal) — Medium
4. **Q25+Q26 audit cadence + archive policy** — Medium-low
5. **Q7 typed Effects boundary surface** — Medium

These are the parts of the lean surface that legitimately need psyche call. Designer correctly identified them as Medium-confidence (not letter-of-intent inferable). My /181 only surfaced 3 truly-open questions (§3 historical module location resolved by intent 587; §6 Storage scope, §7 Mirror dynamic_roles); designer's 5 are broader because /336 covers broader surface.

## §8 What changes about my prior work

Recommendations to act on this audit's findings:

1. **Annotate /179 §4** — Spirit Mirror phase-ordering "divergence" reframe: this is intended per-component variation per /336 Q1+Q4+Q6; not a divergence to fix
2. **Revise /181 §2** — primary-602y bundle becomes ShortHeader-backport-only; drop the Spirit Mirror alignment from the bundle
3. **Revise /178 §3 + §6** — "backport ShortHeader-validation + marker-consistency to Spirit for symmetry" is correct; "Spirit Mirror phase ordering" recommendation is WRONG and should be retracted
4. **Reorder /181 §9 sequencing** — promote multi-endpoint macro extension to immediate-second-slice (after primary-602y) per /336 Q21 priority; demote UpgradeMacro to third
5. **Adopt /336's typed DivergenceAction** approach (Q2) into the next iteration's design instead of my /181 §7 deferral
6. **Adopt /336's persona-daemon-as-fleet-conductor** framing (Q15+Q19) — drop the upgrade-daemon binary placeholder per Q19

## §9 What this audit does NOT do

- Does NOT re-litigate the 27 questions — /336's leans stand; this is comparison + correction-acknowledgment, not parallel-leans
- Does NOT propose new design beyond noting that /336's per-component-gating read should land in my prior reports
- Does NOT block any /336 work — /336 dispatches its MVP test subagent per /336 §6 step 2; that work proceeds independently
- Does NOT capture new psyche intent (intent corpus untouched by this audit)

## §10 References

- `reports/designer/336-designer-leans-on-27-psyche-questions-and-mvp-plan.md` — under audit
- `reports/designer/335-state-audit-and-test-verification/` — source of the 27 questions (referenced by /336)
- `reports/second-designer/181-counter-ego-mvp-leans-2026-05-25.md` — my parallel 5-MVP-slice report (needs §2 revision)
- `reports/second-designer/179-audit-operator-180-schema-field-name-and-upgrade-context-2026-05-25.md` — Spirit Mirror "divergence" finding (needs §4 annotation per /336 reframe)
- `reports/second-designer/178-audit-second-operator-186-orchestrate-upgrade-socket-2026-05-25.md` — Mirror phase-ordering recommendation (needs §3 + §6 revision)
- `reports/second-designer/184-fully-schema-and-nota-comprehensive-understanding-2026-05-25.md` — comprehensive synthesis (Q11 self-hosting matches /336 Q11 lean)
- `reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md` §9 — Spirit's empty Mirror payload (supporting evidence for /336's per-component gating reframe)
- Intent records 511 (audit cycle), 535 (real-world testing), 547 (in-test unblock), 549 (multi-pass NOTA-first), 561-573 (schema patterns), 583 + 584 (commit discipline + lean-on-patterns referenced by /336), 599 (research-first before dispatch)
