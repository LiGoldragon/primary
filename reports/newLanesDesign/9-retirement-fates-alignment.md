# 9 — Lane-retirement fates: alignment

Reopening the lane model on one point the psyche flagged: **a drained
lane should not be automatically deleted.** Deletion stays available, but
as one option among several, not the mandatory single outcome.

This is an alignment thread (not yet a settled design). It does not
supersede report 8 (closeout); it adds the retirement-fate dimension that
8 left as a binary (keep-active vs. delete).

## What we are refining

| Surface | What it currently says |
|---|---|
| Spirit **6utp** (Decision, High) | *[When a session lane drains its report directory is deleted because git history and the session transcript hold the substance; a single append-only registry at protocols/retired-lanes.md records each retired lane... The thin index keeps drained sessions discoverable... without regrowing the working report tree.]* |
| `skills/session-lanes.md` §"Lane retirement" | Three mechanical steps: delete the report dir, append a `retired-lanes.md` row, `meta-orchestrate "(Retire (Lane …))"`. |
| `protocols/retired-lanes.md` | Bills itself as *"the discoverable middle path between 'delete everything' and 'keep every report forever'."* |
| `AGENTS.md` (drain paragraph + lane table) | "When the lane drains, delete its `reports/<lane>/` directory — git history and the session transcript are the archive." |

So today the model already has exactly **one** archival path (delete +
thin index). The psyche wants that widened into a **menu**.

## Reading check (the highest-risk fork)

"Don't automatically delete lanes" has two possible meanings, and they
build differently:

- **(A) Don't auto-destroy the report substance.** The lane identity
  still retires (it is throwaway, disciplines are the persistent
  identity), but the *report directory* gets a menu of fates instead of
  forced deletion. — **my read.**
- **(B) Don't auto-retire the lane identity itself.** Some lanes persist
  across sessions as standing identities.

I am proceeding on **(A)**: it preserves the just-landed
discipline-is-permanent / lane-is-throwaway split, and the last agent's
concrete suggestion that triggered the pushback was specifically *delete
`reports/newLanesDesign/`*. If the psyche means (B), the rest of this
report is the wrong tree.

## Proposed menu of retirement fates (the report directory)

1. **Delete** (today's behavior) — raw reports removed; git history, the
   session transcript, and the thin `retired-lanes.md` row are the
   archive. Right when the reports were *scaffolding* and every bit of
   substance already landed elsewhere (intent → Spirit, work → beads,
   docs updated).
2. **Distill-then-delete (promote)** — before deleting, the lane's
   reusable substance is synthesized into a durable canonical home (a
   `skills/` file, `ARCHITECTURE.md`, a per-repo `INTENT.md`,
   `ESSENCE`/`INTENT`, or a Spirit record), then the raw reports are
   deleted. The *essence* survives in the right surface; only the
   scaffolding goes. This is the fate that fixes the actual loss: today
   the atomic ideas route to intent/work/abandon, but the report-level
   synthesis (the walk-through, the diagram, the argued reasoning) dies
   with the directory.
3. **Preserve as standing reference** — a curated report (or the whole
   dir) is kept as durable reference future agents will read in full,
   moved or marked so it is not mistaken for an active lane. Some design
   syntheses are reference material, not scaffolding.

Plus the not-a-fate case: **keep open** — the lane simply is not drained
yet (this is where `newLanesDesign` sits right now).

## The decision procedure — who picks

- **(a) Agent autonomous by rubric** — fast, but it is exactly the
  "automatic" the psyche just pushed back on.
- **(b) Psyche confirms every retirement** — safest, mirrors the coming
  auditor discipline (*"the psyche confirms each source-record
  retirement"*), but adds a gate to every drain.
- **(c) Hybrid (recommended)** — the agent always *proposes* a fate with
  one-line reasoning at drain (never silent); the psyche can override;
  **deletion specifically** is the one fate that may warrant explicit
  psyche confirmation, since it is the only irreversible-in-spirit choice.

## Surfaces that change once settled

- **6utp** — edit (`Clarify` if the core identity holds, `Supersede` if
  the shape changes enough) from "is deleted" to "routes to one of
  {delete, distill, preserve}, agent proposes, psyche may gate deletion."
- `skills/session-lanes.md` §"Lane retirement" — replace the 3-step
  delete with the fate-menu + procedure.
- `protocols/retired-lanes.md` — a preserved/distilled lane still earns a
  row, but the row gains a **fate** column and a pointer to *where the
  substance went* (the skill/doc it was promoted into).
- `AGENTS.md` — the drain paragraph and the `reports/<lane>/` table row
  both name deletion as the outcome; both move to the menu.
- `ESSENCE.md` / `INTENT.md` — only if the archival philosophy is
  essence-level (likely a light touch, not a new section).

## Live test case

`newLanesDesign` itself is the dogfood: it is plausibly a
**preserve-as-reference** or **distill** lane (a meta-design future
agents will want to read), which is precisely why the last agent's
instinct to *delete* it read as wrong. Settling the menu lets us route
this lane correctly instead of by the one default that exists today.

## Open alignment questions (in order)

1. Reading **(A)** vs **(B)** above — confirmed as (A)?
2. **What is the default fate** when the agent has no strong reason
   otherwise? (recommend: distill-then-delete is default; bare delete is
   the opt-in for pure scaffolding; preserve is the explicit choice.)
3. **Who decides + does delete need psyche confirmation?** (recommend:
   hybrid (c).)

## Spirit-gate decision for this turn

**No capture yet.** The psyche opened a design conversation ("I want to do
an intent-alignment"), and the constructive shape (menu, default, gate) is
not settled — capturing a half-formed policy would corrupt 6utp. Once the
menu and default settle, do **one** clean edit to 6utp (and manifest into
the surfaces above). The directional signal lives in this report until
then.
