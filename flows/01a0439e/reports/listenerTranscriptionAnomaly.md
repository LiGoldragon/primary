# Listener transcription anomaly report

## Observations

1. The exact latest matching Claude input event is the queue enqueue at JSONL
   line 192, `2026-08-27T14:26:02.556Z`, whose complete 45-character text is
   `something weird happened to the transcription`. It was dequeued, an
   interrupt record was emitted, and the same text became human-origin queued
   input at line 196.
2. Listener history record 374 is capture session 530, completed at
   `2026-08-27T13:48:37.092Z` and transcribed at
   `2026-08-27T13:49:43.569Z`. Its text is 15,663 characters. The corresponding
   owner-only WebM remains at `capture-530.webm`.
3. Claude line 166 contains that Listener record exactly as its final 15,663
   characters. This is source-level evidence that the anomalous text existed
   before Claude rendered or interpreted it.
4. The stored Listener text includes two duplicate occurrences of
   `public static void main(String[] args) {` and 94 exact newline/indent/comment
   prefixes (newline + eight spaces + `//`) in the middle of the otherwise
   spoken-text body.
5. Claude line 199 is a later typed resubmission. Relative to line 166 it
   deletes only one 98-character block (the two headers and the first prefix)
   plus the other 93 prefixes. No new characters are present. The resulting
   text therefore removes the visible code/comment contamination without
   changing the remaining words.

6. Listener source shows that this 1,606.808-second capture is split into
   three requests beginning at 0, 600, and 1,200 seconds, with joined text
   stored without per-chunk timestamps or IDs. Consequently, offset 10,190
   cannot be proven to be a chunk boundary. A uniform-rate estimate places it
   near 1,045.4 seconds, inside the second chunk; metadata-only silence
   detection found a nearby pause around 1,045.849–1,046.923 seconds, but this
   is not a proven text/audio or topic mapping.
7. The exact Java header and comment-prefix artifacts were absent from the
   scoped Listener source, transcription fixture/vocabulary/dictation inputs,
   and deployed customization archive strings. No topic transition is
   recoverable from the available transcript structure.

## Strongest conclusion

The precise anomaly is a code/comment formatting contamination in Listener
capture 530's stored transcription: a duplicated Java method header and
comment-line prefixes were embedded in the transcript. Claude line 166
faithfully received that contaminated Listener record. A later resubmission
removed exactly those artifacts, which is recovery evidence, not evidence of a
new transcription result.

## Hypotheses

- The contamination was introduced in the transcription or delivery path
  before Claude line 166, because the private Listener history already carries
  it and line 166 is an exact suffix copy.
- The line-199 cleanup may have been a user edit, terminal/input normalization,
  or another harness action. The available records do not distinguish these.

These remain hypotheses. The record does not prove whether the Java text was
spoken, inserted by the speech-to-text provider, introduced while copying, or
introduced by another input layer.

## Unknowns and boundaries

- The audio was not listened to or independently transcribed, so the spoken
  ground truth is unknown.
- `promptSource: queued` identifies Claude queue handling, not the physical
  source of the 45-character report phrase.
- No listener journal/status entry links capture 530 to the queue event, and
  no causal actor for insertion or cleanup is identified.
- Whether any semantic words were lost relative to the audio cannot be proved;
  the comparison proves only that the later message removes the listed
  formatting artifacts and no other characters from the stored text.
- The proportional audio-time estimate is not a timestamped alignment; the
  actual onset time, chunk response containing it, and any topic/audio
  transition remain unknown.

## Privacy and safety

Only lengths, hashes, structural counts, the short report phrase, and the
non-private Java marker needed to establish the anomaly are retained here.
The long transcription, history body, and audio remain private and were not
copied into this report.

## Sources

- Witness: `flows/01a0439e/witnesses/listenerTranscriptEvent.md`.
- Claude transcript: `/home/li/.claude/projects/-home-li-primary/04db2fd2-8e23-4751-8d8a-0efb6676a4f3.jsonl`, physical lines 166, 192–199.
- Listener history: `/home/li/.local/share/listener/history.jsonl`, physical line 374, session 530.
- Listener capture metadata: `/home/li/.local/state/listener/captures/capture-530.webm` and `capture-530.terminal`.
- Chunking/prompt source: `/git/github.com/LiGoldragon/listener/src/transcription.rs:22,507-526`.
- Scoped prompt/vocabulary inputs: `/git/github.com/LiGoldragon/listener/tests/fixtures/transcription_customization_terms.txt` and `/git/github.com/LiGoldragon/CriomOS-home-spirit-main-f53aacdd/modules/home/profiles/min/dictation.nix`.
- Flow: `01a0439e`.
