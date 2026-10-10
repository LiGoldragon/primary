# Distillation candidates — Nexus

Gathered by subflow acbb6006. Records are quoted verbatim; agent context is kept apart. No distilled statements are composed here.

---

## Subject A: What a Nexus is — definition and naming

**A1.** id: 55d18f4f (2026-08-08T11:28Z), rustComponentArchitecture.md

> "And I think part of that was essentially this standard of how we create components. And all the components had the same overall architecture. They were a daemon that spoke signal. [...] It's a bunch of signals speaking. [...] It should have two CLIs, which are just proof of concept. All those CLIs are short-term shims that we use to talk to the daemons."

**A2.** id: e06e4c07 (2026-08-19T13:49+02:00), flows/e06e4c07/vision/nexus.md — dictated

> "There's something else I want to talk about before we get deeper into creating this component, which is vocabulary related. [...] instead of calling them the rest components or the daemon CLI signal components and all of that stuff, we're just going to say another Nexus. Or if we say a Nexus, like when we aren't being specific. So there's the Nexus part, which is the execution engine inside a Nexus. And the same way that we talk about a man when we're really talking deeply, we talk about his heart or his soul. It doesn't mean that we are saying that we should take the heart out and that everything else in the body should be excluded [...] So we can still talk about the whole thing as a Nexus [...] each Nexus has for now a client that we write by default, or two clients, because each Nexus needs to have two sockets, right? [...] all clients will have to talk to the Nexus, regardless of which socket, in pure signal, in signal, which is fully binary [...] all Nexus components speak only pure signal, the contracts which they are compiled with, and two of those contracts are its own, one for its regular socket, one for its meta-socket."

**A3.** id: e06e4c07 (2026-08-19T14:33+02:00), flows/e06e4c07/vision/nexus.md — typed

On the Nexus part being the execution engine and the whole also called a Nexus:

> "a. yes"

On whether to rename the skill nexus:

> "why is that relevant?"
> "Yes, I want the rename. I also want a nexus repo (if there is one, it probably doesnt fit the role I now have for it) which will explain the principle, and potentially even hold the nexus traits"
> "We could rename the current Nexus (the "actor/interface/abstraction" for execution) as NexusCore; the heart of this nexus; where all the decision-making happens."
> "so 'The execution engine inside it is also called the Nexus' would become 'called Nexus Core'. Feedback"

On "A Nexus speaks only the contracts it is compiled with":

> "how about 'signal contracts'?"

On "and those of every peer Nexus it talks to":

> "some vertices will not have the meta access. its case by case. so that statement is incorrect"

**A4.** id: e06e4c07 (2026-08-19T14:51+02:00), flows/e06e4c07/vision/nexus.md — typed

On "A Nexus is a daemon with two sockets":

> "we should say *at least* two sockets. some nexus might need more than 2 levels of access."

On "its two default CLI clients":

> "then this would become a default cli client per socket. the cli is for bootstrap and later on can be used for debugging and testing even after it isnt used in production anymore"

On traits lines proposed:

> "this is good. deploy it"

**A5.** id: e06e4c07 (2026-08-19T14:56+02:00), flows/e06e4c07/vision/nexus.md — typed

> "re vertices: then I was trying to say edge. not all edges will have meta access (if we think of both socket as a single edge. said otherwise, not every two vertices will have a meta edge). We could use the word edge instead of contract."

**A6.** id: e06e4c07 (2026-08-19T16:47+02:00), flows/e06e4c07/vision/nexus.md — typed

On "A Nexus is a vertex in the graph of nexuses. An edge joins two vertices and carries one contract: every connected pair has an ordinary edge; only some pairs have a meta edge. A Nexus is compiled with the contracts of its own sockets and of every edge it has.":

> "the nexus line is good."

**A7.** id: 01a03d6e (2026-08-26T10:10:32.842Z), flows/01a03d6e/vision/nexus.md — typed

