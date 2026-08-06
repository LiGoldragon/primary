# Textual-Form Metadata Store; Pipe-Text Staleness — 2026-08-07

Rulings from the psyche during the vision-reacquisition session (three-wave
report), answering two clarification items the report raised.

## Ruling: no pipes anywhere; the dotos pipe-text claim is stale

Agent text answered (report clarification note):

> The dotos repository's architecture document still claims "pipe-text is
> kept — the sole surviving piped form" for quotation safety, while the
> 08-04 ruling drops all piped delimiters family-wide and seats curly
> quotes. Either Dotos holds a special serialization-layer exception or
> the document is stale.

Psyche: "thats stale, there are no more pipes."

The curly-quote string ruling (llmTokenOptimizationRulings-2026-08-04)
governs family-wide with no Dotos exception. The dotos ARCHITECTURE
passage claiming pipe-text survival is stale documentation.

## Ruling: editing never mints a fresh EncodedName; the name-table claim is disavowed

Agent text answered (report clarification note):

> The name-table component (08-06) states that changing authored text is
> not an identity-preserving rename — the next seal allocates a fresh
> encodedID and orphans the old one. This sits in tension with
> EncodedName stability across edits and with "encoded-name persistence
> makes renames migration-free" (databaseEvolutionEngine · 08-02).

Psyche: that claim is wrong — "hardcore hallucination", never a psyche
ruling. Changing authored text does not create a new EncodedName. If the
EncodedName changed, everything referring to the subject would have to be
rewritten — "that would be fucking insanity." EncodedName stability
across edits stands absolutely.

(Terminology note: the ruled term is EncodedName; the name-table
document's "encodedID" is not vocabulary — consistent with
traitVocabularyRulings-2026-08-07.)

## Ruling: the name table is replaced by the textual-form metadata store

Psyche: the name-table component is superseded. Its replacement — name
not yet chosen; the psyche gestured at "the textual form data" — holds
all textual-form metadata associated with an object:

1. The TextualName.
2. The re-emission placement: the module, or series of submodules
   (recursive submodules, as in Rust), that allows the code to be
   re-emitted into files. Emitting everything into a single file would
   not work without prefixing, because textual names may conflict;
   placement is what disambiguates.

This extends the standing textual-form-metadata ruling
(visionReacquisitionRulings-2026-08-05: one record per object, keyed to
the encoded identity, carrying TextualName and module/file placement) and
names the component consequence: the name table dies into this store.

## Ruling (lean, pushback invited): no module concept in the encoded form

Psyche: the encoded form does not need the module concept; modules exist
only in textual-form metadata. Explicitly open to pushback.

Management pushback offered in session: agreed for reference resolution
(encoded references are absolute EncodedNames, so no namespacing is
needed), with one boundary to check — if any semantics depend on
grouping (visibility, a capsule's exported surface, coherence rules),
that grouping needs an encoded home; the capsule and the interface file
kinds may already cover it. Not yet ruled either way.
