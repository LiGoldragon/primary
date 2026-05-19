# 234 — Concept designer: role definition + fleshing-out

*A workspace role that serves as the entry point for new concepts.
Captures the psyche's restoration of concept designer (which earlier
/224 incorrectly framed as a "mode") and seeds the fleshing-out
conversation. Companion to the broader workspace-redesign work in
/224, which retires alongside this report's landing.*

## 0 · TL;DR

**Concept designer is a real role.** Its scope: be the entry point
for new concepts the psyche is juggling. Compare new ideas against
the existing concept landscape, surface relationships, decide when a
concept earns its own dedicated design lane, and hand off when it
does.

The role is distinct from other designer lanes (`primary-designer`,
`persona-designer`, `system-designer`, etc.) which work *within*
established concepts. Concept designer sits *upstream* of those —
the role that decides when a new lane should exist.

## 1 · What the psyche has said

Psyche-stated in this session (intent in `intent/workspace.nota`)
and earlier (transcribed verbatim from the 2026-05-18 turn):

> "concept designer is, because I don't live in an ideal world. …
> I juggle so many new concepts that I kind of think it would make
> sense for me to just have this role called a concept designer.
> And I might keep it as a sort of entry point because he sort of
> keeps tally on like all these concepts that I'm juggling with.
> And he might actually say, well, you know what, there's this
> other concept over here that relates to it. And maybe we can move
> some of this here, move some of it out of it into this new
> concept. So there's a sort of, I think, a warranted role for like
> this really high level designer who's like the designer that
> precedes the actual concept becoming a full design lane of its
> own. So let's say I have like this new idea for … this concept X.
> And I come to the concept designer with it. I'm like, okay, here's
> this concept X. And then we like talk about it, compare it with
> the other concepts. And then he's like, okay, let's start the X
> designer lane. And then we start a new role."

> "There is a concept designer. It's actually a really important
> role. And I think I'm, yeah, I'm ready to move on to fleshing
> that out more."

## 2 · Settled scope

Three things the psyche has named that this role does:

1. **Concept tally.** Maintain awareness of every concept the psyche
   is currently juggling. Read across `intent/`, recent designer
   reports, ongoing work. Know what's in flight.
2. **Cross-concept relationships.** When a new concept arrives,
   identify which existing concepts it relates to. Move substance
   between concepts (e.g., "this idea fits better under X than
   under Y").
3. **Lane spawning judgment.** Decide when a concept has matured
   enough to warrant its own dedicated design lane. Hand off to a
   new (or existing) lane when ready.

## 3 · Open for fleshing out

### Q1 — Lane mechanics

The role needs a lane in the orchestrate sense (claim file, reports
subdir, beads label). Naming candidates:

- `concept-designer` — direct
- `concept` — broader
- `concept-architect` — emphasises the seeded-design aspect

How does this fit alongside `primary-designer`, `persona-designer`,
etc.? Concept designer is workspace-cross-cutting (any new concept
can land); the per-subsystem designers handle established work
inside their subsystem.

### Q2 — Concept inventory

The role needs a queryable view of every concept currently in
flight. Today that's scattered across `intent/`, reports, beads,
and the psyche's memory. Candidates for the inventory:

- A `concepts/` directory at workspace root, one file per concept
- A view derived from `intent/` (each concept = group of intent
  entries that share a semantic area)
- A persona-mind future surface (concepts as memory variants)

Today's lightest move: concepts derive from existing intent topics
(`intent/<topic>.nota` files); the concept designer reads these to
maintain tally. Heavyweight inventory waits for persona-mind.

### Q3 — Handoff protocol

When concept designer decides a concept earns its own lane:

1. Concept designer writes a kickoff report under
   `reports/concept-designer/<N>-<topic>-launch.md` that summarises
   what the new lane inherits.
2. The new lane gets a claim file (`orchestrate/<new-lane>.lock`)
   and a reports subdir (`reports/<new-lane>/`).
3. The first agent for the new lane reads the kickoff report and
   takes over.

Does the concept designer remain involved after handoff (advisory
role), or fully passes ownership? Probably the latter — clean
handoff per the workspace's "one owner per scope" discipline.

### Q4 — When the role retires a concept

A concept can also be *retired* (decided not to pursue, absorbed
into another concept, or completed). Concept designer needs a
mechanism for that — a `Constraint` or `Decision` recorded in
`intent/<topic>.nota` marking the concept as retired, plus any
report retirement that follows.

### Q5 — Workspace-redesign open questions inherited from /224

The broader workspace-redesign work in /224 included these still-
open questions that concept designer could be the right home for:

- Subsystem boundaries (are there 5 subsystems? Different cut?)
- Whether deployer is its own discipline distinct from operator
- Poet specialisation (single role vs Vedic/Greek/editor split)

These are themselves concepts being juggled. Concept designer
processes them as it builds its inventory.

## 4 · Predecessors

This report supersedes the concept-designer dismissal in:

- `reports/designer/224-workspace-redesign-first-concept-2026-05-18.md`
  §2 "Concept designer is a mode, not a role" — that recommendation
  was wrong; psyche corrected it during the 2026-05-18 pushback turn
  and confirmed in this turn. /224 retires alongside this report.

The still-open questions from /224 (workspace-redesign substance
beyond concept designer) are carried into this report as §3 Q5 and
into intent records on `intent/workspace.nota`.

## 5 · Next steps

The psyche is *ready to flesh this out more.* The next move is
psyche-led: pick which of Q1-Q5 to settle first. My lean — Q1 (lane
mechanics) first since it's needed to make the role operable, then
Q2 (concept inventory) since it shapes what the role does
day-to-day.

## See also

- `intent/workspace.nota` — psyche statements driving this report.
- `skills/role-lanes.md` — workspace lane mechanism the concept-
  designer lane will plug into.
- `skills/intent-log.md` — intent layer concept designer will read
  to maintain tally.
- `reports/designer/232-persona-spirit-new-component.md` — a
  parallel example of a workspace-meta role (spirit; cognitive
  apex) that emerged from psyche illumination.
