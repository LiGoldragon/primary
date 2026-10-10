# Side-branch repair in the shared Primary working copy

Method: `jj log`, `jj op log`, `jj diff`, `git diff`, `git patch-id`,
`git ls-remote origin main` and `git merge-file -p` (on scratch copies)
run in /home/li/primary by a subflow of c64ee3, 2026-09-29 from 15:41.

## Return point

JJ operation before the first change (15:42:54, "snapshot working copy"):

    48bea7b80d17a70d01927df4a740d1116cdbefe077744935f2169b1ce88c9006f546162246a444ce47b1f94e1763d69aec13444faf26cf3ac4c50491dbf4dcdd

## Before

- `main` = `main@origin` = remote `refs/heads/main` = 9de3b469aa5d
  "Record passive Zeus post-replug snapshot".
- `default@` 994d03e446ca sat on a side branch rooted on 5ce8d1fa1ccf
  (parent 0aecbfcd494d, an old main):
  5ce8d1fa1ccf c64ee3 answer to Field Astra; 8d69f40217c8 Record session
  reaping exploration and working request; 5eb10607cbd9 Record final
  recovery correction; 74c0f6c05ab9 Log bd0019: Anatomy Correction page
  evidence; be599a7b17b5 Record Clojure tooling exploration; 8a0efed72214
  Record living network and Codex update requests; 10362c89e591 Synthesize
  Zeus topology evidence and production questions; 2af39bdd212f Update
  Zeus synthesis with final Field witness; b196c7f0d5e0 Record Field book
  source and Zeus evidence; 0872bf2f7e23 Record Psyche triad and reply hook.
- 3c6769fb8b7e, undescribed, 12:47, a second head on 5eb10607cbd9,
  touching flows/1bc255/log.md and flows/caf622/log.md; every line it
  adds is already on main. A trial merge onto main conflicts in
  flows/1bc255/log.md (the same five lines on both sides).
- 10362c89e591 and 2af39bdd212f have the same patch-id as main's
  aed45b63a8e7 and 9da71be4764b (651b36c2..., d62a42c2...); the Zeus
  report at 2af39bdd212f equals main's.
- Missing from main: flows/d5b96b/notion/session-reaping.md,
  flows/bd0019/fable-last-presentation-evidence.md,
  flows/6f51ad/notion/clojure.md, flows/d5b96b/log.md (whole file),
  flows/d5b96b/vision/cluster-survey.md, and appended lines of
  flows/bd0019/log.md and flows/6f51ad/log.md.
- Uncommitted in `default@` (diff saved before the change, 592 lines):
  flows/6f51ad/vision/clusterSurvey.md, flows/7328f4/log.md,
  flows/7328f4/reports/seat-records.md, flows/bd0019/log.md,
  flows/bd0019/page-books-psyche-digest.md.
- Other workspaces: 1bc255-record@ on 9de3b469aa5d,
  primary-1bc255-log-9207@ on 9100575c8445; neither on the side branch.

## 5ce8d1fa1 against 0925daa46

Both change only flows/c64ee3/log.md from blob 77d59ef3f to blob
4f137b7a4; patch-id 2472310cbb33 for both; 0925daa46 is an ancestor of
main.

## Steps
1. `jj rebase -r 3c6769fb -d 0aecbfcd494d`: the undescribed head was moved
   off the side branch onto its old base, unchanged (now be7ca128c46d,
   change tukwynmx). It was not carried to main: its lines are already
   there.
2. `jj rebase -s 8d69f402 -d main --skip-emptied` (main 9de3b469aa5d):
   10362c89e591 and 2af39bdd212f were abandoned by JJ as already present
   in main. Conflict in the working copy only, flows/7328f4/log.md: main
   had received the two Fable paragraphs the file already held, and the
   flow had appended a third. Both sides only appended; resolved to main's
   lines followed by the third paragraph, each once.
3. Main moved to dc6da6b34f50 (7328f4 seat records, from another
   checkout) and a flow committed "Add Field state book preview" in
   `default`. `jj rebase -s f1d05c24 -d main --skip-emptied`: no conflict.
4. `jj bookmark set main -r 1182ee4b20d9`; `jj git push --bookmark main`
   moved the remote forward from dc6da6b34f50 to 1182ee4b20d9.
5. 5ce8d1fa1ccf had no children; `jj abandon 5ce8d1fa1`.

## After

- `main` = `main@origin` = remote main = 1182ee4b20d9. Carried commits in
  order, author li, messages unchanged: afc38368ac56 Record session
  reaping exploration and working request; 824364523d65 Record final
  recovery correction; d6c0add9779e Log bd0019: Anatomy Correction page
  evidence; b4c33ec7f9c3 Record Clojure tooling exploration; 52fa27909beb
  Record living network and Codex update requests; 5e4d66a21b09 Record
  Field book source and Zeus evidence; eba607fbed19 Record Psyche triad
  and reply hook; 1182ee4b20d9 Add Field state book preview.
- `default@` sits on main. The four files and
  flows/d5b96b/vision/cluster-survey.md are on origin/main; every line
  added by the side commits is present in origin/main's files (the Zeus
  report equals its final side version).
- Uncommitted additions in flows/6f51ad/vision/clusterSurvey.md,
  flows/bd0019/log.md and flows/bd0019/page-books-psyche-digest.md are
  line-for-line those of the before-state; the 7328f4 files now equal
  main, which received them from the flow's own commit.
- Stale `push-*` bookmarks moved locally with the rebase; their remote
  copies still name the old side commits.
