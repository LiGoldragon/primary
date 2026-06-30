# Scout Mechanisms: Orchestration By Default Across Harnesses

## Task and scope

Investigate local implementation mechanisms for making ordinary sessions orchestration sessions by default, with the main agent interviewing, dispatching workers, and synthesizing rather than doing task work. Scope included local Codex, Pi, Claude, generated role packets, global config, hooks, prompt injection, startup instruction surfaces, and automatic LLM-model identity in commit messages. I did not edit source/config, launch subagents, inspect `private-repos/`, or inspect `repos/` contents. The only write is this assigned scout output.

## Commands and files consulted

- `AGENTS.md`, `CLAUDE.md`, `flake.nix`, `skills/generated-role-outputs.nota`
- `.codex/agents/*.toml`, `.pi/agents/*.md`, `.claude/agents/*.md`
- `.agents/skills/intent-led-orchestration/SKILL.md`, `.claude/skills/intent-led-orchestration/SKILL.md`
- `.claude/settings.json`, `/home/li/.claude/settings.json`, `/home/li/.claude/statusline.sh`
- `/home/li/.codex/config.toml`, `/home/li/.codex/prompts/helper-only.md`, `/home/li/.codex/rules/default.rules`
- `/home/li/.pi/agent/settings.json` with sensitive keys redacted by a script
- Pi package docs/source through stable symlink paths: `/home/li/.local/share/criomos/pi/package/docs/{settings.md,prompt-templates.md,skills.md,packages.md,sdk.md}` and selected files under `/home/li/.local/share/criomos/pi/package/src/`
- Pi subagents package docs/source through `/home/li/.pi/agent/packages/pi-subagents/{README.md,package.json,skills/pi-subagents/SKILL.md,agents/*.md,src/...}`
- CLI help: `codex --help`, `codex exec --help`, `codex debug prompt-input --help`, `pi --help`, `claude --help`, `jj commit --help`, `jj help -k config`, `jj help -k templates`
- Inspection commands included `rg`, `find`, `ls`, `jj status --no-pager`, `codex debug prompt-input 'probe prompt'`, and selected `jj config` queries.

## Observed facts

### Workspace and generated surfaces

- `AGENTS.md` is the workspace boot contract. It says generated worker role packets carry normal role doctrine; agents read the file and the role packet, prompt, or dispatch envelope supplied for the task. It also says additional doctrine is loaded only when named by the prompt, packet, envelope, or local repo context.
- `CLAUDE.md` contains only `@AGENTS.md`, so Claude project startup points back to the same workspace boot contract.
- `flake.nix` describes this primary workspace as generated skill surfaces and uses input `skills.url = "github:LiGoldragon/skills"`. The canonical generator/source for role packet changes is therefore not proven to be primary itself.
- `skills/generated-role-outputs.nota` lists generated role packet outputs for all three harnesses: `.claude/agents/<role>.md`, `.codex/agents/<role>.toml`, and `.pi/agents/<role>.md`.
- Generated worker role packets currently include role contracts and the child-output/edit-coordination modules. They are worker packets, not parent orchestrator packets.
- The current role packet injected into this Scout session includes a child-subagent boundary: “You are a child subagent, not the parent orchestrator,” and “Do not propose or run subagents.” That is a necessary counterweight if parent sessions become orchestration-only by default.

### Current orchestration skill

- `.agents/skills/intent-led-orchestration/SKILL.md` and `.claude/skills/intent-led-orchestration/SKILL.md` describe the existing intent-led orchestration protocol.
- The skill says it is used only at fresh-context startup when the psyche wants intent-led alignment or orchestration, and not mid-session.
- It says the orchestrator interviews, gates, dispatches, and synthesizes; never performs task work; and uses only psyche chat, psyche-pasted content, spawned agents, and worker output files.
- It requires two explicit approvals: alignment locked and method approved. A request to implement does not bypass those gates.
- Because this is a skill body, it is not necessarily loaded in full by default. Codex and Pi both expose skill metadata at startup and load full bodies on demand. A skill alone is therefore not sufficient for “every session defaults to orchestration-only” unless the harness explicitly forces that skill body or equivalent instructions into the root prompt.

### Codex mechanisms

