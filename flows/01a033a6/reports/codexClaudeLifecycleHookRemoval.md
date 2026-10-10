# Global Codex and Claude lifecycle-hook removal

The mutable home-level Codex and Claude lifecycle integration has been
removed, without changing package ownership, executables, project hook files,
or Claude's status line.

## Removed

- The whole global Codex definition `/home/li/.codex/hooks.json` (eight
  lifecycle entries).
- The eight `/home/li/.codex/hooks.json:*` trust/state tables from
  `/home/li/.codex/config.toml`.
- The whole `hooks` property from `/home/li/.claude/settings.json` (eleven
  Orca lifecycle event groups); all other top-level settings, including
  `statusLine`, remain.
- `/home/li/.orca/agent-hooks/codex-hook.sh` and
  `/home/li/.orca/agent-hooks/claude-hook.sh`.

The unrelated `/home/li/.orca/agent-hooks/gemini-hook.sh` remains. The scan of
the active Codex, Claude, and Orca configuration locations found no additional
Codex/Claude lifecycle endpoint or provenance artifact to remove.

## Recovery

`/home/li/.local/share/Trash/files/CodexClaudeLifecycleHooks-01a033a6` holds
the removed definition and scripts, plus pre-removal snapshots of the Codex
TOML and Claude settings JSON. Restoration should merge only the archived
hook state or `hooks` property into a current configuration, rather than
overwriting a configuration that may have changed later. The two archived
scripts and the archived `codex-hooks.json` can be restored to their original
paths if the lifecycle integration is intentionally reinstated.

## Verification

The active Claude settings parse as JSON, contain no `hooks` key, and retain
`statusLine`. The active Codex configuration contains no hook state or
reference to the removed file/scripts, and `codex doctor` reports its TOML
configuration parsed successfully. Claude's user-settings doctor succeeds.
The Codex doctor process exits non-zero for its independent unreadable
TERMINFO diagnosis, not configuration parsing.

No lifecycle event was deliberately triggered after removal: producing such a
test would require starting an agent session and could introduce new runtime
state. Parser and active-configuration probes establish that there is no
remaining global definition or persisted trust/state for the removed Codex
hooks.

## Unknowns

The installed Codex CLI exposes no `hooks` management subcommand, so no
first-party list command was available for a separate enumeration probe.
Claude exposes no comparable persisted-trust record in the inspected user
settings. This report does not make a claim about project/worktree hooks,
which were explicitly outside this cleanup's scope.

The local edit-coordination transport was unavailable when this work began,
so its normal lane registration and path-claim record could not be made. The
attempted operations failed with a missing transport endpoint; the change was
therefore kept to the explicitly assigned paths.

## Sources

- `flows/01a033a6/reports/codexClaudeHooks.md`
- `flows/01a033a6/witnesses/codexClaudeLifecycleHookRemoval.md`
- `flows/019fe728/vision/agentIntercom.md`
- `flows/01a01a93/vision/hostEnvironmentRecovery.md`
