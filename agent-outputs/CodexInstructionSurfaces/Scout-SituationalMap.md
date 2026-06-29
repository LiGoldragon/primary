# Scout Situational Map: Codex Instruction Surfaces

## Task and scope

Investigate accessible, local mechanisms for Codex-facing instructions that load in new Codex sessions, specifically to place a rule that complete pasted `<skill name=... location=...>...</skill>` blocks count as already loaded and should not be re-read from disk.

Scope was local/public workspace and user Codex configuration. I did not inspect `private-repos/`, patch Codex internals, edit source/config, commit, or push. This file is the only written artifact.

## Files and commands consulted

- Read project startup instructions from `/home/li/primary/AGENTS.md` via the supplied context.
- Inspected local Codex/user surfaces: `/home/li/.codex/config.toml`, `/home/li/primary/.codex/agents/scout.toml`, `/home/li/primary/AGENTS.md`, `/home/li/primary/.agents/skills/*/SKILL.md` listings.
- Consulted local Codex docs cache: `/tmp/openai-docs-cache/codex-manual.md` sections on `AGENTS.md`, config precedence, project config, skills, team config, and subagents/custom agents.
- Commands run included `find`, `rg`, `codex --help`, `codex exec --help`, `codex debug prompt-input --help`, `codex debug prompt-input ...`, `wc -c`, and `jj status --no-pager`.

## Observed facts

### Automatically loaded / plausibly automatic surfaces

1. **Global Codex `AGENTS.md` is documented but absent locally.** Docs at `/tmp/openai-docs-cache/codex-manual.md:7581-7591` say Codex reads `AGENTS.md` files before work; global scope is `$CODEX_HOME` (default `~/.codex`) using `AGENTS.override.md` first, otherwise `AGENTS.md`. Local check `ls -la ~/.codex/AGENTS.md ~/.codex/AGENTS.override.md` reported both missing.

2. **Project `AGENTS.md` is auto-loaded in this repo.** Docs at `/tmp/openai-docs-cache/codex-manual.md:7587-7591` say project scope walks from project root to cwd, loading `AGENTS.override.md`, `AGENTS.md`, then configured fallbacks, capped by `project_doc_max_bytes`. Local `codex debug prompt-input "Probe instruction sources only."` produced a model-visible user item beginning `# AGENTS.md instructions for /home/li/primary`; it included `/home/li/primary/AGENTS.md`. `wc -c AGENTS.md` reported 3152 bytes, well below the documented/default 32768 byte cap.

3. **User config exists and supports a stronger instruction hook.** `/home/li/.codex/config.toml` exists and currently sets model/trust/plugins but has no `developer_instructions`. Docs at `/tmp/openai-docs-cache/codex-manual.md:3068-3093` list `developer_instructions = ""` as "Additional user instructions are injected before AGENTS.md." A read-only injection probe, `codex debug prompt-input -c 'developer_instructions="TEST_DUPLICATE_SKILL_CARVEOUT"' "Probe."`, placed the string in model-visible item `0` with role `developer`, before app/skills instructions.

4. **Project `.codex/config.toml` would auto-load for trusted projects, but is absent here.** Docs at `/tmp/openai-docs-cache/codex-manual.md:2165-2183` say Codex reads `.codex/config.toml` from project root to cwd in trusted projects; `/home/li/.codex/config.toml` marks `/home/li/primary` trusted; local `test -f .codex/config.toml || echo no .codex/config.toml` reported absent.

5. **Repo `.codex/agents/*.toml` files are custom agent role prompts, not root-session universal instructions.** Local `find .codex -maxdepth 2 -type f` found ten role files, e.g. `.codex/agents/scout.toml`. Docs at `/tmp/openai-docs-cache/codex-manual.md:12371-12380` say custom agents live under `~/.codex/agents/` or `.codex/agents/` and load as configuration layers for spawned sessions. The debug prompt for the root session did not contain `.codex/agents` or `developer_instructions` from those files.

