# Distillation Candidates: Kinds, Capabilities, Interactions, Ontology-Based Design

## Sub-topic: The word for what Rust calls "trait"

**6863ef19-6** | 2026-08-13 | typed | NEW
> all traits will be qualifiers. I disagree with rust's convention (Write Read should be Writable and Readable).
> lets look at an update to the skills, and reconsider traits as "capabilities". Rethink the whole concept over and represent it this way
Source: flows/6863ef19/vision/traitsAsCapabilities.md
SUPERSEDED-BY f426777b-11 (vocabulary one abstraction up), f426777b-13 (kind ruled)

**f426777b-11** | 2026-08-26 | psyche's own transcription | NEW
> And I don't like the word "trait," if only because it's a bit acoustically ambiguous, maybe--kind of like how the Rust language often is mistaken for REST, R-E-S-T.
Source: flows/f426777b/vision/spokenVocabulary.md
SUPERSEDES 6863ef19-6 (now not just qualifiers but a new vocabulary entirely)

**f426777b-12** | 2026-08-26 | typed | NEW
> Capability is great, but how do we see "an object which has a capability" in one word? Because that's basically what we're looking for here; a new way to *speak* software engineering at a higher, more correct layer of abstraction. we should even call it logic engineering.
> Something that can run is a runner. "something that can X" ... a Kind? Seems that type would also work.
Source: flows/f426777b/vision/spokenVocabulary.md

**f426777b-13** | 2026-08-26 | typed | NEW
> kind is perfect.
Source: flows/f426777b/vision/spokenVocabulary.md
SUPERSEDES 6863ef19-6 ("capabilities" as the trait word), f426777b-12 (Kind? floated, now ruled)

**b675f3d9-7** | 2026-08-26 | typed | NEW
> 1. qualifier. Write isnt a kind. we say kind now, not trait. declare a new kind = declare a new trait, in Ethos world, which will imply some things which arent in rust world (tbd). so in Ethos there are no generics, only kinds.
Source: flows/b675f3d9/vision/kinds.md
SUPERSEDES f426777b-13 (extends: "we say kind now, not trait" and the implication that declaring a kind implies more than Rust)

---

## Sub-topic: Capability = a function a kind has

**b675f3d9-8** | 2026-08-26 | typed | NEW
> 4. capability will refer to the actual functions a kind has (Runnable would be the Kind, run would be a capability)
Source: flows/b675f3d9/vision/kinds.md
SUPERSEDES f426777b-12 ("Capability is great" — now sealed with a specific meaning: a function, not the bearer)

---

## Sub-topic: Trait/kind naming form (qualifier vs infinitive vs verb)

**6863ef19-6** | 2026-08-13 | typed | SUPERSEDED-BY 06196cc7-20
> all traits will be qualifiers. I disagree with rust's convention (Write Read should be Writable and Readable).
Source: flows/6863ef19/vision/traitsAsCapabilities.md
(Same record as above — also bears on naming form)

**06196cc7-20** | 2026-08-13 | typed | SUPERSEDED-BY 06196cc7-21
> Or maybe we need to accept verbs for traits, since theyre capitalized and therefore not a function
Source: flows/06196cc7/vision/traitsAsCapabilities.md (excerpt)

**06196cc7-21** | 2026-08-14 | typed | SUPERSEDED-BY 2b34fafa-31
> Yes, I accept verbs. now I can see why rust went with verbs; it is easy to understand that a thing that which implements Run is CapableOfRunning.
Source: flows/06196cc7/vision/traitsAsCapabilities.md

**2b34fafa-31** | 2026-08-21 | dictated | SUPERSEDED-BY f426777b-14
> we would use the sort of infinitive form of the word, of the verb, I mean. If it's an action that can be purely described as an action, like write, read, resolve, create.
Source: psyche-raw/Vision/traitsAsCapabilities.md (excerpt; full in assembly.md 2026-08-21)

**f426777b-14** | 2026-08-26 | typed | SUPERSEDED-BY b675f3d9-7
> I also want to lean back to writable > write
Source: flows/f426777b/vision/spokenVocabulary.md

