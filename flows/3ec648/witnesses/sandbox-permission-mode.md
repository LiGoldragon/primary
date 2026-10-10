# Witness: why a sandboxed `claude -p --permission-mode default` reports bypassPermissions

Method: claude 2.1.284, haiku, `say ok`, `--output-format stream-json --verbose`, fresh empty HOME holding only `.claude/.credentials.json` installed mode 600 (as semi-sandbox-capsule.sh does; never printed). Each run bounded to 170 s, stdin from /dev/null. Read the `permissionMode` of the init event. Scratch: the flow scratchpad, dirs h1..h10, o*.jsonl.

## Environment present in the parent (names only)
CLAUDECODE, CLAUDE_PID, CLAUDE_EFFORT, CLAUDE_CODE_ENTRYPOINT, CLAUDE_CODE_EXECPATH, CLAUDE_CODE_SESSION_ID, CLAUDE_CODE_CHILD_SESSION, CLAUDE_CODE_SESSION_ATTENDED, CLAUDE_CODE_BRIDGE_SESSION_ID, CLAUDE_CODE_MESSAGING_SOCKET, CLAUDE_CODE_MESSAGING_TOKEN, CLAUDE_CODE_DISABLE_WORKFLOWS, CLAUDE_CODE_DISABLE_AUTO_MEMORY. No ANTHROPIC_* variable. None of these is a permission-mode setting.

## Runs (reported permissionMode)
| run | result |
|---|---|
| installed `claude`, inherited env, `--permission-mode default` | bypassPermissions |
| installed `claude`, `env -i PATH HOME`, default | bypassPermissions |
| installed `claude`, all CLAUDE_* removed, default | bypassPermissions |
| installed `claude`, `env -i`, plan / acceptEdits / no flag | bypassPermissions each |
| installed `claude`, `env -i`, default, asked to `touch` a file | file created (really bypassed) |
| `.claude-wrapped` directly, `env -i`, default | default |
| `.claude-wrapped` directly, `env -i`, plan | plan |
| `.claude-wrapped` directly, no flag | default |
| `.claude-wrapped` directly, default, asked to `touch` | denied (permission_denials lists Bash), no file |

## Cause
The installed `claude` (`~/.nix-profile/bin/claude`, a Nix bash wrapper) ends with
`exec -a claude .../.claude-wrapped --dangerously-skip-permissions "$@"`.
The wrapper prepends the skip flag, and it beats any later `--permission-mode`. The report is honest: bypass is really in force.

## Ruled out
Inherited env vars (identical under `env -i`), parent bypass leaking via env, managed/policy settings (/etc/claude-code, /etc/claude absent), HOME or synced settings (fresh HOME, direct binary gives default), `-p` defaults (default is `default`).

## Variable set to clear
None: the cause is not an env var. A sandbox must run the unwrapped binary (`/nix/store/...-claude-code-2.1.284/bin/.claude-wrapped`, resolved from the wrapper's exec line) rather than `claude`, or otherwise drop the injected flag. The wrapper itself unsets CLAUDE_CODE_CHILD_SESSION, CLAUDE_CODE_SESSION_KIND, CLAUDE_CODE_SESSION_ID and exports DISABLE_AUTOUPDATER, DISABLE_NON_ESSENTIAL_MODEL_CALLS, DISABLE_INSTALLATION_CHECKS. Calling .claude-wrapped skips these; set the DISABLE_* ones if wanted. Clearing CLAUDE_* is still wise for hygiene but unneeded for the mode.
