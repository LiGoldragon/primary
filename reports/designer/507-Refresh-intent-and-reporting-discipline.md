---
title: 507 — Refresh: intent and reporting discipline
role: designer
variant: Refresh
date: 2026-06-04
topics: [intent-log, reporting, context-maintenance, skill-cleanup, certainty, report-headers]
description: |
  Agglomerated refresh of the intent-and-reporting-discipline cluster
  (former designer reports 351, 352, 472, 489, 490, 491, 494). Nearly
  all of this cluster's discipline substance has matured into permanent
  skills — intent-log.md, intent-maintenance.md, context-maintenance.md,
  reporting.md — so those parts are migrated-and-dropped, named here
  only as landing witnesses. What survives as a live working artifact is
  ONE punch list: the eight stale-report-citation and drift findings the
  489 audit surfaced in skill files, still unfixed as of 2026-06-04.
  Everything else (the 2026-05-26 intent-log audit flags, the pseudo-NOTA
  header migration, the workspace update survey, the end-of-day state) is
  superseded by skill landings or by ~1850 newer Spirit records and
  retires. Proposes two testable constraints to the permanent layer.
---

# 507 — Refresh: intent and reporting discipline

## Why this refresh exists

Seven older designer reports (351, 352, 472, 489, 490, 491, 494) all
sat on one topic arc: **how the workspace captures intent and how it
shapes reports**. Read together at 2026-06-04, almost all of their
substance has either matured into a permanent skill or been superseded
by the intent log moving on by roughly 1850 records. This refresh
absorbs the arc, names exactly where each piece landed, and keeps the
one part that is still a live working artifact.

The rule applied is `skills/context-maintenance.md`
§"3a · Migrate live patterns first, then retire" and §"Staleness has a
landing gate": a report drops only after its load-bearing substance is
witnessed in a successor surface. Below, every drop names its witness.

## The one live working artifact — the 489 skill-cleanup punch list

The 489 audit (2026-06-03) found that the report-header *discipline*
had drifted in practice and fixed it (that fix is fully landed — see
§"Migrated and dropped" below). But the same audit's §C.1 surfaced a
**second, separable** finding: skill files carry stale citations of
deleted reports and retired lanes, in direct violation of
`skills/skill-editor.md` §"Skills never reference reports". That punch
list has NOT yet been worked. Verified live on 2026-06-04 — every row
below still matches in the named skill file:

| Skill file | Stale reference | Severity | Fix |
|---|---|---|---|
| `reporting.md` | §"Worked example" cites `reports/second-designer/152-persona-engine-architecture-overview/` (consolidated into 162/3 and deleted, `3307c471`) | Stale citation | Replace with a live meta-report directory, or remove the worked-example block (skills shouldn't cite reports). |
| `kameo.md` | cites `reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md` (retired lane + deleted report `c93c9888`) | Stale citation | Inline the `StoreKernel`-deferral / persona-mind-gap finding if load-bearing, else remove. |
| `actor-systems.md` | same `operator-assistant/138-…` citation | Stale citation | Inline or remove. |
| `intent-manifestation.md` | cites `reports/designer/232-persona-spirit-new-component.md` (deleted) | Stale citation | Remove; the persona-spirit forward direction lives in INTENT.md + `skills/spirit-cli.md`. |
| `autonomous-agent.md` | cites `reports/operator/205-spirit-next-schema-pilot-implementation-2026-05-26.md` (deleted) | Stale citation | Replace with a `reports/<role>/<N>-…md` placeholder. |
| `contract-repo.md` | cites `reports/designer-assistant/125-v2-contract-local-verbs-vs-sema-core-verbs.md` (retired lane + deleted) | Stale citation | Inline the contract-local-verb vs Sema split if load-bearing, else remove. |
| `testing.md` | cites `reports/designer/211-persona-terminal-consolidation-one-daemon-2026-05-17.md` §7/§11 (deleted) | Stale citation | Inline the persona-terminal-daemon rationale if load-bearing, else remove. |
| `poet.md` | mentions `reports/poet-assistant/` as a lane subdirectory (retired per Spirit 920) | Drift | Update to `second-poet`. |

One related item from the same audit is **already fixed** and listed
only so it is not re-opened: the `owner-signal` → `meta-signal` rename
landed in `AGENTS.md` (commit `c1b7f17d`, zero `owner-signal` matches
now). It still survives in `skills/component-triad.md` (two matches) —
fold that into the cleanup batch.

The whole punch list is mechanical: each row is inline-the-substance-
or-remove-the-pointer. It is dispatchable as a single sub-agent batch
with the same shape as the 47-report YAML migration. When the batch
lands, this refresh's only live function is discharged and the refresh
itself becomes retirement-eligible.

## Migrated and dropped — discipline that now lives in skills

Each item below was load-bearing when its source report was written and
is now fully in a permanent skill. The source reports retire; the skill
is the witness.

### Intent capture and audit discipline (from 351, 352)

The 2026-05-26 intent-file-tour (351) and intent-log audit (352)
taught a discipline that is now entirely in the skills:

- **Intent lives in the file that owns its scope** — workspace
  `INTENT.md` for workspace-shape intent, per-repo `INTENT.md` for
  repo intent. Witness: `skills/intent-manifestation.md` (where intent
  statements land) + `AGENTS.md` §"Required reading" pointing each repo
  at its own `INTENT.md`.
- **Don't infer to close incomplete design; ask the psyche.** Witness:
  `AGENTS.md` §"Psyche is the human; intent is primordial; ask when
  unclear" + `skills/intent-log.md` §"Conservative by default — never
  overextend".
- **Audits flag, never delete unilaterally; tombstone before removal.**
  Witness: `skills/intent-maintenance.md` §"Removing a record —
  tombstone first" + §"Sweep — when and how" (proposes; does not
  execute; psyche/orchestrator authorises) + `skills/intent-log.md`
  §"When a working order slips in anyway".
