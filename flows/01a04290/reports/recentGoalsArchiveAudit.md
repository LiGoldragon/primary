# Recent goals and archive-readiness audit

Snapshot: 2026-08-27. This is a present-state audit, not an authorized retention design or implementation.

## Checkable recent window

The window is the connected research tree rooted at Codex `01a04236-2355-7d20-94aa-e3b814a52b32` through audit root `01a0428b-fc0e-7200-904e-2e2991e5425f` and worker `01a04290-0178-7f41-bf68-5c3769174607`.

It includes every descendant of `01a04236`, including `01a04285`. It excludes same-day threads attached to other roots. Persisted `thread_spawn_edges` therefore make “all goals” checkable without treating chronological proximity as relevance.

## Goal status

| Codex thread / Flow record | Aim | Status at audit | Evidence |
|---|---|---|---|
| `01a04236…` / `flows/01a04236` | Archive, hidden transcript data, size/schema, subflow lifecycle, compact access | Research complete; no retention implementation authorized. Later remote-publishing goal is not verified complete. | Root aim, Flow log, schema report |
| `01a04237…242c` / `flows/01a04237` | Archive lifecycle | Complete as investigation. Archived-parent/child local observation remains open. | `archiveLifecycle.md`, four witnesses, final response |
| `01a04237…4416` / no own Flow directory | Schema and size analysis | Substantive evidence complete; provenance representation is defective. Its report/witness are under parent Flow `01a04236`. | `codexTranscriptSchema.md`, `transcriptSchemaSizes.md`, child final |
| `01a04237…6379` / `flows/01a042376379` | Compact retention design | Complete as design only. Policy, ACL, expiry, resume, and identity questions remain open. | `compactRetention.md`, `retentionInventory.md`, final |
| `01a04285…` / no Flow artifact | Visual/social-card and hub publication follow-on | Unknown, likely unfinished. The root final said publishing awaited a production URL. | Root final; no Flow directory |
| `01a0428b…` / `flows/01a0428b` | Goal-status/archive-readiness audit and visual | In progress when audited. | Flow log; `primary-z88` |
| `01a04290…` / `flows/01a04290` | Terra evidence assembly | Findings complete. The parent materialized the artifacts because the worker could not edit. | Worker probes and returned report |

No native Codex goal state was found. A direct search of all seven in-window rollouts found no `create_goal`, `get_goal`, `update_goal`, or `update_plan` record. Their aims are transcript and Flow facts, not native goal objects.

Bead `primary-z88` is independently in progress at the audit snapshot. A Bead is tracking state, not proof that an individual session aim is complete.

## Archive compatibility

| Concern | Compatibility | Evidence and limit |
|---|---|---|
| Flow logs, witnesses, reports, reviewed psyche | Compatible | Archive affects `/home/li/.codex`; Flow artifacts are separate workspace files. This is storage separation, not a tested restoration path. |
| Exact raw Codex provenance | Compatible, presently plain JSONL | One archived rollout has 21 parseable JSONL records and is absent from its dated active path. Archive source uses rename plus SQLite metadata. |
| Active UI/resume-list clutter | Compatible | Source shows an archived row and preview are removed from the active picker; default `thread/list` omits archived rows. No fresh UI gesture was performed. |
| Archived discovery | Conditional | Source supports archived listing and unarchive; direct database state has `archived=1` plus an archived path. `session_index.jsonl` lacks the archived thread. |
| Search during remembering | Conditional and presently weak | Archived JSONL remains manually searchable with `rg`/`jq`. The deployed skill specifies typed-message-first retrieval, but the local `transcript` executable is absent and no scalable archived-search index was found. |
| Resume | Not directly witnessed | CLI accepts a session UUID/name; source establishes that unarchive restores active dated storage. Exact archived-session resume behavior was not exercised. |
| Parent/subflow archive | Conditional | Source tests establish descendant traversal and partial failure. Local state has no archived parent/child pair, so atomic subtree archival must not be inferred. |
| Provenance identity | Incompatible with the current eight-hex Flow convention | Three children begin `01a04237`; one Flow used extended `01a042376379`, while another worker's artifacts landed in the parent directory. Archive does not cause the collision, but compact references cannot key solely on eight hex characters. |

## Evidence boundaries

### Observed

- Codex archive preserves a rollout as local JSONL in `archived_sessions`; it does not itself compress, rewrite, or delete it.
- Current Flow artifacts already form a compact recall surface: index lines, logs, reports, witnesses, and reviewed psyche records.
- The related research tree produced the requested archive-lifecycle, schema/storage, and compact-retention reports.
- The audit window had seven Codex threads but only four related Flow directories before this worker record was materialized; short-ID collision prevents a one-to-one mapping.

### Source-confirmed claim

Codex `0.149.1` archives via `thread/archive`, moves files, updates thread metadata, hides archived rows from default active listing, and supports unarchive. A separate cold worker may later zstd-compress active or archived rollouts.

### Inference

Current remembering works after archive for ordinary depth-one recall because it starts with Flow logs/reports and can still reach raw JSONL by archive path. It is not robust yet for required transcript-depth remembering because discovery/search and stable session-to-Flow identity are not defined end to end.

### Unknown

- Resume requirements after archive or cold compression.
- Retention authority, expiry, deletion, holds, ACLs/encryption, backup policy, and recovery proof.
- A canonical collision-safe mapping among Flow, parent thread, child thread, and artifact directory.
- Whether the hub/social-card publication finished.
- Post-archive child visibility in a real parent/subflow archive.

## Current visual and report convention

The written psyche rule is ASCII in a conversation response and Mermaid in an artifact. The current compact human-reference convention is Flow `index.md` plus `log.md` plus reviewed psyche, with reports and witnesses providing deeper evidence.

A scalable retention system is not yet an accepted protocol. Its schema should not be placed in `AGENTS.md`. If the living later authorizes it:

- the eventual retention component's `ARCHITECTURE.md` should own system shape, invariants, identity, recovery, privacy, and lifecycle;
- the `flows` skill should hold only agent procedure and point to that architecture;
- this audit remains in its Flow directory rather than becoming canonical protocol documentation.

## Proposed reference fields

`thread_uuid`, `flow_artifact_id`, `parent_uuid`, `aim`, `status`, `status_basis`, `evidence_kind`, `archive_state`, `resume_evidence`, `remembering_depth`, `open_questions`, and `identity_collision`.

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
- `flows/01a04290/witnesses/recentGoalsArchiveAudit.md`
- `flows/index.md`
- `psyche-raw/Vision/visuals.md`
- `flows/b675f3d9/vision/remembering.md`
- `.agents/skills/flows/SKILL.md`
- `.agents/skills/transcript-search/SKILL.md`
- `.agents/skills/documentation-placement/SKILL.md`
- `/home/li/.codex/state_5.sqlite`
- `/home/li/.codex/sessions/`
- `/home/li/.codex/archived_sessions/`
- `/home/li/.codex/session_index.jsonl`
- `/git/github.com/openai/codex`, especially the source paths named in the witness methods.
