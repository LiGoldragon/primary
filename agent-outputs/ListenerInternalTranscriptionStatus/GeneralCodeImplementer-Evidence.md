# Listener Internal Transcription Actor Implementation Evidence

## Task And Scope

Tracker item: `primary-acmr.2`.

Implemented the Listener runtime side of internal OpenAI transcription and
UI-safe status events. Scope was limited to Rust/runtime support in
`/git/github.com/LiGoldragon/listener`; no CriomOS-home status-bar wiring,
deployment, real microphone smoke test, secret value readout, or transcript/audio
artifact inspection was performed.

## Context Consulted

- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/TrackerWeaver-WorkGraph.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/ListenerFreshHandover/ContextHandover.md`
- `/home/li/primary/agent-outputs/ListenerDirectSttConfig/OperatingSystemImplementer-Evidence.md`
- `bd show primary-acmr.2`
- Listener `AGENTS.md`, `ARCHITECTURE.md`, `README.md`
- signal-listener `AGENTS.md`, `ARCHITECTURE.md`, `README.md`
- Whisrs OpenAI REST transcription source and the CriomOS-home stopgap wrapper
  behavior, without reading or reporting secrets.

## Repos And Commits

Changed and pushed:

- `/git/github.com/LiGoldragon/listener`
- commit `da771e23fae4`: `listener: internal OpenAI transcription and status stream`

Assessed but unchanged:

- `/git/github.com/LiGoldragon/signal-listener`
- current `main` remained `16b54472`

Not changed:

- `/git/github.com/LiGoldragon/meta-signal-listener`

## Files Changed

Listener changed files:

- `ARCHITECTURE.md`
- `README.md`
- `Cargo.toml`
- `Cargo.lock`
- `src/capture.rs`
- `src/configuration.rs`
- `src/daemon.rs`
- `src/error.rs`
- `src/lib.rs`
- `src/runtime.rs`
- `src/status.rs`
- `src/transcription.rs`
- `tests/capture.rs`
- `tests/runtime.rs`

## Runtime Shape

Production `ListenerRuntime::from_configuration_with_status` now constructs an
internal `OpenAiBatchTranscriptionActor` instead of using
`LISTENER_TRANSCRIPTION_PROGRAM` as the normal path.

The actor is a bounded worker-thread mailbox:

- input: `BatchTranscriptionRequest`;
- queue capacity: one in-flight/admitted request;
- owned state: current in-flight artifact plus request execution resources;
- execution: converts exported Listener raw `s16le` PCM to an in-memory WAV
  upload, reads the OpenAI credential through `gopass show -o openai/api-key`,
  calls OpenAI REST `/v1/audio/transcriptions` with `gpt-4o-transcribe`, and
  returns the terminal `TranscriptText` or typed Listener error through a reply
  channel;
- timeout: caller waits with a bounded timeout and reports actor timeout as a
  transcription actor failure;
- status: publishes `transcribing` when request execution begins and `error` on
  actor/backend failure.

The external command transcriber remains only as an explicit development seam
behind `LISTENER_DEVELOPMENT_TRANSCRIPTION_PROGRAM`; the old
`LISTENER_TRANSCRIPTION_PROGRAM` default production path was removed from the
Listener repo.

## Status Stream Shape

Added Listener-owned local status stream in `src/status.rs`.

Default socket path:

- `$XDG_RUNTIME_DIR/listener/status.sock`
- override: `LISTENER_STATUS_SOCKET`

Frame shape:

```json
{"state":"idle|recording|transcribing|copied|error","level":0.0}
```

The status stream carries only state and normalized microphone level. It does
not carry transcript text. New clients receive the current event immediately;
subsequent events are pushed as newline-delimited JSON. `copied` and `error`
are terminal UI events that return to `idle` after a short delay in the stream
owner.

Microphone activity is computed at the capture-writer PCM payload boundary as
RMS over `s16le` samples using `1.0 - exp(-rms * 18.0)`, clamped to `0.0..=1.0`.

Runtime transitions now publish:

- `recording` on successful start and on payload-level microphone activity;
- `transcribing` from the internal actor when OpenAI work begins;
- `copied` after successful transcript delivery to at least one configured
  target with no delivery failures;
- `error` for capture stop/recovery/export/transcription/delivery failures;
- `idle` from the status stream after terminal copied/error events, and directly
  when stop completes with no delivery targets.

The existing public `signal-listener` start/status/stop request-reply behavior
and exchange identity were preserved. `CaptureStopped` still contains transcript
text for the existing stop reply, and was not reused as a bar/status feed.

## Credential Handling

Listener reads the OpenAI credential at transcription request time by spawning:

```sh
gopass show -o openai/api-key
```

No secret value was printed, recorded, committed, or included in this evidence.
No live OpenAI transcription request was run by this implementation pass.

## Versioning

Listener package version was bumped from `0.3.0` to `0.4.0` because the default
runtime transcription behavior changed from external command seam to internal
OpenAI actor plus status stream.

No `signal-listener` wire contract version change was needed because the UI
status surface is a Listener-owned local JSON socket, not a public Signal
operation or reply change.

## Checks Run

Local Rust checks:

- `cargo test --test runtime` passed: 13 tests passed.
- `cargo test` passed: all Listener tests passed.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.

Nix checks:

- `nix build .#checks.x86_64-linux.test .#checks.x86_64-linux.clippy .#checks.x86_64-linux.fmt --no-link --print-out-paths` passed after the `0.4.0` version bump.

Focused coverage added or preserved:

- status stream newline JSON framing;
- no transcript text in status events;
- recording/transcribing/copied event publication;
- normalized microphone level while recording;
- existing socket exchange identity for public status;
- existing typed lifecycle conflict replies.

Checks intentionally not run:

- no real spoken microphone smoke test;
- no live OpenAI request;
- no CriomOS-home status-bar integration check.

## Tracker State

`primary-acmr.2` implementation evidence is this file. The item was closed
after Listener commit `da771e23fae4` passed local and Nix checks.

## Blockers And Follow-Up

No implementation blocker remains for `primary-acmr.2`.

Recommended audit scope for `primary-acmr.3`:

- verify the actor boundary is sufficient despite the existing synchronous
  request/reply stop path waiting for the actor terminal reply;
- inspect status stream lifecycle and the delayed idle semantics for copied and
  error;
- verify OpenAI request construction, WAV conversion, and gopass error handling
  do not leak secrets or transcript text;
- confirm `LISTENER_TRANSCRIPTION_PROGRAM` is fully absent from the Listener
  production path and only the explicit development seam remains;
- confirm existing public Signal contract compatibility and typed conflict
  behavior remain intact.
