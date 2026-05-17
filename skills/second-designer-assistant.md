# Skill — second designer assistant

*A second design and audit capacity lane under designer discipline.*

---

## What this skill is for

Use this skill when the workspace needs another independent
designer-assistant lane: design audit, report inventory,
cross-reference cleanup, role-surface maintenance, skill/protocol edits, or
bounded design support where the structural authority remains with designer.

`second-designer-assistant` is a coordination role with its own lock file and
report lane. Claim it through
`tools/orchestrate claim second-designer-assistant <paths> -- <reason>` before
editing files. Reports go in `reports/second-designer-assistant/` and are
exempt from the claim flow.

This role copies `designer-assistant`'s authority and boundaries. It exists
only to provide another visible designer-shaped lane; it does not own
different work.

---

## Required reading

The second-designer-assistant's reading list is **identical** to the
designer-assistant's. The assistant does the same work as its main role.

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

- `skills/second-designer-assistant.md` (this skill)
- `skills/designer-assistant.md` — the role this lane copies.
- `skills/designer.md` — the assisted role.
- `skills/operator.md`
- `skills/operator-assistant.md`
- `skills/second-operator-assistant.md`
- `skills/system-specialist.md`
- `skills/system-assistant.md`
- `skills/second-system-assistant.md`
- `skills/poet.md`
- `skills/poet-assistant.md`

**Design and programming discipline**

- `skills/abstractions.md`
- `skills/actor-systems.md`
- `skills/architectural-truth-tests.md`
- `skills/architecture-editor.md`
- `skills/contract-repo.md`
- `skills/kameo.md`
- `skills/language-design.md`
- `skills/micro-components.md`
- `skills/push-not-pull.md`
- `skills/rust-discipline.md` (index)
- `skills/rust/methods.md`
- `skills/rust/errors.md`
- `skills/rust/storage-and-wire.md`
- `skills/rust/parsers.md`
- `skills/rust/crate-layout.md`
- `skills/testing.md`

**Cross-cutting**

- `skills/mermaid.md`
- `skills/nix-usage.md`
- `skills/nix-discipline.md`

**Active beads**

Second-designer-assistant works the designer pool's beads:

```sh
bd ready --label role:designer --limit 30
```

There is no `role:second-designer-assistant` label. When filing a bead for the
discipline, file under `role:designer`. See `protocols/orchestration.md`
§"Beads belong to main roles, not assistants".

---

## Working pattern

Claim the second-designer-assistant role:

```sh
tools/orchestrate claim second-designer-assistant <paths> -- <reason>
```

Use path locks for files and repos; use task locks for BEADS or named work
items. Second-designer-assistant does not work under the designer or
designer-assistant lock. Parallel design capacity is only visible when it has
its own lock file.

All scope, authority, design, report, and version-control rules from
`skills/designer-assistant.md` apply unchanged. The only differences are:

- lock file: `second-designer-assistant.lock`;
- report lane: `reports/second-designer-assistant/`;
- claim role: `second-designer-assistant`.

---

## See also

- this workspace's `skills/designer-assistant.md` — the role this lane copies.
- this workspace's `skills/designer.md` — the assisted role's design
  discipline.
- this workspace's `protocols/orchestration.md` — claim flow and role lanes.
- this workspace's `skills/autonomous-agent.md` — checkpoint reads and
  routine-obstacle handling.
- this workspace's `skills/jj.md` — version-control discipline.
