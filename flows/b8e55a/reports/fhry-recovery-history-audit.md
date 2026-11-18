# Audit fhry: Flow recovery-history candidate 0f822a45

Auditor: Mind harnessNexus Opus (b8e55a), for Mind flowNexus Sol, admitted by Core q1ul.
Candidate: flow `0f822a458becf99d2dc5d5880b9aae80c6017e08`, branch `recovery-history-a7785f`, read in /git/worktrees/manual-hold-56ca20/flow.

## Verdict

**Pass, with one stated divergence.** The candidate is a history-only merge. It drops none of the recovery's runtime safety. The recovery's two store tests for the opaque hold families do not carry over to main, and main has no equivalent tests. That is the intended difference between the two (main owns those families, the recovery only tolerated them), not a lost guard.

## Facts checked

- **Parents.** The parents are exactly `1d3f633a` (origin/main at audit time), then `19378d08` (origin `recovery0591-2176a8`, "Release Flow 0.59.1-recovery.1"). Main is the first-parent ancestor, so landing this is a fast-forward.
- **Tree.** The tree is exactly `e1ecb178`, identical to main 1d3f633's tree (`git diff` is empty). No source, generated code, pin or version changes: main stays 0.59.2, and the recovery's 0.59.1-recovery.1 version and its Cargo.lock, Cargo.nix and flake.nix bumps are deliberately not taken.
- **Reachability.** 19378d08 was not reachable from main before; after the candidate it is. Its own branch, recovery0591-2176a8, is still published. The fork point is c0d51dc9, and the recovery carries seven commits from there to 19378d08.
- **Fixtures byte-identical to 19378.** These files have the same blob in main and in 19378: `src/send_tool.rs`, `src/test_faults.rs` and `tests/unit/waking.rs`.
- **Recovery behavior present in main.** I checked each change the recovery made since c0d51dc. Every added line not found literally in main is a comment, an import, or a recovery-only constant or test:
  - `RecognizesInterruptedLaunches` and `LaunchAttemptCarrying` are declared in `ethos/overriding.ethos`, generated, and implemented in `launching.rs:929-950`. They are used in `launching.rs:1332`, which excludes interrupted threads from responder selection, and in `send_tool.rs:1334`.
  - The global Hold guard is in `reconcile_interrupted_launches` (`launching.rs:956`, `if self.held() { return; }`): cleanup of an interrupted launch waits for the owner's Resume. Main adds the per-permaflow holds and the `ResumesPermaflowCleanup`, `ResumesHeldLaunches` and `ResumesPermaflowWork` capabilities beside it.
  - The refused-write fault for Resume and Hold is `RefusedWrite::OverrideTransition`, at `store/overriding.rs:193`.
  - The main tests `persisted_global_hold_defers_interrupted_launch_cleanup_until_owner_resume` (`waking.rs:6061`) and `releasing_one_permaflow_while_global_hold_stands_keeps_its_work_queued` cover the same ground.
- **Families.** Main owns `flow_nexus_permaflow_holds` and `flow_nexus_held_launches` under exactly the family and schema identities the recovery recognized by catalog alone (`flow-nexus-permaflow-holds-v1`, `flow-nexus-held-launches-v1`; `store/overriding.rs:24-26, 444-446`). Main lists them as optional tables of the running schema only.

## Disconfirmation attempted

I placed the recovery's two store tests, `manual_hold_families_are_preserved_unread_while_latest_memory_advances` and `manual_hold_recovery_refuses_wrong_identities_without_changing_memory`, into main's tree and ran them on prometheus with cargo. Both fail:

1. The preservation test fails because main refuses the store with `UnrecognizedMemory`: "family catalog is not a complete authored Flow Memory v3 configuration-only or running schema". The test sets up a configuration-only store carrying the hold families, with opaque bytes in them. Main places those families in the running schema only and decodes their rows itself, so this test is specific to the recovery.
2. The wrong-identity test fails during its own setup. The fixture's engine already holds `flow_nexus_permaflow_holds` under its true identity, so registering it as "foreign" is refused (`FamilyIdentityMismatch`). That refusal is itself the guard the test was written to prove, just reached one step earlier.

What follows: if the recovery binary ever wrote a configuration-only store with hold families, main would refuse to open it. No writer of that shape is known: the recovery only preserves rows it never wrote, and main writes these families in running stores. This is the "feature owns newer families" side of the split, as expected.

## Not done

- No gate run on the candidate SHA (the whole-gate run of the new SHA follows, per the task).
- I did not check whether main's refusal of that configuration-only shape leaves the file unchanged; the recovery test that would show it does not apply to main.
- No main movement and no runtime action.
