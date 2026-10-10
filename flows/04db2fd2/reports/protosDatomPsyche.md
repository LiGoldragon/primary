# Protos and Datom: verbatim psyche catalogue

## (a) What a datom is / datom syntax

### Name and nature

**Vision/datom.md > Name** (distilled, latest authority):

> Datom is the psyche's own coinage for the new data notation, the
> successor to NOTA and to the rejected name Dotos. The name was
> chosen for its energetic power and to echo what the notation is:
> data, strictly typed, super dense, no field names.

**Vision/datom.md > Nature** (distilled):

> Datom carries data only -- like JSON, but strictly typed. Generics
> belong to Ethos; Datom's whole work is serialization and
> deserialization -- carrying data between text and typed form.
> Generating Rust is Ethos's duty, in today's division of labor. When
> Ethos becomes the full authoring language, with Rustlang as its
> assembly layer, Datom -- the data dialect of the Protos family -- may
> gain an inline place in authored Ethos, the way Rustlang composes
> data directly in code. That road is reached, or even floated, only
> with explicit context: how, when, and where data yields Rust, stated
> without ambiguity; until then the division stands as spoken.

**flows/ac1e9ec8/vision/datomIsData.md** (2026-08-26, session ac1e9ec8):

> you've mixed up datom with ethos. datom is data

Context: the flow's distillation proposal had carried protos parse machinery (shapes, contexts, Realize/Textualize, real and signal forms) and Ethos-side rulings under datom headings.

**flows/ac1e9ec8/vision/datomSyntax.md** (2026-08-26, session ac1e9ec8) -- on the name:

> dont be so apologetic. Datom is the most advanced textual data format in the world.

**flows/ac1e9ec8/vision/datomSyntax.md** (2026-08-26) -- datom is the edge form of signal:

> not legacy. In fact I think they should be positioned as the
> default string delimiter. the vision is that parenthesis will
> become the delimiter for structured strings, still to be designed.
> So let's switch it all to curly quotes first, with parenthesis
> reserved for structured strings, which we currently designate as
> Meaning

> no, this is false. all our components speak signal, not datom;
> datom is only used at the edge to let text-based systems (LLMs and
> all existing editors) understand signal.

**flows/01a02a34/vision/archive-datum.md** (2026-08-22, session 01a02a34, archived -- distilled into Vision/datom.md):

> And you're saying dotos, but like that's the old syntax, which is being replaced by datum, which is, you know, has the same concept.

> And use datom instead of dotos.

### De/serialization

**Vision/datom.md > De/serialization** (distilled):

> Schema-driven and positional: the reader walks the expected type,
> writing is the exact reverse projection, and decoding lands directly
> in the typed Rust structs. All naming and self-description live in
> the type; the text carries only the data.

### Repository and migration

**Vision/datom.md > Repository and migration** (distilled):

> Everything migrates to Datom. Datom's own line of descent is NOTA --
> which also passed through the temporary name Dotos; that old
> notation stays behind, frozen, and may be called legacy. Schema is
> the abandoned ancestor of Ethos, not of Datom. The repository is
> plain datom, with no variant suffix.

**psyche-raw/Vision/archive-threeStacks.md** (2026-08-11, session 012fbf07, archived -- distilled into Vision/datom.md):

> we don't need to worry about the old repo. We're just going to
> move forward and migrate everything to datum [Datom].

**psyche-raw/Vision/archive-threeStacks.md** (2026-08-10, session c6b71b4c):

> So, yeah, I still really much want the new ethos and datum [Datom]
> languages, even if we use the hacky incorrect new stack ... the datum
> [Datom] part is not really problematic in terms of like it's a
> fairly simple thing ... because it's just a serialization and
> deserialization logic.

### Syntax

**Vision/datom.md > Syntax** (distilled, latest authority):

> Consistency comes first: datom's syntax is fixed before the rest.
> Parentheses carry a duty -- they are a major symbol of cognition --
> and are the default string delimiter, balance-based: interior
> balanced pairs are plain content (parentheses inside text are
> markup, the seed of the structured string), the string closes at the
> final unbalanced closer, and an unbalanced interior parenthesis is
> escaped. A string is written bare whenever the bare form can carry
> it, and a bare string may carry symbols that are load-bearing
> elsewhere -- the machinery is made fit for this by the right
> abstraction layers. String blocks are opaque: interior delimiters
> become content until the block closes. A bare brace block is a
> struct; a dot-parenthesis block is a string-carrying variant. The
> dotted prefix of a delimited block is part of the block's type; its
> official name is Head; a variant always re-emits its Head when
> textualized. A map's payload is a square-bracket vector of key.value
> entries, since a map is conceptually a list of key/values.

