<!-- to-the-living:start -->
Presentation.{ «The main flow delegates, second edition» }

# The main flow delegates, second edition

```
 ┌──────────────────────────────┐
 │  MAIN FLOW                   │
 │  does not do things itself   │
 │  itself: log, psyche, beads, │
 │  skill files, a file it      │
 │  knows whole and relevant    │
 └──────────────┬───────────────┘
                │ one or two lines
                ▼
 ┌──────────────────────────────┐
 │  SPECIALIZED SUBFLOW         │
 │  already knows almost        │
 │  everything it needs         │
 └──────────────────────────────┘
```

Every sentence below is yours; the records are named beside each. Two landed lines of vision-flow sit against them, and five pieces are missing; those are the questions, which come first.

## Questions

Question 1. The record flows/6cc91b/vision/mainFlow.md, 2026-09-14, through speech-to-text, reads: «it's important for the main flow to not waste context and not use subagents, because their models are way more expensive and their context is way more valuable than any of the stuff that they should let subflows do». Is «not use subagents» what you said, or its opposite?

Question 2. vision-flow carries «a brief of a small paragraph». On 2026-10-03 you said «you just send them one or two lines, very extremely brief». Does the later replace the earlier?

Question 3. vision-flow's section «Subflows replace the harness subagent facility» describes a subflow as an independent flow, created by routing from the questions a flow ends with. Your 2026-10-03 records speak of subagents the main flow launches with a brief. Is the section proposed below about today's subagents until Flow exists, about Flow's subflows, or both?

Question 4. On 2026-08-09 you said you would rather train subagents to escalate back to their parents when the way forward is unclear than have parents micromanage. Does that stand today, as part of this?

Question 5. On 2026-09-09 you said «you do want to read skill files yourself». Today a skill is loaded only through the skill interface. Is reading skill files still the main flow's own?

## Distillation

### Proposal 1: in vision-flow

File: `psyche-skills/skills/vision-flow.md`. As it stands, the line reads:

A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph.

Replaced by:

A launch names the metaflow, the context modules composed into its prompts, and a brief of one or two lines.

Record: flows/9fb0ad/vision/subflows.md, 2026-10-03.

Ruling 1: does the replacement land, given Question 2?

### Proposal 2: in vision-flow

Added, as a new section before «## Subflows replace the harness subagent facility»:

## The main flow uses subflows

A main flow does not do things itself; it uses subflows to do them. It does not try to locate a file: a trivial subflow locates and reads it and returns what is relevant, and the main flow reads a file itself only when it knows exactly where the file is and that all of its content is relevant. The main flow still writes its flow log, records the psyche, and writes beads. A subflow is a specialized role that already has almost everything it needs to know, and the brief it is sent is one or two lines.

Records: flows/b05237/vision/operational-mainFlowUsesSubflows.md, 2026-09-18; flows/0d557b/vision/subflows.md, 2026-09-09; flows/a5940a/vision/mainFlowShouldNeverTryToLocateAFile.md and flows/7fba5f/vision/mainFlowWrites.md, 2026-09-03; flows/9fb0ad/vision/subflows.md and flows/edf227/vision/subflowBriefs.md, 2026-10-03.

Ruling 2: does the section land, once Questions 1, 3, 4 and 5 are answered?
<!-- to-the-living:end -->
