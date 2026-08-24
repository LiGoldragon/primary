# Codex and Claude hook inventory

> Removal follow-up: global hooks and all 24 standalone project/worktree
> consumers were removed from active discovery on 2026-08-24–25. All active
> hooks audited in this inventory are now removed. See `hookRemovalStatus.md`
> for the independently checked current state.

The detailed sections below preserve the pre-removal inventory and provenance;
they are historical descriptions, not claims of current activation.

Observed on 2026-08-24. The local Home update and the hook audit are separate:
CriomOS-home owns the Claude and Codex executables, while the global hook files
described below are ordinary mutable home files outside that declarative owner.

## What Codex hooks are

Codex hooks are a first-party lifecycle-command interface. Codex loads hook
definitions from global `~/.codex/hooks.json`, project `.codex/hooks.json`, and
enabled plugin hook manifests; supplies event JSON on standard input; and
requires trust when a hook command changes. The hooks feature is enabled by
default unless `[features].hooks = false`. This is separate from Git hooks,
skills, plugins as such, and an application's unrelated `--run-hooks` option.

## Pre-removal global Orca integration

| Harness | Configuration and events | Present state | Purpose | Age and provenance |
|---|---|---|---|---|
| Codex | `/home/li/.codex/hooks.json`: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `SubagentStart`, `SubagentStop`, `Stop` | All eight commands have persisted trusted hashes. `PreToolUse` alone is explicitly disabled. The other seven are structurally enabled, but their external side effect is presently inert because Orca is stopped and direct sessions lack the required Orca port, token, and pane-key environment. | Pass Codex lifecycle JSON to Orca's local `/hook/codex` endpoint so Orca can track a managed agent session. | Regular unmanaged file, born and modified 2026-08-23 19:17:02 +02:00, less than a day before this audit. An agent launched the Orca GUI at 19:17:01 local during a smoke test; Orca then reported granting eight managed Codex hook entries with `wrote=true`. |
| Claude | `/home/li/.claude/settings.json`: `SessionStart`, `UserPromptSubmit`, `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`, `TeammateIdle`, plus wildcard `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, and `PermissionRequest` | The 11 entries are configured for direct Claude sessions. No independent Claude trust witness was recovered. Their Orca side effect is presently inert for the same stopped-server/missing-environment reason. | Pass Claude lifecycle JSON to Orca's local `/hook/claude` endpoint; the wrapper first emits `{}` so a missing endpoint does not block Claude. | Regular unmanaged file, born and modified 2026-08-23 19:17:03 +02:00. Its backup contains the same settings with `.hooks` removed, proving these entries were added in the Orca timestamp burst. |

The executables are:

- `/home/li/.orca/agent-hooks/codex-hook.sh`, born 2026-08-23 19:17:02
  +02:00, executable, posting to `/hook/codex`.
- `/home/li/.orca/agent-hooks/claude-hook.sh`, born 2026-08-23 19:17:03
  +02:00, executable, returning `{}` and posting to `/hook/claude`.

`orca-ide status --json` reported `running:false`, `state:not_running`, and
`reachable:false`; no Orca listener or process was found. Thus “installed and
configured” and “currently producing an Orca effect” have different answers:
the former is yes, the latter no.

The provenance is strong. In session `01a02f90`, an agent ran
`orca-ide-gui --no-sandbox` at 2026-08-23T17:17:01.612Z. The hook files appeared
at 17:17:02–03Z, and at 17:17:15.265Z Orca logged twice that it had granted eight
managed Codex hook entries with `wrote=true`. The living's request in the
parent flow was to install Herdr and Orca in Home and deploy them; no request to
install hooks was found, and no agent-issued `install hooks` command was found.
The grounded account is therefore: an agent explicitly launched Orca for the
authorized GUI smoke, and Orca's internal bootstrap performed an additional
mutable hook installation and trust grant that the living had not separately
requested. The exact internal writer call and any meaning of Orca's “intent
record 884” remain unknown.

## Project policy hooks

### Primary Claude policy

`/home/li/primary/.claude/settings.json` defines two `PreToolUse` hooks:

- matcher `Agent` runs
  `/home/li/primary/.claude/hooks/deny-fable-subagents.sh`. It denies `fork`,
  rewrites forbidden fable/sonnet/opus subagents to `write-ordinary`, and fails
  closed on malformed input.
- matcher `Write|Edit` returns an inline Rust-discipline reminder.

These are project-scoped and apply when Claude runs in the project. The script
is executable, was born 2026-08-07 14:26:11 +02:00, and its current primary
change is attributed by repository history to `li` in commit `ccede43e667f`,
2026-08-07 14:26:34 +02:00. Copies occur in five observed primary worktrees:
`wt-primary-migrate-flow-01`, `wt-primary-session-migration-wave5a`,
`wt-primary-vision-migration-wave5b`,
`wt/github.com/LiGoldragon/primary/land-modifier-continuity`, and
`primary-workspaces/LandCodiumWitness`.

Four other Claude worktrees contain only the Rust reminder:
`mind-live-judge-eval-rerun`,
`primary-worktrees/MindJudgePromptRewrite-NarrowThirdPass`,
`primary-worktrees/MindJudgePromptRewrite-TargetedSecondPass`, and
`primary-worktrees/mind-judge-fixture-label-cleanup`. Their settings date from
2026-07-03 through 2026-07-06 and apply only when Claude runs there.

### Primary Codex policy

`/home/li/primary/.codex/hooks.json` and
`/home/li/primary/.codex/hooks/deny-fable-subagents.sh` were born together on
2026-08-24 at 10:21:44 +02:00 and are uncommitted working-copy additions. They
mirror the primary Claude `Agent` denial/rewrite and `Write|Edit` Rust reminder;
the script is byte-identical to the Claude script. No transcript write, request,
commit author, or project-hook trust record was found. Reads and audits were
found, but execution was not. Their creator, authorization, and active runtime
state are therefore unknown; global Codex trust does not prove project-hook
trust.

## Claude `bd prime` project hooks

Twenty repository copies define `PreCompact` and `SessionStart` hooks that run
`bd prime`, whose purpose is to refresh Beads guidance/context for that Claude
project. Three are archived and inactive:

- `/home/li/.local/share/Trash/files/CriomOS-deployLatestAgentsB8x-20260824/.claude/settings.json`
  — born 2026-08-24 10:42:16 +02:00.
- `/home/li/git-archive/github.com/LiGoldragon/lojix-archive/.claude/settings.json`
  — born 2026-05-06 14:42:28 +02:00.
- `/home/li/git-archive/github.com/LiGoldragon/workspace/.claude/settings.json`
  — born 2026-05-05 23:11:54 +02:00.

The remaining seventeen are conditional rather than globally active: each can
run only if Claude is launched in its worktree.

- `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/fixlojixbootownership/.claude/settings.json`
  — 2026-08-23 14:36.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/ChromaNoctaliaDeployIntegration/.claude/settings.json`
  — 2026-08-19 23:19.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/DotosMapKeyCompatibility/.claude/settings.json`
  — 2026-08-08 14:58.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/IntegrateLojix0191/.claude/settings.json`
  — 2026-08-23 21:14.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/clavifaber-request-shape/.claude/settings.json`
  — 2026-08-23 12:06.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/criomosDotosRepair/.claude/settings.json`
  — 2026-08-24 01:13.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/default-opener-nhb-pin/.claude/settings.json`
  — 2026-08-21 20:31.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/dotos-upper-integration/.claude/settings.json`
  — 2026-08-10 19:23.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/fixlojixbootownership/.claude/settings.json`
  — 2026-08-23 14:34.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/home-orchestrate-main-pin/.claude/settings.json`
  — 2026-08-10 18:08.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/lojix-breaking-upgrade-docs/.claude/settings.json`
  — 2026-08-23 18:51.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/lojix-ownership-mjl6/.claude/settings.json`
  — 2026-08-10 16:16.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/modifier-architecture-20260811/.claude/settings.json`
  — 2026-08-11 18:39.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/remove-lojix-timeout-consumer/.claude/settings.json`
  — 2026-08-23 11:02.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/repair-home-dependency-chain-20260811/.claude/settings.json`
  — 2026-08-11 00:43.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/schema-rust-main-repair/.claude/settings.json`
  — 2026-08-10 17:47.
