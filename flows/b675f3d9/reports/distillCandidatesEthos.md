# Distill Candidates: ETHOS

Candidate records for distillation on the topic of Ethos the language
and its realization. Records are the psyche's verbatim words; grouped
by sub-topic, date order within each group.

Status key: NEW = not reflected in any distilled Vision file;
REFLECTED = carried by a distilled statement (named); SUPERSEDES /
SUPERSEDED-BY = one record replaces or is replaced by another.

---

## What Ethos is and why it exists

RECORD: no-id/1 | ~2026-08-01 | recovered
VERBATIM: "youre right; and the answer is the mandatory trait! so T would be a trait! and multiple trait in the declaration would just adjust the emitted rust - remember for us rust is assembly"
SOURCE: psyche-raw/Vision/genericParametersAreTraits.md
STATUS: REFLECTED (Vision/ethos.md "Why Ethos"). The generics-are-traits detail is NEW.

RECORD: no-id/2 | ~2026-08-02 | recovered
VERBATIM: "the two main syntaxes most agents will face; one specifies the types, the other fills them with data -- hence why the basic 'cli help' for their dotos objects is meant to emit the ethos syntax that describes their anatomy."
SOURCE: psyche-raw/Vision/archive-ethosDotosDivisionAndHelp.md
STATUS: REFLECTED (Vision/ethos.md "What Ethos is" + "Self-description"). "Dotos" SUPERSEDED-BY "Datom" (2026-08-11).

RECORD: a5587095/1 | 2026-08-11 | typed
VERBATIM: "I even want to make the broad statement that I want *all* method calls in our rust code to be part of a trait, since I need to understand my systems through traits and main types, as I cannot possibly read all the code, and rust is the new assembly language; no serious engineer reads all the assembly code anymore, and the same is going to happen to rust, hence why we need a more concise, dense and congnitively concentrated language like ethos to write code with AI agents."
SOURCE: flows/a5587095/vision/rustComponentArchitecture.md
STATUS: REFLECTED (Vision/ethos.md "Why Ethos")

RECORD: d2bb5f5f/1 | 2026-08-13 | psyche-approved wording
VERBATIM: "Every method call in our Rust code lives under a trait, because traits are the comprehension surface -- the layer where concepts become visible and implementations are constrained to think within them. Rust is the new assembly language: no serious engineer reads all the assembly, and the same is happening to Rust. Traits and main types are what the psyche reads; everything else is implementation detail that Ethos will eventually generate."
SOURCE: psyche-raw/Intent/mandatoryTraits.md
STATUS: NEW as INTENT. Not in Vision files (Intent level).

RECORD: ba906ae2/1 | 2026-08-14 | dictated (excerpt)
VERBATIM: "Rust is the new assembly, read in full by no one; Ethos is the concise, dense, cognitively concentrated language for writing code with AI agents ... I wanted something that's easy to read and write that lets me see the interfaces ... the main types and the main traits ... I realized how important they are in design and how I would now want everything, every behavior to fall under a trait, which essentially creates an ontology in code."
SOURCE: psyche-raw/Vision/rustComponentArchitecture.md (session ba906ae2)
STATUS: REFLECTED (Vision/ethos.md "Why Ethos")

RECORD: bc05da32/1 | 2026-08-22 | typed
VERBATIM: "youre suggesting a free function. you're not realizing that ethos will eventually replace everything, so of course B will happen. just not now."
SOURCE: flows/bc05da32/vision/mainFunction.md
STATUS: REFLECTED (Vision/ethos.md "Horizon")

RECORD: aa4c7747/1 | 2026-08-24 | dictated
VERBATIM: "ethos is essentially meant to give us, for now anyway, the entry or the biggest gain short-term is to give us a language that allows us to, in one swoop, write down our mental model of the machine and write code so that we don't get this problem where the code and the ideas for the code, well, we have psyche for that, but psyche is sort of one step back from the actual hard implementation. It's just that something like Rust or even JavaScript is full of noise. It's like maybe more than half of the code is noise, whereas we want a language that allows us to separate the mental model we have and still write it in code."
SOURCE: flows/aa4c7747/vision/ethos.md
STATUS: NEW -- "mental model and code in one swoop", "more than half of the code is noise"

