# Datom Syntax Transcript Audit

Every typed message by the living psyche about datom syntax and its
ancestors (NOTA, Dotos, Protos-family text notation), extracted from
transcripts, grouped by sub-subject, in chronological order within
each group.

Legend:
- RECORDED = verbatim or near-verbatim text found in Vision/, flows/*/vision/, or psyche-raw/
- **UNRECORDED** = no matching record found in any vision or psyche-raw file
- SUPERSEDED = later message overrides this one

## Delimiters and blocks (general)

### 236af273:99 [2026-08-03T12:37:43.347Z] RECORDED (Vision/datom.md references structural parsing)

> the *text* is the payload. structural parsing means we can represent a payload any way we want.

### 236af273:101 [2026-08-03T13:44:31.366Z] **UNRECORDED**

> >  Stream.Observer.{...} (two dotted symbols before the payload)
>
> the *text* is the payload. structural parsing means we can represent a payload any way we want.
>
> >  whether the third (or nth) dotted symbol binds as a further transformer parameter,
>
> You mean for *potential* uses of this?
>
> ```dotos
> ExpectedObject.{ Stream ;; name
>                  SingleDottedPrefix.TypeName ;; Variant and its payload - could also be DottedPrefix.[TypeName AnAdditionalTypeForEachAdditionalDottedPrefixChainedSymbol ... ]
>                  PossiblyOtherMetadata
>                }
> ```

### 5abf3be8:471 [2026-08-06T17:39:42Z] RECORDED (flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md)

> you mean, it opens a delimiter. everything is data

### 6b31eff3:80 [2026-08-04T08:47:11.293Z] **UNRECORDED**

> >  Bare < > as data delimiters buy nothing
>
> so its the same as {| |} ?
>
> >  Name.{, Name{, and Name { all tokenize to exactly 2 tokens
>
> Then it's Name.{ which is much better visually

### 6b31eff3:677 [2026-08-04T19:52:28.102Z] **UNRECORDED**

> yes, cut it. and you can keep the co-reference syntax.
>
> << >> should be kept for the next special syntax need we might encounter. it is the only good delimiter pair left for extending the language

### 06196cc7:276 [2026-08-13T21:54:32.631Z] RECORDED (flows/06196cc7/vision/archive-datomSyntax.md)

> on the block pass: Im willing to increase the complexity a bit to allow some blocks, like strings, to allow other delimiters to be ignored until it closes, which would allow a string to contain [ { ( etc
>
> And the dotted prefix of a delimiter must be part of its type. it could be a universal type, and unprefixed blocks simply have no prefix. what do we want to call the prefix shape?

## Strings: parentheses, curly quotes, bare strings

### 6b31eff3:120 [2026-08-04T09:09:57.035Z] **UNRECORDED** (SUPERSEDED by later rulings)

> if "" is different from "", then we should use it for strings instead of () and (||), and make it common-indentation safe, so it can parse indented blocks properly. but Ill need an easy way to type it [...]
>
> so we should drop the piped delimiters. I dont even think we need a complex struct/enum, if we use a special delimiter for traits(generics), we get optional generics using unambiguous parsing trick. im debatting different delimiters in my head right now.
>
> ```ethos
> Vector.<Sortable>
> Vector<Sortable> ;; cognitive reuse of rust, right?
> Vector.<<Sortable>> ;; inefficient apparently
> Vector<<Sortable>>
> ```

Note: curly quotes for strings was an early float; later the psyche settled on parentheses as the default string delimiter (a5587095:133, 06196cc7:316).

### a5587095:133 [2026-08-11T16:51:32.326Z] RECORDED (Vision/datom.md, flows/a5587095/vision/archive-datomSyntax.md)

> On parenthesis: It would be strange for parenthesis to be unused in datom. They are a major symbol of cognition.
>
> I think we are wrongly using parenthesis in ethos now, since we introduced X:Transformer syntax, which differentiates transformers (and some transformers might expect a single vector, in which case .[ is better, and for the rest expecting a structured input .{ is the right delimiter). This would free patenthesis completly, and I have an idea for a revolutionary type; a structured string type - something that would revolutionize LLM performance by exposing the emphasis and other structural aspects which a plain string simply doesnt have. think of it as an annotated string

### 06196cc7:197 [2026-08-13T21:18:31.018Z] RECORDED (flows/06196cc7/vision/archive-datomSyntax.md)

> we'll postpone the Meaning type in datom to get a working syntax asap. lets accept a () or the curly quotes for strings for now, with the actual shapedefined implementation just casting both into a string for now, with a comment to implement the Meaning type later (the super-string type we discussed before).

### 06196cc7:316 [2026-08-13T22:47:05.758Z] RECORDED (Vision/datom.md, flows/06196cc7/vision/archive-datomSyntax.md)

> Ok now Im full backpedaling on the () for simple strings, since parenthesis are so common in strings, and curly brackets are not. But there is an interesting pattern here which is tha parentheses are already used in text as a way to *markup* the text; so my complex-string idea is actually right on the money. I would just let the block parser balance parentheses until it reaches the final unbalanced ). So im not backpedalling actually; go for balance-based, where an unbalanced parenthesis needs to be escaped.

Same message, later part (RECORDED, archive-datomSyntax.md):

> A string that doesnt need quotes *must not* be quoted

Same message, later part (RECORDED, archive-datomSyntax.md):

> I would prefer to default to parenthesis for string delimiters. I might drop the idea of using parenthesis for a specific Meaning type, and just use it for strings. full vertical length delimiters have a cognitive ease to them that quotes simply cannot even rival

### 06196cc7:405 [2026-08-13T23:20:11.791Z] RECORDED (Vision/datom.md)

> If its a string, then it can use symbols which would be load bearing in other situations, just like delimiters in string blocks. no problem there. lets make the machinery fit for this, bullet proof not by lots of complex code, but by the right abstraction layers.

### 6b31eff3:725 [2026-08-04T19:55:08.151Z] **UNRECORDED**

> > Text <-> String
>
> I never said we need to call strings text

### 6b31eff3:741 [2026-08-04T20:00:33.168Z] **UNRECORDED**

> String is correct; remove the table entry

## Braces, structs, enums, variants

### 236af273:140 [2026-08-03T17:39:34.663Z] **UNRECORDED**

> > Struct.{...}
>
> thanks for reminding me why agents are not going to design my syntax.
>
> The prefix should universally be the name. then something differentiates what comes after [...]
>
> ```ethos
> ;; Name    transformer
> Something!ComplexStruct.{ ... }
> Observer!Stream.{ ... }
>
> ;; Regular struct
> X.{ ... }
> ;; Regular enum
> Y.[ ... ]
> ```

Note: the `!` separator was floated here and SUPERSEDED by the `:` colon-form (5abf3be8:463, 2026-08-06).

### 236af273:176 [2026-08-03T17:57:59.626Z] **UNRECORDED** (SUPERSEDED by pipe retirement 6b31eff3:264)

> I also think we should use {||} for non-trivial structs (and define what that is; what is the greatest need in non-trivial struct? generics (which means traits for us?), and [||] for non-trivial enums. what do you think?

### 236af273:205 [2026-08-03T18:13:40.980Z] **UNRECORDED** (SUPERSEDED by pipe retirement 6b31eff3:264)

> > pipe-text [| |]
>
> wtf are you talking about? pipe text is (||)

### 06196cc7:316 [2026-08-13T22:47:05.758Z] RECORDED (Vision/datom.md, archive-datomSyntax.md)

> I dont understand. we have clearly enunciated what those are. the first is a struct, the second is (now) a string-carrying variant. Why wasnt that obvious?

(On `{...}` = struct and `X.(...)` = string-carrying variant.)

### 06196cc7:361 [2026-08-13T23:04:42.944Z] **UNRECORDED** (the specific question is not in any vision file)

> > omitted the variant head on Entry::Group and Entry::Tags, because their payloads already carry headed shapes and Group.Group.{...} would double the same name.
>
> I dont understand. where does Group.Group.{ come from?
> There should be a string with inner balanced parentheses

### 06196cc7:672 [2026-08-13T12:03:44.075Z] **UNRECORDED**

> > (DotBraced, |walk| Ok(Entry::Group(walk.read()?))),
>
> no, I said data, not functions

## Head (the dotted prefix)

### 06196cc7:276 [2026-08-13T21:54:32.631Z] RECORDED (archive-datomSyntax.md)

> And the dotted prefix of a delimiter must be part of its type. it could be a universal type, and unprefixed blocks simply have no prefix. what do we want to call the prefix shape?

### 06196cc7:316 [2026-08-13T22:47:05.758Z] RECORDED (archive-datomSyntax.md, Vision/datom.md)

> I like the Head terminology actually. lets make it official
>
> for the text block type? Head

### 06196cc7:316 [2026-08-13T22:47:05.758Z] RECORDED (Vision/datom.md, archive-datomSyntax.md)

> is Note a variant? then yes. does it have a special shape? then it might. It depends.
>
> Like in ethos, when we are defining types, X.{} is a struct called X, and textualizing that type back will re-emit X.{} which must be understood in the right context if printed alone, or inserted in the right position, if the whole source is textualized

## Map and vector

### a5587095:171 [2026-08-11T17:15:26.696Z] RECORDED (Vision/datom.md, archive-datomSyntax.md)

> Yes, map would use .[ since a map is conceptually a list of key/values

## Colon form and transformer syntax

### 236af273:147 [2026-08-03T17:42:06.006Z] RECORDED (colonFormTransformerSyntax.md notes the line of descent from ! to | to :)

> maybe Name|Transformer is visually easier to see. or maybe something else. Name-Transformer?

### 5abf3be8:463 [2026-08-06T17:25:39.072Z] RECORDED (psyche-raw/Vision/colonFormTransformerSyntax.md)

> unrelated first. I think Name:TransformerName.( ... ) is the better syntax for named transformers. The other syntax will create difficult parsing and reasoning. Do you agree?

### 5abf3be8:471 [2026-08-06T17:39:42Z] RECORDED (flows/5abf3be8/vision/colonLegalInStringPosition.md)

> and : remains legal in a position expecting a string

### d63804f2:127/129 [2026-08-07T18:28-33Z] RECORDED (psyche-raw/Vision/colonConfusion.md)

> I would rather not create confusion with :

### d63804f2:605 [2026-08-07T22:09:56.435Z] RECORDED (psyche-raw/Vision/colonConfusion.md, observerFixtureBlessed.md)

> the fixture is blessed, and / for imports

### a5587095:133 [2026-08-11T16:51:32.326Z] RECORDED (colonFormTransformerSyntax.md)

> I think we are wrongly using parenthesis in ethos now, since we introduced X:Transformer syntax, which differentiates transformers (and some transformers might expect a single vector, in which case .[ is better, and for the rest expecting a structured input .{ is the right delimiter).

## Generics and angle brackets

### 6b31eff3:156 [2026-08-04T09:41:52.824Z] **UNRECORDED** (SUPERSEDED by a5587095:133 which moves transformer payloads to .[ and .{)

> we could use .() for transformers, and <> for generics

### 6b31eff3:158 [2026-08-04T09:42:51.469Z] **UNRECORDED**

> and I want the Result<Vector<Sortable> Error> syntax for generics, since its more token efficient than using a dot, and recycles rust cognition

### 6b31eff3:419-423 [2026-08-04T12:41-44Z] **UNRECORDED**

> ``` ethos
> Sorted.{Vector<Ordered>}              ;; struct Sorted<Ordered: Ord>(Vec<Ordered>)
> Range.{<Ordered> <Ordered>}               ;; struct Range<Ordered: Ord>(Ordered, Ordered)
> Status.[Pending Ready.<Numeric>]  ;; enum with a generic variant payload
> ```
>
> I want to create a translation table in logos' rust textualform emission for correctNaming <-> incorrectNaming, like Ordered and Ord, so we can have legible ethos/nomos/logos
>
> 1. I dont understand. explain
>
> 2. are Vector, Option, Map really generics though? Im not talking about how rust sees it, but how we decide to see it. Or do we want to call those things generics? or something else?

### 236af273:282-284 [2026-08-03T19:32-34Z] **UNRECORDED**

> Bridge.{|
>     {Left Sortable}
>     {Right Sortable}
> |}
>
> Obviously Sortable needs to be in scope, and this would create different rust than the example its based on. and the trait would be obtained by its usage (no repitition)

Note: the `{| |}` extended delimiters were SUPERSEDED when pipes retired (6b31eff3:264).

## Pipe retirement

### 6b31eff3:264 [2026-08-04T10:40:06.467Z] **UNRECORDED**

> > does | retire from the grammar entirely?
>
> obviously. youre demonstrating that LLMs arent really intelligent yet by asking. One syntax necessarily replaces another

## Numbers and decimal representation

### d63804f2:129 [2026-08-07T18:33:22.940Z] **UNRECORDED** (the decimal/float question itself is not recorded)

> I also dont like the version number. which makes me wonder; how do we represent floating integer, represent in decimal (0.1)? Technically, if the expected position is a float, then it should be aple to read Interface.0.1.0 right? although the syntax he has now is technically more correct {MajorVersion SubVersion MinorRevisionVersion}, which is strictly typed. but I was still wondering about the decimal representation (or float, which could be represented as such, unless Im wrong about that, you can verify)

## Structured string / Meaning type

### a5587095:171 [2026-08-11T17:15:26.696Z] RECORDED (flows/a5587095/vision/structuredStringType.md, archive-datomSyntax.md)

> 1. I am considering it, yes. This would require a new type (in rust, later ethos-generated) which can be met with either a curly quotes or parenthesis (two variants, legacy and structured). The structured type would allow for an arbitrary depth, since it is a graph of sorts.
>
> 3. shape is still up in the air, but () would be the delimiter

### a5587095:229 [2026-08-11T17:42:29.743Z] RECORDED (flows/a5587095/vision/structuredStringType.md)

> remember; once we open the Meaning delimiter (that what were calling it), all the delimiters and structured parsing spectrum is available, until that closing delimiter comes in and changes the parser's context; that is how all our languages parse and why we can design so freely. This is important and is the part of the code which can be shared between all parsers (should be in protos; protos is the name we give to the style which all our dialects share; hence why the final fully-decomposed engine with 3 daemons is the protos engine, with datom sort of sitting besides it, as it is only for pure, typed data)

### a5587095:231 [2026-08-11T17:43:09.691Z] RECORDED (flows/a5587095/vision/structuredStringType.md)

> I want the most advanced structured meaning system ever made

### a5587095:253 [2026-08-11T17:52:17.867Z] RECORDED (flows/a5587095/vision/structuredStringType.md)

> what do you mean by self-describing tag? The way I see it right now is there would be enums which would be used throughout the tree, like Emphasis.{} or similar, but its still too early to tell

### a5587095:364 [2026-08-12T01:26Z] RECORDED (flows/a5587095/vision/structuredStringType.md)

> I dont understand. A string expects a string. we can have another type for MeaningOrString (or maybe Meaning is the type that can also expect a plain string, which can derive a simple structured meaning (PlainText?)) which implements ProtosShape (Which I think is misnamed - its more like MultiplePossibleTypesDefinedByShape which is obviously way too long - maybe you have a better suggestion). So that is another ProtosShape type field (I dont know why I zoomed in on the vector of them, theyre totally possible in a particular struct field too!)

### 06196cc7:224 [2026-08-13T21:24:42.375Z] RECORDED (flows/06196cc7/vision/encodedFormIsTheCode.md)

> can we reliably find all the blocks in a first pass so we have a bunch of types (text blocks) to cast from into working form? I dont like working, it smells like a verb. Same with meaning

## De/serialization and parsing approach

### 012fbf07:240 [2026-08-11T11:51:41.718Z] RECORDED (flows/012fbf07/vision/archive-threeStacks.md)

> 1 yes, direct to typed structs. 3 what is reflection? no self-describing tags
>
> datom is just a renamed dotos, so there was no need to create a new repo. unless I missed something.

### 012fbf07:312 [2026-08-11T12:05:12.069Z] RECORDED (flows/012fbf07/vision/archive-threeStacks.md)

> > ethos-rust consumes datom's parser
>
> no, I dont think so. they share an approach, but are different languages. they could have a shared substrate (traits with a shared implementation and types)

### a5587095:253 [2026-08-11T17:52:17.867Z] RECORDED (flows/a5587095/vision/protosIsTheSharedStyle.md)

> > does the no-self-describing-tags ruling still bind?
>
> you keep asking that. what do you mean by self-describing tag?
>
> > the outer positional decode suspends at (
>
> no, there is always a parsing context. it doesnt suspend, it *changes*, but the underlying mechanism is always the same; Now, we are parsing in context X and can therefore expect A, B or C shapes of things

### a5587095:398 [2026-08-12T19:21:27.359Z] Partially RECORDED (recursion/position in protosIsTheSharedStyle.md)

> > nothing routes centrally; meeting a shape yields a type, and the type carries its own context.
>
> because of recursion, the position of the parent context still needs to be kept, so that returning to the parent context resumes at the following position. Do you understand? Show me with an example
>
> > BareAtom
>
> You mean BareSymbol?
>
> What do we call X.[/{/( ? Since they are distinct shapes, they should be distinct variants. What do you think?

The specific items **UNRECORDED** from this message:
- "BareSymbol" correction (BareAtom -> BareSymbol)
- "X.[/{/( are distinct shapes, should be distinct variants"

### a5587095:337 [2026-08-11T22:57:51.581Z] **UNRECORDED**

> I read design/ProtosEngine/twoWayStructuralTranscoding-2026-08-11.md - the more complex trait will be a vector of ProtosShape's (welcome to propose other names), when the structure dictates the outer type, for example in ethos when X.{ means a struct, and Y.[ means an enum, and Z:Transform.[/{ means different kinds of transformers

### 06196cc7:672 [2026-08-13T12:03:44.075Z] **UNRECORDED**

> > (DotBraced, |walk| Ok(Entry::Group(walk.read()?))),
>
> no, I said data, not functions

### 06196cc7:141 [2026-08-13T20:59:16.826Z] RECORDED (flows/06196cc7/vision/traitsAsCapabilities.md)

> I see a problem myself; when reading text, we dont know what we're reading, so how do we call a method without a type?
>
> Conceptually, we need to give a type to the text block, then we can have an encode trait on that, and textualize on the true type.

## Naming (Datom vs Dotos vs NOTA)

### 012fbf07:218 [2026-08-11T11:23:59.524Z] **UNRECORDED** (the phrasing and question are not recorded)

> so you created a new repo for datom. were you planning to reuse the dotos code? do you know how I want the datom de/serializer to work?

### 01a02a34:288 [2026-08-22T17:32:33.328Z] RECORDED (flows/01a02a34/vision/archive-datum.md)

> And you're saying dotos, but like that's the old syntax, which is being replaced by datum, which is, you know, has the same concept.

### 01a02a34:439 [2026-08-22T21:43:29.015Z] RECORDED (flows/01a02a34/vision/archive-datum.md)

> And use datom instead of dotos.

### 68512643:406 [2026-08-23T13:06:42.341Z] RECORDED (Vision/datom.md captures the essence)

> [long passage about "it does not generate rust" being true in context because we aren't there yet; might eventually get there but would need explicit context]

### 68512643:660 [2026-08-24T10:01:21.168Z] RECORDED (Vision/datom.md)

> chosen for it's energetic power
>
> schema is the abandoned ancestor of ethos, not datom. so this line could be ambiguous, and misses dotos, the other temporary name Nota took
>
> another enum if sub operations are wanted, and strut or vector for final options. a struct could embed further sub operations even, or any combination imaginable really.

### 01a03d6e:300 [2026-08-26T10:10:32.842Z] RECORDED (flows/01a03d6e/vision/dotosFiles.md)

> There should be no Dodos files anymore. [STT: Dotos]

## Interface shape (enum-first)

### 68512643:917 [2026-08-24T10:30:26.871Z] RECORDED (Vision/datom.md)

> output *is* an enum. always. even the most basic response interface must be an enum; Success/Failure.

## What the syntax must not be / negatives

### 6b31eff3:264 [2026-08-04T10:40:06.467Z] **UNRECORDED** (the pipe retirement)

> > does | retire from the grammar entirely?
>
> obviously. youre demonstrating that LLMs arent really intelligent yet by asking. One syntax necessarily replaces another

### 6b31eff3:666 [2026-08-04T19:48:04.393Z] **UNRECORDED**

> > Observer.(...)
>
> why am I still seeing this?

Note: by this point `.(` for transformers had been superseded by the colon form.

### 6b31eff3:725 [2026-08-04T19:55:08.151Z] **UNRECORDED**

> > Text <-> String
>
> I never said we need to call strings text

### 6b31eff3:741 [2026-08-04T20:00:33.168Z] **UNRECORDED**

> String is correct; remove the table entry

### 06196cc7:672 [2026-08-13T12:03:44.075Z] **UNRECORDED**

> no, I said data, not functions

(On seeing closures/functions in the shape-determination table instead of pure data.)

## ShapeDefined / ProtosShape and parsing traits

### a5587095:337 [2026-08-11T22:57:51.581Z] **UNRECORDED**

> the more complex trait will be a vector of ProtosShape's (welcome to propose other names), when the structure dictates the outer type, for example in ethos when X.{ means a struct, and Y.[ means an enum, and Z:Transform.[/{ means different kinds of transformers

### a5587095:398 [2026-08-12T19:21:27.359Z] Partially **UNRECORDED**

> You mean BareSymbol? [correcting BareAtom]
>
> What do we call X.[/{/( ? Since they are distinct shapes, they should be distinct variants.

## Supersession chain / reversals

1. **!-separator -> |-separator -> :-separator**: 236af273:140 (2026-08-03) floated `Something!ComplexStruct`; 236af273:147 (same day) floated `Name|Transformer`; 5abf3be8:463 (2026-08-06) ruled `Name:TransformerName.(...)`. The exclamation and pipe forms are SUPERSEDED.

2. **Pipe delimiters -> retirement**: 236af273:176 (2026-08-03) proposed `{||}`/`[||]` for non-trivial structs/enums; 6b31eff3:264 (2026-08-04) retired `|` from the grammar entirely.

3. **Curly quotes for strings -> parentheses -> backpedal -> balance-based parentheses**: 6b31eff3:120 (2026-08-04) floated curly quotes for strings; a5587095:133 (2026-08-11) assigned parentheses as Meaning delimiter; 06196cc7:316 (2026-08-13) "full backpedaling" on () for simple strings but immediately reverses by discovering balance-based parsing. Net result: parentheses stay as default string delimiter, balance-based.

4. **.() for transformers -> :[/{ for transformer payloads**: 6b31eff3:156 (2026-08-04) ruled `.()` for transformers; a5587095:133 (2026-08-11) moved transformer payloads to `.[` and `.{` after the colon form; the `.(` combination for transformers is retired.

5. **Meaning type -> postponed -> parentheses vindicated**: a5587095:171 (2026-08-11) introduced the Meaning/structured string type with parentheses; 06196cc7:197 (2026-08-13) postponed it for a working syntax; 06196cc7:316 (2026-08-13) "my complex-string idea is actually right on the money" -- parentheses-as-markup vindicates the structured string.

## Sources

Transcripts searched (Claude Code, /home/li/.claude/projects/-home-li-primary/):
- 236af273-a771-43bc-bfa5-aa252d20fb3b.jsonl (2026-08-03, Designer)
- 6b31eff3-6477-4ee4-baed-cb491ebadd48.jsonl (2026-08-04, Designer)
- 5abf3be8-f31c-417f-982a-923eb83fb455.jsonl (2026-08-06, Designer)
- d63804f2-5a05-4e60-9448-94c95c3803d6.jsonl (2026-08-07, Designer)
- 012fbf07-6c4a-4f7a-9474-137aa967e582.jsonl (2026-08-11, Designer)
- a5587095-4368-42d3-9c38-6bc87fb7f436.jsonl (2026-08-11-12, Designer)
- 06196cc7-0e13-4c16-9beb-509da55a2bb3.jsonl (2026-08-13-14, Designer)
- 68512643-3229-449c-9152-9e2ff103dfbe.jsonl (2026-08-23-24, Distillation)
- 01a02a34 (2026-08-22, Codex realization, via rollout JSONL)
- 01a03d6e (2026-08-26, via rollout JSONL)
- All 99 Claude Code transcripts and 1530 Codex transcripts scanned programmatically.

Vision/psyche-raw files checked:
- Vision/datom.md
- flows/06196cc7/vision/archive-datomSyntax.md
- flows/a5587095/vision/archive-datomSyntax.md
- psyche-raw/Vision/archive-datomSyntax.md
- flows/a5587095/vision/colonFormTransformerSyntax.md
- psyche-raw/Vision/colonFormTransformerSyntax.md
- flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md
- flows/5abf3be8/vision/colonLegalInStringPosition.md
- psyche-raw/Vision/colonConfusion.md
- flows/a5587095/vision/structuredStringType.md
- psyche-raw/Vision/structuredStringType.md
- flows/a5587095/vision/protosIsTheSharedStyle.md
- flows/012fbf07/vision/archive-threeStacks.md
- flows/01a02a34/vision/archive-datum.md
- flows/01a03d6e/vision/dotosFiles.md
- psyche-raw/Vision/parserIsTheParser.md
- psyche-raw/Vision/observerFixtureBlessed.md
- flows/06196cc7/vision/traitsAsCapabilities.md
- flows/06196cc7/vision/encodedFormIsTheCode.md
