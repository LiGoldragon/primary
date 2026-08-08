# Skill — workspace update report

*A recurring report variant that surveys what changed in the
workspace between the previous workspace update report and now.
Files changed and why, new skills, new components, new intent
records, new patterns, retired surfaces. Periodic synthesis the
psyche reads to understand the shape of recent motion without
opening every commit.*

## What this skill is for

The workspace generates a lot of motion — Spirit captures,
commits, reports, skill edits, component changes — over the
course of any active period. An agent reading the workspace at
any single moment cannot easily see the *direction* of that
motion without rebuilding the picture from scratch. The
**workspace update report** is the recurring synthesis that
holds the direction together. Per Spirit 1530 (Decision High):
*"Workspace update reports are a new report variant. An agent
periodically surveys major workspace changes since the previous
workspace update report — files changed and why, new skills,
new components, new intent records, new patterns, retired
surfaces … Becomes part of the workspace context-maintenance
rhythm."*

The variant is `Update` (Spirit 1481 closed variant set). The
discipline is per-report-instance the same; the substance is
what changed in the named period.

## When to write one

- **Psyche explicitly requests one.** *"Do a workspace update
  report."* The most common trigger.
- **End of an extended busy period** — a major sweep, a
  multi-day implementation push, a meta-report cycle wrapping
  up. The cadence is not fixed; the report fires when there's
  enough motion to summarize.
- **Before a long context-loss event** — preparing for major
  re-platform, lane retirement, or context compaction across
  many sessions. The update report becomes the durable summary.

A workspace update report is NOT for:

- Per-commit narration (commit messages do that).
- Per-session handover (the handover variant does that).
- Auditing a specific surface (the audit variant does that).
- Capturing intent (Spirit does that).

## Method — find the baseline, survey the period

### 1. Find the previous workspace update report

```sh
ls /home/li/primary/reports/*/  | grep -E '\-Update-' | sort | tail -1
```

If a previous report exists, the baseline is its date (and
optionally its commit hash, named in the report itself). If no
previous report exists — this is the **first** workspace update
report — pick a sensible baseline: a recent date with clear
workspace state, the last major checkpoint, or roughly two
weeks back. Name the baseline choice + rationale in the report.

### 2. Survey the period

Five surfaces to look at, in roughly increasing depth:

- **`git log --since=<baseline>`** — commit titles and
  authorship. Skim for the shape of work.
- **`git log --since=<baseline> --stat`** — per-commit file
  changes. Identifies which files moved and how much.
- **`spirit "(Observe (Records ((Any []) None Any (Since
  (<baseline>)) SummaryOnly)))"`** — Spirit captures in the
  period. The intent layer's record of psyche statements.
- **`ls reports/<role>/ | grep '<date-range>'`** — reports
  written in the period. The motion across lanes.
- **`skills/` diff against baseline** — skill additions and
  edits. Discipline evolution.

The first three are mechanical (run, read). The last two require
judgment — what's significant, what's noise.

### 3. Synthesize the substance

A workspace update report has six sections plus front matter:

| Section | Substance |
|---|---|
| Baseline + period | What dates / commits / Spirit range the report covers. |
| Headlines | The 3-7 most important shifts of the period, each one paragraph. |
| Intent captures | The Spirit records, grouped by topic, with bracket-quoted summaries for the load-bearing ones. |
| Skill + ESSENCE / INTENT evolution | Which discipline files changed, what the change was, why it mattered. |
| Reports — landed, retired, in-flight | Per role / lane: what was produced, what retired. |
| Component / repo state | Code-side motion: which repos got new code or skills, which moved into production-orientation, which stayed quiet. |

Then a closing **forward-look** section names what's queued or
pending for the next period.

The report is narrative-voice per `skills/reporting.md`
§"Psyche reports — show the code, not the summary" and Spirit
1521 (Principle High): *"Talk to a human being in a narrative
voice — not citation-heavy. Numeric Spirit record IDs should be
used to mark ranges when highlighting a relevant span of intent,
not as constant inline citations on every claim."* When a single
record is load-bearing, name the number + bracket-quote the
summary per Spirit 1522. When a region of intent is being
summarised, use ranges or phrasings (*"the recent corpus shows
…"*).

### 4. Reference the previous update + name the next baseline

The report explicitly names the previous workspace update
report's path (if one exists) and declares its own commit hash
as the next baseline. The chain is the discipline's continuity.

## Filename convention

Per Spirit 1481 + `skills/report-naming.md`:

```
reports/<role>/<N>-Update-<period-name>-<date>.md
```

Where `<period-name>` is a short kebab-case label for the
covered span (e.g., `since-baseline`, `week-of-trace-redesign`,
`spirit-next-cutover`). The date is the report's first-written
date.

Examples:

- `reports/designer/491-Update-workspace-changes-since-baseline-2026-06-03.md`
- `reports/designer/512-Update-since-thirty-day-quiet-2026-07-04.md`

## Front matter

YAML front matter per `skills/reporting.md` §"Report header":

```yaml
---
title: 491 — Workspace update report (since baseline)
role: designer
variant: Update
date: 2026-06-03
topics: [workspace-update, change-survey, context-maintenance]
description: |
  First workspace update report in the series. Baseline pick:
  <date + rationale>. Surveys git log, Spirit captures,
  reports, and skill evolution across the period. Names what
  shifted and what's queued.
---
```

The `variant: Update` field is what marks this as an update
report. Indexing tools key off it.

## Tone

Narrative, terse. Substance over format. Per AGENTS.md hard
overrides plus `INTENT.md` §"Skills must not grow noisy":
*"Smart models can fill in blanks from good high-level guidance;
over-elaborated reports add cost without benefit."* The update
report's job is to compress a period's motion into something
the psyche can read in one sitting; bloat defeats the purpose.

A typical update report is 200-400 lines. Larger when the
period was unusually busy; smaller when it was quiet.

## What an update report does NOT do

- It does not propose new design (that's `Design`).
- It does not audit a specific surface (that's `Audit`).
- It does not ratify decisions (that's the psyche's job; the
  update can surface candidates for ratification, but the report
  itself is not a Decision-making artifact).
- It does not duplicate Spirit captures (it references them by
  number + bracket-quoted summary; the records themselves live
  in Spirit).
- It does not narrate per commit (it groups commits into the
  themes of the period).

## See also

- `skills/reporting.md` §"Kinds of reports — closed set, with
  destination" — the variant table.
- `skills/reporting.md` §"Psyche reports — show the code, not
  the summary" — the substance-first discipline (workspace
  update reports inherit it; code excerpts where load-bearing).
- `skills/report-naming.md` — filename + front matter.
- `skills/context-maintenance.md` — adjacent discipline (the
  update report is one tool in the maintenance kit).
- `skills/intent-log.md` §"Citing intent in prose —
  bracket-quote the summary" — the citation form workspace
  update reports use.
- Spirit 1530 — the capture that established the variant.
