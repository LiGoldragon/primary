## A flow is one run of a metaflow

Context: comment on «Flow's vision», the current vision/flow.md line "A flow is one run of a voice".

> The run: one run of a metaflow not a voice. Let's get rid of that voice vocabulary. Consistency

-- psyche, book comment, 2026-10-19T17:27, input mode not shown.

## Subflows replacing the subagent tool is long term, stated broadly

Context: comment on «How a flow is defined», the vision/flow.md heading "Subflows replace the harness subagent facility".

> Let's clean up this subflow vision a bit. It's a bit confusing and mark it as long term. This should just be in its own book. This is long term. We want to replace the subagent tool with actual flows but it's long term and it should be just a broad explanation of the concept instead of being so specific. These paragraphs are getting maybe too much into specifics and these are confusing short-term hacks with long-term vision. Like how we have the field coordinator involved, this sounds more short-term than long-term and maybe it's not even relevant anymore. I don't know. If we're not doing it right now, we can remove it and just represent the concept more clearly or more sanely.

-- psyche, book comment, 2026-10-19T17:45, input mode not shown.

## A startup may take several prompts, one model call

Context: comment on proposal 11, "A fresh flow starts with one prompt".

> Well this is true except that if it doesn't fit in one prompt, we can put it in two. Technically speaking from the harness's point of view, it looks like two prompts but they're sent almost instantaneously, one after the other. We don't end up making two LLM calls. However many prompts it needs to fit the initial startup in, we should never forget that a lot of the stuff goes in the system prompt, which is technically different from the harness's point of view.

-- psyche, book comment, 2026-10-19T18:20, input mode not shown.

## The Primary becomes a simplified flow

Context: comment on proposal 12, no Primary without its Secondary.

> Yes this is good, especially since we eventually want primary to be a simplified flow so that it's only used for guiding the design or posing questions, things like that. Essentially rendering a judgment

-- psyche, book comment, 2026-10-19T18:20, input mode not shown.

## A refreshed flow's first act is a book shaped by its context and prompt

Context: comments on proposals 16 and 17, a refreshed flow's first act.

> Not quite. It's a book, basically. It's a book which can have different forms so the book that it makes will depend on the context that it was loaded with and the goal or question it was given (essentially like the prompt). The so-called prompt is the actual only piece of string which was given to this supplier, which is unique to it and not a context module.

> This is also good so I'm not clear on which proposal I want. Like I said I want the difference between the different proposals to be explained.

-- psyche, book comments, 2026-10-19T18:23, input mode not shown.

## No handover: every task ends in a presentation, and Flow moves the next messages on

Context: comments on proposals 18 and 19, the handover warning thresholds.

> Like I said before there's no handover because every time a flow is given a task, it should end with a presentation. Maybe the word "presentation" is not right, but "a book." I don't like the word "book" because the books are going to go away and be replaced by a better user interface. We can use a word that essentially just means, for now, that we're making a book: a presentation, I think, or something which essentially could fit into a book, like the specification of every main response that the model gives.
>
> If it's being interrupted by messages from other flows, obviously, depending on what the messages are, it doesn't need to make a full presentation because it's maybe just being updated about things. Whenever it's given a specific psyche-originating task or goal or question, or whenever it starts its flow for the first time, the first thing it'll do (when it stops or in its last response) will be a presentation.

> Besides the whole fact that it's not told to write a handover, in fact it doesn't need to be told anything when it's going over context. It just stops getting new messages because the Flow reserves its next messages for the next flow of it. It just needs to be trained by default to always give a presentation whenever it's given significant new context to consider, especially psyche-originating.
>
> The amount at which each model should be refreshed depends on the models. It's going to be a specification and configuration that goes into Flow and obviously we need to specify. Roughly speaking the OpenAI models have a smaller usable context. The Claude models seem to be better: they can handle a longer horizon better and context recovery is deeper and better.

-- psyche, book comments, 2026-10-19T18:25–18:26, input mode not shown.

## Compaction is allowed for continuous work, with a warning and an investigation

Context: comment on proposal 21, some flows may compact.

> Yes some flows, like all flows, can compact if they're just continually working and without being given more work. But we should get a warning and somebody should investigate if a flow is working so much that it has to compact. Then maybe it's having trouble and we can bring this up to the living or get Psyche to reconsider how to approach it and give guidance.

-- psyche, book comment, 2026-10-19T18:29, input mode not shown.
