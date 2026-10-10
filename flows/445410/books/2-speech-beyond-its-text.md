Presentation.{ «Speech beyond its text» }

Today the living's voice reaches the flows as text alone. The emotion, the emphasis and the pauses are gone before any flow reads a word. This book reports what the research found about getting them back and proposes one line for the skills. Nothing of this is built; it is research. Only four sources were opened and read by the researcher: two Gemini documentation pages, one paper, and our own records. Everything else is reported from search summaries and was not witnessed.

## What Gemini does

Only when asked: it gives words, per-word timings and speaker labels as standard. Emotion, emphasis, tone and hesitation appear only if the prompt names them and the response format holds a field for them. A verbatim mode keeps fillers, false starts and self-corrections; a clean mode removes them without marking that it did.

Not at all: it has no built-in field for emotion, emphasis, tone, pace, hesitation or pause. Google's cloud speech service has none either, and its per-word confidence is, by its own documentation, not truly a confidence score.

## What is unreliable

- Gemini's own timestamps drift, so pauses should come from a separate aligner. This rests on user reports; Google has said nothing.
- Audio models tend to judge emotion from the words more than from the voice. When words and voice disagree, one tested model followed the words. Gemini was not in that test, so whether it does the same is unknown.
- Misread paralinguistic cues are a large share of errors in the benchmarks. Nobody has published Gemini's accuracy on emphasis or hesitation.
- The one result in Gemini's favour is a single political speech, compared with scores from other language models, not with human labels.

## The few alternatives

All reported, none witnessed: a commercial transcriber that tags timed sounds such as laughter and applause; a transcription setting that keeps fillers; an open model that keeps fillers and false starts and marks pauses, its licence reported as non-commercial; an open model that scores emotion straight from the voice. A real-time emotion service remains; its batch form was shut down.

## How it would work here

This is the flow's inference, not a finding.

- The verbatim words stay unchanged.
- Annotation is a separate layer of marked spans keyed to the words. Each span has a range, a kind, and the model's own confidence.
- It runs in the listener, while the audio still exists, as a second pass. The cues live only in the audio, and the dictation tool hands back plain text.
- Flows read a mark as evidence, never as a ruling. A mark of thinking aloud can prompt a question to the living. It never moves a record from vision to notion by itself.

What is supported: repairs and broken-off sentences today, because the verbatim mode keeps them. Pauses, from gaps between aligned word timings. Emphasis, uncertainty, and thinking aloud against pronouncement, only by prompting, untested, and mostly judged from the words. The smallest test is to annotate a sample of dictations and compare the marks with the living's own reading of the same clips.

## 1. The living's direction on speech understood deeper

Target: psyche-skills/skills/vision-speech-to-text.md, a new file. No existing vision skill covers speech-to-text.
Removed: none.
Added:
The living's speech is understood deeper than its text: the emotion, emphasis and pauses of his voice reach the flows beside his verbatim words.
Source: flows/445410/vision/speech-to-text.md, 2026-10-09.
Ruling: Create the skill with this line and its source?
