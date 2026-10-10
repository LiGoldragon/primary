# Per-File-Kind Schemas for Protos/Ethos Files

Design proposal for psyche review. Schema-first; bootstrap Rust readers
follow as future implementation work.

## 1. The Old Six-Slot Form (Contrast, Closed)

The dissolved `SixSlotEthosCodec` modeled every Ethos document as an ordered
product of six positional sections: (1) imports, (2) input (input-interface
declarations), (3) output (output-interface declarations), (4) types (the
only slot that carried content in practice), (5) generics, and (6) impls.
Five of six slots were empty in every shipped fixture. The psyche cut this
form on 2026-08-02: "We don't care about the old form. We never care about
the old form ... we're making a clean cut here. It's over." It is mentioned
here solely for contrast and is not a design input.

## 2. The Meta-Schema: What a File-Kind Schema Is

Per the same-form law (2026-08-01) and the header/imports/body ruling
(2026-08-02), every Ethos file is three positional objects. File kinds differ
only in the body's root type. One shared parsing machinery handles all kinds;
per-kind parsing code means the implementation failed.

The meta-schema (the type of a file) is therefore:

```
EthosFile.{
  Header.{EthosType Version}
  Imports.[ImportEntry]
  Body                          ;; root type determined by Header.EthosType
}
```

Where:

- `Header` is exactly two positions: the ethos type (file kind) and a
  SemVer-style version denoting the Ethos language version the content last
  worked with. The header is how the reader learns the body's root type.
- `Imports` is universal across file kinds, the second object. Imports are
  textual-form-only; encoded form addresses absolutely via encoded names.
- `Body` is the file-kind-specific root type. Its internal structure is the
  only thing a file-kind schema defines.

In textual surface form, the header renders as two atoms on the first line
(matching the current fixtures: `Interface.1`), imports as the second object,
body as the third.

### [agent-proposed] Meta-schema as a DOTOS declaration

```
EthosFileSchema.{
  kind EthosType
  headerVersion Version
  bodyRootType TypeDeclaration
}
```

This is the declaration a file-kind schema record would carry in a
schema-of-schemas registry. Open for psyche ruling.

## 3. Concrete Schema Proposals Per File Kind

Each file kind below shows: its body root type, position definitions, and a
full realistic example file in current syntax. The header and imports
structure is shared and shown once.

### Shared surface grammar

```
;; Line 1: header — EthosType.Version (dot-prefixed, two atoms)
;; Line 2: imports — [] vector of import entries
;; Line 3+: body — {} struct whose positions are defined by the file kind
```

Import entry syntax (from current fixtures):

```
[source.{ImportedName ImportedName} standalone.ImportedName]
```

### 3.1 interface.ethos

**Body root type: InterfaceBody**

Four positional sections (ruled 2026-08-02): inputs, outputs, refusals,
shared types. Membership in the input/output/refusal traits is positional and
never written. In a specialized file kind, declarations carry no kind tag.

```
InterfaceBody.{
  Inputs.[InputDeclaration]       ;; position 1
  Outputs.[OutputDeclaration]     ;; position 2
  Refusals.[RefusalDeclaration]   ;; position 3
  Types.[TypeDeclaration]         ;; position 4
}
```

Each input and output declaration is a named type: `Name.PayloadType`. Each
refusal is a named struct. Shared types are ordinary type declarations
(structs and enums).

**Full example (Spirit interface, current syntax):**

```ethos
Interface.1
[]
{
  [Record.Entry Observe.Query Register.ReferentRegistration]
  [Recorded.RecordIdentifier Observed.RecordSet Registered.ReferentIdentifier]
  [GuardianRejection.{GuardianReason Explanation} ReferentRejection.{GuardianReason Explanation}]
  [
    Topic.String
    Topics.Vector<Topic>
    Description.String
    Explanation.String
    Kind.[Decision Principle Correction Clarification Constraint]
    Magnitude.[Minimum VeryLow Low Medium High VeryHigh Maximum]
    Entry.{Topics Kind Description Magnitude}
    Query.{Topic Kind}
    RecordIdentifier.Integer
    RecordSet.Vector<Entry>
    Referent.String
    Aliases.Vector<String>
    ReferentRegistration.{Referent Aliases}
    ReferentIdentifier.Integer
    GuardianReason.[NotSpirit PrivateContent MeaningUnclear Duplicate]
    ObserverFilter.{Topics}
    ObservationEvent.{Topic RecordIdentifier}
    Observer.Stream.(ObserverFilter ObservationEvent)
    IntentFilter.{Query}
    IntentEvent.{Entry}
    Intent.Stream.(IntentFilter IntentEvent)
  ]
}
```

Notes on current syntax applied:
- `String` not `Text` (ruled 2026-08-05).
- `Vector<Topic>` uses shape angles `<>` (ruled 2026-08-05: shapes keep bare
  angles).
- `Stream.(Filter Event)` uses standalone transformer form (sectioned form
  cut 2026-08-04).
