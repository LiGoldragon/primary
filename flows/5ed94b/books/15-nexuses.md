Presentation.{ «Nexuses» }

What a Nexus is, how it is built and reached, what it keeps, how it is updated without stopping, and which Nexuses the system is made of. A Nexus is one of our long-running programs together with its ways in. A socket is a door a program listens on. Signal is the binary message form Nexuses send each other. A datom is our small structured text form.

## 1. What he wants

### A Nexus is a kind of thing

Nexus names a style of component, not one program.

> nexus is not a thing, its a kind of thing

-- typed, recorded 9 September 2026

> The word Nexus is our word for the style of component that speaks signal and uses a similar database.

-- spoken, 10 September 2026

It runs the way a background service does, but "daemon" is only a hint for a machine that thinks in daemons, never its name. Every Nexus carries the word in its program name, and in speech the short name is enough.

> Also, we should make an invariant that the daemons are not called daemons but Nexus. So it should be Orchestrate Nexus, and all Nexuses should be like that.

-- spoken, 26 August 2026

> in everyday speech, orchestrate-nexus will be called orchestrate, etc

-- typed, 27 August 2026

### A library and a running program

There is one shared Nexus library that defines what every Nexus is, and each Nexus is a long-running program built on it.

> a nexus is a daemon. every component we will build will be a nexus. so the nexus repo is the library that defines the core of a nexus component, which is a daemon

-- typed, 10 September 2026

### Every component is a Nexus

The old names for components go; everything built from now on is a Nexus, and what was built otherwise is rewritten.

> But everything we're going to build is going to be a nexus now, and anything that has already been built that did not take the shape of The nexus is going to be rewritten.

-- spoken, 19 August 2026

The reason is that sameness makes the machine reliable.

> well, maybe we should make it a nexus now because consistency is very good for AI models.

-- spoken, recorded 27 August 2026

### Three faces: what it says, does, and keeps

A Nexus has three layers. Signal is what it says, the Nexus layer is what it does, and Sema is what it keeps.

> There are basically three different layers of the runtime:
> - The Nexus: the process or Nexus core, which is the process part.
> - The Sema: the storage part.
> - Signal: sending and receiving requests and responses or replies or whatever.

-- spoken, 13 September 2026

The doing layer holds ongoing work, such as anything that must hold a lock until it ends.

> The nexus layer describes processes that are ongoing, like the operating system update operation or assistant call, basically something that has to lock. It's an actor.

-- spoken, 13 September 2026

An outside tool the Nexus runs, such as a system build, is one of those processes, wrapped behind the Nexus's own requests.

> Lojix shells out to Nix. That's Nexus. Nexus encapsulates processes

-- spoken, 14 September 2026

### How one is reached

A Nexus opens at least two sockets: an ordinary one for any peer, and a meta one that acts as its root user, through which it is configured.

> we should say *at least* two sockets. some nexus might need more than 2 levels of access.

-- typed, 19 August 2026

Each socket has a default command-line client, packaged with the Nexus but separate from it. The meta client takes the component's name plus "-meta", as in orchestrate-meta.

> no, the clients are not the nexus. for now, default clients are packaged with the nexus

-- typed, 27 August 2026

> meta cli names is <component>-meta.

-- typed, 12 September 2026

The clients start things up, then stay on for debugging and testing.

> the cli is for bootstrap and later on can be used for debugging and testing even after it isnt used in production anymore

-- typed, 19 August 2026

### Wire contracts and the graph

A Nexus speaks only the contracts it was compiled with: its own two, plus one for each Nexus it talks to.

> So all Nexus components speak only pure signal, the contracts which they are compiled with

-- spoken, 19 August 2026

Signal means binary messages and nothing else.

> Everything is signal messages, meaning RKYV binary messages. That's what signal means.

-- spoken, 8 August 2026

The Nexuses form a graph. Every connected pair shares an ordinary link; only some pairs share a meta one (proposed).

### What it stores

Everything a Nexus knows lives inside it as typed values, kept in its own database rather than loose in memory.

