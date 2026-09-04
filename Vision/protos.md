# Protos

## What Protos is

Protos is the name for the style all the dialects share. The
context-switching parse, the delimiters, the heads, the recursive
structure — this is the code that can be shared between all parsers
and belongs in protos. Datom is a protos dialect, carrying only
pure typed data; it does not take part in the multi-pass
rust-generation engine that ethos, nomos and logos are slated to
become, but it shares the protos style. The final fully-decomposed
engine with three daemons is the protos engine.

## What Protos knows

Protos is only about structure. It has nothing to do with struct and
vector, and it only understands form: the syntactic structure. It
would not know what anything is. A head in protos is just a head —
anatomy, not interpretation. Pure anatomy is only structural
recognition of delineations, nothing more. Protos examples show the
textual structure — the delimiters, the head, the capitalization, the
recursive structure — universally, at a very high level,
non-dialect-specific.

## Direction

Text arrives as a potential value and leaves as a value. Incorporate
reads the textual form into the corporal form and may fault: the
text is potential until it matches its anatomy. Textualize writes
the corporal form into the textual form and cannot fault: a corporal
value is already whole. Spans are found on the way in and computed
on the way out. Each direction is several passes.

## Structure

Structure is the word for every unit of the text; its type is
Protoform: headed, enclosed, opaque, or bare.

A headed structure is a head, a separator and a body. The separators
are period, exclamation and colon. The head is a symbol. The body is
another structure. Heads may be daisy-chained: different separators
too.

An enclosed structure stands between its delimiters. Six delimiter
pairs in all: four structural — braces, brackets, guillemets, angle
brackets — and two opaque — curly quotes, where every glyph inside
is content, and parentheses, read by balance. Angle brackets are a
real protos delimiter. A bare structure has no delimiters.

## Delineation

Delineation is protos. A delineation is the structural survey of a
text: here we have a headed structure, there an enclosed one — no
detail as to what these things mean in terms of the dialect.
Protosize on text is the delineation. A brace-enclosed structure's
arity is anatomical; a bracket-enclosed structure's arity is not.

## Layers

Text, Protoform, Concept, Corporal — four layers. Potential and
actualize go universally, layer to layer: a potential Protoform
actualized yields a Protoform; a potential corporal value actualized
yields the corporal value.

A capability is named by the layer it goes to, and for the middle
layers both the layer above and the layer below bear it, since we go
both ways: text and concept are protosizable; protoform and corporal
are conceivable. Textualize goes to the text layer; incorporate goes
to the corporal layer. Calling incorporate on text daisy-chains:
protosize, then conceive, then incorporate the concept.

| capability | goes to | borne by |
|---|---|---|
| textualize (Textualizable) | Text | Protoform, and the layers below through the chain |
| protosize (Protosizable) | Protoform | Text, where it is the delineation, and Concept |
| conceive (Conceivable) | Concept | Protoform and Corporal |
| incorporate | Corporal | Concept, and the layers above through the chain |

Sized is the bound borne by every corporal type.

## Multi-pass

Multiple passes are wanted over a single pass, because a single pass
creates corner-cutting bad design. The multiple steps create a mental
model of the machinery, which enforces a correctness in the code that
is millions of times more beneficial than the cost of doing these
multiple passes. Extents are not intrinsic to objects; when we
textualize, these can be computed.

## Canonical print

It is canonical, and it is considered good style, to leave a space
between the delimiters and the content, except for the curly quotes
where a space would be load-bearing. Space the delimiters and the
inner content.
