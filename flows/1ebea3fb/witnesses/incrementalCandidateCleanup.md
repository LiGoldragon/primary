# Incremental preserved-candidate cleanup

This witness resolves the five candidates preserved by the first cleanup
round. Method: inspect each root's `Cargo.toml`/`Cargo.lock`/`flake.nix` and
ignore files, probe the parent commit and working copy with `jj file list` and
`jj status --no-pager`, run `cargo metadata --no-deps --format-version 1
--offline` where a manifest exists, inspect Cargo's `.rustc_info.json` and
`CACHEDIR.TAG`, inspect Python source and `.pyc` suffixes, then measure each
exact path with `du -sx --bytes`. No build was run and no `/nix/store` search
was performed.

All five paths are wholly derived output, with no source-owned files. Four are
Cargo `target/` trees; the fifth is a Python `__pycache__` containing only
`.pyc` files. Dirty source or beads elsewhere was not treated as a reason to
retain an independent derived directory.

## Path-specific evidence

| Path | Metadata/status/index evidence | Resolution |
| --- | --- | --- |
| `/git/github.com/LiGoldragon/Curriculum/target` | Standard Cargo markers `.rustc_info.json` and `CACHEDIR.TAG`; payload is Cargo release/debug/dependency output (`.rlib`, `.rmeta`, `.so`, `.d`, binaries, generated build files, locks, and flycheck stdout/stderr). The root has no current `Cargo.toml` or `Cargo.lock`; `jj file list -r @- -- target` has no match; `jj status` reports 3,410 target-only additions and no source/other entries. The target is unignored but untracked; no source-owned path is present. | Derived output is unambiguous and explicitly authorized for cleanup, although regeneration from this current source-only checkout is not demonstrated. |
| `/git/github.com/LiGoldragon/lojix/target` | Root `Cargo.toml`, `Cargo.lock`, and `flake.nix`; `cargo metadata --no-deps --offline` exits 0 and names `lojix` plus workspace packages. `.gitignore` contains `target/`; `jj file list -r @- -- target` has no match. `jj status` has 13 unrelated `.beads` entries and no target entries. | Safe: ignored, untracked, reproducible Cargo output; unrelated dirty beads preserved. |
| `/git/github.com/LiGoldragon/spirit/target` | Root `Cargo.toml`, `Cargo.lock`, and `flake.nix`; offline Cargo metadata exits 0 and names `spirit` plus workspace packages. `.gitignore` contains `/target`; `jj file list -r @- -- target` has no match. `jj status` has 18 unrelated source edits and no target entries. | Safe: ignored, untracked, reproducible Cargo output; unrelated dirty source preserved. |
| `/git/github.com/LiGoldragon/spirit-ethos/target` | Root `Cargo.toml`, `Cargo.lock`, and `flake.nix`; offline Cargo metadata exits 0 and names `spirit-ethos` plus workspace packages. No ignore rule exists, but `jj file list -r @- -- target` has no match; current `jj status` reports 15 target additions separately from six source/config changes. Payload is only Cargo markers, locks, fingerprints, `.rmeta`, `.d`, and the library output. | Safe: untracked, unignored but wholly derived Cargo output; source/config changes preserved. |
| `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/tools/edn_format/__pycache__` | Parent `/home/li/git-archive/Mentci-AI` has both `.git` and `.jj`; `jj file list -r @- -- Sources/mentci-ai/tools/edn_format/__pycache__` has no match, and `jj status` has no path-specific entry. Parent and nested `.gitignore` files contain only target rules, not Python-cache rules; Git index strings contain no `edn_format`, `__pycache__`, or `.pyc` path. The containing package has eight `.py` source files; this directory has 11 `.pyc` files only. | Safe: untracked, unignored, wholly derived Python bytecode cache; unrelated archive dirty paths preserved. |

The four Cargo directories all have Cargo's standard cache marker and Rust
fingerprint metadata. Curriculum lacks a current manifest, so its immediate
rebuild was not claimed; its directory class and payload still establish
derived output rather than source. The other three had successful offline
metadata witnesses.

## Pre-delete measurements

| Path | Bytes | Files |
| --- | ---: | ---: |
| `/git/github.com/LiGoldragon/Curriculum/target` | 2,033,177,042 | 3,410 |
| `/git/github.com/LiGoldragon/lojix/target` | 10,644,240,040 | 6,419 |
| `/git/github.com/LiGoldragon/spirit/target` | 495,431,163 | 1,070 |
| `/git/github.com/LiGoldragon/spirit-ethos/target` | 120,784 | 15 |
| `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/tools/edn_format/__pycache__` | 57,231 | 11 |
| **Incremental total** | **13,172,906,260** | **10,925** |

The incremental byte sum is **13,172,906,260** (12.263597 GiB,
13.172906 GB). The individual measurements above are the authoritative
pre-delete values.

## Post-delete verification and cumulative receipt

Deletion used `find <exact-path> -depth -delete` only after validating each
candidate as a non-symlink directory. The command selected exactly the five
paths in the table and reported `deleted=5 failures=0 selected=5`. A direct
`test ! -e` check then found every selected path absent. The bounded
rescan of `/git`, `/home/li/git-archive`, `/home/li/wt`,
`/home/li/worktrees`, `/home/li/primary-worktrees`, and
`/home/li/primary-workspaces`, with virtual environments, package/dependency
trees, and VCS metadata excluded, found no remaining cleanup candidates in
the scanned congregation roots. The archive virtual environment's
`site-packages/**/__pycache__` directories were observed separately and
retained as package/dependency cache content.

| Path | Post-delete bytes | Post-delete state |
| --- | ---: | --- |
| `/git/github.com/LiGoldragon/Curriculum/target` | 0 | absent |
| `/git/github.com/LiGoldragon/lojix/target` | 0 | absent |
| `/git/github.com/LiGoldragon/spirit/target` | 0 | absent |
| `/git/github.com/LiGoldragon/spirit-ethos/target` | 0 | absent |
| `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/tools/edn_format/__pycache__` | 0 | absent |
| **Incremental reclaim** | **13,172,906,260** | **5 deleted, 0 failures** |

The first cleanup round reclaimed 37,930,817,068 directory-measured bytes.
Including this incremental pass, cumulative directory-measured reclaim is
**51,103,723,328 bytes** (47.594051 GiB, 51.103723 GB). The independent
filesystem observation moved from 499,964,684 to 486,998,292 used 1 KiB
blocks, a 13,277,585,408-byte decrease; that `df` value includes filesystem
allocation effects and is reported separately from the authoritative
per-directory sum.

Post-delete VCS checks show no derived entries in any of the five containing
repositories. Unrelated dirty work remains intact: 13 `.beads` entries in
`lojix`, 18 source entries in `spirit`, six source/config entries in
`spirit-ethos`, and two archive entries in `Mentci-AI`. Curriculum is clean
after its target-only additions were removed.

## Sources

- `flows/1ebea3fb/witnesses/preDeleteArtifactSizes.md`
- `flows/1ebea3fb/witnesses/postDeleteArtifactSizes.md`
- `flows/1ebea3fb/reports/repositoryArtifactCleanup.md`
