# SkillEditor Handoff

## Task and scope

Task: `ReplaceRuntimeDiscoveryDoctrine` for `SkillDoctrineV2`.

Scope owned here: stale `skills.nota` doctrine references and replacement
wording in primary boot/architecture/intent docs, skills repo README and
architecture, active skill source modules, and generated skill packet
reconciliation where the current generator allowed it. Generator Rust/tests and
role assignment manifests were not edited.

Settled direction applied: `skills.nota` is dead as runtime discovery; generated
role packets carry curated critical doctrine modules for normal role work;
skills are terse, self-contained instruction packets; manifests and dependency
indexes own output identity, descriptions, tiers, target surfaces, and module
edges.

## Files consulted

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/home/li/primary/INTENT.md`
- `/home/li/primary/.agents/skills/skill-editor/SKILL.md`
- `/home/li/primary/.agents/skills/architecture-editor/SKILL.md`
- `/home/li/primary/.agents/skills/jj/SKILL.md`
- `/git/github.com/LiGoldragon/skills/AGENTS.md`
- `/git/github.com/LiGoldragon/skills/skills.md`
- `/git/github.com/LiGoldragon/skills/README.md`
- `/git/github.com/LiGoldragon/skills/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota`
- `/git/github.com/LiGoldragon/skills/manifests/module-dependencies.nota`
- `/git/github.com/LiGoldragon/skills/manifests/skills-roster.nota`
- Touched source modules under `/git/github.com/LiGoldragon/skills/modules/`

## Changed files

Primary workspace prose:

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/home/li/primary/INTENT.md`

Deleted generated runtime discovery file:

- `/home/li/primary/skills/skills.nota`

Skills repo source prose:

- `/git/github.com/LiGoldragon/skills/README.md`
- `/git/github.com/LiGoldragon/skills/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/skills/modules/skill-editor/full.md`
- `/git/github.com/LiGoldragon/skills/modules/helper-context-transfer/full.md`
- `/git/github.com/LiGoldragon/skills/modules/nota-design/full.md`
- `/git/github.com/LiGoldragon/skills/modules/nota-schema-docs/full.md`
- `/git/github.com/LiGoldragon/skills/modules/skill-source-core/full.md`

Generated skill packets reconciled before generator blockage:

- `/home/li/primary/.agents/skills/helper-context-transfer/SKILL.md`
- `/home/li/primary/.agents/skills/nota-design/SKILL.md`
- `/home/li/primary/.agents/skills/nota-schema-docs/SKILL.md`
- `/home/li/primary/.agents/skills/skill-editor/SKILL.md`
- `/home/li/primary/.claude/skills/helper-context-transfer/SKILL.md`
- `/home/li/primary/.claude/skills/nota-design/SKILL.md`
- `/home/li/primary/.claude/skills/nota-schema-docs/SKILL.md`
- `/home/li/primary/.claude/skills/skill-editor/SKILL.md`

## Checks run

- `rg -n 'skills\.nota|Skill Index|runtime discovery|discovery index|discovery-index|legacy discovery index|canonical workspace example' AGENTS.md ARCHITECTURE.md INTENT.md /git/github.com/LiGoldragon/skills/README.md /git/github.com/LiGoldragon/skills/ARCHITECTURE.md /git/github.com/LiGoldragon/skills/modules -g '*.md'`
  - Result: no matches in active scoped docs/source modules after edits.
- `rg -n 'skills/skills\.nota|skills\.nota' /git/github.com/LiGoldragon/skills --glob 'README.md' --glob 'ARCHITECTURE.md' --glob 'modules/**/*.md' --glob '!target/**' --glob '!skills/archive/**'`
  - Result: no matches.
- `rg -n 'skills/skills\.nota|skills\.nota' AGENTS.md ARCHITECTURE.md INTENT.md`
  - Result: no matches.
- Manifest/dependency path existence check over `/git/github.com/LiGoldragon/skills/manifests`.
  - Result: no missing source paths reported.
- Fence-aware duplicate heading check on touched source modules.
  - Result: no duplicate headings outside fenced code blocks.
- Harness-frontmatter scan on touched source modules.
  - Result: no frontmatter-like headers in source modules.
- `test ! -e /home/li/primary/skills/skills.nota`
  - Result: deleted file is absent.
- Generated packet stale-reference scan over the four regenerated `.agents` and `.claude` skill packets.
  - Result: no stale `skills.nota` or runtime-discovery references.
- `SKILLS_SOURCE_ROOT=/git/github.com/LiGoldragon/skills SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota`
  - Result: failed on first stale generated output before reconciliation: `.agents/skills/nota-schema-docs/SKILL.md`.
- `SKILLS_SOURCE_ROOT=/git/github.com/LiGoldragon/skills SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-generate.nota`
  - Result: partially reconciled generated skill packets, then failed with `duplicate markdown heading 'Purpose' in /home/li/primary/.claude/agents/intent-translator.md`.
- Final rerun of `SKILLS_SOURCE_ROOT=/git/github.com/LiGoldragon/skills SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota`
  - Result: failed on stale generated role output `/home/li/primary/.claude/agents/intent-translator.md`, consistent with the role-packet generation blocker above.

## Blockers and follow-up

The current generator cannot complete a full reconciliation because
`intent-translator` role packet assembly hits duplicate `Purpose` headings from
existing role/module composition. That is outside this prose-only brief and was
not fixed here.

Generator implementers still need to land or finish the generator-side removal
of `skills.nota` emission/check expectations if not already complete in their
concurrent work. This task removed the consuming workspace file and active
doctrine references, and reconciled generated skill packets as far as the
current generator allowed.

Historical references intentionally left alone:

- `/home/li/primary/agent-outputs/**`
- `/git/github.com/LiGoldragon/skills/agent-outputs/**`
- `/home/li/primary/context.md`

Those are prior investigation or handoff artifacts, not active boot docs or
active skill source doctrine.
