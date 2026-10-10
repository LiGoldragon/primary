# Harness settings: what we set today, and what the harnesses offer

A read-only inventory for the living's vision in `flows/28d847/vision/harness.md`. That vision asks for a standard, Nix-defined setup for every Claude Code and Codex home, kept in its own repository, which also documents the harnesses' options. Read on 2026-10-04 from:
- CriomOS-home `origin/main` (`d029e60f`); the local checkout is on branch `flow-home-opencode-42265e`;
- the live homes on Ouranos;
- the Primary launchers in `tools/`;
- Flow (repository 0.24.0 at `5e0b1bf`; deployed flow-nexus 0.23.0);
- hexis, persona-test and flow-test.

How the managed settings are applied: Home Manager activation runs `hexis.lib.mkManagedConfig`, which merges declared keys into a live, mutable file. Hexis has three modes:
- `ensure` (the default): the declared value wins where it speaks, and user changes survive elsewhere;
- `always`: the declared value is asserted on every activation;
- `once`: the value is seeded at the first activation and then left alone.

In the tables, **Scope** names which homes get the setting.

## 1. What we set today

### 1.1 Claude Code

| Setting | Value | Where it is set | Why (record) | Scope |
|---|---|---|---|---|
| `permissions.defaultMode` | `bypassPermissions` | CriomOS-home `modules/home/profiles/min/codex-remote-control.nix:51-56` (hexis, `always`) into `~/.claude/settings.json` | commit c6419c84 "declare Claude bypass permission default" (2026-09-24); psyche `flows/5578cc/vision/permissions.md` "I don't want to have to allow stuff manually" | every Home user's `~/.claude` |
| `--dangerously-skip-permissions` | flag on every run | `owned-agents/claude-code/default.nix` wrapper `--add-flags` | commit 3c868629 "Make managed Claude launchers bypass and child-session safe" | every `claude` started from the installed package |
| unset `CLAUDE_CODE_CHILD_SESSION`, `_SESSION_KIND`, `_SESSION_ID` | unset | same wrapper; also `direct-claude` (`min/default.nix:307-317`) | same commit: a nested launch must not inherit the parent's identity | every `claude` |
| `DISABLE_AUTOUPDATER=1`, `DISABLE_INSTALLATION_CHECKS=1` | set | same wrapper | commit f964853a: the package is declared, so self-update and installation checks are disabled | every `claude` |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS=1` | set-default | same wrapper | commit f964853a; no stated reason | every `claude` |
| `DISABLE_TELEMETRY`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | **off**; the switch `disableTelemetry ? false` is never passed | same wrapper | the comment says remote control stays intact by default | not set anywhere |
| `PATH` prefix with bubblewrap and socat | set | same wrapper | Claude's sandbox runtime needs them | every `claude` |
| `CLAUDE_CODE_DISABLE_WORKFLOWS=1` | env | `min/default.nix:672` `home.sessionVariables` | commit 41472fac (2026-07-19); no stated reason | login shells only. A systemd unit or a launcher with a cleared environment does not get it. |
| `ENABLE_CLAUDEAI_MCP_SERVERS=false` | env | `min/default.nix:673` | commit 839a429f "claude disable account MCP connectors"; psyche `flows/e4be1c4a/vision/codeAnalysisTools.md` ("the standard is still cli's") | login shells only |
| `projects["/home/li/primary"].hasTrustDialogAccepted` | `true` | `codex-remote-control.nix:58-87` (canonicalize, then hexis `always`) into `~/.claude.json` | commits 7d036382 and 122bc1d1 (2026-08-31) | every Home user; hard-coded to `$HOME/primary` |
| `env.CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, `autoMemoryEnabled=false` | set | `~/.claude/settings.json`, written by hand | Primary `ARCHITECTURE.md` §4–5: "harness-private state stores, including Claude auto-memory, are gated opt-in paths rather than defaults" | this home only |
| `permissions.allow` | about 90 rules (`Read(**)`, `Bash(rm *)`, …) | `~/.claude/settings.json`, written by hand | accumulated from prompts that were answered. Under bypass they matter only to modes other than bypass. | this home only |
| `permissions.additionalDirectories` | `/home/li/git/CriomOS`, an old memory directory | `~/.claude/settings.json`, written by hand | old | this home only |
| `model` | `claude-fable-5-1[1m]` | `~/.claude/settings.json`, written by hand | none found; launchers always pass `--model` | this home only |
| `effortLevel`, `modelSettings.*.effortLevel` | `medium` | `~/.claude/settings.json`, written by hand | psyche `flows/1ac573/vision/operational-effortIsAlwaysMedium.md`; Intent `models.md` "Better models, not higher effort" | this home only |
| `hooks.SessionStart` | Herdr `~/.claude/hooks/herdr-agent-state.sh session` | `~/.claude/settings.json` and the script, put there by Herdr's own installer, **not by Nix** | Herdr pane/session binding | this home only |
| `statusLine` | `bash ~/.claude/statusline.sh` (jj change, model, context %, weekly remaining) | `~/.claude/settings.json`, written by hand (Jun 25) | none found | this home only |
| `enabledPlugins` | `rust-analyzer-lsp@claude-plugins-official` | `~/.claude/settings.json`, written by hand | none found | this home only |
| `tui`, `theme`, `editorMode`, `voiceEnabled`, `agentPushNotifEnabled` | `fullscreen`, `auto`, `vim`, `true`, `true` | `~/.claude/settings.json`, written by hand | the living's preferences, set through `/config` | this home only |
| `skipDangerousModePermissionPrompt`, `skipWorkflowUsageWarning` | `true` | `~/.claude/settings.json`, written by hand | dismissed dialogs | this home only |
| `crossSessionInbound` | `accept` | `~/.claude/settings.json`, written by hand | lets sessions send each other messages | this home only |
| `worktree.bgIsolation` | `none` | `/home/li/primary/.claude/settings.json` (project, tracked) | none found | Primary workspace |
| project `permissions.allow` | three tmux/tmp rules | `/home/li/primary/.claude/settings.local.json` | left over | Primary workspace |
| **Flow seat `--settings`** | `permissions.defaultMode=bypassPermissions`; hooks `SessionStart`, `PostToolUse` (`*`) and `Stop` running `flow-hook` | Flow `crates/flow-nexus/src/herdr/launch.rs:160-180` | the code comment says naming the mode in flag settings suppresses the "Make auto mode your default?" offer, and the hooks report each harness event to Flow | Flow-launched Claude seats only (in the repository; whether 0.23.0 carries all three hooks was not checked) |
| Flow seat flags | `--remote-control <name>`, `--system-prompt-file`, `--session-id`, `--model`, `--effort` | same file, `:1360-1390` | every Flow is remotely controllable; the effort comes from the launch profile | Flow-launched seats |
| Flow unit environment | `CLAUDE_CONFIG_DIR=/home/li/.claude` | `flow-nexus.service`, `flow-nexus-next.service` | pins the home | Flow seats |
| **Primary launcher** | `--effort medium --remote-control --dangerously-skip-permissions --system-prompt-file … --settings <jobDir>/main-flow-settings.json` with a `UserPromptSubmit` main-flow reminder hook (every 20) | `/home/li/primary/tools/claude-main-flow-launch.mjs:99-114,191` | the main-flow mode | seats from that launcher |
| Subagent definitions (`model`, `effort: medium`, tools, prompt) | per role | `/home/li/primary/.claude/agents/*.md`, generated from Curriculum | the Curriculum role tiers | Primary workspace |
| **Not yet set:** a `PermissionRequest` hook (deny with a rewrite message) | n/a | ruled by the living on 2026-10-04 (log line 85); dispatched, not on `origin/main` | `reports/permission-prompts.md` | n/a |

