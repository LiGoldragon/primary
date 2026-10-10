# Scout: Harness Agent Discovery

## Scope

This investigation used local evidence under `/home/li/primary`, installed CLI help, local package/source trees, installed Pi packages, user config files, and Codex debug output. It did not edit any workspace files other than this report.

## Codex Observed Facts

`codex` is installed at `/home/li/.nix-profile/bin/codex` and reports `codex-cli 0.141.0`.

`codex --help` exposes commands including `exec`, `review`, `mcp`, `plugin`, and `debug prompt-input`. The top-level help did not expose a direct `--agent` or project agent file flag. `codex plugin --help` exposes plugin management commands: `add`, `list`, `marketplace`, and `remove`.

`codex plugin list` reported installed/enabled curated plugins:

```text
gmail@openai-curated
github@openai-curated
```

`codex -C /home/li/primary debug prompt-input 'probe prompt'` showed model-visible skill roots including:

```text
r0 = /home/li/.codex/skills/.system
r1 = /home/li/.codex/plugins/cache/openai-curated/github/3fdeeb49/skills
r2 = /home/li/.codex/plugins/cache/openai-curated/gmail/3fdeeb49/skills
r3 = /home/li/primary/.agents/skills
```

That proves Codex loads `/home/li/primary/.agents/skills` in this workspace session as reusable skill packets.

`/home/li/primary/.codex` exists with empty subdirectories:

```text
/home/li/primary/.codex/agents
/home/li/primary/.codex/commands
/home/li/primary/.codex/prompts
```

Those empty directories were not treated as proof by themselves.

Primary Codex source is locally available at `/git/github.com/openai/codex`. The source file `/git/github.com/openai/codex/codex-rs/core/src/config/agent_roles.rs` implements agent role loading. It loads roles from:

1. `[agents.<name>]` declarations in Codex config layers.
2. TOML role files discovered recursively under `agents` beside an active config layer folder.

For a project config layer, that means the discovered project-local path is:

```text
<project>/.codex/agents/**/*.toml
```

The same source recursively walks directories and includes files whose extension is `toml`.

`/git/github.com/openai/codex/codex-rs/config/src/config_toml.rs` defines the declared config shape:

```toml
[agents.researcher]
description = "Research role"
config_file = "./agents/researcher.toml"
nickname_candidates = ["Hypatia", "Noether"]
```

The declaration fields are:

```text
description
config_file
nickname_candidates
```

`config_file` paths are relative to the config file directory.

Standalone role files under `.codex/agents` are TOML. Source parsing in `agent_roles.rs` accepts metadata fields:

```text
name
description
nickname_candidates
```

It also flattens normal Codex config fields into the same TOML file. Practical fields include `developer_instructions`, `model`, `model_provider`, `model_reasoning_effort`, `sandbox_mode`, and other valid Codex config options.

Source validation requires standalone auto-discovered role files to have both:

```text
name
developer_instructions
```

The final role also needs a human-facing `description`, either from the role file or from a config declaration. A split config role referenced by `[agents.<name>]` can provide the role name from the table and the description from the declaration.

`/git/github.com/openai/codex/codex-rs/core/src/agent/role.rs` defines built-in agent roles:

```text
default
explorer
worker
```

The same file applies user-defined role config as a high-precedence session config layer when spawning an agent role. Spawn selection errors and tests refer to the role selector as `agent_type`.

Project-local config layers are trust-gated. `/git/github.com/openai/codex/codex-rs/core/src/config/config_loader_tests.rs` includes `project_layers_disabled_when_untrusted_or_unknown`, and config loader warnings say project config layers are not loaded until the project is trusted. Therefore `.codex/config.toml` and `.codex/agents/*.toml` depend on the project config layer being active/trusted.

Codex skills are implemented separately in `/git/github.com/openai/codex/codex-rs/core-skills/src/loader.rs`. That loader uses:

```text
.agents/skills
skills
```

For project/repo ancestors it scans for `.agents/skills`, which matches the `debug prompt-input` evidence in this workspace. These are model-visible reusable instruction packets, not spawnable agent roles.

`/git/github.com/openai/codex/codex-rs/external-agent-migration/src/lib.rs` migrates external Markdown agent files into Codex TOML role files. The migrated Markdown format uses YAML frontmatter with required `name` and `description`, optional fields such as `permissionMode` and `effort`, and a body that becomes `developer_instructions`. The target is TOML, not live direct Markdown loading.

Plugin manifests in the installed curated plugin cache use `.codex-plugin/plugin.json` with fields such as:

```text
name
version
description
skills
apps
mcpServers
interface
```

The installed plugins provide skills and apps/connectors, not project-local agent role files.

## Codex Interpretations

Codex does support project-local custom subagent role packets, based on source evidence, at:

```text
.codex/agents/**/*.toml
```

The safest standalone V1 file shape is:

```toml
name = "scout"
description = "Fast local evidence gathering role."
developer_instructions = """
You are a Scout. Gather local evidence, separate facts from interpretations, and return concise handoff context.
"""
```

Optional role fields can use normal Codex config keys, for example:

```toml
model_reasoning_effort = "low"
nickname_candidates = ["Scout"]
```

The enabling condition is that the project config layer must be active/trusted. If using a declared role instead of standalone discovery, put a table like this in `.codex/config.toml`:

```toml
[agents.scout]
description = "Fast local evidence gathering role."
config_file = "./agents/scout.toml"
nickname_candidates = ["Scout"]
```

For reusable role-like instructions that should be visible in the current Codex prompt without relying on subagent spawning, `.agents/skills/<skill>/SKILL.md` is the closest proven mechanism. The current workspace already loads `/home/li/primary/.agents/skills`.

Do not treat `.codex/commands` or `.codex/prompts` as proven Codex agent role locations from the evidence gathered here.

## Pi Observed Facts

`pi` is installed at `/home/li/.nix-profile/bin/pi` and reports version `0.80.2`.

`pi --help` exposes resource-loading flags:

```text
--extension, -e <path>
--skill <path>
--prompt-template <path>
--no-extensions
--no-skills
--no-prompt-templates
--no-context-files
--approve
--no-approve
```

The help text says `--approve` trusts project-local files for the run and `--no-approve` ignores project-local files for the run. It also says context files include `AGENTS.md` and `CLAUDE.md`.

`pi list` reported active user packages:

```text
packages/pi-criomos
packages/pi-linkup
packages/pi-web-access
packages/pi-subagents
packages/pi-continue
```

`~/.pi/agent/settings.json` includes `packages/pi-subagents`, so the active subagent mechanism is installed through Pi packages.

`~/.pi/agent/packages/pi-subagents` is a symlink to:

```text
/nix/store/2fbpkcdc14p22zgakfbp9hanpgai83fk-pi-subagents-0.31.0/share/pi-packages/pi-subagents
```

The package manifest at that path declares:

```json
"pi": {
  "extensions": ["./src/extension/index.ts"],
  "skills": ["./skills"],
  "prompts": ["./prompts"]
}
```

That proves the installed package contributes an active extension, skills, and prompts to Pi.

The previously found `pi-superpowers-plus` subagent extension is disabled. It exists under disabled locations such as:

```text
~/.pi/agent/extensions-disabled/pi-superpowers-plus-repo
~/.pi/agent/extensions-disabled/pi-superpowers-plus.off
```

It is not listed in active `pi list` output and is not listed as an active package in `~/.pi/agent/settings.json`.

Native Pi source is installed under:

```text
/nix/store/crjni6hgmdz5jchc1xl936lx844g515s-pi-0.80.2/lib/pi-monorepo/packages/coding-agent
```

The core trust manager lists project-local trust-gated resources:

```text
.pi/settings.json
.pi/extensions
.pi/skills
.pi/prompts
.pi/themes
.pi/SYSTEM.md
.pi/APPEND_SYSTEM.md
```

It also handles `.agents/skills` in ancestor directories. It does not list native `.pi/agents`.

The core resource loader loads resource types:

```text
extensions
skills
prompts
themes
```

It has `getAgentsFiles()`, but that refers to context files named `AGENTS.md` and `CLAUDE.md`, not custom subagent role packets.

The Pi package manifest type includes:

```text
extensions
skills
prompts
themes
```

It does not include native `agents` as a core Pi resource type.

The active `pi-subagents` package source at `src/agents/agents.ts` implements subagent discovery. It loads agent Markdown files from:

```text
builtin package agents directory
installed package-declared subagent paths
~/.pi/agent/agents/**/*.md
~/.agents/**/*.md
<project>/.agents/**/*.md
<project>/.pi/agents/**/*.md
directories in PI_SUBAGENT_EXTRA_AGENT_DIRS
```

The source excludes files ending in `.chain.md` and skips legacy `.agents/skills` paths.

The package README confirms the preferred project-local path:

```text
.pi/agents/**/*.md
```

It also documents legacy project discovery at:

```text
.agents/**/*.md
```

When both legacy and preferred project locations define the same runtime name, the preferred `.pi/agents` definition wins.

The `pi-subagents` Markdown frontmatter parser requires:

```text
name
description
```

The body after frontmatter becomes the subagent system prompt.

Known frontmatter fields from `src/agents/agent-serializer.ts` are:

```text
name
package
description
tools
model
fallbackModels
thinking
systemPromptMode
inheritProjectContext
inheritSkills
defaultContext
skill
skills
extensions
subagentOnlyExtensions
output
defaultReads
defaultProgress
interactive
maxSubagentDepth
completionGuard
```

Fields such as `tools`, `defaultReads`, `skills`, `fallbackModels`, `extensions`, and `subagentOnlyExtensions` are parsed as comma-separated strings. Boolean-like fields are parsed from strings such as `true` and `false`.

The README gives this representative agent file shape:

```yaml
---
name: scout
package: code-analysis
description: Fast codebase recon
tools: read, grep, find, ls, bash, mcp:chrome-devtools
extensions:
subagentOnlyExtensions: ./tools/child-only-search.ts
model: claude-haiku-4-5
fallbackModels: openai/gpt-5-mini, anthropic/claude-sonnet-4
thinking: high
systemPromptMode: replace
inheritProjectContext: false
inheritSkills: false
skills: safe-bash, chrome-devtools
output: context.md
defaultReads: context.md
defaultProgress: true
completionGuard: false
interactive: true
maxSubagentDepth: 1
---
Your system prompt goes here.
```

Bundled examples in the active package include `agents/scout.md`, `agents/worker.md`, `agents/reviewer.md`, `agents/researcher.md`, `agents/context-builder.md`, `agents/planner.md`, `agents/delegate.md`, and `agents/oracle.md`.

The bundled `scout.md` uses frontmatter like:

```yaml
name: scout
description: Fast codebase recon that returns compressed context for handoff
tools: read, grep, find, ls, bash, write, intercom
thinking: low
systemPromptMode: replace
inheritProjectContext: true
inheritSkills: false
output: context.md
defaultProgress: true
```

The current project has `/home/li/primary/.pi/continue/*.md`, but no observed `/home/li/primary/.pi/agents` directory. `/home/li/primary/.agents` currently contains `skills/*/SKILL.md`; no project-local Pi agent Markdown files were observed directly under `.agents`.

## Pi Interpretations

Native Pi does not appear to have a built-in custom agent role packet resource. Native reusable mechanisms are project/user extensions, skills, prompt templates, themes, and context files.

