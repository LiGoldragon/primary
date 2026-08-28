# Distillation round 5: protos, datom, ethos, ethos interfaces, ethos-monolith, kinds, anatomy, portion, spokenVocabulary, rustConventions

Composed in flow 2ef42163, superseding round 4 (flows/acbb6006/reports/distillProposalRound4.md). Incorporates the 04db2fd2 vision entries round 4 was absent on, and the corrections ruled since round 4 was drafted. Each statement lands only on the living's approval.

Changes from round 4:
- Realize/real renamed to embody/embodied throughout (2ef42163 ruling: "embody." over forge).
- Yields always in [], even a single yield (04db2fd2 ruling); round 4's SingleYield written Head.Concept is superseded.
- Result<A F> is the fallible yield; the struct form is for complex kinds (04db2fd2 ruling).
- protos.md is (additions), not (new): Direction already landed (commit 10a2eb054).
- "A Head is always a variant" and "key/value resolving by position in a map" are both now ruled and landed in Vision/datom.md; round 4's "Not stated (unruled)" paragraph is removed.
- The direction kinds are settled: the actual type bears both Embodiable and Textualizable. There is no separate Embodied type; "embodied" is vocabulary for the bearer once in its Rust form. `⟦Delineated|Delineatable⟧` marks the delineation kind whose -able form is under discussion.
- ~30 entries from 04db2fd2 vision/ absorbed; impurities listed under Discards.

---

# Vision/protos.md (additions; Direction is a revision of the landed section)

## Direction (revision of the landed section)
Text arrives as a prospective value and leaves as a value. Embody reads the textual form into the embodied form and may fault: the text is prospective until it matches its anatomy. Textualize writes the embodied form into the textual form and cannot fault: an embodied value is already whole. Spans are found on the way in and computed on the way out. Each direction is several passes.

Sources: 06196cc7 direction, 04db2fd2 directionAsymmetry, 04db2fd2 multiPass, 2ef42163 kinds

## The shared style
Protos is the name of the style all our dialects share. The final, fully decomposed engine with its three daemons is the protos engine; Datom sits beside it, a protos dialect for pure typed data only, outside the Ethos/Nomos/Logos Rust-generation engine.

Sources: a5587095 protos, ba906ae2 protos

## Everything is data
The dot opens a delimiter, and everything is data. The textual form of a thing is data, and so a type.

Sources: 5abf3be8 protos, 6863ef19 protos

## One representation
A type has one protos representation.

Sources: 6863ef19 protos

## Structure tells the type
Structural parsing tells types apart by structure: structs of different size are different types, and the delimiter between the head and the body adds further type differentiation at the cost of one character.

Sources: b675f3d9 structuralParsing

## Struct and vector
A struct always has the same fields in the same order; its definition declares the field types, and a field may hold any type. Variable length is a vector, and all its components share one type or one kind.

Sources: b675f3d9 kinds

## Angle brackets
Angle brackets are a protos delimiter. Datom and Ethos keep angle brackets compatible, so that datom may one day be embedded in ethos positions.

Sources: b675f3d9 kinds, ac1e9ec8 datomSyntax

## Forms of a value
A value has an embodied form, a signal form, and a textual form. Code, encoded, working, and transcodable are retired words.

Sources: 06196cc7 direction, 6863ef19 protos, 2ef42163 kinds

## Prospective
Text taken as a would-be T is Prospective<T>. The text is prospective until it matches the expected type.

Sources: 04db2fd2 textualTypes

## Shape-defined types
ShapeDefined is the kind a protos type bears. Implementing it is a match over the standard shapes, each shape with its own parsing context; a more complex type is a vector of shapes, the structure dictating the outer type.

Sources: a5587095 protos, 06196cc7 direction

## Delineation and anatomy are protos
Delineation is protos: the untyped structural pass that identifies portions. Anatomy is protos: the shape of an object can be described independently of the type it represents.

Sources: 04db2fd2 anatomy, 04db2fd2 delineate

## Pure anatomy
For protos a Head is just a Head: anatomy, not interpretation. Pure anatomy is structural recognition of delineations, nothing more.

Sources: 04db2fd2 anatomy

## Brace arity is anatomical
The number of components in a brace-enclosed portion is anatomical; in a bracket-enclosed portion it is not.

