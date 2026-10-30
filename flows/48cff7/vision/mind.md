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

## 2026-09-16 (later same day) — the interim shape is a folder per trust variant, like the psyche's

Refined in the artifact comment thread `6bab0b72` on the mind artifact (`https://claude.ai/code/artifact/e31893f6-4c7e-4736-bcbf-74d7131cd177`).

> Just make a folder for each type of mind type there are, like we do with the psyche, the vision, and all that. Let each flow just record their own in files, just like we do with psyche, but they're not psyche: they're variants of the mind types, so:
> - verified
> - attested
> - professional
> - deprecated
>
> Does that make sense? Even a single file, verified.md, that agents can add to, or if it's the same flow, they can edit it or whatever.

-- psyche, typed. "professional" is left as transcribed; the flow reads "provisional" — the third trust variant this entry already carries.

Flow reading, not the living's words: until the mind-nexus runs, mind records live on the filesystem in the same shape the psyche uses. Four folders at the top level, or four files each collecting records of that trust variant. Each flow writes into its own file under the relevant folder (or into a shared per-variant file), matching how `flows/<flow>/vision/<topic>.md` works today.

This does not contradict the Nexus target shape recorded above: the folder-per-variant is the *pre-Nexus* form. When the `mind-nexus` runs, its sema store subsumes these files; the variant folders become variant tags on typed records inside the store.
