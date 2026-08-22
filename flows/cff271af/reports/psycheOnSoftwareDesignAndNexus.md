# What the Written Psyche Holds: Software Design, Nexus, Signal, Datom, Sema

Acquisition report assembled 2026-08-22 by flow cff271af.
All quoted text is the psyche's verbatim words unless marked otherwise.

## I. Software Design Philosophy

### A. Traits-First / Mandatory Traits

**Intent-level (approved wording, 2026-08-13, Steward session d2bb5f5f):**

> Every method call in our Rust code lives under a trait, because traits are the comprehension surface — the layer where concepts become visible and implementations are constrained to think within them. Rust is the new assembly language: no serious engineer reads all the assembly, and the same is happening to Rust. Traits and main types are what the psyche reads; everything else is implementation detail that Ethos will eventually generate.

Source: `psyche-raw/Intent/mandatoryTraits.md`

**The broad statement (2026-08-11, session a5587095):**

> I even want to make the broad statement that I want *all* method calls in our rust code to be part of a trait, since I need to understand my systems through traits and main types, as I cannot possibly read all the code, and rust is the new assembly language; no serious engineer reads all the assembly code anymore, and the same is going to happen to rust, hence why we need a more concise, dense and congnitively concentrated language like ethos to write code with AI agents.

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-11)

**Traits constrain the implementers to think in concepts (2026-08-11, session a5587095):**

> I meant traits constrain the implementers to think in a certain way, by forcing the implementation to fit within certain concepts. does that make sense? Do a trait-first development research, finding people who argue everything should go through traits (they do conceptually, if not explicitely; function names often betray the trait they would otherwise use in their name)

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-11)

**Greenfield is trait-first natively (2026-08-12, session a5587095):**

> well, on a greenfield we wouldnt extract; a new need would require a new trait (or extending an existing one if that looks more appropriate. Extraction would be for porting existing code to mandatory-trait standard

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-12)

### B. Types / Ontology

**Types first; traits are what types implement (2026-08-13, session 6863ef19):**

> we need to think very carefully of what the types are. First, really, because the traits are something that the types implement. We don't look for traits and then think of types for that. So, what are all the types? Let's look at the types first.

Source: `psyche-raw/Vision/traitsAsCapabilities.md` (2026-08-13)

**Trait/types design is ontology in code (2026-08-18, session 2b34fafa):**

> Using mechanical tests isnt going to create good ontology; trait/types design is ontology in code.

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-18)

**The ontology must be designed before implementation (2026-08-19, session e06e4c07):**

> It uses a software ontology using traits, which hasn't been done properly yet [...] when we introduced the mandatory traits, that the first implementation just simply created placeholder traits for every function, and just sort of mindlessly created traits that don't create a sensible ontology. And there's going to have to be a lot to be done in terms of creating training for this to be understood better by agents, and also creating a workflow for this, for any ontology to be designed properly before it's implemented.

