# Recent goals and archive audit witness

Snapshot: 2026-08-27. This is a read-only witness. It records identifiers, counts, paths, structural fields, and source-code behavior only. It does not copy transcript payload text, prompts, secrets, or generated content.

## Scope and terminology

A **Codex thread** is the harness-native persisted session row and rollout file. A **Flow** is the workspace record under `flows/<id>/`. A **Bead** is separate task-tracking state. These are related but not interchangeable.

The checkable recent window is defined by a connected task tree rather than a time-only range:

1. research root `01a04236-2355-7d20-94aa-e3b814a52b32`;
2. every persisted descendant of that root; and
3. audit root `01a0428b-fc0e-7200-904e-2e2991e5425f` and audit worker `01a04290-0178-7f41-bf68-5c3769174607`.

This includes the specifically requested Flow records `01a04236`, `01a04237`, and `01a042376379`. Same-day Codex threads attached to other roots are outside the window because timestamp proximity does not establish relevance.

## Observations

### Connected recent-window tree

Method: probe

```sh
python3 - <<'PY'
import sqlite3

path = "/home/li/.codex/state_5.sqlite"
root = "01a04236-2355-7d20-94aa-e3b814a52b32"
connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)

query = """
WITH RECURSIVE tree(id, depth) AS (
  VALUES (?, 0)
  UNION ALL
  SELECT edge.child_thread_id, tree.depth + 1
  FROM thread_spawn_edges AS edge
  JOIN tree ON edge.parent_thread_id = tree.id
)
SELECT tree.id, tree.depth, thread.thread_source, thread.archived,
       substr(thread.rollout_path, length(thread.rollout_path) - 68)
FROM tree
JOIN threads AS thread ON thread.id = tree.id
ORDER BY tree.depth, tree.id
"""
for row in connection.execute(query, (root,)):
    print("\t".join(map(str, row)))
PY
```

The query returned five threads: root `01a04236…`, and four direct subagent children: `01a04237…242c`, `01a04237…4416`, `01a04237…6379`, and `01a04285…`. All five had `archived=0` at the snapshot.

Method: probe

```sh
python3 - <<'PY'
import sqlite3

path = "/home/li/.codex/state_5.sqlite"
ids = (
    "01a0428b-fc0e-7200-904e-2e2991e5425f",
    "01a04290-0178-7f41-bf68-5c3769174607",
)
connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
for row in connection.execute(
    "SELECT id, thread_source, archived FROM threads WHERE id IN (?, ?)",
    ids,
):
    print("\t".join(map(str, row)))
PY
```

The audit root was an active ordinary thread and its worker was an active subagent thread. The defined recent window therefore contained seven Codex threads: five connected research threads plus two audit threads.

### No native Codex goal object in the defined window

Method: probe

```sh
for file in \
  /home/li/.codex/sessions/2026/08/27/*01a04236*.jsonl \
  /home/li/.codex/sessions/2026/08/27/*01a04237*.jsonl \
  /home/li/.codex/sessions/2026/08/27/*01a04285*.jsonl \
  /home/li/.codex/sessions/2026/08/27/*01a0428b*.jsonl \
  /home/li/.codex/sessions/2026/08/27/*01a04290*.jsonl
do
  printf '### %s\n' "$(basename "$file")"
  rg -o '"(create_goal|get_goal|update_goal|update_plan)"' "$file" |
    sort | uniq -c
done
```

The probe returned no native `create_goal`, `get_goal`, `update_goal`, or `update_plan` record for the seven rollouts. Their aims and statuses must therefore be sourced from typed requests, Flow logs/reports, and the Bead, rather than native Codex goal state.

### Flow records and short-ID collision

Method: probe

```sh
find flows -maxdepth 1 -type d -name '01a042*' -printf '%f\n' | sort

find flows -maxdepth 3 -type f -path '*/01a042*/*' -printf '%p\n' | sort
```

At the snapshot, the workspace contained these related Flow directories:

- `flows/01a04236/`
- `flows/01a04237/`
- `flows/01a042376379/`
- `flows/01a0428b/`

The three distinct Codex children `01a04237…242c`, `01a04237…4416`, and `01a04237…6379` share the first eight hexadecimal characters. `01a042376379` is a collision-extended local Flow directory. The archive-lifecycle Flow is stored under `01a04237`; the compact-retention Flow under `01a042376379`; and the schema-and-size report and witness under `01a04236`, rather than a distinct child directory. The audit worker had no Flow directory before the parent materialized this record.

