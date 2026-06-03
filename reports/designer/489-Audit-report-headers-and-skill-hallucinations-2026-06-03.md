---
title: 489 — Audit of report headers and skill hallucinations
role: designer
variant: Audit
date: 2026-06-03
topics: [reports, markdown, front-matter, skills-audit, hallucination]
description: |
  Workspace-scale audit per psyche 2026-06-03 STT directive: origin of
  the semicolon-bracket pseudo-NOTA report header, YAML front matter
  migration proposal, and a sweep of skills/ for hallucinated or
  drifted content. Per Spirit 1527 (Decision High) and Spirit 1528
  (Correction High).
---

# 489 — Audit of report headers and skill hallucinations

## Verdict — short

**Problem 1.** The semicolon-led pseudo-NOTA header at the top of recent
designer and operator reports is **drift / hallucination**. It first
appeared on `2026-06-01` (commit `9d985bf9`) on report 445 and spread
through the lane unchecked. `skills/reporting.md` §"Report header" does
NOT document it — the documented format is the italicised one-liner
*"Kind: Design · Topics: intent, recording-system · 2026-05-22"*. The
pseudo-NOTA shape mimics the **Spirit intent-record vector + description
+ daemon-stamp** structure — agents grafted the intent-record shape onto
markdown headers without psyche authority. Per Spirit 1527 (Decision
High): *"Reports use standard YAML front matter for metadata, not the
semicolon-bracket pseudo-NOTA shape … YAML front matter plugs into
standard markdown UI tooling (previewers, GitHub rendering, Obsidian,
editor frontmatter parsers); valid markdown so renderers display reports
cleanly; is the conventional metadata-on-markdown standard."* Per Spirit
1528 (Correction High): *"The semicolon-bracket pseudo-NOTA report
header format that many recent reports use at the top is a drift or
hallucination — it does not match skills/reporting.md §Report header …
Reports drifted to a NOTA-styled header that mimics Spirit intent record
shape; this was never a ratified workspace decision."*

**Problem 2.** A workspace-scale skills sweep surfaces a handful of
genuine drifts. The major findings:

- `skills/reporting.md` and `skills/report-naming.md` do NOT reflect
  Spirit 1481 (Decision High): *"Report filename convention is
  reports/<role>/<N>-<Variant>-<topic>-<date>.md where <Variant> is a
  capitalized word naming the report kind."* Both skills still say the
  kind moves to the header, not the filename. Recent reports (484, 487,
  488) DO follow 1481 in practice; the skill files don't.
- `skills/component-triad.md` still flags the `owner-signal` →
  `meta-signal` rename as **tentative** per records 290 + 299 + 293
  (Minimum / Medium / Medium, May 23). Spirit 1428 (Decision Maximum,
  later) ratified the **fleet-wide** rename of all 13 contract repos.
  AGENTS.md still uses `owner-signal` in its component-triad override.
- Six skill files cite **retired report paths** that no longer exist:
  `kameo.md`, `actor-systems.md`, `intent-manifestation.md`,
  `autonomous-agent.md`, `contract-repo.md`, `testing.md`. Most cite
  `reports/operator-assistant/138-*` or `reports/designer/232-*` or
  `reports/designer/211-*` or `reports/operator/205-*` — all retired in
  the May context-maintenance sweep `c93c9888` or earlier. Compounds the
  violation: per `skills/skill-editor.md` §"Skills never reference
  reports", skills SHOULD NOT cite reports in the first place.
- `skills/reporting.md` cites `reports/second-designer/152-…/` as the
  canonical worked example of a meta-report directory, but `152` was
  consolidated into `162/3` and deleted (`jj show 3307c471`).
- `skills/reporting.md` §"Where reports live" still lists the
  `<role>-assistant` lane subdirectories (`reports/operator-assistant/`,
  `reports/designer-assistant/`, `reports/poet-assistant/`) which were
  RETIRED per Spirit record 920 (Maximum, 2026-05-27).
- `skills/intent-log.md` lacks a `§"Citing intent in prose — bracket-
  quote the summary"` section despite Spirit 1522 + 1526 (Principle
  Maximum + High, 2026-06-03) mandating that exact discipline. The
  bracket-quote citation pattern IS being applied in the latest
  reports and in skills/component-triad.md, but no skill documents the
  rule. (The dispatch context to this sub-agent assumes such a section
  exists; it does not.)