RECORD: f426777b/1 | 2026-08-26 | psyche's own transcription (excerpt)
VERBATIM: "We need a different vocabulary because we're moving one abstraction up from Rust. ... I don't like the word 'trait,' if only because it's a bit acoustically ambiguous ... So I want you to do some research in, like, ontology, category theory, how we model the universe, and how we would model this -- Ethos specifically -- which is our response to all other programming languages ... a higher level of abstraction than, I would say, any other programming language that I know out there"
SOURCE: flows/f426777b/vision/spokenVocabulary.md
STATUS: NEW -- "one abstraction up from Rust", "our response to all other programming languages"

RECORD: ac1e9ec8/1 | 2026-08-26 | typed
VERBATIM: "you've mixed up datom with ethos. datom is data"
SOURCE: flows/ac1e9ec8/vision/datomIsData.md
STATUS: NEW -- Ethos/Datom boundary enforcement

---

## Non-repetition law

RECORD: no-id/3 | ~2026-08-01 | recovered
VERBATIM: "we wouldnt repeat Ord; any such repition in ethos syntax is an implementation failure. ethos will be the most terse non-repetitive syntax ever made"
SOURCE: psyche-raw/Vision/archive-ethosNonRepetitionLaw.md
STATUS: REFLECTED (Vision/ethos.md "Non-repetition")

---

## Document kinds and placement

RECORD: 55d18f4f/1 | 2026-08-08 | dictated (excerpt)
VERBATIM: "Everything is in the daemon. ... You have the Ethos daemon, the Nomos daemon. I mean, they're just called Ethos, Nomos, and Logos. Those are the name of the repositories. They're all daemons. The same architecture as all my other components, right? There's the daemon, there's a CLI, there's a CLI for the metasocket. Everything is signal messages, meaning RKYV binary messages. ... So the whole engine working is the Ethos daemon loads the Ethos and then holds the whole thing."
SOURCE: flows/55d18f4f/vision/everythingIsInTheDaemon.md
STATUS: NEW -- full trinity vision; Ethos/Nomos/Logos as daemons

RECORD: 019feb93/1 | 2026-08-10 | typed
VERBATIM: "just generate the rust code for types and generics/traits to define the wire types (signal), major internal engine operation types (nexus), and database types (sema). log this"
SOURCE: flows/019feb93/vision/threeStacks.md
STATUS: NEW -- generation output: signal, nexus, sema

RECORD: 012fbf07/1 | 2026-08-11 | typed
VERBATIM: "I dont know if we need a core-* repo. I dont see much point. so ethos can have all the code, minus the two signal repos, and so on (3 repos per component). other than reusable libraries of course, which we want to encourage for shared traits especially."
SOURCE: flows/012fbf07/vision/threeStacks.md
STATUS: REFLECTED (Vision/ethosMonolith.md implicitly)

RECORD: 2b34fafa/1 | 2026-08-20 | typed
VERBATIM: "for the monolith thats good enough. easy cognition is the first safe bet."
SOURCE: flows/2b34fafa/vision/ethosSourceFiles.md
STATUS: NEW -- one file = one Rust module for MVP

RECORD: 2b34fafa/2 | 2026-08-20 | typed
VERBATIM: "document sucks. I dont understand your question. What's wrong with File?"
SOURCE: flows/2b34fafa/vision/ethosSourceFiles.md
STATUS: NEW -- File is the unit, not Document

RECORD: 2b34fafa/3 | 2026-08-20 | typed
VERBATIM: "so lets look at all the major types to represent the textual code. source will be the name we use instead of crate"
SOURCE: flows/2b34fafa/vision/sourceNotCrate.md
STATUS: NEW -- Source replaces Crate

RECORD: f426777b/2 | 2026-08-25 | typed
VERBATIM: "I can see a problem already: ... sema and nexus in the signal repos."
SOURCE: flows/f426777b/vision/ethosSourceFiles.md
STATUS: NEW -- triplet-per-repo mistake flagged

