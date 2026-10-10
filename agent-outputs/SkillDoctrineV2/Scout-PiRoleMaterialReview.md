# Pi Role Material Review Scout Map

## Task And Scope

Task: inspect Pi bundled subagent roles as source material for `SkillDoctrineV2`, without accepting them as doctrine or displacing generated project roles.

Scope checked:
- CriomOS package wrapper at `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-subagents/default.nix`.
- CriomOS pin in `/git/github.com/LiGoldragon/CriomOS-home/flake.nix` and `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`.
- Local patches in `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-subagents/`.
- Pinned npm tarball `https://registry.npmjs.org/pi-subagents/-/pi-subagents-0.31.0.tgz`, especially `package/agents/*.md`, `package/src/agents/agents.ts`, `package/src/agents/agent-selection.ts`, `package/src/shared/utils.ts`, `package/README.md`, and `package/package.json`.
- Generated project roles in `/home/li/primary/.pi/agents/`.
- User Pi settings at `/home/li/.pi/agent/settings.json`.

No edits were made outside this output file. No tests were run. I did not run live Pi `/subagents` commands, inspect `/nix/store`, inspect `private-repos/`, or validate the tarball `narHash`; the review relies on the lock entry, package source, generated role files, and discovery code.

## Observed Facts

CriomOS installs `pi-subagents` version `0.31.0` from the npm tarball pinned in `flake.lock` with `narHash` `sha256-EmDqAPVqJ6hxuA3Yj8SikM2kA/oI6D1QEe/gPvJbIVw=`. The wrapper extracts `${inputs.pi-subagents-src}` and applies two local patches: `agent-chain-clarify-opt-in.patch` changes clarify behavior in `src/extension/schemas.ts` and `src/runs/foreground/chain-execution.ts`; `slim-parent-skill.patch` rewrites `skills/pi-subagents/SKILL.md`. The patches do not replace `package/agents/*.md`.

The bundled roles are loaded as Pi `builtin` agents from `BUILTIN_AGENTS_DIR` in `package/src/agents/agents.ts`. Discovery merges agents in this order: builtins, package agents, then user/project agents. With default `agentScope: "both"`, user agents are applied before project agents, so project agents win runtime-name collisions. README confirms builtins are lowest priority and project definitions win collisions.

`/home/li/.pi/agent/settings.json` lists `packages/pi-subagents` in `"packages"`, but has no visible `subagents.agentOverrides`, `disableBuiltins`, or project `.pi/settings.json` override in `/home/li/primary/.pi/`. Therefore unshadowed bundled builtins can appear at startup.

Generated project roles under `/home/li/primary/.pi/agents/` are:
- `criomos-implementer`
- `general-code-implementer`
- `intent-maintainer`
- `intent-translator`
- `nix-auditor`
- `repo-operator`
- `repo-scaffolder`
- `rust-auditor`
- `scout`
- `skill-editor`

Every generated role inspected carries the shared `agent-outputs/<SessionName>/` output protocol. The generated `scout` has the same runtime name as bundled `scout`, so `/home/li/primary/.pi/agents/scout.md` shadows the bundled scout in project scope.

Bundled role frontmatter uses Pi-specific tool names and runtime fields:
- `scout`: `tools: read, grep, find, ls, bash, write, intercom`; `inheritProjectContext: true`; `inheritSkills: false`; `output: context.md`.
- `researcher`: `tools: read, write, web_search, fetch_content, get_search_content, intercom`; `inheritProjectContext: true`; `inheritSkills: false`; `output: research.md`.
- `planner`: `tools: read, grep, find, ls, write, intercom`; `defaultContext: fork`; `defaultReads: context.md`; `output: plan.md`; `inheritSkills: false`.
- `worker`: `tools: read, grep, find, ls, bash, edit, write, contact_supervisor`; `defaultContext: fork`; `defaultReads: context.md, plan.md`; `inheritSkills: false`.
- `reviewer`: `tools: read, grep, find, ls, bash, edit, write, intercom`; `defaultReads: plan.md, progress.md`; `inheritSkills: false`.
- `context-builder`: `tools: read, grep, find, ls, bash, write, web_search, intercom`; `output: context.md`; `inheritSkills: false`.
- `oracle`: `tools: read, grep, find, ls, bash, intercom`; `defaultContext: fork`; `inheritSkills: false`.
- `delegate`: `systemPromptMode: append`; `tools: read, grep, find, ls, bash, edit, write, contact_supervisor`; `inheritSkills: false`.

