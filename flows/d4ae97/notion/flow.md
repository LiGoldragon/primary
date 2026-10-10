# Flow notions

## A shorter flow id; a tool to make harness ids handleable
Context: thinking aloud ("I have so many ideas").

> I don't want to see the... Actually can we get a tool right now? Oh my God I have so many ideas. I don't really want to see. Well I guess it's good to see the flow ID still. I think we can make it shorter.
>
> I wonder where the things line up in terms of the characters when we compare the words with the alpha-numerical or whatever the alpha-numerical encoding is that we use for hashes right now. This is essentially just copying the system that they use in the harnesses themselves but maybe we can actually make a tool to convert that into something more handleable.

-- psyche, STT, 2026-10-07.

## The metaflow record as a fixed-size rkyv unit pointing at the current flow
Context: thinking aloud after commenting on «The queue and the waking rule», section 3; framed as a thought to verify or refute.

> Oh right, the metaflow type. If we make it, I want to talk about essentially RKYV, the format, the archive, like our database format. If we have the metaflow type and it doesn't have any vectors, then it's just this unit of data that has exactly the same size. You essentially end up with a series of them, which I imagine is easier to query.
>
> If we only have one of its fields, right, as the current flow that this metaflow corresponds to, that's mostly what we need. Maybe there's more than one registry to get data about a metaflow. We also have the concept of linking: this pointer, essentially this metaflow entry, is sort of acting as a pointer in one of its capacities to the current flow that it corresponds with. We can also use another pointer somewhere else to hold a different kind of data, the slow aspect of the database.
>
> Here I am optimizing before we even... It's kind of crazy but it's just a thought I wanted to sort of verify or refute for myself by actually checking.

-- psyche, STT, 2026-10-08.
