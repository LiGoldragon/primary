---
title: Correction to cloud schema blocker report
role: cloud-operator
date: 2026-06-04
status: current
supersedes: reports/cloud-operator/14-cloud-schema-triad-engine-blocker-2026-06-04.md
---

# Correction to cloud schema blocker report

`reports/cloud-operator/14-cloud-schema-triad-engine-blocker-2026-06-04.md`
was directionally right that the generated cloud schema triad engine is not
complete and that a nested-import resolver bug exists. It was wrong about the
primary blocker and wrong about the state of bead `primary-1tsw`.

## Corrected status

The generated `cloud` triad engine is still not done. The current blocker stack
is not simply "finish the already-claimed `schema-next` multi-plane work." That
work has landed on `schema-next:main` at commit `3f7813cf` (`schema-next: load
multiple schema modules per package`), and the bead is not currently an
operator-owned dirty worktree.

The real stack is:

1. The daemon schemas and contract schemas disagree on type names. Examples:
   `cloud/schema/sema.schema` imports names such as `PlanQuery`, `Validated`,
   `Observed`, and `PlanResult`, while the `signal-cloud:next` schema exposes
   the actual wire vocabulary around `Observe`, `Validate`, `ObservationResult`,
   `ValidationReport`, and `Plan`. This mismatch leads to
   `ImportedTypeNotFound` once files are reachable.
2. The canonical `/git` contract checkouts still carry only
   `*.concept.schema`; the resolvable `lib.schema` and
   `meta-signal-cloud.schema` modules exist on the `next` worktrees. The cloud
   runtime schemas are on canonical `cloud:main`, but their imports reference
   module names that canonical contract checkouts do not yet expose.
3. A canonical-checkout lowering therefore fails before the nested resolver bug
   with missing module files such as `signal-cloud/schema/lib.schema`.
4. The nested resolver bug is real but secondary: `schema-next/src/resolution.rs`
   lowers directly imported modules without threading the caller's resolver
   through nested imports. A `cloud:nexus -> cloud:sema -> signal-cloud` path can
   still produce `UnresolvedImportCrate { crate_name: "signal-cloud" }` after
   the earlier file/name gates are bypassed.
5. Cloud generation wiring is still incomplete: build-time schema discovery and
   per-plane runtime emission need to be wired through `schema-rust-next`'s
   generation driver before generated `NexusRuntime` / `SemaRuntime` code can be
   compiled in `cloud`.
6. The owner contract package name `meta-signal-cloud` is not itself the
   resolver-name problem when registered correctly, but the lack of a separate
   production `meta-signal-cloud` repo remains a deployment gate.

## Replacement next step

Do not use report 14's "finish `primary-1tsw`, then generate" as the plan. The
replacement sequence is:

1. Align cloud daemon schemas with the actual contract schema names, or update
   the contract schemas intentionally.
2. Decide whether cloud generation consumes canonical contract schemas or the
   `next` worktrees, then make the module files present at that surface.
3. Fix the nested resolver path and add a regression test with a dependency
   chain shaped like `nexus -> sema -> third-crate`.
4. Finish the per-crate generation driver and cloud `build.rs` wiring currently
   being worked under `primary-qhi6`.
5. Generate and compile the daemon runtime modules only after the schema inputs
   and resolver path are coherent.

## Current live-state caveat

At the time of this correction, `/git/github.com/LiGoldragon/cloud` has
operator-claimed dirty work under `primary-qhi6` for per-crate schema generation
wiring. This correction intentionally does not touch that repository.
