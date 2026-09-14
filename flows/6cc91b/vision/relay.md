# Relay

## 2026-09-13 — Relay the prompt by matching a few characters in the transcript, not by re-emitting it

Context: the flow had been retyping the living's words into the relay as output tokens.

> Right now, are you copying all my verbatim in your own output tokens instead of running a script that gets, let's say, a short command that has just a few words at the beginning and at the end? A bit of the first part of the string and the end of the string of what the prompt was verbatim. It could even just be 6 characters, it doesn't even matter, or 12, whatever.
>
> Instead of having to make all the output tokens, just this service, or whatever the script would, get the last user prompt, search for that match in the transcript, and send it as a message. It would be way more efficient. I don't know, I just think it is a fix to your hack, basically.

-- psyche, STT.
