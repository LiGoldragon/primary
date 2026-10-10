# Primary Psyche Medium remote-resume witness

2026-09-17. Delegated read-only restoration attempt for the original Claude
conversation `48cff7d7-d148-4280-89c8-23c460de0d6c`, whose transcript remains
at `/home/li/.claude/projects/-home-li-wt-github-com-LiGoldragon-primary-psyche-medium-jj--claude-worktrees-flow-48cff7/48cff7d7-d148-4280-89c8-23c460de0d6c.jsonl`.

Before launching, installed Claude Code `2.1.263` help was read. It documents
`--bg` with `--resume <session-id>` as continuing a stopped session under the
same ID, and documents `--remote-control [name]`, `--model`, and `--effort`.
`claude agents --json --all` showed exactly the original matching target:
background ID `48cff7d7`, full session ID
`48cff7d7-d148-4280-89c8-23c460de0d6c`, cwd
`/home/li/wt/github.com/LiGoldragon/primary/psyche-medium-jj`, name
`primary-psyche-medium`, state `done`. No live target was found before the
attempt.

One launch only was made from that cwd:

```text
claude --bg --resume 48cff7d7-d148-4280-89c8-23c460de0d6c --remote-control primary-psyche-medium --model claude-opus-4-7[1m] --effort medium
```

It exited 0 but did not restore the same session. Native output said the
background session kept saved options and that passed flags started a copy:
`52ceab4e`; it reported that copy idle and awaiting a prompt. It emitted no
remote URL. To avoid leaving a duplicate target, the copy was stopped without
sending a prompt. The follow-up roster shows original `48cff7d7` still `done`
and copy `52ceab4e` `stopped` (full copy session ID
`52ceab4e-d63a-4820-b70b-843062bc8506`).

Result: no resumed live original, no native remote-control URL or status, and
therefore no laptop-visibility claim. The stated one-launch/no-retry boundary
precludes attempting an unflagged resume, which the CLI said would continue the
original but would not demonstrate the requested explicit model/effort flags.
No prompt, refresh, High message, reset, settings/permission change, or bypass
was made.
