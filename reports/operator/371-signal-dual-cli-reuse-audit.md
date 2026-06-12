# Signal Dual-CLI Reuse Audit

## Verdict

The daemon-side split is substantially reusable. `schema-rust-next` emits a
daemon shape with working and meta listener tiers, and `triad-runtime` owns the
multi-listener socket shell, socket modes, length-prefixed binary framing, and
single-argument process edge.

The client-side split is not production-copyable yet. Spirit's current
`spirit` / `meta-spirit` pair works as a component-local implementation, but it
duplicates the same text-source, socket exchange, and length-prefixed
short-header transport logic that already appears in `orchestrate`, `lojix`,
`cloud`, `message`, and `agent`. There is no shared schema-generated CLI client
noun that a new component can adopt with a one-line binary.

## Findings

### 1. Spirit's meta-socket witness is currently broken

`cargo test --features nota-text --test meta_configure` in `spirit` fails to
compile:

```text
error[E0004]: non-exhaustive patterns: `MetaOutput::Imported(_)` not covered
tests/meta_configure.rs line 128
```

The immediate cause is `tests/meta_configure.rs` line 128: the test matches
`MetaOutput` and handles only `Configured` and `Rejected`. Commit
`spirit: owner-only meta Import + meta-spirit client` added
`MetaOutput::Imported`, but the main meta Configure witness was not kept
exhaustive.

This matters because this is the exact test that should prove the owner-only
meta socket split. A split client that grows a new meta operation and breaks
the meta-socket test is not ready to be the exemplar yet.

### 2. The daemon/listener split is reusable

The reusable daemon pieces are in the right layer:

- `triad-runtime` owns `AsyncMultiListenerDaemon`, `AsyncListenerSocket`,
  `SocketMode`, `BindingSurface`, `LengthPrefixedCodec`, and
  `ComponentCommand`.
- `schema-rust-next` emits the `ComponentDaemon` trait with
  `handle_meta_connection` when the daemon shape has a meta tier
  (`schema-rust-next/src/daemon_emit.rs` lines 470-485).
- `schema-rust-next` emits listener dispatch from `ListenerTier::Meta` to the
  component hook (`schema-rust-next/src/daemon_emit.rs` lines 1257-1262).
- Spirit's `build.rs` asks for a `MetaListenerTier` with owner-only mode, and
  generated `src/schema/daemon.rs` binds the second socket.

Spirit's hand-written daemon hook in `spirit/src/daemon.rs` lines 153-177 is
appropriately small: it reads one length-prefixed frame, decodes generated
meta `Input`, matches `Configure` / `Import`, and writes generated meta
`Output`.

The open reuse gap on daemon side is narrower: the hook still decodes and
encodes the meta wire manually because the emitted daemon shape names only
"there is a meta tier", not "this is the meta contract root to decode." That
is acceptable as a transitional escape hatch, but it should disappear once the
daemon shape can name the meta contract module.

### 3. The client-side shape is duplicated, not reusable

Spirit has two separate binaries:

- `spirit/src/bin/spirit.rs` reads one argument, parses `signal::Input`,
  resolves `SPIRIT_SOCKET`, exchanges through `SignalTransport`, prints
  `signal::Output`, and has subscription-only extra logic.
- `spirit/src/bin/meta-spirit.rs` repeats the same argument/file parsing,
  parses `meta_signal::Input`, resolves `SPIRIT_META_SOCKET`, exchanges through
  `MetaSignalTransport`, and prints `meta_signal::Output`.

The duplication is direct:

- `spirit/src/bin/spirit.rs` lines 71-88 and
  `spirit/src/bin/meta-spirit.rs` lines 40-57 duplicate input-source handling.
- `spirit/src/bin/spirit.rs` lines 92-103 and
  `spirit/src/bin/meta-spirit.rs` lines 61-72 duplicate the string-backed
  parse-source noun.
- `spirit/src/transport.rs` lines 51-70 and
  `spirit/src/meta_transport.rs` lines 60-89 duplicate the one-request
  exchange shape.
- `spirit/src/transport.rs` lines 86-97 and
  `spirit/src/meta_transport.rs` lines 91-102 duplicate the length-prefixed
  frame read/write skeleton.

Some duplication is explainable by Spirit's streaming operation:
`SubscribeIntent` keeps the ordinary CLI attached and reads subscription event
frames. The base one-shot exchange is still generic and should not be copied.

### 4. The existing `signal-frame` client is the wrong abstraction for schema roots

`signal-frame` already contains a reusable-looking split CLI surface:
`CommandLineDispatch`, `CommandLineSockets`, `RequestHead`,
`ClientShape`, and `signal_cli!`.

The problem is that this client is built around the older
`signal_frame::Request<Operation>` plus `ExchangeFrame` /
`StreamingFrame` shape:

- `signal-frame/src/command_line.rs` lines 448-451 parse
  `Request<Operation>`, not a schema-generated root `Input`.
- `signal-frame/src/command_line.rs` lines 455-463 define
  `ClientFrame` in terms of `Operation` and `Reply`.
- `signal-frame/src/command_line.rs` lines 480-485 wrap a request in
  `ExchangeFrameBody::Request`.
