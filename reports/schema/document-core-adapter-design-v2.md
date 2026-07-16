# Schema document roots, Core records, and consumer adapters

**Status:** authorized source-backed design. This is not an implementation, deployment, or Synchronizer readiness claim.

## Decision

Use one closed, header-dispatched document family with four *typed* roots:

| Header | Root/Core | Status | Reason |
| --- | --- | --- | --- |
| `TypeSchema.1` | `CoreTypeSchemaV1` | accepted | General type declarations and its Input/Output roots are the existing six-block schema concern. |
| `SignalContract.1` | `CoreSignalContractV1` | accepted | Peer wire operations and protocol topology have extra stream and endpoint laws. |
| `NexusRuntime.1` | `CoreNexusRuntimeV1` | **header noun proposed** | Internal Work/Action/effect translation topology has different roots and lifecycle laws. |
| `SemaStorage.1` | `CoreSemaStorageV1` | **header noun proposed** | Durable read/write, record, migration, family, table, and key-policy laws are storage concerns. |

`NexusRuntime` and `SemaStorage` are deliberately proposal names, not a ruling on their final header nouns. The source settles that their roots/laws differ from Signal and generic Schema; it does not settle their public textual nouns.

This is not a single generic `Kind.1` with optional bodies. A kind owns its expected root and validation law before body decoding. Shared lower-level declaration, reference, root, import, generic, and impl records are reused, but a generic `TypeSchema` may not regain Stream, Family, relation, runtime, or storage authority.

Ordinary `signal-spirit` and `meta-signal-spirit` should both be `SignalContract.1`. Their source is generated peer-wire contract material; the latter's owner policy and presently empty stream topology do not establish a different Core shape or validation law. It uses empty mandatory topology sections, rather than creating a meta-only document kind or pretending that an empty contract is a generic type document.

### Source basis

- `repos/schema-language/ARCHITECTURE.md:364-440` intentionally removes generic streams, relations, and families, while retaining a fixed six-position type schema.
- `repos/schema/src/schema.rs:464-472, 2156-2205, 2261-2298` preserves the legacy mixed `TrueSchema`, stream relation/descriptor, and family record/table/key semantics to migrate.
- `repos/signal-spirit/schema/signal.schema:44, 165-166` attaches `opens`/`belongs` and `IntentEventStream` to the signal contract; `repos/signal-spirit/src/help.rs:352-365, 486-522` consumes those declarations.
- `repos/spirit/schema/nexus.schema:44-78` defines Work/Action/effect topology; `repos/spirit/src/nexus.rs:435-585` owns effect execution.
- `repos/spirit/schema/sema.schema:25-64` defines durable read/write roots, stored records, migration record, and three families; `repos/spirit/src/store/mod.rs:98, 336-348, 507-516` owns schema-versioned table registration.

## Shared Core and NameTable law

All `Core*` values are rkyv records containing no text. `NominalId`, `ScopedTypeId`, `ImportId`, `VariantId`, `FieldId`, `StreamId`, `FamilyId`, and `TableCoordinateId` below are closed typed identifiers, never strings. `CoreTypeRef` is an identifier-based local/imported type reference. Existing `CoreSchema` provides the immediate precedent: imports, roots, declarations, and impl blocks are stringless (`repos/schema-language/src/core.rs:119-169`).

Every loaded document has one corresponding NameTable sidecar:

```text
DocumentNameTableV1 {
  allocation_layout: NameTableLayoutVersion,
  entries: [NameEntry]
}

NameEntry {
  identifier: NamedIdentifier,
  owner: Optional<NominalId>,
  current_spelling: Text
}
```

The table resolves declaration, member, import-alias, stream, family, and storage-coordinate spellings. It is not embedded in Core and cannot participate in Core identity. In particular, `TableCoordinateId` is Core data and its current physical table spelling is a NameTable entry. A coordinate spelling change is therefore not silently treated as a harmless deployment action: the storage migration adapter must explicitly classify and execute it.

Allocation follows the current preservation discipline, without claiming to solve its known schema-unit problem:

1. On an authorized edit, re-associate an unchanged `(identifier kind, owner scope, current spelling)` against the applicable prior NameTable.
2. A table-mediated rename retains its identifier; member identifiers remain owned by the stable owner identifier.
3. New declarations mint identifiers; names must remain unique in their kind/owner scope; tables canonically sort by identifier.
4. A direct source spelling change without the prior allocation context is not assumed to be a rename. It can be delete-plus-add.
5. Which persisted table/allocation universe applies across split and merge remains open. No record or adapter below infers that policy.

This is the current source's explicit provisional constraint, not a new allocation scheme (`repos/schema-language/src/identifier.rs:1-39, 390-475`).

Each Core kind has a distinct identity domain and an explicit Core-layout version. Its identity is BLAKE3 over that Core record's canonical rkyv bytes under that domain/layout; the NameTable, source header, source formatting, raw profile, and StructuralForm table are excluded. A NameTable has its own versioned identity/provenance. This applies equally to all proposed Core records, following `CoreSchema::canonical_bytes` and its domain-separated identity (`repos/schema-language/src/core.rs:166-169`, `src/identity.rs:1-40, 128-140`).

## Exact proposed Core shapes

`CoreDeclarationSetV1` is the shared *lower-level record*, not a document and not a compatibility back door:

```text
CoreDeclarationSetV1 {
  imports: [CoreImportDeclaration],
  resolved_imports: [CoreResolvedImport],
  declarations: [CoreDeclaration],
  generic_declarations: [CoreGenericDeclaration],
  impl_blocks: [CoreImplBlock]
}

CoreEndpointRootV1 ::= Enum(CoreEnum) | Application(CoreRootApplication)
CoreTypeRef ::= Local(ScopedTypeId) | Imported(ImportedTypeId)
```

All nested declaration, enum, struct, field, variant, application, and reference records are the existing identifier-bearing Core forms. The proposed records only add domain-owned topology that cannot live in those general forms.

### Generic type document

```text
CoreTypeSchemaV1 {
  declarations: CoreDeclarationSetV1,
  input: CoreEndpointRootV1,
  output: CoreEndpointRootV1
}

TypeSchemaNameTableV1 = DocumentNameTableV1
```

This is the stringless equivalent of the current six mandatory body positions: imports, input, output, types, generics, impls. It has no stream, relation, family, storage, Work, Action, or effect field.

### Signal contract

```text
CoreSignalContractV1 {
  declarations: CoreDeclarationSetV1,
  input: CoreEndpointRootV1,
  output: CoreEndpointRootV1,
  streams: [CoreSignalStreamV1],
  relations: [CoreSignalRelationV1]
}

CoreSignalStreamV1 {
  identifier: StreamId,
  token: CoreTypeRef,
  opened: CoreTypeRef,
  event: CoreTypeRef,
  close: CoreTypeRef
}

CoreSignalEndpointV1 {
  root: SignalRootPosition,       // Input | Output
  variant: VariantId
}

CoreSignalRelationV1 {
  endpoint: CoreSignalEndpointV1,
  relation: SignalRelationKind,   // Opens | Belongs
  stream: StreamId
}

SignalContractNameTableV1 = DocumentNameTableV1
```

The four stream references directly preserve the legacy token/opened/event/close tuple. A relation carries no display name and does not extend generic `CoreVariant`. Validation requires every `StreamId`/endpoint to resolve; `Opens` targets an Input variant; `Belongs` targets an Output variant; each endpoint appears at most once for its applicable role; and a belonging event payload is compatible with that stream's `event` type. The exact multiplicity/lifecycle evaluator beyond these source-visible laws is deliberately not hardened here.

`SubscribeIntent opens IntentEventStream` and the four event `belongs IntentEventStream` relations in the current signal source lower directly to this record. A Stream is protocol sequence/lifecycle topology, not `Vec<T>`; `opens` and `belongs` are closed protocol-role relations, not generic associations.

### Nexus runtime topology

