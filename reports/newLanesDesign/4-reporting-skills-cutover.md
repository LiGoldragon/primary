---
title: 4 — reporting + report-naming skills cutover to session lanes
role: newLanesDesign
variant: Design
date: 2026-06-24
topics: [reporting, report-naming, lanes, sessions, drain]
description: |
  Slice 4 of the newLanesDesign session. Cuts skills/reporting.md and
  skills/report-naming.md over from the fixed reports/<role>/ model to the
  session-lane model: reports/<lane>/ session directories, per-lane numbering,
  the fresh-context pickup-point principle (reports as clean-context handoffs
  with implementable work linked into a bead dependency graph), and the
  reframing of report hygiene as session drain (three-fate disposition:
  intent / work / abandon) with directory-as-GC-unit retirement recorded in
  protocols/retired-lanes.md.
---

# 4 — reporting + report-naming skills cutover to session lanes

## What changed

Two skills now teach the session-lane model decided in this session's
frame (`reports/newLanesDesign/0-frame-and-method.md`) rather than the
retired fixed-role-lane model.

`skills/reporting.md`:

- **role → lane everywhere.** `reports/<role>/` subdirectories became
  `reports/<lane>/` session directories named for the session's intent
  (`newLanesDesign`, `schemaWorkAudit`); discipline is metadata that
  loads skills and authority, not the directory name. Updated in the
  Reports-vs-chat intro, "Where reports live", every chat-path example,
  the questions-to-user example, filename/numbering sub-sections (now
  "per-lane"), the cross-references section and its inline-summary
  example (`operator/33` → `proposalReview/3`), and the See-also.
- **New §"Reports are fresh-context pickup points"** (decision 5),
  placed early as a core principle: a report is written so a
  clean-context agent can pick up, reason, and — where implementable —
  implement; implementable work links into a bead dependency graph via
  `bd dep <blocker> --blocks <blocked>`. The report carries the *why*
  and shape; the bead graph carries the ordered next steps.
- **Hygiene reframed as session drain.** The old "soft cap: 12 reports
  per role subdirectory / periodic review when full" model is gone — a
  session directory is not an accumulating-then-pruned archive. It
  split into two sections: §"Within-session supersession" (the
  delete-predecessor-in-same-commit mechanism, kept) and §"Session
  drain — the lane's reports route to intent, work, or abandon" (the
  three-fate disposition table; the session directory as GC unit;
  delete the whole directory at drain and record retirement in
  `protocols/retired-lanes.md`).
- **Meta-report directory → the session directory.** §"Meta-report
  directories — sub-agent sessions" became §"The session directory —
  fleet of sub-agents": the lane directory holds the frame, the
  fleet's slices, and the synthesis; GC now points to the drain
  section. The YAML `role:` field example shows a lane value
  (`newLanesDesign`) and its description clarifies it is the
  session-directory name, not the discipline.

`skills/report-naming.md`:

- **Filename grammar** `reports/<role>/...` → `reports/<lane>/...`;
  `<N>` is per-lane; the worked example and the next-number scan use
  `<lane>`.
- **New §"Reports are fresh-context pickup points"** mirroring the
  principle (tight, one mention of `bd dep`).
- **New §"Session drain and directory retirement"**: the lane
  directory is the GC unit; drain routes every idea to intent / work /
  abandon; retirement deletes the directory and appends one entry to
  `protocols/retired-lanes.md`.

## What was preserved verbatim in shape

Per the slice instruction, these kept their substance and structure:
the kinds-with-destinations table (closed kind set + destination
homes), YAML front matter rules, the chat-vs-report discipline and the
3-7-item paraphrase rule, the questions-to-user paste-the-evidence
rule, and all the visuals rules (Mermaid-only, 3-6 node budget,
implementation-code-stays-out). Only their `<role>` path tokens were
retouched.

## Cross-file coherence note

`protocols/retired-lanes.md` is referenced by both edited skills as the
append-only retired-lane registry. This slice does not create that file
(out of scope — other slices own the protocols/AGENTS surfaces); both
skills now name it as the retirement destination, so the file must
exist for the rule to be actionable. Flagging for the synthesis.

The `private-repos/<role>-reports/` path (assistant/counselor private
reports) was deliberately left role-keyed: private substance still
lives under discipline-named directories, which is a separate surface
from the public session-lane report tree and outside this slice.
