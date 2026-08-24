# Claude and Codex hook removal status

Observed and independently rechecked on 2026-08-24. This report distinguishes
active definitions, inactive recovery material, inactive marketplace source,
and hook-shaped files which the current generated-consumer rule prevents this
realization round from editing directly.

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
`settings.json` paths are all absent. Each original is preserved beside its old
location as `settings.json.hooks-removed-20260824`; these names are not Claude
settings sources. Independent parsing found all 24 valid, with exactly the
expected hook-only content.

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

## Remaining generated policy consumers

Twelve hook-shaped paths remain across six project consumers:

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

The primary Codex pair is uncommitted and has no project hook-trust or execution
witness. The Claude pairs are project-scoped consumers and can apply when
Claude runs in those projects.

These paths were not changed. The workspace's current `AGENTS.md` says all
`.claude/` and `.codex/` trees are generated read-only evidence and must never
be edited directly. The supported Curriculum `check-skills` generation passed
and proved that it owns only `.claude/skills`, `.claude/agents`, and
`.codex/agents`; no authored source or manifest owns settings or hook scripts,
and regeneration preserves them. Removing these twelve paths now therefore
requires either a direct exception to the generated-tree rule or a new authored
owner and complete-output cleanup design. Neither was silently assumed.

## Inactive source and archives

Cached marketplace packages still contain hook-capable source. No such package
is installed as an active Claude/Codex hook; the enabled Claude Rust Analyzer
plugin has none, and installed Codex plugin sources have none. The cache was not
corrupted merely to erase inactive source which the harness does not discover.
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
