# b7ba00 working-copy loss — 2026-09-26

This flow's uncommitted `flows/b7ba00/receipts/readiness-announce.md` and the `log.md` lines it had appended between 10:04 and 10:07 (-06:00) were lost from the shared `/home/li/primary` jj checkout, dropped by a working-copy replacement (`import git head`, op `6b1b894817e5`) that a concurrent-operation reconcile (`6cbe762d880f`) then made permanent, after two earlier field-clj `#restored` whole-repository rewinds had already returned both files to uncommitted state.

## Operations, 10:04:57–10:07:04 (time | op | description | recorded args)

```
10:04:57 9181b713a931 snapshot working copy        jj git remote list
10:04:58 053e1cb640a1 commit a4e919d40fd5           jj commit -m 'b7ba00: launch…' root-file:"flows/b7ba00/log.md" root-file:"flows/index.md"
10:04:58 c428b7d7e868 restore to operation 9181b7…  jj op restore 9181b713a931…      <-- #restored #1
10:05:31 4281f411374c new empty commit              jj new main@origin               (e167d8)
10:05:31 ab5b836f1227 commit 679e3db28bd5           jj commit -m 'e167d8: log b7ba00 ready'
10:05:31 6978ea48f38f point bookmark main           jj bookmark set main -r @-
10:05:32 ed0defc60891 import git head / 3293676c66da snapshot   jj log -r 'main | @ | @-' …
10:05:33 ad59a0e1b7b2 push bookmark main            jj git push --bookmark main
10:05:33 d15c15f47dd1 reconcile divergent operations (parents 3293676c66da, ad59a0e1b7b2)
10:05:42 6e4e83e26531 snapshot working copy         jj git remote list
10:05:43 aad306c1ec16 commit f33af181edf3           jj commit -m 'b7ba00: readiness announce receipts…' root-file:"flows/b7ba00/receipts/readiness-announce.md"
10:05:43 ca204d2dde95 restore to operation 6e4e83e2… jj op restore 6e4e83e26531…     <-- #restored #2
10:05:52 d5a2a817f474 rebase commit 339ca09e46d0 and descendants   jj rebase -d main
10:06:09 0b37b8cbd6b7 import git head               jj git remote list   (WC -> empty 309cea43f6c5; next snapshot re-picked files from disk)
10:06:09 817639cf897c snapshot / 6c671d02b33f commit 4897a60f1e71   jj commit -m 'b7ba00: launch…' (log.md + index.md)  -> bd987fca
10:06:10 6bfd49f44874 point bookmark main -r bd987fca7b0e
10:06:12 a6193c428250 push bookmark main            jj git push --remote origin --bookmark main
10:06:17 cb255a346b28 import git head / 650d777f8f7a snapshot   jj diff -r @- --name-only   (WC 86fd0336e3ff: receipts present, crossover line present twice)
10:06:23 fcfe82969b75 new empty commit / 6e18606c0532 snapshot / 28f4ed18a22c commit / 31ffc437b0b6 bookmark   jj commit -m 'e167d8: log credentials ruling'
10:06:23 6b1b894817e5 import git head               jj diff -r bd987fca7b0e --name-only    <-- WC replaced by EMPTY c40d44408d5a
10:06:25 236aa88e0ace push bookmark main            jj git push --bookmark main            (concurrent sibling, WC still 86fd0336e3ff)
10:06:27 6cbe762d880f reconcile divergent operations (parents 6b1b894817e5, 236aa88e0ace)  jj log … --ignore-working-copy -R /home/li/primary
10:06:57 8d10f40cf320 new empty commit  jj new main@origin ; 305aff78f663 snapshot -> files absent from disk
```

## Culprit operations

