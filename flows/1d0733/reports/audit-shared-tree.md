# Shared-tree audit since 2026-10-10 00:04 local (-0600)

Read-only. Sources: (a) `git reflog --date=iso` in /home/li/primary; (b) the 46 subagent transcripts in tasks/*.output, entries with timestamp >= 2026-10-10T06:04Z, Bash commands matching git/rm/mv/cp/redirect/tee/sed -i, plus Write/Edit calls. The transcript records cwd /home/li/primary for the subagent a23436; no per-command cwd for the others.

## (a) Reflog entries 00:04 to 00:17 (message as recorded)

Reflog has no author field; entries are listed, not attributed.

- 00:04:39 checkout: moving from 73da46e51 to main
- 00:05:39 c8d5abeba push
- 00:07:02 aeffbd61e commit: d5df1d: restore flow directory onto main from 9360a7
- 00:07:52 18a1e737a commit: 1d0733: log and psyche records, rebuilt after the tree wipe
- 00:07:59 da5841bfc commit: 445410: restore flow directory
- 00:08:20 bd94d7f2b commit: 445410: data-loss log
- 00:08:52 795637261 commit: 9fed42: restore lane and Flow Ethos candidate
- 00:08:58 f9d033535 commit: d5df1d: spec settled
- 00:09:00 460ac12e3 commit: 1d0733: reports and log restored from the recovery branch
- 00:09:09 03b2e129c commit: 445410: 1d0733 restored
- 00:09:14 0bd760d6f commit: d5df1d: recovery noted
- 00:10:21 825fdf0e1 commit: 9fed42: log Astra research
- 00:11:46 04c14b747 commit: d5df1d: types reruns green
- 00:13:23 722a2c471 commit: d5df1d: spec corrected to the reruns
- 00:13:23 6df20e439 commit: d5df1d: publish ordered
- 00:14:01 0b0f60055 commit: d5df1d: publish blocked on lock
- 00:15:12 b70d986d9 commit: d5df1d: item 5 acceptance
- 00:15:32 fcb360aa1 commit: d5df1d: answer 0c85a3
- 00:15:50 1e72dc426 commit: d5df1d: item 5 (a) held
- 00:16:09 b2c9c642d commit: d5df1d: queued behind 16030
- 00:17:00 6db506f14 commit: d5df1d: item 5 landed (claim), main tip warning
- 00:17:20 93a033204 commit: d5df1d: main tip witnessed

Entries at 00:04:13 (8e4b59d28) and 00:04:21 (73da46e51) are the boundary entries; see (b).

## (b) Subagent operations in the shared copy outside flows/1d0733

All by subagent a234361776e59afb5, cwd /home/li/primary, UTC timestamps (local = UTC-6):

- 06:04:13 `git add flows/1d0733/reports/variant-name-collision.md && git commit -m "1d0733: variant-name collision datom read analysis from Prometheus ..."` -> detached HEAD 8e4b59d28 (path set: that one file, inside flows/1d0733).
- 06:04:16 `git checkout main && git status | head -15` -> refused: local changes in .agents/skills/..., .claude/skills/... would be overwritten.
- 06:04:19 `git add -A && git status --short | wc -l` -> 326 paths staged, whole tree (includes .agents/, .claude/, .5578cc.flow-id, .5578cc.flow-id.lock, flow submodule path, flows/d5df1d/... etc.).
- 06:04:21 `git commit -m "Regenerate agents and skills from authored sources"` -> detached HEAD 73da46e51, 325 files changed, 27982 insertions, 1150 deletions (path set: the 325 staged paths outside and inside flows/).
- 06:04:33 `git checkout main 2>&1 | tail -5` -> refused: flows/d5df1d/reports/fork-options-spec.md would be overwritten.
- 06:04:37 `git restore flows/d5df1d/reports/fork-options-spec.md && git status | head -3` -> discarded that file's working-tree change (diff seen at 06:04:34: Invariants Proposal 4 edit).
- 06:04:39 `git checkout main && git log --oneline -1` -> HEAD to main; "leaving 94 commits behind" warning for 73da46e51 and ancestors.
- 06:04:41 `git branch recovery 73da46e51` -> created branch recovery at 73da46e51 (exists now).
- Read-only git in the same agent: git status, git branch -a, git log (HEAD..main, --all --name-only), git diff flows/d5df1d/reports/fork-options-spec.md, git show recovery:... > /tmp/variant-file.md.
- Edit 06:04:10 of flows/1d0733/reports/variant-name-collision.md (inside flows/1d0733).

Other subagents since 00:04, shared-copy operations outside flows/1d0733:
- a687544205be7e3c0 06:10-06:17 ran `orchestrate 'Lock.{ PrimaryPublish ... [ /home/li/primary/.PrimaryPublish.lock ] ...}'` and `Release.*` (Orchestrate lock on a path in the shared copy, requested via the orchestrate CLI); `git clone -q /home/li/primary` into the scratchpad; `rm -rf flows/1d0733` and tar copy inside the scratchpad clone; `jj git push --bookmark main` from the scratchpad clone to origin (06:17:04, repeated 06:17:07). These run in the scratchpad clone, not in the shared copy; the push reaches origin main.
- a8d3c13392580ed4d 06:08 read-only git in the shared copy (reflog, fsck --lost-found --no-reflogs, ls-tree, show); wrote files only under flows/1d0733 (`git show recovery:$p > $p`, `> $p.recovered`).
- ada80125019756962, a8847e06c58475c2c: Write/redirect only to flows/1d0733/reports; other commands in scratchpad or on Prometheus.
- ad200245aa2974b4c, adb612258c66e4aaf: read-only git / scratchpad clone of origin.

## Not observed

No git, rm, mv or cp with cwd /home/li/primary outside flows/1d0733 appears in any transcript for the reflog commits from 00:07:02 to 00:17:20, nor for the 00:04:39 checkout other than as listed (b) at 06:04:39, nor for the 00:05:39 push (no transcript command at 06:05:39). Transcripts were not searched for tool calls that lack a Bash command string (e.g. orchestrate or hm-* scripts writing files).
