# Local repository storage map

## Outcome

The child cleanup removed 32 understood ordinary derived artifacts without
touching source, package caches, boot or rollback state, or uncertain
ownership. This closeout independently probed every reported deletion: all 32
paths are absent. The five explicitly preserved candidates still exist at the
recorded sizes, and the primary working copy is clean.

The closeout `df -P /` probe reported 499,862,036 used and 411,107,460
available 1-KiB blocks (55% capacity). A final post-commit probe reports
499,865,124 used and 411,104,372 available blocks (also 55%). These are
current filesystem observations, not claims that all available space came
from this cleanup; the small change reflects concurrent activity.

## Scan boundary and counting rule

The independent census searched `/home/li`, `/git`, and `/tmp` with
`find -xdev`. `/` is the ext4 filesystem; `/nix/store` is a separate
read-only mount and was not searched. `/boot`, `/run`, `/dev`, `/proc`,
`/sys`, `/dev/shm`, and `/run/user/1001` are separate pseudo, temporary, or
FUSE surfaces and were not traversed. `/root`, `/var`, `/opt`, and network or
portal mounts remain outside the targeted census. Permission-denied examples
included Waydroid data and private `/tmp/nix-*` and
`/tmp/systemd-private-*` trees.

For the raw marker census, one physical parent of a VCS marker is one path;
`.git` and `.jj` on that same parent count once. Nested submodules, linked
worktrees, caches, test fixtures, and transient directories are retained as
physical observations but are not silently promoted to human-owned project
roots. Symlink aliases are reported separately.

## Human-owned congregations

These are observed repository congregations and worktree families, with
containment noted so the rows are not added as though they were disjoint:

| Location | Observed roots | Interpretation |
| --- | ---: | --- |
| `/git` | 595 | 576 under `/git/github.com`, 19 under other forge hosts |
| `/git/github.com/LiGoldragon` | 188 recursive | 182 direct VCS roots, 6 nested historical roots; 184 top-level directories, two unmarked |
| `/home/li/primary/repos` | alias | Resolves to `/git/github.com/LiGoldragon`; not a second copy |
| `/home/li/git-archive` | 132 | Archived Git/Jujutsu roots, including historical components |
| `/home/li/wt` | 72 | Isolated Jujutsu worktrees |
| `/home/li/primary-worktrees` | 4 | Isolated primary worktrees |
| `/home/li/primary-workspaces` | 1 | Isolated primary workspace |
| `/home/li/worktrees` | 2 | External worktrees |
| `/home/li/primary` | 1 | Current primary repository |
| `/home/li/primary/private-repos` | 1 VCS root | Contains `social-media` and incident evidence; preserved |

The active membership authority is `protocols/repos-manifest.dotos`; the
`repos/` symlinks are convenience projections. A congregation is evidenced by
multiple child paths carrying independent VCS markers, not by directory names
alone. For example, `/git/github.com/LiGoldragon` has 182 direct marker roots;
the `primary/repos` symlink has no independent root.

The focused cleanup scan found 238 `/home/li` roots: 35 Git-only, 83
Jujutsu-only, and 120 with both markers. The broader `/git` set found 595
roots: 404 Git-only and 191 with both markers. These are the cleanup worker's
human-facing map, not a claim that every marker under caches is a project.

## Embedded, cache, fixture, and transient markers

The broader independent marker pass found 1,633 `.git` directories, 63
`.git` files, and 440 `.jj` directories. There were 314 Git/Jujutsu overlaps,
yielding 1,822 deduplicated Git/Jujutsu physical marker paths. The additional
recognized marker paths were two Mercurial and one CVS fixture. Fossil and
Pijul each appeared once in Cargo test fixtures. These figures deliberately
must not be added to the human-owned map:

- 59 `.git` marker files are submodule checkouts; three point at linked
  worktrees; one empty marker belongs to a UV source-distribution cache.
- Cargo Git checkout and bare-db trees, Nix `gitv3` and tarball caches, Beads
  embedded Dolt stores, and `.git/modules` stores are tool-owned or embedded
  storage. The bare-store probe found 411 candidates, not 411 independent
  projects.
- `/tmp/claude-1001` contains transient Cargo autodetection fixtures for
  Mercurial, Fossil, and Pijul. The CVS marker is Erlang test data.
- History repositories under `.gemini`, `.gc`, and `.pi` are retained as
  separate history/tool surfaces, not merged into the human-owned forge map.

## Ordinary artifacts and cleanup receipt

The selected ordinary set was 31 Cargo `target/` directories and one empty
Python `__pycache__`, all chosen only after repository-level `Cargo.toml`,
`Cargo.lock`, and `flake.nix` evidence plus clean Jujutsu status. The selected
pre-delete allocated total was **37,930,817,068 bytes** (35.325826 GiB).

Independent absence verification at closeout returned `absent=32` and
`present=0`; the selected post-delete directory total is zero. The child
witness independently measured a filesystem `df` delta of
**38,011,604,992 bytes** (35.401066 GiB). The directory sum is the cleanup
receipt; the filesystem delta includes allocation rounding and concurrent
metadata activity.

The preserved ordinary candidates remain present:

