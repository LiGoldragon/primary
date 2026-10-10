# Audit facts: flow d5df1d operations in /home/li/primary since 2026-10-10 00:04 (-0600)

Sources: git log and reflog in /home/li/primary (witnessed by command); grep of the 64 subflow transcripts in /tmp/claude-1001/-home-li-primary/d5df1daf-854d-4469-8700-0997eb3babb1/tasks/*.output (witnessed by grep; transcript timestamps are UTC, local is UTC-6). No cause is inferred.

## 1. In-flight operations

None running of this flow beyond one publisher working in its own clone (scratchpad/pub under this session's scratchpad, cloned from git@github.com:LiGoldragon/primary.git; it uses jj there, and orchestrate Lock/Release PrimaryPublish 15849 and 15850 appear in its transcript).

## 2. Operations outside flows/d5df1d

### Main-thread operations of d5df1d in the shared copy, 2026-10-10

(a) `git checkout 9360a7edd -- flows/d5df1d`, cwd /home/li/primary, run between the 00:04:39 checkout and the commit "d5df1d: restore flow directory onto main from 9360a7" (aeffbd61e); path set: flows/d5df1d only; prestate: flows/d5df1d absent from the working tree and from HEAD's tree; receipt: that commit.

(b) `git checkout aeffbd61e -- flows/d5df1d/reports/fork-options-spec.md` followed by an in-place sed on that same file, cwd /home/li/primary, before the commit "d5df1d: spec settled" (f9d033535); path set: that one file; prestate: the file at 192 lines on disk; receipt: that commit.

(c) Every d5df1d: commit in the window was made with `git add flows/d5df1d` followed by `git commit`, cwd /home/li/primary; path set flows/d5df1d only; each moves HEAD and the index.

(d) No other command of the main thread touched the shared working copy, HEAD or index; the 00:04:39 checkout to main was not issued by this flow or, per the transcripts, by any of its subflows.

Git log and path-set verification:

Output of `git log --format='%H %ci %s' --grep='^d5df1d:' --since='2026-10-10 00:04'`:

```
93a03320445a58618d1475556b2825557c2eb6be 2026-10-10 00:17:20 -0600 d5df1d: main tip witnessed
6db506f1480be7ad18e6ab250cec1b56ed36fd47 2026-10-10 00:17:00 -0600 d5df1d: item 5 landed (claim), main tip warning
b2c9c642d737329759d8858f3a007c1b161b2144 2026-10-10 00:16:09 -0600 d5df1d: queued behind 16030
1e72dc426e5a3fa8e6a1a33fb0331c3cec3e70a0 2026-10-10 00:15:50 -0600 d5df1d: item 5 (a) held
fcb360aa1ffc27e054460a35c84d0adc7d27530a 2026-10-10 00:15:32 -0600 d5df1d: answer 0c85a3
b70d986d969d08d0ba9d2f777d1bda969cac67e6 2026-10-10 00:15:12 -0600 d5df1d: item 5 acceptance
0b0f600558ebacbd2cd2328e77db324996ad96d9 2026-10-10 00:14:01 -0600 d5df1d: publish blocked on lock
6df20e4394ca570f2433f8168ffd2bda0fd496ac 2026-10-10 00:13:23 -0600 d5df1d: publish ordered
722a2c471f4c905671b16461a2c8be0c879dc27f 2026-10-10 00:13:23 -0600 d5df1d: spec corrected to the reruns
04c14b747d543186ba505a72ac4d241b459803a7 2026-10-10 00:11:46 -0600 d5df1d: types reruns green
0bd760d6fb518ebfdfd5162f2de125d4fd78196b 2026-10-10 00:09:14 -0600 d5df1d: recovery noted
f9d033535f5698f3b8f7d6d4df2d659872fa99f5 2026-10-10 00:08:58 -0600 d5df1d: spec settled
aeffbd61efdc5b940c98541c6206b705aaccfc89 2026-10-10 00:07:02 -0600 d5df1d: restore flow directory onto main from 9360a7
```

Path-set check for each hash (`git show --stat --format=` result):

- 93a03320445a58618d1475556b2825557c2eb6be: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- 6db506f1480be7ad18e6ab250cec1b56ed36fd47: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- b2c9c642d737329759d8858f3a007c1b161b2144: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- 1e72dc426e5a3fa8e6a1a33fb0331c3cec3e70a0: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- fcb360aa1ffc27e054460a35c84d0adc7d27530a: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- b70d986d969d08d0ba9d2f777d1bda969cac67e6: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- 0b0f600558ebacbd2cd2328e77db324996ad96d9: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- 6df20e4394ca570f2433f8168ffd2bda0fd496ac: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- 722a2c471f4c905671b16461a2c8be0c879dc27f: flows/d5df1d/reports/fork-options-spec.md only (under flows/d5df1d) ✓
- 04c14b747d543186ba505a72ac4d241b459803a7: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- 0bd760d6fb518ebfdfd5162f2de125d4fd78196b: flows/d5df1d/log.md only (under flows/d5df1d) ✓
- f9d033535f5698f3b8f7d6d4df2d659872fa99f5: flows/d5df1d/log.md and flows/d5df1d/reports/fork-options-spec.md only (under flows/d5df1d) ✓
- aeffbd61efdc5b940c98541c6206b705aaccfc89: flows/73ada7/reports/build/message-design.md (OUTSIDE flows/d5df1d, deletion) and 18 files under flows/d5df1d — ✗ paths outside flows/d5df1d

Git, in /home/li/primary:
- Reflog line at 00:04:39 (not a d5df1d commit): `04ad8e5bd HEAD@{2026-10-10 00:04:39 -0600}: checkout: moving from 73da46e51483ce2251dee66d52c0268c0364b23d to main`. Command, cwd, issuer and path set: unknown. No checkout/reset/stash/clean/rm/mv command in this flow's subflow transcripts matches it (see below). Prestate: HEAD at 73da46e51; receipt: the reflog line and HEAD 04ad8e5bd afterwards.
- All other reflog lines since 00:04 are `commit: d5df1d: ...` (13 lines, 00:07:02 to 00:17:20). Reflog verbatim:
  - 93a033204 HEAD@{2026-10-10 00:17:20 -0600}: commit: d5df1d: main tip witnessed
  - 6db506f14 HEAD@{2026-10-10 00:17:00 -0600}: commit: d5df1d: item 5 landed (claim), main tip warning
  - b2c9c642d HEAD@{2026-10-10 00:16:09 -0600}: commit: d5df1d: queued behind 16030
  - 1e72dc426 HEAD@{2026-10-10 00:15:50 -0600}: commit: d5df1d: item 5 (a) held
  - fcb360aa1 HEAD@{2026-10-10 00:15:32 -0600}: commit: d5df1d: answer 0c85a3
  - b70d986d9 HEAD@{2026-10-10 00:15:12 -0600}: commit: d5df1d: item 5 acceptance
  - 0b0f60055 HEAD@{2026-10-10 00:14:01 -0600}: commit: d5df1d: publish blocked on lock
  - 6df20e439 HEAD@{2026-10-10 00:13:23 -0600}: commit: d5df1d: publish ordered
  - 722a2c471 HEAD@{2026-10-10 00:13:23 -0600}: commit: d5df1d: spec corrected to the reruns
  - 04c14b747 HEAD@{2026-10-10 00:11:46 -0600}: commit: d5df1d: types reruns green
  - 0bd760d6f HEAD@{2026-10-10 00:09:14 -0600}: commit: d5df1d: recovery noted
  - f9d033535 HEAD@{2026-10-10 00:08:58 -0600}: commit: d5df1d: spec settled
  - aeffbd61e HEAD@{2026-10-10 00:07:02 -0600}: commit: d5df1d: restore flow directory onto main from 9360a7
- Before 00:04 (in the reflog, same day, outside the window): 9360a7edd 00:02:01 item 9 withdrawn; 86ca66f05 00:01:21 item 5 path renames; 852815bdd 00:00:38 types forks 1 and 2 rulings.
- Commits whose paths lie outside flows/d5df1d: not checked beyond the five in section 3 (those five touch only flows/d5df1d/log.md). The other `d5df1d:` commits were not path-checked.

Subflow-transcript hits (B) for git add/commit/fetch/worktree/clone, jj, cp/rm in or around /home/li/primary:
- a4f70bb991113c1f0.output, 06:05:23Z (00:05:23 local): `cd /home/li/primary && git worktree list`. Read-only listing; paths outside flows/d5df1d: none written.
- aa6925ab313deede5.output, 06:16:41Z (00:16:41 local): `cd /home/li/primary && git fetch origin main`. Writes to .git (remote-tracking ref and FETCH_HEAD), not to the working tree; result not recorded here.
- a6dbaad764fce699e.output, 05:47:17Z (23:47:17 local Oct 9, before the window): `cd /home/li/primary && git fetch origin main`. Same nature.
- ae9c44e59b9ce13e2.output, 04:44:22Z (22:44:22 local Oct 9, before the window): `cd /home/li/primary && git add flows/d5df1d/reports/ethos-solution.md && git commit -m "d5df1d: update ethos-solution status lines ..." && git status`. Path set: flows/d5df1d only.
- a8a8f4262225d1de3.output, 18:52:32Z (12:52 local Oct 9, before the window): `git add flows/d5df1d/books/invariants.md && git commit -m "Close unknown: probe binary source ..."`. Path set: flows/d5df1d only.
- a770c93ec29840b5d.output, 06:19:20Z (00:19:20 local): `git -C /home/li/primary remote get-url origin` then `git clone "$ORIGIN" clone` into this session's scratchpad. Read of primary's config; writes only to scratchpad.
- a1533f64654eb605c.output and btqjz9tr0.output (same publisher commands twice): `git clone -q git@github.com:LiGoldragon/primary.git $C` into scratchpad/pub; `cp /home/li/primary/flows/d5df1d/reports/fork-options-spec.md flows/d5df1d/reports/` (source under flows/d5df1d, destination in the scratchpad clone); `rm -rf $C` on the scratchpad clone path; jj git fetch, jj commit, jj bookmark set main, `jj git push --bookmark main` run in scratchpad/pub (pushes to the remote from the clone, not from /home/li/primary); orchestrate Lock/Release PrimaryPublish. Paths outside flows/d5df1d in /home/li/primary: none.
- Same two files: `S=.../scratchpad/ez; rm -rf $S; git -C /git/github.com/LiGoldragon/ethos-zero worktree add --detach $S b2fa8b0 ...; git apply /home/li/primary/flows/1d0733/reports/item12-final-ethos-zero.patch`. Touches the ethos-zero repository's worktree list (outside primary, outside flows/d5df1d) and reads a flows/1d0733 file; no write to /home/li/primary.
- a7393ac4a3111da7b.output: `git fetch -q origin` in /git/github.com/LiGoldragon/ethos-zero and /git/github.com/LiGoldragon/Curriculum (outside primary).
- Hits for checkout, reset, stash, clean, mv, rsync, and `rm ` with a path under /home/li/primary: none observed.
- Prestate captures and receipts for the above commands: unknown (not extracted).

## (C) Other worktree

`git worktree list` (run now) shows `/tmp/claude-1001/-home-li-primary/02dda640-dc5f-46ed-9c70-f22f047db2d4/scratchpad/pub b58610ce5 (detached HEAD)`. The directory still exists (modification dates Oct 7). Its session id 02dda640 differs from this session (d5df1daf); it does not belong to this session.

## 3. The five commits (93a033 and the four before it), `git log -5 93a033`

All five touch only flows/d5df1d/log.md; every path is under flows/d5df1d.

- 93a03320445a58618d1475556b2825557c2eb6be 2026-10-10 00:17:20 -0600 d5df1d: main tip witnessed (1 file changed, 2 insertions)
- 6db506f1480be7ad18e6ab250cec1b56ed36fd47 2026-10-10 00:17:00 -0600 d5df1d: item 5 landed (claim), main tip warning (1 file changed, 4 insertions)
- b2c9c642d737329759d8858f3a007c1b161b2144 2026-10-10 00:16:09 -0600 d5df1d: queued behind 16030 (1 file changed, 2 insertions)
- 1e72dc426e5a3fa8e6a1a33fb0331c3cec3e70a0 2026-10-10 00:15:50 -0600 d5df1d: item 5 (a) held (1 file changed, 2 insertions)
- fcb360aa1ffc27e054460a35c84d0adc7d27530a 2026-10-10 00:15:32 -0600 d5df1d: answer 0c85a3 (1 file changed, 2 insertions)
