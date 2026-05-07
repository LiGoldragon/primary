# Persona audit — naming + abstraction discipline

Date: 2026-05-06
Author: Claude (designer)
Scope: `/git/github.com/LiGoldragon/persona` (single commit `dd96d3a`,
"persona: scaffold core state contract").
Reference doctrine: `lore/rust/style.md`, `lore/programming/naming.md`,
`lore/programming/abstractions.md`. Reference example:
`/git/github.com/LiGoldragon/horizon-rs` (recent canonical Rust shape
in the criome space).

---

## Summary

The scaffold compiles and the schema has the right shape — typed
newtypes for identifiers, closed enums for kinds, `thiserror` per-crate
`Error`. The structural problems are mostly **naming**: redundant
project prefixes, redundant suffixes, verb-shaped struct names, and
one-concept-two-types pairs. None block the work; all should be fixed
before any consumer pins this surface.

The horizon-rs reference is the canonical shape: bare nouns per module
(`Cluster`, `Node`, `User`, `Horizon`), prefixes only when *meaningful*
(`ClusterProposal` vs `NodeProposal` are two different proposal kinds —
the prefix carries information), suffixes only when distinguishing
two concepts about the same noun (`Cluster` vs `ClusterTrust`).

Persona violates this in five distinct ways.

---

## Findings

### 1. `Persona`-prefixed types — redundant with crate name

`PersonaRequest`, `PersonaOutput`, `PersonaState`,
`PersonaStateSnapshot`, `PersonaObject`, `PersonaDocument`. At every
use site these read as `persona::PersonaRequest` —
`persona::persona-request`. The prefix carries no information beyond
the namespace.

Compare horizon-rs: the crate is `horizon-rs` but the central type is
`Horizon`, not `HorizonHorizon`. `Cluster`, `Node`, `User` —
unprefixed.

Suggested rename:

| Current | Suggested |
|---|---|
| `PersonaRequest` | `Request` |
| `PersonaOutput` | `Output` (or `Reply`) |
| `PersonaState` | `State` |
| `PersonaStateSnapshot` | `Snapshot` (and consider folding — see #5) |
| `PersonaObject` | `Object` |
| `PersonaDocument` | `Document` |

### 2. `*Record` suffix on every schema record — redundant

`HarnessRecord`, `MessageRecord`, `AuthorizationRecord`,
`DeliveryRecord`, `EventRecord`, `StateCursorRecord`,
`HarnessObservationRecord`, `PendingInteractionRecord`,
`StateTransitionRecord`, `AttachmentRecord`. The whole `schema.rs`
file is records-by-construction (every type carries `#[derive(NotaRecord)]`);
the `*Record` suffix marks something the codec already encodes at the
trait level.

Compare horizon-rs: `Node`, not `NodeRecord`; `Cluster`, not
`ClusterRecord`; `User`, not `UserRecord`. The trait derive is the
record marker; the type name is the noun.

Suggested rename: drop `Record` from every variant. `HarnessRecord` →
`Harness`, `MessageRecord` → `Message`, etc. `Vec<Harness>` reads
naturally; `Vec<HarnessRecord>` reads as ceremony.

### 3. Verb-shaped struct names — `ValidateObject`, `ValidateDocument`, `DescribeSchema`

Per `lore/programming/abstractions.md` and `lore/rust/style.md`:
behavior lives on types; struct names are nouns naming what the value
*is*, not what it *does*. `ValidateObject` reads as an imperative —
"validate the object" — with the implicit type unstated.

These are request envelope kinds, so they need to dispatch via the
codec's record head. The verb-shape works mechanically (the head
identifier matches the struct name), but it puts an action where a
noun belongs.

Two cleaner shapes, pick one:

- **Noun the request:** rename to the *concept of asking* —
  `ObjectValidation`, `DocumentValidation`, `SchemaDescription`. Each
  reads as "a request for X." The dispatcher's match arms become
  `"ObjectValidation" => …`. Same machinery, noun-first names.
- **Method on the noun:** if validation belongs on `Object` /
  `Document` themselves, replace the request kind with
  `Object::validate(&self) -> ValidatedObject` and let `Request` be
  a smaller envelope shape. This matches horizon-rs's
  `ClusterProposal::project(viewpoint) -> Horizon` shape — the verb
  lives on the noun that owns it.

The first is the lighter rename; the second is the deeper alignment
with the lore.

### 4. Mixed `*Name` vs `*Identifier` — inconsistent suffix

```
HarnessName, PrincipalName              → "Name"
MessageIdentifier, DeliveryIdentifier,
EventIdentifier, InteractionIdentifier,
TransitionIdentifier                    → "Identifier"
```

The two groups are doing the same thing (newtype-wrap a `String` for
identity). Picking different suffixes for them costs readers a mental
lookup at every use site about which group a given type belongs to.

Compare horizon-rs: `ClusterName`, `NodeName`, `UserName`,
`DomainName` — uniform `*Name`. `GithubId`, `Keygrip` — when they
truly are *id-shaped* (opaque identifier strings issued elsewhere),
they get `*Id` or the natural domain noun.

Suggested rename: unify under `*Id` for the identifier group
(`MessageId`, `DeliveryId`, `EventId`, `InteractionId`,
`TransitionId`). `id` is in the permitted-acronym list per
`lore/programming/naming.md`. Keep `*Name` for the name group
(harness, principal — these are *names* not opaque ids).

### 5. Two types for one concept — `State` / `StateSnapshot`

`state.rs::PersonaState` is a wrapper that holds a
`PersonaStateSnapshot` and has methods (`from_snapshot`, `snapshot`,
`into_snapshot`, `revision`, `record_transition`). The wrapped type
carries the data; the wrapper carries the methods.

