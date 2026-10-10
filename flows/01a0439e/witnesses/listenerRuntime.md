Method: probe `systemctl --user status listener.service --no-pager -l`; `journalctl --user --since '2026-08-27 15:20:00' --until '2026-08-27 15:52:00'`; `ps`; `stat`; `ffprobe`; metadata-only `jq` over the history store.

Observed on 2026-08-27:

- `listener-daemon` 0.14.0 (PID 3296598) has been active since 2026-08-24
  13:44:17 CEST. Current status socket event is `idle`, level `0.0`,
  `in_flight: 0`.
- The unit journal contains only the service start line; the bounded system
  and kernel journal search around the latest capture contains no Listener
  error, crash, OOM, or coredump.
- Niri's live bindings invoke Listener `Start.{}` on `Mod+C` and the
  `listener-stop-capture` helper on `Mod+V`. Journal scope starts witness a
  start at 15:21:48 and stop helper at 15:48:35.
- Capture session 530 has a canonical owner-only `capture-530.webm`, size
  5,171,870 bytes, valid Matroska/WebM Opus mono 48 kHz, duration 1606.808 s.
  Its owner-only terminal record and history record are present at 15:49:43;
  history has 374 records, with session 530 last. The session-530 text was
  measured only: 15,663 UTF-8 bytes, 98 lines, 3,442 space-delimited words;
  no text was emitted into this witness.
- No `.listenerlog` remains for session 530, consistent with terminal
  successful compaction. Noctalia logged a plain-text clipboard history event
  at 15:49:43.683, without transcript content.
- The deployed process environment points to the fixed OpenAI customization
  archive and `gpt-4o-transcribe`; no latency trace variable is set.

Code witness:

- `/git/github.com/LiGoldragon/listener/src/transcription.rs:507-526` obtains
  WebM duration, uses 600-second steps for longer recordings, submits each
  chunk as a separate OpenAI upload, and joins returned texts with one space.
- `/git/github.com/LiGoldragon/listener/src/runtime.rs:893-985` orders stop,
  compact, transcribe, history append, terminal completion, delivery, and
  status/notification effects.
- `/git/github.com/LiGoldragon/listener/src/history.rs:320-375` rewrites the
  bounded JSONL history atomically on append and read; reading history can
  therefore change its file mtime without creating a new transcript.

Focused signature audit (2026-08-27):

- In the session-530 history text, the supplied Java header occurs exactly
  twice, at decoded UTF-8 offsets 10,190 and 10,236. The supplied newline,
  eight-space, `//` prefix occurs exactly 94 times. The six bytes between the
  end of the first header and the start of the second are `\n\n    ` (two
  newlines and four spaces); there is no literal space at that boundary.
- The deployed request prompt is the fixed generic English transcription
  instruction in `/git/github.com/LiGoldragon/listener/src/transcription.rs:19-28`.
  The only deployed customization is the 21-term archive/`terms.txt` set
  referenced by the unit wrapper; neither that prompt nor the terms/archive
  contains the supplied Java header. Exact-string searches also found no
  header in the Listener source, deployed wrapper, daemon binary, local
  Listener state, or local Whisrs history. These searches did not inspect or
  reproduce the private transcript body.
- The response parser at `transcription.rs:697-738` extracts the JSON `text`
  field and trims only its outer whitespace. History serialization and
  `TranscriptText` construction preserve the incoming string; clipboard
  delivery writes its bytes unchanged. Recall selection clones the stored
  text, so those stages have no witnessed insertion mechanism.
- Session 530's 1606.808-second artifact invokes three 600-second request
  chunks. The deployed join operation inserts exactly one ASCII space between
  chunk response texts. The observed bytes between the two headers are not
  that delimiter, so the pair cannot straddle a chunk-join boundary. No local
  request/response trace identifies which single chunk contains the region.
