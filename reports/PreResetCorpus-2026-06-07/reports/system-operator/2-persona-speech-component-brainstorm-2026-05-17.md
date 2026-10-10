# Persona Speech Component Brainstorm

Role: second-system-assistant
Date: 2026-05-17
Bead context: `primary-ipjx` - durable-first speech-to-text rethink

## Executive Finding

The current durable-first speech-to-text problem should not be solved by
teaching Whisrs to look more like Persona. If this becomes a Persona-native
capability, it should be a triad: a daemon that owns state, a thin CLI that
accepts one NOTA request and prints one NOTA reply, and a `signal-*` contract
crate that owns the typed request/reply/event vocabulary. Raw audio is the
named data-plane carve-out: Signal carries control, identities, status,
subscriptions, and artifact references; large audio bytes move through durable
files and/or a separate raw socket.

Industry practice is mixed but not ambiguous. Cloud providers usually expose
speech-to-text and text-to-speech as separate API surfaces, each with its own
batch and realtime modes. Voice-agent frameworks usually model them as
separate replaceable pipeline stages: transcriber, agent, synthesizer. The
newer exception is speech-to-speech realtime sessions, where one model receives
audio and emits audio directly. That exception is useful for low-latency
conversation, but it is not a good storage model for our durable dictation
requirement because it hides too much of the artifact and retry surface inside
provider session semantics.

My current recommendation is:

1. Build the first replacement as `persona-transcription`, not `persona-stt`
   and not broad `persona-speech`. Its contract is
   `signal-persona-transcription`. It owns durable recording sessions,
   transcription attempts, transcript status, transcript subscriptions, and
   optional dispatch of completed text into Persona.
2. Keep text-to-speech as a separate future component,
   `persona-speech-synthesis` or `persona-utterance`, with contract
   `signal-persona-speech-synthesis` or `signal-persona-utterance`.
3. Introduce a broader `persona-speech` component only if the first real
   full-duplex use case needs a shared speech-session coordinator for barge-in,
   echo cancellation, ducking, and simultaneous listen/speak policy. If that
   happens, `persona-speech` should coordinate the two smaller engines rather
   than absorb both engines into one overlarge daemon.

The name `Persona STT` is useful shorthand in conversation, but it should not
be the repo or type name. Workspace naming discipline wants full English
words. If the component only turns speech into text, call it
`persona-transcription`. If it owns both listening and speaking as one local
voice boundary, call it `persona-speech`.

## What Persona Shape Requires

The relevant workspace pattern is the component triad:

```text
persona-transcription/
  src/lib.rs
  src/bin/persona-transcription-daemon.rs
  src/bin/transcription.rs

signal-persona-transcription/
  src/lib.rs
  tests/round_trip.rs
```

For every stateful component:

- the CLI is a thin text adapter with exactly one Signal peer, its own daemon;
- the daemon external surface is Signal frames, not JSON, env-var dispatch, or
  ad hoc sockets;
- NOTA appears at the CLI boundary and debug/audit projections, not as the
  inter-component wire;
- request variants declare their `SignalVerb` roots in the contract crate's
  `signal_channel!` declaration;
- daemon startup configuration is a typed configuration record decoded by
  `nota-config::ConfigurationSource::from_argv()?.decode()?`;
- if the component has high-bandwidth bytes, those bytes are a separate data
  plane. The control plane still follows the triad.

Audio squarely hits the data-plane carve-out. A `RecordingStart`,
`RecordingFinalize`, `TranscriptionAttempt`, `TranscriptSubscription`, or
`UtterancePlayback` record belongs in Signal. Raw PCM, Opus, FLAC, WAV, or
speaker output bytes do not belong in Signal frames.

The current Whisrs path violates the future Persona shape in three ways:

- it speaks JSON IPC rather than Signal;
- it keeps the complete recording in process memory until stop and only spools
  after failure;
- it has no typed artifact identity, attempt ledger, or subscription surface
  for Persona peers.

The durable-first fix from the previous report maps naturally into a Persona
triad: `RecordingSession` becomes daemon-owned state, persisted under an XDG
or engine-scoped state directory; the transcript is an attempt result over that
artifact; the CLI and peer components talk only through typed records.

## Current Industry Pattern

### Providers usually split STT and TTS

