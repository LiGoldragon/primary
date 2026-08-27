# Distillation Candidates — Ethos

## What Ethos is and why it exists

RECORD: no-session/1 | 2026-08-01 | recovered
VERBATIM: "youre right; and the answer is the mandatory trait! so T would be a trait! and multiple trait in the declaration would just adjust the emitted rust - remember for us rust is assembly"
SOURCE: psyche-raw/Vision/genericParametersAreTraits.md
STATUS: REFLECTED by Vision/ethos.md §Why Ethos ("Rust is the new assembly")

RECORD: no-session/2 | 2026-08-02 | recovered
VERBATIM: "the two main syntaxes most agents will face; one specifies the types, the other fills them with data — hence why the basic 'cli help' for their dotos objects is meant to emit the ethos syntax that describes their anatomy."
SOURCE: psyche-raw/Vision/archive-ethosDotosDivisionAndHelp.md
STATUS: REFLECTED by Vision/ethos.md §What Ethos is + §Self-description

RECORD: ba906ae2/1 | 2026-08-14 | dictated
VERBATIM (excerpt): "ethos is actually the same reason. Programming languages as they stand right now completely suck. And I wanted something that's easy to read and write that lets me see the interfaces ... the main types and the main traits ... I realized how important they are in design and how I would now want everything, every behavior to fall under a trait, which essentially creates an ontology in code."
SOURCE: psyche-raw/Vision/rustComponentArchitecture.md
STATUS: REFLECTED by Vision/ethos.md §Why Ethos

RECORD: aa4c7747/1 | 2026-08-24 | dictated
VERBATIM: "ethos is essentially meant to give us, for now anyway, the entry or the biggest gain short-term is to give us a language that allows us to, in one swoop, write down our mental model of the machine and write code so that we don't get this problem where the code and the ideas for the code, well, we have psyche for that, but psyche is sort of one step back from the actual hard implementation. It's just that something like Rust or even JavaScript is full of noise. It's like maybe more than half of the code is noise, whereas we want a language that allows us to separate the mental model we have and still write it in code."
SOURCE: flows/aa4c7747/vision/ethos.md
STATUS: NEW — "mental model and code in one swoop", "more than half of the code is noise" not in Vision/ethos.md

RECORD: d2bb5f5f/1 | 2026-08-13 | psyche-approved wording
VERBATIM: "Every method call in our Rust code lives under a trait, because traits are the comprehension surface — the layer where concepts become visible and implementations are constrained to think within them. Rust is the new assembly language: no serious engineer reads all the assembly, and the same is happening to Rust. Traits and main types are what the psyche reads; everything else is implementation detail that Ethos will eventually generate."
SOURCE: psyche-raw/Intent/mandatoryTraits.md
STATUS: REFLECTED by Vision/ethos.md §Why Ethos (partial — "one abstraction up from Rust" is below, not here). This is INTENT, not Vision.

RECORD: f426777b/1 | 2026-08-26 | psyche's own transcription
VERBATIM (excerpt): "We need a different vocabulary because we're moving one abstraction up from Rust. ... I don't like the word 'trait,' if only because it's a bit acoustically ambiguous ... So I want you to do some research in, like, ontology, category theory, how we model the universe, and how we would model this — Ethos specifically — which is our response to all other programming languages"
SOURCE: flows/f426777b/vision/spokenVocabulary.md
STATUS: NEW — "one abstraction up from Rust" and "our response to all other programming languages" not in distilled Vision

## Non-repetition law

RECORD: no-session/3 | 2026-08-01 | recovered
VERBATIM: "we wouldnt repeat Ord; any such repition in ethos syntax is an implementation failure. ethos will be the most terse non-repetitive syntax ever made"
SOURCE: psyche-raw/Vision/archive-ethosNonRepetitionLaw.md
STATUS: REFLECTED by Vision/ethos.md §Non-repetition

## Sections confer traits

