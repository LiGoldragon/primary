# Listener Durability Implementation Evidence

## Task And Scope

Implemented the approved Listener durability fix in
`/git/github.com/LiGoldragon/listener`: active capture now writes one
append-only custom Listener recording log instead of a raw PCM file that is only
synced after EOF. No contract repositories were edited.

Consulted:

- `/home/li/primary/agent-outputs/ListenerDurabilityStrategy/Scout-SituationalMap.md`
- `/git/github.com/LiGoldragon/listener/AGENTS.md`
- `/git/github.com/LiGoldragon/listener/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/listener/README.md`
- touched source and tests under `src/` and `tests/`

## Changed Files

- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `README.md`
- `src/capture.rs`
- `src/error.rs`
- `src/lib.rs`
- `src/recording_log.rs`
- `src/runtime.rs`
- `src/transcription.rs`
- `tests/capture.rs`
- `tests/recording_log.rs`
- `tests/runtime.rs`

## Artifact Format And Commit Policy

Active capture artifact: one growing `capture-<session>.listenerlog` file.

Header:

- magic `LSTNLOG1`
- version `1`
- fixed header length `128`
- sample rate, channel count, bytes per frame
- sample format code and label for `s16le`
- input source code and label for `system-default`
- capture session
- capture start Unix seconds and nanoseconds
- record header length, record trailer length, and maximum payload bytes
- CRC32 over the header fields before the checksum

Record:

- magic `LSTNREC1`
- version `1`
- fixed record header length `48`
- sequence number
- cumulative frame offset
- cumulative PCM byte offset
- payload length
- payload CRC32
- record-header CRC32
- frame-aligned PCM payload
- commit trailer with magic `LSTNCMT1`, sequence, next byte offset, payload length, and payload CRC32

Production writer policy:

- creates or truncates the one log file;
- writes the header, flushes userspace state, calls `File::sync_data()`, then
  fsyncs the parent directory;
- reads the capture process stdout in bounded frame-aligned chunks;
- writes one record plus trailer per chunk;
- flushes and calls `File::sync_data()` after every payload record;
- does not use `sync_file_range`;
- keeps the active artifact as one growing file, with no segment rotation.

## Recovery And Transcription

Recovery scans from the header and accepts only a contiguous valid prefix. It
stops at the first incomplete header, invalid length, non-monotonic sequence or
offset, incomplete payload, checksum mismatch, missing trailer, or trailer
mismatch. If the file extends past the last valid boundary, recovery truncates
the log to that boundary and syncs the truncation. Running recovery again is
idempotent.

On stop, Listener recovers the `.listenerlog` and exports a raw `.raw.s16le`
view for the configured batch transcription command. The durable artifact
reported on the wire remains the custom Listener log path; the configured STT
backend receives the recovered raw PCM export path.

## Crash-Resilience Boundary

Now crash-resilient:

- directory entry for a newly created active recording log after the parent
  directory fsync succeeds;
- file header after its `sync_data` commit succeeds;
- every complete record whose write, trailer, flush, and `sync_data` commit
  completed before a crash;
- recovery to the last valid complete record boundary after a torn or corrupt
  tail.

Still dependent on filesystem and device honesty:

- kernel/device compliance with `fdatasync`/`fsync` ordering and volatile-cache
  flushes;
- storage firmware, controller, RAID, and mount behavior;
- real OS or power-loss behavior, which was not simulated in this pass.

## Checks Run

- `cargo fmt`: passed.
- `cargo test --test recording_log`: passed, 3 tests.
- `cargo test --test capture`: passed, 1 test.
- `cargo test --test runtime`: passed, 4 tests.
- `cargo test --test recording_log --test capture --test runtime`: passed, 8 tests.
- `cargo test`: passed, 9 integration tests plus empty unit/doc suites.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `nix flake check`: passed for the local compatible system; Nix reported that
  `aarch64-linux` was omitted as incompatible for this run.

## Commit And Push

Committed and pushed to `main`:

- commit `5ee86c8efc8cc1f8c4a6e6aa04c46f31f0fdf7d6`
- message `listener: add durable recording log`
- `main`, `main@git`, and `main@origin` all pointed at the commit after push

The Listener working copy was clean after push.

## Next Work

Real OS or power-crash validation remains future work. The next practical test
surface is a disposable filesystem or VM/device-mapper harness that kills power
or replays writes around acknowledged `sync_data` boundaries, then runs the
Listener recovery scanner and prefix assertions.