### 1.2 Codex

There are three live homes:
- **`~/.codex`**: the plain `codex-remote-control.service`, frozen at 0.153.4, and the ChatGPT desktop app's default home.
- **`~/.codex-next`**: the promoted *stable* role, with the `codex` command and the Flow stable endpoint, running 0.158.
- **`~/.codex-next-8mkkxq293hk2`**: the *next* candidate, named by its derivation hash. Flow's next endpoint, `codex-next`, and the app opened Sep 30 point here.

| Setting | Value | Where it is set | Why (record) | Scope |
|---|---|---|---|---|
| `approval_policy` | `never` | `min/codex-permission-defaults.nix`, merged by `min/default.nix:77,724-736` (hexis `ensure`) | commit c6c42dbe "Default Codex sessions to full access" (2026-09-01); psyche `flows/5578cc/vision/permissions.md` | **`~/.codex` only.** `~/.codex-next` has it because `codex-next.nix` `prepare` copied `~/.codex/config.toml` once, at bootstrap. **The candidate home lacks it**, because `codex-next-candidate.nix` copies only `auth.json`. This caused 24 prompts on Sep 30 (`reports/permission-prompts.md`). |
| `sandbox_mode` | `danger-full-access` | same | same | same gap |
| `approvals_reviewer` | `user` | not declared; written by Codex itself | n/a | `~/.codex`, `~/.codex-next` |
| `developer_instructions` | the skill-read de-duplication text | `min/default.nix:35,78` | commit 7fc6fab0 "manage Codex developer instructions" (2026-06-29): stops re-reading skills that were already pasted | `~/.codex` (and `~/.codex-next` by copy); not the candidate |
| `model` / `model_reasoning_effort` | `gpt-6-astra` / `xhigh` (hexis `always`) | `min/default.nix:79-80,729-730` | no record. **Contradicts** the living's "effort is always medium" (`flows/1ac573/vision/operational-effortIsAlwaysMedium.md`, Intent `models.md`). Launchers override it with `-c model_reasoning_effort="medium"`, but a bare `codex` or an app thread starts at xhigh. | `~/.codex`; `.codex-next` by copy |
| `plan_mode_reasoning_effort` | `xhigh` | `min/default.nix:82` | none; same tension | same |
| `personality` | `pragmatic` | `min/default.nix:81` | commit 7fc6fab0 | same |
| `features.multi_agent` / `multi_agent_v2` | `true` / `false` | `min/default.nix:84-87` | commits e4123384 and caa77f6f (2026-07-24, "V1 subagent models") | same |
| `agents.default_subagent_model` / `_reasoning_effort` | `gpt-5.6-luna` / `xhigh` (`always`) | `min/default.nix:132-135` | commit e4123384; same effort tension | same |
| Built-in agent roles `default`, `worker`, `explorer` | luna xhigh, terra high, luna xhigh | `min/default.nix:41-75,711-713` → `~/.codex/agents/*.toml` | commit e4123384 | **`~/.codex` only**; neither `.codex-next` home has `agents/` |
| `projects.*.trust_level` | 13 paths (`/home/li/primary` trusted, `/home/li` untrusted, …), several stale `/home/li/git/*` | `min/default.nix:89-103` | none; hand-collected | `~/.codex`; the candidate home has only `/home/li/primary`, added by Codex itself |
| `notice.hide_rate_limit_model_nudge`, `notice.model_migrations` | `true`; three mappings | `min/default.nix:105-112` | commit 7fc6fab0; dismissed nags | `~/.codex` |
| `tui.theme` (`once`), `tui.status_line`, `status_line_use_colors`, `model_availability_nux` (`always`) | `github` (live is `catppuccin-mocha`); five status items | `min/default.nix:114-125` | the living's preferences | `~/.codex`; `.codex-next` by copy; the candidate has none |
| `plugins` (`gmail`, `github`) | enabled | `min/default.nix:127-130` | none | `~/.codex` |
| `features.hooks` | `true` (`always`) | `min/herdr.nix:155-163` | commit 04446e78: Herdr's SessionStart hook needs it | **`~/.codex-next` only.** `~/.codex` has it from Herdr's installer; the candidate home has a trusted hook state but no `features.hooks` key |
| `hooks.json` SessionStart → `herdr-agent-state.sh` | Herdr pane binding | `min/herdr.nix:150-200` for `~/.codex-next`; Herdr's own installer for the other two | same | all three homes, by different routes |
| Removal of retired `orchestrator` and `features.collab` | removed | `min/default.nix:718-722` | commit 433958ae | `~/.codex` |
| `CODEX_HOME` per role | the wrappers `codex`, `codex-next`, `codex-stable-remote`, `codex-*-flow-client` | `codex-remote-control.nix`, `codex-next.nix`, `codex-next-candidate.nix`, `herdr.nix` | home separation per release role | n/a |
| App-server units | `app-server --remote-control --listen unix://…`, `UMask=0077`, `LimitNOFILE=524288` | the same three modules | Remote Control from the phone (`flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md`) | one unit per home |
| Candidate bootstrap | copies `auth.json` only | `codex-next-candidate.nix` `ExecStartPre` | protects the credential, but leaves the home without config | candidate |
| Desktop-app keys (`desktop.*`), `marketplaces.*`, most `plugins.*`, `mcp_servers.*` (`node_repl`, `cua_repl`, `openaiDeveloperDocs`, a stale `agent-intercom`), `features.js_repl=false` | various | written by the ChatGPT app and Codex itself | not ours | `~/.codex`, `~/.codex-next` |
| `rules/default.rules` `prefix_rule … allow` | about 10 rules | `~/.codex/rules/`, written by Codex when prompts were answered | n/a | `~/.codex` only |
| **Flow, Herdr launch** | `-c model_reasoning_effort=<profile>`, `--remote unix://…`; **no approval or sandbox flag** | Flow `herdr/launch.rs:1340-1395` | relies on the home's config, so a Flow seat on the candidate endpoint inherits the gap | Flow Codex seats |
| **Flow, app-server thread** | `approvalPolicy=never`, `sandbox=danger-full-access`, `shell_environment_policy.inherit=core` with `FLOW_ID` and `FLOW_DIRECTORY` set | Flow `codex.rs:930-940` | per-thread override | Flow app-server threads |
| **Primary launcher** | `-m <model> -c 'model_reasoning_effort="medium"' --dangerously-bypass-approvals-and-sandbox` | `tools/codex-main-flow-launch.mjs:82` | the `codex-harness` skill: pin the model and effort, never inherit them | seats from that launcher |
| **Worker launcher** | `thread/start approvalPolicy=never sandbox=danger-full-access`, effort low or medium | `tools/native-worker-launch.mjs:250-256` | same | Terra workers |
| Subagent roles (`read-*`, `write-*`, `tester`, …) | `model`, `model_reasoning_effort=medium`, `developer_instructions` | `/home/li/primary/.codex/agents/*.toml`, generated from Curriculum | the Curriculum role tiers | Primary workspace |

