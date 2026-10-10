# Witness: local archive state and file format

## Method

Method: probe `find`, `stat`, `rg`, and Python SQLite (`mode=ro`) under
`/home/li/.codex`.

Read-only probes on 2026-08-27 from `/home/li/.codex` used `find`, `stat`, `rg`,
and Python's SQLite reader (`file:...state_5.sqlite?mode=ro`). No Codex state
was modified. The archive file was parsed line-by-line as JSON.

## Direct observations

- The installed command reports `codex-cli 0.149.1`. The wrapper resolves to
  `/nix/store/8krf8lj4r85x7hcws5hwmfd9m02m4ryd-codex-0.149.1/bin/codex`.
- `/home/li/.codex/archived_sessions/` contains exactly one JSONL file:
  `rollout-2026-08-27T09-27-48-01a0421e-2c43-7040-8988-fe6521ab908f.jsonl`.
  The probe measured 48,969 bytes and 21 newline-delimited records. Its first
  bytes begin with `{` (JSON), and it does not have the gzip magic bytes
  `1f 8b`. Record types are `session_meta` (1), `event_msg` (11),
  `response_item` (6), `world_state` (1), and `turn_context` (2).
- In the same probe, the active dated sessions tree had no file whose name
  contained `01a0421e-2c43-7040-8988-fe6521ab908f`.
- `state_5.sqlite` contains a `threads` table with `archived` and
  `archived_at` columns, and a `rollout_path` column. It also contains a
  `thread_spawn_edges(parent_thread_id, child_thread_id, status)` table.
- The current database aggregate was `archived=0: 2464` and `archived=1: 1`.
  The one archived row was:

  ```text
  id=01a0421e-2c43-7040-8988-fe6521ab908f
  archived=1 archived_at=1787816203 source=vscode thread_source=user
  rollout_path=/home/li/.codex/archived_sessions/rollout-2026-08-27T09-27-48-01a0421e-2c43-7040-8988-fe6521ab908f.jsonl
  created_at=1787815668 updated_at=1787815832 title=ping
  ```

- The current parent row remained active and pointed into the dated sessions
  tree. The current worker row remained active and had
  `thread_source=subagent`; its `source` JSON contained the parent thread ID,
  depth 1, agent path, nickname, and role. The parent had three `open`
  `thread_spawn_edges` to current worker rows.
- The archived thread ID did not occur in the current
  `/home/li/.codex/session_index.jsonl` byte text. The file is a name-update
  index, not a transcript store.

## What this witness establishes

The local state has a distinct archived collection and a database flag/path
for archived threads. The archived payload is still ordinary, readable JSONL;
there is no evidence of compression. The old dated path is absent while the
archive path exists with the same rollout filename.

The source also contains a separate optional cold-rollout maintenance worker
that scans both active and archived roots and may later create `.jsonl.zst`
then remove the plain file after verification. The current file is plain and
fresh, so that maintenance representation is not present in this snapshot.

This is a snapshot, not a controlled before/after of a newly issued archive
request. It cannot by itself prove which UI action produced the row or infer
the behavior of a parent whose children are archived at the same moment.
