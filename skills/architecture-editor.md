# Skill — architecture editor

*How `ARCHITECTURE.md` files are named, located, scoped, and
maintained.*

## What an `ARCHITECTURE.md` is

An `ARCHITECTURE.md` describes **what the system IS** at a
specific scope. It is not a tour, not a tutorial, not a history.
It is the canonical reference for shape: components, ownership
boundaries, invariants, the typed contracts between parts.

Two scales:

- **Per-repo `ARCHITECTURE.md`** — describes that repo's niche.
  What this repo owns, what it doesn't, the major types and
  their relationships, the contracts on its boundaries.
- **Meta `ARCHITECTURE.md`** — for an ecosystem of related
  repos, lives in the ecosystem's coordination repo and
  describes how the niches fit together.

The pattern follows criome's worked example
(`~/primary/repos/criome/ARCHITECTURE.md`): the meta architecture
in the apex repo (`criome/ARCHITECTURE.md` for the sema
ecosystem); each component repo carries its own
`ARCHITECTURE.md` for its niche.

For Persona, `persona` is the meta repo; its `ARCHITECTURE.md`
is the apex. Active component and contract repos are listed in
`~/primary/protocols/active-repositories.md`.

**Scope discipline.** When an ARCH doc describes a system whose
*eventual* form is larger than what's built today, name the scope
explicitly in a marker near the top (see `criome/ARCHITECTURE.md`
and `sema/ARCHITECTURE.md` for landed examples). ARCH bodies
describe what is true today in present tense; the eventual shape is
labelled, not implied. Per `~/primary/ESSENCE.md` §"Today and
eventually — different things, different names".

## Where each kind of statement lives

| Doc | What goes there | Permanent? |
|---|---|---|
| `ARCHITECTURE.md` (meta) | How the components fit together. The runtime topology. The wire vocabulary. The flow of state across processes. The named clusters and their boundaries. | Yes |
| `ARCHITECTURE.md` (per-repo) | This repo's role, what it owns, what it doesn't, code map, invariants, contracts at its edges. | Yes |
| `skills.md` (per-repo) | How an agent works *in* this repo. The "if you're editing here, here's what's load-bearing." | Yes |
| `AGENTS.md` (per-repo) | Thin shim that names the repo's role + carve-outs from the workspace contract. | Yes |
| Reports | Decision records, design rationales, audits, syntheses. Working surfaces for the path that led to the architecture. | **No — ephemeral, retires** |

If a statement is "what the system IS," it goes in
`ARCHITECTURE.md`. If it's "what an agent should do," it goes in
`skills.md`. If it's "why we chose this," it goes in a report —
and when the rationale is load-bearing for understanding the shape,
**the architecture inlines the load-bearing claim** rather than
citing the report.

## Format

Markdown. No required schema beyond the conventions below.

The structure that has worked:

```markdown
# <repo> — architecture

*<one-line essence>*

> Status note. Read-this-first banner if the file is meta-scope.

---

## 0 · TL;DR

<2–4 paragraphs: the system in its sharpest form>

## 1 · Components and clusters

<typed map of the components; visual diagram>

## 2 · Wire vocabulary

<the contract types; how processes speak; cross-reference contract repos>

## 3 · State and ownership

<who owns what; where each piece of data lives; transaction boundaries>

## 4 · Boundaries

<what this scope owns vs doesn't; cross-references to neighboring repos>

## 5 · Constraints

<line-by-line obligations this component must satisfy; simple enough to become
test names>

## 6 · Invariants

<system-wide truths this scope preserves; usually fewer and broader than
constraints>

## 7 · Possible features (optional, only when there is real uncertainty)

<items under consideration but not decided. Each names the open question;
moves to the cemented body above when settled, retires when ruled out.
Other acceptable headings: "Open questions", "Undecided boundaries",
"Future considerations". See the "Carrying uncertainty" section of this
skill for shape and discipline.>

## Code map

<for per-repo: directory tree with one-line annotations>

## See also

<other ARCHITECTURE.md files this one connects to>
```

