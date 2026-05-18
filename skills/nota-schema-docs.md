# Skill — NOTA schema docs

*A tiny convention for documenting NOTA record schemas so agents
don't have to read Rust to know what a record looks like.*

---

## The convention

To document a NOTA record's shape, write a pseudo-NOTA form where
**placeholders go in angle brackets** and **optional fields end in
`?`**:

```nota
;; Bug: a concrete defect with an incident timestamp and a fix path.
(Bug <title> <description> <severity> <incident-at?> <reproduction?>)
;;   title         : ShortText
;;   description   : TextBody
;;   severity      : Catastrophic | High | Normal | Low
;;   incident-at?  : Timestamp
;;   reproduction? : TextBody
```

The first line: typed-record name + positional placeholders.
The lines below: name → type (one per placeholder).

Rules:

- **Placeholders use `<kebab-case>`.** Spelling-it-out applies (per
  `ESSENCE.md` §"Naming"): `<incident-at>`, not `<inc>`.
- **Optional fields end in `?`** in the form-line **and** in the
  per-line type list.
- **Closed enums use `|`** to separate variants: `Catastrophic | High`.
- **Lists wrap their inner type in square brackets**: `[<label>]`.
- **Nested records use the same form**: `(Identity <name> <ssh-fingerprint?>)`.
- A `;;` line is a NOTA comment; use comments to name each field's
  type and the rule's *why* when it isn't obvious.

That's the whole convention.

---

## Why pseudo-NOTA, not the real syntax

Real NOTA is positional and the field names live in the Rust schema.
A reader of `(Bug "Whisrs hangs" "...")` can't tell what the second
string is for without reading the Rust. The pseudo-NOTA form
**surfaces the field names inline** so the reader doesn't need to
chase the schema crate.

For real records on the wire, names disappear (NOTA is positional).
For *documenting* schemas in skill files, ARCH files, and design
reports, the pseudo-form is what an agent reads.

---

## When to use it

- Documenting record schemas in `signal-*` contract ARCH files.
- Describing message variants in design reports.
- Sketching new record shapes before implementation lands.
- Reference tables in skill files when the schema is load-bearing.

For canonical typed records on the wire — use the real Rust schema +
`tests/round_trip.rs` + `tests/canonical_examples.rs`. The
pseudo-NOTA in docs is teaching material, not the authoritative
shape.

---

## Example — a memory variant set

```nota
;; Persona-mind memory variants. Closed enum.
;; Common fields apply to every variant; kind-specific extensions follow.

(Memory <common> <kind>)
;;   common : (Common <id> <title> <body> <created-at> <created-by> <status> <priority> <labels>)
;;   kind   : Task | Bug | Feature | Epic | Decision | Migration | Discipline | Investigation

(Task <acceptance-criteria> <spec-id?> <progress-notes>)
;;   acceptance-criteria : TextBody
;;   spec-id?            : ReportPath
;;   progress-notes      : [(Note <timestamp> <author> <body>)]

(Bug <severity> <incident-at?> <reproduction?> <discovery-path?>)

(Feature <branch> <repos>)
;;   branch : BranchName
;;   repos  : [RepoName]

(Epic <children> <required-skills?>)
;;   children        : [TypedThoughtId]
;;   required-skills : [SkillName]
```

That's enough to let an agent draft a payload without reading the
Rust schema. When implementation lands, the test in
`tests/canonical_examples.rs` is the authoritative truth — the
pseudo-NOTA in this skill is just orientation.

---

## See also

- `skills/nota-design.md` — canonical NOTA design discipline for the records you actually write. (This skill is about *documenting* schemas in markdown; that skill is about *designing* records in NOTA.)
- `repos/lore/data/nota-syntax.md` — the canonical NOTA syntax reference.
- `nota`'s `example.nota` and `nota`'s `ARCHITECTURE.md` — positional records, two delimiters, two string forms, two sigils.
- `skills/skills.nota` — the canonical workspace example of NOTA designed well.
- `skills/contract-repo.md` — how typed records land in contract crates.
- `skills/skill-editor.md` — keep this skill compact; cut anything that doesn't teach the rule.
