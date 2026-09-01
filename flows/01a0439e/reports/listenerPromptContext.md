# Listener prompt/context follow-up

## Scope

Focused read-only check against the known anomaly: duplicated Java
`public static void main(String[] args) {` and 94 `newline + eight spaces + //`
prefixes in stored Listener output.

## Supported local observations

- Listener source sends model `gpt-4o-transcribe` to `/v1/audio/transcriptions`
  with language `en` and this generic prompt: `Transcribe spoken English as
  dictated text. Preserve technical names, product names, and acronyms exactly
  when spoken. Do not translate.` (`src/transcription.rs:19-22, 652-658`).
- If `LISTENER_TRANSCRIPTION_CUSTOMIZATION_ARCHIVE` is set, source reads one
  trimmed nonempty term per line and appends only
  `Vocabulary terms to preserve exactly when spoken: <terms>.` to that prompt
  (`src/transcription.rs:245-253, 280-286, 301-311`). No Java signature,
  comment-prefix instruction, Markdown, or code-format instruction appears in
  this code.
- The current Listener process (PID 3296598, same process started before capture
  530) exposes no `LISTENER_*` environment variables; the service's referenced
  environment file is absent. This makes the generic prompt the strongest live
  configuration inference, but the historical request itself does not record
  its prompt.
- The current deployed binary's strings contain the model and generic prompt,
  but not the Java signature or a comment-prefix directive. The Listener test
  vocabulary contains product/system terms (for example `Mentci`, `SEMA`,
  `Nexus`, `Rust`-adjacent terms), not Java or comment-format instructions.
- Exact-signature search found no independent match in authored `Vision/`,
  `psyche-raw/`, `flows/*/vision/`, or the Listener repository. The exact Java
  text appears in the anomalous private 04db2fd2 transcript/event itself, so
  that occurrence is not independent prior context.

## Prior psyche/code context

Authored records do contain generic source-code concepts: `mainFunction.md`
describes a program/source-code object; `protosIsTheSharedStyle.md` says to
start with text source code and make each logical aspect a type;
`structuralParsing.md` shows Ethos examples with `;;` comments; and
`aa4c7747/vision/ethos.md` mentions Rust and JavaScript as noisy programming
languages. These records contain no Java method signature and no `//` comment
formatting rule. They are agent-recovery context, not input passed by Listener
to the transcription API.

## Primary OpenAI documentation

OpenAI's speech-to-text guide says prompts can improve recognition of names,
acronyms, formatting, punctuation, capitalization, and filler words, and the
API reference describes `prompt` as optional text guiding style or continuation
of a previous segment. The reference says `gpt-4o-transcribe` accepts only JSON
response format. Neither source documents Java/comment-line insertion or
guarantees that a prompt produces a particular formatting style.

## Assessment

- **Supported claim:** neither the current Listener vocabulary/prompt source
  nor independent authored psyche/code records invite the specific Java/comment
  contamination. The prompt's broad formatting/style affordance is documented,
  but it is not a Java/comment instruction.
- **Hypothesis only:** model-side formatting behavior could be involved because
  OpenAI documents prompt influence over formatting; this does not explain the
  exact duplication or 94 prefixes.
- **Unknown:** the prompt sent for capture 530 is not stored; the audio was not
  independently transcribed/listened to; no evidence identifies whether the
  Java/comment text entered during model transcription, audio content, a
  transport/copy layer, or later rendering/input handling.

## Sources

- Listener source: `/git/github.com/LiGoldragon/listener/src/transcription.rs`.
- Listener deployment: `/nix/store/gypwa5kfnv4fy78l0l8wxdbk0jk1y2wb-listener-0.14.0/bin/.listener-daemon-wrapped`, process 3296598.
- Event witness: `flows/01a0439e/witnesses/listenerTranscriptEvent.md`.
- Psyche/code context: `psyche-raw/Vision/mainFunction.md`,
  `flows/2b34fafa/vision/protosIsTheSharedStyle.md`,
  `flows/b675f3d9/vision/structuralParsing.md`,
  `flows/aa4c7747/vision/ethos.md`.
- OpenAI [speech-to-text prompting guide](https://developers.openai.com/api/docs/guides/speech-to-text#prompting)
  and [Create transcription API reference](https://developers.openai.com/api/reference/python/resources/audio/subresources/transcriptions/methods/create).
