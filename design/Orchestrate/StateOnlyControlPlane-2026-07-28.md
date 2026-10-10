# State-only control-plane ruling — 2026-07-28

Agent question:

> Before I record or implement Claude’s Orchestrate decision: do you personally affirm that Orchestrate retains its Sema database and Unix sockets, while all repository/worktree scanning, /proc inspection, ad-hoc mirrors, VCS subprocesses, and other non-state infrastructure filesystem behavior are removed?

Psyche answer: `yes`.

Ruling:

> Orchestrate retains its Sema database and Unix sockets. Remove every repository/worktree/path scan, `/proc` inspection, ad-hoc mirror/lock projection, VCS subprocess, and other non-state-infrastructure filesystem behavior. Observe and Query are pure store projections. Worktree/claim/repository lifecycle may remain only as typed Sema state supplied by requests, never derived from host state.

This records an affirmed architectural boundary. It does not authorize implementation, deployment, or any other material change.

Correction — 2026-07-28

The `yes` authorizes implementation of exactly the affirmed source/declarative boundary set out in the ruling above. It does not authorize activation, live daemon restart, lifecycle exercise, cleanup, or other runtime mutation.

Clarification — 2026-07-28

Psyche clarification of the affirmed boundary:

> The boundary concerns Orchestrate code written to manage the filesystem/worktrees—no scanning, creating, modifying, merging, pushing, deleting, or otherwise managing filesystem worktrees/repositories; it does not concern ordinary Linux/Rust/glibc/dynamic-loader process startup.

This clarifies the scope of the prior ruling without rewriting it. It does not authorize implementation, deployment, activation, or other material change.