RECORD: 5abf3be8/1 | 2026-08-06 | typed (backfill)
VERBATIM: "What other point is there to have different sections?"
SOURCE: flows/5abf3be8/vision/sectionsExistToConferTraits.md
STATUS: NEW — not in any distilled Vision file

RECORD: ba906ae2/2 | 2026-08-14 | typed
VERBATIM: "why not Input Output Refuse, like Write and Read? ... but actually, it might be better to have a shared Process trait? ... because input.input() is a bit weird? input.process() feels more appropriate. but process is overloaded. lets look at some word choices"
SOURCE: psyche-raw/Vision/signalIsOurMessagingLayer.md
STATUS: NEW — section-role trait naming not distilled

## Streams

RECORD: d63804f2/1 | 2026-08-07 | typed
VERBATIM: "a section inside the object" / "Yes, the initiation and termination live in the input."
SOURCE: psyche-raw/Vision/streamSection.md
STATUS: NEW — stream as a section, initiation/termination placement not distilled

## Document kinds and placement

RECORD: f426777b/2 | 2026-08-25 | typed
VERBATIM: "lets make it clear first; the nexus and sema ethos arent designed yet, but when they are they will live in the nexus' main repo"
SOURCE: flows/f426777b/vision/ethosSourceFiles.md
STATUS: NEW — not in Vision/ethosMonolith.md or Vision/ethos.md

RECORD: f426777b/3 | 2026-08-25 | typed
VERBATIM: "I can see a problem already: ... sema and nexus in the signal repos."
SOURCE: flows/f426777b/vision/ethosSourceFiles.md
STATUS: NEW — the triplet-per-repo problem flagged, not distilled

RECORD: 2b34fafa/1 | 2026-08-20 | typed
VERBATIM: "for the monolith thats good enough. easy cognition is the first safe bet."
SOURCE: flows/2b34fafa/vision/ethosSourceFiles.md (one document per file, one Rust module per document)
STATUS: NEW

RECORD: 2b34fafa/2 | 2026-08-20 | typed
VERBATIM: "document sucks. I dont understand your question. What's wrong with File?"
SOURCE: flows/2b34fafa/vision/ethosSourceFiles.md
STATUS: NEW — File, not Document, is the unit

## Imports and namespaces

RECORD: 2b34fafa/3 | 2026-08-20 | typed
VERBATIM: "this concept is ridiculous in ethos. we're building the foundation and youre talking about wallpaper"
SOURCE: flows/2b34fafa/vision/ethosNamespaces.md (namespace inside a file rejected)
STATUS: NEW

RECORD: 2b34fafa/4 | 2026-08-20 | typed
VERBATIM: "signal in signal/domain must be resolved from a manifest (which we must spec obviously), which uses datom. if signal has no entry, it will look in the directory of the document where the import takes place. signal/domain would be signal/domain.ethos."
SOURCE: flows/2b34fafa/vision/importResolution.md
STATUS: NEW — SUPERSEDED-BY 2b34fafa/5 (fallback killed)

RECORD: 2b34fafa/5 | 2026-08-20 | typed
VERBATIM: "actually, I think the syntax should be explicit when pulling an external source." / "`signal-pysche:Object` pulls Object from lib.es in signal-psyche source" / "`signal-pysche:[Object Thing]` multiple imports" / "`signal-pysche:stream.[Stream Termination]` from stream.es in signal-psyche source"
SOURCE: flows/2b34fafa/vision/importResolution.md
STATUS: NEW — colon-syntax imports not distilled. SUPERSEDES 2b34fafa/4.

RECORD: 2b34fafa/6 | 2026-08-20 | typed
VERBATIM: "confirmed, kill the fallback."
SOURCE: flows/2b34fafa/vision/importResolution.md
STATUS: NEW — colon→manifest or error; bare path→local only

RECORD: 2b34fafa/7 | 2026-08-20 | typed
VERBATIM: "I dont think Import is a type; there are no Import's; what exists is an import reference."
SOURCE: flows/2b34fafa/vision/importResolution.md
STATUS: NEW

## The map / world model before code

