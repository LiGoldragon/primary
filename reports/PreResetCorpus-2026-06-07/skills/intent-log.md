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
binary startup argument," the reader can't tell whether that came from
the psyche or from an agent that wrote it down. The asymmetry matters:

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

## Spirit gate — classify before any write

Spirit writes are conservative. Before any `spirit "(Record …)"`,
answer the gate:

1. Is this an exact psyche statement, not agent inference?
2. Does it still guide after the current task is erased?
3. Is it a Decision, Principle, Correction, Clarification, or Constraint?
4. Is the privacy axis clear?

Gate outcomes:

- **No capture** — pure question, tangent, task-only order, current-state
  reaction, or brainstorming without a settled want.
- **Observe/refresh** — context is needed. The phrase **"refresh intent"**
  means query/read recent Spirit records, not write a new record or edit
  repo `INTENT.md` / `ARCHITECTURE.md` files.
- **Ask** — durable meaning, kind, or privacy is unclear.
- **Record** — explicit durable psyche intent passes the gate.

No-capture is normal. Understatement is recoverable; over-extension
corrupts the load-bearing intent layer.

## Privacy gate before recording

Public workspace intent uses privacy `Zero`. Private or personal-affairs
substance must never be recorded at privacy `Zero`; use elevated Spirit
privacy only when explicitly authorized, otherwise write the relevant
private-report note per `skills/privacy.md`.

## Recordable kinds

Only explicit durable psyche statements in these five shapes are
recordable:

- `Decision` — "we're going with X, not Y".
- `Principle` — "X over Y as a general rule".
- `Correction` — "you were wrong about X; the right thing is Y".
- `Clarification` — "when I said X, I meant Y".
- `Constraint` — "never do Z".

A task instruction may contain a durable statement. Record only the
durable statement; the task itself goes to beads, locks, reports, or
chat. Repetition is signal, but duplicates and supersession are
maintenance work (`skills/intent-maintenance.md`), not an excuse to
write uncertain entries.

## Capture is not done until it manifests into the affected repo's INTENT.md

Recording the Spirit record is the first half. When an intent record
affects a specific repository's design, implementation, or test
direction — whether explicitly scoped to that repo or workspace-level
intent that reaches it — that intent is **manifested into the affected
repo's `INTENT.md`** as part of the work cycle, not a deferred later
pass. Per spirit record 944 (Maximum, 2026-05-27): per-repo `INTENT.md`
is the canonical agent-context surface, and manifestation belongs in
the work cycle. If intent lives only in Spirit and chat, an agent
opening the repo reads stale framing in `INTENT.md` and codes to the
wrong shape — the failure mode 944 corrects. Every repo carries an
`INTENT.md`; its absence is a gap to fill. Discipline:
`skills/repo-intent.md` §"Continuous manifestation discipline".

## One capturer when a prompt addresses multiple lanes

When a psyche prompt explicitly addresses **more than one lane** (e.g.
*"operator needs to understand this… and designer will do the refresh"*),
the intent is recorded by **exactly one** lane — by default the lane that
**responds first**. In practice that is the **operator** (Codex responds
far faster than the designer, Claude), so the operator usually writes the
Spirit entry first and the slower lane **gap-checks** rather than
re-recording. The rule is *first responder records; do not pre-record in
parallel*. Both lanes *engaging with the substance* is correct; both lanes
*logging the same Spirit record* is the recurring duplicate failure (the pairs `24ds`, `js6q`/`pv61`,
`ydvg`/`fkbz`, `de8i`/`v5n7`, `gvaz`/`z6qu` were all exactly this —
mistaken two-agent duplication, not genuine psyche repetition). The
forwarded-prompt discipline (`AGENTS.md` §"forwarded prompts") says a
prompt addressed to you is yours to capture; this extends it to the
multi-addressee case: designate one capturer, and the others query recent
records, confirm the capture covers the intent, and gap-fill only a
genuine omission. Mistaken duplicates are removed without weight change;
they are never reintroduced as a single higher-weight record (that path is
reserved for *genuine* psyche repetition — `skills/intent-maintenance.md`).

## Non-recordable shapes

Do not record pure questions, tangents, task-only instructions,
current-state updates, or reactions that do not state a durable rule.
Short affirmations usually greenlight the immediate action only; ask if
unclear.

A work instruction can contain durable intent. Example: "rename
signal-core to signal-frame" contains a naming decision; "write the
report" does not. Record only the durable part.

