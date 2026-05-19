# 230 — Author-intent log: proposal

*A workspace surface for recording, by topic, what the author explicitly
said — distinct from what agents have decided. Terse summary plus
verbatim quote plus context plus certainty plus timestamp, organised in
topic directories. Eventually migrates to a typed `persona-mind` memory
variant. This report carries the proposal and the open questions for
the author to settle.*

---

## 0 · TL;DR

A new top-level directory holds one NOTA file per sub-topic. Each file
contains typed records — one record per author statement — declaring:

- a terse rephrasing of what the author meant
- the verbatim quote with surrounding context
- a certainty marker (`maximum` / `medium` / `minimum`)
- a timestamp

Records are positional NOTA. Each record's wrapping type names the
*kind* of intent: `Decision`, `Principle`, `Correction`, `Clarification`,
`Constraint`. Topic is the directory; sub-topic is the file.

Cleanup is by explicit supersession — an agent encountering a new
author statement on a topic queries prior entries, and if the new
statement contradicts, surfaces the contradiction (with the prior quote
+ context inline) for the author to confirm before recording. No silent
override.

Five open questions for the author at §6.

---

## 1 · Why this surface exists

Workspace documents (ARCHITECTURE.md, skills, reports) record
*decisions*. They don't record *who decided*. When a doc says "the
daemon takes one NOTA argument," the reader can't tell whether that
came from the author or from an agent that wrote it down.

The asymmetry matters when:

- An agent later proposes contradicting something the author said
  (vs. contradicting what an earlier agent wrote). The author's
  statement is load-bearing; an earlier agent's might be hallucination
  surviving in plain prose.
- Two documents contradict each other and there's no way to rank
  which decision is authoritative.
- A future agent wants to verify "did the author actually want this,
  or is this an agent assumption that compounded?"

The intent log gives agents a way to answer *"what has the author
explicitly said about this topic?"* — distinct from *"what does the
documentation currently say?"*

---

## 2 · Record shape

NOTA, positional. Wrapping type names the intent's kind (per
`skills/nota-design.md` Rule 1: "the wrapping type names the most
useful distinction in context"). Five kinds:

| Kind | Author shape |
|---|---|
| `Decision` | "we're going with X, not Y" |
| `Principle` | "X over Y as a general rule" |
| `Correction` | "you were wrong about X; the right thing is Y" |
| `Clarification` | "when I said X, I meant Y" |
| `Constraint` | "never do Z" |

Positional fields, in order:

1. **summary** — a single-string terse rephrasing by the agent
2. **verbatim** — a nested `Verbatim` record (quote then context)
3. **certainty** — bare enum: `maximum`, `medium`, or `minimum`
4. **when** — ISO-8601 timestamp string

Example record (this very rule, recorded against itself):

```nota
(Decision
  "Intent records use positional NOTA with kind-typed wrapping"
  (Verbatim
    "thats not NOTA, and your response is too long ... the agents.md has a sections describing the skills.nota file, which should go in that file"
    "Correcting the labeled-field NOTA I sketched in chat; framing it as the same mistake many agents make")
  maximum
  "2026-05-19T22:30:00Z")
```

A `Verbatim` record is itself positional: `(Verbatim quote context)`.
Quote allows `…` for elided tangents (the author often interleaves
multiple topics in one turn; the recording only carries the part that
belongs to this record).

---

## 3 · Directory shape

```
<name>/
  component-shape/
    single-nota-argument.nota
    policy-working-state-split.nota
    triad-authority-tiers.nota
    sub-scope-handoff-forbidden.nota
  reports/
    rename-protocol.nota
    no-dates-in-filenames.nota
    chat-vs-report-discipline.nota
  workspace/
    agents-md-stays-compact.nota
    skills-grow-noisy-warning.nota
  orchestrate/
    persona-orchestrate-is-a-real-component.nota
    no-fold-into-mind.nota
  nota/
    positional-not-labeled.nota
  jj/
    no-jj-describe-on-working-copy.nota
  ...
```

One file per sub-topic; each file is a NOTA list `[ … ]` of one or
more records on that point. The topic is the directory name; the
sub-topic is the filename. Cowboy-style today; migrates cleanly to a
persona-mind memory variant when that ships (each record becomes a
memory; topic becomes a relation tag).

---

## 4 · Certainty vocabulary

Triggered by the author's phrasing so the recording is mechanical and
the agent's interpretation is minimal:

| Phrase pattern | Certainty |
|---|---|
| *"I'm certain"*, *"this is settled"*, *"no more questions"*, *"definitively"*, *"never"*, *"always"* | `maximum` |
| (default — direct statement, decision, preference) | `medium` |
| *"I'm not sure"*, *"maybe"*, *"leaning toward"*, *"I think"*, *"perhaps"*, *"could be"* | `minimum` |

