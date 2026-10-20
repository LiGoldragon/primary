<!-- to-the-living:start -->
Presentation.{ «What compaction keeps, 2nd edition» }

# What compaction keeps, 2nd edition

```
 a long thread nears the
 window's end
     |
     v
 +------------------------+
 | the harness asks a     |
 | model to summarise     |
 | the older part         |
 +------------------------+
     |
     v
 +------------------------+
 | new context:           |
 | summary                |
 | + some user messages   |
 | + re-read files,skills |
 +------------------------+
     |  the next compaction
     |  summarises the summary
     v
 +------------------------+
 | the oldest words fade  |
 | first                  |
 +------------------------+
```

No harness keeps every user message word for word. Each keeps the newest within a budget, or only a summary.

## Each harness, from its source and documentation

| harness | your messages after compaction |
|---|---|
| Claude Code | none whole; the summary is asked to list them all, with no cap |
| Codex | the newest, whole, within 64,000 tokens; the oldest one that fits is cut, older ones dropped |
| Codex, local summary | the newest within 20,000 tokens |
| OpenCode | the last 2 turns |
| pi | about the last 20,000 tokens |
| Anthropic API compaction | none, unless the caller keeps a tail |
| OpenAI API compaction | all are returned, with an encrypted summary; no cap stated |

## Checked against our own sessions

| | Claude Code, 15 sessions | Codex, 355 sessions |
|---|---|---|
| user messages before | 59 to 186 per stretch | up to 125 |
| kept whole | 1 to 26 | 102 of 125 in one session |
| the rest | paraphrased in a list, 30 to 95% reworded | dropped, oldest first |
| after many compactions | nothing from before the previous one is quoted | stays near 260,000 characters, about the 64,000-token budget |
| summary | readable, 14,000 to 32,000 characters | encrypted, unreadable |

Two surprises: Codex cuts the middle out of a very large message without marking the cut, and Claude Code keeps the last 2 to 7 messages unchanged although its default path is written to keep none.

## Proposal 1: what survives, harness by harness

File: mind-context/skills/knowledge-compaction.md, at the end of "Claude Code"

+ Across repeated compactions the list of user messages is rewritten each time: measured on 15 sessions, 1 to 26 of 59 to 186 user messages per stretch survived whole, 30 to 95% of the listed ones were paraphrased, and none from before the previous compaction was quoted. The last 2 to 7 messages before a boundary stayed unchanged.

Ruling: land, amend, or reject.

## Proposal 2: Codex's budget, measured

File: mind-context/skills/knowledge-compaction.md, at the end of "Codex"

+ Measured on 355 compactions, the retained user text held near 260,000 characters across repeated compactions, matching the 64,000-token budget. A message larger than the budget lost its middle with no marker of the cut.

Ruling: land, amend, or reject.

## Proposal 3: the other harnesses

File: mind-context/skills/knowledge-compaction.md, new section at the end

+ ## Other harnesses and providers
+
+ OpenCode keeps the last two user turns within 2,000 to 8,000 tokens and summarises the rest. pi keeps about the last 20,000 tokens and rolls earlier ones into a summary of at most about 13,000. Anthropic's API compaction replaces everything before its compaction block with a summary and keeps no user message unless the caller keeps a tail. OpenAI's API compaction returns the user messages followed by one encrypted compaction item, with no stated cap.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
