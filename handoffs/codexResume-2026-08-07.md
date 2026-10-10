# Codex resume dispatch — 2026-08-07 evening

Execute the standing dispatch: `handoffs/codexStartup-2026-08-07.md`.
Nothing there is revoked; the amendments below overlay it.

The leftovers of the earlier unauthorized run were already reverted;
both repositories reported clean working copies. Verify cleanliness
quickly; do not redo the cleanup.

## Rulings since the startup document was written

All logged verbatim with capture timestamps in the flat `psyche/Vision/` corpus.
Binding on your work:

1. The stream position is "a section inside the object", and
   "Yes, the initiation and termination live in the input."
   (`psyche/Vision/streamSection.md`)
2. Interface root objects branch as enumerators: "the root input
   objects and perhaps even a lot of the root output objects should be
   enumerators because if you're trying to create a language, an input
   and output language, you want to create like branches."
   (`psyche/Vision/interfaceRootEnumerators.md`)
3. "is it a newtype around another newtype? Looks really confusing to
   me." — "I don't like it. I don't like the single field struct."
   (`psyche/Vision/newtypeWrappingAndSingleFieldStructs.md`)
4. "I would rather not create confusion with :"
   (`psyche/Vision/colonConfusion.md`)

## Open questions — do NOT decide these; leave current forms in place

- Import separator: the psyche asked "So on the import paths; what if
  we use / ? signal/domain.Observer ?" — `/` is verified unclaimed in
  the delimiter rulings, but colon-in-imports is itself the 2026-08-04
  ruling ("qualification separator in import space"); superseding it
  is the psyche's call. Do not change import spelling.
- Whether a stream-section entry still carries a `Stream` transformer
  head: the psyche asked "and if we have a position dedicated to
  streams, why do we need :Stream ?" Pending the Designer's
  observer-interface proposal, not yet blessed.
- Interface version form: the psyche dislikes `Interface.{1 0 0}`;
  production `spirit-ethos/interface.ethos` uses `Interface.1`.
  Unruled.

## Consequences for your draft observer fixture

The draft (`Interface.{1 0 0}` / `Submit.Request` / `Rejected.{String}`
/ `Observer:Stream. ...`) was reviewed by the psyche and does not
survive: `Submit.Request` over `Request.String` is a newtype around a
newtype; `Rejected.{String}` is a single-field struct; `Submit`,
`Request`, `Response`, `Rejected` are the generic-categorical names the
naming-specificity ruling forbids; and the open questions above touch
its import line, version, and stream entry. Do not land it. Hold all
observer-fixture work until the Designer's counter-proposal is blessed
by the psyche.

## What you can proceed on now

The rest of the slice stands as dispatched in the startup document:

- hqu.26 — the sealed `AdmittedToCoreEthosRawConstruction` landing,
  under its approved conditions (raw constructors die in the same
  landing; site marked `psyche-grasp: slightly-reviewed`; hqu.26.1).
- hqu.33 core — stream-family deletion completion and the colon parser
  for named transformers (`Name:TransformerName.( ... )`), which stands
  ruled; hqu.33.1 re-spell sweep after it lands.
