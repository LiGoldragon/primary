# Operational: messages as Datom objects through the messenger, differentiating psyche from agent input

## We need to pass it through a messenger system. It starts with a variant and then a delimiter, a struct or vector. When the psyche types, he just types normally. We need to implement the proper nexus that uses specified messages

Context: artifact comment by the living on the Vision Dependencies report,
2026-09-18, on the "Turn-end hook" dependency. The living names the message
format: a Datom object starting with a variant head, then a delimiter (struct
or vector depending on message type). Agent messages come through the messenger
system in this format; the psyche types normally (keyboard or Wispr Flow STT).
The distinction between psyche typing and agent messaging is what the messenger
must make easy to recognize. A proper nexus with specified message types is
owed. The living also notes Wispr Flow's STT formatting (removing repetitions,
structuring, bullet points) and asks whether that helps or hinders. Logged by
the main flow before acting.

> Yeah, I wasn't specifically thinking about this, but yes, some kind of flow that monitors what the living says with a hook when the flow ends. We need to make it easy to differentiate between when the psyche is typing and when he's not. Any kind of messaging: that's why we need to pass it through a messenger system. It is going to need to create a certain syntax. Like I was saying, we put it in a Datom object, so it starts with a variant and then a delimiter, which is probably going to be a struct or a vector, right? Depending on the type of messages we want to have and all that, we need to implement the proper nexus that uses specified messages.
>
> Let's get that going so that we can check when a message is from another agent. It could contain psyche, but when the psyche types, he just types normally, like with a keyboard or speech-to-text. That comes in as just a block of text. Wispr Flow is used now mostly for speech-to-text, so it does its own style of formatting and correcting: taking out the repetitions and the hesitations, structuring, and making bullet points and all that. Wispr Flow does that. I don't know if that's good or detrimental. Maybe somebody can comment on it.

-- psyche, artifact comment on Vision Dependencies report.
