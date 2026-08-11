# Psyche Component Ethos Fixture and Expected Generated Rust Shape

Design proposal for psyche review. Bead primary-xqb.8.4.

The psyche component is the first ethos-rust fixture. It holds Spirit,
Intent, and Vision records, introduces a top-level layer enum, and
reuses much of Spirit v14 vocabulary. This document proposes the exact
Ethos fixture text and the exact generated Rust module shapes the
ethos-rust generator must produce.

## Governing rulings

- threeStacks.md 2026-08-11: psyche component is the fixture; reuses
  much of Spirit; top-level `Layer.[Spirit Intent Vision]` enum;
  component + ordinary-socket signal repo + metasocket signal repo;
  no core-* split; ethos-rust is the generator name; generated Rust
  is committed; freshness mechanism open.
- observerFixtureBlessed.md 2026-08-07: blessed fixture format;
  version as `{Major Minor Patch}`; `/` for imports; `[]` for import
  item lists; stream section entries are element-type only; initiation
  and termination live in Input.
- streamSection.md 2026-08-07: stream is a section inside the object.
- redesignAuditRulings-2026-08-06: colon-form transformer syntax;
  stream is a fourth role kind; sections confer universal traits;
  the body is the rkyv payload of the strict typed value.
- ethosFileStructureCleanCut-2026-08-02: header + imports + body;
  interface body four positions (five with stream); nexus declares
  traits and the types those traits' method signatures reference;
  method signature convention `method.{Params... Return}`.
- Spirit v14 roots (spirit-ethos repo, condemned to dissolve):
  interface.ethos, nexus.ethos, sema.ethos as reuse material.

## Part 1: Fixture Text

### interface.ethos

Defines the psyche component's ordinary-socket wire vocabulary.
Five sections: inputs, outputs, refusals, streams, shared types.

```
Interface.{1 0 0}
[signal/domain.[Domain DomainScopes]]
{
  [
    Record.RecordRequest
    Observe.Query
    Lookup.RecordIdentifier
    Subscribe.Query
    Unsubscribe.SubscriptionHandle
  ]
  [
    Recorded.RecordIdentifier
    Observed.RecordSet
    LookedUp.FoundRecord
    Subscribed.SubscriptionHandle
    Unsubscribed.SubscriptionHandle
  ]
  [
    AdmissionRejected.{GuardianReason Explanation}
    QueryRejected.{QueryRefusal Explanation}
    UnknownSubscription.SubscriptionHandle
  ]
  [
    RecordChange.RecordEvent
  ]
  [
    Layer.[Spirit Intent Vision]
    Domains.Vector<Domain>
    Description.String
    Explanation.String
    QuoteText.String
    Reasoning.String
    RecordIdentifier.String
    SubscriptionHandle.Integer
    Importance.Magnitude
    Magnitude.[Zero Minimum VeryLow Low Medium High VeryHigh Maximum]
    Kind.[Decision Principle Correction Clarification Constraint]
    Keyword.String
    Keywords.Vector<Keyword>
    DomainMatch.[Any Partial.DomainScopes Full.DomainScopes]
    KeywordMatch.[Any AnyKeyword.Keywords AllKeywords.Keywords]
    SearchText.String
    TextMatch.[Any ContainsText.SearchText]
    SelectedKind.Optional<Kind>
    ImportanceSelection.[Any ExactImportance.Importance
                             AtMostImportance.Importance
                             AtLeastImportance.Importance]
    LayerSelection.[Any SelectedLayer.Layer]
    Query.{LayerSelection DomainMatch KeywordMatch TextMatch
           SelectedKind ImportanceSelection}
    VerbatimQuote.QuoteText
    Testimony.Vector<VerbatimQuote>
    Justification.{Testimony Reasoning}
    Entry.{Layer Domains Kind Description Importance}
    RecordRequest.{Entry Justification}
    ObservedRecord.{RecordIdentifier Entry}
    RecordSet.Vector<ObservedRecord>
    FoundRecord.{RecordIdentifier Entry}
    GuardianReason.[Duplicate Contradiction Matter
                    InsufficientWarrant ImportanceUnsupported]
    QueryRefusal.[InvalidDomainSelection]
    RecordAdmitted.{Entry RecordIdentifier}
    RecordEvent.[RecordAdmitted]
  ]
}
```

