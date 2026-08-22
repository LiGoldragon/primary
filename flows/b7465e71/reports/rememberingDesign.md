# Remembering — design

Remembering brings a past flow back into a present flow through the
flows protocol: the contextualized psyche and a high-level awareness of
the work done. It is an extension of the flows skill, not a standalone
skill, because the flow log is what makes a remembering traceable — each
log records what its flow remembered, and the chain traces back log by
log. A standalone skill would have no home for the trace.

## Grounding in the psyche

- psyche-raw/Vision/flowKnowledge.md L51 (heard in 15b67974),
  verbatim: "Iv assumed a lot in the last few months. I thought agents
  would carry on momentum. that is now thoroughly disproven."
  Remembering is the deliberate act that replaces the assumed
  momentum: what does not carry on its own is brought back on purpose,
  and the bringing-back is logged.
- psyche-raw/Vision/psycheLogStructure.md L331-334 (heard in
  15b67974), verbatim: "now im considering moving psyche logging into
  the flow protocol as well, and emphasizing more frequent psyche
  distillation, with distilled entries kept in their flow's directory
  but moved into a 'distilled' file or something similar." The vision/
  cutover put the psyche's words into the flow protocol; remembering
  is the reading side of the same move — vision/ holds what a flow
  heard, remembering brings it back.
- psyche-raw/Vision/flowArtifacts.md L16-20 (5c8be3ca-2), the
  no-handoff fresh-view ruling — treated in the tension section below.

## Anatomy of one remembering

Per remembered flow, four parts:

1. **Contextualized psyche** — the psyche records that flow heard
   (its `vision/`, rulings in its log), brought back verbatim.
2. **High-level awareness** — what was done, decided, and left open;
   drawn from the flow's log and reports, not a re-read of everything.
3. **Light current-state audit** — the things touched by the topics
   covered in the past: one look each — moved, drifted, landed,
   superseded, still standing.
4. **Light summary** — the whole, in very simple words and visuals,
   shown to the psyche.

## Depth

- Fresh session startup: one layer — the named flows only — unless
  told otherwise.
- Going deep into a topic: up to a stated number of layers.
- The psyche's explicit word: unlimited — mine to the deepest layer.
  Rare.

## The chain and the trace

A flow's **past** is the flows it has remembered (the psyche's own
shorthand: "the topics covered in your past"). The log entry for a
remembering names the remembered flows and the depth; tracing the chain
back is following those entries through the logs.

## Where a remembering lands

The psyche ruled (vision/remembering.md, 2026-08-22): if the flow
pulls things into its context, it has remembered — the act, not an
artifact. No remembering report. The main log file holds the
remembered flows.

This dissolves the tension with 5c8be3ca-2 (psyche-raw/Vision/
flowArtifacts.md L16-20, the no-handoff fresh-view ruling): with no
formed-view artifact in the protocol, every layer of remembering reads
the remembered flows' own artifacts and forms its own view — there is
no old opinion to impose. The cost of remembering rises with depth,
since each layer is read from its own artifacts; the depth gates are
what keep that affordable.

## The log line

Nothing parses the flow log, so frontmatter has no consumer there: its
`---` delimiters cost only a few tokens, but they buy structure that
only a parser would use. A labeled plain line inside the dated log
entry serves both the model and probes — stable label, one fact per
line, greppable (`grep -h '^Remembered:' flows/*/log.md` walks the
chain) — and the workspace already carries the idiom
(SKILL_VARIABLES.md: one `Name: value` per line). Proposed, one line
per remembering act:

    Remembered: 5c8be3ca, 15b67974 — depth 1

## Proposed exact wording

Target: the authored source
`/git/github.com/LiGoldragon/Curriculum/skills/flows.md` (subflow
witness: the generated `.claude/skills/flows/SKILL.md` is stale — it
lacks the authored paragraph on creating `log.md` at first prompt and
appending the index line; regeneration owed regardless of this
proposal).

In flows.md, replace the sentence

> Earlier work is continued by reading the flows concerned and forming
> a fresh view.

with

> Earlier work is continued by remembering the flows concerned: their
> psyche records, a high-level awareness of their work from log and
> reports, and a light check of the current state of what their topics
> touched, with the result shown to the psyche in simple words and
> visuals. The log records each remembering as
> `Remembered: <short-ids> — depth <n>`. One layer at session start; a
> stated number when going deep into a topic; the whole chain only on
> the psyche's explicit word.

(The annotations sentence that follows stays untouched.)

In `/git/github.com/LiGoldragon/Curriculum/skills/vocabulary.md`,
add the entry

> Past: the flows a flow has remembered, and theirs in turn.

The flows skill then uses "past" without defining it — vocabulary holds
the term, per skill-designing's rule against restating another skill's
rule. What this change preserves: the annotations path, all artifact
rules, the report form (a remembering is an ordinary report). What it
changes: continuing earlier work becomes a logged, traceable act with
named depth. What it removes: the unlogged "read and form a fresh view"
continuation, which left no trace of what was brought back.

## Prior art

The reference skill collections hold no equivalent (subflow search,
2026-08-22). Closest: compaction-recovery ledgers and cross-session
plan files (obra/superpowers — durable files a cold session reads and
trusts), and managed-agents memory stores (anthropics/skills — a
mounted persistent directory). All three restore work state only.
Remembering differs on three points: it restores the psyche's verbatim
words alongside the work; the recall itself is logged with depth, so
the chain of rememberings traces back; and it re-witnesses the present
(the light audit) instead of trusting the stored record — the ledger
patterns explicitly trust the ledger over the world.

## Open questions for the psyche

1. The log line's shape: `Remembered: <short-ids> — depth <n>`, one
   line per remembering act, inside the dated entry. Confirm or
   adjust.
2. The deep-work depth number: stated per occasion (it is visible on
   the Remembered line), rather than fixed once. Confirm.
3. Annotations stay as they are — remembering reads them, never
   replaces them. Confirm.

Settled by ruling (vision/remembering.md, 2026-08-22): no remembering
artifact — the act lands in context, the trace in the log. Vocabulary
entry approved, held until the flows edit settles. The two remembering
reports this flow filed before the ruling
(reports/remembering5c8be3ca.md, remembering15b67974.md) predate it;
they can stand as this flow's ordinary research reports or be deleted
on the psyche's word.

## Sources

- The psyche's brief, verbatim: flows/b7465e71/vision/remembering.md.
- reports/remembering5c8be3ca.md and reports/remembering15b67974.md
  (this flow) — psyche records verbatim with locations, work
  awareness, current-state witnesses, chain links.
- Authored sources, subflow witness (Method: code read
  /git/github.com/LiGoldragon/Curriculum/skills/flows.md and
  vocabulary.md; diff against .claude/skills/ copies — flows deployed
  copy stale, vocabulary body identical).
- Prior-art subflow search of the reference skill collections
  (anthropics/skills, obra/superpowers): no equivalent found; closest
  work-state-only patterns cited in Prior art.
- Flows: 5c8be3ca, 15b67974, b7465e71.