- **Work orders are not intent — the after-the-task test.** Witness:
  `skills/intent-log.md` §"The pre-capture gate — the after-the-task
  test" (carries the exact failing-shape table that 352's H5–H11
  flagged in record form) + `AGENTS.md` §"Capture intent through the
  right intent substrate FIRST" §"Working orders are NOT intent".
- **Dedup: earlier capture wins by default; consolidate duplicate
  clusters.** Witness: `skills/intent-maintenance.md` +
  `skills/context-maintenance.md` §6 "Spirit capture sweep".

The **specific 2026-05-26 flags** in 351 and 352 (the five file-tour
flags; D1–D18 duplicate clusters; M1–M5 misalignments; H1–H12
suspected hallucinations) are now stale as a pending-review punch
list. They audited the v0.2.0 Spirit database at ~719 records. The
live database is past **2566** records — the workspace worked all the
way through the schema-crystallization arc those flags centered on. The
headline flag (352 M1, the schema-defines-effects cluster 660–665/710)
has already been acted on: records 660 and 665 now sit at Magnitude
`Zero` in the live log (the lower-then-leave outcome the
flag-don't-delete discipline produces), and 666/668 carry the
retraction/reframe. The append-only log preserves the lineage; the
audit-as-worklist value is spent. No live decision rides on the 351/352
flag inventory.

### Context-maintenance method and the 472 ledger

Report 472 was a context-maintenance ledger (2026-06-02): it migrated
three pieces of substance into skills, removed seven Spirit duplicates,
and retired seven designer reports. All of its durable output already
lives in its destinations:

- Beauty as primary audit lens → `skills/beauty.md`.
- Typed trace identity (schema-emitted, not stringly) →
  `skills/component-triad.md` §"Trace identity is schema-emitted".
- Interface roots are enums with more than one variant →
  `skills/component-triad.md`.

The ledger's own bookkeeping (which seven duplicates, which seven
reports) is a spent working artifact: per
`skills/context-maintenance.md` anti-pattern "Keeping
successor-superseded maintenance ledgers", a maintenance ledger
retires once a newer sweep reissues its handoffs. The 491 update report
and 494 end-of-day report already re-issued the live handoff state; this
refresh re-issues it once more in §"Carry-forward". 472 drops.

### Report-header discipline and the pseudo-NOTA migration (from 489, 490)

The single biggest concrete output of this cluster — the move from the
drifted semicolon-bracket pseudo-NOTA report header to YAML front
matter — is **completely landed**:

- The discipline lives in `skills/reporting.md` §"Report header — YAML
  front matter": required fields (`title`, `role`, `variant`, `date`,
  `topics`, `description`), the closed variant set, the optional
  `parent_meta_report` / `slot` for meta-report sub-files, and the
  **explicit forbidden shape** (the pseudo-NOTA header, named as drift
  per Spirit 1528).
