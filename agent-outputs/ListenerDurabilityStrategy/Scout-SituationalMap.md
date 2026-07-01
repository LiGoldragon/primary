# Listener Durability Strategy Scout Map

## Task And Scope

Research question: determine whether Listener can maintain a continuous crash-resilient audio artifact on Linux/NixOS/PipeWire without rotating tiny segment files, and identify practical implementation choices for the first durable slice.

Prompt context treated as task context: Listener currently captures the default source with `parecord --device=@DEFAULT_SOURCE@` and streams raw `s16le` bytes to one file; the production writer currently flushes/syncs only after EOF, so it is clean-stop durable but not continuously crash-resilient.

No Listener source files were found by the scoped local filename search `rg --files -g 'AGENTS.md' -g 'ARCHITECTURE.md' -g 'README*' -g '*listener*' -g '*Listener*' . | sed -n '1,200p'`, which returned only workspace `AGENTS.md`/`ARCHITECTURE.md` surfaces. I did not inspect private scopes or run write tests.

## Commands And Sources Consulted

Local commands:

- `sed -n '1,220p' /home/li/primary/AGENTS.md`
- `sed -n '1,220p' /home/li/primary/.agents/skills/library/SKILL.md`
- `pwd`
- `rg --files -g 'AGENTS.md' -g 'ARCHITECTURE.md' -g 'README*' -g '*listener*' -g '*Listener*' . | sed -n '1,200p'`
- `command -v parecord; command -v parec; command -v pw-record; command -v ffmpeg; command -v gst-launch-1.0; command -v ffprobe; command -v sox; command -v flac; command -v rustc; command -v cargo`
- `uname -a`
- `pw-record --version`
- `parecord --version`
- `ffmpeg -hide_banner -muxers | rg -i 'caf|matroska|ogg|flac|wav|webm|segment'`
- `ffmpeg -hide_banner -h muxer=caf`
- `ffmpeg -hide_banner -h muxer=matroska`
- `ffmpeg -hide_banner -h muxer=wav`
- `ffmpeg -hide_banner -h muxer=flac`
- `pw-record --help | sed -n '1,220p'`
- `parecord --help | sed -n '1,220p'`
- `pw-record --list-containers | sed -n '1,240p'`
- `parecord --list-file-formats | sed -n '1,240p'`
- `findmnt -T /home/li/primary -o TARGET,SOURCE,FSTYPE,OPTIONS`
- `nix --version`
- `ffmpeg -hide_banner -version | sed -n '1,24p'`
- `sqlite3 --version`
- `command -v sqlite3; command -v dmsetup; command -v mkfs.ext4; command -v mkfs.xfs; command -v mkfs.btrfs; command -v qemu-system-x86_64`

Primary/reference sources are listed at the end with URL and locator notes.

## Short Answer

Yes, one-file continuous crash-resilient recording is feasible now on Linux. The mechanism is not a new magic container by itself; it is an append-only write protocol with bounded commit units and explicit durability calls, usually `fdatasync(2)`, `fsync(2)`, `O_DSYNC`, or per-call `pwritev2(..., RWF_DSYNC)`.

For a standard immediately readable growing PCM file, CAF is the best fit found: Apple CAF explicitly permits the Audio Data chunk size to be `-1` when unknown, requires that chunk to be last, and readers determine the data size from EOF. That pairs well with periodic `fdatasync`. Matroska live mode and FLAC streams are also real one-file streaming options, but they add muxer/codec complexity. WAV/RF64/BW64 is good for final interchange and large files, but crash-time validity still depends on header repair or nonstandard infinite-size headers.

For Listener's first durable slice, the strongest plan is a single append-only Listener recording log containing raw PCM records with checksums and periodic `fdatasync`, plus a recovery/export path to CAF/WAV/FLAC. If immediate playback by standard tools is more important than internal checksums, use CAF with an unknown-size PCM `data` chunk and periodic `fdatasync`; add a recovery step that truncates any tail to a complete sample frame.

## Observed Facts

### Local Environment

