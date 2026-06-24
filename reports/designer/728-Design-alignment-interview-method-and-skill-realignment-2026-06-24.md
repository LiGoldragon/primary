# Design — alignment-interview method and the first application (skill realignment)

*Interview frame. Round 1. This report is the session log; chat is its paraphrase.*

## What this interview is designing

Two layers at once, because they are the same act:

1. **The method** — a repeatable designer flow: *alignment interview* (back-and-forth
   with the psyche, no workflows/sub-agents for the replies; sub-agents only to research
   context for better questions) → *alignment report* (sub-agents write it once we agree)
   → *dependency graph of vertical slices* that an implementing agent reads to spawn
   parallel sub-agents along the DAG.
2. **The first application** — realign all 144 skills, starting from the `skills.nota`
   descriptions, which read as compressed content-summaries instead of *why-read-this /
   when-to-reach-for-it*.

Per Spirit `kxzh` (Decision High): [when the psyche talks to a role, that conversation
designs that role's operating skill]. The skill-realignment task is also the proving
ground for the method.

## Research synthesis (two background sub-agents)

**Operator's source — `reports/operator/461-Research-ai-coding-workflows-matt-pocock.md`.**
Pocock's end-to-end loop: research/prototype → grill session → write the PRD (a
*destination document*: problem, solution, user stories, implementation + testing
decisions, out-of-scope = definition of done, proposed modules — code-aware from the
start) → slice the PRD into a Kanban **DAG** of issues with explicit blocking edges →
implement with AFK agents under **write-the-test-first** → automated review + human QA →
loop QA-generated issues. Slices are **vertical** ("traceable bullets" crossing enough
layers to be observable/testable) rather than horizontal (DB→API→UI), because horizontal
planning delays integrated feedback. Parallel "Sandcastle" workflow: a *planner* picks
unblocked issues, *implementers* run in per-issue worktrees, a *reviewer* works in fresh
context, a *merger* integrates. This is exactly the shape the psyche is adapting.

**`skills.nota` state — 144 entries**, shape `(Kind name path Tier [Description])`.
Roughly: ~25 descriptions too long (content-summaries — worst: `structural-forms`,
`spirit-cli`, `intent-log`, `double-implementation-strategy`, `human-interaction`,
`main-next`, `workspace-update-report`); ~15 too short / un-triggered (`mermaid`,
`stt-interpreter`, `testing`); ~85 about right (`abstractions`, `naming`,
`enum-contact-points`, `report-naming`, and the existing `alignment-interview` entry).
The fault is symmetric: over-long ones summarize the file; too-short ones give a bare
topic label. Neither tells an agent *why to open it and when*.

## Constraints from existing intent (must fit inside these)

- `k4i3` (Principle VeryHigh): [Skills are tight self-contained teaching, not logs… A
  skill cites nothing external… Brevity is load-bearing… Cut hard: state the rule and the
  why, keep at most one example. The same restraint applies to reports — fewer and
  tighter.] — the rubric is a specialization of this, not a new axis.
- `7nbu` (Principle High): [Designer's deliverable is intent / architecture / skills, not
  reports] — keep this and every interview report tight; the realigned skills are the
  product.
- `o7zt` (Correction VeryHigh) and the `alignment-interview` skill itself: plain language,
  expand/avoid jargon — say *alignment report* not *PRD*, *write-the-test-first* not
  *TDD*. The psyche already renamed to "alignment report" and "dependency graph", so the
  jargon fork resolves toward plain names.
- `amb5` (Decision High): report filename `<N>-<Variant>-<topic>-<date>.md`; `g9oc`
  (Constraint High): chat prints full relative report paths. Candidate meaning of "enforce
  reports better".

## Proposed method shape (for ratification)

- **Interview**: one focused decision at a time (or a tight batch), each carrying
  decision / why / recommended answer / alternatives. Sub-agents research; the psyche and
  I converse until the open decisions no longer change the first slice.
- **Alignment report**: written by sub-agents after agreement. Recommend it be *one
  self-contained document* ending in the dependency graph, so a single read briefs the
  implementing agent and seeds the DAG.
- **Vertical-driven**: build the thinnest end-to-end path first so the whole system is
  observable, then iterate by adding features. For skill realignment the analogue is:
  take a few representative skills all the way through every stage (rewrite description →
  update index → check body vs `k4i3` → manifest if intent shifts → report enforced)
  before fanning out across all 144.
- **Parallel implementation**: clear context, then an implementing agent spawns one
  sub-agent per ready DAG node, respecting blocking edges.

## The description rubric (keystone — every sub-agent applies it)

Recommended shape: **purpose + trigger, ≤2 sentences** — what decision/task the skill
guides, and when to reach for it. Not a summary of the file; not a bare topic label.

Example, `spirit-cli`:

- BEFORE (~49 words, content summary): "How to invoke the deployed Spirit 0.13.0 CLI.
  RecordRequest shape, maintenance operations, missing ResolveClarification protocol,
  bare-string canonicality, recursive Domain records, separate certainty and importance,
  eight-field query shape, justifications, privacy, inline NOTA vs file-path argument, and
  deployed-source verification."
- AFTER (~28 words, purpose + trigger): "How to call the deployed `spirit` binary to
  capture or query psyche intent. Reach for it before any Record or Observe — for the
  invocation shape, the operations, and how to read the current wire shape from source."

## Decisions (resolved)

1. **Rubric** — each `skills.nota` description states purpose + trigger in at most two
   sentences, framed positively: what the skill guides and when to reach for it. (Spirit `9x28`.)
2. **Single source** — `skills.nota` *is* the description. Skill files carry only their
   teaching body: no YAML frontmatter, no tagline repeating the description. (Spirit `1p0r`.)
3. **Scope** — descriptions + frontmatter strip + drop duplicate taglines. No body work
   this pass; flag bloated bodies for a separate later pass. (Task state.)
4. **Interview format** — one focused question per turn, plain chat prose, no
   questionnaire UI. (Spirit `ljce`.)
5. **Golden rule** — state everything positively: what a thing is, what we want from it,
   and why; the why outweighs the what-not-to-do. (Spirit `jlo7`, enriched.)

## The surface (measured)

70 skills, one description and one file each. About half need a real rewrite, the rest a
glance. One file (`human-interaction.md`) carries YAML frontmatter. One `.md` is unindexed
— a gap to fold in or drop. One lean session, one agent, no fan-out.

## Dependency graph (flat)

```
rubric + single-source + golden rule (all settled)
        │
        ▼
rewrite 70 descriptions in skills.nota   ──▶  verify pass  ──▶  done
strip 1 YAML block / drop dup taglines
resolve the 1 unindexed file
```

The description rewrites are independent — no blocking edges among them. The only
prerequisite (rubric + single-source) is already settled.

## Handoff (task state)

- **Goal**: every skill findable from the index by purpose and trigger, in one place.
- **Done**: 70 on-rubric positive descriptions; no YAML frontmatter; no duplicate
  taglines; stray file resolved.
- **Out of scope**: skill body trimming (later, separate pass).

## Captures this session

`ljce` (interview format), `jlo7` (golden rule, enriched), `9x28` (rubric), `1p0r`
(single source / no frontmatter). Rubric and golden rule manifest into the
skills-authoring guidance during the pass.