**b675f3d9-7** | 2026-08-26 | typed | NEW
> qualifier. Write isnt a kind.
Source: flows/b675f3d9/vision/kinds.md
Seals the supersession chain: qualifier form wins. The infinitive ruling (2b34fafa-31) is dead.

---

## Sub-topic: Interactions = implementations

**aa4c7747-10** | 2026-08-24 | dictated | NEW
> they're interactions. Yeah, I think interactions are good, because I think that describes it well, what it is really conceptually.
Source: flows/aa4c7747/vision/interactions.md

**aa4c7747-11** | 2026-08-24 | dictated | NEW
> interactions use the type itself in almost all cases. Well, really in all cases, because if it's not using the type itself, then is it really an interaction of that type?
Source: flows/aa4c7747/vision/interactions.md

---

## Sub-topic: Generics are traits/kinds

**[no-session]-1** | 2026-08-01 | typed | SUPERSEDED-BY b675f3d9-7
> youre right; and the answer is the mandatory trait! so T would be a trait! and multiple trait in the declaration would just adjust the emitted rust - remember for us rust is assembly
Source: psyche-raw/Vision/genericParametersAreTraits.md (recovered, no session id)

**f426777b-11** | 2026-08-26 | psyche's own transcription | NEW (excerpt)
> So we already went over the fact that, for us, a generic is a trait--or unless there's maybe something I don't see right now, but as far as I can tell.
Source: flows/f426777b/vision/spokenVocabulary.md

**b675f3d9-7** | 2026-08-26 | typed | NEW
> so in Ethos there are no generics, only kinds.
Source: flows/b675f3d9/vision/kinds.md
SUPERSEDES [no-session]-1 (T is a trait → no generics, only kinds)

---

## Sub-topic: Kind identity and declaration

**b675f3d9-9** | 2026-08-26 | dictated | NEW
> Your kind syntax proposal is very... is completely inappropriate. So start by looking at a rust trait, which is what our kind essentially becomes, and in its most complex form, and doing the anatomy of a rust trait. [...] I can guarantee you that you're going to need a struct to fit it all in. Or maybe even a root enum to differentiate between different kinds of kinds
Source: flows/b675f3d9/vision/kinds.md (excerpt)

**b675f3d9-10** | 2026-08-26 | typed | NEW
> important: in rust, a trait is identified by its name *and* constraints. How would we want to mirror that?
Source: flows/b675f3d9/vision/kinds.md

**b675f3d9-11** | 2026-08-26 | typed | NEW
> I prefer
> Processable<[Clonable Sendable]  Serializable>
Source: flows/b675f3d9/vision/kinds.md

> do you mean associated types? What is Ref? If we want to refer to existing rust traits in the non-verbal way, we'll have to maintain a table for conversion. but that will incure a cost. it might be better to keep the existing trait as-is
Source: flows/b675f3d9/vision/kinds.md

> dont worry, you understood what I meant; the identity parts of the data.
Source: flows/b675f3d9/vision/kinds.md

**b675f3d9-12** | 2026-08-27 | typed | NEW
> a struct {} always has the same fields, in the same order. the struct definition declares the field types, so they can be anything; there are no restriction in which type a field can hold!
> so if we use a struct for the capability, it's always the same struct type! it cannot change in number of fields!
Source: flows/b675f3d9/vision/kinds.md

**b675f3d9-13** | 2026-08-27 | dictated | SUPERSEDES b675f3d9-12
> It's perfectly acceptable to have different structures, uh, that result in slightly different types. We use the same mechanism in the, uh, ethos signal interfaces and others to differentiate between things like an enum and a struck [struct] by, uh, checking the, uh, delimiter after the head.
Source: flows/b675f3d9/vision/kinds.md

**b675f3d9-14** | 2026-08-27 | typed | NEW
> yes variable length is [] and all components must share a type or kind
Source: flows/b675f3d9/vision/kinds.md

---

## Sub-topic: Structural-form Capability enum

