# Subflow dispatch

## A tool specialized for the expensive-model situation, perhaps used all the time: it starts the subagent differently, the main model does not write a huge prompt; the current subagent API makes specialized subagents so the main model's prompt is minimal; the subagent can read

Context: typed to the primary Claude efa157 on 2026-09-16 after the branch-protocol presentation, opening with a quota question (answered in the reply) and flowing into this design. The message continues in parallelContext.md and modelRoles.md, same date, and breaks off mid-sentence; the remainder is asked for in the reply. Logged by the main flow before acting.

> If there's not much Fable, we can make a tool specialized for this kind of situation where there's an expensive model, and maybe we'll use it all the time, actually. It starts the subagent differently. It doesn't ask the main model to write a whole big, huge prompt. At least we use the current tech, the current API for subagents, to make specialized subagents so that the prompt that the main model gives it is very minimal. That subagent can read.

-- psyche, typed.

## The main flow triggers the subagent by the way it responds: a type, low power thinking, and a delimited payload; that starts the job, which gets the amplified short log as its starting context

Context: same message, later. "Opus 4.6" as the thinking model is in modelRoles.md. Logged by the main flow before acting.

> Instead of asking it to create the subagent call, it just, by the way it responds, is going to trigger, let's say, an Opus 4.6 because it needs to think
> ...
> when it's time to be in Fable mode, Fable can say, "low power background, low power mode thinking." That means I'm going to think about, and then there's a payload. That's the subagent type: low power thinking, and the payload is the string, which is going to be a delimited payload. Here's the message we could even type. The type is low power thinking, and that starts the 4.6 job. That recreates the current sort of signal-to-noise-amplified short version log that we keep, and that essentially becomes its starting context. It puts it together, and then we have another side goal here of creating better tools to do that, to essentially query the session file, the transcript files, more automatically. We started doing that, but we could almost put all of the Claude stuff that

-- psyche, typed. (The message ends there.)

Completion, same day, after the recording stopped: the living resumed with "I was saying the transcript files automatically", closing the broken sentence as "we could almost put all of the Claude stuff that [queries] the transcript files automatically" (the bracket is the flow's reading). The rest of that message is in harnessRepositories.md and mcp.md.

## Opus 4.6 used more to think, a first-pass mass reading giving a predigested view; special subagents easy to invoke, preprogrammed, one per step of the flow, three to five steps, each on the right model: Opus 4.6 for thinking out loud, Opus 5 for doing work, 5.1 when it comes, Haiku for trivial jobs; a commit subflow given a datom; specs in datom between subagents, formalized in an easy nexus or a proof-of-concept feature of an existing one; whether the Claude subagent API is reachable from the CLI, and for Codex

Context: typed to the primary Claude efa157 on 2026-09-16 at 16:5xZ with "refresh your flow now" (a working instruction, log.md). "Focus 5" and "Focus 5.1" are speech-to-text for Opus 5 and 5.1, corrected in the quote and marked. Logged by the main flow before acting.

> Let's get a good view for everything and start using Opus 4.6 more to think about stuff.
>
> Maybe he can do the first-pass mass reading for you, for example, first, then give you a predigested. Create these special subagents that are just really easy to invoke. You don't have to give them a huge prompt because they are already preprogrammed to do a certain thing. You have different steps: 3, 4, or 5 steps that you go through in your flow. Make a subagent for each and use the right model:
> - Opus 4.6 if it's a thinking-out-loud model.
> - Opus 5 [transcribed "Focus 5"] if it's a doing-work model.
> - Opus 5.1 [transcribed "Focus 5.1"] if it comes out.
> - Whatever the latest version is.
>
> You have your haiku for really small, trivial jobs, like running. Maybe we could have a commit subflow that just tells it to commit. You give it a vector. You start using datom. Create these specs that you use between each other. You can formalize them in a tool too, just an easy nexus. You can make proof-of-concept nexuses, or just add a proof-of-concept feature in an already existing one.
>
> There should be enough of your own validation, and then try it to see if you can start the subagents efficiently with this CLI for Claude, for example. I don't know: is the subagent API in Claude itself accessible to us so that RCLI essentially triggers the subflow, and we can do that with Codex? That would be pretty wild. I think that would be pretty cool.

-- psyche, typed.
