# Codex transcript archival and parent/subflow lifecycle

Observed 2026-08-27 for the installed, source-matched `codex-cli 0.149.1`.
This is a read-only investigation; no user transcript, SQLite row, or runtime
process was changed.

## Result

The UI's archive action calls app-server `thread/archive`. For local storage,
Codex moves the selected rollout file from the dated
`~/.codex/sessions/YYYY/MM/DD/` tree into the flat
`~/.codex/archived_sessions/` directory with `std::fs::rename`, then updates
the SQLite thread row (`archived_at` and `rollout_path`). The archive path does
not itself compress, rewrite, or delete the transcript. A separate optional
cold-rollout maintenance worker can later represent either active or archived
files as `.jsonl.zst` and remove the plain source after verification. Unarchive
reverses the move and clears the archive metadata.

Archiving is subtree-aware. A parent request gathers persisted spawn-edge
descendants and live agent descendants, then attempts to archive each
unarchived descendant rollout. A child with a missing rollout is skipped with a
warning while the parent can still archive; a later child move failure is
best-effort after earlier successes; an active writer on any descendant blocks
the operation before files move. Spawn-edge rows are lifecycle metadata and
are not removed by the archive path. The local snapshot has no archived
parent/child pair, so that final edge-preservation statement is source-based,
not a local before/after observation.

## Direct observations

### UI and command path

- `/archive` asks for confirmation, sends `ArchiveCurrentThread`, and exits the
  current main TUI only after a successful app-server call. Side conversations
  are rejected.
- The resume picker sends the same typed `ThreadArchive` request for a selected
  active row (but tells the user to use `/archive` for the currently open row).
  After success it removes the row and transcript preview from picker memory.
- The `codex archive` CLI is also a thin app-server client. A name target is
  resolved among active threads; unarchive resolves among archived threads.
- The app-server's documented list contract omits archived threads unless the
  caller sets `archived=true`; this is metadata/filtering behavior, not a
  second transcript store.

These presentation changes are separate from persistence: the app-server and
thread store perform the move and database update.

### Files and database

The live home probe found one archived transcript at
`/home/li/.codex/archived_sessions/rollout-2026-08-27T09-27-48-01a0421e-2c43-7040-8988-fe6521ab908f.jsonl`
(48,969 bytes, 21 JSONL records, no gzip magic). Its matching dated-session
path was absent. SQLite had one `archived=1` thread row with that archive path
and `archived_at=1787816203`, versus 2,464 active rows. The archived ID was not
present in `session_index.jsonl`; source shows that file is only an append/remove
name-update index, not the archive ledger or transcript store.

The source's distinct compression worker scans both `archived_sessions` and
`sessions`; when enabled, it only processes cold plain rollouts and writes a
verified `.jsonl.zst` before removing the plain file. No such `.zst` file was
present for the current archived snapshot.

### Subflow identity

The `threads` table has one row/path per thread. `thread_spawn_edges` stores
`parent_thread_id`, `child_thread_id` (unique), and `status`. The current
worker's row has `thread_source=subagent` and source JSON recording its parent
ID, depth, agent path, nickname, and role. Its own dated rollout file is
separate from the parent's file. The current parent had three open direct child
edges. All 1,447 joined edge rows in the snapshot had both endpoints active;
there was no local archived-child example.

## Parent archive behavior

The app-server source calls `list_agent_subtree_thread_ids`, which combines
persisted graph descendants with live agent-control descendants. It reads the
root and descendants, excludes already archived descendants, reverses the
descendant order for the store call, and emits `thread/archived` per successful
thread.

The checked-in integration test `thread_archive_archives_spawned_descendants`
creates parent → child → grandchild edges and asserts all three active files
become archived, with notifications ordered `[parent, grandchild, child]`.
Other tests directly establish the boundaries: a missing child does not block
the parent; a child destination collision leaves that child active while the
parent and grandchild archive; and an owned descendant rejects the operation
before any file is moved.

## Inferences

- Because archive's store implementation only renames rollout files and calls
  per-thread `mark_archived`, while edge deletion is implemented separately in
  the delete path, archive leaves `thread_spawn_edges` in place. This is a
  source inference rather than a local archived-parent snapshot.
- The physical archive move preserves the filename and file bytes; the archive
  source does not invoke a compressor or content rewrite. The current archived
  file's plain JSONL shape is consistent with this. A separate cold-file
  maintenance pass may later create a verified zstd representation and remove
  the plain file, so “never compressed” would be an overclaim.
- A child may remain active after a parent archive if its own archive attempt
  fails. “Parent archive” therefore does not mean an atomic transaction over
  the complete spawn subtree.

## Unknowns and limits

- No controlled production UI archive was issued during this investigation, so
  the local archived `ping` row is not attributed to a particular UI gesture.
- The current home state does not contain an archived parent plus child, so it
  cannot independently show post-archive edge flags or child visibility.
- This report covers local Codex storage/app-server behavior in 0.149.1. Remote
  workspaces, other versions, retention scheduling/configuration, backup
  behavior, and any external UI wrapper are outside the direct witnesses.

## Sources

- `flows/01a04237/witnesses/archiveState.md`
- `flows/01a04237/witnesses/archiveSource.md`
- `flows/01a04237/witnesses/spawnLifecycle.md`
- `flows/01a04237/witnesses/archiveTests.md`
- `/git/github.com/openai/codex/codex-rs/thread-store/src/local/archive_thread.rs:15-145`
- `/git/github.com/openai/codex/codex-rs/thread-store/src/local/unarchive_thread.rs:18-145`
- `/git/github.com/openai/codex/codex-rs/state/src/runtime/threads.rs:122-195,283-335,1060-1105`
- `/git/github.com/openai/codex/codex-rs/state/src/runtime/threads.rs:874-1010`
- `/git/github.com/openai/codex/codex-rs/state/src/runtime/threads.rs:1107-1150`
- `/git/github.com/openai/codex/codex-rs/core/src/thread_manager.rs:868-903`
- `/git/github.com/openai/codex/codex-rs/app-server/src/request_processors/thread_processor.rs:1593-1662`
- `/git/github.com/openai/codex/codex-rs/app-server/tests/suite/v2/thread_archive.rs:231-338,340-559,561-634`
- `/git/github.com/openai/codex/codex-rs/app-server/README.md:812-822`
- `/git/github.com/openai/codex/codex-rs/tui/src/chatwidget/slash_dispatch.rs:183-206`
- `/git/github.com/openai/codex/codex-rs/tui/src/app/event_dispatch.rs:2932-2957`
- `/git/github.com/openai/codex/codex-rs/tui/src/resume_picker.rs:708-742`
- `/git/github.com/openai/codex/codex-rs/tui/src/resume_picker/archive.rs:31-166`
- `/git/github.com/openai/codex/codex-rs/tui/src/session_archive_commands.rs:103-183`
- `/git/github.com/openai/codex/codex-rs/rollout/src/session_index.rs:21-105,107-237`
- `/git/github.com/openai/codex/codex-rs/rollout/src/compression.rs:24-30,346-395,432-529,632-701`
- `/home/li/.codex/state_5.sqlite` (read-only schema/query witness)
- `/home/li/.codex/archived_sessions/` and `/home/li/.codex/sessions/` (read-only filesystem witness)