- `signal-frame/src/command_line.rs` lines 611-628 route by head, parse a
  `Request`, inject `Caller`, and submit an `ExchangeFrame`.

Schema-derived components currently speak generated root `Input`/`Output`
directly via `encode_signal_frame` / `decode_signal_frame`.
`orchestrate/src/bin/orchestrate.rs` lines 3-5 states this explicitly: it
speaks the schema-emitted `Input` frame, not the retired `ExchangeFrame` client.

So `signal-frame` owns good pieces, especially head routing and socket-env
derivation, but it does not yet own the client shape schema-derived components
actually use.

### 5. Other components confirm the duplication is fleet-wide

The pattern has already forked:

- `orchestrate/src/signal_transport.rs` has separate
  `OrdinarySignalTransport` and `MetaSignalTransport`, plus a local
  `FrameExchange`.
- `orchestrate/src/bin/orchestrate.rs` routes by trying ordinary parse first,
  then meta parse.
- `lojix/src/client.rs` routes by trying meta decode first, then ordinary
  decode; its own comment notes short-header collisions make this structurally
  weak.
- `cloud/src/client.rs` has a local `SchemaConnection` with
  `exchange_working` and `exchange_meta`, and a local `CliRequest`.
- `message/src/client.rs` and `agent/src/client.rs` each hand-write a
  single-tier version of the same `LengthPrefixedCodec` exchange.

This is the strongest evidence that the split has not been made reusable
enough. A reusable mechanism would cause these components to converge toward
one small binary entry shape, not grow local variants.

### 6. Routing is inconsistent across components

There are three routing strategies in the current fleet:

- Spirit uses two separate CLI binaries, so no runtime routing between working
  and meta is needed.
- Orchestrate tries to parse ordinary `Input`, then tries meta `Input`.
- Cloud uses `signal-frame::RequestHead` against operation-head sets, then
  converts operation payloads into schema inputs.
- Lojix tries to decode a binary signal file as meta first, then ordinary, and
  its comment notes the short-header collision.

This is not a reusable split. The reusable strategy should be one of these,
declared once and tested once. For schema-derived roots, the cleanest shape is
head-table routing over generated `Input::HEADS`, because
`schema-rust-next` already emits `impl signal_frame::SignalOperationHeads for
Input` in generated roots.

### 7. Spirit's meta CLI has no binary/file-signal path despite accepting `SignalFile`

Both `spirit` and `meta-spirit` call `ComponentCommand::nota_argument()`.
When the argument is classified as `SignalFile`, both binaries read it as text
and parse NOTA (`spirit/src/bin/spirit.rs` lines 82-87,
`spirit/src/bin/meta-spirit.rs` lines 51-56).

That may match the current CLI text-edge intent, but the variant name
`SignalFile` is misleading here. If component CLIs should accept only NOTA
text, the shared client should expose a text-only source classifier. If CLIs
should also accept rkyv files, Spirit's current implementation does not.

## What Is Properly Done

- The meta socket is a separate listener tier, not a flag or multiplexed
  ordinary operation.
- The meta socket mode is tested as owner-only.
- The working socket rejects a meta Configure frame.
- Daemon startup rejects missing meta socket.
- The privileged `Import` path lives only on meta input, not on the working
  signal.
- The generated roots implement `SignalOperationHeads`, so schema roots have
  the raw material for shared head-routing.

## Recommendation

Fix this in the shared stack, not by polishing `meta-spirit` alone.

1. Repair Spirit's broken `meta_configure` test by handling
   `MetaOutput::Imported` explicitly in the existing Configure match.
2. Add a reusable schema-root client in `triad-runtime` or `signal-frame`.
   The noun should be something like `SchemaSignalClient<WorkingInput,
   WorkingOutput, MetaInput, MetaOutput>`, but final naming should follow the
   local crate vocabulary.
3. The reusable client should own:
   - one-argument text/file source handling;
   - optional working/meta socket set;
   - head-table routing using generated `SignalOperationHeads`;
   - one-shot length-prefixed `encode_signal_frame` /
     `decode_signal_frame` exchange;
   - display of generated `Output`;
   - a hook for component-specific streaming after the first reply.
4. Teach `schema-rust-next` to emit or at least constrain the small trait that
   lets generated roots satisfy the shared client:
   `encode_signal_frame`, `decode_signal_frame`, `SignalOperationHeads`,
   `FromStr`, and `Display`.
5. Port Spirit to the shared client while keeping `spirit` and `meta-spirit`
   as two binaries if that is the desired authority UX. The binaries should be
   tiny selectors, not duplicated clients.
6. Port `orchestrate`, `lojix`, `cloud`, `message`, and `agent` after Spirit
   proves the shape.

## Tests Run

- `signal-frame`: `cargo test --features nota-text command_line` passed.
- `signal-frame`:
  `cargo test --features nota-text signal_cli_macro_routes_heads_to_working_or_meta_socket`
  passed.
- `spirit`: `cargo test --features nota-text --test meta_configure` failed
  to compile because `MetaOutput::Imported` is not handled in the test.

## Bottom Line

The split is architecturally right at the daemon/socket layer. It is not yet
properly reusable at the CLI/client layer. The current Spirit implementation is
a useful proof of the owner-only meta socket, but the reusable production shape
still needs a shared schema-root client and a repaired Spirit witness.
