# Flow emission branch rebased onto main 967f2f5

## Result

- `emission-e3a7d1` (7 commits on 40104be, head 86b3bd8) is rebased onto flow main 967f2f5. It is pushed to LiGoldragon/flow as `emission-565bc8`.
- The new head is `e69a3dd6e9216746264d16296e846b9d06771efb`, a fast-forward of main's 967f2f5.
- The worktree is /git/worktrees/flow-emission-565bc8. `emission-e3a7d1` is untouched, and so are main and everything live.
- Every conflict was mechanical. No design choice was needed, and nothing is unresolved.

## Commits

| # | old | new | gate |
|---|---|---|---|
| 1 | 78325571 Herdr's command line | 3bf1b72d | exit 0, 929 passed, 9 ignored (gate-emission-3bf1b72.log) |
| 2 | 61907746 Curriculum query | 7e1ad0a2 | exit 0, 929 passed (gate-emission-7e1ad0a.log) |
| 3 | 36d7542a flow-id claim | 548e42bc | not gated, rebased with no conflict |
| 4 | 33f49d28 harness command line | 301fdde0 | not gated, rebased with no conflict |
| 5 | 86918f05 handover archive Git | 7ef65623 | not gated, rebased with no conflict |
| 6 | 1a38cf56 Herdr socket prompt | 91d9fcf3 | exit 0, 929 passed (gate-emission-91d9fcf.log) |
| 7 | 86b3bd8f pane shell line | e69a3dd6 | exit 0, 929 passed, head (gate-emission-e69a3dd.log) |

All logs are in /home/li/primary/flows/565bc8/. The gates ran with the command given, by revision from github on prometheus, and all four ran in parallel. Each ran the full `checks.x86_64-linux` set. Every gate ended with `flow-nexus: 929 passed, 9 ignored`, the same count the 0.56.0 branch had, so main's removal of the contract copy dropped no tests.

## Conflicts and resolutions

1. **Commit 1, `src/generated/mod.rs`.**
   - Main deleted `pub mod curriculum;`. The branch added `pub mod emission;` beside it.
   - Resolution: keep `pub mod emission;` and drop `curriculum`.
   - `build.rs` auto-merged to main's list (no `curriculum`) plus `emission`.
2. **Commit 2, `src/context.rs`.** There were three hunks.
   - Imports. Main imports from `signal_curriculum_nexus`. The branch imported the generated curriculum types and `CurriculumExchange` and `Emittable`.
     - Resolution: drop the generated-curriculum import and keep `use crate::generated::emission::{CurriculumExchange, Emittable};`.
   - `resolve_module`. Main matches `Ok(CurriculumOutcome::SourcesResolved(..))` on `self.exchange(..)`.
     - Resolution: the branch's shape, `CurriculumQuery::ResolveSources(vec![signal_curriculum_nexus::ModuleIdentity(..)]).emit(self)`, matching `CurriculumExchange::Answered(CurriculumOutcome::SourcesResolved(..))`.
     - The branch's `ResolvedSources` becomes main's `SourcesResolved`.
3. **Commit 2, `src/values.rs`.**
   - The branch's generated-curriculum import was dropped.
   - Main's `use signal_curriculum_nexus::{ContextProvenance, Input as CurriculumQuery, StartupComposition}` lost `Input as CurriculumQuery`, because the `CurriculumQuerying` impls that used it are gone from the branch.
4. **Commit 6, `src/values.rs`.** The import block conflicted between the branch (drops `PaneBound` and `HerdrPaneBinding`) and main's `signal_curriculum_nexus` line. Resolution: the branch's lists, plus main's `use signal_curriculum_nexus::{ContextProvenance, StartupComposition};`.

## Why the emission's shape needed no change

`emission.ethos` imports `flow_nexus:[ CurriculumQuery CurriculumOutcome ]`. Main's `lib.rs` re-exports `signal_curriculum_nexus::{Input as CurriculumQuery, Output as CurriculumOutcome}` under those names, so `Curriculum.CurriculumQuery` and `CurriculumExchange.[ Answered.CurriculumOutcome Unexchanged.String ]` resolve to main's imported types. The `Emittable<CurriculumComposer>` frame exchange in `src/emission.rs` is unchanged.

## Regeneration

- `emission.ethos`, `starter.ethos` and the generated `emission.rs` and `starter.rs` come out of the rebase identical to the branch's.
  - Main did not touch them, and they were not regenerated.
  - ethos-zero stays at the lock's pin. flake.lock changed only through main's own commits, which moved build-base to 9706bad.
- `build.rs`'s freshness check passed in all four gates, since the crate builds with it.
