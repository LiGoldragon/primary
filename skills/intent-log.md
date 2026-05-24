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

## Conservative by default — never overextend

Intent logging is **conservative by default**. Never overextend the
psyche's words. When wording is ambiguous, understate. Missing some
intent is recoverable — future agents see the gap and ask. Over-
extending closes the gap with false certainty and causes action on
intent that never existed.

Inferring intent the psyche did not clearly state is **forbidden** —
ESSENCE.md §"Inferring intent is forbidden" carries the absolute. The
intent layer is load-bearing truth; downstream agents act on it.
Attributing words the psyche did not say corrupts the system.

The asymmetry: understatement leaves a gap that future agents see and
ask about — *"the discipline is working when the agent surfaces the
gap as a question."* Over-extension closes the gap and the question
never gets asked. Prefer the recoverable failure mode.

When intent is unclear, **ask**. Short psyche prompts — *"yes,"
"okay,"* — typically mean "go ahead with what was proposed," not
"I agree with everything in your context." The psyche reads bits and
pieces; real psyche attention is the scarcest resource and cannot
be given to everything. The right pattern for an ambiguous short
prompt is to log only the minimally-implied piece (often nothing)
and ask the psyche back: *"when you said yes, did you mean such and
such?"* A confirmed answer becomes clear intent.

Prompt size is a clear indicator. **Long prompts express intent;
short prompts give green lights for action.** A short *"yes"* after
a long agent-written context is almost never blanket agreement with
the surrounding propositions — it's affirmation of whatever specific
piece caught the psyche's attention. Log only that piece; ask if
even that is ambiguous.

The intent log is **gold-ore refinement**, not the archive of
everything ever typed in the prompt box. *"Intent mining is an art.
It's the most valuable art that an agent can produce."* A future
short-term-log substrate may eventually capture all prompts and agent
inferences for historical review; until that exists, the intent
layer is reserved for material with significant intent content.

## When to record

Record every psyche statement that classifies as intent — the five
recordable kinds:

| Kind | Author shape |
|---|---|
| `Decision` | "we're going with X, not Y" |
| `Principle` | "X over Y as a general rule" |
| `Correction` | "you were wrong about X; the right thing is Y" |
| `Clarification` | "when I said X, I meant Y" |
| `Constraint` | "never do Z" |

**Record everything that classifies as intent — no filtering
at capture time.** *"Just write down the intent as it comes."*
Repetition is itself signal: when the psyche restates an intent
across sessions, the cluster of records carries the intensity.
The workspace does not dedup or filter at the log layer.
Refinement of intent — supersession, certainty lowering,
negation, dedup — is downstream (the spirit guardian arrives
with the multi-agent auditing arc per `skills/intent-maintenance.md`
§"Forward — richer supersession lifecycle").

Even short responses can carry intent. *"Let me think about that"*
is a Clarification at `Minimum` certainty — record it. *"I'm not
sure"* during brainstorming carries intent at `Minimum` — record
what was said.

A short *"yes"* or *"okay"* is harder and almost never authorizes
the full agent context that preceded it. Apply the conservative-
by-default rule: log only the minimally-implied piece (often just
the specific action the psyche is greenlighting), never the
surrounding agent reasoning. If even the minimal implication is
ambiguous, ask the psyche back at end-of-session before logging
anything beyond the bare affirmation. The short-affirmation
discipline is detailed in the "Conservative by default" section
above.

What is **not** intent (and so not recorded):

- **Pure questions** — *"How does X work?"* carries no intent;
  answer in chat, no record needed.
- **Conversational tangents** with no decision, principle,
  correction, clarification, or constraint.
- **Work instructions** — *"implement X," "fix the macro," "go
  write the report"* — task assignments that complete when the
  work completes. Future sessions don't need to know the
  directive existed; the code or result is the witness. Work
  instructions live in beads, locks, chat, reports — not the
  intent log. The test: ask *"will an agent in a different
  session need to know this fact?"* If no, it is a work
  instruction. If yes (a rule, decision, principle, name, or
  correction that persists past the task), it is intent.

