## BEADS audit — is it used, and exactly how it uses Dolt

### 1. Config / state files (`/home/li/primary/.beads/`)

| File | Content / meaning |
|---|---|
| `config.yaml` | Stock beads config, almost all commented out. The one live setting is `export.auto: false`. Comments confirm the two operating modes: Dolt-backed (default) vs `no-db` JSONL-only; and that JSONL backup auto-enables when a git remote exists. |
| `metadata.json` | `{database: dolt, backend: dolt, dolt_mode: embedded, dolt_database: primary, project_id: b4fe6b05-…}`. Embedded Dolt, database name `primary`. |
| `push-state.json` | `{last_push: 2026-06-09T19:28:17Z, last_commit: tdiv2v3impeagiisivj4cc57jfvuls75}`. Per-machine push high-water mark. |
| `README.md` | Upstream steveyegge/beads boilerplate. Confirms model: "Stored in Dolt database with version control and branching", `bd dolt push` syncs to a Dolt remote, "Dolt-native three-way merge". |
| `last-touched` | `primary-5top` — the last issue touched (a spirit NOTA bracket-string item, closed Jun 9). |
| `.gitignore` | Tells the story of the data model: `dolt/` managed by Dolt not git; `interactions.jsonl`, `push-state.json`, `backup/`, `ephemeral.sqlite3*` are runtime/local-only and not versioned. Note: it ignores `dolt/` but the actual db dir is `embeddeddolt/` — so this gitignore is largely vestigial for this layout. Config files (metadata.json, config.yaml) are intentionally git-tracked. |
| `.local_version` | `1.0.0` — local bd version marker to suppress upgrade-nag after git ops. |

### 2. `interactions.jsonl` — telemetry, not the issue store

- **639 lines**, one JSON object per line, 100% uniform shape: `{id, kind, created_at, actor, issue_id, extra}`.
- **Every record is `kind: field_change`** — an audit/interaction log of field mutations (e.g. `status: open → closed` with a free-text `reason`), NOT the issues themselves. The issues live in Dolt.
- Actors: 638 `li`, 1 `operator`.
- Timestamps span **2026-05-06T14:23 → 2026-06-09T19:28** (~34 days), covering 549 distinct issue IDs.
- Daily volume shows the usage curve: heavy May 9–24 (peaks of 70–80/day, a 189-record spike on Jun 1), then collapsing to 1–4/day in June, last entry Jun 9. This is interaction/telemetry logging that mirrors mutations applied to the Dolt store.

### 3. On-disk layout — a real Dolt repo

`embeddeddolt/primary/` is a genuine Dolt repository (261 MB total):

```
embeddeddolt/primary/.dolt/
  repo_state.json     head=refs/heads/main; remote origin=git+ssh://…/primary.git; backup_export=file://…/.beads/backup
  config.json         {}
  noms/               the chunk store:
    manifest          5:__DOLT__:<root>:p590…:000…:vvvv…:130734
    journal.idx       3.8 MB chunk index
    vvvvvvvv…vvv       138 MB journal chunk source (the live append journal)
    oldgen/           (empty — never compacted to oldgen here)
    LOCK
```

Dolt commands confirm a live, deep history (ran with `DOLT_ROOT_PATH` isolated to /tmp):

- `dolt status` → `On branch main, working tree clean`
- `dolt branch -a` → `* main` and `remotes/origin/main`
- `dolt remote -v` → `origin  git+ssh://git@github.com/LiGoldragon/primary.git` — a **Git remote**, via Dolt's git-remote integration, not a DoltHub remote.
- `dolt log` → **2031 commits**. Commit messages are bd-generated: `bd: create primary-iumz`, `bd: batch commit by li — 1 updated (+ events)`, `bd: tip (auto-commit) by li [claude_setup]`.
- **23 tables**, including `issues`, `comments`, `dependencies`, `labels`, `events`, `interactions`, plus a `schema_migrations` table at **version 23** (bd versions its own schema inside Dolt).
- `issues` table: **654 rows** — 546 closed, 99 open, 6 in_progress, 3 blocked.

### 4. Backup / push model

There are **two** sync paths configured in `repo_state.json`:

1. **`origin` (the real push):** a Git remote `git+ssh://git@github.com/LiGoldragon/primary.git`. `bd dolt push` serializes the Dolt commit graph and pushes it into the Gitolite-hosted `primary` repo. This is the off-machine durability path. `push-state.json` records `last_commit = tdiv2v3i…` and `last_push = Jun 9 19:28Z`, and that commit is exactly where `remotes/origin/main` points in the local log — so the local Dolt is two commits *ahead* of what was pushed.
2. **`backup_export` (local file backup):** a `file:///home/li/primary/.beads/backup` Dolt remote. `backup/` is itself a noms chunk store (288 `.darc` archive files, 86 MB, its own `manifest` + `backup_state.json`), written incrementally. `backup_state.json` = `{last_dolt_commit: g29e1vqf…, timestamp: 2026-06-10T22:15Z}` (the Jun 11 00:15 local-time tip). The cadence visible in `.darc` mtimes follows the commit rhythm (every batch commit emits an archive). It is content-addressed/append, so each archive is atomic, but the backup set as a whole is incremental, not a single atomic snapshot.

