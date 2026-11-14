# Plain fixes report — 2026-11-11

## Primary Git push

- Local committed `HEAD` is `ca0b66650192179f9842042910d0374eb0561fce`.
- After `git fetch --no-tags origin main`, `origin/main` is `0f412f00f51fc4cf875e5b7ac2765f96a86ff43a`.
- The histories diverge: one remote-only commit and seven local-only commits; `origin/main` is not an ancestor of `HEAD`.
- The required fast-forward-only `git push --porcelain origin HEAD:refs/heads/main` was rejected as non-fast-forward. No pull, rebase, force, commit, index operation, reset, clean, or stash was performed.

## Beads migration

- Before migration, all Beads/Dolt lock probes succeeded and no active `bd` or `dolt` writer was found. The embedded database was clean at `0jk2ppa2fgct8ujvasvqfc145g5qpi1h`, schema v32, with 545 issues.
- Verified full pre-migration backup: `/home/li/primary/flows/121cc5/beads-pre-migrate-20261111T213857-0600` (286 MiB; 292 regular files; SHA-256 manifest verified; copied database plus `config.yaml` and `metadata.json`; backup database opens cleanly at the original head).
- `bd migrate --force` applied all 34 pending migrations. Current schema migrations are 1 through 66 and current Dolt head is `n72oa8l93fktq0m4tmc88ok2649rpqmr`.
- `bd dolt push` succeeded. A subsequent fetch proves `remotes/origin/main` equals the local migrated head. Push default was therefore `origin`.
- Both configured remotes remain unchanged: `origin = git+ssh://git@github.com/LiGoldragon/primary.git`; `dolthub = https://doltremoteapi.dolthub.com/ligoldragon/primary`.
- Preservation checks: `bd status` and `bd list --all --json` each report 545 issues. Direct before/after counts match: issues 545, dependencies 518, events 2780, comments 71, labels 776, config 10, metadata 4. The Dolt working tree is clean.

## Other clones

- Evidence identifies `/home/li/primary-stale-backup-01e496/tree` as another local clone of the same project with an embedded database and the same two remotes. It must run `bd dolt pull` before upgrading/using the newer `bd` schema.
- `/home/li/worktrees/belief-rename-8d9ef9/primary` carries copied project metadata but no embedded database, so it has nothing to pull.
- Numerous frozen evidence copies carry the same metadata; they are artifacts rather than live database clones. Clones on other hosts are unknown from the evidence available here.

Full command output: `/home/li/primary/flows/121cc5/plain-fixes-evidence.log`.
