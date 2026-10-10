# Three open Message/Flow questions: frame for Flow Primary f5a6e9's next book

Scope. Quotes are verbatim from the raw records, with path and date as the record gives them. Where a record is a relay of another flow's record, the original is cited and the relay is named under it. A record marked (notion) is a notion, which rules nothing. A date "not in record" means the record states none. Skill sources (psyche-skills/skills) are distilled text, not raw words, and are marked (skill). flows/73ada7/reports/message-flow/notes.md and flows/f5a6e9/handover.md were used for framing only. Context rule from the living (flows/ebbe30/vision/metaflow-naming.md, 2026-10-09): "the recent vision and the one that's been repeated a lot, which hasn't been overridden by newer decisions or statements."

---

## 1. The lock's time unit

What is open. Message asks Flow for a lock that is time-bound so it does not lock forever. No record gives a unit, a duration or a clock for that lock.

### Records, oldest first

flows/01a03d6e/vision/locks.md, 2026-08-26 (an earlier lock, the Orchestrate path lock; it bears only on how a lock ends):
> any lock remains, they can be removed forcefully by another flow since any lock must be released, and this should be part of training.

> if through a transcription file, if it's possible to know that a flow is idle, meaning it is idle and it has no ongoing non-idle subflow, then all of its locks are automatically forfeited by protocol.

flows/01a03eda/vision/observe.md, 2026-08-26T17:54:57Z (Orchestrate observation, not Flow/Message):
> Actually, Observe.Locks is best. If another kind of lock comes, then we can add it as such; Observe.ExpiredLocks, etc

flows/c7128c/vision/messageAndFlow.md, 2026-09-18:
> - Message can get the data from Flow, and Flow can put a lock on some stuff.

flows/1b8ac0/vision/messaging.md, 2026-09-21 (STT):
> It locks the message for the session to send the message, then it sends the message, then it removes the lock. The messaging will send a request to Flow to send the message, and Flow will say, "Yes, that window is locked."

flows/e51411/vision/locks.md, 2026-09-25 (a stale lock held by a dead flow):
> We need to develop a skill to allow someone to unlock a [stale] flow lock, a lock on a [stale] flow. We should have a registry of flows even if we're working by hand, right? Your by-hand tool has a by-hand database, right?

flows/b7ba00/vision/messaging.md (same text in flows/93ba9f/vision/messagingInterface.md), 2026-09-26. This is the only record in which the living names time units, and it is about a message's age, not a lock:
> The other thing that could be there is a human-readable or, actually, an LLM-readable but more human-friendly time measure, like age. Depending on the scale we're talking about, seconds, minutes, hours, days, and months and years, right? We can use those as measures of time, like age basically.

flows/e5a0bc/vision/flow.md, 2026-10-07 (typed):
> There's also the concept of the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow. We need to be able to lock. I can't really see exactly what function this fills now but I know that it fills a function when message uses the lock later on. We don't have to make message right now but we will eventually and that lock will be useful in order to know whether the messages can or cannot reach a certain flow.

flows/f5a6e9/vision/flow.md, 2026-10-07 (STT, book comment 9 of 9, 19:09, relayed by db38f8):
> I don't think that it's Flow's job to hold messages. It's more like it's Flow's job to tell the message component later on to give it the signal that a message can now be sent. The message is going to ask for a lock, which should be time-bound so that it doesn't lock forever. If it does get a lock then the message nexus can send that object over to Flow with the message because now it has the lock. Flow told the message that it has the lock for that flow or that metaflow. The message doesn't have to know about the flows. It can also just talk in terms of metaflows. And indeed when this is done and more polished, I'm mostly going to talk in terms of meta flows.

Skill sources (skill): vision-flow.md says "Flow holds the lock on flows." and names no unit; vision-messaging.md names none.

### Conflicts and overrides