- Current workspace: `/home/li/primary`, from `pwd`.
- Host kernel: `Linux ouranos 7.0.1 #1-NixOS SMP PREEMPT_DYNAMIC Wed Apr 22 11:32:23 UTC 2026 x86_64 GNU/Linux`, from `uname -a`.
- Workspace filesystem for `/home/li/primary`: ext4 mounted at `/` from `/dev/nvme0n1p2` with options `rw,relatime,stripe=128`, from `findmnt -T /home/li/primary -o TARGET,SOURCE,FSTYPE,OPTIONS`.
- Nix version: `nix (Nix) 2.34.6`.
- Present audio/storage tools in PATH:
  - `/run/current-system/sw/bin/parecord`
  - `/run/current-system/sw/bin/parec`
  - `/run/current-system/sw/bin/pw-record`
  - `/home/li/.nix-profile/bin/ffmpeg`
  - `/home/li/.nix-profile/bin/ffprobe`
  - `/home/li/.nix-profile/bin/sox`
  - `/home/li/.nix-profile/bin/flac`
  - `/home/li/.nix-profile/bin/rustc`
  - `/home/li/.nix-profile/bin/cargo`
- `pw-record --version`: compiled and linked with libpipewire `1.6.3`.
- `parecord --version`: `pacat 17.0`, compiled and linked with libpulse `17.0.0`.
- `ffmpeg -version`: FFmpeg `8.0.1`, built with libpulse and many muxers/codecs enabled.
- `sox --version`: SoX `14.4.2`.
- `flac --version`: FLAC `1.5.0`.
- `rustc --version && cargo --version`: Rust `1.96.0` and Cargo `1.96.0`.
- `sqlite3` was not present in PATH. `dmsetup`, `mkfs.ext4`, `mkfs.xfs`, and `mkfs.btrfs` were present. `qemu-system-x86_64` was not present in PATH.
- `pw-record --list-containers` and `parecord --list-file-formats` both listed `caf`, `flac`, `oga`, `raw`, `rf64`, `w64`, `wav`, and other libsndfile-backed formats.
- FFmpeg muxers observed include `caf`, `flac`, `matroska`, `ogg`, `opus`, `wav`, `w64`, `webm`, `segment`, and `stream_segment,ssegment`.

### Linux Durability Semantics

- `write(2)` success does not mean data has reached durable media. The Linux man page says a successful `write()` does not guarantee disk commit and delayed errors may surface on later `write`, `fsync`, or `close`; the reliable completion boundary is a sync operation after writes.
- `fsync(2)` flushes file data and associated metadata to the underlying device and blocks until the device reports completion. It also notes that newly created directory entries need a separate `fsync` on the parent directory.
- `fdatasync(2)` is like `fsync(2)` but may skip metadata that is not needed for subsequent data retrieval. File size metadata does matter for appends, so appending followed by `fdatasync` is still the right primitive for growing files.
- `O_DSYNC` makes each `write` complete as though followed by `fdatasync`; `O_SYNC` makes each `write` complete as though followed by `fsync`. `O_DSYNC` avoids flushing metadata such as mtime when not needed for data retrieval.
- `pwritev2(2)` supports `RWF_DSYNC` and `RWF_SYNC` as per-write equivalents of `O_DSYNC`/`O_SYNC` for the range written by that call. Linux also has `RWF_APPEND`.
- `sync_file_range(2)` is not a crash-durability primitive. Its Linux man page warns that it does not write metadata, does not flush volatile disk write caches, and gives no crash guarantee except for strict overwrites of already-instantiated blocks. On copy-on-write filesystems such as Btrfs, overwrite assumptions are explicitly unsafe.
- `io_uring` can submit writes and fsyncs, including `IORING_FSYNC_DATASYNC`, but it does not change the required durability semantics. It is a submission/completion mechanism, not a substitute for `fdatasync`/`fsync`.
- Linux now exposes `RWF_ATOMIC`/atomic write fields through `pwritev2` and `statx` on newer kernels/filesystems, and ext4 documentation says atomic writes require Direct I/O and supporting storage. This is a useful emerging capability for torn-write protection, but it is not a general solution for Listener's default first slice because it is hardware/filesystem dependent and still needs sync semantics for durable ordering.

### Filesystem Caveats

- ext4 has data modes. Kernel docs and `ext4(5)` describe:
  - `data=ordered` as the default, journaling metadata while writing associated data blocks before metadata commit.
  - `data=writeback` as faster but allowing old data to appear after crash recovery.
  - `data=journal` as full data and metadata journaling, slower and incompatible with direct I/O.
