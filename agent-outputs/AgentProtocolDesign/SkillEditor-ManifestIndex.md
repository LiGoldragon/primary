# Skill Editor Manifest/Index Report

Task: Add active Role/Skill manifest and module dependency index for the AgentProtocolDesign weave.

BEADS: `primary-y0h6.2` - Add active Role/Skill manifest and module dependency index.

## Status

Completed. I claimed the task through orchestration as `editor` over `(Task primary-y0h6.2)` and `(Path /git/github.com/LiGoldragon/skills)`, then closed the bead after the data surfaces and guidance updates landed locally.

Captured the repo-level intent change in Spirit as record `dfl5`: the skills generator V1 source surface uses one active NOTA manifest for generated Skill and Role outputs, plus a separate dependency-only module index.

No commit or push was performed in this bead; the AgentProtocolDesign weave assigns final repository commit/push mechanics to the downstream Repo Operator bead.

## Changed Files

In `/git/github.com/LiGoldragon/skills`:

- `manifests/active-outputs.nota`
  - New active output manifest.
  - Contains 66 active `Skill` records derived from the current active skill roster.
  - Contains 10 active V1 `Role` records: `intent-translator`, `scout`, `repo-scaffolder`, `general-code-implementer`, `criomos-implementer`, `rust-auditor`, `nix-auditor`, `skill-editor`, `intent-maintainer`, and `repo-operator`.
- `manifests/module-dependencies.nota`
  - New dependency-only module index.
  - Records module id, source path, and dependency module ids only.
  - Existing active skill modules have empty dependency vectors.
  - V1 role modules depend on `agent-output-protocol`.
- `skills.md`
  - Updated repo guidance so agents use `active-outputs.nota` for active generated outputs and `module-dependencies.nota` for source paths/dependencies.
  - Marks `skills-roster.nota` as current CLI compatibility input until generator migration.
- `INTENT.md`
  - Manifested the prompt-level repo intent: V1 generated Skill and Role outputs are governed by one active manifest, and dependencies live in the sidecar index.
- `README.md`
  - Documents the new V1 source-side surfaces and the current compatibility roster.

## Design Decisions

The active manifest is heterogeneous by design, so it uses distinct `Skill(...)` and `Role(...)` records. It lists active outputs only; archived and deleted outputs remain outside this manifest.

The dependency index is homogeneous, so each record is an untagged positional module record:

```nota
(module-id source-path [dependency-module-id ...])
```

The active manifest does not duplicate source paths or dependencies. It refers to module ids; `module-dependencies.nota` resolves those ids to source paths and dependency edges.

No full V1 role source bodies were created. The role source paths in `module-dependencies.nota` are forward references for `primary-y0h6.3`, which owns `roles/<role>/full.md` and `modules/agent-output-protocol/full.md`.

No runtime generated-file notices were added.

## Checks

Ran in `/git/github.com/LiGoldragon/skills`:

```sh
cargo test
```

Result: passed. The existing generator test suite reports 9 integration tests passing.

Structural checks:

- `manifests/active-outputs.nota`: 66 `Skill` records, 10 `Role` records.
- `manifests/module-dependencies.nota`: 77 records total, covering 66 active skills, 10 roles, and the shared `agent-output-protocol` dependency module.

## Follow-Up Requirements

For `primary-y0h6.3`:

- Create `modules/agent-output-protocol/full.md`.
- Create the ten `roles/<role>/full.md` source modules referenced by the dependency index.
- Keep role source markdown mostly role prose; generation metadata stays in the manifest/index.

For `primary-y0h6.4`:

- Add schema/parser support for `manifests/active-outputs.nota` and `manifests/module-dependencies.nota`.
- Migrate generation from the compatibility `skills-roster.nota` to the new active manifest plus dependency index.
- Implement role output expansion, dependency-before-dependent ordering, and first-position deduplication by module id.
- Preserve the no-runtime-generated-file-notice policy.
- Define cleanup boundaries for role packet outputs from the manifest-owned active set rather than broad, unsafe directory pruning.

Known limitation: the current generator schema cannot parse the new files yet. That is expected and intentionally left for `primary-y0h6.4`; this bead only adds the source-side data surfaces and repo guidance.
