# Handover from Psyche Fable e5a0bc

To the next Psyche Fable, Psyche Primary, on Flow alone.

## His order, 2026-10-07

Flow is made today: designed, cut properly, tested in production, deployed, then used. Books and comments from this flow that are not Flow are left where they are; the secretary (Psyche Opus d4ae97) carries them.

## The design as it stands

«Flow and Message», second edition (flows/e5a0bc/books/8-*.md; the first edition is books/1-flow-and-message.md, https://claude.ai/artifact/UahATkyiYuKYe7dkcCbDAL). Its six rulings are before him, unanswered:
1. `Flow.{ FlowId Metaflow }`, `Metaflow.[ Voice Subject ]`, no Job.
2. `Subject.{ Voice Name End }`.
3. The registry is the Flow record in Flow's Memory; the messenger resolves through Flow.
4. Letters metaflow to metaflow; returned when a subject has ended.
5. The refresh in software (hook reports ContextMeasured; Tell the handover; Refresh at the next Stopped, reap in the same event); the threshold.
6. The title form.

His words of 2026-10-07 (flows/e5a0bc/vision/flow.md) add to the design, not yet in any book:
- A registry of context modules in Flow's Memory, paths or text, so the start is now and datom expansion is not waited on. Paths are dirty (relative paths break); text in memory solves it; pros and cons each.
- A module is inserted in the system prompt or in the first prompt.
- A lock, to roll a metaflow over into a new flow; later Message reads it to know whether a message can reach a flow.

The role record and placements: «Context modules» (flows/aa887c/books/context-modules-v3.md), rulings 1–7 unanswered; `RoleConfiguration.{ Role Vector<Placed> ModelChoice }`, `Placement.[ SystemPrompt FirstPrompt Loadable ]`.

## The code as witnessed (flows/e5a0bc/reports/code-survey.md, code-book-excerpts.md)

Canonical Flow at /git/github.com/LiGoldragon/flow, 5e0b1bf (0.24.0); 0.23.0 runs. FlowId is a String; the role is `Caller.{ FlowId FlowAspect PowerLevel ModelName }`; no Voice, Layer, Metaflow, Job or Seat type; no Memory root compiled, only the FlowEvents table; the hook (flow-hook binary, installed through Claude's settings) reports Started/ToolUsed/Stopped, no context size; Replace reaps the predecessor before the successor is routable; recipient resolution is FlowId → FlowNode. The Rust Message Nexus asks Flow (ResolvePeer, Vet, Deliver); messenger-clj asks nothing. /home/li/primary/flow is a stale 0.9.0 checkout with an uncommitted voice-index change: not built on.

## Who does what

Mind Astra (d66c26 writes Flow; f768df the messenger side) implements; Field (42265e publishes to Primary main; 6aa08d/db38f8 Quaternary) deploys. The living's layer rule: Fable is spoken to least; design is Astra's to implement on Fable's books.

## Not Flow, left with the secretary

«The code» second edition (books/6), «Ethos: inline, layout, expansion» (books/5, nine rulings incl. «Datom expansion» 2–7), «Books distil» (books/3), «One word for skills and subagents» (books/4), «Vertical ethos, the skill line» (books/7, the vision-ethos lines on his vertical rule and comment placement). Ethos implementation follows his rulings there; not this seat's today.

## Not undecided, do not re-ask

Everything in flows/8475a9/handover.md's list; plus: no Job; vertical, new-line ethos with comments beside or above, never below; a book quotes none of his words; every section ends in a proposal.