### 1.3 OpenCode (the third harness)

| Setting | Value | Where it is set | Scope |
|---|---|---|---|
| `permission` | `allow` (`always`) | `min/opencode-harness.nix` (hexis) into `~/.config/opencode/opencode.json` | every Home user, Min size and up |
| `plugin` (Herdr state), `tui.json` `plugin` (Herdr TUI) | Nix store paths (`always`) | same | same |
| `autoupdate=false`, `share=disabled` | `always` | same | same |
| `model`, `small_model`, `provider.criomos-local` (llama.cpp on `127.0.0.1:11435`, 64k context, 16k output) | local Qwen3.6-35B-A3B | same, only with `localModel.enable` (the node has the `openCodeTesting` capability) | OpenCode testing node |
| `OPENCODE_DISABLE_EXTERNAL_SKILLS=1` | wrapper | same: reads only `.opencode/skills`, never `.claude` or `.agents` | every `opencode` |
| Seat agent via `OPENCODE_CONFIG_CONTENT` (`agent.main-flow` with the prompt and model) | per launch | `tools/opencode-main-flow-launch.mjs:75-85` | launcher seats |
| Testing server config `share=disabled`, `permission.bash=ask` | `OPENCODE_CONFIG` | `min/opencode.nix` (testing node) | test server |
| System unit `OPENCODE_CONFIG_CONTENT={"share":"disabled"}` | env | CriomOS `modules/nixos/testing/opencode.nix` | system service |

