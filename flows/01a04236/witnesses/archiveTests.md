# Witness: focused archive lifecycle tests in source

## Method

Method: code read
`/git/github.com/openai/codex/codex-rs/app-server/tests/suite/v2/thread_archive.rs`
and local thread-store tests.

Read the checked-in app-server integration tests at
`codex-rs/app-server/tests/suite/v2/thread_archive.rs` with line numbers. The
tests use temporary Codex homes and are direct executable specifications of
the version under investigation; they were not run against the user's home.

## Direct observations

- `thread_archive_archives_spawned_descendants` at lines `231-338` creates a
  parent, child, and grandchild; persists parent→child and child→grandchild
  spawn edges; archives the parent; expects three `thread/archived`
  notifications in order `[parent, grandchild, child]`; and asserts no active
  rollout plus an archived rollout for all three IDs.
- `thread_archive_succeeds_when_descendant_archive_fails` at lines `340-559`
  creates a destination collision for the child. It expects parent and
  grandchild to archive, the child to remain active, a repeated archive of the
  already archived parent to fail, and a later unarchive to emit the expected
  analytics event. Thus descendant failure is best-effort after earlier
  successful archive work, rather than an all-or-nothing transaction over the
  whole subtree.
- `thread_archive_succeeds_when_spawned_descendant_is_missing` at lines
  `561-634` persists an edge to a child with no rollout. It expects the parent
  archive to succeed, with the parent's active path gone and archived path
  present.
- `codex-rs/thread-store/src/local/archive_thread.rs:207-258` separately tests
  that an owned descendant blocks the archive before any parent/child file is
  moved. Lines `260-306` test active-to-archive relocation, and lines
  `309-367` test deduplication and SQLite metadata update.
- `codex-rs/thread-store/src/local/unarchive_thread.rs:162-188` tests that an
  archived rollout is restored to its dated active directory and has
  `archived_at=None`.

## What this witness establishes

The supplied source tests directly cover the parent-affects-descendants rule,
the notification ordering, the distinction between a missing descendant and
an archive collision, and the lock/rollback boundary. They are stronger than
the current home snapshot for answering child behavior, while still being
source evidence rather than a newly executed production UI action.