OpenAI's current audio docs name separate common tasks: speech-to-text,
text-to-speech, and speech-to-speech. They also distinguish request-based
audio APIs for bounded files/text from Realtime sessions for low-latency live
events. The request-based STT API is `/audio/transcriptions`; the request-based
TTS API is `/audio/speech`; Realtime handles live transcription and full
speech-to-speech sessions.

The important design lesson is not "copy OpenAI endpoints." It is that the API
surface differs by direction:

- STT consumes audio and emits text, transcript deltas, final segments,
  language hints, word timing, diarization, confidence/logprob data, and
  turn-boundary events.
- TTS consumes text or SSML plus voice/style controls and emits audio bytes,
  playback chunks, voice metadata, visemes or markers on some platforms, and
  generation-completion events.
- Speech-to-speech sessions collapse both directions for latency and natural
  conversation, but they are provider-session objects, not durable local
  recording/synthesis ledgers.

Deepgram has the same split under one company umbrella: STT offers streaming,
turn-based, and prerecorded paths; TTS has a separate WebSocket `/v1/speak`
surface with `Speak`, `Flush`, `Clear`, and `Close` message types.

Google Cloud exposes Cloud Speech-to-Text as recognition methods
(synchronous, asynchronous, and streaming recognition) and Cloud
Text-to-Speech as synthesis methods, including bidirectional streaming
synthesis where text chunks arrive while audio chunks are produced. These are
different APIs with different request/response types.

Azure Speech likewise keeps Speech-to-Text REST around fast transcription,
batch transcription, and custom speech, while Text-to-Speech has realtime
synthesis, long-audio batch synthesis, voices, SSML, visemes, and separate
pricing by characters.

### Voice-agent frameworks split the pipeline

LiveKit Agents explicitly supports both STT-LLM-TTS pipelines and realtime
speech models. It lists STT, TTS, realtime APIs, and other model classes as
provider plugins. Vocode's public model breaks a conversation into
Transcriber, Agent, Synthesizer, Input Device, and Output Device. This is the
common developer architecture: keep recognition and synthesis as separable
stages so providers, latency knobs, and failure handling can change
independently.

The industry-standard architecture for controllable voice agents is therefore
not one "speech" box; it is a pipeline of separately typed stages, with a
special-case shortcut when an end-to-end realtime model is desired.

### Local tooling is mixed

Local/offline tools are less consistent:

- Piper is text-to-speech only.
- Whisper-family tools are speech-to-text only.
- sherpa-onnx is a broad offline speech toolkit that includes ASR, TTS, VAD,
  diarization, and more under one project.

This does not override the Persona boundary rule. It says our backend adapter
layer should be open to both single-purpose engines and broad toolkits. A
`persona-transcription` daemon can call a local `sherpa-onnx` ASR backend while
a future synthesis daemon calls a `sherpa-onnx` or Piper TTS backend. Shared
backend implementation crates are fine; shared runtime state is what needs a
component-level reason.

## One Component: `persona-speech`

The strongest case for one component is if the bounded context is "local
speech modality" rather than "transcribe audio." That component would own two
long-lived state planes:

- listening: microphone capture, durable recordings, VAD, transcript attempts,
  transcript subscriptions;
- speaking: utterance queue, synthesis attempts, playback, voice catalog,
  interruption and cancellation.

It could also own the full-duplex policy that lives between them:

- barge-in: user starts speaking while Persona is speaking;
- echo cancellation: subtract Persona's output from microphone input;
- ducking: lower playback volume while recording confidence rises;
- half-duplex fallback: pause or cancel output when the microphone captures
  speech;
- shared audio device leases and sample-rate conversion;
- a single user-visible speech status surface.

This is attractive because "people talk over each other" is a real interaction
mode. If Persona speaks at the same time it listens, the coordination between
playback and capture is not accidental glue; it is domain state.

The problem is scope. `persona-speech` can easily become a grab bag:
dictation, voice-agent turn-taking, TTS voice management, audio device policy,
VAD, echo cancellation, cloud provider policy, local model management,
keyboard injection, message submission, notifications, and history. That is
too many nouns for one micro-component unless the architecture draws a hard
line: it owns local speech I/O and artifact state only; it does not own agent
reasoning, router policy, mind memory, terminal injection policy, or desktop
focus policy.

