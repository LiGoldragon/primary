# Flow

## 2026-10-11 — the full vision of Flow in ethos: signal, memory and storage ethos, all the traits and all the types

Order to the Flow topic flow, relayed by core d68c82 through 9519a1. "Let's get the Flow topic flow to reaggregate" and "Let's give this a shot on Flow" are the working instruction; the vision is what the presentation is to hold.

> Let's get the Flow topic flow to reaggregate everything about Ethos and Nexus and Flow and everything I've said about all these things. Present to me the full vision with the signal ethos, the memory ethos, and the storage ethos for it. I want to see traits also because all of the behavior, basically all of the traits. Here's what we need to do: we need to define all of the traits and all of the types in Ethos. Let's give this a shot on Flow.

-- psyche, STT, relayed by 9519a1.

## 2026-10-11 — the voice concept is gone; the default topic is core, the permanent topic, the last to stand

Comment 1 on «Flow, whole, in ethos», 20:21, at the metaflow paragraph; relayed by core d68c82 through 9519a1.

> No we've gotten rid of the voice concept. Now it's just replaced by the core topic. One thing I did notice, which has maybe been fixed, is that the topic should always start with a small letter. It's uncapitalized. In other words we need a name for that. It's like a datomic name or something: a camelCase identifier. Anyway so far, the presentation proposal is good but we can't take out the voice part. Just replace it by saying that the default topic is `core` and that the `core` topic is essentially the permanent topic. It's the thing that keeps the machine going. It's the last topic to stand.

-- psyche, STT, relayed by 9519a1.

## 2026-10-11 — a topic never dies; it goes idle; waking it is a judgment call, with its context modules

Comment 2, 20:23, same passage; the last sentence breaks off.

> Actually we should say that a topic never really dies. It just goes idle, meaning the flows can be turned off. If the topic comes back (in terms of the living touching on something that means we have to address this topic again), then there will be a judgment call. This is where the system 1 models can come in or even a small LLM call to judge whether or not we should wake a flow for this topic and which layer, if we do wake it. The topic could be in the flow nexus for now but maybe at some point in another nexus. The topic will be associated with certain context modules. If that topic is needed again, then we know what to wake it, what to start it, what context modules to start it with, along with whatever new input is coming in that warrants restarting the flow. Are the meta flow ...

-- psyche, STT, relayed by 9519a1.

## 2026-10-11 — the flow id is the harness's session id hash, so a transcript is found from it

Comment 3, 20:25, at the flow-id paragraph; a question, answered by this flow.

> We need the hash from the harness so we have to start the harness before we get the flow ID, I think. I don't know why this got turned around here unless we're not using the harness hash anymore. There are different parts of the session ID depending on the harness, which is supposedly random, and that's what we're using. I don't know why now the proposal is that we create a hash before. We've been using the session ID hash so that we can find a transcript easily from the flow ID. Is my idea stupid somehow or why do you think it's better to not do that?

-- psyche, STT, relayed by 9519a1.

## 2026-10-11 — Flow keeps the lock and delivers; Message asks Flow to send to a metaflow and subscribes to its events

Comment 4, 20:29, at the request paragraph.

> I've actually changed my mind on this. I don't think that the flow should give the lock to message because we need the flow nexus to be the component that delivers the payload because it owns the lock. It can't really give a lock because then, even if it has a timeout, there would be a problematic window when we can't rely on two components sharing a lock. If message wants to send a message, it communicates to flow and flow would take care of the mechanics and then tell message the status. It would also tell message if queued messages have been delivered because a waking message came in and so on. It would just give message the information on what's happening from its perspective. Message would just say, "Okay I want to send a message to this Metaflow." That's what it would tell flow and then flow would do what it does and then respond to message. It might just be like, "Messages queued." Let's say the flow is being refreshed, so the messages are queued for when the flow has restarted. It would have a variant just to express that. Once the message got delivered, message would subscribe to events from flow. When the message gets delivered, message would receive a notification that the message has now entered the context of that flow.