- `/home/li/wt/github.com/LiGoldragon/CriomOS/zeus-vscodium-deployment/.claude/settings.json`
  — 2026-08-09 15:35.

These are 389–390-byte settings files. Birth and modification times are equal
for each worktree copy. Those dates establish copy age, not necessarily the
origin of the hook design.

## Absent, inactive, or similarly named mechanisms

- Herdr 0.8.2 is installed, but `herdr integration status` reports both Claude
  and Codex integrations **not installed**. The expected Herdr scripts
  `/home/li/.claude/hooks/herdr-agent-state.sh` and
  `/home/li/.codex/herdr-agent-state.sh` are absent.
- No executable repository Git hooks and no global `core.hooksPath` were found.
- Active Codex plugin caches contain no hook declarations.
- Only Rust Analyzer is installed/enabled from the Claude plugin marketplace;
  it has no hooks. The marketplace checkout contains inactive, uninstalled
  hook-capable source for `explanatory-output-style` (`SessionStart`), `hookify`
  (`PreToolUse`, `PostToolUse`, `Stop`, `UserPromptSubmit`),
  `learning-output-style` (`SessionStart`), `ralph-loop` (`Stop`), and
  `security-guidance` (`PreToolUse` on `Edit|Write`). Those source files date
  from approximately 2026-04-06 and do not become active merely by existing in
  the marketplace checkout.