RECORD: f426777b/3 | 2026-08-25 | typed
VERBATIM: "lets make it clear first; the nexus and sema ethos arent designed yet, but when they are they will live in the nexus' main repo"
SOURCE: flows/f426777b/vision/ethosSourceFiles.md
STATUS: NEW

RECORD: 01a02fd5/1 | 2026-08-24 | typed
VERBATIM: "we'll just say ethos, which will motivate everyone to get ethos working."
SOURCE: flows/01a02fd5/vision/interfaces.md
STATUS: NEW -- every wire interface in Ethos. SUPERSEDES same-session "schema or ethos if ethos-monolith can already emit working rust".

---

## Sections and what they confer

RECORD: 5abf3be8/1 | 2026-08-06 | typed (backfill)
VERBATIM: "What other point is there to have different sections?"
SOURCE: flows/5abf3be8/vision/sectionsExistToConferTraits.md
STATUS: NEW -- sections exist to confer traits (Input/Output/Refusal)

RECORD: d63804f2/1 | 2026-08-07 | typed
VERBATIM: "a section inside the object" / "Yes, the initiation and termination live in the input."
SOURCE: psyche-raw/Vision/streamSection.md
STATUS: NEW -- stream is a section; initiation/termination in Input

RECORD: 01a03d6e/1 | 2026-08-26 | typed
VERBATIM: "the interface has to be designed in a verb-oriented, an imperative approach" / "When we're designing a signal interface, the input maybe should be even called commands or requests, because they could be refused. So to say request, first of all, is redundant, because this is a request by virtue of being in that slot. And it should be an imperative voice, right, as in list."
SOURCE: flows/01a03d6e/vision/ethosInterfaces.md
STATUS: NEW -- imperative voice; "request" redundant (implied by slot)

RECORD: 01a03d6e/2 | 2026-08-26 | typed
VERBATIM: "observe is more universal, and reuse is good, because there's going to be multiple nexuses, and if they sort of standardize around a set of commands that are more universal, then the models might even be able to instinctively use a tool or a nexus that they weren't even explicitly trained for, just because of the reuse of these primaries, these primordial principles."
SOURCE: flows/01a03d6e/vision/ethosInterfaces.md
STATUS: NEW -- universal commands across nexuses

---

## Streams

RECORD: 5abf3be8/2 | 2026-08-06 | dictated
VERBATIM: "I think we make stream a forest kind and we could even... Yeah. Yeah. Eventually, I mean, not now, we could potentially write a transformer that also creates the required input objects to initiate and end the stream, although it's not necessary for now. ... But yeah, for now we could just create, write it all by hand and wire it up in the implementation. I'm more interested in getting the syntax right, getting the concepts right, and getting to minimum viable product."
SOURCE: flows/5abf3be8/vision/streamAsFourthKindMvpFirst.md. "forest" = "fourth" per agent transcription note.
STATUS: NEW -- stream as fourth kind; MVP first

---

## Imports and namespaces

RECORD: d63804f2/2 | 2026-08-07 | typed
VERBATIM: "the fixture is blessed, and / for imports"
SOURCE: psyche-raw/Vision/observerFixtureBlessed.md
STATUS: NEW -- / ruled as import separator

RECORD: 2b34fafa/4 | 2026-08-20 | typed
VERBATIM: "this concept is ridiculous in ethos. we're building the foundation and youre talking about wallpaper"
SOURCE: flows/2b34fafa/vision/ethosNamespaces.md
STATUS: NEW -- no namespace inside a file

RECORD: 2b34fafa/5 | 2026-08-20 | typed
VERBATIM: "signal in signal/domain must be resolved from a manifest (which we must spec obviously), which uses datom. if signal has no entry, it will look in the directory of the document where the import takes place. signal/domain would be signal/domain.ethos. if the manifest resolves, signal will point at a source root (need to discuss the naming; lets brainstorm on this), and domain will be the file (domain.ethos)."
SOURCE: flows/2b34fafa/vision/importResolution.md
STATUS: NEW -- SUPERSEDED-BY 2b34fafa/7 (fallback killed)