Sources: 04db2fd2 anatomy

## A type's anatomy belongs to its dialect
A type's anatomy is dialect-specific, not protos. The universal structural machinery is protos; the anatomy of a particular type is defined by the dialect it belongs to.

Sources: 04db2fd2 kinds

## Parentheses are a dialect delimiter
Parentheses are a dialect delimiter, not protos. Their content is opaque to delineation: anatomical features inside do not trigger structural recognition.

Sources: 04db2fd2 delimiters

## Logic planes
A big implementation is the sign of a missing logic plane. Everything is simple individually; the complexity is in the totality.

Sources: a5587095 protos

---

# Vision/datom.md (additions)

## Datom is a kind
Datom is a kind, not a type, because it lacks a definite shape: a particular type of datom has a definite shape. The kind is named Datomic.

Sources: 04db2fd2 anatomy, 04db2fd2 textualTypes

## Direction in datom
Inbound, a prospective datom is untrusted until it matches its anatomy; outbound, it is a datom. Embody carries a fault; Textualize does not. A Prospective<Datom> is `⟦Delineated|Delineatable⟧`.

Sources: 04db2fd2 directionAsymmetry, 04db2fd2 delineate

## Text
Text is more than String: non-structural whitespace is removed. A reliable content-addressed hash may be tied to normalized Text for cached reading.

Sources: 04db2fd2 text

## Library
The datom library is renamed to free the name datom for the eventual nexus.

Sources: 04db2fd2 text

## Datom as a nexus
Datom stays a library for now. Eventually it becomes a nexus: a service to translate datom objects between formats. Consistency favors everything being a nexus; the library path is kept until the nexus shape is clear.

Sources: 04db2fd2 datomNexus

---

# Vision/datom.md Syntax (revision)

Round 4 proposed a Syntax section that carried a "Not stated (unruled)" paragraph. Both items in that paragraph are now ruled and landed (guillemets with key/value by position; a Head is always a variant). The paragraph is removed. The rest of the Syntax section is unchanged from round 4:

## Syntax
Consistency comes first: datom's syntax is fixed before the rest. The dot opens a delimiter. The dotted prefix of a delimited block is its Head, part of the block's type; a variant re-emits its Head when textualized. A bare brace block is a struct. Curly quotes delimit strings; parentheses are reserved for structured strings, Meaning. A string is a string only in a position where the type defines a string; there a string that needs no quotes is written bare, and a bare string may carry symbols that are load-bearing elsewhere, the machinery made fit for this by the right abstraction layers. A string block is opaque: interior delimiters are content until the block closes. Guillemets delimit a map; a position expecting a map carries no Map head. An integer is bare decimal: 0, 42, -42.

Sources: 06196cc7 datomSyntax, ac1e9ec8 datomSyntax, 01a03eda datomSyntax, 04db2fd2 datomMaps

---

# Vision/ethos.md (additions)

## The delimiter after the head tells the type
X.{...} declares a struct, Y.[...] an enum: the delimiter after the head tells the type. The same mechanism serves wherever several types share one position -- in the signal interfaces and elsewhere.

Sources: 236af273 ethos, a5587095 protos, b675f3d9 structuralParsing

## A block gives its characters their meaning
Ethos parsing depends on the block being parsed: a colon in an import block is the import form; the same colon in another block means what that block says. Ethos uses the same thing in different contexts to mean different things.

Sources: b675f3d9 structuralParsing

## Angle brackets hold kinds
Angle brackets hold the kinds in a type's positions -- Result<Vector<Sortable> Error> -- chosen for token economy and because it recycles Rust cognition.

Sources: 6b31eff3 ethos, b675f3d9 kinds

## One abstraction up
Ethos is one abstraction up from Rust: our response to all other programming languages, a higher level of abstraction than any of them. It gives, in one swoop, the mental model of the machine and the code for it, where Rust or JavaScript is full of noise -- more than half of the code is noise.

Sources: aa4c7747 ethos, f426777b ethos

## File and source
The unit of Ethos is the file. A source is what Rust calls a crate.

Sources: 2b34fafa ethos