No record conflicts with another on the unit, because only one record (f5a6e9, 2026-10-07) says the lock is time-bound, and it gives no unit. The 2026-08-26 record (forfeiture when the holder is idle) and the 2026-10-07 record (time-bound) describe two ways a lock ends; the later one concerns the Message-to-Flow lock and the earlier one the Orchestrate lock. The seconds-to-years record is about message age and is not stated to apply to the lock.

---

## 2. The role field

What is open. The metaflow record has aspect, layer and topic, so a separate role field may be nothing. The records disagree over time on whether a flow has a role, what a role is, and whether voice is a role, an aspect-layer struct or a permanent metaflow.

### Records, oldest first

flows/dc1c58/notion/meta-flow.md, 2026-09-14 (notion):
> I think the flow ID is too long right now, but we can work on that gradually, replacing that scene and introducing the meta flow, basically composed of multiple main flows that have a particularly coupled communication, like message passing between the three.

flows/9993b5/vision/flowIdLayers.md, 2026-09-17:
> - The meta flow that identifies itself as the continuation, the whole, which is what psyche is going to speak to most of the time.

flows/d8df70/vision/flowTool.md, 2026-09-24:
> It's a flow container that has many flows in it: many typed flows. Typed flow meaning psyche, mind, and field, and then we're going to have sub-subroles, subtypes like that.

flows/edf227/vision/flowRole.md, 2026-10-03 (STT then pasted):
> "I think that the flow definition itself is a struct, and one of its fields is a role. The role is an enum, and one of its variants is voice. The other variants are going to be all the other roles that we create: a system audit; live psyche voice interaction; an implementation; an implementer; a vision audit. These are actually things that are better done with the prompt perfectly aligned, and then they're just running right out of the door. They're just producing the best output based on the smallest, most concentrated, highest signal-to-noise context that we can assemble."

flows/edf227/vision/flowRole.md, 2026-10-03 18:53 (typed):
> "Well either it's living interactor, an implementer, or vision auditor, or it's living interaction, implementation, and vision audit. I think that I prefer the latest."

flows/edf227/vision/flowRole.md, 2026-10-03T19:13Z (typed, his own ethos):
> ```
> Voice.{ Aspect.[ Psyche Mind Field ]
>         Layer.[ Primary
>                 Secondary
>                 Tertiary
>                 Quaternary  }
> ```

flows/5578cc/vision/ethos.md (same words in flows/edf227/vision/contextModules.md, 19:05Z), 2026-10-03 (typed; about role as a context-module kind):
> I don't see `role` as a kind here, and I don't like `kind` because it collides with our use for `kind`, which is more basic.

flows/db38f8/vision/seatNames.md, 2026-10-03:
> - field primary
> - field secondary
> - psyche primary
> - psyche secondary
> - and so on

flows/bad807/vision/ethos.md (original text in flows/aa887c/vision/ethos.md), 2026-10-04 (typed):
> I think we're going to abandon this idea that we wouldn't have an enum where each data-carrying variant carries the same type, because it creates this repetition that you can see now: `[psyche].layer`, `[mind].layer`, `.layer` is being repeated. I think rather the voice is a struct that contains the aspect and the layer, and the flow has a role, one of which is a voice. We can start leaning more on [structs] than on chaining up [variants], which ends up in an ugly Ethos pattern.

flows/bad807/vision/contextModules.md, 2026-10-04T16:42Z (typed):
> There's no role type and I don't know if we want to list the types in too many places. Where is the canonical place to find those types?

flows/bad807/vision/metaflow.md, 2026-10-04 (typed):
> What we're calling a voice, really, is this: a Metaflow with no known ending. This ending could itself become a judgment call.

flows/d4ae97/vision/flow.md, 2026-10-05 (typed, book comment):
> Also we don't want to repeat. This is a repetition. The seat, first of all, is a flow. We don't have seats. There's no seat. It's a flow. We're not going to repeat. The flow is just the flow ID and maybe something else but we're not going to repeat what's already in the voice. Actually yeah, we can say that the flow has a flow ID and a role, one of which is a voice.

flows/d4ae97/vision/voices.md, 2026-10-05:
> Actually the voice is a sort of metaflow so we should throw that into the soup somehow. The voice is a type of metaflow and then there are specialized metaflows.