## When a working order slips in anyway

A mis-logged record can be removed on psyche authority. Before removal,
preserve its full text and provenance per `skills/intent-maintenance.md`
§"Removing a record — tombstone first". When removability is uncertain,
flag rather than remove; over-removal is worse than under-removal. Do
not spree-flag or spree-remove old mis-logs.

## Record shape

The deployed Spirit CLI accepts a NOTA `Operation` argument. For
intent capture, the operation is `Record` carrying an untagged
`Entry` (positional fields per `skills/nota-design.md`):

```nota
(Record
  ([<topic> ...]     ;; vector of topic identifiers: workspace, spirit, signal, …
   <Kind>            ;; Decision | Principle | Correction | Clarification | Constraint
   [<description>]   ;; clarified intent, reusing psyche wording when useful
   <Certainty>        ;; Zero | Minimum | VeryLow | Low | Medium | High | VeryHigh | Maximum
   <Privacy>))        ;; Zero public/open; higher values narrow audience
```

- `Entry` is untagged — no record-head ident (per the NotaRecord
  codec change). `Kind` and `Magnitude` are bare PascalCase NotaEnum
  variants. Topics are a vector of lowercase identifiers; use a
  bracket string only if a topic contains spaces or PascalCase content.
- `Entry` accepts a four-field public shorthand that defaults privacy
  to `Zero`, but agents should use the explicit five-field form when
  privacy classification matters.