- `codex` is installed at `/home/li/.nix-profile/bin/codex` and reports `codex-cli 0.141.0`.
- `/home/li/.codex/config.toml` exists and currently sets `developer_instructions` to the skill-read de-duplication rule, plus model and trusted project config. This proves a user-level developer-instruction surface is already active locally.
- `codex --help` and `codex exec --help` show `-c/--config <key=value>` overrides and `--profile`, `--ignore-user-config`, and prompt arguments.
- `codex debug prompt-input 'probe prompt'` showed model-visible items with a `developer` role first. That developer item contained sandbox/permissions, the user-config `developer_instructions`, app/plugin instructions, and the skills list. It also showed `/home/li/primary/AGENTS.md` inserted as a later `user` item before the actual prompt.
- The same debug output showed Codex skill metadata for `.agents/skills/*/SKILL.md`, including `intent-led-orchestration`, but not full skill bodies unless selected.
- `.codex/agents/*.toml` files exist and each includes `developer_instructions`. These are generated custom-agent/role surfaces. They do not make the root session orchestration-only by themselves.
- `/home/li/.codex/prompts/helper-only.md` exists. Its frontmatter and body make it an explicit prompt template for `$helper-only`, not an automatic startup surface.
- `/home/li/.codex/rules/default.rules` exists and contains command-prefix rules. This is execution policy, not a model-behavior instruction surface.

### Pi mechanisms

- `pi` is installed at `/home/li/.nix-profile/bin/pi` and reports `0.80.2`.
- `pi --help` exposes `--system-prompt <text>` and `--append-system-prompt <text>`, plus resource flags for extensions, skills, prompt templates, context files, and project trust.
- Pi docs at `/home/li/.local/share/criomos/pi/package/docs/settings.md` say global settings live in `~/.pi/agent/settings.json`; project settings live in `.pi/settings.json`; and project trust controls project-local resources.
- Local `/home/li/.pi/agent/settings.json` has active packages including `packages/pi-subagents` and `packages/pi-continue`. It sets default provider/model fields, but it does not contain a native always-append system prompt setting in the documented settings list.
- Pi docs at `/home/li/.local/share/criomos/pi/package/docs/skills.md` say skills are scanned at startup and advertised in the system prompt; full `SKILL.md` is loaded on demand by reading the skill file, and `/skill:name` can force a skill.
- Pi docs at `/home/li/.local/share/criomos/pi/package/docs/prompt-templates.md` say prompt templates are invoked with slash commands and loaded from global/project/package/settings/CLI surfaces. They are not automatic instructions.
- Pi source at `/home/li/.local/share/criomos/pi/package/src/core/system-prompt.ts` builds the system prompt from a custom prompt, append-system-prompt text, context files, and skills. Context files are appended under project context. Skills are appended only as available skills metadata when the read tool is available.
- Pi source at `/home/li/.local/share/criomos/pi/package/src/core/extensions/types.ts` defines a `before_agent_start` extension event that receives the raw prompt and fully assembled system prompt.
- Pi source at `/home/li/.local/share/criomos/pi/package/src/core/extensions/runner.ts` lets extensions return an updated `systemPrompt` and custom messages during `before_agent_start`.
- Pi source at `/home/li/.local/share/criomos/pi/package/src/core/agent-session.ts` applies `before_agent_start` modifications immediately before sending a user prompt to the model.
- The active `pi-subagents` package declares an extension, skills, and prompts in `/home/li/.pi/agent/packages/pi-subagents/package.json`.
- `pi-subagents` docs say Pi is the parent session and subagents are child Pi sessions. It explicitly recommends orchestration as parent-agent guidance, not a runtime workflow mode.
- `pi-subagents` has a parent-only skill at `/home/li/.pi/agent/packages/pi-subagents/skills/pi-subagents/SKILL.md`. It tells the parent to use `subagent`, select roles, keep one writer, choose fresh vs forked context, and synthesize child results.
- `pi-subagents` child runtime source at `/home/li/.pi/agent/packages/pi-subagents/src/runs/shared/subagent-prompt-runtime.ts` injects child boundary instructions into children, strips parent-only subagent artifacts, and prevents normal children from receiving the `pi-subagents` orchestration skill. This is strong local evidence that parent/child role separation is already implemented in Pi.
- `pi-subagents` `buildPiArgs` source passes child instructions through `--system-prompt` or `--append-system-prompt` files and controls child tool availability and model selection. It sets `PI_SUBAGENT_CHILD=1` and related environment variables.

### Claude mechanisms

