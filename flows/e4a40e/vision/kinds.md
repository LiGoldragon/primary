# Kinds

## 2026-09-03 — two heads differing in a required kind are two kinds

The flow asked whether `Processable<[Clonable] Serializable>` and
`Processable<[Sendable] Serializable>` would be two kinds, or one, as
Rust makes them one trait.

> Yes, obviously those would be two kinds [STT: too kind]. I don't know, why did you have to ask me that? Wasn't that obvious? Why is that ambiguous? I'm really curious.

-- psyche, STT.
