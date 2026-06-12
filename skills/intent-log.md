# Skill — intent log

*Record what the psyche explicitly said, with kind, certainty, importance,
privacy, and a Spirit identifier, so future agents can query what the author wanted
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
load this file and `skills/spirit-cli.md` in the current context, then
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

Exploratory wording stays out of the log unless the psyche explicitly
settles it. "I think", "I feel like", "could", "maybe", "what if", and
similar phrasing normally mean brainstorming or design exploration. If the
statement seems important but not settled, ask whether to record it; do
not launder it into a firm Principle or Decision.

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
duplicates are removed without importance change and never reintroduced as a
single higher-importance record — that path is reserved for genuine psyche
repetition (`skills/intent-maintenance.md`).

## When a working order slips in anyway

A mis-logged record can be removed on psyche authority. Before removal,
preserve its full text and provenance per `skills/intent-maintenance.md`
(tombstone first). When removability is uncertain, flag rather than
remove; over-removal is worse than under-removal. Do not spree-flag or
spree-remove old mis-logs.

## Record shape

The deployed Spirit CLI accepts a NOTA `Operation`. For intent capture
the operation is `Record` carrying an untagged `RecordRequest`
(positional fields per `skills/nota-design.md`). `RecordRequest` carries
an `Entry` plus a `Justification`:

```nota
(Record
  (([<domain> ...]      ;; vector of closed taxonomy Domain values
    <Kind>              ;; Decision | Principle | Correction | Clarification | Constraint
    [<description>]     ;; clarified intent, reusing psyche wording when useful
    <Certainty>         ;; Zero | Minimum | VeryLow | Low | Medium | High | VeryHigh | Maximum
    <Importance>        ;; same ladder; repeated attention, not confidence
    <Privacy>           ;; Zero public/open; higher values narrow audience
    [<referent> ...])   ;; registered referents; usually []
   ([<statement text>]  ;; concise psyche statement supporting the capture
    None)))             ;; optional context as (Some [context]) when needed
```

- `Entry` is untagged — no record-head ident. `Kind`, `Certainty`,
  `Importance`, and `Privacy` are bare PascalCase enum variants.
- Domains are closed taxonomy values such as
  `(Information Documentation)`, `(Safety Privacy)`, and
  `(Technology (Software (Engineering SoftwareArchitecture)))`.
- `Entry` has no omission/default syntax. Spell all seven fields.
- `Justification` is also untagged: statement text, then optional context.
  Use `None` for ordinary captures; use `(Some [context])` only when the
  support would otherwise be unclear.
- Record the clarified intent as one dense description, reusing the
  psyche's own words when load-bearing.
- Spirit records carry database markers and opaque identifiers; clients
  do not supply timestamps.

The wire shape may drift; `skills/spirit-cli.md` covers reading the
currently deployed shape directly from the pinned source.

## Recording goes through the Spirit CLI

The deployed `spirit` CLI is the substrate:

```sh
spirit "(Record (([(Information Documentation)] <Kind> [description] <Certainty> <Importance> Zero []) ([psyche statement] None)))"
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

## Certainty versus importance

Certainty is part of an intent record's meaning. Do not inflate it to
make a record feel important — if every record is `Maximum`, the field
carries no information.

Certainty and importance are separate axes:

- **Certainty** — confidence in the specific statement: how sure the
  psyche sounded about this decision/principle/correction/
  clarification/constraint.
- **Importance** — how much pressure a topic carries: it keeps coming up,
  blocks other work, attracts repeated attention. Topic importance, not
  truth confidence.

Do not encode importance by raising certainty. A topic can be high-importance
and low-certainty when the psyche is probing or figuring out what they
want. A statement can be low-importance and high-certainty when it appears
once but is worded as a firm rule. At capture, choose certainty from the
wording; set importance honestly from accumulated attention and repetition.
The deployed `Importance` field is explicit; never smuggle importance into
the certainty value.

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

Repetition usually raises importance, not certainty. Before choosing `High`
or above, query prior records on the topic. If the same settled
statement keeps returning with stronger commitment, that recurrence is
evidence for higher certainty. If the topic merely keeps returning
because it is unresolved or contested, it is high importance but not high
certainty — keep it at the certainty the wording carries. A first clear
mention without strong certainty language stays at `Medium`.

`VeryLow` and `VeryHigh` are available when the wording clearly asks for
a finer notch than `Low` or `High`; do not invent precision the phrasing
does not carry. Certainty calibrates a record only after the gate
already says Record.

## Domain, keyword, and referent organization

Production Spirit uses three retrieval layers:

- **Domains** — closed taxonomy buckets for broad routing. Choose one or
  more coarse domains that genuinely fit the intent. Use
  `(Information Documentation)` for documentation/skill/report guidance,
  `(Technology (Software (Quality Testing)))` for testing discipline,
  `(Technology (Software (Engineering SoftwareArchitecture)))` for system
  design, `(Technology (Software (Data SchemaEvolution)))` for schema
  evolution, `(Safety Privacy)` for privacy boundaries, and
  `(Technology (Software (Intelligence AgentSystems)))` for agent/LLM
  tooling.
- **Description keywords/text** — free words live in the clarified
  description. Query them with `KeywordMatch` or `ContainsText`; keep
  narrow ad hoc tags there.
- **Referents** — named entities that should remain stable across
  descriptions. Only use the referent vector for registered referents;
  otherwise leave it empty as `[]`.

The old topic discipline still applies conceptually: choose broad
routing concepts, avoid filename-like or negative labels, and split only
when query results prove noisy. The wire field is the closed `Domains`
vocabulary.

## If the gate says Record

1. Query prior entries by domain plus keyword/text for contradiction and certainty.
2. Pick the kind, certainty, importance, and privacy.
3. Write one dense description through `spirit`; the daemon returns the
   short identifier and database marker.

If the gate says no capture, Observe, or ask, do not write a record.

## Citing intent in prose — bracket-quote the summary

Reference intent records in prose markdown by quoting the description
summary literally as bracketed text. The identifier is an opaque address;
the bracketed substance is the load-bearing citation. Especially in
psyche-facing reports, and wherever an intent is central to a document,
quote it literally in a prominent place.

> Per Spirit abcd (Decision High): [Generated engine traits carry
> minimal lifecycle hooks: on_start and on_stop with typed failure
> results.]

The brackets are the citation marker. Spirit identifiers are random
opaque lowercase base36 shortest-unique-prefix codes, minimum four
characters.

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
