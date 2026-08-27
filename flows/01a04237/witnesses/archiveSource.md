# Witness: archive UI, RPC, and local store implementation

## Method

Method: code read `/git/github.com/openai/codex/codex-rs/` archive, TUI,
app-server, state, thread-store, rollout, and compression sources.

Read the matching OpenAI Codex source checkout at
`/git/github.com/openai/codex` (clean commit
`ff29a44391deccde0aba0f8390337d7f3c319ea4`, version `0.149.1`) with `nl -ba`.
The installed binary also contains the same archive/source path strings. These
are source witnesses for the installed version, not a mutation or a runtime
experiment.

## Direct observations

- `codex-rs/tui/src/chatwidget/slash_dispatch.rs:183-206` defines `/archive`:
  it asks for confirmation, labels the action “archive and exit”, and sends
  `AppEvent::ArchiveCurrentThread`.
- `codex-rs/tui/src/app/event_dispatch.rs:2932-2957` resolves the current
  main-thread ID, rejects side conversations, calls
  `app_server.thread_archive(thread_id)`, exits only on success, and displays
  an error while continuing on failure.
- `codex-rs/tui/src/resume_picker.rs:708-742` sends the typed app-server
  requests `ClientRequest::ThreadArchive` and `ThreadUnarchive`. The picker
  then updates its rows only after the archive result succeeds.
  `codex-rs/tui/src/resume_picker/archive.rs:31-76,78-137` makes the archive
  shortcut available only for active resume rows, refuses to archive the
  currently open row from the picker, and removes a successfully archived row
  and its transcript preview from picker state. This is UI state, after the
  server operation.
- `codex-rs/tui/src/session_archive_commands.rs:103-134,136-183` shows the
  CLI `archive` command is a thin app-server client. ID targets are passed
  directly; name targets are resolved only among active rows for archive and
  only among archived rows for unarchive.
- `codex-rs/app-server/src/request_processors/thread_processor.rs:1593-1662`
  reads the requested active thread, gathers its spawn subtree, prepares the
  IDs, and invokes `thread_store.archive_threads`. It includes only
  unarchived descendants, and emits an archived notification for each ID
  returned by the store.
- `codex-rs/thread-store/src/local/archive_thread.rs:15-60,63-145` scans
  rollout references, resolves each selected rollout, creates
  `codex_home/archived_sessions`, and constructs `(source,destination)` pairs.
  It then calls `std::fs::rename(source, destination)` and finally
  `mark_archived(thread_id, archive_path, Utc::now())`. Rename and metadata
  failures attempt rollback. There is no compression call and no delete call
  in this path.
- `codex-rs/state/src/runtime/threads.rs:1060-1082` implements
  `mark_archived`: it sets `archived_at`, replaces `rollout_path` with the
  archive path, refreshes `updated_at` from the archived file mtime, and
  upserts the thread row.
- `codex-rs/state/src/runtime/threads.rs:874-1010` binds the persisted
  `archived` flag from `metadata.archived_at.is_some()` during that upsert, so
  the flag and timestamp move together.
- `codex-rs/app-server/README.md:812-822` documents the same contract: the
  persisted JSONL moves into the archived sessions directory and an archived
  thread is omitted from `thread/list` unless `archived=true`.
- `codex-rs/thread-store/src/local/unarchive_thread.rs:18-145` is the reverse:
  it resolves an archived rollout, renames it into
  `sessions/YYYY/MM/DD/<same filename>`, refreshes mtime, clears
  `archived_at`, and updates the active path. It also rolls back on failure.
- A separate mechanism exists and must not be confused with the archive
  request: `codex-rs/rollout/src/compression.rs:24-30,346-395,432-529,632-701`
  starts a best-effort cold-rollout worker (when enabled). That worker scans
  both `archived_sessions` and `sessions`, writes a `.jsonl.zst` sibling, then
  removes the plain `.jsonl` only after verification. Thus a later maintenance
  pass can compress an already archived transcript, but the archive operation
  itself does not invoke this worker or perform that representation change.
- `codex-rs/rollout/src/session_index.rs:21-105,107-237` only appends or
  removes name-update entries and resolves names. The archive implementation
  does not call these functions; archive visibility is therefore represented
  by thread metadata/path and list filtering, not by rewriting this index.

## What this witness establishes

For this installed/source-matched version, the archive operation is a physical
rename of one or more existing rollout files followed by SQLite metadata
updates. It is not an in-place rewrite, compression, or hard delete. A separate
optional cold-rollout maintenance worker can later replace either active or
archived plain JSONL with `.jsonl.zst` and remove the plain representation after
verification; that is retention/maintenance, not the archive request. Unarchive
renames the archived representation back and clears the metadata flag. UI list
removal and the current-session exit are post-success presentation/control
behavior, not the storage operation.
