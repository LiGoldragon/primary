---
title: 3 — orchestrate/AGENTS.md cutover to dynamic session lanes
role: newLanesDesign
variant: Design
date: 2026-06-24
topics: [lanes, sessions, orchestrate, claim-flow, reports, discipline]
description: |
  Slice 3 of the newLanesDesign fleet. Cuts orchestrate/AGENTS.md from the
  fixed-role-lane model to the dynamic session-lane model: disciplines as
  persistent metadata, lanes as per-session intent-named identities registered
  through the daemon's Register/Observe/Retire NOTA surface, claim flow naming
  the session lane, and reports as session directories that drain and retire.
  Lock-file, claim/release, and version-control mechanics left intact.
---

# 3 — orchestrate/AGENTS.md cutover to dynamic session lanes

## What changed

Only the **lane-naming model** in `/home/li/primary/orchestrate/AGENTS.md`.
The lock-file format, claim/release mechanics, task-lock semantics,
component-migration discipline, version-control rules, and overrides are
untouched in substance — only their role-name placeholders moved from a fixed
enumeration to "the registered session lane."

### Roles section → Disciplines and lanes (slice a + b)

The "## Roles" heading became "## Disciplines and lanes." The large fixed-lane
table (`operator` / `second-operator` / `cluster-operator` / `schema-designer`
/ … with lock-file, reports-subdir, default-agent, scope columns) is deleted.
In its place:

- The **nine disciplines** as a list — designer, operator, system-operator,
  system-maintainer, poet, editor, videographer, assistant, counselor — defined
  as persistent metadata (skills + authority class + persona identity:
  persona-mind memory and signing key). A discipline is explicitly "not a
  directory and not a session."
- A **lane** is a per-session intent-named identity (`newLanesDesign`,
  `schemaWorkAudit`) carrying its discipline as the **last token of its NOTA
  role vector** (`[NewLanesDesign Designer]`), per Spirit `irmw`.
- The old fixed role-lanes and ordinal/qualifier shapes are stated as retired
  *as the lane model*; the disciplines survive.
- A new "Registering and observing lanes" subsection shows the daemon surface
  with the exact NOTA, pointing at `skills/session-lanes.md` as canonical.

### Daemon Register/Observe/Retire surface (exact NOTA)

Read from `/git/github.com/LiGoldragon/orchestrate/schema/orchestrate-v0-1.schema`
and `orchestrate-types-v0-1.schema`, cross-checked against `src/lane.rs`:

- `Register [LaneRegistrationRequest]`, where
  `LaneRegistrationRequest (Role LaneAuthority)`, `Role ((Vec RoleToken))`,
  `LaneAuthority [Structural Support]` → reply `LaneRegistered (LaneRegistration)`.
- `Observe Lanes` → `LanesObserved ((Vec LaneRegistration))`, where
  `LaneRegistration (LaneIdentifier Role LaneAuthority)`.
- `Retire [Retirement]`, where
  `Retirement [(Role RetireRoleOrder) (Lane LaneIdentifier)]` →
  `LaneRetired (LaneIdentifier)`.

Example calls written into the doc:

```sh
orchestrate "(Register ([NewLanesDesign Designer] Structural))"
orchestrate "(Observe Lanes)"
orchestrate "(Retire (Lane newLanesDesign))"
```

### Claim flow (slice c)

`(Claim (<lane> ...))` now takes the **registered session lane** as the actor
token, discipline-tagged in the registry by the last token of its role vector.
The flat 22-name `<role>` enumeration is replaced by a pointer to
`orchestrate "(Observe Lanes)"` plus the explicit note that the claim names
*who is acting* (the lane) while the scope names *what* (paths/tasks) — scope
mechanism unchanged. Worked examples (`system-operator`, `system-maintainer`)
re-tagged to session-lane names (`schemaWorkAudit`, `newLanesDesign`). The
`Release <role>` / `Observe Roles` / lock-projection examples follow suit;
`Observe Lanes` is now listed first under Status with its return shape.

### Reports section (slice d)

Rewritten from the per-role permanent-subdirectory convention to:

- `reports/<lane>/` **session directories**, one per active lane, per-lane
  numbering; the old 24-entry `reports/<role>/` bullet list is deleted.
- Reports as **fresh-context pickup points**, implementable work linked into a
  bead dependency graph (`bd dep <blocker> --blocks <blocked>`).
- Claim-exempt because session directories don't overlap (the session dir is
  the implied lock).
- A new "Drain and retire" subsection: the three-fate disposition
  (intent / work / abandon), delete the drained session directory, record one
  append-only entry in `protocols/retired-lanes.md`, and
  `orchestrate "(Retire (Lane <lane>))"`. `LanesObserved` indexes active lanes;
  `protocols/retired-lanes.md` indexes retired ones.

The mind-graph routing paragraph was corrected to route by **discipline**
(persistent persona-mind) rather than "main role," and the two `reports/<role>/`
references in the upper "Exempt from the claim flow" subsection were updated to
`reports/<lane>/`.

## Cross-references created

This slice introduces forward references to two files owned by sibling slices,
already present in `skills/skills.nota` (line 106) and `AGENTS.md` (lines 18,
40):

- `skills/session-lanes.md` — cited as canonical for the lane mechanism and
  full lane lifecycle.
- `protocols/retired-lanes.md` — cited as the append-only retired-lane index.

If either sibling slice renames its file, the two citations in
`orchestrate/AGENTS.md` (in "Disciplines and lanes" and in "Drain and retire")
must track the rename.

## Left intentionally intact

Lock-file format and the two scope kinds, the daemon's five-step claim
processing, task-lock bridging to BEADS lifecycle, release push-bookmark
safety check, worktree verification, blocked-work / persona-mind targeting, the
legacy-BEADS notes, "beads are not role-labeled," version-control, and
overrides. Per the OUT-OF-SCOPE constraint, no Rust touched and no
ESSENCE/INTENT deprecation drift addressed here.

## Open question

The `roles.list` file at `orchestrate/roles.list` still enumerates the fixed
roles and is read by something at daemon startup (it predates this cutover).
This slice did not touch it (out of assigned file scope, and it is daemon
infrastructure). Whether the daemon still needs a seed `roles.list` under the
dynamic-lane model, or whether it should be retired, is an
operator/schema-operator question for a follow-up bead — flagging it so the
synthesis can route it.
