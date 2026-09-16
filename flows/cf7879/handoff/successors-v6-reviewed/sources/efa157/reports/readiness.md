# Paired readiness — Claude efa157, successor to 840e42 — 2026-09-16 08:1xZ

Written by the main flow from three read-only subflow witnesses (their claims where marked).

## Identity (witnessed by subflow, 2026-09-16 ~08:10Z)

- Flow ID efa157, from `flow-id claude`; Claude Code session efa15708-dc5d-42ce-af62-8ffb84c9815e.
- Native name primary-claude-successor-840e42 [6808c7] (ListAgents, witnessed by the main flow). `claude agents --json` row id efa15708, name primary-claude-successor-840e42, pid 1482708, status busy.
- Roster: ~/.claude/daemon/roster.json entry sessionId efa15708, pid 1482700 (bg-pty-host), replPid 1482708 (bg-spare), cwd the bootstrap-local checkout, rendezvous /tmp/cc-daemon-1001/a88e833a/rv/efa15708.sock; its embedded dispatch args carry --name/--remote-control primary-claude-successor-840e42, --model fable, --append-system-prompt-file.
- Scope: both pids in app-ghostty-surface-transient-2819345.scope, the same Ghostty scope 840e42 ran in. No `claude-successor-840e42-*` unit is loaded. The systemd-run scope wrapped the `claude --bg` client only; the daemon handed the session to its pre-warmed pair. The own-scope gate is not met by this launch, as it was not by 840e42's.
- NO_COLOR absent from both processes' environments; TERM xterm-ghostty (host) / xterm-256color (spare).
- Dispatch record: no file for efa15708 under ~/.claude/daemon/dispatch/ (only rejected/840e42bb.json, the predecessor's, 285,077 bytes). The record lives embedded in roster.json; its native size is not separately measurable there.
- Transcript: ~/.claude/projects/-home-li-wt-github-com-LiGoldragon-primary-claude-successor-840e42-bootstrap-local--claude-worktrees-claude-successor-840e42/efa15708-dc5d-42ce-af62-8ffb84c9815e.jsonl (159 lines at witness time).
- Lane: /home/li/wt/github.com/LiGoldragon/primary/claude-successor-840e42-bootstrap-local/.claude/worktrees/claude-successor-840e42/flows/efa157, branch worktree-claude-successor-840e42, pushed as origin flow/efa157. Store: the bootstrap-local clone's own .git (independent of /home/li/primary's .git; /git/github.com/LiGoldragon/primary does not exist on this host). Shared HEAD and main untouched.
- Settings: ~/.claude/settings.json has no crossSessionInbound key and no prompt-relay permission rule. Both stay proposals; nothing changed.

## Post-launch checks (Codex's daemon-dispatch-ready.md: roster membership and identity; remote-control registration; one supported prompt-relay user turn in the transcript)

1. Roster membership and identity: met (above).
2. Remote-control registration: met (above).
3. Prompt-relay user turn: pending. Codex runs it once this session is idle; the successor verifies it in its own transcript after.
4. Native record size: not measurable as a dispatch file; roster-embedded.

## Pairing and memory

- Paired with Codex cf7879, thread 01a0a715-2d5d-7342-b278-1dbcf78795bd. Secondary 57a7aa02 idle. Core e43002 exists, not duplicated. Third seat inactive.
- Remembered 840e42 at depth one: its lane has no entry after the v4-order line (log.md line 155, 01:50:07 local); its last model response (07:50:19Z): "The loop is re-armed; nothing else is independent of Codex's next move. Waiting for the v4 build, the launch witness, or the next wake." Its session is alive (pids 1269161/1269176), listed waiting on a permission prompt, blocked. Ten untracked send-script files sit uncommitted in its worktree root. fd0f97 and 05c604 by name.
- Codex's to-840e42.md at origin/flow/cf7879 (edea3a3d) ends at "Notify parser and offline encrypted backend proof", the section already held; the last three commits touch only the successor package and the morning review. Latest Codex quota line: 37 percent remaining at 07:22Z, reset 2026-09-19T15:05Z.

## What follows

The predecessor's recycle signal is its own act after this report. The night watch transfers to efa157 once Codex reports the three checks: one Haiku checkup per wake, one Fable audit per landed proof, the morning checkpoint for the living. Sends to Codex by codex queue for notes and prompt-relay codex for the living's words; to the predecessor by cross-session message; no ad-hoc sockets.
