<!-- to-the-living:start -->
Presentation.{ «Sources in the commit message» }

# Sources in the commit message

A vision skill today ends with a list like this:

```
## Sources

058f16 source
081064 ethos
```

Each line points to a raw record that the skill's statements were distilled from: the flow that heard it, and the record's topic. Its one use is to let someone find your original words in the archive. Nothing reads these lines automatically; they are only read by hand. Because the list sits inside the skill, every flow that loads the skill loads it too.

This edition puts each reference in the message of the commit that lands the distillation. The commit history keeps every reference, and `git log` on the skill file finds them.

## Distillation

### Proposal 1: the rule, in operation-psyche-distillation

File: `mind-skills/skills/operation-psyche-distillation.md`. The changed sentence follows "A distilled statement stands on its own words." and comes before "The archived originals keep every original word."

Removed:

Every distillation refers to the raw psyche it was distilled from: the references sit in the skill's Sources section, one line per reference — the originating flow's short id and the record file's topic, `e06e4c07 nexus` (`vision-raw <topic>` for a vision-raw record) — appended after every distillation, so the original words are easily found. The path is reconstructed from the line; since distillation moves the record into the archive, the line resolves to the `archive-` file.

Added:

Every distillation refers to the raw psyche it was distilled from, in the message of the commit that lands it and never in a skill: one line per reference, the originating flow's short id and the record file's topic, `e06e4c07 nexus` (`vision-raw <topic>` for a vision-raw record). Since distillation moves the record into the archive, the line resolves to the `archive-` file.

Ruling 1: does this replacement stand?

### Proposal 2: remove the existing lists

Every `## Sources` section in `psyche-skills/skills/*.md` and `psyche-skills/vision/*.md` is deleted, in one commit. That commit's message carries each removed list under its skill's name, so no reference is lost. For example, the end of `psyche-skills/skills/vision-distillation.md`:

```diff
- ## Sources
-
- b675f3d9 visionImpurities
- acbb6006 distillation
- b675f3d9 distillation
- ac1e9ec8 distillationNegatives
```

and the commit message carries:

```
vision-distillation
b675f3d9 visionImpurities
acbb6006 distillation
b675f3d9 distillation
ac1e9ec8 distillationNegatives
```

Ruling 2: remove every existing list this way?
<!-- to-the-living:end -->