> "Also, we should make an invariant that the demons are not called demons but Nexus. So it should be Orchestrate Nexus, and all Nexuses should be like that. So we should make that clear in the Nexus skill."

(Speech-to-text: `demons` → `daemons`.)

---

## Subject B: Privileged vs ordinary sockets; meta socket; configuration

**B1.** id: 98fbfa47 (2026-08-09T12:30Z), flows/98fbfa47/vision/metaSignalNotOptional.md — dictated

> "I'm looking at your draft and I would like to say that the metasignal is not optional because otherwise there's no way to configure the daemon."

**B2.** id: 98fbfa47 (2026-08-09T12:30Z), flows/98fbfa47/vision/metaCliIsComponentDashMeta.md — dictated

> "And the meta-cli is obviously just the name of the component dash meta."

**B3.** id: e06e4c07 (2026-08-19T13:49+02:00), flows/e06e4c07/vision/nexus.md — dictated

> "one of these sockets, the meta-socket, is going to be privileged. And sort of like any system needs a root user, if only in order to configure it and to do privileged operations."

**B4.** id: 01a02fd5 (2026-08-23T20:28:43+02:00), flows/01a02fd5/vision/nexuses.md — typed

> "all nexuses have a meta socket"

**B5.** id: 01a03d6e (2026-08-26T11:38:49.521Z), flows/01a03d6e/vision/nexus.md — typed

> "only problem is the bootstrap binary. There should be no bootstrap binary. So, in terms of configuring the Nexus, obviously, well it's going to have default configuration. And we can make that more sophisticated later on but it can just have a constant in the executable with a default configuration."

> "And because it has a default, well first it should try to get its state from the default location for its Sema database. And then if that database doesn't exist or if, well, if the database exists then it should have the configuration in it. Because the default configuration when creating a new database should set the configuration as the defaults in the database."

> "But yeah, so it has a default configuration by default and create an interface on the meta socket to allow for changing that configuration."

**B6.** id: 01a03d6e (2026-08-26T11:51:46.649Z), flows/01a03d6e/vision/nexus.md — typed

> "this is a problem; new values must be accepted otherwise it's not doing what we want."

> "there is a valid idea behind this however; on a never configured nexus, the ordinary socket could get a configure interface which works but rejects if already configured."

**B7.** id: 01a03d6e (2026-08-26T11:52:03.246Z), flows/01a03d6e/vision/nexus.md — typed

> "we dont need to implement that now however"

