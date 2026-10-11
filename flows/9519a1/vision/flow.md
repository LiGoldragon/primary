# Flow

Comment on «Flow, whole, in ethos», 2026-10-11 20:21, at the passage «Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows …».

> No we've gotten rid of the voice concept. Now it's just replaced by the core topic. One thing I did notice, which has maybe been fixed, is that the topic should always start with a small letter. It's uncapitalized. In other words we need a name for that. It's like a datomic name or something: a camelCase identifier. Anyway so far, the presentation proposal is good but we can't take out the voice part. Just replace it by saying that the default topic is `core` and that the `core` topic is essentially the permanent topic. It's the thing that keeps the machine going. It's the last topic to stand.

-- psyche, STT.

Comment on the same book, 2026-10-11 20:23, same passage.

> Actually we should say that a topic never really dies. It just goes idle, meaning the flows can be turned off. If the topic comes back (in terms of the living touching on something that means we have to address this topic again), then there will be a judgment call.
>
> This is where the system 1 models can come in or even a small LLM call to judge whether or not we should wake a flow for this topic and which layer, if we do wake it. The topic could be in the flow nexus for now but maybe at some point in another nexus. The topic will be associated with certain context modules. If that topic is needed again, then we know what to wake it, what to start it, what context modules to start it with, along with whatever new input is coming in that warrants restarting the flow. Are the meta flow ...

-- psyche, STT.

Comment on the same book, 2026-10-11 20:25, at the passage «A flow's id is a hash, held by the Nexus as bytes and written as three camelCase words. The Nexus reserves it before the …». Context: it is put as a question.

> We need the hash from the harness so we have to start the harness before we get the flow ID, I think. I don't know why this got turned around here unless we're not using the harness hash anymore. There are different parts of the session ID depending on the harness, which is supposedly random, and that's what we're using.
>
> I don't know why now the proposal is that we create a hash before. We've been using the session ID hash so that we can find a transcript easily from the flow ID. Is my idea stupid somehow or why do you think it's better to not do that?

-- psyche, STT.

Comment on the same book, 2026-10-11 20:32, at the passage «A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as i…».

> Well if it doesn't trust the claimed ID, then there is no claimed [ID]. Why would we ask for a claimed [ID] if we can get the [ID] programmatically? If we enforce the caller identification, then we don't need the model to declare its ID.

-- psyche, STT. Transcription corrected: "idea" → "ID".
