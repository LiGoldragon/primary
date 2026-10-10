# Upstream identity

Method: probe `gh api repos/tqwewe/kameo/commits/main`, `gh api repos/LiGoldragon/kameo/commits/main`, `gh api repos/LiGoldragon/kameo/compare/3486e4f63ea4e87123476cfbdefeb12403540306...b4aaee797cc3fd12e8194db406d9d73a6bc021ce`, `gh api repos/tqwewe/kameo/compare/4d2e2d02cc1ba59f05123d79f73eb47dd819ef92...main`, `gh api repos/LiGoldragon/kameo/branches/persona-lifecycle-terminal-outcome`

Observed on 2026-08-22, without changing any local repository:

- `tqwewe/kameo` is public, non-archived, default branch `main`; current `main` is `b4aaee797cc3fd12e8194db406d9d73a6bc021ce`, authored and committed 2026-07-21, with subject `chore(deps): update syn requirement from 2.0.52 to 3.0.2 (#383)`.
- `LiGoldragon/kameo` is public, marked as a fork, default branch `main`; current `main` is `3486e4f63ea4e87123476cfbdefeb12403540306`.
- Forge comparison from fork head to upstream head: status `diverged`, `ahead_by=49`, `behind_by=6`, merge base `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92`.
- Forge comparison from merge base to upstream `main`: `ahead_by=49`, `total_commits=49`.
- Forge comparison from merge base to fork `main`: `ahead_by=6`, `total_commits=6`.
- `GET /repos/LiGoldragon/kameo/branches/persona-lifecycle-terminal-outcome` returned HTTP 404 (`Branch not found`). This proves the named branch is absent from the current fork branch listing; it does not prove the locked commit object is unreachable.
- The locked commit `22514f7c6900da00703a4a0ef096f21a45c95a99` remains addressable through the forge commit endpoint and has subject `actor: gate weak shutdown result helpers`.

## Sources

- https://github.com/LiGoldragon/kameo
- https://github.com/tqwewe/kameo
- https://github.com/tqwewe/kameo/compare/4d2e2d02cc1ba59f05123d79f73eb47dd819ef92...main
- https://github.com/LiGoldragon/kameo/compare/3486e4f63ea4e87123476cfbdefeb12403540306...b4aaee797cc3fd12e8194db406d9d73a6bc021ce
- https://github.com/LiGoldragon/kameo/commit/22514f7c6900da00703a4a0ef096f21a45c95a99