**TENSION (2026-08-26 supersession):** flows/ac1e9ec8/vision/datomSyntax.md (2026-08-26) reverses the parenthesis-as-default-string-delimiter position from the distilled Vision/datom.md. The 2026-08-26 ruling says curly quotes are the default string delimiter, parentheses reserved for structured strings (Meaning). The distilled Vision/datom.md still carries the 2026-08-14 position. The 2026-08-26 entry is later and supersedes:

> not legacy. In fact I think they should be positioned as the
> default string delimiter. the vision is that parenthesis will
> become the delimiter for structured strings, still to be designed.
> So let's switch it all to curly quotes first, with parenthesis
> reserved for structured strings, which we currently designate as
> Meaning

**flows/ac1e9ec8/vision/datomSyntax.md** (2026-08-26) -- guillemets delimit a map:

> let use the guillemets.

Context: choosing between positional pairs in brackets and a dedicated map delimiter (guillemets or angle brackets). This supersedes the distilled Vision/datom.md's `[key.value ...]` map syntax. Entries resolve by position inside; a Head is thereby always a variant.

**flows/ac1e9ec8/vision/datomSyntax.md** (2026-08-26) -- a map in expected position needs no Map head:

> If a position expects a map, the data will be [ k.v ... ], no Map.

**flows/ac1e9ec8/vision/datomSyntax.md** (2026-08-26) -- under consideration (not ruled):

> Im considering making key/values resolve by position in a map
>
> [ key value second-key second-value ... ]
>
> that looks cleaner and makes the Head. always a variant; lower
> cognitive cost

> or we could use one of the unused delimiters for maps, making them
> easy to spot visually

**flows/01a03eda/vision/datomInteger.md** (2026-08-26) -- integer syntax approved:

> 1. yes

Context: approving canonical bare decimal syntax -- `0`, `42`, `-42`; ASCII digits, no leading `+`, no leading zero except `0`.

**Raw syntax entries (archived -- distilled into Vision/datom.md):**

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-13, session 06196cc7) -- Meaning postponed:

> we'll postpone the Meaning type in datom to get a working syntax
> asap. lets accept a () or the curly quotes for strings for now,
> with the actual shapedefined implementation just casting both into
> a string for now, with a comment to implement the Meaning type
> later (the super-string type we discussed before).

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- string blocks:

> on the block pass: Im willing to increase the complexity a bit to
> allow some blocks, like strings, to allow other delimiters to be
> ignored until it closes, which would allow a string to contain [ { ( etc

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- dotted prefix:

> And the dotted prefix of a delimiter must be part of its type. it
> could be a universal type, and unprefixed blocks simply have no
> prefix. what do we want to call the prefix shape?

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- Head official:

> I like the Head terminology actually. lets make it official

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- parentheses are the default delimiter:

> I would prefer to default to parenthesis for string delimiters. I
> might drop the idea of using parenthesis for a specific Meaning
> type, and just use it for strings. full vertical length delimiters
> have a cognitive ease to them that quotes simply cannot even rival

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- balance-based parentheses:

> Ok now Im full backpedaling on the () for simple strings, since
> parenthesis are so common in strings, and curly brackets are not.
> But there is an interesting pattern here which is tha parentheses
> are already used in text as a way to *markup* the text; so my
> complex-string idea is actually right on the money. I would just
> let the block parser balance parentheses until it reaches the
> final unbalanced ). So im not backpedalling actually; go for
> balance-based, where an unbalanced parenthesis needs to be
> escaped.

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- bare strings may carry load-bearing symbols:

> If its a string, then it can use symbols which would be load
> bearing in other situations, just like delimiters in string
> blocks. no problem there. lets make the machinery fit for this,
> bullet proof not by lots of complex code, but by the right
> abstraction layers.

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- bare brace is struct, X.() is string-carrying variant:

> I dont understand. we have clearly enunciated what those are. the
> first is a struct, the second is (now) a string-carrying variant.
> Why wasnt that obvious?

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- a string that doesn't need quotes must not be quoted:

> A string that doesnt need quotes *must not* be quoted

flows/06196cc7/vision/archive-datomSyntax.md (2026-08-14) -- variants always re-emit their head:

> is Note a variant? then yes. does it have a special shape? then
> it might. It depends.

> Like in ethos, when we are defining types, X.{} is a struct
> called X, and textualizing that type back will re-emit X.{} which
> must be understood in the right context if printed alone, or
> inserted in the right position, if the whole source is
> textualized

flows/a5587095/vision/archive-datomSyntax.md (2026-08-11, session a5587095, archived -- distilled into Vision/datom.md) -- parentheses carry a duty:

> On parenthesis: It would be strange for parenthesis to be unused in
> datom. They are a major symbol of cognition.

flows/a5587095/vision/archive-datomSyntax.md (2026-08-11) -- parentheses delimit the structured string:

> 1. I am considering it, yes. This would require a new type (in
> rust, later ethos-generated) which can be met with either a curly
> quotes or parenthesis (two variants, legacy and structured). The
> structured type would allow for an arbitrary depth, since it is a
> graph of sorts.
>
> 3. shape is still up in the air, but () would be the delimiter

flows/a5587095/vision/archive-datomSyntax.md (2026-08-11) -- map payload is a vector:

> Yes, map would use .[ since a map is conceptually a list of
> key/values

psyche-raw/Vision/archive-datomSyntax.md (archived -- distilled into Vision/datom.md):

(2026-08-11, session 012fbf07) -- datom carries data only:

> datom doesnt do generics, it only carries data, like json (but
> strictly typed of course)

(2026-08-11) -- consistency first:

> So we can just fix datum [Datom] first because we need that. We
> need the syntax to start being consistent.

> I'm not even sure where parentheses are going to be in datum
> [Datom] because in ethos, they're for transformers.

### Meaning / structured string type

**Vision/datom.md > Meaning** (distilled):

> The structured super-string type, Meaning, is postponed so a working
> syntax lands as soon as possible: parenthesis-delimited and
> curly-quote text both land as plain String for now, with the later
> Meaning type marked in code. The eventual shape is one string type
> with two variants -- legacy (curly quotes) and structured
> (parentheses, arbitrary depth, a graph of sorts).

### The interface shape

**Vision/datom.md > The interface shape** (distilled):

> A program's configuration surface is the datom's shape itself, as
> the ethos interface declares it: a data enum at the root whose
> variants are the main operations. A variant's data carries what
> follows: another enum where sub-operations are wanted, a struct or
> vector for final options -- and a struct may embed further
> sub-operations, or any combination imaginable. Output is an enum,
> always -- even the most basic response interface is an enum: Success
> or Failure. The shape already is the interface: datom creates the
> configuration options by its very shape.

**flows/bc05da32/vision/archive-interfaceRootEnumerators.md** (2026-08-22, session bc05da32, archived -- distilled into Vision/datom.md):

> and I dont think we need a derive on a datom type for what we want.
> its simpler than that; datom creates configuration options by its
> very shape, as the ethos interface shows; a data enum at the root
> (main operation) with options in its data

### Dotos files

**flows/01a03d6e/vision/dotosFiles.md** (2026-08-26):

> There should be no Dodos files anymore. [STT correction: Dodos -> Dotos]

### Relation to Ethos

**Vision/datom.md > Relation to Ethos** (distilled):

> Datom and Ethos are different languages that share an approach, not
> a parser. What they may share is a substrate -- traits with a shared
> implementation and types; the universal substrate machinery is homed
> in protos, all dialects ride it, and datom is the pure-data dialect
> on it. Ethos depends on Datom, at minimum to intake data for
> signals; the Meaning context therefore lives in the datom
> repository, seen by both languages.

**psyche-raw/Vision/archive-ethosDotosDivisionAndHelp.md** (2026-08-02, archived -- distilled into Vision/ethos.md):

> the two main syntaxes most agents will face; one specifies the types, the
> other fills them with data -- hence why the basic 'cli help' for their dotos
> objects is meant to emit the ethos syntax that describes their anatomy.

## (b) Textualize / realize / rendering-output

### The three forms

**psyche-raw/Vision/encodedFormIsTheCode.md** (2026-08-06, session 5abf3be8):

> So we agreed that there would be a different type for every kind of
> ethos object, even all the way down to ethos mirroring the types
> that are needed to contain the particular nomos types, for now
> anyway. So that's, you know, the serialized RKYV payload of that
> filled data type is the body. The encoded form is the code. So the
> encoded form of ethos is ethos. The textual form is there so that
> our editors, our current editors, and our current LLM harnesses and
> models can actually make sense of it. Does that answer the question?

**psyche-raw/Vision/encodedFormIsTheCode.md** (2026-08-13, session 06196cc7 -- supersedes the 2026-08-06 framing):

> ok, working form and signal form, drop code/encoded entirely

**flows/06196cc7/vision/encodedFormIsTheCode.md** (2026-08-13, session 06196cc7) -- "working" rejected as a verb-smell:

> I dont like working, it smells like a verb. Same with meaning

**flows/06196cc7/vision/encodedFormIsTheCode.md** (2026-08-14, session 06196cc7) -- the real form; Realize:

> Ok with the real/Realize

Context: the form beside signal and textual -- where values are born and changed -- is the real form, and the text-to-form trait is protos::Realize, paired with protos::Textualize.

### Realize and Textualize trait names

**flows/06196cc7/vision/traitsAsCapabilities.md** (2026-08-13, session 06196cc7) -- textualize on the true type:

> I see a problem myself; when reading text, we dont know what we're
> reading, so how do we call a method without a type?
>
> Conceptually, we need to give a type to the text block, then we
> can have an encode trait on that, and textualize on the true type.
>
> I dont know about encode/decode; which is code and which isnt? The
> way I see it, the binary form (in rust memory, which is
> essentially the rkyv format) is the most code-like. But I think we
> might even want to drop the whole concept of code/encoded to make
> it very clear. textual/textualize is clear, so what term could we
> use for the in-memory/signal form? Is the in-memory data actually
> the same format as the rkyv in reality anyway?

**flows/06196cc7/vision/traitsAsCapabilities.md** (2026-08-14) -- Textualize confirmed:

> Textualize is good

> ShapeDefined is good

**flows/06196cc7/vision/traitsAsCapabilities.md** (2026-08-14) -- verbs accepted for traits:

> Yes, I accept verbs. now I can see why rust went with verbs; it
> is easy to understand that a thing that which implements Run is
> CapableOfRunning.

**flows/06196cc7/vision/traitsAsCapabilities.md** (2026-08-14) -- no umbrella; directional traits live in protos:

> none of this makes sense if we use a trait for each direction.
> The traits should live in protos regardless (Textualize and
> whatever we pick for Materialize)

**flows/06196cc7/vision/traitsAsCapabilities.md** (2026-08-14) -- RealizeWalk and TextualizeWalk accepted:

> fine. im not crazy about it but its good enough

Context: direction-drivers are RealizeWalk and TextualizeWalk, conduct methods (enter, close, position, resume) under the protos trait Walk.

**flows/ba906ae2/vision/encodedFormIsTheCode.md** (2026-08-14, session ba906ae2) -- textualize approved:

> textualize is approved. im pretty sure I had approved it, but
> there it is again

### Realize and Textualize are on different types

**flows/2b34fafa/vision/traitsAsCapabilities.md** (2026-08-18, session 2b34fafa):

> realize isnt implemented by the same type as textualize. if you
> cant find two different types, the implementation is wrong. You
> dont textualize the text, and you dont realize the realized data.

Context: the textual type carries Realize (it realizes into the real type); the real type carries Textualize (it textualizes into the textual type). Any type implementing both is a wrong implementation.

### Define the block: ontology of source code

**flows/2b34fafa/vision/protosIsTheSharedStyle.md** (2026-08-18, session 2b34fafa):

> we need to define the block. start with the text source code. turn
> every logical aspect into a type. ontology of source code

Context: after ruling that the text realizes and the real textualizes, when asked what textual type does the realizing below the top level.

### Translator naming

**flows/55d18f4f/vision/itsATranslator.md** (2026-08-08, session 55d18f4f):

> its misnamed. its a translator. it translates code into text. right?

> it should be called protos-translator

(2026-08-14 annotation: "code" here is the pre-drop sense -- now the signal form.)

### Nexus never textualizes

**flows/e06e4c07/vision/nexus.md** (carries context about signal purity):

> Every Nexus speaks only pure binary signal and never textualizes it

## (c) Protos and their relation to ethos

### Protos is the shared style

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-11, session a5587095):

> remember; once we open the Meaning delimiter (that what were
> calling it), all the delimiters and structured parsing spectrum is
> available, until that closing delimiter comes in and changes the
> parser's context; that is how all our languages parse and why we
> can design so freely. This is important and is the part of the
> code which can be shared between all parsers (should be in protos;
> protos is the name we give to the style which all our dialects
> share; hence why the final fully-decomposed engine with 3 daemons
> is the protos engine, with datom sort of sitting besides it, as it
> is only for pure, typed data)

### There is always a parsing context

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-11):

> no, there is always a parsing context. it doesnt suspend, it
> *changes*, but the underlying mechanism is always the same; Now,
> we are parsing in context X and can therefore expect A, B or C
> shapes of things, and Z would end that context, but meeting A
> would switch to the context which A entails. That has been the
> ruling principle of NOTA (datoms's ancestor) from day one. I want
> to extend it now to say it should always use trait.

### Two-way structural parse; flesh out before Intent

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-11):

> Intent would be quite general, about the way the parsing is
> approached. Lets flesh it out in detail with examples then we can
> make it intent. Intent is basically very clear vision which is
> unlikely to change. Dont forget the parsing is also two-ways. I
> feel like we need to really flesh out this two-way structural
> transcoding, through clear explanation and with a trait-library
> first approach, in protos repo (which can be re-considered from
> whatever it is doing now) We need to work with visuals, examples,
> and traits with main types. that must become our design pattern.

### The expects vector: ProtosShapes

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-12):

