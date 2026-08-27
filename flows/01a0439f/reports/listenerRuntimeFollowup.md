# Listener runtime focused boundary follow-up

The known session-530 signature is not attributable to the local prompt,
customization, response parsing, history, recall, clipboard, or chunk-join
stages on the evidence available.

Witnessed exclusions:

- The deployed prompt is fixed generic transcription text. The deployed
  customization has only the 21 configured vocabulary terms. Exact-string
  searches found no occurrence of the supplied Java header in those inputs,
  the Listener source, wrapper, daemon binary, local Listener state, or local
  Whisrs history.
- The parser takes only the upstream JSON `text` field and trims outer
  whitespace. History persistence and `TranscriptText` wrapping preserve the
  incoming string. Clipboard delivery writes the transcript bytes unchanged;
  recall clones stored text. The parent witness also records that the session
  530 history text is byte-identical to the later Claude record, ruling out
  Claude rendering/interpretation as the insertion point.

Chunk-boundary result:

- The 1606.808-second recording is split into three requests. The joiner adds
  one literal space between responses. At the known offsets 10,190 and
  10,236, the bytes between the two headers are `\n\n    `, not a join space.
  Therefore the two-header region is within one upstream response (or was
  spoken in the audio), not created at the local chunk join. Which of the
  three requests owns it is unknown because no per-request response trace is
  retained.

Earliest remaining insertion boundary:

- If the Java material was not spoken, the earliest remaining candidate is
  upstream transcription output (the API/model response), before the local
  parser. This is a bounded hypothesis, not a witnessed model hallucination;
  audio semantics and the actual per-chunk response are unavailable. The
  alternative remains that the material was present in the source audio.

No implementation, service, history, capture, configuration, or deployment
file was changed.

## Sources

- `flows/01a0439f/witnesses/listenerRuntime.md`.
- Parent event witness/report: `flows/01a0439e/witnesses/listenerTranscriptEvent.md`
  and `flows/01a0439e/reports/listenerTranscriptionAnomaly.md`.
- Listener source: `/git/github.com/LiGoldragon/listener/src/transcription.rs`,
  `/git/github.com/LiGoldragon/listener/src/history.rs`,
  `/git/github.com/LiGoldragon/listener/src/delivery.rs`, and
  `/git/github.com/LiGoldragon/listener/src/recall.rs`.
- Deployed unit wrapper: `/home/li/.config/systemd/user/listener.service`.
