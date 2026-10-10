<!-- to-the-living:start -->
Presentation.{ «Three skill repositories and the main workspace» }

```
 psyche-skills    mind-skills     field-skills
   vision-          knowledge-      compensation-
   intent-          operation-      trial-
   spirit
       └───────────────┼───────────────┘
                the main workspace
          mounts them and the psyche data
```

The three repositories are in production and hold
every skill by its kind. The main workspace that
mounts them is designed, not built. vision-psyche
still describes the older single-repository
shape; the lines below bring it to this one.

## 1. Three skill repositories

`psyche-skills/skills/vision-psyche.md`, lines 21 and 22, and a Sources section at the end. Removed lines are wrapped at 52 characters.

```diff
@@ lines 21-22 @@
- The skills belong in a repository. This is a
- target shape, not authorization to
- create or migrate a repository (native desktop
- record, archive ordinal 1835).
+ The skills belong in three repositories, psyche,
+ mind and field, each holding the skills of its
+ own types. A text whose parts belong to different
+ aspects is split, each part to its home.
@@ end of file @@
+
+ ## Sources
+
+ bad807 skills
```

Distils flows/bad807/vision/skills.md, 2026-10-04.

**Ruling 1.** (a) Land as shown. (b) Land as shown, keeping its second sentence, on authorization. (c) Amend by line.

## 2. The main workspace

`psyche-skills/skills/vision-psyche.md`, lines 16 to 19, and one line under Sources. Removed lines are wrapped at 52 characters.

```diff
@@ lines 16-19 @@
- Psyche data belongs in a dedicated repository
- symlinked into Primary. Primary
- Next begins from Primary's root commit and
- carries selected repository mounting
- points plus a README and AGENTS.md explaining
- those relationships. Orchestrate
- coordinates concurrent work across those
- repositories.
+ Psyche data belongs in a dedicated repository
+ symlinked into the main workspace. The main
+ workspace begins from Primary's root commit and
+ carries selected repository mounting points
+ plus a README and AGENTS.md explaining those
+ relationships. The three skill repositories are
+ bootstrapped on it. Orchestrate coordinates
+ concurrent work across those repositories.
@@ Sources @@
+ bad807 workspace
```

Distils flows/bad807/vision/workspace.md, 2026-10-04. That the main workspace is the Primary Next of lines 16 and 17 is this flow's reading.

**Ruling 2.** (a) Land as shown. (b) Keep the name Primary Next and add only the bootstrap sentence. (c) Amend by line.

## 3. Vision is gold

`psyche-skills/skills/vision-psyche.md`, lines 8 and 9. Removed lines are wrapped at 52 characters.

```diff
@@ lines 8-9 @@
- Psyche reaches through its hierarchy to
- Orchestrate coordinates. Unprefixed
- vision is Psyche's most reliable, accepted gold.
+ Psyche reaches through its hierarchy to
+ Orchestrate coordinates. Vision is Psyche's most
+ reliable, accepted gold.
```

Follows the kind prefixes of mind-skills/skills/operation-skill-designing.md, line 55.

**Ruling 3.** (a) Land as shown. (b) Keep the line as it stands.

<!-- to-the-living:end -->