RECORD: 2b34fafa/8 | 2026-08-20 | typed
VERBATIM: "I think training the model to catch themselves before creating a fake trait means we have already failed; the model is trying to write code before it has a *model of the world*. could we say this is about building ontology, anatomy .. a *map* of what we are creating as an object/capability-oriented layout?"
SOURCE: psyche-raw/Vision/worldModelBeforeCode.md
STATUS: NEW

RECORD: 2b34fafa/9 | 2026-08-21 | typed
VERBATIM: "yes, except that it isnt ready to use yet, so the model writes the ethos but has no way to run it (yet)."
SOURCE: psyche-raw/Vision/worldModelBeforeCode.md (the map is the Ethos interface file)
STATUS: NEW

## Ethos-monolith / ethos-zero / ethos-cc

RECORD: c6b71b4c/1 | 2026-08-10 | dictated
VERBATIM (excerpt): "So, yeah, I still really much want the new ethos and datum languages ... we could just make a sort of like shortcut where it's just like schema rest, you know, it's ethos rest ... Schema and NOTA name the old syntax, Ethos and Datom the new"
SOURCE: psyche-raw/Vision/archive-threeStacks.md
STATUS: REFLECTED by Vision/ethosMonolith.md §Origin (partial)

RECORD: ba906ae2/3 | 2026-08-14 | dictated
VERBATIM (excerpt): "the shortcut stack for the new syntax ... we should call it maybe the ethos monolith or something like that ... it's not going to have the nomos and the logos component, it's just going to straight commit to Rust. So we can think of it as more of a monolith ... an incremental implementation slash bootstrap process. I really want to start writing and reading ethos and datum as soon as possible."
SOURCE: psyche-raw/Vision/rustComponentArchitecture.md
STATUS: REFLECTED by Vision/ethosMonolith.md §Name, §Shape, §Purpose

RECORD: 012fbf07/1 | 2026-08-11 | typed
VERBATIM: "I dont know if we need a core-* repo. I dont see much point. so ethos can have all the code, minus the two signal repos, and so on (3 repos per component). other than reusable libraries of course, which we want to encourage for shared traits especially."
SOURCE: flows/012fbf07/vision/threeStacks.md
STATUS: REFLECTED by Vision/ethosMonolith.md §Vocabulary carried (partial — 3-repos anatomy)

RECORD: 012fbf07/2 | 2026-08-11 | typed
VERBATIM: "psyche is the fixture. we re-use much of spirit, and introduce a top-level enum; Spirit, Intent, Vision, which differentiates which layer records belong to."
SOURCE: flows/012fbf07/vision/threeStacks.md
STATUS: REFLECTED by Vision/ethosMonolith.md §First fixture

RECORD: aa4c7747/2 | 2026-08-24 | dictated
VERBATIM: "Ethos zero ... would be a better name."
SOURCE: flows/aa4c7747/vision/ethosMonolith.md
STATUS: NEW — ethos-zero name not in Vision/ethosMonolith.md

RECORD: aa4c7747/3 | 2026-08-24 | dictated
VERBATIM: "we need to just go straight for a nexus. So it has to be written as a nexus. And we need to break down what the things that we're going to deal with ... and then we need to isolate the traits, which is the ways in which these things ... interact, and put the proper names on them."
SOURCE: flows/aa4c7747/vision/ethosMonolith.md
SUPERSEDES: aa4c7747 "whatever shape it is taking already will do" (same session, earlier)
STATUS: NEW — "go straight for a nexus" direction not in Vision/ethosMonolith.md

RECORD: aa4c7747/4 | 2026-08-24 | typed
VERBATIM: "right, so we need ethos-monolith to bootstrap it. We should call it ethos-cc (compiler compiler); would that be an accurate name for it? And ethos-zero because its version zero which will bootstrap ethos in the nexus trinity stack (with nomos and logos nexuses)"
SOURCE: flows/aa4c7747/vision/ethosMonolith.md
STATUS: NEW — bootstrap chain and ethos-cc not in Vision/ethosMonolith.md

