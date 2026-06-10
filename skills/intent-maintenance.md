# Skill — intent maintenance

*Sweep the Spirit intent log: detect supersession, verify entries still
apply, remove safely. Keeps the intent substrate from rotting as the
workspace and the psyche's positions evolve. Companion to
`skills/intent-log.md` (recording).*

## Supersession is always explicit — only the psyche supersedes

A new psyche statement is the only thing that can override a prior psyche
statement. An agent encountering documented intent that seems wrong does
NOT supersede on its own authority — it asks the psyche
(`skills/intent-clarification.md`). This protection is load-bearing
against agent hallucination passing as psyche intent.

When a new psyche statement contradicts a prior recorded entry:

1. **Surface the contradiction inline, before recording.** Quote the
   prior verbatim and its certainty:

   > *"You said earlier (Spirit topic `<topic>`):*
   > *— `<prior verbatim quote>` — certainty `<prior certainty>`, record `<prior identifier>`*
   >
   > *Now you're saying `<new summary>`. Override the prior, or am I misreading?"*

2. **Wait for confirmation.** Three outcomes:

   | Psyche says | Action |
   |---|---|
   | "Yes, override" | Record the new entry; mark the prior superseded (step 3) |
   | "No — the prior still applies, this refines it" | Add the new entry as `Clarification`; prior stays |
   | "Both apply in different contexts" | Add the new entry; prior stays |

3. **On confirmed override:** record the new Spirit entry and name the
   supersession in the commit message
   (`intent: <topic> — psyche overrides prior <slug>; new <slug>`). Spirit
   is the sole substrate. Until typed supersession tooling exists, the
   active/superseded distinction is carried by the newer explicit psyche
   correction; never silently rewrite a prior record.

## Negation shape

Negation is supersession where the psyche says a prior record is
*invalid*, not merely refined. Spirit has no typed `Negates`/`Supersedes`
relation yet, so:

1. Look the prior record up by its identifier (`spirit "(Lookup [abcd])"`).
2. Ask the psyche to confirm the old record is negated.
3. Record a new `Correction` or `Decision` naming the old identifier and
   stating the replacement truth, e.g. `Spirit record [abcd] is negated;
   the correct intent is ...`. Do not delete the old record — lineage
   stays visible.

## Removing a record — tombstone first

Spirit supports psyche-authorized removal: `spirit "(Remove [abcd])"`
(the argument is the record's base36 identifier code, not a number).
Use it only for records that should **not remain at all** — mis-logged
working orders, or fully-stale records whose substance is rehomed. When
lineage should stay visible, supersede with a `Correction` and keep the
record.

Removal is **destructive and irreversible.** The record's key is
retracted from the sema-engine store and there is no undelete.

So **capture before you remove.** Before any `(Remove [abcd])`, look the
record up by its identifier and record the full text into the removing
agent's report:

```sh
spirit "(Lookup [abcd])"
```

Paste the resulting `RecordFound` entry into a tombstone appendix; the
report then IS the record of what was removed. An undocumented removal
once proved unrecoverable, while a tombstoned-first removal preserved
full text — capture first, then remove.

Stay conservative: when removability is uncertain, flag rather than
remove — over-removal is worse than under-removal. Lowering a record's
certainty to `Zero` marks it a removal candidate. `CollectRemovalCandidates`
archives exact-`Zero` candidates as compact summaries before retraction;
archive failure leaves records in the store. Use collection for reviewed
batches; use hard single-record `Remove` only after the tombstone is
captured.

## Verification — does the entry still apply?

Periodically — when sweeping a topic, or when an entry's substance
crosses your path — verify the recorded entry still matches reality.
Failure modes:

- **The workspace evolved past the entry.** A constraint set in a context
  that no longer exists. Ask the psyche for explicit retirement; don't
  assume.
- **The summary doesn't match the verbatim.** Agent rephrasing drift. Fix
  the summary to match the quote.
- **The certainty doesn't match the phrasing.** Re-read against
  `skills/intent-log.md` §"Certainty vocabulary"; correct if mismatched.
- **One record bundles claims of different certainty.** A record can carry
  a settled rule and a tentative design under one high-certainty summary.
  Split it: preserve the settled part at its earned certainty, record the
  tentative part at its lower certainty. Matters most when the psyche
  explicitly flags a clarification as low-certainty.

Corrections that fix the agent's transcription (not override psyche
intent) land directly — they're discipline cleanup, not author overrides.
Log them: `intent: corrected Spirit summary in <topic> to match verbatim`.

## Sweep — when and how

Trigger a sweep when:

- A Spirit topic grows large or query results become noisy. Small sweeps
  ride alongside `skills/context-maintenance.md`.
- An agent notices an entry that no longer matches the workspace.
- A major redesign lands — its premises likely supersede earlier intents
  and need explicit psyche confirmation.
- A context-maintenance pass finds older intent clearly contradicted by
  newer stronger intent. Such an agent may audit even old intent and
  **recommend** removal or supersession — but deletion stays reviewable
  and justified by the newer intent. Propose; do not execute unilaterally.
  The orchestrator or psyche authorizes removal after the contradiction is
  explicitly named.

How:

1. Read every Spirit entry in the topic.
2. For each: does it still apply? Summary match the verbatim? Certainty
   match the phrasing? Does one summary bundle sub-claims of differing
   certainty?
3. Entries that no longer apply: ask the psyche.
4. Transcription drift: correct directly.
5. A genuinely noisy topic with two distinct sub-topics: carve a new
   Spirit topic per `skills/intent-log.md` §"When to actually split". The
   split is housekeeping, not author intent; history holds the lineage.

## When to skip recording in the first place

Some statements are too transient to log:

- "Let's try this and see" — pre-commitment exploration.
- "Maybe X, I'll think about it" — a `Minimum`-certainty note may be worth
  recording, but if the psyche commits to something else within the same
  conversation, skip the intermediate.

If you skip a borderline case and the psyche later asks "why isn't this in
Spirit?" — record it then.

## See also

- `skills/intent-log.md` — recording discipline; record shape; certainty
  vocabulary; topic granularity.
- `skills/context-maintenance.md` — workspace-wide sweep discipline.
