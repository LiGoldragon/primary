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

## 4. Changed files

### synchronizer (public; landed to `main`)

Two commits landed on `github.com/LiGoldragon/synchronizer` `main`
(`8eec5a46` → `4481a72c` → `57082fa6`):

- `4481a72cc980` — the B capability:
  - `src/git_repository.rs` — new `ComponentRepository::remote_staging_tip ->
    Result<Option<CommitIdentifier>, Error>` (staging analogue of
    `remote_main_tip`; empty ls-remote = `None`, absence-is-data) + `GitRepository`
    impl.
  - `src/driver.rs` — `BaseSelection { Mainline, StagedCascade }` typed run mode;
    `SynchronizerRun` carries it (`with_base_selection`, defaults `Mainline`);
    `load_component` selects the base tip per mode and reports the staging tip;
    `execute` collects the pre-staged set and pre-seeds the cascade ledger.
  - `src/main.rs` — optional run-mode arg (`synchronizer <config> [staged-cascade]`).
  - `tests/fixtures/mod.rs` — `standard_config_with_scheme(components, scheme)`
    parameterizes the lone baked branch-scheme literal (was line 43,
    `BranchScheme::new("main","synchronizer")`); `FixtureRepository` gains an
    optional staging tip (`with_staging`) and `remote_staging_tip`;
    `SharedRepository` delegates.
  - `tests/staged_cascade.rs` — new witness of the cross-branch cascade.
- `57082fa6540c` — the tail dep fix: `Cargo.toml`/`Cargo.lock` repoint the real
  `nota` dep (and transitive `nota-derive`) from `nota-next.git` → `nota.git` at
  the same rev `bea7e284`. The 34 `nota-next`/`schema-next` name strings in
  `src/`+`tests/` are fixture data and were deliberately left untouched.

### rename-propagator

No source change needed. Its run config already sets `branch-scheme = (main
drop-next)` (both `config.sample.nota` and the live `criome-sweep-run.nota`), and
its tests already drive `drop-next` as a config parameter (`tests/end_to_end.rs`,
`tests/nota_wire.rs`) — no baked staging literal (the `tests/fixtures/mod.rs:43`
literal named in the brief was the synchronizer's, now parameterized). Making a
change here would violate the smallest-coherent-change and universality rules. The
claim was released unedited.

## 5. Checks run

- `cargo build` / `cargo test` (offline) on synchronizer: **all pass** — 55 tests
  across 17 binaries, incl. the new `tests/staged_cascade.rs` and the unchanged
  ascent/generic/topology/resolver witnesses (no regression). `cargo fmt --check`
  clean; `cargo clippy --all-targets` clean.
- `cargo test` (with `nota.git`) after the tail fix: **all pass** (nota +
  nota-derive recompiled from `nota.git`).

## 6. Acceptance test — schema-rust drop-next GREEN, end to end

Config (scratchpad, not committed): forge `LiGoldragon`, components `nota` /
`schema` / `schema-rust` (AtPath to the old-named local clones), branch scheme
`(main drop-next)`, `DirectHost prometheus`, `DefaultBuild`, author
`rename-propagator`.

Command:

```
synchronizer <config> staged-cascade
```

Run report (`exit 0`, no failures). Branch tips advanced on the tool-owned
staging branch only (no `main` touched anywhere):

| repo | drop-next before | drop-next after | verify |
|---|---|---|---|
| nota | (none; main `bea7e284`) | (none) — `AlreadyAligned`, not pushed | NotAttempted |
| schema | `ef499e25` | `a393c8c822cea737d7ed8e823eae7d821ea19bf2` | **Verified (prometheus)** |
| schema-rust | `4732e4a3` (was FAILED) | `ba6f6df79ccf46225a9a03f0f9724436f9e2330c` | **Verified (prometheus)** |

The cascade repinned schema-rust's `schema` dep `CargoManifest (Reference main) ->
(Reference drop-next)` and `CargoLock 9af2c546 -> a393c8c8`; the `nota` pin
(non-staged producer) was left on `main`/`bea7e284`. Committed content of
`schema-rust@ba6f6df7` verified read-only:

- `Cargo.toml`: `schema = { …/schema.git, branch = "drop-next" }`;
  `nota = { …/nota.git, branch = "main" }`.
- `Cargo.lock`: `schema` `?branch=drop-next#a393c8c8`; `nota`
  `?branch=main#bea7e284`.

Independent re-verification on prometheus (the acceptance proof):

```
nix build github:LiGoldragon/schema-rust/ba6f6df7...
  -> /nix/store/7cacgyfhz71j22y5fp2j0zkj94ky3adp-schema-rust-0.5.3   (GREEN)
nix build github:LiGoldragon/schema/a393c8c8...
  -> /nix/store/3g92a89rz8p97rhykjxkg64vxk2dqm55-schema-0.2.0        (GREEN)
```

`schema-rust`'s drop-next verify — which FAILED before because it fetched
`schema@main` (still declaring `nota-next`) — now resolves `schema@drop-next` and
is GREEN. `schema`'s own drop-next verify is GREEN (no regression). The exact
structural blocker B set out to kill is gone.

## 7. One transparent nuance (flag for audit-B / A)

The run advanced **schema**'s drop-next (`ef499e25` → `a393c8c8`), not merely
`schema-rust`'s. Cause: `schema@drop-next`'s own `nota` lock was stale
(`96e64bcd` vs nota's current `main` tip `bea7e284`), so the cascade re-aligned
it — the tool's normal behavior (a non-staged producer resolves to its mainline
tip). This is within the "staging branch, never main" boundary, keeps the staged
set coherent, and is exactly what a whole-graph green checkpoint (A) wants; but it
is more than a literal read-only touch of the producer's drop-next. The old
`ef499e25` was green in isolation; `a393c8c8` is green against the *current* nota.
Downstream (A / audit-B) should use the new tips above, not the ground-truth
snapshot's `ef499e25` / `4732e4a3`.

## 8. Blockers

None. B is complete and validated: the capability is landed to the synchronizer
`main` (`4481a72c`), the tail dep fix is landed (`57082fa6`), and the acceptance
(schema-rust drop-next GREEN, schema GREEN) is proven end to end on prometheus.