- `skills/component-triad.md` mentions `Sub-design and demo:
  reports/designer/487-…/2-help-namespace-design.md` — that's a live
  cross-reference but still violates `skill-editor.md` §"Skills never
  reference reports". Same with the `483-`, `485-`, `486-` references
  in commit `63533c5e` follow-up: those were retired June 3, but the
  recent skill edits ABSORBED the substance and then DIDN'T add the
  citation back, which is the correct behaviour. New violations occurred
  in the same wave with `487-…/2-help-namespace-design.md`.

The detailed findings, severity, and proposed action live in §C below.

## A — Origin of the pseudo-NOTA header

### A.1 When did it first appear

`git log --diff-filter=A` plus `grep '^; designer$\|^; operator$'`
narrows the origin to one commit:

**Commit `9d985bf9`** — *"designer: next-stack audit + porting research
+ upgrade-as-sema + wrapper-audit"* — Monday June 1, 11:27 +0200. The
commit landed five designer reports simultaneously; every one of them
carried the pseudo-NOTA header. The session that produced 445-448 (plus
the 446 meta-report directory) is the origin event.

Before `9d985bf9` (June 1):

- Report 443 frame (`443-design-improvements-audit-…/0-frame-and-method.md`,
  2026-05-31) used the documented italicised one-liner:

      # 0 — Frame and Method

      *Kind: meta-report frame · Topics: design-audit, reusable-planes, boilerplate-elimination, layering, operator-work-audit · 2026-05-31 · designer lane*

- Report 444 frame (`444-stack-vision-…/0-frame-and-method.md`,
  2026-05-31) likewise.

After `9d985bf9` (June 1):

- Report 445 (`445-next-stack-audit-2026-06-01.md`):

      ; spirit
      [stack-audit nota-next schema-next spirit-next discipline rust-craft]
      [Designer audit of the live nota-next + schema-next + spirit-next surfaces against workspace discipline. Net state — substrate is sound; four small findings remain; designer 444 §5 horizons are accurate.]
      2026-06-01
      designer

The shape proliferated from there: every subsequent designer session
(446-448 same commit; then 449, 450, 451, 452, 458, 463, 465, 466, 468,
469, 470, 472, 473, 474, 475, 477, 478, 481, 484, 487, 488) reproduced
it. Two operator sessions (287, 288, 289 on `2026-06-02`) adopted the
shape as well. Every single instance is within the 2-day window
2026-06-01 → 2026-06-03.

### A.2 Where did it come from

The shape **mimics the Spirit intent-record write surface** (per
`skills/spirit-cli.md` §"Operations on the ordinary channel"):

```nota
(Record
  ([<topic> ...]     ;; vector of topic identifiers
   <Kind>            ;; Decision | Principle | Correction | …
   [<description>]   ;; agent-clarified intent
   <Magnitude>))     ;; Zero | Minimum | … | Maximum
                     ;; (daemon stamps date/time on receipt)
```

Compare the pseudo-NOTA report header:

```
; designer
[psyche-report 487-overview decisions context tracing …]
[Psyche report for the psyche to read directly — full context, full decisions, full forward path …]
2026-06-03
designer
```

The five-line shape maps onto the five Spirit-record positions:

| Pseudo-NOTA header line | Spirit record position |
|---|---|
| `; designer` | semicolon comment (in NOTA, `;;` is line comment; `;` is invalid NOTA) — agent-invented separator |
| `[psyche-report 487-overview …]` | `[<topic> …]` vector |
| `[Psyche report for the psyche …]` | `[<description>]` bracket string |
| `2026-06-03` | the daemon-stamped date Spirit replies with |
| `designer` | second appearance of the lane / role / Kind position |

