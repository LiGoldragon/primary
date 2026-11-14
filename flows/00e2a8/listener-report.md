# Listener investigation, 13 November 2026 (evening, CST)

Read-only. Nothing was changed, restarted, deleted or sent. No key was printed; the OpenAI credential is read by the daemon from gopass `openai/api-key` (src/transcription.rs:468, :479, :592). Wispr Flow transcript text and audio were not opened: only table schema, row counts, timestamps and column lengths were read, from a scratch copy that has since been deleted.

Times are CST (UTC-6). "Observed" means seen in a command or file. "Inferred" means my reading.

## 1. Transcription model

Observed:

- Source constant: `/git/github.com/LiGoldragon/listener/src/transcription.rs:20` is `const OPENAI_TRANSCRIPTION_MODEL: &str = "gpt-4o-transcribe";`. It is the only model value: lines 655, 664 and 690 pass the constant to the request configuration, and line 547 sends it as the multipart field `model`.
- Running build: `systemctl --user status listener.service` shows PID 3202 running `/nix/store/g5ymb7yylryrp05sbn9ginvkq2ii0rsc-listener-0.14.0/bin/listener-daemon`, started Nov 11 18:13:40. `grep -a -o 'gpt-4o-transcribe' .../bin/.listener-daemon-wrapped` finds the string once. The strings `gpt-4o-mini-transcribe`, `whisper-1` and `gpt-transcribe` are absent from the binary. The Cargo.toml version is 0.14.0, repository HEAD `9b963f9` (2026-11-04).
- No configuration overrides it. The wrapper `/nix/store/2hkyi8l1n95x4q5kp85mz8dmiry6miwd-listener-daemon` sets only XDG_STATE_HOME, LISTENER_CAPTURE_PROGRAM, LISTENER_CLIPBOARD_PROGRAM and LISTENER_TRANSCRIPTION_CUSTOMIZATION_ARCHIVE. The archive supplies the prompt only (transcription.rs:655-660). `~/.config/listener/environment` does not exist; only `environment.example` does, and it holds only commented overrides for the capture and clipboard programs. The daemon's process environment (read from /proc/3202/environ, LISTENER/XDG/HOME names only) has no model variable. The model is hardwired, not configurable.
- A newer model exists. OpenAI's API changelog (fetched at https://developers.openai.com/api/docs/changelog):
  - Jul 28, 2026: `gpt-transcribe` (file transcription and final transcripts of committed Realtime turns) and `gpt-live-transcribe` (low-latency streaming) released.
  - Aug 26, 2026: deprecation announced for `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe` and `gpt-4o-transcribe-diarize`. They shut down on **Feb 26, 2027**. The recommended replacement is "gpt-live-transcribe or gpt-transcribe". The deprecations page (https://developers.openai.com/api/docs/deprecations) lists the same dates.
  - Also May 7, 2026: `gpt-realtime-whisper`, a streaming model.
  - Third-party reports give about $0.0045 per minute for gpt-transcribe and a large error-rate reduction. I did not verify these against OpenAI's pricing page. The OpenAI announcement page itself returned 403 to the fetch tool, so the changelog and deprecations pages (read through a summarizing fetch) are the primary evidence.

Consequence: Listener's one model is scheduled to stop working on 26 February 2027. The fix is one constant, plus checking that `gpt-transcribe` accepts the same `/v1/audio/transcriptions` fields (language and prompt).

Sources: https://developers.openai.com/api/docs/changelog , https://developers.openai.com/api/docs/deprecations , https://slator.com/openai-two-new-models-transcription/ , https://9to5mac.com/2026/05/07/openai-has-new-voice-models-that-reason-translate-and-transcribe-as-you-speak/

## 2. Why the history stopped on 23 October

Premise check, observed: the history file has not stopped being written because of a fault. It has no entry after 23 Oct because no successful Listener dictation has completed since, and no capture file newer than 1 Sep exists. I found no evidence of a break at 23 October.

Files (observed):

- History: `/home/li/.local/share/listener/history.jsonl`, 56 entries, 108424 bytes, mtime 2026-11-13 21:34:57. Entry times (from `unix_millis`) run from 2026-08-19 to the last one at **2026-10-23 23:05:37**, session 1. The previous two are 2026-10-23 14:00:17 (session 9049) and 14:00:34 (session 9050). Before them, the last was 2026-09-13 16:57:56 (session 9037).
- The mtime is later than the last entry because `TranscriptHistoryStore::append` and `read_recent` both compact and atomically rewrite the file (src/history.rs:329-355, comment at :326 and :361). The niri journal shows `app-niri-listener-recall-3587331.scope` started at 21:34:57 today, the Mod+Alt+V recall picker. So the mtime is a read, not an append.
- Captures: `/home/li/.local/state/listener/captures/`, 12 files. The newest is `capture-9030.webm` and `.listenerlog`, mtime 2026-09-01 11:30:43. The rest date from 17 Jul to 28 Aug. The directory mtime is Nov 10 07:16 (a deletion; I did not find which). No capture exists from October or November, and a broad search of /tmp, /var/tmp, /run/user/1001, ~/.local/state and ~/.cache for webm, opus, wav, ogg and listenerlog newer than 13 Nov found none.
- Code path: the history is appended only at the end of a successful stop. `src/runtime.rs:299` and `:964` call `record_history`, which calls `TranscriptHistoryStore::append` (:477-484, :1021-1027), after `transcribe` returns text. A cancelled capture never reaches it (comment at :437-440). A completed capture is then marked terminal and its artifacts are reclaimed (git commits bd2fb55 and 9c45852). A failed transcription keeps the capture and marks it failed (:280, :293, :950). So a successful dictation leaves a history line and no capture file; a failed one leaves a capture file and no line; neither exists after 23 Oct.

Key presses (observed; `journalctl --user -g 'Started app-niri-listener'`; the user journal begins 2026-09-26):

| Time | Scope started (key) | Reading |
|---|---|---|
| Oct 3 11:04:29 | start, then cancel 11:06:52 | cancelled |
| Oct 7 14:05:48 | start, then cancel 14:06:35 | cancelled |
| Oct 9 14:58:52 | start, then cancel 14:58:53 | cancelled |
| Oct 15 18:28:19 and 19:49:21 | start, then cancel two seconds later each | cancelled |
| **Oct 23 14:00:10-14:00:32** | start, start, stop (14:00:15), start, stop (14:00:32) | two completed dictations; history lines at 14:00:17 and 14:00:34 |
| Nov 4 12:00:31 | stop only | no start scope in the journal |
| Nov 5 12:47:19 | stop only | no start scope in the journal |
| Nov 5 13:06:03 | start, then cancel 13:06:06 | cancelled |
| Nov 13 21:32:27 | cancel only | daemon was Idle (`listener 'Status.{}'` answers `StatusReported.Idle`) |

So the last successful Listener dictation is 23 Oct 14:00. After it, Listener was started once (Nov 5, cancelled after three seconds). Nothing is wrong in the service: `listener.service` journal shows only restarts (Sep 26, Oct 30 08:37, Nov 2, six on Nov 10, Nov 11) and no errors. The socket `/run/user/1001/listener.sock` exists and the daemon answers.

The 23:05:37 entry (session 1) is not a key-press dictation. Observed: the daemon never restarted between session 9050 (14:00) and 23:05 (journal shows no restart until Oct 30), yet the session number is 1; no `app-niri-listener` scope exists near 23:05; and a codex tool error at 23:05:08 references a `/tmp/listener-...` test directory. Inferred: an agent test run wrote this line into the real history file. The entry is 116 bytes.

What changed around 23 October (observed): CriomOS-home history on 19-22 Oct is all Flow and Message deployments; no commit in that window touches the listener module or niri bindings. The last Listener-related home commits are in July (e7a7fee2, 2026-07-18). The Listener repo's last two commits are 4 Nov (9da0426, 9b963f9). The one deployment event for the daemon is the 30 Oct 08:37 restart. None of these precedes 23 Oct.

What changed in habit (observed): Mod+X was bound to Wispr Flow's `toggle-hands-free` in commit 6f71a8b4 (2026-09-04) and is bound today (`~/.config/niri/config.kdl:117`, `modules/home/profiles/min/niri.nix:459`). Listener keeps Mod+C start, Mod+V complete, Mod+Ctrl+C cancel and Mod+Alt+V recall. Wispr Flow's `launcher.log` says "Launcher Start" on 30 Aug. Listener history thins after 30 Aug (18 entries on 30 Aug alone, 8 entries from 9 Sep to 23 Oct). Inferred: dictation moved to Wispr Flow in early September, and the 23 Oct 14:00 pair were the last Listener dictations. Unknown: why the October Listener starts were each cancelled within seconds.

Pending retention: the 90-day retention (history.rs:27) has not yet cut the August entries; the oldest is 86 days old today. The next compaction after about 17 Nov (90 days from 19 Aug) will start deleting the oldest lines.

## 3. Tonight's Wispr Flow dictation (Mod+X)

It survives, as text and audio, in several places. Not opened: content.

Primary store (observed): `/home/li/Library/Application Support/Wispr Flow/flow.sqlite`, 1166692352 bytes, mtime 21:46:12, plus `flow.sqlite-wal` (77826832 bytes, 21:46:52) and `flow.sqlite-shm` (163840 bytes). The recent rows are still in the WAL, which is not checkpointed. Table `History` has 116 rows, all from today; the earliest is 07:53 CST. Columns include `asrText`, `formattedText`, `pastedText`, `audio` and `opusChunks`.

Evening rows (timestamp 18:00 CST and later): **58 rows, from 18:25:54 to 21:46:50 CST**, 5403 words, about 2685 seconds of speech. For all 58 of them `asrText`, `formattedText`, `audio` and `opusChunks` are all non-null. Audio is stored in the row (`audio` 85887224 bytes and `opusChunks` 30771796 bytes in total for the evening; for the whole day 179151856 and 64194001). Status: 113 `formatted`, 2 `raw_transcript` and 1 `error` across the day. Seven rows have `needsUploading = 1`, so not all have reached Wispr's server. The log at 21:46:52 says "Batch contains 7 transcripts ... skipping upload to batch".

The most recent rows are 21:46:50 (4 words), 21:46:06 (24), 21:45:35 (46), 21:42:40 (337 words, 132 s, 4241964 audio bytes), 21:35:12 (667 words, 287 s, 9191212 audio bytes). The longest of the evening is 287 s.

Backups: `/home/li/Library/Application Support/Wispr Flow/backups/backup-2026-11-13T18-00-00.731Z.sqlite`, 1166692352 bytes, mtime 12:00 today. It predates the evening, so it holds none of tonight. Wispr's daily backup runs at 12:00 CST; the next, 14 Nov 12:00, would contain tonight if the rows are still in `flow.sqlite` then. Older rows are not in the live History table (only today's), so retention is short and tonight's rows could be pruned.

