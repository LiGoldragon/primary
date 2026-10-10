# Same-Form Meaning and File-Kind Law — 2026-08-01

Rulings answering the dependency-ordered psyche review agenda in
`reports/protosVisionReacquisition/2-Research-psyche-vision-open-questions-and-proposals.md`
(section 18). The psyche explicitly confirmed which report he is answering.

## Ruling 1: "same textual/encoded form" means the common-mechanism reading

Agent text answered (codex report, review question 1): the phrase "Nomos must
have the same textual/encoded form as the other two" admits at least three
readings — common machinery, structural isomorphism, or literal
representation equality — and line 178 of the source session does not choose
among them.

Psyche ruling [psyche-verbatim]: "In the context I was saying that Nomos
needs to, like Logos and Ethos, it needs to round trip and use the same
machinery for the round trip between textual and encoded form like the other
two."

Seated meaning: the **common-mechanism reading** is ruled. Nomos round-trips
textual form to and from encoded form through the same shared machinery
(nametree + structuretree) as Ethos and Logos. Structural isomorphism and
literal representation equality are not implied; the ruling is about shared
round-trip machinery, not shared grammar or shared archive layout.

## Ruling 2: file kinds differ only by root type; one shared parsing machinery

Agent text answered (codex report, review question 2): which exact Ethos
roots and recursive form tables exist — program kinds, root selectors,
position order/cardinality/delimiters.

Psyche statement [psyche-verbatim, condensed]: "when I first started Schema,
the ancestor, it was a very specialized use... there was this input and
output because I was defining an interface. So we don't necessarily need to
think about it that way... we can just be adaptable and support different
kinds of files and see which ones are more useful, which ones agents seem to
prefer. And they're basically just a few different types, right? Which is the
only difference there should be. All of the parsing logic — if there's a
bunch of code written to parse each one of them differently, then the
implementation failed. Because it should just be, okay, here's the type we
expect here, and then this just gets passed on to the same exact machinery
that all the other different file types would use depending on what is
expected in each position. So the different types of files shouldn't need a
whole bunch of code. It should just be like defining a new type and then
maybe like a simple trait implementation or something. That's it."

Seated meaning:

- Multiple Ethos file/program kinds are supported; the set is adaptive, to be
  grown by observed usefulness and agent preference, not fixed up front.
- The historical Input/Output roles are explained as artifacts of Schema's
  original specialized interface-definition use; they are not universal root
  requirements.
- **Law**: file kinds differ ONLY in their root type. Every kind is parsed by
  the same shared expected-type-at-position machinery. Adding a kind costs a
  new root type definition plus at most a simple trait implementation.
- **Failure criterion** [psyche-ruled]: per-file-kind parsing code — a body
  of code differentiating how each kind is parsed — means the implementation
  failed.

## Not settled here

The exact root types, their positions, delimiters, cardinalities, and the
recursive form tables (the rest of review question 2) remain open; the psyche
asked the manager to enumerate candidate item kinds of programming languages
viewed structurally as input to that discussion.
