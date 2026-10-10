# Rust Auditor Review

Task: audit approved tracker item `primary-qvud.5` across Listener's three-repo component family:

- `/git/github.com/LiGoldragon/listener`
- `/git/github.com/LiGoldragon/signal-listener`
- `/git/github.com/LiGoldragon/meta-signal-listener`

Scope checked against the approved vertical slice: fresh Listener component family, default-source capture, continuous durable disk artifact, batch transcription on stop, first output to system clipboard while leaving multiple configured outputs open, no deferred safeguards, and no hard binding to a removable source node.

Spirit grounding: `PublicTextSearch` for listener/speech/transcription/signal returned only broad architecture/process records (`hv5f`, `obo5`, `ty3g`) and no listener-specific record. I used the approved task brief as the controlling listener intent.

## Findings

### High: daemon transport does not use the exported `signal-listener` frame contract

Risk: peers that implement the contract as documented and tested cannot reliably talk to the daemon. The contract exports a `Frame` type over `signal-frame` and its tests prove length-prefixed `Frame` round trips, but the runtime daemon and CLI use a local `ContractFrameCodec` that length-prefixes raw `Input::encode_signal_frame()` and raw `Output::encode_signal_frame()` payloads. That means the worker claim "length-prefixed signal-listener frames over Unix socket" is at best ambiguous and likely false for the public `signal_listener::Frame` type.

Evidence:

- `/git/github.com/LiGoldragon/signal-listener/src/schema/lib.rs:1248` defines `pub type Frame = signal_frame::ExchangeFrame<Input, Output>`.
- `/git/github.com/LiGoldragon/signal-listener/src/schema/lib.rs:1258` and `:1272` add `Input::into_frame` and `Output::into_reply_frame`.
- `/git/github.com/LiGoldragon/signal-listener/tests/round_trip.rs:27` and `:43` assert `Frame::encode_length_prefixed()` / `Frame::decode_length_prefixed()` request and reply round trips.
- `/git/github.com/LiGoldragon/listener/src/transport.rs:41` through `:58` directly decode/encode `Input` and `Output` root frames.
- `/git/github.com/LiGoldragon/listener/src/transport.rs:61` through `:92` adds a daemon-local 4-byte big-endian length prefix instead of using the generated `Frame` boundary.
- `/git/github.com/LiGoldragon/listener/tests/runtime.rs:239` through `:252` tests the daemon socket with the same private `ContractFrameStream`, so the test cannot catch a public contract frame mismatch.

Expected correction: either make the daemon/client transport speak `signal_listener::Frame` / `FrameBody` / `ReplyEnvelope` on the Unix socket, preserving exchange identity in replies, or explicitly move this root-enum length-prefixed protocol into `signal-listener` as the public daemon protocol and test it there. Add an architectural witness where a client-built `Input::into_frame(...).encode_length_prefixed()` request reaches `ListenerSocketServer` and the response decodes as the corresponding contract reply frame. The tempting local `ContractFrameStream` shortcut should not be the only passing path.

### Medium: active capture durability is weaker than the "continuous durable write" claim

Risk: a crash or forced daemon loss during active capture can lose buffered audio even though status has already advertised a durable artifact path. The process writer buffers data and calls `sync_all()` only after EOF, which happens after stop kills/waits for the capture process. That is clean-stop durability, not continuous durability while capture is active.

Evidence:

- `/git/github.com/LiGoldragon/listener/src/capture.rs:201` through `:209` stops by killing/waiting for the process and then joining the writer.
- `/git/github.com/LiGoldragon/listener/src/capture.rs:227` through `:234` uses `std::io::copy` into a `BufWriter`, then flushes and `sync_all()` only after the capture stream ends.
- `/git/github.com/LiGoldragon/listener/tests/runtime.rs:75` through `:84` and `:103` through `:109` prove active/stopped writes through a fake backend that explicitly calls `sync_all()`, not through the production `CaptureWriter`.

Expected correction: define the durability guarantee precisely. If the slice promises active durability, write in chunks with a bounded flush/sync policy and add a production-writer witness that bytes are visible and flushed before stop. If the intended guarantee is only "durable on clean stop", adjust README/architecture wording and tests to stop claiming continuous durability.

### Medium: ordinary domain failures are collapsed into `RequestUnimplemented(NotBuiltYet)`

Risk: callers cannot distinguish "already capturing", "no active capture", and "wrong session" from an unimplemented operation. That is a contract/runtime mismatch once Start/Stop are implemented, and it makes CLI output misleading during normal user mistakes.

Evidence:

- `/git/github.com/LiGoldragon/listener/src/error.rs:25` through `:32` has typed errors for `CaptureAlreadyActive`, `NoActiveCapture`, and `CaptureSessionMismatch`.
- `/git/github.com/LiGoldragon/listener/src/runtime.rs:52` through `:62` maps every operation error into `RequestUnimplemented`.
- `/git/github.com/LiGoldragon/listener/src/runtime.rs:218` through `:229` maps those ordinary domain errors through the fallback `_ => UnimplementedReason::NotBuiltYet`.
- `/git/github.com/LiGoldragon/signal-listener/schema/lib.schema:10` through `:13` provides no ordinary rejected/conflict reply variants other than `RequestUnimplemented`.

Expected correction: add typed operation failure replies, or use the signal-frame rejection envelope consistently for request-state conflicts. Add tests for start-while-active, stop-with-no-active-capture, and stop-with-mismatched-session, asserting the public reply is not `RequestUnimplemented(NotBuiltYet)`.

## Acceptance

The vertical slice is acceptable to start using as a local stub/configurable first cut through its own `listener` CLI and daemon, provided use is limited to clean start/stop experiments and the transcript is understood to be a configurable/stub backend unless `LISTENER_TRANSCRIPTION_PROGRAM` is set.

I would not close this as a contract-compatible component boundary yet. The daemon frame mismatch is a real public boundary risk and should be fixed before other clients or components depend on `signal-listener` as the socket protocol.

## Residual Risks

- `meta-listener` remains a scaffold: `/git/github.com/LiGoldragon/listener/src/meta.rs:25` through `:33` prints a scaffold message and returns `NotImplemented`. This is acceptable only because dynamic owner/meta configuration was not required for the first runtime slice.
- Runtime output targets are structurally open through `OutputTargets(Vec<OutputTarget>)`, but process environment configuration currently always constructs `[SystemClipboard]` in `/git/github.com/LiGoldragon/listener/src/configuration.rs:119` through `:131`.
- Capture uses `parecord --device=@DEFAULT_SOURCE@` in `/git/github.com/LiGoldragon/listener/src/capture.rs:126` through `:138`, which avoids hard-binding to a removable node at startup. It does not prove behavior if the system default changes during an active recording; that live-follow behavior was not separately tested.
- Nix checks were run for the current `x86_64-linux` system. The flake command warned that `aarch64-linux` outputs were omitted.

## Verification

Repositories and commits:

- `listener`: clean Jujutsu working copy over `c2f5e33e6c2bf7a46d06b151931810a7618c77a5` (`listener: implement first speech slice`).
- `signal-listener`: clean Jujutsu working copy over `e2a390b0ae56fcf38a0a3749731b3290d2db5630` (`signal-listener: define vertical slice contract`).
- `meta-signal-listener`: clean Jujutsu working copy over `30ed27707ea792ac8b6fa371ec250d1e220ef5bd` (`meta-signal-listener: consume listener vertical slice contract`).

Commands run:

- `cargo fmt --check` in all three repos: passed.
- `cargo test --locked` in `listener`: passed; 1 configuration integration test and 4 runtime integration tests passed.
- `cargo test --locked` in `signal-listener` and `meta-signal-listener`: passed but ran no integration tests because round-trip tests require `nota-text`.
- `cargo test --locked --features nota-text` in `signal-listener`: passed; 4 round-trip/projection tests passed.
- `cargo test --locked --features nota-text` in `meta-signal-listener`: passed; 3 round-trip/projection tests passed.
- `cargo clippy --locked --all-targets --all-features -- -D warnings` in all three repos: passed.
- `cargo tree --locked -e normal -i tokio` in all three repos and `cargo tree --locked -e normal -i kameo` in `signal-listener`: no normal dependency path printed.
- `rg` checks for sibling `path = "../..."`, `anyhow`, `eyre`, local duplicate generated wire shapes, and relevant capture/transcription/clipboard seams: no path deps or `anyhow`/`eyre` boundary leaks found.
- `nix flake check --print-build-logs` in all three repos: command reported all checks passed for the current system; `aarch64-linux` was omitted by Nix as incompatible with the current run.

## Recommended Next Work

1. Fix the daemon socket protocol to use the contract `Frame` type, or move the daemon's root-enum frame protocol into `signal-listener` and make that the tested public boundary.
2. Decide and encode the active-capture durability guarantee. If "continuous durable" remains the claim, make `CaptureWriter` flush/sync during capture and test the production writer.
3. Add typed public failure outcomes for ordinary Start/Stop state conflicts.
4. Add a CLI-through-daemon integration test that starts, status-checks, stops, and decodes the public contract reply path without reusing the daemon's private test codec.
5. Leave deferred safeguards out of this slice unless the tracker item is reopened to include them.
