# 167 — Recent reports and Spirit refresh

*Kind: Refresh · Topic: recent reports + intent logs · Date: 2026-05-24 · Lane: operator*

## Prompt classification

The active turn is a continuation after compaction of a request to read recent reports and intent logs. The continuation text did not contain a new durable psyche Decision, Principle, Correction, Clarification, or Constraint; no new Spirit record was captured in this turn. Prior intent in the thread was already captured where required, especially record 361 for the /310 bead repair and subagent wave.

## Sources refreshed in this pass

Recent Spirit records were observed through record 371. The current late-wave records are 360 through 371:

| Record | Topic | Kind | Operator-relevant summary |
|---|---|---|---|
| 360 | workspace | Decision | Context-maintenance sweep direction for older reports. |
| 361 | operator | Decision | Fix /310 bead dependencies, then work available beads with subagents. |
| 362 | reports | Decision | Aggressive consolidation supersedes conservative context maintenance when psyche directs it. |
| 363 | signal | Correction | Help is at the end of the NOTA path. |
| 364 | signal | Clarification | Help is a noun, not a verb. |
| 365 | signal | Correction | CLI Help examples must obey the single-NOTA-argument rule. |
| 366 | signal-version-migration | Decision | Next-version schema crate is a Cargo dependency of the current schema crate so the macro can emit `VersionProjection`. |
| 367 | signal-macro | Decision | Macro convergence bundles Help docs, 64-bit Tier 1 header, NOTA codec, and next-as-dependency upgrade path. |
| 368 | reporting | Principle | Mermaid node labels should be short visible prose; opaque IDs move outside nodes. |
| 369 | upgrade-component | Decision | Merge sema-upgrade + version-handover into `upgrade`, `signal-upgrade`, `owner-signal-upgrade`; `version-projection` remains separate. |
| 370 | reporting | Principle | Deleted reports live in version-control history and can be read from the commit tree. |
| 371 | component-naming | Decision | Drop the `persona-` prefix from component names except agent-harness components; `persona` itself remains `persona`. |

Recent reports read or refreshed after the previous operator synthesis:

- `reports/designer/316-design-forge-family-current-direction.md`
- `reports/designer/317-sema-upgrade-and-macro-convergence-audit/0-frame-and-method.md` through `4-overview.md`
- `reports/designer/318-upgrade-merger-and-persona-prefix-rename/0-frame-and-method.md`
- `reports/second-designer/162-contract-repo-lens-and-consolidation/4b-consolidated-current-status.md`
- `reports/second-designer/163-signal-sema-interaction-and-spirit-architecture-2026-05-24.md`
- `reports/second-operator/174-review-after-skill-and-intent-refresh-2026-05-24.md`
- `reports/third-designer/25-most-important-questions-2026-05-24/0-frame-and-method.md` through `4-overview.md`

## Assimilated operator state

1. **The macro work is now a single strategic landing, not loose beads.** Spirit record 367 and third-designer /25 converge the macro surface: Help-on-every-enum, Tier 1 micro generation, NOTA codec emission, and next-as-dependency `VersionProjection` belong together on the `signal-frame-macros` extension surface. The live bead store now exposes `primary-ezqx` (consolidated signal_channel/signal_cli macro epic) as the coordinating epic. Standalone work on `primary-v5n2`, `primary-3cl1`, `primary-8r1j`, and `primary-l02o` should be treated as one coordinated implementation unless psyche or designer explicitly splits it.

2. **`primary-li0p` and `primary-avog` are already implemented in `signal-frame`.** Recent reports agree with operator report /165: `NamespaceSection`, `SECTION_CUTOFF = 100`, `classify`, and `assert_triad_sections!` landed. The remaining foundation risk is the frame reshape (`primary-2cjv`) and its sequencing relative to the unified macro PR.

3. **Upgrade merger and mass rename are not ready for operator execution yet.** Designer /318 currently contains only `0-frame-and-method.md`. It frames subreports for rename inventory, rename mechanics, upgrade triad structure, and bead filing, but the subreports and overview were not present when checked. Hold implementation until /318 lands its inventory and bead list, especially because record 371 may rename the new `signal-persona-agent` and `owner-signal-persona-agent` contracts before deeper persona-agent work.

4. **The `upgrade` component direction is settled at intent level.** Record 369 says the triad becomes `upgrade`, `signal-upgrade`, and `owner-signal-upgrade`; `version-projection` stays a library; duplicate migration/handover vocabulary collapses; `AttemptUpgrade` is the surviving flow verb. Component daemons implement only the private handover-protocol subset and return `RequestUnimplemented` for catalogue/flow verbs.

5. **Cloud/domain-criome work has design momentum but open questions.** Third-designer /25 names Phase A contract changes around `MutateSent`/`Mutated`, Phase B runtime/storage, Phase C domain cache, and Phase D authority. Operator should not start Phase A until the Mutate verb shape is confirmed; Phase D is blocked on which component arbitrates node-to-domain authority.

6. **Deploy cutover is system/cluster territory, with operator Rust slices later.** Third-designer /25 carries records 356-358 into an audit shape. The critical operator-adjacent Rust slices are lojix/signal-lojix lock realignment, flake-output split, closure-copy/activation, authorization policy, verb split, typed lowering, and owner-signal-lojix. System-designer decisions on MVP and sandbox criteria precede that wave.

7. **Report retrieval discipline changed.** Record 370 means missing older reports should be sought in version-control history before assuming they are unavailable. This matters during aggressive consolidation: current working tree is the current-state surface, not the only durable archive.

## Immediate operator implications

- Do not broad-commit from `/home/li/primary`; current work remains report-only and the workspace has unrelated lane edits.
- Do not implement the rename/upgrade merger from /318 yet; only the frame exists.
- If asked to continue implementation before /318 finishes, safest operator targets are still bounded code beads already understood from /310 and /317, especially `primary-2cjv` or the coordinated macro epic, but both should be sequenced against the new `primary-ezqx` consolidation framing.
- Re-check `bd ready` before any implementation; the visible ready list has changed since /165 and now includes the consolidated macro epic and additional downstream persona-agent/router/tap beads.
- Treat the two new persona-agent signal repos as local, unpushed, and possibly subject to record-371 rename fallout until Designer resolves /318.
