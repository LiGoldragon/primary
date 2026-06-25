# Mentci real Claude proof witness

status: blocked
missing_prerequisite: exact Claude adapter argv is unavailable; bare mode requires ANTHROPIC_API_KEY or an apiKeyHelper visible to --bare

## Detection
claude_version_status: exit status: 0
claude_version_stdout: 2.1.185 (Claude Code)
bare_auth_probe_program: claude
bare_auth_probe_arguments: ["--bare", "--print", "reply with exactly mentci-bare-availability-ok", "--model", "claude-haiku-4-5-20251001", "--permission-mode", "bypassPermissions"]
bare_auth_probe_status: exit status: 1
bare_auth_probe_stdout: Not logged in · Please run /login
bare_auth_probe_stderr: 

## Required Proof Not Run
The real terminal-cell proof did not run because the exact Claude adapter auth probe failed before launch. The adapter argv includes `--bare`, `--model claude-haiku-4-5-20251001`, and `--permission-mode bypassPermissions`; this environment must expose Anthropic auth to bare mode before the proof bead can close.
