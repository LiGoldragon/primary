NEW PSYCHE RULING — SHORT IDENTIFIERS ARE DISPLAY PROJECTIONS

Append to the design log per its convention (with the agent text it
answered, dated, append-only). The agent text: "every capsule carries
a short identifier". The psyche's verbatim reply:

"no, it's a full content-addressed hash. the short identifiers is for
common display operations, which will use a method on the hash which
solves for the 4 or more chars shortened version that doesnt conflict
in the db"

This is later word and governs. It supersedes R4 clause 3 (kind-typed
stored short codes) and retires the stored-value model entirely.

THE MODEL

- Capsule identity is the full content-addressed hash (plus the
  ruled composed-nametree pin). That is what is stored, carried, and
  compared. Nothing else is identity.
- The short identifier is a DISPLAY OPERATION, not state: a method on
  the content hash that solves for the shortest rendering, minimum 4
  characters and growing as needed, that does not conflict with any
  other hash known to the resolver it is given. Git short hashes are
  the model: computed against the store, never stored, free to
  lengthen as the database grows.
- Signature shape (matter — refine on merit, preserve the model):
  a method on ContentHash taking a resolver/view of known hashes and
  returning the solved short text. The caller's resolver defines the
  conflict scope; no separate ruling on scope is needed.

WHAT THIS RETIRES

1. The standalone stored ShortCode value model in content-identity:
   the numeric type, the mint, the rkyv archive adapters, the archive
   compatibility locks, and today's kind-typed variants
   (SchemaShortCode/LogosShortCode/NomosShortCode + sealed trait).
   Display projections are never archived; delete the adapters and
   their locks rather than maintaining them. Zero consumers exist —
   retire, do not adapt.
2. protos' ShortIdentifier supertrait on Capsule as a self-contained
   getter. A conflict-free short form cannot be derived from the
   capsule alone. The Capsule contract keeps full hashes; short
   display arrives through the hash method with a resolver.
3. The pending course-correction item "adapt protos to the kind-typed
   short codes" — do not adapt; remove the dependency instead. This
   simplifies the bump train: protos drops ShortCode from the capsule
   contract rather than chasing the renamed trait.

KIND SAFETY — RULED

Psyche, on whether a schema capsule's short code and a nomos
capsule's short code may share a Rust type: "they should be a
different type for sure."

So the display projection's RESULT is kind-typed. The clean shape:
the method inherits the hash's existing domain tag —
ContentHash<D>::short(resolver) returns ShortDisplay<D> (name is
matter). Schema, logos, and nomos short forms are distinct types by
construction, with one generic definition: no hand-written type per
kind, no sealed trait, no runtime kind checks. This replaces, not
revives, today's SchemaShortCode/LogosShortCode/NomosShortCode
family — those were stored-value types with mints and archives; the
ruled thing is a kind-tagged display value that is computed, shown,
and dropped.

SEQUENCING

Fold the retirement into the same bump train as the R3/R4 kernel work
(one landing, one set of fresh locks). The hash short-display method
itself is small and unblocking: it needs only ContentHash and a
resolver abstraction; land it with the train or immediately after.
All other standing directives unchanged.
