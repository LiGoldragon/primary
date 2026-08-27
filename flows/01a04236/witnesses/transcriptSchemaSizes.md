# Transcript schema and storage witness

Measurement date: 2026-08-27. The live Codex store was read without mutation; counts can increase while a session is running. Payload text, commands, prompts, URLs, paths inside payloads, and secrets were not copied into this witness.

## Methods

Method: probe `find /home/li/.codex/sessions -type f -name '*.jsonl' -printf '%s\\n'` plus `du -sxB1 /home/li/.codex/sessions`.

Method: probe a streaming JSON decoder over `/home/li/.codex/sessions/*/*/*/*.jsonl`, counting outer `type`, payload `type`, encoded byte length, string lengths, and SHA-256 prefixes only.

Method: probe `python sqlite3` read-only connections to `/home/li/.codex/thread_history_1.sqlite`, `/home/li/.codex/state_5.sqlite`, and `/home/li/.codex/logs_2.sqlite`; query schema, row counts, `length()` aggregates, and hashes/lengths of matched item outputs only.

## Storage

At the final storage pass, 1,606 rollout JSONL files occupied 4,062,623,476 logical bytes (3.784 GiB); filesystem allocation reported by `du` was 4,067,524,608 bytes (3.789 GiB). The parseable records accounted for 4,062,348,656 bytes and 926,791 records. One archived rollout was 48,969 bytes. The largest rollout was 40,379,564 bytes; median rollout size was approximately 1.07 MB.

Eighty-five physical lines failed JSON decoding in five files: 81 `Expecting value` errors in one live file and four `Unterminated string starting at` errors in four older files. All 85 invalid lines were excluded from parsed-record totals. Their presence establishes a file-integrity caveat, not the cause of the writes.

## Outer record schema and byte shares

Every successfully decoded line observed was an object with outer keys `timestamp`, `type`, and `payload`. Outer counts and logical bytes were:

| outer type | records | bytes | share of parseable bytes |
| --- | ---: | ---: | ---: |
| `event_msg` | 375,395 | 2,271,699,251 | 55.921% |
| `response_item` | 515,785 | 1,662,499,797 | 40.925% |
| `compacted` | 856 | 44,213,416 | 1.088% |
| `session_meta` | 2,027 | 38,657,428 | 0.952% |
| `world_state` | 8,441 | 36,483,476 | 0.898% |
| `turn_context` | 6,665 | 6,643,909 | 0.164% |
| `inter_agent_communication_metadata` | 17,622 | 2,151,379 | 0.053% |

The common `response_item` payload subtypes were `custom_tool_call`, `custom_tool_call_output`, `reasoning`, `function_call`, `function_call_output`, `message`, and `agent_message`. Common `event_msg` payload subtypes were `item_completed`, `token_count`, `patch_apply_end`, `task_started`, `task_complete`, `user_message`, `sub_agent_activity`, `thread_settings_applied`, and web/MCP/image events.

Nested schema witnesses include:

- `session_meta.payload`: session/thread IDs, parent/fork IDs when present, timestamp, cwd, source, thread source, model/provider, agent identity, history mode, context window, git metadata, base instructions, and occasional dynamic tools.
- `turn_context.payload`: turn ID, cwd, model, effort, date/timezone, collaboration settings, permission profile, sandbox policy, workspace roots, summary, and compaction hash.
- `world_state.payload`: `full` plus a `state` object containing environment, skills, host instructions, agent instructions, permissions, personality, collaboration, and plugin/application instruction state.
- `compacted.payload`: compaction window IDs, window number, a message field, and a `replacement_history` array containing prior message/reasoning-shaped objects.
- `response_item.*`: IDs and turn metadata plus message content arrays, reasoning encrypted content/summary, function/custom-tool call inputs, and call outputs.
- `event_msg.item_completed`: timing/thread/turn IDs plus an `item` object. `CommandExecution` items have command, cwd, duration, exit code, process/status fields, `stdout`, `stderr`, `aggregated_output`, `formatted_output`, and parsed command actions. `FileChange` items have change maps; agent/MCP/web/image items have their corresponding semantic result fields.

## Output volume, duplication, and references

