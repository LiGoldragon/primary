# Fresh Intent And Recent Work Audit

System-operator subagent report, 2026-06-01.

## Scope

I audited the recent production Spirit qualitative-depth work against:

- `reports/system-designer/56-spirit-verbal-depth-scopes-and-frequency-adaptive-search-2026-06-01.md`
- `reports/system-operator/177-spirit-topic-depth-query-implementation-2026-06-01.md`
- Spirit records 1315-1354
- `/git/github.com/LiGoldragon/signal-persona-spirit`
- `/git/github.com/LiGoldragon/persona-spirit`
- `/git/github.com/LiGoldragon/CriomOS-home`
- `skills/spirit-cli.md`

I did not edit code. I only wrote this assigned report.

## Relevant Intent

The load-bearing records for the shipped feature are:

- 1315: Spirit topic retrieval should emphasize recent intent by default while letting quiet topics reach farther back.
- 1316: topic observation should support multi-topic partial and full matching.
- 1317: query ergonomics should use qualitative depth words instead of routine counts or exact time windows.
- 1338: the settled vocabulary is `Shallow`, `Recent`, `Deep`, `VeryDeep`, with target counts `5`, `15`, `30`, `100`; bare `Recent` adopts the explicit count.

The nearby fresh intent that matters for audit discipline is:

- 1325: Spirit-next production-candidate testing must include a production-copy handover test.
- 1340-1342: positive grep is not proof; tests must compile, execute, round-trip, or exercise the real path.
- 1352-1354: operator integration stays on main; designer prototype work continues one proof at a time in worktrees rebased on main.

## What Is Actually Implemented

The production feature is implemented and live.

In `signal-persona-spirit`:

- `RecordedTimeSelection` has `Any`, `Between`, `Since`, `Until`, `Recent`, `Shallow`, `Deep`, and `VeryDeep`.
- The new qualitative variants round-trip in NOTA tests.
- `spirit.schema`, `examples/canonical.nota`, `ARCHITECTURE.md`, `INTENT.md`, and `skills.md` name the new variants.
- Main is at commit `4c7b51ff` (`signal-persona-spirit: add verbal recency depths`).

In `persona-spirit`:

- `RecentRecordSelection` maps `Shallow`, `Recent`, `Deep`, and `VeryDeep` to limits `5`, `15`, `30`, and `100`.
- Filtering happens before qualitative truncation.
- Qualitative results sort newest-first by recorded time and identifier.
- Tests cover store behavior and a daemon/client boundary query.
- `Cargo.lock` pins `signal-persona-spirit` at `4c7b51ff`.
- Main is at commit `df09280a` (`persona-spirit: add verbal recency depth queries`).

In `CriomOS-home`:

- `persona-spirit-v0-3-0` is pinned to `df09280a`.
- `persona-spirit-next` also resolves to the same `persona-spirit` main commit through the lock.
- The unsuffixed production `spirit` command is therefore on the new build.
- `persona-spirit-daemon-v0.3.0.service` and `persona-spirit-daemon-next.service` are active.

In primary skills:

- `skills/spirit-cli.md` documents `Partial` and `Full` topic selection.
- It documents certainty filters, time filters, and the qualitative depth selectors.
- It gives live examples for `Shallow`, `Recent`, `Deep`, and `VeryDeep`.

## Live Behavior Witness

I exercised the production CLI after deployment.

For `Partial [spirit]`, the live result counts were:

- `Shallow`: 5
- `Recent`: 15
- `Deep`: 30
- `VeryDeep`: 78

`VeryDeep` returned 78 because there are only 78 matching records currently in the database, which is the correct bounded behavior under a maximum of 100.

The first identifiers in every qualitative query were newest-first:

- `1317`
- `1316`
- `1315`
- `1252`
- `1251`

The live `Full [spirit query]` query also parsed and returned records, confirming the multi-topic full-match surface is still active.

## Design Match

The implementation matches the core of designer report 56 and record 1338:

- The vocabulary is the chosen `Shallow`, `Recent`, `Deep`, `VeryDeep`.
- The counts are the chosen `5`, `15`, `30`, `100`.
- `Recent` is no longer unbounded; it is capped at 15.
- Query behavior is newest-first fixed-budget selection after other filters.

The implementation is honest about the term "frequency-adaptive": it is fixed result budgets over newest matching records. Quiet topics reach farther back because fewer records match; busy topics stay near the edge because enough recent records match. There is no statistical per-topic density model, no weighted scoring, no Nexus query language, and no semantic keyword expansion.