Custom agent role packets in this installation are provided by the active `pi-subagents` package. Because `packages/pi-subagents` is active in `pi list` and in user settings, project-local subagent files are supported by the active extension.

The preferred V1 generated Pi subagent path should be:

```text
.pi/agents/<role>.md
```

The recommended V1 file shape is:

```yaml
---
name: scout
description: Fast local evidence gathering role
tools: read, grep, find, ls, bash
thinking: low
systemPromptMode: replace
inheritProjectContext: true
inheritSkills: false
output: context.md
defaultProgress: true
---
You are a Scout. Gather local evidence, separate observed facts from interpretations, and return concise handoff context.
```

Use `.agents/<role>.md` only for legacy compatibility. Do not place Pi subagent role files under `.agents/skills`; the active subagent loader explicitly skips that path and Pi/Codex both use it for skills.

Project-local Pi files should be used with project trust enabled, either through an existing trust entry or with `pi --approve` for a run. `pi --no-approve` should be expected to ignore project-local resources.

The previously found `pi-superpowers-plus` subagent extension should not be targeted for V1 because it is disabled. Target the active `pi-subagents` package instead.

## V1 Recommendations

For Codex, generate two different output types only when each is needed:

1. Spawnable Codex subagent roles: `.codex/agents/<role>.toml`, with `name`, `description`, and `developer_instructions`, plus optional Codex config fields.
2. Reusable Codex role guidance for the current prompt system: `.agents/skills/<skill>/SKILL.md`, because this workspace demonstrably loads `.agents/skills`.

For Pi, generate active subagent roles at:

```text
.pi/agents/<role>.md
```

Use YAML frontmatter with at least `name` and `description`, and put the role prompt in the Markdown body.

For cross-harness generated role packets, keep Codex and Pi outputs separate. Codex subagent roles are TOML config layers; Pi subagent roles are Markdown files consumed by an extension.

## Remaining Unknowns

Codex `.codex/agents/*.toml` support was proven from local source, not by spawning an actual subagent role in this harness. This session did not expose a Codex subagent spawn tool to test role availability directly.

It remains unproven whether Codex auto-discovers `.codex/agents/*.toml` when `.codex/config.toml` is absent. Source discovery is tied to an active config layer folder, so implementers should assume a trusted `.codex` config layer is required until runtime-tested.

Pi `pi-subagents` project discovery was proven from installed active package source and package state, not by invoking a live model/tool call. A quick command with `pi --approve --offline --no-tools --no-session -p '/subagents-models'` produced no useful output in this investigation.

The exact live slash-command output for `/subagents-doctor` and `/subagents-models` was not captured.

## Next Commands And Files

Codex implementers should inspect:

```bash
sed -n '1,540p' /git/github.com/openai/codex/codex-rs/core/src/config/agent_roles.rs
sed -n '1,430p' /git/github.com/openai/codex/codex-rs/core/src/agent/role.rs
sed -n '640,690p' /git/github.com/openai/codex/codex-rs/config/src/config_toml.rs
sed -n '1,260p' /git/github.com/openai/codex/codex-rs/core-skills/src/loader.rs
codex -C /home/li/primary debug prompt-input 'probe'
codex plugin list
```

Pi implementers should inspect:

```bash
readlink -f ~/.pi/agent/packages/pi-subagents
sed -n '1010,1375p' "$(readlink -f ~/.pi/agent/packages/pi-subagents)/src/agents/agents.ts"
sed -n '1,220p' "$(readlink -f ~/.pi/agent/packages/pi-subagents)/src/agents/agent-serializer.ts"
sed -n '439,566p' "$(readlink -f ~/.pi/agent/packages/pi-subagents)/README.md"
pi list
pi --approve
```

Inside an interactive trusted Pi session, implementers should run:

```text
/subagents-doctor
/subagents-models
```

They should also ask the subagent tool to list agents, if exposed in that session:

```text
subagent({ action: "list" })
```