- `/home/li/.claude/statusline.sh` is executable but is a status-line renderer,
  not a lifecycle hook.
- Orca's `worktree create --run-hooks` option concerns worktree setup, not
  Codex/Claude lifecycle hooks.

## Declarative ownership and update result

Current CriomOS-home sources declare the packages but contain no `hooks.json`,
`claude-hook`, `codex-hook`, `agent-hooks`, or `herdr integration` declaration.
The global hook files are regular files, not Home Manager symlinks. They will
therefore survive the declarative update but are not reproducibly owned by it.

Published CriomOS-home revision `0836e4b7e367efe6a81a4fa657e2a2f741f0d801`
already held the latest package changes. A focused evaluation and remote-only
activation build passed. Lojix deployment 60 targeted the local Ouranos Home,
reached `Current`, `Completed`, and `Succeeded` at terminal marker 1408, and an
ordinary login shell resolved Codex CLI 0.149.1 and Claude Code 2.1.241. The
coordinated Codex VSIX is 26.5818.61809. No generated harness tree was edited.

## Sources

- Flow `491750ff`, especially `flows/491750ff/reports/harnessUpdate.md`.
- Codex hook configuration: `/home/li/.codex/hooks.json` and `/home/li/.codex/config.toml`.
- Claude hook configuration: `/home/li/.claude/settings.json` and `/home/li/.claude/settings.json.bak`.
- Orca hook scripts: `/home/li/.orca/agent-hooks/codex-hook.sh` and `/home/li/.orca/agent-hooks/claude-hook.sh`.
- Primary project configurations: `/home/li/primary/.claude/settings.json` and `/home/li/primary/.codex/hooks.json`.
- Orca smoke transcript `01a02f90-7433-72c1-a7b5-078e087703ea`, especially JSONL lines 408 and 432.
- Current provenance transcript `01a033a8-3d7f-7962-bc0a-0f763a7f5d23`.
- Commit `ccede43e667fdcb75b2951d7e3366d9b63557489` in the primary repository.
- [Official Codex hooks documentation](https://learn.chatgpt.com/docs/hooks).
- [Official Codex releases](https://github.com/openai/codex/releases/latest).
- [Official Claude Code releases](https://github.com/anthropics/claude-code/releases/latest).