> the more complex trait will be a vector of ProtosShape's (welcome
> to propose other names), when the structure dictates the outer
> type, for example in ethos when X.{ means a struct, and Y.[ means
> an enum, and Z:Transform.[/{ means different kinds of transformers

### ProtosShape is a trait; types carry their own context

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-12):

> The type met implements its own context? Does that make sense?

> To me ProtosShape was a trait. so for a throaway example (dont
> make this canonical, I just dont have a better example atm),
> NewString would implment ProtosShape. Maybe the right shape for
> NewString is an Enum with variants String and Meaning, and
> implementing ProtosShape means creating a match on standard
> ProtosShape (which is why I thought the trait should be named
> something else - ProtosShaped? ShapeDefined?). Those ProtosShape
> are always the same, and in this case it would use
> SimpleDelimiter(CurlyQuotes), or maybe its just
> CurlyQuoteDelimited if the nested variant data makes the logic
> more complex than warranted, and the other would be
> ParenthesisDelimited, with each yielding the corresponding
> variant, each of which has its own parsing context
> implementation. Does that make sense?

### Recursion, logic planes, child context

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-12):

> because of recursion, the position of the parent context still
> needs to be kept, so that returning to the parent context resumes
> at the following position.

> Your read impl for ShapeDefined seem to want to implement
> parsing. I dont know if thats where we want to put that logic. We
> might want to just get the type, and let that type implement its
> parsing context. Big implementations are a sign of a missing
> logic plane. Everything should be simple individually. The
> complexity is in the totality, not the individual parts.

> that doesnt seem to account for new contexts being entered, where
> the parent's "end shape" could be met, but then it wouldnt have
> that meaning anymore.

### Intent graduated

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-13):

> the intent is good

Context: approved the v3 draft. Landed as psyche/Intent/protosParsing.md.

### Recursion must carry shape-determined types at every level

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-13):

