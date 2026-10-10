Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md.
## 2026-08-13 — Meaning postponed in datom; () or curly quotes both land as String for now

> we'll postpone the Meaning type in datom to get a working syntax
> asap. lets accept a () or the curly quotes for strings for now,
> with the actual shapedefined implementation just casting both into
> a string for now, with a comment to implement the Meaning type
> later (the super-string type we discussed before).

— psyche, 2026-08-13 (Designer session 06196cc7), typed. Interim
surface for a working syntax asap: the string slot accepts
parenthesis-delimited or curly-quote text, and its ShapeDefined
implementation selects plain String for both, with a code comment
pointing at the later Meaning type (structuredStringType.md). This
defers, not supersedes, the 2026-08-11T19:17 parentheses-as-
structured-string ruling; Meaning's shape and vocabulary stay open
under bead primary-xqb.8.5.

## 2026-08-14 — string blocks ignore interior delimiters until they close

> on the block pass: Im willing to increase the complexity a bit to
> allow some blocks, like strings, to allow other delimiters to be
> ignored until it closes, which would allow a string to contain [ { ( etc

— psyche, 2026-08-14 (Designer session 06196cc7), typed, accepting
the first-pass block segmentation with per-kind opacity: string
blocks suppress recognition of other delimiters until their own
closer; the scanner needs only each carrier's lexical close and
escape rules.

## 2026-08-14 — the dotted prefix of a delimiter is part of its type

> And the dotted prefix of a delimiter must be part of its type. it
> could be a universal type, and unprefixed blocks simply have no
> prefix. what do we want to call the prefix shape?

— psyche, 2026-08-14 (Designer session 06196cc7), typed. The `X.`
before a delimited block belongs to the block's type; a universal
prefix type is floated, with unprefixed blocks simply carrying
none. The prefix shape's name is open — a candidate batch was
requested of the Designer. Supersedes the agent coinage "head"
(the estate's ShapeProbe field): the psyche's word is prefix.

## 2026-08-14 — a string that doesn't need quotes must not be quoted

> A string that doesnt need quotes *must not* be quoted

— psyche, 2026-08-14 (Designer session 06196cc7), typed, on seeing
"Q3" delimited in the Designer's example set: canonical
textualization writes a string bare whenever the bare form can
carry it.

## 2026-08-14 — parentheses are the default string delimiter; Meaning-as-parenthesis floated for dropping

> I would prefer to default to parenthesis for string delimiters. I
> might drop the idea of using parenthesis for a specific Meaning
> type, and just use it for strings. full vertical length delimiters
> have a cognitive ease to them that quotes simply cannot even rival

— psyche, 2026-08-14 (Designer session 06196cc7), typed. When a
string needs delimiting, parenthesis is the default carrier; curly
quotes remain the legacy variant. Dropping the 2026-08-11T19:17
Meaning-as-parenthesis-type assignment is floated ("I might"), not
final — noted on bead primary-xqb.8.5.

## 2026-08-14 — bare {…} is a struct; X.(…) is a string-carrying variant

> I dont understand. we have clearly enunciated what those are. the
> first is a struct, the second is (now) a string-carrying variant.
> Why wasnt that obvious?

— psyche, 2026-08-14 (Designer session 06196cc7), typed, on the
estate's ShapeNotYetRuled refusals of BraceDelimited and
DotParenthesized: bare {…} is an unprefixed struct; X.(…) is a
variant carrying a string (under the interim parenthesis-string
ruling). The refusals are stale estate surface predating these
rulings; the realignment assigns both.

## 2026-08-14 — paren strings are balance-based; parentheses are markup inside text

> Ok now Im full backpedaling on the () for simple strings, since
> parenthesis are so common in strings, and curly brackets are not.
> But there is an interesting pattern here which is tha parentheses
> are already used in text as a way to *markup* the text; so my
> complex-string idea is actually right on the money. I would just
> let the block parser balance parentheses until it reaches the
> final unbalanced ). So im not backpedalling actually; go for
> balance-based, where an unbalanced parenthesis needs to be
> escaped.

— psyche, 2026-08-14 (Designer session 06196cc7), typed. Parenthesis
stays the default string delimiter, balance-based: interior
balanced pairs are plain content — and the seed of the
complex-string markup — the string closes at the final unbalanced
), and an unbalanced parenthesis inside is escaped. Supersedes the
Designer's first-unescaped-closer proposal; reverses the same-day
float about dropping the complex-string idea — parens-as-markup
vindicates it (noted on bead primary-xqb.8.5).

## 2026-08-14 — Head is the official term

> I like the Head terminology actually. lets make it official

> for the text block type? Head

— psyche, 2026-08-14 (Designer session 06196cc7), typed. The dotted
prefix of a block is officially its Head, and the universal type on
text blocks is named Head. Supersedes the coinage retirement in the
2026-08-14 dotted-prefix entry above; the estate's head field
stands.

## 2026-08-14 — variants always re-emit their head; special shapes depend

> is Note a variant? then yes. does it have a special shape? then
> it might. It depends.

> Like in ethos, when we are defining types, X.{} is a struct
> called X, and textualizing that type back will re-emit X.{} which
> must be understood in the right context if printed alone, or
> inserted in the right position, if the whole source is
> textualized

— psyche, 2026-08-14 (Designer session 06196cc7), typed, answering
whether Entry::Note always textualizes as Note.(…): a variant
always carries its head; a type with a special shape might omit it
— it depends. Textualizing re-emits the head; a fragment printed
alone must be understood in the right context, or inserted at the
right position when the whole source is textualized. The estate's
headless-when-shape-suffices emission is superseded for variants.

## 2026-08-14 — bare strings may carry load-bearing symbols

> If its a string, then it can use symbols which would be load
> bearing in other situations, just like delimiters in string
> blocks. no problem there. lets make the machinery fit for this,
> bullet proof not by lots of complex code, but by the right
> abstraction layers.

— psyche, 2026-08-14 (Designer session 06196cc7), typed, answering
the bare-symbol boundary question (dates, timestamps): where a
string is expected, symbols that are structural elsewhere are
content — exactly as delimiters inside string blocks. The
machinery is made fit for this by the right abstraction layers,
not by complex code.
