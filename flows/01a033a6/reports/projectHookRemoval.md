# Project lifecycle-hook removal

Observed 2026-08-25 in flow `01a033a6`. The living directly authorized removal after the project Codex launch disclosed two new or changed hooks.

## Purpose

The primary Codex `PreToolUse` definition had two hooks. `Agent` ran `deny-fable-subagents.sh`, which denied `fork` and rewrote certain model selections to `write-ordinary`. `Write|Edit` emitted a Rust-discipline reminder for `.rs` paths. No Codex project hook definition remains.

## Active paths removed

All twelve paths are absent and are archived below `home/li` at the recovery path stated below.

- `/home/li/primary/.claude/settings.json`
- `/home/li/primary/.claude/hooks/deny-fable-subagents.sh`
- `/home/li/primary/.codex/hooks.json`
- `/home/li/primary/.codex/hooks/deny-fable-subagents.sh`
- `/home/li/wt-primary-session-migration-wave5a/.claude/settings.json`
- `/home/li/wt-primary-session-migration-wave5a/.claude/hooks/deny-fable-subagents.sh`
- `/home/li/wt-primary-vision-migration-wave5b/.claude/settings.json`
- `/home/li/wt-primary-vision-migration-wave5b/.claude/hooks/deny-fable-subagents.sh`
- `/home/li/wt/github.com/LiGoldragon/primary/land-modifier-continuity/.claude/settings.json`
- `/home/li/wt/github.com/LiGoldragon/primary/land-modifier-continuity/.claude/hooks/deny-fable-subagents.sh`
- `/home/li/primary-workspaces/LandCodiumWitness/.claude/settings.json`
- `/home/li/primary-workspaces/LandCodiumWitness/.claude/hooks/deny-fable-subagents.sh`

## Earlier recovery paths relocated

The following 24 inactive adjacent hook definitions are also absent from their harness configuration directories and centrally archived.

- `/home/li/mind-live-judge-eval-rerun/.claude/settings.json.hooks-removed-20260824`
- `/home/li/primary-worktrees/MindJudgePromptRewrite-NarrowThirdPass/.claude/settings.json.hooks-removed-20260824`
- `/home/li/primary-worktrees/MindJudgePromptRewrite-TargetedSecondPass/.claude/settings.json.hooks-removed-20260824`
- `/home/li/primary-worktrees/mind-judge-fixture-label-cleanup/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/fixlojixbootownership/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/ChromaNoctaliaDeployIntegration/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/DotosMapKeyCompatibility/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/IntegrateLojix0191/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/clavifaber-request-shape/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/criomosDotosRepair/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/default-opener-nhb-pin/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/dotos-upper-integration/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/fixlojixbootownership/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/home-orchestrate-main-pin/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/lojix-breaking-upgrade-docs/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/lojix-ownership-mjl6/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/modifier-architecture-20260811/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/remove-lojix-timeout-consumer/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/repair-home-dependency-chain-20260811/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/schema-rust-main-repair/.claude/settings.json.hooks-removed-20260824`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/zeus-vscodium-deployment/.claude/settings.json.hooks-removed-20260824`
- `/home/li/.local/share/Trash/files/CriomOS-deployLatestAgentsB8x-20260824/.claude/settings.json.hooks-removed-20260824`
- `/home/li/git-archive/github.com/LiGoldragon/lojix-archive/.claude/settings.json.hooks-removed-20260824`
- `/home/li/git-archive/github.com/LiGoldragon/workspace/.claude/settings.json.hooks-removed-20260824`

## Recovery and durability

The archive is `/home/li/.local/share/Trash/files/ProjectCodexClaudeHooks-01a033a6-20260825/home/li/...`; it holds 36 files: 30 valid JSON configurations and 6 executable scripts. Restoring an item to its original path reenables its lifecycle definition and requires new authorization.

The primary Claude settings and script are versioned primary files. This clean-workspace commit removes them from `main`. The primary Codex pair were untracked local files and have no versioned source. The two `wt-primary-*` consumers are unbookmarked JJ working copies; `land-modifier-continuity` and `LandCodiumWitness` have no working-copy commit. All four were stale physical policy copies with no independent configuration owner, so they were archived rather than creating commits on stale or nonexistent branches. The primary `main` deletion is the durable source change.

The inactive marketplace hook-capable source, Rust Analyzer, Claude status line, and Gemini hook were not changed.

## Witnesses

- All twelve active policy paths and all 24 adjacent recovery paths are absent.
- Codex 0.149.1 launched in a PTY at `/home/li/primary`, reached its regular ready prompt without the two-hook review, and exited 0 without trust acceptance or hook creation.
- `claude --setting-sources project doctor` exited 0 with project settings absent; its only warning was unrelated PATH guidance.
- Every settings file was validated as hook-only JSON before archival, so no unrelated setting was removed.

## Sources

- `flows/01a033a6/reports/codexClaudeHooks.md`
- `flows/01a033a6/reports/codexClaudeLifecycleHookRemoval.md`
- `flows/01a033a6/witnesses/codexClaudeLifecycleHookRemoval.md`
- Local archive, absence, Codex PTY, and Claude doctor witnesses in this flow