A work instruction may *contain* extractable intent. *"Rename
signal-core to signal-frame"* is a work instruction, but it
contains the Decision *"signal-core is now called signal-frame."*
Log the Decision; treat the action as the work item separately
(beads, lock, report). Conversely, *"implement ToSemaOutcome now
and prove it with spirit"* contains no extractable intent — the
rule (the trait shape) was already settled elsewhere, and the
directive itself completes when the work completes.

The classification step is the only filter. The bar: *does the
statement carry intent, or is it a question or work instruction?*
If it carries intent in any of the five kinds — and only what the
psyche actually stated, not what could be inferred from it —
record it.

## Record shape

The deployed Spirit CLI accepts a NOTA `Operation` argument. For
intent capture, the operation is `Record` carrying an untagged
`Entry` (positional fields per `skills/nota-design.md`):

```nota
(Record
  (<topic>           ;; bare identifier: workspace, spirit, signal, component-shape, …
   <Kind>            ;; Decision | Principle | Correction | Clarification | Constraint
   [<summary>]       ;; terse one-line rephrasing by the agent
   [<context>]       ;; surrounding what-was-being-decided
   <Certainty>       ;; Maximum | Medium | Minimum
   [<verbatim>]))    ;; psyche's exact words; `…` for elided tangents
```

- `Entry` is untagged — no record-head ident (per the NotaRecord
  codec change). `Kind` and `Certainty` are bare PascalCase NotaEnum
  variants. `<topic>` is a bare lowercase identifier (quoted only
  if it contains spaces or PascalCase content).
- **The daemon stamps date and time on receipt.** Clients do not
  supply timestamps.

The legacy file substrate used the original shape — Kind as the
record head, no topic field (the filename supplies it), explicit
Date + Time after Certainty:

```nota
(<Kind>
    [<summary>]
    [<verbatim>]
    [<context>]
    <Certainty>
    <Date>
    <Time>)
```

This shape is history, not the normal write path. The deployed
Spirit wire shape may drift;
`skills/spirit-cli.md` covers how to read the currently deployed
shape directly from the pinned source.

The quote records **the psyche's intended words**, not the
speech-to-text layer's literal transcription. When the psyche
dictates a workspace-specific term that the STT mangles (the
canonical example — "Criom" → "Criome"; the full lookup lives in
`skills/stt-interpreter.md`'s tables of repos, libraries, tools,
and other workspace vocabulary), normalise to the canonical
spelling before storing the verbatim. Consult
`skills/stt-interpreter.md` on every verbatim recording where a
proper noun, repo name, or workspace-specific term appears.

The quote uses `…` for elided tangents — the psyche often
interleaves multiple topics in one turn, and the record only
carries the part that belongs to this entry.

## Recording goes through the Spirit CLI

The deployed `spirit` CLI is the substrate. Capture intent by
invoking it with a `Record` operation:

The command below is a temporary deployment caveat: the current
`Spirit 0.1.0` profile binary still requires legacy quote-delimited
strings. Do not generalize it to authored NOTA, whose canonical
string forms are `[text]` and `[|text|]`.

```sh
spirit '(Record (<topic> <Kind> "<summary>" "<context>" <Certainty> "<verbatim>"))'
```

The daemon stamps date and time on receipt; clients do not supply
timestamps. Invocation discipline — finding the deployed wire
shape, inline NOTA vs file-path argument, observation queries — is
in `skills/spirit-cli.md`. When the live Spirit profile supports
bracket strings, update this command and stop using bash ANSI-C
escaping for ordinary apostrophes.

### Spirit-unavailable blocker

Do not silently fall back to `intent/*.nota` appends. If Spirit is
unavailable, surface that as a blocker in chat and in the relevant
bead or report. A legacy file write is emergency maintenance only
when the psyche explicitly authorizes it.

### Supersession needs coordination regardless

Rewriting or removing prior records — supersession per
`skills/intent-maintenance.md` — needs coordinated tooling. That
holds whether the substrate is Spirit or the legacy file: a capture
protocol does not cover replacement.

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

## Topic organization — broad topics, slow split

