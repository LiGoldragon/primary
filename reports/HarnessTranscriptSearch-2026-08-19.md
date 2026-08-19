# Harness Transcript Search — 2026-08-19

Question: What are the session transcript files each coding harness writes, where do they live, what is their format, and what tools exist to search them?

---

## Part 1 — Witness on this machine

### Claude Code

**What Claude Code calls them:** "conversations" in the UI; the CLI flag is `--resume` or `-c` (continue). The `/resume` slash-command opens an interactive picker. The term "session" appears in the sessionId field and the `--no-session-persistence` flag. The term "transcript" does not appear in help text.

**Files witnessed:**

| Path pattern | Count | Size range | Status |
|---|---|---|---|
| `~/.claude/projects/-home-li-primary/<uuid>.jsonl` | 84 JSONL files | 1 KB – 942 KB | WITNESSED |
| `~/.claude/projects/-home-li-primary/<parent-uuid>/subagents/agent-<id>.jsonl` | many per session | small | WITNESSED |
| `~/.claude/projects/-home-li-primary/<parent-uuid>/subagents/agent-<id>.meta.json` | many per session | tiny | WITNESSED |
| `~/.claude/history.jsonl` | 1 file, 12,709 lines | 6.6 MB | WITNESSED |
| `~/.claude/sessions/<pid>.json` | 4 live-session files | ~390 B each | WITNESSED |

Total size of `-home-li-primary` project: 871 MB.

Note: there are also directories named by UUID alongside the `.jsonl` files. Each such directory contains `subagents/` and `tool-results/` trees. The `.jsonl` file is the main session transcript; the directory holds subagent transcripts spawned during that session.

**Record shape — first 3 records of `e06e4c07-...jsonl` (keys and types only):**

```
Record 1: {type:str, mode:str, sessionId:str}
Record 2: {type:str, permissionMode:str, sessionId:str}
Record 3: {type:str, messageId:str, snapshot:{messageId:str, trackedFileBackups:{}, timestamp:str}, isSnapshotUpdate:bool}
```

Message records (the substantive ones, further down in the file):

```
top-level: parentUuid, isSidechain, promptId, type, message, uuid, timestamp,
           permissionMode, origin, promptSource, userType, entrypoint, cwd,
           sessionId, version, gitBranch
message:   {role:str, content:list}
content[]:  {type:"text"|"tool_result"|"tool_use"|"thinking"|"thinking_delta", ...}
```

**How `--resume`/`-c` finds sessions:** `--resume [session-id]` reads the JSONL file whose sessionId matches; without an ID it opens a picker over all project JSONL files. `-c` continues the most recent JSONL in the current directory's encoded project folder. `history.jsonl` records `{display, pastedContents, timestamp, project, sessionId}` and is used to populate the picker. `sessions/<pid>.json` tracks live running sessions (pid, sessionId, cwd, status).

---

### Codex CLI

**What Codex calls them:** "rollouts" (the filename prefix is `rollout-`). Codex also uses "session" for the resumable unit. `codex resume` opens an interactive picker; `codex resume --last` continues the most recent.

**Files witnessed:**

| Path pattern | Count | Size range | Status |
|---|---|---|---|
| `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl` | 1,137 files | up to 17 MB | WITNESSED |
| `~/.codex/session_index.jsonl` | 1 file, 57 lines | small | WITNESSED |

Session index record shape: `{id, thread_name, updated_at}`.

**Record shape — rollout JSONL (keys and types only):**

```
Record 1: {timestamp:str, type:"session_meta", payload:{session_id, id, timestamp, cwd,
           originator, cli_version, source, thread_source, model_provider,
           base_instructions:{text}, history_mode, context_window:{window_id}, git:{...}}}
Record 2: {timestamp:str, type:"event_msg", payload:{type:"turn_started", turn_id, ...}}
Record 3: {timestamp:str, type:"event_msg"|"response_item", payload:{type:str, role:str,
           content:list[N], ...}}
```

