---
title: 446 — Frame: how to port the next stack to other components
role: designer
variant: Design
date: 2026-06-01
topics: [porting-research, next-stack, landscape, playbook, sequencing, meta-report, frame]
parent_meta_report: reports/designer/446-next-stack-porting-research-2026-06-01
slot: 0
description: |
  Frame for the parallel research meta-report: how should the (nota-next + schema-next + spirit-next) substrate be ported to other workspace components? Three sub-agents cover landscape / playbook / sequencing.
---

# 446 — Frame: how to port the next stack to other components

## Why this research

The next stack — `nota-next` parser + `schema-next` lowering + `schema-rust-next` emission + `spirit-next` runtime pilot — has reached a stable shape. Designer 444 (`/444-stack-vision-2026-05-31/`) presents the architecture; designer 445 (`/445-next-stack-audit-2026-06-01.md`) confirms the substrate honors workspace discipline. The natural next question: **how do we apply the same substrate to the rest of the component fleet?**

Many components in the workspace are candidates: every triad (`<component>` + `signal-<component>` + `owner-signal-<component>`) currently relies on hand-written Rust types or legacy `schema` + `signal-core` plumbing. The next stack demonstrates a derive-driven pipeline (schema source → typed Asschema → rkyv artifact → schema-emitted Rust nouns → runtime methods) that should let each component drop its hand-written wire types in favor of schema-emitted ones.

This research lays the foundation for that fleet-wide migration. Output is **not implementation** — it's a designer report tree that operator + cluster-operator can use to file the actual porting beads in the right order.

## What this meta-report covers

| File | Sub-agent | Focus |
|---|---|---|
| `0-frame-and-method.md` | (this file, orchestrator) | Why, what, sub-agent assignment, retirement policy. |
| `1-component-landscape.md` | sub-agent 1 | **WHAT to port** — survey active components, identify next-stack candidates, classify by current shape (legacy-schema / hand-typed / signal-only / signal-contract), estimate fit. |
| `2-porting-playbook.md` | sub-agent 2 | **HOW to port** — step-by-step procedure: schema source authoring, build.rs witness, runtime migration, parallel-track discipline, witness tests. Uses spirit-next as the canonical worked example. |
| `3-sequencing-and-dependencies.md` | sub-agent 3 | **IN WHAT ORDER to port** — which candidates land first, which need schema-core extraction or other horizons first, parallelizable vs sequential, headline first slices. |
| `4-overview.md` | (orchestrator synthesis) | Convergence reading; recommended next slice; operator-bead-shaped action list. |

## Sub-agent assignment

All three sub-agents are dispatched in parallel (non-blocking per `AGENTS.md` §"Every subagent dispatch is non-blocking"). Each receives this frame as context plus a focused brief.