The first heading is `# <repo> — architecture` — recognisable
across the workspace. The TL;DR is the file's most-load-bearing
section: a reader who reads only the first 30 lines should come
away with the right mental model.

Diagrams are first-class. Mermaid `flowchart`, `sequenceDiagram`,
`stateDiagram-v2` — all welcome. Per `~/primary/skills/reporting.md`
§"Mermaid label quoting", quote labels containing parentheses or
slashes.

### Constraints are the test seed

Every component architecture should have a **Constraints** section.
Constraints are short, direct sentences naming what the component must do.
They are intentionally simpler and more numerous than invariants.

Good constraints read like test names in prose:

- The `mind` CLI accepts exactly one NOTA record.
- The `mind` CLI sends a Signal frame to the daemon.
- The daemon owns `mind.redb`.
- Queries never send write intents.
- The router commits a message before delivery.
- A contract crate contains no runtime actors.

Each load-bearing constraint needs an architectural-truth test named after it.
The test can be strange: static source scans, dependency-graph checks, actor
trace witnesses, redb fixture chains, process-boundary probes, or compile-fail
guards are all valid if they prove the constraint. The constraint says what
must be true; the test names the observable witness that makes lying hard.

Use this split:

| Section | Shape |
|---|---|
| Constraints | Many concrete obligations; often one test per line. |
| Invariants | Few broad truths this scope preserves across all constraints. |
| Tests | Constraint-name witnesses that prove the architecture path was used. |

If a constraint cannot be tested, rewrite it until it names an observable
witness or move it to a report as unfinished thinking.

## What an `ARCHITECTURE.md` does NOT contain

- **Implementation code.** Per `~/primary/ESSENCE.md`
  §"Skeleton-as-design", the type system enforces shape; prose
  decays. A few-line snippet of a type's surface is fine; an
  implementation block is not.
- **Decision history.** "We considered X but went with Y" lives
  in a report. The current `ARCHITECTURE.md` describes Y as
  *what is*; if rationale is load-bearing for understanding,
  **inline the rationale** rather than citing a report.
- **References to reports.** See §"Architecture files never
  reference reports" below — this is a load-bearing rule.
