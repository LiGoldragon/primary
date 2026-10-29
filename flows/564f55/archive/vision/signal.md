# signal

## 2026-09-09 — can Signal, the rkyv zero-copy memory-readable binary, be wedged in as a layer between the concept and the in-memory value

Thinking out loud, while naming the layers of the datom conversion chain:

> Can we wedge in the concept of Signal here, which is rkyv, the zero-copy, memory-readable binary type that we use for Signal, and somehow this is the Signal layer? Maybe we need the Signal layer between the actual layer. ... Maybe we need another layer, the Signal layer, between the concept and the in-memory rest value.

-- psyche, STT.

## 2026-09-09 — the Nexus component never textualizes; only the CLI and the client do; the same signal library derives the datom kinds when compiled for the CLI and nothing of textualization when compiled for the Nexus

> Actually, I just thought of something. The Nexus component is not going to do the textualization at all. That's only in the CLI and the client. I think, depending on what the type is being compiled for, it would derive different things, or that part of the derive would be optional. When the CLI uses the signal library, it would derive Datomizable and composable, but when the Nexus compiles the same signal library, it would compile it without any of the textualization capability.

-- psyche, STT.
