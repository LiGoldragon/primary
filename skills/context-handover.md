# Skill — context handover

## Handover preserves decision power

When the psyche asks for a clean-session handover, write the prompt a fresh
agent should receive. The handover is an information map: what accumulated,
where the evidence lives, which topics matter, and what is still uncertain.

The fresh agent keeps its own judgment. A handover does not decide the next
agent's work for it, except when the psyche has already given an explicit
instruction; in that case quote the instruction as psyche instruction rather
than turning it into agent inference.

## What to carry

Name the accumulated context that would otherwise be lost:

- workspace, repo, lane, and relevant discipline;
- the user's goal and any exact psyche instructions;
- current state: commits, files, reports, beads, Spirit records, claims, and
  working-copy status when relevant;
- topics discovered so far and why each one matters;
- source locators for where to read next;
- agreed defaults and the evidence behind them;
- unresolved questions, forks, and uncertainty.

## Make retrieval easy

The next agent should be able to enter with fresh context, read the named
sources, and make its own decision. Prefer compact locators and state over
process narrative. When a subagent is part of the intended continuation, name
the exploration topic, boundaries, and useful return shape; leave synthesis and
choice to the next main agent unless the psyche has explicitly fixed them.

## See also

- `intent-led-orchestration.md` — fresh-context focused-question alignment and
  orchestration.
- `context-maintenance.md` — routing reports and live context to intent, work,
  or abandon.
