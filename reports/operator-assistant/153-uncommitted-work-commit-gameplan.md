# Uncommitted Work Commit Gameplan

## Scope

This report records the operator-assistant audit of uncommitted work on
2026-05-18.

Substance destination: this report retires after the dirty working copies
are either committed, pushed, intentionally abandoned, or moved into a
fresh report/bead that owns the remaining blocker. The durable record then
belongs in the commits, push state, and any closing BEADS notes.

The scan covered:

- `/home/li/primary`
- canonical owned checkouts under `/git/github.com/LiGoldragon/*`
- canonical owned checkouts under `/git/github.com/Criome/*`
- jj worktrees under `~/wt/github.com/LiGoldragon/*/*`
- jj worktrees under `~/wt/github.com/Criome/*/*`

The scan deliberately excluded third-party `ghq` clones. Those are local
dependencies or references, not repositories this workspace should commit
as "our" work by default.

Result: 118 canonical/workspace checkout roots and 20 jj worktree roots were
checked. No status command failed. The initial dirty set was 25 working
copies: 23 canonical/workspace roots plus 2 worktrees.

BEADS note: one `bd ready --label role:operator` read hit the embedded-Dolt
exclusive-lock error; a parallel `bd list --label role:operator --limit 0`
did return the operator queue. Per `skills/beads.md`, this is storage
contention, not coordination ownership.

## Coordination Constraints

Current `tools/orchestrate status` shows `system-assistant` owns
`CriomOS`, `CriomOS-home`, and `lojix-cli` for live
`zeus-audio-debug` work. Those repositories stay out of the
operator-assistant commit queue until that lock clears.

Commit discipline:

- Use `jj` for every Li/Criome repository that has a colocated jj workspace.
- For `orchestrator` and `qmkBinaries`, first claim the repo and run
  `jj git init --colocate`; they are Git-backed Li repos without jj status
  in this scan.
- Read `jj st` immediately before every commit.
- Commit by concern and by owner. Do not sweep unrelated files into a single
  "cleanup" commit.
- Push each logical commit immediately, except where a multi-commit feature
  branch must move as one coherent sequence.

## Dirty Working Copies

| Path | Shape | Immediate commit call |
|---|---|---|
| `/home/li/primary` | Cross-lane report churn: designer-assistant report edits plus operator report deletions. | Do not commit blindly. Let the active designer-assistant lock finish or split only lane-owned files. |
| `/git/github.com/LiGoldragon/CriomOS` | Production deploy surface: docs, Nix checks, modules, `modules/nixos/chroma.nix` deletion. | System-specialist review first; split docs/checks/module behavior. |
| `/git/github.com/LiGoldragon/goldragon` | Production deploy data: `datom.nota`. | System-specialist review with CriomOS/horizon-rs context. |
| `/git/github.com/LiGoldragon/horizon-rs` | Docs/skills change on production-adjacent repo. | Likely one operator/doc commit after checking it matches current production vs lean boundary. |
| `/git/github.com/LiGoldragon/lojix-cli` | `ARCHITECTURE.md` replacement-stack note. | Wait for the active `system-assistant` lock, then commit or fold into the horizon branch-combination pass. |
| `/git/github.com/LiGoldragon/CriomOS-lib` | Canonical checkout is dirty while `@` names `horizon-leaner-shape@git`. | Treat as part of the horizon branch-combination pass. |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-lib/horizon-re-engineering` | `horizon-re-engineering` worktree; `AGENTS.md` edit and deleted `data/largeAI/llm.json`. | Rebase `horizon-leaner-shape` on this branch and combine the changes; do not abandon. |
| `/home/li/wt/github.com/LiGoldragon/goldragon/horizon-re-engineering` | `horizon-re-engineering` worktree; added `secrets/nordvpn-credentials.sops`. | Fold into the combined horizon branch only after verifying the SOPS secret belongs in the merged rewrite. |
| `/git/github.com/LiGoldragon/lore` | New `ARCHITECTURE.md`. | One doc commit, then push main if no peer owns it. |
| `/git/github.com/LiGoldragon/nexus` | `ARCHITECTURE.md` plus `spec/grammar.md`. | Split if grammar changed semantics; otherwise one design-doc/spec commit after review. |
| `/git/github.com/LiGoldragon/nexus-cli` | `ARCHITECTURE.md`. | One doc commit. |
| `/git/github.com/LiGoldragon/sema` | `ARCHITECTURE.md`. | One doc commit. |
| `/git/github.com/LiGoldragon/signal` | `ARCHITECTURE.md`. | One doc commit. |
| `/git/github.com/LiGoldragon/nexus-spec-archive` | `ARCHITECTURE.md` in archived repo. | Commit only if archive docs are intentionally kept current; otherwise consider abandon. |
| `/git/github.com/LiGoldragon/persona-introspect` | Large Rust/runtime/test slice. | High-risk operator slice; inspect diffs, run repo witnesses, then split by behavior/test/doc if needed. |
| `/git/github.com/Criome/mkHorizon` | Nix/flake/TOML changes. | Inspect intent and run the repo's flake check or targeted check before commit. |
| `/git/github.com/LiGoldragon/astro-aski` | Large code/assets/flake/source rename slice. | Needs focused repo pass; likely multiple commits. |
| `/git/github.com/LiGoldragon/aski-cc` | `Cargo.lock` only. | Commit only after identifying whether this is a dependency refresh from a build. |
| `/git/github.com/LiGoldragon/WebPublish` | Added `webpublish.aski`; jj imported Git changes and reset parent to Git HEAD during status. | Inspect branch/bookmarks before commit. |
| `/git/github.com/LiGoldragon/ArtificialIntelligence` | Initial `Readme.md` from empty parent; jj imported Git changes during status. | Done: committed and pushed `main` as `add AI notes readme` (`bfb647cf`). |
| `/git/github.com/LiGoldragon/BookOfLuna` | Initial `Artificial_Intelligence/Intent.md` from empty parent. | Done: committed and pushed `main` as `add Luna AI intent` (`1d612841`). |
| `/git/github.com/LiGoldragon/kibord` | Editor backup-like file `ergodone/coleremak/#keymap.c#`. | Likely do not commit; inspect and either remove intentionally or add ignore rule in a separate commit. |
| `/git/github.com/LiGoldragon/library` | Mixed BEADS metadata, local harness/runtime files, and four Rudhyar texts. | Done for local state: `.gitignore` now ignores agent/runtime harness paths (`ignore local harness state`, `e4ba37fd`). Remaining dirty state is BEADS metadata plus four Rudhyar texts. |
| `/git/github.com/LiGoldragon/orchestrator` | Plain Git repo: `RISK.md`, isolated GC test script. | Initialize colocated jj, inspect, then commit in one or two logical commits. |
| `/git/github.com/LiGoldragon/qmkBinaries` | Plain Git repo: one `.hex` binary changed. | Initialize colocated jj; commit only if this is the intended keyboard artifact. |

