# Protos is the style all our dialects share

## 2026-08-11 — the definition; context-switching parse; the protos engine

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

— psyche, 2026-08-11T19:44+02:00 (Designer session a5587095), typed,
during the structured-string design (structuredStringType.md — the
Meaning delimiter). Rulings carried: (a) protos names the style
shared by all dialects; (b) the context-switching parse — an opened
delimiter makes the full structured-parsing spectrum available
until its closing delimiter restores the outer context — is how all
the languages parse and why design stays free; (c) that parse
machinery is the code shareable between all parsers and belongs in
protos; (d) the final fully-decomposed engine with three daemons is
the protos engine; (e) Datom sits beside the engine, carrying only
pure, typed data.

*(2026-08-14 annotation: ruling (e)'s "beside" is clarified by the
2026-08-14 entry below — Datom is a protos dialect, beside only the
rust-generation engine, not beside protos.)*

## 2026-08-11 — there is always a parsing context; it changes, never suspends; always use trait

> no, there is always a parsing context. it doesnt suspend, it
> *changes*, but the underlying mechanism is always the same; Now,
> we are parsing in context X and can therefore expect A, B or C
> shapes of things, and Z would end that context, but meeting A
> would switch to the context which A entails. That has been the
> ruling principle of NOTA (datoms's ancestor) from day one. I want
> to extend it now to say it should always use trait.

— psyche, 2026-08-11T19:53+02:00 (Designer session a5587095), typed,
correcting the Designer's "the outer positional decode suspends"
framing. One mechanism always: a context defines the shapes it can
expect and what ends it; meeting a shape switches to the context
that shape entails. NOTA's ruling principle from day one, now
extended: it should always use trait. The companion broad statement
that all Rust method calls live in traits is in
rustComponentArchitecture.md.

## 2026-08-11 — two-way structural transcoding; flesh out before Intent; the design pattern

*(2026-08-14 annotation, consistency audit: "two-way structural transcoding" in this agent-authored heading is dead vocabulary — code/encoded was dropped 2026-08-13; the psyche's speech in this entry is preserved verbatim, and the two-way walk concept stands under the real/signal/textual forms frame per encodedFormIsTheCode.md 2026-08-13–14.)*

> Intent would be quite general, about the way the parsing is
> approached. Lets flesh it out in detail with examples then we can
> make it intent. Intent is basically very clear vision which is
> unlikely to change. Dont forget the parsing is also two-ways. I
> feel like we need to really flesh out this two-way structural
> transcoding, through clear explanation and with a trait-library
> first approach, in protos repo (which can be re-considered from
> whatever it is doing now) We need to work with visuals, examples,
> and traits with main types. that must become our design pattern.

— psyche, 2026-08-11T22:04+02:00 (Designer session a5587095), typed,
answering the Designer's Intent-scope question. The Intent will be
general — the way parsing is approached — and lands only after a
detailed flesh-out with examples; Intent is very clear vision
unlikely to change. The parse is two-way: structural transcoding.
The flesh-out is trait-library-first and belongs in the protos
repo, whose current duty may be reconsidered. Design pattern ruled:
visuals, examples, and traits with main types. Flesh-out draft:
design/ProtosEngine/twoWayStructuralTranscoding-2026-08-11.md.

## 2026-08-12 — the expects vector: ProtosShapes; structure can dictate the outer type

> the more complex trait will be a vector of ProtosShape's (welcome
> to propose other names), when the structure dictates the outer
> type, for example in ethos when X.{ means a struct, and Y.[ means
> an enum, and Z:Transform.[/{ means different kinds of transformers

— psyche, 2026-08-12T00:59+02:00 (Designer session a5587095), typed,
after reading the transcoding flesh-out draft. The mechanism
trait's expectation is a vector of ProtosShapes (name open to
proposals): the case it serves is positions where the structure met
in text dictates the outer type — in Ethos, `X.{` is a struct,
`Y.[` is an enum, `Z:Transform.[` / `Z:Transform.{` are different
kinds of transformers. Answers the flesh-out draft's open fork 1.

## 2026-08-12 — ProtosShape is a trait types implement; the match on standard shapes; types carry their own context

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

— psyche, 2026-08-12T01:26+02:00 (Designer session a5587095), typed,
reading the Designer's Intent draft and trait sketches. The design
carried: a fixed universal shape vocabulary (the standard
ProtosShapes — "always the same", e.g. CurlyQuoteDelimited,
ParenthesisDelimited, flat variants preferred if nested data
overcomplicates); a trait (name open — ProtosShaped? ShapeDefined?)
implemented by shape-discriminated types as a match from standard
shapes to the type's own variants; each yielded variant's type has
its own parsing context implementation — the type met implements
its own context. NewString{String, Meaning} is a throwaway
example, explicitly not canonical. Also ruled in the same message:
Intent language must describe positively at high altitude —
mechanism ("uses trait") and placement ("lives in protos") are not
Intent-level.

*(2026-08-14 annotation, consistency audit: naming fork closed — ShapeDefined confirmed 2026-08-14 in traitsAsCapabilities.md ("ShapeDefined is good"); ProtosShaped is dropped.)*

## 2026-08-12 — recursion keeps the parent's position; logic planes; a child context takes the shapes' meaning

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

— psyche, 2026-08-12T21:23+02:00 (Designer session a5587095),
typed, reviewing the round-2 sketches. Three teachings: (a) the
walk is a stack — each frame keeps the parent context's position,
and popping resumes at the following position; (b) ShapeDefined
discriminates only — it yields the type, and the type implements
its own parsing context; big implementations signal a missing
logic plane — everything simple individually, the complexity in
the totality (candidate Intent line); (c) while a child context is
active, only its shapes carry meaning — the parent's end shape has
none until the child completes. Also scoped in the same message:
the Intent's subject is *Protos parsing*, not parsing in general.

## 2026-08-13 — the Protos parsing Intent is graduated

> the intent is good

— psyche, 2026-08-13T00:19+02:00 (Designer session a5587095),
typed, approving the Designer's v3 draft. Landed verbatim as
psyche/Intent/protosParsing.md — the first Intent graduated from
this topic.

## 2026-08-13 — recursion must carry shape-determined types at every level

> your recursive parsing wasnt complex enough. we need to consider
> multiple levels, each with one or more shape-determined type

— psyche, 2026-08-13T00:25+02:00 (Designer session a5587095),
typed, on the round-3 walk example and the fixture requirement:
nesting containers alone is insufficient — the state machine must
be considered (and tested) with discrimination happening at every
depth, one or more shape-determined types per level, including
shape-determined types reached from inside shape-determined types.

## 2026-08-13 — no traits is no good

> I only looked at the code. I need to see the traits. No traits
> is no good

— psyche, 2026-08-13T00:29+02:00 (Designer session a5587095),
typed, on the round-4 fixture, which showed data types without
their trait impls. Reinforces the ruled design pattern: an example
is not complete until the traits with main types are visible — the
data types alone are not the design.

## 2026-08-14 — datom is a protos dialect, not part of the rust-generation engine

> because datom doesnt take part in the multi pass engine which
> ethos->nomos->logos->rust is slated to become. but youre right;
> beside sounds like its not a protos dialect. it *is* a protos
> dialect, but not part of the future ethos/nomos/logos
> rust-generation engine

— psyche, 2026-08-14T10:09+02:00 (Designer session ba906ae2),
typed, answering the Designer's beside-vs-on-top question about
ruling (e) of the 2026-08-11T19:44 entry above. Clarification
carried: "beside" meant outside the multi-pass engine
(ethos→nomos→logos→rust), not outside protos — Datom is a protos
dialect sharing the protos style, excluded only from the future
rust-generation engine.

## 2026-08-18 — define the block: start with the text source code; every logical aspect a type; ontology of source code

Design session `2b34fafa`, typed (captured 2026-08-18), after ruling
that the text realizes and the real textualizes, when asked what
textual type does the realizing below the top level:

> "we need to define the block. start with the text source code. turn
> every logical aspect into a type. ontology of source code"
