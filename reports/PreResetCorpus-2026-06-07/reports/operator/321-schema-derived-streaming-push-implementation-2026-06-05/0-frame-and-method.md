# Operator 321 - Schema-Derived Streaming Push Implementation

## Frame

The user challenged the prior operator wording that streaming push needed a
separate slice: if the intent was clear, why not implement it?

The intent was clear enough to implement the shared substrate. The correct
boundary is:

- `signal-frame` owns the low-level binary streaming frame shape.
- `schema-next` owns the schema-visible stream declaration and operation/event
  relations.
- `schema-rust-next` emits typed frame aliases and constructors only when the
  schema declares a stream.
- `triad-runtime` owns reusable subscription token issuance, live registries,
  stream event sequencing, and event-frame publication.
- component daemons own stream filters and socket delivery IO.

## Method

Two background subagents audited the path while the main operator implemented:

- Galileo mapped the existing `signal-frame` streaming kernel and confirmed it
  already has `StreamingFrameBody::SubscriptionEvent`,
  `SubscriptionTokenInner`, and `ObservableSet` machinery.
- Archimedes mapped the schema-rust-next emission hook and confirmed the
  previous emitter had no schema-authored stream marker to rely on.

The main operator then implemented on main branches, verified with cargo tests
and clippy, and pushed each changed code repository.
