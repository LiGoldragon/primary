# Rust Auditor Review

## Task And Scope

Tracker item: `primary-acmr.3`.

Audited Listener internal OpenAI transcription actor and UI-safe status stream
against the approved intent in the brief:

- Listener owns OpenAI transcription in production, without Whisrs and without
  the stopgap `listener-openai-transcribe` command as the normal path.
- Transcription dispatch is actor-shaped and asynchronous because it is
  stateful and long-running.
- UI status is safe: persistent indicators can see state and microphone level,
  but not transcript text or secrets.
- Existing CLI/socket request-reply behavior and exchange identity remain
  intact.

Reviewed commits:

- `/git/github.com/LiGoldragon/listener` commit
  `da771e23fae4824406eea0ea0fb4dad56d063f3a`
- `/git/github.com/LiGoldragon/signal-listener` commit
  `16b54472f43c9e3cf20b5bef726617156ce8b3a4`

Spirit query:

- `PublicTextSearch [listener transcription openai status]` returned no
  matching public record. The audit used the explicit approved intent in the
  task brief as authority.

## Result

Audit result: **fail for `primary-acmr.3` closure** because one terminal
transcription actor error path is misclassified on the public stop reply.

The defect does **not** expose transcript text or secrets and does **not**
invalidate the Listener status socket shape needed by the later bar widget.
It should be fixed before closing `primary-acmr.3`. `primary-acmr.4` remains
tracker-blocked by `primary-acmr.3`; the code issue itself is not a UI/status
surface blocker once the orchestrator decides whether to allow parallel UI work.

## Findings

### Medium: Transcription Actor Timeout/Disconnect Maps To `NotBuiltYet`

Evidence:

- `/git/github.com/LiGoldragon/listener/src/transcription.rs:130`
- `/git/github.com/LiGoldragon/listener/src/transcription.rs:134`
- `/git/github.com/LiGoldragon/listener/src/transcription.rs:136`
- `/git/github.com/LiGoldragon/listener/src/runtime.rs:380`
- `/git/github.com/LiGoldragon/listener/src/runtime.rs:385`
- `/git/github.com/LiGoldragon/listener/src/runtime.rs:396`

`OpenAiBatchTranscriptionActor::transcribe` returns
`Error::TranscriptionActorUnavailable` when the actor send fails, times out, or
disconnects. `Error::unimplemented_reason` maps
`TranscriptionBackendUnavailable` to
`UnimplementedReason::TranscriptionBackendUnavailable`, but
`TranscriptionActorUnavailable` falls through to `NotBuiltYet`.

Risk:

- A real OpenAI actor timeout or actor disconnection during `Stop` is reported
  on the existing public request/reply surface as `RequestUnimplemented` with
  `NotBuiltYet`, even though the production transcription backend is built and
  the terminal failure is a transcription-path failure.
- This weakens the required failure/timeout semantics for the long-running
  actor boundary and can mislead CLI wrappers, operators, and later smoke-test
  evidence.

Expected correction:

- Map `Error::TranscriptionActorUnavailable` to
  `UnimplementedReason::TranscriptionBackendUnavailable`, or add a more precise
  public reason if the contract is intentionally widened later.
- Add a targeted runtime/socket test proving actor timeout or disconnect
  returns the transcription failure reason, not `NotBuiltYet`, while still
  publishing the UI-safe `error` status event.

Blocks:

- Blocks closing `primary-acmr.3`.
- Does not directly block the `primary-acmr.4` status-bar consumer shape.

## Verified Behaviors

### Production Transcription Path

Observed facts:

- `ListenerRuntime::from_configuration_with_status` constructs
  `OpenAiBatchTranscriptionActor::from_environment` as the default transcriber:
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:36`.
- `OpenAiRestTranscriber::from_environment` builds a blocking `reqwest` client,
  uses `OpenAiCredentialSource::gopass("openai/api-key")`, and sends OpenAI
  REST transcription requests:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:232`.
- The old `LISTENER_TRANSCRIPTION_PROGRAM` string is absent from Listener and
  signal-listener source search. The remaining command seam reads only
  `LISTENER_DEVELOPMENT_TRANSCRIPTION_PROGRAM`:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:508`.
- Source search for `listener-openai-transcribe` in Listener and
  signal-listener returned no matches.
- Source search found no Whisrs dependency or production call path in Listener;
  the only Whisrs references are docs/prompt text.

Interpretation:

- The normal Listener runtime path is internal OpenAI transcription, not Whisrs
  and not the stopgap external production command.
- The remaining external command path is explicitly named development-only and
  is not used by `ListenerRuntime::from_configuration_with_status`.

### Actor And State Boundary

Observed facts:

- `OpenAiBatchTranscriptionActor` owns a bounded mailbox sender and reply
  timeout:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:95`.
- `TranscriptionActorWorker` owns the `OpenAiRestTranscriber`,
  `StatusPublisher`, mailbox receiver, and `in_flight` artifact state:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:146`.
- The worker publishes `transcribing`, executes the OpenAI request, publishes
  `error` on backend failure, replies to the caller, then clears `in_flight`:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:181`.
