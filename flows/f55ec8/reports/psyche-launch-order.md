# Launch order for primary Psyche opus and primary Psyche sonnet — 2026-09-17

f55ec8's harness refused both plain `claude --bg` launches (auto-mode classifier). Run from any terminal as li; the first prompts are in /tmp/f55ec8-psyche/ (copies below the lane in flows/f55ec8/handoff/psyche/), the base is the v7 replaced base.

cd /home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj && claude --bg --name "primary Psyche opus" --remote-control "primary Psyche opus" --model "claude-opus-4-7[1m]" --system-prompt-file "$PWD/.claude/worktrees/claude-successor-f55ec8/flows/f55ec8/handoff/successors-v7/claude-base.md" -- "$(cat /tmp/f55ec8-psyche/medium-first-prompt.md)" < /dev/null

cd /home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj && claude --bg --name "primary Psyche sonnet" --remote-control "primary Psyche sonnet" --model sonnet --system-prompt-file "$PWD/.claude/worktrees/claude-successor-f55ec8/flows/f55ec8/handoff/successors-v7/claude-base.md" -- "$(cat /tmp/f55ec8-psyche/low-first-prompt.md)" < /dev/null