```text
CoreNexusRuntimeV1 {
  declarations: CoreDeclarationSetV1,
  work: CoreNexusWorkRootV1,
  action: CoreNexusActionRootV1,
  effect: CoreNexusEffectTopologyV1
}

CoreNexusWorkRootV1 {
  root: NominalId,
  signal_input: CoreTypeRef,
  sema_write_output: CoreTypeRef,
  sema_read_output: CoreTypeRef,
  effect_result: CoreTypeRef
}

CoreNexusActionRootV1 {
  root: NominalId,
  signal_output: CoreTypeRef,
  sema_write_command: CoreTypeRef,
  sema_read_input: CoreTypeRef,
  effect_command: CoreTypeRef,
  continuation_work: CoreTypeRef
}

CoreNexusEffectTopologyV1 {
  command: CoreTypeRef,
  result: CoreTypeRef
}

NexusRuntimeNameTableV1 = DocumentNameTableV1
```

The roles and ordering are source-backed by the actual `Work` and `Action` root applications. `effect.command`/`result` make the declared effect boundary explicit and must equal the references used by Action/Work; they do not duplicate a second effect vocabulary. The declaration set contains the closed command/result variants and payload records. Validation is runtime-specific: all role references resolve, Work/Action carry exactly the listed topology, the continuation is the Work root, and effect result/command references agree. It is not Signal wire validation, nor Sema table validation.

### Sema storage

```text
CoreSemaStorageV1 {
  declarations: CoreDeclarationSetV1,
  write_input: CoreEndpointRootV1,
  read_input: CoreEndpointRootV1,
  write_output: CoreEndpointRootV1,
  read_output: CoreEndpointRootV1,
  families: [CoreSemaFamilyV1]
}

CoreSemaFamilyV1 {
  identifier: FamilyId,
  record: CoreTypeRef,
  table: TableCoordinateId,
  key: SemaFamilyKeyPolicy
}

SemaFamilyKeyPolicy ::= Domain | Identified
SemaStorageNameTableV1 = DocumentNameTableV1
```

`StoredRecord`, `StoredReferent`, and `Migration` remain ordinary stringless record declarations in `declarations`; `RecordsFamily`, `ReferentsFamily`, and `MigrationsFamily` reference them through three `CoreSemaFamilyV1` values. This is exact to the source's record/table/key arrangement. It does **not** invent a second migration policy field: the current store's runtime schema version and forward-migration behavior remain engine/storage-consumer policy until separately authored and accepted.

A `SemaFamilyClosure` is a derived, versioned resolver result, not a generic field and not a name-bearing legacy projection: starting from the family record reference, it follows the resolved declaration/import graph and the source-required relation/stream edges. This preserves the old family-closure reachability behavior, including reachable stream declarations, without moving Family into generic schema. Its content identity is separately domain/layout-versioned over the resolved stringless closure; table spellings remain excluded. The resolver must fail on absent imports, record, endpoint, or stream rather than make an incomplete closure.

## Legacy TrueSchema disposition