- `claude` is installed at `/home/li/.nix-profile/bin/claude` and reports `2.1.185 (Claude Code)`.
- `claude --help` exposes `--append-system-prompt <prompt>`, `--system-prompt <prompt>`, `--agent <agent>`, `--agents <json>`, `--settings <file-or-json>`, `--setting-sources`, `--tools`, `--allowedTools`, `--disallowedTools`, `--permission-mode`, `--bare`, `--safe-mode`, and `--worktree`.
- `/home/li/primary/.claude/settings.json` defines a `PreToolUse` hook for `Write|Edit` that emits a Rust-source reminder. This hook fires on matching tool use; it does not insert root orchestration instructions before the first user prompt.
- `/home/li/.claude/settings.json` sets model, effort, status line command, permissions, and disabled auto-memory env. It does not currently define an always-orchestrate prompt.
- `/home/li/.claude/statusline.sh` receives JSON containing `.model.display_name` or `.model.id` and displays it. This proves Claude Code can expose model identity to a statusline command, but not that ordinary shell commands or `jj commit` automatically receive it.
- `.claude/agents/*.md` are generated worker agent packets. Claude help confirms `--agent` and `--agents` can select/define agents for the current session, but those generated worker packets are not root-session universal instructions.

### Commit message and model identity facts

- `jj commit --help` exposes `-m/--message <MESSAGE>` and does not show a hook option that can rewrite the commit description at commit time.
- `jj help -k config` documents `[templates] commit_trailers`, which can automatically add or deduplicate trailer lines based on Jujutsu template expressions.
- `jj help -k templates` documents `config(name)` lookup, but I found no template function for reading arbitrary environment variables.
- Current `jj config list` scoped searches did not show existing commit-description, trailer, hook, or alias configuration in this checkout.
- Current role and skill doctrine for `jj`, `repository-closeout`, and `repo-operator` says to use concise imperative commit messages and inline `jj commit -m`, but does not require an LLM model trailer.
- Pi session format docs include provider/model on assistant messages, and `pi-subagents` results track `model` in run metadata. Claude statusline input includes model. Codex config/debug prompt reveals the configured model. These are harness-specific sources, not a unified automatic commit-message source.

## Interpretations

### Can orchestration be auto-loaded into the first user prompt or developer instructions?

Yes, but developer/system-level insertion is safer than first-user-prompt insertion.

- Codex: use `/home/li/.codex/config.toml` `developer_instructions` for personal global default, or a project `.codex/config.toml` for checked-in project-specific behavior. `codex debug prompt-input` proves this lands in a developer message before AGENTS and the user prompt. First-user-prompt prepending is possible through wrapper scripts or shell aliases but would be lower priority and more easily confused with the user’s task content.
- Pi: use a launch wrapper with `--append-system-prompt` or an extension handling `before_agent_start` to modify the assembled system prompt. The extension path is the strongest Pi-native mechanism because it can apply after context/skills are assembled and before the model call. Prompt-template expansion is explicit and not enough for a default. A settings-only solution is not proven because Pi docs list `--append-system-prompt` as CLI, not a settings key.
- Claude: use a launch wrapper or orchestrate/harness spawn adapter passing `--append-system-prompt` or `--system-prompt`, or select a root `--agent`/`--agents` definition for the parent session. Project `CLAUDE.md`/`AGENTS.md` can carry a fallback but is lower-priority and not harness-specific.

### Where should this live?

Recommended home is harness launch/config plus a small generated parent packet, not AGENTS alone and not generated worker packets alone.

1. Create a compact “parent orchestrator default” instruction packet equivalent to the current `intent-led-orchestration` rules, but tuned for default use and with explicit bypass/escape hatch language.
2. Inject that packet at launch time for root sessions through each harness’s strongest startup surface:
   - Codex: user/project `developer_instructions` or a dedicated Codex profile selected by the launch wrapper.
   - Pi: a small trusted global/package extension using `before_agent_start`, or a wrapper adding `--append-system-prompt`.
   - Claude: wrapper/spawn adapter adding `--append-system-prompt` or selecting a root agent.
3. Keep generated worker role packets as child/worker packets and preserve the child boundary. Do not add parent-orchestrator-only rules to every worker role packet.
4. Keep `AGENTS.md` as a minimal cross-harness statement and pointer, not the sole enforcement mechanism. It is visible in primary, but it is lower-priority than harness developer/system prompts and also read by child workers unless filtered.
5. Keep the `intent-led-orchestration` skill as the durable reusable doctrine source, but do not rely on skill progressive disclosure for default activation. Either force-load its body into the parent prompt or generate a compact parent packet from the same source.

### Risk of making every session orchestration-only

