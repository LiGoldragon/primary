<!-- to-the-living:start -->
Presentation.{ «The last response as a datom object» }

# The last response as a datom object

A flow ends each turn with a response. Here the vision of that response, of the refresh and of the handover is set beside what runs today and beside the compensation that stands in for what is missing.

## The last response

The vision says a marked block landing in a transcript becomes an action, a book among them.

The knowledge says the last response is free text. Its only typed part is the one line naming a book inside the marked block. The book tools read that block; Flow learns only that the turn ended.

The compensation puts a book between two marker lines under that naming line, and makes everything else the flow says one line of machine output.

So the type covers one line of a response today. Proposal 1 makes the whole response the object, and Proposal 2 lets each kind of object show itself.

## The refresh

The vision has one threshold per layer: at it the flow is told, writes its handover, and is replaced as it goes idle.

The knowledge says Flow holds two numbers per layer, and none is set. The second decides only whether a sleeping flow resumes or starts fresh; no awake flow is told or replaced. A separate warning program, at 200,000 tokens for Claude and half the window for Codex, has never run.

The compensation gives a flow at its layer's threshold no further work, a Fable flow from 15% of its window or 100,000 tokens, and has its successor started at once from the handover.

The vision names one threshold where Flow carries two. Proposal 3 gives each its role, with no handover written at either.

## The handover

The vision has the flow write its handover.

The knowledge says a handover is a free text file each flow writes in its own shape. A successor started by a launcher gets it in its first prompt. A sleeping flow that Flow wakes fresh gets its modules and its waiting requests, and no handover.

The compensation has the successor take its topics from the handover. The unused warning program asks for judgment only, nothing a tool can look up.

Nothing finds or generates a handover today, and the vision has no line on what a handover carries. Proposals 4 and 5 make it from objects and say what it carries; Proposals 6, 7 and 8 are the three ways to judge, for now, which objects make it.

## Proposal 1: psyche-context › vision/flow.md

A new section at the end. The variants in the code are the machine's example.

+ ## The last response is a datom object
+ A flow's last response is a datom object.
+ Its variant comes first and decides its structure, and that structure may hold further objects, each with its own variant.
+ For example:

```ethos
+ Library.{
+ []
+ [ Title.String
+   Body.String
+   Cause.String
+   Unblock.String
+   Page.{ Title Body }
+   Block.{ Cause Unblock }
+   Kind.[ Presentation Answer Blocker Responses ]
+   Response.[ Presentation.Page
+              Answer.Body
+              Blocker.Block
+              Responses.⟦ Response ⟧ ] ]
+ [ Spelled.[ spelling.[ String ] ]
+   Kinded.[ kind.[ Kind ] ]
+   Presentable.[ presentation.[ String ] ] ]
+ [ Title.[ Spelled ]
+   Body.[ Spelled ]
+   Cause.[ Spelled ]
+   Unblock.[ Spelled ]
+   Kind.[ Spelled ]
+   Page.[ Presentable ]
+   Block.[ Presentable ]
+   Response.[ Kinded Presentable ] ] }
```

```datom
+ Presentation.{ «Refreshing the Illustrator»
+                «One flow does every job.» }
+
+ Answer.«Nine proposals written, none landed.»
+
+ Blocker.{ «No layer has a threshold»
+           «A ruling on the two numbers» }
+
+ Responses.[ Answer.«Modules landed.»
+             Blocker.{ «Fable is asleep»
+                       «Your word to wake it» } ]
```

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › vision/book.md

A new section at the end.

+ ## Each kind of object has its presentation
+ Each kind of datom object has its own presentation in the user interface.
+ The user interface shows an object in its kind's presentation, and no thinking machine renders a page for it.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › vision/flow.md

The refresh at the layer's two thresholds, with no handover written at either. The last sentence removed repeats one a few lines above it.

- Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle.
+ Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told and is refreshed as it goes idle.
- A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.
+ A flow is refreshed at its layer's two thresholds: at the first it is told, and at the second it is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.
- Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › vision/flow.md

A new section after Proposal 3's lines. The code builds on Proposal 1's example.

+ ## A handover is made from objects
+ A successor's handover is found among its predecessor's datom objects, or generated from them: the last object of a kind, or every object of a kind.
+ What is looked for, and whether what is found becomes the handover or generates it, depends on the kinds of objects, on the flow's aspect, and on whether the flow had direct input from the living.
+ For example:

```ethos
+ Library.{
+ [ response:[ Response Kind
+              Spelled Kinded Presentable ] ]
+ [ Aspect.[ Psyche Mind Field ]
+   Living.Boolean
+   Search.[ Last.Kind Every.Kind ]
+   Searches.⟦ Search ⟧
+   Found.⟦ Response ⟧
+   Handover.{ Aspect Living Searches Found } ]
+ [ Counted.[ count.[ Integer ] ] ]
+ [ Aspect.[ Spelled ]
+   Living.[ Spelled ]
+   Search.[ Kinded ]
+   Searches.[ Counted ]
+   Found.[ Counted ]
+   Handover.[ Presentable ] ] }
```

```datom
+ ; a Psyche flow the living spoke to
+ { Psyche
+   True
+   [ Last.Presentation Every.Blocker ]
+   [ Presentation.{ «Refreshing the Illustrator»
+                    «One flow does every job.» }
+     Blocker.{ «Fable is asleep»
+               «Your word to wake it» } ] }
+
+ ; a Mind flow he did not speak to
+ { Mind
+   False
+   [ Last.Answer ]
+   [ Answer.«Modules landed.» ] }
```

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › vision/flow.md

Added to the section of Proposal 4.

+ A handover carries judgment, never what a tool can look up in one call.

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › vision/flow.md

A short-term line, added to the section of Proposal 4. Choose this, Proposal 7 or Proposal 8.

+ For now, a small model judges which objects make a flow's handover, as one judges whether to wake a topic.

Ruling: land, amend, or reject.

## Proposal 7: psyche-context › vision/flow.md

A short-term line, added to the section of Proposal 4, in place of Proposal 6 or 8.

+ For now, a flow judges which of its own objects make its handover, when it is told at its layer's first threshold.

Ruling: land, amend, or reject.

## Proposal 8: psyche-context › vision/flow.md

A short-term line, added to the section of Proposal 4, in place of Proposal 6 or 7.

+ For now, the Field Quaternary flow that checks the questions and requests a flow ends with also judges which of the flow's objects make its handover.

Ruling: land, amend, or reject.

## Proposal 9: psyche-context › vision/flow.md

A new section at the end. The first line is short-term. The living core sessions stay out of it: the vision does not yet say what one is.

+ ## Where the living types
+ For now, the living reaches flows through the harnesses themselves.
+ Once the user interface is ours, the system knows where the living types.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
