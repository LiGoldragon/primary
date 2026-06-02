; designer
[contract-repo signal-interface pipeline-split daemon-imports nexus-sema-local meta-report-frame]
[Meta-report frame for the contract-repository pipeline situation + fork proposal. The psyche directive 2026-06-02: investigate whether contract repositories are part of the next-stack pipeline or have been bypassed; if bypassed, dispatch sub-agent to propose the fork shape across all components from current main HEADs to put Signal interface declaration in the signal-<component> contract repo while keeping Nexus + SEMA local to the daemon. Capture Spirit 1422 Decision Maximum codifies the split. Sub-agent produces the proposal as a sub-report; orchestrator writes the analysis overview after the sub-agent returns.]
2026-06-02
designer

# 475.0 — Frame and method

## The directive

Psyche 2026-06-02: *"So I want to look at how the contract repositories for the next architecture are handled. Are they part of the pipeline or has this all been bypassed for now? And how do we make it happen so that the we split the macro, the interface declaration? ... bring me the situation on that. And if it's not that way, then put a subagent on a proposal from LatestMain on all components that would be forked to accomplish this. And then put his thing in your meta report and then do an analysis overview after."*

## Initial reconnaissance (main agent, before sub-agent dispatch)

**Contract repositories EXIST under `/git/github.com/LiGoldragon/`**:
- `signal-spirit`, `core-signal-spirit`, `owner-signal-persona-spirit` — spirit triad legacy contracts.
- 40+ other contracts across the workspace — `signal-agent`, `signal-cloud`, `signal-introspect`, `signal-mind`, `signal-orchestrate`, `signal-persona`, `signal-router`, `signal-sema`, `signal-upgrade`, ... plus the matching `owner-signal-*` policy contracts.
- `core-signal-spirit` is the legacy `core-` prefix still pending the spirit-triad naming gate ratification (designer 458 Option A `owner-signal-spirit` recommended).

**The next-stack pilot bypasses them**:
- `spirit-next` has its own local schema at `schema/lib.schema` + `schema/lib.asschema` that declares all four planes (Signal Input/Output + NexusInput/Output + SemaWrite/ReadInput/Output) IN THE DAEMON REPO.
- `schema-rust-next` emits the typed Rust code from `spirit-next`'s local schema source — not from any of the contract repos.
- The contract repos themselves DO have `schema/` directories and `build.rs` scaffolding (signal-spirit at least), suggesting an earlier intent to make them the source of Signal types. The next-stack pilot put that intent aside for the rapid-iteration phase.

**Spirit 1422 (Decision Maximum)** codifies the split going forward:
- Signal interface declaration → `signal-<component>` contract repo (clients depend on Signal contract).
- Nexus + SEMA interface declarations → daemon repository (daemon-internal concerns).
- Exception: when a daemon grows a separate scale-out database, the SEMA interface may also extract to a contract repo for the database client.
- The contract repository IS the canonical source for client-facing Signal types.

## The sub-agent's task — `1-fork-proposal.md`

A designer-lane sub-agent will work from current main HEADs across:
- `spirit-next` (daemon) + `signal-spirit` (contract) — the pilot component triad.
- `schema-rust-next` (emitter; not forked but its consumption pattern adapts).
- `schema-next` (schema substrate).
- Optionally other in-flight components if they affect the pipeline.

The sub-agent produces `reports/designer/475-contract-repo-pipeline-situation-and-proposal-2026-06-02/1-fork-proposal.md` with:
- Current state of each affected repo's schema source + emitted code.
- Proposed schema-source split: which planes move where.
- Per-repo fork shape: which branches/changes per repo.
- Build dependency graph: contract repo → daemon imports + schema-rust-next consumption pattern.
- Migration cost estimate: file moves, schema-source edits, build.rs adjustments.
- Edge cases: how does the split interact with the in-flight `IntrospectSocket` (designer 469); how does the typed `ObjectName` from `schema-rust-next` fa3f6153 fit; what happens to `core-signal-spirit` per designer 458.

## The orchestrator's analysis overview — `2-overview.md`

After the sub-agent returns, the orchestrator (main designer) writes `2-overview.md` with:
- Synthesis of the sub-agent's per-repo proposal.
- Connection back to the Spirit 1422 mandate + existing captured intent (Spirit 1326-1336 engine-trait architecture; 1365 trace-as-trait; 1387 schema-drives-most; 1389 slim Nexus; 1419 programmatic triad).
- Recommendations for the operator integration order: which fork lands first, what gates, what risks.
- Decision asks for the psyche: any open shape questions.

## Constraints (sub-agent)

- DESIGN RESEARCH ONLY — no code edits to any repo; no worktree creation; report-only deliverable.
- Bracket NOTA strings only.
- Full English words for all identifiers.
- No `---` horizontal-rule lines.
- Mermaid 5-node cap per Spirit 1282.
- Commit + push the sub-report to primary main; designer-lane authority on `reports/designer/`.
- Report back in under 500 words; full proposal lives in the sub-report.

## Connection to active design surface

- **Designer 458** — spirit-triad naming gate (`core-signal-spirit` → `owner-signal-spirit`). The contract-repo split makes this naming gate more load-bearing since the signal-side and owner-signal-side contracts both become canonical pipeline inputs.
- **Designer 463 gap B** — testing-instrumentation triad placement (trace nouns in signal contract; transport in daemon; policy in owner-signal). Closes naturally if the contract-repo split lands.
- **Designer 466.3 candidate 5** — Output split for slim Nexus + QueryByHandle. Output enum lives on the Signal contract per Spirit 1422 split.
- **Designer 470 top-6** — items 2-6 all build on the schema substrate this proposal touches.
- **Spirit 1419** (operator's Decision High) + **Spirit 1422** (this report's Decision Maximum) — the programmatic-triad + contract-repo-split form a coherent pair for the workspace template.
