# flows skill: remembering paragraph edit proposal

## 1. Proposed text

Diff — `[existing]` unchanged, `+` new:

```diff
 Earlier work is continued by remembering the flows concerned: their
 psyche records, a high-level awareness of their work from log and
 reports, and a light check of the current state of what their topics
 touched, with the result shown to the psyche in simple words and
-visuals. The flow's last model response must be read. The log records each
+visuals. The flow's last model response must be read. All flows are one
+subjectivity; anything not in a flow but not yet remembered can be
+recalled by searching other flows. "You did" or "you said" heard in a
+flow that did not itself do or say the thing obliges that flow to
+remember it at a depth fit to the question, reaching the transcript
+directly when logs are not enough. The log records each
 remembering as `Remembered: <short-ids> — depth <n>`. One layer at
 session start; a stated number when going deep into a topic; the whole
 chain only on the psyche's explicit word.
```

Full paragraph as it would read:

Earlier work is continued by remembering the flows concerned: their
psyche records, a high-level awareness of their work from log and
reports, and a light check of the current state of what their topics
touched, with the result shown to the psyche in simple words and
visuals. The flow's last model response must be read. All flows are one
subjectivity; anything not in a flow but not yet remembered can be
recalled by searching other flows. "You did" or "you said" heard in a
flow that did not itself do or say the thing obliges that flow to
remember it at a depth fit to the question, reaching the transcript
directly when logs are not enough. The log records each remembering as
`Remembered: <short-ids> — depth <n>`. One layer at session start; a
stated number when going deep into a topic; the whole chain only on the
psyche's explicit word.

## 2. Alternative placement

Open the skill with "All flows are one subjectivity." as a standalone
first sentence, before the directory structure. Trade: asserts the
identity claim globally, where it is most foundational, but separates
it from the cross-flow obligation that makes it actionable, requiring
the reader to connect two distant passages.

## 3. Other skills

- **transcript-search** description: add "or for what another flow
  said or did that this flow did not itself witness" — the ruling names
  reaching the transcript as the fallback for cross-flow remembering,
  which the current description does not trigger on explicitly.
- **subflows**: no change needed; "what a subflow did, the flow did"
  already covers the vertical same-subjectivity direction the ruling
  does not re-address.
- **psyche-interraction**: not implicated by this ruling.

## 4. Regeneration and commit steps on approval

Edit `/git/github.com/LiGoldragon/Curriculum/skills/flows.md`; run
`nix run /home/li/primary#generate-skills -- "CurriculumRequest.{Generate.{/git/github.com/LiGoldragon/Curriculum /home/li/primary}}"`;
commit and push Curriculum (authored source change) then primary
(generated `.claude/` update) per the file-editing skill.

## Sources

- `/git/github.com/LiGoldragon/Curriculum/skills/flows.md` commit 3a5e8ba
- `flows/b675f3d9/vision/remembering.md` (psyche ruling, 2026-08-26)
- `/home/li/primary/.claude/skills/transcript-search/SKILL.md`
- `/home/li/primary/.claude/skills/subflows/SKILL.md`
