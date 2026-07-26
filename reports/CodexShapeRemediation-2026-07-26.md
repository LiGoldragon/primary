SHAPE RULINGS ADDENDUM — folds into the standing vertical-slice prompt.

First: read the full graded register at
/home/li/primary/reports/BadDataShapesRegister-2026-07-26.md
It carries file:line, typed replacements, and the tier sequencing this
addendum enacts. This addendum does not restate it.

NEW PSYCHE RULINGS — append to the design log per its convention
(each with the agent text it answered; append-only).

R3 — THE TYPED-RECORD RULING REACHES THE PROTOS KERNEL. Asked whether
Product(Vec<StructuralForm>) / PositionalSignature become typed
positions, accepting the content-hash/layout bump now while the
digests have zero consumers; recommended yes. Psyche: "if you think
it's a good idea, then yes." Ruled yes. One deliberate layout bump,
now, before slice 1 gives the hashes consumers.

R4 — ID RULING SCOPE. Presented three families with recommendations
(type-ids yes, wire contract IDs no, short codes yes). Psyche: "ok."
Ruled: ScopedEncodedTypeId / EncodedConstructorId become
language-variant-wrapped u16 like Identifier (Schema/Logos/Nomos
dimension, private fields); signal-frame ContractId stays as it is;
ShortCode gains the capsule-kind dimension (a schema capsule's code
and a nomos capsule's code become distinct types).

R5 — NAME PROJECTIONS ARE THE ORIGINAL DESIGN. Proposed "derived text
becomes a typed algebra over identifiers, evaluated only at
textualform time." Psyche: "I thought that's what I had designed."
Confirmed: this is his standing design; the implementation inverted
it by evaluating derivations early in nomos and storing the text.
Record the confirmation, not a new ruling. Sketch (the concrete
variant set is matter — refine on engineering merit, preserve the
principle that no spelling is evaluated before the textualform stage):

  NameProjection.[ Exact.Identifier
                   Cased.{ CaseForm Identifier }
                   Composed.Vector.Segment
                   Disambiguated.{ NameProjection Ordinal } ]
  Segment.[ Name.Identifier Projected.NameProjection ]
  CaseForm.[ Snake Screaming Pascal ]

Composition prefixes (e.g. the Signal in Signal<root><variant>) are
Identifiers in the logos standard nametree slice — no string anywhere
in the algebra. The projection evaluator lives on name-table's
dormant TextualProjection surface; per-language spelling data
(English ordinal words, case rules) is textualform data owned by
rust-logos, never nomos. Logos Expression gains NameText(NameProjection);
StringLiteral(String) remains legal only for genuinely opaque text
(current production uses: zero). Nomos constructs projections as pure
typed data — its name boundary (case derivation, format! composition,
the English ordinal speller) deletes rather than relocates.

SEQUENCING DIRECTIVES

1. ONE LAYOUT BUMP TRAIN, not several. Fold into the slice-0/slice-1
   structural-codec work, together: kernel typed positions (R3), the
   identity-shape fixes from register tier 3a (canonical character
   sets, ContentHash domain plumbing at the table boundary, legacy
   delimiter removed from the hashed pre-image, no zero-filled layout
   identity), and the R4 type-id retype. These all move identity;
   they land as one bump with fresh absolute-digest locks.

2. NAME PROJECTIONS phase with the slices: introduce the type in the
   slice-1 train (item names need only Exact); the full algebra
   (Cased, Composed, Disambiguated) lands with slice 2's deterministic
   field naming — disambiguation keyed on TYPE IDENTITY, never on
   derived spelling (this is the fix for the Vector<Topic> /
   Optional<Topic> / Topic grouping bug). Slice 2 still opens by
   presenting the concrete naming rule for ratification; the algebra
   is its vocabulary, not its answer.

3. TIER-1 STANDALONE FIXES, safe now, no identity movement: the
   fabricated-observation errors and missing-lexicon misreport in the
   engine core (register EC13, EC18); the schema-rust FreshnessCheck
   live bug (CE5); promoting the existing private newtypes into the
   ContractCrateBuild API (CE1). Small independent trains.

4. WIRE-LAYER SHAPES (WF1, WF2, and the generator-stamped G-series):
   do NOT regenerate contracts through schema-rust to chase shapes —
   that is investment in the doomed path. Encode them as requirements
   on the new engine's emission, and schedule the signal-frame trait
   fix (log_variant returning WireRoute) with the post-path wire
   regeneration phase.

5. SPIRIT WORKTREE SHAPES (SP-series, including the guardian config
   data-loss and the DatabaseMarker error-as-zero live bugs): deferred
   to the spirit repin phase; the register carries them so they are
   not relost.

6. All standing laws, the slice order, capsule discipline, and
   stop-the-line rules are unchanged. Open questions remain open:
   function-parameter and let-binding names; capsule container
   enum-vs-struct; micro-capsule shape; manifest self-generation;
   reify/reflect derivation. The plane-vocabulary question is
   deliberately deferred until slices reach daemon emission.
