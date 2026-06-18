# 415 — criome interest-bearing token landing

## What Landed

Designer report `680` identified the one concrete schema change that turns the
authorized-object pulse from "fan to every subscriber" into a matchable
subscription table: put `AuthorizedObjectInterest` inside
`AuthorizedObjectUpdateToken`.

That is now landed on main:

- `signal-criome` `e33ea04a` — `AuthorizedObjectUpdateToken` is now
  `{ subscriber Identity, interest AuthorizedObjectInterest }`, with generated
  Rust, canonical NOTA examples, round-trip tests, and docs updated.
- `criome` `4250cbb3` — the daemon consumes the new token shape, stores
  authorized-object subscriptions directly as generated tokens, filters publish
  counts by `token.interest`, and retracts one `(subscriber, interest)` stream
  at a time.

## Code Shape

The contract token is now the stream identity:

```nota
AuthorizedObjectUpdateToken {
  subscriber Identity
  interest AuthorizedObjectInterest
}
```

`AuthorizedObjectObservation` still carries the opening request:

```nota
AuthorizedObjectObservation {
  subscriber Identity
  interest AuthorizedObjectInterest
}
```

`criome` root turns that request into the stream token, then the
`SubscriptionRegistry` stores the token directly. The former local
`AuthorizedObjectSubscription { token, interest }` wrapper is gone.

The runtime filter is still the same closed lattice:

- `AnyAuthorizedObject` matches all updates.
- `Component(c)` matches a component row.
- `ObjectKind(k)` matches an object-kind column.
- `ComponentObject(c, k)` matches one cell.

## Witness

The strengthened daemon test opens two authorized-object subscriptions for the
same subscriber:

1. `Component(Spirit)`.
2. `ObjectKind(Time)`.

It then retracts each token independently. This proves the token identity is
not merely the subscriber identity; it is the subscriber plus interest.

## Verification

Local checks:

```sh
cargo test --features nota-text --all-targets
cargo clippy --features nota-text --all-targets -- -D warnings
```

Remote checks, using GitHub revisions only:

```sh
nix flake check github:LiGoldragon/signal-criome/e33ea04a142dbd77a4bbfe381d2592f3ea06a78d
nix flake check github:LiGoldragon/criome/4250cbb34f3d6537d7a4d3ea8ecdea69b81bffb5
```

Both remote checks passed.

## Remaining Boundary

This lands the matchable subscription identity. It does not yet land:

- socket-level delivery to subscribers;
- router-level fan-out;
- a durable scheduler table or scheduler actor for `ContractTimeCheck`.

Those are the next real implementation surfaces, but they need the actual
delivery/scheduler owner shape. The current code deliberately keeps the POC
inside `criome`'s subscription registry rather than smuggling in a router or
timer architecture.
