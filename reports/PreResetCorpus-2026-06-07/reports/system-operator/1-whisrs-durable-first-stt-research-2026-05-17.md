# Whisrs Durable-First STT Research

Role: second-system-assistant
Date: 2026-05-17
Bead: `primary-ipjx` - "[epic] Rethink speech-to-text recording as durable-first infrastructure"

## Executive Finding

The current CriomOS speech-to-text path is not durable-first. It is
memory-first with a recovery spool after failure. Normal batch dictation keeps
the only complete audio in a process-owned sample buffer until stop, builds an
in-memory WAV, sends that to the configured backend, and writes a recovery file
only if transcription fails. Streaming backends reduce latency, but they still
do not make the original audio durable before transcription begins.

The closest outside model is not another Linux drop-in tool. It is the
"capture" object model used by tools like Voicebox: every dictation produces a
recording artifact paired with transcript state, and that object can be
replayed, retranscribed, refined, exported, or deleted later. Wispr Flow and
Willow show the same user-facing expectation in closed products: failed
transcriptions are recoverable from history because the recording was preserved.
OpenWhispr has an optional local audio-retention policy, but optional retention
is not the safety guarantee this bead asks for. Voxtype is the strongest
Linux-native neighbor for local models and long-form chunking, but it is still a
different tool and not evidence that Whisrs already has the right storage
shape.

Recommendation: keep the CriomOS Whisrs integration for Niri/uinput/Nix
fit, but redesign Whisrs around a durable `RecordingSession` object. Capture
writes to durable state as audio arrives; stop finalizes a recording artifact
and enqueues transcription; transcription consumes the artifact and records
attempt state. Streaming can remain an online accelerator, but it must consume
audio after the durable write, not replace it.

## Bead Context

`primary-ipjx` names the incident and the target architecture. The incident was
a 14:14.95 recording that became a 27,358,538 byte in-memory WAV, tripped the
OpenAI REST 25 MiB upload limit, and then got stuck while trying to spool Opus
through `ffmpeg`. The bead's requirements are correct:

- audio is never only in process memory once recording begins;
- stop/finalize creates a durable artifact before transcription starts;
- status exposes recording id, path or stable id, duration, bytes, phase, and
  last error;
- backend size limits are handled before upload;
- original audio is retained until transcript confirmation and retention policy;
- retry works after daemon restart, suspend, network failure, backend failure,
  or power loss;
- history links back to the retained recording artifact;
- failure notifications tell the user the audio is preserved and how to
  recover it.

A related older bead, `primary-oil`, points at prior Whisrs feature gaps:
try `gpt-4o-mini-transcribe`, expand STT vocabulary, add user-editable prompt
and vocabulary overlays, add `keep_recordings = true` with retention, and add
history copy/search commands. The report it referenced,
`reports/system-specialist/52-whisrs-feedback-and-improvements.md`, is not
present in the current report directory; the bead description was still enough
to recover the relevant prior thread.

## CriomOS Wiring Today

CriomOS-home owns the daily dictation surface:

- `CriomOS-home/flake.nix:88` consumes `github:LiGoldragon/whisrs?ref=criomos`
  as non-flake source. The comment says this branch carries the CriomOS safety,
  recovery, status-bar, and recall changes.
- `CriomOS-home/packages/whisrs/default.nix:12` builds Whisrs with
  `--no-default-features --features tray,overlay`. That means the local Whisper
  feature is not in the deployed package. The configured daily backend is
  OpenAI REST, not a local model.
- `CriomOS-home/modules/home/profiles/min/dictation.nix:19` builds the daemon
  wrapper. It reads `gopass openai/api-key`, exports
  `WHISRS_OPENAI_API_KEY`, creates `~/.local/share/whisrs/history.jsonl`, sets
  `RUST_LOG`, and execs `whisrsd`.
- `dictation.nix:63` writes `~/.config/whisrs/config.toml`: backend `openai`,
  model `gpt-4o-transcribe`, `status_bar = true`, `tray = true`, and
  workspace vocabulary/prompt hints.
- `dictation.nix:87` defines `whisrs.service` as a user service under
  `graphical-session.target`, with restart on failure.
- `dictation.nix:122` defines `whisrs-spool-retry`, a network-online one-shot
  that runs `whisrs spool retry --all --auto`.
- `dictation.nix:147` binds Niri keys: `Mod+V` -> `toggle-copy`,
  `Mod+Shift+V` -> direct keyboard `toggle`, `Mod+Alt+V` -> `whisrs-recall`,
  and `Mod+Ctrl+V` -> `cancel`.
