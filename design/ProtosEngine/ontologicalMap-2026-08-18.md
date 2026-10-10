# Ontological Map of Protos, Datom, Ethos-Monolith

Study ordered by the psyche 2026-08-18: "Do an ontological study of the
code, and create the most unified map of traits and types you can."
Revised with software-ontology research (BWW, OntoClean/UFO, Cook, DCI,
Fowler, ISP, Evans, Hickey, Rendel-Ostermann, AOP). Principles P1-P10.

## 1. Type Taxonomy (types first -- psyche ruling 2026-08-13; P10)

| UFO Category | protos | datom | ethos-monolith |
|---|---|---|---|
| **Kinds (values)** | Head, SourceText, StringCarrier, Block, Shape, WalkFault | Text, TagList, Entry, Group, Report, InterimNote, DatomFault | Version, Interface, Import(s), Input/Output/Refusal/StreamElement, Inputs/Outputs/Refusals/Streams, Types, TypeElement, NamedTypedef/Struct/Enum, EnumVariantElement, InterfaceFault, CargoEthosSourceMetadata, GeneratedArtifact, ComponentGeneration, GeneratedComponent, BuildError |
| **Textual-form Roles** | SourceText (dual) | ReportText, InterimNoteText | InterfaceText |
| **Contexts (drivers/scopes)** | BlockScanner, StructuralWalk, RealizeWalk, TextualizeWalk, RealizeScope, TextualizeScope | -- | -- |
| **Modes (evidence)** | WalkFrame, FrameIdentity, ParentObservation, WalkTransition, WalkObservation | ~~DatomEvidence, Realized\<T\>, Projected\<T\>~~ | ~~InterfaceEvidence, RealizedInterface, ProjectedInterface~~ |

Struck-through dialect Mode types vanish (4C).

## 2. Method Census

| Role | p | d | e | Tot | Note |
|---|---|---|---|---|---|
| `new` under trait | 0 | 0 | 4 | 4 | ethos only; dissolve (4B) |
| Field getters under trait | 10 | 3 | 5 | 18 | values -> pub fields (4B) |
| protos::Realize | 1 | 2 | 1 | 4 | psyche-ruled stay |
| protos::Textualize | 1 | 2 | 1 | 4 | psyche-ruled stay |
| **Scoped block realize** | 0 | 10 | 13 | **23** | universal protos (4A) |
| **Scoped block textualize** | 0 | 10 | 13 | **23** | universal protos (4A) |
| ShapeDefined | 0 | 10 | 16 | 26 | psyche-ruled stay |
| Evidenced realize/textualize | 0 | 4 | 2 | 6 | vanish (4C) |
| Evidence/observation access | 8 | 3 | 2 | 13 | dialect part vanishes (4C) |
| Walk lifecycle | 3 | 0 | 0 | 3 | psyche-ruled stay |
| write_rust | 0 | 0 | 7 | 7 | stays (P5) |
| validate | 0 | 0 | 1 | 1 | stays (P8) |

## 3. Ontological Grouping

| Group | UFO | Principle | Trait? |
|---|---|---|---|
| **Constructing** | Kind event | P1: Kinds own construction | No. Struct literal. Operations traits are Header Interfaces (Fowler); dissolve (4B) |
| **Field getters** | Kind Quality | P1, Hickey | No on values. Pub fields; field access is not a method call (4B) |
| **Realize/Textualize** | Role pair | P4 | Psyche-ruled: two traits, no umbrella |
| **Scoped block pair** | Role pair | P4, Rendel-Ostermann isomorphism | One universal protos capability replacing ~17 dialect traits. One-vs-two open (4A) |
| **ShapeDefined** | Kind/Phase | P6 | Psyche-ruled stay |
| **Evidence** | Mode | P9, AOP | Dialect apparatus vanishes. Caller asks walk (4C) |
| **Walk** | Context | P7 | Psyche-ruled stay |
| **Rust projection** | Role | P5: lossy, one-directional | Stays (ethos-only) |
| **Validation** | Role | P8: predicate, context-specific | Stays |
| **Scanner/walk internals** | Kind | fragmentation ruling | Fuse |

## 4. The Unified Map

### 4A. Scoped block pair: universal protos capability

`realize_block(scope, block) -> Result<Self, Fault>` and
`textualize_in(&self, scope) -> Result<(), Fault>` recur on 23+ types.
Currently ~17 dialect-local traits: DatomRealizing, DatomTextualizing,
TagPayloading, GroupPayloading (datom); OperationElementReading,
Input/Output/Refusal/StreamContext, SectionReading, SectionWriting,
TypeElementReading, EnumVariantReading, VersionReading, ImportReading,
InterfaceDocumentWriting, SectionsReading (ethos). All fold into protos.

Round-trip verified by tests. Rendel-Ostermann isomorphism criterion
argues ONE trait. Psyche precedent (Realize/Textualize) argues TWO.
Count uses two (conservative):