RECORD: 2b34fafa/6 | 2026-08-20 | typed
VERBATIM: "actually, I think the syntax should be explicit when pulling an external source." / "`signal-pysche:Object` pulls Object from lib.es in signal-psyche source" / "`signal-pysche:[Object Thing]` multiple imports" / "`signal-pysche:stream.[Stream Termination]` from stream.es in signal-psyche source"
SOURCE: flows/2b34fafa/vision/importResolution.md
STATUS: NEW -- colon-syntax imports

RECORD: 2b34fafa/7 | 2026-08-20 | typed
VERBATIM: "confirmed, kill the fallback."
SOURCE: flows/2b34fafa/vision/importResolution.md
STATUS: NEW -- colon = manifest or error; bare path = local only. SUPERSEDES 2b34fafa/5.

RECORD: 2b34fafa/8 | 2026-08-20 | typed
VERBATIM: "I dont think Import is a type; there are no Import's; what exists is an import reference."
SOURCE: flows/2b34fafa/vision/importResolution.md
STATUS: NEW

---

## The map / world model before code

RECORD: 2b34fafa/9 | 2026-08-20 | typed
VERBATIM: "I think training the model to catch themselves before creating a fake trait means we have already failed; the model is trying to write code before it has a *model of the world*. could we say this is about building ontology, anatomy .. a *map* of what we are creating as an object/capability-oriented layout?"
SOURCE: psyche-raw/Vision/worldModelBeforeCode.md
STATUS: NEW

RECORD: 2b34fafa/10 | 2026-08-21 | typed
VERBATIM: "yes, except that it isnt ready to use yet, so the model writes the ethos but has no way to run it (yet)."
SOURCE: psyche-raw/Vision/worldModelBeforeCode.md
STATUS: NEW -- the map is the Ethos interface file

RECORD: 15b67974/1 | 2026-08-22 | typed
VERBATIM: "old code is at most inspiration for that map. (no 'never ...')"
SOURCE: flows/fd301d9a/vision/nexusTraits.md
STATUS: NEW

---

## Ethos-monolith / ethos-zero / ethos-cc

RECORD: 13cfc23f/1 | 2026-08-10 | dictated (excerpt)
VERBATIM: "I want to talk about what I'm going to call the three stacks. The legacy stack, which is the schema and the Noda from before ... And then we have the false stack ... the false new stack, which was a misunderstanding by agents who thought that the components were not demons. And the real new stack ... the old stack, the incorrect new stack, and the correct new stack."
SOURCE: flows/13cfc23f/vision/threeStacks.md
STATUS: REFLECTED (Vision/ethosMonolith.md "Origin", partially)

RECORD: c6b71b4c/1 | 2026-08-10 | dictated (excerpt)
VERBATIM: "So, yeah, I still really much want the new ethos and datum languages ... we could just make a sort of like shortcut where it's just like schema rest, you know, it's ethos rest."
SOURCE: psyche-raw/Vision/archive-threeStacks.md
STATUS: REFLECTED (Vision/ethosMonolith.md "Origin")

RECORD: ba906ae2/2 | 2026-08-14 | dictated (excerpt)
VERBATIM: "the shortcut stack for the new syntax ... we should call it maybe the ethos monolith or something like that ... it's not going to have the nomos and the logos component, it's just going to straight commit to Rust. So we can think of it as more of a monolith ... an incremental implementation slash bootstrap process."
SOURCE: psyche-raw/Vision/rustComponentArchitecture.md
STATUS: REFLECTED (Vision/ethosMonolith.md "Name", "Shape", "Purpose")

RECORD: aa4c7747/2 | 2026-08-24 | dictated
VERBATIM: "Ethos zero ... would be a better name."
SOURCE: flows/aa4c7747/vision/ethosMonolith.md
STATUS: NEW -- ethos-zero name not in Vision/ethosMonolith.md

