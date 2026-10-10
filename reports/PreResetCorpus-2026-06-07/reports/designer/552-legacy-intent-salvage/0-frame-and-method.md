---
title: 552 — Legacy intent salvage — frame and method
role: designer
variant: Audit
date: 2026-06-07
topics: [intent, spirit, intent-maintenance, legacy-nota, agglomeration, deletion-readiness]
description: |
  Frame + method for the legacy intent/*.nota salvage audit. The 16 legacy
  intent files (364 records, the pre-Spirit file substrate) are slated for
  deletion. Before deletion, mine them for CORE, durable, not-too-specific
  design intent that is genuinely AT RISK — not already captured in the
  deployed Spirit store and not already manifested into ESSENCE / AGENTS /
  INTENT / skills. This is propose-only: the audit suggests a few records to
  add to Spirit; the psyche decides which to record before the files go.
---

# 552 — Legacy intent salvage — frame and method

## The ask

[Audit the old .nota intent files. See if there's any intent — the core
ideas, not too specific because the specifics change — that looks meaningful
in terms of specifying design, and make suggestions on a few things that could
be added into Spirit from these files before we actually delete them. Not a
massive import.] (psyche 2026-06-07)

The deliverable is a **curated shortlist of suggestions**, not an import.
The psyche decides which suggestions become Spirit records; only then do the
legacy files get deleted.

## What the legacy substrate is

`intent/*.nota` is the **pre-Spirit file substrate** — the original intent log
before the deployed `spirit` daemon existed. Sixteen files, 364 records, 352K.
Record shape is the OLD form: `(<Kind> "summary" "verbatim" "context"
<Certainty> <Date>)` — double-quoted strings, with a certainty + date/time
tail. AGENTS.md and `skills/intent-log.md` both forbid appending here during
normal work; these files are **history**, kept only as historical input for
agents that have not yet absorbed Spirit. The plan is to delete them once
their salvageable core is preserved.

| File | Records | File | Records |
|---|---|---|---|
| workspace.nota | 79 | reports.nota | 24 |
| component-shape.nota | 65 | naming.nota | 21 |
| persona.nota | 61 | deploy.nota | 14 |
| nota.nota | 38 | spirit.nota | 7 |
| horizon.nota | 29 | nota-mixed-enum-support.nota | 7 |
| arca.nota | 6 | signal.nota | 6 |
| nix.nota | 3 | jj.nota | 2 |
| markdown.nota | 1 | intent-log.nota | 1 |

## The text-only extraction tool

The psyche asked for "a tool to just see the text part instead of reading all
the timestamps and stuff." Built `/tmp/intent_text.py`: a small NOTA-lite
tokenizer that walks each record and emits **Kind + Certainty + the prose
fields** (SUMMARY / VERBATIM / CONTEXT), dropping the date/time tail. It
handles both legacy `"double-quoted"` strings and modern `[bracket]` /
`[|multiline|]` strings. Output lives in `/tmp/intent-text/*.txt` — clean,
date-stripped, readable. Finders read those, not the raw `.nota`.

## Curation criteria — what counts as a salvage candidate

A legacy record is a **salvage candidate** only if ALL hold:

1. **Core / durable.** It states a design intent that still guides — a
   principle, a decision-shape, a constraint — not a one-off task order or a
   transient state reaction.
2. **Not too specific.** The specifics change (a specific rename, a specific
   field count, a specific file's line target). Mine the *general* idea behind
   the specific, or drop it. Per the psyche: "the specifics change."
3. **Genuinely at risk.** It is NOT already in the deployed Spirit store AND
   NOT already manifested into a durable guidance file (ESSENCE.md, AGENTS.md,
   per-repo INTENT.md, or `skills/`). An idea already living in ESSENCE or a
   skill is preserved — re-adding it to Spirit is the duplication the psyche
   does not want.

Most of the 364 records will fail criterion 3 — the naming rules, the
component-triad shape, the NOTA discipline, the reporting rules are all
already deep in the live guidance layer. The audit's value is finding the few
that fell through.

## Dedup method (each finder runs this)

- **Targeted Spirit queries.** For each candidate's domain, query the deployed
  store by topic:
  `spirit "(Observe (Records ((Partial [<topic> ...]) None Any VeryDeep SummaryOnly)))"`.
  Per-topic deep queries give complete coverage for that topic (verified:
  naming→21, nota→100). A recent-window dump is at `/tmp/spirit-current.txt`
  and the full topic list at `/tmp/spirit-topics.txt`.
- **Guidance-file greps.** `rg` the idea's keywords across `ESSENCE.md`,
  `AGENTS.md`, `INTENT.md`, and `skills/`. If the idea is already there, it is
  preserved — drop it.

## Method — fan-out

Ten finders mine the 16 files (big files solo, small files clustered), each
producing a numbered mining report in this directory and a structured
candidate list. One synthesis agent cross-dedupes across finders (the same
idea recurs across files), ranks by core-ness and at-risk, trims to the few,
and writes the overview with ready-to-run `spirit "(Record …)"` commands —
all flagged psyche-gated. File assignment:

| # | Finder | Files |
|---|---|---|
| 1 | workspace | workspace.nota |
| 2 | component-shape | component-shape.nota |
| 3 | persona | persona.nota |
| 4 | nota | nota.nota |
| 5 | horizon | horizon.nota |
| 6 | reports | reports.nota |
| 7 | naming | naming.nota |
| 8 | deploy | deploy.nota |
| 9 | small-cluster-A | arca, signal, spirit |
| 10 | small-cluster-B | nix, jj, markdown, intent-log, nota-mixed-enum-support |
| 11 | synthesis (overview) | all candidate lists |

## The gate

Propose-only. Recording any candidate goes through the Spirit gate
(`skills/intent-log.md`) and needs the psyche's go. Deletion of the legacy
files happens AFTER the psyche confirms the salvage set — not in this pass.