- Production Spirit v0.5.2 does not store context or verbatim fields. The agent's
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
spirit "(Record ([<topic> ...] <Kind> [description] <Certainty> Zero))"
```

The daemon stamps date and time on receipt; clients do not supply
timestamps. Invocation discipline — finding the deployed wire
shape, inline NOTA vs file-path argument, observation queries — is
in `skills/spirit-cli.md`. Inline NOTA uses shell double quotes
around the whole object; authored NOTA strings use bracket strings,
so apostrophes can appear naturally inside the NOTA payload.

### Spirit-unavailable blocker

If Spirit is unavailable, surface that as a blocker in chat and in
the relevant bead or report — there is no legacy-file fallback; the
`intent/*.nota` substrate is retired. Spirit is the sole substrate.

### Supersession needs coordination regardless

Rewriting or removing prior records — supersession per
`skills/intent-maintenance.md` — needs coordinated tooling. That
holds whether the substrate is Spirit or the legacy file: a capture
protocol does not cover replacement.

## Magnitude vocabulary

Certainty is part of the meaning of an intent record. Do not inflate
it to make the record feel important. If every record is `Maximum`,
then the certainty field has been destroyed.

### Certainty versus weight

Certainty and weight are separate axes.

**Certainty** means confidence in the specific statement being recorded:
how sure the psyche sounded about this decision, principle, correction,
clarification, or constraint.

**Weight** means how much pressure a topic or concern carries in the
workspace: it keeps coming up, blocks other work, attracts repeated
attention, or needs resolution. Weight is topic importance, not truth
confidence.

Do not encode weight by raising certainty. A topic can be high-weight
and low-certainty when the psyche is probing, testing, or trying to
figure out what they want. A statement can be low-weight and
high-certainty when it appears once in passing but is worded as a firm
rule or decision.

At capture time, choose certainty from the wording and context of the
specific statement. Preserve weight by using broad reusable topics and
by recording repeated probes as repeated records at honest certainty.
The explicit `Weight` field is a future, low-certainty record-shape
design: when it lands, it is set as its own axis, especially to preserve
the accumulated importance of agglomerated source records. Until then,
weight is inferred from topic recurrence and report/work churn, never
smuggled into the certainty value.

### When the psyche says a statement is low-certainty

If the psyche explicitly marks a statement as low-certainty, do not just
record the new low-certainty entry and move on. First query Spirit for
the topic. If an older higher-certainty record already contains the same
idea, inspect whether that record mixed two different certainty levels.

When a higher-certainty record bundles a settled part and a tentative
part, split the truth in Spirit: keep or record the settled part at its
earned certainty, then add a low-certainty correction/clarification for
the tentative part. Do not let a single high-certainty record shelter a
low-certainty sub-claim.

### The ladder — what situation each level is for

Judge **how sure the psyche actually was** (conviction), not how
important the topic is. Importance and certainty are different axes:
a very important decision the psyche is only moderately sure of is
`Medium`, not `Maximum`.

- **`Maximum`** — Near-absolute, founding-rule conviction: the psyche
  stated a universal axiom that could stand as a founding rule of the
  whole way of working, or explicitly elevated it (*"put this in
  essence"*). The gold of the gold. **Genuinely rare — most sessions
  capture none.** Examples: intent is primordial; inferring intent is
  forbidden; spell every identifier as a full English word; break the
  system if it makes it more beautiful. Test: would this still be a
  founding rule a year from now, across every repo and role? A design
  or implementation choice that could be revised is *not* `Maximum`,
  however firmly stated.
- **`VeryHigh`** — Very firm, emphatic, near-irreversible, but
  scope-limited to one discipline rather than a universal axiom.
  Stated with *"never"* / *"always"* and real consequences. Uncommon.
  Example: landed means on main; never report branch work as landed.
- **`High`** — Clear, firm intent stated with conviction: a genuine
  decision or principle the psyche committed to. **The normal home for
  a real decision.** Most decisions land here, not at `Maximum`.
- **`Medium`** — **The default.** A preference, direction, or lean
  without strong emphasis; normal-conviction wording. When in doubt,
  `Medium`. A `Medium` capture is not weak — it is honest.
- **`Low` / `VeryLow`** — Tentative to half-formed: *"we could"*,
  *"maybe"*, *"I think"*, brainstorm-level.
- **`Minimum`** — Weak but real: mentioned in passing, little
  conviction, might matter later.
- **`Zero`** — Not a conviction level: the recoverable removal marker
  (superseded, duplicate, mis-captured).

**The psyche is not an omniscient god.** No human states every
sentence with absolute certainty, so `Maximum` cannot be the reflex.
If you are reaching for `Maximum`, stop and ask: did the psyche state
a *universal founding rule*, or just a firm decision? A firm decision
is `High`. Over-rating destroys the signal — when everything is
`Maximum`, the field carries no information and the psyche cannot tell
what they were actually sure about. Under-rating is the recoverable
error (the innocent-man principle); over-rating corrupts. The agent
must justify any move above `Medium` with evidence in the prompt or in
prior records.

**Repetition usually raises weight, not certainty.** Before choosing
`High`, `VeryHigh`, or `Maximum`, query recent/prior records on the
topic. If the same settled statement keeps returning across records with
the same direction and stronger commitment, that recurrence is evidence
for higher certainty. If the topic merely keeps returning because it is
unresolved, confusing, contested, or under exploration, it is high
weight but not high certainty. Keep those records at the certainty the
wording actually carries. If the current prompt is the first clear
mention and lacks strong certainty language, stay at `Medium`.

Triggered mechanically by the author's phrasing and prior-record
evidence so the agent's interpretation is minimal:

| Phrase pattern | Magnitude |
|---|---|
| Explicit maximum-intensity statement; repeated emphatic correction; settled founding rule with repeated Spirit history | `Maximum` |
| *"I'm certain"*, *"this is settled"*, *"no more questions"*, *"definitively"*, *"never"*, *"always"*, or strong but not absolute correction | `High` / `VeryHigh` unless the prompt or log history truly warrants `Maximum` |
| strong but not absolute emphasis | `High` |
| (default — direct statement, decision, preference) | `Medium` |
| explicit low-certainty but durable rule or preference | `Low` / `Minimum` |

`VeryLow` and `VeryHigh` are available when the psyche's wording
clearly asks for a finer notch than `Low` or `High`; do not invent
precision when the phrasing does not carry it. Certainty calibrates a
record only after the Spirit gate already says Record.

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

## If the gate says Record

1. Query prior entries on the topic for contradiction and certainty.
2. Pick the kind, certainty, and privacy.
3. Write one dense description through `spirit`; the daemon stamps time.

If Spirit is unavailable when a record is required, surface the blocker;
there is no legacy-file fallback — the `intent/*.nota` substrate is
retired. If the gate says no capture, Observe, or ask, do not write a
record.

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
The identifier remains as an address for the reader who wants to
look up the record; the bracketed substance is what the cite carries
forward into the document. Production Spirit v0.5.2 uses random opaque
record identifiers rendered as lowercase base36 shortest-unique-prefix
codes with a minimum of four characters. Repetition
of the substance across documents reinforces the intent layer's
authority: a reader following the citation chain encounters the
load-bearing words at each link, not just opaque pointers.

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
- Forward: `persona-mind` typed memory variants — eventual home.
