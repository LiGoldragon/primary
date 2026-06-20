# 446 — Schema branch cleanup and cargo sweep

## Scope

The psyche asked to remove stale branches after preservation, do broad cargo
sweeping, manage context, and give a small audit of the day's operator work.

## Branch cleanup

Kept preservation refs:

- `schema-rust-next`: `operator/preserve-schema-rust-next-reaction-expand` at
  `8b147fac`.
- `schema-rust-next`:
  `operator/preserve-schema-rust-next-structural-forms-integration` at
  `a0138ce1`.
- `schema-next`: `operator/preserve-schema-next-capability-resolution` at
  `3709fc15`.
- `schema-next`: `operator/preserve-schema-next-structural-forms-integration`
  at `b7af872e`.

Removed stale branch names:

- `schema-rust-next`: local-only `next/schema-capability-resolution`.
- `schema-rust-next`: `structural-forms-integration`, including the tracked
  remote branch.
- `schema-next`: `next/schema-capability-resolution`, including the tracked
  remote branch.
- `schema-next`: `structural-forms-integration`, including the tracked remote
  branch.

This leaves current `main` plus explicit preservation bookmarks. The old names
no longer look active, and the old commits remain recoverable.

## Cargo sweep

Green:

- `schema-next`: `cargo test --all-targets --all-features`.
- `schema-next`: `cargo clippy --all-targets --all-features -- -D warnings`.
- `schema-next`: `cargo test --lib --no-default-features`.
- `schema-rust-next`: `cargo test --all-targets --features nota-text`.
- `schema-rust-next`: `cargo clippy --all-targets --features nota-text -- -D
  warnings`.
- `schema-rust-next`: `cargo test --lib --no-default-features`.

No code changes were made to either schema repo.

## Context state

Clean:

- `/git/github.com/LiGoldragon/schema-next`.
- `/git/github.com/LiGoldragon/schema-rust-next`.
- `/home/li/primary` before this report was added.

The two old worktree directories still exist as filesystem context, but their
content is no longer the only copy of the work. The recoverable source of truth
is now the four `operator/preserve-*` bookmarks above.

## Day audit

Operator work today landed three kinds of value:

- Mentci direction was clarified: the GUI should revive as a daemon client over
  `signal-mentci`, using shared `mentci-lib` model state rather than duplicating
  approval/observation logic in `mentci-egui`.
- The stale schema worktrees were investigated, preserved, and de-risked. The
  result is not a merge: `reaction-expand` needs a fresh cross-repo port over
  current `schema-next`/`schema-rust-next` main, and
  `structural-forms-integration` is only a mining source now.
- The misleading old schema branch names were retired after preservation, and
  current schema mains were swept green with tests and clippy.

Next operator-safe move is to return to the Mentci integration lane: merge the
designer's additive `signal-mentci` readers, then rebase/adapt the
`mentci-lib` and `mentci-egui` shared-model branches onto main.
