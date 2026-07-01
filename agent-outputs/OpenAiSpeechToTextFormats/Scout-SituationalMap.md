# Scout Situational Map

## Task And Scope

Question from psyche: for OpenAI speech-to-text, especially realtime transcription, identify current official evidence for supported audio formats. Practical design context: Listener may use WebM/Opus for batch upload because of file-size limits, but realtime transcription may require PCM or G.711-style streaming frames.

Scope followed: public OpenAI sources only where possible; no private material; no source edits. The only workspace write was this required scout output under `agent-outputs/OpenAiSpeechToTextFormats/`.

## Direct Answer

For batch Audio API transcription uploads, OpenAI officially supports WebM as an upload file type and applies a 25 MB upload limit in the Speech-to-text guide. The current API reference for `POST /audio/transcriptions` lists these accepted file formats: `flac`, `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `ogg`, `wav`, and `webm`. The guide page omits `flac` and `ogg`, so the safest current wording is: WebM is clearly supported for upload; Ogg is listed in the API reference; neither page explicitly says "Opus" as a codec, even though WebM/Ogg often carry Opus in practice.

For realtime transcription, the current GA Realtime docs do not document WebM, Ogg, or Opus as supported realtime input formats. Realtime sessions configure raw audio formats: `audio/pcm` at 24 kHz, `audio/pcmu` for G.711 μ-law, or `audio/pcma` for G.711 A-law. WebSocket audio events carry base64-encoded audio bytes in the configured session format, so a Listener-style WebSocket pipeline should plan to decode/transcode browser/container audio to PCM 24 kHz or G.711 before appending it.

WebRTC is distinct operationally: the OpenAI WebRTC guide shows browser microphone input as a WebRTC media track and recommends WebRTC for browser/mobile clients, while WebSocket is recommended for server-to-server integrations. The official WebRTC guide does not provide a codec/container support list and does not say that WebM/Opus or Ogg Opus chunks may be sent as realtime transcription input. Treat WebRTC as a media-connection path, not as evidence that WebM container chunks are accepted by the realtime JSON/audio-buffer API.

## Official Sources Used

- OpenAI API docs, page title: **Speech to text**. URL: `https://developers.openai.com/api/docs/guides/speech-to-text`. Relevant section: page intro and **Quickstart / Transcriptions**. Evidence: file uploads are limited to 25 MB; listed upload file types are `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, and `webm`; the page directs live microphone/call/media-stream use to **Realtime transcription**.
- OpenAI API Reference, page title: **Create transcription**. URL: `https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create`. Relevant section: `POST /audio/transcriptions`, body parameter `file`. Evidence: the audio file object must be one of `flac`, `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `ogg`, `wav`, or `webm`.
- OpenAI API docs, page title: **Realtime transcription**. URL: `https://developers.openai.com/api/docs/guides/realtime-transcription`. Relevant sections: intro, **Choose a transcription model**, and **Create a transcription session**. Evidence: realtime transcription is for live transcript deltas; `gpt-realtime-whisper` is the live transcription model; sessions use `type: "transcription"` and can connect with WebSocket for server-side audio pipelines or WebRTC for browser audio; the example input format is `{ "type": "audio/pcm", "rate": 24000 }`.
- OpenAI API docs, page title: **Realtime and audio**. URL: `https://developers.openai.com/api/docs/guides/realtime`. Relevant section: **Choose a realtime session**. Evidence: realtime sessions are separated into voice-agent, translation, and transcription sessions; transcription sessions are for streaming transcript deltas without model-generated spoken responses.
- OpenAI API Reference, page title: **Create client secret**. URL: `https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create`. Relevant section: `session` configuration, `audio.input.format`. Evidence: GA `RealtimeAudioFormats` variants are `audio/pcm` at 24 kHz, `audio/pcmu`, and `audio/pcma`.
- OpenAI API Reference, page title: **Realtime client events**. URL: `https://developers.openai.com/api/reference/resources/realtime/client-events`. Relevant section: `input_audio_buffer.append`. Evidence: appended audio is base64-encoded audio bytes and must match the session input audio format; each event can carry up to 15 MiB of audio.
- OpenAI API docs, page title: **Realtime API with WebSocket**. URL: `https://developers.openai.com/api/docs/guides/realtime-websocket`. Relevant sections: intro, **Connect via WebSocket**, and **Sending and receiving events**. Evidence: WebSocket is framed as server-to-server; browser/mobile clients are steered toward WebRTC; over WebSocket, clients send/receive JSON events and are responsible for base64-encoded audio chunks.
- OpenAI API docs, page title: **Realtime API with WebRTC**. URL: `https://developers.openai.com/api/docs/guides/realtime-webrtc`. Relevant sections: intro and browser connection example. Evidence: WebRTC is recommended for client/browser/mobile realtime audio; example uses `navigator.mediaDevices.getUserMedia({ audio: true })` and `pc.addTrack(...)` rather than WebM/Ogg file chunks.
- OpenAI API Reference, page title: **Create transcription session** under **Realtime Beta**. URL: `https://developers.openai.com/api/reference/resources/realtime/subresources/transcription_sessions/methods/create`. Relevant section: deprecation notice and `input_audio_format`. Evidence: deprecated beta endpoint lists legacy names `pcm16`, `g711_ulaw`, and `g711_alaw`; the page says it is deprecated in favor of the realtime GA API.

