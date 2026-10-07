# Vision and Intent to skills — receipt

Subflow of d4ae97, 2026-10-07.

## Source file to skill

Line counts: source file lines, then the skill's lines (frontmatter and
Sources section included). Every non-blank source line and every
sources/ line was checked present, in order, in its skill: 0 missing.
The leading `# Title` line is dropped (the skill name carries it), except
in the archive file, where the retirement note precedes it.

| Source | Skill | Source lines | Skill lines |
|---|---|---|---|
| Vision/archive-ethosMonolith.md (+ sources/ethosMonolith.md) | vision-archive-ethos-monolith | 48 | 59 |
| Vision/committing.md | vision-committing | 9 | 17 |
| Vision/datom.md | vision-datom | 315 | 369 |
| Vision/deployment.md | vision-deployment | 11 | 20 |
| Vision/distillation.md | vision-distillation | 41 | 51 |
| Vision/ethos.md | vision-ethos (merged) | 448 | 510 |
| Vision/flowNexus.md | vision-flow (merged) | 59 | 85 |
| Vision/highLevelView.md | vision-high-level-view | 10 | 18 |
| Vision/horizon.md | vision-horizon | 15 | 23 |
| Vision/meaning.md | vision-meaning | 80 | 95 |
| Vision/messaging.md | vision-messaging | 30 | 42 |
| Vision/modelRoles.md | vision-model-roles | 103 | 117 |
| Vision/nexus.md | vision-nexus (merged) | 178 | 218 |
| Vision/orchestrate.md | vision-orchestrate | 12 | 20 |
| Vision/protos.md | vision-protos | 150 | 186 |
| Vision/psyche.md | vision-psyche | 26 | 25 |
| Vision/remembering.md | vision-remembering | 17 | 24 |
| Vision/sema.md | vision-sema | 15 | 26 |
| Vision/signal.md | vision-signal | 43 | 56 |
| Vision/x11.md | vision-x11 | 3 | 6 |
| Intent/anatomy.md | intent-anatomy | 7 | 14 |
| Intent/context.md | intent-context | 6 | 14 |
| Intent/conversion.md | intent-conversion | 8 | 16 |
| Intent/data.md | intent-data | 22 | 25 |
| Intent/mandatoryTraits.md | intent-mandatory-traits | 15 | 18 |
| Intent/models.md | intent-models | 15 | 23 |
| Intent/protosParsing.md | intent-protos-parsing | 23 | 26 |
| Intent/psycheInteraction.md | intent-psyche-interaction | 5 | 12 |
| Intent/startupPrompt.md | intent-startup-prompt | 5 | 12 |
| Intent/testing.md | intent-testing | 9 | 17 |

Provenance: each Vision/sources/<topic>.md and Intent/sources/<topic>.md
is the skill's closing `## Sources` section, lines unchanged. Intent/data.md
and Intent/protosParsing.md carried their provenance after a `---` rule; that
text is now their Sources section (no horizontal rule). Vision/psyche.md,
Vision/x11.md, Intent/mandatoryTraits.md had no sources file.

Choices to review:

- Vision/flowNexus.md merged into the existing vision-flow, not a new
  vision-flow-nexus: knowledge-flow and knowledge-layer-models depend on
  vision-flow by name.