Source: `psyche-raw/Vision/nexus.md` (2026-08-19) / `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-19)

**The map approved — the map is the Ethos interface file (2026-08-20/21, session 2b34fafa):**

> I think training the model to catch themselves before creating a fake trait means we have already failed; the model is trying to write code before it has a *model of the world*. could we say this is about building ontology, anatomy .. a *map* of what we are creating as an object/capability-oriented layout?

And:

> yes, except that it isnt ready to use yet, so the model writes the ethos but has no way to run it (yet).

Source: `psyche-raw/Vision/worldModelBeforeCode.md` (2026-08-20, 2026-08-21)

**Functions pretending to be traits — a cornerstone of models not understanding the vision (2026-08-20, session 2b34fafa):**

> You misunderstood the trait based approach. your trait methods are just regular functions pretending to be traits. if the type needs a 'name' to resove the import, then it's not resolvable. So we found one of the cornerstone of models not understand my vision. Do a research in this

Source: `psyche-raw/Vision/traitsAsCapabilities.md` (2026-08-20)

**The traits and types map, approved (2026-08-19, session e06e4c07):**

The proposed lines ("The traits and types of a Nexus are designed as one ontology — the most unified map of traits and types — before any body is written; a new need first finds its place in that map. One type implementing many single-function traits is one trait not yet seen."):

> this is good. deploy it

Source: `psyche-raw/Vision/nexus.md` (2026-08-19)

### C. No Free Functions

**All traits are qualifiers (2026-08-13, session 6863ef19):**

> all traits will be qualifiers. I disagree with rust's convention (Write Read should be Writable and Readable).

Source: `psyche-raw/Vision/traitsAsCapabilities.md` (2026-08-13)

Note: superseded by 2026-08-14 verb acceptance:

> Yes, I accept verbs. now I can see why rust went with verbs; it is easy to understand that a thing that which implements Run is CapableOfRunning.

Source: `psyche-raw/Vision/traitsAsCapabilities.md` (2026-08-14)

**Infinitive verb form for action traits — ruling (2026-08-21, session 2b34fafa):**

> So we would use the sort of infinitive form of the word, of the verb, I mean. If it's an action that can be purely described as an action, like write, read, resolve, create. So that's how we would call this trait, I think, for the new is create.

Source: `psyche-raw/Vision/traitsAsCapabilities.md` (2026-08-21)

**CLIs cannot accept any argument other than the typed input object (2026-08-14):**

> An agent broke the invariant. Get rid of the flag and expose the option through nota/dotos. Remove any and all flags from lojix, replace them all. CLIs cannot accept any other type of argument than the typed input object. I feel like I keep repeating myself.

Source: `psyche-raw/Vision/setupIndependentInterfaces.md` (2026-08-14)

### D. The Best Shape

> If we see from a high level here, if we express things properly, we will minimize the amount of code. The minimum amount of code for the most elegant machinery, which can be easily understood by an engineer and easily extended and easily introspected, is the best shape.

Source: `psyche-raw/Vision/theBestShape.md` (2026-08-13) — flagged by the psyche as possibly Intent.

### E. Machine Anatomy and Main Function

**Main is a few clear lines; the program is a spec (2026-08-21, session 2b34fafa):**

> We want to start from the top or the bottom, however you want to see it, the main function. And in the main function, it has to be very clear. It's only a few lines, right? [...] most programmers, most programs I guess you could say, create the schema in the code instead of creating the schema and then just tying it up with a few lines.

Source: `psyche-raw/Vision/mainFunction.md` (2026-08-21)

**From preferred over Into; everything is demand-driven (2026-08-21):**

> I think the From is better than Into, since in reality, we need to create things *from* other things; nobody harvests a material and then asks what this can be made into; everything is demand-driven.

Source: `psyche-raw/Vision/mainFunction.md` (2026-08-21) / `psyche-raw/Vision/worldModelBeforeCode.md` (2026-08-21)

**The 3-part machine, fractal (2026-08-21, session 2b34fafa):**

> agglomerate multiple types -> create a coherent type -> convert it to another type

> since in an executable the output, by the nature of the OS, forces us to create a "pre-output" output-type, the general nature can be better viewed as a 3-part machine; input (diverse, multiple sources) -> coherent type -> output (which is itself coherent inside the program). Then this principle can be extended to be used in every part of our software design.

Source: `psyche-raw/Vision/machineAnatomy.md` (2026-08-21)

**The machine is not one form (2026-08-21):**

> thats just one form of it. the machine might be accumulating variables in a method's body. Im not investing into a single form like this.

Source: `psyche-raw/Vision/machineAnatomy.md` (2026-08-21)

**Main's input is a strictly typed datom object (2026-08-22, session bc05da32):**

> in your main block, you forgot the input, which is a strictly typed object coming in as datom.

Source: `psyche-raw/Vision/mainFunction.md` (2026-08-22)

### F. Code Is Language

> the vocabulary drives the code design, and the implemented code must drive the vocabulary. code is language. I want agents instructed to stick to this assiduously

Source: `psyche-raw/Vision/codeIsLanguage.md` (2026-08-13)

## II. The Software-Design Skill

**Ordered (2026-08-21, session 2b34fafa):**

> we still need to establish the protocol for create the anatomy of a well designed object and capabilities oriented machine.
>
> I want to go really deep into all this, and put together a skill for software design

Source: `psyche-raw/Vision/worldModelBeforeCode.md` (2026-08-21)

**The skill is about the daemon, the signal wire format, the CLIs, traits first (2026-08-09, session 98fbfa47):**

> its 8 thousand lines. If it was a thousand lines, I would still think its big. this is insane. this is no high level explanation. its full of hyper specific stuff. it should be about the daemon, the signal wire format, the cli's, the wire type repos, the traits first, etc

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-09)

**Nexus and software-design will probably merge (2026-08-22, session 15b67974):**

> dont worry about the skill overlap for now. we'll probably end up merging them.

Source: `psyche-raw/Vision/skillDesigning.md` (2026-08-22)

**A skill is not a history book (2026-08-22, session bc05da32):**

> The content there can be good, but this is a skill not a history book

Source: `psyche-raw/Vision/skillDesigning.md` (2026-08-22)

**A toy is not a good example (2026-08-22, session bc05da32):**

> a toy is not a good example

Source: `psyche-raw/Vision/skillDesigning.md` (2026-08-22)

**Old code is at most inspiration (2026-08-22, session 15b67974):**

> old code is at most inspiration for that map. (no "never ...")

Source: `psyche-raw/Vision/worldModelBeforeCode.md` (2026-08-22)

## III. The Nexus Skill and Nexus Architecture

### A. Naming: Everything Built Is a Nexus

**The Nexus is the whole component (2026-08-19, session e06e4c07, dictated):**

> So instead of calling them the rest components or the daemon CLI signal components and all of that stuff, we're just going to say another Nexus. [...] the way I am creating this system, this metasystem that is emerging now, is that there are all these different Nexus, each of which can function on their own, but which really gain a lot of value by working with each other, by exchanging information and communicating with each other. [...] But everything we're going to build is going to be a nexus now, and anything that has already been built that did not take the shape of The nexus is going to be rewritten.

Source: `psyche-raw/Vision/nexus.md` (2026-08-19)

### B. Nexus Core

> We could rename the current Nexus (the "actor/interface/abstraction" for execution) as NexusCore; the heart of this nexus; where all the decision-making happens.

Source: `psyche-raw/Vision/nexus.md` (2026-08-19)

### C. Two Sockets (at Least), Two CLIs, Pure Signal

> each Nexus needs to have two sockets, right? Because one of these sockets, the meta-socket, is going to be privileged.

Amended:

> we should say *at least* two sockets. some nexus might need more than 2 levels of access.

> then this would become a default cli client per socket. the cli is for bootstrap and later on can be used for debugging and testing even after it isnt used in production anymore

Source: `psyche-raw/Vision/nexus.md` (2026-08-19)

### D. Metasignal Not Optional

> the metasignal is not optional because otherwise there's no way to configure the daemon.

Source: `psyche-raw/Vision/metaSignalNotOptional.md` (2026-08-09)

### E. Vertices and Edges

> A Nexus is a vertex in the graph of nexuses. An edge joins two vertices and carries one contract: every connected pair has an ordinary edge; only some pairs have a meta edge. A Nexus is compiled with the contracts of its own sockets and of every edge it has.

Approved:

> the nexus line is good.

Source: `psyche-raw/Vision/nexus.md` (2026-08-19)

### F. Three Repos per Component

> ethos can have all the code, minus the two signal repos, and so on (3 repos per component). other than reusable libraries of course, which we want to encourage for shared traits especially.

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-11)

### G. Actors in the Nexus

> re actors: we are definitely using kameo actors in nexus. I just havent designed the standards of use

> I want to dedicate a flow to the actor question. Everything was done by previous flows that received little to no guidance on design in this respect. Distrust it all, including our fork.

Source: `psyche-raw/Vision/actorLibrary.md` (2026-08-22)

### H. Nexus Skill Renamed

> Yes, I want the rename. I also want a nexus repo (if there is one, it probably doesnt fit the role I now have for it) which will explain the principle, and potentially even hold the nexus traits

Source: `psyche-raw/Vision/nexus.md` (2026-08-19) — the rust-component-architecture skill becomes nexus.

### I. A Rationale Skill for Psyche-Facing Flows

> That we could have a parallel skill. What is the right word to speak of this kind of information? Its "raison d'etre"? That could become a parallel skill design skill. It would only be of use to psyche-facing flows, to allow them to think of the whole, with all the reasoning and concepts, when discussing ideas with the living psyche.

> Re rationale and skill-design line: yes, its good.

Source: `psyche-raw/Vision/nexus.md` (2026-08-19) / `psyche-raw/Vision/skillDesigning.md` (2026-08-19)

### J. Architecture Guard: Stupid

> thats so stupid. I want to get rid of that, and train against this level of expert foolishness.

> what you said is true, but its stupid because it writes a tool for this single repo, instead of a universal tool being created to test this for any repo

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-18)

## IV. Datom

### A. Origin and Name

> what about datom

> ok we'll use datom [...]

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-10) — the psyche's own coinage.

> its data, strictly typed, super dense (no field names). something that echoes this

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-10)

### B. Datom Carries Data Only; No Generics

> datom doesnt do generics, it only carries data, like json (but strictly typed of course)

Source: `psyche-raw/Vision/datomSyntax.md` (2026-08-11)

### C. Datom Does Not Generate Rust

> datom doesnt generate rust. ethos does. so I dont know what youre trying to say there, but its a dangerous line, and should be rooted out, wherever you got tha idea

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-11)

### D. Datom and Ethos Are Different Languages, Shared Substrate

> no, I dont think so. they share an approach, but are different languages. they could have a shared substrate (traits with a shared implementation and types)

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-11)

### E. Ethos Depends on Datom

> Meaning will be seen in datom and ethos. ethos will depend on datom if only because of the need to intake data for signals, so it can go in datom

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-11)

### F. The Two Main Syntaxes

> the two main syntaxes most agents will face; one specifies the types, the other fills them with data — hence why the basic 'cli help' for their dotos objects is meant to emit the ethos syntax that describes their anatomy.

Source: `psyche-raw/Vision/ethosDotosDivisionAndHelp.md` (2026-08-02)

### G. De/serializer: Positional, Direct to Typed Structs

> 1 yes, direct to typed structs. 3 what is reflection? no self-describing tags

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-11)

### H. The Root Enumerator (Datom as Interface)

> datom creates configuration options by its very shape, as the ethos interface shows; a data enum at the root (main operation) with options in its data

Source: `psyche-raw/Vision/interfaceRootEnumerators.md` (2026-08-22)

## V. The Ethos-Monolith Nexus

**Named and explained (2026-08-14, session ba906ae2):**

> The shortcut stack for the new syntax, I think we should just call it, so it's going to be a daemon also. So to differentiate it, we should call it maybe the ethos monolith or something like that. [...] it's not going to have the nomos and the logos component, it's just going to straight commit to Rust. So we can think of it as more of a monolith, so that we can just start using ethos to write components. It's sort of like an incremental implementation slash bootstrap process. I really want to start writing and reading ethos and datum as soon as possible.

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-14) / `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-14)