(B7 defers B6's second proposal. B5 supersedes any pre-existing bootstrap-binary or external-config-file approach.)

---

## Subject C: Ethos-monolith becomes a Nexus; everything will be a Nexus

**C1.** id: psyche-raw/Vision/rustComponentArchitecture.md (2026-08-14T20:48+02:00, session ba906ae2) — dictated

> "we can keep the Signal, Nexus, SEMA vocabulary and principles, but we aren't tied to how they were used and implemented in the past."

> "I want everything, well, I want the main engine to be driven by actors."

**C2.** id: e06e4c07 (2026-08-19T13:49+02:00), flows/e06e4c07/vision/nexus.md — dictated

> "everything we're going to build is going to be a nexus now, and anything that has already been built that did not take the shape of The nexus is going to be rewritten."

**C3.** id: aa4c7747 (2026-08-24), flows/aa4c7747/vision/ethosMonolith.md — typed

> "monolith: whatever shape it is taking already will do. If its an executable library, we'll make a nexus out of it after it becomes usable."

**C4.** id: aa4c7747 (2026-08-24), flows/aa4c7747/vision/ethosMonolith.md — typed (later in same session; supersedes C3)

> "And I think that we need to just go straight for a nexus. So it has to be written as a nexus. And we need to break down what the things that we're going to deal with, which we know, like the Ethos files and their locations, and what will classify or index these locations, and what will specify the system that these files will build, which are going to be Rust generations, like regenerated Rust files. And then we need to isolate the traits, which is the ways in which these things, the ways these things interact, and put the proper names on them."

**C5.** id: aa4c7747 (2026-08-24), flows/aa4c7747/vision/ethosMonolith.md — typed

> "right, so we need ethos-monolith to bootstrap it. We should call it ethos-cc (compiler compiler); would that be an accurate name for it? And ethos-zero because its version zero which will bootstrap ethos in the nexus trinity stack (with nomos and logos nexuses)"

**C6.** id: b675f3d9 (2026-08-26), flows/b675f3d9/vision/ethosMonolith.md — typed

> "5. Then we'll make it a nexus. Everything will be a nexus; the consistency will create reliability and increase the quality and clarity"

Note: C3 and C4 are from the same session; C4 supersedes C3 ("go straight for a nexus" overrides "whatever shape will do"). C6 is the most recent; it restates the universal rule (everything will be a nexus). Vision/ethosMonolith.md carries the distilled statement for this topic.

---

## Subject D: Deployment — Orchestrate Nexus

**D1.** id: aa4c7747 (2026-08-25), flows/aa4c7747/vision/orchestrate.md — typed

> "our first work will be a simple orchestrate nexus that reserves paths to make dead-simple datom-syntax path reservation possible for edit coordination."

> "the old orchestrate code should not be considered sacred; we are starting with a simple component that has a normal and meta socket; MVP"

**D2.** id: 01a02fd5 (2026-08-23T20:28:17+02:00), flows/01a02fd5/vision/metaOrchestrate.md — typed

> "if meta-orchestrate was removed, the work was done incorrectly"

**D3.** id: 01a02fd5 (2026-08-23T20:29:25+02:00), flows/01a02fd5/vision/metaOrchestrate.md — typed

> "restore the meta-orchestrate binary."

**D4.** id: 01a03d6e (2026-08-26T10:10:32.842Z), flows/01a03d6e/vision/orchestrateDeployment.md — typed

> "Well, the previous Orchestrate is broken, so I don't care about it. So we don't care about the old deployment. It's actually just creating problems because agents try to use it and it doesn't even work. So what I would do is just ditch the old Orchestrate."

> "So I would just, if it can do what we need it to do, which is just register paths, then it's good enough for now."

> "then we just deploy it right now in an environment without any conditions as a standard thing that we do for all users. [...] So it should be in the home for now anyway [...] Don't put it behind some kind of gate on Creo OS, just unconditional deployment approved now."

(Speech-to-text: `Creo OS` → `CriomOS`.)

> "But yeah, just go ahead and deploy and replace the skill. So just go ahead and just plow that through: new Orchestrate skill to match, deploy without conditionals. just unconditional deployment approved now."

**D5.** id: 01a03d6e (2026-08-26T11:38:49.521Z), flows/01a03d6e/vision/orchestrateDeployment.md — typed

> "The rest is good, although you're probably going to want to wait for the new orchestrate to be deployed before we change the edit coordination skill. But go ahead and make the changes and then test them and then deploy and then make the rest of the skill changes. But you can change the Nexus skill right away."

**D6.** id: 01a03d6e (2026-08-26T13:25:37.631Z), flows/01a03d6e/vision/orchestrateSkill.md — typed

> "actually, the orchestrate skill shouldnt cover any of the meta ops"

**D7.** id: 01a03eda (2026-08-26T16:55:46.618Z), flows/01a03eda/vision/orchestrateRealization.md — typed

> "looks good. implement and deploy"

Note: D4 supersedes any prior Orchestrate deployment approach. D2/D3 (meta-orchestrate must be present) are consistent with B4 (all nexuses have a meta socket) and stand. D7 is a working-instruction record — **flagged as possible impurity** (see below).

---

## Subject E: Actor library (Kameo)

**E1.** id: psyche-raw/Vision/rustComponentArchitecture.md (2026-08-14T20:48+02:00, session ba906ae2) — dictated

> "I want the main engine to be driven by actors. And we did actually even fork the actor library that we were using."

**E2.** id: 15b67974 (2026-08-21), flows/15b67974/vision/actorLibrary.md — typed

> "Re arc mutex ban: I dont like the approach anyway. I want to review the actor library we use, and if it is well documented in the nexus skill"

**E3.** id: 15b67974 (2026-08-21), flows/15b67974/vision/actorLibrary.md — typed

> "there is no ban of arc mutex. the whole actor subject deserves its own discussion in another flow"

**E4.** id: 15b67974 (2026-08-22T13:39+02:00), flows/15b67974/vision/actorLibrary.md — typed

> "I want to dedicate a flow to the actor question. Everything was done by previous flows that received little to no guidance on design in this respect. Distrust it all, including our fork."

**E5.** id: 15b67974 (2026-08-22T15:19+02:00), flows/15b67974/vision/actorLibrary.md — typed

> "re actors: we are definitely using kameo actors in nexus. I just havent designed the standards of use"

Note: E5 is the latest definitive record. E4 sets the scope: a dedicated flow is wanted for the actor question; all prior actor work including the fork is distrusted. E5 confirms Kameo. Standards of use are undeclared — no distilled statement can be written yet.

---

## Subject F: Signal contracts, edges, wire interfaces

**F1.** id: 55d18f4f (2026-08-08T11:28Z), flows/55d18f4f/vision/rustComponentArchitecture.md — typed

> "all just going to be a giant sort of cluster of components that exchange signal messages with each other. [...] the daemon doesn't really speak string. Although for now they're records that will hold string fields, but it doesn't think in strings at all. And eventually even all of the string part of language will be replaced by a completely specified, fully typed binary system of enums and structs and scalar values."

**F2.** id: 012fbf07 (2026-08-11T12:04+02:00), flows/012fbf07/vision/threeStacks.md — typed

> "the signal ID must be how agents interpreted my vision for an ability for the router to differentiate between signal types for sorting them out. router is for signals to go across the network. it should be an enum in a universal signal repo that all components depend on, which wrap the objects. that universal-signal repo could also serve other functions that all signals need to deal with (handshake payload basically)"

**F3.** id: 01a02fd5 (2026-08-24T00:32:11+02:00), flows/01a02fd5/vision/interfaces.md — typed

> "the interfaces should be written in schema (or ethos if ethos-monolith can already emit working rust)"

**F4.** id: 01a02fd5 (2026-08-24T00:32:28+02:00), flows/01a02fd5/vision/interfaces.md — typed

> "this means the interfaces for meta-signal and signal orchestrate repos should be schema or ethos"

**F5.** id: 01a02fd5 (2026-08-24T00:36:16+02:00), flows/01a02fd5/vision/interfaces.md — typed (supersedes F3 and F4)

> "we'll just say ethos, which will motivate everyone to get ethos working."

**F6.** id: 01a02fd5 (2026-08-24T00:36:44+02:00), flows/01a02fd5/vision/interfaces.md — typed

> "use the line you proposed without schema"

**F7.** id: 01a03d6e (2026-08-26T14:22:01.126Z), flows/01a03d6e/vision/ethosInterfaces.md — typed

> "the interface has to be designed in a verb-oriented, an imperative approach"

> "When we're designing a signal interface, the input maybe should be even called commands or requests, because they could be refused. So to say request, first of all, is redundant, because this is a request by virtue of being in that slot. And it should be an imperative voice, right, as in list."

**F8.** id: 01a03d6e (2026-08-26T14:22:01.126Z), flows/01a03d6e/vision/ethosInterfaces.md — typed

> "observe is more universal, and reuse is good, because there's going to be multiple nexuses, and if they sort of standardize around a set of commands that are more universal, then the models might even be able to instinctively use a tool or a nexus that they weren't even explicitly trained for, just because of the reuse of these primaries, these primordial principles."

> "the better design would be observe with a, observe is the root variant, and then it has, it contains another, maybe a list, or sorry, another enum, right, which is represented as a list in that particular spot in the ethos syntax of the subcommand for that observe."

**F9.** id: 01a03d6e (2026-08-26T15:04:27.982Z), flows/01a03d6e/vision/ethosInterfaces.md — typed

> "that is obsolete nota/dotos format"

---

## Subject G: Universal Nexus traits and ontology

**G1.** id: e06e4c07 (2026-08-19T13:49+02:00), flows/e06e4c07/vision/nexus.md — dictated

> "It uses a software ontology using traits, which hasn't been done properly yet, and I'm in a discussion in another flow about this, about the fact that when we introduced the mandatory traits, that the first implementation just simply created placeholder traits for every function, and just sort of mindlessly created traits that don't create a sensible ontology. And there's going to have to be a lot to be done in terms of creating training for this to be understood better by agents, and also creating a workflow for this, for any ontology to be designed properly before it's implemented. And this relates to why I want ESOS, the language, to allow us to more coherently and clearly design the main traits and types of a system, of a nexus, of any system."

**G2.** id: e06e4c07 (2026-08-19T14:51+02:00), flows/e06e4c07/vision/nexus.md — typed

> "potentially. let's keep that as an possibility under discussion. We need to first design universal nexus traits, which would be the basic ontology of an actor/dataflow software system. lets look at signal and sema with that, without giving much credit to the existing code, approaching it as if we were designing it for the first time (the current code being compared to it, which will show the gaps as we design further)"

**G3.** id: f426777b (2026-08-26), flows/f426777b/vision/nexusTraits.md — dictated

> "I don't know if try from is the right way to think about something that we are processing. [...] what we're doing when we're processing something or when we're... when an object is going into the nexus for an effect to take place, what... conceptually, we're not really trying to get the response. We will get a response as an effect of that, but it's kind of like you wouldn't punch somebody to try and break your own knuckles."

**G4.** id: f426777b (2026-08-26), flows/f426777b/vision/nexusTraits.md — dictated/typed

> "And I don't like the syntax, by the way, that you've been developing for Nexus, which—okay, so let's look at, for example, 'PathLockRegistered.try_from.registration'. It's too difficult to make out what this is, and also it's too many heads in a row. It's very unrefined. This is a very unrefined syntax."

> "I don't think we can just define traits implicitly, meaning if we only declare traits in our own version of implementations, of how we implement them, then it'll be difficult. It's going to be complex to try to extract what that trait actually is and how many interactions it has."

**G5.** id: f426777b (2026-08-26), flows/f426777b/vision/nexusTraits.md — typed

> "I like apply but I'm not certain and the trait suggested for the returned generic made me think of something; we need a new terminology."

---

## Subject H: Repository anatomy (three repos per component)

**H1.** id: 012fbf07 (2026-08-11T00:39+02:00), flows/012fbf07/vision/threeStacks.md — typed

> "I dont know if we need a core-* repo. I dont see much point. so ethos can have all the code, minus the two signal repos, and so on (3 repos per component). other than reusable libraries of course, which we want to encourage for shared traits especially."

**H2.** id: 012fbf07 (2026-08-11T12:04+02:00), flows/012fbf07/vision/threeStacks.md — typed

> "1 yes. 2 psyche is the fixture. we re-use much of spirit, and introduce a top-level enum; Spirit, Intent, Vision, which differentiates which layer records belong to. 3 yes"

(H2's point 3 confirms: the two signal repos per component are the ordinary-socket and metasocket ones.)

---

## Subject I: Flow Nexus — the daemon for model flows

**I1.** id: 358f143a (2026-08-18T15:23+02:00), flows/358f143a/vision/flowDaemon.md — typed

> "On another note: the new daemon I want to make isnt training anymore (abandonned). Its flow, which will setup and start a model flow, with its own working directory, system prompt and training files, and its instruction prompt."

**I2.** id: e06e4c07 (2026-08-19T13:49+02:00), flows/e06e4c07/vision/flowDaemon.md — dictated

> "So for example, the curriculum repository. Now essentially, not all of its content will go into the flow nexus, but because the skill contents themselves will have to live somewhere else because the flow nexus, the repository will be about the machinery of the flow nexus. And the actual skills that people want to use with their system will have to live in a different repository. Of course, there will probably be a few basic skills. No, there will be a few basic skills that are actually included in the flow repo [...] which are essentially the analogs of what the basic harness training prompt is currently that is built into the harnesses, which we will completely replace [...] Just basic stuff on how agents should behave in a harness, but with our own take on it."

---

## Possible vision impurities — flagged only, not acted on

The following records appear to be working instructions logged as vision; they do not state design truths about the system:

1. **flows/01a03d6e/vision/orchestrateDeployment.md** — "Remember everything to do with the recent work on orchestrate, and give me a situation summary with Ascii visuals. I want to plan then execute it's deployment with appropriate skill changes" (2026-08-26T09:37:19.681Z). This is a session opener / task direction, not a design statement.

2. **flows/01a03952/vision/orchestrateInPath.md** — "in the future, propose docs/skill that assume this orchestrate is in PATH." A process directive to future agents, not a design truth.

3. **flows/01a03eda/vision/orchestrateRealization.md** — "looks good. implement and deploy" (2026-08-26T16:55:46.618Z). An approval utterance, not a design statement.

4. **flows/98fbfa47/vision/rustComponentArchitecture.md** — the records "find the parts that are skill" and "this is no high level explanation" (2026-08-09T17:00+, 18:23+) are skill-composition instructions, not design rulings.

---

## Nexus skill claims tracing to psyche records

All of the following nexus skill claims trace to a psyche record found above:

- "A Nexus is the long-running whole with at least two sockets, a default CLI client per socket, and the signal contracts it is compiled with." → A4, A2, A3
- "Every Nexus opens at least two sockets: the ordinary socket, for any authenticated peer, and the meta socket, privileged." → A2, B3, B4
- "A Nexus is a vertex in the graph of nexuses. An edge joins two vertices and carries one contract: every connected pair has an ordinary edge; only some pairs have a meta edge." → A5, A6
- "A Nexus starts with no arguments. Its executable owns default configuration." → B5
- "The same Configure type accepts changed values over the meta socket." → B5, B6
- "Write every wire interface in Ethos." → F5, F6
- "Operations are verbs in verb form." → F7
- "The traits and types of a Nexus are designed as one ontology — the most unified map of traits and types — before any body is written." → G1, G2, A4
- "call it a Nexus, never a daemon" → A7

The following nexus skill claims have **no direct psyche record found**:

- "One capability, one Nexus. A Nexus is sized to be held whole in one mind — human or model; when it outgrows that, it splits." — No psyche record found.
- "Observation flows up, authority flows down: state is observed through push subscriptions — a typed snapshot on open, typed deltas after" — No psyche record found.
- "When one intent spans several nexuses, the issuer commits on the first success and records divergence on failure — no distributed rollback, no all-or-nothing stall." — No psyche record found.
- "Polling is forbidden; a correct system goes quiet when nothing changes." — No psyche record found.
- "The decision-making engine inside it is Nexus Kernel." — Psyche said "NexusCore" (A3). The rename to "Nexus Kernel" has no witnessed psyche approval.

The nexus-rationale skill's claims all trace to psyche records: the coarse-grain rationale → A2 (e06e4c07 dictated); the "man and his heart" framing → A2; the meta socket as root user → B3; clients speak pure signal to preserve simplicity → A2.

---

## What Vision/ already covers

- **Vision/ethosMonolith.md** (distilled, reviewed) covers: ethos-monolith as the short-term production path; the three-nexus stack as the desired long-term destination; the monolith being itself a Nexus; vocabulary kept (Signal, Nexus, SEMA); Nexus as "our specifically designed daemon"; the psyche component as first fixture; readiness witnessing.

## Subjects with no distilled Vision/ statement yet

- A: What a Nexus is (full definition — vertex, edges, contracts, sockets, CLIs)
- B: Privileged vs ordinary sockets; meta socket invariant; configuration via meta socket
- C: "Everything will be a Nexus" as a standalone universal rule (partially implied in Vision/ethosMonolith.md but not self-standing)
- F: Signal contracts and wire interface design (ethos, verb-form operations, observe root variant)
- G: Universal Nexus traits / ontology design discipline
- H: Three repos per component (no Vision/ statement; covered in psyche-raw)
- E: Actor library (standards undesigned; dedicated flow requested — not yet ready for distillation)
- I: Flow Nexus (covered in psyche-raw/Vision/flowDaemon.md title only)

---

## Sources

- `Vision/ethosMonolith.md` — distilled statement (already reviewed by living)
- `psyche-raw/Vision/nexus.md` — title only; records held in flows/e06e4c07/vision/nexus.md and flows/fd301d9a/vision/nexusTraits.md
- `psyche-raw/Vision/actorLibrary.md` — sourced from flows/15b67974 and psyche-raw/Vision/rustComponentArchitecture.md
- `psyche-raw/Vision/rustComponentArchitecture.md` — session ba906ae2 (2026-08-14), dictated
- `psyche-raw/Vision/everythingIsInTheDaemon.md` — header only; content in flows/55d18f4f
- `psyche-raw/Vision/flowDaemon.md` — header only; content in flows/358f143a and flows/e06e4c07
- `flows/01a02fd5/vision/interfaces.md` — 2026-08-24
- `flows/01a02fd5/vision/nexuses.md` — 2026-08-23
- `flows/01a02fd5/vision/metaOrchestrate.md` — 2026-08-23
- `flows/01a03d6e/vision/ethosInterfaces.md` — 2026-08-26
- `flows/01a03d6e/vision/orchestrateDeployment.md` — 2026-08-26
- `flows/01a03d6e/vision/nexus.md` — 2026-08-26
- `flows/01a03d6e/vision/orchestrateSkill.md` — 2026-08-26
- `flows/01a03eda/vision/orchestrateRealization.md` — 2026-08-26
- `flows/01a03952/vision/orchestrateInPath.md` — 2026-08-25
- `flows/e06e4c07/vision/nexus.md` — 2026-08-19
- `flows/e06e4c07/vision/flowDaemon.md` — 2026-08-19
- `flows/aa4c7747/vision/orchestrate.md` — 2026-08-25
- `flows/aa4c7747/vision/ethosMonolith.md` — 2026-08-24
- `flows/b675f3d9/vision/ethosMonolith.md` — 2026-08-26
- `flows/15b67974/vision/actorLibrary.md` — 2026-08-21/22
- `flows/55d18f4f/vision/rustComponentArchitecture.md` — 2026-08-08
- `flows/55d18f4f/vision/everythingIsInTheDaemon.md` — 2026-08-08 (header only)
- `flows/012fbf07/vision/threeStacks.md` — 2026-08-11
- `flows/019feb93/vision/threeStacks.md` — 2026-08-10
- `flows/98fbfa47/vision/metaCliIsComponentDashMeta.md` — 2026-08-09
- `flows/98fbfa47/vision/metaSignalNotOptional.md` — 2026-08-09
- `flows/98fbfa47/vision/rustComponentArchitecture.md` — 2026-08-09
- `flows/f426777b/vision/nexusTraits.md` — 2026-08-26
- `flows/fd301d9a/vision/nexusTraits.md` — 2026-08-19/22
- `flows/358f143a/vision/flowDaemon.md` — 2026-08-18
- `.claude/skills/nexus/SKILL.md` — generated skill (read for claim tracing)
- `.claude/skills/nexus-rationale/SKILL.md` — generated skill (read for claim tracing)