> We've had tertiary and quaternary field flows since we had tertiary and quaternary. There's a tertiary-quaternary of every aspect.

flows/d4ae97/vision/flow.md, 2026-10-06:
> I'd like to make the concept of a meta flow a central concept. I see that it hasn't been brought up so that's part of my vision that's being missed. I want that brought out.

flows/d4ae97/vision/ethos.md, 2026-10-06T14:59 (typed, on `Role.[ Voice Job ]`):
> Well first of all I still don't see the meta flow. If a job is a flow ID, then why are we even using the word "job"? Just use "flow ID". Why are you going to wrap a new type with another new type? Don't double-wrap types. That's silly.

flows/f5a6e9/vision/flow.md, 2026-10-07 18:32 (STT, relayed by db38f8):
> There's a bunch of things that are false in here. I guess you could say a flow always has a role if we describe a role as maybe some kind of short camelcase expression, a string. It just describes, I don't know. I'm not even sure that a flow always has a role but maybe.
>
> A role is a voice. That's not true. A role may be a voice or a worker. Read trivial. Right. No, no, no, no, no, no. This read trivial. Right. Ordinary.
>
> This stuff is just an old system and it doesn't really correspond with the new system. Metaflow is the voice. No, Metaflow is not automatically a voice. A voice is a permanent Metaflow. It's a Metaflow that might go to sleep but can always be woken in the sense that if a message is intended for it, flow would automatically... This isn't intended for the first version but eventually it would just trigger the flow to be spawned with the right context modules depending on the message.

flows/f5a6e9/vision/flow.md, 2026-10-07 18:58 ("goal", relayed by db38f8):
> I don't think "worker" is the right term. Maybe "goal" or something like that.

flows/f5a6e9/vision/flow.md, 2026-10-07 19:01 (STT):
> I don't understand why you insist on using the structure whereby you refer to everything by flow ID instead of referring to the meta flows and then having a reference in the meta flow memory to Wispr Flow's [sic] current for it and maybe its predecessor. I don't see the point of putting that data with the flow data. It's very noisy. Your syntax, now you have all these options and I very much dislike options. I think that they're really a last resort if we can't get a better design that can work without them. What do you think? Give me some feedback on that.

flows/f5a6e9/vision/flow.md, 2026-10-07 19:04:
> Again you're making Flow the only abstraction and you're just shimming Metaflow as a tiny afterthought inside of it, which is not my vision. Metaflow is a major abstraction and it's what we mostly think about. The Flow abstraction is a lower-level thing and it's not user-facing in almost any cases.

flows/d4ae97/vision/flow.md, 2026-10-07 (comment on «Flow and Message» 2nd edition):
> A flow could exist and not be a metaflow so this structure is wrong. I guess you could make it an optional metaflow. What are we trying to show here? The only thing we need is for us to know that a flow is a metaflow. If a flow is a metaflow we'll be addressing it by its long-term metaflow name. There are flows that are not metaflows so I don't think this structure is appropriate. Anyway I haven't read the whole thing. I still have to get to the memory specification but I wanted to point that out.

flows/d4ae97/vision/flow.md, 2026-10-07 (STT):
> I want to change the name "voice" to describe the long-running seed [sic]. There's no voice, right? The variants are all of the different voice aspects directly. They're called by name:
> - psyche
> - mind
> - field
>
> They're separated by layer, right? These are kind of internal and they're going to have different functions for now.

flows/d4ae97/vision/flow.md, 2026-10-07 (STT):
> We're going to create this different flow type that is basically a meta flow. It is one of the four things and they have different types of payload but psyche, mind, and field have similar payloads. I don't know if they're going to be always the same but I think possibly that would be the case.
>
> I guess this is where we made the case to put them all under a certain umbrella since they have a similar payload. Their variant can be just one of the fields in that particular payload. The ethos, I guess, is more terse and the datom is not bigger because you already have the struct.

