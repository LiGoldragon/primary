# Rust Auditor Review

Task and scope: follow-up audit for the harness stream fix and terminal README cleanup. Reviewed the changed Rust and README files named in the brief, checked the `signal-harness` stream contract, and ran focused tests. No repository source files were edited, committed, or pushed.

## Findings

### Medium: a second `WatchHarnessTranscript` on an already-open watch stream creates an unowned subscription

File: `/git/github.com/LiGoldragon/harness/src/daemon.rs:775`

Risk: `HarnessTranscriptWireStream::handle_request` only treats matching `UnwatchHarnessTranscript` specially. Every other request on the subscribed socket is routed through `HandleHarnessRequest` at `/git/github.com/LiGoldragon/harness/src/daemon.rs:793`. If that request is another `WatchHarnessTranscript`, `HarnessRequestHandler::watch_transcript_event` opens a new `TranscriptSubscriptionSink::new()` memory-backed subscription at `/git/github.com/LiGoldragon/harness/src/daemon.rs:941` and `/git/github.com/LiGoldragon/harness/src/daemon.rs:949`. That second subscription is not attached to the accepted socket and has the same domain token shape, `HarnessTranscriptToken { harness }`, as the first subscription. A later same-token unwatch closes only the first matching manager entry at `/git/github.com/LiGoldragon/harness/src/subscription.rs:586`, leaving the extra memory subscription open and still reachable by publisher fanout.

Expected correction: on a subscribed stream, either reject a nested `WatchHarnessTranscript` with typed `HarnessRequestUnimplemented`/protocol error, or promote it into a real second stream with a distinct routeable token and socket writer. Add an architecture witness that sends `WatchHarnessTranscript`, then a second `WatchHarnessTranscript` on the same stream, then publishes an observation and closes; the test should prove no extra handler remains and no deltas fan out to an unreachable sink.

## Fixed Findings Verified

The previous high issue, "watch returns only a snapshot and does not preserve a wire stream," is fixed for the primary path. `HarnessEngine::handle_working_stream` now branches `WatchHarnessTranscript` into `handle_transcript_stream` at `/git/github.com/LiGoldragon/harness/src/daemon.rs:125`; that path creates a channel sink and then serves the original accepted stream through `HarnessTranscriptWireStream::serve` at `/git/github.com/LiGoldragon/harness/src/daemon.rs:159`. The stream loop keeps reading requests and receiving subscription events on the same socket at `/git/github.com/LiGoldragon/harness/src/daemon.rs:742`.

The previous medium close-path issue is fixed for same-stream unwatch. A matching `UnwatchHarnessTranscript` is handled in `HarnessTranscriptWireStream::handle_request` at `/git/github.com/LiGoldragon/harness/src/daemon.rs:785`, closes the manager subscription, and the final delivery event is written as `HarnessSubscriptionRetracted` before the serve loop returns at `/git/github.com/LiGoldragon/harness/src/daemon.rs:822` and `/git/github.com/LiGoldragon/harness/src/daemon.rs:753`.

Transcript deltas now use the streaming frame boundary. `HarnessTranscriptWireStream::write_stream_event` writes `HarnessFrameBody::SubscriptionEvent` at `/git/github.com/LiGoldragon/harness/src/daemon.rs:839`. The focused async daemon test decodes and asserts `HarnessFrameBody::SubscriptionEvent` at `/git/github.com/LiGoldragon/harness/tests/daemon.rs:700` and `/git/github.com/LiGoldragon/harness/tests/daemon.rs:1018`.

The stream lifecycle cleanup path is credible for ordinary disconnect/write failure: `serve` calls `close_after_stream_error` on read/write errors at `/git/github.com/LiGoldragon/harness/src/daemon.rs:749` and `/git/github.com/LiGoldragon/harness/src/daemon.rs:760`, and that asks the instance to close the token at `/git/github.com/LiGoldragon/harness/src/daemon.rs:861`. I did not find a deadlock in the same-stream close path: the manager emits the final ack into the channel before the stream writer waits to write it.