**Adaptations from Spirit v14.**

- `Layer.[Spirit Intent Vision]` added as the top-level discriminator
  per the psyche's 2026-08-11 ruling.
- `Entry` gains `Layer` as its first field: `Entry.{Layer Domains Kind
  Description Importance}`.
- `LayerSelection.[Any SelectedLayer.Layer]` added as a sixth Query
  dimension.
- `Subscribe`/`Unsubscribe` inputs added with corresponding
  `Subscribed`/`Unsubscribed` outputs and `UnknownSubscription`
  refusal, per the stream-as-fourth-kind ruling: initiation and
  termination live in Input as separate hand-authored objects.
- `RecordChange.RecordEvent` in the new Stream section (section 4),
  per the blessed fixture format: stream-section entries are
  element-type only.
- `VerbatimQuote.QuoteText` is a newtype (not a single-field struct)
  per the psyche's expressed preference against single-field structs.
- `RecordAdmitted.{Entry RecordIdentifier}` replaces Spirit's
  `IntentRecorded` to reflect the broader scope.
- `RecordEvent.[RecordAdmitted]` replaces Spirit's `IntentEvent`.
- `SubscriptionHandle.Integer` added for stream identity management.
- `LookupStash`, `Count`, `Marker`, `Version` operations removed:
  these were Spirit-specific operational detail, not core psyche
  vocabulary. They can return in a later fixture revision.
- Import syntax updated: `signal/domain.[Domain DomainScopes]` using
  `/` path separator and `[]` item list per the blessed fixture.
- Version format: `{1 0 0}` SemVer triple per the blessed fixture.

### nexus.ethos

Defines the psyche daemon's internal machinery: behavior traits and
the types those trait method signatures reference.

```
Nexus.{1 0 0}
[interface.[Entry RecordSet RecordRequest RecordIdentifier
            FoundRecord GuardianReason Query RecordEvent]]
{
  [
    AdmissionDecision.[Accepted Rejected.GuardianReason]
    GuardianDecision.[Admit Refuse.GuardianReason]
  ]
  [
    SignalAdmission.{admit.{RecordRequest AdmissionDecision}}
    AgentGuardian.{guard.{Entry RecordSet GuardianDecision}}
    RecordStore.{store.{Entry RecordIdentifier}
                 retrieve.{RecordIdentifier FoundRecord}
                 query.{Query RecordSet}}
    RecordChangeEmitter.{emit.{RecordEvent Unit}}
  ]
}
```

**Adaptations from Spirit v14.**