**Ethos will eventually replace everything (2026-08-22, session bc05da32):**

> youre suggesting a free function. you're not realizing that ethos will eventually replace everything, so of course B will happen. just not now.

Source: `psyche-raw/Vision/mainFunction.md` (2026-08-22)

## VI. Signal (the Wire Format)

### A. What Signal Is

> Signal is our messaging layer, and the CLI's role is to transform text into Signal. [...] it's a RKYV, portable RKYV.

Source: `psyche-raw/Vision/signalIsOurMessagingLayer.md` (2026-08-08)

### B. Signal Is Its Name

> signal. signal. signal. that is what we call it. signal. lets find a place to explain that clearly

Source: `psyche-raw/Vision/signalIsOurMessagingLayer.md` (2026-08-14) — the serialized zero-copy bytes are called signal, not "archive."

### C. Signal Is Fully Typed

> this doesnt make any sense to me. signal is fully typed; both sides know the full schema.

Source: `psyche-raw/Vision/signalIsOurMessagingLayer.md` (2026-08-14)

### D. The Three Forms

> ok, working form and signal form, drop code/encoded entirely

Amended — "working" rejected:

> I dont like working, it smells like a verb.

Settled:

> Ok with the real/Realize

The three forms: **textual** (for editors/humans/LLMs), **real** (in-memory, where values are born and changed), and **signal** (portable rkyv, the wire format). The code/encoded vocabulary was dropped 2026-08-13.

