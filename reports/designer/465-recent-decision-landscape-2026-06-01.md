---
title: 465 — Recent decision landscape consolidation
role: designer
variant: Research
date: 2026-06-01
topics: [recent-decisions, consolidation, engine-trait, testing-trace, deploy-nix, workflow, rkyv-schema-emission, spirit-triad-naming]
description: |
  Review of designer-lane recent reports (458, 461, 463) + Spirit captures (1326-1380) surfacing the important decisions taken or pending. Organizes by theme (engine-trait architecture / testing+verification / deploy+Nix / workflow / schema-emission) and tiers by magnitude. Names the pending psyche ratifications. Produced in response to the psyche's request to represent the recent decision landscape.
---

# 465 — Recent decision landscape consolidation

## TL;DR

The 2026-05-30 → 2026-06-01 window landed a high-magnitude decision cluster — **the engine-trait runtime architecture** for Signal/Nexus/SEMA, ratified in code at spirit-next commit `d29dc6c` (SemaEngine apply/observe split). On top of that, the **testing-build verification surface** is mid-implementation: positive-grep banned as deployment proof; testing-trace pilot live in-process; the trait-on-schema-derived-interfaces shape ratified at Correction Maximum (Spirit 1365); the CLI-translated debug wrapper enum + Nix differentiated packages + last-version package decisions just captured by operator (Spirit 1370-1375). Workflow discipline (designer-on-worktree, operator-on-main, depth-first prototype-proving) settled at High. Three psyche ratifications still pending: designer 458's spirit-triad naming gate, designer 463's gap A (cargo+NOTA stratification) and gap B (testing-instrumentation triad placement).

The decision tier is heavy — 20+ Maximum/High records in 11 days. The architectural direction is coherent and converging across operator + designer + Spirit ratification (the four-way convergence pattern noted in designer 463 §8).

## Section 1 — Engine-trait runtime architecture

The deepest cluster. Anchors the whole next-stack direction.

| Decision | Spirit | Magnitude | Status |
|---|---|---|---|
| Engine-trait architecture: Signal/Nexus/SEMA each get a typed engine trait emitted from schema source | 1326-1336 | Maximum (multiple) | LANDED in code |
| SignalEngine has 2 methods (triage on input, reply on output) — method count matches wire events | 1361 | High | LANDED at spirit-next `5fc96397` |
| NexusEngine has 1 method (execute) — synchronous compute step | 1361 | High | LANDED |
| SemaEngine has 2 methods (apply for writes, observe for parallel reads) | 1332 | Maximum | LANDED at spirit-next `d29dc6c` |
| Engine-trait architecture is live in spirit-next; substrate is `src/schema/lib.rs:1431-1442` | 1357 | High | RATIFIED (live-landing clarification) |
| Trace events are a trait on schema-derived interfaces — peer to engine traits | 1365 | **Correction Maximum** | RATIFIED |
| Signal/Nexus/SEMA should each have an ACTOR TRAIT in addition to engine traits (if-possible hedge) | 1365 | Correction Maximum | RATIFIED with hedge; pilot in flight |
| Trace runs live through daemon → CLI as human-facing log surface | 1370 | Maximum | RATIFIED; implementation in flight |

**Cluster narrative.** The engine-trait architecture is the structural backbone of the next-stack pilot. SignalActor + Nexus + SemaActor were concrete structs in spirit-next's first cut; they're being lifted to schema-emitted ENGINE TRAITS, with concrete spirit-next types implementing those traits. The SemaEngine apply/observe split was the standout gap operator and designer audits both surfaced; it closed in code 2026-06-01 15:17:26 at commit `d29dc6c`. The trace trait + actor trait additions are the next layer of the architecture, ratified at Correction Maximum (Spirit 1365) and in active implementation via parallel operator-on-main + designer-on-worktree paths.

The actor-trait shape carries the "if-possible" hedge — pilot the super-trait form (`SignalActor: SignalEngine` with associated `type Trace`) on a worktree before mandating it. Spirit 1367 (which I duplicated and removed) was an honest attempt to capture the hedge; 1365 already covered it.

## Section 2 — Testing-build verification surface

The decisions that make architecture provable, not assertable.

