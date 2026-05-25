*Kind: Frame · Topic: full state audit + test-claims verification + problems/solutions/open-questions catalog · Date: 2026-05-25 · Lane: designer*

# 335 · Frame — state audit + test-claims verification

## §1 Psyche directive

> *"Encode back detailed analysis of the main problems with proposed solutions and open questions, and even, if anything, a full sort of overview of the whole state of how we implement things, what's tested, what kind of constraints are tested and how also are they tested. I want to see if agents are actually doing the tests they claim to be doing. So do a full audit and visual representation of the problems with solutions with visuals and code everywhere. You can make this more than one report, obviously."*

Captured as spirit record 574 (workspace/Decision: agent test-claims must be verifiable against actual runnable test files).

## §2 What this meta-report delivers

Three parallel subagent audits + an orchestrator synthesis. Each file in this directory:

| File | Author | Topic |
|---|---|---|
| `0-frame-and-method.md` | designer prime | this file |
| `1-test-claims-verification.md` | subagent A | every report that claims a test ran — find the test file, verify it exercises the claimed behavior, surface mismatches |
| `2-implementation-state-with-visuals.md` | subagent B | per-component + per-layer implementation status, with mermaid diagrams of the upgrade flow, schema engine, the three-socket topology, and the parallel-implementation lane model |
| `3-problems-solutions-open-questions.md` | subagent C | catalog of current load-bearing problems, proposed solutions per problem, open psyche questions per problem, with code snippets and visual decision trees |
| `4-overview.md` | designer prime | synthesis after subagents return; the executive view of where the workspace is + what needs psyche attention |

## §3 Method

Three subagents dispatched in background per spirit record 539 (always-background). Each runs in its own scope, on a non-overlapping reading set:

- **Subagent A** reads recent designer + operator + second-designer + second-operator reports (everything dated 2026-05-24 or 2026-05-25), extracts every test-claim ("this test passes" / "the witness shows X" / "ran end-to-end"), locates the cited test file, runs it (or reads the test source if running isn't tractable), and reports whether the claim matches.

- **Subagent B** walks the implementation state across schema / persona-spirit / signal-persona-spirit / signal-version-handover / upgrade / signal-frame / nota-codec / orchestrate / signal-orchestrate / mind. Produces a per-component + per-layer status table + mermaid diagrams. Layers: schema authoring, schema engine (parse + lower + assemble), brilliant macro library (proc_macro emission), three-socket topology, handover ceremony (marker + mirror + divergence + recovery), version projection, migration driver, supervisor, selector flip.

- **Subagent C** catalogs the load-bearing PROBLEMS named in the reports + on the open beads + in /333-v2 + in /334-v2. For each problem: states the proposed solution (cite the bead or report), states the open psyche questions (cite the section), and produces a code snippet showing what the actual current code looks like for that problem area.

## §4 What is in scope vs not

**In scope**:
- Every test claim in reports dated 2026-05-24 or 2026-05-25
- Implementation state of the schema engine + upgrade mechanism + supervisor + ceremony
- Open beads count + status per the schema/upgrade focus
- Mermaid diagrams (state machines, sequences, dependency graphs)
- Code snippets showing real current code (not aspirational)

**Out of scope**:
- The full workspace history before 2026-05-24 (too broad; that's `intent/*.nota` + earlier reports' territory)
- Per-component INTENT.md content review (just-landed `intent-roll-forward-2026-05-25` branches handled this)
- Net-new design work (this is audit + synthesis, not new direction)

## §5 What the synthesis (file 4) will integrate

After subagents return:

1. Cross-reference: how many test claims actually held; pattern of where claims drifted from reality
2. Per-layer implementation maturity score (wired / typed-only / hand-written / missing) summarized as a heat map
3. Top 5 load-bearing problems ranked by leverage (which one's solution unblocks the most other work)
4. The full set of open psyche questions consolidated, deduplicated, prioritized
5. A single mermaid showing the upgrade-mechanism dependency graph: what blocks what

## §6 References

- `reports/designer/333-upgrade-mechanism-full-design-explained.md` + `333-v2` — the design vision + its corrections from real-world testing
- `reports/designer/334-multi-pass-nota-first-schema-reader.md` + `334-v2` — the schema reader design + the subagent witness corrections
- `reports/designer/330-parallel-implementation-pivot-and-spirit-nspawn-plan.md` — the lane model + nspawn substrate
- `reports/designer/331-spirit-cutover-mvp-proposal.md` — the brief-outage cutover plan
- `reports/designer/332-schema-macro-coverage-audit.md` — what's schema-derived vs hand-written today
- `reports/operator/176-schema-macro-upgrade-integration-audit/5-overview.md` — operator's matching audit
- `reports/operator/178-primary-wdl6-spirit-v0-1-0-protocol-build-2026-05-25.md` — v0.1.0.1 retrofit landing
- `reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md` — second-designer's parallel design with state machines
- `reports/second-operator/185-orchestrate-mirror-handover-implementation-2026-05-25.md` — orchestrate MirrorPayload landing
- Workspace sweep just landed: 9 repos' `intent-roll-forward-2026-05-25` branches
- Spirit records 539, 547, 549, 561-573 (today's intent crystallization)
- Beads: `primary-602y` (wire-compat blocker, P0), `primary-x3ci` (Spirit cutover), `primary-wdl6` (v0.1.0.1 retrofit closed), `primary-a5hu` (persona-daemon supervisor), `primary-ezqx.1` (brilliant macro), `primary-cklr` (UpgradeRule variant), `primary-zfxx` (field-name override), `primary-ekxx` (signal-version-handover pilot), `primary-dlut` (nspawn handover), `primary-axuk` (500-record scale, closed), `primary-db49` (operator mirror, closed), `primary-1jql` (in-transition probe, closing candidate), `primary-xina` (bool alias), `primary-0jjz` (brief-outage cutover execution)
