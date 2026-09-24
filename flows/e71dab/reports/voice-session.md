# Voice session evidence

This report carries evidence read and returned by a subflow for the parent
flow. It records what the supplied witnesses establish and keeps unobserved
behavior open.

## Observed

- The active Codex harness version in the read-only current process environment
  was `0.158.0-alpha.9`.
- The recorded session contains discrete speech-to-text (STT) transcript turns
  entering the flow.

## Unknown

- The Android ChatGPT app version was unavailable.
- The supplied record does not witness playback from the flow back to Android.
- It does not establish speaker isolation, end-to-end latency, or barge-in
  behavior.
- It does not establish whether partial transcripts occur outside the supplied
  record.

The STT observation therefore supports discrete transcript entry only. It does
not, by itself, establish a complete voice round trip or the absence of any of
the unknown behaviors above.

## Sources

- Returned witness from the subflow: read-only current process environment,
  active Codex harness version `0.158.0-alpha.9`.
- Returned witness from the subflow: recorded voice session containing discrete
  STT transcript turns entering the flow.
- Returned witness from the subflow: Android ChatGPT app version unavailable;
  playback, speaker isolation, latency, barge-in, and out-of-record partial
  transcript behavior were not witnessed.