**b675f3d9-15** | 2026-08-27 | dictated + handwritten | NEW
> I have actually reconsidered the idea that we can use multiple... that the structural parsing can actually discern between structs of different size to differentiate between different types.
Source: flows/b675f3d9/vision/structuralParsing.md

Handwritten page (image is authoritative; transcription):
```
Capability.[                    ;; A Vector-represented Enum
  SingleYield.{Name Concept}
  ;; Represented as 'Head.Concept'
  ;; A Concept being a type or a Kind
  MutableSingleYield.{Name Concept}
  ;; Head!Concept
  MultipleYields.{Name Vector<Concept>}
  ;; Name.[ConceptOne ConceptTwo ...]
  Multiple-
  Standard.{Name Vector<Concept> Vector<Concept>}
  ;; Head.{[InputOne InputTwo] [OutputOne OutputTwo]}
  ...
]
```

**b675f3d9-16** | 2026-08-27 | dictated | NEW
> No. That's not how it works. [...] ethos parsing is always dependent on the current context in which the parsing is taking place. [...] the same colon used in another block could be used to, obviously, to mean something else since another block would not involve imports.
Source: flows/b675f3d9/vision/structuralParsing.md

---

## Sub-topic: Traits declared explicitly, not extracted

**f426777b-2** | 2026-08-26 | psyche's own transcription | NEW
> I don't think we can just define traits implicitly, meaning if we only declare traits in our own version of implementations, of how we implement them, then it'll be difficult. It's going to be complex to try to extract what that trait actually is and how many interactions it has.
Source: flows/f426777b/vision/nexusTraits.md

**aa4c7747-18** | 2026-08-24 | dictated | NEW
> And so we need to define what the trait syntax for Ethos is

**aa4c7747-19** | 2026-08-24 | typed | NEW
> When I said traits I just meant trait declaration. Implementation would be a big job [...] thats not MVP sounding anymore.
Source: flows/aa4c7747/vision/ethosTraitSyntax.md

---

## Sub-topic: Types first, then traits; sections confer traits

**psyraw-6863ef19** | 2026-08-13 | dictated | NEW
> we need to think very carefully of what the types are. First, really, because the traits are something that the types implement. We don't look for traits and then think of types for that.
Source: psyche-raw/Vision/traitsAsCapabilities.md (session 6863ef19)

**5abf3be8-sect** | 2026-08-06 | typed | NEW
> What other point is there to have different sections?
Source: flows/5abf3be8/vision/sectionsExistToConferTraits.md
Context: sections exist to confer traits (Input, Output, Refusal)

---

## Sub-topic: Ontology / world model before code / the map

**e06e4c07-16** | 2026-08-19 | dictated | NEW (excerpt)
> It uses a software ontology using traits, which hasn't been done properly yet [...] the first implementation just simply created placeholder traits for every function, and just sort of mindlessly created traits that don't create a sensible ontology. And there's going to have to be a lot to be done in terms of creating training for this to be understood better by agents, and also creating a workflow for this, for any ontology to be designed properly before it's implemented.
Source: flows/e06e4c07/vision/nexus.md (session e06e4c07)

**2b34fafa-27** | 2026-08-20 | typed | NEW
> I think training the model to catch themselves before creating a fake trait means we have already failed; the model is trying to write code before it has a *model of the world*. could we say this is about building ontology, anatomy .. a *map* of what we are creating as an object/capability-oriented layout?
Source: psyche-raw/Vision/worldModelBeforeCode.md

**2b34fafa-28** | 2026-08-21 | typed | NEW
> yes, except that it isnt ready to use yet, so the model writes the ethos but has no way to run it (yet).
Source: psyche-raw/Vision/worldModelBeforeCode.md
Confirms: the map = the Ethos interface file.

**15b67974-22** | 2026-08-22 | typed | NEW
> old code is at most inspiration for that map. (no "never ...")
Source: flows/15b67974/vision/worldModelBeforeCode.md

