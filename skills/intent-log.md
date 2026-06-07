# Skill — intent log

*Record what the psyche explicitly said, with kind, certainty, and a
daemon-stamped time, so future agents can query what the author wanted
versus what some agent decided.*

## What this skill is for

Only psyche statements are recorded. The psyche is the human author —
natural-language prompts to the agent, not NOTA persona messages
between agents, not agent-written files. Agent decisions go in reports,
commits, and documentation, never here.

Documentation records *decisions*; the intent log records *who
decided*. When a skill says "the daemon takes one binary startup
argument," the reader can't tell whether that came from the psyche or
from an agent who wrote it down. That asymmetry is the whole point:

- An agent proposing to contradict something needs to know whether the
  prior statement was author intent (load-bearing) or an earlier
  agent's writing (possibly hallucination).
- Two documents that contradict each other can be ranked by which has a
  corresponding intent record.
- An agent verifying "did the author actually want this?" can query the
  log.

The log is a back-reference, not a front-line discipline document. Most
agent reading still happens through skills, ARCHITECTURE.md, and
reports; the intent log surfaces only when the author's voice is the
question.

## Spirit gate — classify before any write

Spirit writes are conservative. Before any `spirit "(Record …)"`,
answer the gate:

1. Is this an exact psyche statement, not agent inference?
2. Does it still guide after the current task is erased?
3. Is it a Decision, Principle, Correction, Clarification, or Constraint?
4. Is the privacy axis clear?

Outcomes:

- **No capture** — pure question, tangent, task-only order,
  current-state reaction, or brainstorming without a settled want.
- **Observe/refresh** — context is needed. "Refresh intent" means
  query/read recent Spirit records, not write a record or edit
  `INTENT.md` / `ARCHITECTURE.md`.
- **Ask** — durable meaning, kind, or privacy is unclear.
- **Record** — explicit durable psyche intent passes the gate.

No-capture is normal. Understatement is recoverable; over-extension
corrupts the load-bearing intent layer.

## Privacy gate before recording

Public workspace intent uses privacy `Zero`. Private or
personal-affairs substance must never be recorded at `Zero`; use
elevated Spirit privacy only when explicitly authorized, otherwise
write the private-report note per `skills/privacy.md`.

## Recordable kinds

Only explicit durable psyche statements in these five shapes are
recordable:

- `Decision` — "we're going with X, not Y".
- `Principle` — "X over Y as a general rule".
- `Correction` — "you were wrong about X; the right thing is Y".
- `Clarification` — "when I said X, I meant Y".
- `Constraint` — "never do Z".

A task instruction may contain a durable statement: "rename
signal-core to signal-frame" carries a naming decision; "write the
report" does not. Record only the durable part; the task itself goes to
beads, locks, reports, or chat. Repetition is signal, but duplicates
and supersession are maintenance work
(`skills/intent-maintenance.md`), not an excuse to write uncertain
entries.

## Non-recordable shapes

Do not record pure questions, tangents, task-only instructions,
current-state updates, or reactions that state no durable rule. Short
affirmations usually greenlight the immediate action only; ask if
unclear.

## Capture is not done until it manifests into the affected repo's INTENT.md

Recording the Spirit record is the first half. When an intent record
affects a specific repository's design, implementation, or test
direction — whether scoped to that repo or workspace-level intent that
reaches it — that intent is manifested into the affected repo's
`INTENT.md` as part of the work cycle, not a deferred later pass. Per-
repo `INTENT.md` is the canonical agent-context surface. If intent
lives only in Spirit and chat, an agent opening the repo reads stale
framing and codes to the wrong shape. Every repo carries an
`INTENT.md`; its absence is a gap to fill. Discipline:
`skills/repo-intent.md`.

## One capturer when a prompt addresses multiple lanes

