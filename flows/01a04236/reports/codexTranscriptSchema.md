# Codex transcript schema and storage

Measurement: 2026-08-27, local read-only scan. The store was live, so counts can grow while sessions run. Payload text, commands, prompts, URLs, and secrets were not emitted.

## Observations

`/home/li/.codex/sessions` contained 1,606 rollout JSONL files: 4,062,623,476 logical bytes (3.784 GiB), with 4,067,524,608 bytes allocated by `du` (3.789 GiB). One archived rollout was 48,969 bytes. The largest rollout was 40,379,564 bytes; the median was about 1.07 MB. The parseable portion was 926,791 records and 4,062,348,656 bytes. Eighty-five physical lines failed JSON decoding in five files (81 `Expecting value`, four `Unterminated string starting at`) and were excluded from parsed totals.

Every successfully decoded line was an object with outer keys `timestamp`, `type`, and `payload`. Outer record byte shares were:

| type | records | bytes | share |
| --- | ---: | ---: | ---: |
| `event_msg` | 375,395 | 2,271,699,251 | 55.921% |
| `response_item` | 515,785 | 1,662,499,797 | 40.925% |
| `compacted` | 856 | 44,213,416 | 1.088% |
| `session_meta` | 2,027 | 38,657,428 | 0.952% |
| `world_state` | 8,441 | 36,483,476 | 0.898% |
| `turn_context` | 6,665 | 6,643,909 | 0.164% |
| `inter_agent_communication_metadata` | 17,622 | 2,151,379 | 0.053% |

Common `response_item` payload subtypes are messages, reasoning, function/custom-tool calls and outputs, and agent messages. Common `event_msg` subtypes are completed semantic items, token counts, patch results, timing, user messages, sub-agent activity, web/MCP/image events, and settings. `session_meta` contains thread/session IDs, parent/fork IDs when present, cwd, source, model/provider, agent identity, history mode, context window, git metadata, base instructions, and occasional dynamic tools. `turn_context` contains turn/model/permission/sandbox/workspace state. `world_state` contains environment, skills, host/agent/plugin instructions, permissions, collaboration, and personality state. `compacted` contains compaction window IDs and replacement history.

`event_msg.item_completed` `CommandExecution` items contain command, cwd, timing, exit/status fields, `stdout`, `stderr`, `aggregated_output`, `formatted_output`, and parsed command actions. `FileChange`, MCP, web, image, agent, and user items use corresponding structured fields. The common output parts are inline strings or typed text/image arrays.

## Outputs and duplication

A fresh scan found 36,875 `CommandExecution` `stdout` strings totaling 759,106,260 bytes; maximum 1,109,211 bytes at `2026/08/26/rollout-2026-08-26T23-00-03-01a03fdf-71a8-72f1-ac86-e24109f0d930.jsonl` line 228. 250 outputs were in the approximately 1 MiB band, with repeated lengths around 1,048,606–1,048,608 bytes. The command item schema had no explicit `truncated` boolean or reference field. These plateaus are compatible with a producer cap, but exact truncation behavior is unknown; `formatted_output` is a separate, often shorter presentation field.

Model-facing output strings totaled 782,722,916 bytes across 98,146 `custom_tool_call_output` text values (maximum 78,683 bytes at `2026/07/26/rollout-2026-07-26T23-38-14-019fa05d-4537-7500-8540-37a068de7668.jsonl` line 74), and 95,213,732 bytes across 50,409 `function_call_output` text values (maximum 240,154 bytes at `2026/07/26/rollout-2026-07-26T18-56-28-019f9f5b-4ba4-7671-9f00-023e982f063b.jsonl` line 576). In a 300-item ID-matched sample, raw command `stdout` and the UI projection's `aggregatedOutput` were exact duplicates for 283 items; the other 17 were wrapper/substring-related. An adjacency scan found 30,112 command completions followed by a custom-tool output; 25,692 non-empty outputs contained the command `stdout` as a substring. This establishes inline duplication across layers, with a wrapper difference.

Images also show reference-plus-inline duplication. Nine `image_generation_end` results were base64-like inline strings from 2.31–5.15 MB and each had an existing `saved_path`. Seventy-nine transcript `image_url` values were data URLs totaling 79,859,414 bytes. The generated-image directory held 35 files totaling 97,821,450 bytes.

## UI projection and subflows

`state_5.sqlite` held 2,465 threads (2,464 unarchived, one archived) and 1,593 parent/child spawn edges; history modes were 1,816 legacy and 649 paginated. `thread_history_1.sqlite` was 947,499,008 bytes and held 111,960 semantic `thread_items` rows with 849,012,661 bytes of `item_json` across 649 projected threads. Its largest item class was `commandExecution`: 34,564 rows and 820,308,254 bytes, including transformed `aggregatedOutput`. This projection appears UI-facing from its semantic item types and joins, while raw JSONL retains telemetry, context snapshots, encrypted reasoning, compaction and protocol records that are not represented as `thread_items`; that UI interpretation is an inference, not direct screen inspection. `logs_2.sqlite` was a separate 779,255,808-byte application log store.

Using first-record `session_meta`, 1,442 of the 1,606 rollout files were marked subflows (`thread_source=subagent` or structured subagent source), totaling 3,787,899,085 bytes (about 93.3% of session storage). The remaining 164 files totaled 274,734,677 bytes. Subflows use the same outer and semantic schema, with parent/fork identity, agent path/role, source metadata, agent messages, sub-agent activity, and inter-agent metadata. They are not a separate file format.

## Inferences and unknowns

The raw event plus model-facing output plus SQLite projection means a single command result can occupy several inline representations. A compact-retention design would need to preserve semantic item identity and selected outputs while deciding separately what to do with telemetry, context snapshots, encrypted reasoning, image data, and malformed records. Exact writer flush/rotation behavior, the cause and durability of malformed lines, truncation markers/caps, UI rendering choices, and server/external retention remain unknown. No deletion, compaction, migration, or configuration change was attempted.

## Sources

- Detailed methods and redacted structural witnesses: `flows/01a04236/witnesses/transcriptSchemaSizes.md`.
- Direct local stores: `/home/li/.codex/sessions/`, `/home/li/.codex/archived_sessions/`, `/home/li/.codex/thread_history_1.sqlite`, `/home/li/.codex/state_5.sqlite`, `/home/li/.codex/logs_2.sqlite`, and `/home/li/.codex/generated_images/`.
- Evidence method: streaming JSON decoding and read-only SQLite schema/length/hash aggregation; payload values were not copied.
