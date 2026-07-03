# B-Harness-Audit — independent audit of the synchronizer cross-branch StagedCascade capability

Session: RenamePropagator. Phase: audit-B (bead `primary-z2vh`, P2). Role: rust
auditor (Claude Opus 4.8, 1M). Date: 2026-07-03. Read-only audit; no source
edited, no branch advanced, no push, `staged-cascade` never run.

## Verdict: GO

The B delta (`synchronizer` `8eec5a46` → `4481a72cc980` → `57082fa6540c`,
`origin/main` = `57082fa6`) is correct, universal, non-regressing, test-guarded,
and its acceptance evidence reproduces independently. Phase A may proceed from
tips **`schema` `a393c8c822cea737d7ed8e823eae7d821ea19bf2`** /
**`schema-rust` `ba6f6df79ccf46225a9a03f0f9724436f9e2330c`**.

No must-fix items. Two low-severity evidence-accuracy notes and three residual
risks for A to carry (below); none blocks the gate.

## Dimension-by-dimension

### 1. Cross-branch cascade correctness — CONFIRMED

The path implements the claim exactly, and it is a *generalization* of the
existing cascade, not a bolt-on. Verified in code:

- `src/driver.rs:388-418` `load_component`: under `StagedCascade` reads
  `remote_staging_tip()`; `Some(tip)` → base = staging tip and the component is
  recorded pre-staged; `None` (no staging branch) → base = `remote_main_tip()`
  and it stays out of the pre-staged set. Under `Mainline` `remote_staging_tip`
  is never called.
- `src/driver.rs:304-311` `execute`: the pre-staged set pre-seeds the cascade
  ledger via `resolver.record_bump(...)`.
- `src/version_resolver.rs:88-98,110-146`: a producer in the ledger resolves to
  `SynchronizerTip`; a `CargoManifest` reference pin is stale iff the target is a
  `SynchronizerTip` and the declared branch ≠ `reachable_branch` (staging); a
  lock pin is stale iff the locked rev ≠ target rev. So a staged producer drives
  BOTH the manifest branch redirect and the lock rev repin; a non-staged
  producer (main-tip target) leaves the manifest branch untouched and only
  repins the lock if its rev drifted.
- `src/driver.rs:681` `apply_bumps`: the commit base is `base_revision()` — i.e.
  the staging tip for a pre-staged component — so the rename-propagator URL
  rewrites already on `drop-next` are preserved and the repin lands on top.

Multi-level set (`nota` leaf → `schema` → `schema-rust`) verified against the
real pushed artifacts (read-only clone of the canonical drop-next tips):

- `schema-rust@ba6f6df7` `Cargo.toml`: `schema = { …/schema.git, branch =
  "drop-next" }`, `nota = { …/nota.git, branch = "main" }`. `Cargo.lock`: schema
  `?branch=drop-next#a393c8c8`, nota `?branch=main#bea7e284`. Coherent manifest
  + lock cross-branch repin, exactly as claimed.
- `schema@a393c8c8` declares `nota` from `nota.git` (both `[dependencies]` and
  dev) and locks `nota.git?branch=main#bea7e284`. No `nota-next` in its
  manifest/lock.

The re-bump composition also holds: `schema-rust@drop-next` pins schema at
`a393c8c8` — schema's **re-bumped** drop-next tip (its stale `nota` lock forced a
re-align off the `ef499e25` pre-seed), not the pre-seed — proving the ledger
overwrite carries through multiple levels.

No-staging fallback (`nota`): `nota.git` has no `drop-next` (ls-remote empty);
`nota` resolved to its main tip, stayed out of the ledger, was `AlreadyAligned`
and not pushed; every consumer left its `nota` pin on `main`/`bea7e284`.

### 2. No regression to the Mainline flow — CONFIRMED

