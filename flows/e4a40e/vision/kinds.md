# Kinds

## 2026-09-03 — two heads differing in a required kind are two kinds

The flow asked whether `Processable<[Clonable] Serializable>` and
`Processable<[Sendable] Serializable>` would be two kinds, or one, as
Rust makes them one trait.

> Yes, obviously those would be two kinds [STT: too kind]. I don't know, why did you have to ask me that? Wasn't that obvious? Why is that ambiguous? I'm really curious.

-- psyche, STT.

## 2026-09-03 — what identifies a trait in Rust is what identifies a kind in the ethos

The flow had said it had to decide which constraints were outside a
kind's identity.

> You don't have to decide which constraints are not part of an identifier. What identifies a trait in Rust is what identifies a kind in the ethos, because we're compiling the Rust [STT: rest], so we don't have a choice. There's no decision involved here, and we're not going to rewrite the Rust compiler.

-- psyche, STT. (First logged as typed, mode not evident; the living's correction of 2026-09-04, flow ad19b1 kinds, shows it was transcribed and misheard.)