| Legacy material | Disposition | Authority after migration | Evidence |
| --- | --- | --- | --- |
| `identity` / authored schema version | compatibility/view provenance only; not Core bytes | document archive/view receipt; not a replacement for any independent version axis | Legacy `TrueSchema` fields; current split keeps identity outside Core. |
| `imports`, `resolved_imports` | `CoreDeclarationSetV1` in every owning document | Core | `schema` and `schema-language` models. |
| `input`, `output` | typed root fields of TypeSchema or SignalContract; Sema has four typed read/write roots | Core | Current TypeSchema and Signal; Sema source. |
| `namespace` declarations | `CoreDeclarationSetV1.declarations` | Core | Current CoreSchema. |
| generic/impl declarations | `CoreDeclarationSetV1.generic_declarations` / `impl_blocks` | Core | Current six-block layout. |
| `EnumVariant.stream_relation` | `CoreSignalContractV1.relations` | Core | Legacy relation and signal source. |
| `streams: Vec<StreamDeclaration>` | `CoreSignalContractV1.streams` | Core | Legacy descriptor and signal generator/help use. |
| stream display name and all names | matching Signal NameTable | NameTable | Stringless Core rule. |
| `families: Vec<FamilyDeclaration>` | `CoreSemaStorageV1.families` | Core | Sema source and store registration. |
| family display name and physical table spelling | Sema NameTable (`FamilyId`, `TableCoordinateId`) | NameTable, with explicit storage migration classification | Legacy comments call table a coordinate; Core must remain stringless. |
| `FamilyKey::{Domain, Identified}` | `SemaFamilyKeyPolicy` | Core | Legacy closed enum. |
| `RelationDeclaration` not meaning signal topology | intentional retirement unless a separately typed owning document/law is evidenced | no generic compatibility projection | Generic schema explicitly retired relations. |
| monolithic `TrueSchema` archive/API | compatibility-only projection | adapters assemble typed projections; never Core authority or identity input | Current `schema-language::TrueSchema` is already a Core+NameTable view. |
| legacy NOTA source spelling | registered historical decoder input only | archive migration adapter | Header cutover cannot use body inference. |

No adapter may synthesize missing streams, relations, families, visibility, or imports from the old projection. Source visibility remains one known authored-semantic fidelity gap in the newer Schema-to-Rust library path; it must be represented before claiming complete authored fidelity.

## Header, registration, and version dispatch

1. Parse exactly the first root under a tiny closed bootstrap profile as `DocumentHeader { kind: DocumentKind, format_version: positive integer }`. `TypeSchema.1` and `SignalContract.1` are accepted examples. The proposed Nexus/Sema spellings are not accepted merely because they appear above.
2. Look up the exact `(kind, document_format_version)` in a closed registration table. No filename, extension, later body form, trial parser, or consumer preference participates.
3. The registration supplies the body raw-profile identity, expected root type, StructuralForm-table identity/revision, Core-layout version, decoder, encoder, and historical upgrade path.
4. Parse/decode the remaining body only with that registration and its expected types. Unknown kind or format version fails before body decoding; an unavailable historical registration fails rather than falling back.
5. Evaluate StructuralForms only by expected type/address. The seven-case `StructuralForm` data kernel and addressed-table separation are current evidence (`repos/structural-codec/src/form.rs:16-47`, `src/table.rs:1-115`). This design does not settle evaluator backtracking, ambiguity, macro, or hardening internals.
6. Decode to Core plus NameTable, validate the typed root laws, then compute Core identity. A historical textual decoder may produce the current Core only through an explicit registered upgrade.

The version axes are independent:

| Axis | Meaning | Changes for |
| --- | --- | --- |
| document-format | a kind's header/body text format | grammar/header evolution |
| raw profile | raw glyph/tree recognition | raw notation revision |
| StructuralForm/table | expected-type form vocabulary | form/table evolution |
| Core-layout | archived semantic record and Core identity domain | Core shape changes |
| NameTable layout | sidecar allocation/projection representation | naming-sidecar changes |
| wire-contract | peer binary operation/reply compatibility | Signal wire change |
| storage schema | durable physical/migration compatibility | Sema persisted-store change |
| package/release | published component release | package delivery change |

The header integer is document-format only. It is never a StructuralForm, Core-layout, wire-contract, storage-schema, or package/release version.

## Consumer adapters

| Boundary | Input and output | Permitted work | Prohibited work |
| --- | --- | --- | --- |
| signal-spirit Help | `CoreSignalContractV1` + Signal NameTable + resolved imports → current Help rows/snapshot | resolve identifiers; render roots, stream tuple, relations, and compatible family/storage references if Help requests them | infer topology from generated Rust; create a stream/family; include projection in Core identity |
| schema-rust / Core→Nomos→Logos | typed Core + corresponding NameTable → Nomos → CoreLogos → generated Rust | lower shared declarations; lower Signal stream/relations to current streaming aliases and event helpers; retain NameTable continuity through Nomos/Logos | accept legacy TrueSchema as authority; put names/forms into Core identity; emit topology absent from Signal Core |
| Sema/storage | `CoreSemaStorageV1` + Sema NameTable → family descriptors, closure, migration plan | resolve record/table/key; register descriptors; compare storage layout; execute explicitly approved migrations | treat a table spelling update as text-only; change a store without storage migration evidence |
| legacy TrueSchema | registered legacy source/archive → typed Core documents + NameTables → compatibility projection where needed | preserve values exactly where each target Core has a home; report intentional retirement | body-infer kind; merge Signal and Sema metadata into generic Core; invent missing data |