The single semicolon `; designer` line is NOT valid NOTA: NOTA's only
comment sigil is `;;` (per `nota-design.md` §"Sigils. Two reserved at
the syntax layer: `;;` for line comments, `#` for byte literals"). The
hybrid is a **markdown-meets-Spirit-record mashup** — the agent who
introduced the shape on June 1 read the Spirit record vocabulary and
projected it onto the report header surface without checking
`skills/reporting.md`.

**No Spirit record endorses the format.** I ran the queries:

```
spirit "(Observe (Records ((Partial [reports header front-matter metadata markdown]) None Any Any SummaryOnly)))"
spirit "(Observe (Records ((Partial [reports topic-vector header-shape kind format]) None Any (Between ((2026-05-29 00:00:00) (2026-06-01 23:59:59))) SummaryOnly)))"
```

Both return only the documented `*Kind: … · Topics: … · YYYY-MM-DD*`
shape per records 939+941 (Decision High / Maximum, 2026-05-27) and the
new Spirit 1481 variant-in-filename rule. NO record blesses the
semicolon-bracket header at any time.

**No skill documents the format.** A workspace-scale grep confirms it:

```
grep -ln 'psyche-report\|^; designer' skills/*.md  # → no matches
grep -ln '^; designer\|^; operator' skills/*.md    # → no matches
```

### A.3 Spread — count by lane

| Lane subdirectory | Reports with pseudo-NOTA header |
|---|---|
| `reports/designer/` | 44 (including all sub-reports inside meta-report directories) |
| `reports/operator/` | 3 (287, 288, 289) |
| `reports/system-operator/` | 0 |
| `reports/poet/` | 0 |
| `reports/cloud-designer/` | 0 |
| `reports/system-designer/` | 0 |
| every other lane | 0 |

**Total: 47 markdown files** carry the pseudo-NOTA header out of 178
total report files in the working tree. The remaining 131 either pre-
date June 1 (older sweep already retired most of them; what remains
follows the italicised one-liner or has no header) or were authored by
agents on lanes that didn't catch the drift.

### A.4 Does `skills/reporting.md` document the format

**No.** `skills/reporting.md` §"Report header — kind, topics, date"
(lines 710-739) prescribes the **italicised one-liner**:

```markdown
# 17 — Real-time intent recording system

*Kind: Design · Topics: intent, recording-system · 2026-05-22*
```

Three fields, one line, italicised. The drift went somewhere else
entirely — the agents emitting pseudo-NOTA were NOT following the
documented format. **The documented format and the actual format have
been disagreeing for three days.** This audit (per psyche 2026-06-03) is
the first time the gap surfaces explicitly.

This is **Spirit 1528's exact diagnosis**: *"The semicolon-bracket
pseudo-NOTA report header format that many recent reports use at the
top is a drift or hallucination — it does not match skills/reporting.md
§Report header which documents an italicised one-liner after the title.
Reports drifted to a NOTA-styled header that mimics Spirit intent record
shape; this was never a ratified workspace decision."*

## B — YAML front matter migration design

### B.1 The canonical shape

Per Spirit 1527 (Decision High): *"Reports use standard YAML front
matter for metadata."* The canonical shape going forward:

```yaml
---
title: <N> — <Report title>
role: <lane>           # designer, operator, system-operator, cloud-designer, etc.
variant: <Variant>     # Psyche / Design / Audit / Research / Synthesis / Closeout / Handover
date: YYYY-MM-DD       # first-written; reaffirmed on substantive rewrite
topics: [topic-1, topic-2, ...]   # broad atomic words; mirrors filename topics
description: |
  Multi-line summary of what the report contains, what was decided,
  and the load-bearing context. Stays self-contained — a future agent
  reading just the front matter knows what the report is about.
---

# <N> — <Report title>

(report body)
```

### B.2 Field list

| Field | Required | Carries |
|---|---|---|
| `title` | yes | Report title — same as the first `#` heading. Lets editors/renderers display the title without scanning Markdown. |
| `role` | yes | The writing lane. Mirrors the report's parent subdirectory. |
| `variant` | yes | The report kind, per Spirit 1481 (Decision High): *"Proposed variant set covers main scenarios — Psyche Design Audit Research Synthesis Closeout Handover. Small set; can grow if a clear new scenario surfaces."* |
| `date` | yes | First-written date, `YYYY-MM-DD` only. Per Spirit 1481 (filename includes `<date>` too) and per existing `skills/reporting.md` discipline. |
| `topics` | yes | YAML list of topic atoms (kebab-case). Mirrors the per-topic-vocabulary discipline and the topic prefixes in the filename. |
| `description` | yes | Multi-line description block. Self-contained per Spirit 1471 (Psyche-variant) + the broader "human-facing references are self-contained" rule from `skills/reporting.md`. |

Optional fields when the report is part of a meta-report directory:

| Field | Required | Carries |
|---|---|---|
| `parent_meta_report` | optional | Path to the meta-report directory the report belongs in (e.g. `reports/designer/487-Design-trace-help-config-context-meta-2026-06-03/`). |
| `slot` | optional | Numeric slot within the meta-report directory (0 for frame, 5 for overview, etc.). Per Spirit 289 (pre-launch lane allocation). |

The two optional fields cover the meta-report directory case
mechanically — the frame report is `slot: 0`, sub-agent reports take
their assigned numbers, the overview report is the highest.

### B.3 Render check

YAML front matter is the **de-facto standard** for markdown-with-metadata.
Renderers that handle it natively (the psyche's stated concern *"all of
my preview are going to work"*):

| Renderer | YAML front matter support |
|---|---|
| **GitHub** | Yes (native; renders fields cleanly above the body in PRs, gists, repos). |
| **VS Code markdown preview** | Yes — the built-in renderer + Markdown-Preview-Enhanced and other extensions show YAML front matter as a metadata table or hide it as preamble per preference. |
| **Obsidian** | Yes — Obsidian's note metadata system reads YAML front matter as note properties (indexed for search, sortable, queryable through Dataview). |
| **Jekyll / Hugo / Eleventy** | Yes (these tools are why YAML front matter became the standard). |
| **pandoc / mkdocs / Sphinx-MyST** | Yes. |

The pseudo-NOTA header renders as **literal plain text** in all of these,
because:

- Lines beginning `; designer` are not recognised by any markdown
  renderer or front-matter parser.
- `[bracket text]` reads as a markdown link `[text]` with no target,
  showing as plain text but in some renderers wrapping in a tooltip-
  shaped element.
- `2026-06-03` alone on a line shows as a paragraph.

So the pseudo-NOTA header isn't just architecturally wrong — it's
visually broken in every markdown UI the psyche uses. The psyche's
phrasing matches what they're seeing: *"this is weird … not valid
markdown."*

### B.4 Migration plan

**Total reports needing migration: 47** (44 designer + 3 operator).
Verified count per §A.3 above.

The migration is **mechanical** because the pseudo-NOTA header is
deterministic five lines + blank line, always preceding the `# <N> —
…` title line. A script can identify and rewrite every file with
high confidence.

**Two-pass plan**, in order:

**Pass 1 — write/update the `skills/reporting.md` §"Report header"
section** (see §B.5 below for the exact edit). This is the upstream
fix; until the discipline doc is corrected, agents will keep emitting
the wrong shape.

**Pass 2 — migrate the 47 in-place.** For each file:

1. Identify the pseudo-NOTA block (5 lines starting with `; <lane>`
   immediately above the `# <N> —` title).
2. Parse the five fields into YAML front matter using the schema in
   §B.1.
3. Field mapping rules:
   - Line 1 (`; designer`) → `role: designer`. Drop the duplicate
     line 5.
   - Line 2 (`[topic-1 topic-2 …]`) → `topics: [topic-1, topic-2, …]`
     (split on whitespace; preserve atoms).
   - Line 3 (`[multi-line description]`) → `description: |` block
     (preserve newlines that exist; for single-line, use the block
     scalar form for consistency).
   - Line 4 (`2026-06-03`) → `date: 2026-06-03`.
   - Determine `variant` from the filename and report opening: if the
     filename has `<Variant>-` (e.g. `Audit-`, `Design-`,
     `Psyche-`), use that; otherwise classify from the report's
     opening section (the "Frame" or "TL;DR" usually states the
     report kind).
   - Determine `title` from the `# <N> — …` heading.
4. Insert the YAML block above the title, separated by one blank line.
5. Remove the original five lines.

The script form (sketch — for the operator who lands the migration to
implement; this is not a designer-lane action):

```sh
# For each file with pseudo-NOTA header:
#   1. Detect ^; <lane>$ followed by 4 lines + blank + # <N>
#   2. Parse the five fields
#   3. Emit YAML block + body
#   4. Replace in place
# Tool form: a small Rust binary using nota-codec to parse the bracket
# strings (they ARE bracket strings even when used wrongly) and serde_yaml
# to emit YAML; or a careful awk/sed script; or a one-shot agent pass.
```

**Migration ordering — recommendation: in-place rewrite (not
deletion + supersession).** Reasons:

- The 47 reports are not stale-by-content; they carry live design and
  audit substance. Only the **header** is wrong.
- Spirit 1487 (the rename rule for old reports) only applies to
  superseded content, not corrupt metadata.
- An in-place rewrite preserves the report's content, number, and
  position in the workspace's reference graph.
- A single commit (or one-per-file commit set) cleanly captures the
  drift correction across the lane.

**Order within Pass 2**: oldest-first (445 → 488) so the lane's
chronology stays coherent if any cross-references between reports
reference field formats.

### B.5 The exact `skills/reporting.md` edit

The current §"Report header — kind, topics, date" (lines 710-739)
prescribes the italicised one-liner. The replacement section should
read (proposed; main designer to execute after psyche approval):

```markdown
## Report header — YAML front matter

Per Spirit 1527 (Decision High, 2026-06-03): *"Reports use standard
YAML front matter for metadata."*

Every report carries a YAML front matter block at the **top of the
file**, before the title heading:

```yaml
---
title: 17 — Real-time intent recording system
role: designer
variant: Design
date: 2026-05-22
topics: [intent, recording-system]
description: |
  Proposal for a typed real-time intent recording system that
  captures author Decisions / Principles / Corrections /
  Clarifications / Constraints as they happen.
---

# 17 — Real-time intent recording system

(report body...)
```

The fields, in canonical order:

- **`title`** — the report's title, matching the `# <N> — …` heading
  on the next line. Lets renderers display the title without scanning
  markdown body.
- **`role`** — the writing lane's exact subdirectory name
  (`designer`, `operator`, `cloud-designer`, `second-designer`, etc.).
- **`variant`** — the report kind per Spirit 1481: `Psyche`,
  `Design`, `Audit`, `Research`, `Synthesis`, `Closeout`, `Handover`.
  Capitalised. Matches the `<Variant>` segment of the filename
  convention.
- **`date`** — first-written date, `YYYY-MM-DD`. Reaffirmed on
  substantive rewrites; unchanged on small fixes.
- **`topics`** — YAML list of broad atomic topic words (kebab-case),
  mirroring the topic prefixes in the filename. Multiple topics
  allowed; first topic is the primary.
- **`description`** — multi-line block scalar (`|`) giving the
  report's substance. Self-contained: a future agent reading just the
  front matter knows what the report is about.

Optional fields for reports inside a meta-report directory:

- **`parent_meta_report`** — path to the meta-report directory.
- **`slot`** — numeric position within the directory (0 for the
  frame; highest for the overview).

YAML front matter is the standard markdown-with-metadata format. It
renders cleanly in GitHub, VS Code markdown preview, Obsidian, and
every static-site generator the workspace might eventually surface
through. The header is also the report's primary self-describing
surface, parseable mechanically by an agent walking the report tree.

**Forbidden shape: the semicolon-bracket pseudo-NOTA header.** Per
Spirit 1528 (Correction High, 2026-06-03): *"The semicolon-bracket
pseudo-NOTA report header format … is a drift or hallucination — it
does not match skills/reporting.md §Report header. Reports drifted to a
NOTA-styled header that mimics Spirit intent record shape; this was
never a ratified workspace decision."* The shape

    ; designer
    [topic-1 topic-2 …]
    [description text]
    2026-06-03
    designer

is **not valid markdown**, **not valid NOTA** (`;` alone is invalid;
NOTA's comment sigil is `;;`), and **not rendered** by any markdown
UI. Migrate any remaining instances to YAML front matter.
```

The old italicised one-liner discipline retires; the workspace had
already drifted away from it. The YAML front matter discipline becomes
the documented and the actual format.

### B.6 Companion edit to `skills/report-naming.md`

`skills/report-naming.md` says report kind belongs "in the report
header" without specifying the form. After §B.5 lands, the companion
edit adds a one-line cross-reference:

```markdown
Report kind (Variant) belongs in the YAML front matter `variant:`
field per `skills/reporting.md` §"Report header — YAML front matter",
AND in the filename per Spirit 1481 (the `<Variant>-` segment between
`<N>-` and `<topic>-`).
```

The current paragraph that says *"kind belongs in the report header,
not in the filename"* contradicts Spirit 1481 and should be replaced.

## C — Skills weird-kinks scan

The audit walked all 57 workspace skills (`skills/*.md` + `skills/rust/`)
looking for content that doesn't trace to a clear psyche intent or skill
rule, is internally contradicted, or references retired material.

Severity scale (used in the table):

- **Hallucination** — content with no upstream psyche intent, no
  pre-existing skill rule, no traceable rationale. The strongest
  finding.
- **Drift** — content that traced to an upstream when written but has
  not been updated as the upstream evolved. Less severe than
  hallucination because there was once intent; now the citation /
  framing is stale.
- **Stale** — content referencing retired components, deleted reports,
  or superseded patterns. Mechanical fix usually.
- **Contradiction** — content that disagrees with another skill or
  with AGENTS.md / ESSENCE.md / INTENT.md.

### C.1 The findings, file by file

| Skill | Severity | Finding | Proposed action |
|---|---|---|---|
| `reporting.md` | **Contradiction** | §"Filename convention" (line 428-433) says *"The kind of the report … moves to the report's frontmatter or opening section, not the filename."* Spirit 1481 (Decision High, 2026-06-02) SUPERSEDES: variant goes in filename `<N>-<Variant>-<topic>-<date>.md`. | Rewrite §"Filename convention" to align with Spirit 1481 — variant goes both in filename AND in front matter. |
| `reporting.md` | **Drift** | §"Where reports live" (line 311-319) still lists `reports/operator-assistant/`, `reports/designer-assistant/`, `reports/poet-assistant/` as canonical role subdirectories. Per Spirit 920 (Decision Maximum, 2026-05-27) the `<role>-assistant` suffix is RETIRED — additional capacity is `second-<role>`. | Replace the assistant-suffixed entries with the current lane vocabulary (`second-<role>`, qualified lanes). |
| `reporting.md` | **Stale citation** | §"Worked example" (line 381-388) cites `reports/second-designer/152-persona-engine-architecture-overview/` as the canonical worked example of a meta-report directory. Directory was consolidated into `/162/3` and deleted (commit `3307c471`). | Replace with a live worked example — `reports/designer/487-Design-trace-help-config-context-meta-2026-06-03/` would work. Or remove the worked-example block entirely (skill-editor.md §"Skills never reference reports"). |
| `reporting.md` | **Drift** | §"Report header — kind, topics, date" documents the italicised one-liner; the workspace has drifted away from it. Per Spirit 1527 + 1528. | Rewrite per §B.5 above (YAML front matter). |
| `report-naming.md` | **Drift** | Filename pattern says `<N>-<primary-topic>[-<secondary-topic>]…-<title-slug>.md`, omitting the `<Variant>-` segment from Spirit 1481. | Update to `<N>-<Variant>-<primary-topic>[-<secondary-topic>]…-<title-slug>[-<date>].md`. |
| `report-naming.md` | **Stale citation** | `## See also` cites `intent/reports.nota` — the legacy file substrate. Per AGENTS.md, agents do not append to `intent/*.nota` during normal work. | Replace with a Spirit query (`spirit "(Observe (Records ((Partial [reports]) None Any Recent SummaryOnly)))"`) or remove the see-also line. |
| `intent-log.md` | **Drift / Missing** | The skill lacks a `§"Citing intent in prose — bracket-quote the summary"` section despite Spirit 1522 (Principle Maximum) + 1526 (Principle High, 2026-06-03) explicitly directing it: *"Reference intent records in prose markdown by quoting the description summary literally as bracketed text — the bracketed form IS the citation — not by the record number alone."* The dispatch context to this audit assumes the section exists. | Add a `§"Citing intent in prose — bracket-quote the summary"` section to `intent-log.md`. Sketch: when citing a Spirit record in prose, quote the description summary as bracketed text alongside the record number; the bracketed summary is the load-bearing citation, the number is the address. Cite Spirit 1522 + 1526 (Maximum + High). |
| `component-triad.md` | **Drift** | §"Proposed rename: `owner-signal` → `meta-signal`" (line 294-301) still labels the rename as **tentative direction, not a completed vocabulary change**, citing records 290 + 293 + 299 (Minimum / Medium / Medium, May 23). Spirit 1428 (Decision Maximum, 2026-05-30 region): *"Workspace-wide rename — all existing owner-signal-* contract repos rename to meta-signal-* as a fleet operation."* The rename IS now ratified at fleet scope. | Rewrite the section to reflect Spirit 1428 as the current authority: meta-signal is the canonical name; the rename is fleet-wide and ratified, not tentative. (Cascade: AGENTS.md hard override §"Component triad" also still says `owner-signal-` — needs the same update.) |
| `component-triad.md` | **Skill-editor rule violation** | Line 538: `Sub-design and demo: reports/designer/487-Design-trace-help-config-context-meta-2026-06-03/2-help-namespace-design.md`. Per `skill-editor.md` §"Skills never reference reports", skills should NOT cite reports. The 487 report substance has been absorbed into the skill body; the citation should be removed. | Remove the report citation. Inline whatever the skill needed from the report; the report retires when its substance is fully migrated. |
| `kameo.md` | **Stale citation** | Lines 922, 1018: cite `reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md`. (a) The `operator-assistant` lane is retired. (b) Report 138 was deleted in commit `c93c9888` (context-maintenance sweep). | Inline the substance the citation supported (a finding about `StoreKernel` deferral and persona-mind gap closure) OR remove the citation if not load-bearing. Per skill-editor.md, the skill should stand on its own. |
| `actor-systems.md` | **Stale citation** | Lines 349, 715: same `reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md` citation. | Same — inline or remove. |
| `intent-manifestation.md` | **Stale citation** | Lines 24, 194: cite `reports/designer/232-persona-spirit-new-component.md`. Report 232 no longer exists (retired). | Remove the citation; the persona-spirit forward direction is documented in INTENT.md and `skills/spirit-cli.md` — no longer needs a report pointer. |
| `autonomous-agent.md` | **Stale citation** | Line 99: cites `reports/operator/205-spirit-next-schema-pilot-implementation-2026-05-26.md` as an example path. Report 205 no longer exists. | Replace with a current report path that still exists, OR replace with a placeholder `reports/<role>/<N>-…md` template. |
| `contract-repo.md` | **Stale citation** | Line 489: cites `reports/designer-assistant/125-v2-contract-local-verbs-vs-sema-core-verbs.md`. Both the `designer-assistant` lane and report 125 are retired. | Inline the contract-local-verb / Sema split analysis if load-bearing, or remove. |
| `testing.md` | **Stale citation** | Line 251: cites `reports/designer/211-persona-terminal-consolidation-one-daemon-2026-05-17.md` §7 and §11 Q2. Report 211 no longer exists. | Inline the design rationale for the persona-terminal-daemon if load-bearing, or remove the citation. |
| `poet.md` | **Drift** | Line 155: still mentions `reports/poet-assistant/` as a lane subdirectory. Spirit 920 retired the `<role>-assistant` suffix. | Update to use the current lane vocabulary (`second-poet`). |
| `nota-design.md` | **Stale reference** | Line 271: references the legacy migration target *"CriomOS-home Nix modules, lojix-cli, downstream consumers"* as still pending migration off legacy `"..."` quoted strings. Status — is this still accurate? AGENTS.md §"NOTA strings come EXCLUSIVELY from bracket forms" treats migration as authorised but not yet completed; the skill says the same. Cross-check needed. | Verify migration status before any change; the skill may be accurate. Flag as **Possible drift** pending verification. |
| `skills.nota` | **Possible drift** | The index lists 33 entries; one entry (`workspace-vocabulary skills/workspace-vocabulary.md`) is in the index but I did not open the file. Verify the file's content is still load-bearing AND aligned with the rest. | Spot-check `workspace-vocabulary.md` against current intent. (Out of scope for this audit; flag for follow-up.) |

### C.2 What did NOT surface in the sweep

To be honest about what didn't show up:

- **No skill mentions or documents the pseudo-NOTA report header.** The
  drift lived entirely in agent practice, not in skill files. This is
  actually reassuring — the discipline files held, the agents drifted.
- **Most cross-skill references (skills citing other skills) are
  current** — `nota-design.md → skills/skills.nota`,
  `intent-log.md → skills/spirit-cli.md`, etc.
- **The Rust craft sub-skills (`skills/rust/methods.md`,
  `skills/rust/errors.md`, `skills/rust/storage-and-wire.md`,
  `skills/rust/parsers.md`, `skills/rust/crate-layout.md`)** were
  spot-checked and look clean — they cite ESSENCE.md / language design
  principles + recent intent records, not retired reports.
- **`spirit-cli.md` already uses YAML front matter** (the
  `tool_versions: [[Spirit, 0.3.0]]` block at the top). The convention
  is not new to the workspace; it's just not the prescribed shape for
  reports. The Spirit 1527 ratification aligns with existing usage in
  one skill file.

### C.3 Severity summary

| Severity | Count | Examples |
|---|---|---|
| Contradiction (skill vs. recent Spirit) | 1 | `reporting.md` §Filename convention vs. Spirit 1481 |
| Drift (rule needs update for newer intent) | 4 | `reporting.md` §Report header + §Where reports live; `component-triad.md` §owner-signal rename; `poet.md` |
| Stale citation (retired report / lane referenced) | 7 | `kameo.md`, `actor-systems.md`, `intent-manifestation.md`, `autonomous-agent.md`, `contract-repo.md`, `testing.md`, `reporting.md` |
| Missing section the dispatch context assumed | 1 | `intent-log.md` missing §"Citing intent in prose — bracket-quote the summary" |
| Skill-editor rule violation (report-citation) | 1 | `component-triad.md` line 538 |
| Possible drift (verification needed) | 2 | `nota-design.md` legacy-migration status; `workspace-vocabulary.md` (not opened) |

**Total findings: 16 across 11 skill files.** Not a catastrophe — the
discipline mostly holds — but enough drift to warrant a context-
maintenance pass.

## Cross-references and Spirit captures

### Spirit records that frame this audit

- **Spirit 1527 (Decision High, 2026-06-03):** *"Reports use standard
  YAML front matter for metadata, not the semicolon-bracket pseudo-
  NOTA shape (; role [topics] [description] date role) that recent
  reports have been emitting. Rationale — YAML front matter plugs into
  standard markdown UI tooling (previewers, GitHub rendering, Obsidian,
  editor frontmatter parsers); valid markdown so renderers display
  reports cleanly; is the conventional metadata-on-markdown standard."*
- **Spirit 1528 (Correction High, 2026-06-03):** *"The semicolon-bracket
  pseudo-NOTA report header format that many recent reports use at the
  top is a drift or hallucination — it does not match skills/reporting.md
  §Report header which documents an italicised one-liner after the
  title."*

### Related intent records used in the audit

- **Spirit 1481 (Decision High, 2026-06-02):** *"Report filename
  convention is reports/<role>/<N>-<Variant>-<topic>-<date>.md where
  <Variant> is a capitalized word naming the report kind. Every report
  has a variant."* — the upstream that contradicts the current
  `reporting.md` and `report-naming.md` filename rules.
- **Spirit 1428 (Decision Maximum, 2026-05-30 region):** *"Workspace-
  wide rename — all existing owner-signal-* contract repos rename to
  meta-signal-* as a fleet operation."* — the upstream that supersedes
  `component-triad.md`'s tentative-rename framing.
- **Spirit 920 (Decision Maximum, 2026-05-27):** *"The prior
  <role>-assistant and <role>-specialist suffixes are RETIRED.
  Additional capacity is added by second-<role>, third-<role>, etc."*
  — the upstream that retired the assistant-suffixed lanes still
  documented in several skill files.
- **Spirit 1522 (Principle Maximum, 2026-06-03):** *"Reference intent
  records in prose markdown by quoting the description summary literally
  as bracketed text — the bracketed form IS the citation — not by the
  record number alone."*
- **Spirit 1526 (Principle High, 2026-06-03):** restates 1522 for the
  context of psyche-facing reports — the bracket-quote discipline.

### Workspace surfaces referenced

- `/home/li/primary/AGENTS.md` §"Hard overrides" — the component-triad
  hard override still uses `owner-signal-` and may need a parallel
  update when the `meta-signal` rename absorbs into discipline files.
- `/home/li/primary/skills/reporting.md` §"Report header" + §"Filename
  convention" — the canonical edit targets for the YAML migration.
- `/home/li/primary/skills/report-naming.md` — companion edit per §B.6.
- `/home/li/primary/skills/intent-log.md` — needs the new §"Citing
  intent in prose — bracket-quote the summary" section per Spirit 1522
  + 1526.
- `/home/li/primary/skills/component-triad.md` §"Proposed rename" — needs
  the Spirit-1428 ratification update.
- `/home/li/primary/skills/skill-editor.md` §"Skills never reference
  reports" — the rule violated by stale citations in 6 other skills;
  the proposed fixes in §C.1 inline-or-remove per this rule.

## Open recommendation for the orchestrator

The audit surfaces **16 actionable findings** across 11 skill files plus
**47 reports** to migrate from pseudo-NOTA to YAML front matter. The
recommendation:

1. **Land the discipline edits first** — `skills/reporting.md` §"Report
   header" gets the YAML front matter section per §B.5; `skills/report-
   naming.md` gets the variant-in-filename update per §B.6; `skills/
   intent-log.md` gets the bracket-quote citation section.
2. **Then the migration pass** — 47 reports rewritten to YAML front
   matter in one or a few commits.
3. **Then the cleanup pass** — the 11 stale-citation / drift skill
   edits per §C.1, in order of severity (Contradiction > Drift > Stale
   > rule-violation > possible-drift).

The work is mechanical once the discipline edits are in place. The
report itself (this one) uses YAML front matter at top to demonstrate
the new convention by example — see the file's first 12 lines.
