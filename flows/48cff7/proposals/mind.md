# proposal · mind

*Flow 48cff7 · 2026-09-16 · pending living review*
*Kind: new skill*
*Source records: flows/48cff7/vision/mind.md*

---

## description

A fact about the system, tools, models, or the world must be recorded or looked up with its date and how much it is trusted.

## body

Facts live in the mind. A record carries what the fact asserts, the date it entered, a trust variant, its evidence, and its subject. Trust variants: `Verified` — round-tripped through a check; `Attested` — a trusted source said so; `Provisional` — inferred, needs check; `Deprecated` — superseded, kept for history.

A skill describes mechanics only. A fact it would assert is a mind reference instead. The psyche records what the living has said; the mind records what the system knows to be true.

The mind is a Nexus: `mind-nexus` binary, ordinary and meta sockets, sema store, Signal wire, `mind` and `mind-meta` CLIs each taking one inline datom. Until it runs, a fact belongs in a psyche entry marked "provisional pending mind."

Queries go by subject, trust level, date range, or evidence origin.
