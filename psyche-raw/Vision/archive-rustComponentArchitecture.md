# Rust component architecture — archived

## 2026-08-14 — reconsider everything; keep the Signal Nexus SEMA vocabulary and principles, not their past implementation

> Yeah, so there's a few things. One is back then I didn't
> understand the importance of designing with traits. Two is I
> understood the threefold separation of logic, but well, yeah,
> it's okay, I guess. I gave them kind of like unusual names. Maybe
> not signal is not so unusual, but SEMA probably is the most
> unusual. So I'm not bound to how things used to be done. And also
> I want to bring this up so that we're clear. The shortcut stack
> for the new syntax, I think we should just call it, so it's going
> to be a daemon also. So to differentiate it, we should call it
> maybe the ethos monolith or something like that. And on the
> signal nexus SEMA separation, I don't know, I'll do some
> research, see what this feels like in terms of the most beautiful
> software ever made in the actor or data flow space. This is
> another thing too. You know, just to give you context, so I
> thought that I didn't understand the importance of skills because
> I didn't know about the different authority of context. And so I
> thought that I would just slim down the skills to some very bare
> instructions and just leave all the documentation in more
> specific places. And now I realized this was a mistake and I
> didn't just, I guess I could have just rewound everything and
> brought everything back up, but I didn't. And now I don't think
> it's worth it to do it. But I did forget to mention that in my
> architecture, I want everything, well, I want the main engine to
> be driven by actors. And we did actually even fork the actor
> library that we were using. So there's a lot to talk about. And I
> kind of want to just reconsider everything. So yeah, I think we
> should start with a new session. And so after this, we'll start a
> new session. So right now I want you to just, I don't know, send
> some high powered researchers and investigators and thinkers to
> just sort of contemplate everything and present me with a
> proposal for the skill, the Rust component skill that is more
> elaborate, that reuses the part of my old vision that are still
> relevant. I'm not bound by the, I mean, you know, so you
> understand actually. The reason I did, like signal is obvious,
> right? The signal interface so you can see how the daemon speaks,
> what kind of things it takes in and out. So the whole point of
> everything that we're doing now, why we want ethos, datum is kind
> of, I think it's obvious because all of the data, the text data
> format suck compared to datum, just completely suck. And well,
> ethos is actually the same reason. Programming languages as they
> stand right now completely suck. And I wanted something that's
> easy to read and write that lets me see the interfaces. And
> eventually I want to write everything with ethos. But just
> letting me see what the types and the main types and the main
> traits are. The traits were something that came to me later. I
> realized that, you know, in order to think about functionality, I
> need to think about behavior. And also it came up, the problem
> came up of generics needing to be expressed in what was then
> called schema, the ancestor of ethos. So traits came up and then
> I realized how important they are in design and how I would now
> want everything, every behavior to fall under a trait, which
> essentially creates an ontology in code. And so the whole point
> of exposing nexus and sema as another, back then it was schema,
> but now ethos authored interfaces was that so that I could see
> what the main operations were inside nexus, right? What the main
> functionality was, what we would do inside the demon, like if it
> had to look stuff up or if it had to write some things or if it
> had to scaffold some things or if it had to run some algorithms
> on some data or if it had to call to make an LLM call. So that I
> could, you know, so that we could see the main types and the main
> behavior of that engine, of the inside of the demon. And then the
> same thing with sema, sema being the database engine, which I
> never really looked at close enough. I think that it's probably
> not designed to my standard at all. So that was the whole point
> was to see what, you know, to, and now we can design this better
> to see, to author the database basically. It's actually, you
> could say sema was way more important than nexus because the
> whole point of creating a real code evolution engine was that
> because through the operational editing, we could have database
> migration operations come out instantly or along with the editing
> operation because it would be this essentially sort of parallel,
> almost, you know, almost the exact same thing. And so, yeah, to
> expose the types that the database stores and for the agent, for
> both the human and the agents to easily reason about this, which
> would allow me to read it more easily and understand it. And also
> it would allow the agent to more easily understand how to
> upgrade, how to do a database migration. And also the nice
> benefit of this is what we never really did properly, but kind of
> tried when it was schemas era was to try to was to create a
> schema explanation mechanism. So essentially if I was to ask
> about a certain object through the CLI, for example, but this
> could be extended, of course, to work in Menchie [Mentci], the
> user interface that's slated to be done, was that I could point
> at a certain object and it would print out its schema and ethos
> syntax, which is very self-describing and very self-evident in
> how, because of how we name the types. And the syntax is so terse
> and so sweet that, you know, it's just, it's very easy to grasp
> what that object is by just seeing how it would be written in
> ethos. So, yeah, just go deep, look at everything, maybe put
> together a report or two, and then I'll look at, you know, you
> can tell me how you understand everything, show me some code.
> Tied up with how the old demons used to do things. Don't forget
> to bring up the actors, look into the library we're using, and
> see if our fork is now falling behind upstream. And if our fork
> is indeed a good change, and if upstream has changed, if they
> have done something that makes our fork either unnecessary or
> partly unnecessary, or if it can be done better. But yeah, just
> go crazy. Spend some agents and acquire a really good
> understanding of my vision, since I've given you such a deep
> explanation of why all of this. Oh, and don't forget, you can
> even send an agent to do the rename for both on the remote and
> the local for the shortcut ethos, right? Which, that wouldn't be
> a really good name for it, but ethos monolith, just because it's
> not going to have the nomos and the logos component, it's just
> going to straight commit to Rust. So we can think of it as more
> of a monolith, so that we can just start using ethos to write
> components. It's sort of like an incremental implementation slash
> bootstrap process. I really want to start writing and reading
> ethos and datum as soon as possible. I don't want to cut corners
> and end up with a shitty implementation, but we'll keep working
> on it and there's a lot of other things I want to start doing,
> which I want to use datum and ethos for. And we can keep the
> Signal, Nexus, SEMA vocabulary and principles, but we aren't tied
> to how they were used and implemented in the past.