- `CriomOS-home/modules/home/profiles/min/sfwbar.nix:44` adds the
  `plugin:whisrs-level` Noctalia widget and pins the Whisrs tray item.
- `CriomOS-home/modules/home/profiles/min/noctalia-plugins/whisrs-level/BarWidget.qml:51`
  subscribes to `$XDG_RUNTIME_DIR/whisrs/level.sock` and shows state plus a
  microphone-level bar.

CriomOS owns the system privilege needed for direct key injection:

- `CriomOS/modules/nixos/users.nix:34` adds edge users to the `uinput` group
  and declares the group.
- `CriomOS/modules/nixos/metal/default.nix:300` loads the `uinput` kernel
  module on min edge machines.
- `CriomOS/modules/nixos/metal/default.nix:474` sets udev rules for
  `/dev/uinput` group access.

This split is sound. The durable-first redesign belongs in Whisrs and
CriomOS-home. CriomOS should only need to keep providing `/dev/uinput` access.

## Whisrs Operation Today

The Whisrs fork has no local `AGENTS.md`, `ARCHITECTURE.md`, or `skills.md`.
CriomOS-home's `skills.md` is the effective local contract for this fork in the
workspace.

Current state and IPC are coarse:

- `whisrs/src/lib.rs:25` defines a JSON-over-Unix-socket command enum:
  `Toggle`, `ToggleCopy`, `Cancel`, `Status`, `Log`, `SpoolList`,
  `SpoolRetry`, and `SpoolDrop`.
- `whisrs/src/lib.rs:114` defines only three daemon states:
  `Idle`, `Recording`, and `Transcribing`.
- `whisrs/src/state.rs:41` confirms the transition graph:
  Idle -> Recording -> Transcribing -> Idle, with cancel only from Recording.

The daemon stores active recording state in process memory:

- `whisrs/src/daemon/main.rs:51` defines `DaemonState` with an
  `audio_capture` handle, source window id, streaming task, start instant, and
  output mode. There is no recording id, durable path, byte count, finalized
  artifact, retry attempt, or persistent phase.
- `whisrs/src/audio/capture.rs:64` starts a `cpal` capture thread that pushes
  `Vec<i16>` chunks through an unbounded channel.
- `AudioCaptureHandle::stop_and_collect` at `capture.rs:103` stops the thread,
  drains remaining chunks, and returns one `Vec<i16>`. That vector is the only
  complete recording in the normal path.

Batch dictation is memory-first:

- `whisrs/src/daemon/main.rs:923` handles stop by transitioning to
  `Transcribing`, taking the capture handle out of daemon state, dropping the
  mutex, and calling `process_recording_batch`.
- `process_recording_batch` at `daemon/main.rs:1263` collects all samples,
  gates silence, encodes an in-memory WAV, and calls the backend with that
  byte buffer.
- Only when `.transcribe(...)` returns an error does it call
  `spool::save_recovery_audio(&samples)` at `daemon/main.rs:1321`.
- Successful transcripts are copied and then written to history; the history
  entry contains timestamp, text, backend, language, and duration only
  (`whisrs/src/history.rs:14`). It has no recording artifact id.

Recovery spool is useful but late:

- `whisrs/src/audio/recovery.rs:31` writes spool files under
  `$XDG_STATE_HOME/whisrs/spool/`, which is the right storage class.
- `save_recovery_audio` at `recovery.rs:183` tries Opus-in-Ogg first, falls
  back to WAV, and returns a path.
- The encoder bug from the bead is visible at `recovery.rs:162`: code borrows
  `child.stdin.as_mut()`, writes all samples, exits the borrow scope, then
  calls `wait_with_output()` while the child still owns stdin. `ffmpeg` never
  sees EOF. The narrow fix is to take/drop stdin before waiting, but that does
  not change the architectural problem.
- `spool_entry_from_path` in `daemon/main.rs:1551` reads duration using
  `hound::WavReader::open(path)`. Opus `.ogg` spool entries therefore list
  duration as `None`.
- `handle_spool_retry` at `daemon/main.rs:1588` reads the file bytes, calls the
  current backend, saves history, copies text to clipboard, and deletes the
  spool file on success. There is no attempt ledger or original-retention
  policy beyond "file remains until success/drop".

Streaming paths are also not durable-first:

- `run_streaming_pipeline` at `daemon/main.rs:1052` streams microphone chunks to
  a backend and types deltas while recording. It saves only the transcript if
  text was produced.