| Decision | Spirit | Magnitude | Status |
|---|---|---|---|
| Positive grep deployment checks are not allowed as proof of live architecture | 1341 | **Maximum** | RATIFIED |
| Positive grep proves text presence, not live use; proof requires compile/execute/round-trip/observe | 1342 | Maximum | RATIFIED |
| Schema-derived runtime supports optional testing/instrumentation build emitting structured trace events | 1343 | Maximum | LANDED partial (in-process); socket pending |
| Testing-mode logging configured by typed NOTA configuration; CLI as log surface | 1344 | High | PENDING implementation |
| Signal admit/reply, Nexus execute/decide, SEMA write apply / SEMA read observe each emit trace | 1345 | High | LANDED (operator 277 + spirit-next `5fc96397`) |
| Schema-emitted objects have optional-compilable logging hooks at the emitter layer | 1346 | Maximum | IN FLIGHT (sub-agent + operator) |
| CLI is the log surface — testing-mode log socket routes back to CLI | 1347 | Maximum | PENDING implementation |
| Build configuration is a NOTA struct with fields | 1348 | Maximum | PENDING (gap A blocks) |
| Testing-build logging socket is the canonical Layer 2 runtime witness | 1349 | Maximum | RATIFIED as proof discipline |
| Each engine carries optional test-build code that self-verifies it ran | 1350 | Maximum | LANDED |
| Signal reply is typically a brief acknowledgement with an identifier | 1351 | High | RATIFIED |
| Trace code optional at compile-time; Nix exposes differentiated packages | 1371 | Maximum | IN FLIGHT |
| Stdout default for debug-mode when no destination configured | 1374 | High | IN FLIGHT |

**Cluster narrative.** The verification cluster has two halves: the positive-grep ban (1340-1342) is the negative constraint — what NOT to use as proof; the testing-build logging architecture (1343-1351 + 1370-1374) is the positive substrate — what IS the canonical Layer 2 runtime witness. Operator's spirit-next `5fc96397` lands the in-process witness; the next slice (in flight via operator-on-main + designer's dispatched sub-agent) takes it to end-to-end CLI translation with default stdout.

The proof-of-usage ladder (Layer 1 STATIC, Layer 2 RUNTIME, Layer 3 BEHAVIORAL) was migrated by designer 461 from retired designer 459 to `skills/architectural-truth-tests.md` §"Proof-of-usage ladder — choose cheapest sufficient" — the canonical discipline.

## Section 3 — Deploy + Nix package shape

The new cluster — captured in operator's Spirit 1370-1375 burst.

| Decision | Spirit | Magnitude | Status |
|---|---|---|---|
| Trace code optional at compile-time; Nix exposes differentiated packages for lean vs trace-enabled builds | 1371 | Maximum | IN FLIGHT |
| Every component's standard Nix package set must include a last-version package | 1372 | Maximum | RATIFIED, IMPLEMENTATION DEFERRED |
| No NOTA between components; daemon binary-only; CLI is the translation/debugging surface that wraps a normal call in a debugging request | 1373 | **Principle Maximum** | RATIFIED |
| CLI defaults to stdout for trace events when no explicit destination configured | 1374 | High | IN FLIGHT |
| Shared Nix library for component-flake boilerplate (last-version + current + next + checks) — if-possible hedge | 1375 | High | RATIFIED, IMPLEMENTATION DEFERRED |

**Cluster narrative.** Three of these are NEW (1372 last-version package, 1373 CLI-wraps-debug-request, 1375 Nix library) — captured in operator's burst at the end of the 2026-06-01 session. The last-version package decision (1372 Maximum) extends the existing next/main/previous deployment vocabulary from `skills/spirit-cli.md` §"Deployment slots" to a STANDARD package set every component flake provides. Rationale: schema-upgrade migrations + message compatibility during client switchover need the prior release at hand.

1373 (Principle Maximum) is the strongest classification in this cluster — it's a PRINCIPLE that no NOTA crosses between components, and the CLI is the wrapping/translation surface. Daemons stay binary; CLI absorbs the human-facing complexity. The "debugging request wraps a normal call with options" pattern (the wrapper enum variant on the root call) is the architectural shape this implies.

## Section 4 — Process + workflow discipline

The decisions about HOW work happens.

| Decision | Spirit | Magnitude | Status |
|---|---|---|---|
| Operator implementation lands on main; designer work for new design/prototype rebases on main and proceeds in worktrees | 1352, 1354 | High | RATIFIED |
| Design work progresses by proving one prototype capability at a time in a worktree (depth-first, not breadth-first) | 1355 | High | RATIFIED |
| After active implementation/prototype sub-agent work, run context maintenance and fresh-intent audit before deciding next slice | 1353 | High | RATIFIED |
| Persistent memory for tool-using agents is the queryable tool-call trace, not the model context window | 1356 | High | RATIFIED (architectural property — implementation horizon) |
| Intent gaps are filled by cross-pollinating patterns from elsewhere in the intent | 1364 | Medium | RATIFIED (designer-authored) |

**Cluster narrative.** This cluster names the workflow shape this session ran on. Operator owned main + integration; designer worked on worktrees for new design + prototypes. Depth-first prototype-proving (one capability at a time) replaced breadth-first design fan-out. Context maintenance after each sub-agent burst (rather than letting stale context drive next slices). Cross-pollination methodology (designer-authored Spirit 1364) for surfacing implicit intent.