The author can also tag certainty explicitly mid-sentence ("I'm
certain about X but not sure about Y") — the agent records X with
maximum and Y with minimum.

---

## 5 · Cleanup / supersession protocol

When an agent receives a new author statement on a topic:

1. **Query prior entries.** Read every record in `<name>/<topic>/`.
2. **If the new statement contradicts a prior:** surface the
   contradiction *before* recording — quote the prior verbatim and its
   certainty inline, then ask: *"You said earlier X (certainty Y); now
   you're saying Z. Override, or am I misreading?"*
3. **On confirmed override:** add a `Superseded` record alongside the
   new entry that names the old entry's path and the new one's:

   ```nota
   (Superseded
     "old-entry-filename"
     "new-entry-filename"
     "2026-05-19T22:35:00Z")
   ```

   …and physically move the prior record's file to
   `<name>/<topic>/superseded/`. The supersession history is itself
   data, queryable.
4. **On clarification (not override):** record the new entry; both
   stay valid. The new entry typically has kind `Clarification`.

Supersession is **always explicit, never silent**. An author entry
never gets quietly overwritten by another author entry. This is the
load-bearing protection against agent hallucination passing as author
intent.

---

## 6 · Open questions for the author

### N — Naming the directory

Strongest candidates (one word):

| Name | Feel | Risk |
|---|---|---|
| `intent/` | direct; the word you reached for | soft collision with ESSENCE.md "workspace intent" |
| `testimony/` | captures the verbatim-quote-with-context character | possibly biblical/legal tone |
| `mandate/` | "what the author mandated"; authoritative | too imperial for `minimum`-certainty entries |
| `canon/` | "the canon of author statements" | implies settled doctrine; too strong for `minimum` |
| `voice/` | "the author's voice on X" | maybe too soft |

Recommendation: **`intent/`** — the ESSENCE collision is semantic
overlap, not clash (ESSENCE = workspace intent in the abstract;
`intent/` = the author's individual statements). The word is
transparent.

### S — Single wrapping type or shape-typed?

This report proposes **shape-typed** wrapping (`Decision` / `Principle`
/ `Correction` / `Clarification` / `Constraint`) per `nota-design.md`
Rule 1. Alternative: a single `Intent` wrapper with a `kind` enum field.

The shape-typed proposal makes the kind grep-able at the wrapping-type
level and matches the canonical NOTA design discipline. It is also
slightly stricter — adding a sixth kind requires adding a new type
rather than a new enum variant.

Recommendation: **shape-typed**. Five wrappers is small; the visual
distinction at-a-glance is worth more than the schema-extension
ergonomics.

### P — Where the discipline skill lives

A new skill `skills/intent-log.md` (or named after N) carries the
discipline: when to record, how to format, supersession protocol,
certainty vocabulary, retroactive seeding policy. The skill registers
in `skills.nota` at tier `mechanism` (procedural; consulted when
recording an entry).

Recommendation: confirm `skills/<N>-log.md` — e.g.,
`skills/intent-log.md` if N is `intent/`.

### R — Retroactive seeding

This session alone has produced multiple durable author intents that
qualify for recording:

- Components take only one NOTA argument; no flags ever
  (`component-shape/single-nota-argument.nota`)
- Policy state + working state in one sema-engine DB;
  `bootstrap-policy.nota` is a one-shot seed (`component-shape/`)
- Claim a directory = everything in it; sub-scope handoff forbidden
  (`component-shape/sub-scope-handoff-forbidden.nota`)
- `permission-signal-<component>` was a hallucination; only
  `signal-` and `owner-signal-` exist (`component-shape/`)
- AGENTS.md stays compact; bulky discipline → AGENTS-extended; no
  line caps quoted inside the file (`workspace/`)
- Skills grow noisy when agents over-elaborate; smart models fill
  blanks (`workspace/`)
- Reports retire when superseded; rename protocol with `-v2`/`-v3`
  for light edits, new number + delete predecessor for substantial
  rewrites (`reports/`)
- NOTA is positional, not labeled (`nota/`)
- Persona-orchestrate is a real component, not a fold-into-mind
  (`orchestrate/`)

Recommendation: **seed `<name>/` with these as the first batch** in
the same commit that lands `skills/<name>-log.md`. Each entry takes a
verbatim quote from the actual transcript (or a corresponding chat
turn) plus the agent's terse rephrasing.

### M — Persona-mind migration

When persona-mind's typed memory variants land, each NOTA record
becomes a memory of variant `AuthorialMemory` (or one variant per
kind: `AuthorialDecision`, `AuthorialPrinciple`, …). Topic becomes a
relation tag. The `<name>/<topic>/<file>.nota` path becomes the
seed for the memory's `uid`.

Recommendation: add a forward-pointing note in `skills/<name>-log.md`
naming this migration target. No work in `persona-mind` yet — the
note signposts where the substance lands eventually.

---

## 7 · What lands when these answers come back

Once you settle N / S / P / R / M, one commit lands:

1. **`skills/<name>-log.md`** — the new skill (when-to-record, the
   record shape, certainty vocabulary, supersession protocol,
   migration note).
2. **`skills/skills.nota`** — adds the new skill to the index
   (`(Meta intent-log skills/intent-log.md mechanism "Record what the author explicitly said …")`).
3. **`<name>/`** — directory created with the retroactive seed batch
   per R.
4. **`AGENTS-extended.md`** — adds a §"Author intent log" section
   (consult-when-the-topic-comes-up).

No `AGENTS.md` change — the discipline isn't every-keystroke, just
sometimes-when-recording.

---

## See also

- `skills/nota-design.md` — positional NOTA discipline; the design
  rules these records follow.
- `skills/nota-schema-docs.md` — pseudo-NOTA convention for
  documenting record schemas in markdown.
- `skills/skills.nota` — canonical positional-NOTA example.
- `skills/skill-editor.md` — how to land the new
  `skills/<name>-log.md`.
- `skills/reporting.md` §"Always name paths" — the chat discipline
  this report is meant to support (recording author intent makes
  "what the author has said" a query-able surface, complementing the
  per-report inlining of decisions).
- Forward: `persona-mind` typed memory variants — where this surface
  migrates.
