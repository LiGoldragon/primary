# Schema document kinds and the signal-contract boundary

**Status:** source-backed design investigation. This report makes no source change and treats proposed syntax and records as proposals, not accepted language rulings.

## Purpose

The next-generation NOTA train exposed a real boundary: the current `schema-language` branch deliberately removed legacy stream and family constructs, while `signal-spirit` still relies on their semantic information to generate its streaming contract and render Help. The right response is not a compatibility parser or a seventh optional block in the general schema document. It is an explicit, versioned document-kind system.

This report specifies the smallest coherent system that lets the text reader learn a document kind without guessing from body content, keeps Core/sema stringless, and gives signal streaming and storage declarations the typed homes their consumers require.

## Reliable governing constraints

The following are the applicable settled or explicit constraints carried into this design:

- Core/sema is the typed rkyv substance; text is a bridge and projection.
- Every Core value is stringless and resolves human names through its corresponding NameTable.
- Core identity is domain-separated and layout-version-tagged over canonical stringless Core bytes; NameTables are excluded, so renames do not move Core identity.
- The expected type controls interpretation. Raw parsing discovers structure and does not classify it into domain meaning.
- Positional forms, exact delimiters, per-kind blocks, one namespace per loaded whole, no aliases, and capitalization as a structural expectation remain the language discipline.
- Textual format evolution must not move Core identity.
- `schema-language/ARCHITECTURE.md` already treats file/document kind as the initial expected-type boundary and distinguishes the general schema document from a `sema.schema` storage-declaration kind.

The evidence below also establishes a narrower fact: retiring generic `Stream` and `Family` heads was intentional in current `schema-language`; restoring them to the generic type schema would contradict that landed construct partition.

## Source inventory and measured models

### Legacy four-root schema

The legacy `schema` repository represents a module as four authored top-level positions:

```text
imports brace
input root enum
output root enum
namespace brace
```

The namespace was a mixed container. It held ordinary type declarations as well as metadata-shaped declarations. In `repos/schema/src/source.rs`, `SourceDeclarationValue` has `Stream(SourceStreamBody)` and `Family(SourceFamilyBody)` variants. In `repos/schema/src/schema.rs`, the lowered `TrueSchema` holds ordinary namespace declarations plus `streams: Vec<StreamDeclaration>` and `families: Vec<FamilyDeclaration>`.

A legacy stream is not a Rust data type. It has a name and four type references:

```text
StreamDeclaration {
  name,
  token,
  opened,
  event,
  close,
}
```

A legacy family is not a wire type either. It declares a storage family name, record type, physical table coordinate, and key policy (`Domain` or `Identified`). The legacy architecture explicitly identifies the table name as a storage coordinate rather than semantic identity and derives a family closure hash from reachable type data.

Legacy enum variants also carry an optional `StreamRelation`:

```text
Opens(StreamName) | Belongs(StreamName)
```

The source spelling is a four-object parenthesized signature, such as:

```text
(SubscribeIntent SubscribeIntent opens IntentEventStream)
(IntentRecorded IntentRecorded belongs IntentEventStream)
```

This is the historical four-root model still used by `repos/signal-spirit/schema/signal.schema` and the pre-next-generation `spirit/schema/sema.schema`.

### Current six-root general schema

The current source on `schema-language` main and its pushed next-generation adaptation branch `language-family-nextgen-schema-language` at `41a7b257` has a different fixed root layout. `SchemaSource::from_document` reads exactly six positions in this order:

```text
imports brace
input root
output root
types brace
generics brace
impls brace
```

All six positions are mandatory; an empty position is an empty typed block. The type source is already split into stringless `CoreSchema` plus `NameTable`; `TrueSchema` is a view over those values. Its current core carries imports, roots, namespace declarations, and impl blocks. It has no stream/family vectors and its source reader has no legacy `Streaming` variant form.

