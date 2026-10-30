# Flow

## 2026-10-27 — In the long term: an idle-flow procedure; the Flow Nexus tells a flow when it has been idle, when its cache will expire, or when its context passes a size; the flow winds down, puts its chat proposals into a proposal book, and refreshes
Context: the living, direct, after his words on short proposals in the chat (flows/bf8ae0/vision/psyche-interaction.md). He marks it as not short term.

> Also, a side thing here is the idea that we have some kind of timer that tells a flow when the cache is going to expire. You can look into the documentation and what Claude does or what Codex does, but we could tell the flow to do some kind of wind-down and flow refresh if its context is, let's say, larger than 100,000 tokens or something. Any proposal that it had in its chat when it does this, I don't know what to call it. There's a term I'm looking for. It's like a procedure that's done when the flow's activity is dropped and hasn't acted in a while.
>
> This is obviously not short term because it involves hooks, right? The Flow Nexus would know when a flow hasn't been active for X amount of time, whatever it is, and when the cache is going to expire. Then it's told that it should do its thing for the idle flow procedure, if you will, right? One of those things would be to put all of the proposals that it had in a chat into a proposal book so that it's not lost.

## 2026-10-27 — The rebuilt Flow: implemented, tested, then used; old flows refreshed; the next design carries the code: all the ethos with example datom, and the Rust that matters
Context: the living, direct, after agreeing the rebuilt Flow should replace the current one.

> All right let's get this implemented and tested and then when it's done let's start using it.
>
> Once you get all this ball rolling (if it's not already rolling), I'd like you to start and to refresh your Flow and any of your other flows that are old. If I'm not talking to you by then you could create a first or a next design with code and everything.
>
> For Flow, the full vision with the code as we discuss, I want to see the code now, especially the ethos and the [datom]. I want ethos with example [datom]. I'd like to see all the ethos and some of the code that matters, even if it's in Rust, if you think it matters that it should be done a certain way or if you want to give some examples.

Transcription corrected: "datum" → "datom".

## 2026-10-27 — Reminders are a Flow feature: a flow asks Flow to wake it at a time, since Flow already sends messages; for the next wave, after what is slated
Context: the living, direct, after I scheduled my own wake with the harness's tool.

> I think this would also be a cool feature in Flow: to give yourself reminders so you don't have to make ad hoc scripts for this kind of stuff. Plus Flow already knows how to send messages so I think it would be a perfect place for it. ... I don't want to make this a blocker for what we currently have slated so it would be something that we could do afterwards.

## 2026-10-27 — The Flow Nexus, so named, has an operation on the meta socket to order a flow's compaction: a fail-safe among the operations to rely on; a flow with a long context self-compacts when all else fails
Context: the living, direct, seeing my context long and refresh refused.

> You're supposed to refresh your flow, right? Your context is really long. I guess if everything else is failing, you can always self-compact.
>
> I think we should have an operation in the Flow Nexus, and I think we should use that term, the Flow Nexus, to know that we're not talking about a flow. We should have an operation to order the compaction on the meta socket for a certain flow. It could be used as a fail-safe, and that's what I meant. We should have all these operations we can rely on in case.

## 2026-10-27 — The pulse: hourly is enough; a 20-minute check with instructions can be the Secondary's, Opus being far cheaper; the Primary keeps itself warm under the hour
Context: the living, direct, same message.

> Please don't let me down, and don't feel shy to check on the hourly. Maybe you don't have to check so much. If you feel like you need to check in 20 minutes, that's okay, but you can also slack back and go to the hourly. ... Sometimes you can also ask to be messaged back through your secondary, as always, or maybe you can have your secondary do the pulse. It's good to keep you warm below the 1-hour cache time, but Opus is way cheaper than Fable.
>
> If you want to do a 20-minute check with instructions on what to check and what to wait for, then your secondary could be a good replacement for that. You could always keep yourself warm on the sub-hour thing.

## 2026-10-27 — Use up Codex; in the long term, the resets are used for the machine
Context: the living, direct, going to bed.

> Don't feel shy to use up Codex. Like I said, we have a reset, so that would also be a good long-term feature: to be able to use those resets for you.
