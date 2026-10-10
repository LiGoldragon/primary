# Orchestrate repository state

Method: subflow probes `git worktree list --porcelain`, `jj workspace list`,
`jj status`, commit/diff queries, repeated `git ls-remote`, and package files in
`/git/github.com/LiGoldragon/orchestrate` at
2026-08-22T18:15:33–18:18:16+02:00.

The primary checkout was clean. Local `main`, the checkout parent, and the
repeatedly observed remote `main` were
`b14355577286e56902d085ad4e1bf2654a55931e`: zero commits ahead or behind.
The repository and CLI package version were both `0.20.0`. The repository had
no upstream remote, upstream-main ref, or local tags.

Two non-primary JJ workspaces had existing roots and clean, empty working-copy
commits:

- `repair-home-dependency-chain-20260811`, target `dcf0a526`, 11 days old. Its
  historical base lacks the six-line Protos status block now on main; it has no
  target-specific content and no lane-registration work.
- `schema-rust-main`, target `7a63b632`, 12 days old. Its historical base has
  dependency-pin/schema differences in `AGENTS.md`, `Cargo.toml`, and
  `Cargo.lock`; it has no target-specific content and no lane-registration
  documentation work.

Six JJ workspace records had missing roots. Every target was an empty
working-copy commit whose parent was reachable from current main. Their target
diffs contained zero changed files:

- `designer-doc-drift-2026-06-07`, `4e4b2d51`, 70 days old.
- `docs-emit-schema-rename`, `220e61f1`, 70 days old.
- `orchestrate-e2e`, `e4b85a74`, 70 days old.
- `orchestrate-supervision-surface`, `a6d8d892`, 78 days old.
- `port-orchestrate`, `564c55af`, 70 days old.
- `worktree-registry-daemon`, `406a3fc9`, 62 days old.

The six are dangling metadata, not recoverable working directories, and hold
no target-specific source content. The first and last names are adjacent to
documentation/worktree machinery but predate and do not contain the
lane-registration incident.

The static `orchestrate/worktrees.dotos` projection was last modified
2026-07-31 and names seven absent paths as active. With no daemon socket, it is
stale evidence rather than current authority.