- XFS is a high-performance metadata-journaling filesystem. It can support large files and has dynamic end-of-file preallocation behavior, but ordinary application crash durability still depends on explicit sync calls.
- Btrfs documentation emphasizes barrier/default flush behavior and notes `flushoncommit` can make committed state include prior dirtied data, but ordinary buffered writes may outlast transaction commits when that option is off. Applications still should use explicit sync for durability claims.
- `fallocate(2)` can preallocate disk space and guarantees subsequent writes into the range will not fail due to lack of disk space. `FALLOC_FL_KEEP_SIZE` can preallocate beyond EOF for append workloads. This is a performance/ENOSPC mitigation, not a replacement for `fdatasync`.

### Audio Container Options

- Raw PCM is the simplest artifact but is not self-describing and has no record boundary, duration metadata, or checksum. If using raw PCM, Listener must persist format metadata elsewhere or in a custom header. Recovery can only truncate to a frame-size multiple unless Listener adds its own record framing/checksums.
- CAF is a strong standard growing-file candidate:
  - CAF files have a file header, required Audio Description chunk, and exactly one Audio Data chunk.
  - CAF chunk sizes are 64-bit.
  - The Audio Data chunk may use size `-1` when the data size is unknown, and in that case the Audio Data chunk must be last so EOF defines the audio-data size.
  - CAF Linear PCM can describe 16-bit signed integer little-endian audio with arbitrary sample rate and channel count.
  - FFmpeg on this host has a CAF muxer; `pw-record`/`parecord` list CAF through libsndfile.
  - CAF does not by itself provide per-audio-block checksums for PCM. For crash recovery, truncate to a complete sample frame, and rely on `fdatasync` for committed data.
- WAV/RF64/BW64:
  - RIFF/WAV chunks use 32-bit chunk sizes. Standard WAV files therefore normally need header/data sizes finalized or repaired.
  - ITU-R BS.2088 BW64 adds a mandatory `ds64` chunk for 64-bit sizes and describes switching from RIFF/WAV to BW64 during recording by reserving a `JUNK` chunk that later becomes `ds64`.
  - FFmpeg has WAV options `-rf64 auto|always|never`. `pw-record`/`parecord` list `rf64` and `w64`.
  - Hound has an "infinite or unknown size" WAV header helper that writes `0xFFFFFFFF` chunk sizes, but its docs call such files potentially non-standard. This is practical for pipes and recovery tooling but weaker than CAF as a standard crash-time artifact.
- Matroska/WebM:
  - RFC 9559 specifies live Matroska streams: a live stream usually has no known end, and the Segment size bits are set to all ones.
  - Matroska has top-level Info, Tracks, Cluster, optional Cues, and CRC-32 elements. FFmpeg's Matroska muxer has `-live`, `-cluster_size_limit`, `-cluster_time_limit`, and `-write_crc32` options.
  - Matroska can hold PCM, but a correct muxer/recovery path is more complex than CAF or a custom PCM record log.
- Ogg:
  - RFC 3533 defines Ogg as providing framing, error protection, and seeking structure; Ogg pages have sequence numbers and CRC checksums.
  - Ogg is good for partial-stream recovery when using a suitable codec mapping, but raw PCM in Ogg is not the most common Linux archival path. Ogg/Opus is lossy; Ogg/FLAC is lossless but adds codec/mapping complexity.
- FLAC:
  - RFC 9639 defines FLAC streams with mandatory Streaminfo before audio frames. Total sample count may be zero to mean unknown, and the MD5 may also be unknown.
  - Xiph's Ogg FLAC mapping explicitly permits redundant fields such as total samples and MD5 to be zero for single-pass encoding.
  - FLAC gives lossless compression and frame structure but adds encoder CPU, encoder state, and more recovery/test surface than raw PCM/CAF.
- SQLite:
  - SQLite can provide crash-safe transactions. In WAL mode, SQLite keeps a `-wal` file as persistent state while the database is open; separating it from the database can lose committed transactions or corrupt the database.
  - `PRAGMA synchronous=FULL` in WAL mode is ACID; `synchronous=NORMAL` in WAL mode is consistent but can lose recent transactions after power loss.
  - SQLite incremental BLOB I/O exists, but BLOB size cannot be changed through the blob API. A row-per-chunk design is more plausible than one growing BLOB. It is a storage database design, not an audio container, and it creates sidecar WAL/SHM files during operation.

## Interpretation

