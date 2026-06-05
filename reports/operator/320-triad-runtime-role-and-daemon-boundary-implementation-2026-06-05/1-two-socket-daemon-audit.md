# Two-Socket Daemon Audit

## Finding

The claim was substantively true. `triad-runtime` previously exposed a single-socket daemon shell. Cloud's prototype avoided the generated engine path and hand-rolled ordinary/meta socket handling, which meant there was no shared runtime shape for a triad daemon with both `signal-*` and `meta-signal-*` doors.

## Implementation

The fix landed in `triad-runtime` as a reusable multi-listener shell:

- `MultiListenerRuntime` owns one mutable runtime instance.
- `ListenerSocket<Listener>` carries socket path plus per-socket `SocketMode`.
- `MultiListenerDaemon<Runtime>` binds any number of Unix sockets, polls them non-blocking, routes accepted streams to the owning runtime with the listener identity, and starts/stops in the shared runtime layer.

This intentionally avoids the naive multi-threaded shape where ordinary and meta listener threads both hold a lock around one engine. The phase-one shape has many listeners but one engine owner, preserving the single-writer runner model.

## Proof

`triad-runtime` now has tests for:

- routing two sockets through one runtime owner;
- applying per-socket modes independently.

The runtime shell is ready for future ordinary/meta daemons. Spirit itself remains single-socket because its current pilot surface has no separate meta-signal door.

