# Closeout — skill-description realignment (2026-06-24)

Mechanical realignment of `skills/skills.nota` so every skill is findable by
purpose + trigger, with skill metadata living in exactly one place. No body
work beyond duplicate-tagline removal; nothing committed.

## Counts

- **Descriptions rewritten to the rubric: 67** of 71 entries. Each was recast
  to purpose + trigger (what decision/task the skill guides, and when to reach
  for it), positively framed, at most two sentences. Kind, name, path, and Tier
  were left exactly as-is on every entry.
- **Descriptions left essentially as-is: 0.** Even the already-good entries
  (`abstractions`, `naming`, `enum-contact-points`, `report-naming`) carried a
  contents-summary tail rather than an explicit trigger, so each got a light
  trigger clause appended in the same voice. The four already fully on-rubric in
  spirit (the role apex lines, which were bare topic labels like
  `Prose as craft.`) were rewritten to add the missing trigger.
- **New entries added: 1** (`context-maintenance-deep`, the unindexed file —
  see below). Total entries after the pass: 71.

The pass leaned on text already present in each entry; for the genuinely
too-short/vague ones (`mermaid`, `stt-interpreter`, `testing`, `nota-design`,
`nota-comments`) I read the target file's opening ~15 lines to write a real
purpose + trigger rather than guess.

## Before -> after examples

- `spirit-cli`
  - Before: `How to invoke the deployed Spirit 0.13.0 CLI. RecordRequest shape, maintenance operations, missing ResolveClarification protocol, bare-string canonicality, recursive Domain records, separate certainty and importance, eight-field query shape, justifications, privacy, inline NOTA vs file-path argument, and deployed-source verification.`
  - After: `How to invoke the deployed Spirit CLI to capture or query intent — RecordRequest shape, operations, query shape, inline-NOTA vs file argument, and reading the current wire shape from source. Reach for it before any Record or Observe.`

- `mermaid` (was too short)
  - Before: `Mermaid diagram conventions and safe-syntax workarounds.`
  - After: `The Mermaid renderer quirks, safe-syntax workarounds, and readability rules that make a diagram survive the strictest target renderer. Reach for it when authoring a Mermaid diagram.`

- `stt-interpreter` (was too short)
  - Before: `Speech-to-text interpreter integration notes.`
  - After: `How to decode speech-to-text prompts that mis-transcribe workspace-specific words — guess the intended word and act, asking only if wrong. Reach for it when a prompt contains a phonetic near-miss for a known workspace term.`

- `double-implementation-strategy` (was an over-long mini-essay)
  - Before: `Two parallel implementation tracks for a major break, BOTH on branches: operator amalgamates best-of-prototypes toward main; designer iterates the forward-looking design on next / a feature branch. Comparison drives convergence. Anti-drift mechanism. New repos are NOT used — major breaks are branches, a new repo is only for a genuinely new project (Spirit op4b / 53bj, 2026-06-07).`
  - After: `How to run two parallel implementation tracks for a major break — operator amalgamates best-of-prototypes toward main while designer iterates the forward design on a branch — using comparison to drive convergence. Reach for it when a major break needs an anti-drift strategy.`

## YAML frontmatter strip

`skills/human-interaction.md` was the only skill file carrying YAML
frontmatter. Removed the leading `---` … `---` block (name / description /
metadata.tier / metadata.kind); the body now starts at `# Skill — human
interaction`. The corresponding `skills.nota` entry already carried the correct
`Meta` Kind and `Apex` Tier; its description was rewritten to the rubric. No
frontmatter was added to any file.

## Opening taglines removed (all of them)

This pass first removed only the four taglines that were verbatim restatements
of their description. The psyche then decided **no opening tagline at all** — the
description lives solely in `skills.nota`, so a skill file carries no purpose line
whatsoever. A follow-up sweep removed the rest: **47 files total** now have their
opening `*…*` tagline deleted, leaving the `# Skill — <name>` heading followed
directly by the first section or body. The remaining files never had a standalone
tagline. `skills.nota` and `skill-editor.md` were handled separately (below).

## Unindexed-file resolution

`find skills -name '*.md'` returns 71 files; the index referenced 70. The
unreferenced file was `skills/context-maintenance-deep.md` — a real skill (the
heavier cross-lane maintenance patterns: cross-lane sweeps, the cross-lane
meta-report directory, lane retirement), the explicit sibling of the indexed
`skills/context-maintenance.md`. Added an entry by analogy to its sibling
(`Meta` Kind, `Mechanism` Tier):

`(Meta context-maintenance-deep skills/context-maintenance-deep.md Mechanism [How to run the heavier maintenance patterns — cross-lane sweeps, the cross-lane meta-report directory, and lane retirement. Reach for it when a sweep spans more than one lane.])`

Placed immediately after the `context-maintenance` entry. The index now covers
all 71 files; zero unindexed, zero missing paths.

## Flagged-unclear skills

None. Every skill's purpose was clear from its index text or opening lines; no
description was left at the original wording for lack of clarity.

## Validation

- `skills.nota` contains zero quotation marks (NOTA-clean).
- 71 positional records; all reference existing files; no file unindexed.
- Kind / name / path / Tier preserved on every pre-existing entry; only the
  `[Description]` field changed.
- Parens (76/76) and brackets (72/72) balanced; spot-checked rewritten files
  (`designer`, `alignment-interview`, `intent-log`) — bodies intact, only the
  opening tagline gone.

## Manifestation, captures, and commit state

The rules this pass enforces now live where skill-authors will see them.
`skill-editor.md` lost its own tagline, dropped the `*<one-line purpose>*` line
from its file template, and gained a "The index entry is the description" section
stating the single-source rule and the purpose+trigger rubric.

Intent captured or edited this session: the description rubric (purpose + trigger,
two sentences, positive); the single-source / no-frontmatter / no-tagline rule
(superseding the earlier no-duplicate-tagline form); the workspace-wide
positive-framing golden rule (enriched); and the one-question alignment-interview
format.

All changes are committed and pushed to `main` — drained across two shared
working-copy commits by peer lanes (generic message "commit pending skill
edits"), not by a dedicated push. `skills.nota`, `skill-editor.md`, the 47 tagline
files, the frontmatter strip, and reports 728/729 are all on origin/main.
