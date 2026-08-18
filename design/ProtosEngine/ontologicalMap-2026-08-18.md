# Ontological Map of Protos, Datom, Ethos-Monolith

Study ordered by the psyche 2026-08-18: "Do an ontological study of the
code, and create the most unified map of traits and types you can."

## 1. Method Census

Across all types in the three crates, the following method roles recur.
Counts are types carrying that role (not method count).

| Method Role | protos | datom | ethos | Total | Types (examples) |
|---|---|---|---|---|---|
| **`new` (constructor under trait)** | 0 | 0 | 4 | 4 | CargoEthosSourceMetadata, GeneratedArtifact, ComponentGeneration, GeneratedComponent |
| **Field getters (under trait)** | 10 | 3 | 5 | 18 | WalkFrame, FrameIdentity, WalkTransition, WalkObservation, DatomEvidence, Realized\<T\>, GeneratedArtifact, ComponentGeneration |
| **protos::Realize** | 1 | 2 | 1 | 4 | SourceText, ReportText, InterimNoteText, InterfaceText |
| **protos::Textualize** | 1 | 2 | 1 | 4 | Block, Report, InterimNote, Interface |
| **Dialect block realize** | 0 | 10 | 13 | 23 | Text, Entry, Group, Report, InterimNote, Import, InputElement, TypeElement... |
| **Dialect block textualize** | 0 | 10 | 13 | 23 | same types as above |
| **ShapeDefined (shapes/select)** | 0 | 10 | 16 | 26 | Text, Entry, Group, Report, Interface, Inputs, TypeElement, EnumVariantElement... |
| **Evidenced realize** | 0 | 2 | 1 | 3 | ReportText, InterimNoteText, InterfaceText |
| **Evidenced textualize** | 0 | 2 | 1 | 3 | Report, InterimNote, Interface |
| **Evidence/observation access** | 8 | 3 | 2 | 13 | StructuralWalk, RealizeWalk, WalkFrame, DatomEvidence, RealizedInterface |
| **Walk lifecycle (enter/close/position/resume)** | 3 | 0 | 0 | 3 | StructuralWalk, RealizeWalk, TextualizeWalk |
| **write_rust** | 0 | 0 | 7 | 7 | InputElement, OutputElement, NamedTypedef, NamedStruct, NamedEnum... |
| **validate** | 0 | 0 | 1 | 1 | Interface |
| **Fault conversion (From\<WalkFault\>)** | 0 | 1 | 1 | 2 | DatomFault, InterfaceFault |

**Dominant pattern**: ShapeDefined (26 types), dialect block realize/textualize (23 types each), field getters (18 types), evidence/observation (13 types).

**The `new` case**: The psyche flagged "the new method is another interesting case." All 4 `new` methods live in ethos-monolith's *Operations traits (CargoEthosSourceMetadataOperations, GeneratedArtifactOperations, ComponentGenerationOperations, GeneratedComponentOperations). Each trait bundles `new` with the type's other methods (getters, operations). No `new` appears under a trait anywhere in protos or datom.

## 2. Ontological Grouping

