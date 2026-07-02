# Rust Auditor Re-Audit

## Task And Scope

Tracker item: `primary-acmr.3`.

Re-audited Listener after the targeted fix for the prior blocking finding:
`Error::TranscriptionActorUnavailable` previously fell through to
`RequestUnimplemented(NotBuiltYet)` instead of the typed public reason
`TranscriptionBackendUnavailable`.

Reviewed commits:

- `/git/github.com/LiGoldragon/listener`
  - original implementation `da771e23fae4824406eea0ea0fb4dad56d063f3a`
  - targeted fix `4080f8e89acc173ac124d814147e13dcb971a7a5`
- `/git/github.com/LiGoldragon/signal-listener`
  - unchanged contract commit `16b54472f43c9e3cf20b5bef726617156ce8b3a4`

Context read:

- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/RustAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/GeneralCodeImplementer-PrimaryAcmr3FixEvidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/Scout-SituationalMap.md`
- `bd show primary-acmr.3 --json`
- Listener and signal-listener `AGENTS.md`, `ARCHITECTURE.md`, and Listener `skills.md`

Spirit query:

- `PublicTextSearch [listener transcription openai status]` returned no
  matching public record. The audit used the explicit task brief and tracker
  acceptance criteria as authority.

## Result

Audit result: **pass**.

No blocking findings remain for `primary-acmr.3`. The prior finding is fixed:
all `Error::TranscriptionActorUnavailable` cases are mapped to the existing
typed public `UnimplementedReason::TranscriptionBackendUnavailable`, and the
new runtime test covers both the public stop reply and an `error` status event.

`primary-acmr.4` can start after tracker closure because its direct blocker
`primary-acmr.3` has passed.

## Findings

No findings.

## Prior Finding Verification

Observed facts:

- `OpenAiBatchTranscriptionActor::transcribe` returns
  `Error::TranscriptionActorUnavailable` when the actor send fails, when the
  reply wait times out, and when the reply channel disconnects:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:123`.
- `Error::unimplemented_reason` now maps both
  `TranscriptionBackendUnavailable` and `TranscriptionActorUnavailable` to
  `UnimplementedReason::TranscriptionBackendUnavailable`:
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:380`.
- `ListenerRuntime::stop` publishes an error status event and returns the error
  when transcription fails:
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:137`.
- The new regression test drives the runtime start/stop path with a transcriber
  that returns `Error::TranscriptionActorUnavailable`, then asserts:
  - public reply is `RequestUnimplemented`;
  - operation kind is `Stop`;
  - reason is `TranscriptionBackendUnavailable`;
  - status events include `ListenerStatusState::Error`.
  Test location:
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:593`.

Interpretation:

- The actor's concrete timeout, disconnect, and unavailable paths share the same
  typed internal error variant, and that variant now reaches the public stop
  reply as `TranscriptionBackendUnavailable`.
- The regression test is meaningful for the public boundary and status event.
  It does not wait for a real 75-second actor timeout, which is acceptable here
  because source inspection verifies the timeout/disconnect conversion into the
  same error variant exercised by the test.

## Reconfirmed Audit Assurances

### Production OpenAI Transcription

Observed facts:

- `ListenerRuntime::from_configuration_with_status` constructs
  `OpenAiBatchTranscriptionActor::from_environment` for the normal runtime path:
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:36`.
- The actor owns a bounded mailbox sender and worker thread:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:95`.
- `TranscriptionActorWorker` owns the OpenAI REST transcriber, status publisher,
  mailbox receiver, and in-flight artifact state:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:146`.
- The REST transcriber builds a blocking `reqwest` client, reads the key from
  `gopass show -o openai/api-key`, prepares a WAV upload, and posts to OpenAI
  REST transcription with `gpt-4o-transcribe`:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:232`.
- Source search in Listener found no `LISTENER_TRANSCRIPTION_PROGRAM` and no
  `listener-openai-transcribe`.
- The remaining external transcription seam is explicitly
  `LISTENER_DEVELOPMENT_TRANSCRIPTION_PROGRAM`:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:508`.
- Listener source search found no Whisrs dependency or production path. The only
  Whisrs source reference in runtime code is an OpenAI prompt vocabulary term.

Interpretation:

- Listener owns production OpenAI transcription internally.
- The old production external command path is absent from Listener.
- The remaining external command seam is development-only.
- Whisrs remains separate and side by side.

