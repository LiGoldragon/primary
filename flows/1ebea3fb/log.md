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
- Thirty-two paths were deleted successfully in the first round with zero
  failures: 31 Cargo targets and one Python cache. A bounded follow-up
  audited and deleted four preserved Cargo targets plus one archive Python
  cache, again with zero failures. Incremental directory-measured reclaim was
  13,172,906,260 bytes; cumulative reclaim is 51,103,723,328 bytes. All 37
  exact paths are absent in the post-delete witnesses, and unrelated dirty
  source/beads work remains intact.

## Open

- Parent-flow handoff after committing and pushing these flow artifacts.