The terminal README no longer contradicts archival status. It leads with archived/inactive status and directs active V1 harness work to `terminal-cell` at `/git/github.com/LiGoldragon/terminal/README.md:5`. Later active-sounding command descriptions are framed as prior, transitional, local helper, or witness details rather than the active harness-control component.

## Test Witness Assessment

Meaningful witnesses added/verified:

- `/git/github.com/LiGoldragon/harness/tests/daemon.rs:622` proves same-stream unwatch returns a typed `HarnessSubscriptionRetracted` on the subscribed daemon socket.
- `/git/github.com/LiGoldragon/harness/tests/daemon.rs:660` proves the in-process daemon stream keeps the socket alive, accepts a published observation, emits it as a `SubscriptionEvent`, and then returns the final ack.
- `/git/github.com/LiGoldragon/harness/flake.nix:124` through `/git/github.com/LiGoldragon/harness/flake.nix:126` exposes these focused witnesses as named flake checks.

Residual test gap: the spawned-daemon unwatch test does not explicitly assert EOF after the final ack. The implementation does return from `serve` after writing the final ack, so I do not classify this as a behavior defect, but the witness would be stronger if it read EOF or used a timeout to prove the daemon closed the subscribed stream.

## Commands Run

- `cargo test --test daemon harness_daemon_unwatch_transcript_returns_final_retraction_ack_on_subscribed_stream -- --exact` in `/git/github.com/LiGoldragon/harness`: passed.
- `cargo test --test daemon harness_daemon_watch_transcript_stream_delivers_published_observation_and_final_ack -- --exact` in `/git/github.com/LiGoldragon/harness`: passed.
- `cargo test --test daemon harness_daemon_watch_transcript_returns_typed_snapshot -- --exact` in `/git/github.com/LiGoldragon/harness`: passed.
- `cargo test --test daemon harness_daemon_returns_typed_unimplemented -- --exact` in `/git/github.com/LiGoldragon/harness`: passed.
- `cargo test --test daemon harness_daemon_answers_status_readiness -- --exact` in `/git/github.com/LiGoldragon/harness`: passed.
- `cargo test --test daemon` in `/git/github.com/LiGoldragon/harness`: passed, 13 tests.
- `cargo test --test subscription_truth` in `/git/github.com/LiGoldragon/harness`: passed, 7 tests.
- `cargo test --test actor_discipline_truth` in `/git/github.com/LiGoldragon/harness`: passed, 2 tests.
- `cargo test --test actor_runtime_truth` in `/git/github.com/LiGoldragon/harness`: passed, 10 tests.
- `cargo test --test actor_runtime_truth harness_transcript -- --nocapture` in `/git/github.com/LiGoldragon/harness`: passed with 0 selected tests.
- `cargo test --test message_router_harness_e2e -- --nocapture` in `/git/github.com/LiGoldragon/harness`: failed with the known router-side `rkyv archive deserialization failed`, then `expected SubmissionAccepted, got Error("router socket unreachable; message not forwarded")` at `/git/github.com/LiGoldragon/harness/tests/message_router_harness_e2e.rs:67`.
- `jj status` in `/git/github.com/LiGoldragon/harness`: working copy has the expected modified `flake.nix`, `src/daemon.rs`, `src/subscription.rs`, and `tests/daemon.rs`.
- `jj status` in `/git/github.com/LiGoldragon/terminal`: working copy includes modified `README.md` plus other pre-existing modified docs.

## Residual Risks

The known `message_router_harness_e2e` failure does not appear related to this stream repair: the test sends a message CLI request through message/router/harness and does not use `WatchHarnessTranscript`, `UnwatchHarnessTranscript`, or subscription event frames.

The stream event frame currently writes `SubscriptionTokenInner::new(1)` for every watch stream at `/git/github.com/LiGoldragon/harness/src/daemon.rs:841`. This is acceptable only under the current one-watch-per-connection assumption; if the daemon later supports multiple simultaneous stream subscriptions on one socket, the frame token must become a real per-stream routing token and the tests should assert it.