The four-way convergence pattern (operator 278 + designer 463 + Spirit 1365 + operator 279) noted in designer 463 §8 extends `skills/designer.md` §"Three-way convergence as correctness signal" to a fourth surface — strong correctness signal when independent agents + ratification converge on the same architectural direction.

## Section 5 — Schema-emission rules from rkyv audit

The cluster from designer 452's audit, captured 2026-06-01.

| Decision | Spirit | Magnitude | Status |
|---|---|---|---|
| Schema-rust-next emitter wraps recursive enum variants in Box automatically | 1358 | **Maximum** | RATIFIED |
| Schema-rust-next consolidates same-shape sibling variants by semantic family | 1359 | High | RATIFIED |
| Schema-rust-next sub-divides closed-sum enums past ~10 variants | 1360 | High | RATIFIED |

**Cluster narrative.** Designer 452's rkyv enum-wrapping audit produced eight pilot tests on the `audit-rkyv-enum-wrapping-presumption` schema-next branch. Three emitter rules came out:
- **1358 (Maximum)**: recursive-variant Box wrapping prevents unsized-type compile failures every schema author would hit by hand.
- **1359 (High)**: semantic-family grouping reduces match-table size + improves authoring ergonomics for repeated-shape variants.
- **1360 (High)**: sub-division past ~10 variants splits flat enums into kinship-grouped sub-enums.

Implementation: not yet landed in the emitter; the audit branch carries the witnesses.

## Section 6 — Pending psyche ratifications

Three items where the design awaits your yes/no.

### 6.1 — Designer 458 spirit-triad naming gate

**The decision**: replace `core-signal-spirit` with EITHER `owner-signal-spirit` (Option A — workspace convention) OR `meta-signal-spirit` (Option B — proposed rename per Spirit 290 + 299 at Minimum/Medium magnitude with explicit "tentative" framing).

