---
title: 490 — Closeout pseudo-NOTA header migration to YAML front matter
role: designer
variant: Closeout
date: 2026-06-03
topics: [reports, markdown, front-matter, migration, closeout, pseudo-nota-header]
description: |
  Closeout log for the mechanical batch migration of 46 reports from the
  semicolon-bracket pseudo-NOTA header to YAML front matter per Spirit
  1527 (Decision High) and Spirit 1528 (Correction High), and per
  skills/reporting.md §[Report header — YAML front matter]. Migration
  driven by the audit in reports/designer/489-Audit-report-headers-and-
  skill-hallucinations-2026-06-03.md; carried out as designer sub-agent
  mechanical batch.
---

# 490 — Closeout: pseudo-NOTA header migration to YAML front matter

## TL;DR

**46 reports migrated** from the semicolon-bracket pseudo-NOTA header
shape to YAML front matter. Body content preserved byte-for-byte (a
verification script confirmed every file). All migrated files pass a
shape check requiring valid `---` delimiters, the six required fields
(`title`, `role`, `variant`, `date`, `topics`, `description`), valid
variant values from the closed set [Psyche Design Audit Research
Synthesis Closeout Handover], `YYYY-MM-DD` date shape, and a blank line
then `# <N> — <title>` heading after the closing `---`.

## Migration count by lane

| Lane | Count |
|---|---|
| `reports/designer/` | 43 |
| `reports/operator/` | 3 |
| **Total** | **46** |

The audit in 489 §A.3 named 47 (44 designer + 3 operator); during this
migration session report 488 had already been independently migrated to
YAML front matter by another agent before this batch ran (verified at
the start of the session — 488 is not in the migration set), so the
batch landed 46 files instead of 47.

Report 489 itself was excluded: it already uses YAML front matter and
contains `; designer` only inside code blocks illustrating the drift it
documents.

## Variant derivation summary

Variants are derived per Spirit 1481 — they go in both the filename's
`<Variant>` segment AND the YAML front matter `variant` field. The
closed set is `[Psyche Design Audit Research Synthesis Closeout
Handover]` per skills/reporting.md §[Report header — YAML front matter].

Variant sources used in this batch:

| Source | Count | Description |
|---|---|---|
| `filename` | 1 | Variant segment present in basename (`488-Psyche-...` — but 488 was already migrated; count remains 1 because the designer 487 sub-report directory had `Design-` in the parent directory name, which falls under `parent-dir` not `filename`). |
| `parent-dir` | 8 | Variant derived from the parent meta-report directory name (`484-Audit-...` for 6 files and `487-Design-...` for 2 files). |
| `content-derive` | 37 | Variant derived from keywords in the filename slug and the title heading. |

No reports were left at `default-fallback`. The heuristic resolved
every variant decision through filename / parent-directory / content
keywords. Keyword matches were Audit (`audit`, `verification`,
`verify`), Synthesis (`overview`, `synthesis`, `consolidation`,
`ledger`, `backlog`, `re-agglomeration`, `comparison`,
`context-maintenance`), Research (`research`, `playbook`, `landscape`,
`porting`), Design (`design`, `proposal`/`proposals` with word-boundary
match to avoid `designer` false positives; secondary `interface`,
`engine`, `spec`, `pilot`, `continuation`, `control`, `sequencing`).
Meta-report sub-files inherit the parent's `<Variant>-` segment unless
their own slug overrides — e.g., 484/6-overview and 487/5-overview
override Audit/Design to Synthesis for the orchestrator's synthesis
slot.

## Variant decisions worth flagging for psyche review

A few cases involve genuine judgment that the psyche may want to
reconsider:

- **466/0-frame-and-method** assigned `Design` (frame for a
  honesty-audit dispatch). The sub-files 466/1 and 466/2 are Audits
  and 466/3 is Synthesis; arguably the frame itself is also an Audit
  since it dispatched audits. The default heuristic chose `Design` for
  frame-and-method files. Easy follow-up: flip to `Audit` if the
  psyche prefers parent-meta-report-variant inheritance for frames.

