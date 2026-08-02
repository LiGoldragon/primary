# Stream Is the Nomos Object; Name Is Data — 2026-08-02

Ruling from the psyche vision session, correcting the manager's stream
candidate `Observer.Stream.{...}` (stream name in head position).

Agent text answered: the manager's reseated stream design — streams as
Nomos-object declarations in the types position, spelled name-first —
and the resolution-decides account of dotted declarations.

Psyche ruling [psyche-verbatim, condensed]: "the way you wrote this,
observer seems to me either a new type or a Nomos object. So otherwise
you have a very specialized syntax — in which case it's a very
specialized section. I think the problem is you keep falling back on
your training in mainstream programming languages, which is not really
written as data... If you have a stream, that's what it is. It's a
stream. That's a Nomos object. And then that object, perhaps at its
first position — or we can have, because Nomos should be powerful
enough to allow us, stream.observer.struct, and observer would be the
name of the stream... my question which surfaces now is how do we see
the query — the shape of the query to request to open a stream — and
what kind of response do we expect?... Do we prefer putting the name as
a second dotted prefix or just as one of the fields in the struct? I
think Nomos should be able to do either. Being able to have a special
way to handle the second or maybe even third dotted symbol after a
Nomos transformer has been called is something that I would like to
see. Go and see what that would look like on the Nomos side... what
kind of syntax to transform the stream object into logos. Let's go far
with the design so we don't end up implementing a bunch of crap that I
don't even like afterwards."

Seated:

- The manager's head-position naming (`Observer.Stream....`) is
  rejected as a mainstream-language habit — not written as data. **The
  Nomos object comes first**: `Stream.Observer.{...}`. The thing is a
  stream; the name is data belonging to the application.
- **Nomos must support both name placements**: the name as a dotted
  symbol after the transformer head (`Stream.Observer.{...}`) and the
  name as a payload field (`Stream.{Observer ...}`). The dotted-chain
  form — binding the second and possibly third dotted symbols after a
  transformer head as transformer parameters — is a wanted Nomos
  capability to be designed.
- The stream application's payload must answer: the shape of the
  open-query and the expected response (and the pushed event) —
  whether by reference to existing types or by definition inside the
  application is part of the commissioned design.
- Commission: a far-reaching design of the full stream vertical —
  authored Ethos surface, the Nomos transformer syntax including
  dotted-chain parameter binding, and the Logos emission — before any
  implementation. Delivered as
  `reports/NomosStreamDesign-2026-08-02.md`.
- This composes with the same-session reseating that streams are not a
  body section: universal roles earn positions; patterns are Nomos
  objects.

## Appended 2026-08-02: the talked-past diagnosis and the parsing method

Agent text answered: the manager's summary presenting
`SimpleGeneric.Sorted.{Ord Vector}` and `ScopeOf.DomainScope.Domain` as
"corrected spellings" under object-first.

Psyche ruling [psyche-verbatim]: "in my mind, SimpleGeneric and ScopOf
were nomos transformers. Im not saying they should be, but that is how
we talked past each other, and why you thought you understood when you
didnt. always think about parsing, then you wont miss details like
this. I always think about how those objects are parsed to and from
encodedform."

Seated:

- **Method directive**: syntax discussion is grounded in parsing —
  every proposed form must state how the reader classifies it at its
  known position, what resolves, what binds, and how the encoded form
  re-emits it. Presenting a spelling without its parse path is how
  agents and the psyche talk past each other.
- **Diagnosis**: the corpus mixed two parse models without anyone
  pinning either. Name-first (declaration-uniform: at a declaration
  position the first symbol is always the declared name, and the
  definition after the first dot classifies by resolution) and
  object-first (constructor-first: the form's kind is known after
  resolving the head, the name is data inside the application). The
  historical spellings `Sorted.SimpleGeneric.{...}` and
  `DomainScope.ScopeOf.Domain` were, in the psyche's mind, transformer
  applications all along; the manager treated the spelling as settled
  surface without stating the parse, and understanding was illusory.
- Whether SimpleGeneric and ScopeOf themselves are Nomos transformers
  is explicitly NOT ruled here ("Im not saying they should be").
- Open, sharpened: one parse model must win for applications at
  declaration positions — coexistence is parse-incoherent (the reader
  cannot know whether symbol one is a name or an object without a
  rule). The Stream ruling seats object-first for streams; whether it
  generalizes to every transformer application is for the psyche.
  Landed-code consequence if it does: Slice 3's ScopeOf recognition
  matches a name-first shape (a typed newtype application whose head
  equals the ScopeOf identity) and would flip to head-resolution.
