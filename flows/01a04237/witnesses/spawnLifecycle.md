# Witness: parent/subflow identity and archive traversal

## Method

Method: probe `/home/li/.codex/state_5.sqlite` read-only and code read the
matching Codex state, core, app-server, and thread-store sources.

Read-only SQLite queries against `/home/li/.codex/state_5.sqlite` and source
reads from the matching Codex 0.149.1 checkout. No rows were changed.

## Direct observations

- The schema probe returned:

  ```sql
  CREATE TABLE thread_spawn_edges (
    parent_thread_id TEXT NOT NULL,
    child_thread_id TEXT NOT NULL PRIMARY KEY,
    status TEXT NOT NULL
  )
  ```

- The current parent
  `01a04236-2355-7d20-94aa-e3b814a52b32` had three direct child edges, all
  `open`, including this worker
  `01a04237-242c-7332-9fa4-52681028c93b`. The worker's `threads.source` JSON
  was:

  ```json
  {"subagent":{"thread_spawn":{"parent_thread_id":"01a04236-2355-7d20-94aa-e3b814a52b32","depth":1,"agent_path":"/root/archive_lifecycle","agent_nickname":"Euler","agent_role":"default"}}}
  ```

  Its `thread_source` column was `subagent`; the parent's was `NULL` in this
  snapshot. This demonstrates that a subflow has its own thread row and
  rollout path, with parent identity represented both in source metadata and
  in the directional edge table.
- `codex-rs/state/src/runtime/threads.rs:122-160` upserts one directional edge
  per child and separately updates its lifecycle status. Lines `163-195` and
  `283-335` query direct children or recursively enumerate all descendants by
  parent edge, with no requirement that an edge be `open` when the
  status-unfiltered query is used.
- `codex-rs/core/src/thread_manager.rs:868-903` returns the requested root,
  all persisted descendants from the graph store, and any live descendants
  from agent control, de-duplicated.
- `codex-rs/app-server/src/request_processors/thread_processor.rs:1600-1640`
  gets that root-plus-descendants list, skips already archived rows, and keeps
  unarchived descendants whose rollouts can be read. Lines `1646-1657` reverse
  descendant order for the store call while preserving the root first.
- `codex-rs/thread-store/src/local/archive_thread.rs:24-60` locks the root
  and descendant IDs, archives each supplied thread, and reports later
  descendant failures as warnings after a successful earlier archive. The
  source path only updates each thread's archive metadata and rollout files;
  it does not delete spawn-edge rows.
- `codex-rs/state/src/runtime/threads.rs:1107-1150` documents the separate
  strict-delete path and deletes spawn edges only there, after the associated
  thread/file work.
- The local edge/flag aggregate had only `(parent archived=0, child
  archived=0): 1447` joined edges and no archived parent/child edge pair. This
  current state therefore supplies no local snapshot showing the result of
  archiving a parent with children.

## What this witness establishes

Subflows are separate persisted threads/transcripts linked by a directional
spawn graph; the source metadata records the spawning context as well. A
`thread/archive` request for a parent traverses persisted and live descendants
and attempts to archive their rollouts too. Existing edge rows are lifecycle
state, not files that are moved by archive.

The last conclusion about edge-row preservation is based on the archive source
calling only per-thread metadata updates (and on the separate delete code being
the code that removes edges), not on a local archived-parent snapshot.