RECORD: aa4c7747/3 | 2026-08-24 | dictated
VERBATIM: "we need to just go straight for a nexus. So it has to be written as a nexus. And we need to break down what the things that we're going to deal with ... and then we need to isolate the traits, which is the ways in which these things ... interact, and put the proper names on them."
SOURCE: flows/aa4c7747/vision/ethosMonolith.md
SUPERSEDES: aa4c7747 "whatever shape it is taking already will do" (same session, earlier)
STATUS: NEW

RECORD: aa4c7747/4 | 2026-08-24 | typed
VERBATIM: "right, so we need ethos-monolith to bootstrap it. We should call it ethos-cc (compiler compiler); would that be an accurate name for it? And ethos-zero because its version zero which will bootstrap ethos in the nexus trinity stack (with nomos and logos nexuses)"
SOURCE: flows/aa4c7747/vision/ethosMonolith.md
STATUS: NEW -- bootstrap chain and ethos-cc name

RECORD: aa4c7747/5 | 2026-08-25 | typed
VERBATIM: "this is about ethos-monolith right? orchestrate is just the project to test it with, not the center of the work."
SOURCE: flows/aa4c7747/vision/ethosMonolith.md
STATUS: NEW

RECORD: 012fbf07/2 | 2026-08-11 | typed
VERBATIM: "psyche is the fixture. we re-use much of spirit, and introduce a top-level enum; Spirit, Intent, Vision, which differentiates which layer records belong to."
SOURCE: flows/012fbf07/vision/threeStacks.md
STATUS: REFLECTED (Vision/ethosMonolith.md "First fixture")

RECORD: b675f3d9/1 | 2026-08-26 | typed
VERBATIM: "Then we'll make it a nexus. Everything will be a nexus; the consistency will create reliability and increase the quality and clarity"
SOURCE: flows/b675f3d9/vision/ethosMonolith.md
STATUS: NEW -- confirms aa4c7747/3

RECORD: e06e4c07/1 | 2026-08-19 | dictated (excerpt)
VERBATIM: "everything we're going to build is going to be a nexus now, and anything that has already been built that did not take the shape of the nexus is going to be rewritten."
SOURCE: flows/e06e4c07/vision/nexus.md
STATUS: REFLECTED (Vision/ethosMonolith.md "Shape", partially)

---

## MVP scope: trait declaration only

RECORD: aa4c7747/6 | 2026-08-24 | typed
VERBATIM: "When I said traits I just meant trait declaration. Implementation would be a big job; it would mean developping the syntax for full function bodies, and the rust generation - thats not MVP sounding anymore."
SOURCE: flows/aa4c7747/vision/ethosTraitSyntax.md
STATUS: NEW

RECORD: aa4c7747/7 | 2026-08-25 | typed
VERBATIM: "this is quackery. Nonsense. There's no need for this. If we want TryFrom/From, then that's what we'll call it."
SOURCE: flows/aa4c7747/vision/ethosTraitSyntax.md
STATUS: NEW -- no Create alias over TryFrom

RECORD: aa4c7747/8 | 2026-08-25 | typed
VERBATIM: "I approve your trait implementation checking mechanism."
SOURCE: flows/aa4c7747/vision/ethosTraitSyntax.md
STATUS: NEW -- build-time carrying check approved

---

## Kind / Capability / Interaction vocabulary

RECORD: aa4c7747/9 | 2026-08-24 | dictated
VERBATIM: "they're interactions. Yeah, I think interactions are good, because I think that describes it well, what it is really conceptually."
SOURCE: flows/aa4c7747/vision/interactions.md
STATUS: NEW

RECORD: aa4c7747/10 | 2026-08-24 | dictated
VERBATIM: "interactions use the type itself in almost all cases. Well, really in all cases, because if it's not using the type itself, then is it really an interaction of that type?"
SOURCE: flows/aa4c7747/vision/interactions.md
STATUS: NEW

RECORD: aa4c7747/11 | 2026-08-24 | dictated
VERBATIM: "We need to establish a vocabulary too. This is what's happening because no one has ever, or before now, programming was not a thing that was really done in speech. So now we're creating a spoken vocabulary for software engineering."
SOURCE: flows/aa4c7747/vision/spokenVocabulary.md
STATUS: NEW