> your recursive parsing wasnt complex enough. we need to consider
> multiple levels, each with one or more shape-determined type

### No traits is no good

**flows/a5587095/vision/protosIsTheSharedStyle.md** (2026-08-13):

> I only looked at the code. I need to see the traits. No traits
> is no good

### Datom is a protos dialect

**flows/ba906ae2/vision/protosIsTheSharedStyle.md** (2026-08-14, session ba906ae2):

> because datom doesnt take part in the multi pass engine which
> ethos->nomos->logos->rust is slated to become. but youre right;
> beside sounds like its not a protos dialect. it *is* a protos
> dialect, but not part of the future ethos/nomos/logos
> rust-generation engine

### Protos homes the universal substrate

**flows/06196cc7/vision/threeStacks.md** (2026-08-14, session 06196cc7):

> what shared framework? I want universal stuff in protos, since
> all dialects will use it. Im not worried about rewriting whatever
> is in protos right now since nothing works anyway. we can just
> leave a big non_idea_agents.md note in its repo. But id like to
> know what you mean by Codec

Context: the universal substrate -- walk machinery, Shape vocabulary, ShapeDefined, Head, protos::Realize and protos::Textualize, the first-pass block scanner, string carriers -- is homed in the protos repository; all dialects ride it; datom is the pure-data dialect on top.

### Protos parsing Intent

**psyche-raw/Intent/protosParsing.md** (Intent level, graduated 2026-08-13):