The key distinction is "recoverable growing file" versus "durably committed prefix." A container such as CAF can make a growing file structurally valid before a clean finalizer runs. It does not make data durable; Linux still requires a sync primitive. Conversely, `fdatasync` can make raw bytes durable, but raw bytes alone are not self-describing or self-validating.

There is no currently practical Linux feature that removes the need for periodic sync if the claim is "survives OS crash or power loss up to a recent bounded point." `sync_file_range` is explicitly unsafe for this. `io_uring` can help keep the capture thread responsive, but the durability cost still exists. `RWF_ATOMIC` is the nearest "newer, less commonly used" feature, but it is only an optional torn-write protection feature for aligned Direct I/O on supporting filesystems/storage, not a general continuous audio recording solution.

## Recommended First Durable Slice

Recommended authoritative artifact: one append-only Listener recording log file.

Suggested shape:

- File header written once:
  - magic/version
  - sample format (`s16le`)
  - sample rate
  - channel count/channel map
  - bytes per frame
  - capture start wall-clock and monotonic timestamps
  - optional source identifier
- Repeated records:
  - record magic/version
  - sequence number
  - byte offset or cumulative sample frame count
  - monotonic timestamp for first sample
  - payload length
  - payload CRC32C/CRC32 or BLAKE3 digest
  - PCM payload
  - optional trailer/commit magic repeating sequence and checksum
- Writer behavior:
  - capture from `parecord --raw`/`parec` initially, or later replace capture with the Rust `pipewire` crate or PulseAudio simple binding.
  - collect bounded chunks, e.g. 250 ms to 2 s of PCM, depending on acceptable data-loss window and sync overhead.
  - write each record with `write_all`/`writev` loops; handle short writes.
  - flush any userspace buffer, then call `fdatasync` after every record or after a configured group of records.
  - only report a record as durable after `fdatasync` succeeds.
  - treat `EIO`, `ENOSPC`, `EDQUOT`, and sync failure as fatal durability failures requiring visible error state.
  - on file creation, write and sync the header, and `fsync` the parent directory so the directory entry is durable.
  - optionally preallocate ahead with `fallocate(FALLOC_FL_KEEP_SIZE)` in large windows to reduce allocation latency and ENOSPC risk; do not treat preallocation as a sync.
- Recovery behavior:
  - scan records from the header.
  - stop at first incomplete header, invalid length, non-monotonic sequence, missing trailer, or checksum mismatch.
  - truncate to the last valid record boundary and `fsync`/`fdatasync` the recovered file.
  - export a conventional CAF/WAV/RF64/FLAC after recovery or clean stop.

This is the most testable design because the recovery predicate is entirely local: the file must contain a valid prefix of records. It does not rely on a third-party muxer finalizer or a guessed WAV header repair step.

Pragmatic alternative for a standard one-file artifact: CAF unknown-size PCM.

Suggested shape:

- Write a CAF header with Audio Description for `lpcm`, `s16le`, known rate/channels, then a `data` chunk with `mChunkSize = -1` and edit count `0`.
- Append raw PCM bytes.
- `fdatasync` every configured interval.
- On recovery, compute the audio-data byte count from EOF, truncate to the nearest full sample frame, and optionally rewrite/finalize `mChunkSize` for archival cleanliness.
- This is simple and immediately compatible with FFmpeg/libsndfile-style tools, but it lacks internal per-record checksums. Use it if "playable while open/recovered" is more important than custom corruption detection.

Avoid as the primary first slice:

- Plain WAV/RF64 requiring clean finalization as the durability claim. It can be repaired from EOF, but the live artifact is less self-consistent than CAF.
- `sync_file_range` as the only durability call.
- SQLite as the audio artifact unless Listener already wants a database. It can be durable with `synchronous=FULL`, but active WAL state means more than one file and a different recovery model.
- Tiny segment rotation unless independent segment-level publication/upload is a hard requirement.

## Tradeoffs Versus Segment Files

One growing file:

- Pros: no directory churn; no rotation gap; easier mental model for "the recording"; CAF/custom-log can be valid or recoverable while active; avoids thousands of tiny files.
- Pros for custom log: exact recovery prefix, checksums, sequence numbers, easy crash tests.
- Cons: needs a recovery scanner/exporter; a very large artifact is less convenient for upload/copy; corruption or operator mistakes affect one large object; a custom log is not directly playable without export.

Segment files:

- Pros: each closed/synced/renamed segment is a natural commit unit; standard muxers work well; upload/index/retry are easier; damage is bounded to one segment.
- Cons: more file creation and directory syncs; possible boundaries/gaps; many files to manage; does not satisfy the psyche's preference unless there is a clear product reason.

Conclusion: segmenting remains a legitimate engineering answer when independent publication units matter, but it is not required for crash-resilient continuous capture. A single append-only record log or CAF unknown-size file is credible.

## Exact APIs, Crates, And Tools Likely Usable From Rust On NixOS

Core Linux/Rust APIs:

- `std::fs::File::sync_data()` and `sync_all()` for `fdatasync`/`fsync`-style operations in stable Rust.
- `std::os::unix::fs::OpenOptionsExt::custom_flags()` for `O_CLOEXEC`, `O_DSYNC`, `O_APPEND`, or related Linux open flags.
- `rustix::fs::fdatasync` and `rustix::fs::fsync`.
- `rustix::io::pwritev2` with `rustix::io::ReadWriteFlags::DSYNC`, `SYNC`, and `APPEND` where Linux-specific per-write flags are desired.
- `nix::fcntl::fallocate` or `rustix::fs::fallocate` for preallocation. Use `FALLOC_FL_KEEP_SIZE` if preallocating beyond EOF for append.
- `libc` remains the direct escape hatch for Linux flags not yet wrapped by a safe crate, such as probing `statx` atomic-write fields or experimental flags.

Capture options:

- Current process pipeline remains viable: `parecord --device=@DEFAULT_SOURCE@ --raw --format=s16le ...` or `parec` into Listener's writer.
- `pw-record` can capture through PipeWire and lists raw/container controls, but it does not solve Listener's durability problem unless Listener controls syncing of the output file.
- Rust `pipewire` crate exists as safe PipeWire bindings, but current docs.rs build for version `0.10.0` failed; its freedesktop-hosted docs should be checked before implementation.
- `libpulse-simple-binding` provides a simple synchronous PulseAudio record/playback API, useful if Listener keeps the PulseAudio compatibility path.

Container/codec/crate options:

- Implement CAF writing directly; the required PCM header is small and the Apple spec is straightforward. Existing Rust CAF crates found are decoder/demuxer oriented, not a mature writer surface.
- `hound` can write WAV and has an infinite/unknown-size WAV header helper, but the docs warn such files may be non-standard and ordinary `WavWriter` requires finalization.
- `ogg` crate provides Ogg packet reader/writer surfaces if using Ogg framing.
- `flacenc` and `flac-codec` are possible Rust FLAC implementation paths; FFmpeg/libFLAC command-line tooling is also available locally.
- `mkv-element`/`media-format-matroska` exist for Matroska element/mux work, but maturity for Listener's exact writer needs was not verified.
- `rusqlite` supports incremental BLOB I/O with the `blob` feature, but BLOB size changes require SQL and SQLite active WAL mode uses additional files.
- `crc32fast` or `blake3` are practical checksum/digest crates for record validation.

Local NixOS tools observed:

- `parecord`, `parec`, `pw-record`, `ffmpeg`, `ffprobe`, `sox`, `flac`, `dmsetup`, `mkfs.ext4`, `mkfs.xfs`, `mkfs.btrfs`, `rustc`, and `cargo`.
- `sqlite3` and `qemu-system-x86_64` were not observed in PATH.

## Test Strategy

Do not use clean EOF, SIGTERM finalization, or muxer close as the proof. Those only test clean-stop durability.

Minimum process-crash tests:

- Build a deterministic synthetic PCM generator with sequence-marked sample patterns.
- Run the Listener writer in a child process against a disposable output path.
- Kill it with `SIGKILL` at random points, including during record header write, payload write, checksum/trailer write, and just before/after `fdatasync`.
- Recovery must produce a valid prefix of records and never accept a partial/torn/corrupt record.
- Repeat with forced short writes and injected `EINTR`/`EIO`/`ENOSPC` at the writer abstraction boundary.
- For CAF mode, verify recovered file opens with `ffprobe`/`sox` after truncating to frame boundary; verify sample prefix against generated PCM.

OS/power-crash tests:

- Use a disposable block device or VM image, not the developer workstation's main filesystem.
- Format and test ext4, XFS, and Btrfs separately.
- Prefer device-mapper `dm-log-writes` for systematic replay: the kernel doc says it logs write operations and flush ordering specifically to verify filesystem metadata/data integrity. Add user marks after each acknowledged `fdatasync`, replay to each mark, mount, and run the recovery checker.
- Use `dm-flakey` for error/drop/corrupt-write behavior tests; the kernel doc says it can periodically return errors, drop writes, or corrupt write bios.
- If VM testing is used later, hard-power the VM off or crash the kernel; do not ask Listener to stop. Host-side durable acks must be recorded only after guest `fdatasync` returns. QEMU was not found in PATH locally, so this was not verified on this host.

Properties to assert:

- Recovered audio is always a prefix of the generated stream.
- All records whose `fdatasync` success was externally acknowledged before the crash are present after recovery, modulo explicit storage/hardware failure tests.
- No record after the first invalid/torn record is accepted.
- Parent directory fsync after file creation makes the recording path discoverable after crash.
- Recovery is idempotent: running it twice changes nothing after the first successful recovery.

## Unknowns And Caveats

- The actual Listener target filesystem and mount options may differ from `/home/li/primary`. The active workspace is ext4 with `rw,relatime,stripe=128`, but Listener recordings may land elsewhere.
- Device write-cache honesty, barriers, firmware behavior, RAID/controller settings, and battery-backed caches are outside the file API. Linux `fsync`/`fdatasync` rely on the kernel/device stack correctly flushing caches.
- Atomic write support (`RWF_ATOMIC`) was not probed on the local recording path. It needs `statx` probing, Direct I/O constraints, filesystem support, and hardware support.
- CAF player compatibility on Linux is likely good through FFmpeg/libsndfile because local tools list CAF, but specific downstream apps should be tested.
- Rust Matroska writer maturity was not verified beyond crate/documentation discovery.
- No actual crash tests were run; this Scout role was research/read-only except for this assigned report file.

## Source Notes

