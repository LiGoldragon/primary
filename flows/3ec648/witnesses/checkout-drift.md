# Checkout drift: published files left the Primary working copy

Method: read-only. `jj --ignore-working-copy op log`, `op show`, `--at-op ... file list -r @`, `git reflog`, file mtimes, `git log` in Curriculum and Primary. Taken 2026-10-02 after 16:47 -0600.

## Affected paths (verified)
- `flows/3ec648/vision/voices.md`, `flows/3ec648/reports/handover-state.md`: present in the working-copy tree at op b336dc08e2b2 (16:36:08), absent at op 7af09c2bb9e7 (16:37:12). `flows/3ec648/log.md`: present at both ops, but the 7af09c2bb9e7 snapshot records it as +2 lines (content changed; the drop of log.md is not shown by the listing). `flows/dea0ba/vision/voices.md` present throughout.
- `flows/index.md` changed by the same op: NOT verified (op show lists only the commits' own changes; the stat shows no index.md line). Unverified.

## The op (verified)
- 9595230fc263, 16:36:10, `jj rebase -r nuxqquvzqmsp -d main@origin`, run in default@. Moved default@ xovwuvrs from 71b9c5fc (parent 4a076b29, the lane commit) to 2d2ee315 (parent 86d70970). The rebased lane commit became 09147149, shown `(conflict)` by op show.
- git reflog HEAD: 4a076b29e at 16:36:08, 86d70970d at 16:36:10.
- Next snapshot 7af09c2bb9e7 (16:37:12) lacks the files (tree listing above).
- Same pattern: bea010de2ce7 (16:26:41, `rebase -r wrwxvvslplvp -d main@origin`, default@ qpypppop cf79cf26 -> 5b4fc7a3; tree listing after it shows only log.md under flows/3ec648, which is consistent with a drop but the pre-op tree could not be compared: unverified as "dropped log.md"). a6840686e548 (16:26:53, `jj rebase -r @- --onto main@origin`, default@ pxykrmto 8f2c5f3c -> e4605316): flows/91ea9f lost `books/kinds-and-parameters-deep-dive/source.md` between b94133c8ac4a and a6840686e548 listings (verified).
- Inference, not observed: `rebase -r` moves only the named commit; its child @ is reparented onto the old parent, and jj checks out a tree without that commit's files.

## Publication ops (ids verified in op log)
- Lane open: 2acc9c571b56 (commit), bea010de2ce7 (rebase), a6a23a559bb5 (bookmark main -> 3f3b2aca), c4638c81c1b9 (push).
- Second publication: f864a2bdd68f (commit), 9595230fc263 (rebase), 5ab2578cf3a6 (bookmark main -> 09147149); repaired in workspace `ws` (60c95a3f9de6 squash into 09147149), pushed as 0a47a553 by d70bd131171d.
- Third: df5aec349901 (commit), 720bcd424a31 (rebase cf6bdca3); squashed in workspace `ws2` (5fbc2c4ddf5c) into 30fc56bf, which is 9e247d23 on main (9e247d23d in Primary log; the 30fc56bf to 9e247d23 id mapping is by title, "Close 91ea9f", not by op).
- e258c1fc18ba (ws2 commit) gave 83cde648; pushed by 88be304bd9fd (16:38:18).

## Working copy and main (verified)
- Before: default@ 71b9c5fc; main@origin 26826d3d (op 796152d0fa9b/d0ee48f06f8c, 16:33:43).
- During drift: default@ 2d2ee315, then 1667571d, both on parent 86d70970.
- After restoration: default@ c99d8308, parent 346d2dd4; main@origin 8a137d6e (op 9ff58d552fe8, 16:44:14).

## update-stale and restoration
- update-stale: no op recorded in the op log.
- Restoration: done outside jj; mtimes of voices.md and handover-state.md are 16:42:54.667/.668. Byte-identity with origin/main was reported by the earlier subflow and not re-checked here: unverified. Snapshot op 0e6067a75660 (16:44:09) recorded handover-state.md (+237), voices.md (+11), skills.md (+17), log.md (+5) and the where-the-edit-goes book.

## Skill text at the time
- The sentence "Under the lock, the sequence is: jj commit of own paths; jj git fetch; jj rebase -r of that one commit onto main@origin; jj bookmark set main; jj git push; release. Nothing else is rebased." was added in Curriculum 3380c82 (12:35) and removed in ae403f5 (12:36). Primary's generated tree carried it from 899a565c5 (16:23:16) until 7297f49e6 (16:26:43). Which text the publishing flow had loaded at 16:36 is not recorded: unverified.
- Authored source: `/git/github.com/LiGoldragon/Curriculum/skills/compensation-primary-commit.md`, HEAD d351f1c (duplicate form, no rebase).