**Sub-agent 1 — Component landscape scout.** Lane: designer (inherits orchestrator's lane). Brief: survey `protocols/active-repositories.md` + `repos/` for components that could plausibly port to the next stack. For each candidate, name (a) current type substrate, (b) whether a signal contract already exists, (c) the rough port-cost and port-benefit, (d) the rank in a "first wave / second wave / later" ordering. Output: `1-component-landscape.md`. Target: 400-700 lines, with a candidates table + per-candidate paragraph.

**Sub-agent 2 — Porting playbook.** Lane: designer. Brief: write the operator-side recipe. Given a component X that wants to adopt the next stack, what are the steps? Use spirit-next as the worked example — its `schema/lib.schema` + `build.rs` + checked-in `src/schema/lib.rs` + the hand-written runtime over schema-emitted nouns IS the recipe. Cover: authoring the schema source; the build.rs witness pattern; the parallel-track discipline (new schema-derived crate alongside the legacy one until cutover); how to migrate one verb at a time; how to keep wire compatibility across the transition; the typed-witness tests; what NOT to port. Output: `2-porting-playbook.md`. Target: 500-800 lines, with a mermaid diagram of the recipe, code excerpts from spirit-next, and a worked migration for one near-trivial candidate.

**Sub-agent 3 — Sequencing + dependency analysis.** Lane: designer. Brief: read designer 444 §5 horizon ledger and designer 445 audit; map the dependency graph between (a) the open horizons (schema-core extraction, generic store substrate, variant projections, CLI source helper) and (b) the candidate components from sub-agent 1's landscape. For each candidate, name what horizons must land before its port is sensible (e.g. a contract-heavy component needs cross-crate import resolution to be mature). Recommend a first slice + a sequencing chain. Output: `3-sequencing-and-dependencies.md`. Target: 300-500 lines, with a phased dependency graph + first-slice recommendation.

## Required reading for every sub-agent

These files MUST be read before writing — they pin the substrate the porting work targets:

- `reports/designer/444-stack-vision-2026-05-31/` (all four body reports + the overview).
- `reports/designer/445-next-stack-audit-2026-06-01.md` (this audit).
- `protocols/active-repositories.md` (workspace component map).
- `AGENTS.md` (workspace hard overrides).
- `skills/component-triad.md` (the daemon + signal + owner-signal triad pattern).
- `skills/contract-repo.md` (wire-contract crate discipline).
- `skills/feature-development.md` (multi-repo feature branch coordination).
- `/git/github.com/LiGoldragon/spirit-next/{ARCHITECTURE.md,INTENT.md,build.rs,schema/lib.schema}` (the canonical worked example).

Sub-agent 1 additionally reads `protocols/active-repositories.md` candidate entries + the `ARCHITECTURE.md` of each candidate it surveys.

Sub-agent 2 additionally reads `spirit-next/build.rs`, the build-step code in `schema-next/src/engine.rs`, and the `schema-rust-next` README + entry points.

Sub-agent 3 additionally reads designer 443 (`/443-design-improvements-audit-2026-05-31/`) for the gap analysis that feeds the dependency-order question.

## Discipline reminders (per AGENTS.md hard overrides)

- **No mermaid graph with more than 5 nodes** (Spirit 1282). Split.
- **Reports as visuals** — mermaid + tables + worked examples, not prose walls.
- **Inline summaries on every cross-reference** — when citing another report or repo, paraphrase enough that the reader doesn't have to context-switch.
- **Operator-bead shape** — the recommendations should be small + distributable + actionable, not "a designer should think about this more". Each first-slice candidate names what operator does and what evidence proves the port worked.
- **No subagent dispatches from these sub-agents** — they do their own research and write their own report; do not spawn further sub-agents.

## What "ported" means in this research

For this meta-report: a component is "ported" when its **wire-and-runtime nouns are schema-emitted** from a `schema/lib.schema` source (or equivalent), instead of being hand-written Rust types. The hand-written runtime (the actor logic, the storage methods, the daemon main loop) stays hand-written — it attaches behavior to schema-emitted nouns, just as spirit-next's `Engine`, `Nexus`, `Mail<Phase>`, `Store` attach behavior to `Input` / `Output` / `NexusInput` / `SemaInput`.

The CLI and daemon binaries adopt the single-NOTA-argument rule (`AGENTS.md` §"NOTA is the only argument language"). The wire shape becomes rkyv-only at the daemon socket; the CLI does NOTA at the human edge. Configuration moves into a typed Configuration rkyv file consumed by daemon-side `from_binary_path`.

Not in scope for this meta-report: schema-core extraction itself (designer 444 §5 horizon 1 — the headline future work that lifts shared mail/route nouns out of spirit-next). That extraction is a precondition for some candidates; this research treats it as a dependency to map, not a thing to plan.

## Retirement policy

This meta-report supersedes ad-hoc porting recommendations scattered across earlier reports. If sub-agent 3's sequencing recommends specific operator beads, those beads become the canonical surface; informal beads created elsewhere should retire into this report's chain.

## Cross-references

- `reports/designer/444-stack-vision-2026-05-31/` — what the next stack IS.
- `reports/designer/445-next-stack-audit-2026-06-01.md` — what the next stack honors today.
- `reports/designer/443-design-improvements-audit-2026-05-31/` — the gap analysis that feeds the horizon ordering.
- `protocols/active-repositories.md` — workspace component map.
- `AGENTS.md` §"NOTA is the only argument language", §"Component triad means daemon + working signal + policy signal".
- `skills/component-triad.md`, `skills/contract-repo.md`, `skills/feature-development.md`.
