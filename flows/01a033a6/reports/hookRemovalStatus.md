# Claude and Codex hook removal status

Observed and independently rechecked on 2026-08-25. All audited global,
project, and generated-consumer hook surfaces are now absent from active
discovery; this report records the recovery archives, behavioral proof, and
the inactive-source boundary.

## Removed from active discovery

The global Orca lifecycle integration is completely absent from the active
Claude and Codex user configuration:

- `/home/li/.codex/hooks.json` is absent.
- All eight global Codex hook trust/state records were removed from
  `/home/li/.codex/config.toml`.
- `/home/li/.claude/settings.json` has no `hooks` property; its unrelated
  `statusLine` remains.
- Orca's `codex-hook.sh` and `claude-hook.sh` are absent; the unrelated
  `gemini-hook.sh` remains executable.

The original global files and pre-edit configuration snapshots are recoverable
at `/home/li/.local/share/Trash/files/CodexClaudeLifecycleHooks-01a033a6`.

Twenty-four standalone Claude project/worktree hook consumers were retired:
four Rust-reminder settings and twenty `bd prime` settings. Their active
`settings.json` paths are all absent. Every adjacent recovery definition was
relocated under
`/home/li/.local/share/Trash/files/ProjectCodexClaudeHooks-01a033a6-20260825/home/li/...`;
these names are not Claude settings sources. The archive contains 30 JSON files
and 6 scripts. Independent parsing found all 24 recovered definitions valid,
with exactly the expected hook-only content.

## Verification

An independent read-only verifier established:

- active global Codex definition, Orca Codex script, and Orca Claude script:
  absent;
- global Codex hook trust/state, removed-script references, and Orca
  references: absent;
- Claude user JSON: valid, no `hooks`, `statusLine` retained;
- `codex --strict-config doctor`: configuration parses; only the independent
  pre-existing unreadable TERMINFO diagnosis remains;
- `claude --setting-sources user doctor`: succeeds;
- Codex 0.149.1 PTY reached `Ready` with no review screen and exited 0;
- the Claude project doctor passed;
- Orca: stopped and unreachable;
- installed Claude/Codex plugin sources: no hook manifests.

Official OpenAI documentation confirms that global, project, inline TOML, and
enabled plugin hook sources merge rather than replace one another. Definitions
must therefore be removed at each real source; global disable alone would not
be removal. The docs specify trust-by-current-hash and disable controls, but do
not document a trust-state purge or a permanent deletion command.

A global-disable fallback was investigated and deliberately not substituted
for removal. Codex supports `[features].hooks = false` and Claude supports
`"disableAllHooks": true`, but user-level values can be overridden by higher
project or managed precedence. Claude's switch also disables the unrelated
custom status line which this cleanup preserves. Neither control resolves the
unowned generated files, so adding it would create a weaker, misleading result.

## Completed generated policy cleanup

The twelve hook-shaped paths previously remaining across six project consumers
are now all absent from active discovery. The two Codex hooks in that final
cleanup were:

- `PreToolUse` matcher `Agent`, which denied `fork` and rewrote forbidden model
  requests;
- `Write|Edit`, which returned the inline Rust-discipline reminder.

The generated-tree ownership boundary was respected while the living's direct
removal authorization was carried out. The recovery definitions remain
available in the dated archive above; no active audited policy hook remains.

## Inactive source and archives

Inactive marketplace caches remain non-installed source and are not active
hooks. The enabled Claude Rust Analyzer plugin has none, and installed Codex
plugin sources have none. The cache was not corrupted merely to erase inactive
source which the harness does not discover.
Historical logs and the explicit recovery archives also retain text or code for
the removed hooks, but are not active definitions.

## Sources

- `flows/01a033a6/reports/codexClaudeHooks.md`
- `flows/01a033a6/reports/codexClaudeLifecycleHookRemoval.md`
- `flows/01a033a6/reports/projectHookRemoval.md`
- `flows/01a033a6/witnesses/codexClaudeLifecycleHookRemoval.md`
- Workspace `AGENTS.md` and Curriculum `check-skills` output.
- [Official OpenAI hooks documentation](https://learn.chatgpt.com/docs/hooks)
- [Official OpenAI configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Official Claude Code settings reference](https://code.claude.com/docs/en/configuration)
- [Official Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
