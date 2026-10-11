# Artifact Comments: Flow, whole, in ethos

## Comment 1 (2026-10-11 20:21)

**Anchored passage:**
"Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one afte…"

**Location:** vision-flow, the vision whole › text "Flow manages metaflows. A metaflow is o…"

**Comment text:**
No we've gotten rid of the voice concept. Now it's just replaced by the core topic. One thing I did notice, which has maybe been fixed, is that the topic should always start with a small letter. It's uncapitalized. In other words we need a name for that. It's like a datomic name or something: a camelCase identifier.  Anyway so far, the presentation proposal is good but we can't take out the voice part. Just replace it by saying that the default topic is `core` and that the `core` topic is essentially the permanent topic. It's the thing that keeps the machine going. It's the last topic to stand.

---

## Comment 2 (2026-10-11 20:23)

**Anchored passage:**
"Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one afte…"

**Location:** vision-flow, the vision whole › text "Flow manages metaflows. A metaflow is o…"

**Comment text:**
Actually we should say that a topic never really dies. It just goes idle, meaning the flows can be turned off. If the topic comes back (in terms of the living touching on something that means we have to address this topic again), then there will be a judgment call.

This is where the system 1 models can come in or even a small LLM call to judge whether or not we should wake a flow for this topic and which layer, if we do wake it. The topic could be in the flow nexus for now but maybe at some point in another nexus. The topic will be associated with certain context modules. If that topic is needed again, then we know what to wake it, what to start it, what context modules to start it with, along with whatever new input is coming in that warrants restarting the flow. Are the meta flow

---

## Comment 3 (2026-10-11 20:25)

**Anchored passage:**
"A flow's id is a hash, held by the Nexus as bytes and written as three camelCase words. The Nexus reserves it before the…"

**Location:** vision-flow, the vision whole › text "A flow's id is a hash, held by the Nexu…"

**Comment text:**
We need the hash from the harness so we have to start the harness before we get the flow ID, I think. I don't know why this got turned around here unless we're not using the harness hash anymore. There are different parts of the session ID depending on the harness, which is supposedly random, and that's what we're using.

I don't know why now the proposal is that we create a hash before. We've been using the session ID hash so that we can find a transcript easily from the flow ID. Is my idea stupid somehow or why do you think it's better to not do that?

---

## Comment 4 (2026-10-11 20:29)

**Anchored passage:**
"A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the li…"

**Location:** vision-flow, the vision whole › text "A request reaching a metaflow is one of…"

**Comment text:**
I've actually changed my mind on this. I don't think that the flow should give the lock to message because we need the flow nexus to be the component that delivers the payload because it owns the lock. It can't really give a lock because then, even if it has a timeout, there would be a problematic window when we can't rely on two components sharing a lock.

If message wants to send a message, it communicates to flow and flow would take care of the mechanics and then tell message the status. It would also tell message if queued messages have been delivered because a waking message came in and so on. It would just give message the information on what's happening from its perspective.

Message would just say, "Okay I want to send a message to this Metaflow." That's what it would tell flow and then flow would do what it does and then respond to message. It might just be like, "Messages queued." Let's say the flow is being refreshed, so the messages are queued for when the flow has restarted. It would have a variant just to express that.

Once the message got delivered, message would subscribe to events from flow. When the message gets delivered, message would receive a notification that the message has now entered the context of that flow.

---

## Comment 5 (2026-10-11 20:30)

**Anchored passage:**
"A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Fl…"

**Location:** vision-flow, the vision whole › text "A layer is Primary, Secondary, Tertiary…"

**Comment text:**
What is this "weeds no path the writer calls"? I have no idea what you're talking about here. It sounds like hallucination.

---

## Comment 6 (2026-10-11 20:32)

**Anchored passage:**
"A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as i…"

**Location:** vision-flow, the vision whole › text "A flow is refreshed when its context pa…"

**Comment text:**
Well if it doesn't trust the claimed ID, then there is no claimed idea. Why would we ask for a claimed idea if we can get the idea programmatically? If we enforce the caller identification, then we don't need the model to declare its ID.
