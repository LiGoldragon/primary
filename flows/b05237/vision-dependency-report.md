# Dependency Report: The Three 09-18 Statements

Date: 2026-09-18
Source: Fable flow c7128c, aggregation subflow (Opus, medium,
two Sonnet read children). Edges verified at source by this report.

## The three new statements

1. **Visualization** — the hook, the slide book, a visualization
   skill, and image cost levels.
2. **Job effort** — "a different model" per job, not a different
   thinking effort; model effort stays medium.
3. **Transcript-as-data** — favor the transcript; the machine flow
   is where data goes.

All three are logged verbatim in `flows/c7128c/vision/`:
`visualization.md`, `jobEffortLevels.md`,
`transcriptAndMachineFlow.md`.

## What Visualization rests on

- **Slide book** (typed, 09-16): biggest model writes Markdown and
  Mermaid; the chart is the flow of the idea.
  Found in `flows/f55ec8/vision/visualPublication.md` and
  `flows/b49251/vision/visualPublication.md`.
- **Scaled SVG, not Mermaid** (artifact comment, 08-31): the
  converting subflow should render properly scaled SVG.
  Found in `flows/f55ec8/vision/visualPublication.md` and
  `flows/995a164e/vision/designPractice.md`. This sits in tension
  with the slide book's own use of Mermaid — unresolved.
- **Turn-end hook** (typed, 09-16): a flow that monitors what the
  living says, with a hook when that flow ends. No dedicated
  vision file located under this exact wording; nearest matches
  are hook records in `flows/6cc91b/vision/messenger.md` and
  `flows/6cc91b/vision/notifications.md`, which are adjacent, not
  identical.
- **Skill is vision** (typed, 09-17): skill and vision are one
  thing; skills get a type at creation.
  Found in `flows/108ab0/vision/operational-skillLagsVisionObservability.md`,
  `flows/9993b5/vision/curriculumNexus.md`, and
  `flows/b49251/vision/systemPrompt.md`.
- **Report format** (09-18): a report is Markdown plus flowcharts;
  illustrations go to the illustrator in prose.
  Found in `flows/b05237/vision/operational-reportFormat.md`.
- **Power level** (typed, 09-17): power level is literally how much
  energy is spent.
  Found in `flows/9993b5/vision/powerLevels.md`.

## What Job effort rests on

- **Restates** the two-scales-share-high-and-medium record (09-18):
  harness effort is always medium.
  Found in `flows/1ac573/vision/operational-effortIsAlwaysMedium.md`
  and `flows/1ac573/vision/operational-defaultModelPsycheMediumClaude.md`.
- **Depends on** three roles per stack, all medium (~09-08).
  Nearest match: `flows/5851f4/vision/subagents.md`. Wording is
  close but not identical to "three roles per stack" — treat as a
  paraphrase, not a verbatim source.
- **Supersedes** "high effort is a waste, medium mode for now"
  (STT, 09-13). Nearest matches:
  `flows/024bc7/vision/effort.md` and
  `flows/6852f4/vision/communication.md`. Neither is an exact
  verbatim hit; this edge is the weakest-verified of the set.

## What Transcript-as-data rests on

- **Depends on** "the report is just the last response; logs are
  references to transcripts" (09-18).
  Found in `flows/b05237/vision/operational-reportIsTranscript.md`
  and `flows/9993b5/vision/transcriptArchive.md`.
- **Depends on** the idea flow's presentation of the machine flow
  and the psyche flow (typed, 09-16).
  Found in `flows/c7128c/vision/transcriptAndMachineFlow.md` and
  `flows/b49251/vision/visualPublication.md`.
- **Tension with** "what is a report but hearsay put into a file"
  (STT, 09-05). Found in
  `flows/78c93c/vision/witnesses-and-reports.md`. This is a live
  disagreement, not a resolved dependency — noted, not settled.

## Unapproved proposals underneath these edges

- **Idea-book decks and index** — flows `f55ec8` and `b49251`,
  proposes the slide-book pipeline the Visualization statement
  draws on. Unapproved.
- **Fresh vision review** — flow `1ac573`, proposes the
  effort-scale record the Job effort statement restates.
  Unapproved.
- **Distillation proposal** — flow `f55ec8`, 09-17, spans 23
  topics; underlies the general expectation that flow-local vision
  gets pulled forward. Unapproved.

## Not yet distilled into Vision/ or Intent/

None of the source records above live in the top-level `Vision/`
or `Intent/` trees. Checked directly: neither tree has any file on
hooks, slide books, power levels, skill-as-vision, effort scales,
or transcript-as-log. Every dependency here is either:

- a flow-local vision record under `flows/*/vision/`, or
- a raw typed/STT statement not yet written into any vision file.

So all three 09-18 statements rest entirely on undistilled
material. Nothing in this graph has cleared the bar into the
shared corpus.

## Weak or unresolved edges

- Turn-end hook: no exact-wording source file found.
- Three-roles-per-stack: nearest match is a paraphrase.
- High-effort-is-a-waste: two partial matches, no verbatim hit.
- SVG vs Mermaid: the slide book and the 08-31 ruling contradict
  each other on which one gets used.
- Hearsay-in-a-file: still an open tension with the transcript
  statement, not a settled dependency.

## Forks left to the living (from Fable's report)

1. Which report style — the generated skill's palette, or the
   09-16 idea-book decks' palette? No record picks one.
2. Mermaid or SVG in the rendered book — the 08-31 ruling says SVG,
   the slide book assumes Mermaid.
3. Where images and slide books live once files are deprecated.
4. Which flows get the turn-end hook, and does Codex get one.
5. Which model renders images at each cost level.
