# Intent Logging Skill Review

## Direct Answer

At the time of the failed attempted capture, I had the `AGENTS.md` Spirit-gate
rule in context. I had not loaded `skills/intent-log.md` before trying to
record the user's tentative design thought. I loaded `skills/intent-log.md`
only after the failed `spirit` call exposed that I also had the wrong current
wire shape.

So the immediate failure was mine in two ways:

- I misclassified tentative exploratory wording as recordable intent.
- I did not load the detailed intent-log skill before acting on the intent
  surface.

## What The Skill Already Says Correctly

`skills/intent-log.md` is clear on the point that failed:

- Only explicit psyche statements are recorded.
- Before any write, the agent must ask whether the statement is exact psyche
  intent, durable after the task is erased, one of the five kinds, and privacy
  clear.
- "No capture" explicitly includes brainstorming without a settled want.
- The certainty ladder explicitly puts phrases like "we could," "maybe," and
  "I think" at `Low` / `VeryLow`, not as high-confidence direction.
- It says over-extension corrupts the load-bearing intent layer.

Your phrasing was exploratory: "I think since..." and "I feel like that same
schema could be used..." That should have been handled as design discussion,
not capture. If I thought it might be durable, the correct action was ask,
not record.

## Skill-Loading Failure

The workspace has two overlapping mechanisms:

- `AGENTS.md` says run the Spirit gate on every psyche prompt.
- `skills/skills.nota` lists `intent-log` as the topic skill and
  `human-interaction` as an Apex skill whose description says it is must-read
  for every harness.

In practice I followed the compact `AGENTS.md` gate rule and did not load the
specialized skill before touching Spirit. That is exactly the failure mode
skill-loading is supposed to prevent: a compact rule got applied without the
detailed calibration that prevents overcapture.

The current reading path also has a small guidance gap: `human-interaction` is
listed in `skills/skills.nota` as Apex / must-read, but the required-reading
sequence in `AGENTS.md` does not explicitly say to open all Apex skills from
the index. It says to query the index when a topic comes up. That still makes
my behavior wrong once I chose to log intent, because the intent-logging topic
had clearly come up. But it explains why the skill was not already in context
from session start.

## Stale Record-Shape Problem

The skill is also stale against deployed Spirit:

- `spirit Version` returned `(VersionReported (0.9.3 ...))`.
- `skills/spirit-cli.md` still says the active production binary is `0.8.1`.
- `skills/intent-log.md` and `skills/spirit-cli.md` describe `Record` as
  carrying a seven-field `Entry` directly.
- The live daemon rejected that shape with:
  `expected RecordRequest to hold 2 root objects, found 1`.
- Current `spirit/schema/signal.schema` says:
  `RecordRequest { Entry * Justification * }`.

That stale documentation did not cause the overcapture mistake, because the
record should not have been attempted at all. But it did make the attempt
fail noisily and confirms the capture docs need immediate refresh.

## Recommended Fixes

1. Add a hard local rule to `skills/intent-log.md`: before invoking
   `spirit "(Record ...)"`, the agent must have loaded `skills/intent-log.md`
   and `skills/spirit-cli.md` in the current session.
2. Update `skills/spirit-cli.md` and `skills/intent-log.md` to the current
   `0.9.3` record shape: `Record` carries `RecordRequest`, which carries
   `Entry` plus `Justification`.
3. Clarify the skill-loading path: either `AGENTS.md` or `skills/operator.md`
   should explicitly load `skills/human-interaction.md` every session, because
   it is marked Apex and says it is must-read for every harness.
4. Add an explicit examples block: exploratory wording such as "I feel like,"
   "could," "maybe," and "what if" is no-capture unless the psyche asks to
   make it policy or record it.
5. Treat failed capture attempts as incidents when the failure was
   classification, not syntax. A syntax failure that prevented a bad capture
   still means the gate failed upstream.

## Bottom Line

The intent-log skill would have prevented this if I had loaded it before
acting. The skill itself needs a record-shape update for current Spirit, but
the classification error was not caused by the stale shape. It was caused by
not applying the specialized skill at the moment I moved from discussion to
Spirit capture.