**Designer recommendation**: Option A. Reasons: (a) honors Spirit 293 ("owner-signal remains active until explicit rename lands"); (b) Spirit 290 + 299 are Minimum/Medium with "tentative" framing — Phase 0 fold is not the right slice for fleet-wide rename; (c) Option B requires renaming 10+ existing `owner-signal-*` repos for fleet consistency, multi-week scope; (d) Option A is reversible (folds into Option B's fleet-wide sweep if/when it lands).

**What it unblocks**: Designer 446 Phase 0 spirit fold. Phase 0 estimate (one operator-week) absorbs the rename of `core-signal-spirit` → `owner-signal-spirit` as the first ~30-minute mechanical step.

**Ask**: ratify Option A (single yes), or pick Option B (single no — designer writes follow-up for fleet-wide rename slice).

### 6.2 — Designer 463 gap A (cargo+NOTA stratification)

**The decision** (proposed Spirit Principle High): *"Compile-time and runtime configuration are stratified — cargo features control which code exists in the binary (compile-time existence); NOTA configuration drives runtime behavior. Optional instrumentation lands as a cargo feature for compile-time inclusion + a typed NOTA configuration field for runtime control."*

**Source**: cross-pollinated from the single-argument rule + Spirit 1346 (feature-gated emitter) + Spirit 1348 (build config as NOTA struct). Operator 279's Pattern 2 framing.

**Operator 279 framing**: *"Capture or ASK PSYCHE to confirm Pattern 2 before typed trace configuration work starts."*

**What it unblocks**: Designer 463 Gap 3 (typed NOTA build/test config) sub-agent dispatch. Without the principle stated, the sub-agent will likely conflate the layers.

**Ask**: confirm the stratification principle (single yes) or reject/refine.

### 6.3 — Designer 463 gap B (testing-instrumentation triad placement)

**The decision** (proposed Spirit Decision High): *"Testing instrumentation surface follows the component triad pattern — trace nouns + traits live in signal-<component>; trace transport lives in the daemon repo; trace policy (emit/filter/socket-path) lives in owner-signal-<component>."*

**Source**: cross-pollinated from the component triad pattern (daemon + signal-<component> + owner-signal-<component>). Operator 279's Pattern 3 framing.

**Operator 279 framing**: *"Capture or ASK PSYCHE to confirm Pattern 3 before splitting trace nouns and trace policy across triad crates."*

**What it unblocks**: When the trait emission slice (currently in flight) lands, the question of "which repo hosts the trace types and trace policy" needs an answer. Without gap B, the implementation will pile everything into one repo by default.

**Ask**: confirm the triad placement (single yes) or reject/refine.

## Section 7 — Decisions retired or removed during the session

A small list, for completeness.

| Item | Disposition | Reason |
|---|---|---|
| `Mail<Phase>` typestate + 4 candidates | RETIRED at spirit-next `d29dc6c` | Designer 456 + Spirit's typestate-retires-when-borrow-rules-enforce-its-invariant principle (now in `skills/rust/methods.md`) |
| Old single SEMA apply surface | RETIRED at schema-rust-next `06a7797` | Replaced by apply/observe split per Spirit 1332 |
| `Nexus::process<Payload>` payload-mail public bypass | RETIRED at spirit-next `d29dc6c` | Per designer 455 + 456 findings |
| Designer 459 (proof-of-usage witness research) | RETIRED by designer 461 sweep | Substance migrated to `skills/architectural-truth-tests.md` |
| Designer 453 (engine-trait broad triad adaptation) | RETIRED by 461 | Substance migrated to `skills/component-triad.md` §"Runtime triad engine traits" |
| Designer 454 (engine role pipeline refinement) | RETIRED by 461 | Same skill landing |
| Designer 415 + 439 (context-maintenance ledgers) | RETIRED by 461 successor sweep | Per `skills/context-maintenance.md` discipline |
| My Spirit 1366 (TraceEngine naming) | REMOVED | Duplicated operator's 1365 |
| My Spirit 1367 (actor-traits restatement) | REMOVED | Duplicated operator's 1365 |
| My Spirit 1376-1380 (last-version, Nix library, debug wrapper, CLI translation, stdout default) | REMOVED | Duplicated operator's 1370-1375 |

The duplications are honest — I failed the gap-fill discipline twice (forwarded-prompts rule from AGENTS.md: query operator's captures FIRST before recording on a prompt addressed to operator). Self-correction noted; sub-agent dispatched today briefed to always query Spirit before capturing.

## Section 8 — What's NOT on this list

For honest scope:
- Older horizon-level documents (designer 443 stack vision, 444 horizon ledger, 446 porting research) carry directional intent but not decisions in the Spirit-Decision sense; they're surveys, not decisions.
- The spirit-fold itself (Phase 0 of porting) is BLOCKED on 458 ratification, not yet a decided slice.
- The upgrade-as-SEMA design (designer 447) is a single design report not yet ratified; sits as horizon.
- The `local-ai` toolkit decisions (Spirit 1362-1363) are tracked but out of the schema-stack scope.

## Cross-references

- `reports/designer/458-spirit-triad-naming-gate-decision-2026-06-01.md` — pending psyche ratification (Section 6.1).
- `reports/designer/461-context-maintenance-2026-06-01/` — meta-report; 5 retirements + 3 substance migrations.
- `reports/designer/463-operator-trace-implementation-audit-and-intent-gaps-2026-06-01.md` — audit + four intent gaps (A, B, C, D).
- `reports/operator/275-schema-runtime-instrumentation-log-socket-prototype.md` — instrumentation design substrate.
- `reports/operator/277-spirit-next-testing-trace-implementation-2026-06-01.md` — in-process trace landing.
- `reports/operator/278-gap-vision-and-subagent-implementation-brief-2026-06-01.md` — operator's parallel-converged vision + worker brief.
- `reports/operator/279-actionable-patterns-from-designer-463-2026-06-01.md` — pattern extraction.
- Spirit records 1326-1380 — the captured intent surface this consolidation reviews.
- `skills/architectural-truth-tests.md` §"Proof-of-usage ladder" — the witness discipline.
- `skills/component-triad.md` §"Runtime triad engine traits" — the engine-trait architecture skill landing.
- `skills/designer.md` §"Three-way convergence as correctness signal" — the convergence pattern.
- `skills/rust/methods.md` §"Typestate retires when borrow rules enforce its invariant" — the typestate retirement principle.

## For the orchestrator (chat paraphrase)

Five clusters dominate: (1) engine-trait architecture for Signal/Nexus/SEMA — Maximum, landed in code at `d29dc6c`; trace trait + actor trait layer ratified at Correction Maximum (1365), in flight via parallel operator-on-main + designer-on-worktree. (2) Testing-build verification surface — positive-grep banned Maximum; in-process trace pilot landed; canonical Layer 2 runtime witness substrate; debug wrapper enum + CLI translation + stdout default + Nix differentiated packages in flight. (3) Deploy+Nix shape — last-version package as standard Maximum; no-NOTA-between-components Principle Maximum reaffirmed; Nix component library deferred. (4) Process — designer-on-worktree + operator-on-main + depth-first prototype-proving; cross-pollination methodology for intent-gap filling. (5) Schema-emission rules — rkyv recursive-Box Maximum + closed-sum grouping High + 10-variant sub-division High. Three psyche ratifications pending: 458 naming gate (Option A recommended); 463 gap A (cargo+NOTA stratification — operator 279 framed as "ask psyche to confirm"); 463 gap B (triad placement — same framing). The decision density is high (20+ records in 11 days); architectural direction is coherent and converging.