If `persona-speech` exists, I would shape it as a coordinator plus two actor
subtrees, not a single mixed state machine:

```text
SpeechRoot
  ListeningSupervisor
    MicrophoneCapture
    RecordingWriter
    VoiceActivityDetector
    TranscriptionAttemptRunner
    TranscriptPublisher
  SpeakingSupervisor
    UtteranceQueue
    SpeechSynthesisRunner
    PlaybackSink
    PlaybackPublisher
  DuplexCoordinator
    EchoReference
    BargeInPolicy
    DeviceLeaseTable
```

The Signal contract would probably need two root families inside
`signal-persona-speech`: a transcription relation and an utterance relation.
`signal-persona` already demonstrates that a contract crate can carry multiple
relations when they are one component's wire surface, but each relation needs
its own closed request/reply/event family.

## Two Components: transcription and synthesis

The strongest case for two components is that STT and TTS have different
natural ownership:

| Axis | Transcription | Speech synthesis |
|---|---|---|
| Input | Microphone/live audio or durable audio file | Text/SSML/voice request |
| Output | Text, segments, timing, confidence, speaker labels | Audio chunks/files, playback state, visemes/markers |
| Durability | Must preserve original user recording before transcription | May or may not retain generated audio |
| Failure | Backend refused audio, no speech, VAD error, oversized file | Voice unavailable, text too long, playback device failure |
| Privacy | User speech recording retention is sensitive | Generated speech is usually less sensitive, but voice cloning is sensitive |
| Cost metric | audio seconds/minutes, model, diarization | characters/tokens/audio seconds, voice |
| Realtime shape | input chunks -> transcript deltas/finals | text chunks -> audio chunks/playback |

The typed surfaces are different enough that separate contracts are cleaner:

```text
signal-persona-transcription
  RecordingStart / RecordingFinalization / RecordingCancellation
  RecordingStatusQuery / RecordingListQuery
  TranscriptionAttempt
  TranscriptSubscription
  RecordingRetentionChange

signal-persona-speech-synthesis
  UtteranceSubmission
  UtteranceCancellation
  UtteranceStatusQuery / UtteranceListQuery
  VoiceCatalogQuery
  PlaybackSubscription
  OutputRetentionChange
```

Separate daemons can run concurrently. Splitting does not prevent Persona from
speaking while listening. In fact, two daemons make CPU/memory isolation and
restart behavior cleaner: a stuck TTS provider does not stop recording; a
microphone backend crash does not stop playback.

The cost of splitting is coordination. Full-duplex features then need either:

- direct peer subscriptions between the two daemons;
- a small coordinator component that owns duplex policy;
- or a higher Persona component, likely mind/router/harness, deciding when
  speaking and listening should overlap.

The first option risks tight peer coupling. The third option puts local audio
device policy too high in the stack. The second option is clean if and only if
duplex policy is real state. That future component could be `persona-speech`.

## Recommended Shape

### First slice: `persona-transcription`

Build the urgent replacement as a transcription triad:

```text
persona-transcription/
  src/bin/persona-transcription-daemon.rs
  src/bin/transcription.rs

signal-persona-transcription/
  src/lib.rs
```

The daemon owns:

- durable recording sessions under its state directory;
- append-as-you-record audio writing;
- finalize-before-transcribe;
- backend selection and backend attempt ledger;
- size/duration preflight;
- transcript history linked to recording artifacts;
- retry after daemon restart;
- status and progress subscriptions;
- optional delivery of completed transcript text to Persona peers.

The daemon does not own:

- Persona message routing policy;
- mind graph policy;
- terminal input gates;
- Niri focus policy;
- TTS playback;
- cloud secret retrieval from Nix store or ambient env.

Likely actor planes:

- `TranscriptionRoot`
- `MicrophoneCapture`
- `RecordingWriter`
- `RecordingStore`
- `VoiceActivityDetector`
- `TranscriptionAttemptRunner`
- `BackendClient`
- `TranscriptPublisher`
- `RetentionPolicy`
- `PersonaDispatch`

The most important invariant from `primary-ipjx` becomes a witness test:
once recording begins, at least one durable artifact exists and is growing; a
daemon crash before finalize leaves a recoverable recording session.

### Future slice: `persona-speech-synthesis` / `persona-utterance`

Build speaking as its own triad when there is a concrete consumer:

```text
persona-speech-synthesis/
  src/bin/persona-speech-synthesis-daemon.rs
  src/bin/speech-synthesis.rs

signal-persona-speech-synthesis/
  src/lib.rs
```

This name is precise but long. `persona-utterance` is shorter and may be more
beautiful if the component's central durable noun is `Utterance`: a text input,
voice/style settings, generated audio artifact, playback state, and completion
record. The possible drawback is that "utterance" can describe both human and
synthetic speech in linguistics; if used, the ARCH must define it as Persona's
spoken-output object.

The daemon owns:

- voice catalog and default voice policy;
- utterance queue;
- provider/model selection;
- generated audio artifact state when retention is enabled;
- playback state and cancellation;
- output-device errors;
- playback subscriptions.

### Full-duplex slice: only if earned

If simultaneous speaking/listening becomes a first-class requirement, add a
coordinator only after the two directional components reveal the need. That
coordinator may be `persona-speech`, with a narrow role:

- subscribe to transcription recording state;
- subscribe to synthesis playback state;
- own barge-in, echo-reference, ducking, and device-lease policy;
- issue typed `Mutate` orders to the two directional components when it owns
  the authority to pause, resume, cancel, or alter device routing.

It should not transcribe or synthesize itself. It should coordinate speech
interaction state.

## Contract Sketch

This is a sketch, not an implementation spec. It names the likely nouns and
Signal roots.

`signal-persona-transcription`:

```text
RecordingSession
  recording_id
  source
  started_at
  artifact_reference
  sample_format
  phase

TranscriptionAttempt
  recording_id
  backend
  model
  attempt_number
  phase

Transcript
  recording_id
  attempt_number
  text
  segments
  confidence_summary

TranscriptionRequest
  Assert RecordingStart(...)
  Mutate RecordingFinalization(recording_id)
  Retract RecordingCancellation(recording_id)
  Assert TranscriptionAttempt(...)
  Match RecordingStatusQuery(...)
  Match RecordingListQuery(...)
  Subscribe TranscriptSubscription(...) opens TranscriptEventStream
  Retract TranscriptSubscriptionRetraction(token)
```

`signal-persona-utterance` or `signal-persona-speech-synthesis`:

```text
Utterance
  utterance_id
  text
  voice
  style
  phase
  artifact_reference

SynthesisRequest
  Assert UtteranceSubmission(...)
  Mutate UtterancePlayback(...)
  Retract UtteranceCancellation(utterance_id)
  Match VoiceCatalogQuery(...)
  Match UtteranceStatusQuery(...)
  Subscribe PlaybackSubscription(...) opens PlaybackEventStream
  Retract PlaybackSubscriptionRetraction(token)
```

The exact `Assert` vs `Mutate` choices need a designer pass. The principle is:
assert new facts or intents; mutate stable state when an authority orders a
specific state transition; retract subscriptions and cancellations when the
contract says the fact/stream should close.

## Integration With Persona

The transcription component should not bypass Persona by typing into terminals
as its only output. It can have a CLI path for human debug and a compatibility
desktop mode for CriomOS dictation, but its native integration should be
Signal:

- Completed transcript can be asserted as a typed observation to
  `persona-mind`.
- A dictation mode can submit text to `persona-message` as a
  `MessageSubmission` only after an explicit target exists.
- A harness can subscribe to transcript events for live voice input.
- The component should expose artifact references, not raw audio bytes, to
  peers.

The component's durable audio store remains owned by the transcription daemon.
`persona-mind` should store semantic references and decisions, not copy the
audio blob into `mind.redb`.

## Open Questions For The User

1. Is the first real product surface still dictation into the active desktop,
   or is the desired first surface Persona-native voice input to agents?
   Dictation wants fast clipboard/typing integration; Persona voice wants
   transcript events and message submission.
2. Does raw recorded human audio retain by default, or only until transcript
   acceptance? The durable-first invariant says "write first"; retention policy
   decides when deletion is allowed.
3. Should generated Persona speech be retained as durable artifacts? TTS can
   be regenerated from text/settings in many cases, but retention helps audit,
   replay, and debugging.
4. Is full-duplex conversation a first-version requirement or a future
   requirement? If first-version, we probably need a speech coordinator or at
   least a shared audio-device policy from day one.