| Protos trait (placeholder) | Implementors |
|---|---|
| <<BlockRealizing>> | 23+ types across datom and ethos |
| <<BlockTextualizing>> | same 23+ types |

### 4B. Operations dissolution (P1, Fowler, Hickey)

The 4 ethos *Operations traits are Header Interfaces (Fowler): they
mirror the whole type. Constructor is a Kind origin event (P1), not a
capability. Immutable values expose data via pub fields (Hickey), not
getter methods. Field access is not a method call, so mandatory traits
("every method call lives under a trait") is honored by elimination.

`new` -> struct literal. Getters -> pub fields. Real capabilities
extracted into Role traits:

| Role trait (placeholder) | Methods | From |
|---|---|---|
| <<ArtifactFreshness>> | assert_matches_existing, write_to, pending_path | GeneratedArtifactOps + Comparison |
| <<CargoSourcePublishing>> | publish, dependency_source_dir, emit_rerun | CargoEthosSourceMetadataOps + LinksNameNorm |
| <<PathDeriving>> | 6 path join methods | ComponentGenerationOps |

GeneratedComponentOps::assert_all_match_existing: with pub fields,
caller invokes <<ArtifactFreshness>> on each artifact directly.

### 4C. Evidence elimination (P9, AOP, UFO Mode)

Evidence is a cross-cutting Mode on the Context (UFO), never inside
domain traits (AOP). Walk drivers already expose it: WalkObserving::
observation(), CursorObserving::cursor(). Caller asks the walk after
the operation. No wrapper types or evidenced-* traits needed.

Vanish: 9 traits (EvidenceObserving, RealizationViewing\<T\>,
ProjectionViewing\<T\>, EvidencedRealizing, EvidencedTextualizing from
datom; InterfaceRealizationViewing, InterfaceProjectionViewing,
InterfaceEvidencedRealizing, InterfaceEvidencedTextualizing from ethos).
6 types vanish with them (DatomEvidence, Realized\<T\>, Projected\<T\>,
InterfaceEvidence, RealizedInterface, ProjectedInterface).

### 4D. Protos gaps (P1)

datom's CarrierRealizing (unescape on protos::StringCarrier) is a protos
gap -- string carriers are psyche-ruled protos substrate. Move: expand
StringCarrying with `unescaped_text()`. HeadReading vanishes; Head.0 is
pub, field access suffices.

### 4E. Full trait table

**Protos -- 30 -> 24**

| Trait | Methods | Types | Status |
|---|---|---|---|
| Realize | realize | 4 | Psyche-ruled |
| Textualize | textualize | 4 | Psyche-ruled |
| ShapeDefined | shapes, select | 26 | Psyche-ruled |
| Walk | enter, close, position, resume | 3 | Psyche-ruled |
| WalkObserving | observation | 3 | Stay |
| CursorObserving | cursor | 2 | Stay |
| RealizeDriving | realize_blocks, realize_source | 1 | Stay |
| TextualizeDriving | textualize_blocks, textualize_source, textual_source | 1 | Stay |
| RealizeScoping | realize_body | 1 | Stay |
| TextualizeScoping | textualize_block, emit_scalar | 1 | Stay |
| BlockScanning | blocks | 1 | Stay |
| Headed | head | 1 | Stay |
| StringCarrying | textual_body, unescaped_text | 1 | Expanded (absorb CarrierRealizing) |
| SourceSlicing | source_slice | 1 | Stay |
| FrameObserving | identity, shape, position, span | 1 | Stay (open: pub fields?) |
| IdentityObserving | ordinal | 1 | Stay (same open) |
| ParentObserving | frame, position | 1 | Stay (same open) |
| TransitionObserving | 5 methods | 1 | Stay (same open) |
| ObservationViewing | 5 methods | 1 | Stay (same open) |
| DriverFailing (priv) | fail, is_faulted | 2 | Stay |
| <<WalkMachinery>> (priv) | 6 methods | 1 | Fused from 5 |
| <<BlockScannerMachinery>> (priv) | 5 methods | 1 | Fused from 3 |
| <<BlockRealizing>> | realize_block | 23+ | New universal |
| <<BlockTextualizing>> | textualize_in | 23+ | New universal |

Vanish (10): BlockRendering, ShapeHeading, FrameFinishing, WalkAborting,
FaultFinishing, HistoryResetting, TransitionRecording, Scanning,
PrefixChecking, DelimiterScanning.

**Datom -- 16 -> 4**

| Trait | Status |
|---|---|
| <<TextProjecting>> (priv) | Fused: BareProjecting + ParenthesisProjecting |
| PairDividing (priv) | Stay (datom Block semantics) |
| MapKeyChecking (priv) | Stay |
| PositionAdvancing (priv) | Stay |

