# Global Codex and Claude lifecycle-hook removal witness

Method: probe `stat`, `jq`, `rg`, `find`, `codex doctor`, `claude --setting-sources user doctor`, and `orca-ide status --json`.

Before removal, `/home/li/.codex/hooks.json` contained eight global Codex
lifecycle definitions. `/home/li/.codex/config.toml` held eight matching
`hooks.state` records keyed to that file. `/home/li/.claude/settings.json`
held eleven lifecycle event groups, all dispatching through the Orca Claude
wrapper. `/home/li/.orca/agent-hooks/` contained Codex, Claude, and unrelated
Gemini scripts.

After removal:

- `/home/li/.codex/hooks.json`, `codex-hook.sh`, and `claude-hook.sh` are
  absent from their active locations.
- No `hooks.state`, `hooks.json`, Orca, or agent-hook reference remains in the
  active Codex TOML or Claude JSON. The Codex state removal covered all eight
  state tables that referenced the deleted global file.
- `jq` accepts the active Claude settings, reports no `hooks` property, and
  confirms that `statusLine` remains.
- The unrelated executable `gemini-hook.sh` remains under Orca.
- `codex doctor` loaded and parsed `/home/li/.codex/config.toml` successfully.
  Its non-zero outcome was solely an existing unreadable-TERMINFO check.
- `claude --setting-sources user doctor` exited successfully.
- Orca was not running before removal; no process or endpoint had to be
  stopped.

The recoverable archive is
`/home/li/.local/share/Trash/files/CodexClaudeLifecycleHooks-01a033a6`.