**2b34fafa-29** | 2026-08-21 | typed | NEW
> we still need to establish the protocol for create the anatomy of a well designed object and capabilities oriented machine.
Source: psyche-raw/Vision/worldModelBeforeCode.md (excerpt)

---

## Sub-topic: Costume traits / training problem

**2b34fafa-30** | 2026-08-20 | typed | NEW
> You misunderstood the trait based approach. your trait methods are just regular functions pretending to be traits. if the type needs a 'name' to resove the import, then it's not resolvable. So we found one of the cornerstone of models not understand my vision. Do a research in this
Source: psyche-raw/Vision/traitsAsCapabilities.md

---

## Sub-topic: Mandatory traits (Intent)

**d2bb5f5f-1** | 2026-08-13 | psyche-approved wording | REFLECTED (Intent/mandatoryTraits.md)
> Every method call in our Rust code lives under a trait, because traits are the comprehension surface -- the layer where concepts become visible and implementations are constrained to think within them. Rust is the new assembly language: no serious engineer reads all the assembly, and the same is happening to Rust. Traits and main types are what the psyche reads; everything else is implementation detail that Ethos will eventually generate.
Source: psyche-raw/Intent/mandatoryTraits.md

---

## Sub-topic: The 3-part machine (anatomy)

**2b34fafa-22** | 2026-08-21 | dictated | SUPERSEDED-BY 2b34fafa-23
> there's sort of always at least four parts. One is input, receiving, then structuring these inputs [...] and then what we want [...] you have to put it all together into something that is coherent [...] under one trait. Easy, easily discoverable.
Source: psyche-raw/Vision/machineAnatomy.md (excerpt)

**2b34fafa-23** | 2026-08-21 | typed | NEW
> agglomerate multiple types -> create a coherent type -> convert it to another type
Source: psyche-raw/Vision/machineAnatomy.md
SUPERSEDES 2b34fafa-22 (4-part → 3-part). The principle nests fractally.

**2b34fafa-24** | 2026-08-21 | typed | NEW
> 1. thats just one form of it. the machine might be accumulating variables in a method's body. Im not investing into a single form like this.
> 2. [...] the coherent input becomes the block of string thus assembled. it could still have a type if we want to be very correct, such as an ImplString or and ImplSignatureString or VariableAssignmentString, or whatever.
Source: psyche-raw/Vision/machineAnatomy.md

---

## Sub-topic: Effect vs conversion (the punch teaching)

**f426777b-1** | 2026-08-26 | dictated | NEW
> I don't know if try from is the right way to think about something that we are processing. [...] because what we're doing when we're processing something or when we're... when an object is going into the nexus for an effect to take place, what... conceptually, we're not really trying to get the response. We will get a response as an effect of that, but it's kind of like you wouldn't punch somebody to try and break your own knuckles. The whole point is to hit him and damage him, not to hurt your fist. Although you might hurt your fist.
Source: flows/f426777b/vision/nexusTraits.md

**f426777b-3** | 2026-08-26 | typed | TENSION
> I like apply but I'm not certain and the trait suggested for the returned generic made me think of something; we need a new terminology.
Source: flows/f426777b/vision/nexusTraits.md

**b675f3d9-3** | 2026-08-26 | typed | NEW
> 2. You proposed a term for this which I liked, but now cannot recall. remind me.
Source: flows/b675f3d9/vision/spokenVocabulary.md

TENSION: "I like apply" (f426777b-3) vs "we need a new terminology" (same record). The psyche liked but was not certain of "apply"; directed that a new terminology is needed; later could not recall the liked term (b675f3d9-3). Unresolved.

---

## Sub-topic: From over Into, demand-driven

**2b34fafa-25** | 2026-08-21 | typed | NEW
> I think the From is better than Into, since in reality, we need to create things *from* other things; nobody harvests a material and then asks what this can be made into; everything is demand-driven.
Source: psyche-raw/Vision/worldModelBeforeCode.md

---

## Sub-topic: No Create trait; TryFrom/From by their own names