`SynchronizerRun::new` (`src/driver.rs:203`) → `with_boundaries` which defaults
`base_selection: Mainline`; the CLI defaults to `Mainline` for no arg / `mainline`
(`src/main.rs`). Under `Mainline`, `load_component` short-circuits to
`remote_main_tip()` (staging never queried) and the pre-seed loop iterates an
empty set — the pre-B code path with only a tuple-return wrapper added.
`StagedCascade` appears only in `driver.rs` (definition) and `main.rs` (explicit
`staged-cascade` token); it cannot leak into the normal path. The 3 pre-existing
`tests/driver.rs` ascent witnesses and all other Mainline-mode suites pass
unchanged. "Byte-for-byte identical result" is accurate.

### 3. Design quality / universality — CONFIRMED

- Typed variant set, not a flag: `BaseSelection { Mainline, StagedCascade }`
  (`src/driver.rs:150`), decoded from an explicit run-mode token. Matches
  typed-records-over-flags. Neither variant carries a branch name.
- Special case dissolves into the normal case (design-quality): the only new
  logic is (a) read at staging tip where it exists and (b) pre-seed the ledger;
  the cascade rule, pin models, and verify are untouched. The cross-branch
  repin emerges from the *unchanged* ascent.
- Zero project data: **no `drop-next` literal in `src/`** (grep = 0). The
  staging branch name comes from `BranchScheme.staging()`
  (`src/git_repository.rs:174`); the pre-staged set is discovered by staging-
  branch existence. The `nota-next`/`schema-next` strings in `src/` are all
  pre-existing doc comments illustrating the package≠repo case (types.rs:18,
  cargo_manifest.rs:20, driver.rs:876) — none in the B delta, none in logic.
- Typed error boundary: `remote_staging_tip -> Result<Option<CommitIdentifier>,
  Error>`; `error.rs` is a thiserror enum; **no `anyhow`/`eyre` anywhere** in
  `src/` or `Cargo.toml`. `is_full_object_id` (40 hex chars) guards a malformed
  ls-remote token to `None` (safe fallback to mainline).

### 4. Tests guard the capability — CONFIRMED (with a count correction)