flows/d4ae97/vision/flow.md, 2026-10-07 (STT; "implementation" as a kind):
> I guess there's nothing against using Opus sometimes for an implementation job, which is actually maybe its own kind. This is how you keep track of your work: each implementation has its own flow or meta flow. That's brilliant. And then each of those can have a different level: primary, secondary, which corresponds with the model, and then we have the actual model.

flows/d4ae97/vision/flow.md, 2026-10-08 (STT; the metaflow as a struct, aspect first, topic a dense string):
> Those three aspects, psyche, mind, and field, I think, are even applicable for topics. If you have a psyche and then it has a topic, the non-topiced flows would just be the topic of core.
>
> We can have the focused starting point, basically the kernel, the first flows that sort of hold all of their aspect together. They think in the most general ways about psyche. They have an overview of all of psyche and all of the other psyche topics sort of go through the core. It's like there's this hub at the center, the psyche core, so it's a struct. It's just a struct.
>
> The first field is the aspect, [psyche, mind or] field:

> The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably.

(The same two passages are relayed in flows/445410/vision/flow.md and flows/f5a6e9/vision/flow.md.)

flows/d4ae97/vision/models.md, 2026-10-08 (STT):
> This primary-to-quaternary division is sort of universal in any type of metaflow or flow.

flows/edf227/vision/topics.md, 2026-10-03 (STT; cited here because it bears on topic being a variant):
> We have different subjects, topics and subtopics and these will even become variants in actual Nexus components like Mind.

flows/ebbe30/vision/aspects.md, 2026-10-09 (STT):
> I know we want to have more than one flow now for psyche, per topic, like each aspect essentially. The aspect is now, I think, part of any metaflow. It shows us which aspect of that topic it's actually taking care of.

flows/445410/vision/flow.md (same words in flows/4ddfe1/vision/core.md), 2026-10-09 (STT):
> Right, so, the topic is always there and by, well, the topic for the current metaflows that we have that essentially are [topicless] is core. Meaning—core, like they're the heart of the machine, they... are the heart of their own aspect.

flows/ebbe30/vision/metaflow-naming.md, 2026-10-09 (STT):
> Start these two topic flows with the psyche::{topic}, either core, flow, or ethos, and then the layer: primary and secondary. There are three things.

flows/73ada7/notion/metaflow.md (also flows/f5a6e9/notion/flow.md, flows/4ddfe1/notion/metaflow-ethos.md), 2026-10-09 (notion, STT, thinking aloud):
> I wanna talk about the structure of the Ethos for um, the metaflows. They're going to be, each one uh, variant of either psyche, mind, or field. So all metaflows will essentially have an aspect. And then the struct, will contain their details, such as their- their- the name of their topic, right? Which will be a, a new type which I talked about yesterday, which is a... annex uh, I'm trying to come up with a name, maybe Opus actually made some suggestions or Fable.

