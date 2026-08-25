# Congregation inventory

Method: probe `find /home/li ... -type d \( -name .git -o -name .jj \)`,
`find /git ... -type d \( -name .git -o -name .jj \)`, `find -L
/home/li/primary/repos`, and `du -sx --bytes` on congregation roots. VCS
markers were normalized to unique repository paths; `.git` and `.jj` markers
for the same path count once.

The primary `repos/` path is a symlink to `/git/github.com/LiGoldragon` and is
reported as an alias, not a second copy.

## Roots

| Root | Unique repository paths | Notes |
| --- | ---: | --- |
| `/git` | 595 | 576 under `/git/github.com`, plus 19 under other forge hosts |
| `/git/github.com/LiGoldragon` | 188 | 182 direct roots and 6 nested roots; 184 top-level directories exist, two without VCS markers |
| `/home/li/primary/repos` | alias of 184 top-level directories | symlink to the LiGoldragon root above |
| `/home/li/git-archive` | 132 | archived Git/Jujutsu repositories, including nested historical components |
| `/home/li/wt` | 72 | isolated repository worktrees |
| `/home/li/primary-worktrees` | 4 | isolated primary worktrees |
| `/home/li/primary-workspaces` | 1 | isolated primary workspace |
| `/home/li/worktrees` | 2 | external worktrees |
| `/home/li/.gemini/history` | 11 | history repositories |
| `/home/li/.gc/cache/repos` | 8 | cache repositories |
| `/home/li/.pi` | 1 | extension repository |
| `/home/li/primary` | 1 | current primary repository |
| `/home/li/primary/private-repos` | 1 VCS root | also contains unversioned incident evidence; preserved |
| standalone local roots | 5 | password-store, judge rerun, and three `wt-primary-*` roots |

The initial focused `/home/li` marker scan found 238 unique repository paths:
35 Git-only, 83 Jujutsu-only, and 120 with both markers. In the broader `/git`
scan, 595 unique VCS roots were found. `/git/github.com` has 576 unique roots;
the other hosts are codeberg.org (2), code.videolan.org (2), depp.brause.cc
(1), gist.github.com (2), git.lix.systems (1), git.sr.ht (5), gitlab.com (3),
gitlab.ezracelli.dev (1), and gitlab.freedesktop.org (2).

Across the focused 238 repositories, ecosystem markers were multi-label:
Rust 105, Nix 152, Python 14, Node 22, and no recognized marker 51; 91 had
more than one ecosystem marker.

## Sources

- `/tmp/repo_roots.txt`, `/tmp/git_actual_unique.txt` — probe outputs used to
  derive the counts above.
- `flows/1ebea3fb/witnesses/preDeleteArtifactSizes.md` — artifact candidates
  and exact size measurements.
