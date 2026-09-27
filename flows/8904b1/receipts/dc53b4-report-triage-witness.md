# dc53b4 recovery report: triage witness (subflow of 8904b1, 2026-09-27 ~01:17Z)

Read-only. Nothing launched, prompted, sent, registered, or repaired.

## Paths and hashes

- Report: `/home/li/primary/flows/dc53b4/reports/predecessor-recovery.md` (uncommitted; `git status` shows ` A`). Log: `/home/li/primary/flows/dc53b4/log.md` (51 lines, uncommitted). Bind receipt: `/home/li/primary/flows/dc53b4/receipts/stable-bind.md`.
- Nothing under `flows/dc53b4/` in `/home/li/wt/primary/56ae53`; `flows/56ae53/opus-recovery/` holds only the launch packet.
- dc53b4 native transcript: `/home/li/.claude/projects/-home-li-wt-primary-opus-sonnet-56ae53/dc53b4be-338b-4601-ab3c-a0e155fc8fa9.jsonl` (269 records, last 01:08:02Z). Subagents: 5 (a32aeb, a2d83a, a7fc9d, a0bdeb, a92883).
- 93ba9f transcript: `/home/li/.claude/projects/-home-li-primary/93ba9ff6-d24a-4dd0-a5c7-f98fab5ca9de.jsonl`, 1901 records; ruling message = line 1900, 2026-09-26T21:36:02.056Z; prior "Open for you" = line 1894, 21:35:17.674Z.
- Working questions: T93:897 (18:39:46.747Z), answered by 93ba9f at T93 ~898-905 (18:39:52Z); T93:1759 (21:18:18.506Z), answered at T93:1762 (21:18:24.530Z).
- 24 Sept living basis for ruling 1: `flows/836818/vision/flowNexus.md` line 33 ("If a message can't be delivered, then we try a higher power ... if there's nothing higher then we try lower."), typed comments to d8df70, 2026-09-24.
- Ruling 2 prompt: `flows/93ba9f/vision/messagingInterface.md` line 69 (typed artifact comment, 2026-09-26T21:04).
- Ruling 4 prompt: same file line 77-83 (STT, 2026-09-26; lists field report / psyche report / field question / psyche question).

## Searches for answers (all negative)

- `Mnema|Bearing|SendRejected|Toward` over every `*/flows/*/vision`, `/home/li/primary/flows/*/vision`: no hit.
- Typed user records after 21:30Z in b7ba00 (`b7ba0089-...`) and e167d8 (`e167d857-...`) transcripts: only task-notifications.
- Typed (non-machine) prompts in 8904b1, dc53b4, 38f337, b7ed066b transcripts: launcher text only.
- Codex user_message events in rollouts newer than 15:36 local (21:36Z) under `~/.codex-next/sessions`: none contain those words.
- Not searched: 56ae53's Codex rollout content beyond keyword user_message filter; artifact comments after the crash.

## Startup witness

- First user record: line 9, 2026-09-27T00:13:46.933Z, promptSource `typed`, CLI 2.1.280, cwd `/home/li/wt/primary/opus-sonnet-56ae53`. Content 57,786 bytes, sha256 `05f5dd46c778c9f58c5f69b083687a2687a50b2971096dc24758f788378b470e` (as extracted by jq -r).
- Expanded blocks: main-flow (lines 4-62), refresh (63-88), psyche-interraction (89-189); bodies byte-equal to SKILL.md in opus-sonnet-56ae53 (main-flow sha256 `119d98a9a290c3edbdbd8106b25b8fca03e8ec3551eb1582f68ff366293c82e2`, refresh `07b97916bfb3201eb41859a90279f6d66a94b7dd9471d1c560f99a6ebf0fe68b`, same hashes in 56ae53 tree).
- System prompt snapshot (replaced via `--system-prompt-file`): 1,527 chars, main-flow reminder text only, no skill bodies; sha256 `5ac5d94ebbab48d759bdaf1cdb87b18f40a5ea6c2de151ffefe38b4510fd5a06` — identical to 8904b1's.
- Attachments: skill_listing (92 skills, names and descriptions only), instructions (CLAUDE.md), no invoked-skill attachment.
- Tool uses over whole transcript: Agent 5, Bash 15, SendMessage 1, ToolSearch 1, Skill 0. 8904b1 transcript: Skill 0.
- Selection code: `tools/claude-native-seat-refresh.py` `startup_skills()` expands only `main-flow`, `psyche-interraction`, and skills with `disable-model-invocation: true`; brief sentence built at line ~693-694.
- Of the 21 declared, only main-flow and refresh carry `disable-model-invocation: true`.
- Batch launcher state `opus-sonnet-56ae53/flows/56ae53/opus-recovery/state.json`: phase `failed` at 00:11:48Z, `agent_not_ready`, same nativeThreadId, pane w1:pC. Fable packet `56ae53/flows/56ae53/fable-recovery/state.json`: failed the same way, but for a different UUID (b7ed066b), not 8904b1's.
- No bootstrap/native-start receipt file found for dc53b4; only the launcher's claim in its second prompt (00:15:15Z).

## Live readback, 2026-09-27T01:17:16Z

- `herdr pane get w1:pC`: agent_status done, title `PsycheV2.{ Opus dc53b4 }`, session dc53b4be-....
- `flow List`: `{ dc53b4 dc53b4be-... Claude Unavailable Available.{ default psyche_opus_dc53b4 w1:pC term_65c6bcb737eabc } ... Active }`.
- `hm-list`: dc53b4 psyche_opus_dc53b4 default done; heartbeat route Bound.
- Last usage: 01:08:02Z, input 91,842 tokens (incl. cache), model claude-opus-5-5.
