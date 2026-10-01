# skillSourceKinds

## 2026-09-16 — composed skills become vision automatically; skill kinds are typed by their source layer (vision · mind · usage)

Context: after the signal-curriculum brief left for Codex, the living named the migration direction and the source-typing that follows from it.

> All the current skills become vision automatically, right? Already agreed: vision, like the skills that we've composed, not the skills that are in the harnesses by default, like Codex, but the skills that we've made are curriculum. We'll just treat that as vision, not necessarily vision. It could be mind also if it's just fact, but we'll treat it as vision for now and just move all of this skill system to vision.
>
> The vision layer is what we hook into the skill, and also some of the mind, some of the knowledge. We'll make the vision soon here with the mind component, also throwing in some skills that'll be basically suffixed, right? Knowledge or suffixed, maybe vision. Yeah, there you go. We're going to have types: suffixed usage, which is just how to use something like a tool, with the languages to speak to that. We're going to have these different types of skills that come from different places.

-- psyche, typed.

## The migration

Every skill in `/git/github.com/LiGoldragon/Curriculum/skills/` that we composed becomes a *vision entry* automatically. The harness-default skills (Claude Code base, Codex base, DeepSeek base) do not migrate — they belong to their harnesses. Our composed skills — 44 as of this reading — become the seed vision corpus.

For now, everything migrates to vision even if some entries would sit better in mind (pure fact) or as usage (tool language). The living's word: "treat as vision for now." Later, mind-appropriate entries move to mind and usage-appropriate ones move to usage.

## The source kinds

A skill's *kind* names where its content came from. This is a different axis from the derivative kinds in `flows/48cff7/vision/skillKindsTaxonomy.md` (Core / Rationale / Extended / Experimental / UndecidedProposal): that axis names *sections within one subject*; this one names the *source layer* the subject was drawn from.

- **Vision-derived** — the subject was distilled from psyche vision (or intent, or spirit). This is the current default for our composed skills. Example: `main-flow`, `psyche`, `nexus`, `datom`.
- **Mind-derived** — the subject is a fact set with dates and trust variants. The skill points at the mind for its content. Example candidate: the harness model ontology (`harnessModelOntology.md`) once the mind runs.
- **Usage** — the subject is how to speak a tool's language or drive its interface. Not vision, not fact — a language reference. Example candidate: `datom` (how to speak datom), `transcript-search` (how to drive the transcript CLI), the future `signal-<nexus>` reference skills.

A composed skill is exactly one kind at any moment. Its kind may change over time — a fact-heavy skill migrates from vision to mind when the mind is running; a design skill stays vision.

## Consequences for the Curriculum-nexus and its wire

`flows/48cff7/proposals/signal-curriculum.md` (dispatched to Codex `01a0acb8`) drafts a `curriculum-nexus` whose ordinary-socket ops read *vision subjects* and emit skill derivative files. Under this teaching, the same Nexus must also read *mind subjects* and *usage subjects* and emit skills for them. Three options for the wire vocabulary:

1. **One `Source` variant on every operation** — `Get.{ subject  kind  source: SourceLayer }` where `SourceLayer := Vision | Mind | Usage`. Same wire; the payload names its layer.
2. **Three separate signal repos** — `signal-curriculum` (vision-derived) alongside `signal-mind` and `signal-usage`, with a routing layer above. Cleaner separation, more repos.
3. **Vision as the primary and mind/usage as later peers** — the current signal-curriculum draft covers vision only; mind and usage arrive later as their own Nexuses that peer with it.

The flow reads the living as leaning toward the first (a unified curriculum-nexus with a `SourceLayer` variant), but this is a design decision for the living. Codex has been dispatched on the vision-only shape; the follow-up will extend once the source-kinds axis is settled.

## Migration mechanics (proposed)

For each existing Curriculum skill file `Curriculum/skills/<name>.md`:

1. Read its content.
2. Classify by source kind: vision-derived (design), mind-derived (fact), usage (tool language). Ask the psyche where the answer is unclear.
3. Move its content into a vision subject file (`Vision/<name>.md`) with the composed body as the Core section.
4. The Curriculum-nexus regenerates the skill file from the vision subject — the current `Curriculum/skills/<name>.md` becomes generated evidence.

## Open questions worth the living's word

1. Confirm the three source kinds (Vision · Mind · Usage) or edit the list.
2. Confirm one unified `curriculum-nexus` with a `SourceLayer` variant, or three signal repos.
3. Which of the current 44 Curriculum skills classify as usage today (this flow's guess: `datom`, `transcript-search`, `orchestrate`, `lojix`, `beads`, some of the harness skills' tool interfaces).
4. Whether harness-default skills (Claude Code base instructions, Codex base instructions) are ever migrated to vision, or stay owned by their harnesses.
5. Whether the migration is done flow-by-flow (each skill as its own vision entry, over many sessions) or as a single bulk pass by a dedicated migration flow.