One Spirit topic per broad semantic area — `component-shape`,
`reports`, `workspace`, `orchestrate`, `nota`, `markdown`, `jj`,
and so on. Topics are semantic routing labels, not filenames.
Entries accumulate under a broad topic as the psyche says more
about the area.

**Topics start broad and stay broad.** Resist the temptation to
name topics after a specific rule (`no-markdown-hr-breakers` is too
narrow — once it is named that, almost nothing else can fit in it).
Name topics after the area the psyche reasons about: `markdown`,
not `markdown-hr-breakers`. The broad name is where future rules
on the same area will land.

**Topics grow before they split.** A topic accumulates entries for
a long time before splitting becomes worthwhile, and only when the
entries genuinely split into two distinct sub-areas. The discipline
is *"can a reader query this topic and follow the area's intent?"*
Splitting is the exception, not the default.

**Topic convention.** Kebab-case, broad, no `intent-`, `no-`, or
`how-to-` prefixes. The topic is already in the intent substrate,
so the prefix is redundant; the negative naming smell (per
`ESSENCE.md` §"Naming") applies here too.

**When to actually split.** Two conditions both hold:
1. The topic is large enough that query results become noisy.
2. The accumulated entries cluster into two genuinely distinct
   topics — not just "lots of entries on the same area."
Carve the new topic through the maintenance tooling. Don't split
prophylactically; split when the surface earns it.

## Recording is the first task of every psyche-prompt turn

When a psyche prompt arrives, **capturing intent through Spirit is the
absolute first thing the agent does** — before editing a report,
before writing code, before responding in chat. Everything else the
prompt asked for is downstream of intent.

The session-turn shape:

1. Read the psyche's message in full.
2. Identify every intent statement — Decision, Principle,
   Correction, Clarification, Constraint. A single prompt often
   contains several across multiple topics.
3. For each: record the entry through `spirit` (or run the
   supersession protocol if it contradicts a prior — see
   `skills/intent-maintenance.md`).
4. If Spirit is unavailable, stop and surface the blocker. Do not
   revive file logging silently.
5. *Now* do the work the psyche asked for (report, code, etc.).

Reports, code, and chat all derive from intent. If you find
yourself editing a report before the intent is captured, stop and
back up. Capture first; act second.

## Recording protocol — three steps per entry

Per entry within the capture pass:

1. **Query prior entries on the topic.** Use Spirit's query surface.
   If the psyche's new statement clearly contradicts a prior,
   switch to the supersession protocol (`skills/intent-maintenance.md`).
2. **Pick the right kind.** Decision / Principle / Correction /
   Clarification / Constraint. If multiple kinds fit, take the
   strongest applicable (Constraint > Correction > Decision >
   Principle > Clarification).
3. **Write the entry through Spirit.** Terse summary; verbatim
   quote with `…` for elided tangents; context line; certainty per
   the vocabulary. The daemon stamps date and time.

The agent who recorded an entry stays accountable for re-reading it
within the session — if a later psyche statement reframes the
earlier one, the recorded entry might need supersession.

## What this skill is NOT for

- Agent-internal decisions. Those live in reports, commits, and
  documentation. Agent decisions don't go in Spirit.
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
relation tag (`(IntentTopic <topic>)`). The Spirit record identity
seeds the memory's `uid`.

No work in `persona-mind` yet. This note signposts where the
substance migrates.

## See also

- `skills/spirit-cli.md` — the deployed substrate. Invocation
  shapes, how to find the current wire shape, every operation.
- `skills/intent-maintenance.md` — sweep, supersession protocol,
  archival to `superseded/`, verification against current state.
- `skills/intent-manifestation.md` — translate recorded intent into
  the right guidance file (ESSENCE / AGENTS / skills / per-repo
  INTENT). The bridge from raw log to behaviour-shaping docs.
- `skills/nota-design.md` — the positional-NOTA discipline these
  records follow.
- `skills/stt-interpreter.md` — STT-misspelling lookup tables; consult
  before recording verbatim where workspace-specific terms appear.
- `skills/skills.nota` — the canonical positional-NOTA example.
- `intent/` — legacy file substrate; do not append during normal
  work.
- Forward: `persona-mind` typed memory variants — eventual home.
