## Refer to metaflows, with the metaflow's memory holding its current flow and maybe its predecessor; options are a last resort

Context: his comment 5 of 9, 19:01, on `Voice.{ Psyche Primary }` in the three written flows, whose records carried `Option<Metaflow>` and `Predecessor.Option<FlowId>`. Relayed by db38f8; "Wispr Flow's" left [sic] by the relayer.

> I don't understand why you insist on using the structure whereby you refer to everything by flow ID instead of referring to the meta flows and then having a reference in the meta flow memory to Wispr Flow's [sic] current for it and maybe its predecessor. I don't see the point of putting that data with the flow data. It's very noisy. Your syntax, now you have all these options and I very much dislike options. I think that they're really a last resort if we can't get a better design that can work without them. What do you think? Give me some feedback on that.

-- psyche, STT, book comment, relayed by db38f8.

## Metaflow is the major abstraction, what we mostly think about; Flow is lower-level and almost never user-facing

Context: his comment 7 of 9, 19:04, on the Memory block of proposal 2. Relayed by db38f8.

> Again you're making Flow the only abstraction and you're just shimming Metaflow as a tiny afterthought inside of it, which is not my vision. Metaflow is a major abstraction and it's what we mostly think about. The Flow abstraction is a lower-level thing and it's not user-facing in almost any cases.

-- psyche, STT, book comment, relayed by db38f8.

## Metaflow kinds and payloads: four things; psyche, mind and field have similar payloads; sessions on spirit, intent, vision

Context: said on 2026-10-07 on Flow's metaflow kinds; relayed by Psyche Opus d4ae97 with elisions marked by it.

> We're going to create this different flow type that is basically a meta flow. It is one of the four things and they have different types of payload but psyche, mind, and field have similar payloads. ... Their variant can be just one of the fields in that particular payload. ... What's the name that we put them all under, these three that are very similar, or are these going to actually diverge and take their own shape? Maybe they subdivide into their own subcategory. ... I'm actually trying to start a session to work on spirit and then I would have a session to work on intent and a session to work on vision. That's what they are so we don't need all of them at the same time.

-- psyche, STT, relayed by d4ae97.

## The thread title names no model; the word-based id, three words or maybe two

Context: same day; relayed by d4ae97 with elisions.

> When we write the name of the thread in the harness, we don't actually mention the model because when I go into Claude I know that I'm talking to Claude, right? I don't need to know that it's Opus. ... I'd rather see the word-based one. I think it would be cool to have this word-based translation that actually works. Let's see if we can do that with three words, maybe even two.

-- psyche, STT, relayed by d4ae97.

## The topic of the topicless metaflows is core: the heart of their own aspect

Context: said 2026-10-09; raw record 445410 vision/flow.md; relayed by 4ddfe1 and 445410. Transcription corrected by the relayer: "[topicless]".

> Right, so, the topic is always there and by, well, the topic for the current metaflows that we have that essentially are [topicless] is core. Meaning—core, like they're the heart of the machine, they... are the heart of their own aspect.

-- psyche, STT, relayed by 445410.

## The Flow Nexus vision skill may split along the code: vision-flow, flow-ethos, then memory-ethos, signal-ethos; signal first

Context: same message, 2026-10-09, on «The metaflow's ethos»; relayed by ebbe30.

> I might approve this. This looks good but it needs to land in vision, right? So let's have that part of things done and then all of the books can be redone also. This doesn't require heavy judgment, right? Essentially we could even break up the skill, if it gets too big, with the code into modules that are about the code, right? You would have, let's say, vision-flow, this is what we're talking about: flow-ethos. If that gets big you can even go: psyche, flow, memory-ethos, signal-ethos, just ethos for the rest. If the signal and the memory files get really big, signal is probably one of the first that you'll want to separate because of how it is. Essentially if you load that skill, this is how we would want to see it currently, according to the latest check with the living: this particular nexus talk, the Flow Nexus. We could even, I don't know, maybe call it Flow Nexus also in the skill. That way in the description it can say, "This is the Flow Nexus vision."

-- psyche, STT, relayed by ebbe30.

## The topic is uncapitalized: core, ethos; it is the core:Name type, a camelCaseExpression with runtime checks on creation

Context: typed 2026-10-09 after 445410 wrote a title as { Psyche Core Secondary 445410 }; corrects the PascalCase of the 2026-10-08 record above; relayed by 445410 and 9fed42.

> but technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one

-- psyche, typed, relayed by 9fed42.

## A new flow's first last response is a presentation of its context in its role, after subflows reinforce it; never "ready"

Context: same typed message, 2026-10-09; relayed by 445410 with an elision marked.

> The worst thing to make a new flow do is to tell it to just say, "You're ready." We need to tell flows, if they don't have it, to start with a startup task: their first last response is to give a presentation of their context, to distill their context for a vision. ... That's what their first last response is. Their first goal when they loaded up all their context is to take all this context now, get some sub-agents to ask questions, reinforce your context, and then give a presentation. A presentation according to your role, which is described when you load that flow properly with the skill for its role, for its aspect, and for its layer, and for its topic

-- psyche, typed, relayed by 445410.

## Core psyche keeps all psyche within psyche; topics talk across aspects at the same layer and shared topic; field goes through mind unless psyche spoke to field

Context: his comment on 445410's «The new flows, as they run», 2026-10-09 20:41, in part; relayed by 445410 and 9fed42 with an elision marked.

> Somebody should keep the core psyche, and the core psyche keeps track of all of the psyche within psyche. The topics can essentially talk at the same layer, right? If there's a psyche ethos secondary and there's a mind ethos secondary (meaning there's a mind flow with the ethos topic), they can start talking to each other in terms of implementation because the mind is implementing, but the psyche is seeing. When the psyche gets updated, if we're in the development mode like now, then the mind of the same topic can actually communicate with the same layer and in a shared topic. And this is true of the field, though. The field should go through the mind and not to the psyche directly unless the psyche just spoke to the field. This should be universal in terms of the aspects. ... Let's start just implementing them even before I comment, or modifying when I comment, etc.

-- psyche, STT, book comment, relayed by 9fed42.
