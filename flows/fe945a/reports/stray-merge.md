# Stray logging merged onto main

Subflow of fe945a, 2026-10-01, carrying out the living's ruling: land all flow logging not on main, stop diverging, remove stray checkouts.

## Landed

Three commits built on main in a temporary jj workspace (fe945a-stray), rebased onto the then-current main, pushed as main 15a9ee98d2b4:

- 5fe1bcab01f0: psyche records. 72 vision/notion files added, 27 extended.
  Added per flow: 48cff7 24, 840e42 19, af762b 5, 0d557b 4, e71dab 3, 139366 2, 6fe957 2, b666e7 2, d9961c 2, and 1 each in 19ff9f, 5ac3a3, 6db4fe, 6f51ad, b7da5d, bd0019, cf7879, d5b96b, efa157.
  Extended: 04db2fd2 4, 1ac573 2, b666e7 2, cf3553 2, and 1 each in 00f95a, 01a03952, 01a03d6e, 01a03eda, 01a03f49, 15b67974, 31147a, 504461, 5851f4, 68512643, 98fbfa47, b675f3d9, b7da5d, b81560, e51411, e8c4cc61, f426777b.
- 7ed4d8c9dd0c: summaries. New in 5ac3a3 and 6fe957, extended in d5b96b.
- 15a9ee98d2b4: logs, reports, witnesses, index. 130 files added and 107 extended. That is 105 log.md files (11 new, 94 extended), the rest reports and witnesses, and 9 flows/index.md lines.
  Most added files: cf7879 25, 5f4fea 17, d9961c 13, 6fe957 10, d5b96b 9, 0d557b 8, efa157 8, 840e42 7.

The earlier empty commit 39893cc64da6 ("Record found Field Sol launch evidence...") was pushed by mistake. Another flow had already committed those changes. It does no harm.

## Method

- Sources: every commit not reachable from main. That covers all refs (branches, refs/jj/keep, codex refs) plus 104 dangling commits from git fsck: 31,472 commits with 29,565 heads.
- For each head, the flows/ files it changed against its merge-base with main were collected. Jj-conflicted commits were read from their .jjconflict-side-* trees.
- Path filter: flows/index.md, flows/*/log.md, flows/*/summary.md, flows/*/{vision,notion,reports,witnesses}/**.
- Merge unit: the paragraph.
  - A paragraph counts as present if its whitespace-free text is already in the file, or it is a fuzzy match (0.85) for a paragraph there.
  - For vision, notion, reports and summaries, it also counts as present if it already appears anywhere under main's flows/, Vision/, Intent/ or vision-raw/.
  - log.md is checked against its own file only. A psyche quote embedded in a log entry is never dropped because it also lives elsewhere.
- Files on main get missing paragraphs appended, along with their section heading when that heading is not already present. New files take the fullest stray version and append missing paragraphs from the others in chronological order.
  - Log and psyche files are append-only by nature, so every version was unioned.
  - Reports, witnesses and summaries on main took only stray versions newer than main's last change. They sit under a "Recovered from unlanded commits" heading, or a whole recovered version is shown under its commit id when more than 30% of it was missing.
- jj conflict-marker lines from stray snapshots were removed.
- flows/index.md got only lines for flow ids absent from the index whose directory exists on main.
- Files of seats still running (d32329, 5104af, e2a70a, 098f27, fe945a) were only appended to. Their workspaces were not touched.
- Check: every non-trivial line in the vision, notion, log and summary files of the 24 named workspace and worktree heads and of worktree-flow-840e42 is present in the same file on the pushed main. All 2,779 lines were found and 0 are missing. All 19 flows/840e42/vision files are present. A first run had left out 4 verbatim psyche quotes in flows/d5b96b/log.md because they were already on main elsewhere. The final rule checks log.md only against its own file, so the quotes are now there too.
- Text was scanned for credentials. Only references and descriptions appear. Pairing material had already been omitted at its source.

## Left out (still reachable in history)

- Everything outside flows/: skills, tools, code, the root scripts of worktree-flow-840e42, generated trees. Not collected.
- 1,715 flows/ paths outside the logging set, for example launches/, messages/, receipts/, build-* output, psyche-block/.
- 362 files under logging dirs that are not logging types: dotfiles, scripts, a cargo target/ cache under flows/857335/witnesses, unknown extensions.
- 16 data dumps: files under data/ or logs/, .csv, .log, and .json over 500 lines. Examples are the state-of-field-20260921 data, the 5f4fea item20/item27 measurements, and the cf7879 order10 build log.
- 422 reports, witnesses and summaries whose stray versions are older than main's later rewrite (superseded drafts).
- 198 files deleted on main after the stray version, mostly the 2026-09-02 consolidation of child flows into parents and the removal of redundant raw records on 2026-08-24. Re-creating them would undo deliberate moves.
- 44 new files whose whole content is already on main elsewhere.
- 2 non-line files that differ from main.
- Binary files and files over 1 MB.
- Branches and bookmarks were kept, so their non-logging work stays reachable.

## Removed

- jj workspaces: 1bc255-record (/home/li/wt/primary/1bc255-record), primary-1bc255-log-9207, b666e7-defect, b666e7-start, b666e7-fable, b666e7-latest, b666e7-publish (their /tmp directories deleted), and the temporary fe945a-stray.
- git worktrees: /tmp/d5-record-push-0930 through 0944 (15). The locked worktree-flow-840e42 entry was unlocked and pruned; its directory was already gone. The branch itself remains.
- Not removed: /tmp/primary-b666e7-clone.eN1oCV, a separate empty jj repository outside the brief's list. Also /home/li/wt/primary/e167d8-cleanup, a directory that is not a registered workspace.
- The shared default workspace was rebased onto the new main, so the landed files are present there. The running seat's uncommitted flows/e2a70a/log.md was carried over unchanged.

## Sources

- Inventory raw lists: /tmp/claude-1001/-home-li-primary/fe945a2e-c785-4af4-9a46-766b6ea512e8/scratchpad/ws/ (targets.txt, heads.txt, recent-check.txt).
- Merge tooling and intermediate data (ephemeral): the same scratchpad's m/ directory, holding collect.py, merge.py, apply.py, versions.json, merged.json and skipped_by_reason.json.
- Landed commits: 5fe1bcab01f0, 7ed4d8c9dd0c, 15a9ee98d2b4 on origin main.
- Live seat roster: hm-list, 2026-10-01.
- Ruling: the living, STT, 2026-10-01, quoted in the fe945a brief.
