# Listener Boundary Fix Evidence

Task: fix the Listener daemon/client ordinary socket boundary so it speaks the exported `signal_listener::Frame` public contract instead of a local payload-only codec.

Scope:

- Edited only `/git/github.com/LiGoldragon/listener`.
- Did not change `signal-listener`, `signal-frame`, or any other contract repository.
- Left durability strategy untouched.

Local guidance and code consulted:

- `/git/github.com/LiGoldragon/listener/AGENTS.md`
- `/git/github.com/LiGoldragon/listener/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/listener/README.md`
- `/git/github.com/LiGoldragon/listener/skills.md`
- `src/transport.rs`, `src/client.rs`, `src/daemon.rs`, `src/runtime.rs`, `src/error.rs`
- `tests/runtime.rs`
- Cached public API source for `signal-listener` and `signal-frame`, specifically `Frame`, `FrameBody`, `Input::into_frame`, `Output::into_reply_frame`, `ExchangeIdentifier`, `Reply`, and `SubReply`.

Observed facts:

- The previous ordinary socket transport length-prefixed `Input::encode_signal_frame()` and `Output::encode_signal_frame()` payloads directly.
- `signal-listener` exports `Frame = signal_frame::ExchangeFrame<Input, Output>` and public helpers `Input::into_frame(exchange)` and `Output::into_reply_frame(exchange)`.
- `Frame::encode_length_prefixed()` and `Frame::decode_length_prefixed()` own the public binary frame shape.
- The public `signal-listener` API exposes `signal_frame::ExchangeIdentifier`, so the listener runtime needs a direct `signal-frame` dependency to name the exchange identity type.

Changed files:

- `Cargo.toml`: added direct `signal-frame` dependency and included `signal-frame/nota-text` in the `nota-text` feature.
- `Cargo.lock`: recorded `signal-frame` as a direct listener dependency.
- `src/transport.rs`: replaced payload-only read/write helpers with public `signal_listener::Frame` read/write; added request/reply boundary objects; client stream mints connector exchanges and checks reply exchange equality; server replies with `Output::into_reply_frame(request.exchange())`.
- `src/client.rs`: sends owned `Input` through the public-frame stream path.
- `src/daemon.rs`: receives a public request frame, lowers its single operation to runtime, and sends a public reply frame preserving exchange identity.
- `src/error.rs`: replaced `signal_listener::SignalFrameError` boundary error with `signal_frame::FrameError` and added typed protocol-shape errors.
- `tests/runtime.rs`: replaced the socket boundary test with a public-frame test using `Input::into_frame(exchange).encode_length_prefixed()` and `Frame::decode_length_prefixed()` on the response.

Exact protocol shape after the fix:

- On the ordinary Listener Unix socket, each message is a `u32` big-endian length prefix followed by a `signal_listener::Frame` archive as produced by `Frame::encode_length_prefixed()`.
- Requests must be `FrameBody::Request { exchange, request }`.
- Listener currently accepts exactly one `Input` payload in the request frame. Multi-operation public frames decode but are rejected by listener as unsupported for this slice.
- Replies are `FrameBody::Reply { exchange, reply }`, where `exchange` is the exact `ExchangeIdentifier` from the request.
- Successful runtime replies are emitted through `Output::into_reply_frame(exchange)`, which wraps the `Output` as a committed `SubReply::Ok` in the public reply envelope.
- The CLI mints connector-lane exchange identifiers for outbound calls and rejects a reply whose exchange does not match the pending request.

Verification:

- `cargo fmt`: passed.
- `cargo test socket_server_answers_public_status_frame_with_matching_exchange`: passed.
- `cargo test`: passed.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `nix flake check --print-build-logs`: passed; checks included build, fmt, clippy, docs, and tests. It warned that `aarch64-linux` was omitted as an incompatible system.

Commit and push:

- Commit: `c21b78f8` (`listener: use public signal frames on socket`).
- Bookmark: `main` points to `c21b78f8`.
- Push: `jj git push --bookmark main` succeeded, advancing `origin/main` from `c2f5e33e` to `c21b78f8`.
- Final listener repo state: clean working copy.

Residual boundary risk:

- No residual risk for the audited public frame boundary: ordinary daemon/client traffic now uses `signal_listener::Frame` encoding and replies preserve exchange identity.
- Listener still accepts only a single operation per public request frame. That matches the current first slice and CLI path, but a future multi-operation client would need an accepted design for batch lowering and reply semantics.
