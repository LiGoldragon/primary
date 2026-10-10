# Design practice

## The main flow writes markdown with mermaid; the converting subagent does not use mermaid — it makes properly scaled SVG

Context: artifact comment on an unreadable mermaid node of the recap page (2026-08-31 11:24).

> I'm not able to read this. Like I said, I told you before. Yes, the main flow shouldn't make a web page or, in this case, a web report. I don't think that's a wise use of its context.
>
> It should make a Markdown file, and then it can use Mermaid graphs to represent the ideas that it wants to represent. The sub-agent that turns this Markdown into the actual web report should not use Mermaid. I think this is what happened here. It should make properly scaled SVG representations of it so that they're clearly readable and render correctly, so I'm not actually able to read that part of the graph here.

-- psyche, typed (artifact comment).

## Associations from different libraries are never mixed in one block; thinking machines copy what they see, a bad pattern is bad at any layer

Context: artifact comment on the recap's Associations block, which held `Text.[ Potential<Protos> ]` and `Protos.[ Potential<Datom> Potential<Ethos> ]` together (2026-08-31 11:16).

> This feels like these two associations would be from different libraries. The text to potential protos would be in protos, and the protos to potential datum [typed; datom] would be in datum [typed; datom]. In order to keep confusion from cascading out of these reports, we shouldn't mix these kinds and types and associations together, because it's going to create problems. Thinking machines just copy what they see, so any bad pattern is bad no matter where it appears and no matter at what layer.

-- psyche, typed (artifact comment).

## Step back: find the beautiful Rust we want first, then work backward to the infrastructure; never assume the infrastructure

Context: terminal, on the flow's generated if-chain walk, which the
psyche found ugly and rushed.

> The code that you showed to me looks really ugly. If kind declaration forms context is really hard to reason about, I would like us to take a step back and discuss this together from a high level: what am I trying to do here? Maybe there's something you're missing.
>
> We're still all over the place with terms of the vocabulary, so you're rushing towards showing me how to do it before it seems you even understand what I've seen [transcription uncertain; possibly "said"]. I think we need to step back before we run ahead.
>
> I really want us to step back. I want you to do a big, huge step back and rethink all of this. Have a fresh new approach and avoid any kind of ugly code. Look at how we look at the beautiful rest [STT; Rust] code that we would want to have to express this, and then work your way back from that: what infrastructure do we need to support that code?
>
> Instead of thinking what the infrastructure is and then trying to fit the rest [STT; Rust] code to fit the infrastructure, which you already assume, but it's not necessarily an invariant, the infrastructure is still in flux. Don't assume the infrastructure first. Find the goal of the beautiful code that we want, and then work your way back. Try to understand the whole from the perspective of achieving a beautiful separation of logic and an elegant final result, in terms of the logic not being just a convoluted bunch of inlined lambdas.

-- psyche, STT.
