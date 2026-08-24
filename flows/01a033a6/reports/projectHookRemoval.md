# Project lifecycle-hook removal

Observed 2026-08-24 in flow `01a033a6`.

## Removed local hook consumers

The following non-generated standalone settings files were renamed to the adjacent inactive recovery name `settings.json.hooks-removed-20260824`. Every original contained only the listed hook surface, so no unrelated setting was removed.

Rust reminder only (`PreToolUse`):

- `/home/li/mind-live-judge-eval-rerun/.claude/settings.json`
- `/home/li/primary-worktrees/MindJudgePromptRewrite-NarrowThirdPass/.claude/settings.json`
- `/home/li/primary-worktrees/MindJudgePromptRewrite-TargetedSecondPass/.claude/settings.json`
- `/home/li/primary-worktrees/mind-judge-fixture-label-cleanup/.claude/settings.json`

`bd prime` (`PreCompact` and `SessionStart`):

- `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/fixlojixbootownership/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/ChromaNoctaliaDeployIntegration/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/DotosMapKeyCompatibility/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/IntegrateLojix0191/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/clavifaber-request-shape/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/criomosDotosRepair/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/default-opener-nhb-pin/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/dotos-upper-integration/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/fixlojixbootownership/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/home-orchestrate-main-pin/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/lojix-breaking-upgrade-docs/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/lojix-ownership-mjl6/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/modifier-architecture-20260811/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/remove-lojix-timeout-consumer/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/repair-home-dependency-chain-20260811/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/schema-rust-main-repair/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/zeus-vscodium-deployment/.claude/settings.json`
- `/home/li/.local/share/Trash/files/CriomOS-deployLatestAgentsB8x-20260824/.claude/settings.json`
- `/home/li/git-archive/github.com/LiGoldragon/lojix-archive/.claude/settings.json`
- `/home/li/git-archive/github.com/LiGoldragon/workspace/.claude/settings.json`

No files were deleted. Restore one consumer by renaming its dated recovery file back to `settings.json` in the same `.claude` directory.

## Excluded generated project consumers

The active primary policy hooks, its uncommitted Codex mirror, and four extant copied primary consumers remain unchanged. `AGENTS.md` declares `.claude/` and `.codex/` generated read-only evidence; no authored hook owner was found.

The Curriculum generator's supported `check-skills` run succeeded and enumerated its generated targets. It owns `.claude/skills`, `.claude/agents`, and `.codex/agents`; it neither emits nor removes `.claude/settings.json`, `.claude/hooks/`, `.codex/hooks.json`, or `.codex/hooks/`. The active manifest and target insertion manifest contain no hook declaration. Thus regeneration cannot remove these hook surfaces without a new authorized design/ownership decision.

The unchanged primary consumers are:

- `/home/li/primary/.claude/settings.json` and `/home/li/primary/.claude/hooks/deny-fable-subagents.sh`
- `/home/li/primary/.codex/hooks.json` and `/home/li/primary/.codex/hooks/deny-fable-subagents.sh`
- `/home/li/wt-primary-session-migration-wave5a/.claude/settings.json` and `.claude/hooks/deny-fable-subagents.sh`
- `/home/li/wt-primary-vision-migration-wave5b/.claude/settings.json` and `.claude/hooks/deny-fable-subagents.sh`
- `/home/li/wt/github.com/LiGoldragon/primary/land-modifier-continuity/.claude/settings.json` and `.claude/hooks/deny-fable-subagents.sh`
- `/home/li/primary-workspaces/LandCodiumWitness/.claude/settings.json` and `.claude/hooks/deny-fable-subagents.sh`

The inventory's fifth copied-primary path, `/home/li/wt-primary-migrate-flow-01`, no longer exists. The marketplace source is also unchanged: inactive marketplace hook-capable source is not an installed/enabled hook surface, while Rust Analyzer is enabled and has no hooks. The supported action is no action to marketplace cache/source; removing or changing it would not remove an active hook and could damage plugin provenance.

## Validation

- `SKILLS_WORKSPACE_ROOT=/home/li/primary nix run /git/github.com/LiGoldragon/Curriculum#check-skills` succeeded. Its output lists only skills and agent packet paths, confirming the generator ownership boundary.
- Schema and absence probe: all 4 Rust-only active `settings.json` files are absent; their recovery files have only `hooks.PreToolUse`.
- Schema, command, and absence probe: all 20 active `bd prime` `settings.json` files are absent; every recovery file has only `hooks.PreCompact` and `hooks.SessionStart`, and every recovered command is exactly `bd prime`.
- Primary evidence restoration probe: the current Claude policy settings/script match their parent revision byte-for-byte, and the current Codex script matches the Claude script byte-for-byte.

## Commit state and unknowns

No authored-source edit was possible, so this removal has no commit or push. The 24 recoverable local relocations intentionally remain local and uncommitted. The open design gap is ownership/reconciliation for non-skill project lifecycle configuration: current regeneration preserves it, but direct edits are prohibited by the consumer-tree boundary. The design must specify an authored source and complete-output cleanup rule before the six extant primary policy consumers can be removed durably.

## Sources

- `flows/01a033a6/reports/codexClaudeHooks.md`
- `AGENTS.md`
- `/git/github.com/LiGoldragon/Curriculum/README.md`
- `/git/github.com/LiGoldragon/Curriculum/manifests/active-outputs.dotos`
- `/git/github.com/LiGoldragon/Curriculum/manifests/target-module-insertions.dotos`
- Curriculum `check-skills` witness in this flow
- Local JSON schema and absence probes in this flow