— psyche, 2026-08-14T20:48+02:00 (Designer session ba906ae2),
dictated, after the miner's report on the pre-reset skill corpus
(reports/PreResetCorpus-2026-06-07/skills/). "demon" reads daemon;
"straight commit to Rust" likely reads "straight compile to Rust".
Rulings and directions carried: (a) the Signal/Nexus/SEMA
vocabulary and principles are kept, but nothing is bound to how
they were used and implemented in the past; (b) the shortcut stack
(ethos-rust) will itself be a daemon and is renamed — ethos
monolith — because it skips nomos and logos and goes straight to
Rust, as an incremental implementation/bootstrap so ethos and
datom get written and read as soon as possible, without cutting
corners; rename authorized for remote and local; (c) the main
engine is to be driven by actors; the actor library was forked and
the fork's standing versus upstream is to be investigated; (d) the
skills slim-down is recognized as a mistake (context authority was
not yet understood), not worth rewinding wholesale — instead the
rust-component-architecture skill is to be made more elaborate,
reusing the still-relevant parts of the old vision, proposal to be
presented; (e) the why of it all: ethos and datom exist because
text data formats and current programming languages suck; ethos
must let the psyche see interfaces — the main types and main
traits; every behavior falls under a trait, creating an ontology
in code; nexus is authored in ethos so the daemon's main
operations are visible; sema — the database engine, likely not yet
at standard — is authored in ethos so the stored types are
visible, and matters more than nexus because operational editing
should yield database migration operations along with the edit;
(f) a schema explanation mechanism is wanted: point at an object
(CLI now, Mentci later) and its ethos prints — self-describing,
self-evident; (g) the psyche will personally research the most
beautiful software in the actor/dataflow space to feel out the
Signal/Nexus/SEMA separation.
