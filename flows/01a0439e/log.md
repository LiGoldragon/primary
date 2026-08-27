# Flow 01a0439e

Investigation of the living's report that something really weird happened to the last listener transcription.

Settled: Listener session 530 completed successfully after a 1,606.808-second capture. Its durable history text already contained the anomaly: two duplicate Java `main` headers followed by 94 inserted comment-line prefixes. Claude received that stored text exactly; its rendering did not create the artifacts.

Settled: the local 600-second chunk joiner, generic prompt, active customization, response parser, history, recall, clipboard, and Claude delivery paths have no witnessed insertion mechanism for this pattern. The anomaly lies within an upstream transcription response unless the Java/comment text was spoken. The exact cause is not knowable from retained metadata because per-chunk responses were not recorded and the audio was not independently checked.

No implementation change was authorized or made. Evidence and analysis are in `witnesses/listenerTranscriptEvent.md`, `reports/listenerTranscriptionAnomaly.md`, and subflow `01a0439f`'s listener runtime/context reports.

Remembered: 04db2fd2, f426777b, 01a0193f, 019fe121, 012fbf07, 13cfc23f, c6b71b4c — depth 1. The most relevant prior facts were the requirement never to lose a transcript, earlier technical-name recognition errors, and the immediately prior long listener monologue.
