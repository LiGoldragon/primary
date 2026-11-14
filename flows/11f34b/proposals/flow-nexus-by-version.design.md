# Design: Each version's vision in its own module

Author: Psyche core Fable (Fable 5.2). A worker assembles the presentation source from this file. Title: «Each version's vision in its own module». Kind: Proposal. Signature line: Created by Fable 5.2; a reader listed the lines, and a worker assembled the page.

His words, 12 November: «it seems there's a lot of Flow Nexus vision that's all over the place that should be in the corresponding version of the Flow Nexus. I'm not so keen on naming the flows so much».

The reader's list is /home/li/primary/flows/11f34b/gathering/flow-nexus-scatter.md (line numbers there are of psyche-belief main). Use the in-place form where the builder carries it and the standard form for removals, moves and replaces. Each removal is shown beside the line that makes it unnecessary, quoted from its module. Wording marked ADD, REMOVE, MOVE, REPLACE or COMMENT is final.

---

## Proposal 1: Later things leave the version 0 module · psyche-belief › vision/flow-nexus.md

COMMENT
The version 0 module holds three paragraphs of later versions. One is already said where it belongs; two move.

MOVE, from vision/flow-nexus.md to psyche-belief › vision/far-flow-nexus.md, placed just before its line beginning «Long term, Fable is a simplified flow», the whole paragraph:
A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, it has no regular tool, and its response is its message.

REMOVE, from vision/flow-nexus.md, the paragraph beginning «A flow is specified whole, in Datom, by a domain-specific language in Ethos». Shown beside the paragraph of psyche-belief › vision/flow-nexus-v1.md that says a metaflow is members, routes and a speaker and what a member is (near its line 17).

His words, 12 November, on the ephemeral flow line (they replace the MOVE that stood here): «I don't agree with the wording where it goes: "The ephemeral flow, when it's done, is replaced by another," because that's the definition of a permaflow. An ephemeral flow is just a single flow: there's a single thing, and then it's done. It's like a single function kind of thing, but for thinking machines. It doesn't have continuity. It takes an input, gives an output, and then it's done. System one models are explicitly made for that, but we can use any model that way. Yes, it goes into version 1.» Whole: the transcript of flow 7998d1.

REMOVE, from vision/flow-nexus.md, the whole paragraph, shown beside the ADD below, which makes it unnecessary:
An ephemeral flow is a continuous job flow that does not wake back up: it takes jobs while it runs, up to a ceiling on its context, and past the ceiling it is given no new job and another ephemeral flow takes it.

ADD, to vision/flow-nexus-v1.md, after that same paragraph of flow-nexus-v1.md (the one beginning «A metaflow is members, routes and a speaker»), two paragraphs:
An ephemeral flow is a single flow with a single job: it takes an input, gives an output, and is done. It has no continuity. It is to a thinking machine what a function is to a program: one call, one decision. A System 1 model is made to run this way, and any model may.

Many ephemeral flows are woven into the code and happen as part of how the system works: a Nexus calls one to judge whether data fits it, such as whether the same data is already held in an almost identical form.

Show, as it stands and unchanged, the Continuity type of vision/flow-nexus-v1.md, as the code of these lines:
Continuity.[ Permanent  ; keeps its address
             Ephemeral ]           ; one run, then gone

---

## Proposal 2: The hub is a definition's, not the aspect's · psyche-belief › vision/psyche-aspect.md

COMMENT
The section names one flow and limits what may reach which flow: a route. Routes are version 1's, written in a complex's definition; his word of 12 November is that the limiting of routes is «more like a version 1 thing».

REMOVE, from vision/psyche-aspect.md, the whole section «## The core Opus is the hub»: its heading and its paragraph. Shown beside the section «## A message takes a route» of psyche-belief › vision/flow-nexus-v1.md.

---

## Proposal 3: Two names that no longer exist · psyche-belief › intent/main-flow.md, vision/energy-nexus-v1.md