> Everything is in the daemon.

-- spoken, 8 August 2026

> It has every object in its own specifically typed object, right? A specific type for every kind in Ethos

-- spoken, 8 August 2026

> Not in memory, in their database. So they can fetch it back.

-- spoken, 8 August 2026

It starts with no arguments. Its defaults are built into it and saved to a new database; a database that already exists brings its saved settings back. Changes come in over the meta socket.

> There should be no bootstrap binary. So, in terms of configuring the Nexus, obviously, well it's going to have default configuration.

-- spoken, 26 August 2026

> But yeah, so it has a default configuration by default and create an interface on the meta socket to allow for changing that configuration.

-- spoken, 26 August 2026

When the shape of stored records changes, the database is upgraded with it.

> We're going to need to handle database upgrades or the database when the records change.

-- 25 September 2026

### How versions rotate

Because each Nexus stands alone, the system can be rebuilt one Nexus at a time, aiming at no downtime at all.

> It allows us to recompile the system incrementally by recompiling one Nexus at a time, and then eventually with a full update mechanism in place to have a system that has zero downtime and that can incrementally recompile itself.

-- spoken, 19 August 2026

Each service runs a stable and a next side by side, on different sockets.

> Then you can run both side by side when you do a migration. You can start into the Next service and then the stable version becomes the same as the Next and that would be the next step.

-- spoken, 26 September 2026

Next becomes stable once every flow has moved onto it; then the newer version goes onto next.

> If all the flows are on the next socket now, next can become stable, and then we can put the next version on next.

-- typed, 30 September 2026

### The Capsule

The Capsule is the component that makes the place a flow runs in.

> Yeah I think I picked the right word. It's going to be called Capsule.

-- typed, 2 October 2026

Its first form is the semi-sandbox: its own sockets and store, with only the login files copied over.

> You could create and use a different socket. Just create the environment yourself. You can make this semi-sandbox.

-- spoken, 2 October 2026

Later it encrypts the sensitive parts of the disk.

> It doesn't have to encrypt the whole file system, just the parts where we put sensitive stuff.

-- typed, 2 October 2026

### The Nexuses by design, and what each owns

**Orchestrate** reserves paths, so two flows never edit the same file. It is deployed for every user.

> our first work will be a simple orchestrate nexus that reserves paths to make dead-simple datom-syntax path reservation possible for edit coordination.

-- typed, 25 August 2026

**Flow** launches flows, knows their state from the harnesses, holds the lock on flows, and lets them be named.

> Flow could have the lock on the flows so that we can lock it and also address it by name instead of by Flow ID.

-- typed, 2 October 2026

**Message** carries messages between seats, drawing on Flow.

> Message can get the data from Flow, and Flow can put a lock on some stuff.

-- 18 September 2026

**Mind** takes over the system's memory: the files, indexes and reports kept by hand today, and checked facts with a date and a trust level.

> The mind will kind of replace all this reporting and keeping track of which repositories are involved, what kind of knowledge and witnesses

-- spoken, 5 September 2026

> The psyche is for storing psyche, and the mind is for storing trustworthy information with a date and a trustworthiness kind of gauge.

-- typed, 16 September 2026

Mind's database will grow largest, so its size must be kept in hand, by spreading it across machines or archiving it.

> But the Flow's memory will live in mind, and so mind will become our most bloated component in terms of the database quickly.

-- typed, 17 September 2026

**Psyche** keeps his words, the way Mind keeps the system's facts.

> Psyche Nexus is going to replace how we log Psyche and Mind.

-- 25 September 2026

**Horizon** answers what the cluster looks like right now, such as which machine can run a sandbox.

> We need to make the Horizon a proper nexus, so the current state of the cluster can be queried from that.

-- 19 September 2026

**Transcript** serves the sessions' records.

> The transcript component is misimplemented. We need to make a nexus out of it and use datom syntax with the CLIs.

-- typed, 16 September 2026

**Curriculum** builds the skills (see question 2). **Field** queries the state of the system.