The two unpushed commits ahead of origin are **not** real work — `dolt diff origin/main..HEAD` shows the only change is one cell in the `metadata` table: `tip_claude_setup_last_shown` bumped `2026-06-08 → 2026-06-11`. That is bd's upgrade/setup-nag display marker, an automated heartbeat.

### 5. VERDICT — gone quiet (but not dead)

BEADS is **installed, functional, and was heavily used through late May, but has effectively gone quiet since Jun 9 2026.** Evidence:

- **Last real issue mutation:** Jun 9 19:28Z (`primary-5top` closed — "Resolved by spirit commit 20793846…"). Before that, the prior four real changes were Jun 7–8. The `interactions.jsonl` daily curve falls from 70–80/day in May to single digits in early June, last real entry Jun 9.
- **Last real Dolt content commit:** `tdiv2v3i…` ("bd: batch commit by li — 1 updated (+ events)"), Jun 9 21:28 — the same commit on `origin/main` and in `push-state.json`. The only newer commits (`8kks2sj…` Jun 9 23:24, `g29e1vqf…` Jun 11 00:15) are `bd: tip (auto-commit) … [claude_setup]` heartbeats touching only the nag-timestamp cell.
- **Last push off-machine:** Jun 9 19:28Z; the local db has not been pushed since.
- The state-file mtimes (`interactions.jsonl`, `push-state.json`, `last-touched` all Jun 9 21:27–21:28) corroborate Jun 9 as the last substantive activity. (The Jun 11 13:57/14:04 mtimes on `noms/manifest` and `journal.idx` are from **this audit's own `dolt` read commands**, not agent work.)

This is fully consistent with **INTENT.md §"BEADS is transitional"** (lines 102–107): "`.beads/` coordinates short-tracked items today; the destination is persona-mind's native typed work graph. Don't deepen the bd investment or build a bridge to it — design assuming it goes away. BEADS is never an ownership lock; any agent may create, update, or close items." Agents have evidently stopped reaching for it as active work moved into Spirit (the closing reasons reference spirit commits) — bead `primary-5top`'s closure literally points to a spirit commit as the resolution.

### 6. Dolt as the version-control reference design

What BEADS demonstrably proves about how Dolt version-controls a database on disk, from the live store:

- **Content-addressed chunk store (noms / "NBS"):** state lives in `noms/` as immutable, content-addressed chunks. Here storage is the **journal format**: a single append-only journal source (`vvvv…vvv`, the all-`v` filename is the journal table-file sentinel) plus a `journal.idx`. Compacted/sealed data would live as hash-named `.darc`/table files and migrate to `oldgen/` (empty here — this store has never compacted). The `backup/` remote shows the *table-file* form: 288 hash-named `.darc` chunk archives.
- **Manifest = the root pointer + chunk inventory.** The `manifest` line `5:__DOLT__:<storeRoot>:<gcGen>:<lock>:<table-or-journal>:<size>` names the format version (`5`), the store type (`__DOLT__`), the current database root hash, and the set of table files (the backup manifest lists every `.darc` with its chunk count). Swapping the root hash atomically advances the whole database — this is the atomic-commit primitive.
- **Commit graph over the chunks.** 2031 commits, each a content-addressed root referencing the prior commit, forming a Git-shaped DAG with `main` and `remotes/origin/main` refs. Branching/merge ("Dolt-native three-way merge") work table-by-table, row-by-row (the `dolt diff … --stat` output reports rows/cells added/modified/deleted).
- **Remote sync is push/pull of chunks + ref updates,** and crucially Dolt can target a **Git remote** (`git+ssh://…/primary.git`) — the chunk store is serialized into a git repo — as well as a plain `file://` remote (the local backup). So "version-control our own component databases" via the Dolt model = (a) a content-addressed chunk store with a journal that compacts into hash-named table files, (b) a manifest holding the atomic root pointer + chunk inventory, (c) a commit DAG with named refs, and (d) push/pull that ships chunks and moves refs, layerable on top of an existing Git host.

This maps cleanly onto the workspace's own durable-state plane intent (Sema = redb+rkyv typed kernel; sema-engine adds "operation log/snapshot identity"): Dolt's manifest-root + chunk store + commit DAG is the concrete reference for what a versioned snapshot-identity + operation-log shape looks like on disk, with the wrinkle that Dolt can ride on Git as transport.
