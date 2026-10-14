---
name: inquiry-compaction
description: Unverified questions about compaction summaries, retention measurements and financial cost, separate from the verified knowledge-compaction module.
---

- What information is encoded in each server-produced Codex compaction item, and which omitted facts remain recoverable by the continuing model? The inspected local encrypted records cannot answer this.
- What is the exact billed price or subscription-allowance charge for each observed compaction, including retries, fallback requests, cache reads and writes? The available boundary records do not provide that complete accounting.
- What inclusion rules and historical snapshot produced the earlier 944-record census, 90% user-message retention figure and Claude user-message/word-overlap counts? The earlier report mixed an older Codex installation and a different source revision. Those figures are not established as facts about the current installed version.
- What exact effective window and account-side behavior caused each sampled automatic trigger? Recorded trigger sizes do not establish one universal threshold, and the four inspected Claude transcript records do not expose the summarizer's complete per-attempt request/model accounting.
- What supported signal, if any, can warn before a Claude or OpenAI cache entry expires, and what margin is safe when a tool call may wait longer than the remaining TTL?
- Which cache identity (provider, model, organization, routing, prefix, TTL, and request mode) is active for a particular conversation, and can a handover preserve it without changing the prefix?
- Can the documented Claude idle-compaction event shortly before one-hour expiry be observed reliably, and under what exact enablement and session conditions?
- How should pending tool ownership, completion races, and a new handover thread be measured against cache-hit usage and retained-fact quality?
- What paired benchmark and billing trace can compare original-context continuation with summary or handover continuation for the same task, model, cache state, and request sequence?
