---
title: 0 - Claude slash autocomplete duplicate intent command
role: claude-intent-debug-operator-assistant
variant: Audit
date: 2026-06-25
topics: [claude, slash-commands]
description: |
  Debugging report for duplicate /intent-led-orchestration autocomplete entries
  in Claude Code within /home/li/primary.
---

# 0 - Claude slash autocomplete duplicate intent command

## Finding

Claude Code 2.1.185 exposes skills through slash resolution. Its `claude
--help` output says `--bare` still resolves skills via `/skill-name`, and
`--disable-slash-commands` is described as disabling all skills.

The project had two Claude-visible surfaces with the same slug and display
description:

- `.claude/commands/intent-led-orchestration.md`
- `.claude/skills/intent-led-orchestration/SKILL.md`

Both used `name: intent-led-orchestration` and the same description. That made
Claude eligible to display at least two indistinguishable project candidates for
`/intent-led-orchestration`. Local Claude state also recorded the old
helper-only command and skill as authored artifacts in `~/.claude.json`, and
recorded `intent-led-orchestration` under `skillUsage`; those are stale state
signals, not project command files.

## Fix Applied

Removed `.claude/skills/intent-led-orchestration/SKILL.md`. The canonical
Claude slash surface is now only `.claude/commands/intent-led-orchestration.md`.
The workspace-level and Codex/agent-oriented copies remain:

- `.agents/skills/intent-led-orchestration/SKILL.md`
- `skills/intent-led-orchestration.md`
- `.codex/commands/intent-led-orchestration.md`
- `.codex/prompts/intent-led-orchestration.md`

## Verification

Focused project searches after the edit show:

- No `.claude` helper-only files remain.
- Only one `.claude` intent-led file remains:
  `.claude/commands/intent-led-orchestration.md`.
- The duplicate Claude skill front matter is gone; the remaining Claude
  front matter with `description: Displays the fresh-context...` is only the
  command file.

## Remaining Uncertainty

The screenshot showed more than two duplicate rows. The extra rows may come
from Claude's in-memory autocomplete index or stale per-session UI cache. The
project-side duplicate source is removed; a fresh Claude session should reload
the command list. If duplicates remain after restart, inspect Claude's
runtime cache/state rather than adding another project command edit.
