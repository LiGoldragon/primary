# 231 — How agents misunderstand NOTA, and what to do about it

*Diagnosis of the recurring "labeled-fields" mistake agents make when
sketching NOTA records, and the interventions that fix it at the moment
of need. Three interventions land in this report's commit; a fourth is
a follow-up for the operator.*

---

## 0 · TL;DR

Agents reach for `(field-name value)` pairs inside NOTA records by
default. The skill that names the right shape
(`skills/nota-design.md`) exists and is clear — but at tier `topic`,
it's read when an agent decides they're doing NOTA design, not when
they're casually sketching a record in chat. The mistake happens at
the moment of casual proposal.

Three interventions, all landed in this commit, raise the visibility
at the point of failure:

1. **`AGENTS.md` hard override** explicitly names the rule
   ("NOTA records are positional, not labeled") alongside the existing
   no-flags-only-NOTA rule.
2. **`skills/skills.nota` top comment** carries a three-line reminder
   right above the data, so any agent reading the index sees the
   rule.
3. **`skills/nota-design.md` "Before you sketch any NOTA record"
   checklist** turns the right approach into a 3-step pre-flight.

A fourth intervention is operator follow-up:

4. **`nota-codec` rejects labeled-field records at parse time** with
   a typed error that names the mistake, so any NOTA file that
   reaches the codec round-trip fails fast with a helpful message
   instead of silently accepting a non-NOTA shape.

---

## 1 · Why agents make this mistake

Three pressures push agents toward labeled fields:

- **S-expression priors**: Lisp/Clojure config sublanguages use
  `(symbol1 :key1 val1 :key2 val2)` or `(symbol1 (key1 val1) (key2 val2))`
  patterns. Models trained on those corpora reach for that shape
  whenever they see parentheses.
- **Self-documentation illusion**: labeled fields look "more readable"
  in isolation. `(verbatim (quote "x") (context "y"))` *seems* to
  document itself; `(Verbatim "x" "y")` requires the reader to know
  the positional contract. The illusion masks the cost of repeating
  the field names in every record.
- **The right rule is one skill away**: `skills/nota-design.md` is
  tier `topic` — read when the agent decides they're doing NOTA
  design. Casual sketching in chat doesn't trip that decision.

The failure mode is consistent across agents and sessions: the agent
isn't *wrong about NOTA*, they're *not consulting the rule when they
should*.

---

## 2 · Where the mistake happens

Three concrete failure surfaces:

| Surface | Failure pattern |
|---|---|
| Chat proposal | Agent invents a NOTA shape in prose; no codec roundtrip catches it; user spots it (the case that surfaced this investigation). |
| Report example | Same as chat — examples inside a report's prose aren't parsed. |
| New NOTA file | A new `<file>.nota` is added without first reading an existing one. If the codec accepts the shape, the file looks like NOTA but isn't. |

The first two are caught only by review; the third is caught only if
the codec rejects the labeled-field shape.

---

## 3 · Interventions landing in this commit

### 3.1 · AGENTS.md hard override

The Hard Overrides section gains a second NOTA rule (alongside the
"only argument is NOTA" rule):

> **NOTA records are positional, not labeled.** Type first, then
> fields in declared order — no keywords inside records. The
> `(key value)` shape from Lisp/Clojure/JSON is not NOTA. Before
> sketching any new record, open `skills/skills.nota` (the canonical
> example) or read `skills/nota-design.md`.

Cost: 5 lines. Benefit: every agent reading AGENTS.md on session
start sees the rule before they ever sketch a record.

### 3.2 · `skills/skills.nota` top comment

Right above the data:

```nota
;; NOTA records are positional. Type, then fields, no keywords.
;; The `(key value)` shape from Lisp/Clojure/JSON is not NOTA.
;; If you're sketching a new NOTA record, read skills/nota-design.md first.
```

Cost: 3 lines. Benefit: any agent querying `skills.nota` (required
reading per AGENTS.md item #3) sees the rule paired with the data
they're modeling new records on.

### 3.3 · `skills/nota-design.md` "Before you sketch any NOTA record"

A new section before the existing "When you find yourself fighting
the rules" section, naming a 3-step pre-flight:

1. Open `skills/skills.nota` and read three records of any category.
2. Identify the wrapping type that names the most useful distinction
   in context.
3. Sketch fields positionally — no `(key value)` pairs inside the
   record.

Plus the meta-line: *"Most agent NOTA mistakes are the same mistake —
labeled fields. The fix is the same too: read the canonical example
before you sketch."*

Cost: ~20 lines of new skill content. Benefit: when an agent does
consult the skill, they get an actionable checklist, not just rules.

---

## 4 · Intervention 4 — operator follow-up

`nota-codec` should reject labeled-field records at parse time with a
helpful error. Concretely:

- When the decoder encounters `(TypeName (Identifier1 value1) (Identifier2 value2) …)`
  and `TypeName`'s registered schema has positional fields (i.e., the
  type isn't declared as a record-of-records), return a typed error:
  `Error::LabeledFieldShape { expected_positional: usize, found_labeled: usize, type_name: String }`.
- The error display string carries: *"NOTA records are positional;
  found labeled-field shape `(TypeName (key value)…)`. The contract
  declares `TypeName` with N positional fields. Did you mean
  `(TypeName <field1> <field2> …)`? See `skills/nota-design.md`."*
- A witness test in `nota-codec/tests/` covers the rejection path.

This is the only intervention that catches the mistake *after* the
agent has written the file — the other three intervene before the
sketch. Both kinds matter.

**Recommended**: file as a bead, owner `operator`, scope
`nota-codec/`. Priority P2.

---

## 5 · Why raising `nota-design.md`'s tier was rejected

A tempting fifth intervention: raise `skills/nota-design.md` from
tier `topic` to tier `keystroke` so it's part of every-session
reading. Rejected because:

- Most sessions don't touch NOTA design. Reading the skill every
  session for the 5% of sessions that need it is a high cost for low
  benefit.
- The AGENTS.md hard override (3.1) plus the skills.nota top comment
  (3.2) catch the rule at the moments that matter — without forcing
  the full skill on every session.

The right tier is `topic` with high-visibility entry points, not
`keystroke`.

---

## 6 · What lands in this commit

1. `AGENTS.md` — Hard Overrides section gains the NOTA-positional
   rule (intervention 3.1).
2. `skills/skills.nota` — top comment expanded with NOTA-positional
   reminder + the existing tier enum legend (intervention 3.2).
3. `skills/nota-design.md` — "Before you sketch any NOTA record"
   checklist (intervention 3.3).

Plus this report — the analysis behind those edits, retained for
future readers who want the *why* of the visibility-raise.

The operator follow-up (intervention 4) needs a bead. Filing
recommended after this report lands.

---

## See also

- `skills/nota-design.md` — the canonical NOTA design discipline.
- `skills/nota-schema-docs.md` — pseudo-NOTA in markdown.
- `skills/skills.nota` — the canonical NOTA example agents should
  read first when sketching new records.
- `nota`'s `ARCHITECTURE.md` — the language's authoritative spec
  (positional, two delimiters, two string forms, two sigils).
- Forward: bead for `nota-codec` labeled-field rejection (intervention 4).
