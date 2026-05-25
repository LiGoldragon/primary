# 0 — Frame and method

*Orchestrator's frame for the coupled context-maintenance + intent-manifestation sweep dispatched 2026-05-25.*

## What this sweep is

Per psyche directive 2026-05-25, a coupled sweep applying `skills/context-maintenance.md` + `skills/intent-manifestation.md` across four topic domains in parallel. **Predominant move**: migrate substance into INTENT/architecture/skill edits; retire most reports; preserve only the few that carry design-rationale (per `context-maintenance.md` §3a) or serve as live working artifacts.

The user-facing headline deliverable inside this directory is **`1-poc-schema-stack-explainer.md`** — a full "what does it do and how does it work" treatment of the schema-based POC, requested explicitly. The other three subagents are scoped sweeps of NOTA discipline, Spirit v0.2.0 integration, and the designer/ reports soft-cap.

## Division of subagents

| File | Subagent | Scope |
|---|---|---|
| `1-poc-schema-stack-explainer.md` | A | Full explainer of the schema-driven full-stack POC + migrate principles into persona-spirit/INTENT.md, signal-frame/INTENT.md, schema/INTENT.md, signal-persona-spirit/INTENT.md, relevant skills |
| `2-nota-discipline-manifestation.md` | B | Manifest NOTA bracket-string + embedding-safety records (690, 698, 703, 704, 705) into skills/nota-design.md, AGENTS.md hard override, INTENT.md NOTA section |
| `3-spirit-v020-integration-manifestation.md` | C | Manifest /187 + /347 findings into skills/spirit-cli.md, persona-spirit/INTENT.md, INTENT.md spirit-deployment section |
| `4-designer-reports-soft-cap-sweep.md` | D | Triage all reports/designer/ entries; migrate/retire per drop/forward/migrate/keep; produce the sweep table |
| `5-overview.md` | Orchestrator | Synthesize; apply consolidated INTENT.md / AGENTS.md edits proposed by subagents; commit + push |

## Shared-file coordination protocol

Subagents may directly edit files in their own scope (skills they own; per-repo INTENT/ARCHITECTURE). For workspace-shared files where multiple subagents have content to contribute, they **propose edits in their own report's "Proposed shared-file edits" section** rather than applying directly:

- `INTENT.md` (workspace) — A, B, C all propose; orchestrator consolidates in `5-overview.md`
- `AGENTS.md` (workspace) — B owns the NOTA hard-override addition; proposes for orchestrator-application
- `ESSENCE.md` — none proposed unless something rises to the bar; surface to psyche before changing

Per-repo shared files:
- `persona-spirit/INTENT.md` — A owns; C may propose additions
- `persona-spirit/ARCHITECTURE.md` — A owns

## Discipline (HARD RULES for every subagent)