RECORD: 2b34fafa/11 | 2026-08-21 | dictated
VERBATIM: "we would use the sort of infinitive form of the word, of the verb ... write, read, resolve, create."
SOURCE: psyche-raw/Vision/traitsAsCapabilities.md
STATUS: SUPERSEDED-BY f426777b/6 (lean to qualifier form)

RECORD: f426777b/4 | 2026-08-26 | typed
VERBATIM: "Capability is great, but how do we see 'an object which has a capability' in one word? ... we should even call it logic engineering."
SOURCE: flows/f426777b/vision/spokenVocabulary.md
STATUS: NEW

RECORD: f426777b/5 | 2026-08-26 | typed
VERBATIM: "kind is perfect."
SOURCE: flows/f426777b/vision/spokenVocabulary.md
STATUS: NEW -- Kind ruled as bearer

RECORD: f426777b/6 | 2026-08-26 | typed
VERBATIM: "I also want to lean back to writable > write"
SOURCE: flows/f426777b/vision/spokenVocabulary.md
STATUS: NEW -- qualifier form lean. SUPERSEDES 2b34fafa/11.

RECORD: b675f3d9/2 | 2026-08-26 | typed
VERBATIM: "qualifier. Write isnt a kind. we say kind now, not trait. declare a new kind = declare a new trait, in Ethos world, which will imply some things which arent in rust world (tbd). so in Ethos there are no generics, only kinds."
SOURCE: flows/b675f3d9/vision/kinds.md
STATUS: NEW -- kind = trait; no generics, only kinds

RECORD: b675f3d9/3 | 2026-08-26 | typed
VERBATIM: "capability will refer to the actual functions a kind has (Runnable would be the Kind, run would be a capability)"
SOURCE: flows/b675f3d9/vision/kinds.md
STATUS: NEW

---

## Traits must not be defined implicitly

RECORD: f426777b/7 | 2026-08-26 | psyche's own transcription
VERBATIM: "I don't think we can just define traits implicitly, meaning if we only declare traits in our own version of implementations ... then it'll be difficult. It's going to be complex to try to extract what that trait actually is and how many interactions it has."
SOURCE: flows/f426777b/vision/nexusTraits.md
STATUS: NEW

---

## Costume traits (functions pretending to be traits)

RECORD: 2b34fafa/12 | 2026-08-20 | typed
VERBATIM: "You misunderstood the trait based approach. your trait methods are just regular functions pretending to be traits. if the type needs a 'name' to resove the import, then it's not resolvable. So we found one of the cornerstone of models not understand my vision."
SOURCE: psyche-raw/Vision/traitsAsCapabilities.md
STATUS: NEW

---

## Encoded form / working form and signal form

RECORD: 5abf3be8/3 | 2026-08-06 | typed
VERBATIM: "The encoded form is the code. So the encoded form of ethos is ethos. The textual form is there so that our editors, our current editors, and our current LLM harnesses and models can actually make sense of it."
SOURCE: psyche-raw/Vision/encodedFormIsTheCode.md
STATUS: SUPERSEDED-BY 06196cc7/1

RECORD: 06196cc7/1 | 2026-08-13 | typed
VERBATIM: "ok, working form and signal form, drop code/encoded entirely"
SOURCE: psyche-raw/Vision/encodedFormIsTheCode.md
STATUS: NEW -- SUPERSEDES 5abf3be8/3

---

## Structural parsing and kind syntax

RECORD: b675f3d9/4 | 2026-08-26 | dictated
VERBATIM: "Your kind syntax proposal is very... is completely inappropriate. So start by looking at a rust trait, which is what our kind essentially becomes, and in its most complex form, and doing the anatomy of a rust trait. And then you'll see how many different kinds, how many different types of things are in a trait. Which means you're almost, I'm like, I can guarantee you that you're going to need a struct to fit it all in."
SOURCE: flows/b675f3d9/vision/kinds.md
STATUS: NEW

RECORD: b675f3d9/5 | 2026-08-26 | typed
VERBATIM: "important: in rust, a trait is identified by its name *and* constraints. How would we want to mirror that?"
SOURCE: flows/b675f3d9/vision/kinds.md
STATUS: NEW -- kind identity = name + constraints

