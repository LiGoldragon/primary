Generated-code observations for whole-flow-ethos.md, Proposals 2 and 3, and for the two removed shared-state proposals. This is evidence for the review, not book text. Proposal 2 states only what this output and the checker's refusals show.

Method: ethos-zero at c4d82bf, built through the configured builder with no local build jobs, run as `ethos-zero 'Inspect.«<file>»'` on each proposal's Ethos example as written in the book. The sealed rules were also probed with Check: a sealed enum, a sealed type with no constructor capability, one with no trait, and a plain struct holding a sealed type in the same file are each refused (`Expected.Declaration`, then `Sealed.<Name>` three times). A no-self capability yielding `Self` or `Result<Self R>` is accepted as the sealed type's constructor, and one yielding `Option<Self>` is refused (`Sealed.V`). The output below omits the `#[rustfmt::skip]` line before each item and the `const _` blocks that assert each association.

What the output shows:
- A sealed struct (VerifiedContext) derives `rkyv::Archive`, `rkyv::Serialize`, Clone, Debug, PartialEq, Eq and Hash, and under the `datom` feature `Datomizable` alone: no `rkyv::Deserialize` and no `Composing`. Its positions are `pub(super)`, visible within the module that contains its own.
- A non-sealed enum in the same file (Refusal) derives both datom traits and `rkyv::Deserialize`.
- A shared type (WakeWaits, Counter, Clock) becomes two structs: `<Name>_State` holding the positions as `pub(super)`, and `<Name>` holding `pub(super) state: Arc<Mutex<<Name>_State>>`, deriving Clone alone. Neither derives rkyv or a datom trait.
- A `!` capability on a shared type's trait takes `&self` (`wait`, `bump`, `lap`); a `:` capability is an associated function with no self (`create`, `start`, `verified`).
- A yield bracket holding nothing generates a method returning unit (`fn bump(&self);`, `fn lap<N: Lapping>(&self, input: N);`).
- The standard-library import `std:time:[ Instant ]` is written as `std::time::Instant` in the state struct.
- Address in Proposal 2 is an alias of String, so its association with Titled asserts `String: Titled`.
- A `!` capability on a plain struct's trait takes `&mut self` (`fn bump(&mut self);` in Proposal 3).

## Proposal 2 (sealed type)

```rust
pub type Address = String;
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub enum Refusal {
    Mismatch,
    Unknown,
}
#[derive(rkyv::Archive, rkyv::Serialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable))]
pub struct VerifiedContext {
    pub(super) address: Address,
    pub(super) string_vector: std::vec::Vec<String>,
}
pub trait Titled {
    fn title(&self) -> String;
}
pub trait Requested {
    fn address(&self) -> Address;
}
pub trait Composed {
    fn modules(&self) -> std::vec::Vec<String>;
}
pub trait Verifying {
    fn verified<N: Requested, O: Composed>(
        input_0: N,
        input_1: O,
    ) -> std::result::Result<Self, Refusal>
    where
        Self: Sized;
    fn text(&self) -> String;
}
```

## Removed: shared state (the former Proposal 4)

```rust
pub type PaneId = String;
pub struct WakeWaits_State {
    pub(super) pane_id_vector: std::vec::Vec<PaneId>,
    pub(super) integer: i64,
}
#[derive(Clone)]
pub struct WakeWaits {
    pub(super) state: std::sync::Arc<std::sync::Mutex<WakeWaits_State>>,
}
pub trait Paned {
    fn pane(&self) -> PaneId;
}
pub trait Waiting {
    fn waits(&self) -> std::vec::Vec<PaneId>;
    fn wait<N: Paned>(&self, input: N) -> i64;
    fn create() -> Self
    where
        Self: Sized;
}
```

## Removed example: empty yield on a shared type (the former Proposal 5's example)

```rust
pub struct Counter_State {
    pub(super) integer: i64,
    pub(super) boolean: bool,
}
#[derive(Clone)]
pub struct Counter {
    pub(super) state: std::sync::Arc<std::sync::Mutex<Counter_State>>,
}
pub trait Counting {
    fn count(&self) -> i64;
    fn bump(&self);
    fn create() -> Self
    where
        Self: Sized;
}
```

## Removed: standard-library import (the former Proposal 6)

```rust
pub type Lap = i64;
pub struct Clock_State {
    pub(super) instant: std::time::Instant,
    pub(super) lap_vector: std::vec::Vec<Lap>,
}
#[derive(Clone)]
pub struct Clock {
    pub(super) state: std::sync::Arc<std::sync::Mutex<Clock_State>>,
}
pub trait Lapping {
    fn lap(&self) -> Lap;
}
pub trait Clocking {
    fn started(&self) -> std::time::Instant;
    fn lap<N: Lapping>(&self, input: N);
    fn start() -> Self
    where
        Self: Sized;
}
```

## Proposal 3 (empty yield, plain struct)

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub struct Counter {
    pub integer: i64,
    pub boolean: bool,
}
pub trait Counting {
    fn count(&self) -> i64;
    fn bump(&mut self);
}
```

## Sources

- /home/li/primary/flows/804eb9/books/whole-flow-ethos.md, Proposals 2 and 3 (the Ethos examples); the removed examples are in scratchpad/c4/whole-flow-ethos.before-audit.md.
- ethos-zero c4d82bf (github.com/LiGoldragon/ethos-zero), the Inspect query.