6. **Repo and system skills are visible by metadata every session; full skill bodies are not.** Docs at `/tmp/openai-docs-cache/codex-manual.md:7345-7349` say skills use progressive disclosure: initial context contains name, description, and path, and full `SKILL.md` loads only when selected. Local debug prompt showed `<skills_instructions>`, system skill paths under `/home/li/.codex/skills/.system/...`, and repo skill paths under `/home/li/primary/.agents/skills/...`. Local `find .agents/skills -maxdepth 2 -name SKILL.md | wc -l` reported 55 repo skills.

7. **The built-in skills instruction currently pushes disk reads.** The debug prompt includes: after deciding to use a skill, "the main agent must read its `SKILL.md` completely" and for `file` entries, "open the listed path." This is why a carveout should be phrased as a definition of already-loaded skill content, not as a bare refusal to follow skill loading.

8. **Custom prompts are not an automatic instruction surface.** Docs at `/tmp/openai-docs-cache/codex-manual.md:7713-7718` say custom prompts are deprecated, require explicit invocation, and live in the local Codex home. Local `/home/li/.codex/prompts/helper-only.md` exists, but no evidence indicates it auto-loads in every new session.

9. **Rules are execution policy, not the right behavior-instruction surface.** `/home/li/.codex/rules/default.rules` exists, and docs describe rules as command/sandbox policy rather than model instruction content. I did not find local evidence that `.rules` is suitable for skill-read semantics.

## Interpretations and confidence

- **Highest-confidence automatic shared surface for this repo:** `/home/li/primary/AGENTS.md` (confirmed by `codex debug prompt-input`; documented). It is lower priority than developer/system skills instructions but appears every ordinary primary-root session.
- **Highest-confidence controllable per-user surface:** `/home/li/.codex/config.toml` `developer_instructions` (confirmed by docs and `-c developer_instructions=...` prompt-input probe). It lands in the model-visible developer message, stronger than `AGENTS.md`, for sessions using this `CODEX_HOME` and not replacing/ignoring the relevant config.
- **Best checked-in Codex-specific config surface:** `/home/li/primary/.codex/config.toml` if created. Docs say trusted project config auto-loads; primary is trusted in `/home/li/.codex/config.toml`. This would be repo-controlled but only applies in trusted project sessions and may not apply if project `.codex` layers are skipped.
- **Generated `.codex/agents/*.toml` files are necessary coverage for spawned custom agents if their `developer_instructions` replace parent/global developer instructions.** Docs say each custom agent file must define `developer_instructions` and acts as a config layer; I did not validate inheritance/merging for spawned children because spawning subagents was outside the scout role. Treat global config coverage of custom-agent children as plausible but not proven.
- **Skills are not the right place for an always-load rule.** Skill metadata is automatic, but body rules are only loaded when the skill is selected; a duplicate-read carveout must be visible before the decision to read a skill body.

## Answers to the requested questions

1. **What Codex-facing instruction surfaces exist locally, and which plausibly load automatically every new Codex session?**
   - `/home/li/.codex/config.toml`: loads as user config; can carry `developer_instructions`; automatic for this `CODEX_HOME`. Confidence: high from docs/help/probe.
   - `/home/li/.codex/AGENTS.md` or `AGENTS.override.md`: documented automatic global instruction files, but absent. Confidence: high that mechanism exists; none currently active locally.
   - `/home/li/primary/AGENTS.md`: active project instruction file; confirmed in prompt input. Confidence: high for primary sessions.
   - `/home/li/primary/.codex/config.toml`: documented project config surface but absent. Confidence: high if created and project trusted.
   - `/home/li/primary/.codex/agents/*.toml`: custom spawned-agent role files; not root-session automatic. Confidence: high.
   - `/home/li/primary/.agents/skills/*/SKILL.md`, `/home/li/.codex/skills/.system/*/SKILL.md`, plugin skills: metadata automatic; full body only selected. Confidence: high.

2. **Is there a global/per-user mechanism we can control, or only per-repo AGENTS / generated `.codex` surfaces?**
   - Yes, there are global/per-user mechanisms: `$CODEX_HOME/config.toml` with `developer_instructions`, and `$CODEX_HOME/AGENTS.md` or `AGENTS.override.md`. Locally `$CODEX_HOME` defaults to `/home/li/.codex`; config exists, global AGENTS files do not.

