# The Stream Vertical: Ethos Surface, Nomos Dotted-Chain Application, Logos Emission — 2026-08-02

Commissioned by the psyche: "go and see what that would look like on
the Nomos side of things... let's go far with the design so we don't
end up implementing a bunch of crap that I don't even like afterwards."
Manager design against the real machinery (transformer surfaces at
core-nomos 0.31.0, Logos vocabulary at core-logos 0.20.0). Everything
here is proposal for psyche review; ruled inputs are cited.

## 1. The reading rule this design rests on

At a declaration position the reader resolves the head symbol:

- Head resolves to a **Nomos object** → this is an application. The
  rest of the dotted chain and the payload bind to the object's
  declared parameters. `Stream.Observer.{...}` — a stream, named
  Observer.
- Head does not resolve to an object → the head **is the declared
  name**, and the payload's shape selects the default form: `X.Y`
  newtype, `X.[...]` enum, `X.{...}` struct.

One rule, no grammar keywords: resolution decides, spelling never does
(the seated builtins-are-prior-definitions law). Shape-implied defaults
stay name-first and free of ceremony; invoked objects announce
themselves first and take the name as their first argument — written
as data: the constructor, then its arguments.

Consequence for existing spellings, flagged for the psyche: under
object-first, the worked generic example would read
`SimpleGeneric.Sorted.{Ord Vector}` and the legacy ScopeOf shape would
read `ScopeOf.DomainScope.Domain`. The old name-first spellings were
agent constructions; nothing ruled protects them.

## 2. The authored Ethos surface

Both name placements, per the ruling that Nomos supports either.

**Name as dotted argument** (the chain form, expected house default):

```ethos
Stream.Observer.{ObserverFilter ObserverSubscription ObservationEvent}
```

**Name as first payload position:**

```ethos
Stream.{Observer ObserverFilter ObserverSubscription ObservationEvent}
```

Payload positions after the name: **open-query type, receipt type,
event type** — the three things a stream interaction needs that differ
per stream. Close and token machinery are universal and emitted.

**Inline definition variant.** The psyche asked whether the query and
response are defined inside the stream object. Both should be
admissible at each payload position: a reference to an existing type,
or an inline shape that mints the type in place —

```ethos
Stream.Observer.{
  {Topics}
  {SubscriptionToken}
  {Topic RecordIdentifier}
}
```

— where the three inline structs become real types whose visible
names are generated from the stream name and the position's role
(ObserverQuery, ObserverReceipt, ObserverEvent), authored by no one,
exactly as Rust's `T` is a generated visible name. Reference when the
type has independent life (shared with plain inputs), inline when it
exists only for this stream. Positional law intact: the position says
which role each shape fills.

## 3. The Nomos side: dotted-chain parameters

Today a structural transformer declares one binding tuple against its
payload and a single-item template:

```nomos
WireNewtype.Structural.Newtype {
  (name.Name type.Type)
  Public Invoke.WireAttributes Realize.name Private Realize.type
}
```

The stream transformer needs two new powers.

