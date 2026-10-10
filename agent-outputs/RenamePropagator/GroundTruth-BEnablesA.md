# Ground Truth + Bead Graph — "B enables A" (the -next migration staged-green arc)

Session: RenamePropagator. Role: tracker-weaver (read-only verification + authorized
tracker weave). Date: 2026-07-03.

## Task and scope

Phase 0 of the gated `-next` -> canonical crate-rename migration arc (parent bead
`primary-ekvt` P1; `primary-w46v` depends on it). Two jobs:

1. Weave the approved "B enables A" bead graph under the `ekvt`/`w46v` line (tracker
   mutation authorized; nothing advanced past today's truth).
2. Return VERIFIED ground truth (read-only) so downstream B/A workers do not build on
   stale handover claims.

No migration repo was touched; all VCS inspection used `jj --ignore-working-copy`
(no snapshot, no write). No B or A work started.

## Sources consulted

- `reports/field-readiness/HANDOVER.md`
- `agent-outputs/RenamePropagator/{DryRunReview.md, StageAndVerify-Evidence.md,
  criome-sweep.nota, criome-sweep-run.nota}`
- Source (read-only): `/git/github.com/LiGoldragon/{rename-propagator, synchronizer,
  nota-next, schema-next, schema-rust-next}`
- `synchronizer/ARCHITECTURE.md` (via source scout).

## Verified ground truth (observed facts)

### Tool mains

| repo | local dir (old name) | current `main` (full commit id) | short | note |
|---|---|---|---|---|
| rename-propagator | rename-propagator | `d4ef1e69175854bcf4f9db5e652c264c18d11e09` | `d4ef1e69` | matches handover `~d4ef1e69` |
| synchronizer | synchronizer | `8eec5a4669ade3afd4ca88c80b6e5b8b6ba9915a` | `8eec5a46` | matches handover `8eec5a46` |

rename-propagator is **edits-only — CONFIRMED**: `grep 'Command::new'` over the tool
crates = 0; the only filesystem write is `crates/rename-propagator/src/discovery.rs:90`
`std::fs::write(&path, &render.rewritten)` (applying format-preserving rewrites).
`crates/rename-propagator/src/landing.rs` computes landing *order* and holds the staging
`BranchName` as a *plan* (`LandingPlan::assemble(staging: BranchName, ...)`, accessor
`staging()`); its module header (landing.rs:11-13) states the "git commit, force-push to
the staging branch, and the per-graph verify gate are the audited, gated apply phase;
they **reuse the synchronizer's `GitRepository`**." So commit/push/lock-regen/verify are
NOT in the tool — exactly as the handover claims.

### Staging producer `drop-next` branches (the three staged producers)

| producer (local `-next` dir) | `main` (id) | `drop-next` (id) | verify status |
|---|---|---|---|
| nota-next | `bea7e2840ac2cf3e384f07b5c10eeb0890cead25` | **none** (0 edits) | main clean |
| schema-next | `9af2c546f10c9aec5fd6669592aed32f72077df2` | `ef499e2505180803ed4b849d22a0aa7e9bb95ca1` (`ef499e25`) | **GREEN** |
| schema-rust-next | `6218fb64f98c909de1eaa5c35744bd48a97a6f87` | `4732e4a3dbe089cde53f603bb1e47cd3803ad0d6` (`4732e4a3`) | **FAILED** |

- `nota` has no `drop-next` bookmark (0 edits -> none needed); main `bea7e284` already
  publishes crate `nota`. Confirms handover "nota main already clean".
- `schema` drop-next `ef499e25` == handover's `ef499e25` GREEN. **Confirmed.**
- `schema-rust` drop-next `4732e4a3` == handover's `4732e4a3` FAILED. **Confirmed.**
- The GREEN/FAILED verdicts are from `StageAndVerify-Evidence.md` (named evidence). I
  verified the branch tips match those revs exactly (read-only) and did not re-run the
  prometheus builds (that would start work). The `schema-rust` failure root cause per the
  evidence: `schema`@main (`9af2c546`) still declares `nota` from `nota-next.git`, so a
  staged consumer's `--locked` no-network build reintroduces the old family URL — the
  exact structural blocker B fixes. `schema-next` main `9af2c546` confirmed as the current
  main tip here.

### Synchronizer staging-branch surface + stale dep

- **Staging-branch location (CORRECTION — see BLOCKER below):** the staging branch is
  ALREADY a configurable field, not a hardcoded constant:
  - `synchronizer/src/configuration.rs:248-250` — `struct BranchScheme { ... staging:
    BranchName }`; constructor `new()` :254; accessor `staging()` :262-264.
  - Threaded through `src/driver.rs:433` (`PushedBranch::new(...staging().clone(), tip)`)
    and `src/git_repository.rs:285-289` (push refspec built from `staging()`).
  - NOTA config exposes it as `branch-scheme : (<mainline> <staging>)`
    (`ARCHITECTURE.md` §3/§6/§7).
  - The ONLY baked-in literal is the **test fixture** `tests/fixtures/mod.rs:43`
    (`BranchScheme::new(BranchName::new("main"), BranchName::new("synchronizer"))`);
    `tests/driver.rs:536` already drives a different scheme (`trunk`/`bump-train`),
    proving it is a genuine parameter.
  - Verify harness surface (for B's coordinated cross-branch work): stage =
    `driver.rs::SynchronizerRun::process_component` (~:349, push at :624 ->
    `git_repository.rs:284-289`); isolated verify = `build_verify.rs` `Verifier` trait
    (:41) / `BuildVerifier::verify` (:317, runs `nix build` over ssh on the builder).
- **Synchronizer's own stale `nota` dep — CONFIRMED present:** `synchronizer/Cargo.toml:21`
  = `nota = { package = "nota", git = "https://github.com/LiGoldragon/nota-next.git",
  branch = "main" }` — still the old `nota-next.git` URL. Matches handover item 4d.

### Artifacts + run config (all match the handover)

- Present under `agent-outputs/RenamePropagator/`: `DryRunPlan.nota` (421 KB),
  `DryRunReview.md`, `criome-sweep.nota`, `StageAndVerify-Evidence.md` (all four named),
  plus `criome-sweep-run.nota` and `GeneralCodeImplementer-Evidence.md`.
- Run config (`criome-sweep-run.nota` + `StageAndVerify-Evidence.md` step 2): **86 repos**
  (3 producers + 83 swept) of the 89-repo dry-run; **3 authorized exclusions**
  (`CriomOS-test-cluster` dirty WIP -> bead `primary-nlks`; the 2 non-canonical
  `CriomOS-home` jj worktrees `CriomOS-home-laptop-colemak-merge`,
  `CriomOS-home-listener-zddv4`); **~2376 edits**; **4 flagged pins** (all in
  `mind/Cargo.toml` lines 59/70/73/76, revs `bb4dfe29`/`7105c2be`/`bb4dfe29`/`b3be7d0f`);
  **219 residue** hits. All confirm the handover.

## BLOCKER — one divergence from the handover premise

**BLOCKER (scope correction, not a stop-the-weave blocker): the handover/dispatch premise
that "the synchronizer's staging-branch name is currently hardcoded" is FALSE for the
library/binary path.** The staging branch is already a configurable `BranchScheme.staging:
BranchName` field (see above); only the test *fixture* bakes in the literal `"synchronizer"`.

Implication for bead B (recorded in B's description): "make the staging-branch name a
configurable parameter" is **largely already done** — B's staging-parameter work reduces
to *setting* the existing `BranchScheme.staging` to `drop-next` for this run (config, not
code). B's genuinely-new content is the **coordinated cross-branch verify**: resolving a
staged consumer's producer git-deps (which rename-propagator leaves declaring
`branch=main`) against the producers' `drop-next` branches during the isolated no-network
verify, so drop-next verifies chain `drop-next -> drop-next`. Downstream B workers must
scope B around the cross-branch dep-resolution, not around re-parameterizing an
already-configurable field.

No other divergence found: tool mains, the three drop-next tips/statuses, the stale
synchronizer dep, the artifacts, and the run-config totals all match the handover.

## Bead graph laid (authorized weave)

All four new beads OPEN; nothing advanced; `ekvt` status unchanged (a gate note added).

| bead | id | P | role |
|---|---|---|---|
| B | `primary-177y` | P1 | coordinated cross-branch verify harness + drop-next staging parameter |
| audit-B | `primary-z2vh` | P2 | audit of the B harness (gates A) |
| A | `primary-aa2i` | P1 | whole-graph staged-green checkpoint on drop-next + riding-along items |
| audit-A | `primary-zohg` | P2 | audit of A's staged-green run (gates the psyche-go land) |

### Dependency edges (blocker -> blocks)

- `primary-177y` (B) -> `primary-aa2i` (A)   — **hard B-before-A**
- `primary-177y` (B) -> `primary-z2vh` (audit-B)
- `primary-z2vh` (audit-B) -> `primary-aa2i` (A)   — gated arc: audited harness before the checkpoint
- `primary-aa2i` (A) -> `primary-zohg` (audit-A)
- `primary-zohg` (audit-A) -> `primary-ekvt`   — **migration-main gate**: staged-green must be audited before any land
- (pre-existing) `primary-ekvt` -> `primary-w46v`

Full chain: **B -> {audit-B} -> A -> audit-A -> ekvt (land, psyche-gated) -> w46v.**
`bd dep cycles` = no cycles.

### Migration-main gate (the "nothing lands" boundary)

A's scope ENDS at whole-graph GREEN staged on `drop-next` with NOTHING landed. The land to
migration producer/consumer mains is `ekvt`'s own acceptance and is **BLOCKED pending an
explicit psyche go** — recorded as a note on `primary-ekvt` (2026-07-03): a green audit-A
gates but does NOT authorize the land. No bead was advanced this session.

### Riding-along items folded into A's bead (`primary-aa2i`)

- `spirit` `NOTA_NEXT_REF` var rename: rename the live var everywhere (scripts
  `run-nix-integration-tests:44-46`, `check-local-schema-stack:26-28`;
  `tests/nix_integration.rs:268`; `README.md:124`) but KEEP any `-next` string LITERAL that
  is a boundary-migration guard (`dependency_boundary.rs`, the `nix_integration.rs` guard
  assertion).
- Regenerate the stale generated-header files (39 on disk vs review's 28; exclude the 2 in
  rename-propagator) with a regenerate-and-diff drift check.
- Act on the 4 `mind` flagged pins (advance to post-rename revs; verify `mind` builds).
- Honor exclusions: `synchronizer` + `sema-engine` excluded from the sweep (family names
  are fixture data); the 2 non-canonical `CriomOS-home` jj worktrees + dirty
  `CriomOS-test-cluster` excluded.

## Follow-up / unknowns

- B/A verify statuses depend on live prometheus builds; this note carries the recorded
  evidence + matching revs only (no re-run).
- `synchronizer/Cargo.toml:21` stale `nota` dep is a normal on-`main` fix outside the
  sweep; noted in A's description for disposition when B lands (not a `drop-next` target).
