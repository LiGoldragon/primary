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

## Rule 1 — If there's no variant, it's a struct (no tag)

A PascalCase tag at the start of `(…)` is an enum variant. If
every record in this file would have the same tag, there's no
enum — it's just a struct, and structs have **no tag at all** in
the wire form. Drop it.

If the file is a skills index and every record were of type
`Skill`, you wouldn't write `(Skill operator …)` — there's no
enum, just a struct: `(operator …)`. But because skills.nota has
actual variants — `Role`, `Architecture`, `Craft`, `Programming`,
`Workflow`, `Meta` — the records ARE enum variants, and each
variant tag tells the reader which kind of skill this is.

If the file is a deployment plan with one kind of step, drop the
tag and write `(zeus apply 2026-05-19)`. If steps have variants
(`Build`, `Verify`, `Deploy`), the variant tags appear.

The CLI parallel: a `message` CLI never wraps every record in
`Message`. The message-ness is implied; the *kind of message* —
when it varies — is the variant tag.

The test: *can the same position carry more than one shape?* If
yes, you have an enum; the variant tag names which shape this
record is. If no, you have a struct; no tag.

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

**The mental model — three cases for PascalCase, one for the rest.**

When you read NOTA, every PascalCase token falls into one of
three cases:

1. `(VariantName fields…)` — **data-carrying enum variant**. The
   opening `(` followed immediately by a PascalCase token means
   you're at an enum variant that carries data; everything after
   the variant name is its fields, positional.
2. `(fields…)` without a leading PascalCase — **struct**. No tag.
   The schema position tells the reader what struct this is.
3. Bare `VariantName` with no preceding `(` — **non-data-carrying
   unit variant**. Like `None`, `Maximum`, `Apex`.

Everything else is a primitive (strings, numbers, bools, bytes) or
a sequence `[…]` which is `Vec<T>` (every element the same type).

**The corollary**: when you write a NOTA record, ask: *can this
position hold more than one shape?* If yes, you have an enum;
every record tags its variant (case 1) or is a unit (case 3). If
no, you have a struct; write the fields directly without any tag
(case 2).

This is the entirety of the PascalCase rule. Earlier versions of
this skill invented terminology ("head", "monomorphic position")
and the `nota/README.md` over-states the rule by conflating
structs with enum variants — both being corrected per bead
`primary-hj63`.

**Bare identifiers as strings.** Where the schema expects `String`,
a bare ident-class token serves as the value (`(Package nota-codec)`
is the same as `(Package "nota-codec")`). PascalCase, camelCase,
and kebab-case all qualify. The reserved literals `true`, `false`,
`None` always mean their typed meaning, not strings.

**Bare `Path`.** Where the schema expects `Path` (not `String`),
the bare alphabet widens to include `/` and `.` for filesystem-
shaped values. A bare `skills/operator.md` at a `Path` position
parses; the same token at a `String` position is a typed error.

**Optional values.** `Option<T>` is a normal data-carrying enum.
Absence writes bare `None` (case 3 of the PascalCase rule);
presence writes `(Some inner)` (case 1 — the standard variant
wrap). Tail omission is **not** a compatibility shape: every
position in the text carries every position in the schema,
always. `#[nota(default = …)]` is **forbidden** (per
`nota/README.md` §"No omittable fields"). A record short on
tokens is a typed error, not a silent zero-fill.

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