| Group | What it is | Deserves a trait? |
|---|---|---|
| **A. Constructing** (`new`) | Building an instance from arguments. | Open question. A constructor is not a capability of the built thing. If fields are private, encapsulation justifies a method, but the trait adds nothing beyond the type name. Construction could live on the type without a trait. The 4 ethos types bundle `new` with other operations in one trait -- the `new` is justified only because the trait already exists for the operations. |
| **B. Disclosing data** (field getters) | Read-only access to a type's data. | Under mandatory traits (psyche Intent), any method call needs a trait. But if a type's fields were public, access would be a field read, not a method call, and no trait would be needed. For immutable evidence records (WalkFrame, DatomEvidence, etc.), public fields would eliminate the getter trait entirely. |
| **C. Realize/Textualize** (protos-level) | The two directional traits converting between textual and real forms. | Yes. Psyche-ruled: "no umbrella over Realize/Textualize." Two separate traits. |
| **D. Dialect block realize/textualize** | Per-block transcription in a dialect's parsing context. | Yes, but the two directions are always co-implemented (10 datom types, 13 ethos types). One dialect-level trait per type may suffice. |
| **E. ShapeDefined** (shapes/select) | Textual shape discrimination. | Yes. Psyche-ruled: "ShapeDefined stays." Discrimination only; the type owns its own realization. |
| **F. Evidenced realize/textualize** | Realize/textualize that returns walk transition evidence alongside the value. | Yes. The pattern is identical in datom and ethos -- duplicated, candidate for protos universalization. |
| **G. Evidence/observation access** | Read-only access to walk facts, cursors, transition history. | Yes per mandatory traits, but each observation trait has exactly one implementing type. Not fragmented type-side. Could be replaced by public fields on the evidence records. |
| **H. Walk lifecycle** | Structural frame enter/close/position/resume. | Yes. One shared discipline, three implementing drivers. |
| **I. Rust projection** (write_rust) | Emit Rust source from a realized type. | Yes. Ethos-only. 7 types share the trait; genuinely different from textualize (which emits Ethos text, not Rust). |
| **J. Validation** (validate) | Check semantic invariants on a realized type. | Yes, but currently single-implementor (Interface). The concept may recur as datom gains record types. |
| **K. Scanner/walk internals** (private) | Delimiter scanning, frame finishing, history recording. | Traits are required (mandatory traits), but fragmented. StructuralWalk carries 5 single-method private traits; BlockScanner carries 3. These are the prime fragmentation cases per psyche ruling: "if one type implements a bunch of single function traits then all those traits are probably only one trait." |

## 3. The Unified Map

### 3A. Type Taxonomy

| Category | protos | datom | ethos-monolith |
|---|---|---|---|
| **Data (values)** | Head, SourceText, StringCarrier, Block, Shape, WalkFault | Text, TagList, Entry, Group, Report, InterimNote, DatomFault | Version, Interface, Imports, Import, Inputs/Outputs/Refusals/Streams, Input/Output/Refusal/StreamElement, Types, TypeElement, NamedTypedef/NamedStruct/NamedEnum, EnumVariantElement, InterfaceFault |
| **Textual forms** | SourceText (dual role) | ReportText, InterimNoteText | InterfaceText |
| **Drivers/engines/scopes** | BlockScanner, StructuralWalk, RealizeWalk, TextualizeWalk, RealizeScope, TextualizeScope | -- | -- |
| **Evidence/instrumentation** | WalkFrame, FrameIdentity, ParentObservation, WalkTransition, WalkObservation | DatomEvidence, Realized\<T\>, Projected\<T\> | InterfaceEvidence, RealizedInterface, ProjectedInterface |
| **Build/generation** | -- | -- | CargoEthosSourceMetadata, GeneratedArtifact, ComponentGeneration, GeneratedComponent, BuildError |

### 3B. Minimal Trait Set

**Protos (universal substrate) -- currently 30 traits -> proposed 22**