## What Ethos generates, and where it lives
Ethos generates the Rust for the wire types (signal), the major internal engine operation types (nexus), and the database types (sema). Every wire interface is written in Ethos, in the component's signal repositories. The nexus and sema Ethos, once designed, live in the component's main repository.

Sources: 019feb93 ethos, 01a02fd5 ethos, f426777b ethos

## Kinds are checked at build time
Ethos checks at build time that a type carries the kinds it claims.

Sources: aa4c7747 ethos

## The trinity
Ethos, Nomos and Logos are nexuses, each with the architecture of every other component, all messages signal. Everything is in the nexus: the Ethos nexus loads the Ethos and holds the whole thing.

Sources: 55d18f4f ethos

---

# Vision/ethosInterfaces.md (new)

## Sections confer
Sections exist to confer a kind on their items -- Input, Output, Refusal. An item in the input slot is a request by standing there; the word request is redundant.

Sources: 5abf3be8 ethosInterfaces, 01a03d6e ethosInterfaces

## Imperative voice
An interface is designed verb-oriented, in the imperative voice: list, observe. Commands universal across nexuses -- observe above all -- are reused, so that a model can use a nexus it was never trained on from the primordial commands it already knows.

Sources: 01a03d6e ethosInterfaces

## Streams
A stream is a section inside the object, the fourth kind of section; its initiation and termination live in the input.

Sources: d63804f2 ethosInterfaces, 5abf3be8 ethosInterfaces

## Imports
Pulling from an external source is explicit: source:Object pulls Object from the source's lib file; source:[Object Thing] pulls several; source:file.[Object Thing] pulls from a named file of the source. The source name resolves through a manifest written in datom; a name the manifest cannot resolve is an error; a bare path resolves locally. What exists is an import reference; there is no Import type. A file has no namespace inside it.

Sources: 2b34fafa ethosInterfaces

---

# Vision/ethosMonolith.md (revisions)

## Name (addition)
Its better name is ethos-zero: version zero, which bootstraps Ethos into the nexus trinity of Ethos, Nomos and Logos nexuses. Whether ethos-cc -- compiler-compiler -- is an accurate name is asked.

Sources: aa4c7747 ethosMonolith

## Shape (replaces the first sentence)
The monolith is written as a nexus from the start: the things it deals with are broken down, and the kinds -- the ways those things interact -- are isolated and properly named.

Sources: aa4c7747 ethosMonolith

---

# Vision/kinds.md (new)

## Kind is the word
In Ethos the word is kind. A kind is what a Rust trait becomes, one abstraction up: declaring a new kind declares a new trait on the Rust side and implies things Rust has no word for, still to be settled. Trait is set aside as acoustically ambiguous in speech.

Sources: b675f3d9 kinds, f426777b kinds

## A kind is named as a qualifier
A kind is named as a qualifier -- Runnable, Writable, Readable. Write is not a kind.

Sources: b675f3d9 kinds, f426777b kinds, 6863ef19 kinds

## Capability
A capability is an actual function a kind has: Runnable is the kind, run is one of its capabilities.

Sources: b675f3d9 kinds

## Interaction
An interaction is a kind's implementation on a type. An interaction uses the type itself; one that does not is no interaction of that type.

Sources: aa4c7747 kinds

## Concept
A concept is a type or a kind.

Sources: b675f3d9 kinds

## No generics, only kinds
In Ethos there are no generics, only kinds. What Rust writes as a generic parameter is a kind, and several kinds in one declaration adjust the emitted Rust.

Sources: b675f3d9 kinds, f426777b kinds

## Identity
As in Rust, a kind is identified by its name and the identity parts of its data: the kinds in its positions, written in the head -- Processable<[Clonable Sendable] Serializable>.

Sources: b675f3d9 kinds

## Kinds are declared explicitly
A kind is declared, never extracted from its interactions; recovering what a kind is and how many interactions it has from implementations would be complex.

Sources: f426777b kinds

## Creation is From
Creation is TryFrom or From, called by those names. There is no Create kind.

Sources: 2b34fafa kinds, aa4c7747 kinds

## Rust's own traits keep their names (a lean)
An existing Rust trait is referred to as Rust names it; a conversion table would incur a cost.

Sources: b675f3d9 kinds

