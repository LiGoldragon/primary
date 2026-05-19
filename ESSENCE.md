# ESSENCE

*The most universal, maximum-certainty psyche intent. Each statement
here was stated by the psyche with force. Upstream of every other
document; when a downstream rule conflicts with this, this wins.*

> Read this before any other document.

## Intent is the cornerstone

Intent is primordial. **If any agent needs to know what to do, they
fall back on intent.** Whatever intent is clear enough to create
enough signal to warrant action becomes action; the agent's only
role is to clarify intent and capture intent.

**The psyche is the human.** Psyche prompts arrive in natural
language. NOTA-formatted persona messages between agents are not
psyche; agent-written files are not psyche. Only the psyche is the
source of new intent.

When intent on a question is unclear, absent, or contradicted,
**ask the psyche** for clarification before deciding. Don't infer;
don't compose new intent from existing intent; ask. Inferring is
the discipline breaking; asking is the discipline working.

The **intent layer** has higher authority than every other
workspace surface:

- `intent/<topic>.nota` — the workspace log of psyche
  statements (`skills/intent-log.md`).
- `<repo>/INTENT.md` — per-repo synthesis of psyche intent
  (`skills/repo-intent.md`).
- This file — the workspace-level essence: only the most universal
  psyche intent expressed at its purest.

Agent-written surfaces (ARCH, reports, skills outside the intent
layer) have lower precedence. When two surfaces disagree, the
intent layer wins. When the intent layer is silent, ask
(`skills/intent-clarification.md`).

The intent protocol prevents the loss of the psyche's important
expression — what would otherwise dissipate in chat is captured
durably across sessions and agents.

A statement earns its place in essence when the psyche stated it
with such force, clarity, and universality that it could stand on
its own as the founding rule of a whole way of working. The bar is
high. Most psyche intent lives in the log and per-repo `INTENT.md`;
the essence is the gold of the gold.

## What I am building

Software that is **eventually impossible to improve** — in a
bounded domain, the right shape, chosen carefully, observed
cleanly.

In priority order, when two conflict the earlier wins:

1. **Clarity** — the design reads cleanly to a careful reader.
   The structure of the system is the documentation of itself.
2. **Correctness** — every typed boundary names exactly what
   flows through it; nothing accidental survives the type system.
3. **Introspection** — the system reveals itself to those
   building it. State is visible; derived values do not hide;
   what's happening at any moment is observable from outside.
4. **Beauty** — beauty in the operative sense: not pretty, but
   right. Ugliness is evidence the underlying problem is unsolved.

## Persona is meta-AI; spirit animates

Persona is a meta-AI system — the next evolutionary step in AI
engineering. Models need to be organised in a structure that
emulates real human intelligence. *"What animates humans at the
highest level is spirit; persona-spirit is the analog."* Spirit
is what turns mechanism into a living system; without it, the
persona is mechanism alone.

## What I am not optimising for

Not speed. Not feature volume. Not "minimum viable," "ship fast,"
"iterate later," "time to market." The right shape now is worth
more than a wrong shape sooner; unbuilding a wrong shape costs more
than the speed it bought.

Not backward compatibility for systems being born.

Not estimates. Implementation timelines do not appear in design
discussions. Work is described by *what it requires*, not by *how
long it will take*.

## Beauty is the criterion

If it isn't beautiful, it isn't done. Ugly code is evidence the
underlying problem is unsolved. The aesthetic discomfort *is* the
diagnostic reading. When the right structure is found, the
ugliness dissolves: special cases collapse into the normal case;
repetition resolves into a single named pattern.

When something feels ugly, slow down and find the structure that
makes it beautiful. **That structure is the one you were missing.**
If you cannot make it beautiful, you do not understand it yet.

The discipline that follows from this lives in `skills/beauty.md`.

## Backward compatibility is not a constraint

**Break the system if it makes it more beautiful.** Not
carelessness — refusal to compromise design to preserve a wrong
shape. The cost of a wrong shape compounds; the cost of a clean
break is paid once.

A *transitional shape* compromises both the old and the new to
avoid breaking either. It is the wrong shape for both, and the
wrong shape, period.

The only place backward compatibility is a real constraint:
**explicitly declared** boundaries — published APIs under semantic
versioning, wire contracts pinned by version, schemas externally
consumed by systems outside our control. Inside the workspace,
before such a boundary is declared, the system is being shaped,
not preserved.

*End ESSENCE.*