- OpenAI Realtime and Deepgram Streaming override `supports_streaming()` to
  `true`; Groq has a chunking implementation but reports `false`; local Whisper
  reports `true` behind a feature that the CriomOS package does not enable.
- If a streaming backend fails, Whisrs can show an error and may have already
  typed partial text, but it has no local original audio to retry.

## External Research

### Best conceptual match: Voicebox captures

Voicebox's capture model is the cleanest external reference. Its docs describe
a capture as paired audio and transcript state. Dictation, manual recording,
and file upload all land in the same Captures tab; rows show transcript,
duration, timestamp, source, a play button, and actions. A detail view exposes
the waveform, transcript editor, settings snapshot, retranscription, and
refinement actions. See:

- https://docs.voicebox.sh/overview/captures
- https://docs.voicebox.sh/overview/dictation

This is the object model `primary-ipjx` is asking for. The important part is
not the GUI; it is that dictation produces a durable capture first, and all
later actions operate on that capture.

### Closed products show the expected failure UX

Wispr Flow's help docs explicitly document history retry and recovery of failed
or still-processing transcriptions. They also state that, during a connection
loss, audio already being recorded may be preserved because it is saved in
parallel during recording. The product is closed and does not run on Linux, but
the UX is exactly the confidence target: when transcription is slow or fails,
the user is told the audio is saved and recoverable from history.

Source: https://docs.wisprflow.ai/articles/4984532368-fix-taking-longer-than-usual-and-transcription-errors

Willow Voice has the same broad shape in support docs: failed dictation can
often be recovered from local transcript history by retrying the unfinished
dictation. Again, closed product and not a Linux solution, but it confirms that
users of high-value dictation tools expect local recovery of failed recordings.

Source: https://help.willowvoice.com/en/articles/12279120-dictation-quality-or-transcription-failure-problem

### OpenWhispr: optional local retention, not the invariant

OpenWhispr is open source and advertises macOS, Windows, and Linux. Its privacy
policy says transcription history lives in a local SQLite database, local STT
is the default processing mode, and optional audio retention can save recorded
audio locally for a configured period. That is close, but the crucial word is
optional. A disabled retention policy cannot satisfy "audio is never only in
process memory once recording begins."

Sources:

- https://openwhispr.com/
- https://openwhispr.com/privacy

### Voxtype: strongest Linux-native neighbor, but a different axis

Voxtype is Linux-native, local by default, and supports Hyprland, Niri, Sway,
River, GNOME, and KDE. It offers multiple local engines, a floating waveform
OSD, push-to-talk/toggle, and meeting mode with continuous chunked processing
and export formats. That makes it worth inspecting for local model packaging,
Niri integration, long-form chunking, and output fallback strategy.

It is not a direct durable-first answer for Whisrs. The public README emphasizes
local/offline transcription and meeting-mode export, not a per-dictation durable
recording object that all dictation attempts must create before transcription.

Source: https://github.com/peteonrails/voxtype

### Same-tool evidence

I did not find public evidence that upstream Whisrs is being used in a
durable-first way. Its public README describes the same basic daemon/CLI
architecture, Linux compositor support, seven backends, tray/overlay, and
history. The CriomOS fork already has more explicit recovery tooling than the
public README foregrounds, but the local source shows that recovery is still
post-failure spool, not first-class recording state.

## Backend Research

The backend swap alone is not the fix.

OpenAI's speech-to-text docs currently say file uploads are limited to 25 MB
and recommend chunking or compressed formats for longer inputs. The same docs
point live microphone/media-stream use to Realtime transcription. OpenAI's
Realtime transcription docs describe streaming transcript deltas as audio
arrives and distinguish `gpt-realtime-whisper` for live deltas from
request-response file transcription models.

Sources:

- https://developers.openai.com/api/docs/guides/speech-to-text
- https://developers.openai.com/api/docs/guides/realtime-transcription

Deepgram offers both pre-recorded-file and live-streaming transcription paths.
The live-streaming docs show a persistent connection that receives audio media
and emits results in real time. This can reduce failure from large file uploads
and supports push-style progress, but it still does not preserve the user's
original audio unless Whisrs writes that audio locally first.

Sources:

- https://developers.deepgram.com/docs/pre-recorded-audio
- https://developers.deepgram.com/docs/live-streaming-audio

Local models avoid paid API limits and network loss, but local inference still
needs the same durable artifact discipline. "Local" only changes who consumes
the recording; it does not prove the recording was preserved before inference.