Vanish (12): DatomRealizing, DatomTextualizing, TagPayloading,
GroupPayloading -> protos universal. EvidenceObserving, RealizationViewing,
ProjectionViewing, EvidencedRealizing, EvidencedTextualizing -> evidence
elimination. CarrierRealizing -> protos StringCarrying. HeadReading -> pub
field. BareProjecting + ParenthesisProjecting -> fused.

**Ethos-monolith -- 29 -> 9**

| Trait | Status |
|---|---|
| <<ArtifactFreshness>> | New Role (from dissolved Operations) |
| <<CargoSourcePublishing>> | New Role (from dissolved Operations) |
| <<PathDeriving>> | New Role (from dissolved Operations) |
| RustArtifactProjecting | Stay (P5) |
| InterfaceValidation (priv) | Stay (P8) |
| InterfaceDocumentReading (priv) | Stay (parser state) |
| SymbolReading (priv) | Stay |
| RustTypeWriting (priv) | Stay (7 types) |
| RustNameWriting (priv) | Stay |

Vanish (20): 9 to protos universal, 4 delegation, 4 evidence,
6 dissolved/absorbed Operations. 3 new Roles replace real capabilities.

### 4F. Summary

| Crate | Current | Proposed | Change |
|---|---|---|---|
| protos | 30 | 24 | -10 fragmented, +2 fused, +2 universal |
| datom | 16 | 4 | -12 (to protos / evidence / fusion) |
| ethos | 29 | 9 | -23 + 3 new Roles |
| **Total** | **75** | **37** | **-38** |

### 4G. Compact Tree

```
protos (universal substrate)
  Psyche-ruled: Realize, Textualize, ShapeDefined, Walk
  Scoped block pair (new, from dialects)
    <<BlockRealizing>>(23+), <<BlockTextualizing>>(23+)
  Walk: WalkObserving, CursorObserving, DriverFailing(priv)
    RealizeDriving, TextualizeDriving
    RealizeScoping, TextualizeScoping
    <<WalkMachinery>>(priv fused)
  Block: Headed, BlockScanning, StringCarrying(expanded),
    SourceSlicing, <<BlockScannerMachinery>>(priv fused)
  Observation (open: pub fields?): FrameObserving,
    IdentityObserving, ParentObserving, TransitionObserving,
    ObservationViewing
datom
  protos impls: ShapeDefined(10), Realize(2), Textualize(2),
    <<BlockRealizing>>(10), <<BlockTextualizing>>(10)
  Own(4): <<TextProjecting>>, PairDividing, MapKeyChecking,
    PositionAdvancing
ethos-monolith
  protos impls: ShapeDefined(16), Realize(1), Textualize(1),
    <<BlockRealizing>>(13), <<BlockTextualizing>>(13)
  Roles(3): <<ArtifactFreshness>>, <<CargoSourcePublishing>>,
    <<PathDeriving>>
  Projection(3): RustArtifactProjecting, RustTypeWriting,
    RustNameWriting
  Dialect(3): InterfaceDocumentReading, InterfaceValidation,
    SymbolReading
```

## 5. Rulings, Proposals, Open Questions

**Psyche-ruled**: Realize/Textualize two traits no umbrella
(traitsAsCapabilities.md 2026-08-14); ShapeDefined stays (same);
Walk stays (same); every method call under a trait (mandatoryTraits.md
2026-08-13); different fields are different types
(signalIsOurMessagingLayer.md 2026-08-14); universal in protos
(threeStacks.md 2026-08-14); fragmentation = one trait
(rustComponentArchitecture.md 2026-08-17); "trait/types design is
ontology in code" (rustComponentArchitecture.md 2026-08-18).

**Proposals** (research basis in parens):
- Scoped block pair: ONE universal protos capability, ~17 dialect traits fold in (P4, Rendel-Ostermann)
- Operations dissolved: `new` is Kind-level, getters -> pub fields, real capabilities -> Role traits (P1, Fowler, Hickey)
- Evidence vanishes: caller asks walk, 9 traits + 6 types removed (P9, AOP, UFO Mode)
- CarrierRealizing -> protos StringCarrying; HeadReading -> pub field (P1)
- Fuse StructuralWalk 5 privates -> 1; BlockScanner 3 -> 1 (fragmentation ruling)

**Open questions** (5):

1. Should the scoped block pair be one trait or two in protos? Isomorphism criterion (Rendel-Ostermann) argues one; the Realize/Textualize precedent argues two.
2. Does dissolving Operations traits and using pub fields + struct literals conflict with "every method call lives under a trait," or is it honored by elimination (field access and construction are not method calls)?
3. Should dialect evidence types vanish entirely (callers ask the walk) or does the evidence wrapper carry domain value worth keeping?
4. Is transition history (WalkObservation.history) part of what a walk is, or test scaffolding?
5. Should observation getter traits on walk-internal types (FrameObserving, etc.) remain, or should those types expose pub fields?