> This would be a script that gets ported eventually to the field nexus. Functionality for the field means querying stuff about the system, any kinds of stuff.

-- 20 September 2026

**Edit** edits datom by structure.

> Edit is the right name. The edit nexus

-- typed, 17 September 2026

### Topics become Nexus variants

Subjects and topics become typed variants inside a Nexus such as Mind. A new variant is submitted, approved, added to Ethos, and the Nexus is rebuilt.

> We have different subjects, topics, and subtopics and these will even become variants in actual Nexus components like Mind.

-- spoken, 3 October 2026

### What a Nexus never does

It never receives text: the client turns datom into Signal.

> the Nexus only gets signal. The CLI translates datom into signal, so that has to be clear everywhere in the skill, in the vision.

-- typed, recorded 15 September 2026

It never polls. It is told of each change, and goes quiet when nothing changes.

> 4. this is true and approved as vision

-- typed, 27 August 2026, approving "Polling is forbidden; a correct system goes quiet when nothing changes."

It never grows without limit. A Nexus serves one domain, and when it grows too large, part of it splits off.

> a nexus deals with a domain, and if its features grow too many, then spliting out one or more nexuses out of it should be considered.

-- typed, 27 August 2026

## 2. What exists today

Witnessed in the running system today. Four Nexuses run. Orchestrate 0.37.0 holds path reservations on its ordinary and meta sockets. Flow 0.23.0 runs twice, as stable and as next, each with its own pair of sockets and its own configuration step. Message 0.19.0 runs as stable and next too, described as a durable message ledger. Lojix 8.1.0, the deployment Nexus, runs system-wide. The older message service no longer runs. No Mind, Psyche, Horizon, Transcript, Curriculum, Field or Edit Nexus is running. The installed skill that describes the running Nexuses still names older versions (orchestrate 0.35.0, flow 0.12.2 and 0.17.4), so it is out of date.

## 3. Questions

**1. Is there a Nexus core library that keeps the three layers apart at compile time?** Say Flow's message-handling code tries to write straight to its database.

> I think I was overthinking the whole "nexus-core" runtime concept.

-- typed, 10 September 2026

> The Nexus core library has all of the interfaces and kinds defined for how to build metaNexus and it has the machinery to make sure, ideally at compile time, that there is no signal-actor-to-sema-actor communication possible.

-- typed, 14 September 2026

Answer yes if the shared library should refuse to compile that write, so everything passes through the Nexus layer.

**2. Does the Curriculum Nexus keep the skill texts in its own database?** Say a skill line is changed.

> We take control of that state, and we can reset it through Nix, of course, or repopulate it, reseed it from Nix. There's a reseed service part that recreates a basic seeded curriculum.

-- typed, 17 September 2026

> because if curriculum is a nexus, we can't have any data there because it's going to keep rebuilding it. We need curriculum data.

-- typed, 17 September 2026

Answer 1 if the skill texts live in a separate data store and Curriculum holds only its own state, seeded from Nix. Answer 2 if Curriculum's own database holds them.

**3. How does a Nexus put datom into a prompt without knowing datom?** Say Message delivers a message into a seat's prompt as datom.

> because the Nexus component cannot be involved in texturalizing signal, because it would just destroy the beauty and the simplicity of the system.

-- spoken, 19 August 2026

> how does Nexus send datom to places without needing to know how to deserialize and serialize datom itself? Interesting.

-- typed, 3 October 2026

Answer 1 if the client or harness hook at the far end turns the Signal into datom. Answer 2 if a separate datom Nexus does the translating for every other Nexus.

**4. Does every new version get its own socket name?** Say Flow 0.24.0 goes onto next while sessions hold the current sockets.

> these services can have a Next component that has a different socket.

-- spoken, 26 September 2026

> Maybe we can get the short version of the hash of the version of Codex that we're using for it, so that each socket will have a different name. That way, we can move the next to the stable without changing the socket name, so it doesn't break any of the sessions.

-- typed, 30 September 2026

Answer yes if each version gets its own socket, named from that version, and "stable" and "next" only point to one.
