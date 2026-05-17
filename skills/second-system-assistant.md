# Skill — second system assistant

*A second system-shaped capacity lane under system-specialist discipline.*

---

## What this skill is for

Use this skill when the workspace needs another independent
system-assistant lane: a bounded CriomOS or CriomOS-home module slice, a
focused platform audit, a host-tool packaging or test backfill, a Nix
hygiene pass, or a deploy-affecting documentation update that can proceed
without taking the `system-assistant` lock.

`second-system-assistant` is a coordination role with its own lock file and
report lane. Claim it through
`tools/orchestrate claim second-system-assistant <paths> -- <reason>` before
editing files. Reports go in `reports/second-system-assistant/` and are
exempt from the claim flow.

This role copies `system-assistant`'s authority and boundaries. It exists only
to provide another visible platform-shaped lane; it does not own different
work.

---

## Required reading

The second-system-assistant's reading list is **identical** to the
system-assistant's. The assistant does the same work as its main role.

**Workspace baseline (every role reads these)**

- `ESSENCE.md`
- `lore/AGENTS.md`
- `protocols/orchestration.md`
- `skills/autonomous-agent.md`
- `skills/beauty.md`
- `skills/naming.md`
- `skills/jj.md`
- `skills/reporting.md`
- `skills/beads.md`
- `skills/skill-editor.md`
- `skills/repository-management.md`
- `skills/feature-development.md`
- `skills/stt-interpreter.md`

**Role contracts**

- `skills/second-system-assistant.md` (this skill)
- `skills/system-assistant.md` — the role this lane copies.
- `skills/system-specialist.md` — the assisted role.
- `skills/operator.md`

**Platform discipline**

- CriomOS's `skills.md` — cluster domain generation, network-neutral
  NixOS module discipline, and the real deploy path.
- `skills/nix-usage.md`
- `skills/nix-discipline.md`
- `skills/testing.md`
- `skills/micro-components.md`
- `skills/contract-repo.md`
- `skills/push-not-pull.md`
- `skills/language-design.md`

**Rust applied to platform work**

- `skills/abstractions.md`
- `skills/rust-discipline.md` (index)
- `skills/rust/methods.md`
- `skills/rust/errors.md`
- `skills/rust/storage-and-wire.md`
- `skills/rust/parsers.md`
- `skills/rust/crate-layout.md`
- `skills/actor-systems.md`
- `skills/kameo.md`
- `skills/architectural-truth-tests.md`
- `skills/architecture-editor.md`

**Active beads**

Second-system-assistant works the system-specialist pool's beads:

```sh
bd ready --label role:system-specialist --limit 30
```

There is no `role:second-system-assistant` label. When filing a bead
for the discipline, file under `role:system-specialist`. See
`protocols/orchestration.md` §"Beads belong to main roles, not
assistants".

Repo-level reads (`AGENTS.md`, `ARCHITECTURE.md`, `skills.md`) sit on top of
these workspace skills when work enters a specific repo.

---

## Working pattern

Claim the second-system-assistant role:

```sh
tools/orchestrate claim second-system-assistant <paths> -- <reason>
```

Use path locks for files and repos; use task locks for BEADS or named work
items. Second-system-assistant does not work under the system-specialist or
system-assistant lock. Parallel system capacity is only visible when it has
its own lock file.

All scope, authority, deploy, secret, and reporting rules from
`skills/system-assistant.md` apply unchanged. The only differences are:

- lock file: `second-system-assistant.lock`;
- report lane: `reports/second-system-assistant/`;
- claim role: `second-system-assistant`.

---

## See also

- this workspace's `skills/system-assistant.md` — the role this lane copies.
- this workspace's `skills/system-specialist.md` — the assisted role's
  platform discipline.
- this workspace's `protocols/orchestration.md` — claim flow and role lanes.
- this workspace's `skills/autonomous-agent.md` — checkpoint reads and
  routine-obstacle handling.
- this workspace's `skills/jj.md` — version-control discipline.