- Trait bodies now carry explicit method signatures per the
  ethosFileStructureCleanCut ruling ("traits and the types those
  traits' method signatures reference"). Spirit v14 listed bare
  trait names; the fixture expands them.
- `RecordChangeEmitter` replaces Spirit's `IntentObserver` to reflect
  the broader scope (emitting events for all three layers).
- `LifecycleDecision.[Persist Emit]` removed: this was Spirit-specific
  and not referenced by any trait method in the v14 source.
- Method signature convention: `method.{Params... Return}` with
  return type last, receiver implied by trait membership.

### sema.ethos

Defines the psyche daemon's persistent database schema.

```
Sema.{1 0 0}
[interface.[Entry RecordIdentifier]]
{
  [
    StoredRecord.{RecordIdentifier Entry}
  ]
  [
    records.{StoredRecord RecordIdentifier}
  ]
}
```

**Adaptations from Spirit v14.**

- `Migration` types removed: Spirit's v13-to-v14 migration receipt is
  Spirit-specific history. The psyche component starts with no
  migration debt. A migration family returns when the psyche schema
  itself evolves.
- The `records` family stores `StoredRecord` keyed by
  `RecordIdentifier`. Since `Entry` now carries `Layer`, each stored
  record inherently records which layer it belongs to.

## Part 2: Expected Generated Rust Shape

The ethos-rust generator reads the three Ethos source files and
produces three Rust module files. Each file is self-contained with the
appropriate imports.

Convention for this document: the full rkyv Wire preamble is shown
once; subsequent Wire-attributed types abbreviate it as `// [Wire]`.
Plain-attributed types (Nexus internals) carry no rkyv preamble.

The full Wire preamble (applied to every type in signal.rs and
sema.rs):

```rust
#[derive(Clone, Debug, PartialEq, Eq, rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
#[rkyv(
    serialize_bounds(
        __S: rkyv::ser::Writer + rkyv::ser::Allocator,
        __S::Error: rkyv::rancor::Source,
    ),
    deserialize_bounds(__D::Error: rkyv::rancor::Source),
    bytecheck(
        bounds(
            __C: rkyv::validation::ArchiveContext,
            __C::Error: rkyv::rancor::Source,
        ),
    ),
)]
```

### signal.rs

Generated from interface.ethos. Lives in the `signal-psyche` crate.
Destination: `signal-psyche/src/generated.rs` (or equivalent).

```rust
// @generated by ethos-rust from an authority-verified psyche interface source
// source-digest: blake3:<64-hex-chars>

use protos::{Input, Output, Refusal, Stream};
use signal_domain::{Domain, DomainScopes};

// ---- Layer enum ----

// [Wire]
pub enum Layer {
    Spirit,
    Intent,
    Vision,
}

// ---- Scalar newtypes ----

// [Wire]
pub struct Domains(Vec<Domain>);

// [Wire]
pub struct Description(String);

// [Wire]
pub struct Explanation(String);

// [Wire]
pub struct QuoteText(String);

// [Wire]
pub struct Reasoning(String);

// [Wire]
pub struct RecordIdentifier(String);

// [Wire]
pub struct SubscriptionHandle(i64);

// [Wire]
pub struct Importance(Magnitude);

// [Wire]
pub struct Keyword(String);

// [Wire]
pub struct Keywords(Vec<Keyword>);

// [Wire]
pub struct SearchText(String);

// [Wire]
pub struct SelectedKind(Option<Kind>);

// [Wire]
pub struct VerbatimQuote(QuoteText);

// [Wire]
pub struct Testimony(Vec<VerbatimQuote>);

// ---- Enums ----

// [Wire]
pub enum Magnitude {
    Zero,
    Minimum,
    VeryLow,
    Low,
    Medium,
    High,
    VeryHigh,
    Maximum,
}

// [Wire]
pub enum Kind {
    Decision,
    Principle,
    Correction,
    Clarification,
    Constraint,
}

// [Wire]
pub enum DomainMatch {
    Any,
    Partial(DomainScopes),
    Full(DomainScopes),
}

// [Wire]
pub enum KeywordMatch {
    Any,
    AnyKeyword(Keywords),
    AllKeywords(Keywords),
}

// [Wire]
pub enum TextMatch {
    Any,
    ContainsText(SearchText),
}

// [Wire]
pub enum ImportanceSelection {
    Any,
    ExactImportance(Importance),
    AtMostImportance(Importance),
    AtLeastImportance(Importance),
}

// [Wire]
pub enum LayerSelection {
    Any,
    SelectedLayer(Layer),
}

// [Wire]
pub enum GuardianReason {
    Duplicate,
    Contradiction,
    Matter,
    InsufficientWarrant,
    ImportanceUnsupported,
}

// [Wire]
pub enum QueryRefusal {
    InvalidDomainSelection,
}

// [Wire]
pub enum RecordEvent {
    RecordAdmitted(RecordAdmitted),
}

// ---- Structs ----

// [Wire]
pub struct Query {
    pub layer_selection: LayerSelection,
    pub domain_match: DomainMatch,
    pub keyword_match: KeywordMatch,
    pub text_match: TextMatch,
    pub selected_kind: SelectedKind,
    pub importance_selection: ImportanceSelection,
}

// [Wire]
pub struct Justification {
    pub testimony: Testimony,
    pub reasoning: Reasoning,
}

// [Wire]
pub struct Entry {
    pub layer: Layer,
    pub domains: Domains,
    pub kind: Kind,
    pub description: Description,
    pub importance: Importance,
}

// [Wire]
pub struct RecordRequest {
    pub entry: Entry,
    pub justification: Justification,
}

// [Wire]
pub struct ObservedRecord {
    pub record_identifier: RecordIdentifier,
    pub entry: Entry,
}

// [Wire]
pub struct RecordSet(Vec<ObservedRecord>);

// [Wire]
pub struct FoundRecord {
    pub record_identifier: RecordIdentifier,
    pub entry: Entry,
}

// [Wire]
pub struct RecordAdmitted {
    pub entry: Entry,
    pub record_identifier: RecordIdentifier,
}

// ---- Input newtypes ----

// [Wire]
pub struct Record(RecordRequest);

// [Wire]
pub struct Observe(Query);

// [Wire]
pub struct Lookup(RecordIdentifier);

// [Wire]
pub struct Subscribe(Query);

// [Wire]
pub struct Unsubscribe(SubscriptionHandle);

// ---- Output newtypes ----

// [Wire]
pub struct Recorded(RecordIdentifier);

// [Wire]
pub struct Observed(RecordSet);

// [Wire]
pub struct LookedUp(FoundRecord);

// [Wire]
pub struct Subscribed(SubscriptionHandle);

// [Wire]
pub struct Unsubscribed(SubscriptionHandle);

// ---- Refusal types ----

// [Wire]
pub struct AdmissionRejected {
    pub guardian_reason: GuardianReason,
    pub explanation: Explanation,
}

// [Wire]
pub struct QueryRejected {
    pub query_refusal: QueryRefusal,
    pub explanation: Explanation,
}

// [Wire]
pub struct UnknownSubscription(SubscriptionHandle);

// ---- Role trait implementations ----

impl Input for Record {}
impl Input for Observe {}
impl Input for Lookup {}
impl Input for Subscribe {}
impl Input for Unsubscribe {}

impl Output for Recorded {}
impl Output for Observed {}
impl Output for LookedUp {}
impl Output for Subscribed {}
impl Output for Unsubscribed {}

impl Refusal for AdmissionRejected {}
impl Refusal for QueryRejected {}
impl Refusal for UnknownSubscription {}

impl Stream for RecordChange {}

// ---- Refusal error implementations ----

impl std::fmt::Display for AdmissionRejected {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        std::fmt::Debug::fmt(self, formatter)
    }
}

impl std::error::Error for AdmissionRejected {}

impl std::fmt::Display for QueryRejected {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        std::fmt::Debug::fmt(self, formatter)
    }
}

impl std::error::Error for QueryRejected {}

impl std::fmt::Display for UnknownSubscription {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        std::fmt::Debug::fmt(self, formatter)
    }
}

impl std::error::Error for UnknownSubscription {}

// ---- Stream wrapper ----

// [Wire]
pub struct RecordChange(RecordEvent);

// ---- Envelope enums ----

// [Wire]
pub enum PsycheRequest {
    Record(Record),
    Observe(Observe),
    Lookup(Lookup),
    Subscribe(Subscribe),
    Unsubscribe(Unsubscribe),
}

// [Wire]
pub enum PsycheReply {
    Recorded(Recorded),
    Observed(Observed),
    LookedUp(LookedUp),
    Subscribed(Subscribed),
    Unsubscribed(Unsubscribed),
}

// [Wire]
pub enum PsycheRefusal {
    AdmissionRejected(AdmissionRejected),
    QueryRejected(QueryRejected),
    UnknownSubscription(UnknownSubscription),
}
```

### nexus.rs

Generated from nexus.ethos. Lives in the `psyche` component crate.
Nexus types carry no rkyv preamble (Plain attribute).

```rust
// @generated by ethos-rust from an authority-verified psyche nexus source
// source-digest: blake3:<64-hex-chars>

use signal_psyche::{
    Entry, RecordSet, RecordRequest, RecordIdentifier,
    FoundRecord, GuardianReason, Query, RecordEvent,
};

// ---- Decision types ----

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum AdmissionDecision {
    Accepted,
    Rejected(GuardianReason),
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum GuardianDecision {
    Admit,
    Refuse(GuardianReason),
}

// ---- Traits ----

pub trait SignalAdmission: Send {
    fn admit(&self, argument_0: RecordRequest) -> AdmissionDecision;
}

pub trait AgentGuardian: Send {
    fn guard(&self, argument_0: Entry, argument_1: RecordSet) -> GuardianDecision;
}

pub trait RecordStore: Send {
    fn store(&self, argument_0: Entry) -> RecordIdentifier;
    fn retrieve(&self, argument_0: RecordIdentifier) -> FoundRecord;
    fn query(&self, argument_0: Query) -> RecordSet;
}

pub trait RecordChangeEmitter: Send {
    fn emit(&self, argument_0: RecordEvent);
}
```

### sema.rs

Generated from sema.ethos. Lives in the `psyche` component crate.
Sema record types carry the Wire preamble (they are persisted
through rkyv). Table specifications are type aliases.

```rust
// @generated by ethos-rust from an authority-verified psyche sema source
// source-digest: blake3:<64-hex-chars>

use signal_psyche::{Entry, RecordIdentifier};

// ---- Record types ----

// [Wire]
pub struct StoredRecord {
    pub record_identifier: RecordIdentifier,
    pub entry: Entry,
}

// ---- Table specifications ----

pub type RecordsTable = (StoredRecord, RecordIdentifier);
```

## Part 3: Coverage Verification

The fixture forces all three output classes per the bead requirement.

**Signal (interface.ethos -> signal.rs):**
- Request: `Record.RecordRequest` (and four other input operations)
- Reply: `Recorded.RecordIdentifier` (and four other output responses)
- Typed refusal: `AdmissionRejected.{GuardianReason Explanation}` --
  a multi-field struct with an enum reason and a string explanation,
  generating `impl Refusal`, `impl Display`, `impl Error`
- Subscription event: `RecordChange.RecordEvent` in the Stream
  section, with `RecordEvent.[RecordAdmitted]` carrying
  `{Entry RecordIdentifier}` per event

**Nexus (nexus.ethos -> nexus.rs):**
- Major Nexus operation with typed input/output:
  `SignalAdmission.{admit.{RecordRequest AdmissionDecision}}` --
  takes `RecordRequest` (typed input), returns `AdmissionDecision`
  (typed output enum with `Accepted` and `Rejected.GuardianReason`
  variants)
- Three additional traits with full method signatures demonstrate the
  generator handles multi-method traits and varied return types

**Sema (sema.ethos -> sema.rs):**
- Sema record: `StoredRecord.{RecordIdentifier Entry}` -- persisted
  struct keyed by a domain identifier
- Key projection: `RecordIdentifier` -- the key type by which stored
  records are looked up
- Table specification: `records.{StoredRecord RecordIdentifier}` --
  generates `type RecordsTable = (StoredRecord, RecordIdentifier)`

**Connecting traits/generics without string dispatch:**
- `Entry` is defined in interface.ethos, imported by nexus.ethos
  (`interface.[Entry ...]`) for trait method signatures, and imported
  by sema.ethos (`interface.[Entry RecordIdentifier]`) for storage.
  In generated Rust, nexus.rs and sema.rs both
  `use signal_psyche::Entry`. No string dispatch; all references are
  typed imports at the Ethos level and `use` paths at the Rust level.
- `RecordIdentifier` follows the same cross-file path.
- `GuardianReason` flows from interface shared types through
  nexus decision types.
- Static typed metadata: the `RecordsTable` type alias encodes
  the record-key relationship as a type-level pair, not a string
  table name.

**Top-level layer enum:**
- `Layer.[Spirit Intent Vision]` declared in interface shared types,
  structurally embedded in `Entry.{Layer ...}`, flows through every
  record path in all three generated files.

## Part 4: Open Forks

Genuine design questions the psyche has not ruled on. Listed as named
forks; the managing flow carries them to the psyche for ruling. None
are silently resolved in the fixture text above -- each is held at
the documented default.

### Fork 1: Stream section position

The blessed fixture (2026-08-07) places the Stream section as the
fourth section, after refusals and before shared types:
inputs, outputs, refusals, streams, shared types. The
redesignAuditRulings say position is a "delegated bootstrap choice,
reviewable." This fixture uses that ordering.

### Fork 2: Kind variants across layers

Spirit's `Kind.[Decision Principle Correction Clarification
Constraint]` is reused for all three layers. Whether Intent and
Vision need their own kind vocabularies or share Spirit's is unruled.
The fixture uses a single shared Kind enum.

### Fork 3: Nexus section ordering

The VISION-2026-08-07 open questions list "Nexus traits-first
ordering" as unresolved. This fixture follows Spirit v14's order:
declarations first, traits second. The psyche may prefer traits
first.

### Fork 4: Stream universal trait name and shape

The stream universal trait's name and whether it carries default
implementations are explicitly open (VISION-2026-08-07 open
questions). This fixture uses `Stream` as the trait name, matching
the pattern of `Input`, `Output`, `Refusal`.

### Fork 5: Subscribe/Unsubscribe naming

The blessed fixture (signal-domain observer) uses `Tap`/`Untap`
naming for stream initiation and termination. This fixture uses
`Subscribe`/`Unsubscribe` as more semantically appropriate for a
record observation service. The naming is a presentational choice
for psyche ruling.

### Fork 6: Meta interface inclusion

The psyche component's metasocket signal repo (`meta-signal-psyche`)
requires its own interface fixture (meta.ethos) for daemon
configuration, import, and head-observation operations. Spirit v14
has a meta.ethos covering `Configure`, `Import`, `ObserveHead`,
`ObserveHeadObject`. This fixture does not include the meta interface
because the bead scope names only signal.rs, nexus.rs, sema.rs. The
meta interface is a known additional deliverable.

### Fork 7: VerbatimQuote double-newtype chain

`VerbatimQuote.QuoteText` where `QuoteText.String` creates a
two-deep newtype chain. The psyche expressed dislike for double
newtype wrapping (2026-08-07). Options: (a) keep both layers for
semantic precision, (b) collapse to `VerbatimQuote.String`, or
(c) drop `VerbatimQuote` and use `QuoteText` directly in
`Testimony.Vector<QuoteText>`.

### Fork 8: Envelope enum naming

The generated envelope enums (`PsycheRequest`, `PsycheReply`,
`PsycheRefusal`) are named by convention: `<Component><Role>`. This
naming is not psyche-ruled; it follows the schema-rust precedent. The
relationship to the universal signal repo wrapping enum (which wraps
all component request enums) is structurally implied but the
universal repo name is itself unruled (primary-xqb.8.3 is blocked
on it).

### Fork 9: Ethos source file placement

The psyche ruled that "the ethos code can live with the component."
This fixture assumes all three Ethos source files (interface.ethos,
nexus.ethos, sema.ethos) reside in the psyche component repository.
The generator reads them there and distributes generated output:
signal.rs to `signal-psyche`, nexus.rs and sema.rs to `psyche`. The
alternative -- Ethos source in each destination repo -- would split
co-designed files across repositories.

### Fork 10: RecordSet as newtype versus named type

`RecordSet.Vector<ObservedRecord>` is a newtype wrapping a vector.
In generated Rust, this becomes `pub struct RecordSet(Vec<ObservedRecord>)`.
Whether collection newtypes are always generated or whether the
generator should inline `Vec<ObservedRecord>` at use sites is a
generator policy question. The fixture follows Spirit v14's explicit
naming.
