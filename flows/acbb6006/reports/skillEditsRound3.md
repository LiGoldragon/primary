# Skill Edits Round 3

Two directed edits applied to authored skill sources in Curriculum, consumer trees regenerated.

## Edit 1: nexus.md — delete multi-nexus commit line

Deleted the paragraph:

> When one intent spans several nexuses, the issuer commits on the first success and records divergence on failure — no distributed rollback, no all-or-nothing stall.

The psyche ruled it "pure quackery" and ordered deletion. The surrounding sentences ("Polling is forbidden"; "One capability, one Nexus") were left exactly as they were.

## Edit 2: psyche-distillation.md — distillation carries what the psyche said

Added after the paragraph beginning "A proposal re-articulates; it never quotes.":

> A distilled statement carries what the psyche said and nothing beyond it; a small ruling makes a small statement, never a theory grown around the words.

The psyche approved this exact wording (flows/acbb6006/vision/distillation.md, "A small bit of psyche is not expanded into a theory").

## Verification

- `.claude/skills/nexus/SKILL.md`: sentence absent.
- `.claude/skills/psyche-distillation/SKILL.md` line 25: new line present.

## Sources

- flows/acbb6006/vision/nexus.md — "The multi-nexus commit line is quackery; deleted from the skill" (psyche, 2026-08-27T15:38:13Z)
- flows/acbb6006/vision/distillation.md — "A small bit of psyche is not expanded into a theory" (psyche, 2026-08-27T15:20:37Z)
- Curriculum commit 55f77904 (`/git/github.com/LiGoldragon/Curriculum`)
