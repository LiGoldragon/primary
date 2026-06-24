---
title: 240 - Lojix contained cluster current surface
role: system-operator
variant: Refresh
date: 2026-06-24
topics: [lojix, contained-cluster, deploy-test, context-maintenance]
description: |
  Refresh of the system-operator lojix contained deploy/test cluster report
  stack. Carries forward the current capability, settled design spine,
  evidence, blockers, and next implementation slice; retires the older
  system-operator audits and handoffs that this report absorbs.
---

# 240 - Lojix contained cluster current surface

## Intent Anchors

[Context maintenance is research-driven intent-alignment refresh, not deletion: read intent first to weight currency, review stale reports and live context against current engine, architecture, and intent, and for each item whose abandon/keep/migrate/forward disposition is unclear, ask the psyche one focused intent-alignment question before deciding. Re-research and write the necessary superseding review or handoff that brings substance forward. Output is a small load-bearing current-state set and a clean starting point for the next session, not an accumulating archive.]

[Reports are a small load-bearing set, not an accumulating archive; history lives in jj/git. Context maintenance reduces report count without losing information by agglomerating per topic: multiple reports become one Refresh report (the Capital variant tag after the number) preserving un-contradicted, un-superseded substance in better form; source reports are then deleted with the Refresh report as landing witness.]

## Current Answer

Lojix does not yet deploy test VM clusters.

The current implementation can accept and verify per-node contained runs on the ordinary signal face. The proof-of-concept authoring layer can express a compact criome/spirit/router cluster as client-side expansion into multiple `DeployContained` requests. That is not yet a real cluster coordinator.

The missing piece is `RunContainedCluster` as a daemon-owned ordinary root with a persisted aggregate record, co-live setup, release-all behavior, restart reconciliation, and queryable cluster history. This is a lifecycle coordinator, not a convenience macro.

## Canonical Surfaces

The canonical wide design map is `reports/system-designer/161-state-of-lojix-unified-deploy-test-visual-reassessment-2026-06-21.md`: it settles the one-component two-face design, public verb grammar, authoring layer, wave plan, and the now-settled answers to the earlier operator questions.

This report is the current system-operator surface. It keeps the operator-side proof, runtime blockers, and next implementation slice without requiring future agents to reconcile the older operator stack.

`reports/system-operator/237-lojix-contained-deploy-test-visual-synthesis-2026-06-21.md` stays in the tree for now because system-designer report 161 still names it as the companion proof/debt snapshot. Treat 237 as companion evidence, not as the current system-operator summary.

## Settled Spine

- Lojix is both deploy and test: contained testing is the ordinary face, production deployment is the meta face.
- The ordinary/meta safety boundary is type-real: ordinary builds a `NodeProfile`; meta mutates a `ProductionNode`; codegen keeps those targets separate without a shared target supertype.
- The public ordinary grammar is `DeployContained`, `VerifyContained`, `Release`, plus status through `Query`.
- `CheckContained` dissolves because it conflated "read status" and "execute verification."
- `DeployContainedRequest.source` is authoritative when present, with daemon defaults only as defaults.
- `Release` is always legal and idempotent; failed or unverified runs need cleanup most.
- `TestRun*` storage nouns should become `ContainedRun*` before `VmHostGuest` hardens.
- `RunContainedCluster` belongs as a public ordinary root once the lower roots stop lying about status, source, and release.

## Current Evidence

The `lojix` proof-of-concept branch `system-operator-contained-test-poc` passed:

- `cargo test --test test_op` with 5 passing contained-run tests.
- `cargo test --features nota-text` with the non-ignored unit and integration suites passing.

The `schema-rust-next` wave-0 proof had already passed on the current schema toolchain at commit `e5f33eed`, proving no generated shared target supertype such as `DeployTarget`, `ContainedOrProduction`, or `ProductionOrContained`.

The direct spirit/criome gate witness did not compile far enough to run because the checked-in generated schema artifact in pinned `signal-criome` was stale. That is a dependency freshness blocker, not a lojix cluster proof.

The read-only `CriomOS-test-cluster` structural probe exposed relevant checks, but selected checks failed before cluster assertions because the pinned Rust channel fixed-output hash was stale. That is a flake freshness blocker, not evidence that the cluster contracts fail.

## Current Blockers

1. `RunContainedCluster` and `ClusterRunRecord` are not implemented in `signal-lojix` / `lojix`.
2. `VmHostGuest` is a typed but unavailable substrate; current POC admission rejects non-`HermeticVm` targets as `SubstrateUnavailable`.
3. The real spirit/criome gate witness is blocked by stale generated `signal-criome` artifacts.
4. `CriomOS-test-cluster` checks are blocked by a stale fixed-output Rust channel hash.
5. VM checks still need explicit VM-testing host or builder authority before running.

## Next Slice

The next implementation slice should add `RunContainedCluster` on `HermeticVm` first, proving aggregate lifecycle, co-live semantics, query shape, release-all, and restart reconciliation before `VmHostGuest` execution exists.

That keeps daemon-owned cluster semantics moving without pretending the VM substrate is ready. Once `VmHostGuest` can bring up real NixOS test guests, it becomes another contained substrate under the already-proven aggregate root.

## Retired Sources

This Refresh absorbs and retires these system-operator sources; git history keeps the old reports:

- `reports/system-operator/234-Audit-lojix-unified-deploy-test-review.md` - the `NodeProfile` / `ProductionNode` correction is now folded into system-designer 161 and this report.
- `reports/system-operator/235-Audit-lojix-contained-poc-designer-and-operator-review.md` - the stale `CheckContained`, ignored `source`, direct-store-read, and `TestRun*` findings carry forward here.
- `reports/system-operator/236-lojix-contained-wave0-proof-and-designer-160-audit.md` - wave-0 proof and designer 160 acceptance carry forward here and in system-designer 161.
- `reports/system-operator/238-context-and-worktree-maintenance-2026-06-22.md` - its cluster design insight carries forward here; its worktree inventory was point-in-time state and must be re-run before acting.
- `reports/system-operator/239-lojix-contained-cluster-investigation-and-tests-2026-06-23.md` - latest test results, blockers, and best insight carry forward here.
