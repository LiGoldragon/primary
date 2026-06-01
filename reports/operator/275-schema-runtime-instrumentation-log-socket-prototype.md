# Schema Runtime Instrumentation Log Socket Prototype

*Kind: prototype design report · Topics: schema-runtime, instrumentation, log-socket, Signal/Nexus/SEMA, spirit-next · 2026-06-01 · operator lane*

## Frame

This report prototypes the schema-derived runtime instrumentation/log-socket
shape from Spirit records 1343-1350 against the current repos:
`spirit-next`, `schema-rust-next`, and `schema-next`.

The current code already has the important floor:

- `schema-rust-next` emits `MessageSent`, `MessageProcessed`, plane envelopes,
  `SignalEngine`, `NexusEngine`, and split `SemaEngine::apply` /
  `SemaEngine::observe`.
- `spirit-next` main uses those traits on the live runtime path. Signal
  admits, Nexus executes, SEMA writes/observes the `.sema` redb file, and CLI
  and daemon communicate by binary rkyv frames.
- `spirit-next` still has several positive grep Nix checks. Those can remain
  only as temporary anchor checks; they are not live architecture proof after
  Spirit records 1340-1342.

## Prototype Claim

The instrumentation slice should be a generated, optional, typed trace surface
that observes the live runtime path without changing the normal Signal wire
protocol.

Shape:

```text
CLI test mode opens normal Signal socket
CLI test mode also owns/attaches log socket
daemon receives binary Signal frame
Signal/Nexus/SEMA engine methods emit generated TraceEvent values
daemon sends TraceEvent frames to the log socket
CLI displays/records trace while normal reply still returns on Signal socket
test asserts trace events plus normal Output
```

The log socket is a side observation channel. It must not become a second
control protocol and must not carry the normal reply.

## Trace Event Schema

The trace vocabulary belongs in schema-rust support emission first, then later
in a shared schema-core floor. It should be schema-emitted data, not strings.

Minimum generated nouns:

```text
TraceEvent [
  (SignalAdmitted SignalTrace)
  (SignalRejected SignalTrace)
  (SignalReplied SignalTrace)
  (NexusEntered NexusTrace)
  (NexusDecided NexusTrace)
  (NexusReplied NexusTrace)
  (SemaWriteApplied SemaTrace)
  (SemaReadObserved SemaTrace)
]

SignalTrace {
  MessageIdentifier *
  OriginRoute *
  ShortHeader *
  MessageRoot *
}

NexusTrace {
  MessageIdentifier *
  OriginRoute *
  root MessageRoot
  decision NexusDecision
}

SemaTrace {
  MessageIdentifier *
  OriginRoute *
  DatabaseMarker *
  operation SemaOperationKind
}
```

`NexusDecision` and `SemaOperationKind` should be closed enums generated from
the declared plane roots where possible. For the spirit-next pilot:
`SemaOperationKind` can distinguish `WriteRecord`, `WriteRemove`, and
`ReadObserve`. This is enough to prove write and read paths separately.

The event sequence for a successful `Record` request should be:

```text
SignalAdmitted
NexusEntered
NexusDecided(SemaWrite)
SemaWriteApplied
NexusReplied
SignalReplied
```

For an `Observe` request:

```text
SignalAdmitted
NexusEntered
NexusDecided(SemaRead)
SemaReadObserved
NexusReplied
SignalReplied
```

For rejected Signal input:

```text
SignalRejected
```

No `Nexus*` or `Sema*` event may appear after Signal rejection.

## Ownership

The daemon owns trace production. The CLI owns the user/test-facing log
surface.

Recommended first implementation in `spirit-next`:

- Extend binary `Configuration` with optional `TraceConfiguration`.
- In production/default configuration, trace is disabled and the daemon does
  not connect or bind any trace socket.
- In testing configuration, the configuration names a Unix log socket path and
  trace encoding mode. The daemon emits length-prefixed rkyv `TraceEvent`
  frames to that socket.
- The CLI's normal single NOTA argument remains the operation. Test launchers
  can create the binary daemon configuration and set the normal
  `SPIRIT_NEXT_SOCKET` plus a test-only environment pointer for the CLI log
  surface. The long-term build configuration should be a typed NOTA struct per
  Spirit 1348.

This honors Spirit 1347: the CLI is the log surface. It also preserves the
normal binary protocol because the ordinary daemon socket still accepts only
generated Signal frames.

## Build Configuration Shape

There are two layers that should not be conflated:

1. Compile-time: production builds should not include trace code unless a
   testing/instrumentation feature is selected.
