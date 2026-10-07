# Curriculum ethos

Curriculum main at 73414b6 (origin/main, read in /git/github.com/LiGoldragon/Curriculum). One ethos file exists: `curriculum.ethos`. No signal-curriculum repository exists under /git/github.com/LiGoldragon. The file has a Library root only; there is no Signal, Operation or Memory root, so there is nothing of those three to copy. The Library root is copied whole below.

## curriculum.ethos, lines 1-41 (Library root)

```
; Typed Curriculum registry protocol. Datom lives at the CLI boundary.

Library
[]
[ SkillPathEdits.{ Vector<String> Vector<String> Vector<String> }
  SkillEdits.{ SkillPathEdits RolePlan }
  SkillChange.{ Vector<String> Vector<String> Vector<String> }
  RolePacketPlan.{ Surface String String String String Effort Permission String String }
  RolePlan.{ Vector<RolePacketPlan> Vector<String> Vector<String> String }
  CliRequest.[ ResolveSkills.Vector<String>
               EditSkills.SkillPathEdits
               CheckSkills
               RebuildSkills ]
  Query.[ ResolveSkills.Vector<String>
          EditSkills.SkillEdits
          CheckSkills.RolePlan
          RebuildSkills.RolePlan ]
  Outcome.[ ResolvedSkills.Vector<String>
            SkillsChanged.SkillChange
            SkillsChecked.Vector<String>
            SkillsRebuilt.Vector<String>
            Rejected.String ]
  RoleManifest.{ Vector<String> }
  RoleManifestDocument.[ GeneratedRoleOutputs.RoleManifest ]
  Provider.[ Claude ChatGpt ]
  Permission.[ Restricted Unrestricted ]
  Effort.[ Low Medium High Xhigh ]
  Surface.[ ClaudeAgent CodexAgent PiAgent ]
  ModelChoice.{ String Option<Effort> }
  RoleModule.{ String String }
  Model.{ String Provider Vector<Effort> }
  RolePermission.{ String String Permission }
  RoleDepth.{ String ModelChoice ModelChoice }
  RoleDescription.{ String String String }
  RoleAlias.{ String String String String Vector<Surface> }
  TargetInsertion.{ String Surface Vector<String> }
  Roles.{ Vector<RoleModule> Vector<Model> Vector<RolePermission> Vector<RoleDepth> Vector<RoleDescription> Vector<RoleAlias> Vector<String> Vector<TargetInsertion> Vector<String> }
  RolesDocument.[ Roles.Roles ] ]

[]
[]
```

The Nexus wires its Signal, Operation and Memory roles in Rust over these Library types: `CurriculumSignal` uses `Query` as both Query and Operation and `Outcome` as both Response and Outcome (src/service.rs:251-256); `SkillMemory` takes `SkillEdits` as its Change (src/service.rs:62).

## Types the Nexus uses that are defined in Rust, not ethos

Data types (11):
- src/service.rs:15 `Settings` (environment roots, workspace, runtime)
- src/service.rs:45 `SkillSnapshot` (the Memory's Remembered)
- src/service.rs:53 `SkillMemory` (the Memory record itself)
- src/registry.rs:12 `SkillEntry`
- src/registry.rs:20 `ResolvedSkill`
- src/registry.rs:28 `SkillRegistry`
- src/registry.rs:34 `RegistryError`
- src/projection.rs:13 `Harness` (Claude, Codex, Pi, OpenCode; ethos `Surface` has no OpenCode)
- src/projection.rs:21 `Surface` (same name as the ethos `Surface` enum, different type)
- src/projection.rs:56 `ProjectionError`
- src/projection.rs:74 `SkillProjector`

Trait-impl markers (3): src/service.rs:130 `CurriculumOperation`, src/service.rs:249 `CurriculumSignal`, src/service.rs:280 `CurriculumNexus`.

CLI-only, behind the `datom` feature (2): src/client.rs:21 `ClientError`, src/client.rs:42 `CurriculumClient`.

## Launch boundary code sites

Curriculum (composes subflow role files and standing skills; writes, does not launch):
- src/roles.rs:46-124 `Roles::packet` builds each role packet from roles.datom: permission module, universal modules, per-surface insertions, model and effort, path `.claude/agents/<id>.md`, `.codex/agents/<id>.toml`, `.pi/agents/<id>.md`.
- src/roles.rs:196-240 render: standing skill bodies are inlined into every role body; Claude gets frontmatter md, Codex a toml with `developer_instructions`, Pi md with `thinking` and `disallowed_tools: 'edit, write'` when Restricted. No OpenCode role surface.
- src/projection.rs:28-54 five skill trees: `.agents/skills`, `.claude/skills`, `.codex/skills`, `.pi/skills`, `.opencode/skills`.
- src/projection.rs:375-389 per-harness skill render; `user-only: true` becomes Claude `disable-model-invocation: true`; OpenCode gets a `name:` frontmatter line.
- src/projection.rs:400-404 Codex trees get `agents/openai.yaml` with `allow_implicit_invocation: false` for user-only skills (the hiding mechanism for Codex).
- src/projection.rs:497-506 writes `tools/standing-skill-selection.mjs` (STANDING_SKILLS).
- src/client.rs:140-170 the CLI reads `CURRICULUM_ROLES_FILE` (roles.datom) and builds the RolePlan sent to the Nexus.

Flow (main flow at ac6ab64; composes and delivers the main-flow startup prompt):
- crates/flow/src/main.rs:127,181-221 `flow` CLI resolves `skill_name_vector` through `curriculum` before Start/Replace and moves operation-main-flow first.
- crates/flow-nexus/src/composition.rs:738-780 `compose`: Codex gets the system-prompt bundle text inline (746); Claude gets a per-launch copy of the bundle file.
- crates/flow-nexus/src/composition.rs:600-631 native head: Claude stacked `/skill` commands; Codex bundle text then `$skill` lines, stock base instructions kept, Codex descendants never see the bundle.
- crates/flow-nexus/src/herdr/launch.rs:1350-1372 Claude argv: `--settings` (bypass permissions, flow-hook), `--remote-control`, `--system-prompt-file <per-launch bundle>`.
- crates/flow-nexus/src/codex.rs:583-690 Codex skills resolved against the app-server `skills/list` catalog; crates/flow-nexus/src/herdr/launch.rs:86-94 Claude skills against its native catalog.
- The bundle path comes from the caller's LaunchProfile field `system_prompt_bundle_file`; neither Flow nor Curriculum authors its text.

Primary launch tools (outside both Nexuses; read in /home/li/primary):
- tools/main-flow-mode/system-prompt.md is the main-flow system prompt text.
- tools/claude-main-flow-launch.mjs:33,40,138,265 and tools/codex-main-flow-launch.mjs:22,33,89 and tools/opencode-main-flow-launch.mjs:32,34,150 import Curriculum's STANDING_SKILLS for birth skills; Claude passes `--system-prompt-file`, Codex passes only `-c model_reasoning_effort`, OpenCode puts the system prompt in its agent config.

## Sources

Witnessed by this subflow through git show and file reads: Curriculum 73414b6 (curriculum.ethos, src/*.rs, roles.datom); flow ac6ab64; root heads grepped on origin/main of every repository under /git/github.com/LiGoldragon; /home/li/primary/tools. No provenance receipt handle is available.
