# Skill — NOTA design

*Canonical patterns for designing NOTA records. Three rules. The
test for "is this NOTA designed well?" is grep-ability and density:
every meaningful distinction is in the data; no token is wasted on
information the context already gives.*

## What this skill is for

NOTA is positional, typed, terse. Designed badly, it becomes a JSON
with extra steps — verbose, redundant, with data hiding in comments
or restated as identical wrappers around every record. Designed
well, the same data takes a third of the tokens and the structure
itself carries category information that would otherwise be a side
channel.

Read this skill before designing a new NOTA file or schema. The
rules below are the difference between NOTA-the-substrate and NOTA-
the-format-you-wrote-once-then-regretted.

## Rule 1 — The wrapping type names the most useful distinction in context

NOTA records are typed. The TYPE you wrap with is what the reader
needs to know about the record that isn't already obvious from
context.

If the file is a skills index, every record is a skill. Wrapping
each one in `(Skill ...)` adds zero information — the file already
says so. The first useful distinction is the *kind* of skill:
`(Role ...)`, `(Architecture ...)`, `(Craft ...)`. That's the type.

If the file is a deployment plan, every record is a step. The type
isn't `(Step ...)` — it's `(Build ...)`, `(Verify ...)`, `(Deploy ...)`.

The CLI parallel: a `message` CLI never wraps every record in
`Message`. The message-ness is implied; the *kind of message* is
the data the CLI dispatches on.

The test: if every record in this file would have the same wrapping
type, that type is implied — drop it, and use the next level of
distinction as the type.

## Rule 2 — Data lives in records, not in comments

NOTA comments are for explaining the schema (what the fields mean,
what the enum variants are, the structural contract). NOTA comments
are NOT for organizing the data into categories or sections.

A `;; Roles` header that introduces three role records is a
category surfaced as a comment. NOTA can't see it. Future readers
can't grep it. The category IS data — make it the type.

Bad:

```nota
;; Roles
(Skill operator "skills/operator.md" role 1 "...")
(Skill designer "skills/designer.md" role 1 "...")

;; Architecture
(Skill component-triad "skills/component-triad.md" architecture 1 "...")
```

Two things are wrong: every record wears the redundant `Skill`
wrapper, and the categories are duplicated as comments AND as a
field. Fix both:

```nota
(Role operator skills/operator.md Apex "...")
(Role designer skills/designer.md Apex "...")

(Architecture component-triad skills/component-triad.md Apex "...")
```

