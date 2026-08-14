# Psyche Stage 2 Ethos Fixture Reconciliation - 2026-08-14

Status: design proposal for psyche review. This document is not a vocabulary
ruling, a runtime design, or authorization to add dependencies or generated
files to any repository.

Psyche is the first Ethos fixture. The ruled component anatomy is `psyche`,
`signal-psyche`, and `meta-signal-psyche`; meta Signal is required. The
ordinary and meta vocabularies are not yet ruled. This proposal gives one small
ordinary candidate and no meta source.

## Evidence and current capability boundary

The 2026-08-11 fixture is donor evidence, not current authority. It assumed a
larger Spirit-derived surface and selected matters that remain open. Its Rkyv
preamble, role implementations, component request/reply/refusal unions,
source digest marker, `Send` bounds, and cross-repository placement assumption
are omitted here.

Current observed facts are narrower.

- `ethos-rust` at `c0f4e11` is a filename and artifact scaffold only. It has
  no Ethos reader, abstract syntax tree, or lowering implementation.
- Protos is the ruled universal home for Input, Output, Refusal, and Stream
  membership. Current Protos does not yet expose that taxonomy; it is a
  prerequisite gap for a complete generated Signal module.
- `psyche`, `signal-psyche`, and `meta-signal-psyche` are deliberately empty
  scaffolds. Their current Cargo dependency graphs are empty.
- `ethos-rust` binds one source directory to one output directory, while the
  candidate below has an ordinary Signal artifact and component-private
  artifacts. No promotion mechanism bridges that mismatch today.

The component architecture standard says Signal is portable Rkyv. This
proposal does not choose derive settings, archive details, or frame anatomy.
Cap'n Proto universal Signal and routable Signal are deferred.

## Minimal candidate Ethos source

These three files are exact proposed text for review only. Labeled payload
membership is the proposal. Header version, empty imports, section order,
generic spelling, lower-case binding, and this form itself are held grammar
questions below.

### `signal.ethos`

```text
Interface.{1 0 0}
[]
{
  [
    Record.Entry
    Subscribe.Layer
    Unsubscribe.SubscriptionHandle
  ]
  [
    Recorded.RecordIdentifier
    Subscribed.SubscriptionHandle
    Unsubscribed.SubscriptionHandle
  ]
  [
    AdmissionRejected.AdmissionRefusal
    UnknownSubscription.SubscriptionHandle
  ]
  [
    RecordChange.RecordEvent
  ]
  [
    Layer.[Spirit Intent Vision]
    Description.String
    RecordIdentifier.String
    SubscriptionHandle.Integer
    Entry.{Layer Description}
    AdmissionRefusal.[Duplicate InvalidRequest]
    RecordEvent.[RecordRecorded.RecordIdentifier]
  ]
}
```

The left names are Ethos operation labels. They do not emit Rust wrapper types
in this candidate. This is the proposed non-double, non-single-field lowering.

Role membership matrix:

```text
inputs   Input   Record -> Entry
                 Subscribe -> Layer
                 Unsubscribe -> SubscriptionHandle
outputs  Output  Recorded -> RecordIdentifier
                 Subscribed -> SubscriptionHandle
                 Unsubscribed -> SubscriptionHandle
refusals Refusal AdmissionRejected -> AdmissionRefusal
                 UnknownSubscription -> SubscriptionHandle
stream   Stream  RecordChange -> RecordEvent
```

The role home is settled: Protos. The unresolved question is exact trait
anatomy only: are these marker traits, do they require methods, and what are
those signatures? Repeated `SubscriptionHandle` memberships and preservation
of operation labels require that anatomy, including the role or envelope home
for operation identity. No compiling membership implementations may be written
until that prerequisite exists.

`Subscribe` selects a `Layer`; `Unsubscribe` carries a handle. `Subscribed`
and `Unsubscribed` both carry a handle. `RecordEvent` is
`RecordRecorded(RecordIdentifier)`. Handle and event correlation, as well as
any envelope, remain held.

### `nexus.ethos`

```text
Nexus.{1 0 0}
[signal.[AdmissionRefusal Entry RecordIdentifier]]
{
  [
    AdmissionDecision.[Accepted.RecordIdentifier Rejected.AdmissionRefusal]
  ]
  [
    Admitting.{admit.{Entry AdmissionDecision}}
  ]
}
```

This forces one internal behavior trait. `Accepted` carries a
`RecordIdentifier`; no daemon or service implementation is proposed.

### `sema.ethos`

```text
Sema.{1 0 0}
[signal.[Entry RecordIdentifier]]
{
  [
    StoredRecord.{RecordIdentifier Entry}
    Records.Vector<StoredRecord>
    RecordsTable.{Records RecordIdentifier}
  ]
  [
    records.RecordsTable
  ]
}
```

`Records.Vector<StoredRecord>` is a generic application only. It does not
declare a generic parameter or trait bound. Psyche must say whether acceptance
requires either one and, if so, give the exact Ethos spelling. The lower-case
`records.RecordsTable` syntax forces the table-anatomy question; its complete
Rust correspondence is intentionally unresolved below.

## Exact candidate real-form Rust core

The code below is exact candidate real-form Rust core, not a complete generated
module. Main types precede the only trait declaration. There are no runtime
bodies, role implementations, archive derives, envelopes, revision fields,
framing types, provenance markers, or `Send` bounds.

A complete generated `signal.rs` must additionally carry portable-Rkyv Signal
form support and the mandatory Protos role memberships. Two held completion
branches remain:

1. Protos publishes marker role traits, so the generator writes membership
   implementations with no method bodies.
