# Wispr Flow streaming in Listener: psyche and history

This is a carried evidence account for flow `4647d2`. `Listener` is the
canonical product spelling. The quotes are written-psyche residues: they are
preserved as recorded, while flow outcomes and technical findings are kept
separate from the living's words.

## Psyche levels

### Spirit

No Wispr- or Listener-specific Spirit expression was found in the loaded
Spirit record.

### Intent

No Wispr- or Listener-specific distilled Intent record was found.

### Vision

The repository search found no matching distilled `Vision/` entry. The
topic-scoped raw vision is in `flows/01a04e75/vision/listenerWisprFlow.md`,
`flows/01a0539e/vision/listenerWisprFlow.md`, and
`flows/01a0539e/vision/wisprInteraction.md`. The following are the relevant
expressions, oldest first.

#### One transcription subscription across Android and Linux

> "Okay, because I can use Wispr Flow on my Android phone and I need speech-to-text, and it's just more practical right now. I don't want to pay $15 a month for Wispr Flow and then also pay for OpenAI API usage for my speech-to-text on desktop. ... That way, I could just pay for this one Pro subscription for Wispr Flow and use it both on my Linux desktop and on my phone."

-- psyche, STT.

Source: `flows/01a04e75/vision/listenerWisprFlow.md`; originating Codex
transcript `/home/li/.codex/sessions/2026/08/29/rollout-2026-08-29T18-58-20-01a04e75-3aee-7720-aa42-64a47f07a9e6.jsonl`, physical lines 9–10.

#### Map the API and keep the implementation separate

The initial design message contains this additional expression, which was
not copied into the flow's vision file:

> "The first thing we need to do is figure out that whole API: what's available, maybe even the implementations that exist right now. The unofficial clients don't even use the entire API. Is there a vocabulary list that we can provide them, and some parameters, recovery, error messages, and everything? Let's get this all mapped out, and then we'll see how we can implement this simply in a separate module in listener so that we can think about it mentally more in a separate way."

-- psyche, STT.

Source: the same 01a04e75 transcript, physical lines 9–10.

#### Different providers and listeners

> "Maybe we need to create an abstraction for different providers and listeners so that it's easy to add different backends. Maybe eventually, soon, we're going to have our own Wispr server providing us with speech-to-text."

-- psyche, STT.

Source: `flows/01a04e75/vision/listenerWisprFlow.md`; 01a04e75 transcript,
physical lines 9–10.

#### First choice with fallbacks

> "Could you confidently implement a first-choice with fallback(s), which would be data-configured in a meta-listener operation, so that a failing Wispr Flow API would send the transcription to OpenAI, with a notification telling me about a failing provider?"

-- psyche, STT. “Whispr Flow” was corrected in the filed record to “Wispr Flow.”

Source: `flows/01a04e75/vision/listenerWisprFlow.md`; 01a04e75 transcript,
physical line 291.

#### Use Wispr through my own Listener Nexus

> "In the end we still want to just get my credentials from wherever the Wispr application is putting them and use Wispr through my own Listener Nexus."

-- psyche, STT.

#### Use it as a backend for my Listener service

> "I would rather just use it as a backend for my Listener service in the future."

-- psyche, STT.

The two preceding expressions are filed in
`flows/01a0539e/vision/listenerWisprFlow.md`; their originating source is the
01a05512 transcript, physical line 273 for the Nexus wording and physical
line 471 for the backend wording (each followed by its event record).

#### A shortcut where I don't have to hold the thing

> "I would like to have a shortcut where I don't have to hold the thing while I'm speaking"

-- psyche, STT.

Source: `flows/01a0539e/vision/wisprInteraction.md`; 01a05512 transcript,
physical line 9.

#### It should just be a widget in the status bar

> "This floating Wispr status thing is kind of inappropriate for my kind of desktop. It should just be a widget in the status bar"

-- psyche, STT.

Source: `flows/01a0539e/vision/wisprInteraction.md`; 01a05512 transcript,
physical line 273.

#### Different operations using a different message for Listener

> "We would add streaming capability to the Listener, and these would be different operations, so they would be initiated using a different message for a Listener. It could support both modes."

-- psyche, STT.

> "Sometimes I needed a particular audio file that I had already recorded to be transcribed. ... It would get the path to an audio file, and it would just use that audio file to get a transcription for it. ... Obviously that would not be a streaming type because the audio files are already recorded."

-- psyche, STT.