Source: `psyche-raw/Vision/encodedFormIsTheCode.md` (2026-08-13, 2026-08-14)

### E. The Ethos Generates the Type in Rust

> The ethos *generates the type in rust*

Source: `psyche-raw/Vision/signalIsOurMessagingLayer.md` (2026-08-14)

### F. Realize and Textualize Are Never on the Same Type

> realize isnt implemented by the same type as textualize. if you cant find two different types, the implementation is wrong. You dont textualize the text, and you dont realize the realized data.

Source: `psyche-raw/Vision/traitsAsCapabilities.md` (2026-08-18)

### G. Universal Signal (CapnProto) and Routable Signal

> So, the closest thing to R-K-Y-V for cross-platform is CapnProto [...] transcodable could mean also transcodable in CapnProto, which we would call, like, universal signal.

> routable signal then

Source: `psyche-raw/Vision/signalIsOurMessagingLayer.md` (2026-08-13)

Note: the "transcodable" vocabulary was dropped later the same day. The CapnProto cross-platform concept and "universal signal" terminology stand; the router-enum repo concept is "routable signal."

### H. A Nexus Speaks Only Pure Signal

> all clients will have to talk to the Nexus, regardless of which socket, in pure signal, in signal, which is fully binary, because the Nexus component cannot be involved in texturalizing signal, because it would just destroy the beauty and the simplicity of the system. So all Nexus components speak only pure signal, the contracts which they are compiled with