`tests/staged_cascade.rs` is a genuine witness, not a trivial pass. It asserts
the schema lock repins to schema's **staging** tip ("not schema@main",
line 259), the manifest redirects `main → drop-next` ("not `synchronizer`",
line 247), the non-staged `nota` pin is **untouched** on main (lines 261-301),
only the consumer is pushed/verified, and it drives `drop-next` (config), never a
baked staging name. It uses `UnreachableLockResolver`, so it also asserts no
transitive fallback fires. This test fails for the most likely shortcut (leaking
the producer's main tip into a staged consumer).

Independent run (`cargo test` in `nix develop`): **45 passed, 0 failed, 1 ignored
(`nix_resolution` stateful probe), across 17 binaries**; `staged_cascade`
passed. `cargo fmt --check` exit 0; `cargo clippy --all-targets` exit 0. The
implementer's "**55 tests**" is an overcount — the true tally is 45 pass + 1
ignored = 46 across 17 binaries. Substance (all green, witness present,
fmt/clippy clean) holds; the count claim is inaccurate.

### 5. Acceptance evidence re-verified, non-mutating — CONFIRMED

- Authoritative remote tips (ls-remote of the **canonical** repos — the local
  `-next` clones point at the old `…-next.git` remotes and stale pre-run
  bookmarks, so they are red herrings): `schema.git` drop-next = `a393c8c8`,
  main = `9af2c546` (untouched); `schema-rust.git` drop-next = `ba6f6df7`, main
  = `6218fb64` (untouched); `nota.git` main = `bea7e284`, drop-next absent.
- `nix build github:LiGoldragon/schema-rust/ba6f6df7…` →
  `/nix/store/7cacgyfhz71j22y5fp2j0zkj94ky3adp-schema-rust-0.5.3` (GREEN, exact
  store path from the evidence). `nix build github:LiGoldragon/schema/a393c8c8…`
  → `/nix/store/3g92a89rz8p97rhykjxkg64vxk2dqm55-schema-0.2.0` (GREEN, exact
  store path). Both fetched from the prometheus cache — reproducible.
- Blocker genuinely gone, not masked: `schema-rust@drop-next` now resolves
  `schema@drop-next` (a393c8c8), and `schema@drop-next` declares/locks `nota`
  from `nota.git` — the whole `schema-rust@drop-next → schema@drop-next →
  nota@main` chain is self-consistent on `nota.git`. The old path
  (`schema@main` still declaring `nota-next`) is bypassed at the root, not
  papered over.

### 6. Tail dep fix (`57082fa6`) — CONFIRMED (with a churn note)

`Cargo.toml:21` and both `Cargo.lock` entries repoint `nota` and transitive
`nota-derive` from `nota-next.git` → `nota.git` at the same rev `bea7e284`; no
`nota-next.git` remains in the manifest/lock. The **34** `nota-next`/`schema-next`
fixture-data strings in `src/`+`tests/` are left untouched (they are the tool's
package≠repo test/doc fixtures, correctly excluded from the sweep). Tests pass
after the fix (nota rebuilt from `nota.git`; clippy shows `nota …/nota.git`).
Undisclosed churn: the same commit also moved `hashbrown 0.17.1 → 0.16.1` (a
transitive lock re-resolution from regeneration) — benign, builds/tests green,
in the tool's own lock only, but not mentioned in the evidence.

## Residual risks (for A to carry; none blocks GO)

1. **Pre-staged-set = every repo with a `drop-next` branch.** The pre-staged set
   is discovered purely by staging-branch existence. Across A's ~86 repos, any
   repo carrying a stray/leftover `drop-next` will be read at that tip and
   cascaded. A should confirm the drop-next set is exactly the intended staged
   set before the whole-graph run.
2. **`main_tips` holds staging tips for pre-staged components under
   StagedCascade** (`src/driver.rs:299-302`, built from `base_revision()`). This
   is currently *safe* because every pre-staged component is also in the ledger
   and therefore always resolves via `SynchronizerTip` (the mislabeled
   `main_tips` entry is shadowed and never read). It is a latent trap: a future
   edit that dropped the pre-seed, or added a code path reading `main_tips` for a
   pre-staged producer, would silently treat a staging tip as a mainline tip. No
   action needed now; flagged for maintainers.
3. **The unit witness does not cover the re-bump composition.** In
   `tests/staged_cascade.rs` the staged producer `schema` is already-aligned and
   stays at its pre-seed tip; the "pre-staged producer re-bumped, consumer picks
   up the new tip" path is proven only by the real-run artifact
   (`schema-rust@ba6f6df7` pinning `schema@a393c8c8`), not by a hermetic test. A
   should treat that path as artifact-covered, not test-covered.

## Checked evidence

- Delta = exactly `4481a72cc980` (B) + `57082fa6540c` (tail); `origin/main` =
  `57082fa6` (pushed). Full code read of both diffs + driver.rs/version_resolver.rs/
  git_repository.rs surrounds.
- `cargo test` (nix develop): 45 pass / 0 fail / 1 ignored / 17 binaries, incl.
  `staged_cascade`. `cargo fmt --check` = 0. `cargo clippy --all-targets` = 0.
- ls-remote of canonical `schema.git`/`schema-rust.git`/`nota.git` (read-only).
- Read-only shallow clones of `schema@drop-next` and `schema-rust@drop-next`;
  inspected committed `Cargo.toml`/`Cargo.lock` pins.
- `nix build` of both reported revs (GREEN, exact store paths, from cache).
- Grep sweeps: no `drop-next`/`anyhow`/`eyre` in `src/`; 34 fixture strings
  preserved; `StagedCascade` confined to driver.rs + main.rs.
