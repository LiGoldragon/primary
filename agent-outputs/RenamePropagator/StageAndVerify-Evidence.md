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

## ADDENDUM — Phase A whole-graph run (2026-07-03, after B landed the harness)

The coordinator decision above was resolved as option (b): B extended the
synchronizer with `staged-cascade`, which repoints a staged consumer's producer
git-deps to the producers' `drop-next` branches during verify. Phase A then
staged the consumers and ran the whole graph. NO migration `main` touched
(verified). Full detail + root-cause taxonomy in `A-Checkpoint-Evidence.md`.

- **80 consumers staged** onto `drop-next` (+ producers `schema a393c8c8`,
  `schema-rust ba6f6df7`). Held out: `mind`/`cloud` (Codex claims), `spirit`
  (uncommitted WIP), `CriomOS`/`CriomOS-home` (NO-CARGO, from verify only).
- One `staged-cascade` over 81 components (~38 min): **40 GREEN, 33 VerifyFailed,
  6 AlreadyAligned, 2 BumpFailed.** Producer `drop-next` after the run:
  `schema a393c8c8`, **`schema-rust 7f746c02`** (re-bumped, GREEN), `nota` none.
- Whole-graph green is **NOT** reached — honest partial. The mechanism is proven
  (40 GREEN incl. `signal-frame`/`triad-runtime` + the full wire layer; every
  cross-source `--locked` blocker resolved). The failures are pre-existing schema
  drift surfaced by rebuilding at schema-rust's current tip (11 retired-syntax +
  6 stale-generated-artifact + 4 cascade), a guard test naming `schema-rust-next`
  (1), a test-compile (1), 9 no-flake false-fails (mechanism correct, verified
  transitively), 1 transient, and the synchronizer multi-pin limit (2). None is a
  rename-migration defect.

### Per-component ledger (drop-next tip after the run · verdict · note)

