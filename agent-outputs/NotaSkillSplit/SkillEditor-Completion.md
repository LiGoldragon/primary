# NOTA Skill Split Completion

## Task And Scope

Skill-editor worker for the approved orchestration lane. Scope was skills only: create or revise reusable NOTA skills in `/git/github.com/LiGoldragon/skills`, regenerate runtime skill surfaces in `/home/li/primary`, and preserve the separate invalid-response-log request for later routing.

## Sources Consulted

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/skills/AGENTS.md`
- `/git/github.com/LiGoldragon/skills/skills.md`
- `/home/li/primary/agent-outputs/NotaSchemaStudy/Scout-SituationalMap.md`
- `/git/github.com/LiGoldragon/skills/modules/nota-design/full.md`
- `/git/github.com/LiGoldragon/skills/modules/nota-schema-docs/full.md`
- `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota`
- `/git/github.com/LiGoldragon/skills/manifests/module-dependencies.nota`
- `/git/github.com/LiGoldragon/skills/manifests/skills-roster.nota`

Spirit public query observed `w312` and `qvb3`, supporting schema-derived mechanics and canonical codec use.

## Source Changes

Changed canonical skills repo files:

- `modules/nota-literacy/full.md`: new skill for understanding and replying with prompt-supplied NOTA schema/help/examples, with expression-only reply discipline and diagnostic escape-hatch guidance.
- `modules/nota-schema-design/full.md`: new skill for authoring schema that specifies NOTA types, positional struct fields, optionality, and codec-backed help surfaces.
- `modules/nota-design/full.md`: compatibility pointer to the two new capability-specific skills.
- `manifests/active-outputs.nota`: exposes both new skills as first-class `AgentsSkill` and `ClaudeSkill` outputs.
- `manifests/module-dependencies.nota`: adds both modules as `RuntimeSkill`.
- `manifests/skills-roster.nota`: adds both modules to the compatibility roster.
- `tests/generation.rs`: updates hardcoded current-skill counts from 55/69 to 57/71.

Compatibility notes:

- `nota-design` remains active for the older raw grammar/codec design guidance.
- `nota-schema-docs` remains active for pseudo-NOTA markdown documentation only.
- The new names split reply literacy from schema authoring as requested.

## Generated Surfaces

Regenerated `/home/li/primary` runtime surfaces with:

```sh
SKILLS_SOURCE_ROOT=/git/github.com/LiGoldragon/skills SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-generate.nota
```

Generated NOTA surfaces changed:

- `.agents/skills/nota-literacy/SKILL.md`
- `.agents/skills/nota-schema-design/SKILL.md`
- `.agents/skills/nota-design/SKILL.md`
- `.claude/skills/nota-literacy/SKILL.md`
- `.claude/skills/nota-schema-design/SKILL.md`
- `.claude/skills/nota-design/SKILL.md`

After rebasing the source repo onto remote `main` commit `c469d147`, regeneration preserved the peer context-handover/orchestration generated changes; those surfaces no longer appear in the final primary diff.

## Checks

Run in `/git/github.com/LiGoldragon/skills`:

```sh
cargo test
SKILLS_SOURCE_ROOT=/git/github.com/LiGoldragon/skills SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota
```

Results:

- `cargo test`: passed, 26 integration tests plus doc tests.
- `skills-check.nota`: passed and reported the generated output set.

Additional grep checks found no `typed NOTA`, generated-file notices, or source frontmatter in the new source modules.

## Version Control

Skills repo:

- Rebased the NOTA skills commit onto remote `main` commit `c469d147`.
- Pushed `main` to `7807e3f1` with message `skills: add NOTA literacy and schema design skills`.

Primary workspace:

- Runtime generated surfaces are ready to commit.
- Unrelated preexisting primary working-copy files present and included by primary whole-working-copy doctrine:
  - `agent-outputs/ChromaPiThemeCleanup/GeneralCodeImplementer-Evidence.md`
  - `agent-outputs/NotaSchemaStudy/Scout-SituationalMap.md`
  - `agent-outputs/PersistentSpiritMirror/OperatingSystemImplementer-MirrorStandUpFindings.md`

## Blockers And Follow-Up

No blockers remain for this task. Do not update Mind/Spirit prompts or handle the separate invalid-response-log request in this worker.
