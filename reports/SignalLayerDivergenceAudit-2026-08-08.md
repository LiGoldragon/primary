# Signal-Layer Divergence Audit

2026-08-08. Ground for fleshing out Signal properly. The psyche:
"It's kind of been really ad hoc. I feel like all the demons like use
a different approach." Confirmed: twelve daemons, four families.

## Family A — spirit-shaped (the standard): spirit, router, message,
## orchestrate, agent, mirror

triad-runtime daemon shell; schema-rust generated Signal/Nexus/Sema
triad; dual sockets (working + meta at 0o600) from typed
configuration; signal-frame `ContractMarker` + `ExchangeIdentifier`
correlation; full rkyv 0.8 feature set (std, bytecheck,
little_endian, pointer_width_32, unaligned); `signal-X` +
`meta-signal-X` contract pairs; `EngineRefusal` error envelope.
Spirit alone has subscription/streaming (`StreamingFrameBody`).
Minor variants: orchestrate adds a third upgrade socket; mirror adds
TCP tailnet ingress, no exchange IDs, errors drop the connection.

## Family B — language-engine trio: ethos-engine, logos-engine,
## sema-storage

Hand-rolled u32 BE length-prefix framing via `Wire` from
signal-sema-storage; MANDATORY handshake per connection (no Family A
member has one); u64 sequence numbers instead of ExchangeIdentifier;
subscriptions via `Reply::Event` on the same connection; hand-written
plane actors on kameo directly; NO meta socket; hardcoded socket
paths under /tmp/new-language-engine/; rkyv bytecheck-only feature
set — a portability risk versus the standard feature set.

## Family C — pre-triad legacy: aggregator, listener

aggregator: signal-frame codecs but hand-rolled socket IO,
hand-written planes, no kameo, std::thread + Mutex. listener: the
extreme outlier — no triad at all, no kameo, synchronous accept loop,
and its meta socket speaks newline-delimited JSON, not rkyv.

## Family D — lojix hybrid

Family A transport and contracts, but hybrid concurrency (kameo for
jobs, tokio tasks per request) and an "owner" socket in place of the
standard meta pattern.

## Unification direction

Spirit is the reference. Divergences to close, per family: B adopts
triad-runtime, meta sockets, ExchangeIdentifier, the full rkyv
feature set, configured socket paths; C adopts the triad shell
wholesale; D normalizes its owner socket and concurrency; mirror and
orchestrate variants need explicit blessing or normalization. The
handshake question (B has one, A does not) and streaming support
(only spirit and B have it) need a single ruled answer when Signal is
fleshed out.
