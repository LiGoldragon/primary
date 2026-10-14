# Crystallization inventory (read-only survey, 2026-10-13)

Origin/main after fetch: psyche-skills b615e96, mind-skills c054cec, field-skills 14269e9 (under /git/github.com/LiGoldragon). Case-insensitive match `distil`.

## 1. The packet

Unavailable. /home/li/primary/flows/d68c82/reports/spirit-packet-recrystallization-2026-10-12.md does not exist: not in the working tree, not in git history (log --all), no file named *recrystal* under flows/. d68c82/reports holds fable-packet-undistilled-2026-10-12.md (three subjects: delegation, words travelling whole, the Primary spoken to least; not a recrystallization packet) and reports/logos/syntax-recrystallization-audit-v1.md (a syntax audit, not read). So no summary and no record headings are given. Decision needed: the correct path, or confirmation that the packet is yet to be written.

## 2. Counts (matching lines at origin/main)

| Repository | Files with matches | Lines |
|---|---|---|
| psyche-skills | 4 | 16 |
| mind-skills | 6 | 30 |
| field-skills | 4 | 5 |
| Total | 14 | 51 |

### (a) Module file names
- psyche-skills/skills/vision-distillation.md -> vision-crystallization.md
- mind-skills/skills/operation-psyche-distillation.md -> operation-psyche-crystallization.md
- field-skills/skills/compensation-book-distillation.md -> compensation-book-crystallization.md

### (b) Lines by file (file:line)
psyche-skills
- spirit-core.md: 3 (dependencies, see c)
- vision-book.md: 3 (dependencies); 8 "Every book has a distillation section: ..."
- vision-distillation.md (10): 2 description "A distillation proposal is composed or judged..."; 3 dependencies; 9 "when distillation finds it"; 13 heading "Impurities fall out through distillation"; 15 (x2) "...in the course of distillation: a distillation"; 21-22 "A distillation proposal ... corrected by a distillation"; 27 "A distilled statement carries..."; 39 "A distilled statement carries no useless negative"; 44 "a distilled statement never says so of itself".
- vision-psyche.md (3): 2 description "...how distilled vision keeps its provenance"; 8 "Everything the living says he wants is distilled"; 15 "Distilled vision preserves references..."

mind-skills
- knowledge-psyche.md (5): 52 "distilled vision"; 54 "distilled intent"; 60 "undistilled vision corpus"; 61 "draining into vision skills as distillation"; 66 "Intent and Spirit can only be distilled."
- operation-book.md (2): 3 dependencies; 23 "If the source lacks distillation,"
- operation-design.md: 16 "compose a distillation presentation"
- operation-psyche-acquisition.md: 15 "do not summarize or distill"
- operation-psyche-distillation.md (19): lines 6, 8, 10, 12, 15, 17, 19, 20, 22, 25, 26, 27, 29, 31, 34, 40, 43, 45, 46 (the whole module; line 6 "Distillation re-articulates psyche records...")
- operation-psyche-interraction.md (2): 9 "enters a vision- skill only as a distillation"; 32 "never logged or distilled as a statement of its own"

field-skills
- compensation-book-distillation.md (2): 6 "Every book the living reads is distillation proposals, 99% of it..."; 18 "the record it distils by path and date"
- compensation-launch.md: 40 "...Psyche distils its context for vision, intent and spirit"
- compensation-orders.md: 17 "Exploratory material need not be distilled at once."
- trial-presentation-book.md: 3 (dependencies)

### (c) Frontmatter naming the modules (all are `dependencies:` lines; no description names a module)
- psyche-skills/spirit-core.md:3 -> compensation-book-distillation
- psyche-skills/vision-book.md:3 -> vision-distillation
- psyche-skills/vision-distillation.md:3 -> operation-psyche-distillation
- mind-skills/operation-book.md:3 -> compensation-book-distillation
- field-skills/trial-presentation-book.md:3 -> compensation-book-distillation
Frontmatter descriptions containing the word: vision-distillation.md:2, vision-psyche.md:2.

### (d) /home/li/primary
- SKILL_VARIABLES.md, CLAUDE.md, NON_MANAGEMENT_AGENTS.md: 0 matches.
- tools/book-check.mjs (7 lines): 5 comment; 9 `hasDistillation`; 12 reason "empty-distillation"; 44 regex `/^(?:\d+[.)]\s+)?distillation\b/i` on headings (the required "## Distillation" heading); 46; 56 reason "missing-distillation".
- tools/book-check.test.mjs (10 lines): 9, 11, 12, 15, 18, 19, 41, 44, 53 use "## Distillation" and the two reason codes.
- tools/standing-skill-selection.mjs:4 lists "compensation-book-distillation".
- tools/native-main-flow-launch-shared.test.mjs:30, 33, 34 list compensation-book-distillation.
- tools/reap-flow:219 "Reports and logs may be distilled to a chronology" (different sense).
- Generated, list only (no edit): .claude/agents: book.md, book-page.md, write-/read-{ordinary,demanding,trivial}.md, tester.md (9 files); .codex/agents 10 files; .pi/agents 6 files; plus the 14 module copies under each of .agents/.claude/.codex/.opencode/.pi skills.
- Existing book sources (flows/*/books/*.md) carry "## Distillation" headings; after a regex change they fail book-check unless the check accepts both or they are renamed. Not counted here.

## 3. Renames and dependents

| Old | New | Files whose dependencies change |
|---|---|---|
| vision-distillation | vision-crystallization | psyche-skills/vision-book.md |
| operation-psyche-distillation | operation-psyche-crystallization | psyche-skills/vision-crystallization.md |
| compensation-book-distillation | compensation-book-crystallization | psyche-skills/spirit-core.md, mind-skills/operation-book.md, field-skills/trial-presentation-book.md, primary tools/standing-skill-selection.mjs, tools/native-main-flow-launch-shared.test.mjs |

## 4. Sentences where a plain swap reads badly (merged wording)

- operation-psyche-distillation.md:6 "Distillation re-articulates psyche records into self-standing statements." Swap loses the reason. Merged: "Crystallization re-articulates psyche records into self-standing statements and merges each with what is already crystallized, so the whole stays cohesive and the new reads as if always written with the original context."
- knowledge-psyche.md:60 "the undistilled vision corpus". Merged: "the vision corpus not yet crystallized".
- operation-psyche-acquisition.md:15 "do not summarize or distill". Distil there means condense, not merge. Merged: "do not summarize or rephrase".
- tools/reap-flow:219 "may be distilled to a chronology". Distil there means condense. Merged: "may be condensed to a chronology".
- operation-psyche-distillation.md:20 "the raw psyche it was distilled from". Swap works, but "crystallized from" should say what it merged into: "the raw psyche it was crystallized from".
- operation-psyche-distillation.md:17 "candidates for distilling together". Merged: "candidates for crystallizing together".
- vision-psyche.md:8 "Everything the living says he wants is distilled". Merged: "is crystallized into the existing vision".
- compensation-launch.md:40 "Psyche distils its context for vision, intent and spirit". Merged: "Psyche crystallizes its context into vision, intent and spirit".
- Derived forms: "distillation agglomerates" (line 10) becomes "crystallization agglomerates"; the noun "a distillation" (a proposal) becomes "a crystallization"; "distillery" does not occur.