## Observed Facts

- `Speech to text` guide says file uploads are limited to 25 MB and supports `webm` among listed file types.
- `Create transcription` API reference additionally lists `flac` and `ogg` as accepted transcription upload file formats.
- No official source consulted lists `opus` as a Speech-to-text upload file type or as a Realtime input format name.
- `Realtime transcription` guide uses `audio.input.format.type = "audio/pcm"` and `rate = 24000` in the session example.
- GA Realtime API reference enumerates `audio/pcm`, `audio/pcmu`, and `audio/pcma` as `RealtimeAudioFormats`.
- Deprecated Realtime Beta reference uses older enum names `pcm16`, `g711_ulaw`, and `g711_alaw`; this maps conceptually to PCM16 / G.711 μ-law / G.711 A-law but is not the current GA shape.
- Realtime WebSocket docs say the developer sends JSON-serialized events and handles base64-encoded audio chunks.
- Realtime WebRTC docs show browser microphone tracks over WebRTC and recommend WebRTC over WebSocket for browser/mobile clients, but they do not publish a codec/container list in the consulted sections.

## Interpretations

- Listener can use WebM for batch transcription uploads within the 25 MB limit. If it specifically means WebM/Opus, the official docs support the `webm` container but do not explicitly guarantee an `opus` codec acceptance matrix.
- Listener should not design realtime transcription around shipping WebM/Opus or Ogg Opus chunks to `input_audio_buffer.append`; official docs point to configured raw PCM/G.711 formats for realtime event audio.
- For browser realtime capture, WebRTC may avoid manual PCM chunk plumbing, but official docs do not establish WebM/Opus chunk support. If Listener's architecture needs a server-side WebSocket path, transcoding to `audio/pcm` 24 kHz or G.711 is the source-backed route.

## Unknowns And Docs Gaps

- Official docs consulted do not state whether `webm` uploads specifically accept every common WebM audio codec, including Opus. They list file/container extensions, not codec-level matrices.
- Official WebRTC docs consulted do not state the negotiated audio codec(s) used with OpenAI or whether any codec preference is configurable.
- There is a small discrepancy between the Speech-to-text guide and the `Create transcription` API reference: the guide lists `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, `webm`; the API reference lists those plus `flac` and `ogg`. For implementation, the API reference is the narrower endpoint contract source, while the guide is the explicit source for the 25 MB file-size limit.

## Commands And Queries Consulted

- `sed -n '1,220p' /home/li/.codex/skills/.system/openai-docs/SKILL.md`
- `sed -n '1,180p' /home/li/primary/AGENTS.md`
- `spirit "(PublicTextSearch [OpenAI speech to text realtime transcription audio formats])"`: no specific OpenAI audio-format intent record found; only general public intent records appeared.
- Official-domain web lookups via `web.search_query`, then direct opens of the OpenAI developer docs pages listed above.

## Checks Not Run

- No API calls were made against OpenAI endpoints.
- No private repositories or private docs were inspected.
- No local code or Listener repository files were inspected, because the task was limited to current official documentation lookup.
