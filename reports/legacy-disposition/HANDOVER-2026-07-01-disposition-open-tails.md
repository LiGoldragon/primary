# Handover — Legacy disposition: open tails and settled intent

## Focus
Continue the coverage-gap + `repos/`-deprecation + manifest-rework effort (epic
`primary-6obv`): land the open cross-lane tails and settle the remaining
decisions. The bulk landed this session; what remains is below.

## Settled intent / decisions (this session)
- All repositories live under `/git/github.com/LiGoldragon/<name>`. Residual
  working dirs are removed once their branch is on the remote; if a worktree's
  changes are merged or irrelevant, deleting it is fine. `repos/` is now empty
  and deprecated.
- `protocols/repos-manifest.nota` is the authoritative repo inventory. Coverage
  runs filter `lifecycle = Active` and iterate `/git/...` directly. It
  supersedes `repos/`, `RECENT-REPOSITORIES.md`, and
  `protocols/active-repositories.md`.
- `INTENT.md` is eliminated; a repo's direction lives in `ARCHITECTURE.md` (or
  code). The coverage gap is closed.
- The three-tuple commit-message format in `goldragon`'s `AGENTS.md` is garbage
  and is to be dropped; doctrine follows the plain `goldragon: <summary>`
  practice (`primary-6obv.11`).

## Completed and landed on main
- Coverage: 40 `INTENT.md`->`ARCHITECTURE.md` folds + `y1v5`->`horizon-rs`;
  authored `signal-standard`/`substack-cli`/`goldragon` (on main) and
  `CriomOS-test-cluster` (on a branch, see below).
- Manifest: `protocols/repos-manifest.nota` at `601d6368`, 121 records, refined
  7-field schema (separate `kind` and `lifecycle`, single-source `IsFork`),
  parse PASS; `orchestrate/AGENTS.md` hygiene scan repointed to it.
- `repos/` deprecation complete (symlink index gone, working dirs removed, docs
  reconciled).
- `t5vj` records integrated across `cloud`/`lojix`/`horizon-rs`/`CriomOS`/
  `CriomOS-home`/`goldragon`; secret-leak audit PASS.
- Retired `AnaSeahawk-website`, `persona-pi`, `WebPublish` (remote archived +
  local deleted).
- Stale `~/primary/ESSENCE.md` references repointed to
  `~/primary/ARCHITECTURE.md §"Workspace vision and intent"` (13 repos on main;
  `criome` on a branch, below). `domain-criome` process rule moved to its
  `AGENTS.md`.
- Intent+design audit: PASS-with-fixes; all fixes applied.

## Open — needs landing (cross-lane merges; work is safe on remotes)
- `primary-2f7j` — merge `CriomOS-test-cluster` branch `intent-curator/
  architecture-md` to its main (checkout owned by the `cloud-operator` lane);
  then `jj workspace forget CriomOS-test-cluster-arch`. Until merged, the
  authored `ARCHITECTURE.md` + `INTENT.md` removal are not on that repo's main.
- `primary-t5vj.3` — land `goldragon`'s `cloud-node-data` branch to main
  (untangle the unrelated sops-file-rename divergence) to fully close records
  `5pf6`/`zeqq` at main level.
- `primary-omis` — `cloud` fold content is already on `cloud/main` (fast-
  forwarded); the `cloud` lane need only dispose its `intent-curator-fold`
  worktree and close the bead.
- `primary-bhox` — merge `criome` branch `essence-repoint` (`4749ffb8`) to
  `criome` main (checkout owned by the `assistant` lane).
- `primary-z2xg` — `spirit-guardian-config` WIP was preserved to bookmark
  `spirit-guardian-config-wip-2026-07-01` (`b5f26173`) on the `spirit` remote;
  its lane recovers/reconciles it if wanted.

## Open — decisions and cleanup
- `primary-6obv.11` — drop the `goldragon` three-tuple commit-format doctrine
  (decided; not yet executed). `goldragon` is a jj-only push-immediately data
  repo.
- `primary-6obv.13` (low) — some cited Spirit design-record IDs (`eeeo`/`t312`/
  `dqg3`; mirror's `0yx5`/`rj9y`/`29pb`/`x0ja`) no longer resolve in the live
  daemon; verbatim-match source and consistent with archive rehoming, so not
  fabrication — a traceability note.
- `primary-6obv.14` (low) — the ESSENCE repoint collapsed fine-grained old
  subsection anchors to the single `§"Workspace vision and intent"` anchor; an
  intent-manifestation task only if per-subsection precision is later wanted.
- After `primary-2f7j` merges, bump `CriomOS-test-cluster`'s manifest
  doctrine-home from `None` to `Architecture` (currently correct as `None`).

## Live notes
- Primary's shared working copy has held other lanes' uncommitted work (a skill/
  agent regeneration, a lojix plan); commit the whole working copy only when it
  is quiescent, or land narrow changes via an isolated `main`-based workspace.
- The listener lane's records (`signal-listener`, `meta-signal-listener`,
  `listener`) and `claude-answers` are already on the new-schema manifest.

## Open — pre-existing epic tracks, not addressed this session
`smwa`, `bvsd`, `7wld`, `g28b`, `zpgw`, `e191` remain open under `primary-6obv`.

## Pointers
- Epic `primary-6obv`; final graph `agent-outputs/LegacyDisposition/
  TrackerWeaver-FinalGraph.md`.
- Audit `agent-outputs/CoverageGapReposDeprecation/
  Auditor-IntentAndDesign.md`; secret/coverage audit
  `agent-outputs/CoverageGapReposDeprecation/Auditor-SecretLeakAndCoverage.md`.
- Proposal `reports/legacy-disposition/
  PROPOSAL-2026-07-01-repos-manifest-and-active-set.md`; prior handover
  `reports/legacy-disposition/
  HANDOVER-2026-06-30-coverage-gap-and-repos-deprecation.md`.
