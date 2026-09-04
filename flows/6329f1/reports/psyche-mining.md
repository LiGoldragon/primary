# Psyche mining — datom, ethos, protos, orchestrate, and related subjects

Flow 6329f1, 2026-09-04.

---

## 1. Datom

### Distilled Vision (Vision/datom.md)

The full distilled Vision/datom.md covers: Name, Nature, Repository and migration, The interface shape, De/serialization, Relation to Ethos, Syntax, and Meaning. It is the current authoritative statement. Key passages verbatim:

**Name:**

> Datom is the psyche's own coinage for the new data notation, the successor to NOTA and to the rejected name Dotos. The name was chosen for its energetic power and to echo what the notation is: data, strictly typed, super dense, no field names.

**Nature:**

> Datom is the most advanced textual data format in the world. It carries data, strictly typed, and its whole work is serialization and deserialization: carrying data between text and typed form. Datom is signal's form at the edge: our components speak signal, and datom lets text-based systems, LLMs and every existing editor, read and write it. Datom is a kind, not a type, since it has no definite shape; the kind is Datomic. Generating Rust is Ethos's duty, in today's division of labor. When Ethos becomes the full authoring language, with Rustlang as its assembly layer, Datom, the data dialect of the Protos family, may gain an inline place in authored Ethos, the way Rustlang composes data directly in code. That road is reached, or even floated, only with explicit context: how, when, and where data yields Rust, stated without ambiguity; until then the division stands as spoken.

**The interface shape:**

> A program's configuration surface is the datom's shape itself, as the ethos interface declares it: a data enum at the root whose variants are the main operations. [...] A Nexus reply is written as its heads down to its data, and only what carries data is written: an empty Locks observation is Observed.Locks.[], the Observed variant, its Locks variant, the empty vector; the layout of a nonempty payload is open.

**De/serialization:**

> Schema-driven and positional: the reader walks the expected type, writing is the exact reverse projection, and decoding lands directly in the typed Rust structs. A datom on the way in is a potential datom, untrusted until it matches its type; on the way out it is a datom. All naming and self-description live in the type; the text carries only the data.

**Syntax (key excerpts):**

> Structure is the word for every unit of the text: enclosed when it stands between its delimiters, unenclosed when bare. A headed structure is a head, a separator and a body; the dot is the separator, written right after the head, and it opens the body's delimiter. A head is a symbol, a qualified string [...] In datom a head is always a variant, so it is capitalized. [...] A brace structure is a struct and a bracket structure is a vector. [...] Guillemets delimit a map; inside, key and value are separated by a space, resolving by position. [...] An integer is written as bare decimal, 0, 42, -42: ASCII digits, no leading plus, no leading zero except 0 itself. A single semicolon opens a comment. Canonical text leaves a space inside every bracket and brace delimiter, at both ends [...] and never inside curly quotes, where a space is content.

**Meaning:**

> Meaning is the structured string: text that carries, besides its words, the emphasis and the other structural aspects a plain string simply lacks [...] Parentheses are a major symbol of cognition, and in datom they have one duty: the parenthesis pair is the Meaning delimiter, as the curly quotes are the plain string's. [...] Meaning is datom. Strings are strings and Meaning is Meaning: a position of type String expects a plain string and nothing else, and a position of type Meaning expects a Meaning. Meaning is postponed so that a working syntax lands as soon as possible [...] The name Meaning smells of a verb; it stands provisionally and is reopened together with the type.

---

### Raw records, newest first

**2026-09-04, flow ad19b1** — `flows/ad19b1/vision/archive-meaning.md`

> there is no more meaninigOrString. strings are strings, and meaning is meaning

-- psyche, typed.

> Meaning is datom

-- psyche, typed.

**2026-09-04, flow 1c282d** — `flows/1c282d/vision/vocabulary.md`

> structure

-- psyche, typed. (Answering: Portion vs. Structure — should it become Structure?)

**2026-09-04, flow ad19b1** — `flows/ad19b1/vision/ethos.md`

> space the delimiters and the inner content.

-- psyche, typed. (On brackets written tight.)

> it should be CAPACITY. and use a key-value map delimiter

-- psyche, typed. (On associated constants.)

**2026-09-03, flow e4a40e** — `flows/e4a40e/vision/archive-datom.md`

> Well, that's not quite true, although ethos could depend on datom [STT: datum], but for quite different reasons. Ethos could be read as datom [STT: datum] in a certain pass, which could be interesting, but I'm not sure that that's even possible given the context and actualization of parsing involved in parsing ethos. I don't think that's a good subject for now.

-- psyche, STT.

> No, not quite. A head has to qualify also in other ways than just bare text. Bare text is true, but it's not specific enough. There's a certain subset of text that qualifies as a head.

-- psyche, STT.

> a braced [STT: brazed] structure in Datom [STT: Datum] is a struct. It's just that if it has a head, then it's a variant that carries data, which is a struct.

-- psyche, STT.

> your example is good, but you should also make it clear that the whole struct itself is also a structure.

-- psyche, STT.

**2026-09-03, flow e4a40e** — `flows/e4a40e/vision/archive-vocabulary.md`

> Absolutely not. "Block" is not any of the terms that we have been considering to talk about this thing, so no, no, no, no, no, no, no, no. On the block, absolutely not. It's an ugly term.

-- psyche, STT.

**2026-09-02, flow 62022e8f** — `flows/62022e8f/vision/archive-datomSyntax.md`

> The example with the compact version number I had just copied, so it was not intentional for me to not have spaces there between the delimiters and the content. It will be canonical, but it is not load-bearing or considered good style to leave a space between the delimiters and the content, except for the strings, of course. The curly quotes, there it'll be bad because a space in that would be load-bearing, so it actually even disqualifies just on that fact.

-- psyche, STT.

**2026-09-01, flow 995a164e** — `flows/995a164e/vision/archive-datomSyntax.md`

> datom is not preceded by a Datom. but one could use a comment to indicate it is datom.

-- psyche, typed (artifact comment).

**2026-08-29, flow e8c4cc61** — `flows/e8c4cc61/vision/archive-datomSyntax.md`

> I guess a single ; is for comments now. semi-colon isnt load bearing anymore so that works.

-- psyche, typed.

> This is not load-bearing on a parser, but just for ease of reading, I would like it whenever there's a delimiter in proto syntax, not the curly quotes, not for strings, but for the brackets or maybe just the brackets. I think it would be good style to leave a space between the delimiter and the next thing inside of it, both at the beginning and the end. It's easier to see the separation there.