A fresh scan found 36,875 `CommandExecution` `stdout` strings totaling 759,106,260 bytes; the maximum was 1,109,211 bytes at relative transcript `2026/08/26/rollout-2026-08-26T23-00-03-01a03fdf-71a8-72f1-ac86-e24109f0d930.jsonl`, line 228. There were 250 outputs in the approximately 1 MiB length band; common exact lengths were 1,048,607, 1,048,606, and 1,048,608 bytes. The `CommandExecution` schema had no explicit `truncated` boolean or reference field. Size plateaus are compatible with an output cap, but the transcript alone does not prove where truncation occurred. `formatted_output` can be much shorter than `stdout`, so it is a separate presentation field.

The same command item commonly carries both `stdout` and `aggregated_output`; a 300-item ID-matched sample found 283 exact duplicate strings and 17 wrapper/substring-related cases when compared with the UI projection. In an adjacency scan, 30,112 command-completion records were followed immediately by a `response_item.custom_tool_call_output`; 25,692 non-empty outputs contained the command `stdout` as a substring. This is evidence of inline duplication across raw event and model-facing records, with a small wrapper difference, not a claim that every record follows one exact sequence.

Model-facing output string totals were 782,722,916 bytes across 98,146 `custom_tool_call_output` text values (maximum 78,683 bytes) and 95,213,732 bytes across 50,409 `function_call_output` text values (maximum 240,154 bytes). These are inline strings, usually in an output array of typed text/image parts; they are not path references.

Image generation is a separate reference-plus-inline case: nine `image_generation_end` results were base64-like inline strings from 2.31 MB to 5.15 MB, each with a `saved_path` that existed at measurement. Seventy-nine transcript `image_url` values were all data URLs totaling 79,859,414 bytes. The generated-image store contained 35 files totaling 97,821,450 bytes. Thus images can be duplicated as inline transcript data, data-URL message parts, and on-disk files.

## UI projection versus transcript-only data

The UI-related state database had 2,465 thread rows (2,464 unarchived, one archived), 1,593 spawn-edge rows, and 1,816 legacy versus 649 paginated history-mode threads. `thread_history_1.sqlite` was 947,499,008 bytes at measurement, with 111,960 `thread_items` rows and 849,012,661 bytes of `item_json`; its 649 distinct projected threads expose semantic item types such as `commandExecution`, `fileChange`, `agentMessage`, `reasoning`, `mcpToolCall`, `webSearch`, `collabAgentToolCall`, `subAgentActivity`, `userMessage`, and `contextCompaction`. `commandExecution` alone occupied 820,308,254 `item_json` bytes across 34,564 rows, with transformed `aggregatedOutput` fields.

The raw transcript has hundreds of thousands of `token_count`, context, world-state, inter-agent, timing, compaction, and other event records that do not appear as `thread_items` types. The projection therefore appears to be the UI-facing semantic history, while the raw JSONL retains telemetry, context snapshots, encrypted reasoning, and intermediate protocol records. This UI interpretation is an inference from the schemas and IDs, not a direct screen inspection. `logs_2.sqlite` was 779,255,808 bytes and held 433,542 application-log rows; it is separate from both the JSONL and history projection.

## Subflow comparison

Using each rollout's first `session_meta`, 1,442 of 1,606 files (3,787,899,085 logical bytes, approximately 93.3% of the session store) were marked as subflows by `thread_source=subagent` or a structured subagent source. The remaining 164 files totaled 274,734,677 bytes. Subflow metadata adds parent/fork identity, agent path/role, and source details; records also use `agent_message`, `sub_agent_activity`, and inter-agent metadata. The same outer JSONL and semantic item schema is used; subflows are not stored in a separate transcript format. `state_5.sqlite.thread_spawn_edges` supplies parent/child links. Exact spawn completion/retention semantics were not established here.

## Unknowns

The observations do not establish the writer's flush/rotation algorithm, whether the 85 invalid lines are transient or durable, the exact truncation boundary/marker policy, which projection fields every UI surface renders, server-side retention, or whether any external sync holds another copy. No deletion, compaction, migration, or configuration change was attempted.

## Sources

- This flow's witness: `flows/01a04236/witnesses/transcriptSchemaSizes.md`.
- Direct local witnesses: `/home/li/.codex/sessions/`, `/home/li/.codex/archived_sessions/`, `/home/li/.codex/thread_history_1.sqlite`, `/home/li/.codex/state_5.sqlite`, `/home/li/.codex/logs_2.sqlite`, and `/home/li/.codex/generated_images/`.
- Schema/record method: streaming JSON decoding and structural aggregation over the local rollout paths; payload values were not emitted.