When a psyche prompt explicitly addresses more than one lane (e.g.
*"operator needs to understand this… and designer will do the
refresh"*), exactly one lane records the intent — by default the lane
that responds first. In practice the operator (Codex) responds far
faster than the designer (Claude), so the operator usually writes the
Spirit entry and the slower lane gap-checks rather than re-recording.
The rule: first responder records; do not pre-record in parallel.

Both lanes engaging with the substance is correct; both lanes logging
the same record is the recurring duplicate failure. A prompt addressed
to you is yours to capture; in the multi-addressee case, designate one
capturer and let the others query recent records, confirm the capture
covers the intent, and gap-fill only a genuine omission. Mistaken
duplicates are removed without weight change and never reintroduced as a
single higher-weight record — that path is reserved for genuine psyche
repetition (`skills/intent-maintenance.md`).

## When a working order slips in anyway

A mis-logged record can be removed on psyche authority. Before removal,
preserve its full text and provenance per `skills/intent-maintenance.md`
(tombstone first). When removability is uncertain, flag rather than
remove; over-removal is worse than under-removal. Do not spree-flag or
spree-remove old mis-logs.

## Record shape

The deployed Spirit CLI accepts a NOTA `Operation`. For intent capture
the operation is `Record` carrying an untagged `Entry` (positional
fields per `skills/nota-design.md`):

```nota
(Record
  ([<topic> ...]     ;; vector of topic identifiers: workspace, spirit, signal, …
   <Kind>            ;; Decision | Principle | Correction | Clarification | Constraint
   [<description>]   ;; clarified intent, reusing psyche wording when useful
   <Certainty>       ;; Zero | Minimum | VeryLow | Low | Medium | High | VeryHigh | Maximum
   <Privacy>))       ;; Zero public/open; higher values narrow audience
```

- `Entry` is untagged — no record-head ident. `Kind` and `Certainty`
  are bare PascalCase enum variants. Topics are a vector of lowercase
  identifiers; use a bracket string only if a topic contains spaces or
  PascalCase content.
- `Entry` accepts a four-field public shorthand that defaults privacy to
  `Zero`, but use the explicit five-field form when privacy
  classification matters.
- Spirit stores no separate context or verbatim fields. Record the
  clarified intent as one dense description, reusing the psyche's own
  words when load-bearing.
- The daemon stamps date and time on receipt; clients do not supply
  timestamps.

The wire shape may drift; `skills/spirit-cli.md` covers reading the
currently deployed shape directly from the pinned source.

## Recording goes through the Spirit CLI

The deployed `spirit` CLI is the substrate:

```sh
spirit "(Record ([<topic> ...] <Kind> [description] <Certainty> Zero))"
```

Inline NOTA wraps the whole object in shell double quotes; authored
NOTA strings use bracket forms, so apostrophes appear naturally inside
the payload. Invocation discipline — finding the deployed wire shape,
inline vs file-path argument, observation queries — is in
`skills/spirit-cli.md`.

If Spirit is unavailable when a record is required, surface that as a
blocker in chat and in the relevant bead or report. There is no
legacy-file fallback — the `intent/*.nota` substrate is retired; Spirit
is the sole substrate. Supersession (rewriting or removing prior
records, per `skills/intent-maintenance.md`) needs coordinated tooling
regardless of substrate; a capture protocol does not cover replacement.

## Certainty versus weight

Certainty is part of an intent record's meaning. Do not inflate it to
make a record feel important — if every record is `Maximum`, the field
carries no information.

Certainty and weight are separate axes:

- **Certainty** — confidence in the specific statement: how sure the
  psyche sounded about this decision/principle/correction/
  clarification/constraint.
- **Weight** — how much pressure a topic carries: it keeps coming up,
  blocks other work, attracts repeated attention. Topic importance, not
  truth confidence.

Do not encode weight by raising certainty. A topic can be high-weight
and low-certainty when the psyche is probing or figuring out what they
want. A statement can be low-weight and high-certainty when it appears
once but is worded as a firm rule. At capture, choose certainty from the
wording; preserve weight by using broad reusable topics and recording
repeated probes as repeated records at honest certainty. A `Weight`
field is a future record-shape design; until it lands, weight is
inferred from topic recurrence and work churn, never smuggled into the
certainty value.

If the psyche explicitly marks a statement as low-certainty, first query
Spirit for the topic. If an older higher-certainty record bundles a
settled part and a tentative part, split the truth: keep the settled
part at its earned certainty, then add a low-certainty
correction/clarification for the tentative part. Do not let one
high-certainty record shelter a low-certainty sub-claim.

### The ladder

Judge how sure the psyche actually was (conviction), not how important
the topic is. A very important decision the psyche is only moderately
sure of is `Medium`, not `Maximum`.

- **`Maximum`** — Near-absolute, founding-rule conviction: a universal
  axiom that could stand as a founding rule of the whole way of working,
  or one the psyche explicitly elevated (*"put this in essence"*).
  Genuinely rare — most sessions capture none. Examples: intent is
  primordial; inferring intent is forbidden; spell every identifier as a
  full English word. Test: would this still be a founding rule a year
  from now, across every repo and role? A revisable design or
  implementation choice is *not* `Maximum`, however firmly stated.
- **`VeryHigh`** — Very firm, emphatic, near-irreversible, but scoped to
  one discipline rather than a universal axiom. Stated with
  *"never"*/*"always"* and real consequences. Uncommon.
- **`High`** — Clear, firm intent stated with conviction. The normal
  home for a real decision — most decisions land here, not at `Maximum`.
- **`Medium`** — The default. A preference, direction, or lean without
  strong emphasis. When in doubt, `Medium` — it is honest, not weak.
- **`Low` / `VeryLow`** — Tentative to half-formed: *"we could"*,
  *"maybe"*, *"I think"*, brainstorm-level.
- **`Minimum`** — Weak but real: mentioned in passing, little
  conviction, might matter later.
- **`Zero`** — Not a conviction level: the recoverable removal marker
  (superseded, duplicate, mis-captured).

The psyche is not an omniscient god — no human states every sentence
with absolute certainty, so `Maximum` cannot be the reflex. If you are
reaching for `Maximum`, ask: did the psyche state a universal founding
rule, or just a firm decision? A firm decision is `High`. Under-rating
is recoverable; over-rating corrupts the signal. Justify any move above
`Medium` with evidence in the prompt or prior records.

Repetition usually raises weight, not certainty. Before choosing `High`
or above, query prior records on the topic. If the same settled
statement keeps returning with stronger commitment, that recurrence is
evidence for higher certainty. If the topic merely keeps returning
because it is unresolved or contested, it is high weight but not high
certainty — keep it at the certainty the wording carries. A first clear
mention without strong certainty language stays at `Medium`.

`VeryLow` and `VeryHigh` are available when the wording clearly asks for
a finer notch than `Low` or `High`; do not invent precision the phrasing
does not carry. Certainty calibrates a record only after the gate
already says Record.

## Topic organization — broad topics, slow split

One Spirit topic per broad semantic area — `component-shape`, `reports`,
`workspace`, `orchestrate`, `nota`, `markdown`, `jj`, and so on. Topics
are semantic routing labels, not filenames. Entries accumulate under a
broad topic as the psyche says more about the area.

Topics start broad and stay broad. Resist naming a topic after a
specific rule (`no-markdown-hr-breakers` is too narrow — once named
that, almost nothing else fits). Name topics after the area the psyche
reasons about: `markdown`, not `markdown-hr-breakers`. The broad name is
where future rules on the same area land.

Topic convention: kebab-case, broad, no `intent-`, `no-`, or `how-to-`
prefixes — the prefix is redundant in the intent substrate, and the
negative-naming smell (`ESSENCE.md` §"Naming") applies here too.

Split compounds into the topic vector when the concepts stand alone.
Prefer `[intent logging]` over `[intent-log]` when the substance is
about both; prefer `[spirit privacy]` over `[spirit-privacy]` when
privacy is a reusable topic outside Spirit. Keep a hyphenated topic only
when the compound names one established thing (`signal-frame`, a
component name, a domain term that stops meaning the same thing when
split). The vector is how Spirit represents several topics; don't hide
that structure in one narrow string.

Actually split only when both hold: (1) the topic is large enough that
query results become noisy, and (2) the accumulated entries cluster into
two genuinely distinct topics, not just "lots of entries on the same
area." Carve the new topic through the maintenance tooling. Don't split
prophylactically; split when the surface earns it.

## If the gate says Record

1. Query prior entries on the topic for contradiction and certainty.
2. Pick the kind, certainty, and privacy.
3. Write one dense description through `spirit`; the daemon stamps time.

If the gate says no capture, Observe, or ask, do not write a record.

## Citing intent in prose — bracket-quote the summary

Reference intent records in prose markdown by quoting the description
summary literally as bracketed text — the bracketed form IS the
citation — not by record number alone. The number is an opaque address;
the substance is what's load-bearing, and repeating it reinforces the
intent. Especially in psyche-facing reports, and wherever an intent is
central to a document, quote it literally in a prominent place.

The form is LITERAL bracketed text in square brackets — not italicized,
not double-quoted approximation. Markdown handles `[bracketed text]`
cleanly; the only edge case is link syntax, which requires zero-space
`[text](url)`.

Wrong (number-only):

> Per Spirit 1487, lifecycle hooks land on the engine traits.

Wrong (italicized double-quote approximation):

> Per Spirit 1487 (Decision High): *"Generated engine traits carry
> minimal lifecycle hooks: on_start and on_stop with typed failure
> results."*

Right (literal bracketed text IS the citation):

> Per Spirit 1487 (Decision High): [Generated engine traits carry
> minimal lifecycle hooks: on_start and on_stop with typed failure
> results.]

The brackets are the citation marker; no italics, no double quotes. The
identifier remains an address for a reader who wants to look up the
record; the bracketed substance is what the cite carries into the
document. Spirit identifiers are random opaque lowercase base36
shortest-unique-prefix codes, minimum four characters.

Markdown rendering: `[text] (Spirit N)` with a space before the
parenthetical renders as bracketed text plus parenthetical; only
`[text](url)` with no space triggers link syntax — easy to avoid.
Brackets are safe in CommonMark, GitHub Flavored Markdown, VS Code
preview, and Obsidian.

Apply this especially in psyche reports, skill files where an intent is
central, `ESSENCE.md` / `INTENT.md` synthesis, and per-repo `INTENT.md`
/ `ARCHITECTURE.md` when manifesting workspace intent. In chat replies
and short cross-references, bracket-quoting can be condensed or omitted
when the substance is already named inline.

## What this skill is NOT for

- Agent-internal decisions — those live in reports, commits, and
  documentation.
- A replacement for ARCHITECTURE.md or skills. The intent log captures
  what the author said; the architecture captures what the system is.
- Long-form analysis. The log carries terse, queryable intent
  descriptions; analysis goes in reports.

## Forward — persona-mind migration

When persona-mind's typed memory variants land, each `<Kind>` record
becomes a memory of variant `Authorial<Kind>` (`AuthorialDecision`,
`AuthorialPrinciple`, …), topic becomes a relation tag
`(IntentTopic <topic>)`, and the Spirit record identity seeds the
memory's `uid`. No work in `persona-mind` yet; this signposts where the
substance migrates.

## See also

- `skills/spirit-cli.md` — the deployed substrate: invocation shapes,
  current wire shape, every operation.
- `skills/intent-maintenance.md` — sweep, supersession, tombstoning,
  verification against current state.
- `skills/intent-manifestation.md` — translate recorded intent into the
  right guidance file (ESSENCE / AGENTS / skills / per-repo INTENT).