- **446/0-frame-and-method** assigned `Design` (research-meta frame).
  The sub-files are mostly `Research` (446/1, 446/2) plus `Design`
  (446/3) plus `Synthesis` (446/4). Same judgment call as above.

- **475/0-frame-and-method** assigned `Design`. The full meta-report
  is a contract-repo pipeline situation + proposal; sub-files are
  `Design` (475/1) and `Synthesis` (475/2). `Design` for the frame
  is consistent here.

- **477** (Nexus re-agglomeration — three angles) assigned `Synthesis`
  because of the `re-agglomeration` keyword in the slug. The report
  does both synthesize across reports AND propose three concrete
  design angles; either Design or Synthesis is defensible. Synthesis
  was chosen mechanically.

- **288** (Nexus recursion designer-477 comparison) assigned
  `Synthesis` via the `comparison` keyword. The report's body
  includes implementation leans and tests, which could push it to
  Design. The heuristic chose Synthesis.

- **451** (Operator-271 falsifiable specs) assigned `Design`. The
  report carries falsifiable spec witnesses for operator pickup —
  more like a proposal/spec than a pure audit. `Design` is the
  closer fit.

None of these are wrong; they're judgment calls where the heuristic
chose one defensible option. A psyche review pass can flip any of them
with a one-line edit to the YAML `variant` field plus an optional
filename rename for stability.

## Skipped files

- `reports/designer/489-Audit-report-headers-and-skill-hallucinations-2026-06-03.md`
  — already uses YAML front matter. Contains `; designer` inside a
  code block as part of the audit's illustration of the drift.

- `reports/designer/488-Psyche-487-overview-context-and-decisions-2026-06-03.md`
  — was migrated to YAML front matter by another agent during this
  session, before the batch ran. Verified at session start that 488
  is not in the affected list.

No reports under `private-repos/` were touched. No reports were
renamed; no files were moved. Only the header was rewritten.

## Verification

A verification script (`/tmp/verify_migration.py`) compared each
migrated file's body — everything from the `# <N> — <title>` heading
onward — against the pre-migration body retrieved from `git show
HEAD:<path>`. All 46 files: body byte-identical to pre-migration.

A YAML shape check (`/tmp/yaml_check.py`) verified that every migrated
file starts with `---`, has a closing `---` followed by a blank line
then the `# ` heading, has all six required fields, has a variant from
the closed set, and a valid `YYYY-MM-DD` date.

### Spot-check sample

Per dispatch context, five random files were inspected after migration:

| Path | Status |
|---|---|
| `reports/designer/445-next-stack-audit-2026-06-01.md` | YAML valid; variant `Audit`; body byte-identical |
| `reports/designer/449-bead-staleness-audit-2026-06-01.md` | YAML valid; variant `Audit`; body byte-identical |
| `reports/designer/465-recent-decision-landscape-2026-06-01.md` | YAML valid; variant `Research`; body byte-identical |
| `reports/designer/466-triad-engine-honesty-situation-2026-06-01/3-overview.md` | YAML valid; variant `Synthesis`; parent_meta_report + slot set; body byte-identical |
| `reports/operator/289-nexus-internal-control-interface-2026-06-02.md` | YAML valid; variant `Design`; body byte-identical |

The 466/3-overview sub-file specifically verifies the meta-report
sub-file YAML carries `parent_meta_report: reports/designer/466-triad-
engine-honesty-situation-2026-06-01` and `slot: 3`. The 484-Audit-
production-readiness-meta and 487-Design-trace-help-config-context-meta
sub-files were also confirmed to carry their parent_meta_report + slot
fields per the meta-report subfile rule.

## What is now load-bearing

All 46 migrated files render in markdown UIs (GitHub, VS Code preview,
Obsidian) with proper metadata; the `; designer` shape is gone from the
working tree except inside 489's code blocks. Downstream skill edits
flagged in the 489 audit — `skills/reporting.md` filename-convention
update for Spirit 1481, `skills/component-triad.md` owner-signal →
meta-signal rename per Spirit 1428, stale citations in 6 skill files,
and `skills/intent-log.md` §[Citing intent in prose — bracket-quote
the summary] — remain as separate follow-up work, out of scope for
this mechanical batch.
