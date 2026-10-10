# Rust Tuple Violations Register — nomos train, 2026-07-30

On 2026-07-30 the psyche restored the standing Rust rule: tuples are
forbidden — ad-hoc tuple types and tuple structs of two or more fields.
The single exception is the newtype pattern (one-field wrapping struct),
which is not considered a tuple. Rust structs use named fields; the
positional-fields law belongs to the protos data model, not Rust source.
Recorded in standards commit bc61e427ab5e (good-rust-practices.md) and
design log design/Nomos/rustTuplesForbiddenLawScope-2026-07-30.md
(commit 71906cf9f566).

A same-day scan of the nomos train's repos found the violations below.
They are almost entirely train-era (2026-07-29/07-30) code. This report
is a pickup surface for the train to execute the cleanup — not itself
the cleanup.

## Multi-field tuple structs (27)

### core-nomos (12)

- src/slice_one.rs:160 `SliceOneVocabularyReferenceMapping` (2 fields)
- src/textual.rs:372 `LoadedNomosPopulation` (2)
- src/manifest.rs:59 `NomosManifestFile` (3)
- src/manifest.rs:67 `NomosFileManifest` (2)
- src/manifest.rs:70 `PlannedNomosPopulation` (5)
- src/manifest.rs:347 `ModulePlan` (2)
- src/sealed.rs:70 `NameTreeProjectionEntry` (2)
- src/sealed.rs:85 `SealedNomosCapsuleArchive` (2)
- src/sealed.rs:170 `NameTreeProjectionPayload` (3)
- src/sealed.rs:177 `NameTreeProjectionArchive` (2)
- src/authored.rs:148 `AuthoredInputParameter` (3)
- src/authored.rs:211 `AuthoredTransformerDeclaration` (6)

### core-ethos (8, all src/whole.rs)

- :249 `WholeEthosWrappedField` (2)
- :179 `WholeEthosNewtype` (4 — name misleading, it is a 4-tuple, not a newtype)
- :284 `WholeEthosTypeApplication` (2)
- :308 `WholeEthosEnumeration` (4)
- :349 `WholeEthosVariant` (3)
- :1021 `WholeEthosBuiltinPriors` (2)
- :1256 `DecodedSixSlotEthos` (2)
- :1277 `SixSlotSourceBounds` (6)

### core-logos (4, all src/whole.rs)

- :190 `WholeLogosNewtype` (4, same misleading-name pattern)
- :245 `WholeLogosTypeApplication` (2)
- :269 `WholeLogosEnumeration` (3)
- :303 `WholeLogosVariant` (2)

### nomos-engine (3, all tests/lifecycle.rs)

- :38 `ForgedWholeEthosNewtype` (4)
- :46 `ForgedWholeEthosEnumeration` (4)
- :54 `ForgedWholeEthosVariant` (3)

### Zero found

name-table, structural-codec, raw-discovery, sema-translator,
signal-sema-translator.

## Ad-hoc tuple returns (~15 src-level, plus test helpers)

- core-nomos/src/textual.rs:413 `target()` -> `(Vec<Name>, Name)`
- core-nomos/src/textual.rs:2200 `bound_key()` -> `(usize, usize)`
- core-nomos/src/native.rs:69 `into_parts()` -> `(NativeEvaluatedLogos, NameTree)`
- core-nomos/src/native.rs:157 `into_parts()` -> `(NativeLogosPopulation<NameTree>, WholeLogos)`
- core-nomos/src/native.rs:407,422 -> `Result<(NativeEvaluatedValue, WholeLogosItem), _>`
- core-ethos/src/whole.rs:1270 `into_parts()` -> `(WholeEthos, SixSlotSourceBounds)`
- structural-codec/src/disjoint.rs:26 -> `(StableRoleId, BTreeMap<StableRoleId, SharedDescriptor<Root>>)`
- structural-codec/src/evaluator.rs:1499 -> `Result<(Atom, SourceBound), DecodeError<Root>>`
- name-table/src/state.rs:81 `allocate()` -> `Option<(LocalEncodedId, Self)>`
- sema-translator/src/store.rs:559 `required_authority()` -> `(AuthorityRole, AuthorityCapability)`
- raw-discovery src/profile.rs:267,687, src/block.rs:105,364,383,
  src/boundary.rs:823,881,977 — `Option<(&T, &T)>` style. block.rs is
  pre-train (dated 2026-07-24), the rest is train-era.