1. **Read `skills/context-maintenance.md` + `skills/intent-manifestation.md` first** — these are the load-bearing disciplines for this sweep.
2. **Use `spirit-v0.2.0`** with the 4-field shape `(Record (<topic> <Kind> [description] <Magnitude>))` if you capture any new intent. **Wrap with shell double quotes**: `spirit-v0.2.0 "(Record (...))"`. NOTA has no `"` inside, so the shell double-quote is the clean outer boundary. Single quotes are wrong; lose apostrophes.
3. **Verbatim-quoting convention**: in INTENT and ESSENCE files, verbatim psyche quotes are in markdown italics inline.
4. **Design-rationale guard (`context-maintenance.md` §3a)**: a report enumerating competing design alternatives stays — add a STATUS-BANNER naming the permanent-doc landing. Standard single-design reports migrate cleanly.
5. **No production code modification.** This sweep is about migrating documentation/intent/skills, not refactoring.
6. **No subagent dispatches of your own.**
7. **No `/nix/store` filesystem search.** Use `nix eval` etc.
8. **`jj` HEADLESS only** — `-m '...'` inline on every description-taking invocation.
9. **Skill files don't reference reports** (per `skill-editor.md`) — once substance is in a skill, the report retires. Don't cite the report from the skill.
10. **Architecture files don't reference reports** (per `architecture-editor.md`) — same rule.
11. **Stay in lane** — designer-assistant scope; don't write into other roles' subdirectories.
12. **Track every worktree you touch** (probably none for this sweep — it's docs and intent, not code).

## Method per subagent

Each subagent's loop:

1. **Read the two source skills + the orchestrator frame** (this file).
2. **Inventory** the topic's substance: Spirit records (`spirit-v0.2.0 "(Observe ...)"`) + the relevant reports.
3. **Decide drop/forward/migrate/keep** per `context-maintenance.md` §2.
4. **Manifest substance** into the right destination per `intent-manifestation.md` §"The decision tree":
   - ESSENCE.md — universal-and-maximum (rare)
   - AGENTS.md — per-keystroke override
   - INTENT.md — onboarding-shaped synthesis
   - `skills/<name>.md` — topic-specific discipline
   - `<repo>/INTENT.md` — project-specific
   - `<repo>/ARCHITECTURE.md` — structural shape
5. **Retire migrated reports** by deleting them with `jj describe -m '...'` (commit message naming the migration target).
6. **Produce your numbered file in `reports/designer/349-context-maintenance-sweep-2026-05-25/`** capturing:
   - What you found
   - What you migrated where
   - What you retired
   - Any proposed shared-file edits for the orchestrator to consolidate

## Subagent A's special remit — the headline explainer

The user explicitly requested a full *"what does it do and how does it work"* report for the schema-based POC. Subagent A's `1-poc-schema-stack-explainer.md` IS that explainer; it's not just a sweep summary. Aim for substantial depth (~600-1000 lines). It should answer:

- What is this POC?
- What problem does it solve?
- What does it do? (capability surface)
- How does it work? (architecture + compile-time pipeline + runtime topology)
- The seven crystallized principles (with concrete examples)
- The six actor schemas in persona-spirit (what each declares)
- The four components: schema crate, schema-rust composer, persona-spirit daemon, signal-persona-spirit dual emission
- The upgrade mechanism (DB-side migration + wire-side projection)
- The actor-schema pattern (ACTION + RESPONSE + universal Unknown)
- The runtime topology (reading actor + logging tap)
- What's verified empirically (the 6 /346 constraints from /105)
- What's still deferred (cross-crate import resolver)
- How does an engineer use this in practice? (worked example)
- Where can they read the code? (file/line pointers)

Mermaid diagrams welcome. Concrete code excerpts where load-bearing. This is the report a fresh agent reads to understand the stack from scratch.

## Subagent A's migration targets (in addition to the explainer)

- `persona-spirit/INTENT.md` — synthesize the actor-schema architecture, the upgrade mechanism, the rkyv-one-format principle, the universal-Unknown safety floor
- `persona-spirit/ARCHITECTURE.md` — the four-component layout + the actor-engine pattern
- `signal-frame/INTENT.md` — the schema-rust composer's responsibility (authored features, not route-derivation)
- `schema/INTENT.md` — the multi-pass parser, finalize_universal_unknowns hook, the three Feature variants
- `signal-persona-spirit/INTENT.md` — the dual emission compatibility approach
- `skills/component-triad.md` — the single-NOTA-argument rule already there; if anything about the schema-driven actor pattern needs to land in a triad-related skill, surface it
- Possible new skill: `skills/schema-driven-actors.md` if the actor-schema pattern warrants its own discipline file. Subagent A makes the call.

Reports A's sweep should consider for migrate-and-retire:
- `/103` schema-driven full-stack initial landing — migrate + retire
- `/104` schema-driven full-stack full implementation — migrate + retire (preserve as commit history)
- `/105` empirical showcase — KEEP as test-witness OR migrate constraint proofs into skill + retire; A decides
- `/341` schema crystallizes architecture — KEEP with STATUS-BANNER (carries competing-design rationale per §2.5 retraction)
- `/343` schema syntax for effect side — migrate + retire (single design, superseded by /345 §8 correction)
- `/345` schemas-as-channel-contracts refresh — migrate + retire (single comprehensive design)
- `/346` actor schemas + upgrade mechanism — migrate + retire (single design; substance into persona-spirit/INTENT.md + ARCH)
- `/347` v0.2.0 integration audit — KEEP as integration-trace OR migrate + retire; A coordinates with C

## Output checkpoint

When all four subagents complete:
- Orchestrator reads each numbered file
- Consolidates proposed shared-file edits into actual edits to INTENT.md / AGENTS.md
- Writes `5-overview.md` synthesizing the sweep
- Commits + pushes everything in one batch

## References

- `skills/context-maintenance.md`
- `skills/intent-manifestation.md`
- `skills/reporting.md` §"Meta-report directories — sub-agent sessions"
- Intent record 231 (meta-report directory mechanism)
- Records 656-705 — the live intent surface this sweep operates on
