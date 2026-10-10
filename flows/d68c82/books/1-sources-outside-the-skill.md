<!-- to-the-living:start -->
Presentation.{ «Sources outside the skill» }

# Sources outside the skill

A vision skill today ends with a list like this:

```
## Sources

058f16 source
081064 ethos
```

Each line points to a raw record that the skill's statements were distilled from: the flow that heard it, and the record's topic. Its one use is to let someone find your original words in the archive. Nothing reads these lines automatically; they are only read by hand. Because the list sits inside the skill, every flow that loads the skill loads it too.

You asked for something else on 2026-08-27: the references sit in a separate file, one per topic, listing only the sources and appended after every distillation, to make the original statement easy to find. You then cut each line down to the flow id and topic. The distillation skill kept the line format but moved the list into the skill. Today you ruled that this data does not belong in the vision.

The skill generator reads only the `skills/` and `vision/` folders of the psyche skills repository, one level deep. A file at `psyche-skills/sources/<topic>.md` is never part of any generated skill.

## Distillation

### Proposal 1: the rule, in operation-psyche-distillation

File: `mind-skills/skills/operation-psyche-distillation.md`. The changed sentence follows "A distilled statement stands on its own words." and comes before "The archived originals keep every original word."

Removed:

Every distillation refers to the raw psyche it was distilled from: the references sit in the skill's Sources section, one line per reference — the originating flow's short id and the record file's topic, `e06e4c07 nexus` (`vision-raw <topic>` for a vision-raw record) — appended after every distillation, so the original words are easily found. The path is reconstructed from the line; since distillation moves the record into the archive, the line resolves to the `archive-` file.

Added:

Every distillation refers to the raw psyche it was distilled from. The references sit in their own file, one per topic, `psyche-skills/sources/<topic>.md`, and never in a skill. Each line is the originating flow's short id and the record file's topic, `e06e4c07 nexus` (`vision-raw <topic>` for a vision-raw record), appended after every distillation. Since distillation moves the record into the archive, the line resolves to the `archive-` file.

Ruling 1: does this replacement stand?

### Proposal 2: move the existing lists out

Every `## Sources` section in `psyche-skills/skills/*.md` and `psyche-skills/vision/*.md` is removed from the skill. Its lines move unchanged, in the same order, into `psyche-skills/sources/<topic>.md` for the same topic. For example, the end of `psyche-skills/skills/vision-distillation.md`:

```diff
- ## Sources
-
- b675f3d9 visionImpurities
- acbb6006 distillation
- b675f3d9 distillation
- ac1e9ec8 distillationNegatives
```

The new file `psyche-skills/sources/distillation.md`:

```diff
+ b675f3d9 visionImpurities
+ acbb6006 distillation
+ b675f3d9 distillation
+ ac1e9ec8 distillationNegatives
```

The other vision skills follow the same pattern. That includes `vision-book`, whose list is a path and a date; it is rewritten to the id-and-topic form, `445410 books`.

Ruling 2: move every existing list this way?
<!-- to-the-living:end -->
