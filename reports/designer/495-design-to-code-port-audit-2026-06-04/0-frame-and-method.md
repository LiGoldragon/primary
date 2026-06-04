---
title: 495 - Design-to-code port audit - frame and method
role: designer
variant: Synthesis
date: 2026-06-04
topics: [audit, intent-manifestation, constraint-witness, abstraction, next-stack, repetition]
description: |
  Orchestrator frame for a five-agent audit of the schema-derived next
  stack: where does ratified intent, constraint, and architecture exist
  in the design layer but not in the code? Each agent owns a disjoint
  slice, writes its numbered entry here, ports the safe ratified deltas
  on a feature branch, and proposes the rest. The 6-overview synthesises;
  the psyche report (496) carries the propositions for the psyche.
---

# 495 - Design-to-code port audit

## The directive

The psyche, as designer: acquire intent from Spirit and design from the
architecture and intent documents, read the recent designer and operator
reports, then audit with sub-agents to **port missing design into
implementation** — especially intent, constraints, and architecture.
Produce a meta-report where each sub-agent gets an entry, and a psyche
report giving the low-down: how everything is going, what needs defining
further or better. Every agent and the orchestrator hunts **bad
patterns, winded code, and repetition** — repetition is the tell that an
abstraction is missing. Acquire all Rust and coding skills before
writing code.

This is a working order, not new durable intent. The principles it
invokes are already captured: continuous manifestation of intent into a
repo's INTENT.md/ARCHITECTURE.md is part of the work cycle [record 944,
Maximum]; repeated nested wrapper construction signals bad design or a
missing layer [record 1557, High] and more generally repetition resolves
into a single named pattern [ESSENCE §Beauty]; audit implementation
against intent for missing constraint witnesses and add tests that prove
the intended path rather than leaving intent as prose [record 1565,
High]; read the Rust discipline skills before authoring Rust source
[record 884, Maximum]. No Spirit capture this turn.

## Ground truth at frame time

The operator has **already landed** the bulk of the recent schema-stack
design, which narrows the porting surface and the collision risk:

- Alias-vs-newtype lowering is committed: `schema-next` exposes
  `TypeDeclaration::Alias(AliasDeclaration)`; `schema-rust-next` emits
  `pub type` for bare bindings (`schema-rust: emit aliases for bare
  declarations`, `schema-rust: skip From impls for alias payloads`).
  This satisfies the "once alias lowering lands upstream" caveat in
  records 1560/1561/1563.
- Typed SymbolPaths landed (`schema-next: add typed symbol paths`,
  `schema-next: resolve symbol path roles through asschema`).
- Bare-name header namespace resolution landed: spirit-next's generated
  `schema/lib.schema` carries the bare header
  `[Record Observe Lookup Count Remove LookupStash]` and reply header
  `[RecordAccepted RecordsObserved RecordsStashed RecordFound
  RecordsCounted RecordRemoved Error Rejected]` (records 1555/1556/1562).
- spirit-next uses alias payloads end to end with e2e constraints
  (`spirit-next: add alias payload e2e constraints`).

So this audit is mostly a **completeness-and-quality** pass over landed
design, not a greenfield port: how complete is each landed mechanism
versus the full intent, what load-bearing intent has no constraint
witness, what repetition signals a missing abstraction, and what design
remains unimplemented (and of that, what is ratified versus open).

## Method

Five agents, disjoint slices so parallel writes never collide. Each
acquires the Rust discipline skills (`skills/rust-discipline.md` plus the
linked sub-files, `skills/abstractions.md`, `skills/actor-systems.md`)
and the slice repo's own AGENTS.md/INTENT.md/ARCHITECTURE.md/skills.md
before touching code, audits its slice, writes its numbered entry in this
directory, and returns structured findings.

Each gap is classified into one of:

- **DONE** — design is fully manifested in code; nothing to port.
- **RATIFIED-PORTABLE** — ratified intent or architecture, design firm,
  not yet (fully) in code, low collision. The agent returns a concrete
  port proposal with file paths and code; the orchestrator lands the
  safe tier-1 (manifest intent into the repo's INTENT.md/ARCHITECTURE.md)
  and tier-2 (additive constraint-witness tests) deltas in Phase 2, with
  cargo verification and revert-on-red. Tier-3 (production feature code)
  is proposed for the operator, the implementing half of the dance.
- **UNRATIFIED-PROPOSE** — design exists but the psyche has not ratified
  it (or it is an open lean). Proposed in the psyche report; not ported.
  Porting unratified design violates the dance: implementation requires
  intent clear AND design good enough.
- **OPERATOR-ACTIVE** — inside the operator's current in-flight path.
  Flagged, not touched.

### Why the agents audit and the orchestrator ports

The five agents are **read-only**: they audit, write their entry, and
return concrete port proposals (file paths plus code). The orchestrator
does the actual porting in Phase 2. This keeps every code edit under one
verified hand rather than five parallel writers contending over jj
worktrees and generated files, and it keeps the implementing edits inside
the dance — the designer manifests intent into the design layer and
authors constraint witnesses as worktree mockups, while production
feature code is handed to the operator. Porting discipline:

- Generated files are never hand-edited [record 1563]: spirit-next's
  `src/schema/lib.rs` is generated from `schema/*.schema`; schema changes
  go in the `.schema` source and the build regenerates.
- Code and repo-doc edits land on a feature branch in
  `~/wt/github.com/LiGoldragon/<repo>/`, never on the `/git/...` main the
  operator owns; the branch is reported for operator integration.
- jj messages are always inline (`-m`); never open an editor.
- A port that cannot be made cargo-green is reverted and downgraded to a
  proposal in the findings — never leave a repo red.
- Repo INTENT.md/ARCHITECTURE.md edits add only the genuinely-missing
  recent-intent deltas; they do not rewrite what the operator already
  manifested on main.

## Agent roster

| Entry | Slice | Repo(s) |
|---|---|---|
| 1 | Pilot, runner loop, lifecycle hooks, daemon string boundary, e2e witnesses | `spirit-next` |
| 2 | SymbolPath, header namespace, multi-pass parsing, alias lowering source side | `schema-next` |
| 3 | Alias-vs-newtype emission, wrapper-repetition, emission-code abstraction | `schema-rust-next` |
| 4 | Trace as typed schema interface, strings-at-edges, lifecycle hooks, thin-doc manifestation | `triad-runtime`, `nota-next` |
| 5 | Cross-cutting repetition/abstraction hunt; meta-signal rename status; triad-shape conformance (read-only) | next stack + contracts |

The 6-overview synthesises landed-versus-proposed and the abstraction
findings; the psyche report `496` carries the propositions, open
questions, visuals, and code for the psyche.
