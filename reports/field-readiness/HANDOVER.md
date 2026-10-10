# Handover — Finishing the `-next` removal in a clean window (2026-07-04)

Focus-scoped freshness aid, prepared for a LATER isolated session that will
unequivocally finish the engine-wide `-next`→canonical crate-rename removal
(bead `ekvt`) — run only when no other agent is pushing `drop-next`. `-next` is
the sole remaining blocker on the whole-engine gate `w46v`. Other field-readiness
threads are carried lean at the end; they were not advanced this session.

## Settled psyche intent

- Drop `-next` from every `*-next` crate everywhere — repos, dep keys, `use`
  paths — with no alias/compat shim (recorded intent `10pz`: replace, don't keep
  a legacy shape; every consumer updated).
- Nothing lands to any migration repo `main` until an explicit psyche go.
  Producers before consumers.
- Universal tools carry zero project data.
- No `jj` worktree/workspace sprawl; use disposable `drop-next` staging branches.
- The synchronizer's staging-branch name is configurable (delivered this session).

## Tools — done and landed

- Synchronizer (public, `main 57082fa6`, + its own stale `nota-next` dep fixed):
  coordinated cross-branch verify — typed `BaseSelection::StagedCascade` +
  `BranchScheme.staging` (set to `drop-next`) pre-seeds the bump ledger from
  producers' staging tips, so a consumer staged on `drop-next` resolves its
  producers' `drop-next` instead of their un-rewritten `main`; producers without
  a `drop-next` fall back to `main`. Independently audited GO. Mainline path
  unchanged.
