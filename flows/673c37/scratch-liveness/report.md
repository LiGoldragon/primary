# Scratchpad cleanup on ouranos, 2026-11-08 (Fable's /tmp ruling)

Scope: Claude session scratch directories /tmp/claude-1001/<project>/<session-uuid>. Nothing else in /tmp was touched; loose files at the top of /tmp/claude-1001 were not touched.

Liveness: a session counts as running when herdr lists it (herdr-ids.txt), a process holds an open file or cwd in it or its transcript (fd-ids.txt), or a claude command line names it (cmd-ids.txt). Rechecked immediately before deletion (herdr-ids-2.txt, open-dirs-2.txt): no overlap.

Kept (196 + 13), listed in kept.tsv and held-protected-names.txt:
- 9 running sessions.
- 171 with any file changed in the last 48 hours: liveness not proven dead (a Claude Desktop session cannot be identified by id).
- 16 whose path is cited in a flow directory (referenced-ids.txt): the owning flow decides.
- 13 holding files named for protected evidence (2931b9, 01e4a4, 0532, 0533, e75baa, 705e10, capsule, preflight): protected-name-hits.txt.

Deleted: 2495 directories, 384869 files, 13.2 GiB; each listed with its size and file count in deleted-manifest.tsv before deletion. Root disk free went from 151 to 164 GiB.