## Interpretations

No bundled role should be used as-is in this workspace doctrine pass. The recurring blockers are tool assumptions, generic authority, `inheritSkills: false`, output paths that bypass `agent-outputs/<SessionName>/`, and default forked context that can treat chat history as more authoritative than psyche intent and generated role contracts.

The bundled roles are still useful as corpus material. Their strongest concepts are role-specific output shapes, one-writer discipline, evidence-first review, explicit escalation for unapproved decisions, and distinguishing local scout work from external research.

## Per-Role Triage

| Bundled role | Triage | Rationale |
|---|---|---|
| `scout` | Mine small idea | Generated `/home/li/primary/.pi/agents/scout.md` is already authoritative and shadows this builtin. Useful source material: compressed handoff context, "Start Here", and file/line evidence. Do not import its `write` tool, `context.md` output, or looser read-only boundary. |
| `researcher` | Modify-and-import concept | Workspace lacks a generated external-research role equivalent. Keep the focused research brief, source evaluation, primary-source preference, stale-source filtering, and gaps section. Modify for workspace web rules, citations, privacy, current-date discipline, official-source requirements where applicable, and `agent-outputs/<SessionName>/`. |
| `planner` | Mine small idea | The concrete plan shape is useful: goal, ordered tasks, files, dependencies, risks, and acceptance. A standalone generic planner conflicts with generated `intent-translator`, which owns dependency graphs, task boundaries, evidence expectations, and decision ownership from psyche intent. |
| `worker` | Mine small idea | Generic `worker` conflicts with generated implementers and role-specific boundaries. Mine only the clauses for one writer, minimal coherent edits, validating the assigned plan against actual code, and escalating unapproved product or architecture decisions. Do not import the broad role name or forked-context authority. |
| `reviewer` | Modify-and-import concept | A generic review/audit concept is useful for non-Rust, non-Nix, plan, diff, and artifact review, but must be review-only by default. The bundled role has `edit` and `write`, allows "Fixed" results, and mentions `progress.md`, so it needs workspace-specific separation between findings, optional fix authority, and output artifacts. |
| `context-builder` | Modify-and-import concept | Useful as a handoff/context synthesis role that reads requirements, local code, external references when needed, and writes a compact meta-prompt. It overlaps with `scout` and `intent-translator`, so import only if V2 gives it a narrow boundary: evidence collection plus handoff context, not authority to choose implementation. |
| `oracle` | Modify-and-import concept | The decision-consistency review role is useful for detecting drift, hidden assumptions, and contradictions. It must be modified so inherited chat is evidence, not authority; psyche intent, Spirit records, generated roles, repo instructions, and accepted designs remain above forked context. |
| `delegate` | Reject | Too generic, append-mode, mutation-capable, and boundary-free. It weakens the generated role packet model and invites using an untyped child instead of selecting a real role. No doctrine import recommended beyond the generic reminder to keep delegated tasks bounded. |

## Name And Precedence Hazards

`scout` is an active name collision. Project `scout` currently wins, but if generation drops or renames `/home/li/primary/.pi/agents/scout.md`, the bundled Pi scout will silently become the visible `scout` again.

`worker`, `reviewer`, `planner`, `researcher`, `context-builder`, `oracle`, and `delegate` are unshadowed bundled names. Because they are generic and visible, a parent or human can select them instead of generated roles such as `general-code-implementer`, `rust-auditor`, `nix-auditor`, `intent-translator`, or `skill-editor`.

