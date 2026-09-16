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
