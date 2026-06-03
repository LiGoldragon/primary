---
title: 466.0 — Frame and method
role: designer
variant: Design
date: 2026-06-01
topics: [situation, triad-engine, honesty, schema-driven, actor-model, interface-first, meta-report]
parent_meta_report: reports/designer/466-triad-engine-honesty-situation-2026-06-01
slot: 0
description: |
  Meta-report frame for the triad-engine honesty situation requested by psyche 2026-06-01. Two sub-agents dispatched in parallel: A audits SCHEMA HONESTY (what schema-rust-next emits vs what spirit-next hand-writes; how much of the architecture is truly schema-driven vs Rust-leakage); B audits ACTOR MODEL + INNER/OUTER FLOW (the signal-in → nexus → sema → signal-out flow shape; Nexus as inner/outer world boundary per Spirit 1388; slim Nexus output per Spirit 1389; meta-actor interface fit). The orchestrator synthesizes both into 3-overview.md when they return.
---

# 466.0 — Frame and method

## Why this report exists

The psyche asked for *"a situation on how honest the traits are and where they're implemented, the whole enforced behavior of the triad engine, the signal nexus SEMA engine, and how the actor model keeps it at the same design, but with the sort of meta actor with interfaces defined that are defined in our new schema language."*

Three substantive concerns:

1. **Honesty.** Is the triad engine architecture *actually* schema-driven, or is the schema-emitted surface thin while the real behavior sits in hand-written Rust? The Rust impl code should be TERSE per Spirit 1387 — match decisions, write/import algorithms, forward results to the next component. When hand-written Rust accumulates substantial behavior beyond match+algorithm+forward, that signals architecture leakage out of schema.

2. **Actor model fit.** The current spirit-next has `SignalActor` + `Nexus` + `Store` as concrete structs implementing engine traits. The user's framing: the actor model + meta-actor with interfaces in the new schema language should keep the design clear, delineated, OO-original-insight-aligned, with interfaces FIRST.

3. **Inner/outer worlds.** Nexus sits between two worlds — Signal is the outer world (clients wire ingress/egress), SEMA is the inner world (durable state). Nexus is the decision center. Spirit 1388 captures this vocabulary. The Nexus IO contract should be slim (query type → result acknowledgement); clients query for specifics later (Spirit 1389, extending 1351's signal slim-acknowledgement up to Nexus).

The report's verdict needs to be HONEST about where the architecture is genuinely schema-driven vs where Rust hand-written code carries substantive behavior — not aspirational about what schema-driven means.

## Method — two sub-agents in parallel

Both sub-agents work on PRIMARY (no worktree; they're read-only audits writing to `reports/designer/466-*`). They run in background (per AGENTS.md hard override).

### Sub-agent A — Schema honesty audit

**Scope.** What does `schema-rust-next` emit? What does spirit-next/src/schema/lib.rs CONTAIN (the generated code)? What does spirit-next/src/*.rs (engine.rs, nexus.rs, store.rs, trace.rs) implement on top? Where is the architecture genuinely schema-driven vs where is Rust hand-written substantively?

**Output**: `reports/designer/466-triad-engine-honesty-situation-2026-06-01/1-schema-honesty-audit.md`.

**Key references**:
- `/git/github.com/LiGoldragon/schema-rust-next/` — emitter source.
- `/git/github.com/LiGoldragon/spirit-next/src/schema/lib.rs` — generated code.
- `/git/github.com/LiGoldragon/spirit-next/src/{engine.rs, nexus.rs, store.rs, trace.rs}` — hand-written impl.
- Spirit records 1326-1336, 1357, 1361 (engine-trait architecture) + 1387 (terseness Principle).
- `skills/component-triad.md` §"Runtime triad engine traits" — workspace discipline.

### Sub-agent B — Actor model + inner/outer flow audit

**Scope.** Map the signal-in → nexus → sema-in/out → nexus-out → signal-out flow with diagrams. Show how concrete spirit-next types (SignalActor, Nexus, Store) implement engine traits + carry actor identity. Assess actor-model fit (per `skills/actor-systems.md`). Articulate the inner/outer world framing per Spirit 1388. Assess the slim-Nexus-output pattern per Spirit 1389 — is Nexus output currently slim or full-payload? Where would slim-acknowledgement + client-query-for-specifics fit?

**Output**: `reports/designer/466-triad-engine-honesty-situation-2026-06-01/2-actor-model-and-flow.md`.

**Key references**:
- `/git/github.com/LiGoldragon/spirit-next/src/{engine.rs, nexus.rs, store.rs}` — concrete actor types.
- `/git/github.com/LiGoldragon/spirit-next/tests/runtime_triad.rs` — runtime witnesses showing actual flow.
- Spirit records 1326-1336, 1357, 1361, 1365 (engine-trait + actor-trait + Correction Maximum) + 1388 (inner/outer world) + 1389 (slim Nexus output) + 1351 (signal slim acknowledgement).
- `skills/component-triad.md`, `skills/actor-systems.md`.

## Synthesis shape (3-overview.md, after both return)

The orchestrator's synthesis answers the three concerns directly:
1. Honesty verdict: percentage-shape estimate of how schema-driven the architecture really is, where Rust leakage is, what needs to move to schema.
2. Actor model fit: where current shapes match meta-actor-with-interfaces vision, where they diverge, what gaps the actor-trait pilot (Spirit 1365 if-possible hedge) needs to close.
3. Inner/outer worlds + slim Nexus output: vocabulary mapped to current code; concrete gaps where Nexus output is too verbose.

The synthesis names ratification candidates if any new design questions surface.

## Constraints (all sub-agents)

- READ-ONLY audits. No code edits; no worktree creation. Output is the sub-report markdown file.
- All workspace hard overrides apply: bracket NOTA strings only; no `---` rules; mermaid 5-node cap (Spirit 1282); full English words.
- Report under 600 words substance per sub-report (diagrams excluded from count).
- Commit + push your sub-report to primary main when complete. Designer-lane authority on `reports/designer/`.