### 1.4 Gaps across homes

1. **The candidate Codex home gets none of the declared config.** It lacks `approval_policy`, `sandbox_mode`, `developer_instructions`, the agent roles, `features.hooks`, the TUI settings, and the model and effort. Codex and the app then use their own defaults (`on-request` with `workspace-write`).
2. **`~/.codex-next` is a one-time copy** of `~/.codex/config.toml`. Later changes to the declaration reach only `~/.codex`, except `features.hooks`.
3. **The declared Codex model and effort contradict Intent.** They are `xhigh` against the "always medium" Intent. Only the launchers correct it.
4. **Most Claude settings are written by hand** in `~/.claude/settings.json`: memory, effort, statusLine, plugins, UI, and the Herdr hook. A new home gets only `defaultMode` and the trust entry.
5. **Two Claude env variables reach only login shells:** `CLAUDE_CODE_DISABLE_WORKFLOWS` and `ENABLE_CLAUDEAI_MCP_SERVERS`.
6. **Telemetry is untouched in both harnesses.**
7. **Trust lists are stale and hard-coded to `/home/li` paths.** The Codex list holds `/home/li/git/*`, and the Claude trust entry is hard-coded to `$HOME/primary`.
8. **The PermissionRequest hook is ruled but not landed.**

## 2. Settings the harnesses offer that we do not set