`repos/schema-language/ARCHITECTURE.md` calls streams and families retired constructs. It gives an important reason for the family removal: storage declarations belong to a separate `sema.schema` document kind, rather than as a general-schema metadata head or a generic-schema block. The same document explains that document kind is the first expected-type boundary.

### Exact Spirit consumer semantics

The blocker is not merely an old syntax spelling.

`repos/signal-spirit/schema/signal.schema` declares:

- `SubscribeIntent` as an Input variant that **opens** `IntentEventStream`;
- `IntentRecorded`, `IntentClarified`, `IntentSuperseded`, and `IntentRetired` as event variants that **belong** to that stream;
- `IntentEventStream` with `SubscriptionToken`, `SubscriptionStarted`, `IntentEvent`, and `SubscriptionToken` as its token/opened/event/close references.

The generated `signal-spirit` module uses that information to define its `StreamingFrame<Input, Output, IntentEvent>` aliases and event framing. Spirit's daemon and transport consume those generated stream types.

`repos/signal-spirit/src/help.rs` is a second direct consumer. It stores `Vec<TrueSchema>` in `HelpModel`, looks up `TrueSchema::streams()` and `TrueSchema::families()`, reconstructs `SourceStreamBody`/`SourceFamilyBody`, and renders them as positional help rows. Existing tests require, among other exact output:

```text
(Stream { token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken })
```

They also prove that stream relations survive the structured `TrueSchema` NOTA projection. Therefore deleting stream metadata simply to parse the current six-root body changes both the generated streaming contract and Help semantics.

A distinct storage consumer exists too. `repos/spirit/schema/sema.schema` declares `RecordsFamily`, `ReferentsFamily`, and `MigrationsFamily`; generated `RecordFamily` descriptors are registered by `repos/spirit/src/store/mod.rs` and routed by `src/store/family_directory.rs`. This confirms that family data is storage policy, not generic type-schema data.

`meta-signal-spirit/schema/meta-signal.schema` is an ordinary owner-only signal contract with no stream declarations. It imports signal-spirit nouns. It must still be migrated consistently because it is built against the same schema-language/schema-rust closure, but it does not itself require stream metadata.

## Decision: distinct typed document kinds

### Recommendation

Keep generic type declarations in `CoreSchema`; move signal stream topology to a separate **CoreSignalContract** document kind; keep storage families in the already-earned **CoreSemaSchema** document kind.

This is preferable to restoring streams/families inside generic CoreSchema:

| Choice | Preserves current Spirit behavior | Fits current construct partition | Main cost |
| --- | --- | --- | --- |
| Restore `Stream`/`Family` in generic CoreSchema | yes, initially | no; reverses retired constructs and mixes contract/storage metadata with types | recreates a broad mixed schema model |
| Keep old schema-language generator only for signal-spirit | temporarily | no durable migration; leaves two compiler boundaries | permanent release-train exception |
| **TypeSchema + SignalContract + SemaSchema kinds** | **yes, through typed projections** | **yes; each noun has one document kind** | one explicit document dispatcher and two focused core records |

A signal stream is contract topology: it relates an input admission, an acknowledgement, an event sum, and a closure token. A family is storage topology: it relates a stored record layout, key policy, physical materialization coordinate, and indexes/projections. Neither is a generic data type. They therefore do not belong as vectors in `CoreSchema` or as special cases in `EnumVariant`.

## Proposed bootstrap header and dispatch

### Header grammar

**Proposal in current next-generation NOTA syntax:** every `.schema` source file begins with exactly one bootstrap header raw block:

```text
TypeSchema.1
```

or:

```text
SignalContract.1
```

or:

```text
SemaSchema.1
```

A reader first parses only the first root object with an immutable, minimal bootstrap raw profile. That profile recognizes the header's atom, dot-application, and integer shape and nothing dialect-specific. It produces a right-associated `Application` tree for `Kind.1`. Before any document-body decoder runs, a small trusted bootstrap decoder is invoked with the already-known expected type `DocumentHeader`:

```text
DocumentHeader {
  kind: DocumentKind,
  format_version: DocumentFormatVersion,
}

DocumentKind ::= TypeSchema | SignalContract | SemaSchema
DocumentFormatVersion ::= positive integer
```

The header's form is one exact application of a registered PascalCase `DocumentKind` atom to an integer leaf. It does not examine the body. The selected registration supplies the body raw profile; the reader then parses the remaining source under that exact profile. It selects a decoder only by the exact header pair:

```text
(DocumentKind, DocumentFormatVersion)
  -> DocumentDecoderRegistration { body_raw_profile_identity, ... }
```

Thus the parser still never classifies arbitrary input. Every file first has the fixed expected type `DocumentHeader`; then the header selects a previously registered body raw profile, root expectation, and StructuralForm table. Filename and extension are discovery aids only and are not semantic authority. A future header spelling that itself needs a new raw construct would require a bootstrap-profile revision and an explicit migration; it cannot be introduced by a body dialect package.

A header is Textual framing, not Core data. Changing a file from an old textual document format to a newer canonical format must not change the decoded Core bytes. The header is archived in a source-artifact envelope to preserve historical decoding provenance, but is excluded from domain Core identity.

### Historical decoding and upgrade

Each registered decoder owns:

```text
DocumentDecoderRegistration {
  kind,
  format_version,
  raw_profile_identity,
  structural_table_identity,
  source_archive_layout,
  decode_to_current_core,
}
```

Old files retain their old header. Their historical decoder produces the current typed Core record plus NameTable. Canonical re-encoding uses the current registered Textual form and writes its current header. If a change cannot preserve the current Core record, it is a typed document upgrade with an explicit input/output record and fixtures; it is never a permissive parser fallback.

This answers the bootstrap problem without letting a body choose its own language. The bootstrap decoder is deliberately small, closed, and revisioned; it recognizes only the fixed header form and dispatches to registered expected roots.

## Proposed Core records and namespace rules

The records below use names for explanation. In implementation, every name-bearing reference is an identifier allocated in the document's NameTable.

```text
CoreDocumentEnvelope {
  kind,
  document_format_version,
  structural_table_identity,
  raw_profile_identity,
  core_layout_version,
  core_identity,
  name_table_identity,
}

CoreTypeSchema {
  imports: [CoreResolvedImport],
  input: CoreRoot,
  output: CoreRoot,
  declarations: [CoreDeclaration],
  impl_blocks: [CoreImplBlock],
}

CoreSignalContract {
  schema: CoreTypeSchema,
  streams: [CoreSignalStream],
  relations: [CoreSignalRelation],
}

CoreSignalStream {
  identifier,
  token: CoreTypeReference,
  opened: CoreTypeReference,
  event: CoreTypeReference,
  close: CoreTypeReference,
}

CoreSignalRelation {
  endpoint: CoreSignalEndpoint,
  relation: CoreSignalRelationKind,
  stream: identifier,
}

CoreSignalEndpoint {
  root: CoreRootPosition,       // Input or Output
  variant: identifier,
}

CoreSignalRelationKind ::= Opens | Belongs

CoreSemaSchema {
  imports: [CoreResolvedImport],
  declarations: [CoreStorageDeclaration],
}

CoreStorageDeclaration {
  identifier,
  record: CoreTypeReference,
  key: CoreStorageKey,
  materialization: CoreStorageMaterialization,
  indices: [CoreIndexDeclaration],
  projections: [CoreProjectionDeclaration],
}
```

`CoreSignalContract` embeds or directly owns a `CoreTypeSchema` because a signal contract declares the roots and types the contract exposes. It has one allocation universe and one `SignalContractNameTable` for the loaded whole: roots, variants, types, streams, imports, and metadata identifiers cannot collide ambiguously. A `CoreSignalRelation` points to existing root/variant and stream identifiers; it does not copy display strings or insert relation state into generic `CoreVariant`.

`CoreSemaSchema` is a different loaded whole with its own NameTable. It references public types exported by a signal/type document through stable imported identity, never through copied spelling. The local alias/display name is stored only in the Sema NameTable.