> Protos parsing always happens inside a context, and only the
> current context gives shapes their meaning: it defines which
> shapes can appear next and which shape completes it. A met shape
> announces a type, and that type's context takes over completely
> until its completing shape; then the parent context resumes
> exactly where it left off. Reading and writing are one walk in
> two directions -- text lands in typed values, and typed values
> project back into the same text.

Provenance: Designer-drafted, approved as Intent by the psyche 2026-08-13.

## (d) Anatomy / ontology-based design bearing on textualize/realize

### The best shape

**flows/6863ef19/vision/theBestShape.md** (2026-08-13, session 6863ef19, candidate Intent):

> If we see from a high level here, if we express things properly,
> we will minimize the amount of code. The minimum amount of code
> for the most elegant machinery, which can be easily understood by
> an engineer and easily extended and easily introspected, is the
> best shape.

### All method calls in traits

**flows/a5587095/vision/rustComponentArchitecture.md** (2026-08-11, session a5587095):

> I even want to make the broad statement that I want *all* method
> calls in our rust code to be part of a trait, since I need to
> understand my systems through traits and main types, as I cannot
> possibly read all the code, and rust is the new assembly language;
> no serious engineer reads all the assembly code anymore, and the
> same is going to happen to rust, hence why we need a more concise,
> dense and congnitively concentrated language like ethos to write
> code with AI agents.

### Ontological study; trait/types design is ontology in code

**flows/2b34fafa/vision/rustComponentArchitecture.md** (2026-08-18, session 2b34fafa):

> Using mechanical tests isnt going to create good ontology;
> trait/types design is ontology in code.

> Do an othological study of the code, and create the most unified
> map of traits and types you can.

### The main function chain

**psyche-raw/Vision/mainFunction.md** (2026-08-21, session 2b34fafa):

> So you get whatever the end result is and then try from and then
> the most high level type.
> So we're going to create an object for everything, basically ...
> a spec that is an object that is a fully compliant data
> tree, a graph of data that can yield the entire program ...

(2026-08-22, session bc05da32) -- main's chain begins at the input:

> in your main block, you forgot the input, which is a strictly
> typed object coming in as datom.

### Structural parsing (latest: 2026-08-27)

**flows/b675f3d9/vision/structuralParsing.md** (2026-08-27) -- arity discriminates; capability enum:

> I have actually reconsidered the idea that we can use multiple... that the structural parsing can actually discern between structs of different size to differentiate between different types. And I don't know why I didn't actually seriously contemplate this before. It seems pretty obvious now. Also, I think we should introduce more of the concept of using different delimiters between the head and the delimiter to add even more type differentiation using very minimal character slash token cost.

> <> is a real Protos delimiter of course. I'm surprised you have to ask

(2026-08-27) -- parsing is always context-dependent; a character in one block is free in another:

> No. That's not how it works. If the, uh, colon is used in imports, it doesn't at all keep us from using it in another context. So, again, you seem to have a hard time understanding that ethos parsing is always dependent on the current context in which the parsing is taking place.

(2026-08-27) -- shape conveys type only within context; a head's presence can itself convey type; not every block starts with a head:

> this is false since it is context dependent. and the mere fact that something starts with a head could convey the type. and not every block starts with a head, which is also implied elsewhere and false

### Distillation correction: placement matters

**flows/b675f3d9/vision/distillation.md** (2026-08-27):

> dont give me blocks of proposal without telling me where it goes, since "The signal interfaces tell an enum from a struct by the delimiter after the head" is ethos vision, *not* protos, so I cant say yes or no to your proposal. propose a distillation edit for this as well.

### Realizer aspect naming

**psyche-raw/Vision/realizer.md** (2026-08-09, Codex session):

> single word. extending athena (bringing design into reality)

> yes, thats right. so change your awareness name and update it.

> the realizer and designer will be involved with each other a lot

**psyche-raw/Vision/flowsNotAgents.md** (2026-08-13):

> I want to change all shard names away from person-implying (realizer) to concept (realization).

### Negatives in distilled vision

**flows/ac1e9ec8/vision/distillationNegatives.md** (2026-08-26):

> now show me the final full-vision for datom. dont give me useless
> negatives; those can be archived without worrying; the archives are
> still there and can be linked in the distillation still

> I want this kind of stuff to be in the forbidden list for vision
> distillation; this *is* the psyche's vision.

(On "The name is the psyche's coinage" -- a vision statement never attributes itself to the psyche.)

### Datom and negatives: the road opens only explicitly contextualized

**flows/68512643/vision/negatives.md** (2026-08-23, session 68512643):