| Trait | Methods | Implementors | Status |
|---|---|---|---|
| `Realize` | realize | SourceText + dialect textual forms | **Psyche-ruled stay** |
| `Textualize` | textualize | Block + dialect real types | **Psyche-ruled stay** |
| `ShapeDefined` | shapes, select | 26 dialect data types | **Psyche-ruled stay** |
| `Walk` | enter, close, position, resume | StructuralWalk, RealizeWalk, TextualizeWalk | **Psyche-ruled stay** |
| `WalkObserving` | observation | 3 walk types | Stay (shared) |
| `CursorObserving` | cursor | RealizeWalk, TextualizeWalk | Stay (shared) |
| `RealizeDriving` | realize_blocks, realize_source | RealizeWalk | Stay |
| `TextualizeDriving` | textualize_blocks, textualize_source, textual_source | TextualizeWalk | Stay |
| `RealizeScoping` | realize_body | RealizeScope | Stay |
| `TextualizeScoping` | textualize_block, emit_scalar | TextualizeScope | Stay |
| `BlockScanning` | blocks | SourceText | Stay |
| `Headed` | head | Block | Stay (used as trait bound) |
| `StringCarrying` | textual_body | StringCarrier | Stay |
| `SourceSlicing` | source_slice | SourceText | Stay |
| `FrameObserving` | identity, shape, position, span | WalkFrame | Stay (single-type, not fragmented) |
| `IdentityObserving` | ordinal | FrameIdentity | Stay (same) |
| `ParentObserving` | frame, position | ParentObservation | Stay (same) |
| `TransitionObserving` | ordinal, kind, frame, parent_before, parent_after | WalkTransition | Stay (same) |
| `ObservationViewing` | depth, resumptions, last_closed, faulted, history | WalkObservation | Stay (same) |
| `DriverFailing` (priv) | fail, is_faulted | RealizeWalk, TextualizeWalk | Stay (shared private) |
| <<WalkMachinery>> (priv) | finish, abort, finish_faulted, reset_history, parent_observation, record_transition | StructuralWalk | **Fused from 5 private traits** |
| <<BlockScannerMachinery>> (priv) | scan, require_delimited_prefix, parenthesized, curly_quoted, structural | BlockScanner | **Fused from 3 private traits** |

Vanish: BlockRendering (absorbed into Textualize impl for Block), ShapeHeading (inlined), FrameFinishing, WalkAborting, FaultFinishing, HistoryResetting, TransitionRecording (into <<WalkMachinery>>), Scanning, PrefixChecking, DelimiterScanning (into <<BlockScannerMachinery>>).

**Protos -- proposed new universal traits (lifted from dialect duplication)**

| Trait | Methods | Currently duplicated as | Implementors |
|---|---|---|---|
| <<WalkEvidence>> | observation, cursor | datom::EvidenceObserving, ethos (field access) | DatomEvidence, InterfaceEvidence (identical structs) |
| <<RealizedViewing\<V, E\>>> | value, evidence | datom::RealizationViewing, ethos::InterfaceRealizationViewing | Realized\<T\>, RealizedInterface |
| <<ProjectedViewing\<T, E\>>> | text, evidence | datom::ProjectionViewing, ethos::InterfaceProjectionViewing | Projected\<T\>, ProjectedInterface |
| <<EvidencedRealizing>> | realize_evidenced | datom::EvidencedRealizing, ethos::InterfaceEvidencedRealizing | ReportText, InterimNoteText, InterfaceText |
| <<EvidencedTextualizing>> | textualize_evidenced | datom::EvidencedTextualizing, ethos::InterfaceEvidencedTextualizing | Report, InterimNote, Interface |

These 5 traits replace 10 dialect-level traits (5 datom + 5 ethos). DatomEvidence and InterfaceEvidence are structurally identical ({observation: WalkObservation, cursor: usize}) and could become one protos type.

**Datom -- currently 16 own traits -> proposed 9**

| Trait | Methods | Status |
|---|---|---|
| <<DatomBlockTranscribing>> (priv) | realize_block, textualize_in | **Fused from DatomRealizing + DatomTextualizing** (10 types, always co-impl) |
| TagPayloading (priv) | realize_tag_payload, textualize_tag_payload | Stay |
| GroupPayloading (priv) | realize_group_payload, textualize_group_payload | Stay |
| CarrierRealizing (priv) | text | Stay (on protos StringCarrier) |
| <<TextProjecting>> (priv) | fits_bare, parenthesized_body | **Fused from BareProjecting + ParenthesisProjecting** (both on Text) |
| HeadReading (priv) | text | Stay (on protos Head) |
| PairDividing (priv) | divide | Stay (on protos Block) |
| MapKeyChecking (priv) | group_key, text_key | Stay (on String) |
| PositionAdvancing (priv) | next | Stay |

