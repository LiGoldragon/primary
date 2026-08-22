# Structured string type — "think of it as an annotated string"

## 2026-08-11 — the idea

> This would free patenthesis completly, and I have an idea for a
> revolutionary type; a structured string type - something that
> would revolutionize LLM performance by exposing the emphasis and
> other structural aspects which a plain string simply doesnt have.
> think of it as an annotated string

— psyche, 2026-08-11T18:53+02:00 (Designer session a5587095), typed,
during the Datom syntax round's parentheses fork. "This" is the
same-message Ethos revision: transformer payloads move to `.[` /
`.{`, freeing parentheses (colonFormTransformerSyntax.md); the
psyche had just ruled parentheses must not be unused in Datom
(datomSyntax.md). No delimiter, language assignment, or anatomy has
been ruled for the structured string yet.

## 2026-08-11 — one type, two variants; parentheses; research directed

> 1. I am considering it, yes. This would require a new type (in
> rust, later ethos-generated) which can be met with either a curly
> quotes or parenthesis (two variants, legacy and structured). The
> structured type would allow for an arbitrary depth, since it is a
> graph of sorts.

> 2. Research the field of representing meaning with structure. Do
> you understand what I mean by that?

> 3. shape is still up in the air, but () would be the delimiter

— psyche, 2026-08-11T19:17+02:00 (Designer session a5587095), typed,
answering the Designer's anatomy questions (1 assignment, 2 what
the structure carries, 3 shape, 4 relation to the plain string —
answered "see 1"). One string type (Rust now, Ethos-generated
later), two variants: legacy — curly quotes U+201C/U+201D — and
structured — parentheses, arbitrary depth, "a graph of sorts".
Shape open. What the structure carries awaits the directed research
into representing meaning with structure.

## 2026-08-11 — the Meaning delimiter; context-switching parse

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

— psyche, 2026-08-11T19:44+02:00 (Designer session a5587095), typed.
The structured string's parenthesis pair is named the Meaning
delimiter. Opening it makes the full delimiter and
structured-parsing spectrum available until the closing delimiter
restores the outer context. The context-switching parse is the
shared style of all dialects; its code belongs in protos
(protosIsTheSharedStyle.md).

## 2026-08-11 — the ambition

> I want the most advanced structured meaning system ever made

— psyche, 2026-08-11T19:44+02:00 (Designer session a5587095), typed,
answering the Designer's deciding question: overlapping annotations
or strict nesting. Designer reading, marked as inference: maximal
expressiveness is the bar — overlap and reentrancy are in scope;
shape design proceeds under this ambition, not under decode
simplicity.

## 2026-08-11 — annotations as enums through the tree

> what do you mean by self-describing tag? The way I see it right
> now is there would be enums which would be used throughout the
> tree, like Emphasis.{} or similar, but its still too early to tell

— psyche, 2026-08-11T19:53+02:00 (Designer session a5587095), typed,
challenging the Designer's "self-describing tags" framing. The
Meaning structure's annotations are typed enum variants used
throughout the tree — named heads like `Emphasis.{…}`, the same
pattern as the existing dotted variants (`None`, `Some.value`) —
not free-form tags. Early; not final.

## 2026-08-11 — Meaning lives in datom; seen by both languages

> Meaning will be seen in datom and ethos. ethos will depend on
> datom if only because of the need to intake data for signals, so
> it can go in datom

— psyche, 2026-08-11T22:04+02:00 (Designer session a5587095), typed,
answering the ownership question. The Meaning context is visible in
both languages and lives in datom; Ethos depends on Datom — at
minimum for signal data intake. Also logged in threeStacks.md; the
dependency edge is stack architecture.

## 2026-08-12 — a string expects a string; MeaningOrString, or Meaning with PlainText

> I dont understand. A string expects a string. we can have another
> type for MeaningOrString (or maybe Meaning is the type that can
> also expect a plain string, which can derive a simple structured
> meaning (PlainText?)) which implements ProtosShape (Which I think
> is misnamed - its more like MultiplePossibleTypesDefinedByShape
> which is obviously way too long - maybe you have a better
> suggestion). So that is another ProtosShape type field (I dont
> know why I zoomed in on the vector of them, theyre totally
> possible in a particular struct field too!)

— psyche, 2026-08-12T01:26+02:00 (Designer session a5587095), typed,
rejecting the Designer's carrier-vector unification: a String
position expects a string, nothing else. Where a field can be
either, that is its own type — MeaningOrString, or possibly Meaning
itself as the type that also accepts a plain string and derives a
simple structured meaning from it (PlainText). Such
shape-discriminated types can sit in any struct field, not only
special contexts. The trait concept is
multiple-possible-types-defined-by-shape; its name is open
(protosIsTheSharedStyle.md).

## 2026-08-14 — cross-reference: datom rulings 2026-08-13/14 govern string and Meaning progress

*(2026-08-14 annotation, consistency audit: this file has no entries after 2026-08-12; the governing downstream rulings for the structured string live in datomSyntax.md and must be read alongside this file. datomSyntax.md 2026-08-13 postpones the Meaning type in datom for a working syntax (both parenthesis and curly-quote land as plain String with a comment, under bead primary-xqb.8.5). datomSyntax.md 2026-08-14 rules parentheses as the default string delimiter with balance-based interiors — balanced pairs are plain content, the string closes at the final unbalanced ), unbalanced interior parentheses are escaped — and reverses the same-day float about dropping the Meaning-as-parenthesis idea ("right on the money"; also bead primary-xqb.8.5). The verb-smell flag on the name Meaning (encodedFormIsTheCode.md 2026-08-13) is also noted on bead primary-xqb.8.5.)*