| Path | Bytes | Reason preserved |
| --- | ---: | --- |
| `/git/github.com/LiGoldragon/Curriculum/target` | 2,033,177,042 | Pre-existing target-only dirty state |
| `/git/github.com/LiGoldragon/lojix/target` | 10,644,240,040 | Pre-existing `.beads` dirty state |
| `/git/github.com/LiGoldragon/spirit/target` | 495,431,163 | Pre-existing source edits |
| `/git/github.com/LiGoldragon/spirit-ethos/target` | 120,784 | Source edits and target additions |
| `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/tools/edn_format/__pycache__` | 57,231 | Git-only archive state uninspectable |
| **Total preserved** | **13,173,026,260** | |

Nix `result`, `result-1`, and `result-2` links, `linux-7.1.8`, rollback
evidence, package caches, Node dependency trees, virtual environments, and
source-like `build`, `dist`, and `out` directories were retained. No
deletion failure was reported by the child cleanup (`deleted=32 failures=0`).

## Nix, Lojix, and generated-input retention

The following are attributed to read-only environment-behavior synthesis,
not independently re-probed in this closeout:

- The Nix daemon is sandboxed, configured with max-jobs 1 and two cores,
  retains derivations and outputs, and enables auto-optimise-store. A
  Prometheus builder/cache and `cache.nixos.org` participate in the build
  path. The Nix store shares the ext4 device with `/home` and `/git`.
- Lojix generated inputs live at `/var/lib/lojix/generated-inputs` with 12
  shape roots. Live retention includes system/Home profiles and 181 automatic
  GC roots; no Nix GC timer was observed. Tmpfiles ages builds at 7 days,
  `/tmp` at 10 days, and `/var/tmp` at 30 days.
- Lojix's Sema models `Current`, `BootPending`, `Rollback`, `Pinned`, and
  `Recent`, with `PathInfoGc`; the intended
  `/nix/var/nix/gcroots/criomos` tree was absent. Whether another live root
  surface supplies equivalent protection is unresolved.

These managed surfaces are not ordinary `target` artifacts. This cleanup did
not remove Nix store paths, profiles, generated inputs, Lojix state, result
links, or rollback material.

## Observations, hypotheses, and unknowns

### Observations

- Every one of the 32 reported deletion paths is currently absent.
- Every one of the five preserved candidates is currently present at its
  recorded byte total.
- The primary working copy reports no changes.
- The cleanup receipt, repository map, and alias relationship are witnessed by
  the child flow records and the commands named in those records.

### Hypotheses

- The 858 additional `/home/li` marker paths found by the broad pass are
  principally Cargo/Nix caches, embedded stores, Trash, or transient
  checkouts; the path classes support this, but project ownership is not
  inferred from a marker alone.
- The `df` delta differs from the `du` sum because of filesystem allocation
  rounding and concurrent metadata activity, not necessarily an unobserved
  deletion.

### Unknowns

- The authoritative `repos-manifest.dotos` membership has not been reconciled
  one-for-one with every physical marker path.
- Exact ownership and recoverability of old archive and private-repository
  surfaces remain unresolved.
- The missing intended Lojix GC-root tree has not been explained.
- No claim is made about repository or artifact state outside the searched
  mounts and roots, and no `/nix/store` filesystem census was performed.

## Design-oriented space-freeing protocol

1. **Classify.** Record each candidate as human-owned repository, linked
   worktree/submodule, ordinary derived artifact, package/cache, Nix/Lojix
   managed output, transient fixture, or unknown. Deduplicate `.git`/`.jj`
   markers by physical parent and record symlink aliases separately.
2. **Resolve authority.** Use `protocols/repos-manifest.dotos` for repository
   membership. Let CriomOS/CriomOS-home own managed Nix outputs and let Lojix
   own generated-input and retention semantics. A path with unclear authority
   is preserved.
3. **Gate dirty trees.** Inspect the repository's VCS status before selecting
   a derived directory. Clean repository plus understood derivation may enter
   the candidate set; dirty or VCS-uninspectable state is preserved and
   escalated.
4. **Measure before.** Capture a filesystem `df` reading, per-path
   `du -sx --bytes`, file count, type, and timestamp. Check for active build
   processes. Preserve boot, rollback, profile, package-cache, and generated
   input evidence.
5. **Delete narrowly.** Delete only the explicit, authorized derived paths;
   never use a broad root glob and never remove Nix store, profile, GC-root,
   Lojix Sema, or generated-input paths as ordinary artifacts.
6. **Verify after.** Probe every path for absence, rescan candidate roots,
   measure preserved paths, rerun VCS status, and capture `df` again. Report
   both directory-measured bytes and filesystem delta, without conflating
   them.
7. **Reconcile Nix/Lojix separately.** Before any managed cleanup, reconcile
   profiles, GC roots, `keep-derivations`/`keep-outputs`, generated-input shape
   roots, and Lojix's modeled retention states against the live root tree.
   Use the declarative owner and its typed GC operation; do not mutate the
   store filesystem directly.
8. **Close out.** Publish the exact path list, classification, authority,
   dirty-tree decisions, measurements, receipts, exclusions, unresolved
   questions, and a clean working-copy/commit/push result.

## Sources

- `flows/1ebea3fb/reports/repositoryArtifactCleanup.md`
- `flows/1ebea3fb/witnesses/congregationInventory.md`
- `flows/1ebea3fb/witnesses/preDeleteArtifactSizes.md`
- `flows/1ebea3fb/witnesses/postDeleteArtifactSizes.md`
- `flows/01a038c9/log.md`
- `protocols/repos-manifest.dotos`
- Read-only environment-behavior synthesis returned by the parent flow
