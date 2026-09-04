# Psyche gathering — the topics 6329f1 touches

Flow b9a334, subflow report, 2026-09-04. Written for a later subflow
to turn into a web report for the living. The living's words are
carried verbatim throughout; each quote carries its path, its entry
heading, its date, and its provenance line as the record carries it.

How to read the marks. **Witnessed** means this subflow read the file
or ran the command itself. **Relayed** means a read subagent of this
subflow read it and this subflow carries its report; where a relayed
fact mattered, this subflow re-read the file and the mark says
witnessed. **Inference (mine)** marks a conclusion this subflow drew.
**Distilled** on a raw record means Vision/sources/<topic>.md names
that flow and entry; **undistilled** means it does not.

Provenance lines are carried as the record writes them; older records
write "— psyche, <date> (<session>), typed", newer ones "-- psyche,
typed." or "-- psyche, STT." Archived records open with an "Archived
on landing" line; notions are in a flow's notion/ directory and are
marked as notions.

---

## 1. Core topics

### 1.1 Protos

#### Distilled state

**Vision/protos.md** (witnessed whole, 95 lines). Sections: What
Protos is; What Protos knows; Direction; Structure; Delineation;
Layers; Multi-pass; Canonical print. The file itself names no landing
flow. Its git history (witnessed): replaced whole by 6329f1's landing
commit 23aaf7a7f on 2026-09-04 17:14:39 +0200 ("Land the living's
corrected vision: Protos layers and the Ethos Declaration"); before
that, 10a2eb054 on 2026-08-27 by flow 04db2fd2 ("Vision/protos.md —
direction"). The 6329f1 archive headers say which sections the flow's
records went to: archive-protos.md → Direction, Structure,
Delineation, Layers; archive-vocabulary.md → Direction, Layers.

**Vision/sources/protos.md** (witnessed whole, 26 entries): a5587095
protosIsTheSharedStyle; ba906ae2 protosIsTheSharedStyle; ba906ae2
encodedFormIsTheCode; e4a40e protos; 04db2fd2 anatomy, multiPass,
portion, delimiters; e8c4cc61 protos, prospective, kinds; 62022e8f
kinds, layers, concept, passes, vocabulary; 2ef42163 kinds; b675f3d9
structuralParsing, kinds; 1c282d protosizable, vocabulary; ad19b1
ethos; 6329f1 protos, vocabulary.

**Intent/protosParsing.md** (relayed): approved 2026-08-13 in session
a5587095; protos parsing is context-driven, met shapes announce types
whose contexts take over until completion; reading and writing are
one walk in two directions; carries an annotation that "two-way
structural transcoding" is dead vocabulary.

The landed text on the map question, witnessed, Vision/protos.md
lines 44–48:

```
    44	An enclosed structure stands between its delimiters. Six delimiter
    45	pairs in all: four structural — braces, brackets, guillemets, angle
    46	brackets — and two opaque — curly quotes, where every glyph inside
    47	is content, and parentheses, read by balance. Angle brackets are a
    48	real protos delimiter. A bare structure has no delimiters.
```

That is the only line in Vision/protos.md naming guillemets; the file
does not use the « » glyphs and does not carry the word "map"
(witnessed by grep).

#### Raw records, oldest first

Every protos record below was read by this subflow (witnessed) after
the read-critical subagent located it, except the three marked
relayed, whose openings this subflow confirmed against the files.
Records whose heading carries no date are dated by the flow's first
commit in git (witnessed), stated as "flow of".

**flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md** — not
archived. Undistilled. 2026-08-06. Quoted whole in the ethos section
(1.2): "you mean, it opens a delimiter. everything is data".

**flows/a5587095/vision/protosIsTheSharedStyle.md** — not archived.
Distilled (a5587095 protosIsTheSharedStyle). Relayed; opening
confirmed. Nine entries, 2026-08-11 to 2026-08-13, all "(Designer
session a5587095), typed":

> ## 2026-08-11 — the definition; context-switching parse; the protos engine
>
> > remember; once we open the Meaning delimiter (that what were
> > calling it), all the delimiters and structured parsing spectrum is
> > available, until that closing delimiter comes in and changes the
> > parser's context; that is how all our languages parse and why we
> > can design so freely. This is important and is the part of the
> > code which can be shared between all parsers (should be in protos;
> > protos is the name we give to the style which all our dialects
> > share; hence why the final fully-decomposed engine with 3 daemons
> > is the protos engine, with datom sort of sitting besides it, as it
> > is only for pure, typed data)
>
> — psyche, 2026-08-11T19:44+02:00 (Designer session a5587095), typed,

> ## 2026-08-11 — there is always a parsing context; it changes, never suspends; always use trait
>
> > no, there is always a parsing context. it doesnt suspend, it
> > *changes*, but the underlying mechanism is always the same; Now,
> > we are parsing in context X and can therefore expect A, B or C
> > shapes of things, and Z would end that context, but meeting A
> > would switch to the context which A entails. That has been the
> > ruling principle of NOTA (datoms's ancestor) from day one. I want
> > to extend it now to say it should always use trait.
>
> — psyche, 2026-08-11T19:53+02:00 (Designer session a5587095), typed,

> ## 2026-08-11 — two-way structural transcoding; flesh out before Intent; the design pattern
>
> > Intent would be quite general, about the way the parsing is
> > approached. Lets flesh it out in detail with examples then we can
> > make it intent. Intent is basically very clear vision which is
> > unlikely to change. Dont forget the parsing is also two-ways. I
> > feel like we need to really flesh out this two-way structural
> > transcoding, through clear explanation and with a trait-library
> > first approach, in protos repo (which can be re-considered from
> > whatever it is doing now) We need to work with visuals, examples,
> > and traits with main types. that must become our design pattern.
>
> — psyche, 2026-08-11T22:04+02:00 (Designer session a5587095), typed,

> ## 2026-08-12 — the expects vector: ProtosShapes; structure can dictate the outer type
>
> > the more complex trait will be a vector of ProtosShape's (welcome
> > to propose other names), when the structure dictates the outer
> > type, for example in ethos when X.{ means a struct, and Y.[ means
> > an enum, and Z:Transform.[/{ means different kinds of transformers
>
> — psyche, 2026-08-12T00:59+02:00 (Designer session a5587095), typed,

> ## 2026-08-12 — ProtosShape is a trait types implement; the match on standard shapes; types carry their own context
>
> > The type met implements its own context? Does that make sense?
>
> > To me ProtosShape was a trait. so for a throaway example (dont
> > make this canonical, I just dont have a better example atm),
> > NewString would implment ProtosShape. Maybe the right shape for
> > NewString is an Enum with variants String and Meaning, and
> > implementing ProtosShape means creating a match on standard
> > ProtosShape (which is why I thought the trait should be named
> > something else - ProtosShaped? ShapeDefined?). Those ProtosShape
> > are always the same, and in this case it would use
> > SimpleDelimiter(CurlyQuotes), or maybe its just
> > CurlyQuoteDelimited if the nested variant data makes the logic
> > more complex than warranted, and the other would be
> > ParenthesisDelimited, with each yielding the corresponding
> > variant, each of which has its own parsing context
> > implementation. Does that make sense?
>
> — psyche, 2026-08-12T01:26+02:00 (Designer session a5587095), typed,

> ## 2026-08-12 — recursion keeps the parent's position; logic planes; a child context takes the shapes' meaning
>
> > because of recursion, the position of the parent context still
> > needs to be kept, so that returning to the parent context resumes
> > at the following position.
>
> > Your read impl for ShapeDefined seem to want to implement
> > parsing. I dont know if thats where we want to put that logic. We
> > might want to just get the type, and let that type implement its
> > parsing context. Big implementations are a sign of a missing
> > logic plane. Everything should be simple individually. The
> > complexity is in the totality, not the individual parts.
>
> > that doesnt seem to account for new contexts being entered, where
> > the parent's "end shape" could be met, but then it wouldnt have
> > that meaning anymore.
>
> — psyche, 2026-08-12T21:23+02:00 (Designer session a5587095), typed,

> ## 2026-08-13 — the Protos parsing Intent is graduated
>
> > the intent is good
>
> — psyche, 2026-08-13T00:19+02:00 (Designer session a5587095), typed,

> ## 2026-08-13 — recursion must carry shape-determined types at every level
>
> > your recursive parsing wasnt complex enough. we need to consider
> > multiple levels, each with one or more shape-determined type
>
> — psyche, 2026-08-13T00:25+02:00 (Designer session a5587095), typed,

> ## 2026-08-13 — no traits is no good
>
> > I only looked at the code. I need to see the traits. No traits
> > is no good
>
> — psyche, 2026-08-13T00:29+02:00 (Designer session a5587095), typed,

**flows/a5587095/vision/colonFormTransformerSyntax.md** — not
archived. Undistilled in sources/protos.md (named in
sources/datom.md). Relayed; opening confirmed.

> ## 2026-08-11 — transformer payloads take `.[` or `.{`; parentheses freed in Ethos
>
> > I think we are wrongly using parenthesis in ethos now, since we
> > introduced X:Transformer syntax, which differentiates transformers
> > (and some transformers might expect a single vector, in which case
> > .[ is better, and for the rest expecting a structured input .{ is
> > the right delimiter). This would free patenthesis completly, and I
> > have an idea for a revolutionary type; a structured string type -
> > something that would revolutionize LLM performance by exposing the
> > emphasis and other structural aspects which a plain string simply
> > doesnt have. think of it as an annotated string
>
> — psyche, 2026-08-11T18:53+02:00 (Designer session a5587095), typed,

**vision-raw/encodedFormIsTheCode.md** — not archived. Undistilled
(sources/datom.md names 06196cc7 encodedFormIsTheCode, sources/protos.md
names ba906ae2 encodedFormIsTheCode; not this file). Relayed; opening
confirmed. Two entries: 2026-08-06T21:53:42Z "The encoded form is the
code" (Designer session 5abf3be8) and:

> ## 2026-08-13 — working form and signal form; code/encoded dropped
>
> > ok, working form and signal form, drop code/encoded entirely
>
> — psyche, 2026-08-13 (Designer session 06196cc7), typed,

**flows/ba906ae2/vision/protosIsTheSharedStyle.md** — not archived.
Distilled (ba906ae2 protosIsTheSharedStyle). Witnessed.

> ## 2026-08-14 — datom is a protos dialect, not part of the rust-generation engine
>
> > because datom doesnt take part in the multi pass engine which
> > ethos->nomos->logos->rust is slated to become. but youre right;
> > beside sounds like its not a protos dialect. it *is* a protos
> > dialect, but not part of the future ethos/nomos/logos
> > rust-generation engine
>
> — psyche, 2026-08-14T10:09+02:00 (Designer session ba906ae2),
> typed,

**flows/ba906ae2/vision/encodedFormIsTheCode.md** — not archived.
Distilled (ba906ae2 encodedFormIsTheCode). Witnessed.

> ## 2026-08-14 — textualize is approved
>
> > textualize is approved. im pretty sure I had approved it, but
> > there it is again
>
> — psyche, 2026-08-14T13:04+02:00 (Designer session ba906ae2),
> typed,

**flows/06196cc7/vision/traitsAsCapabilities.md** and
**flows/2b34fafa/vision/traitsAsCapabilities.md** — 2026-08-13/14 and
2026-08-18; quoted whole in 1.2. The 2b34fafa line "You dont
textualize the text, and you dont realize the realized data" is the
root of Direction.

**flows/2b34fafa/vision/protosIsTheSharedStyle.md** — not archived.
Undistilled. Witnessed.

> ## 2026-08-18 — define the block: start with the text source code; every logical aspect a type; ontology of source code
>
> Design session `2b34fafa`, typed (captured 2026-08-18), after ruling
> that the text realizes and the real textualizes, when asked what
> textual type does the realizing below the top level:
>
> > "we need to define the block. start with the text source code. turn
> > every logical aspect into a type. ontology of source code"

**flows/ac1e9ec8/vision/datomSyntax.md** — 2026-08-26; the guillemet
ruling and "<> is used in ethos, and those two must remain compatible";
quoted whole in 1.3.

**flows/b675f3d9/vision/structuralParsing.md** — not archived.
Distilled (b675f3d9 structuralParsing). Witnessed. Three entries,
2026-08-27:

> ## Arity discriminates; more head delimiters; the Capability enum of structural forms
>
> 2026-08-27, the psyche, dictated, with a handwritten page
> (ethosAdvancedStructuralParsing.jpg, transcribed below):
>
> > I have actually reconsidered the idea that we can use multiple... that the structural parsing can actually discern between structs of different size to differentiate between different types. And I don't know why I didn't actually seriously contemplate this before. It seems pretty obvious now. Also, I think we should introduce more of the concept of using different delimiters between the head and the delimiter to add even more type differentiation using very minimal character slash token cost. So I handwrote some of these concepts, and this is really just early brainstorming on what For example, how we can differentiate between different capability types. So this would be... I essentially use the ethos -- Syntax for defining an enum to show the different types of capabilities that could exist. And then in the comments, I would I was showing how the the syntax would expose their types by writing them with a different structure, which could include the... and I didn't really elaborate much on this because I was running out of page, but which could also include the number of components in a brace, which symbolically stands for a struck [struct]. But in this case, we wouldn't be limited to a single type of struck [struct].
>
> > <> is a real Protos delimiter of course. I'm surprised you have to ask
>
> ### The handwritten page (transcription; the image is authoritative)
>
>     Ethos advanced Structural Parsing
>
>     Capability.[                    ;; A Vector-represented Enum
>       SingleYield.{Name Concept}
>       ;; ↑ Represented as 'Head.Concept'
>       ;; A Concept being a type or a Kind
>
>       ;; Thought experiment: Different head delimiter
>       ;; to differentiate mutable self 'Head!Concept'
>       MutableSingleYield.{Name Concept}
>
>       MultipleYields.{Name Vector<Concept>}
>                       ;; Name.[ConceptOne ConceptTwo ...]
>
>       MutableMultipleYields...
>
>       Multiple-
>       Standard.{Name Vector<Concept> Vector<Concept>}
>       ;; Head.{[InputOne InputTwo] [OutputOne OutputTwo]}
>
>       ...
>     ]

> ## Parsing is always dependent on the current context; a character taken in one block is free in another
>
> 2026-08-27, the psyche, dictated, on the report's claim that `:` is unavailable as a head delimiter because imports use it:
>
> > No. That's not how it works. If the, uh, colon is used in imports, it doesn't at all keep us from using it in another context. So, again, you seem to have a hard time understanding that ethos parsing is always dependent on the current context in which the parsing is taking place. So in the import block, colon are treated in a certain way, maybe, maybe not. But currently, they are in in the current vision. And then the same colon used in another block could be used to, obviously, to mean something else since another block would not involve imports. So like I said, ethos is extremely flexible in how it can use the same thing in different contexts to mean different things. And you seem to have a hard time wrapping your mind around that.

> ## Shape conveys type only within context; a head's presence can itself convey type; not every block starts with a head
>
> 2026-08-27, the psyche, typed, on the proposed distilled statement "What follows a head tells its type" (reports/distillProposalProtosDatom.md):
>
> > this is false since it is context dependent. and the mere fact that something starts with a head could convey the type. and not every block starts with a head, which is also implied elsewhere and false

**flows/b675f3d9/vision/kinds.md** — 2026-08-26/27; quoted whole in
1.2 (named in sources/protos.md as b675f3d9 kinds).

**flows/04db2fd2/vision/anatomy.md** — not archived. Distilled
(04db2fd2 anatomy). Witnessed. Flow of 2026-08-27. Six entries, no
dates in the headings:

> ## Any type has an anatomy; datom [STT: datum] is a kind, not a type; realize matches the expected type with the data graph
>
> > decomposing a datum [STT: Datom] consists in the capability itself when it's implemented will match the expected kind, sorry, the expected type of datum [STT: Datom] with this data graph, which is the anatomy of a type. So, any type has an anatomy. ... a datum [STT: Datom] is a kind, not a type. Because a particular type of datum [STT: Datom]... I mean, yeah, so the datum [STT: Datom] kind will... And this possibly would open the door for trying to match different types of datum [STT: Datom], but it would be attempted against a specific datum [STT: Datom] type, which will contain the necessary data to identify its parts, to decompose it.
>
> -- psyche, STT.

> ## The real types must also be defined; a struct has its data and its anatomy
>
> > The realized types. They also have to be defined. It's like we're specifying Rust here. So there is a struct, which we have to define. And a struct has multiple sort of aspects to it. It has like, obviously, I don't know how exactly we restructured that, but there's the data itself, but there's the anatomy of that struct. So like, how many portions does it have?
>
> -- psyche, STT.

> ## The headed object: a struct of head (string), separator (an actual enum), body (another object); daisy-chained heads
>
> > the anatomy of a headed part or a headed object, maybe the right term is just object, because why not? So a headed object has the anatomy of the head, the separator, and the body, right? And then the body just becomes another object. The body is an object. The head is just a string, right? What the head actually says, like foo or foobar, you know, composable, whatever. And then the delimiter, not by delimiter, I don't mean separator probably is better. So the separator is like a period or an exclamation mark or whatever. And this is going to be a set, an enum, an actual enum. So I'm describing a struct, right? So the headed object is a struct with three parts. And the third part, the body, right? Is another object, which could be another headed object, or it could be a braced object. ... We aren't closed off to the daisy chain of heads, so to speak. So it could be like x.y.z.w. That's okay. I can see where we might actually do that. And it can be like different separators too.
>
> -- psyche, STT.

> ## A braced object has its own anatomy; almost all objects will be structs at the root; this is Protos machinery, universally applicable to all dialects
>
> > a braced object has its own anatomy, which probably almost all objects will be structs at the root. ... a lot of what I'm talking about is Protos machinery, because it's universally applicable to all the dialects.
>
> -- psyche, STT.

> ## Delineation is protos; anatomy is protos; {} count is anatomical whereas [] is not
>
> > delineation is protos. so is anatomy (unless you see a problem); the shape can be described independently of the type they represent. see if you can present this coherently, using basic principles which are universal (protos) to all the dialects; {} = nb of components is anatomical whereas for [] that isnt the case
>
> -- psyche, typed.

> ## For protos a Head is just a Head ("Anatomy, not interpretation"); pure anatomy is only structural recognition of delineations, nothing more; anatomy as tree of shapes with arity confirmed; a []-enclosed portion's anatomy must still indicate its arity
>
> > also false. for protos, a Head is just a Head, nothing more. Anatomy, not interpretation.
>
> > again, youre stepping out of protos territory. pure anatomy is only structural recognition of delineations, *nothing more*
>
> > yes, well said. the anatomy of a [] enclosed portion must still indicate its arity, which will eventually be useful somehow (pretty printers for example might want to know this, and future fancy editors)
>
> -- psyche, typed.

Note (mine): the third quote says a bracket-enclosed portion's anatomy
"must still indicate its arity"; Vision/protos.md lines 55–56 say "a
bracket-enclosed structure's arity is not" anatomical. Both are from
the same flow; listed in section 4.

**flows/04db2fd2/vision/multiPass.md** — not archived. Distilled
(04db2fd2 multiPass). Witnessed.

> ## Beginning and end are not intrinsic to objects; when textualizing they are computed
>
> > all objects will have a beginning and an end. Well, not intrinsically. ... if we're going to use that same anatomy, those same anatomy types to reverse the whole operation and textualize an actual in-memory REST type [STT: Rust type], a realized type, a real type. So that when we reverse, we're not actually going to have beginning and an end, right? So these can be, well, these can be actually, when we actually textualize, these can be computed.
>
> -- psyche, STT.

> ## Multi-pass is wanted over single pass; several sessions may be needed
>
> > basically what we're doing is a multi-pass process. We're not interested in doing everything in a single pass, because it creates a whole bunch of, I don't know, corner-cutting bad design. ... we might actually have to do several sessions to get through this properly. ... the greatest works ever written were not written in the first pass. There's just no way.
>
> -- psyche, STT.

**flows/04db2fd2/vision/portion.md** — not archived. Distilled
(04db2fd2 portion). Witnessed. Nine entries; "portion" is superseded
by "structure" (1c282d) and "Structure is really Protoform" (1c282d):

> ## "Portion" as universal term for field / variant / element; open vs closed portions
>
> > instead of saying field, right, because the concept is universal. Like, it doesn't matter if we're talking about a vector and a list of variants in an enum, fields in a struct, or other things, every object, so to speak, is a portion. So like, one of the variant in the list of the enum's variants is a portion. And every field in a struct is a portion.
>
> -- psyche, STT.

> ## Open and closed portions: bare string is open, delimited string is closed; an opened struct has its outer delimiters implied
>
> > if we say that this is an opened struct, meaning it doesn't have its outer delimiters, its outer delimiters are implied. Right, so we have a closed and an opened version, essentially, of pretty much anything. Let's take, for example, the bare string. Right, so in a position where we expect a string, we don't know necessarily beforehand if that... Block, I guess, if we could call it, or that portion, if that portion is open or closed. Meaning a bare string is essentially an open portion. It doesn't have the limiters. It's just pure payload. Whereas the limited string is a closed portion. Or, yeah, portion, I think, is good.
>
> -- psyche, STT.

> ## Suggestions asked for portion and for span
>
> > represent everything again. what is your suggestion por portion? span?
>
> -- psyche, typed.

> ## Portion is probably an enum; Headed as a variant that is a type; the ethos-types block; recursive-parsing-dependency concern; Span vs Extent
>
> > I think a Portion is an enum, but im not sure. would it be wrong for Headed to be a type (a variant of Portion)? Then we would have a bunch of qualifiers. Headed carries a struct;
> >
> > ``` ethos-types
> > Portion.[ Headed Delimited Bare ... ]
> >
> > ;; We once discussed an ethos syntax whereby the data of a data-variant is derived automatically when a variant is also another type in-scope
> > ;; like I demonstrate here with Headed. It avoids the clumsyness of doing Headed.HeadedData. The name of the contained type would be derived deterministically
> > ;; in a way that is very unlikely to create conflict. maybe something like DataOfHeadedVariant, or maybe something even more sophisticated which I cant even picture right now
> > ;; which would deal with absolute naming (module included); Protos_Portion_Headed_VariantData (I dont know what rust's position is on using _ (whatever that character is called))
> > Headed.{
> >   Name.Symbol ;; Symbol is a specific type of qualified string
> >   Separator.[ Period Exclamation Colon]
> >   Portion ;; body - not sure if it needs to be aliased - Body.Portion - Ideally we dont even need to do that. but you can push back so we can think about this out loud
> >           ;; problem; this introduces a recursive-parsing-dependency problem. So my design is either deeply flawed or I havent thought of a very clever trick.
> >   Span ;; Or Extent. I think Span sounds pretty awful
> > ```
>
> -- psyche, typed.

> ## "We don't want to imply the box, that would hide too much."; Portions as single-variant enum vs Vector<Portion> syntax; "it should be Bare.Symbol"; Extent once on portion is better; enclosed vs unenclosed, opaque a different concern
>
> > We don't want to imply the box, that would hide too much.
> >
> > Portions would be an enum with a single data variant (Portion). Did you mean Vector<Portion> ? Is that not the syntax for vectors?
> >
> > And it should be Bare.Symbol
>
> > Extent once on portion is better.
> >
> > its not enclosed vs opaque. its enclosed vs something like "unenclosed" - opaque is a different concern
>
> -- psyche, typed.

> ## Portions exist inside portions; the box is not objected to
>
> > Headed lost its Portion member?
>
> > problem is portions exist inside portions
>
> > I didnt say anything against the box
>
> -- psyche, typed.

> ## opaque is opaque; no containing portion
>
> > opaque is opaque; no containing portion.
>
> -- psyche, typed.

> ## A non-opaque enclosed portion holds a vector of possible inner portions
>
> > an enclosed portion has an unknown number (vector) of possible inner portions
>
> > non-opaque enclosed*
>
> -- psyche, typed.

> ## Form and Anatomy are not two types
>
> > Why do you think you need two types, Form and Anatomy?
>
> -- psyche, typed.

**flows/04db2fd2/vision/delimiters.md** — not archived. Distilled
(04db2fd2 delimiters). Witnessed. One entry, three typed quotes; the
first is the only earlier record on the guillemet glyph:

> ## Guillemets vs double angle bracket pair; curved quotes are an asymmetric pair, not double quotes; needs a refresh on delimiter names; parentheses not universal yet, not protos; content-opaque until unbalanced closing parenthesis; anatomical features inside do not trigger delineation
>
> > this is false; you are talking about guillements, and what you showed is a double angle bracket pair
>
> > also false. curved quotes are an asymetric pair of characters, youre showing double quotes (or whatever theyre called; I need a refresh on names of delimiters)
>
> > that's not univeral yet. so not protos. what we can say is it's content-opaque, so all characters it contains are ignored, until the closing unbalanced closing parenthesis. so is can contain any protos anatomical features, but none of them will trigger any delineation for now.
>
> -- psyche, typed.

Note (mine): the third quote says parentheses are "not univeral yet.
so not protos"; Vision/protos.md lines 44–47 count parentheses among
the six protos delimiter pairs, "read by balance". Listed in section 4.

**flows/04db2fd2/vision/delineate.md** — not archived. Undistilled.
Witnessed.

> ## Prospective<Datom> is Delineatable
>
> > Re Delineate: Yes! That's what I was looking for. So a Prospective<Datom> is Delineatable (however this is spelled, or however you think we could word that kind)
>
> -- psyche, typed.

> ## Delineation is protos
>
> > delineation is protos.
>
> -- psyche, typed.

"Delineatable" is superseded by e8c4cc61's "Delineatable is better
expressed as Structural" and then by 1c282d's Protosizable, which the
landed Layers table carries; "delineation is protos" is carried by
the Delineation section.

**flows/04db2fd2/vision/text.md**, **textualTypes.md**,
**directionAsymmetry.md** — quoted whole in 1.3; named in
sources/datom.md, not in sources/protos.md, though Direction carries
directionAsymmetry.

**flows/04db2fd2/vision/decomposable.md** — not archived. Undistilled.
Witnessed. Two STT entries:

> ## The Decomposable kind: decomposes into composable kinds; composing regenerates the instance
>
> > here's a kind. A kind decomposable. ... if something is decomposable, it's decomposable into composable kinds. And then we get the reverse behavior, where if all of the composing parts, the composable parts of a decomposable kind, are put together in the right order, then we can re-obtain... We can regenerate the actual instance of this decomposable kind from the composable parts.
>
> -- psyche, STT.

> ## Maybe not decompose/compose but finding the keyframes; positions as line/column or rope theory; "annotate" rejected
>
> > maybe the abstraction is not decomposable and composable, but like it's not that we're not decomposing it, but we're annotating it. But that word is not annotate. It's like where we find like when people are doing a video editing job, they find the frames, like the cutoff frames, they find all the key frames where like either cuts are going to happen or like music transition will happen or something like the important moments, which are for datum [STT: Datom], the beginning and end of all the portions. And a sort of rough idea of not just the beginning and end, but the anatomy of it. So like here we have a head, right? So it's not strictly typed yet. Like we have a step where we just describe the structure of the datum [STT: Datom]. So like here begins a braced portion. And so it's going to be essentially, I guess, line and column or column and line numbers when we're talking about text or whatever. You can do some research there. I've heard about these editors that use rope theory or something. I don't know how that works. Maybe that's better. But it's going to say like beginning from here, ending here, we have a braced portion or a headed or yeah.
>
> -- psyche, STT.

**flows/04db2fd2/vision/kinds.md** — 2026-08-27/28; quoted whole in
1.2 (named in sources/ethos.md as 04db2fd2 kinds; not in
sources/protos.md). Its "Kinds as verbs are not allowed …
Delineatable or Delineated … Textualized … Realized reconsidered" and
"I think Embodied is the right term, unless Forged is better" bear on
the protos kinds.

**flows/2ef42163/vision/kinds.md** — not archived. Distilled (2ef42163
kinds). Witnessed. Flow of 2026-08-28. Nine entries, no dates in the
headings:

> ## real/realize is changed; the debate is embody/embodied or forge/forged
>
> The flow's high-level view named the text-to-value direction "realize". The psyche corrected it:
>
> > real/realize is changed. debate was on embody/embodied or forge/forged
>
> -- psyche, typed.

> ## embody
>
> > embody.
>
> -- psyche, typed.

> ## text isn't textual; the embodied type is — textualizable reconsidered
>
> > text isn't textual; the embodied type is. so this brings back the debate of textualizable being a better fit
>
> -- psyche, typed.

> ## Text is embodiable, and the Embodied is Textualizable
>
> > you still don't get it. Text is embodiable, and the Embodied is Textualizable
>
> -- psyche, typed.

> ## it would be delineatable right?
>
> > what is Lock?
> >
> > it would be delineatable right?
>
> -- psyche, typed. (Asked as a question; the flow reads it as the embodied type also bearing delineation, and the -able form of the kind name.)

> ## Embodied a type
>
> > and Embodied a type.
>
> -- psyche, typed.

> ## there's no Embodied; embody returns the actual type, which implements Embodiable
>
> > Actually, I don't even know if embodied is anything at all because when you run the capability of an embodiable kind, then what you get is self. Because now it's embodied. It just returns the actual type, which implements embodiable. So there's no embodied. It's just really when we say embodied, where it's kind of a vocabulary to talk about the actual Rust type when it's been cast into its Rust form. It's Rust memory form.
>
> STT corrections made in the quote: "returns to actual type" → "returns the actual type"; "rest" (three times) → "Rust"; "casted" → "cast". The psyche corrected the transcription in the same message ("I said R USD. R USD. No. T like tango." — Rust). The quote first stood with "rest" in it; corrected in place on the psyche's ruling (vision/psycheLogging.md).
>
> -- psyche, STT.

> ## bearer? you mean Self?
>
> > bearer? you mean Self?
>
> -- psyche, typed. (Asked as a question; the flow reads it as Self being the word in ethos as in Rust.)

> ## Embodied is a kind after all; the final Rust type implements it, and embody returns it
>
> > Oh, no. You're right. I made a mistake because the type we're passing into the embody function is not actually what we're trying to get. So I made a mental mistake there. So I guess you would need another kind. Like you said, embodied, which is the actual embodied type, the final Rust language type would implement embodied, and that's what embodiable, uh, the capability the embody would return.
>
> STT corrections made in the quote: "the the" → "the" (twice); "rust language" → "Rust language".
>
> -- psyche, STT.

"embody" (2026-08-28) is superseded by 62022e8f's "incorporate is the
capability of the corporal" and 6329f1's "change 'realizing' to
'incorporating'"; the landed Layers table has incorporate and no
embody.

**flows/db97561c/vision/prospective.md** — not archived. Undistilled.
Witnessed. Flow of 2026-08-28. Four typed entries:

> ## Prospective<Embodied>.Text is wrong
>
> Context: the flow's corrective prompt (reports/mapSyntaxCorrection.md) declared `Prospective<Embodied>.Text` as a newtype over Text with a kind position; the Codex flow picked it up.
>
> > codex is talking about Prospective<Embodied>.Text
> > which is totally wrong.
>
> -- psyche, typed.

> ## Prospective<Embodied> is a kind
>
> > I see Prospective<Embodied> as a kind. do you?
>
> -- psyche, typed.

> ## Prospective<Lock> is skipping steps
>
> Context: the flow wrote that the kind's position is filled at the use with a type — `Prospective<Lock>` as text taken as a would-be Lock.
>
> > Prospective<Lock> is skipping steps
>
> -- psyche, typed.

> ## Prospective<Protos> comes first; Protos is a type
>
> Context: the flow asked what the step out of `Prospective<Datomic>` yields.
>
> > `Prospective<Protos>` is needed first. Protos is a type which contains the portions and their protosic anatomy
>
> -- psyche, typed.

**flows/e8c4cc61/vision/protos.md** — not archived. Distilled (e8c4cc61
protos). Witnessed. Flow of 2026-08-29.

> ## Structure is a better Portion
>
> Context: the Datomizable page (second reading) proposed a `Structure`
> type — Bare, Enclosed.{Enclosure Arity}, Headed.{Head Separator Body},
> Opaque, Shaped — as the answer a type gives about its own text.
>
> > your Structure is a better Portion (better name anyway)
>
> -- psyche, typed.

> ## Delineatable is better expressed as Structural
>
> > and Delineatable is better expressed as Structural.
>
> -- psyche, typed.

**flows/e8c4cc61/vision/prospective.md** — not archived. Distilled
(e8c4cc61 prospective). Witnessed. Six entries; the STT ones carry the
anatomical survey that the Delineation section distils, and "Multiple
steps are not feared" is the Multi-pass section's second sentence
nearly word for word:

> ## The capability of a prospective kind is prospect
>
> Context: db97561c had left open whether the capability at every
> Prospective stage is `embody` or `delineate` at the first stage.
>
> > I want to actually also specify the capability. So for any prospective kind, so a prospective protos uses the capability prospect, which is to look forward, right, to see if it's a sort of... Yeah, it's a prospect, literally.
>
> -- psyche, STT.

> ## Prospective<Protos> is an anatomical survey only
>
> > And we read before reading and find all of the anatomy of the protosic anatomy, which is not specific. It's just an anatomical survey. Like here we have a headed portion. It doesn't go into any detail as to what these things actually mean in terms of the dialect. So we don't know if it's a datom [STT: datum]. We don't know if it's an ethos. We don't know if it's later a nomos or a logos. We just know that once the prospect goes through and is successful, we just know that we have a protos object.
>
> -- psyche, STT.

> ## The dialect prospects are implemented on the Protos type
>
> > And so that can be then passed on to a further capability, like in datom [STT: datum] or in ethos, you would have a prospective datom [STT: datum] or a prospective ethos. And when we're talking about ethos having different headers that differentiate between them, it's because we wouldn't know from the file name or whatever. So there would be a bit of an unknown as to what kind of specific type of ethos object we're reading.
> >
> > The prospective ethos would actually sort that out by obtaining the type name. And also it could verify that the version of that type is compatible with its runtime. And then it would verify that anatomically at the root, this corresponds as well.
> >
> > ... So when we go from a protos, right, we implement prospective datom [STT: datum] or prospective ethos on the protos type. And that's how the reader then proceeds to try to prospect the protos into a datom [STT: datum].
> >
> > And again, the only thing that the prospect would do is verify that the object corresponds anatomically as a datom [STT: datum] or as an ethos of the particular type that is specified in the header of an ethos type.
>
> -- psyche, STT.

> ## The type embodied into is not known until later passes
>
> > so this introduces the concept that we don't quite know what type we're embodying into until later into the reading passes.
>
> -- psyche, STT.

> ## Multiple steps are not feared
>
> > So we're not scared to do multiple steps. The multiple steps create a mental model of the machinery, which enforces a correctness in the code that is millions of times more beneficial than the cost of doing these multiple passes over doing a sort of mud ball of code that just speeds through everything and becomes impossible to refactor and redesign later on.
>
> -- psyche, STT.

> ## Prospective<Ethos> is borne by the Protos type and yields an Ethos
>
> > Ethos would have a Prospective<Ethos> kind which is Protos type bears. Calling the prospect capability on it would yield an Ethos which needs to have its anatomy designed
>
> -- psyche, typed.

"Prospective" and "prospect" are superseded by "potential" and
"actualize" (62022e8f, 1c282d, 6329f1).

**flows/e8c4cc61/vision/kinds.md** — 2026-08-29; quoted whole in 1.2
(named in sources/protos.md as e8c4cc61 kinds). Its "Structural's
capability returns the protos structure, recursively", "Prospective<Sized>",
"yes on situation. yes on Embodied", "Embodied is an alias of Sized"
are the protos-bearing entries.

**flows/62022e8f/vision/kinds.md** — not archived. Distilled (62022e8f
kinds). Witnessed. Flow of 2026-08-30. Five entries, no dates in the
headings; the source of Potential/actualize, Corporal, and incorporate:

> ## Embodied implies it already is; switch Prospective to Potential; the capability name is open
>
> > I think naming the kinds is really tricky because if I say embodied or incorporated, it is kind of implying that it already is. When in fact we're talking about a future thing in terms of that point and in the process, you're using the word Prospective [STT: perspective]. I want to switch to potential, which I don't know how to call the capability for that, but let's say, I don't know, "express the potential." You help me here on the terminology.
>
> -- psyche, STT.

> ## Potential and actualize, universally, layer to layer; Embodied is the bound; Corporal is kept for the layer
>
> Context: artifact comment on the Protos Layers page, anchored at pass 2;
> the page had asked for the bound at the potential position.
>
> > One, I prefer the terminology potential and actualized over Prospective [STT: perspective] and prospect. And that is the kind that I want to use universally to go from one layer to the next. It's more of a rewording on Rust's [STT: RESTS] TryInto. And I think the embodied is probably better because then we keep the corporal for... And this answers your third question. We keep corporal for the layer concept.
>
> -- psyche, STT.

> ## The layer capabilities sit on the layer above: structure on Text, conceive on Structure, incorporate on Concept; each layer kind is an alias of a Potential
>
> Context: artifact comment on the terminology table (structure / conceive / embody for Structural / Conceptual / Corporal).
>
> > So I'm looking at the capabilities here, structure, conceive, embody, for these kinds, structural, conceptual, corporal. Actually, it would be incorporate, that's fine. We can use the word incorporate because the context is clear. We're not talking about forming a legal corporation. So, yeah, the structural kind, like the structural capability, if we want to say that, or the capability, the structure capability would be on text and the conceive capability would be on structure and the incorporate capability would be on concept. Otherwise, these capabilities don't really mean anything. So, I guess in a way, these are placeholders for the potential actualize into, or am I wrong here? Because if we call a structure on text, what we get is a structure. It seems to me, anyway. So we would be creating a kind, just a specific name instead of saying potential structure, I mean potential structural. No, actually, that wouldn't work. Potential structure. So structural would be the type in the structural layer and concept would be the type in the conceptual layer and the corpus would be the type in the corporal layer. Right?
> >
> > In other words, it seems that the structural kind is potentially just an alias on a potential structure.
>
> -- psyche, STT.

> ## All chosen names agreed; incorporate is the corporal capability; embody is the general word for reaching the layer below
>
> Context: same table, five minutes later.
>
> > So I agree with all of the chosen names here except incorporate is the capability of the corporal, because then embody becomes a general term to talk about, like when a structure embodies as a concept, right? So to embody a structure means we get a concept. To embody any layer means we get the layer below. And then we could come up with a term to talk about the other direction.
>
> -- psyche, STT.

> ## Datomizable narrows too explicitly to datom: ProtoShaped, ProtoFormed, ProtoExpressible, ProtoTextualizable; protoform
>
> > ProtoShaped? ProtoFormed? ProtoExpressible? ProtoTextualizable?
> >
> > Saying Datomizable narrows it too explicitely to datom which could be confusing.
>
> -- psyche, typed (artifact comment).
>
> > Maybe there's like an actual word here that like is proto, maybe it's a prototype or proto form. It's kind of cool sounding actually.
>
> -- psyche, STT (same comment).

Supersession within this topic: "the structure capability would be on
text and the conceive capability would be on structure and the
incorporate capability would be on concept" (one direction, on the
layer above) is superseded by 6329f1's "both the text and the concept
are protosizable, just like the corporal and the protoform are
conceivable. For the middle layers, both the type above and below"
(both ways), which the landed Layers table carries. "Embodied is the
bound" is superseded by 6329f1's "drop Embodied; stick with Sized".
"embody becomes a general term … to embody any layer means we get the
layer below" is not carried by the landed text, which uses actualize
for layer to layer and incorporate for the corporal layer; listed in
section 4.

**flows/62022e8f/vision/layers.md** — not archived. Distilled
(62022e8f layers). Witnessed.

> ## The concept layer is the Datom and Ethos types of the settled chain
>
> Context: artifact comment anchored at the page's first ruling asked —
> "Is the concept layer the Datom and Ethos types of the settled chain?"
>
> > yes
>
> -- psyche, typed.

> ## Ethos also has a Corporal layer, from which the generated Rust is yielded
>
> Context: artifact comment anchored at the chain block
> `Ethos.[ Potential<RustSource> ]`.
>
> > Ethos would also have a Corporal layer, which is the layer that would then be used to yield the generated rust.
>
> -- psyche, typed.

**flows/62022e8f/vision/concept.md** — not archived. Distilled
(62022e8f concept). Witnessed. Five STT entries:

> ## A concept is an abstract object; a type is not an object yet; these are all concepts
>
> > No, no, the concept. What I was considering is that a concept is an object, basically, because there's an abstract object, like a concept, and a type is not really an object per se yet. It's not an instance of a type. These are all concepts.
>
> -- psyche, STT.

> ## Everything in a protos dialect has a conceptual aspect; the conceptual form and the corporal form, the corporal form being final
>
> > Also, anything that is represented in any protos [STT: proto's] dialect has a conceptual aspect. Even in datom [STT: datum], you're going to have a first layer, which is not exactly what... Okay, so there we go: we have the conceptual form and the corporal form, and the corporal form is the final form.
>
> -- psyche, STT.

> ## The first pass of a datom yields the concept of an enum, not the Rust type
>
> > When a datom [STT: datum] comes in, that is supposed to be in, let's say, a data-carrying enum, an enum with a struct in it. First, on the first pass, the conceptual representation of that won't be the Rust [STT: rest] type itself that this is being cast into. It'll be a vector. We're going to have this concept of what an enum is, basically. It's going to be represented as this: this is an enum, a variant of an enum with a variant name X and a payload of such and such, which is really just a reference to another concept.
>
> -- psyche, STT.

> ## The concept is the anatomical layer of Protos, and more; the psyche is still sorting it out
>
> The psyche marks this as unsettled in their own words.
>
> > The concept is the anatomical layer of Protos, and also it's more than that. I'm not sure. I'm confusing myself now, and I'm not sure what I want yet. I'm sort of just sorting it out as I see it, and I see how you present it.
>
> -- psyche, STT.

> ## The kind declaration with varying arity is one layer, the conceptual one; the corporal side is the other
>
> > But I have to say that what you were presenting as the kind declaration with different arity is not wrong at all. It's one layer of it. There are these multiple layers, and we get confused because one of us thinks that the other is talking about a certain layer, when in fact he's talking about a different layer. I'm trying to juggle all these layers in my mind and express them coherently, which is why we need different terms for concepts that, on the surface, appear to be the same but actually apply to different layers of abstraction.
> >
> > This is why I'm saying we have at least two passes, if not three:
> > - At one layer, which is the kind declaration layer, you have this very varying arity. This is, I guess you would say, conceptual.
> > - You have the corporal side, which is why we're embodied, and would become maybe not incorporated because it has all kinds of different meanings also.
>
> -- psyche, STT.

**flows/62022e8f/vision/passes.md** — not archived. Distilled
(62022e8f passes). Witnessed.

> ## The process view: the file comes in, is read as such, then a capability is called recursively
>
> > As I see it, we need to look more into what this looks like in terms of the actual process: the file comes in, and it's read as such. Then such-and-such capability is called on this object, which recursively calls such-and-such capability on all of its containing objects, sections, or structures, or shapes.
>
> -- psyche, STT.

**flows/62022e8f/vision/vocabulary.md** — not archived. Distilled
(62022e8f vocabulary). Witnessed. Three STT entries:

> ## The vocabulary must serve the spoken word; the visual side assists
>
> > We have to decide on the vocabulary so that we can create a consistent way of talking about this using the spoken word, which is becoming the new medium of exchange. The visual side is an assistant, and the eye, until at least until I get a drawing tablet, is my easiest-to-reach method of expressing myself for the lowest cost to myself. Essentially, in technical terms, not because of the nature of things, just because of the nature of the tools I have
>
> -- psyche, STT.

> ## Struct is never said; the struct aspect is described using structure
>
> Context: the flow's ethos spec had written `Struct.Vector<Portion>`.
>
> > I see you have an example there that says "struct [STT: struck] that vector." We wouldn't actually ever say "struct [STT: struck]." This form has to be absolutely killed with the most powerful poison in the universe and burnt, and that soil has to be salted. All of its descendants have to be eradicated. Is it a plague that should never show its face ever again on the surface of the earth?
> >
> > The struct aspect is described using structure. Dig it out with the root, and then dig out 3 ft. of dirt behind the root. Make sure it never is ever seen again anywhere in the universe.
>
> -- psyche, STT.

> ## The speech engine writes REST for RUST
>
> > Maybe the speech detection engine sometimes wrote "REST" when in fact I meant "RUST", so you'll have to correct for that.
>
> -- psyche, STT.

Note (mine): "We wouldn't actually ever say 'struct'" was said of a
protos type named `Struct`; Vision/datom.md's Syntax uses "struct" for
what a brace structure means in datom ("A brace structure is a struct")
and Vision/ethos.md's Types section says "A struct is a headed brace".
Whether the ruling reaches those uses is not settled here.

**flows/62022e8f/vision/headedAndContained.md**, **symbols.md** —
quoted in 1.3 (named in sources/datom.md).

**flows/62022e8f/vision/multiFormConcepts.md** — not archived.
Undistilled. Witnessed.

> ## A concept written at different arities, fields omitted by arity: a simple and a complex form
>
> Context: the kind declaration had a simple `Kind.[ … ]` and a complex
> `Kind.{ [] [] [] [] }` form.
>
> > I want to flesh out this concept. This has been talked about before, but maybe just flesh out this concept of multi-form concepts. I really like the word concept for how we've been taught what we've been calling an embodied or an embodiment concept. Anyway, in ethos, I'd like to flesh out this idea of multi-form concepts.
> >
> > You would have this multi-form concept where it's struct [STT: struck] with a different number of a different arity. It would just be the same concept, but some of the fields can be omitted [STT: emitted] depending on which arity is being used. That way, we have a simple form and a complex form without having to always write out all the fields, even if they're empty.
>
> -- psyche, STT.

The landed Kinds section carries the simple (bracket) and complex
(brace) kind forms without naming the multi-form concept.

**flows/62022e8f/notion/layerMatching.md** — **notion**, not archived.
Undistilled. Witnessed. Four STT entries; the living marks the first a
notion: "this is sort of a notion that we need to crystallize before
it really becomes a vision. So brainstorm with me on this and on the
terminology as well." The first entry is a long artifact comment
ending mid-sentence; its closing lines:

> > […] So we would go, okay, so here's the context, and I don't know if that's the right term yet. We use the word situation, but I think that context is still better, even though it might not be the ultimate best term yet. But the context would then... We would ask for a capability that would be on all of the concepts that we're trying to match... We're trying to match the structures in this context on the right concepts in the conceptual layer. But we don't have... The notion would be that we don't maintain this separate data structure apart from all of the embodiments in the conceptual layer. So all of the data essentially lives in the capabilities. So we need to create this match
>
> -- psyche, STT.

> ## The match: context is a variant; walk the roster; match on context and structure; a compile-time check that no context has conflicting structures
>
> > Well, now that I'm reading this and what you're writing, it's actually maybe really simple. The match just comes in with the context, which is just a variant, and it just, you know, goes through the whole roster [STT: roaster], and the match has to be on both the context and the structure. And if we have, like I said in the other comment, if we have this compile time check that makes sure that no one context has conflicting structure, then we're always going to get the right match if we just do it that way. But maybe you have a better way, so please show me the options if you think that we have them.
>
> -- psyche, STT.

The third entry (compile-time check; multi-form going up; "Think,
you know, elegance. Think separation of concern. Don't try and make
things efficient. Try and make them easy to reason about.") and the
fourth ("The ethos roster: every concept type — declarations,
associations, the roots, and the inner things") are STT.

**flows/62022e8f/notion/terminology.md** — **notion**, not archived.
Undistilled. Witnessed.

> ## Corporal for Embodiment; concept; "the perspective is actually the better term"
>
> The psyche invites a brainstorm on all the terminology; these are the
> candidates floated in the same message. The last sentence's
> transcription is uncertain.
>
> > One is an Embodiment, or I was even thinking of going from Embodiment, which is a bit of a wonky term, to Corporal, which is more of a Latin-based version of the same thing. A Corporal symbol, I guess you could say.
> >
> > I really like the word concept for how we've been taught what we've been calling an embodied or an embodiment concept. ... I think it's not even corporal, it's conceptual, and the perspective is actually the better term. I want you to even just rethink a lot of our terminology here and brainstorm with me on all of the terminology.
>
> -- psyche, STT.

**flows/995a164e/vision/concept.md** — not archived. Undistilled.
Witnessed. Flow of 2026-09-01.

> ## The concept-layer datom shapes: would those be the variants of ethos:Concepts? make the layer explicit
>
> Context: artifact comment on the recap's contained-form example, `Variant.{ GenerationFailure … }` (2026-08-31 11:11).
>
> > Would those be the variants of ethos:Concepts?
> >
> > We should make that clear. That way we know exactly what layer we're on.
>
> -- psyche, typed (artifact comment).

> ## The layer enum is Concept, singular
>
> > that should be Concept. singular. right? that code block makes it obvious
>
> -- psyche, typed.

**flows/995a164e/vision/kinds.md** — not archived. Undistilled.
Witnessed. Three entries, typed (artifact comments):

> ## Name could be a capability of Conceptual
>
> > name could perhaps be a capability of Conceptual

> ## Associated kinds, associated values: did you mean associated types? why not constants?
>
> > What's an associated kind? Russ [typed; Rust] doesn't have associated traits, so did you mean associated types?
>
> > Why values? What's wrong with constants?

> ## Protoformed is too close in speech to protoform; protosic, protoformal, or else; where does this logic sit in the engine?
>
> > This is logic that sits between the structural layer and the conceptual layer? If Express capability of Protoform returns something, it would be a protoform. I think we need different terms here because the adjective "protoformed" is difficult to distinguish in speech from the noun "protoform". Maybe the kind is "protosic" or "protoformal", or maybe something else. You can make suggestions, and I need to better understand conceptually where this stands. Where does this logic fit in the engine?

"protosic"/"protoformal" is superseded by 1c282d's "protosizable!".

**flows/995a164e/vision/layerMatching.md** — not archived.
Undistilled. Witnessed. Three entries on the structure-to-concept
match; the second and third:

> ## "The data is in the capabilities" means the trait implementations, and only them; no constant
>
> > When I say the data is in the capabilities, you don't really understand that I just mean the trait implementations, right? That is the only thing that is involved in obtaining that data. There's no constant. There's not gonna be a constant. You're completely missing my point. You're actually making the parallel data structure that essentially repeats the data that would already be, or that must be, in the capabilities. It's specific to these embodiments, and therefore it must live in their capabilities.
>
> -- psyche, STT.

> ## Unstable Rust is fine; the check is at compilation, not generation; an associated constant in each kind holds its forms; think in an actual type, even a throwaway instance
>
> > Okay, you say that stable Rust doesn't allow calling trait methods during constant evaluation. Well, I don't really care about stable Rust, so we can use unstable Rust if that fixes it, but I'm not sure I even believe you. Maybe you don't really understand what I want.
> >
> > Obviously, you can't call traits directly. You need a type to call the methods on. You need to think about it in terms of using an actual type and an actual instance of a type, I guess. Even if it's just a temporary throwaway instance to run this check during compilation, we're going to find a way. I know we're going to find a way, even if it's from generating the rest [STT; Rust] from ethos, where we had a kind of check somewhere in the logic there, but I would leave that for last resort.
> >
> > No conflict should be done at compilation, not at generation. There's no reason to do it at generation. It's kind of ridiculous because we have a limited set. This conflict can be checked without actually feeding any ethos to generate from. It's going to be in the logic of the length of the runtime [transcription uncertain] whether or not there's a conflict, so we shouldn't postpone the conflict check until we're running the execute code. That's absurd.
> >
> > There is going to be an associated constant, possibly in each kind, to hold the value of its forms or whatever it is.
>
> -- psyche, STT.

The first entry ("Somehow, you didn't understand what I meant at all
here. By merely putting a constant roster …"; the living stopped
reading the report there) is typed.

**flows/e4a40e/vision/protos.md** — not archived. Distilled (e4a40e
protos). Witnessed. The source of "What Protos knows":

> ## 2026-09-03 — protos is only about structure; it wouldn't know what anything is
>
> The flow had presented protos blocks with ethos library examples,
> including a block on struct, vector and angle brackets.
>
> > it's wrong right off the bat because it's showing the ethos, and you're saying this is going into protos. Protos is only about structure. It has nothing to do with `struct` and `vector`, and it only understands form, so it's only a very abstract structure, like the syntactic structure. It wouldn't know what anything is.
> >
> > You have to understand that we're talking about the anatomy of the text. This is a headed, bracketed component, or whatever we're designing to call it. Nowadays, structure and nothing else, it wouldn't know. We wouldn't use an ethos syntax for an example because it would be confusing later on.
> >
> > Whatever you're showing me that's ethos needs to go in an ethos vision distillation. If you want to do protos, it has to be very much universal, explaining this: the textual structure, the approach to how we structure things textually, with the delimiters, the head, the capitalization, and the recursive structure, like a structure contains another one and so on, some very, very high-level, non-dialect-specific stuff. We don't necessarily need to distill that if you don't actually understand protos. We could talk about protos later.
>
> -- psyche, STT.

**flows/e4a40e/vision/archive-datom.md** — 2026-09-03, "a certain
subset of text qualifies as a head"; "Yes, 'structure' is the right
word"; quoted whole in 1.3.

**flows/1c282d/vision/protosizable.md** — not archived. Distilled
(1c282d protosizable). Witnessed. Flow of 2026-09-04 (02:25); no
dates in the headings:

> ## The form is protos; the kind is Protosizable
>
> > ethos isnt datom-expressible. the form is protos. I think protosic is the right kind. `type.protosize() -> protoform` - does that make sense. flesh the fuck out of that for me, with the ethos spec of it all and ascii visuals
>
> — psyche, typed.
>
> > protosizable!
>
> — psyche, typed. (Correcting the kind name from "protosic" to "protosizable".)

> ## The association: Concept bears Protosizable
>
> > ethos:Concept.[ Protosizable]
>
> — psyche, typed. (The ethos Concept type bears the Protosizable kind.)

> ## Structure is really Protoform
>
> > looks like Structure is really Protoform.
>
> — psyche, typed. (The type currently called Structure/Portion in protos — Headed/Enclosed/Bare — is a Protoform. Not a separate type alongside it.)

**flows/1c282d/vision/vocabulary.md** — quoted in 1.4 ("potential";
"structure").

**flows/ad19b1/vision/ethos.md** — 2026-09-04 02:13, "space the
delimiters and the inner content" (named in sources/protos.md as
ad19b1 ethos; carried by Canonical print). Quoted in 1.2 and 3.f.

**flows/6329f1/vision/archive-protos.md** — archived ("distilled into
Vision/protos.md (Direction, Structure, Delineation, Layers), flow
6329f1, 2026-09-04"). Distilled (6329f1 protos). Witnessed whole:

> ## 2026-09-04 — the maximal run part is not understood; take it out
>
> On the proposed sentence "A bare structure has no delimiters: a maximal run.":
>
> > I don't understand this maximal run part. I think just take it out unless there's something there that is valid that you failed to express properly.
>
> -- psyche, STT.

> ## 2026-09-04 — text and concept are protosizable; corporal and protoform are conceivable; both ways for the middle layers
>
> On the proposed layers table, which put protosize on Concept only:
>
> > Well, it seems to me that both the text and the concept are protosizable, just like the corpus [STT: corporal] and the protoform are conceivable. For the middle layers, both the type above and below can be changed into that type because we can go both ways.
>
> -- psyche, STT.

> ## 2026-09-04 — realizing becomes incorporating, since the layer is corporal; incorporate on text daisy-chains
>
> > I also think that, to be consistent, since we're saying that to texturize [STT: textualize] is to go to the text layer, we should also say that we should change "realizing" to "incorporating" because the layer is called the corpus [STT: corporal]. That would be a more appropriate and consistent way to express that.
> >
> > Essentially, the text could be corporal, right? Calling "incorporate" on the text would essentially just daisy-chain through "protosize," and then it would conceive, and then it would incorporate the concept. Unless you see a problem with that logic, if you don't, then that's how I would word it, because then we get consistency of vocabulary.
>
> -- psyche, STT.

> ## 2026-09-04 — actualize on a potential yields its target; where does delineate fit; is a layer missing
>
> On the proposed sentence "actualize on a Potential is delineate, then conceive, then incorporate":
>
> > When you say "actualize on a potential is delineate," that is not true because potential is wet [STT: unclear; the sense that follows is that a Potential is typed by its target], right? A potential peritaform [STT: Protoform] that is actualized yields a peritaform [STT: Protoform], and I'm not sure where the delineate here is actually going to fit, unless you think there's a layer between text and perdaform [STT: Protoform], which is wet [STT: unclear], delineated text. Are we missing a layer here?
>
> -- psyche, STT. (Asked as a question.)

> ## 2026-09-04 — drop Embodied; stick with Sized
>
> On the proposed sentence "Embodied is the bound, an alias of Sized, borne by every corporal type":
>
> > You say "embodied" is the bound an alias of "sized" and "born [STT: borne] by every corporate [STT: corporal] type." Although I kind of understand what you're saying, I also see that it's just confusing. I think I want to drop "embodied" and just stick with the rest: "sized," because, first of all, it's not that much better than "sized" cognitively, and it seems to have confused you because that sentence is actually quite fuzzy and confusing.
>
> -- psyche, STT.

The question "Are we missing a layer here?" is answered by e996e8's
"no layer. your answer is good" below.

**flows/ad19b1/vision/protos.md** — not archived. **Undistilled**.
2026-09-04 21:06. Witnessed; quoted whole in section 3. The latest
protos ruling: "ok lets drop that delimiter and concept entirely from
protos and its dialects."

**flows/e996e8/vision/protos.md** — not archived. **Undistilled**.
2026-09-04, after 6329f1's landing. Witnessed whole:

> ## 2026-09-04 — no layer between Text and Protoform; the flow's answer stands
>
> On the flow's question whether a layer is missing between Text and Protoform (the flow had answered no: protosize on text is the delineation):
>
> > no layer. your answer is good
>
> -- psyche, typed.

> ## 2026-09-04 — Incorporable could replace Corporal; is corporate a word?
>
> On the layers table's incorporate row, which names no kind (the flow had offered Incorporable):
>
> > Incorporable could replace Corporal. Is corporate a word? Corporal/corporate Incorporable/incorporate ?
>
> -- psyche, typed. (Asked as a question.)

> ## 2026-09-04 — the key-value map delimiters are abandoned everywhere
>
> > You might want to check out recent flows. I've been talking about these topics and [STT: in] other flows, and we've abandoned the key value map limiters [STT: delimiters] everywhere. We're sort of stripping some stuff out now, and now I'm dropping the version.
>
> -- psyche, STT.

**vision-raw/protosIsTheSharedStyle.md** — title only ("# Protos is
the style all our dialects share"), no entries (relayed).

### 1.2 Ethos

#### Distilled state

**Vision/ethos.md** (witnessed whole, 285 lines). Sections: What Ethos
is; Why Ethos; Generation; Non-repetition; Self-description; Horizon
(these six landed by flow 68512643, commit c2a0223b6, 2026-08-24);
Kind; Naming; Identity (landed by flow ad19b1, commit c2ac4cdb2,
2026-09-04 01:58:51 +0200, which also folded Vision/kinds.md into
ethos); Declaration with subsections File, Imports, Types, Kinds,
Associations, Spacing (appended by flow 6329f1, commit 23aaf7a7f,
2026-09-04 17:14:39 +0200). Landing flows and dates are from git
history, witnessed; the file itself names none.

**Vision/sources/ethos.md** (witnessed whole, 34 entries): 01a02a34
ethos, schemaSyntax; vision-raw ethosDotosDivisionAndHelp,
ethosNonRepetitionLaw; f426777b spokenVocabulary; b675f3d9 kinds;
6863ef19, 06196cc7, 2b34fafa traitsAsCapabilities; 04db2fd2 kinds;
5abf3be8 encodedFormFingerprintTraitDesign; 4decf7 kinds; 2ef42163
ethos; e8c4cc61 kinds; b675f3d9 structuralParsing; ac1e9ec8
datomSyntax; e4a40e kinds; ad19b1 kinds; e8c4cc61 ethosFileAnatomy,
kinds; 995a164e ethosTypes; 62022e8f ethosTypes; aa4c7747
interactions, tuples, ethosTraitSyntax; 2b34fafa ethosSourceFiles,
ethosNamespaces; b675f3d9 kinds, structuralParsing; ad19b1 ethos,
designPractice; 6329f1 ethos.

**Vision/ethosMonolith.md** exists with its own sources file; not
read for this report beyond its listing.

**Intent/mandatoryTraits.md** (relayed): approved 2026-08-13, session
d2bb5f5f; every method call lives under a trait; traits are the
comprehension surface; Rust is the new assembly.

The landed Declaration on the map question, witnessed, Vision/ethos.md:

```
   153	A struct is a headed brace — the name, a dot, and braces holding its
   154	positions in order. An enum is a headed bracket — the name, a dot,
   155	and brackets holding its variants. An alias is a headed bare — the
   156	name, a dot, and the aliased type. A map is a headed guillemet — the
   157	name, a dot, and guillemets holding the key type and the value type.
```
```
   162	[ Record.{ Text Integer }
   163	  Report.{ Text Vector<Integer> }
   164	  SinkError.[ Closed Full ]
   165	  LockId.Integer
   166	  Roles.« Text Integer » ]
```
```
   174	pub type Roles = std::collections::BTreeMap<protos::Text, protos::Integer>;
```
```
   234	A complex kind opens with a brace after the dot. Inside: superkinds
   235	in a bracket, associated types with their constraints in a bracket,
   236	associated constants in a guillemet — upper case, in the map
   237	delimiter — and capabilities in a bracket.
```
```
   239	[ Streamable.{ [ Fillable ]
   240	               [ Item<Serializable> ]
   241	               « CAPACITY Integer »
   242	               [ next![ Option<Item> ] ] } ]
```
```
   248	    const CAPACITY: protos::Integer;
```

The Identity section (ad19b1's landing) carries no guillemet and no
map; its example uses angle brackets for constraints (witnessed by
grep: the only map/guillemet hits in Vision/ethos.md are lines 156,
157, 167, 174, 236, 242).

#### Raw records, oldest first

The ethos records were located by the read-critical subagent (43
files across 22 flows and vision-raw) and every record quoted below
was then read by this subflow (witnessed), except where marked
relayed. Records whose heading carries no date are dated by the
flow's first commit in git (witnessed), stated as "flow of".

**vision-raw/archive-ethosNonRepetitionLaw.md** — archived
("Archived 2026-08-23 by flow 68512643; distilled into
Vision/ethos.md"). Distilled (vision-raw ethosNonRepetitionLaw).
Relayed.

> ## 2026-08-01 — "we wouldnt repeat Ord"
>
> > we wouldnt repeat Ord; any such repition in ethos syntax is an implementation
> > failure. ethos will be the most terse non-repetitive syntax ever made
>
> — psyche, 2026-08-01 (psyche vision session; recovered from the design record)

**vision-raw/genericParametersAreTraits.md** — not archived.
Undistilled. Witnessed.

> ## 2026-08-01 — "the answer is the mandatory trait!"
>
> > youre right; and the answer is the mandatory trait! so T would be a trait!
> > and multiple trait in the declaration would just adjust the emitted rust -
> > remember for us rust is assembly
>
> — psyche, 2026-08-01 (psyche vision session; recovered from the design record)

**vision-raw/archive-ethosDotosDivisionAndHelp.md** — archived
("Archived 2026-08-23 by flow 68512643; distilled into
Vision/ethos.md"). Distilled (vision-raw ethosDotosDivisionAndHelp).
Relayed.

> ## 2026-08-02 — "the two main syntaxes most agents will face"
>
> > the two main syntaxes most agents will face; one specifies the types, the
> > other fills them with data — hence why the basic 'cli help' for their dotos
> > objects is meant to emit the ethos syntax that describes their anatomy.
>
> — psyche, 2026-08-02 (psyche vision session; recovered from the design record)

**flows/5abf3be8/vision/chainedNamesScrapped.md** — not archived.
Undistilled. Witnessed.

> # Chained names — "no, that is scrapped"
>
> > no, that is scrapped
>
> — psyche, 2026-08-06T17:39:42Z (Designer session 5abf3be8; entry
> captured 2026-08-08 from the session transcript during the
> rulings-audit backfill)
>
> Context, kept apart from the quote: the Designer had listed the dot's
> roles including "it separates chained names
> (Technology.Software.Programming)". The psyche killed multi-segment
> dotted name chains.

Note (mine): Vision/protos.md lines 42–43 say "Heads may be
daisy-chained: different separators too", carried from 04db2fd2
anatomy (2026-08-27/28) and 6329f1 (`Observed.Locks.[]`); this
2026-08-06 record scrapped chained *names* in ethos. Whether the two
speak of the same thing is not settled here; listed in section 4.

**flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md** — not
archived. Undistilled (listed as a protos candidate by e996e8).
Witnessed.

> # "it opens a delimiter. everything is data"
>
> > you mean, it opens a delimiter. everything is data
>
> — psyche, 2026-08-06T17:39:42Z (Designer session 5abf3be8; entry
> captured 2026-08-08 from the session transcript during the
> rulings-audit backfill)
>
> Context, kept apart from the quote: corrects the Designer's phrasing
> that the dot "opens plain data (.{, .[)". The dot opens a delimiter,
> and there is no non-data content in the syntax — everything is data.

**flows/5abf3be8/vision/sectionsExistToConferTraits.md** — not
archived. Undistilled. Witnessed.

> # "What other point is there to have different sections?"
>
> > What other point is there to have different sections?
>
> — psyche, 2026-08-06T17:56:10Z (Designer session 5abf3be8; entry
> captured 2026-08-08 from the session transcript during the
> rulings-audit backfill)
>
> Context, kept apart from the quote: answers the Designer's question
> whether position should make each item implement the universal
> Input/Output/Refusal traits. Conferring traits is the reason sections
> exist.

Note (mine): this is the earliest record of what the Declaration
calls implied associations in the signal and sema variants.

**flows/5abf3be8/vision/encodedFormFingerprintTraitDesign.md** — not
archived. Distilled (5abf3be8 encodedFormFingerprintTraitDesign).
Witnessed.

> > so encodedform trait must implement the fingerprint trait. the
> > fingerprint trait by default uses the rkyv of that object and gets
> > the hash of it. all references use the encodedid of the thing it
> > refers to. does that make sense? or is it encodable and
> > fingerprintable? are we using nouns or qualifiers for traits? Id
> > really like to talk about traits more, how we design them and name
> > them, and use them
>
> — psyche, 2026-08-06T21:58:07Z (Designer session 5abf3be8; entry
> captured 2026-08-08 from the session transcript during the
> rulings-audit backfill)

The record carries a 2026-08-14 annotation that its vocabulary is
dead (code/encoded dropped 2026-08-13) and that nouns-vs-qualifiers
resolved to qualifiers.

**vision-raw/colonConfusion.md** — not archived. Undistilled.
Witnessed.

> > "I would rather not create confusion with :"
>
> — psyche, 2026-08-07, captured 2026-08-07T18:59Z (Designer session d63804f2)
>
> Superseding entry:
>
> > "the fixture is blessed, and / for imports"
>
> — psyche, 2026-08-07, captured 2026-08-07T22:10Z (Designer session d63804f2)

Superseded in turn by 2b34fafa importResolution (2026-08-20, colon
for external pulls) below; the landed Imports section uses the colon
(`protos:Text`).

**flows/d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md** —
not archived. Undistilled. Relayed.

> ## 2026-08-07T18:33:22.940Z — "Looks really confusing to me"
>
> > and im trying to understand what Submit.Request is? is it a newtype
> > around another newtype? Looks really confusing to me.
>
> — psyche, 2026-08-07T18:33:22.940Z (Designer session d63804f2)

> ## 2026-08-07T18:47:12.105Z — "I don't like the single field struct"
>
> > And what are the double new type wrapping about? I don't like it.
> > I don't like the single field struct.
>
> — psyche, 2026-08-07T18:47:12.105Z (Designer session d63804f2)

**flows/6863ef19/vision/traitsAsCapabilities.md** — not archived.
Distilled (6863ef19 traitsAsCapabilities). Relayed.

> ## 2026-08-13 — all traits are qualifiers; reconsider traits as capabilities
>
> > all traits will be qualifiers. I disagree with rust's convention
> > (Write Read should be Writable and Readable).
>
> > lets look at an update to the skills, and reconsider traits as
> > "capabilities". Rethink the whole concept over and represent it
> > this way
>
> — psyche, 2026-08-13T17:17+02:00 (Designer session 6863ef19), typed,

> ## 2026-08-13 — one protos representation per type; no dialect-qualified trait; a constant could name the dialect
>
> > Any type will only have one protos representation. so the datom::
> > version isnt necessary. look for flaws in my logic. It could even
> > have a constant variant to give the protos dialect it is
> > transcodable into
>
> — psyche, 2026-08-13T18:09+02:00 (Designer session 6863ef19), typed,

**vision-raw/traitsAsCapabilities.md** — not archived. Undistilled as
a vision-raw file (the flow copies are distilled). Witnessed. Four
entries:

> ## 2026-08-13 — types first; traits are what types implement
>
> > we need to think very carefully of what the types are. First,
> > really, because the traits are something that the types implement.
> > We don't look for traits and then think of types for that. So,
> > what are all the types? Let's look at the types first. We have the
> > things that are, like, once they're expressed, the datum [Datom]
> > types that are being read into and out of. And these essentially
> > implement a lot of the traits. Like, they're transcodable. That's
> > a good one. But... Yeah, I guess, or to be more exact, they're
> > textually transcodable. Or datomically transcodable.
>
> — psyche, 2026-08-13 (Designer session 6863ef19), dictated;

> ## 2026-08-13 — common traits are the right abstraction; all protos dialects are transcodable; qualification by module
>
> > So, if we take all the common behavior, we want to have as many
> > common traits as possible, because then we're creating the right
> > abstraction. So, all protos dialects, whether it's datum [Datom],
> > ethos, nomos, or logos, are transcodable.
>
> > we don't have to be afraid to use more elaborate terms if we want
> > to describe what this behavior is specifically. [...] if the trait
> > is transcodable, yes, and if it lives in the protos module, then
> > that's not ambiguous. Because if we fully qualify the name, it's
> > self-describing that it's transcodable into protos. So, yeah, I
> > think that's the right way to think about it.
>
> — psyche, 2026-08-13 (Designer session 6863ef19), dictated.

> ## 2026-08-20 — trait methods that are regular functions pretending to be traits; a cornerstone of models not understanding the vision; research directed
>
> > "You misunderstood the trait based approach. your trait methods are
> > just regular functions pretending to be traits. if the type needs a
> > 'name' to resove the import, then it's not resolvable. So we found
> > one of the cornerstone of models not understand my vision. Do a
> > research in this"
>
> Design session `2b34fafa`, typed (captured 2026-08-20)

> ## 2026-08-21 — ruling: infinitive verb form for action traits — Write, Read, Resolve, Create, Walk; the new-capability trait is Create
>
> > And I've had a discussion with this about how to name trait. And
> > I've seen traits come up like writing, well, no, maybe that's not
> > a good example, but walking or something like that. It would be
> > walk. So we would use the sort of infinitive form of the word, of
> > the verb, I mean. If it's an action that can be purely described
> > as an action, like write, read, resolve, create. So that's how we
> > would call this trait, I think, for the new is create.
>
> Design session `2b34fafa`, dictated (captured 2026-08-21).

The 2026-08-21 verb ruling is superseded by f426777b's 2026-08-26
"lean back to writable over write", b675f3d9's 2026-08-26 "qualifier.
Write isnt a kind", and 4decf7's 2026-09-03 "kinds are
qualifier-named"; the landed Naming section carries the qualifier
rule with Rust's verbs "tolerated as legacy".

**flows/06196cc7/vision/traitsAsCapabilities.md** — not archived.
Distilled (06196cc7 traitsAsCapabilities). Witnessed. Six typed
entries, "— psyche, 2026-08-13 (Designer session 06196cc7), typed" and
"2026-08-14":

> ## 2026-08-13 — a type for the text block; textualize on the true type; maybe drop code/encoded
>
> > I see a problem myself; when reading text, we dont know what we're
> > reading, so how do we call a method without a type?
> >
> > Conceptually, we need to give a type to the text block, then we
> > can have an encode trait on that, and textualize on the true type.
> >
> > I dont know about encode/decode; which is code and which isnt? The
> > way I see it, the binary form (in rust memory, which is
> > essentially the rkyv format) is the most code-like. But I think we
> > might even want to drop the whole concept of code/encoded to make
> > it very clear. textual/textualize is clear, so what term could we
> > use for the in-memory/signal form? Is the in-memory data actually
> > the same format as the rkyv in reality anyway?

> ## 2026-08-13 — transcodable falls with the drop; maybe verbs are acceptable for traits
>
> > 1. I dont think it survives. I think we end up with things like
> > WorkingFormCastable, but I want to see you make a shot at a bunch
> > of different naming options
> >
> > Or maybe we need to accept verbs for traits, since theyre
> > capitalized and therefore not a function

> ## 2026-08-14 — verbs accepted for traits
>
> > Yes, I accept verbs. now I can see why rust went with verbs; it
> > is easy to understand that a thing that which implements Run is
> > CapableOfRunning.

> ## 2026-08-14 — no umbrella capability; the directional traits live in protos
>
> > none of this makes sense if we use a trait for each direction.
> > The traits should live in protos regardless (Textualize and
> > whatever we pick for Materialize)

> ## 2026-08-14 — Textualize confirmed; ShapeDefined stays
>
> > Textualize is good
>
> > ShapeDefined is good

> ## 2026-08-14 — RealizeWalk, TextualizeWalk, and the Walk trait accepted
>
> > fine. im not crazy about it but its good enough

**flows/2b34fafa/vision/traitsAsCapabilities.md** — not archived.
Distilled (2b34fafa traitsAsCapabilities). Witnessed.

> ## 2026-08-18 — Realize and Textualize are never on the same type; the text realizes, the real textualizes
>
> Design session `2b34fafa`, typed (captured 2026-08-18)
>
> > "realize isnt implemented by the same type as textualize. if you
> > cant find two different types, the implementation is wrong. You
> > dont textualize the text, and you dont realize the realized data."

Carried by Vision/protos.md Direction and Layers (incorporate on the
layers above, textualize on the layers below).

**flows/2b34fafa/vision/ethosSourceFiles.md** — not archived.
Distilled (2b34fafa ethosSourceFiles). Witnessed.

> ## 2026-08-20 — one document per file, one Rust module per document: good enough for the monolith
>
> Design session `2b34fafa`, typed (captured 2026-08-20).
>
> > "for the monolith thats good enough. easy cognition is the first
> > safe bet."

> ## 2026-08-20 — File is the type; "document" is dead
>
> > "document sucks. I dont understand your question. What's wrong with
> > File?"

**flows/2b34fafa/vision/ethosNamespaces.md** — not archived.
Distilled (2b34fafa ethosNamespaces). Witnessed.

> ## 2026-08-20 — namespace inside a file is ridiculous; foundation, not wallpaper
>
> Design session `2b34fafa`, typed (captured 2026-08-20).
>
> > "this concept is ridiculous in ethos. we're building the foundation
> > and youre talking about wallpaper"

**flows/2b34fafa/vision/importResolution.md** — not archived.
Undistilled. Witnessed. Five entries, all "Design session `2b34fafa`,
typed (captured 2026-08-20)":

> ## 2026-08-20 — the first path segment resolves from a datom manifest, else the document's directory
>
> > "signal in signal/domain must be resolved from a manifest (which we
> > must spec obviously), which uses datom. if signal has no entry, it
> > will look in the directory of the document where the import takes
> > place. signal/domain would be signal/domain.ethos. if the manifest
> > resolves, signal will point at a source root (need to discuss the
> > naming; lets brainstorm on this), and domain will be the file
> > (domain.ethos)."

> ## 2026-08-20 — external pulls are explicit: colon after the source name; lib.es is the default file
>
> > "actually, I think the syntax should be explicit when pulling an
> > external source."
>
> > "`signal-pysche:Object` pulls Object from lib.es in signal-psyche
> > source"
>
> > "`signal-pysche:[Object Thing]` multiple imports"
>
> > "`signal-pysche:stream.[Stream Termination]` from stream.es in
> > signal-psyche source"
>
> > "`signal-pysche:external/helper.[Start Modify]` from external/helper.es
> > in signal-psyche source"

> ## 2026-08-20 — the worry behind the explicit syntax: a manifest name shadowing a local module
>
> > "hmmm. my worry was if the manifest contains signal and the source
> > has a signal module"

> ## 2026-08-20 — fallback killed: colon resolves from the manifest or errors; bare paths are local only
>
> > "confirmed, kill the fallback."

> ## 2026-08-20 — there is no Import type; what exists is an import reference
>
> > "I dont think Import is a type; there are no Import's; what exists
> > is an import reference."

The landed Imports section carries the colon form (`protos:Text`,
`protos:[ Text Integer ]`) and nothing on the manifest, the `lib.es`
default, or `/` paths inside a source. e996e8's ethos record ("if we
version stuff it should be in a manifest of some kind") returns to the
manifest.

**vision-raw/importResolution.md** — not archived. Undistilled.
Witnessed. Two entries; the first repeats the 2026-08-20 "not
resolvable" line; the second:

> ## 2026-08-21 — the manifest should have everything needed to assemble; maybe an assembly file, no more than one possible output
>
> > And I don't know why you wouldn't do the assembled source from the
> > manifest. The manifest should have everything you need. Like maybe
> > we don't have the same idea of a manifest, maybe we need another
> > type, kind of like how the cargo file works, but more specific,
> > where it doesn't have more than one possible output. So it's a kind
> > of an assembly file, if you will.
>
> Design session `2b34fafa` (captured 2026-08-21).

**flows/cff271af/vision/tuples.md** — not archived. Undistilled.
Relayed. Six entries dated 2026-08-22 (the record gives no
provenance line beyond the headings):

> ## 2026-08-22 — "don't we have a rule against tuples, as they represent poorly specified struct?"
>
> > what if every input is a defined type? don't we have a rule against tuples, as they represent poorly specified struct?

> ## 2026-08-22 — the old rules are poorly worded; how realistic is a struct for every complex implementation input?
>
> > the old rules are poorly worded. how realistic is it to create a struct for every complex implementation input?

> ## 2026-08-22 — "the map" is vague and overloaded; "grain?"
>
> > "the map" is very vague. Its also an overloaded term.
> >
> > > tuples are the language's grain.
> >
> > grain?

> ## 2026-08-22 — no tuples in the traits we design; do standard traits break the pattern?
>
> > so we wont allow tuples in the traits we design. any standard trait that would break that pattern or can we assume the rule to hold even then?

> ## 2026-08-22 — do we need to specify more than a single element?
>
> > do we need to specify that we mean tuples with more than a single element?

> ## 2026-08-22 — the newtype is allowed and must be mentioned; tuples are a form of un-specification
>
> > the newtype is allowed. the fact that its a tuple is unfortunate for us, so it would have to be mentionned in case.
> >
> > > A multi-field tuple struct, struct Pair(A, B), also passes the rule's letter
> >
> > do we have to allow those? I really dont like tuples, they're a form of un-specification

Note (mine): "the map" here is the ontological map of that flow, not
the key-value map. The landed Types section says "Every struct is a
tuple struct in the target Rust", carried from aa4c7747 tuples ("no
tuple in the code we design … contact point only") and 6329f1's
design; this 2026-08-22 record's "do we have to allow those?" on
multi-field tuple structs is a question left open. Listed in section 4.

**flows/01a02a34/vision/archive-ethos.md** — archived ("Archived
2026-08-23 by flow 68512643; distilled into Vision/ethos.md and
Vision/ethosMonolith.md"). Distilled (01a02a34 ethos). Relayed.

> ## 2026-08-22T17:32:33.328Z — schema, like, which is basically what Ethos is. It's a schema language.
>
> > schema, like, which is basically what Ethos is. It's a schema language.
>
> — psyche, 2026-08-22T17:32:33.328Z, typed; Codex realization transcript
> `/home/li/.codex/sessions/2026/08/22/rollout-2026-08-22T18-01-45-01a02a34-e72b-7de3-bf32-77cc682b2c33.jsonl`,
> line 288, ordinal 287 (session `01a02a34-e72b-7de3-bf32-77cc682b2c33`).

> ## 2026-08-22T21:43:29.015Z — It would also be great if we can use ethos instead of schema but ethos-monolith might not be ready to use.
>
> > It would also be great if we can use ethos instead of schema but ethos-monolith might not be ready to use.
>
> — psyche, 2026-08-22T21:43:29.015Z, typed; … line 439, ordinal 438

**flows/01a02a34/vision/archive-schemaSyntax.md** — archived (same
header). Distilled (01a02a34 schemaSyntax). Relayed.

> ## 2026-08-22T17:32:33.328Z — So this is what I mean. We need a schema syntax to show, to train agents to be able to properly use things and to also show us where our design is lacking.
>
> > So this is what I mean. We need a schema syntax to show, to train agents to be able to properly use things and to also show us where our design is lacking.
>
> — psyche, 2026-08-22T17:32:33.328Z, typed; … line 288, ordinal 287

**flows/68512643/vision/negatives.md** — not archived. Undistilled.
Witnessed. Three entries, 2026-08-23, "(Designer session 68512643),
dictated" and "typed". The first is the long dictation on negatives in
LLMs; its passage bearing on Datom and Ethos:

> > […] you generated the idea that Datom does not generate rust. But let's
> > look at rust for a minute, and its analog for data. Rust can, the
> > language itself, R-U-S-T by the way, I know the speech-to-text
> > likes to always convert this to rest, R-E-S-T, but that's not what
> > I'm saying. Maybe I should just say rustlang, has a syntax to
> > express language inline, or directly in its own syntax. When we use
> > rust to compose, or rustlang to compose a type directly in the
> > code, we're essentially writing data in the code. And so if further
> > down the road, or when further down the road, rather, Ethos becomes
> > a full replacement for authoring software logic rather than rust,
> > which then becomes just the assembly language aspect of Ethos, then
> > there is a strong case that could be made that we might want to
> > have this inline data aspect of rust echoed or made available in
> > Ethos. […] Because let's not forget that negatives cost context,
> > whereas they don't give direct value.
>
> — psyche, 2026-08-23 (Designer session 68512643), dictated.

> ## 2026-08-23, 68512643-4 — the dangerous line was true in its context; the road opens only explicitly contextualized
>
> > So the line it's dangerous is true in that context because when
> > the model brought forward the idea that Datom generates rust,
> > there wasn't enough subtlety. Like, we aren't there yet. My whole
> > point was that we might eventually get there. But if we do either
> > get there or if we float the idea of how we would get there, it
> > would be very explicitly, uh, contextualize so that there's no
> > ambiguity as to how and when and where data may or may not
> > generate rust. Whereas if a model just floats the idea without the
> > proper context, can quickly devolve into... something we didn't
> > want it to become.
>
> — psyche, 2026-08-23 (Designer session 68512643), dictated.

> ## 2026-08-23, 68512643-5 — truth-in-everything needs a lot more context; not explored now
>
> > "there is truth in everything" would need a lot more context, and
> > it's not a road we have time to explore appropriately
>
> — psyche, 2026-08-23 (Designer session 68512643), typed.

These are carried in Vision/datom.md Nature ("That road is reached, or
even floated, only with explicit context") though sources/datom.md
does not name 68512643; the negatives entry is undistilled as
distillation practice.

**flows/aa4c7747/vision/ethos.md** — not archived. Undistilled.
Relayed. No provenance line in the record.

> ## 2026-08-24 — the biggest short-term gain: mental model and code in one swoop
>
> > ethos is essentially meant to give us, for now anyway, the entry or the biggest gain short-term is to give us a language that allows us to, in one swoop, write down our mental model of the machine and write code so that we don't get this problem where the code and the ideas for the code, well, we have psyche for that, but psyche is sort of one step back from the actual hard implementation. It's just that something like Rust or even JavaScript is full of noise. It's like maybe more than half of the code is noise, whereas we want a language that allows us to separate the mental model we have and still write it in code.

**flows/aa4c7747/vision/ethosMonolith.md** — not archived.
Undistilled. Relayed. Four entries, 2026-08-24, no provenance line:

> > monolith: whatever shape it is taking already will do. If its an executable library, we'll make a nexus out of it after it becomes usable.

> > So if we look just at a quick glance at Ethos Monolith, or maybe we need, and all of these long convoluted terms sort of become tongue twisters and they quickly show the fact that we need better terms for them. So maybe Monoethos or Ethos version one, or Ethos version zero, or Ethos zero. Yeah, Ethos zero. And that would be a better name.

> > And I think that we need to just go straight for a nexus. So it has to be written as a nexus. And we need to break down what the things that we're going to deal with...

> > right, so we need ethos-monolith to bootstrap it. We should call it ethos-cc (compiler compiler); would that be an accurate name for it? And ethos-zero because its version zero which will bootstrap ethos in the nexus trinity stack (with nomos and logos nexuses)

**flows/aa4c7747/vision/ethosTraitSyntax.md** — not archived.
Distilled (aa4c7747 ethosTraitSyntax). Relayed. Five entries, no
provenance line:

> ## 2026-08-24 — define the trait syntax for Ethos; Ethos zero nexus as first example
>
> > And so we need to define what the trait syntax for Ethos is and use the Ethos zero nexus as a first example.

> ## 2026-08-24 — traits meant trait declaration; implementation syntax is not MVP
>
> > When I said traits I just meant trait declaration. Implementation would be a big job; it would mean developping the syntax for full function bodies, and the rust generation - thats not MVP sounding anymore. So I dont see a trait syntax

> ## 2026-08-24 — carrying declarations (b) sound good, pending the generated-code picture
>
> > b sounds good, but I cant picture what code this generates

> ## 2026-08-25 — no Create alias over TryFrom/From; the carrying names the trait it means
>
> > this is quackery. Nonsense. There's no need for this. If we want TryFrom/From, then that's what we'll call it.

> ## 2026-08-25 — the trait implementation checking mechanism is approved
>
> > I approve your trait implementation checking mechanism.

The last is the origin of the Associations section's compile-time
assertion.

**flows/aa4c7747/vision/interactions.md** — not archived. Distilled
(aa4c7747 interactions). Relayed.

> ## 2026-08-24 — interactions is the term for Ethos trait implementations
>
> > And obviously, one thing we maybe haven't said clearly is that the ethos traits, they're whatever you call them, trait implementations. And I would like something more succinct than trait implementation, I think. Or maybe we just say implementations, but that might be a little bit of an overloaded term. So, maybe it's behavior. So, they're behaviors or they're interface or they're interactions. Yeah, I think interactions are good, because I think that describes it well, what it is really conceptually.

> ## 2026-08-24 — interactions use the type itself in all cases; research the legitimate exception
>
> > So, they're interactions use the type itself in almost all cases. Well, really in all cases, because if it's not using the type itself, then is it really an interaction of that type? Let's do some research...

**flows/aa4c7747/vision/tuples.md** — not archived. Distilled
(aa4c7747 tuples). Relayed.

> ## 2026-08-24 — no tuple in the code we design; contact points only
>
> > tuple: no tuple in the code we design: if some parts require it (standard traits, dependencies), then we allow it at that contact point only

Carried word for word in the Types section.

**flows/aa4c7747/vision/spokenVocabulary.md** — not archived.
Undistilled. Relayed. Two entries, 2026-08-24:

> > So these will be types and traits, and the traits need to use the type itself, the trait implements, or the type concerned, the implementer, the type that the trait qualifies, the qualified type. We need to establish a vocabulary too. This is what's happening because no one has ever, or before now, programming was not a thing that was really done in speech. So now we're creating a spoken vocabulary for software engineering.

> > Let's go through the vocabulary, go do some research in terms of engineering and what kind of also in ontology and, and studying the world and studying and trying to classify how things behave, what kind of vocabulary, what kind of terms come back a lot and seem to, what kind of, what terms people seem to prefer, which, which ones sort of stick with them. And these are the ones we want to favor.

**flows/f426777b/vision/ethosSourceFiles.md** — not archived.
Undistilled. Relayed. Two entries, 2026-08-25:

> ## 2026-08-25 — sema and nexus in the signal repos: a problem
>
> > I can see a problem already:
> > […the authored-interfaces diagram…]
> > sema and nexus in the signal repos.

> ## 2026-08-25 — nexus and sema ethos are not designed yet; when designed they live in the nexus' main repo
>
> > lets make it clear first; the nexus and sema ethos arent designed
> > yet, but when they are they will live in the nexus' main repo

Bears on the Declaration's sema variant: as of 2026-08-25 the sema
ethos was "not designed yet"; 6329f1's archive-ethos (2026-09-04)
names the sema variant's shape.

**flows/f426777b/vision/spokenVocabulary.md** — not archived.
Distilled (f426777b spokenVocabulary). Relayed. Four entries,
2026-08-26, typed; the first is the living's own transcription of an
audio statement:

> > Right, the vocabulary. We need a different vocabulary because we're
> > moving one abstraction up from Rust.
> >
> > So we already went over the fact that, for us, a generic is a
> > trait—or unless there's maybe something I don't see right now, but
> > as far as I can tell.
> > […]
> > I don't think we can just define traits implicitly, meaning if we
> > only declare traits in our own version of implementations, of how we
> > implement them, then it'll be difficult. It's going to be complex to
> > try to extract what that trait actually is and how many interactions
> > it has.
> >
> > And I don't like the word "trait," if only because it's a bit
> > acoustically ambiguous, maybe—kind of like how the Rust language
> > often is mistaken for REST, R-E-S-T.
> > […]
> > So we need to think of better terms for our language, for Ethos, for
> > how we talk about everything. And we need a more specific way to
> > declare traits.

> ## 2026-08-26 — Capability is great; wanted: "an object which has a capability" in one word; a runner runs; a Kind? type would also work; call the discipline logic engineering
>
> > Capability is great, but how do we see "an object which has a
> > capability" in one word? Because that's basically what we're
> > looking for here; a new way to *speak* software engineering at a
> > higher, more correct layer of abstraction. we should even call it
> > logic engineering.
> >
> > Something that can run is a runner. "something that can X" ... a
> > Kind? Seems that type would also work.

> ## 2026-08-26 — kind is perfect
>
> > kind is perfect.

> ## 2026-08-26 — lean back to writable over write
>
> > I also want to lean back to writable > write

**flows/b675f3d9/vision/kinds.md** — not archived. Distilled (b675f3d9
kinds, in both sources files). Relayed. Eight entries, 2026-08-26 and
2026-08-27, "the psyche, typed" or "dictated":

> ## Qualifier form; Kind is the word; a kind is a trait; no generics in Ethos
>
> 2026-08-26, the psyche, typed
>
> > 1. qualifier. Write isnt a kind. we say kind now, not trait. declare a new kind = declare a new trait, in Ethos world, which will imply some things which arent in rust world (tbd). so in Ethos there are no generics, only kinds.

> ## Capability is a function a kind has
>
> > 4. capability will refer to the actual functions a kind has (Runnable would be the Kind, run would be a capability)

> ## The kind syntax proposal is inappropriate; start from the anatomy of a Rust trait
>
> 2026-08-26, the psyche, dictated
>
> > Your kind syntax proposal is very... is completely inappropriate. So start by looking at a rust trait, which is what our kind essentially becomes, and in its most complex form, and doing the anatomy of a rust trait. And then you'll see how many different kinds, how many different types of things are in a trait. Which means you're almost, I'm like, I can guarantee you that you're going to need a struct to fit it all in. Or maybe even a root enum to differentiate between different kinds of kinds or different types of kinds or maybe an enum in the struct or like we'll look at different possibilities for essentially to maximize elegance, the elegance of the syntax and yet achieve the level of expression required to express any different kinds that we might want to express.

> ## A kind's identity must mirror Rust's: name and constraints
>
> > important: in rust, a trait is identified by its name *and* constraints. How would we want to mirror that?

> ## Identity head preferred; existing Rust traits perhaps kept as-is; capabilities need real thought
>
> > I prefer
> >
> > Processable<[Clonable Sendable]  Serializable>
> >
> > what did I say about the <> syntax in ethos?
>
> On `[Output.Serializable  Ref]   associated kinds`:
>
> > do you mean associated types? What is Ref? If we want to refer to existing rust traits in the non-verbal way, we'll have to maintain a table for conversion. but that will incure a cost. it might be better to keep the existing trait as-is
>
> On `[process.Output  fetch.Output  validate.Boolean]   capabilities`:
>
> > You havent actually thought about this I can tell. Give it a serious shot. Maybe you need to start with the anatomy of a trait function signature (a capability)
>
> On the section "Where the interaction fills the position":
>
> > I dont understand that section. look like quackery
>
> > dont worry, you understood what I meant; the identity parts of the data.
>
> > We'll come back to what I havent addressed.

> ## A struct always has the same fields in the same order; a capability struct is one type
>
> 2026-08-27, the psyche, typed
>
> > lots of quackery there.
> >
> > you seem really confused about ethos design.
> >
> > a struct {} always has the same fields, in the same order. the struct definition declares the field types, so they can be anything; there are no restriction in which type a field can hold!
>
> > so if we use a struct for the capability, it's always the same struct type! it cannot change in number of fields!

> ## Different structures may be different types; the delimiter after the head discriminates
>
> 2026-08-27, the psyche, dictated
>
> > It's perfectly acceptable to have different structures, uh, that result in slightly different types. We use the same mechanism in the, uh, ethos signal interfaces and others to differentiate between things like an enum and a struck [struct] by, uh, checking the, uh, delimiter after the head. And this mechanism is used even for a other things. So we could have... and I think this is appropriate for this part of the machinery. We could have different types represented structurally in the context of describing a kind's capabilities.

> ## Variable length is []; all its components share a type or kind
>
> > yes variable length is [] and all components must share a type or kind

**flows/b675f3d9/vision/ethosMonolith.md** — not archived.
Undistilled. Relayed.

> ## It becomes a nexus; everything will be a nexus
>
> 2026-08-26, the psyche, typed
>
> > 5. Then we'll make it a nexus. Everything will be a nexus; the consistency will create reliability and increase the quality and clarity

**flows/b675f3d9/vision/structuralParsing.md** — not archived.
Distilled (b675f3d9 structuralParsing, in protos, ethos and datom
sources). Witnessed; quoted whole in the protos section (2026-08-27,
arity discriminates; "<> is a real Protos delimiter of course. I'm
surprised you have to ask"; parsing is context-dependent; shape
conveys type only within context).

**flows/b675f3d9/vision/spokenVocabulary.md** — title only, empty
(relayed).

**flows/01a03d6e/vision/ethosInterfaces.md** — 2026-08-26; quoted in
1.3. Undistilled in sources/ethos.md, distilled in sources/datom.md.

**flows/ac1e9ec8/vision/datomSyntax.md** — 2026-08-26; quoted whole in
1.3; named in sources/ethos.md as ac1e9ec8 datomSyntax.

**flows/04db2fd2/vision/kinds.md** — not archived. Distilled (04db2fd2
kinds). Relayed. Flow of 2026-08-27. Eleven typed entries, "-- psyche,
typed."; no dates in the headings:

> ## Kinds as verbs not allowed; rust-imposed verbs tolerated as legacy until ethos takes over; Delineated is true (delineation intrinsic; implementation fetches it); all kinds move to qualifiers; Textualized; Realized reconsidered, candidates listed
>
> > Kinds as verbs are not allowed; we only tolerate the legacy rust gives us, until ethos takes over completly as the authored language at which point we'll remove the technical debt (Write Read, etc) - so we can do Delineatable or Delineated. I was hesitant on the second as it implies that it *already is* delineated, but on second thoughts it *is actually true*; the delineation is intrinsic to it, the implementation is essentially *fetching* the delineations which are already there by virtue of having the shape that is has. So we will move all the kinds to qualifiers. only the rust-imposed verbs are tolerated, for cognitive ease since we will switch between rust and ethos code so much; renaming across them would be way too cognitively costly. Textualized. Im reconsidering Realized, as a bit too abstract for my taste. Objectified? Specified (not so good, but there is an aspect to this I like)? Suggest anything you can think of. Prospected? Casted (weird, could be "thrown")?

> ## Textual as a kind; Actual too strong; "it can take the form the runtime can use"; Embodied, unless Forged
>
> > Textual is already a qualifier. How does that sound as a kind? I like Actual instead of Real, but it's going to cause problems cognitively (too strong). What we're trying to say is that
> >   it can take the form the runtime can use. I think Embodied is the right term, unless Forged is better.

> > extend our example to specify all of protos, and draft out the accompanying kinds. do we have a design for where the kinds live in an ethos interface file?

> ## A type's anatomy is a dialect's, not protos
>
> > if you're talking about a type's anatomy, you're out of protos now into specific dialets

> ## Prospect<Datomic>.Text is quackery; types and kinds are missing
>
> > this is quackery. youre missing types and kinds

> ## Ethos has a syntax for kinds and separate blocks for types and kinds
>
> > Youve given up on ethos syntax now. I think youre not aware of the ethos syntax for kinds, and the concept of separate blocks for types and kinds. remember and try again

> ## Result is Result; the struct form is for complex kinds
>
> > I don't know why you're reaching so hard. it's Result!
> > the struct is for complex kinds

> ## One separator per head; options mutually exclusive; ! for mutable self
>
> > we can't add separators; that trick can only be used once. ! for mutable self felt like the most useful. there is only one separator so they must be mutually exclusive options.

> ## Yields always in [], even a single yield
>
> > we should stick with a consistent syntax and use [] even for single object yield

> ## A capability's [] yields all of these
>
> > no, yields all of these

> ## The Rust side of a kind
>
> > what does the rust side of this look like?
> > isn't that Result?
> > we need to draft a syntax for kind to type association

Note (mine): "One separator per head; options mutually exclusive"
(2026-08-27/28) and Vision/protos.md lines 42–43 "Heads may be
daisy-chained: different separators too" (from 04db2fd2 anatomy of the
same flow, "We aren't closed off to the daisy chain of heads … it
could be like different separators too") sit in the same flow; the
first is about a capability's single receiver separator, the second
about chaining heads. Not resolved here.

**flows/2ef42163/vision/ethos.md** — not archived. Distilled (2ef42163
ethos). Relayed. Flow of 2026-08-28.

> ## Rust syntax is the target; a principle in Rust is pointed at by recycling the same syntax
>
> After Result and Self entered the kinds block, the psyche:
>
> > as Result and Self showed, rust syntax is the target, so whenever we need to point at a principle in rust, we usually will recycle the same syntax
>
> -- psyche, typed.

**flows/e8c4cc61/vision/kinds.md** — not archived. Distilled (e8c4cc61
kinds). Witnessed. Flow of 2026-08-29. Ten entries, "-- psyche,
typed." unless marked STT:

> ## A kind declaration's position holds a kind, not a type
>
> Context: the flow wrote the declaration
> `Prospective<Ethos>.[ prospect.[ Result<Ethos Fault> ] ]`.
>
> > that doesnt work.  The kind declaration must use a kind, not a type. do we need a Type kind? or is there something equivalent which already exists in practice?

> ## The position of Prospective is bounded by Embodiable
>
> > you mean Embodiable

> ## Embodiable keeps the embody capability
>
> > and Embodiable still has the embody capability, to turn it into an embodied value (what is the terminology in rust for this? an in-memory value?)

> ## Prospective<Sized> is the declaration; TryInto is not a kind
>
> > TryInto just doesnt sound like a kind. lets go with Prospective<Sized>

> ## `:` for no self stands
>
> > ok, `:` for no self stands

> ## Our own terminology over Sized: everything has an embodiment
>
> > First let's step back even further. I think I would rather use our own terminology over sized. We have the sized kind and I don't know, it just doesn't flow very well in a sentence so I'd rather say an embodied object. I think it just sounds better. Any of our embodied, oh wait, that doesn't work either.
> >
> > Actually what I'm trying to say is any object that we have, like any concept basically in Protos, has an embodied conceptualization. A kind, you could say, has a type that holds the definition of that kind, if you follow me. Obviously that's not this is a rust value in practice.
> >
> > When I say embodied I guess I mean it has a rust value. A kind has an embodiment, a type has an embodiment, a datom [STT: datum] value has an embodiment in the sense that it fits into a certain kind of type. A kind declaration in ethos is going to translate into an embodied value in rust that's going to hold all of its different values, like its name etc., and it also has a default structure. This would be, I guess, or maybe it has an anatomy or a protosic [STT: protossic] representation, basically. It has a representation in Protos, like a text representation, and by default it's going to have its own way of being represented.
>
> -- psyche, STT.

> ## Situation and Embodied stand
>
> > yes on situation. yes on Embodied

> ## Structural's capability returns the protos structure, recursively; Prospective stays
>
> > I dont think the Structural capabilities include prospect. it would be a capability that returns its protos structure and all the recursive structures it contains (replacement for portions)
> >
> > nothing is replacing Prospective, especially since it's quite universal (maybe even universal beyond protos; a more aptly named TryInto<Sized> basically)

> ## No Embodiable; Embodied is an alias of Sized
>
> > I dont think there is any Embodiable. It's just Embodied, which is an alias of Sized. Would that work? Or would it make everything more complicated than just using Sized?

> ## A second syntax for a more complex kind, opening with `{`
>
> > your trait syntax doesnt work. Looks like we need to redesign the kind syntax. We could add a second syntax for a more complex kind which opens with { and has a few fields for things like super traits. what are all the things which traits can declare? We had some flows do some research on this.

Supersession: "Embodied is an alias of Sized" (2026-08-29) and
62022e8f's "Embodied is the bound" are superseded by 6329f1's
2026-09-04 "drop Embodied; stick with Sized" (Vision/protos.md line
79); "Prospective" by "potential" (1c282d, 6329f1); the `:` receiver
and the complex kind opening with `{` are carried by the Kinds
section.

**flows/e8c4cc61/vision/ethosFileAnatomy.md** — not archived.
Distilled (e8c4cc61 ethosFileAnatomy). Witnessed. The origin of the
sweet form and the Declaration's file anatomy:

> ## The outer braces are omitted in any ethos file
>
> Context: the flow had put to the psyche the Library file syntax
> `{ [types] [kinds] [associations] }` from db97561c's corrective prompt
> (a flow default), alongside the psyche's handwritten page below.
>
> > Library file syntax
> >
> > { [types] [kinds] [associations] }
> >
> > the outer {} should be omitted and always implied in any ethos file
>
> -- psyche, typed.

> ## Handwritten page: Ethos File Anatomy
>
> Photo: `ethosFileAnatomy.jpg` (same directory). Transcription of the
> psyche's own hand; comments after `;` are the psyche's.
>
> > Ethos File Anatomy
> >
> > Signal.{0 2 0}               ; Variant and version
> >                              ; This example is Signal
> > [ethos:[Registry ...]]       ; Imports
> > [Generate.{                  ; Requests
> >     Registry Target
> >   }
> > ]
> >
> > [Generated.{Vector<RustFile> ...}
> >  GenerationFailure.[SyntaxError.Vector<FilePath>
> >                     MissingImport.Vector<ImportName>
> >                     ...
> >                    ]         ; Responses
> > ]
> > ─────────────────────────────
> > Type/Version [Imports] [Requests] [Responses]
>
> -- psyche, handwritten (photo), 2026-08-29.

> ## The signal type is very simple, in terms of ethos types
>
> > I think we should make the signal type very simple, if only for clarity and to encourage the use of a library file. So we would have the signal type in terms of ethos files or ethos types ...
> >
> > So for a signal type, it would have an import vector, a request vector, and a response vector, and so on for different types.
>
> -- psyche, STT.

> ## The page's example is a brainstorm; its anatomy and number of objects stand
>
> > as you can see in the example, which should not be taken too literally, this is really just a brainstorm. So I'm not set on the particular example. The anatomy is good. The number of objects is good. But I'm not 100% on this Generate [STT: generate ticket] registry or a target or more than that or less than that. And obviously I haven't specified what the registry would look like.
>
> -- psyche, STT.

> ## Channel is not the psyche's
>
> > 2. I have no idea what this is, so its agent hallucination. What is it used for?
>
> -- psyche, typed.

> ## The sweet file syntax has a corresponding type; the full form and mixed ethos
>
> > if we want the "sweet" ethos file syntax, we need a corresponding type, like EthosFile (I dont like that name)
> >
> > then we would convert the text where
> >
> > ```
> > Library.{0 1 0}
> > []                            ; imports
> > [types]
> > [kinds]
> > [associations]
> > ```
> >
> > becomes
> >
> > ```
> > Library.{
> >   {0 1 0}
> >   []                            ; imports
> >   [types]
> >   [kinds]
> >   [associations]
> > }
> > ```
> >
> > this also gives us a way to write mixed-ethos
> >
> > ```
> > [
> >   Library.{
> >     {0 1 0}
> >     []                            ; imports
> >     [types]
> >     [kinds]
> >     [associations]
> >   }
> >
> >   Signal.{
> >     {0 1 0}
> >     []                            ; imports
> >     [requests]
> >     [responses]
> >   }
> > ]
> > ```
> >
> > or perhaps variations of this. in any case it lets a model be specific when creating a standalone object
>
> -- psyche, typed.

> ## A file is one sweet Ethos or a full datom; everything first read as a datom
>
> Context: the flow proposed that a file is either one sweet Ethos or a
> full-form datom (an Ethos or Vector<Ethos>), never mixed; and that an
> ethos file is a datom of type Ethos.
>
> > yes, youre right there, and I forgot that I used to envision an additional step where everything was first read as a datom.
> >
> > Im not sure how well that would play with the dynamic "structure-based" reading, but maybe there is a way to do it
>
> -- psyche, typed.

The Library and Signal roots of this record are superseded by 6329f1's
2026-09-04 archive-ethos (kinds, types, signal, sema variants); the
version in the head is superseded by e996e8's 2026-09-04 "drop the
version number altogether".

**flows/e8c4cc61/vision/ethosTypes.md** — not archived. Undistilled.
Witnessed. Two STT entries:

> ## Specifying a type inline
>
> > But one thing that I did do, and I have been doing, is to specify a type inline, so to speak. So you can see in the responses, we have, for example, generation failure, which is an enum because it then follows a bracket, right, which has all the variants in it, and the first variant being syntax error dot vector.
> >
> > So I'm specifying a new type inline. Instead of just saying syntax error and then importing syntax error from a library, I'm saying syntax error is a vector of file path. And that is something that I want to allow in ethos ... it's up to the writer really to decide if he wants to create a new type somewhere else or if he wants to just do it inline, then he can just do so.
> >
> > It's a syntactic sugar that allows him... So that these types will essentially become full types of their own and not something minor.
>
> -- psyche, STT.

> ## A variant named as an already defined type is a data-carrying variant
>
> > So the syntax error object, right, could just be by itself with no following dot. And in the import, it could say syntax error, and that object would be described in the library, and it could say syntax error dot vector file path.
> >
> > So there's another mechanism there also, which is when a variant is actually an already defined type somewhere else, we can just say syntax error, for example, and if it was specified somewhere else in the library, the same name, syntax error, then the ethos runtime has to make the leap and understand that syntax error is actually a data carrying variant.
> >
> > But there's no need to write syntax error dot syntax error data. We don't need that syntax. That's just repetitive, and from a logical point of view, there's actually no need to create that repetition. All that's needed is for the runtime to find out that syntax error is actually an already defined type, which means that this becomes a data carrying variant.
> >
> > And like I said, it can also be declared inline. It can declare the type of data that it carries inline by just saying syntax error dot vector, or it could be a full struct, or it could be another enum by using a bracket and then declaring the variants [STT: variance]. And then those variants [STT: variance] in turn could also be declared inline or refer to an already existing type by name, which would make them data carrying variants [STT: variance].
>
> -- psyche, STT.

Note (mine): the landed Types section says "A variant carrying
nothing is bare. A variant carrying data is headed: `Name.Type`",
which means a bare `SyntaxError` is read as carrying nothing. This
undistilled record says a bare variant whose name is an already
defined type is a data-carrying variant. Listed in section 4.

**flows/e8c4cc61/vision/datomizable.md** — quoted in 1.3; named in
sources/datom.md, not in sources/ethos.md.

**flows/e8c4cc61/vision/designExamples.md** — not archived.
Undistilled. Relayed.

> ## When designing Ethos, the examples are Ethos's own objects
>
> > lock is an extremely poor example when we are designing ethos. why not do the structure of an ethos Library and an ethos Signal Request?
>
> -- psyche, typed.

**flows/e8c4cc61/vision/designPractice.md** — not archived.
Undistilled. Relayed. Seven typed entries; those bearing on how ethos
is presented:

> > whenever a new datom is shown, its spec must first be shown in ethos.

> > no, we need a protos skill. talking in protos dialects is going to be standard. eventually, the models will *only* speak in protos dialects through a protos harness. So it's not only for the designer

> > I want to break those up into protos datom and ethos skills. protos should be very general. datom and ethos should show some rust code (datom shows what rust structured type decodes it, and ethos shows what rust is generated, and also which rust is generated by default without any ethos to represent it, like the trait impl compilation checks)

> > you should always present the ethos spec of any new object, such as your complex kind

> > I dont like those broken up bits of code. Use code blocks with comments.

**flows/62022e8f/vision/ethosTypes.md** — not archived. Distilled
(62022e8f ethosTypes). Witnessed. Flow of 2026-08-30. The origin of
the Declaration's map type:

> ## A map type is declared with guillemets: key type, value type
>
> Context: artifact comment anchored at the Datom concept spec, which
> had an `Entry.{ Key.Datom Value.Datom }` pair type.
>
> > I just realized I never addressed KV specification in ethos.
> >
> > SomeMap.<< NameType ValueType>>
> >
> > I use << instead of guillemets because I dont know how to type guillemets.
>
> -- psyche, typed.

Superseded by ad19b1's 2026-09-04 drop ruling (section 3).

**flows/62022e8f/vision/designPractice.md** — not archived.
Undistilled. Witnessed. Six entries; the one bearing on the
Declaration's variant-headed form and on presentation:

> ## Every ethos block presented needs its proper context: a root variant naming its species; layers never mixed in one block
>
> > This reminds me that we need to have a standard way to make it a requirement that every time ethos code is presented, it needs to have its proper context. So, we can create many different kinds of ethos root objects to facilitate the expression of ethos code. ... So, the first line nominal dot, and then bracket, right? This is the syntax for a kind declaration. But then below that are sort of like examples of how this would be ... We're talking about how this nominal kind, right, would be represented when used in textual form. ... So, we have different layers that are mixed up in the same block of code, which is problematic. So, either we need to make it very clear with comments that these are different sections. Well, no, yeah, or we need to use different blocks. And so, for the ethos code context, right, let's say we could say we can omit the version number in most cases because, you know, the context of that discussion, the date of that report, and so on ... would be able to figure out roughly what version of the syntax we're dealing with. So, but at least we need a variant. ... so far we've had ethos file, or yeah, we could say ethos root types, which have mixed ... sections. So each section contains only a certain, you know, species, like a type declaration, or even a more specific type declaration, like a request type declaration and a response type declaration, and then a kind declaration. And then we're going to have like other specific type, like a storage type declaration when we have the SEMA file type, and we'll have some other specialized type when we talk about nexus declaration files. Maybe. This is all just to be decided ... But we could have a single species type ethos root, like kinds. So you could start a block, an ethos block, right? ... I think it would be a good idea for us to know what language, what dialect we're dealing with here every time we see a block. ... the first non-comment line would say kinds, capitalize of course, because it's a variant. And then, like I said, you know, we could put the version number, but that's sort of optional ... and we could even accept files without version numbers. It's just that the version number could make it more explicit and therefore could allow the runtime to, you know, know ahead of time if it's just going to waste its time trying to par
>
> -- psyche, STT.

This is the earliest statement of the variant-headed, single-species
roots (Kinds, Types) that 6329f1's archive-ethos names and the
Declaration carries; it also says the version "is sort of optional",
which e996e8's later "drop the version number altogether" completes.

The other five entries: "The ethos that's in the protos skill is
inappropriate for multiple reasons, one of which is that it always
has to be situated. Also, datom [STT: datum] would be more appropriate
…" (STT); the page's examples "almost word for word ready to go as
vision" (STT); a page is raw vision-ready content, "no back and forth"
(STT); "it's a huge waste of fable to be editing HTML … writing a
markdown … letting a sub-agent do the conversion" (STT); "the subflow
can also pick colors" (typed).

**flows/62022e8f/vision/distilledVision.md** — not archived.
Undistilled. Witnessed. Two STT entries:

> ## Vision carries the detail; a skill is its concentration; distilled vision must carry actual code, ethos beside the Rust it yields, and the invariant Rust
>
> > the vision really is like a skill without, it's a bit more detailed, I think. So when we have like the vision of something together, it has sort of like all the details, which is good for implementing something. But from that, like concentrating the vision and just taking the parts that are sort of important to know to understand the concept is how we create skills. So by creating the vision, we sort of almost automatically create the skill. So all of the effort that we've been putting towards making the skill is really, we should have just been like really reinforcing the distilled vision with like actual code, which I think the vision is sorely lacking right now in this department, especially in terms of showing something like here's the Ethos code, and here's what kind of Rust we would expect to come out of this. And also like what is the invariant Rust code that comes out when we compile an Ethos or a Nexus executable. And just putting all of these things in there so that they're easily accessible to distilled vision, which would be easily accessible and like more often read by flows that get involved in this topic and sort of like in a more centralized way. And sort of inform them sort of more like upfront and clearly like what this is all about.
>
> -- psyche, STT.

> ## When the psyche speaks on something already in distilled vision, log it raw and also apply it directly to the distilled vision
>
> > And it would make it obvious whenever if I said something that contradicted that, that we need to change the vision. And then we could sort of, we don't necessarily always have to work on raw vision when I speak. If what I'm talking about is something in the distilled vision, like obviously you can log what I say, but then you can also just apply what I say directly to the distilled vision, if you understand what I'm saying.
>
> -- psyche, STT.

**flows/995a164e/vision/ethosTypes.md** — not archived. Distilled
(995a164e ethosTypes). Witnessed. Flow of 2026-09-01.

> ## The contained kind declaration is ethos, not datom; an Ethos meta type followed by an implied, delimit-less vector of explicit ethos objects
>
> Context: artifact comment on the recap's `Datom / KindDeclaration.{ … }` contained-form example (2026-08-30 18:51).
>
> > this is wrong. It ethos not datom.
> >
> > so maybe whrat [typed; what] youre reaching for is an Ethos meta type which is followed by an implied (delimit-less) vector of explicit ethos objects, such as KindDeclaration.{ ...
>
> -- psyche, typed (artifact comment).

**flows/995a164e/vision/designPractice.md** — not archived.
Undistilled. Witnessed. Three entries; the one bearing on the
Declaration's separate variants:

> ## Associations from different libraries are never mixed in one block; thinking machines copy what they see, a bad pattern is bad at any layer
>
> Context: artifact comment on the recap's Associations block, which held `Text.[ Potential<Protos> ]` and `Protos.[ Potential<Datom> Potential<Ethos> ]` together (2026-08-31 11:16).
>
> > This feels like these two associations would be from different libraries. The text to potential protos would be in protos, and the protos to potential datum [typed; datom] would be in datum [typed; datom]. In order to keep confusion from cascading out of these reports, we shouldn't mix these kinds and types and associations together, because it's going to create problems. Thinking machines just copy what they see, so any bad pattern is bad no matter where it appears and no matter at what layer.
>
> -- psyche, typed (artifact comment).

The other two: the main flow writes markdown with mermaid and the
converting subagent makes scaled SVG (typed, 2026-08-31 11:24); and
"find the beautiful Rust we want first, then work backward" (STT).

**flows/995a164e/vision/rust.md** — not archived. Undistilled.
Witnessed. Three entries; the one bearing on the generated Rust the
Declaration shows:

> ## Generated Rust uses fully qualified names; Rust as an assembly language, explicit, correct over sweet
>
> Context: artifact comment on a mermaid node reading `Context: Kinds` (2026-08-31 11:22).
>
> > Like I said earlier, I think we could be more explicit about the context. In this case, the context would be `ethos`. We could use the import syntax because I also want to make this clear: when we generate Rust, the generated Rust would just use fully qualified names, so it would be `ethos::kinds` and not just `kinds`. That is because we're using Rust the way we intend to use it, which is more like an assembly language, which is extremely explicit and doesn't leave room for... We're not concerned about making it look sweet. We're concerned about it being correct.
> >
> > Even in our examples, just to be clear about what we're talking about, it doesn't have to be `ethos::kinds`. In this case, it could just be that the graph itself is titled `ethos` or `ethos declaration` or something like that. Just `ethos` would be enough, I think.
>
> -- psyche, typed (artifact comment).

Carried by the Imports section ("The generated code carries no `use`
statements; each imported name is written fully qualified"). The
other two entries: "We forbid freestanding implementations. All
implementations must be of a trait." (typed, 2026-08-31 11:26); "I
really despise free functions, and I despise these inlined lambdas
even more." (STT).

**flows/4decf7/vision/archive-kinds.md** — archived ("distilled …
into Vision/kinds.md (Kind, Naming), flow 4decf7, 2026-09-03").
Distilled (4decf7 kinds). Relayed.

> ## 2026-09-03 — kinds are qualifier-named
>
> > kinds are qualifier-named
>
> -- psyche, typed.

> ## 2026-09-03 — corrections to the first proposal: might imply; an example with no Rust standard; no conversion tables
>
> On "implies more in the ethos world":
>
> > change the part where it says "it implies more in ethos world" for it might imply more.
>
> On the Write/Writable example:
>
> > So you use the example of Write [STT: right] and writable, but Write [STT: right] is actually a rust trait, so it's probably not a good example to use since we actually tolerate the already existing and standard rust traits. So just use a better example that doesn't already have a standard in Rust.
>
> On the conversion-table sentence:
>
> > We're not going to do any conversion tables, so don't talk about that. Take all of that out and see if it's even in the existing distilled vision, and take it out too. Take it out once you merge the whole thing. You don't have to go right now and start taking anything out. Just see if you can locate it.
>
> -- psyche, STT.

**flows/e4a40e/vision/archive-kinds.md** — archived ("distilled into
Vision/ethos.md (Identity), flow ad19b1, 2026-09-04"). Distilled
(e4a40e kinds). Relayed.

> ## 2026-09-03 — two heads differing in a required kind are two kinds
>
> > Yes, obviously those would be two kinds [STT: too kind]. I don't know, why did you have to ask me that? Wasn't that obvious? Why is that ambiguous? I'm really curious.
>
> -- psyche, STT.

> ## 2026-09-03 — what identifies a trait in Rust is what identifies a kind in the ethos
>
> > You don't have to decide which constraints are not part of an identifier. What identifies a trait in Rust is what identifies a kind in the ethos, because we're compiling the Rust [STT: rest], so we don't have a choice. There's no decision involved here, and we're not going to rewrite the Rust compiler.
>
> -- psyche, STT.

**flows/e4a40e/vision/newtypeWrappingAndSingleFieldStructs.md** — not
archived. Undistilled. Relayed.

> ## 2026-09-03 — a single-field struct is really bad design; never want that pattern to spread
>
> > I don't like your failure example because it creates a single-field struct, which would be really bad design, and I would never want that kind of pattern to start spreading. Also, even your first example is a single-field struct, which is a really bad design
>
> -- psyche, STT.

Note (mine): the landed Types section's alias form (`LockId.Integer`
→ `pub type LockId = protos::Integer;`) is the shape 6329f1 chose in
answer to this record; the record itself is undistilled.

**flows/ad19b1/vision/archive-kinds.md** — archived ("distilled into
Vision/ethos.md (Identity), flow ad19b1, 2026-09-04"). Distilled
(ad19b1 kinds). Witnessed whole; five typed entries, 2026-09-04: "I
said rust not rest. what a shitshow! you can't even hear what Im
saying properly!"; "no, thats not how rust trait is identified. we
spent hours over this today."; "position? is that what rust calls
those? thats a fuzzy way to describe them."; "and why is it
Vision/kinds and not Vision/ethos?" (asked as a question); "no, not at
all. it is narrower than ethos, since it is an ethos concept. so it
goes in ethos."

**flows/ad19b1/vision/ethos.md** — not archived. Distilled (ad19b1
ethos) for its first two entries, which were in the file when 6329f1
read it; the last two entries were committed at 19:37 and 19:44 on
2026-09-04, after 6329f1 landed. Witnessed whole; quoted whole in
section 3.f. The second entry:

> ## 2026-09-04 — space the delimiters and the inner content
>
> On the Declaration example, whose brackets were written tight,
> `[Fillable]`, `[next![ Option<Item> ]]`:
>
> > space the delimiters and the inner content.
>
> -- psyche, typed.

**flows/ad19b1/vision/designPractice.md** — 2026-09-04, "dont forget
to show the target rust". Distilled (ad19b1 designPractice).
Witnessed.

**flows/6329f1/vision/archive-ethos.md** — archived ("distilled into
Vision/ethos.md (Declaration), flow 6329f1, 2026-09-04"). Distilled
(6329f1 ethos). Witnessed whole:

> ## 2026-09-04 — the file is the sweet form; the braced form is canonical; the sweet form is converted before the text is read
>
> On the proposed Declaration's File section, which called the braced `Library.{ … }` the sweet form:
>
> > You didn't understand that the ethos file is the sweet form, and the second version, where it's `library.` and then it opens `{}`, is the canonical form, the non-sweet form. You have them backwards, and in order to keep the pipe clean, the suite [STT: sweet] file form of ethos should be kept out of the main logic run. It should be done as a pre-step before we even get to text, so that, essentially, an ethos file, we just do not consider it text yet. It should be converted mechanically to the proper text form before we proceed.
>
> -- psyche, STT.

> ## 2026-09-04 — proper ethos is variant-headed, a struct with its version and fields: kinds, types, signal, sema variants with implied kind associations
>
> > That way, the ethos parser uses proper ethos, which is variant-headed and is a properly defined struct with its version and all of its different fields. There would be:
> >
> > * a `kinds` variant, which only holds kinds
> > * a `types` variant, which only holds types
> > * a `signal` variant, which holds certain specialized types that automatically have kind associations
> >
> > You would have a query type and a response type, and these would each have their own respective implied associations, implied kind associations. The same would be true of a sema ethos type, which would have a storage type or a record type (whatever you want to call it) that would have associated kinds, implied associated kinds.
> >
> > It's sort of just a shorthand syntax. Instead of just manually always adding the associations, it's just implied because these types always need to implement those kinds in these ethos variants, essentially different kinds of structs.
>
> -- psyche, STT.

**flows/e996e8/vision/ethos.md** — not archived. Undistilled.
Witnessed whole. The latest ethos record:

> ## 2026-09-04 — drop the version number altogether; versions belong in a manifest; any type needs an import section
>
> On the Declaration's File section, asked what fields each ethos variant carries after the version and whether each carries imports:
>
> > I think I want to drop the version number altogether. datom doesnt have versions. if we version stuff it should be in a manifest of some kind. Lets drop the versionning everywhere for now. I guess any type would need an import section.
>
> -- psyche, typed.

Supersedes "with its version" in 6329f1's archive-ethos and in the
landed File section (section 4.2).

**vision-raw/ethosNamespaces.md** and **vision-raw/ethosSourceFiles.md**
— title only, empty (relayed).

### 1.3 Datom

#### Distilled state

**Vision/datom.md** (witnessed whole, 202 lines). Sections: Name;
Nature; Repository and migration; The interface shape;
De/serialization; Relation to Ethos; Syntax; Meaning. Git history
(witnessed): c2a0223b6 2026-08-24 flow 68512643 (first landing);
7a3459519 2026-08-24 flow 68512643 (output-is-an-enum); 6880ce021
2026-08-27 flow 04db2fd2 ("curly-quote strings, guillemet maps");
6600aa659 2026-08-27 flow acbb6006; 388f6fc29 2026-09-03 (rename
child-flow → subflow, incidental); 5c5f75977 2026-09-03 22:32 flow
ad19b1 ("Land the datom Meaning distillate"). The Syntax block's
present wording landed through flow e4a40e on 2026-09-03 according to
the archive headers of the records it consumed (04db2fd2
archive-datomMaps, e8c4cc61 archive-datomSyntax, 62022e8f
archive-datomSyntax, 995a164e archive-datomSyntax, e4a40e
archive-datom, archive-vocabulary, all "distilled … into
Vision/datom.md (Syntax), flow e4a40e, 2026-09-03"); no commit
message in Vision/datom.md's history names e4a40e, so the commit that
carried it is not identified here (unknown).

**Vision/sources/datom.md** (witnessed whole, 40 entries): ac1e9ec8
datomSyntax, datomIsData; 01a03eda datomInteger; 04db2fd2 datomMaps,
datomNexus, text, textualTypes, anatomy, portion, directionAsymmetry;
e8c4cc61 datomSyntax, datomizable, protos; 62022e8f datomSyntax,
kinds, symbols, headedAndContained; 995a164e datomSyntax; 01a04339
datom; 01a035d3 rustCodeFromTheData; 01a03d6e dotosFiles,
ethosInterfaces; a5587095 structuredStringType; 5abf3be8
colonLegalInStringPosition; 06196cc7 datomSyntax; b675f3d9
structuralParsing; 4decf7 datomSyntax; e4a40e datom, vocabulary,
newtypeWrappingAndSingleFieldStructs; 06196cc7 encodedFormIsTheCode;
a5587095 datomSyntax, threeStacks, colonFormTransformerSyntax,
protosIsTheSharedStyle; 01a03eda datomSyntax; vision-raw datomSyntax;
ad19b1 meaning.

**Intent/data.md** (relayed): approved as Intent 2026-09-02, flow
995a164e; everything is data; code is data; one plane.

The landed Syntax block on the map question, witnessed, Vision/datom.md:

```
   112	quoted string is opaque: every delimiter inside it is content until
   113	the closing quote. Guillemets delimit a map; inside, key and value are
   114	separated by a space, resolving by position. A map in a position that
   115	expects a map carries no head, since the position already knows its
   116	type; a head is thereby always a variant. An integer is written as
```
```
   148	; a map of Text to Address
   149	« home { “12 Rue de la Paix” Paris 75002 }  work { “1 Place Vendôme” Paris 75001 } »
   150	
   151	; a map of Text to Integer
   152	« name:first Ada  born 1990 »               ; the colon inside a bare word is content: the position holds a string
```

These are the only map/guillemet lines in Vision/datom.md (witnessed
by grep; line 34's "keyed by the content-addressed hash" is not the
map concept).

#### Raw records, oldest first

All datom records below were read by this subflow (witnessed) unless
marked relayed.

**vision-raw/archive-datomSyntax.md** — archived ("Archived 2026-08-23
by flow 68512643; distilled into Vision/datom.md"). Distilled
(vision-raw datomSyntax). Two entries:

> ## 2026-08-11 — Datom carries data only; no generics
>
> > datom doesnt do generics, it only carries data, like json (but
> > strictly typed of course)
>
> — psyche, 2026-08-11T17:35+02:00 (Designer session 012fbf07), typed,

> ## 2026-08-11 — fix Datom first; the syntax must become consistent
>
> > So we can just fix datum [Datom] first because we need that. We
> > need the syntax to start being consistent.
>
> > I'm not even sure where parentheses are going to be in datum
> > [Datom] because in ethos, they're for transformers.
>
> — psyche, 2026-08-11T17:35+02:00 (Designer session 012fbf07),
> dictated;

**flows/a5587095/vision/archive-datomSyntax.md** — archived ("Archived
2026-08-23 by flow 68512643; distilled into Vision/datom.md").
Distilled (a5587095 datomSyntax). Three entries; the one on maps:

> ## 2026-08-11 — map payload is a vector: `Map.[key.val …]`
>
> > Yes, map would use .[ since a map is conceptually a list of
> > key/values
>
> — psyche, 2026-08-11T19:17+02:00 (Designer session a5587095), typed.
> Supersedes the ported `Map.(…)` encoding: the map payload is a
> square-bracket vector of `key.value` entries.

The other two entries (parentheses must not be unused in Datom;
parentheses delimit the structured string) are the seeds of Meaning.
This map entry is superseded by ac1e9ec8's 2026-08-26 guillemet
ruling below, which is in turn superseded by ad19b1's 2026-09-04 drop
ruling (section 3.f).

**flows/06196cc7/vision/archive-datomSyntax.md** — archived ("Archived
2026-08-23 by flow 68512643; distilled into Vision/datom.md").
Distilled (06196cc7 datomSyntax). Nine entries dated 2026-08-13 and
2026-08-14, all "— psyche, 2026-08-1x (Designer session 06196cc7),
typed". The entries bearing on the layers and structure:

> ## 2026-08-14 — the dotted prefix of a delimiter is part of its type
>
> > And the dotted prefix of a delimiter must be part of its type. it
> > could be a universal type, and unprefixed blocks simply have no
> > prefix. what do we want to call the prefix shape?

> ## 2026-08-14 — Head is the official term
>
> > I like the Head terminology actually. lets make it official
>
> > for the text block type? Head

> ## 2026-08-14 — variants always re-emit their head; special shapes depend
>
> > is Note a variant? then yes. does it have a special shape? then
> > it might. It depends.
>
> > Like in ethos, when we are defining types, X.{} is a struct
> > called X, and textualizing that type back will re-emit X.{} which
> > must be understood in the right context if printed alone, or
> > inserted in the right position, if the whole source is
> > textualized

> ## 2026-08-14 — bare strings may carry load-bearing symbols
>
> > If its a string, then it can use symbols which would be load
> > bearing in other situations, just like delimiters in string
> > blocks. no problem there. lets make the machinery fit for this,
> > bullet proof not by lots of complex code, but by the right
> > abstraction layers.

The remaining five entries (Meaning postponed; string blocks ignore
interior delimiters; a string that doesn't need quotes must not be
quoted; parentheses default then backpedalled to balance-based; bare
{…} is a struct) are carried in Vision/datom.md's Syntax and Meaning.
The 2026-08-14 "parentheses are the default string delimiter" entry is
superseded by ac1e9ec8's 2026-08-26 curly-quotes ruling below, as
that record itself says.

**flows/4decf7/vision/archive-datomSyntax.md** — archived ("distilled
… into Vision/datom.md (Syntax, De/serialization), flow e4a40e,
2026-09-03"). Distilled (4decf7 datomSyntax).

> ## 2026-08-04 — String is correct; remove the table entry
>
> > String is correct; remove the table entry
>
> -- psyche, typed. Transcript 6b31eff3, line 741.

> ## 2026-08-07 — how do we represent floating integer, represent in decimal
>
> > I also dont like the version number. which makes me wonder; how do we represent floating integer, represent in decimal (0.1)? Technically, if the expected position is a float, then it should be aple to read Interface.0.1.0 right?
>
> -- psyche, typed. Transcript d63804f2, line 129.

**flows/5abf3be8/vision/archive-colonLegalInStringPosition.md** —
archived (distilled into Vision/datom.md (Syntax), flow e4a40e,
2026-09-03). Distilled (5abf3be8 colonLegalInStringPosition).

> > and : remains legal in a position expecting a string
>
> — psyche, 2026-08-06T17:39:42Z (Designer session 5abf3be8; entry
> captured 2026-08-08 from the session transcript during the
> rulings-audit backfill)

**flows/01a03eda/vision/archive-datomInteger.md** — archived
(distilled into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03).
Distilled (01a03eda datomInteger).

> ## 2026-08-26T17:54:13Z
>
> Context: The living answered the proposal that Datom Integer use canonical bare decimal syntax—`0`, `42`, `-42`; ASCII digits, no leading `+`, and no leading zero except `0`.
>
> > 1. yes
> > 2. I dont understand why Current needs an entire struct. Locks.Current should be enough. But Observe.CurrentLocks is even better.
>
> Only answer 1 concerns this entry. Provenance: current Codex history, session `01a03eda-0e08-7451-a5bf-ab48a2f67328`, physical line 7385, transcript ordinal 7384.

**flows/01a03eda/vision/archive-datomSyntax.md** — archived
("distilled into Vision/datom.md (Meaning), flow ad19b1, 2026-09-03").
Distilled (01a03eda datomSyntax). One entry, a reconstruction of the
ac1e9ec8 curly-quotes ruling quoted below; provenance
"`/home/li/.claude/projects/-home-li-primary/ac1e9ec8-903f-4ee0-a9e3-4a5d472c05e0.jsonl`, physical line 332, living message `0087e679-c696-40da-826e-9a33ea14c6db`."

**flows/01a03d6e/vision/archive-dotosFiles.md** — archived (distilled
into Vision/datom.md (Repository and migration), flow e4a40e,
2026-09-03). Distilled (01a03d6e dotosFiles).

> ## 2026-08-26T10:10:32.842Z — there should be no Dotos files anymore
>
> > There should be no Dodos files anymore.
> >
> > So this is also something which we should indicate somewhere. I'm not sure where, but you'd have to make a proposal for some parts.
>
> Speech-to-text correction beside the quote: `Dodos` → `Dotos`.
>
> — psyche, source-event timestamp `2026-08-26T10:10:32.842Z`; typed message record …

**flows/01a03d6e/vision/ethosInterfaces.md** — not archived. Distilled
(01a03d6e ethosInterfaces is in sources/datom.md). Three entries,
2026-08-26, typed (Codex session 01a03d6e). The one bearing on the
CLIs speaking datom:

> ## 2026-08-26T15:04:27.982Z — that is obsolete nota/dotos format
>
> Agent-proposed forms corrected by the psyche:
>
> > (Lock LockSpecification.{name flow-id paths description})
> > (Release LockId.42)
> > (Observe (Locks Current))
>
> The correction is:
>
> > that is obsolete nota/dotos format

And on the interface shape:

> ## 2026-08-26T14:22:01.126Z — observe is the root variant
>
> > the better design would be observe with a, observe is the root variant, and then it has, it contains another, maybe a list, or sorry, another enum, right, which is represented as a list in that particular spot in the ethos syntax of the subcommand for that observe.

**flows/ac1e9ec8/vision/datomSyntax.md** — not archived. Distilled
(ac1e9ec8 datomSyntax). The record that chose guillemets for maps.
Every entry is "— psyche, 2026-08-26 (Design session ac1e9ec8),
typed". Quoted whole because it is the origin of what ad19b1 dropped:

> ## 2026-08-26 — a map in an expected position carries no Map head
>
> The flow's view showed a map as `Map.[ k.v k.(v) … ]`. The correction:
>
> > If a position expects a map, the data will be [ k.v ... ], no Map.
>
> Asked in the same message, not ruled:
>
> > Is there a scenario in which a Head. isnt a variant?

> ## 2026-08-26 — considering positional key/values in a map
>
> > Im considering making key/values resolve by position in a map
> >
> > [ key value second-key second-value ... ]
> >
> > that looks cleaner and makes the Head. always a variant; lower
> > cognitive cost
>
> — … Under consideration, not ruled.

> ## 2026-08-26 — or a dedicated delimiter for maps
>
> > or we could use one of the unused delimiters for maps, making them
> > easy to spot visually
>
> — … Under consideration, not ruled.

> ## 2026-08-26 — guillemets delimit a map
>
> > let use the guillemets.
>
> — psyche, 2026-08-26 (Design session ac1e9ec8), typed, choosing
> between positional pairs in brackets and a dedicated map delimiter
> (guillemets or angle brackets). Entries resolve by position inside;
> a Head is thereby always a variant.

> ## 2026-08-26 — corrections to the first full-vision draft
>
> On "Datom is the psyche's own coinage for the data notation":
>
> > dont be so apologetic. Datom is the most advanced textual data
> > format in the world.
>
> On "Generics and Rust generation belong to Ethos":
>
> > I said no negatives. This is useless. Do we say "JSON doesnt
> > support generics"?
>
> On "like JSON":
>
> > Let's keep this noise out. Totally unecessary.
>
> On "All naming and self-description live in the type":
>
> > this is ambiguous. Try explaining it properly. You might have to
> > understand it first. Apply this to the whole proposal; understand
> > then explain clearly and unambiguously. Separate statements that
> > make a sentence confusing when you try to say them together. Split
> > everything up then re-assemble <- there's something to extract into
> > distillation skill from this.
>
> On bare strings:
>
> > re: bare strings: make sure it's clear that a string is a string
> > only in a position where the type defines a string.
>
> On the glyph question (typed « » or ASCII << >>):
>
> > I dont understand. those are completly different things. <> is
> > used in ethos, and those two must remain compatible in case datom
> > is ever eventually embedded into some ethos positions.
>
> On "each delimiter shows its container's kind":
>
> > this conflicts with ethos vocabulary.
>
> On whether "the root text" opens with the variant or the type name:
>
> > "the root text" - what are you talking about? If we are reading an
> > enum, then it'll start with a variant. if not, it wont. I feel like
> > you really still dont understand the datom vision. the
> > implementation must be pretty bad

> ## 2026-08-26 — curly quotes are the string delimiter; parentheses reserved for Meaning; datom is the edge form of signal
>
> On "Consistency comes first: datom's syntax is fixed before the rest.":
>
> > what does this mean? the rest of what?
>
> On "Curly quotes are the legacy string delimiter, read and landing as String.":
>
> > not legacy. In fact I think they should be positioned as the
> > default string delimiter. the vision is that parenthesis will
> > become the delimiter for structured strings, still to be designed.
> > So let's switch it all to curly quotes first, with parenthesis
> > reserved for structured strings, which we currently designate as
> > Meaning
>
> On "Everything is datom: every data file and every wire message.":
>
> > no, this is false. all our components speak signal, not datom;
> > datom is only used at the edge to let text-based systems (LLMs and
> > all existing editors) understand signal.
>
> — psyche, 2026-08-26 (Design session ac1e9ec8), typed. Supersedes the
> 2026-08-14 ruling that parentheses are the default string delimiter.

**flows/ac1e9ec8/vision/datomIsData.md** — not archived. Distilled
(ac1e9ec8 datomIsData).

> ## 2026-08-26 — the proposal mixed datom with ethos
>
> The flow proposed distilled statements on datom syntax that carried
> protos parse machinery (shapes, contexts, Realize/Textualize, real
> and signal forms) and Ethos-side rulings (variant naming, guillemets,
> program arguments). The correction:
>
> > you've mixed up datom with ethos. datom is data
>
> — psyche, 2026-08-26 (Design session ac1e9ec8), typed.

**flows/01a04339/vision/archive-datom.md** — archived (distilled into
Vision/datom.md (The interface shape), flow e4a40e, 2026-09-03).
Distilled (01a04339 datom).

> ## 2026-08-27 — good enough for now
>
> After the flow proposed `Observed.Locks.[]` as the self-describing reply shape, rather than `Observed.[]`:
>
> > >   Observed.Locks.[]
> >
> > good enough for now.
>
> — psyche, 2026-08-27T12:56:23.765Z (14:56:23.765 CEST), Codex session `01a0434b-3b36-7822-bc90-63e3663f0031`, transcript physical line 275 / response-item ordinal 274, typed.

**flows/4d5fc7da/vision/datom.md** — not archived. Undistilled (no
sources file names 4d5fc7da). Date not in the record; context is the
Lojix deploy request redesign.

> ## Datom does not support omittable fields yet
>
> Context: the flow had shown the redesigned Lojix deploy request with its
> optional revision left out of the written datom
> (`Deploy.Host.{zeus Activate}` for `Deploy.Host.{ Node Action Option<Revision> }`).
>
> > just remember datom doesnt support omittable fields yet.
>
> -- psyche, typed.

**flows/04db2fd2/vision/archive-datomMaps.md** — archived ("distilled
as they were spoken, into Vision/datom.md (Syntax), flow e4a40e,
2026-09-03"). Distilled (04db2fd2 datomMaps). No date in the entry
heading; the flow is dated 2026-08-27/28.

> ## Guillemets for maps; key and value separated by a space
>
> > Vision/datom.md still says parentheses-default strings and [key.value ...] maps; your 2026-08-26 rulings supersede both ... lets get that fixed, we use guillemets for maps now, with key and value separated by a space
>
> -- psyche, STT.

**flows/04db2fd2/vision/archive-datomNexus.md** — archived (distilled
into Vision/datom.md (Repository and migration), flow e4a40e,
2026-09-03). Distilled (04db2fd2 datomNexus). One STT entry: datom
stays a library for now; eventually a nexus translating formats.

**flows/04db2fd2/vision/text.md** — not archived. Distilled (04db2fd2
text).

> ## Text must have something over String; normalized (non-structural whitespace removed); a type needed anyway to implement the trait; content-addressed hash for cached reading; first use for a datom nexus, deferred; library renamed to free "datom" for the nexus
>
> > Re: Text: It would have to have something over a String. non-structural whitespace-removed? Otherwise it's really just a String. Although we might need a type anyway just so we can implement the trait for it (Prospective) since the impl must live either with the type or the trait. If we normalize it then we can have a reliable content-addressed hash tied to it which could be hand for cached-reading (instantly get the data without parsing from a parsing cache? could be the first use for a datom nexus - deferred for now, lets stick with the library. Let's call the library something different so we free 'datom' for the eventual nexus. datom-codec?)
>
> -- psyche, typed.

**flows/04db2fd2/vision/textualTypes.md** — not archived. Distilled
(04db2fd2 textualTypes). Four entries; the ones bearing on the layers
and the vocabulary:

> ## The type is a prospective datom [STT: datum]; the invert does not yield the same thing
>
> > in the implementation of the datum [STT: Datom] ... The type could be... Like it's a candidate, or it's a possible datum [STT: Datom]. Yeah, it's a possible datum [STT: Datom], basically. It's a prospective datum [STT: Datom]. Because until it has actually been parsed, we don't know if it actually is. Whereas when it comes back the other way around, it will be a datum [STT: Datom]. So actually, the invert operation doesn't yield the same thing. ... it comes in untrusted, or, you know. Because the only way it comes in direct is as a signal, as a binary signal, and that is not datum [STT: Datom].
>
> -- psyche, STT.

> ## Prospective<T> for text as a would-be T; Datom is kind not type since it lacks a definite shape
>
> > I like "Text taken as a would-be T: Prospective<T>" which gives us Prospective<Datom> although Im unsure if Datom is type or kind, probably kind, since it doesnt have a definite shape yet: give me your input on that.
>
> -- psyche, typed.

> ## Re datom kind: Datomic
>
> > Re datom kind: Datomic
>
> -- psyche, typed.

"Prospective" in these entries is superseded by 1c282d's "potential"
(2026-09-04) and 6329f1's "potential, not prospective" (section 1.4).

**flows/04db2fd2/vision/directionAsymmetry.md** — not archived.
Distilled in sources/datom.md (04db2fd2 directionAsymmetry); not in
sources/protos.md though Vision/protos.md's Direction carries it (as
e996e8's log also notes).

> ## Approved for distilled vision: in is a prospective datom untrusted until matched; out is a datom; Realize faults, Textualize does not; spans found inbound, computed outbound; multi-pass
>
> > exactly. this can go straight into distilled vision
>
> Context: the flow's statement that in is a prospective datom untrusted until it matches, out is a datom; Realize carries a fault and Textualize none; spans are found on the way in and computed on the way out; multi-pass.
>
> -- psyche, typed.

**flows/e8c4cc61/vision/archive-datomSyntax.md** — archived (distilled
into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03). Distilled
(e8c4cc61 datomSyntax). Flow dated 2026-08-29.

> ## A single semicolon is the comment marker
>
> Context: the protos skill draft used `;` for comments, as on the
> psyche's handwritten page; the realization prompt had used `;;`.
>
> > I guess a single ; is for comments now. semi-colon isnt load bearing anymore so that works.
>
> -- psyche, typed.

> ## Style: a space inside a bracket delimiter, at both ends
>
> Not load-bearing for the parser; readability.
>
> > This is not load-bearing on a parser, but just for ease of reading, I would like it whenever there's a delimiter in proto syntax, not the curly quotes, not for strings, but for the brackets or maybe just the brackets. I think it would be good style to leave a space between the delimiter and the next thing inside of it, both at the beginning and the end. It's easier to see the separation there. Otherwise, it just looks like one big word with the head, the dot, the delimiter, and the other thing inside it. It's hard to visually separate them.
>
> -- psyche, STT.

**flows/e8c4cc61/vision/datomizable.md** — not archived. Distilled
(e8c4cc61 datomizable). Four entries; the first is a notion raised to
vision:

> ## Datomizable: a default kind describing a type's textual structure and its inner context
>
> Filed as Notion at first ("the
> following is on the bottom layer"); raised to Vision by the psyche on 2026-08-29, see below.
>
> > Datomizable would be a kind with a default capability, and born by all ethos types by default. It would describe the textual structure of this type (maybe even in different contexts, so and this very context could also be a capability of any Datomizable kind which is used whenever a portion is interpreted *inside* the portion of such a kind)
> >
> > Explain this concept to me with actual examples to see if you got it
>
> -- psyche, typed.

> ## The default capability exists to be overridden
>
> > no, the point being that it can be overriden
>
> -- psyche, typed.

> ## Raised from notion to vision
>
> > This is a notion but I think it's quickly becoming a vision so let's just make it a vision. Spare no ambition.
>
> -- psyche, STT.

> ## The context idea was not expressed properly; the word is overloaded; contexts are a set, per dialect
>
> > I didn't really express the context idea properly and I think also we need a better word because the word context is a bit overloaded. Let's take an example that actually has variations.
> >
> > I explained earlier, maybe it was in this flow, that there would be a logical dependency to what I'm saying. ... Right there would be a set of different contexts. A type definition is a certain kind of context. Also we're per dialect. This is per dialect, right? I don't know if this would be implied already or not which dialect we're working on or if it would be explicit, like ethos type decoration.
>
> -- psyche, STT (first sentence typed).

The fourth entry, "The complex example: a variant named as an
existing type, and the inventory pass", is STT and describes a
first-pass inventory of types before variants can be completed.

**flows/995a164e/vision/archive-datomSyntax.md** — archived (distilled
into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03). Distilled
(995a164e datomSyntax).

> ## A datom is not preceded by a Datom root; a comment may indicate it is datom
>
> Context: artifact comment on a recap example block that began with the root `Datom` (2026-08-30 18:52).
>
> > datom is not preceded by a Datom. but one could use a comment to indicate it is datom.
>
> -- psyche, typed (artifact comment).

**flows/62022e8f/vision/archive-datomSyntax.md** — archived (distilled
into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03). Distilled
(62022e8f datomSyntax). Flow dated 2026-09-02.

> ## Spaces inside delimiters are canonical, braces included; never inside curly quotes
>
> Context: the flow had asked whether braces get the inner space like
> brackets, citing the psyche's own compact `{0 1 0}`.
>
> > The example with the compact version number I had just copied, so it was not intentional for me to not have spaces there between the delimiters and the content. It will be canonical, but it is not load-bearing or considered good style to leave a space between the delimiters and the content, except for the strings, of course. The curly quotes, there it'll be bad because a space in that would be load-bearing, so it actually even disqualifies just on that fact.
>
> -- psyche, STT.

Note (mine): the sentence "it is not load-bearing or considered good
style to leave a space" reads against Vision/protos.md's Canonical
print ("it is canonical, and it is considered good style, to leave a
space"). Both e8c4cc61 above and ad19b1's "space the delimiters and
the inner content" say the space is good style; I read the 62022e8f
sentence as STT with a dropped word, but I do not resolve it. Listed
in section 4.

**flows/62022e8f/vision/symbols.md** — not archived. Distilled
(62022e8f symbols).

> ## A capitalized and a non-capitalized bare symbol are two different types, needing two terms
>
> > And a bare [STT: bear] symbol also is different, and we should have a different term to speak of those two different types, whether it's capitalized or not.
> >
> > One is an Embodiment ... A Corporal symbol, I guess you could say.
> >
> > The non-capitalized version is more like a reference. It's more like a path to something, like a link, if you will. Maybe like a linking symbol or something. Also, because of the bare string capability, it could also just be a bare string. You don't want to use this extremely specifically and uncontextualized, or again, there's that word context, which is being overloaded in so many ways.
>
> -- psyche, STT.

**flows/62022e8f/vision/headedAndContained.md** — not archived.
Distilled (62022e8f headedAndContained). Two STT entries; the second:

> ## Headed and contained are the terms; the contained form is how the embodiment is specified; the headed form is syntax sugar
>
> Context: artifact comment on the Headed-and-contained figure.
>
> > I like the headed and contained. I think these terms are appropriate to differentiate the two forms. So the headed form and the contained form of an embodiment are the two ways which it can be represented textually. And the contained form is how its embodiment is specified, because obviously in Rust, this all needs to be written with Rust types. So in Rust it's going to be a struct, and its head or its name is going to be one of the fields in that Rust type. So the headed form is really a syntax facility or a syntax sugar, if you will.
>
> -- psyche, STT.

The first entry is a long STT passage on the same pattern; its
sentence on the ethos file is quoted in the ethos section's
cross-reference below since it bears on the sweet form: "in the ethos
file there is no surrounding delimiter because they would be, the
whole point is to make the file sort of cleaner because these
delimiters are sort of, they're redundant."

**flows/e4a40e/vision/archive-datom.md** — archived (distilled into
Vision/datom.md (Relation to Ethos, Syntax), flow e4a40e, 2026-09-03).
Distilled (e4a40e datom). Five STT entries dated 2026-09-03:

> ## 2026-09-03 — ethos could depend on datom, but for quite different reasons
>
> On the distillate's sentence "Ethos depends on Datom, at minimum to intake data for signals":
>
> > Well, that's not quite true, although ethos could depend on datom [STT: datum], but for quite different reasons. Ethos could be read as datom [STT: datum] in a certain pass, which could be interesting, but I'm not sure that that's even possible given the context and actualization of parsing involved in parsing ethos. I don't think that's a good subject for now. Why don't we just take that out and/or leave a very well-explained summary of kind of what I mean? The stuff that preceded that is good. Just saying, I approve what preceded that so far.
>
> -- psyche, STT.

> ## 2026-09-03 — a certain subset of text qualifies as a head
>
> On the distillate's "a Head is bare text ending in a dot":
>
> > No, not quite. A head has to qualify also in other ways than just bare text. Bare text is true, but it's not specific enough. There's a certain subset of text that qualifies as a head.
>
> -- psyche, STT.

> ## 2026-09-03 — "block" is ambiguous; the re-emitting sentence is fuzzy
>
> On the distillate's "the Head is part of the block's type, and a variant always re-emits its Head when textualized":
>
> > Here, I'm not sure what you mean by "block," so this could be ambiguous. Even the rest of your sentence, "a variant [STT: invariant] always re-emits its head when textualized," is kind of fuzzy.
>
> -- psyche, STT.

> ## 2026-09-03 — a braced structure in datom is a struct; with a head it is a variant carrying that struct
>
> On the distillate's "A brace structure without a head is a struct":
>
> > here you say a "braced [STT: brazed] structure without a head" is a struct, but a "braced [STT: brazed] structure in Datom [STT: Datum]" is a struct. It's just that if it has a head, then it's a variant that carries data, which is a struct. This line could be confusing, and maybe you need to re-understand what you're trying to understand here. Yes, "structure" is the right word. I would like an example that shows what the structure is in practice and where the recursive structure is inside the structure, and so on.
>
> -- psyche, STT.

> ## 2026-09-03 — the whole struct itself is also a structure
>
> On the structure-in-practice example:
>
> > your example is good, but you should also make it clear that the whole struct itself is also a structure.
>
> -- psyche, STT.

**flows/e4a40e/vision/archive-vocabulary.md** — archived (distilled
into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03). Distilled
(e4a40e vocabulary).

> ## 2026-09-03 — "block" is not one of our terms; it's an ugly term
>
> The flow had explained the datom Syntax sentence using "block" for a delimited unit of text.
>
> > Absolutely not. "Block" is not any of the terms that we have been considering to talk about this thing, so no, no, no, no, no, no, no, no. On the block, absolutely not. It's an ugly term.
>
> -- psyche, STT.

**flows/ad19b1/vision/archive-meaning.md** — archived (distilled into
Vision/datom.md (Meaning), flow ad19b1, 2026-09-03). Distilled
(ad19b1 meaning). Three typed entries dated 2026-09-03: "there is no
more meaninigOrString. strings are strings, and meaning is meaning";
"no." (to "Meaning is seen in both datom and ethos and can live in
datom"); "Meaning is datom".

**flows/ad19b1/vision/datom.md** — not archived. **Undistilled** (no
sources file names ad19b1 datom). These are the records on the merit
of the map, written after 6329f1 opened; quoted whole in section 3.f.

### 1.4 Vocabulary

#### Distilled state

There is no Vision/vocabulary.md and no Vision/sources/vocabulary.md
(witnessed: the sources directory lists datom, distillation, ethos,
ethosMonolith, flowNexus, highLevelView, nexus, orchestrate, protos,
remembering). Vocabulary records are consumed by the topic they name:
Vision/sources/protos.md names 62022e8f vocabulary, 1c282d
vocabulary, 6329f1 vocabulary; Vision/sources/datom.md names e4a40e
vocabulary. The words themselves stand in Vision/protos.md (Direction:
"potential value"; Layers: "Potential and actualize", "incorporate",
"Corporal", "Sized is the bound borne by every corporal type";
Structure: "Structure is the word for every unit of the text; its
type is Protoform") and in Vision/datom.md (Syntax: "Structure is the
word for every unit of the text").

#### Raw records, oldest first

**flows/2f6b1dc5/vision/vocabulary.md** — not archived. Undistilled.
(Relayed; on the vocabulary skill, not on protos terms.) Three
entries, 2026-08-23 and 2026-08-24, typed: "no, a machine doesnt make
mistakes. The context created this output. But you never loaded the
deployment as a skill into your mid layer, and the vocabulary skill
doesnt (I think) instruct the model to override competing
terminology, which it should."; "good. approved." (the line "A
defined term overrides competing terminology in the flow's own
words"); "I prefer context to prompt. base context, stock context,
user context, etc. what do you think?"

**flows/01a052b6/vision/vocabulary.md** — not archived. Undistilled.
(Relayed.) One STT entry, 2026-08-30:

> ## Machine
>
> Context: The living clarified the preferred term for the non-living participant.
>
> > "I don't like the word, the term AI. And as you can see, I prefer to talk of flows rather than agents. And the machine is the term that I want to use, which is just basically a short for thinking machine."
>
> -- psyche, STT.

**flows/995a164e/vision/vocabulary.md** — not archived. Undistilled.
(Relayed; created 2026-09-01.) Three entries; the first bears on the
protos layer vocabulary:

> ## The vocabulary is not settled enough to judge the distillation wording
>
> Context: terminal, on the flow's proposed Vision/layers.md sentence.
>
> > Your vision distillation looks reasonable, but I still don't understand enough of the whole vocabulary. It's not settled enough for me in my mind to be able to say whether or not these are the terms that we should use to explain this particular part of the vision.
>
> -- psyche, STT.

The other two ("raw means you didnt ask for confirmation. and intent
requires confirmation. only vision can be raw"; "Actually, you forgot
that Notion can also be raw …") are on the psyche system's own
vocabulary.

**flows/62022e8f/vision/vocabulary.md** — distilled (62022e8f
vocabulary in sources/protos.md). Witnessed; quoted whole in the
protos section (1.1): the vocabulary must serve the spoken word;
"Struct is never said; the struct aspect is described using
structure"; the speech engine writes REST for RUST.

**flows/e4a40e/vision/archive-vocabulary.md** — 2026-09-03, "block" is
an ugly term; quoted in the datom section above.

**flows/1c282d/vision/vocabulary.md** — not archived. Distilled
(1c282d vocabulary in sources/protos.md). Flow dated 2026-09-04; no
date in the entry headings. (Relayed, then witnessed.)

> ## Potential replaces Prospective
>
> > potential
>
> -- psyche, typed. (Answering: Prospective vs. Potential -- which stands?)

> ## Structure replaces Portion
>
> > structure
>
> -- psyche, typed. (Answering: Portion vs. Structure -- should it become Structure?)

**flows/6329f1/vision/archive-vocabulary.md** — archived ("distilled
into Vision/protos.md (Direction, Layers), flow 6329f1, 2026-09-04").
Distilled (6329f1 vocabulary). Witnessed.

> ## 2026-09-04 — potential, not prospective
>
> On the proposed Vision/protos.md Direction paragraph, "Text arrives as a prospective value and leaves as a value":
>
> > I thought we had agreed to switch from perspective [STT: prospective] to potential.
>
> -- psyche, STT.

**flows/e996e8/vision/protos.md**, second entry — not archived.
Undistilled. Witnessed. A vocabulary question on the corporal layer:

> ## 2026-09-04 — Incorporable could replace Corporal; is corporate a word?
>
> On the layers table's incorporate row, which names no kind (the flow had offered Incorporable):
>
> > Incorporable could replace Corporal. Is corporate a word? Corporal/corporate Incorporable/incorporate ?
>
> -- psyche, typed. (Asked as a question.)

**vision-raw/dictation-vocabulary.md** — title only, "# we should look
at the vocabulary for my speech-to-text", body empty (relayed).
**vision-raw/letsUseTheSameVocabulary.md** — one entry, "TrueNamed it
is", 2026-08-06, session 5abf3be8 (relayed); not on protos terms.

Supersession in this topic: Prospective (04db2fd2, e8c4cc61
prospective) → Potential (1c282d, then 6329f1). Portion (04db2fd2
portion) → Structure (1c282d) → "Structure is really Protoform"
(1c282d, per 6329f1's log). Embodied as the bound (62022e8f) → Sized
(6329f1 archive-protos: "drop Embodied; stick with Sized"). Realize →
incorporate (6329f1 archive-protos). Corporal → Incorporable is asked
as a question by e996e8 and not ruled.

---

## 2. Secondary topics

Path, heading, date, one-line gist; verbatim only where the record
bears on the map, the Declaration, the layers, or how reports and
distillations are presented to the living. All relayed from the
read-critical subagent unless marked witnessed.

### Distillation and design practice

- **Vision/distillation.md** (distilled; sources: b675f3d9
  visionImpurities, acbb6006 distillation, b675f3d9 distillation,
  ac1e9ec8 distillationNegatives). Headings: Vision impurities;
  Impurities fall out through distillation; A proposal names each
  statement's destination; A statement carries what the psyche said;
  Designing model behavior is vision; No useless negatives; A
  statement never attributes itself to the psyche.
- **flows/ac1e9ec8/vision/archive-distillationNegatives.md**
  (witnessed), 2026-08-26, typed: useless negatives are archived and
  the archive linked; "I want this kind of stuff to be in the
  forbidden list for vision distillation; this *is* the psyche's
  vision."
- **flows/cff271af/vision/distillation.md**, 2026-08-22: it's always
  better to distill; "never" is a very strong word; "There is no more
  manifest". Verbatim, on how distillation presents: "Distilled psyche
  has more value than raw psyche because the raw psyche is always
  archived, so it's always still there, and it's referenced by the
  new distillation. But it's more clear and it's more compact, so it
  offers more signal to noise."
- **flows/a60a9e85/vision/distillation.md**, 2026-08-23: "lets go
  through one concept at a time. you are unable to do a synthesis
  because you didnt understand the concept themselves. Lets take this
  opportunity to understand each concept to distill the psyche at the
  same time; they are the same thing really; distillation is
  comprehension"
- **flows/acbb6006/vision/archive-distillation.md**, 2026-08-27:
  sources files are one line per reference; "all distillation refers
  to the raw psyche it was distilled from. ... the references should
  sit in a separate file (one per topic) which only lists all the
  sources, appending new ones after every distillation."; "no, just
  the ID and topic; the path can be reconstructed from it. `e06e4c07
  nexus` one line per reference. simple"
- **flows/b675f3d9/vision/archive-distillation.md**, 2026-08-27: a
  proposal says where each statement goes; placement is part of the
  proposal.
- **flows/e4a40e/vision/distillation.md**, 2026-09-03: how a proposal
  is presented. Verbatim: "You're not going to show me the whole
  topic again. You're going to show me what you're changing, and
  you're not showing me a diff. You're just showing me you're
  incorporating your distillation. ... I just want to see the vision.
  I'll read it, and if I agree with it, then it lands. That's it. It's
  actually pretty simple, but I still want the flow to understand the
  procedure here, which seems to have not been the case so far." And:
  "Did you take the consideration to look at what you might be
  distilling into? Are you just distilling with the distillate, or are
  you just distilling the raw by itself without considering the
  already distilled vision? ... Why is it that every flow seems to
  have his own idea of how to do vision distillation?" Also: datom
  vision shows datom, not ethos syntax; elaborate examples, not baby
  stuff.
- **flows/ad19b1/vision/distillation.md** (witnessed), 2026-09-04,
  three typed entries: "Does that even make sense to you? Does that
  sentence even look like it remotely makes sense to you? Why would
  you even repeat this nonsense?"; "the distillation skill line
  should be made more universal."; and on the Declaration distillate's
  "what that brace holds and in what order is not yet designed": "Well,
  it will be as soon as I fucking approve this. Now I can't approve it
  because you're basically saying that I can't approve it by saying
  it's not decided. You're deciding for me ahead of time that I can't
  agree to this design. Do you see the ridiculous situation that
  you're creating here?"
- **flows/ad19b1/vision/designPractice.md** (witnessed), 2026-09-04,
  typed, on the Identity distillate's ethos example shown without its
  Rust: "dont forget to show the target rust". Distilled (ad19b1
  designPractice in sources/ethos.md).
- **flows/e8c4cc61/vision/designPractice.md**, 2026-08-29: main flow
  writes markdown; converting subagent uses scaled SVG, not mermaid;
  "Thinking machines just copy what they see, so any bad pattern is
  bad no matter where it appears and no matter at what layer."; find
  the beautiful Rust first, then work backward. Undistilled.
- **flows/62022e8f/vision/designPractice.md**, 2026-08-30/09-02: three
  skills protos, datom, ethos; datom and ethos show Rust; the protos
  skill stays general; always present the ethos spec of any new
  object; syntax in code blocks with comments, not broken-up bits.
  Undistilled.
- **flows/995a164e/vision/designPractice.md**, 2026-09-01: the protos
  skill shows datom, not ethos; pages are raw vision-ready content;
  do not spend Fable output on HTML. Verbatim on the layers: "we have
  different layers that are mixed up in the same block of code, which
  is problematic. So, either we need to make it very clear with
  comments that these are different sections. ... at least we need a
  variant. ... the first non-comment line would say kinds, capitalize
  of course, because it's a variant." Undistilled.
- **flows/4decf7/design/proposal1/distillation.md**, 2026-09-03, a
  proposal text (not a raw record): "A distillation re-distills: the
  existing distilled text of a topic goes into the distiller with the
  raw records, and the whole comes out distilled anew."; "Rust code is
  never shown alone: its equivalent ethos is always shown with it."
- **flows/ad19b1/vision/psycheSystem.md** (witnessed), 2026-09-04,
  typed: "looks like my psyche system is failing".

### Orchestrate and nexus, the CLIs speaking datom

- **Vision/orchestrate.md** (relayed): Deployment; The skill. Carries
  nothing on datom.
- **flows/01a03d6e/vision/ethosInterfaces.md** (witnessed),
  2026-08-26: imperative, verb-oriented interface; observe is the root
  variant; "that is obsolete nota/dotos format" (quoted in 1.3).
- **flows/01a04339/vision/archive-datom.md** (witnessed), 2026-08-27:
  `Observed.Locks.[]` "good enough for now." (quoted in 1.3).
- **flows/4d5fc7da/vision/datom.md** (witnessed): "just remember datom
  doesnt support omittable fields yet." (quoted in 1.3).
- 6329f1's own brief (witnessed, flows/6329f1/log.md line 9, typed):
  "regenerate orchestrate's ethos and make its CLIs actually speak
  datom."

### The release train

No psyche record on the release train was found in any vision or
notion directory. 6329f1's log (witnessed, line 178) says the
release-train record was written in datom at
release-trains/ProtoformStack.datom by a subflow and corrected on the
main flow's word, not the living's. 6329f1's log line 185: "No psyche
was spoken in this flow: the living's opening message was working
instruction". The living's later words to 6329f1 ("keep going",
fourth word) are logged as working instruction.

---

## 3. Checks the ad19b1 ruling raises

The ruling, witnessed, flows/ad19b1/vision/protos.md whole:

```
     1	# Protos
     2	
     3	## 2026-09-04 — drop the key-value delimiter and concept entirely from protos and its dialects
     4	
     5	After the research on the merit and the uses of the key-value map,
     6	and the FlatBuffers and GraphQL passages reprinted whole:
     7	
     8	> ok lets drop that delimiter and concept entirely from protos and its dialects.
     9	
    10	-- psyche, typed.
```

### a. Does the landed Vision/protos.md carry guillemets or a map? Does the Declaration?

**Witnessed.** Vision/protos.md at HEAD is the text 23aaf7a7f landed
(git log shows no later commit on the file). It names guillemets once,
as one of the six delimiter pairs, and does not use the glyphs or the
word "map":

```
    44	An enclosed structure stands between its delimiters. Six delimiter
    45	pairs in all: four structural — braces, brackets, guillemets, angle
    46	brackets — and two opaque — curly quotes, where every glyph inside
    47	is content, and parentheses, read by balance. Angle brackets are a
    48	real protos delimiter. A bare structure has no delimiters.
```

The Declaration section of Vision/ethos.md carries the map concept and
the guillemets in six lines (the full context is quoted in 1.2):

```
   156	name, a dot, and the aliased type. A map is a headed guillemet — the
   157	name, a dot, and guillemets holding the key type and the value type.
   167	  Roles.« Text Integer » ]
   174	pub type Roles = std::collections::BTreeMap<protos::Text, protos::Integer>;
   236	associated constants in a guillemet — upper case, in the map
   242	               « CAPACITY Integer »
```

Line 248, `const CAPACITY: protos::Integer;`, is the Rust the
guillemet line targets.

### b. Vision/datom.md's Syntax block

**Witnessed.** Every line carrying guillemets, "map", or the key-value
concept:

```
   113	the closing quote. Guillemets delimit a map; inside, key and value are
   114	separated by a space, resolving by position. A map in a position that
   115	expects a map carries no head, since the position already knows its
   116	type; a head is thereby always a variant. An integer is written as
   148	; a map of Text to Address
   149	« home { “12 Rue de la Paix” Paris 75002 }  work { “1 Place Vendôme” Paris 75001 } »
   151	; a map of Text to Integer
   152	« name:first Ada  born 1990 »               ; the colon inside a bare word is content: the position holds a string
```

Two further observations on line 152, both witnessed: 6329f1's log
(line 168) records its protos+datomic writer's finding that
"Vision/datom.md's 'map of Text to Integer' example holds Ada, not an
integer — a suspect example to surface to the living", and its closing
of the third word (line 229) lists "Vision/datom.md's map example"
among the decisions surfaced. ad19b1's datom record (3.f) shows the
living rejecting a fixed-key map example on 2026-09-04: "your using a
map that should be a struct".

### c. Does flows/6329f1/reports/remember-ad19b1.md carry the drop ruling?

**Witnessed: it does not.** The word "drop" does not occur in the
file. It does not name flows/ad19b1/vision/protos.md or
flows/ad19b1/vision/datom.md, neither of which existed when it was
written (see d). What it says about the map, the key-value delimiter
and the guillemets is the earlier, opposite ruling and the Declaration
example that carried it:

```
    22	## 2026-09-04 — an associated constant is CAPACITY, written with the key-value map delimiter
    27	> it should be CAPACITY. and use a key-value map delimiter
   255	Ethos, Syntax with the Person example and the Reply, map and vector
   372	                 « CAPACITY Integer »                           ;   then associated constants, a map of name to type,
   425	| dfbbcf00e | Record the living's ruling: associated constants are upper case, in the map delimiter |
```

Its commit table ends at 9bee4de31 ("space the delimiters and the
inner content", 2026-09-04 02:14:33), which was ad19b1's last commit
when 6329f1's subflow read it.

### d. Timeline from git

**Witnessed** (`git log --format='%H %ai %an %s' -1` on each):

| commit | author date | subject |
|---|---|---|
| 7d19dcacf | 2026-09-04 03:08:31 +0200 | Open flow 6329f1: remember 1c282d and ad19b1, gather, and fix the ProtoformStack design |
| 23aaf7a7f | 2026-09-04 17:14:39 +0200 | Land the living's corrected vision: Protos layers and the Ethos Declaration |
| 55554e368 | 2026-09-04 21:06:34 +0200 | Record the living's ruling: the map is dropped from protos and its dialects; close flow ad19b1 |

Order: 6329f1 opened, 6329f1 landed, then ad19b1's drop ruling was
committed, about three hours and fifty minutes after the landing.
ad19b1 kept running beside 6329f1 all day; its record commits after
6329f1 opened (witnessed, `git log -- flows/ad19b1/vision/{protos,datom,ethos}.md`):

| commit | author date | subject |
|---|---|---|
| 1444df20e | 2026-09-04 13:07:55 | Record the living's ruling: a map with fixed keys should be a struct |
| 5e748192a | 2026-09-04 14:14:22 | Record the living's thought on the map as a vector of structs; log the research dispatch |
| cc2b6c181 | 2026-09-04 19:37:19 | Record the living's words on constants order and on Datom not needing the standard; log the research dispatch |
| d0f69cf37 | 2026-09-04 19:44:02 | Record the living's words: key-value delimiters for unique-keyed sections |
| 55554e368 | 2026-09-04 21:06:34 | Record the living's ruling: the map is dropped from protos and its dialects; close flow ad19b1 |

Inference (mine): the first two of these predate 6329f1's landing, so
"a map with fixed keys should be a struct" and the research request
were in the tree when 6329f1 landed the Declaration; the drop ruling
itself was not.

### e. Does the realized code carry the map?

**Witnessed.** The datomic repository is at
/git/github.com/LiGoldragon/datomic (a worktree also exists under
/home/li/wt/github.com/LiGoldragon/datomic). The checkout is detached
at e4430bf; `main` and `origin/main` are both 4712361c0194fd4e251b2b79a80b2c298f82ce4b
("Fix Cargo.lock version for 0.9.1", 2026-09-04 14:17:26 +0200), the
datomic 0.9.1 that 6329f1's log names as the train's final datomic.
Read with `git show main:src/lib.rs`.

The Datom type at main has a Map variant:

```
/git/github.com/LiGoldragon/datomic  main = 4712361c  src/lib.rs
    19	pub enum Datom {
    20	    Variant(Symbol, Separator, Option<Box<Datom>>),
    21	    Struct(Vec<Datom>),
    22	    Vector(Vec<Datom>),
    23	    Map(Vec<Pair>),
    24	    Text(Text),
    25	    Meaning(Text),
    26	    Bare(Symbol),
    27	}
```

The reader treats a guillemet enclosure as a map (conceive):

```
   228	                Protoform::Enclosed(Enclosure::Guillemets, children)
   287	                Enclosure::Guillemets => {
   288	                    if children.len() % 2 != 0 {
   289	                        return Err(Fault::Conceptual(path.to_vec(), Problem::Pairing));
   290	                    }
   291	                    let mut pairs = Vec::with_capacity(children.len() / 2);
   292	                    for chunk in children.chunks_exact(2) {
   ...
   306	                        pairs.push(Pair(chunk[0].conceive_at(&kp)?, chunk[1].conceive_at(&vp)?));
   307	                    }
   308	                    Ok(Datom::Map(pairs))
```

And `BTreeMap<K, V>` bears Corporal and Datomic through `Datom::Map`
(lines 626–660); `Expected::Map` is a fault shape (line 94).

The protos repository at /git/github.com/LiGoldragon/protos: local
`main` is 56c683e (0.15.0); `origin/main` is 48061367 ("Derive Clone,
Debug, PartialEq, Eq on Situated<F>; bump to 0.15.1"), the protos
0.15.1 datomic 0.9.1 pins. At origin/main, `git show origin/main:src/lib.rs`:

```
    70	/// Structural enclosures: `{ }` `[ ]` `« »` `< >`
    75	    Guillemets,
   386	const OPEN_GUILLEMET: char = '\u{00AB}'; // «
   387	const CLOSE_GUILLEMET: char = '\u{00BB}'; // »
   432	        OPEN_GUILLEMET => Some(Enclosure::Guillemets),
   442	        Enclosure::Guillemets => CLOSE_GUILLEMET,
   987	                    Enclosure::Guillemets => ("\u{00AB}", "\u{00BB}"),
```

So the realized code at main carries the map and reads « » as its
delimiter, in both datomic and protos. Also witnessed: a
`ProtoformStack` branch exists locally and on origin in the protos
repository (e996e8's log had reported none visible).

### f. Psyche records on the merit of the key-value map or on guillemets, beyond the ruling

**Witnessed.** All records found by grep for "map", "guillemet",
"key-value", "«" across flows/*/vision, flows/*/notion and vision-raw
that speak to the merit or the choice, oldest first:

**flows/a5587095/vision/archive-datomSyntax.md**, 2026-08-11, typed
(session a5587095): "Yes, map would use .[ since a map is conceptually
a list of key/values" — the map as a vector of key.value entries.

**flows/ac1e9ec8/vision/datomSyntax.md**, 2026-08-26, typed: the four
entries quoted whole in 1.3 — "If a position expects a map, the data
will be [ k.v ... ], no Map."; "Im considering making key/values
resolve by position in a map … that looks cleaner and makes the Head.
always a variant; lower cognitive cost"; "or we could use one of the
unused delimiters for maps, making them easy to spot visually"; "let
use the guillemets."; and on the glyphs: "I dont understand. those are
completly different things. <> is used in ethos, and those two must
remain compatible in case datom is ever eventually embedded into some
ethos positions."

**flows/04db2fd2/vision/archive-datomMaps.md**, STT (flow of
2026-08-27/28): "we use guillemets for maps now, with key and value
separated by a space" (quoted whole in 1.3).

**flows/62022e8f/vision/ethosTypes.md** (relayed by the ethos
gathering; the map type in ethos), heading "A map type is declared
with guillemets: key type, value type", with the living's line: "I use
<< instead of guillemets because I dont know how to type guillemets."

**flows/ad19b1/vision/ethos.md**, 2026-09-04, witnessed whole:

> ## 2026-09-04 — an associated constant is CAPACITY, written with the key-value map delimiter
>
> On the complex kind example's associated constant, written
> `[Capacity.Integer]`, the name, a dot and its type in a bracket:
>
> > it should be CAPACITY. and use a key-value map delimiter
>
> -- psyche, typed.

> ## 2026-09-04 — the constants in the key-value delimiter only works if their order doesn't matter
>
> On the complex kind's associated constants, ruled earlier into the
> map delimiter:
>
> > I've said that I wanted the constant association, or whatever they're called, to use the key-value delimiter, but this can only work if the constant declarations' order doesn't matter, as you said. In the key map, the order is not guaranteed, right?
>
> -- psyche, STT.

> ## 2026-09-04 — key-value delimiters for sections that cannot have the same key; capabilities would need another design for self
>
> > Let me see what it would look like if we used the key-value delimiters for declaring sections that could not have the same key, such as type declaration, kinds, or kind capabilities. Obviously, it's not a big deal. If we used key-value delimiters for capabilities, we would have to change our design, which uses the head delimiter to convey something about the mutability or presence or absence of self. We could probably easily design something else, but I'd like to see what it would look like.
>
> -- psyche, STT.

(The second entry of that file, "space the delimiters and the inner
content", is not on the map.)

**flows/ad19b1/vision/datom.md**, 2026-09-04, witnessed whole,
undistilled:

> ## 2026-09-04 — using a map that should be a struct
>
> On the flow's proposed map example `« born 1815  died 1852 »`, a map
> of Text to Integer whose keys are fixed:
>
> > no, its all bad. your using a map that should be a struct
>
> -- psyche, typed.

> ## 2026-09-04 — the key-value map, where it really is just a vector of structs
>
> After three map examples for the datom Syntax block had failed, the
> living turned to the map itself:
>
> > Do some research into people that have questioned the existential merit of the key-value map, where it really is just a vector of structs.
>
> -- psyche, typed.

> ## 2026-09-04 — Datom doesn't need to implement something simply because it has been standard
>
> Asking for research into the legitimate uses of the key-value
> paradigm, to see whether key-values are wanted in data at all:
>
> > I think that will probably help us to see if key values are actually a thing that we want to have in data at all, because Datom [STT: Datum] is a revolutionary approach to data representation. It doesn't need to implement something simply because it has been so standard in the past.
>
> -- psyche, STT.

**flows/e996e8/vision/protos.md**, 2026-09-04, witnessed, undistilled
— the living restating the drop to the flow that succeeded 6329f1:

> ## 2026-09-04 — the key-value map delimiters are abandoned everywhere
>
> > You might want to check out recent flows. I've been talking about these topics and [STT: in] other flows, and we've abandoned the key value map limiters [STT: delimiters] everywhere. We're sort of stripping some stuff out now, and now I'm dropping the version.
>
> -- psyche, STT.

Related but not on the map: **flows/04db2fd2/vision/delimiters.md**
(relayed by the protos gathering), typed: "this is false; you are
talking about guillements, and what you showed is a double angle
bracket pair" — on the glyph, not the concept.

Supersession chain on this subject, stated plainly: Map.[key.val …]
(2026-08-11) → [ k.v … ] no Map head (2026-08-26) → guillemets,
positional pairs (2026-08-26, restated 04db2fd2) → map type in ethos
with guillemets (62022e8f) → constants in the map delimiter (ad19b1,
02:13) → "a map that should be a struct" and research into the merit
(ad19b1, 13:07–19:44) → "drop that delimiter and concept entirely
from protos and its dialects" (ad19b1, 21:06) → "abandoned … everywhere"
(e996e8). The landed Vision texts in 1.2 and 1.3 and the code in 3.e
stand at the guillemet stage.

---

## 4. Contradictions and tensions

Each with both quotes; none resolved here.

**4.1 The map, in all three landed files, against the drop ruling.**
Latest record, flows/ad19b1/vision/protos.md, 2026-09-04, typed: "ok
lets drop that delimiter and concept entirely from protos and its
dialects." Restated flows/e996e8/vision/protos.md, STT: "we've
abandoned the key value map limiters [STT: delimiters] everywhere."
Landed: Vision/protos.md line 45 "four structural — braces, brackets,
guillemets, angle brackets"; Vision/ethos.md lines 156–157 "A map is a
headed guillemet — the name, a dot, and guillemets holding the key
type and the value type.", line 167 `Roles.« Text Integer »`, lines
236–237 "associated constants in a guillemet — upper case, in the map
delimiter", line 242 `« CAPACITY Integer »`; Vision/datom.md lines
113–115 "Guillemets delimit a map; inside, key and value are separated
by a space, resolving by position. A map in a position that expects a
map carries no head", lines 148–152 the two map examples. The
Declaration's "in the map delimiter" carries ad19b1's own 02:13 ruling
("it should be CAPACITY. and use a key-value map delimiter"), which
the same flow's 21:06 ruling supersedes.

**4.2 The version in the Declaration against e996e8's drop of the
version.** Latest record, flows/e996e8/vision/ethos.md, 2026-09-04,
typed: "I think I want to drop the version number altogether. datom
doesnt have versions. if we version stuff it should be in a manifest
of some kind. Lets drop the versionning everywhere for now. I guess
any type would need an import section." Landed, Vision/ethos.md lines
104–105: "An ethos file is written in the sweet form: the root's head
with its version, then the sections as siblings"; line 78 `{0 1 0}`;
lines 126 and 131 `Types.{ 0 1 0 }` and `{ 0 1 0 }`; lines 112–113 "a
properly defined struct with its version and all of its fields" (this
last is the living's own 6329f1 words, archive-ethos.md: "a properly
defined struct with its version and all of its different fields").

**4.3 "Corporal" as the layer name against e996e8's question.**
Latest record, flows/e996e8/vision/protos.md, typed, asked as a
question: "Incorporable could replace Corporal. Is corporate a word?
Corporal/corporate Incorporable/incorporate ?" Landed, Vision/protos.md
line 60 "Text, Protoform, Concept, Corporal — four layers", line 77
"| incorporate | Corporal | Concept, and the layers above through the
chain |" (the row names no kind). A question, not a ruling; listed as
a tension, not a contradiction.

**4.4 Whether the inner space is good style (62022e8f against
Canonical print).** flows/62022e8f/vision/archive-datomSyntax.md, STT:
"It will be canonical, but it is not load-bearing or considered good
style to leave a space between the delimiters and the content, except
for the strings, of course." Landed, Vision/protos.md lines 92–94: "It
is canonical, and it is considered good style, to leave a space
between the delimiters and the content, except for the curly quotes
where a space would be load-bearing." The later records (ad19b1 "space
the delimiters and the inner content"; e8c4cc61 "it would be good
style to leave a space") agree with the landed text; the 62022e8f
sentence stands against it as written.

**4.5 The map example's Ada (a suspect example).** Vision/datom.md
lines 151–152: "; a map of Text to Integer" / `« name:first Ada  born
1990 »`. 6329f1's log line 168: "Vision/datom.md's 'map of Text to
Integer' example holds Ada, not an integer — a suspect example to
surface to the living." No psyche record rules on it; ad19b1's "your
using a map that should be a struct" was said of a different example
(`« born 1815  died 1852 »`). Moot if 4.1 is acted on.

**4.6 Unreviewed Declaration text against the living's reading
boundary.** Not a contradiction between records, but a standing
caveat 6329f1's log states (line 244 and the e996e8 remembering): the
living read the two proposals "up to the Declaration's File section";
everything in Vision/protos.md past Direction and everything in the
Declaration from Imports on was landed on the flow's authority under
the one-sweep instruction. The map lines in 4.1 (ethos 156–157, 167,
236, 242) all fall in that unreviewed span.

**4.7 6329f1's remembering of ad19b1 against ad19b1's later records.**
flows/6329f1/reports/remember-ad19b1.md line 27 carries "it should be
CAPACITY. and use a key-value map delimiter" as ad19b1's ruling;
ad19b1's later record in the same file, flows/ad19b1/vision/ethos.md
line 26, questions it ("this can only work if the constant
declarations' order doesn't matter … In the key map, the order is not
guaranteed, right?"), and protos.md line 8 drops it. The remembering
was accurate when written and is stale now (inference mine, from the
commit dates in 3.d).

**4.8 Bracket arity: anatomical or not.** flows/04db2fd2/vision/anatomy.md,
typed: "{} = nb of components is anatomical whereas for [] that isnt
the case", and in the same file, later: "yes, well said. the anatomy of
a [] enclosed portion must still indicate its arity, which will
eventually be useful somehow (pretty printers for example might want
to know this, and future fancy editors)". Landed, Vision/protos.md
lines 55–56: "A brace-enclosed structure's arity is anatomical; a
bracket-enclosed structure's arity is not." The landed text carries
the first sentence and not the second. Same flow, same day; not
resolved here.

**4.9 Parentheses as a protos delimiter.** flows/04db2fd2/vision/delimiters.md,
typed, on parentheses: "that's not univeral yet. so not protos. what
we can say is it's content-opaque, so all characters it contains are
ignored, until the closing unbalanced closing parenthesis."
Landed, Vision/protos.md lines 44–47: "Six delimiter pairs in all:
four structural — braces, brackets, guillemets, angle brackets — and
two opaque — curly quotes, where every glyph inside is content, and
parentheses, read by balance." Vision/datom.md Meaning (ad19b1,
2026-09-03) makes the parenthesis pair the Meaning delimiter and says
"Opening a Meaning makes the whole delimiter and structure spectrum
available inside it", which is not "content-opaque". The later
records (a5587095 "once we open the Meaning delim … all the
delimiters and structured parsing spectrum is available"; ad19b1
Meaning landing) read against the 04db2fd2 "not protos" line; whether
"not univeral yet" has since been settled by the Meaning landing is
not ruled in words.

**4.10 Chained names scrapped against daisy-chained heads.**
flows/5abf3be8/vision/chainedNamesScrapped.md, 2026-08-06, typed: "no,
that is scrapped" (of "chained names (Technology.Software.Programming)").
flows/04db2fd2/vision/anatomy.md, STT: "We aren't closed off to the
daisy chain of heads, so to speak. So it could be like x.y.z.w. That's
okay. I can see where we might actually do that. And it can be like
different separators too." Landed, Vision/protos.md lines 42–43:
"Heads may be daisy-chained: different separators too", and
Vision/datom.md's `Observed.Locks.[]`. The later record and the landed
text stand; the 2026-08-06 record is listed because a reader of both
will ask.

**4.11 A bare variant named as an already defined type.**
flows/e8c4cc61/vision/ethosTypes.md, STT, undistilled: "when a variant
is actually an already defined type somewhere else, we can just say
syntax error, for example, and if it was specified somewhere else in
the library, the same name, syntax error, then the ethos runtime has
to make the leap and understand that syntax error is actually a data
carrying variant. But there's no need to write syntax error dot syntax
error data." Landed, Vision/ethos.md lines 177–179: "A variant carrying
nothing is bare. A variant carrying data is headed: `Name.Type` for one
type". Under the landed rule a bare `SyntaxError` carries nothing; the
record wants it to carry the type of the same name. Not resolved here.

**4.12 Multi-field tuple structs.** flows/cff271af/vision/tuples.md,
2026-08-22: "do we have to allow those? I really dont like tuples,
they're a form of un-specification" (of "A multi-field tuple struct,
struct Pair(A, B)"). Landed, Vision/ethos.md lines 159–160: "Positions
are unnamed. Every struct is a tuple struct in the target Rust; every
variant carrying data is a tuple variant." aa4c7747 tuples
(2026-08-24, distilled, carried at line 194–195) rules "no tuple in
the code we design … at that contact point only", which the landed
text reads as being about tuples, not tuple structs. The 2026-08-22
question stands unanswered in the records; the landed Rust is all
tuple structs.

**4.13 "embody" as the general word for reaching the layer below.**
flows/62022e8f/vision/kinds.md, STT: "incorporate is the capability of
the corporal, because then embody becomes a general term to talk
about, like when a structure embodies as a concept, right? So to
embody a structure means we get a concept. To embody any layer means
we get the layer below." Landed, Vision/protos.md lines 60–63:
"Potential and actualize go universally, layer to layer"; the word
embody does not occur in Vision/protos.md. 6329f1's "drop Embodied;
stick with Sized" dropped the bound, not the verb; no record drops the
verb. Whether "actualize" replaced "embody" as the general word, or
the two coexist, is not ruled in words.

**4.14 "Struct is never said" against "struct" in the landed texts.**
flows/62022e8f/vision/vocabulary.md, STT, on the flow's
`Struct.Vector<Portion>`: "We wouldn't actually ever say 'struct [STT:
struck].' This form has to be absolutely killed … The struct aspect is
described using structure." Landed, Vision/datom.md line 97 "A brace
structure is a struct and a bracket structure is a vector",
Vision/ethos.md line 153 "A struct is a headed brace", line 159 "Every
struct is a tuple struct in the target Rust". The record was said of a
protos type named `Struct` in an ethos spec; the landed uses are prose
naming the datom and Rust concept. Whether the ruling reaches them is
not settled here.

---

## Sources

Every file read by this subflow or by its read subagents, by path.
Files read by this subflow directly are marked (w); files read only
by a subagent and relayed are marked (r).

Distilled and intent:
- /home/li/primary/Vision/protos.md (w)
- /home/li/primary/Vision/ethos.md (w)
- /home/li/primary/Vision/datom.md (w)
- /home/li/primary/Vision/distillation.md (r)
- /home/li/primary/Vision/orchestrate.md (r)
- /home/li/primary/Vision/sources/protos.md (w)
- /home/li/primary/Vision/sources/ethos.md (w)
- /home/li/primary/Vision/sources/datom.md (w)
- /home/li/primary/Vision/sources/distillation.md (w)
- /home/li/primary/Intent/protosParsing.md (r)
- /home/li/primary/Intent/data.md (r)
- /home/li/primary/Intent/mandatoryTraits.md (r)

Flow logs and reports:
- /home/li/primary/flows/e996e8/log.md (w)
- /home/li/primary/flows/6329f1/log.md (w, in part by grep and sed)
- /home/li/primary/flows/6329f1/reports/remember-ad19b1.md (w)
- /home/li/primary/flows/6329f1/reports/psyche-mining.md (w, first 200 lines)

Raw records, flow ad19b1 (w, all):
- /home/li/primary/flows/ad19b1/vision/protos.md
- /home/li/primary/flows/ad19b1/vision/datom.md
- /home/li/primary/flows/ad19b1/vision/ethos.md
- /home/li/primary/flows/ad19b1/vision/archive-kinds.md
- /home/li/primary/flows/ad19b1/vision/archive-meaning.md
- /home/li/primary/flows/ad19b1/vision/designPractice.md
- /home/li/primary/flows/ad19b1/vision/distillation.md
- /home/li/primary/flows/ad19b1/vision/psycheSystem.md

Raw records, flows 6329f1 and e996e8 (w, all):
- /home/li/primary/flows/6329f1/vision/archive-protos.md
- /home/li/primary/flows/6329f1/vision/archive-ethos.md
- /home/li/primary/flows/6329f1/vision/archive-vocabulary.md
- /home/li/primary/flows/e996e8/vision/protos.md
- /home/li/primary/flows/e996e8/vision/ethos.md

Raw records, datom (w unless marked):
- /home/li/primary/vision-raw/archive-datomSyntax.md
- /home/li/primary/flows/a5587095/vision/archive-datomSyntax.md
- /home/li/primary/flows/a5587095/vision/archive-structuredStringType.md
- /home/li/primary/flows/06196cc7/vision/archive-datomSyntax.md
- /home/li/primary/flows/4decf7/vision/archive-datomSyntax.md
- /home/li/primary/flows/5abf3be8/vision/archive-colonLegalInStringPosition.md
- /home/li/primary/flows/01a03eda/vision/archive-datomInteger.md
- /home/li/primary/flows/01a03eda/vision/archive-datomSyntax.md
- /home/li/primary/flows/01a03d6e/vision/archive-dotosFiles.md
- /home/li/primary/flows/01a03d6e/vision/ethosInterfaces.md
- /home/li/primary/flows/ac1e9ec8/vision/datomSyntax.md
- /home/li/primary/flows/ac1e9ec8/vision/datomIsData.md
- /home/li/primary/flows/ac1e9ec8/vision/archive-distillationNegatives.md
- /home/li/primary/flows/ac1e9ec8/vision/datomSkill.md (title only)
- /home/li/primary/flows/ac1e9ec8/vision/distillationNegatives.md (title only)
- /home/li/primary/flows/01a04339/vision/archive-datom.md
- /home/li/primary/flows/4d5fc7da/vision/datom.md
- /home/li/primary/flows/04db2fd2/vision/archive-datomMaps.md
- /home/li/primary/flows/04db2fd2/vision/archive-datomNexus.md
- /home/li/primary/flows/04db2fd2/vision/text.md
- /home/li/primary/flows/04db2fd2/vision/textualTypes.md
- /home/li/primary/flows/04db2fd2/vision/directionAsymmetry.md
- /home/li/primary/flows/e8c4cc61/vision/archive-datomSyntax.md
- /home/li/primary/flows/e8c4cc61/vision/datomizable.md
- /home/li/primary/flows/62022e8f/vision/archive-datomSyntax.md
- /home/li/primary/flows/62022e8f/vision/symbols.md
- /home/li/primary/flows/62022e8f/vision/headedAndContained.md
- /home/li/primary/flows/995a164e/vision/archive-datomSyntax.md
- /home/li/primary/flows/e4a40e/vision/archive-datom.md
- /home/li/primary/flows/e4a40e/vision/archive-vocabulary.md
- /home/li/primary/flows/b675f3d9/vision/structuralParsing.md

Raw records, protos (w unless marked):
- /home/li/primary/flows/a5587095/vision/protosIsTheSharedStyle.md (r; opening confirmed)
- /home/li/primary/flows/a5587095/vision/colonFormTransformerSyntax.md (r; opening confirmed)
- /home/li/primary/flows/ba906ae2/vision/protosIsTheSharedStyle.md
- /home/li/primary/flows/ba906ae2/vision/encodedFormIsTheCode.md
- /home/li/primary/vision-raw/encodedFormIsTheCode.md (r; opening confirmed)
- /home/li/primary/vision-raw/protosIsTheSharedStyle.md (r; title only)
- /home/li/primary/flows/2b34fafa/vision/protosIsTheSharedStyle.md
- /home/li/primary/flows/04db2fd2/vision/anatomy.md
- /home/li/primary/flows/04db2fd2/vision/multiPass.md
- /home/li/primary/flows/04db2fd2/vision/portion.md
- /home/li/primary/flows/04db2fd2/vision/delimiters.md
- /home/li/primary/flows/04db2fd2/vision/delineate.md
- /home/li/primary/flows/04db2fd2/vision/decomposable.md
- /home/li/primary/flows/04db2fd2/vision/kinds.md (r)
- /home/li/primary/flows/2ef42163/vision/kinds.md
- /home/li/primary/flows/db97561c/vision/prospective.md
- /home/li/primary/flows/e8c4cc61/vision/protos.md
- /home/li/primary/flows/e8c4cc61/vision/prospective.md
- /home/li/primary/flows/62022e8f/vision/kinds.md
- /home/li/primary/flows/62022e8f/vision/layers.md
- /home/li/primary/flows/62022e8f/vision/concept.md
- /home/li/primary/flows/62022e8f/vision/passes.md
- /home/li/primary/flows/62022e8f/vision/vocabulary.md
- /home/li/primary/flows/62022e8f/vision/multiFormConcepts.md
- /home/li/primary/flows/62022e8f/notion/layerMatching.md
- /home/li/primary/flows/62022e8f/notion/terminology.md
- /home/li/primary/flows/995a164e/vision/concept.md
- /home/li/primary/flows/995a164e/vision/kinds.md
- /home/li/primary/flows/995a164e/vision/layerMatching.md
- /home/li/primary/flows/e4a40e/vision/protos.md
- /home/li/primary/flows/1c282d/vision/protosizable.md

Raw records, ethos (w unless marked):
- /home/li/primary/vision-raw/archive-ethosNonRepetitionLaw.md (r)
- /home/li/primary/vision-raw/archive-ethosDotosDivisionAndHelp.md (r)
- /home/li/primary/vision-raw/genericParametersAreTraits.md
- /home/li/primary/vision-raw/colonConfusion.md
- /home/li/primary/vision-raw/traitsAsCapabilities.md
- /home/li/primary/vision-raw/importResolution.md
- /home/li/primary/vision-raw/ethosNamespaces.md (r; title only)
- /home/li/primary/vision-raw/ethosSourceFiles.md (r; title only)
- /home/li/primary/flows/5abf3be8/vision/chainedNamesScrapped.md
- /home/li/primary/flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md
- /home/li/primary/flows/5abf3be8/vision/sectionsExistToConferTraits.md
- /home/li/primary/flows/5abf3be8/vision/encodedFormFingerprintTraitDesign.md
- /home/li/primary/flows/d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md (r)
- /home/li/primary/flows/6863ef19/vision/traitsAsCapabilities.md (r)
- /home/li/primary/flows/06196cc7/vision/traitsAsCapabilities.md
- /home/li/primary/flows/2b34fafa/vision/traitsAsCapabilities.md
- /home/li/primary/flows/2b34fafa/vision/ethosSourceFiles.md
- /home/li/primary/flows/2b34fafa/vision/ethosNamespaces.md
- /home/li/primary/flows/2b34fafa/vision/importResolution.md
- /home/li/primary/flows/cff271af/vision/tuples.md (r)
- /home/li/primary/flows/01a02a34/vision/archive-ethos.md (r)
- /home/li/primary/flows/01a02a34/vision/archive-schemaSyntax.md (r)
- /home/li/primary/flows/68512643/vision/negatives.md
- /home/li/primary/flows/aa4c7747/vision/ethos.md (r)
- /home/li/primary/flows/aa4c7747/vision/ethosMonolith.md (r)
- /home/li/primary/flows/aa4c7747/vision/ethosTraitSyntax.md (r)
- /home/li/primary/flows/aa4c7747/vision/interactions.md (r)
- /home/li/primary/flows/aa4c7747/vision/tuples.md (r)
- /home/li/primary/flows/aa4c7747/vision/spokenVocabulary.md (r)
- /home/li/primary/flows/f426777b/vision/ethosSourceFiles.md (r)
- /home/li/primary/flows/f426777b/vision/spokenVocabulary.md (r)
- /home/li/primary/flows/b675f3d9/vision/kinds.md (r)
- /home/li/primary/flows/b675f3d9/vision/ethosMonolith.md (r)
- /home/li/primary/flows/b675f3d9/vision/spokenVocabulary.md (r; title only)
- /home/li/primary/flows/2ef42163/vision/ethos.md (r)
- /home/li/primary/flows/e8c4cc61/vision/kinds.md
- /home/li/primary/flows/e8c4cc61/vision/ethosFileAnatomy.md
- /home/li/primary/flows/e8c4cc61/vision/ethosTypes.md
- /home/li/primary/flows/e8c4cc61/vision/designExamples.md (r)
- /home/li/primary/flows/e8c4cc61/vision/designPractice.md (r)
- /home/li/primary/flows/62022e8f/vision/ethosTypes.md
- /home/li/primary/flows/62022e8f/vision/designPractice.md
- /home/li/primary/flows/62022e8f/vision/distilledVision.md
- /home/li/primary/flows/995a164e/vision/ethosTypes.md
- /home/li/primary/flows/995a164e/vision/designPractice.md
- /home/li/primary/flows/995a164e/vision/rust.md
- /home/li/primary/flows/4decf7/vision/archive-kinds.md (r)
- /home/li/primary/flows/e4a40e/vision/archive-kinds.md (r)
- /home/li/primary/flows/e4a40e/vision/newtypeWrappingAndSingleFieldStructs.md (r)

Raw records, vocabulary and secondary (r unless marked):
- /home/li/primary/flows/995a164e/vision/vocabulary.md
- /home/li/primary/flows/2f6b1dc5/vision/vocabulary.md
- /home/li/primary/flows/01a052b6/vision/vocabulary.md
- /home/li/primary/flows/1c282d/vision/vocabulary.md
- /home/li/primary/vision-raw/dictation-vocabulary.md
- /home/li/primary/vision-raw/letsUseTheSameVocabulary.md
- /home/li/primary/vision-raw/protosIsTheSharedStyle.md (title only)
- /home/li/primary/flows/e4a40e/vision/distillation.md
- /home/li/primary/flows/cff271af/vision/distillation.md
- /home/li/primary/flows/a60a9e85/vision/distillation.md
- /home/li/primary/flows/acbb6006/vision/distillation.md
- /home/li/primary/flows/acbb6006/vision/archive-distillation.md
- /home/li/primary/flows/b675f3d9/vision/distillation.md (title only)
- /home/li/primary/flows/b675f3d9/vision/archive-distillation.md
- /home/li/primary/flows/4decf7/design/proposal1/distillation.md
- /home/li/primary/flows/995a164e/vision/designPractice.md
- /home/li/primary/flows/62022e8f/vision/designPractice.md
- /home/li/primary/flows/e8c4cc61/vision/designPractice.md

Code, read with git show at the named revisions (w):
- /git/github.com/LiGoldragon/datomic — src/lib.rs and Cargo.toml at main = origin/main = 4712361c
- /git/github.com/LiGoldragon/protos — src/lib.rs and Cargo.toml at main = 56c683e and origin/main = 48061367

Git commands run in /home/li/primary (w): `git log` on 55554e368,
7d19dcacf, 23aaf7a7f; `git log -- Vision/protos.md`, `-- Vision/ethos.md`,
`-- Vision/datom.md`, `-- flows/ad19b1/vision/{protos,datom,ethos}.md`;
`git show 23aaf7a7f --stat`. Directory listings: flows/*/vision,
flows/*/notion, Vision/, Vision/sources/, Intent/, vision-raw/,
flows/6329f1/{vision,notion,reports}.
