# Skill — intent maintenance

*Sweep the intent log: detect supersession, verify entries still
apply, archive overrides explicitly. The discipline that keeps
`intent/` from rotting as the workspace and the author's positions
evolve.*

---

## What this skill is for

`skills/intent-log.md` covers recording. This skill covers
*everything that happens to an entry after it's recorded*. An intent
log without maintenance becomes a graveyard of contradictory or
stale statements no future agent can trust.

Three operations: **supersession** (author overrides a prior),
**verification** (does the entry still describe how the workspace
actually works?), and **archival** (moving superseded entries out
of active queries without deleting their content).

---

## Supersession protocol — never silent

When an agent encounters a new author statement that contradicts a
prior recorded entry:

1. **Surface the contradiction inline, before recording.** Quote the
   prior verbatim and its certainty, and ask:

   > *"You said earlier (file `intent/<topic>/<file>.nota`):*
   > *— `<prior summary>`*
   > *— `<prior verbatim quote>`*
   > *— certainty `<prior certainty>`, recorded `<prior timestamp>`*
   >
   > *Now you're saying `<new summary inline>`. Override the prior, or
   > am I misreading?"*

2. **Wait for the author's confirmation.** Three possible answers:

   | Author says | Action |
   |---|---|
   | "Yes, override" | Supersede per step 3 |
   | "No, clarify — the prior still applies, this is a refinement" | Record the new entry as `Clarification`; prior stays active |
   | "Both apply in different contexts" | Record the new entry; add a `Clarification` linking them |

3. **On confirmed override:** write a `Superseded` record into the
   topic's directory, then physically move the prior file to
   `intent/<topic>/superseded/`.

   ```nota
   (Superseded
     "<prior-filename>"
     "<new-filename>"
     <ISO-8601 timestamp of supersession>)
   ```

   (Three positional fields: prior path, new path, timestamp.
   Timestamp written bare per the canonical NOTA shape; codec
   support tracked by bead `primary-dzrn`.)

   The `Superseded` record lives in `intent/<topic>/supersessions.nota`
   (one file per topic, append-only).

Supersession is **always explicit, and only the psyche can supersede
psyche intent.** A new psyche statement is the only source that can
override a prior psyche statement. An agent encountering documented
intent that seems wrong does NOT supersede on its own authority; the
agent asks the psyche (`skills/intent-clarification.md`). An author
entry is never quietly overwritten by another author entry, and
never overwritten by agent inference. This is the load-bearing
protection against agent hallucination passing as psyche intent.

---

## Verification — does the entry still apply?

Periodically (when sweeping the log, or when an entry's substance
crosses the agent's path), verify that the recorded entry still
matches workspace reality. Three failure modes to check for:

- **The workspace evolved past the entry.** The author said "X is
  forbidden" in a context that no longer exists. If the constraint
  no longer applies, the author likely needs to confirm a
  supersession (the constraint may have implicitly retired with the
  context).
- **The recorded summary doesn't match the verbatim.** Agent
  rephrasing drift; the summary says one thing, the quote says
  another. Fix the summary to match the quote.
- **The certainty doesn't match the phrasing.** Re-read the quote
  against `skills/intent-log.md` §"Certainty vocabulary". Correct
  if mismatched.

Verification corrections that aren't superseding the author's
intent (just fixing the agent's transcription) can land directly —
they're discipline cleanup, not author overrides. Log the change in
the commit message ("intent: corrected summary in `<file>.nota` to
match verbatim").

---

## Sweep — when and how

Trigger a sweep when:

- A topic directory grows past ~10 entries — that's the soft
  threshold where the topic is probably overdue for supersession
  cleanup or sub-topic splitting.
- An agent reviewing a topic notices an entry that no longer
  matches the workspace.
- `skills/context-maintenance.md` runs (intent log is part of the
  workspace state that maintenance can touch).
- Major redesigns (the kind that generate /v2 reports) — the
  redesign's premises likely supersede earlier intents.

How:

1. Read every entry in the topic's directory.
2. For each entry, check: does this still apply? Does the summary
   still match the verbatim? Does the certainty still match the
   phrasing?
3. For entries that no longer apply: ask the author for a
   supersession (the entry might just need an explicit override
   rather than silent retirement).
4. For entries with agent-transcription drift: correct directly.
5. For sub-topics splitting: move related entries into a more
   specific sub-topic file; leave a `(SubTopicSplit "old-file" ["new-file-1" "new-file-2"] "<timestamp>")`
   record in the topic's `supersessions.nota`.

---

## Don't delete — archive

The `intent/<topic>/superseded/` subdirectory holds prior entries
that have been overridden. Git history holds everything; the
`superseded/` move keeps the workspace tree showing only currently-
active entries while preserving the lineage at filesystem level for
agents who don't reach for `jj log`.

Do **not** delete a superseded entry from git history. Even when
the author overrides their own prior intent, the prior matters as
context for understanding the override.

---

## When to skip the surface

Some author statements are too transient for the log:

- "Let's try this and see" — pre-commitment exploration.
- "Maybe X, I'll think about it" — `Minimum`-certainty might be
  worth recording, but if the psyche then commits to something
  else within the same conversation, skip recording the
  intermediate.

If you skip recording a borderline case, the author can ask later
"why isn't this in `intent/`?" — at that point, record it.

---

## Forward — persona-mind migration

When persona-mind's typed memory variants land, supersession
becomes a typed relation (`Supersedes` linking two
`Authorial<Kind>` memories), and the `superseded/` subdir
retires — the relation graph carries the lineage. Until then,
filesystem-level archival is the carrier.

---

## See also

- `skills/intent-log.md` — recording discipline; record shape;
  certainty vocabulary.
- `skills/context-maintenance.md` — workspace-wide sweep
  discipline; intent log is one of the things context-maintenance
  may sweep.
- `skills/nota-design.md` — positional-NOTA discipline these
  records follow.
- `intent/` — the surface this skill maintains.