**Power one — chain bindings.** The declaration gains a second binding
tuple: the first binds the dotted chain after the head, the second
binds the payload. Arity carries the information — one tuple means
payload-only (today's transformers unchanged), two tuples mean chain
then payload. No empty tuples, no new keywords:

```nomos
Stream.Structural.Family {
  (name.Name)
  (query.Type receipt.Type event.Type)
  [ ...items... ]
}
```

A third dotted symbol is simply a second chain parameter — the
capability the psyche asked to see: `(name.Name mode.Mode)` binds
`Stream.Observer.Buffered.{...}`. Chain arity is checked; a chain
symbol with no parameter to bind is a typed refusal naming the
transformer and the excess symbol.

**Power two — a family template.** The template becomes a sequence of
emitted items rather than one item — `Structural.Family` (name open)
— because one stream declaration emits several Logos items. Existing
escape vocabulary unchanged: `Realize` for one value, `Splice` for
sequences, `Invoke` for other transformers.

Sketch of the full transformer:

```nomos
Stream.Structural.Family {
  (name.Name)
  (query.Type receipt.Type event.Type)
  [
    Newtype Realize.name Invoke.WireAttributes SubscriptionToken
    Invoke.StreamOpenMembership Realize.query Realize.name Realize.receipt
    Invoke.StreamEventMembership Realize.event Realize.name
  ]
]
```

The first item mints the stream handle type — the answer to "is
Observer a newtype": in emission, yes, a token-wrapping handle; in the
concept layer it is a stream, and the author never chose the shape.
The membership invocations emit the impl items binding query, receipt,
and event to the stream.

## 4. The Logos emission

Fully explicit, per the conciseness gradient. For
`Stream.Observer.{ObserverFilter ObserverSubscription ObservationEvent}`
the family is (sketch in the psyche-base style; TraitImpl carrier is
new vocabulary):

```logos
Public.Newtype.(
  Observer
  [ Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ]
  SubscriptionToken
)

TraitImpl.(StreamOpen ObserverFilter
  [ (Stream Observer) (Receipt ObserverSubscription) ])

TraitImpl.(StreamEvent ObservationEvent
  [ (Stream Observer) ])
```

Projected Rust (assembly, never authored):

```rust
pub struct Observer(SubscriptionToken);

impl StreamOpen for ObserverFilter {
    type Stream = Observer;
    type Receipt = ObserverSubscription;
}

impl StreamEvent for ObservationEvent {
    type Stream = Observer;
}
```

The universal traits live with Input/Output/Refusal (the `protos`
crate per the MVP recommendation): `StreamOpen` (an input that opens a
stream; associated stream and receipt), `StreamEvent` (an event bound
to its stream), and the daemon-side plumbing generic over them —
open/close/token handling written once, never per stream. Because
`StreamOpen` types are inputs, they also carry Input membership; the
Stream object emits both. The daemon runtime keys its subscription
registry by the stream type.

## 5. What this buys, checked against the inventory

- Spirit's two subscription kinds: two `Stream.` declarations.
- Orchestrate's Watch/Unwatch observation protocol: one `Stream.`
  declaration; close-by-token is the universal machinery.
- Mind's demand/backpressure subscriptions: a second Nomos object —
  `DemandStream.` — with one more payload position for the demand
  signal type; the per-need method, not an option on Stream.
- Messenger: no stream declarations, no empty anything.
- New interaction patterns forever after: new Nomos objects, zero
  grammar changes.

## 6. Engine deltas this design adds to the MVP register

- E8: chain-binding parameter tuple in transformer declarations
  (arity-selected), with typed refusals for chain/parameter mismatch.
- E9: family templates (multi-item emission) as a transformer kind.
- E10: inline-definition payloads minting role-named types with
  generated visible names.
- E11: `TraitImpl` carrier in WholeLogos (subsumed by E1's TraitDef
  work; associated-type bindings needed as shown).
- E12: universal StreamOpen/StreamEvent traits beside
  Input/Output/Refusal; daemon plumbing generic over them.

## 7. Open for psyche review

1. House default for the name: dotted chain (`Stream.Observer.{...}`)
   or payload-first — both supported; which is canonical style?
2. Inline definitions minting ObserverQuery/ObserverReceipt/
   ObserverEvent as generated visible names — acceptable?
3. Events: distinct universal `StreamEvent` trait (proposed) rather
   than Output membership — confirm.
4. Token: one universal SubscriptionToken with type-level stream
   binding (proposed) rather than per-stream token types — confirm.
5. The parse model for applications, sharpened by the psyche's
   talked-past diagnosis: one model must win at declaration positions —
   object-first (kind known after resolving the head; name is data;
   the Stream ruling) or name-first (declared name always first;
   definition classifies by resolution). If object-first generalizes,
   the historical spellings flip AND Slice 3's landed ScopeOf
   recognition (name-first shaped) flips to head-resolution. Whether
   SimpleGeneric and ScopeOf are even transformers is itself unruled.
6. The transformer-kind name for family emission (`Structural.Family`
   is a placeholder).