Plus test-only helpers in core-nomos/tests/{textual_nomos.rs,pipeline.rs},
core-ethos/tests/{streaming_relation.rs,whole_six_slot.rs},
name-table/tests/archive.rs, sema-translator/tests/{authority.rs,process.rs}.

## Tuple-typed fields/collections (~11 sites)

- core-nomos/src/template_language.rs:617,624 `Vec<(StableRoleId, SharedDescriptor<Root>)>`
- core-nomos/src/native.rs:788 `fields: Vec<(StableRoleId, NativeTermShape)>`
- core-nomos/src/textual.rs:182 `Vec<(VocabularyEncodedId, String)>` param
- core-nomos/src/textual.rs:2206-2207 `BTreeMap<(usize, usize), (Name, VocabularyEncodedId)>` (x2)
- core-nomos/src/textual.rs:2421 `Vec<(u16, NomosRule)>`
- core-ethos/src/whole.rs:1134 `rules: Vec<(u16, WholeEthosRule)>`
- core-logos/src/language.rs:748 `rules: Vec<(u16, LogosRule)>`
- name-table/src/archive.rs:70 `receipts: Vec<(OperationKey, OperationReceipt<Root>)>`
- test files: core-nomos/tests/textual_nomos.rs:419-423,
  core-ethos/tests/whole_six_slot.rs:73-74,
  structural-codec/tests/{disjointness.rs:62, downstream_authoring.rs:616-617}

## Newtypes (allowed, listed for count only)

50 single-field tuple structs across the repos — compliant, not itemized here.

## Remediation split

**(a) Mechanical, low risk.** Collection-of-tuples sites (swap `(K, V)`
for a small named struct), `into_parts()`-style tuple returns (return a
named struct instead), test-fixture maps. These are local, single-call-site
or few-call-site changes with no cross-cutting consumption pattern.
Covers the "Ad-hoc tuple returns" and "Tuple-typed fields/collections"
sections above in full.

**(b) Structural, correctness-sensitive.** The declaration-model tuple
structs in core-ethos/src/whole.rs, core-logos/src/whole.rs, and
core-nomos/{manifest,sealed,authored,textual,slice_one}.rs. These are
consumed via positional `.0`/`.1` access and `Self(a, b, c)` construction
throughout their respective crates; converting to named fields touches
every constructor and accessor and needs the train's careful sequencing,
not a sweep.

Flag the misleading `*Newtype` names — `WholeEthosNewtype`,
`WholeLogosNewtype`, `ForgedWholeEthosNewtype` — for rename or
restructure; each is a 4-field tuple struct, not a newtype under the
restored rule, and the name actively misleads.

Note: rkyv-archived shapes among these declaration-model structs may
have archive-layout implications. The train must check named-field vs.
tuple-struct layout under rkyv before restructuring any archived type,
so a restructure does not silently change on-disk/wire archive layout.

## Sequencing note

1. Archive-compat check first — confirm rkyv named-field vs. tuple-struct
   layout behavior for the archived declaration-model types before
   touching any of them.
2. Mechanical sweep second — the (a) list above, crate by crate.
3. whole.rs declaration-model refactor as its own reviewed slice —
   core-ethos/src/whole.rs and core-logos/src/whole.rs (plus the
   core-nomos declaration-model files), sequenced and reviewed
   separately from the mechanical sweep, given the positional-access
   blast radius.
