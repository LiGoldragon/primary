# Interflow messaging

## 2026-09-14 — Up-and-down communication on fences: a lower layer's message arrives as a tool-call return or an asynchronous signal, never as the user prompt

Context: "fences" is the living's reference to Steve Yegge's term. The living asks "What can work best here? Is this just our universal MCP datom ethos spec?"

> Have the up-and-down communication system, even if it's just based on trust on fences, what Steve Yegge calls fences.
>
> Your code is basically your instructions to the agents. It's permissive, but still, because the top layer knows that the third layer doesn't have authority over it, when it gets messaged from that layer, it doesn't treat it as authority. It doesn't come in through the third layer, or I mean, to the middle layer. It doesn't come through the user prompt. It comes in some kind of tool call return that all the agents have running, or some kind of MCP signal that can come in asynchronously. What can work best here? Is this just our universal MCP datom ethos spec? In Interflow messaging format, it's like the different types of messages. If you can have a vector, it's basically just a bunch of messages with different types, and it can probably easily know where that came from. That's not hard to do because we trust the system. We're writing it, we're running it, so we're programming that into our components to do all this.

-- psyche, STT.