COMMENT
Primary was a layer's name until the layers became models; the lines read as well of any flow, and the example address names a model.

REPLACE, in intent/main-flow.md, only the changed words marked:
was: A Primary driving a fix owns its whole chain from its first turn
becomes: A flow driving a fix owns its whole chain from its first turn
and in the figure under it:
was: p["a Primary driving a fix"]
becomes: p["a flow driving a fix"]

REPLACE, in vision/energy-nexus-v1.md, only the changed words marked:
was: Configure.Reminder.{ Codex Low { Psyche core Primary } }
becomes: Configure.Reminder.{ Codex Low { Psyche core Opus } }

---

## Proposal 4: A definition may set its own threshold, and the warning is MiddleAbrupt · psyche-belief › vision/flow-nexus.md, vision/flow-nexus-v1.md

COMMENT
Added by Psyche beliefReview Fable. His words, 10 November, on the threshold: «That would be the default for that model, but certain flow definition or a permaflow definition could choose a different value.» And on the priority of the handover notice: «Yeah, I think the middle abrupt is better.»

REPLACE, in vision/flow-nexus.md, only the changed words marked:
was: Each model's threshold is configured in the Flow Nexus.
becomes: Each model's threshold is configured in the Flow Nexus, as the default for that model; a definition may set its own.

REPLACE, in vision/flow-nexus-v1.md, only the changed words marked:
was: It is warned when its context reaches the Warning share of its model's threshold, configured per model in the Flow Nexus: a HardAbrupt Notice naming its handover path, `flows/<id>/handover.md`.
becomes: It is warned when its context reaches the Warning share of its threshold, its model's by default or its definition's own: a MiddleAbrupt Notice naming its handover path, `flows/<id>/handover.md`.

REPLACE, in vision/flow-nexus-v1.md, in the datom under «; the Nexus, to the flow, at the Warning share», only the changed words marked:
was: HardAbrupt.Notice.«Write your handover at
becomes: MiddleAbrupt.Notice.«Write your handover at

---

## Proposal 5: Nothing depends on which flow asks · psyche-belief › vision/flow-nexus.md

COMMENT
Added by Psyche beliefReview Fable. His words, 10 November: «I don't want anything to depend on which flow is doing the query. I've seen that pop up over and over again. I want to make that clear in the vision.» And: «Version 0 does not enforce any kind of provenance, pseudo-security, or restriction because it just gets in the way. Let's make all the things we might want to poke at accessible, so we don't have to rebuild every time we need to do something.»

REPLACE, in vision/flow-nexus.md, in the paragraph beginning «A topic's name is a camelCase identifier», its last two sentences:
was: Every call to the Flow Nexus is identified by the calling process. Anybody may call the Flow Nexus, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
becomes: Anybody may call the Flow Nexus, and nothing it answers depends on which flow asks. Version 0 enforces no provenance and no restriction: everything one may want to try, a queue cancelled or pushed, an order or a reminder cancelled, is an operation, so that nothing is rebuilt to try it.

---

## Proposal 6: Example addresses name models · psyche-belief › vision/flow-nexus.md

COMMENT
Added by Psyche beliefReview Fable. As Proposal 3: Primary and Secondary were layers' names; an address names a model.

REPLACE, in vision/flow-nexus.md, in the datom of sent, delivered and answered, only the changed words marked:
was: Send.{ Address.{ Mind core Secondary } Soft.Order.«Review the drain fix.» }
becomes: Send.{ Address.{ Mind core Astra } Soft.Order.«Review the drain fix.» }
was: { Sender.{ Psyche core Primary } Soft.Order.{ k7ph «Review the drain fix.» } }
becomes: { Sender.{ Psyche core Opus } Soft.Order.{ k7ph «Review the drain fix.» } }
was: Send.{ Address.{ Psyche core Primary } Soft.Result.{ k7ph «Reviewed; green.» } }
becomes: Send.{ Address.{ Psyche core Opus } Soft.Result.{ k7ph «Reviewed; green.» } }