Source: `psyche-raw/Vision/nexus.md` (2026-08-19)

### I. Signal Contracts

Asked about "A Nexus speaks only the contracts it is compiled with":

> how about "signal contracts"?

Source: `psyche-raw/Vision/nexus.md` (2026-08-19)

### J. Every Concept Should Have Its Repo

> every concept should really have its repo, and if anything goes in there, the traits can, since every concept deserves at least one trait, and probably more.

Source: `psyche-raw/Vision/everyConceptShouldHaveItsRepo.md` (2026-08-09)

## VII. Sema (the Typed Durable Store)

**The output of the incorrect new stack — signal, nexus, sema (2026-08-10, session 019feb93):**

> just generate the rust code for types and generics/traits to define the wire types (signal), major internal engine operation types (nexus), and database types (sema). log this

Source: `psyche-raw/Vision/threeStacks.md` (2026-08-10)

**Sema is the database engine; more important than nexus (2026-08-14, session ba906ae2):**

> sema being the database engine, which I never really looked at close enough. I think that it's probably not designed to my standard at all. [...] you could say sema was way more important than nexus because the whole point of creating a real code evolution engine was that because through the operational editing, we could have database migration operations come out instantly or along with the editing operation because it would be this essentially sort of parallel, almost, you know, almost the exact same thing. And so, yeah, to expose the types that the database stores and for the agent, for both the human and the agents to easily reason about this

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-14)

**Keep the Signal/Nexus/SEMA vocabulary and principles (2026-08-14):**

> we can keep the Signal, Nexus, SEMA vocabulary and principles, but we aren't tied to how they were used and implemented in the past.

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-14)

**Sema authored in ethos — the schema explanation mechanism (2026-08-14):**

> the whole point of exposing nexus and sema as another, back then it was schema, but now ethos authored interfaces was that so that I could see what the main operations were inside nexus, right? What the main functionality was [...] And then the same thing with sema [...] to author the database basically.

Source: `psyche-raw/Vision/rustComponentArchitecture.md` (2026-08-14)

**The daemons hold language in their database (2026-08-08, session 55d18f4f):**

> all three of those are daemons. And so it's all message-based. And then all of the daemons hold that language in memory, in their database. Not in memory, in their database. So they can fetch it back. It's there. They can edit it. We're going to do operational editing, right?

Source: `psyche-raw/Vision/everythingIsInTheDaemon.md` (2026-08-08)

## VIII. Supersession and Tensions