These catalogs come from vendor sources.
- **Claude Code:** code.claude.com/docs (the settings, permissions, hooks, env-vars, memory, mcp, sandboxing, authentication, monitoring-usage and cli-reference pages, read 2026-10-04 by a docs subagent).
- **Codex:** the local `openai/codex` checkout `ff29a4439` (2026-08-23), mainly `codex-rs/core/config.schema.json`, the config loader, `config_requirements.rs` and the clap flag definitions. The checkout is six weeks older than our deployed 0.158 and 0.161 alphas.
- **OpenCode:** opencode.ai/docs plus `opencode.ai/config.json` and `opencode.ai/tui.json`, read 2026-10-04.

The `(unverified)` mark means the sources were not clear about that entry. The `(from memory)` mark means the entry was added by me rather than read from these sources. Settings already listed in section 1 are omitted.

### 2.0 Files and precedence (the "home" each harness reads)

- **Claude Code:**
  - Precedence, highest first: managed settings → CLI `--settings` → `.claude/settings.local.json` → `.claude/settings.json` → `~/.claude/settings.json`.
  - `~/.claude.json` holds UI and app state, account details, per-project trust and MCP. It mixes credentials-adjacent account fields with configuration, which is why the semi-sandbox generates it (`flows/e167d8/vision/testRepos.md`).
  - `CLAUDE_CONFIG_DIR` relocates the home. `--setting-sources` picks which scopes load.
  - Managed file on Linux: `/etc/claude-code/managed-settings.json` (from memory; the docs subagent could not confirm the path). Also `managed-mcp.json`.
