# mind

## 2026-09-16 — the mind stores trustworthy information with a date and a trustworthiness gauge; distinct from the psyche

Context: after this flow drafted a model-and-persona ontology as a proposed addition to the harness skills (`flows/48cff7/vision/harnessModelOntology.md`), the living named the component such information actually belongs in.

> You should have a way to query for verified knowledge, and I think that's what the mind component is. The psyche is for storing psyche, and the mind is for storing trustworthy information with a date and a trustworthiness kind of gauge.

-- psyche, typed.

Flow reading, not the living's words:

- **Psyche** stores the living's expressed thought — raw records, distilled Vision, distilled Intent. It is *what the living has said and what stands from it*. Not fact-checked; trusted because it came from the living.
- **Mind** stores verified knowledge — facts about the world, the system, the models, the tools. Every record carries a **date** (when the fact was established) and a **trustworthiness gauge** (how confident we are in it, and by what evidence). It is *what the system knows to be true*.
- The two are queried differently: psyche by topic and by verbatim search; mind by fact and by trust level.

Consequences for prior drafts, if the living accepts:

- The **harness model ontology** this flow just proposed as an addition to `claude-harness` / `codex-harness` skills is mind material, not skill material. The harness skills describe *how the harness works*; the mind holds *which model runs where, at what trust level, dated when*.
- The `harnessModelOntology.md` entry stays as a **psyche record of the living's teaching about naming and tiers**, but the *authoritative facts* — Fable 5.1 is `claude-fable-5-1`; Luna is `gpt-5.6-luna`; the Astra-to-model mapping — belong in the mind once it exists.
- The proposed skill additions from that entry are re-shaped: harness skills carry the mechanics and point at the mind for the fact table.

## Shape (proposed — the living settles)

A `mind-nexus`, alongside `transcript-nexus` and `psyche-nexus` (also proposed by extension), each a Nexus in the sense of the loaded `nexus` skill: long-running binary, two sockets, sema store, Signal-only wire, datom-at-CLI-boundary.

Record shape, in ethos-typed sketch:

- **fact**: what the fact asserts, in domain vocabulary
- **date established**: when this fact entered the mind, and (if different) when the world-fact it names became true
- **trust**: an enum — `Verified` (round-tripped through a check) · `Attested` (a trusted source said so) · `Provisional` (inferred, needs check) · `Deprecated` (superseded, kept for history)
- **evidence**: pointers to what supports it (transcript block, git commit, a psyche entry, a running test)
- **subject**: the domain the fact belongs to (models, harnesses, network, etc.)

Queries: by subject, by trust level, by date range, by evidence origin.

## Open questions worth the living's word

1. Confirm the mind is its own Nexus, or whether it piggybacks on an existing one.
2. What the trust enum's exact variants are — `Verified / Attested / Provisional / Deprecated` is my sketch; the living may cut or add.
3. Whether the mind stores only atomic facts, or also compound assertions (e.g. "Fable is Anthropic's top-tier orchestrator" as one record) — the atomic-fact form is easier to gauge, the compound form is easier to read.
4. Whether every skill that today asserts a fact ("Fable is the Claude Code main flow model") should stop asserting it and reference the mind instead.
