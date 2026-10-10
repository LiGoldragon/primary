# Workspace Hygiene Practices

Proposed by Discipline aspect, 2026-08-08. None yet deployed or
psyche-approved.

## Proposed practices

- **Automated /tmp sweep:** age-based, systemd timer, spare
  /tmp/claude-* for active sessions
- **Cargo target/ sweep:** periodic across /git repos
- **Branch hygiene:** periodic merged-branch pruning across all repos
- **Beads auto-export:** was off, now fixed — must stay on
- **Worktree lifecycle:** crash-recovery fallback needed (agents that
  die skip ConcludeWorktree and orphan registrations)

## Research informing these

Investigated AI workflow workspace management patterns (2026-08-07).
Key findings: branch-lifecycle binding (worktree dies when branch
merges), threshold alerting (cap worktrees per repo), session-start
sweeps, bare-repo layout for agent-heavy repos. Claude Code itself
had the same stale-worktree bug (issue #26725, fixed in v2.1.76).

## Open questions for the psyche

- The right automated cleanup interval
- Whether many repos having uncommitted changes is normal working
  state or neglect — determines whether a practice is needed
- Whether ghost directories under /git (non-repo agent debris) should
  be deleted
- GitHub token in plaintext in nix.conf — move to access-tokens?
