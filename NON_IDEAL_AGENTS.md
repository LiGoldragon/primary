# primary workspace — non-ideal agent operations

This file is the operational mirror of `AGENTS.md` for accepted, temporary
non-idealities in the primary workspace. The workarounds here are known and
sanctioned: honor them without stalling, and route the proper fix to a bigger
feature or a psyche design decision rather than force-fixing out of an unrelated
lane. When you discover a new non-ideality that is not yours to fix now, append
it here; keep ordinary rules in `AGENTS.md` and the ideal shape in
`ARCHITECTURE.md`.

## Stale git linked-worktree registrations linger in backing repos

- **Removing a worktree directory without cleaning the backing repo's git worktree
  registry leaves a prunable stale entry.** The retired `git`/`bd worktree create`
  recipe registered linked worktrees under `agent-worktrees/`; when those
  directories were deleted, the backing repo kept a dangling registration that
  `git worktree list` reports as `prunable`. Clear an existing one in a backing
  repo with `git worktree prune`.

  ```sh
  git -C repos/<repo> worktree list --porcelain   # entries marked prunable are stale
  git -C repos/<repo> worktree prune               # clears them
  ```
- **Proper fix:** create and tear down worktrees only through the orchestrator's
  lifecycle — `RequestWorktree` scaffolds a jj workspace, `ConcludeWorktree`
  (Merged or Rejected) removes it — so no manual directory deletion strands a git
  registration. A periodic sweep can prune the residue across backing repos until
  every legacy git-worktree registration is gone.
- Witnessed 2026-07-16: CriomOS, signal-introspect, and signal-standard each
  carried one stale `prunable` registration pointing at a removed
  `agent-worktrees/` directory.
