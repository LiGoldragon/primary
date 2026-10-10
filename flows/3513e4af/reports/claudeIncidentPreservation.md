# Claude incident preservation

The two incidents have different direct witnesses but the same boundary: work was written into a shared primary working tree before a stable, independently recoverable commit existed. A later state transition presented a tree that did not contain some of that work. The evidence does not identify the actor that selected the stale state.

## Observations

- Session `2f6b1dc5-307c-400c-b339-8ec622e8fadc` survives as a Claude JSONL transcript. It records the flow writing `log.md` and vision files, then reporting that the log tail and latest `vocabulary.md`/`contextStrata.md` entries vanished while subflow commits landed. The same transcript records `jj st` importing a new Git HEAD with those files dirty, followed by a scoped commit that landed the restored 2f6 content as `90575b46c066` and pushed `main`.
- Session `aa4c7747-3b0c-43ea-a131-0fa65b17348e` survives as a Claude JSONL transcript. It records an assistant reread where `flows/aa4c7747/vision/` was absent and only `log.md` remained, then a direct `git checkout e9dbab8c -- flows/aa4c7747/` that restored ten vision files. Later writes added three more vision records (`orchestrate.md`, `promptCrafting.md`, `uncommittedChanges.md`).
- jj history independently shows `89ebc65d` as a child of `90575b46c`; its tree has only aa4’s log. The later `e9dbab8c` tree has aa4’s log and ten vision files. The filesystem state observed by aa4 therefore corresponds to a stale line that did not carry its uncommitted vision files.
- The current primary entry contract gained the exact found-in-tree preservation rule in `634ad0ed5672`, after both incidents. The generated file-editing skill and its Curriculum source still carry the older, less specific dirty-change sentence.

## Claims

- 2f6 recovery was contextual reconstruction, not recovery from an independent pre-loss copy. The surviving set is `log.md`, `vision/systemPrompt.md`, `vision/vocabulary.md`, and `vision/contextStrata.md`; no 2f6 `reports/`, `witnesses/`, or `annotations.md` was found in the transcript’s flow writes or current tree.
- aa4 recovery was commit-backed for the ten files present in `e9dbab8c`; the files written after that checkout are only witnessed by the later transcript and subsequent committed flow state.
- The causal boundary is stale/shared working-copy state plus uncommitted writes. jj misuse is evidenced where the transcript used a path-scoped `jj commit` and aa4 used raw `git checkout`, but neither operation alone is shown deleting a committed artifact. Instruction omission is present as a before-634 gap, while generated-entry drift and lane-parser drift are contributing observability risks rather than established causes.

## Hypotheses

- A concurrent workspace or Git-head import moved the shared checkout to a commit that lacked one flow’s uncommitted files. This is the best-fit explanation for both the aa4 directory absence and 2f6’s loss report, but the exact actor remains unknown.
- The explicit 634ad0ed5672 preflight would likely have caused dirty work to be committed before a new write, reducing the exposure window. It would not eliminate concurrency unless the working-copy ownership/state transition is also controlled.

## Unknowns

- No direct jj operation record names the actor or proves the exact filesystem write that removed 2f6’s tail or selected aa4’s 89eb tree.
- The precise bytes that 2f6 held before reconstruction are not independently preserved; retained context is a second witness of intent, not a byte-for-byte recovery source.
- No authority was granted in this investigation to edit the Curriculum source, generated trees, entry wording, or coordination implementation. Any proposed contract change therefore remains for psyche approval.

## Sources

- `witnesses/claudeIncidents.md`
- `witnesses/jjState.md`
- `witnesses/instructionContract.md`
- `flows/2f6b1dc5/log.md`
- `flows/aa4c7747/log.md`
- `jj show 90575b46c066`, `jj show 89ebc65dc3b5`, `jj show e9dbab8c`, and the local jj operation log
- `/home/li/.claude/projects/-home-li-primary/2f6b1dc5-307c-400c-b339-8ec622e8fadc.jsonl`
- `/home/li/.claude/projects/-home-li-primary/aa4c7747-3b0c-43ea-a131-0fa65b17348e.jsonl`
- `flows/3513e4af/witnesses/claudeIncidents.md`
- `flows/3513e4af/witnesses/jjState.md`
- `flows/3513e4af/witnesses/instructionContract.md`