- **Implementation scheduling.** *When* something will ship
  (next week, next milestone) belongs in beads or coordination
  notes, not architecture. The architecture is what the system
  *is* — or, in dedicated uncertainty sections per §"Carrying
  uncertainty" below, what it *might be*. Not a delivery roadmap.
  For "today vs eventually" scope, use the status-note + scope-
  discipline pattern (per `~/primary/ESSENCE.md` §"Today and
  eventually").
- **Tour-style narration.** "First, you'll find the foo
  module..." Architecture is reference, not a guided tour.
- **Restatement of workspace skills.** The architecture cites
  workspace skills; it doesn't repeat them.

## Architecture files never reference reports

**`ARCHITECTURE.md` files do not cite reports.** Reports under
`reports/<role>/` are ephemeral — working surfaces for design
rationale, decision paths, audits, and syntheses that retire as
their substance migrates elsewhere (per
`~/primary/skills/reporting.md` §"Kinds of reports — and where
their substance ultimately lives"). An `ARCHITECTURE.md` describes
*what is*; it must stand without time-stamped citations into a
working surface that may be deleted, superseded, or renumbered.

When an architecture needs content that currently lives in a
report:

- **Inline the load-bearing claim.** The constraint, the typed
  shape, the invariant, the table — copy it into the architecture
  body. The architecture becomes self-contained.
- **Reference another permanent doc** — a sibling
  `ARCHITECTURE.md`, a `skills.md`, an `ESSENCE.md` section, or
  code (with a file path, not a deep URL).
- **Drop the reference** if nothing in the report is load-bearing
  for the architecture.

If the design the report carries isn't yet settled enough to inline
as architecture, the report stays the canonical state — the
architecture is updated only when the design is ready to be stated
in present-tense "this IS" prose.

**Why:** reports retire; their numbers shift; their contents change
as the design evolves. An `ARCHITECTURE.md` that says "see report
161 for the verb spine" rots the moment 161 is deleted or
superseded. Architecture must stand without ephemeral citations.

This rule has no exception. The corresponding section in
`reporting.md` lists permanent homes for each report shape;
the architecture is one of those homes.

## Carrying uncertainty — possible features and undecided designs

Architecture files are not only for cemented decisions.
`ARCHITECTURE.md`, per-repo `INTENT.md`, and workspace skills CAN
carry possible features, undecided designs, and open questions —
provided the uncertainty is named explicitly, not smuggled into
present-tense "this IS" prose.

The reports lane is for in-flight investigation, not for stacking
tentative architectural ideas indefinitely. When an idea is
interesting but not yet decided, it goes in a dedicated uncertainty
section of the relevant permanent file — not a report that sits
without movement. Reports retire as their substance migrates;
architecture's uncertainty sections persist until the question
settles, then the substance moves to the cemented body. Per psyche
2026-05-22 (*"Architecture files and repositories can have like
uncertain, possible features, possible architecture design decisions
and stuff like that. We don't have to put everything as like raw
decided, only rock solid stuff."*).

### The shape

A dedicated section, clearly labelled, that carries tentative
substance:

```markdown
## Possible features (not decided)

*Items here are under consideration, not committed. Each names the
open question; moves to the cemented body when settled; retires
when ruled out.*

- **Feature X**: open question — how do we handle Y? Considered:
  A, B. Status: undecided, blocked on decision Z.
- **Feature W**: possible direction; rough sketch in
  reports/designer/<N>; will move into Components section if
  adopted.
```

Acceptable section names: `## Possible features`, `## Open
questions`, `## Undecided boundaries`, `## Future considerations`,
`## Under discussion`. Pick one or two per file; consistency over
creativity.

### Disciplines for uncertainty sections

- **Name the certainty explicitly.** A status sentence at the top
  of the section ("Items here are under consideration, not
  committed") or a prefix on each item ("Considered:",
  "Possible:", "Undecided:") prevents a reader from mistaking
  tentative for decided.
- **Name the question, not just the option.** "Possible feature:
  X" is weaker than "Open question: how do we handle Y?
  Considered: X, Z." The question is the real anchor; the options
  cluster under it.
- **Keep entries brief.** One paragraph per item — enough to
  anchor the question, not enough to be a report. When substance
  grows past that, write the report; the uncertainty entry
  collapses to a one-line pointer at the section.
- **Move out when decided.** When a question settles, the substance
  moves into the cemented body of the architecture (or the entry
  retires if the option was ruled out). Don't leave settled
  content sitting in an "undecided" section.
- **Reference, don't restate.** When the substance is in a report
  that's still alive, the entry can be a one-line pointer at it
  ("see reports/designer/<N>"). Same no-report-citation rule
  applies to *cemented* claims — uncertainty entries can name
  reports because they're explicitly tentative, but the moment
  they're decided, the citation gets inlined and the report
  retires.

### Cemented vs uncertain — keep them visually separate

Cemented sections (Components / Wire vocabulary / State / Boundaries
/ Constraints / Invariants) describe what IS. Uncertainty sections
sit AFTER the cemented body, not interleaved, so a reader who stops
at the constraints has read only cemented architecture. The §7
"Possible features" placement in the template (see §"Format" above)
reflects this — uncertainty after invariants, before code map.

This keeps the file's main spine purely descriptive while letting
tentative substance live in the right permanent home, off the
reports lane.

### Where uncertainty lives by file

| File | Cemented content | Uncertainty headings |
|---|---|---|
| `ARCHITECTURE.md` (meta) | Components, wire vocabulary, cross-component invariants | `## Possible future components` / `## Open questions` |
| `ARCHITECTURE.md` (per-repo) | This repo's components, contracts, invariants | `## Possible features` / `## Undecided boundaries` |
| `<repo>/INTENT.md` | Psyche-stated goals/constraints/principles | `## Possible directions` / `## Open questions` (psyche-derived only) |
| `skills/<name>.md` | Decided discipline | `## Open questions` / `## Under discussion` |

For `<repo>/INTENT.md`, the discipline is stricter: every uncertainty
entry is still 100% backed by a psyche statement (per
`~/primary/skills/repo-intent.md`) — the agent doesn't invent open
questions, just records ones the psyche named without yet deciding.

## Continuous manifestation discipline

Per spirit record 944 (Maximum, 2026-05-27) + record 943 (High,
operator-facing companion): **architectural intent must be
manifested into the repo's `ARCHITECTURE.md` AT ALL TIME, not
just at the workspace level**. Companion to the discipline in
`skills/repo-intent.md` §"Continuous manifestation discipline"
for repo-scope intent.

### The work-cycle obligation

When an architectural decision lands in Spirit affecting repo
R's structural shape — a typed contract change, a new
component, a moved boundary, an invariant — reflect it into
R's `ARCHITECTURE.md` **as part of the work cycle, not as a
deferred pass**.

The trigger is wider than "did the psyche specifically address
R?" — any Spirit record whose architectural shape **applies to
R** (because R is in the affected stack, or because the rule
binds R's component category) is in scope. Records 922 (no
`\n` escape inline NOTA), 882 / 712 (methods on non-ZST), 894
(brace = key/value map), 902 (single-colon namespace), 909
(src/schema emission target), 932-940 (schema macro engine
semantics), 935 (Communicate trait + signal-frame mechanism)
are recent examples — each binds multiple repos and each one
that binds R needs to surface in R's `ARCHITECTURE.md`.

### Manifestation flow

1. When you capture an architectural intent through Spirit
   (`skills/spirit-cli.md`), also identify the repos whose
   architectural shape it affects.
2. For each affected repo, edit its `ARCHITECTURE.md` on a
   designer feature branch in
   `~/wt/github.com/<owner>/<repo>/<branch>/`.
3. Land both the Spirit capture and the ARCHITECTURE.md edits
   in the same work cycle — don't sequence them as a "now /
   later" pair.

### Failure mode this prevents

If architectural intent stays in Spirit + reports but doesn't
reach `ARCHITECTURE.md`, an agent reading the repo's
architecture file sees the prior structural shape and codes to
it. The architecture file is the load-bearing **what the
system IS** surface — if it lags behind the typed contract
decisions, the rest of the work loses its anchor.

### Cross-link

For the prose-intent companion (psyche goals / constraints /
principles / anti-patterns in `INTENT.md`), see
`skills/repo-intent.md` §"Continuous manifestation discipline".

## When to edit

Edit `ARCHITECTURE.md` when:

1. **The shape has changed.** A new component, a renamed
   contract, a moved boundary, a different transaction owner.
   Edit immediately. The architecture is a *current-shape*
   document; lag costs comprehension.
2. **A reader will be confused** by the current state. If a
   statement is technically right but easy to misread, rewrite.
3. **A new constraint has emerged** and is now load-bearing.
   Add it to §"Constraints" and name the witness test it implies.
4. **A new invariant has emerged** and is now load-bearing.
   Add it to §"Invariants".
5. **A cross-reference to a neighbor has stale or wrong info.**
   Update the cross-reference; if the neighbor's architecture
   has drifted, surface it (or open a bead for that repo's
   owner).

Don't edit for:

- Historical interest. The path is in commit history.
- Speculative ideas with no real open question behind them.
  Genuinely undecided designs and possible features earn a
  place in a dedicated uncertainty section (per §"Carrying
  uncertainty" above); pure speculation belongs in
  conversation or a draft report, not the architecture.
- Fixing a typo in a comment block. Skip the ARCHITECTURE
  ceremony; just edit.

## Editing rules

- **Edit in place; don't fork or version.** The current shape
  is the authoritative shape. Old versions live in commit
  history.
- **Present tense.** Describe what IS, not what was or what
  will be.
- **Positive framing.** Per `~/primary/ESSENCE.md` §"Positive
  framing": when an option is excluded, state the criterion
  positively ("must be Rust"), not the negative ("Go is
  excluded"). When a direction was wrong, the doc shows the
  new direction; the wrong one disappears from the doc.
- **Cross-reference, don't duplicate.** Workspace skills,
  ESSENCE principles, neighboring `ARCHITECTURE.md` files —
  point at them, don't restate.
- **Commit immediately after a meaningful edit.** Per
  `~/primary/skills/autonomous-agent.md` §"Version-control
  obstacles".

## When to create one

If a repo doesn't have an `ARCHITECTURE.md` and you've done
substantive work in it (per the same trigger as
`autonomous-agent.md` §"A repo has no `skills.md`..."), create
one.

The check: can a fresh agent read your `ARCHITECTURE.md` and
form the right mental model of the repo's shape? If yes, the
file earns its place. If no — vague, missing key types, no
ownership map — keep iterating until yes.

A thin-but-honest `ARCHITECTURE.md` is better than no file.
**Don't write `ARCHITECTURE.md` for a repo you haven't worked
in deeply** — the same warning that applies to `skills.md`
applies here: a confidently-wrong architecture is worse than
no architecture, because future agents will trust it.

## Meta vs per-repo split

When an ecosystem grows past one repo:

```mermaid
flowchart TB
    meta["meta repo<br/>persona / criome / sema"]
    a["component A"]
    b["component B"]
    c["component C"]

    meta -. ARCHITECTURE.md describes whole .-> all["ecosystem topology"]
    a -. ARCHITECTURE.md describes A's niche .-> sa["A's role + boundaries"]
    b -. ARCHITECTURE.md describes B's niche .-> sb["B's role + boundaries"]
    c -. ARCHITECTURE.md describes C's niche .-> sc["C's role + boundaries"]

    meta -- "imports" --> a
    meta -- "imports" --> b
    meta -- "imports" --> c
```

The meta `ARCHITECTURE.md` describes:

- The runtime topology (which processes exist; what speaks to
  what).
- The wire vocabulary (the contract repo and what it carries).
- Cross-component invariants (transaction boundaries, store
  ownership, schema-version discipline).
- The named clusters and how they map to repos.

The per-repo `ARCHITECTURE.md` describes:

- This repo's role inside the ecosystem.
- The major types this repo owns.
- The contracts at this repo's boundaries (what it imports
  from the contract crate; what it exposes to consumers).
- The repo's code map.
- Invariants specific to this repo.

The split avoids the ecosystem-architecture growing into a
single huge file and avoids per-repo files repeating
ecosystem-wide context. Each scope has the appropriate amount
of detail.

## See also

- `~/primary/skills/skill-editor.md` — the parallel skill for
  `skills.md` files; same conventions for cross-references,
  scope, and the no-report-references rule.
- `~/primary/skills/reporting.md` — when to write a report
  versus update an architecture; permanent homes for each
  report shape.
- `~/primary/ESSENCE.md` §"Documentation layers" — where each
  layer lives.
- `~/primary/ESSENCE.md` §"Rules find their level" — finding
  the right home for a rule before writing it.
- `~/primary/ESSENCE.md` §"Positive framing" — the framing
  rule architecture docs follow.
- `~/primary/ESSENCE.md` §"Skeleton-as-design" — why
  architecture stays prose-plus-visuals, not implementation
  blocks.
- `~/primary/repos/criome/ARCHITECTURE.md` — canonical worked
  example of meta-scope architecture.
- `~/primary/repos/signal/ARCHITECTURE.md` — canonical worked
  example of per-repo architecture for a contract crate.
