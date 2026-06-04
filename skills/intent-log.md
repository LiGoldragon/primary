# Skill — intent log

*Record what the author explicitly said. The intent log is a workspace
surface distinct from documentation and reports: it captures a dense
agent-clarified description of the author's intent on each topic,
with kind, magnitude, and daemon-stamped time, so future agents can
query what the author actually wanted versus what some agent decided.*

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

## Privacy gate before recording

Before any ordinary Spirit `Record`, classify whether the content is
public or private. Personal-affairs substance, private life context,
sensitive plans, health, relationships, finances, identity material,
and anything the psyche frames as private does **not** go into ordinary
Spirit. Record only privacy-safe meta-policy in ordinary Spirit. Until
a private Spirit substrate exists, private intent becomes a `Private
intent` note in the relevant private report repository per
`skills/privacy.md`.

## When to record

Record every public psyche statement that classifies as intent — the five
recordable kinds:

| Kind | Author shape |
|---|---|
| `Decision` | "we're going with X, not Y" |
| `Principle` | "X over Y as a general rule" |
| `Correction` | "you were wrong about X; the right thing is Y" |
| `Clarification` | "when I said X, I meant Y" |
| `Constraint` | "never do Z" |

**Record everything public that classifies as intent — no filtering
at capture time except the privacy gate above.** *"Just write down the intent as it comes."*
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

## The pre-capture gate — the after-the-task test

The classification rule above is known and still gets violated:
agents over-capture because they log the prompt's VERB instead of
testing the SENTENCE. This gate is the keystroke check. Before
every `spirit "(Record …)"`, apply the test to the exact sentence
you are about to log:

> *Erase the current task. Is this sentence still meaningful and
> still guiding future work?*

If it dies with the task, it is a working order — do not log it; it
goes in the session task list or a bead. The shapes that keep
slipping through (all working orders, none intent):

| Logged as Decision/Constraint | Why it fails the test |
|---|---|
| "Create a report on X and test it" | dead once the report exists |
| "Dispatch a subagent to finish X" | dead once X is finished |
| "Audit Y and write up the findings" | dead once the audit lands |
| "Operator: integrate these branches" | dead once integrated |
| "Psyche asks this lane to review Z" | dead once reviewed |

The good-call pattern is to extract the durable shape hiding inside a
working order. If the psyche asks for research on expanding Spirit's
interface, don't log "research Spirit". Log the persistent desired
surface instead: "Spirit command surfaces should offer simple-to-
complex operation variants: concise summary defaults for normal use,
and explicit full-metadata/custom forms for advanced use." The report
or task carries the research; Spirit carries the lasting principle.

Contrast — these pass (still guide after any task): "schema is the
source of truth" (Principle), "the Plane is a data-carrying enum"
(Decision), "working orders aren't intent" (Correction). The
pattern: **durable intent describes what the system IS or how to
work; a working order describes what to do next.** Capture the
first; the second is task state. A task prompt that carries no
durable want logs nothing — a no-capture turn is correct, not a
miss.

## When a working order slips in anyway

Deployed Spirit now supports explicit removal (records 1103/1189),
so a mis-logged record can be **removed** on psyche authority — not
only flagged. Log a short `Correction` naming the record number and
that it was an over-capture, pointing to where the durable intent
(if any) actually lives; then remove the mis-log once the psyche
authorizes, **capturing its full text and provenance first** per
`skills/intent-maintenance.md` §"Removing a record — tombstone
first". When removability is uncertain, flag rather than remove
(record 1103: over-removal is worse than under-removal). Do not
spree-flag or spree-remove old mis-logs — act as noticed and rely on
the pre-capture gate above to stop new ones; a cleanup spree would
itself churn the log being kept lean.

## Record shape

The deployed Spirit CLI accepts a NOTA `Operation` argument. For
intent capture, the operation is `Record` carrying an untagged
`Entry` (positional fields per `skills/nota-design.md`):

```nota
(Record
  ([<topic> ...]     ;; vector of topic identifiers: workspace, spirit, signal, …
   <Kind>            ;; Decision | Principle | Correction | Clarification | Constraint
   [<description>]   ;; clarified intent, reusing psyche wording when useful
   <Magnitude>))     ;; Zero | Minimum | VeryLow | Low | Medium | High | VeryHigh | Maximum
```

- `Entry` is untagged — no record-head ident (per the NotaRecord
  codec change). `Kind` and `Magnitude` are bare PascalCase NotaEnum
  variants. Topics are a vector of lowercase identifiers; use a
  bracket string only if a topic contains spaces or PascalCase content.