> On your second point about Datom, and I don't want to go down this
> hole, really ... So, and I'm not arguing completely against that, but
> you generated the idea that Datom does not generate rust. But let's
> look at rust for a minute ... When we use
> rust to compose, or rustlang to compose a type directly in the
> code, we're essentially writing data in the code. And so if further
> down the road ... Ethos becomes
> the full authoring language, with rustlang as its assembly layer ...
> then the idea that Datom doesn't generate rust ... would most likely impede the LLM from suggesting or seeing
> the possibility.

> So the line it's dangerous is true in that context because when
> the model brought forward the idea that Datom generates rust,
> there wasn't enough subtlety. Like, we aren't there yet. My whole
> point was that we might eventually get there. But if we do either
> get there or if we float the idea of how we would get there, it
> would be very explicitly, uh, contextualize so that there's no
> ambiguity as to how and when and where data may or may not
> generate rust.

## Ordering and conflict notes

### Datom string delimiters -- ACTIVE CONFLICT

The distilled Vision/datom.md still carries the 2026-08-14 position (parentheses as the default string delimiter, balance-based). The 2026-08-26 ruling in flows/ac1e9ec8/vision/datomSyntax.md supersedes this: curly quotes are the default string delimiter, parentheses reserved for structured strings (Meaning). **The distilled vision needs updating.** The 2026-08-26 entry is later and explicitly says "let's switch it all to curly quotes first".

### Datom map syntax -- ACTIVE CONFLICT

The distilled Vision/datom.md says "A map's payload is a square-bracket vector of key.value entries." The 2026-08-26 ruling (ac1e9ec8) introduces guillemets as the map delimiter. **The distilled vision needs updating.**

### forms vocabulary

2026-08-06: "the encoded form is the code"
2026-08-13: "working form and signal form, drop code/encoded entirely" -- supersedes
2026-08-13: "working" rejected (verb smell)
2026-08-14: "the real form" confirmed, protos::Realize confirmed
No conflict; clean supersession chain ending at: **real form, signal form, textual form**.

### Realize/Textualize on different types

2026-08-13-14: traits designed alongside the same type (the existing code had both on one type)
2026-08-18: "realize isnt implemented by the same type as textualize" -- clean ruling, no contrary later entry

### Protos engine location

Consistent from 2026-08-11 through 2026-08-14: universal substrate in protos repo, all dialects ride it.

### Structural parsing (latest 2026-08-27)

The 2026-08-27 entries expand the design space (arity discrimination, head delimiters, angle brackets as real protos delimiters, not every block starts with a head). These are the latest rulings and are not yet distilled.

## Unknowns

Things the psyche has not spoken on that a review of textualize/realize anatomy would need:

1. **Textual type taxonomy**: what textual types exist below the top level, and what their Realize implementations look like. The psyche said "define the block; turn every logical aspect into a type; ontology of source code" (2026-08-18) but the actual type set is not enumerated.

2. **Realize trait signature**: the trait is named and homed (protos::Realize), and the design pattern (the textual type carries Realize, the real type carries Textualize) is clear, but the Rust trait signature -- associated types, error handling, lifetime bounds -- is not ruled.

3. **Walk trait method set**: RealizeWalk and TextualizeWalk were accepted with explicit reservation ("im not crazy about it but its good enough"). The conduct methods (enter, close, position, resume) are named in agent context, not in the psyche's own words. Whether this set is final is unruled.

4. **Error handling in realize/textualize**: which form transitions are fallible (TryFrom vs From) at the block level. The top level is TryFrom (main function discussion); block-level fallibility is unspoken.

5. **Signal form production**: the signal form (rkyv-serialized portable binary) is named and the textual form's role as accessibility layer is clear, but how/when a real form becomes a signal form -- and whether there is a protos trait for that direction -- is not ruled. The early "Signalize"/"Materialize" naming was dropped without replacement.

6. **Guillemet map syntax details**: guillemets were chosen (2026-08-26) but the internal positional layout of key/value pairs inside guillemets is "under consideration, not ruled."

7. **Curly-quote string reversal and Meaning**: the 2026-08-26 reversal (curly quotes as default delimiter) is not yet reconciled with the parenthesis-balance-based content rules in the distilled vision. Whether parentheses still participate in the structured-string Meaning type alongside curly quotes, or are now exclusively for Meaning, needs confirmation.

8. **Angle-bracket delimiter semantics**: `<>` confirmed as a real Protos delimiter (2026-08-27) but its use cases beyond "ethos generics" are not ruled.