The unresolved global schema-unit/split/merge policy still governs how these allocation universes are persisted and remapped. This design does not presume a global `u32` type ID. For the present implementation, every identifier is scoped by document/loaded-whole identity and Core layout.

All three Core records are rkyv archives. Their domain identities are distinct and include their typed Core-layout version. Their NameTable identities are co-versioned sidecar identities and excluded from Core hashes. Document format version, StructuralForm revision, and raw-profile revision are also separate from the Core layout version.

## Proposed Textual forms

The following examples are proposals in the current next-generation grammar. They demonstrate exact root positions rather than finalized spelling.

### `TypeSchema.1`

```text
TypeSchema.1
{}
[ Request ]
[ Accepted ]
{
  Request.{ Integer }
  Accepted.{ Request }
}
{}
{}
```

After the header, this is the current six-root general schema body: imports, input, output, types, generics, impls. The header makes that body unambiguous without relying on filename.

### `SignalContract.1`

```text
SignalContract.1
{}
[ SubscribeIntent ]
[ SubscriptionStarted ]
{
  SubscribeIntent.{ Query }
  SubscriptionStarted.{ IntentSubscription }
  IntentEvent.[ IntentRecorded.IntentRecorded IntentClarified.IntentClarified ]
  IntentEventStream.{ SubscriptionToken SubscriptionStarted IntentEvent SubscriptionToken }
}
{}
{}
{
  IntentEventStream.{ SubscriptionToken SubscriptionStarted IntentEvent SubscriptionToken }
}
{
  Input.SubscribeIntent.Opens.IntentEventStream
  Output.IntentRecorded.Belongs.IntentEventStream
  Output.IntentClarified.Belongs.IntentEventStream
}
```

The example intentionally has two final per-kind blocks after the six type-schema blocks:

```text
streams brace
stream-relations brace
```

They belong only to `SignalContract`, are both mandatory (possibly empty), and contain one object class each. The first `IntentEventStream` shown in the types block is illustrative only if the event type itself is exported as a normal type; the actual stream descriptor is the entry in the dedicated streams block. A final language definition must avoid duplicating the same stream name as a type unless the two are intentionally distinct identifiers; the recommended canonical model is that `IntentEvent` is the event type and `IntentEventStream` exists only in the streams block.

A less redundant canonical example is therefore:

```text
SignalContract.1
{}
[ SubscribeIntent ]
[ SubscriptionStarted ]
{
  SubscribeIntent.{ Query }
  SubscriptionStarted.{ IntentSubscription }
  IntentEvent.[ IntentRecorded.IntentRecorded IntentClarified.IntentClarified ]
}
{}
{}
{
  IntentEventStream.{ SubscriptionToken SubscriptionStarted IntentEvent SubscriptionToken }
}
{
  Input.SubscribeIntent.Opens.IntentEventStream
  Output.IntentRecorded.Belongs.IntentEventStream
  Output.IntentClarified.Belongs.IntentEventStream
}
```

The expected `CoreSignalRelation` type gives the four application segments their positions. `Input`/`Output` are a closed root-position vocabulary; `Opens`/`Belongs` are a closed relation-kind vocabulary. Raw application itself remains unclassified.

### `SemaSchema.1`

The existing `spirit/schema/sema.schema` is evidence for a separate storage document, but its exact new entry syntax remains open. A shape consistent with the records above would be:

```text
SemaSchema.1
{
  StoredRecord.RecordsFamily.Domain
  StoredReferent.ReferentsFamily.Domain
  Migration.MigrationsFamily.Domain
}
```

This is only a placeholder proposal. It intentionally does not preserve the retired generic `Family.{...}` head. Storage table coordinates, indices, and projections need their own typed positional forms under `SemaSchema`; they should be designed with sema-engine rather than smuggled back into `TypeSchema`.

## Projection and consumer consequences

### schema-language