Source: `flows/01a0539e/vision/listenerWisprFlow.md`; 01a05512 transcript,
physical line 637.

#### Stream the transcription as well in real time

> "Can they stream the transcription as well in real time so that we could somehow maybe have some kind of visual showing us that real-time transcription while it's happening? That would be kind of cool."

-- psyche, STT.

> "Do side research on a visual notification client that would be compatible with our desktop shell, maybe even one that is included or can fit into the shell that we are using right now. That would be well integrated or well suited for showing the real-time streaming of the words while they're being recorded."

-- psyche, STT.

Source: `flows/01a0539e/vision/listenerWisprFlow.md`; 01a05512 transcript,
physical line 637 for the first quote and 683 for the second.

#### Notify us that we've entered the cutoff window for the chunks

> "Maybe only make that widget notify us somehow that we've entered the cutoff window for the chunks, so that there's a need to leave an obvious pause soon, so that the chunks can stop and start a new one for transcription."

-- psyche, STT.

Source: `flows/01a0539e/vision/listenerWisprFlow.md`; 01a05512 transcript,
physical line 518.

#### Inserting into the clipboard and history suffices for now

> "I never use Listener to automatically inject the text. ... Inserting into the clipboard and history suffices for now."

-- psyche, STT.

Source: `flows/01a0539e/vision/listenerWisprFlow.md`; originating 01a05512
transcript, physical line 978. The transcript's message uses lowercase
`listener`; the filed record uses the canonical product spelling `Listener`.

#### Ease of one-hand reach on my layout

> "It's confusing that they use different modifier keys. Favor ease of one-hand reach on my layout, Colemak, over letter-based mnemonics."

-- psyche, STT.

Source: `flows/01a0539e/vision/listenerWisprFlow.md`; 01a05512 transcript,
physical line 978.

#### Do not rely on X11

> "The fact that it has to run through X alone sucks. I don't know if that's a necessity, but I don't want X11 in my stack. ... It's good to have it installed. It's a good fallback, and I just don't want to have to rely on it."

-- psyche, STT.

Source: `flows/01a0539e/vision/wisprInteraction.md`; 01a05512 transcript,
physical line 471.

#### Fast transcription while recording

This is a direct expression that explains why the streaming capability matters:

> "One thing that is really cool about Wispr is that it's really fast to transcribe once I'm done recording. I'm guessing that's because it's actually transcribing while I'm recording. I'm just wondering if there is a way for us to support something like that with listener."

> "I know that OpenAI, and I'm not talking about just OpenAI, I'm talking about using the Wispr backend this way with listener. I guess the reason we weren't really doing that with OpenAI is because it's not a real-time thing. We were not using the real-time OpenAI API, but they do have one. It's more expensive, so we weren't doing that. Can you look into that and see what's what?"

-- psyche, STT.

Source: 01a05512 transcript, physical line 583. The filed vision record
uses the canonical `Listener` spelling in the related excerpts above.

### Notion

The psyche explicitly marked this as a possible idea and brainstorming; it
does not bind the implementation:

> "How can we get continuous recording using Wispr Flow using chunks? Problem: the cutoff could be at a very bad time. Use a very small local model to find a natural pause after 4-5 minutes? Use overlapping chunks and re-assemble the transcript?"

-- psyche, typed. “wisprflow” was corrected in the filed record to “Wispr Flow.”

Source: `flows/01a04e75/notion/continuousRecordingUsingWisprFlowChunks.md`;
01a04e75 transcript, physical line 352.

An adjacent follow-up was:

> "if the limit is 6 then we can set a hard limit a tad below that. create a fork and implement your idea."

-- psyche, typed.

Source: 01a04e75 transcript, physical line 407. This follow-up is a working
request after the explicitly marked notion, not a separate distilled Vision
or Intent ruling.

## Historical flows and what they establish

These are flow records and witnesses, not additional psyche authority.

### `01a0439e` — Listener durability and transcription boundary

This is the earliest directly relevant Listener evidence found. Its reports
describe the deployed Listener 0.14 behavior: completed recordings are kept
in owner-only durable history; older sessions can finalize/transcribe while a
new recording proceeds; longer recordings were submitted as independent
600-second requests and joined locally; and the known long-capture anomaly had
no retained per-chunk response trace, so its exact upstream cause remained
unknown. It also carries the standing vocabulary request for speech-to-text
from `019fe121`.

The 01a04e75 log says it remembered `01a0439f`, but no such flow directory is
present; the extant Listener reports and index entry are under `01a0439e`.
That suffix mismatch should not be silently treated as two flows.