- Linux `fsync(2)` man page, lines 40-64 and 74-83: `fsync`/`fdatasync` semantics, directory fsync need, writeback error reporting. https://man7.org/linux/man-pages/man2/fsync.2.html
- Linux `open(2)` man page, lines 200-207 and 373-380, plus synchronized I/O notes lines 627-667: `O_DSYNC`, `O_SYNC`, and metadata distinctions. https://man7.org/linux/man-pages/man2/open.2.html
- Linux `write(2)` man page, lines 103-110 and 137-143: delayed writeback errors and no disk-commit guarantee from successful `write`. https://man7.org/linux/man-pages/man2/write.2.html
- Linux `readv(2)`/`pwritev2(2)` man page, lines 91-155: `RWF_DSYNC`, `RWF_SYNC`, `RWF_APPEND`, `RWF_ATOMIC` semantics. https://man7.org/linux/man-pages/man2/readv.2.html
- Linux `sync_file_range(2)` man page, lines 55-68: explicit warning against crash-durability use. https://man7.org/linux/man-pages/man2/sync_file_range.2.html
- Linux `fallocate(2)` man page, lines 37-54: preallocation and `FALLOC_FL_KEEP_SIZE` for append workloads. https://man7.org/linux/man-pages/man2/fallocate.2.html
- Linux `statx(2)` man page, lines 331-355 and 391-392: atomic write fields and support caveat. https://man7.org/linux/man-pages/man2/statx.2.html
- ext4 kernel docs, Data Mode lines 389-401: writeback/ordered/journal modes. https://docs.kernel.org/admin-guide/ext4.html
- `ext4(5)` man page, lines 387-426: journaling modes, default `ordered`, barriers, commit interval. https://man7.org/linux/man-pages/man5/ext4.5.html
- ext4 atomic writes kernel docs, lines 57-62: atomic writes require Direct I/O and supporting device. https://docs.kernel.org/6.17/filesystems/ext4/atomic_writes.html
- XFS kernel docs, lines 66-78: XFS characteristics and EOF preallocation option. https://docs.kernel.org/admin-guide/xfs.html
- Btrfs docs, lines 115-120 and 212-219: barriers and `flushoncommit` behavior. https://btrfs.readthedocs.io/en/latest/Administration.html
- PipeWire `pw-cat`/`pw-record` docs: capture and container controls. https://docs.pipewire.org/page_man_pw-cat_1.html
- PulseAudio `parecord` man page: raw/encoded capture and format options. https://manpages.debian.org/testing/pulseaudio-utils/parecord.1.en.html
- Apple CAF spec, lines 27-72, 78-82, 106-149, 249-260, 479-525: headers, required chunks, Linear PCM fields, unknown-size Audio Data chunk. https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/CAF_spec/CAF_spec.html
- Microsoft RIFF summary, lines 57-62: 4-byte file/chunk sizes and chunk structure. https://learn.microsoft.com/en-us/windows/win32/xaudio2/resource-interchange-file-format--riff-
- ITU-R BS.2088-2 PDF, pages/lines around P2-P8: BW64 scope, 64-bit `ds64`, and on-the-fly RIFF-to-BW64 transition. https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.2088-2-202511-I%21%21PDF-E.pdf
- Library of Congress BWF v2, lines 76-78: RF64/MBWF large-file note. https://www.loc.gov/preservation/digital/formats/fdd/fdd000357.shtml
- RFC 9559 Matroska, live stream passage found in search result and structure/order lines 3427-3480: live unknown-size segment, required top-level elements, optional cues. https://datatracker.ietf.org/doc/rfc9559/
- RFC 3533 Ogg, lines 82-93 and 495-502: framing, packet boundaries, CRC. https://datatracker.ietf.org/doc/html/rfc3533
- RFC 9639 FLAC, lines 715-718 and 797-805: Streaminfo before frames, unknown total sample count and MD5. https://datatracker.ietf.org/doc/rfc9639/
- Xiph Ogg FLAC mapping, line 34: unknown redundant fields for single-pass encoding. https://xiph.org/flac/ogg_mapping.html
- SQLite Atomic Commit, lines 119-124 and 414-420: crash/power atomicity and caveats. https://www.sqlite.org/atomiccommit.html
- SQLite WAL, lines 138-143 and 154-156: WAL file as persistent state, checkpoint behavior. https://sqlite.org/wal.html
- SQLite PRAGMA synchronous, lines 821-850: `FULL`, `NORMAL`, WAL durability matrix. https://sqlite.org/pragma.html
- SQLite incremental BLOB API, lines 56-61: read/write BLOB and fixed-size caveat. https://sqlite.org/c3ref/blob_open.html
- Kernel `dm-log-writes`, lines 66-80 and 134-150: write/flush logging and fsync test example. https://docs.kernel.org/admin-guide/device-mapper/log-writes.html
- Kernel `dm-flakey`, lines 66-71 and 99-150: unreliable device simulation, drop/corrupt/error writes. https://docs.kernel.org/admin-guide/device-mapper/dm-flakey.html
- Rust `std::fs::File` docs: `sync_all`/`sync_data`. https://doc.rust-lang.org/beta/std/fs/struct.File.html
- Rust `OpenOptionsExt` docs: `custom_flags`. https://doc.rust-lang.org/std/os/unix/fs/trait.OpenOptionsExt.html
- `rustix` docs for `fdatasync`, `pwritev2`, and `ReadWriteFlags::DSYNC`. https://docs.rs/rustix/latest/rustix/fs/fn.fdatasync.html, https://docs.rs/rustix/latest/rustix/io/fn.pwritev2.html, https://docs.rs/rustix/latest/rustix/io/struct.ReadWriteFlags.html
- `nix` docs for `fallocate`. https://docs.rs/nix/latest/nix/fcntl/fn.fallocate.html
- `io-uring` docs for write flags and fsync prep; Linux semantics still come from man pages. https://docs.rs/io-uring/latest/io_uring/opcode/struct.Write.html, https://man7.org/linux/man-pages/man3/io_uring_prep_fsync.3.html
- `hound` docs for WAV finalization and infinite header warning. https://docs.rs/hound/latest/hound/struct.WavWriter.html, https://docs.rs/hound/latest/hound/struct.WavSpec.html
- `ogg` crate docs for packet writer/reader existence. https://docs.rs/ogg
- `flacenc` docs for Rust FLAC encoding. https://docs.rs/flacenc
- `rusqlite` blob docs. https://docs.rs/rusqlite/latest/rusqlite/blob/index.html
- Rust `pipewire` crate docs.rs page and freedesktop docs pointer. https://docs.rs/crate/pipewire/latest
- `libpulse-simple-binding` docs for simple synchronous capture/playback API. https://docs.rs/libpulse-simple-binding/latest/libpulse_simple_binding/
- `crc32fast` and `blake3` crate docs for checksum/digest implementation feasibility. https://docs.rs/crc32fast, https://docs.rs/blake3