## Commit Order

1. Stabilize `primary`.

   `primary` already contains designer-assistant report work and operator
   report deletions. Because another lane holds active locks here, the first
   action is coordination, not a commit. Either wait for the
   designer-assistant session to finish, or split only files owned by the
   acting lane. The operator report deletions appear to belong to an
   operator report-cleanup commit already named on `@`; they should be
   committed by the operator lane or explicitly handed to this
   operator-assistant lane.

2. Combine the horizon branches.

   `horizon-leaner-shape` and `horizon-re-engineering` are the same work now:
   the leaning is the re-engineering. Rebase `horizon-leaner-shape` on the
   `horizon-re-engineering` state repo by repo, then resolve conflicts by
   preserving the combined rewrite intent. The branch-combination pass spans
   at least `CriomOS-lib` and `goldragon`, and likely the rest of the horizon
   rewrite set listed in `protocols/active-repositories.md`.

3. Separate live production fixes from the combined rewrite branch.

   Production edits in canonical `/git` checkouts (`CriomOS`, `goldragon`,
   `horizon-rs`, `lojix-cli`, and possibly `CriomOS-lib`) must still be read
   against the two-stack discipline. The current `system-assistant` lock on
   `CriomOS`, `CriomOS-home`, and `lojix-cli` takes precedence while the live
   audio debug is in progress.

4. Land obvious documentation commits.

   Low-risk doc-only changes can be committed one repo at a time after a quick
   diff read: `lore`, `lojix-cli`, `nexus-cli`, `sema`, `signal`, and likely
   `horizon-rs`. `nexus` needs a slightly closer read because `spec/grammar.md`
   may be semantic, not just architectural prose.

5. Handle high-risk implementation slices with witnesses.

   `persona-introspect`, `CriomOS`, `mkHorizon`, and `astro-aski` need repo
   skill/architecture reads and tests before commits. The shape is not "one
   dirty repo, one commit"; it is "one concern, one commit, with the witness
   named in the commit description."

6. Triage questionable artifacts before committing.

   `kibord` has an editor backup-like file. `library` still has BEADS metadata
   mixed with actual texts. The `goldragon` re-engineering worktree has a SOPS
   secret file that must be verified before it joins the combined horizon
   branch. These should be inspected before any commit, because "commit
   everything" would otherwise preserve accidental local state.

7. Convert plain Git repos to colocated jj before landing.

   `orchestrator` and `qmkBinaries` should be claimed, initialized with
   `jj git init --colocate`, then committed and pushed with normal jj flow.

## Proposed First Batch

The safest first commit batch is:

| Repo | Commit message shape |
|---|---|
| `lore` | `ARCHITECTURE add repo shape` |
| `lojix-cli` | Blocked by active `system-assistant` lock; commit after live audio debug releases it. |
| `nexus-cli` | `ARCHITECTURE clarify command surface` |
| `sema` | `ARCHITECTURE drop stale work reference` |
| `signal` | `ARCHITECTURE sweep signal-core surface` |
| `horizon-rs` | `ARCHITECTURE name sorter boundary` |

Before each commit: read `jj st`, read the diff, commit only that repo's
intended files, set `main` to `@-`, push `main`, and delete any now-stale
`push-*` bookmark only after it is ancestor of `main`.

## User-Attention Items

Decisions from the user are now folded into the plan:

1. Resolved: `horizon-leaner-shape` absorbs `horizon-re-engineering`; all
   changes combine into the same rewrite line.
2. Resolved: `library` local harness/runtime files are ignored, not committed.
3. Resolved: `ArtificialIntelligence` and `BookOfLuna` were dirty and are now
   committed and pushed on `main`.

The remaining user-attention item is the branch-combination execution order:
because `system-assistant` currently owns live production paths, the horizon
branch rebase/combine pass should start from repos outside that lock or wait
until the live audio debug releases them.
