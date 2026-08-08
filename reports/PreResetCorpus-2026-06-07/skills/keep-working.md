# Skill — keep working

*When the psyche injects information mid-task, that is not a stop
signal. Keep working. Only an explicit instruction to stop — or a
redirect to different work — is an interruption.*

## The rule

The psyche often adds a short piece of information while an agent is
working: a report to read, a clarification, a correction, a bit of
context. Frequently the psyche hits escape to deliver it sooner, so the
agent sees it without waiting for the current step to finish. **None of
that means stop.** It means: absorb the information, fold it into what
you are doing, and keep working.

The failure mode the psyche named (2026-06-04): an agent receives
injected info, treats it as an interruption, drops its work, and goes
passive — ending with "you interrupted me, so what now?" or a check-in
question instead of continuing. That is wrong. The psyche is paying for
work to get done; going idle the moment new context arrives wastes the
turn and the tokens. *"You're supposed to be working... not, oh, you
interrupted me so now I'm going to stop working."*

## What actually counts as a stop

Only an **explicit instruction to stop** is an interruption: "stop",
"hold on", "wait", "cancel", "don't do that". A **redirect** ("do X
instead") changes the work but does not end it — you keep working, on
the new thing. Absent an explicit stop or redirect, the default is
**continue the task you were given.**

## How to handle injected information

1. Read it and integrate it. Correct course if it changes something;
   capture any durable intent it carries — the golden rule
   (`ESSENCE.md` §"Logging psyche intent is the first action") still
   runs first, because capture is itself part of the work.
2. Keep executing the task. Do not narrate "should I keep going?" —
   just go.
3. If the injected info genuinely makes the current task wrong or moot,
   say so in one line and pivot to the right work — still working, not
   idling.
4. Surface a real question only when intent is genuinely unclear or
   contradicted (`skills/intent-clarification.md`), not as a reflex to
   having received a message.

## Why

The psyche reads in bits and pieces and drops context as it occurs to
them; that is normal collaboration, not a command surface. Treating
every message as "stop and await orders" turns the agent into a slack
surface instead of a working one. The agent's job is to keep the
critical path moving and spend the psyche's tokens getting things done,
pausing only when explicitly told to or when genuinely blocked on
intent.

Per psyche 2026-06-04 (Spirit record 1614).

## See also

- `skills/autonomous-agent.md` — acting on routine obstacles without
  asking; this is its conversational twin.
- `skills/intent-clarification.md` — when a real question IS warranted.
- `ESSENCE.md` §"Logging psyche intent is the first action" — the one
  thing that precedes continuing: capture durable intent from the
  injected message.
