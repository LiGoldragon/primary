# Scout Situational Map

Task: Map skills-generation tooling and harness agent targets for the AgentProtocolDesign weave, bead `primary-y0h6.1`.

Date: 2026-06-28

## Observed Facts

### BEADS and local scope

- `bd show primary-y0h6.1` names this task as "Map skills-generation tooling and harness agent targets" and requires a read-only situational map at `agent-outputs/AgentProtocolDesign/Scout-SituationalMap.md`.
- The bead's required reads include `AGENTS.md`, `skills/skills.nota`, `.agents/skills/beads/SKILL.md`, a generated Scout role packet if available, and discovered local skills-generation/harness docs.
- I claimed the in-flight work through the orchestration lock as `(Task primary-y0h6.1)` under the `assistant` role.
- I did not inspect `private-repos/` or `repos/`.

### Skills-generation source and wrapper surface

- Primary's root `flake.nix` is explicitly described as `"primary workspace generated skill surfaces"`.
- Primary's `flake.nix` has a `skills` input at `github:LiGoldragon/skills` and wraps that input's apps:
  - `generate-skills`: "Regenerate configured skill outputs into the workspace root".
  - `check-skills`: "Check generated skill outputs in the workspace root without writing".
  - `default = generate-skills`.
- Primary's `flake.lock` locks `skills` to `github:LiGoldragon/skills` rev `116498fa818dd682d5b3dffe02cc254f5e375bb7`.
- A local checkout exists at `/git/github.com/LiGoldragon/skills`.
- `/git/github.com/LiGoldragon/skills/README.md` says the repo is the "Source repository for generated workspace skill surfaces".
- The skills repo's checked-in roster is `/git/github.com/LiGoldragon/skills/manifests/skills-roster.nota`.
- Source modules live under `/git/github.com/LiGoldragon/skills/modules/<name>/full.md`.
- Deprecated role modules live under `/git/github.com/LiGoldragon/skills/skills/archive/` and are not emitted.

### Current generator inputs, commands, tests, and cleanup

- The skills repo's generator requests are:
  - `/git/github.com/LiGoldragon/skills/skills-generate.nota`: `(Generate ($SKILLS_SOURCE_ROOT $SKILLS_WORKSPACE_ROOT manifests/skills-roster.nota Write))`
  - `/git/github.com/LiGoldragon/skills/skills-check.nota`: `(Generate ($SKILLS_SOURCE_ROOT $SKILLS_WORKSPACE_ROOT manifests/skills-roster.nota Check))`
- README commands:
  - Regenerate: `nix run github:LiGoldragon/skills#generate-skills -- <workspace-root>`
  - Check drift: `nix run github:LiGoldragon/skills#check-skills -- <workspace-root>`
  - Local Cargo iteration: `SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=<workspace-root> cargo run -- skills-check.nota`
- Primary wrapper commands from primary root:
  - `nix run .#generate-skills -- <workspace-root>`
  - `nix run .#check-skills -- <workspace-root>`
  - `nix flake check` includes `generated-skills-current`, which runs upstream `check-skills` against `${self}`.
- Skills repo `flake.nix` exports checks for `test`, `fmt`, `clippy`, `no-hard-coded-generation-roots`, `check-request-is-non-writing`, `generation-requests-use-roster`, and `obsolete-intent-led-wrappers-removed`; `default = test`.
- I did not run Nix generation or checks during this map.
- Generator code is in `/git/github.com/LiGoldragon/skills/src/assembly.rs`; the binary entry point is `/git/github.com/LiGoldragon/skills/src/main.rs`.
- Generator interfaces are schema-authored in `/git/github.com/LiGoldragon/skills/schema/assembly.schema` and emitted into `/git/github.com/LiGoldragon/skills/src/schema/assembly.rs`.
- Current schema has `SkillRoster`, `SkillModule`, `EntryPoint`, `EntryPointExtra`, `TargetSurface [AgentsSkill ClaudeSkill]`, and `ExtraSurface [ClaudeCommand CodexPrompt CodexCommand]`.
- `GenerationJobs` always renders `skills/skills.nota`, then active first-class skill manifests, then entry-point extras.
- `OutputSurface::skill_path` maps:
  - `AgentsSkill` to `.agents/skills/<module>/SKILL.md`
  - `ClaudeSkill` to `.claude/skills/<module>/SKILL.md`
