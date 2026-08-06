# Trait Vocabulary Rulings — 2026-08-07

Continuation of the 2026-08-06 session
(`redesignAuditRulings-2026-08-06.md`): the psyche's trait-design
conversation following the body-is-rkyv ruling.

## Correction: textual name, not "name"

Agent text answered: "the body must not contain its own name."

Psyche [psyche-verbatim]: "you cant just say 'name' - that isnt
specific enough. you mean textualname."

Seated: three-layer precision is mandatory in design speech —
TrueName, EncodedName, TextualName. The hashed body excludes its own
TextualName, which lives in textual-form metadata keyed by
EncodedName. Alignment note: earlier entries call the third layer the
"visible name"; the psyche's working term is TextualName — treat
TextualName as the canonical spelling going forward; visible-name
prose in older entries denotes the same concept.

## Ruling: one vocabulary — the trait carries the ruled concept's name

Psyche [psyche-verbatim]: "then TrueName is the trait. right, lets use
the same vocabulary" — and, on EncodedName over "encodedid": "I like
EncodedName better. thank you."

Seated: "fingerprint" dies as a synonym; the identity capability trait
is named by the true-name concept (exact grammatical form pending
below). EncodedName stands; "encodedid" does not enter the vocabulary.

## Ruling: defaults whenever possible; sub-traits make them possible

Psyche [psyche-verbatim]: "The default implementation is good if its
possible. I just dont always know if it is. But if enough sub-traits
are implemented, then default implementation is just a bunch of trait
method calls, so possible. In fact this kind of brings the answer to
why we want traits everywhere; one of the reasons is to enable default
implementations."

Seated: a trait method carries a default implementation whenever that
default is expressible entirely through the trait's requirements — the
methods of its required sub-traits. Designing rich-enough requirement
chains is what makes defaults possible. Enabling default
implementations is recorded as one of the reasons for the
traits-everywhere doctrine.

## Open: grammatical form of the true-name trait

Psyche candidates: TrueNameable ("did I spell that right?" — yes),
NameTruly, bare TrueName. Manager analysis: bare TrueName collides
with the value type — the association table `{EncodedName TrueName}`
stores TrueName values, and one name cannot serve both the capability
and the value; NameTruly places the concept adverbially; TrueNameable
is correctly spelled but heavy. Manager recommendation, following the
ruled Ordered pattern (state-adjective, not -able): trait `TrueNamed`,
method `true_name()`, value type `TrueName`. Awaiting the psyche's
pick.
