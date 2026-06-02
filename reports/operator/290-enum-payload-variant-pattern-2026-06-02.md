[Enum-payload variant pattern. Intent search + operator vision. 2026-06-02.]

# 290 — Enum payloads as compact branch data

The pattern the psyche pointed at is real and older than the immediate
`Busy` example:

```schema
Output [(Busy BusyReason)]
BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]
```

The generated value is:

```nota
(Busy DatabaseOverloaded)
```

That means `Output::Busy` is a data-carrying variant, and its payload is
another enum. The payload is not a report struct unless the data is actually a
product of multiple independent facts.

## Intent Search

The strongest intent records are:

- `73` — data-carrying enum variants are branches; unit enums are leaves.
- `437` — vectors are enum-like choice surfaces; variants are unit symbols or
  data-carrying parenthesized records.
- `1269` — notation must truthfully represent the underlying data shape; do
  not introduce empty wrappers to make an encoding fit.
- `1294` and `1295` — enum bodies are homogeneous vectors of variant-signature
  objects; data variants are `(VariantName PayloadType)`, unit variants are
  bare symbols.
- `1301` and `1302` — do not split one semantic object into source/artifact
  mirrors without a real semantic projection.
- `1466` — `Busy` should try the compact enum-payload shape, carrying
  `BusyReason` directly instead of immediately wrapping reason and retry
  guidance in `BusyReport`.

The intent layer already had the general rule. The missed piece was applying
it to ordinary runtime replies: a reply variant whose interesting payload is a
choice should carry that choice enum directly.

## Core Rule

Use a direct enum payload when the data carried by a variant is one axis of
choice.

```schema
Output [(Busy BusyReason)]
BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]
```

Use a struct payload when the carried value is a product of independent facts.

```schema
Output [(RecordAccepted SemaReceipt)]
SemaReceipt { RecordIdentifier * DatabaseMarker * }
```

Use a data-carrying nested enum when only some choices need extra data.

```schema
Output [(Busy BusyReason)]
BusyReason [(DatabaseOverloaded RetryGuidance) ResourceDisconnected OtherBusyReason]
RetryGuidance [(RetryAfter Integer) RetryLater]
```

This keeps the semantic root as `Busy`, keeps the reason axis as `BusyReason`,
and does not invent a `BusyReport` wrapper unless the reply genuinely becomes
a multi-field report.

## Header-Declared Inline Enum Sugar

The stronger sugar from Spirit records `1467` and `1468` is:

```schema
Output [
  RecordAccepted
  RecordsObserved
  (Busy [DatabaseOverloaded ResourceDisconnected OtherBusyReason])
  Rejected
]
```

The header is still a vector of variant-signature objects:

- `RecordAccepted` is one signature object.
- `(Busy [DatabaseOverloaded ResourceDisconnected OtherBusyReason])` is one
  signature object.
- `Rejected` is one signature object.

The inline bracket body declares the payload enum at the header position. That
lets the header carry the small shape directly instead of forcing a separate
namespace declaration:

```schema
Output [(Busy BusyReason)]
BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]
```

The lowering target is equivalent except the inline form derives the payload
type name from context. The Rust-facing generated noun can be:

```rust
pub enum Output {
    Busy(Busy),
}

pub enum Busy {
    DatabaseOverloaded,
    ResourceDisconnected,
    OtherBusyReason,
}
```

or, if the emitter chooses a collision-avoiding contextual name:

```rust
pub enum Output {
    Busy(OutputBusy),
}

pub enum OutputBusy {
    DatabaseOverloaded,
    ResourceDisconnected,
    OtherBusyReason,
}
```

The important rule is not the exact derived name yet; it is that the header
position can declare the payload enum directly as schema data.

## Type-Table Variant Resolution

Spirit `1468` adds a second compact form:

```schema
Output [RecordAccepted RecordsObserved Busy Rejected]
```

In this form the header lists variant names without spelling whether each
variant is unit or data-carrying. The schema reader resolves against the local
type table:

- If `RecordAccepted` is a declared newtype/struct/enum, then
  `Output::RecordAccepted` carries `RecordAccepted`.
- If `RecordsObserved` is a declared type, then
  `Output::RecordsObserved` carries `RecordsObserved`.
- If `Busy` is declared inline or in the namespace, then `Output::Busy`
  carries `Busy`.
- If `Rejected` is declared, then `Output::Rejected` carries `Rejected`.
- If a listed name is not declared as a type, it is a unit variant.

That is the "header does not need to know" insight. The header can stay small
because the type table already knows which names denote payload types.

The fully explicit form remains available when the variant name and payload
type differ:

```schema
Output [(RecordAccepted SemaReceipt) (Rejected SignalRejection)]
```

The type-table shorthand is only for same-name variants.

## Ambiguity Policy

The shorthand introduces one real ambiguity: a schema author may want a unit
variant named `Busy` even though a type `Busy` exists in scope. The current lean
is:

- same-name resolution is data-carrying when a type exists;
- use an explicit unit marker later if the rare conflict appears;
- until that marker exists, avoid declaring a same-named type when the variant
  should be unit.

This is consistent with the broader schema direction: compact headers are the
normal human surface, and explicit records are the escape hatch when the human
surface would be ambiguous.