## Capability forms
A capability is written as one of several structural forms, and Capability is a vector-represented enum of them. A capability's yields are always written in [], even a single yield: Head.[Concept] for one, Head.[ConceptOne ConceptTwo] for several. A mutable-self capability uses the exclamation mark: Head![Concept]. The Standard form carries inputs and outputs: Head.{[InputOne InputTwo] [OutputOne OutputTwo]}. A fallible yield is Result<A F>.

Sources: b675f3d9 structuralParsing, 04db2fd2 kinds

## One separator
There is only one separator after a head, so the separator options are mutually exclusive. The exclamation mark is reserved for mutable self as the most useful option.

Sources: 04db2fd2 kinds

## Finding a kind's declaration
A kind's declaration is found from the anatomy of a Rust trait in its most complex form; a struct is needed to fit it all, or a root enum to tell kinds of kinds apart. The struct form is for complex kinds.

Sources: b675f3d9 kinds, 04db2fd2 kinds

## Separate blocks for types and kinds
Ethos has a syntax for kinds and the concept of separate blocks for types and kinds in an interface file.

Sources: 04db2fd2 kinds

## The direction kinds
Embodiable and Textualizable are kinds borne by the actual type. Embody reads text into the bearer's Rust memory form and may fault. Textualize writes the bearer to text and cannot fault. The actual type also bears `⟦Delineated|Delineatable⟧`. There is no separate Embodied type; "embodied" is vocabulary for the bearer once in its Rust form. Kinds as verbs are not allowed; legacy Rust-imposed verbs (Write, Read) are tolerated until Ethos takes over completely.

Sources: 04db2fd2 kinds, 2ef42163 kinds

## Decomposable
Decomposable is a kind. A decomposable value decomposes into composable kinds; composing all parts in the right order regenerates the instance.

Sources: 04db2fd2 decomposable

---

# Vision/anatomy.md (new)

## The map before the code
An agent that writes code before it has a model of the world has already failed; catching a fake kind afterwards is too late. The work is building a map of what is being made -- its ontology, its anatomy, an object- and capability-oriented layout. The map is the Ethos interface file. Old code is at most inspiration for the map.

Sources: 2b34fafa anatomy, 15b67974 anatomy

## Ontology is designed before it is implemented
Every behaviour falls under a kind, which creates an ontology in code. Placeholder kinds for every function make no sensible ontology; an ontology is designed before it is implemented, and agents are trained and given a workflow for it. The universal nexus kinds are the basic ontology of an actor/dataflow software system.

Sources: e06e4c07 anatomy, ba906ae2 anatomy

## Types first
Types are thought through first; kinds are what types implement.

Sources: psyraw-6863ef19

## Costume kinds
A kind whose capabilities are ordinary functions pretending to be a kind misses the approach; this is a cornerstone of models' misunderstanding of the vision.

Sources: 2b34fafa anatomy

## The three-part machine
A machine agglomerates several types, creates one coherent type from them, and converts it to another type. That is one form of it -- the machine may be accumulating variables in a method's body -- and no single form is invested in.

Sources: 2b34fafa anatomy

## From over Into
Things are created from other things; nothing is harvested and then asked what it can be made into. Everything is demand-driven, so From is better than Into.

Sources: 2b34fafa anatomy

## Processing is for the effect
When an object enters a nexus, the point is the effect; the response comes as an effect of that. TryFrom is doubted as the way to think of processing; Apply is liked, uncertain, and a new terminology is needed.

Sources: f426777b anatomy

## Any type has an anatomy
Any type has an anatomy. Embodying a value consists in matching the expected type with the data, which is the anatomy of a type. A braced object has its own anatomy; almost all objects are structs at the root.

Sources: 04db2fd2 anatomy

---

# Vision/portion.md (new)

## Portion is the universal term
A portion is the universal term for a component of an object: a field in a struct, a variant in an enum, an element in a vector. Every component is a portion.

Sources: 04db2fd2 portion

## Enclosed and unenclosed
A portion is enclosed or unenclosed; opaque is a separate concern. A delimited string is an enclosed portion; a bare string is unenclosed. An opened struct has its outer delimiters implied.

Sources: 04db2fd2 portion

## Portion is an enum
Portion is an enum whose variants are Headed, Enclosed, and Bare, among others. Headed is a variant that is also a type; its contained data is derived deterministically from the variant name to avoid the clumsiness of Headed.HeadedData.

