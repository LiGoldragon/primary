# Compact-retention inventory witness

Method: read-only filesystem inventory of transcript/artifact directories; counted files and bytes by extension/name class, without printing transcript text.

Method: inspected representative JSONL structure with `jq`/metadata-only aggregation, and measured `gzip -1` output for selected largest files. These are samples, not corpus averages.

Method: inspected authored transcript-search, flow, psyche, and prior report records; read each requested prior flow log, pertinent vision, and last model response at depth 1.

Snapshot: 2026-08-27 local state. Live files can change while a session runs; counts are not a deletion or expiry recommendation.

## Inventory

- Claude project `/home/li/.claude/projects/-home-li-primary`: 3,408 files, 786,585,206 bytes. JSONL is 1,520 files / 532,859,893 bytes (98 root files / 110,427,055 bytes; 1,422 nested subagent files / 422,432,838 bytes). Auxiliary `.jsonl.bak-*` is 1 / 82,807,451 bytes; `tool-results` is 461 / 170,669,993 bytes; `.meta.json` is 1,422 / 242,189 bytes. The auxiliary backup plus tool-results class is 253,477,444 bytes (32.2% of this project), but its reference/hold safety was not established.
- Codex `/home/li/.codex/sessions`: 1,606 JSONL files, about 4,057,576,722 bytes (live count). Largest observed file is 40,379,564 bytes. `session_index.jsonl` is 65 lines / 8,226 bytes; `history.jsonl` is 7,432 lines / 5,848,274 bytes and contains text, so indexes are not automatically non-sensitive.
- Pi `/home/li/.pi/agent/sessions`: 1,283 files, 929,902,041 bytes; JSONL is 1,274 / 929,845,071 bytes.
- Pi subagent artifacts `/home/li/primary/.pi-subagents/artifacts`: 5,129 files, 1,206,417,129 bytes. Transcript JSONL is 1,281 / 1,190,161,181 bytes; sidecar input/output/meta classes together are 16,092,174 bytes. Sidecars are compact continuation metadata but do not by themselves retain exact event provenance.
- Combined harness/session/artifact total in this inventory is about 6,980,481,098 bytes (6.50 GiB). Flow artifacts `/home/li/primary/flows` are 684 files / 2,537,906 bytes: logs 119 / 282,552; vision 236 / 407,562; witnesses 140 / 487,603; reports 150 / 1,342,389; annotations 43 / 19,247; index PNG/other remainder. The flow layer is already only about 0.036% of the combined raw archive.

## Structure and duplication witnesses

- Current Codex records include `session_meta`, `event_msg`, `response_item`, `turn_context`, `world_state`, `compacted`, and inter-agent metadata. Response payloads include reasoning (summary plus encrypted content), messages, function calls/outputs, custom tool calls/outputs, and agent messages. One current parent sample had 524 token-count events costing 417,614 bytes (11.7% of that 3,572,752-byte serialized payload).
- An older Codex sample was 40,314,228 serialized bytes; `event_msg/item_completed` occupied 36,768,404 bytes (91.2%), including 184 command executions. In all 184 sampled executions, `stdout` equaled `aggregated_output`; their fields totalled 16,226,340 bytes. This proves a duplicate in that schema/version, not that every rendered/raw output field is interchangeable.
- Representative gzip-1 sizes: old Codex 40,379,564 to 8,620,090 bytes (21.3% retained); current Codex parent 3,578,512 to 1,619,816 (45.3% retained); Claude root 5,664,866 to 1,785,142 (31.5% retained); Claude subagent 2,881,131 to 809,693 (28.1% retained); Pi 10,397,980 to 7,650,516 (73.6% retained); Pi artifact 10,871,696 to 7,701,110 (70.8% retained). Savings range from 26% to 79% in these samples and must not be generalized.
- The deployed `transcript-search` skill describes typed-message-first search and line-addressed raw retrieval, but the `transcript` executable was not found in this setup. `ccusage` and standalone `sqlite3` commands were also absent. `rg`, `jq`, `gzip`, and `zstd` were available. This is a setup/tooling observation, not evidence that the authored search design is invalid.

## Safety/lineage observations

- A content-addressed blob can be a storage address, but it must not be silently treated as a psyche record ID: authored psyche records distinguish raw records, reviewed distilled records, archives, and chain-of-origin references.
- The inventory-health recovery record says failed/truncated/resumable inventory must be resolved before garbage collection. This makes external references, integrity manifests, and hold checks prerequisites to any expiry proposal.
- A subflow is a flow and can remain active through its subflows; parent closure alone is not proof that child transcript material is idle.
