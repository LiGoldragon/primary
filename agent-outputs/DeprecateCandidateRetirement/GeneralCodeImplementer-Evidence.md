# Deprecate-Candidate Retirement — Reference Scan and Retirement Evidence

## Task and Scope

Psyche-authorized (review gate, proposal §1g) retirement of the three
deprecate-candidate repos under `/git/github.com/LiGoldragon/`:
`AnaSeahawk-website`, `persona-pi`, `WebPublish`. Pattern mirrors the prior
`lojix-cli` / `schema-cc` retirements.

Steps executed: (1) reference scan across all repos under
`/git/github.com/LiGoldragon/` plus the primary workspace, (2) safety-abort
check, (3) clean genuine references, (4) `gh repo archive` each remote,
(5) delete each local clone.

Out of scope (owned by the separate manifest worker, NOT edited):
`protocols/repos-manifest.nota`, `protocols/active-repositories.md`,
`RECENT-REPOSITORIES.md`.

## Files / Commands Consulted

- `gh repo view LiGoldragon/<repo> --json ...` for all three (metadata + archive state).
- `rg -l --hidden -g '!.git'` for `AnaSeahawk`, `persona-pi`, `WebPublish`
  across `/git/github.com/LiGoldragon/` and `/home/li/primary/`.
- `rg -l -g 'flake.lock'` for all three across both trees (dependency signal).
- `ls /home/li/primary/repos/` (symlink surface check).
- Per-repo git state: `git status --short --branch`,
  `git log --branches --not --remotes`, `git stash list`, `git remote -v`,
  `git branch -r --contains HEAD`, `git rev-list --left-right --count`.
- Prior evidence: `reports/legacy-disposition/PROPOSAL-2026-07-01-repos-manifest-and-active-set.md`
  (§1g names exactly these three as the LOW-confidence deprecate-candidate set),
  `agent-outputs/SchemaCcRetirement/GeneralCodeImplementer-Evidence.md` (pattern).

## Observed Facts (reference scan)

Zero flake.lock in either tree references any of the three — the strongest
dependency signal. No `repos/` symlink exists for any of the three. Text hits:

- **AnaSeahawk-website**: only self-reference (`AnaSeahawk-website/_index.md`,
  now deleted). Two hits in `TheBookOfSol` (`.../lunar-nectar-and-breath.md`,
  `.../Plasma_Recycling_Manual.md`) link to `https://github.com/AnaSeahawk/website`
  — a DIFFERENT owner (`AnaSeahawk`, the person), NOT `LiGoldragon/AnaSeahawk-website`.
  The retired repo is a fork of that upstream (`upstream = AnaSeahawk/website`).
  Unrelated; not touched.
- **persona-pi**: self-references only (its own `INTENT.md`, `nix/`,
  `ARCHITECTURE.md`, `flake.nix`). `persona/flake.nix` lines 498/511 use
  `mktemp -d -t persona-pi-router.XXXXXX` / `persona-pi-managed.XXXXXX` — sandbox
  temp-dir NAME PREFIXES for terminal-cell smoke tests (persona + pi-harness
  naming), NOT a flake input. `persona/flake.nix` `inputs {}` block has no
  `persona-pi`. Primary `ARCHITECTURE.md:273` names `persona-pi` as one of three
  parallel naming-convention examples `(persona-codex, persona-pi, persona-claude)`
  — a disambiguation-suffix teaching example (the other two are not repos), not a
  repo dependency.
- **WebPublish**: self-references only (`webpublish.aski`, `readme.md`,
  `webpublish.capnp`, `flake.nix`). No external reference anywhere.
- Primary-workspace hits otherwise land only in `reports/legacy-disposition/`,
  `agent-outputs/` (session artifacts) and the three excluded manifest files.

## Interpretation / Safety Verdict

No genuine dependency reference (import, flake input, path wiring) exists to any
of the three. Every external hit is either unrelated (different owner in
TheBookOfSol), a coincidental temp-dir name prefix (persona flake mktemp), or a
conceptual naming-doctrine example (ARCHITECTURE.md). The zero-edge orphan
finding is confirmed, not contradicted. **Safety abort NOT triggered for any of
the three.**

Nothing to clean: no genuine code/docs/config reference points at these repos as
a dependency. See "Deliberately not edited" for the two judgment calls.

## Git Safety Confirmation (before deletion)

- `AnaSeahawk-website`: on `main`, `0	0` ahead/behind `origin/main`, no stash,
  no untracked. Fully synced.
- `persona-pi`: detached HEAD `fbbdaf70`, contained in `origin/main`; local
  `main` not ahead of remotes; no stash, no untracked.
- `WebPublish`: detached HEAD `e4ffc87`, contained in `origin/main`; local
  `main` not ahead of remotes; no stash, no untracked.

All checked-out commits are on the remote; archiving the remote preserves all
history. No unpushed local work lost by clone deletion.

## Retirement Actions and Per-Repo Result

| Repo | Genuine refs found/cleaned | Safety abort | Remote archived | Local deleted |
|------|----------------------------|--------------|-----------------|---------------|
| AnaSeahawk-website | none (self + unrelated `AnaSeahawk/website` links) | no | yes | yes |
| persona-pi | none (self + mktemp prefix + naming example) | no | yes | yes |
| WebPublish | none (self only) | no | yes | yes |

## Deliberately Not Edited (flagged judgment calls)

- Primary `ARCHITECTURE.md:273` — `persona-pi` appears as a naming-convention
  example alongside non-repos `persona-codex`/`persona-claude`. Retiring the repo
  does not invalidate the naming rule; removing it would break the parallel
  triple. This is vocabulary doctrine, not a repo dependency, and arguably owned
  by intent-manifestation. Left intact; flagged for the manifest worker/psyche if
  they want the vocabulary example refreshed.
- `TheBookOfSol` two files — links point to third-party `AnaSeahawk/website`,
  not the retired LiGoldragon fork. Correct as-is; not touched.
- `persona/flake.nix:498,511` — coincidental temp-dir name prefixes; renaming
  would be unrelated scope creep. Not touched.
- Excluded manifest files (`protocols/repos-manifest.nota`,
  `protocols/active-repositories.md`, `RECENT-REPOSITORIES.md`) — the manifest
  worker will mark the three `Deprecated`. Not touched.

## Checks Run (exact results)

- `gh repo view LiGoldragon/<repo> --json isArchived -q .isArchived` after
  archive -> `true` for all three.
- `rm -rf` each clone then existence probe -> "no (deleted)" for all three.
- Orchestrate: claimed `repo-retire` lane over the three paths, released after.

## Blockers / Unknowns

None. All five steps completed cleanly. No unresolved item requiring escalation
beyond the flagged judgment calls above.
