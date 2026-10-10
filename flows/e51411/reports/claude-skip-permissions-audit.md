# Claude skip-permissions audit

Flow e51411, subflow audit, 2026-09-24. This audit was read-only. The living's rule is that every flow starts with `--dangerously-skip-permissions`.

## Direct evidence of the failure

The running Psyche Medium e51411 process (pid 1716162, Herdr pane `wD:pF`, session `messaging-build`) has this argv:

    claude --session-id e5141130-9a4a-4b8f-b405-67d941a7b320 --model claude-opus-5-5 --effort medium --remote-control

It has no skip flag and no `--permission-mode`. No settings file sets `defaultMode`, so the session fell back to Claude Code's own default. On this build that default is auto mode: `~/.claude.json` records `hasSeenAutoDefaultNotice` and `autoModeEnvSetup.denials: 5`. The argv has exactly the shape of `native_argv(manifest, mode=None, name=False)` in `tools/claude-native-seat-refresh.py`. `CLAUDE_JOB_DIR=~/.claude/jobs/native-<uuid>` also matches the job-directory convention of the native launchers.

## Launch paths

| Launch path | Has flag | file:line | Owner |
|---|---|---|---|
| `native-batch-refresh.mjs` Claude main-seat launch (`herdr agent start … --kind claude -- <mainSeatLaunchArgs>`) | **no** | primary `tools/native-batch-refresh.mjs:85` (argv base), `:219` (herdr start) | primary tools (Field) |
| `claude-native-seat-refresh.py` `native_argv`: the declared launch argv. The same list is also the exact-match check at `:321`, `:368`, `:482`, `:503` | **no** | primary `tools/claude-native-seat-refresh.py:47-56` | primary tools (Field) |
| `claude-single-turn-start.py` (herdr agent start, PsycheHigh) | yes, but the path is disabled (raises at `:106`) | primary `tools/claude-single-turn-start.py:116-119` | primary tools |
| `claude-bootstrap-controller.py` (`claude --bg …`, restricted `--tools ""`) | **no**, but obsolete (raises at `:97`) | primary `tools/claude-bootstrap-controller.py:99,109` | primary tools |
| `flow-cli-poc/flow.py` (`claude -p … --permission-mode plan --tools ''`) | no. It is plan mode on purpose, a read-only proof of concept | primary `tools/flow-cli-poc/flow.py:32` | primary tools (POC) |
| `native-seat-launch.mjs` | n/a: Codex app-server only, never starts Claude | primary `tools/native-seat-launch.mjs:333-347` | Field Astra 5f38bc |
| Flow 0.5 `StartsNativeHerdrHarness` (`herdr agent start --kind claude -- --model M --effort E`) | **no** | flow `crates/flow-nexus/src/herdr/launch.rs:766-816` (Claude arm `:807`) on `origin/flow/basic-commands-00f95a` @ 5485683 | flow repo |
| Deployed flow-nexus 0.3.0 (`/nix/store/x1mq…-flow-0.3.0`) Start | n/a: Start accepts only `codex-medium` | flow `crates/flow-nexus/src/store.rs:281`, `lib.rs:41` @ 61d765e | flow repo |
| harness `HarnessLaunchCommand` Claude row (`claude --channels <prompt>`) | **no** | harness `src/launch.rs:51-54` @ 75ff8a2 | harness repo |
| Herdr 0.8.2 `agent start --kind claude` | no default flags. It passes `-- AGENT_ARG…` through unchanged. `~/.config/herdr/config.toml` has no agent section | `herdr agent start --help`; `~/.config/herdr/config.toml` | Herdr upstream |
| Installed `claude` (`~/.nix-profile/bin/claude`, claude-code 2.1.280) | **no**. The wrapper sets only env vars and PATH | CriomOS-home `owned-agents/claude-code/default.nix:51-63` | CriomOS-home |
| `direct-claude` recovery command | **no** (plain `exec claude "$@"`) | CriomOS-home `modules/home/profiles/min/default.nix:305-315` | CriomOS-home |
| agent-intercom `cci` | yes | CriomOS-home `packages/agent-intercom/default.nix:155-157` | CriomOS-home |
| agent-intercom `ccim`, `claude-raw`, `claude-intercom-worker` | **no** (they pass the caller's arguments through) | CriomOS-home `packages/agent-intercom/default.nix:150-152,158-161` | CriomOS-home |
| `main-flow` skill: harness-crossing subflow launch | yes (`claude -p --dangerously-skip-permissions`) | primary `.claude/skills/main-flow/SKILL.md:28`; source Curriculum `skills/main-flow.md:28` | Curriculum |
| Other skills (`refresh`, `field`, `herdr`, `claude-harness`) | no Claude argv given. They point to the programmatic launchers above | `.claude/skills/*/SKILL.md` | Curriculum |
| User settings `~/.claude/settings.json` | **no** `permissions.defaultMode`. It has `skipDangerousModePermissionPrompt: true`. This is a plain mutable file, not Nix-managed | `~/.claude/settings.json` | living / unmanaged |
| Project settings `/home/li/primary/.claude/settings.json`, `settings.local.json` | **no** `defaultMode` (only `worktree.bgIsolation` and a few allow rules) | those files | primary |
| Managed settings `/etc/claude-code/managed-settings.json` | absent | none | CriomOS (system) |

Nothing forces auto mode. No settings file, environment variable or flag selects it. Auto mode is what Claude Code falls back to when `defaultMode` is unset.

About `native-seat-launch.mjs`: the Field Astra 5f38bc edits are already committed on main, in 1d13409 ("Allow the whole Field Sol startup block in native launch") and a7fa56f ("Restore Field Sol full native identity title"). `jj diff` shows no pending change on disk. The file as it is on disk starts only Codex, so it is not a Claude path.

## CLAUDE_CODE_CHILD_SESSION

- Cleared by: `native-batch-refresh.mjs:36`. It types `unset CLAUDE_CODE_CHILD_SESSION CLAUDE_CODE_SESSION_KIND CLAUDE_CODE_SESSION_ID` into the pane shell before `herdr agent start`, and it fails at `:70` if the variable is still inherited. `claude-bootstrap-controller.py:27` also clears it, but that path is obsolete.
- Checked but not cleared: `claude-native-seat-refresh.py:328,491` refuse a seat whose process still has the variable.
- Not handled: Flow 0.5 `launch.rs` (`workspace create --env` sets only `FLOW_LAUNCH_REQUEST_ID`), harness `launch.rs`, `claude-single-turn-start.py`, agent-intercom, and any hand-typed `claude -p` from the main-flow skill. A `claude -p` run from inside a Claude Bash tool inherits `CLAUDE_CODE_CHILD_SESSION=1`. A Herdr pane shell inherits the Herdr server's environment, not the caller's.

## Options for making bypass the default

1. **User settings `permissions.defaultMode: "bypassPermissions"`, managed by Nix. Recommended.**
   - Where: CriomOS-home, a new `home.activation` entry using `inputs.hexis.lib.mkManagedConfig { file = "$HOME/.claude/settings.json"; declared = { permissions.defaultMode = "bypassPermissions"; }; }`. It follows the pattern already used for `~/.claude.json` in `modules/home/profiles/min/agent-intercom.nix:75-99` and could sit in that file or in a sibling `claude-code.nix` under `modules/home/profiles/min/`. The stop-gap before deploy is to add the same key to `~/.claude/settings.json` by hand.
   - Why: it covers every Claude start of user `li` in any cwd, worktree, `-p`, `--bg` or Herdr launch, with no launcher able to forget it. Launcher argv does not change, so the exact-argv checks in `claude-native-seat-refresh.py` keep passing. `skipDangerousModePermissionPrompt: true` is already set, so no confirmation dialog appears.
   - What else it changes: the living's own interactive sessions also start in bypass. The auto-mode classifier no longer runs. The long `permissions.allow` list becomes inert, though `deny` rules would still apply. An explicit CLI `--permission-mode` still wins, so `flow-cli-poc`'s plan mode is unchanged. Hexis owns only that one leaf, so Claude's own writes to the file (model, theme) are kept.
2. **Managed settings** `/etc/claude-code/managed-settings.json` with `permissions.defaultMode`.
   - Where: CriomOS, the NixOS system repo, via `environment.etc`.
   - What else it changes: it covers every user on the host, cannot be changed from `/config`, and needs a system rebuild instead of a Home switch. It is heavier than this problem needs.
3. **Wrapper flag** `--add-flags --dangerously-skip-permissions` in `wrapProgram`.
   - Where: CriomOS-home `owned-agents/claude-code/default.nix:51-63`.
   - What else it changes: the flag gets prepended to every call, including `claude agents --json` (used by `native-batch-refresh.mjs:188`, `prompt-relay`, `fan-out.mjs` and `claude-native-seat-refresh.py:166`) and other subcommands. It also changes every process argv, which breaks the exact-argv match in `claude-native-seat-refresh.py`. Not recommended.
4. **Project settings** `/home/li/primary/.claude/settings.json`: this covers only sessions whose cwd is primary, and misses worktrees and other repos. Not sufficient.

The launcher argv should still carry the flag, to make intent explicit. That means `native-batch-refresh.mjs:85`, `claude-native-seat-refresh.py:49`, Flow 0.5 `launch.rs:807` and harness `launch.rs:53`. Option 1 is the single fix that makes a forgotten flag harmless.

## Sources

- Process witness: `ps -o args= -p 1716162`; `/proc/1716162/environ`; `~/.claude.json` auto-mode keys.
- `/home/li/primary/tools/{native-batch-refresh.mjs,claude-native-seat-refresh.py,claude-single-turn-start.py,claude-bootstrap-controller.py,native-seat-launch.mjs,flow-cli-poc/flow.py}` at main b95dfa5e0.
- `/git/github.com/LiGoldragon/flow`: HEAD 61d765e (0.3.0); `origin/flow/basic-commands-00f95a` 5485683 (0.5.0) `crates/flow-nexus/src/herdr/launch.rs`.
- `/git/github.com/LiGoldragon/harness` 75ff8a2 `src/launch.rs`.
- `/git/github.com/LiGoldragon/CriomOS-home` 90418576: `owned-agents/claude-code/default.nix`, `packages/agent-intercom/default.nix`, `modules/home/profiles/min/{default.nix,agent-intercom.nix,flow.nix}`, `modules/home/core-packages.nix`.
- `/git/github.com/LiGoldragon/Curriculum` 8563235 `skills/main-flow.md`; `/home/li/primary/.claude/skills/*/SKILL.md`.
- `herdr agent start --help` (herdr 0.8.2); `~/.config/herdr/config.toml`.
- `~/.claude/settings.json`, `/home/li/primary/.claude/settings.json`, `/home/li/primary/.claude/settings.local.json`; `/etc/claude-code` is absent.
