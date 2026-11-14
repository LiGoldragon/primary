# landing.ethos: nothing in Flow uses it; nothing changed

Repository LiGoldragon/flow, main eabddc8d (Flow 0.56.2), crate flow-nexus.

## Finding

`ethos/landing.ethos` describes the approval pipeline: landings, steps, retrainings, refresh-due rows, and the capabilities that read the context repository, deploy a commit, resolve module sources and keep landing rows. No hand-written type or trait in Flow does that job, so there is no twin to replace.

- The pipeline was removed in commit 6e908f68 "Remove automatic approval pipeline" (2026-10-20). It deleted `src/landing.rs` (974 lines), `src/store/landing.rs`, `src/tests/landing.rs`, the `pub mod landing;` line in `src/generated/mod.rs`, and the wiring in `composition.rs`, `context.rs`, `main.rs`, `store.rs`, `waking.rs` and `lib.rs`. It left `ethos/landing.ethos`, `src/generated/landing.rs` and the `"landing"` entry in `build.rs`. That is why the module is not declared: the removal took the declaration out and left the ethos behind.
- A search of crates, tests, flake and checks for every type and trait the ethos names (Landing, LandedChange, ChangedModule, Retraining, RefreshDue, RefreshCause, ModuleSource, LandingOrder, CommitNaming, FlowNaming, RunsLandings, KeepsLandings, ReadsContextRepository, DeploysContext, NamesModule, and the rest) finds them only in `src/generated/landing.rs` and the ethos. The store holds no landing or refresh-due table. The `refresh_due` in `waking.rs` is a local boolean about context thresholds and is unrelated.
- `DESIGN.md` ("The approval pipeline") says the Nexus's place carries no landing watch and no watch runs. `flow-ethos` `LandingWatch` and `Start`'s `Option<LandingWatch>` position still exist, and nothing in Rust reads or builds them.

Adding `pub mod landing;` would only compile dead code: the module carries `#![allow(dead_code)]`, and no caller would move onto it.

## Done

By the brief's last clause I changed nothing. I created worktree `/git/worktrees/flow-landing-565bc8` and branch `landing-565bc8`, then removed both. Nothing was committed, pushed or built, and there is no gate log.

## Decision for the living

Either delete the dead ethos, so the removal is complete, or re-land the pipeline from this ethos.

- Deleting it means removing `ethos/landing.ethos` and `src/generated/landing.rs` and dropping `"landing"` from `build.rs`. It is a small change with no wire or stored-byte effect.
- The same dead-ethos question applies to the `LandingWatch` position in `Start`. Removing it changes the Start datom, so it is a wire change and was not touched.
- I did not check that `landing.rs` compiles if declared.