`schema-language` should gain a `DocumentHeader` reader and a document dispatcher above individual kind decoders. The current `SchemaSource` reader becomes the `TypeSchema.1` body reader rather than the only entry point. It should not accept headerless text after the migration cutover.

`CoreSignalContract` and its NameTable/view belong in a focused signal-contract model or contract-schema component, not as fields restored in `CoreSchema`/`TrueSchema`. The exact package boundary is an implementation decision, but source dependencies should remain one-way: the generic type-schema substrate must not import signal runtime code.

The legacy `TrueSchema` archive is not a viable long-term Help storage boundary. The current branch no longer provides the legacy archived `TrueSchema` shape that `signal-spirit::HelpModel` assumes. Help should store an rkyv `SignalContractSnapshot { CoreSignalContract, SignalContractNameTable, imported snapshots or resolved import identities }` and project it through typed views. The public help response still renders the established canonical rows; it need not retain legacy source AST objects.

### schema-rust and generated signal artifacts

`schema-rust` continues to lower normal roots/types/impls from the embedded `CoreTypeSchema`. For a `SignalContract`, a focused lowering adds:

- streaming frame aliases and constants from `CoreSignalStream`;
- subscription open/event/close routing from `CoreSignalRelation`;
- generated validation that every `Opens` endpoint is an Input variant and every `Belongs` endpoint is an Output/event variant of the declared stream event type;
- generated documentation/help metadata from the same typed contract snapshot.

This preserves the current signal-spirit generated contract without putting stream relation fields back on generic enum variants. A generator must produce byte-identical Rust for the selected legacy Spirit contract before this new form becomes canonical; any byte difference is reviewed as a real generator change, not dismissed as formatting.

### signal-spirit and meta-signal-spirit

`signal-spirit/schema/signal.schema` must migrate as a whole to `SignalContract.1`, preserving:

- every Input/Output route and generated rkyv field ordering;
- the `IntentEventStream` token/opened/event/close tuple;
- the `SubscribeIntent` opens relation;
- all event belongs relations;
- Help targets and canonical body text.

`meta-signal-spirit` should migrate to the appropriate headered kind. Since it has no stream topology, it may use `SignalContract.1` with empty streams/relations to preserve its signal-root semantics, or `TypeSchema.1` only if the generator has an explicit non-stream signal-contract projection. That classification should be selected by the component's contract purpose, not by whether today's streams block happens to be empty.

### Spirit storage

`spirit/schema/sema.schema` must become `SemaSchema.1` and regenerate `src/schema/sema.rs` descriptors. That migration is a storage-schema change, not a text-only rewrite: it requires exact record-family identity comparison, old-store fixtures, forward migration, and isolated rollback/restore evidence. The existing `StoreFamilyDirectory`, production migration code, and sema-engine table registrations make this a separate migration track from signal wire migration.

## Version taxonomy

The header removes a dangerous conflation. These versions are independent and must be recorded independently:

| Version | Identifies | Changes when | Does not by itself change |
| --- | --- | --- | --- |
| Document-format version | textual body grammar for one document kind | header/body format evolves | Core semantics or Core identity if decoding is equivalent |
| Raw-profile revision | recognized raw glyph/tree grammar | raw lexical/structural grammar evolves | expected-type meaning alone |
| StructuralForm/table revision | expected-type text/Core form | canonical form or decoder changes | Core layout when same Core is produced |
| Core-layout version | rkyv Core record layout and Core hash domain | stored semantic shape changes | NameTable-only rename |
| NameTable layout/version | naming sidecar representation | name allocation/projection representation changes | Core hash |
| Wire-contract version | signal operation/reply binary compatibility | rkyv wire meaning or layout changes | source text syntax alone |
| Package version | published component release | package API/release changes | a particular document or wire format automatically |

A header's `1` is **document-format version**, never a package version, Core layout version, or wire version.

## Migration and release-train gates

The blocked release train can resume only with a deliberate expansion, not a lock-only edit.

