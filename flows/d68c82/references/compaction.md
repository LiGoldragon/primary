# Compaction: references

Research for a knowledge-review book on context compaction. Gathered 2026-10-16.
Markers: **[doc]** = stated by official documentation; **[src]** = read in source code at the named version; **[bundle]** = read in the installed minified Claude Code bundle; **[module]** = already stated by the `knowledge-compaction` module (verified there on 2026-10-13).

Network note: github.com and developers.openai.com were unreachable from the shell and (for developers.openai.com) from WebFetch. Codex and pi were read from local clones at local tags; OpenCode via raw.githubusercontent.com; OpenAI API facts via the generated `openai-python` SDK types on raw.githubusercontent.com (generated from OpenAI's OpenAPI spec) plus a web-search summary of the guide.

## Earlier book

- `flows/d68c82/books/10-what-compaction-keeps.md` (and `.html`), «What compaction keeps», by Psyche Core Secondary, 2026-10-13. Published: https://claude.ai/artifact/7nx5nPQRN8N8FMZ4XhaD6P (listed in `flows/d68c82/books/index.html` line 41; its two proposals were withdrawn in favour of «Flow: refresh and handover»).
- Related: «A guarded compaction request», second edition, by Fable, 2026-10-13: https://claude.ai/artifact/LwF4EsZcL3CChqbobHjqYJ (index line 37); sources `flows/33752b/books/40-compaction-request.md`, `42-compaction-request-2.md`.
- The earlier book claimed for Claude Code: only 13 to 26 of 91 to 156 user messages per stretch survived whole in the summary; for Codex, "about nine in ten" user messages kept verbatim, trigger ~224k of 258k.

## Existing module: knowledge-compaction

Authored source: `mind-context` skills (loaded through the Skill tool; generated copy at `/home/li/primary/.claude/skills/knowledge-compaction`). Verified 2026-10-13 against Claude Code 2.1.294 and Codex 0.161.0-alpha.2. Key claims: Claude Code summary is a forked single-turn call, nine-section format, preserved tail (last assistant reply), restored files (5 files, 5,000/file, 50,000 total), skills (5,000/skill, 25,000 total); Codex remote V2 keeps newest user/hook and eligible inter-agent messages within 64,000 tokens, agent messages >10,000 tokens excluded, encrypted compaction item; local path keeps recent user text within 20,000 tokens; auto limit capped at 90% of context window.

## Answer table: are ALL user messages kept verbatim?

| Harness / provider | Trigger | What is summarised | User messages kept | What else is re-injected |
|---|---|---|---|---|
| Claude Code 2.1.294 | auto at effective window − 13,000, effective = window − min(max output, 20,000) (≈967K on 1M models) [bundle][doc]; `/compact [focus]` | whole history (full path) by forked single call; 9-section prompt incl. "List ALL user messages that are not tool results" — not "verbatim", no cap [bundle] | **none verbatim** on full path (`messagesToKeep:[]`); only a summary paraphrase; reactive/partial paths keep a recent tail of rounds verbatim [bundle] | system prompt, CLAUDE.md, memory unchanged; ≤5 files (5K each, 50K total); skills 5K each, 25K total; plan; background tasks; SessionStart `compact` hook [bundle][doc] |
| Anthropic API threshold (`compact_20260112`, beta `compact-2026-01-12`) | input_tokens ≥ trigger, default 150,000, min 50,000 [doc] | everything before the compaction block; default prompt "varies by model" [doc] | **none** unless client uses `pause_after_compaction` and re-inserts turns [doc] | nothing; client-managed [doc] |
| Anthropic API on demand (`compact-2026-09-04`) | client decides [doc] | every message sent [doc] | **none** unless client keeps a tail ("No parameter sets which turns are kept") [doc] | nothing [doc] |
| Anthropic API context editing (`clear_tool_uses_20250919`) | default 100,000 input tokens; keep 3 tool uses [doc] | not a summary: old tool results replaced by placeholder [doc] | user messages untouched (only tool results/inputs/thinking cleared) [doc] | n/a |
| Codex 0.161.0 remote V2 (OpenAI providers) | auto at `auto_compact_token_limit`, default and cap 90% of window [src] | full history sent with `CompactionTrigger` item; server returns encrypted compaction item [src] | **capped**: newest user/hook (+ eligible ≤10,000-token agent) messages within `RETAINED_MESSAGE_TOKEN_BUDGET = 64_000`; boundary message truncated, older dropped [src] | initial context (instructions, AGENTS.md, env) reinjected mid-turn before last user message, or on next turn [src] |
| Codex local (non-OpenAI providers) | same | readable summary from `prompt.md` [src] | **capped**: `COMPACT_USER_MESSAGE_MAX_TOKENS = 20_000`, newest first, boundary truncated [src] | same initial-context reinjection [src] |
| OpenAI API `/responses/compact` and `compact_threshold` | client-set `compact_threshold` [SDK type] | prior window into opaque `encrypted_content` [SDK type] | reference: output "is a list of all user messages, followed by a single compaction item" (no stated cap) [SDK type/doc]; guide is vaguer [search summary] | nothing documented |
| OpenCode 1.18.16 | count ≥ input limit − reserved (default min(20,000, max output)) [src] | everything before last 2 user turns; anchored-summary prompt, no verbatim request [src] | **capped**: last 2 turns within `min(8_000, max(2_000, usable/4))` tokens; after overflow the last user message is replayed [src] | none; optional pruning clears old tool output (`PRUNE_PROTECT = 40_000`) [src] |
| pi 0.80.10 | contextTokens > window − `reserveTokens` (16,384) [src][doc] | everything before `keepRecentTokens` (20,000) cut; rolling summary ≤ 0.8×reserve ≈13,107 tokens [src] | **capped**: only messages inside ~20,000 recent tokens [src] | read/modified file lists appended to the summary [src] |

## Claude Code (installed 2.1.294)

Binary: `/home/li/.nix-profile/bin/claude` wraps the native Bun executable `.../claude-code-2.1.294/bin/.claude-wrapped` (253 MB); JavaScript embedded as text. Offsets are byte offsets in that file; identifiers are minified names.

### Trigger [bundle]
- `qV`, `kLe`, `ZY`, `dse` (~213,272,830–213,277,300). Effective window = auto-compact window − min(model max output, 20000) (`Wxt=20000`). Threshold = effective − 13000 (`Pxt=13000`).
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (0–100) gives min(floor(effective×pct/100), effective−13000): can only lower it.
- Warning at threshold − 20000; hard block at window − min(max output, 20000) − 3000 unless `CLAUDE_CODE_BLOCKING_LIMIT_OVERRIDE`.
- Background summary may start at min(0.8×effective, threshold) (`ase=0.2`, flag-adjustable).
- Window source order (`Iv`): `CLAUDE_CODE_AUTO_COMPACT_WINDOW` env, `autoCompactWindow` setting, clientdata, experiment, model default (`z3=200000`, `lse=1e6`); capped at the model window.
- Disabled by `DISABLE_COMPACT` / `DISABLE_AUTO_COMPACT`; else `autoCompactEnabled` (default true). Circuit breaker after 3 consecutive failures; thrash check after 3 refills within 3 turns.

### Summary prompts [bundle] (~214,863,000–214,876,400)
- Arm selected by `Uge()`: env `CLAUDE_CODE_CURRIED_TRINKET`, else flag `tengu_curried_trinket`, default `control`. Arms: `control`, `lean`, `short`, `capped`. Which arm this account gets is unobserved.
- control (`Xsr`), nine sections: Primary Request and Intent; Key Technical Concepts; Files and Code Sections; Errors and fixes; Problem Solving; All user messages; Pending Tasks; Current Work; Optional Next Step. Section 6: "6. All user messages: List ALL user messages that are not tool results. These are critical for understanding the users' feedback and changing intent. Preserve any security-relevant instructions or constraints verbatim so they remain in effect after compaction." Only security constraints and the next-step quote are asked verbatim. No count or length cap in this arm.
- lean (`Jsr`): "The summary is also the only record of what the user said… A limit they set keeps applying only if the summary states it, so quote it exactly".
- short (`eir`): user's words "close to their own words". capped (`tir`): "in 2000 words or fewer".
- Partial compaction (`fJt`): `"from"` direction (`oir`) summarises the recent portion ("ALL user messages from the recent portion"); `"up_to"` (`rir`) ends with "Work Completed" / "Context for Continuing Work".
- Wrappers `dJt` ("CRITICAL: Respond with TEXT ONLY…") and `uJt`; custom `/compact` text appended as "Additional Instructions:". `<analysis>` stripped; `<summary>` becomes "Summary:" (`sir`).
- Continuation wrapper `_Et` (string at ~100,754,796): "This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation." `v3` adds the transcript path; `headTruncated` adds a note that the start is not covered.

### What bounds user messages [bundle]
- Full path (`Ter`): `messagesToKeep:[]` (~214,940,519): no message kept verbatim.
- Reactive/precomputed (`Gge` → `mer`): whole final API rounds kept verbatim, 1 round first, more on retry. Last resort (`hir`): everything from the last genuine user message onward; may drop the conversation head from the summariser input. Kept tails carry `lJt`: "…kept verbatim. The summary was written without seeing them…".
- Images/documents become `[image]`/`[document]` before summarising (`the`).
- Bounds: summariser output length, the 2000-word cap in `capped`, head truncation, the verbatim tail. The JSONL transcript is the only complete copy.
- The earlier book (2026-10-13) measured 13 to 26 of 91 to 156 user messages per stretch surviving whole in summaries [module/book measurement].

### Re-injected [bundle][doc]
- `rhe`, constants ~214,929,799: `aKe=5`, `Yir=50000`, `lKe=5000`, `Qir=5000`, `cKe=25000`, `Jir=500`, `ear=200`.
- Files (`dar`): 5 most recent, 5000 tokens each, ≤50000 total, skipped if in kept tail. Skills (`uar`): newest first, 5000 each, 25000 total. Plan (`car`, plus `plan_mode`). Background bash tasks (`par`): description 200, command 500. Hooks: PreCompact, SessionStart source `"compact"`, PostCompact (`X_t`).
- Docs: https://code.claude.com/docs/en/context-window ("What survives compaction"): CLAUDE.md, auto memory and plan re-injected from disk; up to five files re-read, >5,000-token file returns as "Referenced file"; skills 5,000 each / 25,000 total, oldest dropped first; SessionStart `compact` hooks run. [doc]
- https://code.claude.com/docs/en/how-claude-code-works: "clears older tool outputs first, then summarizes… Your requests and key code snippets are preserved; detailed instructions from early in the conversation may be lost." [doc]
- https://code.claude.com/docs/en/model-config: native 1M models compact at about 967K (= 1,000,000 − 20,000 − 13,000, matches bundle). [doc]
- https://code.claude.com/docs/en/env-vars: PCT override "can't raise the threshold"; `CLAUDE_CODE_AUTO_COMPACT_WINDOW` 100000–1000000; `DISABLE_AUTO_COMPACT` keeps manual `/compact`; `DISABLE_COMPACT` disables both; `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` default 200000. [doc]
- https://code.claude.com/docs/en/costs: `/compact <focus>` and a "Compact instructions" CLAUDE.md section steer the summary. [doc]

### Microcompaction / tool-result clearing [bundle] (~208,307,700–208,317,000)
- Client side: cleared results replaced with "[Old tool result content cleared]"; `JIn=20000` minimum tokens saved; image cost `pd=2000`; `Tis`/`Pro` keep last N results of clearable tools (N not resolved), telemetry `tengu_time_based_microcompact`.
- Server side: `clear_tool_uses_20250919` via beta `context-management-2025-06-27` with `{minIdleSeconds:3900, keepToolUses:5, clearAtLeastTokens:20000, triggerToolUsesBelowCount:3, minTriggerToolUses:20}`; only after >65 min idle, flag `tengu_zany_pike`, default "off".
- `compact_20260112` appears only in the bundled SDK's toolRunner deprecation warning, not in Claude Code's own compaction path.
- Unknown: default arm and path per account (feature flags); the summariser's own max_tokens.

## Anthropic API [doc]

- Overview: https://platform.claude.com/docs/en/build-with-claude/compaction — "Compaction replaces the older turns of a conversation with a summary that Claude writes on the server". Two kinds: on demand (beta `compact-2026-09-04`, top-level `compaction`) and threshold (`compact_20260112` in `context_management`).
- Threshold: https://platform.claude.com/docs/en/build-with-claude/compaction-threshold — header `compact-2026-01-12`; trigger `{"type":"input_tokens","value":150000}` default, minimum 50,000; `instructions` replaces the default prompt entirely; `pause_after_compaction` (default false) ends with `stop_reason: "compaction"` so the client can re-insert turns. "The API ignores all content blocks before the last compaction block." Example default prompt ("some models use"): "You have written a partial transcript for the initial task above. Please write a summary of the transcript. … Write down anything that would be helpful, including the state, next steps, learnings etc. You must wrap your summary in a <summary></summary> block." Usage: summed across `usage.iterations`; top-level excludes compaction.
- On demand: https://platform.claude.com/docs/en/build-with-claude/compaction-on-demand — returns one `compaction` block (readable `content` + `signature`) with `stop_reason: "compaction"`; "the summarized messages are removed"; `instructions` up to 16,384 characters replaces the default; compact again summarises old summary plus later turns; images, documents, `container_upload` and fetched URLs in the summarised range "are gone"; mid-conversation `role: "system"` messages in range are summarised and stop applying.
- Keep recent turns: https://platform.claude.com/docs/en/build-with-claude/compaction-keep-recent-turns — "No parameter sets which turns are kept. You pick a cut point"; kept turns go back word for word.
- Context editing: https://platform.claude.com/docs/en/build-with-claude/context-editing — beta `context-management-2025-06-27`; `clear_tool_uses_20250919` defaults trigger 100,000 input tokens, keep 3 tool uses, `clear_tool_inputs` false, `exclude_tools`, `clear_at_least`; cleared result replaced by placeholder; `clear_thinking_20251015` keep is model-specific; applied server-side, client keeps full history; memory tool warning before clearing. User messages not mentioned as affected.
- Answer: API compaction keeps no user message verbatim by itself; verbatim retention is the client's choice of tail.

## Codex CLI (openai/codex)

Installed `codex-cli 0.158.0-alpha.9`. Source read at local tag `rust-v0.161.0`; three files missing from the partial clone at that tag were read at `rust-v0.161.0-alpha.4` (marked α4). Only two commits touch them between α4 and 0.161.0: b44ca8 "Persist world-state snapshots alongside rendered context (#49847)", de0201 "Persist explicit user goal edits in model history (#49598)" (contents unread). URL form: `https://github.com/openai/codex/blob/rust-v0.161.0/<path>#L<n>` (use `rust-v0.161.0-alpha.4` for α4).

### Path selection [src]
- `run_auto_compact` (`codex-rs/core/src/session/turn.rs#L1471-1535` α4) and manual `CompactTask::run` (`codex-rs/core/src/tasks/compact.rs#L43-76`, 161): `Feature::TokenBudget` → token-budget; else provider `remote_compaction == V2` → remote; else local.
- `ConfiguredModelProvider::capabilities` returns V2 for OpenAI and Azure Responses providers, Unsupported otherwise (`codex-rs/model-provider/src/provider.rs#L37-44,60-69,410-417`, read at 0.158-α9; blob identical at α4 and 0.161.0). Bedrock also V2 (`amazon_bedrock/mod.rs#L283` α4).
- No V1 `compact_remote.rs` and no `/responses/compact` client call in the 0.161.0 tree; remote compaction is a `compaction_trigger` item on the normal Responses stream.

### Local compaction [src]
- Prompt `codex-rs/prompts/templates/compact/prompt.md#L1` (`SUMMARIZATION_PROMPT`, `prompts/src/compact.rs#L1`): "You are performing a CONTEXT CHECKPOINT COMPACTION. Create a handoff summary for another LLM that will resume the task. Include: Current progress and key decisions made; Important context, constraints, or user preferences; What remains to be done (clear next steps); Any critical data, examples, or references needed to continue. Be concise, structured, and focused on helping the next LLM seamlessly continue the work." Overridable by `compact_prompt` (`compact.rs#L116-121` α4).
- Prefix `prompts/templates/compact/summary_prefix.md` (`SUMMARY_PREFIX`): "Another language model started to solve this problem and produced a summary of its thinking process. …". Summary built at `compact.rs#L356` α4, installed as `CompactionSummary` fragment (`core/src/context/compaction_summary.rs#L17-36`, 161).
- On context overflow during the summary request, oldest item removed and retried (`compact.rs#L311-319` α4).
- `build_compacted_history` → `build_compacted_history_with_limit` (`compact.rs#L649-740` α4): initial context (passed empty, L359) + selected user messages + summary (or "(no summary available)"). `collect_annotated_user_messages` drops earlier summaries via `is_summary_message` (L550-579).
- **Cap**: `const COMPACT_USER_MESSAGE_MAX_TOKENS: usize = 20_000;` (`compact.rs#L55` α4; L59 in 0.158-α9). Walk newest first (`.iter().rev()`, L671), boundary message truncated with `truncate_text(..., TruncationPolicy::Tokens(remaining))` then stop (L701-722), reversed back (L725). Text-only messages keep original parts (commit bd3d4d "Preserve user text parts during local compaction").
- Initial context: pre-turn/manual use `InitialContextInjection::DoNotInject` (full reinjection on next turn); mid-turn uses `BeforeLastUserMessage` (`insert_initial_context_before_last_real_user_or_summary`, L591-647; doc comment L57-65).

### Remote V2 [src]
- `codex-rs/core/src/compact_remote_v2_attempt.rs#L39-87` α4: full history after `trim_function_call_history_to_fit_context_window` (`compact_remote_history.rs#L68`, 161), plus `ResponseItem::CompactionTrigger {}`, tools, base instructions; response must contain exactly one `Compaction` item (`compact_remote_v2.rs#L488-492` α4). Retries `MAX_REMOTE_COMPACTION_V2_STREAM_RETRIES = 2` (L79).
- `RETAINED_MESSAGE_TOKEN_BUDGET: usize = 64_000` (L75); `MAX_RETAINED_AGENT_MESSAGE_TOKENS: i64 = 10_000` (L76).
- `is_retained_for_remote_compaction_v2` (L555-600): `UserMessage`/`HookPrompt`; client developer messages only with `Feature::RetainClientDeveloperMessages`; agent messages ≤10,000 tokens excluding FINAL_ANSWER and descendant progress. `truncate_retained_messages` (L620-714): newest first, boundary truncated (marked incomplete), images counted with `Feature::CompactionImageBudget`. Result: retained items then compaction item (L504-530). Initial context via `build_compaction_initial_context` (L324-327).
- The earlier book measured "about nine in ten" user messages kept in this machine's sessions — consistent with a 64K budget not yet exhausted in those threads, not a guarantee.

### Token-budget compaction [src]
- `codex-rs/core/src/compact_token_budget.rs#L19-84` (161): no summary; pre-compact hooks, `start_new_context_window`, post-compact hooks; behind `Feature::TokenBudget`, takes priority.

### auto_compact_token_limit [src]
- Config `model_auto_compact_token_limit`: `config_toml.rs#L179,183`, `core/src/config/mod.rs#L637-641,4286-4288` (α4); `models-manager/src/model_info.rs#L29-31` (161).
- `ModelInfo::auto_compact_token_limit()` (`codex-rs/protocol/src/openai_models.rs#L525-536` α4): default `(context_window * 9) / 10`; configured value clamped to that 90%. `default_effective_context_window_percent()` = 95 (L389-390).
- Evaluation `codex-rs/core/src/session/context_window.rs#L53-117` (161). Fires pre-turn (`run_pre_sampling_compact`, `turn.rs#L1298-1325`), mid-turn when `needs_follow_up && token_limit_reached` (L601-625), post-turn when `model_post_turn_compact_threshold_percent > 0` (L715-734), and on `ContextWindowExceeded` (L336-355, L759-789), all α4.

## OpenAI API

- `openai-python` generated types (from OpenAI's OpenAPI spec), main branch, fetched 2026-10-16:
  - https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/responses/compacted_response.py — `CompactedResponse.output`: "The compacted list of output items. This is a list of all user messages, followed by a single compaction item." `object: "response.compaction"`. [SDK type, spec-derived]
  - https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/responses/response_compaction_item.py — `ResponseCompactionItem` "generated by the `v1/responses/compact` API"; `encrypted_content`: "The encrypted content that was produced by compaction." [SDK type]
  - https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/responses/response_create_params.py — `context_management` entries: `type` "Currently only 'compaction' is supported"; `compact_threshold` "Token threshold at which compaction should be triggered for this entry." [SDK type]
- Guide https://developers.openai.com/api/docs/guides/compaction (unreachable to WebFetch and curl here; content via web-search summary only, **unverified**): server-side compaction via `context_management.compact_threshold` (example 200,000, `store: false`, ZDR-friendly); standalone `/responses/compact` stateless, "do not prune" its output; compaction item is opaque and "not intended to be human-interpretable"; guide says the compacted window "can also include retained items from the previous window" without naming them.
- Answer: the API reference says all user messages are returned, with no cap stated; Codex's own client nonetheless applies its 64K retention budget on top.

## OpenCode (sst/opencode, tag v1.18.16; installed 1.18.16)

Fetched from `https://raw.githubusercontent.com/sst/opencode/v1.18.16/packages/opencode/src/session/...` (whether the repo now redirects to anomalyco unchecked). [src]
- Trigger `overflow.ts#L8-34`: `count >= usable`; with input limit, `usable = limit.input − reserved`, `reserved = cfg.compaction.reserved ?? min(COMPACTION_BUFFER = 20_000, maxOutputTokens)`; else `usable = context − maxOutputTokens`. `compaction.auto === false` disables.
- Docs https://opencode.ai/docs/config: `compaction.auto` (default true), `prune` (default false), `reserved` ("Token buffer for compaction"). [doc]
- Prune `compaction.ts#L28-31, L279-323`: `PRUNE_MINIMUM = 20_000`, `PRUNE_PROTECT = 40_000`, `PRUNE_PROTECTED_TOOLS = ["skill"]`; skips last 2 user turns; protects newest 40K of tool output; clears older if >20K; sent as "[Old tool result content cleared]" (`message-v2.ts#L293-294`). Started from `prompt.ts#L1338`.
- Tail `compaction.ts#L32-34, L116-121, L224-275`: `DEFAULT_TAIL_TURNS = 2` within `preserve_recent_tokens` default `min(8_000, max(2_000, floor(usable*0.25)))`; oversize oldest tail turn split. Tool output in serialised history cut to 2000 chars (L30, L52-53).
- Prompt `packages/core/src/session/compaction.ts#L16-46, L161-168`: "Create a new anchored summary from the conversation history." / "Update the anchored summary below … Preserve still-true details, remove stale details, and merge in the new facts." Sections Objective, Important Details, Work State, Next Move, Relevant Files. No verbatim user-message request.
- After: compaction user message shown as "What did we do so far?" (`message-v2.ts#L228-232`), summary, kept tail; `filterCompacted` (`message-v2.ts#L521-572`) stops at latest compaction / `tail_start_id`. After overflow the last real user message is held out and re-posted (`compaction.ts#L346-362, L462-488`); otherwise synthetic "Continue if you have next steps…" (L512-540).
- Gap: `packages/core/src/session/compaction.ts` `make()` with `DEFAULT_BUFFER = 20_000`, `DEFAULT_KEEP_TOKENS = 8_000`, `SUMMARY_OUTPUT_TOKENS = 4_096` — not confirmed used by the 1.18.16 path.

## pi coding agent (badlogic/pi-mono, tag v0.80.10)

Local clone; paths under `packages/coding-agent/`. URL form `https://github.com/badlogic/pi-mono/blob/v0.80.10/packages/coding-agent/<path>#L<n>`. [src]
- Trigger `src/core/compaction/compaction.ts#L209-212`: `contextTokens > contextWindow − reserveTokens`; defaults L106-110 `{ enabled: true, reserveTokens: 16384, keepRecentTokens: 20000 }`; docs `docs/settings.md#L113-115`, `docs/compaction.md#L29-35` agree [doc]. Token count = last assistant usage + chars/4 for later messages (L176-204). Overflow error → compact and retry once (`src/core/agent-session.ts#L1961-1980`).
- Cut `findCutPoint` L377-435: walk back to `keepRecentTokens`; never cut at a tool result (L282-295). Only messages after `firstKeptEntryId` survive verbatim.
- Summarised `prepareCompaction` L633-712: from previous `firstKeptEntryId` to cut; previous summary passed as `<previous-summary>` with update prompt (L474-511, L565): "PRESERVE all existing information from the previous summary … If something is no longer relevant, you may remove it."
- Prompt L441-472: Goal; Constraints & Preferences; Progress; Key Decisions; Next Steps; Critical Context; "Preserve exact file paths, function names, and error messages." No verbatim user-message request. `SUMMARIZATION_SYSTEM_PROMPT` in `src/core/compaction/utils.ts`.
- Summary cap `maxTokens = min(floor(0.8*reserveTokens), model.maxTokens)` (L559-562) = 13,107 by default.
- Split turns L718-731, L765-794 (`TURN_PREFIX_SUMMARIZATION_PROMPT`, 0.5×reserve). Branch summaries `src/core/compaction/branch-summarization.ts#L189-227,252,299-307`.
- File lists accumulate (`compaction.ts#L41-69`), appended as `<read-files>`/`<modified-files>` (`utils.ts#L72-78`). Tool results cut to `TOOL_RESULT_MAX_CHARS = 2000` only in summariser input (`utils.ts#L89-98,156`); no live-context pruning found.

## Gaps and caveats
- Codex: three files read at 0.161.0-alpha.4, not 0.161.0; installed binary is 0.158.0-alpha.9 (constants unchanged there).
- Claude Code: bundle is minified; default prompt arm and path are feature-flagged and not observed for this account.
- OpenAI guide text not fetched directly; SDK type docstrings used instead.
