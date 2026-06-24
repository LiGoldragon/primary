---
title: 1 — the session-lanes skill (discipline-vs-lane mechanism)
role: newLanesDesign
variant: Design
date: 2026-06-24
topics: [lanes, sessions, disciplines, orchestrate, registration, retirement]
description: |
  Slice 1 of the newLanesDesign cutover. Created skills/session-lanes.md as the
  canonical teaching of the discipline-vs-session-lane model (cutover decisions
  1-6), replacing the retired skills/role-lanes.md. Found and verified the exact
  lane-registration NOTA shape against the orchestrate schemas, and dogfooded it
  by registering this session's lane with the daemon. Flags two dangling
  role-lanes references owned by other slices.
---

# 1 — the session-lanes skill

## What landed

- **Created `skills/session-lanes.md`** — the canonical teaching of the
  new model. Covers: discipline (persistent: skills, authority,
  persona-mind, signing key) versus lane (a throwaway session named for
  its intent); how an agent knows its lane (the session-intent name the
  harness/psyche gives, also the report dir and registry lane, with the
  role vector's last token being the discipline); the worked
  registration command; reports mapping to `reports/<lane>/` as
  fresh-context pickup points with bead-graph links; the session
  lifecycle (smart zone -> fleet -> drain to intent/work/abandon); and
  lane retirement (delete report dir -> append to
  `protocols/retired-lanes.md` -> retire in the daemon).
- **Deleted `skills/role-lanes.md`** — the mirror-model / ordinal-lane
  skill it replaces.

## The exact registration shape (verified against the schemas)

The slice prompt's `orchestrate "(Register ...)"` is corrected in one
important way: `Register` is a **meta-policy** operation on the
owner-only root, so it goes through the sibling **`meta-orchestrate`**
CLI on the owner socket, not the working `orchestrate` CLI. The working
CLI's `Input` (`signal-orchestrate`) has no `Register` arm; the meta CLI
(`meta-signal-orchestrate`) does. This is enforced in the two binaries
(`src/bin/orchestrate.rs`, `src/bin/meta_orchestrate.rs`).

From `meta-signal-orchestrate/schema/lib.schema` and
`orchestrate-types-v0-1.schema`:

- meta `Input` arm: `(Register LaneRegistrationRequest)`
- `LaneRegistrationRequest { Role authority.LaneAuthority }`
- `Role ((Vec RoleToken))` — a Vec, so it renders as a **square-bracket**
  NOTA block, not parens; last token is the discipline.
- `LaneAuthority [Structural Support]`

Worked command:

```sh
meta-orchestrate "(Register ([NewLanesDesign Designer] Structural))"
```

## Dogfood — registration succeeded

Ran the worked command live against the daemon. Reply:

```
(LaneRegistered (new-lanes-design-designer [NewLanesDesign Designer] Structural))
```

The daemon assigned the lane identifier as the hyphen-joined lowercase
rendering of the role vector (`new-lanes-design-designer`), confirming
the `irmw` filesystem-form rule. Confirmed visibility:

```sh
orchestrate "(Observe Lanes)"
;; (LanesObserved [(new-lanes-design-designer [NewLanesDesign Designer] Structural)])
```

The substrate is exactly as the frame found it — dynamic lane
registration works end-to-end today; this cutover is documentation +
convention, not infrastructure. Retirement path (documented in the
skill, not run): `meta-orchestrate "(Retire (Lane new-lanes-design-designer))"`.

## Cross-references for other slices to fix

Two dangling references to the deleted `skills/role-lanes.md` remain in
files outside this slice's scope — they belong to other slices/agents:

- `skills/schema-designer.md:73` — workflow reading list cites
  `skills/role-lanes.md`; should point at `skills/session-lanes.md`.
- `orchestrate/AGENTS.md` — describes the old fixed role-lanes; the
  AGENTS-rewrite slice owns this.

`skills/skills.nota` already indexes `session-lanes` correctly
(line 106, Workflow / Mechanism) — no edit needed.

## Open questions

None blocking. The registration call resolved cleanly. The only
deviation from the slice wording is the CLI binary name
(`meta-orchestrate`, not `orchestrate`) for the `Register` operation,
which the skill states explicitly with the reason.
