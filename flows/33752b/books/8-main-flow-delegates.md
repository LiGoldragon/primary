<!-- to-the-living:start -->
Presentation.{ «The main flow delegates» }

# The main flow delegates

```
 ┌──────────────────────────────┐
 │  MAIN FLOW                   │
 │  context kept clean          │
 │  does no task work           │
 └──────┬───────────────┬───────┘
        │ one or two    │ unclear way:
        │ lines         │ escalates back
        ▼               │
 ┌──────────────────────┴───────┐
 │  TAILOR-MADE SUBFLOW         │
 │  pre-prompted definition     │
 │  holds all it must know      │
 └──────────────────────────────┘
```

You have said this from 2026-08-09 (the manager's context is gold) to 2026-10-06, in twenty-six flows; the machine skills carry it as their own lines, and no psyche skill says it. Records: vision-raw/managementDelegation.md, 2026-08-09; flows/b05237/vision/operational-mainFlowUsesSubflows.md, 2026-09-18; flows/edf227/vision/subflowBriefs.md and flows/9fb0ad/vision/subflows.md, 2026-10-03; flows/e5a0bc/vision/capability.md, 2026-10-06. One record of 2026-09-14 reads «not use subagents» through speech-to-text; its own sentence says the opposite and is read so.

## Distillation

### Proposal 1: in vision-flow

File: `psyche-skills/skills/vision-flow.md`. Added, as a new section before «## Subflows replace the harness subagent facility»:

## The main flow delegates

A main flow does no task work itself: its model is the most expensive and its context the most valuable, so every search, edit, build and probe goes to a subflow, and the main flow keeps its hands clean. The subflow is tailor-made: a pre-prompted definition holds everything it must know, and the brief it is launched with is one or two lines. A subflow whose way forward is unclear escalates back to its parent; the parent does not micromanage it.

Ruling 1: does the section land?

Ruling 2: the third sentence (escalation) rests on one record of 2026-08-09. Does it stand with the rest, or is it left raw?
<!-- to-the-living:end -->