**2b34fafa-26** | 2026-08-21 | dictated | SUPERSEDED-BY 2b34fafa-wm3
> when something has a new method, it means that it can be created. So that's a property, that's a trait [...] I think that that trait would be create
Source: psyche-raw/Vision/assembly.md (excerpt)

**2b34fafa-wm3** | 2026-08-21 | typed | NEW
> it would just be TryFrom, not create, so theres nothing to make.
Source: psyche-raw/Vision/worldModelBeforeCode.md
SUPERSEDES 2b34fafa-26 (Create dissolved into TryFrom)

**aa4c7747-21** | 2026-08-25 | typed | NEW
> this is quackery. Nonsense. There's no need for this. If we want TryFrom/From, then that's what we'll call it.
Source: flows/aa4c7747/vision/ethosTraitSyntax.md
Reinforces: existing Rust traits kept by their Rust names.

---

## Sub-topic: Tuples and kinds

**aa4c7747-14** | 2026-08-24 | typed | NEW
> tuple: no tuple in the code we design: if some parts require it (standard traits, dependencies), then we allow it at that contact point only
Source: flows/aa4c7747/vision/tuples.md

---

## Sub-topic: Spoken vocabulary / logic engineering

**aa4c7747-3** | 2026-08-24 | dictated | NEW
> We need to establish a vocabulary too. This is what's happening because no one has ever, or before now, programming was not a thing that was really done in speech. So now we're creating a spoken vocabulary for software engineering.
Source: flows/aa4c7747/vision/spokenVocabulary.md

**f426777b-12** | 2026-08-26 | typed | NEW (excerpt)
> we should even call it logic engineering.
Source: flows/f426777b/vision/spokenVocabulary.md

---

## Sub-topic: Ethos as mental model and code in one swoop

**aa4c7747-13** | 2026-08-24 | dictated | REFLECTED (partial, in Vision/ethos.md "why")
> ethos is essentially meant to give us [...] a language that allows us to, in one swoop, write down our mental model of the machine and write code so that we don't get this problem where the code and the ideas for the code [...] Rust or even JavaScript is full of noise [...] more than half of the code is noise
Source: flows/aa4c7747/vision/ethos.md

---

## Sub-topic: Ontology in code via traits

**ba906ae2-1** | 2026-08-14 | dictated | REFLECTED (partial, in Vision/ethos.md "why")
> I realized how important they are in design and how I would now want everything, every behavior to fall under a trait, which essentially creates an ontology in code.
Source: psyche-raw/Vision/rustComponentArchitecture.md (session ba906ae2; excerpt)

---

## Sub-topic: Universal nexus traits

**e06e4c07-13** | 2026-08-19 | typed | NEW
> We need to first design universal nexus traits, which would be the basic ontology of an actor/dataflow software system.
Source: flows/e06e4c07/vision/nexus.md (session e06e4c07)

---

## TENSIONS SUMMARY

1. **Apply vs new terminology** (UNRESOLVED): f426777b-3 "I like apply but I'm not certain" + "we need a new terminology"; b675f3d9-3 "You proposed a term [...] which I liked, but now cannot recall."

2. **Struct-always-same-fields vs different-structures-different-types** (RESOLVED in favor of different structures): b675f3d9-12 "a struct {} always has the same fields" then b675f3d9-13 (next day, dictated) "It's perfectly acceptable to have different structures [...] that result in slightly different types." The later supersedes.

3. **Infinitive vs qualifier** (RESOLVED): The chain 6863ef19-6 (qualifier) → 06196cc7-20/21 (verbs accepted) → 2b34fafa-31 (infinitive ruled) → f426777b-14 (lean back to qualifier) → b675f3d9-7 ("qualifier. Write isnt a kind.") — qualifier wins.

4. **"Trait" disliked, no single replacement sealed**: f426777b-11 dislikes "trait" acoustically. Kind is ruled for the bearer (f426777b-13). Capability is ruled for the function (b675f3d9-8). But the word that replaces "trait" itself (the declaration of a kind's capabilities and their interactions) has no sealed name. "Trait declaration" is still used operationally.
