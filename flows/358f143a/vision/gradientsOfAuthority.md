## 2026-08-18 — subflows do have harness training in the top stratum; the doc claim is false; expose the mechanism that let it linger; strata, not rung

Design session `358f143a`, typed (captured 2026-08-18T12:27+02:00).
The Designer had relayed a Claude Code doc line quoted by a
docs-only subflow — that a subagent's `.claude/agents/<name>.md` body
is its system prompt and "Subagents receive only this system prompt
plus basic environment details … not the full Claude Code system
prompt" — as verified:

> This is 100% false. theres no way the subagents have zero harness
> training. a flow already checked. why is this lie coming back? We
> have exposed flaw in our training/protocol that allows lies to
> linger. Expose the mechanism that allowed this to happen, and well
> design a fix. It may be that those prompts *do* reach the top
> strata, but they are not the entire top strata, else the model
> couldnt use the harness tools.

> strata is better than rung.

Context (agent-authored, separate from the psyche's words): the
2026-08-14 entries above already held this — the harness composes
every agent's top from its own built-in templates plus door inputs;
the agent body is one door input, not the whole. The vocabulary
term is now context strata (top / middle / bottom stratum).

## 2026-08-18 — how things work is not ruled; only the code can answer; verify in code and say so; docs are not evidence for code; document the strata in a skill; origin-of-claim rules sit on top; spirit on top

Design session `358f143a`, typed (captured 2026-08-18T13:14+02:00).
Excerpts from one message; trims between. The Designer had written
"what you had already ruled" of the psyche's 2026-08-14 statement
about subagent system prompts:

> I dont rule how things work. things work the way they work. "What
> you had ruled" -> I still dont understand what you mean. So do
> subagents not get the builtin system prompt from the harness? Only
> the code can answer.

On the doc line "a subagent gets only its .claude/agents/<name>.md
body plus basic environment details, not the full Claude Code system
prompt":

> is that how it works? Whenver this is ascertained, we need to make
> it clear somewhere that we verified this in code, so we stop
> dancing the guesswork and bluffing tune

On the Designer having told a docs-only subflow to answer from the
docs:

> docs are not for people who want to hijack a system to use it in a
> completly novel, undocumented way. Maybe we should have a hard rule
> against relying on docs for code; the code is what runs, not the
> docs.

> lets document the strata functionality in a skill

On "origin on every relayed claim, in the subflows skill":

> sounds like something that would sit on top.

> I can see a very strong overlap with many of what we want to put on
> top and spirit (I would want spirit on top in any case)

Context (agent-authored, separate from the psyche's words): facts
about the harness are ascertained from its code (or witnessed), then
recorded with the statement that they were verified in code. A
context-strata skill is to be written. Rules about the origin of
relayed claims belong to the top stratum, where spirit is also to
live.

## 2026-08-18 — the middle stratum holds the typed prompt; its source is unknown to the model

Design session `358f143a`, typed (captured 2026-08-18T15:41+02:00), on the draft
"Middle stratum: the user messages — the typed prompt, …":

> all we know is its the typed prompt. where the prompt came from is
> unknown, so we cant say its from the user