- `OutputSurface::extra_path` maps:
  - `ClaudeCommand` to `.claude/commands/<module>.md`
  - `CodexPrompt` to `.codex/prompts/<module>.md`
  - `CodexCommand` to `.codex/commands/<module>.md`
- The current roster's `EntryPoints` vector is empty.
- Current tests in `/git/github.com/LiGoldragon/skills/tests/generation.rs` assert:
  - generated `.agents/skills/example/SKILL.md` and `.claude/skills/example/SKILL.md` have roster-derived frontmatter and identical body;
  - `skills/skills.nota` points at `.agents/skills/<name>/SKILL.md`;
  - the current roster parses as 76 modules, 66 active modules, 9 archived role modules, and 1 deleted `subagent-session-workflow` module;
  - active modules all emit `[AgentsSkill ClaudeSkill]`;
  - no entrypoint command/prompt extras are currently generated;
  - check mode fails on stale generated outputs;
  - write mode prunes `.agents/skills` and `.claude/skills` before writing.
- `WorkspacePruner` currently removes `.agents/skills` and `.claude/skills` in write mode, plus any entry-point extra paths.
- `StaleOutputScan` checks for stale archived/deleted first-class skill outputs under expected `.agents/skills` and `.claude/skills` paths.
- `README.md`, `INTENT.md`, and `skills.md` all state generated outputs carry no provenance headers.

### Current generated target locations in primary

- `skills/skills.nota` exists and is generated from the roster.
- `.agents/skills/` exists and contains generated skill directories with `SKILL.md` files.
- `.claude/skills/` exists and contains generated skill directories with `SKILL.md` files.
- `.claude/commands/` exists but no generated command files were observed.
- `.codex/commands/` and `.codex/prompts/` exist but no primary project-local files were observed in them.
- `.claude/agents/` exists and is empty.
- `.codex/agents/` exists and is empty.
- `.pi/` exists with `.pi/continue/`; no primary `.pi/agents/` directory was observed.

### Harness discovery evidence: Pi

- Pi source is locally available under `/home/li/.local/share/criomos/pi/package`.
- Pi's core skill loader in `src/core/skills.ts` loads default skills from:
  - user: `agentDir/skills`, where `agentDir` defaults to `~/.pi/agent`;
  - project: `<cwd>/.pi/skills`;
  - explicit skill paths.
- Pi's package manager also discovers `.agents/skills`:
  - user: `~/.agents/skills`;
  - project ancestor directories: `<ancestor>/.agents/skills`, stopping at the git repository root.
- Pi trust code explicitly names `.agents/skills` as a project-trust surface.
- Pi's project context loader discovers `AGENTS.md`/`CLAUDE.md` from the agent dir and cwd ancestors.
- A disabled Pi extension exists under `/home/li/.pi/agent/extensions-disabled/pi-superpowers-plus-repo/extensions/subagent/`.
- That disabled subagent extension discovers user agents from `~/.pi/agent/agents`, project agents from nearest ancestor `.pi/agents`, and bundled extension agents from the extension's package `agents/` directory.
- That disabled extension's agent frontmatter requires at least `name` and `description`; optional fields include `tools`, `extensions`, and `model`; the body becomes the subagent system prompt.
- `/home/li/.pi/agent/agents` exists and is empty.
- Because the subagent extension is under `extensions-disabled`, this is evidence of a local Pi subagent convention, not evidence that project-local Pi agents are currently active in this primary session.

### Harness discovery evidence: Claude

- `claude --help` advertises:
  - `--agent <agent>` for current-session agent selection;
  - `--agents <json>` for custom agents supplied as JSON;
  - `--plugin-dir` for loading plugins;
  - `--bare`, which skips customizations including skills, plugins, hooks, custom commands, and custom agents.
- Local Claude plugin docs state subagents go in `.claude/agents/`.
- Local Claude plugin-development docs state Claude Code scans plugin `agents/` directories for `.md` files.
- Local Claude agent examples use YAML frontmatter with `name`, `description`, `model`, `color`, and sometimes `tools`, followed by the agent body/system prompt.
- Current primary `.claude/agents/` exists and is empty.
- Local installed Claude plugins include agent files under paths such as `/home/li/.claude/plugins/marketplaces/claude-plugins-official/plugins/pr-review-toolkit/agents/code-reviewer.md`, confirming the `.md with YAML frontmatter + body` agent file shape.

### Harness discovery evidence: Codex