- Spirit v0.3 does not store context or verbatim fields. The agent's
  job is to record the clarified intent as one dense description,
  reusing the psyche's own words when they are load-bearing.
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

## Recording goes through the Spirit CLI

The deployed `spirit` CLI is the substrate. Capture intent by
invoking it with a `Record` operation:

```sh
spirit "(Record ([<topic> ...] <Kind> [description] <Magnitude>))"
```

The daemon stamps date and time on receipt; clients do not supply
timestamps. Invocation discipline — finding the deployed wire
shape, inline NOTA vs file-path argument, observation queries — is
in `skills/spirit-cli.md`. Inline NOTA uses shell double quotes
around the whole object; authored NOTA strings use bracket strings,
so apostrophes can appear naturally inside the NOTA payload.

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

## Magnitude vocabulary

Certainty is part of the meaning of an intent record. Do not inflate
it to make the record feel important. If every record is `Maximum`,
then the certainty field has been destroyed.

**Medium is the default for ordinary direct intent.** A clear psyche
statement, decision, preference, or instruction-with-durable-intent
is normally `Medium`. The agent must justify any upward move from
`Medium` with evidence in the prompt or in prior Spirit records.

**Maximum is rare.** Use it only when the psyche explicitly signals
near-absolute conviction: strong universal language, intense
correction, repeated emphatic phrasing, or an established rule that
has recurred across the intent log enough that the current prompt is
obviously reinforcing it. A direct "do X" is not Maximum by itself.

**Repetition can raise certainty.** Before choosing `High`,
`VeryHigh`, or `Maximum`, query recent/prior records on the topic.
If the same intent keeps returning across records, that recurrence is
evidence for higher certainty. If the current prompt is the first
clear mention and lacks strong certainty language, stay at `Medium`.

Triggered mechanically by the author's phrasing and prior-record
evidence so the agent's interpretation is minimal:

| Phrase pattern | Magnitude |
|---|---|
| Explicit maximum-intensity statement; repeated emphatic correction; settled founding rule with repeated Spirit history | `Maximum` |
| *"I'm certain"*, *"this is settled"*, *"no more questions"*, *"definitively"*, *"never"*, *"always"*, or strong but not absolute correction | `High` / `VeryHigh` unless the prompt or log history truly warrants `Maximum` |
| strong but not absolute emphasis | `High` |
| (default — direct statement, decision, preference) | `Medium` |
| weak leaning with real signal | `Low` |
| *"I'm not sure"*, *"maybe"*, *"leaning toward"*, *"I think"*, *"perhaps"*, *"could be"* | `Minimum` |

`VeryLow` and `VeryHigh` are available when the psyche's wording
clearly asks for a finer notch than `Low` or `High`; do not invent
precision when the phrasing does not carry it.

