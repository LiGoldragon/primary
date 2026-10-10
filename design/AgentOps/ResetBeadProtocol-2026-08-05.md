# Reset Bead Protocol — 2026-08-05

Psyche-directed protocol for session resets: context handover carried
by beads. Beads are the current vehicle ("eventually we're going to
use something better than beads. It's just what we have now... it
doesn't pollute the file system so much"). A more humanistic name for
the act (head clearing, rest, nervous-system reset) was floated and is
not settled.

## Protocol

- A reset bead is targeted at a specific agent and model (e.g. the
  Fable 5 main assistant agent). A session loading a reset bead first
  verifies it is the right model; a wrong model refuses: "I'm not the
  right model for this reset bead. You gave it to the wrong person."
- The bead carries: the writing session's ID (so lineage can be walked
  back session to session), the primordial skills to load, pointers to
  the authoritative state, and the open threads.
- Primordial skills (for the Fable assistant: management,
  psyche-interraction, and the Spirit skill once it exists) are valid
  for the entire session, not a single turn. This must be stated
  explicitly because some harness startup prompts (codex) wrongly
  claim skills last one turn. Primordial skills are passed forward
  into every future reset bead the session writes, unless the psyche
  explicitly demotes them.
- The psyche starts the new session by passing the bead ID as the only
  prompt. The new session loads the bead, verifies model, loads the
  primordial skills, closes the bead (the reset is thereby complete),
  and continues the work.
- The resetting session's final response is the bead ID only.

## Open items

- A primordial-skills skill in the skills repository, with per-harness
  emission (the codex variant, at least, stating session-long
  validity — stating it for all harnesses is fine), was approved in
  principle ("let's do that"); its content awaits drafting and psyche
  approval before landing.
- A very minimal AGENTS.md, with non-universal doctrine moved to a
  file read only by the roles that need it, was floated and not
  executed.
- Reset-point guideline: around 20% of a million tokens of context,
  degradation begins; reset around there.