- rename-propagator (public, `main 5c2e0ab4`): hardened — now emits an explicit
  `NoStage(Diverged|Unverified)` instead of SILENTLY skipping a repo that has a
  local `jj main*` divergence (the earlier silent skip produced false "all
  clean" claims). Edits-only, zero project data. Guard: `tests/staging_disposition.rs`.
- The 3 GitHub repo renames are live with redirects: `nota` (was nota-next),
  `schema` (was schema-next), `schema-rust` (was schema-rust-next).

## Current staging state (authoritative source = `git ls-remote`, not local refs)

- Producers: `schema` drop-next `a393c8c8`; `schema-rust` drop-next `7f746c02`
  (its `main` advanced to `0eb5be66` by psyche mid-session — rebase drop-next
  onto main before landing); `nota` main `bea7e284`, no drop-next (correct, no
  `-next` to drop).
- Authoritative residue sweep of all 86 run-config repos: ~77 effectively clean
  (zero live `-next`, or `-next` only in authorized literals); the ledger family
  (`repository-ledger`, `signal-repository-ledger`, `meta-signal-repository-ledger`)
  re-fixed on `drop-next`. Remaining live-`-next` tail:
  - `system` and `meta-signal-spirit` — cascade-blocked: their producers
    (`signal-system`/`meta-signal-system`, `signal-spirit`) are still pinned at
    `branch=main`, where `main` still declares the retired `nota-next` package
    key. Clears once every producer is repinned to `drop-next`. (bead `fyxk`)
  - `mind` and `spirit` — peer-held all session, untouched. `mind` has heavy live
    residue (≈8 manifest deps, ≈27 lock entries, live `use nota_next` /
    `extern crate nota_next` in src); `spirit` ≈3 manifest + ≈5 lock deps plus the
    live `NOTA_NEXT_REF` var to rename to its de-`next`ed name — but KEEP the
    `production_migration.rs` boundary-guard `-next` string literal. (bead `fv4l`)
  - A couple of stale-generated-artifact-only repos (regen item, not dep
    residue), incl. `signal-terminal` (peer-dirty).
- `-next` that MUST stay (do not remove): `dependency_boundary` NEGATIVE guards,
  `#[error("nota-next: …")]` strings, nota/schema NOTA test fixtures,
  `synchronizer`/`schema-rust-next` in-repo test data, docs, `tree-sitter-schema`
  grammar fixtures.

## The finish — settled shape (confirmed by this session's runs)

The removal converges with ONE authoritative whole-graph `staged-cascade`
(staging = `drop-next`) that repins EVERY producer to `drop-next` and does a
FULL `cargo generate-lockfile`, run in isolation — then a residue + composed-green
re-audit against authoritative origin — then, on explicit psyche go, land
`drop-next`→`main` producers-before-consumers.

Two confirmed reasons it must be a single isolated full-regen run:
- The synchronizer's INCREMENTAL per-package bumps do not clear `nota-next-derive`
  and cannot converge a consumer whose producer is pinned at `branch=main`. A full
  `cargo generate-lockfile` does. (Proven: a fresh incremental cascade commit
  still carried the residue.)
- Concurrent `staged-cascade` pushes CLOBBER each other's `drop-next` fixes — a
  landed ledger fix was overwritten by a competing re-stage and had to be remade.
  Only one cascade may push `drop-next` at a time; hence the clean window the
  psyche wants.

## Hazards for the finisher

- STALE LOCAL REFS: local `jj`/`git` `origin/drop-next` are diverged from GitHub
  for many repos (local-only rename re-runs under identity `rename@criome.net`
  were never pushed). Establish ground truth via `git ls-remote`, never local
  refs — the one residue false-alarm this session came from a stale local read.
- No migration `main` was touched this session (gate held). Keep it that way
  until the explicit land.
- prometheus cannot fetch UNCACHED private `LiGoldragon/*` git deps directly
  (`ssh prometheus nix build` → "could not read Username for github.com"). Drive
  builds from a credentialed machine with prometheus as REMOTE builder (works).
  Durable fix = provision a GitHub token on prometheus (psyche-scope).
- Excluded by prior decision: `CriomOS-test-cluster` (dirty WIP, bead `nlks`),
  the 2 non-canonical `CriomOS-home` jj worktrees; `synchronizer`/`sema-engine`
  (their tests use the old names as data).

## Verify-first, before the convergence

- Re-read authoritative producer + consumer `drop-next` tips via `git ls-remote`.
- Confirm whether the synchronizer multi-pin fix (for `router`/`signal-spirit`
  `BumpFailed`, several same-name producer entries) landed to synchronizer `main`
  after `57082fa6`. The `r5gr` worker was stopped while looping before it
  confirmed — check the synchronizer `main` log + `R5gr-MultiPin-Evidence.md`. If
  absent, complete it before the cascade, or those two repos will not converge.

## Beads

- `ekvt` (P1, the migration; land psyche-gated) is blocked by: `5kxh`
  (schema-language drift — retired `.schema` syntax fixed + artifacts regenerated
  across 13 consumers; green DoD at convergence), `fyxk` (P1, complete the
  drop-next cascade for `system` + `meta-signal-spirit`), and `fv4l` (de-`next`
  `mind`/`spirit` + composed-green `cloud`). `w46v` depends on `ekvt`.
- `aa2i` (whole-graph checkpoint) is OPEN — its DoD is a re-run to whole-graph
  staged-green + a clean re-audit.
- Closed this session: `177y`/`z2vh` (B harness + audit GO), `glph`/`a2ik`
  (ledger repos de-`next`ed + tool hardening, composed-green), `qipw`/`djb0`/`zy24`
  (artifact regen / `mentci-egui` / guard-test literals). `zohg` (audit-A) closed
  NO-GO (honest not-green + one 2-repo defect it caught, now fixed).
- Open psyche questions: are `mind`/`spirit` free? (the finish waits on them free
  regardless); the land go; whether to provision the prometheus GitHub token.

## Pointers

- Evidence dir `agent-outputs/RenamePropagator/`: `Residue-Sweep-Evidence.md`
  (authoritative ledger + the convergence root cause), `A-Checkpoint-Audit.md`
  (the not-green + gate-held audit), `A-Checkpoint-Evidence.md`,
  `StageAndVerify-Evidence.md` (81-row ledger), `Tier1-Fix-Evidence.md`,
  `Tier2-SchemaDrift-Evidence.md` (+ `-Sweep-` + `Tier2-Regen-*`),
  `Cloud-Stage-Evidence.md`, `B-Harness-Evidence.md`/`-Audit.md`,
  `GroundTruth-BEnablesA.md`, `R5gr-MultiPin-Evidence.md`.
- `github.com/LiGoldragon/synchronizer/ARCHITECTURE.md`.
- Mains: synchronizer `57082fa6` (verify for any r5gr commit on top),
  rename-propagator `5c2e0ab4`, persona `ac629103`.

## Other open field-readiness threads (carried, not advanced this session)

- `w46v`: wire skew resolved earlier; its only remaining blocker is `ekvt`.
- `vp6d` (P1, continuous-testing entry point, separate from `ekvt`) — see
  `reports/field-readiness/02-kink-ledger.md` (+ its 2026-07-03 closeout delta)
  for the READY-WITH-KINKS verdict.
- `dw95` live prometheus redeploy + reachability verify (vehicle `1e6b.2`;
  re-stage a BootOnce from CriomOS `17caaf88`, not the sshd-less gen-50).
- Deferred live activations: ouranos System Switch for nixos-test; ssh Home
  Activate (coordinate with the Colemak change; back up `~/.ssh/config` first);
  orchestrate `systemd --user` cutover (kill the running daemon first).
- Cluster-data rework (after `-next` reaches horizon-rs): switch synchronizer
  builder-resolution to the system-projected `/etc/horizon.json` via horizon-rs
  types, delete the hand-rolled datom decoder, move synchronizer config to
  `persona`, document "cluster data only via horizon/lojix."
- Workspace/bookmark sprawl cleanup in a quiet window (`nlks` sweep of
  `CriomOS-test-cluster`; ~3 stale jj workspaces; 20+ stale `operator/report-*`
  bookmarks).
- Noted follow-ups: migrate synchronizer onto a shared `manifest-surface` crate;
  a NOTA strict-decoder quirk on a slash-bearing content token; `oftl` (horizon-rs
  nixos-test convergence); `wgae` (lojix Home Build with no observable execution).
