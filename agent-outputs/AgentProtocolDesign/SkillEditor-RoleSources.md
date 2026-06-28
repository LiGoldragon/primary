# Skill Editor Role Sources

Task: Add V1 role source modules and `agent-output-protocol` for the AgentProtocolDesign weave.

BEADS: `primary-y0h6.3` - Add V1 role source modules and agent-output-protocol.

## Status

Implemented locally. I claimed the task through orchestration as
`skill-editor` over the task, the new role/protocol source paths, and this
output file, then released the claim after the files and checks were complete.

Closed `primary-y0h6.3` with a note pointing at the new source modules, this
handoff output, and the downstream generator task.

No commit or push was performed. The weave assigns final version-control
mechanics to the downstream Repo Operator task.

## Changed Files

In `/git/github.com/LiGoldragon/skills`:

- `modules/agent-output-protocol/full.md`
  - Defines the shared worker output convention:
    `agent-outputs/<SessionName>/`, CamelCase session names,
    `<RoleLabel>-<ArtifactName>.md`, path-only/minimal chat returns, durable
    fallback handling when a worker already replied substantively in chat, and
    provisional handling for audit/corpus learning.
- `roles/intent-translator/full.md`
  - Defines the role as translation from clarified psyche intent into domain
    dependency graph, implementation brief, evidence expectations, and audit
    recommendation.
- `roles/scout/full.md`
  - Defines read-only context mapping with observed facts separated from
    interpretations and explicit unknowns.
- `roles/repo-scaffolder/full.md`
  - Defines repository scaffold and structural rework preparation from accepted
    intent and local conventions.
- `roles/general-code-implementer/full.md`
  - Defines normal code and generator implementation work, while leaving
    skill-system prose to Skill Editor.
- `roles/criomos-implementer/full.md`
  - Defines CriomOS-specific implementation with host, deployment, secret, and
    rollback discipline.
- `roles/rust-auditor/full.md`
  - Defines independent Rust review with findings-first output and workspace
    Rust discipline.
- `roles/nix-auditor/full.md`
  - Defines independent Nix review with flake/module/check/deployment focus.
- `roles/skill-editor/full.md`
  - Defines exclusive ownership of skill-system source content, manifests,
    dependency indexes, and source/generated reconciliation.
- `roles/intent-maintainer/full.md`
  - Defines intent log, supersession, manifestation, and cleanup boundaries.
- `roles/repo-operator/full.md`
  - Defines final repository status, commit, push, BEADS closeout, and handoff
    mechanics after validation and audit evidence exist.

In `/home/li/primary`:

- `agent-outputs/AgentProtocolDesign/SkillEditor-RoleSources.md`
  - This handoff output.

## Design Decisions

Each role source starts with a role contract before workflow details so role
identity stays first when packets are assembled.

Common output mechanics live only in `agent-output-protocol`. The role files
refer to the shared protocol and do not duplicate the full protocol body.

The lead/orchestrator is intentionally absent from the generated role set.
Generated spawned roles cover only the ten V1 worker roles named in the active
manifest.

The files carry no harness frontmatter, generated-file notice, output
description metadata, target metadata, or dependency metadata. Those stay in the
manifest and dependency index.

Where psyche intent did not define a finer point, the source text instructs the
role to surface a question instead of inventing authority.

## Checks Run

In `/git/github.com/LiGoldragon/skills`:

```sh
cargo test
```

Result: passed. The existing suite reports 9 integration tests passing, plus
empty unit/doc test suites.

Structural checks:

- Verified all eleven new source paths named by
  `manifests/module-dependencies.nota` exist.
- Checked new role/protocol files for duplicate `##` headings; none found.
- Checked for runtime generated-file notice banners. The only matches were
  policy sentences forbidding generated notices, not notice banners.

An initial attempt to use `rg`, `sort`, and `uniq` failed because those commands
were not on this shell's `PATH`; the structural checks were rerun with
available tools.

## Follow-Up Requirements

For the generator implementation task:

- Teach the generator to parse `active-outputs.nota` and
  `module-dependencies.nota`.
- Expand role packets with dependency-before-dependent ordering so
  `agent-output-protocol` is included in every spawned worker role packet.
- Deduplicate modules by module id at first position.
- Emit role outputs without generated-file notices.
- Define generator-owned cleanup boundaries for role packet target directories.

For the doctrine revision task:

- Align intent-led orchestration guidance with the new spawned role set while
  preserving the lead/orchestrator as a special non-generated role.

For validation and audit:

- Inspect a generated sample role packet once generation exists.
- Confirm Claude, Codex, and Pi physical outputs use the correct wrapper/path
  per the harness discovery evidence.
