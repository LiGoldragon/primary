# Listener context

## Verbatim psyche

The standing listener/healing record says:

> I would like the listener component to And the user interface for it right on
> my desktop to support Being able to record While there's a transcription or
> more than one transcription going on and

> I certainly would prefer even if I have to manually select the transcription
> from the menu Then losing a transcription because I started recording before
> the previous one was done. That's very frustrating

> ... the really slow transcription ... [you can] take charge of ... Implementing
> the multiple transcription in parallel ... and never lose Never lose a transcript

> I just lost a recording; the multiple transcription in parallel isnt working
> smoothly.

Source: `psyche-raw/Vision/healingAspect.md` (captured 2026-08-09).

The only standing dictation-vocabulary request found is:

> we should look at the vocabulary for my speech-to-text.

Source: `flows/019fe121/vision/dictationVocabulary.md`, 2026-08-08.

## Immediate prior flow context

Flow `04db2fd2` (2026-08-27) contains the immediately preceding long STT
monologue. Its own log says the message was split into ten topic records and
that the psyche-logging proposal should retain only relevant verbatim excerpts,
mark omitted stretches with ` ... `, and keep the original transcript reachable.
The flow's final model response, read from its Claude transcript, reported two
unapplied proposals (excerpt logging and rolling distillation) and five open
anatomy questions. This is the closest prior listener-related event found; it
does not itself establish that the current odd result came from the listener.

Flow `f426777b` records a later audio statement whose transcript was still
pending when the flow ended; its final model response was a design handoff,
not a transcription diagnosis. This establishes that audio input was being
used in the design flow but gives no result for the pending transcript.

## Known transcription failure pattern

Historical psyche records repeatedly show technical names requiring explicit
correction after dictation. Examples include `schema-rust`/`ethos-rust` being
heard as “schema rest”/“ethos rest”, and `Rust` being heard as “rest”. The
three-stack record also flags “Dothos”, “demons”, and “Frotos” as probable
listener artifacts before later typed corrections. These are claims/records of
recognition error, not proof of the current failure mode.

## Current intended behavior witness

The current Listener README describes the desired contract: `Toggle.{}`
releases the recording slot after graceful completion is acknowledged even
while finalization/transcription continues; multiple older sessions may
finalize and transcribe concurrently; successful results are appended to
owner-only history; a failed retry keeps its compact artifact and remains
retryable. `tests/history.rs` additionally witnesses newest-first history,
multiline round-trip, owner-only permissions, malformed-tail recovery, atomic
replacement, and concurrent appends without lost records.

The implementation source currently feeds completed compact WebM/Opus into an
OpenAI transcription request with a generic instruction to preserve technical
names, optionally extended by a vocabulary archive. That makes recognition,
customization, artifact choice, and downstream history/delivery distinct places
to test; this report does not choose among them.

## Claims, observations, hypotheses, unknowns

Claims from prior flow/model responses: `01a0193f` ended with deployment and
safe reload reported successful, while user-visible widget confirmation remained
a proof gap. `019fe121` ended with an awareness/session-log rewrite and did not
settle listener behavior. `04db2fd2` ended with the excerpt-logging proposal
awaiting the psyche's word.

Direct observations: the files and source paths cited above exist; the current
Listener checkout is clean; the relevant README and tests state the behavior
described above; and the historical records contain explicit STT corrections.

Hypotheses: the current odd result could be a normal STT recognition artifact,
an input/customization mismatch, an artifact/session mix-up, or a display/
delivery projection issue. No one of these is supported strongly enough here.

Unknowns: the exact latest transcript text, its capture/session identity, the
audio bytes actually uploaded, the prompt/customization used for that request,
and whether the oddness appeared before or after history/delivery are left to
the parent event/runtime witnesses.

## Sources

- `psyche-raw/Vision/healingAspect.md`
- `flows/019fe121/vision/dictationVocabulary.md`
- `flows/012fbf07/vision/archive-threeStacks.md`
- `flows/13cfc23f/vision/threeStacks.md`
- `flows/c6b71b4c/vision/archive-threeStacks.md`
- `flows/04db2fd2/log.md`
- `flows/04db2fd2/vision/psycheLogging.md`
- `flows/f426777b/log.md`
- `flows/01a0193f/log.md`
- `/git/github.com/LiGoldragon/listener/README.md`
- `/git/github.com/LiGoldragon/listener/tests/history.rs`
- `/git/github.com/LiGoldragon/listener/src/transcription.rs`
- Last model responses read from the Codex/Claude transcripts for flows
  `01a0193f`, `019fe121`, `04db2fd2`, `f426777b`, `01a04236`, `01a0428b`, and
  `01a04290`.
