# Codex Handoff — Workspace Staleness / Deprecation Sweep

This document is self-contained. It hands the entire epic to an external agent
(Codex) with no dependence on the originating session. The beads in the tracker
are also self-contained; this document is the map over them.

## Epic intent

The psyche's workspace carries stale material that keeps getting re-surfaced as
if it were live. Examples the psyche named:

- "persona-mind" is a dead name — the thing is "mind" now.
- "horizon re-engineering" finished long ago but is still described as active.
- "router Wi-Fi" is a mystery item the psyche never raised.
- persona-engine-sandbox work was driven by agents without psyche tracking.

This noise leaks into every agent's context and manufactures confusion. The
epic's job: find where a NEW thing replaced / renamed / deprecated an OLD thing,
and REMOVE the lingering mentions of the dead thing so context stops carrying
ghosts.

This is enforcement of the standing replaceable-design rule (Spirit record
`10pz`): "Design replaceably, not additively: do not preserve an older shape for
backward-compatibility's sake when it manufactures legacy. If the current system
is not designed to do what we want, it is replaced — every consumer updated —
rather than extended with a parallel compatibility path."

## The evidence-anchored rule (binding on every sweep)

A candidate is reported ONLY if it names all four of:

1. THE NEW THING (what replaced/renamed/superseded the old).
2. THE OLD THING IT KILLED.
3. A LOCATOR (path, issue id, repo+symbol, line/section).
4. THE EVIDENCE — one of: a rename; a finished effort still described as
   active; an explicit deprecate/replace/supersede statement; or landed work
   that makes an older shape dead.

No hunches. A candidate missing any of the four does NOT go on the confirmed
track — it goes to SUSPECT.

This rule is the primary safeguard against the audit manufacturing the very
noise it is meant to remove. It is restated in every sweep bead's description.

## Surface scopes

In scope (three surfaces):

1. Tracker — beads issues/epics.
2. Skills & docs — skill source (skills-repo modules that generate runtime
   `.claude/skills/*`), `AGENTS.md` / `INTENT.md` / `ARCHITECTURE.md` / `README`
   files, and generated runtime surfaces. When a hit lands in a GENERATED
   surface, the SOURCE is edited and the runtime surface is reconciled — the
   generated file is never hand-edited.
3. Repos / code — tracked workspace code only.

Out of scope (hard boundaries):

- Spirit intent records — the intent layer is NOT swept.
- `private-repos/` is untouched. A sweep that seems to need that scope FLAGS it
  in its output and never enters it.

## The kill model

Deletion is UNGATED by the psyche. It is gated SOLELY by the verification bead
(`primary-5rzf.4`). No removal bead may act until the verifier has produced its
ledger.

The audit produces two clearly separated outputs, never mixed:

- CONFIRMED ledger — evidence-backed; the ONLY thing the kill beads may remove.
- SUSPECT list — plausible but unproven; surfaced to the psyche, NEVER
  auto-killed (there is no evidence to act on).

The verifier is adversarial: for each candidate it actively tries to REFUTE it
("is the old thing actually dead, or still live?") and DEFAULTS to "still live /
reject" when uncertain. It sorts every candidate into Confirmed / Suspect /
Rejected.

Suspect items are non-destructive: the suspect-ruling bead only surfaces them
for a psyche decision. It does not block the confirmed kills.

## Bead graph (IDs + dependency edges)

Epic: `primary-5rzf` — Workspace staleness/deprecation sweep.

Children:

- `primary-5rzf.1` — Phase 1 audit — Tracker sweep (finished-but-open,
  dead-name, superseded, mystery items; trace mystery-item ORIGIN).
- `primary-5rzf.2` — Phase 1 audit — Skills & docs sweep (replaced/renamed
  terms, guidance describing dead shapes; flag source-vs-generated).
- `primary-5rzf.3` — Phase 1 audit — Code sweep (deprecated APIs, old shapes,
  dead consumers; report repos covered; stop at private-repos boundary).
- `primary-5rzf.4` — Phase 1b — Adversarial verifier; produces the
  Confirmed / Suspect / Rejected ledger. THE ONLY GATE before deletion.
- `primary-5rzf.5` — Phase 2 kill — Tracker (close/delete CONFIRMED stale
  issues only).
- `primary-5rzf.6` — Phase 2 kill — Docs+Skills (delete CONFIRMED dead-name
  mentions, reconcile generated surfaces).
- `primary-5rzf.7` — Phase 2 kill — Code (delete CONFIRMED dead code paths,
  update consumers).
- `primary-5rzf.8` — Phase 2 — Suspect-ruling (surface Suspect list to psyche;
  non-destructive; does NOT block the kills).
- `primary-5rzf.9` — Closeout (verify ghosts gone, builds/checks green, commit
  + push on main via jj).

Dependency edges (blocker -> blocked):

```text
.1 ─┐
.2 ─┼─> .4  (verifier: blocked by all three sweeps)
.3 ─┘

.4 ─> .5   (tracker kill)
.4 ─> .6   (docs+skills kill)
.4 ─> .7   (code kill)
.4 ─> .8   (suspect-ruling; non-blocking for kills/closeout)

.5 ─┐
.6 ─┼─> .9 (closeout: blocked by the three kills; NOT by .8)
.7 ─┘
```

Phase 1 (`.1 .2 .3`) runs in parallel — no deps among them. The verifier
(`.4`) is the single convergence/gate. The three kills (`.5 .6 .7`) run in
parallel after the gate. The suspect-ruling (`.8`) runs after the gate in
parallel with the kills and blocks nothing downstream. Closeout (`.9`) waits on
the three kills only.

## Per-bead outputs (durable pickup surfaces)

All under `agent-outputs/WorkspaceStalenessSweep/`:

- `.1` -> `TrackerSweep-Candidates.md` (Candidates + Suspects; mystery-item
  origin traces).
- `.2` -> `DocsSkillsSweep-Candidates.md` (Candidates + Suspects; each hit
  flagged source-vs-generated).
- `.3` -> `CodeSweep-Candidates.md` (Repos covered; Candidates + Suspects;
  private-repos boundary flags).
- `.4` -> `Verifier-Ledger.md` (Confirmed / Suspect / Rejected — the SOLE
  authority for what the kills may remove).
- `.5` -> `KillTracker-Evidence.md`.
- `.6` -> `KillDocsSkills-Evidence.md`.
- `.7` -> `KillCode-Evidence.md`.
- `.8` -> `SuspectRuling-ForPsyche.md`.
- `.9` -> `Closeout-Evidence.md`.

## Version-control discipline (for the kill + closeout beads)

On primary, work on `main` with `jj`: `jj commit -m '<message>'` (inline
message — never open an editor), `jj bookmark set main -r @-`, and at closeout
`jj git push --bookmark main`. Commit the whole working copy. For skill edits,
edit the source modules and reconcile the generated runtime surfaces. For other
repos, follow that repo's VC discipline; if another agent owns a checkout, work
from `main` in an isolated worktree and claim shared paths before editing.

## Where the rule lives

The standing replaceable-design directive this epic enforces is Spirit record
`10pz`. Its full prose and the manifestation context are recorded at
`agent-outputs/ReplaceableDesignIntent/IntentMaintainer-ReplaceableDesignRecord.md`.