## Recommended Shape

### 1. Durable recording session is the core type

Introduce a first-class recording object under state storage, for example:

```text
$XDG_STATE_HOME/whisrs/recordings/<recording-id>/
  original.pcm-or-wav-or-flac
  recording-state.<typed-metadata>
  attempts/
    <attempt-id>.<typed-metadata>
  transcript.<typed-metadata>
```

The exact metadata format should follow the repo's eventual contract
discipline. The important fields are stable id, created time, source window id,
sample rate, channels, bytes written, samples written, duration, phase, backend
attempts, last error, retained/deleted state, and transcript links.

### 2. Capture appends to durable state as audio arrives

Replace `stop_and_collect() -> Vec<i16>` as the source of truth. The capture
thread should write chunks to a durable writer immediately and publish progress
events. In-memory buffers are allowed as transient staging for one chunk, never
as the only complete recording.

Durability target:

- create recording directory at start;
- write to `original.tmp` or a journaled raw PCM file as chunks arrive;
- periodically flush enough metadata that `status` can report bytes, duration,
  and stable id;
- on stop, close/finalize the audio file, atomically mark the recording
  finalized, then enqueue transcription.

### 3. Transcription is an attempt over a recording

Each transcription attempt reads the finalized artifact or a derived encoding.
The attempt records backend, model, configuration snapshot, derived file path,
started/completed timestamps, result text, and error.

Backend policy:

- If OpenAI REST is selected and the derived file would exceed 25 MB, do not
  upload and then fail. Choose a configured alternate path first: Opus/FLAC
  derivation, sentence-aware chunking, local backend, Deepgram streaming over
  file chunks, or explicit "needs user action".
- Derived compressed/chunk files do not replace the original unless retention
  policy explicitly says so.
- A successful attempt appends transcript history with `recording_id` and
  `attempt_id`, not just text/backend/language/duration.

### 4. Streaming becomes an accelerator, not ownership

For OpenAI Realtime, Deepgram Streaming, local Whisper windows, or any future
streaming backend, the capture path should still write the original chunk
before forwarding it to the backend. The event order should be:

1. chunk accepted from microphone;
2. chunk appended to durable recording state;
3. progress event emitted;
4. chunk sent to streaming transcription, if enabled.

If the stream fails, the durable recording remains and a retry attempt can run
from the artifact. If streaming succeeds, the same capture still backs history,
retranscription, and audit.

### 5. Status and UI need recording state, not just daemon state

The current `State` enum is too thin. The `whisrs status`, tray tooltip,
Noctalia level socket, and failure notification need at least:

- phase: idle, recording, finalizing, queued, transcribing, failed, done;
- recording id;
- duration;
- bytes written;
- retained path or stable locator;
- active backend/model;
- last error;
- recovery command.

The important notification text on failure is not just "Transcription failed".
It should say that the recording is preserved and name the retry command or
stable id.

### 6. Recovery commands become first-class recording commands

The existing `whisrs spool list/retry/drop` surface is the right instinct, but
it should become recording-centered:

- `whisrs recordings list`
- `whisrs recordings show <id>`
- `whisrs recordings retry <id> [--backend ...]`
- `whisrs recordings export <id> [--format ...]`
- `whisrs recordings drop <id>`
- `whisrs recordings retain <id>`

The old spool path can migrate into recordings as a compatibility import, then
retire.

### 7. Tests must prove the path, not only the result

The witnesses from `primary-ipjx` are the right list. Add Nix-exposed tests for:

- long recording writes a durable artifact before transcription starts;
- oversized OpenAI REST input is caught before upload;
- daemon crash during recording leaves recoverable partial/finalizable state;
- daemon crash during transcription leaves a retryable recording and attempt
  record;
- encoder subprocess receives EOF and terminates;
- retry after daemon restart uses the original artifact;
- successful transcript history links to recording id;
- retention keeps original until explicit policy deletes it.

## Immediate Work Order

1. Fix `primary-kyhs`: close/drop `ffmpeg` stdin before
   `wait_with_output()` in `audio/recovery.rs`. This removes the live hang from
   the incident, but should be treated as the narrow bug fix, not the
   architecture.
2. Add the durable recording session type and writer. This is the real P1.
3. Change batch stop to finalize and enqueue, then make transcription consume
   the artifact.
4. Expand status/notifications around recording id and recovery state.
5. Migrate spool/history into recording-linked state.
6. Revisit backend policy after storage is correct. Backend switching before
   durable capture will only move the failure mode.

