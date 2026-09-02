# Protos — gathered psyche records

Gathered by flow 4decf7 for the parent's distill-as-we-go practice.
Each record quoted verbatim, considered individually.

---

## Intent

### 1. Intent/protosParsing.md — "Protos parsing"

Originating flow: a5587095 (Designer session, typed). Date: graduated
2026-08-13T00:19+02:00. Provenance: Designer-drafted through the
two-way structural transcoding flesh-out
(design/ProtosEngine/twoWayStructuralTranscoding-2026-08-11.md);
approved as Intent by the psyche 2026-08-13.

> Protos parsing always happens inside a context, and only the
> current context gives shapes their meaning: it defines which
> shapes can appear next and which shape completes it. A met shape
> announces a type, and that type's context takes over completely
> until its completing shape; then the parent context resumes
> exactly where it left off. Reading and writing are one walk in
> two directions — text lands in typed values, and typed values
> project back into the same text.

Standing: distilled Intent, approved by the psyche. The provenance
paragraph's "two-way structural transcoding" is annotated as dead
vocabulary (code/encoded dropped 2026-08-13); the Intent body itself
is unaffected.

---

## Vision distilled (in Vision/)

### 2. Vision/protos.md — "Direction"

Landed in flow 04db2fd2 from distillation proposal
b675f3d9/reports/distillProposalProtosDatom.md. The psyche approved
this single statement: "exactly. this can go straight into distilled
vision" (flows/04db2fd2/vision/directionAsymmetry.md, typed).

> Text arrives as a prospective value and leaves as a value. Realize reads the textual form into the real form and may fault: the text is prospective until it matches its anatomy. Textualize writes the real form into the textual form and cannot fault: a real value is already whole. Spans are found on the way in and computed on the way out. Each direction is several passes.

Standing: distilled Vision, approved by the psyche.

---

## Vision raw and undistilled

### 3. vision-raw/parserIsTheParser.md — "The parser is the parser"

Originating flow: steward session, 2026-08-11. Provenance: psyche,
date unclear (captured from a steward session).

> "assembly.rs reimplements its own parser, which is forbidden.
> the parser is the parser, nothing implements its own parsing logic."

Standing: raw and undistilled.

---

### 4. vision-raw/encodedFormIsTheCode.md — "The encoded form is the code" (2026-08-06)

Originating flow: 5abf3be8 (Designer session, STT; entry captured
2026-08-08 from the session transcript during the rulings-audit backfill).

> So we agreed that there would be a different type for every kind of
> ethos object, even all the way down to ethos mirroring the types
> that are needed to contain the particular nomos types, for now
> anyway. So that's, you know, the serialized RKYV payload of that
> filled data type is the body. The encoded form is the code. So the
> encoded form of ethos is ethos. The textual form is there so that
> our editors, our current editors, and our current LLM harnesses and
> models can actually make sense of it. Does that answer the question?

Standing: **superseded** by the same file's 2026-08-13 entry (record 5
below) — code/encoded vocabulary dropped.

---

### 5. vision-raw/encodedFormIsTheCode.md — "working form and signal form; code/encoded dropped" (2026-08-13)

Originating flow: 06196cc7 (Designer session, typed).

> ok, working form and signal form, drop code/encoded entirely

Standing: the drop stands. The name "working" was rejected hours later
(record 9 below); signal form stands; the form formerly called
working was renamed "real" (record 10). Raw and undistilled; partially
drawn into Vision/protos.md "Direction" (record 2).

---

### 6. vision-raw/colonConfusion.md — "Confusion with :"

Originating flow: d63804f2 (Designer session, 2026-08-07, captured
2026-08-07T18:59Z).

> "I would rather not create confusion with :"

Superseding entry in the same file (2026-08-07T22:10Z):

> "the fixture is blessed, and / for imports"

Standing: raw and undistilled. The import-separator ruling (`/`)
stands from this file; the colon carries exactly one meaning: the
named-transformer form. **Tension noted**: the living's later fixtures
(2026-08-20) write imports with a colon (`signal-psyche:Object`) —
the b675f3d9 distillation proposal surfaced this, unresolved.

---

### 7. vision-raw/colonFormTransformerSyntax.md — "Name:TransformerName.( ... ) is the better syntax"

Originating flow: 5abf3be8 (Designer session, 2026-08-06T17:25:39Z;
entry captured 2026-08-08 during the rulings-audit backfill).

> unrelated first. I think Name:TransformerName.( ... ) is the better
> syntax for named transformers. The other syntax will create
> difficult parsing and reasoning. Do you agree?

Standing: raw and undistilled. Origin of the colon-form transformer
syntax.

---

### 8. vision-raw/importResolution.md — "a type that needs a name handed in is not resolvable" (2026-08-20) and "the manifest should have everything" (2026-08-21)

Originating flow: 2b34fafa (Design session, typed).

2026-08-20:
> "if the type needs a 'name' to resove the import, then it's not
> resolvable."

2026-08-21:
> And I don't know why you wouldn't do the assembled source from the
> manifest. The manifest should have everything you need. Like maybe
> we don't have the same idea of a manifest, maybe we need another
> type, kind of like how the cargo file works, but more specific,
> where it doesn't have more than one possible output. So it's a kind
> of an assembly file, if you will.

Standing: raw and undistilled.

---

### 9. vision-raw/itsATranslator.md — "Im 100% in vision description mode"

Originating flow: 55d18f4f (Designer session, 2026-08-08T11:48:31.390Z;
human-origin queued-command attachment).

> right now, I dont really give a fuck what anything is built as. Im 100% in vision description mode. Consider all the implementation half garbage for now.

Standing: raw and undistilled.

---

### 10. vision-raw/protosIsTheSharedStyle.md

This file contains only a heading and no psyche entries:

> # Protos is the style all our dialects share

Standing: placeholder; the substance is in the flow records below.

---

### 11. vision-raw/structuredStringType.md — "think of it as an annotated string" and subsidiary entries

Originating flow: pre-flows (captured across multiple flows). The file
carries a 2026-08-14 cross-reference annotation linking downstream
rulings to datomSyntax.md.

Standing: raw and undistilled. The governing entries are in the flow
records on structuredStringType (records 37-42 below).

---

### 12. vision-raw/traitsAsCapabilities.md — "types first; all protos dialects are transcodable"

Originating flow: 6863ef19 (Designer session, 2026-08-13, dictated).

2026-08-13, entry 1:
> we need to think very carefully of what the types are. First,
> really, because the traits are something that the types implement.
> We don't look for traits and then think of types for that. So,
> what are all the types? Let's look at the types first.

2026-08-13, entry 2:
> So, if we take all the common behavior, we want to have as many
> common traits as possible, because then we're creating the right
> abstraction. So, all protos dialects, whether it's datum [Datom],
> ethos, nomos, or logos, are transcodable.

> we don't have to be afraid to use more elaborate terms if we want
> to describe what this behavior is specifically. [...] if the trait
> is transcodable, yes, and if it lives in the protos module, then
> that's not ambiguous.

Standing: raw and undistilled. "Transcodable" superseded by the
code/encoded drop (same session); the principle that common traits
are the right abstraction and all protos dialects share them stands,
now applied to protos::Realize and protos::Textualize.

---

