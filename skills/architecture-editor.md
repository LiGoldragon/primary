# Skill — architecture editor

*How `ARCHITECTURE.md` files are named, located, scoped, and
maintained.*

---

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
is the apex; `persona-message`, `persona-router`,
`persona-system`, `persona-harness`, `persona-store`,
`signal-persona`, etc. each carry their own.

---

## Where each kind of statement lives

| Doc | What goes there |
|---|---|
| `ARCHITECTURE.md` (meta) | How the components fit together. The runtime topology. The wire vocabulary. The flow of state across processes. The named clusters and their boundaries. |
| `ARCHITECTURE.md` (per-repo) | This repo's role, what it owns, what it doesn't, code map, invariants, contracts at its edges. |
| `skills.md` (per-repo) | How an agent works *in* this repo. The "if you're editing here, here's what's load-bearing." |
| `AGENTS.md` (per-repo) | Thin shim that names the repo's role + carve-outs from the workspace contract. |
| Reports | Decision records, design rationales, audits, syntheses. The path that led to the architecture. |

If a statement is "what the system IS," it goes in
`ARCHITECTURE.md`. If it's "what an agent should do," it goes in
`skills.md`. If it's "why we chose this," it goes in a report
and the architecture cites the report only when the rationale is
load-bearing for understanding the shape.

---

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

## 5 · Invariants

<things that must always be true; the load-bearing constraints>

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

---

## What an `ARCHITECTURE.md` does NOT contain

- **Implementation code.** Per `~/primary/ESSENCE.md`
  §"Skeleton-as-design", the type system enforces shape; prose
  decays. A few-line snippet of a type's surface is fine; an
  implementation block is not.
- **Decision history.** "We considered X but went with Y" lives
  in a report. The current `ARCHITECTURE.md` describes Y as
  *what is*; if rationale is load-bearing for understanding,
  cross-reference the report.
- **Roadmap or implementation order.** "Will land" / "is
  planned" belongs in a report. The architecture is what the
  system *is*; if a piece isn't built yet, either describe it
  as "the destination" with a status note or leave it for the
  report.
- **Tour-style narration.** "First, you'll find the foo
  module..." Architecture is reference, not a guided tour.
- **Restatement of workspace skills.** The architecture cites
  workspace skills; it doesn't repeat them.

---

## When to edit

Edit `ARCHITECTURE.md` when:

1. **The shape has changed.** A new component, a renamed
   contract, a moved boundary, a different transaction owner.
   Edit immediately. The architecture is a *current-shape*
   document; lag costs comprehension.
2. **A reader will be confused** by the current state. If a
   statement is technically right but easy to misread, rewrite.
3. **A new invariant has emerged** and is now load-bearing.
   Add it to §"Invariants".
4. **A cross-reference to a neighbor has stale or wrong info.**
   Update the cross-reference; if the neighbor's architecture
   has drifted, surface it (or open a bead for that repo's
   owner).

Don't edit for:

- Historical interest. The path is in commit history.
- Tentative plans. Use a report.
- Fixing a typo in a comment block. Skip the ARCHITECTURE
  ceremony; just edit.

---

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

---

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

---

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

---

## See also

- `~/primary/skills/skill-editor.md` — the parallel skill for
  `skills.md` files; same conventions for cross-references and
  scope.
- `~/primary/skills/reporting.md` — when to write a report
  versus update an architecture.
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
