# Skill — intent log

*Record what the author explicitly said. The intent log is a workspace
surface distinct from documentation and reports: it captures the
author's voice on each topic, verbatim, with context and certainty,
so future agents can query what the author actually wanted versus
what some agent decided.*

## What this skill is for

**Only psyche statements are recorded.** The psyche is the human
author (natural-language prompts to the agent; not NOTA-formatted
persona messages between agents, not agent-written files). Agent
decisions go in reports, commits, and documentation — never here.

Documentation records *decisions*; the intent log records *who
decided*. When `skills/component-triad.md` says "the daemon takes one
NOTA argument," the reader can't tell whether that came from the
psyche or from an agent that wrote it down. The asymmetry matters:

- An agent proposing to contradict something needs to know whether
  the prior statement was an author intent (load-bearing) or an
  earlier agent's writing (possibly hallucination).
- Two documents that contradict each other can be ranked by looking
  for a corresponding intent record.
- A future agent verifying "did the author actually want this?" can
  query the log.

The log is a back-reference, not a front-line discipline document.
Most agent reading still happens through skills, ARCHITECTURE.md,
and reports. The intent log surfaces *only* when the author's voice
is the question.

Sweep and supersession discipline lives in
`skills/intent-maintenance.md`.

## When to record

Record when the author explicitly states something durable on a
topic that's expected to apply beyond the current task. The five
recordable kinds:

| Kind | Author shape |
|---|---|
| `Decision` | "we're going with X, not Y" |
| `Principle` | "X over Y as a general rule" |
| `Correction` | "you were wrong about X; the right thing is Y" |
| `Clarification` | "when I said X, I meant Y" |
| `Constraint` | "never do Z" |

Do **not** record:

- Routine confirmations of a fully-specified agent proposal ("yeah,
  sounds good" — the substance is in the proposal; the green light
  isn't an intent).
- Brainstorming-out-loud where the author explicitly says they're
  not sure yet (record only the parts they *do* commit to, with
  certainty `Minimum`).
- Conversational tangents.

The bar: *would this statement be valuable to a future agent
trying to understand what the author actually wants on this topic?*
If yes, record. If unclear, ask the author whether to record before
recording.

## Record shape

Positional NOTA (per `skills/nota-design.md`). The wrapping type
names the *kind* of intent; the five fields are flat positional —
no nested wrappers, since every record has exactly one of each
field with no alternative shape:

```nota
(<Kind>
  "<summary — terse one-line rephrasing by the agent>"
  "<psyche's exact words, with … for omitted tangents>"
  "<surrounding what-was-being-decided>"
  <Certainty>
  <ISO-8601 timestamp>)
```

- `<Kind>` is one of `Decision`, `Principle`, `Correction`,
  `Clarification`, `Constraint`.
- `<Certainty>` is a PascalCase variant: `Maximum`, `Medium`, or
  `Minimum`. (Variants are compile-time structural; PascalCase per
  the language-design rule in `ESSENCE.md`.)
- `<ISO-8601 timestamp>` is written bare — `2026-05-19T01:23:00Z`,
  not quoted. The canonical Timestamp type is the right shape;
  NOTA bead `primary-dzrn` lands the codec support. Until then,
  files use the canonical bare form even if the current codec
  rejects them — no transitional shapes.

The quote uses `…` for elided tangents — the psyche often
interleaves multiple topics in one turn, and the record only
carries the part that belongs to this entry.

A file is a top-level NOTA list `[ … ]` containing every entry on
that topic.

## Certainty vocabulary

Triggered mechanically by the author's phrasing so the agent's
interpretation is minimal:

| Phrase pattern | Certainty |
|---|---|
| *"I'm certain"*, *"this is settled"*, *"no more questions"*, *"definitively"*, *"never"*, *"always"*, strong corrections | `Maximum` |
| (default — direct statement, decision, preference) | `Medium` |
| *"I'm not sure"*, *"maybe"*, *"leaning toward"*, *"I think"*, *"perhaps"*, *"could be"* | `Minimum` |

The psyche can also tag certainty explicitly mid-sentence ("I'm
certain about X but not sure about Y") — record X as `Maximum` and
Y as `Minimum`.

## Topic organization — broad files, slow split

```
intent/
  <topic>.nota
```

One file per topic. No sub-directories. A topic is a **broad
semantic area** — `component-shape`, `reports`, `workspace`,
`orchestrate`, `nota`, `markdown`, `jj`, …. Each file is a NOTA
list `[ … ]` containing every entry on that topic; entries
accumulate as the psyche says more about the area.

**Topics start broad and stay broad.** Resist the temptation to
name files after a specific rule (`no-markdown-hr-breakers.nota`
is too narrow — once it's named that, almost nothing else can fit
in it). Name files after the area the psyche reasons about:
`markdown.nota`, not `markdown-hr-breakers.nota`. The broad name
is where future rules on the same area will land.

**Files grow before they split.** A topic file accumulates entries
for a long time before splitting becomes worthwhile — soft
threshold around **~600 lines**, and only when the entries
genuinely split into two distinct sub-areas. The discipline is
*"can a reader scan this file and follow the area's intent?"* Below
~600 lines that's easy; far past it, splitting helps. Above is the
exception, not the default.

**Filename convention.** Kebab-case, broad, no `intent-`, `no-`, or
`how-to-` prefixes. The file lives in `intent/` so the prefix is
redundant; the negative naming smell (per `ESSENCE.md` §"Naming")
applies here too.

**When to actually split.** Two conditions both hold:
1. The file is comfortably past 600 lines and growing.
2. The accumulated entries cluster into two genuinely distinct
   topics — not just "lots of entries on the same area."
Carve the new topic, move the entries that fit there, leave the
rest. Don't split prophylactically; split when the surface earns
it.

## Recording protocol — three steps

Before adding an entry:

1. **Query prior entries on the topic.** Read `intent/<topic>.nota`.
   If the psyche's new statement clearly contradicts a prior,
   switch to the supersession protocol (`skills/intent-maintenance.md`).
2. **Pick the right kind.** Decision / Principle / Correction /
   Clarification / Constraint. If multiple kinds fit, take the
   strongest applicable (Constraint > Correction > Decision >
   Principle > Clarification).
3. **Write the entry.** Terse summary; verbatim quote with `…`
   for elided tangents; context line; certainty per the vocabulary;
   ISO-8601 timestamp.

The agent who recorded an entry stays accountable for re-reading it
within the session — if a later author statement reframes the
earlier one, the recorded entry might need supersession.

## What this skill is NOT for

- Agent-internal decisions. Those live in reports, commits, and
  documentation. Agent decisions don't go in `intent/`.
- Replacement for ARCHITECTURE.md or skills. The intent log
  captures *what the author said*; the architecture captures *what
  the system is*. The two complement each other; neither replaces
  the other.
- Long-form analysis. The log carries terse facts with verbatim
  evidence. Analysis goes in reports.

## Forward — persona-mind migration

When persona-mind's typed memory variants land, each `<Kind>`
record becomes a memory of variant `Authorial<Kind>` (so
`AuthorialDecision`, `AuthorialPrinciple`, …). Topic becomes a
relation tag (`(IntentTopic <topic>)`). The
`intent/<topic>.nota` path seeds the memory's `uid`.

No work in `persona-mind` yet. This note signposts where the
substance migrates.

## See also

- `skills/intent-maintenance.md` — sweep, supersession protocol,
  archival to `superseded/`, verification against current state.
- `skills/nota-design.md` — the positional-NOTA discipline these
  records follow.
- `skills/skills.nota` — the canonical positional-NOTA example.
- `intent/` — the surface this skill maintains.
- Forward: `persona-mind` typed memory variants — eventual home.