-- psyche, STT.

**2026-08-28, flow 04db2fd2** — `flows/04db2fd2/vision/anatomy.md`

> decomposing a datum [STT: Datom] consists in the capability itself when it's implemented will match the expected kind, sorry, the expected type of datum [STT: Datom] with this data graph, which is the anatomy of a type. So, any type has an anatomy. ... a datum [STT: Datom] is a kind, not a type.

-- psyche, STT.

> the headed object has the anatomy of the head, the separator, and the body [...] The body is an object. The head is just a string [...] the separator is like a period or an exclamation mark or whatever. And this is going to be a set, an enum, an actual enum. So I'm describing a struct [...] We aren't closed off to the daisy chain of heads [...] it could be like different separators too.

-- psyche, STT.

> a braced object has its own anatomy [...] almost all objects will be structs at the root. ... a lot of what I'm talking about is Protos machinery, because it's universally applicable to all the dialects.

-- psyche, STT.

> delineation is protos. so is anatomy [...] {} = nb of components is anatomical whereas for [] that isnt the case

-- psyche, typed.

> also false. for protos, a Head is just a Head, nothing more. Anatomy, not interpretation.

-- psyche, typed.

> pure anatomy is only structural recognition of delineations, *nothing more*

-- psyche, typed.

**2026-08-28, flow 04db2fd2** — `flows/04db2fd2/vision/delimiters.md`

> this is false; you are talking about guillements, and what you showed is a double angle bracket pair

> also false. curved quotes are an asymetric pair of characters

> that's not univeral yet. so not protos. what we can say is it's content-opaque, so all characters it contains are ignored, until the closing unbalanced closing parenthesis.

-- psyche, typed.

**2026-08-28, flow 04db2fd2** — `flows/04db2fd2/vision/textualTypes.md`

> I like "Text taken as a would-be T: Prospective<T>" which gives us Prospective<Datom> although Im unsure if Datom is type or kind, probably kind, since it doesnt have a definite shape yet

-- psyche, typed.

> Re datom kind: Datomic

-- psyche, typed.

**2026-08-28, flow 04db2fd2** — `flows/04db2fd2/vision/directionAsymmetry.md`

> exactly. this can go straight into distilled vision

-- psyche, typed. (Approving: in is a prospective datom untrusted until matched; out is a datom; Realize faults, Textualize does not; spans found inbound, computed outbound; multi-pass.)

**2026-08-28, flow 04db2fd2** — `flows/04db2fd2/vision/archive-datomMaps.md`

> Vision/datom.md still says parentheses-default strings and [key.value ...] maps; your 2026-08-26 rulings supersede both ... lets get that fixed, we use guillemets for maps now, with key and value separated by a space

-- psyche, STT.

**2026-08-27, flow 01a04339** — `flows/01a04339/vision/archive-datom.md`

> Observed.Locks.[]
>
> good enough for now.

-- psyche, typed, 2026-08-27T12:56.

**2026-08-27, flow 4d5fc7da** — `flows/4d5fc7da/vision/datom.md`

> just remember datom doesnt support omittable fields yet.

-- psyche, typed.

**2026-08-26, flow ac1e9ec8** — `flows/ac1e9ec8/vision/datomSyntax.md`

> If a position expects a map, the data will be [ k.v ... ], no Map.

-- psyche, typed.

> Im considering making key/values resolve by position in a map [...] that looks cleaner and makes the Head. always a variant; lower cognitive cost

-- psyche, typed.

> let use the guillemets.

-- psyche, typed. (Ruling: guillemets delimit a map.)

**2026-08-26, flow ac1e9ec8** — `flows/ac1e9ec8/vision/datomSyntax.md` (corrections)

> dont be so apologetic. Datom is the most advanced textual data format in the world.

> I said no negatives. This is useless. Do we say "JSON doesnt support generics"?

> re: bare strings: make sure it's clear that a string is a string only in a position where the type defines a string.

> curly quotes [...] should be positioned as the default string delimiter. the vision is that parenthesis will become the delimiter for structured strings, still to be designed. So let's switch it all to curly quotes first, with parenthesis reserved for structured strings, which we currently designate as Meaning

> no, this is false. all our components speak signal, not datom; datom is only used at the edge to let text-based systems (LLMs and all existing editors) understand signal.

-- psyche, typed.

**2026-08-26, flow ac1e9ec8** — `flows/ac1e9ec8/vision/datomIsData.md`

> you've mixed up datom with ethos. datom is data

-- psyche, typed.

**2026-08-26, flow 01a03eda** — `flows/01a03eda/vision/archive-datomInteger.md`

Integer syntax proposal (canonical bare decimal, 0 42 -42, ASCII digits, no leading +, no leading zero except 0):

> 1. yes

-- psyche, typed, 2026-08-26.

**2026-08-25, flow 01a038b5** — `flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md`

> I want to migrate curriculum stack to datom instead of dotos

-- psyche, typed, 2026-08-25.

**2026-08-23, flow 68512643** — `flows/68512643/vision/negatives.md`

(Long dictation on negatives in distillation; see the file for the full verbatim text. Key ruling:)

> So the line it's dangerous is true in that context [...] if we do either get there or if we float the idea of how we would get there, it would be very explicitly [...] contextualize so that there's no ambiguity as to how and when and where data may or may not generate rust.

-- psyche, dictated, 2026-08-23.

**2026-08-22, flow 01a02a34** — `flows/01a02a34/vision/archive-datum.md`

> And you're saying dotos, but like that's the old syntax, which is being replaced by datum, which is, you know, has the same concept.

> And use datom instead of dotos.

-- psyche, typed, 2026-08-22.

**2026-08-11, flow a5587095** — `flows/a5587095/vision/archive-datomSyntax.md`

> On parenthesis: It would be strange for parenthesis to be unused in datom. They are a major symbol of cognition.

-- psyche, typed, 2026-08-11.

> parentheses delimit the structured string; one string type, two variants [...] () would be the delimiter

-- psyche, typed, 2026-08-11.