RECORD: aa4c7747/5 | 2026-08-25 | typed
VERBATIM: "this is about ethos-monolith right? orchestrate is just the project to test it with, not the center of the work."
SOURCE: flows/aa4c7747/vision/ethosMonolith.md
STATUS: NEW

RECORD: b675f3d9/1 | 2026-08-26 | typed
VERBATIM: "Then we'll make it a nexus. Everything will be a nexus; the consistency will create reliability and increase the quality and clarity"
SOURCE: flows/b675f3d9/vision/ethosMonolith.md
STATUS: NEW — confirms aa4c7747/3, adds the why

## Every wire interface in Ethos

RECORD: 01a02fd5/1 | 2026-08-24 | typed
VERBATIM: "we'll just say ethos, which will motivate everyone to get ethos working."
SOURCE: flows/01a02fd5/vision/interfaces.md
SUPERSEDES: 01a02fd5 "the interfaces should be written in schema (or ethos if ethos-monolith can already emit working rust)" (same session, minutes earlier)
STATUS: NEW

## MVP scope: trait declaration only

RECORD: aa4c7747/6 | 2026-08-24 | typed
VERBATIM: "When I said traits I just meant trait declaration. Implementation would be a big job; it would mean developping the syntax for full function bodies, and the rust generation - thats not MVP sounding anymore."
SOURCE: flows/aa4c7747/vision/ethosTraitSyntax.md
STATUS: NEW

RECORD: aa4c7747/7 | 2026-08-25 | typed
VERBATIM: "this is quackery. Nonsense. There's no need for this. If we want TryFrom/From, then that's what we'll call it."
SOURCE: flows/aa4c7747/vision/ethosTraitSyntax.md (no Create alias over TryFrom)
STATUS: NEW

RECORD: aa4c7747/8 | 2026-08-25 | typed
VERBATIM: "I approve your trait implementation checking mechanism."
SOURCE: flows/aa4c7747/vision/ethosTraitSyntax.md
STATUS: NEW — build-time carrying check approved

## Ethos generation of Rust

RECORD: ba906ae2/4 | 2026-08-14 | dictated
VERBATIM (excerpt): "I could point at a certain object and it would print out its schema and ethos syntax, which is very self-describing and very self-evident"
SOURCE: psyche-raw/Vision/rustComponentArchitecture.md
STATUS: REFLECTED by Vision/ethos.md §Self-description

## The three stacks

RECORD: c6b71b4c/1 | 2026-08-10 | dictated
(See entry under ethos-monolith above — same record.)
STATUS: REFLECTED by Vision/ethosMonolith.md §Origin

## Vocabulary: Kind, Capability, Interaction

RECORD: aa4c7747/9 | 2026-08-24 | dictated
VERBATIM: "they're interactions. Yeah, I think interactions are good, because I think that describes it well, what it is really conceptually."
SOURCE: flows/aa4c7747/vision/interactions.md
STATUS: NEW — "interactions" as term for trait implementations not distilled

RECORD: aa4c7747/10 | 2026-08-24 | dictated
VERBATIM: "interactions use the type itself in almost all cases. Well, really in all cases, because if it's not using the type itself, then is it really an interaction of that type?"
SOURCE: flows/aa4c7747/vision/interactions.md
STATUS: NEW

RECORD: f426777b/4 | 2026-08-26 | typed
VERBATIM: "Capability is great, but how do we see 'an object which has a capability' in one word? ... we should even call it logic engineering."
SOURCE: flows/f426777b/vision/spokenVocabulary.md
STATUS: NEW

RECORD: f426777b/5 | 2026-08-26 | typed
VERBATIM: "kind is perfect."
SOURCE: flows/f426777b/vision/spokenVocabulary.md
STATUS: NEW — Kind ruled as bearer of capabilities

RECORD: f426777b/6 | 2026-08-26 | typed
VERBATIM: "I also want to lean back to writable > write"
SOURCE: flows/f426777b/vision/spokenVocabulary.md
STATUS: NEW — revises 2b34fafa/infinitive-verb ruling