This is the `Item` / `ItemDetails` pattern that
`lore/rust/style.md` §"One type per concept — no `-Details` /
`-Info` companions" calls out: the base was designed too thin
(snapshot = data only) and the verbs ended up on a sibling type.

The fix per the lore is to **make the data type the noun and put the
methods on it**. One `State` struct, with the fields currently in
`PersonaStateSnapshot` and the methods currently on `PersonaState`.
That's a single noun owning its affordances.

If the mutation/immutability split is genuinely load-bearing (e.g. the
durable engine wants an inert serialised form distinct from the
in-memory holder), name them by what each *is*: `State` (the in-memory
holder) and `StateBytes` / `Frozen<State>` / similar. The shape
"`X`/`XSnapshot`" is what the lore rejects.

---

## Smaller observations

- **`example_objects()`** in `schema.rs` is 90+ lines constructing
  one Vec of examples. It's borderline-ok as test fixture data but
  fits the lore's "long function with multiple responsibilities"
  smell. If it's exclusively for tests/examples, `#[cfg(test)]` or
  move to `tests/`. If it's seed data for the daemon, name what each
  bundle is.
- **End-of-input check duplicated** between `PersonaRequest::from_nota`
  and `PersonaDocument::from_nota`. Same six lines. Either make it a
  small helper inside the crate, or — better — push it into
  `nota_codec::Decoder` as an `expect_end()` method and let the codec
  own the rule. Probably a missing nota-codec primitive.
- **`#[derive(NotaRecord)]` on `DescribeSchema {}`** — the empty-record
  shape works, but it's worth checking whether nota's grammar wants
  `(DescribeSchema)` to round-trip through a real `NotaRecord` derive
  or whether a unit struct + manual encode/decode would be cleaner.
- **`lib.rs`** is a clean re-export shim — good, nothing to change.
- **`error.rs`** uses thiserror with `#[from]` for foreign error types,
  no `anyhow`/`eyre` — clean, matches the doctrine.
- **`HarnessRole::{Operator, Designer, Observer}`** lines up with
  `~/primary`'s role taxonomy. Good landing.

---

## Suggested rename pass (concrete diff sketch)

```rust
// schema.rs
pub struct Harness { … }                  // was HarnessRecord
pub struct Message { … }                  // was MessageRecord
pub struct Authorization { … }            // was AuthorizationRecord
pub struct Delivery { … }                 // was DeliveryRecord
pub struct Event { … }                    // was EventRecord
pub struct StateCursor { … }              // was StateCursorRecord
pub struct HarnessObservation { … }       // was HarnessObservationRecord
pub struct PendingInteraction { … }       // was PendingInteractionRecord
pub struct StateTransition { … }          // was StateTransitionRecord
pub struct Attachment { … }               // was AttachmentRecord

pub struct Snapshot { … }                 // was PersonaStateSnapshot
pub enum Object { … }                     // was PersonaObject
pub struct Document { … }                 // was PersonaDocument

pub struct MessageId(String);             // was MessageIdentifier
pub struct DeliveryId(String);            // was DeliveryIdentifier
pub struct EventId(String);               // was EventIdentifier
pub struct InteractionId(String);         // was InteractionIdentifier
pub struct TransitionId(String);          // was TransitionIdentifier
// HarnessName, PrincipalName stay as-is (genuine names)

// request.rs
pub struct ObjectValidation { object: Object }     // was ValidateObject
pub struct DocumentValidation { document: Document } // was ValidateDocument
pub struct SchemaDescription {}                     // was DescribeSchema

pub enum Request { … }    // was PersonaRequest
pub enum Output { … }     // was PersonaOutput  (or Reply)

// state.rs
// Either fold PersonaState into Snapshot (make Snapshot own the methods),
// or keep one mutable holder named State that owns a Snapshot field.
// Either way: drop the `Persona` prefix.
```

The dispatcher match arms in
`NotaDecode for PersonaRequest::decode` change from
`"ValidateObject" => …` to `"ObjectValidation" => …`. The wire
shape changes — fine while there are no external consumers.

---

## Questions

1. **Is the request-record dispatch by head identifier load-bearing
   long-term?** If yes (the wire is "the record's name *is* the
   verb"), then noun-shaped names (`ObjectValidation`) keep the
   dispatch but read as nouns. If the dispatch is going to evolve to
   typed verbs at a different boundary, the `Validate*` shape might
   intentionally encode the imperative — worth confirming with the
   operator before the rename.
2. **Is `PersonaState` vs `PersonaStateSnapshot` deliberately split**
   to model "in-memory holder" vs "durable record," anticipating the
   redb/rkyv landing? If so, name them by what they *are*; if not,
   collapse.
3. **Are `MessageIdentifier` etc. issued by Persona or arrived from
   outside?** If outside-issued (some other component mints them),
   `*Id` might be the wrong suffix and the upstream's name should
   carry through. Worth a quick check against the architecture doc.

---

## Recommendation

Land the renames as a single rename pass before any consumer pins this
surface. The schema scaffold is small enough that one commit
("persona: rename types per workspace style") covers it. After that,
the schema reads cleanly against the lore and the horizon-rs reference,
and the next layer (daemon + redb tables) lands without inheriting the
prefix/suffix overhead.

The deeper question (#1 in Questions) — whether request kinds should
be noun-records dispatched by name, or methods on the noun being
acted on — is worth one focused conversation with the operator. Both
shapes work; the second is more aligned with `lore/programming/abstractions.md`.