> Yes, map would use .[ since a map is conceptually a list of key/values

-- psyche, typed, 2026-08-11. (Superseded 2026-08-26 by guillemets.)

**2026-08-11, vision-raw** — `vision-raw/archive-datomSyntax.md`

> datom doesnt do generics, it only carries data, like json (but strictly typed of course)

-- psyche, typed, 2026-08-11.

> So we can just fix datum [Datom] first because we need that. We need the syntax to start being consistent.

-- psyche, dictated, 2026-08-11.

**2026-08-10, vision-raw** — `vision-raw/archive-threeStacks.md`

> we don't need to worry about the old repo. We're just going to move forward and migrate everything to datum [Datom].

-- psyche, dictated, 2026-08-11.

**2026-08-06, flow 5abf3be8** — `flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md`

> you mean, it opens a delimiter. everything is data

-- psyche, typed, 2026-08-06.

**2026-08-06, flow 5abf3be8** — `flows/5abf3be8/vision/chainedNamesScrapped.md`

> no, that is scrapped

-- psyche, typed, 2026-08-06. (Multi-segment dotted name chains killed.)

---

## 2. Ethos and Ethos-zero

### Distilled Vision (Vision/ethos.md)

Full file covers: What Ethos is, Why Ethos, Generation, Non-repetition, Self-description, Horizon, Kind, Naming, Identity. Key passages:

**What Ethos is:**

> Ethos is the schema language. Of the two main syntaxes most agents will face, Ethos specifies the types and Datom fills them with data.

**Why Ethos:**

> Existing text data formats and existing programming languages both fail. Rust is the new assembly, read in full by no one; Ethos is the concise, dense, cognitively concentrated language for writing code with AI agents — easy to read and write, showing the interfaces: the main types and the main traits. Behavior falls under traits, which creates an ontology in code.

**Generation:**

> Ethos generates the Rust. Rust generated from ethos is committed, so ordinary tooling — language servers — works normally; a freshness mechanism is deliberately left open.

**Non-repetition:**

> Any repetition in ethos syntax is an implementation failure. Ethos aims to be the most terse, non-repetitive syntax ever made.

**Self-description:**

> A datom object's basic CLI help emits the Ethos that describes its anatomy. [...] it trains agents to use things properly, and it shows where the design is lacking.

**Horizon:**

> Ethos will eventually replace everything, Rustlang becoming its assembly layer. Designs are chosen for that horizon; what it enables — generator emission among it — comes in its time.

**Kind:**

> Kind is the word for the bearer of capabilities: something that can run is a runner, Runnable is its kind, and run is its capability, a function the kind has. Trait is set aside as acoustically ambiguous. In ethos there are no generics, only kinds. Declaring a new kind declares a new trait in the Rust world and might imply more in the ethos world.

**Naming:**

> Kinds are qualifier-named: Runnable, Textualizable, Structural, Embodied. Run is not a kind. The verbs Rust imposes, Write and Read among them, are tolerated as legacy, for cognitive ease while Rust and ethos code are switched between so often; once ethos is the authored language that debt is removed.

**Identity:**

> A kind is identified as a Rust trait is, by its name and its constraints, written as one head: Processable<[Clonable Sendable] Serializable>. A constraint is a kind, or a bracket of kinds: what Rust writes as a generic parameter with its bounds, ethos writes as the bounds alone, since in ethos there are no generics, only kinds [...] Two heads that differ in a constraint are two kinds. Which constraints belong to the identity is not a decision to make: the ethos compiles to Rust, and what identifies the trait identifies the kind. [...] Angle brackets hold the constraints; they are a protos delimiter, recycled from Rust as Result and Self are.

### Distilled Vision (Vision/ethosMonolith.md)

**Origin:**

> All our systems will be Nexuses, and the correct three-nexus ethos stack is the desired stack — but it is too complex to go for directly [...] The monolith is the short-term path that brings ethos into production: the earlier stack's code is kept, left in place, frozen, and new repositories carry a simplified path from Ethos straight to Rust.

**Name:**

> First named ethos-rust, the schema-rust analogue; then renamed ethos-monolith: it has no nomos and no logos component and goes straight to Rust — a monolith.

**Shape:**

> The monolith will itself be a Nexus. Nexus by itself names our specifically designed daemon — distinct from Nexus Core, the runtime engine — and executables are named component-nexus.

### Raw records, newest first

**2026-09-04, flow ad19b1** — `flows/ad19b1/vision/archive-kinds.md`

> I said rust not rest. what a shitshow! you can't even hear what Im saying properly!

> no, thats not how rust trait is identified. we spent hours over this today.

> position? is that what rust calls those? thats a fuzzy way to describe them.

> no, not at all. it is narrower than ethos, since it is an ethos concept. so it goes in ethos.

-- psyche, typed. (Kinds go in Vision/ethos.md, not Vision/kinds.md; kind is an ethos concept.)

**2026-09-04, flow ad19b1** — `flows/ad19b1/vision/ethos.md`

> it should be CAPACITY. and use a key-value map delimiter

-- psyche, typed. (Associated constants are upper case, in the map delimiter.)

> space the delimiters and the inner content.

-- psyche, typed.

**2026-09-03, flow e4a40e** — `flows/e4a40e/vision/archive-kinds.md`

> Yes, obviously those would be two kinds [...] Why is that ambiguous? I'm really curious.

-- psyche, STT. (Two heads differing in a required kind are two kinds.)

> You don't have to decide which constraints are not part of an identifier. What identifies a trait in Rust is what identifies a kind in the ethos, because we're compiling the Rust [...] There's no decision involved here, and we're not going to rewrite the Rust compiler.

-- psyche, STT.

**2026-09-03, flow 4decf7** — `flows/4decf7/vision/archive-kinds.md`

> kinds are qualifier-named

-- psyche, typed.

**2026-09-02, flow 62022e8f** — `flows/62022e8f/vision/kinds.md`

> I think naming the kinds is really tricky [...] Prospective [STT: perspective]. I want to switch to potential

> Potential and actualize, universally, layer to layer; Embodied is the bound; Corporal is kept for the layer

> the structural capability [...] would be on text and the conceive capability would be on structure and the incorporate capability would be on concept.

-- psyche, STT.

**2026-09-02, flow 62022e8f** — `flows/62022e8f/vision/ethosTypes.md`

> I just realized I never addressed KV specification in ethos. SomeMap.<< NameType ValueType>>

-- psyche, typed.

**2026-09-01, flow 995a164e** — `flows/995a164e/vision/ethosTypes.md`

> this is wrong. It ethos not datom. [...] an Ethos meta type which is followed by an implied (delimit-less) vector of explicit ethos objects

-- psyche, typed.

**2026-08-29, flow e8c4cc61** — `flows/e8c4cc61/vision/ethosFileAnatomy.md`

(Contains the psyche's handwritten page: Ethos File Anatomy. See the full file for the image transcription.)

> the outer {} should be omitted and always implied in any ethos file

-- psyche, typed.

> if we want the "sweet" ethos file syntax, we need a corresponding type

-- psyche, typed.

**2026-08-29, flow e8c4cc61** — `flows/e8c4cc61/vision/kinds.md`

> that doesnt work. The kind declaration must use a kind, not a type. do we need a Type kind?

> TryInto just doesnt sound like a kind. lets go with Prospective<Sized>

> ok, `:` for no self stands

> I dont think there is any Embodiable. It's just Embodied, which is an alias of Sized. Would that work?

> your trait syntax doesnt work. Looks like we need to redesign the kind syntax. We could add a second syntax for a more complex kind which opens with {

-- psyche, typed.

**2026-08-28, flow 2ef42163** — `flows/2ef42163/vision/ethos.md`

> as Result and Self showed, rust syntax is the target, so whenever we need to point at a principle in rust, we usually will recycle the same syntax

-- psyche, typed.

**2026-08-28, flow 2ef42163** — `flows/2ef42163/vision/kinds.md`

> real/realize is changed. debate was on embody/embodied or forge/forged

> embody.

> text isn't textual; the embodied type is. so this brings back the debate of textualizable being a better fit

> you still don't get it. Text is embodiable, and the Embodied is Textualizable

> it would be delineatable right?

> Actually, I don't even know if embodied is anything at all because when you run the capability of an embodiable kind, then what you get is self. Because now it's embodied.

> bearer? you mean Self?

> the type we're passing into the embody function is not actually what we're trying to get. So I guess you would need another kind. Like you said, embodied, which is the actual embodied type, the final Rust language type would implement embodied

-- psyche, typed and STT.

**2026-08-27, flow b675f3d9** — `flows/b675f3d9/vision/kinds.md`

> 1. qualifier. Write isnt a kind. we say kind now, not trait. [...] in Ethos there are no generics, only kinds.

> 4. capability will refer to the actual functions a kind has (Runnable would be the Kind, run would be a capability)

> important: in rust, a trait is identified by its name *and* constraints. How would we want to mirror that?

> I prefer Processable<[Clonable Sendable]  Serializable>

-- psyche, typed.

**2026-08-27, flow b675f3d9** — `flows/b675f3d9/vision/ethosMonolith.md`

> 5. Then we'll make it a nexus. Everything will be a nexus; the consistency will create reliability and increase the quality and clarity

-- psyche, typed.

**2026-08-25, flow aa4c7747** — `flows/aa4c7747/vision/ethosMonolith.md`

> Ethos zero would be a better name. [...] Ethos zero. Yeah, Ethos zero. And that would be a better name.

> And I think that we need to just go straight for a nexus. So it has to be written as a nexus. [...] we need to isolate the traits, which is the ways in which these things [...] interact, and put the proper names on them.

> right, so we need ethos-monolith to bootstrap it. We should call it ethos-cc (compiler compiler); would that be an accurate name for it? And ethos-zero because its version zero which will bootstrap ethos in the nexus trinity stack (with nomos and logos nexuses)

-- psyche, dictated and typed.

**2026-08-24, flow aa4c7747** — `flows/aa4c7747/vision/ethos.md`

> ethos is essentially meant to give us [...] a language that allows us to, in one swoop, write down our mental model of the machine and write code [...] something like Rust or even JavaScript is full of noise. It's like maybe more than half of the code is noise

-- psyche, dictated.

**2026-08-24, flow aa4c7747** — `flows/aa4c7747/vision/ethosTraitSyntax.md`

> And so we need to define what the trait syntax for Ethos is and use the Ethos zero nexus as a first example.

> When I said traits I just meant trait declaration. Implementation would be a big job [...] thats not MVP sounding anymore.

> this is quackery. Nonsense. There's no need for this. If we want TryFrom/From, then that's what we'll call it.

-- psyche, typed.

**2026-08-24, flow aa4c7747** — `flows/aa4c7747/vision/interactions.md`

> interactions are good, because I think that describes it well, what it is really conceptually.

> they're interactions use the type itself in almost all cases. Well, really in all cases, because if it's not using the type itself, then is it really an interaction of that type?

-- psyche, dictated.

**2026-08-24, flow aa4c7747** — `flows/aa4c7747/vision/tuples.md`

> tuple: no tuple in the code we design: if some parts require it (standard traits, dependencies), then we allow it at that contact point only

-- psyche, typed.

**2026-08-22, flow 01a02a34** — `flows/01a02a34/vision/archive-ethos.md`

> schema, like, which is basically what Ethos is. It's a schema language.

> It would also be great if we can use ethos instead of schema but ethos-monolith might not be ready to use.

-- psyche, typed.

**2026-08-20, flow 2b34fafa** — `flows/2b34fafa/vision/ethosSourceFiles.md`

> for the monolith thats good enough. easy cognition is the first safe bet.

> document sucks. I dont understand your question. What's wrong with File?

-- psyche, typed. (One file, one Rust module for the monolith. The unit is File.)

**2026-08-20, flow 2b34fafa** — `flows/2b34fafa/vision/ethosNamespaces.md`

> this concept is ridiculous in ethos. we're building the foundation and youre talking about wallpaper

-- psyche, typed. (No namespace inside a file.)

**2026-08-11, flow a5587095** — `flows/a5587095/vision/rustComponentArchitecture.md`

> I even want to make the broad statement that I want *all* method calls in our rust code to be part of a trait, since I need to understand my systems through traits and main types, as I cannot possibly read all the code, and rust is the new assembly language

-- psyche, typed, 2026-08-11.

**2026-08-01, vision-raw** — `vision-raw/archive-ethosNonRepetitionLaw.md`

> we wouldnt repeat Ord; any such repition in ethos syntax is an implementation failure. ethos will be the most terse non-repetitive syntax ever made

-- psyche, 2026-08-01.

### Intent (Intent/mandatoryTraits.md)

> Every method call in our Rust code lives under a trait, because traits are the comprehension surface — the layer where concepts become visible and implementations are constrained to think within them. Rust is the new assembly language: no serious engineer reads all the assembly, and the same is happening to Rust. Traits and main types are what the psyche reads; everything else is implementation detail that Ethos will eventually generate.

-- psyche-approved, 2026-08-13.

---

## 3. Protos

### Distilled Vision (Vision/protos.md)

> Text arrives as a prospective value and leaves as a value. Realize reads the textual form into the real form and may fault: the text is prospective until it matches its anatomy. Textualize writes the real form into the textual form and cannot fault: a real value is already whole. Spans are found on the way in and computed on the way out. Each direction is several passes.

### Intent (Intent/protosParsing.md)

> Protos parsing always happens inside a context, and only the current context gives shapes their meaning: it defines which shapes can appear next and which shape completes it. A met shape announces a type, and that type's context takes over completely until its completing shape; then the parent context resumes exactly where it left off. Reading and writing are one walk in two directions — text lands in typed values, and typed values project back into the same text.

### Intent (Intent/data.md)

> Everything is data. Code is data: a type is declared with code, so a type is data; a trait is data; an impl is data. [...] Protolanguages make this obvious by being a data notation before they are anything else.

### Raw records, newest first

**2026-09-04, flow 1c282d** — `flows/1c282d/vision/protosizable.md`

> ethos isnt datom-expressible. the form is protos. I think protosic is the right kind. `type.protosize() -> protoform` - does that make sense.

> protosizable!

-- psyche, typed. (Kind name corrected to Protosizable.)

> ethos:Concept.[ Protosizable]

-- psyche, typed. (The ethos Concept type bears the Protosizable kind.)

> looks like Structure is really Protoform.

-- psyche, typed.

**2026-09-03, flow e4a40e** — `flows/e4a40e/vision/protos.md`

> it's wrong right off the bat because it's showing the ethos, and you're saying this is going into protos. Protos is only about structure. It has nothing to do with `struct` and `vector`, and it only understands form, so it's only a very abstract structure, like the syntactic structure. It wouldn't know what anything is.
>
> You have to understand that we're talking about the anatomy of the text. This is a headed, bracketed component, or whatever we're designing to call it. Nowadays, structure and nothing else, it wouldn't know. We wouldn't use an ethos syntax for an example because it would be confusing later on.
>
> Whatever you're showing me that's ethos needs to go in an ethos vision distillation. If you want to do protos, it has to be very much universal, explaining this: the textual structure, the approach to how we structure things textually, with the delimiters, the head, the capitalization, and the recursive structure, like a structure contains another one and so on, some very, very high-level, non-dialect-specific stuff.

-- psyche, STT.

**2026-09-01, flow 995a164e** — `flows/995a164e/vision/data.md`

> everything is data. you have been trained by idiots. Code is data. a type is declared with code, so a type is data. a trait is data. an impl is data. *everything* is data, but protolanguages make it more obvious.

-- psyche, typed.

**2026-08-29, flow e8c4cc61** — `flows/e8c4cc61/vision/protos.md`

> your Structure is a better Portion (better name anyway)

> and Delineatable is better expressed as Structural.

-- psyche, typed.

**2026-08-14, flow ba906ae2** — `flows/ba906ae2/vision/protosIsTheSharedStyle.md`

> because datom doesnt take part in the multi pass engine which ethos->nomos->logos->rust is slated to become. but youre right; beside sounds like its not a protos dialect. it *is* a protos dialect, but not part of the future ethos/nomos/logos rust-generation engine

-- psyche, typed, 2026-08-14.

**2026-08-14, flow ba906ae2** — `flows/ba906ae2/vision/encodedFormIsTheCode.md`

> textualize is approved.

-- psyche, typed, 2026-08-14. (protos::Textualize ruled.)

**2026-08-13, vision-raw** — `vision-raw/traitsAsCapabilities.md`

> if the trait is transcodable, yes, and if it lives in the protos module, then that's not ambiguous. Because if we fully qualify the name, it's self-describing that it's transcodable into protos.

(2026-08-14 annotation: "transcodable" superseded by the code/encoded drop; successor pair is protos::Realize / protos::Textualize.)

-- psyche, dictated, 2026-08-13.

**2026-08-12, flow a5587095** — `flows/a5587095/vision/protosIsTheSharedStyle.md`

> the more complex trait will be a vector of ProtosShape's [...] when the structure dictates the outer type, for example in ethos when X.{ means a struct, and Y.[ means an enum

> The type met implements its own context? Does that make sense? [...] ProtosShape was a trait. [...] implementing ProtosShape means creating a match on standard ProtosShape [...] Those ProtosShape are always the same

> because of recursion, the position of the parent context still needs to be kept, so that returning to the parent context resumes at the following position.

> ShapeDefined discriminates only — it yields the type, and the type implements its own parsing context; big implementations signal a missing logic plane — everything simple individually, the complexity in the totality

-- psyche, typed, 2026-08-12.

**2026-08-11, flow a5587095** — `flows/a5587095/vision/protosIsTheSharedStyle.md`

> protos is the name we give to the style which all our dialects share; hence why the final fully-decomposed engine with 3 daemons is the protos engine, with datom sort of sitting besides it, as it is only for pure, typed data

> no, there is always a parsing context. it doesnt suspend, it *changes*, but the underlying mechanism is always the same; Now, we are parsing in context X and can therefore expect A, B or C shapes of things, and Z would end that context, but meeting A would switch to the context which A entails. That has been the ruling principle of NOTA (datoms's ancestor) from day one. I want to extend it now to say it should always use trait.

> Lets flesh it out in detail with examples then we can make it intent. [...] Dont forget the parsing is also two-ways. [...] design pattern ruled: visuals, examples, and traits with main types.

-- psyche, typed, 2026-08-11.

---

## 4. Serialization / Deserialization — multi-pass, trait-based anatomy

### Raw records, newest first

**2026-09-02, flow 62022e8f** — `flows/62022e8f/vision/passes.md`

> the file comes in, and it's read as such. Then such-and-such capability is called on this object, which recursively calls such-and-such capability on all of its containing objects, sections, or structures, or shapes.

-- psyche, STT.

**2026-09-02, flow 62022e8f** — `flows/62022e8f/vision/layers.md`

> [the concept layer is the Datom and Ethos types of the settled chain?] yes

> Ethos would also have a Corporal layer, which is the layer that would then be used to yield the generated rust.

-- psyche, typed.

**2026-09-02, flow 62022e8f** — `flows/62022e8f/vision/concept.md`

> we have the conceptual form and the corporal form, and the corporal form is the final form.

> When a datom [STT: datum] comes in [...] the conceptual representation of that won't be the Rust [STT: rest] type itself that this is being cast into. It'll be a vector. [...] this is an enum, a variant of an enum with a variant name X and a payload of such and such, which is really just a reference to another concept.

> The concept is the anatomical layer of Protos, and also it's more than that. I'm not sure. I'm confusing myself now, and I'm not sure what I want yet.

> we have at least two passes, if not three [...] At one layer, which is the kind declaration layer, you have this very varying arity. This is, I guess you would say, conceptual. [...] You have the corporal side

-- psyche, STT.

**2026-08-29, flow e8c4cc61** — `flows/e8c4cc61/vision/prospective.md`

> for any prospective kind, so a prospective protos uses the capability prospect, which is to look forward

> we read before reading and find all of the anatomy [...] not specific. It's just an anatomical survey.

> And so that can be then passed on to a further capability, like in datom [STT: datum] or in ethos, you would have a prospective datom [STT: datum] or a prospective ethos.

> we don't quite know what type we're embodying into until later into the reading passes.

> So we're not scared to do multiple steps. The multiple steps create a mental model of the machinery, which enforces a correctness in the code that is millions of times more beneficial than the cost of doing these multiple passes

-- psyche, STT.

**2026-08-28, flow 04db2fd2** — `flows/04db2fd2/vision/multiPass.md`

> all objects will have a beginning and an end. Well, not intrinsically. [...] when we actually textualize, these can be computed.

> basically what we're doing is a multi-pass process. We're not interested in doing everything in a single pass, because it creates a whole bunch of [...] corner-cutting bad design.

-- psyche, STT.

**2026-08-28, flow 04db2fd2** — `flows/04db2fd2/vision/portion.md`

> instead of saying field [...] the concept is universal. [...] every object, so to speak, is a portion.

> if we say that this is an opened struct, meaning it doesn't have its outer delimiters [...] a bare string is essentially an open portion. It doesn't have the limiters [...] the limited string is a closed portion.

-- psyche, STT.

**2026-08-27, flow b675f3d9** — `flows/b675f3d9/vision/structuralParsing.md`

> the structural parsing can actually discern between structs of different size to differentiate between different types.

> <> is a real Protos delimiter of course. I'm surprised you have to ask

> again, you seem to have a hard time understanding that ethos parsing is always dependent on the current context

> this is false since it is context dependent. and the mere fact that something starts with a head could convey the type. and not every block starts with a head

-- psyche, typed and dictated, 2026-08-27.

---

## 5. Orchestrate

### Distilled Vision (Vision/orchestrate.md)

> Orchestrate is deployed unconditionally, in the home, for every user. Its meta binary is part of it; a deployment without meta-orchestrate is wrong.

> The orchestrate skill covers ordinary operations only; meta operations are outside it.

### Raw records, newest first

**2026-08-27, flow acbb6006** — `flows/acbb6006/vision/archive-nexus.md`

> the clients are not the nexus. for now, default clients are packaged with the nexus, so they should be separate crates (multi crate repo), in the form of a datom-converting cli for each socket

> in everyday speech, orchestrate-nexus will be called orchestrate, etc

-- psyche, typed, 2026-08-27.

**2026-08-26, flow 01a03eda** — `flows/01a03eda/vision/observe.md`

> Observe.Locks is best. If another kind of lock comes, then we can add it as such; Observe.ExpiredLocks, etc

-- psyche, typed, 2026-08-26. (Supersedes Locks.Current and Observe.CurrentLocks.)

**2026-08-26, flow 01a03eda** — `flows/01a03eda/vision/orchestrateRealization.md`

> actually, first mine the session designing datom; we have changed direction on the string delimiters. So youll have datom modified again. You can do all the work in parallel, and re-adapt orchestrate to the new datom once its done.

-- psyche, typed, 2026-08-26.

**2026-08-26, flow 01a03d6e** — `flows/01a03d6e/vision/ethosInterfaces.md`

> the interface has to be designed in a verb-oriented, an imperative approach

> When we're designing a signal interface, the input maybe should be even called commands or requests [...] to say request, first of all, is redundant, because this is a request by virtue of being in that slot. And it should be an imperative voice, right, as in list.

> observe is more universal, and reuse is good [...] the better design would be observe with a, observe is the root variant, and then it has [...] another enum

> that is obsolete nota/dotos format

-- psyche, typed, 2026-08-26.

**2026-08-26, flow 01a03d6e** — `flows/01a03d6e/vision/locks.md`

> I think it's better to think of the lock as the lock, and the lock returns like a certain structure which shows the paths.

> any lock must be released before its flow becomes idle [...] if through a transcription file, if it's possible to know that a flow is idle [...] then all of its locks are automatically forfeited by protocol.

> Better to think of it as a Lock than a PathLock

-- psyche, typed, 2026-08-26.

**2026-08-26, flow 01a03d6e** — `flows/01a03d6e/vision/archive-orchestrateDeployment.md`

> Well, the previous Orchestrate is broken, so I don't care about it. [...] just ditch the old Orchestrate.

> if it can do what we need it to do, which is just register paths, then it's good enough for now.

> deploy it right now in an environment without any conditions as a standard thing [...] per user [...] in the home

-- psyche, STT/typed, 2026-08-26.

**2026-08-26, flow 01a03d6e** — `flows/01a03d6e/vision/archive-nexus.md`

> the daemons are called Nexus. So it should be Orchestrate Nexus, and all Nexuses should be like that.

> there should be no bootstrap binary. [...] it can just have a constant in the executable with a default configuration.

> try the default Sema database location and initialize new databases with defaults

> create an interface on the meta socket to allow for changing that configuration.

-- psyche, STT/typed, 2026-08-26.

**2026-08-25, flow aa4c7747** — `flows/aa4c7747/vision/orchestrate.md`

> our first work will be a simple orchestrate nexus that reserves paths to make dead-simple datom-syntax path reservation possible for edit coordination.

> the old orchestrate code should not be considered sacred; we are starting with a simple component that has a normal and meta socket; MVP

-- psyche, typed, 2026-08-25.

**2026-08-24, flow 01a02fd5** — `flows/01a02fd5/vision/interfaces.md`

> the interfaces should be written in schema (or ethos if ethos-monolith can already emit working rust)

> we'll just say ethos, which will motivate everyone to get ethos working.

-- psyche, typed, 2026-08-24.

**2026-08-24, flow 01a02fd5** — `flows/01a02fd5/vision/archive-metaOrchestrate.md`

> if meta-orchestrate was removed, the work was done incorrectly

> restore the meta-orchestrate binary.

-- psyche, typed, 2026-08-24.

**2026-08-24, flow 01a02fd5** — `flows/01a02fd5/vision/archive-nexuses.md`

> all nexuses have a meta socket

-- psyche, typed, 2026-08-24.

**2026-08-22, flow 01a02a34** — `flows/01a02a34/vision/epicBranches.md`

> and youll need to branch the two signal repos as well.

-- psyche, typed, 2026-08-22.

---

## 6. Branch-trains, release-trains, POC stacks, MVPs

### Raw records, newest first

**2026-08-25, flow aa4c7747** — `flows/aa4c7747/vision/dispatches.md`

> And we'll iterate over the design, send, whenever we agree on one round of the design, we'll send a dispatch [...] to a codex flow that will start consecutive rounds of vertical slice implementations, probably on a new repository.

> I dont like this. Id rather get a POC, then we can just write a new version to change the bits we dont like later. Im going to bed so lets get codex working; IV been losing tons of unused quotas lately because im not making the agents work.

-- psyche, typed, 2026-08-25.

**2026-08-22, flow 01a02a34** — `flows/01a02a34/vision/progression.md`

> So we have to take one bite at a time here.

-- psyche, typed, 2026-08-22.

**2026-08-22, flow 01a02a34** — `flows/01a02a34/vision/epicBranches.md`

> and youll need to branch the two signal repos as well.

-- psyche, typed, 2026-08-22.

**2026-08-10, vision-raw** — `vision-raw/mainForEverything.md`

> we should use main for everything

-- psyche, typed, 2026-08-10.

**2026-08-10, vision-raw** — `vision-raw/archive-threeStacks.md`

> I still really much want the new ethos and datum [Datom] languages [...] we could take a lot of complexity out of the incorrect stack because we just want to emit rust. So we could just make a sort of like shortcut [...] ethos rest [ethos-rust]. [...] we should just keep all of the code that's been written on in on the incorrect stuff. I think we should just leave it there and create new repositories for this like shortcut ethos to rest.

-- psyche, dictated, 2026-08-10.

---

## 7. Design approach

### Raw records, newest first

**2026-09-01, flow 995a164e** — `flows/995a164e/vision/designPractice.md`

> step back and discuss this together from a high level: what am I trying to do here?

> Look at how we look at the beautiful rest [STT; Rust] code that we would want to have to express this, and then work your way back from that: what infrastructure do we need to support that code? [...] Don't assume the infrastructure first. Find the goal of the beautiful code that we want, and then work your way back.

-- psyche, STT.

**2026-09-01, flow 995a164e** — `flows/995a164e/vision/rust.md`

> I'm trying to understand why you're presenting this to me in Rust code [...] You've used an implementation block that is not implementing a trait, and that is forbidden. We forbid freestanding implementations. All implementations must be of a trait.

> when we generate Rust, the generated Rust would just use fully qualified names [...] we're using Rust the way we intend to use it, which is more like an assembly language, which is extremely explicit

> I really despise free functions, and I despise these inlined lambdas even more. Whenever I see that, to me, that smells of bullshit and ugly design.

-- psyche, typed and STT.

**2026-08-29, flow e8c4cc61** — `flows/e8c4cc61/vision/designPractice.md`

> whenever a new datom is shown, its spec must first be shown in ethos.

> we need a protos skill. talking in protos dialects is going to be standard.

> Three skills: protos, datom, ethos; datom and ethos should show some rust code

-- psyche, typed.

**2026-08-23, flow a60a9e85** — `flows/a60a9e85/vision/demandDrivenDesign.md`

> that wording "backward from the want" sounds like it came from a pre-school child. too infantile. research the concept and word it as an engineer would word it

-- psyche, typed, 2026-08-23.

**2026-08-18, flow 2b34fafa** — `flows/2b34fafa/vision/rustComponentArchitecture.md`

> thats so stupid. I want to get rid of that, and train against this level of expert foolishness.

> Using mechanical tests isnt going to create good ontology; trait/types design is ontology in code.

> what you said is true, but its stupid because it writes a tool for this single repo, instead of a universal tool being created to test this for any repo

-- psyche, typed, 2026-08-18.

**2026-08-13, flow 6863ef19** — `flows/6863ef19/vision/theBestShape.md`

> If we see from a high level here, if we express things properly, we will minimize the amount of code. The minimum amount of code for the most elegant machinery, which can be easily understood by an engineer and easily extended and easily introspected, is the best shape.

-- psyche, dictated, 2026-08-13.

**2026-08-06, flow 5abf3be8** — `flows/5abf3be8/vision/replacementKillsOldSystem.md`

> any new design that replacess the functionality of an existing system kills the old system.

-- psyche, typed, 2026-08-06.

---

## Vision/ and Intent/ files touching these subjects

| File | Subject(s) |
|---|---|
| **Vision/datom.md** | datom: name, nature, interface shape, de/serialization, relation to ethos, syntax, meaning |
| **Vision/ethos.md** | ethos: what it is, why, generation, non-repetition, self-description, horizon, kind, naming, identity |
| **Vision/ethosMonolith.md** | ethos-zero/monolith: origin, name, shape, purpose, vocabulary, readiness |
| **Vision/protos.md** | protos: direction (realize/textualize, multi-pass) |
| **Vision/orchestrate.md** | orchestrate: deployment, skill scope |
| **Vision/highLevelView.md** | design approach: routinely examine the high-level view |
| **Vision/distillation.md** | distillation process rules |
| **Intent/data.md** | everything is data; protolanguages |
| **Intent/mandatoryTraits.md** | all method calls under traits; Rust is assembly |
| **Intent/protosParsing.md** | context-switching parse; two-way walk |

---

## Entries from flows 1c282d and ad19b1 (being read in full by other subflows)

| Path | Date | One-line pointer |
|---|---|---|
| `flows/1c282d/vision/protosizable.md` | 2026-09-04 | Protosizable is the kind; Structure is really Protoform; ethos:Concept bears Protosizable |
| `flows/1c282d/vision/vocabulary.md` | 2026-09-04 | Potential replaces Prospective; Structure replaces Portion |
| `flows/ad19b1/vision/archive-kinds.md` | 2026-09-04 | Kind Identity rulings; kind is an ethos concept; "I said rust not rest" |
| `flows/ad19b1/vision/archive-meaning.md` | 2026-09-03 | Strings are strings, Meaning is Meaning; Meaning is datom |
| `flows/ad19b1/vision/ethos.md` | 2026-09-04 | Associated constants are UPPER_CASE in the map delimiter; space delimiters and content |
| `flows/ad19b1/vision/designPractice.md` | 2026-09-04 | Show the target Rust alongside ethos |
| `flows/ad19b1/vision/distillation.md` | 2026-09-04 | "Does that sentence even make sense?"; distillation skill universality |
| `flows/ad19b1/vision/psycheSystem.md` | 2026-09-04 | "looks like my psyche system is failing" |

---

## Superseded or conflicting entries

1. **Map delimiter**: `Map.[key.val …]` (2026-08-11, a5587095) was superseded by guillemets (2026-08-26, ac1e9ec8). The distilled Vision/datom.md carries the guillemet ruling.

2. **String delimiter**: Parentheses as the default string delimiter (2026-08-14, ba906ae2 per structuredStringType annotation) was superseded by curly quotes as default, parentheses reserved for Meaning (2026-08-26, ac1e9ec8). The distilled Vision/datom.md carries the later ruling.

3. **Transcodable vocabulary**: `protos::Transcodable` (2026-08-13, 6863ef19) was superseded by the code/encoded drop (2026-08-13 same day). Successor pair is `protos::Realize` / `protos::Textualize` (2026-08-14, ba906ae2).

4. **Ethos-monolith naming**: "whatever shape it is taking already will do" (2026-08-24, aa4c7747 first entry) was superseded same conversation by "go straight for a nexus; it has to be written as a nexus" and "Ethos zero would be a better name."

5. **real/realize**: "realize" for the text-to-value direction (2026-08-28 04db2fd2) was superseded by "embody" (2026-08-28, 2ef42163), then Embodied was revised to be a kind, and the whole was further reworked with Potential/Actualize (2026-09-02, 62022e8f).

6. **Prospective vs Potential**: All uses of "Prospective" were superseded by "Potential" (2026-09-04, 1c282d).

7. **Portion vs Structure**: "Portion" superseded by "Structure" (2026-09-04, 1c282d). Then "Structure is really Protoform" (same flow).

8. **EncodedForm/code vocabulary**: The entire encoded/code vocabulary (2026-08-06, 5abf3be8) was dropped 2026-08-13 in favor of working form and signal form (06196cc7).

9. **Kind identity by path**: The flow's "identified by path, library, and name" was rejected as wrong (2026-09-04, ad19b1). The correct identity: name and constraints, as Rust identifies a trait.

---

## Sources

06196cc7 archive-datomSyntax, encodedFormIsTheCode
a5587095 protosIsTheSharedStyle, archive-datomSyntax, colonFormTransformerSyntax, rustComponentArchitecture
ba906ae2 protosIsTheSharedStyle, encodedFormIsTheCode
5abf3be8 dotOpensDelimiterEverythingIsData, chainedNamesScrapped, sectionsExistToConferTraits, replacementKillsOldSystem, encodedFormFingerprintTraitDesign, streamAsFourthKindMvpFirst, streamDisqualifiesBundling
2b34fafa protosIsTheSharedStyle, ethosNamespaces, ethosSourceFiles, sourceNotCrate, rustComponentArchitecture
01a02a34 epicBranches, progression, archive-ethos, archive-schemaSyntax, archive-datum
01a02fd5 metaOrchestrate, archive-metaOrchestrate, interfaces, archive-nexuses
01a03d6e ethosInterfaces, locks, archive-orchestrateDeployment, archive-orchestrateSkill, archive-dotosFiles, archive-nexus
01a03eda orchestrateRealization, observe, archive-datomSyntax, archive-datomInteger
01a03952 orchestrateInPath
01a038b5 curriculumStackToDatomInsteadOfDotos
01a04339 archive-datom
04db2fd2 anatomy, multiPass, portion, decomposable, delineate, delimiters, directionAsymmetry, kinds, text, textualTypes, archive-datomMaps, archive-datomNexus, artifacts
ac1e9ec8 datomIsData, datomSyntax, distillationNegatives, archive-distillationNegatives
62022e8f archive-datomSyntax, concept, designPractice, distilledVision, ethosTypes, headedAndContained, kinds, layers, multiFormConcepts, passes, symbols, vocabulary, notion/layerMatching, notion/terminology
995a164e archive-datomSyntax, concept, contexts, data, designPractice, entryFiles, ethosTypes, explodedForm, intent, kinds, layerMatching, rust, tokenCosts, vocabulary
e8c4cc61 archive-datomSyntax, datomizable, designExamples, designPractice, ethosFileAnatomy, ethosTypes, kinds, protos, prospective, psycheLayers
aa4c7747 ethos, ethosMonolith, ethosTraitSyntax, orchestrate, interactions, tuples, dispatches
b675f3d9 kinds, structuralParsing, ethosMonolith, highLevelView
2ef42163 ethos, kinds
e4a40e protos, archive-datom, archive-kinds, archive-vocabulary, distillation, newtypeWrappingAndSingleFieldStructs, witnesses
4decf7 archive-datomSyntax, archive-kinds
68512643 negatives
a60a9e85 demandDrivenDesign
6863ef19 theBestShape
f426777b ethosSourceFiles, nexusTraits
db97561c nexus, prospective
acbb6006 approval, distillation, archive-distillation, nexus, archive-nexus
4d5fc7da datom
ad19b1 archive-kinds, archive-meaning, ethos, designPractice, distillation, psycheSystem
1c282d protosizable, vocabulary
Vision/datom, Vision/ethos, Vision/ethosMonolith, Vision/protos, Vision/orchestrate, Vision/highLevelView, Vision/distillation
Intent/data, Intent/mandatoryTraits, Intent/protosParsing
vision-raw/archive-datomSyntax, vision-raw/archive-ethosDotosDivisionAndHelp, vision-raw/archive-ethosNonRepetitionLaw, vision-raw/traitsAsCapabilities, vision-raw/encodedFormIsTheCode, vision-raw/archive-threeStacks, vision-raw/mainForEverything, vision-raw/genericParametersAreTraits, vision-raw/colonFormTransformerSyntax, vision-raw/structuredStringType
