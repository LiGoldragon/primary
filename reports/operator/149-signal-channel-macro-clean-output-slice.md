# Signal Channel Macro Clean Output Slice

## Scope

This report records the operator slice that implemented bead
`primary-77hh` for the Spirit path.

The work covered four code repositories:

- `signal-frame`
- `signal-persona-spirit`
- `owner-signal-persona-spirit`
- `persona-spirit`

It also recorded the new psyche constraint in
`intent/component-shape.nota`.

## What Changed

`signal-frame` now makes the channel macro emit clean names directly.

Before this slice, a contract such as Spirit received generated names
like:

```rust
SpiritFrame
SpiritFrameBody
SpiritChannelRequest
SpiritChannelReply
SpiritRequestBuilder
SpiritObserverSubscriptionToken
```

Contracts then immediately hand-wrote aliases to strip the ancestry:

```rust
pub type Frame = SpiritFrame;
pub type FrameBody = SpiritFrameBody;
pub type ChannelRequest = SpiritChannelRequest;
pub type ChannelReply = SpiritChannelReply;
pub type RequestBuilder = SpiritRequestBuilder;
```

After this slice, the macro emits the contract-local names directly:

```rust
pub type Frame = ::signal_frame::ExchangeFrame<Operation, Reply>;
pub type FrameBody = ::signal_frame::ExchangeFrameBody<Operation, Reply>;
pub type Request = ::signal_frame::Request<Operation>;
pub type ReplyEnvelope = ::signal_frame::Reply<Reply>;
pub type RequestBuilder = ::signal_frame::RequestBuilder<Operation>;
```

The macro also emits the structurally derivable pieces that contracts
were hand-writing:

```rust
pub enum OperationKind { ... }
pub enum ReplyKind { ... }
pub enum EventKind { ... }
pub enum StreamKind { ... }

impl From<EntryRecorded> for Reply { ... }
impl From<RecordSummary> for Reply { ... }
```

The intent is not that every name becomes globally generic. The crate
or module supplies the ancestry. Outside the contract, callers write
`signal_persona_spirit::Operation` or
`owner_signal_persona_spirit::Operation`.

## Spirit Contract Changes

`signal-persona-spirit` now declares clean root enums:

```rust
operation Operation {
    State(StateStatement),
    Record(RecordEntry),
    Observe(Observation),
    Subscribe(Subscription),
    Retract(SubscriptionToken),
}

reply Reply {
    StateRecorded(StateRecorded),
    EntryRecorded(EntryRecorded),
    SummaryObserved(SummaryObserved),
    SubscriptionOpened(SubscriptionOpened),
    SubscriptionRetracted(SubscriptionRetracted),
    RequestUnimplemented(RequestUnimplemented),
}
```

The contract no longer contains the alias block or manual
`OperationKind` / `From<Payload> for Reply` boilerplate.

`owner-signal-persona-spirit` received the same cleanup for the owner
contract.

## Persona Spirit Consumer Changes

`persona-spirit` now consumes the generated clean contract names.

The daemon still aliases imports locally where it talks to two
contracts in one crate:

```rust
use signal_persona_spirit::{
    Operation as WorkingOperation,
    Reply as WorkingReply,
};

use owner_signal_persona_spirit::{
    Operation as OwnerOperation,
    Reply as OwnerReply,
};
```

Those aliases are local disambiguation at the runtime boundary, not
contract-generated ancestry. They are the intended Rust-module
disambiguation shape.

Local helpers such as `SpiritFrameCodec` and
`OwnerSpiritFrameCodec` remain because they are daemon boundary objects
that hold codec behavior for two sockets. They are not generated signal
types.

## Tests

The following passed:

```sh
cargo fmt && CARGO_BUILD_JOBS=2 cargo test --locked
nix flake check -L --max-jobs 0
```

for:

- `signal-frame`
- `signal-persona-spirit`
- `owner-signal-persona-spirit`
- `persona-spirit`

The `persona-spirit` Nix check exercised:

- daemon and CLI package builds;
- split package checks for `spirit` and `persona-spirit-daemon`;
- actor runtime constraint tests;
- daemon socket routing tests;
- boundary tests;
- Sema projection tests.

## Commits

- `signal-frame` `653773b7`: clean channel macro boilerplate.
- `signal-persona-spirit` `3c111725`: Spirit contract consumes clean
  macro output.
- `owner-signal-persona-spirit` `00d15451`: owner Spirit contract
  consumes clean macro output.
- `persona-spirit` `41975128`: runtime consumes clean Spirit signal
  types.
- `primary` `b25ca75b`: intent log records the macro naming and
  boilerplate-generation rules.

## What Is Not Done

Bead `primary-77hh` remains open.

The macro is fixed and the Spirit path proves it, but the bead's
acceptance list requires sweeping every remaining contract:

- `signal-persona`
- `signal-persona-auth`
- `signal-persona-mind`
- `signal-persona-orchestrate`
- `signal-persona-router`
- `signal-persona-message`
- `signal-persona-introspect`
- `signal-persona-system`
- `signal-persona-terminal`
- `signal-persona-harness`
- owner contracts beyond Spirit
- repository-ledger contracts

The next operator slice should apply the same pattern contract by
contract, with narrow locks and Nix checks after each group.

## Remaining Risk

The macro tests cover multiple channel invocations by putting them in
Rust modules. That matches the psyche rule that modules, not prefix
knobs, disambiguate multiple channel declarations.

The broad risk is propagation, not the macro mechanism. Any contract
still pinned to the older `signal-frame` revision will still carry the
old alias shape until it is bumped and cleaned.
