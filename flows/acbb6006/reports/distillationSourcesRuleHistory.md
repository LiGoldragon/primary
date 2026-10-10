# Distillation Sources Rule History

## Question

The living asked: "all distillation refers to the raw psyche it was distilled from.
this was the distillation protocol from the start. was that taken out of the skill?"

## Finding 1: Was such a rule ever in the skill?

No. The psyche-distillation skill was first created in Curriculum commit
**ebba084** (2026-08-22, flow 68512643 session "psyche logging: vision/,
distillation, psyche-raw/ paths, the living shorthand"). The initial text
contained no requirement that a distilled statement refer to the raw psyche
records it was distilled from. Specifically:

> "A proposal re-articulates; it never quotes. The archived originals keep
> every original word."

The archive was required to be preserved, but there was no rule requiring
the distilled statement itself to carry a back-reference to its sources.

## Finding 2: What was added, not removed — and when

Commit **f505c72** (Curriculum, 2026-08-24 12:06:24, flow 68512643) ADDED
the self-standing rule to the skill. This was not a replacement of a prior
references rule; it was a new insertion:

> "A distilled statement stands on its own words, referring to no beads,
> files, or flows."

The commit message is simply "land self-standing rule in psyche-distillation
skill" with no Claude-Session attribution. The originating flow is 68512643,
identified from the parallel primary-repo commit 6f118ee7f (2026-08-24 12:06:07):
"flows: 68512643 — searches resolved; self-standing line deployed".

## Finding 3: The psyche's words that drove the addition

From transcript 68512643 L661, 2026-08-24 10:01 (typed):

> "we can't refer to beads and files in Vision. let's make sure the skill
> know this. psyche must remain self standing"

Context from the flow log (flows/68512643/log.md): the distillation proposal
for Vision/datom.md had a bead reference inside the Meaning statement; the
psyche directed it removed ("bead reference dropped from the Meaning statement").
The ruling applied to Vision files specifically. The model then dispatched a
write subflow to land the self-standing line in the Curriculum skill.

No words of the living were found discussing a prior convention that required
distillation to reference the raw psyche. The living's words drove the addition
of the opposite rule.

## Finding 4: The 2026-08-14 archive-linking design (related but inverse)

In psyche-raw/Vision/psycheLogStructure.md, a 2026-08-14 record carries the
psyche's words on the cleaning-pass design:

> "it should even be archived to link back to the record(s) that replace them,
> ostensibly with a short hash"

This describes archives linking TO the distilled statements that replaced them
(archive → distilled), not distilled statements linking back to archives
(distilled → archive). The existing archive files do carry forward references
("Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md") but
not short hashes. This design idea was not turned into a skill rule.

## Finding 5: Sources convention in Vision files

No `## Sources` sections exist in any Vision/ file. No `Vision/sources/`
directory exists. A "sources-file rule" (one `Vision/sources/<topic>.md` per
topic listing archived sources) was proposed within flow acbb6006 and
re-presented to the living in the third round of that flow — its approval
status is open as of this writing.

## Observations vs. Inferences

**Observed:**
- The psyche-distillation skill never contained a rule requiring distilled
  statements to refer to their source records.
- The self-standing rule was added 2026-08-24 in response to the living's
  explicit typed word.
- Archive files carry forward references to what distilled them; Vision files
  carry no back-references to archives.

**Inference:**
- The living may be recalling the 2026-08-14 bidirectional-archive design
  (which was never codified in the skill) or the practical convention of bead
  references in proposals (not in Vision), rather than a rule that existed
  and was removed.

## Sources

- Curriculum git log: `git log -p --follow skills/psyche-distillation.md`
  (commits ebba084, f505c72)
- Transcript 68512643 L661 (2026-08-24 10:01)
- flows/68512643/log.md (inline witness of the self-standing landing and its
  context)
- psyche-raw/Vision/psycheLogStructure.md (2026-08-14 archive-linking design)
- Vision/datom.md (no ## Sources section)
- flows/acbb6006/log.md (sources-file rule, third-round re-presentation)