- high: If injected through `AGENTS.md` only, child workers may inherit parent-only rules and refuse assigned work. Pi already mitigates this via child boundary injection and skill stripping; Codex/Claude generated worker packets need equivalent precedence.
- high: If the root session lacks a subagent/agent-launch tool, “orchestration-only” can deadlock: the model is forbidden to do work but has no worker dispatch mechanism.
- high: The current `intent-led-orchestration` skill requires two explicit psyche approvals. Making that universal will add latency and may feel broken for trivial questions, emergency fixes, or commands where the user explicitly expects direct action.
- medium: Parent no-inspection means validation must be delegated. This is good for context preservation but weaker for immediate trust unless worker outputs have structured evidence and a separate reviewer.
- medium: Prompt-injection or project-local files can try to override orchestration. Developer/system-level insertion and child boundaries reduce but do not eliminate this.
- medium: Cost and latency increase because even small work may require worker startup and synthesis.
- medium: Recursion and fanout risk unless child packets explicitly say not to launch subagents and the runtime enforces depth/tool limits. Pi has local evidence for this; Codex/Claude need validation.
- low/medium: Users may need an explicit direct-work escape hatch for maintenance, debugging broken subagent infrastructure, or simple conversational answers.

### Model identity in commit messages

Feasible as role doctrine; only partly feasible as pure automatic VCS behavior.

- Jujutsu `commit_trailers` can add static trailers from config, but I did not find a way for a Jujutsu template to read the current harness model from the environment. It can read `config(name)`, so a static `ai.model` config key could be appended, but that will become stale when the model changes.
- Harness wrappers can set an environment variable such as `LLM_MODEL_ID` and a custom commit helper can append `LLM-Model: $LLM_MODEL_ID` to the `jj commit -m` text. This requires agents to use the helper instead of raw `jj commit`.
- Repo-operator doctrine can require a trailer such as `LLM-Model: <provider/model>` and tell the operator where to obtain it per harness: Codex from configured/session model, Pi from session/subagent metadata or model setting, Claude from statusline/session model. This is implementable without VCS internals but depends on model honesty and operator compliance.
- Best implementation path is a hybrid: update repo-operator/repository-closeout doctrine to require a model trailer when known, and later add a small wrapper/helper to make the trailer easy. Do not try to make raw `jj commit` infer dynamic harness model identity without a wrapper or config bridge.

## Recommended implementation path

1. Define one compact root-parent packet named something like `orchestration-default-parent`, generated from the same doctrine as `intent-led-orchestration` but with default-session language. It should state: parent interviews/frames; parent dispatches for task work; parent does not read files/links/status directly; parent synthesizes only from psyche chat and worker outputs; child packets override parent rules; direct-work escape hatch exists only when launched under a non-orchestrator profile or when subagent infrastructure is unavailable.
2. Implement per-harness launch injection, not first-prompt prepending:
   - Codex: add/select a profile or config layer that sets `developer_instructions` to the parent packet. Validate with `codex debug prompt-input`.
   - Pi: prefer a small global/package extension using `before_agent_start` for root sessions and skipping when `PI_SUBAGENT_CHILD=1`; alternatively use a wrapper that passes `--append-system-prompt <file>`. Validate with a non-mutating prompt or extension unit test.
   - Claude: create/use a wrapper or orchestrate spawn adapter that passes `--append-system-prompt` for root sessions and does not pass it to spawned worker agents. Validate wrapper argv and a harmless `--help`/debug smoke; behavioral validation can require a model call.
3. Keep generated worker role packets unchanged except to strengthen child-boundary language where needed. Do not make all `.claude/agents`, `.codex/agents`, or `.pi/agents` orchestration parents.
4. Add a minimal `AGENTS.md` pointer only after the harness-level mechanism exists, for cross-harness human readability and fallback. Avoid detailed universal orchestration rules in `AGENTS.md` that children will accidentally inherit.
5. Add repo-operator doctrine for `LLM-Model:` commit trailers when known. Initially make it explicit role behavior; later add a `jj-ai-commit` or harness-provided commit helper if strict automation is desired.

## Validation methods

