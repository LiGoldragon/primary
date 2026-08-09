# Major recovery effort — repos are ethos, nomos, logos; recover the component standard

Captured 2026-08-08 (~11:30Z), designer session. Context, brief: after the
daemon-inspection report showed the daemon track alive in `ethos-engine`/
`logos-engine` and threatened by deletion beads, the psyche ordered
recovery. Verbatim:

> im too angre to read all this right now. do a major recovery effort
> right now. I want the repos to be called ethos nomos and logos
>
> they will each have a signal-XXX and meta-signal-XXX repo, which will
> hold the ethos describing the types of the messaging layer, which we
> call signal, and always have.
>
> we can still have a core-XXX repo for each, if you think that wise or
> useful, otherwise all the logic can live in the main repo.
>
> Ask me your most important questions while you have agents get started
> on that
>
> be brief, im not in the mood. been working for a month building the
> wrong thing. Never count on agents to see that something is going the
> wrong way.
>
> I think the biggest lesson from this is that we need to routinely look
> at the very high-level view of what we're building, because then it
> would have been obvious to me right away. And I have, you know, used
> this concept of high-level view, showing me the high-level view with
> agents before, but I've never seen an agent pull it off. It's like they
> don't understand how to explain their project in simple terms. Like,
> here's this repo, here's, like, the concept of what it is and how much
> it does, and, like, I don't know, maybe you want to, like, send an
> agent on a research about this. Like, how do you explain an engine
> simply in a very high-level view? Like, let's say you had a whole day
> to explain, maybe not a whole day, but, you know, like, that would be a
> very big engine, but let's say if you only had, like, half an hour to
> explain something to someone who's coming on to a project, you would
> want him to have, like, a very clear view of the whole engine from a
> high level. That's really what I mean.
>
> And also, I can be blamed for a big part of this, which is I wiped, I
> completely demolished or significantly altered the workspace and the
> skills and everything, how the agents were being trained. And I think
> part of that was essentially this standard of how we create components.
> And all the components had the same overall architecture. They were a
> daemon that spoke signal. So you should send an agent to recover that.
> What's that architecture that we mistakenly thought was still
> understood by agents, but I never even really considered that my big,
> huge cleanup actually took that away. And now agents thought they were
> just writing like, they forgot that all my components have to be like
> this. So it's like, it's a bunch of signals speaking. And I want to
> actually be very clear about the terminology here so we don't fucking
> get lost again. So signal, right? Tell me what signal is. Let's start
> from the basics. What is SEMA? What is Nexus? I think everybody's
> completely fucking confused on what I'm actually meaning when I say
> these things because of how things have been brought up to me. The
> questions have shown me more and more confusion and I didn't actually
> clue in that everybody's totally fucking confused and lost on what I
> actually mean. So go dig in the past. Find out when that big, huge
> cutoff happened when I decided I need to clean all my skills and change
> everything and find everything before that. And I mean, spirit should
> show you how this works, right? It's a daemon. It should have two CLIs,
> which are just proof of concept. All those CLIs are short-term shims
> that we use to talk to the daemons. But eventually this is all just
> going to be a giant sort of cluster of components that exchange signal
> messages with each other. And there will be like a few different entry
> points. But yeah, the CLI is just like, it's a way to work ourselves
> up. Like eventually the LLM models will be trained not in text anymore,
> but in signal, in binary signal, which is way more dense and carries
> way more information per bits than any of that text crap. So that's
> what's going to give rise. This is why I'm going to have to head a
> multi-billion dollar AI company to show the world how you do this
> properly because everybody's still doing text like monkeys. And it's
> wrong. And this is how we're going to get there, bits by bits and
> component by component. So the daemon doesn't really speak string.
> Although for now they're records that will hold string fields, but it
> doesn't think in strings at all. And eventually even all of the string
> part of language will be replaced by a completely specified, fully
> typed binary system of enums and structs and scalar values.