## Shape Comparison

Bad shape:

```schema
Output [(Busy BusyReport)]
BusyReport { BusyReason * RetryGuidance * DatabaseMarker * }
BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]
RetryGuidance [(RetryAfter Integer) RetryLater]
```

That makes every busy reply pretend to be a three-field product. It is too
heavy when the immediate runtime decision is only "busy because this reason."
It also hides the useful choice one layer deeper than necessary.

Better immediate shape:

```schema
Output [(Busy BusyReason)]
BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]
```

Better future shape if retry guidance is real:

```schema
Output [(Busy BusyReason)]
BusyReason [(DatabaseOverloaded RetryGuidance) ResourceDisconnected OtherBusyReason]
RetryGuidance [(RetryAfter Integer) RetryLater]
```

The second future shape still avoids `BusyReport`: the guidance belongs to the
reason variant that needs it.

## Generated Rust

The schema above should emit:

```rust
pub enum Output {
    Busy(BusyReason),
    // other variants...
}

pub enum BusyReason {
    DatabaseOverloaded,
    ResourceDisconnected,
    OtherBusyReason,
}
```

If guidance is added:

```rust
pub enum BusyReason {
    DatabaseOverloaded(RetryGuidance),
    ResourceDisconnected,
    OtherBusyReason,
}

pub enum RetryGuidance {
    RetryAfter(Integer),
    RetryLater,
}
```

The nesting is honest: `Busy` is the reply branch; `BusyReason` is the reason
choice; `RetryGuidance` is only carried where it is semantically present.

## Assembled Schema

The authored schema:

```schema
Output [(Busy BusyReason)]
BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]
```

lowers to an assembled schema shape like:

```asschema
[(Busy (Some (Plain BusyReason)))]
(Public BusyReason (Enum [
  (DatabaseOverloaded None)
  (ResourceDisconnected None)
  (OtherBusyReason None)
]))
```

With guidance:

```asschema
[(Busy (Some (Plain BusyReason)))]
(Public BusyReason (Enum [
  (DatabaseOverloaded (Some (Plain RetryGuidance)))
  (ResourceDisconnected None)
  (OtherBusyReason None)
]))
(Public RetryGuidance (Enum [
  (RetryAfter (Some Integer))
  (RetryLater None)
]))
```

The assembled form is still a homogeneous vector of enum-variant definitions.
The payload is `Optional<TypeReference>`; the type reference can point to an
enum just as naturally as it points to a struct or newtype.

## Header And Trace Consequence

This pattern is especially important for the trace/header work.

```mermaid
flowchart LR
  Root[Output Busy] --> Payload[BusyReason]
  Payload --> Reason[DatabaseOverloaded]
```

Compact trace can name the root activation:

```text
OutputBusy
```

Extended trace can include the second enum row:

```text
OutputBusy.DatabaseOverloaded
```

That is exactly the direction in Spirit records `1405` and `1408`: trace names
come from the schema-defined interface header, including nested enum rows when
the payload object is itself an enum.

## Operator Lean

For `spirit-next`, the immediate implementation should use:

```schema
Output [
  (RecordAccepted SemaReceipt)
  (RecordsObserved ObservedRecords)
  (RecordFound FoundRecord)
  (RecordsCounted CountedRecords)
  (RecordRemoved RemoveReceipt)
  (Busy BusyReason)
  (Error ErrorReport)
  (Rejected SignalRejection)
]

BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]
```

That is the current implementable form because schema-next already accepts
explicit variant payload types. The cleaner future source form is:

```schema
Output [
  RecordAccepted
  RecordsObserved
  RecordFound
  RecordsCounted
  RecordRemoved
  (Busy [DatabaseOverloaded ResourceDisconnected OtherBusyReason])
  Error
  Rejected
]
```

with same-name type-table resolution for the non-`Busy` payload variants.

The current `BusyReport` direction from report
`reports/operator/289-nexus-internal-control-interface-2026-06-02.md` is
superseded by this pattern. The runtime can still know the `DatabaseMarker`
internally through Nexus/SEMA state, but the wire `Busy` reply should not carry
that marker unless the client needs it as part of the busy reply semantics.

If clients later need structured retry behavior, add it as a nested enum
payload:

```schema
BusyReason [(DatabaseOverloaded RetryGuidance) ResourceDisconnected OtherBusyReason]
```

Do not revive `BusyReport` as a convenience wrapper unless there are at least
two independent facts that all `Busy` replies must carry.

## Implementation Consequence

The schema-rust emitter does not need a new kind for this. It already supports
enum variants carrying named payload types. What needs to stay disciplined is
the schema authoring choice:

- `Variant PayloadEnum` is valid and desirable.
- `Variant PayloadStruct` is valid when the payload is product data.
- `Variant WrapperStruct` is wrong when the wrapper only exists to hold one
  enum that could be the payload directly.

The next implementation pass should finish the `spirit-next` `Busy` slice in
the compact shape, and the tests should assert the live value:

```nota
(Busy DatabaseOverloaded)
```

not:

```nota
(Busy (DatabaseOverloaded RetryLater ...))
```

unless the schema intentionally grows a nested data-carrying reason variant.
