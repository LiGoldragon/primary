# Remembering — design (draft, evidence in flight)

Remembering brings a past flow back into a present flow through the
flows protocol: the contextualized psyche and a high-level awareness of
the work done. It is an extension of the flows skill, not a standalone
skill, because the flow log is what makes a remembering traceable — each
log records what its flow remembered, and the chain traces back log by
log. A standalone skill would have no home for the trace.

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

Proposal: `reports/remembering<ShortId>.md` in the remembering flow's
directory — a report like any other, per the existing artifact rules.
Filing it memoizes the chain: a flow remembering this one at depth two
reads this flow's remembering reports instead of re-mining, which is
what makes deep remembering affordable.

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
> psyche records verbatim, a high-level awareness of their work from
> log and reports, a light check of the current state of what their
> topics touched, and a light summary for the psyche in simple words
> and visuals. A remembering goes in `reports/remembering<ShortId>.md`;
> its log entry names the flows remembered and the depth. One layer at
> session start; a stated number when going deep into a topic; the
> whole chain only on the psyche's explicit word.

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

1. Filed or context-only? Recommended: filed as a report (memoizes the
   chain; matches existing artifact rules).
2. The deep-work depth number: fixed once, or stated per occasion in
   the log? Recommended: stated per occasion.
3. Annotations stay as they are — remembering reads them, never
   replaces them. Confirm.

## Sources

- The psyche's brief, verbatim: flows/b7465e71/vision/remembering.md.
- Deployed flows skill text as loaded this session (authored-source
  fetch and diff in flight).
- Rememberings of 5c8be3ca and 15b67974 in flight; prior-art search of
  the reference skill collections in flight.