That is consistent with report 56's simplifying insight and report 177's non-implemented surface.

## Gaps And Risks

### 1. Production-copy handover testing is not satisfied

The feature was tested with Rust unit/integration tests and then live CLI smoke tests against the running production daemon. That satisfies records 1340-1342 better than a grep-only proof.

It does not satisfy record 1325. I found no production-copy handover test for the deployed production candidate: copy a production-like SEMA database, exercise the candidate runtime against the copy, verify existing state is preserved, and verify writes touch only the copy.

This was a small wire/query change with no data migration, so the absence did not show up as a live bug. But record 1325 is explicit for Spirit-next production-candidate testing, and this deployment also updated the `next` slot. The main lane should add this acceptance gate before the next Spirit production-candidate cutover, and ideally add it now while the deployment path is fresh.

### 2. The source design report was retired during the pass

`reports/system-designer/56-spirit-verbal-depth-scopes-and-frequency-adaptive-search-2026-06-01.md` existed when I read it at the beginning of this audit. Later in the same pass it was no longer present under `reports/system-designer/`.

This is not a data-loss issue for the feature because the substance is preserved in:

- Spirit records 1315-1317 and 1338
- `reports/system-operator/177-spirit-topic-depth-query-implementation-2026-06-01.md`
- `skills/spirit-cli.md`
- repo `ARCHITECTURE.md` and `INTENT.md` files

Still, the active task prompt named report 56 directly. The parent lane should treat this as a context-maintenance concurrency wrinkle: retiring reports during an active audit is acceptable only when the successor surface is already clear. Here it is, but the final synthesis should name that successor explicitly.

### 3. Duplicate `178-*` meta-report directories create report-index ambiguity

There are two similarly named system-operator meta-report directories:

- `reports/system-operator/178-context-maintenance-and-recent-audit-2026-06-01/`
- `reports/system-operator/178-context-maintenance-and-recent-work-audit-2026-06-01/`

The active assigned directory is the second one, with `work` in the name. The first one only contained a frame when I checked. This is not a Spirit feature bug, but it is immediate context hygiene: two `178-*` directories make future handoff harder.

The main lane should delete or fold the unused sibling after confirming no live subagent owns it.

### 4. Older human-facing reply cleanup remains intentionally unimplemented

The feature did not address older observation-shape cleanup such as the `DescriptionOnly` compatibility name or historical concern around plural reply wrappers. That is acceptable: records 1063 and 1064 are separate observation-surface cleanup work, not part of the qualitative-depth feature.

The current skill examples use `SummaryOnly`, not `DescriptionOnly`, so agents are not being taught the stale name.

### 5. The current algorithm has no explanation reply

The daemon does not report why a given depth returned a particular count or how far back the selected records reached. For now this is acceptable because the chosen production implementation is fixed-budget retrieval.

If the next design wave adds real density-based search, the reply should expose the selected strategy or effective window so agents can tell whether a quiet topic reached months back or a busy topic stayed within hours.

## Immediate Fix Recommendations

Do now:

- Remove or fold `reports/system-operator/178-context-maintenance-and-recent-audit-2026-06-01/` if no process is writing there.
- In the parent synthesis, state that report 56 has been absorbed by report 177 plus records 1315-1317 and 1338, because the named source file is now absent.

Do next before the next Spirit production-candidate deployment:

- Add a production-copy handover acceptance test per record 1325. It should seed or copy a production-like database, start or exercise the candidate runtime against the copy, verify existing records remain readable, write a test record into the copy, and verify the original database is unchanged.

Do not do now:

- Do not expand this production feature into Nexus scoring or semantic search in-place. That belongs to the next design/prototype wave.
- Do not pretend the current fixed-budget implementation is a full adaptive-statistics engine. It is the simple, useful, deployed version.

## Top Findings

1. Production Spirit qualitative depth is implemented, pinned, deployed, and live. The live CLI returns `Shallow = 5`, `Recent = 15`, `Deep = 30`, and `VeryDeep = all matching up to 100`, newest-first.
2. The only serious missing acceptance gate is record 1325: no production-copy handover test was run or added for Spirit-next production-candidate safety. This should be added before the next Spirit cutover.
3. Context hygiene needs a quick main-lane cleanup: report 56 was retired after being read but is absorbed by report 177 and Spirit records; the unused sibling `178-context-maintenance-and-recent-audit-2026-06-01/` directory should be removed or folded.