- `codex --help` exposes commands for `plugin`, `mcp`, `exec`, `review`, and `debug prompt-input`; it does not list an `agents` command.
- `codex debug prompt-input` in `/home/li/primary` shows current Codex skill roots:
  - `/home/li/.codex/skills/.system`
  - plugin cache skill roots under `/home/li/.codex/plugins/cache/.../skills`
  - `/home/li/primary/.agents/skills`
- The same prompt input evidence shows Codex is consuming primary generated skills through `.agents/skills`, not `.codex/skills`.
- `/home/li/.codex/prompts/helper-only.md` exists as a user-level prompt with frontmatter `description` and `argument-hint`.
- Current primary `.codex/prompts/` and `.codex/commands/` directories exist but no project-local files were observed in them.
- Current primary `.codex/agents/` exists and is empty.
- Codex plugin marketplace README under `/home/li/.codex/.tmp/plugins/README.md` says plugins can contain optional `skills/`, `.app.json`, `.mcp.json`, plugin-level `agents/`, `commands/`, hooks, assets, and other files.
- Codex plugin cache examples contain skill-local `agents/openai.yaml` files with OpenAI-facing metadata.
- I did not find local evidence that project-level `.codex/agents/*.md` is an active Codex discovery surface.

### Existing versus missing V1 role-packet surfaces

- Existing now:
  - Skill-only generator repo: `/git/github.com/LiGoldragon/skills`.
  - Skill-only active roster: `/git/github.com/LiGoldragon/skills/manifests/skills-roster.nota`.
  - Generated skill outputs in primary: `skills/skills.nota`, `.agents/skills/*/SKILL.md`, `.claude/skills/*/SKILL.md`.
  - Schema support for non-skill entrypoint extras: `ClaudeCommand`, `CodexPrompt`, `CodexCommand`, but no current roster entries using them.
  - Empty project directories that look intended or reserved: `.claude/agents/`, `.codex/agents/`, `.codex/commands/`, `.codex/prompts/`.
  - Pi project-local subagent directory convention `.pi/agents` exists in a disabled extension's code, but primary does not currently have `.pi/agents/`.
- Drafted only in the translator output:
  - The ten V1 worker role names: Intent Translator, Scout, Repo Scaffolder, General Code Implementer, CriomOS Implementer, Rust Auditor, Nix Auditor, Skill Editor, Intent Maintainer, Repo Operator.
  - The requirement for `agent-output-protocol`.
  - The requirement for an active Role/Skill manifest and sidecar dependency index.
- Missing in local source as of this map:
  - Generated Scout role packet.
  - Active role source modules for the ten V1 worker roles.
  - `agent-output-protocol` source module.
  - A manifest with explicit `Role(...)` and `Skill(...)` records.
  - A sidecar module dependency index.
  - Generator support for role packet outputs.
  - Generator cleanup logic for generated role packet target directories.
  - Tests or checks for role packet expansion, dependency ordering, role-specific frontmatter/wrappers, or role-output cleanup.

## Interpretations

- The likely implementation home is the existing `/git/github.com/LiGoldragon/skills` generator, because primary already depends on it for generated harness skill surfaces and its schema/code already owns target-surface projection into the primary workspace.
- Extending the existing generator is not a trivial data-only change. The repo's current intent and tests explicitly frame V1 as skill-module assembly with no module-declared dependencies/imports; role packets plus a sidecar dependency index are a scope expansion.
- `.agents/skills` is the proven shared generated skill surface for Pi and Codex. It is not proven as a role-packet surface.
- Claude role packets have the clearest local file target: `.claude/agents/<name>.md` with YAML frontmatter and body.
- Pi role packets have a plausible but not currently active local target through the disabled subagent extension: project `.pi/agents/<name>.md` using `name`, `description`, optional `tools`, `extensions`, `model`, and body.
- Codex role packets are the least proven locally. Current Codex consumes `.agents/skills` for skills and supports prompts/commands/plugins, but I did not find evidence that `.codex/agents/*.md` is a live project agent target.
- Existing `.claude/agents/` and `.codex/agents/` empty directories are local evidence of intended project surfaces, but emptiness alone does not prove runtime discovery.
- For V1, implementation should avoid claiming "Claude/Codex/Pi all use the same agent-file semantics" until the Codex and Pi active-runtime paths are proven by a smoke test or current harness docs.

## Likely Relevant Files and Surfaces for the Next Implementer

- Primary wrapper:
  - `flake.nix`
  - `flake.lock`
  - `skills/skills.nota`
  - `.agents/skills/`
  - `.claude/skills/`
  - `.claude/agents/`
  - `.codex/agents/`
  - `.codex/commands/`
  - `.codex/prompts/`
  - `.pi/`
