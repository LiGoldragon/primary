# B — coordinated cross-branch staged verify: design intent + implementation evidence

Session: RenamePropagator. Phase: B (bead `primary-177y`). Role: general code
implementer (Claude Opus 4.8, 1M). Date: 2026-07-03.

Two public/shared Rust tools touched: `LiGoldragon/synchronizer` (the capability)
and `LiGoldragon/rename-propagator` (fixture-scheme parameterization). No migration
producer/consumer `main` is touched. Only the producers' `drop-next` branches are
read; the consumer `schema-rust`'s `drop-next` is advanced to a green repinned tip
(staging, tool-owned).

## 1. The structural problem B must solve (verified)

When rename-propagator stages a consumer on `drop-next`, its token rewrite changes
family URLs (`nota-next.git` → `nota.git`) but keeps `branch = "main"` and does not
repin revisions. So a staged consumer references its producers at
`producer.git?branch=main`, and the producers' `main` is (correctly) never rewritten
this pass. In the no-network build sandbox, crane vendors from `Cargo.lock`; when it
builds `schema-rust@drop-next` it pulls `schema@main` (`9af2c546`), whose manifest
still declares `nota` from `nota-next.git`, conflicting with the vendored `nota.git`
source → cargo tries to fetch `nota-next.git` live → fails. (Verified failing chain
in `StageAndVerify-Evidence.md`.) Flake `--override-input` cannot fix it: the family
crates are consumed as **Cargo git deps**, not flake inputs.

Grounded exact repin (read-only inspection of the real repos):

- `schema-rust@drop-next` (`4732e4a3`) `Cargo.toml`:
  `schema = { package = "schema", git = ".../schema.git", branch = "main" }`;
  `Cargo.lock` `schema` source `...schema.git?branch=main#9af2c546` (version `0.2.0`).
- `nota@drop-next` does not exist (0 edits); `nota` is fine at `main` (`bea7e284`),
  which already publishes crate `nota`. `schema-rust`'s `nota` lock entry
  (`nota.git?branch=main#bea7e284`) already matches `nota`'s current `main` tip.
- `schema@drop-next` (`ef499e25`) publishes `schema 0.2.0` and declares `nota` from
  the rewritten `nota.git` — so it is self-consistent with the vendored `nota.git`.
- Transitive safety: `schema-rust`'s non-dev family producers are only `nota`,
  `schema`, `triad-runtime`; `triad-runtime`'s `nota-next` is behind a non-default
  feature (`default = []`), and `sema-engine`/`signal-frame` are dev-deps — so
  repinning `schema → drop-next` is the sole binding fix (matches the recorded
  root-cause).

The fix: repin `schema-rust@drop-next`'s `schema` dep to
`schema@drop-next` (`ef499e25`), i.e. `branch=main → branch=drop-next` in `Cargo.toml`
and `?branch=main#9af2c546 → ?branch=drop-next#ef499e25` (version `0.2.0`) in
`Cargo.lock`. Then `schema-rust@drop-next → schema@drop-next → nota@main` is
self-consistent and vendors offline.

## 2. Placement decision (which crate gets the resolution, and why)

**The cross-branch producer resolution goes in the synchronizer.** This is a
*cascade*: a consumer must pin a producer at that producer's staging-branch tip
rather than its mainline. The synchronizer already owns exactly this machinery —
the cascade rule (`version_resolver.rs` + `BumpLedger`), the rev-aware pin models
(`cargo_manifest` branch redirect, `cargo_lock`/`flake_lock` rev repin), the
`BranchScheme`, the `GitRepository` commit/push boundary, and the `BuildVerifier`.
rename-propagator is a *sibling* that does identity token-substitution only; its
ARCHITECTURE §1/§7 deliberately delegates commit/push/verify to the synchronizer's
boundaries and refuses rev work ("the tool never recomputes them"). Reimplementing
rev-aware repin in rename-propagator would duplicate the synchronizer's pin models —
the parallel-logic anti-pattern the sibling discipline and role contract forbid.

rename-propagator "drives it" by (a) staging the URL rewrites to `drop-next` (already
done) and (b) the run being configured with `BranchScheme.staging = drop-next` + the
component set. The staged producer set is **discovered** from the forge (a component
whose staging branch exists), never named in code.

**Beauty gate:** the special case (staged cross-branch verify) *dissolves* into the
normal case (cascade ascent). The synchronizer's ascent already: reads each
component's base manifests, resolves each producer edge to a target (mainline tip, or
staging tip when the producer is in the ledger), repins stale pins, commits on the
base, force-pushes the staging branch, and verifies. The only generalization needed
is: the base a component is read/committed at may be its **staging** tip (where that
branch exists) rather than its mainline tip, and the cascade ledger may start
**pre-seeded** with the already-staged producers. With those two generalizations the
existing ascent performs the cross-branch repin unchanged — no new special path.

## 3. The capability (universal, zero project data)

A typed run-mode `BaseSelection` (not a bool flag), added to `SynchronizerRun`:

- `Mainline` — byte-for-byte the existing behavior: read every component at its
  mainline tip; the ledger starts empty.
- `StagedCascade` — read a component at its staging-branch tip where that branch
  exists (its mainline tip otherwise, via a new read-only
  `ComponentRepository::remote_staging_tip -> Option<CommitIdentifier>`), and seed
  the cascade ledger with those existing staging tips.

No branch name, repo name, or producer list is baked in: the staging branch name is
the configured `BranchScheme.staging`; the component set is config; the staged
producer set is discovered (branch existence). The cascade rule, pin models, and
verify are untouched.

(implementation + validation evidence appended below after the run)