3. **Where should the duplicate skill-read carveout be placed for maximum chance Codex sees it every session?**
   - Recommended maximum-coverage path:
     1. Add it to `/home/li/.codex/config.toml` as `developer_instructions` for all personal Codex sessions using this `CODEX_HOME`.
     2. Also put the same sentence in generated Codex custom-agent role source so regenerated `/home/li/primary/.codex/agents/*.toml` include it, covering spawned roles if custom-agent `developer_instructions` replace inherited/global instructions.
     3. Add a short fallback in `/home/li/primary/AGENTS.md` or a new checked-in `/home/li/primary/.codex/config.toml` if the rule should travel with this workspace rather than only this user. Prefer `.codex/config.toml` for Codex-specific developer-level injection; prefer `AGENTS.md` for cross-harness/project guidance.

4. **Exact concise wording to add:**

   `Skill-read de-duplication: A complete pasted <skill name=... location=...>...</skill> block counts as that skill already loaded for this session. Do not read the same skill location again unless the block is incomplete, conflicts with higher-priority instructions, or the user explicitly asks to verify the file.`

5. **What validation is possible?**
   - Static/model-input validation: run `codex debug prompt-input -c 'developer_instructions="<sentinel>"' "Probe."` or after editing config run `codex debug prompt-input "Probe."` and verify the rule appears in the developer item before `AGENTS.md`.
   - Instruction-source validation: run `codex --ask-for-approval never "Summarize the current instructions."` from `/home/li/primary` and confirm it reports global/user plus project sources, matching docs.
   - Behavioral validation: run `codex exec --json` with a prompt containing a complete pasted fake skill block and ask Codex to use that skill without reading disk; inspect JSONL for absence of file-read tool calls for that location. This validates obedience but is model-behavior evidence, not a guaranteed formal contract.
   - Spawned-agent validation: after adding to generated custom agents, spawn one custom role and inspect its initial instructions or ask it to summarize the rule. I did not run this because scout instructions prohibit launching subagents.

## Likely relevant files

- `/home/li/.codex/config.toml` — current per-user config; best personal insertion point.
- `/home/li/.codex/AGENTS.md` — absent; documented global instruction file if created.
- `/home/li/.codex/AGENTS.override.md` — absent; documented global override if created.
- `/home/li/primary/AGENTS.md` — current project boot contract; confirmed loaded.
- `/home/li/primary/.codex/config.toml` — absent; potential checked-in Codex-specific project config.
- `/home/li/primary/.codex/agents/*.toml` — generated custom subagent role surfaces.
- `/home/li/primary/.agents/skills/*/SKILL.md` — repo skills; metadata auto-visible, full body selected-on-demand.

## Unknowns and residual risks

- Whether custom spawned agents merge parent/global `developer_instructions` with their own `.codex/agents/*.toml` `developer_instructions` was not validated. Severity: medium for subagent coverage.
- `developer_instructions` insertion currently appears before built-in `<skills_instructions>` in `codex debug prompt-input`; the built-in later skill text still says to open the listed file. Severity: medium. Wording should define the pasted block as already-loaded rather than directly contradicting skill loading.
- Sessions launched with a different `CODEX_HOME`, with `--ignore-user-config`, from untrusted projects, or with instruction-replacing flags/files may miss some surfaces. Severity: medium.
- Behavioral compliance can be tested but not guaranteed because Codex internals are closed and model behavior is probabilistic. Severity: low/medium after prompt-input validation.

## Review findings

- No blockers for implementing the rule through accessible Codex configuration/instruction surfaces.
- Medium: root `AGENTS.md` alone is lower priority than Codex's built-in skills instruction, so using only `/home/li/primary/AGENTS.md` is weaker than `developer_instructions`.
- Medium: generated custom-agent role coverage needs follow-up validation because `.codex/agents/*.toml` files define their own `developer_instructions`.

## Checks run and results