### A. Supersessions (Later Entries Replacing Earlier Ones)

1. **"The encoded form is the code"** (2026-08-06) — the entire code/encoded vocabulary was **dropped** 2026-08-13: "ok, working form and signal form, drop code/encoded entirely." The three forms are now textual, real, and signal. Source: `encodedFormIsTheCode.md`

2. **"Transcodable"** as a trait name — dropped 2026-08-13 with the code/encoded vocabulary: "I dont think it survives." Successor pair: protos::Realize / protos::Textualize. Source: `traitsAsCapabilities.md`

3. **"All traits are qualifiers"** (2026-08-13) — qualified by verb acceptance 2026-08-14: "Yes, I accept verbs." Further refined 2026-08-21 to the ruling: infinitive verb form for action traits (Walk, Write, Read, Resolve, Create). Source: `traitsAsCapabilities.md`

4. **The Create trait** (2026-08-21) — introduced and dissolved in the same day: "it would just be TryFrom, not create, so theres nothing to make." Source: `assembly.md`

5. **ethos-rust** (2026-08-11) — superseded by **ethos-monolith** (2026-08-14), which is itself a daemon. Source: `threeStacks.md`

6. **"datom is just a renamed dotos"** (2026-08-11) — superseded the same day: "we don't need to worry about the old repo. We're just going to move forward and migrate everything to datum [Datom]." The fresh datom repo stands. Source: `threeStacks.md`

7. **Four-part machine** (2026-08-21) — superseded same day by the **3-part machine**: "agglomerate multiple types -> create a coherent type -> convert it to another type." Source: `machineAnatomy.md`

8. **Lojix skill rejection** (2026-08-19: "We wont use a skill called lojix") — reversed 2026-08-20: "we should create a lojix skill that properly documents it, and reference it in operating-system." Source: `skillDesigning.md`

### B. Tensions

1. **Sema's design status.** The psyche says (2026-08-14): "I think that it's probably not designed to my standard at all" and calls sema "way more important than nexus," yet sema has received far less attention than nexus and signal in the written psyche. The detailed anatomy of what sema holds, its trait surface, and its ethos interface are almost entirely undesigned in the record. This is a gap, not a contradiction — the psyche has stated the importance but not yet engaged the design.

2. **Nexus skill and software-design skill overlap.** The psyche acknowledged this (2026-08-22): "dont worry about the skill overlap for now. we'll probably end up merging them." The merge has not happened; both exist.

3. **Actor standards undesigned.** The psyche confirmed kameo actors in nexus (2026-08-22) but stated: "I just havent designed the standards of use" and "Distrust it all, including our fork." A dedicated flow is wanted but does not yet exist.

4. **"Universal signal" naming collision was resolved** — CapnProto cross-platform form is "universal signal"; the router-enum repo concept is "routable signal" (2026-08-13). But the transcodable vocabulary that framed it was dropped the same day; successor naming for the cross-platform capability is open.

### C. Suspect Entries

None identified. The entries are internally consistent once supersession is tracked. The dictated entries carry transcription artifacts ("rest" for Rust, "demons" for daemons, "ESOS" for Ethos) but the psyche or agents have noted these, and no semantic ambiguity remains.

## IX. Unknowns (Not Found in the Written Psyche)

1. **Sema's trait surface and ethos interface** — the psyche has stated sema is more important than nexus and wants it authored in ethos, but no detailed sema design session appears in the record.

2. **The software-design skill's final form** — ordered (2026-08-21), under active drafting (sessions bc05da32 and 15b67974 on 2026-08-22), but not yet approved or deployed.

3. **The nexus repo** — the psyche floated a nexus repo to hold the principle and universal nexus traits (2026-08-19): "potentially. let's keep that as an possibility under discussion." Status: under discussion, not ruled.

4. **Universal nexus traits** — ordered designed from first principles (2026-08-19): "We need to first design universal nexus traits, which would be the basic ontology of an actor/dataflow software system." This design has not appeared in the record.

5. **CapnProto / universal signal successor naming** — the concept stands but its capability trait name is open after the transcodable drop.

6. **Datom's Meaning type** — postponed (2026-08-13): "we'll postpone the Meaning type in datom to get a working syntax asap." Still deferred.