The psyche can also tag magnitude explicitly mid-sentence ("I'm
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

**Split compounds into the topic vector when the concepts stand
alone.** Prefer `[intent logging]` over `[intent-log]` when the
substance is about both intent and logging. Prefer `[spirit
privacy]` over `[spirit-privacy]` when privacy is a reusable topic
outside Spirit too. Keep a hyphenated topic only when the compound
names one established thing (`signal-frame`, a component name, or a
domain term that stops meaning the same thing when split). The vector
is how Spirit represents several topics; don't hide that structure in
one narrow string.

**When to actually split.** Two conditions both hold:
1. The topic is large enough that query results become noisy.
2. The accumulated entries cluster into two genuinely distinct
   topics — not just "lots of entries on the same area."
Carve the new topic through the maintenance tooling. Don't split
prophylactically; split when the surface earns it.

## Recording is the first task of every psyche-prompt turn

When a psyche prompt arrives, **capturing intent through the right
intent substrate is the absolute first thing the agent does** — before
editing a report, before writing code, before responding in chat.
Everything else the prompt asked for is downstream of intent. Public
intent goes through ordinary Spirit; private personal substance follows
`skills/privacy.md` instead of ordinary Spirit.

The session-turn shape:

1. Read the psyche's message in full.
2. Identify every intent statement — Decision, Principle,
   Correction, Clarification, Constraint. A single prompt often
   contains several across multiple topics.
3. For each public entry: record it through `spirit` (or run the
   supersession protocol if it contradicts a prior — see
   `skills/intent-maintenance.md`). For private personal substance,
   write a `Private intent` note in the matching private report repo
   until private Spirit exists.
4. If Spirit is unavailable, stop and surface the blocker. Do not
   revive file logging silently.
5. *Now* do the work the psyche asked for (report, code, etc.).

Reports, code, and chat all derive from intent. If you find
yourself editing a report before the intent is captured, stop and
back up. Capture first; act second.

## Recording protocol — three steps per entry

Per entry within the capture pass:

1. **Query prior entries on the topic.** Use Spirit's query surface.
   Use the results for two things: contradiction detection and
   certainty calibration. Repeated same-direction records can justify
   `High` / `VeryHigh`; contradiction switches to the supersession
   protocol (`skills/intent-maintenance.md`). If the statement is new
   and the prompt lacks strong certainty language, default to
   `Medium`.
2. **Pick the right kind.** Decision / Principle / Correction /
   Clarification / Constraint. If multiple kinds fit, take the
   strongest applicable (Constraint > Correction > Decision >
   Principle > Clarification).
3. **Write the entry through Spirit.** One dense description that
   clarifies the intent and reuses the psyche's wording where it is
   load-bearing; magnitude per the vocabulary. The daemon stamps
   date and time.

The agent who recorded an entry stays accountable for re-reading it
within the session — if a later psyche statement reframes the
earlier one, the recorded entry might need supersession.

## Citing intent in prose — bracket-quote the summary

Per psyche 2026-06-03 (Spirit 1522 + 1526): [Reference intent
records in prose markdown by quoting the description summary
literally as bracketed text — the bracketed form IS the citation
— not by the record number alone. Repetition reinforces intent:
the number is an opaque address, the substance is what's
load-bearing. Especially in psyche-facing reports, and wherever
an intent is central to a document, quote it literally in a
prominent place. Applies to all agents.]

Per psyche 2026-06-03 (Spirit 1533 Correction Maximum): [The
bracket-quote citation discipline means LITERAL bracketed text in
square brackets — not italicized plus double-quoted approximation.
Markdown handles `[bracketed text]` cleanly; the only edge case is
link syntax which requires zero-space `[text](url)`. The form
prescribed is the literal bracket form.]

Wrong shape (number-only citation):

> Per Spirit 1487, lifecycle hooks land on the engine traits.

Wrong shape (italicized double-quote approximation, what some
agents drifted to):

> Per Spirit 1487 (Decision High): *"Generated Signal, Nexus, and
> SEMA engine traits should carry minimal lifecycle hooks:
> on_start and on_stop with typed start and stop failure
> results."*

Right shape (literal bracketed text IS the citation):

> Per Spirit 1487 (Decision High): [Generated Signal, Nexus, and
> SEMA engine traits should carry minimal lifecycle hooks:
> on_start and on_stop with typed start and stop failure
> results.]

The brackets are the citation marker; no italics, no double quotes.
The number remains as an address for the reader who wants to look
up the record; the bracketed substance is what the cite carries
forward into the document. Repetition of the substance across
documents reinforces the intent layer's authority — a reader
following the citation chain encounters the load-bearing words at
each link, not just numeric pointers.

Markdown rendering note: `[text] (Spirit N)` with a space between
the closing bracket and the parenthetical renders as bracketed
text followed by the parenthetical. The only form that triggers
link syntax is `[text](url)` with no space — easy to avoid.
Brackets are safe in CommonMark, GitHub Flavored Markdown, VS Code
preview, and Obsidian.

Apply this discipline especially in:

- Psyche reports (per `skills/reporting.md` §"Psyche reports —
  show the code, not the summary" — the same self-contained
  rationale).
- Skill files where an intent is central (the rule's source).
- ESSENCE.md and INTENT.md prose synthesis.
- Per-repo INTENT.md / ARCHITECTURE.md when manifesting workspace
  intent into a repo's surface.

For chat replies and short cross-references, bracket-quoting can
be condensed or omitted when the substance is already named
inline; the discipline is about written documents where the
citation does the load-bearing work.

## What this skill is NOT for

- Agent-internal decisions. Those live in reports, commits, and
  documentation. Agent decisions don't go in Spirit.
- Replacement for ARCHITECTURE.md or skills. The intent log
  captures *what the author said*; the architecture captures *what
  the system is*. The two complement each other; neither replaces
  the other.
- Long-form analysis. The log carries terse, queryable intent
  descriptions. Analysis goes in reports.

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
  before writing descriptions that include workspace-specific terms.
- `skills/skills.nota` — the canonical positional-NOTA example.
- `intent/` — legacy file substrate; do not append during normal
  work.
- Forward: `persona-mind` typed memory variants — eventual home.