1. Define and test the header dispatcher, `TypeSchema.1`, and historical legacy decoder fixtures.
2. Define `SignalContract.1`, `CoreSignalContract`, NameTable/view/archive, and its exact stream/relation validation.
3. Migrate a bounded signal fixture and prove that the new generator reproduces its Rust/stream/help outputs.
4. Migrate `signal-spirit` with golden comparison for `src/schema/signal.rs`, streaming frame behavior, and every Help target. Preserve the established stream help row exactly unless an explicit product decision changes it.
5. Migrate `meta-signal-spirit` and all import resolution fixtures.
6. Separately design and migrate `SemaSchema.1`; verify generated family identities, store reopen, historical production fixtures, forward migration, and isolated restore.
7. Only then update the release-train intent to include `signal-spirit`, `meta-signal-spirit`, and Spirit; materialize per-component Cargo/flake locks, run the generated integration closure, and perform an isolated copied-store/socket pilot.

Required compatibility witnesses:

- header dispatch rejects unknown `(kind, format-version)` before body decoding;
- a historical four-root signal file decodes through its registered legacy decoder, then re-emits canonical current text without changing decoded Core identity where semantic equivalence is defined;
- the same raw application shape is accepted as a string/float/reference only under its expected leaf type;
- `CoreSignalContract` plus its NameTable survives rkyv round trip;
- stream relation validation rejects missing streams, missing endpoints, wrong root positions, and incompatible event payloads;
- old and new signal generated Rust has byte-exact selected goldens and equivalent streaming-frame routes;
- Help's stream body, top-level targets, and rkyv snapshot round trips remain stable or have an explicitly versioned public migration;
- Sema family descriptor/hash changes have legacy-store and rollback fixtures;
- the train's Nix closure uses only exact pushed commits and no local path.

## Risks and boundaries

- The source reports record that generic streams and families were deliberately retired. Reinstating them unchanged would be a regression to a mixed metadata namespace, not a minimal compatibility repair.
- The header itself is new syntax. Its exact spelling and whether the extension remains `.schema` are proposals requiring acceptance; the need for a kind-first typed boundary follows from existing architecture and the current blocker.
- `SignalContract.1` must not add generic relation/equivalence constructs. Its relations are closed signal topology records only.
- Existing `HelpModel` is public Rust API and rkyv-derived. Replacing stored `TrueSchema` with a contract snapshot is a package/API/archive compatibility event even if rendered help text remains identical.
- Storage family migration can change persistent identities and is not authorized by a green wire-contract build. It needs its own storage migration evidence.
- The future general StructuralForm table may supersede today’s handwritten body readers, but this document-kind boundary should not wait for that work. The bootstrap header dispatcher can initially use a small trusted typed reader and later be expressed by the accepted StructuralForm authority.

## Psyche-only questions

1. Confirm the document-kind direction: `TypeSchema`, `SignalContract`, and `SemaSchema` are separate typed documents, rather than restoring Stream/Family to generic CoreSchema. The report recommends this direction.
2. Approve a mandatory first textual header with `(DocumentKind, document-format version)` and header-selected historical decoder dispatch. The report proposes `TypeSchema.1`, `SignalContract.1`, and `SemaSchema.1` in current next-generation syntax.
3. Confirm that signal streams and `Opens`/`Belongs` are typed `CoreSignalContract` topology, not generic enum/type metadata and not Textual-only Help decoration.
4. Confirm that storage families remain a `SemaSchema` concern and need their own migration, rather than being restored to type schema.
5. For stream relations, is the proposed explicit endpoint spelling `Input.SubscribeIntent.Opens.IntentEventStream` / `Output.IntentRecorded.Belongs.IntentEventStream` acceptable as a design direction, or should root position be implicit from the target variant's type?
6. Should a non-streaming ordinary signal contract such as meta-signal-spirit still be `SignalContract` with empty stream sections, or should it be a distinct non-stream contract kind? This affects the smallest stable kind taxonomy.