-- psyche, STT, relayed by 9519a1.

## 2026-10-11 — no claimed id: the caller is identified programmatically

Comment 6, 20:32, at the refresh paragraph. (Comment 5, 20:30, asked what "weeds no path the writer calls" meant; the sentence was "reads no path a caller writes"; answered, not vision.)

> Well if it doesn't trust the claimed ID, then there is no claimed [ID]. Why would we ask for a claimed [ID] if we can get the [ID] programmatically? If we enforce the caller identification, then we don't need the model to declare its ID.

-- psyche, STT, relayed by 9519a1. Transcription corrected: "claimed" → "claimed [ID]".

## 2026-10-12 — four comments on «Flow, whole, in ethos, third edition»

Context: comment 1 sits on proposal 1's paragraph «A request reaching a metaflow is one of a closed set of types…».

> This is all good. Land it.

-- psyche, typed, 16:07, relayed by 9519a1.

Context: comment 2 sits on the item «Name» among the options for the camelCase identifier type (ruling 3); he notes it is used across dialects.

> Well if we create a special thing and we call it a name or we call it a word, you're never going to know when I'm talking about it. Those are silly suggestions. We need something that somehow embodies what we're trying to do. This is going to be used a lot here so whenever it's like an identifier, a word identifier, or an expression, it will be more than one word. Wherever we have something like a topic, a particular object that needs to be identified by agents or humans, which is anything that's user-facing that needs to be named through judgment and has to be given a name. Obviously variants are great but we have to recompile everything to add one. It's essentially a variant that is created on demand and is a bit more descriptive. The fact that it doesn't start with a capital is how we differentiate it from variants. You could give a few different shots at how we could call this. It would go in some kind of shared library, maybe the [protos] library, because I think it could be used in more than one place, in more than one dialect. It would also do a check, which is interesting. Maybe this deserves its own full research, especially in terms of Rust libraries and executable size bloat. If you have a library of words or you use an external service, which I'm not a fan of, at least it should look like a word. Oh my God this is a perfect spot for a system1 AI call to use a cheap judgment on: Is this composed mostly? Is this made up of words? Is this a camel-case string made up of words, whether they're proper nouns or not? It's not a problem and then we would have, I guess, a certainty threshold. Brilliant. But then again maybe there's a cheap library that can do a quick check with a fallback on AI. That's also an interesting possibility: if there's something that's cheap, lightweight (in terms of runtime cost) and can, in many cases, give us an answer on whether or not these components are actual words programmatically, and then fall back to the AI in case of a negative.

-- psyche, STT, 16:12, relayed by 9519a1. Bracket [protos] as relayed.

Context: comment 3 sits on «the title of a thread:»; a question.

> What do you mean by thread?

-- psyche, typed, 16:13, relayed by 9519a1.

Context: comment 4 sits on the process object («Instant») in Flow's Library in the ethos file; the last comment, where he stopped reading.

> I see that you have the process object defined in the library for Flow but we should have a shared library that many components, that many nexuses, are going to use. This is because identifying the calling process of a CLI is something I would like to minimize the amount of code that needs to be rewritten for every CLI and increase the ease of cognition when reading the code as to what this is doing. Obviously this is done in the background whenever the CLI is used so none of it is actually user-facing in a sense or configurable. It's just something that happens and it may be on all CLIs. I'm not sure now but it's an interesting topic to eventually develop further. We should get Mind to put together a concept that can test whether or not this can actually work using Ethos and everything. We can test it on Flow. Let's give free rein to Fable and Astra to design something like this and implement it. Flow isn't even on in production so I'm not even worried about merging more into main. I'm also curious why we haven't been able to start using Flow Nexus so far, even though it's been a month or something, so I'd like to get an investigation on that.

-- psyche, STT, 16:21, relayed by 9519a1.
