# Implementation

## Schema-derived streaming substrate

`schema-next` commit `30a88bee` added stream metadata to the typed schema:

- `Schema::streams()`
- `StreamDeclaration`
- `StreamRelation`
- direct lowering support for `Stream { token opened event close }`
- variant relations for `opens` and `belongs`

`triad-runtime` commit `de332266` added reusable streaming runtime nouns:

- `SubscriptionToken`
- `SubscriptionTokenIssuer`
- `SubscriptionRegistry`
- `Subscription`
- `SubscriptionEventSequence`
- `SubscriptionEventPublisher`

`schema-rust-next` commit `4ee2c898` made schema stream declarations emit
Signal-frame streaming support, using explicit `Schema::streams()` metadata
rather than ad hoc source scanning.

## Rust-native emitter migration

`schema-rust-next` commit `d8e0a37a` marked runtime string emission as debt in
repo docs and tokenized the streaming support emitter through a
context-carrying token wrapper.

`schema-rust-next` commit `fd84aae2` tokenized trace object-name and trace
support emission. This moved another runtime-adjacent cluster away from manual
string formatting and refreshed the checked fixtures.

Remaining string clusters are still present in the runner, engine-trait,
mail/envelope, and signal-frame routing emitters. The migration is active and
partially landed, not complete.

## Dependency cleanup

`signal-sema` commit `c132e9a0` removed a stale `signal-frame` dependency and
the leftover `LogVariant` implementation path. The crate now exposes only its
own sema vocabulary and local `log_variant()` methods.

This matters because Spirit's updated lockfile should not drag multiple
historical signal-frame/schema graphs through obsolete dependencies.

## Spirit exemplar and Nix proof

`spirit` commit `a2df8176` updated the stack pins and documented Spirit as the
copyable three-plane exemplar. It aligned `INTENT.md` and `ARCHITECTURE.md`
with the current shape:

- crate-local `schema/signal.schema`
- crate-local `schema/nexus.schema`
- crate-local `schema/sema.schema`
- generated modules under `spirit::schema`
- `sema-engine` storage
- `triad-runtime` runner/listener/runtime support

`spirit` commit `885aa932` hardened the production-style Nix proof:

- updated `Cargo.lock` to `schema-rust-next` commit `fd84aae2`
- regenerated `src/schema/{signal,nexus,sema}.rs`
- added complete flake source inputs for every Li git dependency reachable in
  Spirit's Cargo graph
- rewrote the Nix source patch to replace those git dependencies with local
  vendored paths during local stack tests
- updated `scripts/check-local-schema-stack`,
  `scripts/run-nix-integration-tests`, and `tests/nix_integration.rs` to pass the
  complete override set
- updated stale ignored Nix tests to the current `Observe -> RecordsStashed ->
  LookupStash -> RecordsObserved` flow

The Nix failure that triggered this fix was not a Spirit runtime failure. It was
a packaging defect: after the remote builder/cache was unavailable, the local
Nix build fell back to Cargo trying to fetch `schema-next` from GitHub inside
the build. The complete override set removes that class of failure.
