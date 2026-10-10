# Listener Live Level Responsiveness Implementation Evidence

## Task And Scope

Tracker item: `primary-zddv.3`.

Implemented the Listener runtime/status fix for live microphone-level
responsiveness while recording. Scope stayed in `/git/github.com/LiGoldragon/listener`.
No CriomOS-home shortcut/widget files were edited, no live microphone audio was
read, no transcript or clipboard contents were inspected, and no OpenAI request
was made.

## Context Consulted

Required evidence:

- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/TrackerWeaver-WorkGraph.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/ListenerCancelSemantics/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/RustAuditor-ReAudit.md`

Repository and doctrine context:

- Listener `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, and `skills.md`
- local Rust, component, Nix, testing, work-tracking, reporting, and version-control doctrine
- `bd show primary-zddv.3 --json`
- Spirit public text search for Listener level/status responsiveness returned no matching public record, so the tracker brief and repo architecture were used as authority.

## Root Cause

Observed fact from the scout: Listener status events were not frozen, but while
recording they arrived in multi-second bursts. The first nonzero level events
arrived roughly 2.5 seconds after the recording state, then several frames
arrived within milliseconds. Whisrs emitted roughly every 50 to 55 ms.

Implementation interpretation: Listener's capture path asked `parecord` for the
default buffered stream and sized capture reads to the `.listenerlog` maximum
record payload. The live level publication was also in the durable append path.
That made UI status cadence vulnerable to upstream stdout buffering and durable
record timing, so the status stream saw burst delivery rather than steady
recording-level updates.

## Changed Repo And Commit

Changed and pushed:

- `/git/github.com/LiGoldragon/listener`
- commit `ea47f0b2fb3f`: `listener: steady live capture levels (Codex GPT-5)`

Not changed:

- `/git/github.com/LiGoldragon/signal-listener`
- `/git/github.com/LiGoldragon/CriomOS-home`

## Files Changed

- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `README.md`
- `src/capture.rs`
- `src/status.rs`
- `tests/capture.rs`

## Behavior Implemented

Capture/runtime:

- Default `parecord` arguments now request low-latency capture with
  `--latency-msec=50` and `--process-time-msec=25`.
- `CaptureWriter` now uses a frame-aligned read window derived from the audio
  format and a 50 ms live-level sample duration.
- For Listener's default 16 kHz mono `s16le` format, that read window is 1,600
  bytes instead of the 8,192-byte durable-record ceiling.
- Recording level publication now happens when a complete PCM status window is
  available, before the durable append call for that payload. The durable
  `.listenerlog` append and sync still happen for the same payload afterward.
- The recording log format and recovery rules were not changed.

Status stream:

- Accepted status clients are set nonblocking.
- Broadcast writes now drop clients that cannot accept a full status frame
  instead of allowing a slow/non-reading client to block publication for other
  clients.
- Existing status frame shape remains unchanged: state and level only, with no
  transcript text.

Versioning:

- Listener package version bumped from `0.5.0` to `0.5.1`.
- No `signal-listener` version change was needed because no public Signal
  operation, reply, storage format, or wire contract changed.

## New Status Cadence Behavior

The intended runtime cadence during recording is now one status sample per
roughly 50 ms PCM window when the capture backend delivers data at the requested
low-latency cadence. This is comparable to the Whisrs scout observation of
roughly 50 to 55 ms frames.

The status feed is no longer designed around waiting for the 8,192-byte maximum
`.listenerlog` record payload. The focused test proves the writer requests a
1,600-byte read window for the default format and emits one recording-level event
per 50 ms window while still recovering the durable recording bytes.

## Checks Run

In `/git/github.com/LiGoldragon/listener`:

- `parecord --help | sed -n '1,220p'` passed and showed support for
  `--latency-msec` and `--process-time-msec`.
- `cargo fmt --check` passed.
- `cargo test --test capture capture_writer_samples_live_level_at_fifty_millisecond_pcm_window` passed.
- `cargo test --test runtime status_stream_sends_newline_json_frames` passed.
- `cargo test --test runtime` passed: 17 tests passed.
- `cargo test` passed: 25 tests passed across unit and integration tests; doc tests had zero tests.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `nix build .#checks.x86_64-linux.test .#checks.x86_64-linux.clippy .#checks.x86_64-linux.fmt --no-link --print-out-paths` passed.

## Preserved Behavior

- Cancel semantics from `listener` `a4f1c281` are preserved: cancel retains the
  artifact, skips transcription/OpenAI/clipboard delivery, and publishes
  `cancelled`.
- Internal OpenAI transcription path, typed conflict replies, exchange identity,
  and status socket privacy were preserved.
- Status JSON remains UI-safe and does not include transcript text.
- No Whisrs dependency or shared runtime path was introduced.

## Blockers, Unknowns, And Follow-Up

No implementation blocker remains for `primary-zddv.3`.

This pass did not activate the new Listener build into CriomOS-home and did not
run a live microphone smoke test. Follow-up scope:

- `primary-zddv.4` should update CriomOS-home to pin Listener commit
  `ea47f0b2fb3f` and wire the shortcut changes owned by that bead.
- `primary-zddv.5` should audit this runtime/status change together with the
  cancel contract behavior.
- The OS/UI worker should verify live `status.sock` cadence after activation.
  If the runtime stream is steady but quiet-room levels around `0.06` still move
  the QML bars by only about one pixel, the UI-side fix belongs in
  `primary-zddv.4` or its audit path rather than this runtime pass.