Sources: 04db2fd2 portion

## Bare.Symbol
A bare portion is Bare.Symbol: Symbol is a specific type of qualified string.

Sources: 04db2fd2 portion

## The headed portion
A headed portion is a struct: a head (Symbol), a separator (Period, Exclamation, or Colon), and a body that is another portion. Heads may be daisy-chained: x.y.z.w, with different separators.

Sources: 04db2fd2 anatomy, 04db2fd2 portion

## Non-opaque enclosed portions
A non-opaque enclosed portion holds a vector of possible inner portions: an unknown number of portions inside.

Sources: 04db2fd2 portion

## Opaque portions
An opaque portion has no containing portions: its content is opaque.

Sources: 04db2fd2 portion

## Portions inside portions
Portions exist inside portions. The recursive dependency this introduces is accepted.

Sources: 04db2fd2 portion

## Extent
Extent sits once on Portion, not on each variant.

Sources: 04db2fd2 portion

## Portion carries its anatomy
Form and Anatomy are not two types; the Portion itself carries both its structural form and its anatomy.

Sources: 04db2fd2 portion

---

# Vision/spokenVocabulary.md (new)

## A spoken vocabulary for software engineering
Programming was never done in speech. A spoken vocabulary for software engineering is being created -- a way to speak it at a higher, more correct layer of abstraction; it may be called logic engineering.

Sources: aa4c7747 spokenVocabulary, f426777b spokenVocabulary

---

# Vision/rustConventions.md (new)

## Tuples
There is no tuple in the code we design; where a standard trait or a dependency requires one, it is allowed at that contact point only.

Sources: aa4c7747 rustConventions

---

# Round 4 statements superseded

1. **Capability forms / SingleYield**: round 4 had "SingleYield.{Name Concept}, written Head.Concept". Superseded: yields are always written in [], even a single yield (04db2fd2 ruling). Round 5 writes Head.[Concept].

2. **Result and struct form**: round 4 did not address Result or the struct-form ruling. Round 5 adds: a fallible yield is Result<A F>; the struct form is for complex kinds.

3. **protos.md marked "(new)"**: round 4 marked protos as a new file. Corrected: Vision/protos.md already exists with a Direction section (commit 10a2eb054). Round 5 marks it "(additions)" with Direction as a revision.

4. **"Not stated (unruled)" in datom Syntax**: round 4 carried "Not stated (unruled): key/value resolving by position in a map (ac1e9ec8/3, 'considering'); whether a Head is always a variant (ac1e9ec8/5, a question)." Both are now ruled and landed in Vision/datom.md. Removed.

5. **Forms of a value**: round 4 had "A value has a real form, a signal form and a textual form. Realize reads the textual form into the real form; Textualize writes it back." Revised: "real" becomes "embodied"; "Realize" becomes "Embody"; the Embody/Textualize sentence removed (it restates Direction).

6. **"A Head is always a variant" unruled note**: round 4 noted this as unruled. It is ruled and landed. Note removed.

7. **Direction kinds**: round 4 did not address the direction kinds. The psyche has since ruled: the actual type bears both Embodiable and Textualizable; there is no separate Embodied type. "Embodied" is vocabulary for the bearer once in its Rust form. The Textual kind name is gone.

---

# Graduation and Intent questions

Carried from round 4:
- "Logic planes" (protos): Intent?
- "easy cognition is the first safe bet" (2b34fafa/1): a principle worth Intent, or a monolith working decision (discard)?
- psyche-raw/Intent/mandatoryTraits.md carries a psyche-approved wording; does it enter Intent/mandatoryTraits.md as it stands?

New:
- The Standard capability form (Head.{[inputs] [outputs]}) from the handwritten page uses a struct; the psyche later said "the struct is for complex kinds." Does the Standard form survive as a valid capability form, or is it superseded?
- Decomposable: the psyche explored an alternative to decompose/compose ("finding the keyframes," positions as line/column or rope theory). Is Decomposable settled as the kind name, or still being reconsidered?
- The psyche suggested a content-addressed hash on normalized Text for cached reading, and named this "the first use for a datom nexus." Is this vision or a deferred working plan?