- `codex debug prompt-input "Probe instruction sources only."`: passed; showed three model-visible items, including a developer item with skills metadata and a user item containing `# AGENTS.md instructions for /home/li/primary`.
- `codex debug prompt-input -c 'developer_instructions="TEST_DUPLICATE_SKILL_CARVEOUT"' "Probe."`: passed; sentinel appeared in model-visible developer item.
- `ls -la ~/.codex/AGENTS.md ~/.codex/AGENTS.override.md ~/.codex/skills`: passed with expected missing-file errors for both global AGENTS files and listed `~/.codex/skills`.
- `find .codex -maxdepth 2 -type f`: passed; found only generated custom agent TOML files and no `.codex/config.toml`.
- `jj status --no-pager`: passed before writing this report; working copy had no changes at that point.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings name /home/li/.codex/config.toml, /home/li/primary/AGENTS.md, /home/li/primary/.codex/agents/*.toml, /home/li/primary/.agents/skills/*/SKILL.md, and local Codex manual sections; severities are listed under reviewFindings and residualRisks."
    }
  ],
  "changedFiles": [
    "agent-outputs/CodexInstructionSurfaces/Scout-SituationalMap.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "find .codex -maxdepth 2 -type f -print | sort",
      "result": "passed",
      "summary": "Found generated custom agent TOML files; no project .codex/config.toml."
    },
    {
      "command": "codex --help; codex exec --help; codex debug prompt-input --help",
      "result": "passed",
      "summary": "Confirmed CLI config flags, exec behavior, and prompt-input debug surface."
    },
    {
      "command": "codex debug prompt-input \"Probe instruction sources only.\"",
      "result": "passed",
      "summary": "Rendered model-visible prompt; confirmed skills metadata and /home/li/primary/AGENTS.md instructions are present."
    },
    {
      "command": "codex debug prompt-input -c 'developer_instructions=\"TEST_DUPLICATE_SKILL_CARVEOUT\"' \"Probe.\"",
      "result": "passed",
      "summary": "Confirmed developer_instructions injection appears in the developer item."
    },
    {
      "command": "ls -la ~/.codex/AGENTS.md ~/.codex/AGENTS.override.md ~/.codex/skills",
      "result": "passed",
      "summary": "Confirmed global AGENTS files are absent and user skills directory exists."
    },
    {
      "command": "jj status --no-pager",
      "result": "passed",
      "summary": "Before writing this report, working copy had no changes."
    }
  ],
  "validationOutput": [
    "codex debug prompt-input showed item 1 role=user begins '# AGENTS.md instructions for /home/li/primary'.",
    "codex debug prompt-input with -c developer_instructions sentinel showed the sentinel in item 0 role=developer.",
    "Local docs state global ~/.codex/AGENTS.md / AGENTS.override.md and project AGENTS.md discovery, capped by project_doc_max_bytes."
  ],
  "residualRisks": [
    "medium: custom spawned-agent inheritance/merge behavior for global developer_instructions was not validated.",
    "medium: developer_instructions appears before built-in skills instructions, so wording must define pasted complete blocks as already-loaded rather than contradicting skill loading.",
    "medium: alternate CODEX_HOME, --ignore-user-config, untrusted project state, or instruction replacement flags can bypass some recommended surfaces."
  ],
  "noStagedFiles": true,
  "diffSummary": "Investigation only; created the scout output report and made no source/config changes.",
  "reviewFindings": [
    "no blockers",
    "medium: /home/li/primary/AGENTS.md alone is lower priority than Codex's built-in skill-loading instructions; prefer developer_instructions for the primary carveout.",
    "medium: generated .codex/agents/*.toml role prompts should be updated or validated for spawned custom-agent coverage."
  ],
  "manualNotes": "Recommended implementation path: add the concise skill-read de-duplication rule to /home/li/.codex/config.toml developer_instructions for personal global coverage, mirror it into generated Codex custom-agent role instructions for spawned roles, and optionally add a short project fallback in /home/li/primary/AGENTS.md or a checked-in /home/li/primary/.codex/config.toml."
}
```