Record type taxonomy (from a 17 MB session): `event_msg+token_count` (490), `response_item+function_call` (428), `response_item+function_call_output` (428), `response_item+reasoning` (304), `response_item+message` (152), `event_msg+agent_message` (145), and others. The outer `type` field is coarse (`event_msg`, `response_item`); the `payload.type` field is the discriminator.

---

### Pi harness

Pi (the psyche's earlier coding harness, now supplanted by Codex) is present on this machine.

**Files witnessed:**

| Path pattern | Count | Size range | Status |
|---|---|---|---|
| `~/.pi/agent/sessions/<encoded-cwd>/<timestamp>_<uuid>.jsonl` | 1,274 files | 1 KB – 512 KB | WITNESSED |
| `~/.pi/agent/run-history.jsonl` | 1 file, 16,193 lines | medium | WITNESSED |

Run-history record shape: `{agent, task, ts, status, duration, taskHash}`.

**Record shape — pi session JSONL (keys and types only):**

```
Record 1: {type:"session", version:int, id:str, timestamp:str, cwd:str}
Record 2: {type:"model_change", id, parentId, timestamp, provider, modelId}
Record 3: {type:"thinking_level_change", id, parentId, timestamp, thinkingLevel}
```

Message records: `{type:"message", id, parentId, timestamp, message:{role, content:list, timestamp}}`. Other types in a full session: `session_info`, `custom_message`, `custom`.

Pi's encoded CWD appears in the session directory name (e.g. `--home-li-primary--`), paralleling Claude Code's `~/.claude/projects/-home-li-primary/` encoding convention.

---

## Part 2 — Tools for searching these transcripts

### ccusage (WITNESSED — available via `npx ccusage`)

- Reads: Claude Code, Codex, pi-agent, and 15+ other harnesses
- Detects JSONL paths automatically by harness
- Commands: `session`, `daily`, `monthly`, `weekly`, `blocks`
- Query support: by date, by session, by harness — **not by text content**
- Purpose: token counting and cost reporting, not transcript search
- Offline: yes after first run
- CLI-callable: yes; output is a table
- Limitation: no text search, no role filtering

### ripgrep + jq (WITNESSED — both installed)

- `rg '"text":\s*".*keyword.*"' ~/.claude/projects/-home-li-primary/*.jsonl` searches across all sessions
- `jq -r 'select(.message.role=="user") | .message.content[] | select(.type=="text") | .text'` extracts user text from one file
- Query support: arbitrary regex; can filter by role/type in jq
- Offline: yes
- CLI-callable: yes; output can be bounded with `--max-count`
- Limitation: no cross-session index; on 871 MB it is slow; jq processes one file at a time

### Python sqlite3 FTS5 import (not installed as package; python3 sqlite3 module available)

A small script can read all JSONL files, extract `(session_id, timestamp, role, content_type, text)` rows, and load into SQLite FTS5. Queries then run sub-second across the full corpus.

```python
# Sketch (not yet written):
import sqlite3, json, glob
con = sqlite3.connect("transcripts.db")
con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS turns USING fts5(session_id, ts, role, text)")
for f in glob.glob("/home/li/.claude/projects/-home-li-primary/*.jsonl"):
    ...  # extract user/assistant text content items
```

- Query support: full-text search across all sessions, filterable by role
- Offline: yes
- CLI-callable: `sqlite3 transcripts.db "SELECT * FROM turns WHERE turns MATCH 'ruling'"`
- Limitation: requires initial build (~minutes over 871 MB); must be rebuilt after new sessions

### DuckDB (NOT available on this machine)

DuckDB can query JSONL natively with `read_ndjson_auto()` and supports full-text filtering. Would be ideal for ad-hoc queries. Not installed.

### The size problem

A single Claude Code session JSONL reaches 942 KB; some Codex rollouts hit 17 MB. Tool results dominate by volume — a single file may have 73 `tool_result` content items vs 9 user text messages (witnessed ratio in current session). Any search approach that does not filter to `content[].type == "text"` and `message.role == "user"|"assistant"` will be dominated by tool output noise.

### Comparison table

| Tool | Reads | Text search | By date | By role | Offline | Bounded CLI output |
|---|---|---|---|---|---|---|
| ccusage | all harnesses | no | yes | no | yes | yes |
| rg + jq | any JSONL | yes (regex) | manual | yes (jq) | yes | yes (--max-count) |
| sqlite3 FTS5 (custom) | any JSONL | yes (FTS) | yes | yes | yes | yes |
| DuckDB | any JSONL | yes | yes | yes | yes | yes |

### Three options for this workspace

**Option A — rg + jq, no setup.** For ad-hoc queries now: `rg '"kind": "human"' ~/.claude/projects/-home-li-primary/*.jsonl -l` to find files with psyche-typed messages, then `jq` to extract text. Slowest on large corpus but zero infrastructure.

**Option B — SQLite FTS5 import script.** Write a 30-line Python script that scans all JSONL files, extracts user-role text-type content items (distinguishing human-origin from tool-injected by `origin.kind == "human"`), and loads into a local SQLite FTS5 database. Agents call `sqlite3 ~/transcripts.db "SELECT session_id, ts, text FROM turns WHERE turns MATCH 'X'"`. Rebuild after each session.

**Option C — ccusage for session discovery, jq for content.** Use `npx ccusage session` to list sessions by date, identify the relevant session UUID, then run jq over that one file. Narrows the search space before the expensive text scan.

---

## Part 3 — JSONL encoding of message types and psyche distinguishability

### Witnessed from `e06e4c07-...jsonl` (current session file)

**User record:**
```
{
  "type": "user",
  "message": {"role": "user", "content": [{"type": "text|tool_result", ...}]},
  "origin": {"kind": "human"} | {"kind": "task-notification"} | {},
  "userType": "external",
  "uuid": "<per-message uuid>",
  "parentUuid": "<previous message uuid>",
  "sessionId": "...",
  "cwd": "...",
  "gitBranch": "..."
}
```

**Assistant record:**
```
{
  "type": "assistant",
  "message": {"role": "assistant", "content": [{"type": "thinking|text|tool_use", ...}]},
  "origin": {},
  "uuid": "...",
  "parentUuid": "...",
  "sessionId": "..."
}
```

**Content item types by role (witnessed counts in current session file):**

| Role | Content type | Count |
|---|---|---|
| user | text | 9 |
| user | tool_result | 73 |
| assistant | text | 26 |
| assistant | thinking | 47 |
| assistant | tool_use | 73 |

### Are the psyche's typed messages distinguishable?

**Partially, but not cleanly.** The `origin` field is the key discriminator:

- `{"kind": "human"}` — the living psyche typed this directly (4 records in the current session)
- `{"kind": "task-notification"}` — a subagent completion injected this (6 records)
- `{}` — system-injected: skill text, hooks, `<system-reminder>` blocks, and everything the harness prepends (293 records — the vast majority)

All of these appear as `message.role == "user"` in the JSONL. The `origin: {}` records include the psyche's task prompt (delivered by the harness, not typed live) as well as all injected context. There is no field that definitively marks "this text originated in the psyche's mind right now" vs "this was the task brief injected at session start."

**Practical implication:** To find psyche rulings in session transcripts, search for `origin.kind == "human"` user messages, or search assistant text blocks for the agent's synthesis of a ruling. The psyche's actual live words are a small fraction of the volume; most "user" text is harness-injected context.

---

## Summary of witnessed file locations

| Harness | Session file pattern | Index/history | Session term |
|---|---|---|---|
| Claude Code | `~/.claude/projects/<encoded-cwd>/<uuid>.jsonl` | `~/.claude/history.jsonl` | "conversation" / "session" |
| Codex | `~/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl` | `~/.codex/session_index.jsonl` | "rollout" / "session" |
| Pi | `~/.pi/agent/sessions/<encoded-cwd>/<ts>_<uuid>.jsonl` | `~/.pi/agent/run-history.jsonl` | "session" |