### `019fe121` — Speech-to-text vocabulary

The raw vision record preserves:

> "And that's another thing. We should add that. We should, after all this, we should look at the vocabulary for my speech-to-text."

-- psyche, typed.

Source: `flows/019fe121/vision/dictationVocabulary.md`, with its originating
transcript and physical line recorded there. This is relevant to provider
customization but does not itself specify Wispr streaming.

### `01a04e75` — Design and isolated Listener feature

This flow researched Wispr's unofficially used service surface and Linux
clients, mapped Listener, and implemented an isolated Listener feature at
version 0.17.0 (`71a194df8dc6dfb232049473481e67b405153e49`) with portable
companion revisions. Its log records a provider-neutral boundary,
Wispr-first/OpenAI fallback, a privileged data-configured provider policy,
provider health/degradation notifications, durable job/result/history and
delivery receipts, and pause-aware segmentation with a hard cap and overlap
stitching. It says the synthetic Nix gate and package build passed.

The same log is explicit about the boundary of that work: main integration,
downstream activation, gopass provisioning, and real Wispr interoperability
were not performed; no real credential or provider call entered the flow.
It also corrects that `wispr-flow-linux` is an unofficial repackaging of the
proprietary Electron desktop client, not an independent API implementation.
The inferred private gRPC route differed from the desktop bundle's observed
Baseten route and extra headers, so compatibility remained unproved.

### `01a05209` — Package the desktop fallback, keep it separate

This realization remembered 01a04e75 and packaged the user-supplied Wispr
Flow 1.6.7 desktop installer on NixOS. Its integration boundary explicitly
kept Listener, Listener autostart, and Listener hotkeys unchanged; Home owned
the desktop package and CriomOS owned only narrow input capability. Live
deployment preserved production Listener, but the living's onboarding witness
showed missing modifier capture and a broken Status surface. This is desktop
fallback/infrastructure history, not proof that Listener can call Wispr's
streaming backend.

### `01a052bb` — Deploy the desktop package through the proposal repair

This flow repaired the canonical proposal path and activated the packaged
desktop client. It left the remaining keyboard capture and Status behavior
open, and handed those to 01a0539e. It does not establish Listener streaming.

### `01a0539e` — Pivot from desktop UI to Listener backend and visual

This flow's own direction change says the desired destination is the living's
Listener Nexus using Wispr as a provider, with the desktop retained only as a
fallback. It preserved production Listener 0.14.0 and later recorded the
typed-operation anatomy: streaming and ordinary capture are different
operations/messages, a third operation accepts an already-recorded audio-file
path, and file transcription is non-streaming. It also recorded the open
question of whether file results enter durable history/delivery or only return
to the caller.

An isolated Wispr-only Listener sandbox was then pushed at
`04c5ba2aba60b5e2c49de86e740f33c88161b0b4`, using separate paths and inherited
credential descriptors. Two single submissions of the non-private fixture
“Listener sandbox confirms the blue comet.” failed with the same redacted
provider-protocol failure; neither returned a transcript. Whether either
request reached inference or billing is unknown, and the log authorizes no
third private-backend request.

The flow's later streaming research record says Desktop 1.6.7 sends
bidirectional init/context/audio packets and receives intermediate states,
while the official Voice API separately documents WebSocket partial/final
results. That record also says official access is approval-based and metered,
and that a consumer Flow Pro subscription does not officially establish reuse
of the private desktop backend. These are historical research claims, not a
successful Listener interoperability witness.

For the visual, the existing Noctalia `criomos/listener-level` plugin was
extended with a private transcript stream parser and bounded multiline panel.
Synthetic tests and a temporary-socket live shell witness proved ordered
partial/final rendering, stale rejection, clearing, and no notification
spam; production Listener remained on its existing PID/sockets and no real
Wispr transcript was displayed. A manual panel toggle can reconcile only on a
later terminal/disconnect transition.

### `01a05588` — Supported local Desktop proxy inquiry

Two read-only inspections recorded no supported/public local authenticated
transcription proxy in Wispr Desktop 1.6.7: no TCP/UDP listener, no
transcription CLI, DBus service, native-messaging host, or advertised HTTP
socket. The Electron singleton socket and helper pipes were internal; the
declared `wispr-flow:` deeplinks only start/stop hands-free mode, switch
microphones, or navigate and do not submit audio or return transcripts.
No session contents were read, no endpoint was contacted, and production
Listener stayed unchanged.