- Codex static validation: `codex debug prompt-input 'probe'` and assert the orchestration packet appears in the first developer item, before `AGENTS.md` and before the user prompt.
- Codex bypass validation: run the same debug command with `--ignore-user-config` or alternate profile to ensure the escape hatch actually omits the packet.
- Pi static/unit validation: unit-test a root `before_agent_start` extension with and without `PI_SUBAGENT_CHILD=1`, verifying it injects into root system prompts and skips child sessions.
- Pi runtime validation: start a trusted non-mutating session with a sentinel instruction and use logs/session export or a controlled prompt to confirm the parent uses `subagent` for inspection instead of `read`/`bash` itself.
- Claude wrapper validation: inspect wrapper argv or debug logs to confirm `--append-system-prompt` is passed for root sessions and absent for worker sessions. Confirm `claude --help` still exposes the expected flags.
- Cross-harness behavioral validation: ask the root parent to answer a local-code question requiring file inspection. Acceptance: parent launches a Scout worker; parent does not call file/system tools; final answer cites the worker output path; worker role packet contains child boundary and can inspect files.
- Generated-surface validation: run the existing generated-skill check (`nix run .#check-skills` or equivalent) after generator changes; verify `skills/generated-role-outputs.nota` still lists only worker outputs unless a separate parent packet output is intentionally added.
- Commit trailer validation: make a disposable test commit in an isolated repo or dry-run helper; verify description contains a single `LLM-Model: provider/model` trailer and repeated amend/commit helper use does not duplicate it.

## Blockers and unknowns

- medium: I did not inspect the canonical `LiGoldragon/skills` source repo or generator implementation because `repos/` is out of this scout scope. Implementers need to locate and edit the canonical source, not hand-edit generated primary outputs.
- medium: I did not inspect private or external harness launcher repositories/configuration. If actual root sessions are launched by an orchestrate/harness daemon outside primary, the correct injection point may be that spawn adapter rather than user dotfiles.
- medium: Codex root sessions have a proven developer-instruction surface, but this Scout did not prove a root Codex subagent launch tool is available in every local harness mode. Orchestration-only default must not be enabled where no dispatch mechanism exists.
- medium: Claude behavioral validation may require an actual model call or debug logs not run here. Help proves flags, not prompt visibility.
- low/medium: Global user config files are personal state. A checked-in implementation should prefer declarative Home Manager/CriomOS-home or harness spawn configuration if reproducibility across machines matters.
- low: The working copy was already dirty before this Scout, and final status showed additional unrelated agent-output files that may have appeared concurrently. I did not inspect unrelated dirty entries beyond `jj status --no-pager`.

## Review findings

- no blocker: Codex has a proven high-priority `developer_instructions` insertion surface at `/home/li/.codex/config.toml`; `codex debug prompt-input` confirms visibility.
- no blocker: Pi has proven CLI `--append-system-prompt` and extension `before_agent_start` mechanisms; local `pi-subagents` already demonstrates parent/child prompt rewriting.
- no blocker: Claude has proven launch flags `--append-system-prompt`, `--system-prompt`, `--agent`, and `--agents` by `claude --help`.
- high: Do not implement default orchestration only in `AGENTS.md`; it is lower-priority than harness system/developer prompts and will also be seen by child workers.
- high: Do not add parent orchestration rules to every generated worker role packet; workers need the opposite child boundary.
- high: Do not enable orchestration-only default in a harness mode until worker dispatch is available and validated.
- medium: Do not rely on prompt templates (`/helper-only`, Pi prompt templates) for automatic startup behavior; local docs/help show explicit invocation semantics.
- medium: Commit-message model identity should start as repo-operator doctrine or a commit helper, not raw `jj` magic; dynamic model identity is harness-specific and not currently exposed to `jj commit`.

## Residual risks

