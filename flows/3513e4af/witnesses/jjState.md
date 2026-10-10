# jj state

Method: probe `jj status`, `jj log -r 'all()'`, `jj op log -n 1000 --no-graph`, `jj op show <operation>`, `jj file list`, `jj show`, and `jj diff` in `/home/li/primary`; correlate the operation records with the two Claude transcript tool calls.

## Observations

- The relevant primary commit chain is witnessed by `jj log`: `748569dbf` (“verified: record Claude Code 2.1.235 and Codex 0.148.0 harness witnesses”), `90575b46c` (“flows: 2f6b1dc5 — restore lost records; base-context deployment accounts”), then `89ebc65d` (“flows: record Codex and Claude lifecycle hook removal”). `89ebc65d` has parent `90575b46c` and its tree contains only `flows/aa4c7747/log.md`; `90575b46c` has no aa4 path. The later `e9dbab8c` line has parent `30840e655a` and contains aa4’s log plus ten vision files.
- `jj show 90575b46c` reports only three modified 2f6 files: `log.md`, `vision/contextStrata.md`, and `vision/vocabulary.md`. `jj file list -r 90575b46c flows/2f6b1dc5` shows four surviving files including `vision/systemPrompt.md`.
- The operation log records, in order around 2f6 recovery: `import git head` (`112e0a614cdc`) changed the default working copy to an empty child and retained 2f6/aa4 dirty files; `commit` (`42d012a74da8`) made the restored 2f6 commit; bookmark movement (`c4ab52dbe1c1`) advanced `main`; and push (`d03199f3c008`) published it. `jj op show 112e0a614cdc` directly reports the changed working copy from `43424f60` to an empty child and `jj op show 42d012a74da8` reports the creation of `90575b46c`.
- The operation log later records a separate branch of state work: `e9b1094c9929` rebased a commit and descendants, `7072b88dd9b7` committed “flows: preserve current investigation records”, and `59d496704ee1` pushed `fcbabf8b`. The subsequent root work rebased and advanced main again. This is evidence of concurrent state movement, not proof of a particular culprit.
- At this subflow’s start, the working copy held seven dirty files in `flows/01a035d3` and `flows/aa4c7747`; per the required preservation contract they were committed unchanged as `498cf24d` (“Preserve found-in-tree changes before incident evidence”), then `main` was advanced and pushed. The current follow-up `jj status` was clean before this flow’s evidence write.

## Claims

- The jj graph independently supports the aa4 stale-tree boundary: the line observed by Claude (`89ebc65d`) is a child of the 2f6 restoration but predates the later branch carrying aa4 vision files (`e9dbab8c`). A working copy at 89eb’s tree necessarily lacks those uncommitted vision files.
- The operation log proves that Git-head imports, rebases, workspace operations, and concurrent bookmark pushes occurred in the same time window. It does not expose an operation saying “delete aa4 vision” or identify the process that selected 89eb’s tree.

## Hypotheses

- The loss mechanism is stale shared working-copy selection or snapshot replacement, not a successful `jj commit` that recorded then deleted the files. The aa4 files were absent from the 89eb tree because they were not committed on that line; the recovery checkout copied them from e9db’s tree.
- The 2f6 scoped commit preserved its named path but could not protect unrelated uncommitted files from concurrent workspace/Git state movement. Whether the scoped form materially contributed to later loss is not proven.

## Unknowns

- The exact process, workspace, or operation that advanced Git HEAD or selected the stale working copy is not present in the available jj operation records.
- The operation log is local and serialized, but several operations came from named workspaces; the surviving records do not provide a complete cross-process causal trace for every filesystem write.