- The daemon stop path still waits synchronously for the actor reply:
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:137`.

Interpretation:

- The OpenAI request execution and in-flight artifact state live behind an
  asynchronous worker-thread mailbox. This is actor-shaped enough for the
  current blocking daemon architecture.
- The stop request/reply path remains blocking, but the UI can observe
  `transcribing` while it blocks because status publication is separate.

### Secret Handling

Observed facts:

- The credential command is `gopass show -o openai/api-key`:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:303`.
- Failure messages mention only process start failure, exit status, or empty
  output; they do not include stdout/stderr or key values:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:307`.
- OpenAI HTTP error handling reports status code or decode error, not response
  body:
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:390`.

Interpretation:

- No secret values were read, printed, committed, or included in this report.

### UI-Safe Status Stream

Observed facts:

- Default status socket is `$XDG_RUNTIME_DIR/listener/status.sock`, with
  `LISTENER_STATUS_SOCKET` override:
  `/git/github.com/LiGoldragon/listener/src/configuration.rs:121`.
- Status frames serialize through `ListenerStatusEventFrame`, which has only
  `state` and `level` fields:
  `/git/github.com/LiGoldragon/listener/src/status.rs:134`.
- Status states are `idle`, `recording`, `transcribing`, `copied`, and `error`:
  `/git/github.com/LiGoldragon/listener/src/status.rs:19`.
- New status clients receive the current newline JSON event immediately:
  `/git/github.com/LiGoldragon/listener/src/status.rs:353`.
- `copied` and `error` schedule an automatic idle transition:
  `/git/github.com/LiGoldragon/listener/src/status.rs:39` and
  `/git/github.com/LiGoldragon/listener/src/status.rs:376`.
- Runtime publishes recording, transcribing, copied, error, and idle/no-target
  transitions:
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:204`,
  `/git/github.com/LiGoldragon/listener/src/transcription.rs:183`,
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:249`.
- Tests assert newline JSON framing and absence of transcript text in status
  event JSON:
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:513` and
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:563`.

Interpretation:

- The status socket is safe for a bar indicator. Transcript text remains in the
  existing `CaptureStopped` reply and delivery path, not the local status feed.

### Microphone Level

Observed facts:

- Microphone level is RMS over `s16le` samples with
  `1.0 - exp(-rms * 18.0)`, clamped to `0.0..=1.0`:
  `/git/github.com/LiGoldragon/listener/src/status.rs:64`.
- Capture writer computes/publishes the level after each committed complete PCM
  payload chunk:
  `/git/github.com/LiGoldragon/listener/src/capture.rs:439`.
- Runtime tests assert a nonzero recording level appears while recording:
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:549`.

Interpretation:

- Level computation is meaningful and wired to the PCM capture path.

### Contract Compatibility

Observed facts:

- `signal-listener` schema remains at the start/stop/status request-reply
  surface with typed lifecycle conflicts:
  `/git/github.com/LiGoldragon/signal-listener/schema/lib.schema:7`.
- Listener tests prove public status and conflict replies preserve the exchange
  identifier:
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:670` and
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:722`.
- Listener `Cargo.lock` pins `signal-listener` to
  `16b54472f43c9e3cf20b5bef726617156ce8b3a4`.

Interpretation:

- Existing public CLI/socket request-reply behavior and exchange identity are
  preserved for the audited surfaces.

## Version And Documentation

Observed facts:

- Listener package version is `0.4.0`:
  `/git/github.com/LiGoldragon/listener/Cargo.toml:1`.
- `Cargo.lock` records Listener `0.4.0`.
- `README.md` and `ARCHITECTURE.md` describe internal OpenAI transcription,
  the development-only command seam, and UI-safe status frames.

Interpretation:

- The version bump and docs are coherent with the behavior change.

## Checks Run

Listener:

- `cargo test --test runtime`: passed, 13 tests.
- `cargo test`: passed, 19 tests across integration suites plus doc tests.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `nix build .#checks.x86_64-linux.test .#checks.x86_64-linux.clippy .#checks.x86_64-linux.fmt --no-link --print-out-paths`: passed with outputs
  `listener-test-0.4.0`, `listener-clippy-0.4.0`, and
  `listener-fmt-0.4.0`.

signal-listener:

- `cargo test`: passed default build/doc tests; the `nota-text` integration
  test is feature-gated and was not run by this command.
- `cargo test --features nota-text`: passed 4 round-trip tests.

Targeted inspection:

- `rg` confirmed `LISTENER_TRANSCRIPTION_PROGRAM` and
  `listener-openai-transcribe` are absent from Listener and signal-listener.
- `rg` confirmed `TranscriptionActorUnavailable` is produced by actor
  send/timeout/disconnect paths and has no explicit public reason mapping.
- `rg` confirmed status frame serialization only exposes `state` and `level`.

## Residual Risks

- No live OpenAI request was run and no real microphone smoke test was run.
  That belongs to `primary-acmr.6`.
- Tests do not exercise the real OpenAI multipart request construction, WAV
  upload bytes, gopass command wrapper, HTTP status handling, or actor timeout
  path. The source is readable and mostly conservative, but coverage should be
  added with a local/mockable boundary before treating the OpenAI actor as
  fully witnessed.
- Tests do not directly assert the `copied`/`error` automatic return-to-idle
  timing on the socket. Source supports it, but a small socket-level witness
  would reduce UI integration risk.

## Tracker Outcome

Recommended tracker state:

- Leave `primary-acmr.3` open with this audit report attached.
- Add or complete a narrow fix for the actor unavailable public reason mapping,
  then rerun the Listener runtime tests and relevant Nix checks.
- Do not close `primary-acmr.3` until that fix is audited or the psyche accepts
  the public reason behavior as intentional.