The living then said:

> "then let's reverse engineer its api. I have their implicit permission to do so"

-- psyche, typed.

Source: `/home/li/.codex/sessions/2026/08/31/rollout-2026-08-31T03-57-07-01a05588-db47-7091-af64-914a7c01fa1f.jsonl`, physical line 230.

The flow log records that static private-protocol archaeology was opened but
no new billable backend call was to be made until the request shape could be
discriminated. The sentence is the living's stated authority, not an
independent vendor-license witness.

### Peripheral desktop-only flows

`01a05e03` repaired the Wispr Linux helper's modifier-release path and proved
the desktop helper's virtual device had no held modifiers. It explicitly kept
Wispr as a contingency/future Listener backend and did not reopen Listener
backend work. `01a05d25`, `01a05cd5`, and related flows concern desktop setup
window/profile deployment and are not evidence of Listener streaming.

## Current boundary and unresolved questions

- The living's direction is clear at Vision level: Listener is the ordinary
  surface; Wispr is a desired provider backend, with a separate streaming
  operation and partial-transcript visual. The 0.17.0 feature is isolated;
  main integration and activation are not witnessed.
- Real private Wispr interoperability remains unproved: the two sandbox
  requests failed without a transcript, and their inference/billing outcome
  is unknown. The desktop bundle's route and the inferred Listener route did
  not match in the static record.
- Authority is unresolved. The living stated implicit permission for private
  reverse engineering, but no official contract or vendor licensing record
  was found for reusing the private desktop protocol. Official Voice API
  access, entitlement, metering, and limits remain separate questions.
- Credential privacy is unresolved as a product contract. Desktop session
  material stayed behind a mode-protected boundary and was not read into
  these records; the feature expected gopass or inherited-descriptor delivery,
  but no accepted credential-consumer interface has been approved. No secret
  should enter arguments, ordinary environment, logs, reports, temporary
  files, clipboard, or commits.
- The partial-transcript visual has a synthetic Noctalia implementation and
  parser proof, not a real Wispr stream. Its ownership/persistence was an
  open design question during 01a0539e; the chosen panel keeps text in shell
  memory and rejects stale revisions, but production Wispr delivery remains
  unproved.
- The cutoff warning's exact start, urgency, and modality remain open. The
  existing Listener status-bar widget is the intended place for the cue.
- File transcription's durable behavior remains open: whether a path-based
  result only returns to its caller or also enters Listener history and the
  normal clipboard/delivery path needs an explicit ruling. The living did
  state that ordinary Listener behavior should use clipboard and transcription
  history, without automatic focused-application injection.
- The hands-free shortcut should use the same modifiers for start and stop,
  favor Colemak one-hand reach, and avoid inventing a binding until actual
  physical placement and conflicts are checked. This is adjacent desktop
  interaction, not proof of backend streaming.

## Sources

- `flows/01a04e75/vision/listenerWisprFlow.md`
- `flows/01a04e75/notion/continuousRecordingUsingWisprFlowChunks.md`
- `flows/01a04e75/log.md`
- `flows/01a0539e/vision/listenerWisprFlow.md`
- `flows/01a0539e/vision/wisprInteraction.md`
- `flows/01a0539e/log.md`
- `flows/01a0439e/log.md`
- `flows/01a0439e/reports/listenerContext.md`
- `flows/01a0439e/reports/listenerRuntime.md`
- `flows/01a0439e/witnesses/listenerRuntime.md`
- `flows/019fe121/vision/dictationVocabulary.md`
- `flows/01a05209/log.md`
- `flows/01a052bb/log.md`
- `flows/01a05588/log.md`
- `flows/01a05e03/log.md`
- `/home/li/.codex/sessions/2026/08/29/rollout-2026-08-29T18-58-20-01a04e75-3aee-7720-aa42-64a47f07a9e6.jsonl`, physical lines 9–10, 264, 278, 291, 352, 407, 2200, 2214, and 2242
- `/home/li/.codex/sessions/2026/08/31/rollout-2026-08-31T01-47-18-01a05512-0204-75e2-9733-bac963f1051f.jsonl`, physical lines 9, 145, 250, 273, 309, 471, 507, 518, 545, 571, 583, 637, 683, 966, 978, and 992
- `/home/li/.codex/sessions/2026/08/31/rollout-2026-08-31T03-57-07-01a05588-db47-7091-af64-914a7c01fa1f.jsonl`, physical line 230