This is a direct provenance/identity observation. It does not establish why the schema worker artifacts were placed under the parent and does not authorize an identity-scheme change.

### Existing research artifacts

Method: probe

```sh
stat -c '%n %s %y' \
  flows/01a04236/log.md \
  flows/01a04236/reports/codexTranscriptSchema.md \
  flows/01a04237/log.md \
  flows/01a04237/reports/archiveLifecycle.md \
  flows/01a042376379/log.md \
  flows/01a042376379/reports/compactRetention.md \
  flows/01a0428b/log.md
```

The three requested preceding investigations had extant logs and reports:

- `flows/01a04236/reports/codexTranscriptSchema.md`
- `flows/01a04237/reports/archiveLifecycle.md`
- `flows/01a042376379/reports/compactRetention.md`

The audit root's open items were a sourced subflow audit, a conversation visual, and separation of present-state audit from later protocol design or implementation.

### Local archived-rollout facts

Method: probe

```sh
find /home/li/.codex/archived_sessions -maxdepth 1 -type f \
  -name '*01a0421e-2c43-7040-8988-fe6521ab908f.jsonl' \
  -exec sh -c '
    printf "%s records=" "$1"
    jq -c . "$1" | wc -l
  ' sh {} \;

find /home/li/.codex/sessions/2026/08/27 -type f \
  -name '*01a0421e-2c43-7040-8988-fe6521ab908f.jsonl' -print

rg -l '01a0421e-2c43-7040-8988-fe6521ab908f' \
  /home/li/.codex/session_index.jsonl || true
```

The archived collection contained a file for thread `01a0421e-2c43-7040-8988-fe6521ab908f`. It was parseable plain JSONL with 21 records. The matching active dated-session path was absent, and the identifier was absent from `session_index.jsonl`.

Method: probe

```sh
python3 - <<'PY'
import sqlite3

path = "/home/li/.codex/state_5.sqlite"
connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
for row in connection.execute("""
    SELECT archived, COUNT(*)
    FROM threads
    GROUP BY archived
    ORDER BY archived
"""):
    print(row)

for row in connection.execute("""
    SELECT id, archived, archived_at, rollout_path
    FROM threads
    WHERE id = ?
""", ("01a0421e-2c43-7040-8988-fe6521ab908f",)):
    print(row)
PY
```

The database had one archived thread row at the snapshot. Its `rollout_path` pointed into `/home/li/.codex/archived_sessions/` and its archive metadata was populated.

### Archive-related CLI and resume surface

Method: probe

```sh
codex resume --help
codex archive --help
codex unarchive --help
```

The installed CLI exposes `codex archive <SESSION>` and `codex unarchive <SESSION>`. `codex resume` accepts a session UUID or name, opens a picker by default, and supports `--last` and `--all`. Help output does not establish whether an archived row can be resumed without unarchiving.

### Archive implementation and UI-list behavior

Method: code read `/git/github.com/openai/codex/codex-rs/thread-store/src/local/archive_thread.rs:15-145`

The source moves selected rollout files into `archived_sessions` with `std::fs::rename`, then marks each thread archived in persisted metadata. This path contains no compressor or hard-delete call.

Method: code read `/git/github.com/openai/codex/codex-rs/thread-store/src/local/unarchive_thread.rs:18-145`

The source implements unarchive as the reverse move into a dated active sessions path plus clearing archive metadata.

Method: code read `/git/github.com/openai/codex/codex-rs/state/src/runtime/threads.rs:874-1010,1060-1082`

Archive metadata is represented through the thread row's archive fields and updated rollout path. The schema also contains directional `thread_spawn_edges(parent_thread_id, child_thread_id, status)` rows.

Method: code read `/git/github.com/openai/codex/codex-rs/app-server/src/request_processors/thread_processor.rs:1593-1662`

A parent archive request gathers the spawn subtree, excludes already archived descendants, and sends the selected IDs to the thread store.

Method: code read `/git/github.com/openai/codex/codex-rs/tui/src/resume_picker.rs:708-742`

The resume picker issues typed archive/unarchive requests and changes its in-memory rows after successful results.

Method: code read `/git/github.com/openai/codex/codex-rs/tui/src/resume_picker/archive.rs:31-166`

