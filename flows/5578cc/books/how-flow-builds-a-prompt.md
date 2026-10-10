<!-- to-the-living:start -->
Presentation.{ «How Flow launches a flow and builds its prompt» }

# How Flow launches a flow and builds its prompt

This is Flow as it stands on its main branch (version 0.24.0). It is built but not deployed; your machine still runs older versions, and today's seats are launched by a script instead.

## What Flow is

- **One long-running service.** It has two sockets: an ordinary one any flow can use, and a meta one for configuration. It keeps its own store of flows and their events.
- **Small clients.** `flow` sends one request, `flow-meta` configures, and `flow-hook` is what Claude's hooks call to report events.
- **One request launches a flow:** Start, with a launch profile.

## What happens on Start

1. Flow checks the request and writes a copy of the system prompt for this one launch.
2. Flow picks the session id and claims the flow id before the harness exists (Claude). Codex gets its id after it starts.
3. Flow opens a Herdr pane and starts the harness in it. The pane is given `FLOW_ID` and Flow's socket, and the hooks are wired to report to Flow.
4. Flow registers the flow, titles the pane, and finds the skills.
5. Flow types the first message into the pane. The seat answers with a fixed receipt word once its skills are loaded.
6. Flow sees the receipt in the transcript and types "Begin the brief" to start the work.

## What goes into the seat's head (Claude)

In the order it enters the context:

1. **System prompt.** Replaced entirely by one file the caller supplies. Flow adds a line naming the predecessor and any remembered flows.
2. **Settings.** No permission prompts, plus the three hooks: start, every tool use, and stop. The hooks only report to Flow; they add nothing to the context.
3. **Entry files.** CLAUDE.md loads as usual, because the pane opens at Primary's root.
4. **First message.** Up to five skills loaded as `/name` commands, then "Read your launch file, load these other skills, then:", the brief, the paths of any source files, and the receipt instruction.
5. **"Begin the brief"**, after the receipt.

For Codex it differs. Flow leaves Codex's own base instructions alone. The supplied system-prompt text goes at the top of the first message, a lower place in Codex's context than in Claude's. Skills go in as typed skill items.

## What a caller can pass in

- **The system-prompt file**, used whole.
- **The brief** (the instruction text).
- **The skills**, in order.
- **Source files**, by path, each checked by hash. Only their paths enter the prompt.
- **Aspect and power, model and effort, harness** (Claude or Codex), **Herdr session.**
- **Predecessor and remembered flows.**

Fixed in Flow's code: the wording of the first message, the receipt and "Begin" lines, the five-skill limit, the settings and hooks, and no permission prompts.

## What is missing, if you want prompt modules

- **The system prompt is one file.** Flow cannot assemble it from parts, such as a base, a text for the aspect, one for the layer, one for the voice's work. It can only replace Claude's own prompt, never add to it.
- **No voice or layer.** The profile has an aspect (Psyche, Mind, Field) and an old "power level", not Psyche Primary.
- **Fixed hooks.** A caller cannot add hooks. Today's launcher has one Flow lacks: it re-reminds the seat of its main-flow rules every 20 messages.
- **Codex's top layer is unused.** Flow sets nothing at the top of a Codex seat's context.
- **The flow id is not in the text.** A Claude seat gets it in its environment only.

## How today's launcher differs

The script always uses the same system-prompt file and the same six skills, with effort fixed at medium. It sends the whole brief as the first message in one turn, with no receipt. It has no sources, layer, predecessor or remembered flows.

## The question for you

Which parts should a flow's prompt be built from? One proposal for Mind Astra to design: the system prompt assembled from named parts (a base, the aspect, the layer, and the voice's role), chosen by the voice, with your notion of a private part kept as one more slot for later. Say what you want in it, or comment "design it" and Mind Astra proposes the parts.
<!-- to-the-living:end -->
