# Repo Scaffolder — lore INTENT→ARCHITECTURE Fold

## Task and scope

Per-repo doctrine campaign Phase 1, repo `lore` at
`/git/github.com/LiGoldragon/lore` (its own git+jj checkout, own remote;
`/home/li/primary/repos/lore` is a symlink to it). Doctrine: a repo's durable
direction lives in `ARCHITECTURE.md`, not a per-repo `INTENT.md`. lore had no
`ARCHITECTURE.md`, so one was authored from the existing `INTENT.md` direction
and `INTENT.md` was deleted.

## Files and commands consulted

- Read `/git/github.com/LiGoldragon/lore/INTENT.md` (source of durable
  direction), `README.md`, `AGENTS.md` (18 KB canonical cross-workspace agent
  contract — read to understand what lore IS; agent operating rules NOT copied
  into ARCHITECTURE.md).
- Read `/git/github.com/LiGoldragon/spirit/ARCHITECTURE.md` and
  `/git/github.com/LiGoldragon/orchestrate/ARCHITECTURE.md` for sibling house
  style only (Purpose heading, constraints/invariants as bullets, code map).
- `grep -rn "INTENT" --include='*.md'` before and after deletion.
- All VCS via `jj -R /home/li/primary/repos/lore`.

## Observed facts

- Pre-flight verdict re-confirmed: `@` (61cd3652) was empty and directly
  parented on `main` (1d76dea0 "docs use remote nix inputs-from refs"). `main`
  was level with `main@origin`. Clean, no divergence. No `jj new` needed.
- SECRETS scan on INTENT.md: pure direction prose. No passwords, tokens, key
  paths, or secret-adjacent material. Clean.
- Pointer grep before edit found four INTENT hits: two inside INTENT.md itself
  (title + a "what does not live here" bullet naming the workspace intent
  layer), and two in AGENTS.md (lines 13 and 78) that name the
  **workspace-level** intent docs (`ESSENCE.md` / `INTENT.md` / `INTENTION.md`)
  as required reading. None of these is an on-entry pointer to lore's own
  per-repo INTENT.md. README's "See also" does not reference INTENT.md.

## Interpretation

Zero on-entry pointers to lore's own INTENT.md existed outside the file itself,
so zero pointers needed retargeting to ARCHITECTURE.md. The surviving INTENT
references are correct references to the workspace intent layer that genuinely
exists and were preserved unchanged.

## Changed files

- Authored `/git/github.com/LiGoldragon/lore/ARCHITECTURE.md` (new). Carries
  durable direction + structure only: Purpose, "Two halves at one root" (agent
  contract + curated upstream docs, with the subdir layout map), Boundaries
  (what lives here / what does not), Invariants (canonical-shim precedence,
  one-topic-per-file ≤~100 lines, verbatim-over-paraphrase, source/date
  frontmatter, stable-patterns-not-in-flight-work), See also. 100% backed by
  INTENT.md + README.md + AGENTS.md statements; no invented content; no `---`
  horizontal rules.
- Deleted `/git/github.com/LiGoldragon/lore/INTENT.md`.

## Checks run and exact result

- Post-delete re-grep: 3 remaining INTENT matches, all naming the
  workspace-level intent layer (ARCHITECTURE.md:49, AGENTS.md:13, AGENTS.md:78).
  Zero references to lore's own INTENT.md remain.
- `jj status` before commit: `A ARCHITECTURE.md`, `D INTENT.md`, parented on
  main. Whole working copy committed.
- Commit: `3c104b8e` "docs: fold INTENT.md into ARCHITECTURE.md" with the
  required Co-Authored-By trailer.
- `jj bookmark set main -r @-`: moved main to 3c104b8e.
- `jj git push --bookmark main`: fast-forward, main 1d76dea0 → 3c104b8e.
  Accepted, not rejected.
- Post-push log: `main` and `main@origin` converged at 3c104b8e.

## Blockers, unknowns, follow-up

None. Scaffold complete: ARCHITECTURE.md is the on-entry direction surface for
lore; INTENT.md is gone; remote is up to date.