Future generated roles using any of those exact names will shadow builtins. That may be desirable if intentional, but it is a precedence hazard unless the generator owns it explicitly. Package-qualified names are supported by Pi frontmatter, but the bundled builtins are unqualified.

Saved chains or prompts that refer to unqualified `worker`, `reviewer`, `planner`, or `scout` are brittle because role meaning changes when a project role shadows a builtin. V2 doctrine should prefer generated role names or explicit project role selection for workspace workflows.

## Constraint Hazards

Tool assumptions:
- Bundled tools are Pi runtime names, not this harness's tool names.
- `scout`, `reviewer`, `context-builder`, and `researcher` include write-capable or web-capable tools in ways that do not match workspace role boundaries.
- `researcher` assumes `web_search`, `fetch_content`, and `get_search_content`; those are package/tooling-specific and not a doctrine-level guarantee.
- `intercom` and `contact_supervisor` are runtime coordination mechanisms, not stable workspace authority surfaces.

`inheritSkills` hazard:
- All bundled roles set or default to `inheritSkills: false`. That avoids context bloat, but it bypasses workspace skill-trigger discipline unless a parent injects specific skills. Generated workspace roles and skill doctrine should not inherit this as a default rule.

Authority hazard:
- `planner`, `worker`, and `oracle` default to forked context. Forked context is useful for continuity, but the bundled wording can treat inherited conversation as the contract. Workspace doctrine needs a stronger hierarchy: psyche intent and generated role contracts outrank chat drift.

Output protocol hazard:
- Bundled defaults such as `context.md`, `research.md`, `plan.md`, `progress.md`, and normal final summaries conflict with the generated `agent-outputs/<SessionName>/<RoleLabel>-<ArtifactName>.md` pickup protocol.

Role boundary hazard:
- Bundled `reviewer` can edit, bundled `scout` can write, bundled `delegate` can edit/write, and bundled `worker` is an all-purpose implementation role. These conflict with generated role separation between scout, translator, implementer, auditor, skill editor, and repo operator.

## Recommendations

Feed `SkillEditor-CorpusTriage`:
- Keep source snippets or paraphrases for `researcher` source evaluation, especially kept/dropped sources and gaps.
- Keep `scout` handoff ideas: file ranges, architecture summary, and "Start Here".
- Keep `planner` task row idea: file, change, acceptance.
- Keep `reviewer` evidence-only finding discipline, but strip edit authority from review-only roles.
- Keep `worker` unapproved-decision escalation and one-writer language as shared implementer module material.
- Keep `oracle` drift/contradiction checklist, rewritten around workspace authority.

Feed `V2RoleDoctrineBundles`:
- Candidate roles or bundles: `Researcher`, `GeneralAuditor` or `Reviewer`, `ContextBuilder` or `HandoffBuilder`, and `DecisionConsistencyReviewer` or `Oracle`.
- Do not add generic `Delegate`.
- Do not add generic `Worker`; fold useful worker language into `general-code-implementer`, `criomos-implementer`, and any future specialist implementers.
- Do not add generic `Planner` as a peer to `intent-translator`; fold useful plan formatting into translator output or downstream implementation briefs.
- Explicitly decide whether to shadow, disable, or tolerate unaccepted builtins at Pi startup. Until psyche decides, generated project roles remain authoritative and bundled builtins are source material only.

## Unknowns And Blockers

Unknown: the exact live `/subagents list` output in the current Pi UI. I did not run it because source discovery code plus local settings were enough for this material review, and invoking runtime UI was outside the read-only source inspection path.

Unknown: whether future CriomOS packaging sets `PI_SUBAGENT_EXTRA_AGENT_DIRS` or settings overrides outside the files inspected here. The source code supports extra user agent dirs through that environment variable.

No blocker for doctrine triage. The main decision for the psyche or lead remains policy: whether unaccepted bundled builtins should be hidden/disabled, shadowed by generated roles, or left visible with doctrine saying they are untrusted source material.
