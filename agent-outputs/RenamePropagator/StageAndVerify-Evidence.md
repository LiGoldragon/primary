# rename-propagator — stage-and-verify driver evidence (HARD STOP)

Session: RenamePropagator. Driver: General Code Implementer (Claude Opus 4.8,
1M context). Status: STOPPED at step-3 producer verify on a reproducible
build-verify failure whose root cause the reviewed plan did not predict. NO
landing to any `main`. Producers staged to `drop-next`; consumer fan-out NOT
started.

## Task and scope

Drive the mechanical `-next` rename migration onto STAGING branches only:
rename 3 GitHub repos, re-plan against clean tips, apply the tool onto per-repo
`drop-next` branches, per-graph lock-regen + build-verify on the prometheus
builder, fold in 4 manual items, final verify. STOP-and-report on any
build-verify failure or unpredicted surprise.

## Step 1 — GitHub renames: DONE, verified

- `gh repo rename` under `LiGoldragon`: `nota-next`->`nota`,
  `schema-next`->`schema`, `schema-rust-next`->`schema-rust`. All succeeded.
- New names resolve (`gh repo view` OK for `nota`/`schema`/`schema-rust`).
- Old names redirect: `gh api repos/LiGoldragon/<old>` -> new `full_name`.
- Git-level redirect verified over SSH: `git ls-remote ssh://git@github.com/
  LiGoldragon/<old>-next.git HEAD` still resolves (so pinned revs + flake
  inputs at old URLs keep resolving).

## Exclusions (coordinator-authorized) + follow-up bead

Removed from the swept set for this pass (config
`agent-outputs/RenamePropagator/criome-sweep-run.nota`, 3 renamed + 83 swept):

- `CriomOS-test-cluster` — dirty unrelated WIP (nested-microvm reachability
  spike: `clusters/fieldlab.nota`, `fixtures/horizon/atlas.json`, `flake.nix`,
  new `lib/nestedReachability.nix`, `lib/nestedSpike.nix`). Verified it carries
  NO family tokens. Bead filed: **`primary-nlks`** (label `field-readiness`).
- `CriomOS-home-laptop-colemak-merge`, `CriomOS-home-listener-zddv4` —
  non-canonical jj workspaces of `CriomOS-home` (no own `.git`; jj remote =
  `ssh://git@github.com/LiGoldragon/CriomOS-home`; identical bookmark set).
  Canonical `CriomOS-home` stays swept and carries the same 6 edits.

## Step 2 — plan-drift check: PASS

`cargo run --example summarize` (tool at `d4ef1e6`, offline) against current
clean tips:

- ORIGINAL config (89 repos): 2400 edits, 4 flagged pins, 219 residue —
  reproduces the reviewed `DryRunPlan.nota` exactly (NO drift from working-copy
  state since the review, incl. dirty `CriomOS-test-cluster` which has no
  family tokens).
- RUN config (86 repos, 3 exclusions): 2376 edits, 4 flagged pins, 219 residue.
  Delta = exactly the 3 excluded repos (24 format-preserving edits: test-cluster
  12, the two worktree variants 6 each = the same 6 as canonical CriomOS-home),
  0 flagged, 0 residue. Flagged pins (mind 59/70/73/76, exact reviewed revs)
  and residue unchanged. synchronizer correctly absent.

## Step 3 — producer stage + verify: 2 GREEN, 1 FAILED (HARD STOP)

Producer edits applied via a producers-only config
(`scratchpad/producers-only.nota`, swept=[]): nota-next 0 edits, schema-next 5,
schema-rust-next 6 — all clean `nota-next`->`nota` / `schema-next`->`schema`
token rewrites (Cargo.toml deps + Cargo.lock source URLs), rev hashes preserved,
format-preserving. Producer flake.lock/flake.nix carry no family refs (deps come
via Cargo, vendored by `craneLib.vendorCargoDeps`).

Staged to `drop-next` (jj commit as author `rename-propagator
<rename@criome.net>`; `main` bookmark NOT moved in any repo; pushed via redirect):

- `nota`: 0 edits -> no drop-next needed (landing = the GitHub rename; main
  already publishes crate `nota`).
- `schema` drop-next = `ef499e2505180803ed4b849d22a0aa7e9bb95ca1` (pushed).
- `schema-rust` drop-next = `4732e4a3dbe089cde53f603bb1e47cd3803ad0d6` (pushed).

Prometheus builder reachable; private-repo flake fetch + check enumeration
confirmed. Verify (`ssh prometheus nix build '<flake>#packages.x86_64-linux.default'`):

- `nota` (main): **GREEN** -> `/nix/store/7jzyfdxrbpw8l7sfz0lanq5qg4lwsw5f-nota-0.5.1`.
- `schema` (drop-next): **GREEN** -> `/nix/store/dblmyy7lla2w909xrjwn7j6kgn64ia3z-schema-0.2.0`
  (crane vendored `nota` from rewritten `nota.git` lock via redirect — proves
  the textual rewrite is coherent for a leaf-only consumer).
- `schema-rust` (drop-next): **FAILED** — dep derivation
  `schema-rust-deps-0.5.3` failed in `cargo check --release --locked`.

### Root cause of the schema-rust failure (the unpredicted blocker)

The build sandbox has no network; crane pre-vendors from the Cargo.lock. The
failing chain (verbatim from the nix log):