Vanish to protos: EvidenceObserving, RealizationViewing, ProjectionViewing, EvidencedRealizing, EvidencedTextualizing (5 traits -> protos universals).
Vanish by fusion: DatomRealizing, DatomTextualizing (-> <<DatomBlockTranscribing>>); BareProjecting, ParenthesisProjecting (-> <<TextProjecting>>).

**Ethos-Monolith -- currently 29 own traits -> proposed 20**

| Trait | Methods | Status |
|---|---|---|
| CargoEthosSourceMetadataOperations | new + 4 methods | Stay (absorb LinksNameNormalizing) |
| GeneratedArtifactOperations | new + 5 methods | Stay (absorb GeneratedArtifactComparison) |
| ComponentGenerationOperations | new + 8 methods | Stay |
| GeneratedComponentOperations | new + 4 methods | Stay |
| RustArtifactProjecting | rust_source, rust_artifact | Stay |
| OperationElementReading (priv) | realize_operation, textualize_operation | Stay (4 impl types) |
| <<SectionTranscribing>> (priv) | realize_section, textualize_section | **Fused from SectionReading + SectionWriting** (5 types) |
| TypeElementReading (priv) | realize_type, textualize_type | Stay |
| EnumVariantReading (priv) | realize_variant, textualize_variant | Stay |
| VersionReading (priv) | read_header, write_header | Stay |
| ImportReading (priv) | realize_import, textualize_import | Stay |
| InterfaceDocumentReading (priv) | realize_root_block, finish | Stay (on InterfaceState) |
| InterfaceDocumentWriting (priv) | textualize_document | Stay (on Interface) |
| InterfaceValidation (priv) | validate | Stay |
| SectionsReading (priv) | realize_sections | Stay |
| SymbolReading (priv) | symbol, bare_value, bare_symbol, head_symbol | Stay |
| RustTypeWriting (priv) | write_rust | Stay (7 types) |
| RustNameWriting (priv) | rust_type_name, rust_field_name | Stay |

Vanish entirely: InputContext, OutputContext, RefusalContext, StreamContext (pure delegation; the types are the context).
Vanish by absorption: LinksNameNormalizing (into CargoEthosSourceMetadataOperations), GeneratedArtifactComparison (into GeneratedArtifactOperations).
Vanish to protos: InterfaceRealizationViewing, InterfaceProjectionViewing, InterfaceEvidencedRealizing, InterfaceEvidencedTextualizing (4 traits -> protos universals).
Vanish by fusion: SectionReading + SectionWriting -> <<SectionTranscribing>>.

### 3C. Summary

| Crate | Current traits | Proposed | Change |
|---|---|---|---|
| protos | 30 | 27 (22 kept/fused + 5 new universal) | +5 universal, -8 fragmented |
| datom | 16 | 9 | -7 (5 to protos, 4 fused, 2 new fused) |
| ethos | 29 | 20 | -9 (4 vanish, 4 to protos, 3 fused/absorbed) |
| **Total** | **75** | **56** | **-19** |

### 3D. Compact Tree

