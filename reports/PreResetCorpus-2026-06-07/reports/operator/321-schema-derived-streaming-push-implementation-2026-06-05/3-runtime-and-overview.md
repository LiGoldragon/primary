# Runtime And Overview

## triad-runtime

`triad-runtime` now owns the reusable streaming runtime pieces above the
`signal-frame` wire kernel:

- `SubscriptionToken` bridges generated component token newtypes to
  `SubscriptionTokenInner`;
- `SubscriptionTokenIssuer` mints monotonically increasing wire tokens;
- `SubscriptionRegistry<Token, Filter>` stores live subscriptions and
  publishes matching events through caller-supplied filter and delivery
  closures;
- `SubscriptionEventSequence` mints monotonic acceptor-lane
  `StreamEventIdentifier` values;
- `SubscriptionEventPublisher<Input, Output, Event>` constructs real
  `signal_frame::StreamingFrame<Input, Output, Event>` subscription-event
  frames.

This keeps the reusable mechanics out of component daemons while leaving
component policy visible in schema and component code.

## Commits

- `schema-next` main: `30a88bee` after stream metadata and direct-lowering
  alignment.
- `schema-rust-next` main: `4ee2c898` for signal-frame stream emission.
- `triad-runtime` main: `de332266` for subscription runtime support.
- `signal-frame` main: `6f5a77f` for local INTENT and meta boundary wording.

## Verification

- `schema-next`: `cargo test`; `cargo clippy --all-targets -- -D warnings`.
- `schema-rust-next`: `cargo test --test big_emission`; `cargo test`;
  `cargo clippy --all-targets -- -D warnings`.
- `triad-runtime`: `cargo test`; `cargo clippy --all-targets -- -D warnings`.

## What Is Still Not Done

This implements the shared schema/emission/runtime substrate. It does not yet
pilot a real component operation that opens a long-lived subscriber socket and
delivers later daemon events to that socket.

That remaining slice is component integration: declare a real stream in a
component schema, route the opening operation through Nexus, store the returned
token, publish a later event through the runtime registry, and write the frame
to the subscriber connection. That work should now be a component-pilot task,
not a missing shared-substrate task.
