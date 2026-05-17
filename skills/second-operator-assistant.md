# Skill — second operator assistant

*A second implementation and audit capacity lane under operator discipline.*

---

## What this skill is for

Use this skill when the workspace needs another independent
operator-assistant lane: a bounded implementation slice, an audit of operator
commits, a test backfill, a mechanical migration, a dependency bump, or a
per-repo documentation update caused by implementation work.

`second-operator-assistant` is a coordination role with its own lock file and
report lane. Claim it through
`tools/orchestrate claim second-operator-assistant <paths> -- <reason>` before
editing files. Reports go in `reports/second-operator-assistant/` and are
exempt from the claim flow.

This role copies `operator-assistant`'s authority and boundaries. It exists
only to provide another visible operator-shaped lane; it does not own
different work.

---

## Required reading

The second-operator-assistant's reading list is **identical** to the
operator-assistant's. The assistant does the same work as its main role.

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

- `skills/second-operator-assistant.md` (this skill)
- `skills/operator-assistant.md` — the role this lane copies.
- `skills/operator.md` — the assisted role.
- `skills/designer.md`

**Programming discipline**

- `skills/abstractions.md`
- `skills/actor-systems.md`
- `skills/architectural-truth-tests.md`
- `skills/architecture-editor.md`
- `skills/contract-repo.md`
- `skills/kameo.md`
- `skills/language-design.md`
- `skills/micro-components.md`
- `skills/nix-usage.md`
- `skills/nix-discipline.md`
- `skills/push-not-pull.md`
- `skills/rust-discipline.md` (index)
- `skills/rust/methods.md`
- `skills/rust/errors.md`
- `skills/rust/storage-and-wire.md`
- `skills/rust/parsers.md`
- `skills/rust/crate-layout.md`
- `skills/testing.md`

**Active beads**

Second-operator-assistant works the operator pool's beads:

```sh
bd ready --label role:operator --limit 30
```

There is no `role:second-operator-assistant` label. When filing a bead for the
discipline, file under `role:operator`. See `protocols/orchestration.md`
§"Beads belong to main roles, not assistants".

Repo-level `AGENTS.md`, `ARCHITECTURE.md`, and `skills.md` sit on top of
these workspace skills when the work enters a repo under `repos/`.

---

## Working pattern

Claim the second-operator-assistant role:

```sh
tools/orchestrate claim second-operator-assistant <paths> -- <reason>
```

Use path locks for files and repos; use task locks for BEADS or named work
items. Second-operator-assistant does not work under the operator or
operator-assistant lock. Parallel operator capacity is only visible when it has
its own lock file.

All scope, authority, implementation, report, and version-control rules from
`skills/operator-assistant.md` apply unchanged. The only differences are:

- lock file: `second-operator-assistant.lock`;
- report lane: `reports/second-operator-assistant/`;
- claim role: `second-operator-assistant`.

---

## See also

- this workspace's `skills/operator-assistant.md` — the role this lane copies.
- this workspace's `skills/operator.md` — the assisted role's implementation
  discipline.
- this workspace's `protocols/orchestration.md` — claim flow and role lanes.
- this workspace's `skills/autonomous-agent.md` — checkpoint reads and
  routine-obstacle handling.
- this workspace's `skills/jj.md` — version-control discipline.
