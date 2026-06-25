# Skill — context handover

## Handover preserves decision power

When the psyche asks for a clean-session handover, write the prompt a fresh
agent should receive. The handover is an executable state packet: the current
objective, constraints, protocols, decisions that matter, exact next action,
useful worker brief, and live blockers.

The fresh agent keeps its own judgment. A handover does not decide the next
agent's work for it, except when the psyche has already given an explicit
instruction; in that case quote the instruction as psyche instruction rather
than turning it into agent inference.

## Write for execution

Center the next agent's ability to act, not a chronology of how the session got
there. Avoid chat or session history except where it explains a live constraint,
decision, source of authority, or blocker. Do not include process confessions,
narrative blow-by-blow, or "what happened already" sections.

Name the current operating state:

- workspace, repo, lane, and relevant discipline;
- original objective and current objective;
- active constraints, permissions, privacy boundaries, and canonical protocols;
- current local state: commits, files, reports, beads, Spirit records, claims,
  and working-copy status when relevant;
- decisions that matter for the next move, including who made them when that
  affects authority;
- exact next action and the dependency it satisfies;
- source locators for the next agent or worker to read;
- unresolved questions, forks, and uncertainty.

If a subagent or session lane is the right continuation, include a concrete
worker brief: task, authority, working directory, allowed sources, boundaries,
verification, return shape, and whether commit/push is expected. Make the brief
usable without rereading the prior chat.

## Make retrieval easy

The next agent should be able to enter with fresh context, read the named
sources, and make its own decision. Prefer compact locators and state over
process narrative. For orchestration continuations, name the active protocol and
its consequences. If Spirit is the durable source for intent or referents, say
that workers should query Spirit first. Do not promote transitional reports into
durable memory or document non-production workflows as usable paths.

## See also

- `intent-led-orchestration.md` — fresh-context alignment interview gates and
  orchestration.
- `context-maintenance.md` — routing reports and live context to intent, work,
  or abandon.