### UI-Safe Status Socket

Observed facts:

- `listener-daemon` starts `StatusStreamServer` and passes its publisher into
  the runtime:
  `/git/github.com/LiGoldragon/listener/src/daemon.rs:37`.
- Default status socket is `$XDG_RUNTIME_DIR/listener/status.sock` with
  `LISTENER_STATUS_SOCKET` override:
  `/git/github.com/LiGoldragon/listener/src/configuration.rs:121`.
- `ListenerStatusEventFrame` serializes only `state` and `level`:
  `/git/github.com/LiGoldragon/listener/src/status.rs:134`.
- Status states are `idle`, `recording`, `transcribing`, `copied`, and `error`:
  `/git/github.com/LiGoldragon/listener/src/status.rs:19`.
- New clients receive the current JSON-line event immediately, and copied/error
  events return to idle after a short delay:
  `/git/github.com/LiGoldragon/listener/src/status.rs:353`.
- Runtime tests prove JSON-line framing, recording/transcribing/copied events,
  nonzero recording level, and absence of transcript text in status event JSON:
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:543` and
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:626`.

Interpretation:

- The status socket is safe for a persistent bar consumer. It exposes state and
  normalized microphone level only, not transcript text.

### Microphone Level And State Coherence

Observed facts:

- Microphone level is RMS over signed 16-bit little-endian PCM with
  `1.0 - exp(-rms * 18.0)`, clamped to `0.0..=1.0`:
  `/git/github.com/LiGoldragon/listener/src/status.rs:64`.
- Capture writer publishes recording level after each complete committed PCM
  payload chunk:
  `/git/github.com/LiGoldragon/listener/src/capture.rs:439`.
- Runtime publishes recording, transcribing, copied, error, and idle/no-target
  transitions through the status publisher:
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:188` and
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:249`.

Interpretation:

- Recording microphone activity and state transitions remain coherent for the
  status-bar consumer shape.

### Public Contract And Typed Conflicts

Observed facts:

- `signal-listener` remains at the start/stop/status request-reply vocabulary
  with typed lifecycle conflicts and `RequestUnimplemented` reasons:
  `/git/github.com/LiGoldragon/signal-listener/schema/lib.schema:7`.
- Listener `Cargo.lock` pins `signal-listener` to
  `16b54472f43c9e3cf20b5bef726617156ce8b3a4`:
  `/git/github.com/LiGoldragon/listener/Cargo.lock:1198`.
- Runtime tests still prove typed active/no-active/session-mismatch conflict
  replies:
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:644`.
- Socket tests still prove public status and conflict replies preserve the
  exchange identifier:
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:732` and
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:785`.

Interpretation:

- Existing typed conflict and exchange behavior remains intact.
- No signal-listener contract change was needed for the Listener-local status
  socket.

### Secret And Transcript Handling

Observed facts:

- No secret values were read.
- No live OpenAI request was made.
- No transcript contents or audio artifact contents were inspected.
- OpenAI HTTP error handling reports status or decode failure, not response
  body:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:390`.

Interpretation:

- This audit did not expose secrets or transcript text.

## Checks Run

In `/git/github.com/LiGoldragon/listener`:

- `cargo fmt --check` passed.
- `cargo test --test runtime stop_actor_unavailable_returns_transcription_backend_unavailable_reply` passed: 1 test passed.
- `cargo test --test runtime` passed: 14 tests passed.
- `cargo test` passed: 20 tests passed across integration tests; doc tests and unit test harnesses had zero tests.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.

Inspected but not rerun:

- Fix evidence reports
  `nix build .#checks.x86_64-linux.test .#checks.x86_64-linux.clippy .#checks.x86_64-linux.fmt --no-link --print-out-paths`
  passed after commit `4080f8e8`.
- `signal-listener` was unchanged at the audited commit; its schema and
  Listener lockfile pin were inspected instead of rerunning its checks.

## Residual Risks

- No real microphone smoke test was run.
- No live OpenAI transcription request was run.
- The new regression test uses a synthetic `TranscriptionActorUnavailable`
  transcriber to keep the runtime test fast; the actor source maps real send
  failure, timeout, and disconnect into that same error variant.

## Tracker Action

`primary-acmr.3` may be closed with this report as audit evidence. Closing it
unblocks `primary-acmr.4`.