# Tensions (carried from round 4)
- ethos-cc: asked as a name by the psyche, never answered.
- Effect verb: Apply liked, uncertain; "we need a new terminology."
- The word for a kind's declaration itself (still "trait declaration" in operational use).

---

# Discards this round

## Carried from round 4 (the living's ruling asked)
- aa4c7747/6 "not MVP sounding anymore" -- MVP scope decision.
- 2b34fafa/1 "easy cognition is the first safe bet" -- unless graduated (above).
- 5abf3be8/2, the working-plan clauses ("not now ... for now we could just ...") -- working plan; the stream-as-fourth-kind words are kept.
- aa4c7747-18 "And so we need to define what the trait syntax for Ethos is" -- task.
- 2b34fafa-30, the clause "Do a research in this" -- instruction.
- b675f3d9-9, the instruction clauses ("So start by looking at ...") -- the design content is kept in "Finding a kind's declaration."
- 2b34fafa-29 "we still need to establish the protocol ..." -- task.
- a5587095/11 "the intent is good" -- approval.
- a5587095/7 "Lets flesh it out in detail with examples" -- instruction.
- 6863ef19/1, the instruction clause "lets look at an update to the skills ..." -- instruction.
- ac1e9ec8/5 "Is there a scenario in which a Head. isnt a variant?" -- a question; now ruled and landed.
- aa4c7747/8 "I approve your trait implementation checking mechanism." -- approval that carries the ruling; proposed ARCHIVED (the only record of the mechanism), not destroyed.

## New from 04db2fd2 (impurities, dissected)
- **artifacts.md** (both entries): "No subtype-of-reports directories; subflows need a skill ..." and "two things come out of this work ..." -- working instructions about file management and task planning. Neither carries vision.
- **overtalking.md** (both entries): "Stop making file reports; talk here ..." and "holding comment rule goes in psyche-interraction only" -- conduct and process instructions, not vision.
- **softwareAnatomySkill.md** (both entries): "two things will come out of the work ..." and "how to work out the anatomy of a nexus" -- task planning; the vision content (anatomy, ontology) is captured in the anatomy statements.
- **kinds.md** "extend our example to specify all of protos ..." -- task instruction.
- **kinds.md** "Prospect<Datomic>.Text is quackery; types and kinds are missing" -- correction of agent work.
- **kinds.md** "what does the rust side look like? ... we need to draft a syntax for kind to type association" -- question and task.
- **kinds.md** "Youve given up on ethos syntax now ..." -- correction of agent work; the vision content (separate blocks) is captured in the kinds statement "Separate blocks for types and kinds."
- **portion.md** "represent everything again. what is your suggestion por portion? span?" -- question / suggestion request.
- **psycheLogging.md** "we have psyche logging spread across more than one skill now?" -- question.
- **rollingDistillation.md** "design and psyche-distillation skill edit is good" -- approval.

---

# Borderline -- parent decides

These may be vision (designing model behavior is vision) or may be working instructions. A proposed wording is offered for each; the parent decides whether to include them in the proposal to the living.

## Psyche logging: relevant bits only
Proposed destination: Vision/distillation.md (addition)

A vision entry includes only the psyche's words relevant to that entry, with triple-dot notation for omitted stretches; the full text is in the transcript.

Sources: 04db2fd2 psycheLogging

## Psyche logging: no timestamps
Proposed destination: Vision/distillation.md (addition)

A vision entry carries no timestamp; the flow directory implies the session.

Sources: 04db2fd2 psycheLogging

## Rolling distillation
Proposed destination: Vision/distillation.md (addition)

Distillation is proposed as the work proceeds: agents propose distilling accumulated vision at every second or third encounter, so raw vision stays clean and current rather than piling up stale or contradictory.

Sources: 04db2fd2 rollingDistillation

---

## Sources
- flows/acbb6006/reports/distillProposalRound4.md (round 4 base)
- flows/04db2fd2/vision/*.md (17 files)
- flows/2ef42163/vision/kinds.md (embody ruling)
- flows/b675f3d9/vision/*.md (style and structural parsing rulings)
- flows/ac1e9ec8/vision/*.md (datom syntax and distillation rulings)
- Vision/protos.md, Vision/datom.md, Vision/ethos.md, Vision/ethosMonolith.md (landed)