- Translator output and BEADS:
  - `agent-outputs/AgentProtocolDesign/IntentTranslator-TranslationBrief.md`
  - bead `primary-y0h6.1` through `primary-y0h6.9`
- Skills generator repo:
  - `/git/github.com/LiGoldragon/skills/AGENTS.md`
  - `/git/github.com/LiGoldragon/skills/INTENT.md`
  - `/git/github.com/LiGoldragon/skills/skills.md`
  - `/git/github.com/LiGoldragon/skills/README.md`
  - `/git/github.com/LiGoldragon/skills/flake.nix`
  - `/git/github.com/LiGoldragon/skills/schema/assembly.schema`
  - `/git/github.com/LiGoldragon/skills/manifests/skills-roster.nota`
  - `/git/github.com/LiGoldragon/skills/skills-generate.nota`
  - `/git/github.com/LiGoldragon/skills/skills-check.nota`
  - `/git/github.com/LiGoldragon/skills/src/assembly.rs`
  - `/git/github.com/LiGoldragon/skills/src/markdown.rs`
  - `/git/github.com/LiGoldragon/skills/src/error.rs`
  - `/git/github.com/LiGoldragon/skills/tests/generation.rs`
- Pi local evidence:
  - `/home/li/.local/share/criomos/pi/package/src/core/skills.ts`
  - `/home/li/.local/share/criomos/pi/package/src/core/package-manager.ts`
  - `/home/li/.local/share/criomos/pi/package/src/core/resource-loader.ts`
  - `/home/li/.local/share/criomos/pi/package/src/core/trust-manager.ts`
  - `/home/li/.pi/agent/extensions-disabled/pi-superpowers-plus-repo/extensions/subagent/agents.ts`
  - `/home/li/.pi/agent/extensions-disabled/pi-superpowers-plus-repo/extensions/subagent/index.ts`
  - `/home/li/.pi/agent/extensions-disabled/pi-superpowers-plus-repo/agents/*.md`
- Claude local evidence:
  - `claude --help`
  - `/home/li/.claude/plugins/marketplaces/claude-plugins-official/plugins/claude-code-setup/skills/claude-automation-recommender/references/subagent-templates.md`
  - `/home/li/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/agent-development/SKILL.md`
  - `/home/li/.claude/plugins/marketplaces/claude-plugins-official/plugins/*/agents/*.md`
- Codex local evidence:
  - `codex --help`
  - `codex debug prompt-input`
  - `/home/li/.codex/.tmp/plugins/README.md`
  - `/home/li/.codex/prompts/helper-only.md`
  - `/home/li/.codex/plugins/cache/*/*/skills/*/agents/openai.yaml`

## Unknowns and Blockers

- Codex project-local role packet discovery is not proven. I found `.codex/agents/` in primary and plugin-level `agents/` support, but no local proof that Codex loads `.codex/agents/*.md`.
- Pi project-local role packet discovery depends on a disabled extension in the local installation. I found `.pi/agents` discovery code there, but not evidence that this extension is currently enabled.
- The current skills repo intent says V1 has no module-declared dependencies or imports. The new sidecar dependency index directly expands the generator's current model and may need explicit acceptance as a scope change.
- Current generated skill cleanup prunes full `.agents/skills` and `.claude/skills`. Equivalent cleanup boundaries for role packets are not defined.
- Current schema has `EntryPointExtra` for Claude commands and Codex prompts/commands, but no role target enum. Role targets need a new typed surface rather than overloading skill surfaces.
- No generated file ownership marker exists by design. Cleanup for role packet files will need another way to distinguish generator-owned files from user-authored harness files, likely by manifest-owned active output set and narrow target directory policy.
- No Scout role packet was generated or available to read.

## Clarification Questions for the Psyche

- Should generated worker role packets live in the existing `skills` repo even though its current repo intent is skill-focused, or should role-packet generation be a sibling generator/source surface?
- For Codex, is the desired V1 output an actual `.codex/agents/*.md` project surface, a plugin-level `agents/openai.yaml` surface, a `.codex/prompts/*.md` prompt surface, or another Codex-specific mechanism?
- For Pi, should V1 depend on enabling the local subagent extension that discovers `.pi/agents`, or should Pi receive role packets through an already-active skill/prompt path?
- Should role-packet cleanup be allowed to prune entire harness role directories such as `.claude/agents` or only files explicitly named in the active manifest?