The active picker offers archive for active rows and removes a successfully archived row and its preview from picker state. This is source evidence, not a fresh controlled UI action in this audit.

Method: code read `/git/github.com/openai/codex/codex-rs/app-server/README.md:812-822`

The documented list contract omits archived threads unless the caller requests archived rows.

Method: code read `/git/github.com/openai/codex/codex-rs/app-server/tests/suite/v2/thread_archive.rs:231-338,340-559,561-634`

Source tests cover successful parent-child-grandchild archival, missing-child behavior, and a child archive failure that leaves that child active while other selected threads can archive.

Method: code read `/git/github.com/openai/codex/codex-rs/rollout/src/compression.rs:24-30,346-395,432-529,632-701`

A separate optional cold-rollout worker can scan both active and archived rollout roots, create a verified `.jsonl.zst` representation, and remove the plain source after verification. This is distinct from archive.

### Remembering and visual convention

Method: code read `.agents/skills/flows/SKILL.md`

The deployed Flow protocol requires a per-flow log, index entry, witnesses, and reports. Remembering requires reading the remembered Flow's log, relevant vision, and final model response; transcript search is used when the log is insufficient. The log records remembered Flow IDs and depth.

Method: code read `.agents/skills/transcript-search/SKILL.md`

The deployed search procedure is typed-message-first: search transcript records, then retrieve exact line-addressed records; it advises against reading a transcript whole.

Method: code read `flows/b675f3d9/vision/remembering.md`

The written psyche requires the last model response of a remembered Flow to be read and says a claimed past action may require transcript-level remembering.

Method: code read `psyche-raw/Vision/visuals.md`

The written psyche's visual-medium rule is ASCII when printed in a response and Mermaid when placed in an artifact.

## Inferences

Archive is compatible with ordinary depth-one remembering: Flow logs, witnesses, reports, and reviewed psyche records are independent workspace artifacts, while archived Codex rollouts remain local JSONL at a known archive path.

Transcript-depth remembering is only conditionally compatible. Raw archived evidence remains locally readable, but the deployed `transcript-search` executable was observed absent in this setup, and no scalable search index spanning active and archived Codex rollout storage was found.

A compact-reference system must not use only the Flow's first eight hexadecimal characters as source identity. The current connected tree already contains three distinct threads sharing that prefix.

Archive hides a session from default active-list surfaces; it does not itself reduce stored data. The separate cold-compression worker is a different lifecycle mechanism.

## Limits and unknowns

- This witness did not issue archive, unarchive, deletion, compression, or resume actions.
- No controlled parent-plus-child archive was performed locally. Child behavior is source/test evidence, not a local before/after observation.
- Exact resume requirements after archive or cold compression were not tested.
- Retention periods, deletion authority, holds, backups, encryption, ACLs, privacy classification, recovery latency, and canonical collision-safe Flow identity remain unresolved authority questions.
- The snapshot does not establish whether child `01a04285…` reached a production URL.
- The compact-retention report is design work, not an approved protocol or implementation.

## Sources

- `flows/01a04236/log.md`
- `flows/01a04236/reports/codexTranscriptSchema.md`
- `flows/01a04236/witnesses/transcriptSchemaSizes.md`
- `flows/01a04237/log.md`
- `flows/01a04237/reports/archiveLifecycle.md`
- `flows/01a04237/witnesses/archiveState.md`
- `flows/01a04237/witnesses/archiveSource.md`
- `flows/01a04237/witnesses/archiveTests.md`
- `flows/01a04237/witnesses/spawnLifecycle.md`
- `flows/01a042376379/log.md`
- `flows/01a042376379/reports/compactRetention.md`
- `flows/01a042376379/witnesses/retentionInventory.md`
- `flows/01a0428b/log.md`
- `flows/01a0428b/vision/useASubflowToPutTheReportTogether.md`
- `flows/index.md`
- `flows/b675f3d9/vision/remembering.md`
- `psyche-raw/Vision/visuals.md`
- `.agents/skills/flows/SKILL.md`
- `.agents/skills/transcript-search/SKILL.md`
- `/home/li/.codex/state_5.sqlite`
- `/home/li/.codex/sessions/`
- `/home/li/.codex/archived_sessions/`
- `/home/li/.codex/session_index.jsonl`
- `/git/github.com/openai/codex`, source paths named in the observation methods above.
