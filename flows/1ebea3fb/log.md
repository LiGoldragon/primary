# Flow 1ebea3fb

## About

Repository-congregation inventory and safe removal of understood derived
build artifacts under the living's explicit cleanup request.

## Settled

- The scan covers `/git` (all local forge hosts), `/home/li/git-archive`,
  `/home/li/wt`, `/home/li/worktrees`, `/home/li/primary-worktrees`,
  `/home/li/primary-workspaces`, `/home/li/.gemini/history`,
  `/home/li/.gc/cache/repos`, `/home/li/.pi`, the primary repository, and
  the primary `repos/` and `private-repos/` congregation roots.
- Only Cargo `target/` directories and Python `__pycache__` directories with
  clear derivation are cleanup candidates. Source, package caches,
  rollback evidence, Nix result links, and uncertain ownership remain.
- Dirty or VCS-uninspectable repositories are preserved.
- Thirty-two selected paths were deleted successfully with zero failures:
  31 Cargo targets and one Python cache. The directory-measured reclaim was
  37,930,817,068 bytes; all selected paths are absent in the post-delete
  witness.

## Open

- Parent-flow handoff and commit/push of these flow artifacts.