| repo | drop-next tip | verdict | note |
|---|---|---|---|
| agent | 55d96af59382 | GREEN |  |
| chroma | 68d6678e0a5c | GREEN |  |
| chronos | 2a091f6b65b2 | GREEN |  |
| clavifaber | defd1afc8c2b | GREEN |  |
| criome | dd6c70f5669a | GREEN |  |
| horizon-rs | 33014c71ebec | GREEN |  |
| listener | 767eb72778e7 | GREEN |  |
| mentci-lib | ebedb36ab74d | GREEN |  |
| message | 1c747398fa58 | GREEN |  |
| meta-signal-agent | 5451da7fba07 | GREEN |  |
| meta-signal-criome | 6f8568022b19 | GREEN |  |
| meta-signal-listener | 40f9f2de2a87 | GREEN |  |
| meta-signal-message | 5c13b776298d | GREEN |  |
| meta-signal-router | 47c0da0a9807 | GREEN |  |
| meta-signal-spirit | b05464fd1c5c | GREEN |  |
| meta-signal-terminal | 31cad8912ca7 | GREEN |  |
| meta-signal-version-handover | 72b8d3abeb45 | GREEN |  |
| mirror | 11933f21e07c | GREEN |  |
| nexus | fc700a6414a4 | GREEN |  |
| nota-config | c37627dd8872 | GREEN |  |
| schema-rust | 7f746c020bfb | GREEN | producer re-bump |
| signal | fa82cf9d9ccd | GREEN |  |
| signal-agent | 32f193e27e7e | GREEN |  |
| signal-criome | 91096526fbf2 | GREEN |  |
| signal-frame | 44d22a07e75e | GREEN | universal dep |
| signal-harness | 59015508e5c3 | GREEN |  |
| signal-introspect | 3309f13ccb4c | GREEN |  |
| signal-listener | 714c32084b17 | GREEN |  |
| signal-message | a302b59d8465 | GREEN |  |
| signal-mind | 8187b71959e7 | GREEN |  |
| signal-persona | 9d03892ff886 | GREEN |  |
| signal-repository-ledger | 87495b7802b4 | GREEN |  |
| signal-router | f15c3c5d3b16 | GREEN |  |
| signal-sema | cf95702f489e | GREEN |  |
| signal-standard | 6d17b1189faa | GREEN |  |
| signal-system | 09e3b65c5040 | GREEN |  |
| signal-version-handover | b69077f65259 | GREEN |  |
| skills | c38e464c71bf | GREEN |  |
| terminal-cell | a69fb26ca5bd | GREEN |  |
| triad-runtime | f9a6a7c8ab50 | GREEN |  |
| domain-criome | ee91bbb3f6d2 | VERIFYFAIL | schema-retired-syntax |
| harness | b31e1217734a | VERIFYFAIL | cascade |
| introspect | 01d01bea6d37 | VERIFYFAIL | stale-generated-artifact |
| lojix | a31bb090c1dc | VERIFYFAIL | schema-retired-syntax |
| mentci | dbc2e22a29bf | VERIFYFAIL | no-flake (false-fail) |
| mentci-egui | ee84ae10142e | VERIFYFAIL | fetch-transient (retry) |
| meta-signal-cloud | ab825b7a84c3 | VERIFYFAIL | schema-retired-syntax |
| meta-signal-domain-criome | aaa42dc8e0bb | VERIFYFAIL | schema-retired-syntax |
| meta-signal-introspect | fa163717d7fa | VERIFYFAIL | test-compile |
| meta-signal-lojix | 74a7c71e99c0 | VERIFYFAIL | no-flake (false-fail) |
| meta-signal-mentci | f81a2f94a1b6 | VERIFYFAIL | no-flake (false-fail) |
| meta-signal-mentci-client | d7abb5b0c971 | VERIFYFAIL | no-flake (false-fail) |
| meta-signal-mind | 972117b4304f | VERIFYFAIL | stale-generated-artifact |
| meta-signal-mirror | c1e10ebd6f5c | VERIFYFAIL | no-flake (false-fail) |
| meta-signal-orchestrate | 9b090e5a726b | VERIFYFAIL | stale-generated-artifact |
| meta-signal-persona | a6cdae029641 | VERIFYFAIL | schema-retired-syntax |
| meta-signal-repository-ledger | 12bc96b47609 | VERIFYFAIL | cascade |
| meta-signal-upgrade | 92825f316d8c | VERIFYFAIL | schema-retired-syntax |
| orchestrate | 0f28fda8f195 | VERIFYFAIL | stale-generated-artifact |
| persona | f2149c0e4821 | VERIFYFAIL | schema-retired-syntax |
| repository-ledger | 2e4ef76bec92 | VERIFYFAIL | cascade |
| signal-cloud | c50af8997a62 | VERIFYFAIL | schema-retired-syntax |
| signal-domain-criome | 3aca32823671 | VERIFYFAIL | schema-retired-syntax (root) |
| signal-lojix | 4db768af4a1a | VERIFYFAIL | no-flake (false-fail) |
| signal-mentci | 901a4c309167 | VERIFYFAIL | no-flake (false-fail) |
| signal-mentci-client | d9d14520ea25 | VERIFYFAIL | no-flake (false-fail) |
| signal-mirror | bed619daacd0 | VERIFYFAIL | no-flake (false-fail) |
| signal-orchestrate | d4cb86769773 | VERIFYFAIL | stale-generated-artifact (root) |
| signal-terminal | 729a04a9e396 | VERIFYFAIL | guard-test (schema-rust-next) |
| signal-upgrade | e88082edd099 | VERIFYFAIL | schema-retired-syntax (root) |
| system | f112d19afd8d | VERIFYFAIL | cascade |
| terminal | 064f88e5e39c | VERIFYFAIL | stale-generated-artifact |
| upgrade | e6feb8dc9103 | VERIFYFAIL | schema-retired-syntax |
| router | (rp-tip, not repinned) | BUMPFAIL | multi-pin (signal-criome) |
| signal-spirit | (rp-tip, not repinned) | BUMPFAIL | multi-pin (schema) |
| claude-answers | (rp-tip) | ALIGNED | nota-only, self-consistent |
| meta-signal-harness | (rp-tip) | ALIGNED | no-flake, aligned |
| meta-signal-system | (rp-tip) | ALIGNED | no-flake, aligned |
| nota | (main bea7e284) | ALIGNED | producer |
| schema | a393c8c8 | ALIGNED | producer |
| version-projection | (rp-tip) | ALIGNED | verified GREEN in subset |
