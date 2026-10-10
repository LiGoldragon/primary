# Implementer Generator Report

Task: Implement role-packet generation, dependency expansion, and cleanup for the AgentProtocolDesign weave.

BEADS: `primary-y0h6.4` - Implement role-packet generation, dependency expansion, and cleanup.

## Status

Implemented locally in `/git/github.com/LiGoldragon/skills`.

I claimed the task through orchestration as `general-code-implementer` over the generator repo and this output file, then closed `primary-y0h6.4` and released the orchestration claim after implementation and checks completed. No commit or push was performed; final repository mechanics remain assigned to the downstream Repo Operator bead.

## Changed Files

In `/git/github.com/LiGoldragon/skills`:

- `schema/assembly.schema`
  - Added V1 active output manifest types, module dependency index types, role target surfaces, TOML output kind, and generated role-output inventory type.
  - Renamed the request field from roster path to manifest path while preserving the same positional request shape.
- `src/schema/assembly.rs`
  - Regenerated from the schema.
- `src/assembly.rs`
  - Reads `manifests/active-outputs.nota` plus sibling `manifests/module-dependencies.nota` for normal generation.
  - Keeps `manifests/skills-roster.nota` parseable as a legacy compatibility input.
  - Builds skill outputs from active `Skill` records and module index paths.
  - Builds role packets from role source module first, then ordered manifest includes expanded through module dependencies.
  - Deduplicates module ids at first resolved position.
  - Emits Claude and Pi role packets as Markdown with YAML frontmatter/body.
  - Emits Codex role packets as TOML with `name`, `description`, and `developer_instructions`.
  - Adds generator-owned role cleanup through `skills/generated-role-outputs.nota` instead of pruning whole role target directories.
- `src/error.rs`
  - Added duplicate and missing module-id errors.
- `tests/generation.rs`
  - Added parser coverage for active manifest/index.
  - Added role expansion, dependency ordering, dedupe, no-notice, physical path, Codex TOML, Claude/Pi Markdown, and stale role cleanup coverage.
  - Preserved legacy roster compatibility coverage.
- `skills-generate.nota`, `skills-check.nota`
  - Switched checked-in generation requests to `manifests/active-outputs.nota`.
- `flake.nix`
  - Updated the generation-request check to require the active manifest.
- `manifests/active-outputs.nota`
  - Converted `Skill` and `Role` records to generated-codec enum payload shape.
  - Added explicit ordered role includes.
  - Kept role output ids unchanged while changing role source module ids to `role-*` to avoid collisions with skill module ids.
- `manifests/module-dependencies.nota`
  - Updated role source module ids to match active role records and keep module ids unique.
- `README.md`, `skills.md`
  - Updated generation and cleanup guidance for active manifest/index and role-output inventory.

Upstream files from earlier beads are still present in the same dirty working copy: the new manifest/index files, `modules/agent-output-protocol/full.md`, and the ten `roles/*/full.md` source files. I preserved and built on them.

## Behavior

Normal generation now uses:

```text
manifests/active-outputs.nota
manifests/module-dependencies.nota
```

Role output paths are:

```text
.claude/agents/<role>.md
.codex/agents/<role>.toml
.pi/agents/<role>.md
```

Runtime role packets do not receive generated-file notices.

Skill target surfaces remain separate from role target surfaces. `AgentsSkill` and `ClaudeSkill` are still skill outputs; `ClaudeAgent`, `CodexAgent`, and `PiAgent` are role outputs.

Role cleanup does not prune `.claude/agents`, `.codex/agents`, or `.pi/agents` wholesale. The generator writes `skills/generated-role-outputs.nota`; on the next write it removes only previously inventoried generated role paths that are no longer active.

## Checks Run

In `/git/github.com/LiGoldragon/skills`:

```sh
cargo test
cargo clippy --all-targets -- -D warnings
nix flake check
```

Results: all passed.

Local primary check:

```sh
SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota
```

Result: failed because `/home/li/primary/skills/skills.nota` is missing. I did not run write mode against `/home/li/primary`; emitting physical workspace role files is assigned to the downstream harness-output bead.

## Handoff Notes

Next harness-output/validation work should run generation in write mode against `/home/li/primary`, then inspect:

```text
skills/skills.nota
skills/generated-role-outputs.nota
.claude/agents/*.md
.codex/agents/*.toml
.pi/agents/*.md
```

Validation should also confirm that existing non-inventoried files in role target directories survive regeneration.

No unresolved generator blocker remains. The only known external condition is that Codex and Pi runtime discovery still need live harness validation, as noted by the Scout reports.