2. Runtime test configuration: when that feature is present, typed config
   decides whether a daemon instance emits trace events and where.

Recommended feature naming:

```toml
[features]
runtime-trace = []
```

Recommended typed configuration, initially hand-written in `spirit-next`
beside current binary `Configuration`, later schema-emitted:

```text
Configuration {
  socket_path ConfigurationPath
  database_path ConfigurationPath
  trace (Optional TraceConfiguration)
}

TraceConfiguration {
  socket_path ConfigurationPath
  mode TraceMode
}

TraceMode [Testing]
```

Do not add daemon flags. Do not put trace routing on the normal operation
NOTA. Do not make the daemon parse NOTA for configuration; the current
daemon startup path is binary rkyv configuration.

The Spirit 1348 typed NOTA build-config decision should land at the build
or test-launcher layer, not as a daemon CLI flag. A test launcher can read:

```nota
(BuildConfiguration TestingBuild Enabled)
```

and produce the binary daemon `Configuration` file with a trace socket path.
The daemon still receives one binary configuration path.

## Emitter Responsibilities

`schema-rust-next` should emit the trace event nouns and minimal hook traits
behind `runtime-trace`.

Recommended generated support:

```rust
pub trait TraceEventSink {
    type Error;
    fn trace_event(&mut self, event: TraceEvent) -> Result<(), Self::Error>;
}

pub trait RuntimeTrace {
    fn trace_to<Sink>(&self, sink: &mut Sink) -> Result<(), Sink::Error>
    where
        Sink: TraceEventSink;
}
```

Engine traits should not change their production signatures to take a sink.
Instead, the runtime objects get optional sinks when constructed in test mode:
`SignalActor`, `Nexus`, and `Store` can each hold an optional trace sink handle
behind the feature. That keeps generated trait signatures stable and avoids
polluting every production impl with test-only parameters.

## Tests That Prove Use

Layer 2 runtime witness per designer 459 is the right target. The tests should
prove engine methods ran, not only that the traits exist.

Initial tests in `spirit-next`:

- `trace_socket_records_full_record_plane_chain`: start daemon with trace
  enabled, invoke CLI `Record`, read trace frames from CLI/test log socket,
  assert the sequence includes `SignalAdmitted`, `NexusEntered`,
  `NexusDecided(SemaWrite)`, `SemaWriteApplied`, `NexusReplied`,
  `SignalReplied`, and assert the normal CLI reply parses as
  `Output::RecordAccepted`.
- `trace_socket_records_observe_as_sema_read`: seed one record, invoke CLI
  `Observe`, assert trace includes `SemaReadObserved` and does not include
  `SemaWriteApplied` for the observe request.
- `signal_rejection_does_not_emit_nexus_or_sema_trace`: send invalid input,
  assert `Output::Rejected`, and assert trace contains only Signal rejection
  class events.
- `normal_socket_still_rejects_trace_or_nota_bytes`: send a length-prefixed
  trace frame or raw NOTA to the normal daemon socket and assert rejection.
- `production_build_has_no_trace_socket_dependency`: with default/no trace
  feature, dependency and symbol checks prove the trace transport is absent.
  This is a negative guard, not a positive use proof.

Nix shape:

- Pure cargo tests for generated trace nouns and in-process trace sink.
- Stateful `nix run .#test-runtime-trace` or a named check that spawns the
  daemon and CLI with trace enabled and leaves a small trace artifact.
- A later chained test can write the trace artifact first, then read it with a
  small trace-reader binary to prove the artifact is typed rkyv and not a
  string log.

## Immediate Queue

1. `schema-rust-next`: emit `TraceEvent`, `TraceEventSink`, and trace support
   behind `runtime-trace`; add emitter tests that compile and call the support.
2. `spirit-next`: extend `Configuration` with optional trace configuration
   behind the feature; implement a `TraceSocket` sink that writes rkyv
   `TraceEvent` frames.
3. `spirit-next`: thread optional trace sinks through `SignalActor`, `Nexus`,
   and `Store` and emit events at the exact engine entry/exit points.
4. `spirit-next`: add runtime trace process-boundary tests; replace remaining
   positive grep witness checks with live tests where they are currently
   pretending to prove usage.
5. Later: move trace support nouns to schema-authored/schema-core once at
   least two components need them.

## Non-goals

- No logging daemon.
- No text log format as the proof surface.
- No normal Signal socket multiplexing.
- No production logging by default.
- No broad source grep as proof that tracing or engine usage is live.

