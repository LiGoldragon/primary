---
name: knowledge-paralinguistic-transcription
description: Verified current facts about Android speech transcription, prosody-related output, providers, and IME insertion.
dependencies: []
---

Google's current Gemini audio documentation exposes transcription, translation,
speaker diarization, timestamps and emotion detection. Its structured example
uses speaker, timestamp, content, language and an emotion enum. These are model
judgments in a requested schema, not calibrated acoustic measurements. The
current pages do not name returned pitch, loudness, speaking rate, pause
duration, prosody contours or calibrated confidence. That absence does not
prove a model cannot infer such properties; timestamp gaps can support derived
pause or pace proxies that still require validation. [Evidence](../evidence/android-paralinguistic-transcription-sources.md)

The dedicated Gemini transcription route is stable `gemini-3.5-transcribe`
through `interactions.create`. It describes verbatim output, which preserves
fillers, repetitions, false starts and pauses as text, and smart cleanup, which
changes that representation. Smart mode cannot combine with word timestamps or
diarization; custom vocabulary accepts up to 1,000 terms but cannot combine
with speaker diarization or word-level timestamps. Its documented word and
speaker timestamps do not establish prosody annotations. The Live route is
`gemini-3.5-transcribe-live`: it documents interim/final input transcription,
utterance timing and a ten-minute session limit, but no word timestamps or
diarization. General Live currently names `gemini-3.8-live`; general audio
understanding and affective dialogue must not be substituted for these route-
specific facts.

The official dedicated-transcript estimates are about $0.005/min batch and
$0.009/min live under the published token assumptions. They do not establish
an all-in per-minute cost for richer annotations, markup, model analysis,
backend or network path. Paid rows state that prompts/responses are not used
for product improvement, while limited abuse/safety logging still applies.
Interactions default to 55-day paid or 1-day free storage; `store=false` opts
out of Interaction storage but does not erase all abuse/safety logs and disables
previous-interaction and background execution. EEA/UK/Switzerland paid-service
exceptions require account/route review. These Google terms do not transfer to
OpenRouter or vBoard. No matched accuracy or latency comparison with Wispr was
found. Wispr's
Android product is an accessibility/overlay flow whose listing describes
removing fillers, stutters, false starts and self-corrections; that documents
cleanup behavior rather than preserved prosody. Its dated Play and help pages
currently conflict about free/unlimited use versus a 1,000-word mobile weekly
soft limit and 1,500-word hard cap. Pro is listed as $15 monthly or $12/month
when billed annually. vBoard documents Gemini through OpenRouter; this is not
evidence of direct paid Gemini API routing. Loquela's Full unlock amount is not
publicly established in the checked source, and Dictus makes a free-project
claim. Their model catalogs and privacy claims are not device accuracy or
latency measurements.

Android's documented custom keyboard path is `InputMethodService` plus
`InputConnection` composing and `commitText`. A custom tag can be committed as
literal text and consumed by a downstream machine, while ordinary target apps
still treat it as text rather than shared prosody semantics. Microphone and
foreground-service restrictions, IME lifecycle, OEM behavior and sensitive
field policy require target-device verification. Long-lived provider keys
belong off-device; restricted Live ephemeral tokens still require a backend and
do not automatically cover every API route.

A minimal implementation shape remains a design option: microphone button or
bounded utterance capture, stop/VAD, a model adapter, separate raw words and
annotation result, user review, and `commitText` of accepted text or literal
markup. A local ASR route may improve privacy but does not itself produce
prosody. Literal markup and a separate display/export representation are both
open choices. [Primary evidence and URLs](../evidence/android-paralinguistic-transcription-sources.md)