```
protos (universal substrate)
  Psyche-ruled (immovable)
    Realize, Textualize, ShapeDefined, Walk
  Walk infrastructure
    WalkObserving, CursorObserving
    RealizeDriving, TextualizeDriving
    RealizeScoping, TextualizeScoping
    <<WalkMachinery>> (fused private)
    DriverFailing (shared private)
  Block infrastructure
    Headed, BlockScanning, StringCarrying, SourceSlicing
    <<BlockScannerMachinery>> (fused private)
  Evidence (universal, lifted from dialects)
    <<WalkEvidence>>
    <<RealizedViewing>>, <<ProjectedViewing>>
    <<EvidencedRealizing>>, <<EvidencedTextualizing>>
  Observation (per-type, not fragmented)
    FrameObserving, IdentityObserving, ParentObserving
    TransitionObserving, ObservationViewing

datom (pure positional typed data)
  protos impls: ShapeDefined(10), Realize(2), Textualize(2)
  <<DatomBlockTranscribing>> (fused, 10 types)
  TagPayloading, GroupPayloading
  <<TextProjecting>> (fused)
  Helpers: CarrierRealizing, HeadReading, PairDividing,
           MapKeyChecking, PositionAdvancing

ethos-monolith (Ethos->Rust generator)
  protos impls: ShapeDefined(16), Realize(1), Textualize(1)
  Build types: CargoEthosSourceMetadataOperations,
    GeneratedArtifactOperations, ComponentGenerationOperations,
    GeneratedComponentOperations
  RustArtifactProjecting, RustTypeWriting, RustNameWriting
  Dialect parsing: OperationElementReading(4 types),
    <<SectionTranscribing>>(5 types, fused),
    TypeElementReading, EnumVariantReading,
    VersionReading, ImportReading
  Interface lifecycle: InterfaceDocumentReading,
    InterfaceDocumentWriting, InterfaceValidation,
    SectionsReading
  Helpers: SymbolReading
```

## 4. Rulings, Proposals, and Open Questions

**Psyche-ruled (with reference):**
- protos::Realize and protos::Textualize stay as two directional traits, no umbrella (traitsAsCapabilities.md 2026-08-14: "none of this makes sense if we use a trait for each direction")
- ShapeDefined stays (traitsAsCapabilities.md 2026-08-14: "ShapeDefined is good")
- Walk stays (traitsAsCapabilities.md 2026-08-14: "fine. im not crazy about it but its good enough")
- Every method call lives under a trait (mandatoryTraits.md 2026-08-13)
- Different section fields are different types (signalIsOurMessagingLayer.md 2026-08-14: "Because they're different things")
- Sharing is trait-borne; universal stuff in protos (threeStacks.md 2026-08-14: "I want universal stuff in protos")
- Fragmentation rule: "if one type implements a bunch of single function traits then all those traits are probably only one trait" (rustComponentArchitecture.md 2026-08-17)

**Proposal (agent-authored, not ruled):**
- Fuse StructuralWalk's 5 private traits into one; fuse BlockScanner's 3 private traits into one
- Absorb BlockRendering into Block's Textualize impl (it only serves textualize)
- Lift the evidence/evidenced-realize/evidenced-textualize pattern to protos (identical struct in datom and ethos; identical trait shape)
- Fuse DatomRealizing + DatomTextualizing (always co-implemented, 10 types)
- Remove the 4 context delegation traits in ethos (InputContext, OutputContext, RefusalContext, StreamContext) -- the types themselves are the context
- Fuse SectionReading + SectionWriting (always co-implemented, 5 types)

**Open questions for the psyche (5):**

1. Should `new` live under a trait (as in ethos-monolith's *Operations traits), or should construction stay at the type level as a struct literal or non-trait method?
2. Should read-only evidence records (WalkFrame, DatomEvidence, etc.) expose public fields instead of private fields behind getter traits, given that field access is not a method call and therefore needs no trait?
3. At the dialect level, should the realize/textualize block pair (DatomRealizing + DatomTextualizing) be one trait or two, given they are always co-implemented on every type?
4. Should the evidence pattern (DatomEvidence/InterfaceEvidence, Realized/RealizedInterface, EvidencedRealizing/InterfaceEvidencedRealizing) be lifted to protos as universal generic traits, since the structs and trait shapes are identical across dialects?
5. Should the four section-context delegation traits (InputContext, OutputContext, RefusalContext, StreamContext) remain as explicit "each section has its own parsing context" markers, or are the distinct section types themselves sufficient context?
