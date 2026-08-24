# Claude incidents

Method: probe `jq -r` over `/home/li/.claude/projects/-home-li-primary/2f6b1dc5-307c-400c-b339-8ec622e8fadc.jsonl` and `/home/li/.claude/projects/-home-li-primary/aa4c7747-3b0c-43ea-a131-0fa65b17348e.jsonl`, selecting human typed records, assistant tool-use records, and their paired tool results; re-read the referenced flow directories and commit contents with `jj file list`, `jj show`, and `find`.

## Observations

### 2f6b1dc5

- The Claude transcript is present at the first path above, 787 JSONL records and 1,704,524 bytes at probe time. The human typed ruling `deploy the LLM strata skill with context instead of prompt.` is a user record at `...2f6b1dc5....jsonl:608`; the transcript's last-prompt record repeats it at `:611` and `:769`.
- The flow wrote `flows/2f6b1dc5/vision/systemPrompt.md` at `2026-08-23T13:42:36.499Z`, `log.md` at `13:44:52.683Z`, then `vision/vocabulary.md` at `2023-08-23T14:11:31.949Z` and `vision/contextStrata.md` at `2026-08-23T22:47:35.567Z` (assistant tool-use records selected by the probe). The timestamp year in the vocabulary record is the transcript's recorded timestamp; no byte-level claim is made about an earlier uncommitted version.
- At `2026-08-24T12:46:35.204Z`, the flow edited the log and explicitly recorded that its tail and the latest vocabulary/context-strata entries had vanished while subflow commits landed; it said the entries were restored from the flow's context. The edit is the assistant record at `:739`; its paired file-write result is at `:762`.
- At `:764`, Claude ran `jj st --no-pager`. The paired result at `:766` says: `Reset the working copy parent to the new Git HEAD`, then lists uncommitted `flows/2f6b1dc5/log.md`, `vision/contextStrata.md`, `vision/vocabulary.md`, and `flows/aa4c7747/log.md`, with parent `748569dbf`.
- At `:777`, Claude ran `jj commit -m 'flows: 2f6b1dc5 — restore lost records; base-context deployment accounts' flows/2f6b1dc5 && jj bookmark set main -r @- && jj git push --bookmark main`. The paired result at `:779` reports commit `90575b46`, `main` moved from `748569dbf` to `90575b46`, and an empty working-copy child.

### aa4c7747

- The Claude transcript is present at the second path above, 777 JSONL records and 1,884,028 bytes at probe time. The human typed instruction `fix the repo, and make a proposal for entry files to instruct agents to never leave uncommitted changes behind like that` is at `...aa4c7747....jsonl:521`; `entry file proposal approved` is at `:556`. Earlier writes are represented by file-history snapshots and assistant `Write`/`Edit` calls, not by a commit made by this flow.
- At `2026-08-24T22:07:42.032Z`, the assistant said: `The skill edit landed — but my flow log on disk was reverted to its old diary state by something outside this flow. Checking what happened before restoring it.` This is the assistant text record at `:468`.
- At `:469`, it ran `git log --oneline -6 -- flows/aa4c7747/`, `git status --short flows/aa4c7747/`, and `git log --oneline -4`. The result at `:470` listed `89ebc65dc` as the flow-path commit and showed no status output; the recent history listed `90575b46c`, `748569dbf`, and `a0cfffea7`.
- At `:473`, it ran `ls -la flows/aa4c7747/ flows/aa4c7747/vision/`, inspected `89ebc65dc`, checked `e9dbab8c`, and read the deployed flows skill. The result at `:474` says `flows/aa4c7747/vision/: No such file or directory`; only `log.md` was present. It also shows `git show e9dbab8c` containing the flow's vision files and the deployed newer flows wording.
- The current transcript's lane attempts are at `:494` and `:499`; results at `:495` and `:500` reject the skill's parenthesized and first brace forms before transport (`expected LaneRegistrationRequest to be a brace block`, then `expected ... to hold 2 root objects`). These are parser observations from the incident, not successful claims.
- At `:503`, it ran `git checkout e9dbab8c -- flows/aa4c7747/ && ls flows/aa4c7747/vision/ ...`. The result at `:504` lists ten recovered vision files and confirms the `.jj` directory. The subsequent verification at `:513`/`:514` finds one `Settled also` line and `TryFrom is` at log line 20.
- Current re-read finds `flows/aa4c7747/log.md`, ten original vision files, and the later `orchestrate.md`, `promptCrafting.md`, and `uncommittedChanges.md`. The latter three were written after the checkout restoration and are not in `e9dbab8c`.

## Claims

- The transcripts witness two distinct loss presentations: 2f6’s missing tail was reported on reread and reconstructed from retained model context; aa4’s missing `vision/` directory was observed directly by `ls` and recovered from a named commit.
- Both sessions were writing into the shared `/home/li/primary` tree. The records establish reads, writes, and recovery actions, but they do not identify the concurrent session that changed the checked-out state.

## Hypotheses

- For 2f6, a concurrent jj/Git state transition during subflow commits or Git-head import selected a working-copy snapshot that omitted the uncommitted tail. The transcript's own candidate list names concurrent snapshots and the unexplained `a0cfffea7`; this witness does not choose between them.
- For aa4, the working copy was on the stale `89ebc65dc` line, whose tree has only `flows/aa4c7747/log.md`; the newer `e9dbab8c` line carried the vision files. This explains the observed absence, but not who selected that line.

## Unknowns

- No independent pre-loss byte copy of 2f6’s missing tail was found. “Restored verbatim” means reconstructed from retained flow/model context, not recovered from a second file image.
- The exact concurrent actor, jj operation, or Git ref writer responsible for each stale selection remains unknown. The Claude transcripts show the symptom and the repair, while the jj operation witness shows surrounding state transitions.