Same data, fewer tokens, grep-able category. Note also: instance
names (`operator`, `designer`, `component-triad`) are lowercase /
kebab-case because they're runtime instances; the tier value
(`Apex`) is PascalCase because it's a compile-time enum variant
(see Rule 3 below and `ESSENCE.md`'s language-design rule).

What comments DO carry: the schema preamble at the top of the file
(positional field meaning, enum variants, optional-marker convention).
That teaches the reader how to parse the data. The data itself stays
in records.

## Rule 3 — Enums get PascalCase names, not numbers

Ad-hoc integer codes for enum variants are a smell. `tier 1` /
`tier 2` / `tier 3` means nothing without a key. `tier Apex` /
`tier Keystroke` / `tier Topic` is self-documenting and grep-able
from any cold read.

Bad: `(Skill component-triad ... 1 ...)`.
Good: `(Architecture component-triad ... Apex ...)`.

Variants are **PascalCase** because they're compile-time
structural (per `ESSENCE.md`'s language-design rule:
*"PascalCase = compile-time structural; camelCase = instance"*).
The parser dispatches on first-character case; a lowercase
`apex` would parse as an instance identifier, not a variant.
Instance names (the second field above — `operator`,
`component-triad`) stay lowercase / kebab-case for the same
reason.

Numbers are fine for actual numbers — counts, identifiers, slots,
ordinals where the ordering matters. They are not fine as
stand-ins for named categorical distinctions.

The schema preamble names the enum's allowed values. Grep for
`Apex` finds every apex-tier record across the file (and across
every NOTA file in the workspace that uses the same vocabulary).

## The canonical example

`/home/li/primary/skills/skills.nota` is the workspace's canonical
example of NOTA designed well. Open it. Notice:

- No `(Skill ...)` wrapper — that's implied by the file.
- The type is the category: `(Role ...)`, `(Architecture ...)`,
  `(Craft ...)`, `(Programming ...)`, `(Workflow ...)`, `(Meta ...)`.
- Tier values are PascalCase variants: `Apex`, `Keystroke`,
  `Topic`, `Mechanism`.
- Comments only explain the schema — what the fields mean, what the
  enums allow, what's not in the index and why.

If you're designing a new NOTA file, read it first.

## Grammar facts that catch the recurring mistakes

These are not design rules — they're the language's actual grammar.
Agents (this one, repeatedly) keep proposing shapes that violate
them. The source of truth is `nota/README.md`; restated here so
the discipline skill carries the load.

**Records and sequences.** Two delimiter pairs:

- `(…)` — a **record**. A Rust struct or enum variant. Fields are
  positional. When the type isn't determined by schema position
  (enum variants, top-level records in a file with multiple
  types), the type name appears as the first token: `(Decision
  …)`. When the type IS determined by schema position (e.g.
  every element of a `Vec<Statement>` is a `Statement`), the type
  name is omitted and the fields come directly: `(2026-05-19
  18:30 "quote")`.
- `[…]` — a **sequence**. A `Vec<T>`. Every element is the same
  type `T`.

**Lists are homogeneous; heterogeneous positional structure is a
record (struct).** A `(date, time, quote)` triple is a struct;
write it `(2026-05-19 18:30 "first quote")` at a position the
schema declares as that struct.

A struct does NOT need to be wrapped in an enum variant. A struct
is just a struct with positional fields. The "wrapping type names
the most useful distinction" rule (Rule 1) is about enum variants
where one of several types could appear; a struct that is the
only type at a position writes positionally without naming the
type.

> *(Note 2026-05-19: the prior version of this section invented
> 'head' and 'monomorphic position' terminology. NOTA's actual
> concepts are struct, enum variant, positional fields, schema
> position. The over-strict 'every record names its type' claim
> in `nota/README.md` is being corrected per bead `primary-hj63`.)*

**Bare identifiers as strings.** Where the schema expects `String`,
a bare ident-class token serves as the value (`(Package nota-codec)`
is the same as `(Package "nota-codec")`). PascalCase, camelCase,
and kebab-case all qualify. The reserved literals `true`, `false`,
`None` always mean their typed meaning, not strings.

**Bare `Path`.** Where the schema expects `Path` (not `String`),
the bare alphabet widens to include `/` and `.` for filesystem-
shaped values. A bare `skills/operator.md` at a `Path` position
parses; the same token at a `String` position is a typed error.

**Optional values.** `Option<T>` writes the literal `None` for
absence; presence writes the inner value with no `Some` wrapper.
Tail-omission is decode-only compatibility, not canonical output.
`#[nota(default = …)]` is **forbidden** (per `nota/README.md`
§"No omittable fields") — every position in the text carries every
position in the schema, always.

**Multi-field unnamed structs are forbidden.** `struct Pair(i32, i32)`
has no field-name mapping; NOTA rejects at serialize time. The
single-field tuple struct (newtype) is the only allowed unnamed
shape. For heterogeneous positional data, use a **named-field**
struct, which emits as a typed record.

**Sigils.** Two reserved at the syntax layer: `;;` for line
comments, `#` for byte literals. Other sigils (`~ @ ! ? *`) are
nexus extensions and reserved (syntax error in pure NOTA). `=` is
reserved.

## Before you sketch any NOTA record

Before producing any new NOTA shape — in a report, in chat, in a
proposal, anywhere — do these four things:

1. **Open `skills/skills.nota` and read three records of any category.**
   That's your template for what NOTA looks like in this workspace.
   Also read `nota/README.md` if you haven't recently — the grammar
   facts above are easy to misremember.
2. **Identify the wrapping type that names the most useful distinction
   in context** (Rule 1 above). The wrapper is never a generic name
   like `Item`, `Entry`, or `Record` when the file already says so.
   **The variant test**: if you can't name another type that could
   go in this position, the wrapper is superfluous — drop it.
3. **If the structure is heterogeneous positional, it's a record
   (struct) — not a sequence.** Lists are homogeneous; mixed-type
   positional structure is a struct with positional fields. The
   struct's type name appears only when not determined by schema
   position (enum variants, top-level records); at a known
   schema position, the fields come directly without naming the
   type.
4. **Sketch fields positionally — no `(key value)` pairs inside the
   record. No nested wrappers when every record has the same
   inner shape.** Positional means
   `(Decision "summary" "quote" "context" Maximum 2026-05-19 01:23)`,
   not `(Decision (summary "…") (verbatim …) (certainty Maximum))`
   and not `(Decision "summary" (Verbatim "quote" "context") Maximum …)`
   if `Verbatim` is the only thing that ever appears in that slot.
   Variants are **PascalCase** (`Maximum`, not `maximum`); date and
   time are two bare positional fields (`2026-05-19 01:23`), not one
   quoted string.

Most agent NOTA mistakes are the same mistake — labeled fields. The
fix is the same too: read the canonical example before you sketch,
and let the wrapping type carry the schema.

## When you find yourself fighting the rules

You'll notice yourself wanting to:

- Wrap every record in `(Item ...)` "for safety." Don't. The file is
  the safety.
- Group records under section comments. Don't. Surface the category
  as the type.
- Use integer codes "because they're shorter." They're not shorter
  once you account for the lookup-table that decodes them. Names
  win.

If the same structural decision recurs across many NOTA files (a
shared enum vocabulary, a shared identity newtype, a shared
date-shape), that's a sign of a real workspace primitive. Document
it once in the relevant repo's `skills.md` or `ARCHITECTURE.md` and
reference by name; don't restate it in every NOTA file's preamble.

## See also

- `skills/nota-schema-docs.md` — pseudo-NOTA convention for
  documenting record schemas in markdown (angle-bracket placeholders,
  optional `?`, enum `|`). Complementary: this skill is about real
  NOTA; that one is about teaching-shape NOTA in docs.
- `nota`'s `example.nota` — the language's reference example.
- `nota`'s `ARCHITECTURE.md` — positional, two delimiters, two
  string forms, two sigils.
- `skills/skills.nota` — the canonical workspace example.
- `ESSENCE.md` §"Naming — full English words" — the naming
  discipline NOTA enums inherit.