RECORD: b675f3d9/6 | 2026-08-27 | dictated (excerpt)
VERBATIM: "I have actually reconsidered the idea that we can use multiple... that the structural parsing can actually discern between structs of different size to differentiate between different types. ... Also, I think we should introduce more of the concept of using different delimiters between the head and the delimiter to add even more type differentiation using very minimal character slash token cost."
SOURCE: flows/b675f3d9/vision/structuralParsing.md
STATUS: NEW -- arity discrimination; multiple head delimiters

RECORD: b675f3d9/7 | 2026-08-27 | dictated
VERBATIM: "<> is a real Protos delimiter of course. I'm surprised you have to ask"
SOURCE: flows/b675f3d9/vision/structuralParsing.md
STATUS: NEW

RECORD: b675f3d9/8 | 2026-08-27 | dictated
VERBATIM: "No. That's not how it works. ... ethos parsing is always dependent on the current context in which the parsing is taking place. So in the import block, colon are treated in a certain way, maybe, maybe not. ... And then the same colon used in another block could be used to, obviously, to mean something else since another block would not involve imports. So like I said, ethos is extremely flexible in how it can use the same thing in different contexts to mean different things."
SOURCE: flows/b675f3d9/vision/structuralParsing.md
STATUS: NEW -- context-dependent parsing

RECORD: b675f3d9/9 | 2026-08-27 | typed
VERBATIM: "a struct {} always has the same fields, in the same order. the struct definition declares the field types, so they can be anything; there are no restriction in which type a field can hold!" / "so if we use a struct for the capability, it's always the same struct type! it cannot change in number of fields!"
SOURCE: flows/b675f3d9/vision/kinds.md
STATUS: NEW -- struct invariant for capability shape

RECORD: b675f3d9/10 | 2026-08-27 | dictated
VERBATIM: "It's perfectly acceptable to have different structures, uh, that result in slightly different types. We use the same mechanism in the, uh, ethos signal interfaces and others to differentiate between things like an enum and a struck [struct] by, uh, checking the, uh, delimiter after the head."
SOURCE: flows/b675f3d9/vision/kinds.md
STATUS: NEW -- delimiter after head discriminates types

RECORD: b675f3d9/11 | 2026-08-27 | typed
VERBATIM: "yes variable length is [] and all components must share a type or kind"
SOURCE: flows/b675f3d9/vision/kinds.md
STATUS: NEW

---

## TryFrom vs effect for nexus processing

RECORD: f426777b/8 | 2026-08-26 | dictated (excerpt)
VERBATIM: "I don't know if try from is the right way to think about something that we are processing ... we're not really trying to get the response. We will get a response as an effect of that, but it's kind of like you wouldn't punch somebody to try and break your own knuckles."
SOURCE: flows/f426777b/vision/nexusTraits.md
STATUS: NEW

RECORD: f426777b/9 | 2026-08-26 | typed
VERBATIM: "I like apply but I'm not certain and the trait suggested for the returned generic made me think of something; we need a new terminology."
SOURCE: flows/f426777b/vision/nexusTraits.md
STATUS: NEW

---

## Title-only stubs

| Stub file | Content location |
|---|---|
| psyche-raw/Vision/ethosNamespaces.md | flows/2b34fafa/vision/ethosNamespaces.md (gathered above) |
| psyche-raw/Vision/ethosSourceFiles.md | flows/2b34fafa/vision/ethosSourceFiles.md + flows/f426777b/vision/ethosSourceFiles.md |
| psyche-raw/Vision/protosIsTheSharedStyle.md | flows/a5587095/vision/protosIsTheSharedStyle.md |
| psyche-raw/Vision/nexus.md | flows/e06e4c07/vision/nexus.md |
| psyche-raw/Vision/streamAsFourthKindMvpFirst.md | flows/5abf3be8/vision/streamAsFourthKindMvpFirst.md (gathered above) |

All stub topics have content in flow vision files; no transcript searches needed.
