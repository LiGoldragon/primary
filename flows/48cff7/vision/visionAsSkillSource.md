# visionAsSkillSource

## 2026-09-16 — a vision file for a subject is the source; its sections generate the skill kinds

Context: after the diff-viz refinement, the living named the anatomy — each vision file (per subject) is broken into named sections, one of which is the *core* that becomes the primary skill body, the others generating the derivative kinds already named in `skillKindsTaxonomy.md`.

> These vision repositories, which are represented by files now, are sort of main big types, which I guess now are becoming the source for skills. If we can do this right, we can do that, which are broken up into sections. Look at vision as a core, a basic, core, most important, blah, blah, blah, and then that's the main skill that gets created. You can create any number of other main sections, but there are a few that are sort of suggested.
>
> In the scale on how to do this, until we do this fully typed in the psyche database, that basically becomes the anatomy for that.

-- psyche, typed.

## The suggested sections

For a vision subject `<S>`, its file `Vision/<S>.md` (or `flows/<flow>/vision/<S>.md` raw) is broken into sections. Each section is one kind of material. The Curriculum-nexus (proposed) reads the sections and generates the deterministic-named skill files.

Suggested sections:

- **Core** — the imperative, minimal, most-important statement. Generates `<S>.md` (skill body).
- **Rationale** — the why, the concepts, the context. Generates `<S>-rationale.md`.
- **Extended** — the broader domain view for readers who want more than the action. Generates `<S>-extended.md`.
- **Experimental** — in-flight material being tried; not standing. Generates `<S>-experimental.md`.
- **Undecided proposal** — drafts awaiting the living's word. Generates `<S>-undecided-proposal.md`.
- **Raw records** — verbatim living quotes and their surrounding context. Not generated to a skill; kept in the vision file.
- **Open questions** — questions the vision itself carries. Not generated to a skill; kept in the vision file.

Any number of ad hoc sections are allowed. The above are the ones the taxonomy suggests today. A section unknown to the Curriculum-nexus generator is preserved verbatim in the vision file and does not emit a derivative.

## Until the psyche is fully typed in a database

The living's phrase: "until we do this fully typed in the psyche database, that basically becomes the anatomy for that." The vision-file-with-sections shape *is* the anatomy of a psyche subject until the typed store runs. When the store runs (per `flows/48cff7/vision/mind.md` and the proposed `curriculum-nexus`), the same section names become the typed positional fields on a Vision record — the Ethos anatomy for the signal.

That anatomy is drafted at `flows/48cff7/proposals/signal-curriculum.md` as a candidate signal vocabulary Codex can turn into `signal-curriculum` and `meta-signal-curriculum` Ethos wire type repos.

## Open questions worth the living's word

1. Confirm the seven suggested sections (Core, Rationale, Extended, Experimental, UndecidedProposal, RawRecords, OpenQuestions), or edit / cut / add.
2. Whether ad hoc named sections are first-class in the signal vocabulary (a `Custom.{ name  content }` variant), or preserved only in the file and invisible to the Nexus.
3. Whether the Core section can hold zero content (a vision that is still all rationale / experimental), or is required non-empty for the vision to stand.
4. Whether a section boundary in the file is a Markdown heading level (H2? H3?), a `<!-- section: name -->` marker, or something else.