## Sources

All paths are relative to `/home/li/primary/`.

| Path | Topics Covered |
|---|---|
| `psyche-raw/Intent/mandatoryTraits.md` | Mandatory traits (Intent-level approved wording) |
| `psyche-raw/Vision/nexus.md` | Nexus naming, architecture, vertices/edges, signal contracts, rationale skill |
| `psyche-raw/Vision/signalIsOurMessagingLayer.md` | Signal definition, fully typed, universal/routable signal, CapnProto |
| `psyche-raw/Vision/traitsAsCapabilities.md` | Traits as capabilities, qualifiers/verbs, types first, Realize/Textualize, functions pretending to be traits |
| `psyche-raw/Vision/genericParametersAreTraits.md` | Generic parameters as mandatory traits |
| `psyche-raw/Vision/sectionsExistToConferTraits.md` | Sections confer traits |
| `psyche-raw/Vision/datomSyntax.md` | Datom syntax rulings |
| `psyche-raw/Vision/everythingIsInTheDaemon.md` | Everything in the daemon, Ethos/Nomos/Logos as daemons, operational editing |
| `psyche-raw/Vision/rustComponentArchitecture.md` | Component architecture, traits first, skill scope, architecture guard, ontology, sema |
| `psyche-raw/Vision/metaSignalNotOptional.md` | Metasignal mandatory |
| `psyche-raw/Vision/encodedFormFingerprintTraitDesign.md` | Early trait design, fingerprinting (dead vocabulary) |
| `psyche-raw/Vision/threeStacks.md` | Three stacks, Datom naming, three repos per component, ethos-monolith, signal repos |
| `psyche-raw/Vision/flowDaemon.md` | Flow Nexus, 100% typed datom messages |
| `psyche-raw/Vision/flowsNotAgents.md` | Flows vs agents, synthetic intelligence |
| `psyche-raw/Vision/mainFunction.md` | Main function, TryFrom chains, assembled source, datom input |
| `psyche-raw/Vision/machineAnatomy.md` | 3-part machine, fractal anatomy |
| `psyche-raw/Vision/worldModelBeforeCode.md` | Map before code, software-design skill ordered, From over Into |
| `psyche-raw/Vision/assembly.md` | Registry, assembly file, Create trait (dissolved) |
| `psyche-raw/Vision/encodedFormIsTheCode.md` | Three forms (textual/real/signal), code/encoded drop |
| `psyche-raw/Vision/theBestShape.md` | Best shape criterion |
| `psyche-raw/Vision/codeIsLanguage.md` | Code is language |
| `psyche-raw/Vision/highLevelView.md` | High-level view as routine practice |
| `psyche-raw/Vision/everyConceptShouldHaveItsRepo.md` | Concept repos, concept traits |
| `psyche-raw/Vision/sourceNotCrate.md` | Source, not crate |
| `psyche-raw/Vision/ethosDotosDivisionAndHelp.md` | Two main syntaxes |
| `psyche-raw/Vision/interfaceRootEnumerators.md` | Root enumerators, datom-as-interface |
| `psyche-raw/Vision/setupIndependentInterfaces.md` | No flags on CLIs |
| `psyche-raw/Vision/newtypeWrappingAndSingleFieldStructs.md` | No single-field structs |
| `psyche-raw/Vision/actorLibrary.md` | Kameo actors, distrust prior work |
| `psyche-raw/Vision/hexis.md` | Hexis architecture distrust |
| `psyche-raw/Vision/streamAsFourthKindMvpFirst.md` | Stream as fourth kind |
| `psyche-raw/Vision/streamSection.md` | Stream section inside the object |
| `psyche-raw/Vision/skillDesigning.md` | Skill design rules, rationale skill, nexus/software-design merge |
| `psyche-raw/Vision/spirit.md` | Spirit universality, entry-file placement |
| `psyche-raw/Vision/realizer.md` | Flow is realizing; psyche is realized into code |
| `psyche-raw/Vision/itsATranslator.md` | Protos-translator naming |
| `flows/b7465e71/vision/remembering.md` | Remembering skill, flows protocol |
