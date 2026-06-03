---
title: 493 — Schema header variants resolve through namespace; inline declarations auto-register
role: designer
variant: Design
date: 2026-06-03
topics: [schema, header, namespace-lookup, inline-declaration, type-table-resolution, shorthand-syntax, exported-types]
description: |
  Designer-space implementation of the psyche's directive that schema header
  variant references should resolve through namespace lookup (or be auto-registered
  from inline declarations) rather than carrying the verbose explicit (Variant Payload)
  form. Demonstrates the rewrite on spirit-next/schema/lib.schema. Documents the
  engine semantics operator's slice needs to implement. Per Spirit 1554 + 1555 + 1556.
---

# 493 — Schema header variants resolve through namespace

## What the psyche asked for

[Header variant references should resolve through namespace lookup or inline declarations. A bare PascalCase variant name in the schema header (Input/Output root enum bodies) looks up the matching type in the namespace per Spirit 1468 type-table variant resolution. An inline declaration at variant position auto-registers the type into the namespace. This eliminates the verbose (Variant Payload) form when the variant name matches a namespace type or carries its own inline definition.] — Spirit 1554 (Decision High, 2026-06-03).

[Every PascalCase name appearing in the schema header (Input root enum body, Output root enum body, NexusWork, NexusAction, SemaWriteInput, SemaReadInput) becomes an exported top-level type. Library consumers of the schema can import these names. The header IS the component's public type-level interface — each header variant is a public thing with a name and a definition (in the namespace or inline).] — Spirit 1555 (Principle High).

[Schema parsing operates in multiple passes per source block. Pass 1 finds all identifier uses and their source locations. Pass 2 registers inline declarations into the namespace and resolves identifier references through namespace lookup … The multi-pass approach lets the engine know whether each identifier defines a type, references a type, or both — guesswork is eliminated by the source representation rather than rediscovered from lowered fields.] — Spirit 1556 (Decision High).

The psyche pointed at operator 297's Layer 1 example showing the current spirit schema, asking why `Lookup` isn't just defined in the namespace so we don't have to write `(Lookup RecordIdentifier)`, and noting that header items become exported types other consumers can use. The psyche wants this implemented in designer space — the rewrite of `spirit-next/schema/lib.schema` using the new sugar — as the worked demonstration of the shape.

## The current shape

`spirit-next/schema/lib.schema` today carries six Input variants, eight Output variants, four NexusWork variants, five NexusAction variants, and the two SEMA input enums all in the verbose explicit-payload form:

```
{}
[(Record Entry) (Observe Query) (Lookup RecordIdentifier) (Count Query) (Remove RecordIdentifier) (LookupStash StashHandle)]
[(RecordAccepted SemaReceipt) (RecordsObserved ObservedRecords) (RecordsStashed StashedObservation) (RecordFound FoundRecord) (RecordsCounted CountedRecords) (RecordRemoved RemoveReceipt) (Error ErrorReport) (Rejected SignalRejection)]
{
  ...
  NexusWork [(SignalArrived Input) (SemaWriteCompleted SemaWriteOutput) (SemaReadCompleted SemaReadOutput) (EffectCompleted NexusEffectResult)]
  NexusAction [(CommandSemaWrite SemaWriteInput) (CommandSemaRead SemaReadInput) (ReplyToSignal Output) (CommandEffect NexusEffectCommand) (Continue NexusWork)]
  SemaWriteInput [(Record Entry) (Remove RecordIdentifier)]
  SemaReadInput [(Observe Query) (Lookup RecordIdentifier) (Count Query)]
  ...
}
```

The pattern that repeats: every variant carries an explicit payload type whose name differs from the variant's. `Record` carries `Entry`, `Observe` carries `Query`, `Lookup` carries `RecordIdentifier`, and so on. The verbose form is structurally complete but it doesn't expose the verbs as exported types — `Record` and `Lookup` are just enum-variant tags rather than top-level names a downstream consumer could import.

## The rewrite

Header items become bare PascalCase names; each is a namespace entry that binds the verb-name to its payload type. The type-table variant resolution rule at Spirit 1468 (bare PascalCase variant in header looks up the namespace) governs the source layer, and the lowering distinguishes two namespace-entry shapes at the Rust emission layer — see §"The Rust emission distinction" below for the refinement that addresses the nested-wrapper-construction smell operator surfaced at Spirit 1557.

```
{}
[Record Observe Lookup Count Remove LookupStash]
[RecordAccepted RecordsObserved RecordsStashed RecordFound RecordsCounted RecordRemoved Error Rejected]
{
  ; Input verbs — each is an exported newtype over its payload
  Record Entry
  Observe Query
  Lookup RecordIdentifier
  Count Query
  Remove RecordIdentifier
  LookupStash StashHandle

  ; Output replies — same pattern
  RecordAccepted SemaReceipt
  RecordsObserved ObservedRecords
  RecordsStashed StashedObservation
  RecordFound FoundRecord
  RecordsCounted CountedRecords
  RecordRemoved RemoveReceipt
  Error ErrorReport
  Rejected SignalRejection

  ; NexusWork / NexusAction — same pattern
  SignalArrived Input
  SemaWriteCompleted SemaWriteOutput
  SemaReadCompleted SemaReadOutput
  EffectCompleted NexusEffectResult
  NexusWork [SignalArrived SemaWriteCompleted SemaReadCompleted EffectCompleted]

  CommandSemaWrite SemaWriteInput
  CommandSemaRead SemaReadInput
  ReplyToSignal Output
  CommandEffect NexusEffectCommand
  Continue NexusWork
  NexusAction [CommandSemaWrite CommandSemaRead ReplyToSignal CommandEffect Continue]

  ; SEMA inputs reuse the same Input verbs by name
  SemaWriteInput [Record Remove]
  SemaReadInput [Observe Lookup Count]

  ; effect vocabulary
  Stash StashRequest
  Stashed StashResult
  NexusEffectCommand [Stash]
  NexusEffectResult [Stashed]

  ; SEMA outputs — same reply pattern
  Recorded SemaReceipt
  Removed RemoveReceipt
  Missed ErrorReport
  Observed ObservedRecords
  Found FoundRecord
  Counted CountedRecords
  SemaWriteOutput [Recorded Removed Missed]
  SemaReadOutput [Observed Found Counted Missed]

  ; supporting types stay as they are
  Topic String
  Topics (Vec Topic)
  Description String
  ErrorMessage String
  RecordIdentifier Integer
  CommitSequence Integer
  StateDigest Integer
  DatabaseMarker { CommitSequence * StateDigest * }
  SemaReceipt { RecordIdentifier * DatabaseMarker * }
  RemoveReceipt { RecordIdentifier * DatabaseMarker * }
  ObservedRecords { RecordSet * DatabaseMarker * }
  FoundRecord { RecordIdentifier * Entry * DatabaseMarker * }
  RecordCount Integer
  CountedRecords { RecordCount * DatabaseMarker * }
  ErrorReport { ErrorMessage * DatabaseMarker * }
  SignalRejection { ValidationError * DatabaseMarker * }
  ValidationError [EmptyTopic EmptyDescription EmptyQueryTopic StashHandleNotFound]
  StashHandle Integer
  StashRequest { Records * DatabaseMarker * }
  StashResult { StashHandle * RecordCount * DatabaseMarker * }
  StashedObservation { StashHandle * RecordCount * DatabaseMarker * }
  Records (Vec Entry)
  RecordSet (Vec Entry)
  Entry { Topics * Kind * Description * Magnitude * Privacy * }
  Query { TopicMatch * kind (Optional Kind) privacy_selection PrivacySelection }
  TopicMatch [Partial Full]
  Partial Topics
  Full Topics
  Privacy Magnitude
  PrivacySelection [Any Exact AtMost AtLeast]
  Exact Privacy
  AtMost Privacy
  AtLeast Privacy
  Kind [Decision Principle Correction Clarification Constraint]
  Magnitude [Zero Minimum VeryLow Low Medium High VeryHigh Maximum]
}
```

Three things change at the source level.

First, the Input and Output root enum bodies become bare-name lists. `[Record Observe Lookup Count Remove LookupStash]` is now a vector of variant signatures resolved through the namespace — `Record` is a typed variant whose payload comes from the namespace entry `Record Entry`. The reader's pass 2 looks up each header name and binds the variant to its namespace type.

Second, every header verb gets its own namespace entry binding the verb-name to its payload type. `Record Entry` is a bare aliasing entry — no struct body, no field name, just `Name TypeReference`. These bare aliasing entries lower to **Rust type aliases**, not newtypes — see §"The Rust emission distinction" below for why this matters and for the genuine-newtype case it's distinguished from.

## The Rust emission distinction — bare aliases vs struct bodies

This refinement addresses the nested-wrapper-construction smell operator surfaced at Spirit 1557: [repeated nested variant-wrapper construction in code, such as Output::Rejected wrapping Rejected wrapping SignalRejection, indicates bad design or a missing logic/emission layer; generated APIs should not force callers to hand-write that repetition.] An earlier draft of this report proposed lowering every namespace entry to a newtype, which produced `Output::Rejected(Rejected(SignalRejection { ... }))` at call sites. That's the bad design Spirit 1557 names.

The clean distinction is at the source-language layer. The schema-next `SyntaxDeclaration` at `syntax.rs:70-75` already tags two kinds of declarations:

- `Alias(SyntaxReference)` — a bare aliasing entry. The source is `Name TypeRef` with no struct body. Example: `Record Entry`, `Rejected SignalRejection`, `Topic String`, `RecordIdentifier Integer`.
- `Struct(SyntaxStructDeclaration)` — a declaration with an explicit struct body. The source is `Name { field Type ... }` with one or more fields. Example: `TraceEvent { object_name ObjectName }`, `Entry { Topics * Kind * Description * Magnitude * Privacy * }`.

The lowering at Rust emission distinguishes these:

- Bare aliasing entries (`Alias(...)`) lower to **Rust type aliases**: `pub type Record = Entry;`, `pub type Rejected = SignalRejection;`. The exported name lives — consumers can `use spirit_next_signal::Record;` and the SymbolPath identity is preserved for Help / NotaConfig / trace surfaces. But at the Rust type level Record IS Entry, so `Input::Record(some_entry)` constructs without ceremony because there's no distinct type to wrap.
- Struct-body entries (`Struct(...)`) keep the newtype lowering operator landed at 295 for single-field cases — `TraceEvent { object_name: ObjectName }` stays `pub struct TraceEvent(pub ObjectName);` because the source explicitly wrote a struct body, and the field name was load-bearing enough to author. Multi-field struct bodies lower to named structs, unchanged.

So the Rust emission for the rewritten schema becomes:

```rust
// Bare aliasing entries → Rust type aliases
pub type Record = Entry;
pub type Observe = Query;
pub type Lookup = RecordIdentifier;
pub type Count = Query;
pub type Remove = RecordIdentifier;
pub type LookupStash = StashHandle;

pub type RecordAccepted = SemaReceipt;
pub type RecordsObserved = ObservedRecords;
pub type Rejected = SignalRejection;
// ... etc

// Generated Input / Output enums carry the underlying type directly
pub enum Input {
    Record(Entry),
    Observe(Query),
    Lookup(RecordIdentifier),
    Count(Query),
    Remove(RecordIdentifier),
    LookupStash(StashHandle),
}

pub enum Output {
    RecordAccepted(SemaReceipt),
    RecordsObserved(ObservedRecords),
    // ... etc
    Rejected(SignalRejection),
}
```

Construction at call sites is one level of wrapping, not three:

```rust
let input = Input::Record(Entry {
    topics: Topics(vec![...]),
    kind: Kind::Decision,
    ...
});

let output = Output::Rejected(SignalRejection {
    validation_error: ValidationError::EmptyTopic,
    database_marker: marker(0, 0),
});
```

Consumers who want to construct a Rejected can also do `let r: Rejected = SignalRejection { ... };` — the alias works both directions.

This refines the Spirit 1535 newtype-lowering rule's application boundary: the rule applies to **declarations with struct bodies** (where the field name carries domain meaning), not to bare aliasing entries (where the alias is just a renamed reference). Operator's slice at schema-rust-next implements the alias-vs-newtype branch in the emitter; the schema-next source layer doesn't need to change because the distinction already lives in `SyntaxDeclaration::Alias` vs `SyntaxDeclaration::Struct`.

This composes with operator's planned constructor-ergonomic work for genuine newtypes. Where a newtype IS the right shape (struct-body declarations like `TraceEvent { object_name: ObjectName }`), operator's `Output::rejected(SignalRejection { ... })` style associated constructors still help by hiding the wrapper at construction. The alias-lowering removes the wrapper for bare aliases; the constructor sugar hides it for genuine newtypes. Both compose; both are needed.

Third, SemaWriteInput and SemaReadInput collapse to bare-name lists too. `SemaWriteInput [Record Remove]` reuses the same `Record` and `Remove` namespace types the Input root uses — these are the same operations expressed at the SEMA write boundary. The repetition that the verbose form created (`(Record Entry)` in Input + `(Record Entry)` in SemaWriteInput) collapses to one declared type, one binding, two references.

## Engine semantics — what operator's slice needs to implement

The engine needs to support multi-pass identifier resolution for the source block, per Spirit 1556. The proposed pass shape:

**Pass 1 — Identifier collection.** Walk the source tree. For every PascalCase name encountered in a header variant position, a namespace entry RHS, or a struct field type position, record (identifier, location, role). Roles are `Declares` (this position introduces a new type into the namespace) or `References` (this position uses a type that should resolve through the namespace).

**Pass 2 — Inline declaration registration.** For inline declarations (header position carrying a brace body or bracket body, e.g. `(Record { Entry * })` or `NexusWork [...]`), auto-register the inline body as a namespace entry under the header name. After pass 2 the namespace contains every type the source declares — both explicit namespace entries and lifted-from-inline.

**Pass 3 — Reference resolution.** For every `References` identifier, look up the namespace. If found, bind the reference to the declared type. If not found, error with the source location.

The result is an enriched `SchemaSource` where every identifier is resolved. The existing single-field newtype lowering rule then applies as it does today; the new substrate is just that the namespace is fully populated before lowering runs.

A concrete change in the schema-next source crate: `SchemaSource::from_document` at `source.rs:27-68` currently parses each root in one pass. The new substrate has an intermediate `ResolvedSchemaSource` that the engine produces after the three passes, and `SchemaSource::lower` consumes the resolved form. The `SourceField` and `SourceReference` shapes don't need to change — only how references are bound to declarations changes.

A test that pins the new behavior: feed the rewritten `lib.schema` above through the engine, lower to Asschema, and assert the resulting `TypeDeclaration` set is byte-identical to what the verbose form produces today. Same assembled program, shorter source.

## Why this is the right shape

Three reasons the rewrite is better than the verbose form, beyond the line-count win.

First, the header reads as a contract. `[Record Observe Lookup Count Remove LookupStash]` says — these are the six verbs the daemon supports. The verbose form `[(Record Entry) (Observe Query) ...]` mixes the verb with its payload type at the contract layer, which is fine information but it's at the wrong level — a downstream reader wants the verbs first and the payload types as a separate look-up.

Second, the namespace becomes the export list. Every type a consumer might want to use (whether they're another component implementing this contract, a test harness producing inputs, or a client constructing requests) lives at one declared name. `spirit_next_signal::Record(some_entry)` is the constructor — the Rust noun the downstream code reaches for is the same shape as the schema name. The verbose form spreads the same information across the Input variant body, which a downstream reader can't easily project to "give me a Record constructor."

Third, multiple use sites collapse to one binding. `Record` appears in Input, in SemaWriteInput, and (transitively) in NexusWork through the SignalArrived → Input chain. The verbose form repeats the `(Record Entry)` pair at every use; the rewrite has one `Record Entry` declaration and lets every use site reference it by name. The same insight skills/nota-design.md Rule 4 names for the BusyReason case — *"the semantic root is the variant; the choice axis is the payload enum; no wrapper"* — applies upward to header variants: the variant IS the type, and the namespace owns the type's definition.

## Cross-references and forward direction

The rewrite shape is a clean composition of three already-ratified rules:

- Spirit 1467 (header-declared inline enum sugar): the header may carry an inline body directly, and that body lowers to a namespace declaration. Captured.
- Spirit 1468 (type-table variant resolution): a bare PascalCase variant in the header resolves through the namespace. Captured.
- Spirit 1535 (single-field newtype lowering, operator 295): a single-field declaration emits as a Rust newtype, not a one-field struct. Implemented.

The new captures today extend these from "lowering rules" to "source-language shape" — the verbose form should give way to the shorter form in authored schema source. The engine needs the multi-pass identifier resolution to support it.

Operator's natural next slice: implement the multi-pass resolution in schema-next's engine and migrate `spirit-next/schema/lib.schema` to the rewritten form. Tests pin that the lowered Asschema is identical between the two source forms — same assembled program, shorter source. The migration can be incremental — start with the Input and Output root enum bodies (the highest-visibility rewrite), then SemaWriteInput / SemaReadInput, then the NexusWork / NexusAction declarations.

When that lands, the rewrite ratifies in production. spirit-next becomes the worked example of the shorter form; other components (introspect, schema-daemon, persona, the future cross-component pair) adopt it from inception.

## Cross-references

- `reports/operator/297-Psyche-...-2026-06-03.md` — operator's Layer 1 framing the psyche pointed at.
- `reports/operator/295-Implementation-schema-newtype-trace-cleanup-2026-06-03.md` — the newtype-lowering rule the rewrite composes with.
- `reports/operator/296-Psyche-schema-representation-in-out-codec-2026-06-03.md` — the SchemaSource layer this rewrite extends.
- `skills/nota-design.md` §"Rule 4 — Enum payloads are choices; structs are products" — header-declared inline enum sugar + type-table variant resolution discipline.
- `skills/component-triad.md` §"Nexus mechanism substrate" — the substrate the schema describes.
- Spirit 1467 + 1468 (inline enum sugar + type-table resolution, the earlier captures), 1535 (newtype lowering implemented), 1554 + 1555 + 1556 (the new captures driving this rewrite).
