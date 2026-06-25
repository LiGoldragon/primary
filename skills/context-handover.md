# Skill — context handover

## Handover is a prompt, not more work

When the psyche asks for a clean-session handover, write the prompt a fresh
agent should receive. Do not continue the task inside the current degraded
context, and do not launch the subagent unless explicitly asked to launch it
now.

The prompt states:

- the workspace and repo;
- the concrete goal;
- required reading that matters for this task;
- current state, including commits, files, open decisions, and agreed defaults;
- exactly what the next main agent should do;
- any subagent role, scope, and waiting behavior the psyche requested.

## Keep it executable

Write the handover as direct instructions the next agent can paste into a new
session. Include enough context to act without scrolling chat, but keep history
only when it changes the next action.

If the next step is delegated exploration, the handover names the subagent's
bounded task and the expected return shape. The main-agent instruction says
whether to wait, stay idle, or do non-overlapping work.

## See also

- `intent-alignment.md` — one-question-at-a-time alignment.
- `context-maintenance.md` — routing reports and live context to intent, work,
  or abandon.