### 13. vision-raw/mainFunction.md — "main is a few lines; generated Rust comes from a full Logos program" (2026-08-21)

Originating flow: 2b34fafa (Design session, dictated).

> We want to start from the top or the bottom, however you want to
> see it, the main function.
> And in the main function, it has to be very clear. It's only a few
> lines, right? [...]
> Like eventually, when we have the three demons [daemons], for
> example, in the Protoss [Protos] engine, the generated rest [Rust]
> comes from the logos [...]

Standing: raw and undistilled. Mentions the Protos engine with three
daemons as eventual architecture.

---

## Vision raw — flow records

### 14. 55d18f4f itsATranslator — "its misnamed. its a translator" (2026-08-08)

> its misnamed. its a translator. it translates code into text. right?

Provenance: typed, 2026-08-08T11:47:07.277Z. 2026-08-14 annotation:
"code" is the pre-drop sense; the form is now the signal form.

Standing: raw and undistilled.

---

### 15. 55d18f4f itsATranslator — "it should be called protos-translator" (2026-08-08)

> it should be called protos-translator

Provenance: typed, 2026-08-08T12:00:33.185Z.

Standing: raw and undistilled.

---

### 16. 06196cc7 encodedFormIsTheCode — "working rejected: it smells like a verb" (2026-08-13)

> I dont like working, it smells like a verb. Same with meaning

Provenance: typed, hours after "working form and signal form" landed.

Standing: raw and undistilled. The form name was left unnamed; resolved
by record 17.

---

### 17. 06196cc7 encodedFormIsTheCode — "the real form; Realize" (2026-08-14)

> Ok with the real/Realize

Provenance: typed. The form beside signal and textual is the real form;
the text-to-form trait is protos::Realize, paired with
protos::Textualize.

Standing: raw and undistilled. Partially drawn into Vision/protos.md
"Direction" (record 2).

---

### 18. 06196cc7 traitsAsCapabilities — "a type for the text block; maybe drop code/encoded" (2026-08-13)

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
> use for the in-memory/signal form?

Provenance: typed.

Standing: raw and undistilled. The code/encoded drop was enacted same
session.

---

### 19. 06196cc7 traitsAsCapabilities — "transcodable falls with the drop" (2026-08-13)

> 1. I dont think it survives. I think we end up with things like
> WorkingFormCastable, but I want to see you make a shot at a bunch
> of different naming options
>
> Or maybe we need to accept verbs for traits, since theyre
> capitalized and therefore not a function

Provenance: typed.

Standing: raw and undistilled. Superseded by later verb acceptance
(record 21) and the naming resolution (Realize/Textualize, records
17, 22).

---

### 20. 06196cc7 traitsAsCapabilities — "verbs accepted for traits" (2026-08-14)

> Yes, I accept verbs. now I can see why rust went with verbs; it
> is easy to understand that a thing that which implements Run is
> CapableOfRunning.

Provenance: typed. Qualifies the 2026-08-13 all-traits-are-qualifiers
ruling.

Standing: raw and undistilled. Later partially revisited by the lean
back to "writable > write" (f426777b, record 47).

---

### 21. 06196cc7 traitsAsCapabilities — "no umbrella capability; the directional traits live in protos" (2026-08-14)

> none of this makes sense if we use a trait for each direction.
> The traits should live in protos regardless (Textualize and
> whatever we pick for Materialize)

Provenance: typed.

Standing: raw and undistilled. protos::Textualize and
protos::Realize (once unnamed here) are protos-homed.

---

### 22. 06196cc7 traitsAsCapabilities — "Textualize confirmed; ShapeDefined stays" (2026-08-14)

> Textualize is good

> ShapeDefined is good

Provenance: typed.

Standing: raw and undistilled.

---

### 23. 06196cc7 traitsAsCapabilities — "RealizeWalk, TextualizeWalk, and Walk accepted" (2026-08-14)

> fine. im not crazy about it but its good enough

Provenance: typed. Accepted with reservation.

Standing: raw and undistilled.

---

### 24. 06196cc7 codeIsLanguage — "explaining concepts is not formulating vocabulary" (2026-08-14)

> I wasnt designing vocabulary. we need to explain to agents the
> difference between psyche explaining concepts, and formulating
> vocabulary. the quoted psyche is obviously conveying a broad
> concept

Provenance: typed.

Standing: raw and undistilled. Governs how protos terminology is read.

---

### 25. ba906ae2 protosIsTheSharedStyle — "datom is a protos dialect, not part of the rust-generation engine" (2026-08-14)

> because datom doesnt take part in the multi pass engine which
> ethos->nomos->logos->rust is slated to become. but youre right;
> beside sounds like its not a protos dialect. it *is* a protos
> dialect, but not part of the future ethos/nomos/logos
> rust-generation engine

Provenance: typed, 2026-08-14T10:09+02:00.

Standing: raw and undistilled.

---

### 26. ba906ae2 encodedFormIsTheCode — "textualize is approved" (2026-08-14)

> textualize is approved. im pretty sure I had approved it, but
> there it is again

Provenance: typed, 2026-08-14T13:04+02:00.

Standing: raw and undistilled. Settles protos::Textualize.

---

### 27. a5587095 protosIsTheSharedStyle — "the definition; context-switching parse; the protos engine" (2026-08-11)

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

Provenance: typed, 2026-08-11T19:44+02:00. Five rulings carried:
(a) protos names the shared style; (b) context-switching parse is how
all languages parse; (c) that parse code belongs in protos; (d) the
fully-decomposed engine with three daemons is the protos engine;
(e) Datom sits beside it. (e) clarified by record 25: beside the
rust-generation engine, not beside protos.

Standing: raw and undistilled. The definition of protos is in this
entry.

---

### 28. a5587095 protosIsTheSharedStyle — "there is always a parsing context; it changes, never suspends; always use trait" (2026-08-11)