- Prompt obedience is not a formal security boundary; model behavior still needs runtime/tooling enforcement where possible.
- Project-local trust modes can skip Pi/Codex project resources, so global or launcher-level injection has higher coverage than project files.
- Claude safe/bare modes can disable customizations or context discovery; wrappers need explicit tests for those modes if used.
- Model identity can be ambiguous when a session switches models, uses fallback models, or multiple workers contribute to one commit. Doctrine must define whether the trailer records the committer/operator model, implementer model(s), or all material worker models.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings cite Codex (/home/li/.codex/config.toml, codex debug prompt-input), Pi (/home/li/.local/share/criomos/pi/package docs/source, /home/li/.pi/agent/settings.json, /home/li/.pi/agent/packages/pi-subagents), Claude (.claude/settings.json, /home/li/.claude/settings.json, claude --help), generated role outputs (skills/generated-role-outputs.nota), and Jujutsu commit mechanisms (jj commit/help config/templates), with severity-tagged review findings."
    }
  ],
  "changedFiles": [
    "agent-outputs/OrchestrationDefaultMechanisms/Scout-Mechanisms.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "pwd && ls -la && find .. -maxdepth 2 -name AGENTS.md -print",
      "result": "passed",
      "summary": "Confirmed cwd /home/li/primary and local AGENTS surfaces."
    },
    {
      "command": "jj status --no-pager",
      "result": "passed",
      "summary": "Initial status showed the working copy was already dirty before writing this report."
    },
    {
      "command": "rg --files -g '!*private-repos*' -g '!repos/**' -g '!private-repos/**'",
      "result": "passed",
      "summary": "Scoped file inventory without private-repos or repos contents."
    },
    {
      "command": "find .codex .pi .claude .agents skills orchestrate protocols tools -maxdepth 4 -type f ...",
      "result": "passed",
      "summary": "Listed local generated role, skill, and harness-adjacent files."
    },
    {
      "command": "codex --help; codex exec --help; codex debug prompt-input --help; codex debug prompt-input 'probe prompt'",
      "result": "passed",
      "summary": "Confirmed Codex config/developer prompt insertion and AGENTS/skills visibility."
    },
    {
      "command": "pi --help; claude --help; codex --version; pi --version; claude --version",
      "result": "passed",
      "summary": "Confirmed installed CLI versions and prompt/system/agent flags."
    },
    {
      "command": "Read selected Pi docs/source under /home/li/.local/share/criomos/pi/package and pi-subagents under /home/li/.pi/agent/packages/pi-subagents",
      "result": "passed",
      "summary": "Confirmed Pi settings/resources, system prompt construction, extension before_agent_start, and subagent child-boundary rewriting."
    },
    {
      "command": "jj commit --help; jj help -k config; jj help -k templates",
      "result": "passed",
      "summary": "Confirmed Jujutsu commit message/trailer mechanisms and lack of observed dynamic env-based model identity support."
    },
    {
      "command": "test -f /home/li/primary/agent-outputs/OrchestrationDefaultMechanisms/Scout-Mechanisms.md && wc -c /home/li/primary/agent-outputs/OrchestrationDefaultMechanisms/Scout-Mechanisms.md",
      "result": "passed",
      "summary": "Verified the required output file exists."
    },
    {
      "command": "jj status --no-pager | sed -n '1,80p'",
      "result": "passed",
      "summary": "Final status showed this output plus unrelated dirty files; no source/config edits by this Scout."
    }
  ],
  "validationOutput": [
    "Codex debug prompt showed user-config developer_instructions in a developer item before AGENTS/user prompt.",
    "Pi source shows before_agent_start extensions can modify systemPrompt before the agent loop.",
    "Claude help shows --append-system-prompt/--system-prompt and --agent/--agents surfaces.",
    "Pi-subagents source shows child boundary injection and stripping of parent-only orchestration skill/artifacts."
  ],
  "residualRisks": [
    "medium: canonical skills generator/source repo was not inspected; generated outputs in primary should not be hand-edited as source of truth.",
    "medium: actual orchestrate/harness launch adapters outside primary were not inspected.",
    "medium: Claude prompt visibility was inferred from help flags, not debug-prompt output.",
    "medium: Codex/Pi/Claude model identity is harness-specific and not currently proven available to raw jj commit templates."
  ],
  "noStagedFiles": true,
  "diffSummary": "Scout only; wrote agent-outputs/OrchestrationDefaultMechanisms/Scout-Mechanisms.md and made no source/config changes.",
  "reviewFindings": [
    "no blocker: developer/system prompt insertion surfaces exist for Codex, Pi, and Claude.",
    "high: AGENTS.md alone is the wrong enforcement point for orchestration-only default because children also read it and it is lower-priority than harness developer/system instructions.",
    "high: generated worker role packets must retain child boundaries and must not all become parent orchestrators.",
    "high: orchestration-only default must not be enabled in harness modes without a validated worker-dispatch mechanism.",
    "medium: prompt templates and skills are useful doctrine surfaces but are not automatic default activation surfaces by themselves.",
    "medium: model identity in commit messages is feasible via repo-operator doctrine or commit helper, not proven as raw automatic jj behavior."
  ],
  "manualNotes": "Recommended path: implement a compact root-parent orchestration packet through harness launch/config surfaces, keep worker role packets child-only, use AGENTS as a pointer/fallback, and add LLM-Model commit trailer doctrine before attempting stricter commit-helper automation."
}
```
