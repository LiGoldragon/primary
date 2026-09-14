# Relay

## 2026-09-13 — Relay the prompt by matching a few characters in the transcript, not by re-emitting it

Context: the flow had been retyping the living's words into the relay as output tokens.

> Right now, are you copying all my verbatim in your own output tokens instead of running a script that gets, let's say, a short command that has just a few words at the beginning and at the end? A bit of the first part of the string and the end of the string of what the prompt was verbatim. It could even just be 6 characters, it doesn't even matter, or 12, whatever.
>
> Instead of having to make all the output tokens, just this service, or whatever the script would, get the last user prompt, search for that match in the transcript, and send it as a message. It would be way more efficient. I don't know, I just think it is a fix to your hack, basically.

-- psyche, STT.

## 2026-09-14 — Six characters each end is enough; the tool lives outside the flow directory

> You should make that tool. You don't need so many words, so many characters at the beginning and the end. I said 6, and you used like 60 or something, so 12 will be enough because the script should only search user prompt input. There are not going to be that many matches, and you should put that tool somewhere other than in the Flow ID directory.

-- psyche, STT.
