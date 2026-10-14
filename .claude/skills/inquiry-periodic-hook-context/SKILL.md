---
description: Unresolved implementation, counting and native-effect questions for periodic hook reminders.
---

- Was the 2026-09-24 requested recurring reminder ever implemented and installed? The original words and current hook contracts do not establish a deployment.
- What does “every twentieth prompt” count: submissions, accepted turns, externally injected messages, queued prompts, or prompts including those later blocked? The original retained wording says every so many messages and does not settle this count.
- What is the intended reset boundary across resume, clear, compact, fork and a replacement session, and how would concurrent submissions or duplicate executions affect retained counter state? No periodic counter was implemented or exercised in this investigation.
- Does a particular seat's effective hook configuration, feature/trust policy and input route actually fire the event and deliver the exact reminder at the twentieth boundary? Source contracts were verified; no fresh native twenty-prompt test or live-seat configuration change was performed.
- How much long reminder text reaches the immediate model request after output limits/spill, and what survives compaction or a full-history fork? The event's injection role does not guarantee unlimited verbatim retention or main-only visibility.
- Does the reminder change behavior or prevent forgetting? Additional context insertion alone does not establish that effect, or raise conversation/developer text to the base system stratum.
