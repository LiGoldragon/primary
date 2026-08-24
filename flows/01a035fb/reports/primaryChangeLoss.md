# Primary change loss

## Conclusion

The two recent Claude incidents were not evidence that `jj commit` destroyed committed data. Both were shared-working-copy incidents: flow records were written but remained uncommitted while other agents changed repository state, and a later working-copy view selected a tree that did not contain those writes. The records became absent from disk; recovery material remained in jj history or the originating transcript.

The exact concurrent actor and exact state-changing operation remain unknown. The evidence therefore supports a state-ownership defect plus an uncommitted-work exposure window, not a claim that one named agent or one named jj command caused both losses.

## Incident `2f6b1dc5`

- The full Claude transcript survives as session `2f6b1dc5-307c-400c-b339-8ec622e8fadc`.
- The transcript records writes to the flow log and vision files, then a reread where the newest log, vocabulary, and context-strata material was missing while concurrent subflow commits landed.
- `jj status` imported a new Git HEAD and reported that the working-copy parent had been reset; the restored three files were then dirty against parent `748569dbf`.
- The flow reconstructed the missing text from retained model context, committed it as `90575b46c066`, moved `main`, and pushed it.
- The current surviving set is `log.md` plus `vision/systemPrompt.md`, `vision/vocabulary.md`, and `vision/contextStrata.md`. No report or witness file is proven missing.

Thus the flow logs are recovered now, with a provenance caveat: the missing tail was contextually reconstructed, not restored byte-for-byte from an independent pre-loss copy.

## Incident `aa4c7747`

- The full Claude transcript survives as session `aa4c7747-3b0c-43ea-a131-0fa65b17348e`.
- Its working-copy parent was the stale `89ebc65d` line, whose tree held only the flow log. Direct `ls` evidence showed that the vision directory was absent.
- Revision `e9dbab8c` held the log and ten vision files. The session copied those files back; later records were also committed.
- Subsequent recovery preserved the dirty state, rebased it onto current `main`, resolved two flow-log conflicts by keeping the supersets, and pushed it.

Again, repository history retained the data; the stale disk view hid it.

## Instruction boundary

The later flow `aa4c7747` obtained psyche approval for and landed this worker-entry contract in `NON_MANAGEMENT_AGENTS.md` at `634ad0ed5672`: agents must commit and push their own changes, and commit changes already found in a tree first as a separate found-in-tree commit.

That exact rule postdates both incidents. The Curriculum-authored and generated file-editing skill still has the shorter rule to commit existing dirty changes before starting, plus the unscoped `jj commit`, bookmark, and push sequence. No Curriculum skill change was made.

The new entry rule is directionally correct: had it been followed before new writes, it would likely have reduced the amount of uncommitted work exposed. It cannot by itself prevent another agent or Git-head import from changing a shared working-copy parent. The terminal correction must establish ownership of repository state transitions; additional jj wording is only a supporting contract.

The edit-coordination skill also contains command syntax rejected by the current CLI. That reduces coordination observability, but claims are advisory by design, so its drift is not a proven cause of either loss.

## Observations, hypotheses, and unknowns

Observed:

- Concurrent repository operations and Git-head imports occurred in the incident windows.
- Both affected flows had uncommitted records when another tree became the working view.
- Both flows' material survives now.
- The exact found-in-tree entry rule was absent during the incidents.

Best-fit hypothesis:

- A concurrent writer or import selected a stale/shared working-copy snapshot that omitted another flow's uncommitted files.

Unknown:

- Which process selected each stale state and the precise filesystem operation that made the files disappear.
- Whether the terminal design should use a single serialized writer, independently owned jj workspaces, or another mechanism; that design needs an explicit anatomy and a behavioral witness.

## Sources

- `flows/3513e4af/witnesses/claudeIncidents.md`
- `flows/3513e4af/witnesses/jjState.md`
- `flows/3513e4af/witnesses/instructionContract.md`
- `flows/3513e4af/reports/claudeIncidentPreservation.md`
- `flows/2f6b1dc5/log.md`
- `flows/aa4c7747/log.md`
- Flow `3513e4af`
- Flows `2f6b1dc5` and `aa4c7747`

