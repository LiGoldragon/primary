*Kind: Audit Slice · Topic: Spirit runtime, CLI, and contract path · Date: 2026-05-24 · Lane: operator*

# 176.3 · Spirit runtime, CLI, and contract path

## Scope

Read-only audit of:

- `/git/github.com/LiGoldragon/persona-spirit`
- `/git/github.com/LiGoldragon/signal-persona-spirit`
- `/git/github.com/LiGoldragon/owner-signal-persona-spirit`

## CLI Path

`persona-spirit/src/bin/spirit.rs` is exactly the generated CLI invocation:

```rust
signal_frame::signal_cli!(spirit, signal_persona_spirit);
```

The shared `signal_cli!` machinery enforces the one-argument rule, peeks the
NOTA head, routes to the ordinary or owner socket shape, builds a signal frame,
and prints the reply as NOTA.

Boundary tests cover the one-argument rule and generated routing.

Important distinction: CLI routing is still NOTA-head routing. It does not use
`ShortHeader` to choose the socket because the header exists after request
construction.

## Daemon Ingress Path

The daemon takes one NOTA `DaemonConfiguration` argument and binds ordinary,
owner, and upgrade sockets.

Ordinary ingress reads decoded signal frames and sends them through
`SubmitFrameRequest`. Dispatch then goes through:

1. decoded `Operation`
2. `DispatchPhase`
3. `signal_executor::Executor`
4. `SpiritLowering`
5. `SpiritCommandExecutor`
6. `SpiritStore`

That means the ordinary request path does use the new signal-executor/component
command architecture.

It does not use generated `OperationDispatch` to route by `ShortHeader` before
full frame decode.

## Store Path

`SpiritStore` persists current records as:

- `StoredRecord`
- `StampedEntry`
- current `Entry`
- current `Magnitude`

It opens sema-engine with a schema version and uses current sema-engine storage
operations. There is no runtime read-side old-to-new projection hook in
`persona-spirit` itself.

## Upgrade Socket Path

Spirit exposes a private upgrade socket and handles:

- `AskHandoverMarker`
- `ReadyToHandover`
- `HandoverCompleted`
- `Mirror`
- `Divergence`
- `RecoverFromFailure`

The root actor freezes public writes during readiness and closes ordinary/owner
socket paths after handover completion. Tests cover upgrade socket behavior,
freezing, completion, and mirroring `StampedEntry` payloads.

This path is real inside `persona-spirit`, but the nspawn migration runner does
not yet drive it as the end-to-end cutover mechanism.

## Contract Path

The ordinary Spirit contract uses `spirit.schema` through
`signal_channel!([schema])`.

The owner Spirit contract remains handwritten. It has not yet moved into a
schema input file.

## Verdict

Spirit is no longer a fake pilot: the CLI is generated, the ordinary signal
contract is schema-backed, and production dispatch uses `signal-executor`.

The remaining gap is narrower and sharper: the daemon receives decoded frames,
not short-header-routed frame envelopes, and upgrade migration is external and
handwritten rather than schema-derived.