9. **How datom's Realize/Textualize relate to protos's**: datom is a protos dialect and datom is data only. Whether datom types implement protos::Realize and protos::Textualize directly or through dialect-specific intermediaries is unspoken.

10. **The Meaning type design**: postponed for a working syntax, the structured super-string type remains undesigned. Its interaction with the realize/textualize walk (does Meaning content recurse into a new parse context?) is unspoken.

## Sources

### Distilled vision (highest authority)
- Vision/datom.md
- Vision/ethos.md
- Vision/ethosMonolith.md

### Intent
- psyche-raw/Intent/protosParsing.md

### psyche-raw/Vision
- psyche-raw/Vision/archive-datomSyntax.md (archived; distilled into Vision/datom.md)
- psyche-raw/Vision/archive-ethosDotosDivisionAndHelp.md (archived; distilled into Vision/ethos.md)
- psyche-raw/Vision/archive-threeStacks.md (archived; distilled into Vision/datom.md and Vision/ethosMonolith.md)
- psyche-raw/Vision/assembly.md
- psyche-raw/Vision/encodedFormIsTheCode.md
- psyche-raw/Vision/flowsNotAgents.md
- psyche-raw/Vision/mainFunction.md
- psyche-raw/Vision/protosIsTheSharedStyle.md (empty; content is in flow records)
- psyche-raw/Vision/realizer.md
- psyche-raw/Vision/structuredStringType.md

### Flow vision records
- flows/012fbf07/vision/threeStacks.md
- flows/01a02a34/vision/archive-datum.md
- flows/01a02a34/vision/archive-ethos.md
- flows/01a02a34/vision/archive-schemaSyntax.md
- flows/01a02fd5/vision/interfaces.md
- flows/01a03d6e/vision/dotosFiles.md
- flows/01a03eda/vision/datomInteger.md
- flows/01a03eda/vision/orchestrateRealization.md
- flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md
- flows/01a035d3/vision/rustCodeFromTheData.md
- flows/06196cc7/vision/archive-datomSyntax.md
- flows/06196cc7/vision/encodedFormIsTheCode.md
- flows/06196cc7/vision/threeStacks.md
- flows/06196cc7/vision/traitsAsCapabilities.md
- flows/2b34fafa/vision/protosIsTheSharedStyle.md
- flows/2b34fafa/vision/rustComponentArchitecture.md
- flows/2b34fafa/vision/traitsAsCapabilities.md
- flows/2b34fafa/vision/importResolution.md
- flows/55d18f4f/vision/itsATranslator.md
- flows/68512643/vision/negatives.md
- flows/6863ef19/vision/theBestShape.md
- flows/a5587095/vision/archive-datomSyntax.md
- flows/a5587095/vision/colonFormTransformerSyntax.md
- flows/a5587095/vision/protosIsTheSharedStyle.md
- flows/a5587095/vision/rustComponentArchitecture.md
- flows/ac1e9ec8/vision/datomIsData.md
- flows/ac1e9ec8/vision/datomSkill.md
- flows/ac1e9ec8/vision/datomSyntax.md
- flows/ac1e9ec8/vision/distillationNegatives.md
- flows/b675f3d9/vision/distillation.md
- flows/b675f3d9/vision/structuralParsing.md
- flows/ba906ae2/vision/encodedFormIsTheCode.md
- flows/ba906ae2/vision/protosIsTheSharedStyle.md
- flows/bc05da32/vision/archive-interfaceRootEnumerators.md
- flows/bc05da32/vision/mainFunction.md
- flows/e06e4c07/vision/nexus.md
- flows/e4be1c4a/vision/rustComponentArchitecture.md

### Files read but carrying only incidental mentions (not catalogued above)
- flows/01a01bac/vision/skillDesigning.md
- flows/01a02400/vision/defaultOpeningLogic.md
- flows/01a02b46/vision/zeusUpdate.md
- flows/01a02b4d/vision/actualProblemsWeAreSolving.md
- flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md
- flows/01a04336/vision/remoteFlag.md
- flows/358f143a/vision/trainingRepo.md
- flows/b7465e71/vision/remembering.md
- psyche-raw/Vision/mentci.md
- psyche-raw/Vision/skillsRepository.md

### Curriculum skills
No authored skill derived from datom vision was found in `Curriculum skills/`. Flow ac1e9ec8's datomSkill.md records the psyche's directive to create one after distillation, but the skill itself has not been authored yet.
