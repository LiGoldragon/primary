# Spirit Cleanup Plan (2026-06-26)

Principle (psyche, first-degree): Spirit stores durable **intent/direction** only.
Records that *describe how Spirit / guardian / the system / a process works* →
**manual/docs**. Records stating a *config/operational fact* (paths, URLs, nodes,
tokens, wiring) → **architecture docs**. Only direction stays a record. Misplaced
records migrate OUT (content into the doc, record retired) — careful Supersede
preserving any still-live rule.

## Store totals
1388 entries · 649 active (cert ≥ Minimum) · 739 already at Zero (removal-nominated).
Active split (after aggressive borderline call): KEEP 575 · TO-MANUAL 57 · TO-ARCH 10 · STALE 7.

## TO-ARCH (10) — config/operational facts → architecture docs, then retire
go41 (local-llm token path) · nz0t (prometheus gopass token wiring) · 16l0 (flarectl
on cloud daemon PATH) · upza (privileged ops via ssh root@host) · bdse (Playwright
token gopass path) · nsi2 (Cloudflare token → CF_API_TOKEN shim) · p6k5 (persona-spirit
prod / spirit-next pilot status) · bnxx (persona repo/binary names) · osoo (backup
WiFi password via sops-nix) · qxye (Bird/Aether forked repos)

## TO-MANUAL (43) — self-description → manual, then retire
7hrd 4ry9 rvnf zt1 zt2 zt3 zt4 j6r4 qjrf tfpd oqwb 6z6t kmhb 2o5j 4vde 8pux dctk
fwme ktub kxzh pjib rnrg us1v ospz 3ey7 ngk0 0fmg 1i1b bhs5 dfii irmw l7kt n1x8
nr7h oe6s pn0n q9iz tbg6 vjye yenl ypg9 ztX sqnx

Sub-themes: Spirit-self (qjrf, 7hrd) · guardian/certainty (j6r4, tfpd, nr7h, dfii,
vjye, 6z6t) · orchestration/role/capture process (ktub, kxzh, dctk, 2o5j, yenl,
3ey7, l7kt, irmw) · report conventions (pjib, n1x8, q9iz, pn0n, ypg9, 0fmg) ·
definitional "what X means" (4vde, fwme, 8pux, rnrg, 1i1b, ngk0, kmhb, us1v, oqwb,
oe6s, bhs5, ospz, sqnx, tbg6, 4ry9).
Duplicate cluster: zt1 zt2 zt3 zt4 rvnf ztX = six copies of one capture-gate
discipline → migrate once, remove the rest.

## STALE (7) — obsolete → retire
6cfr a9sq hc0t (VeryHigh, Asschema-IR-bound — PRESERVE the live SpecifiedSchema /
typed-codec rule already in 6grf/bkcd/kfqa before retiring) · dqmc (abandoned
@-binder) · zNEW9 ztA ztB (junk test placeholders — safe hard-remove).

## BORDERLINE (~14) — RESOLVED: AGGRESSIVE → all move to TO-MANUAL (total 57)
Guardian mechanism: i59i 7xnx kasm mrsy.
Spirit behavior / data-model: 8jtz oj3i t4uq qbx7 fiw4 rh29.
Term definitions: g78b ("refresh = read Spirit") 20hv ("landed = on main").
Vocabulary/definitional: qerc 61lk.

## Decisions (psyche)
1. Borderline policy: **AGGRESSIVE** — the ~14 borderline mechanism/behavior
   descriptions → manual. Spirit keeps only build-direction. TO-MANUAL now 57.
2. The 739 Zero-cert records: **garbage-collect** — archive first, then remove,
   via Spirit's archive-then-retract flow.
3. Target docs per record — being mapped (Spirit manual / ARCHITECTURE / skills),
   authored-vs-generated checked. PENDING execution plan.

## Execution notes
- High/VeryHigh-cert records in TO-MANUAL/TO-ARCH/STALE: careful Supersede, not bare
  Remove; preserve any still-live rule in the doc + a surviving record.
- All 649 active are Privacy Zero (no private substance) — safe to migrate publicly.

## Execution grounding (doc map + commands)

Doc targets (authored, in-tree, committable unless noted):
- intent-log.md ← capture/Spirit-self: 7hrd qjrf tfpd mrsy + dup-cluster rvnf/zt1-4/ztX (migrate once)
- intent-maintenance.md ← 6z6t tbg6
- intent-led-orchestration.md (+ Codex mirror .agents/skills/.../SKILL.md) ← ktub kxzh dctk 2o5j 3ey7 l7kt
- reporting.md / report-naming.md / architecture-editor.md / context-handover.md ← pjib n1x8 q9iz ypg9 us1v 0fmg pn0n 4ry9
- workspace-vocabulary.md ← qerc bnxx 1i1b kmhb ngk0 20hv
- nota-design.md / structural-forms.md ← oqwb bhs5 rnrg oe6s 61lk
- schema skills (component-triad / schema-designer) ← 4vde fwme ospz 8pux sqnx (in-tree fallback); irmw → session-lanes.md
- spirit-cli.md (TRANSITIONAL; durable home = spirit repo, generated per xblw) ← 7xnx kasm dfii i59i + the already-covered set

Already-covered (Retire only, no new writing): j6r4 nr7h vjye t4uq fiw4 rh29 8jtz oj3i qbx7 g78b yenl kmhb ngk0 20hv q9iz.

Spirit commands (guardian-gated; Justification needs VERBATIM psyche testimony, paraphrase → MissingTestimony):
- Supersede (retire + affirmative replacement) — preserve live rule.
- Retire (deactivate, no replacement).
- Remove (hard) — junk only: zNEW9 ztA ztB.
- GC 739 Zero: CollectRemovalCandidates with ExactCertainty Zero filter — archives then removes; restorable via ChangeCertainty.

Asschema STALE: 6cfr a9sq hc0t → Supersede preserving SpecifiedSchema/typed-codec rule (held in active 6grf/bkcd/kfqa) before retiring; dqmc → Retire.

BLOCKED — home is an UNTRACKED repo (can't commit from primary main), no in-tree fallback:
TO-ARCH config facts: go41 nz0t upza osoo 16l0 nsi2 bdse p6k5 qxye (9). [bnxx → workspace-vocabulary.md, in-tree, OK]

Phasing: Phase 1 = all in-tree (57 manual + bnxx + 7 stale = 65 records) + 739 GC. Phase 2 = the 9 blocked config facts (psyche call: hold / edit-untracked-repos / transitional in-tree doc).

## CORRECTION (psyche — approved-with-corrections)
- Destination is the MANUAL, not skills (do NOT bloat skills). The manual is the new
  semi-standard: something simple — a single manual.md or a book-style directory.
- Spirit-mechanism records → a real manual in the spirit repo (repos/spirit/manual.md).
- Config facts → the relevant component's architecture file OR a manual in its repo
  (CriomOS-home, persona, spirit, cloud — create where missing). No "hold in Spirit".
- Descriptive/concept records → simple per-domain manuals, not skills.
- Execution APPROVED. Order: author manual/arch content first, verify coverage, THEN
  retire/supersede the records; GC the Zero-cert pile (archived first).