- vision-psyche: the `operational-`/`testing-` prefix paragraph is cut.
- Merges kept the old skill's statements Vision lacked, placed under the
  nearest Vision heading. Dropped as already stated by Vision: in
  vision-ethos the "schema language… one swoop", "specifies types; datom
  fills", "repetition is failure", "no version; manifest", "kind is
  qualifier-named", "no generics, a constraint is a kind" sentences and
  the old Flow Nexus four-root example (Vision/nexus.md "Three parts and
  one path" now carries the authoritative example); in vision-nexus the
  opening "long-running whole" paragraph, the start-with-no-arguments and
  speaks-only-its-contracts sentences, the ordinary/meta socket sentence,
  the CLI-is-bootstrap sentence, subscription/polling/one-domain
  sentences, and the "four ethos files in vision-ethos are the example"
  pointer; in vision-flow the launch, refresh-reaps and whole subflow
  paragraph.
- Tension left standing, not resolved: vision-ethos "Roots" (Vision text)
  says "Library, Signal, Sema"; the kept skill line says "Four roots:
  Library, Signal, Operation, Memory", as does vision-nexus "Three parts".
  Wants a distillation ruling.

## Gold-skill lines, removed (-) and added (+), verbatim

```
+++ b/skills/compensation-book-distillation.md
-Work moves forward through distillation: a book carries the raw records it would distil into a named Vision, Intent or skill file, as that file's new lines.
+Work moves forward through distillation: a book carries the raw records it would distil into a named skill, as that skill's new lines.
+++ b/skills/psyche-distillation.md
-statement stands on its own words. Every distillation refers to the raw psyche it was distilled from: the references sit in the topic's sources file, `Vision/sources/<topic>.md`, one line per reference — the originating flow's short id and the record file's topic, `e06e4c07 nexus` (`vision-raw <topic>` for a vision-raw record) — appended after every distillation, so the original words are easily found. The path is reconstructed from the line; since distillation moves the record into the archive, the line resolves to the `archive-` file. The archived
+statement stands on its own words. Every distillation refers to the raw psyche it was distilled from: the references sit in the skill's Sources section, one line per reference — the originating flow's short id and the record file's topic, `e06e4c07 nexus` (`vision-raw <topic>` for a vision-raw record) — appended after every distillation, so the original words are easily found. The path is reconstructed from the line; since distillation moves the record into the archive, the line resolves to the `archive-` file. The archived
-A distilled statement lands in `Vision/<topic>.md` on the
-living's explicit approval, and never before. A ruling a
-distillation lands in Vision is not also logged as raw vision;
-the landing is the record. Intent enters
-`Intent/` only on the living's explicit word. The raw records a
+A distilled statement lands as lines in a vision-, intent- or
+other skill's authored source on the living's explicit approval,
+and never before. A ruling a distillation lands in a skill is not
+also logged as raw vision; the landing is the record. Intent enters
+an intent- skill only on the living's explicit word. The raw records a
-for every statement, the Vision topic it lands in; a statement in the
+for every statement, the skill it lands in; a statement in the
+++ b/skills/psyche-interraction.md
-A statement enters `Vision/` only as a distillation the living
+A statement enters a vision- skill only as a distillation the living
+++ b/skills/psyche.md
-  heard before flows, draining into `Vision/` as distillation
+  heard before flows, draining into vision skills as distillation
+++ b/skills/skill-designing.md
-A skill's kind says who stands behind it.
-A gold skill carries no prefix. It is the living's vision of the desired result, approved by the living, and changes only on the living's word.
+A skill's kind says who stands behind it, and is its prefix: `vision-`, `intent-`, `knowledge-`, `operation-`, `trial-` or `compensation-`.
+A `vision-` or `intent-` skill is gold: the living's approved words, changed only on the living's word.
+A `knowledge-` skill states what is deployed and true today, written by flows from what they have read and verified.
+Compensation and trial skills are machine-authored without the living in the loop, refined as they are used and reviewed, and upgraded into operation, knowledge, vision or intent skills.
```

psyche-interraction and compensation-book-distillation (body line 5, on
the coordinator's word) were added to the write set: both still pointed
at Vision/ or Intent/. In Primary, the same psyche search line was
changed in CLAUDE.md, AGENTS.md and NON_MANAGEMENT_AGENTS.md:

```
-have spoken on, search `Vision/`, `vision-raw/`, and `flows/*/vision/` before assuming.
+have spoken on, search the vision- and intent- skills, `vision-raw/`, and `flows/*/vision/` before assuming.
```

## Unprefixed skills, for the next pass

Proposed prefix per the six kinds; not renamed here.

| Skill | Proposed |
|---|---|
| agent-harness-packaging | operation- |
| beads | operation- |
| behavior | conduct rule, stays as is |
| breaking-upgrades | operation- |
| claude-harness | knowledge- |
| codex-harness | knowledge- |
| context-strata | vision- |
| correction | conduct rule, stays as is |
| datom | knowledge- |
| design | role skill (user-only); operation-, or ruling |
| disk-hygiene | operation- |
| documentation-placement | operation- |
| edit-coordination | operation- |
| feature-development | operation- |
| file-editing | operation- |
| flow-evidence | operation- |
| lojix | knowledge- |
| main-flow | role skill (user-only); operation-, or ruling |
| nix-input-upgrade | operation- |
| nix-workflow | operation- |
| operating-system | operation- |
| orchestrate | knowledge- |
| prompt-crafting | operation- |
| protos | knowledge- |
| psyche | vision- (gold; beside vision-psyche) |
| psyche-acquisition | operation- |
| psyche-distillation | vision- (gold) |
| psyche-grasp | operation- |
| psyche-interraction | vision- (gold) |
| realization | role skill (user-only); operation-, or ruling |
| repository-lifecycle | operation- |
| secrets | operation- |
| skill-designing | vision- (gold) |
| spirit | none of the six: spirit stands above intent; ruling needed |
| stale-lock | operation- |
| testing | operation- |
| transcript-search | operation- |
| versioning | operation- |
| vocabulary | conduct rule, stays as is |

## Commits (not pushed)

- Curriculum b7785457: "Vision and Intent become vision- and intent- skills; six skill kinds as prefixes".
- Primary 6a3db7a94: "Vision: ethos and messaging lines found uncommitted in the tree".
- Primary 1faf3230c: "OpenCode skill projections found uncommitted in the tree".
- Primary, next commit: "d4ae97: Vision and Intent moved into skills; trees regenerated" (Vision/ and Intent/ removed, entry-file lines, regenerated .claude, .agents, .opencode trees, this receipt).

## Generation and check

`nix run .#generate-skills -- 'Generate.{ «/git/github.com/LiGoldragon/Curriculum» [ Psyche.«/git/github.com/LiGoldragon/Curriculum/skills» ] «/home/li/primary» }'` → `Generated.{ 99 24 }`.
`nix run .#check-skills -- 'Check.{ … same … }'` → `Checked.{ 99 24 }`, exit 0, first run.
flake.nix still pins Curriculum cdf1d43f; the pin moves when b7785457 is pushed.