- The mechanical migration is done: 46 reports converted to YAML front
  matter in one batch (490 closeout), body byte-identical, all passing
  a shape check.
- The companion filename rule (variant in BOTH filename and front
  matter, Spirit 1481) is in `skills/reporting.md` §"Filename
  convention" and `skills/report-naming.md`.

So 489's Problem 1 (pseudo-NOTA origin + YAML design) and the whole of
490 (the migration witness) are spent. 489's Problem 2 / §C.1 is the
live remainder kept in §"The one live working artifact" above. 489 and
490 both drop once §C.1 is held in this refresh.

### Bracket-quote citation and Psyche-report discipline (from 491, 494)

The reporting-discipline edits that 491 and 494 narrated as
freshly-landing are now stable skill content:

- **Bracket-quote intent citation** — cite a Spirit record in prose by
  quoting its description summary as bracketed text; the bracket form
  IS the citation. Witness: `skills/intent-log.md` §"Citing intent in
  prose — bracket-quote the summary".
- **Psyche reports: show the code, narrative voice, plain-language open
  items.** Witness: `skills/reporting.md` (the Psyche-report sections).
- **Auto-edit fresh-in-context reports + v-versioning committed
  reports.** Witness: `skills/reporting.md` §"Editing fresh-in-context
  reports".
- **The Update report variant.** Witness:
  `skills/workspace-update-report.md`.
- **Report claim exemption.** Witness: `orchestrate/AGENTS.md` +
  `skills/reporting.md`.

491 (the inaugural workspace-update survey) and 494 (the 2026-06-03
end-of-day Psyche report) were both **snapshots of a single day's
moving state** — exactly the report shape that
`skills/context-maintenance.md` names as retiring "once the live state
is the baseline". One day later, that state is the baseline. Their
durable contributions (the discipline edits above) have skill homes;
their day-specific synthesis (what landed in spirit-next on 2026-06-03,
which eighteen items ratified that afternoon) is now git history and the
later Update-report chain. 491 and 494 drop, with their forward items
folded into §"Carry-forward" below so nothing pending is lost.

## Carry-forward — open items re-issued from the dropped reports

These were the genuinely-still-open items inside 491 and 494. They are
re-stated here so retiring those reports loses nothing. Anything since
resolved is omitted.

- **The 489 §C.1 skill cleanup** — the punch list in §"The one live
  working artifact". This is the primary carry-forward.
- **The component-triad `owner-signal` → `meta-signal` cascade** — done
  in `AGENTS.md`, still pending in `skills/component-triad.md` (two
  matches). Folds into the §C.1 batch.
- **SymbolPath shape — opaque `Vec<Name>` vs structured five-field
  record.** A design choice flagged in 494 §4. Designer lean:
  structured form long-run, `Vec` form acceptable as the slice-1
  baseline; promote when the Help/Description namespace lands. This is
  a live architecture question, not a discipline one — it belongs to
  the schema-stack cluster's current surface, not here. Named only so
  it is not orphaned by 494's retirement.

These are pointers, not substance — the substance for the live
architecture items lives in the current schema-stack reports and the
ratification queue, not in this discipline refresh.

## Manifestation proposals

Two pieces of this cluster's discipline are mature and leaned-on enough
to belong in the permanent layer as **constraints** (a constraint lets
us write a test, per the constraint-preference rule). Both are already
stated in prose in a skill; the proposal is to sharpen them into a
checkable form.

1. **Skills never cite report paths** — already prose in
   `skills/skill-editor.md`; the 489 §C.1 punch list exists *because*
   the rule had no enforcement. Proposed as a constraint: no
   `skills/**/*.md` file contains a `reports/` path reference. This is
   directly testable by grep.

2. **Reports carry YAML front matter, never the pseudo-NOTA header** —
   already prose in `skills/reporting.md`. Proposed as a constraint:
   every `reports/**/*.md` file begins with a `---` YAML front-matter
   block carrying the six required fields; no report body (outside a
   fenced code block) begins with a `; <lane>` line. Directly testable.

## What this refresh deletes

Source reports retired by this refresh (substance witnessed above):
351, 352, 472, 489, 490, 491, 494. Git history preserves them; this
refresh is the landing witness.