5. Who owns echo cancellation and barge-in? If it is local audio policy,
   `persona-speech` can own it. If it is conversation policy, harness/router
   may participate, but they should not manipulate audio devices directly.
6. Is local-first mandatory for transcription/synthesis, with cloud backends
   only as opt-in, or should cloud be normal for quality? This affects model
   packaging, Nix closures, secrets, latency, and cost witnesses.
7. What is the typed target for a transcript: a message recipient, a mind
   thought, an active desktop insertion point, or all three as explicit modes?
   This must be typed; it should not be inferred from focus or a freeform CLI
   string.

## Risks

- A broad `persona-speech` becomes a hidden voice-agent monolith.
- A split transcription/synthesis design fails to coordinate full-duplex
  behavior and pushes echo/barge-in glue into random consumers.
- A realtime provider session is mistaken for durability. It is latency
  machinery, not a local artifact ledger.
- Audio bytes leak into Signal frames because it feels convenient. That would
  violate the triad's high-bandwidth carve-out.
- The component grows a "desktop dictation" backend that bypasses Persona
  forever. Compatibility is fine, but the native surface should be Signal.
- Cloud API keys leak into Nix or broad process environments. Follow the
  existing system-specialist secret discipline: daemon wrapper or manager
  supplies secrets at runtime, never store paths or reports.

## Bottom Line

Build `persona-transcription` first. It is the precise replacement for the
Whisrs durable-first gap and gives Persona a clean speech-to-text surface
without pre-deciding the larger voice architecture.

Keep synthesis separate until a real speaking consumer exists. When it does,
prefer `persona-utterance` if the central durable noun is the utterance, or
`persona-speech-synthesis` if the explicit transformation name reads better.

Reserve `persona-speech` for the moment when the system truly owns full-duplex
speech interaction as a bounded context. That component should coordinate
listening and speaking; it should not be the place where every audio-related
feature accumulates.

## Sources

Workspace sources:

- `skills/component-triad.md`
- `skills/micro-components.md`
- `skills/contract-repo.md`
- `skills/actor-systems.md`
- `skills/push-not-pull.md`
- `reports/second-system-assistant/1-whisrs-durable-first-stt-research-2026-05-17.md`
- `persona/ARCHITECTURE.md`
- `persona-message/ARCHITECTURE.md`
- `persona-mind/ARCHITECTURE.md`
- `persona-terminal/ARCHITECTURE.md`
- `persona-system/ARCHITECTURE.md`
- `signal-persona/ARCHITECTURE.md`
- `signal-persona-message/ARCHITECTURE.md`
- `signal-persona-system/ARCHITECTURE.md`
- `signal-core/ARCHITECTURE.md`
- `nota-config/ARCHITECTURE.md`

External sources:

- OpenAI Audio and speech guide:
  https://developers.openai.com/api/docs/guides/audio
- OpenAI Speech to text guide:
  https://developers.openai.com/api/docs/guides/speech-to-text
- OpenAI Realtime transcription guide:
  https://developers.openai.com/api/docs/guides/realtime-transcription
- OpenAI Realtime model announcement:
  https://openai.com/index/introducing-gpt-realtime/
- Deepgram Speech to Text guide:
  https://developers.deepgram.com/docs/stt/getting-started
- Deepgram streaming Text to Speech reference:
  https://developers.deepgram.com/reference/text-to-speech/speak-streaming
- Google Cloud Speech-to-Text overview:
  https://docs.cloud.google.com/speech-to-text/docs/overview
- Google Cloud bidirectional streaming Text-to-Speech:
  https://docs.cloud.google.com/text-to-speech/docs/create-audio-text-streaming
- Azure Speech-to-Text REST API:
  https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-speech-to-text
- Azure Text-to-Speech overview:
  https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech
- LiveKit Agents overview:
  https://docs.livekit.io/agents/
- Vocode "How it works":
  https://docs.vocode.dev/open-source/how-it-works
- ElevenLabs Text to Speech overview:
  https://elevenlabs.io/docs/overview/capabilities/text-to-speech
- ElevenLabs Speech to Text overview:
  https://elevenlabs.io/docs/overview/capabilities/speech-to-text
- Piper:
  https://github.com/rhasspy/piper
- sherpa-onnx:
  https://github.com/k2-fsa/sherpa-onnx
