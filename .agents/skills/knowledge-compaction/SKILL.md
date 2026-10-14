---
description: What Claude Code and Codex compaction keep, replace and summarize, how the installed implementations run, and their measured context and request costs.
---

Compaction replaces the active conversation history with a smaller continuation context. Earlier records remain in the transcript; their presence on disk does not mean they remain in the next model request.

Verified on 2026-10-13 against installed Claude Code 2.1.294 and active Codex 0.161.0-alpha.2. Source behavior below belongs to those versions. Measurements belong to the named sample, not every session or model.

## Claude Code

**Mechanism.** The normal cached-prefix summarization path makes a forked model call with tools denied and `maxTurns: 1`. It normally uses the configured main-loop model. Retry, fallback-model and media-stripping paths also exist: one successful summary does not establish that only one request was made, that the same model always wrote it, or that every original input was passed unchanged. Manual and automatic compaction are both recorded.

**What is summarized.** Selected earlier conversation messages become a readable text summary. The installed program contains several summary formats, not just one fixed template. One format requests nine sections, including user messages, decisions, files, errors, pending tasks and current work. All four inspected summaries used that nine-section format. Asking for all user messages does not itself preserve their complete text.

**What is retained or restored.** A preserved tail can remain alongside the summary. In the four inspected boundaries it was the last assistant text reply and its duration record. Earlier tool calls, results and thinking were not listed in that preserved tail. The program also restores selected context separately: recently read files, invoked skills, a plan where present, task status and other attachments. File restoration selects up to five recent eligible files, reads them again from disk, and applies a 5,000-token per-file limit and a 50,000-token aggregate limit. Invoked-skill restoration applies 5,000 tokens per skill and 25,000 total, with recently invoked skills considered first. It can truncate or omit bodies; it does not guarantee every loaded skill is restored verbatim.

In the inspected session, each of the four boundaries restored the same 21 skill bodies, totaling 43,761 characters, and two to four file-content attachments plus file-reference notes. The system-prompt snapshot was identical before and after each boundary. Instructions and tool configuration remained separate request inputs. Restored file content comes from a new read, rather than a promise that the earlier tool result is preserved unchanged.

**Observable effect and cost.** Compaction records distinguish a reduced-history estimate (`postTokens`) from the next request's input usage. The latter includes restored context and request instructions. The first four boundaries in the inspected Claude transcript measured:

| Trigger | Before | Boundary after | First subsequent request input | Duration |
|---|---:|---:|---:|---:|
| automatic | 336,492 | 22,932 | 59,499 | 73.617 s |
| automatic | 286,071 | 26,396 | 63,691 | 108.675 s |
| automatic | 334,233 | 22,952 | 58,649 | 94.529 s |
| manual | 281,533 | 21,803 | 58,196 | 81.694 s |

Request input here is `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`, not a monetary charge. The recorded cumulative reduction after the fourth boundary was 1,144,246 tokens; this is not a count of deleted transcript tokens or a bill. The first three subsequent requests recorded zero cache-read input and substantial cache creation; the fourth reused 24,127 cached input tokens. Cache reuse therefore varies. Summarization itself consumes model requests and input/output tokens; the installed code records those usage categories, but these boundary records do not give a complete itemized compaction bill.

## Codex

**Mechanism.** In the installed version, the provider's compaction capability selects remote compaction or a local model-summary path. A separate token-budget mode starts a new context window without model/server summarization. These are different implementations. The observed current-version corpus used remote compaction with an encrypted result. In remote V2, the client sends conversation input, base instructions, tool specifications and a compaction-trigger item through its Responses stream, receives a compaction item, installs replacement history and recomputes context usage. Retries and model fallback are implemented.

**What is retained.** Remote V2 selects real user/hook messages and eligible inter-agent messages, then retains the newest selected content within a 64,000-token budget. The boundary message can be truncated and older messages omitted. Agent messages above the 10,000-token eligibility limit, descendant progress messages and final-answer notifications are excluded by the source filter. Client-authored developer messages are retained only when the corresponding feature is enabled. Initial context is inserted during mid-turn compaction or fully re-injected on a subsequent regular turn after standalone/pre-turn compaction. There is no source guarantee that every user or other-flow message survives verbatim.

**What is replaced or summarized.** Ordinary assistant messages, reasoning, tool calls and tool results are not selected as raw retained dialogue by remote V2. The server-produced compaction item carries `encrypted_content`; the inspected local records provide no readable text summary of its contents. Those records do not establish which individual omitted facts the server preserved. History outputs may also be truncated before a remote request if they exceed the available context.

The local-summary implementation instead produces a readable text summary and retains recent user text within a separate 20,000-token budget. Its existence in the installed source is not evidence that it ran in the inspected remote-compaction sessions.

**Observable effect and cost.** A read-only scan of the current Codex home's session files found 338 compaction records, all tagged CLI version 0.161.0-alpha.2. Every replacement history contained an encrypted compaction item; the records' plaintext summary field was empty. Aggregate replacement item types were messages, agent messages and compaction items, with no raw reasoning or tool-call/result items. Earlier transcript records remained present before those checkpoints.

Remote compaction is an additional server request, with input/output and cache usage recorded when supplied by the server. Compaction time and rebuilt context affect the continuation request. Token-budget compaction makes no summarization request. Automatic limits depend on model/configuration; this version's model limit is capped at 90% of its resolved context window. A particular observed trigger, retention percentage or next-request size is not a universal limit or price.

## Evidence

Claude: installed bundled functions `fZt`, `rhe`, `dar`, `uar` and summary-format definitions; the first four `compact_boundary` records of the inspected Psyche Core Secondary Claude transcript, their restored attachments, preserved-message references, summaries, prompt snapshots and subsequent usage records.

Codex: release tag `rust-v0.161.0-alpha.2`, `codex-rs/core/src/{tasks/compact.rs,compact.rs,compact_remote_v2.rs,compact_remote_v2_attempt.rs,compact_token_budget.rs}` and `codex-rs/protocol/src/openai_models.rs`; current-version session checkpoints. Exact source excerpts, transcript locations, measurements and the claim-by-claim verification are retained with this module's publication evidence.
