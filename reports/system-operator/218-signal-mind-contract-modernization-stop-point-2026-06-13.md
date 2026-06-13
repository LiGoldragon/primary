# 218 — signal-mind contract modernization stop point

## Context

The mind upkeep slice has already landed the narrow meta plane:

- `meta-signal-mind` now derives its contract from `schema/lib.schema` on main.
- `mind` consumes that schema-derived meta contract on main.

The remaining repo in the component lock is `signal-mind`, the working signal contract for the public mind channel.

## Finding

`signal-mind` is not the same kind of conversion as `meta-signal-mind`.

`meta-signal-mind` was a compact request/reply grammar. `signal-mind` is the full public vocabulary for the mind daemon:

- `src/lib.rs` is about 1,300 lines.
- `src/graph.rs` is about 1,400 lines.
- `tests/round_trip.rs` is about 1,300 lines.
- `mind` consumes the contract directly across daemon transport, tests, text projection, actor dispatch, store tables, graph validation, subscriptions, and SEMA ingress.

The current schema file, `schema/signal-mind.concept.schema`, is only a concept sketch. It does not describe the real contract shape.

## Why this is a stop point

The handwritten surface has two different kinds of content mixed together:

- Declarative wire nouns that should move into schema generation: newtypes, records, enums, request/reply/event roots, stream grammar, and feature-gated NOTA/rkyv projections.
- Semantic contract methods that still need hand ownership after generation: endpoint-domain validation on `RelationKind`, boundary validation on `WirePath` and `TaskToken`, operation-kind compatibility aliases, and graph convenience predicates such as identity-reference checks.

Converting only part of it would make the repo look modern while preserving the hard problem. Converting all of it in the current slice would be a broad public-contract migration and would force a large synchronized `mind` consumer update.

## Recommended next slice

Treat `signal-mind` as its own explicit contract migration:

1. Replace the concept schema with a real `schema/lib.schema` that covers the full current public contract.
2. Generate `src/schema/lib.rs` and make `src/lib.rs` a thin export and compatibility layer.
3. Preserve current public aliases where practical: `MindRequest`, `MindReply`, `MindFrame`, `MindFrameBody`, `MindOperationKind`, `MindStreamKind`.
4. Reattach semantic methods as impls on generated nouns, not as schema generator hacks.
5. Keep the exhaustive round-trip tests, adjusting only generated NOTA shapes that intentionally change.
6. Update `mind` in the same slice after `signal-mind` lands.

## Operator stance

Do not block the broader component-upkeep queue on this repo. The useful thing to land now was the meta-plane modernization, and that is done. The working-signal conversion should be scheduled as a focused contract migration because it is large enough to deserve its own review boundary.

