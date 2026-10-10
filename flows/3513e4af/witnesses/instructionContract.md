# instruction contract

Method: code read `AGENTS.md`, `CLAUDE.md`, `NON_MANAGEMENT_AGENTS.md`, `.agents/skills/file-editing/SKILL.md`, `.claude/skills/file-editing/SKILL.md`, `.agents/skills/edit-coordination/SKILL.md`, `.claude/skills/edit-coordination/SKILL.md`, `/git/github.com/LiGoldragon/Curriculum/skills/file-editing.md`, `/git/github.com/LiGoldragon/Curriculum/skills/edit-coordination.md`, `/git/github.com/LiGoldragon/Curriculum/skills/flows.md`; probe `jj show 634ad0ed5672`, `jj diff -r '634ad0ed5672-' -r 634ad0ed5672`, and the current generated files. No instruction or generated tree was edited by this flow.

## Observations

- Primary revision `634ad0ed5672` changes only `NON_MANAGEMENT_AGENTS.md`. Its exact replacement at line 20 is: `Leave no uncommitted changes behind: what you changed, you commit and push before finishing. When a tree you are about to write in already holds changes, commit those first, as their own commit, described as found in the tree.` It replaced two older bullets, including `Commit and push edited work.` and `Commit the whole working copy; dirty or unrelated existing files in primary are not a blocker and may be included.`
- `AGENTS.md` and `CLAUDE.md` both require reading `@NON_MANAGEMENT_AGENTS.md`; therefore the new preservation sentence is directly present through the hand-authored primary entry contract. The entry files are ordinary tracked primary files, not generated `.agents` or `.claude` skill outputs.
- The authored Curriculum `skills/file-editing.md` and the generated `.agents/skills/file-editing/SKILL.md` and `.claude/skills/file-editing/SKILL.md` still say only: `Commit existing dirty changes first with an appropriate message before starting new work.` They carry the `jj commit`, bookmark, push sequence and prohibit raw Git, but do not carry the exact “found in the tree” sentence from 634ad0ed5672.
- The authored and generated `edit-coordination` skill still prints parenthesized Register/Claim/Release forms. The current CLI probe rejected those forms and required brace-block syntax; the incident transcripts independently record the same parser boundary. The skill also says refusal is advisory and work may continue.
- The authored and generated `flows` skill now says `log.md makes the flow's main points easily accessible` and that the transcript holds conversation and times. This is the deployed wording present in `e9dbab8c` and current primary.
- The Curriculum source checkout is clean at `e7520542`; its file-editing source still has the older dirty-change sentence. Primary’s lock points at Curriculum, but no Curriculum edit was authorized or made here.

## Claims

- The exact entry-file preservation contract in `634ad0ed5672` postdates both Claude incidents. It cannot explain or retroactively prevent those losses.
- Before 634ad0ed5672, the entry and file-editing text required committing dirty changes but did not explicitly say to make a found-in-tree commit before any new write. The omission is a contract gap, not proof that an agent was instructed to discard work.
- The current direct entry rule is stronger than the still-generated file-editing wording for the specific “found in the tree” case. They are related contracts with different owners; this evidence does not authorize unifying or editing them.

## Hypotheses

- An explicit found-in-tree preflight could have made the shared-working-copy hazard more visible before the incidents, but it cannot by itself prevent a concurrent stale checkout or Git-head import.
- The edit-coordination syntax drift may have reduced coordination observability during aa4 recovery, but the skill explicitly makes claims advisory and the parser failure is not a causal proof of file loss.

## Unknowns

- Whether Claude or Codex received the current hand-authored entry files in exactly the same way at the incident start is not re-probed here; the transcripts establish their own loaded skill text and tool calls, not a complete harness context reconstruction.
- Whether the Curriculum source should eventually carry the entry-file rule, or whether the current direct-primary ownership is intentional, remains an authority question for the living psyche.
