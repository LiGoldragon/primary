# Signal-Frame Kernel Map

`signal-frame` already had the real wire kernel for streaming push:

- `StreamingFrame<RequestPayload, ReplyPayload, EventPayload>`;
- `StreamingFrameBody::SubscriptionEvent { event_identifier, token, event }`;
- `SubscriptionTokenInner`;
- `StreamEventIdentifier`, `ExchangeLane`, `LaneSequence`, and
  `SessionEpoch`;
- `ObservableSet` as the older publish/filter trait shape.

The key boundary is that these are frame mechanics, not component semantics.
`signal-frame` should not learn about Spirit mail filters, Nexus decisions, or
SEMA writes. It remains the domain-free binary envelope.

This session added `signal-frame/INTENT.md` and updated stale owner/meta
wording in its repo docs. No signal-frame Rust code changed.
