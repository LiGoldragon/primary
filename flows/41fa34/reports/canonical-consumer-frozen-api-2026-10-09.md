# Canonical consumer frozen API — 2026-10-09

This is a pre-publication implementation record.  It authorizes no flake
edit until Astra supplies one published handoff with exact Psyche and
Curriculum pins.

## Required interface

- Replace `CURRICULUM_PSYCHES_SKILLS_DIR` with
  `CURRICULUM_PSYCHES_REPOSITORY_DIR`.
- Its value is the Psyche repository root:
  `${inputs."psyche-skills"}`.  There is no compatibility fallback.
- Mind and Field environment-variable semantics remain unchanged.
- Registry roots are explicit: current `psyche-skills/*.md` retains its
  logical name; `vision/*.md` has logical name `vision-<stem>`.
- Duplicate logical names are refused.  No path extension or implicit escape
  is admitted.  The logical `vision-ethos` dependency graph remains stable.

## Publication dependency and scope

Astra reports fresh remote Psyche main `5c1922`, superseding an earlier
`3fea248` observation; this record does not establish ancestry or content.
The one publication handoff must provide exact immutable pins and cover the
old/new authored source, Curriculum settings/registry/docs, and fixture
updates under their assigned writers.

The canonical flake already has a pre-existing dirty modification and remains
untouched.  The legacy workspace flake and its checks are not validation for
this migration.

## Runtime handoff after publication

Astra qualifies the immutable-Nix root change as requiring a fresh registry
in memory through `SkillMemory::open`, with Home `ExecStartPost` running
`RebuildSkills`.  The new resolver, exact
`CURRICULUM_PSYCHES_REPOSITORY_DIR` repository root, and published revisions
must be present before that open.  Field then owns restart/reseed/rebuild.

The old Nix path cannot be removed through a cross-root `EditSkills` signal;
the registry refuses it outside the new roots.  A mutable within-repository
fixture does not cover this immutable transition.  Field must compare logical
skill set, bodies, and every role output before and after while preserving the
prior output; `CheckSkills` after automatic `RebuildSkills` is insufficient
proof.  Producer reopen fixtures remain pending remote immutable checks.