```
failed to get `nota` as a dependency of package
  `schema v0.2.0 (https://github.com/LiGoldragon/schema.git?branch=main#9af2c546)`
  ... which satisfies git dependency `schema` of `schema-rust v0.5.3`
Caused by: unable to update https://github.com/LiGoldragon/nota-next.git?branch=main
Caused by: failed to resolve address for github.com (no network in sandbox)
```

Confirmed: `schema.git` **main** HEAD (`9af2c546`, current) still declares
`nota = { ... git = ".../nota-next.git", branch = "main" }` (Cargo.toml:22,32) —
it was never rewritten, because we correctly do NOT touch `main` this pass.

The mechanism: the tool keeps `branch = "main"` on rewritten deps, so
`schema-rust`'s drop-next references `schema` at **`schema.git?branch=main`**.
`schema-rust`'s own Cargo.lock was rewritten to pull `nota` from `nota.git`, but
`schema@main` (pulled transitively) still declares `nota` from `nota-next.git`.
Under `cargo --locked`, the vendored source map (keyed on `nota.git`) does not
contain `nota-next.git`, so cargo tries to fetch the old URL live and the
no-network sandbox fails. Cargo treats `nota.git` and `nota-next.git` as
DISTINCT sources even though the git remote redirects.

### Why this is a structural blocker, not a one-off

- `nota` (leaf) and `schema` (depends only on the leaf `nota`, whose main is
  self-consistent) build green.
- ANY repo that transitively depends on `schema` or `schema-rust` **at its
  un-rewritten `?branch=main`** will hit the same lock/manifest source conflict.
  That is `schema-rust` itself plus essentially every consumer in the schema /
  schema-rust graphs (mind, spirit, lojix, cloud, router, terminal, most
  signal-*/meta-signal-*, ...). So the consumer fan-out was NOT started — it
  would fail the same way at scale.

The tension the reviewed plan did not predict: staged verification references
producers via `?branch=main`, but the rewrite lives only on `drop-next`, and
`main` is (correctly) never touched this pass. A multi-level producer chain
therefore reintroduces the OLD family URL through the un-rewritten producer main,
breaking `--locked` vendoring in the no-network build sandbox. `nix flake
--override-input` cannot fix this: nota/schema/schema-rust are consumed as CARGO
git deps, not flake inputs, so a flake input override does not repoint them.

## Manual items — analyzed, NOT folded (blocked behind step 3)

- **4a mind pins (4, lines 59/70/73/76):** flagged pins reproduced exactly
  (revs bb4dfe29 / 7105c2be / bb4dfe29 / b3be7d0f). Advancing + building `mind`
  requires a green schema/schema-rust stack first, which is blocked. Note: mind
  line 41 `nota-next` (branch=main) is a normal rewrite, not a flagged pin.
- **4b spirit scripts:** repo-name args at `run-nix-integration-tests:44-46` and
  `check-local-schema-stack:26-28` are the residue to rename (`nota-next`->`nota`
  etc). SURPRISE: the coupled var `NOTA_NEXT_REF` is ALSO used in
  `spirit/tests/nix_integration.rs:268` (`github_source("nota-next",
  "NOTA_NEXT_REF")`) and `spirit/README.md:124` — and the DryRunReview classified
  `nix_integration.rs` as a must-stay guard. So renaming `NOTA_NEXT_REF`->`NOTA_REF`
  is NOT local to the two scripts; needs a coordinator call (see chat).
- **4c generated files:** 39 files carry `@generated by schema-rust-next` on
  disk (2 in excluded rename-propagator), vs the review's "28 stale" — a count
  discrepancy to reconcile. Regeneration needs the schema-rust generator run
  against each consumer's schema inputs, i.e. a working schema-rust — blocked.
- **4d synchronizer nota dep:** `synchronizer/Cargo.toml:21` is still stale
  (`nota = { package = "nota", git = ".../nota-next.git", branch = "main" }`).
  Cleanly scoped (URL-only change). synchronizer is excluded from the sweep and
  is not a drop-next target; needs a placement decision (which branch).

## Staging-branch state (as left)

- `schema` drop-next @ `ef499e25` pushed, verify GREEN. `main` unmoved.
- `schema-rust` drop-next @ `4732e4a3` pushed, verify FAILED. `main` unmoved.
- `nota`: no drop-next (0 edits). `main` unmoved.
- All producer working copies clean (edits committed to drop-next; `@` is an
  empty commit on the drop-next line). No consumer touched. No `main` touched
  anywhere.

## Checks run

- `gh repo rename` x3 + redirect verification (gh api + git ls-remote): PASS.
- `cargo build/run --offline --example {validate,summarize}` (tool `d4ef1e6`):
  PASS; drift check PASS.
- `ssh prometheus nix eval/build`: nota GREEN, schema GREEN, schema-rust FAILED.

## Open questions / recommendation (for coordinator)

The staging-only verify model cannot go green for multi-level producer chains
without one of: (a) rewriting producer `main`s (forbidden this pass); (b) the
tool repointing consumer deps to producer `drop-next` (`branch=main`->
`branch=drop-next`) so staged verifies chain drop-next->drop-next (tool change,
out of my scope); (c) a defined verify that tolerates the old URL via redirect
with network (contradicts `--locked` no-network sandbox + the rewrite). Needs a
coordinator decision before any consumer fan-out.