> no, there is always a parsing context. it doesnt suspend, it
> *changes*, but the underlying mechanism is always the same; Now,
> we are parsing in context X and can therefore expect A, B or C
> shapes of things, and Z would end that context, but meeting A
> would switch to the context which A entails. That has been the
> ruling principle of NOTA (datoms's ancestor) from day one. I want
> to extend it now to say it should always use trait.

Provenance: typed, 2026-08-11T19:53+02:00.

Standing: raw and undistilled. The context mechanism and its NOTA
lineage. Drawn into Intent/protosParsing.md (record 1).

---

### 29. a5587095 protosIsTheSharedStyle — "two-way structural transcoding; flesh out before Intent" (2026-08-11)

> Intent would be quite general, about the way the parsing is
> approached. Lets flesh it out in detail with examples then we can
> make it intent. Intent is basically very clear vision which is
> unlikely to change. Dont forget the parsing is also two-ways. I
> feel like we need to really flesh out this two-way structural
> transcoding, through clear explanation and with a trait-library
> first approach, in protos repo (which can be re-considered from
> whatever it is doing now) We need to work with visuals, examples,
> and traits with main types. that must become our design pattern.

Provenance: typed, 2026-08-11T22:04+02:00.

Standing: raw and undistilled. "Two-way structural transcoding" is
dead vocabulary post code/encoded drop; the two-way walk concept
stands.

---

### 30. a5587095 protosIsTheSharedStyle — "the expects vector: ProtosShapes" (2026-08-12)

> the more complex trait will be a vector of ProtosShape's (welcome
> to propose other names), when the structure dictates the outer
> type, for example in ethos when X.{ means a struct, and Y.[ means
> an enum, and Z:Transform.[/{ means different kinds of transformers

Provenance: typed, 2026-08-12T00:59+02:00.

Standing: raw and undistilled.

---

### 31. a5587095 protosIsTheSharedStyle — "ProtosShape is a trait; the match on standard shapes; types carry their own context" (2026-08-12)

> The type met implements its own context? Does that make sense?

> To me ProtosShape was a trait. so for a throaway example [...],
> NewString would implment ProtosShape. Maybe the right shape for
> NewString is an Enum with variants String and Meaning, and
> implementing ProtosShape means creating a match on standard
> ProtosShape (which is why I thought the trait should be named
> something else - ProtosShaped? ShapeDefined?). Those ProtosShape
> are always the same [...]

Provenance: typed, 2026-08-12T01:26+02:00.

Standing: raw and undistilled. ShapeDefined naming fork closed
2026-08-14 (record 22).

---

### 32. a5587095 protosIsTheSharedStyle — "recursion keeps the parent's position; logic planes; a child context takes the shapes' meaning" (2026-08-12)

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

Provenance: typed, 2026-08-12T21:23+02:00.

Standing: raw and undistilled. Drawn into Intent/protosParsing.md
(record 1). "Logic planes" is candidate Spirit/Intent.

---

### 33. a5587095 protosIsTheSharedStyle — "the Protos parsing Intent is graduated" (2026-08-13)

> the intent is good

Provenance: typed, 2026-08-13T00:19+02:00.

Standing: the approval that created record 1
(Intent/protosParsing.md).

---

### 34. a5587095 protosIsTheSharedStyle — "recursion must carry shape-determined types at every level" (2026-08-13)

> your recursive parsing wasnt complex enough. we need to consider
> multiple levels, each with one or more shape-determined type

Provenance: typed, 2026-08-13T00:25+02:00.

Standing: raw and undistilled.

---

### 35. a5587095 protosIsTheSharedStyle — "no traits is no good" (2026-08-13)

> I only looked at the code. I need to see the traits. No traits
> is no good

Provenance: typed, 2026-08-13T00:29+02:00.

Standing: raw and undistilled.

---

### 36. a5587095 colonFormTransformerSyntax — "transformer payloads take .[ or .{; parentheses freed" (2026-08-11)

> I think we are wrongly using parenthesis in ethos now, since we
> introduced X:Transformer syntax, which differentiates transformers
> (and some transformers might expect a single vector, in which case
> .[ is better, and for the rest expecting a structured input .{ is
> the right delimiter). This would free patenthesis completly [...]

Provenance: typed, 2026-08-11T18:53+02:00.

Standing: raw and undistilled. Supersedes the 2026-08-06 `.(` payload
opener.

---

### 37. a5587095 structuredStringType — "the idea" (2026-08-11)

> This would free patenthesis completly, and I have an idea for a
> revolutionary type; a structured string type - something that
> would revolutionize LLM performance by exposing the emphasis and
> other structural aspects which a plain string simply doesnt have.
> think of it as an annotated string

Provenance: typed, 2026-08-11T18:53+02:00.

Standing: raw and undistilled. Same message as record 36.

---

### 38. a5587095 structuredStringType — "one type, two variants; parentheses; research directed" (2026-08-11)

> 1. I am considering it, yes. This would require a new type (in
> rust, later ethos-generated) which can be met with either a curly
> quotes or parenthesis (two variants, legacy and structured). The
> structured type would allow for an arbitrary depth, since it is a
> graph of sorts.
>
> 2. Research the field of representing meaning with structure.
>
> 3. shape is still up in the air, but () would be the delimiter

Provenance: typed, 2026-08-11T19:17+02:00.

Standing: raw and undistilled.

---

### 39. a5587095 structuredStringType — "the Meaning delimiter; context-switching parse" (2026-08-11)

Same quote as record 27 (protosIsTheSharedStyle), dual-logged in
structuredStringType.md. The Meaning delimiter is the parenthesis pair.

Standing: raw and undistilled.

---

### 40. a5587095 structuredStringType — "the ambition" (2026-08-11)

> I want the most advanced structured meaning system ever made

Provenance: typed, 2026-08-11T19:44+02:00.

Standing: raw and undistilled.

---

### 41. a5587095 structuredStringType — "annotations as enums through the tree" (2026-08-11)

> what do you mean by self-describing tag? The way I see it right
> now is there would be enums which would be used throughout the
> tree, like Emphasis.{} or similar, but its still too early to tell

Provenance: typed, 2026-08-11T19:53+02:00.

Standing: raw and undistilled.

---

### 42. a5587095 structuredStringType — "Meaning lives in datom; seen by both languages" (2026-08-11)

> Meaning will be seen in datom and ethos. ethos will depend on
> datom if only because of the need to intake data for signals, so
> it can go in datom

Provenance: typed, 2026-08-11T22:04+02:00.

Standing: raw and undistilled. Drawn into Vision/datom.md "Relation
to Ethos" and "Meaning".

---

### 43. a5587095 rustComponentArchitecture — "all method calls in our rust code are part of a trait" (2026-08-11)

> I even want to make the broad statement that I want *all* method
> calls in our rust code to be part of a trait, since I need to
> understand my systems through traits and main types, as I cannot
> possibly read all the code, and rust is the new assembly language;
> no serious engineer reads all the assembly code anymore, and the
> same is going to happen to rust, hence why we need a more concise,
> dense and congnitively concentrated language like ethos to write
> code with AI agents.

Provenance: typed, 2026-08-11T19:53+02:00, during the protos
context-parsing discussion.

Standing: raw and undistilled. Candidate Intent.

---

### 44. 2b34fafa protosIsTheSharedStyle — "define the block: start with the text source code; every logical aspect a type; ontology of source code" (2026-08-18)

> "we need to define the block. start with the text source code. turn
> every logical aspect into a type. ontology of source code"

Provenance: typed.

Standing: raw and undistilled.

---

### 45. 2b34fafa traitsAsCapabilities — "Realize and Textualize are never on the same type" (2026-08-18)

> "realize isnt implemented by the same type as textualize. if you
> cant find two different types, the implementation is wrong. You
> dont textualize the text, and you dont realize the realized data."

Provenance: typed.

Standing: raw and undistilled.

---

### 46. 2b34fafa traitsAsCapabilities — "trait methods that are regular functions pretending to be traits" (2026-08-20)

> "You misunderstood the trait based approach. your trait methods are
> just regular functions pretending to be traits. if the type needs a
> 'name' to resove the import, then it's not resolvable. So we found
> one of the cornerstone of models not understand my vision. Do a
> research in this"

Provenance: typed.

Standing: raw and undistilled. Named a cornerstone of models not
understanding the vision.

---

### 47. f426777b spokenVocabulary — "lean back to writable over write" (2026-08-26)

> I also want to lean back to writable > write

Provenance: typed, mid-round after the Kind ruling.

Standing: raw and undistilled. Partially revises 2026-08-14 verb
acceptance (record 20) and 2026-08-21 infinitive ruling
(2b34fafa traitsAsCapabilities). Whether it reaches individually
confirmed names (Textualize, Realize) is not addressed.

---

### 48. 2b34fafa sourceNotCrate — "source is the name we use instead of crate" (2026-08-20)

> "so lets look at all the major types to represent the textual code.
> source will be the name we use instead of crate"

Provenance: typed.

Standing: raw and undistilled.

---

### 49. 2b34fafa importResolution — "the first path segment resolves from a datom manifest" (2026-08-20)

> "signal in signal/domain must be resolved from a manifest (which we
> must spec obviously), which uses datom. if signal has no entry, it
> will look in the directory of the document where the import takes
> place."

Provenance: typed. Later same day the fallback was killed (record 50).

Standing: raw and undistilled.

---

### 50. 2b34fafa importResolution — "colon resolves from the manifest or errors; bare paths are local only" (2026-08-20)

> "confirmed, kill the fallback."

Provenance: typed.

Standing: raw and undistilled.

---

### 51. 2b34fafa importResolution — "there is no Import type; what exists is an import reference" (2026-08-20)

> "I dont think Import is a type; there are no Import's; what exists
> is an import reference."

Provenance: typed.

Standing: raw and undistilled.

---

### 52. 2b34fafa importResolution — "external pulls are explicit: colon after the source name" (2026-08-20)

> "`signal-pysche:Object` pulls Object from lib.es in signal-psyche
> source"

> "`signal-pysche:[Object Thing]` multiple imports"

> "`signal-pysche:stream.[Stream Termination]` from stream.es in
> signal-psyche source"

Provenance: typed.

Standing: raw and undistilled. **Tension with record 6**: the 2026-08-07
ruling assigned `/` for imports and freed colon for transformers only;
these 2026-08-20 examples use colon for external imports. Unresolved.

---

### 53. 04db2fd2 textualTypes — "prospective datom until parsed; Prospective<T>" (undated)

> in the implementation of the datum [STT: Datom] ... The type could be... Like it's a candidate, or it's a possible datum [STT: Datom]. Yeah, it's a possible datum [STT: Datom], basically. It's a prospective datum [STT: Datom]. Because until it has actually been parsed, we don't know if it actually is.

> I like "Text taken as a would-be T: Prospective<T>" which gives us Prospective<Datom> although Im unsure if Datom is type or kind, probably kind, since it doesnt have a definite shape yet

> Re datom kind: Datomic

Provenance: first two STT, last two typed.

Standing: raw and undistilled.

---

### 54. 04db2fd2 multiPass — "beginning and end not intrinsic; multi-pass wanted" (undated)

> all objects will have a beginning and an end. Well, not intrinsically. [...] when we actually textualize, these can be computed.

> basically what we're doing is a multi-pass process. We're not interested in doing everything in a single pass, because it creates a whole bunch of, I don't know, corner-cutting bad design. [...] the greatest works ever written were not written in the first pass.

Provenance: STT.

Standing: raw and undistilled. Partially drawn into Vision/protos.md
"Direction" (record 2).

---

### 55. 04db2fd2 directionAsymmetry — "exactly. this can go straight into distilled vision"

> exactly. this can go straight into distilled vision

Provenance: typed.

Standing: the approval that created record 2 (Vision/protos.md
"Direction").

---

### 56. 04db2fd2 delineate — "Prospective<Datom> is Delineatable; delineation is protos"

> Re Delineate: Yes! That's what I was looking for. So a Prospective<Datom> is Delineatable

> delineation is protos.

Provenance: typed.

Standing: raw and undistilled.

---

### 57. 04db2fd2 anatomy — "any type has an anatomy; datom is a kind; realize matches the expected type"

> decomposing a datum [STT: Datom] consists in the capability itself when it's implemented will match the expected kind, sorry, the expected type of datum [STT: Datom] with this data graph, which is the anatomy of a type. So, any type has an anatomy.

> a datum [STT: Datom] is a kind, not a type.

Provenance: STT.

Standing: raw and undistilled.

---

### 58. 04db2fd2 anatomy — "protos machinery, universally applicable to all dialects"

> a braced object has its own anatomy, which probably almost all objects will be structs at the root. ... a lot of what I'm talking about is Protos machinery, because it's universally applicable to all the dialects.

> delineation is protos. so is anatomy (unless you see a problem); the shape can be described independently of the type they represent. [...] {} = nb of components is anatomical whereas for [] that isnt the case

> also false. for protos, a Head is just a Head, nothing more. Anatomy, not interpretation.

> again, youre stepping out of protos territory. pure anatomy is only structural recognition of delineations, *nothing more*

Provenance: first STT, second typed, third and fourth typed.

Standing: raw and undistilled. Key boundary: protos is structural
recognition only; interpretation belongs to the dialect.

---

### 59. 04db2fd2 portion — "Portion as universal term; open vs closed portions"

> instead of saying field, right, because the concept is universal. Like, it doesn't matter if we're talking about a vector and a list of variants in an enum, fields in a struct, or other things, every object, so to speak, is a portion.

Provenance: STT.

Standing: raw and undistilled. Later revisited as "Structure is a
better Portion" (record 66).

---

### 60. 04db2fd2 delimiters — "parentheses not universal yet, not protos"

> that's not univeral yet. so not protos. what we can say is it's content-opaque, so all characters it contains are ignored, until the closing unbalanced closing parenthesis.

Provenance: typed.

Standing: raw and undistilled.

---

### 61. 04db2fd2 decomposable — "the Decomposable kind"

> here's a kind. A kind decomposable. ... if something is decomposable, it's decomposable into composable kinds.

Provenance: STT.

Standing: raw and undistilled.

---

### 62. 04db2fd2 text — "Text must have something over String"

> Re: Text: It would have to have something over a String. non-structural whitespace-removed? [...] If we normalize it then we can have a reliable content-addressed hash [...] Let's call the library something different so we free 'datom' for the eventual nexus. datom-codec?

Provenance: typed.

Standing: raw and undistilled.

---

### 63. 04db2fd2 kinds — "Kinds as verbs not allowed; Delineated is true; Textualized; Embodied or Forged"

> Kinds as verbs are not allowed; we only tolerate the legacy rust gives us, until ethos takes over completly as the authored language [...]

> Textual is already a qualifier. How does that sound as a kind? I like Actual instead of Real, but it's going to cause problems cognitively (too strong). What we're trying to say is that it can take the form the runtime can use. I think Embodied is the right term, unless Forged is better.

Provenance: typed.

Standing: raw and undistilled. Embodied/Forged naming fork was
superseded by later sessions (Realized, then Real — record 17).

---

### 64. 04db2fd2 kinds — "a type's anatomy is a dialect's, not protos"

> if you're talking about a type's anatomy, you're out of protos now into specific dialets

Provenance: typed.

Standing: raw and undistilled. Reinforces record 58's boundary.

---

### 65. db97561c prospective — "Prospective<Protos> comes first; Protos is a type"

> `Prospective<Protos>` is needed first. Protos is a type which contains the portions and their protosic anatomy

Provenance: typed.

Standing: raw and undistilled.

---

### 66. e8c4cc61 protos — "Structure is a better Portion; Delineatable is better expressed as Structural"

> your Structure is a better Portion (better name anyway)

> and Delineatable is better expressed as Structural.

Provenance: typed.

Standing: raw and undistilled.

---

### 67. e8c4cc61 prospective — "the capability of a prospective kind is prospect" (STT)

> I want to actually also specify the capability. So for any prospective kind, so a prospective protos uses the capability prospect, which is to look forward, right, to see if it's a sort of... Yeah, it's a prospect, literally.

Provenance: STT.

Standing: raw and undistilled.

---

### 68. e8c4cc61 prospective — "Prospective<Protos> is an anatomical survey only" (STT)

> And we read before reading and find all of the anatomy of the protosic anatomy, which is not specific. It's just an anatomical survey. [...] we just know that we have a protos object.

Provenance: STT.

Standing: raw and undistilled.

---

### 69. e8c4cc61 prospective — "the dialect prospects are implemented on the Protos type" (STT)

> So when we go from a protos, right, we implement prospective datom [STT: datum] or prospective ethos on the protos type. And that's how the reader then proceeds to try to prospect the protos into a datom [STT: datum].

Provenance: STT.

Standing: raw and undistilled.

---

### 70. e8c4cc61 prospective — "the type embodied into is not known until later passes" (STT)

> so this introduces the concept that we don't quite know what type we're embodying into until later into the reading passes.

Provenance: STT.

Standing: raw and undistilled.

---

### 71. e8c4cc61 prospective — "multiple steps are not feared" (STT)

> So we're not scared to do multiple steps. The multiple steps create a mental model of the machinery, which enforces a correctness in the code that is millions of times more beneficial than the cost of doing these multiple passes [...]

Provenance: STT.

Standing: raw and undistilled. Candidate Spirit/Intent.

---

### 72. e8c4cc61 prospective — "Prospective<Ethos> is borne by the Protos type" (typed)

> Ethos would have a Prospective<Ethos> kind which is Protos type bears. Calling the prospect capability on it would yield an Ethos which needs to have its anatomy designed

Provenance: typed.

Standing: raw and undistilled.

---

### 73. e8c4cc61 designPractice — "a skill explaining how to design Protos" and "a protos skill, for every agent"

> we need a skill explaining how to design Protos.

> no, we need a protos skill. talking in protos dialects is going to be standard. eventually, the models will *only* speak in protos dialects through a protos harness. So it's not only for the designer

> I want to break those up into protos datom and ethos skills. protos should be very general. datom and ethos should show some rust code

> The protos skill shouldnt go so deep into dialects

Provenance: typed.

Standing: raw and undistilled.

---

### 74. e8c4cc61 datomizable — "Datomizable: a default kind describing textual structure and inner context"

> Datomizable would be a kind with a default capability, and born by all ethos types by default. It would describe the textual structure of this type [...]

> This is a notion but I think it's quickly becoming a vision so let's just make it a vision. Spare no ambition.

Provenance: typed and STT.

Standing: raw and undistilled (raised from notion to vision by the
psyche).

---

### 75. 62022e8f concept — "a concept is an abstract object; everything in a protos dialect has a conceptual aspect"

> No, no, the concept. What I was considering is that a concept is an object, basically, because there's an abstract object

> Also, anything that is represented in any protos [STT: proto's] dialect has a conceptual aspect. Even in datom [...]: we have the conceptual form and the corporal form, and the corporal form is the final form.

> The concept is the anatomical layer of Protos, and also it's more than that. I'm not sure. I'm confusing myself now

Provenance: STT.

Standing: raw and undistilled. The psyche marks this as unsettled in
their own words.

---

### 76. 62022e8f headedAndContained — "the headed (implicit) form and the contained (explicit) form"

> I like the headed and contained. I think these terms are appropriate [...] So the headed form and the contained form of an embodiment are the two ways which it can be represented textually. And the contained form is how its embodiment is specified [...] So the headed form is really a syntax facility or a syntax sugar, if you will.

Provenance: STT.

Standing: raw and undistilled.

---

### 77. 62022e8f passes — "the process view"

> As I see it, we need to look more into what this looks like in terms of the actual process: the file comes in, and it's read as such. Then such-and-such capability is called on this object, which recursively calls such-and-such capability on all of its containing objects, sections, or structures, or shapes.

Provenance: STT.

Standing: raw and undistilled.

---

### 78. 62022e8f multiFormConcepts — "multi-form concepts"

> I want to flesh out this concept. [...] in ethos, I'd like to flesh out this idea of multi-form concepts. [...] You would have this multi-form concept where it's struct [STT: struck] with a different number of a different arity.

Provenance: STT.

Standing: raw and undistilled.

---

### 79. 62022e8f designPractice — "the protos skill shows datom, not ethos"

> The ethos that's in the protos skill is inappropriate for multiple reasons, one of which is that it always has to be situated. Also, datom [STT: datum] would be more appropriate just because it's a more basic form of protos

Provenance: STT.

Standing: raw and undistilled.

---

### 80. 62022e8f designPractice — "the page's examples are almost ready as vision"

> This document is really good. Most of the examples and the explanations that I find in here are almost word for word ready to go as vision. [...] I think we're finally starting to get together at least one or two of the cornerstones of the concepts in the Protos meta-language and the Protos dialects

Provenance: STT.

Standing: raw and undistilled.

---

### 81. 62022e8f kinds — "Potential and actualize, universally, layer to layer"

> One, I prefer the terminology potential and actualized over Prospective [...] And that is the kind that I want to use universally to go from one layer to the next. It's more of a rewording on Rust's [STT: RESTS] TryInto. And I think the embodied is probably better because then we keep the corporal for [...] We keep corporal for the layer concept.

Provenance: STT (artifact comment).

Standing: raw and undistilled. **Same-time conflict**: this session
(62022e8f, undated but from the 2026-08-31 Protos Layers artifact
round) replaces Prospective with Potential and prospect with actualize,
while earlier sessions (e8c4cc61, 04db2fd2, db97561c) use Prospective
and prospect. The later term should govern, but it has not been
explicitly confirmed outside this artifact-comment context.

---

### 82. 62022e8f kinds — "the layer capabilities sit on the layer above"

> the structural capability, if we want to say that, or the capability, the structure capability would be on text and the conceive capability would be on structure and the incorporate capability would be on concept.

> it seems that the structural kind is potentially just an alias on a potential structure.

Provenance: STT (artifact comment).

Standing: raw and undistilled.

---

### 83. 62022e8f kinds — "Datomizable narrows too explicitly; ProtoShaped, ProtoFormed, ProtoExpressible"

> ProtoShaped? ProtoFormed? ProtoExpressible? ProtoTextualizable?
>
> Saying Datomizable narrows it too explicitely to datom which could be confusing.

> Maybe there's like an actual word here that like is proto, maybe it's a prototype or proto form. It's kind of cool sounding actually.

Provenance: typed and STT (artifact comment).

Standing: raw and undistilled.

---

### 84. 995a164e designPractice — "associations from different libraries are never mixed; Text to Potential<Protos> in protos, Protos to Potential<Datom> in datom"

> This feels like these two associations would be from different libraries. The text to potential protos would be in protos, and the protos to potential datum [typed; datom] would be in datum [typed; datom]. In order to keep confusion from cascading [...] we shouldn't mix these kinds and types and associations together

Provenance: typed (artifact comment).

Standing: raw and undistilled. Library placement of the associations.

---

### 85. 995a164e designPractice — "step back: find the beautiful Rust first; never assume the infrastructure"

> I really want us to step back. [...] Look at how we look at the beautiful rest [STT; Rust] code that we would want to have to express this, and then work your way back from that: what infrastructure do we need to support that code? [...] Don't assume the infrastructure first.

Provenance: STT.

Standing: raw and undistilled.

---

### 86. 995a164e kinds — "Protoformed is too close to protoform; protosic, protoformal"

> This is logic that sits between the structural layer and the conceptual layer? [...] I think we need different terms here because the adjective "protoformed" is difficult to distinguish in speech from the noun "protoform". Maybe the kind is "protosic" or "protoformal"

Provenance: typed (artifact comment).

Standing: raw and undistilled.

---

### 87. 995a164e rust — "freestanding implementations are forbidden; Rust as assembly language"

> You've used an implementation block that is not implementing a trait, and that is forbidden. We forbid freestanding implementations.

> when we generate Rust, the generated Rust would just use fully qualified names [...] we're using Rust the way we intend to use it, which is more like an assembly language, which is extremely explicit

Provenance: typed (artifact comments).

Standing: raw and undistilled. Reinforces record 43.

---

### 88. b675f3d9 structuralParsing — "arity discriminates; more head delimiters; the Capability enum" (2026-08-27)

> I have actually reconsidered the idea that we can use multiple... that the structural parsing can actually discern between structs of different size to differentiate between different types. [...] Also, I think we should introduce more of the concept of using different delimiters between the head and the delimiter

> <> is a real Protos delimiter of course. I'm surprised you have to ask

Provenance: dictated (with a handwritten page).

Standing: raw and undistilled.

---

### 89. b675f3d9 structuralParsing — "parsing is always dependent on the current context; a character taken in one block is free in another" (2026-08-27)

> No. That's not how it works. [...] ethos parsing is always dependent on the current context in which the parsing is taking place. So in the import block, colon are treated in a certain way [...] And then the same colon used in another block could be used to, obviously, to mean something else since another block would not involve imports.

Provenance: dictated.

Standing: raw and undistilled.

---

### 90. b675f3d9 structuralParsing — "shape conveys type only within context" (2026-08-27)

> this is false since it is context dependent. and the mere fact that something starts with a head could convey the type. and not every block starts with a head, which is also implied elsewhere and false

Provenance: typed.

Standing: raw and undistilled.

---

### 91. 2ef42163 kinds — "real/realize is changed; embody" and "Text is embodiable, and the Embodied is Textualizable" (undated)

> real/realize is changed. debate was on embody/embodied or forge/forged

> embody.

> text isn't textual; the embodied type is. so this brings back the debate of textualizable being a better fit

> you still don't get it. Text is embodiable, and the Embodied is Textualizable

Provenance: typed.

Standing: raw and undistilled. **Same-time conflict**: this session
(2ef42163) rejects real/realize and rules embody, while 06196cc7
(record 17, 2026-08-14) rules "Ok with the real/Realize" and e8c4cc61
uses "Protos is a type which contains the portions and their protosic
anatomy". The 2ef42163 session is undated in the record; if it
predates 06196cc7, it was superseded by the later ruling (real form,
Realize). If simultaneous, it is a genuine conflict. The flow notes
this without resolving it.

---

### 92. 5abf3be8 colonLegalInStringPosition — ": remains legal in a position expecting a string" (2026-08-06)

> and : remains legal in a position expecting a string

Provenance: 2026-08-06T17:39:42Z; entry captured 2026-08-08.

Standing: raw and undistilled.

---

### 93. 5abf3be8 dotOpensDelimiterEverythingIsData — "it opens a delimiter. everything is data" (2026-08-06)

> you mean, it opens a delimiter. everything is data

Provenance: 2026-08-06T17:39:42Z; entry captured 2026-08-08.

Standing: raw and undistilled.

---

### 94. 5abf3be8 encodedFormFingerprintTraitDesign — "encodedform trait must implement the fingerprint trait" (2026-08-06)

> so encodedform trait must implement the fingerprint trait. the
> fingerprint trait by default uses the rkyv of that object and gets
> the hash of it. all references use the encodedid of the thing it
> refers to. does that make sense? or is it encodable and
> fingerprintable? are we using nouns or qualifiers for traits? Id
> really like to talk about traits more, how we design them and name
> them, and use them

Provenance: 2026-08-06T21:58:07Z; entry captured 2026-08-08.

Standing: raw and undistilled. **Entire entry in dead vocabulary** per
2026-08-14 annotation — encodedform, encodable, EncodedName all carry
code/encoded, dropped 2026-08-13.

---

### 95. 5abf3be8 sectionsExistToConferTraits — "What other point is there to have different sections?" (2026-08-06)

> What other point is there to have different sections?

Provenance: 2026-08-06T17:56:10Z; entry captured 2026-08-08.

Standing: raw and undistilled. Conferring traits is the reason
sections exist.

---

### 96. 6863ef19 traitsAsCapabilities — "all traits are qualifiers; reconsider traits as capabilities" (2026-08-13)

> all traits will be qualifiers. I disagree with rust's convention
> (Write Read should be Writable and Readable).

> lets look at an update to the skills, and reconsider traits as
> "capabilities". Rethink the whole concept over and represent it
> this way

Provenance: typed, 2026-08-13T17:17+02:00.

Standing: raw and undistilled. Partially revised by verb acceptance
(record 20) and lean-back (record 47).

---

### 97. 6863ef19 traitsAsCapabilities — "one protos representation per type; a constant could name the dialect" (2026-08-13)

> Any type will only have one protos representation. so the datom::
> version isnt necessary. look for flaws in my logic. It could even
> have a constant variant to give the protos dialect it is
> transcodable into

Provenance: typed, 2026-08-13T18:09+02:00.

Standing: raw and undistilled. "Transcodable" superseded same session.
The one-representation-per-type principle stands.

---

### 98. 6863ef19 encodedFormIsTheCode — "the textual form is data, a type" (2026-08-13)

> It occurred to me that we haven't discussed the different forms.
> And this is very important, actually. So, the textual form of a
> thing is data. So, it's a type. Or we say it's textually
> expressible or something like that.

Provenance: dictated.

Standing: raw and undistilled.

---

### 99. 6863ef19 theBestShape — "the criterion" (2026-08-13)

> If we see from a high level here, if we express things properly,
> we will minimize the amount of code. The minimum amount of code
> for the most elegant machinery, which can be easily understood by
> an engineer and easily extended and easily introspected, is the
> best shape.

Provenance: dictated. The psyche flagged this may contain Intent.

Standing: raw and undistilled. Candidate Spirit/Intent.

---

### 100. 55d18f4f signalIsOurMessagingLayer — "Signal is our messaging layer; the CLI transforms the textual form into Signal" (2026-08-08)

> Signal is our messaging layer, and the CLI's role is to transform text into Signal. So we used to call it NOTA, now it's DOTOS. [...] So it's the textual form, the CLI transforms the textual form into actual Signal.

Provenance: 2026-08-08T11:45:33.818Z.

Standing: raw and undistilled. DOTOS name later superseded by Datom.

---

### 101. ba906ae2 signalIsOurMessagingLayer — "signal. signal. signal." (2026-08-14)

> signal. signal. signal. that is what we call it. signal. lets
> find a place to explain that clearly

Provenance: typed, 2026-08-14T15:12+02:00.

Standing: raw and undistilled.

---

### 102. 06196cc7 threeStacks — "universal stuff lives in protos; the protos repo opens for the substrate" (2026-08-14)

> what shared framework? I want universal stuff in protos, since
> all dialects will use it. Im not worried about rewriting whatever
> is in protos right now since nothing works anyway. [...] But id like to
> know what you mean by Codec

Provenance: typed.

Standing: raw and undistilled. The substrate — walk machinery, Shape
vocabulary, ShapeDefined, Head, Realize, Textualize, block scanner,
string carriers — is homed in protos.

---

### 103. d63804f2 newtypeWrappingAndSingleFieldStructs — "I don't like the single field struct" (2026-08-07)

> And what are the double new type wrapping about? I don't like it.
> I don't like the single field struct.

Provenance: 2026-08-07T18:47:12.105Z.

Standing: raw and undistilled.

---

### 104. 2b34fafa rustComponentArchitecture — "the architecture guard is stupid; get rid of it" (2026-08-18)

> "thats so stupid. I want to get rid of that, and train against this
> level of expert foolishness."

> "Using mechanical tests isnt going to create good ontology;
> trait/types design is ontology in code."

> "what you said is true, but its stupid because it writes a tool
> for this single repo, instead of a universal tool being created to
> test this for any repo"

Provenance: typed.

Standing: raw and undistilled. On the protos repo's architecture
guard.

---

### 105. e4be1c4a rustComponentArchitecture — "single-implementor traits: a trait design training problem" (2026-08-16)

> "i dont see the purpose, as in needing a trait specifically for
> this one impl. what other traits does block implement? if it
> implements any other related trait, we have a trait design
> training problem"

> "the problem isnt that it only has one implementor, but that many
> of those traits should be one."

Provenance: typed.

Standing: raw and undistilled. On protos crate traits.

---

### 106. f426777b skillDesigning — "the protos philosophy was not understood; training is lacking" (2026-08-26)

> One thing really worth noting here is that you did not understand
> the proto's [protos] philosophy or way of doing things in how you
> presented me your first prototype.

> Your proto scale [protos skill] proposal is too intellectual. [...]
> if there is a protoskill [protos skill], it would be quite simple.
> And then we would have an ethos skill and an an adam [a datom]
> skill, which would be more... Flashed [fleshed] out

> your Protos example is wrong, on top of being way too specific.
> Protos is the high level concept

> that's still too specific for Protos.

> you can't explain Protos well

Provenance: dictated and typed.

Standing: raw and undistilled.

---

### 107. ac1e9ec8 datomIsData — "you've mixed up datom with ethos. datom is data" (2026-08-26)

> you've mixed up datom with ethos. datom is data

Provenance: typed.

Standing: raw and undistilled. Boundary enforcement: protos parse
machinery (shapes, contexts, Realize/Textualize) was wrongly placed
in a datom distillation.

---

### 108. 68512643 negatives — "datom is the data dialect of the Protos family" (2026-08-23)

> Datom would be the syntax in Ethos, whereby data is represented
> since it is the data sort of substrate of or dialect of the Protos
> family

Provenance: dictated.

Standing: raw and undistilled. Part of the negatives discourse.

---

### 109. c6b71b4c archive-threeStacks — "obviously protos" (2026-08-10)

> obviously protos

> obviously NOTA

> people wont remember dotos, eidos or rhetos. it just wont stick at
> all

Provenance: typed, 2026-08-10T12:44Z.

Standing: **archived** — distilled into Vision/datom.md. The Protos
name confirmation.

---

### 110. 13cfc23f threeStacks — "the three stacks" (2026-08-10)

> So currently we have... I've made a mess because I've tried to rename
> everything. [...] the Ethos.

Provenance: 2026-08-10T12:12Z. STT: "Frotos" probably = Protos,
"demons" = daemons.

Standing: raw and undistilled. The three-stack model speech.

---

### 111. e8c4cc61 datomSyntax — "a single ; is for comments; style: a space inside a bracket delimiter"

> I guess a single ; is for comments now. semi-colon isnt load bearing anymore so that works.

> it would be good style to leave a space between the delimiter and the next thing inside of it, both at the beginning and the end.

Provenance: typed and STT.

Standing: raw and undistilled.

---

### 112. 2b34fafa traitsAsCapabilities — "ruling: infinitive verb form for action traits" (2026-08-21)

> It would be walk. So we would use the sort of infinitive form of
> the word, of the verb, I mean. If it's an action that can be
> purely described as an action, like write, read, resolve, create.

Provenance: dictated.

Standing: raw and undistilled. Partially revisited by lean-back
(record 47).

---

## Vision archived

### 113. c6b71b4c archive-threeStacks — "obviously protos" (record 109)

As noted above, archived by flow 68512643; distilled into
Vision/datom.md. The Protos name confirmation sits here.

---

## Notion

### 114. 62022e8f notion/layerMatching — "two-way logic between the structural and conceptual layers" (undated)

The psyche explicitly marks this a notion: "this is sort of a notion
that we need to crystallize before it really becomes a vision."

> And on the whole, you said structure, and this is big. [...] the vision
> that I have is for this logic that allows us to go both ways between
> the conceptual layer and the structural layer [...] the data has to be
> generated from all of the concepts. So essentially all the
> embodiments, all of the types. [...] all of the embodiments would sort
> of come up to this sort of single enumerator that would contain them
> all.

> The match just comes in with the context, which is just a variant,
> and it just [...] goes through the whole roster, and the match has to
> be on both the context and the structure.

> no two embodiments claim the same shape in that context [compile-time
> check]. [...] more logic that is easier to reason about is better than
> a smaller, faster machine that no one can understand

Provenance: STT.

Standing: notion. The psyche is still sorting this out.

---

### 115. 62022e8f notion/terminology — "Corporal for Embodiment; concept; the perspective is the better term"

The psyche invites a brainstorm:

> One is an Embodiment, or I was even thinking of going from
> Embodiment [...] to Corporal

> the perspective is actually the better term. I want you to even
> just rethink a lot of our terminology here

Provenance: STT.

Standing: notion. Terminology brainstorm.

---

## Typed transcript words found in no log

No psyche typed words about protos were found in the searched
transcripts that are not already carried in the vision records above.
The sessions searched: 55d18f4f, 5abf3be8, a5587095, ba906ae2,
6863ef19, 2b34fafa, ac1e9ec8, 68512643, e8c4cc61, 995a164e, 62022e8f,
b675f3d9, db97561c, 04db2fd2, f426777b. All "protos" mentions in user
messages were either skill-loading artifacts or messages already
captured in vision records.

---

## Tensions and oddities

1. **Import separator conflict** (records 6, 52): The 2026-08-07
   ruling says `/` for imports, colon for transformers only. The
   2026-08-20 examples (2b34fafa) use colon for external source pulls.
   The b675f3d9 distillation proposal surfaced this; it remains
   unresolved.

2. **embody vs. realize** (records 17, 91): Session 2ef42163 rejects
   real/realize and rules embody; session 06196cc7 (2026-08-14) rules
   "Ok with the real/Realize." If 2ef42163 predates 06196cc7, it was
   superseded. If simultaneous, a genuine conflict. The 2ef42163
   session carries no date on its records.

3. **Prospective vs. Potential** (records 53, 81): Sessions 04db2fd2,
   db97561c, e8c4cc61 use Prospective; session 62022e8f (artifact
   comments) replaces it with Potential. Potential is the later word
   but was spoken only in artifact comments on one page.

4. **writable vs. verb traits** (records 20, 47, 96, 112): The
   qualifier/verb pendulum: 2026-08-13 "all qualifiers", 2026-08-14
   "verbs accepted", 2026-08-21 "infinitive verb form", 2026-08-26
   "lean back to writable > write". The lean-back does not explicitly
   address individually confirmed names (Textualize, Realize).

5. **"you can't explain Protos well"** (record 106): After four
   drafts, the Designer could not articulate the protos concept. The
   psyche has not provided their own articulation. The protos skill
   remains unwritten.

---

## Unapproved distillation proposal

The b675f3d9 distillation proposal
(reports/distillProposalProtosDatom.md) proposed multiple statements
for Vision/protos.md. Only "Direction" (record 2) was approved and
landed. The remaining proposed statements — "The shared style",
"Everything is data", "One representation", "Parsing in context",
"Shape in context tells the type", "Struct and vector", "Angle
brackets", "Forms of a value", "Shape-defined types", "Logic planes"
— remain unapproved. They sit in
flows/b675f3d9/reports/distillProposalProtosDatom.md.

The addendum (flows/acbb6006/reports/distillProposalProtosDatomAddendum.md)
also remains unapproved.

---

## Sources

Account of what was read and what was written, in order:

### Read

1. Vision/protos.md (distilled)
2. Intent/protosParsing.md (distilled Intent)
3. vision-raw/parserIsTheParser.md
4. vision-raw/encodedFormIsTheCode.md
5. vision-raw/colonConfusion.md
6. vision-raw/colonFormTransformerSyntax.md
7. vision-raw/importResolution.md
8. vision-raw/itsATranslator.md
9. vision-raw/protosIsTheSharedStyle.md
10. vision-raw/structuredStringType.md
11. vision-raw/traitsAsCapabilities.md
12. vision-raw/mainFunction.md
13. flows/04db2fd2/vision/textualTypes.md
14. flows/04db2fd2/vision/directionAsymmetry.md
15. flows/04db2fd2/vision/multiPass.md
16. flows/04db2fd2/vision/delimiters.md
17. flows/04db2fd2/vision/decomposable.md
18. flows/04db2fd2/vision/text.md
19. flows/04db2fd2/vision/delineate.md
20. flows/04db2fd2/vision/portion.md
21. flows/04db2fd2/vision/anatomy.md
22. flows/04db2fd2/vision/kinds.md
23. flows/06196cc7/vision/encodedFormIsTheCode.md
24. flows/06196cc7/vision/traitsAsCapabilities.md
25. flows/06196cc7/vision/codeIsLanguage.md
26. flows/06196cc7/vision/threeStacks.md
27. flows/55d18f4f/vision/itsATranslator.md
28. flows/55d18f4f/vision/signalIsOurMessagingLayer.md
29. flows/55d18f4f/vision/highLevelView.md
30. flows/e8c4cc61/vision/protos.md
31. flows/e8c4cc61/vision/prospective.md
32. flows/e8c4cc61/vision/designPractice.md
33. flows/e8c4cc61/vision/datomizable.md
34. flows/e8c4cc61/vision/kinds.md
35. flows/e8c4cc61/vision/datomSyntax.md
36. flows/e8c4cc61/vision/ethosFileAnatomy.md
37. flows/2b34fafa/vision/protosIsTheSharedStyle.md
38. flows/2b34fafa/vision/traitsAsCapabilities.md
39. flows/2b34fafa/vision/importResolution.md
40. flows/2b34fafa/vision/sourceNotCrate.md
41. flows/2b34fafa/vision/rustComponentArchitecture.md
42. flows/a5587095/vision/protosIsTheSharedStyle.md
43. flows/a5587095/vision/colonFormTransformerSyntax.md
44. flows/a5587095/vision/structuredStringType.md
45. flows/a5587095/vision/rustComponentArchitecture.md
46. flows/ba906ae2/vision/protosIsTheSharedStyle.md
47. flows/ba906ae2/vision/encodedFormIsTheCode.md
48. flows/ba906ae2/vision/signalIsOurMessagingLayer.md
49. flows/d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md
50. flows/db97561c/vision/prospective.md
51. flows/db97561c/vision/promptCrafting.md
52. flows/db97561c/vision/psycheLogging.md
53. flows/6863ef19/vision/codeIsLanguage.md
54. flows/6863ef19/vision/encodedFormIsTheCode.md
55. flows/6863ef19/vision/signalIsOurMessagingLayer.md
56. flows/6863ef19/vision/traitsAsCapabilities.md
57. flows/6863ef19/vision/theBestShape.md
58. flows/62022e8f/vision/passes.md
59. flows/62022e8f/vision/multiFormConcepts.md
60. flows/62022e8f/vision/headedAndContained.md
61. flows/62022e8f/vision/concept.md
62. flows/62022e8f/vision/designPractice.md
63. flows/62022e8f/vision/kinds.md
64. flows/62022e8f/vision/symbols.md
65. flows/995a164e/vision/contexts.md
66. flows/995a164e/vision/explodedForm.md (not protos-specific)
67. flows/995a164e/vision/designPractice.md
68. flows/995a164e/vision/kinds.md
69. flows/995a164e/vision/rust.md
70. flows/b675f3d9/vision/structuralParsing.md
71. flows/2ef42163/vision/kinds.md
72. flows/358f143a/vision/realizer.md
73. flows/5abf3be8/vision/colonLegalInStringPosition.md
74. flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md
75. flows/5abf3be8/vision/encodedFormFingerprintTraitDesign.md
76. flows/5abf3be8/vision/sectionsExistToConferTraits.md
77. flows/e4be1c4a/vision/rustComponentArchitecture.md
78. flows/f426777b/vision/spokenVocabulary.md
79. flows/f426777b/vision/skillDesigning.md
80. flows/13cfc23f/vision/threeStacks.md
81. flows/c6b71b4c/vision/archive-threeStacks.md
82. flows/68512643/vision/negatives.md
83. flows/ac1e9ec8/vision/datomIsData.md
84. flows/acbb6006/vision/distillation.md
85. flows/acbb6006/vision/nexus.md
86. flows/b675f3d9/vision/archive-distillation.md
87. flows/b675f3d9/reports/distillProposalProtosDatom.md
88. flows/acbb6006/reports/distillProposalProtosDatomAddendum.md
89. flows/62022e8f/notion/layerMatching.md
90. flows/62022e8f/notion/terminology.md
91. Vision/datom.md (for protos context)
92. Vision/sources/ (no protos.md found)
93. design/ProtosEngine/ (directory listing only)
94. flows/04db2fd2/log.md (for landed-distillation context)
95. flows/b675f3d9/log.md (for distillation-proposal status)
96. Transcripts for sessions: 55d18f4f, 5abf3be8, a5587095, ba906ae2,
    6863ef19, 2b34fafa, ac1e9ec8, 68512643, e8c4cc61, 995a164e,
    62022e8f, b675f3d9, db97561c, 04db2fd2, f426777b

### Written

1. flows/4decf7/reports/protos.md (this report)
