# Signal-Frame Push Audit

## 2026-06-05 Follow-Up

The shared streaming substrate is now implemented in report
`reports/operator/321-schema-derived-streaming-push-implementation-2026-06-05/`.
The finding below is retained as the audit state before that follow-up slice.

## Finding

The claim was true but not fixed in this implementation slice. `signal-frame` already contains streaming/push primitives: streaming frame bodies, subscription tokens, and a publish/subscribe registry. The schema-derived Spirit path does not currently consume them.

## Boundary

This is not the same problem as the reusable runner or ordinary/meta listener shell. Push requires a schema-visible streaming operation shape, generated frame routing, and a runtime session model. A narrow import of the low-level registry would not make Spirit production-ready; it would just hide another feature behind implementation code.

## Recommended Fix Shape

The next slice should:

- add schema-rust-next emission for streaming Signal operations whose replies can become server-pushed events;
- add triad-runtime session support that maps generated subscription roots onto `signal-frame` subscription tokens and registry publication;
- pilot one Spirit or cloud operation end to end, with a test that proves a subscription request creates a token and a later Nexus/SEMA event publishes through `signal-frame`.

This remains an important open item, but it is intentionally not claimed as solved by the role-trait and daemon-shell commits.