`jj diff --from 86fd0336e3ff --to c40d44408d5a --name-only` is exactly:
`flows/31147a/log.md, flows/38de5b/log.md, flows/b7ba00/log.md, flows/b7ba00/receipts/readiness-announce.md, flows/index.md`.
The first operation whose working-copy commit lacks both `flows/b7ba00/receipts/readiness-announce.md` and the `- Received #msg from 38de5b (crossover)` line is **6b1b894817e5, 10:06:23.975, "import git head", recorded args `jj diff -r bd987fca7b0e --name-only`**. It replaced working-copy commit 86fd0336e3ff (which held both, uncommitted) with a fresh **empty** commit c40d44408d5a on git HEAD 12b586e41ee4. The concurrent sibling 236aa88e0ace still had them; **6cbe762d880f "reconcile divergent operations" (10:06:27) adopted the import-git-head side**, making the loss permanent. Disk deletion is observable by 305aff78f663 (10:06:57).
(An identical earlier import-git-head, 0b37b8cbd6b7 at 10:06:09, also emptied the WC commit but the snapshot 0.06s later recovered the files from disk.)

In the window: two `jj op restore` (c428b7d7e868, ca204d2dde95 — both field-clj `#restored`), one `jj rebase -d main` (d5a2a817f474), several `jj new main@origin`, and two `reconcile divergent operations` (d15c15f47dd1, 6cbe762d880f). **No `jj abandon`, no `jj edit`, no path-level `jj restore`.**

## field-clj `#restored` mechanism

Jar `/nix/store/a15b2pbqw7m66cix9l5qzrayjp8mdrgi-field-clj-uberjar/share/field-clj/field-clj.jar`, sources `field_clj/commit.clj`, `field_clj/jj.clj`:

```clojure
;; jj.clj
(mark [_ root]
  (let [result (run root "jj" "op" "log" "-n1" "--no-graph" "-T" "id ++ \"\\n\"")] ...))
(restore [_ root operation]
  (let [result (run root "jj" "op" "restore" operation)]
    (if (failed? result) (refused :restore-failed result) (ok operation))))
;; commit.clj
(defn- restoration [{:keys [committer root operation]}]
  (when (and root operation
             (not= operation (ok-value (call :committer/mark mark committer root))))
    (let [[status value stderr] (call :committer/restore restore committer root operation)]
      (if (= :ok status) (schema/tagged 'restored value) ...))))
```

It runs **`jj op restore <op-id>`** — a whole-repository operation rewind to the op id captured before the commit — not `jj restore`, and **not scoped to the named paths**: it reverts every bookmark, commit and the working-copy pointer created since that mark, including other flows' operations interleaved in the same shared repo.

## Observations (seen in the op log)

- field-clj's refusal path rewound b7ba00's two commits (a4e919d40fd5 at 10:04:58, f33af181edf3 at 10:05:43), returning both files to *uncommitted* working-copy state.
- Uncommitted, they were then carried in WC commit 86fd0336e3ff and dropped by import-git-head 6b1b894817e5, with reconcile 6cbe762d880f choosing that side.
- log.md's crossover line was present **twice** in 86fd0336e3ff (committed copy in bd987fca plus a re-append), which is why the committed copy survived and the appended one did not.

## Hypotheses (not established)

- Something outside jj moved git HEAD around 10:06:09 and 10:06:23, triggering the two import-git-head ops; the recorded args (`jj git remote list`, `jj diff …`) are read-only commands that merely observed it. field-clj's `target` step does run raw `git --git-dir … remote get-url --push`, which is read-only.
- The reconcile's choice of the empty-WC side may be jj's ordinary concurrent-op merge rule rather than anything flow-specific.

## Unknowns

- Which process moved git HEAD to 12b586e41ee4 before 10:06:23 — the op log does not record it.
- Why 0b37b8cbd6b7 recovered the files and 6b1b894817e5 did not (no snapshot op followed the latter on its branch before the reconcile).
- Which flow ran `jj rebase -d main` at 10:05:52 and the `jj new main@origin` at 10:06:57.

---

Witnessed by a subflow of b7ba00 from `jj op log`; the field-clj source was read from the installed jar's sources.
