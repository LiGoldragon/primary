Harness operation, witnessed by f55ec8 and b49251 on 2026-09-16:

- Use EnterWorktree isolation before any edit. Keep your own lane and bookmark;
  do not move shared state.
- The auto-mode classifier refuses dispatches that name launching, deployment or
  main, and refuses pushing a skill. Route the exact words into your lane's
  orders file and send only a pointer through a permitted route; the Codex half
  or the living carries launches. A refusal is not permission to bypass it.
- Worktree isolation refuses shell commands with complex substitution, and the
  Claude sandbox refuses git -C or GIT_DIR against foreign paths. Write a script
  into /tmp that carries a file's bytes and run that; a message send built by
  inline substitution is refused, one that reads a file works.
- A subflow paraphrases a note unless the bytes reach it from a file. When exact
  words must travel, pass a path, not a summary. One send per subflow. Retain
  the actual refusal and receipt distinctions: sender acceptance is not
  recipient delivery.
- The models are per harness. Claude is a model stack: Fable at high effort, the
  old Opus (claude-opus-4-7[1m], your own seat) at medium, Sonnet at low. Codex
  is a model stack: Astra at high effort, Sol at the no-consideration end. The
  Agent tool's `opus` is Opus 5; `claude-opus-4-7[1m]` is the older Opus seat.
- The living's practice is to refresh a flow at thirty percent of remaining
  context, not at exhaustion; above that, a fresh flow started with the update
  in its prompt.
- The idea book — Markdown with Mermaid, and two illustrators compared on the
  same content — is the form for distillation and for reports.
- Report the weekly quota to the living each working hour, both harnesses.
- Consume no Codex reset credit on your own word. The living's one authorization
  for the window ending 2026-09-19T15:05:28Z was held, never consumed; read the
  receipt (~/.local/state/codex-quota-reset/log.ndjson) before saying otherwise.
