---
description: Open measurements and design decisions for Android paralinguistic transcription.
dependencies: [knowledge-paralinguistic-transcription]
---

Measure Wispr, Gemini-backed alternatives and a custom IME on the same target
devices, languages, microphones, utterance scripts and network conditions.
Record word error rate, filler/false-start retention, pause-boundary fidelity,
emphasis/tone annotation agreement, speaking-rate error, partial/final timing,
end-to-end latency distribution, failure/reconnect behavior and battery/data
use. No winner should be declared without these matched trials.

Resolve which output is wanted: literal textual tags that downstream machines
can read, a separate annotation/display/export result, or both. Define the
annotation vocabulary and whether users can review each tag before
`InputConnection.commitText`; do not infer emotional intent as ground truth.

Resolve the provider route and model: direct Gemini API, OpenRouter, another
provider, local ASR, or a hybrid. Establish exact model, API feature support,
price, retention/training terms, abuse/safety logging, backend responsibility,
key/token lifecycle and whether audio leaves the device. Gemini's published
transcribe estimates are not a complete keyboard cost, and a paid route is not
automatically zero retention.

Resolve Android lifecycle and eligibility on target OEM/API levels: IME audio
capture, microphone foreground-service rules, background start behavior,
sensitive/password fields, interruptions, reconnects and offline behavior.

Resolve licensing and base fork only after inspecting the current source and
license of candidate projects such as WhisperToInput, HeliMic, Deskdrop and
Dictus. Measure engineering dimensions explicitly (surface area, integration
complexity, model size, runtime memory, battery, maintenance and test burden);
do not invent effort-day estimates.