## Traits must not be defined implicitly

RECORD: f426777b/7 | 2026-08-26 | psyche's own transcription
VERBATIM: "I don't think we can just define traits implicitly, meaning if we only declare traits in our own version of implementations, of how we implement them, then it'll be difficult. It's going to be complex to try to extract what that trait actually is and how many interactions it has."
SOURCE: flows/f426777b/vision/nexusTraits.md
STATUS: NEW

## TryFrom vs effect for nexus processing

RECORD: f426777b/8 | 2026-08-26 | dictated
VERBATIM (excerpt): "I don't know if try from is the right way to think about something that we are processing ... we're not really trying to get the response. We will get a response as an effect of that, but it's kind of like you wouldn't punch somebody to try and break your own knuckles."
SOURCE: flows/f426777b/vision/nexusTraits.md
STATUS: NEW

RECORD: f426777b/9 | 2026-08-26 | typed
VERBATIM: "I like apply but I'm not certain and the trait suggested for the returned generic made me think of something; we need a new terminology."
SOURCE: flows/f426777b/vision/nexusTraits.md
STATUS: NEW

## The encoded form / working form and signal form

RECORD: 5abf3be8/2 | 2026-08-06 | dictated
VERBATIM (excerpt): "The encoded form is the code. So the encoded form of ethos is ethos. The textual form is there so that our editors, our current editors, and our current LLM harnesses and models can actually make sense of it."
SOURCE: psyche-raw/Vision/encodedFormIsTheCode.md
STATUS: SUPERSEDED-BY 06196cc7/1

RECORD: 06196cc7/1 | 2026-08-13 | typed
VERBATIM: "ok, working form and signal form, drop code/encoded entirely"
SOURCE: psyche-raw/Vision/encodedFormIsTheCode.md
STATUS: NEW — SUPERSEDES 5abf3be8/2

## Costume traits

RECORD: 2b34fafa/10 | 2026-08-20 | typed
VERBATIM: "You misunderstood the trait based approach. your trait methods are just regular functions pretending to be traits. if the type needs a 'name' to resove the import, then it's not resolvable. So we found one of the cornerstone of models not understand my vision."
SOURCE: psyche-raw/Vision/traitsAsCapabilities.md
STATUS: NEW

## Spoken vocabulary for software engineering

RECORD: aa4c7747/11 | 2026-08-24 | dictated
VERBATIM: "We need to establish a vocabulary too. This is what's happening because no one has ever, or before now, programming was not a thing that was really done in speech. So now we're creating a spoken vocabulary for software engineering."
SOURCE: flows/aa4c7747/vision/spokenVocabulary.md
STATUS: NEW

## Everything will be a nexus

RECORD: e06e4c07/1 | 2026-08-19 | dictated
VERBATIM (excerpt): "everything we're going to build is going to be a nexus now, and anything that has already been built that did not take the shape of the nexus is going to be rewritten."
SOURCE: flows/e06e4c07/vision/nexus.md
STATUS: REFLECTED by Vision/ethosMonolith.md §Shape (partial)

---

## Title-only stubs requiring transcript search

| Stub file | Originating session | Notes |
|---|---|---|
| psyche-raw/Vision/ethosNamespaces.md | 2b34fafa | Content exists in flows/2b34fafa/vision/ethosNamespaces.md — not a stub-needing-transcript |
| psyche-raw/Vision/ethosSourceFiles.md | 2b34fafa | Content exists in flows/2b34fafa/vision/ethosSourceFiles.md — not a stub-needing-transcript |
| psyche-raw/Vision/protosIsTheSharedStyle.md | a5587095 | Content exists in flows/a5587095/vision/protosIsTheSharedStyle.md |
| psyche-raw/Vision/nexus.md | e06e4c07 | Content exists in flows/e06e4c07/vision/nexus.md |
| psyche-raw/Vision/streamAsFourthKindMvpFirst.md | unknown | Title only: "I think we make stream a forest kind" — no content, no session id; transcript search needed |
