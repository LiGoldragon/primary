# Listener transcription event witness

Method: probe `nix run /git/github.com/LiGoldragon/transcript -- search 'listener|transcription' --recent 80 --cap 180`, targeted `jq` fields from the named Claude JSONL records, a metadata-only comparison of the two long message bodies, `jq` over the private Listener history JSONL, `stat`, `ffprobe`, metadata-only `ffmpeg silencedetect`, a read of Listener's chunking source, a scoped exact-marker search over prompt/vocabulary/input sources, and a decode of the 24-byte Listener terminal record. No full transcript, history body, or audio was printed or listened to; no retranscription was performed.

## Exact event

The latest matching live input in the Claude project transcripts is session
`04db2fd2-8e23-4751-8d8a-0efb6676a4f3`,
`/home/li/.claude/projects/-home-li-primary/04db2fd2-8e23-4751-8d8a-0efb6676a4f3.jsonl`:

- Physical line 192 is a `queue-operation` `enqueue` at
  `2026-08-27T14:26:02.556Z`. Its complete content is exactly
  `something weird happened to the transcription` (45 characters).
- Physical line 193 is the corresponding `dequeue` at
  `2026-08-27T14:26:03.858Z`.
- Physical line 194 records `[Request interrupted by user]` at
  `2026-08-27T14:26:03.849Z`, with an `interruptedMessageId`.
- Physical line 196 is the resulting human-origin user record at
  `2026-08-27T14:26:03.869Z`, with `promptSource: queued`; its complete text
  is the same 45-character phrase.

The queue record is the direct harness evidence. The transcript does not label
the physical input device, so `promptSource: queued` proves queue delivery but
does not independently prove whether the phrase came from Listener or a
keyboard/paste action.

## Listener record mapped to the long message

The owner-private Listener history
`/home/li/.local/share/listener/history.jsonl`, physical record line 374,
has `session: 530`, `unix_millis: 1787838583569`
(`2026-08-27T13:49:43.569Z`), text length 15,663, and SHA-256
`3fccae9c1e119079a36c77f0b600e6513c5a68a75bf67f39709050450338805d`.

The matching durable capture is
`/home/li/.local/state/listener/captures/capture-530.webm`, owner-only mode
600, 5,171,870 bytes, Opus 48 kHz mono, duration 1,606.808 seconds. Its
owner-only terminal record decodes as `LSTNTERM`, version 1, state code 2
(`Completed`), completion time `2026-08-27T13:48:37.092Z`.

Claude physical line 166 (same session, `2026-08-27T14:25:25.296Z`,
`promptSource: typed`) is 15,950 characters. Its final 15,663 characters
are byte-for-byte identical to the Listener history record above. The first
287 characters are a separate preamble and are not reproduced here.

## Observed anomaly

The Listener history text contains two occurrences of the exact Java header
`public static void main(String[] args) {` at offsets 10,190 and 10,236,
followed by 94 occurrences of the line prefix consisting of a newline, eight
spaces, and `//`. The surrounding
spoken-text sequence is otherwise retained in the history record.

Claude physical line 199 is a later typed resubmission at
`2026-08-27T14:26:52.307Z`, 14,829 characters. It has the same 287-character
preamble. Its remainder is exactly the Listener-history text with only these
deletions:

- the 98-character block containing both Java headers and the first comment
  prefix;
- the remaining 93 exact newline/eight-space/`//` prefixes (11 characters
  each).

Thus 1,121 characters are removed (`98 + 93*11`), with no added characters;
the later remainder is a strict subsequence of the stored Listener text. This
establishes a formatting/content contamination in the stored transcription
before Claude received line 166, followed by a later cleanup/resubmission. It
does not establish who or what performed the cleanup.

## Negative evidence

`listener.service` was active when checked. `journalctl --user -u
listener.service` for 2026-08-27 14:20–14:35 UTC had no entries. The service
logs and status surface therefore provide no causal record for this event.

## Chunk boundary, audio transition, and source-marker follow-up

Listener source `/git/github.com/LiGoldragon/listener/src/transcription.rs:507-526`
uses 600-second chunks for this 1,606.808-second capture, at starts 0, 600,
and 1,200 seconds, then joins returned text with spaces. The stored history
has no chunk IDs, segment timestamps, or separator markers, so text offset
10,190 cannot be established as a chunk boundary. A uniform character-to-time
calculation places it at approximately 1,045.4 seconds, inside chunk 2, not at
600 or 1,200; this is only a heuristic because speech/text rates vary.

Metadata-only silence detection found a pause at approximately
1,045.849–1,046.923 seconds, near that heuristic estimate, but this does not
prove the offset maps to that pause or to a topic transition. Topic alignment
is unknown without per-segment timestamps or retranscription (which was not
performed).

The exact Java header and the newline/eight-space/`//` artifact prefix were
absent from the scoped Listener source, transcription fixtures, vocabulary and
dictation inputs, and deployed customization archive strings. They were found
only in the private stored history/Claude input (and this evidence artifact).
