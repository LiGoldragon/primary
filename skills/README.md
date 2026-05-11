# Workspace Skills — Index

*Canonical index of workspace skills, grouped into four named
bundles. Read this file to resolve a bundle name to its members,
then read the members.*

The substance of each skill lives in its own file under
`skills/<name>.md`; this is the navigation surface, not the
content.

For the proposal and reasoning behind these bundles, see
`~/primary/reports/designer/130-skill-bundles.md`. For the
conventions that govern editing skill files themselves, see
`~/primary/skills/skill-editor.md`.

---

## Bundles

Each bundle has a name. Reading "all the X skills" means reading
every file listed under that bundle.

### Bundle: `programming`

*Read before writing or reviewing code in this workspace,
designing wire contracts, or shaping actor topologies.*

- `skills/abstractions.md`
- `skills/actor-systems.md`
- `skills/architectural-truth-tests.md`
- `skills/beauty.md`
- `skills/contract-repo.md`
- `skills/kameo.md`
- `skills/language-design.md`
- `skills/micro-components.md`
- `skills/naming.md`
- `skills/push-not-pull.md`
- `skills/rust-discipline.md`
- `skills/testing.md`

### Bundle: `operational`

*Read before any commit, push, report, bead, skill edit, or repo
creation. The autonomy floor — these are what lets the agent act
without asking for routine obstacles.*

- `skills/autonomous-agent.md`
- `skills/beads.md`
- `skills/jj.md`
- `skills/nix-discipline.md`
- `skills/reporting.md`
- `skills/repository-management.md`
- `skills/skill-editor.md`

### Bundle: `role`

*Read for the role you're taking on. Each role has a "what I own
/ what I don't own" frame.*

- `skills/designer.md` / `skills/designer-assistant.md`
- `skills/operator.md` / `skills/operator-assistant.md`
- `skills/system-specialist.md` / `skills/system-assistant.md`
- `skills/poet.md` / `skills/poet-assistant.md`

### Bundle: `specialty`

*Read when the task surfaces one of these specific surfaces.*

- `skills/architecture-editor.md` — when editing a per-repo `ARCHITECTURE.md`
- `skills/library.md` — when citing scholarly sources
- `skills/prose.md` — when prose is the craft surface
- `skills/stt-interpreter.md` — when decoding speech-to-text-mangled input

---

## Invocation phrasings

The index recognises these natural human phrasings as referring
to the named bundles:

| Phrase | Resolves to |
|---|---|
| "read the programming skills" / "read all programming skills" | `programming` |
| "read the operational skills" / "operational skills bundle" | `operational` |
| "read the role skills" / "all role skills" | `role` |
| "read the specialty skills" | `specialty` |

When the user names a bundle, the agent reads this index once and
then parallel-reads the bundle's members.

---

## Maintaining this file

The index is hand-maintained. When you create a new skill under
`skills/<name>.md`, add it to the right bundle here in the same
commit. When you delete a skill, remove it. When you move a skill
between bundles (rare), the move is a coordinated change with a
short note in a designer report.

Every skill lives in exactly one bundle, in its primary home.
Cross-references between bundles live in the skill files
themselves (via each skill's `See also` section), not in this
index.
