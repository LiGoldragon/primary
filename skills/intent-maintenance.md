# Skill — intent maintenance

*Sweep the intent log: detect supersession, verify entries still
apply. Keeps `intent/` from rotting as the workspace and the
psyche's positions evolve. Companion to `skills/intent-log.md`
(recording).*

## Supersession protocol — never silent

When an agent encounters a new psyche statement that contradicts a
prior recorded entry:

1. **Surface the contradiction inline, before recording.** Quote
   the prior verbatim and its certainty, and ask:

   > *"You said earlier (file `intent/<topic>.nota`):*
   > *— `<prior summary>`*
   > *— `<prior verbatim quote>`*
   > *— certainty `<prior certainty>`, recorded `<prior timestamp>`*
   >
   > *Now you're saying `<new summary inline>`. Override the prior,
   > or am I misreading?"*

2. **Wait for the psyche's confirmation.** Three possible answers:

   | Psyche says | Action |
   |---|---|
   | "Yes, override" | Replace the prior entry with the new one (step 3) |
   | "No, clarify — the prior still applies, this is a refinement" | Add the new entry as `Clarification`; prior stays |
   | "Both apply in different contexts" | Add the new entry; the existing one stays |

3. **On confirmed override:** remove the prior entry from the
   topic file and add the new entry in the same commit. **This is
   one of the cases that needs a designer lock** (per
   `skills/intent-log.md` §"Recording is a lock-free shell
   append" — routine appends are lock-free, but rewrites that
   remove prior content need coordination). Name the supersession
   in the commit message (`intent: <topic> — psyche overrides
   prior <summary slug>; new <new summary slug>`).

**Git history holds the lineage.** No `superseded/` subdirectory,
no `Superseded` records in the file. The topic file always
contains the *currently-applicable* intent; the prior content lives
in `jj log` if anyone needs to recover it. This matches the
report-rename protocol — the file is the current truth, history
the path.

Supersession is **always explicit, and only the psyche can
supersede psyche intent.** A new psyche statement is the only
source that can override a prior psyche statement. An agent
encountering documented intent that seems wrong does NOT supersede
on its own authority; the agent asks the psyche
(`skills/intent-clarification.md`). The protection is load-bearing
against agent hallucination passing as psyche intent.

## Verification — does the entry still apply?

Periodically (when sweeping a topic, or when an entry's substance
crosses the agent's path), verify that the recorded entry still
matches workspace reality. Three failure modes:

- **The workspace evolved past the entry.** The psyche said "X is
  forbidden" in a context that no longer exists. If the constraint
  no longer applies, ask the psyche for explicit retirement —
  don't assume.
- **The recorded summary doesn't match the verbatim.** Agent
  rephrasing drift; the summary says one thing, the quote says
  another. Fix the summary to match the quote.
- **The certainty doesn't match the phrasing.** Re-read the quote
  against `skills/intent-log.md` §"Certainty vocabulary". Correct
  if mismatched.

Verification corrections that aren't superseding the psyche's
intent (just fixing the agent's transcription) can land directly —
they're discipline cleanup, not author overrides. Log the change
in the commit message
(`intent: corrected summary in <topic>.nota to match verbatim`).

## Sweep — when and how

Trigger a sweep when:

- A topic file grows substantially (soft threshold ~600 lines per
  `skills/intent-log.md`). Most sweeps don't need to fire that
  high; smaller sweeps run alongside `skills/context-maintenance.md`.
- An agent reviewing a topic notices an entry that no longer
  matches the workspace.
- Major redesigns (the kind that generate `v2` reports) — the
  redesign's premises likely supersede earlier intents and need
  explicit psyche confirmation.

How:

1. Read every entry in the topic file.
2. For each entry, check: does this still apply? Does the summary
   still match the verbatim? Does the certainty still match the
   phrasing?
3. For entries that no longer apply: ask the psyche.
4. For agent-transcription drift: correct directly.
5. For a genuine 600+-line file with two distinct sub-topics:
   carve a new topic file per `skills/intent-log.md` §"When to
   actually split", move the relevant entries, commit. The split
   itself is not author intent — it's housekeeping; git history
   holds the lineage.

## When to skip recording in the first place

Some psyche statements are too transient for the log (covered in
`skills/intent-log.md` §"When to record" — restated here for
maintenance context):

- "Let's try this and see" — pre-commitment exploration.
- "Maybe X, I'll think about it" — `Minimum`-certainty might be
  worth recording, but if the psyche then commits to something
  else within the same conversation, skip the intermediate.

If you skip recording a borderline case and the psyche later asks
"why isn't this in `intent/`?" — at that point, record it.

## Forward — persona-mind migration

When persona-mind's typed memory variants land, supersession
becomes a typed relation (`Supersedes` linking two
`Authorial<Kind>` memories); the workspace topic file retires in
favor of memory-graph queries. Until then, the topic file plus
`jj log` are the carrier.

## See also

- `skills/intent-log.md` — recording discipline; record shape;
  certainty vocabulary; topic granularity.
- `skills/context-maintenance.md` — workspace-wide sweep discipline;
  intent log is one of the things context-maintenance may sweep.
- `skills/nota-design.md` — positional-NOTA discipline these
  records follow.
- `intent/` — the surface this skill maintains.
