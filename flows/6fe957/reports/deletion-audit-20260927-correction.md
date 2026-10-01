# Correction: line-level deletion audit — 2026-09-27

This corrects the earlier file-status audit. A zero count of deleted paths does not establish zero deleted lines in modified files.

Repository context at audit: native primary Git `HEAD` was `a8e9ae3b59c357f630bb2dbdc06b89c4237ddd49`; JJ working copy had uncommitted additions/modifications; remote and local `main` both read as `18baad590b13ff5dfb4e9855dcd492580f9b4b5a`. `git merge-base HEAD main` was `9c3d6bf87edf94aeec688826e91ab2134b43abcf`.

Line numstats:

- Working tree relative to HEAD: 9 paths, +370/-0.
- HEAD to main: 139 paths, +16,606/-147.
- Main to HEAD, the reverse comparison a UI may present as applying the current checkout over main: 139 paths, +147/-16,606.
- `b8bebfa418ca3178e196fa3d8d9480b8b2a456ad` relative to its parent: 1 path, +2/-0.

The reverse `main → HEAD` range exactly explains an approximately 16,000-line deletion display. Its largest apparent deletions are files that are additions on `main` beyond the local HEAD, including `flows/8904b1/log.md` (3,269), `flows/38f337/successor-prompt-fable.md` (648), and `flows/38f337/handoff-fable.md` (448). Immutable blobs for those three paths are present in `main`; real `origin/main` points to the same commit. This is therefore a base-direction/materialized checkout comparison, not evidence that an agent destructively deleted those contents from published main.

The direct forward range also contains real edits within modified files: 147 deleted lines total. Largest: `flows/56ae53/receipts/roster.md` +118/-45. This bounded audit does not attribute authorship beyond commit metadata, nor audit external UI state. No rename/binary rows occurred in these numstats.

Retained raw numstats: `/var/tmp/flow-home-delete-numstat-WORKTREE-6fe957.txt` (SHA-256 `4fd498e8e9238e9ef360db88ffb28673034f6e22a986a6ddcae6b56b88aa99ce`), `/var/tmp/flow-home-delete-numstat-HEAD-6fe957.txt` (SHA-256 `b914a369f06d804dd8cc2e7f6cf8b42f3c9c23d14e803e0383c746b215b7add8`), and `/var/tmp/flow-home-delete-numstat-main-to-head-6fe957.txt` (SHA-256 `a9e4115c0a1b12c2b08bda004b5ff14df2b6edabe17ce8d5a50761dab6472e6c`).