Other Wispr data (observed, metadata only):

- `/home/li/.cache/wispr-flow/launcher.log`, 80817417 bytes, written continuously (21:46:57). It is a launcher and app log, with 291067 lines matching transcript, dictation or audio words; I did not read it. It records events such as "Batch contains 7 transcripts", not text; whether it holds transcript text is unchecked.
- `~/.config/Wispr Flow/logs/main.log` (1092710 bytes) was last written 2026-09-07; it holds nothing from tonight.
- `~/.config/Wispr Flow/Cache/Cache_Data/` has network cache entries from tonight (several small files, 3826-18541 bytes). Inferred: API response caches, not audio.
- `~/.config/Wispr Flow/config.json` (38030 bytes, 21:46:12): preferences and notification state; no transcript key names at the top level.

Listener: nothing from tonight. Its history has no entry after 23 Oct, no capture exists, and the daemon is Idle (section 2). The only Listener events tonight were a cancel at 21:32:27 and the recall picker at 21:34:57.

Clipboard history (observed): Noctalia keeps one, `/home/li/.local/state/noctalia/clipboard/`, with `index.enc` (42280 bytes, 21:46:52) and `entries/`, 100 encrypted `.enc` files named `<unix_millis>-<n>.enc`. Filename times run from 2026-11-13 09:08:39 to 21:46:52; **57 entries fall in 18:27:04 to 21:46:52 tonight**, sizes from 75 to about 3000 bytes. They are encrypted; I did not look for the key or decrypt them. Inferred: these are text copies (Wispr pastes through the clipboard), so each may be one dictation's pasted text, but that is not checked. The listing is capped at 100 entries, so older entries drop as new ones arrive.

No other clipboard manager (cliphist, clipse, CopyQ) exists on this machine.

Recommendation, not done because the task is read-only: copy `flow.sqlite`, `flow.sqlite-wal` and `flow.sqlite-shm` together (or run `sqlite3 .backup`) before Wispr prunes or the WAL checkpoints, and keep the 14 Nov 12:00 `backups/` file. Reading `asrText` or `formattedText` for rows timestamped 2026-11-14 00:25 to 03:46 UTC gives tonight's text; `audio` or `opusChunks` give the audio.
