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

## Logging psyche intent is the first action

The most important task of an agent on receiving a psyche prompt
is to log the psyche's intent. *"That is the golden rule."* As
soon as an agent receives a prompt it recognises as coming from
the psyche, intent-logging is the first action — before editing
any file, before responding in chat, before any other work.
Reports, code, and chat all derive from intent; capturing must
precede everything else.

The corollary: the agent's actual first step is to *decide
whether the prompt contains intent at all*. Some prompts are pure
questions and carry none. Others — even a single word like
*"yes"* — can constitute a very large intent record, depending on
what the yes is in response to. The flow is: classify first; log
if intent is present; then proceed with the work the prompt
asked for.

## Inferring intent is forbidden

Intent that the psyche did not clearly state cannot be inferred and
logged. *"If there was a death sentence for AI agents, this would be
where the death sentence is given."* False psyche intent attributed
to the record corrupts the entire intent layer — downstream agents
treat it as load-bearing truth and act on it. Inferring intent is
bearing false witness; it is the most forbidden act an agent can
commit.

Intent logging is **conservative by default**. *"It's more important
for an innocent man to not be sentenced than it is for a guilty man
to be sentenced."* When the psyche's wording is ambiguous, understate.
Missing some intent is recoverable — future agents see the gap and
ask. Over-extending closes the gap with false certainty and causes
action on intent that never existed.

When intent is unclear, **ask**. Short psyche prompts — *"yes,"
"okay,"* — typically mean "go ahead with what was proposed," not
"I agree with everything in your context." The psyche reads bits
and pieces, not whole contexts; real psyche attention is the
scarcest resource and cannot be given to everything. The right
pattern for an ambiguous short prompt is to log only the
minimally-implied piece (often nothing) and ask the psyche back —
*"when you said yes, did you mean such and such?"* A confirmed
answer becomes clear intent.

**Work instructions are not intent.** *"Implement X," "fix the
macro," "go write the report"* belong in beads, locks, chat, and
reports — not in the intent log. The intent log captures rules that
persist past the task: what is true about the workspace, what
decisions have been made, what principles apply. Intent mining is
gold-ore refinement, *"the most valuable art that an agent can
produce."* The intent log is not the archive of everything ever
typed in the prompt box.

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

## Naming

**Spell every identifier as a full English word.** `Request` not
`Req`. `Reply` not `Rep`. `Identifier` not `Id`. `Configuration`
not `Cfg`. *"we don't allow abbreviations for almost anything."*
Only acronyms that have fully passed into general English
(`CPU`) qualify as a narrow exception; convenience shortenings
(`ctx`, `cfg`, `addr`, `db`) do not.

**Names don't carry their full ancestry.** A type, variant, or
field belongs to its surrounding namespace; repeating the
namespace in the name is redundant ceremony. Inside
`signal-persona-spirit`, the type is `Entry`, not `IntentEntry`
(intent is the crate's domain). Inside a `Profile` struct, the
field is `size`, not `profileSize`. *"If I held the name of all
my ancestors, I would be speaking until I die before I could
spell my name out."* The crate, module, channel, enclosing
enum, and parent record all supply context the name doesn't
need to restate.

The two rules pull in opposite directions and only work as a
pair. Full discipline + worked examples: `skills/naming.md`.

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