2. Protos publishes role traits with required methods, so the generator writes
   the ruled method implementations after their signatures and obligations are
   specified.

No third completion branch is assumed.

### `signal.rs`

```rust
pub enum Layer {
    Spirit,
    Intent,
    Vision,
}

pub struct Description(pub String);
pub struct RecordIdentifier(pub String);
pub struct SubscriptionHandle(pub i64);

pub struct Entry {
    pub layer: Layer,
    pub description: Description,
}

pub enum AdmissionRefusal {
    Duplicate,
    InvalidRequest,
}

pub enum RecordEvent {
    RecordRecorded(RecordIdentifier),
}
```

Labeled payload membership is the candidate grammar. Direct bare membership is
an alternate grammar fork. Neither form creates a Rust wrapper type in this
candidate.

### `nexus.rs`

`/* SIGNAL TYPES PATH: HELD */`

If a Cargo edge is ruled, branch C is
`use signal_psyche::{AdmissionRefusal, Entry, RecordIdentifier};`.
If artifacts are installed together, branch M is
`use crate::signal::{AdmissionRefusal, Entry, RecordIdentifier};`.
Neither branch is selected, so this is not a complete compiling module.

```rust
pub enum AdmissionDecision {
    Accepted(RecordIdentifier),
    Rejected(AdmissionRefusal),
}

pub trait Admitting {
    fn admit(&self, entry: Entry) -> AdmissionDecision;
}
```

### `sema.rs`

`/* SIGNAL TYPES PATH: HELD */`

For `Entry` and `RecordIdentifier`, branch C is
`use signal_psyche::{Entry, RecordIdentifier};`; branch M is
`use crate::signal::{Entry, RecordIdentifier};`. Neither is selected, so this
is candidate data core rather than a complete compiling module.

```rust
pub struct StoredRecord {
    pub record_identifier: RecordIdentifier,
    pub entry: Entry,
}

pub struct Records(pub Vec<StoredRecord>);

pub struct RecordsTable {
    pub records: Records,
    pub key: RecordIdentifier,
}
```

The lower-case declaration has two held lowering branches.

1. T1 is the data core shown above: `RecordsTable` is data-bearing, and
   `records.RecordsTable` has no separate Rust representation.
2. T2 is a table capability or associated Record-and-Key representation. Its
   trait and its data-bearing home require a ruling before Rust can be shown.

This proposal creates neither a zero-sized namespace nor a static value. The
`pub` fields and tuple fields are candidate cross-crate usability, not a
settled constructor or visibility policy.

## Generation boundary that this proposal does not fill

Ethos and Datom are different languages. They may ride the Protos substrate,
and Ethos is ruled to depend on Datom for Signal intake, but this proposal does
not define the Ethos reader or a new text reader. Any implementation must use
the eventually ruled language machinery rather than independently interpreting
the source text.

Generated Rust is ruled to be committed for normal tooling. The current
one-output-directory `ethos-rust` scaffold cannot decide whether the three
candidate files are installed together, promoted across repositories, or use
another approved artifact boundary.

## Questions for psyche

### Ordinary and meta vocabulary

- Is the labeled ordinary candidate exactly the listed operation labels and
  payloads?
- How is operation identity preserved in Signal without Rust wrapper types?
- Do Protos role traits accept operation identity, or does an envelope own it?
- Which configuration and owner operations belong in mandatory
  `meta-signal-psyche`? No candidate meta source is offered until that
  vocabulary is ruled.
- Does `Layer.[Spirit Intent Vision]` reuse exactly the intended Spirit,
  Intent, and Vision semantics, and what concrete `Entry` content is reused?

### Artifact and Cargo boundary

- Where do `signal.ethos`, `nexus.ethos`, and `sema.ethos` live?
- Where do `signal.rs`, `nexus.rs`, and `sema.rs` land, and how may one result
  be promoted when destinations are separate repositories?
- Is the cross-crate `psyche -> signal-psyche` edge ruled, or are artifacts
  installed under one owner/module path?

### Freshness, determinism, and provenance

- What makes checked-in Rust current with its Ethos source?
- What determinism witness is required?
- Does a generated file carry source identity or authority information, and if
  so what exact fields establish it?
- How is a stale generated file rejected?

### Runtime and Sema anatomy

- What daemon, CLI, and configuration behavior follows `Admitting`?
- Is T1 or T2 the intended meaning of `records.RecordsTable`?
- Are single-field scalar and collection wrappers desired?
- Are public fields the intended construction surface, or should generated
  values have another trait-homed construction surface?

### Signal role, framing, and revision anatomy

- Are Protos role traits markers or traits with required methods? If methods,
  what exact signatures and obligations do Input, Output, Refusal, and Stream
  carry?
- Does the ordinary contract have component-wide request/reply/refusal unions?
- What contract revision anatomy, routing identity, and unknown-revision
  behavior are required?
- Which portable-Rkyv details are required now, and when do deferred Cap'n
  Proto universal Signal and routable Signal enter the design?

### Ethos grammar

- Is `Interface.{1 0 0}` the exact header and version form?
- Is `[]` the correct empty import form?
- Are the five section positions and their order correct?
- Is labeled payload membership the rule, or is direct bare membership the
  rule? In either case, how does the chosen grammar lower without Rust wrapper
  types?
- Is `Records.Vector<StoredRecord>` the correct generic application, and does
  a generic parameter or bound also need declaration?
- Is `records.RecordsTable` the correct lower-case binding form?

Until these questions are ruled, this document is a small falsifiable
candidate, not a contract or implementation plan.