- **Codex:**
  - Precedence, lowest first: built-in → `/etc/codex/config.toml` → `$CODEX_HOME/config.toml` → profile `$CODEX_HOME/<name>.config.toml` (`--profile`'s new meaning; the `[profiles]` table is legacy) → `./.codex/config.toml` up to the repository root (only in trusted projects) → `-c` and UI.
  - Admin-enforced: `/etc/codex/requirements.toml`, which can pin allowed approval policies, sandbox modes, hooks, MCP servers, login methods and more. The legacy `/etc/codex/managed_config.toml` is read as requirements.
  - `CODEX_HOME` relocates everything. `CODEX_SQLITE_HOME` relocates state.
- **OpenCode:**
  - Precedence, lowest first: remote `.well-known/opencode` → global `~/.config/opencode/opencode.json` → `OPENCODE_CONFIG` → project `opencode.json` → `.opencode/` → `OPENCODE_CONFIG_CONTENT` → managed `/etc/opencode/opencode.json`.
  - TUI settings live separately in `tui.json`.

### 2.1 Permissions

- **Claude:**
  - `permissions.deny`, `permissions.ask` (`ask` from memory). Deny is the one list that still bites under bypass.
  - `permissions.disableBypassPermissionsMode` (from memory).
  - `--permission-mode`, `--allow-dangerously-skip-permissions`, `--allowedTools`, `--disallowedTools`, `--tools`.
  - `--permission-prompt-tool` (an MCP tool that answers prompts in `-p` mode), `--permission-prompts`.
- **Codex:**
  - `approval_policy.granular.{sandbox_approval, rules, skill_approval, request_permissions, mcp_elicitations}`.
  - `approvals_reviewer=auto_review|guardian_subagent` and `auto_review.policy`, with the `guardian*` features.
  - Named permission profiles `permissions.<name>.{filesystem, network, workspace_roots, extends}` with `default_permissions`.
  - `apps.*` and `mcp_servers.*.tools.*.approval_mode`.
  - `allow_login_shell`.
  - `--approve-for-me` (the old `--full-auto` is gone).
  - `on-failure` is now an alias of `on-request`.
- **OpenCode:**
  - A per-tool map: `read`, `edit`, `bash`, `task`, `external_directory`, `webfetch`, `doom_loop`, … each `ask|allow|deny`, with glob patterns.
  - Per-agent overrides: `agent.<n>.permission`.
  - `--auto`, env `OPENCODE_PERMISSION`, `experimental.policies`.
  - Default denies `*.env` reads, and asks for `doom_loop` and `external_directory`.

### 2.2 Hooks

- **Claude:**
  - Events beyond the three we use (SessionStart, PostToolUse, Stop, plus UserPromptSubmit in the launcher): `Setup`, `StopFailure`, `SessionEnd`, `PreToolUse`, **`PermissionRequest`** (ruled, not landed), `PostToolUseFailure`, `ConfigChange`, `FileChanged`, `CwdChanged`, `InstructionsLoaded`, `PreModelSwitch`, `PostModelSwitch`, `Notification`, `PreCompact`, `PostCompact`, `WorktreeRemove`.
  - Subagent start and stop events are not in the docs list (unverified).
  - `disableAllHooks` (from memory). `--include-hook-events`, `--init`, `--maintenance`.
- **Codex:**
  - `[hooks]` inline in `config.toml`, as an alternative to `hooks.json`.
  - Events: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, **`PermissionRequest`**, `PreCompact`, `PostCompact`, `Stop`, `SubagentStart`, `SubagentStop`.
  - Handler types: `command` or `mcp_tool`.
  - `hooks.state.*.trusted_hash`: hooks need trust. Codex wrote these entries itself in `.codex-next` and the candidate home.
  - `--dangerously-bypass-hook-trust`, `notify`, and `allow_managed_hooks_only` (requirements only).
- **OpenCode:**
  - Hooks are JS plugins (`plugin`): `event`, `tool.execute.before`, `tool.execute.after`, `shell.env`, `experimental.session.compacting`.
  - Events include `permission.asked` and `permission.replied`.
  - `OPENCODE_DISABLE_DEFAULT_PLUGINS`.

### 2.3 Models and effort

- **Claude:**
  - `availableModels`, `fallbackModel` / `--fallback-model`, `fastMode`, `alwaysThinkingEnabled`, `language`.
  - Env: `ANTHROPIC_MODEL`, `CLAUDE_CODE_EFFORT_LEVEL`, `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` (which alias each tier resolves to), `CLAUDE_CODE_MAX_OUTPUT_TOKENS`.
  - `agent` / `--agent` / `--agents`, `--append-subagent-system-prompt[-file]`.
- **Codex:**
  - `model_provider`, `model_providers.*` (custom endpoints, auth command), `oss_provider`, `--oss`.
  - `model_reasoning_summary`, `model_verbosity`, `service_tier`, `review_model`, `model_context_window`, `model_catalog_json`.
  - `agents.{max_concurrent_threads_per_session, max_depth}`, `agents.<role>.config_file`, `multi_agent_v2.*`.
- **OpenCode:**
  - `enabled_providers` / `disabled_providers`, `provider.*.models.*.variants`, `--variant`.
  - Agent `temperature`, `top_p`, `steps`; `default_agent`, `subagent_depth`, `command.*`.
  - There is no first-class effort key: `reasoningEffort` passes through to the provider.

### 2.4 Context and memory

- **Claude:**
  - `autoCompactEnabled`, `--autocompact`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS`.
  - `--exclude-dynamic-system-prompt-sections`, `--append-system-prompt[-file]`, `--bare` / `CLAUDE_CODE_SIMPLE`, `--safe-mode`.
  - `cleanupPeriodDays` (transcript retention, from memory), `--no-session-persistence`, `disableBundledSkills`.
  - `BASH_DEFAULT_TIMEOUT_MS`, `BASH_MAX_TIMEOUT_MS`, `BASH_MAX_OUTPUT_LENGTH`, `MAX_MCP_OUTPUT_TOKENS`.
- **Codex:**
  - `memories.*` and `features.memories`. Our homes do not set them, while `memories_1.sqlite` exists in all three, so Codex memory is in its default state and unexamined against `ARCHITECTURE.md`'s "memory is opt-in" rule.
  - `model_auto_compact_token_limit`, `compact_prompt` / `experimental_compact_prompt_file`, `tool_output_token_limit`.
  - `project_doc_max_bytes`, `project_doc_fallback_filenames`, `project_root_markers`.
  - `include_environment_context` / `_permissions_instructions` / `_apps_instructions` / `_collaboration_mode_instructions`.
  - `model_instructions_file` (the `codex-harness` skill says we use it; it is not in any home config, so it is per launch).
  - `history.{persistence, max_bytes}`, `skills.*`, `sqlite_home`.
- **OpenCode:**
  - `instructions[]`; AGENTS.md falls back to CLAUDE.md, switched off with `OPENCODE_DISABLE_CLAUDE_CODE*`.
  - `compaction.*`, `snapshot`, `tool_output.*`, `skills.{paths, urls}`, `formatter`, `lsp`, `watcher.ignore`.

### 2.5 Telemetry

None of these is set in any home.

- **Claude:**
  - `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. The wrapper has an unused `disableTelemetry` switch, held off "so remote-control remains intact".
  - OpenTelemetry export: `CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_*_EXPORTER`, `OTEL_EXPORTER_OTLP_*`, `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_TOOL_CONTENT`, `otelHeadersHelper` (from memory).
  - Update control: `autoUpdatesChannel`, `minimumVersion`, `DISABLE_UPDATES`.
- **Codex:**
  - `analytics.enabled` (default true), `feedback.enabled` (default true), `check_for_update_on_startup`.
  - `otel.{exporter, trace_exporter, metrics_exporter, log_user_prompt, environment}`, `log_dir`, `responses_api_metadata`.
- **OpenCode:**
  - `experimental.openTelemetry`, `logLevel`, `OPENCODE_AUTO_SHARE`.
  - No usage-analytics switch is documented.

### 2.6 MCP

- **Claude:**
  - `.mcp.json`, `--mcp-config`, `--strict-mcp-config` (used in the capsule test).
  - `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers` (from memory), `allowedMcpServers`, `deniedMcpServers`.
  - `MCP_TIMEOUT`, `ENABLE_TOOL_SEARCH`.
  - `~/.claude.json` `mcpServers` is empty today.
- **Codex:**
  - `mcp_servers.*.{enabled_tools, disabled_tools, required, startup_timeout_*, tool_timeout_sec, default_tools_approval_mode}`, `mcp_oauth_credentials_store`, `tool_suggest.*`.
  - A stale `agent-intercom` entry remains in `~/.codex` and `~/.codex-next`. Home removed Agent Intercom on 2026-09-28 (commit b87f68cd), but hexis `ensure` does not remove undeclared keys.
- **OpenCode:** `mcp.<name>.{type, command | url, environment, headers, oauth, enabled, timeout}`.
- **Psyche:** "the standard is still cli's" (`flows/e4be1c4a/vision/codeAnalysisTools.md`).

### 2.7 Sandbox

- **Claude:**
  - `sandbox.enabled`, with `sandbox.excludedCommands`, `sandbox.autoAllowBashIfSandboxed`, `sandbox.network.*` (key names from memory). The docs subagent reported `sandbox.level` and per-directory lists (unverified).
  - The wrapper ships bubblewrap and socat for it, but sandboxing is off.
  - `--restricted`.
- **Codex:**
  - `sandbox_workspace_write.{writable_roots, network_access, exclude_*}`.
  - `shell_environment_policy.{inherit, exclude, include_only, set}`. Flow uses `inherit=core`.
  - `[network]` proxy in permission profiles; `features.use_linux_sandbox_bwrap`, `use_legacy_landlock`; `background_terminal_max_timeout`.
- **OpenCode:** no sandbox; only `permission` and `external_directory`.

### 2.8 Credentials

- **Claude:**
  - `~/.claude/.credentials.json`, `ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN` (`claude setup-token`, valid one year), `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, `apiKeyHelper`.
  - Managed-only: `forceLoginMethod`, `forceLoginOrgUUID`, `allowedProviders`.
- **Codex:**
  - `cli_auth_credentials_store=file|keyring|auto|ephemeral`, `forced_login_method`, `forced_chatgpt_workspace_id`.
  - Env: `OPENAI_API_KEY`, `CODEX_API_KEY`, `CODEX_ACCESS_TOKEN`, `CODEX_REMOTE_AUTH_TOKEN` / `--remote-auth-token-env`.
  - `$CODEX_HOME/auth.json`, copied today by `codex-next.nix` and `codex-next-candidate.nix`.
- **OpenCode:**
  - `~/.local/share/opencode/auth.json` (`opencode auth login`), provider env keys, `{env:VAR}` / `{file:path}` substitution.
  - `OPENCODE_SERVER_PASSWORD`; the testing node passes it through systemd `LoadCredential`.
- **For the semi-sandbox:**
  - The two credential files are the only things to copy (persona-test already does this).
  - `CLAUDE_CODE_OAUTH_TOKEN` and `cli_auth_credentials_store=ephemeral` are the documented routes to a credential without a copied file. The `secrets` skill governs how either reaches the program.

### 2.9 UI

- **Claude:**
  - `verbose`, `viewMode`, `axScreenReader`, `outputStyle`, `spinnerTipsEnabled`, `includeCoAuthoredBy` / attribution (from memory), `CLAUDE_CODE_DISABLE_MOUSE`.
  - `~/.claude.json` counters and dismissed-tip flags are harness-written state, not settings.
- **Codex:**
  - `tui.{alternate_screen, animations, show_tooltips, vim_mode_default, notifications, notification_method, terminal_title, keymap.*}`.
  - `notice.hide_full_access_warning` (relevant under `danger-full-access`).
  - `file_opener`, `hide_agent_reasoning`, `show_raw_agent_reasoning`, `web_search`, `tools.web_search.*`.
- **OpenCode** (`tui.json`): `theme`, `keybinds.*`, `scroll_*`, `diff_style`, `mouse`, `attention.*`, `plugin_enabled`.

## 3. Existing repositories that already hold part of this

- **CriomOS-home**: every declared setting above. The modules are split by accident of history; `codex-remote-control.nix` holds Claude's settings. It also holds the packaging (`owned-agents/claude-code`, `owned-agents/codex*`).
- **hexis**: the merge engine (`ensure`, `always`, `once`). It is what lets a declared overlay coexist with the settings each harness writes itself.
- **persona-test** (`lib/default.nix` `seatCredentialEnv`): already generates a semi-sandbox seat home from the credentials alone, as the living asked on 2026-09-26 (`flows/e167d8/vision/testRepos.md`: "copy the login credentials and then generate all the configuration details"). It writes:
  - Claude's `.credentials.json`, with `.claude.json` holding `oauthAccount`, onboarding and seat trust;
  - `settings.json` with `defaultMode=bypassPermissions`;
  - Codex's `auth.json`, with `config.toml` holding `approval_policy=never`, `sandbox_mode=danger-full-access`, `model` and seat trust.

  This is the nearest existing embryo of the requested standard.
- **flow-test** (`packages/flow-claude.nix`) and the 3ec648 capsule script (`flows/3ec648/witnesses/semi-sandbox-capsule.sh`): the same credential-only pattern, with `ENABLE_CLAUDEAI_MCP_SERVERS=false` and the three `DISABLE_*` variables.
- **flow**: the per-seat Claude `--settings` and the Codex thread overrides.
- **harness**: the harness abstraction and `flow-id`. It carries no harness configuration.

## Sources
- CriomOS-home `origin/main` at `d029e60f`: `modules/home/profiles/min/{default,codex-permission-defaults,codex-remote-control,codex-next,codex-next-candidate,herdr,opencode-harness,opencode,harness}.nix`, `owned-agents/claude-code/default.nix`, and the commits named above.
- Live files: `~/.claude/settings.json`, `~/.claude.json` (non-account keys only), `~/.codex/config.toml`, `~/.codex-next/config.toml`, `~/.codex-next-8mkkxq293hk2/config.toml`, their `hooks.json`, `~/.codex/rules/default.rules`, `~/.config/opencode/{opencode,tui}.json`, `/home/li/primary/.claude/settings*.json`, and the units `flow-nexus`, `flow-nexus-next` and `opencode`.
- Primary `tools/{claude,codex,opencode}-main-flow-launch.mjs`, `tools/native-worker-launch.mjs`, `ARCHITECTURE.md` §4–5.
- Flow `5e0b1bf`: `crates/flow-nexus/src/herdr/launch.rs`, `crates/flow-nexus/src/codex.rs`.
- hexis `README.md`; persona-test `c1a2370` `lib/default.nix`; flow-test `ac986be` `packages/flow-claude.nix`.
- Vendor: code.claude.com/docs/en/{settings,settings-reference,permissions,hooks,env-vars,memory,mcp,sandboxing,authentication,monitoring-usage,cli-reference,managed-settings}; openai/codex `ff29a4439` `codex-rs/core/config.schema.json`, `codex-rs/config/src/{loader/mod.rs,config_requirements.rs}`, `codex-rs/utils/cli/src/shared_options.rs`, `codex-rs/hooks/src/engine/discovery.rs`; opencode.ai/docs, opencode.ai/config.json, opencode.ai/tui.json.
- `flows/28d847/reports/permission-prompts.md`; psyche records as cited.
- Provenance receipt: unavailable (no PROVENANCE handoff received).
