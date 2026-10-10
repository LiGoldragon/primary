# Aggregator-only broken Claude session recovery

## Scope and rule followed

I used the deployed `aggregator`/`meta-aggregator` path for recovery evidence. After aggregator attempts were exhausted, I checked only path existence, names, permissions, sizes, and timestamps for backing files. I did not read transcript JSONL or `.output` bodies directly.

## Aggregator operations attempted and results

- `aggregator` with `(Version (None))`: succeeded, reporting `signal-aggregator 0.4.0`.
- `aggregator` with `(ObserveHealth (recovery-health-1))`: succeeded. Health reported:
  - Claude root `/home/li/.claude/projects/-home-li-primary`: `DiscoveryTruncated`, `discovered_files=105878`, `indexed_records=105878`, `malformed_records=128`.
  - Claude subagent output root `/tmp/claude-1001`: `UnreadableRoot`, `discovered_files=18`, `indexed_records=18`, `unreadable_records=128`.
  - Index: `ReadableIndexed`, `session_count=985`, `subagent_count=0`, `output_count=105896`, `transcript_block_count=105936`.
- `ListSessions` for Claude sessions since `2026-07-07T00:00:00Z`: returned zero sessions.
- `ListSessions` newest Claude sessions without a time filter: returned sessions only up to `2026-07-05`; the known broken `a2018f45-014c-45ef-9483-b9e5c9c0f086` session was not visible in the returned newest page.
- `SearchTranscriptBlocks` for `quota` and `rate_limit`: both rejected with `OperationRejected ... Oversized` on the same transcript block reference before useful matches were returned.
- `ListOutputs` for `ClaudeSubagentOutput`: returned 18 indexed output cards, but they were for other sessions/paths and mostly repeated one task path; no target broken-session outputs were returned.
- `ListOutputs` for Claude outputs since `2026-07-07T00:00:00Z`: returned zero outputs.
- `ListOutputs` with bounded previews: timed out after 30 seconds.
- `Collect` for Claude since `2026-07-07T00:00:00Z`, metadata-only and limited: returned no transcript segments and no output artifacts; it returned many read failures and request-limit entries for other paths, not the target broken session.

## Broken session summary

Aggregator could not produce an evidence-backed summary of the broken Claude session. The known quota event around `2026-07-07T16:05:08` and the known file `/home/li/.claude/projects/-home-li-primary/a2018f45-014c-45ef-9483-b9e5c9c0f086.jsonl` were not discoverable as a session, transcript block, output, or evidence package through the deployed aggregator operations I tried.

Partial summary from non-aggregator prompt context only: the session ended because Claude API returned `rate_limit`/HTTP `429` with “You've hit your session limit · resets 8:30pm (Europe/Tirane)”. Because this fact was supplied in the task prompt, not recovered through aggregator, it should not be treated as aggregator-backed recovery evidence.

Exact missing aggregator evidence: a session card for `a2018f45-014c-45ef-9483-b9e5c9c0f086`, bounded transcript blocks around the quota failure, task/subagent metadata for the affected subagents, and readable bounded output excerpts for the unfinished subagents.

## Per-subagent recovery

- `agent-ab35d7d3b3fe2b7da` (“Implement everywhere-gate semantics”): aggregator did not provide a subagent card, task result, transcript blocks, or output text. Missing: indexed task metadata and bounded readable output/transcript excerpts.
- `agent-a26c57dc4305aa1f8` (“Scratch mirror typecheck grind”): same blocker; no aggregator-backed recovery summary was possible.
- `agent-a3c78b5bcea8ae091` (“Contract-crate schema toolchain migration”, believed complete from earlier context): aggregator did not expose completion evidence for this target session, so completion cannot be confirmed through aggregator.

## File-presence check summary, metadata only

- Known session file exists: `/home/li/.claude/projects/-home-li-primary/a2018f45-014c-45ef-9483-b9e5c9c0f086.jsonl`, regular file, mode `-rw-------`, size `1,152,268`, mtime `2026-07-08 10:25:14 +0300`.
- Target subagent transcript directory exists: `/home/li/.claude/projects/-home-li-primary/a2018f45-014c-45ef-9483-b9e5c9c0f086/subagents`, mode `drwxr-xr-x`; it contains JSONL names for `agent-ab35d7d3b3fe2b7da`, `agent-a26c57dc4305aa1f8`, and `agent-a3c78b5bcea8ae091`.
- `/tmp/claude-1001` exists, mode `drwx------`; `/tmp/claude-1001/-home-li-primary/a2018f45-014c-45ef-9483-b9e5c9c0f086/tasks` exists.
- Target `.output` symlinks exist for `ab35d7d3b3fe2b7da`, `a26c57dc4305aa1f8`, and `a3c78b5bcea8ae091`. Following symlinks, targets are regular mode `-rw-------` with sizes `3,448,486`, `883,704`, and `986,443` bytes respectively.

## Aggregator shortcomings and needed features

### Product/API capability gaps

- Need direct lookup by known transcript path, session UUID, subagent id, and task/output filename.
- Need a “summarize recovery bundle” operation that returns bounded blocks around failure events plus per-subagent status metadata.
- Search should skip or report oversized blocks and continue, not abort the whole search.
- Need bounded tail/head reads by session/subagent path when a fragile reference is unavailable.
- Need subagent cards for Claude transcript subagents; health currently reports `subagent_count=0` despite subagent files existing.

### Configuration/path-derivation/deployment gaps

- Deployed indexing does not derive or expose the known July 7 session even though backing files exist.
- Claude subagent output root is marked `UnreadableRoot` even though the relevant derived `/tmp/claude-1001/-home-li-primary/.../tasks` path and symlinks exist.
- Output indexing appears to include stale or unrelated task paths while missing the target session outputs.

### Health/indexing/limit gaps

- `DiscoveryTruncated` on the primary Claude root blocks confidence in recency and completeness.
- List operations showed no July 7 sessions/outputs despite target files existing.
- `Collect` reported request limits and many malformed read failures, but did not explain how to reach the target file.
- Preview listing timed out, suggesting index operations need bounded latency guarantees.

### Privacy/safety concerns

- Existing bounded-read concepts are good, but direct path/session lookup must preserve explicit byte limits and metadata-only defaults.
- Search failure reports should avoid leaking unrelated path inventories unless requested; `Collect` emitted many unrelated malformed file paths.

## Recommended next action

Fix aggregator discovery/path derivation first: make the known session path and `/tmp/claude-1001/-home-li-primary/<session>/tasks/*.output` indexable and retrievable by stable lookup. Then rerun this recovery using direct session lookup, bounded transcript search around `2026-07-07T16:05:08`, and bounded per-subagent output reads.