- No pipes, no commas. Positional throughout.

**[agent-proposed]** The `Stream.(Filter Event)` form follows the ruled
standalone transformer syntax `Name.Transformer.(payload)`. Whether stream
declarations belong in the types section or merit their own position is open.

**[agent-proposed]** Trait-requirement example using guillemets (not present
in the Spirit fixture but showing the ruled syntax):

```ethos
    Sorted.{Vector<«Ordered»>}
    Range.{<«Ordered»> <«Ordered»>}
```

Where `«Ordered»` marks a trait requirement inside a shape slot, and bare
same-trait mentions co-refer (one parameter, same-type enforced at
instantiation).

### 3.2 nexus.ethos

**Body root type: NexusBody**

The nexus declares the daemon's internal machinery spec: its behavior traits
and the types those traits' method signatures reference (ruled 2026-08-02).
The old file-level input/output idea is demoted; in/out is real per method
and lives in signatures, not in file sections.

The current fixture has two sections: types and traits. In a nexus file,
declarations carry no kind tag; the file type supplies it.

**[agent-proposed] Body structure: two positions.**

```
NexusBody.{
  Types.[TypeDeclaration]         ;; position 1: types referenced by traits
  Traits.[TraitDeclaration]       ;; position 2: behavior trait definitions
}
```

Each trait declaration carries method signatures:
`TraitName.{method.{Params... Return} method.{Params... Return}}` where the
last position of each method is the return type, the receiver is implied by
trait membership.

**Full example (Spirit nexus, current syntax):**

```ethos
Nexus.1
[interface.{Entry Referent RecordSet GuardianReason}]
{
  [
    AdmissionDecision.[Accepted Rejected.GuardianReason]
    GuardianDecision.[Admit Refuse.GuardianReason]
  ]
  [
    SignalAdmission.{admit.{Entry AdmissionDecision}
                     recordDecision.{AdmissionDecision Unit}}
    AgentGuardian.{guard.{Entry RecordSet GuardianDecision}
                   guardReferent.{Referent RecordSet GuardianDecision}}
  ]
}
```

Notes:
- Trait declarations carry method signatures inline. The no-tag ruling means
  `SignalAdmission` is known to be a trait by its position in the traits
  section, not by a keyword.
- Method signatures follow the ruled convention: `method.{Params... Return}`,
  last position is the return type.

**[agent-proposed]** Whether traits should carry trait-requirement annotations
on their own type parameters (e.g. a trait whose methods are generic) is not
shown in the Spirit fixture and remains open. The syntax would follow the
guillemet ruling: `«Ordered»` in a method's type positions.

**[agent-proposed]** Whether the nexus body needs more than two positions
(e.g. a section for constants, configuration types, or lifecycle hooks) is
open. The current two-position structure covers Spirit's needs.

### 3.3 sema.ethos

**Body root type: SemaBody**

The per-component database specification. Record types define what is stored;
tables define the keyed collections. This is the basis for the eventual
database evolution engine (ruled 2026-08-02): diffing two encoded schema
versions produces migration code.

**[agent-proposed] Body structure: two positions.**

```
SemaBody.{
  RecordTypes.[TypeDeclaration]   ;; position 1: storable record types
  Tables.[TableDeclaration]       ;; position 2: keyed table definitions
}
```

Each table declaration is `tableName.{RecordType KeyType}`.

**Full example (Spirit sema, current syntax):**

```ethos
Sema.1
[interface.{Entry Referent Aliases RecordIdentifier} signal-domain.Domain]
{
  [
    StoredRecord.{RecordIdentifier Entry}
    StoredReferent.{Referent Aliases}
    SourceSchemaVersion.Integer
    MigratedRecordCount.Integer
    MigratedReferentCount.Integer
    Migration.{SourceSchemaVersion MigratedRecordCount MigratedReferentCount}
  ]
  [
    records.{StoredRecord Domain}
    referents.{StoredReferent Domain}
    migrations.{Migration Domain}
  ]
}
```

Notes:
- Table names are lowercase (convention from current fixture), record types
  are uppercase.
- `Domain` is imported from `signal-domain`, showing cross-component type
  sharing via imports.

**[agent-proposed]** Table declarations use a two-position struct:
`tableName.{RecordType KeyType}`. Whether additional positions are needed
(e.g. index declarations, uniqueness constraints) is open and ties into the
database evolution engine's requirements. Minimal for now.

**[agent-proposed]** Whether the sema body needs a third position for
migration policy declarations (e.g. specifying which fields are
one-way-fold-safe versus requiring LLM-assisted ambiguity resolution) is
open.

## 4. Whether More File Kinds Are Needed

The psyche named three file kinds: interface, nexus, sema. The
ethosFileStructureCleanCut ruling also floated a "design/traits file kind"
as "really useful for when designing." Current fixtures show exactly these
three kinds; no other `.ethos` files exist anywhere in the corpus.

Arguments from what components actually need:

**Trait-definition file kind (trait.ethos)** [agent-proposed, moderate
confidence]: the psyche's own words point to this: "a design/traits file
kind" (2026-08-02). Currently, traits live inside nexus files. A dedicated
trait file kind would let shared traits (like `Ordered`, `Sortable`,
`Iterable`) be defined once and imported by any component, rather than being
re-declared in each nexus. The body root type would be a single position:
trait declarations.

```
TraitBody.{
  Traits.[TraitDeclaration]
}
```

This aligns with the psyche's vision that "traits are the code ontology" and
the target of 100% of impls living under a trait. Shared, cross-component
traits need a home.

**Configuration/constants file kind** [agent-proposed, low confidence]:
components need configuration schemas (timeouts, limits, feature gates).
These could live as types in the interface or nexus, or they could warrant
their own file kind. No current fixture suggests this; the psyche has not
mentioned it. Lean: not needed yet.

**Event-log/changelog file kind** [agent-proposed, low confidence]: the
identity scheme (2026-08-05) mentions "the change log records every
association." Whether the change log's schema is itself an Ethos file kind
or a Sema concern is unclear. Lean: it is a Sema concern, not a separate
file kind.

Recommendation: the trait file kind deserves a psyche ruling. The others do
not rise to the level of proposal.

## 5. Bootstrap Rust Reader Strategy

Per the same-form law, the Rust reader surface is minimal. The strategy:

**One shared positional decoding machinery.** The parser reads the universal
three-object structure (header, imports, body) using a single code path. The
header's ethos-type field selects the body's root type. The parser then
hands the body to the same expected-type-at-position machinery that handles
all type declarations.

**Per-file-kind root types only.** Each file kind contributes exactly one
root type definition to the Rust side. Per the strict-types ruling
(2026-08-04), these are purpose-designed types, not generic containers:

```rust
/// interface.ethos body
struct InterfaceBody {
    inputs: InputDeclarations,
    outputs: OutputDeclarations,
    refusals: RefusalDeclarations,
    types: TypeDeclarations,
}

/// nexus.ethos body
struct NexusBody {
    types: TypeDeclarations,
    traits: TraitDeclarations,
}

/// sema.ethos body
struct SemaBody {
    record_types: TypeDeclarations,
    tables: TableDeclarations,
}
```

**Minimal hand-written Rust surface:**

1. The shared positional decoder (header parse, imports parse, body
   dispatch). This is the only substantial hand-written code. It walks the
   name-tree and structure-tree, resolves positions against expected types,
   and produces the encoded form. This machinery already exists in
   `core-ethos` and is being redesigned.

2. Per-file-kind root type definitions (3 structs, shown above). Each is a
   simple trait implementation that tells the shared machinery what types to
   expect at each position. Adding a new file kind costs one struct and one
   trait impl.

3. The `WholeEthosFileKind` enum (already exists: `Interface`, `Nexus`,
   `Sema`). The header parser maps the ethos-type atom to this enum, which
   selects the body root type.

**[agent-proposed]** The trait each root type implements could be:

```rust
trait FileKindBody: Sized {
    fn position_types() -> &'static [PositionExpectation];
    fn from_positions(positions: Vec<DecodedPosition>) -> Result<Self, DecodeError>;
}
```

This keeps the failure criterion satisfied: no per-kind parsing code, only
per-kind type definitions that the shared machinery consumes.

## 6. Open Questions

**Q1. Trait file kind.** The psyche floated a "design/traits file kind" on
2026-08-02 but never ruled it. Should trait.ethos exist as a fourth file
kind for shared, cross-component trait definitions?

**Q2. Sema table declaration shape.** Is `tableName.{RecordType KeyType}`
sufficient, or do tables need additional positions for index declarations,
uniqueness constraints, or migration policy hints that feed the database
evolution engine?

**Q3. Nexus body completeness.** Is the two-position nexus body
(types + traits) sufficient for all daemon machinery, or do components need
additional positions for lifecycle declarations, configuration schemas, or
internal state specifications?

**Q4. Stream declarations.** Stream types currently live in the interface
types section as `Observer.Stream.(Filter Event)`. Should streams have a
dedicated position in the interface body, or is the types section the
correct home?

**Q5. Header extensibility.** The header is ruled as "just those two things
for now." The psyche floated an ancestor-reference hash in the header
(2026-08-02, explicitly not pushed). When and how does the header grow?

**Q6. Version semantics.** The header version is "SemVer-style,
writer-bumped when a change could break." Does this version the Ethos
language dialect, the file's content schema, or both? A bumping standard is
pending.

**Q7. Guillemet trait-requirement representation in the body schema.** The
examples show `«Ordered»` inline in type positions. Does the file-kind
schema need to declare which traits are available for requirement, or is
that purely a resolution/typing concern outside the file schema?

**Q8. Import syntax formalization.** Imports use
`source.{Name Name}` for multi-import and `source.Name` for single import
in the current fixtures. Is this the ruled form, or should the schema
proposal formalize it?
