---
title: 7 — skill index + role-skill lane-reference sweep
role: newLanesDesign
variant: Design
date: 2026-06-24
topics: [lanes, sessions, skills, skills.nota, cross-references]
description: |
  Cut the skills.nota lane-mechanism index entry from role-lanes to
  session-lanes, and swept the nine discipline skills for references to
  role-lanes.md and the fixed-lane model, reframing them onto the
  session-lane model. Minimal edits — only lane references touched.
---

# 7 — skill index + role-skill lane-reference sweep

## What changed

### skills.nota — the lane-mechanism index entry

The `(Workflow role-lanes …)` record became `(Workflow session-lanes …)`.
NOTA positional fields: Kind `Workflow`, name `session-lanes`, path
`skills/session-lanes.md`, Tier `Mechanism` (unchanged), Description.
The description was rewritten as purpose + trigger in two sentences,
positive framing:

```
[How a lane is a fresh work-session identity named for its intent,
carrying a discipline as metadata that loads its skills and authority.
Read when opening, registering, naming, or draining a session lane.]
```

The sibling slice owns creating `skills/session-lanes.md` and retiring
`skills/role-lanes.md`; this slice only repoints the index entry and the
role-skill cross-references at the new path.

### Role-skill sweep — four files carried lane references

The grep across all nine discipline skills surfaced four with
`role-lanes.md` links or fixed-lane phrasing. Edits were kept minimal —
only lane references reframed, no surrounding rewrite:

- `skills/designer.md` — required-reading baseline repointed to
  `skills/session-lanes.md`; the "Working with designer's lanes" section
  retitled to "Working with parallel designer-discipline lanes" and its
  opener reframed (a session lane carries the designer discipline as
  metadata; several can run at once).
- `skills/operator.md` — required-reading baseline, the role-contracts
  note, the "Working with additional operator lanes" section header +
  opener, and the See-also entry all repointed and reframed off the
  fixed `second-operator`/`pi-operator`/`cluster-operator`/`cloud-operator`
  pool onto session lanes carrying the operator discipline.
- `skills/system-operator.md` — the "Lanes" section opener (off
  `second-system-operator`) and the See-also entry repointed; the
  `system-designer` cross-reference reframed as a lane carrying the
  designer discipline for system architecture.
- `skills/poet.md` — the "Lanes" section opener reframed off
  `second-poet`/`third-poet` onto session lanes carrying the poet
  discipline; See-also link repointed.

## Files with no lane references (no edit)

`skills/system-maintainer.md`, `skills/editor.md`, `skills/assistant.md`,
and `skills/counselor.md` contained no `role-lanes.md` link or fixed-lane
phrasing — confirmed by grep, left untouched.

## Open items for the orchestrator

- `skills/videographer.md` does not exist, though videographer is one of
  the nine disciplines listed in `AGENTS.md`. The slice could not sweep a
  file that is absent. If a videographer skill is expected, that is a
  separate gap (route to a bead or to the discipline owner); it is not in
  scope for this lane-reference sweep.
- The four reframed sections (designer/operator/system-operator/poet)
  still phrase parallel-lane capacity in terms inherited from the
  fixed-lane era ("additional lanes", "additional capacity"). The
  openers now anchor on the session-lane model; deeper rewrites of those
  section bodies were deliberately not done to stay within the minimal
  edit instruction. If the orchestrator wants the section bodies fully
  re-voiced, that is a follow-up.
- This slice depends on the sibling slice landing `skills/session-lanes.md`
  at the cited path. Until that file exists the index entry and the four
  cross-references point at a not-yet-created file.
