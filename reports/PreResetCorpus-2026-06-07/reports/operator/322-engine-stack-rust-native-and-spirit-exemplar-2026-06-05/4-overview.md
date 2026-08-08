# Overview

## Operator verdict

This pass materially improved the new Spirit production path.

Spirit is now a stronger copyable exemplar because the important proof no
longer stops at `cargo test`: the Nix-built CLI and daemon cross the real socket,
persist through the `.sema` store, exercise rejection, state persistence,
back-to-back daemon requests, stash lookup, and schema-emitted output
round-trips. The Nix proof also no longer depends on a working binary cache or
Cargo network fetches for local Li dependencies.

## What is now true

The new Spirit stack is green on:

- normal Rust tests
- all-features Rust tests
- process-boundary CLI/daemon tests
- clippy with all targets and all features
- ignored Nix-built binary integration tests through the script entry point

The repo now states and proves that `Observe` uses the current slim-output flow:
`Observe` returns `RecordsStashed`, then `LookupStash` returns
`RecordsObserved`. The outdated Nix tests were corrected to prove that actual
runtime behavior.

The schema-derived streaming substrate is in place at the schema/runtime/emitter
level, but it is not yet a full component streaming product. The next production
slice is a component that declares a stream and serves subscription events
through the daemon path.

## What remains unfinished

The runtime emitter migration is still incomplete. The trace object-name slice
is done, and streaming support is tokenized, but large string-format clusters
remain in:

- generated runner glue
- generated engine traits
- mail/envelope/namespaces
- signal-frame routing and short-header support

The generic multi-listener daemon runner is still not fully proven as a
copy-paste replacement for every component. Spirit currently proves the
single-listener runtime path. The ordinary/meta two-listener shape still needs
the single engine-owner loop design implemented and tested.

Production cutover from `persona-spirit` is still a separate task. The new
Spirit has stronger parity and production-style tests, but a real deployment
cutover still needs live database/interface compatibility decisions and an
operator-managed release path.

## Important design contention

The most important operator contention remains the same: reusable role names
belong in shared traits and runtime nouns, while component-specific variants
stay generated in the component schema modules.

That means names such as `NexusWork`, `NexusAction`, `SemaWriteInput`, and
`SemaReadInput` should be traits or fixed runner roles in `triad-runtime` when
the reusable behavior is generic. The Spirit variants implementing those roles
remain Spirit-specific generated types under `spirit::schema::{nexus,sema}`.
This preserves both sides of the psyche's intent: no repeated boilerplate, and
the internal feature catalog remains visible in `schema/nexus.schema`.

## Next operator moves

1. Continue tokenizing `schema-rust-next` runtime emission, starting with runner
   glue and then engine traits.
2. Implement the two-listener ordinary/meta daemon runner as shared
   `triad-runtime` code with one engine-owner loop.
3. Build the first real streaming component path: schema stream declaration,
   generated support, runtime subscription registry, and socket delivery.
4. Use Spirit's now-green Nix proof as the exemplar test shape before porting
   other components.
