# Kind and Capability Types

## A. WITNESS: Protos Struct, Enum, and Discrimination Semantics

### Struct

A struct is `Name.{Field1 Field2 ...}` -- shape `DottedBraced`, head = type name. Fields are positional, unnamed, identified by type name. The implementation stores fields as `Vec<String>` of type references. Duplicate field types are rejected. Exact field count is enforced: too few = `MissingPosition`, too many = `ExtraPosition`.

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs` lines 137-141 (NamedStruct), 1271-1280 (duplicate rejection), 1135-1163 (position count enforcement).

Struct bodies in type declarations contain only bare symbols. In data instances (like `Channel.{Psyche 1 1}`), the body carries positional values; nested delimited blocks within struct bodies are structurally possible (the scanner handles nested braces) but the current type-declaration dialect uses only bare words.

Method: code read same file lines 949-951.

### Enum

An enum is `Name.[Variant1 Variant2.Payload ...]` -- shape `DottedSquareBracketed`. Variants are unit (`Shape::Bare`: `Pending`) or data-carrying (`Shape::DottedBare`: `Ready.Payload`). A variant carries exactly zero or one type.

Method: code read same file lines 143-156, 1009-1044.

### Delimiter discrimination: the witnessed mechanism

**In the types section, three different structural types coexist in one `[...]` vector.** `TypeElement` accepts shapes `Bare`, `DottedBare`, `DottedBraced`, and `DottedSquareBracketed`. Its `ShapeDefined::select` dispatches:

- `(DottedBare, Some(head))` -> Typedef: `LockName.String`
- `(DottedBraced, Some(head))` -> Struct: `Lock.{LockId LockName FlowId LockPaths LockReason}`
- `(DottedSquareBracketed, Some(head))` -> Enum: `LockRejection.[DuplicateName.Lock PathOverlap.LockOverlap]`

These are three distinct Rust types (`NamedTypedef`, `NamedStruct`, `NamedEnum`) unified under a Rust enum (`TypeElement`). The types section `[...]` holds a `Vec<TypeElement>`.

Method: code read same file lines 123-127 (TypeElement enum), 430-451 (ShapeDefined, select by shape+head).

**This IS the mechanism the psyche cited.** The psyche said: "We use the same mechanism in the ethos signal interfaces and others to differentiate between things like an enum and a struct by checking the delimiter after the head." The fixture code confirms: the delimiter (square bracket vs brace) after the head selects the type.

**Arity does not discriminate today.** Within one delimiter shape (e.g. DottedBraced), all entries are the same type regardless of how many fields the body holds. The `NamedStruct` collects fields into a `Vec<String>` without checking length at selection time. Arity checking (fixed field count per struct type) happens at the dialect level, not at the structural selection level.

Method: code read same file lines 947-951 (struct realize: bare_symbol into Vec, no count check at select time).

### Vector homogeneity

The psyche ruled (2026-08-27): "variable length is [] and all components must share a type or kind."

**Witnessed:** The types section `[...]` holds TypeElement items of three shapes. They share the TypeElement KIND (a Rust enum that encompasses all three). This is a heterogeneous-shape vector that is homogeneous in KIND.

Method: code read `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos` lines 9-30 (types section with typedefs, structs, and enums in one vector).

**Consequence for capabilities:** If capabilities come in multiple structural forms (e.g. `len.Count` beside `register.{[PathLock] Registered Refused}`), they can sit in one `[capabilities]` vector only if they share a Capability KIND. Each form is a distinct type under that kind.

### Vector, Optional, and `<>`

**`Vector<T>`** is a type reference string, parsed as one bare token (angle brackets are not protos delimiters). `Optional<T>` appears in fixtures (`SelectedKind.Optional<Kind>` in spirit-ethos) but is not handled in the ethos-monolith POC.

Method: code read `/git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs` lines 511-521.

Spelling inconsistency: spirit-ethos uses `Optional<T>`; signal-agent uses `Option<T>`.

**`<>` is NOT a protos structural delimiter.** The scanner recognizes `()`, `""`, `[]`, `{}` only. `Processable<[Clonable Sendable] Serializable>` fails: `[` inside the prefix interrupts bare-word collection. However, `Sortable<Ordered>` (no spaces or delimiters inside `<>`) works as one bare token.

Method: code read `/git/github.com/LiGoldragon/protos/src/block.rs` lines 147-149, 306-311.

### Representing absence

Three witnessed patterns: (1) empty vector `[]` for 0..n. (2) `Optional<T>` for 0..1 (textual data encoding unwitnessed). (3) Enum with `None`-like variant: `EndpointSelection.[Bound.AgentEndpoint None]`, `ThreadSelection.[Named.ThreadName None]` -- most broadly witnessed.

Method: code read `/git/github.com/LiGoldragon/signal-message/ethos/interface.ethos` line 7.

### Implementation-to-Vision agreement

No disagreements found between datom.md and the implementation on struct, enum, head, or positional semantics.


## B. THE TYPES

### Supporting type declarations (shared by all designs)

```
KindReference.String

;; Position bounds
PositionBound.KindReference
PositionBounds.Vector<PositionBound>
Positions.Vector<PositionBounds>

;; Superkinds, associated kinds, associated values
Superkinds.Vector<KindReference>
AssociatedKindName.KindReference
AssociatedKindBounds.Vector<KindReference>
AssociatedKind.{AssociatedKindName AssociatedKindBounds}
AssociatedKinds.Vector<AssociatedKind>
AssociatedValueName.String
AssociatedValueType.String
AssociatedValue.{AssociatedValueName AssociatedValueType}
AssociatedValues.Vector<AssociatedValue>

;; Shared enums
BearerMode.[Reads Changes Consumes Creates]
Provision.[Required Provided]
Timing.[Sync Async]
YieldSlot.[None Yields.KindReference]
RefusalSlot.[None Refuses.KindReference]
InputKinds.Vector<KindReference>
Capabilities.Vector<Capability>
```


### Design (i): Flat structs -- every slot a field

**Types:**
```
Capability.{InputKinds YieldSlot RefusalSlot BearerMode Provision Timing}
Kind.{Positions Superkinds AssociatedKinds AssociatedValues Capabilities}
```

Capability: 6 fields (name in head). Kind: 5 fields (name in head). One type each. Every instance fills every field. Absence is an empty vector or a `None` enum variant.

**Instances:**

```
;; Sendable (marker)
Sendable.{[] [] [] [] []}

;; Runnable with run
Runnable.{[] [] [{Output []}] [] [
  run.{[] Yields.Output None Reads Required Sync}
]}

;; Processable with six capabilities
Processable.{
  [[Clonable Sendable] [Serializable]]
  [Displayable Debuggable Sendable Syncable Sealed]
  [{Output [Serializable DeserializeOwned]} {Ref []}]
  [{KIND String} {MAX_ITEMS Integer}]
  [
    len.{[] Yields.Count None Reads Required Sync}
    push.{[Item] None None Changes Required Sync}
    into_bytes.{[] Yields.Bytes None Consumes Required Sync}
    create.{[Config] Yields.Self None Creates Required Sync}
    register.{[PathLock] Yields.Registered Refuses.Refused Changes Required Sync}
    fetch.{[Key] Yields.Payload None Reads Required Async}
  ]
}
```

Sendable: 1 head, 5 fields, 12 brackets.
Runnable: 3 heads, 13 fields, 22 brackets.
Processable: 13 heads, 49 fields, ~64 brackets.

**Cannot express:** No structural distinction between marker and full kind. `Sendable` carries 5 empty vectors. Verbose for simple capabilities: `len.{[] Yields.Count None Reads Required Sync}` is 7 tokens for a one-line Rust signature.


### Design (ii): Structural discrimination -- different forms, same kind

The psyche's endorsed mechanism. Different structural types, told apart by delimiter, unified under one kind. This is how TypeElement works in the types section today.

**Capability kind -- three structural types:**
```
;; Bare: void capability (no inputs, no yield, no refusal)
;; name
;; e.g. notify

;; DottedBare: simple capability (no inputs, no refusal, yields)
;; name.yield
;; e.g. len.Count

;; DottedBraced: full capability (inputs and/or yield and/or refusal)
;; name.{InputKinds YieldSlot RefusalSlot}
;; e.g. register.{[PathLock] Yields.Registered Refuses.Refused}
```

All three sit in one `[capabilities]` because they share the Capability kind. Discrimination is by delimiter: Bare / DottedBare / DottedBraced.

**Kind kind -- three structural types:**
```
;; Bare: marker kind (no capabilities, no superkinds, no positions)
;; Name
;; e.g. Sendable

;; DottedSquareBracketed: simple kind (capabilities only)
;; Name.[capabilities]
;; e.g. Runnable.[len.Count]

;; DottedBraced: full kind (superkinds + assoc kinds + assoc values + capabilities)
;; Name.{Superkinds AssociatedKinds AssociatedValues Capabilities}
;; e.g. Processable.{[Displayable ...] [...] [...] [...]}
```

Kinds in a `[kinds]` vector share the Kind kind. Discrimination by delimiter.

**Instances:**

```
;; Sendable (marker) -- Bare
Sendable

;; Runnable -- DottedSquareBracketed
Runnable.[run.Count]

;; Processable -- DottedBraced
Processable.{
  [Displayable Debuggable Sendable Syncable Sealed]
  [{Output [Serializable DeserializeOwned]} {Ref []}]
  [{KIND String} {MAX_ITEMS Integer}]
  [
    len.Count
    push.{[Item] None None}
    into_bytes.Bytes
    create.{[Config] Yields.Self None}
    register.{[PathLock] Yields.Registered Refuses.Refused}
    fetch.{[Key] Yields.Payload None}
  ]
}
```

Sendable: 0 heads, 0 fields, 0 brackets.
Runnable: 1 head (Runnable) + 1 (run), 1 capability, 2 brackets.
Processable: 1 head (Processable) + 6 (capabilities) + 2 (Yields/Refuses variants) = 9 heads, 4 kind fields + 6x3 cap fields = 22 fields, ~40 brackets.

**Bearer mode is NOT in the capability entry.** The three-field full capability carries only the signal triple (inputs, yield, refusal). Mode, provision, timing live elsewhere: in mode-grouping sections within the kind (per capabilityAnatomy Design (b)), or in the interaction. This is a design choice: the kind declaration shows WHAT a capability takes and returns; the interaction shows HOW (mode, async, provision).

**The simple form carries defaults.** `len.Count` (DottedBare) means: no inputs, no refusal, yields Count. The simple form is equivalent to `len.{[] Yields.Count None}` with the struct elided. A capability with ANY inputs or ANY refusal must use the full form.

**Cannot express:** Bearer mode, provision, and timing are absent from capability entries -- they must live elsewhere. Promoting a marker kind to a simple kind changes delimiter (Bare -> DottedSquareBracketed), which is a structural rewrite. Arity discrimination within DottedBraced (e.g. 2-field vs 3-field) is not witnessed in the current implementation; if the full form has 3 fields, then capabilities with inputs + yield but no refusal still write `None` in the refusal position.

**Open within this design:** Whether the full capability `name.{...}` always has exactly 3 fields (inputs, yield, refusal) with enum-wrapped None for absent slots, or whether DottedBraced entries may have 2 or 3 fields discriminated by arity. Arity discrimination is structurally possible (the walker counts children) but not witnessed in the current `ShapeDefined` mechanism.


### Design (iii): Struct with inner enums -- variability in field types

**Types:**
```
KindBody.[Marker Bearer.BearerDetail]
BearerDetail.{Superkinds AssociatedKinds AssociatedValues Capabilities}
Kind.{Positions KindBody}

CapabilityYield.[NoYield YieldsKind.KindReference YieldsSelf YieldsAssociated.KindReference]
CapabilityRefusal.[Infallible Refuses.KindReference]
Capability.{InputKinds CapabilityYield CapabilityRefusal BearerMode Provision Timing}
```

Kind: 2 fields (name in head). Capability: 6 fields (name in head). Fixed shapes, richer inner enums absorb variability.

**Instances:**

```
;; Sendable
Sendable.{[] Marker}

;; Runnable
Runnable.{[] Bearer.{[] [{Output []}] [] [
  run.{[] YieldsAssociated.Output Infallible Reads Required Sync}
]}}

;; Processable
Processable.{
  [[Clonable Sendable] [Serializable]]
  Bearer.{
    [Displayable Debuggable Sendable Syncable Sealed]
    [{Output [Serializable DeserializeOwned]} {Ref []}]
    [{KIND String} {MAX_ITEMS Integer}]
    [
      len.{[] YieldsKind.Count Infallible Reads Required Sync}
      push.{[Item] NoYield Infallible Changes Required Sync}
      into_bytes.{[] YieldsKind.Bytes Infallible Consumes Required Sync}
      create.{[Config] YieldsSelf Infallible Creates Required Sync}
      register.{[PathLock] YieldsKind.Registered Refuses.Refused Changes Required Sync}
      fetch.{[Key] YieldsKind.Payload Infallible Reads Required Async}
    ]
  }
}
```

Sendable: 1 head, 2 fields, 4 brackets.
Runnable: 4 heads, 14 fields, 22 brackets.
Processable: 14 heads, 50 fields, ~62 brackets.

**Cannot express:** The `YieldsSelf` variant assumes Self is universally understood. The `YieldsAssociated` variant requires semantic classification. Four nesting levels: Kind braces > KindBody variant braces > Capabilities vector > Capability braces.


## C. IDENTITY

### Kind identity

The psyche ruled: "the identity parts of the data" are name and positions. In a Kind instance:
- **Name**: the head (`Processable`)
- **Positions**: the `<>` content, or the first body field in Design (i)/(iii)

All other fields (superkinds, associated kinds, associated values, capabilities) are non-identity.

### What `<>` holds

`Processable<[Clonable Sendable] Serializable>` holds a vector of positions. Each position is either:
- A single kind reference: `Serializable` (one bound)
- A bracketed vector of kind references: `[Clonable Sendable]` (multi-bound, homogeneous per the `[]` rule)

In type terms: `Positions` = `Vector<PositionBounds>`, `PositionBounds` = `Vector<PositionBound>`. A single-bound position is a 1-element vector.

### Head form vs body form

**Head form** (psyche's preferred): `Processable<[Clonable Sendable] Serializable>.{...}`. Requires parser extension for `<>` as a structural delimiter. Single-bound positions like `Sortable<Ordered>` work today (one bare token); multi-bound positions with `[` inside do not.

**Body form** (currently parseable): `Processable.{[[Clonable Sendable] [Serializable]] ...}`. Positions are the first body field. No parser changes needed.

In Design (ii), where full kinds are DottedBraced, the `<>` would be part of the head: `Processable<[Clonable Sendable] Serializable>.{[superkinds] [assocKinds] [assocValues] [capabilities]}`.

### Capability identity

The name alone. The head of every capability entry is its identity. No `<>` or additional identity fields.


## D. RECOMMENDATION

Design (ii), structural discrimination. It is the mechanism the psyche explicitly endorsed, it is witnessed in the living implementation (TypeElement discriminates Typedef/Struct/Enum by delimiter today), and it yields the tersest syntax for the common cases: `Sendable` with zero overhead, `len.Count` with one head, while the full forms carry exactly the fields their category needs. It costs: bearer mode, provision, and timing are not in the capability entry (they live in the kind's mode structure or in the interaction); and promoting a marker to a bearer changes delimiter.


## E. OPEN QUESTIONS

1. Does `<>` become a protos structural delimiter, or only single-bound `<Kind>` (already parseable as one bare token)?
2. Does the full capability form `name.{...}` always have 3 fields (inputs, yield, refusal) with enum-wrapped None for absence, or do DottedBraced arities of 1, 2, and 3 each denote a distinct type?
3. Do bearer mode, provision, and timing appear in the capability entry, in mode-grouping sections, or in the interaction?
4. Are associated values (const generics, associated constants) expressed in kind declarations?
5. Is `Self` a valid kind reference in a yield slot?
6. Does a DottedSquareBracketed simple kind carry only capabilities, or also superkinds?
7. What is the exact set of defaults the DottedBare simple form carries?
8. Is the Capability kind declared in Ethos (how?), or only realized in the walker code as TypeElement is today?


## F. Sources

### Vision and psyche
- Vision/datom.md
- Vision/ethos.md
- flows/b675f3d9/vision/kinds.md (all entries through 2026-08-27)
- flows/b675f3d9/reports/rustTraitAnatomy.md (sections 1-2)
- flows/b675f3d9/reports/capabilityAnatomy.md (sections 1-3)
- flows/b675f3d9/reports/ethosAnatomyVision.md
- flows/b675f3d9/witnesses/angleBracketsInEthos.md

### Living fixtures
- /git/github.com/LiGoldragon/ethos-monolith/fixtures/psyche/interface.ethos
- /git/github.com/LiGoldragon/ethos-monolith/README.md
- /git/github.com/LiGoldragon/ethos-monolith/ARCHITECTURE.md
- /git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos
- /git/github.com/LiGoldragon/spirit-ethos/interface.ethos
- /git/github.com/LiGoldragon/spirit-ethos/meta.ethos
- /git/github.com/LiGoldragon/spirit-ethos/nexus.ethos
- /git/github.com/LiGoldragon/spirit-ethos/sema.ethos
- /git/github.com/LiGoldragon/spirit-ethos/batch-config.json
- /git/github.com/LiGoldragon/signal-agent/ethos/interface.ethos
- /git/github.com/LiGoldragon/signal-standard/ethos/interface.ethos
- /git/github.com/LiGoldragon/signal-message/ethos/interface.ethos

### Implementation (protos and ethos-monolith)
- /git/github.com/LiGoldragon/protos/src/shape.rs
- /git/github.com/LiGoldragon/protos/src/block.rs
- /git/github.com/LiGoldragon/ethos-monolith/src/fixture/mod.rs
- /git/github.com/LiGoldragon/ethos-monolith/src/generate.rs
- /git/github.com/LiGoldragon/ethos-monolith/src/lib.rs
