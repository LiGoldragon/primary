Presentation.{ «Code craft» }

How a piece of code comes to be, how it is shaped, and what is never done. Ethos is the language the types and traits are written in. A Nexus is a long-running component that speaks binary signal.

## 1. What he wants

### The world model comes before the code

Code is written from a map of what is being made: its objects, its capabilities, how they fit. If a check ever has to catch a fake trait, the failure already happened upstream.

> I think training the model to catch themselves before creating a fake trait means we have already failed; the model is trying to write code before it has a *model of the world*. could we say this is about building ontology, anatomy .. a *map* of what we are creating as an object/capability-oriented layout?

-- 20 August 2026

Old code may inspire the map. It never decides it.

> old code is at most inspiration for that map. (no "never ...")

-- 22 August 2026

### Design starts from what is wanted

The wanted result is named first, and the design asks what it is made from. Conversions are written "from", never "into".

> I think the From is better than Into, since in reality, we need to create things *from* other things; nobody harvests a material and then asks what this can be made into; everything is demand-driven.

-- 21 August 2026

### The anatomy of a machine

Every machine has three parts, and each part is itself such a machine.

> agglomerate multiple types -> create a coherent type -> convert it to another type

-- 21 August 2026

The output comes from one coherent type, in one place, under one trait.

> we need a coherent type from which that output is a simple operation or at least an operation that can be reviewed all in one place, where all the logic is found in one place or under one trait. Easy, easily discoverable.

-- 21 August 2026

The three parts are a law, not a fixed spelling. At small scale they may be plain variables in a method.

> thats just one form of it. the machine might be accumulating variables in a method's body. Im not investing into a single form like this.

-- 21 August 2026

### The main function is a few lines

The knowledge lives in the types. Main ties them together.

> Because most programmers, most programs I guess you could say, create the schema in the code instead of creating the schema and then just tying it up with a few lines.

-- 21 August 2026

Its chain begins with the typed input arriving as datom.

> in your main block, you forgot the input, which is a strictly typed object coming in as datom.

-- 22 August 2026

### Beautiful code first, then the infrastructure

The design starts from the code he would want to read, and works back to what must exist to support it.

> Find the goal of the beautiful code that we want, and then work your way back. Try to understand the whole from the perspective of achieving a beautiful separation of logic and an elegant final result, in terms of the logic not being just a convoluted bunch of inlined lambdas.

-- 31 August 2026

### Code is language

Words and code drive each other.

> the vocabulary drives the code design, and the implemented code must drive the vocabulary. code is language. I want agents instructed to stick to this assiduously

-- 13 August 2026

A name must be true at the moment it names.

> I wouldn't call it generated Rust because if you need to still write it, it hasn't been generated yet. So it would be more like assembled Rust.

-- 21 August 2026

### Rust is generated from Ethos

He reads traits and main types. Rust becomes an assembly language that no one reads in full, and Ethos is what is written.

> rust is the new assembly language; no serious engineer reads all the assembly code anymore, and the same is going to happen to rust, hence why we need a more concise, dense and congnitively concentrated language like ethos to write code with AI agents.

-- 11 August 2026

Generated Rust is explicit before it is pretty.

> We're not concerned about making it look sweet. We're concerned about it being correct.

-- 31 August 2026

Every wire interface is written in Ethos, so that Ethos gets finished.

> we'll just say ethos, which will motivate everyone to get ethos working.

-- 24 August 2026

Ethos ends up generating everything. Interim scaffolding Ethos will later replace is not built.

> youre suggesting a free function. you're not realizing that ethos will eventually replace everything, so of course B will happen. just not now.

-- 22 August 2026

### Trait and type design is ontology

Traits are where concepts become visible. They make the implementer think within a concept.

> Using mechanical tests isnt going to create good ontology; trait/types design is ontology in code.

-- 18 August 2026

> I meant traits constrain the implementers to think in a certain way, by forcing the implementation to fit within certain concepts.

-- 11 August 2026

Trait names are qualifiers: what a thing is able to do.

> all traits will be qualifiers. I disagree with rust's convention (Write Read should be Writable and Readable).

-- 13 August 2026

Many one-method traits on one type are a sign they are really one trait.

> if one type implements a bunch of single function traits (or is that what you meant by one implementor), then all those traits are probably only one trait

-- 17 August 2026

### Every method belongs to a trait

> I even want to make the broad statement that I want *all* method calls in our rust code to be part of a trait, since I need to understand my systems through traits and main types, as I cannot possibly read all the code

-- 11 August 2026

Implementations outside a trait are forbidden. Free functions and inline lambdas are signs of bad design.

> We forbid freestanding implementations. All implementations must be of a trait.

-- 31 August 2026

> I really despise free functions, and I despise these inlined lambdas even more.

-- 31 August 2026

### Rust in layers

The top layer reads simply. The logic lives in implementation files below it.

> At the higher layer it looks kind of like baby code and all of the implementation blocks are where the logic lies. These are separate files.

-- 14 September 2026

### A component is a Nexus

Everything built is a Nexus.

> So instead of calling them the rest components or the daemon CLI signal components and all of that stuff, we're just going to say another Nexus.

-- 19 August 2026

A Nexus speaks only binary signal. Its command-line tools are short-lived ways to reach it.

> All those CLIs are short-term shims that we use to talk to the daemons. But eventually this is all just going to be a giant sort of cluster of components that exchange signal messages with each other.

-- 8 August 2026

> the Nexus component cannot be involved in texturalizing signal, because it would just destroy the beauty and the simplicity of the system.

-- 19 August 2026

A command line takes one typed input and no flags.

