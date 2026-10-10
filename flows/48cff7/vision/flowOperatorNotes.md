# flowOperatorNotes

## 2026-09-16 — a flow role has an operator's notes skill it can edit itself, more liberally than a standing skill

Context: after the accumulated-proposal document landed, the living opened a new idea.

> Oh, I just had a brilliant idea. There is a skill, the Flow, that is named after it and can more liberally edit when it learns a way of doing something, like operational notes. It's like an operator's note skill. You have the psyche's operators' notes skill. He can say, "Oh, I have a suggestion for basically anything that he needs to know to operate better. He should just edit it." I don't know exactly how that's going to work, but that's the idea. That's the vision. Let's see how we would do that.

-- psyche, typed.

## Flow reading

Each flow role has an *operator's notes* skill named after itself — a loose, editable-by-the-flow scratchpad of how-to-operate. Unlike the standing skills composed under skill-designing's brutal minimalism, the operator's notes accepts verbose, tentative, iteratively-refined tips. When a session in that role learns a way of doing something better, it edits its own notes so the next session starts with the discovery.

## Proposed shape

A per-role skill file `<flow-role>-notes.md`, or `<role>-<tier>-notes.md` when the tip differs by effort tier. Examples:

- `psyche-notes.md` — for any psyche flow.
- `psyche-medium-notes.md` — specific to MEDIUM tier when the tip is tier-specific.
- `visualization-notes.md` — for visualization subflows.
- `implementation-notes.md` — for implementation subflows.

Content is free-form. Sections by topic. Entries dated. Each entry names what was learned and how it applies. A seed demonstration lives at `flows/48cff7/notes/psyche-medium-notes.md`.

The flow reads its notes file at session start (as part of its role skill's dependencies) and adds to it during the session. Every edit is committed to the flow branch with a short line naming what was learned.

## Kind and place in the taxonomy

Operator's notes fit awkwardly against the source kinds named in `flows/48cff7/vision/skillSourceKinds.md`:

- Not *vision-derived* — they are not designed; they are discovered.
- Not *mind-derived* — they are operational habits, not verified world-facts.
- Not quite *usage* — usage teaches a tool's language; notes teach a role's practice.

Proposal: a fourth source kind, **Notes**, whose content is editable by the flow itself. Alternatively, a subtype marker under Usage.

Editing rules for the Notes kind are looser than skill-designing:

- Verbose is acceptable when brevity would lose signal.
- Tentative wording is acceptable; iteration is expected.
- The flow may add, edit, or reorganize its own notes; it may not edit another role's notes.
- Every edit still commits with a short line naming the incident or the choice being recorded.

## Consequences

- **Accumulation across sessions.** A successor psyche-main-flow session loads the same `psyche-notes.md` and inherits every prior discovery. Refresh becomes cheaper — the successor does not re-learn what the predecessor already learned.
- **Drift risk.** Free-form editing can accumulate stale or contradicting notes. A periodic pruning pass by a psyche flow keeps the file current.
- **Ownership boundary.** A flow edits only its own role's notes. Cross-role suggestions become vision proposals for the other role's operator to consider.
- **Promotion path.** A note that hardens into a standing rule promotes upward — from notes to a vision entry, from vision to a skill body — per the pipeline in `flows/48cff7/vision/highPowerAndUpgradePipeline.md`.

## Open questions worth the living's word

1. Confirm the file-per-role shape, or prefer file-per-role-per-tier, or file-per-role-per-stack.
2. Whether Notes is a fourth source kind or a subtype of Usage.
3. Whether a flow may add a note that references or contradicts a standing Vision — if so, does that trigger a promotion path?
4. Where the file lives — Curriculum authored surface (alongside other skills), or a separate `notes/` tree beside it.
5. Which flow performs the periodic pruning pass, and how often.