Help must preserve current canonical signal wire/help behavior: stream token/opened/event/close rows, targeted streams/families, and `opens`/`belongs` projection. The generator must preserve the existing `StreamingFrame` and subscription-event behavior. These are acceptance witnesses, not license to retain legacy `TrueSchema` as production authority.

The nine-crate Schema→Nomos→Logos→Rust path is a clean-mainline library/test pipeline with byte-exact fixtures and identity/macro-failure tests, but it is neither externally consumed nor deployed. It may supply the adapter's lowering stages; it does not prove full authored fidelity or train readiness. Synchronizer remains **NO-GO** and is not an adapter or a delivery claim.

## Migration and acceptance sequence

1. Add only the closed header bootstrap and registration tests, beginning with `TypeSchema.1`; reject unknown kind/version before body parsing. Preserve explicit historical fixtures.
2. Establish `CoreTypeSchemaV1`/NameTable archival, identity, projection, and structural-form conformance witnesses. Keep header/version axes separately asserted.
3. Add `CoreSignalContractV1`, its NameTable, relation/stream validation, archive round trips, and a bounded fixture migrated from legacy source.
4. Drive that fixture through Schema→Nomos→Logos→Rust. Compare selected generated Rust bytes and streaming routes with existing goldens; compare Help stream body, targets, relations, and snapshot round trips.
5. Migrate `signal-spirit` as one contract. Migrate `meta-signal-spirit` as the same kind with empty stream/relation sections; exercise imports and generated wire compatibility.
6. Add the separately finalized Nexus header/root only after its noun and expected-root form are accepted; verify Work/Action/effect topology without exposing it as peer wire.
7. Add the separately finalized Sema header/root and family resolver. Compare family descriptors/closures, open historical store fixtures, prove forward migration and isolated restore/rollback behavior before changing a real store.
8. Make candidate work reachable through the actual Help, generator, signal, and storage consumers. Run their real repo/Nix checks and only use pushed, pinned dependencies for an integration closure.
9. Treat any Synchronizer integration as a separate future gate. It still lacks end-to-end CLI/discovery, valid generated-flake build, observed-base proof, and real train verification.

Required negative witnesses include: unknown header pair; body that would parse under another kind; missing NameTable resolution; missing stream/endpoint; wrong relation root; incompatible event payload; duplicate family/table policy conflict; identifier-allocation collision; unsupported authored visibility; and historical store incompatibility. None can be repaired by projection fallback.

## Decision slate

Only these semantic decisions still need psyche authority:

1. **Nexus textual noun:** should the internal Work/Action/effect document be named `NexusRuntime` or another name that conveys its runtime-translation role?
2. **Sema textual noun:** should the durable record/family/table/key document be named `SemaStorage` or another name that conveys its storage role?
3. **Schema-unit allocation:** what authoritative lineage/allocation rule carries NameTables through document split and merge? This design intentionally does not infer it.
4. **Authored visibility fidelity:** should source visibility become represented Core semantics before generated Rust is considered a complete source-faithful projection, and what compatibility policy applies?

The type-root separation, mandatory first header, SignalContract classification (ordinary and meta), stream/family ownership, stringless Core identity, and independent versions are not reopened by this slate.

## Validation scope

This report is design-only. No source, generated artifact, store, deployment, or Spirit activation was changed. Its claims were checked against the cited current source and the supplied source-audit artifacts, including the current nine-crate pipeline and Synchronizer NO-GO findings.