> CLIs cannot accept any other type of argument than the typed input object.

-- 14 August 2026

Small specialised Nexuses come first. Higher tools are later built from them.

> Once we develop these tools we're redoing Unix with nexuses that tell binary signal instead of text.

-- 28 September 2026

Data lives in data, not in code.

> Correctness means the data lives with the data not in the code, right?

-- 28 September 2026

### The actor library

The running engine of a Nexus is built from actors. Anything that must lock is an actor.

> I want the main engine to be driven by actors. And we did actually even fork the actor library that we were using.

-- 14 August 2026

> When you need something that locks, you get an actor because it has to be synchronous, so it's a process actor.

-- 13 September 2026

He never banned shared locks. The rules for using actors are still to be designed (question 2).

> there is no ban of arc mutex. the whole actor subject deserves its own discussion in another flow

-- 21 August 2026

Proposed: one actor per piece of state that changes over time, with messages typed in Ethos. Shared locks are allowed only inside a single actor.

### Repositories and their lifecycle

Every concept has its own repository, and in it at least one trait.

> every concept should really have its repo, and if anything goes in there, the traits can, since every concept deserves at least one trait, and probably more.

-- 9 August 2026

Everything is a repository. A root repository records them all, active or archived.

> Everything is a repo, so our databases are amalgamation repos. We should have a root repo that holds essentially all the data about all the repositories

-- recorded 14 September 2026

Any repository that is touched is checked against a list and brought up to date.

> When you encounter a new repository that hasn't been touched in a while, or any repository, you have a checklist to see if it still conforms with our checklist.

-- 16 September 2026

### Clojure as the prototyping language

While Ethos is unfinished, quick tools and prototypes are written in Clojure, because it reads as data. Tension with the Ethos-first map is question 1.

> Clojure is the best Lisp, right, because the thing is, Clojure is data.

-- 29 September 2026

> Eventually we'll move all of this onto a nexus but because Clojure is more accessible to you, it's more mature, and its user interface is kind of more developed because we're so early.

-- 29 September 2026

### What is never done

Backward compatibility is never weighed. What does not fit the design is rewritten.

> But everything we're going to build is going to be a nexus now, and anything that has already been built that did not take the shape of The nexus is going to be rewritten.

-- 19 August 2026

> id rather get a minimal but broken setup than try to fix a bloated machine

-- 23 August 2026

No checker is written for a single repository. Text search is not code analysis.

> grep isnt the right way to do this testing anyway; there are much better tools to analyze code than grep nowadays

-- 18 August 2026

### Beauty, correctness and the best shape

The best shape is the least code for the most elegant machinery.

> The minimum amount of code for the most elegant machinery, which can be easily understood by an engineer and easily extended and easily introspected, is the best shape.

-- 13 August 2026

Words are chosen by beauty and correctness.

> We have to decide on the language, which words are best based on beauty and correctness.

-- 13 September 2026

More correctness pays for its machinery.

> The multiple steps create a mental model of the machinery, which enforces a correctness in the code that is millions of times more beneficial than the cost of doing these multiple passes

-- recorded 4 September 2026

Simple is worth more than he had counted.

> I think I've been underestimating the value of simple, which is why now we're stuck in mud up to our necks.

-- 28 September 2026

His standing philosophy, which every agent loads, puts it this way. Beauty is the symptom of good engineering. More correctness more than pays for its machinery, and makes growth easier. The build target is the best design possible, not a good-enough one.

## 2. What exists today

Running on his machine tonight, as Rust Nexuses: orchestrate (the lock service), flow (three processes), message (two), and lojix. Older Rust daemons also run beside them: the repository ledger, listener and chroma.

Two Clojure tools are installed: the messenger and the field tool. The messenger has no Nexus of its own.

The shared tools folder holds 62 entries. Thirty-two are JavaScript scripts and seven are Python. The rest are directories and shell tools.

The record of the Nexuses says that every wire contract on main is generated from Ethos by the current generator. None of the running Nexuses speaks that newest wire yet. Implementation code is still written by hand.

There is no root repository of repositories yet, and no Nexus that classifies them.

## 3. Questions

**1. Which comes first for the next new component?** On 25 September you said:

> You could kind of emulate the kind of code that you would write in Rust and it's sort of faster to make one-off prototypes. Then you can rewrite them in Ethos and in Rust from the [Malli] and the pseudo traits that you wrote in [Clojure].

-- 25 September 2026

On 21 August, of writing the map in Ethos:

> yes, except that it isnt ready to use yet, so the model writes the ethos but has no way to run it (yet).

-- 21 August 2026

Answer 1 for a Clojure prototype first, or 2 for the Ethos map first.

**2. Do we keep our fork of the Kameo actor library?**

> re actors: we are definitely using kameo actors in nexus. I just havent designed the standards of use

-- 22 August 2026

> Everything was done by previous flows that received little to no guidance on design in this respect. Distrust it all, including our fork.

-- 22 August 2026

Answer yes to keep the fork while the actor standards are designed.

**3. Should one checker test every repository for methods outside traits?**

> what you said is true, but its stupid because it writes a tool for this single repo, instead of a universal tool being created to test this for any repo

-- 18 August 2026

> the tool is almost useless.

-- 18 August 2026

Answer yes to build it once, for all repositories.

**4. Should Ethos generate implementation code, not only types?**

> You're saying that Datomic is implemented by or generated by Ethos, but Ethos doesn't generate implementations, so I don't understand what you mean. That sounds like bluffing.

-- 8 September 2026

> I never said that Ethos Zero should not generate implementations.

-- 8 September 2026

Answer yes.
