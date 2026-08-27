Renamed "Nexus Kernel" to "Nexus Core" in all authored skill sources, per the psyche's 2026-08-19 naming ("NexusCore… the heart of this nexus; where all the decision-making happens") ruled living on 2026-08-27 in flows/acbb6006/vision/nexus.md.

Two authored files held the old name. Both were updated with a literal substitution, sentences otherwise unchanged. Consumer trees (.claude/skills/ and .agents/skills/) were refreshed by copying the updated authored files.

## Sources

Curriculum repo commit: 6dc67e3529a3 — "flow acbb6006: Nexus Kernel → Nexus Core (psyche ruling 2026-08-27)"
Files changed in Curriculum:
  /git/github.com/LiGoldragon/Curriculum/skills/nexus.md
  /git/github.com/LiGoldragon/Curriculum/skills/nexus-rationale.md

Primary repo commit: recorded in this flow's skill-update commit (see log).
Files changed in primary consumer trees:
  /home/li/primary/.claude/skills/nexus/SKILL.md
  /home/li/primary/.agents/skills/nexus/SKILL.md
  /home/li/primary/.claude/skills/nexus-rationale/SKILL.md
  /home/li/primary/.agents/skills/nexus-rationale/SKILL.md

Ruling source: flows/acbb6006/vision/nexus.md

## Coordinator verifications (2026-08-27)

### 1. Regeneration mechanism

The regeneration mechanism is `nix run /home/li/primary#generate-skills -- "CurriculumRequest.{Generate.{/git/github.com/LiGoldragon/Curriculum /home/li/primary}}"`. It calls `curriculum-deploy` (pinned in flake.nix at `github:LiGoldragon/curriculum-deploy/ef35a6dc`) with a local Curriculum path. The generator produced `Generated.{36 27}` and left no changes in the working copy (`jj status` clean), confirming the files I copied are byte-for-byte identical to what the generator produces. There is no .codex/ or .pi/ consumer tree in primary; only .claude/ and .agents/ are generated here.

### 2. Files in commit 559c7901

Commit 559c7901 ("found: uncommitted flow and vision changes") contained 26 files across three categories:

Skill files (my changes, swept in because they were already dirty):
  .agents/skills/nexus/SKILL.md
  .agents/skills/nexus-rationale/SKILL.md
  .claude/skills/nexus/SKILL.md
  .claude/skills/nexus-rationale/SKILL.md

Flow acbb6006 files (parent flow, pre-existing dirty):
  flows/acbb6006/reports/distillProposalNexusRevision2.md (new)
  flows/acbb6006/reports/distillProposalProtosDatomAddendum.md (modified)
  flows/acbb6006/reports/distillProposalPsycheProcess.md (modified)
  flows/acbb6006/vision/distillation.md (new)
  flows/acbb6006/vision/nexus.md (new)
  flows/index.md (modified)

Shared Vision files (parent flow, pre-existing dirty):
  Vision/ethosMonolith.md (modified)
  Vision/flowNexus.md (new)
  Vision/nexus.md (new)
  Vision/orchestrate.md (new)

Flow 04db2fd2 files (different flow, pre-existing dirty):
  flows/04db2fd2/log.md
  flows/04db2fd2/reports/anatomyFirstPrinciples.md
  flows/04db2fd2/reports/psycheLoggingProposal.md
  flows/04db2fd2/reports/rollingDistillationProposal.md
  flows/04db2fd2/reports/textPositionRepresentations.md
  flows/04db2fd2/vision/anatomy.md
  flows/04db2fd2/vision/datomNexus.md
  flows/04db2fd2/vision/multiPass.md
  flows/04db2fd2/vision/portion.md
  flows/04db2fd2/vision/psycheLogging.md
  flows/04db2fd2/vision/rollingDistillation.md
  flows/04db2fd2/vision/softwareAnatomySkill.md

Twelve of the 26 files belonged to flow 04db2fd2 (a different flow). Four were skill files belonging to this task. The rest were acbb6006 or shared Vision. Nothing has been reverted.