flows/f5a6e9/vision/flow.md, 2026-10-09 (STT, relayed by ebbe30; said on the book «The metaflow's ethos»):
> I might approve this. This looks good but it needs to land in vision, right?

flows/4ddfe1/vision/flow-names.md, 2026-10-09 (STT):
> You mean like psyche secondary or psyche primary? I want all the metaflows addressed this way and not with hashes.

Skill source (skill): vision-flow.md, "A voice is an aspect carrying a rank, `Psyche.Primary`: Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices." It names no role field and no topic.

Scope note: records about what each layer does, rather than its place in the record, were left out.

### Conflicts and overrides

- Role as a field of Flow. 2026-10-03 (edf227) "one of its fields is a role. The role is an enum, and one of its variants is voice"; repeated 2026-10-04 (bad807) and 2026-10-05 (d4ae97) "the flow has a flow ID and a role, one of which is a voice". The 2026-10-07 comment (f5a6e9) says "I'm not even sure that a flow always has a role but maybe", and calls role maybe "a short camelcase expression, a string".
- Voice. 2026-10-03/04: Voice is a struct of Aspect and Layer, and a variant of role. 2026-10-05: "the voice is a type of metaflow". 2026-10-07: "A voice is a permanent Metaflow" and "There's no voice" (the aspects are the variants, separated by layer). The later records override the role-variant reading.
- Worker. 2026-10-07 says a role may be "a voice or a worker" is false, and "worker" is not the right term (maybe "goal"). No later record names the replacement.
- Role as a context-module type. 2026-10-03 (5578cc) names `role` among kinds; 2026-10-04 (bad807) "There's no role type".
- Shape of the metaflow. 2026-10-04 Voice.{ Aspect Layer }; 2026-10-07 aspects as variants carrying a shared payload; 2026-10-08 "a struct... The first field is the aspect" (with topic and layer named in the same message); 2026-10-09 "each one a variant of either psyche, mind, or field... the struct will contain their details" (notion). The 2026-10-08 record says struct with aspect first field; the 2026-10-09 notion says variant of aspect carrying a struct; the notion rules nothing.
- Topic. 2026-10-03 topics become variants; 2026-10-08 topic is a PascalCase dense string; 2026-10-09 the topic name is "a new type" whose name is unsettled.
- Implementation. 2026-10-07 "maybe its own kind"; no record from 2026-10-08/09 names implementation among the aspect, topic and layer fields.
- No record from 2026-10-07 to 2026-10-09 gives a role field to the metaflow beyond the "maybe" of 2026-10-07 18:32.

---

## 3. Simple versus full message forms (shorthand as omitted tail positions)

What is open. The living has spoken of a simple form and a full form of the same data. The «Stored type and datom form» book reads shorthand as omitted tail positions of a struct; the question is what the living's records say that shorthand, short and simple forms are.

### Records, oldest first

flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md, 2026-08-14T18:01+02:00 (archive; shorthand in ethos shapes):
> if the anonymous struct is a bad idea, which I think it is, it
> could be a shorthand for two types, where the struct would get a
> derived name (RecordData?)

> In simple cases, that syntax will be much easier to read and
> write than referring to another type and using a whole other
> line for that type.

flows/62022e8f/vision/multiFormConcepts.md, STT, date not in record (file first committed 2026-08-30):
> You would have this multi-form concept where it's struct [STT: struck] with a different number of a different arity. It would just be the same concept, but some of the fields can be omitted [STT: emitted] depending on which arity is being used. That way, we have a simple form and a complex form without having to always write out all the fields, even if they're empty.

flows/62022e8f/notion/layerMatching.md, date not in record (notion):
> So if we had a struct and it has multiple arity forms, like a multi-form, we could call that a multi-form.

> Or maybe we can only do the variable arity for things like a vector. If it's a struct, then it would be obligatory, like in the sense that otherwise you would have to make it an option.

flows/692df8/vision/signal.md, typed, date not in record (file first committed 2026-09-15):
> You can have these shorthand types that are usually default, and then you have the more explicit longer name.

> You would have an explicit type of call to get the full explicit response type.

flows/9993b5/vision/orchestrateCommitBinding.md, 2026-09-17 (typed; shorthand for the Orchestrate lock):
> Let's make a shorthand for Flow to make a lock on something.

flows/1b8ac0/vision/messaging.md, 2026-09-21 (STT):
> It's just a shorthand for a certain configured type of messaging request, or a request to send this text into a particular harness.

flows/e51411/vision/launch.md, 2026-09-25 (the Flow tool):
> It should have a complex Flow start call and then it should have shorthands for partly preconfigured minimal calls that don't require so many arguments passed. We like this idea of having these shorthands, I call them. I don't know if there's a canonical way to name them in the industry.

flows/b7ba00/vision/messaging.md (same text in flows/93ba9f/vision/messagingInterface.md), 2026-09-26, relayed by 93ba9f:
> Even if the ordinary message API is complex, we create a shorthand version which has a shorthand response type or display type.

> Okay no, these will be different. Let's do it differently. We have the [soft] variant but maybe we even have the soft message, the soft psyche. These are shorthand. That's what I mean by shorthand and they become... You should have, at the top level, even a psyche, right? Sharing a psyche means sharing something that psyche said and it maybe even has an inner variant for the verbatim, like speech-to-text or if we know or unknown. We have the short variants too for the response:
> - The full psyche with the date and stuff
> - The short psyche, which is the context
>
> Maybe the short psyche is not so much that the date is missing, but maybe there are other fields too that are not there. It could be in the metadata but we don't need to obsess over metadata. Let's just put it in as we need it.

> You have this: not necessarily a short response but a human response. You have this human prefix and then you create these human variant responses. You have the not-human but simple. Simple is better:
> - A simple message, a simple psyche
> - A full message that can have many fields, one of which is a vector of psyches that are essentially the support for that message

flows/b7ba00/vision/messaging.md, 2026-09-26 (typed comment):
> We don't even do the soft or hard, actually. That was the wrong approach.

flows/e167d8/vision/roles.md, 2026-09-26 (STT):
> If you use datom you're going to have to set it unless you have a shorthand.

flows/edf227/vision/signalForms.md (same words in flows/dea0ba/vision/contextModules.md), 2026-10-03T18:01Z (typed book comment):
> "This is a different representation of the same fundamental data. ... This would not so much be a short form but a simple form, right? The simplified version is the part that doesn't have the flow ID. It's the same data, just represented differently, like it's cast into a different container, if you will. This is defined in ethos somewhere in signal as different types of formats that communication can happen in, basically. These simplified formats are what the common queries and responses will use and the more extended version will be for the more technical side (which can sometimes be used with the CLI, but mostly not). It is mostly used for either debugging or for other components to have some kind of more advanced compatibility or feature with each other."

flows/d4ae97/vision/datom.md, 2026-10-07 (comment on the registry record):
> The shorthand concept ties into this, where you get a certain kind of query or response that is the full-size, fully explicit, advanced expert version that has all the parameters. You have the shortened version that only contains the bits that matter for the particular use case in which these shorthands are being used, namely in the thinking machine context most of the time.
>
> For example messaging doesn't require knowing its flow ID at all. In fact it would be bad practice to try to send to a flow ID because the sender doesn't know if that is the current flow of that voice.

flows/ebbe30/vision/lojix.md, 2026-10-09 (shorthands in Ethos for Lojix, later):
> We can make shorthands for all kinds of stuff in Ethos, like easy one-off build script shorthands, packages, and basically emulate the trivial build or the options on the builds that can be overridden and all that stuff.

Skill source (skill): vision-datom.md, section "Omittable fields": "Not yet; a written datom gives every position." followed by `Deploy.{ ouranos }     ; Arity.{ 2 1 }`.

Searches of vision-raw/ and of the other flows' notion/ directories for shorthand, short form, simple form and arity found nothing beyond the notion above.

### Conflicts and overrides

- Short versus simple. 2026-09-26 (b7ba00) calls the short psyche and the simple message "shorthand" and says the short psyche may lack fields other than the date. 2026-10-03 (edf227) corrects the naming: "not so much a short form but a simple form", defined as the same data without the flow ID, cast into a different container, defined in Signal as formats. 2026-10-07 (d4ae97) again says shorthand is the shortened version with "only the bits that matter", opposite the full-size form with all parameters. None of the records says the omitted positions must be the tail positions.
- Omitted fields. The undated multi-form record says fields can be omitted by arity; the notion (undated) says variable arity may only be for vectors, since a struct field would otherwise be an option. The vision-datom skill source says omission is "Not yet". The living also dislikes options (flows/f5a6e9/vision/flow.md, 2026-10-07 19:01, quoted under question 2).
- Soft and hard. 2026-09-26 (b7ba00, typed) calls the soft/hard distinction the wrong approach, while the same day's STT record uses "soft" as the name of the variant; the typed comment is later in the relay order and the quoted STT text predates it by relay order only (both dated 2026-09-26; the order within the day is not established).
- Form versus type. 2026-09-26 "A simple message... A full message" reads as two kinds of message; 2026-10-03 reads simple and extended as the same data in different containers.
